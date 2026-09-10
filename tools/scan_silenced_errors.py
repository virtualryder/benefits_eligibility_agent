#!/usr/bin/env python3
r"""scan_silenced_errors.py - fail CI when a NEW silenced error path appears in a shell script.

WHY THIS EXISTS. On 2026-09-10 the CONN-1 connector took SIX from-zero live runs, roughly ten hours
of AWS time, to prove. Every single root cause was the same defect wearing a different hat - an
error path that could not speak:

  ben-fpa  tok() discarded stderr inside a command substitution, so a real failure reported
           "could not mint a REV token via client 3mejbkk... | " - a guard's words and an empty
           string where AWS's belonged.
  ben-fpd  `aws lambda invoke ... >/dev/null 2>&1` reported only "could not invoke" - no reason.
  ben-fpe  `aws lambda update-function-configuration --environment "Variables={...}"` failed six
           times into >/dev/null because SOR_LABEL contains a comma and the CLI shorthand splits
           on commas. The system of record then ran with EXPECTED_ISS="" - trusting no issuer -
           and refused every governed call with a signature error, while the token was perfect.

And earlier, on 2026-09-09, destroy_connector.sh printed CONNECTOR TEARDOWN: CLEAN over eight live
resources because every probe ended in 2>/dev/null and the aws CLI was not on PATH.

Each was fixed where it was found. This exists because fixing them one at a time is not a strategy:
the next one costs another six runs. A new silenced failure now fails CI instead.

WHAT COUNTS AS SILENCED. stderr discarded (`2>/dev/null`, `>/dev/null 2>&1`) on a logical line whose
exit status nothing consumes - no `||`, no `&&`, not the condition of if/elif/while/until, not
negated with `!`. Line continuations are joined first, because `cmd >/dev/null 2>&1 \` followed by
`&& log ... || err ...` is perfectly honest and must not be flagged.

WHAT IS EXPLICITLY FINE:
  * `X="$(cmd 2>&1 >/dev/null)"` - stderr CAPTURED, stdout discarded. This is the repair idiom used
    throughout lib/connector; flagging it would punish the fix.
  * anything whose failure is consumed on the same logical line.

BASELINE. The sites that existed when this was written are listed in SILENCED_BASELINE with the
reason each is tolerable. The count may SHRINK, never grow. A new one fails, and so does a stale
baseline entry - an allowlist that outlives its entries is how allowlists rot into permission.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".venv", "cdk.out", ".build", "__pycache__", "node_modules", "evidence",
             ".work", "runtime"}

# stderr is thrown away
DISCARDS_STDERR = re.compile(r"2>\s*/dev/null|>\s*/dev/null\s+2>&1")
# stderr is CAPTURED and stdout dropped - the repair idiom, never a finding
CAPTURES_STDERR = re.compile(r"2>&1\s*>\s*/dev/null")
# the exit status is consumed somewhere on this logical line
CONSUMED = re.compile(r"\|\||&&|^\s*(if|elif|while|until)\b|^\s*!\s|\bthen\b")

# MUTATIONS ONLY, and that narrowing is deliberate.
#
# A first draft of this control flagged every discarded stderr and found 28 sites, nearly all of the
# shape X="$(aws ... list|get|describe ... 2>/dev/null)" whose emptiness IS checked on the following
# line. A control that reports 28 findings on a healthy tree gets baselined wholesale and stops
# being read - the failure mode of every linter anyone has ever ignored. Worse here, it would have
# buried the two findings that matter among twenty-six that do not.
#
# Every incident this exists to prevent was a WRITE that failed invisibly:
#   fpe  update-function-configuration  -> the SoR ran with no environment
#   fpd  lambda invoke                  -> "could not invoke", no reason
#   2026-09-09  delete-* in destroy_connector.sh -> CLEAN printed over live resources
# A read that returns empty is usually caught by the next line testing it; a write that fails
# silently leaves the system in a state nobody checked. So this fires on mutations, where the
# evidence is, and says nothing about reads.
MUTATING = re.compile(
    r"\b(create|update|delete|put|attach|detach|add|remove|set|invoke|tag|untag"
    r"|enable|disable|register|deregister|associate|disassociate|modify)[-_a-z]*\b")


def logical_lines(path):
    """Yield (first_line_number, joined_text). Continuations are joined before judging."""
    buf, start = "", None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for n, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if start is None:
                start = n
            stripped = line.rstrip()
            if stripped.endswith("\\"):
                buf += stripped[:-1] + " "
                continue
            buf += stripped
            yield start, buf
            buf, start = "", None
    if buf:
        yield start or 1, buf


def findings(root=ROOT):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if not fn.endswith(".sh"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root).replace("\\", "/")
            for n, text in logical_lines(path):
                s = text.strip()
                if not s or s.startswith("#"):
                    continue
                if not DISCARDS_STDERR.search(s) or CAPTURES_STDERR.search(s):
                    continue
                if CONSUMED.search(s):
                    continue
                if not MUTATING.search(s):
                    continue
                out.append((rel, n, s[:120]))
    return out


# Sites that existed when this control was written, each with the reason it is tolerable.
# This list may SHRINK, never grow. Entries are (path, logical-line): why.
#
# The first run of this control found three. Two were in lib/engine/demo.sh - a shared /tmp file
# across two lambda invokes, which made a FALSE PASS reachable in the separation-of-duties
# assertion (stale '"approved": true' plus a failing invoke reads as a valid approval). Those were
# FIXED, not baselined. Only one earned an entry, and it earned it by having the check that can
# fail immediately downstream.
SILENCED_BASELINE = {
    ("lib/connector/deploy_connector.sh", 126):
        "admin-create-user: UsernameExistsException IS the normal re-run case, and the very next "
        "call - admin-set-user-password - fails loudly if the user genuinely does not exist. The "
        "check that can fail is downstream of the one that is allowed to; that ordering is the "
        "whole justification and is spelled out at the call site.",
}


def main():
    found = findings()
    baseline = set((p, n) for (p, n) in SILENCED_BASELINE)
    new = [f for f in found if (f[0], f[1]) not in baseline]
    stale = [b for b in baseline if b not in set((p, n) for p, n, _ in found)]

    if new:
        print("SILENCED ERROR PATHS - %d new site(s).\n" % len(new))
        print("stderr is discarded and nothing consumes the exit status, so a failure here is")
        print("indistinguishable from success. This is the defect that cost six live runs on")
        print("2026-09-10; see the module docstring.\n")
        print("Fix by making the failure speak - capture it and act on it:")
        print('    ERR="$(cmd 2>&1 >/dev/null)" || err "what failed: $ERR"')
        print("or by consuming the status on the same line (`|| true` is acceptable ONLY when a")
        print("later check can still fail loudly - say so in a comment).\n")
        for p, n, s in new:
            print("  %s:%d\n      %s" % (p, n, s))
        return 1

    if stale:
        print("STALE BASELINE - %d entr(y|ies) no longer exist:" % len(stale))
        for p, n in sorted(stale):
            print("  %s:%d" % (p, n))
        print("\nRemove them. An allowlist that outlives its entries stops being an allowlist and")
        print("becomes permission.")
        return 1

    print("silenced-error scan: clean (%d baselined site(s), 0 new)" % len(baseline))
    return 0


if __name__ == "__main__":
    sys.exit(main())
