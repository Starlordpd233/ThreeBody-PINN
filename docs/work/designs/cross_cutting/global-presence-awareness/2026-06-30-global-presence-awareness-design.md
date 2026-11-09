---
status: active
purpose: design
created: 2026-06-30
milestone: untracked
phase: cross-cutting
retirement_trigger: The global presence layer is implemented (module + wrapper + launcher installed under ~/.claude/hooks/, all active profiles wired, -alt migrated off the repo script) and its operating contract is folded into docs/git-guidelines.md. Then follow docs/README.md retirement (mark consumed or propose archive with a README mirroring the predecessor at docs/archive/work/designs/cross_cutting/presence-overlap-awareness/).
---

# Global Presence Awareness — Design Spec

> **Audience:** the agent that implements this (likely launched from this repo, but the
> system it builds lives in `~/.claude/`, outside the repo). This document is
> self-contained: it captures the investigation, the locked decisions, the exact target
> architecture, and the traps to avoid. Read it in order before writing any code or
> editing any `settings.json`.

## 0. How to use this document

1. Read §1–§4 to understand **why** (intent, what was found, the core principle, the
   locked decisions — do **not** re-litigate the decisions in §4).
2. Read §5 for the **current-state ground truth**, then **re-verify it at implementation
   time** with the commands given — profile sets drift.
3. Implement §6–§8. Respect the **do-not-touch list** in §9.
4. Run §11 verification before declaring done.
5. Obey §12 (risks) at every step — most of the cost of this task is in §12, not §6.

This is a **design spec, not final code**. Code blocks here are contracts (signatures,
schemas, exact JSON to merge). The implementing agent writes the real module; it must
match these contracts.

---

## 1. Intent (the problem being solved)

The user wants the **presence awareness** mechanism to apply to **all Claude Code
sessions, regardless of where Claude is working** — not just inside the 3-body-problem
repo. Their words: "it should not be a project-level design."

The investigation (2026-06-30) confirmed the existing system is **repo-scoped**, and
that this was **deliberate in the original design**, not an oversight. So the global
intent was never captured before. This spec defines the missing global layer.

---

## 2. What was found (investigation synthesis)

Three concrete facts make the current system repo-scoped. Each is a file you can point
at; the implementing agent should re-confirm they still hold:

1. **The SessionStart hook lives in the project, not globally.** The project
   `.claude/settings.json` wires `scripts/session_banner.sh`, which calls
   `agent_presence.py register`. The global `~/.claude/settings.json` has four
   SessionStart hooks (`context-mode-cache-heal`, three `gsd-*`); **presence is not
   among them.** No other project fires it.
2. **The scripts live inside this repo** and are located via
   `git rev-parse --show-toplevel` (`scripts/session_banner.sh:6`,
   `scripts/agent-presence:4`). Another project does not contain these files.
3. **The registry state is stored inside the repo's `.git`.**
   `scripts/git_policy/agent_presence.py` puts presence files under
   `$(git rev-parse --git-common-dir)/agent-presence/`, and the claims board it sits on
   does the same (`scripts/git_policy/agent_claims.py` → `…/agent-claims/`). So two
   different repos keep **completely separate** rosters, and the code hard-requires git
   on every entry point (in a non-git folder it silently no-ops).

The predecessor design doc (now archived) confirms this scope was intentional: its whole
motivation is parallel agents *within this repo* — per-track worktrees, same-worktree /
same-branch file-collision weighting, "cross-worktree" meaning *other worktrees of the
same repo* (confirmed by the user 2026-06-26). It never claims to cover other projects.

### Half-built global attempt already in `~/.claude-alt`

`~/.claude-alt/settings.json` **already** wires `SessionStart → register` and
`SessionEnd → deregister`, but pointing at the **repo-resident**
`scripts/git_policy/presence_hook.sh`, which forwards to the repo's git-coupled
`agent_presence.py`. So it runs from the `-alt` profile but **only works inside a git
repo**, and the script physically lives in this repo. The other active profiles have no
presence wiring at all. The global layer defined here **replaces** the `-alt` wiring
with a clean, git-decoupled module (see §7, §12-risk-7).

---

## 3. Core principle: presence vs. overlap generalize differently

This is the single most important idea in the doc. Two different features are bundled
in the repo system; only one generalizes to global scope:

- **Presence** — *"who is alive right now and what are they working on?"* — generalizes
  cleanly to global. Value is preserved (machine-wide awareness across all projects).
