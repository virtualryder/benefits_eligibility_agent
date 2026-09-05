# EP1 — Live Clean-Account Validation (Public-Benefits Eligibility Assistant)

> ## Re-validation — `ben-val2`, 2026-07-28 (supersedes the EP1 run below)
>
> The full runbook was re-walked end to end as a Solution Architect would, from the hardened code
> (post `e4ee109`), on a clean account. **Every gate passed.**
>
> | Check | Result |
> |---|---|
> | 7/7 CDK stacks (all Gate-B switches) | `CREATE_COMPLETE`, **734s** |
> | AgentCore Gateway + Cedar **ENFORCE** | attached as IaC, no post-deploy shell step |
> | `validate_deployment.py --env val2` | **PASS** (`masking_control`, `guard_genuine`, `forged_ref_denied`, `ingest_pass_by_reference` all PASS) |
> | Happy path | ran every guard, paused at `HumanSignoff` |
> | Due process (*Goldberg v. Kelly*) | adverse-without-notice → **`AdverseNoticeHold`**, SUCCEEDED; never reached a drafted notice or the gate |
> | Strict PII canary | **PASS**, `leaks: {}` (marker `CANARY-8E1FC8E616AD-…`) |
> | Identity | MFA `ON`, **0 users**, admin-create-only `True` |
> | Zero public egress | **0 NAT gateways · 0 internet gateways · 9 VPC endpoints** (measured, not asserted) |
>
> **What this run proves that EP1 did not.** During EP1 the zero-egress security group blocked the
> S3/DynamoDB *gateway* endpoints, and the fix was applied by hand to the live SG because a named SG
> cannot be updated in place. The corrected rule went into `network_stack.py` but had **never been
> exercised from IaC**. This run deployed from code onto a clean account and the data plane worked on
> the first call — `ingest-application` returned a `case_ref` with no timeout. That claim is now
> demonstrated rather than inferred.
>
> **Runbook defects found and fixed in this pass** (the point of the exercise):
> `npx aws-cdk@2` hangs on an install prompt without `--yes`; §3 didn't restate the deploy switches, so
> an SA reproducing EP1 would inherit `retention_profile=pilot` (90-day Object Lock) on a throwaway
> environment; the teardown step didn't say to stop executions parked at the human gate first; and
> nothing warned that the validator and canary buffer output for minutes (I misread it as a hang twice).
>
> Account IDs redacted to `111122223333`. Torn down with a residual sweep.

---


**Environment:** `ben-val1` · **Region:** us-east-1 · **Account:** `111122223333` (redacted) ·
**Date:** 2026-07-27 · **Switches:** `network_mode=private kms=customer-managed identity_mode=pilot
tenant=ben-example-agency retention_profile=sandbox-demo` (all Gate-B switches ON).

This is the live EP1 run behind `v0.1.0-pilot-rc1`. All seven CDK stacks deployed to a clean account,
evidence was captured, and the environment was **torn down** with a residual sweep (below). Account IDs
in ARNs are redacted to `111122223333`.

## Deployment

All 7 stacks reached a `*_COMPLETE` state, including **zero-public-egress** private networking (isolated
subnets + AWS private endpoints only; no NAT/IGW/firewall), customer-managed KMS across data/secrets/logs,
the MFA-enforced identity pool, and the **AgentCore/Gateway/Cedar ENFORCE attachment** (custom resource) —
the highest-risk step — completed cleanly. Deploy time ~12 min (no egress-firewall provisioning).

**Toolchain (pinned so an independent verifier resolves the same synthesis):**
`aws-cdk-lib==2.262.1` · `constructs==10.7.1` · Python 3.12 · CDK CLI `npx aws-cdk@2`.
These are pinned in `cdk/requirements.txt` and enforced by `tests/test_ci_completeness.py`.

*Post-run change (2026-07-27):* `verify_income` was **removed from the deployed Lambda set**. It was
never configured (`SOR_URL` unset), never a Gateway target, and always returned `verified: false` — so it
was an unreachable function holding an AgentCore-Identity OAuth grant. Removing it drops that privilege;
it changes none of the results below.

## Turnkey validator — `scripts/validate_deployment.py --env val1` → **PASS**

