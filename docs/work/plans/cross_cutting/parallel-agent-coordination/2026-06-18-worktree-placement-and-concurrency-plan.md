---
status: consumed
purpose: implementation-plan
created: 2026-06-18
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  When all tasks are executed and committed (gitignore line, agent-commit lock,
  owned-paths net, claims board + hooks, banner hook, worktree migration, and the
  governance-text landing). At that point set status to consumed and point readers
  to docs/git-guidelines.md and the shipped scripts.
---

# Worktree Placement & Parallel-Agent Concurrency — Implementation Plan

> **Status: CONSUMED (2026-06-18).** All tasks executed and committed; Task 3 resolved as
> already-existing (see Deviations §1 — the owned-paths net lives in
> `scripts/git_policy/validate_commit_msg.py`). Canonical homes: `docs/git-guidelines.md`
> (§"Per-track worktrees and overlap avoidance") and the shipped scripts under `scripts/`
> and `scripts/git_policy/`. Retained as the execution record.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved design at `docs/work/designs/cross_cutting/parallel-agent-coordination/2026-06-18-worktree-placement-and-concurrency-design.md` — per-track worktrees under `.worktrees/<track>/`, a wait-and-retry commit lock, a hard commit-time owned-paths net, an advisory auto-declare claims board, and an enforced session-start banner.

**Architecture:** All enforcement rides the project's existing git-policy infrastructure: bash entry points in `scripts/`, Python validators in `scripts/git_policy/`, git hooks in `.githooks/` (via `core.hooksPath`), and Claude Code hooks registered in the **tracked** `.claude/settings.json`. The cross-worktree shared state (commit lock, claims) lives under `$(git rev-parse --git-common-dir)/`, which every worktree shares. No new dependencies.

**Tech Stack:** bash, python3 (stdlib only), git ≥ 2.54, Claude Code hooks.

## Global Constraints

- Commit only via `scripts/agent-commit`; set `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`; never raw `git commit`, never broad `git add`, never `--no-verify`. (Enforced by `guard_agent_git_command.py`.)
- Commit message format: `<type>(<scope>): <lowercase imperative subject>`, ≤ 80 chars, no trailing period, no backticks/quotes/semicolons in the subject. Allowed types: `spec evidence verify plan docs feat fix refactor test chore`. Scope here is `governance`.
- Each agent-authored commit carries an `Agent-Assisted-By:` trailer (added automatically by `agent-commit`).
- Never rewrite history; tracks **merge** `master`, never rebase.
- Portable to Linux clones: do **not** rely on BSD-only `stat` flags; store timestamps in lock/claim files instead.
- Numbers (overridable via env): commit-lock wait & stale-floor = `300`s (~5 min); claim expiry = `7200`s (~2 h).
- Claude Code hooks ship through the tracked `.claude/settings.json`; hook scripts live tracked under `scripts/` / `scripts/git_policy/`.

---

## Task 1: Ignore the `.worktrees/` root

**Files:**
- Modify: `.gitignore` (append near the existing `.claude/worktrees/` rule)

**Interfaces:**
- Produces: a gitignored `.worktrees/` directory so nested worktrees never appear as untracked noise in the main repo.

- [ ] **Step 1: Add the ignore rule.** Append these two lines to `.gitignore` (after line `.claude/worktrees/`):

```gitignore
# Manual per-track worktrees (see docs/git-guidelines.md A4)
.worktrees/
```

- [ ] **Step 2: Verify the main repo stays clean with a nested dir present.**

Run:
```bash
mkdir -p .worktrees/_probe && git status --short && rmdir .worktrees/_probe
```
Expected: `git status --short` shows **only** ` M .gitignore` (no `.worktrees/` line).

- [ ] **Step 3: Commit.**

```bash
GIT_AGENT_ID="<agent/tool/model>" GIT_AGENT_OWNED_PATHS=".gitignore" \
  scripts/agent-commit -m "chore(governance): ignore .worktrees worktree root"
```

