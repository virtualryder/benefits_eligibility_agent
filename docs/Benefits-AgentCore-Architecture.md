# Benefits Eligibility Agent — AgentCore-Native Architecture

*Target architecture for the public-benefits eligibility & adjudication hero agent, built natively on Amazon Bedrock AgentCore. This note is the anchor design — it doubles as the opening of the leadership deck and the first section of the SA runbook. It is the SLG counterpart to the pharmacovigilance (HCLS) agent, produced from the same reusable governed-hero-agent template. Draft v1.0 · 2026-07.*

---

## 1. What this agent does (the regulated workflow)

Public-benefits intake is high-volume, time-critical eligibility work: SNAP, Medicaid, TANF, unemployment insurance, and general assistance. When an application arrives, a regulated adjudication workflow must run end to end:

**intake the application → de-identify PII → assess eligibility and the processing clock (expedited vs. standard) → draft a determination notice → a qualified caseworker reviews and signs off → the determination is committed to the benefits system of record.**

Under the Social Security Act and program regulations (for SNAP, 7 CFR Part 273), and under constitutional due-process requirements (*Goldberg v. Kelly*), **a qualified caseworker must make and commit the determination** — with timely and adequate written notice and a right to a fair hearing. The agent intakes, de-identifies, screens, and drafts; it never self-adjudicates. That single rule drives the whole security design.

## 2. Design thesis

AWS now ships, in Amazon Bedrock AgentCore, the governance primitives a regulated agent needs. So we don't build a parallel governance platform — we become **the regulated-industry pattern implemented natively on AgentCore**: governed agentic AI built on AWS-native services, plus the three last-mile controls regulated customers need that AgentCore doesn't provide out of the box. This benefits agent is the second proof of that pattern: it was produced from the same manifest-driven template as the pharmacovigilance agent, by swapping the domain tools, the Cedar policies, and the masking primitive — the governance spine, runtime, and control library were reused unchanged.

## 3. Native on AgentCore vs. built alongside

| Control (governed-agent requirement) | Native? | AgentCore component / how |
|---|---|---|
| Verified human + agent identity | Native | **AgentCore Identity** — inbound JWT authorizer (Cognito / customer IdP) |
| Deny-by-default tool authorization | Native | **AgentCore Policy (Cedar)** — default-deny + forbid-wins, enforced at the Gateway |
| Least-privilege intersection (agent ∩ caseworker) | Native | Cedar principal with JWT group claims (`benefits_caseworker`) as tags + tool-parameter conditions |
| Tools as governed endpoints | Native | **AgentCore Gateway** — Lambda → MCP tools; every call passes Policy |
| Agent hosting / runtime | Native | **AgentCore Runtime** — hosts the Strands agent, serverless, session-isolated |
| Tracing / observability | Native | **AgentCore Observability** — OpenTelemetry spans per agent/tool step |
| Fail-closed PII de-identification | Build | `mask_pii` Gateway tool: Comprehend `DetectPiiEntities` (name, SSN, address, DOB…), before model + before audit |
| Human sign-off gate (separation of duties) | Build | Step Functions `waitForTaskToken` — bound, single-use approval; AgentCore has no native human gate |
| Immutable WORM audit (due-process evidence) | Build | Append-only DynamoDB + S3 Object Lock; Observability traces are for ops, not tamper-proof evidence |

## 4. Target architecture (components)

**AgentCore Runtime** hosts the Strands benefits agent (`benefits_runtime_agent`). The Strands agent gets a `BedrockAgentCoreApp` entrypoint and is deployed with the AgentCore starter toolkit (`agentcore configure` / `agentcore launch`), which containerizes it (ARM64 via CodeBuild) and manages the endpoint. The agent is generic — its workflow prompt is rendered from the manifest, so the same runtime image serves any agent built from the template.

**AgentCore Gateway** (`ben-eligibility-gw`) exposes each capability as an MCP tool backed by a Lambda target: `intake_application`, `mask_pii` (fail-closed), `assess_eligibility`, `draft_notice`, `write_audit`, and `request_signoff`. Because every tool call is a Gateway call, Policy can gate all of them uniformly. The consequential `finalize_determination` action exists only behind the human gate.

