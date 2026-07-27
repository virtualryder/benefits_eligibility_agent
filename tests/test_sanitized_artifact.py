"""P0-1 — server-issued sanitized-artifact references (ported from the financial-aid/housing control
plane). Proves the PII de-identification gate now rests on a mask_pii-SIGNED reference (proof-of-masking)
with a CONTENT-BINDING hash — and that the previously spoofable `deidentified: true` boolean is no longer
accepted as proof by any tool. Pure logic, no AWS (the artifact store is in-memory)."""
import json

from toolkit import call, make_sanitized_ref
import sanitized

MASKED = "[REDACTED:NAME] household of 3, monthly income 1800, [REDACTED:SSN]"


def _ref(text=MASKED, store=None):
    return sanitized.mint_ref(text, engine="comprehend:DetectPiiEntities", entities_masked=2, store=store)


def test_mint_then_verify_roundtrips():
    ref = _ref()
    assert ref["authoritative"] is True and ref["sig"]
    assert sanitized.verify_ref(ref) is True
    assert sanitized.verify_ref(json.dumps(ref)) is True


def test_verify_rejects_forged_and_tampered_refs():
    ref = _ref()
    assert sanitized.verify_ref(dict(ref, sig="deadbeef" * 8)) is False
    assert sanitized.verify_ref(dict(ref, sanitized_sha256=sanitized.sha256_text("other"))) is False
    assert sanitized.verify_ref({"deidentified": True}) is False
    assert sanitized.verify_ref(True) is False
    assert sanitized.verify_ref(None) is False


def test_mint_without_secret_is_not_authoritative(monkeypatch):
    monkeypatch.delenv("PROVENANCE_SECRET", raising=False)
    ref = _ref()
    assert ref["authoritative"] is False
    assert sanitized.verify_ref(ref) is False


def test_store_roundtrip_and_content_binding():
    st = sanitized.MemoryStore()
    ref = _ref(store=st)
    assert ref["stored"] is True
    assert sanitized.load_text(ref, store=st) == MASKED
    assert sanitized.load_text(ref, candidate_text=MASKED, store=None) == MASKED
    assert sanitized.load_text(ref, candidate_text="UNMASKED John Doe SSN 123-45-6789", store=None) is None


# ── the tools refuse the spoofed boolean (the P0-1 attack) ────────────────────

def test_spoofed_boolean_refused_by_assess():
    r = call("assess_eligibility", {"household_size": 4, "monthly_income": 2500, "deidentified": True})
    assert r["assessed"] is False


def test_spoofed_boolean_refused_by_redetermine():
    r = call("redetermine", {"household_size": 4, "monthly_income": 9000, "prior_eligible": True,
                             "deidentified": True})
    assert r["redetermined"] is False


def test_spoofed_boolean_refused_by_overpayment():
    r = call("overpayment", {"prior_monthly_benefit": 500, "corrected_monthly_benefit": 300, "months": 6,
                             "deidentified": True})
    assert r["computed"] is False


def test_spoofed_boolean_refused_by_draft():
    r = call("benefits_core", {"case": "unmasked: Jane Roe DOB 1990-01-01", "deidentified": True})
    assert r.get("drafted_by") is None and "refused" in r.get("error", "")


def test_draft_refuses_substituted_content():
    ref = make_sanitized_ref("[REDACTED:NAME] approved for SNAP")
    r = call("benefits_core", {"case": "SUBSTITUTED unmasked John Doe SSN 123-45-6789", "sanitized_ref": ref})
    assert r.get("drafted_by") is None
    assert r.get("content_bound") is False
