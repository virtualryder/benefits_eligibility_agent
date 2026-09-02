import json
import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Benefits core tools behind the `ben-core` Gateway target:
#   - draft_notice        -> REAL Bedrock (Converse) determination notice from a de-identified case
#   - finalize_determination -> deny-only stub (the human sign-off gate owns the real commit)
# Branch on the input shape (finalize carries case_id; draft carries case/deidentified).

DRAFT_MODEL_ID = os.environ.get("DRAFT_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
GUARDRAIL_ID = os.environ.get("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "DRAFT")

_SYSTEM = (
    "You draft a benefits eligibility DETERMINATION NOTICE for a caseworker to review. You are given an "
    "ALREADY DE-IDENTIFIED case plus an eligibility determination. Write a clear, plain-language notice "
    "(roughly 120-250 words). Rules: (1) Preserve every [REDACTED:...] placeholder verbatim; never guess "
    "redacted values. (2) State the determination (eligible/ineligible/needs review) and the plain reason. "
    "(3) Note the processing timeframe. (4) Include a short, neutral statement of appeal/fair-hearing "
    "rights. (5) This is a DRAFT for human review, not a final decision. Output the notice text only."
)


def _coerce(event):
    e = event or {}
    if isinstance(e, str):
        try:
            e = json.loads(e)
        except Exception:
            e = {"_raw": e}
    return e


def _draft(e):
    # P0-1: draft ONLY from content proven de-identified by a mask_pii-signed sanitized_ref, and only if
    # the case text binds to the signed digest (the model cannot substitute unmasked content).
    import sanitized
    ref = e.get("sanitized_ref")
    if not sanitized.verify_ref(ref):
        return {"error": "refused: de-identification not proven - a valid sanitized_ref signed by mask_pii is required (a boolean is not proof)",
                "drafted_by": None, "deidentified_input": e.get("deidentified")}
    raw_case = e.get("case", "")
    if not isinstance(raw_case, str):
        raw_case = json.dumps(raw_case, ensure_ascii=False)
    case = sanitized.load_text(ref, candidate_text=raw_case)
    if case is None:
        return {"error": "refused: case content does not match the signed sanitized artifact",
                "drafted_by": None, "sanitized_ref_verified": True, "content_bound": False}
    kwargs = dict(
        modelId=DRAFT_MODEL_ID,
        system=[{"text": _SYSTEM}],
        messages=[{"role": "user", "content": [{"text": "De-identified case + determination:\n" + case}]}],
        inferenceConfig={"maxTokens": 700, "temperature": 0.2},
    )
    if GUARDRAIL_ID:
        kwargs["guardrailConfig"] = {"guardrailIdentifier": GUARDRAIL_ID, "guardrailVersion": GUARDRAIL_VERSION}
    try:
        br = boto3.client("bedrock-runtime")
        resp = br.converse(**kwargs)
        notice = resp["output"]["message"]["content"][0]["text"].strip()
        if resp.get("stopReason") == "guardrail_intervened":
            # ANY intervention is fail-closed — including when the guardrail substitutes its
            # configured blocked message (non-empty text). Proven live 2026-08-29: a prompt-injection
            # application was intervened with the canned Aegis message, and the old `and not notice`
            # condition would have minted a notice_ref for it. No notice_ref is created for a
            # blocked draft; the case surfaces to the caseworker as draft-blocked instead.
            return {"error": "guardrail blocked the draft (fail-closed)", "drafted_by": None,
                    "guardrail": "BLOCKED", "guardrail_version": GUARDRAIL_VERSION}
        out = {"drafted_by": DRAFT_MODEL_ID, "chars": len(notice),
               "guardrail_applied": bool(GUARDRAIL_ID), "deidentified_input": True}
        # R3-2 pass-by-reference for the DRAFT OUTPUT: even though the notice is drafted from
        # de-identified content, a redaction gap could leave PII in the text — so it must never travel
        # in Step Functions state or telemetry. With a case store configured, store the notice
        # server-side and return ONLY an opaque notice_ref; the caseworker retrieves it at sign-off.
        import os
        if os.environ.get("CASE_TABLE"):
            import case_store
            out["notice_ref"] = case_store.put_case(notice, kind="notice")
        else:
            out["notice"] = notice
        return out
    except (BotoCoreError, ClientError, KeyError, IndexError) as exc:
        return {"error": "draft failed: " + type(exc).__name__ + ": " + str(exc), "drafted_by": None}


import tenancy  # noqa: E402  (phase 107: interceptor-injected, HMAC-signed tenant)


def handler(event, context):
    # Phase 107 (hybrid multi-tenant): bind the gateway-interceptor-injected, HMAC-SIGNED tenant for
    # per-tenant store routing. Unsigned/forged values are refused; multi-tenant mode fails closed.
    tenancy.bind_tenant_from_args(event)
    e = _coerce(event)
    if "fraud_case_id" in e:
        # refer_fraud is a consequential, HUMAN-ONLY action. The agent can never refer a case as suspected
        # fraud; a qualified investigator/official does. Forbidden to the agent by Cedar (no_self_fraud_referral)
        # and refused here too (defense in depth).
        return {"error": "refused: a fraud referral is a human-only decision; the agent cannot refer",
                "fraud_case_id": e.get("fraud_case_id"), "referred": False}
    if "case_id" in e and "case" not in e:
        # finalize_determination is never a real inline call — the human sign-off gate owns it.
        return {"error": "refused: finalize_determination must go through the human sign-off gate",
                "case_id": e.get("case_id"), "committed": False}
    if "case" in e or "deidentified" in e or "sanitized_ref" in e:
        return _draft(e)
    return {"ok": True, "received": e, "note": "benefits core tool"}
