#!/usr/bin/env bash
# destroy_connector.sh - REUSABLE. Remove everything deploy_connector.sh created.
#
# WHY THIS EXISTS
# ---------------
# deploy_connector.sh stands up nine things that CloudFormation does NOT own: a Cognito hosted
# domain, a resource server, an M2M app client, two Lambdas, an API Gateway HTTP API, an IAM role,
# an AgentCore Identity OAuth2 credential provider, a workload identity, and a gateway target.
#
# `cdk destroy` deletes none of them. Without this script a CONN-1 run would leave a live
# OAuth-protected API and a credential provider holding a client secret behind after teardown -
# which would break the platform's zero-residue claim in exactly the way L37 and the AgentCore
# residue check exist to prevent. The gate's teardown_zero_agentcore_residue check would catch the
# credential provider and the workload identity; nothing would have caught the API Gateway.
#
# Order matters: the gateway target references the Lambda, the credential provider holds the M2M
# client's secret, and the hosted domain must go before the pool is touched. Every step is
# idempotent and non-fatal, because a partial deploy must still be cleanable.
#
# Usage: bash lib/connector/destroy_connector.sh <agent_dir>
set -uo pipefail
export AWS_PAGER="" MSYS_NO_PATHCONV=1
AGENT_DIR="${1:?usage: destroy_connector.sh <agent_dir>}"
SELF="$(cd "$(dirname "$0")" && pwd)"; LIB="$(cd "$SELF/.." && pwd)"
AGENT="$(cd "$AGENT_DIR" && pwd)"; BUILD="$AGENT/.build"; mkdir -p "$BUILD"
( unset MSYS_NO_PATHCONV; python "$LIB/engine/render.py" "$AGENT/manifest.yaml" "$BUILD" >/dev/null 2>&1 || true )
source "$BUILD/agent.env"
[ -f "$AGENT/spine-state.env" ] && source "$AGENT/spine-state.env"
REGION="${REGION:-us-east-1}"; P="$PREFIX"

# Same GW_ID defect as deploy_connector.sh: spine-state carries GW_ARN, never GW_ID, so the
# gateway-target removal silently reported "absent" on every run. See the block in deploy.
GW_ID="${GW_ID:-${GW_ARN:-}}"; GW_ID="${GW_ID##*/}"

# THIS SCRIPT CERTIFIES ZERO RESIDUE, so it must never mistake "I could not look" for "nothing is
# there". On 2026-09-09 it was run in a shell where the aws CLI was not on PATH. Every CLI probe
# returned empty, every resource was logged "absent", and it printed CONNECTOR TEARDOWN: CLEAN
# while an OAuth-protected API Gateway, the verify_source Lambda and the connector IAM role were
# all still live - and it did so because each probe hides its own stderr with 2>/dev/null. Only the
# boto3 steps (credential provider, workload identity) actually worked, which is what exposed it.
# A teardown that cannot fail is worse than no teardown: it is a false all-clear on a credential.
command -v aws >/dev/null 2>&1 || {
  echo "[connector-destroy] FATAL: aws CLI not on PATH - cannot verify or remove connector resources"
  echo "CONNECTOR TEARDOWN: UNVERIFIED"; exit 1; }
LIBRT="$LIB/runtime"; PY="$LIBRT/.venv/Scripts/python.exe"; [ -f "$PY" ] || PY="$LIBRT/.venv/bin/python"
[ -f "$PY" ] || PY="python"
log(){ echo "[connector-destroy] $*"; }
gone=0; left=0
ok(){ log "removed $*"; gone=$((gone+1)); }
skip(){ log "absent   $*"; }
fail(){ log "LEFT     $* <- $2"; left=$((left+1)); }

DOMAIN_PREFIX="${P}-sor-${ACCOUNT:-}"
RS="${P}-sor"; PROVIDER="${P}-sor-oauth"; WI="${P}-verify-source-wi"
SOR_FN="${P}-sor-api"; VERIFY_FN="${P}-verify-source"; CONN_ROLE="${P}-connector-exec"; M2M_NAME="${P}-sor-m2m"

# ---- 1. gateway target first: it references the verify_source Lambda ----
if [ -n "${GW_ID:-}" ]; then
  TID="$(aws bedrock-agentcore-control list-gateway-targets --gateway-identifier "$GW_ID" --region "$REGION" \
        --query "items[?name=='verify-source'].targetId | [0]" --output text 2>/dev/null | tr -d '\r')"
  if [ -n "$TID" ] && [ "$TID" != "None" ]; then
    aws bedrock-agentcore-control delete-gateway-target --gateway-identifier "$GW_ID" --target-id "$TID" \
      --region "$REGION" >/dev/null 2>&1 && ok "gateway target verify-source" || fail "gateway target verify-source" "delete failed"
  else skip "gateway target verify-source"; fi
else skip "gateway target (no GW_ID in spine-state)"; fi

# ---- 2. API Gateway HTTP API ----
API_ID="$(aws apigatewayv2 get-apis --region "$REGION" --query "Items[?Name=='$SOR_FN'].ApiId | [0]" --output text 2>/dev/null | tr -d '\r')"
if [ -n "$API_ID" ] && [ "$API_ID" != "None" ]; then
  aws apigatewayv2 delete-api --api-id "$API_ID" --region "$REGION" >/dev/null 2>&1 && ok "http api $API_ID" || fail "http api $API_ID" "delete failed"
