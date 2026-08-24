# Demo deployment — ben-demo, account 111122223333 (us-east-1), 2026-08-24

Deployed from local HEAD (post-hardening commits, ahead of the pilot tag — demo posture, not
customer delivery) with: `-c env=demo -c retention_profile=sandbox-demo -c tenant=demo-agency`
(defaults: network public, identity sandbox, aws-managed keys). Six stacks CREATE_COMPLETE in
402s (`cdk/deploy-demo.log`): data, compute, workflow, identity, observability, gateway —
including a live AgentCore Gateway (`ben-demo-ben-gw-<REDACTED>...amazonaws.com/mcp`) with the
Cedar policy engine `ben_demo_ben_authz` in ENFORCE, dashboard `ben-demo-operations`, and the
Cognito pool `us-east-1_<REDACTED>` (no IaC users, by design).

`scripts/validate_deployment.py --env demo` → **deployment_status: PASS** (`validate-demo.log`):
stacks COMPLETE, secret PRESENT, masking_control PASS, guard_genuine PASS, forged_ref_denied
PASS, ingest_pass_by_reference PASS, workflow PASS:RUNNING(awaiting human gate).

Synthetic-case runs (dataset: `data/synthetic/`, 900-series SSNs, fictional persons):
- **BEN-SYN-0001 (NEW)** — ingest → `case_ref` → controller: Extract → GuardExtracted →
  MaskPii → GuardDeidentified → Assess → GuardRulesExecuted → Draft → INTENT audit →
  **parked RUNNING at HumanSignoff** (waitForTaskToken). Execution `BEN-SYN-0001-demo`.
- **BEN-SYN-ADV-01 (ADVERSE, incomplete intake)** — GuardExtracted failed closed
  ("intake did not yield a household_size") → safe terminal, never reached assessment.
- **BEN-SYN-ADV-02 (ADVERSE, advance_notice_required=false)** — terminated at
  **AdverseNoticeHold** (due-process terminal), exactly per DEPLOYMENT-GUIDE §3.

Platform side (same account): governance core guardrail upgraded the same day — harm-category
+ prompt-attack filters at HIGH, published **Version 1** pinned by the platform gateway
(WOGplatform commit 8185218).

Teardown when done: stop the RUNNING HumanSignoff executions first, then
`cdk destroy --all --force -c env=demo -c retention_profile=sandbox-demo` (§4 of the guide).
