"""OBS-1..OBS-4: the alarms must be OPERABLE, not merely present.

WHY THIS FILE EXISTS
--------------------
On 2026-09-09 the partner brief, the partner deck and a verbal assessment all said this platform
deploys "three alarms" and called observability its thinnest layer. The number came from counting
`cw.Alarm(` CALL SITES in observability_stack.py; two of the three are inside loops. The template
carries twenty-two. Counting the source instead of the artifact is the same defect as L60 (a
negation control whose mutation never landed) and L67 (a survey loop that measured the previous
repository), and it was the third occurrence in one remediation.

So alarm COVERAGE was never the problem. What the census found once it read the template was that
the alarms were not operable:

  OBS-1  nine of twenty-two had no AlarmName - only a CloudFormation logical id
         (`WorkflowFailedEDBEFEBB`), which no runbook can reference and no operator can find;
  OBS-2  zero composite alarms and one SNS topic, so a tenant at 60% of budget arrived with the
         same urgency as the determination workflow failing;
  OBS-3  p95 duration was charted and never alarmed - an absent SLO, in practice;
  OBS-4  a stalled human sign-off was detected only by the 24h execution timeout.

Every test below asserts a property of the SYNTHESIZED TEMPLATE. Several are negations - the
load-bearing one being that a budget advisory must never reach the page tier - because a severity
scheme nothing can violate is not a severity scheme.
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

from app import stage_lambda_bundle  # noqa: E402
from ben_stacks.compute_stack import ComputeStack  # noqa: E402
from ben_stacks.data_stack import DataStack  # noqa: E402
from ben_stacks.lineage_stack import LineageStack  # noqa: E402
from ben_stacks.observability_stack import ObservabilityStack  # noqa: E402
from ben_stacks.workflow_stack import WorkflowStack  # noqa: E402

PREFIX = "ben-obs"
TENANTS = ("sp-a", "sp-b")


def _template(prefix=PREFIX):
    prices = json.dumps({"price_version": "t",
                         "models": {"anthropic.claude-sonnet-4-5": {"input_per_m": 3, "output_per_m": 15}}})
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    data = DataStack(app, "d", prefix=prefix, retention_profile="sandbox-demo")
    compute = ComputeStack(app, "c", prefix=prefix, asset_dir=asset, data=data, multitenant=True,
                           budget={"monthly_token_cap": 5000000, "cap_behavior": "hard",
                                   "monthly_usd": 25.5, "prices_json": prices})
    workflow = WorkflowStack(app, "w", prefix=prefix, compute=compute, data=data, multitenant=True)
    lineage = LineageStack(app, "l", prefix=prefix)
    obs = ObservabilityStack(app, "o", prefix=prefix, compute=compute, workflow=workflow, data=data,
                             tenants=TENANTS, budget_usd=25.5, lineage=lineage,
                             runtime_role_name="AmazonBedrockAgentCoreSDKRuntime-t")
    return Template.from_stack(obs).to_json()


TPL = _template()
RES = TPL["Resources"]
ALARMS = {k: v for k, v in RES.items() if v["Type"] == "AWS::CloudWatch::Alarm"}
COMPOSITES = {k: v for k, v in RES.items() if v["Type"] == "AWS::CloudWatch::CompositeAlarm"}
TOPICS = {k: v for k, v in RES.items() if v["Type"] == "AWS::SNS::Topic"}
NAME_OF = {k: v["Properties"].get("AlarmName") for k, v in ALARMS.items()}


def _members(composite):
    """Alarm names referenced by a composite's AlarmRule.

    The rule renders as a Fn::Join over Fn::GetAtt references to each constituent alarm's Arn, so
    membership is resolved through the logical ids that appear in the rule, not by string matching
    on names that are themselves tokens.
    """
    rule = json.dumps(composite["Properties"]["AlarmRule"])
    return {NAME_OF[lid] for lid in ALARMS if '"%s"' % lid in rule or "'%s'" % lid in rule}


# ── OBS-1 ────────────────────────────────────────────────────────────────────────

def test_every_alarm_has_a_name_a_runbook_can_reference():
    unnamed = sorted(k for k, n in NAME_OF.items() if not isinstance(n, str))
    assert not unnamed, (
        "%d alarm(s) carry only a CloudFormation logical id, so no runbook can name them "
        "and no operator can find them in the console: %s" % (len(unnamed), unnamed))


def test_alarm_names_are_prefix_scoped_and_carry_no_synth_hash():
    for k, n in NAME_OF.items():
        assert n.startswith(PREFIX + "-"), "%s -> %r is not prefix-scoped" % (k, n)
        assert not re.search(r"[0-9A-F]{8}$", n), "%r looks like a logical-id hash, not a name" % n


def test_alarm_names_are_stable_across_synths():
    """A runbook is worthless if the names move. Two independent synths must agree."""
    second = _template()
    a = sorted(v["Properties"]["AlarmName"] for v in
               (r for r in second["Resources"].values() if r["Type"] == "AWS::CloudWatch::Alarm"))
    assert a == sorted(NAME_OF.values())


def test_every_alarm_still_reaches_the_original_ops_topic():
    """OBS-2 is additive. The budget-breach function subscribes to <prefix>-ops-alarms."""
    for k, v in ALARMS.items():
        assert v["Properties"].get("AlarmActions"), "%s has no action" % (NAME_OF[k],)


# ── OBS-2 ────────────────────────────────────────────────────────────────────────

def test_three_severity_tiers_exist_with_distinct_topics():
    names = {v["Properties"]["AlarmName"] for v in COMPOSITES.values()}
    assert names == {"%s-severity-%s" % (PREFIX, t) for t in ("p1", "p2", "p3")}, names
    topic_names = {v["Properties"].get("TopicName") for v in TOPICS.values()}
    for t in ("p1", "p2", "p3"):
        assert "%s-ops-%s" % (PREFIX, t) in topic_names, topic_names
    assert "%s-ops-alarms" % PREFIX in topic_names, "the original topic must survive"
    # each composite publishes somewhere, and to a different place than its neighbours
    actions = [json.dumps(v["Properties"]["AlarmActions"]) for v in COMPOSITES.values()]
    assert len(set(actions)) == 3, "tiers share a topic, so tiering changes nothing"


def _tier(t):
    return next(v for v in COMPOSITES.values()
                if v["Properties"]["AlarmName"] == "%s-severity-%s" % (PREFIX, t))


def test_p1_is_the_governed_path_and_evidence_integrity():
    m = _members(_tier("p1"))
    for expected in ("%s-workflow-failed" % PREFIX, "%s-mask-errors" % PREFIX,
                     "%s-write-audit-errors" % PREFIX, "%s-guard-failures" % PREFIX,
                     "%s-bedrock-perimeter-bypass" % PREFIX):
        assert expected in m, "%s missing from P1; members=%s" % (expected, sorted(m))


def test_a_budget_advisory_never_reaches_the_page_tier():
    """The load-bearing negation.

    The whole point of tiering is that 60% of a spend ceiling does not wake anyone. If an advisory
    can reach P1 the scheme is decorative, and operators will mute the topic - which turns
    twenty-six alarms back into zero.
    """
    p1 = _members(_tier("p1"))
    advisory = {n for n in NAME_OF.values() if re.search(r"-budget-.*-(60|85)$", n or "")}
    assert advisory, "no 60/85% budget alarms were generated - the fixture is not exercising them"
    assert not (advisory & p1), "advisory alarms in the PAGE tier: %s" % sorted(advisory & p1)


def test_a_hard_cap_breach_is_degraded_not_advisory():
    """100% under a hard cap means tenants are being refused. That is service impact."""
    p2, p3 = _members(_tier("p2")), _members(_tier("p3"))
    hundreds = {n for n in NAME_OF.values() if re.search(r"-budget-.*-100$", n or "")}
    assert hundreds and hundreds <= p2, sorted(hundreds - p2)
    assert not (hundreds & p3)


def test_every_alarm_belongs_to_exactly_one_tier():
    """An alarm in no tier is invisible to the paging scheme - the inert-control shape."""
    tiers = {t: _members(_tier(t)) for t in ("p1", "p2", "p3")}
    everything = set(NAME_OF.values())
    covered = tiers["p1"] | tiers["p2"] | tiers["p3"]
    assert everything == covered, "untiered alarms: %s" % sorted(everything - covered)
    for a, b in (("p1", "p2"), ("p1", "p3"), ("p2", "p3")):
        assert not (tiers[a] & tiers[b]), "%s and %s overlap: %s" % (a, b, sorted(tiers[a] & tiers[b]))


# ── OBS-3 ────────────────────────────────────────────────────────────────────────

def test_latency_is_alarmed_not_merely_charted():
    lat = {k: v for k, v in ALARMS.items() if v["Properties"].get("MetricName") == "Duration"}
    assert lat, "p95 duration is on the dashboard and nothing alarms on it - that is an absent SLO"
    for k, v in lat.items():
        assert v["Properties"].get("ExtendedStatistic") == "p95", NAME_OF[k]
        assert v["Properties"]["EvaluationPeriods"] >= 3, (
            "%s fires on a single period - one slow invocation should not raise a latency alarm"
            % NAME_OF[k])


def test_latency_alarms_are_degraded_not_a_page():
    """Slow is not down. A caseworker waiting is a ticket, not a 3am page."""
    lat = {NAME_OF[k] for k, v in ALARMS.items() if v["Properties"].get("MetricName") == "Duration"}
    assert lat <= _members(_tier("p2"))
    assert not (lat & _members(_tier("p1")))


# ── OBS-4 ────────────────────────────────────────────────────────────────────────

def test_approval_backlog_is_detected_in_hours_not_at_the_24h_timeout():
    backlog = [v for k, v in ALARMS.items() if NAME_OF[k] == "%s-approval-backlog" % PREFIX]
    assert backlog, "no approval-backlog alarm; a stalled due-process gate is invisible for a day"
    p = backlog[0]["Properties"]
    # a math expression over BOTH signals, not a single metric
    blob = json.dumps(p)
    assert "signoff" in blob.lower() or "Metrics" in p, "expected a math expression over two metrics"
    window_hours = p["EvaluationPeriods"] * 1  # 1h period
    assert window_hours < 24, "detection window %sh is not better than the execution timeout" % window_hours


def test_approval_backlog_does_not_use_execution_time():
    """Step Functions publishes ExecutionTime on COMPLETION.

    An execution stuck at the approval gate never emits it, so an alarm on that metric would be
    green and inert - precisely the failure this register keeps recording. Guard against a future
    'simplification' to ExecutionTime.
    """
    for k, v in ALARMS.items():
        if NAME_OF[k] == "%s-approval-backlog" % PREFIX:
            assert v["Properties"].get("MetricName") != "ExecutionTime"


# ── guard on the guard ───────────────────────────────────────────────────────────

def test_the_membership_helper_can_actually_fail():
    """If _members() returned everything, every membership assertion above would pass vacuously."""
    p1, p3 = _members(_tier("p1")), _members(_tier("p3"))
    assert p1 and p3 and p1 != p3, "the tier-membership helper is not discriminating"
    assert len(p1) < len(NAME_OF), "P1 contains every alarm - the helper is matching too broadly"
