# Audit Readiness — Control-to-Evidence Matrix (Benefits)

*Maps each obligation the assistant touches to the artifact/test/log that demonstrates the control — for
an agency QA/compliance reviewer or an independent auditor. Evidence to date is **author-produced on
synthetic data**; independent testing is a pre-production item.*

---

## Regulatory frame (benefits)

**Due process for adverse actions** (*Goldberg v. Kelly*; SNAP 7 CFR 273, Medicaid 42 CFR 435) ·
**state public-assistance confidentiality** and **Medicaid confidentiality (42 CFR 431 Subpart F)** ·
**SNAP disclosure rules (7 CFR 272.1(c))** · SSA data-exchange agreements where applicable ·
**IRS Publication 1075 only where federal tax information is in scope — this pilot processes no FTI** ·
StateRAMP / NIST 800-53 as the agency requires. Agency SOPs govern the final determination.

## Control-to-evidence matrix

| Obligation | Control | Evidence (artifact / test / log) |
|---|---|---|
| **Limit access to applicant data; account for actions** | Cedar deny-by-default at the AgentCore Gateway; identity-derived approver; WORM audit ledger records every consequential action | `tests/test_signoff_identity.py`; audit hash-chain `verify_chain`; `docs/THREAT-MODEL.md` |
| **PII de-identification before model use or audit write** | Deterministic masking proven by a signed `sanitized_ref` (a caller-supplied boolean is never accepted); **pass-by-reference** keeps the raw application *and* the drafted notice out of workflow state | `tests/test_sanitized_artifact.py`; `tests/test_pass_by_reference.py`; `tests/test_draft_pass_by_reference.py`; `tests/test_cdk_stacks.py`; live: strict canary 0 leaks (`evidence/EP1-VALIDATION.md`) |
| **Preliminary income screen is deterministic and reproducible** | Rules engine over public HHS Federal Poverty Guidelines + SNAP-style gross-income test; no model, no licensed data; **illustrative federal defaults, not an authoritative determination** | `agents/benefits-eligibility/tools/assess_eligibility.py`; `tests/test_fpl_pinned.py`; `tests/test_eval.py`; `docs/SME-REVIEW-PACKET.md` |
| **Processing clock (expedited 7-day vs standard 30-day)** | Deterministic expedited screen on income + liquid resources | `tests/test_eval.py`; SME sign-off row in `docs/SME-REVIEW-PACKET.md` |
| **Due process — no adverse action without advance notice** | Deterministic `adverse_notice` guard; an adverse redetermination lacking notice terminates at `AdverseNoticeHold` | `tests/test_workflow_guards.py`; live: `evidence/EP1-VALIDATION.md` (AdverseNoticeHold captured) |
| **No adjudication / no autonomous adverse action** | Cedar `no_self_commit` + tool refusal; human `waitForTaskToken` sign-off; approver ≠ requester | `tests/test_tools.py`; workflow gate asserted in `tests/test_cdk_stacks.py` |
| **Fraud referral is human-only** | Cedar `no_self_fraud_referral` + tool refusal | `tests/test_tools.py` |
| **Overpayment is identified, never recovered** | `overpayment` computes only; recovery/referral are human actions outside the assistant | `tests/test_tools.py`; `PILOT-SCOPE.md` |
| **Encryption at rest / in transit** | Customer-managed KMS over tables, secrets, Lambda env, log groups, SNS; **zero-public-egress** private networking (AWS endpoints only) | `tests/test_cdk_stacks.py` (CMK + `test_network_zero_public_egress`); `docs/KEY-MANAGEMENT.md` |
| **Audit immutability** | Append-only + hash chain + IAM Deny on update/delete/Object-Lock bypass; WORM Object Lock | `tests/test_audit_chain.py`; tamper-Deny asserted in `tests/test_cdk_stacks.py` |
| **Least privilege / no resource discovery** | Exact-ARN IAM; no role-lookup-by-prefix; zero IaC users, no default passwords | `tests/test_token_boundary.py`; `tests/test_cdk_stacks.py` |
| **Change integrity** | `RELEASE` single-source + consistency gate; tagged releases; cross-vertical term gate | `tests/test_release_consistency.py`; `tests/test_no_cross_vertical_terms.py` |

## How to run an audit dry-run

Check out the tag, open each cited artifact/test, and confirm it demonstrates the control; walk
`docs/THREAT-MODEL.md` as a mock question set; compare claims against
[`docs/VALIDATED-MATRIX.md`](VALIDATED-MATRIX.md). Open items live in `RELEASE-MANIFEST.md` and
`BENEFITS-PILOT-READINESS-PLAN.md`.

## Not yet proven (state these plainly)

Live EP1 evidence exists (2026-07-27, synthetic, torn down) but there is **no independent deployment, no
independent audit or penetration test, no benefits-program SME sign-off on the rules, no enterprise IdP
round-trip, no authoritative state/program rule set, and no system-of-record integration**. No real
applicant data has ever been processed.
