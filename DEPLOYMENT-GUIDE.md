# Deployment Guide — Public Benefits Intake & Eligibility Screening Assistant (AWS CDK)

*The authoritative step-by-step for the supported deployment path. CDK, at the validated release tag,
never `main`. The shell engine (`lib/engine/`) is a legacy internal reference and must not be used for
customer deployments.*

---

## 0. Supported path

```bash
git checkout v0.1.2-pilot-rc1                 # a validated release tag, never main
cd cdk && pip install -r requirements.txt     # PINNED: aws-cdk-lib==2.262.1, constructs==10.7.1
npx --yes aws-cdk@2 bootstrap aws://<account>/us-east-1     # once per account
```

> **Use `npx --yes`** (or install the CDK CLI globally). Without `--yes`, `npx aws-cdk@2` stops at an
> interactive "Ok to proceed?" install prompt — in a hidden or CI shell that simply hangs with no
> output and no error. Verified on a clean machine, 2026-07-28.

## 1. Deploy (full Gate-B posture)

```bash
npx --yes aws-cdk@2 deploy --all --require-approval never \
  -c env=pilot \
  -c retention_profile=pilot \
  -c kms=customer-managed \
  -c network_mode=private \
  -c identity_mode=pilot \
  -c tenant=<agency-id>
```

Seven stacks deploy: `ben-pilot-{data,network,compute,workflow,identity,observability,gateway}`,
including the AgentCore Gateway + Cedar policies as IaC (no post-deploy shell steps). **No API key or
external data credential is needed** — the eligibility screen runs on public HHS Federal Poverty
Guidelines compiled in as configuration, so there is no runtime external dependency. Switches:

| Switch | Effect |
|---|---|
| `retention_profile=sandbox-demo\|pilot\|production-reference` | WORM Object-Lock mode + days (GOVERNANCE/1d sandbox → COMPLIANCE/7y prod) |
| `kms=customer-managed` | one CMK over tables, secrets, Lambda env, log groups, SNS |
| `network_mode=private` | **ZERO public egress** — governed Lambdas in isolated subnets, AWS private endpoints only; **no NAT, no internet gateway, no egress firewall** (benefits reaches no external API) |
| `identity_mode=pilot` | MFA ON (software token), threat protection ENFORCED, admin-create-only, zero users |
| `tenant=<agency-id>` | HMAC-signed into sanitized artifacts (Gate-B B5) |

## 2. Run a case (execution-input contract)

**Step 1 — ingest (required, R3-2).** Call the **`ben-<env>-ingest-application`** Lambda FIRST with
`{application, case_id}`. It stores the raw application in the encrypted case store and returns an opaque
`case_ref`. Raw applicant content never enters Step Functions state.

**Step 2 — start the controller** (`ben-<env>-determination-workflow`) with:

```json
{ "case_id": "<id>", "requester": "<caseworker-id>", "case_ref": "case-…",
  "redetermination": { "change_type": "NEW" } }
```

`redetermination.change_type` is `NEW` for a new application, or `ADVERSE` / `FAVORABLE` / `NO_CHANGE`
for a re-determination (an `ADVERSE` change must carry `"advance_notice_required": true` to proceed).

The pipeline: extract → **GuardExtracted** → mask PII → **GuardDeidentified** → assess eligibility →
**GuardRulesExecuted** → **CheckAdverseNotice** → (**AdverseNoticeHold** if an adverse change lacks the
required advance notice — terminal, due process) → draft notice → INTENT audit → a **different**
qualified caseworker approves at the `waitForTaskToken` gate → finalize (exactly-once `FINAL#` marker).
Any guard that fails routes to `ManualReview`.

> **Zero-PII note (R3-2, both directions):** the masked case *and* the drafted notice are stored
> server-side and reached only via signed references — neither the raw application nor the notice text
> enters Step Functions state, which is why the strict PII canary passes with 0 leaks.

## 3. Validate the deployment (reproduce EP1)

This exact sequence was re-run on a clean account on 2026-07-28 (env `ben-val2`) — see
[`evidence/EP1-VALIDATION.md`](evidence/EP1-VALIDATION.md). To reproduce it in your own account, deploy
with **`retention_profile=sandbox-demo`**, *not* the `pilot` profile shown in §1:

```bash
npx --yes aws-cdk@2 deploy --all --require-approval never \
  -c env=<env> -c retention_profile=sandbox-demo \
  -c kms=customer-managed -c network_mode=private -c identity_mode=pilot -c tenant=<agency-id>
```

> **Why `sandbox-demo` for a validation run.** `retention_profile=pilot` applies **90-day GOVERNANCE**
> Object Lock to the WORM vault. That is right for a real pilot, but on a throwaway environment you
> intend to destroy the same day it leaves locked objects behind — and the audit writer is deliberately
> DENIED `s3:BypassGovernanceRetention`, by design. `sandbox-demo` is GOVERNANCE / 1 day.

