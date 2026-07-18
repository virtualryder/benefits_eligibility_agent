const G = require("./guides.js");
const { H1, H2, H3, P, bold, code, bullet, num, codeBlock, callout, table, spacer, coverAndToc, makeDoc, Packer } = G;

const cover = coverAndToc(
  ["Benefits Eligibility Agent", "on Amazon Bedrock AgentCore"],
  "Solution Architect Deployment Runbook",
  "Step-by-step deployment of the governed public-benefits eligibility accelerator into an AWS account — identity, governance spine, tools, and the Runtime agent — from one manifest. Region: us-east-1. Accelerator reference; not production-certified. Version 1.1 · 2026.",
  ["1. Overview", "2. Prerequisites", "3. What gets deployed", "4. Deployment procedure", "5. Configuration reference", "6. Validation checklist", "7. Teardown", "8. Windows / Git-Bash operational notes"]
);

const body = [
  H1("1. Overview"),
  P("This runbook stands up the governed benefits-eligibility agent in an AWS account. The agent is defined by a single manifest and produced from the reusable governed-hero-agent template; the deployment is split into three lifecycles that are deployed and torn down independently:"),
  bullet([bold("Identity stack "), "— a stable Amazon Cognito user pool, app client, and test users. Long-lived; not touched by spine redeploys."]),
  bullet([bold("Governance spine "), "— the Cedar policy engine, AgentCore Gateway, tool Lambdas, Bedrock Guardrail, WORM audit stores, and the Step Functions human sign-off gate. Reproducible; stood up and torn down as a unit."]),
  bullet([bold("Runtime agent "), "— the generic Strands agent, containerized and deployed to AgentCore Runtime with a Cognito JWT inbound authorizer; its workflow prompt is rendered from the manifest."]),
  P(["The whole spine deploys with one command, proves itself with a 28-check governance demo, and tears down with zero residual. Everything is driven from ", code("agents/benefits-eligibility/manifest.yaml"), " — the engine, control library, and runtime are shared across agents."]),
  callout("Honesty boundary", [["This is an accelerator, not a production-certified system. Authorization to operate (StateRAMP / ATO), IdP federation, validated connectors to the state benefits system of record, the authoritative program rules, and legal review of notices are agency responsibilities. See the Regulatory-Adherence Guide."]], G.colors.AMBER, "FBF3E7"),

  H1("2. Prerequisites"),
  H2("2.1 AWS account & access"),
  bullet([bold("An AWS account "), "with administrative credentials configured for the AWS CLI (", code("aws sts get-caller-identity"), " must succeed)."]),
  bullet([bold("Region "), "— us-east-1 (the reference deployment; Comprehend, Bedrock models, and AgentCore are all available there)."]),
  bullet([bold("Model access "), "— enable the Anthropic Claude models in Amazon Bedrock (the notice-drafting tool defaults to the ", code("us.anthropic.claude-sonnet-4-5"), " cross-region inference profile)."]),
  H2("2.2 Tooling"),
  table(["Tool", "Version / note"], [
    [code("aws"), "AWS CLI v2.30+ (validated on 2.33)"],
    [code("python3"), "3.12 (Lambda runtime is python3.12; the Runtime toolkit needs a 3.12 venv)"],
    [code("pyyaml"), "for render.py (turns the manifest into deploy inputs)"],
    ["bash", "Any POSIX shell. On Windows, use Git-Bash (see §8)"],
    [code("agentcore"), "bedrock-agentcore-starter-toolkit (installed into the Runtime venv in Step 4)"],
  ], [2600, 7840]),
  H2("2.3 Project layout"),
  bullet([bold("lib/engine/ "), "— the manifest-driven engine: ", code("render.py"), " plus ", code("deploy.sh"), " / ", code("demo.sh"), " / ", code("destroy.sh"), " / ", code("deploy_identity.sh"), " and the sign-off state-machine template."]),
  bullet([bold("lib/controls/ "), "— the shared control library: ", code("mask_pii"), ", ", code("write_audit"), ", the sign-off Lambdas, and the MCP client. Reused by every agent."]),
  bullet([bold("lib/runtime/ "), "— the generic Strands agent (", code("agent.py"), ", ", code("Dockerfile"), ", ", code("requirements.txt"), ") and the ", code("_configure/_launch/_invoke/_obs_setup"), " helper scripts (self-locating; run from a fresh clone)."]),
  bullet([bold("agents/benefits-eligibility/ "), "— the only agent-specific part: ", code("manifest.yaml"), " (single source of truth), ", code("tools/"), " (", code("intake_application.py"), ", ", code("assess_eligibility.py"), ", ", code("benefits_core.py"), "), and ", code("demo_extra.sh"), "."]),

  bullet([bold("lib/connector/ "), "— the reusable governed OAuth connector (optional depth add-on): ", code("verify_source"), " (mints an outbound token via AgentCore Identity — no stored secret), ", code("deploy_connector.sh"), " / ", code("prove_connector.sh"), ", and a mock OAuth-protected system of record. Deployed separately from the spine."]),
  H1("3. What gets deployed"),
  table(["Component", "AWS resource(s)", "Lifecycle"], [
    [[bold("Identity")], "Cognito user pool ben-eligibility, app client ben-gw, users caseworker / approver / outsider", "Stable"],
    [[bold("Policy engine")], "AgentCore Policy engine ben_eligibility_authz (Cedar, deny-by-default)", "Spine"],
    [[bold("Gateway")], "AgentCore Gateway ben-eligibility-gw (MCP, CUSTOM_JWT, ENFORCE)", "Spine"],
    [[bold("Tools")], "Lambdas: ben-intake-application, ben-mask-pii, ben-assess-eligibility, ben-redetermine, ben-overpayment, ben-core-tools, ben-write-audit, ben-request-signoff (+ 3 sign-off Lambdas)", "Spine"],
    [[bold("Guardrail")], "Bedrock Guardrail ben-eligibility-guardrail (PII anonymize + prompt-attack)", "Spine"],
    [[bold("WORM audit")], "DynamoDB ben-audit (append-only) + S3 Object Lock bucket ben-audit-worm-<acct>-<region>", "Spine"],
    [[bold("Human gate")], "Step Functions ben-signoff + DynamoDB ben-pending-approvals", "Spine"],
    [[bold("Discovery")], "SSM parameter /ben-eligibility/gateway-url", "Spine"],
    [[bold("Runtime")], "AgentCore Runtime benefits_runtime_agent (ARM64 container via CodeBuild + ECR)", "Runtime"],
  ], [1700, 6300, 1440]),

  P([bold("Optional connector (Step 5). "), "If deployed, the governed OAuth connector adds a mock system-of-record Lambda behind API Gateway (", code("ben-sor-api"), "), an AgentCore Identity OAuth2 credential provider (", code("ben-sor-oauth"), ") and workload identity (", code("ben-verify-source-wi"), "), a Cognito M2M domain and resource server on the agent’s pool, and the governed ", code("verify_source"), " tool. Torn down separately — see §7."]),
  H1("4. Deployment procedure"),
  P([bold("Run the steps in order. "), "All commands assume you are in the project root (the folder containing ", code("lib/"), " and ", code("agents/"), "), with the AWS CLI configured for us-east-1."]),

  H2("Step 0 — Confirm the environment"),
  ...codeBlock(["aws sts get-caller-identity          # confirms credentials", "aws configure get region             # should print us-east-1", "python3 -c \"import yaml\"              # render.py needs pyyaml"]),

  H2("Step 1 — Deploy the stable identity stack"),
  P(["Creates (or reuses) the Cognito pool, app client, group, and the three test users; writes ", code("identity-state.env"), ". Idempotent and safe to re-run."]),
  ...codeBlock(["bash lib/engine/deploy_identity.sh agents/benefits-eligibility"]),
  P([bold("Result: "), "pool ", code("ben-eligibility"), ", client ", code("ben-gw"), ", users ", code("caseworker"), " / ", code("approver"), " (group ", code("benefits_caseworker"), ") and ", code("outsider"), ". Discovery URL and IDs land in ", code("identity-state.env"), "."]),

  H2("Step 2 — Deploy the governance spine"),
  P(["One idempotent command renders the manifest and builds the entire spine in the proven order: IAM roles → WORM stores → Guardrail → tool Lambdas (with per-agent resource env wired in) → policy engine → Gateway (LOG_ONLY) → targets → Cedar policies → flip to ENFORCE → human-gate Step Functions → publish the gateway URL to SSM. It sources the stable identity and writes ", code("spine-state.env"), "."]),
  ...codeBlock(["bash lib/engine/deploy.sh agents/benefits-eligibility"]),
  callout("Run cycles serialized", [["Do not run two spine deploys concurrently — overlapping runs collide on the policy-engine name. Deploy takes roughly three to four minutes end to end."]], G.colors.TEAL),

  H2("Step 3 — Prove the governance (28 checks)"),
  P("Mints caseworker and outsider tokens and exercises the full governed workflow live, in ENFORCE mode. Expect 28 passed / 0 failed."),
  ...codeBlock(["bash lib/engine/demo.sh agents/benefits-eligibility"]),
  P("The demo proves deny-by-default (caseworker ALLOW / outsider DENY), the mask-before-assess and mask-before-draft forbids and no-self-commit (each denial names the exact Cedar policy), real PII masking (name/SSN redaction), the eligibility determination + processing clock (using the authoritative 2026 HHS poverty guidelines, with the source stamped into the determination), a real Bedrock determination notice through the Guardrail, the immutable WORM audit (write-once + duplicate rejection), and the human sign-off gate (separation of duties + single-use token)."),
  P([bold("Deeper caseload workflows (step two). "), "The demo also exercises the deeper workflows, each a governed tool with its own Cedar control: ", code("redetermine"), " (a changed-circumstances re-determination that, on an ADVERSE result, flags that timely advance due-process notice is required — Goldberg v. Kelly), ", code("detect_overpayment"), " (deterministic overpayment math), and ", code("refer_fraud"), " — a consequential, human-only action the agent can never take (forbidden by ", code("no_self_fraud_referral"), "). The pattern is the point: every new high-risk action is a tool body plus its own deny-by-default forbid."]),

  H2("Step 4 — Deploy the Runtime agent"),
  P(["Create the Python 3.12 virtual environment and install the toolkit once. Use the ", code("setup_venv.sh"), " helper — it builds the venv with the correct per-OS layout (on Windows a venv exposes ", code("Scripts/"), ", not ", code("bin/"), ") and installs ", code("bedrock-agentcore"), ", ", code("bedrock-agentcore-starter-toolkit"), ", ", code("strands-agents"), ", and ", code("strands-agents-tools"), ":"]),
  ...codeBlock(["bash lib/runtime/setup_venv.sh"]),
  P(["Grant the Runtime execution role permission to read the gateway-URL parameter, configure the agent with the Cognito JWT inbound authorizer (and the manifest-rendered workflow prompt), and launch it (ARM64 build runs in CodeBuild — no local Docker needed). Each helper takes the agent directory:"]),
  ...codeBlock(["bash lib/runtime/_obs_setup.sh  agents/benefits-eligibility   # grants ssm:GetParameter", "bash lib/runtime/_configure.sh  agents/benefits-eligibility   # agentcore configure -- JWT authorizer", "bash lib/runtime/_launch.sh     agents/benefits-eligibility   # agentcore launch -- CodeBuild ARM64 -> Runtime"]),
  P([bold("Result: "), "an AgentCore Runtime ", code("benefits_runtime_agent-<id>"), " with a Cognito JWT inbound authorizer, OpenTelemetry observability enabled, and the gateway URL discovered from SSM."]),

  H2("Step 5 — Invoke and verify"),
  P("Invoke as a caseworker (full governed workflow) and as an outsider (access denied):"),
  ...codeBlock(["bash lib/runtime/_invoke.sh agents/benefits-eligibility caseworker", "bash invoke_demo.sh                          # caseworker invoke with a sample application", "bash lib/runtime/_invoke.sh agents/benefits-eligibility outsider $BEN_OUTSIDER_PW"]),
  P(["Expected: the caseworker returns a workflow summary (eligibility determination, income vs. FPL, processing clock, drafted notice, INTENT audit, PENDING_APPROVAL) and ", code("tools_available"), " that does not include ", code("finalize_determination"), " — Cedar hides the forbidden tool. The outsider returns ", code("ACCESS DENIED"), " with ", code("tools_available: []"), "."]),

  H2("Step 5 (optional) — Adversarial proof and the governed OAuth connector"),
  P(["Two optional proofs that deepen the evidence. The red-team harness re-runs the governed workflow under adversarial inputs (prompt injection, forbidden-tool coaxing, attempts to act on unmasked data) and shows every control holds — the mask-before forbids and no-self-commit fire by name:"]),
  ...codeBlock(["bash lib/engine/redteam.sh agents/benefits-eligibility          # adversarial proof: governance holds under attack"]),
  P(["The connector proves the agent authenticates to a real, OAuth2-protected dependency without holding a secret. ", code("deploy_connector.sh"), " stands up a mock system of record (", code("MOCK-SoR"), ") behind API Gateway, an AgentCore Identity OAuth2 credential provider + workload identity, and the governed ", code("verify_source"), " tool. ", code("prove_connector.sh"), " mints a token through Identity and shows the SoR rejects unauthenticated calls, the tool holds no secret, and Cedar deny-by-default extends to the connector. The mock SoR verifies the token’s ", bold("RS256 signature against the Cognito JWKS"), " (not just its claims), so a forged or tampered token is rejected:"]),
  ...codeBlock(["bash lib/connector/deploy_connector.sh agents/benefits-eligibility   # mock SoR + Identity OAuth provider + verify_source", "bash lib/connector/prove_connector.sh  agents/benefits-eligibility   # OAuth + RS256/JWKS + no stored secret + deny-by-default"]),
  H1("5. Configuration reference"),
  table(["Setting", "Where", "Default / value"], [
    ["Region", "agent.region in the manifest", "us-east-1"],
    ["Drafting model", [code("model.draft_model_id"), { text: " in the manifest", size: 19 }], "us.anthropic.claude-sonnet-4-5-20250929-v1:0"],
    ["Guardrail", "ben-eligibility-guardrail (created in deploy)", "PII=ANONYMIZE + PROMPT_ATTACK HIGH; version DRAFT"],
    ["Cognito users", "identity.users in the manifest", "caseworker / approver / outsider; passwords via env (placeholder defaults ChangeMe-*1!)"],
    ["Eligibility thresholds", [code("assess_eligibility.py"), { text: " (illustrative)", size: 19 }], "FPL base 15650, +5500/member, 130% gross limit, expedited < 150 income / 100 resources"],
    ["Gateway URL", "SSM /ben-eligibility/gateway-url", "published each spine deploy; read by the Runtime agent"],
    ["Caseworker group", "Cedar permit condition", "cognito:groups contains benefits_caseworker"],
    ["Audit stores", "controls + audit in the manifest", "DynamoDB ben-audit + S3 ben-audit-worm-<acct>-<region> (Object Lock GOVERNANCE 1d)"],
  ], [2100, 3540, 4800]),
  callout("Change the passwords, and configure the real rules, before any shared use", [["The default test-user passwords are for a private evaluation account only — rotate them (or federate a real IdP) before the environment is shared. The poverty guidelines and thresholds in assess_eligibility are illustrative federal defaults — replace them with the authoritative program rules, under legal review, before any real use. See the Maintenance Guide."]], G.colors.AMBER, "FBF3E7"),

  H1("6. Validation checklist"),
  bullet([code("deploy_identity.sh"), " → identity-state.env written; pool visible in Cognito."]),
  bullet([code("deploy.sh"), " → ends with a ", code("Gateway URL: … (mode ENFORCE)"), " line and ", code("spine-state.env"), " written."]),
  bullet([code("demo.sh"), " → ", code("28 passed, 0 failed"), " / ", code("GOVERNANCE DEMO: PASS"), "."]),
  bullet(["SSM parameter ", code("/ben-eligibility/gateway-url"), " exists and matches the live gateway."]),
  bullet(["Runtime invoke: caseworker → workflow summary; outsider → ACCESS DENIED."]),
  bullet(["CloudWatch log group ", code("/aws/bedrock-agentcore/runtimes/benefits_runtime_agent-*-DEFAULT"), " shows per-step, identity-tagged logs."]),

  H1("7. Teardown"),
  P("The spine tears down with zero residual (including the Object-Lock bucket, which requires an admin governance-bypass the tool role does not have). Identity is preserved by design — remove it explicitly only when finished."),
  ...codeBlock(["bash lib/engine/destroy.sh agents/benefits-eligibility     # spine only; leaves identity + Runtime", "# optional, full cleanup:", "#   remove the Cognito pool, and from lib/runtime: agentcore destroy"]),
  P([bold("If you deployed the connector (Step 5), "), "tear its resources down too — ", code("destroy.sh"), " removes the ", code("ben-sor-api"), " and ", code("ben-verify-source"), " Lambdas with the spine, but the API, the Identity provider and workload identity, the connector role, and the connector’s Cognito artifacts persist:"]),
  ...codeBlock(["aws apigatewayv2 delete-api --api-id <ben-sor-api id> --region us-east-1", "aws bedrock-agentcore-control delete-oauth2-credential-provider --name ben-sor-oauth --region us-east-1", "aws bedrock-agentcore-control delete-workload-identity --name ben-verify-source-wi --region us-east-1", "aws iam delete-role --role-name ben-connector-exec        # detach its policies first", "# the connector Cognito domain (ben-sor-<acct>), M2M app client, and resource server go with the user pool"]),
  callout("Export evidence first", [["The WORM audit ledger and bucket are deleted by ", code("destroy.sh"), ". Export any audit evidence you need to retain before tearing down. See the Maintenance Guide, §5."]], G.colors.TEAL),
  callout("Stop orphaned sign-off executions before teardown", [["The human sign-off gate uses a Step Functions ", code("waitForTaskToken"), " execution that can run for up to a year. If you invoke the agent and leave a determination PENDING (never approved) before tearing down, that RUNNING execution keeps the ", code("ben-signoff"), " state machine stuck in ", code("DELETING"), ", which then blocks the next deploy from re-creating a state machine of the same name (", code("StateMachineDeleting"), "). ", code("destroy.sh"), " stops RUNNING executions before deleting, but if a redeploy hits this, stop the leftover execution and let deletion finish:"]], G.colors.AMBER, "FBF3E7"),
  ...codeBlock(["aws stepfunctions list-executions --state-machine-arn arn:aws:states:<region>:<acct>:stateMachine:ben-signoff \\", "    --status-filter RUNNING --region us-east-1 --query 'executions[].executionArn' --output text", "aws stepfunctions stop-execution --execution-arn <arn> --region us-east-1   # then redeploy"]),
  callout("Multiple template agents coexist — policy names are prefixed per agent", [["AgentCore Policy names are unique per account/region, so the template prefixes every policy name with the agent’s short code (", code("fa_mask_before_assess"), ", ", code("pv_no_self_submit"), ", …) in ", code("render.py"), ". Several template agents therefore run side by side in one account with no collision (validated with three spines live at once). ", bold("Only older, unprefixed checkouts"), " shared names like ", code("mask_before_assess"), " and failed with ", code("ConflictException"), "; if you pin one, deploy a single agent at a time or update ", code("render.py"), " to prefix."]], G.colors.TEAL),

  H1("8. Windows / Git-Bash operational notes"),
  P("The reference environment is Windows with Git-Bash driving the native AWS CLI. These are the lessons that make a Windows deploy go clean the first time (some are handled inside the scripts; the first two are on you):"),
  bullet([bold("Deploy from a path WITHOUT spaces. "), "A project path like ", code("C:\\...\\eligibility agent"), " (with a space) breaks Git-Bash argument quoting when driven from PowerShell — you get errors like ", code("cd: /c/Users/.../eligibility: No such file or directory"), ". Put the project in a no-space path such as ", code("C:\\...\\benefits_eligibility_agent"), " before deploying."]),
  bullet([bold("Detached long runs — Start-Process with a single-argument runner. "), "The 3–4 minute deploy, the venv build, and the CodeBuild launch must run detached, or a foreground shell can be killed on a timeout before they finish. The pattern that works: write a tiny runner script that self-logs and changes into the no-space dir — its first lines are ", code("exec > run.log 2>&1"), ", then ", code("cd <no-space dir>"), ", then the command — and launch it with ", code("Start-Process -FilePath 'C:\\Program Files\\Git\\bin\\bash.exe' -ArgumentList '/c/…/runner.sh' -WindowStyle Hidden"), ". Pass the runner path as ", bold("one space-free argument"), ": PowerShell's ", code("-ArgumentList"), " joins a multi-token array unquoted, so ", code("'-lc','bash /c/…/runner.sh'"), " silently drops the command at the space and the process exits doing nothing. Then verify progress by ", bold("polling AWS state"), " (list the gateway/lambdas/policies) — the runner's log is block-buffered to a file, so an empty log does not mean no progress; query the resources."]),
  bullet([bold("Path conversion: "), "Git-Bash rewrites arguments that start with ", code("/"), " (e.g. SSM names) into Windows paths. The scripts set ", code("MSYS_NO_PATHCONV=1"), " where it matters — but ", code("render.py"), " runs under native Python, which cannot take ", code("/c/"), " paths, so render is invoked with ", code("MSYS_NO_PATHCONV"), " unset in a subshell."]),
  bullet([bold("Carriage returns: "), "the CLI ", code("--output text"), " picks up a trailing ", code("\\r"), "; the scripts pipe through ", code("tr -d '\\r'"), " where it matters."]),
  bullet([bold("Self-locating helpers: "), "the ", code("lib/runtime/"), " helpers resolve the agent directory before changing directory and detect the venv layout per OS (", code("Scripts/"), " vs ", code("bin/"), "), so they run from a fresh clone on any OS."]),
  bullet([bold("AgentCore toolkit: "), "export ", code("PYTHONIOENCODING=utf-8"), " and ", code("AGENTCORE_SUPPRESS_RECOMMENDATION=1"), " (already set in the helper scripts) so the rich console output does not crash under the Windows codepage."]),
  spacer(),
  P([{ text: "End of runbook. See the Regulatory-Adherence Guide for the control-to-requirement mapping and the Maintenance Guide for day-two operations.", italics: true, color: G.colors.MUTED }]),
];

const doc = makeDoc(cover, body, "Benefits AgentCore · SA Deployment Runbook");
Packer.toBuffer(doc).then((b) => { require("fs").writeFileSync("Benefits-AgentCore-SA-Runbook.docx", b); console.log("wrote runbook"); });
