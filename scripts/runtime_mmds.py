#!/usr/bin/env python3
"""runtime_mmds - MMDSv2 on the AgentCore Runtime, EXPLICIT and asserted (fourth review R4-6, 2026-09-06).

AWS rejects AgentCore Runtime invocations from 2026-06-30 unless `metadataConfiguration.requireMMDSV2` is
true (IMDSv2-style token-required instance metadata inside the runtime microVM - a defense against SSRF-
style credential theft from the container). The starter toolkit may set it by default, but customer
readiness cannot rest on an undocumented default, so:

  --assert   read the deployed runtime and print {requireMMDSV2: bool}; exit 0 only when it is true
  --enforce  if it is not true, UpdateAgentRuntime with the SAME artifact / role / network / authorizer /
             protocol / env and metadataConfiguration.requireMMDSV2=true, wait for READY, then assert

Usage: python scripts/runtime_mmds.py --runtime-id <id> [--region us-east-1] (--assert | --enforce)
The full-portfolio gate calls --enforce right after launch and records the result as RT2_runtime_mmdsv2.
"""
import argparse
import json
import sys
import time

import boto3


def current(acc, rid):
    r = acc.get_agent_runtime(agentRuntimeId=rid)
    return r, bool((r.get("metadataConfiguration") or {}).get("requireMMDSV2"))


def enforce(acc, rid, r):
    kw = {"agentRuntimeId": rid, "agentRuntimeArtifact": r["agentRuntimeArtifact"], "roleArn": r["roleArn"],
          "networkConfiguration": r["networkConfiguration"], "metadataConfiguration": {"requireMMDSV2": True}}
    for k in ("authorizerConfiguration", "protocolConfiguration", "environmentVariables", "requestHeaderConfiguration",
              "lifecycleConfiguration", "description"):
        if r.get(k):
            kw[k] = r[k]
    acc.update_agent_runtime(**kw)
    for _ in range(60):
        st = acc.get_agent_runtime(agentRuntimeId=rid)["status"]
        if st == "READY":
            return st
        if st in ("CREATE_FAILED", "UPDATE_FAILED", "DELETE_FAILED"):
            return st
        time.sleep(10)
    return "TIMEOUT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runtime-id", required=True)
    ap.add_argument("--region", default="us-east-1")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--assert", dest="check", action="store_true")
    g.add_argument("--enforce", action="store_true")
    a = ap.parse_args()
    acc = boto3.client("bedrock-agentcore-control", region_name=a.region)
    r, ok = current(acc, a.runtime_id)
    out = {"runtime_id": a.runtime_id, "requireMMDSV2_before": ok, "enforced": False}
    if not ok and a.enforce:
        out["update_status"] = enforce(acc, a.runtime_id, r)
        r, ok = current(acc, a.runtime_id)
        out["enforced"] = True
    out["requireMMDSV2"] = ok
    out["metadataConfiguration"] = r.get("metadataConfiguration")
    print(json.dumps(out, indent=1, default=str))
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
