#!/usr/bin/env python3
"""lineage_proof.py (#168) - prove that EVERY governed API call is captured and joins into ONE lineage.

The pack already has per-source observability (WORM ledger, gateway log, per-Lambda `aegis.call`, the
Step Functions history, and the Bedrock model-invocation log). scripts/trace_case.py joins those into
one timeline for a case. What THIS proof adds is the account-wide CAPTURE (the LineageStack trail:
management ALL + S3/Lambda data events, multi-region, file-validation) and, on top of the join, a
COVERAGE ASSERTION: no governed API call may be

  * invoked-but-unaudited  - a governed tool Lambda that AWS recorded being invoked (a CloudTrail
    Lambda data event) with NO matching `aegis.call` line -> a side effect the audit trail missed;
  * audited-but-uninvoked  - an `aegis.call` line with NO matching CloudTrail invoke -> an audit
    record with no captured API call behind it;
  * uncorrelated           - a governed node (audit line, evidence record, model invocation) that
    carries NONE of the run's correlation keys (trace_id / session_id / execution_arn / case_id),
    so it cannot be tied into the lineage.

Any of those is an ORPHAN and FAILS the proof. On success the joined lineage + the verdict are written
to the capture WORM bucket, so the coverage evidence is itself under Object-Lock custody.

The join/coverage logic is pure (build_lineage / assess_coverage) and is unit-tested offline in
tests/test_lineage_coverage.py, including that an injected orphan is detected. main() wires the live
AWS sources through the same functions.
"""
import argparse
import json
import time

# Correlation keys a governed node must carry at least one of to join the run's lineage.
CORRELATION_KEYS = ("trace_id", "session_id", "execution_arn", "case_id")

# CloudTrail event names for a Lambda synchronous/async invoke across API versions.
_LAMBDA_INVOKE_EVENTS = {"Invoke", "InvokeFunction", "Invoke20150331", "InvokeAsync"}


def tool_of(function_name, tool_names):
    """Map a CloudTrail Lambda functionName back to the logical governed tool it hosts. The governed
    Lambdas embed the tool name in the function name (e.g. ben-gate-mask_pii). Longest match wins so
    'signoff_register' is not shadowed by 'request_signoff' etc."""
    fn = function_name or ""
    hits = [t for t in tool_names if t and t in fn]
    return max(hits, key=len) if hits else None


def assess_coverage(sources, tool_names):
    """The coverage assertion. `sources` is a dict of lists (cloudtrail, aegis, worm, model_log, sfn,
    gateway); see the fixtures in the offline test for the exact node shapes. Returns a verdict dict
    with covered:bool and the list of orphans."""
    orphans = []

    # --- A/B: per-tool parity between CloudTrail Lambda invokes and aegis.call audit lines ----------
    ct_invokes, aegis_calls = {}, {}
    for e in sources.get("cloudtrail", []):
        if e.get("event_source") == "lambda.amazonaws.com" and e.get("event_name") in _LAMBDA_INVOKE_EVENTS:
            t = tool_of(e.get("target", ""), tool_names)
            if t:
                ct_invokes[t] = ct_invokes.get(t, 0) + 1
    for a in sources.get("aegis", []):
        t = a.get("tool")
        if t:
            aegis_calls[t] = aegis_calls.get(t, 0) + 1
    for t in sorted(set(ct_invokes) | set(aegis_calls)):
        ci, ai = ct_invokes.get(t, 0), aegis_calls.get(t, 0)
        if ci > ai:
            orphans.append({"type": "invoked_not_audited", "tool": t,
                            "cloudtrail_invokes": ci, "aegis_calls": ai,
                            "detail": "a governed tool was invoked (CloudTrail) more times than it was audited (aegis.call)"})
        elif ai > ci:
            orphans.append({"type": "audited_not_invoked", "tool": t,
                            "cloudtrail_invokes": ci, "aegis_calls": ai,
                            "detail": "an aegis.call audit line has no captured CloudTrail invoke behind it"})

    # --- C: every governed node must carry at least one correlation key ----------------------------
    for src in ("aegis", "worm", "model_log"):
        for n in sources.get(src, []):
            if not any(n.get(k) for k in CORRELATION_KEYS):
                orphans.append({"type": "uncorrelated", "source": src,
                                "node": {k: n.get(k) for k in CORRELATION_KEYS},
                                "detail": "a governed node carries none of the run's correlation keys"})

    counts = {
        "cloudtrail_lambda_invokes": sum(ct_invokes.values()),
        "aegis_calls": sum(aegis_calls.values()),
        "worm_records": len(sources.get("worm", [])),
        "model_invocations": len(sources.get("model_log", [])),
        "sfn_events": len(sources.get("sfn", [])),
        "gateway_requests": len(sources.get("gateway", [])),
    }
    return {"covered": not orphans, "orphans": orphans, "counts": counts,
            "per_tool": {t: {"cloudtrail_invokes": ct_invokes.get(t, 0), "aegis_calls": aegis_calls.get(t, 0)}
                         for t in sorted(set(ct_invokes) | set(aegis_calls))}}


