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
                "DraftNotice", "AuditIntent", "HumanSignoff", "Finalize", "Committed"]
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
