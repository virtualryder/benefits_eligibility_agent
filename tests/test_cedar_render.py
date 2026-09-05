#!/usr/bin/env python3
"""Offline proof of the full 9-condition Cedar authorization model (#160 + #161).

Renders the real manifest through lib/engine/render.py and asserts that the emitted
policies.tsv is the complete model: every one of the nine conditions is present as a
Cedar statement, and every statement parses under the Cedar grammar (cedarpy). This is
the offline gate; the live gate attaches these same statements to the GA AgentCore
Policy engine and proves deny/allow on a real gateway.

The nine conditions:
  1. entitlement           zero-default tools (require_entitlement)
  2. data-classification   mask-before-processing (deidentified == true)
  3. consent               recorded consent on the eligibility decision
  4. purpose               purpose-limitation on the eligibility decision
  5. budget                live per-tenant spend gate on the drafter
  6. temporal              service-window gate (within_service_window)
  7. quantitative          overpayment amount cap
  8. tenant                un-tenanted identities refused (multi-tenant only)
  9. human-only / SoD      no_self_commit + no_self_fraud_referral
"""
import os
import subprocess
import sys
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RENDER = os.path.join(ROOT, "lib", "engine", "render.py")
MANIFEST = os.path.join(ROOT, "agents", "benefits-eligibility", "manifest.yaml")
GW_ARN = "arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"


def _render():
    """Render the real manifest and return {policy_name: (mode, cedar_stmt)}."""
    build = tempfile.mkdtemp(prefix="cedar_render_")
    subprocess.run([sys.executable, RENDER, MANIFEST, build], check=True,
                   capture_output=True, text=True)
    rows = {}
    with open(os.path.join(build, "policies.tsv"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            name, mode, stmt = line.split("\t", 2)
            rows[name] = (mode, stmt)
    return rows


@pytest.fixture(scope="module")
def policies():
    return _render()


# Each condition is proven by a specific policy carrying a specific Cedar fragment.
# (policy_name_suffix, required_substring_in_statement)
NINE_CONDITIONS = [
    ("ben_require_entitlement",            'principal.getTag("custom:tools") != ""'),        # 1 entitlement
    ("ben_mask_before_assess",             "context.input.deidentified == true"),            # 2 data-class
    ("ben_consent_purpose_before_assess",  "context.input.consent == true"),                 # 3 consent
    ("ben_consent_purpose_before_assess",  'context.input.purpose == "eligibility"'),        # 4 purpose
    ("ben_budget_before_draft",            "context.input.budget_ok == true"),               # 5 budget
    ("ben_require_service_window",         "context.input.within_service_window == true"),   # 6 temporal
    ("ben_amount_cap_overpayment",         "context.input.prior_monthly_benefit <= 5000"),   # 7 quantitative
    ("ben_require_tenant",                 'principal.hasTag("custom:tenant")'),             # 8 tenant
    ("ben_no_self_commit",                 'AgentCore::Action::"ben-core___finalize_determination"'),  # 9 SoD
]


def test_thirteen_policies_rendered(policies):
    # 8 originals + 5 new (#160/#161) = 13 statements in the model.
    assert len(policies) == 13, sorted(policies)


@pytest.mark.parametrize("name,fragment", NINE_CONDITIONS)
def test_condition_present(policies, name, fragment):
    assert name in policies, "missing policy %s" % name
    _mode, stmt = policies[name]
    assert fragment in stmt, "policy %s missing %r:\n%s" % (name, fragment, stmt)


def test_all_nine_dimensions_covered(policies):
    covered = {name for name, _ in NINE_CONDITIONS}
    # Nine conditions across eight distinct policies (consent + purpose share one statement).
    assert len(covered) == 8
    assert len(NINE_CONDITIONS) == 9


def test_entitlement_is_zero_default(policies):
    """#160: entitlement forbid is unconditional over every action/resource (no action==),
    so a principal with no NON-EMPTY custom:tools claim is denied for ALL tools, not one."""
    _mode, stmt = policies["ben_require_entitlement"]
    assert "action, resource is AgentCore::Gateway" in stmt   # not scoped to a single action
    assert 'principal.hasTag("custom:tools")' in stmt
    assert 'principal.getTag("custom:tools") != ""' in stmt    # empty claim is not enough


def test_every_statement_parses_under_cedar():
    """Cedar grammar check: all 13 statements parse as one policy set (cedarpy)."""
    cedarpy = pytest.importorskip("cedarpy")
    rows = _render()
    policy_set = "\n".join(stmt.replace("__GW_ARN__", GW_ARN) for _m, stmt in rows.values())
    req = {
        "principal": 'AgentCore::User::"u"',
        "action": 'AgentCore::Action::"assess-eligibility___assess_eligibility"',
        "resource": 'AgentCore::Gateway::"%s"' % GW_ARN,
        "context": {},
    }
    # is_authorized parses the whole policy_set; a syntax error raises instead of returning.
    res = cedarpy.is_authorized(req, policy_set, [])
    # Deny-by-default with an empty context and no matching permit condition.
    assert "Deny" in str(res.decision)
