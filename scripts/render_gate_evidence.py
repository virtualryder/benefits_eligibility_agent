#!/usr/bin/env python3
"""Render the redacted full-portfolio gate evidence document from the gate's JSON.

REL-6. Written as a script rather than by hand so the evidence cannot drift from the run it
describes: every number in the document is read out of the JSON the gate itself wrote. The account
id is redacted here, at render time, so a raw id can never reach a committed evidence file by
someone forgetting a sed - `tools/scan_account_ids.py` remains the backstop, not the mechanism.
"""
import argparse
import io
import json
import os

REAL_ACCOUNT = "864217980669"
REDACTED = "111122223333"

# what each check actually establishes, in plain words - the JSON detail alone is not evidence,
# it is a measurement; the claim is what a reader needs.
CLAIMS = {
    "deploy": "All nine stacks deploy from zero (CloudFormation is the authority, not the CLI exit code)",
    "outputs_present": "Identity, gateway and compute publish the outputs the rest of the platform binds to",
    "RT2_configure_on_iac_role": "The AgentCore Runtime is CONFIGURED against the IaC execution role, not a console-made one",
    "RT2_launch": "The runtime launches on that role",
    "RT2_runtime_uses_iac_role": "The live runtime's execution role is the IaC role (RT-2)",
    "RT2_runtime_ready": "The runtime reaches READY",
    "RT2_runtime_mmdsv2": "IMDSv2 is required on the runtime",
    "G111_consolidated_gate": "Phase-111 consolidated governance gate: tenant isolation, transparency, PII canary",
    "KS_kill_switch_proof": "The kill switch stops a running agent mid-session",
    "BUD_budget_proof": "The per-token/USD budget ceiling refuses work when breached",
    "RT2_runtime_calls_guardrail_assessed": "Every model call from the runtime was guardrail-assessed",
    "LIN_case_driven": "One real case drives the full workflow through every governed state",
    "LIN_zero_orphans": "Every governed tool invocation in CloudTrail has a matching aegis.call audit line, and vice versa",
    "E2E_zero_unexpected": "No unexpected error in any log group; every refusal is a classified, deliberate one",
    # Runs before 2026-09-08 used the name `teardown_zero_residue`. That name overclaimed: the
    # check verifies stacks + model-logging config, and the toolkit's ECR repository survives
    # teardown (L37). Renamed at the source; the old key is still described here because the
    # evidence files that carry it are records of past runs and must not be rewritten.
    "teardown_zero_residue": "(pre-2026-09-08 name) Stacks are gone and model-invocation logging is restored - does NOT cover the toolkit ECR repository (L37)",
    "teardown_zero_stack_residue": "Every CloudFormation stack for this run is gone and model-invocation logging is restored. The AgentCore toolkit's ECR repository is NOT covered - it is measured under steps.toolkit_residue (L37)",
}


def redact(x):
    if isinstance(x, str):
        return x.replace(REAL_ACCOUNT, REDACTED)
    if isinstance(x, dict):
        return {k: redact(v) for k, v in x.items()}
    if isinstance(x, list):
        return [redact(v) for v in x]
    return x


# Some checks carry the raw stdout of a CLI that draws boxes. A table cell full of U+2500s is not
# evidence, it is noise - keep the assertions (EXIT codes, counts, verdicts) and drop the drawing.
_BOX = "\u2500\u2502\u250c\u2510\u2514\u2518\u251c\u2524\u252c\u2534\u253c\u2550\u2551\u2554\u2557\u255a\u255d"


def clean_detail(text, width=220):
    text = " ".join((text or "").split())
    for ch in _BOX:
        text = text.replace(ch, " ")
    text = text.replace("|", " ").replace('"', "")
    keep = [w for w in text.split() if w]
    text = " ".join(keep)
    # prefer the assertion-bearing fragments when the line is mostly CLI chatter
    marks = [w for w in keep if "EXIT=" in w or "=" in w and w.count("=") == 1 and not w.startswith("http")]
    if len(text) > width and marks:
        text = " ".join(dict.fromkeys(marks))
    return text[:width].strip()


