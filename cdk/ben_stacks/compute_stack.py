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
from aws_cdk import (aws_bedrock as bedrock, aws_dynamodb as ddb, aws_ec2 as ec2, aws_iam as iam,
                     aws_kms as kms, aws_lambda as lambda_, aws_logs as logs,
                     aws_secretsmanager as sm, aws_ssm as ssm)
from constructs import Construct

RUNTIME = lambda_.Runtime.PYTHON_3_12


def drafter_role_name(prefix):
    """The governed drafter's PINNED IAM role name - the single principal every perimeter layer admits
    (Bedrock VPC-endpoint policy, org SCP/VPCE templates, bypass-alarm allowlist). L12."""
    return f"{prefix}-compute-coretools"


class ComputeStack(cdk.Stack):
    def __init__(self, scope: Construct, cid: str, *, prefix: str, asset_dir: str, data,
                 provenance_secret: str = "", network=None, tenant: str = "",
                 guardrail_id: str = "", guardrail_version: str = "1", guardrail_config: dict = None,
                 identity=None, approvals_client_id: str = "", multitenant: bool = False,
                 global_kill_switch: str = "", budget: dict = None, runtime_name: str = "",
                 model_id: str = "us.anthropic.claude-sonnet-4-5-20250929-v1:0", **kw):
        super().__init__(scope, cid, **kw)
        # R4-3 (fourth review, 2026-09-06): the ONLY model the drafter and the runtime may invoke, from the
        # manifest `model.draft_model_id` - IAM resources are scoped to it (inference profile + the
        # foundation model it routes to), never `foundation-model/*` / `<account>:*`.
        self._model_id = model_id
        code = lambda_.Code.from_asset(asset_dir)
        self._runtime_name = runtime_name or "benefits_runtime_agent"
        self._global_kill_switch = global_kill_switch

        # ── #166: Bedrock Guardrail as IaC ───────────────────────────────────
        # If an external guardrail id is supplied (-c guardrail_id) it wins (platform-managed guardrail);
        # otherwise create the guardrail here from the manifest `guardrail:` block so a from-zero CDK
        # deploy is self-contained. PII entities -> ANONYMIZE, prompt-attack -> the declared strength,
        # both input+output. A published version is created and PINNED (never DRAFT) so the drafter
        # assesses against an immutable version. The drafter (benefits_core) already fails closed on
        # guardrail_intervened; wiring GUARDRAIL_ID/VERSION here makes every generation assessed.
        gcfg = guardrail_config or {}
        self.guardrail = None
        self.guardrail_arn = ""
        if not guardrail_id and gcfg.get("name"):
            pa = (gcfg.get("prompt_attack") or "HIGH").upper()
            pii = [{"type": t, "action": "ANONYMIZE"} for t in gcfg.get("pii_anonymize", [])]
            # #150: contextual grounding policy from the manifest `grounding:` thresholds. GROUNDING scores
            # how well the drafted notice is supported by the case facts (grounding_source); RELEVANCE how
            # well it answers the ask (query). The drafter tags its Converse content with those qualifiers,
            # and benefits_core fails closed on guardrail_intervened, so an ungrounded/irrelevant notice is
            # blocked. Thresholds are pilot-tunable in the manifest.
            gnd = gcfg.get("grounding") or {}
            grounding_filters = []
            if gnd.get("grounding_threshold") is not None:
                grounding_filters.append(bedrock.CfnGuardrail.ContextualGroundingFilterConfigProperty(
                    type="GROUNDING", threshold=float(gnd["grounding_threshold"]), action="BLOCK"))
            # L17 (full-portfolio gate attempt 4, 2026-09-06): RELEVANCE scores a terse factual core against
            # the fixed query unreliably (0.32-0.56 for faithful answers at threshold 0.55; GROUNDING scored
            # 0.99 on the same answers), so every legitimate notice was intermittently blocked on relevance
            # alone. GROUNDING (the hallucination guard) stays BLOCKING; RELEVANCE defaults to DETECTIVE
            # (scored + traced in the invocation log, not blocking). `grounding.relevance_action: BLOCK` in
            # the manifest re-enables blocking once PQ has a threshold that holds.
            if gnd.get("relevance_threshold") is not None:
                grounding_filters.append(bedrock.CfnGuardrail.ContextualGroundingFilterConfigProperty(
                    type="RELEVANCE", threshold=float(gnd["relevance_threshold"]),
                    action=(str(gnd.get("relevance_action") or "NONE").upper())))
            self.guardrail = bedrock.CfnGuardrail(
                self, "Guardrail",
                name=f"{prefix}-{gcfg['name']}",
                description=gcfg.get("description", "Aegis benefits output guardrail (IaC)"),
                blocked_input_messaging="Blocked by the Aegis benefits guardrail.",
                blocked_outputs_messaging="[Output withheld by the Aegis benefits guardrail.]",
                content_policy_config=bedrock.CfnGuardrail.ContentPolicyConfigProperty(
                    filters_config=[bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="PROMPT_ATTACK", input_strength=pa, output_strength="NONE")]),
                sensitive_information_policy_config=(
                    bedrock.CfnGuardrail.SensitiveInformationPolicyConfigProperty(
                        pii_entities_config=[bedrock.CfnGuardrail.PiiEntityConfigProperty(
                            type=e["type"], action=e["action"]) for e in pii]) if pii else None),
                contextual_grounding_policy_config=(
                    bedrock.CfnGuardrail.ContextualGroundingPolicyConfigProperty(
                        filters_config=grounding_filters) if grounding_filters else None),
            )
            # A guardrail VERSION is an immutable snapshot; CfnGuardrailVersion does NOT auto-republish
            # when the guardrail's policies change (found live 2026-09-05: a tuned grounding threshold
            # updated DRAFT but the pinned v1 the drafter enforces stayed stale). Embed a config signature
            # in the description so a policy change replaces the version -> a fresh published version whose
            # attr_version flows into the drafter's GUARDRAIL_VERSION env.
            _cfg_sig = "pa=%s;pii=%d;gnd=%s;rel=%s;relact=%s" % (
                pa, len(pii), gnd.get("grounding_threshold"), gnd.get("relevance_threshold"),
                str(gnd.get("relevance_action") or "NONE").upper())
            ver = bedrock.CfnGuardrailVersion(self, "GuardrailVersion",
                                              guardrail_identifier=self.guardrail.attr_guardrail_id,
                                              description="aegis-guardrail cfg " + _cfg_sig)
            guardrail_id = self.guardrail.attr_guardrail_id
            guardrail_version = ver.attr_version
            self.guardrail_arn = self.guardrail.attr_guardrail_arn
        # R4-3: the EXACT guardrail the IAM layer admits - `bedrock:GuardrailIdentifier` carries the guardrail
        # ARN (optionally with `:<version>`), so the allow names both forms and the explicit Deny refuses
        # every other value INCLUDING an absent one (StringNotEquals matches a missing key). An altered
        # drafter/runtime can therefore neither drop the guardrail nor point at a weaker one.
        self.guardrail_ref = []
        if guardrail_id:
            g_arn = self.guardrail_arn or f"arn:aws:bedrock:{self.region}:{self.account}:guardrail/{guardrail_id}"
            self.guardrail_ref = [g_arn, f"{g_arn}:{guardrail_version}"]
            cdk.CfnOutput(self, "GuardrailId", value=guardrail_id)
            cdk.CfnOutput(self, "GuardrailVersionOut", value=guardrail_version, export_name=None)
            cdk.CfnOutput(self, "GuardrailArnOut", value=self.guardrail_arn)
        cmk = None
        if getattr(data, "cmk", None) is not None:
            cmk = kms.Key.from_key_arn(self, "DataCmk", data.cmk.key_arn)

        # ── Kill Switch (task 127, governed-core 1.8.0) ──────────────────────
        # ONE SSM Parameter Store flag per deployment, under the same root as the gateway-discovery
        # parameter (/<prefix>-eligibility/*) so the Runtime's existing ssm:GetParameter grant covers
        # it. Every governed Lambda (incl. the gateway interceptor) and the Runtime read it FIRST,
        # fail-closed, with a 15 s in-process TTL cache (time-to-effect <= TTL; Parameter Store stays
        # far under its 40 TPS default). Optional -c global_kill_switch=/aegis/kill-switch adds the
        # platform-wide parameter: engaged if EITHER is engaged. Only the two controller functions
        # below may write the deployment parameter (see their roles) - nothing else in this app holds
        # ssm:PutParameter on it, and the CloudTrail PutParameter event names the true principal.
        ks_name = f"/{prefix}-eligibility/kill-switch"
        self.kill_switch_param = ssm.StringParameter(
            self, "KillSwitchParam",
            parameter_name=ks_name,
            string_value='{"engaged": false, "actor": "", "reason": "", "at": 0}',
            description="Benefits pack Kill Switch (containment). engaged=true => every agent action "
                        "is refused: gateway interceptor 403 + WORM DENIED record, tool Lambdas refuse, "
                        "Runtime refuses. Change ONLY via the engage/disengage function URLs "
                        "(IAM-verified actor, separation of duties). docs/ops/KILL-SWITCH.md")
        kill_params = [ks_name]
        kill_param_arns = [self.kill_switch_param.parameter_arn]
        if global_kill_switch:
            kill_params.append(global_kill_switch)
            kill_param_arns.append(f"arn:aws:ssm:{self.region}:{self.account}:parameter{global_kill_switch}")

        # ── Budget meter (task 128, governed-core 1.9.0) ────────────────────
        # ONE DynamoDB table per deployment: <tenant>#<YYYY-MM> -> used / tokens_in / tokens_out /
        # usd_micro (+ optional per-tenant cap overrides written by an operator with one PutItem).
        # The deployment DEFAULTS come from the agent manifest's budget: block (B5: one place to set the
        # number) and -c budget_usd=<dollars>/month; the pinned price table (lib/model_prices.json) is
        # passed inline so every commit records which price_version produced the USD figure.
        budget = budget or {}
        self.budgets_table = ddb.Table(
            self, "Budgets", table_name=f"{prefix}-budgets",
            partition_key=ddb.Attribute(name="budget_key", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST, encryption_key=cmk,
            encryption=ddb.TableEncryption.CUSTOMER_MANAGED if cmk else ddb.TableEncryption.AWS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY)
        budget_env = {
            "BUDGET_TABLE": self.budgets_table.table_name,
            "BUDGET_CAP_TOKENS": str(int(budget.get("monthly_token_cap") or 0)),
            "BUDGET_CAP_USD_MICRO": str(int(round(float(budget.get("monthly_usd") or 0) * 1_000_000))),
            "BUDGET_BEHAVIOR": str(budget.get("cap_behavior") or "hard"),
            "BUDGET_RESERVE_TOKENS": str(int(budget.get("reserve_tokens") or 4000)),
            "BUDGET_PRICES_JSON": budget.get("prices_json") or "",
            "BUDGET_DEPLOYMENT": prefix,
        }

        common_env = {
            **budget_env,
            "KILL_SWITCH_PARAMS": ",".join(kill_params),
            "KILL_SWITCH_TTL_SECONDS": "15",
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
            # deep-dive #3: the AUTHORITATIVE consent/authorized-purpose store the interceptor's
            # authoritative_context resolver reads so Cedar's consent/purpose come from a trusted record,
            # never a caller-asserted boolean. Per-tenant routed via AUTHZ_TABLE_TEMPLATE in MT mode.
            "AUTHZ_TABLE": data.authz_table.table_name,
            "AUTHZ_TABLE_TEMPLATE": f"{prefix}-{{tenant}}-authz-context",
            # deep-dive #3: the interceptor derives within_service_window from the SERVER CLOCK vs this
            # window (UTC), authoritatively (the caller can no longer assert it). Default 00:00-24:00 =
            # ALWAYS in-window (temporal enforcement OFF by default, matching prior behavior); a
            # deployment enables real temporal limits by narrowing SERVICE_WINDOW_START/END (and DAYS).
            "SERVICE_WINDOW_START": str(self.node.try_get_context("service_window_start") or "0"),
            "SERVICE_WINDOW_END": str(self.node.try_get_context("service_window_end") or "24"),
        }
        # Gate-B B5: the deployment's pinned tenant (one agency per isolated deployment). Tenant identity
        # is DERIVED from this env, never from a request body (lib/controls/tenancy.py).
        if tenant:
            common_env["TENANT_ID"] = tenant
        # Hybrid multi-tenant (phase 107): tenant is derived per request from the gateway interceptor's
        # HMAC-signed injection (never the pinned env); MULTITENANT=1 makes the routing fail-closed.
        if multitenant:
            common_env["MULTITENANT"] = "1"
            # governed-core 1.6.0: the CANONICAL evidence writer routes the WORM copy to the acting
            # tenant's OWN Object Lock vault. The template is the exact per-tenant DataStack naming
            # (<prefix>-<tenant>-worm-<account>), so infra and runtime cannot drift.
            common_env["WORM_BUCKET_TEMPLATE"] = f"{prefix}-{{tenant}}-worm-{self.account}"
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
            # Kill switch: READ the switch parameter(s) and nothing else in Parameter Store.
            f.add_to_role_policy(iam.PolicyStatement(
                sid="ReadKillSwitch", actions=["ssm:GetParameter"], resources=kill_param_arns))
            return f

        # Benefits governed tool set (manifest targets).
        # Hybrid multi-tenant ingestion boundary (governed-core 1.6.0): ingest is NOT a gateway tool
        # (direct IAM invocation by the intake integration), so there is no interceptor to derive the
        # tenant. In multi-tenant mode it derives the tenant from a VERIFIED Cognito access token of a
        # tenant member (RS256/JWKS, pool + client checked) and mints the signed pair the workflow
        # carries. Same identity env as approve_signoff; unused in silo mode.
        ingest_env = ({"POOL_ID": identity.pool.user_pool_id,
                       "CLIENT_ID": approvals_client_id or identity.client.user_pool_client_id,
                       "REVIEWER_GROUP": "benefits_caseworker"}
                      if (multitenant and identity is not None) else {})
        # L18 (full-portfolio gate attempt 4, 2026-09-06): the AUTHORITATIVE consent / authorized-purpose
        # record the interceptor's resolver reads (#3) was written by NOTHING in the production path (only
        # the Cedar proof seeded it), so with -c perimeter=1 every real runtime flow was denied at
        # assess_eligibility. Ingest - the one door raw content enters, performed by a VERIFIED caseworker
        # (MT) - now records the caseworker's attestation of the applicant's consent and the case's
        # authorized purpose, server-side, so later Cedar context comes from that record, never the caller.
        ingest_env.update({"AUTHZ_TABLE": data.authz_table.table_name,
                           "AUTHZ_TABLE_TEMPLATE": f"{prefix}-{{tenant}}-authz-context"})
        self.ingest = fn("ingest-application", "ingest_case", env=ingest_env)   # R3-2: the only door for raw content
        data.authz_table.grant(self.ingest, "dynamodb:PutItem")   # L18: write the consent/purpose record (silo)
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
        # Live-found L12 (Tier-1 gate attempt 9, 2026-09-06): the Bedrock VPC-endpoint policy and the org
        # SCP/VPCE templates admit the drafter BY ROLE ARN, but a CDK-generated role name
        # (<prefix>-compute-CoreToolsServiceRole<hash>-<rand>) is neither predictable nor the case the
        # pattern guessed (ArnLike is case-sensitive). Pin the physical name so every perimeter layer
        # can name the EXACT principal - no wildcard, no case guessing. Immutable: changing it replaces
        # the role (fine for a fresh deploy; a pilot re-deploy is a role replacement, documented).
        self.core.role.node.default_child.add_property_override("RoleName", drafter_role_name(prefix))
        self.drafter_role_arn = f"arn:aws:iam::{self.account}:role/{drafter_role_name(prefix)}"
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

        # Kill Switch controller (task 127): TWO functions from ONE governed-core module, each behind
        # its own Lambda FUNCTION URL with AuthType AWS_IAM. Lambda puts the IAM-verified caller into
        # requestContext.authorizer.iam.userArn for AWS_IAM URLs (AWS Lambda dev guide, "Invoking
        # function URLs"), so the actor recorded in the parameter + the WORM ledger is never
        # self-declared, and separation of duties on release is enforced on that identity. IAM SoD:
        # two managed policies (engage-only / disengage-only) grant lambda:InvokeFunctionUrl on ONE
        # function each - the runbook assigns them to different roles.
        self.kill_switch_fns = {}
        self.kill_switch_urls = {}
        self.kill_switch_policies = {}
        for mode in ("engage", "disengage"):
            f = fn(f"kill-switch-{mode}", "kill_switch_control",
                   env={"KILL_SWITCH_MODE": mode, "KILL_SWITCH_PARAM": ks_name})
            f.add_to_role_policy(iam.PolicyStatement(
                sid="WriteKillSwitch", actions=["ssm:PutParameter"],
                resources=[self.kill_switch_param.parameter_arn]))
            # state changes are COMMITTED / DENIED records in the BASE ledger + vault (platform scope)
            data.audit_table.grant(f, "dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:TransactWriteItems")
            data.worm_bucket.grant_put(f)
            url = f.add_function_url(auth_type=lambda_.FunctionUrlAuthType.AWS_IAM)
            pol = iam.ManagedPolicy(
                self, f"KillSwitch{mode.title()}Policy",
                managed_policy_name=f"{prefix}-killswitch-{mode}",
                description=f"Grants ONLY lambda:InvokeFunctionUrl on the {mode} function of the "
                            f"{prefix} Kill Switch (AWS_IAM function URL). Assign to a different "
                            f"role than the other mode (separation of duties).",
                # Lambda dev guide, "Control access to function URLs": a same-account principal needs BOTH
                # lambda:InvokeFunctionUrl AND lambda:InvokeFunction in its identity policy (found live on
                # ben-mt5: URL-only => 403 at the front door). lambda:InvokedViaFunctionUrl=true keeps
                # this grant usable ONLY through the URL (not a direct Invoke), so the IAM-verified caller
                # context is always present.
                statements=[iam.PolicyStatement(
                    sid=f"{mode.title()}KillSwitch",
                    actions=["lambda:InvokeFunctionUrl", "lambda:InvokeFunction"],
                    resources=[f.function_arn],
                    conditions={"StringEquals": {"lambda:FunctionUrlAuthType": "AWS_IAM"},
                                "Bool": {"lambda:InvokedViaFunctionUrl": "true"}})])
            self.kill_switch_fns[mode], self.kill_switch_urls[mode], self.kill_switch_policies[mode] = f, url, pol
        # The gateway interceptor writes a DENIED record for every refused call into the ACTING
        # tenant's ledger + vault (mirror grants below in multi-tenant mode), base stores in silo mode.
        data.audit_table.grant(self.tenant_interceptor, "dynamodb:PutItem", "dynamodb:GetItem",
                               "dynamodb:TransactWriteItems")
        data.worm_bucket.grant_put(self.tenant_interceptor)
        # deep-dive #3: the interceptor's authoritative_context resolver READS the authoritative
        # consent/authorized-purpose record (least privilege: GetItem only). In multi-tenant mode it also
        # needs the per-tenant authz tables (name pattern <prefix>-*-authz-context), granted below.
        data.authz_table.grant(self.tenant_interceptor, "dynamodb:GetItem")
        if multitenant:
            self.tenant_interceptor.add_to_role_policy(iam.PolicyStatement(
                sid="AuthzPerTenantRead", actions=["dynamodb:GetItem"],
                resources=[f"arn:aws:dynamodb:{self.region}:{self.account}:table/{prefix}-*-authz-context"]))
        # Budget meter grants (least privilege): the interceptor only READS the meter (check); the drafter
        # (server-side Bedrock call) READS + UPDATES it (commit) and publishes the Aegis/Budget metrics.
        # The Runtime's exec role is granted the same by lib/runtime/_obs_setup.sh (it is created by the
        # AgentCore toolkit, outside this app).
        self.budgets_table.grant(self.tenant_interceptor, "dynamodb:GetItem")
        self.budgets_table.grant(self.core, "dynamodb:GetItem", "dynamodb:UpdateItem")
        self.core.add_to_role_policy(iam.PolicyStatement(
            sid="BudgetMetrics", actions=["cloudwatch:PutMetricData"], resources=["*"],
            conditions={"StringEquals": {"cloudwatch:namespace": "Aegis/Budget"}}))
        # The drafter refuses on the WORKFLOW hop (no interceptor in front of a Step Functions task), so
        # its budget / kill-switch refusals must land as DENIED records too: the same append-only ledger
        # grant the interceptor has (Put + Get head + TransactWrite; no Update/Delete). Found on the
        # mt6 sweep: the first refusal logged `stored: false` (AccessDenied on GetItem) - fixed here.
        data.audit_table.grant(self.core, "dynamodb:PutItem", "dynamodb:GetItem",
                               "dynamodb:TransactWriteItems")
        data.worm_bucket.grant_put(self.core)

        # ── explicit least-privilege wiring ──────────────────────────────────
        # Signing secret: readable ONLY by the minter (mask_pii) + the sanitized_ref verifiers
        # (assess / redetermine / overpayment / core / guards). No external source signer exists.
        if self.signing_secret is not None:
            for f in (self.mask, self.assess, self.redetermine, self.overpayment,
                      self.core, self.guards, self.tenant_interceptor):   # interceptor SIGNS the tenant
                self.signing_secret.grant_read(f)
            # Hybrid multi-tenant (governed-core 1.6.0): EVERY Lambda that routes a store VERIFIES the
            # HMAC-signed tenant pair first, so every one of them is a verifier and needs the key
            # (ingest also SIGNS the pair the workflow carries). Found live 2026-09-02 (ben-mt2): the
            # audit writer, intake and the sign-off Lambdas had no read grant, so verification failed
            # and they refused fail-closed (TenantError) - correct behavior, missing grant.
            if multitenant:
                for f in (self.ingest, self.intake, self.write_audit, self.request_signoff,
                          self.signoff_register, self.finalize, self.approve_signoff):
                    if f is not None:
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
        # drafter: Bedrock only. MANDATORY-GUARDRAIL IAM CONDITION (external review): when a guardrail is
        # configured, the drafter's model invocations are DENIED unless the request carries a guardrail
        # (`bedrock:GuardrailIdentifier` must be present) - so a compromised or mis-coded drafter cannot
        # make an UNGOVERNED Bedrock call that bypasses the guardrail. This is the AWS-documented pattern
        # for enforcing a mandatory guardrail at the IAM layer (Null present-check on the condition key).
        _has_guardrail = bool(guardrail_id) or bool(self.guardrail)
        # R4-3 (fourth review): not "a guardrail is present" (the old Null check let an altered drafter name a
        # weaker guardrail) but THE guardrail: allow on StringEquals <exact ARN[:version]>, explicit Deny on
        # anything else, resources scoped to the manifest model (AWS "enforce a specific guardrail" pattern).
        for st in self._bedrock_invoke_statements("Drafter", _has_guardrail):
            self.core.add_to_role_policy(st)
        self.runtime_role = self._runtime_execution_role(prefix, _has_guardrail, guardrail_id)
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

        # ── Hybrid multi-tenant (phase 107/109) ─────────────────────────────
        # The SAME least-privilege actions, mirrored onto EVERY tenant's own store inside this
        # deployment prefix (<prefix>-<tenant>-<logical>). Stores are routed per request by
        # tenancy.route_store from the interceptor-injected, signed tenant; grants never widen past
        # the prefix, and the audit tamper DENY is mirrored onto every tenant's ledger + vault.
        if multitenant:
            def _tbl(logical):
                base = f"arn:aws:dynamodb:{self.region}:{self.account}:table/{prefix}-*-{logical}"
                return [base, f"{base}/index/*"]
            worm = [f"arn:aws:s3:::{prefix}-*-worm-*", f"arn:aws:s3:::{prefix}-*-worm-*/*"]

            def _mt(fn, resources, *actions):
                fn.add_to_role_policy(iam.PolicyStatement(actions=list(actions), resources=resources))
            RW = ["dynamodb:GetItem", "dynamodb:BatchGetItem", "dynamodb:Query", "dynamodb:Scan",
                  "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem",
                  "dynamodb:BatchWriteItem", "dynamodb:ConditionCheckItem", "dynamodb:DescribeTable"]
            AUD = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:TransactWriteItems"]
            _mt(self.ingest, _tbl("case-store"), "dynamodb:PutItem")
            _mt(self.ingest, _tbl("authz-context"), "dynamodb:PutItem")   # L18: per-tenant consent/purpose record
            _mt(self.intake, _tbl("case-store"), "dynamodb:GetItem")
            _mt(self.mask, _tbl("case-store"), "dynamodb:GetItem")
            _mt(self.core, _tbl("case-store"), "dynamodb:PutItem")
            _mt(self.signoff_register, _tbl("pending-approvals"), "dynamodb:PutItem")
            _mt(self.finalize, _tbl("pending-approvals"), *RW)
            _mt(self.mask, _tbl("sanitized-artifacts"), "dynamodb:PutItem")
            for f in (self.core, self.guards, self.assess):
                _mt(f, _tbl("sanitized-artifacts"), "dynamodb:GetItem")
            for f in (self.write_audit, self.request_signoff, self.finalize, self.tenant_interceptor, self.core):
                _mt(f, _tbl("audit-ledger"), *AUD)
                _mt(f, worm, "s3:PutObject", "s3:Abort*")
            if self.approve_signoff is not None:
                _mt(self.approve_signoff, _tbl("pending-approvals"), "dynamodb:GetItem", "dynamodb:UpdateItem")
                _mt(self.approve_signoff, _tbl("audit-ledger"), *AUD)
                _mt(self.approve_signoff, worm, "s3:PutObject", "s3:Abort*")
            self.write_audit.add_to_role_policy(iam.PolicyStatement(
                effect=iam.Effect.DENY,
                actions=["dynamodb:DeleteItem", "dynamodb:UpdateItem",
                         "s3:DeleteObject", "s3:DeleteObjectVersion",
                         "s3:PutObjectRetention", "s3:PutObjectLegalHold",
                         "s3:BypassGovernanceRetention"],
                resources=_tbl("audit-ledger") + worm))

        for name, f in {
            "IngestArn": self.ingest, "IntakeArn": self.intake, "MaskArn": self.mask,
            "AssessArn": self.assess,
            "RedetermineArn": self.redetermine, "OverpaymentArn": self.overpayment,
            "CoreArn": self.core, "WriteAuditArn": self.write_audit,
            "RequestSignoffArn": self.request_signoff, "GuardsArn": self.guards,
        }.items():
            cdk.CfnOutput(self, name, value=f.function_arn)   # exact ARNs (P0-7)
        cdk.CfnOutput(self, "DrafterRoleArn", value=self.drafter_role_arn)   # the perimeter's exact principal (L12)
        cdk.CfnOutput(self, "BudgetsTableName", value=self.budgets_table.table_name,
                      description="Per-tenant meter: <tenant>#<YYYY-MM>; PutItem cap_tokens / cap_usd_micro / behavior to override one tenant")
        cdk.CfnOutput(self, "KillSwitchParameter", value=ks_name)
        for mode in ("engage", "disengage"):
            cdk.CfnOutput(self, f"KillSwitch{mode.title()}Url", value=self.kill_switch_urls[mode].url,
                          description=f"POST {{reason}} with SigV4 (AWS_IAM) to {mode} the Kill Switch; GET = status")
            cdk.CfnOutput(self, f"KillSwitch{mode.title()}PolicyArn",
                          value=self.kill_switch_policies[mode].managed_policy_arn)
        if self.approve_signoff is not None:
            cdk.CfnOutput(self, "ApproveSignoffArn", value=self.approve_signoff.function_arn,
                          description="The ONLY working approve path: verifies the approver's Cognito "
                                      "access token, enforces SoD, consumes the single-use approval.")

    def _model_resources(self):
        """The model ARNs the pack may invoke: the (cross-region) inference profile in this account/region and
        the foundation model it routes to (any region the profile spans) - nothing else."""
        mid = self._model_id
        fm = mid.split(".", 1)[1] if mid[:3] in ("us.", "eu.", "ap.", "jp.", "au.", "ca.") else mid
        return [f"arn:aws:bedrock:*::foundation-model/{fm}",
                f"arn:aws:bedrock:{self.region}:{self.account}:inference-profile/{mid}"]

    def _bedrock_invoke_statements(self, who, has_guardrail):
        """R4-3: model-invocation grant for a governed principal. With a guardrail: ALLOW only with the exact
        guardrail (`StringEquals bedrock:GuardrailIdentifier` = ARN or ARN:version) on the scoped model
        resources, plus an explicit DENY for any other or missing guardrail value on every model. Without a
        guardrail (sandbox): the scoped allow only."""
        actions = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
        if not has_guardrail:
            return [iam.PolicyStatement(sid=f"{who}Bedrock", actions=actions, resources=self._model_resources())]
        return [
            iam.PolicyStatement(sid=f"{who}BedrockExactGuardrail", actions=actions, resources=self._model_resources(),
                                conditions={"StringEquals": {"bedrock:GuardrailIdentifier": self.guardrail_ref}}),
            iam.PolicyStatement(sid=f"{who}DenyOtherOrNoGuardrail", effect=iam.Effect.DENY, actions=actions,
                                resources=["*"],
                                conditions={"StringNotEquals": {"bedrock:GuardrailIdentifier": self.guardrail_ref}}),
        ]

    def _runtime_execution_role(self, prefix, has_guardrail, guardrail_id):
        """AgentCore RUNTIME EXECUTION ROLE as IaC (third external review, 2026-09-05). The toolkit's
        `agentcore configure` otherwise auto-creates the role, and AWS states CLI-generated policies are
        for development/testing. This role is the documented runtime policy ("IAM Permissions for
        AgentCore Runtime": ECR pull, runtime log groups, X-Ray, bedrock-agentcore metrics, workload
        access tokens, model invocation) plus exactly what THIS runtime needs (gateway-URL + kill-switch
        SSM reads, the budget meter's table + metric namespace, ApplyGuardrail on the platform guardrail),
        every resource scoped to the deployment. With a guardrail configured, the runtime's model calls
        carry the same MANDATORY-GUARDRAIL condition as the drafter (agent.py passes guardrailConfig via
        Strands), so the runtime cannot make an unguarded model call either. Launch with
        `agentcore configure --execution-role <RuntimeExecutionRoleArn>`; the role name is deterministic so
        the org SCP allowlist and the bypass alarm can reference it."""
        rt, region, acct = self._runtime_name, self.region, self.account
        role = iam.Role(
            self, "RuntimeExecutionRole", role_name=f"{prefix}-agentcore-runtime",
            assumed_by=iam.ServicePrincipal("bedrock-agentcore.amazonaws.com", conditions={
                "StringEquals": {"aws:SourceAccount": acct},
                "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{region}:{acct}:*"}}),
            description="Aegis governed AgentCore runtime execution role (IaC, least privilege)")
        stmts = [
            iam.PolicyStatement(sid="ECRImageAccess", actions=["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"],
                                resources=[f"arn:aws:ecr:{region}:{acct}:repository/*"]),
            iam.PolicyStatement(sid="ECRTokenAccess", actions=["ecr:GetAuthorizationToken"], resources=["*"]),
            iam.PolicyStatement(sid="RuntimeLogGroups", actions=["logs:DescribeLogStreams", "logs:CreateLogGroup"],
                                resources=[f"arn:aws:logs:{region}:{acct}:log-group:/aws/bedrock-agentcore/runtimes/*"]),
            iam.PolicyStatement(sid="RuntimeLogResourcePolicy", actions=["logs:PutResourcePolicy"],
                                resources=[f"arn:aws:logs:{region}:{acct}:log-group:/aws/bedrock-agentcore/runtimes/{rt}-*"]),
            iam.PolicyStatement(sid="DescribeLogGroups", actions=["logs:DescribeLogGroups"],
                                resources=[f"arn:aws:logs:{region}:{acct}:log-group:*"]),
            iam.PolicyStatement(sid="RuntimeLogStreams", actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                                resources=[f"arn:aws:logs:{region}:{acct}:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"]),
            iam.PolicyStatement(sid="XRay", actions=["xray:PutTraceSegments", "xray:PutTelemetryRecords",
                                                     "xray:GetSamplingRules", "xray:GetSamplingTargets"], resources=["*"]),
            iam.PolicyStatement(sid="AgentCoreMetrics", actions=["cloudwatch:PutMetricData"], resources=["*"],
                                conditions={"StringEquals": {"cloudwatch:namespace": "bedrock-agentcore"}}),
            iam.PolicyStatement(sid="BudgetMetrics", actions=["cloudwatch:PutMetricData"], resources=["*"],
                                conditions={"StringEquals": {"cloudwatch:namespace": "Aegis/Budget"}}),
            # R4-8 (fourth review): the runtime ALWAYS has a verified JWT, so the user-id token path is never a
            # legitimate need - AWS recommends an explicit Deny on GetWorkloadAccessTokenForUserId and
            # InvokeAgentRuntimeForUser so identity can only come from the cryptographically verified JWT.
            iam.PolicyStatement(sid="GetAgentAccessToken",
                                actions=["bedrock-agentcore:GetWorkloadAccessToken", "bedrock-agentcore:GetWorkloadAccessTokenForJWT"],
                                resources=[f"arn:aws:bedrock-agentcore:{region}:{acct}:workload-identity-directory/default",
                                           f"arn:aws:bedrock-agentcore:{region}:{acct}:workload-identity-directory/default/workload-identity/{rt}-*"]),
            iam.PolicyStatement(sid="DenyUserIdIdentityPaths", effect=iam.Effect.DENY,
                                actions=["bedrock-agentcore:GetWorkloadAccessTokenForUserId", "bedrock-agentcore:InvokeAgentRuntimeForUser"],
                                resources=["*"]),
            *self._bedrock_invoke_statements("Runtime", has_guardrail),
            iam.PolicyStatement(sid="GovernanceParameters", actions=["ssm:GetParameter"],
                                resources=[f"arn:aws:ssm:{region}:{acct}:parameter/{prefix}-eligibility/*"]
                                + ([f"arn:aws:ssm:{region}:{acct}:parameter{self._global_kill_switch}"] if self._global_kill_switch else [])),
            iam.PolicyStatement(sid="BudgetMeter", actions=["dynamodb:GetItem", "dynamodb:UpdateItem"],
                                resources=[self.budgets_table.table_arn]),
        ]
        if has_guardrail:
            g_arn = self.guardrail_arn or f"arn:aws:bedrock:{region}:{acct}:guardrail/{guardrail_id}"
            stmts.append(iam.PolicyStatement(sid="ApplyPlatformGuardrail", actions=["bedrock:ApplyGuardrail"], resources=[g_arn]))
        for st in stmts:
            role.add_to_policy(st)
        cdk.CfnOutput(self, "RuntimeExecutionRoleArn", value=role.role_arn,
                      description="Pass to `agentcore configure --execution-role` (IaC role; never the CLI-generated one).")
        cdk.CfnOutput(self, "RuntimeExecutionRoleName", value=role.role_name)
        return role

