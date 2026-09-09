#!/usr/bin/env python3
"""Census of what the observability stacks ACTUALLY deploy, read off the synthesized template.

WHY THIS EXISTS
---------------
On 2026-09-09 the partner brief, the partner deck and a verbal assessment all stated that this
platform deploys "three alarms". That number came from counting `cw.Alarm(` CALL SITES in
observability_stack.py. Two of the three are inside loops. The template actually carries 22 alarms.

The error is not the arithmetic, it is the method: counting the source instead of the artifact.
That is the same defect as L60 (a negation control whose mutation never landed) and L67 (a survey
loop that measured the wrong repository) - an instrument that reports on something other than the
thing it claims to measure. So the fix is not "remember the right number", it is to make the number
come from a script that reads the CloudFormation template, and to have the doc gate consume it.

WHAT IT REPORTS
---------------
Counts, plus the three operational properties that a raw count hides and that an operator actually
feels at 3am:

  * alarms with no AlarmName - they exist only as CloudFormation logical IDs, so an incident
    runbook cannot name them and an operator cannot find them in the console;
  * composite alarms - without them every alarm pages at the same severity;
  * dashboard-charted metrics that carry no alarm at all - the shape an absent SLO takes in practice.

    python tools/observability_census.py [--json out.json] [--assert-baseline]

`--assert-baseline` fails non-zero if the census drifts from BASELINE below, so the numbers quoted
in partner material cannot silently rot.
"""
import argparse
import json
import pathlib
import re
import sys

# Measured 2026-09-09 from the synthesized template, two tenants, budget on, lineage wired.
# Post-OBS-1..4 (2026-09-09). Pre-uplift this read alarms=22, unnamed=9, composite=0 - the numbers
# the first version of the partner brief quoted. Any change here must move the partner documents in
# the SAME commit; --assert-baseline is what makes that non-optional.
BASELINE = {
    "alarms": 26,
    "metric_filters": 2,
    "dashboards": 1,
    "unnamed_alarms": 0,
    "composite_alarms": 3,
}


def _synth(repo: pathlib.Path):
    sys.path.insert(0, str(repo / "cdk"))
    import aws_cdk
    from aws_cdk.assertions import Template
    from app import stage_lambda_bundle
    from ben_stacks.compute_stack import ComputeStack
    from ben_stacks.data_stack import DataStack
    from ben_stacks.lineage_stack import LineageStack
    from ben_stacks.observability_stack import ObservabilityStack
    from ben_stacks.workflow_stack import WorkflowStack

    prices = json.dumps({"price_version": "census",
                         "models": {"anthropic.claude-sonnet-4-5": {"input_per_m": 3, "output_per_m": 15}}})
    app = aws_cdk.App()
    asset = stage_lambda_bundle()
    data = DataStack(app, "d", prefix="ben-census", retention_profile="sandbox-demo")
    compute = ComputeStack(app, "c", prefix="ben-census", asset_dir=asset, data=data, multitenant=True,
                           budget={"monthly_token_cap": 5000000, "cap_behavior": "hard",
                                   "monthly_usd": 25.5, "prices_json": prices})
    workflow = WorkflowStack(app, "w", prefix="ben-census", compute=compute, data=data, multitenant=True)
    lineage = LineageStack(app, "l", prefix="ben-census")
    obs = ObservabilityStack(app, "o", prefix="ben-census", compute=compute, workflow=workflow,
                             data=data, tenants=("sp-a", "sp-b"), budget_usd=25.5, lineage=lineage,
                             runtime_role_name="AmazonBedrockAgentCoreSDKRuntime-census")
    return Template.from_stack(obs).to_json()


def census(repo: pathlib.Path):
    res = _synth(repo)["Resources"]
    of = lambda t: {k: v for k, v in res.items() if v["Type"] == t}  # noqa: E731
    alarms = of("AWS::CloudWatch::Alarm")
    composite = of("AWS::CloudWatch::CompositeAlarm")
    dashes = of("AWS::CloudWatch::Dashboard")

    named, unnamed = {}, {}
    for k, v in alarms.items():
        nm = v["Properties"].get("AlarmName")
        (named if isinstance(nm, str) else unnamed)[k] = v

    alarmed_metrics = {(str(v["Properties"].get("Namespace")), str(v["Properties"].get("MetricName")))
                       for v in alarms.values()}
    body = json.dumps(list(dashes.values())[0]["Properties"]["DashboardBody"]) if dashes else ""
    widget_titles = re.findall(r'title\\+"\s*:\s*\\+"([^\\"]{3,70})', body)

    return {
        "alarms": len(alarms),
        "composite_alarms": len(composite),
        "metric_filters": len(of("AWS::Logs::MetricFilter")),
        "dashboards": len(dashes),
        "dashboard_widgets": len(widget_titles),
        "widget_titles": widget_titles,
        "named_alarms": len(named),
        "unnamed_alarms": len(unnamed),
        "unnamed_alarm_ids": sorted(re.sub(r"[0-9A-F]{8}$", "", k) for k in unnamed),
        "alarms_with_action": sum(1 for v in alarms.values() if v["Properties"].get("AlarmActions")),
        "alarm_names": sorted(v["Properties"]["AlarmName"] for v in named.values()),
        "alarmed_metrics": sorted(alarmed_metrics),
        "latency_alarmed": any(m == "Duration" for _, m in alarmed_metrics),
        "sns_topics": len(of("AWS::SNS::Topic")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None, help="pack root (default: two levels up from this file)")
    ap.add_argument("--json", dest="out", default=None)
    ap.add_argument("--assert-baseline", action="store_true")
    a = ap.parse_args()
    repo = pathlib.Path(a.repo) if a.repo else pathlib.Path(__file__).resolve().parents[1]

    c = census(repo)
    print("observability census (2 tenants, budget on, lineage wired)")
    print("  alarms                 %3d   (%d named, %d logical-id only)"
          % (c["alarms"], c["named_alarms"], c["unnamed_alarms"]))
    print("  composite alarms       %3d   %s" % (c["composite_alarms"],
          "<- no severity tiering" if not c["composite_alarms"] else ""))
    print("  alarms with an action  %3d" % c["alarms_with_action"])
    print("  metric filters         %3d" % c["metric_filters"])
    print("  dashboards / widgets   %3d / %d" % (c["dashboards"], c["dashboard_widgets"]))
    print("  sns topics             %3d" % c["sns_topics"])
    print("  latency alarmed        %s   %s" % (c["latency_alarmed"],
          "<- p95 is charted but never alarmed: this is what an absent SLO looks like"
          if not c["latency_alarmed"] else ""))
    if c["unnamed_alarm_ids"]:
        print("  UNNAMEABLE BY A RUNBOOK:")
        for i in c["unnamed_alarm_ids"]:
            print("      %s" % i)

    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(c, indent=2), encoding="utf-8")
        print("  -> %s" % a.out)

    if a.assert_baseline:
        drift = {k: (BASELINE[k], c[k]) for k in BASELINE if BASELINE[k] != c[k]}
        if drift:
            print("\nBASELINE DRIFT (expected, actual):")
            for k, (e, g) in sorted(drift.items()):
                print("  %-18s %s -> %s" % (k, e, g))
            print("\nUpdate BASELINE and every partner document that quotes these numbers, "
                  "in the same commit.")
            return 1
        print("\nbaseline OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
