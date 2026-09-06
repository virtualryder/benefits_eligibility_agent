# Tier-1 live re-gate — `ben-t1` — 2026-09-06 (attempt 11: **PASS**)

Full from-zero acceptance run of the hardened tree (release `v0.5.2-pilot-rc1`) by `scripts/tier1_regate.py`:
deploy all eight stacks in **private** network mode with customer-managed KMS, the enforcement perimeter
(`perimeter=1`), account model-invocation logging into the CMK log group, and capture-all CloudTrail with
advanced selectors; then the checks below; then teardown to zero residue. Raw record:
[`TIER1-REGATE-2026-09-06.json`](TIER1-REGATE-2026-09-06.json) (account id redacted to `111122223333`).

Attempts 1–10 on 2026-09-05/06 each failed on a defect the offline suite could not see; every one is fixed and
pinned by a test — the live-found register **L1–L13** in the platform gap backlog
(`WOGplatform/docs/GAP-CLOSURE-BACKLOG.md`). Attempt 11 is the first end-to-end green run.

## Checks

| Check | Result | Detail |
|---|---|---|
| `deploy` | PASS | rc=0 in 964.4s |
| `P2_advanced_selectors` | PASS | management=True types=12 basic_selectors=False |
| `P5_endpoint_policy_present` | PASS | endpoints=1 |
| `P4_invocation_log_group_cmk` | PASS | kms=5f-8180-f80968f256ee |
| `T1a_guardrail_proof` | PASS | rc=0 |
| `T1b_cedar_perimeter_proof` | PASS | rc=0 |
| `P4_invocation_log_delivered_with_cmk` | PASS | streams_with_events=1 |
| `P3_bypass_alarm_fired` | PASS | alarm=ALARM; bypass=invoked (no guardrail, no gateway - the exact bypass the perimeter must see) |
| `P3_metric_counts_exactly_the_non_allowlisted_calls` | PASS | metric_sum=1.0 human_events=1 |
| `P3_drafter_calls_not_counted` | PASS | drafter_events=2 (allowlisted, must exist and be excluded); metric_sum=1.0 |
| `D2_operator_console_live` | PASS | bytes=3372 |
| `teardown_zero_residue` | PASS | destroy_rc=1 cleanup_rc=0 clean=True model_logging_as_before=True |

## What each PASS proves

- **deploy** — the eight stacks (data, identity, network, compute, workflow, gateway, observability, lineage) create from zero in private mode with every VPC interface endpoint the deployed Lambdas need (L9: `ssm`, `monitoring` were missing until attempt 8), the IaC entitlement grant (L11) and the pinned drafter role (L12).
- **P2** — the capture trail runs advanced event selectors: management events plus 12 Bedrock/AgentCore data-event resource types (L2: `AWS::Bedrock::Prompt` is not a valid type).
- **P5** — the bedrock-runtime VPC endpoint carries the `GovernedDrafterOnly` policy naming the exact pinned drafter role ARN (L12) plus `-c approved_bedrock_principals`.
- **P4** — the model-invocation log group is CMK-encrypted and Bedrock actually delivered the drafter's invocations into it (KMS grant scope, L3).
- **T1a** — guardrail proof: the guardrail exists with PII anonymize + contextual grounding; the drafter is wired to the pinned version; a prompt-injection/exfil case (inside its own masked artifact) is blocked fail-closed with no notice_ref and no canary leak; a clean case drafts with the guardrail applied; `ApplyGuardrail` intervenes deterministically on a jailbreak + raw SSN; grounding blocks an ungrounded answer and passes a grounded one.
- **T1b** — Cedar perimeter proof (#3, #160, #161): zero-default entitlement, consent/purpose, budget, quantitative cap and service-window gates all hold at the gateway in ENFORCE mode.
- **P3** — a real bypass (direct `Converse` by the deployer IAM user, no guardrail, no gateway) fires `ben-t1-bedrock-perimeter-bypass`; the metric counts exactly the non-allowlisted inference events in the capture log (1 = that call) and the drafter's two allowlisted calls through the endpoint are excluded (L10).
- **D2** — the Day-2 operator console renders live from the deployed state.
- **teardown** — the driver's own residue report is clean: no stacks, tables, Lambdas, pools, buckets, AgentCore resources or log groups carry the prefix, and the account's model-invocation logging config is restored as before (L5, L6, L13).

## Proof verdicts (verbatim from the run)

Guardrail proof:

```json
"verdict": {
  "guardrail_exists": true,
  "guardrail_pii_anonymize": true,
  "drafter_wired": true,
  "guardrail_applied_on_every_draft": true,
  "exfil_did_not_leak": true,
  "guardrail_intervenes_directly": true,
  "clean_draft_ok": true,
  "grounding_policy_present": true,
  "grounding_blocks_ungrounded": true,
  "grounding_passes_grounded": true,
  "PASS": true
 }
```

Cedar perimeter proof:

```json
"verdict": {
  "entitlement_zero_default": true,
  "consent_purpose_authoritative": true,
  "amount_cap": true,
  "PASS": true
 }
```

## Bypass event as captured

```json
[{"eventName": "GetGuardrail", "type": "IAMUser", "category": "Management"}, {"eventName": "Converse", "type": "IAMUser", "category": "Management"}]
```

P3 counts: `{"metric_sum": 1.0, "human_events": 1, "drafter_events": 2}`

## Teardown

`destroy_remaining`: `["round 0: re-emptied 5 late deliveries", "ben-t1-lineage deleted", "ben-t1-compute deleted", "ben-t1-network deleted", "ben-t1-identity deleted", "ben-t1-data deleted"]`

Written 2026-09-06 15:26Z from the JSON record; no content beyond the driver's own output was added.
