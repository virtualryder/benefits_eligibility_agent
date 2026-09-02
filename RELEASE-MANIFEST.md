# Release Manifest — single authoritative record

*This is the ONE place that states the release, the counts, and the validation status. Every other
document should reference this file rather than restating numbers. If a number anywhere disagrees with
this table, this table is correct and the other file is a bug.*

---

## Authoritative record

| Field | Value |
|---|---|
| **Product** | Public-Benefits Eligibility Screening & Determination-Support **Assistant** (never an adjudicator; never denies/reduces/terminates/refers fraud) |
| **Pilot tag** | `v0.1.2-pilot-rc1` (RELEASE file) — **cut after the live EP1 validation (2026-07-27)** |
| **Offline test suite** | **125** passing **on current main** (control-plane + **14 CDK stack-synthesis** assertions + 3 doc-integrity gates + 4 independent-verification gates + 3 CI-completeness gates + the doc-count gate). 124 run locally; 1 CI-completeness gate runs only in CI (`skipif` outside CI). Tag `v0.2.0-pilot-rc1` was cut from this tree and matches this count. The older `v0.1.2-pilot-rc1` tag predates the governed-core dependency migration and stood at 101. |
| **Deployment IaC** | AWS CDK, 7 stacks (`cdk/ben_stacks`, prefix `ben-`) — synthesizes to valid CloudFormation (in-suite `aws_cdk.assertions`) |
| **Gate-B posture** | **zero public egress** (isolated subnets; AWS private endpoints only; no NAT/IGW/firewall) · customer-managed KMS · MFA-enforced pilot identity · tenant pin — **as CDK switches, live EP1-validated** |
| **Live EP1 validation** | **DONE (2026-07-27, env `ben-val1`, us-east-1)** — see `evidence/EP1-VALIDATION.md` |
| **Control plane** | signed `sanitized_ref` masking proof (P0-1) · token boundary (P0-3) · deterministic Step Functions controller + guards incl. the **due-process advance-notice HOLD** (P0-2) · R3-2 pass-by-reference **both directions** (application + notice) · WORM hash-chained audit · human sign-off (separation of duties) |
| **Evidence source** | author-produced, synthetic data only — not independently audited or pen-tested |

## Count glossary

- **142 offline tests** — the CI suite (control-plane + 14 CDK synthesis + 3 doc-integrity gates + 4 independent-verification gates + 3 CI-completeness gates + the doc-count gate). Authoritative offline number. Locally you see `124 passed, 1 skipped`: one gate asserts the CDK libs are installed and only runs inside CI.
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
