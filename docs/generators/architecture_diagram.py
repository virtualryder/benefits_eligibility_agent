#!/usr/bin/env python3
"""Generate the Aegis 'architecture verified' drawio diagram.

Every box carries a VERDICT, and a verdict is only ever one of three things:

    VERIFIED   proven live on a from-zero gate run, with the check that proves it named
    SHIPPED    the code exists and is unit-tested, but no live run has demonstrated it
    ADOPTER    deliberately not ours - stubbed, or the customer's to own

The point of the diagram is that the third category is drawn at the same size and in the
same places as the first. An architecture picture that shows only what works is marketing.
Regenerate both artifacts (the .drawio and the .svg rendered from the same model, so the two
cannot disagree) with:

    python docs/generators/architecture_diagram.py

Change RUN/DATE below when a newer from-zero gate run supersedes this one, and re-check every
verdict against that run's evidence rather than carrying the old ones forward. A verdict copied
from a previous run is exactly the kind of claim this diagram exists to prevent.
"""
import html
import os

RUN = "ben-fpg"
DATE = "2026-09-10"

VERIFIED = "fillColor=#d5e8d4;strokeColor=#4d7c3a;"
SHIPPED = "fillColor=#ffe6cc;strokeColor=#b06a00;"
ADOPTER = "fillColor=#eeeeee;strokeColor=#8a8a8a;fontColor=#3a3a3a;"
ZONE = ("fillColor=none;strokeColor=#8fa3b8;dashed=1;verticalAlign=top;"
        "align=left;spacingLeft=10;spacingTop=4;fontSize=13;fontStyle=1;fontColor=#33546f;")
NOTE = ("shape=note;whiteSpace=wrap;html=1;fillColor=#fff8d5;strokeColor=#d6b656;"
        "size=14;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;fontSize=10;")
ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"

BOX = ("rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
       "fontSize=11;arcSize=8;")
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=9;"
        "labelBackgroundColor=#ffffff;strokeColor=#43536b;")
EDGE_OUT = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=9;"
            "labelBackgroundColor=#ffffff;strokeColor=#1a7f37;strokeWidth=2;")
EDGE_DENY = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=9;dashed=1;"
             "labelBackgroundColor=#ffffff;strokeColor=#a11;")

cells = []
model = []          # the same content, kept structured so the SVG cannot drift from the .drawio
_id = [10]


def nid():
    _id[0] += 1
    return "n%d" % _id[0]


def esc(s):
    """Only for plain text that will be embedded in a label's HTML."""
    return s


def label(title, sub=None, verdict=None, evidence=None):
    """A box label: bold title, then the detail, then the verdict line."""
    parts = ["<b>%s</b>" % esc(title)]
    if sub:
        parts.append('<font style="font-size:10px">%s</font>' % esc(sub))
    if verdict:
        tag = {"VERIFIED": "\u2713 VERIFIED LIVE",
               "SHIPPED": "\u25cf SHIPPED, NOT PROVEN LIVE",
               "ADOPTER": "\u25cb ADOPTER-OWNED / STUBBED"}[verdict]
        line = tag
        if evidence:
            line += " \u00b7 " + esc(evidence)
        parts.append('<font style="font-size:9px;color:#2f4858">%s</font>' % line)
    return "<br>".join(parts)


def node(x, y, w, h, title, sub=None, verdict=None, evidence=None, style=None, parent="1"):
    i = nid()
    st = (style if style else BOX) + {"VERIFIED": VERIFIED, "SHIPPED": SHIPPED,
                                      "ADOPTER": ADOPTER}.get(verdict, "")
    cells.append(
        '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
        '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
        % (i, html.escape(label(title, sub, verdict, evidence), quote=True),
           st, parent, x, y, w, h))
    model.append({"kind": "box", "id": i, "x": x, "y": y, "w": w, "h": h,
                  "title": title, "sub": sub, "verdict": verdict, "evidence": evidence})
    return i


def raw(x, y, w, h, value, style, parent="1"):
    i = nid()
    cells.append(
        '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
        '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
        % (i, html.escape(value, quote=True), style, parent, x, y, w, h))
    model.append({"kind": "raw", "id": i, "x": x, "y": y, "w": w, "h": h,
                  "value": value, "style": style})
    return i


def zone(x, y, w, h, title):
    return raw(x, y, w, h, esc(title), ZONE)


