# Unattended Idle-Wake Test Results — 2026-06-26

Phase 1 of the cross-session watchdog implementation plan
(`docs/work/plans/cross_cutting/parallel-agent-coordination-watchdog/2026-06-26-cross-session-watchdog-implementation-plan.md`).

**Question under test:** does an idle `claude` session, with no human present, re-enter
and act on its own when its own background shell exits (P1) or its own durable cron fires
(P2)? This is the load-bearing unknown the whole "pull" wake path rests on.

## Environment

- macOS (Darwin), Claude Code TUI.
- Two-terminal manual test. Terminal A = an idle, armed `claude` session ("Agent B").
  The wake signal was created by a *separate* process — no keystroke ever entered
  Terminal A after arming.

## P1 — background-watcher re-entry: **PASS** ✅

- **Arming:** Terminal A's `claude` was instructed to run, in the background and then end
  its turn, `bash -c 'until test -f /tmp/wd_wake_demo; do sleep 2; done'`, and to print
  `WOKE` when that command returned.
- **Observed idle posture:** the agent ended its turn and sat idle **while its background
  shell kept polling**. "Conversation idle + background watcher still live" is therefore a
  real, stable state — exactly the watchdog's intended consumer posture. (Confirmed
  directly by the operator: the session reported the launched shell still running while
  the agent was idle.)
- **Signal:** `/tmp/wd_wake_demo` created at 13:24:17 by a separate process (the operator's
  other session), with no interaction with Terminal A.
- **Result:** Terminal A **spontaneously started a new assistant turn with no human
  keystroke** and printed `WOKE`.
- **Latency:** a few seconds (background poll interval was 2s + harness re-invoke;
  not instrumented to sub-second).
- **Re-entry mode:** spontaneous — NOT keystroke-gated.

## P2 — durable cron re-entry: **NOT YET RUN**

Deferred. P1 PASS already establishes that an unattended PULL wake is viable, which is the
load-bearing unknown for the MVP — the Phase 2 MVP wake *is* the P1 background-watcher
path. P2 (durable `CronCreate`, which survives restarts and long idle) is the intended
fallback and will be validated when Phase 4 builds the durable wake.

## Decision (Phase 1 Step 4 gate)

- **PULL is viable unattended.** Confirmed by P1.
- **Primary wake path = P1 background-watcher re-entry** (low latency). This is what the
  Phase 2 MVP `wd-arm` watcher relies on.
- **P2 durable cron = intended fallback**, to be verified at Phase 4.
- **PUSH (tmux) stays an optional accelerator** (Phase 5), not the primary — PULL works.

## Provenance

- Resolves review finding **F2** (idle-wake was the least-demonstrated piece) for the
  primary path.
- The earlier OS-primitive PTY-injection proof (`/tmp/wd_pty_proof.py`, prior session)
  pertained to the **PUSH** path and is not on disk anymore; it is not needed for this P1
  PULL result and would be regenerated only if/when Phase 5 (PUSH) is taken up.
