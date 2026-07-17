// mask_before_assess  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS)
// No eligibility assessment on un-masked data. assess_eligibility is forbidden unless the
// caller passes deidentified == true (set only by mask_pii). forbid wins over any permit.
forbid(
  principal,
  action == AgentCore::Action::"assess-eligibility___assess_eligibility",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless { context.input.deidentified == true };
