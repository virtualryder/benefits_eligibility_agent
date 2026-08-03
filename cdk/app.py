#!/usr/bin/env python3
"""CDK app — the PRIMARY customer deployment path for the Public-Benefits Eligibility Screening &
Determination-Support Assistant (P0-5).

Replaces the imperative shell engine for customer deployments with reviewable, parameterized IaC:
explicit IAM, exact-ARN outputs (P0-7), configurable audit retention profiles incl. COMPLIANCE (P0-12),
no built-in users or default passwords (P0-6 — identity is a federation-ready pool only), a
sanitized-artifacts store (P0-1), an R3-2 pass-by-reference case store, and the DETERMINISTIC workflow
controller state machine with the due-process advance-notice HOLD (P0-2).

    cdk synth -c env=dev -c retention_profile=sandbox-demo
    cdk deploy --all -c env=prod -c retention_profile=production-reference -c kms=customer-managed \
        -c network_mode=private -c identity_mode=pilot -c tenant=<agency-id>

The AgentCore control-plane attachment (gateway targets + Cedar policy load) consumes the CfnOutputs
of these stacks; see cdk/README.md. The legacy shell engine remains an internal reference only.

Benefits has NO external data dependency (the eligibility engine runs on public HHS Federal Poverty
Guidelines baked in as configuration — no lookup call), so `network_mode=private` gives ZERO public
egress: the governed Lambdas have no internet route at all and reach AWS services only via private
VPC endpoints.
"""
import os
import shutil

import aws_cdk as cdk

from ben_stacks.data_stack import DataStack
from ben_stacks.network_stack import NetworkStack
from ben_stacks.compute_stack import ComputeStack
from ben_stacks.workflow_stack import WorkflowStack
from ben_stacks.identity_stack import IdentityStack
from ben_stacks.observability_stack import ObservabilityStack
from ben_stacks.gateway_stack import GatewayStack

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def stage_lambda_bundle():
    """Stage tools + controls into one flat Lambda asset dir.

    The governance controls come from the PINNED `governed-core` package, not from a copy in this
    repo. That is the whole point: this repo once carried its own copy of these modules and the copy
    was missing the exactly-once FINAL# finalization control that two sibling agents had, which for a
    benefits determination is a due-process risk — the same adverse action committed twice against
    the same person. A copy can silently diverge; a hash-pinned wheel cannot.

    Layering is deliberate and ordered:
      1. governed_core.controls_dir()  — the shared, versioned control plane
      2. lib/controls                  — this agent's domain-shaped modules (mask_pii, provenance,
                                         workflow_guards, sanitized, case_store, ingest_case, tenancy)
      3. agents/.../tools              — the tool handlers

    Later layers overwrite earlier ones, so a domain module could in principle shadow a core module.
    Every such shadow must be DECLARED, and `tests/test_core_dependency.py` fails the build if one is
    not — an undeclared shadow would reintroduce the drift by the back door.
    """
    import governed_core

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".build", "lambda-src")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    for src in (str(governed_core.controls_dir()),
                os.path.join(REPO, "lib", "controls"),
                os.path.join(REPO, "agents", "benefits-eligibility", "tools")):
        for f in os.listdir(src):
            if f.endswith(".py"):
                shutil.copy2(os.path.join(src, f), os.path.join(out, f))
    # Stamp the staged bundle with the core version actually used, so a deployed artifact can be
    # traced back to a released core rather than "whatever was in the tree that day".
    with open(os.path.join(out, "CORE_VERSION"), "w", encoding="utf-8") as fh:
        fh.write(governed_core.__version__ + "\n")
    return out


app = cdk.App()
env_name = app.node.try_get_context("env") or "dev"
profile = app.node.try_get_context("retention_profile") or "sandbox-demo"
prefix = f"ben-{env_name}"
asset_dir = stage_lambda_bundle()

data = DataStack(app, f"{prefix}-data", prefix=prefix, retention_profile=profile,
                 kms_mode=app.node.try_get_context("kms") or "aws-managed")
network = None
if (app.node.try_get_context("network_mode") or "public") == "private":
    network = NetworkStack(app, f"{prefix}-network", prefix=prefix)
compute = ComputeStack(app, f"{prefix}-compute", prefix=prefix, asset_dir=asset_dir, data=data,
                       provenance_secret=app.node.try_get_context("provenance_secret") or "",
                       network=network,
                       tenant=app.node.try_get_context("tenant") or "")
workflow = WorkflowStack(app, f"{prefix}-workflow", prefix=prefix, compute=compute, data=data)
identity = IdentityStack(
    app, f"{prefix}-identity", prefix=prefix,
    identity_mode=app.node.try_get_context("identity_mode") or "sandbox",
    federation={
        "issuer_url": app.node.try_get_context("oidc_issuer_url") or "",
        "client_id": app.node.try_get_context("oidc_client_id") or "",
        "client_secret_arn": app.node.try_get_context("oidc_client_secret_arn") or "",
    })
observability = ObservabilityStack(app, f"{prefix}-observability", prefix=prefix,
                                   compute=compute, workflow=workflow, data=data)
gateway = GatewayStack(app, f"{prefix}-gateway", prefix=prefix, compute=compute, identity=identity)

for s in (data, compute, workflow, identity, observability, gateway) + ((network,) if network else ()):
    cdk.Tags.of(s).add("app", "benefits-eligibility-agent")
    cdk.Tags.of(s).add("env", env_name)
    cdk.Tags.of(s).add("cost-center", "governed-agents")

app.synth()