---

## Task 2: Commit lock — wait-and-retry with dead-holder reclaim (Option β)

**Files:**
- Modify: `scripts/agent-commit` (replace the fail-fast lock block, lines ~23–28, keep the rest)

**Interfaces:**
- Consumes: `GIT_AGENT_ID`, `GIT_AGENT_OWNED_PATHS` (already required).
- Produces: a commit path that waits up to `AGENT_COMMIT_LOCK_TIMEOUT` (default 300s) for the shared lock, reclaims it when the holder PID is dead or the lock is older than `AGENT_COMMIT_LOCK_STALE` (default 300s), and otherwise reports clearly. Lock dir records `pid` and `started` (epoch) for liveness/age checks.

- [ ] **Step 1: Replace the lock acquisition block.** In `scripts/agent-commit`, replace this:

```bash
lock_dir="$common_dir/agent-commit.lock"
if ! mkdir "$lock_dir" 2>/dev/null; then
  echo "git policy: another agent commit is in progress; retry after the lock clears: $lock_dir" >&2
  exit 1
fi
trap 'rmdir "$lock_dir" 2>/dev/null || true' EXIT
```

with this:

```bash
lock_dir="$common_dir/agent-commit.lock"

# Option beta: wait up to ~5 min for the shared lock. Reclaim it only when the
# holder process is gone, or as a backstop when the lock is older than the stale
# floor. Poll window and stale floor share one value so a waiter never gives up
# on a commit that is still legitimately in progress. Both are overridable.
lock_timeout="${AGENT_COMMIT_LOCK_TIMEOUT:-300}"
lock_stale="${AGENT_COMMIT_LOCK_STALE:-300}"
deadline=$(( $(date +%s) + lock_timeout ))

while true; do
  if mkdir "$lock_dir" 2>/dev/null; then
    printf '%s\n' "$$" > "$lock_dir/pid"
    date +%s > "$lock_dir/started"
    break
  fi

  holder_pid="$(cat "$lock_dir/pid" 2>/dev/null || true)"
  started="$(cat "$lock_dir/started" 2>/dev/null || echo 0)"
  age=$(( $(date +%s) - started ))

  holder_gone=0
  if [ -n "$holder_pid" ]; then
    kill -0 "$holder_pid" 2>/dev/null || holder_gone=1
  fi

  if [ "$holder_gone" -eq 1 ] || [ "$age" -ge "$lock_stale" ]; then
    # Atomic steal: only one waiter can rename the lock aside, so two waiters
    # cannot both reclaim. The commit-time owned-paths net (Task 3) is the
    # backstop for the rare case where a holder dies and a new one acquires
    # within this window.
    steal_dir="${lock_dir}.steal.$$"
    if mv "$lock_dir" "$steal_dir" 2>/dev/null; then
      rm -rf "$steal_dir" 2>/dev/null || true
    fi
    continue
  fi

  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "git policy: an agent commit has held the lock for >${lock_timeout}s; retry shortly: $lock_dir" >&2
    exit 1
  fi
  sleep 1
done

trap 'rm -rf "$lock_dir" 2>/dev/null || true' EXIT
```

- [ ] **Step 2: Verify a normal commit still works.** Make a trivial tracked change and commit it via `agent-commit`; expected: commit succeeds, `ls "$(git rev-parse --git-common-dir)/agent-commit.lock" 2>/dev/null` afterwards prints nothing (lock released).

- [ ] **Step 3: Verify a waiter waits then succeeds.**

Run (simulates a live holder, then releases it after 3s while a second commit waits):
```bash
L="$(git rev-parse --git-common-dir)/agent-commit.lock"
mkdir "$L"; printf '%s\n' "$$" > "$L/pid"; date +%s > "$L/started"
( sleep 3; rm -rf "$L" ) &
time ( echo "probe" >> README.md
       GIT_AGENT_ID=test GIT_AGENT_OWNED_PATHS=README.md scripts/agent-commit -m "chore(governance): lock wait probe" )
git reset --soft HEAD~1 && git checkout -- README.md   # undo the probe commit
```
Expected: the second commit blocks ~3s, then succeeds (real `$$` is alive, so it is not stolen; it proceeds once the background process removes the lock).

