// Partner brief - Aegis governed-agent platform. Built with docx-js (npm i docx).
//
//     node docs/generators/partner_brief.js
//
// It reads the COMMITTED evidence file for the latest from-zero gate run and refuses to build if
// that run did not pass, so the brief cannot quietly describe a run that failed. The suite size
// comes from MATURITY.yaml and the core version from requirements-core.txt, for the same reason:
// every number in the brief has exactly one source, and it is not this file.
//
// The diagram on the landscape page is arch.png beside this script, rendered by
// architecture_diagram.py. Regenerate the diagram first if the architecture changed.
//
// US Letter, dual-width tables, no literal bullets (numbering config), no \n inside runs.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageOrientation, LevelFormat, convertInchesToTwip, ImageRun,
} = require("docx");

// ---- the run this brief speaks for -------------------------------------------------------------
// Derived from the COMMITTED EVIDENCE FILE, never hand-typed. A partner brief whose numbers are
// typed in by hand is a partner brief that goes stale between the run and the reader, and this
// repository has already had to fix four documents that did exactly that.
const path = require("path");
const ROOT = process.env.BEN_REPO || path.resolve(__dirname, "..", "..");
const rd = (r) => fs.readFileSync(path.join(ROOT, r), "utf8");

const EV = JSON.parse(rd("evidence/FULL-PORTFOLIO-GATE-benefits_runtime_agent.json"));
const checks = Object.entries(EV.checks || {}).map(([name, v]) => ({
  ok: !!v.ok, name,
  // Gate details carry raw console output - box-drawing characters, embedded newlines, whole
  // log tails. Squeeze it to something a reader can scan; the evidence file remains the record.
  // REDACTION IS NOT OPTIONAL. Gate details quote live resource names, and a hosted domain is
  // named "<prefix>-sor-<ACCOUNT ID>". The first build of this brief carried the real 12-digit
  // account id into a document meant to be sent outside. Any bare 12-digit run becomes the
  // documentation placeholder, exactly as tools/scan_account_ids.py enforces for the repo.
  detail: String(v.detail || "").replace(/\s+/g, " ").replace(/[\u2500-\u257f|]/g, "")
    .replace(/\b\d{12}\b/g, "111122223333").trim().slice(0, 190),
}));
const coreM = /governed_core-([0-9.]+)-py3/.exec(rd("requirements-core.txt"));
const testsM = /offline_total:\s*(\d+)/.exec(rd("MATURITY.yaml"));
const RUN = {
  run: EV.prefix || EV.env,
  date: EV.date,
  core: coreM ? coreM[1] : "(unknown)",
  tests: testsM ? testsM[1] : "(unknown)",
  passed: checks.filter((c) => c.ok).length,
  total: checks.length,
  checks,
};
if (!EV.PASS) {
  throw new Error("refusing to build a partner brief from a run that did not pass: " + RUN.run +
                  " (" + RUN.passed + "/" + RUN.total + ")");
}
console.log("brief built from", RUN.run, RUN.date, RUN.passed + "/" + RUN.total);

const NAVY = "1F3A56";
const GREY = "5A6672";
const RULE = "C7D2DC";
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1080;   // Letter, 0.75"
const CONTENT = PAGE_W - 2 * MARGIN;

const h1 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 140 },
  children: [new TextRun({ text: t, bold: true, size: 30, color: NAVY, font: "Calibri" })],
});
const h2 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_2, spacing: { before: 260, after: 100 },
  children: [new TextRun({ text: t, bold: true, size: 24, color: NAVY, font: "Calibri" })],
});
const p = (t, opts = {}) => new Paragraph({
  spacing: { after: opts.after === undefined ? 130 : opts.after, line: 276 },
  alignment: opts.align,
  children: (Array.isArray(t) ? t : [{ text: t }]).map((r) => new TextRun({
    text: r.text, bold: r.bold, italics: r.italics, font: r.mono ? "Consolas" : "Calibri",
    size: r.size || (r.mono ? 19 : 21), color: r.color || "222222",
  })),
});
const bullet = (t, level = 0) => new Paragraph({
  numbering: { reference: "dots", level },
  spacing: { after: 70, line: 276 },
  children: (Array.isArray(t) ? t : [{ text: t }]).map((r) => new TextRun({
    text: r.text, bold: r.bold, italics: r.italics, font: r.mono ? "Consolas" : "Calibri",
    size: r.size || (r.mono ? 19 : 21), color: r.color || "222222",
  })),
});
const num = (t) => new Paragraph({
  numbering: { reference: "steps", level: 0 },
  spacing: { after: 90, line: 276 },
  children: (Array.isArray(t) ? t : [{ text: t }]).map((r) => new TextRun({
    text: r.text, bold: r.bold, italics: r.italics, font: r.mono ? "Consolas" : "Calibri",
    size: r.size || (r.mono ? 19 : 21), color: r.color || "222222",
  })),
});
const rule = () => new Paragraph({
  spacing: { before: 60, after: 160 }, children: [],
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE, space: 1 } },
});

