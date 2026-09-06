"""Unit tests for the benefits-eligibility governed tools — contract + fail-closed behavior.
No AWS: only the deterministic paths and the deny-branches are exercised (the model/masking calls
are covered by the live demo, not here)."""
from toolkit import call, make_sanitized_ref


def test_intake_extracts_decision_fields():
    r = call("intake_application", {"application": "Household size 4. Monthly income 2500. Savings 60."})
    assert r["fields"]["household_size"] == 4
    assert r["fields"]["monthly_income"] == 2500


def test_assess_is_fail_closed_on_unmasked():
    r = call("assess_eligibility", {"household_size": 4, "monthly_income": 2500, "deidentified": False})
    assert r["assessed"] is False
    assert "de-identif" in r["error"]


def test_assess_eligible_path():
    r = call("assess_eligibility", {"household_size": 4, "monthly_income": 2500,
                                    "sanitized_ref": make_sanitized_ref()})
    assert r["determination"] == "ELIGIBLE"
    assert r["eligible"] is True
    assert r["fpl_year"] == 2026


def test_redetermine_adverse_requires_advance_notice():
    r = call("redetermine", {"household_size": 4, "monthly_income": 9000,
                             "prior_eligible": True, "sanitized_ref": make_sanitized_ref()})
    assert r["change_type"] == "ADVERSE"
    assert r["advance_notice_required"] is True


def test_overpayment_math():
    r = call("overpayment", {"prior_monthly_benefit": 500, "corrected_monthly_benefit": 300,
                             "months": 6, "sanitized_ref": make_sanitized_ref()})
    assert r["classification"] == "OVERPAYMENT"
    assert r["overpayment_amount"] == 1200.0


def test_core_finalize_is_refused():
    r = call("benefits_core", {"case_id": "CASE-1"})
    assert r["committed"] is False


def test_core_refer_fraud_is_refused():
    r = call("benefits_core", {"fraud_case_id": "CASE-1"})
    assert r["referred"] is False
    assert "human-only" in r["error"]


def test_core_draft_refused_on_unmasked():
    r = call("benefits_core", {"case": "x", "deidentified": False})
    assert r.get("drafted_by") is None


# -- L20 (live-found, full-portfolio gate attempt 6, 2026-09-06) ------------------------------------
# The extractor matched the bare token `tanf` and set categorical_eligibility=True for an application
# reading "... no TANF." Categorical eligibility SKIPS the income/resource test, so a negation-blind
# match converts an income-tested case into an automatic approval - a materially wrong legal
# determination drawn from text that says the opposite. It reached production because every fixture
# here asserted the POSITIVE case; what caught it was the contextual-grounding guardrail live (the
# drafter refused a determination its own case facts contradicted, score 0.31 vs threshold 0.55).

NEGATED = [
    "Household 3, monthly income 1800, liquid resources 400, no TANF.",   # the exact live case
    "Denied SSI in March; reapplying.",
    "TANF: none",
    "Not receiving general assistance.",
    "SSI benefits were terminated last year.",
    "No longer on TANF.",
    "Applicant has never had SSI.",
]

GRANTED = [
    "Applicant receives TANF for the household.",
    "No TANF. Receives SSI since 2024.",        # a clause boundary ends the negation
    "Household receives Medicaid and SSI.",
    "Household 2, income 900, receives general assistance.",
]


def test_intake_categorical_eligibility_is_negation_aware():
    """A negated benefit mention must never grant categorical eligibility."""
    for text in NEGATED:
        r = call("intake_application", {"application": text})
        assert r["fields"]["categorical_eligibility"] is False, text


def test_intake_still_detects_a_real_categorical_grant():
    """...and the negation guard must not suppress an actual grant."""
    for text in GRANTED:
        r = call("intake_application", {"application": text})
        assert r["fields"]["categorical_eligibility"] is True, text


def test_intake_explicit_field_still_wins_over_the_text():
    """A caller-supplied structured field is authoritative - the text scan is only the fallback."""
    r = call("intake_application", {"application": "no TANF", "categorical_eligibility": True})
    assert r["fields"]["categorical_eligibility"] is True
