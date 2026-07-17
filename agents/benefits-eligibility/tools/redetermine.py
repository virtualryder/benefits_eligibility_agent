import json

# redetermine — changed-circumstances RE-DETERMINATION. Re-runs the deterministic eligibility rules on
# NEW facts and compares to the prior determination to classify the change. The governance point:
# an ADVERSE change (a reduction or termination of benefits) triggers constitutional due process
# (Goldberg v. Kelly) — the household must get TIMELY, ADEQUATE ADVANCE NOTICE and a fair-hearing right
# BEFORE the adverse action takes effect. This tool flags that requirement; it never commits the change
# (the human sign-off gate owns the commit, and an adverse commit must carry the advance notice).
#
# Fail-closed: refuses non-de-identified input (mirrors mask_before_assess). Uses the same authoritative
# 2026 HHS poverty guidelines as assess_eligibility.

FPL_BASE = 15960      # 2026 HHS, 1-person, 48 states + DC (authoritative)
FPL_PER_ADD = 5680    # 2026 HHS, each additional member
GROSS_LIMIT_PCT = 130 # SNAP gross monthly income limit (7 CFR 273.9)


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


def _eligible(hh, income, categorical):
    if categorical:
        return True, "categorically eligible"
    annual_fpl = FPL_BASE + (hh - 1) * FPL_PER_ADD
    gross_limit = (GROSS_LIMIT_PCT / 100.0) * (annual_fpl / 12.0)
    if income <= gross_limit:
        return True, "within 130%% FPL (%.0f)" % gross_limit
    return False, "exceeds 130%% FPL (%.0f)" % gross_limit


def handler(event, context):
    e = _coerce(event)
    if e.get("deidentified") is not True:
        return {"redetermined": False, "error": "refused: case is not de-identified (deidentified must be true)",
                "deidentified_input": e.get("deidentified")}

    hh = e.get("household_size")
    try:
        hh = int(hh)
    except Exception:
        hh = None
    income = _num(e.get("monthly_income"))
    categorical = bool(e.get("categorical_eligibility"))
    # prior state: accept an explicit prior_eligible, or infer from a prior_determination string
    prior_eligible = e.get("prior_eligible")
    if prior_eligible is None:
        pd = str(e.get("prior_determination", "")).upper()
        if "INELIGIBLE" in pd:
            prior_eligible = False
        elif "ELIGIBLE" in pd:
            prior_eligible = True

    if not hh or hh < 1 or income is None or prior_eligible is None:
        return {"redetermined": True, "change_type": "NEEDS_REVIEW", "advance_notice_required": None,
                "reason": "insufficient data (need household_size, monthly_income, and the prior determination)",
                "deidentified_input": True}

    new_eligible, why = _eligible(hh, income, categorical)

    if prior_eligible and not new_eligible:
        change_type = "ADVERSE"          # termination — reduces/ends benefits
    elif (not prior_eligible) and new_eligible:
        change_type = "FAVORABLE"        # newly eligible
    else:
        change_type = "NO_CHANGE"

    advance_notice_required = (change_type == "ADVERSE")
    due_process_note = (
        "ADVERSE action: due process (Goldberg v. Kelly) requires timely, adequate ADVANCE written notice "
        "and a fair-hearing right BEFORE the reduction/termination takes effect; the commit must go through "
        "the human sign-off gate carrying that notice." if advance_notice_required else
        "no adverse action; standard processing"
    )

    # Short proof fields FIRST (MCP client truncates ~200 chars).
    return {
        "redetermined": True,
        "change_type": change_type,                 # ADVERSE | FAVORABLE | NO_CHANGE
        "advance_notice_required": advance_notice_required,
        "prior_eligible": bool(prior_eligible),
        "new_eligible": bool(new_eligible),
        "deidentified_input": True,
        "redetermined_by": "rules:FPL/SNAP-gross(2026 authoritative)",
        "reason": why,
        "due_process_note": due_process_note,
    }
