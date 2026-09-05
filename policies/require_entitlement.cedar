// require_entitlement  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS)
// ENTITLEMENT / zero-default tools (#160): a principal with no NON-EMPTY custom:tools
// entitlement claim may call NOTHING - being in the benefits_caseworker group is not
// enough. An empty-string claim ("") is also refused. Forbid wins over caseworker_permit,
// so tools are opt-in per identity, never default-to-all. This is defense in depth for the
// gateway REQUEST interceptor, which already drops the entire advertised tool list when the
// claim is missing or malformed; the policy makes the denial authoritative at the engine.
forbid(
  principal,
  action,
  resource is AgentCore::Gateway
)
unless {
  principal.hasTag("custom:tools") && principal.getTag("custom:tools") != ""
};
