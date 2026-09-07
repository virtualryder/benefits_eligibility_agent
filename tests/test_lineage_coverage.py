"""#168 - the unified-lineage COVERAGE proof, tested offline.

The live scripts/lineage_proof.py joins the account capture trail, the per-Lambda aegis.call audit
lines, the Step Functions history, the Bedrock model-invocation log and the WORM ledger into one
lineage and asserts that NO governed API call is an orphan. These tests drive the pure join/coverage
functions with fixtures - including deliberately injected orphans - so the detector itself is proven,
not just the happy path. If assess_coverage stopped catching an orphan, that is the whole control
failing silently; that is what these tests exist to prevent.
"""
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import lineage_proof as lp  # noqa: E402

TOOLS = ["mask_pii", "assess_eligibility", "draft_award_notice", "finalize_signoff",
         "request_signoff", "signoff_register"]

TRACE = "6a99b48df6fc6e20d82d074efa877cbd"
SESSION = "sess-abc"
EXEC = "arn:aws:states:us-east-1:111122223333:execution:ben-gate-determination-workflow:CASE-1"
CASE = "CASE-1"


def _clean_sources():
    """One tenant-a execution where every governed tool invoked (CloudTrail) has a matching aegis.call
    line, and every governed node carries a correlation key."""
    corr = {"trace_id": TRACE, "session_id": SESSION, "execution_arn": EXEC, "case_id": CASE}
    ct = [{"ts": 100 + i, "event_source": "lambda.amazonaws.com", "event_name": "Invoke",
           "target": "ben-gate-%s" % t, "principal": "arn:aws:sts::111122223333:assumed-role/ben-gate-gw"}
          for i, t in enumerate(["mask_pii", "assess_eligibility", "draft_award_notice", "finalize_signoff"])]
    ct += [{"ts": 90, "event_source": "states.amazonaws.com", "event_name": "StartExecution",
            "target": EXEC, "principal": "arn:aws:sts::111122223333:assumed-role/ben-gate-caller"},
           {"ts": 130, "event_source": "s3.amazonaws.com", "event_name": "PutObject",
            "target": "ben-gate-sp-a-worm", "principal": "arn:aws:sts::111122223333:assumed-role/ben-gate-finalize"}]
    aegis = [dict(corr, tool=t, ts=100 + i, args_sha256="deadbeef%d" % i)
             for i, t in enumerate(["mask_pii", "assess_eligibility", "draft_award_notice", "finalize_signoff"])]
    worm = [dict(corr, ts=131, key="A1"), dict(corr, ts=132, key="A2")]
    model = [dict(corr, ts=120, request_id="req-1")]
    sfn = [{"ts": 90, "type": "ExecutionStarted", "name": "", "execution_arn": EXEC},
           {"ts": 140, "type": "ExecutionSucceeded", "name": "", "execution_arn": EXEC}]
    gateway = [dict(corr, ts=95)]
    return {"cloudtrail": ct, "aegis": aegis, "worm": worm, "model_log": model, "sfn": sfn, "gateway": gateway}


def test_tool_of_longest_match_wins():
    assert lp.tool_of("ben-gate-signoff_register", TOOLS) == "signoff_register"
    assert lp.tool_of("ben-gate-request_signoff", TOOLS) == "request_signoff"
    assert lp.tool_of("ben-gate-unrelated", TOOLS) is None


def test_clean_run_is_fully_covered():
    v = lp.assess_coverage(_clean_sources(), TOOLS)
    assert v["covered"] is True, v["orphans"]
    assert v["orphans"] == []
    # every governed tool: exactly one CloudTrail invoke and one aegis.call line
    for t, pair in v["per_tool"].items():
        assert pair["cloudtrail_invokes"] == pair["aegis_calls"] == 1


def test_lineage_is_one_ordered_timeline():
    lineage = lp.build_lineage(_clean_sources())
    # every governed source contributes and the whole thing is ordered by ts
    ts = [r["ts"] for r in lineage]
    assert ts == sorted(ts)
    sources = {r["source"] for r in lineage}
    assert {"cloudtrail", "aegis", "bedrock-model-log", "worm", "sfn", "gateway"} <= sources


