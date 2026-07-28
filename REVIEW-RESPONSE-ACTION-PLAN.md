# Benefits Agent — CIO/CISO/Architecture/GTM Review: Validation + Action Plan

*Response to the independent review of `v0.1.0-pilot-rc1`. Verdict on each theme, then a prioritized
plan. Date: 2026-07-27.*

---

## Validation of the review (what's true, what's already covered, what's off)

**Confirmed valid (highest priority):**

- **Documentation is contaminated by the sibling verticals.** Grep-confirmed in the pushed repo:
  START-HERE, DEPLOYMENT-GUIDE, INCIDENT-RESPONSE, AUDIT-READINESS, BENEFITS-PILOT-READINESS-PLAN still
  carry PV/EDU terms (`drug`, `suspect product`, `narrative`, HIPAA, `21 CFR`, `fda.gov`, safety
  physician). A prior cleanup pass missed `drug`/`suspect product`/`narrative`/HIPAA/`fda.gov`/safety
  physician and never rewrote START-HERE / INCIDENT-RESPONSE / DEPLOYMENT-GUIDE headers.
- **Test counts conflict.** START-HERE says 95 and 88 (and "22 CDK" — a PV number); DEPLOYMENT-GUIDE
  says 88; PILOT-SCOPE says 73; the authoritative number is **91** (RELEASE-MANIFEST/VALIDATED_RELEASE).
  The `29 passed` in README is the *live shell governance demo* — a separate artifact, not the offline
  suite — but the docs don't disambiguate it.
- **Product scope is overclaimed.** README frames SNAP/Medicaid/TANF/unemployment insurance; the actual
  engine is a **preliminary FPL / SNAP-style gross-income screen**. That cannot be presented as a
  multi-program eligibility engine.

**Valid but already scoped as adopter / Gate-C-D work** (needs consolidation into one honest matrix, not
new claims): independent pen test; enterprise IdP round-trip; FTI / IRS Pub 1075 determination; tenant-
scoped case-store fetch; multi-account evidence isolation; live concurrency / failure-injection at scale;
system-of-record integration; complete state/program rules. These are in PILOT-SCOPE / READINESS today but
scattered and partly buried under contaminated text.

**Minor inaccuracies in the review (do not action):** the "no live EP1 evidence" and "EP1 remains unrun"
lines it cites are *stale copied text*, not the truth — the live EP1 genuinely ran and is captured in
`evidence/EP1-VALIDATION.md` (fixing the stale text is part of P0). The `28/28 live` vs `29` confusion is
the shell demo, which P0 will label distinctly.

**Bottom line:** the governance engineering is real and strong; the *documentation and the domain/scope
framing* are the blockers. The review's product-framing recommendation — narrow to **one state, one
program (SNAP intake screening)** — is correct and adopted below.

---

## P0 — Documentation integrity + honest framing (blocks any AWS/customer showing)

*Target: same-day. All low-risk edits + one CI guard. No new AWS spend.*

- **P0-1 — Rewrite START-HERE.md** fresh, benefits-only: assistant framing, correct reading order by
  role, kill `95`/`88`/`22 CDK`, remove all PV terms, point to the real EP1 evidence + tag.
- **P0-2 — Rewrite DEPLOYMENT-GUIDE.md**: remove `drug`/`suspect product`/`narrative`/`fda.gov`; benefits
  workflow input (`case_ref` + `redetermination`); fix `88`→`91`; zero-egress network (no firewall).
- **P0-3 — Rewrite INCIDENT-RESPONSE.md**: benefits privacy frameworks (state privacy law, Medicaid
  confidentiality 42 CFR 431 Subpart F, IRS Pub 1075 *where FTI applies*, SSA data agreements) — remove
  HIPAA-as-default and the safety-physician role.
- **P0-4 — Rewrite AUDIT-READINESS.md + BENEFITS-PILOT-READINESS-PLAN.md** fully benefits (they are still
  PV templates in places): due-process, eligibility-rule provenance, notice language, human sign-off.
- **P0-5 — Reconcile every test count to 91**, and label the `29`-check shell demo as the *live
  governance demo* (distinct from the 91 offline). One number, everywhere.
- **P0-6 — Tighten the product claim.** Reframe README + PILOT-SCOPE as **"Public Benefits Intake,
  Eligibility Screening & Caseworker Decision-Support Assistant."** State plainly: the rules are a
  *preliminary federal-threshold (FPL / SNAP-style) income screen*, not an authoritative determination;
  **remove unemployment insurance**; mark Medicaid/TANF as illustrative, not supported determinations.
