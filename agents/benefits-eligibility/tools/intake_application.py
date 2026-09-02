import json
import re

# intake_application — extract the decision-relevant, NON-PII fields from a raw benefits application
# (free text or JSON): household size, monthly income, liquid resources, categorical-eligibility flag.
# Deterministic and fail-soft. PII (name, SSN, address) is NOT needed downstream for the determination
# and is redacted separately by mask_pii before drafting/audit.

def _coerce(e):
    e = e or {}
    if isinstance(e, str):
        try:
            return json.loads(e)
        except Exception:
            return {"application": e}
    return e

def _num(s):
    m = re.search(r"[-+]?\d[\d,]*(?:\.\d+)?", str(s))
    return float(m.group(0).replace(",", "")) if m else None

import tenancy  # noqa: E402  (phase 107: interceptor-injected, HMAC-signed tenant)


def handler(event, context):
    # Phase 107 (hybrid multi-tenant): bind the gateway-interceptor-injected, HMAC-SIGNED tenant for
    # per-tenant store routing. Unsigned/forged values are refused; multi-tenant mode fails closed.
    tenancy.bind_tenant_from_args(event)
    e = _coerce(event)
    # R3-2 pass-by-reference: the controller hands an OPAQUE case_ref (raw application content never
    # travels through Step Functions state); fetch server-side. Inline text stays for direct/dev calls.
    if not e.get("application") and e.get("case_ref"):
        import case_store
        _t = case_store.get_case(e["case_ref"]) or ""
        if not _t:
            return {"structured": False, "fields": {}, "missing_required": ["application"],
                    "error": "case_ref unresolved (unknown ref or wrong tenant) - fail-closed"}
        e = {**e, "application": _t}
    # direct structured fields win; otherwise parse the free-text application
    text = e.get("application", "")
    if not isinstance(text, str):
        text = json.dumps(text)
    low = text.lower()

    hh = e.get("household_size")
    if hh is None:
        m = re.search(r"household(?:\s+size)?[^0-9]{0,12}(\d+)", low)
        hh = int(m.group(1)) if m else None
    income = e.get("monthly_income")
    if income is None:
        m = re.search(r"(?:monthly\s+income|income[^.\n]{0,20}month)[^0-9$]{0,12}\$?([\d,]+(?:\.\d+)?)", low)
        income = _num(m.group(1)) if m else None
    resources = e.get("liquid_resources")
    if resources is None:
        m = re.search(r"(?:liquid\s+resources|savings|cash on hand)[^0-9$]{0,12}\$?([\d,]+(?:\.\d+)?)", low)
        resources = _num(m.group(1)) if m else None
    categorical = e.get("categorical_eligibility")
    if categorical is None:
        categorical = bool(re.search(r"\b(ssi|tanf|general assistance|receives medicaid)\b", low))

    fields = {"household_size": hh, "monthly_income": income,
              "liquid_resources": resources, "categorical_eligibility": bool(categorical)}
    missing = [k for k in ("household_size", "monthly_income") if fields.get(k) is None]
    return {"structured": True, "fields": fields, "missing_required": missing,
            "note": "non-PII decision fields; PII is redacted separately by mask_pii"}
