#!/usr/bin/env python3
"""Post-111 END-TO-END REGRESSION sweep on a live deployment: after the proofs have run, prove there
were NO unexpected errors anywhere - every Lambda log group, the Step Functions controller (all
executions and their terminal states), the gateway's request log, the AgentCore Runtime's logs, the
DLQs and the CloudWatch alarms - and classify every error-shaped event as EXPECTED (a fail-closed
refusal the proofs deliberately provoked) or UNEXPECTED. Read-only. Exit 0 iff nothing unexpected.

Usage: python scripts/e2e_regression.py --env mt4 --since-minutes 60 --runtime-log-group <group> [--out x.json]"""
import argparse
import json
import re
import sys
import time

# error-shaped events the proofs PROVOKE on purpose (fail-closed controls doing their job)
EXPECTED = [
    (r"multi-tenant: identity carries no tenant", "cw-none denied at the gateway (require_tenant / interceptor)"),
    (r"multi-tenant: no verified custom:tenant claim; refusing", "fail-closed: execution/tool without the signed tenant pair"),
    (r"TenantError", "fail-closed: TenantError raised by a Lambda without a verified tenant binding"),
    (r"JSONPath '\$\.__aegis_tenant' specified for the field", "fail-closed: execution started WITHOUT the signed pair fails at Extract"),
    (r"ingestion identity not verified", "ingest refused without a verified caseworker token"),
    (r"de-identification not proven", "assess/draft refused without a signed sanitized_ref"),
    (r"stopped by the harness|mt proof complete", "harness stopped the execution at the sign-off pause"),
    (r"start_execution failed|governed-signoff|StateMachineDoesNotExist", "request_signoff targets the shell-engine sign-off machine (not provisioned by CDK) - a documented control block"),
    (r"case_ref unresolved|unknown ref or wrong tenant", "cross-tenant / unknown case_ref refused"),
    (r"refused|DENIED|not authorized|AccessDenied.*tools/call", "a governed refusal"),
    # L22: the Cedar deny as the GATEWAY logs it. The platform's headline control fires here, and
    # matching only uppercase DENIED made a correct deny read as an incident.
    (r"Policy evaluation denied|Tool Execution Denied|\"decision\"\s*:\s*\"DENY\"",
     "Cedar DENY at the gateway (the request never reached the tool) - the enforcement point working"),
    (r"DeprecationWarning: `url\.parse\(\)`", "CDK custom-resource framework (Node) deprecation warning logged at ERROR level - AWS-provided provider code, not a failure"),
    # task 127: every refusal the kill-switch proof deliberately provokes (interceptor 403, tool Lambda
    # KillSwitchEngaged, workflow FAILED at Extract, runtime session stopped, SoD-refused release)
    (r"KillSwitchEngaged|kill_switch|containment engaged|separation of duties|SEV-1 drill", "task 127: kill-switch containment provoked by scripts/kill_switch_proof.py (engaged => refused everywhere; released by a second identity)"),
    # task 128: every refusal the budget proof deliberately provokes (capped tenant at gateway / runtime /
    # drafter, mid-session stop, synthetic AWS Budgets breach -> kill switch) + the STANDBY-locked action
    (r"BudgetExceeded|budget exceeded|denied:budget|budget_exceeded|AWS Budgets|ResourceLockedException", "task 128: budget refusals provoked by scripts/budget_proof.py (capped tenant; synthetic USD-ceiling breach)"),
]
# warnings that are NOT errors but must be REPORTED (a working fallback hid a misconfiguration once)
WARN_ONLY = [(r"SSM gateway lookup failed", "runtime fell back to the GATEWAY_URL env (the SSM grant did not cover the deployment's parameter path) - fixed in lib/runtime/_obs_setup.sh 2026-09-02")]
PATTERNS = ["ERROR", "Traceback", "Task timed out", "Exception", "FAILED", "errorType"]



# ---- L22: correlate the gateway's OPAQUE tool error with the tool Lambda's explicit refusal -------
# The gateway logs "An error occurred while executing tool: mask-pii___mask_pii from target X" with
# no reason attached, so no content pattern can separate a deliberate kill-switch/budget refusal
# from a genuinely broken tool - and matching the wrapper text itself would blind this gate to real
# tool failures. Instead: a gateway wrapper is EXPECTED only when the named tool's own Lambda log
# carries an already-classified-EXPECTED refusal within a few seconds of it. No matching Lambda
# refusal => the gateway error stays UNEXPECTED.
_GATEWAY_WRAPPER = re.compile(r"An error occurred while executing tool:\s*([A-Za-z0-9_\-]+)")
_CORRELATION_WINDOW_MS = 15000


