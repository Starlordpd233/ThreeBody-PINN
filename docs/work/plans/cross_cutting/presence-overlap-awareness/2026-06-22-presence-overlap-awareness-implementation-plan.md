---
status: consumed
purpose: implementation-plan
created: 2026-06-22
milestone: untracked
phase: cross-cutting
retirement_trigger: Retire when all tasks are executed, the test suite is green, and the operating contract is merged into docs/git-guidelines.md; or when superseded by a consolidated parallel-agent-coordination plan.
execution_status: executed
executed_at: 2026-06-26T13:38:00+08:00
review_status: reviewed
reviewed_at: 2026-06-26
---

# Presence & Overlap Awareness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a passive, advisory presence registry on top of the existing claims board so a starting agent can see who else is live, read each peer's plain-language task summary, and reason about task/scope overlap before working.

**Architecture:** A new stdlib-only Python module `agent_presence.py` writes one JSON file per live top-level session under the shared git common dir (beside `agent-claims/`). Sessions register at SessionStart (via `session_banner.sh`), heartbeat on every edit (via `claim_guard.py`), and deregister at Stop (via a new `.claude/settings.json` hook). A session's *write set* is **derived** from the claims board (never duplicated). The agent runs one `announce` CLI call after its first prompt to set its task summary and declare intended write areas, then applies a documented graduated-autonomy protocol. Everything is advisory and fails open; the commit-time owned-paths net in `scripts/agent-commit` stays the only hard backstop.

**Tech Stack:** Python 3 standard library only (`os`, `json`, `subprocess`, `time`, `re`, `sys`). Tests use `unittest` driven by `python3 tests/git_policy/test_presence.py`, mirroring the isolated-temp-repo harness in `tests/git_policy/test_concurrency.py`. Bash shims mirror `scripts/agent-claim`.

## Operating model & design priorities

This repo is **agent-first**: agents run the planning, GSD processes, execution, and review for nearly all work, and human attention is reserved for decisions a human *must* own. This plan is built — and must be executed — in that priority order:

1. **Agent-autonomy by default.** If an agent can resolve a situation itself, it should; escalating to a human is a fallback for genuine deadlock, not a routine step. This is deliberately *distinct* from the v1.4/v1.5 **adjudication** STOP protocol in `CLAUDE.md` (which surfaces spec/physics decisions to the user on purpose): presence/overlap is **operational coordination**, so it defaults to agent-autonomous resolution and does **not** relax that adjudication norm.
2. **Prevent mistakes by construction.** The mechanical layer makes correct behavior the easy default — auto-register, auto-heartbeat, board-derived write sets, declare-not-seize — so an agent has little to remember to behave well.
3. **Stay recoverable when a mistake slips through.** Everything is advisory and fail-open; presence state self-heals (sweep + 2 h TTL); every task is an atomic, revertible commit; and the commit-time owned-paths net stays the one hard backstop. A wrong overlap call must only ever cost a little rework — never corrupt work or block an agent.

When a choice trades these off, prefer accuracy and recoverability over cleverness, and agent-autonomy over human escalation.

## Global Constraints

