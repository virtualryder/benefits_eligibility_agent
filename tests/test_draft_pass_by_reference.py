"""R3-2 (draft output): the benefits determination NOTICE must NEVER be returned as text by the drafter
in pass-by-reference mode — only an opaque notice_ref. Even though the notice is drafted from
de-identified content, a redaction gap could leave PII in the text, so it must not enter Step Functions
state, the pending record, or telemetry. Regression guard for the class of leak the PV strict canary
caught (drafted text crossing execution state)."""
import json

from toolkit import load, make_sanitized_ref

CASE = "[REDACTED:NAME] household of 3; monthly income [REDACTED:OTHER]"
NOTICE = "Determination: ELIGIBLE. CANARY_LEAKMARKER_XYZ. You may request a fair hearing within 90 days."
# the deterministic engine's output (assess_eligibility) - the ONLY determination the grounded drafter may state
DETERMINATION = {"assessed": True, "determination": "ELIGIBLE", "eligible": True, "processing_clock": "EXPEDITED",
                 "processing_days": 7, "income_pct_fpl": 66.4, "household_size": 3,
                 "reason": "gross monthly income 1800 is within the 130% FPL limit (2711)",
                 "notes": ["SMUGGLED free text must not reach the grounding source"]}


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


def test_draft_converse_is_tagged_with_correlation_request_metadata(monkeypatch):
    """Task 128 follow-up (mt6 gate): the drafter's model-invocation log row must be per-tenant filterable
    like the Runtime's, so requestMetadata carries the correlation keys - and NEVER content or a case id
    (R3-2). Values must respect the Converse charset / length limits."""
    core = load("benefits_core")
    seen = {}

    class _Spy(_FakeBedrock):
        def converse(self, **kw):
            seen.update(kw)
            return super().converse(**kw)
    monkeypatch.setattr(core.boto3, "client", lambda *a, **k: _Spy())
    monkeypatch.setenv("CASE_TABLE", "ben-test-case-store")
    import case_store
    monkeypatch.setattr(case_store, "put_case", lambda text, kind="application", case_id="": "case-notice-1")
    import telemetry
    monkeypatch.setattr(telemetry, "current", lambda: {"trace_id": "6a99b48df6fc6e20d82d074efa877cbd",
                                                       "execution_arn": "arn:aws:states:us-east-1:111122223333:execution:wf:x-1",
                                                       "case_id": "CASE-SECRET-1", "request_id": "req-1"})
    monkeypatch.setattr(core, "_metered_tenant", lambda: "pha-a")
    core.handler({"sanitized_ref": make_sanitized_ref(CASE), "case": CASE, "deidentified": True}, None)
    meta = seen.get("requestMetadata")
    assert meta and meta["tenant"] == "pha-a" and meta["component"] == "draft_notice"
    assert meta["trace_id"] == "6a99b48df6fc6e20d82d074efa877cbd" and meta["execution_arn"].endswith(":execution:wf:x-1")
    assert "case_id" not in meta and "CASE-SECRET-1" not in json.dumps(meta), "no case id / content in requestMetadata"
    assert len(meta) <= 16 and all(len(k) <= 256 and len(v) <= 256 and core._META_OK.search(v) is None for k, v in meta.items())


# --- #190: contextual grounding enforced end-to-end on the drafter -----------------------------------

def test_draft_grounds_core_and_appends_boilerplate_when_guardrail_bound(monkeypatch):
    """#190: with a guardrail bound, the model is asked for ONLY the grounded factual core (case tagged
    grounding_source + a query, via guardContent, so the CONTEXTUAL GROUNDING filter scores the model's
    factual claims); the fixed notice boilerplate is appended DETERMINISTICALLY after the call, so a
    legitimate notice is never blocked by boilerplate the grounding source doesn't contain."""
    core = load("benefits_core")
    seen, stored = {}, {}

    class _Spy(_FakeBedrock):
        def converse(self, **kw):
            seen.update(kw)
            return super().converse(**kw)
    monkeypatch.setattr(core.boto3, "client", lambda *a, **k: _Spy())
    monkeypatch.setattr(core, "GUARDRAIL_ID", "gr-abc123")   # module constant, set at import
    monkeypatch.setattr(core, "GUARDRAIL_VERSION", "1")
    monkeypatch.setenv("CASE_TABLE", "ben-test-case-store")
    import case_store
    monkeypatch.setattr(case_store, "put_case",
                        lambda text, kind="application", case_id="": (stored.update(text=text), "case-notice-190")[1])
    r = core.handler({"sanitized_ref": make_sanitized_ref(CASE), "case": CASE, "deidentified": True,
                      "determination": DETERMINATION}, None)

    # the guardrail is bound on the Converse call, on the PINNED enforced version
    # L17: trace enabled so a blocked draft's assessment (filter + score) lands in the model-invocation log
    assert seen.get("guardrailConfig") == {"guardrailIdentifier": "gr-abc123", "guardrailVersion": "1", "trace": "enabled"}
    # grounded-core system prompt, not the full-notice system prompt
    assert seen["system"] == [{"text": core._SYSTEM_GROUNDED_CORE}]
    # the case is the grounding_source and a query is present -> grounding scores the model's claims
    quals = [q for block in seen["messages"][0]["content"] for q in block.get("guardContent", {}).get("text", {}).get("qualifiers", [])]
    assert "grounding_source" in quals and "query" in quals
    assert CASE in json.dumps(seen["messages"][0]["content"]), "the de-identified case must be the grounding source"
    # L14: the engine's determination is IN the grounding source (allowlisted fields only), so a faithful
    # core is groundable; a caller-supplied free-text field outside the allowlist never reaches the source
    src = [b["guardContent"]["text"]["text"] for b in seen["messages"][0]["content"]
           if "grounding_source" in b.get("guardContent", {}).get("text", {}).get("qualifiers", [])][0]
    assert "determination=ELIGIBLE" in src and "processing_clock=EXPEDITED" in src and "reason=gross monthly income" in src
    assert "SMUGGLED" not in src
    # the boilerplate was appended deterministically (outside the model / grounding scope)
    assert stored["text"].endswith(core._NOTICE_BOILERPLATE)
    assert stored["text"].startswith(NOTICE), "the grounded core precedes the fixed boilerplate"
    assert r.get("notice_ref") == "case-notice-190" and r.get("guardrail_applied") is True


