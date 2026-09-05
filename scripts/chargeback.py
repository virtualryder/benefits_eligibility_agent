#!/usr/bin/env python3
"""chargeback.py (#169) - platform-wide LLM token tracking + chargeback, reconciled to AUTHORITATIVE
AWS billing.

The per-tenant token/USD meter already exists: governed-core `budget.py` records, per tenant per month,
`tokens_in` / `tokens_out` / `usd_micro` in the deployment's `<prefix>-budgets` table, priced from a
VERSIONED price table (`price_version` stamped on every commit). Its own docstring is explicit that the
USD figure is an ESTIMATE and that "the financial truth is the AWS Cost and Usage Report."

This tool closes that gap. It:
  1. reads the budget table(s) across one or more deployments and aggregates per tenant for a period
     (the metered, price-table estimate - authoritative for TOKEN COUNTS, which come from the real
     Bedrock Converse usage the meter committed);
  2. pulls the ACTUAL Amazon Bedrock spend for the same period from authoritative AWS billing (Cost
     Explorer `ce:GetCostAndUsage`, UnblendedCost, SERVICE = Amazon Bedrock);
  3. RECONCILES the summed metered estimate against the actual billed spend - a variance and a
     reconciliation factor - and produces a per-tenant chargeback (estimated USD and a reconciled USD
     scaled so the tenant shares sum to the real bill).

Why per-tenant chargeback is metered-then-reconciled, not read straight from the bill: Amazon Bedrock
spend is NOT tagged per request, so Cost Explorer cannot split Bedrock cost by tenant. The authoritative
PER-TENANT quantity is the token usage the meter recorded from each real Converse; Cost Explorer is the
authoritative ACCOUNT total. Chargeback = per-tenant metered tokens priced, reconciled to the account
bill. This is stated in the report so no one mistakes the estimate for the bill.

The pricing / aggregation / reconciliation logic is pure and unit-tested offline
(tests/test_chargeback.py); main() wires the live budget tables + Cost Explorer.
"""
import argparse
import json
import sys
import pathlib

# Reuse the meter's EXACT pricing so a chargeback USD can never diverge from what the meter committed.
import governed_core  # noqa: E402
sys.path.insert(0, str(governed_core.controls_dir()))
import budget  # noqa: E402  (governed_core.controls.budget - usd_micro / prices / MICRO / period)

MICRO = budget.MICRO


def price_micro(tokens_in, tokens_out, model_id, prices=None):
    """Micro-dollars for a token count under the pinned price table - the meter's own function."""
    return budget.usd_micro(model_id, {"inputTokens": tokens_in, "outputTokens": tokens_out}, prices)[0]


def aggregate(rows):
    """Aggregate budget rows (each: tenant, tokens_in, tokens_out, usd_micro) into per-tenant totals.
    Token counts come straight from the meter (real Converse usage); usd_micro is the meter's stored
    estimate at its own price_version."""
    out = {}
    for r in rows:
        t = r.get("tenant") or "default"
        a = out.setdefault(t, {"tokens_in": 0, "tokens_out": 0, "tokens": 0, "usd_micro": 0})
        ti = int(r.get("tokens_in", 0) or 0)
        to = int(r.get("tokens_out", 0) or 0)
        a["tokens_in"] += ti
        a["tokens_out"] += to
        a["tokens"] += int(r.get("tokens", ti + to) or (ti + to))
        a["usd_micro"] += int(r.get("usd_micro", 0) or 0)
    return out


def reconcile(metered_usd_micro_total, actual_bedrock_usd):
    """Reconcile the summed metered estimate against the authoritative account bill for the period.
    reconciliation_factor scales metered estimates so the tenant shares sum to the real bill; it is
    None when there is no metered spend to scale (avoid divide-by-zero)."""
    metered_usd = metered_usd_micro_total / MICRO
    actual = None if actual_bedrock_usd is None else float(actual_bedrock_usd)
    factor = None
    variance_usd = None
    variance_pct = None
    if actual is not None:
        variance_usd = round(actual - metered_usd, 6)
        if metered_usd > 0:
            factor = actual / metered_usd
            variance_pct = round((actual - metered_usd) / metered_usd * 100, 2)
    return {"metered_usd": round(metered_usd, 6), "actual_bedrock_usd": actual,
            "variance_usd": variance_usd, "variance_pct": variance_pct,
            "reconciliation_factor": factor}


def build_report(per_tenant, actual_bedrock_usd, price_version, period_label, deployments=None):
    """Assemble the chargeback report: per-tenant tokens + estimated USD + reconciled USD (scaled to the
    real bill when it is known), plus the account-level reconciliation."""
    metered_total_micro = sum(a["usd_micro"] for a in per_tenant.values())
    rec = reconcile(metered_total_micro, actual_bedrock_usd)
    factor = rec["reconciliation_factor"]
    tenants = []
    for t in sorted(per_tenant):
        a = per_tenant[t]
        est_usd = a["usd_micro"] / MICRO
        reconciled = round(est_usd * factor, 6) if factor is not None else None
        share = round(a["usd_micro"] / metered_total_micro * 100, 2) if metered_total_micro else 0.0
        tenants.append({"tenant": t, "tokens_in": a["tokens_in"], "tokens_out": a["tokens_out"],
                        "tokens": a["tokens"], "estimated_usd": round(est_usd, 6),
                        "reconciled_usd": reconciled, "share_pct": share})
    return {"period": period_label, "price_version": price_version,
            "deployments": deployments or [], "reconciliation": rec, "tenants": tenants,
            "note": ("token counts are authoritative (metered from each real Bedrock Converse); per-tenant "
                     "USD is the metered estimate at the stamped price_version, reconciled to the actual "
                     "account Bedrock bill (Cost Explorer). Amazon Bedrock spend is not tagged per request, "
                     "so per-tenant figures are metered-then-reconciled, not read from the bill.")}


