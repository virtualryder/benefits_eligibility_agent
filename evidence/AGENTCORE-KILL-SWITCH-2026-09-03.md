# Kill Switch on the AgentCore path — live gate (task 127)

Env `ben-mt5` · us-east-1 · parameter `/ben-mt5-eligibility/kill-switch` · tenants ['pha-a', 'pha-b'] · 109.2 s · **PASS** · time-to-effect at the gateway: **13.9 s**

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

## Run history on this deployment (why the base ledger shows 15 rows)

The gate was run four times on the same `ben-mt5` deployment (one from-zero `cdk deploy --all`, governed-core
1.8.0 hash-pinned, runtime `benefits_runtime_agent-57ZgmU8ZmY`); the ledger is append-only, so every run's
state changes are still there — three engage/release cycles per successful run × 3 runs = seq 0–14.

| Run | Result | What it found |
|---|---|---|
| 1 | 25 checks failed | every controller call was refused at the function-URL front door (HTTP 403 before the function ran). Cause: the managed policies granted only `lambda:InvokeFunctionUrl`; the Lambda dev guide ("Control access to function URLs") requires a same-account identity policy to grant **both** `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction`. Fixed in `cdk/ben_stacks/compute_stack.py` (+ `lambda:InvokedViaFunctionUrl=true` so the grant is usable only through the URL); compute stack redeployed. |
| 2 | 25/29 | engage, containment and SoD all worked. 3 misses were a harness bug (assumed-role session name compared against a different session), 1 was real: the in-flight session ended before engage (the agent gave up on an unresolvable case in ~10 s). Harness fixed: a ten-tool-call prompt keeps the session busy. |
| 3 | 28/29 | in-flight session WAS stopped (runtime log shows the `aegis.kill_switch` line from the model-call hook) but surfaced as a runtime 500: Strands wraps the hook's `KillSwitchEngaged` in `strands.types.exceptions.EventLoopException`. Fixed in `lib/runtime/agent.py` (`_contained()` walks the cause chain and re-reads the switch); runtime relaunched; unit test added. |
| 4 | **29/29 PASS** | this record. |

Nothing was changed in governed-core between runs; the 1.8.0 wheel that passed is the one pinned.

## What happened

- Gateway after engage: tools/list 403 / tools/call 403 — `containment engaged (kill switch /ben-mt5-eligibility/kill-switch): every agent action is refused` (time-to-effect 13.9 s)
- Direct tool invoke: {'FunctionError': 'Unhandled', 'errorType': 'KillSwitchEngaged', 'errorMessage': 'kill switch ENGAGED (/ben-mt5-eligibility/kill-switch): SEV-1 drill: runaway agent suspected'}; Step Functions: {'status': 'FAILED', 'error': 'KillSwitchEngaged', 'states_entered': ['Extract']}
- Runtime fresh invocation: refused=True guardrail_action=KILL_SWITCH; in-flight session: stopped=mid-session guardrail_action=KILL_SWITCH
- SoD: B releases A's engagement → 200; C engages → 200; C releases own → 403; A (engage-only) releases → 403 (IAM); B releases → 200
- **Base ledger `KILL-SWITCH` chain** (platform scope): seq 0 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-responder/ks-a`; seq 1 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-security-lead/ks-b`; seq 2 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-overprivileged/ks-c`; seq 3 kill_switch.disengage DENIED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-overprivileged/ks-c`; seq 4 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-security-lead/ks-b`; seq 5 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-responder/ks-a`; seq 6 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-security-lead/ks-b`; seq 7 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-overprivileged/ks-c`; seq 8 kill_switch.disengage DENIED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-overprivileged/ks-c`; seq 9 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-security-lead/ks-b`; seq 10 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-responder/ks-a`; seq 11 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-security-lead/ks-b`; seq 12 kill_switch.engage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-overprivileged/ks-c`; seq 13 kill_switch.disengage DENIED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-overprivileged/ks-c`; seq 14 kill_switch.disengage COMMITTED by `arn:aws:sts::111122223333:assumed-role/ben-mt5-ks-security-lead/ks-b`
- Tenant-A denials (DENIED `kill_switch.deny`): 7; WORM copies: 7; tenant-B rows in its own ledger: 6

Roles (throwaway, deleted): {'A': 'arn:aws:iam::111122223333:role/ben-mt5-ks-responder', 'B': 'arn:aws:iam::111122223333:role/ben-mt5-ks-security-lead', 'C': 'arn:aws:iam::111122223333:role/ben-mt5-ks-overprivileged'} → cleanup {'A': 'deleted', 'B': 'deleted', 'C': 'deleted'}

## Zero-unexpected-errors sweep (scripts/e2e_regression.py, after run 4)

`AGENTCORE-KILL-SWITCH-2026-09-03-regression.json`: **PASS, 0 unexpected** across 20 log groups, all
executions (3 FAILED at Extract with `KillSwitchEngaged` = expected; run 1's execution, which reached the
24 h sign-off pause because the switch never engaged, was stopped by the harness), the WorkflowFailed
alarm (expected: fires on the deliberate kill-switch failures), no DLQ messages. The run-3 runtime
traceback (`EventLoopException` wrapping `KillSwitchEngaged`, the bug fixed before run 4) is visible in a
60-minute sweep and absent after the relaunch — it is a finding, not a regression.

Account ids redacted to 111122223333 before commit. Raw detail: the `.json` beside this file.
