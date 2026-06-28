---
status: active
purpose: verification-report
created: 2026-06-28
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire when the watchdog ships as a packaged skill (Phase 4) and this same-worktree
  end-to-end behavior is covered by an automated harness test, or when Claude Code's
  background-shell re-entry primitive changes — re-validate after any harness upgrade
  that touches background re-entry.
---

# Same-Worktree Live Dry-Run Results — 2026-06-28

Phase 2, Task 2.5 Step 3 of the cross-session watchdog implementation plan
(`docs/work/plans/cross_cutting/parallel-agent-coordination-watchdog/2026-06-26-cross-session-watchdog-implementation-plan.md`).

**Question under test:** does an idle `claude` session (Agent B), armed with the real
`wd-arm` watcher and with no human present, re-enter and act on its own the moment a
*separate* `claude`/shell (Agent A) publishes a `done` marker into the shared channel —
claiming exactly once and reading its task from the channel?

This is the same-worktree common case: A's commit is already on B's HEAD, so the
watchdog reduces to its essential core — wake idle B when A's done-marker lands.

## Environment

- macOS (Darwin), Claude Code TUI.
- Two tabs in the main worktree (`<home>/Desktop/3_body_problem`, `master`).
  Tab B = an idle, armed `claude` session ("Agent B"). Tab A = the producer.
- No keystroke entered Tab B after arming; the wake signal came only from A's publish.

## Procedure

1. **B (Tab B `claude`)** ran, as a background command from inside its own session:
   `tools/watchdog/wd-arm --channel live --poll-secs 5 --timeout-secs 600`.
   The session went idle with the watcher polling. (`pgrep -fl wd-arm` confirmed a live
   watcher before publishing.)
2. **A (Tab A shell)** published against a clean, committed scope:
   `tools/watchdog/wd-publish-done --channel live --stage demo --scope <clean tracked file>`.

## Result — PASS ✅

Within ~one poll interval of A's publish, **Tab B re-entered unattended** (no keystroke),
printed its wake line (`WAKE <head>`), made the atomic exactly-once claim
(`<channel>/claimed.<head>`), and began its armed task — running
`python3 -m unittest tests/watchdog/test_watchdog_mvp.py`, which reported green.

This confirms the same-worktree handoff end-to-end against the real scripts, on top of
the P1 background-watcher re-entry path proven in Phase 1
(`2026-06-26-idle-wake-results.md`). The committed unittest
(`tests/watchdog/test_watchdog_mvp.py`) is the re-derivable proof of the script logic;
this note records the harness re-entry behavior the unittest cannot capture.

## Method notes (for re-derivability and honesty)

- **Build-time single-session check.** Before the two-tab run, the same path was
  demonstrated within one session: `wd-arm` launched as a background command, A's publish
  from the foreground, and the harness re-entered on the watcher's exit with `WAKE <head>`;
  the woken side read `consumer-task.md` and ran the armed task green.
- **Smoke deviations from the plan text.** The Task 2.2 / 2.3 smoke steps (written as
  "commit a trivial change … in the main worktree") were instead run in throwaway temp git
  repos and against an already-clean tracked-file scope, to avoid junk commits on `master`.
  The committed unittest reproduces each in an isolated temp repo, so the verifications are
  re-derivable without those manual smokes.
- **First two-tab attempt FAILED — root-caused and fixed.** The initial instructions had B
  pre-create `/tmp/b-task.md` and arm with `--task-file /tmp/b-task.md`. The file was not
  where `wd-arm` looked, so `wd-arm` exited 2 *before* arming — leaving no watcher process
  and no `consumer-task.md`, with B simply idle. Evidence: a valid `done.json` was present
  and `wd-check` returned `WAKE`, but there was no claim and no watcher. Fixed two ways:
  (a) the corrected procedure drops `--task-file` (the payload is optional to the wake);
  (b) `wd-arm` was hardened (commit `dbca0af`) so a missing `--task-file` warns and arms
  anyway, with a regression test.

## Cross-references

- MVP tools + unittest: commit `f37469c4`.
- `wd-arm` missing-`--task-file` hardening: commit `dbca0af`.
- Phase 1 idle-wake evidence: `2026-06-26-idle-wake-results.md`.

## Status

Phase 2 same-worktree path verified end-to-end (committed unittest + two-tab live dry run).
Phase 3 (cross-worktree integration) and Phases 4–5 (durable wake, packaging, PUSH/GSD)
remain out of scope and unexecuted.