```bash
python scripts/validate_deployment.py --env <env> --region us-east-1   # expect deployment_status: PASS
python scripts/pii_canary.py --prefix ben-<env> --execute --strict     # expect verdict: PASS, leaks: {}
```

> **Both scripts run for minutes and print nothing until they finish — that is not a hang.**
> `validate_deployment.py` polls the Step Functions execution (20 × 6s ≈ 2–3 min); `pii_canary.py
> --strict` intentionally waits 120s for telemetry to settle before sweeping (≈ 3 min). Redirected to a
> file, Python buffers, so the log stays 0 bytes until the process exits. Do not kill them early.

Then exercise both terminals: a **new application** (`change_type: NEW`) should run to `HumanSignoff`
and pause; an **adverse redetermination without advance notice**
(`{"change_type":"ADVERSE","advance_notice_required":false}`) should terminate at `AdverseNoticeHold`.
Tear down and confirm zero residual:

```bash
npx --yes aws-cdk@2 destroy --all --force -c env=<env> -c retention_profile=sandbox-demo
python scripts/validate_deployment.py --env <env> --expect-absent      # expect residual_stacks: []
```

Live prod-scale load and failure-injection testing are **not** covered by this run — they are a
customer-side Gate-B exit item (`BENEFITS-PILOT-READINESS-PLAN.md`).

## 4. Teardown

```bash
# Stop any executions parked at the human sign-off gate FIRST — a RUNNING execution
# blocks deletion of the state machine and the destroy stalls.
aws stepfunctions list-executions --state-machine-arn <arn> --status-filter RUNNING \
  --query "executions[].executionArn" --output text | xargs -n1 -I{} \
  aws stepfunctions stop-execution --execution-arn {} --cause "teardown"

npx --yes aws-cdk@2 destroy --all --force -c env=pilot -c retention_profile=pilot
```

The audit ledger + WORM vault + customer-managed CMK are **RETAIN'd** by design (the CMK alias deletes
with the stack — find the retained key by tag and schedule deletion). VPC-attached Lambda stacks take
~15–30 min to delete (Hyperplane ENI release).

### Completing a zero-residual teardown (validation environments only)

`cdk destroy` leaves the retained resources behind **on purpose** — that is correct for a pilot, where
the audit ledger and WORM vault are the evidence you must keep. On a throwaway validation environment
you also want them gone. `destroy` alone does **not** get you to zero; these are the resources it leaves
and the commands to clear them (verified on `ben-val2`, 2026-07-28):

```bash
E=val2   # your env

aws dynamodb   delete-table    --table-name ben-$E-audit-ledger
aws cognito-idp delete-user-pool --user-pool-id "$(aws cognito-idp list-user-pools --max-results 50 \
                  --query "UserPools[?contains(Name,'ben-$E')].Id" --output text)"
aws logs       delete-log-group --log-group-name "$(aws logs describe-log-groups \
                  --log-group-name-prefix "/aws/lambda/ben-$E-gateway" \
                  --query 'logGroups[0].logGroupName' --output text)"   # AgentCore attachment provider
aws s3api      delete-bucket   --bucket "$(aws s3api list-buckets \
                  --query "Buckets[?contains(Name,'ben-$E-data-wormvault')].Name" --output text)"
```

> The WORM vault deletes cleanly only if it is **empty or past retention**. Under `sandbox-demo`
> (GOVERNANCE / 1 day) a same-day validation vault with no committed evidence is empty and deletes
> immediately. Under `pilot` (90 days) it will **not** — another reason to validate with `sandbox-demo`.

Then confirm zero residual across every resource type, not just stacks:

```bash
python scripts/validate_deployment.py --env $E --expect-absent   # residual_stacks: []
for q in "cloudformation list-stacks" "lambda list-functions" "dynamodb list-tables" \
         "s3api list-buckets" "logs describe-log-groups"; do aws $q | grep -c "ben-$E"; done   # all 0
```

## 4b. EP1 harness (turnkey)

Two scripts make the EP1 run turnkey:

```bash
python scripts/validate_deployment.py --env pilot --region us-east-1   # machine PASS/FAIL verdict
python scripts/pii_canary.py --prefix ben-pilot --execute --strict      # PII telemetry canary (0 hits)
python scripts/validate_deployment.py --env pilot --expect-absent      # after teardown: 0 residual stacks
```

`validate_deployment` probes stacks/secret/masking-control/guards/ingest-pass-by-reference/workflow and
prints a JSON verdict (exit 0 = PASS). `pii_canary --strict` seeds a marked case through ingest → the
workflow and sweeps CloudWatch Logs, X-Ray, DLQs, and Step Functions history for the marker — with R3-2
pass-by-reference it should report **PASS** (0 hits everywhere).

## 5. Offline verification (no AWS)

```bash
python -m pytest tests/ -q                    # 124 pass locally (+1 CI-only gate = 125 tests): control-plane + CDK synthesis + pass-by-ref + canary + doc-integrity gates
python -m pytest tests/test_cdk_stacks.py -q  # 13 CDK assertions (synthesizes all 7 stacks)
```