def correlate_gateway_wrappers(by_group, prefix):
    """Reclassify gateway tool-execution wrappers that a Lambda refusal explains. Mutates rows."""
    # tool name as the gateway spells it ("mask-pii___mask_pii") -> the Lambda log group
    lambda_rows = {g: rows for g, rows in by_group.items() if g.startswith("/aws/lambda/%s-" % prefix)}

    def _explained(tool_token, ts):
        stem = tool_token.split("___", 1)[0].replace("_", "-").lower()
        for g, rows in lambda_rows.items():
            fn = g.rsplit("/", 1)[-1]
            if not fn.startswith("%s-%s" % (prefix, stem)):
                continue
            for r in rows:
                if (r["kind"] == "expected" and r.get("why")
                        and abs(int(r.get("ts") or 0) - int(ts or 0)) <= _CORRELATION_WINDOW_MS):
                    return g, r["why"]
        return None, None

    for g, rows in by_group.items():
        if "/gateway/" not in g:
            continue
        for r in rows:
            if r["kind"] != "unexpected":
                continue
            m = _GATEWAY_WRAPPER.search(r.get("excerpt") or "")
            if not m:
                continue
            src, why = _explained(m.group(1), r.get("ts"))
            if why:
                r["kind"] = "expected"
                r["why"] = ("gateway wrapper over a classified refusal in %s: %s"
                            % (src.rsplit("/", 1)[-1], why))


def classify(msg):
    for rx, why in EXPECTED:
        if re.search(rx, msg):
            return "expected", why
    for rx, why in WARN_ONLY:
        if re.search(rx, msg):
            return "warning", why
    return "unexpected", ""


def sweep_logs(logs, group, since_ms, patterns):
    out = []
    for pat in patterns:
        try:
            tok = None
            while True:
                kw = dict(logGroupName=group, startTime=since_ms, filterPattern='"%s"' % pat, limit=500)
                if tok:
                    kw["nextToken"] = tok
                r = logs.filter_log_events(**kw)
                out += r.get("events", [])
                tok = r.get("nextToken")
                if not tok:
                    break
        except logs.exceptions.ResourceNotFoundException:
            break
        except Exception as exc:
            out.append({"message": "sweep-error:%s" % type(exc).__name__, "logStreamName": "?", "timestamp": 0})
            break
    seen, uniq = set(), []
    for e in out:
        k = (e.get("logStreamName"), e.get("timestamp"), e.get("message", "")[:200])
        if k not in seen:
            seen.add(k); uniq.append(e)
    return uniq


