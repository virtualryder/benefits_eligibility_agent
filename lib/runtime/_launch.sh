#!/usr/bin/env bash
# Build + deploy the Runtime for an agent. Usage: _launch.sh <agent_dir>
SELF="$(cd "$(dirname "$0")" && pwd)"; export MSYS_NO_PATHCONV=1   # Git-Bash: keep "/ben-.../gateway-url" a parameter NAME, not a Windows path (found 2026-09-02: GATEWAY_SSM_PARAM became C:/Program Files/Git/...)
AGENT="$(cd "${1:?usage: _launch.sh <agent_dir>}" && pwd)"; cd "$SELF"; source "$SELF/_env.sh"
[ -f "$STATE" ] || { echo "spine-state not found ($STATE)."; exit 1; }
source "$STATE"
MODEL="${RUNTIME_MODEL_ID:-us.anthropic.claude-sonnet-4-5-20250929-v1:0}"
echo "GATEWAY_URL=$GW_URL runtime=$RUNTIME_NAME"
# Hybrid multi-tenant (phase 107): MULTITENANT=1 makes the runtime bind the session to the identity's
# tenant and refuse un-tenanted identities (agent.py). Unset = silo.
MT_ENV=(); [ -n "${MULTITENANT:-}" ] && MT_ENV=(--env MULTITENANT="$MULTITENANT")
"$AC" launch \
  --env GATEWAY_URL="$GW_URL" \
  --env GATEWAY_SSM_PARAM="$SSM_PARAM" \
  --env MODEL_ID="$MODEL" \
  --env SYSTEM_PROMPT="$WORKFLOW_PROMPT" \
  "${MT_ENV[@]}" \
  --auto-update-on-conflict 2>&1
echo "LAUNCH_EXIT=${PIPESTATUS[0]}"
