#!/usr/bin/env python3
"""tier1_regate — ONE from-zero live gate for the Tier-1 hardening + enforcement-perimeter batch.

Deploys the pack with every control armed that the batch changed only in IaC, proves each one against the
real account, exercises a REAL bypass (a direct model call by the deployer IAM user) to make the
perimeter-bypass alarm fire, renders the Day-2 operator console from live state, then tears down to zero
residue. ALWAYS tears down, even on failure. Evidence JSON/MD under evidence/, account id redacted.

Proves, live:
  T1-a  mandatory-guardrail IAM condition does not break the drafter (guardrail_proof PASS)
  T1-b  #3 authoritative consent/purpose still holds (cedar_perimeter_proof PASS)
  P-2   capture trail carries the ADVANCED selectors (management + every Bedrock data type + AgentCore)
  P-3   <prefix>-bedrock-perimeter-bypass -> ALARM after a direct IAM-user call; the drafter's own calls
        did NOT count (metric sum == number of human calls)
  P-4   model-invocation log group is CMK-encrypted AND received the drafter's invocations (delivery works
        with the key grant)
  P-5   bedrock-runtime VPC endpoint carries the GovernedDrafterOnly policy AND the drafter still drafts
        through it (private mode)
  D2    operator console renders from live state
Usage: python scripts/tier1_regate.py --env t1 --region us-east-1 [--skip-deploy] [--skip-teardown]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CDK = os.path.join(REPO, "cdk")
ACCOUNT_RE = re.compile(r"\b\d{12}\b")
REDACT = "111122223333"


def ctx(env):
    return ["-c", "env=%s" % env, "-c", "retention_profile=sandbox-demo", "-c", "kms=customer-managed",
            "-c", "network_mode=private", "-c", "perimeter=1", "-c", "model_logging=1",
            "-c", "model_log_lock_days=0", "-c", "capture_all=1", "-c", "capture_lock_mode=GOVERNANCE",
            "-c", "capture_retention_days=1", "-c", "tenant=ben-%s-agency" % env]


def sh(cmd, cwd=None, timeout=3600):
    t0 = time.time()
    # CDK prints UTF-8 (smart quotes, arrows); on Windows the locale codec is cp1252 -> decode error mid-gate.
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout, shell=(os.name == "nt"))
    return {"cmd": " ".join(cmd) if isinstance(cmd, list) else cmd, "rc": r.returncode,
            "secs": round(time.time() - t0, 1), "out": (r.stdout or "")[-6000:], "err": (r.stderr or "")[-4000:]}


def cdk_cmd(*args):
    return ["npx", "--yes", "aws-cdk@2", *args]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="t1")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--skip-deploy", action="store_true")
    ap.add_argument("--skip-teardown", action="store_true")
    ap.add_argument("--alarm-wait-min", type=int, default=25)
    a = ap.parse_args()
    env, region, prefix = a.env, a.region, "ben-%s" % a.env
    s = boto3.Session(region_name=region)
    acct = s.client("sts").get_caller_identity()["Account"]
    checks, steps = {}, {}
    t_start = int(time.time() * 1000)
    # Model-invocation logging is an ACCOUNT singleton: -c model_logging=1 REPLACES whatever the account had
    # (here: the platform runbook's /aegis/bedrock/model-invocations config) and the stack's on_delete
    # DELETES it. Snapshot now; restore after teardown; the residue check requires "as before".
    bedrock = s.client("bedrock")
    try:
        pre_cfg = bedrock.get_model_invocation_logging_configuration().get("loggingConfig")
    except Exception:
        pre_cfg = None
    steps["pre_model_logging_cfg"] = pre_cfg

    def check(name, ok, detail=""):
        checks[name] = {"ok": bool(ok), "detail": detail}
        print(("PASS " if ok else "FAIL ") + name + (" - " + str(detail)[:200] if detail else ""), flush=True)

    fatal = None
    try:
        # ── 1. deploy from zero ───────────────────────────────────────────────────────────────
        if not a.skip_deploy:
            steps["deploy"] = sh(cdk_cmd("deploy", "--all", "--require-approval", "never",
                                         "--outputs-file", "outputs-%s.json" % env, *ctx(env)), cwd=CDK, timeout=3600)
            check("deploy", steps["deploy"]["rc"] == 0, "rc=%s in %ss" % (steps["deploy"]["rc"], steps["deploy"]["secs"]))
            if steps["deploy"]["rc"] != 0:
                raise RuntimeError("deploy failed")
        outputs = {}
        try:
            outputs = json.load(open(os.path.join(CDK, "outputs-%s.json" % env), encoding="utf-8"))
        except Exception:
            pass

        # ── 2. P-2 advanced selectors on the capture trail ────────────────────────────────────
        ct = s.client("cloudtrail")
        sel = ct.get_event_selectors(TrailName="%s-capture-all" % prefix)
        adv = sel.get("AdvancedEventSelectors", [])
        types = {f["Equals"][0] for x in adv for f in x.get("FieldSelectors", []) if f["Field"] == "resources.type"}
        mgmt = any(f["Field"] == "eventCategory" and f["Equals"] == ["Management"]
                   for x in adv for f in x.get("FieldSelectors", []))
        need = {"AWS::Bedrock::Guardrail", "AWS::Bedrock::Model", "AWS::Bedrock::KnowledgeBase",
                "AWS::Bedrock::AgentAlias", "AWS::BedrockAgentCore::Gateway", "AWS::S3::Object", "AWS::Lambda::Function"}
        check("P2_advanced_selectors", mgmt and need <= types and not sel.get("EventSelectors"),
              "management=%s types=%d basic_selectors=%s" % (mgmt, len(types), bool(sel.get("EventSelectors"))))

        # ── 3. P-5 endpoint policy present ────────────────────────────────────────────────────
        ec2 = s.client("ec2")
        eps = ec2.describe_vpc_endpoints(Filters=[{"Name": "service-name", "Values": ["com.amazonaws.%s.bedrock-runtime" % region]}])["VpcEndpoints"]
        pol = " ".join(e.get("PolicyDocument", "") for e in eps)
        check("P5_endpoint_policy_present", len(eps) >= 1 and "GovernedDrafterOnly" in pol and "-compute-coretools" in pol,
              "endpoints=%d" % len(eps))

        # ── 4. P-4 invocation log group is CMK-encrypted ──────────────────────────────────────
        logs = s.client("logs")
        mig = "/aws/bedrock/modelinvocations/%s" % prefix
        g = logs.describe_log_groups(logGroupNamePrefix=mig).get("logGroups", [])
        check("P4_invocation_log_group_cmk", bool(g) and bool(g[0].get("kmsKeyId")), "kms=%s" % (g[0].get("kmsKeyId", "")[-20:] if g else None))

        # ── 5. T1-a guardrail proof (drafter through the endpoint, mandatory-guardrail condition) ─
        steps["guardrail_proof"] = sh([sys.executable, os.path.join(HERE, "guardrail_proof.py"), "--env", env, "--region", region], cwd=REPO, timeout=1800)
        check("T1a_guardrail_proof", steps["guardrail_proof"]["rc"] == 0, "rc=%s" % steps["guardrail_proof"]["rc"])
        # ── 6. T1-b #3 perimeter proof ─────────────────────────────────────────────────────────
        steps["cedar_perimeter_proof"] = sh([sys.executable, os.path.join(HERE, "cedar_perimeter_proof.py"), "--env", env, "--region", region], cwd=REPO, timeout=1800)
        check("T1b_cedar_perimeter_proof", steps["cedar_perimeter_proof"]["rc"] == 0, "rc=%s" % steps["cedar_perimeter_proof"]["rc"])

        # ── 7. P-4 the drafter's invocations were DELIVERED to the CMK log group ──────────────
        delivered = 0
        for _ in range(12):
            streams = logs.describe_log_streams(logGroupName=mig, orderBy="LastEventTime", descending=True, limit=5).get("logStreams", [])
            delivered = sum(1 for st in streams if st.get("lastEventTimestamp", 0) >= t_start)
            if delivered:
                break
            time.sleep(20)
        check("P4_invocation_log_delivered_with_cmk", delivered > 0, "streams_with_events=%d" % delivered)

        # ── 8. P-3 REAL bypass: direct model call as the deployer IAM user -> alarm ───────────
        br = s.client("bedrock-runtime")
        model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
        bypass_t = int(time.time() * 1000)
        try:
            br.converse(modelId=model, messages=[{"role": "user", "content": [{"text": "Reply with the single word OK."}]}],
                        inferenceConfig={"maxTokens": 4})
            bypass_call = "invoked (no guardrail, no gateway - the exact bypass the perimeter must see)"
        except Exception as exc:
            bypass_call = "call refused (%s) - still an InvokeModel event by an IAM user" % type(exc).__name__
        cw = s.client("cloudwatch")
        alarm_name = "%s-bedrock-perimeter-bypass" % prefix
        state, deadline = "", time.time() + a.alarm_wait_min * 60
        while time.time() < deadline:
            al = cw.describe_alarms(AlarmNames=[alarm_name]).get("MetricAlarms", [])
            state = al[0]["StateValue"] if al else "MISSING"
            if state == "ALARM":
                break
            time.sleep(30)
        # the metric must count ONLY the human call(s): the drafter's guardrail-proof invocations are allowlisted
        from datetime import datetime, timezone
        ms = cw.get_metric_statistics(Namespace="Aegis/Perimeter/%s" % prefix, MetricName="BedrockBypassInvocations",
                                      StartTime=datetime.fromtimestamp(t_start / 1000 - 60, tz=timezone.utc),
                                      EndTime=datetime.now(tz=timezone.utc), Period=3600, Statistics=["Sum"])
        total = sum(d["Sum"] for d in ms.get("Datapoints", []))
        check("P3_bypass_alarm_fired", state == "ALARM", "alarm=%s; bypass=%s" % (state, bypass_call))
        # Attempt-8 lesson: the metric legitimately counts EVERY non-allowlisted Bedrock call in the window,
        # not just this script's converse - the guardrail proof's direct ApplyGuardrail calls by the deployer
        # user are real bypasses too (and proved the data-event selectors live). So the assertion is
        # exactness against the capture log: metric_sum == non-allowlisted events, and the drafter's
        # own calls (allowlisted sessionIssuer) exist but are NOT counted.
        cap = "/aws/cloudtrail/%s-capture-all" % prefix
        def _count(pattern):
            n, tok = 0, None
            for _ in range(50):
                kw = dict(logGroupName=cap, startTime=t_start - 60000, filterPattern=pattern)
                if tok:
                    kw["nextToken"] = tok
                r = logs.filter_log_events(**kw)
                n += len(r.get("events", []))
                tok = r.get("nextToken")
                if not tok:
                    break
            return n
        # Attempt-9 lesson: the metric filter counts only INFERENCE-family event names (GetGuardrail by a
        # human is a management read, not a bypass), so the capture-log counts use the SAME event set.
        sys.path.insert(0, os.path.join(REPO, "cdk"))
        from ben_stacks.observability_stack import ObservabilityStack
        from ben_stacks.compute_stack import drafter_role_name
        inv = "(" + " || ".join('($.eventName = "%s")' % e for e in ObservabilityStack.BEDROCK_INVOKE_EVENTS) + ")"
        try:
            human = _count('{ ($.eventSource = "bedrock.amazonaws.com") && %s && (($.userIdentity.type = "IAMUser") || ($.userIdentity.type = "Root")) }' % inv)
            drafter = _count('{ ($.eventSource = "bedrock.amazonaws.com") && %s && ($.userIdentity.type = "AssumedRole") && ($.userIdentity.sessionContext.sessionIssuer.arn = "arn:aws:iam::*:role/%s") }' % (inv, drafter_role_name(prefix)))
        except Exception as exc:
            human, drafter = -1, -1
            steps["p3_capture_counts_error"] = str(exc)[:200]
        steps["p3_counts"] = {"metric_sum": total, "human_events": human, "drafter_events": drafter}
        check("P3_metric_counts_exactly_the_non_allowlisted_calls", human >= 1 and total == human,
              "metric_sum=%s human_events=%s" % (total, human))
        check("P3_drafter_calls_not_counted", drafter >= 1 and total == human,
              "drafter_events=%s (allowlisted, must exist and be excluded); metric_sum=%s" % (drafter, total))
        # what the capture log recorded for it
        try:
            ev = logs.filter_log_events(logGroupName="/aws/cloudtrail/%s-capture-all" % prefix, startTime=bypass_t - 60000,
                                        filterPattern='{ ($.eventSource = "bedrock.amazonaws.com") && ($.userIdentity.type = "IAMUser") }', limit=3)
            rec = [json.loads(e["message"]) for e in ev.get("events", [])]
            steps["bypass_capture"] = [{"eventName": r.get("eventName"), "type": r.get("userIdentity", {}).get("type"),
                                        "category": r.get("eventCategory")} for r in rec]
        except Exception as exc:
            steps["bypass_capture"] = str(exc)[:200]
        # ApplyGuardrail DATA event (if the drafter exercised it) - proves the data selector end to end
        try:
            ev = logs.filter_log_events(logGroupName="/aws/cloudtrail/%s-capture-all" % prefix, startTime=t_start,
                                        filterPattern='{ $.eventName = "ApplyGuardrail" }', limit=3)
            steps["applyguardrail_data_events"] = len(ev.get("events", []))
        except Exception as exc:
            steps["applyguardrail_data_events"] = str(exc)[:200]

        # ── 9. D2 operator console from live state ────────────────────────────────────────────
        try:
            sys.path.insert(0, HERE)
            import operator_console as oc
            state_d = oc.gather_state(env, region)
            html = oc.render_console(state_d)
            with open(os.path.join(REPO, "evidence", "OPERATOR-CONSOLE-%s-LIVE.html" % prefix), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(ACCOUNT_RE.sub(REDACT, html))
            check("D2_operator_console_live", "Containment" in html or "kill" in html.lower(), "bytes=%d" % len(html))
        except Exception as exc:
            check("D2_operator_console_live", False, "%s: %s" % (type(exc).__name__, str(exc)[:150]))
    except Exception as exc:  # noqa: BLE001 - record, tear down, still write evidence
        fatal = "%s: %s" % (type(exc).__name__, str(exc)[:300])
        print("FATAL " + fatal, flush=True)
    finally:
        # ── 10. teardown to zero residue ──────────────────────────────────────────────────────
        if not a.skip_teardown:
            # The capture WORM bucket holds CloudTrail deliveries under a GOVERNANCE lock; CloudFormation
            # cannot delete a non-empty bucket and CDK's auto-delete cannot bypass a lock, so the lineage
            # stack would end DELETE_FAILED. Empty it (bypass, sandbox retention only) BEFORE destroy.
            try:
                # stop the trail FIRST - otherwise CloudTrail keeps delivering between the emptying below
                # and CloudFormation's bucket delete, and the lineage stack ends DELETE_FAILED anyway
                try:
                    s.client("cloudtrail").stop_logging(Name="%s-capture-all" % prefix)
                    time.sleep(20)
                except Exception as exc:
                    steps["capture_trail_stopped"] = "%s" % type(exc).__name__
                s3 = s.client("s3")
                wb = "%s-capture-worm-%s" % (prefix, acct)

                def _empty_capture_bucket():
                    n = 0
                    for page in s3.get_paginator("list_object_versions").paginate(Bucket=wb):
                        for o in page.get("Versions", []) + page.get("DeleteMarkers", []):
                            s3.delete_object(Bucket=wb, Key=o["Key"], VersionId=o["VersionId"], BypassGovernanceRetention=True)
                            n += 1
                    return n
                steps["capture_bucket_emptied"] = _empty_capture_bucket()
            except Exception as exc:
                steps["capture_bucket_emptied"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
                _empty_capture_bucket = lambda: 0
            steps["destroy"] = sh(cdk_cmd("destroy", "--all", "--force", *ctx(env)), cwd=CDK, timeout=3600)
            # Attempt-9 lesson (L13): CloudTrail keeps delivering for minutes after StopLogging, so the
            # capture bucket can be non-empty again by the time CloudFormation deletes it; `cdk destroy`
            # then aborts on the lineage stack and leaves every stack below it standing. Finish the job:
            # re-empty the bucket and delete whatever is still up, dependents first, with waits and retries.
            cf = s.client("cloudformation")
            order = ["lineage", "observability", "gateway", "workflow", "compute", "network", "identity", "data"]
            notes = []
            for rnd in range(3):
                present = {st["StackName"]: st["StackStatus"] for st in cf.describe_stacks()["Stacks"]
                           if st["StackName"].startswith(prefix + "-")}
                if not present:
                    break
                try:
                    notes.append("round %d: re-emptied %d late deliveries" % (rnd, _empty_capture_bucket()))
                except Exception as exc:
                    notes.append("round %d: empty -> %s" % (rnd, type(exc).__name__))
                for suffix in order:
                    name = "%s-%s" % (prefix, suffix)
                    if name not in present:
                        continue
                    try:
                        cf.delete_stack(StackName=name)
                        cf.get_waiter("stack_delete_complete").wait(StackName=name, WaiterConfig={"Delay": 15, "MaxAttempts": 100})
                        notes.append("%s deleted" % name)
                    except Exception as exc:
                        notes.append("%s: %s %s" % (name, type(exc).__name__, str(exc)[:100]))
            steps["destroy_remaining"] = notes
            steps["cleanup"] = sh([sys.executable, os.path.join(HERE, "cleanup_retained.py"), "--prefix", prefix,
                                   "--region", region, "--i-know-this-deletes-evidence"], cwd=REPO, timeout=1200)
            try:
                cfg = bedrock.get_model_invocation_logging_configuration().get("loggingConfig")
            except Exception:
                cfg = None
            if pre_cfg and cfg != pre_cfg:
                try:
                    bedrock.put_model_invocation_logging_configuration(loggingConfig=pre_cfg)
                    cfg = bedrock.get_model_invocation_logging_configuration().get("loggingConfig")
                    steps["model_logging_restored"] = True
                except Exception as exc:
                    steps["model_logging_restored"] = "%s: %s" % (type(exc).__name__, str(exc)[:150])
            restored = (cfg == pre_cfg) if pre_cfg else (not cfg or "modelinvocations/%s" % prefix not in json.dumps(cfg))
            # zero residue is what matters: the cleanup's own residue report (stacks/buckets/lambdas/...) is
            # the verdict; a first-pass `cdk destroy` failure that the retry loop finished is recorded, not fatal
            clean = False
            try:
                rep = json.loads(steps["cleanup"]["out"][steps["cleanup"]["out"].rindex("{\n  \"prefix\""):])
                clean = bool(rep.get("clean"))
            except Exception:
                clean = steps["cleanup"]["rc"] == 0
            check("teardown_zero_residue", clean and restored,
                  "destroy_rc=%s cleanup_rc=%s clean=%s model_logging_as_before=%s" % (steps["destroy"]["rc"], steps["cleanup"]["rc"], clean, restored))

    ok = all(c["ok"] for c in checks.values()) and not fatal
    result = {"gate": "tier1-regate", "env": env, "region": region, "pass": ok, "fatal": fatal, "checks": checks, "steps": steps,
              "context": ctx(env), "finished_at": int(time.time())}
    raw = json.dumps(result, indent=1, default=str)
    raw = raw.replace(acct, REDACT)
    raw = ACCOUNT_RE.sub(REDACT, raw)
    out = os.path.join(REPO, "evidence", "TIER1-REGATE-%s.json" % time.strftime("%Y-%m-%d"))
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(raw + "\n")
    print(json.dumps({"pass": ok, "checks": {k: v["ok"] for k, v in checks.items()}, "evidence": out}, indent=1))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
