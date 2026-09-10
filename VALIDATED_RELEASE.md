# Validated Release Record

*Single source of truth for the current release tag is the repo-root `RELEASE` file, enforced by
`tests/test_release_consistency.py`. Authoritative counts + limitations: `RELEASE-MANIFEST.md`.*

## Current release — `v0.7.0-pilot-rc1` (2026-09-09)

| | |
|---|---|
| Tag | `v0.7.0-pilot-rc1` — single source of truth: `RELEASE`. Cut from main on 2026-09-09 after the **full-portfolio gate passed 17/17 from zero** on the tree this tag points at (`git rev-list -n1 v0.7.0-pilot-rc1`). The gate ran on `938dfe8`; the tag was moved forward to the doc-sync commit so that the `RELEASE` file INSIDE the tag names the tag - it named `v0.6.0-pilot-rc1` otherwise, which is the same self-contradiction as L54. |
| Commit SHA | `git rev-list -n1 v0.7.0-pilot-rc1` |
| Scope of the claim, exactly | ONE pack (benefits). ONE account. ONE region (us-east-1). Synthetic data. Two tenants. Deployed from zero, exercised, torn down to zero residue. `evidence/FULL-PORTFOLIO-GATE-2026-09-09.json`, env `ben-fp2`. Deploy rc=0 in 706.2s / nine stacks; runtime READY on `ben-fp2-agentcore-runtime` with MMDSv2 required; G111 rc=0 in 550.8s; kill switch rc=0 in 102.4s; budget rc=0 in 372.6s; `RT2_runtime_calls_guardrail_assessed` runtime_rows=20 guardrail_assessed=20; `LIN_zero_orphans` covered=True, orphans=0, invokes=11, aegis=11, settle 384.9s; `E2E_zero_unexpected` rc=0; both teardown checks clean. |
| What this tag adds over `v0.6.0-pilot-rc1` | **Two checks, and the reason they exist.** `preflight_no_agentcore_residue` refuses to deploy if any gateway, policy engine or agent runtime carrying the prefix already exists, and `teardown_zero_agentcore_residue` asserts the same after teardown. v0.6.0's "zero residue" covered CloudFormation stacks only — AgentCore gateways, policy engines and runtimes are not owned by the stacks that create them. Also carried: **the policy-name prefix fix (L64)**, without which this gate cannot pass in an account that has ever hosted a second pack, because AgentCore policy names are unique per ACCOUNT and REGION rather than per policy engine; and **the RT-4 reversal (L66)**. |
| What it took to get there | **Seven attempts, and the six failures are published in the same commit as the pass.** In order: CRLF noise that was cosmetic, and which I first diagnosed as digest corruption and was wrong (L60); three consecutive wrong diagnoses of one `ConflictException`, whose real cause — account-wide policy-name uniqueness — was stated in `lib/engine/render.py`'s own comment the whole time (L64); the CloudTrail five-trails-per-region quota, which AWS marks not adjustable (L61); and RT-4, a control that worked correctly and made the agent unreachable (L65, L66). |
| Residue | Verified independently of the check: no `ben-fp2-` CloudFormation stacks and no AgentCore gateways, policy engines or runtimes. `teardown_zero_stack_residue` passed with `destroy_rc=1` and `stacks_clean=True` — by design (L28), the residue sweep is the claim and the CLI exit code is not. **Known gap (L37):** the toolkit's ECR repository is not pruned by teardown and grows one image per run. |
| Reopened by this tag | **R4-2.** RT-4 closed "a token that can reach the gateway can also reach the runtime directly, past the gateway's Cedar interceptor" by restricting the runtime's authorizer to the gateway workload. It works, and it closed the intended human-to-agent path with it, because the gateway is downstream of the runtime in this architecture. RT-4 is now opt-in behind `RT4_GATEWAY_ONLY=1` and off by default (L66), so R4-2 is OPEN and is stated as open in the partner material. |
| Still not proven live | PV / EDU / Housing full-portfolio gates (REL-5). Those three packs share the hash-locked core and received the L64 and L66 fixes with unit tests, and **none has been deployed in the AgentCore era**; the gate harness `scripts/full_portfolio_gate.py` exists only in this pack. Also: manifest signing (SIG-1), the Organizations-level SCP perimeter (PERIM-1b, blocked on an Organization), real data, multi-account, multi-region, and scale. |
| Independence | All of this evidence is author-produced. That is the single largest credibility gap in this repository and no amount of further self-testing closes it; the protocol for a third party to reproduce it is `docs/INDEPENDENT-VERIFICATION.md`. |