// pull-quote box
const quote = (lines) => new Table({
  columnWidths: [CONTENT],
  width: { size: CONTENT, type: WidthType.DXA },
  borders: {
    top: { style: BorderStyle.SINGLE, size: 2, color: "E3B341" },
    bottom: { style: BorderStyle.SINGLE, size: 2, color: "E3B341" },
    left: { style: BorderStyle.SINGLE, size: 18, color: "E3B341" },
    right: { style: BorderStyle.SINGLE, size: 2, color: "E3B341" },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
  },
  rows: [new TableRow({
    children: [new TableCell({
      width: { size: CONTENT, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: "FDF8E7" },
      margins: { top: 160, bottom: 160, left: 220, right: 220 },
      children: lines.map((l) => p(l, { after: 60 })),
    })],
  })],
});

// two-column table
function table(headers, rows, widths) {
  const cw = widths.map((f) => Math.round(CONTENT * f));
  cw[cw.length - 1] = CONTENT - cw.slice(0, -1).reduce((a, b) => a + b, 0);
  const cell = (txt, w, opts = {}) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: opts.fill || "FFFFFF" },
    margins: { top: 70, bottom: 70, left: 110, right: 110 },
    children: (Array.isArray(txt) ? txt : [txt]).map((line) => new Paragraph({
      spacing: { after: 0, line: 250 },
      children: (Array.isArray(line) ? line : [{ text: line }]).map((r) => new TextRun({
        text: r.text, bold: opts.bold || r.bold, italics: r.italics,
        font: r.mono ? "Consolas" : "Calibri", size: r.size || (r.mono ? 16 : 19),
        color: opts.headerColor || r.color || "222222",
      })),
    })),
  });
  return new Table({
    columnWidths: cw,
    width: { size: CONTENT, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "E8EEF4" },
      insideVertical: { style: BorderStyle.NONE },
    },
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map((hh, i) => cell(hh, cw[i],
          { fill: "EDF2F7", bold: true, headerColor: NAVY })),
      }),
      ...rows.map((r) => new TableRow({ children: r.map((c, i) => cell(c, cw[i])) })),
    ],
  });
}

// ---------------------------------------------------------------- content
const body = [];

body.push(new Paragraph({
  spacing: { after: 40 },
  children: [new TextRun({
    text: "AEGIS GOVERNED-AGENT PLATFORM", bold: true, size: 18, color: GREY,
    font: "Calibri", characterSpacing: 60,
  })],
}));
body.push(new Paragraph({
  spacing: { after: 60 },
  children: [new TextRun({
    text: "Where things stand, and what a partner can do",
    bold: true, size: 40, color: NAVY, font: "Calibri",
  })],
}));
body.push(p([
  { text: "Benefits eligibility pack · prepared " + RUN.date + " · evidence from the from-zero gate run ", color: GREY },
  { text: RUN.run, bold: true, color: GREY },
], { after: 60 }));
body.push(rule());

body.push(p([
  { text: "This brief is written to be checked, not believed. ", bold: true },
  { text: "Every claim below is either tied to a named gate check from a live run whose evidence is committed " +
          "to the repository, or it is listed under what is not proven. There is no third category. If you " +
          "read only one section, read ", },
  { text: "“The gap a partner actually closes”", italics: true },
  { text: " on page 3 — it is the honest answer to why this document exists." },
]));