def note(x, y, w, h, text):
    body = "<br>".join(esc(t) for t in text.split("\n"))
    return raw(x, y, w, h, body, NOTE)


def edge(a, b, text="", style=EDGE, exit_=None, entry=None):
    i = nid()
    st = style
    if exit_:
        st += "exitX=%s;exitY=%s;exitDx=0;exitDy=0;" % exit_
    if entry:
        st += "entryX=%s;entryY=%s;entryDx=0;entryDy=0;" % entry
    cells.append(
        '<mxCell id="%s" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
        '<mxGeometry relative="1" as="geometry"/></mxCell>'
        % (i, html.escape(text, quote=True), st, a, b))
    model.append({"kind": "edge", "id": i, "src": a, "dst": b, "text": text, "style": st})
    return i


# ---------------------------------------------------------------- title
raw(40, 20, 1560, 46,
    '<b style="font-size:19px">Aegis governed-agent architecture \u2014 what is actually verified</b><br>'
    '<font style="font-size:11px">Benefits eligibility pack \u00b7 from-zero gate run <b>%s</b> (%s), '
    'us-east-1, single account \u00b7 AWS account id redacted to 111122223333 throughout</font>' % (RUN, DATE),
    "text;html=1;align=center;verticalAlign=middle;fillColor=none;strokeColor=none;")

# ---------------------------------------------------------------- legend
raw(40, 74, 1560, 30,
    '<font style="font-size:10px">'
    '<b>How to read this.</b> Green = demonstrated on a from-zero live run and named by the gate check that proves it. '
    'Amber = the code exists and is unit-tested, but no live run has demonstrated it. '
    "Grey = deliberately not ours: stubbed in the manifest, or the adopter's to own. "
    'A picture that showed only the green boxes would be a sales diagram, not an architecture.</font>',
    "text;html=1;align=left;verticalAlign=middle;fillColor=#f4f7fa;strokeColor=#b8c6d4;spacingLeft=10;")

# ---------------------------------------------------------------- identity plane
zone(40, 130, 330, 330, "Identity plane")
idp = node(60, 170, 290, 62, "Corporate IdP",
           "Okta / Entra / Ping — OIDC or SAML",
           "ADOPTER", "reference: deploy_federation.sh")
cog = node(60, 258, 290, 66, "Cognito user pool + groups",
           "benefits_caseworker · tools_granted · tenant_*",
           "VERIFIED", "outputs_present")
user = raw(150, 356, 40, 70, esc("Caseworker / reviewer"), ACTOR)
raw(60, 434, 290, 20,
    '<font style="font-size:9px;color:#555">Two proof users per run, removed at teardown.</font>',
    "text;html=1;align=left;fillColor=none;strokeColor=none;")

# ---------------------------------------------------------------- workload account
zone(400, 130, 700, 600, "Workload account — VPC, private subnets")
gw = node(425, 172, 300, 66, "AgentCore Gateway (MCP)",
          "CUSTOM_JWT authorizer · allow-lists exactly one client",
          "VERIFIED", "G111_consolidated_gate")
cedar = node(760, 172, 315, 66, "Cedar policy engine",
             "deny-by-default · forbid wins over permit",
             "VERIFIED", "CONN_governed_sor_proof")
icept = node(425, 268, 650, 62, "Gateway request interceptor",
             "tenant DERIVED from the verified identity · consent / purpose / budget_ok "
             "stripped from the caller and injected server-side · kill switch read FIRST, fail-closed",
             "VERIFIED", "KS_kill_switch_proof · BUD_budget_proof")
rt = node(425, 360, 300, 66, "AgentCore Runtime",
          "Strands agent · IaC-provisioned role · MMDSv2 required",
          "VERIFIED", "RT2_runtime_ready · RT2_runtime_mmdsv2")
bed = node(760, 360, 315, 66, "Bedrock model + Guardrail",
           "every runtime row guardrail-assessed (20 of 20)",
           "VERIFIED", "RT2_runtime_calls_guardrail_assessed")
tools = node(425, 456, 650, 80, "Tool Lambdas (private subnets)",
             "intake_application · mask_pii (Comprehend) · assess_eligibility · redetermine · "
             "overpayment · write_audit · request_signoff / approve_signoff",
             "VERIFIED", "E2E_zero_unexpected · LIN_case_driven")