- **Overlap** — *"are we about to edit the same file?"* — does **not** generalize. File
  collisions only matter inside a shared workspace; two sessions in two different repos
  cannot clobber each other's files. The claims board uses repo-relative paths by
  design. A "global overlap" feature is mostly noise.

**Consequence:** the global layer is **presence-only**. It deliberately drops the
claims-board / `--areas` overlap machinery. The repo layer keeps that machinery, because
that is where file collision is meaningful.

---

## 4. Locked decisions (do not re-litigate)

These were decided with the user on 2026-06-30:

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Architecture | **Add a global presence-only layer; keep the repo system untouched.** | Presence goes machine-wide; repo claims/overlap/guard stay for in-repo collision. Two clean layers, no regression. |
| D2 | Coverage breadth | **Everywhere (incl. non-git dirs) × all profiles.** | Matches "regardless of where Claude is working"; the global layer must not depend on git or on a single profile. |

### Recommended defaults on two sub-decisions (reversible; confirm before building)

- **S1 — Heartbeat hook: OFF by default.** Do **not** add a `PostToolUse` heartbeat hook
  in the first pass. The stale-floor reaper (§6) handles dead sessions. Rationale: less
  hook surface, less churn; can add later if rosters feel stale.
- **S2 — Commit the docs note: YES.** The single `docs/git-guidelines.md` contract update
  (§10) is committed as one atomic `docs(governance)` commit, per repo policy. The new
  global scripts live **outside** the repo and are **not** committed here.

---

## 5. Current-state ground truth (re-verify at implementation time)

### 5.1 Active Claude profiles

Re-verify with `ls -d ~/.claude*` before editing anything. As of 2026-06-30 the active
profiles with hooks are:

| Profile dir | Has hooks? | Current presence wiring |
|---|---|---|
| `~/.claude` (default) | yes | **none** |
| `~/.claude-alt` | yes | repo-pointed: `presence_hook.sh register` (SessionStart) + `deregister` (SessionEnd) — **replace** |
| `~/.claude-free` | yes | **none** |
| `~/.claude-max` | yes | **none** |
| `~/.claude-mem` | **no** (utility profile, no hooks) | skip |

> **Memory note:** older memory references profiles `~/.claude-glm`, `~/.claude-kimi`,
> `~/.claude-qwen`, `~/.claude-xiaomi`. They have **been torn down** and no longer
> exist. Do not trust stale memory — re-run `ls -d ~/.claude*` and wire whatever real
> profile dirs with hooks you find.

Each profile has its **own real (non-symlink) `hooks/` directory** with its own copies of
the `gsd-*` and `context-mode` hooks. The global layer does **not** copy into each
profile's hooks dir; it lives **once** at `~/.claude/hooks/` and is referenced by
**absolute path** from every profile's `settings.json` (one source of truth; see §12-risk-3).

Node binary used by existing hooks (use the same for any JS, though the global module is
Python): `<home>/.local/share/node-v24.16.0-darwin-arm64/bin/node`.

### 5.2 Repo layer (the "do-not-touch" set — see §9)

Files, all under this repo:

- `scripts/session_banner.sh` — SessionStart banner; calls repo `agent_presence.py register`.
- `scripts/agent-presence` — repo wrapper (agent-facing `announce`/`list`).
- `scripts/git_policy/agent_presence.py` — repo presence module (git-coupled, claims-integrated).
- `scripts/git_policy/agent_claims.py` — claims board (repo-local state under git common-dir).
- `scripts/git_policy/presence_hook.sh` — repo launcher currently mis-used by `~/.claude-alt`.
- `scripts/git_policy/claim_guard.py` — PreToolUse edit-claim guard.
- `scripts/agent-commit` — commit-time owned-paths hard backstop.
- project `.claude/settings.json` — PreToolUse guards + SessionStart banner wiring.

Repo layer state dirs: `<repo>/.git/agent-presence/` and `<repo>/.git/agent-claims/`.
The global layer uses a **different** state dir (`~/.claude/agent-presence/`), so the two
never collide (§9).

### 5.3 Confirmed Claude Code hook facts (no guessing needed)

