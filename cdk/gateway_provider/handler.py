"""GA-1 — CloudFormation custom-resource provider for the AgentCore control plane.

Executes, as IaC, the exact sequence the proven shell engine performed:
  policy engine → gateway (MCP, CUSTOM_JWT, policy engine LOG_ONLY) → SSM discovery param
  → gateway targets (one per governed tool Lambda) → Cedar policies (gateway ARN injected into
  forbids) → update gateway to ENFORCE.
Delete reverses: policies → targets → gateway → engine → SSM. Update = idempotent re-create of
policies + re-assert ENFORCE. Fail-loud: any control-plane error fails the stack operation."""
import json
import re
import time
import uuid
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


def _collides(cc, engine_id, wanted):
    """Names in `wanted` that this engine already holds. Empty for a freshly created engine."""
    try:
        have = {q.get("name") for q in cc.list_policies(policyEngineId=engine_id).get("policies", [])}
    except Exception:
        return []
    return sorted(have & set(wanted))


def _log(msg, *args):
    """Progress line into the provider's CloudWatch stream.

    This resource logged NOTHING but its final traceback until 2026-09-08. Four failed live
    deploys were spent working out which policy was failing and why, because the only signal was
    "ConflictException" with no name attached and a stack event that said the custom resource
    failed. A deploy that can only be diagnosed by running it again is not diagnosable; every step
    that talks to AgentCore says what it is about to do, and names the resource, BEFORE it does it.
    """
    print("[agentcore-attach] " + (msg % args if args else msg), flush=True)


_ACTION_RE = re.compile(r'AgentCore::Action::"([^"]+)"')


def _actions_in(definition):
    """Tool actions a Cedar policy names. A policy naming none is not validated against the tool set."""
    return _ACTION_RE.findall(definition)


def _wait_tool_actions_visible(cc, engine_id, gw_arn, action, timeout=600):
    """Block until the policy engine's validator can actually SEE the gateway's tool set.

    Every target reporting READY plus a fixed settle is NOT enough. Live 2026-09-08: four
    action-free policies went ACTIVE and the fifth - the first one naming a specific tool action -
    was rejected with "unrecognized action". The tool schema reaches the validator some time after
    the targets are READY, and nothing in the target status says when.

    The probe is a DISPOSABLE policy with a UNIQUE name, and that is the whole point. AgentCore
    reserves a deleted policy's name long after the policy is gone - measured that day at over
    170 seconds, while list_policies already showed the engine as empty - so anything that might
    need to be created twice must never reuse a name we still want. The probe burns a fresh name
    per attempt; the real policies are then created exactly once, under the names they must have.

    Returns True when the tool set is visible (or when the probe fails for some OTHER reason, which
    is not this function's to diagnose - the real policy will report it with its own reasons), and
    False if the tool set never became visible within the budget.
    """
    deadline = time.time() + timeout
    definition = ('forbid(principal, action == AgentCore::Action::"%s", '
                  'resource == AgentCore::Gateway::"%s");' % (action, gw_arn))
    attempt = 0
    _log("probing tool-set visibility with action %r (budget %ds)", action, timeout)
    while True:
        attempt += 1
        name = "aegis_toolset_probe_%d_%s" % (attempt, uuid.uuid4().hex[:8])
        try:
            pid = cc.create_policy(policyEngineId=engine_id, name=name,
                                   definition={"cedar": {"statement": definition}},
                                   validationMode="FAIL_ON_ANY_FINDINGS")["policyId"]
        except Exception:
            if time.time() > deadline:
                return False
            time.sleep(10)
            continue

        status, reasons = None, []
        for _ in range(30):
            status, reasons = _policy_status(cc, engine_id, pid)
            if status in ("ACTIVE", "CREATE_FAILED", "FAILED"):
                break
            time.sleep(4)
        try:
            cc.delete_policy(policyEngineId=engine_id, policyId=pid)
        except Exception:
            pass

        if status == "ACTIVE":
            _log("tool set visible after %d probe(s)", attempt)
            return True
        if not any("unrecognized action" in str(r) for r in reasons):
            _log("probe %d failed for a reason that is not the propagation race (%s); "
                 "letting the real policy report it", attempt, "; ".join(str(r)[:120] for r in reasons))
            return True
        _log("probe %d: tool set still not visible (%s)", attempt,
             "; ".join(str(r)[:120] for r in reasons))
        if time.time() > deadline:
            return False
        time.sleep(15)


