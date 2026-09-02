"""tenancy.py — Gate-B B5: tenant identity is DERIVED, never REQUESTED.

THE DEFECT THIS FIXES: mask_pii once stamped `tenant` into the signed sanitized_ref straight from the
tool-call BODY (`e.get("tenant", "default")`) — i.e. the caller/model chose its own tenant. That lets
one tenant mint artifacts that verify as another's, and mis-attributes audit records. A tenant you can
type is not a tenant.

TWO MODES (both derive tenant from a TRUSTED source, never the request body):

  * SINGLE-TENANT / SILO (default) — one PHA per isolated deployment. The tenant id is pinned at deploy
    time (CDK context `tenant` -> env TENANT_ID on every governed Lambda) and is the only source.
    resolve_tenant() ignores request input by design.

  * MULTI-TENANT / HYBRID (env MULTITENANT=1 — phase 107) — one shared control plane serves many
    tenants. The tenant is derived from the VERIFIED JWT `custom:tenant` claim (the human's access token
    is the bearer the gateway already validated; Cedar evaluates that same principal). It is NEVER read
    from the tool-call body. Missing/blank claim => FAIL-CLOSED (refuse), so an un-tenanted or spoofed
    call cannot silently fall back to a default tenant.

In BOTH modes `check_ref_tenant` refuses an artifact whose tenant != the acting tenant, so an artifact
minted for another tenant (even under a shared signing key) is rejected — fail-closed cross-tenant
rejection. The multi-tenant claim path is the documented Gate-B extension, now implemented.
"""
import base64
import binascii
import json
import os

_ENV = "TENANT_ID"
_MT_ENV = "MULTITENANT"          # "1"/"true"/"yes" => multi-tenant (claim-derived); else silo
_CLAIM = "custom:tenant"         # the VERIFIED JWT claim carrying the tenant id
DEFAULT_TENANT = "default"


class TenantError(Exception):
    """Raised in multi-tenant mode when no verified tenant claim is present (fail-closed)."""


def multitenant_enabled():
    return os.environ.get(_MT_ENV, "").strip().lower() in ("1", "true", "yes", "on")


def tenant_from_claims(claims):
    """Extract the tenant id from VERIFIED JWT claims (custom:tenant). Never from a request body.
    Returns the trimmed tenant id, or None if absent/blank/not-a-dict."""
    if not isinstance(claims, dict):
        return None
    t = claims.get(_CLAIM)
    if isinstance(t, str) and t.strip():
        return t.strip()
    return None


def tenant_from_bearer(token):
    """Read custom:tenant from a JWT bearer WITHOUT verifying it — the gateway (CUSTOM_JWT) is the
    verifier; the runtime only reads the already-trusted claim to bind the session tenant / log it.
    Returns None on any decode problem. Never use this for an AUTHORIZATION decision (that is Cedar's
    job at the gateway); use it only for session binding / observability tagging."""
    if not isinstance(token, str) or token.count(".") < 2:
        return None
    payload_b64 = token.split(".")[1]
    payload_b64 += "=" * (-len(payload_b64) % 4)          # pad to a multiple of 4
    try:
        claims = json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return None
    return tenant_from_claims(claims)


def resolve_tenant(_event=None, *, claims=None):
    """Resolve the acting tenant.

    SILO (default): the deployment's pinned TENANT_ID (request input IGNORED).
    MULTI-TENANT (MULTITENANT=1): the VERIFIED custom:tenant claim; FAIL-CLOSED if absent.

    In BOTH modes, request-body tenant values are ignored — identity is derived, never requested.
    Pass `claims` (the gateway-verified JWT claims) in multi-tenant mode.
    """
    if multitenant_enabled():
        t = tenant_from_claims(claims)
        if not t:
            raise TenantError(
                "multi-tenant: no verified custom:tenant claim; refusing "
                "(tenant is derived from the authenticated identity, never requested)")
        return t
    return os.environ.get(_ENV) or DEFAULT_TENANT


def check_ref_tenant(ref, *, claims=None):
    """True iff the (already signature-verified) ref belongs to the ACTING tenant.
    Fail-closed: not-a-dict, missing tenant field, a mismatch, or (multi-tenant) a missing claim -> False."""
    if not isinstance(ref, dict):
        return False
    try:
        return ref.get("tenant") == resolve_tenant(claims=claims)
    except TenantError:
        return False


def tenant_scoped_name(base, tenant):
    """Per-tenant PHYSICAL resource name (hybrid model: each tenant gets its OWN data store, not a
    shared table with a tenant partition key). Blank tenant -> the base name (single-tenant silo).
    Used by the CDK (per-tenant table/bucket naming) and by the compute layer (routing a claim-derived
    tenant to its store), so naming cannot drift between infra and runtime."""
    t = (tenant or "").strip()
    return f"{t}-{base}" if t else base
