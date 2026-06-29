---
status: active
purpose: design
created: 2026-06-28
milestone: untracked
phase: cross-cutting
retirement_trigger: When codex presence integration is implemented, tested, and the implementation plan is consumed.
---

# Codex Presence Integration Design

Extends the existing Claude Code presence-overlap awareness system so that Codex CLI
sessions also participate as first-class presence peers: appearing on the roster,
auto-declaring write areas on edit, and seeing peers' current claims.

> **Placement note (not doc content):** this is cross-cutting agent infrastructure. Per
> repo governance, the presence system lives on `master`; `master` owns cross-cutting
> infra while the milestone worktrees (specwork=`milestone/v1.6`, trainex=`track/trainex`)
> own milestone work. This file is currently untracked **in the specwork worktree** — it
> must be moved to and committed on `master`, alongside the implementation, **not** the
> milestone branch. The new scripts below are likewise master-owned.

---

## Background

The existing system (built for Claude Code) works as follows:

- **Presence registry** — one JSON file per live session under
  `$(git --git-common-dir)/agent-presence/`. All linked worktrees share the same
  common-dir, so the roster is cross-worktree.
- **Claims board** — one JSON file per claimed write-area under
  `$(git --git-common-dir)/agent-claims/`. This is the real overlap-prevention signal.
- **Identity** — each session is keyed by a session ID. Claude Code sessions use
  `CLAUDE_CODE_SESSION_ID`, seeded into `CLAUDE_ENV_FILE` by the `SessionStart` hook.
- **Auto-declare-on-edit** — a `PreToolUse` hook (`claim_guard.py`) fires on
  `Edit|Write|MultiEdit`, reads `tool_input.file_path`, and auto-claims the area or
  warns on foreign overlap.
- **Advisory announce** — the agent explicitly calls
  `scripts/agent-presence announce "<task>" --areas <paths>` to declare intended
  write areas upfront (e.g. at session start or plan time).
- **Hard backstop** — none of the above blocks anything; they are advisory. The only
  hard guarantee against silent overwrite is the commit-time owned-paths net in
  `scripts/agent-commit`. This matters for scoping below: an advisory signal that lands
  a beat late, or that occasionally fails open, does not by itself cause data loss.

Codex sessions today are invisible to this system: no presence file, no claims, no
roster visibility for the Codex agent.

---

## Empirical findings (probe session 2026-06-28)

These findings constrain the design and must be respected by the implementation.

### F1 — Identity: CODEX_THREAD_ID is the direct equivalent

`CODEX_THREAD_ID` is present in the shell-tool environment for every Codex session and
is identical to `session_id` in hook payloads. No env-file seeding is needed. When
`agent_presence.py` is called from a Codex shell-tool invocation, it can read this
env var directly as the session identity.

Evidence: empirical probe confirmed `CODEX_THREAD_ID` = hook `session_id`; hook payload
schema confirmed as `{"session_id": "...", "cwd": "...", "hook_event_name": "...",
"tool_name": "...", "tool_input": {...}}`.

Caveat (subagents): Codex subagent hooks report the **parent** session id. Whether a
subagent's shell `CODEX_THREAD_ID` matches that parent id is unconfirmed — see V6. This
matters only if subagents call `announce`; auto-declare (P1) attributes to whatever
`session_id` the hook reports, which is internally consistent either way.

### F2 — Sandbox: model-generated shell runs under seatbelt workspace-write

