"""Phase 107 — tenant identity is DERIVED, never REQUESTED, in BOTH silo and multi-tenant modes.

Proves: (a) silo mode returns the pinned TENANT_ID and ignores any request body; (b) multi-tenant mode
derives the tenant from the VERIFIED custom:tenant claim; (c) multi-tenant mode is FAIL-CLOSED when the
claim is absent/blank; (d) a body-supplied `tenant` is ignored in both modes; (e) cross-tenant refs are
refused; (f) tenant_from_bearer reads the claim from a JWT payload without verifying. Pure stdlib, no AWS.
"""
import base64
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib" / "controls"))
import tenancy  # noqa: E402


def _reset(monkeypatch, *, mt=False, pinned=None):
    monkeypatch.delenv("MULTITENANT", raising=False)
    monkeypatch.delenv("TENANT_ID", raising=False)
    if mt:
        monkeypatch.setenv("MULTITENANT", "1")
    if pinned is not None:
        monkeypatch.setenv("TENANT_ID", pinned)


def _jwt(claims):
    hdr = base64.urlsafe_b64encode(b'{"alg":"RS256"}').decode().rstrip("=")
    body = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    return f"{hdr}.{body}.sig"


def test_silo_returns_pinned_and_ignores_body(monkeypatch):
    _reset(monkeypatch, pinned="pha-alameda")
    assert tenancy.resolve_tenant() == "pha-alameda"
    # a request body claiming another tenant is ignored
    assert tenancy.resolve_tenant({"tenant": "pha-evil"}) == "pha-alameda"


def test_silo_default_when_unset(monkeypatch):
    _reset(monkeypatch)
    assert tenancy.resolve_tenant() == tenancy.DEFAULT_TENANT


def test_multitenant_derives_from_verified_claim(monkeypatch):
    _reset(monkeypatch, mt=True, pinned="pha-ignored-in-mt")
    claims = {"sub": "u1", "custom:tenant": "pha-oakland", "cognito:groups": "benefits_caseworker"}
    assert tenancy.resolve_tenant(claims=claims) == "pha-oakland"
    # the pinned env is NOT used in multi-tenant mode
    assert tenancy.resolve_tenant(claims=claims) != "pha-ignored-in-mt"


def test_multitenant_fail_closed_without_claim(monkeypatch):
    _reset(monkeypatch, mt=True, pinned="pha-fallback")
    with pytest.raises(tenancy.TenantError):
        tenancy.resolve_tenant(claims={"sub": "u1"})        # no custom:tenant
    with pytest.raises(tenancy.TenantError):
        tenancy.resolve_tenant(claims={"custom:tenant": "  "})  # blank
    with pytest.raises(tenancy.TenantError):
        tenancy.resolve_tenant()                             # no claims at all


def test_multitenant_ignores_body_tenant(monkeypatch):
    _reset(monkeypatch, mt=True)
    # body says pha-evil; only the verified claim counts
    claims = {"custom:tenant": "pha-real"}
    assert tenancy.resolve_tenant({"tenant": "pha-evil"}, claims=claims) == "pha-real"


def test_check_ref_tenant_cross_tenant_refused(monkeypatch):
    _reset(monkeypatch, mt=True)
    claims = {"custom:tenant": "pha-real"}
    assert tenancy.check_ref_tenant({"tenant": "pha-real"}, claims=claims) is True
    assert tenancy.check_ref_tenant({"tenant": "pha-other"}, claims=claims) is False
    assert tenancy.check_ref_tenant({}, claims=claims) is False
    assert tenancy.check_ref_tenant("not-a-dict", claims=claims) is False


def test_check_ref_tenant_silo(monkeypatch):
    _reset(monkeypatch, pinned="pha-alameda")
    assert tenancy.check_ref_tenant({"tenant": "pha-alameda"}) is True
    assert tenancy.check_ref_tenant({"tenant": "pha-other"}) is False


def test_tenant_from_bearer_reads_claim_without_verify(monkeypatch):
    tok = _jwt({"sub": "u1", "custom:tenant": "pha-oakland"})
    assert tenancy.tenant_from_bearer(tok) == "pha-oakland"
    assert tenancy.tenant_from_bearer("not-a-jwt") is None
    assert tenancy.tenant_from_bearer(_jwt({"sub": "u1"})) is None   # no tenant claim
