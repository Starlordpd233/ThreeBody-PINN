#!/usr/bin/env python3
"""Tests for deterministic watchdog channel resolution and mismatch warnings."""
import os
import pathlib
import re
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
COMMON = WD / "lib" / "wd-common.sh"
PUBLISH = WD / "wd-publish-done"
CHECK = WD / "wd-check"
ARM = WD / "wd-arm"
INTEGRATE = WD / "wd-integrate"
GSD = WD / "wd-gsd-publish"

ISOLATED_KEYS = (
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "GIT_DIR",
    "GIT_WORK_TREE",
)


def _clean_env(extra=None):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if extra:
        merged.update(extra)
    return merged


def run(args, cwd, env=None, timeout=60):
    return subprocess.run(
        [str(a) for a in args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        env=_clean_env(env),
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
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    (path / "README.md").write_text("hello\n")
    git(path, "add", "README.md")
    git(path, "commit", "-q", "-m", "init")
    return path


def jget(path, key):
    text = pathlib.Path(path).read_text()
    m = re.search(r'"%s":"([^"]*)"' % re.escape(key), text)
    return m.group(1) if m else None


class ChannelResolutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def channel_dir(self, channel):
        return self.repo / ".git" / "live-monitor" / "channels" / channel

    def stop_process(self, proc):
        if proc.poll() is None:
            proc.kill()
        try:
            proc.wait(timeout=5)
        except Exception:
            pass

    def publish(self, *extra, scope="README.md"):
        return run([PUBLISH, *extra, "--stage", "stage", "--scope", scope], self.repo)

    def test_key_slug_converges_across_publish_and_check(self):
        pub = self.publish("--key", "Phase 36: Execution!")
        self.assertEqual(pub.returncode, 0, pub.stderr)
        done = self.channel_dir("phase-36-execution") / "done.json"
        self.assertTrue(done.is_file(), "publish did not use the expected slug")

        chk = run([CHECK, "--key", "phase 36 execution"], self.repo)
        self.assertEqual(chk.returncode, 0, chk.stderr)
        self.assertEqual(chk.stdout.strip(), "WAKE")

    def test_phase_derivation_publish_arm_and_zero_pad(self):
        pub = self.publish("--phase", "036")
        self.assertEqual(pub.returncode, 0, pub.stderr)
        self.assertTrue((self.channel_dir("gsd-phase-36") / "done.json").is_file())
        self.assertFalse(self.channel_dir("gsd-phase-036").exists())

        arm = run([ARM, "--phase", "36", "--poll-secs", "1", "--timeout-secs", "5"], self.repo)
        self.assertEqual(arm.returncode, 0, arm.stderr)
        self.assertTrue(arm.stdout.startswith("WAKE "), arm.stdout)

    def test_wd_slug_normalization_table(self):
        cases = {
            "Phase 36: Execution!": "phase-36-execution",
            "---Hello!!!": "hello",
            "a///b": "a-b",
            "caf\u00e9": "caf",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                proc = run(
                    ["bash", "-c", f"source {COMMON}; wd_slug \"$1\"", "bash", raw],
                    self.repo,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(proc.stdout, expected)

        empty = run(
            ["bash", "-c", f"source {COMMON}; wd_slug \"$1\"", "bash", "\u4f60\u597d"],
            self.repo,
        )
        self.assertEqual(empty.returncode, 1)
        self.assertEqual(empty.stdout, "")

    def test_empty_key_rejected(self):
        pub = self.publish("--key", "\u2603")
        self.assertEqual(pub.returncode, 2, pub.stdout)
        self.assertIn("--key produced an empty channel slug", pub.stderr)

    def test_missing_and_mutually_exclusive_selectors_exit_2(self):
        tools = [
            (PUBLISH, ["--stage", "s", "--scope", "README.md"]),
            (ARM, ["--poll-secs", "1", "--timeout-secs", "1"]),
            (CHECK, []),
            (INTEGRATE, []),
        ]
        for tool, required in tools:
            with self.subTest(tool=tool.name, mode="missing"):
                proc = run([tool, *required], self.repo, timeout=10)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("exactly one of --channel, --phase, --key", proc.stderr)
            with self.subTest(tool=tool.name, mode="exclusive"):
                proc = run([tool, "--channel", "raw", "--phase", "36", *required], self.repo, timeout=10)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("exactly one of --channel, --phase, --key", proc.stderr)

    def test_gsd_publish_default_channel_derived_and_override_kept(self):
        derived = run([GSD, "--phase", "036", "--scope", "README.md"], self.repo)
        self.assertEqual(derived.returncode, 0, derived.stderr)
        done = self.channel_dir("gsd-phase-36") / "done.json"
        self.assertTrue(done.is_file(), "derived channel missing")
        self.assertEqual(jget(done, "stage"), "gsd:phase-36")
        self.assertFalse(self.channel_dir("default").exists(), "default channel should not be used")

        override = run([GSD, "--phase", "36", "--scope", "README.md", "--channel", "raw-demo"], self.repo)
        self.assertEqual(override.returncode, 0, override.stderr)
        self.assertTrue((self.channel_dir("raw-demo") / "done.json").is_file())

    def test_publish_warns_when_consumers_are_armed_elsewhere(self):
        wrong = self.channel_dir("phase-36-execution-backup")
        wrong.mkdir(parents=True)
        (wrong / "armed.json").write_text(
            '{"kind":"watcher","channel":"phase-36-execution-backup",'
            '"armed_at":0,"ttl":null,"armed_by":"agent-b","pid":1}\n'
        )
        pub = self.publish("--phase", "36")
        self.assertEqual(pub.returncode, 0, pub.stderr)
        self.assertIn("WARNING: no consumer is armed on channel 'gsd-phase-36'", pub.stderr)
        self.assertIn("'phase-36-execution-backup' (armed_by=agent-b)", pub.stderr)
        self.assertIn("re-arm on 'gsd-phase-36'", pub.stderr)

    def test_publish_warning_is_silent_without_mismatch(self):
        pub = self.publish("--phase", "36")
        self.assertEqual(pub.returncode, 0, pub.stderr)
        self.assertNotIn("WARNING:", pub.stderr)

        target = self.channel_dir("gsd-phase-37")
        target.mkdir(parents=True)
        (target / "armed.json").write_text(
            '{"kind":"watcher","channel":"gsd-phase-37","armed_at":0,'
            '"ttl":null,"armed_by":"agent-b","pid":1}\n'
        )
        target_pub = self.publish("--phase", "37")
        self.assertEqual(target_pub.returncode, 0, target_pub.stderr)
        self.assertNotIn("WARNING:", target_pub.stderr)

    def test_arm_warns_on_unclaimed_done_elsewhere_but_not_claimed_done(self):
        pub = self.publish("--channel", "other")
        self.assertEqual(pub.returncode, 0, pub.stderr)

        arm = run([ARM, "--phase", "36", "--poll-secs", "1", "--timeout-secs", "1"], self.repo, timeout=10)
        self.assertEqual(arm.returncode, 42, arm.stderr)
        self.assertIn("UNCLAIMED done marker", arm.stderr)
        self.assertIn("channel 'other'", arm.stderr)
        self.assertIn("stage=stage", arm.stderr)

        head = jget(self.channel_dir("other") / "done.json", "head")
        (self.channel_dir("other") / f"claimed.{head}").mkdir()
        quiet = run([ARM, "--phase", "37", "--poll-secs", "1", "--timeout-secs", "1"], self.repo, timeout=10)
        self.assertEqual(quiet.returncode, 42, quiet.stderr)
        self.assertNotIn("UNCLAIMED done marker", quiet.stderr)

    def test_arm_warns_when_replacing_live_armed_json(self):
        sleeper = subprocess.Popen(["sleep", "30"])
        self.addCleanup(self.stop_process, sleeper)
        target = self.channel_dir("same")
        target.mkdir(parents=True)
        (target / "armed.json").write_text(
            '{"kind":"watcher","channel":"same","armed_at":0,"ttl":null,'
            f'"armed_by":"agent-b","pid":{sleeper.pid}}}\n'
        )

        arm = run([ARM, "--channel", "same", "--poll-secs", "1", "--timeout-secs", "1"], self.repo, timeout=10)
        self.assertEqual(arm.returncode, 42, arm.stderr)
        self.assertIn("WARNING: replacing live armed.json on channel 'same'", arm.stderr)
        self.assertIn("armed_by=agent-b", arm.stderr)
        self.assertIn(f"pid={sleeper.pid}", arm.stderr)

    def test_check_and_integrate_accept_phase_equivalent_selector(self):
        with tempfile.TemporaryDirectory() as d:
            main = init_repo(pathlib.Path(d) / "main")
            wt_b = pathlib.Path(d) / "wt_b"
            subprocess.run(
                ["git", "-C", str(main), "worktree", "add", "-q", "-b", "b-branch", str(wt_b)],
                check=True,
            )
            (main / "README.md").write_text("hello\nA\n")
            git(main, "commit", "-q", "-am", "a-work")
            pub = run([PUBLISH, "--phase", "36", "--stage", "stage", "--scope", "README.md"], main)
            self.assertEqual(pub.returncode, 0, pub.stderr)

            pre = run([CHECK, "--phase", "036", "--require-integration"], wt_b)
            self.assertEqual(pre.returncode, 20, pre.stderr)
            self.assertEqual(pre.stdout.strip(), "STALE:not-integrated")

            integ = run([INTEGRATE, "--phase", "36"], wt_b)
            self.assertEqual(integ.returncode, 0, integ.stderr)
            self.assertIn("integrated", integ.stdout)

            chk = run([CHECK, "--channel", "gsd-phase-36", "--require-integration"], wt_b)
            self.assertEqual(chk.returncode, 0, chk.stderr)
            self.assertEqual(chk.stdout.strip(), "WAKE")


if __name__ == "__main__":
    unittest.main()
