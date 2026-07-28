# Independent Verification Protocol

*For a **third party** — another AWS SA, a partner SA, or the customer's engineer. **Not** the author.*

---

## Why you are being asked to do this

Every piece of evidence in this repository was produced by the author on the author's own account. An
independent review correctly discounted it for that reason, and named this the **single biggest
credibility gap** in the project. Your run is the thing that closes it.

You are not being asked to agree with the design. You are being asked to answer one question:

> **Does the released tag deploy and behave as documented, on an account the author does not control,
> using only the written instructions?**

A **failure is a useful result.** If a step doesn't work, or you needed a fix that isn't in the docs,
that is a real defect and recording it is the whole point. Please do not ask the author to talk you
through it — that would defeat the exercise. Note it and move on.

## What it costs and how long

~45–75 minutes wall-clock, most of it unattended. Real AWS spend on a sandbox account: VPC interface
endpoints, Lambda, Step Functions, DynamoDB, KMS, one Bedrock call and one Comprehend call — a few
dollars. **Everything is torn down at the end**; you confirm zero residual before you finish.

## Prerequisites

- An AWS **sandbox** account you control, `us-east-1`, with admin-ish rights, and **CDK bootstrapped**
  (`npx aws-cdk@2 bootstrap aws://<account>/us-east-1`).
- **Amazon Bedrock model access enabled** for Claude Sonnet in that account/region (the drafter calls it).
- Python 3.12+, Node (for `npx`), the AWS CLI authenticated.
- No connection to the author's account, credentials, or environment.

## Run it

```bash
git clone https://github.com/virtualryder/benefits_eligibility_agent
cd benefits_eligibility_agent
git checkout v0.1.1-pilot-rc1          # the tag, never main — the harness enforces this
pip install -r cdk/requirements.txt

# 1) sanity check first: no AWS calls, no spend
python scripts/independent_verify.py --dry-run

# 2) the real run
python scripts/independent_verify.py --verifier "Your Name <you@example.com>" --env iv1
```

The harness runs, in order: **preflight** (on the tag, clean tree, toolchain, AWS identity) → **offline
suite** → **cdk deploy --all** (all Gate-B switches) → **validate_deployment** → **strict PII canary** →
**happy path** → **adverse-notice hold** → **destroy --all** → **residual sweep**. It writes
`evidence/independent-verification-report.json`.

Record anything noteworthy as you go:

```bash
python scripts/independent_verify.py --verifier "..." --env iv1 \
  --note "step X needed an undocumented fix: ..." --note "docs said Y, actual was Z"
```

Your AWS account id is **never written to the report** — only a truncated hash, so runs are
distinguishable without disclosing the account.

## What each step must show

| Step | Expected result | What it proves |
|---|---|---|
| `preflight.on_release_tag` | you are on `v0.1.1-pilot-rc1` with a clean tree | you verified the *released* artifact, not a working copy |
| `offline.pytest` | all tests pass | the suite is honest about its own count |
| `deploy.cdk_all` | 7 stacks reach `*_COMPLETE` | the IaC deploys unaided, incl. the AgentCore/Cedar **ENFORCE** attachment |
| `validate.deployment` | `deployment_status: PASS` | masking is proven by a signed ref; a **forged ref is refused**; ingest is pass-by-reference; the workflow reaches the human gate |
| `canary.strict_zero_pii` | `verdict: PASS`, `leaks: {}` | no PII marker in CloudWatch Logs, X-Ray, DLQs **or Step Functions history** |
| `happy.reaches_human_gate_and_pauses` | status `RUNNING`, states include `HumanSignoff` | the assistant **stops for a human** — it never self-commits |
| `adverse.holds_without_advance_notice` | states include `AdverseNoticeHold`, and **not** `DraftNotice`/`HumanSignoff` | due process is enforced by the platform (*Goldberg v. Kelly*), not by the model |
| `teardown.zero_residual` | `residual_stacks: []` | nothing is left running or billing |

## Optional but valuable adversarial checks

If you have time, try to break it and record what happens:

1. **Forge a masking reference** — take a genuine `sanitized_ref` from `mask-pii`, change one character of
   `sig`, and call `ben-iv1-workflow-guards` with `{"guard":"deidentified","sanitized_ref":<forged>}`.
   Expected: `ok:false`.
2. **Skip masking** — call `assess-eligibility` with `{"deidentified": true}` and no signed ref.
   Expected: refusal (a boolean is never accepted as proof).
3. **Check the network claim** — confirm the VPC has **no NAT gateway, no internet gateway, no firewall**,
   and that the tool Lambdas sit in isolated subnets.
4. **Check identity** — confirm the Cognito pool has **0 users** and `MfaConfiguration = ON`.
5. **Try to reach the raw application from execution state** — inspect a Step Functions execution history
   and confirm it carries only opaque `case-…` / signed refs, never applicant text or the drafted notice.

## Report your result

1. Fill in **`evidence/INDEPENDENT-VERIFICATION-RESULT.md`** (name, date, region, verdict, per-step
   outcomes, and — importantly — every discrepancy or undocumented fix).
2. Attach `evidence/independent-verification-report.json`.
3. Open a PR, or send both files to the author.

Until that signed result exists, `docs/VALIDATED-MATRIX.md` must continue to state that independent
verification has **not** been done. A CI gate enforces that, so the claim cannot be made on your behalf.
