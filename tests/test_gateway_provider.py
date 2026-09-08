"""AgentCore attachment provider (cdk/gateway_provider/handler.py) - the custom resource that creates the
policy engine, gateway, targets and Cedar policies. Live-found 2026-09-05 (Tier-1 gate, attempt 6): a
policy never reached ACTIVE because the engine validated its tool ACTION against targets whose tool
schemas were not yet visible ("unrecognized action ..."), and the provider's bare wait said only
"resource did not reach ACTIVE". These tests pin the hardened behaviour: fail FAST with the engine's
reasons on a real validation error, retry ONLY the propagation race, and name the resource in every wait
failure."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "cdk" / "gateway_provider"))
import handler  # noqa: E402


class _CC:
    """Fake bedrock-agentcore-control: statuses scripted per policy name (list consumed per get)."""
    def __init__(self, script):
        self.script, self.created, self.deleted, self.n = script, [], [], 0

    def create_policy(self, policyEngineId, name, definition, validationMode):
        self.n += 1
        pid = "%s-%d" % (name, self.n)
        self.created.append(pid)
        return {"policyId": pid}

    def get_policy(self, policyEngineId, policyId):
        name = policyId.rsplit("-", 1)[0]
        seq = self.script[name]
        status, reasons = seq.pop(0) if len(seq) > 1 else seq[0]
        return {"status": status, "statusReasons": reasons}

    def delete_policy(self, policyEngineId, policyId):
        self.deleted.append(policyId)


def test_the_transient_is_not_retried_here_because_the_name_cannot_be_reused(monkeypatch):
    """This test used to assert the opposite, and the opposite was impossible.

    It required _create_policy_active to delete a CREATE_FAILED policy and re-create it under the
    same name. Three live deploys on 2026-09-08 proved that cannot work: AgentCore reserves a
    deleted policy's name for longer than a deploy can wait (measured >170s, with list_policies
    already reporting the engine empty), so the re-create is refused with ConflictException and the
    stack rolls back. The test passed for weeks because its double released names instantly.

    The race is now waited out BEFORE any real policy is created, by _wait_tool_actions_visible
    using disposable uniquely-named probes. A real policy is created exactly once, and a
    CREATE_FAILED here is reported rather than papered over.
    """
    monkeypatch.setattr(handler.time, "sleep", lambda s: None)
    cc = _CC({"budget_before_draft": [("CREATING", []),
                                      ("CREATE_FAILED", ["unrecognized action `AgentCore::Action::\"ben-core___draft_notice\"`"])]})
    with pytest.raises(RuntimeError) as ei:
        handler._create_policy_active(cc, "eng", "budget_before_draft", "forbid(...)", "FAIL_ON_ANY_FINDINGS")
    assert "budget_before_draft" in str(ei.value) and "unrecognized action" in str(ei.value)
    assert len(cc.created) == 1, "it must NOT create a second policy under a name it cannot reuse"


def test_real_validation_error_fails_fast_with_reasons(monkeypatch):
    monkeypatch.setattr(handler.time, "sleep", lambda s: None)
    cc = _CC({"bad_policy": [("CREATE_FAILED", ["unexpected token `}` at line 3"])]})
    with pytest.raises(RuntimeError) as ei:
        handler._create_policy_active(cc, "eng", "bad_policy", "forbid(", "FAIL_ON_ANY_FINDINGS")
    assert "bad_policy" in str(ei.value) and "unexpected token" in str(ei.value)
    assert len(cc.created) == 1, "a genuine validation error must not be retried"


def test_persistent_propagation_failure_gives_up_with_reasons(monkeypatch):
    """Same intent as before - the engine's reasons must reach the stack event - but with one
    create. The `attempts=3` parameter is gone with the retry it drove."""
    monkeypatch.setattr(handler.time, "sleep", lambda s: None)
    cc = _CC({"p": [("CREATE_FAILED", ["unrecognized action `X`"])]})
    with pytest.raises(RuntimeError) as ei:
        handler._create_policy_active(cc, "eng", "p", "forbid(...)", "FAIL_ON_ANY_FINDINGS")
    assert len(cc.created) == 1 and "unrecognized action" in str(ei.value)


def test_wait_fails_fast_on_terminal_status_and_names_the_resource(monkeypatch):
    monkeypatch.setattr(handler.time, "sleep", lambda s: None)
    seq = iter(["CREATING", "FAILED", "READY"])
    with pytest.raises(RuntimeError) as ei:
        handler._wait(lambda: next(seq), "READY", label="gateway target t-1")
    assert "gateway target t-1 reached FAILED" in str(ei.value)
    seq2 = iter(["CREATING"] * 5)
    with pytest.raises(RuntimeError) as ei2:
        handler._wait(lambda: next(seq2), "READY", tries=3, label="policy engine")
    assert "policy engine did not reach READY (last status CREATING)" in str(ei2.value)
