---
status: archived
archived_at: 2026-06-27
purpose: design
created: 2026-06-22
milestone: untracked
phase: cross-cutting
retirement_trigger: Retire when the Presence & Overlap Awareness system is implemented and its operating contract is folded into docs/git-guidelines.md, or when superseded by a consolidated parallel-agent-coordination design.
---

# Presence & Overlap Awareness — Design

## Summary

A passive, advisory system that lets a starting agent answer one question before it
begins work: **"Who else is alive right now, and does their in-flight work overlap
mine?"** It adds a lightweight **presence registry** (one small file per live session)
on top of the existing **claims board** (`scripts/git_policy/agent_claims.py`), and a
short **agent-driven reasoning step** that reads the roster, compares it against the
agent's own intended work, and coordinates, defers, or proceeds according to a
graduated-autonomy protocol.

It is built in two layers:

1. **Mechanical lifecycle** — fully automatic via hooks. Sessions register at start,
   heartbeat on every edit, and deregister at stop. No daemon, no polling, no
   user action.
2. **Semantic reasoning** — agent-driven. After the first prompt the agent runs one
   CLI call to announce its task in plain language, then reasons about overlap. This is
   judgment, not a lock.

The system is **advisory only**. The commit-time owned-paths net in `scripts/agent-commit`
remains the single hard backstop; nothing here can block a commit.

## Motivation: the missing middle

The repo already coordinates parallel agents along two structural seams (Part A of the
[parallel-agent coordination design](../parallel-agent-coordination/2026-06-17-parallel-agent-coordination-design.md)):

- **Per-track worktrees** keep independent tracks on separate branches.
- **The claims board** records, per file path, `{who, area, why, when}` so a second
  agent editing the same file gets a warning (`claim_guard.py`), with the commit-time
  owned-paths check as the hard backstop.

Both seams answer **"are we about to edit the same file?"** Neither answers **"are we
doing the same *task*?"** Two agents can pursue a semantically identical or overlapping
goal while touching *different* files — and today that collision is only discovered
**after** the duplicate work exists.

This was observable live while writing this very document. The claims board held eight
records; to judge whether any peer's work overlapped, the author had to read eight
hash-named JSON files and **infer** intent from file paths alone — "this session is on
Phase 32 / trainex planning" — because the board records *areas* but **no statement of
intent**. That inference step is the gap. The unlocking new datum is a single
**natural-language task summary per live session**, which a starting agent can read and
reason about directly.

This design is the **missing middle**: the layer between Part A's structural,
file-granular claims and the (separately parked) cross-session watchdog. It is **not**
the watchdog — see Non-goals.

## Scope

### Goals

- Make every live top-level session **discoverable** with a one-line task summary,
  worktree, branch, and liveness.
- Give a starting agent a **roster** at session start and a **one-call** way to announce
  its own task.
- Provide a **graduated-autonomy protocol** for what to do when the agent's intended
  work overlaps a peer's — distinguishing same-file write contention from semantic task
  duplication.
- Reuse the claims board as the single source of truth for "who writes what"; presence
  is a *frontend* to it, not a parallel mechanism.

### Non-goals

- **Not the cross-session watchdog.** No agent is ever auto-activated, woken, or
  signalled. No daemon, no `tmux send-keys`, no cron, no cross-session invocation. The
  watchdog is a separate, parked effort
  (`docs/work/plans/cross_cutting/parallel-agent-coordination-watchdog/`).
- **Not a re-implementation of Part A.** The claims board, `claim_guard.py`, and the
  commit-time net already exist and are unchanged in contract. Presence sits on top.
- **Not a lock.** No verdict here blocks an edit or a commit. The hard backstop stays
  the owned-paths check in `agent-commit`.
- **No sub-file granularity.** Claims and overlap are file-granular (see Decision R1).

## Architecture

```
SessionStart hook ─▶ agent-presence register ──▶ writes <session_id>.json, sweeps stale, prints roster
                                                        │
Edit/Write hook ──▶ claim_guard.py ──┬─▶ agent_claims.claim(area)   (existing: auto-declare)
                                     └─▶ agent_presence.heartbeat()  (new: bump last_heartbeat)
                                                        │
agent (after 1st prompt) ─▶ agent-presence announce "<summary>" --areas a,b,c
                                     └─▶ sets task_summary + agent_claims.claim() per area
                                     └─▶ agent reasons over roster (graduated-autonomy protocol)
                                                        │
Stop hook ────────▶ agent-presence deregister ──▶ releases this session's claims, removes <session_id>.json
```