---

## Previous release — `v0.6.0-pilot-rc1` (2026-09-07)

| | |
|---|---|
| Tag | `v0.6.0-pilot-rc1` — single source of truth: `RELEASE`. Cut from main on 2026-09-07 after the **full-portfolio gate passed 15/15 from zero** on this exact tree. |
| Commit SHA | `git rev-list -n1 v0.6.0-pilot-rc1` |
| What this tag adds over `v0.5.2-pilot-rc1` | **The claim v0.5.2 could not make.** v0.5.2 was offline-green and Tier-1 live-gated, but the heavier full-portfolio gate — consolidated 111, kill switch, per-tenant budget, #168 lineage, runtime on the IaC execution role, e2e, teardown — had never been green on any tree. It is now: `evidence/FULL-PORTFOLIO-GATE-2026-09-07.json`, env `ben-fp`, from zero, two tenants, real AgentCore Runtime, 15/15, torn down. Deploy 670.8s / nine stacks; G111 rc=0 in 533.8s (isolation + audit routing 12/12, transparency 13/13 per tenant, strict PII canary); kill switch rc=0; budget rc=0; `LIN_zero_orphans` covered=True, orphans=0, invokes=10, aegis=10, settle 406.7s; guardrail-assessed 20/20; e2e 0 unexpected; teardown clean. |
| What it took to get there | Twenty-one gate attempts. The platform was not the obstacle: of the findings the campaign produced, **seven were cases where the platform was right and the thing checking it was wrong** (L25, L29, L31, L33, L33b, L39, L40). The three that gated this tag directly: **L34** CloudTrail identity must be `eventID` (a merge on a second-granular key fabricated invokes); **L38** a loop variable rebound a live boto3 client twelve minutes into a from-zero run; **L39** `filter_log_events` takes milliseconds and the audit reader was passing seconds, so it scanned 1970 and reported "no audit lines" — which reads as a governed tool that never audited itself. Each is now pinned by an offline test, and each of those tests is negation-controlled. |
| Residue | Verified independently of the check: no `ben-` CloudFormation stacks, no AgentCore runtimes. `teardown_zero_residue` passed with `destroy_rc=1` — by design (L28), the residue sweep is the claim and the CLI exit code is not. **Known gap (L37):** the toolkit's ECR repository is not pruned by teardown and grows one image per run (20 → 22 images, 2,544 → 2,799 MB across attempts 20 and 21). "Zero residue" means zero *stack* residue; the container images persist. |
| Still not proven live | PV / EDU / Housing full-portfolio gates (REL-5 — PV now has a `pack.json` and a `drive_one_case.py`, neither yet exercised against a deployment), manifest signing (SIG-1), COMPLIANCE-mode retention in a disposable account (EV-1), and the Organizations-level SCP perimeter (PERIM-1b, blocked on an Organization). Housing has never had an AgentCore-era live gate at all. |

---

## Previous release — `v0.5.2-pilot-rc1` (2026-09-06)

