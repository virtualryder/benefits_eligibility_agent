# START HERE — Public-Benefits Eligibility Screening & Determination-Support Assistant

*One page. What this is, what's proven, how to evaluate it, and what a pilot looks like. Target
validated release: **[`v0.1.0-pilot-rc1`](https://github.com/virtualryder/benefits_agent/releases/tag/v0.1.0-pilot-rc1)**
(cut after the live EP1 validation; deploy tags, never `main`). Supported deployment path: **AWS CDK**
(`cdk/`); the shell engine is legacy/internal.*

> **Evaluating for a pilot?** Read [`PV-PILOT-READINESS-PLAN.md`](PV-PILOT-READINESS-PLAN.md) and
> [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md) (authoritative counts + limitations). It states plainly
> what is **not yet true**: no live EP1 evidence yet, no independent audit, no benefits-program SME sign-off,
> synthetic data only.

## What this is (and is not)

A **governed assistant** for benefits intake: it extracts non-PII decision fields from an
benefits source, pulls **aggregate FPL config background (reference context only)**, de-identifies PII,
runs a deterministic **SNAP/Medicaid program rules / 7 CFR 273 / 42 CFR 435 eligibility + processing-clock** assessment, detects
duplicate ICSRs (holding them so they are never double-reported), **prepares** a redetermination/overpayment
determination, and drafts a determination notice — every consequential action human-approved, exactly once,
with a tamper-evident audit trail.

It is **NOT an autonomous submitter**: no determination submission, no adverse-action commit, no system-of-record gateway write —
Cedar-forbidden, tool-refused, human-gated ([`PILOT-SCOPE.md`](PILOT-SCOPE.md)). the eligibility engine/FPL config is
reference context, never a case-level or adverse-action determination source.

## Evidence provenance — read this honestly

The control plane is ported from the proven financial-aid/housing pattern (signed sanitized-ref masking,
token boundary, deterministic Step Functions controller). **What's proven today: the 95-test offline
suite** — control-plane behavior + full CDK stack synthesis. **What's NOT proven yet: a live EP1
clean-account run** with captured evidence; that run cuts `v0.1.0-pilot-rc1`. See `RELEASE-MANIFEST.md`.

## Reading order by role

| You are | Read, in order |
|---|---|
| **Solution Architect** | [`DEPLOYMENT-GUIDE.md`](DEPLOYMENT-GUIDE.md) → [`cdk/README.md`](cdk/README.md) → [`PV-PILOT-READINESS-PLAN.md`](PV-PILOT-READINESS-PLAN.md) |
| **CISO / security** | [`docs/THREAT-MODEL.md`](docs/THREAT-MODEL.md) → [`docs/GATE-B-CHECKLIST.md`](docs/GATE-B-CHECKLIST.md) → [`docs/DATA-SOURCE-POLICY.md`](docs/DATA-SOURCE-POLICY.md) |
| **Safety / benefits-program SME leadership** | [`PILOT-SCOPE.md`](PILOT-SCOPE.md) → README §controls → the pilot offer below |
| **Auditor / compliance** | [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md) → [`VALIDATED_RELEASE.md`](VALIDATED_RELEASE.md) |

**Regulatory frame:** SNAP/Medicaid program rules · 7 CFR 273 / 42 CFR 435 (postmarket expedited/periodic reporting) · program-integrity ·
HIPAA (PII) · 21 CFR Part 11 (electronic records/signatures — adopter CSV). Adopter work: authoritative program rules
coding, system-of-record integration + FPL config/EudraVigilance gateway, the state benefits system of record integration.

## Status in one line

Control-plane hardened + full CDK/Gate-B IaC, **live EP1-validated** (2026-07-27, `ben-val1`),
**88/88 offline tests (incl. 22 CDK synthesis)**, tag `v0.1.0-pilot-rc1`. Evidence:
`evidence/EP1-VALIDATION.md` (validate PASS, controller to the human gate, AdverseNoticeHold, **strict PII
canary 0 leaks**). Next: a credentialed drug-safety (benefits-program SME) SME sign-off, enterprise IdP round-trip, and
independent security testing before real data.
