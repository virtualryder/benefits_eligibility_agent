#!/usr/bin/env python3
"""render_org_perimeter — render + LINT the account-boundary enforcement templates under org/.

The templates ship with EXAMPLE principal ARNs. This script substitutes the real ones (the governed
drafter role, the AgentCore runtime role, the platform deployer role, optional break-glass) and writes
org/rendered/*.json, then lints every policy against the mistakes an enforcement SCP must not make:

  * only REAL Bedrock IAM actions (Converse / ConverseStream are NOT IAM actions - they authorize as
    InvokeModel / InvokeModelWithResponseStream; listing them is dead text);
  * the allowlist keys on aws:PrincipalArn (which resolves to the ROLE arn for a role session) - NEVER
    on aws:userId / the session name, which the caller chooses when it calls AssumeRole;
  * no aws:PrincipalType condition ANDed into a Deny (a Deny that also requires PrincipalType !=
    AssumedRole never denies a role - i.e. never denies the EC2 / ECS / Lambda bypass it exists for);
  * no service-linked-role exemption (SCPs never apply to service-linked roles; the exemption is noise);
  * the allowlisted role names are PROTECTED (a second statement denies creating / re-pointing a role
    that would match the allowlist to anyone but the deployer);
  * the perimeter's own telemetry is protected (invocation logging + the capture trail).

Usage:
    python scripts/render_org_perimeter.py --drafter-role-arn ARN --runtime-role-arn ARN \
        --deployer-role-arn ARN [--extra-principal ARN ...] [--outputs cdk-outputs.json]
    python scripts/render_org_perimeter.py --lint            # lint the shipped templates only
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ORG = os.path.join(REPO, "org")

# Real Bedrock actions that invoke a model / agent / knowledge base / guardrail (Service Authorization
# Reference). Converse / ConverseStream deliberately absent: they are API operations, not IAM actions.
BEDROCK_INFERENCE_ACTIONS = {
    "bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:InvokeModelWithBidirectionalStream",
    "bedrock:InvokeAgent", "bedrock:InvokeInlineAgent", "bedrock:InvokeFlow", "bedrock:Retrieve",
    "bedrock:RetrieveAndGenerate", "bedrock:StartAsyncInvoke", "bedrock:CreateModelInvocationJob",
    "bedrock:ApplyGuardrail",
}
NOT_IAM_ACTIONS = {"bedrock:Converse", "bedrock:ConverseStream"}
SCP_MAX_BYTES = 5120


def _stmts(doc):
    s = doc.get("Statement", [])
    return s if isinstance(s, list) else [s]


def _as_list(v):
    return v if isinstance(v, list) else [v]


def lint_scp(doc):
    """Return a list of problems (empty == clean)."""
    problems = []
    raw = json.dumps(doc, separators=(",", ":"))
    if len(raw.encode("utf-8")) > SCP_MAX_BYTES:
        problems.append("SCP exceeds the %d-byte limit" % SCP_MAX_BYTES)
    if "aws:userId" in raw or "aws:userid" in raw:
        problems.append("keys on aws:userId (caller-chosen session name) - use aws:PrincipalArn")
    if "aws-service-role" in raw:
        problems.append("exempts service-linked roles - SCPs never apply to them; the exemption is noise")
    if "aws:PrincipalType" in raw:
        problems.append("uses aws:PrincipalType - ANDed into a Deny it exempts every role session")
    for a in NOT_IAM_ACTIONS:
        if a in raw:
            problems.append("%s is not an IAM action (Converse authorizes as InvokeModel)" % a)
    inference = [s for s in _stmts(doc) if s.get("Effect") == "Deny"
                 and BEDROCK_INFERENCE_ACTIONS & set(_as_list(s.get("Action", [])))]
    if not inference:
        problems.append("no Deny statement over the Bedrock inference actions")
    for s in inference:
        acts = set(_as_list(s.get("Action", [])))
        missing = BEDROCK_INFERENCE_ACTIONS - acts
        if missing:
            problems.append("inference Deny misses actions: %s" % ", ".join(sorted(missing)))
        cond = s.get("Condition", {})
        pa = (cond.get("ArnNotLike") or {}).get("aws:PrincipalArn")
        if not pa:
            problems.append("inference Deny must allowlist via Condition.ArnNotLike.aws:PrincipalArn")
        elif not all(re.match(r"^arn:aws:iam::\d{12}:role/", p) for p in _as_list(pa)):
            problems.append("allowlist entries must be explicit role ARNs (arn:aws:iam::<acct>:role/...)")
    protect = [s for s in _stmts(doc) if s.get("Effect") == "Deny"
               and {"iam:CreateRole", "iam:UpdateAssumeRolePolicy", "iam:AttachRolePolicy", "iam:PutRolePolicy"}
               <= set(_as_list(s.get("Action", [])))]
    if not protect:
        problems.append("allowlisted identities are not protected (no Deny on iam:CreateRole/UpdateAssumeRolePolicy/"
                        "AttachRolePolicy/PutRolePolicy for the allowlisted role ARNs)")
    telemetry = [s for s in _stmts(doc) if s.get("Effect") == "Deny"
                 and {"bedrock:DeleteModelInvocationLoggingConfiguration", "cloudtrail:StopLogging",
                      "cloudtrail:DeleteTrail", "cloudtrail:PutEventSelectors"} <= set(_as_list(s.get("Action", [])))]
    if not telemetry:
        problems.append("perimeter telemetry is not protected (invocation logging + capture trail)")
    return problems


def lint_vpce(doc):
    problems = []
    raw = json.dumps(doc)
    if "aws:userId" in raw:
        problems.append("endpoint policy keys on aws:userId")
    for s in _stmts(doc):
        if s.get("Effect") != "Allow":
            problems.append("endpoint policy should be Allow-only (anything not allowed is denied)")
        cond = s.get("Condition", {})
        if not (cond.get("ArnLike") or cond.get("ArnEquals") or {}).get("aws:PrincipalArn"):
            problems.append("endpoint Allow must be conditioned on aws:PrincipalArn")
        if not (cond.get("StringEquals") or {}).get("aws:PrincipalAccount"):
            problems.append("endpoint Allow must be conditioned on aws:PrincipalAccount")
        for a in NOT_IAM_ACTIONS:
            if a in _as_list(s.get("Action", [])):
                problems.append("%s is not an IAM action" % a)
    return problems


def _sub(obj, mapping):
    """Replace EXAMPLE principal ARNs. mapping: substring-key -> list of real ARNs."""
    if isinstance(obj, list):
        out = []
        for v in obj:
            if isinstance(v, str) and "EXAMPLE" in v:
                for key, arns in mapping.items():
                    if key in v:
                        out.extend(arns)
                        break
                else:
                    raise SystemExit("no substitution for placeholder %s" % v)
            else:
                out.append(_sub(v, mapping))
        return out
    if isinstance(obj, dict):
        return {k: _sub(v, mapping) for k, v in obj.items()}
    if isinstance(obj, str) and "EXAMPLE" in obj:
        for key, arns in mapping.items():
            if key in obj:
                return arns[0]
        raise SystemExit("no substitution for placeholder %s" % obj)
    return obj


def render(drafter, runtime, deployer, extras=()):
    mapping = {"coretoolsServiceRole": [drafter] + list(extras), "AgentCoreSDKRuntime": [runtime] if runtime else [],
               "platform-deployer": [deployer]}
    out_dir = os.path.join(ORG, "rendered")
    os.makedirs(out_dir, exist_ok=True)
    written = {}
    for name, linter in (("scp-bedrock-runtime-perimeter.json", lint_scp), ("vpce-policy-bedrock-runtime.json", lint_vpce)):
        doc = _sub(json.load(open(os.path.join(ORG, name), encoding="utf-8")), mapping)
        # the VPCE policy account must match the principal's account
        if name.startswith("vpce"):
            acct = re.match(r"^arn:aws:iam::(\d{12}):", drafter).group(1)
            for s in _stmts(doc):
                s["Condition"]["StringEquals"]["aws:PrincipalAccount"] = acct
        problems = linter(doc)
        if problems:
            raise SystemExit("%s: %s" % (name, "; ".join(problems)))
        p = os.path.join(out_dir, name)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=2)
            fh.write("\n")
        written[name] = p
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafter-role-arn")
    ap.add_argument("--runtime-role-arn", default="")
    ap.add_argument("--deployer-role-arn")
    ap.add_argument("--extra-principal", action="append", default=[])
    ap.add_argument("--lint", action="store_true", help="lint the shipped templates and exit")
    a = ap.parse_args()
    if a.lint or not (a.drafter_role_arn and a.deployer_role_arn):
        scp = json.load(open(os.path.join(ORG, "scp-bedrock-runtime-perimeter.json"), encoding="utf-8"))
        vp = json.load(open(os.path.join(ORG, "vpce-policy-bedrock-runtime.json"), encoding="utf-8"))
        problems = {"scp": lint_scp(scp), "vpce": lint_vpce(vp)}
        print(json.dumps(problems, indent=1))
        sys.exit(1 if any(problems.values()) else 0)
    written = render(a.drafter_role_arn, a.runtime_role_arn, a.deployer_role_arn, a.extra_principal)
    print(json.dumps({"rendered": written}, indent=1))


if __name__ == "__main__":
    main()
