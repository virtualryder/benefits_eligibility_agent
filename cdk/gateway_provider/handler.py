"""GA-1 — CloudFormation custom-resource provider for the AgentCore control plane.

Executes, as IaC, the exact sequence the proven shell engine performed:
  policy engine → gateway (MCP, CUSTOM_JWT, policy engine LOG_ONLY) → SSM discovery param
  → gateway targets (one per governed tool Lambda) → Cedar policies (gateway ARN injected into
  forbids) → update gateway to ENFORCE.
Delete reverses: policies → targets → gateway → engine → SSM. Update = idempotent re-create of
policies + re-assert ENFORCE. Fail-loud: any control-plane error fails the stack operation."""
import json
import time
import urllib.request
import urllib.parse

import boto3



def _require_https(url):
    """B310: refuse anything that is not https before opening it.

    Bandit's warning is real, not noise: these URLs come from configuration (SOR_URL, a JWKS
    endpoint, a CloudFormation ResponseURL). urlopen honours file:// and custom schemes, so a
    config value an attacker can influence turns a fetch into local-file disclosure. Validate the
    scheme and fail closed; the nosec on the urlopen below points at THIS check, it does not wave
    the finding away.
    """
    scheme = urllib.parse.urlsplit(url).scheme
    if scheme != "https":
        raise ValueError("refusing non-https URL scheme %r" % (scheme or "<none>"))
    return url

def _send(event, context, status, data=None, reason=""):
    body = json.dumps({
        "Status": status, "Reason": (reason or "ok")[:1000],
        "PhysicalResourceId": data.get("GatewayId", "agentcore-attachment") if data else "agentcore-attachment",
        "StackId": event["StackId"], "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"], "Data": data or {},
    }).encode()
    req = urllib.request.Request(event["ResponseURL"], data=body, method="PUT",
                                 headers={"Content-Type": ""})
    _require_https(event["ResponseURL"])
    urllib.request.urlopen(req, timeout=30)  # nosec B310 - scheme checked above


def _wait(fn, want, tries=40, delay=6, label="resource", failed=("FAILED", "CREATE_FAILED", "UPDATE_FAILED", "DELETE_FAILED")):
    """Poll fn() until it returns `want`. A terminal failure status raises IMMEDIATELY (no 4-minute wait
    on a resource that will never arrive), and every raise names the resource and its last status - the
    2026-09-05 live gate spent a full cycle on a bare "resource did not reach ACTIVE"."""
    last = None
    for _ in range(tries):
        last = fn()
        if last == want:
            return
        if last in failed:
            raise RuntimeError(f"{label} reached {last} (wanted {want})")
        time.sleep(delay)
    raise RuntimeError(f"{label} did not reach {want} (last status {last})")


def _policy_status(cc, engine_id, pid):
    d = cc.get_policy(policyEngineId=engine_id, policyId=pid)
    return d.get("status"), d.get("statusReasons") or []


def _error_code(exc):
    """botocore puts the modelled error name in response.Error.Code; anything else has none."""
    return getattr(exc, "response", {}).get("Error", {}).get("Code")


def _policy_ids_by_name(cc, engine_id, name):
    """Every policyId in this engine carrying this NAME. Name is what create_policy collides on."""
    try:
        return [p["policyId"] for p in cc.list_policies(policyEngineId=engine_id).get("policies", [])
                if p.get("name") == name]
    except Exception:
        return []


