# selftest_proof_auth.sh — prove the connector's PROOF AUTH PATH works, without a 10-hour gate run.
#
# Why this exists. On ben-fpa every platform check passed and CONN_governed_sor_proof failed with
#   "could not mint a REV token via client 3mejbkk... | "
# - my own guard's words followed by an empty string where AWS's should have been. The cause was that
# the CDK identity stack creates ZERO Cognito users (measured: a synth carries UserPool=1,
# UserPoolClient=1, UserPoolGroup=4 and no AWS::Cognito::UserPoolUser at all), while the proof
# authenticated users that only lib/engine/deploy_identity.sh - the hand-built spine path - ever
# creates. Ten hours of live deploy to learn one fact about two API calls.
#
# So this stands up a THROWAWAY user pool, runs the REAL functions out of the REAL scripts against
# it, asserts the claims that Cedar actually reads, and deletes the pool. Minutes, not hours.
#
# It does NOT extract-and-reimplement: mkuser() is cut out of deploy_connector.sh and mint() out of
# prove_connector.sh at run time and eval'd here, so this tests the shipped text. If someone edits
# those functions, this test follows them - and if someone deletes them, it fails loudly instead of
# quietly testing a copy that no longer ships.
#
# Usage: bash lib/connector/selftest_proof_auth.sh [region]
# Exit 0 = the auth path works. Non-zero = it does not, and the reason is printed.
set -uo pipefail
export AWS_PAGER="" MSYS_NO_PATHCONV=1
REGION="${1:-us-east-1}"
SELF="$(cd "$(dirname "$0")" && pwd)"
command -v aws >/dev/null 2>&1 || { echo "SELFTEST FATAL: aws CLI not on PATH - refusing to run"; exit 1; }

POOL_NAME="conn-selftest-$$-$(date +%s)"
POOL_ID=""
pass=0; fail=0
ok(){   echo "  PASS | $*"; pass=$((pass+1)); }
bad(){  echo "  FAIL | $*"; fail=$((fail+1)); }
log(){  echo "[selftest] $*"; }
err(){  echo "[selftest] ERROR: $*" >&2; fail=$((fail+1)); }

# The pool is real and costs nothing but must not outlive this script. EXIT covers the error paths
# too - a self-test that leaks the resource it created has no business auditing anyone's teardown.
cleanup(){
  if [ -n "$POOL_ID" ]; then
    if aws cognito-idp delete-user-pool --user-pool-id "$POOL_ID" --region "$REGION" 2>/dev/null; then
      log "deleted throwaway pool $POOL_ID"
    else
      echo "[selftest] LEFT BEHIND: user pool $POOL_ID ($POOL_NAME) - delete it by hand" >&2
    fi
  fi
}
trap cleanup EXIT

# ---- lift the REAL functions out of the REAL scripts -------------------------------------------
# sed prints from the function's opening line to its closing brace at column 0. If either script is
# refactored so the marker no longer matches, extraction yields nothing and the guard below fails the
# test - which is the correct outcome: this must never silently fall back to a private copy.
MKUSER_SRC="$(sed -n '/^mkuser(){/,/^}/p' "$SELF/deploy_connector.sh")"
MINT_SRC="$(sed -n '/^mint(){/,/^}/p'   "$SELF/prove_connector.sh")"
[ -n "$MKUSER_SRC" ] || { echo "SELFTEST FATAL: could not extract mkuser() from deploy_connector.sh"; exit 1; }
[ -n "$MINT_SRC" ]   || { echo "SELFTEST FATAL: could not extract mint() from prove_connector.sh";  exit 1; }
eval "$MKUSER_SRC"
eval "$MINT_SRC"
log "extracted mkuser() ($(echo "$MKUSER_SRC" | wc -l) lines) and mint() ($(echo "$MINT_SRC" | wc -l) lines) from the shipped scripts"

# ---- 1. throwaway pool, groups and proof client --------------------------------------------------
# The password policy mirrors the CDK pool so a policy-rejected password fails HERE, not in a run.
POOL_ID="$(aws cognito-idp create-user-pool --pool-name "$POOL_NAME" --region "$REGION" \
  --policies '{"PasswordPolicy":{"MinimumLength":12,"RequireUppercase":true,"RequireLowercase":true,"RequireNumbers":true,"RequireSymbols":true}}' \
  --query 'UserPool.Id' --output text 2>&1 | tr -d '\r')"
case "$POOL_ID" in us-east-*|us-*_*) log "created throwaway pool $POOL_ID" ;;
  *) echo "SELFTEST FATAL: could not create a user pool: $POOL_ID"; POOL_ID=""; exit 1 ;; esac

