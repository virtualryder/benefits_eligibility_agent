// amount_cap_overpayment  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS  ·  scope: perimeter)
// QUANTITATIVE (#161): an overpayment computation whose prior_monthly_benefit exceeds the caseworker
// amount cap ($5000) is refused at the gateway - a large-dollar case needs elevated authorization,
// not a routine caseworker call. prior_monthly_benefit is a `number` in the tool schema, so the GA
// Policy engine types it as a Cedar DECIMAL: the comparison uses the decimal extension
// (.lessThanOrEqual(decimal("5000.0"))), not the Long `<=` operator, and is presence-guarded so a
// missing amount fails closed (forbid fires). This is the coarse quantitative gate; the authoritative
// overpayment math and its dollar ceilings live server-side in the tool. forbid wins over caseworker_permit.
forbid(
  principal,
  action == AgentCore::Action::"overpayment___detect_overpayment",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless {
  context.input has prior_monthly_benefit
  && context.input.prior_monthly_benefit.lessThanOrEqual(decimal("5000.0"))
};
