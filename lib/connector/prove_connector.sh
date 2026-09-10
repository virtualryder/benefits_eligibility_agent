#!/usr/bin/env bash
# prove_connector.sh — REUSABLE. Prove the governed OAuth connector end to end for any agent.
# Usage: bash lib/connector/prove_connector.sh <agent_dir>
set -uo pipefail
export AWS_PAGER=""
AGENT_DIR="${1:?usage: prove_connector.sh <agent_dir>}"
SELF="$(cd "$(dirname "$0")" && pwd)"; LIB="$(cd "$SELF/.." && pwd)"
AGENT="$(cd "$AGENT_DIR" && pwd)"; BUILD="$AGENT/.build"
mkdir -p "$BUILD"; python "$LIB/engine/render.py" "$AGENT/manifest.yaml" "$BUILD" >/dev/null 2>&1 || true
source "$BUILD/agent.env"; source "$AGENT/spine-state.env"; source "$AGENT/connector-state.env"
# mcp_client lives in the PINNED governed-core, not in this repo. Pointing at
# "$LIB/controls/mcp_client.py" meant this proof could never run: the file exists nowhere in the
# tree, and copying it here would shadow the core module - which tests/test_core_dependency.py
# exists to forbid. Resolve it from the installed package instead, so the proof uses the same
# hash-locked client everything else does.
# Pick the interpreter by CAPABILITY, not by path. The previous version took
# lib/runtime/.venv first because it exists - but that venv is the Lambda BUILD environment and
# has no governed_core installed ("ModuleNotFoundError"), so CLIENT came back empty and this proof
# aborted on 2026-09-10 (ben-fp7) even though the connector had deployed perfectly: SoR Lambda up,
# gateway target attached, and the SoR answering an anonymous probe with 401. Existing is not the
# same as being able to do the job; ask each candidate whether it can actually import the pinned
# core, and use the one that answers yes for BOTH resolving and running the client.
PY=""
for CAND in "$LIB/runtime/.venv/Scripts/python.exe" "$LIB/runtime/.venv/bin/python" python; do
  if [ -f "$CAND" ] || command -v "$CAND" >/dev/null 2>&1; then
    C="$("$CAND" -c 'import governed_core, os; print(os.path.join(governed_core.controls_dir(), "mcp_client.py"))' 2>/dev/null | tr -d '\r')"
    if [ -n "$C" ] && [ -f "$C" ]; then PY="$CAND"; CLIENT="$C"; break; fi
  fi
done
[ -n "$PY" ] && [ -n "${CLIENT:-}" ] && [ -f "$CLIENT" ] || {
  echo "FAIL | no interpreter on this machine can import the pinned governed-core (tried the runtime venv and system python)"; exit 1; }
# Use the throwaway proof client, NOT the CDK GatewayClient. The shipped client is SRP-only by
# design (identity_stack.py: "no USER_PASSWORD_AUTH in the CDK path"), which is why fp8 failed here
# with "USER_PASSWORD_AUTH flow not enabled for this client". Fall back to CLIENT_ID so a
# hand-built environment (deploy_identity.sh, whose client does allow it) still works.
AUTH_CLIENT="${PROOF_CLIENT_ID:-$CLIENT_ID}"
[ -n "$AUTH_CLIENT" ] || { echo "FAIL | no PROOF_CLIENT_ID or CLIENT_ID to authenticate with"; exit 1; }
tok(){ aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id "$AUTH_CLIENT" \
        --auth-parameters "USERNAME=$1,PASSWORD=$2" --region "$REGION" --query 'AuthenticationResult.AccessToken' --output text | tr -d '\r'; }
REV_U="$(awk -F'\t' '$3=="yes"{print $1; exit}' "$BUILD/users.tsv")"; REV_P="$(awk -F'\t' '$3=="yes"{print $2; exit}' "$BUILD/users.tsv")"
OUT_U="$(awk -F'\t' '$3=="no"{print $1; exit}' "$BUILD/users.tsv")"; OUT_P="$(awk -F'\t' '$3=="no"{print $2; exit}' "$BUILD/users.tsv")"
REV="$(tok "$REV_U" "$REV_P")"; OUT="$(tok "$OUT_U" "$OUT_P")"
# An empty or "None" token is not a caller. Without this the proof would carry on and report
# "outsider denied" for a request that was never authenticated - a pass for the wrong reason.
for _n in REV OUT; do
  eval "_v=\$$_n"
  [ -n "$_v" ] && [ "$_v" != "None" ] || { echo "FAIL | could not mint a $_n token via client $AUTH_CLIENT"; exit 1; }
done
call(){ "$PY" "$CLIENT" "$GW_URL" "$1" "$2" "$3"; }   # same interpreter that resolved CLIENT
pass=0; fail=0

echo "=== CONNECTOR PROOF ($SLUG): governed verify_source via AgentCore Identity outbound OAuth ($SOR_LABEL) ==="

echo "-- 1. the system of record REALLY requires OAuth (no token / bad token are rejected) --"
NO_TOK="$(curl -s -o /dev/null -w '%{http_code}' "$SOR_URL?case_id=CASE-1")"
BAD_TOK="$(curl -s -o /dev/null -w '%{http_code}' -H 'Authorization: Bearer not-a-real-token' "$SOR_URL?case_id=CASE-1")"
if [ "$NO_TOK" = "401" ] && { [ "$BAD_TOK" = "401" ] || [ "$BAD_TOK" = "403" ]; }; then
  echo "  PASS | SoR rejects no-token ($NO_TOK) and bad-token ($BAD_TOK) — genuinely OAuth-protected"; pass=$((pass+1))
else echo "  FAIL | SoR did not reject unauthenticated calls (no=$NO_TOK bad=$BAD_TOK)"; fail=$((fail+1)); fi

echo "-- 2. governed tool: reviewer calls verify_source; AgentCore Identity mints the outbound token --"
VI="$(call "$REV" "$TOOL_ID" '{"case_id":"CASE-1"}')"
if echo "$VI" | grep -q '"verified": *true' && echo "$VI" | grep -qi 'AgentCore Identity'; then
  echo "  PASS | verify_source returned an authoritative record via the OAuth-protected SoR (token minted by Identity)"; pass=$((pass+1))
else echo "  FAIL | verify_source -> $VI"; fail=$((fail+1)); fi
if echo "$VI" | grep -q '"tool_holds_secret": *false'; then echo "  PASS | the tool holds NO client secret (it lives in the Identity token vault)"; pass=$((pass+1)); else echo "  FAIL | secret-handling claim missing -> $VI"; fail=$((fail+1)); fi

echo "-- 3. deny-by-default extends to the new connector (outsider denied) --"
OD="$(call "$OUT" "$TOOL_ID" '{"case_id":"CASE-1"}')"
if echo "$OD" | grep -qiE 'denied|not allowed|policy enforcement'; then echo "  PASS | outsider call to verify_source DENIED (Cedar deny-by-default)"; pass=$((pass+1)); else echo "  FAIL | outsider not denied -> $OD"; fail=$((fail+1)); fi

echo "=== CONNECTOR PROOF: $pass passed, $fail failed ==="
[ "$fail" -eq 0 ] && echo "CONNECTOR PROOF: PASS" || { echo "CONNECTOR PROOF: FAIL"; exit 1; }
