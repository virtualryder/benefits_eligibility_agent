"""PAR-4: the gate is pack-driven, and a pack fact must never be inherited silently.

The portfolio gate used to hard-code the agent directory, tenants, deployment prefix, stack list,
runtime name and sign-off state, so a second pack could not be gated without copying the file — and
copying is how four versions of the log readers drifted three fixes apart. These tests pin the
contract that replaced it: everything pack-specific comes from pack.json, and the fields that DIFFER
between packs must be declared rather than defaulted.
"""
import importlib.util
import io
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "full_portfolio_gate.py")


def _load_gate():
    spec = importlib.util.spec_from_file_location("fpgate_under_test", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fpgate_under_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_this_pack_ships_a_descriptor_and_the_gate_reads_it():
    gate = _load_gate()
    assert gate.PACK["pack"]
    assert gate.PACK["agent_dir"]
    assert gate.PACK["prefix_prefix"]
    assert gate.TENANTS, "tenants must come from pack.json"
    assert os.path.isdir(gate.AGENT), "agent_dir must resolve: %s" % gate.AGENT


def test_the_descriptor_is_valid_json_with_the_fields_the_gate_needs():
    with io.open(os.path.join(ROOT, "pack.json"), encoding="utf-8") as fh:
        d = json.load(fh)
    for k in ("pack", "agent_dir", "prefix_prefix", "tenants"):
        assert d.get(k), "pack.json must declare %r" % k
    assert d["lineage"]["tool_names"], "the governed tool identity is a pack fact"
    assert d["workflow"]["signoff_state"]


def test_tenants_are_required_never_defaulted(tmp_path):
    """A silent tenant default would gate the WRONG tenants and still report PASS."""
    gate = _load_gate()
    (tmp_path / "pack.json").write_text(json.dumps({
        "pack": "x", "agent_dir": "agents/x", "prefix_prefix": "x"}), encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        gate.load_pack(str(tmp_path))
    assert "tenants" in str(e.value)


def test_a_missing_descriptor_fails_loudly(tmp_path):
    gate = _load_gate()
    with pytest.raises(SystemExit) as e:
        gate.load_pack(str(tmp_path))
    assert "pack.json" in str(e.value)


def test_the_gate_source_carries_no_pack_identity():
    """The harness must not name this pack; that is what forced a fork last time."""
    src = io.open(GATE, encoding="utf-8").read()
    body = "\n".join(l for l in src.split("\n")
                     if not l.strip().startswith("#") and '"""' not in l)
    for literal in ("benefits_runtime_agent", "agents/benefits-eligibility", '"ben-%s"'):
        assert literal not in body, "pack literal %r is still baked into the gate" % literal
