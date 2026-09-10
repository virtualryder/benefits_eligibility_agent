#!/usr/bin/env bash
# deploy_connector.sh — REUSABLE. Stand up a REAL OAuth2-protected system of record + a governed
# verify_source connector that authenticates to it via AgentCore Identity OUTBOUND auth
# (client_credentials / M2M), for ANY agent. Prefix-parameterized from the manifest.
# Usage: bash lib/connector/deploy_connector.sh <agent_dir> ["SOR label"]
# 2026-09-09 (CONN-1). This was `set -uo pipefail` - no -e - and every step swallows its own
# failure with `|| true` or `|| log`, so the script returned 0 whether it created nine resources or
# none. On the ben-fp3 run it returned 0 having created NOTHING, because it had sourced a five-week-
# old spine-state naming a pool and gateway that no longer existed. A deploy script that cannot
# report failure is not a deploy script, it is a wish. The gate now verifies artifacts rather than
# this exit code, and `err` below makes the script itself honest about the steps that matter.
set -uo pipefail
FAILED=0
err(){ echo "[connector] ERROR: $*" >&2; FAILED=1; }
trap 'if [ "$FAILED" -ne 0 ]; then echo "[connector] DEPLOY INCOMPLETE - see ERROR lines above"; exit 1; fi' EXIT
export AWS_PAGER="" MSYS_NO_PATHCONV=1
AGENT_DIR="${1:?usage: deploy_connector.sh <agent_dir> [sor_label]}"
SOR_LABEL="${2:-MOCK-SOR}"
SELF="$(cd "$(dirname "$0")" && pwd)"                    # .../lib/connector
LIB="$(cd "$SELF/.." && pwd)"                            # .../lib
AGENT="$(cd "$AGENT_DIR" && pwd)"; LIBRT="$LIB/runtime"
BUILD="$AGENT/.build"; mkdir -p "$BUILD"
( unset MSYS_NO_PATHCONV; python "$LIB/engine/render.py" "$AGENT/manifest.yaml" "$BUILD" >/dev/null )
source "$BUILD/agent.env"                                # PREFIX
source "$AGENT/spine-state.env"                          # REGION, ACCOUNT, POOL_ID, GW_ARN, GW_URL
REGION="${REGION:-us-east-1}"; ACC="${ACCOUNT:?}"
# CONN-1 (2026-09-09, ben-fp5): every resource the CDK builds is env-scoped ("ben-fp5-..."), but
# this script used agent.env's PREFIX ("ben"). So it looked for the tool-execution role at
# "ben-tool-exec" when the real one is "ben-fp5-tool-exec", `create-function` failed into
# >/dev/null, the SoR Lambda was never created, and the API in front of it answered the
# unauthenticated probe with 500 instead of refusing it. The hosted domain was likewise shared
# across environments, so fp5 "reused" fp4's - still bound to fp4's dead pool, which that same
# live domain had prevented from being deleted. The gate passes CONN_PREFIX; standalone runs
# fall back to PREFIX.
P="${CONN_PREFIX:-$PREFIX}"

# CONN-1 ROOT CAUSE, found on the 2026-09-09 ben-fp4 live run.
# This script referenced $GW_ID at step 9, but spine-state.env has only ever carried GW_ARN and
# GW_URL - never GW_ID. Under `set -u` an unbound variable is fatal, so bash aborted the instant it
# reached the gateway-target call: the run died right after "verify_source Lambda ready" with EIGHT
# of nine resources live, no connector-state.env written, and no error text a reader could act on.
# The comment on the line above used to claim spine-state supplied GW_ID. It never did, on any
# commit - which is why CONN_governed_sor_proof had never once run to completion.
# The gateway id is the last path segment of the ARN; `##*/` is a no-op on a bare id.
GW_ID="${GW_ID:-${GW_ARN:-}}"; GW_ID="${GW_ID##*/}"
[ -n "$GW_ID" ] || err "neither GW_ID nor GW_ARN in $AGENT/spine-state.env - cannot attach the gateway target"