- [ ] **Step 4: Verify a dead-holder lock is reclaimed immediately.**

Run:
```bash
L="$(git rev-parse --git-common-dir)/agent-commit.lock"
mkdir "$L"; echo 999999 > "$L/pid"; date +%s > "$L/started"   # 999999 = a PID that does not exist
echo "probe2" >> README.md
GIT_AGENT_ID=test GIT_AGENT_OWNED_PATHS=README.md scripts/agent-commit -m "chore(governance): lock reclaim probe"
git reset --soft HEAD~1 && git checkout -- README.md
```
Expected: commit succeeds within ~1s (dead PID → immediate steal). No leftover lock dir.

- [ ] **Step 5: Commit.**

```bash
GIT_AGENT_ID="<agent/tool/model>" GIT_AGENT_OWNED_PATHS="scripts/agent-commit" \
  scripts/agent-commit -m "feat(governance): make agent-commit wait-and-retry with dead-holder reclaim" \
  -m "Replaces fail-fast locking with Option beta: wait up to ~5 min, reclaim only when the holder PID is gone or the lock exceeds the stale floor; lock records pid and started for liveness and age."
```

---

## Task 3: The hard guarantee — commit-time owned-paths net  — NOT NEEDED (already exists)

> **Resolved during execution:** this net already exists and is the canonical
> enforcement. `scripts/git_policy/validate_commit_msg.py` calls
> `validate_agent_owned_paths()` on every agent commit (`GIT_AGENT_COMMIT=1`, set by
> `scripts/agent-commit`) and fails any staged file outside `GIT_AGENT_OWNED_PATHS`
> (message: `staged file outside declared owned paths`). The original design's
> "(unchanged)" was correct. A duplicate added to the pre-commit hook during
> execution (commit 24bd70e) was reverted (commit c5cb055) to keep a single
> enforcement point. **No action required for this task.** The steps below are
> retained only as the historical record of the mistaken addition.

**Files:**
- Modify: `scripts/git_policy/validate_staged_paths.py` (extend `main()`)

**Interfaces:**
- Consumes: `GIT_AGENT_OWNED_PATHS` (colon- or newline-separated repo-relative prefixes).
- Produces: a pre-commit failure if any staged path is **outside** the declared owned paths. This is the design's hard backstop against silent same-file overwrite. No-op when `GIT_AGENT_OWNED_PATHS` is unset (e.g. human commits).

- [ ] **Step 1: Add an owned-paths check.** In `scripts/git_policy/validate_staged_paths.py`, inside `main()`, immediately after the existing blob-size loop and **before** the `if errors:` block, insert:

```python
    owned_raw = os.environ.get("GIT_AGENT_OWNED_PATHS", "")
    if owned_raw:
        prefixes = [
            piece.strip().lstrip("./").rstrip("/")
            for chunk in owned_raw.split(":")
            for piece in chunk.splitlines()
            if piece.strip()
        ]
        for path in paths:
            if not any(path == prefix or path.startswith(prefix + "/") for prefix in prefixes):
                errors.append(
                    f"staged path outside GIT_AGENT_OWNED_PATHS (declare it or unstage it): {path}"
                )
```

- [ ] **Step 2: Verify an owned path passes.**

Run:
```bash
echo "probe" >> README.md && git add README.md
GIT_AGENT_OWNED_PATHS=README.md python3 scripts/git_policy/validate_staged_paths.py; echo "exit=$?"
git restore --staged README.md && git checkout -- README.md
```
Expected: `exit=0`.

- [ ] **Step 3: Verify a non-owned path fails.**

