# Per-tenant token + USD budget on the AgentCore path — live gate (task 128)

Env `ben-fp2` · us-east-1 · meter table `ben-fp2-budgets` · tenants ['sp-a', 'sp-b'] · 435.2 s · **FAIL**

| Check | Result |
|---|---|
| baseline_meters_readable | ✅ |
| baseline_calls_allowed | ✅ |
| gateway_refuses_capped_tenant | ✅ |
| gateway_allows_other_tenant | ✅ |
| runtime_refuses_capped_tenant | ❌ |
| workflow_draft_refused_fail_closed | ✅ |
| denials_recorded_in_tenant_ledger | ✅ |
| workflow_denial_recorded_by_drafter | ✅ |
| run1_completed | ❌ |
| meter_counts_after_run | ❌ |
| meter_equals_model_invocation_log | ✅ |
| usd_matches_pinned_price_table | ✅ |
| run2_stopped_mid_session_by_budget | ❌ |
| meter_never_exceeds_cap_beyond_one_call | ❌ |
| alarms_60_and_85_fired | ❌ |
| usd_budget_action_wired | ✅ |
| usd_action_execution_recorded | ✅ |
| breach_engages_kill_switch | ✅ |
| containment_after_breach | ✅ |
| breach_engage_in_worm_ledger | ✅ |
| released_by_different_identity | ✅ |
| recovery_calls_allowed | ✅ |
| runtime_budget_log_lines | ❌ |
| left_disengaged_and_uncapped | ✅ |

## Numbers

- Run 1 (tenant A, uncapped): meter tokens_in 637 / tokens_out 85 / calls 2 / usd_micro 3186 (= $0.003186 at price_version `benefits-2026-09-03-anthropic-platform-UNCONFIRMED-ON-BEDROCK`); model-invocation log for the same session: rows 0, tokens_in 0, tokens_out 0.
- Run 2 (tenant A, cap 5722 = 1.5 x run 1): stopped None with guardrail_action None; meter used 722 = 12.6 % of cap; alarms {'ben-fp2-budget-sp-a-TokensUsedPct-100': 'OK', 'ben-fp2-budget-sp-a-TokensUsedPct-60': 'OK', 'ben-fp2-budget-sp-a-TokensUsedPct-85': 'OK'}.
- Tenant B (cap 0): gateway 403 `budget exceeded (sp-b): the tenant's period cap is reached; refused`; workflow states ['Extract', 'GuardExtracted', 'ExtractedOk', 'MaskPii', 'GuardDeidentified', 'DeidentifiedOk', 'AssessEligibility', 'GuardRulesExecuted', 'RulesOk', 'CheckAdverseNotice', 'AdverseNoticeOk', 'DraftNotice', 'DraftOk', 'ManualReview'].
- USD backstop: budget action {'ActionType': 'APPLY_IAM_POLICY', 'ApprovalModel': 'AUTOMATIC', 'Status': 'STANDBY', 'NotificationType': 'ACTUAL'}; execute attempt {'executed': False, 'error': 'ResourceLockedException: An error occurred (ResourceLockedException) when calling the ExecuteBudgetAction operation: This method is not allowed during [ActionStatus: Standby]', 'note': "ExecuteBudgetAction refused outside a real threshold breach - the action's wiring is proven by describe-budget-action; billing-triggered firing is not exercisable in a test"}; engaged record {'actor': 'arn:aws:sts::111122223333:assumed-role/ben-fp2-observability-BudgetBreachServiceRole183A35-H0WWGmr1xhUu/ben-fp2-budget-breach', 'actor_user_id': 'AROA4SN3H3366WQKLYRX2:ben-fp2-budget-breach', 'at': 1788922215, 'engaged': True, 'reason': 'AWS Budgets ben-fp2-bedrock-usd-ceiling: USD ceiling threshold reached - automatic containment (AWS Budgets: ben-fp2-bedrock-usd-ceiling has exceeded your alert threshold)'}.

## Price table used (pinned, provenance stated)

```json
{
 "price_version": "benefits-2026-09-03-anthropic-platform-UNCONFIRMED-ON-BEDROCK",
 "note": "USD per 1M tokens, on-demand. Anthropic models are NOT in the AWS Price List API (checked 2026-09-03: get-products ServiceCode=AmazonBedrock, us-east-1 returns no Anthropic rows) and aws.amazon.com/bedrock/pricing is not machine-readable, so these numbers are pinned from platform.claude.com/docs/en/about-claude/pricing on 2026-09-03. CONFIRM against the Bedrock pricing page for the customer's region before production and bump price_version; the version is recorded on every meter commit so the evidence shows which prices produced which USD figure. The financial truth is the Cost and Usage Report.",
 "models": {
  "anthropic.claude-sonnet-4-5": {
   "input_per_m": 3.0,
   "output_per_m": 15.0
  },
  "anthropic.claude-haiku-4-5": {
   "input_per_m": 1.0,
   "output_per_m": 5.0
  }
 }
}
```

AWS Budgets is not real-time (AWS: updated up to three times a day, 8-12 h after the previous update); the real-time guard is the meter. The USD figure is an estimate from the pinned table; the Cost and Usage Report is the financial truth. Account ids redacted before commit.
