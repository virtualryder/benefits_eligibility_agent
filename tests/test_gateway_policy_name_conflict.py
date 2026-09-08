"""The gateway custom resource must create each Cedar policy exactly once, under its real name.

Three live failures on 2026-09-08, all on ben-fp2-gateway/AgentCoreAttachment, all while trying to
earn a tag for main. They are one story:

  1. The Cedar policy create has a documented transient: right after the gateway targets report
     READY, the policy validator can still see an empty tool set and rejects a policy that names a
     tool action with "unrecognized action". The handler rode this out by deleting the failed
     policy and re-creating it under the SAME name after 20s. delete_policy returns before the name
     is released, so the re-create was refused with ConflictException. That is not a validation
     failure, nothing caught it, and it escaped and rolled the stack back.

  2. Fix attempt: delete the holder, then wait on list_policies until the name stops appearing.
     Rolled back again, same message, from the second create. list_policies is NOT authoritative -
     the policy had already vanished from the list view and create_policy refused the name anyway.

  3. Fix attempt: retry create_policy itself with bounded backoff, since only it knows. Rolled back
     again: "policy name 'mask_before_assess' is still refused as a duplicate after 170s". AgentCore
     reserves a deleted policy's name for far longer than a deploy can wait.

The conclusion the third failure forced: a name that might need to be used twice cannot be a name we
care about. So the race is now waited out BEFORE any real policy is created, using disposable probe
policies with unique names, and each real policy is created exactly ONCE under the name it must have.

FakeCC therefore reserves deleted names PERMANENTLY. That is the behaviour that was actually
observed, and it is what makes these tests able to fail: every delete-and-retry design, including
both of my own, is refused by this double.
"""
import importlib.util
import pathlib
import sys

import pytest

HANDLER = pathlib.Path(__file__).resolve().parents[1] / "cdk" / "gateway_provider" / "handler.py"
GW_ARN = "arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"


