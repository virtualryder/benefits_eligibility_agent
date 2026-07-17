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
    if e.get("deidentified") is not True:
        return {"error": "refused: case is not de-identified (deidentified must be true)",
                "drafted_by": None, "deidentified_input": e.get("deidentified")}
    case = e.get("case", "")
    if not isinstance(case, str):
        case = json.dumps(case, ensure_ascii=False)
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
        if resp.get("stopReason") == "guardrail_intervened" and not notice:
            return {"error": "output guardrail blocked the draft (fail-closed)", "drafted_by": None, "guardrail": "BLOCKED"}
        return {"drafted_by": DRAFT_MODEL_ID, "chars": len(notice),
                "guardrail_applied": bool(GUARDRAIL_ID), "deidentified_input": True, "notice": notice}
    except (BotoCoreError, ClientError, KeyError, IndexError) as exc:
        return {"error": "draft failed: " + type(exc).__name__ + ": " + str(exc), "drafted_by": None}


def handler(event, context):
    e = _coerce(event)
    if "case_id" in e and "case" not in e:
        # finalize_determination is never a real inline call — the human sign-off gate owns it.
        return {"error": "refused: finalize_determination must go through the human sign-off gate",
                "case_id": e.get("case_id"), "committed": False}
    if "case" in e or "deidentified" in e:
        return _draft(e)
    return {"ok": True, "received": e, "note": "benefits core tool"}