vpce = node(425, 566, 315, 62, "VPC endpoints (PrivateLink)",
            "bedrock-runtime · comprehend · states · kms · ssm · ddb · s3",
            "SHIPPED", "private mode gated separately (ben-t1)")
scp = node(760, 566, 315, 62, "Org SCP + VPC-endpoint policy",
           "denies direct model calls and evidence deletion org-wide",
           "ADOPTER", "ships under org/; org enforcement is the adopter's")

# ---------------------------------------------------------------- CONN-1
zone(400, 760, 700, 250, "CONN-1 — governed outbound to a system of record")
vs = node(425, 800, 300, 70, "verify_source Lambda",
          "holds NO client secret · exposed as a gateway target",
          "VERIFIED", "CONN_deploy (artifacts + rc + outbound)")
ident = node(760, 800, 315, 70, "AgentCore Identity",
             "token vault · workload identity → M2M client_credentials",
             "VERIFIED", "CONN_governed_sor_proof")
sor = node(425, 900, 300, 80, "MOCK system of record",
           "API Gateway + Lambda · OAuth2 · full RS256/JWKS signature verification "
           "against the live public keys",
           "VERIFIED", "rejects no-token and bad-token 401")
csor = node(760, 900, 315, 80, "connect_system_of_record",
            "the real state benefits SoR — EIV, The Work Number, a state system",
            "ADOPTER", "STUBBED in the manifest, on purpose")

# ---------------------------------------------------------------- governance / evidence
zone(1130, 130, 470, 440, "Governance & evidence")
ledger = node(1150, 172, 430, 62, "DynamoDB audit ledger",
              "append-only hash chain · CMK · per-tenant store",
              "VERIFIED", "G111_consolidated_gate")
worm = node(1150, 246, 430, 62, "S3 WORM bucket",
            "Object Lock COMPLIANCE · CMK · a commit requires the WORM copy",
            "VERIFIED", "evidence.is_durable, core 1.10.1")
sfn = node(1150, 320, 430, 62, "Step Functions sign-off",
           "separation of duties · exactly-once FINAL# marker · no self-commit",
           "VERIFIED", "G111_consolidated_gate")
kms = node(1150, 394, 430, 54, "Customer-managed KMS key",
           "rotate · audit · revoke", "VERIFIED", "ben-t1 CMK re-gate")
sep = node(1150, 462, 430, 62, "Separate governance / audit account",
           "operators of the agent cannot rewrite history",
           "ADOPTER", "target topology; this gate runs single-account")

# ---------------------------------------------------------------- observability
zone(1130, 600, 470, 410, "Observability & containment")
aegis = node(1150, 642, 430, 62, "aegis.call structured log",
             "one line per tool invocation, correlation set hashed into every WORM record",
             "VERIFIED", "LIN_zero_orphans")
trail = node(1150, 716, 430, 62, "CloudTrail management events",
             "InvokeModel / Converse captured account-wide",
             "VERIFIED", "LIN_zero_orphans: 11 invokes, 11 aegis, 0 orphans")
ks = node(1150, 790, 430, 62, "Kill switch (SSM, 15 s TTL)",
          "containment precedes evaluation · 403 + DENIED WORM record",
          "VERIFIED", "KS_kill_switch_proof")
bud = node(1150, 864, 430, 62, "Per-tenant budget meter",
           "reserve-before / commit-after · hard cap fails closed",
           "VERIFIED", "BUD_budget_proof")
td = node(1150, 938, 430, 54, "Teardown — zero residue",
          "asked of AWS directly, not taken from the script's own verdict",
          "VERIFIED", "teardown_zero_*_residue (4 checks)")

# ---------------------------------------------------------------- edges
edge(idp, cog, "OIDC / SAML  (adopter wires this)", EDGE_DENY)
edge(user, cog, "authenticate (SRP)")
edge(cog, user, "RS256 access token")
edge(user, gw, "MCP tool call · bearer = the caseworker's own JWT")
edge(gw, cedar, "principal · action · resource · server-derived context")
edge(cedar, gw, "PERMIT / DENY")
edge(gw, icept, "authorized call")
edge(icept, rt, "invoke")
edge(rt, tools, "tool invocation")
edge(rt, bed, "model call (metered, guardrailed)")
edge(tools, vpce, "AWS APIs, no public egress")
edge(tools, ledger, "append-only evidence write")
edge(tools, worm, "durable WORM copy — required before any commit")
edge(tools, sfn, "request / approve sign-off")
edge(tools, aegis, "one aegis.call per invocation")
edge(rt, vs, "verify_source, through the gateway target", EDGE_OUT)
edge(vs, ident, "get_workload_access_token → get_resource_oauth2_token", EDGE_OUT)
edge(ident, vs, "M2M bearer — never stored in the tool", EDGE_OUT)
edge(vs, sor, "Authorization: Bearer …", EDGE_OUT)
edge(sor, vs, "authoritative record, or 401", EDGE_OUT)
edge(sor, cog, "fetch JWKS · verify RS256 signature", EDGE_OUT)
edge(csor, sor, "what would replace it", EDGE_DENY)

