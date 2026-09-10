"""The control that stops the defect which cost six live runs on 2026-09-10.

Every root cause of the CONN-1 hunt was an error path that could not speak: discarded stderr on a
command whose failure nothing consumed. tools/scan_silenced_errors.py finds those; this makes it
fail CI rather than fail a reader's attention.
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import scan_silenced_errors as scan  # noqa: E402


def test_no_new_silenced_error_paths():
    """No mutating command may discard its stderr with nothing consuming its exit status."""
    found = scan.findings()
    baseline = set(scan.SILENCED_BASELINE)
    new = [f for f in found if (f[0], f[1]) not in baseline]
    assert not new, (
        "New silenced error path(s). stderr is discarded and nothing consumes the exit status, so a "
        "failure is indistinguishable from success:\n  "
        + "\n  ".join("%s:%d: %s" % f for f in new)
        + "\n\nMake the failure speak:  ERR=\"$(cmd 2>&1 >/dev/null)\" || err \"...: $ERR\""
    )


def test_baseline_has_no_stale_entries():
    """An allowlist that outlives its entries stops being an allowlist and becomes permission."""
    live = set((p, n) for p, n, _ in scan.findings())
    stale = [b for b in scan.SILENCED_BASELINE if b not in live]
    assert not stale, (
        "Baseline entries that no longer match a real site (the code moved or was fixed) - "
        "remove them: %s" % stale)


def test_every_baseline_entry_states_a_reason():
    """A baselined site without a written justification is an unexplained exception."""
    for key, why in scan.SILENCED_BASELINE.items():
        assert why and len(why) > 40, "baseline %s needs a real reason, got %r" % (key, why)


def test_the_scanner_actually_catches_one():
    """NEGATION TEST - the whole point of L60.

    A control that has never been shown to fail is not evidence. Plant the exact defect from ben-fpe
    (a mutating aws call whose stderr goes to /dev/null with nothing checking the status) in a
    throwaway tree and require the scanner to find it. If this ever stops failing, the two tests
    above are decoration.
    """
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "planted.sh"), "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/env bash\n"
                     'aws lambda update-function-configuration --function-name "$FN" \\\n'
                     '  --environment "Variables={A=1}" --region "$REGION" >/dev/null 2>&1\n')
        assert scan.findings(root=tmp), "the scanner did not catch a planted silenced mutation"


def test_the_scanner_does_not_flag_the_repair_idiom():
    """`ERR="$(cmd 2>&1 >/dev/null)" || err ...` captures stderr - it is the fix, never a finding.

    Flagging it would punish exactly the change this control exists to encourage.
    """
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "good.sh"), "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/env bash\n"
                     'ERR="$(aws lambda update-function-configuration --function-name "$FN" \\\n'
                     '  --environment file://env.json --region "$REGION" 2>&1 >/dev/null)" \\\n'
                     '  || err "could not set the environment: $ERR"\n')
        assert not scan.findings(root=tmp), "the scanner flagged the repair idiom"
