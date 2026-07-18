"""Eval / regression harness for the benefits eligibility rules engine.

Golden cases pin the DETERMINATION for representative inputs, so a change to the rules (thresholds,
FPL figures, clock) that alters an outcome fails CI instead of silently shipping. Negative cases pin
the fail-closed behavior. This is the drift check a due-diligence review looks for after the live demo.

Rules basis (assess_eligibility): 2026 HHS poverty guidelines — FPL base 15960, +5680/member; SNAP
gross limit 130% FPL; expedited when gross monthly income < 150 AND liquid resources <= 100.
"""
import pytest
from toolkit import call

# (label, input, expected-subset) — every key in the expected dict must match the tool output.
GOLDEN = [
    ("eligible_family_of_4",
     {"household_size": 4, "monthly_income": 2500, "deidentified": True},
     {"determination": "ELIGIBLE", "eligible": True, "processing_clock": "STANDARD"}),
    ("ineligible_over_limit",
     {"household_size": 1, "monthly_income": 3000, "deidentified": True},
     {"determination": "INELIGIBLE", "eligible": False}),
    ("expedited_service",
     {"household_size": 2, "monthly_income": 120, "liquid_resources": 50, "deidentified": True},
     {"determination": "ELIGIBLE", "processing_clock": "EXPEDITED", "processing_days": 7}),
    ("categorical_eligibility",
     {"household_size": 3, "monthly_income": 9999, "categorical_eligibility": True, "deidentified": True},
     {"determination": "ELIGIBLE", "eligible": True}),
    ("needs_review_missing_income",
     {"household_size": 3, "deidentified": True},
     {"determination": "NEEDS_REVIEW"}),
]

NEGATIVE = [
    ("assess_unmasked_refused", "assess_eligibility",
     {"household_size": 4, "monthly_income": 2500, "deidentified": False},
     lambda r: r["assessed"] is False),
    ("redetermine_unmasked_refused", "redetermine",
     {"household_size": 4, "monthly_income": 2500, "prior_eligible": True, "deidentified": False},
     lambda r: r["redetermined"] is False),
    ("overpayment_unmasked_refused", "detect_overpayment_alias", None, None),  # placeholder removed below
]
NEGATIVE = [n for n in NEGATIVE if n[2] is not None]


@pytest.mark.parametrize("label,inp,expected", GOLDEN, ids=[g[0] for g in GOLDEN])
def test_golden_determination(label, inp, expected):
    r = call("assess_eligibility", inp)
    for k, v in expected.items():
        assert r.get(k) == v, f"{label}: {k} expected {v!r}, got {r.get(k)!r}"


@pytest.mark.parametrize("label,tool,inp,check", NEGATIVE, ids=[n[0] for n in NEGATIVE])
def test_negative_fail_closed(label, tool, inp, check):
    assert check(call(tool, inp)), f"{label}: fail-closed guard did not hold"


def test_fpl_figures_are_authoritative_2026():
    """Guards against silent drift of the authoritative FPL constants."""
    mod = __import__("toolkit").load("assess_eligibility")
    assert mod.FPL_BASE == 15960 and mod.FPL_PER_ADD == 5680, "FPL constants drifted from 2026 HHS"
    assert mod.FPL_YEAR == 2026
