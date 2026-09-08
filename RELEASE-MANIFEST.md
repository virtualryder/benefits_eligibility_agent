# Release Manifest — single authoritative record

*This is the ONE place that states the release, the counts, and the validation status. Every other
document should reference this file rather than restating numbers. If a number anywhere disagrees with
this table, this table is correct and the other file is a bug.*

---

## Authoritative record

| Field | Value |
|---|---|
| **Product** | Public-Benefits Eligibility Screening & Determination-Support **Assistant** (never an adjudicator; never denies/reduces/terminates/refers fraud) |
| **Pilot tag** | `v0.6.0-pilot-rc1` (RELEASE file) — **cut 2026-09-07** at `9624dab`, the first tag in this repo's history cut on a **GREEN full-portfolio gate** (15/15 from zero, env `ben-fp`, two tenants, real AgentCore Runtime on the IaC execution role; `evidence/FULL-PORTFOLIO-GATE-2026-09-07.json`). Supersedes `v0.5.2-pilot-rc1` <!-- count-gate:historical --> (2026-09-06, cut after the Tier-1 live re-gate `ben-t1`) and `v0.5.1-pilot-rc1` <!-- count-gate:historical --> (2026-09-05, pre-Tier-1-gate). The tag pins **governed-core 1.10.1** <!-- count-gate:historical -->; **main has since moved to 1.11.1 and is 16 commits ahead of the tag**, so main is NOT the tag — deploy the tag, and read the rows below as describing main. "Zero residue" in that gate means zero STACK residue: teardown does not prune the toolkit ECR repository, which grows one image per run (L37). |
| **Offline test suite** | **433 tests** **on current main** (control-plane + **45 CDK stack-synthesis** assertions + doc-integrity, independent-verification, CI-completeness and doc-count gates). Skips are PLATFORM-DEPENDENT and the count differs between a developer machine and CI: on Windows 1 CI-completeness gate skips, on Linux/CI the Windows-specific process-tree cases skip as well. An external review on 2026-09-08 reported ~15 skips and 1 FAILURE on Linux - the failure was real (L42: `sh()` opened children without `start_new_session`, so the timeout's `killpg` targeted the caller's own process group; the grandchildren survived and CI's unit-test step ran 46 minutes and died before reaching lint). Fixed and pinned; the honest statement is "433 collected, all passing on both platforms, with a platform-dependent skip set", not "all local tests pass". Tag `v0.5.2-pilot-rc1` is cut from this tree and matches this count; `v0.4.0-pilot-rc1` PREDATES the 2026-09-05 work and does NOT match (it stood lower — do not deploy it as "current"). (`v0.3.0-pilot-rc1` stood at 154 <!-- count-gate:historical -->; the older `v0.1.2-pilot-rc1` predates the governed-core dependency migration and stood at 101.) |
| **Deployment IaC** | AWS CDK, 7 stacks + one data stack per tenant in multi-tenant mode (`cdk/ben_stacks`, prefix `ben-`) — synthesizes to valid CloudFormation (in-suite `aws_cdk.assertions`) |
| **Gate-B posture** | **zero public egress** (isolated subnets; AWS private endpoints only; no NAT/IGW/firewall) · customer-managed KMS · MFA-enforced pilot identity · tenant pin — **as CDK switches, live EP1-validated** |
| **Live EP1 validation** | **DONE (2026-07-27, env `ben-val1`, us-east-1)** — see `evidence/EP1-VALIDATION.md` |
| **AgentCore ENFORCE from-zero re-proof** | **DONE (2026-09-02, `ben-e2e`)** — `evidence/AGENTCORE-E2E-FROMZERO-2026-09-02.md` |
| **Hybrid multi-tenant + per-tenant audit routing** | **DONE (2026-09-02, `ben-mt` 5/5, `ben-mt2` 12/12)** — `evidence/AGENTCORE-MULTITENANT-E2E-2026-09-02.md`, `evidence/AGENTCORE-MULTITENANT-AUDIT-2026-09-02.md`; governed-core 1.6.0 |
| **Full transparency through the AgentCore Runtime** | **DONE (2026-09-02, `ben-mt3`, 13/13 per tenant)** — `evidence/AGENTCORE-OBSERVABILITY-2026-09-02.md`; governed-core 1.7.1 |
| **Consolidated 111 gate on `v0.3.0-pilot-rc1`** | **PASS (2026-09-02, `ben-mt4`)** — all proofs on one deployment + strict PII canary + 0-unexpected-errors sweep — `evidence/AGENTCORE-111-GATE-2026-09-02.md` |
| **Kill Switch on the AgentCore path** | **PASS (2026-09-03, `ben-mt5`, 29/29, time-to-effect 13.9 s)** — one-command containment: interceptor + every tool Lambda + runtime refuse (fail-closed, 15 s TTL), AWS_IAM function-URL engage/disengage with IAM + code separation of duties, IAM-verified actors, WORM-chained state changes; 0-unexpected-errors sweep after — `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md` |
| **Per-tenant token + USD budget** | **PASS (2026-09-03, `ben-mt6`, 24/24)** — meter == model-invocation log; cap refusals at runtime (mid-session) / gateway / drafter; 60/85/100 % alarms; AWS Budgets USD ceiling with IAM-deny action + breach → kill switch — a **backstop with at-least-daily billing latency that alerts once per budget period**, not a real-time cap; the per-tenant meter is what refuses before the spend (#231); 0-unexpected-errors sweep — `evidence/AGENTCORE-BUDGET-2026-09-03.md` |
| **Governance core** | `governed-core` **1.11.1**, pinned by URL + sha256 in `requirements-core.txt` (`--require-hashes`); `lib/core.lock` derived from it. 1.10.1 <!-- count-gate:historical --> = the fault-semantics batch (external review): consequential commit requires ledger **and** WORM (durable-evidence-before-side-effect), request/approve fail-closed + un-strandable sagas, and authoritative Cedar context fields (caller can no longer assert consent/purpose/budget_ok/within_service_window). |
| **Control plane** | signed `sanitized_ref` masking proof (P0-1) · token boundary (P0-3) · deterministic Step Functions controller + guards incl. the **due-process advance-notice HOLD** (P0-2) · R3-2 pass-by-reference **both directions** (application + notice) · WORM hash-chained audit · human sign-off (separation of duties) |
| **Evidence source** | author-produced, synthetic data only — not independently audited or pen-tested |

## Count glossary

- **433 offline tests** — the CI suite (control-plane + 45 CDK synthesis + 3 doc-integrity gates + 4 independent-verification gates + 3 CI-completeness gates + the doc-count gate). Authoritative offline number. Locally you see `298 passed, 1 skipped`: one gate asserts the CDK libs are installed and only runs inside CI.
- The number above is machine-enforced by `tests/test_doc_counts.py`, which collects the suite for real and fails if any counted document disagrees. Counts that describe a **past run** are exempt only when the line says "at the time of this run" or carries a `<!-- count-gate:historical -->` marker.

## Known limitations (explicit)

- **Live EP1 captured on a disposable sandbox only** — synthetic data, torn down afterward; not a
  production ATO and no real PII. Record: `evidence/EP1-VALIDATION.md`.
- **Zero external dependency.** The eligibility engine runs on **public HHS Federal Poverty Guidelines**
  baked in as configuration; there is no external lookup, so the network has **no internet egress at all**
  (stronger than an allowlist). The authoritative, market-specific program rules and income/identity
  verification remain the agency's (`docs/DATA-SOURCE-POLICY.md`, `PILOT-SCOPE.md`).
- **One signing domain** — only `mask_pii` signs (the sanitized_ref); there is no external-source signer,
  so GA-2 domain-split is N/A.
- **Pass-by-reference (R3-2) — both directions.** Raw application text enters only via `ingest-application`
  (opaque `case_ref`); the masked case and the **drafted determination notice** are stored server-side
  under signed refs — neither crosses Step Functions state. Proven at synth + runtime
  (`tests/test_pass_by_reference.py`… `tests/test_draft_pass_by_reference.py`) and by the live strict canary.
- Evidence is author-produced on synthetic data; **no independent audit / pen test** and **no
  benefits-program SME sign-off** on the eligibility rules + notice language yet.
- No system-of-record integration, no notice/appeal workflow, no IRS Pub 1075 controls for federal tax
  info, no authoritative state rules — adopter/out-of-scope (`PILOT-SCOPE.md`).
