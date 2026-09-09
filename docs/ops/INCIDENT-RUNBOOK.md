# Incident runbook — Aegis governed path

*OBS-6. Every alarm this platform deploys appears below. That is enforced, not maintained by
goodwill: `tests/test_incident_runbook_covers_every_alarm.py` fails CI if an alarm exists with no
entry here, so a new alarm cannot ship without a first action.*

Alarm names are prefixed with the deployment prefix (`ben-fp2-`, `ben-t1-`, …). This document uses
the suffix; `*` stands for a tenant id. Confirm the live set with:

```
python tools/observability_census.py
```

---

## Severity tiers

Every alarm belongs to **exactly one** tier, and each tier has its own SNS topic. Subscribe a pager
to P1, a ticket queue to P2, and a mailbox to P3. Subscribing one destination to all three
reproduces the problem tiering exists to solve.

| Composite | Topic | Meaning | Response |
|---|---|---|---|
| `severity-p1` | `<prefix>-ops-p1` | **PAGE.** The governed path is down, or evidence integrity or the perimeter is compromised. | Immediate. Wake someone. |
| `severity-p2` | `<prefix>-ops-p2` | **TICKET.** Degraded — cases still complete, but something is failing, slow, or backing up. | Next business hour. |
| `severity-p3` | `<prefix>-ops-p3` | **ADVISORY.** Spend approaching a ceiling. | No action unless it is a surprise. |

Every constituent alarm *also* publishes to `<prefix>-ops-alarms`, which is where the budget-breach
function listens. Do not unsubscribe that.

---

## P1 — page

### `workflow-failed`
**Means:** a determination workflow execution reached `FAILED`. Cases are not being processed.
**First action:** open the Step Functions execution history for the most recent failure; the failed
state names the control that refused. A guard refusal is *correct behaviour* and should appear as
`guard-failures` too — check that before treating this as a platform fault.
**Escalate if:** more than one execution fails with a non-guard error, or the failures are in
`AuditIntent` (evidence is not being written).
**Recovery confirmed when:** a new case reaches `HumanSignoff` and the alarm returns to OK.

### `mask-errors`
**Means:** the de-identification Lambda is erroring. **Stop and read this:** the platform is
fail-closed, so no un-masked payload reaches a consequential action — the four `mask_before_*` Cedar
forbids hold regardless. The risk is not exposure, it is that nothing is being processed.
**First action:** CloudWatch Logs for the mask function. A `sanitized_ref` signing failure points at
the KMS key or the signing secret, not at the input.
**Escalate if:** errors coincide with `guard-failures` — that combination can mean a forged
reference is being retried.
**Recovery confirmed when:** a case passes `GuardDeidentified`.

### `write-audit-errors`
**Means:** the audit-ledger writer is failing. The record is written *before* the side effect, so
this fails closed — but it means consequential actions are being refused.
**First action:** check the ledger table and the WORM vault for throttling or a KMS denial. Confirm
the hash chain is intact (`verify_chain`) before restarting anything.
**Escalate immediately if:** the chain does not verify. That is an evidence-integrity event, not an
availability event, and it is the one alarm on this page that may require notifying a customer.
**Recovery confirmed when:** a new case writes a row whose `prev_hash` matches the previous tip.

### `guard-failures`
**Means:** a workflow guard refused a transition — a forged or tampered `sanitized_ref`, a spoofed
boolean, or an adverse benefits action lacking its advance notice.
**First action:** identify the case and which guard fired. **A single failure is very often correct
behaviour** — the due-process guard doing its job. Triage per `docs/THREAT-MODEL.md`.
**Escalate if:** repeated failures from the same principal (possible forgery attempt), or any
failure of `GuardDeidentified` (masking bypass attempt).
**Recovery confirmed when:** the rate returns to its baseline. Do not "fix" this by relaxing a guard.

