#!/usr/bin/env python3
"""operator_console — the Day-2 OPERATOR CONSOLE for a governed benefits deployment.

One read-only pane a CISO/operator opens to see the live control state of a deployment:

  * CONTAINMENT — the kill switch (engaged / disengaged), from the deployment's SSM flag.
  * COST — per-tenant token/USD budget burn vs cap, from the live meter table.
  * APPROVALS — the open human-sign-off queue (pending, single-use, bound), from the register.
  * CASE LINEAGE — the most recent cases and their latest hash-chained phase, from the audit ledger.

Design: the DATA GATHERING (AWS reads, read-only) and the RENDERING (a pure function of a state dict)
are separate, so the HTML renderer is unit-tested offline with a synthetic state and the console never
needs AWS to be tested. Output is a SELF-CONTAINED HTML file (inline CSS, theme-aware, no external
dependencies) — a point-in-time snapshot the operator can open, save, or share.

Usage:
    python scripts/operator_console.py --env demo --region us-east-1 --out operator-console.html
"""
import argparse
import html
import json
import time


# ─────────────────────────── pure renderer (unit-tested offline) ───────────────────────────

_CSS = """
:root{--bg:#f7f7f5;--card:#fff;--ink:#1a1a1a;--muted:#666;--line:#e5e5e2;--ok:#0a7d33;--warn:#b26a00;--bad:#b3261e;--accent:#2b4a8b}
:root:not([data-theme=light]) @media (prefers-color-scheme:dark){}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#16171a;--card:#1f2024;--ink:#ececec;--muted:#9a9a9a;--line:#33343a;--ok:#4cc96b;--warn:#e0a24a;--bad:#f0736a;--accent:#7fa0e0}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:24px}
h1{font-size:20px;margin:0 0 2px}.sub{color:var(--muted);font-size:13px;margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.card h2{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:0 0 12px}
.big{font-size:26px;font-weight:650}
.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600}
.pill.ok{background:color-mix(in srgb,var(--ok) 16%,transparent);color:var(--ok)}
.pill.bad{background:color-mix(in srgb,var(--bad) 16%,transparent);color:var(--bad)}
.pill.warn{background:color-mix(in srgb,var(--warn) 16%,transparent);color:var(--warn)}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:600}td.num{text-align:right;font-variant-numeric:tabular-nums}
.bar{height:8px;border-radius:999px;background:var(--line);overflow:hidden;margin-top:4px}
.bar>i{display:block;height:100%}
.muted{color:var(--muted)}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.empty{color:var(--muted);font-style:italic;padding:8px 0}
footer{color:var(--muted);font-size:12px;margin-top:20px;border-top:1px solid var(--line);padding-top:12px}
"""


def _esc(v):
    return html.escape(str(v), quote=True)


def _pct_color(pct):
    return "var(--bad)" if pct >= 100 else "var(--warn)" if pct >= 85 else "var(--ok)"


def render_console(state):
    """Pure: state dict -> self-contained HTML string. No AWS, no I/O."""
    env = state.get("env", "?")
    region = state.get("region", "?")
    generated = state.get("generated_at") or int(time.time())
    ks = state.get("kill_switch") or {}
    engaged = bool(ks.get("engaged"))
    budgets = state.get("budgets") or []
    approvals = state.get("approvals") or []
    cases = state.get("cases") or []

    # containment
    ks_pill = '<span class="pill bad">ENGAGED — all agent actions refused</span>' if engaged \
        else '<span class="pill ok">DISENGAGED — normal operation</span>'
    ks_detail = ""
    if engaged:
        ks_detail = '<div class="muted" style="margin-top:8px">by %s · %s</div>' % (
            _esc(ks.get("actor", "?")), _esc(ks.get("source", "")))

    # budgets
    if budgets:
        rows = []
        for b in budgets:
            pct = float(b.get("pct_tokens") or 0)
            usd = b.get("usd") or 0
            rows.append(
                "<tr><td>%s</td><td class='num'>%s / %s</td><td class='num'>$%s</td>"
                "<td style='width:120px'><div class='num'>%.0f%%</div><div class='bar'>"
                "<i style='width:%s%%;background:%s'></i></div></td></tr>" % (
                    _esc(b.get("tenant", "?")), _esc(b.get("used_tokens", 0)), _esc(b.get("cap_tokens", "?")),
                    _esc(usd), pct, min(pct, 100), _pct_color(pct)))
        budget_html = ("<table><tr><th>Tenant</th><th class='num'>Tokens</th><th class='num'>USD</th>"
                       "<th>Burn</th></tr>%s</table>" % "".join(rows))
    else:
        budget_html = '<div class="empty">No metered spend yet.</div>'

    # approvals
    if approvals:
        rows = ["<tr><td class='mono'>%s</td><td>%s</td><td>%s</td><td class='muted'>%s</td></tr>" % (
            _esc(a.get("case_id", "?")), _esc(a.get("requester", "?")),
            ('<span class="pill warn">PENDING</span>' if a.get("status") == "PENDING"
             else _esc(a.get("status", "?"))), _esc(a.get("action", ""))) for a in approvals]
        appr_html = ("<table><tr><th>Case</th><th>Requester</th><th>Status</th><th>Action</th></tr>%s</table>"
                     % "".join(rows))
    else:
        appr_html = '<div class="empty">No open approvals.</div>'

    # cases / lineage
    if cases:
        rows = ["<tr><td class='mono'>%s</td><td>%s</td><td class='muted'>%s</td>"
                "<td class='num'>%s</td></tr>" % (
                    _esc(c.get("case_id", "?")), _esc(c.get("phase", "?")),
                    _esc(c.get("actor", "")), _esc(c.get("seq", ""))) for c in cases]
        cases_html = ("<table><tr><th>Case</th><th>Latest phase</th><th>Actor</th>"
                      "<th class='num'>Seq</th></tr>%s</table>" % "".join(rows))
    else:
        cases_html = '<div class="empty">No cases recorded yet.</div>'

    ts = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(generated))
    return """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Aegis Operator Console — %s</title>
<style>%s</style></head><body><div class="wrap">
<h1>Aegis Operator Console</h1>
<div class="sub">Deployment <b>ben-%s</b> · %s · snapshot %s</div>
<div class="grid">
  <div class="card"><h2>Containment (kill switch)</h2><div class="big">%s</div>%s</div>
  <div class="card"><h2>Per-tenant budget burn</h2>%s</div>
  <div class="card"><h2>Open approvals (human sign-off)</h2>%s</div>
  <div class="card"><h2>Recent case lineage</h2>%s</div>
</div>
<footer>Read-only snapshot generated by <span class="mono">scripts/operator_console.py</span>. Values are
point-in-time reads of the deployment's SSM kill-switch, budget meter, pending-approvals register and
hash-chained audit ledger. This console performs no writes.</footer>
</div></body></html>""" % (_esc(env), _CSS, _esc(env), _esc(region), _esc(ts),
                           ks_pill, ks_detail, budget_html, appr_html, cases_html)