Run:
```bash
echo "probe" >> README.md && git add README.md
GIT_AGENT_OWNED_PATHS="docs/" python3 scripts/git_policy/validate_staged_paths.py; echo "exit=$?"
git restore --staged README.md && git checkout -- README.md
```
Expected: `exit=1` with `git policy: staged path outside GIT_AGENT_OWNED_PATHS ...: README.md`.

- [ ] **Step 4: Commit.**

```bash
GIT_AGENT_ID="<agent/tool/model>" GIT_AGENT_OWNED_PATHS="scripts/git_policy/validate_staged_paths.py" \
  scripts/agent-commit -m "feat(governance): enforce owned paths at commit time" \
  -m "Adds the design's hard commit-time net: when GIT_AGENT_OWNED_PATHS is set, every staged path must fall under a declared prefix, else the pre-commit hook fails."
```

---

## Task 4: Claims board + `agent-claim` / `agent-release`

**Files:**
- Create: `scripts/git_policy/agent_claims.py` (claims library + CLI)
- Create: `scripts/agent-claim` (bash wrapper)
- Create: `scripts/agent-release` (bash wrapper)
- Modify: `scripts/setup-git-hooks.sh` (add the three to its `chmod +x` list)

**Interfaces:**
- Produces:
  - `agent_claims.py claim <area> [why]` → records/refreshes this agent's claim (no-op if a different live agent holds it).
  - `agent_claims.py release <area>` → removes this agent's claim.
  - `agent_claims.py check <area>` → exit 0 if free/mine, exit 3 (+ stderr) if a different agent holds it.
  - `agent_claims.py list` → prints `who\tarea\twhy`.
  - Storage: one JSON file per claim (keyed by sha1(area)) under `$(git rev-parse --git-common-dir)/agent-claims/`; expiry is **time-based** (default 7200s) plus explicit release.
- Consumes: `GIT_AGENT_ID` for identity (falls back to `pid:<ppid>`).

- [ ] **Step 1: Create `scripts/git_policy/agent_claims.py`:**

