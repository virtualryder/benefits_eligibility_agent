// require_service_window  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS  ·  scope: perimeter (temporal))
// TEMPORAL (#161): no governed action outside the deployment's service window. The flag
// within_service_window is set by the gateway REQUEST interceptor from the REAL request time
// (authoritative - any caller-supplied value is overwritten), so this is not a caller-asserted
// boolean. A call arriving outside the window is denied at the gateway before any target runs.
forbid(
  principal,
  action,
  resource is AgentCore::Gateway
)
unless { context.input.within_service_window == true };