# Every step below uses the aws CLI. If it is not on PATH each call fails, `2>/dev/null` hides the
# reason, and an empty result reads as "already exists" or "absent" - the exact defect that made
# destroy_connector.sh certify CONNECTOR TEARDOWN: CLEAN over live resources on 2026-09-09.
command -v aws >/dev/null 2>&1 || { echo "[connector] FATAL: aws CLI not on PATH - refusing to run"; exit 1; }
PY="$LIBRT/.venv/Scripts/python.exe"; [ -f "$PY" ] || PY="$LIBRT/.venv/bin/python"
log(){ echo "[connector] $*"; }
log "prefix=$P (CONN_PREFIX=${CONN_PREFIX:-<unset, falling back to agent.env PREFIX>})"
WORK="$SELF/.work"; rm -rf "$WORK"; mkdir -p "$WORK"; cd "$WORK"

DOMAIN_PREFIX="${P}-sor-$ACC"
ISSUER="https://cognito-idp.$REGION.amazonaws.com/$POOL_ID"
TOKEN_EP="https://$DOMAIN_PREFIX.auth.$REGION.amazoncognito.com/oauth2/token"
AUTH_EP="https://$DOMAIN_PREFIX.auth.$REGION.amazoncognito.com/oauth2/authorize"
RS="${P}-sor"; SCOPE="${P}-sor/read"; PROVIDER="${P}-sor-oauth"; WI="${P}-verify-source-wi"
SOR_FN="${P}-sor-api"; VERIFY_FN="${P}-verify-source"; CONN_ROLE="${P}-connector-exec"; M2M_NAME="${P}-sor-m2m"

# ---- 1. Cognito hosted domain ----
if ! aws cognito-idp describe-user-pool-domain --domain "$DOMAIN_PREFIX" --region "$REGION" --query "DomainDescription.Domain" --output text 2>/dev/null | grep -q "$DOMAIN_PREFIX"; then
  aws cognito-idp create-user-pool-domain --domain "$DOMAIN_PREFIX" --user-pool-id "$POOL_ID" --region "$REGION" >/dev/null && log "created hosted domain $DOMAIN_PREFIX"
else log "reusing hosted domain $DOMAIN_PREFIX"; fi

# ---- 2. Resource server + scope ----
aws cognito-idp create-resource-server --user-pool-id "$POOL_ID" --identifier "$RS" --name "$RS" \
  --scopes ScopeName=read,ScopeDescription="read verification" --region "$REGION" >/dev/null 2>&1 \
  && log "created resource server $SCOPE" || log "resource server $RS exists"

# ---- 3. M2M app client ----
M2M_ID="$(aws cognito-idp list-user-pool-clients --user-pool-id "$POOL_ID" --region "$REGION" --max-results 60 \
  --query "UserPoolClients[?ClientName=='$M2M_NAME'].ClientId | [0]" --output text | tr -d '\r')"
if [ -z "$M2M_ID" ] || [ "$M2M_ID" = "None" ]; then
  M2M_ID="$(aws cognito-idp create-user-pool-client --user-pool-id "$POOL_ID" --client-name "$M2M_NAME" \
    --generate-secret --allowed-o-auth-flows client_credentials --allowed-o-auth-scopes "$SCOPE" \
    --allowed-o-auth-flows-user-pool-client --region "$REGION" --query "UserPoolClient.ClientId" --output text | tr -d '\r')"
  log "created M2M client $M2M_ID"
else log "reusing M2M client $M2M_ID"; fi
M2M_SECRET="$(aws cognito-idp describe-user-pool-client --user-pool-id "$POOL_ID" --client-id "$M2M_ID" --region "$REGION" --query "UserPoolClient.ClientSecret" --output text | tr -d '\r')"

# ---- 3c. Proof authentication: NO throwaway client. ben-fpb proved that road is closed: a test client with USER_PASSWORD_AUTH
# minted tokens perfectly and the gateway rejected every one, denying the REVIEWER and the OUTSIDER
# with the same "insufficient_scope". gateway_stack.py's customJWTAuthorizer carries
# allowedClients = [identity.client.user_pool_client_id] - an allow-list of exactly one. Admitting a
# test client meant editing the PRODUCTION authorizer, which is a worse compromise than the one the
# throwaway client existed to avoid. The proof now authenticates by SRP through the shipped client,
# as cedar_perimeter_proof.py and mt_two_tenant_proof.py always have. See mint_token.py.
log "proof auth: SRP through the shipped GatewayClient $CLIENT_ID (no test-only client is created)"

