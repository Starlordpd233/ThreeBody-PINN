import os
import pathlib
import re
import shutil
import signal
import subprocess
import tempfile
import time
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
COMMON = WD / "lib" / "wd-common.sh"
PUBLISH = WD / "wd-publish-done"
CHECK = WD / "wd-check"
ARM = WD / "wd-arm"
PUSH = WD / "wd-push"
DISARM = WD / "wd-disarm"
STATUS = WD / "wd-status"
INTEGRATE = WD / "wd-integrate"
GSD_PUBLISH = WD / "wd-gsd-publish"

# Git/agent vars that could leak the parent session's repo or identity into a
# temp-repo test are stripped from the inherited environment.
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


def first_token(proc):
    return proc.stdout.split()[0] if proc.stdout.strip() else ""


HOME = pathlib.Path.home()
CANON = HOME / ".claude" / "skills" / "cross-session-watchdog"
CANON_BIN = CANON / "bin"
REPO_SKILL = ROOT / ".claude" / "skills" / "cross-session-watchdog" / "SKILL.md"


class GlobalPackagingTests(unittest.TestCase):
    def setUp(self):
        if not CANON_BIN.exists():
            self.skipTest("global install absent; run tools/watchdog/install-global.sh")

    def test_a5_canonical_bin_matches_repo_source(self):
        for src in sorted(WD.glob("wd-*")):
            dst = CANON_BIN / src.name
            self.assertTrue(dst.exists(), f"canonical missing {dst}")
            self.assertEqual(src.read_bytes(), dst.read_bytes(),
                             f"DRIFT: {src.name} differs between repo and canonical bin")
        self.assertEqual((WD / "lib" / "wd-common.sh").read_bytes(),
                         (CANON_BIN / "lib" / "wd-common.sh").read_bytes(),
                         "DRIFT: wd-common.sh differs between repo and canonical")

    def test_a6_deployed_skill_paths_rewritten(self):
        skill = CANON / "SKILL.md"
        self.assertTrue(skill.exists(), f"missing deployed {skill}")
        text = skill.read_text()
        self.assertNotIn("tools/watchdog/", text,
                         "deployed SKILL.md still has repo-relative tools/watchdog/ paths")
        refs = set(re.findall(
            r"\$HOME/\.claude/skills/cross-session-watchdog/bin/(wd-[a-z-]+)", text))
        self.assertTrue(refs, "deployed SKILL.md references no bin/ tools (rewrite failed?)")
        for name in sorted(refs):
            p = CANON_BIN / name
            self.assertTrue(p.exists() and os.access(p, os.X_OK),
                            f"deployed SKILL.md references non-executable {p}")

    def test_a7_alt_profiles_symlink_to_canonical(self):
        checked = 0
        for profile in ("alt", "free", "max"):
            link = HOME / f".claude-{profile}" / "skills" / "cross-session-watchdog"
            if not link.exists():
                continue
            checked += 1
            self.assertTrue(link.is_symlink(), f"{link} is not a symlink")
            self.assertEqual(os.path.realpath(link), os.path.realpath(CANON),
                             f"{link} does not resolve to canonical {CANON}")
        if checked == 0:
            self.skipTest("no alt profiles present")