# Independent Verification Result

> **STATUS: UNCLAIMED — no independent verification has been performed.**
>
> This file is a template awaiting a third party. While the status line above reads `UNCLAIMED`, every
> other document in this repository must continue to state that independent verification has **not**
> been done. A CI gate (`tests/test_independent_verification.py`) enforces that, so the claim cannot be
> made on a verifier's behalf.
>
> **Verifier:** replace the status line with `STATUS: VERIFIED` (or `STATUS: FAILED`) and fill in
> everything below. Protocol: [`docs/INDEPENDENT-VERIFICATION.md`](../docs/INDEPENDENT-VERIFICATION.md).

---

## Who / what / when

| Field | Value |
|---|---|
| Verifier (name, org, email) | _______________________ |
| Relationship to the author | _(independent SA / partner / customer — must not be the author)_ |
| Date of run (UTC) | _______________________ |
| Release tag verified | `v0.1.2-pilot-rc1` |
| Commit SHA (from the report) | _______________________ |
| AWS account | **do not record** — the harness stores a truncated hash only |
| Region | _______________________ |
| Attached machine report | `evidence/independent-verification-report.json` ☐ attached |

## Step results

Copy from the harness output. Mark each honestly.

| Step | Expected | Result | Notes |
|---|---|---|---|
| `preflight.on_release_tag` | on the tag, clean tree | ☐ PASS ☐ FAIL | |
| `offline.pytest` | all tests pass | ☐ PASS ☐ FAIL | count observed: ____ |
| `deploy.cdk_all` | 7 stacks `*_COMPLETE` | ☐ PASS ☐ FAIL | wall-clock: ____ |
| `validate.deployment` | `deployment_status: PASS` | ☐ PASS ☐ FAIL | |
| `canary.strict_zero_pii` | `verdict: PASS`, `leaks: {}` | ☐ PASS ☐ FAIL | |
| `happy.reaches_human_gate_and_pauses` | `RUNNING` at `HumanSignoff` | ☐ PASS ☐ FAIL | |
| `adverse.holds_without_advance_notice` | ends at `AdverseNoticeHold`, no draft/sign-off | ☐ PASS ☐ FAIL | |
| `teardown.zero_residual` | `residual_stacks: []` | ☐ PASS ☐ FAIL | |

## Optional adversarial checks

| Check | Expected | Result | Notes |
|---|---|---|---|
| Forged `sanitized_ref` rejected by the guard | `ok:false` | ☐ PASS ☐ FAIL ☐ not run | |
| `deidentified: true` boolean alone refused | refusal | ☐ PASS ☐ FAIL ☐ not run | |
| VPC has no NAT / IGW / firewall | confirmed | ☐ PASS ☐ FAIL ☐ not run | |
| Cognito pool: 0 users, MFA ON | confirmed | ☐ PASS ☐ FAIL ☐ not run | |
| Execution history carries only opaque refs | no applicant text or notice text | ☐ PASS ☐ FAIL ☐ not run | |

## Discrepancies, undocumented fixes, and friction

**This is the most valuable section — please be blunt.** Anything you had to figure out that the docs
didn't tell you is a defect, even if you worked around it.

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Documentation that was wrong, missing, or misleading:

- _______________________________________________

Time actually spent (including troubleshooting): ______

## Verdict

☐ **VERIFIED** — deployed and behaved as documented, using only the written instructions.
☐ **VERIFIED WITH FINDINGS** — worked, but required undocumented steps (listed above).
☐ **FAILED** — did not deploy or did not behave as documented (details above).

**Would you be comfortable if a customer ran this exact procedure themselves?** ☐ Yes ☐ No — why:
_______________________________________________

**Signature / attestation:** _______________________  **Date:** ____________
