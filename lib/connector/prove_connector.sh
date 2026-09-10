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
# Authenticate through the SHIPPED GatewayClient, by SRP, exactly as a real caller does.
# ben-fpb settled this. The proof used to mint through a throwaway USER_PASSWORD_AUTH client so as
# not to weaken the SRP-only shipped one; that client minted tokens fine and the gateway rejected
# every one of them, denying the REVIEWER and the OUTSIDER identically with "insufficient_scope".
# gateway_stack.py: customJWTAuthorizer.allowedClients = [identity.client.user_pool_client_id] - an
# allow-list of ONE. Admitting a test client would have meant editing the production authorizer.
# See mint_token.py for the full account.
AUTH_CLIENT="$CLIENT_ID"
[ -n "$AUTH_CLIENT" ] || { echo "FAIL | no CLIENT_ID in spine-state to authenticate with"; exit 1; }
[ -n "${POOL_ID:-}" ] || { echo "FAIL | no POOL_ID in spine-state - SRP needs the pool"; exit 1; }
# The interpreter that can do SRP is not necessarily the one that can import governed_core, so ask
# each candidate the question that matters instead of assuming. Same lesson as $PY above: existing
# is not the same as being able to do the job.
MINT_PY=""
for CAND in "$PY" "$LIB/runtime/.venv/Scripts/python.exe" "$LIB/runtime/.venv/bin/python" python; do
  if [ -n "$CAND" ] && { [ -f "$CAND" ] || command -v "$CAND" >/dev/null 2>&1; }; then
    "$CAND" -c 'import pycognito' >/dev/null 2>&1 && { MINT_PY="$CAND"; break; }
  fi
done
[ -n "$MINT_PY" ] || { echo "FAIL | no interpreter on this machine can import pycognito, so SRP is impossible"; exit 1; }
# Git-Bash hands out /c/Users/... paths. With MSYS_NO_PATHCONV set they reach a Windows python.exe
# verbatim, which resolves them against the current drive as C:\c\Users\... and dies with ENOENT.
# selftest_proof_auth.sh caught this on 2026-09-10 before any live run paid for it.
MINT_SCRIPT="$SELF/mint_token.py"
command -v cygpath >/dev/null 2>&1 && MINT_SCRIPT="$(cygpath -w "$MINT_SCRIPT")"
[ -n "$MINT_SCRIPT" ] || { echo "FAIL | could not resolve a usable path to mint_token.py"; exit 1; }
# MINT, and say WHY when it fails. The previous tok() piped stderr nowhere and was called inside a
# command substitution, so on ben-fpa the whole diagnosis of a real failure was
#   "FAIL | could not mint a REV token via client 3mejbkk... | "
# - my guard's words and an empty string where AWS's were. Same defect class as the 2>/dev/null that
# let destroy_connector.sh certify CLEAN over live resources (L70): an error path that cannot speak.
# mint() is called WITHOUT command substitution so the assignment lands in this shell, not a subshell.
mint(){   # $1=variable to set  $2=username  $3=password
  local _n="$1" _u="$2" _p="$3" _o _rc
  # mint_token.py prints the token on stdout OR the reason on stderr, never both. 2>&1 folds them
  # together deliberately: on success $_o is the token, on failure it is AWS's own words.
  _o="$("$MINT_PY" "$MINT_SCRIPT" "$POOL_ID" "$AUTH_CLIENT" "$REGION" "$_u" "$_p" 2>&1 | tr -d '\r')"; _rc=$?
  if [ "$_rc" -ne 0 ] || [ -z "$_o" ] || [ "$_o" = "None" ]; then
    echo "FAIL | could not mint a $_n token for user '$_u' by SRP via client $AUTH_CLIENT (rc=$_rc): ${_o:-<no output>}"
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
# Order matters, and it is the opposite of the obvious one. On ben-fpb this step read
#   FAIL | outsider not denied -> DENY insufficient_scope - The request requires higher privileges...
# and the tempting fix was to add DENY to the pattern - which would have turned this check GREEN while
# the gateway was refusing the REVIEWER with the identical string. A vocabulary match cannot tell
# "denied because unauthorized" from "denied because nothing works". So the dangerous case is tested
# FIRST and on substance: if the outsider ever receives an authoritative record, no wording makes
# that a pass. Only then is the denial vocabulary consulted - and step 2 above is what proves the
# denial is selective rather than universal.
if echo "$OD" | grep -q '"verified": *true'; then
  echo "  FAIL | outsider RECEIVED AN AUTHORITATIVE RECORD - deny-by-default is broken -> $OD"; fail=$((fail+1))
elif echo "$OD" | grep -qiE 'deny|denied|not allowed|policy enforcement|insufficient_scope|accessdenied|unauthorized|forbidden'; then
  echo "  PASS | outsider call to verify_source DENIED (Cedar deny-by-default) -> $(echo "$OD" | cut -c1-110)"; pass=$((pass+1))
else
  echo "  FAIL | outsider neither denied nor recognisable as a denial -> $OD"; fail=$((fail+1))
fi

echo "=== CONNECTOR PROOF: $pass passed, $fail failed ==="
[ "$fail" -eq 0 ] && echo "CONNECTOR PROOF: PASS" || { echo "CONNECTOR PROOF: FAIL"; exit 1; }
