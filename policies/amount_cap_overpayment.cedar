// amount_cap_overpayment  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS  ·  scope: perimeter)
// QUANTITATIVE (#161): an overpayment computation whose prior_monthly_benefit exceeds the
// caseworker amount cap ($5000) is refused at the gateway - a large-dollar case needs elevated
// authorization, not a routine caseworker call. This is the coarse quantitative gate; the
// authoritative overpayment math and its dollar ceilings live server-side in the tool. forbid
// wins over caseworker_permit.
forbid(
  principal,
  action == AgentCore::Action::"overpayment___detect_overpayment",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
)
unless { context.input.prior_monthly_benefit <= 5000 };