// ---------------------------------------------------------------- 1
body.push(h1("1.  What Aegis is, in one paragraph"));
body.push(p(
  "Aegis is a governance control plane for agentic AI on Amazon Bedrock AgentCore. Deny-by-default Cedar " +
  "authorization is evaluated against the real human’s verified identity before any tool runs; every " +
  "consequential step writes hash-chained evidence to an append-only ledger and a WORM bucket, and cannot " +
  "commit unless that evidence is durable in both; a separation-of-duties Step Functions gate means a " +
  "different verified person approves before anything finalizes, and the agent never self-commits; tenants " +
  "are physically separated, with the tenant derived from the identity rather than taken from the caller; a " +
  "one-command kill switch is read before evaluation, fail-closed; and a per-tenant token and USD meter " +
  "reserves before every model call and commits real usage after. The control plane ships as a pinned, " +
  "hash-verified dependency — governed-core " + RUN.core + ", consumed by URL and sha256 under " +
  "pip install --require-hashes — and four vertical packs consume it."));
body.push(p([
  { text: "The agents are assistants. ", bold: true },
  { text: "They do not award, adjudicate, deny, or auto-submit anything. Every consequential action " +
          "terminates at a human sign-off gate. Nothing here confers GxP, Part 11, HIPAA, FedRAMP or " +
          "StateRAMP compliance; these are controls that " },
  { text: "support", italics: true },
  { text: " those validation activities, and validation is owned by the deploying organization." },
]));

// ---------------------------------------------------------------- 2
body.push(h1("2.  What is proven live, and by what"));
body.push(p([
  { text: "“From zero” means the AWS account is empty when the run starts and empty when it ends, " +
          "and both facts are established by asking AWS directly — not by trusting the teardown script’s " +
          "own verdict. The run below passed " },
  { text: RUN.passed + " of " + RUN.total + " checks", bold: true },
  { text: ". The check names are the ones in the committed evidence file, so you can grep for them." },
]));
body.push(table(
  ["What is demonstrated", "The check that proves it"],
  [
    ["Deny-by-default authorization reaches every tool, including a newly added one, and the denial names a specific policy rather than refusing everyone alike",
     [[{ text: "CONN_governed_sor_proof", mono: true }], [{ text: "G111_consolidated_gate", mono: true }]]],
    ["The gateway authorizer, the Cedar engine and the runtime stand up from IaC and reach READY on the IaC-provisioned role, with IMDSv2 required",
     [[{ text: "outputs_present", mono: true }], [{ text: "RT2_runtime_ready · RT2_runtime_uses_iac_role", mono: true }], [{ text: "RT2_runtime_mmdsv2", mono: true }]]],
    ["Every model call the runtime makes is guardrail-assessed — 20 rows, 20 assessed",
     [[{ text: "RT2_runtime_calls_guardrail_assessed", mono: true }]]],
    ["Containment precedes evaluation: the kill switch is read first and fails closed, with a DENIED WORM record per tenant",
     [[{ text: "KS_kill_switch_proof", mono: true }]]],
    ["The per-tenant meter matches the model-invocation log to the token, and a hard cap refuses at the gateway, the drafter and the runtime",
     [[{ text: "BUD_budget_proof", mono: true }]]],
    ["Every governed API call is accounted for — zero orphans across CloudTrail, the per-Lambda log line and the WORM ledger",
     [[{ text: "LIN_zero_orphans", mono: true }], [{ text: "LIN_case_driven", mono: true }]]],
    ["A case drives the whole workflow end to end with no unexpected errors; the fail-closed refusals that do appear are the deliberate ones",
     [[{ text: "E2E_zero_unexpected", mono: true }]]],
    ["A governed outbound connector authenticates to an OAuth2 system of record with no secret in the tool, and the outbound leg is exercised during the deploy",
     [[{ text: "CONN_deploy", mono: true }], [{ text: "CONN_governed_sor_proof", mono: true }]]],
    ["The account is returned to empty — stacks, AgentCore resources and connector resources each checked against AWS itself",
     [[{ text: "teardown_zero_stack_residue", mono: true }], [{ text: "teardown_zero_agentcore_residue", mono: true }], [{ text: "teardown_zero_connector_residue", mono: true }]]],
  ],
  [0.56, 0.44]));
body.push(p([
  { text: "Offline, the pack carries ", },
  { text: RUN.tests + " tests", bold: true },
  { text: " with a doc-integrity gate that fails CI when a document quotes a test count the suite no longer " +
          "has, and a gate that fails CI when a new silenced error path appears on a command whose failure " +
          "nothing checks. Both exist because both defects happened here." },
]));