# ─────────────────────────── live AWS gathering (read-only) ───────────────────────────

def _outputs(cf, stack):
    try:
        st = cf.describe_stacks(StackName=stack)["Stacks"][0]
        return {o["OutputKey"]: o["OutputValue"] for o in st.get("Outputs", [])}
    except Exception:
        return {}


def _kill_switch(ssm, prefix):
    for name in ("/%s-eligibility/kill-switch" % prefix, "/%s/kill-switch" % prefix):
        try:
            v = ssm.get_parameter(Name=name)["Parameter"]["Value"]
            d = json.loads(v) if v.strip().startswith("{") else {"engaged": v.strip().lower() in ("1", "true", "engaged")}
            d["param"] = name
            return d
        except Exception:
            continue
    return {"engaged": False, "unknown": True}


def _budgets(ddb, prefix):
    out = []
    try:
        items = ddb.Table("%s-budgets" % prefix).scan(Limit=50).get("Items", [])
        for it in items:
            used = int(it.get("used", 0))
            cap = it.get("cap")
            usd_micro = int(it.get("usd_micro", 0))
            out.append({"tenant": it.get("budget_key") or it.get("tenant") or "default",
                        "used_tokens": used, "cap_tokens": int(cap) if cap is not None else "?",
                        "pct_tokens": round(100.0 * used / int(cap), 1) if cap else 0,
                        "usd": round(usd_micro / 1_000_000.0, 4)})
    except Exception:
        pass
    return sorted(out, key=lambda b: b.get("tenant", ""))


def _approvals(ddb, prefix):
    out = []
    try:
        items = ddb.Table("%s-pending-approvals" % prefix).scan(Limit=50).get("Items", [])
        for it in items:
            out.append({"case_id": it.get("case_id", "?"), "requester": it.get("requester", "?"),
                        "status": it.get("status", "?"), "action": it.get("action", "")})
    except Exception:
        pass
    return [a for a in out if a.get("status") == "PENDING"] or out


def _cases(ddb, prefix, limit=15):
    latest = {}
    try:
        items = ddb.Table("%s-audit-ledger" % prefix).scan(Limit=400).get("Items", [])
        for it in items:
            aid = str(it.get("audit_id", ""))
            if aid.startswith("HEAD#") or aid.startswith("FINAL#"):
                continue
            cid = it.get("case_id")
            if not cid:
                continue
            seq = int(it.get("seq", 0))
            if cid not in latest or seq >= latest[cid]["seq"]:
                latest[cid] = {"case_id": cid, "phase": it.get("phase", "?"),
                               "actor": it.get("actor", ""), "seq": seq}
    except Exception:
        pass
    return sorted(latest.values(), key=lambda c: -c["seq"])[:limit]


def gather_state(env, region):
    import boto3
    prefix = "ben-%s" % env
    cf = boto3.client("cloudformation", region_name=region)
    ssm = boto3.client("ssm", region_name=region)
    ddb = boto3.resource("dynamodb", region_name=region)
    return {
        "env": env, "region": region, "generated_at": int(time.time()),
        "gateway": _outputs(cf, "%s-gateway" % prefix).get("GatewayUrl", ""),
        "kill_switch": _kill_switch(ssm, prefix),
        "budgets": _budgets(ddb, prefix),
        "approvals": _approvals(ddb, prefix),
        "cases": _cases(ddb, prefix),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="demo")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--out", default="operator-console.html")
    a = ap.parse_args()
    state = gather_state(a.env, a.region)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(render_console(state))
    print(json.dumps({"wrote": a.out, "env": a.env, "kill_switch_engaged": state["kill_switch"].get("engaged"),
                      "tenants_metered": len(state["budgets"]), "open_approvals": len(state["approvals"]),
                      "recent_cases": len(state["cases"])}, indent=1))


if __name__ == "__main__":
    main()