```python
#!/usr/bin/env python3
"""Advisory cross-worktree claims board (one JSON file per claim).

Claims live under $(git rev-parse --git-common-dir)/agent-claims/ so every
worktree shares them. One file per claim means concurrent agents add and drop
claims without corrupting a shared file. Expiry is time-based (each edit-hook
is a short-lived process, so there is no persistent agent PID to test) plus
explicit release.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

EXPIRY_SECONDS = int(os.environ.get("AGENT_CLAIM_EXPIRY", str(2 * 60 * 60)))


def claims_dir():
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
    path = os.path.join(common, "agent-claims")
    os.makedirs(path, exist_ok=True)
    return path


def claim_file(area):
    key = hashlib.sha1(area.encode("utf-8")).hexdigest()[:16]
    return os.path.join(claims_dir(), key)


def agent_id():
    return os.environ.get("GIT_AGENT_ID") or f"pid:{os.getppid()}"


def load(path):
    try:
        with open(path) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def expired(entry):
    return entry is None or (time.time() - entry.get("when", 0)) > EXPIRY_SECONDS


def sweep():
    directory = claims_dir()
    for name in os.listdir(directory):
        full = os.path.join(directory, name)
        if name.endswith(".tmp") or expired(load(full)):
            try:
                os.remove(full)
            except OSError:
                pass


def holder(area):
    """Return the entry if a *different* live agent holds `area`, else None."""
    entry = load(claim_file(area))
    if expired(entry) or entry.get("who") == agent_id():
        return None
    return entry


def claim(area, why=""):
    sweep()
    other = holder(area)
    if other is not None:
        return 0  # held by someone else; advisory, do not clobber
    path = claim_file(area)
    entry = {"who": agent_id(), "area": area, "why": why, "when": int(time.time())}
    tmp = f"{path}.tmp"
    with open(tmp, "w") as handle:
        json.dump(entry, handle)
    os.replace(tmp, path)
    return 0


def release(area):
    path = claim_file(area)
    entry = load(path)
    if entry is not None and entry.get("who") == agent_id():
        try:
            os.remove(path)
        except OSError:
            pass
    return 0


def check(area):
    other = holder(area)
    if other is None:
        return 0
    when = time.strftime("%H:%M", time.localtime(other.get("when", 0)))
    print(f"claim conflict: '{area}' is held by {other.get('who')} since {when}", file=sys.stderr)
    return 3


def list_claims():
    sweep()
    directory = claims_dir()
    for name in sorted(os.listdir(directory)):
        entry = load(os.path.join(directory, name))
        if entry is not None:
            print(f"{entry.get('who')}\t{entry.get('area')}\t{entry.get('why', '')}")
    return 0


def main(argv):
    if not argv:
        print("usage: agent_claims.py {claim|release|check|list} [area] [why]", file=sys.stderr)
        return 2
    command, rest = argv[0], argv[1:]
    if command == "list":
        return list_claims()
    if not rest:
        print(f"git policy: '{command}' needs an <area>", file=sys.stderr)
        return 2
    if command == "claim":
        return claim(rest[0], rest[1] if len(rest) > 1 else "")
    if command == "release":
        return release(rest[0])
    if command == "check":
        return check(rest[0])
    print(f"unknown command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 2: Create `scripts/agent-claim`:**

```bash
#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
exec python3 "$repo_root/scripts/git_policy/agent_claims.py" claim "$@"
```

- [ ] **Step 3: Create `scripts/agent-release`:**

```bash
#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
exec python3 "$repo_root/scripts/git_policy/agent_claims.py" release "$@"
```

- [ ] **Step 4: Make them executable and add to setup.** Run `chmod +x scripts/agent-claim scripts/agent-release scripts/git_policy/agent_claims.py`, then in `scripts/setup-git-hooks.sh` add these three to the `chmod +x` list (before the final `\` of that list).

- [ ] **Step 5: Verify claim / conflict / release / expiry.**

Run:
```bash
GIT_AGENT_ID=A scripts/agent-claim simulation_data/foo.py "edit foo"
GIT_AGENT_ID=B python3 scripts/git_policy/agent_claims.py check simulation_data/foo.py; echo "B sees exit=$?"
GIT_AGENT_ID=A python3 scripts/git_policy/agent_claims.py check simulation_data/foo.py; echo "A sees exit=$?"
GIT_AGENT_ID=A scripts/agent-release simulation_data/foo.py
GIT_AGENT_ID=B python3 scripts/git_policy/agent_claims.py check simulation_data/foo.py; echo "after release exit=$?"
```
Expected: `B sees exit=3` (conflict), `A sees exit=0` (own claim), `after release exit=0`.

- [ ] **Step 6: Commit.**

```bash
GIT_AGENT_ID="<agent/tool/model>" \
  GIT_AGENT_OWNED_PATHS="scripts/git_policy/agent_claims.py:scripts/agent-claim:scripts/agent-release:scripts/setup-git-hooks.sh" \
  scripts/agent-commit -m "feat(governance): add agent-claim and agent-release claims board" \
  -m "Advisory one-file-per-claim board under the shared git common dir; time-based expiry; check returns exit 3 on a foreign live claim."
```

---

## Task 5: Warn-on-edit + auto-declare hook

**Files:**
- Create: `scripts/git_policy/claim_guard.py` (PreToolUse hook for Edit/Write)
- Modify: `.claude/settings.json` (add a PreToolUse matcher for `Edit|Write|MultiEdit`)
- Modify: `scripts/setup-git-hooks.sh` (add `claim_guard.py` to `chmod +x`)

**Interfaces:**
- Consumes: the Claude Code PreToolUse JSON payload on stdin (`tool_input.file_path`); `agent_claims.py`.
- Produces: a **non-blocking** warning (stderr, exit 0) when the target file is held by a different agent, and **auto-declares** this agent's claim otherwise. Always exits 0 (advisory; fails open on any internal error).

- [ ] **Step 1: Create `scripts/git_policy/claim_guard.py`:**

```python
#!/usr/bin/env python3
"""PreToolUse hook for Edit/Write: warn on a foreign claim, else auto-declare.

Advisory only: always exits 0 so it never blocks an edit. The hard guarantee
against silent overwrite is the commit-time owned-paths net, not this hook.
"""
import json
import os
import subprocess
import sys

