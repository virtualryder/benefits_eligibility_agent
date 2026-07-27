# Audit Readiness — Control-to-Evidence Matrix (Benefits)

*Maps each obligation the assistant touches to the artifact/test/log that demonstrates the control —
for an inspector or an internal QA/compliance reviewer. Evidence to date is author-produced on synthetic
data; independent testing + the live EP1 run are pre-production items.*

---

## Regulatory frame

HIPAA (PII) · SNAP/Medicaid program rules + 7 CFR 273 / 42 CFR 435 (postmarket expedited/periodic reporting) · program-integrity · 21 CFR Part
11 (electronic records/signatures — adopter CSV) · sponsor SOPs.

## Control-to-evidence matrix

| Obligation | Control | Evidence (artifact / test / log) |
|---|---|---|
| **HIPAA — limit access; account for disclosures** | Cedar deny-by-default; identity-derived approver; WORM audit ledger records every consequential action | `tests/test_signoff_identity.py`; audit hash-chain `verify_chain`; `docs/THREAT-MODEL.md` T4/T8 |
| **PII de-identification before model/audit** | Deterministic masking proven by a signed `sanitized_ref` (boolean never accepted); **pass-by-reference** keeps raw+masked content out of workflow state | `tests/test_sanitized_artifact.py`; `tests/test_pass_by_reference.py`; `tests/test_cdk_stacks.py` (no raw/masked in SFN) |
| **Seriousness + processing clock (7 CFR 273 / 42 CFR 435 / ICH system-of-record)** | Deterministic rules engine (serious criteria; expedited 15-day / periodic / routine) | `assess_seriousness.py`; `tests/test_eval.py` golden cases; `docs/SME-REVIEW-PACKET.md` |
| **No double-reporting** | Deterministic duplicate detection → terminal AdverseNoticeHold (no submission) | `tests/test_workflow_guards.py::test_duplicate_holds`; `test_audit_chain.py` |
| **Causality is human-only, documented (program-integrity)** | Cedar `no_self_causality_commit` + tool refusal; prepare-only + required rationale | `tests/test_tools.py::test_core_commit_causality_refused`, `::test_record_causality_requires_rationale` |
| **No autonomous submission** | Cedar `no_self_submit` + refusal; human `waitForTaskToken` sign-off; approver ≠ requester | `tests/test_tools.py::test_core_finalize_refused`; workflow gate (`tests/test_cdk_stacks.py`) |
| **Due-process advance-notice HOLD** | an adverse redetermination without advance notice HOLDS at `AdverseNoticeHold` (deterministic `adverse_notice` guard; Goldberg v. Kelly) | `tests/test_workflow_guards.py` |
| **Encryption at rest/in transit** | Customer-managed KMS over tables/secrets/env/logs/SNS; private networking; TLS to the eligibility engine | `tests/test_cdk_stacks.py::test_customer_managed_kms...`; `docs/KEY-MANAGEMENT.md` |
| **Audit immutability** | Append-only + hash chain + IAM Deny on update/delete/bypass; WORM Object Lock | `tests/test_audit_chain.py`; compute tamper-Deny (`tests/test_cdk_stacks.py`) |
| **Least privilege / no discovery** | Exact-ARN IAM; no role-lookup-by-prefix; zero users/no default passwords | `tests/test_token_boundary.py`; `tests/test_cdk_stacks.py` |
| **Change integrity** | RELEASE single-source + consistency gate; tagged releases | `tests/test_release_consistency.py` |
| **21 CFR Part 11 (adopter CSV)** | Electronic-records/signature validation of the sign-off + audit design | adopter validation (out of scope here) |

## How to run an audit dry-run

Pull the tag + evidence; for each row open the cited artifact/test and confirm it demonstrates the
control; walk the threat model as a mock question set; record gaps. Open items are in
`RELEASE-MANIFEST.md` / `PV-PILOT-READINESS-PLAN.md`.

## Not yet proven

No live EP1 evidence yet, no independent audit/pen test, no benefits-program SME SME sign-off, no authoritative program rules coding
or system-of-record gateway. Author-produced on synthetic data.
