#!/usr/bin/env python3
"""mint_token.py - mint a Cognito ACCESS token the way a REAL caller does: SRP against the SHIPPED
GatewayClient.

Why this replaced an `aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH` call.

ben-fp8 failed with "USER_PASSWORD_AUTH flow not enabled for this client", because the CDK client is
declared `auth_flows=cognito.AuthFlow(user_srp=True)` - SRP only, deliberately. The response was to
give the proof its own throwaway client with USER_PASSWORD_AUTH enabled, so as not to weaken the
shipped one. On ben-fpb that client minted tokens perfectly and the gateway refused every single one:

    FAIL | verify_source -> DENY insufficient_scope - The request requires higher privileges ...
    FAIL | outsider not denied -> DENY insufficient_scope - The request requires higher privileges ...

The REVIEWER and the OUTSIDER were denied identically, which is the tell: this was not Cedar
authorizing, it was the gateway refusing the token's issuer. gateway_stack.py says why, in one line:

    "AuthorizerConfigJson": json.dumps({"customJWTAuthorizer": {
        "discoveryUrl": discovery,
        "allowedClients": [identity.client.user_pool_client_id]}})

`allowedClients` is an allow-list of exactly ONE client - the shipped GatewayClient. A token from any
other client is rejected before Cedar is consulted. Making the throwaway client work would have meant
adding it to the gateway's own authorizer: weakening the PRODUCTION authorization boundary to let a
test identity in. That is far worse than the thing the throwaway client was invented to avoid.

So the proof authenticates the way every other live proof already did (cedar_perimeter_proof.py,
mt_two_tenant_proof.py): SRP, through the shipped client, exactly as a real caller does. Nothing is
weakened, no test-only client exists, and the token the proof carries is the same KIND of token a
caseworker carries. The proof users are still created by deploy_connector.sh and removed by
destroy_connector.sh - the CDK identity stack creates zero users by design.

Usage: mint_token.py <pool_id> <client_id> <region> <username> <password>
Prints the access token on stdout. On failure prints the reason on stderr and exits non-zero -
never both, and never a partial token, so a caller can test rc and trust stdout.
"""
import sys


def main():
    if len(sys.argv) != 6:
        sys.stderr.write("usage: mint_token.py <pool_id> <client_id> <region> <username> <password>\n")
        return 2
    pool, client, region, user, password = sys.argv[1:6]
    try:
        from pycognito import Cognito
    except Exception as exc:                      # noqa: BLE001 - the reason must reach the caller
        sys.stderr.write("pycognito is not importable in this interpreter: %r\n" % (exc,))
        return 3
    try:
        u = Cognito(pool, client, user_pool_region=region, username=user)
        u.authenticate(password=password)
    except Exception as exc:                      # noqa: BLE001
        # AWS's own words. The predecessor of this script discarded stderr, so ben-fpa's whole
        # diagnosis of a real failure was "could not mint a REV token via client 3mejbkk... | ".
        sys.stderr.write("%s: %s\n" % (type(exc).__name__, str(exc)[:400]))
        return 1
    token = getattr(u, "access_token", None)
    if not token:
        sys.stderr.write("authenticate() succeeded but returned no access_token\n")
        return 4
    sys.stdout.write(token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
