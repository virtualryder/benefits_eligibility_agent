import json

# assess_eligibility — deterministic income-based benefits eligibility + processing-clock determination.
# NO licensed data and NO model call: a rules engine over PUBLIC Federal Poverty Guidelines and the
# SNAP-style gross-income and expedited-service tests. Runs AFTER mask_pii (fail-closed: refuses
# un-masked input, mirroring the PV mask-before-model control). The specific thresholds and program
# rules are a per-program/per-state CONFIGURATION item (customer engagement) — these are the widely
# used federal defaults and are labeled illustrative.
#
# Federal Poverty Guidelines (illustrative, 48 contiguous states): 1-person ~$15,650/yr, +$5,500 per
# additional person. SNAP gross-income limit = 130% FPL; expedited service = very low income + minimal
# liquid resources -> 7-day clock (vs. 30-day standard). Confirm current figures for the intended year.

FPL_BASE = 15650      # annual, 1-person household (illustrative)
FPL_PER_ADD = 5500    # annual, each additional household member (illustrative)
GROSS_LIMIT_PCT = 130 # SNAP gross monthly income limit as % of FPL
EXPEDITED_INCOME = 150     # expedited: gross monthly income under this ...
EXPEDITED_RESOURCES = 100  # ... AND liquid resources at/under this


def _coerce(e):
    e = e or {}
    if isinstance(e, str):
        try:
            e = json.loads(e)
        except Exception:
            e = {"_raw": e}
    return e


def _num(v, default=None):
    try:
        return float(v)
    except Exception:
        return default


def handler(event, context):
    e = _coerce(event)
    # Fail-closed: like PV draft/assess, refuse to operate on non-de-identified input. Cedar's
    # mask_before_assess forbid blocks this at the gateway; the body refuses too (defense in depth).
    if e.get("deidentified") is not True:
        return {"assessed": False, "error": "refused: case is not de-identified (deidentified must be true)",
                "deidentified_input": e.get("deidentified")}

    hh = e.get("household_size")
    try:
        hh = int(hh)
    except Exception:
        hh = None
    income = _num(e.get("monthly_income"))
    resources = _num(e.get("liquid_resources"), 0.0)
    categorical = bool(e.get("categorical_eligibility"))

    if not hh or hh < 1 or income is None:
        return {"assessed": True, "determination": "NEEDS_REVIEW", "eligible": None,
                "reason": "insufficient data (need household_size and monthly_income)",
                "deidentified_input": True, "assessed_by": "rules:FPL/SNAP-gross(illustrative)"}

    annual_fpl = FPL_BASE + (hh - 1) * FPL_PER_ADD
    monthly_fpl = annual_fpl / 12.0
    gross_limit = (GROSS_LIMIT_PCT / 100.0) * monthly_fpl
    income_pct_fpl = round(income / monthly_fpl * 100.0, 1) if monthly_fpl else None

    if categorical:
        determination, eligible, reason = "ELIGIBLE", True, "categorically eligible (receives TANF/SSI/GA)"
    elif income <= gross_limit:
        determination, eligible, reason = "ELIGIBLE", True, ("gross monthly income %.0f is within the %d%% FPL limit (%.0f)" % (income, GROSS_LIMIT_PCT, gross_limit))
    else:
        determination, eligible, reason = "INELIGIBLE", False, ("gross monthly income %.0f exceeds the %d%% FPL limit (%.0f)" % (income, GROSS_LIMIT_PCT, gross_limit))

    expedited = (income < EXPEDITED_INCOME and resources <= EXPEDITED_RESOURCES)
    processing = "EXPEDITED" if expedited else "STANDARD"
    processing_days = 7 if expedited else 30

    notes = ["FPL and thresholds are illustrative federal defaults; configure per program/state/year"]
    if determination == "ELIGIBLE" and not categorical:
        notes.append("gross-income test only; net-income test and verification remain for caseworker review")

    # Short proof fields FIRST (the MCP client truncates long results ~200 chars); detail LAST.
    return {
        "assessed": True,
        "determination": determination,           # ELIGIBLE | INELIGIBLE | NEEDS_REVIEW
        "eligible": eligible,
        "processing_clock": processing,            # EXPEDITED | STANDARD
        "processing_days": processing_days,        # 7 expedited / 30 standard
        "income_pct_fpl": income_pct_fpl,
        "household_size": hh,
        "deidentified_input": True,
        "assessed_by": "rules:FPL/SNAP-gross(illustrative)",
        "reason": reason,
        "notes": notes,
    }
