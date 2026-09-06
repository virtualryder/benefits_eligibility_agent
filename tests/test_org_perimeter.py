"""Account-boundary enforcement templates (org/) - the PREVENTIVE half of the Bedrock perimeter raised by
the 2026-09-05 enforcement-perimeter review. Static tests (no Organization needed): the shipped SCP /
endpoint policy / CloudTrail selectors are structurally sound, the renderer substitutes real principals
and stays sound, and - as a regression fixture - the SCP that was PROPOSED in that review fails the lint
for every one of its real defects (so those mistakes cannot be re-introduced by copy-paste)."""
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import render_org_perimeter as rop  # noqa: E402

ORG = ROOT / "org"


def _load(name):
    return json.loads((ORG / name).read_text(encoding="utf-8"))


def test_shipped_scp_and_endpoint_policy_lint_clean():
    assert rop.lint_scp(_load("scp-bedrock-runtime-perimeter.json")) == []
    assert rop.lint_vpce(_load("vpce-policy-bedrock-runtime.json")) == []
    assert len(json.dumps(_load("scp-bedrock-runtime-perimeter.json"), separators=(",", ":")).encode()) <= rop.SCP_MAX_BYTES


# The SCP proposed in the review, verbatim in structure. Each defect below is a REAL bypass:
#  - stmt 1 ANDs `aws:PrincipalType != AssumedRole` into the Deny, so NO role session is ever denied
#    (the EC2 / ECS / Lambda bypass it targets sails through);
#  - stmt 2 keys on aws:userId, i.e. the session name the CALLER chooses at AssumeRole time
#    (`--role-session-name AegisGovernanceProxy-anything` satisfies it);
#  - bedrock:Converse / ConverseStream are not IAM actions (dead text; Converse authorizes as InvokeModel);
#  - the aws-service-role exemption is noise (SCPs never apply to service-linked roles);
#  - nothing protects the allowlisted role names or the perimeter's telemetry.
PROPOSED_SCP = {
    "Version": "2012-10-17",
    "Statement": [
        {"Sid": "EnforceCentralizedGovernanceProxyForBedrockRuntime", "Effect": "Deny",
         "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:Converse",
                    "bedrock:ConverseStream", "bedrock:ApplyGuardrail"],
         "Resource": "*",
         "Condition": {"ArnNotLike": {"aws:PrincipalArn": ["arn:aws:iam::*:role/AegisGovernanceProxyExecutionRole*",
                                                            "arn:aws:iam::*:role/aws-service-role/*"]},
                       "StringNotLike": {"aws:PrincipalType": "AssumedRole"}}},
        {"Sid": "BlockBedrockCallsFromUnapprovedProxySessions", "Effect": "Deny",
         "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:Converse",
                    "bedrock:ConverseStream", "bedrock:ApplyGuardrail"],
         "Resource": "*",
         "Condition": {"StringNotLike": {"aws:userId": ["*:AegisGovernanceProxy*", "*:AWSServiceRoleFor*"]}}},
    ],
}


def test_proposed_review_scp_fails_lint_for_each_real_defect():
    problems = " | ".join(rop.lint_scp(PROPOSED_SCP))
    assert "aws:userId" in problems, "session-name keying must be flagged"
    assert "aws:PrincipalType" in problems, "the PrincipalType AND-trap must be flagged"
    assert "bedrock:Converse is not an IAM action" in problems
    assert "service-linked" in problems
    assert "not protected" in problems and "telemetry" in problems
    assert "misses actions" in problems, "the proposal misses agent / KB / async / batch inference surfaces"


def test_render_substitutes_real_principals_and_stays_sound(tmp_path, monkeypatch):
    monkeypatch.setattr(rop, "ORG", str(tmp_path))
    for name in ("scp-bedrock-runtime-perimeter.json", "vpce-policy-bedrock-runtime.json"):
        (tmp_path / name).write_text((ORG / name).read_text(encoding="utf-8"), encoding="utf-8")
    drafter = "arn:aws:iam::444455556666:role/ben-prod-compute-coretools"
    runtime = "arn:aws:iam::444455556666:role/AmazonBedrockAgentCoreSDKRuntime-us-east-1-9f8e7d"
    deployer = "arn:aws:iam::444455556666:role/aegis-platform-deployer"
    extra = "arn:aws:iam::444455556666:role/aegis-break-glass"
    out = rop.render(drafter, runtime, deployer, extras=[extra])
    scp = json.loads(pathlib.Path(out["scp-bedrock-runtime-perimeter.json"]).read_text(encoding="utf-8"))
    vp = json.loads(pathlib.Path(out["vpce-policy-bedrock-runtime.json"]).read_text(encoding="utf-8"))
    raw = json.dumps(scp) + json.dumps(vp)
    assert "EXAMPLE" not in raw and "111122223333" not in raw
    assert rop.lint_scp(scp) == [] and rop.lint_vpce(vp) == []
    inference = scp["Statement"][0]["Condition"]["ArnNotLike"]["aws:PrincipalArn"]
    assert inference == [drafter, extra, runtime], "allowlist order: drafter, extras, runtime"
    protect = scp["Statement"][1]
    assert protect["Resource"] == [drafter, extra, runtime]
    assert protect["Condition"]["ArnNotLike"]["aws:PrincipalArn"] == [deployer]
    assert vp["Statement"][0]["Condition"]["StringEquals"]["aws:PrincipalAccount"] == "444455556666"
    assert vp["Statement"][0]["Condition"]["ArnLike"]["aws:PrincipalArn"] == [drafter, extra]


def test_shipped_selectors_match_the_capture_trail():
    """org/cloudtrail-advanced-event-selectors.json is the landing-zone copy of exactly what the pack's
    LineageStack applies - it must never drift (a reviewer applying the org file must get the same net)."""
    pytest.importorskip("aws_cdk")
    sys.path.insert(0, str(ROOT / "cdk"))
    from ben_stacks.lineage_stack import LineageStack
    assert _load("cloudtrail-advanced-event-selectors.json") == LineageStack.advanced_event_selectors()
    types = {f["Equals"][0] for s in _load("cloudtrail-advanced-event-selectors.json")
             for f in s["FieldSelectors"] if f["Field"] == "resources.type"}
    assert {"AWS::Bedrock::Model", "AWS::Bedrock::Guardrail", "AWS::Bedrock::KnowledgeBase",
            "AWS::Bedrock::AgentAlias", "AWS::BedrockAgentCore::Gateway"} <= types
