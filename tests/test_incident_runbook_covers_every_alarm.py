"""OBS-6: every deployed alarm must have a runbook entry, or CI fails.

An alarm with no documented first action is a notification, not a control. Runbooks rot because
nothing checks them - someone adds an alarm, the page is not updated, and six months later an
operator is paged by a name that appears nowhere. This test is the thing that checks.

It reads the alarm names out of the SYNTHESIZED TEMPLATE (not the source - see the header of
tests/test_observability_operability.py for why that distinction cost us a wrong number in a
partner brief) and asserts each one is documented in docs/ops/INCIDENT-RUNBOOK.md.

Budget alarms are per-tenant, so the runbook documents them by pattern (`budget-*-UsdUsedPct-85`)
and this test expands `*`. Everything else must be named literally.
"""
import json
import pathlib
import re
import sys

import pytest

aws_cdk = pytest.importorskip("aws_cdk")
from aws_cdk.assertions import Template  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cdk"))
sys.path.insert(0, str(ROOT / "tools"))

RUNBOOK = ROOT / "docs" / "ops" / "INCIDENT-RUNBOOK.md"
PREFIX = "ben-rb"


def _alarm_and_composite_names():
    from app import stage_lambda_bundle
    from ben_stacks.compute_stack import ComputeStack
    from ben_stacks.data_stack import DataStack
    from ben_stacks.lineage_stack import LineageStack
    from ben_stacks.observability_stack import ObservabilityStack
    from ben_stacks.workflow_stack import WorkflowStack

    prices = json.dumps({"price_version": "rb",
                         "models": {"anthropic.claude-sonnet-4-5": {"input_per_m": 3, "output_per_m": 15}}})
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    data = DataStack(app, "d", prefix=PREFIX, retention_profile="sandbox-demo")
    compute = ComputeStack(app, "c", prefix=PREFIX, asset_dir=asset, data=data, multitenant=True,
                           budget={"monthly_token_cap": 5000000, "cap_behavior": "hard",
                                   "monthly_usd": 25.5, "prices_json": prices})
    workflow = WorkflowStack(app, "w", prefix=PREFIX, compute=compute, data=data, multitenant=True)
    lineage = LineageStack(app, "l", prefix=PREFIX)
    obs = ObservabilityStack(app, "o", prefix=PREFIX, compute=compute, workflow=workflow, data=data,
                             tenants=("sp-a", "sp-b"), budget_usd=25.5, lineage=lineage,
                             runtime_role_name="AmazonBedrockAgentCoreSDKRuntime-rb")
    res = Template.from_stack(obs).to_json()["Resources"]
    names = []
    for v in res.values():
        if v["Type"] in ("AWS::CloudWatch::Alarm", "AWS::CloudWatch::CompositeAlarm"):
            n = v["Properties"].get("AlarmName")
            if isinstance(n, str):
                names.append(n)
    return sorted(names)


NAMES = _alarm_and_composite_names()
SUFFIXES = sorted(n[len(PREFIX) + 1:] for n in NAMES)
TEXT = RUNBOOK.read_text(encoding="utf-8") if RUNBOOK.is_file() else ""
# Entries are written as inline code: `workflow-failed`, `budget-*-UsdUsedPct-85`
DOCUMENTED = set(re.findall(r"`([a-zA-Z0-9*\-]+)`", TEXT))


def _is_documented(suffix):
    if suffix in DOCUMENTED:
        return True
    for entry in DOCUMENTED:
        # `.+` not `[^-]+`: tenant ids contain hyphens (`sp-a`), so the stricter class matched
        # nothing and every budget alarm read as undocumented.
        #
        # And a pattern must carry real literal text. The runbook explains its own notation with a
        # bare `*` in prose, which this scraper picked up as an entry - as the regex `.+` it then
        # matched EVERY alarm name and the coverage check passed vacuously. It was caught by
        # test_the_coverage_check_can_fail, which is the entire argument for writing that test.
        if "*" not in entry:
            continue
        if len(entry.replace("*", "").strip("-")) < 4:
            continue
        if re.fullmatch(entry.replace("*", ".+"), suffix):
            return True
    return False


def test_the_runbook_exists():
    assert RUNBOOK.is_file(), "%s is missing; every alarm needs a documented first action" % RUNBOOK


def test_the_fixture_actually_produced_alarms():
    """Guard on the guard: if synthesis produced nothing, every assertion below is vacuous."""
    assert len(NAMES) >= 20, "only %d alarms synthesized - the fixture is not exercising the stack" % len(NAMES)
    assert any(s.startswith("severity-") for s in SUFFIXES), "no composite alarms in the fixture"


def test_every_alarm_has_a_runbook_entry():
    missing = sorted(s for s in SUFFIXES if not _is_documented(s))
    assert not missing, (
        "%d alarm(s) deploy with no entry in docs/ops/INCIDENT-RUNBOOK.md. An alarm with no "
        "documented first action is a notification, not a control. Add an entry for: %s"
        % (len(missing), missing))


def test_every_tier_is_documented():
    for tier in ("severity-p1", "severity-p2", "severity-p3"):
        assert _is_documented(tier), "%s has no runbook entry" % tier


def test_the_runbook_states_what_it_does_not_cover():
    """A runbook that implies complete coverage is worse than one that names its holes."""
    low = TEXT.lower()
    for phrase in ("dr exercise", "on-call", "canary"):
        assert phrase in low, "the runbook does not disclose the missing %r capability" % phrase


def test_the_coverage_check_can_fail():
    """If _is_documented() returned True for anything, this whole file would pass vacuously."""
    assert not _is_documented("an-alarm-that-does-not-exist")
    assert not _is_documented("workflow-failed-nonsense")