for g in benefits_caseworker tools_granted tenant_sp-a; do
  aws cognito-idp create-group --user-pool-id "$POOL_ID" --group-name "$g" --region "$REGION" >/dev/null 2>&1 \
    || err "could not create group $g"
done

# SRP ONLY, exactly like the shipped GatewayClient (identity_stack.py: AuthFlow(user_srp=True)).
# On ben-fpb this client was created with ALLOW_USER_PASSWORD_AUTH, and that is precisely why the
# self-test went 15/15 green over a connector the gateway would reject: the test client could do
# something the real one cannot, so the test was not testing the shipped path. A fixture that is
# more permissive than production does not validate production.
AUTH_CLIENT="$(aws cognito-idp create-user-pool-client --user-pool-id "$POOL_ID" \
  --client-name "selftest-gateway-client" --explicit-auth-flows ALLOW_USER_SRP_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --region "$REGION" --query 'UserPoolClient.ClientId' --output text 2>&1 | tr -d '\r')"
[ -n "$AUTH_CLIENT" ] && [ "$AUTH_CLIENT" != "None" ] \
  || { echo "SELFTEST FATAL: could not create the SRP client: $AUTH_CLIENT"; exit 1; }
log "created SRP-only client $AUTH_CLIENT (mirrors the shipped GatewayClient)"

# mint() shells out to mint_token.py through $MINT_PY, and resolves the script via $SELF - both are
# set by prove_connector.sh at run time, so set them the same way here.
MINT_PY=""
LIB="$(cd "$SELF/.." && pwd)"
for CAND in python "$LIB/runtime/.venv/Scripts/python.exe" "$LIB/runtime/.venv/bin/python"; do
  if [ -n "$CAND" ] && { [ -f "$CAND" ] || command -v "$CAND" >/dev/null 2>&1; }; then
    "$CAND" -c 'import pycognito' >/dev/null 2>&1 && { MINT_PY="$CAND"; break; }
  fi
done
[ -n "$MINT_PY" ] || { echo "SELFTEST FATAL: no interpreter here can import pycognito"; exit 1; }
MINT_SCRIPT="$SELF/mint_token.py"
command -v cygpath >/dev/null 2>&1 && MINT_SCRIPT="$(cygpath -w "$MINT_SCRIPT")"
log "mint interpreter: $MINT_PY  script: $MINT_SCRIPT"

# ---- 2. NEGATIVE FIRST: reproduce the ben-fpa failure ---------------------------------------------
# Before proving the fix works, prove the test can SEE the bug. A user that does not exist is exactly
# the fpa condition; if mint() succeeded here, or failed without saying why, this self-test would be
# incapable of catching a regression and every PASS below would be worthless. Negation-test per L60.
NEG="$(mint NEVERMINTED "ghost-user-that-does-not-exist" "Whatever-Pass1!" 2>&1)"
if [ -n "$NEG" ] && echo "$NEG" | grep -q 'could not mint'; then
  if echo "$NEG" | grep -qiE 'UserNotFound|NotAuthorized|Incorrect username|rc=[1-9]'; then
    ok "a nonexistent user fails AND the message carries AWS's own reason -> $(echo "$NEG" | cut -c1-150)"
  else
    bad "a nonexistent user failed but the message names no cause (the ben-fpa defect is still here) -> $NEG"
  fi
else
  bad "mint() did not fail for a nonexistent user - this test cannot detect the bug it exists for -> ${NEG:-<silence>}"
fi

# ---- 3. create the proof users through the SHIPPED mkuser() --------------------------------------
REV_U="selftest-caseworker"; REV_P="ChangeMe-Reviewer1!"
OUT_U="selftest-outsider";   OUT_P="ChangeMe-Outsider1!"
TENANT_G="$(aws cognito-idp list-groups --user-pool-id "$POOL_ID" --region "$REGION" \
  --query "Groups[?starts_with(GroupName,'tenant_')].GroupName | [0]" --output text 2>/dev/null | tr -d '\r')"
[ "$TENANT_G" = "None" ] && TENANT_G=""
[ -n "$TENANT_G" ] && ok "tenant group discovered off the live pool: $TENANT_G" \
                   || bad "no tenant_* group found on the pool - require_tenant would forbid every call"

mkuser "$REV_U" "$REV_P" "benefits_caseworker tools_granted${TENANT_G:+ $TENANT_G}" \
  && ok "mkuser created the reviewer" || bad "mkuser could not create the reviewer"
mkuser "$OUT_U" "$OUT_P" "" \
  && ok "mkuser created the outsider" || bad "mkuser could not create the outsider"

