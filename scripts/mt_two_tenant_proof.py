#!/usr/bin/env python3
"""Phase 111 - LIVE two-tenant proof for the hybrid multi-tenant control plane.

Drives the deployed AgentCore gateway as THREE identities and records verbatim results:
  * cw-a   : benefits_caseworker + tenant_pha-a  -> allowed; mask_pii routes to pha-a's OWN store
  * cw-b   : benefits_caseworker + tenant_pha-b  -> allowed; routes to pha-b's OWN store
  * cw-none: benefits_caseworker, NO tenant      -> DENIED at the gateway (require_tenant / interceptor)
Then proves physical isolation: after cw-a's call only pha-a's sanitized store holds the artifact,
and after cw-b's only pha-b's - never the other tenant's, never the base silo table.

Usage: python scripts/mt_two_tenant_proof.py --env mt --tenants pha-a,pha-b --region us-east-1
Creates disposable Cognito users (admin-create, permanent password) and authenticates via SRP.
Synthetic data only. Writes evidence JSON to stdout."""
import argparse
import json
import secrets
import sys
import time
import uuid

import boto3
import requests
from pycognito import Cognito

SYNTHETIC_CASE = ("Applicant Jane Q. Sample, SSN 900-12-3456, DOB 1990-01-01, 12 Elm St Springfield. "
                  "Household 3, monthly income 1800, liquid resources 400, no TANF.")


def outputs(cf, stack):
    d = cf.describe_stacks(StackName=stack)["Stacks"][0]
    return {o["OutputKey"]: o["OutputValue"] for o in d.get("Outputs", [])}


def make_user(idp, pool, name, groups, password):
    try:
        idp.admin_create_user(UserPoolId=pool, Username=name, MessageAction="SUPPRESS",
                              TemporaryPassword=password)
    except idp.exceptions.UsernameExistsException:
        pass
    idp.admin_set_user_password(UserPoolId=pool, Username=name, Password=password, Permanent=True)
    for g in groups:
        idp.admin_add_user_to_group(UserPoolId=pool, Username=name, GroupName=g)


def access_token(pool, client, region, name, password):
    u = Cognito(pool, client, user_pool_region=region, username=name)
    u.authenticate(password=password)
    return u.access_token


class Mcp:
    """Minimal streamable-HTTP JSON-RPC client for an AgentCore gateway."""
    def __init__(self, url, token):
        self.url, self.token, self.sid, self.n = url, token, None, 0

    def call(self, method, params=None):
        self.n += 1
        body = {"jsonrpc": "2.0", "id": self.n, "method": method}
        if params is not None:
            body["params"] = params
        h = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json",
             "Accept": "application/json, text/event-stream"}
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        r = requests.post(self.url, headers=h, json=body, timeout=60)
        self.sid = r.headers.get("Mcp-Session-Id", self.sid)
        text = r.text or ""
        payload = None
        try:
            payload = r.json()
        except Exception:
            for line in text.splitlines():           # SSE frames: data: {...}
                if line.startswith("data:"):
                    try:
                        payload = json.loads(line[5:].strip())
                    except Exception:
                        pass
        return {"status": r.status_code, "body": payload if payload is not None else text[:800]}

    def init(self):
        out = self.call("initialize", {"protocolVersion": "2025-03-26",
                                       "capabilities": {}, "clientInfo": {"name": "mt-proof", "version": "1"}})
        try:
            self.call("notifications/initialized")
        except Exception:
            pass
        return out


