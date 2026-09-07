#!/usr/bin/env python3
"""Full-portfolio live gate on ONE from-zero two-tenant deployment of the release tree, with the REAL
AgentCore Runtime launched on the IaC execution role (RT-2), then torn down to zero residue.

What it re-proves on the exact tree (the "not re-run on this tag" list in VALIDATED_RELEASE.md):
  111   consolidated gate            gate_111.py           isolation + audit routing 12/12, transparency 13/13
                                                           per tenant, strict PII canary
  KS    kill switch                  kill_switch_proof.py  29/29 incl. in-flight mid-session stop
  BUD   per-tenant token+USD budget  budget_proof.py       24/24 incl. meter == model log
  LIN   #168 lineage, 0 orphans      drive_one_case.py + lineage_proof.py
  RT-2  runtime on the IaC role      _configure.sh refuses a toolkit role; MMDSv2 explicit + asserted (R4-6); runtime model calls are
                                     guardrail-assessed (invocation log) and allowlisted by the perimeter
  E2E   0-unexpected regression      e2e_regression.py
  TD    teardown to zero residue     runtime + cdk destroy + cleanup_retained; model-logging restored

Usage: python scripts/full_portfolio_gate.py --env fp --region us-east-1 [--skip-deploy] [--skip-runtime]
       [--skip-teardown] [--teardown-on-fail] [--teardown-only]
Writes evidence/FULL-PORTFOLIO-GATE-<date>.json (+ the per-proof evidence files the proofs write).
Runs from the Windows host (Python 3.12 with governed_core + aws_cdk; Git-Bash for the runtime scripts).
"""
import argparse
import datetime
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
AGENT = os.path.join(REPO, "agents", "benefits-eligibility")
RUNTIME_DIR = os.path.join(REPO, "lib", "runtime")
GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
TENANTS = ("sp-a", "sp-b")


def ctx(env):
    return ["-c", "env=%s" % env, "-c", "retention_profile=sandbox-demo", "-c", "tenants=%s" % ",".join(TENANTS),
            "-c", "model_logging=1", "-c", "budget_usd=5", "-c", "capture_all=1",
            "-c", "capture_lock_mode=GOVERNANCE", "-c", "capture_retention_days=1", "-c", "perimeter=1"]


def sh(cmd, cwd=None, timeout=3600, env=None):
    t0 = time.time()
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout, shell=(os.name == "nt"), env=e)   # npx/aws are .cmd shims on Windows
    return {"cmd": cmd if isinstance(cmd, str) else " ".join(cmd), "rc": r.returncode,
            "secs": round(time.time() - t0, 1), "out": (r.stdout or "")[-8000:], "err": (r.stderr or "")[-4000:]}


def cdk_cmd(*args):
    return ["npx", "--yes", "aws-cdk@2", *args]


def bash(script, *args, env=None, timeout=1800):
    """Run a lib/runtime shell script under Git-Bash with POSIX-style paths."""
    def posix(p):
        p = p.replace("\\", "/")
        return re.sub(r"^([A-Za-z]):/", lambda m: "/%s/" % m.group(1).lower(), p)
    return sh([GIT_BASH, "-lc", "cd '%s' && bash '%s' %s" % (posix(REPO), posix(script), " ".join("'%s'" % posix(a) for a in args))],
              timeout=timeout, env=env)


def stack_outputs(cf, name):
    try:
        return {o["OutputKey"]: o["OutputValue"] for o in cf.describe_stacks(StackName=name)["Stacks"][0].get("Outputs", [])}
    except Exception:
        return {}


class _TeardownOnly(Exception):
    """--teardown-only: skip straight from the runtime-state read to the teardown block."""


