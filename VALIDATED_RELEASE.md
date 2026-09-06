# Validated Release Record

*Single source of truth for the current release tag is the repo-root `RELEASE` file, enforced by
`tests/test_release_consistency.py`. Authoritative counts + limitations: `RELEASE-MANIFEST.md`.*

## Current release — `v0.5.2-pilot-rc1` (2026-09-06)

| Field | Value |
|---|---|
| Tag | `v0.5.2-pilot-rc1` — single source of truth: `RELEASE`. Cut from main on 2026-09-06 after the Tier-1 live re-gate (`ben-t1`: mandatory-guardrail IAM, #3 perimeter, advanced capture selectors, CMK invocation store, endpoint policy, bypass alarm, operator console) passed on it. |
| Commit SHA | `git rev-list -n1 v0.5.2-pilot-rc1` |
| Test count at the tag | **285** offline tests <!-- count-gate:historical --> collected at `v0.5.2-pilot-rc1` (284 pass + 1 CI-only skip locally; 37 CDK <!-- count-gate:historical --> assertions) — a record of the tag; current main carries more (README "Run the tests") |
| Governance core | `governed-core` **1.10.1**, pinned by URL + sha256 (`requirements-core.txt`, `--require-hashes`); `lib/core.lock` locked at 1.10.1 (`lib/verify_core.py` OK) |
| What this tag adds over `v0.5.1-pilot-rc1` | **Tier-1 live re-gate PASS** — `evidence/TIER1-REGATE-2026-09-06.md` (env `ben-t1`, from zero, PRIVATE network mode, customer-managed KMS, perimeter on, CMK model-invocation logging, capture-all trail with advanced selectors; 12/12: deploy, P2 selectors, P5 endpoint policy naming the pinned drafter role, P4 CMK store + delivery, T1a guardrail proof, T1b Cedar perimeter proof 6/6, P3 real-bypass alarm with exact accounting, D2 operator console, teardown to zero residue). Live-found defects L9–L13 fixed on the way (missing `ssm`/`monitoring` VPC endpoints, IaC entitlement grant, pinned drafter role for the endpoint policy, teardown late deliveries, gate accounting). |
| What `v0.5.1-pilot-rc1` (2026-09-05) added over `v0.3.0-pilot-rc1` | governed-core 1.10.0/1.10.1 (audit-before-finalize, bound approvals, deepened PII, WORM-required commit, fail-closed sagas, authoritative Cedar context), Cedar perimeter + zero-default entitlement, output guardrail as IaC, contextual grounding end-to-end, capture-every-API-call lineage, token chargeback, the #3 `authoritative_context` resolver (live on `ben-perim`, 2026-09-05). |
| What `v0.4.0-pilot-rc1` (2026-09-03) added over `v0.3.0-pilot-rc1` | **Kill Switch on the AgentCore path** — `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md` (env `mt5`, 2 tenants, real Runtime, **29/29**, 13.9 s to effect). **Per-tenant token + USD budget** — `evidence/AGENTCORE-BUDGET-2026-09-03.md` (env `mt6`, **24/24**: meter == model-invocation log to the token, cap refusals at gateway / drafter / runtime incl. mid-session, 60/85 % alarms, AWS Budgets ceiling → kill switch) + `-regression.json` (0 unexpected). Two drafter fixes found by that gate: the append-only ledger grant so its workflow-hop DENIED record lands, and `requestMetadata` tagging on its server-side `Converse`. |
| Carried unchanged from `v0.3.0-pilot-rc1` | AgentCore ENFORCE from-zero, hybrid multi-tenant (2 tenants), per-tenant audit routing 12/12, full transparency 13/13 per tenant, consolidated 111 gate + strict PII canary + 0-unexpected sweep (`ben-mt4`, 2026-09-02) — the control code those runs exercised is unchanged; the deltas are the two controls above and the drafter fixes, each proven on their own from-zero deployments (`mt5`, `mt6`). |
| Not re-run on this tree | the consolidated 111 gate (isolation + per-tenant audit routing + transparency + PII canary), the kill-switch (29/29) and budget (24/24) gates, the #168 lineage proof and the two-tenant runtime gate on the IaC execution role (RT-2) — last green at governed-core 1.10.0 (2026-09-05) / 1.9.0 (2026-09-03) on ancestor trees. The private-networking + CMK posture IS re-run (`ben-t1`); MFA-required identity (`identity_mode=pilot`) and the WAF↔Cognito association remain IaC-asserted. |

## Previous release — `v0.3.0-pilot-rc1` (2026-09-02)

| Field | Value |
|---|---|
| Tag | `v0.3.0-pilot-rc1` — single source of truth: `RELEASE`. Cut from the tree the 2026-09-02 runs validated. |
| Commit SHA | `git rev-list -n1 v0.3.0-pilot-rc1` |
| Test count at the tag | **168** offline tests <!-- count-gate:historical --> (153 local + 1 CI-only) — a record of that tag, not the current tree |
| Governance core | `governed-core` **1.7.1**, pinned by URL + sha256 (`requirements-core.txt`, `--require-hashes`) |
| Validated live on this tree (each deployed from zero, exercised, torn down) | AgentCore ENFORCE from-zero re-proof (`ben-e2e`) — `evidence/AGENTCORE-E2E-FROMZERO-2026-09-02.md` · hybrid multi-tenant, 2 tenants, cross-tenant deny + per-tenant routing (`ben-mt`, 5/5) — `evidence/AGENTCORE-MULTITENANT-E2E-2026-09-02.md` · per-tenant audit ledger / WORM vault / approvals routing on the gateway AND workflow hops, fail-closed (`ben-mt2`, 12/12) — `evidence/AGENTCORE-MULTITENANT-AUDIT-2026-09-02.md` · full per-case transparency through the real AgentCore Runtime (`ben-mt3`, 13/13 per tenant) — `evidence/AGENTCORE-OBSERVABILITY-2026-09-02.md` |
| Consolidated 111 gate on this tag | **PASS (2026-09-02, env `mt4`)** — ONE from-zero deployment of this tag: isolation + per-tenant audit routing 12/12, full transparency through the real AgentCore Runtime 13/13 per tenant, strict PII canary clean, and an end-to-end regression sweep with **0 unexpected errors** across 20 log groups, all executions, alarms, DLQs and Lambda error metrics — [`evidence/AGENTCORE-111-GATE-2026-09-02.md`](evidence/AGENTCORE-111-GATE-2026-09-02.md). Two launch-tooling defects found by the sweep (Git-Bash path mangling of the SSM parameter name; SSM grant on the wrong path) fixed in `lib/runtime/*.sh` after the tag — harness only, no product code |
| Kill Switch on the AgentCore path (after this tag, on main) | **PASS (2026-09-03, env `mt5`, 29/29)** — governed-core 1.8.0; `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md`. Not part of `v0.3.0-pilot-rc1`; carried by `v0.5.1-pilot-rc1`. |
| Per-tenant token + USD budget (after this tag, on main) | **PASS (2026-09-03, env `mt6`, 24/24)** — governed-core 1.9.0; `evidence/AGENTCORE-BUDGET-2026-09-03.md`. Not part of `v0.3.0-pilot-rc1`; carried by `v0.5.1-pilot-rc1`. |
| Not re-run on this tree | the EP1 Gate-B posture walk (zero-egress private networking, CMK, MFA identity) — last captured 2026-07-27/28 on `v0.1.2-pilot-rc1`; the switches are unchanged and synth-tested, but the live re-walk is owed |

## EP1 record — `v0.1.2-pilot-rc1` (2026-07-27)

| Field | Value |
|---|---|
| Tag | `v0.1.2-pilot-rc1` — cut after the live EP1 validation below. |
| Commit SHA | the commit carrying tag `v0.1.2-pilot-rc1` (`git rev-list -n1 v0.1.2-pilot-rc1`) |
| Test count at the tag | **101** offline tests <!-- count-gate:historical --> at the moment `v0.1.2-pilot-rc1` was cut — a record of that tag, not a claim about the current tree |
| Test count on current main | **291 offline tests** (control-plane + CDK synthesis + governance gates + the doc-count gate). Authoritative matrix: [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md). |
| Validation date | **2026-07-27** (live EP1, env `ben-val1`, us-east-1) |
| Region | us-east-1 |
| Deployment | AWS CDK `deploy --all`, all Gate-B switches: `network_mode=private kms=customer-managed identity_mode=pilot tenant=ben-example-agency retention_profile=sandbox-demo` |
| Evidence | **captured — [`evidence/EP1-VALIDATION.md`](evidence/EP1-VALIDATION.md)**: 7/7 stacks incl. the AgentCore ENFORCE attachment; `validate_deployment.py` → PASS; happy-path ran the full guarded controller to the human sign-off gate; **AdverseNoticeHold** due-process gate held an adverse redetermination; **strict PII canary PASS (0 leaks across Logs / X-Ray / DLQ / Step Functions history)**; MFA pool ON with 0 users. Then torn down (`destroy --all`) with a residual sweep. Account IDs redacted to `111122223333`. |

## What EP1 proved (live)

The deployed control plane behaves as designed on a clean account with every Gate-B switch on: the
deterministic Step Functions controller runs each guard in order and **cannot** advance a case on
unverified state; de-identification is proven by a mask-signed `sanitized_ref` (a forged ref is refused);
raw application content enters only via `ingest-application` and **only opaque refs — including the
drafted determination notice — cross Step Functions state** (strict PII canary PASS); an **adverse
redetermination without advance notice HOLDS** (Goldberg v. Kelly, enforced by the platform); and every
consequential action pauses at a caseworker sign-off gate. Networking is **zero public egress** (isolated
subnets + AWS private endpoints only; no NAT/IGW/firewall) — benefits has no external dependency.

One finding was fixed during the run (a zero-egress security-group rule blocked the S3/DynamoDB gateway
endpoints; corrected in `network_stack.py`); see `evidence/EP1-VALIDATION.md`.

## Still not live-validated (say these out loud)

Enterprise IdP federation round-trip; a benefits-program SME sign-off on the eligibility rules, processing
clocks, redetermination/overpayment logic, and notice language; independent security testing / pen test;
prod-scale load; system-of-record integration and the notice/appeal workflow. These are Gate-C/D items —
see `BENEFITS-PILOT-READINESS-PLAN.md`. Evidence to date is author-produced on synthetic data.
