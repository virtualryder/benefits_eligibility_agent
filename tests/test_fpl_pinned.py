"""P0-3 (benefits) — the Federal Poverty Guidelines are a PINNED, CITED authoritative constant, not a
runtime fetch, so there is no source-failure path that could be fabricated. This test guards that:
(1) the FPL constants have not silently drifted from the cited 2026 HHS values, and (2) assess_eligibility
does not overclaim — it labels the gross-income screen as a screen and leaves verification to a human,
rather than fabricating an authoritative income-verification result. No AWS."""
from toolkit import call, load


def test_fpl_constants_pinned_and_cited():
    mod = load("assess_eligibility")
    assert mod.FPL_YEAR == 2026, "FPL year drifted"
    assert mod.FPL_BASE == 15960 and mod.FPL_PER_ADD == 5680, "FPL constants drifted from 2026 HHS guidelines"
    assert "Federal Register" in mod.FPL_SOURCE and "7 CFR 273.9" in mod.FPL_SOURCE, "FPL citation missing"


def test_assess_does_not_overclaim_verification():
    # An ELIGIBLE gross-income screen must not claim the income was authoritatively verified; it must
    # flag that verification remains for a human (no fabricated authoritative determination on income).
    r = call("assess_eligibility", {"household_size": 3, "monthly_income": 2000, "deidentified": True})
    assert r["determination"] == "ELIGIBLE"
    joined = " ".join(r.get("notes", [])).lower()
    assert "verification" in joined and "review" in joined, "must flag that verification remains for review"
    assert "authoritative" in r.get("fpl_source", "").lower() or "hhs" in r.get("fpl_source", "").lower()


def test_assess_fail_closed_on_unmasked():
    r = call("assess_eligibility", {"household_size": 3, "monthly_income": 2000, "deidentified": False})
    assert r["assessed"] is False
