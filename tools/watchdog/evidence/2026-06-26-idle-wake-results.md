---
status: active
purpose: verification-report
created: 2026-06-26
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire when the Phase 4 termination-guarantee contract lands and the watchdog MVP
  ships — this file's "Discoveries" become regression-test targets rather than standing
  evidence. The P1/P2 results remain valid for as long as Claude Code's harness primitives
  (`Bash` background re-entry, `CronCreate`) behave as observed; re-validate after any
  harness upgrade that touches either primitive.
---

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

## P2 — durable cron re-entry: **PASS** ✅ (with caveats)

- **Arming.** A durable `CronCreate` was armed in the consumer session with the fixed
  prompt: *"If `/tmp/wd_wake_demo2` exists, print WOKE-CRON and stop; else do nothing."*
  `CronList` and `.claude/scheduled_tasks.json` were verified immediately after arming to
  confirm the job was on disk (see "Discoveries" below — durability must be verified, not
  assumed).
- **Signal.** `/tmp/wd_wake_demo2` created at the consumer session's home worktree by a
  separate process (the operator's other session), with no interaction with the consumer
  session after arming.
- **Result.** The consumer session **spontaneously started new assistant turns with no
  human keystroke** and printed `WOKE-CRON` on every fire. The cron fired repeatedly (every
  minute per the cron spec) as long as the session remained foreground and the signal file
  existed; once the operator closed the session (full computer restart at session end), the
  fires stopped cleanly.
- **Latency.** ≤ 60 seconds per fire (cron spec interval). Not instrumented to sub-minute.
- **Re-entry mode.** spontaneous — NOT keystroke-gated.

### Caveats

- **Foreground requirement.** Cron firing pauses when the consumer session's terminal tab
  is backgrounded on macOS (process-group throttling). P2 is therefore only reliable when
  B's TUI is foreground or near-foreground. The watchdog's arming step must warn the user
  about this.
- **Drain risk.** A `CronCreate` armed with `durable: true` and no termination contract is a
  **silent quota drain** against the owning session — confirmed in this test (see
  "Discoveries"). P2 is therefore not eligible for activation until the Phase 4
  termination-guarantee contract ships.

## Discoveries (regression targets for Phase 4)

1. **macOS background-tab throttle (MEDIUM).** `CronCreate` does not fire reliably when the
   consumer session's terminal tab is backgrounded on macOS — the timer pauses with the
   rest of the tab's process group. Re-entry happens, but with unpredictable / unbounded
   latency. First observed when an initial arming attempt against a backgrounded tab
   produced no fires despite the cron being correctly registered.
2. **Agent-armed `durable: true` crons can come out session-only (MEDIUM).** When a
   `claude` agent invokes `CronCreate` with `durable: true`, the job has been observed
   persisting as **session-only** (lives in the agent's process memory, not in
   `.claude/scheduled_tasks.json`) on at least one path through the harness — even though
   the `durable` flag was explicitly set. Observed twice in succession on the operator's
   fresh-session arming attempt; the third attempt (this session, direct arming) did
   persist correctly. Counterintuitively, **durable is safer than session-only for this
   use case** because a durable job is observable on disk and externally killable (via
   `.claude/scheduled_tasks.json` edit), whereas a session-only job is invisible from
   outside the owning session. The arming skill must therefore **verify persistence on
   disk** immediately after arming and refuse to consider the arm complete until
   `CronList` shows the job AND `.claude/scheduled_tasks.json` contains it.
3. **Silent drain risk from recurring crons (HIGH).** The most important finding of this
   test. A `CronCreate` armed with `durable: true` and no termination contract will keep
   firing every minute against an unattended session — every fire is an
   inference-cost-attached prompt. If the user walks away from the session (or forgets
   the cron exists), usage accumulates with no visible signal. The operator's own session
   ran a recurring `* * * * *` cron for ~25 minutes during this test before explicit
   deletion via `CronDelete` — and a separate agent's `f4c0519d` session-only cron
   remained live in its owning terminal until the operator closed the entire workstation.
   The watchdog's P2 path therefore MUST be gated on the Phase 4 termination-guarantee
   contract (`wd-disarm`, `wd-status`, TTL-bound arming, conservative defaults,
   disarm-on-success) before it is enabled. This is now a hard requirement in the plan
   ("Termination guarantee (hard requirement — discovered 2026-06-26)").

## Decision (Phase 1 Step 4 gate)

- **PULL is viable unattended.** Confirmed by both P1 and P2 (in the foreground case).
- **Primary wake path = P1 background-watcher re-entry** (low latency, inherently
  drain-safe). This is what the Phase 2 MVP `wd-arm` watcher relies on. The MVP MAY ship
  with P1 only.
- **P2 durable cron = intended fallback**, eligible for activation **only after** the
  Phase 4 termination-guarantee contract lands and is verified by `tests/watchdog/test_termination.py`.
  Until then, P2 is documented but not enabled.
- **PUSH (tmux) stays an optional accelerator** (Phase 5), not the primary — PULL works.

## Provenance

- Resolves review finding **F2** (idle-wake was the least-demonstrated piece) for the
  primary path.
- The earlier OS-primitive PTY-injection proof (`/tmp/wd_pty_proof.py`, prior session)
  pertained to the **PUSH** path and is not on disk anymore; it is not needed for this P1
  PULL result and would be regenerated only if/when Phase 5 (PUSH) is taken up.