def build_lineage(sources):
    """Flatten the per-source nodes into ONE list ordered by timestamp; each node keeps its source, a
    short summary, and its correlation keys, so the result is the single joined lineage."""
    rows = []

    def add(ts, source, kind, summary, node, extra=None):
        rows.append({"ts": ts or 0, "source": source, "kind": kind, "summary": summary,
                     "correlation": {k: node.get(k) for k in CORRELATION_KEYS if node.get(k)},
                     "extra": extra or {}})

    for e in sources.get("cloudtrail", []):
        add(e.get("ts"), "cloudtrail", "api-call",
            "%s:%s %s" % (e.get("event_source", "?"), e.get("event_name", "?"), e.get("target", "")),
            e, {"principal": e.get("principal")})
    for a in sources.get("aegis", []):
        add(a.get("ts"), "aegis", "tool-audit", "aegis.call %s" % a.get("tool", "?"), a,
            {"args_sha256": a.get("args_sha256")})
    for m in sources.get("model_log", []):
        add(m.get("ts"), "bedrock-model-log", "model-invocation", "model invocation %s" % m.get("request_id", ""), m)
    for w in sources.get("worm", []):
        add(w.get("ts"), "worm", "evidence", "WORM evidence %s" % w.get("key", ""), w)
    for s in sources.get("sfn", []):
        add(s.get("ts"), "sfn", "state", "%s %s" % (s.get("type", ""), s.get("name", "")), s)
    for g in sources.get("gateway", []):
        add(g.get("ts"), "gateway", "mcp-request", "gateway request", g)

    rows.sort(key=lambda r: r["ts"])
    return rows


def verdict_markdown(case_id, tenant, lineage, verdict):
    lines = ["# Lineage coverage proof - case %s (tenant %s)" % (case_id, tenant), "",
             "**Coverage: %s**" % ("PASS - every governed API call is captured and correlated"
                                   if verdict["covered"] else "FAIL - orphan(s) found"), ""]
    c = verdict["counts"]
    lines.append("Captured: %d CloudTrail Lambda invokes, %d aegis.call audit lines, %d WORM records, "
                 "%d model invocations, %d SFN events, %d gateway requests."
                 % (c["cloudtrail_lambda_invokes"], c["aegis_calls"], c["worm_records"],
                    c["model_invocations"], c["sfn_events"], c["gateway_requests"]))
    lines.append("")
    lines.append("Per-tool invoke/audit parity: " + ", ".join(
        "%s=%d/%d" % (t, v["cloudtrail_invokes"], v["aegis_calls"]) for t, v in verdict["per_tool"].items()))
    if verdict["orphans"]:
        lines += ["", "## Orphans", ""]
        for o in verdict["orphans"]:
            lines.append("- " + json.dumps(o))
    lines += ["", "## Joined lineage (%d nodes)" % len(lineage), ""]
    for r in lineage:
        lines.append("- %d  %-16s  %s  %s" % (r["ts"], r["source"], r["summary"], json.dumps(r["correlation"])))
    return "\n".join(lines) + "\n"


# ============================ LIVE wiring (AWS) ==================================================

