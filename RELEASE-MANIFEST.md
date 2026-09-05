# Release Manifest — single authoritative record

*This is the ONE place that states the release, the counts, and the validation status. Every other
document should reference this file rather than restating numbers. If a number anywhere disagrees with
this table, this table is correct and the other file is a bug.*

---

## Authoritative record

| Field | Value |
|---|---|
| **Product** | Public-Benefits Eligibility Screening & Determination-Support **Assistant** (never an adjudicator; never denies/reduces/terminates/refers fraud) |
| **Pilot tag** | `v0.5.1-pilot-rc1` (RELEASE file) — **cut 2026-09-05** from current main; pins **governed-core 1.10.1** and contains the 2026-09-05 work (Cedar perimeter/zero-default entitlement, output guardrail as IaC, contextual grounding end-to-end, VPC posture, capture-every-API-call lineage, token chargeback) **and** the 1.10.1 fault-semantics fixes (WORM-required commit, request/approve fail-closed sagas, authoritative Cedar context). **Supersedes `v0.4.0-pilot-rc1`**, which was cut 2026-09-03 at `be39f1c` (governed-core 1.9.0) and PREDATES all of the above — a prior version of this file wrongly said v0.4.0 matched current main; it did not (corrected 2026-09-05 after external review). Older tags: `v0.3.0-pilot-rc1` (2026-09-02 111 gate), EP1 Gate-B `v0.1.2-pilot-rc1`. Adds the #3 `authoritative_context` resolver (consent/purpose from an authoritative server-side record). **Live re-gate of the perimeter + #3 path: PASS** (from-zero `ben-perim`, torn down — `evidence/AGENTCORE-PERIMETER-AUTHZ-3-2026-09-05.md`): zero-default entitlement, authoritative consent/purpose (a caller-forged consent with no record is DENIED), and amount cap. The heavier full-portfolio gates (111 / kill-switch / budget / lineage — last green at 1.10.0) re-run against this exact tag is the remaining live step. |
| **Offline test suite** | **244** passing **on current main** (control-plane + **25 CDK stack-synthesis** assertions + doc-integrity, independent-verification, CI-completeness and doc-count gates). 243 run locally; 1 CI-completeness gate runs only in CI (`skipif` outside CI). Tag `v0.5.1-pilot-rc1` is cut from this tree and matches this count; `v0.4.0-pilot-rc1` PREDATES the 2026-09-05 work and does NOT match (it stood lower — do not deploy it as "current"). (`v0.3.0-pilot-rc1` stood at 154 <!-- count-gate:historical -->; the older `v0.1.2-pilot-rc1` predates the governed-core dependency migration and stood at 101.) |
| **Deployment IaC** | AWS CDK, 7 stacks + one data stack per tenant in multi-tenant mode (`cdk/ben_stacks`, prefix `ben-`) — synthesizes to valid CloudFormation (in-suite `aws_cdk.assertions`) |
| **Gate-B posture** | **zero public egress** (isolated subnets; AWS private endpoints only; no NAT/IGW/firewall) · customer-managed KMS · MFA-enforced pilot identity · tenant pin — **as CDK switches, live EP1-validated** |
| **Live EP1 validation** | **DONE (2026-07-27, env `ben-val1`, us-east-1)** — see `evidence/EP1-VALIDATION.md` |
| **AgentCore ENFORCE from-zero re-proof** | **DONE (2026-09-02, `ben-e2e`)** — `evidence/AGENTCORE-E2E-FROMZERO-2026-09-02.md` |
| **Hybrid multi-tenant + per-tenant audit routing** | **DONE (2026-09-02, `ben-mt` 5/5, `ben-mt2` 12/12)** — `evidence/AGENTCORE-MULTITENANT-E2E-2026-09-02.md`, `evidence/AGENTCORE-MULTITENANT-AUDIT-2026-09-02.md`; governed-core 1.6.0 |
| **Full transparency through the AgentCore Runtime** | **DONE (2026-09-02, `ben-mt3`, 13/13 per tenant)** — `evidence/AGENTCORE-OBSERVABILITY-2026-09-02.md`; governed-core 1.7.1 |
| **Consolidated 111 gate on `v0.3.0-pilot-rc1`** | **PASS (2026-09-02, `ben-mt4`)** — all proofs on one deployment + strict PII canary + 0-unexpected-errors sweep — `evidence/AGENTCORE-111-GATE-2026-09-02.md` |
| **Kill Switch on the AgentCore path** | **PASS (2026-09-03, `ben-mt5`, 29/29, time-to-effect 13.9 s)** — one-command containment: interceptor + every tool Lambda + runtime refuse (fail-closed, 15 s TTL), AWS_IAM function-URL engage/disengage with IAM + code separation of duties, IAM-verified actors, WORM-chained state changes; 0-unexpected-errors sweep after — `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md` |
| **Per-tenant token + USD budget** | **PASS (2026-09-03, `ben-mt6`, 24/24)** — meter == model-invocation log; cap refusals at runtime (mid-session) / gateway / drafter; 60/85/100 % alarms; AWS Budgets USD ceiling with IAM-deny action + breach → kill switch; 0-unexpected-errors sweep — `evidence/AGENTCORE-BUDGET-2026-09-03.md` |
| **Governance core** | `governed-core` **1.10.1**, pinned by URL + sha256 in `requirements-core.txt` (`--require-hashes`); `lib/core.lock` derived from it. 1.10.1 = the fault-semantics batch (external review): consequential commit requires ledger **and** WORM (durable-evidence-before-side-effect), request/approve fail-closed + un-strandable sagas, and authoritative Cedar context fields (caller can no longer assert consent/purpose/budget_ok/within_service_window). |
| **Control plane** | signed `sanitized_ref` masking proof (P0-1) · token boundary (P0-3) · deterministic Step Functions controller + guards incl. the **due-process advance-notice HOLD** (P0-2) · R3-2 pass-by-reference **both directions** (application + notice) · WORM hash-chained audit · human sign-off (separation of duties) |
| **Evidence source** | author-produced, synthetic data only — not independently audited or pen-tested |

## Count glossary

- **244 offline tests** — the CI suite (control-plane + 25 CDK synthesis + 3 doc-integrity gates + 4 independent-verification gates + 3 CI-completeness gates + the doc-count gate). Authoritative offline number. Locally you see `243 passed, 1 skipped`: one gate asserts the CDK libs are installed and only runs inside CI.
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
