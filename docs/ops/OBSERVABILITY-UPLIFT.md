# Observability uplift — scope, baseline and acceptance criteria

*Opened 2026-09-09. Baseline measured, not recalled: `python tools/observability_census.py`.*

---

## 0. The correction this document starts from

The partner brief, the partner deck and a verbal assessment on 2026-09-09 all said this platform
deploys **"three alarms"** and called observability "the thinnest part of the platform."

**That was wrong.** The number came from counting `cw.Alarm(` *call sites* in
`cdk/ben_stacks/observability_stack.py`. Two of the three are inside loops. The synthesized
CloudFormation template carries **22 alarms**.

| | Claimed | Measured |
|---|---|---|
| Alarms | 3 | **22** |
| Metric filters | 1 | **2** |
| Dashboards / widgets | 1 / 6 | 1 / 6 |

The defect is the method, not the arithmetic: counting the source instead of the artifact. It is the
same shape as **L60** (a negation control whose mutation never landed, read as a pass) and **L67** (a
survey loop that measured the previous repository while carrying the next one's label). Third
occurrence in one remediation.

**Standing rule, extended again:** a quantitative claim about deployed infrastructure must be
produced by a script that reads the synthesized template or the live account — never by reading the
generating code. `tools/observability_census.py` is that script for this claim, and
`--assert-baseline` fails if the numbers drift from what the partner documents quote.

## 1. Measured baseline (2026-09-09)

Two tenants, budget on, lineage wired:

```
alarms                  22   (13 named, 9 logical-id only)
composite alarms         0
alarms with an action   22
metric filters           2
dashboards / widgets     1 / 6
sns topics               1
latency alarmed        False
```

The 22 break down as: **12** per-tenant budget alarms (2 tenants × `TokensUsedPct` + `UsdUsedPct`
× 60 / 85 / 100 %), **3** workflow alarms (failed, timed-out, throttled), **5** per-function Lambda
error alarms (assess, finalize, guards, mask, write-audit), **1** `Benefits/Governance GuardFailed`,
and **1** `bedrock-perimeter-bypass`. Every one has an SNS action.

**So alarm coverage of the governed path is reasonable.** The honest gap is not quantity. It is that
the alarms are not *operable*: they cannot all be named, they are not tiered, they do not cover
latency or approval backlog, and nothing tells an operator what to do when one fires.

## 2. What is actually wrong

| ID | Finding | Why it matters at 3am |
|---|---|---|
| **OBS-1** | **9 of 22 alarms have no `AlarmName`** — they exist only as CloudFormation logical IDs (`WorkflowFailedEDBEFEBB`). | A runbook cannot reference them and an operator cannot find them in the console. Invisible from the source, which is why it survived this long. |
| **OBS-2** | **Zero composite alarms; one SNS topic.** | No severity tiering. A tenant reaching 60 % of budget pages exactly as loudly as the determination workflow failing. Operators learn to ignore the topic. |
| **OBS-3** | **Latency is charted and never alarmed.** `Duration p95` is a dashboard widget; no alarm reads it. | This is what an absent SLO looks like in practice. Degradation is visible only to someone already looking at the dashboard. |
| **OBS-4** | **No approval-backlog signal.** A stalled human sign-off is detected only when the execution times out. | For a due-process workflow the detection window is a day. It should be minutes. |
| **OBS-5** | **One dashboard, not per-tenant.** Budget *alarms* are per-tenant; the operational view is not. | In a multi-tenant deployment you cannot answer "is tenant A healthy?" without reading raw metrics. |
| **OBS-6** | **No incident-response runbook.** | An alarm with no documented first action is a notification, not a control. |
| **OBS-7** | **No synthetic canary.** Nothing exercises the governed path between real cases. | A broken governed path is discovered by the next caseworker, not by the platform. |
| **OBS-8** | **No DR exercise, no documented RTO/RPO.** | Named in `R4-15` and unaddressed. Out of scope for the pre-pilot tranche; recorded so it is not lost. |

## 3. Scope and acceptance criteria

Tranche A is the pre-pilot work. Tranche B needs a live deployment. Tranche C needs a customer.

### Tranche A — code and tests, no deployment required

| ID | Deliverable | Acceptance criterion |
|---|---|---|
| OBS-1 | Every alarm carries a deterministic, prefix-scoped `AlarmName`. | `observability_census.py` reports `unnamed_alarms: 0`, and a test asserts it. Names are stable across synths (no logical-ID suffixes). |
| OBS-2 | Three severity tiers as composite alarms, each with its own SNS topic: **P1** governed path down or perimeter bypassed; **P2** degraded; **P3** advisory. | A test asserts three composite alarms exist, that each names its constituent alarms, and that P1/P2/P3 publish to *different* topics. A budget-60 % alarm must not reach the P1 topic. |
| OBS-3 | Latency SLO alarms on the governed path (p95 duration per governed function, and end-to-end workflow duration). | A test asserts at least one alarm reads `Duration` with an `ExtendedStatistic` of `p95`, and that it is wired to the P2 tier. `census.latency_alarmed` becomes `True`. |
| OBS-4 | Approval-backlog alarm — sign-off requests raised but not resolved within the SLO window. | A test asserts an alarm exists on the pending-approval signal with a threshold well below the 24 h execution timeout. |
| OBS-5 | Per-tenant operational dashboard, one per configured tenant, plus the existing portfolio view. | A test asserts `dashboards == 1 + len(tenants)` and that each tenant dashboard filters on its own `Tenant` dimension. |
| OBS-6 | `docs/ops/INCIDENT-RUNBOOK.md` — every alarm name mapped to: what it means, first action, escalation, and how to confirm recovery. | A test asserts **every** alarm name emitted by the census appears in the runbook. This is the control that keeps the runbook from rotting: a new alarm without a runbook entry fails CI. |

### Tranche B — needs a live deployment

| ID | Deliverable | Acceptance criterion |
|---|---|---|
| OBS-7 | Synthetic canary exercising the governed path on a schedule, alarmed when it fails. | Runs in a from-zero gate; the canary's own failure raises the P1 tier. |
| OBS-B1 | Alarms proven to fire, not merely to exist. | A gate check that deliberately breaks one thing per tier and asserts the right tier fired — negation-tested, per the L60 rule. |

### Tranche C — needs a customer or a partner account

| ID | Deliverable |
|---|---|
| OBS-8 | DR exercise with documented RTO/RPO. |
| — | On-call integration against a real rotation (PagerDuty/Opsgenie), rather than an SNS topic subscribed at deploy time. |

## 4. What this uplift will and will not let us claim

**Will:** that the governed path is monitored with tiered, named, runbook-backed alarms covering
availability, error rate, latency, due-process backlog, spend and perimeter bypass — and that the
alarm set cannot drift from its runbook without failing CI.

**Will not (CONN-1 specifically):** see section 5 — the governed system-of-record connector is
**unproven** and may not be cited in any partner document.

**Will not:** any claim about operating this in production. There is still no DR exercise, no real
on-call rotation, no SLO *agreement* with anyone, and no evidence from a system carrying real load.
An SLO alarm is not an SLO; it is a threshold we chose. Say it that way.

## 5. CONN-1 (governed system-of-record connector) — OPEN, NOT PROVEN

**Status as of 2026-09-09: unproven. It may not be cited in any partner document.**

The `ben-fp4` live run put 14 platform checks through from zero — deploy across nine stacks, runtime
READY, G111, kill switch, budget, guardrail 19/19, `LIN_zero_orphans` 11/11, E2E with zero
unexpected errors — and `CONN_deploy` **failed**, correctly.

Root cause: `deploy_connector.sh` referenced `$GW_ID`, but `spine-state.env` has only ever carried
`GW_ARN` and `GW_URL`. Under `set -u` that is a fatal unbound variable, so the deploy aborted at the
gateway-target step on every run it has ever had. `CONN_governed_sor_proof` has **never completed on
any commit** — the earlier `ben-fp3` "PASS" was the check passing, not the connector.

Three further defects surfaced in the same run, all now fixed and recorded as **L70**:

- `conn_artifacts()` returned unmeasured `False`s without querying AWS, so "I never looked" was
  indistinguishable from "nothing exists". It now probes regardless and records `None` for
  unmeasured, and `conn_ok` tests `is True`.
- The teardown guard keyed on one of those unmeasured `False`s and **skipped cleanup over eight live
  resources**, including a credential provider holding an M2M client secret. It now fires whenever
  the deploy was attempted.
- `destroy_connector.sh` reported `absent` for live resources and printed `CONNECTOR TEARDOWN:
  CLEAN`, because every probe is an `aws` CLI call ending in `2>/dev/null` and `aws` was not on
  PATH. It now refuses to run without the CLI and prints `UNVERIFIED`.

A new `teardown_zero_connector_residue` check asks AWS directly for the connector's lambdas, IAM
role, http api and credential provider, and **counts "could not check" as a failure** — the two
existing residue checks had no opinion on any of these, which is how the gate certified a clean
account over a live secret.

### 5.1 `ben-fpa` (2026-09-10) — 20 of 21, and the one that failed is the one that counts

A from-zero run cleared **twenty** checks, including every teardown check, with the account
independently verified at zero afterwards (0 stacks, 0 gateways, 0 credential providers, 0 lambdas,
no `ben-fpa` pools — asked of AWS, not read off the gate's verdict). `CONN_deploy` passed on its own
merit: SoR Lambda up, verify Lambda up, credential provider created, gateway target attached, and
the SoR answering an anonymous probe with **401**.

`CONN_governed_sor_proof` **failed**, and CONN-1 therefore remains unproven and uncited.

The whole diagnosis it produced was:

```
rc=1 FAIL | could not mint a REV token via client 3mejbkk… |
```

— my own guard's words, then an empty string where AWS's words belonged. `tok()` discarded stderr
and ran inside a command substitution, so the real error could not reach the log. **Same defect
class as L70**: an error path that cannot speak turns a specific failure into an unattributable one.

**Root cause, measured rather than read.** The first draft of this diagnosis came from reading
`identity_stack.py`'s header — the exact method §0 of this document exists to forbid. Re-derived
from the artifact: a synth of the identity stack carries `AWS::Cognito::UserPool` = 1,
`UserPoolClient` = 1, `UserPoolGroup` = 4 and **`AWS::Cognito::UserPoolUser` = 0**, with the client's
`ExplicitAuthFlows` = `ALLOW_USER_SRP_AUTH | ALLOW_REFRESH_TOKEN_AUTH`. The CDK path creates no
users. `users.tsv` is rendered from the manifest and is only ever pushed into a pool by
`lib/engine/deploy_identity.sh`, which belongs to the hand-built spine path and never runs in a CDK
environment. The proof was authenticating two identities that had never existed. fp8's
"USER_PASSWORD_AUTH flow not enabled" was Cognito rejecting on the client's allowed flows *before*
it ever looked up the user — which is what hid this second layer for two runs.

**Fixed:** `deploy_connector.sh` now creates both proof users beside the throwaway proof client
(reviewer in `benefits_caseworker` + `tools_granted` + the tenant group read off the live pool;
outsider in none, because that absence is what makes the deny half real) and smoke-tests the mint
where a failure is attributable to the deploy; `destroy_connector.sh` removes them;
`prove_connector.sh`'s `mint()` reports rc and AWS's own message, and asks for `ChallengeName` alone
— never the full response, which on a later success would put a live access token into the gate log
and from there into committed evidence.

**And a test that does not need ten hours.** `lib/connector/selftest_proof_auth.sh` stands up a
throwaway user pool, `sed`s `mkuser()` and `mint()` **out of the shipped scripts** rather than
reimplementing them, and asserts what a 10-hour run would have: that a nonexistent user fails *and
names UserNotFoundException* (the negation test — a suite that cannot see the bug it was written for
is decoration), that both users mint, that the reviewer's decoded token carries all three claims
Cedar reads, that the outsider's carries none, and that teardown removes them. 15/15 on
2026-09-10 in about thirty seconds. Ten hours of live deploy had been the only way to learn one fact
about two API calls; that is now a design defect with a fix, not a cost of doing business.

**Required before CONN-1 may be claimed:** one more from-zero live run in which `CONN_deploy`,
`CONN_governed_sor_proof` and both residue checks pass on their own. Until that exists,
`connect_system_of_record` stays stubbed in the manifest and the connector appears in no brief,
deck, or architecture legend.

And when it does pass, two sentences stay adjacent, as they always have: the system of record is a
**real** OAuth2 API with RS256/JWKS signature verification, and it is **ours**. Proving the governed
path reaches it is not the same as proving a customer's system has been governed.