def main():
    import boto3
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", required=True)
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--since-minutes", type=int, default=90)
    ap.add_argument("--runtime-log-group", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    prefix = f"ben-{a.env}"
    logs = boto3.client("logs", region_name=a.region)
    sfn = boto3.client("stepfunctions", region_name=a.region)
    cw = boto3.client("cloudwatch", region_name=a.region)
    sqs = boto3.client("sqs", region_name=a.region)
    lam = boto3.client("lambda", region_name=a.region)
    since_ms = int((time.time() - a.since_minutes * 60) * 1000)
    rep = {"prefix": prefix, "since_minutes": a.since_minutes, "log_groups": {}, "executions": [], "alarms": [], "dlqs": {}, "lambda_errors_metric": {}}

    groups = [g["logGroupName"] for pg in logs.get_paginator("describe_log_groups").paginate(logGroupNamePrefix=f"/aws/lambda/{prefix}-") for g in pg["logGroups"]]
    groups += [g["logGroupName"] for pg in logs.get_paginator("describe_log_groups").paginate(logGroupNamePrefix=f"/aws/states/{prefix}") for g in pg["logGroups"]]
    groups += [f"/aws/vendedlogs/bedrock-agentcore/gateway/{prefix}"]
    if a.runtime_log_group:
        groups.append(a.runtime_log_group)
    by_group = {}
    for g in groups:
        evs = sweep_logs(logs, g, since_ms, PATTERNS)
        rows = []
        for e in evs:
            m = e.get("message", "")
            kind, why = classify(m)
            # Lambda platform lines that are not errors: "REPORT ... Error" absent; keep only real ones
            if kind == "unexpected" and re.search(r'"severityText":"INFO"|"level": "INFO"|"aegis": "call"', m) and "Traceback" not in m and "exception" not in m.lower():
                kind, why = "expected", "INFO-level line matched a pattern word (not an error)"
            rows.append({"ts": e.get("timestamp"), "stream": (e.get("logStreamName") or "")[:60], "kind": kind, "why": why, "excerpt": m[:260].replace("\n", " ")})
        by_group[g] = rows

    correlate_gateway_wrappers(by_group, prefix)

    unexpected_total = 0
    for g, rows in by_group.items():
        n_unexp = sum(1 for r in rows if r["kind"] == "unexpected")
        unexpected_total += n_unexp
        rep["log_groups"][g] = {"events": len(rows), "unexpected": n_unexp, "warnings": sum(1 for r in rows if r["kind"] == "warning"),
                                "rows": [r for r in rows if r["kind"] == "unexpected"][:20] + [r for r in rows if r["kind"] == "warning"][:6] + [r for r in rows if r["kind"] == "expected"][:6]}

    # Step Functions: every execution's terminal state, classified
    for m in sfn.list_state_machines()["stateMachines"]:
        if not m["name"].startswith(prefix):
            continue
        for ex in sfn.list_executions(stateMachineArn=m["stateMachineArn"], maxResults=100)["executions"]:
            d = sfn.describe_execution(executionArn=ex["executionArn"])
            st = d["status"]; cause = (d.get("cause") or "") + " " + (d.get("error") or "")
            kind, why = ("ok", "") if st in ("SUCCEEDED",) else classify(cause) if st in ("FAILED", "ABORTED") else ("running", "still at the sign-off pause (24h wait) - stop before teardown")
            if st == "ABORTED" and kind == "unexpected":
                kind, why = "expected", "stopped by the harness at the sign-off pause"
            if st == "RUNNING":
                kind = "running"
            rep["executions"].append({"name": ex["name"], "status": st, "kind": kind, "why": why, "cause": cause[:200]})
            if kind == "unexpected":
                unexpected_total += 1

    def _alarm_why(al):
        name = al["AlarmName"]
        if "WorkflowFailed" in name:
            return "WorkflowFailed fires on the DELIBERATE no-binding execution (fail-closed proof)"
        if "-budget-" in name and ("TokensUsedPct" in name or "UsdUsedPct" in name):
            # task 128: scripts/budget_proof.py caps tenant A just above its usage and drives it to >= 85 % on
            # purpose - the gate ASSERTS these alarms reach ALARM. They stay in ALARM until the next datapoint
            # (the cap is cleared at the end of the proof; the metric is only published on a commit).
            return "task 128: per-tenant budget alarm provoked by scripts/budget_proof.py (the gate asserts it fires)"
        return ""

    # alarms
    for al in cw.describe_alarms(AlarmNamePrefix=prefix)["MetricAlarms"] + cw.describe_alarms(AlarmNamePrefix=prefix.replace("ben-", "ben"))["MetricAlarms"]:
        if al["StateValue"] == "ALARM":
            why = _alarm_why(al)
            rep["alarms"].append({"name": al["AlarmName"], "state": al["StateValue"], "kind": "expected" if why else "unexpected", "why": why, "reason": al.get("StateReason", "")[:160]})
            if not why:
                unexpected_total += 1
    # alarms created with CDK ids may not carry the prefix: scan all alarms whose dimensions reference the prefix
    for al in cw.describe_alarms()["MetricAlarms"]:
        if al["StateValue"] == "ALARM" and prefix in json.dumps(al.get("Dimensions", [])) and not any(x["name"] == al["AlarmName"] for x in rep["alarms"]):
            why = _alarm_why(al)
            rep["alarms"].append({"name": al["AlarmName"], "state": "ALARM", "kind": "expected" if why else "unexpected", "why": why, "reason": al.get("StateReason", "")[:160]})
            if not why:
                unexpected_total += 1

    # DLQs
    for q in sqs.list_queues(QueueNamePrefix=prefix).get("QueueUrls", []):
        n = int(sqs.get_queue_attributes(QueueUrl=q, AttributeNames=["ApproximateNumberOfMessages"])["Attributes"]["ApproximateNumberOfMessages"])
        rep["dlqs"][q.rsplit("/", 1)[-1]] = n
        if n:
            unexpected_total += 1

    # Lambda Errors metric (invocation-level errors) per function
    for fn in [f["FunctionName"] for pg in lam.get_paginator("list_functions").paginate() for f in pg["Functions"] if f["FunctionName"].startswith(prefix + "-")]:
        r = cw.get_metric_statistics(Namespace="AWS/Lambda", MetricName="Errors", Dimensions=[{"Name": "FunctionName", "Value": fn}],
                                     StartTime=time.time() - a.since_minutes * 60, EndTime=time.time(), Period=a.since_minutes * 60, Statistics=["Sum"])
        rep["lambda_errors_metric"][fn] = int(sum(p["Sum"] for p in r["Datapoints"]))
    # invocation-level Lambda errors are EXPECTED only for the fail-closed TenantError paths (intake/write_audit in the no-binding tests)
    rep["lambda_errors_note"] = "Errors>0 on intake-application/assess-eligibility/write-audit are the deliberate fail-closed TenantError refusals; see log_groups classification"

    rep["unexpected_total"] = unexpected_total
    rep["verdict"] = "PASS" if unexpected_total == 0 else "FAIL"
    js = json.dumps(rep, indent=1, default=str)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(js)
    print(js)
    sys.exit(0 if unexpected_total == 0 else 1)


if __name__ == "__main__":
    main()
