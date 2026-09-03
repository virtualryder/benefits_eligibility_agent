"""P0-5 / P0-2 / P0-6 / P0-7 / P0-12 / R3-2 — the benefits CDK stacks synthesize and carry the controls.

Uses aws_cdk.assertions (pure Python; no CDK CLI, no AWS). Skipped automatically when aws-cdk-lib is
not installed (CI installs it)."""
import json
import pathlib
import sys

import pytest

aws_cdk = pytest.importorskip("aws_cdk")
from aws_cdk.assertions import Template, Match  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cdk"))

from app import stage_lambda_bundle  # noqa: E402
from ben_stacks.data_stack import DataStack  # noqa: E402
from ben_stacks.network_stack import NetworkStack  # noqa: E402
from ben_stacks.compute_stack import ComputeStack  # noqa: E402
from ben_stacks.workflow_stack import WorkflowStack  # noqa: E402
from ben_stacks.identity_stack import IdentityStack  # noqa: E402


def _stacks(profile="sandbox-demo", kms="aws-managed", private=False):
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    data = DataStack(app, "d", prefix="ben-test", retention_profile=profile, kms_mode=kms)
    net = NetworkStack(app, "n", prefix="ben-test") if private else None
    compute = ComputeStack(app, "c", prefix="ben-test", asset_dir=asset, data=data, network=net,
                           tenant="ben-test-agency")
    workflow = WorkflowStack(app, "w", prefix="ben-test", compute=compute, data=data)
    identity = IdentityStack(app, "i", prefix="ben-test")
    return data, net, compute, workflow, identity


DATA, NET, COMPUTE, WORKFLOW, IDENTITY = _stacks(private=True)
T_DATA, T_COMPUTE = Template.from_stack(DATA), Template.from_stack(COMPUTE)
T_WORKFLOW, T_IDENTITY, T_NET = Template.from_stack(WORKFLOW), Template.from_stack(IDENTITY), Template.from_stack(NET)


# ── data: retention profiles (P0-12) + sanitized store (P0-1) ────────────────

def test_worm_bucket_object_lock_default_profile():
    T_DATA.has_resource_properties("AWS::S3::Bucket", Match.object_like({
        "ObjectLockEnabled": True,
        "ObjectLockConfiguration": Match.object_like({
            "Rule": {"DefaultRetention": {"Mode": "GOVERNANCE", "Days": 1}}}),
    }))


def test_production_profile_is_compliance_mode():
    d, *_ = _stacks(profile="production-reference")
    Template.from_stack(d).has_resource_properties("AWS::S3::Bucket", Match.object_like({
        "ObjectLockConfiguration": Match.object_like({
            "Rule": {"DefaultRetention": {"Mode": "COMPLIANCE", "Days": 2555}}}),
    }))


def test_unknown_profile_refused():
    with pytest.raises(ValueError):
        _stacks(profile="whatever")


def test_sanitized_and_case_tables_with_ttl():
    T_DATA.has_resource_properties("AWS::DynamoDB::Table", Match.object_like({
        "TableName": "ben-test-sanitized-artifacts",
        "TimeToLiveSpecification": {"AttributeName": "expires_at", "Enabled": True}}))
    T_DATA.has_resource_properties("AWS::DynamoDB::Table", Match.object_like({
        "TableName": "ben-test-case-store",
        "TimeToLiveSpecification": {"AttributeName": "expires_at", "Enabled": True}}))


def test_audit_ledger_retained_with_pitr():
    T_DATA.has_resource("AWS::DynamoDB::Table", Match.object_like({
        "DeletionPolicy": "Retain",
        "Properties": Match.object_like({
            "TableName": "ben-test-audit-ledger",
            "PointInTimeRecoverySpecification": {"PointInTimeRecoveryEnabled": True}})}))


# ── compute: explicit IAM (P0-5) + tamper deny + exact-ARN outputs (P0-7) ────

