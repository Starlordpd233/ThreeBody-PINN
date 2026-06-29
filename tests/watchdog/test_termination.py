#!/usr/bin/env python3
"""Tests for the cross-session watchdog termination-guarantee layer (Phase 4).

Covers the **on-disk termination lifecycle layer**: <channel>/armed.json, the
<channel>/disarm sentinel, wd-disarm, and wd-status. This layer is the shared
substrate for BOTH the P1 background watcher (wd-arm) and the future P2 durable
cron (whose armer writes the same armed.json from agent-side). It does NOT
exercise the harness `CronCreate`/`CronList` (a plain python3 -m unittest
subprocess cannot invoke those — they are agent-side harness actions), and it
does NOT assert anything about a scheduled cron job. What it does assert is that
the bash-observable lifecycle — armed record write/remove, sentinel standdown,
status visibility, idempotent disarm — behaves exactly as both wake paths depend
on. Every test isolates shared state in a throwaway git repo, so the live
channel under the real repo's .git/live-monitor/channels/ is never touched.
"""
import os
import pathlib
import subprocess
import tempfile
import time
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
ARM = WD / "wd-arm"
DISARM = WD / "wd-disarm"
STATUS = WD / "wd-status"

# Git/agent vars that could leak the parent session's repo or identity into a
# temp-repo test are stripped from the inherited environment.
ISOLATED_KEYS = (
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "GIT_DIR",
    "GIT_WORK_TREE",
)


def run(args, cwd, env=None, timeout=30):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if env:
        merged.update(env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        env=merged,
        check=False,
        timeout=timeout,
    )


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def init_repo(path):
    # .resolve() collapses the macOS /var -> /private/var symlink so cwd-based
    # paths and git's realpath toplevel agree.
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    (path / "README.md").write_text("hello\n")
    git(path, "add", "README.md")
    git(path, "commit", "-q", "-m", "init")
    return path


class WatchdogTerminationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self._spawned = []
        self.addCleanup(self._reap_spawned)
        self.addCleanup(self.tmp.cleanup)

    # ----- helpers ---------------------------------------------------------
    def _reap_spawned(self):
        """Disarm + kill any watcher left running if a test failed mid-flight."""
        try:
            run(["bash", str(DISARM), "--all"], self.repo, timeout=10)
        except Exception:
            pass
        for proc in self._spawned:
            if proc.poll() is None:
                proc.kill()
            try:
                proc.communicate(timeout=5)
            except Exception:
                try:
                    proc.communicate()
                except Exception:
                    pass

    def channel_dir(self, channel):
        return self.repo / ".git" / "live-monitor" / "channels" / channel

    def spawn_arm(self, channel, poll="1", timeout="8", env=None):
        """Launch wd-arm as a non-blocking background process."""
        merged = os.environ.copy()
        for key in ISOLATED_KEYS:
            merged.pop(key, None)
        if env:
            merged.update(env)
        proc = subprocess.Popen(
            ["bash", str(ARM), "--channel", channel,
             "--poll-secs", poll, "--timeout-secs", timeout],
            cwd=str(self.repo),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=merged,
        )
        self._spawned.append(proc)
        return proc

    def disarm(self, *extra):
        return run(["bash", str(DISARM), *extra], self.repo)

    def status(self):
        return run(["bash", str(STATUS)], self.repo)

    def wait_for(self, fn, timeout_s=8.0, interval=0.2):
        """Poll fn() until it returns truthy or timeout_s elapses."""
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if fn():
                return True
            time.sleep(interval)
        return False

    # ----- 1. live arm is visible -----------------------------------------
    def test_live_arm_is_visible_to_status(self):
        proc = self.spawn_arm("live", poll="1", timeout="8")
        # Wait until the watcher has written its armed record.
        armed = self.channel_dir("live") / "armed.json"
        ok = self.wait_for(lambda: armed.is_file(), timeout_s=5)
        self.assertTrue(ok, "watcher did not write armed.json in time")
        st = self.status()
        self.assertEqual(st.returncode, 0, st.stderr)
        self.assertIn("live kind=watcher", st.stdout)
        # armed_by defaults to "unknown" when GIT_AGENT_ID is unset.
        self.assertIn("armed_by=unknown", st.stdout)
        # Clean up: let the watcher exit gracefully (communicate drains+closes pipes).
        self.disarm("--channel", "live")
        proc.communicate(timeout=5)

    # ----- 2. disarm removes it immediately -------------------------------
    def test_disarm_stands_down_running_watcher(self):
        proc = self.spawn_arm("disarm", poll="1", timeout="10")
        armed = self.channel_dir("disarm") / "armed.json"
        self.assertTrue(self.wait_for(lambda: armed.is_file(), timeout_s=5))
        # Disarm writes the sentinel, removes armed.json, and best-effort kills.
        d = self.disarm("--channel", "disarm")
        self.assertEqual(d.returncode, 0, d.stderr)
        self.assertIn("disarmed disarm", d.stdout)
        # The watcher exits 0 with DISARMED (via sentinel check or TERM trap).
        try:
            out, _ = proc.communicate(timeout=6)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
            self.fail("watcher did not exit after disarm")
        self.assertEqual(proc.returncode, 0, f"rc={proc.returncode} out={out!r}")
        self.assertIn("DISARMED", out)
        # After standdown: armed.json is gone, and wd-status reports no arm.
        self.assertFalse(armed.exists(), "armed.json not removed on standdown")
        st = self.status()
        self.assertEqual(st.returncode, 0, st.stderr)
        self.assertNotIn("disarm kind=watcher", st.stdout)

    # ----- 3. TTL self-termination removes the record ---------------------
    def test_ttl_self_termination_removes_record(self):
        # Synchronous run: blocks until the 2s timeout fires with no done marker.
        r = run(
            ["bash", str(ARM), "--channel", "ttl", "--poll-secs", "1", "--timeout-secs", "2"],
            self.repo,
            timeout=15,
        )
        self.assertEqual(r.returncode, 42, r.stderr)
        self.assertIn("PRODUCER-STALLED", r.stdout)
        # The watcher removed its armed record on the timeout exit path.
        self.assertFalse((self.channel_dir("ttl") / "armed.json").exists())
        # wd-status reflects the absence.
        st = self.status()
        self.assertEqual(st.returncode, 0, st.stderr)
        self.assertNotIn("ttl kind=watcher", st.stdout)

    # ----- 4. wd-disarm is idempotent / empty-safe ------------------------
    def test_disarm_empty_and_idempotent(self):
        # --all on a repo with no arms.
        empty = self.disarm("--all")
        self.assertEqual(empty.returncode, 0, empty.stderr)
        self.assertIn("no active arms", empty.stdout)
        # --channel X on a repo with no arms on X.
        empty_c = self.disarm("--channel", "X")
        self.assertEqual(empty_c.returncode, 0, empty_c.stderr)
        self.assertIn("no active arms", empty_c.stdout)
        # Arm, then disarm --channel X twice in a row: both must exit 0.
        proc = self.spawn_arm("idem", poll="1", timeout="10")
        self.assertTrue(self.wait_for(
            lambda: (self.channel_dir("idem") / "armed.json").is_file(), timeout_s=5))
        first = self.disarm("--channel", "idem")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("disarmed idem", first.stdout)
        # Wait for the watcher to finish its standdown (so the sentinel is gone).
        proc.communicate(timeout=6)
        second = self.disarm("--channel", "idem")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("no active arms", second.stdout)

    # ----- 5. armed_by captured from GIT_AGENT_ID -------------------------
    def test_armed_by_captured_from_env(self):
        # Spawn the watcher with GIT_AGENT_ID set; the record must capture it.
        proc = self.spawn_arm(
            "by", poll="1", timeout="10", env={"GIT_AGENT_ID": "test-b"}
        )
        armed = self.channel_dir("by") / "armed.json"
        self.assertTrue(self.wait_for(lambda: armed.is_file(), timeout_s=5))
        body = armed.read_text()
        self.assertIn('"armed_by":"test-b"', body)
        # wd-status surfaces the same value.
        st = self.status()
        self.assertEqual(st.returncode, 0, st.stderr)
        self.assertIn("by kind=watcher", st.stdout)
        self.assertIn("armed_by=test-b", st.stdout)
        self.disarm("--channel", "by")
        proc.communicate(timeout=5)


if __name__ == "__main__":
    unittest.main()