def _insights(logs, groups, query, start, end, limit=2000):
    qid = logs.start_query(logGroupNames=groups, startTime=int(start // 1000), endTime=int(end // 1000),
                           queryString=query, limit=limit)["queryId"]
    while True:
        r = logs.get_query_results(queryId=qid)
        if r["status"] in ("Complete", "Failed", "Cancelled"):
            break
        time.sleep(1)
    out = []
    for row in r.get("results", []):
        out.append({c["field"]: c["value"] for c in row})
    return out


def _iso_ms(ts):
    if not ts:
        return 0
    try:
        import datetime
        return int(datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp() * 1000)
    except Exception:
        return 0


def read_cloudtrail_capture(logs, capture_log_group, prefix, start, end):
    """Read the account capture trail's CloudWatch Logs: every governed Lambda invoke, every S3 write
    to a pack bucket, and Step Functions control-plane calls in the window."""
    q = (r'fields @timestamp, eventSource, eventName, '
         r'requestParameters.functionName as fn, requestParameters.bucketName as bkt, '
         r'userIdentity.arn as who, requestParameters.stateMachineArn as sm '
         r'| filter (eventSource="lambda.amazonaws.com" and eventName like /Invoke/ and fn like /' + prefix + r'/) '
         r'or (eventSource="s3.amazonaws.com" and (eventName="PutObject" or eventName="CompleteMultipartUpload") and bkt like /' + prefix + r'/) '
         r'or (eventSource="states.amazonaws.com") '
         r'| sort @timestamp asc | limit 2000')
    rows = _insights(logs, [capture_log_group], q, start, end)
    out = []
    for r in rows:
        out.append({"ts": _iso_ms(r.get("@timestamp")), "event_source": r.get("eventSource", ""),
                    "event_name": r.get("eventName", ""),
                    "target": r.get("fn") or r.get("bkt") or r.get("sm") or "",
                    "principal": r.get("who", "")})
    return out


def main():
    import boto3
    import trace_case as tc

    ap = argparse.ArgumentParser()
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--tenant", default="default")
    ap.add_argument("--prefix", required=True, help="deployment prefix, e.g. ben-gate")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--capture-log-group", required=True)
    ap.add_argument("--ledger-table", required=True)
    ap.add_argument("--model-log-group", default="")
    ap.add_argument("--gateway-log-group", default="")
    ap.add_argument("--lambda-log-prefix", default="")
    ap.add_argument("--capture-worm-bucket", default="", help="write the coverage evidence under Object-Lock")
    ap.add_argument("--window-min", type=int, default=60)
    ap.add_argument("--tool-names", default="")
    args = ap.parse_args()

    end = int(time.time() * 1000)
    start = end - args.window_min * 60 * 1000

    logs = boto3.client("logs", region_name=args.region)
    ddb = boto3.resource("dynamodb", region_name=args.region)
    sfn = boto3.client("stepfunctions", region_name=args.region)

    # Seed correlation keys from the case's WORM rows (same seed trace_case uses).
    worm_rows = tc.read_worm_rows(ddb, args.ledger_table, args.case_id)
    keys = tc.join_keys(worm_rows)
    session_ids = list(keys.get("session_id", []))
    exec_arns = list(keys.get("execution_arn", []))

    lambda_groups = []
    if args.lambda_log_prefix:
        try:
            paginator = logs.get_paginator("describe_log_groups")
            for pg in paginator.paginate(logGroupNamePrefix=args.lambda_log_prefix):
                lambda_groups += [g["logGroupName"] for g in pg["logGroups"]]
        except Exception:
            pass

    aegis = tc.read_lambda_calls(logs, lambda_groups, args.case_id, keys, start, end) if lambda_groups else []
    model = tc.read_model_rows(logs, args.model_log_group, args.case_id, session_ids, start, end) if args.model_log_group else []
    sfn_events = tc.read_sfn(sfn, exec_arns) if exec_arns else []
    gateway = tc.read_gateway_rows(logs, args.gateway_log_group, session_ids, list(keys.get("mcp_session_id", [])),
                                   list(keys.get("trace_id", [])), start, end) if args.gateway_log_group else []
    cloudtrail = read_cloudtrail_capture(logs, args.capture_log_group, args.prefix, start, end)

    def _corr(node, extra):
        node = dict(node or {})
        node.update(extra)
        return node

    sources = {
        "cloudtrail": cloudtrail,
        "aegis": [_corr(a.get("keys", {}), {"tool": a.get("tool"), "ts": a.get("ts"), "args_sha256": a.get("args_sha256")})
                  for a in aegis],
        "model_log": [_corr(m.get("keys", {}), {"ts": m.get("ts"), "request_id": (m.get("keys") or {}).get("request_id")})
                      for m in model],
        "worm": [{"ts": int(r.get("recorded_at", 0)) * 1000, "key": r.get("_key"),
                  **{k: (r.get("correlation") or {}).get(k) for k in CORRELATION_KEYS if (r.get("correlation") or {}).get(k)},
                  "case_id": r.get("case_id", args.case_id)} for r in worm_rows],
        "sfn": [{"ts": _iso_ms(e.get("timestamp")), "type": e.get("type"), "name": e.get("name"),
                 "execution_arn": e.get("execution_arn")} for e in sfn_events],
        "gateway": [_corr(g.get("keys", {}), {"ts": g.get("ts")}) for g in gateway],
    }

    tool_names = [t for t in args.tool_names.split(",") if t] or [
        "mask_pii", "assess_eligibility", "redetermine", "overpayment", "draft_award_notice",
        "verify_income", "ingest_case", "request_signoff", "signoff_register", "approve_signoff",
        "finalize_signoff", "write_audit"]

    verdict = assess_coverage(sources, tool_names)
    lineage = build_lineage(sources)
    md = verdict_markdown(args.case_id, args.tenant, lineage, verdict)
    print(md)
    print(json.dumps({"covered": verdict["covered"], "counts": verdict["counts"],
                      "orphans": verdict["orphans"]}, indent=2))

    if args.capture_worm_bucket:
        try:
            body = json.dumps({"case_id": args.case_id, "tenant": args.tenant, "verdict": verdict,
                               "lineage": lineage, "generated_at": end}, default=str).encode("utf-8")
            boto3.client("s3", region_name=args.region).put_object(
                Bucket=args.capture_worm_bucket,
                Key="lineage-coverage/%s/%s-%d.json" % (args.tenant, args.case_id, end),
                Body=body, ContentType="application/json")
            print("wrote coverage evidence to Object-Lock bucket %s" % args.capture_worm_bucket)
        except Exception as exc:
            print("WARN could not write coverage evidence to WORM bucket: %s" % type(exc).__name__)

    return 0 if verdict["covered"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
