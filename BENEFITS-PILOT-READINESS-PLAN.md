# Benefits Pilot Readiness Plan

**Product:** Public Benefits Intake, Eligibility Screening & Caseworker Decision-Support **Assistant**
(never an adjudicator; never denies, reduces, terminates, refers fraud, or writes to a system of record).
**Repo:** `github.com/virtualryder/benefits_eligibility_agent`. **Tag:** `v0.1.2-pilot-rc1` (cut after the
live EP1 run, 2026-07-27). **Build state:** control plane hardened + full CDK/Gate-B IaC, **live
EP1-validated**; **133 offline tests** on current main (control-plane + 13 CDK synthesis). **Owner:** David Ryder (AWS SA).

---

## 0. Honesty guardrails (carried into every claim)

- The agent is an **assistant**: it summarizes an application, de-identifies PII, runs a **preliminary
  income screen**, prepares redetermination/overpayment findings, and drafts a determination notice.
  It never adjudicates, denies, reduces, terminates, refers fraud, calculates a benefit allotment, or
  writes to a system of record — Cedar-forbidden, tool-refused, human-gated.
- **The rules are illustrative federal defaults**, not authoritative eligibility: public HHS Federal
  Poverty Guidelines with a SNAP-style gross-income test. This is **not** a SNAP, Medicaid, or TANF
  eligibility engine. Authoritative state/program rules are adopter configuration.
- **Evidence is author-produced and synthetic-only.** The live EP1 run is captured
  (`evidence/EP1-VALIDATION.md`, 2026-07-27) but on a disposable sandbox; **no independent deployment,
  no independent audit, no real applicant data**.

## 1. What is done

| Area | Status |
|---|---|
| Control plane (signed `sanitized_ref` P0-1, token boundary P0-3, deterministic guards P0-2, fail-closed data-source policy P0-4) | ✅ |
| AWS CDK 7-stack set (`cdk/ben_stacks`, prefix `ben-`) + Gate-B switches | ✅ synth-validated (13 assertions) |
| Deterministic controller with the **AdverseNoticeHold** due-process terminal | ✅ (in CDK, live-proven) |
| R3-2 pass-by-reference, both directions (application + drafted notice) | ✅ (live strict canary, 0 leaks) |
| Zero-public-egress private networking (no NAT/IGW/firewall) | ✅ live-validated |
| Release discipline (`RELEASE` + manifest + `VALIDATED_RELEASE` + consistency + cross-vertical gates) | ✅ |
| Core + operating-model docs (START-HERE, DEPLOYMENT-GUIDE, PILOT-SCOPE, threat model, data-source policy, Gate-B, key mgmt, retention, IR, audit readiness, MCP gateway, config worksheet, SME packet) | ✅ |

## 2. Gates

**Gate A — code + synth (done).** 133/133 offline (CI); CDK synthesizes to valid CloudFormation.

**Gate B — live EP1 validation (done, 2026-07-27, env `ben-val1`, us-east-1).** All Gate-B switches on a
clean account: `validate_deployment.py` PASS; the controller ran every guard to the human sign-off gate;
an adverse redetermination without advance notice held at `AdverseNoticeHold`; **strict PII canary PASS
(0 leaks)**; MFA pool ON with 0 users; torn down with a zero-residual sweep. One real defect was found and
fixed during the run (zero-egress SG blocked the S3/DynamoDB gateway endpoints).

**Gate B-exit — independent reproduction (NOT done; highest-priority next step).**
1. **A second AWS SA deploys the exact tag** unaided and runs the validation suite — the single biggest
   credibility gap today (all current evidence is author-produced).
   **Kit is ready — this now needs a person, not more engineering:** hand the verifier
   [`docs/INDEPENDENT-VERIFICATION.md`](docs/INDEPENDENT-VERIFICATION.md); they run
   `python scripts/independent_verify.py --verifier "<name>" --env iv1` (~45–75 min, a few dollars,
   self-tearing-down) and sign `evidence/INDEPENDENT-VERIFICATION-RESULT.md`. Until that signed result
   exists, a CI gate keeps every document saying independent verification has **not** happened.