def report_markdown(rep):
    lines = ["# Token chargeback - %s" % rep["period"], "",
             "Price table: `%s`. Deployments: %s." % (rep["price_version"], ", ".join(rep["deployments"]) or "(all)"),
             ""]
    rc = rep["reconciliation"]
    lines.append("**Reconciliation to authoritative billing (Cost Explorer, Amazon Bedrock):** "
                 "metered estimate $%.4f vs actual $%s%s." % (
                     rc["metered_usd"],
                     "%.4f" % rc["actual_bedrock_usd"] if rc["actual_bedrock_usd"] is not None else "n/a",
                     "" if rc["variance_pct"] is None else " (variance %+.2f%%)" % rc["variance_pct"]))
    lines += ["", "| tenant | tokens in | tokens out | est USD | reconciled USD | share |",
              "|---|--:|--:|--:|--:|--:|"]
    for t in rep["tenants"]:
        lines.append("| %s | %d | %d | $%.4f | %s | %.1f%% |" % (
            t["tenant"], t["tokens_in"], t["tokens_out"], t["estimated_usd"],
            "$%.4f" % t["reconciled_usd"] if t["reconciled_usd"] is not None else "n/a", t["share_pct"]))
    lines += ["", "> " + rep["note"]]
    return "\n".join(lines) + "\n"


# ============================ LIVE wiring (AWS) ==================================================

def _month_bounds(period_label):
    """(start, end_exclusive) ISO dates for a YYYY-MM period - Cost Explorer's TimePeriod.End is exclusive."""
    y, m = (int(x) for x in period_label.split("-"))
    start = "%04d-%02d-01" % (y, m)
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    return start, "%04d-%02d-01" % (ny, nm)


def read_budget_rows(ddb, table, period_label):
    """Scan a deployment's `<prefix>-budgets` table for the period. budget_key = '<tenant>#<YYYY-MM>'."""
    rows, kw = [], {"TableName": table}
    suffix = "#" + period_label
    while True:
        r = ddb.scan(**kw)
        for it in r.get("Items", []):
            bk = (it.get("budget_key") or {}).get("S", "")
            if not bk.endswith(suffix):
                continue
            rows.append({
                "tenant": bk[: -len(suffix)] or "default",
                "tokens_in": int((it.get("tokens_in") or {}).get("N", 0) or 0),
                "tokens_out": int((it.get("tokens_out") or {}).get("N", 0) or 0),
                "tokens": int((it.get("used") or {}).get("N", 0) or 0),
                "usd_micro": int((it.get("usd_micro") or {}).get("N", 0) or 0),
                "price_version": (it.get("price_version") or {}).get("S", ""),
                "_table": table})
        if "LastEvaluatedKey" in r:
            kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
        else:
            break
    return rows


# Anthropic models on Bedrock bill under a MARKETPLACE service label ("Claude Sonnet 4.5 (Amazon
# Bedrock Edition)"), NOT under "Amazon Bedrock" - a SERVICE=Amazon Bedrock filter misses the model
# spend entirely. So group by SERVICE and sum every line whose name mentions Bedrock.
BEDROCK_MATCH = ("bedrock",)


def actual_bedrock_usd(ce, period_label, match=BEDROCK_MATCH):
    """Authoritative account Bedrock spend for the month from Cost Explorer (UnblendedCost), summed
    across ALL Bedrock-related service lines (base Bedrock + the per-model '(Amazon Bedrock Edition)'
    marketplace lines)."""
    start, end = _month_bounds(period_label)
    r = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end}, Granularity="MONTHLY", Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}])
    results = r.get("ResultsByTime") or []
    if not results:
        return 0.0
    total = 0.0
    for g in results[0].get("Groups", []):
        name = (g.get("Keys") or [""])[0].lower()
        if any(m in name for m in match):
            total += float(g["Metrics"]["UnblendedCost"]["Amount"])
    return round(total, 6)


def main():
    import boto3

    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", default="", help="comma-separated <prefix>-budgets table names")
    ap.add_argument("--prefixes", default="", help="comma-separated deployment prefixes (-> <prefix>-budgets)")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--period", default=budget.period(), help="YYYY-MM (default: current month, UTC)")
    ap.add_argument("--no-billing", action="store_true", help="skip Cost Explorer (metered estimate only)")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    tables = [t.strip() for t in args.tables.split(",") if t.strip()]
    tables += ["%s-budgets" % p.strip() for p in args.prefixes.split(",") if p.strip()]
    if not tables:
        print("no budget tables given (use --tables or --prefixes)", file=sys.stderr)
        return 2

    ddb = boto3.client("dynamodb", region_name=args.region)
    rows = []
    for t in tables:
        try:
            rows += read_budget_rows(ddb, t, args.period)
        except Exception as exc:
            print("WARN could not read %s: %s" % (t, type(exc).__name__), file=sys.stderr)

    actual = None
    if not args.no_billing:
        try:
            actual = actual_bedrock_usd(boto3.client("ce", region_name="us-east-1"), args.period)
        except Exception as exc:
            print("WARN Cost Explorer unavailable (%s); reporting metered estimate only" % type(exc).__name__,
                  file=sys.stderr)

    per_tenant = aggregate(rows)
    price_version = next((r.get("price_version") for r in rows if r.get("price_version")), budget.prices().get("price_version", ""))
    rep = build_report(per_tenant, actual, price_version, args.period, deployments=tables)

    md = report_markdown(rep)
    print(md)
    print(json.dumps(rep, indent=2))
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(rep, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