- **Source of identity:** the Claude session id. Hooks (SessionStart `register`, Stop `deregister`, PreToolUse `heartbeat`) read it from their **stdin payload** `session_id` — the documented Claude Code channel and the same field `claim_guard.py` already uses. The SessionStart hook additionally **seeds** `CLAUDE_CODE_SESSION_ID` into `CLAUDE_ENV_FILE` so later **agent Bash-tool** calls (`announce`, `list`) can read it from the environment (those calls have no hook payload). `CLAUDE_CODE_SESSION_ID` is therefore *seeded by us*, not assumed to pre-exist (it is not in Claude Code's documented hook env vars). The join key with the claims board is the string `session:<session_id>` — exactly what `claim_guard.py` writes as `AGENT_CLAIM_WHO`. Probe 1a (Task 0) verifies the seeded env var equals the payload id before any build.
- **Advisory / fail-open everywhere:** every library entry point swallows its own exceptions and the CLI always returns exit code 0. A presence failure must never block an edit, a hook, or the agent's shell. The only hard backstop is the owned-paths check in `scripts/agent-commit`.
- **Atomic writes:** all presence-file writes use the `tmp` + `os.replace` pattern already used by `agent_claims.claim`.
- **Claims board is the single source of truth for "who writes what."** Presence stores only liveness + intent (`task_summary`); claimed areas are derived by scanning the board, never persisted in the presence file (design decision #4, adopted).
- **Adopted design decisions:** (1) 20-minute heartbeat-stale floor; a `kill -0`-live pid is **never** reaped for idleness, and a pid that is absent **or untrusted** (e.g. the transient SessionStart shell captured by `getppid()`) falls through to the floor rather than being reaped on sight — this is the design reaping table's row 3 (the floor is the real backstop for untrusted PIDs); (2) **RESOLVED 2026-06-26 (user-confirmed):** cross-worktree weighting (visible-but-marked; file-collision weight highest for same-worktree/same-branch; semantic-duplication weight across all peers). Originally a *reconstruction of garbled source text* per the design's Open Decision #2; the user confirmed during post-execution review that it matches intent, so it is now settled; (3) deregister = release-on-exit, expire-on-crash (Stop releases claims, the claims board's existing 2 h TTL is the crash backstop); (4) `claimed_areas` derived, not persisted.
- **Non-goals (do NOT build):** cross-session activation / the watchdog, any daemon / polling / `tmux send-keys` / cron, any lock that blocks an edit or commit, and sub-file / line-range claim granularity (Decision R1: rejected — the claims engine prefix-matches on `/`).
- **Execution location:** this is cross-cutting parallel-agent infrastructure; like the claims board it lives on **`master`** and is developed from the **master-root** worktree. **Never push from `master`** — commits are local-only.
- **Commit policy (every task):** commit via `scripts/agent-commit` only, with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set to explicit owned paths; stage explicit paths only (never `git add -A/-u/.`). Conventional message `<type>(governance): <lowercase imperative>`; body required (governance + multi-file); include an `Agent-Assisted-By:` or `Co-Authored-By:` trailer. Re-run `git status --short --branch` before each commit.

---

## Scope & sequencing note (review outcome)

The mechanical layer (Tasks 1–8) plus an announce nudge and a single "if a peer's
summary looks like your task, stand down and redirect to other work" rule delivers
the core value and is recommended as the MVP. The following are **deferral-eligible** and should not be
built until explicitly confirmed:

- **Task 9 (Stop hook)** — correctness-non-critical (dead-pid sweep + 2 h TTL already
  clean up) and the only shared-`.claude/settings.json` touch. Defer unless prompt
  cleanup is wanted.
- **Task 10 graduated-autonomy matrix + A1/A2/B/C/D taxonomy** — unenforced prose with
  no code consuming it; the value is the agent *seeing* peer summaries, which the
  roster already provides. Keep S1 (the headline duplicate-task case); the rest can
  collapse to the one stand-down rule for v1.
- **Cross-worktree weighting** — Decision #2 was **RESOLVED 2026-06-26** (user-confirmed
  during post-execution review; originally reconstructed from garbled source text).

---

## Task 0: Pre-build verification gate

**No code.** Confirm the load-bearing identity assumption (Probe 1a) before writing any module code. Probe 2 (pid durability) is **no longer a blocker** because the reaper now treats an untrusted pid as floor-governed rather than trusting `getppid()` (see Task 2); it is kept below as an informational observation. Probes 3 and 4 remain non-blocking confirmations folded into later tasks with graceful-degradation contingencies.

**Probe 1a — identity equality (HARD BLOCKER).** Hooks (`register`/`deregister`/`heartbeat`) read the session id from their **stdin payload**; agent Bash-tool calls (`announce`/`list`) read it from the **seeded** `CLAUDE_CODE_SESSION_ID` env var (Task 8 writes it into `CLAUDE_ENV_FILE` at SessionStart). The join works only if the value an agent Bash-tool call sees equals the payload id `claim_guard` writes. **Run this probe as a normal agent Bash-tool call** — the same context `announce`/`list` use — so it exercises the real environment.

- [ ] **Step 1: Capture the env identity (agent Bash-tool call).**

Run: `echo "$CLAUDE_CODE_SESSION_ID"`
- Non-empty UUID-like string → record it as `ENV_SID` and go to Step 2.
- **Empty** → expected *before* Task 8 seeds it. De-risk now by confirming the seeding mechanism exists: from a SessionStart hook, `echo "$CLAUDE_ENV_FILE"` must yield a writable path (that is how Task 8 will export `CLAUDE_CODE_SESSION_ID` to later tool calls). If `CLAUDE_ENV_FILE` is also unavailable here, **STOP and surface to the user** — the seeding strategy is unsupported and the design must change (e.g. the agent passes `--session` explicitly).

- [ ] **Step 2: Capture the claim_guard payload identity.**

Make one real edit this session (writing this plan file already did so), then read the newest claims-board record's `who`:

Run: `python3 - <<'PY'
import os, subprocess, json, glob
common = subprocess.run(["git","rev-parse","--git-common-dir"],text=True,capture_output=True).stdout.strip()
root = subprocess.run(["git","rev-parse","--show-toplevel"],text=True,capture_output=True).stdout.strip()
common = common if os.path.isabs(common) else os.path.join(root, common)
d = os.path.join(common, "agent-claims")
whos = set()
for f in glob.glob(os.path.join(d, "*")):
    try:
        whos.add(json.load(open(f)).get("who"))
    except Exception:
        pass
print("env :", "session:" + os.environ.get("CLAUDE_CODE_SESSION_ID",""))
print("board who values:", sorted(whos))
PY`
Expected: `session:$CLAUDE_CODE_SESSION_ID` appears among the board's `who` values (the claim auto-declared by `claim_guard` on a recent edit by this session).

- [ ] **Step 3: Verdict.**

PASS if (a) Step 1 yields a non-empty id in an agent Bash-tool call **or** `CLAUDE_ENV_FILE` is confirmed available so Task 8 can seed it, **and** (b) `session:$CLAUDE_CODE_SESSION_ID` matches the `who` `claim_guard` wrote for this session. Proceed to Task 1.
FAIL → do not build. The env var is the only identity source for `announce`/`list`, which are **not hooks and have no stdin payload to fall back to**. Contingency options, in order: (i) confirm `CLAUDE_ENV_FILE` seeding works and rely on it (Task 8); (ii) have the agent pass `--session "$CLAUDE_CODE_SESSION_ID"` on every `announce`/`list`; (iii) resolve identity from the claims board's most-recent payload-seeded `who` for this session. Surface the failure to the user before changing the design.

**Probe 2 — `getppid()` durability (INFORMATIONAL, no longer a blocker).** At SessionStart the hook's `getppid()` is typically the *transient* shell running `session_banner.sh`, which exits immediately — so its pid is usually a dead, **untrusted** pid within milliseconds. The reaper (Task 2) is built for this: a pid is trusted only while `kill -0` succeeds; a dead/untrusted pid is **not** reaped on sight but falls through to the 20-minute heartbeat-stale floor, and `register`/`announce`/`heartbeat` keep the heartbeat fresh so an active session is never reaped. Optional observation after `register` exists: read a presence file's `pid` and run `ps -p <pid> -o comm=`. If it is the durable `claude` process you additionally get "live-pid → never reaped even when idle"; if it is a shell, the floor governs. Either way no design change is required.

**Probe 3 — subagent identity (NON-BLOCKING, documented in Task 10).** Inspect whether `CLAUDE_CODE_SESSION_ID` changes inside an Agent-tool subagent and what `CLAUDE_CODE_CHILD_SESSION` holds. If subagent edits carry a distinct child id, their auto-declared claims become orphan records that expire under the 2 h TTL and never attach to a rostered session — acceptable per the design's contingency. `register` is wired only to SessionStart, so subagents never create presence files regardless.

**Probe 4 — Stop reliability (NON-BLOCKING, verified in Task 9).** The Stop hook must fire with the session id available so `deregister` can release claims. If it does not fire, the dead-PID sweep (Task 2) plus the 2 h TTL still reap the session — Stop only makes cleanup prompt, not correct.

- [ ] **Step 4: Record the gate result** in the eventual commit body for Task 1 (one line, e.g. "Probe 1a PASS: agent-Bash CLAUDE_CODE_SESSION_ID == claim_guard payload who; CLAUDE_ENV_FILE seeding available").

---

## Task 1: Claims-board query and release helpers

Add two small, pure helpers to the existing (tested) claims module. The roster derives a session's write set with `claims_for_who`; `deregister` and the dead-PID sweep release a session's claims with `release_by_who`. Keeping claim-file mechanics in `agent_claims.py` preserves the single source of truth.

**Files:**
- Modify: `scripts/git_policy/agent_claims.py` (append two functions after `list_claims`)
- Create: `tests/git_policy/test_presence.py`

**Interfaces:**
- Consumes: existing `agent_claims.{claims_dir, load, expired, sweep}`.
- Produces:
  - `agent_claims.claims_for_who(who: str) -> list[str]` — sorted non-expired areas held by `who`.
  - `agent_claims.release_by_who(who: str) -> int` — removes every claim file whose `who` matches; returns count removed.

- [ ] **Step 1: Write the failing test (creates the shared harness).**

Create `tests/git_policy/test_presence.py`:

```python
#!/usr/bin/env python3
"""Tests for the advisory presence registry (agent_presence.py) and the
claims-board helpers it relies on (claims_for_who / release_by_who).

Every test isolates shared state in a throwaway git repo (cwd is chdir'd into
it), so the live presence registry and claims board under the real repo's .git/
are never touched. Identity/floor env vars are stripped per-test so the parent
session never leaks into a temp-repo assertion.
"""
import importlib
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
GIT_POLICY = ROOT / "scripts" / "git_policy"

ISOLATED_KEYS = (
    "AGENT_CLAIM_WHO",
    "AGENT_CLAIM_EXPIRY",
    "AGENT_PRESENCE_STALE",
    "CLAUDE_CODE_SESSION_ID",
    "CLAUDE_CODE_CHILD_SESSION",
    "GIT_AGENT_ID",
)

sys.path.insert(0, str(GIT_POLICY))
import agent_claims  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=False)


def init_repo(path):
    # .resolve() collapses the macOS /var -> /private/var symlink so cwd-based
    # abspath() and git's realpath toplevel agree.
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    return path


class PresenceTestBase(unittest.TestCase):
    """Temp git repo + cwd + env isolation, shared by all in-process tests."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        prev = os.getcwd()
        os.chdir(self.repo)
        self.addCleanup(lambda: os.chdir(prev))
        saved = {k: os.environ.get(k) for k in ISOLATED_KEYS}
        for k in ISOLATED_KEYS:
            os.environ.pop(k, None)

        def restore():
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

        self.addCleanup(restore)


class ClaimsByWhoTests(PresenceTestBase):
    def test_claims_for_who_returns_only_that_whos_areas(self):
        os.environ["AGENT_CLAIM_WHO"] = "session:A"
        agent_claims.claim("sim/a.py")
        agent_claims.claim("sim/b.py")
        os.environ["AGENT_CLAIM_WHO"] = "session:B"
        agent_claims.claim("pinn/c.py")
        self.assertEqual(agent_claims.claims_for_who("session:A"),
                         ["sim/a.py", "sim/b.py"])
        self.assertEqual(agent_claims.claims_for_who("session:B"), ["pinn/c.py"])

    def test_release_by_who_removes_only_that_whos_claims(self):
        os.environ["AGENT_CLAIM_WHO"] = "session:A"
        agent_claims.claim("sim/a.py")
        os.environ["AGENT_CLAIM_WHO"] = "session:B"
        agent_claims.claim("pinn/c.py")
        removed = agent_claims.release_by_who("session:A")
        self.assertEqual(removed, 1)
        self.assertEqual(agent_claims.claims_for_who("session:A"), [])
        self.assertEqual(agent_claims.claims_for_who("session:B"), ["pinn/c.py"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py ClaimsByWhoTests -v`
Expected: FAIL with `AttributeError: module 'agent_claims' has no attribute 'claims_for_who'`.

- [ ] **Step 3: Implement the helpers.**

Append to `scripts/git_policy/agent_claims.py` (after `list_claims`, before `main`):

```python
def claims_for_who(who):
    """Return the sorted non-expired areas currently claimed by `who`."""
    sweep()
    areas = []
    directory = claims_dir()
    for name in os.listdir(directory):
        entry = load(os.path.join(directory, name))
        if entry is None or expired(entry):
            continue
        if entry.get("who") == who:
            area = entry.get("area")
            if area:
                areas.append(area)
    return sorted(areas)


def release_by_who(who):
    """Remove every claim held by `who`. Returns the count removed."""
    directory = claims_dir()
    removed = 0
    for name in os.listdir(directory):
        full = os.path.join(directory, name)
        entry = load(full)
        if entry is not None and entry.get("who") == who:
            try:
                os.remove(full)
                removed += 1
            except OSError:
                pass
    return removed
```

- [ ] **Step 4: Run the test to verify it passes.**

Run: `python3 tests/git_policy/test_presence.py ClaimsByWhoTests -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/git_policy/agent_claims.py tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_claims.py:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): add claims-board who-scoped query and release helpers" \
  -m "Add claims_for_who and release_by_who to support presence-roster area derivation and session deregistration. Probe 1a PASS: claim_guard payload session_id == CLAUDE_CODE_SESSION_ID." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: Presence module core — directory, identity, atomicity, register, sweep

Create `agent_presence.py` with the location/identity primitives, the persisted schema via `register`, and the reaper `sweep_presence` (live-PID keep, dead-PID reap, heartbeat-floor for absent PID).

**Files:**
- Create: `scripts/git_policy/agent_presence.py`
- Modify: `tests/git_policy/test_presence.py` (append `RegisterSweepTests`)

**Interfaces:**
- Consumes: `agent_claims.{load, release_by_who}`.
- Produces:
  - `presence_dir() -> str`; `_safe_session_id(sid) -> str|None`; `presence_file(sid) -> str|None`; `who_key(sid) -> str`
  - `_session_from_env() -> str|None`; `_session_from_stdin() -> str|None`; `_pid_alive(pid) -> bool`; `_atomic_write(path, obj) -> None`; `_git_context() -> (worktree, branch)`; `_load_or_init(sid) -> dict`; `_stale_floor() -> int`
  - `register(session_id=None, pid=None) -> str` (roster string; `""` when no identity)
  - `sweep_presence() -> None`
  - Schema written: `{session_id, pid, worktree, branch, start_time, task_summary, last_heartbeat}`

- [ ] **Step 1: Write the failing test.**

Append to `tests/git_policy/test_presence.py` (before the `if __name__` line):

```python
class RegisterSweepTests(PresenceTestBase):
    def _load(self, sid):
        import agent_presence
        return agent_claims.load(agent_presence.presence_file(sid))

    def test_register_writes_schema_with_live_pid(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        entry = self._load("sid-1")
        self.assertEqual(entry["session_id"], "sid-1")
        self.assertEqual(entry["pid"], os.getpid())
        self.assertIsNone(entry["task_summary"])
        self.assertIn("start_time", entry)
        self.assertIn("last_heartbeat", entry)

    def test_register_is_idempotent_and_preserves_summary(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        path = agent_presence.presence_file("sid-1")
        entry = agent_claims.load(path)
        entry["task_summary"] = "do the thing"
        entry["start_time"] = 111
        agent_presence._atomic_write(path, entry)
        agent_presence.register("sid-1", pid=os.getpid())  # re-register (resume)
        again = self._load("sid-1")
        self.assertEqual(again["task_summary"], "do the thing")
        self.assertEqual(again["start_time"], 111)

    def test_sweep_keeps_live_pid_even_when_heartbeat_old(self):
        import agent_presence
        os.environ["AGENT_PRESENCE_STALE"] = "0"  # floor would reap if applied
        agent_presence.register("sid-live", pid=os.getpid())
        path = agent_presence.presence_file("sid-live")
        entry = agent_claims.load(path)
        entry["last_heartbeat"] = 0  # ancient
        agent_presence._atomic_write(path, entry)
        agent_presence.sweep_presence()
        self.assertIsNotNone(self._load("sid-live"))  # live pid => kept

    def test_sweep_reaps_dead_pid_past_floor_and_releases_claims(self):
        import agent_presence
        os.environ["AGENT_PRESENCE_STALE"] = "0"  # collapse the floor
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()  # pid now dead
        os.environ["AGENT_CLAIM_WHO"] = agent_presence.who_key("sid-dead")
        agent_claims.claim("sim/owned.py")
        os.environ.pop("AGENT_CLAIM_WHO", None)
        agent_presence.register("sid-dead", pid=dead.pid)
        path = agent_presence.presence_file("sid-dead")
        entry = agent_claims.load(path)
        entry["last_heartbeat"] = 0  # ancient -> past the (zero) floor
        agent_presence._atomic_write(path, entry)
        agent_presence.sweep_presence()
        self.assertIsNone(self._load("sid-dead"))                     # reaped
        self.assertEqual(agent_claims.claims_for_who(
            agent_presence.who_key("sid-dead")), [])                  # claims released

    def test_sweep_keeps_dead_pid_within_floor(self):
        # A transient SessionStart shell pid dies immediately; an actively
        # heartbeating session must survive (untrusted pid -> floor, not reap).
        import agent_presence
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        agent_presence.register("sid-untrusted", pid=dead.pid)  # dead nonzero pid
        # last_heartbeat is fresh (register set it); default 20-min floor applies
        agent_presence.sweep_presence()
        self.assertIsNotNone(self._load("sid-untrusted"))  # kept by the floor grace

    def test_sweep_reaps_pidless_entry_past_floor(self):
        import agent_presence
        os.environ["AGENT_PRESENCE_STALE"] = "0"
        agent_presence.register("sid-x", pid=os.getpid())
        path = agent_presence.presence_file("sid-x")
        entry = agent_claims.load(path)
        entry["pid"] = None          # untrusted/absent pid
        entry["last_heartbeat"] = 0  # past the (zero) floor
        agent_presence._atomic_write(path, entry)
        agent_presence.sweep_presence()
        self.assertIsNone(self._load("sid-x"))

    def test_register_without_identity_is_silent(self):
        import agent_presence
        self.assertEqual(agent_presence.register(None), "")  # no env, no arg
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py RegisterSweepTests -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'agent_presence'`.

- [ ] **Step 3: Create the module.**

Create `scripts/git_policy/agent_presence.py`:

```python
#!/usr/bin/env python3
"""Advisory presence registry: one JSON file per live top-level session.

Sits on top of the claims board (agent_claims.py) and shares its git
common-dir location so every worktree sees the same roster. A presence file
records liveness (pid, last_heartbeat) and intent (task_summary); a session's
*write set* is derived from the claims board, never duplicated here.

Identity is the Claude session id. Hooks read it from their stdin payload; agent
Bash-tool calls read it from CLAUDE_CODE_SESSION_ID, which the SessionStart hook
seeds into CLAUDE_ENV_FILE (it is not assumed to pre-exist). The join key with the
claims board is "session:<session_id>" -- exactly what claim_guard.py writes as
AGENT_CLAIM_WHO.

Advisory only: every entry point fails open and the CLI always exits 0. The one
hard backstop against silent overwrite is the commit-time owned-paths net in
scripts/agent-commit, not this module.
"""
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_claims  # noqa: E402

FRESH_SECONDS = 120
_SAFE_SID = re.compile(r"^[A-Za-z0-9._-]+$")


def _stale_floor():
    return int(os.environ.get("AGENT_PRESENCE_STALE", str(20 * 60)))


def presence_dir():
    common = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    if not os.path.isabs(common):
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        common = os.path.join(root, common)
    path = os.path.join(common, "agent-presence")
    os.makedirs(path, exist_ok=True)
    return path


def _safe_session_id(session_id):
    if not session_id:
        return None
    session_id = str(session_id).strip()
    return session_id if _SAFE_SID.match(session_id) else None


def presence_file(session_id):
    sid = _safe_session_id(session_id)
    if sid is None:
        return None
    return os.path.join(presence_dir(), f"{sid}.json")


def who_key(session_id):
    return f"session:{session_id}"


def _session_from_env():
    return _safe_session_id(os.environ.get("CLAUDE_CODE_SESSION_ID"))


def _session_from_stdin():
    # Only read a piped payload; never block on an interactive tty.
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return None
        payload = json.load(sys.stdin)
    except Exception:
        return None
    return _safe_session_id(payload.get("session_id"))


def _pid_alive(pid):
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 1:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True   # exists, owned by another user
    except OSError:
        return False


def _atomic_write(path, obj):
    tmp = f"{path}.tmp"
    with open(tmp, "w") as handle:
        json.dump(obj, handle)
    os.replace(tmp, path)


def _git_context():
    try:
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
    except Exception:
        return "?", "?"
    worktree = os.path.basename(root) or "?"
    try:
        branch = subprocess.run(
            ["git", "-C", root, "symbolic-ref", "--short", "HEAD"],
            text=True, capture_output=True, check=True,
        ).stdout.strip() or "DETACHED"
    except Exception:
        branch = "DETACHED"
    return worktree, branch


def _load_or_init(session_id):
    path = presence_file(session_id)
    entry = agent_claims.load(path) if path else None
    if entry is None:
        now = int(time.time())
        entry = {
            "session_id": session_id,
            "pid": None,
            "worktree": "?",
            "branch": "?",
            "start_time": now,
            "task_summary": None,
            "last_heartbeat": now,
        }
    return entry


def sweep_presence():
    directory = presence_dir()
    now = int(time.time())
    floor = _stale_floor()
    for name in os.listdir(directory):
        full = os.path.join(directory, name)
        if name.endswith(".tmp"):
            try:
                os.remove(full)
            except OSError:
                pass
            continue
        entry = agent_claims.load(full)
        if entry is None:
            continue
        pid = entry.get("pid")
        if pid and _pid_alive(pid):
            continue                # trusted-live: keep regardless of heartbeat age
        # Absent, dead, OR untrusted pid (e.g. the transient SessionStart shell
        # captured by getppid()): do NOT reap on sight -- fall through to the
        # heartbeat-stale floor (design reaping table row 3). register/announce/
        # heartbeat keep last_heartbeat fresh, so an active session is never reaped.
        reap = (now - entry.get("last_heartbeat", 0)) > floor
        if reap:
            sid = entry.get("session_id")
            if sid:
                agent_claims.release_by_who(who_key(sid))
            try:
                os.remove(full)
            except OSError:
                pass


def register(session_id=None, pid=None):
    session_id = _safe_session_id(session_id) or _session_from_env()
    if session_id is None:
        return ""   # no identity -> no presence; stay silent
    sweep_presence()
    entry = _load_or_init(session_id)
    worktree, branch = _git_context()
    entry["session_id"] = session_id
    entry["pid"] = int(pid) if pid is not None else os.getppid()
    entry["worktree"] = worktree
    entry["branch"] = branch
    entry["last_heartbeat"] = int(time.time())
    _atomic_write(presence_file(session_id), entry)
    return list_roster(exclude=session_id)
```

> Note: `register` calls `list_roster` (defined in Task 3). The module will not be import-complete until Task 3 adds it. To keep Task 2's tests green now, also append the Task 3 stub at the bottom of the file in this step — replace it with the full body in Task 3. Stub:
>
> ```python
> def list_roster(exclude=None):
>     return ""  # full implementation in Task 3
> ```

- [ ] **Step 4: Run the test to verify it passes.**

Run: `python3 tests/git_policy/test_presence.py RegisterSweepTests -v`
Expected: PASS (7 tests).

- [ ] **Step 5: Confirm Probe 2 (non-blocking).**

After registering once in a real session, run `python3 scripts/git_policy/agent_presence.py list` then inspect a presence file's `pid` with `ps -p <pid> -o comm=`. Note whether it is `claude` (trusted) or a shell (floor-backstopped). Record the observation in the commit body. No code change either way.

- [ ] **Step 6: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/git_policy/agent_presence.py tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_presence.py:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): add presence registry core with register and sweep" \
  -m "New agent_presence.py: identity primitives, atomic schema write via register, and sweep_presence (live-pid keep, dead-pid reap with claim release, heartbeat floor for absent pid). list_roster stubbed pending Task 3. Probe 2 observation: <claude|shell>." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: heartbeat, roster derivation, and line formatting

Add the per-edit `heartbeat` bump, the `list_roster` that derives each peer's write set from the board, and the `_format_line` renderer matching the spec's roster format.

**Files:**
- Modify: `scripts/git_policy/agent_presence.py` (add `heartbeat`, replace the `list_roster` stub, add `_format_line`)
- Modify: `tests/git_policy/test_presence.py` (append `RosterHeartbeatTests`)

**Interfaces:**
- Consumes: `agent_claims.claims_for_who`, Task 2 primitives.
- Produces:
  - `heartbeat(session_id) -> int` (0; no-op when no presence file exists)
  - `list_roster(exclude=None) -> str` (multi-line roster; current session excluded; areas derived from the board)
  - `_format_line(entry, areas, now, my_worktree=None) -> str`

- [ ] **Step 1: Write the failing test.**

Append to `tests/git_policy/test_presence.py`:

```python
class RosterHeartbeatTests(PresenceTestBase):
    def test_heartbeat_bumps_only_existing_file(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        path = agent_presence.presence_file("sid-1")
        entry = agent_claims.load(path)
        entry["last_heartbeat"] = 100
        agent_presence._atomic_write(path, entry)
        self.assertEqual(agent_presence.heartbeat("sid-1"), 0)
        self.assertGreater(agent_claims.load(path)["last_heartbeat"], 100)

    def test_heartbeat_missing_file_is_noop(self):
        import agent_presence
        self.assertEqual(agent_presence.heartbeat("never-registered"), 0)
        self.assertIsNone(agent_claims.load(
            agent_presence.presence_file("never-registered")))

    def test_roster_excludes_self_and_derives_areas(self):
        import agent_presence
        agent_presence.register("me", pid=os.getpid())
        agent_presence.register("peer", pid=os.getpid())
        os.environ["AGENT_CLAIM_WHO"] = agent_presence.who_key("peer")
        agent_claims.claim("ctl_instruction.md")
        os.environ.pop("AGENT_CLAIM_WHO", None)
        roster = agent_presence.list_roster(exclude="me")
        self.assertIn("[peer", roster)
        self.assertNotIn("[me]", roster)
        self.assertIn("ctl_instruction.md", roster)

    def test_roster_empty_when_alone(self):
        import agent_presence
        agent_presence.register("me", pid=os.getpid())
        self.assertIn("none", agent_presence.list_roster(exclude="me"))

    def test_roster_marks_cross_worktree_peer(self):
        import agent_presence
        agent_presence.register("me", pid=os.getpid())
        agent_presence.register("peer", pid=os.getpid())
        ppath = agent_presence.presence_file("peer")
        pe = agent_claims.load(ppath)
        pe["worktree"] = "some-other-worktree"  # force a different worktree
        agent_presence._atomic_write(ppath, pe)
        roster = agent_presence.list_roster(exclude="me")
        self.assertIn("[cross-worktree]", roster)
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py RosterHeartbeatTests -v`
Expected: FAIL — `test_roster_excludes_self_and_derives_areas` fails (stub returns `""`), `heartbeat` is undefined.

- [ ] **Step 3: Implement.**

In `scripts/git_policy/agent_presence.py`, add `heartbeat` (after `register`) and **delete the Task 2 `list_roster` stub** (the two-line `def list_roster(exclude=None): return ""` at the bottom of the file), replacing it with the full body below plus `_format_line`. Afterward confirm there is exactly one `def list_roster` in the file:

```python
def heartbeat(session_id):
    sid = _safe_session_id(session_id)
    if sid is None:
        return 0
    path = presence_file(sid)
    entry = agent_claims.load(path) if path else None
    if entry is None:
        return 0   # no registered presence -> nothing to bump (fail-safe)
    entry["last_heartbeat"] = int(time.time())
    _atomic_write(path, entry)
    return 0


def _format_line(entry, areas, now, my_worktree=None):
    sid = (entry.get("session_id") or "????")[:4]
    worktree = entry.get("worktree") or "?"
    branch = entry.get("branch") or "?"
    summary = entry.get("task_summary") or "(no task announced)"
    age = now - entry.get("last_heartbeat", now)
    heart = "fresh" if age < FRESH_SECONDS else f"{age // 60}m"
    writes = ", ".join(areas) if areas else "none"
    # Cross-worktree peers are visible but marked (design roster format).
    mark = "" if (my_worktree is None or worktree == my_worktree) else "  [cross-worktree]"
    return (f"  [{sid}] {worktree} / {branch}{mark} — \"{summary}\"\n"
            f"         writes: {writes}   ♥ {heart}")


def list_roster(exclude=None):
    sweep_presence()
    if exclude is None:
        exclude = _session_from_env()
    directory = presence_dir()
    now = int(time.time())
    my_worktree, _ = _git_context()
    lines = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        entry = agent_claims.load(os.path.join(directory, name))
        if entry is None:
            continue
        sid = entry.get("session_id")
        if sid and sid == exclude:
            continue
        areas = agent_claims.claims_for_who(who_key(sid)) if sid else []
        lines.append(_format_line(entry, areas, now, my_worktree))
    if not lines:
        return "Active sessions (excluding yours): none"
    return "Active sessions (excluding yours):\n" + "\n".join(lines)
```

- [ ] **Step 4: Run the test to verify it passes.**

Run: `python3 tests/git_policy/test_presence.py RosterHeartbeatTests -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/git_policy/agent_presence.py tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_presence.py:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): add presence heartbeat and board-derived roster" \
  -m "heartbeat bumps last_heartbeat (no-op without a presence file); list_roster derives each peer's write set from the claims board via claims_for_who and renders the spec roster format, excluding the current session." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: announce — set task summary and declare intended write set

`announce` sets the session's `task_summary` and declares its intended write areas on the claims board (attributed to `session:<id>`). Areas are explicit; never parsed from the summary. It respects peer claims (best-effort declaration, not a seize, because `agent_claims.claim` declines a foreign-held area).

**Files:**
- Modify: `scripts/git_policy/agent_presence.py` (add `announce`)
- Modify: `tests/git_policy/test_presence.py` (append `AnnounceTests`)

**Interfaces:**
- Consumes: `agent_claims.claim`, `who_key`, `_load_or_init`, `_atomic_write`.
- Produces: `announce(session_id, summary, areas) -> str` (roster string).

- [ ] **Step 1: Write the failing test.**

Append to `tests/git_policy/test_presence.py`:

```python
class AnnounceTests(PresenceTestBase):
    def test_announce_sets_summary_and_claims_areas(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        agent_presence.announce("sid-1", "adjudicate phase 32", ["a.md", "b.md"])
        entry = agent_claims.load(agent_presence.presence_file("sid-1"))
        self.assertEqual(entry["task_summary"], "adjudicate phase 32")
        self.assertEqual(
            agent_claims.claims_for_who(agent_presence.who_key("sid-1")),
            ["a.md", "b.md"])

    def test_announce_empty_areas_sets_summary_only(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        agent_presence.announce("sid-1", "just thinking", [])
        entry = agent_claims.load(agent_presence.presence_file("sid-1"))
        self.assertEqual(entry["task_summary"], "just thinking")
        self.assertEqual(
            agent_claims.claims_for_who(agent_presence.who_key("sid-1")), [])

    def test_announce_does_not_seize_peer_claim(self):
        import agent_presence
        os.environ["AGENT_CLAIM_WHO"] = agent_presence.who_key("peer")
        agent_claims.claim("contested.md")
        os.environ.pop("AGENT_CLAIM_WHO", None)
        agent_presence.register("mine", pid=os.getpid())
        agent_presence.announce("mine", "try to take it", ["contested.md"])
        # peer still owns it; announce did not clobber
        self.assertEqual(
            agent_claims.claims_for_who(agent_presence.who_key("peer")),
            ["contested.md"])
        self.assertEqual(
            agent_claims.claims_for_who(agent_presence.who_key("mine")), [])
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py AnnounceTests -v`
Expected: FAIL with `AttributeError: module 'agent_presence' has no attribute 'announce'`.

- [ ] **Step 3: Implement `announce`.**

Add to `scripts/git_policy/agent_presence.py` (after `announce`'s dependencies, e.g. after `heartbeat`):

```python
def announce(session_id, summary, areas):
    session_id = _safe_session_id(session_id) or _session_from_env()
    if session_id is None:
        return ""
    entry = _load_or_init(session_id)
    entry["session_id"] = session_id
    if entry.get("pid") is None:
        entry["pid"] = os.getppid()
    if entry.get("worktree") in (None, "?"):
        entry["worktree"], entry["branch"] = _git_context()
    entry["task_summary"] = summary
    entry["last_heartbeat"] = int(time.time())
    _atomic_write(presence_file(session_id), entry)
    # Declare the intended write set on the board, attributed to this session.
    # Save/restore AGENT_CLAIM_WHO so announce never leaks identity into a
    # longer-lived process that later calls agent_claims under its own who.
    saved_who = os.environ.get("AGENT_CLAIM_WHO")
    os.environ["AGENT_CLAIM_WHO"] = who_key(session_id)
    try:
        for area in areas:
            area = area.strip()
            if area:
                agent_claims.claim(area, why="announced intent")
    finally:
        if saved_who is None:
            os.environ.pop("AGENT_CLAIM_WHO", None)
        else:
            os.environ["AGENT_CLAIM_WHO"] = saved_who
    return list_roster(exclude=session_id)
```

- [ ] **Step 4: Run the test to verify it passes.**

Run: `python3 tests/git_policy/test_presence.py AnnounceTests -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/git_policy/agent_presence.py tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_presence.py:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): add presence announce for task summary and intended writes" \
  -m "announce sets task_summary and declares explicit intended write areas on the claims board attributed to session:<id>, respecting peer claims (declaration, not seize)." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: deregister — release-on-exit

`deregister` releases the session's claims and removes its presence file (design decision #3). The crash path is already covered by the dead-PID sweep (Task 2) plus the claims board's 2 h TTL.

**Files:**
- Modify: `scripts/git_policy/agent_presence.py` (add `deregister`)
- Modify: `tests/git_policy/test_presence.py` (append `DeregisterTests`)

**Interfaces:**
- Consumes: `agent_claims.release_by_who`, `who_key`, `presence_file`.
- Produces: `deregister(session_id=None) -> int`.

- [ ] **Step 1: Write the failing test.**

Append to `tests/git_policy/test_presence.py`:

```python
class DeregisterTests(PresenceTestBase):
    def test_deregister_removes_presence_and_releases_claims(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        agent_presence.announce("sid-1", "work", ["x.md", "y.md"])
        agent_presence.deregister("sid-1")
        self.assertIsNone(agent_claims.load(
            agent_presence.presence_file("sid-1")))
        self.assertEqual(
            agent_claims.claims_for_who(agent_presence.who_key("sid-1")), [])

    def test_deregister_unknown_session_is_noop(self):
        import agent_presence
        self.assertEqual(agent_presence.deregister("ghost"), 0)
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py DeregisterTests -v`
Expected: FAIL with `AttributeError: ... 'deregister'`.

- [ ] **Step 3: Implement `deregister`.**

Add to `scripts/git_policy/agent_presence.py` (after `announce`):

```python
def deregister(session_id=None):
    session_id = _safe_session_id(session_id) or _session_from_env()
    if session_id is None:
        return 0
    agent_claims.release_by_who(who_key(session_id))
    path = presence_file(session_id)
    if path:
        try:
            os.remove(path)
        except OSError:
            pass
    return 0
```

- [ ] **Step 4: Run the test to verify it passes.**

Run: `python3 tests/git_policy/test_presence.py DeregisterTests -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/git_policy/agent_presence.py tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_presence.py:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): add presence deregister for release-on-exit" \
  -m "deregister releases the session's claims via release_by_who and removes its presence file; the dead-pid sweep plus 2h TTL remain the crash backstop." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: CLI `main` + `agent-presence` shim

Wire the five subcommands and the bash shim, resolving identity from `CLAUDE_CODE_SESSION_ID` with a non-blocking stdin fallback. This is the surface the hooks and the agent call.

**Files:**
- Modify: `scripts/git_policy/agent_presence.py` (add `_parse_announce`, `main`, `__main__`)
- Create: `scripts/agent-presence`
- Modify: `tests/git_policy/test_presence.py` (append `CliTests` — subprocess-driven)

**Interfaces:**
- Produces: CLI `agent-presence {register|deregister|announce "<summary>" [--areas a,b] [--session id]|list|heartbeat [sid]}`, always exit 0.

- [ ] **Step 1: Write the failing test.**

Append to `tests/git_policy/test_presence.py`:

```python
PRESENCE = GIT_POLICY / "agent_presence.py"
AGENT_PRESENCE = ROOT / "scripts" / "agent-presence"


def run_iso(args, cwd, stdin=None, env=None):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if env:
        merged.update(env)
    return subprocess.run(args, cwd=str(cwd), input=stdin, text=True,
                          capture_output=True, env=merged, check=False)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def cli(self, *args, env=None, stdin=None):
        return run_iso([sys.executable, str(PRESENCE), *args],
                       self.repo, stdin=stdin, env=env)

    def test_register_then_list_via_env(self):
        self.cli("register", env={"CLAUDE_CODE_SESSION_ID": "peer1"})
        out = self.cli("list", env={"CLAUDE_CODE_SESSION_ID": "me"})
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("[peer", out.stdout)

    def test_announce_declares_areas(self):
        self.cli("announce", "do the thing", "--areas", "a.md,b.md",
                 env={"CLAUDE_CODE_SESSION_ID": "me"})
        claims_out = run_iso(
            [sys.executable, str(GIT_POLICY / "agent_claims.py"), "list"],
            self.repo)
        self.assertIn("a.md", claims_out.stdout)
        self.assertIn("b.md", claims_out.stdout)

    def test_unknown_and_noenv_exit_zero(self):
        self.assertEqual(self.cli("bogus").returncode, 0)
        # No env, stdin is /dev/null (not a tty) -> silent, no hang.
        self.assertEqual(self.cli("register", stdin="").returncode, 0)

    def test_shim_runs(self):
        out = run_iso(["bash", str(AGENT_PRESENCE), "list"],
                      self.repo, env={"CLAUDE_CODE_SESSION_ID": "me"})
        self.assertEqual(out.returncode, 0, out.stderr)
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py CliTests -v`
Expected: FAIL — `main` returns the usage path / shim file missing.

- [ ] **Step 3: Add `main`, the parser, and `__main__`.**

Append to `scripts/git_policy/agent_presence.py`:

```python
def _parse_announce(args):
    summary_parts, areas, session = [], [], None
    i = 0
    while i < len(args):
        tok = args[i]
        if tok == "--areas":
            i += 1
            if i < len(args):
                areas = [a for a in args[i].split(",") if a.strip()]
        elif tok == "--session":
            i += 1
            if i < len(args):
                session = args[i]
        else:
            summary_parts.append(tok)
        i += 1
    return " ".join(summary_parts), areas, session


def main(argv):
    if not argv:
        print("usage: agent_presence.py "
              "{register|deregister|announce|list|heartbeat} ...", file=sys.stderr)
        return 0
    command, rest = argv[0], argv[1:]
    try:
        if command == "register":
            roster = register(_session_from_env() or _session_from_stdin())
            if roster:
                print(roster)
            return 0
        if command == "deregister":
            deregister(_session_from_env() or _session_from_stdin())
            return 0
        if command == "list":
            print(list_roster())
            return 0
        if command == "heartbeat":
            heartbeat(rest[0] if rest else _session_from_env())
            return 0
        if command == "announce":
            summary, areas, session = _parse_announce(rest)
            roster = announce(session or _session_from_env(), summary, areas)
            if roster:
                print(roster)
            return 0
    except Exception:
        return 0   # advisory: never fail a hook or the agent's shell
    print(f"unknown command: {command}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Create the shim.**

Create `scripts/agent-presence`:

```bash
#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
exec python3 "$repo_root/scripts/git_policy/agent_presence.py" "$@"
```

- [ ] **Step 5: Make the shim executable, run the test to verify it passes.**

Run: `chmod +x scripts/agent-presence && python3 tests/git_policy/test_presence.py CliTests -v`
Expected: PASS (4 tests).

- [ ] **Step 6: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/git_policy/agent_presence.py scripts/agent-presence tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_presence.py:scripts/agent-presence:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): add agent-presence CLI and shim" \
  -m "Wire register/deregister/announce/list/heartbeat with CLAUDE_CODE_SESSION_ID identity and a non-blocking stdin fallback; add the agent-presence bash shim mirroring agent-claim." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: claim_guard heartbeat integration (PreToolUse wiring)

Make every edit bump the session's heartbeat, via one in-process call inside the existing claim guard. It must remain fail-open and must not change the existing auto-declare behavior. (Cost note: `heartbeat` resolves the presence dir via `git rev-parse`, so it is one cheap subprocess per edit, not literally zero as the design's "not a fork" wording implies — still well under the hook budget and fail-open.)

**Files:**
- Modify: `scripts/git_policy/claim_guard.py`
- Modify: `tests/git_policy/test_presence.py` (append `GuardHeartbeatTests`)

**Interfaces:**
- Consumes: `agent_presence.heartbeat`.
- Produces: no new symbol; `claim_guard` now bumps `last_heartbeat` for the payload session when a presence file exists.

- [ ] **Step 1: Write the failing test.**

Append to `tests/git_policy/test_presence.py`:

```python
CLAIM_GUARD = GIT_POLICY / "claim_guard.py"


def guard(cwd, file_path, session, env=None):
    payload = json.dumps({"session_id": session,
                          "tool_input": {"file_path": file_path}})
    return run_iso([sys.executable, str(CLAIM_GUARD)], cwd, stdin=payload, env=env)


class GuardHeartbeatTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_edit_bumps_heartbeat_when_registered(self):
        run_iso([sys.executable, str(PRESENCE), "register"], self.repo,
                env={"CLAUDE_CODE_SESSION_ID": "sess-A"})
        pf = self.repo / ".git" / "agent-presence" / "sess-A.json"
        before = json.loads(pf.read_text())
        before["last_heartbeat"] = 0
        pf.write_text(json.dumps(before))
        result = guard(self.repo, "sim/foo.py", "sess-A")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreater(json.loads(pf.read_text())["last_heartbeat"], 0)

    def test_edit_without_presence_still_exits_zero(self):
        result = guard(self.repo, "sim/foo.py", "sess-Z")
        self.assertEqual(result.returncode, 0, result.stderr)
        # heartbeat no-op left no presence file behind
        self.assertFalse(
            (self.repo / ".git" / "agent-presence" / "sess-Z.json").exists())
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py GuardHeartbeatTests -v`
Expected: FAIL — `test_edit_bumps_heartbeat_when_registered` fails (heartbeat not called).

- [ ] **Step 3: Edit `claim_guard.py`.**

Add the import beside the existing `import agent_claims`:

```python
import agent_claims  # noqa: E402
import agent_presence  # noqa: E402
```

Replace the session block in `main()`:

```python
    session = payload.get("session_id")
    if session:
        os.environ["AGENT_CLAIM_WHO"] = f"session:{session}"
```

with:

```python
    session = payload.get("session_id")
    if session:
        os.environ["AGENT_CLAIM_WHO"] = f"session:{session}"
        try:
            agent_presence.heartbeat(session)
        except Exception:
            pass   # advisory: heartbeat must never block an edit
```

- [ ] **Step 4: Run the test to verify it passes, and confirm no regression.**

Run: `python3 tests/git_policy/test_presence.py GuardHeartbeatTests -v && python3 tests/git_policy/test_concurrency.py -v`
Expected: PASS for both (the existing `ClaimGuardTests` still pass — auto-declare unchanged).

- [ ] **Step 5: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/git_policy/claim_guard.py tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/git_policy/claim_guard.py:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): bump presence heartbeat on every edit" \
  -m "claim_guard calls agent_presence.heartbeat for the payload session in a fail-open try/except, alongside its unchanged auto-declare. No-op when the session has no presence file." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 8: SessionStart wiring (register + roster banner)

Extend the existing SessionStart banner so each session (1) reads its session id from the SessionStart **stdin payload**, (2) **seeds** `CLAUDE_CODE_SESSION_ID` into `CLAUDE_ENV_FILE` so later agent Bash-tool calls (`announce`/`list`) can read it, (3) registers, and (4) prints the roster plus a one-line announce nudge. No `.claude/settings.json` change is needed (the SessionStart hook already runs `session_banner.sh`); the banner now reads stdin, guarded so it never blocks on a tty.

**Files:**
- Modify: `scripts/session_banner.sh`
- Modify: `tests/git_policy/test_presence.py` (append `BannerRegisterTests`)

**Interfaces:**
- Consumes: `agent-presence register`.
- Produces: SessionStart seeds `CLAUDE_CODE_SESSION_ID` (via `CLAUDE_ENV_FILE`) for later tool calls, registers a presence file when a session id is resolvable (payload or env), and prints the worktree/branch line, the roster, and an announce nudge.

- [ ] **Step 1: Write the failing test.**

Append to `tests/git_policy/test_presence.py`:

```python
SESSION_BANNER = ROOT / "scripts" / "session_banner.sh"


class BannerRegisterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        (self.repo / "f").write_text("x\n")
        git(self.repo, "add", "f")
        git(self.repo, "commit", "-q", "-m", "init")

    def test_banner_registers_via_payload_and_seeds_env_file(self):
        env_file = self.repo / "claude_env"
        payload = json.dumps({"session_id": "sess-banner",
                              "hook_event_name": "SessionStart"})
        result = run_iso(["bash", str(SESSION_BANNER)], self.repo, stdin=payload,
                         env={"CLAUDE_ENV_FILE": str(env_file)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"worktree \S+ -> branch \S+")
        self.assertTrue(
            (self.repo / ".git" / "agent-presence" / "sess-banner.json").exists())
        self.assertIn("CLAUDE_CODE_SESSION_ID=sess-banner", env_file.read_text())

    def test_banner_registers_via_env_when_no_payload(self):
        result = run_iso(["bash", str(SESSION_BANNER)], self.repo, stdin="",
                         env={"CLAUDE_CODE_SESSION_ID": "sess-env"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            (self.repo / ".git" / "agent-presence" / "sess-env.json").exists())

    def test_banner_silent_without_session_id(self):
        result = run_iso(["bash", str(SESSION_BANNER)], self.repo, stdin="")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"worktree \S+ -> branch \S+")
        # No identity -> no presence dir entries created
        pdir = self.repo / ".git" / "agent-presence"
        self.assertTrue(not pdir.exists() or not any(pdir.iterdir()))
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tests/git_policy/test_presence.py BannerRegisterTests -v`
Expected: FAIL — `test_banner_registers_via_payload_and_seeds_env_file` fails (banner does not yet read the payload, seed the env file, or register).

- [ ] **Step 3: Edit `scripts/session_banner.sh`.**

Replace the final `exit 0` with the identity-seeding + register block followed by `exit 0`:

```bash
echo "worktree $(basename "$root") -> branch ${branch}  ($root)"

# Advisory presence. Identity is the Claude session id, which arrives on the
# SessionStart hook payload (stdin). Read it (guarded so we never block on a
# tty), seed CLAUDE_CODE_SESSION_ID into CLAUDE_ENV_FILE so later agent
# Bash-tool calls (announce/list) can read it, then register for this call.
# Everything here is advisory; failures are ignored.
sid=""
if [ ! -t 0 ]; then
  payload="$(cat 2>/dev/null || true)"
  sid="$(printf '%s' "$payload" | python3 -c 'import sys, json
try:
    print(json.load(sys.stdin).get("session_id", "") or "")
except Exception:
    pass' 2>/dev/null || true)"
fi
if [ -n "$sid" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  printf 'export CLAUDE_CODE_SESSION_ID=%s\n' "$sid" >> "$CLAUDE_ENV_FILE"
fi
CLAUDE_CODE_SESSION_ID="${sid:-${CLAUDE_CODE_SESSION_ID:-}}" \
  python3 "$root/scripts/git_policy/agent_presence.py" register 2>/dev/null || true

# Nudge the agent to announce its task so peers can see intent (the core datum).
echo 'presence: run  scripts/agent-presence announce "<your task>" --areas <paths>  so peers can see your work.'

exit 0
```

- [ ] **Step 4: Run the test to verify it passes, confirm no regression.**

Run: `python3 tests/git_policy/test_presence.py BannerRegisterTests -v && python3 tests/git_policy/test_concurrency.py SessionBannerTests -v`
Expected: PASS for both (the existing `SessionBannerTests` regex still matches the unchanged first line).

- [ ] **Step 5: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add scripts/session_banner.sh tests/git_policy/test_presence.py
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="scripts/session_banner.sh:tests/git_policy/test_presence.py" \
scripts/agent-commit -m "feat(governance): register presence and print roster at SessionStart" \
  -m "session_banner.sh runs agent-presence register after the worktree/branch line; identity from CLAUDE_CODE_SESSION_ID, silent when absent, never blocks." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 9: Stop wiring (deregister) — isolated and concurrency-guarded

Add a Stop hook so a clean session end releases claims and removes its presence file. This is the **one** task that edits `.claude/settings.json`, a file another session may hold uncommitted. It is correctness-non-critical (the dead-PID sweep + 2 h TTL already clean up); sequence it last and guard it.

**Files:**
- Modify: `.claude/settings.json`

**Interfaces:**
- Consumes: `agent-presence deregister`.
- Produces: Stop event runs `deregister` for `CLAUDE_CODE_SESSION_ID`.

- [ ] **Step 0: Resolve any pre-existing modification first.**

`.claude/settings.json` may already be modified in the working tree (it is, in the repo state this plan was written against). A bulk edit must not fold an unrelated change into this commit. If `git status --short .claude/settings.json` is non-empty, first commit or stash that pre-existing change as its own unit (with user confirmation), or have the user confirm it is yours to include. Only then continue.

- [ ] **Step 1: Concurrency guard — check for a foreign in-flight edit.**

`git status` cannot tell "a live peer is mid-edit" from "benign local dirt", so use the claims board (the mechanism this very system provides) as the ownership signal, with `git status` only as a secondary smell test:

Run: `python3 "$(git rev-parse --show-toplevel)/scripts/git_policy/agent_claims.py" check .claude/settings.json`
- Exit code 3 (a **foreign** session holds a claim) → **STOP** and surface to the user; do not clobber a peer's in-flight edit.
- Exit 0 (no foreign claim) → proceed. The commit-time owned-paths net (`GIT_AGENT_OWNED_PATHS=.claude/settings.json`, Step 5) remains the hard backstop if a peer races in after this check.

> Note: this task edits a shared file and is **correctness-non-critical** (the dead-pid sweep + 2 h TTL already clean up). If you are shipping the MVP slice, it is safe to defer Task 9 entirely.

- [ ] **Step 2: Add the Stop hook.**

In `.claude/settings.json`, add a `"Stop"` array as a sibling of `"PreToolUse"` and `"SessionStart"` inside `"hooks"` (additive — do not alter the existing entries):

```json
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/scripts/git_policy/agent_presence.py\" deregister",
            "timeout": 10
          }
        ]
      }
    ]
```

- [ ] **Step 3: Validate JSON and the wiring.**

Run: `python3 -c "import json; json.load(open('.claude/settings.json')); print('settings.json OK')"`
Expected: `settings.json OK`.

- [ ] **Step 4: Confirm Probe 4 (manual).** End a throwaway session (or trigger Stop) and confirm the session's presence file disappears and its claims are released. If Stop does not fire in this environment, record it — the dead-PID sweep still reaps the session, so no code change is required, but note the limitation.

- [ ] **Step 5: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add .claude/settings.json
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS=".claude/settings.json" \
scripts/agent-commit -m "feat(governance): deregister presence on Stop" \
  -m "Add a Stop hook running agent-presence deregister so a clean session end releases its claims and removes its presence file; the dead-pid sweep and 2h TTL remain the crash backstop." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 10: Operating contract — the agent-facing semantic layer

Document the judgment layer (taxonomy, graduated-autonomy protocol, cross-worktree weighting, subagent rule, the announce-after-first-prompt habit) where agents will read it. This is the *only* part of the system that is not enforced by code — it is the contract every starting agent follows.

**Files:**
- Modify: `docs/git-guidelines.md` (append a top-level section)

**Interfaces:** none (documentation).

- [ ] **Step 1: Append the operating-contract section to `docs/git-guidelines.md`.**

Add at the end of the file:

```markdown
## Presence & overlap awareness (advisory)

At session start you are shown a **roster** of other live sessions: each peer's
short id, worktree/branch, one-line task summary, derived write set, and
heartbeat age. After your first prompt, announce your own task so peers can see
it:

    scripts/agent-presence announce "<one-line task summary>" --areas path/a,path/b

`--areas` is your **intended write set** as explicit paths (never inferred from
the summary). Announcing declares those areas on the claims board; it respects
peers' existing claims and never seizes them. Read-only files need no area.

**Before working, classify overlap with live peers and resolve it yourself where you can. Escalating to a human is the fallback for genuine deadlock, not the default — if you can resolve it autonomously, do.**

- **HIGH — proceed autonomously.** Disjoint work, or a conflict you can dissolve
  yourself: narrow your own write set to dodge a peer's claimed areas, then go. No
  human, no waiting.
- **MEDIUM — self-mitigate, then proceed.** A real but workable interaction (you
  both touch one file in sequence, or your scopes are related). *Act on a
  mitigation yourself* — sequence your edits after the peer's, re-scope to a
  disjoint slice, or take a non-overlapping portion — and record what you did in
  your `announce` summary so the roster reflects it. There is no synchronous peer
  to "acknowledge"; do not idle waiting for one. Surface to a human only if no
  self-mitigation exists.
- **LOW — stand down autonomously; surface only if unresolved.** This is likely
  the *same task* as a live peer (S1). Do **not** proceed on the overlapping work.
  Prefer an autonomous resolution: defer to the peer and pick up the next
  unclaimed task, or re-scope to clearly different work. Surface to a human
  **only** when you cannot resolve it yourself — e.g. both efforts look canonical
  and choosing which proceeds is a priority call you don't own.

Two axes drive the call — **write-overlap** and **semantic relationship**.
Compute write-overlap against the live board, but **run the check under your own
session identity** so your own announced areas aren't mistaken for a peer's
(`agent_claims.find_conflict` excludes only the *caller's* `who`; a plain shell
resolves a different `who`, so it would flag your own claims):

    AGENT_CLAIM_WHO="session:$CLAUDE_CODE_SESSION_ID" python3 scripts/git_policy/agent_claims.py check <path>

The roster above already excludes your session, so it is the primary surface;
use `check` only for an authoritative per-path verdict. Mapping the two axes:

| Planned writes vs. live peers | Unrelated | Related (S2) | Same task (S1) |
|---|---|---|---|
| No write-overlap | proceed | MEDIUM — self-mitigate (re-scope), then proceed | LOW — stand down / re-scope; surface only if unresolved |
| Write-overlap | MEDIUM — sequence yourself (Class B) | MEDIUM → LOW — sequence or re-scope; surface only if stuck | LOW — stand down / re-scope; surface only if unresolved |

Conflict classes: **A1/A2** same-file contention (handled by the claim guard +
commit-time net); **B** shared-file-in-sequence; **C** branch/worktree
structural; **D** read-only sharing (always proceed); **S1** task duplication
(same task, possibly different files — the case this system exists to catch);
**S2** scope overlap (related tasks that may interfere).

**Conservative tie-breaks:** if you cannot *confidently* place a situation in
the proceed cell, treat it as at least MEDIUM (self-mitigate before proceeding).
**Any** whiff of S1 → treat as LOW and **stand down from the duplicate work**,
regardless of file overlap — duplicated effort is the failure to prevent.
Standing down means redirecting yourself to other useful work, not halting for a
human; escalate only when you cannot find a safe autonomous path.

**Cross-worktree weighting:** peers in other worktrees stay visible but marked.
Same-worktree/same-branch peers carry the highest weight for *file-collision*
risk; *semantic duplication* (S1/S2) is weighted across **all** peers, including
cross-worktree ones.

**Subagents:** the unit of presence is the top-level session. Agent-tool
subagents do not register, announce, or appear in the roster.

This layer is **advisory**. No verdict here blocks an edit or a commit; the
commit-time owned-paths net in `scripts/agent-commit` is the only hard backstop.
```

- [ ] **Step 2: Verify the doc renders and links resolve.**

Run: `python3 -c "p=open('docs/git-guidelines.md').read(); assert 'Presence & overlap awareness' in p; print('section present')"`
Expected: `section present`.

- [ ] **Step 3: Commit.**

```bash
cd <home>/Desktop/3_body_problem
git -C "$(git rev-parse --show-toplevel)" add docs/git-guidelines.md
GIT_AGENT_ID="claude-code/claude-opus-4-8" \
GIT_AGENT_OWNED_PATHS="docs/git-guidelines.md" \
scripts/agent-commit -m "docs(governance): document presence and overlap operating contract" \
  -m "Add the agent-facing semantic layer to git-guidelines: announce habit, S1/S2 taxonomy, the graduated-autonomy 2x3 matrix, conservative tie-breaks, cross-worktree weighting, and the subagent rule." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Final validation

- [ ] **Run the full presence suite and the existing concurrency suite together:**

Run: `python3 tests/git_policy/test_presence.py -v && python3 tests/git_policy/test_concurrency.py -v && python3 tests/git_policy/test_git_policy.py -v`
Expected: all PASS — the new module is covered and the claim_guard / banner edits did not regress the existing parallel-agent tooling.

- [ ] **Smoke-test the live surface (in the real repo, from master root):**

Run: `scripts/agent-presence list` then `scripts/agent-presence announce "smoke test" --areas tmp/scratch.txt` then `scripts/agent-presence list`
Expected: the second `list` shows no error; the announce created a `session:<id>` claim for `tmp/scratch.txt` visible via `python3 scripts/git_policy/agent_claims.py list`. Release it afterward: `python3 scripts/git_policy/agent_claims.py release tmp/scratch.txt`.

---

## Self-review — spec coverage map

| Spec section | Task(s) |
|---|---|
| Two-layer architecture (mechanical + semantic) | T1–T9 (mechanical), T10 (semantic) |
| Presence registry: location / identity / schema / atomicity | T2 |
| `claimed_areas` derived, not persisted (decision #4) | T1 (`claims_for_who`) + T3 (roster) |
| Liveness & reaping table (decision #1) | T2 (`sweep_presence` keeps trusted-live pids; absent/dead/untrusted pids → heartbeat floor; `_pid_alive`) |
| announce sets summary + declares write set | T4 |
| claim_guard heartbeat on edit | T7 |
| Deregister = release-on-exit / expire-on-crash (decision #3) | T5 + T2 (dead-pid reap) + 2 h TTL |
| Conflict taxonomy A1/A2/B/C/D/S1/S2 | T10 |
| Graduated-autonomy protocol + 2×3 matrix + tie-breaks | T10 |
| CLI surface (announce/list/register/deregister/heartbeat) | T6 (+ funcs in T2–T5) |
| Hook wiring SessionStart / PreToolUse / Stop | T8 / T7 / T9 |
| Subagents (unit = top-level session) | T10 + Probe 3 (T0); heartbeat no-op safety |
| Roster format | T3 (`_format_line`) |
| Cross-worktree visibility & weighting (decision #2) | T3 (`_format_line` marks cross-worktree peers) + T10 (weighting — **RESOLVED 2026-06-26, user-confirmed**) |
| Pre-build verification gate | T0 |
| Failure modes / hard backstop | fail-open in every function + T10 note |

Every spec section is mapped (deltas noted inline: cross-worktree weighting was RESOLVED 2026-06-26 by user confirmation; reaping uses the untrusted-pid→floor refinement). No task references a symbol defined only in a later task (T1 helpers precede their T3/T5 consumers; T2 primitives precede T3–T6; `register`'s forward call to `list_roster` is covered by the explicit stub-then-delete note in T2/T3).

## Execution handoff

After the user approves this plan, choose an execution path:

1. **Subagent-Driven (recommended)** — a fresh subagent per task with two-stage review between tasks (REQUIRED SUB-SKILL: `superpowers:subagent-driven-development`).
2. **Inline Execution** — batch execution in this session with checkpoints (REQUIRED SUB-SKILL: `superpowers:executing-plans`).

Either way: **Task 0 (Probe 1a) must pass before Task 1**, and all work runs on `master` from the master-root worktree with **no push**.

---

## Post-execution review (2026-06-26)

Reviewed after execution by driving the live CLI and hooks at runtime (not just the
test suite): `agent-presence list` against the live board, plus
register / announce / heartbeat-on-edit / deregister / sweep exercised through the
real module and the real `claim_guard.py` and `session_banner.sh` against an isolated
temp repo. The presence suite passes 28/28; the pre-existing `test_concurrency.py` (12)
and `test_git_policy.py` (27) suites still pass — the shared-file edits to `claim_guard.py`
and `session_banner.sh` did not regress existing tooling.

**Decision #2 (cross-worktree weighting):** the plan's confirm-before-Task-10 gate was
not recorded at execution time, so the weighting shipped into `docs/git-guidelines.md`
unconfirmed. The user confirmed it on 2026-06-26 during this review; it is now settled
and the OPEN markers above are reconciled to RESOLVED. The agent-facing guidance in
`docs/git-guidelines.md` was already written as settled and needs no change.

**Reviewer note (good deviation):** the executor correctly extended the plan's prescribed
`CliTests`/`BannerRegisterTests` by copying the scripts into each temp repo (the shim and
banner resolve the module via `$root/scripts/git_policy/…`, which a bare temp repo lacks),
so those tests genuinely exercise the module.

**Not changed:** task-step checkboxes were left unticked (execution is verified by the
runtime review and git history, not the checkboxes); committed history (Task 2–3 commit
granularity, the separate `claude-mem` settings commit) was left intact rather than
rewritten.
