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
import telemetry  # noqa: E402  (phase 110: correlation keys -> one aegis.call log line per invocation)



# L20 (live-found 2026-09-06): categorical eligibility is NEGATION-AWARE. A bare token search set
# categorical_eligibility=True for an application reading "... no TANF." - and categorical
# eligibility SKIPS the income/resource test, so a negation-blind match silently converts an
# income-tested case into an automatic approval. Caught downstream by the contextual-grounding
# guardrail (the drafter refused a determination its own case facts contradicted), never by a unit
# test, because every fixture asserted the positive case.
_CATEGORICAL_TOKENS = r"(?:ssi|tanf|general assistance|receives medicaid)"
# Cues that negate a benefit mentioned nearby, in either direction ("no TANF", "TANF: none",
# "denied SSI", "SSI - terminated", "not receiving general assistance").
_NEGATION_CUES = (
    "no ", "not ", "non-", "never", "none", "without", "denied", "denies", "denial",
    "ineligible", "terminated", "discontinued", "closed", "ended", "no longer",
    "does not", "doesn't", "did not", "didn't", "is not", "isn't", "are not", "aren't",
    "declined", "withdrew", "withdrawn", "expired", "n/a", "refused",
)
# A clause boundary stops the negation window: "no TANF. Receives SSI" must still be categorical.
# A colon breaks the window only when looking BACKWARD - forward it usually introduces the value
# ("TANF: none"), so the negation must still be visible after it.
_CLAUSE_BREAK_BEFORE = ".;:\n|"
_CLAUSE_BREAK_AFTER = ".;\n|"


def _clause_before(low, start, width=40):
    """The text just before a match, back to the nearest clause boundary (max `width` chars)."""
    lo = max(0, start - width)
    seg = low[lo:start]
    for ch in _CLAUSE_BREAK_BEFORE:
        seg = seg.rsplit(ch, 1)[-1]
    return seg


def _clause_after(low, end, width=40):
    """...and just after it. Wide enough to see a trailing status ("SSI benefits were terminated")."""
    seg = low[end:end + width]
    for ch in _CLAUSE_BREAK_AFTER:
        seg = seg.split(ch, 1)[0]
    return seg


def _categorical_from_text(low):
    """True only when a categorical-eligibility benefit is mentioned WITHOUT a negation cue in the
    clause around it. Fail-closed on ambiguity: a negated mention never counts as a grant."""
    for m in re.finditer(r"\b" + _CATEGORICAL_TOKENS + r"\b", low):
        before = _clause_before(low, m.start())
        after = _clause_after(low, m.end())
        window = before + " " + after
        if any(cue in window for cue in _NEGATION_CUES):
            continue
        return True
    return False


@telemetry.instrument('intake_application')
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
        categorical = _categorical_from_text(low)

    fields = {"household_size": hh, "monthly_income": income,
              "liquid_resources": resources, "categorical_eligibility": bool(categorical)}
    missing = [k for k in ("household_size", "monthly_income") if fields.get(k) is None]
    return {"structured": True, "fields": fields, "missing_required": missing,
            "note": "non-PII decision fields; PII is redacted separately by mask_pii"}
