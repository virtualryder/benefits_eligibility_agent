#!/usr/bin/env bash
# One-off: invoke the deployed benefits Runtime as a caseworker WITH real application data, to show
# the full governed workflow end to end. Usage: bash invoke_demo.sh
SELF="$(cd "$(dirname "$0")" && pwd)"
export MSYS_NO_PATHCONV=1 PYTHONIOENCODING=utf-8 PYTHONUTF8=1 AWS_REGION=us-east-1 AWS_PAGER=""
AGENT="$SELF/agents/benefits-eligibility"; RT="$SELF/lib/runtime"
source "$AGENT/spine-state.env"
if [ -f "$RT/.venv/Scripts/agentcore.exe" ]; then AC="$RT/.venv/Scripts/agentcore.exe"; PY="$RT/.venv/Scripts/python.exe"; else AC="$RT/.venv/bin/agentcore"; PY="$RT/.venv/bin/python"; fi
TOK="$(aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id "$CLIENT_ID" \
  --auth-parameters "USERNAME=caseworker,PASSWORD=${PV_REVIEWER_PW:-ChangeMe-Reviewer1!}" --region us-east-1 \
  --query 'AuthenticationResult.AccessToken' --output text | tr -d '\r')"
APP="Applicant Jane Doe, SSN 555-12-3456, 10 Oak Ave. Applying for SNAP. Household size 4. Monthly income 2500. Savings 60."
PROMPT="Process this benefits application for case CASE-2026-0700. Raw application text: $APP  Run the full governed workflow end to end (intake_application, mask_pii, assess_eligibility, draft_notice, write_audit, request_signoff) and request caseworker sign-off with case id CASE-2026-0700 and requester caseworker."
PAYLOAD="$("$PY" -c "import json,sys;print(json.dumps({'access_token':sys.argv[1],'case_id':'CASE-2026-0700','requester':'caseworker','prompt':sys.argv[2]}))" "$TOK" "$PROMPT")"
cd "$RT"
"$AC" invoke --bearer-token "$TOK" "$PAYLOAD" 2>&1
echo "INVOKE_EXIT=${PIPESTATUS[0]}"