# ---------------------------------------------------------------- notes
note(40, 490, 330, 250,
     "THE RULE THIS DIAGRAM OBEYS\n\n"
     "Measure the artifact, not the source.\n\n"
     "Every green box was read back from AWS after the\n"
     "run, or from the synthesized template - never from\n"
     "the code that was supposed to produce it. Three\n"
     "separate defects in this build were invisible in\n"
     "the source and obvious in the artifact: users the\n"
     "IaC path never creates, an authorizer that trusts\n"
     "exactly one client, and a Lambda environment left\n"
     "empty because a label contained a comma.")

note(40, 760, 330, 250,
     "WHAT THE OUTBOUND LEG COST\n\n"
     "CONN-1 took six from-zero live runs. Not one of\n"
     "the six failures was where it appeared to be:\n\n"
     "  fpa  authentication - proof users the CDK\n"
     "       path never creates\n"
     "  fpb  the gateway - the authorizer allow-lists\n"
     "       exactly ONE client\n"
     "  fpd  no diagnosis at all - the error went\n"
     "       to /dev/null\n"
     "  fpe  the SoR trusted nothing - EXPECTED_ISS\n"
     "       was empty; six retries failed silently\n"
     "  fpf  proven, 21 of 21\n\n"
     "Each was hidden behind a silenced error path. CI\n"
     "now fails when a new one appears.")

note(400, 1030, 700, 130,
     "THE TWO SENTENCES THAT BELONG TOGETHER, AND SHOULD NEVER BE QUOTED APART\n\n"
     "The system of record is a REAL OAuth2 API with RS256/JWKS signature verification.   IT IS OURS.\n\n"
     "Proving the governed path reaches it is not proving a customer's system of record has been governed.\n"
     "connect_system_of_record stays stubbed in the manifest for exactly that reason. Standing this connector up\n"
     "against our own mock took six live runs; a real integration adds the customer's IdP, network boundary, token\n"
     "lifetimes and change control on top of that. The governance is reusable. The integration is engineering work.")

note(1130, 1030, 470, 130,
     "ON DENY-BY-DEFAULT\n\n"
     "Step 3 of the connector proof denies an outsider, and\n"
     "the denial NAMES require_tenant - a specific policy.\n"
     "An earlier run denied the outsider and the legitimate\n"
     "reviewer with the same string. 'Outsider denied' proved\n"
     "nothing then, because everything was denied.\n\n"
     "A deny-by-default claim is only evidence when the\n"
     "denial is selective.")

# ---------------------------------------------------------------- emit
xml = (
    '<mxfile host="app.diagrams.net" agent="aegis-architecture-generator" version="24.7.17">\n'
    '  <diagram id="aegis-verified" name="Aegis - architecture verified">\n'
    '    <mxGraphModel dx="1600" dy="1200" grid="0" gridSize="10" guides="1" tooltips="1" '
    'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" '
    'math="0" shadow="0">\n'
    '      <root>\n'
    '        <mxCell id="0"/>\n'
    '        <mxCell id="1" parent="0"/>\n'
    + "\n".join("        " + c for c in cells) + "\n"
    '      </root>\n'
    '    </mxGraphModel>\n'
    '  </diagram>\n'
    '</mxfile>\n')

DOCS = os.environ.get("BEN_DOCS") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..")
with open(os.path.join(DOCS, "Aegis-Architecture-Verified.drawio"), "w",
          encoding="utf-8", newline="\n") as fh:
    fh.write(xml)
print("wrote Aegis-Architecture-Verified.drawio  (%d cells)" % len(cells))


