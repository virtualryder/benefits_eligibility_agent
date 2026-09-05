"""deep-dive #3 (end-to-end): the benefits `authoritative_context` resolver supplies Cedar's
consent/purpose from an AUTHORITATIVE record, never a caller assertion. The gateway interceptor strips
any caller-supplied consent/purpose and calls resolve(args, tenant); this module returns a field ONLY
when a real record supports it, and stays SILENT (fail-closed -> Cedar denies) otherwise.

Offline: boto3 is stubbed at the module seam (no AWS).
"""
import sys
import pathlib
import time

CONTROLS = pathlib.Path(__file__).resolve().parents[1] / "lib" / "controls"
sys.path.insert(0, str(CONTROLS))

import authoritative_context as ac  # noqa: E402


class _Tbl:
    def __init__(self, item):
        self._item = item

    def get_item(self, Key):
        return {"Item": self._item} if self._item is not None else {}


def _wire(monkeypatch, item, table="ben-x-authz-context", raises=False):
    monkeypatch.setenv("AUTHZ_TABLE", table)
    monkeypatch.delenv("AUTHZ_TABLE_TEMPLATE", raising=False)
    tbl = _Tbl(item)

    class _Res:
        def Table(self, name):
            if raises:
                raise RuntimeError("dynamodb unavailable")
            return tbl
    import types
    monkeypatch.setattr(ac, "boto3", types.SimpleNamespace(resource=lambda *a, **k: _Res()), raising=False)
    # ac imports boto3 lazily inside _get_record; patch the module the lazy import resolves to
    monkeypatch.setitem(sys.modules, "boto3", types.SimpleNamespace(resource=lambda *a, **k: _Res()))


def test_no_case_id_returns_empty(monkeypatch):
    _wire(monkeypatch, {"consent": True, "authorized_purpose": "eligibility"})
    assert ac.resolve({}, None) == {}
    assert ac.resolve({"case_id": 123}, None) == {}          # non-string case id -> fail-closed


def test_authoritative_consent_and_purpose(monkeypatch):
    _wire(monkeypatch, {"case_id": "C1", "consent": True, "authorized_purpose": "eligibility"})
    out = ac.resolve({"case_id": "C1", "consent": False, "purpose": "marketing"}, None)
    assert out == {"consent": True, "purpose": "eligibility"}  # record wins; caller args are irrelevant


def test_no_record_is_fail_closed(monkeypatch):
    _wire(monkeypatch, None)                                   # no record for the case
    assert ac.resolve({"case_id": "C1", "consent": True}, None) == {}   # caller cannot fake consent


def test_expired_consent_is_not_granted(monkeypatch):
    _wire(monkeypatch, {"case_id": "C1", "consent": True, "authorized_purpose": "eligibility",
                        "expires_at": int(time.time()) - 60})
    out = ac.resolve({"case_id": "C1"}, None)
    assert "consent" not in out and out.get("purpose") == "eligibility"  # stale consent dropped


def test_unreadable_table_never_grants(monkeypatch):
    _wire(monkeypatch, {"case_id": "C1", "consent": True}, raises=True)
    assert ac.resolve({"case_id": "C1"}, None) == {}           # error -> fail-closed, never grant


def test_no_table_configured_is_fail_closed(monkeypatch):
    monkeypatch.delenv("AUTHZ_TABLE", raising=False)
    monkeypatch.delenv("AUTHZ_TABLE_TEMPLATE", raising=False)
    assert ac.resolve({"case_id": "C1", "consent": True}, None) == {}


def test_multitenant_template_routes_to_tenant_table(monkeypatch):
    captured = {}

    class _Res:
        def Table(self, name):
            captured["name"] = name
            return _Tbl({"case_id": "C1", "consent": True})
    import types
    monkeypatch.setenv("AUTHZ_TABLE", "ben-x-authz-context")
    monkeypatch.setenv("AUTHZ_TABLE_TEMPLATE", "ben-x-{tenant}-authz-context")
    monkeypatch.setitem(sys.modules, "boto3", types.SimpleNamespace(resource=lambda *a, **k: _Res()))
    ac.resolve({"case_id": "C1"}, "pha-a")
    assert captured["name"] == "ben-x-pha-a-authz-context"     # routed to the acting tenant's store
