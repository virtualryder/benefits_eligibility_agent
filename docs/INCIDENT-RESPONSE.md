# Incident Response — Public Benefits Intake & Eligibility Screening Assistant

*Pilot IR procedure: who does what when something goes wrong, mapped to the detecting control.*

> **Applicable privacy frameworks (benefits, not healthcare).** The governing rules depend on the
> program, the state, and the data source — commonly: **state privacy / public-assistance
> confidentiality law**, **Medicaid confidentiality (42 CFR 431 Subpart F)**, **SNAP disclosure rules
> (7 CFR 272.1(c))**, **SSA data-exchange agreements**, and — **only where federal tax information (FTI)
> is in scope** — **IRS Publication 1075**, which requires prompt reporting of possible unauthorized
> inspection or disclosure to the IRS Office of Safeguards. **HIPAA is not the default framework here**
> and applies only if the agency is a covered entity/business associate for the data in question.
> **This pilot processes no FTI** (`PILOT-SCOPE.md`); if an agency introduces FTI, a Pub 1075 control
> mapping is required *before* that data is used.

---

## Roles

| Role | Responsibility |
|---|---|
| **Incident lead** | Agency benefits-program operations lead — owns the incident, decides notification |
| **Technical responder** | Agency IT / security — contains, rotates keys, pulls logs |
| **Privacy officer** | Determines reportability under the applicable state/program rule (and Pub 1075 if FTI) and drives notification |
| **Benefits-program SME** | Assesses impact on eligibility correctness, due process, and processing clocks |
| **Builder / SA** | Supports diagnosis of the assistant/pipeline (best-effort, pilot) |

## Detection sources (built)

- **PII-telemetry canary** — strict 0-hit assertion across Logs / X-Ray / DLQ / Step Functions history
  (R3-2 pass-by-reference keeps the raw application *and* the drafted notice out of execution state).
- **Guard-failure metric** (`Benefits/Governance :: GuardFailed`) — forged/tampered masking evidence, or
  an adverse action attempted without its advance notice.
- **WORM audit ledger** — tamper-evident hash chain (`lib/controls/verify_chain.py`).
- **CloudWatch alarms** on the above (ObservabilityStack) → encrypted SNS ops topic.

## Runbooks

### R1 — Suspected applicant PII in telemetry or a store
Contain the affected Lambda/version; determine what fields, whose data, how many records; rotate
KMS-encrypted secrets/signing material if exposure is possible; purge offending telemetry per the
agency's retention policy; the **privacy officer** makes the reportability determination under the
applicable state/program rule (and Pub 1075 if FTI were ever in scope) and drives notification; add the
failing case to the canary/redaction suite.

### R2 — An incorrect screen or notice reached a caseworker or applicant
Retract/correct. Outputs are **drafts and preliminary screens gated by a human**, so first trace the
approval record in the audit ledger. The **benefits-program SME** assesses impact on the applicant —
especially **processing-clock accuracy** (expedited vs standard) and whether any **adverse action** was
communicated without proper notice or appeal rights. Root-cause (stale FPL/threshold configuration, a
wrong household-composition assumption, an incorrect change classification); log the correction; hold
the affected cohort if the fault is systemic; confirm no adverse action was taken on the bad output.

### R3 — Forged / tampered evidence (guard-failure spike)
Determine attack vs. bug; confirm the pipeline **failed closed** (`ManualReview`, or `AdverseNoticeHold`
for a due-process failure) and that no case advanced on unverified state; verify the audit chain with
`verify_chain`; rotate signing keys if compromise is suspected (`docs/KEY-MANAGEMENT.md`).

### R4 — Unauthorized access / identity compromise
Disable the affected identity (MFA-enforced pool or federated IdP); run an access review; check the audit
ledger for actions taken under that identity — especially approvals; rotate credentials; if a caseworker
approval may have been made by the wrong person, treat every determination they committed as suspect.

### R5 — Due-process failure (adverse action without notice)
Treat as a **high-severity program incident, not just a technical one**. Identify affected households;
confirm whether any adverse action actually took effect; the benefits-program SME and agency counsel
determine corrective notice, restoration, and fair-hearing obligations; document the root cause of the
guard bypass or misclassification.

## Reportability & notification

The **privacy officer** determines whether an incident is reportable under the applicable framework
(state public-assistance confidentiality, Medicaid 42 CFR 431 Subpart F, SNAP 7 CFR 272.1(c), an SSA
data-exchange agreement, or IRS Pub 1075 where FTI applies) and drives notification on that framework's
timeline. This document makes **no categorical promise** about who is or is not notified — that is the
privacy officer's determination under the applicable rule and the facts.

## Before real applicant data: tabletop

Run a tabletop of **R1, R2 and R5** with the agency program office, IT/security, and the privacy officer
before the assistant touches real cases. Record the date and participants in the change log.
