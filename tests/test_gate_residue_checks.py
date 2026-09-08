"""The gate must verify "from zero" rather than assume it, and must not judge a teardown too early.

Both of these come straight out of the four failed re-gates of main on 2026-09-08.

  * `teardown_zero_stack_residue` reported stacks_clean=False on ALL FOUR teardowns and was wrong
    every time: it asked CloudFormation while the stacks were still DELETE_IN_PROGRESS, and they
    were gone moments later. A check that fails because it asked too early trains people to ignore
    it, which is worse than not having it.

  * Nothing checked for AgentCore residue at either end. Gateways, policy engines and agent runtimes
    live outside CloudFormation and survive their stack. Four orphaned READY gateways - live MCP
    URLs whose IAM roles belonged to deleted stacks - were removed by hand that day, and an orphaned
    POLICY ENGINE is worse than a stray cost: the next deploy adopts it BY NAME and inherits its
    policies, and a policy name is not reusable once taken (measured: still refused 170 seconds
    after deletion, with list_policies already reporting the engine empty).
"""
import importlib.util
import pathlib
import sys

import pytest

GATE = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "full_portfolio_gate.py"


@pytest.fixture(scope="module")
def gate():
    spec = importlib.util.spec_from_file_location("full_portfolio_gate_under_test", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- residue detection

class FakeACC:
    def __init__(self, gateways=(), engines=(), runtimes=(), fail=None):
        self._gw, self._en, self._rt, self._fail = list(gateways), list(engines), list(runtimes), fail

    def list_gateways(self):
        if self._fail == "gateways":
            raise RuntimeError("service unavailable")
        return {"items": [{"name": n, "gatewayId": n + "-id"} for n in self._gw]}

    def list_policy_engines(self):
        if self._fail == "engines":
            raise RuntimeError("service unavailable")
        return {"policyEngines": [{"name": n, "policyEngineId": n + "-id"} for n in self._en]}

    def list_agent_runtimes(self):
        return {"agentRuntimes": [{"agentRuntimeName": n, "agentRuntimeId": n + "-id"} for n in self._rt]}


class FakeSession:
    def __init__(self, acc):
        self._acc = acc

    def client(self, name, region_name=None):
        assert name == "bedrock-agentcore-control"
        return self._acc


def test_a_clean_account_reports_clean(gate):
    found = gate.agentcore_residue(FakeSession(FakeACC()), "ben-fp2", "us-east-1")
    assert gate.agentcore_residue_is_clean(found)


def test_an_orphaned_gateway_is_found(gate):
    """The exact residue removed by hand four times on 2026-09-08."""
    found = gate.agentcore_residue(FakeSession(FakeACC(gateways=["ben-fp2-ben-gw"])), "ben-fp2", "us-east-1")
    assert not gate.agentcore_residue_is_clean(found)
    assert found["gateways"] == [{"name": "ben-fp2-ben-gw", "id": "ben-fp2-ben-gw-id"}]


def test_an_orphaned_policy_engine_is_found_despite_underscore_naming(gate):
    """The engine is named with underscores where the gateway uses hyphens.

    Matching only the hyphenated prefix would have missed the single most dangerous piece of
    residue, which is the one the next deploy silently adopts.
    """
    found = gate.agentcore_residue(FakeSession(FakeACC(engines=["ben_fp2_ben_authz"])), "ben-fp2", "us-east-1")
    assert not gate.agentcore_residue_is_clean(found)
    assert found["policy_engines"][0]["name"] == "ben_fp2_ben_authz"


def test_another_environments_residue_is_not_ours(gate):
    """pv-fp-* residue predates this environment and must not fail ben-fp2's gate."""
    acc = FakeACC(gateways=["pv-fp-pv-gw"], engines=["pv_fp_pv_authz"])
    assert gate.agentcore_residue_is_clean(gate.agentcore_residue(FakeSession(acc), "ben-fp2", "us-east-1"))


def test_a_read_failure_is_not_clean(gate):
    """"We could not look" must never be recorded as "there was nothing there".

    This is the L41/L44b failure mode - a check that treats an unreadable result as a pass.
    """
    found = gate.agentcore_residue(FakeSession(FakeACC(fail="engines")), "ben-fp2", "us-east-1")
    assert not gate.agentcore_residue_is_clean(found)
    assert str(found["policy_engines"]).startswith("ERROR RuntimeError")


# --------------------------------------------------------------------------- stack settle

class FakeCF:
    """describe_stacks that drains: the stacks disappear after a few polls, as CloudFormation does."""

    def __init__(self, sequence):
        self.sequence = list(sequence)
        self.calls = 0

    def describe_stacks(self):
        self.calls += 1
        names = self.sequence[min(self.calls - 1, len(self.sequence) - 1)]
        return {"Stacks": [{"StackName": n, "StackStatus": "DELETE_IN_PROGRESS"} for n in names]}


def test_settle_waits_out_delete_in_progress(gate, monkeypatch):
    """The four false failures: judged mid-DELETE, clean moments later."""
    monkeypatch.setattr(gate.time, "sleep", lambda *_a: None)
    cf = FakeCF([["ben-fp2-data", "ben-fp2-gateway"], ["ben-fp2-data"], []])
    clean, note = gate.wait_stacks_gone(cf, "ben-fp2")
    assert clean is True
    assert cf.calls == 3, "it must actually have waited rather than passing on the first look"


def test_settle_reports_failure_when_stacks_really_do_persist(gate, monkeypatch):
    """A genuine residue failure must stay a failure - the fix must not make the check unfailable."""
    monkeypatch.setattr(gate.time, "sleep", lambda *_a: None)
    cf = FakeCF([["ben-fp2-data"]])
    clean, note = gate.wait_stacks_gone(cf, "ben-fp2", timeout=0)
    assert clean is False
    assert "ben-fp2-data" in note


def test_settle_ignores_stacks_from_other_environments(gate, monkeypatch):
    monkeypatch.setattr(gate.time, "sleep", lambda *_a: None)
    cf = FakeCF([["pv-fp-data", "ben-demo-data"]])
    clean, _ = gate.wait_stacks_gone(cf, "ben-fp2", timeout=0)
    assert clean is True


def test_settle_treats_an_unlistable_account_as_not_clean(gate, monkeypatch):
    monkeypatch.setattr(gate.time, "sleep", lambda *_a: None)

    class Boom:
        def describe_stacks(self):
            raise RuntimeError("throttled")

    clean, note = gate.wait_stacks_gone(Boom(), "ben-fp2", timeout=0)
    assert clean is False and "could not list stacks" in note
