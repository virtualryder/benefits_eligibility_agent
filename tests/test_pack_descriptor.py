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


# ---- PAR-4 stage 3: one harness, many packs ----------------------------------------------------
# Reading pack facts from pack.json was only half the fix. The gate still resolved everything from
# its own location, so gating a second pack still meant copying the file. These pin the other half.

def test_the_gate_can_be_pointed_at_another_repo(monkeypatch):
    gate = _load_gate()
    monkeypatch.setattr(sys, "argv", ["full_portfolio_gate.py", "--repo", os.sep + "somewhere"])
    assert gate._early_repo() == os.path.abspath(os.sep + "somewhere")
    monkeypatch.setattr(sys, "argv", ["full_portfolio_gate.py", "--repo=" + os.sep + "elsewhere"])
    assert gate._early_repo() == os.path.abspath(os.sep + "elsewhere")


def test_without_repo_the_gate_still_gates_its_own_pack(monkeypatch):
    gate = _load_gate()
    monkeypatch.setattr(sys, "argv", ["full_portfolio_gate.py", "--env", "fp"])
    assert gate._early_repo() == ROOT


def test_a_proof_script_resolves_pack_local_first_then_harness(tmp_path, monkeypatch):
    """A pack whose proof genuinely differs keeps its own; the harness copy is the fallback."""
    gate = _load_gate()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "gate_111.py").write_text("# the pack's own\n", encoding="utf-8")
    monkeypatch.setattr(gate, "REPO", str(tmp_path))
    assert gate.script("gate_111.py") == str(tmp_path / "scripts" / "gate_111.py")
    assert gate._SCRIPT_SOURCE["gate_111.py"] == "pack"
    # a script the pack does not have falls back to the harness, and is recorded as such
    assert gate.script("lineage_proof.py") == os.path.join(gate.HERE, "lineage_proof.py")
    assert gate._SCRIPT_SOURCE["lineage_proof.py"] == "harness"


# ---- the descriptor has to match the pack, not just parse --------------------------------------
# A descriptor that merely parses is worthless: the lineage proof compares CloudTrail Lambda invokes
# against aegis.call lines BY TOOL NAME, so a tool that is instrumented but not declared is simply
# never checked - and the gate still reports zero orphans. That is a silent hole, not a failure.

def _instrumented_tool_names(root):
    """Every @telemetry.instrument('<name>') in this pack's TRACKED source. The build output under
    cdk/.build is gitignored, so only tracked files are scanned; tools that come from the pinned
    governed-core wheel are outside the pack and are not asserted here."""
    import re
    import subprocess
    files = subprocess.run(["git", "ls-files", "*.py"], cwd=root, capture_output=True,
                           text=True, check=True).stdout.split()
    names = set()
    pat = re.compile(r"instrument\(\s*['\"]([a-z_]+)['\"]")
    for rel in files:
        try:
            src = io.open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        names.update(pat.findall(src))
    return names


def test_every_instrumented_tool_in_this_pack_is_declared():
    with io.open(os.path.join(ROOT, "pack.json"), encoding="utf-8") as fh:
        declared = set(json.load(fh)["lineage"]["tool_names"])
    found = _instrumented_tool_names(ROOT)
    assert found, "no @telemetry.instrument names found - the scan itself is broken"
    undeclared = found - declared
    assert not undeclared, (
        "these tools emit aegis.call lines but are not in pack.json tool_names, so the lineage "
        "proof would never check them: %s" % sorted(undeclared))


def test_every_alias_resolves_to_a_declared_tool():
    """L21d again: an alias whose target is not a declared tool silently never fires, and the tool
    it was meant to rescue is reported as an orphan on every run."""
    with io.open(os.path.join(ROOT, "pack.json"), encoding="utf-8") as fh:
        lin = json.load(fh)["lineage"]
    declared = set(lin["tool_names"])
    for stem, tool in lin.get("tool_aliases", {}).items():
        if stem.startswith("//"):
            continue
        assert tool in declared, "alias %r -> %r, which is not a declared tool" % (stem, tool)


def test_the_declared_tenants_are_the_ones_this_pack_s_proofs_use():
    """L35, live-found while preparing REL-5. Tenant ids are not in the CDK - they arrive as
    `-c tenants=`, which is right. The place a mismatch bites is the proof scripts: five of them
    defaulted `--tenants` to pha-a,pha-b, the ids benefits used in the mt..mt6 era, while the pack
    has declared sp-a,sp-b since the fp era. The usage lines in the two packs' docstrings were also
    cross-copied - benefits' said pha-a,pha-b and PV's said sp-a,sp-b, each naming the other pack.
    Masked only because the orchestrator always passes --tenants explicitly, so running any proof
    by hand would have gated tenants that do not exist and still reported PASS."""
    with io.open(os.path.join(ROOT, "pack.json"), encoding="utf-8") as fh:
        declared = set(json.load(fh)["tenants"])
    import re
    found = set()
    sdir = os.path.join(ROOT, "scripts")
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith(".py") or fn == "full_portfolio_gate.py":
            continue   # the gate names both packs' ids in the L35 comment, which is the point of it
        src = io.open(os.path.join(sdir, fn), encoding="utf-8", errors="replace").read()
        found.update(re.findall(r"\b((?:sp|pha)-[ab])\b", src))
    assert found, "no tenant ids found under scripts/ - the scan itself is broken"
    assert found <= declared, (
        "these proof scripts name tenants this pack does not declare, so running one without an "
        "explicit --tenants would gate the wrong tenants and still report PASS: %s"
        % sorted(found - declared))
