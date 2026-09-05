# org/ — account-boundary enforcement for the Bedrock governance perimeter

**Why this exists.** Aegis governs every call *on the governed path* preventively (AgentCore Gateway →
Cedar deny-by-default → tool Lambdas → drafter with a mandatory guardrail), and the account capture trail
(`-c capture_all=1`, #168) records every Bedrock invocation in the account by *any* principal. What no
application-layer control can do is **prevent** a principal with its own `bedrock:InvokeModel` grant from
calling Bedrock directly. That prevention lives at the organization and network boundary, and it is what
these templates provide. Without them the pack is a governed application path plus account-wide
*detection*; with them, a direct call outside the allowlist is **denied**, and any that could still occur
(management account, service-linked roles) is **captured and alarmed**.

| File | Layer | Closes |
|---|---|---|
| `scp-bedrock-runtime-perimeter.json` | AWS Organizations SCP (attach to the workload OU) | Direct model / agent / KB / async / batch invocation by any principal other than the allowlist; re-pointing or re-creating an allowlisted role; switching off invocation logging or the capture trail; guardrail / customization / provisioned-throughput changes outside the deployer |
| `vpce-policy-bedrock-runtime.json` | VPC endpoint policy on `com.amazonaws.<region>.bedrock-runtime` | In-VPC callers with foreign or unapproved credentials reaching the endpoint (the pack's own `NetworkStack` applies the same policy to its endpoint automatically) |
| `cloudtrail-advanced-event-selectors.json` | CloudTrail (org trail or per-account) | The Bedrock **data** events CloudTrail does not log by default — `ApplyGuardrail`, `InvokeAgent`, `InvokeInlineAgent`, `InvokeFlow`, `Retrieve`/`RetrieveAndGenerate`, async + bidirectional invokes, `RenderPrompt` — and the AgentCore Gateway data plane. `InvokeModel` / `Converse` are **management** events and need no selector. Identical to what `LineageStack` applies (a test pins them equal). |

## Render, then attach

```bash
python scripts/render_org_perimeter.py \
  --drafter-role-arn  arn:aws:iam::<acct>:role/<prefix>-compute-coretoolsServiceRole...   # ComputeStack output
  --runtime-role-arn  arn:aws:iam::<acct>:role/AmazonBedrockAgentCoreSDKRuntime-...       # toolkit-created
  --deployer-role-arn arn:aws:iam::<acct>:role/<your platform deployer / pipeline role>
  [--extra-principal arn:aws:iam::<acct>:role/<break-glass>]
# -> org/rendered/*.json, linted. `--lint` alone lints the shipped templates.
aws organizations create-policy --type SERVICE_CONTROL_POLICY --name aegis-bedrock-perimeter \
    --content file://org/rendered/scp-bedrock-runtime-perimeter.json
aws organizations attach-policy --policy-id p-xxxx --target-id ou-xxxx      # the WORKLOAD OU, sandbox OU first
```

Attach to a **sandbox OU first** and run the pack's live gates there before the production OU: the SCP
must leave the drafter (`guardrail_proof`) and the runtime (`cedar_perimeter_proof`) working while a
plain `aws bedrock-runtime converse` from an operator role is refused. That refusal is the acceptance test.

## What the design gets right that a naive SCP gets wrong

- **Allowlist by `aws:PrincipalArn`, never by session name.** For a role session `aws:PrincipalArn` is the
  *role* ARN, so a caller cannot satisfy it by naming its session cleverly. `aws:userId` is
  `<role-id>:<caller-chosen session name>` — an allowlist on it is defeated by
  `--role-session-name AegisGovernanceProxy-anything`.
- **No `aws:PrincipalType` in a Deny.** ANDing `PrincipalType != AssumedRole` into a Deny means *no role
  session is ever denied* — the EC2 / ECS / Lambda bypass the statement exists to stop passes straight
  through.
- **Only real IAM actions.** `bedrock:Converse` / `bedrock:ConverseStream` are API operations, not IAM
  actions; Converse authorizes as `bedrock:InvokeModel` (ConverseStream as `...WithResponseStream`). The
  Deny also covers agents, inline agents, flows, knowledge bases, async / bidirectional and **batch**
  inference — all of them invoke a model.
- **No service-linked-role exemption.** SCPs never apply to service-linked roles, so an
  `aws-service-role/*` carve-out changes nothing and only widens the pattern.
- **The allowlist is protected.** A name-pattern allowlist is self-defeating if anyone can create a role
  that matches it; statement 2 denies create / re-point / attach on the allowlisted ARNs to everyone but
  the deployer.
- **The telemetry is protected.** Statement 3 denies turning off invocation logging or stopping / editing
  the capture trail to everyone but the deployer, so the *detective* half cannot be silenced first.
- **Console / playground needs no special case.** A console user invoking a model in the Bedrock
  playground is the console principal calling `InvokeModel` — outside the allowlist, denied by statement
  1. No `aws:UserAgent` matching (which is spoofable anyway).

`scripts/render_org_perimeter.py --lint` encodes each of these as a check, and
`tests/test_org_perimeter.py` keeps the SCP that was proposed in the 2026-09-05 review as a fixture that
must keep **failing** the lint.

## Limits an auditor should know

- SCPs do not apply to the **management account** or to **service-linked roles**. Put the governance and
  workload accounts in member OUs; never run workloads in the management account. Both residual paths are
  still captured by the trail and raise `<prefix>-bedrock-perimeter-bypass`.
- An SCP is an allow-list *ceiling*, not a grant: principals still need their own IAM allow. The pack's
  drafter allow additionally requires a guardrail on every call (`Null: bedrock:GuardrailIdentifier=false`).
- **Non-Bedrock model surfaces** (SageMaker endpoints, third-party APIs over the internet) are outside
  Bedrock's perimeter by definition. The pack's `network_mode=private` has no IGW / NAT (asserted:
  0 NAT gateways) so its own compute cannot reach them; org-wide, pair this SCP with an egress control
  (Network Firewall / no-IGW SCP) — tracked in the gap register as PERIM-5.
- The reference account is a standalone account, so the SCP has been validated **statically** (lint +
  render + regression fixture) and the pack-level halves **in IaC assertions**; live SCP validation
  requires an Organization and is the first step of the customer landing-zone runbook
  (`WOGplatform/docs/16-MULTI-ACCOUNT-LANDING-ZONE.md`). MATURITY.yaml records this honestly.