# Idempotence: a re-run must not fail on UsernameExistsException. deploy_connector.sh is re-runnable
# by contract and CONN_deploy would go red on the second attempt if this were not true.
mkuser "$REV_U" "$REV_P" "benefits_caseworker" >/dev/null \
  && ok "mkuser is idempotent (second call on an existing user succeeds)" \
  || bad "mkuser is NOT idempotent - a re-deploy would fail on UsernameExistsException"

# ---- 4. POSITIVE: both identities mint a token through the SHIPPED mint() -------------------------
REV=""; OUT=""
if mint REV "$REV_U" "$REV_P"; then ok "reviewer minted an access token"
else bad "reviewer could NOT mint - this is the ben-fpa failure, unfixed"; fi
if mint OUT "$OUT_U" "$OUT_P"; then ok "outsider minted an access token (it must authenticate; Cedar is what denies it)"
else bad "outsider could NOT mint - the deny half of the proof would be a pass for the wrong reason"; fi

# ---- 5. the CLAIMS Cedar actually reads ----------------------------------------------------------
# Minting is not enough. caseworker_permit reads cognito:groups for benefits_caseworker,
# require_entitlement for tools_granted, require_tenant for tenant_*. A token that carries the wrong
# groups authenticates perfectly and is then denied at the gateway - which on a 10-hour run looks
# identical to a broken connector. Decode the payload here instead.
claims(){   # $1 = JWT -> prints the decoded payload
  local _p="${1#*.}"; _p="${_p%%.*}"
  case $(( ${#_p} % 4 )) in 2) _p="$_p==" ;; 3) _p="$_p=" ;; esac
  printf '%s' "$_p" | tr '_-' '/+' | base64 -d 2>/dev/null
}
REV_CLAIMS="$(claims "${REV:-}")"
OUT_CLAIMS="$(claims "${OUT:-}")"
for want in benefits_caseworker tools_granted "${TENANT_G:-tenant_}"; do
  echo "$REV_CLAIMS" | grep -q "$want" \
    && ok "reviewer token carries $want" \
    || bad "reviewer token is MISSING $want - Cedar would deny verify_source at the gateway"
done
for unwanted in benefits_caseworker tools_granted tenant_; do
  echo "$OUT_CLAIMS" | grep -q "$unwanted" \
    && bad "outsider token carries $unwanted - the deny half of the proof is not testing anything" \
    || ok "outsider token does NOT carry $unwanted"
done

# ---- 5b. THE ben-fpb CHECK: minted through the client the GATEWAY trusts -------------------------
# fpb failed with the reviewer AND the outsider both getting "DENY insufficient_scope". Nothing about
# users or groups was wrong; the tokens came from a throwaway client, and gateway_stack.py allow-lists
# exactly one - customJWTAuthorizer.allowedClients = [identity.client.user_pool_client_id]. A token
# minted through any other client is refused before Cedar is consulted, so every caller looks denied
# and the deny-by-default check passes for entirely the wrong reason. Assert the issuing client on
# the token itself: this cannot prove the GATEWAY's allow-list from a throwaway pool, but it does
# prove the proof authenticates through the client it was handed, which is the half that broke.
for _pair in "reviewer:$REV_CLAIMS" "outsider:$OUT_CLAIMS"; do
  _who="${_pair%%:*}"; _cl="${_pair#*:}"
  if echo "$_cl" | grep -q "\"client_id\": *\"$AUTH_CLIENT\""; then
    ok "$_who token was minted through the intended client ($AUTH_CLIENT)"
  else
    bad "$_who token's client_id is NOT $AUTH_CLIENT - the gateway allow-lists one client and would refuse this -> $(echo "$_cl" | cut -c1-160)"
  fi
done

# ---- 6. teardown removes the users ---------------------------------------------------------------
for U in "$REV_U" "$OUT_U"; do
  aws cognito-idp admin-delete-user --user-pool-id "$POOL_ID" --username "$U" --region "$REGION" >/dev/null 2>&1 \
    || bad "could not delete proof user $U"
  aws cognito-idp admin-get-user --user-pool-id "$POOL_ID" --username "$U" --region "$REGION" >/dev/null 2>&1 \
    && bad "proof user $U survived deletion" || ok "proof user $U removed"
done

echo "=== SELFTEST: $pass passed, $fail failed ==="
[ "$fail" -eq 0 ] && { echo "PROOF AUTH SELFTEST: PASS"; exit 0; } || { echo "PROOF AUTH SELFTEST: FAIL"; exit 1; }