Codex sandboxes model-generated shell commands under `seatbelt workspace-write`. Writes
to the git common-dir from a linked worktree (e.g. specwork → master's `.git`) are
**blocked** by the seatbelt. This means a Codex `announce` call in a Bash tool
cannot directly write the presence/claims board from a linked worktree.

Evidence: `$HOME`-based sandbox probe returned `COMMON_DIR_WRITE=BLOCKED`.

Note: per Codex docs, `workspace-write` also keeps `.git/` read-only **even when it sits
inside the working dir**, so the same `announce` write is blocked on the **master**
worktree too — not only in linked worktrees. The design therefore does not special-case
master (see P2).

### F3 — Hooks are unsandboxed

Codex only sandboxes model-generated shell commands, not hooks. Hooks run as host-trusted
processes and can write the git common-dir freely regardless of worktree.

Implication: hooks are the only path that can reliably write presence/claims board entries
from a linked worktree.

### F4 — apply_patch hook shape (Codex 0.124+ / running 0.142)

Before 0.124.0, `apply_patch` emitted zero hook events (issue #16732). PR #18391 fixed
it, shipped in 0.124.0. The payload shape is:
- `tool_name`: `"apply_patch"` (matcher aliases: `Edit`, `Write`)
- `tool_input.command`: raw patch body (NOT `file_path`)

The patch body contains `*** Add/Update/Delete File: <path>` and `*** Move to: <path>`
markers for each affected file.

Implication: `claim_guard.py` (which reads `tool_input.file_path`) is not reusable for
Codex. A new `codex_claim_guard.py` must parse the patch body.

### F5 — Hook coverage in Codex 0.142

Only Bash/shell, unified_exec, apply_patch, and MCP tool handlers opt into
PreToolUse/PostToolUse. All other tool handlers return `None` (issue #20204).

Implication: PreToolUse fires for edit operations (apply_patch) and shell commands but
not for read-only tools. A PostToolUse heartbeat therefore fires on any *activity*
(edit/shell/exec/MCP) — which is exactly the liveness signal we want (see P0).

### F6 — Hook trust: per-hash, per-worktree gap

`~/.codex/config.toml` `[hooks.state]` stores a `trusted_hash` per
`"<source-file>:<event>:<group>:<index>"` key. Non-managed hooks must be interactively
reviewed per machine per file change. As of 2026-06-28, only the main worktree
`.codex/hooks.json` PreToolUse entry is trusted; specwork and trainex entries are absent
from `[hooks.state]` and silently not firing.

Implication: the trust gap must be closed by policy, not per-machine interactive review,
or hooks silently do nothing in linked worktrees. **This is also a current, independent
governance hole**: the Git-policy guard already shipped in `.codex/hooks.json` is *not
firing* for Codex in specwork/trainex today, so Codex git commands in those worktrees are
presently unguarded. Worth fixing on its own, ahead of (or alongside) this work.

### F7 — Latent bug: scripts/agent-presence shim broken in linked worktrees

`scripts/agent-presence` resolves `repo_root` via `git rev-parse --show-toplevel`, which
returns the linked worktree root (e.g. specwork). But `agent_presence.py`,
`presence_hook.sh`, and the shim itself live **only** in the master worktree's
`scripts/` (verified 2026-06-28: present on `master`, absent from specwork and trainex;
`agent_claims.py`/`claim_guard.py` happen to exist in all three because they landed before
the worktree branches last synced). The path
`<specwork>/scripts/git_policy/agent_presence.py` does not exist, so `announce` and
`list` fail in linked worktrees for Claude too — not just Codex.

---

## Design

Five pieces (P0–P4) plus two related fixes (F-A, F-B).

**Priority / scope.** P0 (roster lifecycle) and P1 (auto-declare on edit) are the
mandatory safety/coordination core: together they give Codex roster visibility and
write-area claims with no dependence on the model remembering to do anything. P3
(identity) and P4 (trust) are prerequisites that make P0/P1 fire correctly. P2 (proactive
announce) is a **secondary**, human-intent enhancement and the only piece with a residual
sandbox dependency; it can ship as a fast-follow without weakening safety, because the
commit-time owned-paths net in `scripts/agent-commit` is the hard backstop for everyone.

### P0 — Roster lifecycle hooks (register / heartbeat / deregister)

**What**: Wire three Codex lifecycle hooks to the existing branch-independent launcher
`presence_hook.sh`, exactly as Claude Code already does:

- **SessionStart → `presence_hook.sh register`** — creates the session's presence file
  under `$(git --git-common-dir)/agent-presence/` (liveness, worktree, branch).
- **PostToolUse → heartbeat** — folded into the P2 flush hook
  (`codex_presence_flush.py`), which calls `agent_presence.heartbeat(session_id)` on
  *every* PostToolUse, before any staging work.
- **Stop → `presence_hook.sh deregister`** — releases the session's claims and removes
  its presence file on clean exit.

**Why this is foundational, not optional.** The auto-declare hook (P1) and the announce
flush (P2) write *claims*, but neither creates the *presence file*.
`agent_presence.heartbeat()` is a no-op when no presence file exists yet
(`agent_presence.py:203` — `if entry is None: return 0`). So without SessionStart→register:

1. A Codex session that edits would hold claims on the board but **never appear on the
   roster** — defeating success criterion 1, since `list_roster()` iterates presence
   files, not claims.
2. With no presence file, `sweep_presence()` never reaps the session and so never calls
   `release_by_who()`; a crashed Codex session's claims would linger until the **2-hour**
   claims expiry instead of being released at the 20-minute presence stale floor.

**And heartbeat must fire on all activity, not just edits.** `sweep_presence()` reaps any
presence file whose `last_heartbeat` is older than the stale floor
(`AGENT_PRESENCE_STALE`, default 20 min). If heartbeat rode only `apply_patch`, a live
session doing 20+ minutes of non-edit work (reads, shell, MCP) would be reaped **while
alive**, releasing its claims and inviting the exact clobber this system prevents. Folding
heartbeat into the catch-all PostToolUse flush hook keeps a session alive as long as it
makes any tool call (F5).

### P1 — codex_claim_guard.py (primary safety mechanism)

**What**: A new `scripts/git_policy/codex_claim_guard.py` PreToolUse hook for Codex.
Mirrors `claim_guard.py` but parses the apply_patch patch body for file paths instead
of reading `tool_input.file_path`.

**Why primary**: Captures actual write areas at edit time, runs unsandboxed, has no
latency, and does not depend on the model remembering to announce. Write-area safety
must not hinge on AGENTS.md compliance. (Caveat: per Codex docs, PreToolUse is a
guardrail, not a complete enforcement boundary — F5 — so the commit-time net remains the
hard guarantee.)

**Trigger**: Codex `PreToolUse` event where `tool_name == "apply_patch"` (or its
matcher aliases `Edit`, `Write`).

**Identity**: Reads `session_id` from hook payload stdin (same as Claude hooks).
Sets `AGENT_CLAIM_WHO = "session:<session_id>"` — identical to the join key
`claim_guard.py:42` writes and to `agent_presence.who_key()` (`agent_presence.py:68`).
This identity must match the value the model side uses for staging (P2/P3); see the
invariant under P3.

**Path parsing**: Extracts file paths from `tool_input.command` (raw patch body) using
**all** of these markers (not just `*** Move to:`, which alone would capture only
renames):
```
*** Add File: <path>
*** Update File: <path>
*** Delete File: <path>
*** Move to: <path>
```
For a rename, both the `*** Update File:` (old path) and `*** Move to:` (new path) are
claimed, since the session is touching both. Each extracted path is resolved to a
repo-relative path (same logic as `claim_guard.py`'s `repo_relative()`).

**Behavior**:
1. For each extracted path, call `agent_claims.find_conflict(area)`.
2. If conflict: print warning to stderr (advisory; never blocks).
3. If no conflict: call `agent_claims.claim(area, why="auto-declared on edit")`.
4. Always exit 0 (fail-open; advisory).

(Heartbeat is handled by the PostToolUse flush hook on every tool call — see P0 — so it
is not duplicated here.)

**Output location**: `scripts/git_policy/codex_claim_guard.py`

### P2 — Stage→flush for proactive announce (secondary)

**What**: A two-part mechanism so `announce` (intended areas + human-readable summary)
can work from a linked worktree despite the seatbelt. This is the *secondary* signal:
write-area safety is already covered by P0+P1 and the commit-time net; announce adds a
human-readable task summary and lets a peer see intent before the first edit.

**Stage** (runs sandboxed, in a Codex Bash tool call):
The Codex agent calls a new `scripts/agent-codex-announce` shim, which writes a staging
payload JSON keyed by session id:
```json
{"session_id": "<CODEX_THREAD_ID>", "summary": "...", "areas": ["..."]}
```
Staging location is `$TMPDIR/agent-presence-staging/<CODEX_THREAD_ID>.json`. `$TMPDIR` is
writable under `workspace-write` **by default** — but not unconditionally: if the sandbox
is hardened (`exclude_tmpdir_env_var` / `exclude_slash_tmp`) or the sandboxed shell and
the host hook resolve **different** `$TMPDIR` values, staging silently fails. This is
gated by V4. If V4 is not clean, the robust fallback is a `.gitignore`d, workspace-relative
staging dir that both sides compute via `git rev-parse --show-toplevel` — the workspace is
the one path `workspace-write` always grants and the unsandboxed hook can always read.

**Flush + heartbeat** (runs unsandboxed, in the PostToolUse hook
`scripts/git_policy/codex_presence_flush.py`). On **every** PostToolUse event:
1. Read `session_id` from the hook payload.
2. `agent_presence.heartbeat(session_id)` — unconditional (this is the P0 heartbeat).
3. If `$TMPDIR/agent-presence-staging/<session_id>.json` exists:
   - `agent_presence.announce(session_id, summary, areas)`.
   - Delete the staging file. (Existence alone marks "not yet flushed"; deleting on
     consume means no timestamp bookkeeping is needed and a re-flush is harmless.)
4. Always exit 0.

**Latency**: near-zero. The `announce` shim is itself a Bash tool call, so the staging
file it writes is consumed by the **PostToolUse of that same call** — not a later one.

**Lifecycle hygiene**: SessionStart sweeps stale staging files (orphans from a crashed
session, guarding against a reused id); Stop deletes this session's staging file.
Flushing on Stop is intentionally *not* done — it would be immediately undone by the
deregister that follows.

**Why uniform stage→flush (even on the master worktree)**: Codex keeps `.git` read-only
under `workspace-write` even inside the working dir (F2), so a model-run `announce` is
blocked on master too. A single staging path with no per-worktree conditional is therefore
both simpler and correct everywhere.

**New files**:
- `scripts/agent-codex-announce` (shim: stage to `$TMPDIR`; must be reachable from any
  worktree — see F-B)
- `scripts/git_policy/codex_presence_flush.py` (hook: heartbeat every call; flush staging
  when present)

### P3 — Codex identity resolver in agent_presence.py

**What**: Extend `_session_from_env()` in `scripts/git_policy/agent_presence.py` to
read `CODEX_THREAD_ID` first, then fall back to `CLAUDE_CODE_SESSION_ID`.

**Current code** (`agent_presence.py:72`):
```python
def _session_from_env():
    return _safe_session_id(os.environ.get("CLAUDE_CODE_SESSION_ID"))
```

**New code**:
```python
def _session_from_env():
    # Codex sets CODEX_THREAD_ID; Claude Code sets CLAUDE_CODE_SESSION_ID.
    # When Codex is launched from within a Claude session, both may be set —
    # CODEX_THREAD_ID takes precedence because it is the active session's identity.
    return (
        _safe_session_id(os.environ.get("CODEX_THREAD_ID"))
        or _safe_session_id(os.environ.get("CLAUDE_CODE_SESSION_ID"))
    )
```

**Env-bleed guard**: When Codex is launched from a Claude terminal tab, the parent
shell may have `CLAUDE_CODE_SESSION_ID` set. Taking `CODEX_THREAD_ID` first ensures
the Codex session is identified by its own thread ID, not the parent Claude session's.

**Change scope**: one function, three lines. No other callers change.

**Invariant (must be tested — V5)**: the identity the model sees (`CODEX_THREAD_ID`) and
the identity hooks see (payload `session_id`) must be the **same string** (F1). The P2
staging key is written under the model's `CODEX_THREAD_ID` and read by the hook under the
payload `session_id`; the claims/roster join key is `session:<id>`. If these ever
diverge, one session fragments into two roster entries and its staged announce is never
found. Lock the equality with a test; track the subagent case under V6.

### P4 — requirements.toml managed hooks (trust by policy)

**What**: Declare the Codex presence hooks in `requirements.toml` under the
`[features].hooks = true` and managed-hooks sections so they are trusted-by-policy in
every worktree without per-machine interactive review.

**Why**: The hook-trust gap (F6) kills every hook-based piece, not just P1. Per-machine
interactive review is fragile (silently not firing today for specwork/trainex). Managed
hooks convert trust from a silent per-machine gap into an automatable, enforceable policy.
P4 is what actually delivers the design's "no per-machine manual setup" goal — so the
headline outcome is **contingent on P4**; if it cannot be made to work, the outcome
degrades to a one-time `/hooks` review per machine (loud, not silent).

**Verification item (V1; flagged, not a blocker)**: Codex's `requirements.toml`
managed-hooks support must be confirmed against the Codex 0.142 changelog and docs before
the implementation plan is finalized. If `requirements.toml` cannot enforce hook trust for
project-local `.codex/hooks.json` entries, the fallback is a setup script that runs the
per-worktree `/hooks` trust step (or equivalent) with an explicit error if run in an
untrusted worktree. The intent (trust-by-policy) is non-negotiable; the exact mechanism is
to verify at implementation time.

---

## Related fixes (in scope)

### F-A — Fix scripts/agent-presence shim for linked worktrees

**Bug**: `scripts/agent-presence` resolves `repo_root` via
`git rev-parse --show-toplevel` and then runs
`python3 "$repo_root/scripts/git_policy/agent_presence.py"`. In a linked worktree,
`show-toplevel` returns the linked worktree root, where the script does not exist (F7).

**Fix**: Resolve the main repo root from the git common-dir (which, from any worktree,
points at the main repo's `.git`):
```bash
#!/usr/bin/env bash
set -euo pipefail
# --path-format=absolute avoids the bare ".git" the main worktree would otherwise return.
repo_root="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
exec python3 "$repo_root/scripts/git_policy/agent_presence.py" "$@"
```

This resolves to the main repo's `agent_presence.py` from the main worktree and from every
linked worktree, regardless of checked-out branch. (`agent_presence.py` itself already
finds the shared presence/claims dirs via the common-dir and attributes the correct
worktree/branch via `--show-toplevel`.)

**Scope note**: This bug affects Claude sessions in linked worktrees too. The fix is
shared.

### F-B — AGENTS.md nudge

**What**: Add a brief nudge in `AGENTS.md` (Codex reads `AGENTS.md`, not `CLAUDE.md`)
instructing the Codex agent to announce at session start. Because the announce shim is
master-only infra (like the presence shim, F7), the nudge must invoke it by a
worktree-independent path, not a bare relative path that only exists on master.

**Content** (to be added under a "Concurrent Agent Coordination" or equivalent section):
```
At session start, announce your task and intended write paths so peer agents can see
your work. From any worktree:

    P="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
    "$P/scripts/agent-codex-announce" "<your task summary>" --areas <comma,separated,paths>

Check peers:

    "$P/scripts/agent-presence" list
```

**Safety note**: announce is advisory and secondary — if the agent skips it, P0+P1 still
record liveness and write-area claims automatically. The nudge is the human-intent layer,
not a safety dependency.

---

## Hook wiring

### `.codex/hooks.json` entries (project-local, real Codex schema)

Add the presence hooks to the **project-local** `.codex/hooks.json` — the same tracked
file that already carries the Git-policy guard — using the **real Codex hook schema**:
Pascal-case event names under a top-level `"hooks"` object, each event a list of matcher
groups whose `"hooks"` array holds `{"type": "command", ...}` handlers. (An earlier draft
used a flat `pre_tool_use` / `name` / `command` shape; that is **not** valid Codex schema.
The shape below matches the working git-guard entry and the Codex docs.)

Command paths are resolved from the common-dir at run time, so one tracked file works from
every worktree and on any machine with **no hardcoded absolute paths**. (The command runs
in the session's cwd, which is inside the repo, so `git rev-parse` resolves correctly even
if this lived in a global `~/.codex/hooks.json`.)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "\"$(dirname \"$(git rev-parse --path-format=absolute --git-common-dir)\")/scripts/git_policy/presence_hook.sh\" register",
            "timeout": 5000,
            "statusMessage": "Registering presence"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "apply_patch|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(dirname \"$(git rev-parse --path-format=absolute --git-common-dir)\")/scripts/git_policy/codex_claim_guard.py\"",
            "timeout": 5000,
            "statusMessage": "Auto-declaring write area"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(dirname \"$(git rev-parse --path-format=absolute --git-common-dir)\")/scripts/git_policy/codex_presence_flush.py\"",
            "timeout": 5000,
            "statusMessage": "Presence heartbeat / announce flush"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "\"$(dirname \"$(git rev-parse --path-format=absolute --git-common-dir)\")/scripts/git_policy/presence_hook.sh\" deregister",
            "timeout": 5000,
            "statusMessage": "Deregistering presence"
          }
        ]
      }
    ]
  }
}
```

Notes:
- Keep the existing Git-policy `PreToolUse` group; add `codex_claim_guard.py` as a second
  group (or a second handler in the same group), do not replace it.
- **Project-local vs global**: project-local `.codex/hooks.json` travels with the repo and
  needs no per-machine file, but is subject to the per-hash trust gap (F6) that **P4**
  closes by policy — this matches how the git-guard is already deployed across the three
  branches. A global `~/.codex/hooks.json` is trusted once per machine but is a per-machine
  file to install; either way, use the common-dir command resolution above (never hardcode
  paths). Prefer project-local + P4.
- The nested `$(...)` quoting inside a JSON string is finicky; validate the exact escaping
  against a live Codex session (V7) before relying on it.
- **stdin to register/deregister** (V3): `presence_hook.sh` passes `"$@"` to
  `agent_presence.py` and inherits stdin, and `register`/`deregister` fall back to
  `_session_from_stdin()` when no env identity is present. Confirm Codex delivers the hook
  payload on stdin for SessionStart/Stop so the session id resolves; `codex_claim_guard.py`
  and `codex_presence_flush.py` read stdin independently.

---

## File change summary

| File | Action | Notes |
|------|--------|-------|
| `scripts/git_policy/codex_claim_guard.py` | **Create** | P1: apply_patch PreToolUse guard (parse patch body; `session:<id>` who-key) |
| `scripts/git_policy/codex_presence_flush.py` | **Create** | P0/P2: heartbeat every PostToolUse; flush staging when present |
| `scripts/agent-codex-announce` | **Create** | P2: sandboxed staging shim (writes `$TMPDIR` payload) |
| `scripts/git_policy/agent_presence.py` | **Edit** | P3: `_session_from_env()` — CODEX_THREAD_ID first |
| `scripts/agent-presence` | **Edit** | F-A: common-dir based path resolution |
| `.codex/hooks.json` | **Edit** | P0/P1/P2: wire SessionStart/PreToolUse/PostToolUse/Stop (real schema, common-dir paths) |
| `AGENTS.md` | **Edit** | F-B: announce nudge (worktree-independent invocation) |
| `requirements.toml` (or equivalent) | **Edit/Create** | P4: managed hook trust (pending V1) |

All new/edited scripts are **master-owned** (the presence layer lives only on `master`,
F7) and must be created/committed there.

---

## Success criteria

1. A live Codex session appears on the roster returned by
   `scripts/agent-presence list` (visible to Claude peers), from any worktree.
2. When a Codex session edits a file via apply_patch, a claims entry attributed to
   `session:<id>` appears on the board within the edit's PreToolUse round-trip.
3. If a Claude session holds a claim on a file and a Codex session issues apply_patch
   on the same file, the Codex PreToolUse hook prints a conflict warning to stderr.
4. `scripts/agent-presence announce` and `scripts/agent-presence list` work correctly
   from specwork and trainex linked worktrees for both Claude and Codex sessions (F-A).
5. **Liveness**: a Codex session doing only non-edit activity stays on the roster for the
   duration of that activity (heartbeat fires on every PostToolUse); on **clean exit** its
   presence file and claims are removed promptly (Stop→deregister); on **crash** they are
   released by the 20-minute presence sweep, not left to the 2-hour claims expiry.
6. A proactive `announce` issued by a Codex session in any worktree lands on the board by
   the PostToolUse of that same call (summary visible in `list`).
7. No hook fires silently due to trust gaps: all presence hooks are trusted-by-policy
   across all three worktrees (master, specwork, trainex).

---

## Open verification items (not blockers for the design; must be resolved before plan execution)

| # | Item | Resolution path |
|---|------|-----------------|
| V1 | Confirm `requirements.toml` managed-hook trust mechanism for Codex 0.142 | Read Codex changelog / docs; fall back to a per-worktree `/hooks` trust setup script if unavailable |
| V2 | Confirm exact `tool_name` emitted for apply_patch in 0.142 (`"apply_patch"` vs `"Edit"` vs other) and the precise patch-body markers | Run an interactive Codex session with a PostToolUse logging hook; capture a real `tool_input.command` |
| V3 | Confirm `presence_hook.sh` stdin forwarding is compatible with Codex SessionStart/Stop payload delivery | Trace a SessionStart event through `presence_hook.sh` in an interactive session |
| V4 | Confirm `$TMPDIR` is the **same path** for both the sandboxed model-shell and the unsandboxed flush hook (and is not excluded) | Probe in a real Codex session; if not clean, switch P2 staging to a `.gitignore`d workspace-relative dir |
| V5 | Lock the identity equality `CODEX_THREAD_ID == hook session_id` with a test | Add a test that registers via a simulated hook payload and announces via env, asserting one roster entry |
| V6 | Subagent identity: do Codex subagent shells expose the parent `session_id` as `CODEX_THREAD_ID`? Should subagents announce at all? | Probe a subagent; decide whether to disable announce in subagents |
| V7 | Validate the `.codex/hooks.json` schema, matcher tokens (`startup\|resume`, `apply_patch\|Edit\|Write`, `.*`), and the nested-`$(...)` command quoting against running Codex | Install entries in a trusted test worktree; confirm each hook fires and resolves the master script path |
| V8 | Confirm the current, independent trust gap (F6) — is the Git-policy guard actually not firing for Codex in specwork/trainex today? | Inspect `~/.codex/config.toml [hooks.state]`; trust or policy-manage as a standalone fix |
