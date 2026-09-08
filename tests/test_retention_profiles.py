"""EV-1: the retention profiles, and the one that made the auditor's question answerable.

Every gate up to 2026-09-08 ran Object Lock in GOVERNANCE mode with 1-day retention so the
environment could be torn down - and the teardown path calls delete_object with
BypassGovernanceRetention=True. So "the audit record cannot be altered" had never been tested
against the mode that actually guarantees it.

It could not be tested cheaply either: the only COMPLIANCE profile locks for 2555 days, and AWS
states "the only way to delete an object under the compliance mode before its retention date
expires is to delete the associated AWS account". Nobody runs that on a working account.

`compliance-proof` is the same mechanism at a disposable duration. Proven live on 2026-09-08
against `ben-ev1-data` (evidence/COMPLIANCE-LOCK-PROOF-2026-09-08.json): the bucket reports
COMPLIANCE, a plain delete is refused, and the deployment's own BypassGovernanceRetention teardown
call is refused with "Access Denied because object protected by object lock."
"""
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "cdk"))

from ben_stacks.data_stack import RETENTION_PROFILES  # noqa: E402


def test_sandbox_and_pilot_are_governance_and_are_not_evidence_of_immutability():
    assert RETENTION_PROFILES["sandbox-demo"][0].value == "GOVERNANCE"
    assert RETENTION_PROFILES["pilot"][0].value == "GOVERNANCE"


def test_a_compliance_profile_exists_at_a_duration_that_can_actually_be_run():
    """The 7-year profile is unrunnable on a working account, so it proved nothing."""
    mode, dur = RETENTION_PROFILES["compliance-proof"]
    assert mode.value == "COMPLIANCE"
    assert dur.to_days() <= 7, (
        "compliance-proof must stay disposable - the point is that it releases itself. A long "
        "retention here recreates the problem it exists to solve: an untestable claim.")


def test_the_production_reference_profile_is_still_compliance_and_long():
    mode, dur = RETENTION_PROFILES["production-reference"]
    assert mode.value == "COMPLIANCE"
    assert dur.to_days() >= 2555


def test_the_production_gate_accepts_the_proof_profile():
    """cdk/app.py gates the production profile on a name prefix; `compliance-proof` must qualify."""
    src = (ROOT / "cdk" / "app.py").read_text(encoding="utf-8")
    assert 'startswith(("production", "compliance"))' in src, (
        "the production-profile gate no longer accepts a compliance* profile name; EV-1's proof "
        "profile would be rejected by the very gate that requires COMPLIANCE")


@pytest.mark.parametrize("name", sorted(RETENTION_PROFILES))
def test_every_profile_declares_both_a_mode_and_a_duration(name):
    mode, dur = RETENTION_PROFILES[name]
    assert mode.value in ("GOVERNANCE", "COMPLIANCE")
    assert dur.to_days() >= 1


def test_the_ev1_evidence_records_the_refusal_and_scopes_its_own_claim():
    """A pass here is not the proof - the live run is. This keeps the record honest."""
    import json
    p = ROOT / "evidence" / "COMPLIANCE-LOCK-PROOF-2026-09-08.json"
    if not p.exists():
        pytest.skip("EV-1 evidence not present in this checkout")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["PASS"] is True
    assert d["object_lock"]["mode"] == "COMPLIANCE"
    assert d["checks"]["teardown_bypass_is_refused"]["ok"] is True
    assert "object lock" in d["checks"]["teardown_bypass_is_refused"]["detail"].lower()
    assert "does NOT prove a 7-year schedule" in d["scope_note"], (
        "the evidence must scope its own claim - the duration is a parameter, the immutability is "
        "the mechanism")
