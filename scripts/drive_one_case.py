#!/usr/bin/env python3
"""Drive ONE isolated governed workflow case (for the #168 lineage coverage proof).

Reuses mt_two_tenant_proof's helpers to: create a caseworker in tenant sp-a, token-verify an ingest
(which mints the signed tenant pair), start ONE determination-workflow execution, and poll to the
HumanSignoff pause. Runs in a quiet window so the account capture in [start_ms, end_ms] contains only
this execution's governed activity - clean invoke/audit parity for the lineage proof.
Prints a JSON result (case_id, execution_arn, window) to stdout and to .build/lineage-case.json.
"""
import json, time, uuid, secrets, sys, pathlib
import boto3

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mt_two_tenant_proof as mt

REGION, PREFIX, TENANT = "us-east-1", "ben-gate", "sp-a"
CASE = ("Applicant Jane Q Public, SSN 123-45-6789, DOB 1990-02-02, 742 Evergreen Terrace, "
        "phone 617-555-0142, email jane.public@example.com. Household of 3, monthly income 1800, "
        "liquid resources 400, no TANF. Source IP 10.1.2.3, card 4111 1111 1111 1111.")

cf = boto3.client("cloudformation", region_name=REGION)
idp = boto3.client("cognito-idp", region_name=REGION)
lam = boto3.client("lambda", region_name=REGION)
sfn = boto3.client("stepfunctions", region_name=REGION)

ident = mt.outputs(cf, f"{PREFIX}-identity")
pool, client = ident["UserPoolId"], ident["ClientId"]
ctrl = mt.outputs(cf, f"{PREFIX}-workflow")["ControllerArn"]

pw = "Ln-" + secrets.token_urlsafe(12) + "aA1!"
mt.make_user(idp, pool, "lineage-cw", ["benefits_caseworker", "tenant_" + TENANT], pw)
time.sleep(3)
tok = mt.access_token(pool, client, REGION, "lineage-cw", pw)

case_id = "LIN-" + uuid.uuid4().hex[:6].upper()
start_ms = int(time.time() * 1000)
ing = json.loads(lam.invoke(FunctionName=f"{PREFIX}-ingest-application",
                            Payload=json.dumps({"application": CASE, "case_id": case_id,
                                                "access_token": tok}).encode())["Payload"].read())
ex = sfn.start_execution(stateMachineArn=ctrl, name="lineage-" + case_id.lower(),
                         input=json.dumps({"case_id": case_id, "requester": "lineage-cw",
                                           "case_ref": ing.get("case_ref"),
                                           "redetermination": {"change_type": "NEW"},
                                           **ing.get("tenant_binding", {})}))["executionArn"]
status, states = "RUNNING", []
for _ in range(60):
    time.sleep(5)
    d = sfn.describe_execution(executionArn=ex)
    status = d["status"]
    states = [e.get("stateEnteredEventDetails", {}).get("name") for e in
              sfn.get_execution_history(executionArn=ex, maxResults=200)["events"]
              if e["type"] == "TaskStateEntered"]
    states = [s for s in states if s]
    if status != "RUNNING" or "HumanSignoff" in states:
        break
if status == "RUNNING":
    time.sleep(6)
    sfn.stop_execution(executionArn=ex, cause="lineage isolated case: signoff pause reached")
end_ms = int(time.time() * 1000)

result = {"case_id": case_id, "execution_arn": ex, "status": status, "states": states,
          "start_ms": start_ms, "end_ms": end_ms, "tenant": TENANT,
          "case_ref": ing.get("case_ref"), "minted_binding": bool(ing.get("tenant_binding"))}
pathlib.Path(__file__).resolve().parent.parent.joinpath(".build", "lineage-case.json").write_text(
    json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
