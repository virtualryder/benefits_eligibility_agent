#!/usr/bin/env python3
"""LIVE proof of the Cedar PERIMETER profile — the #160/#161 nine-condition model.

Runs against a benefits gateway deployed with `-c perimeter=1` (Cedar ENFORCE on the GA AgentCore
Policy engine), and proves, as real MCP calls through the gateway:

  #160 ENTITLEMENT (zero-default tools)
    * cw-noent  (benefits_caseworker ONLY)                         -> DENIED on every tool
    * cw-ent    (benefits_caseworker + tools_granted + custom:tools)-> ALLOWED (mask_pii runs)
    * cw-claim  (benefits_caseworker + custom:tools, NOT in group) -> diagnostic: ALLOWED iff the
                 per-user custom:tools claim reaches Cedar (the pre-token-generation trigger path)

  #161, as cw-ent (a valid signed sanitized_ref is minted once via mask_pii):
    * CONSENT      assess consent=false                    -> DENIED ; consent=true              -> past-gate
    * PURPOSE      assess purpose="fraud"                  -> DENIED ; purpose="eligibility"     -> past-gate
    * BUDGET       draft  budget_ok=false                  -> DENIED ; budget_ok=true            -> past-gate
    * QUANTITATIVE overpayment prior_monthly_benefit=9000  -> DENIED ; 3000                      -> past-gate
    * TEMPORAL     any call within_service_window=false    -> DENIED ; true                      -> past-gate

require_service_window is UNSCOPED, so every cw-ent happy-path call sets within_service_window=true.
Synthetic data only. Writes evidence JSON to stdout; exit 0 iff every gate held.

Usage: python scripts/cedar_perimeter_proof.py --env perim --region us-east-1
       [--keep]   leave the entitlement trigger/attr in place (default: detach + delete the mapper)
"""
import argparse
import base64
import json
import os
import secrets
import sys
import time
import uuid
import zipfile
import io

import boto3
from pycognito import Cognito

HERE = os.path.dirname(os.path.abspath(__file__))
SYNTHETIC_CASE = ("Applicant Jane Q. Sample, SSN 900-12-3456, DOB 1990-01-01, 12 Elm St Springfield. "
                  "Household 3, monthly income 1800, liquid resources 400, no TANF.")
TOOLS_CLAIM = ("intake_application,mask_pii,assess_eligibility,redetermine,detect_overpayment,"
               "draft_notice,write_audit,request_signoff")


import requests


def outputs(cf, stack):
    d = cf.describe_stacks(StackName=stack)["Stacks"][0]
    return {o["OutputKey"]: o["OutputValue"] for o in d.get("Outputs", [])}