def _secs(steps, key):
    s = steps.get(key) or {}
    return s.get("secs") if isinstance(s, dict) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--commit", default="")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()

    d = redact(json.load(io.open(a.json, encoding="utf-8")))
    checks, steps = d["checks"], d.get("steps", {})
    n_ok = sum(1 for c in checks.values() if c["ok"])
    n = len(checks)
    verdict = "**PASS**" if d.get("PASS") else "**FAIL**"

    L = []
    L.append("# Full-portfolio gate — %s (%s) — %s %d/%d" % (d["prefix"], d["date"], verdict, n_ok, n))
    L.append("")
    L.append("**What this is.** ONE from-zero deployment of the benefits pack (env `%s`, region `%s`, "
             "nine stacks, two tenants, Bedrock model-invocation logging on, the AgentCore Runtime "
             "launched on the IaC execution role), against which every governance proof ran back to "
             "back on the same live environment, then torn down and the account's prior "
             "model-invocation logging configuration restored." % (d["env"], d["region"]))
    if a.commit:
        L.append("Product tree: commit `%s`%s." % (a.commit, (" = tag `%s`" % a.tag) if a.tag else ""))
    L.append("")
    L.append("From zero means from zero: the preceding teardown asserted zero residue before this run "
             "started, so nothing here rides on state left by an earlier deployment. That distinction "
             "is not academic — it is what surfaced the settle-window and correlation defects recorded "
             "in `WOGplatform/docs/GAP-CLOSURE-BACKLOG.md` (L21–L31).")
    L.append("")
    L.append("## Verdict")
    L.append("")
    L.append("| # | check | result | what it establishes | measured |")
    L.append("|---|---|---|---|---|")
    for i, (k, v) in enumerate(checks.items(), 1):
        detail = clean_detail(v.get("detail"))
        L.append("| %d | `%s` | %s | %s | %s |"
                 % (i, k, "**PASS**" if v["ok"] else "**FAIL**", CLAIMS.get(k, ""), detail))
    L.append("")

    lv = steps.get("lineage_verdict") or {}
    if lv:
        c = lv.get("counts", {})
        s = lv.get("settle", {})
        L.append("## Lineage parity (the load-bearing claim)")
        L.append("")
        L.append("Governed-tool invocations recorded by CloudTrail against `aegis.call` audit lines written "
                 "by the tools themselves — read from two independent systems, correlated on case id, "
                 "trace id and execution ARN:")
        L.append("")
        L.append("| source | count |")
        L.append("|---|---|")
        for key, label in (("cloudtrail_lambda_invokes", "CloudTrail governed-Lambda invokes"),
                           ("aegis_calls", "`aegis.call` audit lines"),
                           ("worm_records", "WORM ledger records"),
                           ("sfn_events", "Step Functions events"),
                           ("model_invocations", "Bedrock model invocations"),
                           ("gateway_requests", "gateway requests")):
            if key in c:
                L.append("| %s | %s |" % (label, c[key]))
        L.append("")
        L.append("Coverage: **%s**, orphans: **%d**. Settle waited %ss over %s polls (bound %ss). "
                 "The wait is recorded because an expired deadline still FAILS — \"we waited and nothing "
                 "arrived\" can never be confused with \"we did not wait\"."
                 % (lv.get("covered"), len(lv.get("orphans") or []), s.get("waited_sec"),
                    s.get("polls"), s.get("max_sec")))
        L.append("")

    L.append("## Timings")
    L.append("")
    L.append("| phase | seconds |")
    L.append("|---|---|")
    for key, label in (("deploy", "deploy (nine stacks, from zero)"), ("gate_111", "phase-111 consolidated gate"),
                       ("kill_switch", "kill-switch proof"), ("budget", "budget proof"),
                       ("lineage", "lineage proof (incl. settle)"), ("e2e", "regression sweep"),
                       ("destroy", "teardown")):
        v = _secs(steps, key)
        if v is not None:
            L.append("| %s | %s |" % (label, v))
    L.append("")

    L.append("## What this does NOT prove")
    L.append("")
    L.append("- Cognito MFA enforcement and the WAF rules are asserted in CDK and unit-tested, not "
             "exercised live in this run.")
    L.append("- One pack (benefits). PV and EDU carry the same control set by parity but were not "
             "live-gated here; Housing is a partial pack (see PACK-PARITY).")
    L.append("- Object Lock is exercised in GOVERNANCE mode with a 1-day retention, not COMPLIANCE "
             "(EV-1 needs a disposable account).")
    L.append("- The AgentCore runtime survives teardown: `DeleteAgentRuntime` is denied to the "
             "operator user and the prefix residue sweep does not cover it (L30, open).")
    L.append("")
    L.append("Account ids in this document are redacted to the AWS documentation example account "
             "`%s`." % REDACTED)
    L.append("")

    txt = "\n".join(L)
    assert REAL_ACCOUNT not in txt, "redaction failed"
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
    print("wrote %s (%d checks, %d passed)" % (a.out, n, n_ok))


if __name__ == "__main__":
    main()
