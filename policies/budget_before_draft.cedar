// budget_before_draft  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS)
// BUDGET (#161) on the model-spending drafter. draft_notice is the only tool that spends model
// tokens, so it carries the spend gate: budget_ok is set by the gateway REQUEST interceptor from
// the LIVE per-tenant meter (<prefix>-budgets), not asserted by the caller. When the tenant is at
// or over its hard cap the interceptor sets budget_ok false and this forbid fires, failing the
// draft closed. The authoritative meter + AWS Budgets kill switch remain the enforcing controls;
// this is the coarse gateway layer. forbid wins over caseworker_permit.
forbid(
  principal,
  action == AgentCore::Action::"ben-core___draft_notice",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless { context.input.budget_ok == true };
