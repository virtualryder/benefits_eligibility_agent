// no_self_commit  (kind: forbid  ·  validation: IGNORE_ALL_FINDINGS)
// The agent can never commit a determination. finalize_determination is forbidden outright and
// hidden from the agent's tool list; the only path to commit is the human sign-off gate
// (Step Functions), where a DIFFERENT qualified caseworker approves with a single-use token.
forbid(
  principal,
  action == AgentCore::Action::"ben-core___finalize_determination",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-eligibility-gw"
);
