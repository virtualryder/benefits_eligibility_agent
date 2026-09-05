# Gate-B Checklist — Benefits determination Assistant

*The Gate-B security posture, as CDK switches, and what remains to a captured-evidence pilot. "Built"
means the control is in the IaC and synth-validated; "live-validated" requires the EP1 run.*

| Gate-B control | Switch | Built (synth) | Live-validated (EP1, 2026-07-27, `ben-val1`) |
|---|---|---|---|
| **B1 · Private networking, ZERO public egress** — VPC, isolated subnets, AWS private endpoints only; no NAT/IGW/firewall (no external dependency) | `-c network_mode=private` | ✅ | ✅ (isolated subnets; 9 AWS private endpoints; no internet route) |
| **B2 · Customer-managed KMS** over tables, secrets, Lambda env, log groups, SNS | `-c kms=customer-managed` | ✅ | ✅ (CMK across data/secrets/logs; keys retained-by-policy at teardown) |
| **B3 · Pilot identity** — MFA ON (software token), threat protection ENFORCED, admin-create-only, zero users; OIDC IdP federation as IaC | `-c identity_mode=pilot` | ✅ | ✅ (`MfaConfiguration=ON`, software-token MFA, **0 users**) · ☐ enterprise IdP round-trip (Gate-C) |
| **B4 · PII-telemetry canary** — strict 0-hit gate across Logs/X-Ray/DLQ/SFN history | (harness) | ✅ R3-2 pass-by-reference (both directions) | ✅ **strict canary PASS — 0 leaks** (fixed a real narrative-in-state gap the canary caught; see `evidence/EP1-VALIDATION.md`) |
| **B5 · Tenant isolation** — deployment-pinned tenant HMAC-signed into artifacts | `-c tenant=<sponsor-id>` | ✅ | ✅ (deployed with `tenant=pv-example-sponsor`) |
| **B6 · Load / replay** — concurrency + exactly-once replay storm | (harness / offline) | ✅ (234 offline tests) | ☐ prod-scale live load (customer-side Gate-B exit) |

## Controls proven offline now (independent of EP1)

- Signed `sanitized_ref` masking proof; token boundary; deterministic guard set with AdverseNoticeHold;
  fail-closed data-source policy; exact-ARN IAM + tamper-Deny; no users/passwords; retention profiles; gateway
  ENFORCE with the benefits tool/policy set — all asserted by the **234-test suite** (incl. 25 CDK assertions).

## EP1 — done (2026-07-27, env `ben-val1`, us-east-1)

Live clean-account run: 7/7 stacks CREATE_COMPLETE incl. the AgentCore ENFORCE attachment;
`validate_deployment.py` → PASS; happy-path ran the full guarded controller to the human sign-off gate;
AdverseNoticeHold terminal; **strict PII canary PASS (0 leaks)**; MFA pool ON with 0 users; then torn down +
residual-swept. Full record: `evidence/EP1-VALIDATION.md`. The strict canary caught a real R3-2 gap (the
determination notice crossed execution state) which was fixed (narrative now server-side under a ref) and
re-validated before the tag was cut.

## Remaining to production (Gate C / D)

1. **Enterprise IdP** round-trip and **benefits-program SME SME sign-off** (`docs/SME-REVIEW-PACKET.md`). The
   operating-model doc bundle is complete: KEY-MANAGEMENT, RETENTION-PROFILES, INCIDENT-RESPONSE,
   AUDIT-READINESS, MCP-GATEWAY, CONFIGURATION-WORKSHEET, SME-REVIEW-PACKET (all in `docs/`).
2. **Gate D** (production): independent pen test, multi-account, prod-scale live load, authoritative program rules + system-of-record
   gateway integration.

See `PV-PILOT-READINESS-PLAN.md` for the full gate sequence.
