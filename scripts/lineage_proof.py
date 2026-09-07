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
# L21 (CORRECTED, attempt 7): the #168 capture-all trail records Lambda invocations as DATA events,
# and a Lambda data event's eventName is "InvokeExecution" - NOT the management-plane "Invoke". The
# set below listed only the management names, so every governed invoke the trail captured was
# discarded and EVERY audited tool was reported as an orphan ("audited_not_invoked").
#
# Attempt 6 misdiagnosed this as CloudTrail delivery latency and added a settle window. The settle is
# kept (delivery lag is real and the wait is now recorded), but it was never the fix: attempt 7 waited
# and still saw zero, because no amount of waiting makes "InvokeExecution" match "Invoke". Proving the
# platform from zero twice is what separated the two explanations.
#
# Data events also put the full function ARN in requestParameters.functionName rather than a bare
# name; tool_of() canonicalizes and substring-matches, so the ARN still resolves to its tool.
_LAMBDA_INVOKE_EVENTS = {"Invoke", "InvokeFunction", "Invoke20150331", "InvokeAsync", "InvokeExecution"}


def _canon(s):
    return "".join(ch for ch in (s or "").lower() if ch.isalnum())


def tool_of(function_name, tool_names, prefix="ben-gate-", aliases=None):
    """Map a CloudTrail Lambda functionName to the aegis tool identity it hosts, tolerant of the
    deployment differences between the function name (ben-gate-mask-pii, ben-gate-finalize) and the
    aegis.call tool field (mask_pii, finalize_signoff): compare on the alphanumeric-only stem with
    bidirectional containment, longest match wins so 'signoff_register' is not shadowed by
    'request_signoff'. `aliases` maps a canonical function stem to an aegis tool for the cases with no
    lexical overlap (the multi-tool 'core-tools' Lambda hosts the 'benefits_core' drafter)."""
    raw = (function_name or "").split(":function:")[-1]  # ARN -> bare function name
    fn = _canon(raw)
    pf = _canon(prefix)
    stem = fn[len(pf):] if pf and fn.startswith(pf) else fn
    aliases = aliases or {}
    if stem in aliases and aliases[stem] in tool_names:
        return aliases[stem]
    # L21d (live-found, attempt 7): the exact match above only fires when `prefix` matched the actual
    # deployment prefix - and callers do not pass one, so it defaulted to a stale "ben-gate-" while
    # the real stem was "benfpcoretools". The alias silently never applied, and benefits_core (the
    # ONLY tool that needs an alias, because "core-tools" and "benefits_core" share no lexical stem)
    # was reported as an orphan on every run. Fall back to containment so the alias resolves under
    # any deployment prefix; the containment loop below cannot rescue this case by construction.
    for k, v in aliases.items():
        if k and k in stem and v in tool_names:
            return v
    best = None
    for t in tool_names:
        ct = _canon(t)
        if ct and (ct in stem or stem in ct):
            if best is None or len(ct) > len(_canon(best)):
                best = t
    return best


def assess_coverage(sources, tool_names, aliases=None):
    """The coverage assertion. `sources` is a dict of lists (cloudtrail, aegis, worm, model_log, sfn,
    gateway); see the fixtures in the offline test for the exact node shapes. Returns a verdict dict
    with covered:bool and the list of orphans."""
    orphans = []

    # --- A/B: per-tool parity between CloudTrail Lambda invokes and aegis.call audit lines ----------
    ct_invokes, aegis_calls = {}, {}
    for e in sources.get("cloudtrail", []):
        if e.get("event_source") == "lambda.amazonaws.com" and e.get("event_name") in _LAMBDA_INVOKE_EVENTS:
            t = tool_of(e.get("target", ""), tool_names, aliases=aliases)
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


