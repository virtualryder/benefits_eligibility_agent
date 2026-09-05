"""IdentityStack — federation-ready Cognito, NO built-in users (P0-6), Gate-B pilot posture (B3).

Production identity is a federated enterprise IdP (Okta / Entra ID / Ping) through this pool — see
docs/IdP-Federation-Reference.md. This stack deliberately creates ZERO users and ships ZERO passwords;
sandbox demo users exist only in the legacy shell path behind an explicit SANDBOX_IDENTITY=1
acknowledgment.

Gate-B (`identity_mode="pilot"`): MFA becomes REQUIRED (software token only — no SMS, which is not
phishing-resistant and drags in an SNS role), Cognito threat protection (advanced security) is
ENFORCED, and an enterprise OIDC IdP can be attached AS IaC (issuer/client id via context, client
secret via a Secrets Manager dynamic reference — never plaintext in the template). Federated users
land in the SAME pool and hit the SAME deny-by-default Cedar policies as native operators."""
import aws_cdk as cdk
from aws_cdk import (aws_cognito as cognito, aws_iam as iam, aws_wafv2 as wafv2,
                     custom_resources as cr)
from constructs import Construct


class IdentityStack(cdk.Stack):
    def __init__(self, scope: Construct, cid: str, *, prefix: str,
                 identity_mode: str = "sandbox", federation: dict | None = None,
                 tenants: tuple = (), waf: bool = False, **kw):
        super().__init__(scope, cid, **kw)
        if identity_mode not in ("sandbox", "pilot"):
            raise ValueError(f"unknown identity_mode {identity_mode!r}; choose sandbox or pilot")
        pilot = identity_mode == "pilot"

        self.pool = cognito.UserPool(
            self, "Pool", user_pool_name=f"{prefix}-identity",
            self_sign_up_enabled=False,
            # Gate-B: REQUIRED software-token MFA for every operator; sandbox keeps OPTIONAL so the
            # disposable validation loop stays scriptable. SMS is disabled in both modes.
            mfa=cognito.Mfa.REQUIRED if pilot else cognito.Mfa.OPTIONAL,
            mfa_second_factor=cognito.MfaSecondFactor(sms=False, otp=True),
            # Threat protection. Replaces the deprecated `advanced_security_mode`,
            # which CDK now warns will be removed in the next major release AND
            # which hard-fails synth on some 2.2xx versions with "you cannot enable
            # Advanced Security when feature plan is not Plus" - i.e. the HARDENED
            # posture was the one that would not synthesize. Feature plan is now
            # set explicitly so the pilot posture is version-stable.
            feature_plan=(cognito.FeaturePlan.PLUS if pilot
                          else cognito.FeaturePlan.ESSENTIALS),
            standard_threat_protection_mode=(
                cognito.StandardThreatProtectionMode.FULL_FUNCTION if pilot
                else cognito.StandardThreatProtectionMode.NO_ENFORCEMENT),
            password_policy=cognito.PasswordPolicy(
                min_length=14, require_lowercase=True, require_uppercase=True,
                require_digits=True, require_symbols=True),
            removal_policy=cdk.RemovalPolicy.RETAIN,
        )

        # Gate-B: enterprise OIDC federation as IaC. The client SECRET arrives as a Secrets Manager
        # DYNAMIC REFERENCE (resolved by CloudFormation at deploy) — it never appears in the template.
        self.federated_idp = None
        fed = federation or {}
        if fed.get("issuer_url") and fed.get("client_id"):
            secret_arn = fed.get("client_secret_arn") or ""
            client_secret = (cdk.SecretValue.secrets_manager(secret_arn).unsafe_unwrap()
                             if secret_arn else "")
            self.federated_idp = cognito.UserPoolIdentityProviderOidc(
                self, "EnterpriseIdp", user_pool=self.pool,
                name=f"{prefix}-enterprise",
                issuer_url=fed["issuer_url"], client_id=fed["client_id"],
                client_secret=client_secret,
                scopes=["openid", "email", "profile"],
                attribute_mapping=cognito.AttributeMapping(
                    email=cognito.ProviderAttribute.other("email")),
            )
            # Hosted-UI domain so the OIDC round-trip has an endpoint (prefix must be dns-safe).
            self.pool.add_domain("FederationDomain", cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=f"{prefix}-eligibility".replace("_", "-")))

        providers = [cognito.UserPoolClientIdentityProvider.COGNITO]
        if self.federated_idp is not None:
            providers.append(cognito.UserPoolClientIdentityProvider.custom(self.federated_idp.provider_name))
        self.client = self.pool.add_client(
            "GatewayClient", user_pool_client_name=f"{prefix}-gw",
            auth_flows=cognito.AuthFlow(user_srp=True),   # no USER_PASSWORD_AUTH in the CDK path
            generate_secret=False,
            supported_identity_providers=providers,
        )
        if self.federated_idp is not None:
            self.client.node.add_dependency(self.federated_idp)

        # Hybrid multi-tenant (phase 107/108): tenant membership is a Cognito GROUP (tenant_<id>) because
        # access tokens carry cognito:groups but not custom attributes; Cedar require_tenant and the
        # gateway interceptor both read it. A caseworker holds benefits_caseworker + exactly one tenant group.
        self.tenant_groups = {}
        for t in tenants:
            self.tenant_groups[t] = cognito.CfnUserPoolGroup(
                self, f"TenantGroup-{t}",
                user_pool_id=self.pool.user_pool_id, group_name=f"tenant_{t}",
                description=f"Hybrid multi-tenant membership: tenant {t}")
        cognito.CfnUserPoolGroup(self, "ReviewerGroup", user_pool_id=self.pool.user_pool_id,
                                 group_name="benefits_caseworker",
                                 description="Qualified benefits caseworkers (Cedar role group)")

        # ── #170: WAFv2 on the auth front door ───────────────────────────────
        # The AgentCore Gateway and Runtime are MANAGED endpoints and are NOT WAF-associable resource
        # types (WAFv2 associates only with ALB / API Gateway / CloudFront / AppSync / Cognito user pool
        # / App Runner). The Cognito user pool IS the token-issuance surface for the whole runtime path,
        # and it IS associable — so the perimeter WAF sits here (`-c waf=1`): a REGIONAL Web ACL with the
        # AWS managed Common Rule Set + a per-IP rate limit, default-allow. (No ATP managed rule set and
        # no CAPTCHA action: Cognito forbids ATP on a pool and CAPTCHA can break managed-login TOTP.)
        self.web_acl = None
        self.web_acl_arn = ""
        if waf:
            self.web_acl = wafv2.CfnWebACL(
                self, "AuthWebAcl",
                name=f"{prefix}-auth-waf", scope="REGIONAL",
                default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
                visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                    sampled_requests_enabled=True, cloud_watch_metrics_enabled=True,
                    metric_name=f"{prefix}-auth-waf"),
                rules=[
                    wafv2.CfnWebACL.RuleProperty(
                        name="CommonRuleSet", priority=1,
                        override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                        statement=wafv2.CfnWebACL.StatementProperty(
                            managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                                vendor_name="AWS", name="AWSManagedRulesCommonRuleSet")),
                        visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                            sampled_requests_enabled=True, cloud_watch_metrics_enabled=True,
                            metric_name=f"{prefix}-waf-common")),
                    wafv2.CfnWebACL.RuleProperty(
                        name="RateLimitPerIp", priority=2,
                        action=wafv2.CfnWebACL.RuleActionProperty(block={}),
                        statement=wafv2.CfnWebACL.StatementProperty(
                            rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                                limit=2000, aggregate_key_type="IP")),
                        visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                            sampled_requests_enabled=True, cloud_watch_metrics_enabled=True,
                            metric_name=f"{prefix}-waf-ratelimit")),
                ])
            self.web_acl_arn = self.web_acl.attr_arn
            pool_arn = f"arn:aws:cognito-idp:{self.region}:{self.account}:userpool/{self.pool.user_pool_id}"
            # Associate via an AwsCustomResource (AssociateWebACL / DisassociateWebACL) rather than the
            # native AWS::WAFv2::WebACLAssociation: for a COGNITO target that resource's CloudFormation
            # stabilization waiter hangs (found live 2026-09-05 — CREATE_IN_PROGRESS with no progress and
            # get-web-acl-for-resource still null). The API call returns immediately; propagation then
            # completes async. on_delete disassociates so the association follows the stack lifecycle.
            assoc = cr.AwsCustomResource(
                self, "AuthWebAclAssoc",
                on_create=cr.AwsSdkCall(
                    service="WAFV2", action="associateWebACL",
                    parameters={"WebACLArn": self.web_acl.attr_arn, "ResourceArn": pool_arn},
                    physical_resource_id=cr.PhysicalResourceId.of(f"{prefix}-auth-waf-assoc")),
                on_delete=cr.AwsSdkCall(
                    service="WAFV2", action="disassociateWebACL",
                    parameters={"ResourceArn": pool_arn}),
                policy=cr.AwsCustomResourcePolicy.from_statements([
                    iam.PolicyStatement(actions=["wafv2:AssociateWebACL", "wafv2:DisassociateWebACL",
                                                 "wafv2:GetWebACLForResource"], resources=["*"]),
                    iam.PolicyStatement(actions=["cognito-idp:AssociateWebACL",
                                                 "cognito-idp:DisassociateWebACL",
                                                 "cognito-idp:GetWebACLForResource"], resources=["*"])]))
            assoc.node.add_dependency(self.web_acl)
            cdk.CfnOutput(self, "WebAclArn", value=self.web_acl.attr_arn)
            cdk.CfnOutput(self, "WafAssociatedResource", value=pool_arn)

        cdk.CfnOutput(self, "UserPoolId", value=self.pool.user_pool_id)
        cdk.CfnOutput(self, "ClientId", value=self.client.user_pool_client_id)
        cdk.CfnOutput(self, "IdentityMode", value=identity_mode)
        cdk.CfnOutput(self, "FederationNote",
                      value=("Enterprise OIDC IdP attached as IaC; map IdP groups to benefits_caseworker "
                             "(docs/IdP-Federation-Reference.md)." if self.federated_idp is not None else
                             "No users are created by IaC; federate the enterprise IdP "
                             "(docs/IdP-Federation-Reference.md) or create operators out-of-band."))
