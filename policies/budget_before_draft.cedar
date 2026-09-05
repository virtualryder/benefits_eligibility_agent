// budget_before_draft  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS  ·  scope: perimeter)
// BUDGET (#161) on the model-spending drafter. draft_notice is the only tool that spends model
// tokens, so it carries the spend gate: budget_ok is set by the gateway REQUEST interceptor from
// the LIVE per-tenant meter (<prefix>-budgets), not asserted by the caller. budget_ok is an OPTIONAL
// context.input field, so it is presence-guarded (`context.input has budget_ok`) - the GA Policy
// engine rejects an unguarded optional-attribute access; a missing field fails the guard so the
// forbid fires (fail-closed). The authoritative meter + AWS Budgets kill switch remain the enforcing
// controls; this is the coarse gateway layer. forbid wins over caseworker_permit.
forbid(
  principal,
  action == AgentCore::Action::"ben-core___draft_notice",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless { context.input has budget_ok && context.input.budget_ok == true };