def test_audit_writer_has_explicit_tamper_deny():
    tpl = json.dumps(T_COMPUTE.to_json())
    assert "s3:BypassGovernanceRetention" in tpl and '"Effect": "Deny"' in tpl.replace("'", '"')


def test_exact_arn_outputs_exist():
    outs = T_COMPUTE.to_json().get("Outputs", {})
    for k in ("MaskArn", "AssessArn", "WriteAuditArn", "GuardsArn", "IngestArn", "CoreArn"):
        assert k in outs, f"exact-ARN output {k} missing (P0-7)"


# ── compute: SINGLE signing domain via Secrets Manager, no plaintext (P0-1) ──

def test_single_signing_secret_provisioned_no_plaintext():
    tpl = T_COMPUTE.to_json()
    types = [r["Type"] for r in tpl.get("Resources", {}).values()]
    assert types.count("AWS::SecretsManager::Secret") >= 1
    s = json.dumps(tpl)
    assert "PROVENANCE_SECRET_ARN" in s
    assert '"PROVENANCE_SECRET"' not in s, "plaintext signing secret must not appear in the template"
    # benefits has ONE trust domain — no external-source signer, so no GA-2 scorecard/HUD key here
    assert "SCORECARD" not in s and "HUD" not in s


# ── network: ZERO public egress (no NAT, no firewall; isolated subnets + endpoints) ──

def test_network_zero_public_egress():
    tpl = T_NET.to_json()
    types = [r["Type"] for r in tpl.get("Resources", {}).values()]
    assert "AWS::EC2::NatGateway" not in types, "zero-egress design has no NAT gateway"
    assert "AWS::EC2::InternetGateway" not in types, "zero-egress design has no internet gateway"
    assert "AWS::NetworkFirewall::Firewall" not in types, "benefits needs no egress firewall (no external dependency)"
    assert types.count("AWS::EC2::VPCEndpoint") >= 7, "AWS services must be reachable via private endpoints"


# ── workflow: deterministic controller shape + due-process HOLD (P0-2) ───────

def _controller_definition():
    tpl = T_WORKFLOW.to_json()
    for r in tpl["Resources"].values():
        if r["Type"] == "AWS::StepFunctions::StateMachine":
            parts = r["Properties"]["DefinitionString"]["Fn::Join"][1]
            return json.loads("".join(p if isinstance(p, str) else "ARN" for p in parts))
    raise AssertionError("no state machine in workflow stack")


def test_controller_pipeline_order_and_fail_closed_choices():
    doc = _controller_definition()
    state, visited = doc["StartAt"], []
    while state and len(visited) < 40:
        visited.append(state)
        st = doc["States"][state]
        state = st["Choices"][0]["Next"] if st["Type"] == "Choice" else st.get("Next")
    expected = ["Extract", "GuardExtracted", "ExtractedOk",
                "MaskPii", "GuardDeidentified", "DeidentifiedOk",
                "AssessEligibility", "GuardRulesExecuted", "RulesOk",
                "CheckAdverseNotice", "AdverseNoticeOk",
                "DraftNotice", "DraftOk", "AuditIntent", "HumanSignoff", "Finalize", "FinalizeOk", "Committed"]
    assert visited == expected, f"happy path deviates from the regulated sequence: {visited}"
    # every non-adverse guard Choice fails closed to ManualReview
    for choice in ("ExtractedOk", "DeidentifiedOk", "RulesOk"):
        assert doc["States"][choice]["Default"] == "ManualReview"
    # DUE PROCESS: an adverse redetermination without advance notice HOLDS (not ManualReview)
    assert doc["States"]["AdverseNoticeOk"]["Default"] == "AdverseNoticeHold"
    # the human gate is a real waitForTaskToken pause
    assert "waitForTaskToken" in doc["States"]["HumanSignoff"]["Resource"]


