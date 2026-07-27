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

## Sponsor / market-controlled values

| Value | Default | Owner | Where set | Authoritative source | Approved by |
|---|---|---|---|---|---|
| ICH system-of-record eligibility criteria | death · life-threatening · hospitalization · disability · congenital anomaly · other medically important | Safety/benefits-program SME | `assess_seriousness.py::_CRITERIA` | SNAP/Medicaid program rules / 7 CFR 273 / 42 CFR 435 | ☐ |
| Expedited processing clock | 15 calendar days (serious + unexpected, postmarket) | Safety/benefits-program SME | `assess_seriousness.py` | 7 CFR 273 / 42 CFR 435 / program-integrity (per market) | ☐ |
| Expectedness default | unknown → treated as unlisted (conservative → expedited) | Safety/benefits-program SME | `assess_seriousness.py` | Product RSI / CCDS | ☐ |
| Duplicate-key fields | product \| event \| onset \| reporter | Safety/benefits-program SME | `detect_duplicate.py` | Sponsor case-handling SOP | ☐ |
| Causality documentation | conclusion + case-specific rationale (required) | Safety/benefits-program SME | `record_causality.py` (prepare-only) | program-integrity / 21 CFR | ☐ |
| Draft narrative style | determination notice, ≤ 350 words, preserve `[REDACTED:…]` | Safety/benefits-program SME | `pv_core.py::_SYSTEM` | Sponsor narrative SOP | ☐ |
| Retention profile | (deploy choice) | IT/security | CDK `-c retention_profile=…`; `docs/RETENTION-PROFILES.md` | Sponsor record-retention schedule | ☐ |
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
