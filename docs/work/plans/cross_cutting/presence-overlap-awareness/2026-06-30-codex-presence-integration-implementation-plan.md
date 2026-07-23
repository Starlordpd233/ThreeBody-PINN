---
status: consumed
purpose: implementation-plan
created: 2026-06-30
milestone: untracked
phase: cross-cutting
retirement_trigger: When Codex presence integration is implemented — the seven core tasks (T1-T6, T8) committed on master, the seven success criteria pass, and Task 7 either committed or explicitly skipped per its decision point — and this plan is consumed by execution. (Task 7 is flagged optional; the retirement trigger must fire on the documented skip path, not only when all eight commit.)
execution_status: first-pass-complete
executed_at: 2026-07-22 06:45 PDT
review_status: reviewed
---

# Codex Presence Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Codex CLI sessions first-class peers in the existing Claude-Code presence/overlap-awareness system — on the roster, auto-claiming write areas on `apply_patch`, and visible to peers — with zero per-**worktree** manual setup.

> **Scope of "zero setup" (honesty note):** "Zero setup" means per-worktree, not per-machine. A one-time per-machine cost remains: after running the installer (Task 5), Codex prompts **once per machine** to trust each new global hook entry (SessionStart, PreToolUse, PostToolUse, Stop). The prompt recurs on every new machine, fresh clone, or `~/.codex` wipe. There is no `requirements.toml` by-policy mechanism in this repo to silence it automatically (P4 was cut). This is accepted, not hidden.

**Architecture:** Reuse the existing master-owned presence core (`agent_presence.py`, `agent_claims.py`, `presence_hook.sh`) unchanged in spirit; add three Codex-specific adapters (a patch-body claim guard, a heartbeat+announce-flush PostToolUse hook, and a sandboxed announce shim) plus a 3-line identity-resolver edit. Wire them through the **global** `~/.codex/hooks.json` (trusted once per machine, fires in every worktree) using guarded commands that resolve this repo at runtime and no-op cleanly elsewhere.

**Tech Stack:** Python 3 (stdlib only), Bash, Codex hooks JSON schema (Pascal-case events), git worktrees + git common-dir resolution, `unittest`/`pytest` mirroring `tests/git_policy/`.

## Provenance & grounding (read before executing)

This plan supersedes parts of the source design after a 2026-06-28/29 probe session. The design doc is **not** edited (deliverable is plan-only); the deltas below are authoritative where they disagree with it.

**Source design:** `docs/work/designs/cross_cutting/presence-overlap-awareness/2026-06-28-codex-presence-integration-design.md`.

**Confirmed by the probe (`probe.log`, real Codex session `019f13c1-…`):**
- `apply_patch` → `tool_name == "apply_patch"`, `tool_input.command` = raw patch body; markers `*** Add File:`, `*** Update File:`, `*** Delete File:`, `*** Move to:`; a rename emits **both** `Update File:` (old) and `Move to:` (new). Patch paths are **cwd-relative** (`probe.txt`, `renamed.txt`) — resolved against payload `cwd`. (V2 resolved.)
- PostToolUse fires on `apply_patch` **and** `Bash` → catch-all `.*` heartbeat is valid. (F5 extended.)
- SessionStart and Stop deliver the payload on **stdin** (`stdin=True`, `session_id` present) → `presence_hook.sh` / `_session_from_stdin()` resolve identity. Stop fired **twice** → deregister + staging-delete must be idempotent. (V3 resolved.)
- `$TMPDIR` is a single consistent value and the **unsandboxed hook can read** staging files written by the sandboxed model shell (`aps-probe.88888` visible) → the workspace-relative fallback is **not needed**. (V4 resolved.)
- One `session_id` (a hyphenated UUID, passes `_SAFE_SID`) across every event. (F1/V5 at hook level.)
- The nested `$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")` substitution executes inside a Codex hook command (`probe-nested.log`: `NESTED_ESCAPE_OK`). (V7 resolved.)

**Verified live (this machine, 2026-06-30):**
- Codex keys hook trust by **absolute source-file path** in `~/.codex/config.toml [hooks.state]`, keyed per `<filepath>:<event>:<group_idx>:<hook_idx>` with a `trusted_hash`. Only `…/3_body_problem/.codex/hooks.json:pre_tool_use:0:0` (master) is trusted; **specwork and trainex have no trust entries** despite all three `.codex/hooks.json` being byte-identical (`a0fe1c39…`). The existing Git-policy guard is therefore **not firing in specwork/trainex right now** — a lost *early warning*, not a data-integrity hole (the commit-time owned-paths net still backstops both worktrees). Addressed optionally by Task 7.
- Global `~/.codex/hooks.json` entries **are** trusted and already carry other tools' hooks (claude-mem, context-mode, gsd) — the installer must **merge**, never overwrite. **Verified shape (2026-06-30):** the existing gsd `SessionStart`/`Stop`/`PostToolUse` groups carry **no `matcher` field and no `statusMessage`**; trusted indices today are `session_start:0:0`, `post_tool_use:0:0`, `subagent_start:0:0` (there is **no `pre_tool_use` trust entry** yet — adding one is part of this work). Codex's global-file trust is path-keyed, so once trusted it fires in every project.
- `requirements.toml` does **not** exist in the repo.

