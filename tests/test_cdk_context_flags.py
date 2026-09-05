"""cdk.json feature-flag gate — a removed-in-v2 flag makes the REAL deploy impossible.

WHY THIS EXISTS. `cdk/cdk.json` carried `@aws-cdk/core:enableStackNameDuplicates`, a CDK **v1** feature
flag that was REMOVED in v2. On the pinned CDK (aws-cdk-lib 2.262.1) the CLI raises:

    RuntimeError: Unsupported feature flag '@aws-cdk/core:enableStackNameDuplicates'.
    This flag existed on CDKv1 but has been removed in CDKv2.

That is fatal: `cdk synth` and `cdk deploy` both abort, so the documented deployment path could not be
followed at all. It was found by actually walking the runbook on 2026-07-28, not by the test suite.

**Why the existing tests missed it.** `tests/test_cdk_stacks.py` builds stacks with
`aws_cdk.assertions.Template.from_stack()`, which instantiates constructs directly in-process and
**never reads `cdk.json`**. Only the `cdk` CLI loads that file. So the whole CDK suite stayed green
while the real deployment was broken — the unit tests and the shipped artifact disagreed.

This gate closes that gap cheaply: it asserts no known removed-in-v2 flag is present, without needing
Node or a real synth in CI.
"""
import json
import pathlib

CDK_JSON = pathlib.Path(__file__).resolve().parents[1] / "cdk" / "cdk.json"

# Flags that existed in CDK v1 and are REMOVED in v2 — presence is a hard CLI error.
REMOVED_IN_V2 = {
    "@aws-cdk/core:enableStackNameDuplicates",
    "@aws-cdk/core:newStyleStackSynthesis",
    "aws-cdk:enableDiffNoFail",
}


def test_cdk_json_parses():
    assert CDK_JSON.exists(), "cdk/cdk.json is missing"
    json.loads(CDK_JSON.read_text(encoding="utf-8"))


def test_no_removed_v1_feature_flags():
    """A removed-in-v2 flag aborts `cdk synth`/`cdk deploy` — the documented path stops working."""
    ctx = json.loads(CDK_JSON.read_text(encoding="utf-8")).get("context", {})
    offenders = sorted(set(ctx) & REMOVED_IN_V2)
    assert not offenders, (
        "cdk/cdk.json contains CDK v1 feature flags that were REMOVED in v2; the CDK CLI will refuse "
        f"to synth or deploy: {offenders}. Delete them from the context block.")


APP_PY = pathlib.Path(__file__).resolve().parents[1] / "cdk" / "app.py"


def test_production_profile_gate_present_and_complete():
    """deep-dive #6: `env=prod` must FAIL CLOSED at synth unless EVERY production control is explicitly
    enabled, so 'production' can never synthesize with dev defaults (public network, AWS-managed KMS,
    sandbox identity, WAF/perimeter/model-logging/account-capture off). Guards that the synth-time gate
    exists and still enforces each required control — a pure-source check (no Node/synth needed), proven
    live to refuse with `-c env=prod` (see RELEASE-MANIFEST / GAP register)."""
    src = APP_PY.read_text(encoding="utf-8")
    assert "_require_production_controls" in src and "PRODUCTION PROFILE REFUSED" in src, \
        "the production-profile synth gate is missing from cdk/app.py"
    for control in ("kms=customer-managed", "retention_profile=production-reference", "network_mode=private",
                    "identity_mode!=sandbox", "oidc_issuer_url", "waf=1", "perimeter=1", "model_logging=1",
                    "capture_all=1", "capture_lock_mode=COMPLIANCE"):
        assert control in src, f"the production gate no longer enforces: {control}"
    # the only sanctioned bypass is the explicit, audited override
    assert "allow_insecure_prod" in src, "the audited-exception override must remain explicit"
