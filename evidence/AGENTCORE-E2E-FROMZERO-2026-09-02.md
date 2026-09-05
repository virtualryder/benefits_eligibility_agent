# AgentCore from-zero end-to-end run — 2026-09-02 (env `e2e`)

Account **864217980669** · us-east-1 · run by `dryder`. Synthetic data only. Deploy → prove → destroy.

## From-zero deploy (clean namespace)

A true from-scratch deploy: `cdk deploy --all -c env=e2e -c retention_profile=sandbox-demo
-c tenant=e2e-agency`. All **6 stacks CREATE_COMPLETE** (`ben-e2e-{data,identity,compute,workflow,gateway,observability}`).

> **Finding (documented for the runbook):** a first attempt at `env=demo` **failed** because
> `ben-demo-audit-ledger` (DynamoDB) still existed — `cdk destroy` deliberately **retains** the audit
> ledger (evidence must not be auto-deleted), so the CFN stacks are gone but the WORM/ledger resource
> persists. A clean from-zero deploy therefore needs either `scripts/cleanup_retained.py` first or a
> fresh env prefix. This run used a fresh `env=e2e` namespace (non-destructive to prior evidence).

## Control-plane: AgentCore in ENFORCE (live reads)

- Gateway `ben-e2e-ben-gw-tnqgqwbsao` — status **READY**, protocol **MCP**, authorizer **CUSTOM_JWT**.
  URL `https://ben-e2e-ben-gw-tnqgqwbsao.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp`.
- Policy engine `ben_e2e_ben_authz-c14nz3aueh` — gateway `policyEngineConfiguration.mode` = **ENFORCE**
  (Cedar deny-by-default, forbid-wins). Same Cedar set as `policies/*.cedar` (caseworker_permit,
  four mask_before_*, no_self_commit, no_self_fraud_referral).

## Data-plane: `scripts/validate_deployment.py --env e2e` machine verdict

```
release: dev · env: e2e
stacks: COMPLETE
secret: PRESENT
masking_control: PASS               (fail-closed de-identification runs)
guard_genuine: PASS                 (a genuine sanitized_ref is accepted)
forged_ref_denied: PASS             (a FORGED sanitized_ref is DENIED - governed deny path)
ingest_pass_by_reference: PASS      (R3-2 pass-by-reference case store)
workflow: PASS:RUNNING(awaiting human gate)   (SoD human sign-off gate reached, not auto-committed)
deployment_status: PASS
```

This exercises the governed deny path (`forged_ref_denied`), fail-closed masking (`masking_control`),
and the separation-of-duties human gate (`workflow` parked at HumanSignoff, never auto-committed) live,
on top of the AgentCore Cedar engine in ENFORCE.

## Teardown

Running human-gate execution stopped, then `cdk destroy --all --force -c env=e2e
-c retention_profile=sandbox-demo`. Confirmed via CloudFormation: **residual `ben-e2e` stacks = none** (2026-09-02). The retained `ben-e2e-audit-ledger` DynamoDB table is left by design (audit evidence), same as `ben-demo`. Both retained ledgers can be removed with `scripts/cleanup_retained.py` if a full wipe is wanted.

*Not legal or compliance advice. AgentCore Policy is GA (2026-03-03); the reviewed platform_core
engine remains the fail-closed fallback + parity oracle.*
