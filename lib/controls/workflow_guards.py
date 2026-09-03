import json

import sanitized

# workflow_guards — the machine-verifiable transition evidence for a DETERMINISTIC benefits-eligibility
# workflow controller (P0-2), ported from the financial-aid/housing control plane.
#
# THE DEFECT THIS FIXES: the intake -> mask -> assess -> notice -> audit -> signoff pipeline was
# sequenced by the MODEL (workflow.entrypoint: agent.py). A prompt-injection or model error could skip
# masking or the eligibility gate, or advance an adverse action without the due-process advance notice.
# A model should not be the thing that guarantees regulated transitions happened.
#
# THE FIX: a deterministic controller (a Step Functions state machine, wired in the CDK/deploy layer)
# invokes this single guard Lambda BETWEEN pipeline stages; each guard returns {"guard","ok","reason"}
# and the state machine BRANCHES on `ok`. A stage cannot be skipped, reordered, or passed on unverified
# state, because the transition itself demands structural or cryptographic proof:
#
#   extracted      -> intake produced the load-bearing decision field (household size)
#   deidentified   -> a VERIFIED mask_pii-signed sanitized_ref exists (P0-1; a boolean is never accepted)
#   rules_executed -> the deterministic eligibility engine ran and returned a legal determination
#   adverse_notice -> an ADVERSE redetermination (benefit reduced/terminated) carries the required
#                     advance notice — DUE PROCESS (Goldberg v. Kelly); otherwise it HOLDS
#
# Fail-closed: any missing/forged/tampered/malformed evidence -> ok:false; the controller routes to
# ManualReview / a HOLD, never onward. Pure logic + the shared verifiers, fully unit-testable offline.
# (This module is the portable heart of P0-2; wiring the Step Functions controller is the CDK/deploy
# follow-on — the guards it will branch on are proven here.)

_LEGAL_DETERMINATIONS = {"ELIGIBLE", "INELIGIBLE", "NEEDS_REVIEW"}


def _coerce(e):
    e = e or {}
    if isinstance(e, str):
        try:
            e = json.loads(e)
        except Exception:
            e = {}
    return e


def _as_dict(v):
    if isinstance(v, str):
        try:
            return json.loads(v)
        except Exception:
            return {}
    return v if isinstance(v, dict) else {}


def guard_extracted(e):
    """intake_application must yield the household size — the load-bearing field for an eligibility
    determination. Income may be absent (routes to NEEDS_REVIEW downstream)."""
    f = _as_dict(e.get("fields")) or {}
    hh = f.get("household_size")
    ok = hh is not None and str(hh).strip() not in ("", "0", "None")
    return ok, ("household_size present" if ok else "intake did not yield a household_size")


def guard_deidentified(e):
    """PII de-identification must be PROVEN by a mask_pii-signed sanitized_ref (P0-1), never a boolean."""
    ok = sanitized.verify_ref(e.get("sanitized_ref"))
    return ok, ("masking proven by a verified mask_pii-signed sanitized_ref" if ok else
                "de-identification not proven (no valid sanitized_ref; a boolean is not proof)")


def guard_rules_executed(e):
    """The deterministic eligibility engine must have run and returned a legal determination."""
    a = _as_dict(e.get("assessment")) or e
    ok = a.get("assessed") is True and a.get("determination") in _LEGAL_DETERMINATIONS
    return ok, ("deterministic eligibility engine produced a legal determination" if ok else
                "eligibility engine did not run or returned no legal determination")


def guard_adverse_notice(e):
    """DUE PROCESS gate. An ADVERSE redetermination (benefit reduced or terminated) must carry the
    required timely advance notice before it can proceed to a caseworker for commitment. If an adverse
    change lacks advance notice, this HOLDS (ok=False) — the constitutional protection (Goldberg v.
    Kelly) is enforced by the platform, not left to the model. Non-adverse changes pass."""
    r = _as_dict(e.get("redetermination")) or e
    change = str(r.get("change_type") or "").upper()
    adverse = change == "ADVERSE"
    if not adverse:
        return True, "non-adverse change — no advance-notice hold"
    ok = r.get("advance_notice_required") is True
    return ok, ("adverse change carries the required advance notice (due process)" if ok else
                "adverse change is missing the required advance notice — HOLD (Goldberg due process)")


_GUARDS = {
    "extracted": guard_extracted,
    "deidentified": guard_deidentified,
    "rules_executed": guard_rules_executed,
    "adverse_notice": guard_adverse_notice,
}


def _emit_metric(guard, ok):
    """Security telemetry: every guard evaluation emits a CloudWatch EMF metric
    (Benefits/Governance :: GuardFailed{Guard}). A failed guard is a SECURITY / due-process SIGNAL —
    forged sanitized_ref, an adverse action without notice — not just an ops event. Metric only."""
    import json as _json
    import time as _time
    try:
        print(_json.dumps({
            "_aws": {"Timestamp": int(_time.time() * 1000),
                     "CloudWatchMetrics": [{"Namespace": "Benefits/Governance",
                                            "Dimensions": [["Guard"]],
                                            "Metrics": [{"Name": "GuardFailed", "Unit": "Count"}]}]},
            "Guard": guard, "GuardFailed": 0 if ok else 1}))
    except Exception:
        pass   # metrics must never affect the control decision


import tenancy  # noqa: E402  (phase 107: interceptor-injected, HMAC-signed tenant)
import telemetry  # noqa: E402  (phase 110: correlation keys -> one aegis.call log line per invocation)


@telemetry.instrument('workflow_guards')
def handler(event, context):
    # Phase 107 (hybrid multi-tenant): bind the gateway-interceptor-injected, HMAC-SIGNED tenant for
    # per-tenant store routing. Unsigned/forged values are refused; multi-tenant mode fails closed.
    tenancy.bind_tenant_from_args(event)
    e = _coerce(event)
    name = str(e.get("guard", ""))
    fn = _GUARDS.get(name)
    if fn is None:
        _emit_metric(name or "unknown", False)
        return {"guard": name, "ok": False, "reason": "unknown guard (fail-closed)"}
    try:
        ok, reason = fn(e)
    except Exception as exc:  # any guard error is a fail-closed deny, never a pass
        ok, reason = False, "guard error (fail-closed): %s" % type(exc).__name__
    _emit_metric(name, ok)
    return {"guard": name, "ok": bool(ok), "reason": reason}
