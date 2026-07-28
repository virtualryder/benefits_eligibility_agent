# Validated / Not-Validated Matrix

*The single page that says exactly what is proven, how it was proven, and what is not. If any other
document in this repo disagrees with this table, **this table is correct and the other file is a bug.***

Release `v0.1.0-pilot-rc1` · live EP1 run 2026-07-27 (env `ben-val1`, us-east-1) · offline suite **94/94**.

---

## ✅ Validated — live, on AWS, with captured evidence

| Claim | How it was proven | Artifact |
|---|---|---|
| 7-stack CDK deploys clean, incl. **AgentCore Gateway + Cedar in ENFORCE as IaC** | Clean-account deploy, all Gate-B switches | `evidence/EP1-VALIDATION.md` |
| **Masking is proven, not asserted** — a signed `sanitized_ref` is required; a forged/tampered ref is refused | Live probe of `mask-pii` + `workflow-guards` (genuine → `ok:true`, tampered → `ok:false`) | validator `masking_control` / `guard_genuine` / `forged_ref_denied` |
| **Raw application never enters workflow state** (R3-2) | Execution starts from an opaque `case-…` ref via `ingest-application` | validator `ingest_pass_by_reference` |
| **Drafted notice never enters workflow state** (R3-2, both directions) | Drafter returns `notice_ref`; strict canary swept clean | `tests/test_draft_pass_by_reference.py` + canary |
| **Zero PII in telemetry** | Strict canary: 0 marker hits in CloudWatch Logs, X-Ray, DLQs, **Step Functions history** | canary `verdict: PASS, leaks: {}` |
| **Deterministic controller; the model cannot skip a control** | Live run traversed every guard to the human gate | EP1 state list |
| **Due process — adverse action without notice HOLDS** | Live adverse redetermination terminated at `AdverseNoticeHold` | EP1 state list |
| **Human sign-off is structural** | `waitForTaskToken` pause; approver ≠ requester; content-hash bound | EP1 (`RUNNING` at gate) + `tests/test_signoff_identity.py` |
| **Zero public egress** | Isolated subnets + AWS private endpoints; no NAT/IGW/firewall in the deployed template | `tests/test_cdk_stacks.py::test_network_zero_public_egress` + live deploy |
| **MFA identity, no IaC users** | Live pool: `MfaConfiguration=ON`, 0 users | EP1 identity capture |
| **Clean teardown** | `destroy --all` + residual sweep = 0 stacks / 0 residual resources | EP1 teardown record |

## ⚠️ Validated offline only (not yet live at scale)

| Claim | Status |
|---|---|
| Exactly-once finalization + replay-storm idempotency | Offline suite only — **no live load test** |
| Concurrency behavior under peak/renewal surge | **Not tested live** |
| Failure injection (throttling, KMS failure, conditional-write conflict, WORM/ledger split-brain) | **Not tested** |
| Cedar negative-authorization matrix (role/tool denies, self-approval, expired token) | Offline policy tests — **no live captured evidence** |
| Audit-chain tamper evidence | Offline (`tests/test_audit_chain.py`) + IaC Deny asserted at synth |

## ❌ Not validated — do not claim

| Item | Reality |
|---|---|
| **Independent deployment by a third party** | Never done. All evidence is author-produced. **The single biggest credibility gap.** |
| **Independent security test / penetration test** | Never done |
| **Authoritative program eligibility rules** | The engine is a **preliminary FPL / SNAP-style gross-income screen**. No net-income test, no deductions, no per-state resource rules, no benefit allotment. **Not** a SNAP/Medicaid/TANF determination engine |
| **Medicaid / TANF determinations** | Not implemented — state- and coverage-group-specific |
| **Unemployment insurance** | Out of scope entirely — no UI logic exists |
| **Benefits-program SME sign-off** on rules, clocks, notice language | Not obtained (`docs/SME-REVIEW-PACKET.md`) |
| **Enterprise IdP round-trip** | Federation exists as IaC; no agency IdP has been integrated |
| **Tenant-scoped retrieval** | Tenant is signed into artifacts; **per-retrieval subject/tenant/case binding is a follow-on**. Cross-tenant negative tests not run |
| **Multi-account evidence isolation** | Single sandbox account used; workload and evidence not separated |
| **Federal tax information (FTI) handling** | **No FTI processed.** IRS Pub 1075 controls are not implemented; a control mapping is required before any FTI |
| **System-of-record integration** | None (no read, no write-back) |
| **Notice / appeal / fair-hearing workflow** | Not implemented |
| **Real applicant data** | **Never processed.** Synthetic only |
| **Production authorization (StateRAMP / ATO)** | Not started |
| **Measured ROI with a customer** | None. Cost figures are AWS transaction costs only, not a business case |

## Reading the evidence honestly

Everything in the ✅ table was produced by the author on a **disposable sandbox with synthetic data** and
then torn down. It demonstrates that **the governance controls work as designed**. It does **not**
demonstrate correct benefits eligibility, production readiness, or independent verification. The next
proof that matters is an **independent deployment of the tag by another AWS SA or partner**.
