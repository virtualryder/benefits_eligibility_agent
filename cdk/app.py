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
    """Stage tools + shared controls into one Lambda asset dir (what the shell engine did per-zip)."""
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".build", "lambda-src")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    for src in (os.path.join(REPO, "agents", "benefits-eligibility", "tools"),
                os.path.join(REPO, "lib", "controls")):
        for f in os.listdir(src):
            if f.endswith(".py"):
                shutil.copy2(os.path.join(src, f), os.path.join(out, f))
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
