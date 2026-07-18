const G = require("./guides.js");
const { H1, H2, H3, P, bold, code, bullet, num, codeBlock, callout, table, spacer, coverAndToc, makeDoc, Packer } = G;

const cover = coverAndToc(
  ["Regulatory-Adherence Guide"],
  "Benefits Eligibility Agent on Amazon Bedrock AgentCore",
  "How the governed benefits-eligibility accelerator maps to the Social Security Act / program rules, constitutional due process, IRS Publication 1075, and StateRAMP / NIST SP 800-53 — the controls it provides, the evidence it produces, and the validation that remains the agency's responsibility. Accelerator reference; not a compliance certification or legal advice. Version 1.0 · 2026.",
  ["1. Purpose & scope", "2. The regulated workflow", "3. Frameworks in scope", "4. Due process mapping", "5. IRS Publication 1075 (FTI) mapping", "6. StateRAMP / NIST SP 800-53 mapping", "7. Separation of duties & the human gate", "8. Shared responsibility", "9. Disclaimer"]
);

const body = [
  H1("1. Purpose & scope"),
  P("This guide maps the controls implemented in the benefits-eligibility accelerator to the requirements a state or local human-services agency must satisfy. It is written for the compliance, privacy, security, and program stakeholders who decide whether an AI-assisted eligibility workflow can be adopted."),
  P([bold("What this guide is: "), "a control-to-requirement mapping showing how the accelerator supports adherence, what evidence it produces, and where the agency's own validation is required."]),
  P([bold("What this guide is not: "), "a certification, an attestation, or legal/regulatory advice. Adopting this accelerator does not by itself make a system compliant or an eligibility determination lawful. Authorization to operate, and the legal correctness of program rules and notices, remain the agency's responsibility (§8)."]),
  callout("Design principle", [["Every control below follows one rule from the regulated workflow: a qualified caseworker makes the eligibility determination and commits it — the agent intakes, de-identifies, screens, and drafts, but never self-adjudicates. The security design exists to enforce that rule and to produce the due-process evidence trail."]], G.colors.TEAL),

  H1("2. The regulated workflow"),
  P("Public-benefits adjudication decides whether an applicant qualifies for SNAP, Medicaid, TANF, unemployment insurance, or general assistance, and how fast the case must be worked. When an application arrives, a regulated workflow runs: intake the application, de-identify PII, assess eligibility and the processing clock (expedited vs. standard), draft a determination notice, obtain a qualified caseworker's review and sign-off, and commit the determination to the system of record."),
  P("The accelerator automates the intake, de-identification, screening, and drafting steps under governance, and pauses at a human sign-off gate before any determination is committed. Four regulatory areas bear on this workflow, mapped in §§4–6."),

  H1("3. Frameworks in scope"),
  table(["Framework", "Relevance to the workflow"], [
    [[bold("Social Security Act / program rules")], "Program eligibility criteria and processing timeliness (e.g. SNAP under 7 CFR Part 273, including 7-day expedited service); the qualified-caseworker determination."],
    [[bold("Constitutional due process")], "Goldberg v. Kelly — timely and adequate written notice of an adverse determination and the right to a fair hearing."],
    [[bold("IRS Publication 1075")], "Safeguarding Federal Tax Information (FTI) where tax data is used for income verification — access, audit, and disclosure controls."],
    [[bold("StateRAMP / NIST SP 800-53")], "The security-authorization framework for state systems — access control, audit, and system integrity."],
  ], [2900, 7540]),

  H1("4. Due process mapping"),
  P("Due process requires that an applicant receive timely and adequate written notice of an adverse determination and an opportunity for a fair hearing. The accelerator produces the notice and the tamper-evident record that a hearing depends on; the legal sufficiency of the notice and the hearing process remain the agency's responsibility."),
  table(["Due-process requirement", "How the accelerator addresses it", "Evidence / agency responsibility"], [
    ["Adequate written notice of the determination", "draft_notice produces a de-identified determination notice through a fail-closed output guardrail, on de-identified data only.", [{ text: "Agency: ", bold: true }, "legal review of notice language, appeal rights, and citations."]],
    ["Timely action (processing clocks)", "assess_eligibility returns the processing clock — EXPEDITED (7-day) vs STANDARD (30-day) — deterministically from the case facts, so timeliness is computed, not guessed.", "The determination + processing_clock fields; agency configures the authoritative clocks."],
    ["A defensible, reproducible determination", "assess_eligibility is a deterministic rules engine (no model) returning ELIGIBLE / INELIGIBLE / NEEDS_REVIEW with the income-vs-threshold basis, so a caseworker can defend it at a hearing.", "The auditable determination basis; agency owns the authoritative rules."],
    ["A tamper-evident record for the hearing", "Append-only DynamoDB ledger plus an S3 Object Lock (WORM) copy of each decision; the writing principal is denied delete, update, and retention bypass.", "Object Lock configuration; IAM deny policy. Agency sets the retention period."],
    ["The determination is made by a qualified person", "The commit is performed by a caseworker at the human sign-off gate; the agent cannot finalize (Cedar no-self-commit).", "Enforced by the Step Functions gate + the forbid (see §7)."],
    ["Advance notice before an ADVERSE change", "redetermine (changed-circumstances re-determination) classifies the change and, on an ADVERSE result (reduction or termination), flags that timely, adequate ADVANCE written notice and a fair-hearing right are required before the action takes effect.", [{ text: "Agency: ", bold: true }, "the advance-notice period and notice content; the commit routes through the human gate carrying that notice."]],
    ["Overpayment handling stays with a human", "detect_overpayment computes an overpayment deterministically; recovery, and any suspected-fraud referral, are human decisions — refer_fraud is forbidden to the agent (no_self_fraud_referral).", "Cedar forbid + the human gate; agency owns recovery notice and appeal rights."],
  ], [2650, 4090, 3700]),

  H1("5. IRS Publication 1075 (FTI) mapping"),
  P("Where the case uses Federal Tax Information for income verification, Pub 1075 requires strict safeguarding — restricted access, audit of every access, and protection against unauthorized disclosure. The accelerator de-identifies PII before the model or the audit sees it, and constrains access by least privilege. A safeguarding agreement and the agency's Pub 1075 program remain prerequisites for handling real FTI."),
  table(["Pub 1075 area", "How the accelerator addresses it", "Evidence / agency responsibility"], [
    ["Minimize access to FTI/PII", "The mask_pii tool runs Amazon Comprehend DetectPiiEntities to remove PII (name, SSN, address, date of birth, and more) before drafting and before the audit — fail-closed: if masking cannot run, no draft is produced.", "Comprehend detection; demo proves name/SSN redaction and the fail-closed path."],
    ["Restrict access to authorized users", "Amazon Cognito authentication with AgentCore Policy (Cedar) deny-by-default; every tool call is authorized against the caseworker's identity and group.", "Cognito pool + Cedar policies; deny strings name the firing policy."],
    ["Audit every access and disclosure", "Every governed action writes a tamper-evident record capturing INTENT → COMMITTED with a content hash and timestamp; duplicates are rejected.", "The ben-audit ledger + WORM bucket; demo proves write-once + duplicate rejection."],
    ["Least privilege", "The agent acts only within the intersection of its own and the caseworker's permissions; the finalize action is forbidden to the agent entirely.", "Cedar least-privilege permit/forbid policies."],
    ["Protect FTI in transit and at rest", "Runs inside the agency's AWS account; PII is masked before any model call; records are Object-Lock protected.", [{ text: "Agency: ", bold: true }, "safeguarding agreement, KMS/encryption, network controls, Pub 1075 program & SAR."]],
  ], [2500, 4240, 3700]),

  H1("6. StateRAMP / NIST SP 800-53 mapping"),
  P("State systems are typically authorized under StateRAMP, which is built on NIST SP 800-53 control families. The accelerator implements technical controls in the access-control, audit, and system-integrity families; the authorization package and continuous monitoring are the agency's."),
  table(["NIST 800-53 family", "How the accelerator addresses it", "Status / agency responsibility"], [
    ["AC — Access Control", "Deny-by-default Cedar authorization at the Gateway; authenticated identity via Cognito/IdP; least-privilege permits scoped to the caseworker group.", "Live in ENFORCE; agency federates its IdP and maps roles."],
    ["AU — Audit & Accountability", "Immutable WORM audit of every decision and state change (append-only DynamoDB + S3 Object Lock), with identity-tagged, OTel-correlated logs.", "Live; agency sets retention and log aggregation."],
    ["SI — System & Information Integrity", "Fail-closed PII masking and a fail-closed Bedrock output guardrail (PII anonymize + prompt-attack HIGH) on every drafted notice.", "Live; agency tunes guardrail policy."],
    ["IA — Identification & Authentication", "JWT inbound authorizer validates the caseworker before any tool runs.", [{ text: "Agency: ", bold: true }, "IdP federation, MFA, and account lifecycle."]],
    ["CA/CM — Assessment & Configuration Mgmt", "Reproducible, manifest-driven infrastructure-as-code and a 28-check governance test harness that runs in enforcement mode.", [{ text: "Agency: ", bold: true }, "the StateRAMP authorization package and continuous monitoring."]],
  ], [2500, 4240, 3700]),

  H1("7. Separation of duties & the human sign-off gate"),
  P("The single most important control for due process and program integrity is that a qualified caseworker — not the agent — makes and commits the determination. The accelerator enforces this structurally:"),
  bullet([bold("The agent cannot commit. "), "The finalize_determination action is forbidden by a Cedar policy and is hidden from the agent entirely; it is not reachable as a tool."]),
  bullet([bold("Commitment runs only through the gate. "), "The sanctioned path is a request for sign-off that starts a Step Functions workflow, which pauses until a caseworker approves."]),
  bullet([bold("The approver must differ from the requester. "), "A separation-of-duties check rejects self-approval."]),
  bullet([bold("Approvals are single-use. "), "The approval token is consumed against a durable ledger; it cannot be replayed."]),
  bullet([bold("Both ends are audited. "), "An INTENT record is written when sign-off is requested and a COMMITTED record when the determination is finalized."]),
  callout("Proven live", [["In enforcement mode: a caseworker's request to self-approve is blocked as a separation-of-duties violation; a different qualified caseworker's approval succeeds; the determination finalizes only after approval; and re-using the token is rejected."]], G.colors.MINT, "E9F5EF"),

  H1("8. Shared responsibility"),
  P("The accelerator provides the pattern, the controls, and the evidence. Authorization and the connection to the agency's real systems and rules remain the agency's."),
  table(["The accelerator provides", "The agency is responsible for"], [
    ["The governed agent, Cedar policies, and tools", "Authorization to operate (StateRAMP / ATO) and continuous monitoring"],
    ["Fail-closed PII de-identification", "IdP federation and caseworker role mapping to the workforce"],
    ["The human sign-off workflow (separation of duties)", "Validated connectors to the state benefits system of record"],
    ["The deterministic eligibility rules engine (illustrative defaults)", "The authoritative program rules/thresholds and their legal review"],
    ["The immutable WORM audit design", "Data-retention policy and records management"],
    ["Reproducible IaC + the 28-check governance harness", "Notice language, appeal rights, and the fair-hearing process (legal review)"],
    ["Documentation (this guide, the runbook, maintenance)", "Pub 1075 safeguarding program and the safeguard security report, where FTI is used"],
  ], [5220, 5220]),

  H1("9. Disclaimer"),
  P([{ text: "This document describes how an accelerator's technical controls map to selected regulatory requirements. It is provided for evaluation and architecture purposes only. It is not legal, regulatory, or compliance advice, and it is not a certification or attestation of compliance with the Social Security Act, program regulations, constitutional due process, IRS Publication 1075, StateRAMP, NIST SP 800-53, or any other authority. Eligibility determinations have direct legal consequences for applicants; the correctness of program rules, thresholds, and notices, and the lawfulness of the process, depend on the agency's validated implementation, policies, legal review, and use. The poverty guidelines and program thresholds shipped with the accelerator are illustrative federal defaults, not authoritative program rules. Consult your legal, privacy, and program functions before processing real applicant data.", italics: true, color: G.colors.MUTED, size: 19 }]),
];

const doc = makeDoc(cover, body, "Benefits AgentCore · Regulatory-Adherence Guide");
Packer.toBuffer(doc).then((b) => { require("fs").writeFileSync("Benefits-AgentCore-Regulatory-Adherence.docx", b); console.log("wrote regulatory"); });