def _wait_policy_name_free(cc, engine_id, name, timeout=120):
    """Block until list_policies stops showing this NAME.

    ADVISORY ONLY. Live-observed 2026-09-08: a deleted policy disappears from list_policies while
    create_policy STILL refuses the name with ConflictException. So a True from this function means
    "the list view is clean", NOT "the name is free". The only authoritative answer comes from
    create_policy itself, which is why _create_policy_claiming_name retries THAT call rather than
    trusting this one. Kept because it is a cheap settle that removes most conflicts before they
    happen; never used as a precondition for declaring success.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not _policy_ids_by_name(cc, engine_id, name):
            return True
        time.sleep(3)
    return not _policy_ids_by_name(cc, engine_id, name)


def _create_policy_claiming_name(cc, engine_id, name, definition, mode,
                                 waits=(5, 10, 20, 30, 45, 60)):
    """create_policy, resolving a name still held by an earlier attempt or an earlier run.

    Two live failures on 2026-09-08, same stack, same message, different causes:

      1. The retry in _create_policy_active deleted a CREATE_FAILED policy and immediately
         re-created it under the same name. delete_policy returns before the name is released,
         so the re-create was refused. Fixed by deleting the holder explicitly.
      2. The fix for (1) trusted list_policies to say when the name was free. It is not
         authoritative: the policy had vanished from the list view and create_policy refused
         the name anyway. Same stack rolled back again, from the second create in this function.

    So the holder is deleted best-effort by name, and then the AUTHORITATIVE call - create_policy
    - is retried with backoff, because it is the only thing that actually knows. The waits are
    bounded: an unbounded loop inside a CloudFormation custom resource is a hung stack, not a
    resilient one. A name still contended after all of them raises with the elapsed budget named,
    so the stack event says how long we waited rather than just that we gave up.

    Only ConflictException means "the name is taken". Throttling, access-denied and everything
    else propagate untouched on the first attempt and on every retry.
    """
    body = {"policyEngineId": engine_id, "name": name,
            "definition": {"cedar": {"statement": definition}}, "validationMode": mode}

    try:
        return cc.create_policy(**body)["policyId"]
    except Exception as exc:
        if _error_code(exc) != "ConflictException":
            raise

    for pid in _policy_ids_by_name(cc, engine_id, name):
        try:
            cc.delete_policy(policyEngineId=engine_id, policyId=pid)
        except Exception:
            pass

    last = None
    for wait in waits:
        time.sleep(wait)
        try:
            return cc.create_policy(**body)["policyId"]
        except Exception as exc:
            if _error_code(exc) != "ConflictException":
                raise
            last = exc
    raise RuntimeError(
        "policy name %r is still refused as a duplicate after %ds of retries; the previous policy "
        "of this name has not been released (last error: %s)" % (name, sum(waits), last))


def _create_policy_active(cc, engine_id, name, definition, mode, attempts=3):
    """Create a Cedar policy and wait for ACTIVE. The engine validates tool ACTIONS against the gateway
    targets' tool schemas; right after the targets report READY the validator can still see an empty
    tool set ("unrecognized action ...") - a propagation race the 2026-09-05 live gate hit. A
    CREATE_FAILED whose reasons say "unrecognized action" is deleted and retried after a settle; any other
    validation failure raises at once WITH the engine's reasons (so the stack event says what was wrong).

    The retry was itself racy until 2026-09-08. delete_policy returns before the NAME is released, so
    attempt 2 called create_policy under the same name and got ConflictException("Policy with the same
    name already exists"). That is not a validation failure, nothing caught it, and it escaped this loop
    and failed the custom resource - rolling back ben-fp2-gateway and killing the full-portfolio re-gate
    of main. The one transient this retry exists to survive was the one case it could not survive. Both
    halves are handled now: the delete is waited out BY NAME, and a ConflictException on create is
    resolved by removing whatever holds the name before trying again."""
    last_reasons = []
    for attempt in range(attempts):
        pid = _create_policy_claiming_name(cc, engine_id, name, definition, mode)
        status, reasons = None, []
        for _ in range(40):
            status, reasons = _policy_status(cc, engine_id, pid)
            if status in ("ACTIVE", "CREATE_FAILED", "FAILED"):
                break
            time.sleep(4)
        if status == "ACTIVE":
            return pid
        last_reasons = reasons
        try:
            cc.delete_policy(policyEngineId=engine_id, policyId=pid)
        except Exception:
            pass
        # Wait for the NAME, not the id: the next attempt re-creates under the same name and the
        # name outlives the id. Skipping this is what produced the 2026-09-08 rollback.
        _wait_policy_name_free(cc, engine_id, name)
        transient = any("unrecognized action" in str(r) for r in reasons)
        if not transient or attempt == attempts - 1:
            break
        time.sleep(20 * (attempt + 1))
    raise RuntimeError("policy %s did not reach ACTIVE: %s" % (name, "; ".join(str(r)[:400] for r in last_reasons) or "no reasons"))


def _find_engine(cc, name):
    """An existing engine with our name that is (or is becoming) usable. An engine still DELETING
    (the Update path deletes then re-creates) is NOT reusable - found live 2026-09-02: reusing one
    raced its deletion and the re-create failed with GetPolicyEngine ResourceNotFound, leaving the
    stack without a gateway."""
    try:
        for e in cc.list_policy_engines().get("policyEngines", []):
            if e.get("name") == name and e.get("status") in (None, "ACTIVE", "CREATING"):
                return e["policyEngineId"]
    except Exception:
        pass
    return None


def _find_gateway(cc, name):
    try:
        for g in cc.list_gateways().get("items", []):
            if g.get("name") == name:
                return g["gatewayId"]
    except Exception:
        pass
    return None


def _remove_gateway(cc, gw_id):
    """Delete a gateway (targets first) and WAIT until it is gone - gateway names are unique per
    account, so a create right after a delete conflicts until the deletion has propagated."""
    for t in cc.list_gateway_targets(gatewayIdentifier=gw_id).get("items", []):
        try:
            cc.delete_gateway_target(gatewayIdentifier=gw_id, targetId=t["targetId"])
        except Exception:
            pass
    for _ in range(30):
        try:
            if not cc.list_gateway_targets(gatewayIdentifier=gw_id).get("items", []):
                break
        except Exception:
            break
        time.sleep(3)
    try:
        cc.delete_gateway(gatewayIdentifier=gw_id)
    except Exception:
        pass
    for _ in range(60):
        try:
            cc.get_gateway(gatewayIdentifier=gw_id)
        except Exception:
            return
        time.sleep(3)


def _interceptors(p):
    """Phase 107: attach the REQUEST interceptor when provided. passRequestHeaders=True is REQUIRED so
    the interceptor receives the validated JWT (AgentCore does not forward claims to Lambda targets)."""
    arn = p.get("InterceptorLambdaArn")
    if not arn:
        return {}
    return {"interceptorConfigurations": [{
        "interceptor": {"lambda": {"arn": arn}},
        "interceptionPoints": ["REQUEST"],
        "inputConfiguration": {"passRequestHeaders": True}}]}


def _create(cc, ssm, p, region, acct):
    # Live-run find: a failed CreateGateway can orphan the policy engine (created first). Reuse an
    # existing engine with our name instead of ConflictException-failing forever.
    engine_id = _find_engine(cc, p["EngineName"])
    if engine_id is None:
        engine_id = cc.create_policy_engine(name=p["EngineName"],
                                            description=p.get("EngineDesc", ""))["policyEngineId"]
    engine_arn = f"arn:aws:bedrock-agentcore:{region}:{acct}:policy-engine/{engine_id}"
    try:
        _wait(lambda: cc.get_policy_engine(policyEngineId=engine_id)["status"], "ACTIVE", label="policy engine")
    except cc.exceptions.ResourceNotFoundException:
        # the reused engine vanished under us (deletion still propagating): create a fresh one
        engine_id = cc.create_policy_engine(name=p["EngineName"],
                                            description=p.get("EngineDesc", ""))["policyEngineId"]
        engine_arn = f"arn:aws:bedrock-agentcore:{region}:{acct}:policy-engine/{engine_id}"
        _wait(lambda: cc.get_policy_engine(policyEngineId=engine_id)["status"], "ACTIVE")

    # A gateway with our name already present (a half-finished earlier Update, or a delete that has
    # not propagated - names are unique per account; found live 2026-09-02 as ConflictException):
    # remove it and wait, then create. The Update path is delete+create by design.
    stale = _find_gateway(cc, p["GatewayName"])
    if stale:
        _remove_gateway(cc, stale)

    authz = json.loads(p["AuthorizerConfigJson"])
    gw = cc.create_gateway(name=p["GatewayName"], roleArn=p["GatewayRoleArn"],
                           protocolType="MCP", authorizerType="CUSTOM_JWT",
                           authorizerConfiguration=authz,
                           policyEngineConfiguration={"arn": engine_arn, "mode": "LOG_ONLY"},
                           description=p.get("GatewayDesc", ""), **_interceptors(p))
    gw_id = gw["gatewayId"]
    _wait(lambda: cc.get_gateway(gatewayIdentifier=gw_id)["status"], "READY", label="gateway")
    g = cc.get_gateway(gatewayIdentifier=gw_id)
    gw_arn, gw_url = g["gatewayArn"], g["gatewayUrl"]
    ssm.put_parameter(Name=p["SsmParam"], Type="String", Overwrite=True, Value=gw_url)

    target_ids = []
    for t in json.loads(p["TargetsJson"]):
        target_ids.append(cc.create_gateway_target(
            gatewayIdentifier=gw_id, name=t["name"],
            targetConfiguration={"mcp": {"lambda": {
                "lambdaArn": t["lambda_arn"],
                "toolSchema": {"inlinePayload": t["tools"]}}}},
            credentialProviderConfigurations=[{"credentialProviderType": "GATEWAY_IAM_ROLE"}],
        )["targetId"])
    # EVERY target must be READY (not just the last one created) before the Cedar policies that name
    # their tools are validated against the gateway's tool set - then a short settle for propagation.
    for tid in target_ids:
        _wait(lambda tid=tid: cc.get_gateway_target(gatewayIdentifier=gw_id, targetId=tid)["status"], "READY",
              label="gateway target %s" % tid)
    if target_ids:
        time.sleep(15)

    for pol in json.loads(p["PoliciesJson"]):
        definition = pol["definition"].replace("__GATEWAY_ARN__", gw_arn)
        _create_policy_active(cc, engine_id, pol["name"], definition, pol.get("validation_mode", "FAIL_ON_ANY_FINDINGS"))

    cc.update_gateway(gatewayIdentifier=gw_id, name=p["GatewayName"], roleArn=p["GatewayRoleArn"],
                      protocolType="MCP", authorizerType="CUSTOM_JWT",
                      authorizerConfiguration=authz,
                      policyEngineConfiguration={"arn": engine_arn, "mode": "ENFORCE"}, **_interceptors(p))
    _wait(lambda: cc.get_gateway(gatewayIdentifier=gw_id)["status"], "READY")
    return {"GatewayId": gw_id, "GatewayArn": gw_arn, "GatewayUrl": gw_url,
            "PolicyEngineId": engine_id, "Enforcement": "ENFORCE"}


def _delete(cc, ssm, p, gw_id):
    # Live-run find: rollback of a FAILED create may target a gateway that was never created.
    # Delete must be tolerant of every absent resource (idempotent), never raise on not-found.
    try:
        eng = cc.get_gateway(gatewayIdentifier=gw_id)["policyEngineConfiguration"]["arn"].split("/")[-1]
    except Exception:
        # No gateway — but a failed create may have ORPHANED the engine; clean it by name.
        orphan = _find_engine(cc, p.get("EngineName", ""))
        if orphan:
            try:
                for pol in cc.list_policies(policyEngineId=orphan).get("policies", []):
                    cc.delete_policy(policyEngineId=orphan, policyId=pol["policyId"])
            except Exception:
                pass
            try:
                cc.delete_policy_engine(policyEngineId=orphan)
            except Exception:
                pass
        try:
            ssm.delete_parameter(Name=p.get("SsmParam", ""))
        except Exception:
            pass
        return   # nothing (else) was created
    if eng:
        for pol in cc.list_policies(policyEngineId=eng).get("policies", []):
            try:
                cc.delete_policy(policyEngineId=eng, policyId=pol["policyId"])
            except Exception:
                pass
    for t in cc.list_gateway_targets(gatewayIdentifier=gw_id).get("items", []):
        try:
            cc.delete_gateway_target(gatewayIdentifier=gw_id, targetId=t["targetId"])
        except Exception:
            pass
    time.sleep(10)
    try:
        cc.delete_gateway(gatewayIdentifier=gw_id)
    except Exception:
        pass
    if eng:
        time.sleep(10)
        try:
            cc.delete_policy_engine(policyEngineId=eng)
        except Exception:
            pass
    try:
        ssm.delete_parameter(Name=p["SsmParam"])
    except Exception:
        pass


def handler(event, context):
    p = event.get("ResourceProperties", {})
    region = context.invoked_function_arn.split(":")[3]
    acct = context.invoked_function_arn.split(":")[4]
    cc = boto3.client("bedrock-agentcore-control", region_name=region)
    ssm = boto3.client("ssm", region_name=region)
    try:
        if event["RequestType"] == "Create":
            data = _create(cc, ssm, p, region, acct)
        elif event["RequestType"] == "Delete":
            _delete(cc, ssm, p, event.get("PhysicalResourceId", ""))
            data = {}
        else:  # Update: tear down and re-create attachment (policies/targets may have changed)
            _delete(cc, ssm, p, event.get("PhysicalResourceId", ""))
            data = _create(cc, ssm, p, region, acct)
        _send(event, context, "SUCCESS", data)
    except Exception as exc:  # fail loud — never a silent partial attachment
        _send(event, context, "FAILED", {}, reason=f"{type(exc).__name__}: {exc}")
        raise