def test_r32_no_raw_or_masked_or_notice_content_in_state():
    """R3-2: the execution carries only opaque refs. The controller must pass case_ref + sanitized_ref
    and must NEVER thread the raw application text, the masked case, or the drafted notice through state."""
    doc = json.dumps(_controller_definition())
    assert "case_ref" in doc and "sanitized_ref" in doc
    assert "masked_case" not in doc, "masked content must not travel in Step Functions state (R3-2)"
    # the drafter is invoked with only the ref (no notice text keyed into state)
    assert '"notice"' not in doc, "drafted notice text must not be threaded through state (R3-2)"


# ── identity: no users, no passwords (P0-6) ──────────────────────────────────

def test_identity_creates_no_users_and_no_passwords():
    tpl = T_IDENTITY.to_json()
    types = [r["Type"] for r in tpl.get("Resources", {}).values()]
    assert "AWS::Cognito::UserPoolUser" not in types
    assert "ChangeMe" not in json.dumps(tpl)


def test_no_default_password_anywhere_in_any_template():
    for t in (T_DATA, T_COMPUTE, T_WORKFLOW, T_IDENTITY, T_NET):
        assert "ChangeMe" not in json.dumps(t.to_json())


def test_data_stack_per_tenant_naming_is_physically_separate():
    """Hybrid multi-tenant: each tenant's DataStack yields its OWN tenant-scoped tables (physical
    separation, not a shared table with a tenant key). Silo (no tenant) keeps the base names."""
    app = aws_cdk.App()
    # create every stack BEFORE any synth (Template.from_stack synthesizes the app)
    a = DataStack(app, "da", prefix="ben-test", tenant="pha-oakland")
    b = DataStack(app, "db", prefix="ben-test", tenant="pha-alameda")
    silo = DataStack(app, "ds", prefix="ben-test")
    Template.from_stack(a).has_resource_properties("AWS::DynamoDB::Table",
        Match.object_like({"TableName": "ben-test-pha-oakland-audit-ledger"}))
    Template.from_stack(b).has_resource_properties("AWS::DynamoDB::Table",
        Match.object_like({"TableName": "ben-test-pha-alameda-audit-ledger"}))
    Template.from_stack(silo).has_resource_properties("AWS::DynamoDB::Table",
        Match.object_like({"TableName": "ben-test-audit-ledger"}))
    # per-tenant WORM vault gets a predictable, tenant-scoped name (so IAM can scope to <prefix>-*-worm-*)
    assert "ben-test-pha-oakland-worm-" in json.dumps(Template.from_stack(a).to_json())


def test_tenant_interceptor_wired_into_compute_and_gateway():
    """Phase 107 (hybrid multi-tenant): the gateway REQUEST interceptor Lambda exists with MULTITENANT set,
    the gateway attachment carries its ARN (passRequestHeaders -> it sees the validated JWT), the gateway
    role may invoke it, and every tool schema carries the reserved HMAC-signed tenant fields."""
    from ben_stacks.gateway_stack import GatewayStack
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    data = DataStack(app, "d2", prefix="ben-mt", retention_profile="sandbox-demo")
    compute = ComputeStack(app, "c2", prefix="ben-mt", asset_dir=asset, data=data, multitenant=True)
    identity = IdentityStack(app, "i2", prefix="ben-mt", tenants=("pha-oakland", "pha-alameda"))
    gateway = GatewayStack(app, "g2", prefix="ben-mt", compute=compute, identity=identity, multitenant=True)
    gateway_silo = GatewayStack(app, "g3", prefix="ben-mt", compute=compute, identity=identity)  # before synth
    tc, tg = Template.from_stack(compute), Template.from_stack(gateway)
    tc.has_resource_properties("AWS::Lambda::Function", Match.object_like({
        "FunctionName": "ben-mt-tenant-interceptor",
        "Handler": "tenant_interceptor.handler",
        "Environment": {"Variables": Match.object_like({"MULTITENANT": "1"})},
    }))
    gw = json.dumps(tg.to_json())
    assert "InterceptorLambdaArn" in gw, "gateway attachment does not carry the interceptor ARN"
    assert "__aegis_tenant" in gw and "__aegis_tenant_sig" in gw, \
        "tool schemas are missing the reserved signed-tenant fields"
    # per-tenant identity: one tenant_<id> Cognito group per tenant (membership is what the access token carries)
    ti = Template.from_stack(identity)
    ti.has_resource_properties("AWS::Cognito::UserPoolGroup", Match.object_like({"GroupName": "tenant_pha-oakland"}))
    ti.has_resource_properties("AWS::Cognito::UserPoolGroup", Match.object_like({"GroupName": "tenant_pha-alameda"}))
    # phase 108: require_tenant attaches ONLY in multi-tenant deployments (silo would forbid everything)
    assert "require_tenant" in gw and "custom:tenant" in gw
    assert "require_tenant" not in json.dumps(Template.from_stack(gateway_silo).to_json())
    # multi-tenant mirror grants: the shared Lambdas reach EVERY tenant's store, scoped to the prefix
    cj = json.dumps(tc.to_json())
    assert "table/ben-mt-*-case-store" in cj and "table/ben-mt-*-audit-ledger" in cj
    assert "arn:aws:s3:::ben-mt-*-worm-*" in cj
    # (the gateway role's invoke grant and the attachment both reference the interceptor ARN via the
    #  same cross-stack export token, so InterceptorLambdaArn being present proves the wiring)


