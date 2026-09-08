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


def _probe_pids():
    """PIDs of the processes this test's command creates. Machine-global by image/pattern, so it
    is snapshotted BEFORE and AFTER and only the DIFFERENCE is judged."""
    if _WIN:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq PING.EXE", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True).stdout
        return {l.split('","')[1] for l in out.splitlines() if l.startswith('"')}
    out = subprocess.run(["pgrep", "-f", "sleep 300"], capture_output=True, text=True).stdout
    return {l.strip() for l in out.splitlines() if l.strip()}


def test_sh_timeout_kills_the_whole_process_tree():
    # This assertion used to read machine-global state - "is ANY ping.exe running?" - so a stray
    # probe left by an earlier run, or by anything else on the box, failed it. On 2026-09-08 it
    # did exactly that: two PING.EXE from this test's own previous invocation failed the next run,
    # which reads as a regression and is not one. Judge only the processes THIS call created.
    before = _probe_pids()
    with pytest.raises(subprocess.TimeoutExpired):
        g.sh(_ORPHAN_CMD, timeout=5)
    time.sleep(2)
    survivors = sorted(_probe_pids() - before)
    if survivors:  # never leave the box dirtier than we found it, whatever the verdict
        for pid in survivors:
            subprocess.run(["taskkill", "/F", "/PID", pid] if _WIN else ["kill", "-9", pid],
                           capture_output=True)
    assert not survivors, "process tree survived the timeout kill: %r" % survivors


# ---- L42: the timeout must not kill the process running it ---------------------------------------
# The three tests above pass on Windows and FAILED on Linux, which is where CI runs. sh() opened the
# child without start_new_session, so it inherited the CALLER's process group, and _kill_tree's
# killpg(getpgid(child)) therefore SIGKILLed the caller's group - the gate, or under pytest the test
# runner itself - while the grandchildren it was meant to reap survived. Reproduced on Linux before
# fixing: caller pgid 1603 == child pgid 1603, the process died mid-kill, two `sleep 300` survived.
# With the fix: child pgid 1672 != caller pgid 1670, caller exits normally, survivors none.

@pytest.mark.skipif(_WIN, reason="POSIX process groups; Windows reaps the tree with taskkill /T")
def test_the_child_gets_its_own_process_group():
    """The invariant the whole-tree kill depends on. Cheap, and it fails loudly if it regresses."""
    import signal
    p = subprocess.Popen(["sleep", "30"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL, start_new_session=True)
    try:
        assert os.getpgid(p.pid) != os.getpgid(0), (
            "the child shares the caller's process group, so killpg would kill the caller")
        assert os.getpgid(p.pid) == p.pid, "the child should lead its own group"
    finally:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except OSError:
            pass
        p.wait(timeout=10)


@pytest.mark.skipif(_WIN, reason="POSIX only")
def test_sh_opens_children_in_a_new_session_on_posix():
    """Pin it at the call site too - a future edit that drops the flag must fail here."""
    import inspect
    src = inspect.getsource(g.sh)
    assert "start_new_session" in src, "sh() must isolate the child's process group on POSIX (L42)"


@pytest.mark.skipif(_WIN, reason="POSIX only")
def test_kill_tree_refuses_to_kill_its_own_group(monkeypatch):
    """Belt and braces: if the child ever IS in our group, kill the child, never the group."""
    import signal
    killed = {}
    monkeypatch.setattr(g.os, "getpgid", lambda pid: 4242)          # child and caller in one group
    monkeypatch.setattr(g.os, "killpg", lambda *a: killed.setdefault("killpg", a))
    monkeypatch.setattr(g.os, "kill", lambda *a: killed.setdefault("kill", a))
    g._kill_tree(1234)
    assert "killpg" not in killed, "killed its own process group - that is the L42 defect"
    assert killed.get("kill") == (1234, signal.SIGKILL)