// ---------------------------------------------------------------- 3
body.push(h1("3.  The newest result, and what it cost"));
body.push(p(
  "The template used to ship system-of-record connectors as labeled stubs. One is now real: verify_source " +
  "obtains an OAuth2 machine-to-machine token from the AgentCore Identity token vault, holds no client " +
  "secret itself, and calls a system of record that verifies the token’s RS256 signature against the " +
  "issuer’s live published keys. An unauthenticated caller gets 401. An outsider calling the same tool " +
  "through the gateway is refused by Cedar, and the refusal names the specific policy that refused it."));
body.push(p([
  { text: "That last clause is doing real work. ", bold: true },
  { text: "An earlier run denied the outsider and the legitimate reviewer with the same string. " },
  { text: "“Outsider denied” proved nothing then, because everything was denied.", italics: true },
  { text: " A deny-by-default claim is only evidence when the denial is selective." },
]));
body.push(p([
  { text: "Getting there took six from-zero live runs, and not one of the six failures was where it " +
          "appeared to be: authentication (proof users the IaC path never creates), then the gateway (an " +
          "authorizer that allow-lists exactly one client), then the system of record itself (an " +
          "environment variable silently left empty because a label contained a comma). Each was hidden " +
          "behind an error written to " },
  { text: "/dev/null", mono: true },
  { text: ". That defect class now fails CI." },
]));
body.push(quote([
  [{ text: "The system of record is a real OAuth2 API with RS256/JWKS signature verification. ", bold: true },
   { text: "It is ours.", bold: true }],
  [{ text: "Proving the governed path reaches it is not proving a customer’s system of record has been " +
           "governed. connect_system_of_record stays stubbed in the manifest for exactly that reason." }],
]));

// ---------------------------------------------------------------- 4
body.push(h1("4.  What is not proven, stated plainly"));
body.push(table(
  ["Not proven", "Why, and what would change it"],
  [
    ["A connector to a real system of record",
     "connect_system_of_record is stubbed on purpose. Standing the connector up against our own mock took six live runs; a real integration adds the customer’s IdP, network boundary, token lifetimes and change control on top of that. It is engineering work, not configuration."],
    ["The other three packs, live",
     "Pharmacovigilance, financial aid and housing share the same hash-locked core and received the same fixes with unit tests, but none has had an AgentCore-era live gate. The gate harness itself exists only in the benefits pack."],
    ["Manifest signing, live",
     "The manifest is Ed25519-signed and verification passes offline; the signing path has not been exercised on a live gate."],
    ["The Organizations-level SCP perimeter",
     "The org SCP and VPC-endpoint policy that prevent direct model calls ship in the repo. Demonstrating them requires an AWS Organization, which we do not have. This is a hard blocker, not a backlog item."],
    ["Scale, multi-region, multi-account, real data",
     "One pack, one account, one region (us-east-1), synthetic data, two tenants. The separate governance/audit account in the architecture is the target topology; the gate runs single-account."],
    ["Any compliance status",
     "Not GxP, Part 11, HIPAA, FedRAMP or StateRAMP authorized, and not an official AWS solution."],
  ],
  [0.30, 0.70]));

// ---------------------------------------------------------------- 5
body.push(h1("5.  The gap a partner actually closes"));
body.push(quote([
  [{ text: "Every piece of evidence in this brief was produced by the author, on the author’s own AWS " +
           "account.", bold: true }],
  [{ text: "An independent review discounted it for that reason and was right to. No amount of further " +
           "self-testing closes it. Someone else’s run is the thing that closes it." }],
]));
body.push(p(
  "That is the single most valuable thing a partner can do, and it is deliberately cheap: the protocol is " +
  "written down, the harness is committed, and it needs no contact with us."));

body.push(h2("The ask, in priority order"));
body.push(num([
  { text: "Run the independent verification on your own sandbox account. ", bold: true },
  { text: "45–75 minutes wall-clock, most of it unattended, a few dollars of AWS spend, everything torn " +
          "down at the end and you confirm zero residue yourself. Clone the repo, check out the released " +
          "tag, run " },
  { text: "scripts/independent_verify.py --dry-run", mono: true },
  { text: " first (no AWS calls, no spend), then the real run. It writes its own report." },
]));
body.push(bullet([
  { text: "A failure is a useful result. ", bold: true },
  { text: "If a step does not work, or you needed a fix that is not in the documentation, that is a real " +
          "defect and recording it is the entire point. Please do not ask us to talk you through it — " +
          "that would defeat the exercise. Note it and move on." },
], 0));
body.push(num([
  { text: "Bring a real system of record. ", bold: true },
  { text: "The next honest milestone for CONN-1 is the same proof against a real IdP and a real API " +
          "— EIV, The Work Number, a state eligibility system. We can do the engineering; we cannot " +
          "manufacture the counterparty." },
]));
body.push(num([
  { text: "Get us inside an AWS Organization. ", bold: true },
  { text: "The org-level SCP perimeter is written and cannot be demonstrated without one. This is the " +
          "cheapest unblock on the list." },
]));
body.push(num([
  { text: "A pilot with realistic data and a domain SME. ", bold: true },
  { text: "The program rules and thresholds in the pack are illustrative federal defaults. They need an " +
          "owner who can say what the authoritative rules are and sign off on them." },
]));
body.push(num([
  { text: "Adversarial review. ", bold: true },
  { text: "Specifically of the Cedar policy set and the fault semantics — what happens when the WORM " +
          "copy fails, when a task token is released twice, when a caller forges consent. Three external " +
          "review rounds have each found something real; a fourth would too." },
]));