def test_multitenant_audit_routing_wired_through_compute_and_workflow():
    """governed-core 1.6.0: per-tenant ledger/WORM/approvals routing. Compute hands the evidence writer
    the exact per-tenant vault template; the workflow threads the HMAC-signed tenant pair into EVERY
    Lambda payload (the Step Functions hop has no interceptor). Silo templates carry neither."""
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    data = DataStack(app, "d4", prefix="ben-mt", retention_profile="sandbox-demo")
    compute = ComputeStack(app, "c4", prefix="ben-mt", asset_dir=asset, data=data, multitenant=True)
    workflow = WorkflowStack(app, "w4", prefix="ben-mt", compute=compute, data=data, multitenant=True)
    tc, tw = Template.from_stack(compute), Template.from_stack(workflow)
    tc.has_resource_properties("AWS::Lambda::Function", Match.object_like({
        "FunctionName": "ben-mt-write-audit",
        "Environment": {"Variables": Match.object_like({
            "MULTITENANT": "1",
            "WORM_BUCKET_TEMPLATE": Match.object_like({"Fn::Join": Match.any_value()})})},
    }))
    assert "ben-mt-{tenant}-worm-" in json.dumps(tc.to_json())
    # every tenant-verifying Lambda can read the signing secret (found missing live on ben-mt2):
    # a role policy granting secretsmanager:GetSecretValue on the SigningSecret for each of these
    roles_with_secret = set()
    for name, res in tc.to_json()["Resources"].items():
        if res["Type"] != "AWS::IAM::Policy":
            continue
        doc = json.dumps(res["Properties"]["PolicyDocument"])
        if "secretsmanager:GetSecretValue" in doc and "SigningSecret" in doc:
            roles_with_secret.update(json.dumps(res["Properties"]["Roles"]).split('"Ref": "')[1:])
    roles_with_secret = {r.split('"')[0] for r in roles_with_secret}
    assert len(roles_with_secret) >= 13, roles_with_secret     # 7 original readers + 6 multi-tenant verifiers
    fn_roles = {res["Properties"]["FunctionName"]: json.dumps(res["Properties"]["Role"])
                for res in tc.to_json()["Resources"].values() if res["Type"] == "AWS::Lambda::Function"}
    for fname in ("ben-mt-ingest-application", "ben-mt-intake-application", "ben-mt-write-audit",
                  "ben-mt-request-signoff", "ben-mt-signoff-register", "ben-mt-finalize", "ben-mt-mask-pii"):
        assert any(r in fn_roles[fname] for r in roles_with_secret), f"{fname} cannot read the signing secret"
    wj = json.dumps(tw.to_json())
    # every LambdaInvoke payload (incl. the waitForTaskToken sign-off register) carries the signed pair
    # 11 Lambda-backed states: Extract, 5 guards, MaskPii, AssessEligibility, DraftNotice, AuditIntent,
    # HumanSignoff (waitForTaskToken), Finalize -> each carries the pair exactly once
    assert wj.count("__aegis_tenant.$") == 11 and wj.count("__aegis_tenant_sig.$") == 11, wj.count("__aegis_tenant.$")
    silo = json.dumps(T_WORKFLOW.to_json()) + json.dumps(T_COMPUTE.to_json())
    assert "__aegis_tenant" not in silo and "WORM_BUCKET_TEMPLATE" not in silo