- **`SessionEnd` is a valid hook type** — already used by `~/.claude-alt` for deregister.
- **Hook scripts receive the session id on stdin** as JSON (`.session_id`).
- **`CLAUDE_ENV_FILE`** is the mechanism to seed `CLAUDE_CODE_SESSION_ID` so later
  Bash-tool calls (e.g. `announce`) can read identity — mirror `scripts/session_banner.sh`.

---

## 6. Target architecture

A single **git-decoupled, profile-agnostic presence module**, installed once under
`~/.claude/hooks/`, referenced by absolute path from every active profile. Presence-only.

### 6.1 Files to create (all outside the repo)

| Path | Kind | Purpose |
|---|---|---|
| `~/.claude/hooks/agent_presence_global.py` | Python module | The presence engine. CLI: `register\|deregister\|announce\|list\|heartbeat`. Advisory, fail-open. |
| `~/.claude/hooks/agent-presence-global` | bash wrapper | Agent-facing CLI. Seeds `CLAUDE_CODE_SESSION_ID` from env, forwards to the module. This is what the "announce your task" nudge points at. |
| `~/.claude/hooks/presence_global_hook.sh` | bash launcher | SessionStart/SessionEnd hook entrypoint: reads session id from stdin, seeds `CLAUDE_ENV_FILE`, calls `register`/`deregister`, prints a one-line global roster nudge. |

### 6.2 State

- **Dir:** `~/.claude/agent-presence/` — one JSON file per live session, named
  `<session_id>.json`. **Fixed absolute path**, profile-agnostic (this is *mandatory*;
  see §12-risk-2). Env override: `AGENT_PRESENCE_GLOBAL_DIR`.
- **Key:** the Claude session id (globally unique across profiles → no key collision).
- **Atomic writes:** `tmp` + `os.replace` (mirror repo module).

### 6.3 State-file schema (concrete)

```json
{
  "session_id": "<claude-session-uuid>",
  "pid": <int|null>,
  "worktree": "<basename of repo root, or cwd basename in non-git>",
  "branch": "<git branch, or \"(no-git)\">",
  "repo_root": "<absolute repo root, or null in non-git>",
  "cwd": "<absolute working directory at register time>",
  "profile": "<basename of the active CLAUDE_CONFIG_DIR, e.g. \".claude\" or \".claude-alt\">",
  "start_time": <unix epoch seconds>,
  "task_summary": "<plain-text task, or null>",
  "last_heartbeat": <unix epoch seconds>
}
```

The `profile`, `repo_root`, and `cwd` fields are **new** vs. the repo schema — they
exist so the global roster can group/mark peers (§6.6).

### 6.4 `agent_presence_global.py` — contract

Same shape and advisory discipline as the repo module, with three differences:

| Concern | Repo `agent_presence.py` | Global `agent_presence_global.py` |
|---|---|---|
| State dir | `$(git rev-parse --git-common-dir)/agent-presence/` | `~/.claude/agent-presence/` (fixed; env override `AGENT_PRESENCE_GLOBAL_DIR`) |
| Git dependency | hard-required (fails open outside git) | **optional** — git used only for display; falls back to cwd basename / `(no-git)` |
| Claims board | sits on `agent_claims.py`; `announce --areas` claims paths | **none** — must not import `agent_claims`; `announce` takes a summary **only** |
| Scope | one repo (worktrees share via git common-dir) | machine-wide, all profiles |
| Roster | same-repo; cross-worktree marked | machine-wide; cross-project marked; profile tag shown |

Required behavior (carry over from the repo module unless overridden here):

- **CLI:** `register | deregister | announce <summary> | list | heartbeat` — always exits `0`.
- **Identity resolution:** `_session_from_env()` (`CLAUDE_CODE_SESSION_ID`) →
  `_session_from_stdin()` (JSON `.session_id`). Safe-id guard:
  `^[A-Za-z0-9._-]+$` (reject anything else silently).
- **`register`:** write/refresh entry with pid (`os.getppid()`), git-or-cwd context,
  `profile`, fresh `last_heartbeat`; then `sweep`; then print the roster (excluding self).
- **`announce <summary>`:** set `task_summary`, refresh heartbeat, print roster. **No
  path claiming.**
- **`heartbeat`:** bump `last_heartbeat` only.
- **`deregister`:** delete the entry; release nothing on a claims board (there is none).
- **`sweep` (reaper):** on every `register`/`list`/`announce`, walk the dir; for each
  entry, if pid trusted-alive → keep; otherwise reap when
  `now - last_heartbeat > stale_floor`. See §12-risk-5 for the pid caveat.