# ---- 3c-2. Proof USERS. Root cause of the ben-fpa failure, and MEASURED rather than assumed: a
# synth of the identity stack carries UserPool=1, UserPoolClient=1, UserPoolGroup=4 and ZERO
# AWS::Cognito::UserPoolUser resources. users.tsv is rendered from the manifest and is only ever
# pushed into a pool by lib/engine/deploy_identity.sh, which belongs to the hand-built spine path and
# never runs in a CDK environment. So the proof was authenticating two identities that had never
# existed in that pool. fp8's "USER_PASSWORD_AUTH flow not enabled" was Cognito rejecting on the
# client's allowed flows BEFORE it ever looked up the user, which is what hid this second layer.
# Every other live proof (cedar_perimeter_proof.py, mt_two_tenant_proof.py) creates its own users and
# removes them; this now does the same. Groups follow the policy set exactly: caseworker_permit needs
# benefits_caseworker, require_entitlement needs tools_granted, require_tenant needs a tenant_*
# group. The outsider gets NONE of them - that absence is what makes the deny half of the proof real,
# so it must never be "fixed" by granting the outsider anything.
UTSV="$BUILD/users.tsv"
[ -f "$UTSV" ] || err "no users.tsv at $UTSV - cannot create the proof users"
PROOF_REV_U="$(awk -F'\t' '$3=="yes"{print $1; exit}' "$UTSV" | tr -d '\r')"
PROOF_REV_P="$(awk -F'\t' '$3=="yes"{print $2; exit}' "$UTSV" | tr -d '\r')"
PROOF_OUT_U="$(awk -F'\t' '$3=="no"{print $1; exit}' "$UTSV" | tr -d '\r')"
PROOF_OUT_P="$(awk -F'\t' '$3=="no"{print $2; exit}' "$UTSV" | tr -d '\r')"
[ -n "$PROOF_REV_U" ] && [ -n "$PROOF_OUT_U" ] \
  || err "users.tsv at $UTSV has no in-group (yes) and out-of-group (no) rows"
# Read the tenant group off the LIVE pool instead of hardcoding one: the group is env-scoped
# (tenant_sp-a in the full-portfolio envs, tenant_a elsewhere) and a name invented here would fail
# closed at require_tenant with no clue why. Empty is legitimate - a silo deployment attaches no
# require_tenant policy and has no tenant_* group to join.
TENANT_G="$(aws cognito-idp list-groups --user-pool-id "$POOL_ID" --region "$REGION" \
  --query "Groups[?starts_with(GroupName,'tenant_')].GroupName | [0]" --output text 2>/dev/null | tr -d '\r')"
[ "$TENANT_G" = "None" ] && TENANT_G=""
mkuser(){   # $1=username  $2=password  $3=space-separated groups (may be empty)
  # admin-create-user is allowed to fail quietly ONLY because UsernameExistsException is the normal
  # re-run case and the very next call is a hard check: if the user genuinely does not exist,
  # admin-set-user-password fails and says so. The check that can fail is downstream of the one that
  # is allowed to - that ordering is the whole point, and is what 2>/dev/null must never hide.
  aws cognito-idp admin-create-user --user-pool-id "$POOL_ID" --username "$1" \
    --message-action SUPPRESS --region "$REGION" >/dev/null 2>&1
  UERR="$(aws cognito-idp admin-set-user-password --user-pool-id "$POOL_ID" --username "$1" \
          --password "$2" --permanent --region "$REGION" 2>&1 >/dev/null)" \
    || { err "could not set a permanent password for proof user $1: ${UERR:-unknown}"; return 1; }
  for g in $3; do
    GERR="$(aws cognito-idp admin-add-user-to-group --user-pool-id "$POOL_ID" --username "$1" \
            --group-name "$g" --region "$REGION" 2>&1 >/dev/null)" \
      || err "could not add proof user $1 to group $g: ${GERR:-unknown}"
  done
  log "proof user $1 ready (groups: ${3:-<none, by design>})"
}
mkuser "$PROOF_REV_U" "$PROOF_REV_P" "benefits_caseworker tools_granted${TENANT_G:+ $TENANT_G}"
mkuser "$PROOF_OUT_U" "$PROOF_OUT_P" ""

