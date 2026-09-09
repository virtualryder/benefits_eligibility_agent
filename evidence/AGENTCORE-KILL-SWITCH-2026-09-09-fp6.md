# Kill Switch on the AgentCore path — live gate (task 127)

Env `ben-fp6` · us-east-1 · parameter `/ben-fp6-eligibility/kill-switch` · tenants ['sp-a', 'sp-b'] · 98.4 s · **PASS** · time-to-effect at the gateway: **19.3 s**

| Check | Result |
|---|---|
| baseline_disengaged | ✅ |
| baseline_calls_allowed | ✅ |
| iam_sod_disengage_only_cannot_engage | ✅ |
| engage_ok | ✅ |
| actor_is_iam_verified_not_body | ✅ |
| engage_audited_worm | ✅ |
| interceptor_denies_list_and_call | ✅ |
| time_to_effect_within_2x_ttl | ✅ |
| tool_lambda_refuses_direct_invoke | ✅ |
| workflow_fails_at_first_state_with_kill_switch | ✅ |
| runtime_refuses_new_invocation | ✅ |
| runtime_stops_in_flight_session | ✅ |
| disengage_by_second_identity | ✅ |
| code_sod_same_identity_refused | ✅ |
| code_sod_refusal_audited | ✅ |
| iam_sod_engage_only_cannot_disengage | ✅ |
| final_release_ok | ✅ |
| recovery_calls_allowed | ✅ |
| recovery_runtime_answers | ✅ |
| base_ledger_state_changes | ✅ |
| base_ledger_chained | ✅ |
| base_worm_copies | ✅ |
| denials_in_acting_tenant_ledger | ✅ |
| denials_of_other_tenant_in_its_own_ledger | ✅ |
| no_denials_in_base_ledger | ✅ |
| denial_worm_copies | ✅ |
| interceptor_log_lines | ✅ |
| runtime_log_lines | ✅ |
| left_disengaged | ✅ |

## What happened

- Gateway after engage: tools/list 403 / tools/call 403 — `containment engaged (kill switch /ben-fp6-eligibility/kill-switch): every agent action is refused` (time-to-effect 19.3 s)
- Direct tool invoke: {'FunctionError': 'Unhandled', 'errorType': 'KillSwitchEngaged', 'errorMessage': 'kill switch ENGAGED (/ben-fp6-eligibility/kill-switch): SEV-1 drill: runaway agent suspected'}; Step Functions: {'status': 'FAILED', 'error': 'KillSwitchEngaged', 'states_entered': ['Extract']}
- Runtime fresh invocation: refused=True guardrail_action=KILL_SWITCH; in-flight session: stopped=mid-session guardrail_action=KILL_SWITCH
- SoD: B releases A's engagement → 200; C engages → 200; C releases own → 403; A (engage-only) releases → 403 (IAM); B releases → 200
- **Base ledger `KILL-SWITCH` chain** (platform scope): seq 0 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-fp6-ks-responder/ks-a`; seq 1 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-fp6-ks-security-lead/ks-b`; seq 2 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-fp6-ks-overprivileged/ks-c`; seq 3 kill_switch.disengage DENIED by `arn:aws:sts::111122223333:assumed-role/ben-fp6-ks-overprivileged/ks-c`; seq 4 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-fp6-ks-security-lead/ks-b`
- Tenant-A denials (DENIED `kill_switch.deny`): 3; WORM copies: 3; tenant-B rows in its own ledger: 2

Roles (throwaway, deleted): {'A': 'arn:aws:iam::111122223333:role/ben-fp6-ks-responder', 'B': 'arn:aws:iam::111122223333:role/ben-fp6-ks-security-lead', 'C': 'arn:aws:iam::111122223333:role/ben-fp6-ks-overprivileged'} → cleanup {'A': 'deleted', 'B': 'deleted', 'C': 'deleted'}

Account ids redacted to 111122223333 before commit. Raw detail: the `.json` beside this file.
