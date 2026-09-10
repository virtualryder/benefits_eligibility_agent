import base64
import json
import os
import urllib.request
import urllib.parse
import urllib.error
import boto3

# verify_source — a reusable GOVERNED connector tool that verifies a case against a REAL, OAuth2-protected
# external system of record (mock). It retires the "labeled stub" caveat: it is a real authenticated call.
# The outbound OAuth2 token is minted by **AgentCore Identity** — this tool holds NO client secret. Flow
# (client_credentials / 2-legged M2M):
#   1. get_workload_access_token(workloadName)         -> a workload identity token
#   2. get_resource_oauth2_token(..., oauth2Flow=M2M)  -> an OAuth2 access token from the Identity
#      credential provider (which holds the SoR's client_id/secret in the token vault)
#   3. call the system-of-record with Authorization: Bearer <token>
# Cedar-authorized at the Gateway like every other tool (deny-by-default). Fails soft (verified:false).

SOR_URL = os.environ.get("SOR_URL", "")
PROVIDER_NAME = os.environ.get("PROVIDER_NAME", "")
WI_NAME = os.environ.get("WI_NAME", "")
SCOPE = os.environ.get("SCOPE", "")
REGION = os.environ.get("AWS_REGION", "us-east-1")



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

def _coerce(e):
    e = e or {}
    if isinstance(e, str):
        try:
            e = json.loads(e)
        except Exception:
            e = {"case_id": e}
    return e


def _oauth_token():
    dp = boto3.client("bedrock-agentcore", region_name=REGION)
    wt = dp.get_workload_access_token(workloadName=WI_NAME)["workloadAccessToken"]
    r = dp.get_resource_oauth2_token(
        workloadIdentityToken=wt,
        resourceCredentialProviderName=PROVIDER_NAME,
        scopes=[SCOPE],
        oauth2Flow="M2M",
    )
    return r.get("accessToken")


def _claims_for_diagnosis(tok):
    """The token's NON-SECRET claims, so a rejection can be attributed to the right check.

    Deliberately never the token itself. A claim set cannot be replayed; a bearer token can, and
    this value travels through the gate log into committed evidence. These six fields are exactly
    what sor_api.py tests - kid/alg for the signature, iss/client_id/scope for the claims - so the
    rejection reason and the reason it was rejected land side by side in one output.
    """
    try:
        hdr_b64, payload_b64, _sig = tok.split(".")
        def _d(seg):
            return json.loads(base64.urlsafe_b64decode(seg + "=" * (-len(seg) % 4)))
        hdr, payload = _d(hdr_b64), _d(payload_b64)
        return {"kid": hdr.get("kid"), "alg": hdr.get("alg"), "iss": payload.get("iss"),
                "client_id": payload.get("client_id"), "scope": payload.get("scope"),
                "token_use": payload.get("token_use"), "exp": payload.get("exp")}
    except Exception:                                              # noqa: BLE001
        return {"parse": "the value returned by AgentCore Identity is not a readable JWT"}


def handler(event, context):
    e = _coerce(event)
    case_id = e.get("case_id") or "_default"
    if not SOR_URL:
        return {"verified": False, "error": "connector not configured (SOR_URL missing)"}

    try:
        token = _oauth_token()
    except Exception as ex:
        return {"verified": False, "error": "AgentCore Identity token fetch failed: %s" % type(ex).__name__,
                "detail": str(ex)[:200]}
    if not token:
        return {"verified": False, "error": "no OAuth token returned by the AgentCore Identity credential provider"}

    url = SOR_URL.rstrip("/") + "?" + urllib.parse.urlencode({"case_id": case_id})
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token,
                                               "User-Agent": "governed-connector/1.0"})
    try:
        _require_https(url)
        with urllib.request.urlopen(req, timeout=8) as resp:  # nosec B310 - scheme checked above
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        # READ THE BODY. sor_api.py answers every rejection with a JSON reason - "token signature
        # verification failed", "malformed token", "insufficient scope", "wrong issuer", "token
        # expired" - and this handler used to discard all of it and report only the status code.
        # On ben-fpc that left the entire diagnosis at "system-of-record returned HTTP 401", which
        # names a symptom with five possible causes and distinguishes none of them. Same defect
        # class as L70's 2>/dev/null and fpa's discarded stderr: an error path that cannot speak
        # turns a specific failure into an unattributable one, and costs a full live cycle to learn
        # what the response already said.
        try:
            said = ex.read().decode("utf-8", "replace")[:400]
        except Exception:                                          # noqa: BLE001
            said = "<no body>"
        # token_claims comes BEFORE sor_said on purpose. On ben-fpd the gateway truncated this
        # response mid-string and ate the claims, leaving the SoR's verdict ("signing key (kid) not
        # found in issuer JWKS") with nothing to attribute it to. The diagnosis has to survive the
        # transport, so the scarcest field goes first.
        return {"verified": False, "error": "system-of-record returned HTTP %s" % ex.code,
                "token_claims": _claims_for_diagnosis(token),
                "sor_said": said, "sor_auth_enforced": ex.code in (401, 403)}
    except (urllib.error.URLError, TimeoutError, ValueError) as ex:
        return {"verified": False, "error": "system-of-record call failed: %s" % type(ex).__name__,
                "detail": str(ex)[:200]}

    return {
        "verified": bool(data.get("verified")),
        "tool_holds_secret": False,
        "case_id": case_id,
        "connector": {
            "system_of_record": data.get("system_of_record"),
            "outbound_auth": "AgentCore Identity OAuth2 credential provider (%s), client_credentials/M2M" % PROVIDER_NAME,
            "token_minted_by_identity": True,
            "tool_holds_secret": False,
            "authorized_via": data.get("authorized_via"),
        },
        "note": "verified against an OAuth-protected system of record; the outbound OAuth token was minted by AgentCore Identity, not stored in this tool.",
    }
