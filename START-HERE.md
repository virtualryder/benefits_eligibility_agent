# START HERE — Public Benefits Intake, Eligibility Screening & Caseworker Decision-Support Assistant

*One page: what this is, what is actually proven, how to evaluate it, and what a first pilot looks like.*

**Validated release: [`v0.1.2-pilot-rc1`](https://github.com/virtualryder/benefits_eligibility_agent/releases/tag/v0.1.2-pilot-rc1)**
— cut after a **full runbook re-walk and clean-account re-validation on 2026-07-28** (env `ben-val2`),
run from the hardened code with the whole `DEPLOYMENT-GUIDE.md` followed step by step as an SA would.
**Deploy the tag, never `main`.** Supported deployment path: **AWS CDK** (`cdk/ben_stacks`, 7 stacks);
the shell engine (`lib/engine/`) is legacy/internal only.

> The earlier `v0.1.0-pilot-rc1` tag is **superseded — do not deploy it.** It predates the security
> hardening: it still deploys the unreachable `verify_income` Lambda holding an AgentCore-Identity OAuth
> grant, and its CDK dependencies are unpinned.

---

## What this is — and what it is deliberately NOT

A **governed assistant** for public-benefits intake. It:

- extracts non-PII decision fields from a raw application (household size, income, resources, categorical flag),
- **de-identifies PII** (fail-closed; proven by a signed reference, not a caller-supplied flag),
- runs a **deterministic preliminary income screen** — public HHS Federal Poverty Guidelines with a
  SNAP-style gross-income test — plus the expedited (7-day) vs standard (30-day) processing clock,
- prepares redetermination / overpayment findings,
- drafts a determination notice for a caseworker,
- then **pauses at a human sign-off gate**.

**It is NOT an eligibility determination engine.** The rules here are a **preliminary federal-threshold
screen on illustrative federal defaults** — not authoritative SNAP, Medicaid, or TANF eligibility. It does
not adjudicate, deny, reduce, terminate, refer fraud, calculate a benefit allotment, or write to a system
of record. Every consequential action is made and committed by a qualified caseworker.
See [`PILOT-SCOPE.md`](PILOT-SCOPE.md) for the explicit exclusion list.

## Evidence provenance — read this honestly

| Claim | Status |
|---|---|
| Offline suite | **133 passing** (124 locally + 1 CI-only gate) (control-plane + 13 CDK stack-synthesis assertions) — authoritative count: [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md) |
| Live clean-account validation | **Done twice** — EP1 2026-07-27 (`ben-val1`) and a full runbook re-walk 2026-07-28 (`ben-val2`), us-east-1, all Gate-B switches — [`evidence/EP1-VALIDATION.md`](evidence/EP1-VALIDATION.md) |
| Zero public egress | **Measured, not asserted** — 0 NAT gateways · 0 internet gateways · 9 VPC endpoints on the live `ben-val2` VPC |
| Deploy-from-IaC of the zero-egress SG fix | **Proven** on `ben-val2`. (In EP1 that rule had to be patched onto the live SG by hand, so the IaC version was previously unexercised.) |
| Live governance demo (shell engine, legacy) | 29 checks against a deployed system in Cedar ENFORCE — a **separate** artifact from the 133 offline tests |
| Independent deployment by a third party | **Not yet** — all evidence is author-produced. **A verification kit is ready:** [`docs/INDEPENDENT-VERIFICATION.md`](docs/INDEPENDENT-VERIFICATION.md) + `python scripts/independent_verify.py`. This is the highest-value next step — if you are that third party, start there. |
| Independent security test / pen test | **Not yet** |
| Enterprise IdP round-trip | **Not yet** (federation exists as IaC; no agency IdP integrated) |
| Benefits-program SME sign-off on the rules | **Not yet** ([`docs/SME-REVIEW-PACKET.md`](docs/SME-REVIEW-PACKET.md)) |
| Real applicant data | **Never used** — synthetic only |

The single consolidated view is [`docs/VALIDATED-MATRIX.md`](docs/VALIDATED-MATRIX.md).

## What EP1 proved live

7/7 CDK stacks deployed (incl. the AgentCore Gateway/Cedar **ENFORCE** attachment as IaC);
`validate_deployment.py` → PASS; the deterministic controller ran every guard to the **human sign-off
gate**; an adverse redetermination without advance notice **held** at `AdverseNoticeHold` (due process —
*Goldberg v. Kelly*); the **strict PII telemetry canary found 0 leaks** across CloudWatch Logs, X-Ray,
DLQs and Step Functions history; MFA identity pool ON with 0 users. Then torn down with a zero-residual
sweep.

## Reading order by role

| You are | Read, in order |
|---|---|
| **Solution Architect** | [`DEPLOYMENT-GUIDE.md`](DEPLOYMENT-GUIDE.md) → [`cdk/README.md`](cdk/README.md) → [`BENEFITS-PILOT-READINESS-PLAN.md`](BENEFITS-PILOT-READINESS-PLAN.md) |
| **CISO / security** | [`docs/THREAT-MODEL.md`](docs/THREAT-MODEL.md) → [`docs/GATE-B-CHECKLIST.md`](docs/GATE-B-CHECKLIST.md) → [`docs/INCIDENT-RESPONSE.md`](docs/INCIDENT-RESPONSE.md) → [`docs/DATA-SOURCE-POLICY.md`](docs/DATA-SOURCE-POLICY.md) |
| **Program / policy leadership** | [`PILOT-SCOPE.md`](PILOT-SCOPE.md) → [`docs/SME-REVIEW-PACKET.md`](docs/SME-REVIEW-PACKET.md) → the pilot shape below |
| **Auditor / compliance** | [`docs/VALIDATED-MATRIX.md`](docs/VALIDATED-MATRIX.md) → [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md) → [`VALIDATED_RELEASE.md`](VALIDATED_RELEASE.md) → [`docs/AUDIT-READINESS.md`](docs/AUDIT-READINESS.md) |
| **GTM / seller** | This page → [`PILOT-SCOPE.md`](PILOT-SCOPE.md) → [`docs/Cost-and-Latency-One-Pager.md`](docs/Cost-and-Latency-One-Pager.md) |

## Regulatory frame (benefits)

Due process for adverse actions (*Goldberg v. Kelly*; SNAP 7 CFR 273, Medicaid 42 CFR 435) · state
privacy law and Medicaid confidentiality (42 CFR 431 Subpart F) · **IRS Publication 1075 where federal tax
information is in scope** (this pilot processes **no FTI** — see [`PILOT-SCOPE.md`](PILOT-SCOPE.md)) ·
StateRAMP / NIST 800-53 as the agency requires. Adopter work: authoritative state/program rules,
income and identity verification, system-of-record integration, notice and fair-hearing workflow, ATO.

## Recommended first pilot

**One state, one program (SNAP intake screening), read-only shadow mode.** Synthetic cases first, then
de-identified retrospective cases with agency approval. Every output human-reviewed. Measured on intake
handling time, screen agreement with caseworkers, expedited-clock agreement, notice edit rate, and
override reasons. Full shape + exclusions: [`BENEFITS-PILOT-READINESS-PLAN.md`](BENEFITS-PILOT-READINESS-PLAN.md).

## Status in one line

Control plane hardened, full CDK/Gate-B IaC, **live-validated twice** (2026-07-27 `ben-val1`;
2026-07-28 `ben-val2` full runbook re-walk, all gates PASS, zero residual),
tag `v0.2.0-pilot-rc1`, cut from this tree. Suite: **133 offline tests** (the older `v0.1.2-pilot-rc1` tag predates the dependency migration and stood at 101; do not
re-align). Next, in order: independent redeploy of the tag,
tenant-scoped case-store fetch, enterprise IdP round-trip, a one-state SNAP rule set with
benefits-program SME sign-off, and independent security testing — before any real data.
