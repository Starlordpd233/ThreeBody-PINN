---
phase: 42-operator-runbook-surface-monitoring
plan: 08
subsystem: training-lifecycle
tags: [signals, heartbeat, run-artifacts, graceful-shutdown]
requires:
  - phase: 42-01
    provides: widened training logger records
  - phase: 42-04
    provides: JSONL and human log handlers
  - phase: 42-05
    provides: TensorBoard logging sink
  - phase: 42-06
    provides: heartbeat and summary writers
provides:
  - main-thread SIGINT/SIGTERM handling with graceful-stop and escalation behavior
  - RunController stop checks at Adam and L-BFGS boundaries
  - complete catchable-run lifecycle artifacts and terminal honesty states
affects: [42-09, signal-tests, run-contract-tests]
tech-stack:
  added: []
  patterns: [composition-root lifecycle wiring, callback-driven optimizer interruption]
key-files:
  created: [pinn/training/signals.py]
  modified: [pinn/training/controllers.py, pinn/train.py]
key-decisions:
  - "Operator disposition derives from stop state, failure artifacts, non-finite JSONL state, and exceptions rather than HALT alone."
  - "The second-SIGINT callback is restricted to atomic status transition and handler flushes; terminal summary finalization remains on the main thread."
patterns-established:
  - "Process-global handlers, heartbeat, and sinks are installed and removed exclusively in pinn.train.main()."
requirements-completed: [OPS-01, OPS-02, OPS-05]
coverage:
  - id: D1
    description: Signal debounce, SIGTERM graceful state, synchronous escalation, and handler restoration.
    requirement: OPS-02
    verification:
      - kind: unit
        ref: "conda run -n pinn-train python -c SignalState/note_signal and install_signal_handlers probes"
        status: pass
    human_judgment: false
  - id: D2
    description: RunController stop seam at Adam and L-BFGS boundaries.
    requirement: OPS-02
    verification:
      - kind: unit
        ref: "tests.phase40.test_controllers + tests.phase41.test_controllers_ext"
        status: pass
    human_judgment: false
  - id: D3
    description: Catchable training runs produce honest status and summary artifacts with cleaned-up sinks.
    requirement: OPS-05
    verification:
      - kind: integration
        ref: "tests.phase41.test_train_entrypoint; isolated synthetic lifecycle smoke"
        status: pass
    human_judgment: false
duration: unrecorded
completed: 2026-07-19
status: complete
---

# Phase 42 Plan 08: Signal and Run Lifecycle Summary

**Graceful signal interruption and honest run-directory lifecycle wiring for the training composition root**

## Performance

- **Completed:** 2026-07-19T15:05:38Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Added a pure signal-state helper with SIGINT debounce, synchronous escalation, SIGTERM graceful handling, and reversible handler installation.
- Added an opt-in `RunController.should_stop` seam at Adam boundaries and inside L-BFGS closure evaluation.
- Wired run-directory scaffolding, sinks, heartbeat, terminal state classification, graceful checkpointing, and catchable-path cleanup into `pinn.train.main()`.

## Task Commits

1. **Task 1: signal state and handler installer** — `bf98bce` (`feat`)
2. **Tasks 2–3: stop seam and lifecycle wiring** — `07fa2a3` (`feat`)

## Files Created/Modified

- `pinn/training/signals.py` — debounce state and main-thread handler installer.
- `pinn/training/controllers.py` — optional stop callback at optimizer boundaries and L-BFGS closure evaluations.
- `pinn/train.py` — composition-root lifecycle, terminal classification, and cleanup.

## Decisions Made

- `interrupted` takes precedence over a concurrent divergence, while the canonical JSONL retains the non-finite record for later inspection.
- `HALT` is not used as a success/failure discriminator because curriculum completion and guard-halting share that disposition.

## Deviations from Plan

None - plan executed as specified. Tasks 2 and 3 share one code commit because resource installation and catchable-path cleanup are one lifecycle boundary.

## Issues Encountered

- The terminal runner returned before long test processes had completed, and zsh reserves the variable name `status`; explicit process checks and a portable result variable confirmed the suites passed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for 42-09 to exercise the held-out signal and run-contract scenarios.
- No 42-09 test files were modified by this plan.

---
*Phase: 42-operator-runbook-surface-monitoring*
*Completed: 2026-07-19*