def read_cloudtrail_capture(logs, capture_log_group, prefix, start, end, query_end=None):
    """CloudTrail delivers to CloudWatch Logs at DELIVERY time (minutes after the API call), so query a
    broad delivery window [start, query_end=now] but keep only events whose own eventTime falls in the
    semantic window [start, end] - the execution window. Returns governed Lambda invokes, S3 writes to
    pack buckets, and Step Functions calls."""
    import time as _t
    query_end = query_end or int(_t.time() * 1000)
    # ---- L34: eventID is the only safe identity for a CloudTrail event -----------------------------
    # This reader is built from four `like` predicates, and L33 proved Insights silently drops rows
    # for those. Attempt 18 showed the lineage failure move to this arm the moment the audit arm was
    # fixed: 11 audit lines against 10 invokes, `audited_not_invoked:assess_eligibility`.
    #
    # The first attempt at this fix made it WORSE - re-reading the window unfiltered and merging on
    # (eventTime, eventName, fn, bkt) took invokes from 10 to 21, because CloudTrail's eventTime has
    # one-second granularity (L21c) and several DISTINCT invokes legitimately share a second. Merging
    # on a non-unique key does not deduplicate, it fabricates. That was L21e's lesson - a change to
    # one arm of a two-sided comparison is not a fix - walked into twice in one session, and it is
    # why `eventID` is now selected: CloudTrail guarantees it unique per event, so a merge cannot
    # invent an invoke and cannot collapse two real ones.
    _FIELDS = (r'fields @timestamp, eventID, eventTime, eventSource, eventName, '
               r'requestParameters.functionName as fn, requestParameters.bucketName as bkt, '
               r'userIdentity.arn as who, requestParameters.stateMachineArn as sm ')
    _KEEP = (r'| filter (eventSource="lambda.amazonaws.com" and eventName like /Invoke/ and fn like /' + prefix + r'/) '
             r'or (eventSource="s3.amazonaws.com" and (eventName="PutObject" or eventName="CompleteMultipartUpload") and bkt like /' + prefix + r'/) '
             r'or (eventSource="states.amazonaws.com") ')
    q = _FIELDS + _KEEP + r'| sort @timestamp asc | limit 5000'
    rows = _insights(logs, [capture_log_group], q, start, max(end, query_end))
    # L21c (live-found, attempt 7): CloudTrail's eventTime has ONE-SECOND granularity, but the case
    # window is measured in milliseconds. The invoke that STARTS a case is recorded at the enclosing
    # second - 23:22:41.000 for a case whose window opens at 23:22:41.003 - so `start <= et` dropped
    # the very first governed invokes by three milliseconds, and intake_application /
    # ingest_application were reported as audited-but-never-invoked on every run.
    #
    # The window is widened to the RESOLUTION OF THE SOURCE, not by an arbitrary fudge: floor the
    # start to its second and ceil the end to its second, which is exactly the interval CloudTrail
    # could have stamped for an event inside the real window. Anything further out is still dropped.
    w_start = (start // 1000) * 1000
    w_end = -(-end // 1000) * 1000
    out, seen = [], set()
    for r in rows:
        eid = r.get("eventID") or ""
        if eid and eid in seen:
            continue          # L34: identity is eventID, never a timestamp tuple
        et = _iso_ms(r.get("eventTime"))
        if et and not (w_start <= et <= w_end):
            continue
        if eid:
            seen.add(eid)
        out.append({"ts": et or _iso_ms(r.get("@timestamp")), "event_id": eid,
                    "event_source": r.get("eventSource", ""),
                    "event_name": r.get("eventName", ""),
                    "target": r.get("fn") or r.get("bkt") or r.get("sm") or "",
                    "principal": r.get("who", "")})
    return out


def verify_cloudtrail_capture(logs, capture_log_group, prefix, start, end, known, query_end=None):
    """L34: re-read the SAME window with no predicates and merge anything the filtered query missed.

    Called only when the filtered read would otherwise produce an orphan, because the unfiltered scan
    is expensive - the expensive read happens when the answer would otherwise be an accusation. The
    merge is keyed on eventID, so a recovered row can never double-count an invoke already counted.
    """
    import time as _t
    query_end = query_end or int(_t.time() * 1000)
    raw = _insights(logs, [capture_log_group], _cloudtrail_fields() + r'| sort @timestamp asc | limit 10000',
                    start, max(end, query_end), 10000)
    w_start = (start // 1000) * 1000
    w_end = -(-end // 1000) * 1000
    seen = {r.get("event_id") for r in known if r.get("event_id")}
    added = []
    for r in raw:
        eid = r.get("eventID") or ""
        if not eid or eid in seen:
            continue
        src, name = (r.get("eventSource") or ""), (r.get("eventName") or "")
        fn, bkt = (r.get("fn") or ""), (r.get("bkt") or "")
        keep = ((src == "lambda.amazonaws.com" and "Invoke" in name and prefix in fn)
                or (src == "s3.amazonaws.com" and name in ("PutObject", "CompleteMultipartUpload")
                    and prefix in bkt)
                or src == "states.amazonaws.com")
        if not keep:
            continue
        et = _iso_ms(r.get("eventTime"))
        if et and not (w_start <= et <= w_end):
            continue
        seen.add(eid)
        added.append({"ts": et or _iso_ms(r.get("@timestamp")), "event_id": eid,
                      "event_source": src, "event_name": name,
                      "target": fn or bkt or (r.get("sm") or ""), "principal": r.get("who", "")})
    return known + added, len(added)


def _cloudtrail_fields():
    return (r'fields @timestamp, eventID, eventTime, eventSource, eventName, '
            r'requestParameters.functionName as fn, requestParameters.bucketName as bkt, '
            r'userIdentity.arn as who, requestParameters.stateMachineArn as sm ')


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
    # L21: CloudTrail -> CloudWatch Logs delivery lags the recorded API call, and lags most on a
    # freshly created trail. Wait for the capture to arrive rather than reading an empty group.
    ap.add_argument("--settle-max-sec", type=int, default=900,
                    help="max seconds to wait for CloudTrail/model/gateway log delivery (0 = read once)")
    ap.add_argument("--settle-poll-sec", type=int, default=30)
    ap.add_argument("--start-ms", type=int, default=0)
    ap.add_argument("--end-ms", type=int, default=0)
    ap.add_argument("--tool-names", default="")
    args = ap.parse_args()

    end = args.end_ms or int(time.time() * 1000)
    start = args.start_ms or (end - args.window_min * 60 * 1000)

    # ---- L21e SYMMETRIC WINDOW (live-found, attempt 10; caused by the L21c fix itself) ------------
    # A PARITY assertion has to compare like with like. L21c widened only the CLOUDTRAIL window to
    # CloudTrail's one-second resolution, and left the aegis/model/gateway reads on the exact
    # millisecond window. The two sides then covered different intervals: the case-opening
    # ingest_application invoke at :41.000 was now inside the CloudTrail window while its aegis.call
    # audit line stayed outside the audit window, so an "audited_not_invoked" orphan simply flipped
    # into an "invoked_not_audited" one - the scarier direction, a governed tool appearing to run
    # unaudited, produced by nothing but a window mismatch.
    #
    # The window is widened ONCE, here, to the coarsest resolution any source records at (one
    # second), and every source is read over that same interval. Both sides move together or the
    # comparison means nothing.
    start = (start // 1000) * 1000
    end = -(-end // 1000) * 1000

    logs = boto3.client("logs", region_name=args.region)
    ddb = boto3.client("dynamodb", region_name=args.region)
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

    sfn_events = tc.read_sfn(sfn, exec_arns) if exec_arns else []

    # ---- L21 SETTLE (corrected twice; the correction matters more than the fix) -------------------
    # The three sources below arrive through LOG DELIVERY, not a direct API read, so they lag the run
    # and must be waited for. Two earlier readings of this were wrong, and the record is kept because
    # each wrong turn is the kind a reviewer should be able to audit:
    #
    #   attempt 6  read them ONCE and saw nothing -> "CloudTrail delivery lags"; a settle was added.
    #   attempt 7  waited 173s, declared delivery complete, and STILL counted 0 governed invokes.
    #
    # The settle was real but its READINESS CONDITION was wrong: it waited for "any Lambda invoke in
    # the window", and the tenant interceptor fires constantly (105 invokes in this run), so the very
    # first poll almost always looked "delivered" while the GOVERNED TOOLS' invokes had not arrived.
    # It waited for the wrong evidence.
    #
    # The condition is now the claim itself: wait until every tool with an aegis.call audit line has a
    # matching CloudTrail invoke - i.e. until the coverage assertion this proof exists to make can
    # actually be evaluated - or the deadline passes. An expired deadline is still a FAIL, and the
    # wait is recorded either way, so "we waited and nothing arrived" stays distinguishable from
    # "we did not wait".
    # L21g (live-found, attempt 11): the AUDIT side lags too, and it was read only ONCE.
    # aegis.call lines reach CloudWatch Logs - and become queryable by Insights - after the tool
    # returns, so the LAST tool in a case (signoff_register here, its line verified present and
    # in-window on the 6.5s side of the boundary) had simply not been ingested when the single read
    # happened. The settle then waited 419 seconds refreshing only CloudTrail and never looked at
    # the audit side again, so it kept re-evaluating a stale audit set and reported the tool as
    # invoked-but-never-audited: the alarming direction, from an ingestion race.
    #
    # Everything that arrives through CloudWatch Logs is subject to ingestion lag, so EVERY lagging
    # source is re-read on every poll - audit lines included. Step Functions history is read once
    # because it comes from a direct API, not log delivery.
    def _read_lagging():
        a = tc.read_lambda_calls(logs, lambda_groups, args.case_id, keys, start, end) if lambda_groups else []
        m = tc.read_model_rows(logs, args.model_log_group, args.case_id, session_ids, start, end) if args.model_log_group else []
        g = tc.read_gateway_rows(logs, args.gateway_log_group, session_ids, list(keys.get("mcp_session_id", [])),
                                 list(keys.get("trace_id", [])), start, end) if args.gateway_log_group else []
        ct = read_cloudtrail_capture(logs, args.capture_log_group, args.prefix, start, end)
        return a, m, g, ct

    tool_names = [t for t in args.tool_names.split(",") if t] or [
        "mask_pii", "assess_eligibility", "redetermine", "detect_overpayment", "benefits_core",
        "ingest_application", "intake_application", "workflow_guards",
        "request_signoff", "signoff_register", "approve_signoff", "finalize_signoff", "write_audit"]
    # the multi-tool core-tools Lambda hosts the benefits_core drafter (no lexical overlap in the name)
    aliases = {"coretools": "benefits_core"}

    def _unsettled(aegis_rows, ct):
        """Tools whose two records do not yet agree - in EITHER direction.

        Waiting only on audited_not_invoked was half the picture: an invoke whose audit line has not
        been ingested yet looks exactly like a governed tool running unaudited. Both directions are
        ingestion races until the deadline; only after it are they findings."""
        probe = {"cloudtrail": ct,
                 "aegis": [{"tool": a.get("tool"), "ts": a.get("ts"), "case_id": args.case_id} for a in aegis_rows],
                 "worm": [], "model_log": [], "sfn": [], "gateway": []}
        v = assess_coverage(probe, tool_names, aliases=aliases)
        return sorted("%s:%s" % (o.get("type"), o.get("tool")) for o in v["orphans"]
                      if o.get("type") in ("audited_not_invoked", "invoked_not_audited"))

    settle = {"waited_sec": 0, "polls": 1, "max_sec": int(args.settle_max_sec),
              "reason": "CloudTrail -> CloudWatch Logs delivery lags the API call it records",
              "waits_for": "audit lines and CloudTrail invokes to agree in BOTH directions"}
    aegis, model, gateway, cloudtrail = _read_lagging()
    t_settle = time.time()
    missing = _unsettled(aegis, cloudtrail)
    while missing and time.time() - t_settle < int(args.settle_max_sec):
        time.sleep(max(1, int(args.settle_poll_sec)))
        settle["polls"] += 1
        aegis, model, gateway, cloudtrail = _read_lagging()
        missing = _unsettled(aegis, cloudtrail)
    # L34: the settle has run out and the CloudTrail arm is the one that looks short. Before that
    # becomes an accusation, re-read the SAME window with no predicates - the filtered query is built
    # from `like` terms and L33 proved those drop rows silently. Only reached when a tool would
    # otherwise be reported as audited-but-never-invoked, so the expensive scan is rare, and the
    # merge is keyed on eventID so it cannot fabricate an invoke.
    if any(m.startswith("audited_not_invoked:") for m in missing):
        cloudtrail, recovered = verify_cloudtrail_capture(
            logs, args.capture_log_group, args.prefix, start, end, cloudtrail)
        settle["cloudtrail_unfiltered_reread"] = {"recovered_events": recovered}
        if recovered:
            print("  cloudtrail: filtered query missed %d event(s); recovered by unfiltered "
                  "re-read (L34)" % recovered)
            missing = _unsettled(aegis, cloudtrail)

    settle["waited_sec"] = round(time.time() - t_settle, 1)
    settle["still_missing"] = missing
    settle["cloudtrail_delivered"] = not missing
    if missing:
        settle["note"] = ("these tool records still disagree after the full settle window - reported "
                          "as a coverage FAILURE, not waited away")
    print("settle: waited %ss over %s poll(s); delivered=%s; still_missing=%s"
          % (settle["waited_sec"], settle["polls"], settle["cloudtrail_delivered"], missing))

    def _corr(node, extra):
        node = dict(node or {})
        node.update(extra)
        return node

    sources = {
        "cloudtrail": cloudtrail,
        "aegis": [dict({k: a.get(k) for k in CORRELATION_KEYS if a.get(k)},
                       tool=a.get("tool"), ts=a.get("ts"), args_sha256=a.get("args_sha256"))
                  for a in aegis],
        "model_log": [dict({k: (m.get(k) or (m.get("requestMetadata") or {}).get(k)) for k in CORRELATION_KEYS
                            if (m.get(k) or (m.get("requestMetadata") or {}).get(k))},
                       ts=m.get("ts"), request_id=m.get("requestId"))
                      for m in model],
        "worm": [{"ts": int(r.get("recorded_at", 0)) * 1000, "key": r.get("_key"),
                  **{k: (r.get("correlation") or {}).get(k) for k in CORRELATION_KEYS if (r.get("correlation") or {}).get(k)},
                  "case_id": r.get("case_id", args.case_id)} for r in worm_rows],
        "sfn": [{"ts": _iso_ms(e.get("timestamp")), "type": e.get("type"), "name": e.get("name"),
                 "execution_arn": e.get("execution_arn")} for e in sfn_events],
        "gateway": [_corr(g.get("keys", {}), {"ts": g.get("ts")}) for g in gateway],
    }

    verdict = assess_coverage(sources, tool_names, aliases=aliases)
    lineage = build_lineage(sources)
    md = verdict_markdown(args.case_id, args.tenant, lineage, verdict)
    print(md)
    print(json.dumps({"covered": verdict["covered"], "counts": verdict["counts"],
                      "settle": settle, "orphans": verdict["orphans"]}, indent=2))

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
