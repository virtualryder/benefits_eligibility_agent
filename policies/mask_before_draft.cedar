// mask_before_draft  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS)
// No notice drafting on un-masked data. draft_notice is forbidden unless deidentified == true,
// so the model only ever sees de-identified case text.
forbid(
  principal,
  action == AgentCore::Action::"ben-core___draft_notice",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless { context.input.deidentified == true };
