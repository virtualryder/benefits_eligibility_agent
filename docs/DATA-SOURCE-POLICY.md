# Data-Source Policy — Public-Benefits Eligibility Assistant

*Correctness over availability. What data the assistant uses, where it comes from, and the fail-closed
rule when it can't be trusted. One page.*

---

## The assistant has NO external data dependency

Unlike the sibling agents (housing → HUD income limits, financial-aid → College Scorecard, PV → openFDA
FAERS), the benefits eligibility engine reaches **no external API at determination time**. The eligibility
screen runs entirely on **public HHS Federal Poverty Guidelines** compiled into the tool as configuration:

- **Source:** HHS annual poverty guidelines — 2026 figures (Federal Register 2026-00755, published
  2026-01-15): 1-person household $15,960/yr, +$5,680 per additional member (48 contiguous states + DC).
- **Test:** SNAP-style gross-income limit = **130% of FPL** (7 CFR 273.9); expedited-service screen on
  low income + low liquid resources.
- **Nature:** these are **illustrative federal defaults**, labeled as such. The authoritative,
  market-specific program rules, thresholds, categorical-eligibility criteria, and their frequent policy
  churn are **per-program / per-state CONFIGURATION** and remain the agency's responsibility.

Because there is no external call, the network runs with **zero public egress** (see
`docs/Production-Network-Hardening.md` and the Gate-B checklist): the governed Lambdas have no internet
route at all. This is a stronger posture than an egress allowlist — there is no external destination to
allow or deny.

## Fail-closed rule (P0-4)

The eligibility engine is deterministic and self-contained, so "source down" is not a runtime failure
mode. The fail-closed discipline instead governs **de-identification** and **model output**:

- **No processing on un-masked input.** `assess_eligibility`, `redetermine`, `overpayment`, and
  `draft_notice` all REFUSE any input not proven de-identified by a `mask_pii`-signed `sanitized_ref`
  (P0-1). A `deidentified: true` boolean is never accepted. If masking cannot run, nothing downstream
  proceeds.
- **No fabricated determination.** The engine returns `ELIGIBLE`, `INELIGIBLE`, or `NEEDS_REVIEW` from the
  rules only; missing/insufficient facts route to `NEEDS_REVIEW` (and the controller's `ManualReview`),
  never to a guessed outcome.
- **No adverse action without due process.** An adverse redetermination lacking the required advance
  notice HOLDS at `AdverseNoticeHold` — the platform enforces Goldberg v. Kelly, not the model.

## What is explicitly NOT an authoritative source

The federal defaults here are a **screen / estimate** for case preparation. They are not an authoritative
eligibility determination, and the assistant never presents them as one. Income and identity verification
against authoritative systems (IEVS / SAVE / PARIS-class matches), the state's authoritative rules, and
the system of record are the agency's — see `PILOT-SCOPE.md`.
