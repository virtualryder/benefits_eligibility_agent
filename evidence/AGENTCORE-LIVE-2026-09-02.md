# AgentCore ENFORCE — live control-plane re-verification, 2026-09-02

Account **864217980669** · us-east-1 · verified by `dryder` via `bedrock-agentcore-control` +
`cloudformation` live reads (not inferred). Synthetic-data environment; no real PII.

## What this pass proves (and what it does not)

This is a **fresh, timestamped re-verification of the live AgentCore ENFORCE posture on current
code** (2026-09-02). It is a re-prove of the standing `ben-demo` environment, **not** a new
from-scratch deploy: the six `ben-demo` stacks were originally created 2026-08-24; today's
`cdk deploy --all -c env=demo` refreshed **`ben-demo-compute` from current HEAD**
(`UPDATE_COMPLETE` 2026-09-02T16:44:41Z) and left the rest unchanged. The AgentCore control plane
was then read live and confirmed in **ENFORCE**.

The full data-plane behavioral proof (each Cedar denial naming the policy that fired, over HTTPS
with a Cognito JWT) is in `evidence/EP1-VALIDATION.md` (ben-val1 2026-07-27, ben-val2 2026-07-28,
both torn down) and `evidence/DEMO-DEPLOY-2026-08-24.md`. This pass re-confirms the posture those
runs exercised is still live and ENFORCE on today's code.

## Live control-plane reads (2026-09-02, us-east-1)

**Gateway** `ben-demo-ben-gw-2cdvjxaxth`
- arn: `arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-demo-ben-gw-2cdvjxaxth`
- url: `https://ben-demo-ben-gw-2cdvjxaxth.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp`
- status **READY** · protocolType **MCP** · authorizerType **CUSTOM_JWT**
- inbound authz: Cognito discovery `us-east-1_HiNG6H9qk`, allowedClients `[26eu58bmp51fu8iaa6l3kpftnr]`

**Policy engine** `ben_demo_ben_authz` (`ben_demo_ben_authz-lph_q0uak0`)
- status **ACTIVE** · description "Deny-by-default Cedar authz (IaC-attached)"
- gateway `policyEngineConfiguration.mode` = **ENFORCE**  ← deny-by-default is live, not LOG_ONLY

**Gateway targets** (governed tool Lambdas, all **READY**): `mask-pii`, `intake-application`,
`assess-eligibility`, `ben-core` (draft_notice / finalize_determination / refer_fraud),
`overpayment`, `redetermine`, `request-signoff`, `write-audit`.

**Cedar policy set** enforced by the engine (rendered form checked in at `policies/*.cedar`):
`caseworker_permit` (deny-by-default; only the `benefits_caseworker` Cognito group is granted),
`mask_before_assess` / `mask_before_draft` / `mask_before_overpayment` / `mask_before_redetermine`
(forbid processing unless `context.input.deidentified == true`), `no_self_commit` and
`no_self_fraud_referral` (the agent can never call `finalize_determination` / `refer_fraud`;
commit is reachable only through the human sign-off gate with a different caseworker + single-use
token). Forbid overrides permit, so mask-before-processing and no-self-commit always hold.

## Stacks (live)

`ben-demo-data` CREATE_COMPLETE · `ben-demo-identity` CREATE_COMPLETE · `ben-demo-compute`
UPDATE_COMPLETE (2026-09-02, refreshed from current code) · `ben-demo-workflow` UPDATE_COMPLETE ·
`ben-demo-observability` UPDATE_COMPLETE · `ben-demo-gateway` CREATE_COMPLETE.

## Teardown (completed 2026-09-02)

After this verification the environment was **torn down** — `cdk destroy --all --force -c env=demo
-c retention_profile=sandbox-demo` — completing the deploy -> exercise -> destroy lifecycle. All six
`ben-demo` stacks (including `ben-demo-gateway`, which ran the AgentCore custom-resource Delete to
remove targets -> Cedar policies -> gateway -> policy engine) are gone; CloudFormation shows **zero
residual `ben-demo` stacks**. No standing cost remains.

## Residual note (historical)

`ben-demo` is the **standing demo environment** (up since 2026-08-24), deliberately not torn down
so it can be shown on demand — unlike the throwaway `ben-val1/ben-val2` validation envs, which were
destroyed with a residual sweep. It therefore incurs ongoing (small, sandbox-posture) cost. Tear it
down with `cdk destroy --all --force -c env=demo -c retention_profile=sandbox-demo` when the demo
window closes; keep it if active demos are scheduled.

*Not legal or compliance advice. AgentCore Policy is GA (2026-03-03); the reviewed
`platform_core` engine remains the fail-closed fallback + parity oracle (see platform
docs/AGENTCORE-INTEGRATION.md).*
