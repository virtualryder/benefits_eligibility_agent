# Observability Validation — ben-demo — 2026-08-29 (LIVE)

Account 864217980669 · us-east-1 · run by the Aegis working session (dryder CLI identity).
Everything below was executed against the LIVE deployment and observed, not inferred.
Synthetic data only: fictional names, 900-series SSNs (never issued by SSA).

## What was deployed in this wave

| Layer | Change | Result |
|---|---|---|
| Platform `aegis-governance-core` | EvidenceTrail (advanced selectors: management writes + DynamoDB data events ALL tables + platform WORM objects) + X-Ray on gateway | `UPDATE_COMPLETE`, trail `aegis-evidence-trail-pii-dev` IsLogging=true |
| `ben-demo-compute` | X-Ray `Active` on all 12 tool Lambdas; unconditional CFN-managed log groups, 365-day retention | `UPDATE_COMPLETE` (39 resources) |
| `ben-demo-workflow` | State machine `tracingConfiguration.enabled=true`, `loggingConfiguration` level=ALL, includeExecutionData=false → retained log group | `UPDATE_COMPLETE` |
| `ben-demo-observability` | Data-only trail `ben-demo-worm-data-events` on the agent WORM vault (management events NONE) | `UPDATE_COMPLETE`, IsLogging=true |
| Account baseline | Bedrock model invocation logging → `/aegis/bedrock/model-invocations` (365-day retention, delivery role `aegis-bedrock-invocation-logging`) | `textDataDeliveryEnabled=true`, verified via get-model-invocation-logging-configuration |

Deploy note: the pre-existing Lambda auto-created log groups (`/aws/lambda/ben-demo-*`, retention
"Never expire", a few KB of prior demo output) collided with the new CFN-managed groups. With the
owner's approval they were deleted and recreated as managed resources with 1-year retention.

## Config verification (live reads)

- `lambda get-function-configuration` → `TracingConfig.Mode=Active` on mask-pii, core-tools,
  write-audit, workflow-guards, finalize, ingest-application (all governed tools) and the platform
  gateway `aegis-gateway-pii-dev`.
- `stepfunctions describe-state-machine` → `{logging: ALL, includeExecutionData: false, tracing: true}`.
- 13 `/aws/lambda/ben-demo-*` + `/aws/states/ben-demo-determination-workflow` log groups at 365-day retention.
- Both trails: `IsLogging=true`; selectors exactly as coded (platform: 3 advanced selectors;
  agent: S3 object events on the WORM vault only, management excluded).

## End-to-end proof: one action, four independent captures

Case **BEN-SYN-0002** (synthetic, expected ELIGIBLE): ingest → `case-f7ae471a…` →
execution `obs-e2e-BEN-SYN-0002` → all guards passed → DraftNotice → HumanSignoff
(requester `caseworker-demo-1`, approved by `supervisor-demo-2`) → **Committed / SUCCEEDED**,
finalize marker `FINAL#BEN-SYN-0002`, submission `SUB-07E0C17A052F`.

1. **X-Ray**: single trace `1-6a92f3d3-e7f91aecd1ab5a68cab4a821` spanning the state machine and all
   8 invoked tool Lambdas (ingest has its own trace `1-6a92f3ca-…`). The whole governed action is one
   connected trace.
2. **Step Functions execution log** (`/aws/states/ben-demo-determination-workflow`): state-by-state
   events (TaskStateEntered HumanSignoff, waitForTaskToken schedule with 86400s timeout, …) with NO
   case content in any event — includeExecutionData=false matches the R3-2 references-only discipline.
3. **Bedrock model invocation log** (`/aegis/bedrock/model-invocations`): the DraftNotice `Converse`
   call captured with FULL request/response bodies — and the logged prompt reads
   `Applicant [REDACTED:NAME], SSN [REDACTED:SSN] …` because masking runs BEFORE the model.
   Full LLM capture without creating a PII lake, exactly as designed.
