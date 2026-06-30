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


# The fixed wake prompt — byte-exact single-line form (as in wd-push line ~94).
WAKE = (
    "Watchdog: read `consumer-task.md` in this channel and the `wd-arm` result "
    "line; if WAKE, begin that task; if ALREADY-CLAIMED or PRODUCER-STALLED, "
    "stop and report."
)
REPO_SKILL = ROOT / ".claude" / "skills" / "cross-session-watchdog" / "SKILL.md"
HOME_SKILL = pathlib.Path.home() / ".claude" / "skills" / "cross-session-watchdog" / "SKILL.md"

# Verdict tokens the tools emit and the skill doc must name (grep-confirmed in
# wd-arm / wd-push / wd-check on 2026-06-30).
VERDICTS = ("WAKE", "ALREADY-CLAIMED", "PRODUCER-STALLED", "DISARMED", "PUSHED")


def _norm(s):
    # Collapse blockquote ('>') and comment ('#') markers + whitespace runs so a
    # line-wrapped SKILL.md blockquote / wd-arm comment compares equal to the
    # single-line shell constant. Semantic identity, not literal byte identity.
    return re.sub(r"\s+", " ", re.sub(r"[>#]", " ", s)).strip()


class ContractTests(unittest.TestCase):
    def test_a1_shellcheck_clean(self):
        sc = shutil.which("shellcheck")
        if sc is None:
            self.skipTest("shellcheck not installed")
        targets = [str(COMMON)] + [str(p) for p in sorted(WD.glob("wd-*"))]
        proc = subprocess.run([sc, "-S", "error", *targets],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0,
                         "shellcheck errors:\n" + proc.stdout + proc.stderr)

    def test_a2_wake_prompt_consistent(self):
        canon = _norm(WAKE)
        candidates = [PUSH, ARM, REPO_SKILL]
        if HOME_SKILL.exists():
            candidates.append(HOME_SKILL)
        carriers = [c for c in candidates if c.exists() and canon in _norm(c.read_text())]
        names = [c.name for c in carriers]
        # The injector (wd-push) and at least one SKILL.md must carry the prompt.
        self.assertIn("wd-push", names, f"wd-push lost the wake prompt; carriers={names}")
        self.assertTrue(any(c.name == "SKILL.md" for c in carriers),
                        f"no SKILL.md carries the wake prompt; carriers={names}")
        # wd-push carries the byte-exact single-line form.
        self.assertIn(WAKE, PUSH.read_text(), "wd-push prompt is not byte-exact")

    def test_a3_verdict_vocab(self):
        self.assertTrue(REPO_SKILL.exists(), f"missing {REPO_SKILL}")
        skill = REPO_SKILL.read_text()
        tools_text = "\n".join(p.read_text() for p in WD.glob("wd-*"))
        for token in VERDICTS:
            self.assertIn(token, skill, f"SKILL.md does not document verdict {token}")
            self.assertIn(token, tools_text, f"no tool emits verdict {token}")

    def test_a4_watch_loops_restore_set_plus_e(self):
        # wd-arm and wd-push run a long poll loop after sourcing wd-common.sh
        # (which sets -e); both must restore `set +e` so an expected non-zero
        # from wd-check does not kill the loop.
        for tool in (ARM, PUSH):
            text = tool.read_text()
            self.assertRegex(text, r"\n\s*set \+e\b",
                             f"{tool.name} does not restore 'set +e' after sourcing")