import agent_claims  # same directory


def repo_relative(file_path):
    try:
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        return os.path.relpath(os.path.abspath(file_path), root)
    except Exception:
        return file_path


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    area = repo_relative(file_path)
    try:
        other = agent_claims.holder(area)
        if other is not None:
            print(
                f"claim warning: '{area}' is already claimed by {other.get('who')} "
                f"(reason: {other.get('why') or 'n/a'}). Coordinate before overlapping.",
                file=sys.stderr,
            )
        else:
            agent_claims.claim(area, why="auto-declared on edit")
    except Exception:
        return 0  # fail open: advisory must never block
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(main())
```

- [ ] **Step 2: Register the hook in `.claude/settings.json`.** Add a second entry to the `PreToolUse` array (sibling of the existing `Bash` matcher):

```json
{
  "matcher": "Edit|Write|MultiEdit",
  "hooks": [
    {
      "type": "command",
      "command": "python3 \"$(git rev-parse --show-toplevel)/scripts/git_policy/claim_guard.py\"",
      "timeout": 15,
      "statusMessage": "Checking agent claims"
    }
  ]
}
```

- [ ] **Step 3: `chmod +x scripts/git_policy/claim_guard.py`** and add it to the `chmod +x` list in `scripts/setup-git-hooks.sh`.

- [ ] **Step 4: Verify warn + auto-declare.**

Run (simulates the hook payload):
```bash
PAY='{"tool_input":{"file_path":"'"$PWD"'/simulation_data/bar.py"}}'
echo "$PAY" | GIT_AGENT_ID=A python3 scripts/git_policy/claim_guard.py; echo "A exit=$?"   # auto-declares
echo "$PAY" | GIT_AGENT_ID=B python3 scripts/git_policy/claim_guard.py; echo "B exit=$?"   # warns
GIT_AGENT_ID=A scripts/agent-release simulation_data/bar.py
```
Expected: A prints nothing, `A exit=0`; B prints `claim warning: 'simulation_data/bar.py' is already claimed by A ...` and `B exit=0`.

- [ ] **Step 5: Commit.**

```bash
GIT_AGENT_ID="<agent/tool/model>" \
  GIT_AGENT_OWNED_PATHS="scripts/git_policy/claim_guard.py:.claude/settings.json:scripts/setup-git-hooks.sh" \
  scripts/agent-commit -m "feat(governance): add warn-on-edit auto-declare claim hook" \
  -m "PreToolUse hook on Edit/Write/MultiEdit: warns (non-blocking) when a file is held by another agent and auto-declares the editing agent's claim otherwise."
