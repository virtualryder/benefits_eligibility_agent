"""The agent manifest must ship SIGNED (external review: no more `signature: null`) and the deploy must
be able to ENFORCE that signature. These tests prove the committed manifest verifies, that any content
edit or an unsigned slot fails CLOSED, and that the signature slot itself is excluded from the signed
bytes (so pointing the slot at the detached file does not invalidate the signature)."""
import base64
import copy
import json
import pathlib

import yaml

import verify_manifest as vm  # lib/controls is on sys.path via conftest

MANIFEST_PATH = pathlib.Path(__file__).resolve().parents[1] / "agents" / "benefits-eligibility" / "manifest.yaml"
SIG_PATH = MANIFEST_PATH.parent / "manifest.sig"


def _load():
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_committed_manifest_is_signed_and_verifies():
    ok, reason = vm.verify_file(str(MANIFEST_PATH))
    assert ok, reason


def test_sig_file_exists_and_digest_matches_manifest():
    assert SIG_PATH.exists(), "detached signature file is missing"
    sig = json.loads(SIG_PATH.read_text(encoding="utf-8"))
    assert sig["algorithm"] == "Ed25519"
    assert sig["digest_sha256"] == vm.digest_hex(_load())


def test_tamper_fails_closed():
    m = _load()
    m["agent"]["title"] = m["agent"]["title"] + " (edited)"
    ok, reason = vm.verify(m, str(MANIFEST_PATH))
    assert not ok
    assert "mismatch" in reason or "does not verify" in reason


def test_unsigned_slot_fails_closed():
    m = _load()
    m["signing"]["signature"] = None
    ok, reason = vm.verify(m, str(MANIFEST_PATH))
    assert not ok
    assert "UNSIGNED" in reason


def test_signature_slot_excluded_from_signed_bytes():
    """Changing the signature slot's VALUE must not change the canonical digest — it is what lets the
    signer point the slot at the detached file after signing without breaking verification."""
    m = _load()
    d0 = vm.digest_hex(m)
    m["signing"]["signature"] = "something-else.sig"
    assert vm.digest_hex(m) == d0
    # top-level slot is also stripped (backward-compat with a flat schema)
    m2 = _load()
    m2["signature"] = "x"
    assert vm.digest_hex(m2) == d0


def test_wrong_key_fails_closed():
    """A signature made by a DIFFERENT key over the same content must not verify."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    m = _load()
    other = Ed25519PrivateKey.generate()
    forged = other.sign(vm.canonical_bytes(m))
    sig = json.loads(SIG_PATH.read_text(encoding="utf-8"))
    inline = copy.deepcopy(sig)
    inline["signature_b64"] = base64.b64encode(forged).decode("ascii")  # forged sig, but ORIGINAL pubkey
    m["signing"]["signature"] = inline  # inline signature block path
    ok, reason = vm.verify(m, str(MANIFEST_PATH))
    assert not ok
    assert "does not verify" in reason
