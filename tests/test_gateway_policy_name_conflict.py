"""The AgentCore gateway custom resource must survive its own policy-delete propagation lag.

Live-found 2026-09-08, full-portfolio re-gate of main. ben-fp2-gateway rolled back with
ConflictException("Policy with the same name already exists"), raised by create_policy inside
_create_policy_active's retry loop. The sequence:

  1. create_policy(name="ben_authz_...")            -> policyId p1
  2. p1 reaches CREATE_FAILED, reasons "unrecognized action ..."   (the documented transient:
     the Cedar engine validates tool ACTIONS against the gateway targets' schemas, and right
     after the targets report READY the validator can still see an empty tool set)
  3. delete_policy(p1)                              -> returns immediately
  4. sleep 20s, retry: create_policy(same name)     -> ConflictException

delete_policy returns before the NAME is released. ConflictException is not a validation
failure, so nothing in the loop caught it and it escaped to fail the custom resource. The one
transient the retry exists to survive was the one case it could not survive.

These tests model the lag explicitly (a deleted name stays visible for N list_policies calls)
because that lag is the whole defect. A fake that frees the name instantly cannot fail, and a
test that cannot fail is the thing this repository keeps finding in itself.
"""
import importlib.util
import pathlib
import sys

import pytest

HANDLER = pathlib.Path(__file__).resolve().parents[1] / "cdk" / "gateway_provider" / "handler.py"


