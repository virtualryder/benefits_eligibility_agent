"""AgentCore policy names are unique per ACCOUNT and REGION, so every policy name must be prefixed.

This is the defect that cost four full-portfolio gate runs on 2026-09-08 and three wrong diagnoses.

lib/engine/render.py had said it all along: "AgentCore Policy names are unique per account/region,
and template agents share logical names (mask_before_assess, no_self_commit, ...). Prefixing (e.g.
ben_mask_before_assess) lets multiple agents coexist in one account." The CDK path did not do it -
it used the bare filename stem - so a pharmacovigilance deployment that was still up held
`mask_before_assess` account-wide, and every benefits deploy after it failed on the FIRST shared
name with `ConflictException: Policy with the same name already exists`. The message names neither
the policy nor the engine holding it, which is why it read like a race for three rounds.

Verified live in a brand-new engine before this test was written:

    mask_before_assess      (held by the leftover pv_fp engine)  -> ConflictException
    mask_before_causality   (held by the leftover pv_fp engine)  -> ConflictException
    ben_mask_before_assess  (free)                               -> CREATED
    caseworker_permit       (free)                               -> CREATED

The four policies that always succeeded in every failed run were exactly the four whose names the
PV engine did not hold. Nothing about the policy set was wrong.
"""
import importlib.util
import pathlib
import re
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
STACK = REPO / "cdk" / "ben_stacks" / "gateway_stack.py"
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")   # the API's rule for policy and engine names


@pytest.fixture(scope="module")
def policies():
    """_policies() without importing aws_cdk: exec just that function from the source."""
    src = STACK.read_text(encoding="utf-8")
    start = src.index("def _policies(")
    end = src.index("\nclass ", start)
    ns = {"REPO": REPO, "re": re, "pathlib": pathlib}
    exec(compile(src[start:end], str(STACK), "exec"), ns)          # noqa: S102 - our own source
    return ns["_policies"]


def test_every_policy_name_is_prefixed(policies):
    for p in policies("ben-fp2", multitenant=True, perimeter=True):
        assert p["name"].startswith("ben_fp2_"), p["name"]


def test_names_match_the_api_character_rule(policies):
    """Hyphens are legal in a stack prefix and illegal in a policy name."""
    for p in policies("ben-fp2", multitenant=True, perimeter=True):
        assert NAME_RE.match(p["name"]), p["name"]
        assert "-" not in p["name"]


def test_the_prefix_actually_varies_with_the_environment(policies):
    """A hardcoded prefix would pass the test above and still collide between environments."""
    a = {p["name"] for p in policies("ben-fp2", perimeter=True)}
    b = {p["name"] for p in policies("ben-demo", perimeter=True)}
    assert a and b and not (a & b), "two environments must not share a single policy name"


def test_the_exact_cross_pack_collision_cannot_recur(policies):
    """The names the leftover pv_fp engine held, which blocked four gate runs.

    A pack deployed alongside another must not claim any of these bare names.
    """
    pv_held = {"budget_before_draft_narrative", "consent_purpose_before_assess_seriousness",
               "mask_before_assess", "mask_before_causality", "mask_before_draft",
               "no_self_causality_commit", "no_self_submit", "pv_reviewer_permit",
               "require_entitlement", "require_service_window", "require_tenant"}
    ours = {p["name"] for p in policies("ben-fp2", multitenant=True, perimeter=True)}
    assert not (ours & pv_held), "collides with a co-deployed pack: %s" % sorted(ours & pv_held)


def test_the_shared_logical_names_are_still_there_underneath(policies):
    """Prefixing must not have renamed or dropped a control - only namespaced it.

    mask_before_assess is the policy the four failed runs died on; it must still be deployed,
    under a prefixed name.
    """
    stems = {p["name"].split("ben_fp2_", 1)[1] for p in policies("ben-fp2", multitenant=True, perimeter=True)}
    for expected in ("mask_before_assess", "mask_before_draft", "caseworker_permit",
                     "consent_purpose_before_assess", "require_service_window"):
        assert expected in stems, expected


def test_scope_filtering_still_works(policies):
    """The perimeter profile adds policies; the baseline profile must not carry them."""
    base = {p["name"] for p in policies("ben-fp2")}
    perim = {p["name"] for p in policies("ben-fp2", perimeter=True)}
    assert base < perim
    assert "ben_fp2_consent_purpose_before_assess" in perim - base


def test_no_duplicate_names_within_one_deployment(policies):
    names = [p["name"] for p in policies("ben-fp2", multitenant=True, perimeter=True)]
    assert len(names) == len(set(names))