# Smoke-test the auth path HERE, where a failure is attributable to the deploy, instead of letting it
# surface three steps later as a proof failure with no cause attached. This is the exact call that
# died on ben-fpa; if it cannot mint now, CONN_deploy says so in AWS's own words.
MINT_PY=""
for CAND in "$PY" "$LIBRT/.venv/Scripts/python.exe" "$LIBRT/.venv/bin/python" python; do
  if [ -n "$CAND" ] && { [ -f "$CAND" ] || command -v "$CAND" >/dev/null 2>&1; }; then
    "$CAND" -c 'import pycognito' >/dev/null 2>&1 && { MINT_PY="$CAND"; break; }
  fi
done
# Git-Bash /c/Users/... paths reach a Windows python.exe verbatim under MSYS_NO_PATHCONV and resolve
# to C:\c\Users\... - caught by selftest_proof_auth.sh on 2026-09-10, not by a live run.
MINT_SCRIPT="$SELF/mint_token.py"
command -v cygpath >/dev/null 2>&1 && MINT_SCRIPT="$(cygpath -w "$MINT_SCRIPT")"
if [ -z "$MINT_PY" ]; then
  err "no interpreter here can import pycognito, so the proof cannot do SRP - install it or the proof will fail"
else
  for _pu in "$PROOF_REV_U:$PROOF_REV_P" "$PROOF_OUT_U:$PROOF_OUT_P"; do
    _u="${_pu%%:*}"; _p="${_pu#*:}"
    MERR="$("$MINT_PY" "$MINT_SCRIPT" "$POOL_ID" "$CLIENT_ID" "$REGION" "$_u" "$_p" 2>&1 | tr -d '\r')"
    if [ $? -ne 0 ] || [ -z "$MERR" ]; then
      err "proof user $_u cannot mint a token by SRP via the shipped client $CLIENT_ID: ${MERR:-<no output>}"
    else log "proof user $_u mints a token by SRP OK"; fi
  done
  unset MERR _pu _u _p
fi

# ---- 3b. Connector exec role. MOVED AHEAD OF THE LAMBDAS ON PURPOSE (2026-09-09, ben-fp6).
# The SoR Lambda used to be created with $TOOL_ROLE_ARN ("<prefix>-tool-exec"), which is the
# AGENTCORE TOOL execution role: it trusts bedrock-agentcore, not Lambda. AWS said so plainly once
# the error path existed - "The role defined for the function cannot be assumed by Lambda" - and no
# amount of retrying fixes a trust policy. This role already trusts lambda.amazonaws.com and was
# built for exactly this; it was simply created at step 7, three steps AFTER the Lambda that needed
# it. Both Lambdas now use it.
printf '%s' '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' > lam-trust.json
if ! aws iam get-role --role-name "$CONN_ROLE" >/dev/null 2>&1; then
  aws iam create-role --role-name "$CONN_ROLE" --assume-role-policy-document file://lam-trust.json >/dev/null \
    || err "could not create role $CONN_ROLE"
  aws iam attach-role-policy --role-name "$CONN_ROLE" --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  log "created role $CONN_ROLE"
fi
printf '%s' '{"Version":"2012-10-17","Statement":[{"Sid":"Identity","Effect":"Allow","Action":["bedrock-agentcore:GetWorkloadAccessToken","bedrock-agentcore:GetResourceOauth2Token"],"Resource":"*"},{"Sid":"Secret","Effect":"Allow","Action":["secretsmanager:GetSecretValue"],"Resource":"*"}]}' > conn-perms.json
aws iam put-role-policy --role-name "$CONN_ROLE" --policy-name "${P}-connector-perms" --policy-document file://conn-perms.json
CONN_ROLE_ARN="arn:aws:iam::$ACC:role/$CONN_ROLE"
sleep 8

# ---- 4. Mock SoR Lambda + API Gateway HTTP API (OAuth-protected) ----
cp "$SELF/sor_api.py" lambda_function.py
"$PY" -c "import zipfile;z=zipfile.ZipFile('sor.zip','w',zipfile.ZIP_DEFLATED);z.write('lambda_function.py');z.close()"
if aws lambda get-function --function-name "$SOR_FN" --region "$REGION" >/dev/null 2>&1; then
  aws lambda update-function-code --function-name "$SOR_FN" --zip-file fileb://sor.zip --region "$REGION" >/dev/null
