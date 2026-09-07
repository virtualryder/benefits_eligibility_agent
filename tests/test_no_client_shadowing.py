"""L38: a loop variable that rebound a live boto3 client, found by a live gate.

Gate attempt 19 deployed all nine stacks, configured and launched the runtime, passed five checks,
and then died with `AttributeError: 'str' object has no attribute 'client'` - twelve minutes and a
full from-zero deploy in. The cause was one line introduced when the gate was made pack-driven:

    s = boto3.Session(region_name=region)      # the session, used by ten later s.client(...) calls
    ...
    for s in PACK["stacks"]:                   # rebinds s to "observability"

Nothing offline caught it. The descriptor tests import the module and exercise load_pack and
script(), but never run main(), so a name-shadowing bug inside main() was invisible until it cost a
live cycle. This is the register's own recurring lesson - the last three lineage iterations each
cost ~90 minutes to learn what a unit test teaches in milliseconds - so the check is written as a
test rather than as care.

The rule: in any one scope, a name assigned a boto3 Session or client must not later be rebound by
a for-loop or comprehension target. It is a shape a linter can see without running anything.
"""
import ast
import io
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")


def _nested_function_nodes(fn):
    """Every node belonging to a function nested inside fn (i.e. NOT fn's own scope)."""
    skip = set()
    for n in ast.walk(fn):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n is not fn:
            skip.update(ast.walk(n))
    return skip


def shadowed_clients(src):
    """[(func, name, assigned_line, rebound_line)] for clients rebound by a loop in the same scope."""
    tree = ast.parse(src)
    out = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        skip = _nested_function_nodes(fn)
        nodes = [n for n in ast.walk(fn) if n not in skip]
        bound = {}
        for n in nodes:
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call):
                call = ast.unparse(n.value.func)
                if "boto3.Session" in call or "boto3.client" in call or call.endswith(".client"):
                    for t in n.targets:
                        if isinstance(t, ast.Name):
                            bound.setdefault(t.id, n.lineno)
        for n in nodes:
            for tgt in ([n.target] if isinstance(n, (ast.For, ast.comprehension)) else []):
                for sub in ast.walk(tgt):
                    if isinstance(sub, ast.Name) and sub.id in bound:
                        line = getattr(n, "lineno", getattr(tgt, "lineno", 0))
                        if line > bound[sub.id]:
                            out.append((fn.name, sub.id, bound[sub.id], line))
    return sorted(set(out))


def _scripts():
    return [os.path.join(SCRIPTS, f) for f in sorted(os.listdir(SCRIPTS)) if f.endswith(".py")]


@pytest.mark.parametrize("path", _scripts(), ids=lambda p: os.path.basename(p))
def test_no_loop_variable_shadows_a_boto3_client(path):
    src = io.open(path, encoding="utf-8", errors="replace").read()
    bad = shadowed_clients(src)
    assert not bad, "\n".join(
        "%s(): %r is a boto3 client assigned at line %d, rebound by a loop at line %d"
        % (fn, name, a, b) for fn, name, a, b in bad)


def test_the_detector_catches_the_exact_shape_that_cost_gate_19():
    """A guard that cannot fail is not a guard."""
    bad = shadowed_clients(
        "import boto3\n"
        "def main():\n"
        "    s = boto3.Session()\n"
        "    for s in ['a', 'b']:\n"
        "        pass\n"
        "    s.client('sts')\n")
    assert bad == [("main", "s", 3, 4)]


def test_the_detector_does_not_fire_across_separate_scopes():
    """`s` in one function has nothing to do with `s` in another - the naive version of this check
    reported seven false positives before it was made scope-aware."""
    assert shadowed_clients(
        "import boto3\n"
        "def a():\n"
        "    s = boto3.Session()\n"
        "    return s.client('sts')\n"
        "def b():\n"
        "    for s in [1, 2]:\n"
        "        print(s)\n") == []