else skip "http api for $SOR_FN"; fi

# ---- 3. Lambdas ----
for FN in "$SOR_FN" "$VERIFY_FN"; do
  if aws lambda get-function --function-name "$FN" --region "$REGION" >/dev/null 2>&1; then
    aws lambda delete-function --function-name "$FN" --region "$REGION" >/dev/null 2>&1 && ok "lambda $FN" || fail "lambda $FN" "delete failed"
  else skip "lambda $FN"; fi
done

# ---- 4. AgentCore Identity: credential provider (holds the M2M client secret) + workload identity ----
# These two steps run through boto3, not the aws CLI, and their outcome must reach the counters:
# on 2026-09-09 they removed a credential provider and a workload identity while SUMMARY still
# said removed=0, because the heredoc only printed and never touched $gone or $left. A summary
# that under-reports its own removals is one edit away from over-reporting its own cleanliness.
# Exit code carries the verdict: 0 = nothing left behind, 1 = something could not be removed.
if "$PY" - "$PROVIDER" "$WI" "$REGION" <<'PYEOF'
import sys, boto3
provider, wi, region = sys.argv[1:4]
left = 0
c = boto3.client("bedrock-agentcore-control", region_name=region)
try:
    names = [p.get("name") for p in c.list_oauth2_credential_providers().get("credentialProviders", [])]
    if provider in names:
        c.delete_oauth2_credential_provider(name=provider)
        print("[connector-destroy] removed credential provider %s" % provider)
    else:
        print("[connector-destroy] absent   credential provider %s" % provider)
except Exception as exc:
    print("[connector-destroy] LEFT     credential provider %s <- %s" % (provider, str(exc)[:120]))
    left += 1
try:
    c.delete_workload_identity(name=wi)
    print("[connector-destroy] removed workload identity %s" % wi)
except Exception as exc:
    msg = str(exc)
    if "ResourceNotFound" in type(exc).__name__ or "not found" in msg.lower():
        print("[connector-destroy] absent   workload identity %s" % wi)
    else:
        print("[connector-destroy] LEFT     workload identity %s <- %s" % (wi, msg[:120]))
        left += 1
sys.exit(1 if left else 0)
PYEOF
then :; else left=$((left+1)); log "LEFT     one or more AgentCore Identity objects (see above)"; fi

# ---- 5. IAM role (inline policy first) ----
if aws iam get-role --role-name "$CONN_ROLE" >/dev/null 2>&1; then
  aws iam delete-role-policy --role-name "$CONN_ROLE" --policy-name "${P}-connector-perms" >/dev/null 2>&1 || true
  aws iam detach-role-policy --role-name "$CONN_ROLE" --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole >/dev/null 2>&1 || true
  aws iam delete-role --role-name "$CONN_ROLE" >/dev/null 2>&1 && ok "iam role $CONN_ROLE" || fail "iam role $CONN_ROLE" "delete failed"
else skip "iam role $CONN_ROLE"; fi

# ---- 6. Cognito: M2M client, resource server, hosted domain ----
if [ -n "${POOL_ID:-}" ]; then
  M2M_ID="$(aws cognito-idp list-user-pool-clients --user-pool-id "$POOL_ID" --region "$REGION" --max-results 60 \
    --query "UserPoolClients[?ClientName=='$M2M_NAME'].ClientId | [0]" --output text 2>/dev/null | tr -d '\r')"
  if [ -n "$M2M_ID" ] && [ "$M2M_ID" != "None" ]; then
    aws cognito-idp delete-user-pool-client --user-pool-id "$POOL_ID" --client-id "$M2M_ID" --region "$REGION" >/dev/null 2>&1 \
      && ok "m2m client $M2M_ID" || fail "m2m client $M2M_ID" "delete failed"
  else skip "m2m client $M2M_NAME"; fi
  aws cognito-idp delete-resource-server --user-pool-id "$POOL_ID" --identifier "$RS" --region "$REGION" >/dev/null 2>&1 \
    && ok "resource server $RS" || skip "resource server $RS"
  if aws cognito-idp describe-user-pool-domain --domain "$DOMAIN_PREFIX" --region "$REGION" \
       --query "DomainDescription.Domain" --output text 2>/dev/null | grep -q "$DOMAIN_PREFIX"; then
    aws cognito-idp delete-user-pool-domain --domain "$DOMAIN_PREFIX" --user-pool-id "$POOL_ID" --region "$REGION" >/dev/null 2>&1 \
      && ok "hosted domain $DOMAIN_PREFIX" || fail "hosted domain $DOMAIN_PREFIX" "delete failed"
  else skip "hosted domain $DOMAIN_PREFIX"; fi
else
  skip "cognito objects (no POOL_ID in spine-state; the pool stack may already be gone)"
fi

rm -f "$AGENT/connector-state.env"
echo "[connector-destroy] SUMMARY removed=$gone left=$left"
# Non-zero only when something was found and could NOT be removed. "Already absent" is a pass -
# teardown must be safe to run twice, and safe to run after a partial deploy.
[ "$left" -eq 0 ] && echo "CONNECTOR TEARDOWN: CLEAN" || { echo "CONNECTOR TEARDOWN: RESIDUE"; exit 1; }
