# Live re-gate — deep-dive #3 CLOSED end-to-end: authoritative consent/purpose (2026-09-05) — **PASS**

**What this is.** A from-zero AWS deploy (`ben-perim`, `-c perimeter=1`, us-east-1) on governed-core
**1.10.1** + the benefits `authoritative_context` resolver, proving that the Cedar "nine-condition" model
no longer trusts caller assertions — the external review's critical blocker #3. Deployed, proven with
`scripts/cedar_perimeter_proof.py`, and torn down to zero residue. Account ids redacted to `111122223333`.

## Verdict — PASS

| check | result |
|---|---|
| `entitlement_zero_default` — a caseworker with no `custom:tools` claim / not in `tools_granted` gets ZERO tools | **PASS** |
| **`consent_purpose_authoritative`** — authoritative record → allowed; caller-FORGED consent/purpose with NO record → DENIED | **PASS** |
| `amount_cap` — overpayment 9000 → DENIED (decimal cap); 3000 → allowed | **PASS** |

## The #3 proof, from the live call outcomes

Two `assess_eligibility` calls as the SAME entitled caseworker, differing only in whether an
**authoritative** consent/purpose record exists for the case:

- **`authz_present`** — case `CASE-AUTH-…` has an authz record `{consent: true, authorized_purpose:
  "eligibility"}` seeded server-side. Result: **ALLOWED** — returned a real determination
  (`"determination":"ELIGIBLE"`). The gateway interceptor's `authoritative_context` resolver read the
  record and injected `consent`/`purpose`, so Cedar's `consent_purpose_before_assess` passed.
- **`forged_no_record`** — case `CASE-NOAUTH-…` has NO authz record, and the caller **deliberately
  forged** `consent: true, purpose: "eligibility"` in the request. Result: **DENIED** — 
  `Tool call not allowed … [consent_purpose_before_assess]`. The interceptor STRIPPED the caller's
  forged values, the resolver found no record, so Cedar saw consent/purpose UNSET and denied.

This is the whole point of the fix: **a caller cannot assert its own consent/purpose**. It also proves
the interceptor's injection **reaches the Cedar decision** — had Cedar evaluated the pre-interceptor
caller args, the pattern would have inverted (authz_present denied, forged allowed). It did not.

`within_service_window` and `budget_ok` are likewise no longer caller-controllable: the interceptor
derives them from the **server clock** (SERVICE_WINDOW_* — default 00:00–24:00 UTC, i.e. temporal
enforcement opt-in) and the **live meter**. Their fail-closed negatives are covered by governed-core's
offline interceptor tests and the live budget gate.

## How it is wired (all least-privilege, fail-closed)

- `lib/controls/authoritative_context.py` — `resolve(args, tenant)` reads the authoritative consent
  record + the case's authorized purpose from the authz store by `case_id`. No case / no record /
  unreadable table → the field stays UNSET → Cedar denies. Never grants on error.
- DataStack — a new `authz-context` DynamoDB table (case_id key, CMK, TTL). The interceptor gets
  `GetItem` only; multi-tenant adds the per-tenant table pattern.
- compute_stack — `AUTHZ_TABLE` / `AUTHZ_TABLE_TEMPLATE` on the governed Lambdas; `SERVICE_WINDOW_*`
  on the interceptor.
- gateway_stack — `case_id` added to the perimeter input fields so it flows to the interceptor.

## Guardrail + grounding on this deployment

`scripts/guardrail_proof.py` on `ben-perim` confirmed the guardrail + contextual-grounding MECHANISM:
guardrail READY with PROMPT_ATTACK + PII ANONYMIZE, drafter wired, direct `ApplyGuardrail` intervenes,
grounding present + blocks-ungrounded + passes-grounded — all PASS. Its draft-EXECUTION checks were
denied by `require_entitlement` because the guardrail-proof user carries no entitlement claim — i.e. the
zero-default entitlement (#160) correctly refusing an unentitled caller on a perimeter deployment, not a
defect. The full 10/10 guardrail+grounding gate is in `AGENTCORE-GROUNDING-DRAFTER-190-2026-09-05.md`
(baseline `ben-gr` deploy).

## Teardown

`cdk destroy --all` (env `perim`) + `scripts/cleanup_retained.py --prefix ben-perim` (RETAIN'd audit
ledger / WORM vault / Cognito pool). Account model-invocation logging never touched. Raw redacted record:
`evidence/AGENTCORE-PERIMETER-AUTHZ-3-2026-09-05.json`.
