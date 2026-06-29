---
name: cross-session-watchdog
description: Use when an idle Claude session (Agent B) must start working the moment another session (Agent A) finishes a unit of work — the same-worktree common case (A and B share one checkout) or the cross-worktree case (A and B are on different branches and B must integrate A's commit before acting).
---

# Cross-Session Watchdog

## Overview

A **producer** (Agent A) commits a unit of work and signals completion. An idle
**consumer** (Agent B) is re-entered the moment that signal is actionable and
begins its pre-written task. The watchdog guarantees the wake happens exactly
once (atomic `mkdir` claim), never waits forever on a dead producer
(dead-producer timeout), and is always observable and killable from the shell
(on-disk `armed.json` + `disarm` sentinel + `wd-disarm`/`wd-status`).

Channel state lives on disk under the shared git common dir at
`<git-common-dir>/live-monitor/channels/<channel>/` (`done.json`,
`claimed.<head>`, `armed.json`, `disarm`, `consumer-task.md`), so a producer and
consumer in the same repo — main worktree or any linked worktree — agree on one
channel location with no setup.

Two wake paths ship:

- **P1 — background watcher (default; drain-safe).** Agent B runs `wd-arm` in
  the background via the Bash tool and ends its turn. The watcher polls
  `wd-check`; on the first `WAKE` it atomically claims and exits, and the
  harness re-enters B's session. This is the only path enabled by default. It
  is **inherently drain-safe**: B's session is idle-but-alive while the watcher
  polls, so there is no background timer to leave stranded.
- **P2 — durable cron (fallback; GATED).** When P1 cannot be used (e.g. B's
  session cannot stay foreground), a Claude Code harness `CronCreate` may arm a
  recurring wake. This path is gated and bounded; see "P2 durable cron" below.
- **PUSH (optional standalone accelerator for tmux users).**
  `tools/watchdog/wd-push` is an external watcher (run from the operator's
  terminal, not B's session) that polls `wd-check` and injects the fixed wake
  prompt into B's tmux pane via `send-keys` on `WAKE`; it shares the same
  `armed.json`/`disarm` lifecycle (`kind="push-watcher"`) and is a standalone
  tool, not a skill operation.

The **fixed wake prompt** (the arming session fires this verbatim on re-entry,
for both P1 and P2 — never interpolate channel-file contents into a prompt):

> Watchdog: read `consumer-task.md` in this channel and the `wd-arm` result
> line; if WAKE, begin that task; if ALREADY-CLAIMED or PRODUCER-STALLED, stop
> and report.

## When to use

- A is about to finish a unit of work and B should pick it up immediately,
  without a human in the loop.
- B is idle and waiting; you want B's next action to start automatically when
  A's commit lands.
- Same-worktree (common): A and B share one checkout — A's done commit lands on
  B's HEAD directly.
- Cross-worktree (secondary): A and B are on different branches in linked
  worktrees — B integrates A's commit before acting.

**Not for:** single-session, single-agent work; or coordinating agents that
don't share a git repo.

## Operation 1 — `publish-done` (Agent A, the producer)

After committing its unit of work, A publishes a terminal "done" marker anchored
on its HEAD commit:

```
tools/watchdog/wd-publish-done --channel <name> --stage <stage> --scope "<pathspec>"
```

- Refuses to publish a dirty scope (exit 3) — the marker can only certify
  committed work.
- Same-worktree vs cross-worktree is documented for B (next section): A's
  command is identical in both cases.

The marker (`<channel>/done.json`) is written atomically (write-temp + `mv`), so
the newest publish always wins and a reader never sees a half-written file.

## Operation 2 — `arm-consumer` (Agent B, the idle consumer)

B writes the task it should perform on wake to a file (e.g. `consumer-task.md`),
then arms.

### P1 watcher (default; drain-safe)

Run in the background via the Bash tool and end the turn:

```
tools/watchdog/wd-arm --channel <name> --poll-secs 20 --timeout-secs <N> --task-file <task.md>
```

The watcher writes `<channel>/armed.json` (so `wd-status`/`wd-disarm` can see
it), polls `wd-check`, and on the first `WAKE` performs an atomic exactly-once
claim (`mkdir <channel>/claimed.<head>`) and prints one of:

- `WAKE <head>` (exit 0) — claimed; begin the `consumer-task.md` task.
- `ALREADY-CLAIMED <head>` (exit 0) — another watcher already claimed this head.
- `PRODUCER-STALLED after Ns` (exit 42) — no `done` marker within `--timeout-secs`.
- `DISARMED` (exit 0) — stood down via the `<channel>/disarm` sentinel.

**On wake re-entry, B runs** `wd-check` (same-worktree) **or**
`wd-integrate` then `wd-check --require-integration` (cross-worktree), then
begins the task in `consumer-task.md`. (Cross-worktree: B's branch does not yet
contain A's done commit, so `wd-integrate` merges A's HEAD into B's branch
before `wd-check --require-integration` will return `WAKE`.)

### P2 durable cron (fallback; GATED)

The skill MUST REFUSE to arm P2 unless ALL three conditions hold:

1. The user typed an explicit **"yes, durable"** at the prompt (no inferred
   consent — P2's caveats are material and the user must opt in knowingly).
2. A **TTL was supplied** (a cron without a TTL can fire forever).
3. **`wd-disarm` and `wd-status` exist on disk and pass their own smoke tests**
   (`wd-status` runs clean; `wd-disarm --all` exits 0). The termination layer is
   the safety contract for P2 — without it, an unattended cron cannot be killed.

When arming P2, write the same `<channel>/armed.json` record (with
`"kind":"cron"` and the TTL), and the wake prompt must, as its **FIRST action on
each fire**, check the `<channel>/disarm` sentinel and the TTL:

- on success (WAKE) or TTL expiry → `CronDelete` the job and remove
  `armed.json` **before doing anything else** (disarm-on-success +
  self-termination), so a finished handoff or an expired arm never leaves a
  stranded cron behind.

Two P2 caveats (from the idle-wake evidence), to surface when arming:

- **Foreground requirement.** `CronCreate` firing pauses when B's terminal tab
  is backgrounded on macOS (process-group throttling). P2 is only reliable when
  B's TUI is foreground or near-foreground.
- **On-disk verification.** The skill MUST verify the durable job is on disk at
  `.claude/scheduled_tasks.json` (and visible to `CronList`) immediately after
  arming, and refuse to consider the arm complete otherwise — a job that only
  lives in memory is invisible to other sessions and may not survive a restart.

### GSD adapter (optional)

When `tools/watchdog/wd-gsd-publish` is present, GSD phase mapping is available:
`wd-gsd-publish --phase NN --scope "<pathspec>" [--channel NAME]` maps to
`wd-publish-done --stage gsd:phase-NN --scope "<pathspec>"` and forwards the exit
code and stdout/stderr. By convention, run it **immediately after** the
`git commit` whose message is `verify(<scope>): …` for phase NN, so `done.head`
(anchored on HEAD by `wd-publish-done`) IS the verify(NN) commit — the adapter
does no commit archaeology. If the adapter is absent, use `--stage`/`--scope`
directly. Detected by presence, never required.

### After every successful arm (P1 or P2), print:

- the **channel** that was armed;
- the **TTL** (or: "no TTL — watcher runs until WAKE or --timeout-secs");
- **when the TTL expires** (wall-clock), if a TTL is set;
- the **disarm command**: `tools/watchdog/wd-disarm --channel <name>`;
- the **status command**: `tools/watchdog/wd-status`.

## If anything goes wrong

- `tools/watchdog/wd-disarm --all` cleans up **every** arm across every channel
  (writes the `disarm` sentinel, best-effort kills the armed pid, removes every
  `armed.json`). Safe to run repeatedly; exit 0 even when nothing is armed.
- `tools/watchdog/wd-status` shows what's live — every active arm with its kind,
  age, TTL, and armed-by, plus any pending disarm-request sentinel.

## Common mistakes

| Mistake | Fix |
|--------|-----|
| Arming P2 without explicit "yes, durable" + TTL + smoke-tested disarm | Refuse; fall back to P1 (drain-safe by construction). |
| Interpolating channel-file bytes into the wake prompt | Use the **fixed wake prompt** verbatim; the prompt names `consumer-task.md` by path, never its contents. |
| Skipping `wd-integrate` in the cross-worktree path | `wd-check --require-integration` returns `STALE:not-integrated` until B merges A's HEAD; integrate first, then check. |
| Treating "no TTL" as "runs forever" in P2 | P2 REQUIRES a TTL. "No TTL" is only valid for P1, where `--timeout-secs` is the watcher's own bound. |
| Not verifying the durable job on disk after P2 arm | `CronList` AND `.claude/scheduled_tasks.json` must both show it; if not, the arm is incomplete. |

## Red flags — STOP

- About to arm P2 without surfacing the foreground-tab caveat and getting
  explicit user consent.
- About to arm P2 without a TTL.
- About to interpolate `done.json` / `consumer-task.md` bytes into the wake
  prompt instead of using the fixed constant.
- About to walk away from a P2 arm without verifying the job landed on disk.
