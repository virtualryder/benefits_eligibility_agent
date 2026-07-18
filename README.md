# Benefits Eligibility Agent — Governed Agentic AI on Amazon Bedrock AgentCore

[![CI](https://github.com/virtualryder/benefits_eligibility_agent/actions/workflows/ci.yml/badge.svg)](https://github.com/virtualryder/benefits_eligibility_agent/actions/workflows/ci.yml)

A **governed** public-benefits eligibility & adjudication agent for State & Local Government. It
intakes an application, de-identifies PII, determines eligibility and the processing clock, drafts a
determination notice, and **pauses at a human sign-off gate** — a caseworker makes and commits the
determination; the agent never self-adjudicates. Built on the same governed-hero-agent pattern as the
pharmacovigilance agent, from a reusable, manifest-driven template.

> **Accelerator, not a certification.** Reference implementation of the *pattern*. Not a
> production-certified system. Computer-system validation, IdP federation, connectors to the state's
> benefits system of record, authoritative program rules, and the authorization to operate (StateRAMP /
> ATO) remain the adopter's responsibility. Poverty guidelines and program thresholds here are
> **illustrative federal defaults** — configure per program, state, and year.

---

## Why this agent

Benefits intake (SNAP, Medicaid, TANF, unemployment insurance) is high-volume, time-critical, and
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
- **draft_notice** — a real Bedrock (Claude) determination notice, through a fail-closed output
  guardrail, on de-identified data only.
- **write_audit** — append-only DynamoDB ledger + S3 Object Lock (WORM) copy of every decision.
- **request_signoff** — starts a Step Functions separation-of-duties gate; a *different* caseworker
  approves with a single-use token before `finalize_determination` ever runs.

Authorization is **Cedar deny-by-default** at the AgentCore Gateway: `caseworker_permit` (role-gated),
`mask_before_assess` and `mask_before_draft` forbids (no processing/drafting on un-masked data), and
`no_self_commit` (the agent can never finalize a determination). The Runtime discovers the gateway via
SSM and validates the caseworker's Cognito JWT.

## Tests — proven live in ENFORCE

`bash lib/engine/demo.sh agents/benefits-eligibility` exercises the full governed workflow against the
deployed system with Cedar in **ENFORCE**, and reports `28 passed, 0 failed / GOVERNANCE DEMO: PASS`:
deny-by-default (caseworker ALLOW / outsider DENY), fail-closed PII masking, the mask-before forbids
firing *by name*, the eligibility determination + processing clock (with the authoritative 2026 HHS
poverty guidelines and provenance), a real guarded Bedrock notice, the immutable WORM audit (write-once +
duplicate rejection), `no_self_commit`, and the human sign-off gate (separation of duties + single-use
token).

### Deeper caseload workflows (each a governed tool + its own Cedar control)

The higher-risk the action, the stronger the governance. Beyond intake/adjudication, the agent adds:

- **`redetermine`** — changed-circumstances re-determination that classifies the change and, on an
  **ADVERSE** result (a reduction or termination), flags that **timely advance due-process notice** is
  required (*Goldberg v. Kelly*) before the action takes effect. Fail-closed (`mask_before_redetermine`).
- **`detect_overpayment`** — deterministic overpayment calculation over a recovery period; recovery and
  any referral remain human decisions. Fail-closed (`mask_before_overpayment`).
- **`refer_fraud`** — a **consequential, human-only** action: the agent can **never** refer a case as
  suspected fraud. Forbidden by Cedar `no_self_fraud_referral` — the same deny-by-default pattern as
  `no_self_commit`, showing the model scales to every new high-risk action.

All three are proven live in the 28-check demo.

## Deploy / prove / run / tear down

Requirements: AWS CLI v2 (admin, us-east-1), Python 3.12 + `pyyaml`, Bedrock model access, Bash
(Git-Bash on Windows). One agent = one manifest (`agents/benefits-eligibility/manifest.yaml`) + domain
tool bodies + Cedar policies; the engine, control library, and runtime are reused.

```bash
bash lib/engine/deploy.sh  agents/benefits-eligibility   # spine: engine -> gateway -> targets -> policies -> ENFORCE
bash lib/engine/demo.sh    agents/benefits-eligibility   # 28-check governance proof
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
lib/controls/   shared control tools: mask_pii, write_audit, request/approve/finalize sign-off, mcp_client
lib/runtime/    generic Strands agent on AgentCore Runtime (agent.py + Dockerfile + toolkit helpers)
lib/connector/  reusable governed OAuth connector: verify_source (token via AgentCore Identity, no stored secret) + deploy/prove scripts + RS256/JWKS-verified mock SoR
agents/benefits-eligibility/
                manifest.yaml (single source of truth) + tools/ (intake, assess_eligibility, redetermine, overpayment, benefits_core) + demo_extra.sh
policies/       the seven Cedar policies (rendered from the manifest), human-readable + a README
docs/           architecture note + Word guides (regulatory-adherence, SA runbook, maintenance, depth-evidence, cost/latency one-pager)
```

The Cedar policies in `policies/` are the governance core — see `policies/README.md`. They are
generated from the manifest at deploy time; the checked-in `.cedar` files are the reviewable
rendered form (account id and gateway ARN are placeholders).

## Honesty boundary

The accelerator owns the governed agent, the Cedar policies, the tools, the fail-closed masking, the
human-gate workflow, the WORM audit design, the IaC, the tests. The adopter owns: IdP federation and
caseworker role mapping; validated connectors to the state benefits system of record; the authoritative
program rules/thresholds and their legal review; computer-system validation; and production authorization
to operate (StateRAMP / ATO). The repo also ships a **real** governed OAuth connector — `verify_source` authenticates to a mock system of record via AgentCore Identity (no stored secret) and the SoR verifies the token's RS256 signature against the Cognito JWKS — as the reference pattern; connectors to the **production** system of record remain adopter work.


## License

Apache-2.0 — see [LICENSE](LICENSE).
