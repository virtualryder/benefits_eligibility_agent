# Live gate — governed-core **1.10.0** correctness batch + capture-every-API-call (#168), benefits pack (2026-09-05) — **PASS**

**What this is.** ONE from-zero two-tenant deployment of the benefits pack re-pinned to governed-core
**1.10.0** (the correctness batch: #159 audit fail-closed, #162 approval binding, #164 deepened
PII/PHI), with the new **#168 account-wide capture** turned on, exercised by a live isolation proof, a
live PII-masking check, and the new unified-lineage coverage proof, then torn down to zero residue.

Environment `ben-gate`: 9 CDK stacks
(`-c env=gate -c retention_profile=sandbox-demo -c tenants=sp-a,sp-b -c model_logging=1 -c budget_usd=5 -c capture_all=1 -c capture_retention_days=1`),
two tenants `sp-a` / `sp-b`, Bedrock model-invocation logging on, the account capture trail on. All
account ids redacted to `111122223333`.

## Deploy

All 9 stacks `CREATE_COMPLETE` in ~11.5 min, no rollback: `ben-gate-data`, `ben-gate-sp-a-data`,
`ben-gate-sp-b-data`, `ben-gate-identity`, `ben-gate-compute`, `ben-gate-workflow`,
`ben-gate-gateway` (AgentCore Gateway, Cedar ENFORCE), `ben-gate-observability` (model-logging +
budget), `ben-gate-lineage` (#168 account capture). Lambda bundle staged from the pinned
governed-core **1.10.0** wheel (verified: `pii_detect.py` staged beside the pack's `mask_pii.py`
override, `CORE_VERSION` stamp 1.10.0).

## Verdict

| gate step | result | detail |
|---|---|---|
| 1. Isolation + per-tenant routing (`mt_two_tenant_proof.py`) | **PASS 12/12** | cw-a / cw-b allowed only to their own tenant (9 tools, `mask_pii` executed) and routed only to their own store / ledger / WORM vault; cw-none denied; ingest refuses without a verified token; the workflow hop with the signed pair reached `HumanSignoff` writing INTENT evidence + a pending approval to sp-a only; the same execution without the pair FAILED at `Extract`. `workflow_reached_signoff_with_binding = true` exercises **#162 approval binding** live. |
| 2. Deepened PII/PHI masking, live (**#164**) | **PASS** | the deployed `mask_pii` returned `masked_by = comprehend:DetectPiiEntities+regex-backstop` with `comprehend_entities=5, regex_backstop=1` against **real Amazon Comprehend** — i.e. the shared `pii_detect` (UTF-8 byte-window chunking + Luhn-checked regex backstop) is what runs in the deployed Lambda — while still minting the signed `sanitized_ref` (`authoritative:true`, HMAC-SHA256, stored). Masked output: `Applicant [REDACTED:NAME], SSN [REDACTED:SSN], DOB [REDACTED:DATE_TIME], [REDACTED:ADDRESS] ... [REDACTED:IP_ADDRESS]`. |
| 3. Capture EVERY API call — unified lineage (**#168**) (`lineage_proof.py`) | **PASS — 0 orphans** | one isolated governed case `LIN-5B0383` (sp-a) driven through the full pipeline (Extract → GuardExtracted → MaskPii → GuardDeidentified → AssessEligibility → GuardRulesExecuted → CheckAdverseNotice → DraftNotice → AuditIntent → HumanSignoff). The account trail's captured API calls were joined with the per-Lambda `aegis.call` audit lines, the Step Functions history and the WORM ledger into ONE lineage keyed by execution_arn / trace_id / case_id: **11 CloudTrail Lambda invokes ↔ 11 `aegis.call` audit lines**, per-tool parity all N/N (`workflow_guards 4/4, mask_pii 1/1, assess_eligibility 1/1, benefits_core 1/1, ingest_application 1/1, intake_application 1/1, signoff_register 1/1, write_audit 1/1`), 17 Step Functions events, 1 WORM record — **covered=true, orphans=[]** (no invoked-but-unaudited, no audited-but-uninvoked, no uncorrelated node). |
| 4. WORM custody of the capture (**#168**) | **PASS** | the joined lineage + coverage verdict were written to the capture bucket `ben-gate-capture-worm-111122223333` (S3 **Object Lock**, GOVERNANCE, RetainUntil +1 day). Deleting the locked object version **without** `s3:BypassGovernanceRetention` was **DENIED** — the capture is immutable. The account trail itself has log-file validation on (digest chain). |

Raw records (in `.build/`): `gate-deploy.log`, `gate-mt2.json` (isolation, 12/12 + the live mask_pii
output), `lineage-case.json` (the isolated case), `lineage-proof-LIN-5B0383.md` (the joined lineage +
coverage verdict).

## Scope / honesty

- The **runtime-dependent** gate proofs (full-transparency-through-the-Runtime, kill-switch mid-session,
  per-tenant budget mid-session) were **not** re-run in this gate: they were proven at governed-core
  1.9.0 in the prior benefits/EDU gates, and the 1.10.0 delta is the correctness batch — #159/#162/#164
  — which is covered by the offline suite (governed-core 71 + benefits 179) plus the live #162/#164
  evidence above. Re-running them requires launching the Strands AgentCore Runtime container.
- The account capture trail records account-wide **management events (ALL)** + **S3 / Lambda data
  events**; DynamoDB and Bedrock data-plane calls are covered by the dedicated hash-chained WORM ledger
  and the Bedrock model-invocation log, which the lineage proof joins alongside the trail.
- `pii_detect` propagation was applied to the **benefits (lead) pack** this session; the other four
  packs adopt it with their 1.10.0 re-pin in the batched task #176.

## Teardown

`cdk destroy --all` (env `gate`) removed all 9 stacks. The #168 capture bucket
`ben-gate-capture-worm-111122223333` is S3 **Object Lock** (GOVERNANCE), so its 101 locked
versions were emptied with `s3:BypassGovernanceRetention` and the bucket deleted, then the
`ben-gate-lineage` stack deleted. `scripts/cleanup_retained.py --prefix ben-gate` then swept the
RETAIN-policy audit resources (the base + two tenant audit-ledger tables, the base + two tenant WORM
vaults with governance bypass, the observability WORM data-events bucket, the Cognito user pool) and
re-swept AgentCore policy engines/gateways by prefix.

The account's Bedrock **model-invocation logging configuration was restored** to its exact prior
state (`/aegis/bedrock/model-invocations`, role `aegis-bedrock-invocation-logging`, text+video
delivery) and verified — the ObservabilityStack's delete had disabled it (it is an account
singleton).

**Zero residue verified via the AWS API**: no `ben-gate` CloudFormation stacks, S3 buckets, DynamoDB
tables, Lambda functions, CloudTrail trails, or Cognito user pools remain; model-logging is back to
the account's own log group. Residual by design: none.