Two state stores, both under the **shared** git common directory so all worktrees see
the same picture:

- `"$(git rev-parse --git-common-dir)/agent-claims/` — **existing.** Source of truth for
  "who writes what." One file per area, name = `sha1(area)[:16]`.
- `"$(git rev-parse --git-common-dir)/agent-presence/` — **new.** Liveness + intent. One
  file per session, name = `<session_id>.json`.

The two stores **join on the same identity key**, `session:<session_id>` (see Identity).

## The presence registry

### Location and identity

- Directory: `"$(git rev-parse --git-common-dir)/agent-presence/"` (created lazily;
  shared across worktrees, exactly like `agent-claims/`).
- One file per **top-level session**: `<session_id>.json`.
- **Identity = `session:<session_id>`**, taken from the Claude Code hook payload's
  `session_id` field — the *same* key `claim_guard.py` already writes via
  `AGENT_CLAIM_WHO = f"session:{session}"`. This is what makes presence and claims
  joinable: a session's claimed areas are exactly the claim records whose `who` equals
  its presence key.

### Persisted schema

```json
{
  "session_id": "<uuid>",
  "pid": 12345,
  "worktree": "specwork",
  "branch": "milestone/v1.6",
  "start_time": 1782058000,
  "task_summary": null,
  "last_heartbeat": 1782058600
}
```

- `pid` — captured at register via `getppid()` (see verification item #2). Used by the
  `kill -0` liveness check.
- `task_summary` — `null` until the agent runs `announce`; then a one-line plain-language
  description of the task.
- `last_heartbeat` — epoch seconds, bumped on every edit by the `claim_guard` hook.

**Claimed areas are derived, not persisted** (refinement of the original sketch, flagged
for review — see Open Decisions). The original schema carried a `claimed_areas: []`
field. Because `announce` and `claim_guard` both write to the **claims board**
immediately, a session's claimed areas are already fully represented there. The roster
therefore **derives** each session's areas by scanning the board and grouping records by
`who` — keeping the board the single source of truth and eliminating any chance of the
presence file drifting out of sync with reality. The presence file owns only liveness and
intent.

### Atomicity

All writes use the `tmp` + `os.replace` pattern already in `agent_claims.py` (write to a
temp file in the same directory, then atomically rename over the target). No partial reads.

## Liveness and reaping

The claims board deliberately does **not** test process liveness — its records are
written by short-lived edit-hook processes with no persistent PID, so it relies on a
time-based TTL plus explicit release. Presence is different: a session *is* a persistent
process, so we can test it directly, the way `agent-commit`'s lock does
(`kill -0 <pid>`).

Reaping policy (applied lazily during `sweep`, on every `register`/`list`):

| Condition | Action |
|---|---|
| `pid` alive (`kill -0` succeeds) | **Keep.** Even if the heartbeat is old — an open, idle session is genuinely present and may resume. Render as `idle (♥ 23m)`. **Never** reaped for idleness. |
| `pid` dead (`kill -0` fails) | **Reap.** Remove the presence file; release its claims (best-effort). |
| `pid` absent or untrusted (PID reuse, or verification item #2 fails) | Fall back to the **heartbeat-stale floor**: reap if `now - last_heartbeat > 20 min`. |

This mirrors `agent-commit`'s "gone OR stale" reclaim, with one deliberate refinement:
**we do not evict a live-PID session for idleness.** The heartbeat-stale floor is a
*backstop* for the case where the PID can't be trusted, not the primary reaper.

No daemon. Sweeping is lazy, exactly as `agent_claims.sweep()` already works.

## Presence ↔ claims integration

Presence is a **frontend to the claims board**, so a third agent that does not
participate in presence still gets the normal claim warnings.

- **`announce "<summary>" --areas a,b,c`** does two things atomically: (1) sets
  `task_summary` in the presence file, and (2) calls `agent_claims.claim(area)` for each
  `--areas` entry — i.e., it declares the session's **intended write set** on the board.
  Areas are **explicit paths**, never parsed out of the natural-language summary.
- **`claim_guard.py`** continues to auto-declare a claim on every actual edit, and now
  *also* bumps the session's `last_heartbeat` (an in-process import call, not a fork — it
  adds no measurable cost to the edit path).
- Because claims are only ever created by **writes** (announced intent + actual edits), a
  session's claim set on the board **is** its write set. Read-only access creates no
  claim. This is the load-bearing simplification behind the overlap protocol below.

**Deregistration = release-on-exit, expire-on-crash** (adopted recommendation, flagged
for review):

- On a clean **Stop**, `deregister` reads the session's claim records (those whose `who`
  matches its key), releases each from the board, and removes the presence file.
