# Per-tenant token + USD budget on the AgentCore path — live gate (task 128)

Env `ben-mt6` · us-east-1 · meter table `ben-mt6-budgets` · tenants ['pha-a', 'pha-b'] · 328.1 s · **PASS**

| Check | Result |
|---|---|
| baseline_meters_readable | ✅ |
| baseline_calls_allowed | ✅ |
| gateway_refuses_capped_tenant | ✅ |
| gateway_allows_other_tenant | ✅ |
| runtime_refuses_capped_tenant | ✅ |
| workflow_draft_refused_fail_closed | ✅ |
| denials_recorded_in_tenant_ledger | ✅ |
| workflow_denial_recorded_by_drafter | ✅ |
| run1_completed | ✅ |
| meter_counts_after_run | ✅ |
| meter_equals_model_invocation_log | ✅ |
| usd_matches_pinned_price_table | ✅ |
| run2_stopped_mid_session_by_budget | ✅ |
| meter_never_exceeds_cap_beyond_one_call | ✅ |
| alarms_60_and_85_fired | ✅ |
| usd_budget_action_wired | ✅ |
| usd_action_execution_recorded | ✅ |
| breach_engages_kill_switch | ✅ |
| containment_after_breach | ✅ |
| breach_engage_in_worm_ledger | ✅ |
| released_by_different_identity | ✅ |
| recovery_calls_allowed | ✅ |
| runtime_budget_log_lines | ✅ |
| left_disengaged_and_uncapped | ✅ |

## Run history

| Run | Result | What it found |
|---|---|---|
| 1 | 19/23 | The product held (meter == model log, capped tenant refused at gateway/runtime/workflow, mid-session stop, breach → kill switch). Four harness bugs: the alarm scenario capped the tenant so tightly that the next reservation was refused before any commit could publish a ≥60 % datapoint; the workflow proof read the wrong Step Functions event key; the Budgets-action check looked for a literal function name where CDK generates role names; a CloudWatch filter pattern was malformed. Fixed in `scripts/budget_proof.py`; nothing in governed-core or the CDK changed between runs. |
| 2 | 23/23 PASS | First green run. The 0-unexpected-errors sweep that followed it surfaced finding A below. |
| 3 | 22/24 | Two new checks added. (A) `workflow_denial_recorded_by_drafter`: the drafter's refusal on the workflow hop (Step Functions `DraftNotice`, no interceptor in front) had logged `stored: false` — `AccessDenied` on `GetItem` against the tenant's ledger — because the drafter's role had no ledger grant at all. Fixed in `cdk/ben_stacks/compute_stack.py`: the same append-only grant the interceptor has (`PutItem` + `GetItem` + `TransactWriteItems`, mirrored per tenant; `UpdateItem` / `DeleteItem` verified implicit-deny with `SimulatePrincipalPolicy`); CDK assertion added. The row landed on this run, but the check looked for a case id the drafter never sees (R3-2: refs only) — the check now joins by the execution ARN in the record's correlation block. (B) `meter_equals_model_invocation_log` failed on a run whose agent called `draft_notice`: the meter counted 7 calls, the session-tagged log rows summed 6 — the drafter's server-side `Converse` carried no `requestMetadata`, so its row was not per-tenant filterable. Fixed in `benefits_core.py` (tags `{tenant, component=draft_notice, trace_id, execution_arn, request_id}`, never a case id; unit test) and the harness now sums the log by `requestMetadata.tenant` (Runtime + drafter rows) after the delivery lag settles. |
| 4 | **24/24 PASS** | this record. Product changes between runs 2 and 4: the drafter's ledger grant and its `requestMetadata` tagging — nothing in governed-core 1.9.0. |

Honest limits recorded in the run: `ExecuteBudgetAction` is refused while the action is in STANDBY
(`ResourceLockedException`), so the IAM-attach path is proven by configuration, not execution; AWS Budgets
itself updates "up to three times a day"; the USD figure comes from a price table pinned from Anthropic's
published pricing and marked UNCONFIRMED-ON-BEDROCK until confirmed per region.

## Numbers

- Run 1 (tenant A, uncapped; this run's delta on the meter): tokens_in 7002 / tokens_out 321 / calls 2 / usd_micro 25821 (= $0.025821 at price_version `benefits-2026-09-03-anthropic-platform-UNCONFIRMED-ON-BEDROCK`); model-invocation log for tenant A in the same window: rows 2, tokens_in 7002, tokens_out 321, by component {'runtime': 2} — **equal to the token**.
- Run 2 (tenant A, cap 66445 = used + one reservation + 1000): stopped mid-session with guardrail_action BUDGET (`cap reached: reserving 4000 tokens would exceed the tenant's period cap (tokens 66445, usd_micro 5000000)`); meter used 64957 = 97.8 % of cap; alarms {'ben-mt6-budget-pha-a-TokensUsedPct-100': 'OK', 'ben-mt6-budget-pha-a-TokensUsedPct-60': 'ALARM', 'ben-mt6-budget-pha-a-TokensUsedPct-85': 'ALARM'}.
- Tenant B (cap 0): gateway 403 `budget exceeded (pha-b): the tenant's period cap is reached; refused`; runtime refused (`budget_exceeded`); workflow states ['Extract', 'GuardExtracted', 'ExtractedOk', 'MaskPii', 'GuardDeidentified', 'DeidentifiedOk', 'AssessEligibility', 'GuardRulesExecuted', 'RulesOk', 'CheckAdverseNotice', 'AdverseNoticeOk', 'DraftNotice', 'DraftOk', 'ManualReview']; DENIED `budget.deny` rows in B's ledger: 6, of which by the drafter (joined by execution ARN): 2.
- USD backstop: budget action {'ActionType': 'APPLY_IAM_POLICY', 'ApprovalModel': 'AUTOMATIC', 'Status': 'STANDBY', 'NotificationType': 'ACTUAL'}; execute attempt {'executed': False, 'error': 'ResourceLockedException: An error occurred (ResourceLockedException) when calling the ExecuteBudgetAction operation: This method is not allowed during [ActionStatus: Standby]', 'note': "ExecuteBudgetAction refused outside a real threshold breach - the action's wiring is proven by describe-budget-action; billing-triggered firing is not exercisable in a test"}; engaged record {'actor': 'arn:aws:sts::111122223333:assumed-role/ben-mt6-observability-BudgetBreachServiceRole183A35-i6df3Ez48d0Y/ben-mt6-budget-breach', 'actor_user_id': 'AROA4SN3H3366OB6JAU3U:ben-mt6-budget-breach', 'at': 1788459052, 'engaged': True, 'reason': 'AWS Budgets ben-mt6-bedrock-usd-ceiling: USD ceiling threshold reached - automatic containment (AWS Budgets: ben-mt6-bedrock-usd-ceiling has exceeded your alert threshold)'}.

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