def test_orphan_invoked_but_not_audited_is_caught():
    """A governed tool Lambda invoked (CloudTrail) with NO aegis.call line = a side effect the audit
    trail missed. Coverage MUST fail."""
    s = _clean_sources()
    s["cloudtrail"].append({"ts": 200, "event_source": "lambda.amazonaws.com", "event_name": "Invoke",
                            "target": "ben-gate-assess_eligibility", "principal": "arn:aws:sts::111122223333:assumed-role/rogue"})
    v = lp.assess_coverage(s, TOOLS)
    assert v["covered"] is False
    kinds = {(o["type"], o.get("tool")) for o in v["orphans"]}
    assert ("invoked_not_audited", "assess_eligibility") in kinds


def test_orphan_audited_but_not_invoked_is_caught():
    """An aegis.call line with NO captured CloudTrail invoke behind it = an audit record with no real
    API call. Coverage MUST fail."""
    s = _clean_sources()
    s["aegis"].append(dict(trace_id=TRACE, session_id=SESSION, execution_arn=EXEC, case_id=CASE,
                           tool="mask_pii", ts=205, args_sha256="x"))
    v = lp.assess_coverage(s, TOOLS)
    assert v["covered"] is False
    assert ("audited_not_invoked", "mask_pii") in {(o["type"], o.get("tool")) for o in v["orphans"]}


def test_orphan_uncorrelated_node_is_caught():
    """A governed node (here a WORM record) carrying NONE of the run's correlation keys cannot be tied
    into the lineage. Coverage MUST fail."""
    s = _clean_sources()
    s["worm"].append({"ts": 210, "key": "A3"})  # no trace/session/execution/case
    v = lp.assess_coverage(s, TOOLS)
    assert v["covered"] is False
    assert any(o["type"] == "uncorrelated" and o["source"] == "worm" for o in v["orphans"])


def test_markdown_renders_pass_and_fail():
    clean = _clean_sources()
    v = lp.assess_coverage(clean, TOOLS)
    md = lp.verdict_markdown(CASE, "sp-a", lp.build_lineage(clean), v)
    assert "Coverage: PASS" in md and "Joined lineage" in md
    bad = _clean_sources()
    bad["worm"].append({"ts": 210, "key": "A3"})
    vb = lp.assess_coverage(bad, TOOLS)
    assert "Coverage: FAIL" in lp.verdict_markdown(CASE, "sp-a", lp.build_lineage(bad), vb)


# -- L21 CORRECTED (attempt 7, 2026-09-06): Lambda DATA events say "InvokeExecution" ----------------
# The #168 capture-all trail records Lambda invocations as data events, whose eventName is
# "InvokeExecution", not the management-plane "Invoke". The invoke-event set listed only the
# management names, so every governed invoke the trail captured was discarded and EVERY audited tool
# was reported as an orphan. Attempt 6 misread this as CloudTrail delivery latency and added a settle
# window; attempt 7 waited the full window and still saw zero, because waiting cannot make
# "InvokeExecution" match "Invoke". This test is the guard that keeps the two explanations apart.

def test_lambda_data_event_invocations_count_as_invokes():
    """A data-plane InvokeExecution must count, and carry the ARN form of the function name."""
    arn = "arn:aws:lambda:us-east-1:111122223333:function:ben-x-mask-pii"
    sources = {
        "cloudtrail": [{"ts": 1000, "event_source": "lambda.amazonaws.com",
                        "event_name": "InvokeExecution", "target": arn, "principal": "p"}],
        "aegis": [{"tool": "mask_pii", "ts": 1000, "case_id": "C1"}],
        "worm": [], "model_log": [], "sfn": [], "gateway": [],
    }
    v = lp.assess_coverage(sources, ["mask_pii"])
    assert v["counts"]["cloudtrail_lambda_invokes"] == 1, v["counts"]
    assert v["orphans"] == [], v["orphans"]
    assert v["covered"] is True