- **Constants:** `FRESH_SECONDS = 120`; stale floor `AGENT_PRESENCE_STALE` default
  `1200` (20 min). (Mirror repo defaults; a separate `AGENT_PRESENCE_GLOBAL_STALE` may
  be added if global reaping should diverge — optional.)
- **Fail-open:** every public entry wrapped so any exception → exit `0`. A presence bug
  must never block a session or a hook.

### 6.5 Roster presentation (global)

Group/mark so the machine-wide roster stays scannable:

- **Same project** peers (same `repo_root`, or same `cwd` when non-git) listed first,
  unmarked — these are the ones that could actually collide with you.
- **Other-project** peers marked `[other-project]`.
- Each line shows the short session id, `worktree / branch`, the `profile` tag (so you
  can see which profile a peer runs under), the `task_summary`, and heartbeat freshness
  (`fresh` or `Nm`).
- **SessionStart banner is one concise line** (e.g. `global presence: N other session(s)
  across M project(s); run agent-presence-global announce "<task>"`) — it must not be
  noisy printed right after the repo's own multi-line banner. The full roster prints on
  `list` / `announce`, not on every SessionStart.

Suggested line format:

```
  [<sid4>] <worktree> / <branch>  (.<profile>)  [other-project] — "<summary>"  ♥ fresh
```

### 6.6 Cross-cutting behaviors

- **Non-git directory:** registers with `branch="(no-git)"`, `repo_root=null`,
  `worktree=<cwd basename>`, `cwd=<absolute>`. Still appears in the roster. This is what
  satisfies "regardless of where Claude is working."
- **Cross-profile:** all profiles read/write the **same** `~/.claude/agent-presence/`.
  Session ids are globally unique, so no key collision; the `profile` field lets the
  roster show which profile a peer is running under.
- **Cross-project:** grouping + `[other-project]` mark (§6.5). We group/mark; we do
  **not** partition the registry by project.

---

## 7. Profile wiring (exact edits)

> Editing these files affects **every Claude session the user runs**. See §12 before
> touching them. Back up each file first.

### 7.1 Snippet to merge into each profile's `settings.json`

Add a new block to `hooks.SessionStart` and add a `hooks.SessionEnd` block. Both call the
launcher by **absolute path** (identical in every profile):

```json
"SessionStart": [
  { "hooks": [ { "type": "command",
      "command": "bash \"<home>/.claude/hooks/presence_global_hook.sh\" register" } ] }
],
"SessionEnd": [
  { "hooks": [ { "type": "command",
      "command": "bash \"<home>/.claude/hooks/presence_global_hook.sh\" deregister" } ] }
]
```

Append the SessionStart block to the profile's **existing** SessionStart blocks — do not
replace them. (Optional, off by default per S1: a `PostToolUse` `Write|Edit` block calling
`… presence_global_hook.sh heartbeat`.)

### 7.2 Per-profile actions

| Profile | Action |
|---|---|
| `~/.claude` | Add SessionStart(register) + SessionEnd(deregister). |
| `~/.claude-free` | Add SessionStart(register) + SessionEnd(deregister). |
| `~/.claude-max` | Add SessionStart(register) + SessionEnd(deregister). |
| `~/.claude-alt` | **Remove** the two existing repo-`presence_hook.sh` lines (SessionStart register + SessionEnd deregister); **add** the global register/deregister blocks above. Net effect: `-alt` stops depending on the repo script. |
| `~/.claude-mem` | Skip (no hooks profile). |

Use a JSON parse→merge→write (Python `json`), not string editing, so existing
`gsd-*`/`context-mode`/`Stop`/`SubagentStop` blocks and key order are preserved.

---

## 8. `presence_global_hook.sh` and `agent-presence-global` — contracts

### 8.1 `presence_global_hook.sh` (SessionStart / SessionEnd entrypoint)

Mirror `scripts/session_banner.sh`'s identity-seeding block, but git-decoupled and
presence-only:

1. Read stdin JSON only if not a tty; extract `session_id`.
2. If `CLAUDE_ENV_FILE` is set, append
   `export CLAUDE_CODE_SESSION_ID=<sid>` to it (idempotently) so later Bash-tool calls
   resolve identity.
3. Forward `$1` (`register` | `deregister`) to `agent_presence_global.py` with
   `CLAUDE_CODE_SESSION_ID` exported.
