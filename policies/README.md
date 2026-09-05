# Cedar policies (the governance core)

These Cedar statements are the authorization model for the agent. They are the
**single most important artifact in the repo** — everything else exists to enforce them.
Together they implement a **nine-condition model** (#160 entitlement + #161 consent, purpose,
budget, temporal, quantitative, layered on data-classification, tenant, and human-only / SoD).

They are **declared in `agents/benefits-eligibility/manifest.yaml`** (under `policies:`) and
rendered to Cedar by `lib/engine/render.py` at deploy time, then attached to the AgentCore
Policy engine. The `.cedar` files here are the rendered, human-readable form, checked in so the
model is reviewable without running a deploy. The account id (`111122223333`) and gateway ARN
are placeholders — the deploy substitutes the real account and the gateway ARN that only exists
after the gateway is created. `lib/engine/render.py` is the single source of truth; the offline
gate `tests/test_cedar_render.py` re-renders the real manifest, asserts all nine conditions are
present, and parses every statement under the Cedar grammar (cedarpy).

| Policy | Kind | Condition | What it enforces |
|---|---|---|---|
| `caseworker_permit` | permit | (grant) | Only a member of the `benefits_caseworker` Cognito group may use any tool. Everything else is denied by default. |
| `require_entitlement` | forbid | entitlement | **Zero-default tools (#160):** a principal with no NON-EMPTY `custom:tools` claim may call **nothing** — group membership is not enough, and an empty claim is refused. Defense in depth for the interceptor, which already drops the tool list on a missing claim. |
| `mask_before_assess` | forbid | data-classification | `assess_eligibility` cannot run on data that hasn't been de-identified (`deidentified == true`). |
| `mask_before_redetermine` | forbid | data-classification | `redetermine` (changed-circumstances re-determination) cannot run on un-masked data. |
| `mask_before_overpayment` | forbid | data-classification | `detect_overpayment` cannot run on un-masked data. |
| `mask_before_draft` | forbid | data-classification | `draft_notice` cannot run on un-masked data — the model only sees de-identified text. |
| `consent_purpose_before_assess` | forbid | consent + purpose | **(#161)** `assess_eligibility` is refused unless recorded `consent == true` **and** the declared `purpose` is one of `eligibility` / `redetermination` (purpose-limitation). |
| `budget_before_draft` | forbid | budget | **(#161)** `draft_notice` (the only token-spending tool) is refused when `budget_ok == false`, set by the interceptor from the live per-tenant meter at/over the hard cap. |
| `require_service_window` | forbid | temporal | **(#161)** No governed action outside the deployment's service window; `within_service_window` is set by the interceptor from the real request time. |
| `amount_cap_overpayment` | forbid | quantitative | **(#161)** `detect_overpayment` is refused when `prior_monthly_benefit > 5000` — a large-dollar case needs elevated authorization, not a routine caseworker call. |
| `no_self_commit` | forbid | human-only / SoD | The agent can never call `finalize_determination`; committing a determination is reachable **only** through the human sign-off gate. |
| `no_self_fraud_referral` | forbid | human-only / SoD | The agent can never call `refer_fraud`; a suspected-fraud referral is a human-only decision. |
| `require_tenant` | forbid | tenant | **Multi-tenant deployments only** (phase 108): an identity carrying no `custom:tenant` may not call any tool. Forbid wins. Cross-tenant access is impossible by construction - the gateway interceptor derives the tenant from the caller's own validated identity and the target routes to that tenant's store. Not attached in silo mode. |

Two rules of the engine make this airtight:

1. **Deny-by-default.** No statement, no access. `caseworker_permit` is the only broad grant.
2. **Forbid wins.** A `forbid` overrides any `permit`, so no forbid can be circumvented by the
   permit — entitlement, masking-before-processing, consent/purpose, budget, temporal,
   quantitative, tenant, and no-self-commit always hold.

**Coarse gate vs. authoritative control.** The condition booleans (`deidentified`, `consent`,
`budget_ok`, `within_service_window`, ...) are COARSE gateway gates layered on the authoritative
server-side controls — the signed `sanitized_ref`, the live budget meter, the recorded consent
artifact, the interceptor-injected request time. No single boolean is accepted downstream as
proof; they are defense in depth, the same role the `deidentified` flag has always played.

The demo (`bash lib/engine/demo.sh agents/benefits-eligibility`) proves each of these live in
ENFORCE mode, and each denial names the exact policy that fired.