def test_an_audited_tool_with_no_invoke_at_all_is_still_an_orphan():
    """The fix must not blanket-pass: with nothing in CloudTrail the orphan is still reported."""
    sources = {"cloudtrail": [], "aegis": [{"tool": "mask_pii", "ts": 1000, "case_id": "C1"}],
               "worm": [], "model_log": [], "sfn": [], "gateway": []}
    v = lp.assess_coverage(sources, ["mask_pii"])
    assert any(o["type"] == "audited_not_invoked" for o in v["orphans"])
    assert v["covered"] is False


# -- L21d: the alias must resolve under the REAL deployment prefix (attempt 7) ----------------------
# tool_of()'s exact-match alias lookup only fired when its `prefix` argument matched the deployment,
# and no caller passes one - it defaulted to a stale "ben-gate-" while the live stem was
# "benfpcoretools". benefits_core is the ONLY tool that needs an alias ("core-tools" and
# "benefits_core" share no lexical stem, so the containment fallback cannot rescue it), so it was
# reported as an orphan on every live run while the offline fixtures - which used the default prefix
# - passed.

def test_alias_resolves_regardless_of_deployment_prefix():
    arn = "arn:aws:lambda:us-east-1:111122223333:function:%s-core-tools"
    for prefix in ("ben-fp", "ben-gate", "pv-prod", "fa-x"):
        got = lp.tool_of(arn % prefix, ["benefits_core", "mask_pii"], aliases={"coretools": "benefits_core"})
        assert got == "benefits_core", (prefix, got)


def test_alias_does_not_fire_for_an_unrelated_function():
    got = lp.tool_of("arn:aws:lambda:us-east-1:111122223333:function:ben-fp-budget-breach",
                     ["benefits_core", "mask_pii"], aliases={"coretools": "benefits_core"})
    assert got is None, got


# -- L21e: the parity window must be SYMMETRIC (attempt 10) -----------------------------------------
# The L21c fix widened only the CloudTrail side to CloudTrail's one-second resolution and left the
# audit-line side on the exact millisecond window. The two sides then covered different intervals,
# and the case-opening invoke flipped from "audited_not_invoked" to "invoked_not_audited" - a
# governed tool appearing to run UNAUDITED, manufactured purely by a window mismatch. A parity
# assertion compares like with like or it means nothing.

def test_parity_is_symmetric_not_one_sided():
    """Same tool, one invoke and one audit line: parity holds and neither orphan type appears."""
    arn = "arn:aws:lambda:us-east-1:111122223333:function:ben-x-ingest-application"
    sources = {
        "cloudtrail": [{"ts": 1000, "event_source": "lambda.amazonaws.com",
                        "event_name": "InvokeExecution", "target": arn, "principal": "p"}],
        "aegis": [{"tool": "ingest_application", "ts": 1000, "case_id": "C1"}],
        "worm": [], "model_log": [], "sfn": [], "gateway": [],
    }
    v = lp.assess_coverage(sources, ["ingest_application"])
    assert v["orphans"] == [], v["orphans"]
    assert v["covered"] is True


def test_an_invoke_with_no_audit_line_is_still_caught():
    """The fix must not blunt the control: a genuinely unaudited invoke still fails."""
    arn = "arn:aws:lambda:us-east-1:111122223333:function:ben-x-ingest-application"
    sources = {
        "cloudtrail": [{"ts": 1000, "event_source": "lambda.amazonaws.com",
                        "event_name": "InvokeExecution", "target": arn, "principal": "p"}],
        "aegis": [], "worm": [], "model_log": [], "sfn": [], "gateway": [],
    }
    v = lp.assess_coverage(sources, ["ingest_application"])
    assert any(o["type"] == "invoked_not_audited" for o in v["orphans"]), v["orphans"]
    assert v["covered"] is False