| Field | Value |
|---|---|
| Tag | `v0.5.2-pilot-rc1` — single source of truth: `RELEASE`. Cut from main on 2026-09-06 after the Tier-1 live re-gate (`ben-t1`: mandatory-guardrail IAM, #3 perimeter, advanced capture selectors, CMK invocation store, endpoint policy, bypass alarm, operator console) passed on it. |
| Commit SHA | `git rev-list -n1 v0.5.2-pilot-rc1` |
| Test count at the tag | **285** offline tests <!-- count-gate:historical --> collected at `v0.5.2-pilot-rc1` (284 pass + 1 CI-only skip locally; 37 CDK <!-- count-gate:historical --> assertions) — a record of the tag; current main carries more (README "Run the tests") |
| Governance core | `governed-core` **1.11.1**, pinned by URL + sha256 (`requirements-core.txt`, `--require-hashes`); `lib/core.lock` locked at 1.11.1 (`lib/verify_core.py` OK) |
| What this tag adds over `v0.5.1-pilot-rc1` | **Tier-1 live re-gate PASS** — `evidence/TIER1-REGATE-2026-09-06.md` (env `ben-t1`, from zero, PRIVATE network mode, customer-managed KMS, perimeter on, CMK model-invocation logging, capture-all trail with advanced selectors; 12/12: deploy, P2 selectors, P5 endpoint policy naming the pinned drafter role, P4 CMK store + delivery, T1a guardrail proof, T1b Cedar perimeter proof 6/6, P3 real-bypass alarm with exact accounting, D2 operator console, teardown to zero residue). Live-found defects L9–L13 fixed on the way (missing `ssm`/`monitoring` VPC endpoints, IaC entitlement grant, pinned drafter role for the endpoint policy, teardown late deliveries, gate accounting). |
| What `v0.5.1-pilot-rc1` (2026-09-05) added over `v0.3.0-pilot-rc1` | governed-core 1.10.0/1.10.1 (audit-before-finalize, bound approvals, deepened PII, WORM-required commit, fail-closed sagas, authoritative Cedar context), Cedar perimeter + zero-default entitlement, output guardrail as IaC, contextual grounding end-to-end, capture-every-API-call lineage, token chargeback, the #3 `authoritative_context` resolver (live on `ben-perim`, 2026-09-05). |
| What `v0.4.0-pilot-rc1` (2026-09-03) added over `v0.3.0-pilot-rc1` | **Kill Switch on the AgentCore path** — `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md` (env `mt5`, 2 tenants, real Runtime, **29/29**, 13.9 s to effect). **Per-tenant token + USD budget** — `evidence/AGENTCORE-BUDGET-2026-09-03.md` (env `mt6`, **24/24**: meter == model-invocation log to the token, cap refusals at gateway / drafter / runtime incl. mid-session, 60/85 % alarms, AWS Budgets ceiling → kill switch) + `-regression.json` (0 unexpected). Two drafter fixes found by that gate: the append-only ledger grant so its workflow-hop DENIED record lands, and `requestMetadata` tagging on its server-side `Converse`. |
| Carried unchanged from `v0.3.0-pilot-rc1` | AgentCore ENFORCE from-zero, hybrid multi-tenant (2 tenants), per-tenant audit routing 12/12, full transparency 13/13 per tenant, consolidated 111 gate + strict PII canary + 0-unexpected sweep (`ben-mt4`, 2026-09-02) — the control code those runs exercised is unchanged; the deltas are the two controls above and the drafter fixes, each proven on their own from-zero deployments (`mt5`, `mt6`). |
| Not re-run on this tree | the consolidated 111 gate (isolation + per-tenant audit routing + transparency + PII canary), the kill-switch (29/29) and budget (24/24) gates, the #168 lineage proof and the two-tenant runtime gate on the IaC execution role (RT-2) — last green at governed-core 1.10.0 (2026-09-05) / 1.9.0 (2026-09-03) on ancestor trees. The private-networking + CMK posture IS re-run (`ben-t1`); MFA-required identity (`identity_mode=pilot`) and the WAF↔Cognito association remain IaC-asserted. **Full-portfolio re-gate: GREEN 15/15 on 2026-09-07 (env `ben-fp`, from zero) — see `v0.6.0-pilot-rc1` above; the qualifier below applied to this tag and is now discharged by that tag.** Originally recorded as in progress: — attempts 2–3 found two defects the earlier gates had not exercised on this tree, both fixed on main AFTER this tag: **L14** the workflow's `DraftNotice` passed only the masked application to the grounded drafter, so every real notice was blocked by contextual grounding (the earlier guardrail proof had pre-baked the determination into the masked text); the engine's determination is now a required, allowlisted drafter input carried by the workflow and the gateway schema. **L15** the runtime's guardrail-assessed prompt path flagged the observability proof's imperative wording as a prompt attack (LOW confidence at HIGH strength); proof wording changed, guardrail unchanged. Until that gate is green, the 111 / kill-switch / budget / lineage / RT-2 claims stand only for their ancestor trees. |

## Previous release — `v0.3.0-pilot-rc1` (2026-09-02)

| Field | Value |
|---|---|
| Tag | `v0.3.0-pilot-rc1` — single source of truth: `RELEASE`. Cut from the tree the 2026-09-02 runs validated. |
| Commit SHA | `git rev-list -n1 v0.3.0-pilot-rc1` |
| Test count at the tag | **168** offline tests <!-- count-gate:historical --> (153 local + 1 CI-only) — a record of that tag, not the current tree |
| Governance core | `governed-core` **1.7.1** <!-- count-gate:historical -->, pinned by URL + sha256 (`requirements-core.txt`, `--require-hashes`) |
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
| Test count on current main | **512 offline tests** (control-plane + CDK synthesis + governance gates + the doc-count gate). Authoritative matrix: [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md). |
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