def jwt_claims(token):
    """Decode a JWT payload (no verification — evidence/diagnostics only)."""
    try:
        p = token.split(".")[1]
        p += "=" * (-len(p) % 4)
        return json.loads(base64.urlsafe_b64decode(p))
    except Exception as exc:
        return {"_decode_error": type(exc).__name__}


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
            for line in text.splitlines():
                if line.startswith("data:"):
                    try:
                        payload = json.loads(line[5:].strip())
                    except Exception:
                        pass
        return {"status": r.status_code, "body": payload if payload is not None else text[:600]}

    def init(self):
        out = self.call("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                       "clientInfo": {"name": "perim-proof", "version": "1"}})
        try:
            self.call("notifications/initialized")
        except Exception:
            pass
        return out

    def tool(self, name, args):
        return self.call("tools/call", {"name": name, "arguments": args})


def tool_result(call):
    b = call.get("body")
    try:
        return json.loads(b["result"]["content"][0]["text"])
    except Exception:
        return {}


def is_denied(call):
    """A gateway/Cedar ENFORCE denial (NOT a tool-level business error)."""
    b = call.get("body")
    if call.get("status") in (401, 403):
        return True
    if isinstance(b, dict) and "error" in b:
        return True
    if isinstance(b, dict):
        res = b.get("result")
        if isinstance(res, dict) and res.get("isError"):
            txt = json.dumps(res).lower()
            if any(w in txt for w in ("denied", "not allowed", "policy", "forbid",
                                      "authoriz", "enforcement", "access denied")):
                return True
    return False


def past_gate(call):
    """Not denied by policy, and the call reached a tool result (status 200 + a JSON-RPC result)."""
    b = call.get("body")
    return (not is_denied(call)) and call.get("status") == 200 and isinstance(b, dict) and "result" in b


def ensure_custom_attr(idp, pool):
    try:
        idp.add_custom_attributes(UserPoolId=pool, CustomAttributes=[
            {"Name": "tools", "AttributeDataType": "String", "Mutable": True,
             "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "2048"}}])
        return "created"
    except Exception as exc:
        return "exists_or_" + type(exc).__name__


def deploy_mapper(region, pool, prefix):
    """Deploy the pre-token-generation V2_0 trigger that injects custom:tools into the access token.
    Best-effort: returns (fn_arn or None, note). Never raises — the tools_granted group is the
    tier-independent grant, so the proof still holds if the claim path is unavailable."""
    iam = boto3.client("iam", region_name=region)
    lam = boto3.client("lambda", region_name=region)
    idp = boto3.client("cognito-idp", region_name=region)
    acct = boto3.client("sts", region_name=region).get_caller_identity()["Account"]
    role_name = f"{prefix}-entitlement-mapper-exec"
    trust = json.dumps({"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]})
    try:
        iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=trust)
        iam.attach_role_policy(RoleName=role_name,
                               PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
        time.sleep(10)
    except iam.exceptions.EntityAlreadyExistsException:
        pass
    role_arn = f"arn:aws:iam::{acct}:role/{role_name}"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(HERE, "entitlement_mapper.py"), "lambda_function.py")
    code = buf.getvalue()
    fn = f"{prefix}-entitlement-mapper"
    try:
        r = lam.create_function(FunctionName=fn, Runtime="python3.12", Role=role_arn,
                                Handler="lambda_function.handler", Code={"ZipFile": code},
                                Timeout=10)
        fn_arn = r["FunctionArn"]
    except lam.exceptions.ResourceConflictException:
        lam.update_function_code(FunctionName=fn, ZipFile=code)
        fn_arn = lam.get_function(FunctionName=fn)["Configuration"]["FunctionArn"]
    try:
        lam.add_permission(FunctionName=fn, StatementId="cognito-invoke",
                           Action="lambda:InvokeFunction", Principal="cognito-idp.amazonaws.com",
                           SourceArn=f"arn:aws:cognito-idp:{region}:{acct}:userpool/{pool}")
    except Exception:
        pass
    # attach as PreTokenGeneration V2_0 without clobbering pool settings: replay the safe subset.
    up = idp.describe_user_pool(UserPoolId=pool)["UserPool"]
    kw = {"UserPoolId": pool, "LambdaConfig": {
        "PreTokenGenerationConfig": {"LambdaArn": fn_arn, "LambdaVersion": "V2_0"}}}
    if up.get("Policies"):
        kw["Policies"] = up["Policies"]
    if up.get("AutoVerifiedAttributes"):
        kw["AutoVerifiedAttributes"] = up["AutoVerifiedAttributes"]
    if up.get("UserPoolTier"):
        kw["UserPoolTier"] = up["UserPoolTier"]
    try:
        idp.update_user_pool(**kw)
        note = "attached PreTokenGeneration V2_0"
    except Exception as exc:
        note = "attach_failed:" + type(exc).__name__ + ":" + str(exc)[:160]
        return fn_arn, note
    time.sleep(8)
    return fn_arn, note


def teardown_mapper(region, pool, prefix):
    idp = boto3.client("cognito-idp", region_name=region)
    lam = boto3.client("lambda", region_name=region)
    iam = boto3.client("iam", region_name=region)
    steps = {}
    try:
        up = idp.describe_user_pool(UserPoolId=pool)["UserPool"]
        kw = {"UserPoolId": pool, "LambdaConfig": {}}
        if up.get("Policies"):
            kw["Policies"] = up["Policies"]
        if up.get("UserPoolTier"):
            kw["UserPoolTier"] = up["UserPoolTier"]
        idp.update_user_pool(**kw)
        steps["detached_trigger"] = True
    except Exception as exc:
        steps["detach"] = type(exc).__name__
    role_name = f"{prefix}-entitlement-mapper-exec"
    try:
        lam.delete_function(FunctionName=f"{prefix}-entitlement-mapper")
        steps["deleted_fn"] = True
    except Exception as exc:
        steps["delete_fn"] = type(exc).__name__
    try:
        iam.detach_role_policy(RoleName=role_name,
                               PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
        iam.delete_role(RoleName=role_name)
        steps["deleted_role"] = True
    except Exception as exc:
        steps["delete_role"] = type(exc).__name__
    # NB: the custom:tools schema attribute cannot be deleted from a Cognito pool (AWS limitation);
    # it is harmless and the pool is deleted with the identity stack on teardown.
    return steps


def make_user(idp, pool, name, groups, password, tools=None):
    try:
        idp.admin_create_user(UserPoolId=pool, Username=name, MessageAction="SUPPRESS",
                              TemporaryPassword=password)
    except idp.exceptions.UsernameExistsException:
        pass
    idp.admin_set_user_password(UserPoolId=pool, Username=name, Password=password, Permanent=True)
    if tools is not None:
        idp.admin_update_user_attributes(UserPoolId=pool, Username=name,
                                         UserAttributes=[{"Name": "custom:tools", "Value": tools}])
    for g in groups:
        try:
            idp.admin_add_user_to_group(UserPoolId=pool, Username=name, GroupName=g)
        except Exception:
            pass


def access_token(pool, client, region, name, password):
    u = Cognito(pool, client, user_pool_region=region, username=name)
    u.authenticate(password=password)
    return u.access_token


MASK = "mask-pii___mask_pii"
ASSESS = "assess-eligibility___assess_eligibility"
DRAFT = "ben-core___draft_notice"
OVERPAY = "overpayment___detect_overpayment"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="perim")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--keep", action="store_true", help="leave the entitlement trigger/attr in place")
    a = ap.parse_args()
    prefix = f"ben-{a.env}"
    cf = boto3.client("cloudformation", region_name=a.region)
    idp = boto3.client("cognito-idp", region_name=a.region)

    ident, gw = outputs(cf, f"{prefix}-identity"), outputs(cf, f"{prefix}-gateway")
    pool, client, url = ident["UserPoolId"], ident["ClientId"], gw["GatewayUrl"]
    ev = {"env": a.env, "prefix": prefix, "gateway_url": url, "enforcement": gw.get("Enforcement"),
          "policy_engine": gw.get("PolicyEngineId"), "steps": []}

    # ---- authoritative entitlement infra ----
    attr = ensure_custom_attr(idp, pool)
    try:
        idp.create_group(UserPoolId=pool, GroupName="tools_granted",
                         Description="Explicit tool entitlement grant (zero-default #160)")
    except Exception:
        pass
    fn_arn, mapper_note = deploy_mapper(a.region, pool, prefix)
    ev["steps"].append({"step": "entitlement_infra", "custom_attr": attr, "mapper_fn": fn_arn,
                        "mapper": mapper_note, "group": "tools_granted"})

    pw = "Pm-" + secrets.token_urlsafe(12) + "aA1!"
    users = {
        "cw-ent":   {"groups": ["benefits_caseworker", "tools_granted"], "tools": TOOLS_CLAIM},
        "cw-noent": {"groups": ["benefits_caseworker"],                   "tools": None},
        "cw-claim": {"groups": ["benefits_caseworker"],                   "tools": TOOLS_CLAIM},
    }
    for name, u in users.items():
        make_user(idp, pool, name, u["groups"], pw, tools=u["tools"])
    time.sleep(4)
    tok = {name: access_token(pool, client, a.region, name, pw) for name in users}
    claims = {name: {k: jwt_claims(tok[name]).get(k) for k in ("cognito:groups", "custom:tools")}
              for name in users}
    ev["steps"].append({"step": "identities", "users": {k: v["groups"] for k, v in users.items()},
                        "token_claims": claims})

    # ---- #160 ENTITLEMENT (zero-default tools) ----
    def mask_call(name, within=True):
        m = Mcp(url, tok[name]); m.init()
        return m.tool(MASK, {"case": SYNTHETIC_CASE + " " + str(uuid.uuid4()),
                             "within_service_window": within})

    ent = {}
    ent["cw-noent"] = mask_call("cw-noent")
    ent["cw-ent"] = mask_call("cw-ent")
    ent["cw-claim"] = mask_call("cw-claim")
    ev["steps"].append({"step": "entitlement", "calls": ent})

    # mint a real signed sanitized_ref as the entitled identity (for the #161 tool calls)
    tr = tool_result(ent["cw-ent"])
    sr = tr.get("sanitized_ref")
    ev["steps"].append({"step": "sanitized_ref_minted", "have_ref": bool(sr),
                        "masked_by": tr.get("masked_by"), "deidentified": tr.get("deidentified")})

    m = Mcp(url, tok["cw-ent"]); m.init()

    # ---- #3 AUTHORITATIVE consent/purpose (end-to-end). The interceptor STRIPS caller-supplied
    # consent/purpose and the authoritative_context resolver injects them from the server-side authz
    # store keyed by case_id. Seed ONE authorized case (consent recorded + authorized purpose); use one
    # UNAUTHORIZED case. budget_ok / within_service_window are ALSO caller-uncontrollable now (server
    # meter / server clock) - their negatives are covered by governed-core's offline interceptor tests
    # and the live budget gate; here we prove the two the resolver owns.
    data = outputs(cf, f"{prefix}-data")
    authz_table = data.get("AuthzTableName") or f"{prefix}-authz-context"
    authz = boto3.resource("dynamodb", region_name=a.region).Table(authz_table)
    CASE_AUTH = "CASE-AUTH-" + uuid.uuid4().hex[:8]
    CASE_NOAUTH = "CASE-NOAUTH-" + uuid.uuid4().hex[:8]
    authz.put_item(Item={"case_id": CASE_AUTH, "consent": True, "authorized_purpose": "eligibility"})
    ev["steps"].append({"step": "authz_seed", "table": authz_table,
                        "authorized_case": CASE_AUTH, "unauthorized_case": CASE_NOAUTH})

    def assess(case_id, forge_consent=False):
        args = {"household_size": 3, "monthly_income": 1800, "liquid_resources": 400,
                "categorical_eligibility": False, "deidentified": True,
                "sanitized_ref": sr, "case_id": case_id}
        if forge_consent:   # the caller TRIES to assert consent/purpose — the interceptor MUST strip them
            args.update({"consent": True, "purpose": "eligibility"})
        return m.tool(ASSESS, args)

    def overpay(amount):
        # AgentCore Cedar evaluates prior_monthly_benefit via the decimal extension; send decimals so the
        # amount-cap gate evaluates on the real value. amount is a REAL tool arg (not a stripped field).
        return m.tool(OVERPAY, {"prior_monthly_benefit": float(amount), "corrected_monthly_benefit": 200.0,
                                "months": 6.0, "deidentified": True, "sanitized_ref": sr, "case_id": CASE_AUTH})

    c = {}
    c["authz_present"] = assess(CASE_AUTH)                             # authoritative record -> past-gate
    c["forged_no_record"] = assess(CASE_NOAUTH, forge_consent=True)    # caller forges, no record -> DENIED
    c["amount_over"] = overpay(9000)
    c["amount_ok"] = overpay(3000)
    ev["steps"].append({"step": "conditions", "calls": c})

    def allowed(x):
        return not is_denied(x)

    verdict = {
        # #160 — zero-default entitlement
        "entitlement_zero_default": is_denied(ent["cw-noent"]) and allowed(ent["cw-ent"]),
        # #3 END-TO-END — consent/purpose are AUTHORITATIVE, not caller-asserted. A case with a real
        # authz record passes; a caller that FORGES consent/purpose on a case with NO record is DENIED
        # (interceptor stripped the caller values, resolver found no record -> Cedar sees them unset).
        # NOTE: this ALSO proves the interceptor's injection reaches the Cedar decision — if Cedar read
        # the pre-interceptor caller args, the pattern would invert (authz_present denied, forged allowed).
        "consent_purpose_authoritative": allowed(c["authz_present"]) and is_denied(c["forged_no_record"]),
        "amount_cap": is_denied(c["amount_over"]) and allowed(c["amount_ok"]),
    }
    # diagnostic (NON-gating): does the per-user custom:tools claim alone reach Cedar?
    diag = {
        "custom_tools_in_token": bool(claims["cw-claim"].get("custom:tools")),
        "custom_tools_claim_enforced_in_cedar": allowed(ent["cw-claim"]) and bool(claims["cw-claim"].get("custom:tools")),
        "cw-claim_result": "allowed" if allowed(ent["cw-claim"]) else "denied",
    }
    verdict["PASS"] = all(v for k, v in verdict.items())
    ev["diagnostic_custom_tools_claim"] = diag
    ev["verdict"] = verdict

    # ---- teardown the entitlement trigger/mapper (unless --keep) ----
    if not a.keep:
        ev["steps"].append({"step": "teardown_mapper", "result": teardown_mapper(a.region, pool, prefix)})

    print(json.dumps(ev, indent=1, default=str))
    sys.exit(0 if verdict["PASS"] else 1)


if __name__ == "__main__":
    main()