def test_draft_fail_closed_on_guardrail_intervention(monkeypatch):
    """#190/#166: ANY guardrail intervention on the draft is fail-closed - no notice_ref is minted, even
    when the guardrail substitutes a non-empty blocked message. A hallucinated/ungrounded determination
    is blocked here."""
    core = load("benefits_core")

    class _Blocked(_FakeBedrock):
        def converse(self, **kw):
            return {"output": {"message": {"content": [{"text": "Sorry, the model cannot assist."}]}},
                    "stopReason": "guardrail_intervened"}
    monkeypatch.setattr(core.boto3, "client", lambda *a, **k: _Blocked())
    monkeypatch.setattr(core, "GUARDRAIL_ID", "gr-abc123")
    monkeypatch.setattr(core, "GUARDRAIL_VERSION", "1")
    monkeypatch.setenv("CASE_TABLE", "ben-test-case-store")
    import case_store
    minted = {"called": False}
    monkeypatch.setattr(case_store, "put_case",
                        lambda *a, **k: minted.__setitem__("called", True) or "case-should-not-happen")
    r = core.handler({"sanitized_ref": make_sanitized_ref(CASE), "case": CASE, "deidentified": True,
                      "determination": DETERMINATION}, None)

    assert r.get("guardrail") == "BLOCKED" and r.get("drafted_by") is None
    assert "notice_ref" not in r and "notice" not in r
    assert minted["called"] is False, "a blocked draft must never mint a notice_ref"


def test_draft_refuses_without_the_engine_determination_when_guardrail_bound(monkeypatch):
    """L14 (full-portfolio gate attempt 3, 2026-09-06): the grounded-core drafter can only state a
    determination present in its grounding source, so the deterministic engine's output is a REQUIRED
    input under a guardrail. Without it the drafter refuses fail-closed BEFORE any model call (no spend,
    no notice_ref) instead of producing a draft that contextual grounding would block every time."""
    core = load("benefits_core")
    called = {"converse": False}

    class _Never(_FakeBedrock):
        def converse(self, **kw):
            called["converse"] = True
            return super().converse(**kw)
    monkeypatch.setattr(core.boto3, "client", lambda *a, **k: _Never())
    monkeypatch.setattr(core, "GUARDRAIL_ID", "gr-abc123")
    monkeypatch.setattr(core, "GUARDRAIL_VERSION", "1")
    monkeypatch.setenv("CASE_TABLE", "ben-test-case-store")
    r = core.handler({"sanitized_ref": make_sanitized_ref(CASE), "case": CASE, "deidentified": True}, None)
    assert r.get("drafted_by") is None and r.get("determination_present") is False
    assert "determination required" in r.get("error", "")
    assert "notice_ref" not in r and called["converse"] is False, "no model spend without the determination"
    # the workflow passes the assessment output with the signed ref (the production path, not a proof artifact)
    import pathlib
    wf = (pathlib.Path(__file__).resolve().parents[1] / "cdk" / "ben_stacks" / "workflow_stack.py").read_text(encoding="utf-8")
    assert '"determination.$": "$.assessment.out"' in wf
    # and the gateway schema requires it, so the runtime agent must pass it too
    import yaml
    m = yaml.safe_load((pathlib.Path(__file__).resolve().parents[1] / "agents" / "benefits-eligibility" / "manifest.yaml").read_text(encoding="utf-8"))
    tool = [t for tg in m["tools"] for t in tg.get("mcp_tools", []) if t["name"] == "draft_notice"][0]
    assert "determination" in tool["input"] and "determination" in tool["required"]
