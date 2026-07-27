# PV Pilot Readiness Plan

**Product:** Benefits determination Intake **Assistant** (never an autonomous submitter or
adverse-action determination-committer). **Repo:** `github.com/virtualryder/benefits_agent`. **Target tag:**
`v0.1.0-pilot-rc1` (cut after live EP1 — **done 2026-07-27**). **Build state:** control-plane hardened +
full CDK/Gate-B IaC, **live EP1-validated**; **91/91 offline tests** (control-plane + 22 CDK synthesis).
**Owner:** David Ryder (AWS HCLS SA).

---

## 0. Honesty guardrails (carried into every claim)

- The agent is an **assistant**: it prepares determination intake, eligibility determinations, duplicate holds,
  adverse-action determination **preparation**, and draft narratives. It never submits an determination, commits a adverse-action determination
  determination, or writes to an system-of-record gateway — Cedar-forbidden, tool-refused, human-gated.
- **the eligibility engine/FPL config is reference context**, not authoritative for a case, adverse-action determination, or incidence, and it
  never feeds the eligibility determination.
- **Evidence is author-produced and synthetic-only.** The CDK synthesizes, the controls are unit-proven,
  and the **live EP1 run is captured** (`evidence/EP1-VALIDATION.md`, 2026-07-27) — but on a disposable
  sandbox with synthetic data; no independent audit and no real PII yet.

## 1. What is done

| Area | Status |
|---|---|
| Control plane (signed sanitized_ref P0-1, token boundary P0-3, deterministic guards P0-2, fail-closed data-source policy P0-4) | ✅ |
| AWS CDK 7-stack set (`cdk/pv_stacks`) + Gate-B switches | ✅ synth-validated (22 assertions) |
| Deterministic Step Functions controller w/ AdverseNoticeHold terminal | ✅ (in CDK) |
| Release discipline (`RELEASE` + manifest + `VALIDATED_RELEASE` + consistency gate) | ✅ |
| START-HERE, DEPLOYMENT-GUIDE, PILOT-SCOPE, threat model, data-source policy, Gate-B checklist | ✅ |

## 2. Gates to pilot depth

**Gate A — code + synth (done).** 91/91 offline; CDK synthesizes to valid CloudFormation; release
scaffolding + core docs in place.

**Gate B — live EP1 validation (DONE, 2026-07-27, env `ben-val1`, us-east-1).** All Gate-B switches
deployed to a clean account; captured `validate_deployment.py` PASS, a happy-path run to the human gate, a
AdverseNoticeHold terminal, and the **strict PII canary PASS (0 leaks)**; torn down + residual-swept; recorded
in `VALIDATED_RELEASE.md` + `evidence/EP1-VALIDATION.md`; tag cut. The strict canary caught a real R3-2
gap (the determination notice crossed execution state) — fixed (narrative now server-side under a ref) and
re-validated. Prod-scale live load remains a customer-side exit item.

**Gate C — before real (PII) data.**
- ~~Pass-by-reference (R3-2)~~ — **done**: ingest/case-store keeps raw + masked content out of execution
  history (synth + runtime proven); the strict canary is expected to PASS on the EP1 run.
- **Drug-safety SME (benefits-program SME) sign-off** on the eligibility rules, processing clocks, duplicate logic, the
  redetermination/overpayment prepare-only boundary, and the determination notice language.
- **Enterprise IdP** federation round-trip; HIPAA/21 CFR Part 11 data-handling assessment. (The
  operating-model doc bundle — KEY-MANAGEMENT, RETENTION-PROFILES, INCIDENT-RESPONSE, AUDIT-READINESS,
  MCP-GATEWAY, CONFIGURATION-WORKSHEET, SME-REVIEW-PACKET — is now complete in `docs/`.)

**Gate D — before production.** Independent security testing / pen test; multi-account separation
(workload vs evidence); asymmetric-KMS signing evaluation; optionally sign the the eligibility engine (would
add a second signing domain); authoritative program rules
coding + system-of-record integration gateway + the state benefits system of record integration; measured pilot metrics; production ATO/CSV.

## 3. Explicit not-yet-true (say these out loud)

- Live EP1 evidence is captured (2026-07-27) but on a disposable sandbox with synthetic data only.
- Pass-by-reference (R3-2) **done in both directions** — raw, masked, AND the drafted narrative stay out
  of SFN state (strict canary PASS, 0 leaks). B5 tenant-scoped fetch is a follow-on.
- One signing domain (mask_pii); the eligibility engine is unsigned (authoritative-flag). GA-2 split N/A.
- No independent audit/pen test; no benefits-program SME SME sign-off; no enterprise IdP round-trip; no prod-scale load.
- authoritative program rules coding, system-of-record integration/gateway submission, the state benefits system of record, 21 CFR Part 11 CSV are adopter.

## 4. Recommended pilot shape

One product / one market · synthetic + de-identified retrospective cases first, then shadow mode ·
read-only everything · every output human-reviewed · no submission, no adverse-action commit, no gateway
writes · measured against handling time, duplicate-catch accuracy, eligibility/clock agreement with a
reviewer, and narrative edit rate.
