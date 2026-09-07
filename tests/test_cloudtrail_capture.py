"""L34: CloudTrail identity is eventID, and a recovery merge must never fabricate an invoke.

Attempt 18's lineage failure moved to the CloudTrail arm the moment the audit arm was fixed
(11 audit lines vs 10 invokes). The first fix re-read the window unfiltered and merged on
(eventTime, eventName, fn, bkt) — and took invokes from 10 to 21, because CloudTrail's eventTime has
ONE-SECOND granularity (L21c) and distinct invokes legitimately share a second. Merging on a
non-unique key does not deduplicate, it fabricates.

These tests pin the behaviour that replaced it, using synthetic rows shaped like the ones that
caused the damage — no AWS, no live gate cycle.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import lineage_proof as lp  # noqa: E402

PREFIX = "ben-fp"
T0 = 1788788790000          # inside any window used below
START, END = 1788788783602, 1788788821602


def _ev(eid, name="Invoke", fn="arn:aws:lambda:us-east-1:1234:function:ben-fp-write-audit",
        src="lambda.amazonaws.com", when="2026-09-07T13:46:31Z"):
    return {"eventID": eid, "eventTime": when, "eventSource": src, "eventName": name,
            "fn": fn, "bkt": "", "who": "arn:aws:sts::1234:assumed-role/r/s", "sm": ""}


class _Logs:
    """Returns `filtered` for the query carrying a filter, `raw` for the unfiltered one."""

    def __init__(self, filtered, raw):
        self.filtered, self.raw, self.queries = filtered, raw, []

    def start_query(self, **kw):
        self.queries.append(kw["queryString"])
        return {"queryId": "q%d" % len(self.queries)}

    def get_query_results(self, queryId):
        rows = self.raw if "| filter" not in self.queries[int(queryId[1:]) - 1] else self.filtered
        return {"status": "Complete",
                "results": [[{"field": k, "value": v} for k, v in r.items()] for r in rows]}


def test_two_distinct_invokes_in_the_same_second_are_both_kept():
    """The exact shape that made the first fix fabricate invokes."""
    same_second = [_ev("id-1"), _ev("id-2")]          # different events, identical eventTime
    logs = _Logs(same_second, same_second)
    rows = lp.read_cloudtrail_capture(logs, "/g", PREFIX, START, END, query_end=END)
    assert len(rows) == 2, rows
    assert {r["event_id"] for r in rows} == {"id-1", "id-2"}


def test_a_repeated_eventid_is_counted_once():
    dupes = [_ev("id-1"), _ev("id-1")]
    logs = _Logs(dupes, dupes)
    rows = lp.read_cloudtrail_capture(logs, "/g", PREFIX, START, END, query_end=END)
    assert [r["event_id"] for r in rows] == ["id-1"]


def test_verify_recovers_a_row_the_filtered_query_dropped():
    """L33's silent drop, seen from the CloudTrail side."""
    filtered = [_ev("id-1")]
    raw = [_ev("id-1"), _ev("id-2")]                  # the filtered query lost id-2
    logs = _Logs(filtered, raw)
    known = lp.read_cloudtrail_capture(logs, "/g", PREFIX, START, END, query_end=END)
    assert len(known) == 1
    merged, recovered = lp.verify_cloudtrail_capture(logs, "/g", PREFIX, START, END, known, query_end=END)
    assert recovered == 1
    assert {r["event_id"] for r in merged} == {"id-1", "id-2"}


def test_verify_never_double_counts_what_is_already_known():
    rows = [_ev("id-1"), _ev("id-2")]
    logs = _Logs(rows, rows)
    known = lp.read_cloudtrail_capture(logs, "/g", PREFIX, START, END, query_end=END)
    merged, recovered = lp.verify_cloudtrail_capture(logs, "/g", PREFIX, START, END, known, query_end=END)
    assert recovered == 0
    assert len(merged) == len(known) == 2


def test_verify_still_excludes_events_outside_the_window_and_other_prefixes():
    raw = [_ev("id-in"),
           _ev("id-late", when="2026-09-07T23:59:59Z"),
           _ev("id-other", fn="arn:aws:lambda:us-east-1:1234:function:someone-else-fn")]
    logs = _Logs([], raw)
    merged, recovered = lp.verify_cloudtrail_capture(logs, "/g", PREFIX, START, END, [], query_end=END)
    assert recovered == 1
    assert [r["event_id"] for r in merged] == ["id-in"]
