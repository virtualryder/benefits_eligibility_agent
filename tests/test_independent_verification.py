"""Self-enforcing honesty gate for the independent-verification claim.

WHY THIS EXISTS: "independently verified" is the single most valuable — and most temptingly
fabricable — claim this project can make. An independent reviewer named the absence of third-party
verification as the biggest credibility gap. This gate makes the claim mechanically dependent on a real
signed result:

  * while `evidence/INDEPENDENT-VERIFICATION-RESULT.md` is UNCLAIMED, the docs MUST keep saying that
    independent verification has NOT happened;
  * a result may only be marked VERIFIED if it actually carries a verifier identity and an attached
    machine report — a bare status flip fails the build;
  * the verification kit itself (protocol + harness + template) must stay present and wired together.

The author cannot satisfy this by editing prose. That is the point.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULT = ROOT / "evidence" / "INDEPENDENT-VERIFICATION-RESULT.md"
PROTOCOL = ROOT / "docs" / "INDEPENDENT-VERIFICATION.md"
HARNESS = ROOT / "scripts" / "independent_verify.py"
MATRIX = ROOT / "docs" / "VALIDATED-MATRIX.md"

# Phrases that would assert independent verification has happened.
CLAIM_PATTERNS = [
    r"independently verified",
    r"independent(ly)? (deployment|verification) (was )?(done|complete[d]?|performed)",
    r"third[- ]party (verified|verification (complete|done))",
    r"reproduced by (a|an) (independent|third)",
]


def _status():
    """UNCLAIMED | VERIFIED | VERIFIED WITH FINDINGS | FAILED | (unknown)."""
    text = RESULT.read_text(encoding="utf-8")
    m = re.search(r"STATUS:\s*([A-Z][A-Z ]*)", text)
    return (m.group(1).strip() if m else "UNKNOWN"), text


def test_verification_kit_is_present_and_wired():
    """The protocol, the one-command harness, and the result template must all exist."""
    assert PROTOCOL.exists(), "docs/INDEPENDENT-VERIFICATION.md (the protocol) is missing"
    assert HARNESS.exists(), "scripts/independent_verify.py (the harness) is missing"
    assert RESULT.exists(), "evidence/INDEPENDENT-VERIFICATION-RESULT.md (the result template) is missing"

    protocol = PROTOCOL.read_text(encoding="utf-8")
    assert "independent_verify.py" in protocol, "the protocol must tell the verifier how to run the harness"
    assert "INDEPENDENT-VERIFICATION-RESULT.md" in protocol, "the protocol must point at the result template"

    harness = HARNESS.read_text(encoding="utf-8")
    # the harness must exercise every load-bearing claim, not just deploy
    for required in ("validate_deployment.py", "pii_canary.py", "AdverseNoticeHold",
                     "HumanSignoff", "expect-absent"):
        assert required in harness, f"the harness must exercise/reference {required!r}"


def test_matrix_tells_the_truth_about_independent_verification():
    """While UNCLAIMED, the matrix must still list independent deployment as NOT validated."""
    status, _ = _status()
    matrix = MATRIX.read_text(encoding="utf-8")
    if status == "UNCLAIMED":
        assert re.search(r"Independent deployment[^|]*\|[^|]*(Never done|Not done|not been done)",
                         matrix, re.I), (
            "evidence/INDEPENDENT-VERIFICATION-RESULT.md is UNCLAIMED, so docs/VALIDATED-MATRIX.md must "
            "still list independent deployment as NOT validated")


def test_no_document_claims_independent_verification_while_unclaimed():
    """No doc may assert third-party verification until a signed result exists."""
    status, _ = _status()
    if status != "UNCLAIMED":
        return
    offenders = []
    skip_dirs = {".git", "cdk.out", ".build", "__pycache__", "node_modules"}
    for p in ROOT.rglob("*.md"):
        if any(part in skip_dirs for part in p.parts):
            continue
        if p.name in {"INDEPENDENT-VERIFICATION-RESULT.md", "INDEPENDENT-VERIFICATION.md"}:
            continue  # the kit itself describes the process
        text = p.read_text(encoding="utf-8", errors="replace")
        for pat in CLAIM_PATTERNS:
            for m in re.finditer(pat, text, re.I):
                line = text[: m.start()].count("\n") + 1
                # allow explicit negations ("no independent verification", "not yet")
                ctx = text[max(0, m.start() - 120): m.end() + 60].lower()
                if any(neg in ctx for neg in ("no independent", "not yet", "never done", "not been",
                                              "has not", "awaiting", "until", "not validated",
                                              "biggest credibility gap", "would be")):
                    continue
                offenders.append(f"{p.relative_to(ROOT)}:{line}: {m.group(0)!r}")
    assert not offenders, (
        "A document claims independent verification, but evidence/INDEPENDENT-VERIFICATION-RESULT.md is "
        "still UNCLAIMED:\n  " + "\n  ".join(offenders))


def test_a_verified_result_must_carry_real_attestation():
    """A status flip alone is not enough: a VERIFIED result needs a verifier, a date, and a report."""
    status, text = _status()
    if not status.startswith("VERIFIED"):
        return
    body = text
    # the blank template rows must have been filled in
    assert "_______________________" not in body.split("## Step results")[0], (
        "VERIFIED result still contains blank identity fields — fill in verifier, date, commit SHA")
    assert re.search(r"@", body), "VERIFIED result must record a contactable verifier"
    report = ROOT / "evidence" / "independent-verification-report.json"
    assert report.exists(), (
        "VERIFIED result claims a run, but evidence/independent-verification-report.json is missing")
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data.get("kind") == "independent-verification", "attached report is not a verification report"
    assert not data.get("dry_run"), "a dry-run report cannot support a VERIFIED result"
    assert data.get("verifier"), "the attached report has no verifier recorded"
