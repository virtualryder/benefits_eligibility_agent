# Public Benefits Intake, Eligibility Screening & Caseworker Decision-Support Assistant

*Governed Agentic AI on Amazon Bedrock AgentCore*

[![CI](https://github.com/virtualryder/benefits_eligibility_agent/actions/workflows/ci.yml/badge.svg)](https://github.com/virtualryder/benefits_eligibility_agent/actions/workflows/ci.yml)

> **SUPPORTED DEPLOYMENT PATH — read this first.** The ONE supported path is **AWS CDK at the validated
> release tag [`v0.3.0-pilot-rc1`](https://github.com/virtualryder/benefits_eligibility_agent/releases/tag/v0.3.0-pilot-rc1)**
> (`cdk/ben_stacks`, 7 stacks + one data stack per tenant in multi-tenant mode, prefix `ben-` — includes the AgentCore Gateway/Cedar attachment as IaC),
> per [`DEPLOYMENT-GUIDE.md`](DEPLOYMENT-GUIDE.md) and [`VALIDATED_RELEASE.md`](VALIDATED_RELEASE.md). `v0.3.0-pilot-rc1`
> (2026-09-02) is the tree the AgentCore from-zero, hybrid multi-tenant, per-tenant audit routing and full-transparency
> runs validated live; the older `v0.1.2-pilot-rc1` is the EP1 Gate-B tag (2026-07-27 — `evidence/EP1-VALIDATION.md`).
> The shell engine (`lib/engine/`) is **legacy/internal reference only**. Product framing: a governed
> eligibility **screening & determination-support Assistant** — it never adjudicates, denies, reduces,
> terminates, or refers fraud (`PILOT-SCOPE.md`).
>
> *Part of the Governed Agent Platform: shares one versioned governance core with the sibling verticals,
> also consolidated into the [governed-agent-platform](https://github.com/virtualryder/governed-agent-platform) monorepo.*

> **Continuous validation.** On every push CI runs the **governance-core integrity gate** (`lib/verify_core.py`, so the shared core must match its pinned `core.lock` and drift cannot merge unnoticed), manifest render, the unit + eval suite, and a bug-class lint, plus a **supply-chain job** that audits the pinned runtime dependencies (`pip-audit`) and emits a CycloneDX SBOM. An **opt-in** end-to-end job (`.github/workflows/e2e.yml`, manual `workflow_dispatch`) deploys the spine to a sandbox AWS account, proves it live with the demo in ENFORCE, and tears it down — see the workflow header for one-time setup.


A **governed** public-benefits eligibility-**screening** & determination-**support** assistant for State &
Local Government. It intakes an application, de-identifies PII, runs a deterministic **eligibility screen +
estimate** and the processing clock, prepares redetermination/overpayment findings, drafts a determination
notice, and **pauses at a human sign-off gate** — a caseworker makes and commits the determination; the
assistant never adjudicates, denies, reduces, terminates, or refers fraud on its own. Because benefits
determinations are **due-process protected** (Goldberg v. Kelly), every adverse action stays human-committed
with notice and appeal rights. Built on the same governed-hero-agent pattern as the pharmacovigilance agent,
from a reusable, manifest-driven template.

> ## ⚠️ Scope boundary — read before any customer conversation
>
> **This is NOT an eligibility determination engine.** The deterministic logic here is a **preliminary
> income screen**: public HHS Federal Poverty Guidelines with a **SNAP-style gross-income test** (130% FPL,
> 7 CFR 273.9) plus an expedited/standard processing clock.
>
> A production SNAP determination additionally requires gross **and net** income tests, earned-income /
> shelter / dependent-care / medical / child-support deductions, resource rules, broad-based categorical
> eligibility, household composition, student and immigration eligibility, work requirements, state
> options, proration, certification periods and benefit-allotment calculation. **Medicaid** eligibility
> varies by state and coverage group (MAGI vs non-MAGI, disability, pregnancy, spend-down, asset and
> long-term-care rules) and **cannot** be represented by a generic FPL rule. **TANF** is state-specific.
> **Unemployment insurance is out of scope entirely** — no UI logic exists in this repository.
>
> Position this as: *intake summarization, preliminary screening, missing-information identification and
> draft caseworker communication* — for **one state and one program** at a time. The authoritative rules
> remain the agency's. See [`PILOT-SCOPE.md`](PILOT-SCOPE.md) and [`docs/VALIDATED-MATRIX.md`](docs/VALIDATED-MATRIX.md).

> **Accelerator, not a certification.** Reference implementation of the *pattern*. Not a
> production-certified system. Computer-system validation, IdP federation, connectors to the state's
> benefits system of record, authoritative program rules, and the authorization to operate (StateRAMP /
> ATO) remain the adopter's responsibility. Poverty guidelines and program thresholds here are
> **illustrative federal defaults** — configure per program, state, and year.

> **Control-plane hardening (ported from the financial-aid/housing agents).** De-identification is now
> proven by a **mask_pii-signed `sanitized_ref`** with content binding — the spoofable `deidentified`
> boolean is no longer accepted by any tool (P0-1). The bearer token is **out of every tool schema**;
> the trusted runtime injects it out-of-band (P0-3). A **deterministic guard set** (`workflow_guards.py`)
> gives a Step Functions controller the machine-verifiable transition evidence to branch on — including a
> **due-process advance-notice HOLD** on any adverse redetermination — so eligibility/masking/notice
> cannot be skipped by the model (P0-2). **Now at the sibling agents' pilot depth: the full 7-stack AWS
> CDK set + Gate-B posture (zero public egress · CMK · MFA identity · tenant pin), R3-2 pass-by-reference
> (both directions), release discipline + manifest, and the operating-model doc bundle — all live
> EP1-validated** (2026-07-27, env `ben-val1`, us-east-1): `validate_deployment.py` PASS, the deterministic
> controller ran to the human sign-off gate, the **AdverseNoticeHold** due-process gate held an adverse
> redetermination, and the **strict PII canary passed with 0 leaks**, then torn down + residual-swept.
> Evidence: `evidence/EP1-VALIDATION.md`; tag `v0.1.2-pilot-rc1`. Current suite: **173 offline tests**;
> tag `v0.3.0-pilot-rc1` was cut from this tree (2026-09-02); `v0.2.0-pilot-rc1` marked the governed-core dependency migration.
>
> **2026-09-02 — AgentCore repositioning, hybrid multi-tenant SaaS, full transparency (all live, all torn down).**
> Fresh from-zero ENFORCE re-proof (`evidence/AGENTCORE-E2E-FROMZERO-2026-09-02.md`); **hybrid multi-tenant**
> control plane — one shared AgentCore Gateway + Cedar engine, physically separate per-tenant data stacks,
> tenant DERIVED from the verified identity by a gateway request interceptor, cross-tenant deny proven with
> two tenants (`evidence/AGENTCORE-MULTITENANT-E2E-2026-09-02.md`); **per-tenant audit ledger / WORM vault /
> approvals routing** across both the gateway and the Step Functions hop, fail-closed
> (`evidence/AGENTCORE-MULTITENANT-AUDIT-2026-09-02.md`, governed-core 1.6.0); and **full per-case
> transparency** through the real AgentCore Runtime — the agent's reasoning spans, every gateway / tool /
> model API call and the WORM record joined by session + trace id, tagged per tenant, masked-before-model
> measured on every model invocation (`evidence/AGENTCORE-OBSERVABILITY-2026-09-02.md`, governed-core
> 1.7.1). Design: platform `docs/MULTI-TENANT-SAAS-DESIGN.md` + `docs/OBSERVABILITY-CORRELATION.md`.
> **2026-09-03:** the **Kill Switch** (governed-core 1.8.0; `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md`, 29/29, 13.9 s to effect) and the **per-tenant token + USD budget** (governed-core 1.9.0; `evidence/AGENTCORE-BUDGET-2026-09-03.md`, 23/23) are live on the AgentCore path — see the sections below.
> Multi-tenant is the SaaS roadmap path; the per-customer single-tenant silo remains the default deployment.

---

## Why this agent

Public-benefits intake (SNAP and similar means-tested programs) is high-volume, time-critical, and
under heavy regulation (Social Security Act, IRS Pub 1075 for federal tax info, due-process
requirements, StateRAMP / NIST 800-53). It's an obvious place for an AI agent — but a regulated agency
cannot adopt an ungoverned one: PII must never leak, every decision needs a tamper-evident audit, tool
access must be least-privilege, and a **qualified caseworker must make and commit the determination**.
This agent keeps the human in charge and makes the platform enforce it.

## The governed workflow

```
intake_application -> mask_pii -> assess_eligibility -> draft_notice -> write_audit -> request_signoff
                                                                                          |
                                                          caseworker (a DIFFERENT person) approves -> finalize
```

- **intake_application** — extract the non-PII decision fields (household size, income, resources,
  categorical flag) from the raw application.
- **mask_pii** — fail-closed PII de-identification (Amazon Comprehend `DetectPiiEntities`: name, SSN,
  address, DOB…). If masking can't run, nothing downstream proceeds.
- **assess_eligibility** — a deterministic rules engine (public Federal Poverty Guidelines + SNAP-style
  gross-income test) returning ELIGIBLE / INELIGIBLE / NEEDS_REVIEW and the **processing clock**
  (EXPEDITED 7-day vs STANDARD 30-day). No model, no licensed data.
- **draft_notice** — a real Bedrock (Claude) determination notice on de-identified data only,
  through the platform Bedrock guardrail when armed (`-c guardrail_id=…`). Any guardrail
  intervention fails closed (no `notice_ref`); the workflow's `DraftOk` gate then routes the case
  to `ManualReview` rather than the sign-off gate. Proven live 2026-08-29: a prompt-injection
  application was intervened and never reached an approver.
- **write_audit** — append-only DynamoDB ledger + S3 Object Lock (WORM) copy of every decision. Each record is **hash-chained** to the prior one (`chain_hash = SHA-256(prev_hash + entry_hash)`), so the ledger is tamper-evident by construction — not just un-deletable but provably un-editable — and `lib/controls/verify_chain.py` replays the links to prove INTACT (or name the first broken record).
- **request_signoff / approve-signoff / finalize** — a Step Functions separation-of-duties gate. A
  *different* caseworker approves through **`approve-signoff`** (Cognito access-token verified, SoD,
  single-use token) before `finalize` runs. On **governed-core ≥ 1.5.0**, `finalize` verifies the
  **approval path**: a token released around that Lambda (a raw `send-task-success`, say) is refused
  fail-closed to `ManualReview` and recorded `DENIED`. Proven live 2026-08-29: a raw-CLI approval
  wrote no `COMMITTED` marker; a token-verified approval committed; self-approval was refused.

**Observability** is IaC on every deploy: X-Ray on all tools + the gateway, Step Functions execution
logging (payload-free), unconditional 1-year Lambda log retention, account-level Bedrock
model-invocation logging (de-identified prompts), and a data-only CloudTrail on the WORM vault
alongside the platform evidence trail — four independent captures of every action. See
`DEPLOYMENT-GUIDE.md` and `evidence/OBSERVABILITY-VALIDATION-2026-08-29.md`.

Authorization is **Cedar deny-by-default** at the AgentCore Gateway: `caseworker_permit` (role-gated),
`mask_before_assess` and `mask_before_draft` forbids (no processing/drafting on un-masked data), and
`no_self_commit` (the agent can never finalize a determination). The Runtime discovers the gateway via
SSM and validates the caseworker's Cognito JWT.

## Tests — proven live in ENFORCE

> **Two distinct artifacts — do not conflate them.** (1) The **offline suite: 173 tests**
> (control-plane + 18 CDK synthesis) — the authoritative CI number (`RELEASE-MANIFEST.md`).
> (2) The **legacy shell governance demo below: 29 live checks** against a deployed system in Cedar
> ENFORCE. The demo is an internal reference; the supported deployment path is CDK.

`bash lib/engine/demo.sh agents/benefits-eligibility` exercises the full governed workflow against the
deployed system with Cedar in **ENFORCE**, and reports `29 passed, 0 failed / GOVERNANCE DEMO: PASS`:
deny-by-default (caseworker ALLOW / outsider DENY), fail-closed PII masking, the mask-before forbids
firing *by name*, the eligibility determination + processing clock (with the authoritative 2026 HHS
poverty guidelines and provenance), a real guarded Bedrock notice, the append-only, tamper-evident WORM audit (write-once +
duplicate rejection), `no_self_commit`, and the human sign-off gate (separation of duties + single-use
token).

### Deeper caseload workflows (each a governed tool + its own Cedar control)

The higher-risk the action, the stronger the governance. Beyond intake/screening, the agent adds:

- **`redetermine`** — changed-circumstances re-determination that classifies the change and, on an
  **ADVERSE** result (a reduction or termination), flags that **timely advance due-process notice** is
  required (*Goldberg v. Kelly*) before the action takes effect. Fail-closed (`mask_before_redetermine`).
- **`detect_overpayment`** — deterministic overpayment calculation over a recovery period; recovery and
  any referral remain human decisions. Fail-closed (`mask_before_overpayment`).
- **`refer_fraud`** — a **consequential, human-only** action: the agent can **never** refer a case as
  suspected fraud. Forbidden by Cedar `no_self_fraud_referral` — the same deny-by-default pattern as
  `no_self_commit`, showing the model scales to every new high-risk action.

All three are proven live in the 29-check demo.

## Hybrid multi-tenant + full transparency (2026-09-02)

Both are CDK context switches on the same stacks (see `DEPLOYMENT-GUIDE.md` §1b); silo deployments
are unchanged when the switches are off.

```bash
cd cdk && npx --yes aws-cdk@2.1139.0 deploy --all --require-approval never \
  -c env=mt -c retention_profile=sandbox-demo -c tenants=pha-a,pha-b -c model_logging=1
python scripts/mt_two_tenant_proof.py  --env mt --tenants pha-a,pha-b          # cross-tenant deny + per-tenant routing (12 checks)
python scripts/obs_two_tenant_proof.py --env mt --tenants pha-a,pha-b \
  --runtime-arn <runtime arn> --runtime-log-group /aws/bedrock-agentcore/runtimes/<agent>-DEFAULT   # 13 checks per tenant
python scripts/trace_case.py --env mt --case-id <id> --tenant pha-a --session-id <runtime session>  # one auditor timeline
```

- **Tenant is derived, never requested.** Cognito `tenant_<id>` group → gateway REQUEST interceptor →
  HMAC-signed pair in the tool arguments → every Lambda verifies it before routing to
  `<prefix>-<tenant>-{case-store,sanitized-artifacts,audit-ledger,pending-approvals}` and the tenant's own
  Object-Lock vault; `require_tenant` (Cedar, multi-tenant only) refuses un-tenanted identities at the gateway.
- **The workflow hop** (no interceptor) carries the signed pair in the execution input; an execution
  started without it fails at the first state. `ingest` derives the tenant from a verified access token.
- **Transparency.** One correlation set (tenant · session · trace · request · case) on every runtime span
  (Strands `trace_attributes`), every Bedrock call (`requestMetadata`), every tool Lambda's `aegis.call`
  log line, the gateway's request rows and the hash-chained WORM record (`correlation` block); the
  Bedrock model-invocation log (`-c model_logging=1`, account-level, opt-in) holds the exact bodies.

## Kill Switch — one-command containment (2026-09-03, governed-core 1.8.0)

Every deployment carries `/ben-<env>-eligibility/kill-switch` (SSM Parameter Store). Every component on
the agent path reads it **first**, fail-closed, with a 15 s TTL cache: the gateway REQUEST interceptor
short-circuits `tools/list` + `tools/call` with a 403 **and** writes a `DENIED` record + WORM object into
the acting tenant's ledger; every governed tool Lambda refuses at `telemetry.instrument` (a Step Functions
execution fails at its next state with `KillSwitchEngaged`); the Runtime refuses new invocations and stops a
**running** session at its next model call. Engage / disengage are two Lambda function URLs with
`AuthType: AWS_IAM` behind separate managed policies (IAM separation of duties); the actor is the
IAM-verified caller, and the engaging identity can never release its own engagement (a `DENIED` record).
Every state change is a `COMMITTED` row in the base ledger's `KILL-SWITCH` chain.

```bash
python scripts/kill_switch_proof.py --env mt --tenants pha-a,pha-b --runtime-arn <arn> \
  --runtime-log-group /aws/bedrock-agentcore/runtimes/<agent>-DEFAULT --out evidence/AGENTCORE-KILL-SWITCH-<date>   # 21 checks
```

Details: `DEPLOYMENT-GUIDE.md` §1c; evidence `evidence/AGENTCORE-KILL-SWITCH-2026-09-03.md`; runbook:
platform `docs/ops/KILL-SWITCH.md`.

## Per-tenant token budget + USD ceiling (2026-09-03, governed-core 1.9.0)

Every model call is metered per tenant per month (`ben-<env>-budgets`): one conditional reservation before the
call, the real Converse `usage` committed after — proven equal to the Bedrock model-invocation log. A tenant
at/over its hard cap is refused before the spend at the Runtime (mid-session if needed), at the gateway
interceptor (403 + DENIED WORM record) and at the drafter (→ `ManualReview`); 60/85/100 % alarms per tenant;
`-c budget_usd` adds the USD cap and the AWS Budgets ceiling whose breach engages the kill switch. Prices are
pinned with stated provenance (`lib/model_prices.json`) — an estimate; the CUR is the financial truth.

```bash
python scripts/budget_proof.py --env mt --tenants pha-a,pha-b --runtime-arn <arn> \
  --runtime-log-group /aws/bedrock-agentcore/runtimes/<agent>-DEFAULT --out evidence/AGENTCORE-BUDGET-<date>   # 24 checks
```

Details: `DEPLOYMENT-GUIDE.md` §1d; evidence `evidence/AGENTCORE-BUDGET-2026-09-03.md`.

## Deploy / prove / run / tear down

Requirements: AWS CLI v2 (admin, us-east-1), Python 3.12 + `pyyaml`, Bedrock model access, Bash
(Git-Bash on Windows). One agent = one manifest (`agents/benefits-eligibility/manifest.yaml`) + domain
tool bodies + Cedar policies; the engine, control library, and runtime are reused.

```bash
bash lib/engine/deploy.sh  agents/benefits-eligibility   # spine: engine -> gateway -> targets -> policies -> ENFORCE
bash lib/engine/demo.sh    agents/benefits-eligibility   # 29-check governance proof
bash lib/engine/redteam.sh agents/benefits-eligibility   # adversarial proof: governance holds under attack
# Runtime (from a fresh venv):
bash lib/runtime/setup_venv.sh
bash lib/runtime/_obs_setup.sh  agents/benefits-eligibility
bash lib/runtime/_configure.sh  agents/benefits-eligibility
bash lib/runtime/_launch.sh     agents/benefits-eligibility
bash lib/runtime/_invoke.sh     agents/benefits-eligibility caseworker   # or: bash invoke_demo.sh (with sample data)
# Optional depth add-on — the governed OAuth connector (real outbound auth via AgentCore Identity, no stored secret):
bash lib/connector/deploy_connector.sh agents/benefits-eligibility   # mock OAuth SoR (MOCK SoR) + Identity provider + verify_source
bash lib/connector/prove_connector.sh  agents/benefits-eligibility   # proves OAuth + RS256/JWKS signature check + no secret + deny-by-default
bash lib/engine/destroy.sh agents/benefits-eligibility   # zero-residual teardown (identity preserved)
```

Test-user passwords are env-driven (`PV_REVIEWER_PW` / `PV_APPROVER_PW` / `PV_OUTSIDER_PW`) with
placeholder defaults (`ChangeMe-*1!`) — rotate before shared use. Region/account resolve dynamically.

## Layout

```
lib/engine/     manifest-driven engine: render.py + deploy/demo/destroy + deploy_identity + signoff.asl.tmpl
lib/controls/   this agent's domain-shaped controls: mask_pii, provenance (declared overrides), sanitized, case_store, ingest_case, workflow_guards
                (evidence, write_audit, sign-off, identity, tenancy, tenant_interceptor, telemetry come from the PINNED governed-core wheel - requirements-core.txt)
lib/runtime/    generic Strands agent on AgentCore Runtime (agent.py + Dockerfile + toolkit helpers)
lib/connector/  reusable governed OAuth connector: verify_source (token via AgentCore Identity, no stored secret) + deploy/prove scripts + RS256/JWKS-verified mock SoR
agents/benefits-eligibility/
                manifest.yaml (single source of truth) + tools/ (intake, assess_eligibility, redetermine, overpayment, benefits_core) + demo_extra.sh
policies/       the seven Cedar policies (rendered from the manifest), human-readable + a README
docs/           architecture note + Word guides (regulatory-adherence, SA runbook, maintenance, depth-evidence, cost/latency one-pager, IdP-federation reference; generators/ regenerates the guides & decks)
```

The Cedar policies in `policies/` are the governance core — see `policies/README.md`. They are
generated from the manifest at deploy time; the checked-in `.cedar` files are the reviewable
rendered form (account id and gateway ARN are placeholders).

## Honesty boundary

The accelerator owns the governed agent, the Cedar policies, the tools, the fail-closed masking, the
human-gate workflow, the WORM audit design, the IaC, the tests. The adopter owns: IdP federation to their own provider (a working OIDC/SAML → Cognito → Cedar reference ships as `lib/engine/deploy_federation.sh` + `docs/IdP-Federation-Reference.md`, so federated users hit the same deny-by-default policies as the built-in users) and caseworker role mapping; validated connectors to the state benefits system of record; the authoritative
program rules/thresholds and their legal review; computer-system validation; and production authorization
to operate (StateRAMP / ATO). The repo also ships a **real** governed OAuth connector — `verify_source` authenticates to a mock system of record via AgentCore Identity (no stored secret) and the SoR verifies the token's RS256 signature against the Cognito JWKS — as the reference pattern; connectors to the **production** system of record remain adopter work.


## License

Apache-2.0 — see [LICENSE](LICENSE).