def count_items(ddb, table):
    try:
        return ddb.scan(TableName=table, Select="COUNT")["Count"]
    except Exception as exc:
        return "ERR:" + type(exc).__name__


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="mt")
    ap.add_argument("--tenants", default="pha-a,pha-b")
    ap.add_argument("--region", default="us-east-1")
    a = ap.parse_args()
    prefix = f"ben-{a.env}"
    ta, tb = [t.strip() for t in a.tenants.split(",")][:2]
    cf = boto3.client("cloudformation", region_name=a.region)
    idp = boto3.client("cognito-idp", region_name=a.region)
    ddb = boto3.client("dynamodb", region_name=a.region)

    ident, gw = outputs(cf, f"{prefix}-identity"), outputs(cf, f"{prefix}-gateway")
    pool, client, url = ident["UserPoolId"], ident["ClientId"], gw["GatewayUrl"]
    ev = {"env": a.env, "prefix": prefix, "tenants": [ta, tb], "gateway_url": url,
          "enforcement": gw.get("Enforcement"), "policy_engine": gw.get("PolicyEngineId"), "steps": []}

    pw = "Mt-" + secrets.token_urlsafe(12) + "aA1!"
    users = {"cw-a": ["benefits_caseworker", f"tenant_{ta}"],
             "cw-b": ["benefits_caseworker", f"tenant_{tb}"],
             "cw-none": ["benefits_caseworker"]}
    for name, groups in users.items():
        make_user(idp, pool, name, groups, pw)
    ev["steps"].append({"step": "users", "created": {k: v for k, v in users.items()}})
    time.sleep(3)

    tok = {name: access_token(pool, client, a.region, name, pw) for name in users}

    san = {ta: f"{prefix}-{ta}-sanitized-artifacts", tb: f"{prefix}-{tb}-sanitized-artifacts",
           "base": f"{prefix}-sanitized-artifacts"}
    before = {k: count_items(ddb, v) for k, v in san.items()}
    ev["steps"].append({"step": "store_counts_before", "counts": before})

    def drive(name, expect_allowed):
        m = Mcp(url, tok[name])
        init = m.init()
        lst = m.call("tools/list")
        tools = []
        if isinstance(lst["body"], dict):
            tools = [t.get("name") for t in (lst["body"].get("result", {}) or {}).get("tools", [])]
        call = m.call("tools/call", {"name": "mask-pii___mask_pii",
                                     "arguments": {"case": SYNTHETIC_CASE + " " + str(uuid.uuid4())}})
        rec = {"identity": name, "groups": users[name], "expect_allowed": expect_allowed,
               "initialize": init, "tools_list": {"status": lst["status"], "tools": tools,
                                                  "error": (lst["body"].get("error") if isinstance(lst["body"], dict) else lst["body"])},
               "mask_pii_call": call}
        ev["steps"].append(rec)
        return rec

    ra = drive("cw-a", True)
    mid = {k: count_items(ddb, v) for k, v in san.items()}
    ev["steps"].append({"step": "store_counts_after_cw-a", "counts": mid})
    rb = drive("cw-b", True)
    after = {k: count_items(ddb, v) for k, v in san.items()}
    ev["steps"].append({"step": "store_counts_after_cw-b", "counts": after})
    rn = drive("cw-none", False)

    def ok_call(r):
        b = r["mask_pii_call"]["body"]
        return r["mask_pii_call"]["status"] == 200 and isinstance(b, dict) and "error" not in b and not (
            isinstance(b.get("result"), dict) and b["result"].get("isError"))

    def grew(k, x, y):
        return isinstance(x.get(k), int) and isinstance(y.get(k), int) and y[k] > x[k]

    verdict = {
        "cw-a_allowed": ok_call(ra),
        "cw-b_allowed": ok_call(rb),
        "cw-none_denied": (not ok_call(rn)) and (rn["tools_list"]["status"] in (401, 403) or not rn["tools_list"]["tools"]
                                                 or rn["mask_pii_call"]["status"] in (401, 403)
                                                 or (isinstance(rn["mask_pii_call"]["body"], dict) and "error" in rn["mask_pii_call"]["body"])),
        "routing_cw-a_only_to_pha-a": grew(ta, before, mid) and not grew(tb, before, mid) and not grew("base", before, mid),
        "routing_cw-b_only_to_pha-b": grew(tb, mid, after) and not grew(ta, mid, after) and not grew("base", mid, after),
    }
    verdict["PASS"] = all(verdict.values())
    ev["verdict"] = verdict
    print(json.dumps(ev, indent=1, default=str))
    sys.exit(0 if verdict["PASS"] else 1)


if __name__ == "__main__":
    main()