2. **Live concurrency + failure injection**: peak/renewal surge, Lambda/Bedrock/Comprehend throttling,
   KMS failure, DynamoDB conditional-write conflict, WORM-succeeds/ledger-fails (and the inverse), two
   caseworkers approving simultaneously, a case changed after approval, a stale policy version.
3. **Cedar negative-authorization matrix as live evidence** against the deployed ENFORCE gateway (role
   and tool denies, self-approval, fraud referral, expired/forged approval token).
4. **Tenant-scoped case-store fetch** — bind authenticated subject + agency/tenant + case id + role on
   every retrieval, with cross-tenant negative tests. (Today the tenant is signed into artifacts; that is
   not sufficient for a shared deployment.)

**Gate C — before real applicant data (shadow mode).**
- **Enterprise IdP federation round-trip** (Entra/Okta) with IdP-group → caseworker/supervisor role
  mapping, MFA, session revocation, joiner/mover/leaver.
- **One-state, one-program (SNAP) rule set** as versioned configuration — gross **and** net income tests,
  standard/earned-income/shelter/dependent-care/medical deductions, resource rules, categorical and
  broad-based categorical eligibility, proration — replacing the illustrative federal screen.
- **Benefits-program SME sign-off** on the rules, clocks, redetermination/overpayment logic, and notice
  language (`docs/SME-REVIEW-PACKET.md`).
- **Read-only system-of-record connector** (design + mock) for that program.
- **FTI determination**: decide whether federal tax information is in scope; if yes, an IRS Pub 1075
  control mapping **before** that data is used; if no, an explicit "no FTI processed" boundary.
- Agency privacy assessment; state retention approval; incident-response tabletop; Section 508 /
  plain-language review of the notice; independent security testing.
- **Structured decision explanation** for caseworkers: facts used and missing, income included/excluded,
  deductions applied, categorical treatment, every rule triggered, rule version + effective date, and the
  reason for `NEEDS_REVIEW` — not just ELIGIBLE/INELIGIBLE/NEEDS_REVIEW.

**Gate D — before production.** Complete state/program rules; authoritative verification integrations
(IEVS / SAVE / PARIS-class); integrated-eligibility-system connector; notice and fair-hearing/appeal
workflow; benefit-allotment calculation where in scope; policy versioning and effective dating with
stale-screen invalidation; multi-account separation (workload vs. evidence); independent penetration
test; StateRAMP/ATO or agency authorization; DR with tested RPO/RTO; independent fairness and accuracy
review; measured positive ROI; customer acceptance testing.

## 3. Explicit not-yet-true (say these out loud)

- Live EP1 evidence exists but is **author-produced, synthetic, and on a disposable sandbox**.
- **No independent deployment** of the tag by a third party; no independent audit or pen test.
- **The eligibility logic is a preliminary federal-threshold screen**, not authoritative SNAP/Medicaid/
  TANF eligibility. Medicaid and TANF are **not supported determinations**; unemployment insurance is
  **out of scope entirely**.
- No enterprise IdP round-trip; tenant-scoped fetch is a follow-on; no prod-scale load or failure
  injection; no system-of-record integration; no notice/appeal workflow.
- One signing domain (only `mask_pii` signs); there is no external authoritative source to sign.

## 4. Recommended first pilot — one state, one program

**One-state SNAP intake and preliminary-screening pilot**, read-only shadow mode. Synthetic cases first,
then de-identified retrospective cases with agency approval. Every result human-reviewed.

**In scope:** application summarization · preliminary gross-income screen · expedited-service indication ·
missing-information identification · draft applicant communication.

**Explicitly excluded:** final eligibility · net-income determination unless fully configured · benefit
allotment · adverse action · fraud referral · overpayment establishment or recovery · system-of-record
write-back · fair-hearing decisions · Medicaid · TANF · unemployment insurance.

**Success gates:** zero authorization bypasses · zero PII in telemetry · zero cross-case or cross-tenant
access · high agreement with caseworker preliminary screens · high expedited-clock agreement · acceptable
notice edit rate · reduced intake handling time · documented override reasons · a written go/no-go.

**Do not broaden to more programs** before one state-specific implementation is validated — added breadth
without depth reduces customer credibility.