def main():
    # the gate log is a redirected file on Windows (cp1252): the toolkit prints box-drawing characters, and a
    # print() of a check detail must never take the whole gate down (attempt 1, 2026-09-06)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="fp")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--skip-deploy", action="store_true")
    ap.add_argument("--skip-runtime", action="store_true", help="reuse the runtime already launched for this env")
    ap.add_argument("--skip-teardown", action="store_true")
    ap.add_argument("--teardown-on-fail", action="store_true")
    ap.add_argument("--deploy-timeout", type=int, default=1800,
                    help="seconds to wait for the cdk CLI before falling back to CloudFormation state (L24)")
    ap.add_argument("--teardown-only", action="store_true",
                    help="no proofs: tear down the env this script left behind (runtime from .bedrock_agentcore.yaml + stacks)")
    a = ap.parse_args()
    if a.teardown_only:
        a.skip_deploy = a.skip_runtime = a.teardown_on_fail = True
    env, region, prefix = a.env, a.region, "ben-%s" % a.env
    date = datetime.date.today().isoformat()
    s = boto3.Session(region_name=region)
    acct = s.client("sts").get_caller_identity()["Account"]
    cf = s.client("cloudformation")
    bedrock = s.client("bedrock")
    checks, steps = {}, {}
    t_start = int(time.time() * 1000)
    try:
        pre_cfg = bedrock.get_model_invocation_logging_configuration().get("loggingConfig")
    except Exception:
        pre_cfg = None
    steps["pre_model_logging_cfg"] = pre_cfg

    def check(name, ok, detail=""):
        checks[name] = {"ok": bool(ok), "detail": detail}
        print(("PASS " if ok else "FAIL ") + name + (" - " + str(detail)[:200] if detail else ""), flush=True)

    fatal = None
    runtime_arn, runtime_log_group, runtime_id = "", "", ""
    try:
        # -- 1. deploy from zero (two tenants, model logging, USD ceiling, capture-all, perimeter) --
        if not a.skip_deploy:
            # L24 (live-found, attempt 8): CLOUDFORMATION, NOT THE CLI, IS THE AUTHORITY ON DEPLOY.
            # The gate defined "deployed" as "the cdk CLI exited 0". On attempt 8 every stack reached
            # CREATE_COMPLETE by 00:59:40Z and the CLI then sat at ZERO CPU for 50 minutes without
            # exiting - the whole gate blocked behind a hung process and would have died on the
            # 3600s timeout as a FATAL, not a readable failure. Attempt 5 hit the same hang.
            #
            # The deploy is now bounded, and on a timeout or a non-zero rc the state of the STACKS
            # decides: if every expected stack is CREATE/UPDATE_COMPLETE the deploy really did
            # succeed and the run continues, with the hang RECORDED rather than hidden. If the
            # stacks are not complete it is a real failure and still fails. This makes the evidence
            # stronger, not weaker - a CLI exit code was never the thing being claimed.
            EXPECTED = [prefix + "-" + s for s in
                        (["data"] + ["%s-data" % t for t in TENANTS] +
                         ["identity", "lineage", "compute", "workflow", "gateway", "observability"])]

            def _stacks_all_complete():
                done, missing = {}, []
                for name in EXPECTED:
                    try:
                        st = cf.describe_stacks(StackName=name)["Stacks"][0]["StackStatus"]
                    except Exception:
                        st = "ABSENT"
                    done[name] = st
                    if st not in ("CREATE_COMPLETE", "UPDATE_COMPLETE"):
                        missing.append("%s=%s" % (name, st))
                return (not missing), done, missing

            try:
                steps["deploy"] = sh(cdk_cmd("deploy", "--all", "--require-approval", "never",
                                             "--outputs-file", "outputs-%s.json" % env, *ctx(env)),
                                     cwd=CDK, timeout=int(a.deploy_timeout))
                deploy_rc = steps["deploy"]["rc"]
                hung = False
            except subprocess.TimeoutExpired:
                steps["deploy"] = {"rc": "timeout", "secs": int(a.deploy_timeout),
                                   "note": "cdk CLI did not exit within the deploy timeout"}
                deploy_rc, hung = None, True

            ok, statuses, missing = _stacks_all_complete()
            steps["deploy_stack_states"] = statuses
            if deploy_rc == 0 and not hung:
                check("deploy", True, "rc=0 in %ss" % steps["deploy"]["secs"])
            elif ok:
                steps["deploy_cli_hung"] = True
                check("deploy", True,
                      "cdk CLI %s but every expected stack is COMPLETE (CloudFormation is the "
                      "authority; CLI hang recorded)" % ("hung - no exit" if hung else "rc=%s" % deploy_rc))
            else:
                check("deploy", False, "cdk rc=%s; stacks not complete: %s" % (deploy_rc, "; ".join(missing)[:180]))
                raise RuntimeError("deploy failed")
        ident, gw, comp = stack_outputs(cf, prefix + "-identity"), stack_outputs(cf, prefix + "-gateway"), stack_outputs(cf, prefix + "-compute")
        obs, lin, data, wf = (stack_outputs(cf, prefix + "-observability"), stack_outputs(cf, prefix + "-lineage"),
                              stack_outputs(cf, prefix + "-data"), stack_outputs(cf, prefix + "-workflow"))
        check("outputs_present", all(k in ident for k in ("UserPoolId", "ClientId")) and "GatewayUrl" in gw
              and "RuntimeExecutionRoleArn" in comp and "SsmDiscoveryParam" in gw,
              "identity=%s gateway=%s compute_runtime_role=%s" % (bool(ident), bool(gw), comp.get("RuntimeExecutionRoleName")))

        # -- 2. runtime on the IaC execution role (RT-2) --
        # spine-state for the runtime scripts: the DEPLOYMENT's identity + gateway + SSM parameter (the
        # manifest default /ben-eligibility/... is overridden by this file, sourced after agent.env).
        build = os.path.join(AGENT, ".build"); os.makedirs(build, exist_ok=True)
        state = os.path.join(build, "spine-state-%s.env" % env)
        discovery = "https://cognito-idp.%s.amazonaws.com/%s/.well-known/openid-configuration" % (region, ident.get("UserPoolId", ""))
        with open(state, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("".join("%s=%s\n" % kv for kv in [
                ("REGION", region), ("ACCOUNT", acct), ("POOL_ID", ident.get("UserPoolId", "")),
                ("CLIENT_ID", ident.get("ClientId", "")), ("DISCOVERY", discovery),
                ("GW_URL", gw.get("GatewayUrl", "")), ("GW_ARN", gw.get("GatewayArn", "")),
                ("ENGINE_ID", gw.get("PolicyEngineId", "")), ("SSM_PARAM", gw.get("SsmDiscoveryParam", ""))]))
        rt_env = {"PV_SPINE_STATE": state, "MULTITENANT": "1", "RUNTIME_EXEC_ROLE": comp.get("RuntimeExecutionRoleName", ""),
                  "RUNTIME_ROLE_ARN": comp.get("RuntimeExecutionRoleArn", ""), "AWS_REGION": region}
        if not a.skip_runtime:
            # a stale toolkit state file would make `launch --auto-update-on-conflict` target a runtime that
            # no longer exists; configure regenerates it
            for f in (".bedrock_agentcore.yaml",):
                try:
                    os.remove(os.path.join(RUNTIME_DIR, f))
                except FileNotFoundError:
                    pass
            steps["rt_obs_setup"] = bash(os.path.join(RUNTIME_DIR, "_obs_setup.sh"), AGENT, env=rt_env, timeout=600)
            steps["rt_configure"] = bash(os.path.join(RUNTIME_DIR, "_configure.sh"), AGENT, env=rt_env, timeout=900)
            cfg_ok = "CONFIGURE_EXIT=0" in steps["rt_configure"]["out"] and "execution_role=arn:aws:iam::" in steps["rt_configure"]["out"]
            check("RT2_configure_on_iac_role", cfg_ok and "REFUSED" not in steps["rt_configure"]["out"],
                  (steps["rt_configure"]["out"][-300:]).replace("\n", " | "))
            if not cfg_ok:
                raise RuntimeError("runtime configure failed")
            steps["rt_launch"] = bash(os.path.join(RUNTIME_DIR, "_launch.sh"), AGENT, env=rt_env, timeout=2400)
            check("RT2_launch", "LAUNCH_EXIT=0" in steps["rt_launch"]["out"], (steps["rt_launch"]["out"][-300:]).replace("\n", " | "))
            if "LAUNCH_EXIT=0" not in steps["rt_launch"]["out"]:
                raise RuntimeError("runtime launch failed")
        # the toolkit records the runtime it created
        exec_role = ""
        try:
            import yaml
            y = yaml.safe_load(open(os.path.join(RUNTIME_DIR, ".bedrock_agentcore.yaml"), encoding="utf-8"))
            ag = y["agents"][y["default_agent"]]
            runtime_arn = ag["bedrock_agentcore"]["agent_arn"]; runtime_id = ag["bedrock_agentcore"]["agent_id"]
            exec_role = ag["aws"]["execution_role"]
        except Exception as exc:
            runtime_arn = runtime_id = exec_role = ""
            steps["rt_state_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        runtime_log_group = "/aws/bedrock-agentcore/runtimes/%s-DEFAULT" % runtime_id
        check("RT2_runtime_uses_iac_role", bool(runtime_arn) and exec_role == comp.get("RuntimeExecutionRoleArn"),
              "runtime=%s role=%s" % (runtime_id, exec_role.rsplit("/", 1)[-1] if exec_role else None))
        steps["runtime"] = {"arn": runtime_arn, "id": runtime_id, "log_group": runtime_log_group, "exec_role": exec_role}
        if a.teardown_only:
            raise _TeardownOnly()
        # wait until the runtime is READY
        acc = s.client("bedrock-agentcore-control")
        st = ""
        for _ in range(40):
            try:
                st = acc.get_agent_runtime(agentRuntimeId=runtime_id)["status"]
            except Exception as exc:
                st = type(exc).__name__
            if st == "READY":
                break
            time.sleep(15)
        check("RT2_runtime_ready", st == "READY", "status=%s" % st)
        # R4-6 (fourth review): MMDSv2 must be EXPLICIT and asserted on the deployed runtime, not an
        # undocumented toolkit default - enforce (UpdateAgentRuntime if needed) and record the fact.
        steps["mmds"] = sh([sys.executable, os.path.join(HERE, "runtime_mmds.py"), "--runtime-id", runtime_id,
                            "--region", region, "--enforce"], cwd=REPO, timeout=900)
        try:
            mm = json.loads(steps["mmds"]["out"][steps["mmds"]["out"].index("{"):])
        except Exception:
            mm = {}
        check("RT2_runtime_mmdsv2", steps["mmds"]["rc"] == 0 and mm.get("requireMMDSV2") is True,
              "requireMMDSV2=%s before=%s enforced=%s" % (mm.get("requireMMDSV2"), mm.get("requireMMDSV2_before"), mm.get("enforced")))

        # -- 3. the proofs --
        common = ["--env", env, "--tenants", ",".join(TENANTS), "--region", region,
                  "--runtime-arn", runtime_arn, "--runtime-log-group", runtime_log_group]
        ev = os.path.join(REPO, "evidence")
        steps["gate_111"] = sh([sys.executable, os.path.join(HERE, "gate_111.py"), *common,
                                "--out", os.path.join(ev, "AGENTCORE-111-GATE-%s" % date)], cwd=REPO, timeout=3600)
        check("G111_consolidated_gate", steps["gate_111"]["rc"] == 0, "rc=%s in %ss" % (steps["gate_111"]["rc"], steps["gate_111"]["secs"]))
        steps["kill_switch"] = sh([sys.executable, os.path.join(HERE, "kill_switch_proof.py"), *common,
                                   "--out", os.path.join(ev, "AGENTCORE-KILL-SWITCH-%s" % date)], cwd=REPO, timeout=3600)
        check("KS_kill_switch_proof", steps["kill_switch"]["rc"] == 0, "rc=%s in %ss" % (steps["kill_switch"]["rc"], steps["kill_switch"]["secs"]))
        steps["budget"] = sh([sys.executable, os.path.join(HERE, "budget_proof.py"), *common,
                              "--out", os.path.join(ev, "AGENTCORE-BUDGET-%s" % date)], cwd=REPO, timeout=3600)
        check("BUD_budget_proof", steps["budget"]["rc"] == 0, "rc=%s in %ss" % (steps["budget"]["rc"], steps["budget"]["secs"]))
        # runtime model calls were guardrail-assessed (RT-2): the invocation log carries the guardrail trace
        try:
            logs = s.client("logs")
            mig = obs.get("ModelInvocationLogGroup", "/aws/bedrock/modelinvocations/%s" % prefix)
            ev_rows = logs.filter_log_events(logGroupName=mig, startTime=t_start,
                                             filterPattern='{ $.requestMetadata.component = "runtime" }', limit=20).get("events", [])
            assessed = sum(1 for e in ev_rows if "guardrail" in e["message"].lower())
            check("RT2_runtime_calls_guardrail_assessed", len(ev_rows) > 0 and assessed > 0,
                  "runtime_rows=%d guardrail_assessed=%d" % (len(ev_rows), assessed))
        except Exception as exc:
            check("RT2_runtime_calls_guardrail_assessed", False, "%s: %s" % (type(exc).__name__, str(exc)[:150]))
        # #168 lineage on one isolated case
        steps["drive_case"] = sh([sys.executable, os.path.join(HERE, "drive_one_case.py")], cwd=REPO, timeout=1200,
                                 env={"LINEAGE_PREFIX": prefix, "LINEAGE_TENANT": TENANTS[0], "AWS_REGION": region})
        case = {}
        try:
            case = json.load(open(os.path.join(REPO, ".build", "lineage-case.json"), encoding="utf-8"))
        except Exception:
            pass
        check("LIN_case_driven", steps["drive_case"]["rc"] == 0 and bool(case.get("case_id")) and "HumanSignoff" in case.get("states", []),
              "case=%s states=%s" % (case.get("case_id"), case.get("states")))
        if case.get("case_id"):
            tenant_data = stack_outputs(cf, "%s-%s-data" % (prefix, TENANTS[0]))
            steps["lineage"] = sh([sys.executable, os.path.join(HERE, "lineage_proof.py"), "--case-id", case["case_id"],
                                   "--tenant", TENANTS[0], "--prefix", prefix, "--region", region,
                                   "--capture-log-group", lin.get("CaptureLogGroupName", "/aws/cloudtrail/%s-capture-all" % prefix),
                                   "--ledger-table", tenant_data.get("AuditTableName", data.get("AuditTableName", "")),
                                   "--model-log-group", obs.get("ModelInvocationLogGroup", ""),
                                   "--gateway-log-group", obs.get("GatewayRequestLogGroup", ""),
                                   "--lambda-log-prefix", "/aws/lambda/%s-" % prefix,
                                   "--capture-worm-bucket", lin.get("CaptureWormBucket", ""),
                                   "--start-ms", str(case.get("start_ms", 0)), "--end-ms", str(case.get("end_ms", 0))],
                                  cwd=REPO, timeout=1800)
            # L25 (live-found, attempt 9): this asserted on a SUBSTRING of the proof's stdout - it
            # required the literal text "0 orphan"/"orphans: 0". The proof prints structured JSON
            # ("orphans": []), so a run with rc=0, zero orphans and nothing missing was still marked
            # FAIL. A gate that greps prose can disagree with the proof it is gating, and here it did.
            # Assert on the STRUCTURED verdict the proof emits, with rc as the fallback.
            def _lineage_verdict(out):
                """The verdict JSON the proof printed: {covered, counts, settle, orphans}.

                raw_decode, not json.loads: the proof prints a trailing "wrote coverage evidence
                to ..." line after the object, so decoding the whole tail always fails."""
                dec = json.JSONDecoder()
                for i, ch in enumerate(out):
                    if ch != "{":
                        continue
                    try:
                        v, _ = dec.raw_decode(out[i:])
                    except ValueError:
                        continue
                    if isinstance(v, dict) and "covered" in v:
                        return v
                return None

            lv = _lineage_verdict(steps["lineage"]["out"])
            steps["lineage_verdict"] = lv
            lin_ok = steps["lineage"]["rc"] == 0 and bool(lv) and lv.get("covered") is True and not lv.get("orphans")
            check("LIN_zero_orphans", lin_ok,
                  ("rc=%s covered=%s orphans=%d invokes=%s aegis=%s settle=%ss"
                   % (steps["lineage"]["rc"], (lv or {}).get("covered"), len((lv or {}).get("orphans") or []),
                      ((lv or {}).get("counts") or {}).get("cloudtrail_lambda_invokes"),
                      ((lv or {}).get("counts") or {}).get("aegis_calls"),
                      ((lv or {}).get("settle") or {}).get("waited_sec"))
                   if lv else "rc=%s (no structured verdict in output) %s"
                   % (steps["lineage"]["rc"], steps["lineage"]["out"][-160:].replace("\n", " | "))))
        # 0-unexpected-errors sweep
        steps["e2e"] = sh([sys.executable, os.path.join(HERE, "e2e_regression.py"), "--env", env, "--region", region,
                           "--since-minutes", str(int((time.time() * 1000 - t_start) / 60000) + 5),
                           "--runtime-log-group", runtime_log_group, "--out", os.path.join(ev, "FULL-PORTFOLIO-GATE-%s-regression.json" % date)],
                          cwd=REPO, timeout=1800)
        check("E2E_zero_unexpected", steps["e2e"]["rc"] == 0, "rc=%s %s" % (steps["e2e"]["rc"], steps["e2e"]["out"][-200:].replace("\n", " | ")))
    except _TeardownOnly:
        steps["teardown_only"] = True
    except Exception as exc:
        fatal = "%s: %s" % (type(exc).__name__, str(exc)[:300])
        print("FATAL", fatal, flush=True)

    # -- 4. teardown --
    failed = [k for k, v in checks.items() if not v["ok"]] + (["FATAL: " + fatal] if fatal else [])
    if failed and not a.teardown_on_fail:
        steps["teardown_skipped_for_diagnosis"] = failed
        check("teardown_zero_residue", False, "SKIPPED: environment kept for diagnosis of %s" % failed)
    elif not a.skip_teardown:
        try:
            if runtime_id:
                s.client("bedrock-agentcore-control").delete_agent_runtime(agentRuntimeId=runtime_id)
                steps["runtime_deleted"] = runtime_id
        except Exception as exc:
            steps["runtime_deleted"] = "%s: %s" % (type(exc).__name__, str(exc)[:150])
        s3 = s.client("s3"); wb = "%s-capture-worm-%s" % (prefix, acct)

        def _empty_capture_bucket():
            n = 0
            try:
                for page in s3.get_paginator("list_object_versions").paginate(Bucket=wb):
                    for o in page.get("Versions", []) + page.get("DeleteMarkers", []):
                        s3.delete_object(Bucket=wb, Key=o["Key"], VersionId=o["VersionId"], BypassGovernanceRetention=True); n += 1
            except Exception:
                pass
            return n
        try:
            s.client("cloudtrail").stop_logging(Name="%s-capture-all" % prefix); time.sleep(20)
        except Exception as exc:
            steps["capture_trail_stopped"] = type(exc).__name__
        steps["capture_bucket_emptied"] = _empty_capture_bucket()

        # L23 (live-found, attempt 7 teardown 2026-09-06): the workflow stack sat in
        # DELETE_IN_PROGRESS for 30 minutes on the state machine. The PII-canary probe starts an
        # execution that PARKS at the human sign-off wait by design and is never resumed, so it is
        # still RUNNING when teardown begins and CloudFormation waits on it. Any proof that leaves
        # an execution parked at a wait state does the same. Stop them first - they belong to a
        # disposable proof environment that is being destroyed.
        def _stop_running_executions():
            stopped = []
            try:
                sfn_c = s.client("stepfunctions")
                for m in sfn_c.list_state_machines().get("stateMachines", []):
                    if not m["name"].startswith(prefix):
                        continue
                    tok = None
                    while True:
                        kw = {"stateMachineArn": m["stateMachineArn"], "statusFilter": "RUNNING"}
                        if tok:
                            kw["nextToken"] = tok
                        page = sfn_c.list_executions(**kw)
                        for ex in page.get("executions", []):
                            try:
                                sfn_c.stop_execution(executionArn=ex["executionArn"],
                                                     cause="teardown: proof environment %s is being destroyed" % prefix)
                                stopped.append(ex["name"])
                            except Exception as exc:
                                stopped.append("%s: %s" % (ex["name"], type(exc).__name__))
                        tok = page.get("nextToken")
                        if not tok:
                            break
            except Exception as exc:
                return "%s: %s" % (type(exc).__name__, str(exc)[:120])
            return stopped

        steps["executions_stopped"] = _stop_running_executions()
        steps["destroy"] = sh(cdk_cmd("destroy", "--all", "--force", *ctx(env)), cwd=CDK, timeout=3600)
        order = ["lineage", "observability", "gateway", "workflow", "compute"] + ["%s-data" % t for t in TENANTS] + ["network", "identity", "data"]
        notes = []
        for rnd in range(3):
            present = {st["StackName"] for st in cf.describe_stacks()["Stacks"] if st["StackName"].startswith(prefix + "-")}
            if not present:
                break
            notes.append("round %d: re-emptied %d, stopped %s" % (rnd, _empty_capture_bucket(), _stop_running_executions()))
            for suffix in order:
                name = "%s-%s" % (prefix, suffix)
                if name in present:
                    try:
                        cf.delete_stack(StackName=name)
                        cf.get_waiter("stack_delete_complete").wait(StackName=name, WaiterConfig={"Delay": 15, "MaxAttempts": 100})
                        notes.append(name + " deleted")
                    except Exception as exc:
                        notes.append("%s: %s" % (name, type(exc).__name__))
        steps["destroy_remaining"] = notes
        steps["cleanup"] = sh([sys.executable, os.path.join(HERE, "cleanup_retained.py"), "--prefix", prefix, "--region", region,
                               "--i-know-this-deletes-evidence"], cwd=REPO, timeout=1200)
        try:
            cfg = bedrock.get_model_invocation_logging_configuration().get("loggingConfig")
        except Exception:
            cfg = None
        # --teardown-only starts while the env's own logging config is active, so pre_cfg is NOT the
        # baseline: the L6 provider restores the real prior config on delete; only judge that it did.
        if pre_cfg and cfg != pre_cfg and not a.teardown_only:
            try:
                bedrock.put_model_invocation_logging_configuration(loggingConfig=pre_cfg)
                cfg = bedrock.get_model_invocation_logging_configuration().get("loggingConfig")
                steps["model_logging_restored"] = True
            except Exception as exc:
                steps["model_logging_restored"] = "%s: %s" % (type(exc).__name__, str(exc)[:150])
        restored = (cfg == pre_cfg) if (pre_cfg and not a.teardown_only) else (not cfg or "modelinvocations/%s" % prefix not in json.dumps(cfg))
        clean = False
        try:
            out = steps["cleanup"]["out"]; rep = json.loads(out[out.rindex('{\n  "prefix"'):]); clean = bool(rep.get("clean"))
        except Exception:
            clean = steps["cleanup"]["rc"] == 0
        # the runtime's own ECR repo / CodeBuild project are toolkit residue outside the prefix - report them
        try:
            ecr = s.client("ecr"); repos = [r["repositoryName"] for r in ecr.describe_repositories().get("repositories", []) if "benefits_runtime_agent" in r["repositoryName"]]
            steps["toolkit_residue"] = {"ecr_repos": repos}
        except Exception:
            pass
        check("teardown_zero_residue", clean and restored, "destroy_rc=%s clean=%s model_logging_as_before=%s" % (steps["destroy"]["rc"], clean, restored))

    ok = all(c["ok"] for c in checks.values()) and not fatal
    out = os.path.join(REPO, ".build" if a.teardown_only else "evidence",
                       "FULL-PORTFOLIO-GATE-%s%s.json" % (date, "-teardown" if a.teardown_only else ""))
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"env": env, "prefix": prefix, "region": region, "date": date, "PASS": ok, "fatal": fatal,
                   "checks": checks, "steps": steps, "evidence": out}, fh, indent=1, default=str)
    print(json.dumps({"PASS": ok, "checks": checks, "fatal": fatal, "evidence": out}, indent=1, default=str))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
