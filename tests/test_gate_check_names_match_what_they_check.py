"""#231 / L37: a gate check must not claim more than it verifies.

The full-portfolio gate reported a check called `teardown_zero_residue` as PASS while the block
immediately above it recorded the residue it had not looked at:

    steps["toolkit_residue"] = {"ecr_repos": [...]}          # named, never judged
    check("teardown_zero_residue", clean and restored, ...)  # clean = stacks; restored = log config

The AgentCore toolkit's ECR repository and CodeBuild project live outside the deployment prefix and
teardown does not delete them. The repository accrues one image per gate run - measured monotonic
across two attempts (20 -> 22 images, 2,544 -> 2,799 MB). The cost is negligible; the CLAIM was the
defect, because "zero residue" is exactly the sentence a reviewer would quote.

The check is now `teardown_zero_stack_residue` and the toolkit residue is measured beside it and
explicitly marked `gated: false`. This test keeps the overclaiming name from coming back, and keeps
the residue measurement from being quietly reduced to a list of names again.
"""
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATES = ["scripts/full_portfolio_gate.py", "scripts/tier1_regate.py"]

# `check("<name>", ...)` calls in the gate harnesses.
_CHECK = re.compile(r'check\(\s*"([A-Za-z0-9_]+)"')

# A name that promises the absence of everything, from a check that verifies a subset.
_OVERCLAIMING = {"teardown_zero_residue"}


def test_no_gate_check_is_named_for_more_than_it_verifies():
    offenders = []
    for rel in GATES:
        p = ROOT / rel
        if not p.exists():
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for m in _CHECK.finditer(line):
                if m.group(1) in _OVERCLAIMING:
                    offenders.append(
                        "%s:%d defines check %r - it verifies stacks and the model-logging config, "
                        "not the absence of everything the run created (the toolkit ECR repository "
                        "survives teardown, L37). Use teardown_zero_stack_residue."
                        % (rel, n, m.group(1)))
    assert not offenders, "\n  ".join(offenders)


def test_the_toolkit_residue_is_measured_not_just_named():
    """A list of repository names is not a measurement; the next run needs a number to compare."""
    src = (ROOT / "scripts" / "full_portfolio_gate.py").read_text(encoding="utf-8")
    assert 'steps["toolkit_residue"]' in src, "the toolkit residue is no longer recorded at all"
    for needed in ('"gated": False', '"images"', '"size_mb"', "describe_images"):
        assert needed in src, (
            "toolkit_residue no longer records %s - L37 was found because the residue was named but "
            "not counted, and the fix was to count it" % needed)


def test_the_evidence_renderer_still_describes_the_old_key():
    """Evidence files from before the rename are records of past runs and must stay readable."""
    p = ROOT / "scripts" / "render_gate_evidence.py"
    if not p.exists():
        return
    src = p.read_text(encoding="utf-8")
    for key in ("teardown_zero_residue", "teardown_zero_stack_residue"):
        assert '"%s"' % key in src, (
            "render_gate_evidence.py no longer describes %r; historical evidence carrying that key "
            "would render without a description" % key)


def test_conn_deploy_outbound_marker_is_pinned_to_what_the_deploy_actually_logs():
    """The gate greps the deploy output for a sentence another file prints. Pin them together.

    CONN_deploy used to pass on artifacts alone, which is how it went green on the ben-fpd and
    ben-fpe runs over a connector whose system of record trusted nothing. It now also requires
    that the outbound leg was exercised, which it decides by looking for a marker string in the
    deploy output. Nothing else ties that string to the `log` line in deploy_connector.sh that
    emits it, so a harmless reword there would silently turn a good run red and the message would
    blame the connector. This test is the tie.
    """
    marker = "outbound leg OK"
    gate = (ROOT / "scripts" / "full_portfolio_gate.py").read_text(encoding="utf-8")
    deploy = (ROOT / "lib" / "connector" / "deploy_connector.sh").read_text(encoding="utf-8")
    assert '"%s"' % marker in gate, (
        "the gate no longer looks for %r; if the outbound check moved, move this test with it"
        % marker)
    assert marker in deploy, (
        "lib/connector/deploy_connector.sh no longer logs %r, but scripts/full_portfolio_gate.py "
        "still requires it to declare CONN_deploy a pass. Every real run would fail there, and the "
        "failure would read as a connector defect rather than a reworded log line." % marker)
