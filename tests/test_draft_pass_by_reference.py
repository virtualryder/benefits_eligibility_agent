"""R3-2 (draft output): the benefits determination NOTICE must NEVER be returned as text by the drafter
in pass-by-reference mode — only an opaque notice_ref. Even though the notice is drafted from
de-identified content, a redaction gap could leave PII in the text, so it must not enter Step Functions
state, the pending record, or telemetry. Regression guard for the class of leak the PV strict canary
caught (drafted text crossing execution state)."""
import json

from toolkit import load, make_sanitized_ref

CASE = "[REDACTED:NAME] household of 3; monthly income [REDACTED:OTHER]"
NOTICE = "Determination: ELIGIBLE. CANARY_LEAKMARKER_XYZ. You may request a fair hearing within 90 days."


class _FakeBedrock:
    def converse(self, **kw):
        return {"output": {"message": {"content": [{"text": NOTICE}]}}, "stopReason": "end_turn"}


def test_draft_returns_notice_ref_never_text(monkeypatch):
    core = load("benefits_core")
    monkeypatch.setattr(core.boto3, "client", lambda *a, **k: _FakeBedrock())
    # pass-by-reference mode on; stub the server-side store so no DynamoDB is needed
    monkeypatch.setenv("CASE_TABLE", "ben-test-case-store")
    import case_store
    monkeypatch.setattr(case_store, "put_case",
                        lambda text, kind="application", case_id="": "case-notice-deadbeef")
    r = core.handler({"sanitized_ref": make_sanitized_ref(CASE), "case": CASE, "deidentified": True}, None)

    assert "notice" not in r, "raw notice text must not be a response field in pass-by-reference mode"
    assert "CANARY_LEAKMARKER_XYZ" not in json.dumps(r), "notice text leaked into the tool response"
    assert r.get("notice_ref") == "case-notice-deadbeef", "the drafter must return an opaque notice_ref"


def test_draft_fail_closed_without_proof():
    core = load("benefits_core")
    r = core.handler({"case": "unmasked PII here", "deidentified": True}, None)  # no valid sanitized_ref
    assert r.get("drafted_by") is None
    assert "notice_ref" not in r and "notice" not in r