def _load():
    spec = importlib.util.spec_from_file_location("gw_handler_under_test", HANDLER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def handler(monkeypatch):
    mod = _load()
    monkeypatch.setattr(mod.time, "sleep", lambda *_a, **_k: None)
    return mod


class Conflict(Exception):
    """Shaped like botocore's ClientError: the code is read off .response."""

    def __init__(self):
        super().__init__("An error occurred (ConflictException) when calling the CreatePolicy "
                         "operation: Policy with the same name already exists")
        self.response = {"Error": {"Code": "ConflictException"}}


class FakeCC:
    """AgentCore control-plane double whose deleted policy NAMES are never released.

    `unrecognized_until` is how many create_policy calls happen before the tool set becomes
    visible; until then any policy naming an action lands in CREATE_FAILED with the transient
    reason. Policies naming no action are never affected, which is what was observed live: four
    action-free policies went ACTIVE and the fifth, the first to name an action, did not.
    """

    def __init__(self, unrecognized_until=0):
        self.unrecognized_until = unrecognized_until
        self.live = {}            # policyId -> name
        self.retired = set()      # names that can never be used again
        self.pid_status = {}
        self.pid_reasons = {}
        self.creates = 0
        self.created_names = []

    def create_policy(self, policyEngineId, name, definition, validationMode):
        if name in self.retired or name in self.live.values():
            raise Conflict()
        self.creates += 1
        self.created_names.append(name)
        pid = "p%d" % self.creates
        self.live[pid] = name
        names_action = "AgentCore::Action::" in str(definition)
        if names_action and self.creates <= self.unrecognized_until:
            self.pid_status[pid] = "CREATE_FAILED"
            self.pid_reasons[pid] = ['unrecognized action Action::"assess-eligibility___assess_eligibility"']
        else:
            self.pid_status[pid] = "ACTIVE"
            self.pid_reasons[pid] = []
        return {"policyId": pid}

    def get_policy(self, policyEngineId, policyId):
        return {"status": self.pid_status.get(policyId, "ACTIVE"),
                "statusReasons": self.pid_reasons.get(policyId, [])}

    def delete_policy(self, policyEngineId, policyId):
        name = self.live.pop(policyId, None)
        if name is not None:
            self.retired.add(name)      # the name is gone for good

    def list_policies(self, policyEngineId):
        return {"policies": [{"policyId": pid, "name": nm} for pid, nm in self.live.items()]}


MASK = ('forbid(principal, action == AgentCore::Action::"assess-eligibility___assess_eligibility", '
        'resource == AgentCore::Gateway::"%s") unless { context.input.deidentified == true };' % GW_ARN)
PERMIT = "permit(principal, action, resource is AgentCore::Gateway) when { true };"


# --- the double reproduces what AgentCore actually did ---------------------------------

def test_a_deleted_policy_name_is_never_reusable(handler):
    """Guard on the guard. This is the measured behaviour that broke three deploys.

    If this ever stops holding, every test below is proving nothing.
    """
    cc = FakeCC()
    pid = cc.create_policy("e", "pol", MASK, "M")["policyId"]
    cc.delete_policy("e", pid)
    assert cc.list_policies("e")["policies"] == [], "list_policies shows it gone..."
    with pytest.raises(Conflict):
        cc.create_policy("e", "pol", MASK, "M")   # ...and the name is still refused


# --- _actions_in -----------------------------------------------------------------------

def test_actions_in_finds_the_tool_actions_a_policy_names(handler):
    assert handler._actions_in(MASK) == ["assess-eligibility___assess_eligibility"]


def test_actions_in_is_empty_for_a_policy_that_names_no_action(handler):
    """These are the four that went ACTIVE live; they are not validated against the tool set."""
    assert handler._actions_in(PERMIT) == []


# --- _wait_tool_actions_visible --------------------------------------------------------

def test_probe_returns_true_once_the_tool_set_is_visible(handler):
    cc = FakeCC(unrecognized_until=3)
    assert handler._wait_tool_actions_visible(cc, "e", GW_ARN, "a___b") is True


def test_every_probe_uses_a_fresh_name(handler):
    """The property the whole design rests on.

    A probe may have to run many times, and a name used twice is a ConflictException. Reusing one
    is exactly the mistake that rolled the stack back three times.
    """
    cc = FakeCC(unrecognized_until=4)
    handler._wait_tool_actions_visible(cc, "e", GW_ARN, "a___b")
    assert len(cc.created_names) == len(set(cc.created_names)), "a probe name was reused"
    assert len(cc.created_names) >= 5, "the probe must actually have retried"


def test_probe_names_cannot_collide_with_a_real_policy(handler):
    cc = FakeCC(unrecognized_until=2)
    handler._wait_tool_actions_visible(cc, "e", GW_ARN, "a___b")
    for n in cc.created_names:
        assert n.startswith("aegis_toolset_probe_"), "probe names must be unmistakably disposable"


def test_probe_gives_up_within_its_budget(handler):
    """Never visible -> False, so the caller can refuse instead of burning the real names."""
    cc = FakeCC(unrecognized_until=10 ** 6)
    assert handler._wait_tool_actions_visible(cc, "e", GW_ARN, "a___b", timeout=0) is False


def test_probe_does_not_diagnose_failures_that_are_not_the_race(handler):
    """A different validation error is the real policy's to report, with its own reasons."""
    cc = FakeCC()

    def get_policy(policyEngineId, policyId):
        return {"status": "CREATE_FAILED", "statusReasons": ["undeclared entity type Foo::Bar"]}

    cc.get_policy = get_policy
    assert handler._wait_tool_actions_visible(cc, "e", GW_ARN, "a___b") is True


# --- _create_policy_active -------------------------------------------------------------

def test_a_real_policy_is_created_exactly_once(handler):
    """The core regression guard. Two creates under one name is the bug, in every variant."""
    cc = FakeCC()
    handler._create_policy_active(cc, "e", "mask_before_assess", MASK, "IGNORE_ALL_FINDINGS")
    assert cc.created_names == ["mask_before_assess"]


def test_a_failed_policy_raises_with_the_engine_reasons_instead_of_retrying(handler):
    """Once the probe has established the tool set is visible, a failure here is real.

    Retrying it under the same name is impossible, and papering over it is how the true reason
    stayed out of the stack events for three runs.
    """
    cc = FakeCC(unrecognized_until=1)
    with pytest.raises(RuntimeError, match="unrecognized action"):
        handler._create_policy_active(cc, "e", "mask_before_assess", MASK, "IGNORE_ALL_FINDINGS")
    assert cc.creates == 1, "it must NOT have tried a second time under a name it cannot reuse"


def test_the_raised_error_names_the_policy_and_the_status(handler):
    cc = FakeCC(unrecognized_until=1)
    with pytest.raises(RuntimeError) as err:
        handler._create_policy_active(cc, "e", "mask_before_assess", MASK, "IGNORE_ALL_FINDINGS")
    assert "mask_before_assess" in str(err.value)
    assert "CREATE_FAILED" in str(err.value)


# --- the two together, which is the live sequence ---------------------------------------

def test_probe_then_create_survives_the_transient_that_broke_three_deploys(handler):
    """Probe absorbs the race on disposable names; the real policy then creates once and sticks."""
    cc = FakeCC(unrecognized_until=4)
    assert handler._wait_tool_actions_visible(cc, "e", GW_ARN, "assess-eligibility___assess_eligibility")
    handler._create_policy_active(cc, "e", "mask_before_assess", MASK, "IGNORE_ALL_FINDINGS")
    assert "mask_before_assess" in cc.live.values()
    assert "mask_before_assess" not in cc.retired, "the real name was never burned"


def test_action_free_policies_never_needed_the_probe(handler):
    """Matches the live evidence: four action-free policies went ACTIVE before anything failed."""
    cc = FakeCC(unrecognized_until=10 ** 6)
    for name in ("amount_cap_overpayment", "budget_before_draft", "caseworker_permit"):
        handler._create_policy_active(cc, "e", name, PERMIT, "FAIL_ON_ANY_FINDINGS")
    assert cc.creates == 3
