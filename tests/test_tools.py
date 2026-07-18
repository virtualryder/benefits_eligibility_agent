"""Unit tests for the benefits-eligibility governed tools — contract + fail-closed behavior.
No AWS: only the deterministic paths and the deny-branches are exercised (the model/masking calls
are covered by the live demo, not here)."""
from toolkit import call


def test_intake_extracts_decision_fields():
    r = call("intake_application", {"application": "Household size 4. Monthly income 2500. Savings 60."})
    assert r["fields"]["household_size"] == 4
    assert r["fields"]["monthly_income"] == 2500


def test_assess_is_fail_closed_on_unmasked():
    r = call("assess_eligibility", {"household_size": 4, "monthly_income": 2500, "deidentified": False})
    assert r["assessed"] is False
    assert "de-identified" in r["error"]


def test_assess_eligible_path():
    r = call("assess_eligibility", {"household_size": 4, "monthly_income": 2500, "deidentified": True})
    assert r["determination"] == "ELIGIBLE"
    assert r["eligible"] is True
    assert r["fpl_year"] == 2026


def test_redetermine_adverse_requires_advance_notice():
    r = call("redetermine", {"household_size": 4, "monthly_income": 9000,
                             "prior_eligible": True, "deidentified": True})
    assert r["change_type"] == "ADVERSE"
    assert r["advance_notice_required"] is True


def test_overpayment_math():
    r = call("overpayment", {"prior_monthly_benefit": 500, "corrected_monthly_benefit": 300,
                             "months": 6, "deidentified": True})
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
