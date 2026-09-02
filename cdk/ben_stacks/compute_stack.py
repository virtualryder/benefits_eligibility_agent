"""ComputeStack (Benefits) — the governed tool Lambdas with explicit least-privilege IAM (P0-5/P0-7).

One function per manifest tool target, from a single staged asset bundle (tools + shared controls).
IAM is explicit and minimal per function: the audit writer can only PutItem the ledger + PutObject the
vault (with an explicit Deny on mutation/bypass); mask_pii can only Comprehend-detect + write the
sanitized store; the assessor/guards/drafter only read the sanitized store; the drafter only invokes
Bedrock. (`verify_income` is intentionally NOT deployed — see the note at the tool list.)
Benefits has ONE signing trust domain (only mask_pii signs a sanitized_ref — there is no external
authoritative source to sign), so a single per-deploy HMAC key suffices (GA-2 domain-split N/A).
Exact ARNs are exported — nothing downstream discovers by name (P0-7)."""
import aws_cdk as cdk
from aws_cdk import (aws_ec2 as ec2, aws_iam as iam, aws_kms as kms, aws_lambda as lambda_,
                     aws_logs as logs, aws_secretsmanager as sm)
from constructs import Construct

RUNTIME = lambda_.Runtime.PYTHON_3_12


class ComputeStack(cdk.Stack):
    def __init__(self, scope: Construct, cid: str, *, prefix: str, asset_dir: str, data,
                 provenance_secret: str = "", network=None, tenant: str = "",
                 guardrail_id: str = "", guardrail_version: str = "1",
                 identity=None, approvals_client_id: str = "", multitenant: bool = False, **kw):
        super().__init__(scope, cid, **kw)
        code = lambda_.Code.from_asset(asset_dir)
        cmk = None
        if getattr(data, "cmk", None) is not None:
            cmk = kms.Key.from_key_arn(self, "DataCmk", data.cmk.key_arn)
        common_env = {
            "AUDIT_TABLE": data.audit_table.table_name,
            "WORM_BUCKET": data.worm_bucket.bucket_name,
            # The pinned governed-core evidence writer reads AUDIT_BUCKET
            # (governed_core/controls/evidence.py: _env("AUDIT_BUCKET") or
            # "evidence-worm-<acct>-<region>"). Without this alias the WORM mirror
            # silently no-ops with worm_error=NoSuchBucket (found live on ben-demo,
            # 2026-08-24). WORM_BUCKET kept for anything reading the old name.
            "AUDIT_BUCKET": data.worm_bucket.bucket_name,
            "SANITIZED_TABLE": data.sanitized_table.table_name,
            "PENDING_TABLE": data.pending_table.table_name,
            "CASE_TABLE": data.case_table.table_name,   # R3-2 pass-by-reference store
        }
        # Gate-B B5: the deployment's pinned tenant (one agency per isolated deployment). Tenant identity
        # is DERIVED from this env, never from a request body (lib/controls/tenancy.py).
        if tenant:
            common_env["TENANT_ID"] = tenant
        # Hybrid multi-tenant (phase 107): tenant is derived per request from the gateway interceptor's
        # HMAC-signed injection (never the pinned env); MULTITENANT=1 makes the routing fail-closed.
        if multitenant:
            common_env["MULTITENANT"] = "1"
        # Per-deploy signing secret (P0-1). DEFAULT: a generated AWS Secrets Manager secret referenced
        # by ARN — never plaintext in the template. A context-supplied plaintext secret remains available
        # for disposable sandbox validation ONLY.
        self.signing_secret = None
        if provenance_secret:
            common_env["PROVENANCE_SECRET"] = provenance_secret   # sandbox-only path
        else:
            self.signing_secret = sm.Secret(
                self, "SigningSecret", secret_name=f"{prefix}/provenance-signing",
                description="Per-deploy HMAC key: signs mask_pii sanitized-artifact refs (single trust domain; rotate via new version; consumers re-read on cold start)",
                generate_secret_string=sm.SecretStringGenerator(password_length=64, exclude_punctuation=True),
                encryption_key=cmk)
            common_env["PROVENANCE_SECRET_ARN"] = self.signing_secret.secret_arn

        def fn(name, handler_module, env=None, timeout=30):
            # Observability review 2026-08-29: the log group is now UNCONDITIONAL —
            # 1-year retention must not be a side effect of the kms switch. CMK
            # encryption still applies only when a customer-managed key exists.
            log_group = logs.LogGroup(
                self, name.replace("-", " ").title().replace(" ", "") + "Logs",
                log_group_name=f"/aws/lambda/{prefix}-{name}",
                encryption_key=cmk, retention=logs.RetentionDays.ONE_YEAR,
                removal_policy=cdk.RemovalPolicy.DESTROY)
            net = {}
            if network is not None:
                net = dict(vpc=network.vpc,
                           vpc_subnets=ec2.SubnetSelection(subnet_group_name="app"),
                           security_groups=[network.lambda_sg])
            f = lambda_.Function(
                self, name.replace("-", " ").title().replace(" ", ""),
                function_name=f"{prefix}-{name}", runtime=RUNTIME, code=code,
                handler=f"{handler_module}.handler",
                timeout=cdk.Duration.seconds(timeout), memory_size=256,
                environment={**common_env, **(env or {})},
                environment_encryption=cmk, log_group=log_group,
                tracing=lambda_.Tracing.ACTIVE,   # X-Ray on every governed tool (obs review 2026-08-29)
                **net,
            )
            if cmk is not None:
                cmk.grant_decrypt(f)
            return f

        # Benefits governed tool set (manifest targets).
        self.ingest = fn("ingest-application", "ingest_case")   # R3-2: the only door for raw content
        self.intake = fn("intake-application", "intake_application")
        self.mask = fn("mask-pii", "mask_pii")
        self.assess = fn("assess-eligibility", "assess_eligibility")
        # NOTE: `verify_income` is deliberately NOT deployed. It is a reference implementation of an
        # AgentCore-Identity M2M connector to a benefits system of record, but no SoR exists for this
        # pilot: `SOR_URL` is never set, it is not a Gateway target (so Cedar cannot authorize it), and
        # it would always return `verified: false`. Shipping an unreachable Lambda that holds
        # `bedrock-agentcore:GetResourceOauth2Token` is privilege with no purpose — least privilege says
        # don't deploy it. The manifest lists it under `stubbed:`. Re-enable it here (and add it to the
        # gateway target map + set SOR_URL) only when a real read-only SoR connector is in scope
        # (Gate-C, see BENEFITS-PILOT-READINESS-PLAN.md).
        self.redetermine = fn("redetermine", "redetermine")
        self.overpayment = fn("overpayment", "overpayment")
        # Guardrail-pinned drafting (G1, obs review 2026-08-29): the drafter already honors
        # GUARDRAIL_ID / GUARDRAIL_VERSION (benefits_core passes guardrailConfig to Converse and
        # fails closed on guardrail_intervened with empty output). Supplying the platform guardrail
        # here makes EVERY generation guardrail-assessed — without it the direct Bedrock call is
        # unguarded even though the platform gateway path is pinned.
        core_env = {}
        if guardrail_id:
            core_env = {"GUARDRAIL_ID": guardrail_id, "GUARDRAIL_VERSION": guardrail_version}
        self.core = fn("core-tools", "benefits_core", env=core_env, timeout=60)  # draft_notice (Bedrock)
        self.write_audit = fn("write-audit", "write_audit")
        self.request_signoff = fn("request-signoff", "request_signoff")
        self.signoff_register = fn("signoff-register", "signoff_register")
        self.finalize = fn("finalize", "finalize_signoff")
        self.guards = fn("workflow-guards", "workflow_guards")
        # Phase 107: the AgentCore Gateway REQUEST interceptor - derives the tenant from the VALIDATED JWT
        # and injects it HMAC-signed for the targets (a pass-through in silo mode).
        self.tenant_interceptor = fn("tenant-interceptor", "tenant_interceptor")
        # approve-signoff (G2, 2026-08-29): the human approver's OUT-OF-BAND door — verifies a
        # Cognito ACCESS token (RS256/JWKS), enforces separation of duties, consumes the single-use
        # approval (PENDING -> CONSUMED + recorded approver), and only then releases the task token.
        # It is deliberately NOT a gateway target (not an agent tool). The finalize shadow refuses
        # any approval that did not come through here, so this is now the ONLY working approve path.
        self.approve_signoff = None
        if identity is not None:
            self.approve_signoff = fn("approve-signoff", "approve_signoff", env={
                "POOL_ID": identity.pool.user_pool_id,
                "CLIENT_ID": approvals_client_id or identity.client.user_pool_client_id,
                "REVIEWER_GROUP": "benefits_caseworker",
            })

        # ── explicit least-privilege wiring ──────────────────────────────────
        # Signing secret: readable ONLY by the minter (mask_pii) + the sanitized_ref verifiers
        # (assess / redetermine / overpayment / core / guards). No external source signer exists.
        if self.signing_secret is not None:
            for f in (self.mask, self.assess, self.redetermine, self.overpayment,
                      self.core, self.guards, self.tenant_interceptor):   # interceptor SIGNS the tenant
                self.signing_secret.grant_read(f)
        # R3-2 case store: ingest WRITES raw content; intake + mask READ it (the only two consumers of
        # raw text); the drafter WRITES the notice. Nothing else touches raw content; only opaque refs
        # cross Step Functions state.
        data.case_table.grant(self.ingest, "dynamodb:PutItem")
        data.case_table.grant(self.intake, "dynamodb:GetItem")
        data.case_table.grant(self.mask, "dynamodb:GetItem")
        data.case_table.grant(self.core, "dynamodb:PutItem")
        data.pending_table.grant(self.signoff_register, "dynamodb:PutItem")
        data.pending_table.grant_read_write_data(self.finalize)
        if self.approve_signoff is not None:
            # approve path: read + consume the pending row, release the token, write DENIED/APPROVED
            # evidence. SendTaskSuccess is scoped to this deployment's controller by NAME (a
            # constructed ARN, not a cross-stack ref — workflow deploys after compute).
            data.pending_table.grant(self.approve_signoff, "dynamodb:GetItem", "dynamodb:UpdateItem")
            self.approve_signoff.add_to_role_policy(iam.PolicyStatement(
                actions=["states:SendTaskSuccess", "states:SendTaskFailure"],
                resources=[f"arn:aws:states:{self.region}:{self.account}:"
                           f"stateMachine:{prefix}-determination-workflow"]))
            data.audit_table.grant(self.approve_signoff, "dynamodb:PutItem",
                                   "dynamodb:GetItem", "dynamodb:TransactWriteItems")
            data.worm_bucket.grant_put(self.approve_signoff)
        # masking: detect PII + write the sanitized store (PutItem only)
        self.mask.add_to_role_policy(iam.PolicyStatement(
            actions=["comprehend:DetectPiiEntities"], resources=["*"]))
        data.sanitized_table.grant(self.mask, "dynamodb:PutItem")
        # sanitized-store readers (content channel: the drafter loads masked text; guards/assess verify)
        for f in (self.core, self.guards, self.assess):
            data.sanitized_table.grant(f, "dynamodb:GetItem")
        # drafter: Bedrock only
        self.core.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"], resources=["*"]))
        if guardrail_id:
            # Converse with guardrailConfig requires ApplyGuardrail on the specific guardrail.
            self.core.add_to_role_policy(iam.PolicyStatement(
                actions=["bedrock:ApplyGuardrail"],
                resources=[f"arn:aws:bedrock:{self.region}:{self.account}:guardrail/{guardrail_id}"]))
        # (No AgentCore-Identity OAuth grant is issued: `verify_income` is not deployed — see above.)
        # audit writer: append-only + WORM put, with explicit tamper Deny
        data.audit_table.grant(self.write_audit, "dynamodb:PutItem",
                               "dynamodb:GetItem", "dynamodb:TransactWriteItems")
        data.worm_bucket.grant_put(self.write_audit)
        self.write_audit.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.DENY,
            actions=["dynamodb:DeleteItem", "dynamodb:UpdateItem",
                     "s3:DeleteObject", "s3:DeleteObjectVersion",
                     "s3:PutObjectRetention", "s3:PutObjectLegalHold",
                     "s3:BypassGovernanceRetention"],
            resources=[data.audit_table.table_arn,
                       data.worm_bucket.bucket_arn, f"{data.worm_bucket.bucket_arn}/*"]))
        # request_signoff records INTENT evidence + starts the sign-off machine
        data.audit_table.grant(self.request_signoff, "dynamodb:PutItem",
                               "dynamodb:GetItem", "dynamodb:TransactWriteItems")
        data.worm_bucket.grant_put(self.request_signoff)
        # finalize: writes the COMMITTED evidence + the exactly-once FINAL# marker (conditional put)
        data.audit_table.grant(self.finalize, "dynamodb:PutItem",
                               "dynamodb:GetItem", "dynamodb:TransactWriteItems")
        data.worm_bucket.grant_put(self.finalize)

        for name, f in {
            "IngestArn": self.ingest, "IntakeArn": self.intake, "MaskArn": self.mask,
            "AssessArn": self.assess,
            "RedetermineArn": self.redetermine, "OverpaymentArn": self.overpayment,
            "CoreArn": self.core, "WriteAuditArn": self.write_audit,
            "RequestSignoffArn": self.request_signoff, "GuardsArn": self.guards,
        }.items():
            cdk.CfnOutput(self, name, value=f.function_arn)   # exact ARNs (P0-7)
        if self.approve_signoff is not None:
            cdk.CfnOutput(self, "ApproveSignoffArn", value=self.approve_signoff.function_arn,
                          description="The ONLY working approve path: verifies the approver's Cognito "
                                      "access token, enforces SoD, consumes the single-use approval.")