### `bedrock-perimeter-bypass`
**Means:** a principal outside the approved allowlist called Bedrock directly, going around the
governed path. Source is the account capture trail.
**First action:** identify the principal in the capture log. An engineer testing in the console is
the common case and is not an incident — but it must be *confirmed*, not assumed.
**Escalate if:** the principal is an IAM user or root, or is unknown.
**Known limitation, state it plainly:** this is **detective, not preventive**. Prevention needs an
AWS Organization SCP (PERIM-1b), which does not exist. Until it does, this alarm is the only signal.
**Recovery confirmed when:** the caller is identified and either allowlisted (`-c
approved_bedrock_principals`) or stopped.

---

## P2 — ticket

### `workflow-timed-out`
**Means:** an execution exceeded its timeout — usually an approval that sat past the 24h gate.
**First action:** check `approval-backlog` first; if that is also in alarm, this is a staffing or
routing problem, not a platform one.
**Recovery confirmed when:** pending approvals drain.

### `workflow-throttled`
**Means:** Step Functions throttled executions — quota pressure.
**First action:** check concurrent executions against the account quota. Related open item: PERIM-8
(no capacity and quota model exists yet).

### `approval-backlog`
**Means:** more sign-off requests were raised than finalised, for two consecutive hours.
**Why it exists:** without it a stalled due-process gate was invisible until the 24-hour execution
timeout. For a due-process workflow that is the wrong order of magnitude.
**First action:** list executions waiting at `HumanSignoff` and confirm approvers are receiving the
task tokens. **A backlog is not necessarily a fault** — it may be a staffing signal.
**Known limitation:** it is a difference of two invocation counts over a rolling hour, so a genuine
surge of new cases can raise it. Tune `approval_backlog_threshold` to the deployment's volume.
**Recovery confirmed when:** finalisations catch up with requests.

### `assess-errors` · `finalize-errors` · `guards-errors`
**Means:** a governance-critical Lambda is erroring. Fail-closed, so cases stop rather than proceed
incorrectly.
**First action:** CloudWatch Logs for the named function. `finalize-errors` with a
`waitForTaskToken` message usually means an expired or reused sign-off token — that is the
single-use control working, not a bug.

### `mask-latency-p95` · `assess-latency-p95` · `core-latency-p95`
**Means:** p95 duration exceeded the latency objective for 15 minutes. The path is degraded, not
down — cases complete, but a caseworker is waiting.
**First action:** check cold-start rate and any downstream Bedrock throttling. Compare against the
dashboard's duration widget for shape.
**Say this precisely:** the threshold is an objective **we chose**, not an SLO agreed with anyone.
Until this runs under real load it is a starting point — see `docs/ops/OBSERVABILITY-UPLIFT.md`.

### `budget-*-TokensUsedPct-100` · `budget-*-UsdUsedPct-100`
**Means:** a tenant reached 100% of its period budget. Under `cap_behavior=hard` that tenant is now
being **refused** at the runtime, the gateway and the drafter. That is service impact for that
tenant, which is why it is P2 and not advisory.
**First action:** confirm the refusals are the cap and not a fault. Decide deliberately whether to
raise the cap — raising it is a governance decision with a cost consequence, not an ops reflex.
**Recovery confirmed when:** the period rolls over, or the cap is raised through the normal change path.

---

## P3 — advisory

### `budget-*-TokensUsedPct-60` · `budget-*-UsdUsedPct-60`
**Means:** a tenant passed 60% of its period budget. Informational.
**Action:** none, unless the pace is a surprise for this point in the period.

### `budget-*-TokensUsedPct-85` · `budget-*-UsdUsedPct-85`
**Means:** a tenant passed 85%. Refusals begin at 100%.
**Action:** decide *now* whether the cap should be raised, so the decision is not made under pressure
when the tenant is already being refused.

---

## What this runbook does not cover

- **There has been no DR exercise and no documented RTO or RPO** (OBS-8, `R4-15`). If the region or
  the account is lost, there is no rehearsed procedure.
- **No alarm here has been observed firing in a live incident.** They are asserted by tests against
  the synthesized template; proving each tier actually fires is OBS-B1 and needs a live gate.
- **No on-call rotation.** The tier topics exist; nothing is subscribed to them until someone
  subscribes at deploy time.
- **No synthetic canary** (OBS-7), so between real cases a broken governed path is discovered by the
  next caseworker rather than by the platform.