# ------------------------------------------------------------------ SVG rendering
# Rendered from the SAME model that produced the .drawio above, so the picture in the partner
# brief and the editable file cannot drift apart. This is a static rendering, not a drawio
# replacement: the .drawio remains the editable original.
def _wrap(text, width_px, px_per_char):
    per = max(6, int(width_px / px_per_char))
    words, line, out = text.split(), "", []
    for w in words:
        if line and len(line) + 1 + len(w) > per:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def _strip(v):
    import re as _re
    return html.unescape(_re.sub("<[^>]+>", "", v))


def to_svg(path):
    import re as _re
    W, H = 1660, 1180
    byid = {m["id"]: m for m in model if m["kind"] != "edge"}
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
         'font-family="Helvetica,Arial,sans-serif">' % (W, H, W, H),
         '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)]

    # zones and plain text first, so boxes sit on top
    for m in model:
        if m["kind"] != "raw":
            continue
        st = m["style"]
        if st.startswith("fillColor=none;strokeColor=#8fa3b8"):        # zone
            s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#8fa3b8" '
                     'stroke-dasharray="7 5" rx="6"/>' % (m["x"], m["y"], m["w"], m["h"]))
            s.append('<text x="%d" y="%d" font-size="13" font-weight="bold" fill="#33546f">%s</text>'
                     % (m["x"] + 10, m["y"] + 17, html.escape(_strip(m["value"]))))
        elif st.startswith("shape=note"):                              # sticky note
            x, y, w, h, cut = m["x"], m["y"], m["w"], m["h"], 15
            s.append('<path d="M%d %d h%d l%d %d v%d h%d z" fill="#fff8d5" stroke="#d6b656"/>'
                     % (x, y, w - cut, cut, cut, h - cut, -(w), ))
            for i, ln in enumerate(_strip(m["value"]).split("\n") if "\n" in m["value"]
                                   else _re.split(r"<br\s*/?>", m["value"])):
                s.append('<text x="%d" y="%d" font-size="9.5" fill="#4a4020">%s</text>'
                         % (x + 9, y + 17 + i * 11.4, html.escape(_strip(ln))))
        elif st.startswith("shape=umlActor"):                          # actor
            cx, cy = m["x"] + m["w"] / 2, m["y"]
            s.append('<g stroke="#33546f" stroke-width="1.6" fill="none">'
                     '<circle cx="%.0f" cy="%.0f" r="7" fill="#33546f"/>'
                     '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>'
                     '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>'
                     '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>'
                     '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/></g>'
                     % (cx, cy + 10, cx, cy + 17, cx, cy + 40,
                        cx - 13, cy + 24, cx + 13, cy + 24,
                        cx, cy + 40, cx - 11, cy + 56, cx, cy + 40, cx + 11, cy + 56))
            s.append('<text x="%.0f" y="%d" font-size="10" text-anchor="middle" fill="#222">%s</text>'
                     % (cx, m["y"] + m["h"] + 2, html.escape(_strip(m["value"]))))
        else:                                                          # free text / legend
            fill = _re.search(r"fillColor=([^;]+)", st)
            if fill and fill.group(1) != "none":
                s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#b8c6d4" rx="3"/>'
                         % (m["x"], m["y"], m["w"], m["h"], fill.group(1)))
            big = "font-size:19px" in m["value"]
            centred = "align=center" in st
            lines = []
            for chunk in _re.split(r"<br\s*/?>", m["value"]):
                txt = _strip(chunk)
                if not txt.strip():
                    continue
                size = 17 if (big and not lines) else (10.5 if big else 10)
                for ln in _wrap(txt, m["w"] - 16, size * 0.53):
                    lines.append((ln, size, big and not lines))
            for i, (ln, size, bold) in enumerate(lines):
                anchor = 'text-anchor="middle" x="%d"' % (m["x"] + m["w"] // 2) if centred \
                    else 'x="%d"' % (m["x"] + 8)
                s.append('<text %s y="%.0f" font-size="%.1f" %s fill="#1f3a56">%s</text>'
                         % (anchor, m["y"] + 15 + i * (size + 3.5), size,
                            'font-weight="bold"' if bold else "", html.escape(ln)))

    edge_labels = []
    placed = []          # label rects already drawn, so two labels never sit on each other

    # edges
    for m in model:
        if m["kind"] != "edge":
            continue
        a, b = byid.get(m["src"]), byid.get(m["dst"])
        if not a or not b:
            continue
        ax, ay = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
        bx, by = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
        col = "#1a7f37" if "strokeColor=#1a7f37" in m["style"] else (
            "#aa1111" if "strokeColor=#a11" in m["style"] else "#43536b")
        dash = ' stroke-dasharray="5 4"' if "dashed=1" in m["style"] else ""
        wid = 1.8 if col == "#1a7f37" else 1.1
        # L-shaped routing, leaving from whichever side of the source faces the target. Straight
        # diagonals through the middle of other boxes are what makes a generated diagram unreadable.
        if abs(bx - ax) > abs(by - ay):
            ax2 = a["x"] + a["w"] if bx > ax else a["x"]
            bx2 = b["x"] if bx > ax else b["x"] + b["w"]
            pts = [(ax2, ay), ((ax2 + bx2) / 2, ay), ((ax2 + bx2) / 2, by), (bx2, by)]
        else:
            ay2 = a["y"] + a["h"] if by > ay else a["y"]
            by2 = b["y"] if by > ay else b["y"] + b["h"]
            pts = [(ax, ay2), (ax, (ay2 + by2) / 2), (bx, (ay2 + by2) / 2), (bx, by2)]
        s.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f"%s opacity="0.8"/>'
                 % (" ".join("%.0f,%.0f" % pt for pt in pts), col, wid, dash))
        if m["text"]:
            mx, my = pts[1][0], pts[1][1]
            if abs(bx - ax) > abs(by - ay):
                my = (pts[1][1] + pts[2][1]) / 2
            else:
                mx = (pts[1][0] + pts[2][0]) / 2
            lbl = m["text"]
            tw = len(lbl) * 3.9 + 8
            # Reciprocal edges (A->B and B->A) midpoint to the same spot, and a label under another
            # label is worse than no label. Nudge until clear.
            for _ in range(8):
                box = (mx - tw / 2, my - 9, mx + tw / 2, my + 3)
                if not any(box[0] < q[2] and q[0] < box[2] and box[1] < q[3] and q[1] < box[3]
                           for q in placed):
                    break
                my += 14
            placed.append((mx - tw / 2, my - 9, mx + tw / 2, my + 3))
            edge_labels.append(
                '<rect x="%.0f" y="%.0f" width="%.0f" height="12" fill="#ffffff" '
                'opacity="0.95" stroke="#dfe6ee" rx="2"/>'
                '<text x="%.0f" y="%.0f" font-size="7.6" text-anchor="middle" fill="%s">%s</text>'
                % (mx - tw / 2, my - 9, tw, mx, my, col, html.escape(lbl)))

    # boxes on top
    for m in model:
        if m["kind"] != "box":
            continue
        fill, stroke = {"VERIFIED": ("#d5e8d4", "#4d7c3a"),
                        "SHIPPED": ("#ffe6cc", "#b06a00"),
                        "ADOPTER": ("#eeeeee", "#8a8a8a")}.get(m["verdict"], ("#ffffff", "#666"))
        s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" rx="5"/>'
                 % (m["x"], m["y"], m["w"], m["h"], fill, stroke))
        lines = [(t, 10.5, True) for t in _wrap(m["title"], m["w"] - 14, 5.9)]
        if m["sub"]:
            lines += [(t, 8.8, False) for t in _wrap(m["sub"], m["w"] - 14, 4.7)]
        if m["verdict"]:
            tag = {"VERIFIED": "✓ VERIFIED LIVE", "SHIPPED": "● SHIPPED, NOT PROVEN LIVE",
                   "ADOPTER": "○ ADOPTER-OWNED / STUBBED"}[m["verdict"]]
            if m["evidence"]:
                tag += " · " + m["evidence"]
            lines += [(t, 8.0, False) for t in _wrap(tag, m["w"] - 14, 4.3)]
        total = sum(sz + 2.6 for _, sz, _ in lines)
        y = m["y"] + (m["h"] - total) / 2 + lines[0][1]
        for ln, sz, bold in lines:
            s.append('<text x="%d" y="%.1f" font-size="%.1f" %s text-anchor="middle" fill="#1a2a38">%s</text>'
                     % (m["x"] + m["w"] // 2, y, sz,
                        'font-weight="bold"' if bold else "", html.escape(ln)))
            y += sz + 2.6

    s.extend(edge_labels)
    s.append("</svg>")
    open(path, "w", encoding="utf-8").write("\n".join(s))
    print("wrote", path)


to_svg(os.path.join(DOCS, "Aegis-Architecture-Verified.svg"))