```

---

## Task 6: Session-start banner hook

**Files:**
- Create: `scripts/session_banner.sh`
- Modify: `.claude/settings.json` (add a `SessionStart` hook)
- Modify: `scripts/setup-git-hooks.sh` (add `session_banner.sh` to `chmod +x`)

**Interfaces:**
- Produces: a one-line banner on stdout naming the worktree directory and branch, printed at the top of every session. No inputs; always exits 0.

- [ ] **Step 1: Create `scripts/session_banner.sh`:**

```bash
#!/usr/bin/env bash
# SessionStart banner: states which worktree + branch this session is in.
set -uo pipefail
root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
branch="$(git -C "$root" symbolic-ref --short HEAD 2>/dev/null || echo 'DETACHED')"
echo "worktree $(basename "$root") -> branch ${branch}  ($root)"
exit 0
```

- [ ] **Step 2: Register in `.claude/settings.json`.** Add a `SessionStart` key as a sibling of `PreToolUse` inside `hooks`:

```json
"SessionStart": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "bash \"$(git rev-parse --show-toplevel)/scripts/session_banner.sh\"",
        "timeout": 10
      }
    ]
  }
]
```

- [ ] **Step 3: `chmod +x scripts/session_banner.sh`** and add it to the `chmod +x` list in `scripts/setup-git-hooks.sh`.

- [ ] **Step 4: Verify the banner.**

Run:
```bash
bash scripts/session_banner.sh
```
Expected (from the main repo): `worktree 3_body_problem -> branch master  (/Users/.../3_body_problem)`.

- [ ] **Step 5: Commit.**

```bash
GIT_AGENT_ID="<agent/tool/model>" \
  GIT_AGENT_OWNED_PATHS="scripts/session_banner.sh:.claude/settings.json:scripts/setup-git-hooks.sh" \
  scripts/agent-commit -m "feat(governance): add session-start worktree banner hook" \
  -m "SessionStart hook prints the worktree directory and branch at the top of every session — the enforced form of the announce-your-branch rule."
```

---

## Task 7: Migrate the v1.6 worktree into `.worktrees/specwork` — GATED

> **Prerequisite (human confirmation required):** the `~/Desktop/3_body_problem-v1.6` worktree must be **quiescent** — no active agent session editing inside it. `git worktree move` relocates that directory; doing it under an active session disrupts that session's working directory. Confirm idle before running.

**Files:** none tracked — `git worktree move` updates `.git` worktree metadata only; there is nothing to commit.

- [ ] **Step 1: Confirm the source worktree exists and is clean.**

Run:
```bash
git worktree list
git -C ~/Desktop/3_body_problem-v1.6 status --short --branch
```
Expected: the list shows `~/Desktop/3_body_problem-v1.6  <sha> [milestone/v1.6]`; its status is acceptably clean (commit or stash anything you intend to keep first).

- [ ] **Step 2: Move it.**

Run:
```bash
mkdir -p .worktrees
git worktree move ~/Desktop/3_body_problem-v1.6 "$(git rev-parse --show-toplevel)/.worktrees/specwork"
```

- [ ] **Step 3: Verify the move (design §6 acceptance).**

Run:
```bash
git worktree list
git status --short          # main repo: no .worktrees/ noise
git -C .worktrees/specwork rev-parse --abbrev-ref HEAD   # -> milestone/v1.6
```
Expected: list shows `.worktrees/specwork ... [milestone/v1.6]`; main `git status` shows no `.worktrees/` entry (Task 1 ignore is in effect); the branch is unchanged.

- [ ] **Step 4: Confirm a commit inside lands on the right branch (non-destructive check).**

Run:
```bash
git -C .worktrees/specwork log -1 --pretty='%h %d %s'
```
Expected: HEAD is on `milestone/v1.6`. (No commit is created by this plan.)

---

## Task 8: Land the policy in the governance text

**Files:**
- Modify: `docs/git-guidelines.md` (the A4 / worktree + commit-lock section)
- Modify: `CLAUDE.md` (add one recognition line under the concurrent-agents governance)

**Interfaces:**
- Produces: the canonical, agent-facing statement of: per-track worktrees under `.worktrees/<track>/`; merge-not-rebase sync; the Option-β commit lock; the commit-time owned-paths net; and the advisory claims board with auto-declare. At this point the design doc may be set to `status: consumed`.

- [ ] **Step 1: Read `docs/git-guidelines.md` in full** (it is the authoritative policy; follow its existing structure and the A-prefixed section numbering before editing).

- [ ] **Step 2: Update the worktree/commit-lock section** to state, in the guidelines' own voice and format:
  - Per-track worktrees live at `.worktrees/<track>/`; tracks persist across milestones and **merge** `master` (never rebase).
  - Milestone science work and its `.planning/phases/NN/` planning live in the owning track's worktree; cross-cutting governance/CI lives on `master`.
  - `scripts/agent-commit` waits up to ~5 min for the shared lock and reclaims it only when the holder PID is gone or the lock exceeds the stale floor.
  - Agents may only stage paths under `GIT_AGENT_OWNED_PATHS` (now enforced at commit time).
  - Before overlapping on a file, consult/declare via `scripts/agent-claim`; the edit hook warns and auto-declares automatically.

- [ ] **Step 3: Add one recognition line to `CLAUDE.md`** under "CRITICAL GOVERNANCE: Git ... Concurrent agents", e.g.: "Per-track worktrees live under `.worktrees/<track>/`; the commit lock waits-and-retries; same-file overlap is mediated by `scripts/agent-claim` plus a warn-on-edit hook, with a hard commit-time owned-paths net. See `docs/git-guidelines.md`."

- [ ] **Step 4: Verify** no broken internal links and that the new prose matches the shipped script behavior (re-read Tasks 2–5).

- [ ] **Step 5: Commit.**

```bash
GIT_AGENT_ID="<agent/tool/model>" GIT_AGENT_OWNED_PATHS="docs/git-guidelines.md:CLAUDE.md" \
  scripts/agent-commit -m "docs(governance): land worktree concurrency policy in guidelines" \
  -m "Documents per-track worktrees, merge-not-rebase, the Option-beta commit lock, the commit-time owned-paths net, and the advisory auto-declare claims board."