else
  # This create used to end in `>/dev/null` with no error path. On ben-fp5 it failed - the role
  # ARN was wrong - and the failure vanished: no Lambda, an API Gateway proxying to nothing, and
  # a 500 on every request that the gate had to infer backwards from. Retry for IAM propagation
  # (a freshly created role is not immediately assumable by Lambda), then report honestly.
  CREATED=0
  for attempt in 1 2 3 4 5 6; do
    CREATE_ERR="$(aws lambda create-function --function-name "$SOR_FN" --runtime python3.12 \
      --role "$CONN_ROLE_ARN" --handler lambda_function.handler --zip-file fileb://sor.zip \
      --timeout 15 --region "$REGION" 2>&1 >/dev/null)" && { CREATED=1; break; }
    case "$CREATE_ERR" in
      *"cannot be assumed"*|*InvalidParameterValueException*) sleep 5 ;;
      *) break ;;
    esac
  done
  if [ "$CREATED" -eq 1 ]; then log "created SoR Lambda $SOR_FN"
  else err "could not create SoR Lambda $SOR_FN (role $CONN_ROLE_ARN): ${CREATE_ERR:-unknown}"; fi
fi
for i in 1 2 3 4 5 6; do aws lambda update-function-configuration --function-name "$SOR_FN" \
  --environment "Variables={EXPECTED_ISS=$ISSUER,EXPECTED_CLIENT_ID=$M2M_ID,REQUIRED_SCOPE=$SCOPE,SOR_LABEL=$SOR_LABEL}" --region "$REGION" >/dev/null 2>&1 && break; sleep 4; done
