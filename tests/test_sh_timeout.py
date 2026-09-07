"""L28: the gate's sh() timeout must be enforceable, not decorative.

Attempt 14 of the full-portfolio gate hung for 2h20m against a 30-minute
`--deploy-timeout`. The timeout fired on schedule; it simply could not take
effect. `subprocess.run(capture_output=True, shell=True)` kills only its DIRECT
child on timeout and then re-enters communicate() to drain the pipes, and the
orphaned grandchildren still held the pipe write handles, so the drain never
reached EOF. The live process tree at the time:

    python 19192 -> cmd.exe 18340   (GONE - killed at the timeout)
                    node/npx 33888  (ALIVE, orphaned) -> cmd 42832 -> cdk 9396 (ALIVE)

These tests pin both halves of the fix: output through files rather than pipes,
and a whole-tree kill. They are written against the shape that actually hung -
a command whose grandchild outlives it holding the inherited handles.
"""
import os
import subprocess
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import full_portfolio_gate as g  # noqa: E402

_WIN = os.name == "nt"
# a parent that exits/blocks while a detached child keeps the inherited stdout handle open
_ORPHAN_CMD = (["cmd", "/c", "start /b ping -n 300 127.0.0.1 > nul & ping -n 300 127.0.0.1"]
               if _WIN else ["sh", "-c", "sleep 300 & sleep 300"])


def test_sh_still_captures_normal_output():
    r = g.sh(["cmd", "/c", "echo hello-from-sh"] if _WIN else ["echo", "hello-from-sh"], timeout=60)
    assert r["rc"] == 0
    assert "hello-from-sh" in r["out"]


def test_sh_timeout_raises_promptly_when_a_grandchild_holds_the_handles():
    """Under the old pipe-based sh() this blocks forever; it must now raise near the bound."""
    t0 = time.time()
    with pytest.raises(subprocess.TimeoutExpired):
        g.sh(_ORPHAN_CMD, timeout=5)
    elapsed = time.time() - t0
    assert elapsed < 45, "sh() did not return promptly after its timeout: %.1fs" % elapsed


def test_sh_timeout_kills_the_whole_process_tree():
    with pytest.raises(subprocess.TimeoutExpired):
        g.sh(_ORPHAN_CMD, timeout=5)
    time.sleep(2)
    if _WIN:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq PING.EXE"],
                             capture_output=True, text=True).stdout.upper()
        survivors = [l for l in out.splitlines() if "PING.EXE" in l]
    else:
        out = subprocess.run(["pgrep", "-f", "sleep 300"], capture_output=True, text=True).stdout
        survivors = [l for l in out.splitlines() if l.strip()]
    assert not survivors, "process tree survived the timeout kill: %r" % survivors
