"""#169 - token tracking + chargeback reconciled to authoritative AWS billing, tested offline.

The pricing / aggregation / reconciliation logic is pure; these tests pin it (including the
divide-by-zero and no-billing edges and the December -> January month boundary) so a chargeback USD
can never silently diverge from the meter's own pricing or misstate the reconciliation to the bill.
"""
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import chargeback as cb  # noqa: E402
import budget  # noqa: E402  (on path via chargeback's governed_core import)

MICRO = cb.MICRO


def test_pricing_matches_the_meter():
    # chargeback prices through the meter's own usd_micro, so they must be identical.
    for ti, to, mid in [(1000, 500, "anthropic.claude-sonnet-4-5"),
                        (12345, 6789, "anthropic.claude-haiku-4-5"),
                        (10, 0, "anthropic.claude-sonnet-4-5")]:
        assert cb.price_micro(ti, to, mid) == budget.usd_micro(mid, {"inputTokens": ti, "outputTokens": to})[0]


def test_aggregate_sums_per_tenant_across_rows():
    rows = [
        {"tenant": "sp-a", "tokens_in": 1000, "tokens_out": 500, "usd_micro": 10500},
        {"tenant": "sp-a", "tokens_in": 2000, "tokens_out": 0, "usd_micro": 6000},   # another month
        {"tenant": "sp-b", "tokens_in": 500, "tokens_out": 500, "usd_micro": 9000},
    ]
    agg = cb.aggregate(rows)
    assert agg["sp-a"]["tokens_in"] == 3000 and agg["sp-a"]["tokens_out"] == 500
    assert agg["sp-a"]["usd_micro"] == 16500
    assert agg["sp-b"]["tokens"] == 1000  # default tokens = in+out when 'tokens' absent


def test_reconcile_variance_and_factor():
    r = cb.reconcile(10 * MICRO, 12.0)
    assert r["metered_usd"] == 10.0 and r["actual_bedrock_usd"] == 12.0
    assert r["variance_usd"] == 2.0 and r["variance_pct"] == 20.0
    assert abs(r["reconciliation_factor"] - 1.2) < 1e-9


def test_reconcile_handles_zero_metered_and_no_billing():
    z = cb.reconcile(0, 5.0)          # nothing metered -> no factor (no divide-by-zero)
    assert z["reconciliation_factor"] is None and z["variance_pct"] is None
    nb = cb.reconcile(10 * MICRO, None)  # billing unavailable -> estimate only
    assert nb["actual_bedrock_usd"] is None and nb["reconciliation_factor"] is None


def test_report_shares_sum_and_reconciled_matches_bill():
    per_tenant = cb.aggregate([
        {"tenant": "sp-a", "tokens_in": 1000, "tokens_out": 500, "usd_micro": 10 * MICRO},
        {"tenant": "sp-b", "tokens_in": 500, "tokens_out": 500, "usd_micro": 30 * MICRO},
    ])
    rep = cb.build_report(per_tenant, actual_bedrock_usd=60.0, price_version="pv-test",
                          period_label="2026-09", deployments=["ben-gate-budgets"])
    shares = sum(t["share_pct"] for t in rep["tenants"])
    assert abs(shares - 100.0) < 0.1
    # metered total is $40, actual $60 -> factor 1.5 -> reconciled shares sum to the real bill
    reconciled = sum(t["reconciled_usd"] for t in rep["tenants"])
    assert abs(reconciled - 60.0) < 1e-6
    assert rep["price_version"] == "pv-test"
    assert "not tagged per request" in rep["note"]  # the honesty caveat is present


def test_report_without_billing_leaves_reconciled_null():
    per_tenant = cb.aggregate([{"tenant": "sp-a", "tokens_in": 1, "tokens_out": 1, "usd_micro": MICRO}])
    rep = cb.build_report(per_tenant, actual_bedrock_usd=None, price_version="pv", period_label="2026-09")
    assert rep["tenants"][0]["reconciled_usd"] is None
    assert rep["reconciliation"]["actual_bedrock_usd"] is None
    md = cb.report_markdown(rep)
    assert "Token chargeback" in md and "n/a" in md


def test_month_bounds_including_year_rollover():
    assert cb._month_bounds("2026-09") == ("2026-09-01", "2026-10-01")
    assert cb._month_bounds("2026-12") == ("2026-12-01", "2027-01-01")