SOR_LARN="arn:aws:lambda:$REGION:$ACC:function:$SOR_FN"
API_ID="$(aws apigatewayv2 get-apis --region "$REGION" --query "Items[?Name=='$SOR_FN'].ApiId | [0]" --output text | tr -d '\r')"
if [ -z "$API_ID" ] || [ "$API_ID" = "None" ]; then
  API_ID="$(aws apigatewayv2 create-api --name "$SOR_FN" --protocol-type HTTP --target "$SOR_LARN" --region "$REGION" --query ApiId --output text | tr -d '\r')"
  aws lambda add-permission --function-name "$SOR_FN" --statement-id apigw-invoke --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:$REGION:$ACC:$API_ID/*" --region "$REGION" >/dev/null 2>&1 || true
fi
[ -n "$API_ID" ] && [ "$API_ID" != "None" ] || err "no API id for $SOR_FN"
SOR_URL="https://$API_ID.execute-api.$REGION.amazonaws.com/"
log "mock SoR ($SOR_LABEL, OAuth-protected, API Gateway) at $SOR_URL"

# ---- 5. AgentCore Identity OAuth2 credential provider ----
"$PY" - "$PROVIDER" "$ISSUER" "$AUTH_EP" "$TOKEN_EP" "$M2M_ID" "$M2M_SECRET" "$REGION" <<'PYEOF'
import sys, boto3
name, issuer, auth_ep, token_ep, cid, csec, region = sys.argv[1:8]
c = boto3.client("bedrock-agentcore-control", region_name=region)
for p in c.list_oauth2_credential_providers().get("credentialProviders", []):
    if p.get("name") == name:
        c.delete_oauth2_credential_provider(name=name); print("[connector] deleted existing provider", name)
cfg = {"customOauth2ProviderConfig": {
    "oauthDiscovery": {"authorizationServerMetadata": {
        "issuer": issuer, "authorizationEndpoint": auth_ep, "tokenEndpoint": token_ep, "responseTypes": ["token"]}},
    "clientId": cid, "clientSecret": csec, "clientAuthenticationMethod": "CLIENT_SECRET_BASIC"}}
r = c.create_oauth2_credential_provider(name=name, credentialProviderVendor="CustomOauth2", oauth2ProviderConfigInput=cfg)
print("[connector] credential provider:", r["credentialProviderArn"])
PYEOF

# ---- 6. Workload identity ----
"$PY" - "$WI" "$REGION" <<'PYEOF'
import sys, boto3
name, region = sys.argv[1:3]
c = boto3.client("bedrock-agentcore-control", region_name=region)
try:
    r = c.create_workload_identity(name=name); print("[connector] workload identity:", r["workloadIdentityArn"])
except Exception as e:
    if "Conflict" in type(e).__name__ or "exist" in str(e).lower(): print("[connector] workload identity exists:", name)
    else: raise
PYEOF

# ---- 8. verify_source Lambda (bundled boto3 for the bedrock-agentcore client) ----
rm -rf pkg && mkdir pkg
cp "$SELF/verify_source.py" pkg/lambda_function.py
"$PY" -m pip install -q -t pkg boto3==1.43.50 2>&1 | tail -1 || true
find pkg/botocore/data -mindepth 1 -maxdepth 1 -type d ! -name 'bedrock-agentcore*' ! -name 'sts' -exec rm -rf {} + 2>/dev/null || true
"$PY" - <<'PYZIP'
import zipfile, os
z = zipfile.ZipFile('vi.zip', 'w', zipfile.ZIP_DEFLATED)
for root, _, files in os.walk('pkg'):
    for f in files:
        fp = os.path.join(root, f); z.write(fp, os.path.relpath(fp, 'pkg'))
z.close()
PYZIP
if aws lambda get-function --function-name "$VERIFY_FN" --region "$REGION" >/dev/null 2>&1; then
  aws lambda update-function-code --function-name "$VERIFY_FN" --zip-file fileb://vi.zip --region "$REGION" >/dev/null
else
  aws lambda create-function --function-name "$VERIFY_FN" --runtime python3.12 --role "$CONN_ROLE_ARN" \
    --handler lambda_function.handler --zip-file fileb://vi.zip --timeout 30 --region "$REGION" >/dev/null
fi
for i in 1 2 3 4 5 6; do aws lambda update-function-configuration --function-name "$VERIFY_FN" \
  --environment "Variables={SOR_URL=$SOR_URL,PROVIDER_NAME=$PROVIDER,WI_NAME=$WI,SCOPE=$SCOPE}" --region "$REGION" >/dev/null 2>&1 && break; sleep 4; done
aws lambda get-function --function-name "$VERIFY_FN" --region "$REGION" >/dev/null 2>&1 \
  || err "verify_source Lambda $VERIFY_FN does not exist after create/update"
log "verify_source Lambda ready"

# ---- 9. Add the governed tool as a Gateway target on the LIVE gateway ----
printf '%s' '[{"credentialProviderType":"GATEWAY_IAM_ROLE"}]' > cred.json
cat > vitarget.json <<JSON
{"mcp":{"lambda":{"lambdaArn":"arn:aws:lambda:$REGION:$ACC:function:$VERIFY_FN","toolSchema":{"inlinePayload":[{"name":"verify_source","description":"Verify a case against an OAuth2-protected external system of record. The outbound OAuth token is minted by AgentCore Identity (client_credentials/M2M); this tool holds no secret. Non-consequential; Cedar-authorized like every tool.","inputSchema":{"type":"object","properties":{"case_id":{"type":"string","description":"Case id to verify."}},"required":[]}}]}}}}
JSON
EXIST="$(aws bedrock-agentcore-control list-gateway-targets --gateway-identifier "$GW_ID" --region "$REGION" --query "items[?name=='verify-source'].targetId | [0]" --output text 2>/dev/null | tr -d '\r')"
# The gateway's own execution role must be allowed to invoke the tool Lambda. On ben-fp6 it was
# not, and AWS said exactly that once the error path existed: "Gateway execution role lacks
# permission to invoke Lambda function ...:ben-fp6-verify-source. Update the permission and retry."
# Nothing in this script had ever granted it. Read the role off the LIVE gateway rather than
# guessing its name from a prefix - the gateway is the artifact, the naming convention is a belief.
GW_ROLE_ARN="$(aws bedrock-agentcore-control get-gateway --gateway-identifier "$GW_ID" --region "$REGION" --query roleArn --output text 2>/dev/null | tr -d '\r')"
if [ -n "$GW_ROLE_ARN" ] && [ "$GW_ROLE_ARN" != "None" ]; then
  GW_ROLE_NAME="${GW_ROLE_ARN##*/}"
  printf '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"lambda:InvokeFunction","Resource":"arn:aws:lambda:%s:%s:function:%s"}]}' \
    "$REGION" "$ACC" "$VERIFY_FN" > gw-invoke.json
  aws iam put-role-policy --role-name "$GW_ROLE_NAME" --policy-name "${P}-gw-invoke-verify" \
    --policy-document file://gw-invoke.json >/dev/null 2>&1 \
    && log "granted $GW_ROLE_NAME lambda:InvokeFunction on $VERIFY_FN" \
    || err "could not grant $GW_ROLE_NAME permission to invoke $VERIFY_FN"
  sleep 10   # IAM propagation; the target call below fails closed if this was not enough
