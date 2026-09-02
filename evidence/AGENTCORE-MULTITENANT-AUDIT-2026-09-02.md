# AgentCore hybrid multi-tenant — per-tenant AUDIT routing, live proof (2026-09-02)

**What this proves.** With governed-core **1.6.0** the CANONICAL evidence writer, the exactly-once
finalize marker and the pending-approvals register route to the acting tenant's PHYSICALLY separate
ledger / WORM vault / approvals table — across BOTH trust hops: the AgentCore Gateway (request
interceptor injects the HMAC-signed tenant) and the Step Functions workflow (no interceptor; the
signed pair travels in the execution input and every Lambda re-verifies it). The shared base ledger
and base vault received **zero** writes for the entire run. This closes the cross-repo gap recorded
in `AGENTCORE-MULTITENANT-E2E-2026-09-02.md`.

Deployment: `cdk deploy --all -c env=mt2 -c retention_profile=sandbox-demo -c tenants=pha-a,pha-b`
(8 stacks, from zero, account 864217980669 / us-east-1; benefits `c29003b`+, governed-core `v1.6.0`
pinned by hash `6dbe4c26…93cd`). Gateway `https://ben-mt2-ben-gw-vrmhkswhoe.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp`, enforcement `ENFORCE`.
Harness: `scripts/mt_two_tenant_proof.py --env mt2 --tenants pha-a,pha-b` (verbatim JSON alongside; ARN account ids redacted to 111122223333 per repo policy).

## Verdict

| check | result |
|---|---|
| `cw-a_allowed` | ✓ PASS |
| `cw-b_allowed` | ✓ PASS |
| `cw-none_denied` | ✓ PASS |
| `routing_cw-a_only_to_pha-a` | ✓ PASS |
| `routing_cw-b_only_to_pha-b` | ✓ PASS |
| `audit_cw-a_ledger_and_worm_only_pha-a` | ✓ PASS |
| `audit_cw-b_ledger_and_worm_only_pha-b` | ✓ PASS |
| `ingest_refuses_without_verified_token` | ✓ PASS |
| `workflow_reached_signoff_with_binding` | ✓ PASS |
| `workflow_intent_evidence_only_pha-a` | ✓ PASS |
| `workflow_pending_approval_only_pha-a` | ✓ PASS |
| `workflow_without_binding_fails_closed` | ✓ PASS |
| `PASS` | ✓ PASS |

## Gateway hop — `write-audit___write_audit` as two tenanted identities

- cw-a (groups `benefits_caseworker`, `tenant_pha-a`): `stored:true worm:true` → table
  `ben-mt2-pha-a-audit-ledger`, bucket `ben-mt2-pha-a-worm-864217980669`, key `MT-E40A087D/e3ca2eb5b696f9759f26fcf8f90d0aec4cf2a47d8fdef42f587df076c8047669.json` (seq 0, prev `GENESIS`).
- cw-b (`tenant_pha-b`): `stored:true worm:true` → table `ben-mt2-pha-b-audit-ledger`, bucket `ben-mt2-pha-b-worm-864217980669`.
- Counts: before — ledger a/b/base = 0/0/0 · WORM a/b/base = 0/0/0; after cw-a — ledger a/b/base = 2/0/0 · WORM a/b/base = 1/0/0; after cw-b — ledger a/b/base = 2/2/0 · WORM a/b/base = 1/1/0.
  (Each write is 2 ledger rows: the immutable event + the `HEAD#` chain tip.)
- cw-none (no tenant): 0 tools listed, `tools/call` denied verbatim (require_tenant / interceptor) — unchanged.

## Workflow hop — token-verified ingest → execution with the signed pair

- `ingest-application` invoked directly (IAM) with cw-a's Cognito access token: `ingested:true`, the
  response minted `tenant_binding` (`__aegis_tenant` / `__aegis_tenant_sig`). The same call with a typed
  `tenant` and no token: `multi-tenant: ingestion identity not verified: no access token presented`.
- Execution `mtproof-mt-wf-c0c146` carrying the pair: states
  Extract → GuardExtracted → MaskPii → GuardDeidentified → AssessEligibility → GuardRulesExecuted → CheckAdverseNotice → DraftNotice → AuditIntent → HumanSignoff → status `RUNNING` at the sign-off pause (then stopped by the harness).
- Evidence + approvals: ledger/WORM before — ledger a/b/base = 2/2/0 · WORM a/b/base = 1/1/0; after — ledger a/b/base = 4/2/0 · WORM a/b/base = 2/1/0
  (AuditIntent's record + WORM copy landed in **pha-a only**). Pending-approvals row for the case:
  pha-a `True`, pha-b `False`, base `False`.
- The SAME execution started WITHOUT the pair: `FAILED` /
  `States.Runtime` at `Extract` — fail-closed, nothing written anywhere.

## Found and fixed during the run (both are in this commit)

1. **Missing IAM read of the signing secret** on the audit writer, intake and sign-off Lambdas: they
   could not VERIFY the HMAC pair, so they refused (`TenantError` / `stored:false … routing refused`)
   — correct fail-closed behaviour, missing grant. Every multi-tenant verifier now reads the secret;
   `test_cdk_stacks` asserts it.
2. **Failure poisoning** in `provenance._sm`: a failed Secrets Manager read was cached for the
   container lifetime, so warm containers kept refusing after the grant landed. Only successful
   reads are cached now.

## Scope / honesty

- Silo deployments are unchanged (routers are identity when `MULTITENANT` is unset).
- The ingestion boundary (direct Lambda invoke) derives the tenant from a VERIFIED Cognito access
  token of a tenant member; the IAM principal allowed to invoke ingest is the deployment's intake
  integration. Tenant onboarding = a `tenant_<id>` group + a per-tenant DataStack.
- Approval (`approve_signoff`) and finalize routing use the same verified pair; this run stopped at
  the sign-off pause and did not exercise finalize live (finalize's per-tenant marker is covered by
  governed-core `tests/test_tenant_routing.py`).
- Disposable users; torn down after the run (confirmation below).

## Teardown (completed 2026-09-02 18:25 EDT)

`cdk destroy --all --force -c env=mt2 -c retention_profile=sandbox-demo -c tenants=pha-a,pha-b` — all 8
stacks `DELETE_COMPLETE` (EXIT=0). Residual, **by design (retained on destroy)**: the three hash-chained
ledgers `ben-mt2-audit-ledger`, `ben-mt2-pha-a-audit-ledger`, `ben-mt2-pha-b-audit-ledger` (the base one
holds 0 rows — it was never written) and the Object-Lock vaults `ben-mt2-pha-a-worm-864217980669`,
`ben-mt2-pha-b-worm-864217980669` (+ the base vault / observability data-events bucket). No Lambda,
gateway, state machine or user pool remains (`list-functions`, `list-gateways`, `list-stacks` empty for
`ben-mt2`). Retained stores are removed with `scripts/cleanup_retained.py` once their retention lapses.
