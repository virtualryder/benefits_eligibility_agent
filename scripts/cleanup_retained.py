#!/usr/bin/env python3
"""Teardown helper — removes the RETAIN'd resources a `cdk destroy` deliberately leaves behind.

RETAIN policies protect evidence in real deployments; in a DISPOSABLE validation account they leave
residue. This script deletes, for one env prefix: the audit ledger table, the WORM vault (versions
deleted with governance bypass — sandbox-demo retention only), the Cognito pool, any `<prefix>*`
secrets (force, no recovery), and schedules any `alias/<prefix>-data` CMK for deletion (KMS 7-day
minimum). It then prints a residual sweep. REFUSES to run unless --i-know-this-deletes-evidence.

Usage: python scripts/cleanup_retained.py --prefix hou-val9 --region us-east-1 --i-know-this-deletes-evidence
Exit 0 = swept clean; 2 = residue remains (fail the validation run)."""
import argparse
import json
import sys
import time as _t

import boto3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--i-know-this-deletes-evidence", action="store_true")
    a = ap.parse_args()
    if not a.i_know_this_deletes_evidence:
        ap.error("refusing: this deletes audit evidence; pass --i-know-this-deletes-evidence (validation accounts only)")
    p, region = a.prefix, a.region
    s = boto3.session.Session(region_name=region)

    ddb = s.client("dynamodb")
    for t in ddb.list_tables()["TableNames"]:
        if t.startswith(p):
            ddb.delete_table(TableName=t)
            print("deleted table", t)

    s3 = s.client("s3")

    def _locked(name):
        try:
            return s3.get_object_lock_configuration(Bucket=name)["ObjectLockConfiguration"].get(
                "ObjectLockEnabled") == "Enabled"
        except Exception:
            return False

    for b in s3.list_buckets()["Buckets"]:
        if p in b["Name"]:
            try:
                # BypassGovernanceRetention is only VALID on an Object-Lock bucket - on a plain bucket
                # it is an InvalidRequest (the 2026-09-05 residue: the observability data-events
                # bucket survived every sweep). Decide per bucket.
                bypass = {"BypassGovernanceRetention": True} if _locked(b["Name"]) else {}
                paginator = s3.get_paginator("list_object_versions")
                for page in paginator.paginate(Bucket=b["Name"]):
                    for o in page.get("Versions", []) + page.get("DeleteMarkers", []):
                        s3.delete_object(Bucket=b["Name"], Key=o["Key"], VersionId=o["VersionId"], **bypass)
                s3.delete_bucket(Bucket=b["Name"])
                print("deleted bucket", b["Name"])
            except Exception as e:
                print("bucket", b["Name"], "->", type(e).__name__, str(e)[:120])

    # log groups a destroy can leave (RETAIN'd invocation store, CloudTrail delivery group, vended logs)
    lg = s.client("logs")
    for pat in ("/aws/cloudtrail/%s" % p, "/aws/bedrock/modelinvocations/%s" % p, "/aws/lambda/%s" % p,
                "/aws/vendedlogs/bedrock-agentcore/gateway/%s" % p, "/aws/vendedlogs/%s" % p):
        for g in lg.describe_log_groups(logGroupNamePrefix=pat).get("logGroups", []):
            try:
                lg.delete_log_group(logGroupName=g["logGroupName"])
                print("deleted log group", g["logGroupName"])
            except Exception as e:
                print("log group", g["logGroupName"], "->", type(e).__name__)

    cog = s.client("cognito-idp")
    for pool in cog.list_user_pools(MaxResults=60)["UserPools"]:
        if pool["Name"].startswith(p):
            try:
                for d in cog.describe_user_pool(UserPoolId=pool["Id"])["UserPool"].get("Domain", []) or []:
                    pass
                cog.delete_user_pool(UserPoolId=pool["Id"])
                print("deleted pool", pool["Id"])
            except Exception as e:
                print("pool", pool["Id"], "->", type(e).__name__)

    sm = s.client("secretsmanager")
    for sec in sm.list_secrets(IncludePlannedDeletion=False).get("SecretList", []):
        if sec["Name"].startswith(p):
            sm.delete_secret(SecretId=sec["ARN"], ForceDeleteWithoutRecovery=True)
            print("purged secret", sec["Name"])

    kms = s.client("kms")
    for al in kms.list_aliases()["Aliases"]:
        if al["AliasName"] == f"alias/{p}-data":
            try:
                kms.schedule_key_deletion(KeyId=al["TargetKeyId"], PendingWindowInDays=7)
                print("CMK scheduled for deletion (7d)", al["TargetKeyId"])
            except Exception as e:
                print("cmk ->", type(e).__name__)

    # AgentCore engines can resurface (async deletes) — always re-sweep by name prefix. Gateways FIRST:
    # an engine attached to a surviving gateway (e.g. a FAILED gateway left by a rolled-back stack)
    # cannot be deleted, which is how ben_perim_ben_authz outlived its gate on 2026-09-05 while the
    # old sweep swallowed the error.
    engp = p.replace("-", "_")
    agentcore_residue = []
    try:
        cc = s.client("bedrock-agentcore-control")
        for g in cc.list_gateways().get("items", []):
            if g.get("name", "").startswith(p):
                try:
                    for t in cc.list_gateway_targets(gatewayIdentifier=g["gatewayId"]).get("items", []):
                        cc.delete_gateway_target(gatewayIdentifier=g["gatewayId"], targetId=t["targetId"])
                    cc.delete_gateway(gatewayIdentifier=g["gatewayId"])
                    print("deleted orphan gateway", g["name"], g.get("status"))
                except Exception as e:
                    print("gateway", g["name"], "->", type(e).__name__, str(e)[:120]); agentcore_residue.append(g["name"])
        for e in cc.list_policy_engines().get("policyEngines", []):
            if e.get("name", "").startswith(engp):
                try:
                    for pol in cc.list_policies(policyEngineId=e["policyEngineId"]).get("policies", []):
                        cc.delete_policy(policyEngineId=e["policyEngineId"], policyId=pol["policyId"])
                    # policy deletes are async: "Policy engine still contains N policies" clears in seconds
                    import time as _t
                    for attempt in range(6):
                        try:
                            cc.delete_policy_engine(policyEngineId=e["policyEngineId"]); break
                        except Exception as ex:
                            if "still contains" not in str(ex) or attempt == 5:
                                raise
                            _t.sleep(5)
                    print("deleted orphan policy engine", e["name"])
                except Exception as ex:
                    print("policy engine", e["name"], "->", type(ex).__name__, str(ex)[:120]); agentcore_residue.append(e["name"])
    except Exception as ex:
        print("agentcore sweep ->", type(ex).__name__, str(ex)[:120])

    # ---- L29: a table that is still DELETING is not residue ------------------------------------
    # The 2026-09-07 teardown reported clean=False with two "residual" tables that this same run had
    # just deleted three lines earlier. DeleteTable is ASYNCHRONOUS: the table stays in ListTables
    # with TableStatus=DELETING for a while after the call returns. Re-listing immediately therefore
    # reports a false residue - the same failure class as L25, a check misreading a good outcome.
    # Verified after the fact: both tables were gone with no further action taken.
    # A table still in DELETING is waited out (bounded); anything else is genuine residue.
    def _tables_residue(deadline_sec=180):
        end = _t.time() + deadline_sec
        while True:
            names = [t for t in ddb.list_tables()["TableNames"] if t.startswith(p)]
            if not names:
                return []
            pending = []
            for name in names:
                try:
                    if ddb.describe_table(TableName=name)["Table"]["TableStatus"] == "DELETING":
                        pending.append(name)
                except ddb.exceptions.ResourceNotFoundException:
                    pass                      # vanished between the list and the describe
                except Exception:
                    pending.append(name)      # cannot tell - treat as pending, then as residue
            settled = [n for n in names if n not in pending]
            if settled or _t.time() >= end:
                return settled if settled else pending
            _t.sleep(5)

    # residual sweep
    residue = {
        "tables": _tables_residue(),
        "lambdas": [f["FunctionName"] for f in s.client("lambda").list_functions()["Functions"]
                    if f["FunctionName"].startswith(p)],
        "stacks": [st["StackName"] for st in s.client("cloudformation").describe_stacks()["Stacks"]
                   if st["StackName"].startswith(p)],
        "pools": [q["Name"] for q in cog.list_user_pools(MaxResults=60)["UserPools"] if q["Name"].startswith(p)],
        "buckets": [b["Name"] for b in s3.list_buckets()["Buckets"] if p in b["Name"]],
        "agentcore": agentcore_residue,
        "log_groups": [g["logGroupName"] for pat in ("/aws/cloudtrail/%s" % p, "/aws/bedrock/modelinvocations/%s" % p,
                                                     "/aws/lambda/%s" % p, "/aws/vendedlogs/bedrock-agentcore/gateway/%s" % p)
                       for g in lg.describe_log_groups(logGroupNamePrefix=pat).get("logGroups", [])],
    }
    clean = not any(residue.values())
    print(json.dumps({"prefix": p, "clean": clean, "residue": residue}, indent=2))
    sys.exit(0 if clean else 2)


if __name__ == "__main__":
    main()