else
  err "could not read roleArn from gateway $GW_ID - cannot grant invoke permission"
fi

# Attaching the governed tool to the gateway IS the claim this connector exists to support, and
# on ben-fp5 it failed leaving no trace at all: both branches log only on success via `&&`, with
# no error path, so the script walked from "verify_source Lambda ready" straight to "DONE" and
# returned 0 with no target attached. Never let the load-bearing step be the quiet one.
if [ -n "$EXIST" ] && [ "$EXIST" != "None" ]; then
  TGT_ERR="$(aws bedrock-agentcore-control update-gateway-target --gateway-identifier "$GW_ID" --target-id "$EXIST" --name verify-source \
    --target-configuration file://vitarget.json --credential-provider-configurations file://cred.json --region "$REGION" 2>&1 >/dev/null)" \
    && log "updated target verify-source" || err "update-gateway-target failed on $GW_ID: ${TGT_ERR:-unknown}"
else
  TGT_OK=0
  for attempt in 1 2 3 4 5 6; do
    TGT_ERR="$(aws bedrock-agentcore-control create-gateway-target --gateway-identifier "$GW_ID" --name verify-source \
      --target-configuration file://vitarget.json --credential-provider-configurations file://cred.json --region "$REGION" 2>&1 >/dev/null)" \
      && { TGT_OK=1; break; }
    # Only the IAM-propagation shape is worth retrying; anything else is a real defect.
    case "$TGT_ERR" in *"lacks permission"*|*"not authorized"*) sleep 10 ;; *) break ;; esac
  done
  [ "$TGT_OK" -eq 1 ] && log "created target verify-source" \
    || err "create-gateway-target failed on $GW_ID: ${TGT_ERR:-unknown}"
fi

# ---- 10. Smoke-test the OUTBOUND leg, here, where a failure is attributable to the deploy.
# ben-fpc was the first run ever to get a governed caller through Cedar and into this tool: the
# gateway said ALLOW and the tool answered {"verified":false,"error":"system-of-record returned
# HTTP 401"}. That message names a symptom with five possible causes in sor_api.py and
# distinguishes none of them, so twenty minutes of live deploy bought one string the response had
# already contained. Invoking the tool directly puts the SoR's OWN words into CONN_deploy.
INV_OUT="$WORK/verify-invoke.json"
if aws lambda invoke --function-name "$VERIFY_FN" --region "$REGION" \
     --cli-binary-format raw-in-base64-out --payload '{"case_id":"CASE-1"}' "$INV_OUT" >/dev/null 2>&1; then
  INV="$(tr -d '\r\n' < "$INV_OUT" 2>/dev/null)"
  case "$INV" in
    *'"verified": true'*|*'"verified":true'*)
      log "outbound leg OK: verify_source verified CASE-1 against the OAuth-protected SoR" ;;
    *)
      err "outbound leg FAILED - the tool reached the SoR and was refused: $(printf '%s' "$INV" | cut -c1-600)" ;;
  esac
else
  err "could not invoke $VERIFY_FN to smoke-test the outbound leg"
fi

# EVERY value is quoted. SOR_LABEL is "MOCK-SOR (OAuth2, RS256/JWKS)" - spaces and parentheses -
# and unquoted it made `source connector-state.env` a bash syntax error, which is what actually
# killed the fp8 proof ("syntax error near unexpected token `('", then SOR_LABEL: unbound variable).
# A state file that cannot be sourced is worse than no state file: it fails at the reader, not here.
cat > "$AGENT/connector-state.env" <<EOF
SOR_URL="$SOR_URL"
PROVIDER="$PROVIDER"
WI="$WI"
M2M_ID="$M2M_ID"
PROOF_REV_U="${PROOF_REV_U:-}"
PROOF_OUT_U="${PROOF_OUT_U:-}"
DOMAIN="$DOMAIN_PREFIX"
SOR_LABEL="$SOR_LABEL"
TOOL_ID="verify-source___verify_source"
EOF
log "DONE. connector-state -> $AGENT/connector-state.env"