**Deltas from the source design (this plan diverges deliberately):**
1. **F-A is already done** — `scripts/agent-presence` on master already resolves `repo_root` via `git rev-parse --path-format=absolute --git-common-dir`. → Task 8 verifies it; no re-implementation.
2. **P4 is cut** — `requirements.toml` managed-hooks is not a confirmed Codex mechanism and was collapsed by the probe. Trust is delivered by **global install** (user decision 2026-06-30), not managed hooks.
3. **Hook wiring is global, not project-local** — hooks go in `~/.codex/hooks.json` via an idempotent installer, not the repo's `.codex/hooks.json`. Every command is **guarded** to no-op outside this repo (new requirement: global hooks fire machine-wide).
4. **`codex_claim_guard.py` resolves paths against payload `cwd`** (Codex paths are relative), a real divergence from `claim_guard.py` (which abspath's against the process cwd).
5. **P2 uses `$TMPDIR` staging only** — no workspace-relative fallback (V4 clean).

## Global Constraints

- **Master-owned.** Every new/edited file is created and committed on `master`. The presence layer lives only on `master`; linked worktrees reach it via the git common-dir. Do not commit these on `milestone/v1.6` or `track/trainex`.
- **Advisory / fail-open.** Every hook and shim exits `0` unconditionally and never blocks an edit, a shell, or session start/stop. The only hard guarantee against silent overwrite is the commit-time owned-paths net in `scripts/agent-commit` — unchanged by this work.
- **Identity join key is the exact string `session:<session_id>`** everywhere: `codex_claim_guard.py`, `codex_presence_flush.py`, and `agent_presence.who_key()`. The model-side announce shim keys staging by `CODEX_THREAD_ID`, which equals the hook payload `session_id` (F1). If these strings ever diverge, one session fragments into two roster entries — locked by tests in Tasks 1 and 4.
- **Staging contract (shared by Task 3 and Task 4), computed identically on both sides:**
  - Directory: `${TMPDIR:-/tmp}/agent-presence-staging`
  - File: `<staging-dir>/<session_id>.json`
  - Body: `{"session_id": "<id>", "summary": "<text>", "areas": ["<path>", …]}`
  - Existence == "not yet flushed"; the flush hook deletes on consume (re-flush is harmless).
- **Guarded global command template** (used for all four hook entries; `<REL>` is repo-relative, `<ARGS>` optional):
  ```
  sh -c 'r="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" || exit 0; p="$(dirname "$r")"; s="$p/<REL>"; [ -f "$s" ] || exit 0; exec "$s" <ARGS>'
  ```
  For Python targets the final clause is `exec python3 "$s"`. `exec` preserves the hook payload on stdin. `git rev-parse … || exit 0` covers "not in a repo"; `[ -f "$s" ] || exit 0` covers "a different repo without our scripts".
- **Commits** use `scripts/agent-commit` (never raw `git commit`), staging explicit owned paths only:
  ```
  GIT_AGENT_ID="<id>" GIT_AGENT_OWNED_PATHS="<path1>:<path2>" \
    scripts/agent-commit -m "<type>(governance): <subject>" -m "<body>" -m "Agent-Assisted-By: Claude Opus 4.8"
  ```
  Conventional types: `feat`/`test`/`fix`/`docs`/`chore`; scope `governance`; body required (touches `scripts/`/governance). No `git add .`. Re-check `git status --short --branch` and `git diff --cached` before each commit.
- **Tests** are stdlib `unittest`, mirroring `tests/git_policy/` (subprocess with JSON on stdin; `init_repo()` throwaway repos; `ISOLATED_KEYS` env stripping so the live board is never touched). Run: `python3 -m pytest tests/git_policy/ -q` (or `python3 -m unittest discover -s tests/git_policy -p 'test_*.py'`).

---

## File structure

| File | Action | Task | Responsibility |
|------|--------|------|----------------|
| `scripts/git_policy/agent_presence.py` | Edit | T1 | `_session_from_env()` reads `CODEX_THREAD_ID` first |
| `tests/git_policy/test_codex_identity.py` | Create | T1 | identity-resolver precedence + env-bleed |
| `scripts/git_policy/codex_claim_guard.py` | Create | T2 | apply_patch PreToolUse guard: parse patch body, claim/warn |
| `tests/git_policy/test_codex_claim_guard.py` | Create | T2 | add/update/delete/rename/conflict/cwd-resolution |
| `scripts/git_policy/codex_presence_flush.py` | Create | T3 | PostToolUse: heartbeat-first, flush staging if present |
| `tests/git_policy/test_codex_presence_flush.py` | Create | T3 | heartbeat bump, no-op-without-presence, flush, idempotent |
| `scripts/agent-codex-announce` | Create | T4 | sandboxed shim: stage `{summary,areas}` under `$TMPDIR` |
| `tests/git_policy/test_codex_announce_shim.py` | Create | T4 | staging write + flush round-trip (V5) |
| `scripts/git_policy/install_codex_presence_hooks.py` | Create | T5 | idempotent merge of guarded hook entries into `~/.codex/hooks.json` |
| `tests/git_policy/test_install_codex_presence_hooks.py` | Create | T5 | merge/idempotency/preserve-existing against a temp hooks file |
| `AGENTS.md` | Edit | T6 | F-B announce nudge under "### Concurrent agents" |
| `install_codex_presence_hooks.py`, `test_install_codex_presence_hooks.py`, `.codex/hooks.json` | Edit (T7-FLAGGED) | T7 | git-guard global relocation (FLAGGED — confirm before executing; optionally skipped) |
| (verification only) | — | T8 | 7 success criteria + F-A regression check |

---

### Task 1: Codex identity resolver (P3)

**Files:**
- Modify: `scripts/git_policy/agent_presence.py:71-72` (`_session_from_env`)
- Test: `tests/git_policy/test_codex_identity.py`

**Interfaces:**
- Produces: `agent_presence._session_from_env() -> str | None` — returns a `CODEX_THREAD_ID` (if set and safe), else `CLAUDE_CODE_SESSION_ID`, else `None`. All existing callers (`register`, `announce`, `deregister`, `list_roster`, `heartbeat` CLI) are unchanged.

- [ ] **Step 1: Write the failing test**

```python
# tests/git_policy/test_codex_identity.py
#!/usr/bin/env python3
"""P3: _session_from_env() prefers CODEX_THREAD_ID over CLAUDE_CODE_SESSION_ID."""
import importlib, os, pathlib, sys, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "git_policy"))
import agent_presence  # noqa: E402

KEYS = ("CODEX_THREAD_ID", "CLAUDE_CODE_SESSION_ID")


class SessionFromEnvTests(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in KEYS}
        for k in KEYS:
            os.environ.pop(k, None)
        self.addCleanup(self._restore)
        importlib.reload(agent_presence)

    def _restore(self):
        for k, v in self._saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

    def test_codex_id_wins_when_both_set(self):
        os.environ["CODEX_THREAD_ID"] = "codex-1"
        os.environ["CLAUDE_CODE_SESSION_ID"] = "claude-1"
        self.assertEqual(agent_presence._session_from_env(), "codex-1")

    def test_claude_id_used_when_codex_absent(self):
        os.environ["CLAUDE_CODE_SESSION_ID"] = "claude-1"
        self.assertEqual(agent_presence._session_from_env(), "claude-1")

    def test_uuid_codex_id_passes_safe_filter(self):
        os.environ["CODEX_THREAD_ID"] = "019f13c1-cfbc-7b73-a8b5-9f67d910532b"
        self.assertEqual(agent_presence._session_from_env(),
                         "019f13c1-cfbc-7b73-a8b5-9f67d910532b")

    def test_none_when_neither_set(self):
        self.assertIsNone(agent_presence._session_from_env())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/git_policy/test_codex_identity.py -q`
Expected: FAIL on `test_codex_id_wins_when_both_set` (current code reads only `CLAUDE_CODE_SESSION_ID`).

- [ ] **Step 3: Apply the minimal edit**

Replace `agent_presence.py:71-72`:

```python
def _session_from_env():
    # Codex sets CODEX_THREAD_ID; Claude Code sets CLAUDE_CODE_SESSION_ID. When
    # Codex is launched from within a Claude terminal both may be set, so take
    # CODEX_THREAD_ID first: it is the active session's own identity.
    return (
        _safe_session_id(os.environ.get("CODEX_THREAD_ID"))
        or _safe_session_id(os.environ.get("CLAUDE_CODE_SESSION_ID"))
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/git_policy/test_codex_identity.py tests/git_policy/test_presence.py -q`
Expected: PASS (new file all green; `test_presence.py` unaffected).

- [ ] **Step 5: Commit**

```bash
GIT_AGENT_ID="codex-presence" GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_presence.py:tests/git_policy/test_codex_identity.py" \
  scripts/agent-commit -m "feat(governance): resolve codex session identity in presence" \
  -m "Prefer CODEX_THREAD_ID over CLAUDE_CODE_SESSION_ID in _session_from_env so Codex sessions key presence by their own thread id; guards against Claude env bleed when Codex is launched from a Claude tab." \
  -m "Agent-Assisted-By: Claude Opus 4.8"
```

---

### Task 2: codex_claim_guard.py (P1 — primary safety)

**Files:**
- Create: `scripts/git_policy/codex_claim_guard.py`
- Test: `tests/git_policy/test_codex_claim_guard.py`

**Interfaces:**
- Consumes (stdin): Codex PreToolUse payload `{"session_id","cwd","tool_name":"apply_patch","tool_input":{"command":"<patch body>"}}`.
- Consumes: `agent_claims.find_conflict(area)`, `agent_claims.claim(area, why=…)`, `agent_presence.heartbeat(session)`, `agent_presence.who_key(session)`.
- Produces: claims on the board attributed to `session:<id>`; advisory stderr warnings; always exit `0`.
- Internal: `extract_paths(command:str) -> list[str]` (parses the four markers), `repo_relative(path:str, cwd:str) -> str` (resolve vs `cwd`, then relpath against `git -C cwd rev-parse --show-toplevel`).

- [ ] **Step 1: Write the failing tests**

```python
# tests/git_policy/test_codex_claim_guard.py
#!/usr/bin/env python3
"""P1: codex_claim_guard parses apply_patch bodies and auto-declares write areas."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
GIT_POLICY = ROOT / "scripts" / "git_policy"
GUARD = GIT_POLICY / "codex_claim_guard.py"
CLAIMS = GIT_POLICY / "agent_claims.py"
ISOLATED = ("AGENT_CLAIM_WHO", "AGENT_CLAIM_EXPIRY", "GIT_AGENT_ID", "CODEX_THREAD_ID")


def run(args, cwd, stdin=None):
    env = os.environ.copy()
    for k in ISOLATED:
        env.pop(k, None)
    return subprocess.run(args, cwd=str(cwd), input=stdin, text=True,
                          capture_output=True, env=env, check=False)


def init_repo(path):
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@e.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "T"], check=True)
    return path


def patch(*body_lines):
    return "*** Begin Patch\n" + "\n".join(body_lines) + "\n*** End Patch\n"


def edit(repo, command, session, cwd=None):
    payload = json.dumps({"session_id": session, "cwd": str(cwd or repo),
                          "tool_name": "apply_patch",
                          "tool_input": {"command": command}})
    return run([sys.executable, str(GUARD)], repo, stdin=payload)


def claimed_areas(repo, who):
    # Read the board directly via agent_claims to assert exact areas.
    out = run([sys.executable, "-c",
               f"import sys;sys.path.insert(0,{str(GIT_POLICY)!r});"
               "import agent_claims,os;print('\\n'.join(agent_claims.claims_for_who("
               f"{who!r})))"], repo).stdout
    return sorted(x for x in out.splitlines() if x)


class CodexClaimGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_add_file_is_claimed(self):
        r = edit(self.repo, patch("*** Add File: sim/foo.py", "+x"), "S-A")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sim/foo.py"])

    def test_update_file_is_claimed(self):
        edit(self.repo, patch("*** Update File: sim/foo.py", "@@", "+x"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sim/foo.py"])

    def test_delete_file_is_claimed(self):
        edit(self.repo, patch("*** Delete File: sim/foo.py"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sim/foo.py"])

    def test_rename_claims_both_old_and_new(self):
        edit(self.repo, patch("*** Update File: a.py", "*** Move to: b.py", "@@", "+x"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["a.py", "b.py"])

    def test_multifile_patch_claims_all(self):
        edit(self.repo, patch("*** Add File: a.py", "+1",
                              "*** Update File: sub/b.py", "@@", "+2"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["a.py", "sub/b.py"])

    def test_cwd_relative_path_resolves_repo_relative(self):
        # cwd is a subdir; "foo.py" must resolve to "sub/foo.py" repo-relative.
        sub = self.repo / "sub"
        sub.mkdir()
        edit(self.repo, patch("*** Add File: foo.py", "+x"), "S-A", cwd=sub)
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sub/foo.py"])

    def test_foreign_overlap_warns_and_does_not_block(self):
        edit(self.repo, patch("*** Add File: sim/foo.py", "+x"), "S-A")
        r = edit(self.repo, patch("*** Update File: sim/foo.py", "@@", "+y"), "S-B")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("claim warning", r.stderr)

    def test_garbage_stdin_exits_zero(self):
        self.assertEqual(run([sys.executable, str(GUARD)], self.repo, stdin="nope").returncode, 0)

    def test_non_applypatch_payload_is_noop(self):
        payload = json.dumps({"session_id": "S", "cwd": str(self.repo),
                              "tool_name": "Bash", "tool_input": {"command": "ls"}})
        r = run([sys.executable, str(GUARD)], self.repo, stdin=payload)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(claimed_areas(self.repo, "session:S"), [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/git_policy/test_codex_claim_guard.py -q`
Expected: FAIL — `codex_claim_guard.py` does not exist (ModuleNotFound / file-not-found on every test).

- [ ] **Step 3: Write the implementation**

```python
# scripts/git_policy/codex_claim_guard.py
#!/usr/bin/env python3
"""PreToolUse hook for Codex apply_patch: warn on a foreign claim, else auto-declare.

Mirrors claim_guard.py but parses the apply_patch *patch body* (tool_input.command)
for affected paths instead of reading tool_input.file_path. Codex emits cwd-relative
paths, so each is resolved against the payload's cwd before being made repo-relative.

Advisory only: always exits 0; never blocks an edit. The hard guarantee against
silent overwrite is the commit-time owned-paths net, not this hook.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_claims  # noqa: E402
import agent_presence  # noqa: E402

# "*** Add File: <p>", "*** Update File: <p>", "*** Delete File: <p>", "*** Move to: <p>"
_MARKER = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+?)\s*$")
_MOVE = re.compile(r"^\*\*\* Move to: (.+?)\s*$")


def extract_paths(command):
    paths = []
    for line in (command or "").splitlines():
        m = _MARKER.match(line) or _MOVE.match(line)
        if m:
            paths.append(m.group(1))
    return paths


def repo_relative(path, cwd):
    base = path if os.path.isabs(path) else os.path.join(cwd, path)
    try:
        root = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        return os.path.relpath(os.path.abspath(base), root)
    except Exception:
        return path


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command")
    if not command:
        return 0  # not an apply_patch-shaped payload; nothing to claim
    cwd = payload.get("cwd") or os.getcwd()
    session = payload.get("session_id")
    if session:
        os.environ["AGENT_CLAIM_WHO"] = agent_presence.who_key(session)
        try:
            agent_presence.heartbeat(session)
        except Exception:
            pass  # advisory: heartbeat must never block an edit
    seen = set()
    for raw in extract_paths(command):
        area = repo_relative(raw, cwd)
        if area in seen:
            continue
        seen.add(area)
        try:
            other = agent_claims.find_conflict(area)
            if other is not None:
                print(
                    f"claim warning: '{area}' overlaps a claim held by {other.get('who')} "
                    f"(area: {other.get('area')}, reason: {other.get('why') or 'n/a'}). "
                    f"Coordinate before overlapping.",
                    file=sys.stderr,
                )
            else:
                agent_claims.claim(area, why="auto-declared on edit")
        except Exception:
            return 0  # fail open: advisory must never block
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Then make it executable: `chmod +x scripts/git_policy/codex_claim_guard.py`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/git_policy/test_codex_claim_guard.py -q`
Expected: PASS (all cases, including rename-claims-both and cwd-relative resolution).

- [ ] **Step 5: Commit**

```bash
GIT_AGENT_ID="codex-presence" GIT_AGENT_OWNED_PATHS="scripts/git_policy/codex_claim_guard.py:tests/git_policy/test_codex_claim_guard.py" \
  scripts/agent-commit -m "feat(governance): add codex apply_patch claim guard" \
  -m "New PreToolUse hook parses the apply_patch patch body (Add/Update/Delete File, Move to) and auto-declares write areas, resolving Codex's cwd-relative paths against the payload cwd. Renames claim both old and new path. Advisory, fail-open, exit 0." \
  -m "Agent-Assisted-By: Claude Opus 4.8"
```

---

### Task 3: codex_presence_flush.py (P0 heartbeat + P2 flush)

**Files:**
- Create: `scripts/git_policy/codex_presence_flush.py`
- Test: `tests/git_policy/test_codex_presence_flush.py`

**Interfaces:**
- Consumes (stdin): any Codex PostToolUse payload `{"session_id", …}`.
- Consumes: `agent_presence.heartbeat(session)`, `agent_presence.announce(session, summary, areas)`.
- Produces: bumps `last_heartbeat` on every call; applies and deletes a staging file when present; always exit `0`.
- Internal: `staging_file(session) -> str` using the Global-Constraints staging contract.

- [ ] **Step 1: Write the failing tests**

```python
# tests/git_policy/test_codex_presence_flush.py
#!/usr/bin/env python3
"""P0/P2: heartbeat on every PostToolUse; flush a staged announce when present."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
GIT_POLICY = ROOT / "scripts" / "git_policy"
FLUSH = GIT_POLICY / "codex_presence_flush.py"
PRESENCE = GIT_POLICY / "agent_presence.py"
ISOLATED = ("AGENT_CLAIM_WHO", "AGENT_PRESENCE_STALE", "CODEX_THREAD_ID",
            "CLAUDE_CODE_SESSION_ID", "GIT_AGENT_ID")


def run(args, cwd, stdin=None, env=None):
    merged = os.environ.copy()
    for k in ISOLATED:
        merged.pop(k, None)
    if env:
        merged.update(env)
    return subprocess.run(args, cwd=str(cwd), input=stdin, text=True,
                          capture_output=True, env=merged, check=False)


def init_repo(path):
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@e.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "T"], check=True)
    return path


def presence_entry(repo, sid, env):
    out = run([sys.executable, "-c",
               f"import sys;sys.path.insert(0,{str(GIT_POLICY)!r});import agent_presence,"
               f"agent_claims,json;print(json.dumps(agent_claims.load("
               f"agent_presence.presence_file({sid!r}))))"], repo, env=env).stdout.strip()
    return json.loads(out) if out and out != "null" else None


class FlushTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.staging = pathlib.Path(self.tmp.name).resolve() / "stg"
        self.staging.mkdir()
        self.env = {"TMPDIR": str(self.staging.parent)}  # staging dir = $TMPDIR/agent-presence-staging
        self.sdir = self.staging.parent / "agent-presence-staging"

    def _register(self, sid):
        # The CLI `register` ignores argv — main() resolves identity from env/stdin,
        # so `agent-presence register <sid>` drops <sid> and registers nothing. Call
        # the Python API with the explicit sid (mirrors tests/git_policy/test_presence.py).
        # env still carries TMPDIR so the shared presence dir resolves inside the temp repo.
        run([sys.executable, "-c",
             f"import sys;sys.path.insert(0,{str(GIT_POLICY)!r});"
             f"import agent_presence,os;agent_presence.register({sid!r},pid=os.getpid())"],
            self.repo, env=self.env)

    def _flush(self, sid):
        return run([sys.executable, str(FLUSH)], self.repo,
                   stdin=json.dumps({"session_id": sid, "tool_name": "Bash"}), env=self.env)

    def test_heartbeat_bumps_when_registered(self):
        self._register("S1")
        before = presence_entry(self.repo, "S1", self.env)["last_heartbeat"]
        import time
        time.sleep(1)
        self.assertEqual(self._flush("S1").returncode, 0)
        after = presence_entry(self.repo, "S1", self.env)["last_heartbeat"]
        self.assertGreater(after, before)

    def test_noop_when_not_registered(self):
        r = self._flush("ghost")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIsNone(presence_entry(self.repo, "ghost", self.env))

    def test_flush_applies_staged_announce_and_deletes_file(self):
        self._register("S2")
        self.sdir.mkdir(parents=True, exist_ok=True)
        (self.sdir / "S2.json").write_text(json.dumps(
            {"session_id": "S2", "summary": "build the thing", "areas": ["sim/x.py"]}))
        self.assertEqual(self._flush("S2").returncode, 0)
        entry = presence_entry(self.repo, "S2", self.env)
        self.assertEqual(entry["task_summary"], "build the thing")
        self.assertFalse((self.sdir / "S2.json").exists())

    def test_double_flush_is_idempotent(self):
        self._register("S3")
        self.sdir.mkdir(parents=True, exist_ok=True)
        (self.sdir / "S3.json").write_text(json.dumps(
            {"session_id": "S3", "summary": "x", "areas": ["a.py"]}))
        self.assertEqual(self._flush("S3").returncode, 0)
        self.assertEqual(self._flush("S3").returncode, 0)  # Stop fired twice → no error

    def test_garbage_stdin_exits_zero(self):
        self.assertEqual(run([sys.executable, str(FLUSH)], self.repo, stdin="nope",
                             env=self.env).returncode, 0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/git_policy/test_codex_presence_flush.py -q`
Expected: FAIL — `codex_presence_flush.py` does not exist.

- [ ] **Step 3: Write the implementation**

```python
# scripts/git_policy/codex_presence_flush.py
#!/usr/bin/env python3
"""PostToolUse hook for Codex: heartbeat on every call; flush a staged announce.

Runs unsandboxed (Codex sandboxes only model-generated shell, not hooks), so it can
write the shared presence/claims board from any worktree. On every PostToolUse it
bumps the session heartbeat (keeping a live session on the roster through non-edit
work), then applies any announce the model staged via agent-codex-announce.

Advisory only: always exits 0.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_presence  # noqa: E402


def staging_file(session_id):
    base = os.path.join(os.environ.get("TMPDIR", "/tmp"), "agent-presence-staging")
    return os.path.join(base, f"{session_id}.json")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    session = payload.get("session_id")
    if not session:
        return 0
    try:
        agent_presence.heartbeat(session)  # unconditional P0 heartbeat, first
    except Exception:
        pass
    path = staging_file(session)
    try:
        if os.path.exists(path):
            with open(path) as handle:
                staged = json.load(handle)
            agent_presence.announce(
                session, staged.get("summary"), staged.get("areas") or [])
            os.remove(path)  # consume; existence alone marks "not yet flushed"
    except Exception:
        return 0  # advisory: never fail the PostToolUse round-trip
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Then: `chmod +x scripts/git_policy/codex_presence_flush.py`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/git_policy/test_codex_presence_flush.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
GIT_AGENT_ID="codex-presence" GIT_AGENT_OWNED_PATHS="scripts/git_policy/codex_presence_flush.py:tests/git_policy/test_codex_presence_flush.py" \
  scripts/agent-commit -m "feat(governance): add codex presence flush postooluse hook" \
  -m "Heartbeat on every PostToolUse keeps a Codex session on the roster through non-edit work; when the model staged an announce under \$TMPDIR, apply it and delete the staging file. Idempotent (Stop fires twice), advisory, exit 0." \
  -m "Agent-Assisted-By: Claude Opus 4.8"
```

---

### Task 4: agent-codex-announce shim (P2 — proactive announce)

**Files:**
- Create: `scripts/agent-codex-announce`
- Test: `tests/git_policy/test_codex_announce_shim.py`

**Interfaces:**
- CLI: `agent-codex-announce "<summary>" --areas <comma,separated,paths>`; identity from `CODEX_THREAD_ID`.
- Produces: `${TMPDIR:-/tmp}/agent-presence-staging/<CODEX_THREAD_ID>.json` per the staging contract — consumed by `codex_presence_flush.py` (Task 3) on the next (same-call) PostToolUse.
- This closes the V5 round-trip: staging key (`CODEX_THREAD_ID`) == flush read key (payload `session_id`).

- [ ] **Step 1: Write the failing tests**

```python
# tests/git_policy/test_codex_announce_shim.py
#!/usr/bin/env python3
"""P2: announce shim stages summary+areas; flush consumes them (V5 round-trip)."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SHIM = ROOT / "scripts" / "agent-codex-announce"
GIT_POLICY = ROOT / "scripts" / "git_policy"
FLUSH = GIT_POLICY / "codex_presence_flush.py"
PRESENCE = GIT_POLICY / "agent_presence.py"
ISOLATED = ("AGENT_CLAIM_WHO", "CODEX_THREAD_ID", "CLAUDE_CODE_SESSION_ID", "GIT_AGENT_ID")


def run(args, cwd, stdin=None, env=None):
    merged = os.environ.copy()
    for k in ISOLATED:
        merged.pop(k, None)
    if env:
        merged.update(env)
    return subprocess.run(args, cwd=str(cwd), input=stdin, text=True,
                          capture_output=True, env=merged, check=False)


def init_repo(path):
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@e.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "T"], check=True)
    return path


class AnnounceShimTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.tmpdir = pathlib.Path(self.tmp.name).resolve()
        self.env = {"TMPDIR": str(self.tmpdir), "CODEX_THREAD_ID": "S-Z"}
        self.staged = self.tmpdir / "agent-presence-staging" / "S-Z.json"

    def test_shim_writes_staging_payload(self):
        r = run(["bash", str(SHIM), "do the work", "--areas", "sim/a.py,sim/b.py"],
                self.repo, env=self.env)
        self.assertEqual(r.returncode, 0, r.stderr)
        body = json.loads(self.staged.read_text())
        self.assertEqual(body["session_id"], "S-Z")
        self.assertEqual(body["summary"], "do the work")
        self.assertEqual(body["areas"], ["sim/a.py", "sim/b.py"])

    def test_round_trip_announce_then_flush(self):
        # Register via the Python API (the CLI `register` ignores argv — see Task 3).
        run([sys.executable, "-c",
             "import sys;sys.path.insert(0,%r);import agent_presence,os;"
             "agent_presence.register('S-Z',pid=os.getpid())" % str(GIT_POLICY)],
            self.repo, env=self.env)
        run(["bash", str(SHIM), "round trip", "--areas", "sim/a.py"], self.repo, env=self.env)
        run([sys.executable, str(FLUSH)], self.repo,
            stdin=json.dumps({"session_id": "S-Z"}), env=self.env)
        self.assertFalse(self.staged.exists())  # consumed by flush

    def test_missing_thread_id_exits_zero_no_file(self):
        r = run(["bash", str(SHIM), "x", "--areas", "a.py"], self.repo,
                env={"TMPDIR": str(self.tmpdir)})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.staged.exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/git_policy/test_codex_announce_shim.py -q`
Expected: FAIL — `scripts/agent-codex-announce` does not exist.

- [ ] **Step 3: Write the implementation**

```bash
# scripts/agent-codex-announce
#!/usr/bin/env bash
# Sandboxed staging shim: a Codex model-run Bash tool call cannot write the git
# common-dir under seatbelt workspace-write, so it stages its announce under
# $TMPDIR instead. The unsandboxed PostToolUse flush hook (codex_presence_flush.py)
# consumes the file on the same call. Advisory: always exits 0.
#
# Usage: agent-codex-announce "<summary>" --areas <comma,separated,paths>
set -uo pipefail

sid="${CODEX_THREAD_ID:-}"
[ -n "$sid" ] || exit 0  # no identity -> nothing to stage

summary=""
areas=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --areas) shift; areas="${1:-}";;
    *) summary="${summary:+$summary }$1";;
  esac
  shift || true
done

dir="${TMPDIR:-/tmp}/agent-presence-staging"
mkdir -p "$dir" 2>/dev/null || exit 0

# Emit JSON via python3 to avoid quoting/escaping pitfalls; areas split on comma.
SID="$sid" SUMMARY="$summary" AREAS="$areas" python3 - "$dir/$sid.json" <<'PY' 2>/dev/null || exit 0
import json, os, sys
path = sys.argv[1]
areas = [a.strip() for a in os.environ.get("AREAS", "").split(",") if a.strip()]
payload = {"session_id": os.environ["SID"],
           "summary": os.environ.get("SUMMARY", ""),
           "areas": areas}
tmp = path + ".tmp"
with open(tmp, "w") as fh:
    json.dump(payload, fh)
os.replace(tmp, path)
PY

echo "announce staged for session $sid (flushes on next tool call)"
exit 0
```

Then: `chmod +x scripts/agent-codex-announce`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/git_policy/test_codex_announce_shim.py -q`
Expected: PASS (including the announce→flush round-trip).

- [ ] **Step 5: Commit**

```bash
GIT_AGENT_ID="codex-presence" GIT_AGENT_OWNED_PATHS="scripts/agent-codex-announce:tests/git_policy/test_codex_announce_shim.py" \
  scripts/agent-commit -m "feat(governance): add codex announce staging shim" \
  -m "Sandboxed Codex Bash tool calls cannot write the git common-dir, so the announce shim stages summary+areas under \$TMPDIR keyed by CODEX_THREAD_ID; the unsandboxed flush hook consumes it on the same call. Advisory, exit 0." \
  -m "Agent-Assisted-By: Claude Opus 4.8"
```

---

### Task 5: Global hook installer (P0/P1/P2 wiring — replaces design's project-local P4)

**Files:**
- Create: `scripts/git_policy/install_codex_presence_hooks.py`
- Test: `tests/git_policy/test_install_codex_presence_hooks.py`

**Interfaces:**
- CLI: `install_codex_presence_hooks.py [--print]`; target file from `${CODEX_HOOKS_FILE:-$HOME/.codex/hooks.json}` (env override makes it testable).
- Behavior: idempotently merge four guarded hook groups (SessionStart→register, PreToolUse→codex_claim_guard, PostToolUse→codex_presence_flush, Stop→deregister) into the target JSON, **preserving all existing handlers** (claude-mem/context-mode/gsd). Groups are tagged `statusMessage` prefix `aps:` so re-runs replace only our groups. Writes a `.bak` first.

**Why global (user decision 2026-06-30):** project-local `.codex/hooks.json` is trusted per absolute path and is *not* trusted in specwork/trainex today (verified). A global file is trusted once per machine and fires in every worktree; the guarded command resolves this repo at runtime and no-ops elsewhere.

- [ ] **Step 1: Write the failing tests**

```python
# tests/git_policy/test_install_codex_presence_hooks.py
#!/usr/bin/env python3
"""Installer merges guarded presence hooks into ~/.codex/hooks.json idempotently."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "scripts" / "git_policy" / "install_codex_presence_hooks.py"


def run(target, args=()):
    env = os.environ.copy()
    env["CODEX_HOOKS_FILE"] = str(target)
    return subprocess.run([sys.executable, str(INSTALLER), *args],
                          text=True, capture_output=True, env=env, check=False)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = pathlib.Path(self.tmp.name) / ".codex" / "hooks.json"

    def _events(self):
        return json.loads(self.target.read_text())["hooks"]

    def test_creates_file_with_four_events(self):
        self.assertEqual(run(self.target).returncode, 0)
        ev = self._events()
        for name in ("SessionStart", "PreToolUse", "PostToolUse", "Stop"):
            self.assertIn(name, ev)

    def test_commands_are_guarded_and_path_free(self):
        run(self.target)
        blob = self.target.read_text()
        self.assertIn("git rev-parse --path-format=absolute --git-common-dir", blob)
        self.assertIn('[ -f "$s" ] || exit 0', blob)
        self.assertNotIn("/Users/", blob)  # no hardcoded absolute paths

    def test_preserves_existing_foreign_handler(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_text(json.dumps({"hooks": {"PostToolUse": [
            {"matcher": ".*", "hooks": [{"type": "command", "command": "echo claude-mem",
                                         "statusMessage": "claude-mem"}]}]}}))
        run(self.target)
        post = self._events()["PostToolUse"]
        msgs = [h["statusMessage"] for g in post for h in g["hooks"]]
        self.assertIn("claude-mem", msgs)          # foreign handler kept
        self.assertTrue(any(m.startswith("aps:") for m in msgs))  # ours added

    def test_idempotent_no_duplicate_groups(self):
        run(self.target)
        run(self.target)
        post = self._events()["PostToolUse"]
        aps_groups = [g for g in post
                      if any(h.get("statusMessage", "").startswith("aps:") for h in g["hooks"])]
        self.assertEqual(len(aps_groups), 1)

    def test_sessionstart_stop_postooluse_omit_matcher(self):
        # Real Codex global hooks (~/.codex/hooks.json, verified 2026-06-30) carry no
        # matcher for these events. A "startup|resume" value is Claude-Code vocabulary
        # and would never match Codex SessionStart, silently breaking roster registration.
        run(self.target)
        ev = self._events()
        for event in ("SessionStart", "Stop", "PostToolUse"):
            for g in ev[event]:
                self.assertNotIn("matcher", g, f"{event} group must omit matcher")
        # PreToolUse is the only event that must restrict firing, and only to apply_patch.
        self.assertEqual([g.get("matcher") for g in ev["PreToolUse"]], ["apply_patch"])

    def test_pretooluse_narrowed_to_apply_patch(self):
        # Edit/Write are not Codex tool names (probe F4) and codex_claim_guard only
        # parses tool_input.command (apply_patch bodies); the matcher must not advertise
        # broader coverage than the guard can deliver.
        run(self.target)
        blob = self.target.read_text()
        self.assertIn('"apply_patch"', blob)
        self.assertNotIn("Edit|Write", blob)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/git_policy/test_install_codex_presence_hooks.py -q`
Expected: FAIL — installer does not exist.

- [ ] **Step 3: Write the implementation**

```python
# scripts/git_policy/install_codex_presence_hooks.py
#!/usr/bin/env python3
"""Idempotently install guarded Codex presence hooks into the global hooks file.

Target: ${CODEX_HOOKS_FILE:-$HOME/.codex/hooks.json}. Existing handlers from other
tools are preserved; our groups are tagged with a 'aps:' statusMessage prefix and
replaced on re-run. Commands resolve this repo at runtime from the git common-dir
and no-op cleanly in any other repo or outside a repo (global hooks fire machine-wide).
"""
import json
import os
import shutil
import sys

TAG = "aps:"


def guarded(rel, args, status):
    # `s` is the resolved script path; the final clause matches the Global-Constraints
    # guarded-command template verbatim (`exec python3 "$s"` / `exec "$s"`).
    runner = 'exec python3 "$s"' if rel.endswith(".py") else 'exec "$s"'
    cmd = (
        "sh -c '"
        'r="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" || exit 0; '
        'p="$(dirname "$r")"; '
        f's="$p/{rel}"; '
        '[ -f "$s" ] || exit 0; '
        + (f'{runner} {args}' if args else runner)
        + "'"
    )
    return {"type": "command", "command": cmd, "timeout": 5000, "statusMessage": TAG + status}


# GROUPS maps each Codex hook event to a LIST of (matcher, handler) groups so a single
# event (PreToolUse) can carry more than one of our groups (Task 7 appends the git-guard).
# matcher=None means "omit the matcher field" — which is how Codex's real global hooks
# (~/.codex/hooks.json, verified 2026-06-30) express catch-all SessionStart/Stop/PostToolUse
# firing. Do NOT use "startup|resume" for SessionStart: that is Claude-Code vocabulary and
# Codex SessionStart has no such sub-events, so it would never match and the register hook
# would silently never fire (success criterion 1 would fail with no error). PreToolUse MUST
# be restricted to apply_patch — the only Codex edit tool (probe F4) and the only payload
# shape codex_claim_guard.py can parse (tool_input.command). Edit/Write are Claude-Code tool
# names, not Codex, and the guard no-ops on them, so they are deliberately NOT in the matcher.
GROUPS = {
    "SessionStart": [(None, guarded("scripts/git_policy/presence_hook.sh", "register", "register presence"))],
    "PreToolUse": [("apply_patch", guarded("scripts/git_policy/codex_claim_guard.py", "", "auto-declare write area"))],
    "PostToolUse": [(None, guarded("scripts/git_policy/codex_presence_flush.py", "", "presence heartbeat / flush"))],
    "Stop": [(None, guarded("scripts/git_policy/presence_hook.sh", "deregister", "deregister presence"))],
}


def _strip_ours(groups):
    out = []
    for g in groups or []:
        kept = [h for h in g.get("hooks", []) if not h.get("statusMessage", "").startswith(TAG)]
        if kept:
            out.append({**g, "hooks": kept})
    return out


def install(doc):
    hooks = doc.setdefault("hooks", {})
    for event, our_groups in GROUPS.items():
        groups = _strip_ours(hooks.get(event))
        for matcher, handler in our_groups:
            entry = {"hooks": [handler]}
            if matcher is not None:
                entry["matcher"] = matcher  # omit the field entirely when None (Codex catch-all)
            groups.append(entry)
        hooks[event] = groups
    return doc


def main(argv):
    target = os.environ.get("CODEX_HOOKS_FILE") or os.path.expanduser("~/.codex/hooks.json")
    doc = {}
    if os.path.exists(target):
        try:
            with open(target) as fh:
                doc = json.load(fh)
        except ValueError:
            print(f"refusing to overwrite unparseable {target}", file=sys.stderr)
            return 1
    install(doc)
    if "--print" in argv:
        print(json.dumps(doc, indent=2))
        return 0
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if os.path.exists(target):
        shutil.copyfile(target, target + ".bak")  # back up the original before overwrite
    tmp = target + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, indent=2)
    os.replace(tmp, target)
    print(f"installed presence hooks into {target}; review/trust once via Codex /hooks if prompted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/git_policy/test_install_codex_presence_hooks.py -q`
Expected: PASS (creation, guarded/path-free commands, preserve-foreign, idempotent).

- [ ] **Step 5: Install for real + one-time trust + smoke check**

```bash
python3 scripts/git_policy/install_codex_presence_hooks.py
```
Then start one Codex session in **each** worktree (master, specwork, trainex). On first encounter Codex prompts to trust the new global hook entries — accept once per machine. Verify each event fires (status messages `aps: …` appear) and that a Codex `apply_patch` produces a claim:
```bash
scripts/agent-presence list   # the Codex session appears on the roster
```

- [ ] **Step 6: Commit**

```bash
GIT_AGENT_ID="codex-presence" GIT_AGENT_OWNED_PATHS="scripts/git_policy/install_codex_presence_hooks.py:tests/git_policy/test_install_codex_presence_hooks.py" \
  scripts/agent-commit -m "feat(governance): add global codex presence hook installer" \
  -m "Idempotently merge four guarded presence hook groups into the global ~/.codex/hooks.json, preserving other tools' handlers. Guarded commands resolve this repo via the git common-dir and no-op in any other repo, so global firing is safe machine-wide. Replaces the design's project-local P4 (collapsed)." \
  -m "Agent-Assisted-By: Claude Opus 4.8"
```

---

### Task 6: AGENTS.md announce nudge (F-B)

**Files:**
- Modify: `AGENTS.md` (under `### Concurrent agents`, ~line 129, after the `scripts/agent-claim` sentence)

**Interfaces:** documentation only; invokes `agent-codex-announce` (Task 4) and `agent-presence` (existing) by a worktree-independent path.

- [ ] **Step 1: Add the nudge** (no test; verified by Task 8 manual check)

Insert after the `### Concurrent agents` paragraph:

```markdown
**Codex sessions — announce at session start (advisory).** Codex reads this file, not
`CLAUDE.md`. Presence/claims are recorded automatically by the global hooks (roster on
session start, write-area claims on `apply_patch`), so this step is optional human-intent
signalling, not a safety requirement. From any worktree:

    P="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
    "$P/scripts/agent-codex-announce" "<your task summary>" --areas <comma,separated,paths>

See peers:

    "$P/scripts/agent-presence" list
```

- [ ] **Step 2: Verify rendering**

Run: `python3 -c "import pathlib;print('agent-codex-announce' in pathlib.Path('AGENTS.md').read_text())"`
Expected: `True`.

- [ ] **Step 3: Commit**

```bash
GIT_AGENT_ID="codex-presence" GIT_AGENT_OWNED_PATHS="AGENTS.md" \
  scripts/agent-commit -m "docs(governance): nudge codex sessions to announce at start" \
  -m "Add an advisory announce nudge for Codex under Concurrent agents, invoking the announce shim and roster via a worktree-independent common-dir path. Advisory only; the global hooks record presence and claims automatically." \
  -m "Agent-Assisted-By: Claude Opus 4.8"
```

---

### Task 7: Git-guard trust-hole companion fix (flagged — confirm before executing)

> **⚠️ DISPOSITION RESOLVED 2026-06-30: A (SKIP).** The user chose disposition A: presence hooks go global via Task 5; the git-policy guard stays self-contained in the repo; the specwork/trainex early-warning gap is closed by a one-time `/hooks` trust per worktree. **All steps below are NOT executed.** This task is retained only as a documented option for a future decision. An executor MUST NOT empty `.codex/hooks.json` or add the git-guard to the global installer without a new explicit user decision (disposition B or C). Skip directly to Task 8.

**Context:** The existing Git-policy guard lives in the repo's `.codex/hooks.json` `PreToolUse` (matcher `^(Bash|shell_command|exec_command|functions\.exec_command)$`). Verified live: it is trusted (and firing) only in `master`; **specwork and trainex are unguarded today**. The same global-install mechanism closes this. The git-guard matcher is disjoint from the claim-guard matcher (`apply_patch`), so both PreToolUse groups coexist with no double-fire.

> **DECISION REQUIRED (flagged — confirm before executing).** This task edits the tracked enforcement artifact (`.codex/hooks.json`) and makes git-policy enforcement depend on a per-machine, **untracked** global file. The user endorsed the global *strategy* on 2026-06-30 but did **not** specifically endorse emptying the tracked file. Three dispositions:
>
> - **A — SKIP (safe default).** Leave Task 5's installer as shipped (claim-guard only); keep the project-local git-guard; close the specwork/trainex gap with a one-time `/hooks` trust per worktree. Git-policy stays portable and self-contained in the repo. **Recommended if undecided.**
> - **B — EXECUTE + REMOVE (destructive).** Append the git-guard group to the global installer **and** empty the repo `.codex/hooks.json` to `{ "hooks": {} }`. Git-policy then fires in all worktrees on *this* machine — but disappears on fresh clone, CI, other machines, or after a `~/.codex` wipe (the user wiped `~/.codex` recently). Requires `ALLOW_DESTRUCTIVE_GIT=1` + a recovery checkpoint per repo git policy.
> - **C — EXECUTE ADDITIVE (no removal).** Append the git-guard group globally **but keep** the repo `.codex/hooks.json` git-guard. Both PreToolUse groups fire in master (harmless — both exit 0) at the cost of a noisy double-fire. Trades quietness for zero-removal safety and full portability.
>
> Pick A, B, or C before executing. This plan ships in disposition **A** (Task 5 installs presence hooks only; the git-guard is untouched).

- [ ] **Step 1 (dispositions B/C only): Extend the installer** by appending a second tuple to the `GROUPS["PreToolUse"]` list (the Task 5 list-per-event structure supports this directly): `("^(Bash|shell_command|exec_command|functions\\.exec_command)$", guarded("scripts/git_policy/guard_agent_git_command.py", "", "git policy"))`. Add a test asserting both PreToolUse groups (claim-guard `apply_patch` + git-guard) survive one install run and that no tool name matches both matchers (disjoint). **Skip this step entirely under disposition A.**

- [ ] **Step 2: Run installer tests**

Run: `python3 -m pytest tests/git_policy/test_install_codex_presence_hooks.py -q`
Expected: PASS.

- [ ] **Step 3: Remove the project-local git-guard to avoid double-fire in master.** Replace `.codex/hooks.json` contents with `{ "hooks": {} }` (or delete the `PreToolUse` group), since the guard now fires globally in all worktrees. Re-run the installer and re-trust once per machine.

- [ ] **Step 4: Verify** the git-guard now fires in specwork/trainex (attempt a disallowed `git push` from a Codex session in specwork → blocked) and still fires once (not twice) in master.

- [ ] **Step 5: Commit**

```bash
GIT_AGENT_ID="codex-presence" GIT_AGENT_OWNED_PATHS="scripts/git_policy/install_codex_presence_hooks.py:tests/git_policy/test_install_codex_presence_hooks.py:.codex/hooks.json" \
  scripts/agent-commit -m "fix(governance): fire codex git-guard in all worktrees via global hooks" \
  -m "Relocate the Git-policy PreToolUse guard to the global ~/.codex/hooks.json installer so it is trusted-by-machine and fires in specwork/trainex (previously unguarded); drop the project-local entry to avoid double-firing in master. Matcher is disjoint from the claim guard." \
  -m "Agent-Assisted-By: Claude Opus 4.8"
```

---

### Task 8: End-to-end verification against success criteria

**Files:** none (verification + the already-shipped F-A check).

- [ ] **Step 1: Full suite green**

Run: `python3 -m pytest tests/git_policy/ -q`
Expected: PASS (existing `test_presence.py`, `test_concurrency.py`, `test_git_policy.py` + the four new files).

- [ ] **Step 2: F-A regression (already-shipped) check**

Confirm `scripts/agent-presence` resolves via the common-dir (not `--show-toplevel`):
Run: `grep -n 'git-common-dir' scripts/agent-presence`
Expected: the `repo_root="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"` line is present (F-A is already done; do not re-implement).

- [ ] **Step 3: Walk the seven success criteria** (interactive, with at least one real Codex session per worktree):

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Codex on roster from any worktree | `scripts/agent-presence list` shows the Codex session |
| 2 | Claim within the apply_patch round-trip | after a Codex edit, a `session:<id>` claim is on the board |
| 3 | Conflict warning Claude↔Codex | Claude claims a file; Codex `apply_patch` on it prints a stderr warning |
| 4 | `announce`/`list` work in specwork & trainex | run both from each linked worktree, Claude and Codex |
| 5 | Liveness | non-edit activity keeps the roster entry; clean Stop removes presence+claims; on crash the **roster entry** is cleared by the 20-min presence sweep and the session's **claims** expire at the 2-hour `agent_claims` expiry — two distinct timers, do not conflate them |
| 6 | Proactive announce lands same-call | `agent-codex-announce …` then any tool call → summary in `list` |
| 7 | No silent trust gaps | all four `aps:` hooks fire in master, specwork, trainex |

- [ ] **Step 4: Final state commit (if any verification notes/fixtures were added)** — otherwise none.

---

## Self-Review (run before handoff)

**Spec coverage:** P0 → Tasks 3+5 (heartbeat hook + SessionStart/Stop wiring). P1 → Task 2 (apply_patch only — see below). P2 → Tasks 3+4. P3 → Task 1. P4 → **cut**, replaced by Task 5 (global install) per user decision. F-A → **already done**, verified in Task 8. F-B → Task 6. Hook wiring → Task 5 (global, guarded). Git-guard gap (F6) → Task 7 (FLAGGED, three dispositions A/B/C; ships as A). Success criteria 1–7 → Task 8. V2/V3/V4/V5/V7 → resolved by probe; V5 locked by Tasks 1+4 tests; V6 (subagent announce) is out of scope (auto-declare attributes to whatever `session_id` the hook reports, which is internally consistent — note for follow-up).

**Matcher grounding (corrected 2026-06-30 review):** SessionStart/Stop/PostToolUse **omit the matcher field** (Codex's real global hooks carry none for these events; `startup|resume` is Claude-Code vocabulary and would silently never match). PreToolUse is restricted to **`apply_patch` only** — the claim guard parses `tool_input.command` (apply_patch bodies) and no-ops on anything else, so Edit/Write are deliberately excluded. Locked by `test_sessionstart_stop_postooluse_omit_matcher` and `test_pretooluse_narrowed_to_apply_patch`. The "zero setup" goal is per-**worktree**; a one-time per-machine trust prompt remains and recurs on new machines / fresh clones / `~/.codex` wipes.

**Placeholder scan:** every code/test step contains real, runnable content. The patch parser, the installer merge/idempotency, and the guarded global command were each validated against the real probe patch bodies and the live worktrees before this plan was finalized.

**Type/name consistency:** staging path `${TMPDIR:-/tmp}/agent-presence-staging/<id>.json` and JSON keys `{session_id,summary,areas}` are identical in `agent-codex-announce` (Task 4) and `codex_presence_flush.py` (Task 3). who-key `session:<id>` is produced via `agent_presence.who_key()` in Task 2 and consumed by `agent_claims.claims_for_who("session:…")` in tests. `extract_paths`/`repo_relative` are defined and used only within Task 2.

**Known limitation (accepted):** the catch-all PostToolUse heartbeat fires on Bash/exec/MCP/apply_patch (F5) but not read-only tools; a session doing only read-only tools for >20 min could be swept. Reads interleave with shell in practice; the commit-time net remains the hard backstop.

**Additional known limitations (2026-06-30 review):**
- **Staging channel is unauthenticated.** The flush hook (unsandboxed) reads and deletes `${TMPDIR}/agent-presence-staging/<session_id>.json`, and the sandboxed model shell shares that TMPDIR (V4). Any local process that can read `CODEX_THREAD_ID` can drop a staging file and inject an announce. Accepted because announce is advisory-only and the claim guard + commit-time net are the real safety mechanisms — but it is a shared writable channel, not a trusted one.
- **Identity equality across paths is asserted, not tested end-to-end.** All hook-side code (register, claim guard, flush) keys by the payload `session_id`; only the model-side announce shim keys by `CODEX_THREAD_ID` (env). F1 asserts these are equal. Tasks 1 and 4 lock each side independently, but no test exercises the full SessionStart→register path against a real Codex stdin payload to confirm the registered id equals `CODEX_THREAD_ID`. Verify on the first real Codex session in Task 8 (criterion 1); if they diverge, one session fragments into two roster entries.
- **Claim-vs-presence timers differ.** Crash recovery uses two distinct timers — the 20-min presence sweep clears the roster entry; claims expire at the 2-hour `agent_claims` expiry. Criterion 5 reflects this; do not assume the 20-min sweep releases claims.

### Post-execution notes (2026-07-22, first pass)

Tasks 1–6 and 8 executed and committed on `master` (`b2ca5a9b`, `f4840229`, `77b869d7`, `70494cc3`, `47cd898f`, `110d67fc`, plus final-review fix `27dd9d61`); Task 7 skipped per disposition A. Sanctioned deviations from the literal task code, each enforcing the plan's own binding constraints (recorded in commit bodies): isinstance shape/type guards in the claim guard and flush hook (fail-open Global Constraint), a non-vacuous V5 round-trip assertion in the shim test, and the installer guard-template test rewritten against decoded command strings (the raw-text `assertIn` could never match past `json.dump` escaping). `test_presence.py` now isolates `CODEX_THREAD_ID` (final-review must-fix). The real `~/.codex/hooks.json` install ran with pre/post verification (backup `.bak` matches pre-state; all foreign entries byte-intact at stable indices).

New known limitation (final review 2026-07-22): **reverse-nesting identity precedence** — a Claude session launched from inside a Codex terminal inherits `CODEX_THREAD_ID`, and `register`/`deregister` resolve env before stdin, so the inner Claude session would adopt (and on Stop, deregister) the outer Codex identity. Advisory-only, self-heals via sweep/expiry; same env-leak class as claude-in-claude. Optional hardening if ever wanted: pin `$r` in the installed global commands to this repo's absolute common dir (linked worktrees share it; zero functionality loss) — this would also close the foreign-repo-executes-lookalike-scripts edge inherent in runtime `$p` resolution.

Verified synthetically (verbatim installed hook commands, Codex-shaped stdin payloads, from the trainex worktree): register / apply_patch claim / foreign-overlap warning / same-call announce flush with staging consumed / heartbeat / idempotent double-Stop (which also released the session's claims). Remaining for criteria closure (interactive, user): one-time Codex trust of the four `aps:` global hook entries, then Step-3 criteria 1–7 with a real Codex session per worktree — including the F1 check that the registered id equals `CODEX_THREAD_ID`.

## Execution Handoff

Plan complete and saved to `docs/work/plans/cross_cutting/presence-overlap-awareness/2026-06-30-codex-presence-integration-implementation-plan.md`. Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task (T1→T8), review between tasks, fast iteration. REQUIRED SUB-SKILL: superpowers:subagent-driven-development.
2. **Inline Execution** — execute tasks in-session with checkpoints. REQUIRED SUB-SKILL: superpowers:executing-plans.

Tasks 1–4 are independent of trust wiring and can land first; Task 5 wires them globally; Task 7 is RESOLVED as disposition A (skipped, 2026-06-30) — do not execute its steps. All commits are master-owned.
