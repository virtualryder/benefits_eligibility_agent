# Deployment Guide — Public Benefits Intake & Eligibility Screening Assistant (AWS CDK)

*The authoritative step-by-step for the supported deployment path. CDK, at the validated release tag,
never `main`. The shell engine (`lib/engine/`) is a legacy internal reference and must not be used for
customer deployments.*

---

## 0. Supported path

```bash
git checkout v0.4.0-pilot-rc1                 # a validated release tag, never main
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
| `guardrail_id=<id>` `guardrail_version=<v>` | Arms the platform Bedrock guardrail on the drafter (`draft_notice`). Every generation is guardrail-assessed; an intervention fails closed (no `notice_ref`) and the case routes to `ManualReview`. Omit → drafting is unguarded (sandbox only). |
| `approvals_client_id=<cognito-client-id>` | Client id the `approve-signoff` Lambda verifies caseworker access tokens against. The identity pool/reviewer group are wired from the identity stack automatically; this is only needed when approvals use a different app client than the gateway (e.g. a CLI/native client). |

### 1b. Hybrid multi-tenant + full transparency switches (2026-09-02)

| Switch | Effect |
|---|---|
| `tenants=<a>,<b>,…` | **Hybrid multi-tenant**: one shared control plane (identity, compute, workflow, gateway + Cedar engine) and ONE physically separate data stack per tenant (`ben-<env>-<tenant>-data`: tenant-scoped tables + the tenant's own Object-Lock vault `<prefix>-<tenant>-worm-<account>`). Creates a `tenant_<id>` Cognito group per tenant, deploys the gateway REQUEST interceptor (`tenant-interceptor`), attaches `require_tenant` (Cedar), sets `MULTITENANT=1` + `WORM_BUCKET_TEMPLATE` on the governed Lambdas, threads the signed tenant pair through the workflow, and mirrors least-privilege grants onto `<prefix>-*-<logical>`. Mutually exclusive in spirit with `tenant=` (silo). |
| `model_logging=1` | **Bedrock model-invocation logging** for the account+region (an account-level singleton — it REPLACES any existing configuration, hence opt-in): CloudWatch group `/aws/bedrock/modelinvocations/<prefix>` + S3 large-data bucket + the `bedrock.amazonaws.com` role; removed on teardown. Also delivers the AgentCore gateway's vended request logs to `/aws/vendedlogs/bedrock-agentcore/gateway/<prefix>`. |

Multi-tenant contracts: the tenant is **derived, never requested** (verified identity → interceptor →
HMAC-signed `__aegis_tenant`/`__aegis_tenant_sig` → every Lambda verifies before routing); `ingest`
(direct IAM invocation) derives it from a verified caseworker access token (`access_token` in the
payload) and returns `tenant_binding`, which the workflow starter MUST splat into the execution input
(`{case_id, requester, case_ref, redetermination, **tenant_binding}`) — an execution without it fails
at the first state. Proofs: `scripts/mt_two_tenant_proof.py` (cross-tenant deny, per-tenant routing,
audit/WORM/approvals routing on both hops) and `scripts/obs_two_tenant_proof.py` + `scripts/trace_case.py`
(one per-case timeline across runtime spans, gateway rows, Lambda `aegis.call` lines, model-invocation
rows and the WORM record). Evidence: `evidence/AGENTCORE-MULTITENANT-*.md`, `evidence/AGENTCORE-OBSERVABILITY-2026-09-02.md`.

### 1c. Kill Switch — one-command containment (task 127, governed-core ≥ 1.8.0)

Every deployment gets ONE SSM Parameter Store flag, `/ben-<env>-eligibility/kill-switch`, that every
component on the agent path reads **first** — before tenancy, before Cedar, before masking, before the
human sign-off gate. Containment precedes evaluation. When engaged:

| Component | What happens | Evidence it leaves |
|---|---|---|
| Gateway REQUEST interceptor | `tools/list` + `tools/call` → 403 JSON-RPC error (`transformedGatewayResponse`; the target Lambda is never invoked) | `DENIED kill_switch.deny` record + WORM object in the **acting tenant's** ledger / vault; `aegis.kill_switch` log line |
| Every governed tool Lambda | `telemetry.instrument` raises `KillSwitchEngaged` before the handler runs (workflow hop, direct invoke) | a Step Functions execution FAILS at its next state with error `KillSwitchEngaged`; `aegis.call` line `denied:kill_switch` |
| AgentCore Runtime | a new invocation is refused before the tenant is derived or the gateway is contacted; a **running** session stops at its next model call (`stopped: mid-session`) | `aegis.kill_switch` line in the runtime log group; structured refusal (`guardrail_action: KILL_SWITCH`) |

Rules (mirroring the platform reference gateway): **fail-closed** — an unreadable or malformed
parameter counts as engaged; **15 s TTL cache** per execution environment, so time-to-effect ≤ 15 s and
Parameter Store stays far under its 40 TPS default (the AWS-documented caching pattern for Lambda reads);
**many-to-one** — `-c global_kill_switch=/aegis/kill-switch` makes the pack honour the platform-wide
parameter too (engaged if either is engaged).

**Engage / disengage** are two Lambda **function URLs with `AuthType: AWS_IAM`** (stack outputs
`KillSwitchEngageUrl` / `KillSwitchDisengageUrl`), one managed policy each
(`ben-<env>-killswitch-engage` / `-disengage`, `lambda:InvokeFunctionUrl` on one function only) — assign
them to **different** roles. The actor recorded in the parameter and in the WORM ledger is the IAM-verified
caller (`requestContext.authorizer.iam.userArn`), never a body field, and the controller refuses to let the
engaging identity (same ARN or same assumed role) release its own engagement — the refusal is itself a
`DENIED` ledger record. Nothing else in the app holds `ssm:PutParameter` on the flag.

```bash
# engage (SigV4-signed POST; service name "lambda"). Any SigV4 client works; e.g. awscurl:
awscurl --service lambda --region us-east-1 -X POST -d '{"reason":"SEV-1: runaway agent"}' "$KILL_SWITCH_ENGAGE_URL"
# status
awscurl --service lambda --region us-east-1 "$KILL_SWITCH_ENGAGE_URL"
# release — a DIFFERENT identity, via the disengage URL
awscurl --service lambda --region us-east-1 -X POST -d '{"reason":"security lead sign-off"}' "$KILL_SWITCH_DISENGAGE_URL"
```

Live gate: `scripts/kill_switch_proof.py` (21 checks: IAM SoD, code SoD, IAM-verified actor,
interceptor time-to-effect, tool Lambda + workflow refusal, runtime fresh + in-flight refusal, base-ledger
`KILL-SWITCH` chain, per-tenant denials, recovery, log lines). Evidence:
`evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md`. Runbook: platform `docs/ops/KILL-SWITCH.md`.

### 1d. Per-tenant token budget + USD ceiling (task 128, governed-core ≥ 1.9.0)

One DynamoDB meter per deployment (`ben-<env>-budgets`, key `<tenant>#<YYYY-MM>`). Before **every** model call
the Runtime makes one conditional reservation against the tenant's cap and after it commits the real Converse
`usage`; the gateway interceptor refuses a tenant at/over its cap on every `tools/call` (403 + DENIED WORM
record); the drafter's own Bedrock call is metered the same way (a refusal routes the workflow to
`ManualReview` and lands a DENIED record joined by the execution ARN — the drafter carries the same append-only
ledger grant as the interceptor, never Update/Delete; its `Converse` is tagged with `requestMetadata`
{tenant, component, trace/execution ids} so the model log reconciles per tenant). Hard caps fail closed (an
unreadable meter denies); soft caps flag and alert only.

