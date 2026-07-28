# Configuration Worksheet — Benefits determination Assistant

*Every sponsor/market-controlled value the assistant uses, with owner, where it is set, its authoritative
source, and a sign-off line. The eligibility thresholds and processing clocks are **illustrative defaults**
— a benefits-program SME/regulatory owner must confirm them per market and product before a pilot.*

---

## How configuration works

Two kinds of settings:

1. **Deploy-time switches** (CDK context) — posture: `env`, `retention_profile`, `kms=customer-managed`,
   `network_mode=private`, `identity_mode=pilot`, `tenant`. Owned by IT/security; on the `cdk deploy`
   command; documented in `DEPLOYMENT-GUIDE.md`.
2. **Regulatory constants** — the values below (in the rules engine). Each has a single home in code.

No configuration value is accepted from a request body at runtime.

## Agency / program-controlled values

*Every row is **per state and per program** and must be approved by the agency's benefits-program SME
before real cases are screened. The shipped defaults are **illustrative federal values**, not the
authoritative rules for any given program.*

| Value | Shipped default (illustrative) | Owner | Where set | Authoritative source | Approved by |
|---|---|---|---|---|---|
| Federal Poverty Guidelines | 2026 HHS: $15,960 base, +$5,680 per additional member (48 states + DC) | Benefits-program SME | `assess_eligibility.py::FPL_BASE / FPL_PER_ADD` | HHS annual poverty guidelines (Federal Register) | ☐ |
| Gross-income limit | 130% FPL | Benefits-program SME | `assess_eligibility.py::GROSS_LIMIT_PCT` | SNAP 7 CFR 273.9 (+ state options) | ☐ |
| Expedited-service screen | gross monthly income < $150 **and** liquid resources ≤ $100 | Benefits-program SME | `assess_eligibility.py::EXPEDITED_*` | SNAP 7 CFR 273.2(i) (+ state policy) | ☐ |
| Processing clock | expedited 7 days · standard 30 days | Benefits-program SME | `assess_eligibility.py` | SNAP 7 CFR 273.2 (+ state policy) | ☐ |
| Categorical eligibility | SSI / TANF / general assistance flag | Benefits-program SME | `intake_application.py` | State categorical / broad-based categorical policy | ☐ |
| **Net-income test + deductions** | **NOT IMPLEMENTED** — earned-income, shelter, dependent-care, medical, child-support deductions are required for a real SNAP determination | Benefits-program SME | *(adopter configuration — Gate-C)* | SNAP 7 CFR 273.9(d) | ☐ |
| **Resource limits** | **NOT IMPLEMENTED** as a per-state rule | Benefits-program SME | *(adopter configuration — Gate-C)* | SNAP 7 CFR 273.8 (+ state options) | ☐ |
| Redetermination / overpayment findings | change classification + case-specific rationale (required) | Benefits-program SME | `redetermine.py` / `overpayment.py` (prepare-only) | SNAP 7 CFR 273 / state policy | ☐ |
| Advance-notice requirement (due process) | required for any ADVERSE change; enforced by the `adverse_notice` guard | Benefits-program SME + agency counsel | `workflow_guards.py::guard_adverse_notice` | *Goldberg v. Kelly*; SNAP 7 CFR 273.13 | ☐ |
| Determination-notice language | plain-language draft, ≤ 250 words, preserves `[REDACTED:…]`, states appeal/fair-hearing rights | Benefits-program SME | `benefits_core.py::_SYSTEM` | State notice template + Section 508 review | ☐ |
| Retention profile | (deploy choice) | IT/security | CDK `-c retention_profile=…`; `docs/RETENTION-PROFILES.md` | State record-retention schedule | ☐ |
| Draft model id | Claude Sonnet (cross-region inference profile) | IT/security | `DRAFT_MODEL_ID` env | — | ☐ |

**the eligibility engine/FPL config is reference context only** and never a case/adverse-action determination source — not a configurable
determination input.

## Change procedure

Any change is a change-managed event: update the code constant, run the suite (`pytest tests/`), record
the approver, deploy through a tagged release. **Follow-on:** a machine-readable config file +
`test_config_schema.py` drift gate (as the financial-aid agent has) — noted in the readiness plan.

## Sign-off

We, the safety/benefits-program SME office, confirm the values above reflect our SOPs and the applicable market
regulation for the pilot product(s).

benefits-program SME / safety (name / title / date): __________________________
IT / security (name / title / date): __________________________
