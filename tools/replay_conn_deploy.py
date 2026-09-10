"""Replay the CONN_deploy rule against evidence we already own.

The rule, now shipped in scripts/full_portfolio_gate.py: CONN_deploy passes only when the
artifacts are present AND the deploy script exited 0 AND the outbound leg was proven. It used to
pass on artifacts alone, which is how it went green on fpd and fpe over a connector whose system
of record trusted nothing. Run from the repo root: python tools/replay_conn_deploy.py

A rule is only worth shipping if it DISCRIMINATES. This replays it against the committed evidence
of three runs whose real outcome we know:
    fpd  outbound leg broken  -> must FAIL
    fpe  outbound leg broken  -> must FAIL
    fpf  connector proven     -> must PASS
If it does not split them exactly that way, the rule is wrong and no live run should be spent on it.
"""
import json
import subprocess
import sys

EV = "evidence/FULL-PORTFOLIO-GATE-benefits_runtime_agent.json"
RUNS = [("fda1a53", "fpd", False), ("2ecb03b", "fpe", False), ("490ca7e", "fpf", True)]


def evidence_at(commit):
    out = subprocess.run(["git", "show", "%s:%s" % (commit, EV)],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit("cannot read %s at %s: %s" % (EV, commit, out.stderr[:200]))
    return json.loads(out.stdout)


def current_rule(ev):
    """What the gate does today: artifacts only."""
    a = ev["steps"].get("conn_artifacts") or {}
    return all(v is True for k, v in a.items() if isinstance(v, bool))


def proposed_rule(ev):
    """artifacts AND rc==0 AND the outbound leg proven."""
    a = ev["steps"].get("conn_artifacts") or {}
    artifacts_ok = all(v is True for k, v in a.items() if isinstance(v, bool))
    rc_ok = ev["steps"].get("conn_deploy", {}).get("rc") == 0
    blob = json.dumps(ev["steps"].get("conn_deploy", {}))
    outbound_ok = "outbound leg OK" in blob
    return artifacts_ok and rc_ok and outbound_ok, artifacts_ok, rc_ok, outbound_ok


def main():
    print("%-5s %-9s %-9s %-9s %-9s  %-9s %s" %
          ("run", "artifacts", "rc==0", "outbound", "TODAY", "PROPOSED", "verdict"))
    wrong = 0
    for commit, name, should_pass in RUNS:
        ev = evidence_at(commit)
        today = current_rule(ev)
        prop, art, rc, outb = proposed_rule(ev)
        ok = (prop == should_pass)
        wrong += 0 if ok else 1
        print("%-5s %-9s %-9s %-9s %-9s  %-9s %s" %
              (name, art, rc, outb, "PASS" if today else "FAIL",
               "PASS" if prop else "FAIL",
               "correct" if ok else "WRONG (expected %s)" % ("PASS" if should_pass else "FAIL")))
    print()
    if wrong:
        print("RULE REJECTED: %d of %d runs classified wrongly. Do not ship it." % (wrong, len(RUNS)))
        return 1
    # Discrimination is the point: a rule that passes everything is not a rule.
    if all(current_rule(evidence_at(c)) for c, _, _ in RUNS):
        print("note: today's artifacts-only rule passes ALL THREE, including the two broken runs.")
    print("RULE ACCEPTED: fails both broken runs, passes the proven one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