- If the session **crashes** (Stop never fires), the claims board's existing **2 h TTL**
  expires the records and the next `sweep` reaps the dead-PID presence file. No orphaned
  state survives a session.

## Conflict taxonomy

Reuses Part A's structural classes and adds two semantic classes:

- **A1/A2** — same-file edit contention (exact path / folder-covers-file), already
  handled by `claim_guard` + commit-time net.
- **B** — two sessions writing a shared file in sequence (coordinatable).
- **C** — branch/worktree-structural conflict.
- **D** — read-only sharing; **always proceed** (no claim, no contention).
- **S1 — task duplication.** Two sessions pursuing the **same task**, possibly on
  **different files**. The headline case this system exists to catch.
- **S2 — scope overlap.** Two sessions on **related** tasks whose outputs may interfere
  or should be sequenced.

## Graduated-autonomy overlap protocol

After `announce`, the agent compares its intended work against the roster and classifies
its confidence that proceeding is safe:

- **HIGH → auto-coordinate and proceed.** Includes first **narrowing its own write set**
  to avoid a peer's claimed areas, when the narrowed set still completes the task.
- **MEDIUM → propose a mitigation and wait for acknowledgement** (e.g., "I'll sequence
  after session `a1b2`'s edit to `ctl_instruction.md`").
- **LOW → STOP and surface to the user.** Do not proceed on the overlapping work.

Two axes drive the classification: **write-overlap** (do both sessions plan to write the
same file?) and **semantic relationship** (unrelated / S2-related / S1-same-task). Because
a session's claims *are* its write set, "write-overlap" is computed authoritatively by
`agent_claims.find_conflict(my_intended_writes)` against the live board — never from any
cached field.

| Planned writes vs. live peers | Unrelated task | Related task (S2) | Same task (S1) |
|---|---|---|---|
| **No write-overlap** (disjoint, or narrowed to disjoint) | **proceed** — auto-declare and go | **MEDIUM** — propose, wait | **LOW** — STOP, surface |
| **Write-overlap** (both write one file) | **MEDIUM** — Class B, sequence the edits | **MEDIUM → LOW** — sequence and confirm | **LOW** — STOP, surface |

Read-only sharing creates no claim → it never appears as write-overlap → **proceed**
(Class D).

**Conservative tie-breaks** (this is the highest-risk part of the design — bad
coordination is worse than none):

- If the agent cannot *confidently* place a situation in the **proceed** cell, it treats
  it as at least **MEDIUM**.
- **Any** whiff of S1 (same task) → **LOW**, regardless of file overlap. Duplicated work
  is the failure this system exists to prevent; err toward surfacing it.

## CLI surface

A new module `scripts/git_policy/agent_presence.py` plus an `agent-presence` shim
(mirroring `agent_claims.py` and the `agent-claim` shim).

| Command | Caller | Effect |
|---|---|---|
| `announce "<summary>" --areas a,b,c` | **agent**, after first prompt | set `task_summary`; `agent_claims.claim()` each explicit area. Never NLP-parses areas. |
| `list` | agent or human | sweep stale, print the roster |
| `register` | **SessionStart hook only** | create `<session_id>.json` (session_id from hook payload on stdin, pid via `getppid()`, worktree/branch via git), sweep, print roster |
| `deregister` | **Stop hook only** | release this session's claims, remove its presence file |
| `heartbeat <session_id>` | **`claim_guard.py` only** | bump `last_heartbeat`. `claim_guard` invokes this as an **in-process module call** (`agent_presence.heartbeat(session)`) on the hot edit path; the subcommand form exists only for parity and manual use |

## Hook wiring

Three touch-points in `.claude/settings.json` / the hook scripts:

1. **SessionStart** — extend `scripts/session_banner.sh` (it already prints
   worktree/branch context) to also run `agent-presence register`, which appends the
   roster after the existing banner line. Registration reads `session_id` from the
   SessionStart payload on stdin (same source `claim_guard.py` uses).
2. **PreToolUse `Edit|Write|MultiEdit`** — `claim_guard.py` adds one in-process call,
   `agent_presence.heartbeat(session)`, alongside its existing auto-declare.
3. **Stop** — a **new** Stop hook entry running `agent-presence deregister`. Claude Code
   supports multiple hooks per event, so this coexists with the claude-mem plugin's
   existing Stop hook. (Verification item #4 confirms Stop fires with the session_id.)

## Subagents

The **unit of presence is the top-level session.** Agent-tool subagents do **not**
register, announce, or appear in the roster. This keeps the roster a list of *actors a
user is driving*, not internal fan-out.

This depends on a payload fact that must be verified before build (item #3): subagent
edits must carry the **parent** session_id (so their auto-declared claims and heartbeats
attribute to the parent), and SessionStart must **not** fire per-subagent. If subagent
edits instead carry a distinct child session_id, the contingency is to map child→parent
(requires a parent-id field in the payload) or to accept short-lived child claims that
expire under the 2 h TTL.

## Roster format

Printed at SessionStart and on `list`. One line per live peer (the current session is
excluded):

```
Active sessions (excluding yours):
  [a1b2] specwork / milestone/v1.6 — "Phase 32 evidence-framework adjudication"
         writes: .planning/phases/32-*, ctl_instruction.md   ♥ fresh
  [c3d4] trainex  / track/trainex   — (no task announced)
         writes: none   ♥ 12m
```

Fields: short session id, worktree, branch, `task_summary` (or "no task announced"),
derived claimed (write) areas, heartbeat age.

**Cross-worktree visibility and weighting** (originally a reconstruction of garbled
source text; **confirmed by the user 2026-06-26**): peers in **other** worktrees remain
visible but are **marked** as cross-worktree. The agent weights overlap **by locality**:

- **Same-worktree / same-branch** peers carry the **highest** weight for *file-collision*
  risk, because they share a working directory.
- **Semantic duplication (S1/S2)** is weighted across **all** peers, including
  cross-worktree ones — duplicate work happens across branches too.

## Pre-build verification gate

These are read-only probes that **must pass before any implementation begins**. Each
guards a load-bearing assumption; a failure forces a design revision, not a workaround.

1. **`session_id` identity match.** The `session_id` in the **SessionStart** payload must
   equal the `session_id` in the **PreToolUse / `claim_guard`** payload. If they differ,
   presence and claims key the same session under different identities and the entire
   join breaks. *(Partial evidence already in hand: the live board shows one stable
   `session:9d11c50f…` across four edits over ~10 minutes — the claim-guard side is
   stable within a session. The SessionStart-equality half is still unproven.)*
2. **`getppid()` durability.** At SessionStart, `getppid()` must resolve to the durable
   `claude` session process, not a transient shell. Determines whether `kill -0` is
   trustworthy or whether we lean on the 20-minute heartbeat backstop.
3. **Subagent payloads.** Subagent edit hooks must carry the **parent** session_id, and
   SessionStart must not fire per-subagent (see Subagents).
4. **Stop reliability.** The Stop hook must fire on session end with the correct
   session_id, so `deregister` can release claims cleanly.

## Failure modes and the hard backstop

- **Stale presence after a crash** → reaped by dead-PID `kill -0` on the next sweep;
  claims expire under the 2 h TTL. Bounded by one session's lifetime.
- **An agent ignores the roster** → no worse than today; the commit-time owned-paths net
  in `agent-commit` still catches same-file collisions. Presence adds awareness, removes
  no guardrail.
- **Cache/board drift** → impossible to cause a wrong verdict: overlap verdicts always
  read the live claims board (`find_conflict`), never a cached list.

The owned-paths check in `scripts/agent-commit` remains the **single hard backstop**.
Everything in this document is advisory.

## Open decisions (adopted recommendations — confirm at review)

These were carried as recommendations into this draft. They are marked here so they can
be corrected at the spec-review gate rather than buried:

1. **Heartbeat-stale floor = 20 min**, and **live-PID sessions are never reaped for
   idleness** (rendered `idle (♥ Nm)`). The floor is a backstop for untrusted PIDs only.
2. **Cross-worktree weighting** as reconstructed above (visible-but-marked; file-collision
   weight highest for same-worktree/same-branch; semantic weight across all peers).
   Originally a reconstruction of garbled source text; **confirmed by the user 2026-06-26**
   (post-execution review) to match intent — now settled.
3. **Deregister = release-on-exit, expire-on-crash** (Stop releases claims; 2 h TTL is
   the crash backstop).
4. **`claimed_areas` derived from the board, not persisted** in the presence file
   (refinement of the original schema sketch). Confirm this is acceptable.

## Out of scope / future

- Cross-session **activation** (the watchdog) — separate parked effort.
- Sub-file / section-granular claims (Decision R1: rejected; the claims engine
  prefix-matches on `/`, so a sub-file token cannot register against a whole-file edit,
  and line ranges drift).
- Automatic reconciliation with external design efforts (e.g., a sibling review of a
  downloaded design) — handled by the user, not this system.
