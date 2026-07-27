# SME Review Packet — Benefits-Program SME Sign-off

*What a qualified benefits-program subject-matter expert must review and sign before this assistant sees
real applicant data in a pilot. A pre-production (Gate-C) gate — not satisfied by the code or the EP1 run.*

---

## Why this gate exists

The assistant runs a deterministic **eligibility screen + estimate** on **illustrative federal defaults**
(2026 HHS Federal Poverty Guidelines; SNAP-style 130% gross-income test, 7 CFR 273.9). Those defaults,
the processing clocks, the redetermination/overpayment logic, and the notice language must be reviewed by
someone who owns the program rules before any real household is screened. The platform enforces *that a
human decides*; the SME confirms *the rules the human is handed are correct for this program and state*.

## What the SME reviews and signs

1. **Eligibility rules & thresholds** — the FPL figures, the 130%-FPL gross-income test, categorical
   eligibility, and the expedited (7-day) vs standard (30-day) processing clock. Confirm these are the
   correct **per-program / per-state** rules for the pilot (or supply the correct configuration).
2. **Redetermination logic** — the classification of a change as ADVERSE / FAVORABLE / NO_CHANGE /
   NEEDS_REVIEW, and the rule that an **adverse** change requires timely advance notice.
3. **Due process** — confirm the **AdverseNoticeHold** behavior (an adverse redetermination without
   advance notice HOLDS, never proceeds) matches the agency's obligations under Goldberg v. Kelly and the
   program regulations (SNAP 7 CFR 273; Medicaid 42 CFR 435).
4. **Overpayment calculation** — the arithmetic and the boundary that the assistant *identifies* an
   overpayment but never *recovers* it or *refers fraud*.
5. **Determination-notice language** — the drafted notice's plain-language determination, reason,
   processing timeframe, and **fair-hearing / appeal-rights** statement. The notice is a DRAFT for a
   caseworker; confirm the language and the appeal-rights statement are adequate.
6. **Scope boundaries** — confirm the "will NOT do" list in `PILOT-SCOPE.md` (no adjudication, no adverse
   action, no fraud referral, no system-of-record writes) is complete and correct for this program.

## What the SME is NOT asked to do

Review the security controls (that is the CISO / independent security testing track), or re-derive the
governance model. The SME's sign-off is specifically on the **program correctness** of the rules,
clocks, redetermination/overpayment logic, and notice language.

## Sign-off record (attach to the pilot authorization)

| Item | Reviewer | Date | Accept / changes required |
|---|---|---|---|
| Eligibility rules & thresholds (FPL, 130% test, categorical, clock) | | | |
| Redetermination classification + advance-notice rule | | | |
| Due-process AdverseNoticeHold behavior | | | |
| Overpayment calculation + recover/refer boundary | | | |
| Determination-notice language + appeal rights | | | |
| Scope boundaries (`PILOT-SCOPE.md`) | | | |

Until this packet is signed, the pilot runs on **synthetic and de-identified retrospective data only**,
in shadow mode, with every output human-reviewed (see `BENEFITS-PILOT-READINESS-PLAN.md`).
