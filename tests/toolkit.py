"""Test helper: load a governed tool's Lambda handler module by name, from the agent's tools, this
agent's domain controls, or the pinned governance core — without any AWS calls."""
import importlib.util
import json
import pathlib

import governed_core

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENT_TOOLS = ROOT / "agents" / "benefits-eligibility" / "tools"
# The core controls come from the PINNED governed-core package, not from a copy in this repo.
# lib/controls now holds only this agent's domain-shaped modules, and it is searched FIRST so a
# declared domain override wins — the same precedence the Lambda bundler uses at deploy time.
CONTROLS = ROOT / "lib" / "controls"
CORE_CONTROLS = pathlib.Path(governed_core.controls_dir())


def make_sanitized_ref(text="[REDACTED:NAME] household of 3, monthly income 1800"):
    """Mint a GENUINE mask_pii-style sanitized_ref (P0-1) for tests, as the JSON string it crosses the
    gateway as. Requires PROVENANCE_SECRET in env (set by conftest before import)."""
    import sanitized
    return json.dumps(sanitized.mint_ref(text, engine="comprehend:DetectPiiEntities", entities_masked=1))


def load(name):
    for base in (AGENT_TOOLS, CONTROLS, CORE_CONTROLS):
        p = base / f"{name}.py"
        if p.exists():
            spec = importlib.util.spec_from_file_location(name, p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    raise FileNotFoundError(name)


def call(name, event):
    return load(name).handler(event, None)