def test_kill_switch_wired_into_every_lambda_and_the_controller_has_sod(monkeypatch):
    """Task 127 (governed-core 1.8.0): ONE SSM parameter per deployment under the gateway-discovery root;
    EVERY governed Lambda (incl. the interceptor and the controller) reads it (KILL_SWITCH_PARAMS + an
    ssm:GetParameter grant scoped to that parameter); ONLY the two controller functions may write it;
    the controller is two functions (engage / disengage) behind AWS_IAM function URLs with one
    managed policy each (IAM separation of duties); the interceptor may write DENIED records to the
    ledger + vault; -c global_kill_switch adds the platform-wide parameter to every reader."""
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    data = DataStack(app, "d4", prefix="ben-ks", retention_profile="sandbox-demo")
    compute = ComputeStack(app, "c4", prefix="ben-ks", asset_dir=asset, data=data, multitenant=True,
                           global_kill_switch="/aegis/kill-switch")
    t = Template.from_stack(compute)
    t.has_resource_properties("AWS::SSM::Parameter", Match.object_like({
        "Name": "/ben-ks-eligibility/kill-switch", "Type": "String",
        "Value": '{"engaged": false, "actor": "", "reason": "", "at": 0}'}))
    fns = t.find_resources("AWS::Lambda::Function")
    names = {v["Properties"]["FunctionName"] for v in fns.values()}
    assert {"ben-ks-kill-switch-engage", "ben-ks-kill-switch-disengage", "ben-ks-tenant-interceptor"} <= names
    for v in fns.values():
        env = v["Properties"]["Environment"]["Variables"]
        assert env["KILL_SWITCH_PARAMS"] == "/ben-ks-eligibility/kill-switch,/aegis/kill-switch", v["Properties"]["FunctionName"]
        assert env["KILL_SWITCH_TTL_SECONDS"] == "15"
    for mode in ("engage", "disengage"):
        t.has_resource_properties("AWS::Lambda::Function", Match.object_like({
            "FunctionName": f"ben-ks-kill-switch-{mode}", "Handler": "kill_switch_control.handler",
            "Environment": {"Variables": Match.object_like({"KILL_SWITCH_MODE": mode,
                                                            "KILL_SWITCH_PARAM": "/ben-ks-eligibility/kill-switch"})}}))
        t.has_resource_properties("AWS::IAM::ManagedPolicy", Match.object_like({
            "ManagedPolicyName": f"ben-ks-killswitch-{mode}",
            "PolicyDocument": Match.object_like({"Statement": [Match.object_like({
                "Action": ["lambda:InvokeFunctionUrl", "lambda:InvokeFunction"],   # both: Lambda dev guide, urls-auth
                "Condition": {"StringEquals": {"lambda:FunctionUrlAuthType": "AWS_IAM"},
                              "Bool": {"lambda:InvokedViaFunctionUrl": "true"}}})]})}))
    urls = t.find_resources("AWS::Lambda::Url")
    assert len(urls) == 2 and all(u["Properties"]["AuthType"] == "AWS_IAM" for u in urls.values())
    # ssm:PutParameter on the switch appears in EXACTLY the two controller roles; GetParameter everywhere
    pols = json.dumps(t.find_resources("AWS::IAM::Policy"))
    assert pols.count('"ssm:PutParameter"') == 2
    assert pols.count("ReadKillSwitch") == len(fns)
    # the interceptor can write the DENIED evidence: base ledger transact + vault put, mirrored per tenant
    ipol = [p for p in t.find_resources("AWS::IAM::Policy").values()
            if any("TenantInterceptor" in r.get("Ref", "") for r in p["Properties"]["Roles"])]
    ij = json.dumps(ipol)
    assert "dynamodb:TransactWriteItems" in ij and "s3:PutObject" in ij and "table/ben-ks-*-audit-ledger" in ij
    outs = t.to_json()["Outputs"]
    assert {"KillSwitchParameter", "KillSwitchEngageUrl", "KillSwitchDisengageUrl",
            "KillSwitchEngagePolicyArn", "KillSwitchDisengagePolicyArn"} <= set(outs)
    # silo / no global switch: exactly the deployment's own parameter
    app2 = aws_cdk.App()                                       # a fresh app: the first one is already synthesized
    data2 = DataStack(app2, "d5", prefix="ben-ks2", retention_profile="sandbox-demo")
    c2 = Template.from_stack(ComputeStack(app2, "c5", prefix="ben-ks2", asset_dir=asset, data=data2))
    for v in c2.find_resources("AWS::Lambda::Function").values():
        assert v["Properties"]["Environment"]["Variables"]["KILL_SWITCH_PARAMS"] == "/ben-ks2-eligibility/kill-switch"


