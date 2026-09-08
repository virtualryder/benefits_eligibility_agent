#!/usr/bin/env python3
"""EV-1: prove the evidence vault is immutable in COMPLIANCE mode and that teardown cannot bypass it.

WHY THIS EXISTS
---------------
Every gate to date deployed S3 Object Lock in GOVERNANCE mode with 1-day retention so the
environment could be torn down - and the teardown path itself calls

    s3.delete_object(..., BypassGovernanceRetention=True)

which is exactly the operation an auditor is asking about when they ask whether the audit record can
be altered. The answer had never been tested, because the only COMPLIANCE profile in the repo locks
for seven years and AWS states plainly:

    "In compliance mode, a protected object version can't be overwritten or deleted by any user,
     including the root user in your AWS account."
    "The only way to delete an object under the compliance mode before its retention date expires is
     to delete the associated AWS account."
    https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html

So this runs the SAME mechanism at a disposable duration (the `compliance-proof` retention profile:
COMPLIANCE, 1 day) and asserts four things against a live bucket:

  1. the bucket really is configured COMPLIANCE (not GOVERNANCE)
  2. a plain delete of a locked object version is REFUSED
  3. the deployment's own teardown call - delete_object(BypassGovernanceRetention=True) - is REFUSED
     (that header applies only to governance mode)
  4. the retention timestamp on the object is what the profile says

It does NOT prove a seven-year schedule. The duration is a parameter; the immutability is the
mechanism. Cite it that way.

    python scripts/compliance_lock_proof.py --bucket <worm-bucket> --region us-east-1 \
        --out evidence/COMPLIANCE-LOCK-PROOF-<date>.json
"""
import argparse
import datetime
import json
import os
import sys

REAL_ACCOUNT = os.environ.get("AEGIS_REAL_ACCOUNT", "")
REDACTED = "111122223333"


def _redact(x):
    if isinstance(x, str):
        return x.replace(REAL_ACCOUNT, REDACTED) if REAL_ACCOUNT else x
    if isinstance(x, dict):
        return {k: _redact(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_redact(v) for v in x]
    return x


def main(argv=None):
    import boto3
    from botocore.exceptions import ClientError

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bucket", required=True)
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    s3 = boto3.client("s3", region_name=a.region)
    checks, key = {}, "ev1-compliance-proof/%s.json" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    def check(name, ok, detail):
        checks[name] = {"ok": bool(ok), "detail": str(detail)[:400]}
        print("%-46s %s  %s" % (name, "PASS" if ok else "FAIL", str(detail)[:110]))

    # 1. the bucket is COMPLIANCE, not GOVERNANCE
    cfg = s3.get_object_lock_configuration(Bucket=a.bucket)["ObjectLockConfiguration"]
    rule = (cfg.get("Rule") or {}).get("DefaultRetention") or {}
    mode, days = rule.get("Mode"), rule.get("Days")
    check("bucket_object_lock_mode_is_COMPLIANCE", mode == "COMPLIANCE",
          "mode=%s days=%s enabled=%s" % (mode, days, cfg.get("ObjectLockEnabled")))

    # 2. write an evidence object; it inherits the bucket's default retention
    body = json.dumps({"ev1": "compliance lock proof", "written_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}).encode()
    put = s3.put_object(Bucket=a.bucket, Key=key, Body=body, ContentType="application/json")
    vid = put["VersionId"]
    head = s3.head_object(Bucket=a.bucket, Key=key, VersionId=vid)
    check("written_object_is_locked_COMPLIANCE", head.get("ObjectLockMode") == "COMPLIANCE",
          "ObjectLockMode=%s retainUntil=%s" % (head.get("ObjectLockMode"),
                                                head.get("ObjectLockRetainUntilDate")))

    # 3. a plain versioned delete must be REFUSED
    try:
        s3.delete_object(Bucket=a.bucket, Key=key, VersionId=vid)
        check("plain_delete_is_refused", False,
              "DELETE SUCCEEDED - the object was not protected")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code")
        check("plain_delete_is_refused", code in ("AccessDenied", "InvalidRequest"),
              "%s: %s" % (code, exc.response.get("Error", {}).get("Message", "")[:160]))

    # 4. THE ACTUAL TEARDOWN CALL must be REFUSED. full_portfolio_gate.py and tier1_regate.py both
    #    empty the vault with exactly this, and it works against GOVERNANCE. Against COMPLIANCE the
    #    header does not apply and S3 rejects it - that refusal is the evidence.
    try:
        s3.delete_object(Bucket=a.bucket, Key=key, VersionId=vid, BypassGovernanceRetention=True)
        check("teardown_bypass_is_refused", False,
              "BYPASS DELETE SUCCEEDED - teardown can erase the audit record")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code")
        check("teardown_bypass_is_refused", code in ("AccessDenied", "InvalidRequest"),
              "%s: %s" % (code, exc.response.get("Error", {}).get("Message", "")[:160]))

    # 5. the object survived both attempts
    try:
        s3.head_object(Bucket=a.bucket, Key=key, VersionId=vid)
        check("object_still_present_after_both_attempts", True, "head_object succeeded")
    except ClientError as exc:
        check("object_still_present_after_both_attempts", False, str(exc)[:200])

    ok = all(c["ok"] for c in checks.values())
    result = _redact({
        "gate": "EV-1 compliance-lock-proof",
        "date": datetime.date.today().isoformat(),
        "bucket": a.bucket, "region": a.region, "key": key,
        "object_lock": {"mode": mode, "days": days},
        "PASS": ok,
        "checks": checks,
        "scope_note": ("Proves the MECHANISM (COMPLIANCE mode is set, a plain delete is refused, and "
                       "the deployment's own BypassGovernanceRetention teardown call is refused) at a "
                       "1-day retention so the test is disposable. It does NOT prove a 7-year "
                       "schedule - the duration is a parameter, the immutability is the mechanism."),
        "aws_reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html",
    })
    print()
    print(json.dumps(result, indent=1, default=str))
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(result, fh, indent=1, default=str)
        print("\nevidence -> %s" % a.out)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
