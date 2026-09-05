# Live gate — Cedar PERIMETER profile: the #160/#161 nine-condition model (2026-09-05) — **PASS**

**What this is.** ONE from-zero silo deployment of the benefits pack with `-c perimeter=1`, which
attaches the full nine-condition Cedar authorization model to the **GA AgentCore Policy engine** in
**ENFORCE**, exercised as real MCP calls through the gateway by three Cognito identities, then torn
down. Account ids redacted to `111122223333`. Gate driver: `scripts/cedar_perimeter_proof.py`.

The nine conditions: **entitlement** (#160 zero-default tools), **data-classification** (mask-before-
processing), **consent**, **purpose**, **budget**, **temporal** (service window), **quantitative**
(amount cap), **tenant** (multi-tenant only — not in this silo run), and **human-only / SoD**
(no-self-commit / no-self-fraud-referral).

## Deploy

`ben-perim` (silo): `ben-perim-data`, `ben-perim-identity`, `ben-perim-compute`, `ben-perim-gateway`.
The gateway stack's custom-resource provider created the policy engine, MCP gateway (CUSTOM_JWT via the
identity pool), one target per governed tool, and **all 12 silo policies**, then flipped to **ENFORCE**.
Engine `ben_perim_ben_authz`; all 12 policies `ACTIVE`:

    caseworker_permit, mask_before_assess, mask_before_redetermine, mask_before_overpayment,
    mask_before_draft, no_self_commit, no_self_fraud_referral,
    require_entitlement, require_service_window, consent_purpose_before_assess,
    budget_before_draft, amount_cap_overpayment

(`require_tenant` correctly excluded — it is `scope: multitenant`.)

### Authoritative entitlement input

The identity stack ships no users and its access token carries `cognito:groups` but not custom
attributes. For the gate the driver provisioned, on the deployed pool: a `custom:tools` custom
attribute, a `tools_granted` group, and a **Pre-Token-Generation (V2_0) Lambda trigger**
(`scripts/entitlement_mapper.py`) that injects the user's `custom:tools` attribute into the access
token. Three identities (synthetic, disposable):

| identity | groups | custom:tools | expected |
|---|---|---|---|
| `cw-ent`   | benefits_caseworker + tools_granted | (full tool list) | entitled |
| `cw-noent` | benefits_caseworker                 | (empty)          | **denied — zero-default** |
| `cw-claim` | benefits_caseworker                 | (full tool list) | entitled **via the claim alone** |

## Verdict — 6/6 gates held, each denial named its policy

| condition | test (only the tested field differs) | result | policy that fired on the deny |
|---|---|---|---|
| **entitlement (#160)** | `cw-noent` (no grant) calls mask_pii → DENIED; `cw-ent` → allowed | **PASS** | `require_entitlement` |
| **consent (#161)** | assess `consent=false` → DENIED; `consent=true` → past-gate | **PASS** | `consent_purpose_before_assess` |
| **purpose (#161)** | assess `purpose="fraud"` → DENIED; `"eligibility"` → past-gate | **PASS** | `consent_purpose_before_assess` |
| **budget (#161)** | draft `budget_ok=false` → DENIED; `true` → past-gate | **PASS** | `budget_before_draft` |
| **quantitative (#161)** | overpayment `prior_monthly_benefit=9000.0` → DENIED; `3000.0` → past-gate | **PASS** | `amount_cap_overpayment` |
| **temporal (#161)** | assess `within_service_window=false` → DENIED; `true` → past-gate | **PASS** | `require_service_window` |

Verbatim ENFORCE denials (the gateway names the exact policy):

    require_entitlement:           "Policy evaluation denied due to require_entitlement-…"
    consent_purpose_before_assess: "Policy evaluation denied due to consent_purpose_before_assess-…"
    budget_before_draft:           "Policy evaluation denied due to budget_before_draft-…"
    amount_cap_overpayment:        "Policy evaluation denied due to amount_cap_overpayment-…"
    require_service_window:        "Policy evaluation denied due to require_service_window-…"

**Diagnostic — per-user claim path (bonus).** `cw-claim` carries `custom:tools` but is NOT in
`tools_granted`, and it was **allowed** → the pre-token-generation trigger injects `custom:tools` into
the access token AND Cedar reads it as `principal.getTag("custom:tools")`. So entitlement is enforceable
by the richer **per-user claim**, with the `tools_granted` **group** as the tier-independent fallback
(the dual grant in `require_entitlement`). The mask/consent/purpose happy paths ran real **Amazon
Comprehend** masking (`masked_by = comprehend:DetectPiiEntities+regex-backstop`, signed `sanitized_ref`).

## What the LIVE GA engine caught that offline could not

Schema-less `cedarpy` accepts statements the **GA AgentCore Policy engine rejects** at create-policy
time, because the GA engine validates each statement against the AgentCore tool schema. The first
perimeter deploy `CREATE_FAILED`; three real Cedar bugs were found and fixed (now regression-linted
offline by `tests/test_cedar_render.py`):

1. **Optional `context.input` fields must be presence-guarded** (`context.input has consent && …`) —
   an unguarded optional-attribute access is rejected; a missing field now fails closed.
2. **An unscoped `context.input` forbid is invalid** — built-in actions (InvokeAgent/InvokeLLM/Mcp/…)
   carry no `input`, so `require_service_window` is scoped to the four decision actions via `action in […]`.
3. **A `number` tool field is a Cedar decimal** — `prior_monthly_benefit` uses
   `.lessThanOrEqual(decimal("5000.0"))`, not the Long `<=`; and the **caller must send the value with a
   decimal point** (`3000.0`), or Cedar evaluation errors and fails closed.

## Scope / honesty

- The perimeter gates are **coarse gateway gates layered on the authoritative server-side controls**
  (the signed `sanitized_ref`, the live budget meter, the recorded consent, the interceptor-injected
  request time) — the same defense-in-depth role the baseline `deidentified` boolean plays. No single
  boolean is accepted downstream as proof.
- The perimeter profile is **opt-in** (`-c perimeter=1`) so the proven baseline policy set (7 silo
  policies) is byte-for-byte unchanged; verified offline (`_policies(perimeter=False)` = 7).
- The `custom:tools` pre-token-generation trigger is deployed for the gate and torn down with it;
  promoting it into the IdentityStack as IaC is the authoritative-inputs follow-up (#163).

## Teardown

`ben-perim-gateway` stack deleted (removing the policy engine, gateway, targets and all 12 policies via
the custom-resource `Delete`); `ben-perim-compute`, `ben-perim-identity`, `ben-perim-data` destroyed;
the entitlement mapper trigger detached and its Lambda + role deleted (the `custom:tools` pool attribute
cannot be deleted by AWS — harmless, and the pool is removed with the identity stack). The account's
Bedrock **model-invocation logging was never touched** by this profile (the observability stack was not
deployed) and remains on its own log group `/aegis/bedrock/model-invocations` (verified).

**Zero residue** verified via the AWS API: no `ben-perim` CloudFormation stacks, no `perim` policy
engines or gateways remain.

Raw redacted record: `.build/cedar-perimeter-proof.json`.
