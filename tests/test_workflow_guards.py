"""P0-2 — deterministic workflow guards. Proves each machine-verifiable transition gate a Step Functions
controller would branch on: intake extraction, PROVEN de-identification (signed sanitized_ref, not a
boolean), a legal eligibility determination, and the DUE-PROCESS advance-notice HOLD on an adverse
redetermination. Fail-closed everywhere. Pure logic, no AWS."""
from toolkit import call, make_sanitized_ref


def _g(name, **kw):
    return call("workflow_guards", {"guard": name, **kw})


def test_extracted_requires_household_size():
    assert _g("extracted", fields={"household_size": 4})["ok"] is True
    assert _g("extracted", fields={"monthly_income": 2500})["ok"] is False
    assert _g("extracted", fields={})["ok"] is False


def test_deidentified_requires_signed_ref_not_boolean():
    assert _g("deidentified", sanitized_ref=make_sanitized_ref())["ok"] is True
    assert _g("deidentified", deidentified=True)["ok"] is False
    assert _g("deidentified")["ok"] is False


def test_rules_executed_requires_legal_determination():
    assert _g("rules_executed", assessment={"assessed": True, "determination": "ELIGIBLE"})["ok"] is True
    assert _g("rules_executed", assessment={"assessed": True, "determination": "INELIGIBLE"})["ok"] is True
    assert _g("rules_executed", assessment={"assessed": False})["ok"] is False
    assert _g("rules_executed", assessment={"assessed": True, "determination": "MAYBE"})["ok"] is False


def test_adverse_change_holds_without_advance_notice():
    # non-adverse change passes
    assert _g("adverse_notice", redetermination={"change_type": "NONE"})["ok"] is True
    # adverse WITH advance notice passes (due process satisfied)
    assert _g("adverse_notice", redetermination={"change_type": "ADVERSE", "advance_notice_required": True})["ok"] is True
    # adverse WITHOUT advance notice HOLDS (Goldberg due process)
    assert _g("adverse_notice", redetermination={"change_type": "ADVERSE"})["ok"] is False


def test_unknown_guard_and_error_fail_closed():
    assert _g("does_not_exist")["ok"] is False
    assert _g("rules_executed", assessment="{not json")["ok"] is False
