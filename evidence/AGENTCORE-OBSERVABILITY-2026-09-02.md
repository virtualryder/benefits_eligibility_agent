# AgentCore full transparency — every API call, the model's reasoning, and the WORM evidence joined by session/trace id, per tenant (live proof 2026-09-02)

**What this proves (phase 110).** Through the REAL AgentCore Runtime (Strands agent on Bedrock, ADOT) for two
tenants, one correlation set — `tenant · session_id · trace_id · request_id · case_id` — joins every signal the
platform and AWS emit for a case: the runtime's `invoke_agent` / cycle / model / tool spans (the model's reasoning),
the gateway's request rows (every `initialize` / `tools/list` / `tools/call`), each tool Lambda's structured
`aegis.call` line, the Bedrock model-invocation rows (the exact request/response bodies) and the hash-chained WORM
record. Every model invocation is tagged with the tenant and session (`requestMetadata`), checked
**masked-before-model**, and the other tenant's ledger holds nothing for the case.

Deployment: `cdk deploy --all -c env=mt3 -c tenants=pha-a,pha-b -c model_logging=1` (8 stacks) + AgentCore Runtime
`benefits_runtime_agent` (CodeBuild, `MULTITENANT=1`, JWT authorizer = the deployment's Cognito pool); governed-core
**1.7.1**; benefits at this commit. Harness: `scripts/obs_two_tenant_proof.py` (verbatim JSON alongside, account
ids in ARNs redacted); the per-case timelines: `scripts/trace_case.py` (Markdown next to this file).

## Verdict — PASS

| check | pha-a | pha-b |
|---|---|---|
| `runtime_invoked_200` | ✓ | ✓ |
| `worm_records` | ✓ | ✓ |
| `agent_span_with_session` | ✓ | ✓ |
| `model_reasoning_spans` | ✓ | ✓ |
| `tool_spans` | ✓ | ✓ |
| `lambda_calls_logged` | ✓ | ✓ |
| `lambda_calls_joined_to_evidence` | ✓ | ✓ |
| `model_invocations_logged` | ✓ | ✓ |
| `model_invocations_tagged_tenant` | ✓ | ✓ |
| `model_invocations_joined_to_spans` | ✓ | ✓ |
| `masked_before_model_all` | ✓ | ✓ |
| `single_tenant_timeline` | ✓ | ✓ |
| `other_tenant_ledger_empty` | ✓ | ✓ |

## What the timelines contain

| tenant | WORM | agent / model / tool spans | gateway rows | Lambda `aegis.call` | model invocations | masked before model | single tenant | other tenant's ledger rows |
|---|---|---|---|---|---|---|---|---|
| `pha-a` | 1 | 1 / 14 / 12 | 33 | 7 (6 joined) | 7 (7 tagged, 7 joined to spans) | True | True | 0 |
| `pha-b` | 1 | 1 / 10 / 12 | 33 | 7 (6 joined) | 5 (5 tagged, 5 joined to spans) | True | True | 0 |

- Runtime invocations: `pha-a` 59.0s, `pha-b` 34.5s (HTTP 200); sessions
  `aegis-pha-a-bbc06cfdbc0f4eb29f63359870578efd` / `aegis-pha-b-48610677f9b845d8ae5f30689809a82b` (explicit `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id`).
- Governed tool calls the agent made (pha-a): ingest_application→ingested=True, intake_application→ok, mask_pii→deidentified=True, assess_eligibility→ok, benefits_core→ok, write_audit→stored=True, request_signoff→requested=False.
- Model reasoning (from the model-invocation log, pha-a; first three):
  - `9530365b` … I'll process this intake following the governed workflow. Let me execute each step in sequence. 
  - `40909599` … Good! Step 1 complete. Now let me mask the PII: 
  - `78164790` … Perfect! Step 2 complete. Now let me assess eligibility with the extracted fields and the sanitized_ref: 
- The WORM record's `correlation` block carries the runtime's trace id + session id + tenant (hashed into the
  chain), and its `invocation` block the Lambda request id — see the JSON.

## Join keys, as observed live

- Runtime → gateway → tool: the Strands MCP client propagates `traceparent`, `X-Amzn-Trace-Id` and `baggage`
  (`session.id`, `tenant`, `case_id`) in `params._meta`; the gateway request rows carry the same `trace_id`; the
  REQUEST interceptor injects them as `__aegis_trace`; each Lambda's `aegis.call` line and WORM record carry them.
- Gateway → Lambda: the gateway propagates the runtime's X-Ray trace to the Lambda invoke, so with Transaction
  Search the tool Lambdas' segments appear in `aws/spans` under the SAME trace id as the agent's spans.
- Runtime → model: `requestMetadata` (tenant / session_id / case_id / requester) on every `ConverseStream` and the
  Bedrock client span's `aws.request_id` == the model-invocation row's `requestId`.

## Found and fixed during the gate (all in the commits of this run)

1. The Strands MCP client carries the OTEL context in `params._meta`, not HTTP headers → governed-core 1.7.1.
2. The tool schemas never exposed `case_ref` / `sanitized_ref` → the gateway stripped the de-identification proof and
   every agent-path determination refused fail-closed (the control worked; the agent path could never succeed).
3. `BedrockModel(region_name=…, boto_session=…)` is refused by Strands; the runtime's session-tenant mirror ignored
   `tenant_<id>` groups; the gateway provider's Update path could race its own delete.
4. `trace_case`: OTEL log records share `spanId` with their span and shadowed `invoke_agent` in the dedup.

## Scope / honesty

- Bedrock model-invocation logging is account+region level; the deployment sets it (`-c model_logging=1`) and
  removes it on teardown; the account's previous configuration was captured and restored afterwards.
- `request_signoff` starts the shell-engine sign-off machine (`governed-signoff`), which this CDK deployment does
  not provision; the agent reports that control block. Sign-off/finalize correlation is covered by the workflow-hop
  proof (`AGENTCORE-MULTITENANT-AUDIT-2026-09-02.md`) and unit tests.
- Disposable users; torn down after the run (confirmation below).

## Teardown (completed 2026-09-02 21:38 EDT)

Runtime `benefits_runtime_agent` deleted; `cdk destroy --all` for `mt3` — all 8 stacks `DELETE_COMPLETE`
(EXIT=0); `list-agent-runtimes`, `list-gateways`, `list-functions ben-mt3*` all empty. The stack's
model-invocation logging configuration was removed on delete and the account's PREVIOUS configuration
(`/aegis/bedrock/model-invocations`, captured before the run) was re-applied and verified. Residual, by
design (retained on destroy): the three `ben-mt3*-audit-ledger` tables and the per-tenant Object-Lock vaults.