```

- [ ] **Step 6 (optional):** set `status: consumed` in the design doc frontmatter and add a pointer to `docs/git-guidelines.md`; commit as `docs(governance): mark worktree concurrency design consumed`.

---

## Deviations from the design (captured during planning)

1. **Commit-time net already exists (correction of an execution-time error).** The pre-existing `validate_commit_msg.py` (`validate_agent_owned_paths`, gated on `GIT_AGENT_COMMIT=1`) already fails any agent commit staging a file outside `GIT_AGENT_OWNED_PATHS`. An earlier check missed that file and wrongly concluded the net did not exist; Task 3 then added a duplicate to the pre-commit hook (commit `24bd70e`), which was reverted (commit `c5cb055`). The original design's "(unchanged)" was correct; the design note is re-corrected accordingly. Net effect: no code change to the owned-paths net.
2. **Claim expiry is time-based, not PID-based.** Edit-hooks are short-lived processes, so there is no persistent agent PID to test (the PID-liveness check is valid only for the commit lock, where the committing process is alive throughout). Design corrected in the same commit.
3. **Hook shipping mechanism confirmed:** `.claude/settings.json` is tracked, so the new PreToolUse and SessionStart hooks propagate to clones/worktrees with no extra installer. (`.claude/settings.local.json` remains gitignored for machine-specific overrides.)
4. **Codex parity not included:** `.codex/hooks.json` exists, so a Codex equivalent of the claim/banner hooks is a possible follow-up; this plan implements the Claude Code hooks the design specifies.

## Self-review

- **Spec coverage:** design §5 change-set items 1–8 map to Tasks 1–8; §2.4 commit-time net → already enforced by `validate_commit_msg.py` (Task 3 not needed); §2.4 claims board + auto-declare → Tasks 4–5; §2.2 banner → Task 6; §2.1 migration → Task 7. ✓
- **Placeholders:** none — every code/file step shows complete content; `<agent/tool/model>` in commit commands is the executor's required identity value, not a code placeholder. ✓
- **Type/name consistency:** `agent_claims.holder/claim/release/check/list_claims` are defined in Task 4 and consumed unchanged in Task 5; lock files `pid`/`started` defined and read in Task 2; `GIT_AGENT_OWNED_PATHS` semantics consistent across Tasks 2–3. ✓