4. On `register`: print the one-line global nudge (§6.5).
5. Always `exit 0`. All best-effort; failures swallowed.

### 8.2 `agent-presence-global` (agent-facing CLI wrapper)

Mirror the repo's `scripts/agent-presence` wrapper:

```sh
#!/usr/bin/env bash
set -euo pipefail
exec python3 "$HOME/.claude/hooks/agent_presence_global.py" "$@"
```

It must rely on `CLAUDE_CODE_SESSION_ID` (seeded into `CLAUDE_ENV_FILE` by the SessionStart
launcher) for identity, exactly as the repo wrapper does.

---

## 9. Coexistence with the repo layer (and the do-not-touch list)

- **Two separate state dirs** → no collision. Inside this repo a session registers in
  **both** layers: the repo roster (rich, with overlap/claims) **and** the global roster
  (everyone, machine-wide). This is expected, not a bug.
- **Banner ordering:** the global nudge is one line (§6.5) so it doesn't clutter the
  repo's multi-line banner.
- **Do not modify** any file in §5.2. The repo layer is intentionally left as-is; its
  git-coupling and claims integration are correct for its purpose.
- **Do not import** repo code (`agent_claims.py`, `agent_presence.py`) from the global
  module — that would re-introduce git coupling and repo-local path claims.

---

## 10. Docs update (the only repo-side change)

Add a subsection to `docs/git-guidelines.md` → "Presence & overlap awareness
(advisory)" documenting the **global presence layer**: scope (machine-wide, all
profiles, non-git-capable), state location (`~/.claude/agent-presence/`),
presence-only vs. repo-local overlap, and the agent-facing CLI
(`agent-presence-global announce/list`). Commit as one atomic `docs(governance)` commit
(per S2), via `scripts/agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS` set to
`docs/git-guidelines.md`. The new global scripts under `~/.claude/` are **not** committed
in this repo.

---

## 11. Verification plan (run before declaring done)

1. **Non-git registration.** From a temp non-git dir:
   ```sh
   d="$(mktemp -d)"; cd "$d"
   printf '{"session_id":"probe-non-git-1"}' | python3 ~/.claude/hooks/agent_presence_global.py register
   cat ~/.claude/agent-presence/probe-non-git-1.json   # expect branch "(no-git)", repo_root null
   python3 ~/.claude/hooks/agent_presence_global.py deregister   # cleanup (needs CLAUDE_CODE_SESSION_ID set, or pass via stdin)
   ```
2. **Cross-profile visibility.** With one session live under `~/.claude` and another
   under `~/.claude-alt` (different `CLAUDE_CONFIG_DIR`), run `agent-presence-global list`
   from either → each must see the other, tagged with its profile.
3. **Repo-layer regression.** Inside `3_body_problem`, confirm `scripts/agent-presence list`
   still works and `<repo>/.git/agent-presence/` still populates — i.e. the repo layer is
   untouched and healthy.
4. **`-alt` migration.** Confirm `~/.claude-alt/settings.json` no longer references the
   repo `presence_hook.sh`, and now references the global launcher; `-alt` registers into
   `~/.claude/agent-presence/`, not the repo's `.git/`.
5. **SessionEnd cleanup.** Trigger `deregister` → global file removed. Simulate a crash
   (kill -9 / no SessionEnd) → confirm the stale-floor reaper removes the entry on the
   next `register`/`list`/`announce`.
6. **Fail-open.** Run the module from a broken context (e.g. unset HOME, read-only state
   dir) → it must exit `0` and emit nothing harmful.

---

## 12. Risks — things to be careful about (read carefully)

1. **Editing global `settings.json` affects every Claude session.** Back up each file
   (`cp settings.json settings.json.bak-$(date +%Y%m%d)`) before editing. Use JSON
   parse→merge→write; preserve existing blocks and key order. Never `--no-verify` or
   bypass hooks.
2. **State dir MUST be a fixed absolute path** (`~/.claude/agent-presence/`), **not**
   `$CLAUDE_CONFIG_DIR`-relative. If each profile wrote to its own config dir, profiles
   would not share the roster and cross-profile awareness would silently fail.
3. **One source of truth for the script.** Install the module/wrapper/launcher **once**
   at `~/.claude/hooks/`. Reference it by absolute path from every profile. Do **not**
   copy it per-profile — copies drift. After wiring, grep each profile's `settings.json`
   to confirm it actually points at the global launcher.
