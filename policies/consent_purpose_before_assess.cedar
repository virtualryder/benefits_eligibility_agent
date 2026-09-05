// consent_purpose_before_assess  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS  ·  scope: perimeter)
// CONSENT + PURPOSE (#161) on the eligibility decision. assess_eligibility is refused unless
// recorded consent is present AND the declared purpose is one of the allowed purposes
// (eligibility or redetermination) - purpose-limitation. consent/purpose are OPTIONAL context.input
// fields, so each access is presence-guarded (`context.input has ...`) - the GA AgentCore Policy
// engine validates against the tool schema and rejects an unguarded optional-attribute access.
// A missing field fails the guard, so the forbid fires (fail-closed). These are COARSE gateway gates
// layered on the authoritative server-side controls (the recorded consent artifact, the case purpose
// in the audit trail); no single boolean is accepted downstream as proof, the same defense-in-depth
// role the `deidentified` flag plays. forbid wins over caseworker_permit.
forbid(
  principal,
  action == AgentCore::Action::"assess-eligibility___assess_eligibility",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless {
  context.input has consent && context.input.consent == true
  && context.input has purpose
  && (context.input.purpose == "eligibility" || context.input.purpose == "redetermination")
};
