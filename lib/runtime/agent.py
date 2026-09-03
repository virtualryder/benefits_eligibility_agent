"""Generic governed intake agent — runs natively on Amazon Bedrock AgentCore Runtime.

Reusable across agents: the workflow prompt, model, and gateway discovery all come from the manifest
(passed in as env vars by the launch step). Identity: the human authenticates and their ACCESS token
is the bearer for every governed Gateway (MCP) tool call, so Cedar evaluates the real human principal.
The agent never commits the consequential action; it requests human sign-off (separation of duties).
"""
import os
import base64
import binascii
import json
import logging
import re
import time
import boto3
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s agent %(message)s")
log = logging.getLogger("agent")

app = BedrockAgentCoreApp()

MODEL_ID = os.environ.get("MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
REGION = os.environ.get("AWS_REGION", "us-east-1")
GATEWAY_URL_ENV = os.environ.get("GATEWAY_URL", "")
GATEWAY_SSM_PARAM = os.environ.get("GATEWAY_SSM_PARAM", "")
# Kill Switch (task 127): the deployment's containment flag(s), comma-separated SSM parameter names
# (the CDK's /<prefix>-eligibility/kill-switch, optionally + the platform-wide /aegis/kill-switch).
KILL_SWITCH_PARAMS = [p.strip() for p in os.environ.get("KILL_SWITCH_PARAMS", "").split(",") if p.strip()]
KILL_SWITCH_TTL = int(os.environ.get("KILL_SWITCH_TTL_SECONDS", "15") or 15)

# The governed workflow prompt is manifest-driven (passed via --env at launch). Fallback below keeps
# the agent safe/generic if it is missing.
SYSTEM = os.environ.get("SYSTEM_PROMPT") or (
    "You are an intake agent running under strict governance on Amazon Bedrock AgentCore. Your tools "
    "are exposed via a governed gateway; every call is authorized by policy against the human identity "
    "you act for. Use the available tools in a sensible order, never commit a consequential submission "
    "directly (that is owned by the human sign-off gate), and if any tool is denied by policy, STOP and "
    "report exactly which control blocked you. End with a short summary and the sign-off status."
)


class KillSwitchEngaged(Exception):
    """Containment is engaged: the session is refused / the in-flight agent loop is stopped."""


_ks_cache = {}   # param -> (fetched_at, record)


def _kill_switch(now=None):
    """The RUNTIME analog of governed-core kill_switch.state() (the runtime image carries only
    agent.py, so the rules are restated here and unit-tested in tests/test_runtime_kill_switch.py):
    read each configured parameter FIRST, 15 s TTL cache, FAIL-CLOSED on an unreadable / malformed
    value, engaged if ANY parameter is engaged. Returns the engaged record or None."""
    if not KILL_SWITCH_PARAMS:
        return None
    now = time.time() if now is None else now
    for name in KILL_SWITCH_PARAMS:
        hit = _ks_cache.get(name)
        if hit and now - hit[0] < KILL_SWITCH_TTL:
            rec = hit[1]
        else:
            try:
                raw = boto3.client("ssm", region_name=REGION).get_parameter(Name=name)["Parameter"]["Value"]
                rec = json.loads(raw)
                if not isinstance(rec, dict) or not isinstance(rec.get("engaged"), bool):
                    rec = {"engaged": True, "reason": "malformed kill-switch record (fail-closed)"}
            except Exception as exc:          # AccessDenied / not found / throttled / bad JSON => ENGAGED
                rec = {"engaged": True, "reason": "unreadable: %s" % type(exc).__name__}
            rec = dict(rec, source=name)
            _ks_cache[name] = (now, rec)
        if rec.get("engaged"):
            return rec
    return None


def _contained(exc):
    """True when this exception is (or wraps) KillSwitchEngaged, or the switch is engaged right now."""
    seen, e = set(), exc
    while e is not None and id(e) not in seen:
        if isinstance(e, KillSwitchEngaged):
            return True
        seen.add(id(e))
        e = e.__cause__ or e.__context__
    return _kill_switch() is not None


def _refusal(engaged, corr=None):
    line = {"aegis": "kill_switch", "component": "runtime", "outcome": "denied:kill_switch",
            "source": engaged.get("source"), "engaged_by": engaged.get("actor", ""),
            "engaged_reason": engaged.get("reason", ""), **(corr or {})}
    log.warning(json.dumps(line, sort_keys=True, default=str))
    return {"error": "containment engaged (kill switch %s): every agent action is refused" % engaged.get("source"),
            "refused": True, "reason": "kill_switch_engaged", "guardrail_action": "KILL_SWITCH",
            "engaged_by": engaged.get("actor", ""), "engaged_reason": engaged.get("reason", ""), "governed": True}


def _gateway_url():
    if GATEWAY_SSM_PARAM:
        try:
            p = boto3.client("ssm", region_name=REGION).get_parameter(Name=GATEWAY_SSM_PARAM)
            log.info("gateway_url source=SSM param=%s", GATEWAY_SSM_PARAM)
            return p["Parameter"]["Value"]
        except Exception as exc:
            log.warning("SSM gateway lookup failed (%s); falling back to GATEWAY_URL env", type(exc).__name__)
    return GATEWAY_URL_ENV


def _session_tenant(token):
    """Read custom:tenant from the human's VERIFIED access token to BIND this Runtime session to one
    tenant. AgentCore Runtime already isolates sessions (microVM per session); this makes the tenant
    explicit and lets the agent fail closed in multi-tenant mode. READ-ONLY: authorization stays at the
    gateway/Cedar Policy engine — this never makes an access decision. Mirrors
    lib/controls/tenancy.tenant_from_bearer (kept self-contained because the runtime image stages only
    agent.py)."""
    if not isinstance(token, str) or token.count(".") < 2:
        return None
    seg = token.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    try:
        claims = json.loads(base64.urlsafe_b64decode(seg).decode("utf-8"))
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return None
    t = claims.get("custom:tenant")
    if isinstance(t, str) and t.strip():
        return t.strip()
    # Cognito ACCESS tokens carry cognito:groups (not custom attributes): tenant membership is the
    # tenant_<id> group - the same rule as tenancy.tenant_from_claims (found while wiring phase 110:
    # this mirror only read custom:tenant and would have refused every group-tenanted identity).
    g = claims.get("cognito:groups")
    groups = g if isinstance(g, (list, tuple)) else (str(g).replace(",", " ").split() if g else [])
    for grp in groups:
        if isinstance(grp, str) and grp.startswith("tenant_") and grp[len("tenant_"):].strip():
            return grp[len("tenant_"):].strip()
    return None


_MULTITENANT = os.environ.get("MULTITENANT", "").strip().lower() in ("1", "true", "yes", "on")
_META_OK = re.compile(r"[^a-zA-Z0-9\s:_@$#=/+,\-.]")


def _meta_value(v):
    """Converse.requestMetadata values: ≤256 chars from [a-zA-Z0-9\s:_@$#=/+,-.] (API reference)."""
    return _META_OK.sub("_", str(v or ""))[:256]


def _correlation(context, session_tenant, case_id, requester):
    """Phase 110: the ONE correlation set every signal of this invocation carries. The runtime session
    id comes from AgentCore (X-Amzn-Bedrock-AgentCore-Runtime-Session-Id -> context.session_id) and is
    the mandatory `session.id` span attribute; tenant is the DERIVED session tenant."""
    sid = getattr(context, "session_id", None) or os.environ.get("AGENTCORE_SESSION_ID") or ""
    c = {"session.id": sid, "case_id": case_id, "requester": requester}
    if session_tenant:
        c["tenant"] = session_tenant
    return {k: v for k, v in c.items() if v}


def _attach_baggage(corr):
    """Propagate session.id + tenant as OTEL baggage so ADOT puts them on the outbound MCP call headers
    (the gateway interceptor reads them into __aegis_trace) and on every child span."""
    try:
        from opentelemetry import baggage, context as otel_ctx
        ctx = otel_ctx.get_current()
        for k in ("session.id", "tenant", "case_id"):
            if corr.get(k):
                ctx = baggage.set_baggage(k, corr[k], context=ctx)
        return otel_ctx.attach(ctx)
    except Exception as exc:               # observability must never change control flow
        log.warning("baggage not attached: %s", type(exc).__name__)
        return None


def _bedrock_session(corr):
    """A boto3 session whose bedrock-runtime Converse/ConverseStream calls carry `requestMetadata`
    (tenant, session_id, case_id, requester) - the model-invocation LOG rows become filterable per
    tenant/session without reading bodies (Bedrock model invocation logging: requestMetadata)."""
    session = boto3.Session(region_name=REGION)
    meta = {"tenant": corr.get("tenant", "silo"), "session_id": corr.get("session.id", ""),
            "case_id": corr.get("case_id", ""), "requester": corr.get("requester", ""),
            "governed_by": "aegis"}
    meta = {k: _meta_value(v) for k, v in meta.items() if v}

    def _inject(params, **_kw):
        # Kill switch (task 127): checked before EVERY model call, so an in-flight agent loop stops at
        # its next model call (<= TTL after engage) - not just at the next session.
        engaged = _kill_switch()
        if engaged:
            _refusal(engaged, corr)
            raise KillSwitchEngaged(engaged.get("reason", "engaged"))
        params.setdefault("requestMetadata", {}).update(meta)

    for op in ("Converse", "ConverseStream"):
        session.events.register("provide-client-params.bedrock-runtime.%s" % op, _inject)
    session.aegis_inject = _inject        # exposed for the unit test (tests/test_runtime_kill_switch.py)
    return session


@app.entrypoint
def invoke(payload, context=None):
    p = payload or {}
    token = p.get("access_token") or ""
    requester = p.get("requester", "reviewer")
    case_id = p.get("case_id") or p.get("icsr_id") or "CASE-0001"
    prompt = p.get("prompt") or (
        "Process the intake for case %s (requester %s). Run the governed workflow end to end and "
        "request human sign-off with the case id and requester." % (case_id, requester)
    )
    log.info("invocation requester=%s case_id=%s token_present=%s", requester, case_id, bool(token))
    if not token:
        return {"error": "no access_token provided; a human identity is required to drive governed tools"}
    # Kill switch (task 127): CONTAINMENT FIRST - before the tenant is derived, before the gateway is
    # contacted, before the first model call. Fail-closed on an unreadable switch.
    engaged = _kill_switch()
    if engaged:
        return _refusal(engaged, {"case_id": case_id, "requester": requester})

    session_tenant = _session_tenant(token)
    if _MULTITENANT and not session_tenant:
        log.warning("MULTITENANT: identity carries no custom:tenant claim; refusing (tenant is derived, never requested)")
        return {"error": "multi-tenant: your identity carries no tenant (custom:tenant); refusing",
                "governed": True}
    log.info("session_tenant=%s multitenant=%s", session_tenant, _MULTITENANT)
    corr = _correlation(context, session_tenant, case_id, requester)
    _attach_baggage(corr)
    log.info(json.dumps({"aegis": "invocation", **corr}, sort_keys=True))

    gw = _gateway_url()
    if not gw:
        return {"error": "gateway URL not available (SSM and env both empty)"}

    # region comes from the session (Strands refuses region_name + boto_session together - found live)
    model = BedrockModel(model_id=MODEL_ID, temperature=0.2, boto_session=_bedrock_session(corr))
    mcp_client = MCPClient(lambda: streamablehttp_client(gw, headers={"Authorization": "Bearer %s" % token}))
    with mcp_client:
        tools = mcp_client.list_tools_sync()
        names = [getattr(t, "tool_name", str(t)) for t in tools]
        log.info("authorized_tools requester=%s count=%d names=%s", requester, len(names), names)
        if not tools:
            log.warning("ACCESS DENIED requester=%s (no authorized tools)", requester)
            return {
                "result": "ACCESS DENIED - your identity is not authorized for any governed tool at the "
                          "gateway (Cedar deny-by-default). No workflow was run and nothing was drafted, "
                          "masked, audited, or submitted.",
                "tools_available": [], "governed": True, "tenant": session_tenant,
            }
        # trace_attributes land on EVERY Strands span of this invocation (invoke_agent, cycles, model
        # invoke, execute_tool): session.id (mandatory for AgentCore observability) + tenant + case.
        agent = Agent(model=model, tools=tools, system_prompt=SYSTEM, trace_attributes=corr)
        try:
            result = agent(prompt)
        except Exception as exc:              # engaged mid-session: stop, report, never retry
            # Strands wraps a hook exception in strands.types.exceptions.EventLoopException (seen live
            # 2026-09-03: "Invocation failed ... exception.type EventLoopException, message = our reason"),
            # so walk the cause chain and ALSO re-read the switch: either one proves containment.
            if _contained(exc):
                engaged = _kill_switch() or {"reason": str(exc), "source": ",".join(KILL_SWITCH_PARAMS)}
                return {**_refusal(engaged, corr), "tools_available": names, "tenant": session_tenant,
                        "stopped": "mid-session"}
            raise
    log.info("invocation_complete requester=%s case_id=%s result_chars=%d", requester, case_id, len(str(result)))
    return {"result": str(result), "tools_available": names, "tenant": session_tenant}


if __name__ == "__main__":
    app.run()
