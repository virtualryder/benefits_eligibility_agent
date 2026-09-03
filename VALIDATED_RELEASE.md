# Validated Release Record

*Single source of truth for the current release tag is the repo-root `RELEASE` file, enforced by
`tests/test_release_consistency.py`. Authoritative counts + limitations: `RELEASE-MANIFEST.md`.*

| Field | Value |
|---|---|
| Tag | `v0.1.2-pilot-rc1` — cut after the live EP1 validation below. Single source of truth: `RELEASE`. |
| Commit SHA | the commit carrying tag `v0.1.2-pilot-rc1` (`git rev-list -n1 v0.1.2-pilot-rc1`) |
| Test count at the tag | **101** offline tests at the moment `v0.1.2-pilot-rc1` was cut — a record of that tag, not a claim about the current tree <!-- count-gate:historical --> |
| Test count on current main | **154 offline tests** (control-plane + CDK synthesis + governance gates + the doc-count gate). Authoritative matrix: [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md). Tag `v0.2.0-pilot-rc1` was cut from this tree and matches this count. |
| Validation date | **2026-07-27** (live EP1, env `ben-val1`, us-east-1) |
| Region | us-east-1 |
| Deployment | AWS CDK `deploy --all`, all Gate-B switches: `network_mode=private kms=customer-managed identity_mode=pilot tenant=ben-example-agency retention_profile=sandbox-demo` |
| Evidence | **captured — [`evidence/EP1-VALIDATION.md`](evidence/EP1-VALIDATION.md)**: 7/7 stacks incl. the AgentCore ENFORCE attachment; `validate_deployment.py` → PASS; happy-path ran the full guarded controller to the human sign-off gate; **AdverseNoticeHold** due-process gate held an adverse redetermination; **strict PII canary PASS (0 leaks across Logs / X-Ray / DLQ / Step Functions history)**; MFA pool ON with 0 users. Then torn down (`destroy --all`) with a residual sweep. Account IDs redacted to `111122223333`. |

## What EP1 proved (live)

The deployed control plane behaves as designed on a clean account with every Gate-B switch on: the
deterministic Step Functions controller runs each guard in order and **cannot** advance a case on
unverified state; de-identification is proven by a mask-signed `sanitized_ref` (a forged ref is refused);
raw application content enters only via `ingest-application` and **only opaque refs — including the
drafted determination notice — cross Step Functions state** (strict PII canary PASS); an **adverse
redetermination without advance notice HOLDS** (Goldberg v. Kelly, enforced by the platform); and every
consequential action pauses at a caseworker sign-off gate. Networking is **zero public egress** (isolated
subnets + AWS private endpoints only; no NAT/IGW/firewall) — benefits has no external dependency.

One finding was fixed during the run (a zero-egress security-group rule blocked the S3/DynamoDB gateway
endpoints; corrected in `network_stack.py`); see `evidence/EP1-VALIDATION.md`.

## Still not live-validated (say these out loud)

Enterprise IdP federation round-trip; a benefits-program SME sign-off on the eligibility rules, processing
clocks, redetermination/overpayment logic, and notice language; independent security testing / pen test;
prod-scale load; system-of-record integration and the notice/appeal workflow. These are Gate-C/D items —
see `BENEFITS-PILOT-READINESS-PLAN.md`. Evidence to date is author-produced on synthetic data.