- **P0-7 — Add a CI forbidden-term gate** (`tests/test_no_cross_vertical_terms.py`): fail the build on
  `drug`, `ICSR`, `openFDA`/`FAERS`, `EudraVigilance`, `causality`, `seriousness`, `21 CFR 314`,
  `safety physician`, `QPPV`, `pharmacovigilance`, `atorvastatin` in tracked docs — prevents regression.
- **P0-8 — Fix the GTM docs** (Cost-and-Latency "live authoritative lookup" row, Architecture-Diagram
  `openFDA` edge, Production-Network-Hardening) to benefits reality: **no external lookup, zero egress.**
- **P0-9 — Publish a single VALIDATED / NOT-VALIDATED matrix** (one page) so a reviewer sees exactly
  what's proven (synthetic EP1) vs. pending (IdP, pen test, scale, real data). Refresh the GitHub release
  notes to match. Then: run the 91 suite + the new CI gate, commit, push.

## P1 — Assurance + one-program pilot enablement (before a real-data shadow pilot)

- **P1-1 — Independent deploy of the exact tag** by a second AWS SA (reproducibility proof; the biggest
  single credibility gap the review names).
- **P1-2 — Tenant-scoped case-store fetch**: bind authenticated subject + agency/tenant + case id + role
  on every `get_case`/artifact retrieval; add cross-tenant negative tests (offline + live).
- **P1-3 — Cedar negative-authz matrix as live evidence**: role/tool denies, self-approval, fraud-
  referral, expired/forged approval token — captured against the deployed ENFORCE gateway.
- **P1-4 — Enterprise IdP federation round-trip** (Entra/Okta) with IdP-group → caseworker/supervisor
  role mapping; MFA + session revocation.
- **P1-5 — One-state SNAP rule set**: turn the illustrative FPL screen into a real *one-program* screen —
  gross + net income tests, standard/earned-income/shelter/dependent-care/medical deductions, resource
  rules, categorical & broad-based categorical eligibility, proration — as versioned configuration, with
  a **benefits-program SME sign-off** (`docs/SME-REVIEW-PACKET.md`).
- **P1-6 — Read-only system-of-record connector** (design + mock) for that one program.
- **P1-7 — Live concurrency + failure-injection**: peak/renewal surge, Lambda/Bedrock/Comprehend
  throttle, KMS failure, DynamoDB conditional-write conflict, WORM-ok/ledger-fail (and inverse), dual
  simultaneous approval, case-changed-after-approval, stale policy version.
- **P1-8 — FTI / IRS Pub 1075 determination**: decide if FTI is in scope for the pilot agency; if yes, a
  control-mapping doc; if no, an explicit "no FTI processed" boundary in scope + IR.
- **P1-9 — Structured decision-explanation output**: facts used/missing, income included/excluded,
  deductions applied, categorical treatment, every rule triggered, rule version + effective date, reason
  for NEEDS_REVIEW — so a caseworker gets more than ELIGIBLE/INELIGIBLE/NEEDS_REVIEW.

## P2 — Production (large; not near-term)

Complete state/program rules; authoritative verification integrations (IEVS/SAVE/PARIS); integrated-
eligibility-system connector; notice & fair-hearing/appeal workflow; benefit-allotment calculation;
policy versioning + effective-dating with stale-screen invalidation; multi-account evidence isolation;
independent pen test; StateRAMP/ATO or customer authorization; DR + RPO/RTO testing; measured positive
ROI with a named agency; independent fairness/accuracy review; CAT.

---

## Recommended first pilot (adopted from the review)

**One-state SNAP intake & preliminary-screening pilot** — read-only shadow mode, synthetic cases first
then de-identified retrospective, every result human-reviewed. Scope: application summarization,
preliminary gross-income screen, expedited-service indication, missing-information identification, draft
applicant communication. **Excludes**: final eligibility, benefit calculation, adverse action, fraud
referral, overpayment recovery, SoR write-back, Medicaid/TANF/UI. Success gates: 0 authorization
bypasses, 0 PII in telemetry, 0 cross-case/tenant access, high agreement with caseworker preliminary
screens, acceptable notice-edit rate, reduced intake handling time, documented override reasons, a
written go/no-go.

## Do NOT do next

Add more programs. Broadening before one state-specific SNAP screen is validated raises the feature count
and *lowers* customer credibility — exactly the review's warning.