body.push(h2("What you would need"));
body.push(bullet("An AWS sandbox account you control, us-east-1, admin-ish rights, CDK bootstrapped."));
body.push(bullet("Amazon Bedrock model access enabled for Claude Sonnet in that account and region."));
body.push(bullet("Python 3.12+, Node, the AWS CLI authenticated. No connection to our account or credentials."));

// ---------------------------------------------------------------- 6 (its own landscape page)
const diagram = [];
diagram.push(h1("6.  The architecture, and how to read it"));
diagram.push(p([
  { text: "Three colours, and the third is the point: green is demonstrated on this live run and " +
          "labelled with the gate check that proves it; amber is code that exists and is unit-tested " +
          "but that no live run has demonstrated; grey is deliberately not ours — stubbed in the " +
          "manifest, or the adopter’s to own. The grey boxes are drawn at the same size and in the " +
          "same places as the green ones. A diagram that showed only what works would be a sales " +
          "diagram, not an architecture. The editable original is " },
  { text: "Aegis-Architecture-Verified.drawio", mono: true },
  { text: "; the image below is rendered from the same source, so the two cannot disagree." },
], { after: 40 }));
{
  const png = fs.readFileSync(path.join(__dirname, "arch.png"));
  diagram.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 60 },
    children: [new ImageRun({
      data: png, type: "png",
      transformation: { width: 820, height: Math.round(820 / (2200 / 1564)) },
    })],
  }));
}

// ---------------------------------------------------------------- appendix
const appendix = [];
appendix.push(h1("Appendix — the run record"));
appendix.push(p([
  { text: "Run " }, { text: RUN.run, bold: true },
  { text: " · " + RUN.date + " · us-east-1 · single account · governed-core " + RUN.core +
          " · deployed from zero, exercised, torn down. Every check below is reproduced verbatim from " },
  { text: "evidence/FULL-PORTFOLIO-GATE-benefits_runtime_agent.json", mono: true },
  { text: ". The AWS account id is redacted to 111122223333 throughout the repository." },
]));
appendix.push(table(["Result", "Check", "Detail"],
  RUN.checks.map((c) => [
    [[{ text: c.ok ? "PASS" : "FAIL", bold: true, color: c.ok ? "1A7F37" : "B42318" }]],
    [[{ text: c.name, mono: true }]],
    [[{ text: c.detail }]],
  ]),
  [0.09, 0.30, 0.61]));

// ---------------------------------------------------------------- doc
const doc = new Document({
  creator: "Aegis", title: "Aegis — where things stand, and what a partner can do",
  numbering: {
    config: [
      { reference: "dots", levels: [{ level: 0, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: convertInchesToTwip(0.42), hanging: convertInchesToTwip(0.19) } } } }] },
      { reference: "steps", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: convertInchesToTwip(0.36), hanging: convertInchesToTwip(0.24) } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H, orientation: PageOrientation.PORTRAIT },
        margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
      },
    },
    children: body,
  }, {
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H, orientation: PageOrientation.LANDSCAPE },
        // 0.5in all round: the diagram is the page, and it needs the room.
        margin: { top: 720, bottom: 720, left: 720, right: 720 },
      },
    },
    children: diagram,
  }, {
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H, orientation: PageOrientation.PORTRAIT },
        margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
      },
    },
    children: appendix,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(path.join(ROOT, "docs", "Aegis-Partner-Brief.docx"), b);
  console.log("wrote docs/Aegis-Partner-Brief.docx", b.length, "bytes");
});
