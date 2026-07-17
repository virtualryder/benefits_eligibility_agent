# demo_extra.sh (benefits-eligibility) — agent-specific payloads + content checks.
# Sourced by lib/engine/demo.sh; shares: REV, OUT, REV_U, call(), check(), pass, fail.
T_INTAKE="intake-application___intake_application"
T_MASK="mask-pii___mask_pii"
T_ASSESS="assess-eligibility___assess_eligibility"
T_DRAFT="ben-core___draft_notice"
T_AUDIT="write-audit___write_audit"
T_FINAL="ben-core___finalize_determination"

echo "  -- deny-by-default (identity -> Cedar) --"
check "caseworker intake_application" ALLOW "$(call "$REV" "$T_INTAKE" '{"application":"Applicant requests SNAP. Household size: 3. Monthly income: 2000."}')"
check "outsider   intake_application" DENY  "$(call "$OUT" "$T_INTAKE" '{"application":"Household size: 3. Monthly income: 2000."}')"

echo "  -- fail-closed PII de-identification (mask_pii) --"
MASK_OUT="$(call "$REV" "$T_MASK" '{"case":"Applicant John Smith, SSN 123-45-6789, 42 Main St, applied for SNAP; household of 3, monthly income 2000."}')"
check "caseworker mask_pii" ALLOW "$MASK_OUT"
if echo "$MASK_OUT" | grep -q 'REDACTED' && ! echo "$MASK_OUT" | grep -q 'John Smith'; then echo "  PASS | mask_pii redacted PII (name/SSN removed)"; pass=$((pass+1)); else echo "  FAIL | mask_pii did NOT redact -> $MASK_OUT"; fail=$((fail+1)); fi

echo "  -- forbid: mask-before-assess (eligibility) --"
check "caseworker assess (UN-masked)" DENY "$(call "$REV" "$T_ASSESS" '{"household_size":3,"monthly_income":2000,"deidentified":false}')"
ASSESS_OUT="$(call "$REV" "$T_ASSESS" '{"household_size":3,"monthly_income":2000,"liquid_resources":80,"deidentified":true}')"
check "caseworker assess (de-identified)" ALLOW "$ASSESS_OUT"
if echo "$ASSESS_OUT" | grep -q 'ELIGIBLE' && echo "$ASSESS_OUT" | grep -qE '"processing_clock"'; then echo "  PASS | assess_eligibility returned a determination + processing clock"; pass=$((pass+1)); else echo "  FAIL | assess -> $ASSESS_OUT"; fail=$((fail+1)); fi

echo "  -- forbid: mask-before-model (notice) --"
check "caseworker draft (UN-masked)" DENY "$(call "$REV" "$T_DRAFT" '{"case":"x","deidentified":false}')"
DRAFT_OUT="$(call "$REV" "$T_DRAFT" '{"case":"De-identified applicant [REDACTED:NAME], household of 3, gross monthly income 2000. Determination: ELIGIBLE (within 130% FPL), standard 30-day processing.","deidentified":true}')"
check "caseworker draft (de-identified)" ALLOW "$DRAFT_OUT"
if echo "$DRAFT_OUT" | grep -qE '"chars": *[1-9]' && ! echo "$DRAFT_OUT" | grep -q '"error"'; then echo "  PASS | draft_notice produced a real Bedrock notice"; pass=$((pass+1)); else echo "  FAIL | draft -> $DRAFT_OUT"; fail=$((fail+1)); fi
if echo "$DRAFT_OUT" | grep -q '"guardrail_applied": *true'; then echo "  PASS | notice passed the fail-closed guardrail"; pass=$((pass+1)); else echo "  FAIL | guardrail not applied -> $DRAFT_OUT"; fail=$((fail+1)); fi

echo "  -- immutable WORM audit --"
NONCE="$RANDOM$RANDOM"
AUDIT_IN="{\"icsr_id\":\"CASE-2026-0002\",\"action\":\"determination\",\"phase\":\"INTENT\",\"actor\":\"$REV_U\",\"payload\":\"run-$NONCE\"}"
A1="$(call "$REV" "$T_AUDIT" "$AUDIT_IN")"
check "caseworker write_audit (1st)" ALLOW "$A1"
if echo "$A1" | grep -q '"stored": *true' && echo "$A1" | grep -q '"worm": *true'; then echo "  PASS | audit -> append-only ledger + WORM"; pass=$((pass+1)); else echo "  FAIL | audit not stored/worm -> $A1"; fail=$((fail+1)); fi
A2="$(call "$REV" "$T_AUDIT" "$AUDIT_IN")"
if echo "$A2" | grep -q '"stored": *false' && echo "$A2" | grep -qi 'append-only'; then echo "  PASS | duplicate rejected (immutable)"; pass=$((pass+1)); else echo "  FAIL | dup not rejected -> $A2"; fail=$((fail+1)); fi

echo "  -- forbid: no self-commit --"
check "caseworker finalize_determination" DENY "$(call "$REV" "$T_FINAL" '{"case_id":"CASE-2026-0002"}')"
