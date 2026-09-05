# CDK — THE supported customer deployment path

*Reviewable, parameterized IaC. Deploy the validated release tag (`v0.5.0-pilot-rc1`), never `main`, per
[`../DEPLOYMENT-GUIDE.md`](../DEPLOYMENT-GUIDE.md). The shell engine (`lib/engine/`) is
**legacy/internal reference only** and must not be used for customer deployments.*

## Stacks (`ben_stacks`, prefix `ben-`)

| Stack | What it is | Controls |
|---|---|---|
| `ben-<env>-data` | append-only audit ledger (PITR, RETAIN), **sanitized-artifacts store** (TTL), **case store** (R3-2, TTL), pending-approvals table, **WORM vault** (Object Lock, retention profile), optional customer-managed KMS | P0-1 store · R3-2 · P0-12 retention (`-c retention_profile=sandbox-demo\|pilot\|production-reference`) · Gate-B B2 |
| `ben-<env>-network` *(optional, `-c network_mode=private`)* | 2-AZ VPC, governed Lambdas in ISOLATED subnets, **ZERO public egress** — no NAT, no IGW, no firewall (benefits has no external dependency); S3/DDB gateway + 7 interface endpoints; 443-only SG | Gate-B B1 (EP1 live-validated 2026-07-27) |
| `ben-<env>-compute` | one Lambda per governed tool, **explicit least-privilege IAM** per function, tamper **Deny** on the audit writer, **exact-ARN outputs**, **single signing secret** (mask_pii sanitized_ref; one trust domain — GA-2 N/A), CMK env+logs under `kms=customer-managed`, `TENANT_ID` pinning | P0-5 · P0-7 · Gate-B B5 |
| `ben-<env>-workflow` | the **deterministic controller** state machine (guarded transitions → ManualReview on unverified evidence; **AdverseNoticeHold** due-process gate on adverse redeterminations) + the human sign-off gate (`waitForTaskToken`, SoD, content-hash binding) | P0-2 · GA-5 |
| `ben-<env>-identity` | federation-ready Cognito pool + client + caseworker group — **zero users, zero passwords**; `-c identity_mode=pilot` = MFA REQUIRED (software token) + threat protection ENFORCED; optional enterprise-OIDC IdP as IaC | P0-6 · Gate-B B3 |
| `ben-<env>-observability` | CloudWatch alarms → SNS ops topic (CMK-encrypted) + operations dashboard; guard-failure security metric. **Deploy AFTER workflow** | GA-6 · R3-3 |
| `ben-<env>-gateway` | **the full AgentCore attachment AS IaC** (GA-1, live-validated): custom-resource provider creates the Cedar policy engine → MCP gateway (CUSTOM_JWT via the identity pool) → SSM discovery param → one target per governed tool (exact ARNs, schemas synthesized from the manifest) → all Cedar policies → **ENFORCE**; stack delete reverses everything | GA-1 |

## Kill Switch (task 127, governed-core 1.8.0)

`ComputeStack` also provisions the deployment's containment control: the SSM parameter
`/ben-<env>-eligibility/kill-switch` (default disengaged), `KILL_SWITCH_PARAMS` + a read-only
`ssm:GetParameter` grant on every governed Lambda (incl. the gateway interceptor), and the controller —
`kill-switch-engage` / `kill-switch-disengage` (one governed-core module, `KILL_SWITCH_MODE`) behind Lambda
function URLs with `AuthType: AWS_IAM`, each with its own managed policy (`ben-<env>-killswitch-engage|disengage`:
`lambda:InvokeFunctionUrl` + `lambda:InvokeFunction`, conditioned on `lambda:FunctionUrlAuthType=AWS_IAM` and
`lambda:InvokedViaFunctionUrl=true`). Only those two function roles hold `ssm:PutParameter` on the flag; the
interceptor gets ledger + vault put grants (mirrored per tenant) for its `DENIED` records; the controller writes
to the base ledger/vault. `-c global_kill_switch=/aegis/kill-switch` adds the platform-wide parameter. Outputs:
`KillSwitchParameter`, `KillSwitchEngageUrl`, `KillSwitchDisengageUrl`, `KillSwitch{Engage,Disengage}PolicyArn`.
Asserted by `tests/test_cdk_stacks.py::test_kill_switch_wired_into_every_lambda_and_the_controller_has_sod`.

## Budget meter + USD ceiling (task 128, governed-core 1.9.0)

`ComputeStack`: `<prefix>-budgets` (DynamoDB, PAY_PER_REQUEST, CMK when present) + `BUDGET_*` env on every
governed Lambda (caps from the manifest `budget:` block via `cdk/app.py::budget_from_manifest`, `-c budget_usd`,
`-c budget_behavior`, the pinned `lib/model_prices.json` inline); grants: interceptor `GetItem` only, drafter
`GetItem` + `UpdateItem` + `cloudwatch:PutMetricData` (namespace-conditioned). `ObservabilityStack`: per-tenant
`Aegis/Budget` alarms at 60/85/100 % → ops topic; with `-c budget_usd`: `AWS::Budgets::Budget` (Amazon Bedrock,
MONTHLY COST) + `AWS::Budgets::BudgetsAction` (`APPLY_IAM_POLICY`, AUTOMATIC, deny `bedrock:*Invoke*/Converse*` on
the drafter role + `-c runtime_role`) + the inline `budget-breach` function subscribed to the topic that engages the
kill switch via its AWS_IAM URL. Asserted by `tests/test_cdk_stacks.py::test_budget_meter_alarms_and_usd_ceiling_are_wired`.

## Deploy

```
git checkout v0.5.0-pilot-rc1            # deploy the validated release, never main
cd cdk && pip install -r requirements.txt
npx aws-cdk@2 deploy --all --require-approval never \
  -c env=pilot -c retention_profile=pilot -c kms=customer-managed \
  -c network_mode=private -c identity_mode=pilot -c tenant=<agency-id>
```

See [`../DEPLOYMENT-GUIDE.md`](../DEPLOYMENT-GUIDE.md) for the full walkthrough and
[`../VALIDATED_RELEASE.md`](../VALIDATED_RELEASE.md) for the captured EP1 evidence.