4. **Audit ledger + WORM + CloudTrail data events**: hash-chained ledger entries
   (`HEAD#BEN-SYN-0002` seq=1), two WORM objects under `BEN-SYN-0002/` (INTENT 14:59:59Z,
   COMMITTED 15:02:22Z); the agent trail independently recorded
   `PutObject BEN-SYN-0006/… by …WriteAuditServiceRole…` and even the operator's own `ListObjects`;
   the platform trail delivered item-level DynamoDB events — `PutItem ben-demo-pending-approvals`
   by signoff-register, `TransactWriteItems ben-demo-audit-ledger` by write-audit,
   `GetItem` by finalize, plus the operator's console scans. "Who touched the evidence" now has an
   answer independent of the application's own logging.

Second case **BEN-SYN-0006** ran the same path to Committed (approver `supervisor-demo-3`), and a
**forged sanitized_ref** submitted to workflow-guards was refused
(`ok:false — de-identification not proven (no valid sanitized_ref; a boolean is not proof)`) and
surfaced as CloudWatch metric `Benefits/Governance GuardFailed{Guard=deidentified} Sum=1` — the
security-signal path that drives the GuardFailures alarm.

## Gap closure — same-day fixes, all proven live

Every gap below was fixed, redeployed, and re-verified live in the same session.

**G1 — guardrail-pinned drafting (closed).** `core-tools` now carries `GUARDRAIL_ID=h02ji3st2lkd`,
`GUARDRAIL_VERSION=1` + `bedrock:ApplyGuardrail`; a guardrail intervention fails closed (no
`notice_ref`), and a new `DraftOk` workflow choice routes a blocked draft to `ManualReview`. Proven
live: a **prompt-injection application** (`BEN-SYN-ATK-02`) was **intervened**
(`AWS/Bedrock/Guardrails InvocationsIntervened=1`, guardrail version `1`); the drafter returned
`guardrail: BLOCKED` and the case went to `ManualReview` — it never reached an approver. A clean case
still drafts and commits normally.

**G2 — approval-path verification (closed, governed-core 1.5.0).** Deployed the identity-verifying
`approve-signoff` Lambda (Cognito access-token RS256/JWKS, separation-of-duties, single-use), and
`finalize` now verifies the approval path with a `FinalizeOk` fail-closed route. Proven live across
three scenarios:
- raw `send-task-success` bypass (`BEN-G2-0009`, approver `attacker-self`) → **ManualReview, no
  `FINAL#` COMMITTED marker** (refused);
- token-verified approval (`BEN-G2-0010`, `approver-demo-1` ≠ requester) → **Committed**,
  `FINAL#BEN-G2-0010` approver `approver-demo-1`;
- self-approval (identity == requester) → refused (`separation-of-duties`); spoofed approver string
  with no token → refused (`a signed access token is required, not an 'approver' field`).

**G5 hardening (closed).** Gateway AttachmentProvider log group set to 365-day retention; the Bedrock
invocation log group is now **CMK-encrypted** (added the CloudWatch Logs statement to the platform CMK
key policy — the generic ViaService statement never matches Logs; found live, fixed in the platform
stack and associated); stale PENDING approval rows marked `EXPIRED_STALE`/`CONSUMED` (no deletes).

**G3 — ported.** The observability edits + `AUDIT_BUCKET` alias + guardrail/approve-signoff wiring are
now in the PV and financial-aid templates (both `cdk synth` green, core-dependency tests pass), on
governed-core 1.5.0.

**Deferred (optional):** X-Ray Transaction Search destination — classic X-Ray is in use and sufficient
today; enable when console-first trace queries or a SIEM seam are needed.

## Final live config (re-verified)

`core-tools`: TracingConfig=Active, GUARDRAIL_ID=h02ji3st2lkd, GUARDRAIL_VERSION=1 ·
`approve-signoff`: Active, pool us-east-1_HiNG6H9qk, group benefits_caseworker ·
state machine: logging ALL, tracing enabled · `/aegis/bedrock/model-invocations`: 365-day, CMK=true.
