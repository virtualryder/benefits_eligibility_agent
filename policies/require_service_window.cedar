// require_service_window  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS  ·  scope: perimeter (temporal))
// TEMPORAL (#161): no governed DECISION action outside the deployment's service window. Scoped to the
// four consequential tool actions (assess / redetermine / overpayment / draft) rather than left
// unscoped: an unscoped context.input access is invalid on the GA Policy engine because the built-in
// AgentCore actions (InvokeAgent, InvokeLLM, Mcp, ...) carry no `input` in their context. within_service_window
// is set by the gateway REQUEST interceptor from the REAL request time (authoritative - any caller value
// is overwritten); it is an OPTIONAL context.input field, so it is presence-guarded and a missing value
// fails closed (forbid fires). A call outside the window is denied at the gateway before the tool runs.
forbid(
  principal,
  action in [AgentCore::Action::"assess-eligibility___assess_eligibility",
             AgentCore::Action::"redetermine___redetermine",
             AgentCore::Action::"overpayment___detect_overpayment",
             AgentCore::Action::"ben-core___draft_notice"],
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless {
  context.input has within_service_window && context.input.within_service_window == true
};
