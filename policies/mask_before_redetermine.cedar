// mask_before_redetermine  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS)
// No changed-circumstances re-determination on un-masked data. redetermine is forbidden unless the
// caller passes deidentified == true (set only by mask_pii). forbid wins over any permit.
forbid(
  principal,
  action == AgentCore::Action::"redetermine___redetermine",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless { context.input.deidentified == true };
