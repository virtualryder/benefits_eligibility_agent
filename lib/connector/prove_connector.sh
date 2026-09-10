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
# MINT, and say WHY when it fails. The previous tok() piped stderr nowhere and was called inside a
# command substitution, so on ben-fpa the whole diagnosis of a real failure was
#   "FAIL | could not mint a REV token via client 3mejbkk... | "
# - my guard's words and an empty string where AWS's were. Same defect class as the 2>/dev/null that
# let destroy_connector.sh certify CLEAN over live resources (L70): an error path that cannot speak.
# mint() is called WITHOUT command substitution so the assignment lands in this shell, not a subshell.
mint(){   # $1=variable to set  $2=username  $3=password
  local _n="$1" _u="$2" _p="$3" _o _rc _why
  _o="$(aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id "$AUTH_CLIENT" \
        --auth-parameters "USERNAME=$_u,PASSWORD=$_p" --region "$REGION" \
        --query 'AuthenticationResult.AccessToken' --output text 2>&1 | tr -d '\r')"; _rc=$?
  if [ "$_rc" -ne 0 ] || [ -z "$_o" ] || [ "$_o" = "None" ]; then
    _why="$_o"
    if [ "$_rc" -eq 0 ] && [ "$_o" = "None" ]; then
      # rc=0 with no token means Cognito answered with a CHALLENGE rather than an error. Ask for the
      # challenge NAME only - never re-run without --query and dump the whole response, because on a
      # later success that would put a live access token into the gate log and from there into
      # committed evidence.
      _why="rc=0, no AccessToken - ChallengeName=$(aws cognito-idp initiate-auth \
            --auth-flow USER_PASSWORD_AUTH --client-id "$AUTH_CLIENT" \
            --auth-parameters "USERNAME=$_u,PASSWORD=$_p" --region "$REGION" \
            --query 'ChallengeName' --output text 2>&1 | tr -d '\r')"
    fi
    echo "FAIL | could not mint a $_n token for user '$_u' via client $AUTH_CLIENT (rc=$_rc): ${_why:-<no output>}"
    return 1
  fi
  eval "$_n=\$_o"
}
REV_U="$(awk -F'\t' '$3=="yes"{print $1; exit}' "$BUILD/users.tsv")"; REV_P="$(awk -F'\t' '$3=="yes"{print $2; exit}' "$BUILD/users.tsv")"
OUT_U="$(awk -F'\t' '$3=="no"{print $1; exit}' "$BUILD/users.tsv")"; OUT_P="$(awk -F'\t' '$3=="no"{print $2; exit}' "$BUILD/users.tsv")"
[ -n "$REV_U" ] && [ -n "$OUT_U" ] \
  || { echo "FAIL | users.tsv at $BUILD/users.tsv has no reviewer (yes) / outsider (no) rows"; exit 1; }
# An unminted token is not a caller. Without this guard the proof would carry on and report
# "outsider denied" for a request that was never authenticated - a pass for the wrong reason. mint()
# fails loudly and names the cause, so this exits with a diagnosis rather than a symptom.
mint REV "$REV_U" "$REV_P" || exit 1
mint OUT "$OUT_U" "$OUT_P" || exit 1
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
