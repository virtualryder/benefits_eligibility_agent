# Phase 111 — consolidated post-SaaS validation gate on release `v0.3.0-pilot-rc1` (2026-09-02) — **PASS**

**What this is.** ONE from-zero deployment of the release tag (env `mt4`: 8 stacks, two tenants `pha-a`/`pha-b`,
Bedrock model-invocation logging on, the AgentCore Runtime launched with `MULTITENANT=1`), on which the three
proofs ran back to back against the same live environment, followed by an end-to-end regression sweep for
unexpected errors; then torn down. Product tree: commit `8b804bea4a86` = tag `v0.3.0-pilot-rc1`
(the only uncommitted files at run time were the harness scripts `scripts/gate_111.py` and the
`--access-token` option of `scripts/pii_canary.py`, committed as `31ceb4a`; no product code differed).

## Verdict

| gate step | result | detail |
|---|---|---|
| 1. Isolation + per-tenant audit routing (`scripts/mt_two_tenant_proof.py`) | **PASS 12/12** in 86.5s | cw-a / cw-b allowed and routed only to their own sanitized store, ledger and WORM vault (base 0 writes); cw-none 0 tools + 403; token-verified ingest, workflow hop with the signed pair reached `HumanSignoff` writing INTENT evidence + pending approval to pha-a only; the same execution without the pair FAILED at the first state |
| 2. Full transparency through the real AgentCore Runtime (`scripts/obs_two_tenant_proof.py`) | **PASS 13/13 per tenant** in 255.6s | pha-a: 1 agent / 12 model / 12 tool spans, 33 gateway rows, 7 Lambda `aegis.call` lines (6 joined to the WORM record), 6 model invocations (all tenant-tagged, all joined to spans, masked-before-model True); pha-b: 1/10/12 spans, 33 gateway rows, 7 calls, 5 model invocations (masked True); other tenant's ledger empty for both |
| 3. Strict PII telemetry canary, workflow path (`scripts/pii_canary.py --strict --access-token`) | **PASS** in 159.4s | marker `CANARY-EBF9A0920674-TELEMETRYPROBE`: 0 hits in CloudWatch Logs (all `/aws/lambda/ben-mt4-*` + the gateway request log + the model-invocation log), X-Ray, DLQs and Step Functions history |
| 4. End-to-end regression sweep (`scripts/e2e_regression.py`) | **PASS — 0 unexpected** | 20 log groups swept for ERROR / Traceback / timeout / exception shapes; every Lambda group clean (0 error-shaped events), Lambda `Errors` metric 0 on every function, DLQs empty, no alarm in ALARM; every execution's terminal state explained (deliberate no-binding FAILED, harness ABORTED at sign-off, canary stopped before teardown) |

## What the sweep found and what was fixed (all harness / launch tooling; product code unchanged)

- The runtime logged `SSM gateway lookup failed (AccessDeniedException); falling back to GATEWAY_URL env`
  on every invocation. Two causes, both in the Git-Bash launch tooling: `_launch.sh` did not set
  `MSYS_NO_PATHCONV`, so the parameter NAME `/ben-mt4-eligibility/gateway-url` was rewritten to
  `C:/Program Files/Git/ben-mt4-eligibility/gateway-url` in the runtime's environment; and `_obs_setup.sh`
  granted `ssm:GetParameter` on the manifest's default path, not the deployment's. Both fixed, the runtime
  relaunched, and `gateway_url source=SSM param=/ben-mt4-eligibility/gateway-url` observed live. The
  fallback had kept every prior run working, which is exactly why a zero-warnings sweep is worth doing.
- Two `ERROR`-level lines are Node `DeprecationWarning`s from the AWS-provided CDK custom-resource
  provider framework (`url.parse()`), not failures; classified and reported, not hidden.

## Teardown

Runtime deleted; `cdk destroy --all` for `mt4` (all 8 stacks); the account's previous model-invocation
logging configuration re-applied and verified. Residual by design: the retained `ben-mt4*` audit
ledgers and per-tenant Object-Lock vaults.