4. **Fail-open discipline is non-negotiable.** Every entry point wraps exceptions →
   `exit 0`. Presence is advisory; a bug here must never block a session or a hook.
5. **The pid caveat (carry over from the repo module).** In `register`, `os.getppid()`
   captures the **transient SessionStart shell**, not the long-lived Claude process — so
   `pid`-liveness is unreliable as a "trusted-live" shortcut. Do **not** add "reap on
   sight if pid is dead." Carry over the repo module's reaping behavior: when pid is
   absent/dead/untrusted, fall through to the **heartbeat-stale floor** before reaping.
   Active sessions keep `last_heartbeat` fresh via `register`/`announce`/`heartbeat`, so
   an active session is never reaped. (See repo `agent_presence.py` comments on the
   reaping table, "row 3".)
6. **SessionEnd is not guaranteed** (kill -9, laptop force-quit, crash). The
   stale-floor reaper is the backstop. Keep `sweep` on every `register`/`list`/`announce`.
7. **Migrate `-alt` off the repo script.** The current `-alt` wiring points at
   `scripts/git_policy/presence_hook.sh`. Replacing it (§7.2) is a strict improvement
   (works outside git, no repo-path dependency). Do not leave both wirings in place.
8. **Do not depend on repo `agent_claims.py`** at the global layer. It is repo-local and
   path-keyed; importing it re-introduces git coupling and cross-project path claims that
   do not compose.
9. **Re-verify the profile set at implementation time.** `ls -d ~/.claude*`. Memory
   references glm/kimi/qwen/xiaomi profiles that have been torn down; do not wire ghosts.
10. **Only the docs note is a repo change.** The new scripts live outside the repo and
    are not `git add`-ed here. Stage `docs/git-guidelines.md` explicitly; never
    `git add .`/`-A` (repo policy).
11. **Public-release mindfulness.** Paths in scripts are the user's own `~/.claude` —
    fine. Do not embed secrets, tokens, or machine-specific credentials in any new file.
12. **JSON merge must not clobber.** Appending the global SessionStart block must not
    reorder or drop the existing `gsd-*` / `context-mode` / `Stop` / `SubagentStop`
    hooks. For `-alt`, the removal of the two repo-`presence_hook.sh` lines and the
    addition of the global lines must be one coherent edit.

---

## 13. Non-goals

- **Cross-machine presence.** This is per-machine shared-filesystem state. Two laptops do
  not share a roster.
- **Global claims / overlap detection.** Intentionally not built (§3).
- **Replacing the repo layer.** The repo system stays.
- **Watchdog / cross-session-wakeup integration.** Separate system
  (`cross-session-watchdog` skill; the watchdog design is its own track).
- **Per-project isolation within the global registry.** We group and mark; we do not
  partition.

---

## 14. References

- Predecessor design (archived):
  `docs/archive/work/designs/cross_cutting/presence-overlap-awareness/2026-06-22-presence-overlap-awareness-design.md`
  (+ its `README.md`).
- Companion implementation plan (archived):
  `docs/archive/work/plans/cross_cutting/presence-overlap-awareness/2026-06-22-presence-overlap-awareness-implementation-plan.md`.
- Repo presence module: `scripts/git_policy/agent_presence.py` — esp. `presence_dir`,
  `sweep_presence`, and the reaping comments (the pid-caveat source).
- Repo claims board: `scripts/git_policy/agent_claims.py`.
- Repo SessionStart banner (identity-seeding pattern to mirror):
  `scripts/session_banner.sh`.
- Repo launcher currently mis-used by `-alt`: `scripts/git_policy/presence_hook.sh`.
- Repo PreToolUse guard: `scripts/git_policy/claim_guard.py`.
- Operating contract to extend: `docs/git-guidelines.md` → "Presence & overlap awareness
  (advisory)".
- Settings files to edit: `~/.claude/settings.json`,
  `~/.claude-alt/settings.json`, `~/.claude-free/settings.json`,
  `~/.claude-max/settings.json`.

---

## 15. Lifecycle note for the implementing agent

When the global layer is built and its contract is folded into `docs/git-guidelines.md`,
this design doc's `retirement_trigger` is satisfied. At that point follow `docs/README.md`:
mark this file `consumed` (or propose archive with a README mirroring the predecessor's
archive README). Do **not** delete without the reference audit + user approval described
in `docs/README.md`.
