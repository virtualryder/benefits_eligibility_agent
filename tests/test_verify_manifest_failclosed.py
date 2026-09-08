"""L43: the signature verifier's fail-closed path was the one path that did not fail closed.

verify_manifest.verify() documents "Fail-closed: any error -> (False, reason)". It did not. The
`cryptography` imports sat INSIDE the same try whose handler names InvalidSignature, so when the
library was absent the import raised, Python evaluated `except InvalidSignature:`, and that name -
a local assigned only by the import that had just failed - was unbound. The function raised
UnboundLocalError instead of returning (False, reason).

A verifier that raises where it promises to return False is a control whose failure mode depends on
what the caller happens to catch. Found by CI on 2026-09-08, which surfaced it only because CI never
installed cryptography - the dependency gap and the defect hid each other.

These tests pin the contract with the library genuinely unavailable, so the fix cannot regress if
someone moves the imports back.
"""
import builtins
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib"))
from controls import verify_manifest as vm  # noqa: E402

_SIGNED = {
    "agent": {"name": "x"},
    "signature": {
        "algorithm": "Ed25519",
        "signer": "test",
        "public_key_pem": "-----BEGIN PUBLIC KEY-----\nnot-a-real-key\n-----END PUBLIC KEY-----\n",
        "signature_b64": "AAAA",
    },
}


@pytest.fixture
def no_cryptography(monkeypatch):
    """Make `import cryptography...` raise, exactly as a CI runner without the wheel would."""
    real_import = builtins.__import__

    def _blocked(name, *a, **kw):
        if name.startswith("cryptography"):
            raise ModuleNotFoundError("No module named 'cryptography'")
        return real_import(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", _blocked)
    for mod in [m for m in list(sys.modules) if m.startswith("cryptography")]:
        monkeypatch.delitem(sys.modules, mod, raising=False)


def test_a_missing_signature_library_returns_false_not_an_exception(no_cryptography):
    """The defect: this raised UnboundLocalError instead of answering."""
    m = dict(_SIGNED)
    m["signature"] = dict(_SIGNED["signature"], digest_sha256=vm.digest_hex(_SIGNED))
    ok, reason = vm.verify(m, "manifest.yaml")
    assert ok is False
    assert "signature library unavailable" in reason, reason


def test_it_does_not_raise_unboundlocalerror(no_cryptography):
    """Name the exact failure so a regression is unmistakable in the report."""
    m = dict(_SIGNED)
    m["signature"] = dict(_SIGNED["signature"], digest_sha256=vm.digest_hex(_SIGNED))
    try:
        vm.verify(m, "manifest.yaml")
    except UnboundLocalError as exc:                      # pragma: no cover - the bug being pinned
        pytest.fail("fail-closed path raised instead of returning: %s" % exc)


def test_the_imports_are_not_inside_the_handler_s_own_try():
    """Structural guard: the handler must not name something the try block binds."""
    import inspect
    src = inspect.getsource(vm.verify)
    head, _, tail = src.partition("except InvalidSignature")
    assert "from cryptography.exceptions import InvalidSignature" not in head.split("try:")[-1], (
        "InvalidSignature is imported inside the try whose handler names it (L43)")
