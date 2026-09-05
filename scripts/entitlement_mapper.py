#!/usr/bin/env python3
"""entitlement_mapper — Cognito Pre-Token-Generation (V2_0) trigger for AUTHORITATIVE entitlement.

Makes the per-user tool entitlement authoritative in the ACCESS token so the require_entitlement Cedar
gate (#160, zero-default tools) can read it as principal.getTag("custom:tools"). A Cognito access token
carries cognito:groups natively but NOT custom attributes; this trigger copies the user's authoritative
`custom:tools` attribute into an access-token claim of the same name (access-token customization needs
the ESSENTIALS/PLUS feature plan, which the pool uses). Empty/absent => the claim is set to "" so the
gate denies (with the tools_granted group as the tier-independent fallback grant).

This is the reference wiring for the perimeter profile's entitlement input. It is deployed for the live
Cedar-perimeter gate and torn down with it; productionizing it into the IdentityStack is tracked as the
authoritative-inputs follow-up (#163).
"""


def handler(event, context):
    attrs = (event.get("request") or {}).get("userAttributes") or {}
    tools = attrs.get("custom:tools", "") or ""
    event.setdefault("response", {})["claimsAndScopeOverrideDetails"] = {
        "accessTokenGeneration": {
            "claimsToAddOrOverride": {"custom:tools": tools},
        },
        "idTokenGeneration": {
            "claimsToAddOrOverride": {"custom:tools": tools},
        },
    }
    return event
