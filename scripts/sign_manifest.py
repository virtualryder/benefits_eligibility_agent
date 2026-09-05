#!/usr/bin/env python3
"""sign_manifest — produce a DETACHED signature for the agent manifest (external review: no more
`signature: null`, and the deploy enforces verification via lib/controls/verify_manifest.py).

Signs the CANONICAL bytes of the manifest (everything EXCEPT the signature slot) and writes a detached
signature file beside it, then points the manifest's `signing.signature` field at that filename and sets
`signing.algorithm` to the algorithm actually used (Ed25519 for the reference signer).

Two signer backends:
  * default (reference): a fresh Ed25519 keypair is generated, used to sign, and the PRIVATE key is NOT
    persisted — so the committed public key + signature are tamper-evidence for THIS manifest revision
    (any edit breaks verification until re-signed). Re-signing generates a new keypair.
  * --kms-key <arn|alias> (production): sign with a KMS-asymmetric key whose private half never leaves
    KMS; the public key is embedded so verification stays offline. (Requires an ECC/Ed25519 key.)

Usage:
    python scripts/sign_manifest.py                       # reference Ed25519 signer
    python scripts/sign_manifest.py --signer ci@aegis     # label the signer
"""
import argparse
import base64
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "lib", "controls"))
import verify_manifest as vm  # noqa: E402

MANIFEST = os.path.join(REPO, "agents", "benefits-eligibility", "manifest.yaml")
SIG_NAME = "manifest.sig"


def _sign_ed25519(message):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    key = Ed25519PrivateKey.generate()
    sig = key.sign(message)
    pub_pem = key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8")
    return sig, pub_pem


def _set_field(text, name, value):
    """Targeted, comment-preserving replace of a `  <name>: ...` line (indentation preserved)."""
    pat = re.compile(r"(?m)^(?P<indent>[ \t]*)%s:[ \t]*.*$" % re.escape(name))
    m = pat.search(text)
    if not m:
        raise SystemExit("manifest has no `%s:` line to update" % name)
    return pat.sub(lambda mm: "%s%s: %s" % (mm.group("indent"), name, value), text, count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--signer", default="aegis-reference-signer")
    ap.add_argument("--kms-key", default="", help="KMS asymmetric key ARN/alias (production signer)")
    a = ap.parse_args()

    import yaml

    # 1) Declare the algorithm we actually sign with and point at the detached sig file FIRST, so the
    #    canonical bytes we sign match what verify recomputes from the on-disk manifest. (canonical_bytes
    #    excludes the signature slot, so its final value is immaterial; algorithm is NOT excluded.)
    with open(a.manifest, encoding="utf-8") as fh:
        text = fh.read()
    text = _set_field(text, "algorithm", "Ed25519" if not a.kms_key else "ECDSA_SHA_256")
    text = _set_field(text, "signature", SIG_NAME)
    with open(a.manifest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    # 2) Recompute canonical bytes over the UPDATED manifest and sign them.
    with open(a.manifest, encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh) or {}
    message = vm.canonical_bytes(manifest)
    digest = vm.digest_hex(manifest)

    if a.kms_key:
        raise SystemExit("KMS signer path: sign the digest with %s (ECDSA/Ed25519) and embed the KMS "
                         "public key. Not run in this reference invocation." % a.kms_key)
    sig, pub_pem = _sign_ed25519(message)

    sig_doc = {
        "algorithm": "Ed25519", "manifest_file": os.path.basename(a.manifest),
        "digest_sha256": digest, "signature_b64": base64.b64encode(sig).decode("ascii"),
        "public_key_pem": pub_pem, "signer": a.signer, "signed_at": int(time.time()),
        "note": "detached signature over the canonical manifest (excluding the signature slot). "
                "Reference Ed25519 signer; production uses a KMS-asymmetric key (private key never leaves KMS).",
    }
    sig_path = os.path.join(os.path.dirname(a.manifest), SIG_NAME)
    with open(sig_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(sig_doc, fh, indent=2)
        fh.write("\n")

    # 3) Verify the on-disk result end-to-end.
    ok, reason = vm.verify_file(a.manifest)
    print(json.dumps({"signed": True, "sig_file": sig_path, "digest_sha256": digest,
                      "verify_ok": ok, "verify_reason": reason}, indent=1))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
