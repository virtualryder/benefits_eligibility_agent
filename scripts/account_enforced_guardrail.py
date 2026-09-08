#!/usr/bin/env python3
"""Account-level enforced guardrail: report, apply, remove.

WHY THIS EXISTS (#234, and a correction to a standing claim)
------------------------------------------------------------
The register has said since 2026-09-05 that account-wide enforcement is "detective only until an
Organization exists" (PERIM-1b / R4-1). For SCPs that is still true - an SCP needs an Organization,
and this is a standalone account. For GUARDRAILS it is not, and the claim was too strong.

AWS documents an account-level enforced guardrail that needs no Organization:

  "The account-enforced guardrail should automatically apply to both inputs and outputs" - it
  applies to model invocations that do NOT specify a guardrail, and it cannot be bypassed by
  omitting one. Set with "the PutEnforcedGuardrailConfiguration API in every region where you want
  to enforce the guardrail". DeleteGuardrail is blocked for a guardrail bound to an enforcement
  configuration. Where account- and organization-level enforcements both apply, "the net effect is
  a union of all guardrails, with the most restrictive control taking precedence".
  https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-enforcements.html
  https://docs.aws.amazon.com/cli/latest/reference/bedrock/put-enforced-guardrail-configuration.html

WHAT IT DOES AND DOES NOT CLOSE
-------------------------------
It does NOT stop a principal from calling Bedrock - that is the SCP's job and still needs an
Organization. What it closes is the other half: any call that DOES happen is guardrailed, including
one from a bypass caller who never went through the gateway. The #168 capture trail already DETECTS
those calls; this makes them SAFE as well as visible.

Read the two halves separately, and do not let this be quoted as "account-wide non-bypassable
governance". It is non-bypassable GUARDRAILING, which is one control, not the perimeter.

CAVEATS THE DOCS STATE, WORTH REPEATING BEFORE YOU APPLY IT
-----------------------------------------------------------
  * PER REGION. It must be set in every region you care about; setting us-east-1 protects only
    us-east-1.
  * ACCOUNT-WIDE BLAST RADIUS. It applies to EVERY Bedrock model invocation in the account, not
    only this deployment's. On a shared account that affects other people's work.
  * Automated reasoning policies are unsupported in an enforcement configuration and "will cause
    runtime failures".
  * A numeric guardrail VERSION is required; DRAFT is not an enforcement target.

So `--apply` refuses without an explicit typed confirmation. Reporting is the default.

    python scripts/account_enforced_guardrail.py --region us-east-1
    python scripts/account_enforced_guardrail.py --apply --guardrail-id <id> --guardrail-version 1 \
        --region us-east-1 --i-understand-this-affects-every-bedrock-call-in-the-account
"""
import argparse
import json
import sys

CONFIRM = "--i-understand-this-affects-every-bedrock-call-in-the-account"


def _client(region):
    import boto3
    return boto3.client("bedrock", region_name=region)


def report(region):
    """Read-only. Returns the enforcement configurations set in this region."""
    c = _client(region)
    # NOTE the operation name: `list_enforced_guardrails_configuration` - guardrailS plural,
    # configuration singular. Both obvious spellings (list_enforced_guardrail_configurations,
    # get_enforced_guardrail_configuration) do not exist; guessing costs two round trips.
    resp = c.list_enforced_guardrails_configuration()
    cfgs = resp.get("guardrailsConfig") or []
    return {"region": region, "enforced_guardrails": cfgs, "count": len(cfgs)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--guardrail-id")
    ap.add_argument("--guardrail-version")
    ap.add_argument("--config-id")
    ap.add_argument(CONFIRM, dest="confirmed", action="store_true",
                    help="required for --apply and --remove")
    a = ap.parse_args(argv)

    if a.apply and a.remove:
        print("::error::--apply and --remove are mutually exclusive")
        return 2

    if not (a.apply or a.remove):
        print(json.dumps(report(a.region), indent=2, default=str))
        return 0

    if not a.confirmed:
        print("REFUSED: %s changes EVERY Bedrock model invocation in this AWS account, not just "
              "this deployment's. Re-run with %s if that is what you mean."
              % ("--apply" if a.apply else "--remove", CONFIRM))
        return 2

    c = _client(a.region)
    if a.apply:
        if not (a.guardrail_id and a.guardrail_version):
            print("::error::--apply needs --guardrail-id and a NUMERIC --guardrail-version "
                  "(DRAFT is not an enforcement target)")
            return 2
        if str(a.guardrail_version).upper() == "DRAFT":
            print("::error::guardrail version DRAFT cannot be enforced; publish a numeric version")
            return 2
        kwargs = {"guardrailInferenceConfig": {"guardrailIdentifier": a.guardrail_id,
                                               "guardrailVersion": str(a.guardrail_version)}}
        if a.config_id:
            kwargs["configId"] = a.config_id
        c.put_enforced_guardrail_configuration(**kwargs)
        print(json.dumps({"applied": True, **report(a.region)}, indent=2, default=str))
        print("REMEMBER: this is PER REGION. Repeat for every region you invoke Bedrock in.")
        return 0

    if not a.config_id:
        print("::error::--remove needs the --config-id shown by a plain report run")
        return 2
    c.delete_enforced_guardrail_configuration(configId=a.config_id)
    print(json.dumps({"removed": a.config_id, **report(a.region)}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
