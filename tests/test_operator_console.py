"""The Day-2 operator console's renderer is a PURE function of a state dict — unit-tested offline (no
AWS). Verifies the four panels render, empty state is handled, and untrusted values are HTML-escaped."""
import sys
import pathlib

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import operator_console as oc  # noqa: E402


def _state(**kw):
    base = {"env": "demo", "region": "us-east-1", "generated_at": 1788600000,
            "kill_switch": {"engaged": False}, "budgets": [], "approvals": [], "cases": []}
    base.update(kw)
    return base


def test_renders_all_panels_and_is_self_contained():
    html = oc.render_console(_state(
        kill_switch={"engaged": True, "actor": "arn:aws:iam::111122223333:user/ops", "source": "manual"},
        budgets=[{"tenant": "pha-a", "used_tokens": 9000, "cap_tokens": 10000, "pct_tokens": 90.0, "usd": 1.23}],
        approvals=[{"case_id": "C-1", "requester": "alice", "status": "PENDING", "action": "finalize"}],
        cases=[{"case_id": "C-1", "phase": "COMMITTED", "actor": "bob", "seq": 3}]))
    # self-contained: no external resource references
    assert "<style>" in html and "http://" not in html and "https://" not in html.replace("https://ben", "")
    # containment panel reflects the engaged kill switch
    assert "ENGAGED" in html and "Containment" in html
    # budget burn panel shows the tenant + a burn bar
    assert "pha-a" in html and "90" in html and "class='bar'" in html
    # approvals + lineage panels
    assert "alice" in html and "PENDING" in html
    assert "COMMITTED" in html and "bob" in html


def test_empty_state_renders_placeholders_not_errors():
    html = oc.render_console(_state())
    assert "DISENGAGED" in html
    assert html.count("empty") >= 3            # budgets / approvals / cases all show an empty placeholder
    assert "<table" not in html or "No " in html


def test_untrusted_values_are_escaped():
    html = oc.render_console(_state(
        approvals=[{"case_id": "<script>alert(1)</script>", "requester": "x", "status": "PENDING", "action": ""}]))
    assert "<script>alert(1)</script>" not in html      # the raw tag must be escaped
    assert "&lt;script&gt;" in html
