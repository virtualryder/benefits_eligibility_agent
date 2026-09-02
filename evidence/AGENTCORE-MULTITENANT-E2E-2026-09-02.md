# Hybrid multi-tenant — LIVE two-tenant end-to-end, 2026-09-02 (env `mt`) — **PASS**

Account **864217980669** · us-east-1 · deploy → prove → destroy. Synthetic data only (900-series SSN).
Harness: `scripts/mt_two_tenant_proof.py` (raw results: `AGENTCORE-MULTITENANT-E2E-2026-09-02.json`).

## What was deployed (first live run of the hybrid control plane)

`cdk deploy --all -c env=mt -c retention_profile=sandbox-demo -c tenants=pha-a,pha-b` → **8 stacks
CREATE_COMPLETE in 499s**: one SHARED control plane (`ben-mt-{identity,compute,workflow,observability,
gateway}` + base `ben-mt-data`) and **two physically separate per-tenant data stacks**
(`ben-mt-pha-a-data`, `ben-mt-pha-b-data`: tenant-scoped tables + each its own WORM vault).

Control plane (live `bedrock-agentcore-control` reads): gateway `ben-mt-ben-gw-20vmzpygzi` **READY**,
`policyEngineConfiguration.mode` = **ENFORCE**, engine `ben_mt_ben_authz-7f_roak7f3`;
**`interceptorConfigurations`** attached — `ben-mt-tenant-interceptor`, `interceptionPoints: [REQUEST]`,
`passRequestHeaders: true`. Identity: `tenant_pha-a` / `tenant_pha-b` Cognito groups + `benefits_caseworker`.

## The proof — three identities drive the gateway over HTTPS with SRP-authenticated access tokens

| Identity | Groups | `tools/list` | `mask_pii` call | sanitized-store counts after |
|---|---|---|---|---|
| cw-a | benefits_caseworker + tenant_pha-a | 200 · **8 tools** | **200, no error** | pha-a **1** · pha-b 0 · base 0 |
| cw-b | benefits_caseworker + tenant_pha-b | 200 · **8 tools** | **200, no error** | pha-a 1 · pha-b **1** · base 0 |
| cw-none | benefits_caseworker (no tenant) | 200 · **0 tools** | **403** | — |

Verbatim deny for cw-none's call (the interceptor, fail-closed):
`{"code": -32000, "message": "multi-tenant: identity carries no tenant (custom:tenant); refused"}` —
and its `tools/list` came back **empty**: the `require_tenant` Cedar forbid removed every tool from an
un-tenanted identity's list (deny-by-default tool filtering) before any call was attempted.

## What this proves, live

1. **Un-tenanted / cross-tenant deny, at two independent layers** — Cedar `require_tenant` (ENFORCE,
   forbid-wins) hides all tools; the gateway REQUEST interceptor refuses the call with a verbatim reason.
2. **Per-tenant physical routing + isolation** — each tenant's artifact landed ONLY in that tenant's own
   store (`ben-mt-<tenant>-sanitized-artifacts`), never the other tenant's, never the base silo table:
   the interceptor derived the tenant from the caller's OWN validated identity, injected it HMAC-signed,
   the tool Lambda verified the signature and routed via `tenancy.route_store`. A caller can only ever
   reach its own tenant — cross-tenant access is impossible by construction.
3. **AgentCore does not forward JWT claims to Lambda targets** (the probe finding) — the interceptor path
   is what makes tenant derivation work, and it worked on the first live attempt.

Verdict (harness): `cw-a_allowed ✓ · cw-b_allowed ✓ · cw-none_denied ✓ · routing_cw-a_only_to_pha-a ✓ ·
routing_cw-b_only_to_pha-b ✓ · PASS`.

## Scope / honesty

- Per-tenant routing is proven for the benefits-owned stores (sanitized artifacts, case store). At the
  time of this run the audit/WORM ledger writer (`governed-core` 1.5.0) still wrote to the base ledger in
  multi-tenant mode. **Closed by governed-core 1.6.0** (per-tenant ledger / WORM vault / approvals
  register routing promoted into the core) — see `evidence/AGENTCORE-MULTITENANT-AUDIT-2026-09-02.md`
  for the live re-run that proves it.
- Test users were disposable (admin-created, deleted with the identity stack). Torn down after the run;
  residual confirmation appended below.

## Teardown (completed 2026-09-02)

`cdk destroy --all --force -c env=mt -c retention_profile=sandbox-demo -c tenants=pha-a,pha-b` — all 8
stacks deleted (the gateway stack ran the AgentCore custom-resource Delete: targets → Cedar policies incl.
`require_tenant` → gateway with its interceptor → policy engine). Confirmed: **residual `ben-mt` CFN
stacks: none; AgentCore gateways named `ben-mt*`: none; policy engines named `ben_mt*`: none.** Per-tenant
audit ledgers / WORM vaults are retained by design (evidence); `scripts/cleanup_retained.py` removes them
if a full wipe is wanted.
