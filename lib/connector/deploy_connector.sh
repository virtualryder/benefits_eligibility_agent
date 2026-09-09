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

# ---- 4. Mock SoR Lambda + API Gateway HTTP API (OAuth-protected) ----
TOOL_ROLE_ARN="arn:aws:iam::$ACC:role/${P}-tool-exec"
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
      --role "$TOOL_ROLE_ARN" --handler lambda_function.handler --zip-file fileb://sor.zip \
      --timeout 15 --region "$REGION" 2>&1 >/dev/null)" && { CREATED=1; break; }
    case "$CREATE_ERR" in
      *"cannot be assumed"*|*InvalidParameterValueException*) sleep 5 ;;
      *) break ;;
    esac
  done
  if [ "$CREATED" -eq 1 ]; then log "created SoR Lambda $SOR_FN"
  else err "could not create SoR Lambda $SOR_FN (role $TOOL_ROLE_ARN): ${CREATE_ERR:-unknown}"; fi
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

# ---- 7. Connector exec role (Identity outbound perms) ----
printf '%s' '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' > lam-trust.json
if ! aws iam get-role --role-name "$CONN_ROLE" >/dev/null 2>&1; then
  aws iam create-role --role-name "$CONN_ROLE" --assume-role-policy-document file://lam-trust.json >/dev/null
  aws iam attach-role-policy --role-name "$CONN_ROLE" --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  log "created role $CONN_ROLE"
fi
printf '%s' '{"Version":"2012-10-17","Statement":[{"Sid":"Identity","Effect":"Allow","Action":["bedrock-agentcore:GetWorkloadAccessToken","bedrock-agentcore:GetResourceOauth2Token"],"Resource":"*"},{"Sid":"Secret","Effect":"Allow","Action":["secretsmanager:GetSecretValue"],"Resource":"*"}]}' > conn-perms.json
aws iam put-role-policy --role-name "$CONN_ROLE" --policy-name "${P}-connector-perms" --policy-document file://conn-perms.json
sleep 8

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
CONN_ROLE_ARN="arn:aws:iam::$ACC:role/$CONN_ROLE"
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
# Attaching the governed tool to the gateway IS the claim this connector exists to support, and
# on ben-fp5 it failed leaving no trace at all: both branches log only on success via `&&`, with
# no error path, so the script walked from "verify_source Lambda ready" straight to "DONE" and
# returned 0 with no target attached. Never let the load-bearing step be the quiet one.
if [ -n "$EXIST" ] && [ "$EXIST" != "None" ]; then
  TGT_ERR="$(aws bedrock-agentcore-control update-gateway-target --gateway-identifier "$GW_ID" --target-id "$EXIST" --name verify-source \
    --target-configuration file://vitarget.json --credential-provider-configurations file://cred.json --region "$REGION" 2>&1 >/dev/null)" \
    && log "updated target verify-source" || err "update-gateway-target failed on $GW_ID: ${TGT_ERR:-unknown}"
else
  TGT_ERR="$(aws bedrock-agentcore-control create-gateway-target --gateway-identifier "$GW_ID" --name verify-source \
    --target-configuration file://vitarget.json --credential-provider-configurations file://cred.json --region "$REGION" 2>&1 >/dev/null)" \
    && log "created target verify-source" || err "create-gateway-target failed on $GW_ID: ${TGT_ERR:-unknown}"
fi

cat > "$AGENT/connector-state.env" <<EOF
SOR_URL=$SOR_URL
PROVIDER=$PROVIDER
WI=$WI
M2M_ID=$M2M_ID
DOMAIN=$DOMAIN_PREFIX
SOR_LABEL=$SOR_LABEL
TOOL_ID=verify-source___verify_source
EOF
log "DONE. connector-state -> $AGENT/connector-state.env"
