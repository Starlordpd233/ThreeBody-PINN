#!/usr/bin/env python3
"""Tests for wd-gsd-publish (Phase 5): the GSD adapter for wd-publish-done.

The adapter maps GSD phase concepts onto the generic, GSD-agnostic core:
  --phase NN  -> stage "gsd:phase-NN"
  --scope STR -> forwarded unchanged
  --channel N -> forwarded (defaults to "default")

done.head is anchored on HEAD by wd-publish-done; by convention the adapter is
run immediately after the verify(NN) commit, so HEAD IS that commit. These tests
verify the arg mapping, validation, clean delegation, and that done.head equals
the caller's HEAD. Channel state is isolated in a throwaway git repo.
"""
import os
import pathlib
import re
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
GSD = WD / "wd-gsd-publish"

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
        args, cwd=str(cwd), text=True,
        capture_output=True, env=merged, check=False, timeout=timeout,
    )


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=False,
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


def jget(path, key):
    """Minimal single-line JSON field extractor (matches the scripts' sed idiom).

    Returns the value of the first `"key":"value"` pair, or None.
    """
    text = pathlib.Path(path).read_text()
    m = re.search(r'"%s":"([^"]*)"' % re.escape(key), text)
    return m.group(1) if m else None


class WdGsdPublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def channel_dir(self, channel):
        return self.repo / ".git" / "live-monitor" / "channels" / channel

    def commit(self, path, content, msg):
        p = self.repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        git(self.repo, "add", path)
        git(self.repo, "commit", "-q", "-m", msg)

    # ----- 1. maps phase -> stage, head = HEAD -----------------------------
    def test_phase_maps_to_stage_and_anchors_head(self):
        # Run immediately after the verify(35) commit — the documented convention
        # that makes HEAD == the verify(NN) commit at publish time.
        self.commit("src/foo", "content\n", "verify(src/foo): phase 35 work")
        head = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        r = run(
            ["bash", str(GSD), "--phase", "35",
             "--scope", "src/foo", "--channel", "demo"],
            self.repo,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        done = self.channel_dir("demo") / "done.json"
        self.assertTrue(done.is_file(), "done.json not written")
        self.assertEqual(jget(done, "stage"), "gsd:phase-35")
        self.assertEqual(jget(done, "scope"), "src/foo")
        self.assertEqual(jget(done, "head"), head)

    # ----- 2. bad --phase / missing --scope -> exit 2 ----------------------
    def test_bad_phase_rejected(self):
        # Non-numeric.
        r = run(["bash", str(GSD), "--phase", "abc",
                 "--scope", "src/foo"], self.repo)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("positive integer", r.stderr)
        # Zero (not positive).
        r2 = run(["bash", str(GSD), "--phase", "0",
                  "--scope", "src/foo"], self.repo)
        self.assertEqual(r2.returncode, 2, r2.stdout)
        # Missing --phase entirely.
        r3 = run(["bash", str(GSD), "--scope", "src/foo"], self.repo)
        self.assertEqual(r3.returncode, 2, r3.stdout)

    def test_missing_scope_rejected(self):
        r = run(["bash", str(GSD), "--phase", "35"], self.repo)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("scope", r.stderr.lower())

    # ----- 3. delegates cleanly to wd-publish-done -------------------------
    def test_delegates_cleanly(self):
        self.commit("src/foo", "content\n", "verify(src/foo): delegate check")
        r = run(
            ["bash", str(GSD), "--phase", "35",
             "--scope", "src/foo", "--channel", "demo"],
            self.repo,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        # wd-publish-done's own success line surfaces unchanged via exec.
        self.assertIn("published done @", r.stdout)


if __name__ == "__main__":
    unittest.main()
