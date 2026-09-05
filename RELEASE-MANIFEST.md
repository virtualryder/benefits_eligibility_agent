# Release Manifest — single authoritative record

*This is the ONE place that states the release, the counts, and the validation status. Every other
document should reference this file rather than restating numbers. If a number anywhere disagrees with
this table, this table is correct and the other file is a bug.*

---

## Authoritative record

| Field | Value |
|---|---|
| **Product** | Public-Benefits Eligibility Screening & Determination-Support **Assistant** (never an adjudicator; never denies/reduces/terminates/refers fraud) |
| **Pilot tag** | `v0.4.0-pilot-rc1` (RELEASE file) — **cut 2026-09-03** from main after the kill-switch (29/29, `mt5`) and per-tenant budget (24/24, `mt6`) gates passed on it; builds on `v0.3.0-pilot-rc1` (2026-09-02: AgentCore from-zero, hybrid multi-tenant, per-tenant audit routing, full transparency, 111 gate). Older EP1 Gate-B tag: `v0.1.2-pilot-rc1`. |
| **Offline test suite** | **236** passing **on current main** (control-plane + **25 CDK stack-synthesis** assertions + doc-integrity, independent-verification, CI-completeness and doc-count gates). 235 run locally; 1 CI-completeness gate runs only in CI (`skipif` outside CI). Tag `v0.4.0-pilot-rc1` was cut from this tree and matches this count (`v0.3.0-pilot-rc1` stood at 154 <!-- count-gate:historical -->). The older `v0.1.2-pilot-rc1` tag predates the governed-core dependency migration and stood at 101. |
| **Deployment IaC** | AWS CDK, 7 stacks + one data stack per tenant in multi-tenant mode (`cdk/ben_stacks`, prefix `ben-`) — synthesizes to valid CloudFormation (in-suite `aws_cdk.assertions`) |
| **Gate-B posture** | **zero public egress** (isolated subnets; AWS private endpoints only; no NAT/IGW/firewall) · customer-managed KMS · MFA-enforced pilot identity · tenant pin — **as CDK switches, live EP1-validated** |
| **Live EP1 validation** | **DONE (2026-07-27, env `ben-val1`, us-east-1)** — see `evidence/EP1-VALIDATION.md` |
| **AgentCore ENFORCE from-zero re-proof** | **DONE (2026-09-02, `ben-e2e`)** — `evidence/AGENTCORE-E2E-FROMZERO-2026-09-02.md` |
| **Hybrid multi-tenant + per-tenant audit routing** | **DONE (2026-09-02, `ben-mt` 5/5, `ben-mt2` 12/12)** — `evidence/AGENTCORE-MULTITENANT-E2E-2026-09-02.md`, `evidence/AGENTCORE-MULTITENANT-AUDIT-2026-09-02.md`; governed-core 1.6.0 |
| **Full transparency through the AgentCore Runtime** | **DONE (2026-09-02, `ben-mt3`, 13/13 per tenant)** — `evidence/AGENTCORE-OBSERVABILITY-2026-09-02.md`; governed-core 1.7.1 |
| **Consolidated 111 gate on `v0.3.0-pilot-rc1`** | **PASS (2026-09-02, `ben-mt4`)** — all proofs on one deployment + strict PII canary + 0-unexpected-errors sweep — `evidence/AGENTCORE-111-GATE-2026-09-02.md` |
| **Kill Switch on the AgentCore path** | **PASS (2026-09-03, `ben-mt5`, 29/29, time-to-effect 13.9 s)** — one-command containment: interceptor + every tool Lambda + runtime refuse (fail-closed, 15 s TTL), AWS_IAM function-URL engage/disengage with IAM + code separation of duties, IAM-verified actors, WORM-chained state changes; 0-unexpected-errors sweep after — `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md` |
| **Per-tenant token + USD budget** | **PASS (2026-09-03, `ben-mt6`, 24/24)** — meter == model-invocation log; cap refusals at runtime (mid-session) / gateway / drafter; 60/85/100 % alarms; AWS Budgets USD ceiling with IAM-deny action + breach → kill switch; 0-unexpected-errors sweep — `evidence/AGENTCORE-BUDGET-2026-09-03.md` |
| **Governance core** | `governed-core` **1.9.0**, pinned by URL + sha256 in `requirements-core.txt` (`--require-hashes`); `lib/core.lock` derived from it |
| **Control plane** | signed `sanitized_ref` masking proof (P0-1) · token boundary (P0-3) · deterministic Step Functions controller + guards incl. the **due-process advance-notice HOLD** (P0-2) · R3-2 pass-by-reference **both directions** (application + notice) · WORM hash-chained audit · human sign-off (separation of duties) |
| **Evidence source** | author-produced, synthetic data only — not independently audited or pen-tested |

## Count glossary

- **236 offline tests** — the CI suite (control-plane + 25 CDK synthesis + 3 doc-integrity gates + 4 independent-verification gates + 3 CI-completeness gates + the doc-count gate). Authoritative offline number. Locally you see `235 passed, 1 skipped`: one gate asserts the CDK libs are installed and only runs inside CI.
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
