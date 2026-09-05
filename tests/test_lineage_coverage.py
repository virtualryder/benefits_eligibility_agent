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