def _load():
    spec = importlib.util.spec_from_file_location("gw_handler_under_test", HANDLER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def handler(monkeypatch):
    mod = _load()
    # The retry sleeps 20s and 40s between attempts; the name-free wait sleeps 3s per poll.
    # Real time is not what is under test.
    monkeypatch.setattr(mod.time, "sleep", lambda *_a, **_k: None)
    return mod


class Conflict(Exception):
    """Shaped like botocore's ClientError: the code is read off .response."""

    def __init__(self):
        super().__init__("An error occurred (ConflictException) when calling the CreatePolicy "
                         "operation: Policy with the same name already exists")
        self.response = {"Error": {"Code": "ConflictException"}}


class Throttled(Exception):
    def __init__(self):
        super().__init__("throttled")
        self.response = {"Error": {"Code": "ThrottlingException"}}


class FakeCC:
    """Minimal AgentCore control-plane double with a DELETE PROPAGATION LAG.

    A deleted policy's name stays visible to list_policies -- and still collides in
    create_policy -- for `linger` further list_policies calls. That is the production
    behaviour the live rollback demonstrated.
    """

    def __init__(self, statuses=("ACTIVE",), linger=2, create_error=None, ghosts_visible=True):
        self.statuses = list(statuses)
        self.linger = linger
        self.create_error = create_error
        # ghosts_visible=False is the SECOND live failure of 2026-09-08: the deleted policy has
        # already vanished from list_policies while create_policy still refuses the name. Any
        # implementation that asks list_policies whether the name is free is wrong here.
        self.ghosts_visible = ghosts_visible
        self.live = {}          # policyId -> name
        self.ghosts = {}        # name -> remaining list_policies calls
        self.pid_status = {}
        self.creates = 0
        self.create_calls = 0
        self.conflicts_raised = 0

    def _names_taken(self):
        return set(self.live.values()) | set(self.ghosts)

    def create_policy(self, policyEngineId, name, definition, validationMode):
        self.create_calls += 1
        if self.create_error is not None:
            raise self.create_error
        if name in self._names_taken():
            self.conflicts_raised += 1
            self._age_ghosts()   # time passes on this call too, not only on list_policies
            raise Conflict()
        self.creates += 1
        pid = "p%d" % self.creates
        self.live[pid] = name
        self.pid_status[pid] = self.statuses.pop(0) if self.statuses else "ACTIVE"
        return {"policyId": pid}

    def get_policy(self, policyEngineId, policyId):
        st = self.pid_status.get(policyId, "ACTIVE")
        reasons = ["unrecognized action"] if st == "CREATE_FAILED" else []
        return {"status": st, "statusReasons": reasons}

    def delete_policy(self, policyEngineId, policyId):
        name = self.live.pop(policyId, None)
        if name is not None and self.linger > 0:
            self.ghosts[name] = self.linger

    def _age_ghosts(self):
        for nm, left in list(self.ghosts.items()):
            if left - 1 <= 0:
                del self.ghosts[nm]
            else:
                self.ghosts[nm] = left - 1

    def list_policies(self, policyEngineId):
        out = [{"policyId": pid, "name": nm} for pid, nm in self.live.items()]
        if self.ghosts_visible:
            out += [{"policyId": "ghost-%s" % nm, "name": nm} for nm in self.ghosts]
        self._age_ghosts()
        return {"policies": out}


# --- the lag is real -------------------------------------------------------------------

def test_fake_reproduces_the_conflict_without_the_fix(handler):
    """Guard on the guard: a raw create-delete-create MUST collide in this double.

    If this passes trivially the other tests prove nothing.
    """
    cc = FakeCC(linger=3)
    pid = cc.create_policy("e", "pol", {}, "FAIL_ON_ANY_FINDINGS")["policyId"]
    cc.delete_policy("e", pid)
    with pytest.raises(Conflict):
        cc.create_policy("e", "pol", {}, "FAIL_ON_ANY_FINDINGS")


# --- _wait_policy_name_free ------------------------------------------------------------

def test_wait_returns_true_once_the_name_is_released(handler):
    cc = FakeCC(linger=3)
    pid = cc.create_policy("e", "pol", {}, "M")["policyId"]
    cc.delete_policy("e", pid)
    assert handler._wait_policy_name_free(cc, "e", "pol") is True
    assert "pol" not in cc._names_taken()


def test_wait_returns_false_rather_than_hanging_when_the_name_never_frees(handler):
    cc = FakeCC(linger=10 ** 9)
    pid = cc.create_policy("e", "pol", {}, "M")["policyId"]
    cc.delete_policy("e", pid)
    assert handler._wait_policy_name_free(cc, "e", "pol", timeout=0) is False


def test_wait_is_not_confused_by_a_different_policy_name(handler):
    cc = FakeCC(linger=5)
    cc.create_policy("e", "other", {}, "M")
    assert handler._wait_policy_name_free(cc, "e", "pol") is True


# --- _create_policy_claiming_name ------------------------------------------------------

def test_claiming_name_succeeds_when_nothing_holds_it(handler):
    cc = FakeCC()
    assert handler._create_policy_claiming_name(cc, "e", "pol", "permit(...);", "M") == "p1"


def test_claiming_name_clears_a_lingering_holder_and_succeeds(handler):
    cc = FakeCC(linger=3)
    pid = cc.create_policy("e", "pol", {}, "M")["policyId"]
    cc.delete_policy("e", pid)
    got = handler._create_policy_claiming_name(cc, "e", "pol", "permit(...);", "M")
    assert got == "p2"
    assert cc.conflicts_raised >= 1, "the conflict must actually have been hit and recovered"
    assert cc.creates == 2, "exactly one successful re-create, not a storm of them"


def test_claiming_name_clears_residue_from_a_previous_run(handler):
    """Not a ghost: a real, live policy of the same name left by an earlier deploy."""
    cc = FakeCC(linger=0)
    cc.create_policy("e", "pol", {}, "M")
    got = handler._create_policy_claiming_name(cc, "e", "pol", "permit(...);", "M")
    assert got == "p2"
    assert list(cc.live.values()) == ["pol"], "exactly one policy of that name must remain"


def test_claiming_name_gives_up_with_a_bounded_budget_rather_than_spinning(handler):
    """A name that never frees must RAISE after a bounded budget, not loop forever.

    An unbounded retry inside a CloudFormation custom resource is a hung stack, which is worse
    than a failed one: it cannot be diagnosed from the stack events and it blocks teardown.
    """
    cc = FakeCC(linger=10 ** 9)
    cc.create_policy("e", "pol", {}, "M")
    with pytest.raises(RuntimeError, match="still refused as a duplicate after 170s"):
        handler._create_policy_claiming_name(cc, "e", "pol", "permit(...);", "M")
    assert cc.create_calls == 8, "one live create, one initial attempt, then six bounded retries"


def test_a_non_conflict_error_is_not_swallowed(handler):
    """Only ConflictException means 'the name is taken'. Everything else must surface."""
    cc = FakeCC(create_error=Throttled())
    with pytest.raises(Throttled):
        handler._create_policy_claiming_name(cc, "e", "pol", "permit(...);", "M")


# --- the whole retry loop, which is what actually broke ---------------------------------

def test_retry_survives_the_transient_that_it_exists_to_survive(handler):
    """attempt 1 CREATE_FAILED('unrecognized action') -> delete -> attempt 2 must reach ACTIVE.

    This is the exact live sequence. Before the fix it raised ConflictException out of the loop
    and rolled back ben-fp2-gateway.
    """
    cc = FakeCC(statuses=["CREATE_FAILED", "ACTIVE"], linger=3)
    pid = handler._create_policy_active(cc, "e", "pol", "permit(...);", "FAIL_ON_ANY_FINDINGS")
    assert cc.pid_status[pid] == "ACTIVE"
    assert cc.creates == 2, "it must have genuinely re-created, not returned the failed policy"


def test_a_real_validation_failure_still_raises_with_the_engine_reasons(handler):
    """The fix must not turn a genuine Cedar validation error into an infinite retry."""
    cc = FakeCC(statuses=["CREATE_FAILED"], linger=1)  # frees after one list call; no spin

    def get_policy(policyEngineId, policyId):
        return {"status": "CREATE_FAILED", "statusReasons": ["undeclared entity type Foo::Bar"]}

    cc.get_policy = get_policy
    with pytest.raises(RuntimeError, match="did not reach ACTIVE"):
        handler._create_policy_active(cc, "e", "pol", "permit(...);", "FAIL_ON_ANY_FINDINGS")
    assert cc.creates == 1, "a non-transient failure must not be retried"


def test_the_failure_path_waits_on_the_name_not_the_id(handler, monkeypatch):
    """Regression guard for the specific omission that caused the rollback.

    The delete inside the retry loop must be followed by a wait keyed on the NAME. Asserting the
    call happens -- rather than only that the happy path passes -- is the L60 rule: a control is
    only proven when its absence is observable.
    """
    seen = []
    real = handler._wait_policy_name_free
    monkeypatch.setattr(handler, "_wait_policy_name_free",
                        lambda cc, eng, name, **kw: (seen.append(name), real(cc, eng, name, **kw))[1])
    cc = FakeCC(statuses=["CREATE_FAILED", "ACTIVE"], linger=3)
    handler._create_policy_active(cc, "e", "pol", "permit(...);", "FAIL_ON_ANY_FINDINGS")
    assert "pol" in seen, "the retry deleted a policy without waiting for its NAME to free"


# --- the SECOND live failure: invisible to list_policies, still refused by create_policy -----

def test_a_name_invisible_to_list_policies_can_still_be_refused_by_create(handler):
    """Guard on the guard, for failure #2. The double must reproduce the asymmetry.

    2026-09-08, second re-gate attempt: the deleted policy had already vanished from
    list_policies and create_policy refused the name anyway. If this test stops holding, every
    assertion below about the authoritative-retry design is vacuous.
    """
    cc = FakeCC(linger=3, ghosts_visible=False)
    pid = cc.create_policy("e", "pol", {}, "M")["policyId"]
    cc.delete_policy("e", pid)
    assert handler._policy_ids_by_name(cc, "e", "pol") == [], "the list view must look clean"
    with pytest.raises(Conflict):
        cc.create_policy("e", "pol", {}, "M")


def test_the_advisory_wait_is_fooled_by_an_invisible_holder(handler):
    """_wait_policy_name_free reports True here and is WRONG. That is why it is advisory.

    Pinning the limitation keeps someone from promoting this function back into a precondition
    for success, which is exactly the mistake that produced the second rollback.
    """
    cc = FakeCC(linger=10 ** 9, ghosts_visible=False)
    pid = cc.create_policy("e", "pol", {}, "M")["policyId"]
    cc.delete_policy("e", pid)
    assert handler._wait_policy_name_free(cc, "e", "pol") is True
    with pytest.raises(Conflict):
        cc.create_policy("e", "pol", {}, "M")


def test_claiming_name_succeeds_against_an_invisible_holder(handler):
    """The real fix: retry the AUTHORITATIVE call, do not ask the list view for permission.

    linger=6 is measured, not arbitrary. The list-based implementation that shipped and rolled the
    stack back gets about three chances to age the holder out (its conflicting create, its
    _policy_ids_by_name lookup, its _wait_policy_name_free poll) before its single re-create, so
    at linger<=4 it survives and this test would prove nothing. Both implementations were run
    against this double across linger 4..8: 6 is the value where the list-based one fails and the
    retrying one still passes on BOTH this path and the full-loop path below. At 8 the holder
    outlives even the bounded budget on this path, which is the give-up case covered separately.
    """
    cc = FakeCC(linger=6, ghosts_visible=False)
    pid = cc.create_policy("e", "pol", {}, "M")["policyId"]
    cc.delete_policy("e", pid)
    got = handler._create_policy_claiming_name(cc, "e", "pol", "permit(...);", "M")
    assert got == "p2"
    assert cc.conflicts_raised >= 1, "the conflict must have been hit and ridden out"


def test_full_retry_loop_survives_an_invisible_holder(handler):
    """End to end: the exact live sequence, with the list view lying about availability."""
    cc = FakeCC(statuses=["CREATE_FAILED", "ACTIVE"], linger=6, ghosts_visible=False)
    pid = handler._create_policy_active(cc, "e", "pol", "permit(...);", "FAIL_ON_ANY_FINDINGS")
    assert cc.pid_status[pid] == "ACTIVE"


def test_retries_stop_at_the_first_non_conflict_error(handler):
    """A throttle or access-denied during the backoff must surface immediately, not burn 170s."""
    cc = FakeCC(linger=10 ** 9)
    cc.create_policy("e", "pol", {}, "M")

    calls = {"n": 0}
    original = cc.create_policy

    def flaky(policyEngineId, name, definition, validationMode):
        calls["n"] += 1
        if calls["n"] >= 3:
            raise Throttled()
        return original(policyEngineId, name, definition, validationMode)

    cc.create_policy = flaky
    with pytest.raises(Throttled):
        handler._create_policy_claiming_name(cc, "e", "pol", "permit(...);", "M")
    assert calls["n"] == 3, "it must stop at the throttle, not keep retrying"
