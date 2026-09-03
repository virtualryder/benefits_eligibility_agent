# Pilot Scope — Public-Benefits Eligibility Screening & Communication Assistant

*What a pilot of this assistant is, what it is explicitly NOT, and what the adopter owns. Due process is
the headline constraint. One page.*

---

## Due process is the defining constraint

A benefits determination that reduces, suspends, or terminates aid triggers constitutional and statutory
**due-process** protections (Goldberg v. Kelly; program regulations — SNAP 7 CFR 273, Medicaid 42 CFR 435).
That is exactly why this assistant **screens and prepares, never adjudicates**, and why every adverse action
stays human-committed, with timely written notice and appeal rights. The deterministic guard set enforces an
**advance-notice HOLD** on any adverse redetermination so the platform — not the model — protects due process.

## What it is

A **governed assistant** for benefits intake: it extracts non-PII decision fields, de-identifies PII, runs a
deterministic **eligibility screen + estimate** and the processing clock (expedited vs standard), prepares
**redetermination** and **overpayment** findings, and drafts a determination notice — then **pauses at a
caseworker sign-off gate**. Every consequential action is made and committed by a qualified human.

## What it will NOT do (do not claim these)

- **No adjudication / no adverse action.** The assistant never denies, reduces, suspends, or terminates
  benefits; a caseworker commits every determination (Cedar `no_self_commit`, tool-refused).
- **No fraud referral.** Referring a case as suspected fraud is a human-only action (Cedar
  `no_self_fraud_referral`, tool-refused).
- **No writes to the system of record.** Shadow mode reads nothing and writes nothing into the official case.
- **No authoritative eligibility determination.** Output is a **screen/estimate** on illustrative federal
  thresholds; the authoritative rules and verification are the agency's.
- **No PII unmasked downstream.** Tools refuse anything not proven de-identified by a signed `sanitized_ref`
  (P0-1); a `deidentified: true` boolean is never accepted.

## Adopter / out-of-scope (state in every conversation)

Authoritative **state eligibility rules** and their frequent policy churn · **income/identity verification**
against authoritative sources (IEVS / SAVE / PARIS-class matches) · **system-of-record** integration (the
state benefits/eligibility system) · **notice and appeal / fair-hearing** workflow · **overpayment
establishment and recovery** rules · multi-program interactions · **IRS Pub 1075** controls where federal tax
info is used · **Section 508 / plain-language** accessibility for citizen-facing notices (arguably more
important here, since notices go directly to recipients) · enterprise **IdP** federation · **StateRAMP / ATO**.

## Maturity (honest, code-accurate)

**Present + hardened:** signed-`sanitized_ref` de-identification (P0-1), token boundary (P0-3),
deterministic guard set with the due-process advance-notice HOLD (P0-2), Cedar deny-by-default,
`no_self_commit` + `no_self_fraud_referral`, WORM hash-chained audit, human separation-of-duties sign-off,
the FPL-pinned drift gate, **R3-2 pass-by-reference in both directions** (application + drafted notice).
**Plus the full 7-stack AWS CDK set + Gate-B posture** (zero-public-egress private networking ·
customer-managed KMS · MFA identity · tenant pin), release discipline (RELEASE + manifest +
VALIDATED_RELEASE + consistency and cross-vertical gates), and the operating-model doc bundle.
Suite: **154 offline tests** (control-plane + 16 CDK synthesis + 3 doc-integrity gates + 4
independent-verification gates + 3 CI-completeness gates + the doc-count gate) — authoritative count in
[`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md). Locally you see `124 passed, 1 skipped`: one gate asserts
the CDK libraries are installed and runs only inside CI.
A separate legacy shell **governance demo** reports 29 live checks in Cedar ENFORCE; it is **not** part
of the 125.

**Live-validated (EP1, 2026-07-27, env `ben-val1`, us-east-1):** `validate_deployment.py` PASS; the
controller ran to the human sign-off gate; **AdverseNoticeHold** held an adverse redetermination; **strict
PII canary 0 leaks**; MFA pool ON with 0 users; torn down + residual-swept
([`evidence/EP1-VALIDATION.md`](evidence/EP1-VALIDATION.md)).

**Not yet — say these plainly:** the eligibility logic is a **preliminary federal-threshold screen**, not
authoritative program rules; **no independent deployment** of the tag by a third party; no independent
audit or penetration test; no benefits-program SME sign-off on the rules or notice language; no enterprise
IdP round-trip; tenant-scoped case-store fetch is a follow-on; no prod-scale load or failure-injection
testing; no system-of-record integration; **no real applicant data has ever been processed**. Full gate
sequence: [`BENEFITS-PILOT-READINESS-PLAN.md`](BENEFITS-PILOT-READINESS-PLAN.md).

## Recommended pilot shape

One program / one state · synthetic and de-identified retrospective cases first, then shadow mode ·
read-only everything · every output human-reviewed · no adjudication, no adverse action, no fraud referral,
no SoR writes · measured against verification handling time, repeat-contact rate, determination agreement with
a caseworker, and notice edit rate.
