"""verify_manifest — signed-manifest verification (external review: the manifest must not ship
`signature: null`, and the deploy must ENFORCE verification).

The manifest carries a `signing.signature` field that names a DETACHED signature file (JSON) sitting
beside it. That file holds the signer's PUBLIC key (PEM), the Ed25519 signature, and the canonical
digest. This module recomputes the canonical digest over the manifest (EXCLUDING the signature slot
itself) and verifies the signature against the EMBEDDED public key — so verification needs no AWS/KMS
and no network, and any edit to the manifest breaks verification until it is re-signed.

`signing.signature: null` (or a missing/invalid signature) verifies FALSE, so the production-profile
synth gate can refuse an unsigned manifest. In production the same detached-signature format is produced
by a KMS-asymmetric key (scripts/sign_manifest.py --kms-key ...), where the private key never leaves KMS;
the verify path here is identical (it only needs the public key).
"""
import base64
import copy
import hashlib
import json
import os


def _strip_sig_slots(body):
    """Remove every signature slot the schema might use (top-level `signature` and nested
    `signing.signature`) so the signed bytes are identical whether the slot holds null or a filename."""
    body.pop("signature", None)
    if isinstance(body.get("signing"), dict):
        body["signing"] = {k: v for k, v in body["signing"].items() if k != "signature"}
    return body


def canonical_bytes(manifest):
    """Canonical JSON of the manifest with the signature slot removed — the exact bytes that are signed.
    Stable (sorted keys, no insignificant whitespace) so signer and verifier agree."""
    body = _strip_sig_slots(copy.deepcopy(manifest or {}))
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_hex(manifest):
    return hashlib.sha256(canonical_bytes(manifest)).hexdigest()


def _sig_ref(manifest):
    """The signature reference, from nested `signing.signature` first, then top-level `signature`."""
    m = manifest or {}
    signing = m.get("signing")
    if isinstance(signing, dict) and "signature" in signing:
        return signing.get("signature")
    return m.get("signature")


def _load_sig(manifest, manifest_path):
    ref = _sig_ref(manifest)
    if not ref or (isinstance(ref, str) and ref.strip().lower() in ("null", "none", "")):
        return None, "manifest is UNSIGNED (signature: null)"
    if isinstance(ref, dict):                       # inline signature block
        return ref, None
    # a detached-signature filename beside the manifest
    sig_path = os.path.join(os.path.dirname(manifest_path or "."), str(ref))
    if not os.path.exists(sig_path):
        return None, "signature file not found: %s" % ref
    try:
        with open(sig_path, encoding="utf-8") as fh:
            return json.load(fh), None
    except Exception as exc:
        return None, "signature file unreadable: %s" % type(exc).__name__


def verify(manifest, manifest_path=None):
    """Return (ok: bool, reason: str). ok only if the manifest is signed AND the signature verifies AND
    the recorded digest matches the recomputed one. Fail-closed: any error -> (False, reason)."""
    sig, err = _load_sig(manifest, manifest_path)
    if err:
        return False, err
    algo = sig.get("algorithm", "")
    if algo != "Ed25519":
        return False, "unsupported signature algorithm: %r" % algo
    want_digest = digest_hex(manifest)
    if sig.get("digest_sha256") and sig["digest_sha256"] != want_digest:
        return False, "manifest digest mismatch (content changed since signing)"
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.exceptions import InvalidSignature
        pub = load_pem_public_key(sig["public_key_pem"].encode("utf-8"))
        signature = base64.b64decode(sig["signature_b64"])
        pub.verify(signature, canonical_bytes(manifest))     # Ed25519: raises on mismatch
        return True, "verified (Ed25519; signer=%s)" % sig.get("signer", "?")
    except InvalidSignature:
        return False, "signature does not verify against the manifest content"
    except Exception as exc:
        return False, "verification error: %s" % type(exc).__name__


def verify_file(manifest_path):
    """Convenience: load a YAML manifest from disk and verify it."""
    import yaml
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh) or {}
    return verify(manifest, manifest_path)
