#!/usr/bin/env python3
"""INDEPENDENT VERIFICATION HARNESS — for a third party, not the author.

WHY THIS EXISTS: every piece of evidence in this repository was produced by the author. An independent
reviewer correctly discounted it for that reason. This script exists so a DIFFERENT engineer (another AWS
SA, a partner, or the customer) can reproduce the whole validation on their own AWS account with one
command and produce a result the author cannot fabricate.

It runs the full chain and writes a machine-readable report:

  preflight  -> tag/commit integrity, clean tree, toolchain, AWS identity
  offline    -> the full pytest suite
  deploy     -> cdk deploy --all with every Gate-B switch
  validate   -> scripts/validate_deployment.py  (expects deployment_status: PASS)
  canary     -> scripts/pii_canary.py --strict  (expects verdict: PASS, leaks: {})
  happy      -> a new application runs to the HUMAN SIGN-OFF gate and pauses there
  adverse    -> an adverse redetermination WITHOUT advance notice stops at AdverseNoticeHold
  teardown   -> cdk destroy --all, then a residual sweep (expects 0 residual stacks)

Usage
-----
  python scripts/independent_verify.py --verifier "Jane Doe <jane@example.com>" --env iv1
  python scripts/independent_verify.py --dry-run          # preflight + plan only, no AWS calls, no spend

IMPORTANT FOR THE VERIFIER
--------------------------
* Do NOT ask the author for help. If a step fails or needs an undocumented fix, that IS the finding —
  record it with --note and in the results file. A documentation gap is a real defect.
* The AWS account id is never written to the report; only a truncated hash, so two runs are
  distinguishable without disclosing the account.
* This costs real money (VPC endpoints, Lambda, Step Functions, KMS, Bedrock/Comprehend calls). The
  environment is torn down at the end; confirm zero residual before you walk away.
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_TAG_FILE = ROOT / "RELEASE"


def run(cmd, cwd=None, timeout=3600, capture=True):
    """Run a command; return (rc, stdout+stderr). UTF-8 decoded (Windows-safe)."""
    p = subprocess.run(cmd, cwd=cwd or str(ROOT), shell=isinstance(cmd, str),
                       capture_output=capture, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout)
    out = ((p.stdout or "") + (p.stderr or "")).strip() if capture else ""
    return p.returncode, out


def _hash(s):
    return hashlib.sha256((s or "").encode()).hexdigest()[:12]


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class Report:
    def __init__(self, verifier, env, region, dry_run):
        self.data = {
            "kind": "independent-verification",
            "verifier": verifier,
            "env": env,
            "region": region,
            "dry_run": dry_run,
            "started_at": _now(),
            "steps": [],
            "notes": [],
            "verdict": "INCOMPLETE",
        }

    def step(self, name, ok, detail="", **extra):
        self.data["steps"].append(
            {"step": name, "ok": bool(ok), "at": _now(), "detail": detail[:4000], **extra})
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}" + (f" — {detail.splitlines()[0][:160]}" if detail else ""), flush=True)
        return ok

    def note(self, text):
        if text:
            self.data["notes"].append(text)

    def finish(self, path):
        steps = self.data["steps"]
        self.data["verdict"] = "PASS" if steps and all(s["ok"] for s in steps) else "FAIL"
        self.data["finished_at"] = _now()
        path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        return self.data["verdict"]


# ── steps ────────────────────────────────────────────────────────────────────

def preflight(rep, args):
    expected_tag = EXPECTED_TAG_FILE.read_text(encoding="utf-8").strip()

    rc, described = run(["git", "describe", "--tags", "--exact-match"])
    on_tag = (rc == 0 and described.strip() == expected_tag)
    rep.step("preflight.on_release_tag", on_tag,
             f"expected {expected_tag}, got {described.strip() or '(not on a tag)'} — "
             f"check out the tag: git checkout {expected_tag}",
             expected_tag=expected_tag, actual=described.strip())

    rc, status = run(["git", "status", "--porcelain"])
    rep.step("preflight.clean_worktree", rc == 0 and not status.strip(),
             "uncommitted changes present" if status.strip() else "clean")

    rc, sha = run(["git", "rev-parse", "HEAD"])
    rep.data["commit"] = sha.strip()

    rc, ver = run([sys.executable, "--version"])
    rep.step("preflight.python", rc == 0, ver)

    rc, out = run("npx --yes aws-cdk@2 --version")
    rep.step("preflight.cdk_cli", rc == 0, out.splitlines()[-1] if out else "")

    if args.dry_run:
        rep.step("preflight.aws_identity", True, "skipped (--dry-run)")
        return
    rc, acct = run(["aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text"])
    ok = rc == 0 and acct.strip().isdigit()
    # NEVER record the account id — only a truncated hash so runs are distinguishable
    rep.data["account_hash"] = _hash(acct.strip()) if ok else None
    rep.step("preflight.aws_identity", ok,
             "authenticated (account recorded as a truncated hash only)" if ok else acct)


def offline_suite(rep):
    rc, out = run([sys.executable, "-m", "pytest", "tests/", "-q"], timeout=1800)
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    rep.step("offline.pytest", rc == 0, tail)


def deploy(rep, args):
    cmd = (f'npx --yes aws-cdk@2 deploy --all --require-approval never '
           f'-c env={args.env} -c retention_profile=sandbox-demo -c kms=customer-managed '
           f'-c network_mode=private -c identity_mode=pilot -c tenant={args.tenant}')
    rc, out = run(cmd, cwd=str(ROOT / "cdk"), timeout=5400)
    rep.step("deploy.cdk_all", rc == 0, out[-2000:] if rc else "7 stacks deployed")


def validate(rep, args):
    rc, out = run([sys.executable, "scripts/validate_deployment.py",
                   "--env", args.env, "--region", args.region], timeout=1800)
    try:
        payload = json.loads(out[out.index("{"): out.rindex("}") + 1])
    except Exception:
        payload = {}
    ok = payload.get("deployment_status") == "PASS"
    rep.step("validate.deployment", ok, json.dumps(payload) if payload else out[-1500:], result=payload)


def canary(rep, args):
    rc, out = run([sys.executable, "scripts/pii_canary.py",
                   "--prefix", f"ben-{args.env}", "--execute", "--strict"], timeout=1800)
    try:
        payload = json.loads(out[out.index("{"): out.rindex("}") + 1])
    except Exception:
        payload = {}
    ok = payload.get("verdict") == "PASS" and not payload.get("leaks")
    rep.step("canary.strict_zero_pii", ok, json.dumps(payload) if payload else out[-1500:],
             result={k: v for k, v in payload.items() if k != "marker"})


def _sfn_arn(args):
    rc, acct = run(["aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text"])
    return f"arn:aws:states:{args.region}:{acct.strip()}:stateMachine:ben-{args.env}-determination-workflow"


def _ingest(args, application, case_id):
    payload = json.dumps({"application": application, "case_id": case_id})
    tmp = ROOT / f".iv_{case_id}.json"
    tmp.write_text(payload, encoding="utf-8")
    outp = str(tmp) + ".out"
    run(["aws", "lambda", "invoke", "--function-name", f"ben-{args.env}-ingest-application",
         "--region", args.region, "--cli-binary-format", "raw-in-base64-out",
         "--payload", f"file://{tmp}", outp])
    try:
        data = json.loads(pathlib.Path(outp).read_text(encoding="utf-8"))
    except Exception:
        data = {}
    for f in (tmp, pathlib.Path(outp)):
        try:
            f.unlink()
        except Exception:
            pass
    return data


def _start(args, body, name):
    tmp = ROOT / f".iv_start_{name}.json"
    tmp.write_text(json.dumps(body), encoding="utf-8")
    rc, arn = run(["aws", "stepfunctions", "start-execution", "--region", args.region,
                   "--state-machine-arn", _sfn_arn(args), "--input", f"file://{tmp}",
                   "--query", "executionArn", "--output", "text"])
    try:
        tmp.unlink()
    except Exception:
        pass
    return arn.strip() if rc == 0 else ""


def _wait(args, arn, secs=120):
    end = time.time() + secs
    last = "?"
    while time.time() < end:
        rc, st = run(["aws", "stepfunctions", "describe-execution", "--execution-arn", arn,
                      "--query", "status", "--output", "text", "--region", args.region])
        last = st.strip()
        if last != "RUNNING":
            return last
        time.sleep(6)
    return last


def _states(args, arn):
    rc, out = run(["aws", "stepfunctions", "get-execution-history", "--execution-arn", arn,
                   "--region", args.region, "--max-items", "500", "--output", "json",
                   "--query", "events[?type=='TaskStateEntered'||type=='SucceedStateEntered']"
                              ".stateEnteredEventDetails.name"])
    try:
        return json.loads(out)
    except Exception:
        return []


APP = ("Applicant Test Person, SSN 900-00-1234, 5 Main St. Household size 3. "
       "Monthly income $1200. Liquid resources $50.")


def happy_path(rep, args):
    cid = f"IV-HAPPY-{int(time.time())}"
    ing = _ingest(args, APP, cid)
    arn = _start(args, {"case_id": cid, "requester": "independent-verifier",
                        "case_ref": ing.get("case_ref", ""),
                        "redetermination": {"change_type": "NEW"}}, "happy")
    status = _wait(args, arn) if arn else "NOT_STARTED"
    states = _states(args, arn) if arn else []
    # correct behaviour: pauses at the human gate (RUNNING), having traversed every guard
    ok = status == "RUNNING" and "HumanSignoff" in states
    rep.step("happy.reaches_human_gate_and_pauses", ok,
             f"status={status} states={states}", status=status, states=states)


def adverse_hold(rep, args):
    cid = f"IV-ADVERSE-{int(time.time())}"
    ing = _ingest(args, APP, cid)
    arn = _start(args, {"case_id": cid, "requester": "independent-verifier",
                        "case_ref": ing.get("case_ref", ""),
                        "redetermination": {"change_type": "ADVERSE",
                                            "advance_notice_required": False}}, "adverse")
    status = _wait(args, arn) if arn else "NOT_STARTED"
    states = _states(args, arn) if arn else []
    ok = ("AdverseNoticeHold" in states and "DraftNotice" not in states
          and "HumanSignoff" not in states)
    rep.step("adverse.holds_without_advance_notice", ok,
             f"status={status} states={states}", status=status, states=states)


def teardown(rep, args):
    rc, out = run(f"npx --yes aws-cdk@2 destroy --all --force -c env={args.env} "
                  f"-c retention_profile=sandbox-demo -c kms=customer-managed "
                  f"-c network_mode=private -c identity_mode=pilot -c tenant={args.tenant}",
                  cwd=str(ROOT / "cdk"), timeout=5400)
    rep.step("teardown.destroy_all", rc == 0, out[-1500:] if rc else "destroyed")

    rc, out = run([sys.executable, "scripts/validate_deployment.py",
                   "--env", args.env, "--region", args.region, "--expect-absent"], timeout=900)
    try:
        payload = json.loads(out[out.index("{"): out.rindex("}") + 1])
    except Exception:
        payload = {}
    ok = payload.get("deployment_status") == "PASS" and not payload.get("residual_stacks")
    rep.step("teardown.zero_residual", ok, json.dumps(payload) if payload else out[-800:])
    print("\nNOTE: retained-by-policy resources (audit ledger, WORM vault, CMK) may survive by design —\n"
          "see DEPLOYMENT-GUIDE 'Teardown'. Confirm and clean per your account policy.", flush=True)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Independent verification of the benefits agent release.")
    ap.add_argument("--verifier", default="", help='who is running this, e.g. "Jane Doe <jane@example.com>"')
    ap.add_argument("--env", default="iv1", help="deployment env suffix (stacks become ben-<env>-*)")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--tenant", default="ben-independent-verify")
    ap.add_argument("--note", action="append", default=[],
                    help="record an observation / undocumented fix you needed (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="preflight + plan only; no AWS calls, no spend")
    ap.add_argument("--skip-teardown", action="store_true", help="leave the env up (you MUST tear it down)")
    ap.add_argument("--out", default="evidence/independent-verification-report.json")
    a = ap.parse_args()

    if not a.verifier and not a.dry_run:
        sys.exit("--verifier is required for a real run (this is third-party evidence; it must be attributable)")

    rep = Report(a.verifier or "(dry-run)", a.env, a.region, a.dry_run)
    for n in a.note:
        rep.note(n)

    print(f"\n=== Independent verification — env ben-{a.env} — {'DRY RUN' if a.dry_run else 'LIVE'} ===\n")
    preflight(rep, a)
    offline_suite(rep)

    if a.dry_run:
        print("\nDry run: skipping deploy / validate / canary / executions / teardown.")
        print("Plan: deploy(7 stacks, all Gate-B switches) -> validate -> strict canary -> "
              "happy path to human gate -> adverse hold -> destroy -> residual sweep")
    else:
        deploy(rep, a)
        validate(rep, a)
        canary(rep, a)
        happy_path(rep, a)
        adverse_hold(rep, a)
        if a.skip_teardown:
            rep.step("teardown.skipped", False, "--skip-teardown was used; environment still running")
        else:
            teardown(rep, a)

    out_path = ROOT / a.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    verdict = rep.finish(out_path)
    print(f"\n=== VERDICT: {verdict} ===\nreport: {out_path}")
    print("Next: paste the summary into evidence/INDEPENDENT-VERIFICATION-RESULT.md, sign it, and open a PR.")
    sys.exit(0 if verdict == "PASS" else 2)


if __name__ == "__main__":
    main()