| Switch / knob | Effect |
|---|---|
| manifest `budget: monthly_token_cap / cap_behavior` | the deployment default cap (B5 — one place to set the number); read by the CDK and the Runtime launch |
| `-c budget_usd=<dollars>` | per-tenant USD cap (`cap_usd_micro`, from the pinned price table) **and** the AWS Budgets monthly ceiling on Amazon Bedrock with an `APPLY_IAM_POLICY` action (deny `bedrock:InvokeModel*` on the drafter + `-c runtime_role=` roles) and a notification whose subscriber (`ben-<env>-budget-breach`) engages the kill switch |
| `-c budget_behavior=soft` | flag-only for the whole deployment |
| `PutItem <tenant>#<YYYY-MM> {cap_tokens \| cap_usd_micro \| behavior}` | per-tenant override with no redeploy; `cap_tokens 0` switches a tenant off |
| `lib/model_prices.json` | the pinned price table; its `price_version` is recorded on every commit (confirm against the Bedrock pricing page per region before production — see the file's note) |

Alarms: `Aegis/Budget` `TokensUsedPct` / `UsdUsedPct` per tenant → 60 / 85 / 100 % on the ops topic. AWS Budgets is
**not** real-time (AWS: updated up to three times a day, 8–12 h after the previous update) — it is the backstop;
the meter is the real-time guard. Live gate: `scripts/budget_proof.py` (24 checks) —
`evidence/AGENTCORE-BUDGET-2026-09-03.md`. Design + honest status: platform `docs/TOKEN-BUDGETS-AND-COST-CEILINGS.md`.

### Observability & governance evidence (verify the claims)

Deployed as IaC by the stacks above — no post-deploy instrumentation:

- **X-Ray** — `Tracing.ACTIVE` on every governed tool Lambda and the gateway; one execution is a single connected trace (ingest → guards → mask → assess → draft → audit → finalize).
- **Step Functions execution logging** — `loggingConfiguration` level `ALL`, `includeExecutionData=false` (R3-2: references only, no case content), 1-year CMK-when-present log group at `/aws/states/<prefix>-determination-workflow`.
- **Lambda logs** — unconditional 1-year retention on every `/aws/lambda/<prefix>-*` group (decoupled from the KMS switch).
- **Model prompts & responses** — account-level **Bedrock model-invocation logging** (`-c model_logging=1`, or the platform runbook one-time step) captures full request/response bodies, tagged per tenant / session / case via `requestMetadata`; because masking runs *before* the model, the logged prompt is de-identified — `scripts/trace_case.py` measures `masked_before_model` on every row.
- **Per-tenant budget (task 128, governed-core ≥ 1.9.0)** — §1d: reserve-before / commit-after on every model call, meter == model-invocation log, cap refusals at runtime / gateway / drafter, 60/85/100 % alarms, AWS Budgets USD backstop → kill switch.
- **Kill Switch (task 127, governed-core ≥ 1.8.0)** — §1c: engaged ⇒ interceptor 403 + DENIED WORM record, tool Lambdas + runtime refuse; engage/disengage via AWS_IAM function URLs with IAM-verified actors and separation of duties.
- **Correlation (phase 110, governed-core ≥ 1.7.1)** — every runtime span, gateway row, tool-Lambda `aegis.call` line, model-invocation row and WORM record carries the same tenant · session · trace · request · case keys; `scripts/trace_case.py` joins them into one auditor timeline.
- **Data-source touches** — the platform **evidence trail** records management-write events + DynamoDB data events for all tables; each agent adds a **data-only CloudTrail** on its own WORM vault (`<prefix>-worm-data-events`). Answers "who touched the evidence" independent of the app's own logging.
- **Approval integrity (governed-core ≥ 1.5.0)** — approvals go through `approve-signoff` (Cognito access-token verified, separation-of-duties, single-use). `finalize` verifies the **approval path**: a task token released around that Lambda (e.g. a raw `send-task-success`) is refused fail-closed to `ManualReview` and recorded `DENIED` — never `COMMITTED`.

One end-to-end run produces four independent captures of the same action (X-Ray trace, SFN log stream, de-identified invocation-log entry, ledger + WORM object with a CloudTrail data event). See `evidence/OBSERVABILITY-VALIDATION-2026-08-29.md` for a live run.

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
python -m pytest tests/ -q                    # 233 pass locally (+1 CI-only gate = 234 tests): control-plane + CDK synthesis + pass-by-ref + canary + doc-integrity gates
python -m pytest tests/test_cdk_stacks.py -q  # 25 CDK assertions (synthesizes all 7 stacks + the multi-tenant variants)
```