```json
{
 "release": "dev", "env": "val1",
 "stacks": "COMPLETE",
 "secret": "PRESENT",
 "masking_control": "PASS",
 "guard_genuine": "PASS",
 "forged_ref_denied": "PASS",
 "ingest_pass_by_reference": "PASS",
 "workflow": "PASS:RUNNING(awaiting human gate)",
 "deployment_status": "PASS"
}
```

- **masking_control** — `mask-pii` masks a probe SSN and mints an authoritative signed `sanitized_ref`.
- **guard_genuine / forged_ref_denied** — the deployed `workflow-guards` VERIFIES a genuine mask-signed
  ref (`ok:true`) and REFUSES a ref with a tampered signature (`ok:false`) — proof-of-masking holds.
- **ingest_pass_by_reference** — raw application content enters only via `ingest-application`; the
  execution starts with an opaque `case-…` ref (R3-2).
- **workflow** — a full pass-by-reference execution ran every deterministic guard and **paused at the
  human sign-off gate** (expected happy-path terminal for an assistant that never self-commits).

## Deterministic controller — live executions

**Happy path** (new application) ran the full guarded controller and paused at the human gate:

```
Extract → GuardExtracted → MaskPii → GuardDeidentified → AssessEligibility → GuardRulesExecuted →
CheckAdverseNotice → DraftNotice → AuditIntent → HumanSignoff   [status: RUNNING — awaiting a qualified
caseworker at waitForTaskToken]
```

**AdverseNoticeHold** (due process, Goldberg v. Kelly) — an **adverse** redetermination lacking the
required advance notice branched at the due-process guard to the terminal hold; it never reached a
drafted notice or the sign-off gate:

```
Extract → … → GuardRulesExecuted → CheckAdverseNotice → AdverseNoticeHold   [status: SUCCEEDED — terminal hold]
```

## Strict PII-telemetry canary — `scripts/pii_canary.py --prefix ben-val1 --execute --strict` → **PASS**

A globally-unique fake-PII marker was run through the deployed pipeline, then every telemetry destination
was swept. **Zero hits** where the marker must not appear:

```json
{ "verdict": "PASS", "leaks": {}, "marker": "CANARY-…-TELEMETRYPROBE", "prefix": "ben-val1" }
```

Swept clean: CloudWatch Logs (`/aws/lambda/ben-val1-*`), X-Ray traces, SQS DLQs, **and Step Functions
execution history** — with R3-2 pass-by-reference in **both directions** (raw application via
`case_ref`; masked case and the drafted determination notice via server-side signed refs) the execution
carries only opaque refs, so even a redaction gap does not surface content in telemetry.

## Identity posture (Gate-B)

Cognito user pool `MfaConfiguration = ON`, software-token MFA, **0 users** (admin-create-only; no
default/self-signup identities). OIDC IdP federation is present as IaC; an enterprise IdP round-trip is a
customer-side Gate-C item.

## Load / exactly-once

Concurrency and exactly-once replay-storm behavior (idempotent finalize, single FINAL# marker) are proven
by the offline suite — **98/98 passing at the time of this run** (control-plane + 24 CDK synthesis).
The suite has grown since: it is **233 tests** today, after post-run hardening and doc-integrity gates
were added. A live prod-scale load test is a customer-side Gate-B exit item.

## Finding fixed during this EP1 run

**Zero-egress SG blocked the AWS gateway endpoints.** On the first probe, `ingest-application` and
`mask-pii` timed out (30s) — the governed Lambdas' security group allowed egress 443 only to the VPC
CIDR, but the **S3/DynamoDB gateway endpoints** route to the AWS service prefix-lists (not the VPC CIDR),
so every DynamoDB write hung. Fix: the Lambda SG egress is 443 to any IPv4 — which, with **no NAT/IGW**,
can still only reach the in-VPC interface endpoints and the S3/DDB gateway prefix-lists (no arbitrary
internet host is routable). The corrected rule is in the IaC (`network_stack.py`) for clean-account
deploys; on this already-running sandbox the rule was authorized on the live SG (the named SG could not
be updated in place) and re-validated → all controls PASS.

## Teardown + residual sweep

`cdk destroy --all -c env=val1` then `validate_deployment.py --env val1 --expect-absent` (0 residual
stacks); provider log groups, the Cognito pool, and the WORM audit table + S3 vault (sandbox-demo
retention, synthetic data only) removed; final sweep = **zero residual**. See the teardown record
appended below. No account IDs appear in this record (redacted to `111122223333`).