def test_budget_meter_alarms_and_usd_ceiling_are_wired():
    """Task 128 (governed-core 1.9.0): ONE <prefix>-budgets table; every governed Lambda carries the meter
    env (caps from the manifest budget: block, pinned price table with its version, deployment dimension);
    the interceptor may only READ the meter, the drafter may UPDATE it + publish Aegis/Budget metrics;
    per-tenant 60/85/100 % alarms exist; with -c budget_usd the AWS Budgets USD ceiling exists with an
    APPLY_IAM_POLICY action (deny bedrock:* on the drafter role, automatic approval) + the budget-breach
    function subscribed to the ops topic with permission to invoke the kill-switch engage URL."""
    from ben_stacks.observability_stack import ObservabilityStack
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    prices = json.dumps({"price_version": "test-2026-09-03", "models": {"anthropic.claude-sonnet-4-5": {"input_per_m": 3, "output_per_m": 15}}})
    data = DataStack(app, "d6", prefix="ben-bg", retention_profile="sandbox-demo")
    compute = ComputeStack(app, "c6", prefix="ben-bg", asset_dir=asset, data=data, multitenant=True,
                           budget={"monthly_token_cap": 5000000, "cap_behavior": "hard", "monthly_usd": 25.5, "prices_json": prices})
    workflow = WorkflowStack(app, "w6", prefix="ben-bg", compute=compute, data=data, multitenant=True)
    obs = ObservabilityStack(app, "o6", prefix="ben-bg", compute=compute, workflow=workflow, data=data,
                             tenants=("pha-a", "pha-b"), budget_usd=25.5, runtime_role_name="AmazonBedrockAgentCoreSDKRuntime-x")
    tc, to = Template.from_stack(compute), Template.from_stack(obs)
    tc.has_resource_properties("AWS::DynamoDB::Table", Match.object_like({
        "TableName": "ben-bg-budgets", "KeySchema": [{"AttributeName": "budget_key", "KeyType": "HASH"}],
        "BillingMode": "PAY_PER_REQUEST"}))
    for v in tc.find_resources("AWS::Lambda::Function").values():
        env = v["Properties"]["Environment"]["Variables"]
        assert env["BUDGET_CAP_TOKENS"] == "5000000" and env["BUDGET_CAP_USD_MICRO"] == "25500000", v["Properties"]["FunctionName"]
        assert env["BUDGET_BEHAVIOR"] == "hard" and env["BUDGET_DEPLOYMENT"] == "ben-bg" and env["BUDGET_RESERVE_TOKENS"] == "4000"
        assert json.loads(env["BUDGET_PRICES_JSON"])["price_version"] == "test-2026-09-03"
    pols = tc.find_resources("AWS::IAM::Policy")
    def _role_pols(marker):
        return json.dumps([p for p in pols.values() if any(marker in r.get("Ref", "") for r in p["Properties"]["Roles"])])
    ij, cj = _role_pols("TenantInterceptor"), _role_pols("CoreTools")
    assert "ben-bg-budgets" not in ij or "dynamodb:UpdateItem" not in ij.split("Budgets")[0]   # interceptor: read-only meter
    assert "cloudwatch:PutMetricData" in cj and "Aegis/Budget" in cj
    # the drafter refuses on the workflow hop -> its DENIED records need the append-only ledger grant
    # (mirrored per tenant), never Update/Delete on a ledger (mt6 sweep finding, 2026-09-03)
    assert "dynamodb:TransactWriteItems" in cj and "table/ben-bg-*-audit-ledger" in cj and "s3:PutObject" in cj
    for stmt in (st for p in pols.values() if any("CoreTools" in r.get("Ref", "") for r in p["Properties"]["Roles"])
                 for st in p["Properties"]["PolicyDocument"]["Statement"]):
        res = json.dumps(stmt.get("Resource"))
        if "audit-ledger" in res or "AuditLedger" in res:
            acts = stmt["Action"] if isinstance(stmt["Action"], list) else [stmt["Action"]]
            assert not {"dynamodb:UpdateItem", "dynamodb:DeleteItem"} & set(acts), stmt
    # alarms: 3 thresholds x 2 metrics x 2 tenants
    alarms = to.find_resources("AWS::CloudWatch::Alarm")
    names = {a["Properties"].get("AlarmName", "") for a in alarms.values()}
    assert {f"ben-bg-budget-{t}-{m}-{p}" for t in ("pha-a", "pha-b") for m in ("TokensUsedPct", "UsdUsedPct") for p in (60, 85, 100)} <= names
    # AWS Budgets USD ceiling + action + breach function
    to.has_resource_properties("AWS::Budgets::Budget", Match.object_like({"Budget": Match.object_like({
        "BudgetName": "ben-bg-bedrock-usd-ceiling", "BudgetType": "COST", "TimeUnit": "MONTHLY",
        "BudgetLimit": {"Amount": 25.5, "Unit": "USD"}, "CostFilters": {"Service": ["Amazon Bedrock"]}})}))
    to.has_resource_properties("AWS::Budgets::BudgetsAction", Match.object_like({
        "ActionType": "APPLY_IAM_POLICY", "ApprovalModel": "AUTOMATIC", "NotificationType": "ACTUAL",
        "ActionThreshold": {"Type": "PERCENTAGE", "Value": 100}}))
    oj = json.dumps(to.to_json())
    assert "AmazonBedrockAgentCoreSDKRuntime-x" in oj and "bedrock:InvokeModel" in oj and '"Effect": "Deny"' in oj.replace("\\", "")
    to.has_resource_properties("AWS::Lambda::Function", Match.object_like({"FunctionName": "ben-bg-budget-breach"}))
    to.has_resource_properties("AWS::SNS::Subscription", Match.object_like({"Protocol": "lambda"}))
    assert "lambda:InvokeFunctionUrl" in oj
    # without -c budget_usd: no Budgets resources, token alarms only
    app2 = aws_cdk.App()
    d2 = DataStack(app2, "d7", prefix="ben-bg2", retention_profile="sandbox-demo")
    c2 = ComputeStack(app2, "c7", prefix="ben-bg2", asset_dir=asset, data=d2, budget={"monthly_token_cap": 10, "prices_json": prices})
    w2 = WorkflowStack(app2, "w7", prefix="ben-bg2", compute=c2, data=d2)
    o2 = Template.from_stack(ObservabilityStack(app2, "o7", prefix="ben-bg2", compute=c2, workflow=w2, data=d2))
    assert not o2.find_resources("AWS::Budgets::Budget")
    assert "ben-bg2-budget-default-TokensUsedPct-100" in {a["Properties"].get("AlarmName", "") for a in o2.find_resources("AWS::CloudWatch::Alarm").values()}