**AgentCore Identity** provides inbound auth — a JWT authorizer (Amazon Cognito or the customer's IdP) authenticates the caseworker on whose behalf the agent acts — and outbound auth for the credentials the Gateway uses to reach connectors (the state benefits system of record, delivered as a labeled stub).

**AgentCore Policy (Cedar)** is the deny-by-default authorization engine (`ben_eligibility_authz`). Default-deny and forbid-wins are automatic. Principal = the OAuth user (JWT `cognito:groups` surfaced as a tag); Action = the specific tool invocation (auto-mapped from the Gateway's tool definitions); Resource = the Gateway; conditions can test both user claims and tool input parameters. This is simultaneously the deny-by-default gateway and the least-privilege intersection — natively.

**AgentCore Observability** emits OpenTelemetry spans for every agent and tool step.

**Built alongside — the regulated last mile:**
- **Fail-closed PII de-identification:** the `mask_pii` tool de-identifies the application (Amazon Comprehend `DetectPiiEntities` — name, SSN, address, date of birth, and more) before the model drafts and before anything is written to the audit. Fail-closed — if masking can't run, the call stops rather than exposing PII.
- **Human sign-off gate (separation of duties):** `request_signoff` starts a Step Functions execution that pauses on `waitForTaskToken`; a *different* qualified caseworker approves with a bound, single-use token. The agent cannot finalize a determination itself.
- **Immutable WORM audit:** an append-only, tamper-evident record (append-only DynamoDB + S3 Object Lock) capturing `INTENT → COMMITTED` for the due-process and IRS Pub 1075 evidence trail.

## 5. How one governed action flows

1. The caseworker authenticates (Cognito/IdP) and receives a JWT.
2. The agent (on AgentCore Runtime) decides to call a tool.
3. The call goes through AgentCore Gateway; **Inbound Auth** validates the JWT.
4. The **Policy Engine** evaluates Cedar: principal (user claims) + action (the tool) + resource (the gateway) + conditions (group, tool parameters), default-deny. A deny means the tool never runs — and the denial is auditable.
5. The allowed tool runs. For drafting, `mask_pii` runs first (fail-closed), so the model only ever sees de-identified text.
6. The consequential step never executes inline: `request_signoff` opens the Step Functions human gate; a second qualified caseworker approves; only then does `finalize_determination` run.
7. Every decision and state change is written to the WORM audit, and every step is traced in Observability.

## 6. The eligibility rules engine (deterministic, illustrative)

`assess_eligibility` is a **deterministic rules engine**, not a model. It applies the **authoritative 2026 HHS Federal Poverty Guidelines** ($15,960 base, +$5,680 per additional person — Federal Register 2026‑00755) and a SNAP-style gross-income test (130% FPL, 7 CFR 273.9) to the de-identified decision fields, and returns a determination (ELIGIBLE / INELIGIBLE / NEEDS_REVIEW) and the **processing clock** (EXPEDITED 7-day vs. STANDARD 30-day). Every determination now **stamps the FPL source and year** into its output, so the basis is traceable to a named, authoritative source in the audit — not a magic number. It fails closed if the case is not marked de-identified. Alaska/Hawaii and program/state variations remain a per-program configuration item. This is the eligibility counterpart to the PV agent's seriousness/reporting-clock step: a transparent, auditable, non-model determination that a caseworker can defend at a fair hearing.

## 6a. Deeper caseload workflows (step two)

Beyond intake and adjudication, the agent adds the workflows a real caseload needs — each a **new governed tool with its own Cedar control**, following one rule: the higher-risk the action, the stronger the governance.

- **`redetermine`** — changed-circumstances re-determination. It re-runs the rules on new facts, classifies the change, and on an **ADVERSE** result (a reduction or termination) flags that **timely, adequate advance written notice** and a fair-hearing right are required *before* the action takes effect (*Goldberg v. Kelly*). Fail-closed (`mask_before_redetermine`).
- **`detect_overpayment`** — deterministic overpayment math over a recovery period. Recovery and any referral remain human decisions. Fail-closed (`mask_before_overpayment`).
- **`refer_fraud`** — a **consequential, human-only** action. The agent can **never** refer a case as suspected fraud; `refer_fraud` is forbidden outright by `no_self_fraud_referral`, exactly mirroring `no_self_commit`.

The point for an adopter: the governance model scales to new workflows with no new plumbing — a tool body plus a deny-by-default forbid — and each new forbid fires *by name* in ENFORCE.

## 7. Cedar policy model for benefits (illustrative)

Default-deny is automatic; we author explicit permits plus a few targeted forbids. Illustrative — final syntax is pinned against the account during deploy:

```cedar
// A benefits caseworker may intake, mask, assess, and draft — gated on the group claim.
permit(principal, action, resource is AgentCore::Gateway)
when { principal.hasTag("cognito:groups") &&
       principal.getTag("cognito:groups") like "*benefits_caseworker*" };

// No eligibility assessment on un-masked data: assess requires the de-identified flag.
forbid(principal, action == AgentCore::Action::"assess-eligibility___assess_eligibility",
       resource == AgentCore::Gateway::"<gateway-arn>")
unless { context.input.deidentified == true };

// No drafting on un-masked data.
forbid(principal, action == AgentCore::Action::"ben-core___draft_notice",
       resource == AgentCore::Gateway::"<gateway-arn>")
unless { context.input.deidentified == true };

// The determination is never a direct tool call — only the approval workflow can finalize.
forbid(principal, action == AgentCore::Action::"ben-core___finalize_determination",
       resource == AgentCore::Gateway::"<gateway-arn>");
```

The shape is the point: a group-scoped permit, two forbids that enforce masking-before-processing and masking-before-model, and no path for the agent to self-commit a determination.

## 8. Build order

1. **Governance spine first** — Cedar policies + Policy Engine + Gateway, with deny-by-default proven before anything else.
2. **Tools as Gateway Lambda targets** — `intake_application`, `mask_pii`, `assess_eligibility`, `draft_notice`, `write_audit`, `request_signoff`.
3. **Runtime + Identity** — the generic Strands agent onto AgentCore Runtime; Cognito inbound JWT wired to the Cedar principal.
4. **Human sign-off gate** — Step Functions `waitForTaskToken` wired to `request_signoff` and `finalize_determination`.
5. **WORM audit + Observability.**
6. **Manifest + validate** — the whole agent is one manifest; deploy; end-to-end run (Cedar allow/deny, masking, eligibility, real Bedrock notice, immutable audit) + negative tests; teardown.

## 9. What's ours vs. the customer's (honesty boundary)

The accelerator owns: the agent, the Cedar policies, the tools, the fail-closed masking, the human-gate workflow, the WORM audit design, the eligibility rules engine, the IaC/manifest, and the docs. The customer owns: IdP federation and caseworker role mapping; validated connectors to the state benefits system of record; the authoritative program rules and thresholds and their legal review; computer-system validation; and production authorization to operate (StateRAMP / ATO). Poverty guidelines and program thresholds here are illustrative federal defaults, and `verify_income` / system-of-record connectors ship as labeled stubs. Nothing here is production-certified on day one — and saying so is part of the credibility.

## 10. Regulatory anchors (full mapping is a separate guide)

- **Social Security Act / program regulations** (SNAP 7 CFR 273, Medicaid, TANF) → `assess_eligibility` rules engine + processing-clock logic; the **qualified-caseworker determination** → the human gate.
- **Due process (*Goldberg v. Kelly*)** → the drafted determination notice (timely & adequate written notice) + the WORM record + the fair-hearing evidence trail.
- **IRS Publication 1075** (safeguarding Federal Tax Information used in income verification) → fail-closed masking + least-privilege Cedar + immutable audit + encryption.
- **StateRAMP / NIST SP 800-53** (the authorization framework for state systems) → deny-by-default access control, audit, and the reproducible control evidence.

Each of these becomes a control-to-requirement line in the regulatory-adherence guide.