def _create_policy_active(cc, engine_id, name, definition, mode):
    """Create a Cedar policy and wait for ACTIVE. Creates ONCE, deliberately.

    This used to delete a CREATE_FAILED policy and retry under the same name, to ride out the
    "unrecognized action" propagation transient. That cannot work: AgentCore reserves the deleted
    name for longer than a deploy can wait, so the retry was refused with ConflictException and
    rolled the stack back - twice on 2026-09-08, the second time through a fix that asked
    list_policies whether the name was free (it is not authoritative; the name was invisible there
    and still refused).

    The race is now waited out BEFORE any real policy is created, by _wait_tool_actions_visible,
    using disposable uniquely-named probes. So a validation failure here is a real one and is
    raised with the engine's reasons, which is what the stack event should have said all along.
    """
    _log("creating policy %r (mode=%s, actions=%s)", name, mode, _actions_in(definition) or "none")
    pid = cc.create_policy(policyEngineId=engine_id, name=name,
                           definition={"cedar": {"statement": definition}},
                           validationMode=mode)["policyId"]
    status, reasons = None, []
    for _ in range(40):
        status, reasons = _policy_status(cc, engine_id, pid)
        if status in ("ACTIVE", "CREATE_FAILED", "FAILED"):
            break
        time.sleep(4)
    if status == "ACTIVE":
        _log("policy %r ACTIVE", name)
        return pid
    raise RuntimeError("policy %s did not reach ACTIVE (status=%s): %s"
                       % (name, status, "; ".join(str(r)[:400] for r in reasons) or "no reasons"))


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
        _log("created policy engine %r -> %s", p["EngineName"], engine_id)
    else:
        # An ADOPTED engine can already hold policies under the names we are about to create. That
        # is a collision this resource cannot resolve (a deleted policy name is not reusable), so
        # say so loudly here rather than failing anonymously eleven policies later.
        existing = [q.get("name") for q in cc.list_policies(policyEngineId=engine_id).get("policies", [])]
        _log("ADOPTED existing policy engine %r -> %s, holding %d policy/policies: %s",
             p["EngineName"], engine_id, len(existing), existing or "none")
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
    _log("gateway %s READY with %d target(s)", gw_id, len(target_ids))
    if target_ids:
        time.sleep(15)

    policies = json.loads(p["PoliciesJson"])
    _log("%d policies to create: %s", len(policies), [q["name"] for q in policies])

    # An adopted engine may already hold a policy under a name we must create. A policy name, once
    # used, is not reusable - deleting the policy does not release it in any timeframe a deploy can
    # wait out (measured 2026-09-08: still refused after 170s, with list_policies already reporting
    # the engine empty). So this is unrecoverable HERE, and the only honest thing is to say so
    # before creating anything, naming the engine an operator has to remove. Failing at this point
    # also leaves the engine untouched, so the operator's cleanup is a single delete.
    taken = _collides(cc, engine_id, [q["name"] for q in policies])
    if taken:
        raise RuntimeError(
            "policy engine %s already holds %d of the %d policy names this deployment must create "
            "(%s). A policy name is not reusable once taken, so this cannot be resolved here. "
            "Delete the policy engine and redeploy." % (engine_id, len(taken), len(policies), taken))

    # Wait until the validator can SEE the tool set before creating any real policy. Targets READY
    # plus a settle is not that signal (live 2026-09-08). Probe with the first action any policy
    # actually names; policies naming none are not validated against the tool set and need no wait.
    probe_action = next((a for pol in policies for a in _actions_in(pol["definition"])), None)
    if probe_action and not _wait_tool_actions_visible(cc, engine_id, gw_arn, probe_action):
        raise RuntimeError(
            "gateway tool set never became visible to the policy validator: action %r still "
            "unrecognized after 600s with every target READY. Creating the real policies now would "
            "fail them under names that cannot be reused." % probe_action)

    for pol in policies:
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
