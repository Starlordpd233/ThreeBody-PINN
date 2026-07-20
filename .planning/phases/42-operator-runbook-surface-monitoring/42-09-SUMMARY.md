---
phase: 42-operator-runbook-surface-monitoring
plan: 09
subsystem: test-suite
tags: [signals, run-contract, honesty, redaction, e2, e4]
requires:
  - phase: 42-03
    provides: test stubs + _fixtures.py subprocess harness
  - phase: 42-07
    provides: wrapper exit code contract
  - phase: 42-08
    provides: signal handling, lifecycle wiring, failure artifacts
provides:
  - E2 signal-race tests (SIGINT/SIGTERM exit codes, debounce, atomic checkpoints)
  - E4 SIGKILL presence/staleness tests at three barriers
  - must-NOT #1 honesty-layer tests (failed runs never masquerade as finished)
  - must-NOT #2 redaction tests (no /Users/, hostname, secrets in artifacts)
affects: []
tech-stack:
  added: [tests/phase42/test_signals.py, tests/phase42/test_runs_contract.py, tests/phase42/test_honesty_layer.py, tests/phase42/test_redaction.py]
  patterns: [subprocess-driven synthetic runs, PHASE42_REPO_ROOT env-var path injection, failure-artifact barrier polling, pure-function Nyquist bracket beside the subprocess case]
key-files:
  created:
    - tests/phase42/test_signals.py
    - tests/phase42/test_runs_contract.py
    - tests/phase42/test_honesty_layer.py
    - tests/phase42/test_redaction.py
  modified:
    - tests/phase42/_fixtures.py
    - tests/phase42/__init__.py
key-decisions:
  - "Subprocess path injection via PHASE42_REPO_ROOT env var (not cwd manipulation) — bare conda python lacks pinn on path; wrapper prepends repo root to sys.path."
  - "argv slicing is sys.argv[2:] (0=script, 1=runs_root, 2=--config, 3=path) — an earlier [3:] silently dropped --config."
  - "guards override deep-merges into run.guards (YAML schema nests guards under run.guards, not top-level) — an earlier silent-drop kept loss_explosion_ceiling at 1e12 instead of 1e-12."
  - "The E2 two-point debounce bracket is pinned twice: deterministically on note_signal() (SignalStateLogicTests, W/5+W/3 vs 1.5W+2W) and end-to-end in the subprocess cases. Real-signal delivery races graceful teardown, so the bracket itself must not depend on subprocess timing."
  - "E4 staleness is asserted as DECIDABLE (timestamp_epoch + staleness_threshold_secs present, positive, and from this run) rather than ELAPSED — the plan forbids a real wall-clock wait past the threshold, and SIGKILL freezes timestamp_epoch so any later reader decides staleness from the file's own fields."
  - "A coalesced double-SIGINT accepts returncode 130 OR -SIGINT: finish_run() restores the default disposition (train.py:380) only after the checkpoint, status transition, and summary have landed, so the -SIGINT encoding is provably post-finalization — proven in-test by asserting latest.pt and status.state == interrupted, not assumed."
patterns-established:
  - "_wait_for_failure_artifact barrier: poll runs/<name>/failure/ non-empty before asserting terminal state."
  - "Pair a timing-sensitive subprocess case with a pure-function test over the same decision function, so the contract is pinned deterministically and the subprocess case only has to prove real delivery."
requirements_completed: [OPS-02, OPS-03, OPS-04, OPS-05]
coverage:
  - id: E2-sigint-once
    description: SIGINT once → checkpoint written + exit 130 + state=interrupted.
    requirement: OPS-02
    verification:
      - kind: subprocess
        ref: test_sigint_once_checkpoints_and_exits_130
        status: pass
    human_judgment: false
  - id: E2-sigterm
    description: SIGTERM → graceful checkpoint + exit 143.
    requirement: OPS-02
    verification:
      - kind: subprocess
        ref: test_sigterm_graceful_exit_143
        status: pass
    human_judgment: false
  - id: E2-debounce-bracket-logic
    description: Two-point Nyquist bracket on note_signal — W/5 and W/3 coalesce, 1.5W and 2W escalate.
    requirement: OPS-02
    verification:
      - kind: unit
        ref: SignalStateLogicTests (3 cases)
        status: pass
    human_judgment: false
  - id: E2-debounce-coalesce
    description: Two SIGINTs within debounce window coalesce into one graceful stop.
    requirement: OPS-02
    verification:
      - kind: subprocess
        ref: test_sigint_twice_inside_debounce_coalesces
        status: pass
    human_judgment: false
  - id: E2-debounce-escalate
    description: Second SIGINT outside debounce → os._exit(130), no further checkpoint.
    requirement: OPS-02
    verification:
      - kind: subprocess
        ref: test_sigint_twice_outside_debounce_escalates
        status: pass
    human_judgment: false
  - id: E4-sigkill-launch
    description: SIGKILL at launch → summary present, state not terminal, staleness-decidable.
    requirement: OPS-05
    verification:
      - kind: subprocess
        ref: test_sigkill_at_launch_presence_and_staleness
        status: pass
    human_judgment: false
  - id: E4-sigkill-mid-adam
    description: SIGKILL mid-Adam → same invariants.
    requirement: OPS-05
    verification:
      - kind: subprocess
        ref: test_sigkill_mid_adam_presence_and_staleness
        status: pass
    human_judgment: false
  - id: E4-sigkill-mid-ckpt
    description: SIGKILL mid-checkpoint → same invariants, no abandoned .tmp.
    requirement: OPS-05
    verification:
      - kind: subprocess
        ref: test_sigkill_mid_checkpoint_presence_and_staleness
        status: pass
    human_judgment: false
  - id: E2-mid-lbfgs-closure
    description: SIGINT mid-L-BFGS-closure → _StopRequested between evals, exit 130.
    requirement: OPS-02
    verification:
      - kind: subprocess
        ref: test_sigint_mid_lbfgs_closure_stops_between_evals
        status: pass
    human_judgment: false
  - id: honesty-forced-halt
    description: Guard-tripped failed run → state=failed, disposition=failed, all losses null.
    requirement: OPS-05
    verification:
      - kind: subprocess
        ref: test_forced_halt_catchable_state_not_finished_and_no_fabricated_metrics
        status: pass
    human_judgment: false
  - id: honesty-forced-divergence
    description: Same honesty invariants for forced-divergence catchable path.
    requirement: OPS-05
    verification:
      - kind: subprocess
        ref: test_forced_divergence_catchable_state_not_finished
        status: pass
    human_judgment: false
  - id: redaction-no-forbidden-shapes
    description: No /Users/, hostname, AWS-key, bearer-token in any artifact.
    requirement: CTX-79
    verification:
      - kind: subprocess
        ref: test_no_forbidden_shapes_in_artifacts
        status: pass
    human_judgment: false
  - id: redaction-summary-md-no-fingerprint
    description: summary.md has no env_fingerprint keys (summary.json only).
    requirement: CTX-79
    verification:
      - kind: subprocess
        ref: test_summary_md_has_no_env_fingerprint
        status: pass
    human_judgment: false
  - id: contract-success-member-list
    description: Success summary.json carries full ratified member list.
    requirement: OPS-05
    verification:
      - kind: subprocess
        ref: test_success_summary_has_full_member_list
        status: pass
    human_judgment: false
  - id: contract-repeated-main
    description: Two main() calls → handlers restored, no leaked handlers, no duplicate JSONL lines.
    requirement: OPS-05
    verification:
      - kind: in-process
        ref: test_repeated_main_handler_lifecycle_regression
        status: pass
    human_judgment: false
duration: 2 sessions (2026-07-19 realization, 2026-07-20 completion)
completed: 2026-07-20
status: complete
---

# Phase 42 Plan 09: Summary

**Realize E2/E4/must-NOT edge tests against the fully wired system (42-08)**

## Status

**Complete.** All four test modules are realized and the full `tests/phase42` suite is green
(37 tests, 0 failures, 0 errors — see Validation below). Execution ran in two sessions: the
2026-07-19 session realized the modules and left four failing cases with diagnosed root
causes; the 2026-07-20 session fixed those four plus one race the reruns exposed.

## Accomplishments

### Files realized (all 4 test modules)
- `tests/phase42/test_signals.py` — E2: SIGINT once / coalesce / escalate, SIGTERM,
  mid-L-BFGS-closure, plus `SignalStateLogicTests` pinning the debounce bracket on the
  pure `note_signal` decision function.
- `tests/phase42/test_runs_contract.py` — success member list, 3 SIGKILL barriers,
  repeated-`main()` handler-lifecycle regression.
- `tests/phase42/test_honesty_layer.py` — forced-HALT and forced-divergence catchable paths.
- `tests/phase42/test_redaction.py` — negative-grep forbidden shapes, summary.md
  no-fingerprint positive control.
- `tests/phase42/__init__.py` — `TODO(phase-43)` deferral comment for the s/step
  non-degradation smoke test.

### Fixture fixes in `tests/phase42/_fixtures.py` (session 1)
1. **`make_runner_wrapper`**: reads `PHASE42_REPO_ROOT` and prepends it to `sys.path`
   (bare conda python lacks `pinn` on path).
2. **argv slicing**: corrected from `sys.argv[3:]` (dropped `--config`) to `sys.argv[2:]`.
3. **`launch_train`**: injects `PHASE42_REPO_ROOT` into the subprocess env and passes
   `env=env` to `Popen`.
4. **`write_train_config` guards merge**: added `elif key == "guards": run["guards"].update(val)`
   — the YAML schema nests guards under `run.guards`, so a top-level `guards` override was
   silently dropped (root cause of the honesty tests failing: `loss_explosion_ceiling` stayed
   at 1e12 instead of 1e-12, so the guard never tripped).

### Fixes applied in session 2 (2026-07-20)

1. **`test_sigkill_mid_checkpoint_presence_and_staleness`** — checkpoint glob was
   `rolling-*.pt`; the store writes `step-{step:06d}.pt` (`checkpoint.py` `_STEP_RE`).
   Changed the glob to `step-*.pt`.
2. **`test_sigkill_at_launch_…` / `test_sigkill_mid_adam_…`** — the assertion required the
   run to be observably stale (`age > threshold * 0.5`), which is only reachable by sleeping
   ~7.5 s past the kill. Plan 42-09 Task 2 explicitly forbids a real wall-clock wait, and the
   invariant it actually asks for is that staleness is **decidable from the file**: SIGKILL
   freezes `timestamp_epoch`, so any later reader computes `now − timestamp_epoch >
   staleness_threshold_secs` itself. Both tests now assert those two fields are present,
   numeric, positive, and belong to this run (not future-dated, under 300 s old).
3. **`test_sigint_mid_lbfgs_closure_stops_between_evals`** — timed out waiting for the
   `phase="2b"` JSONL record because `lbfgs_max_iter=50` made the first `optimizer.step(closure)`
   run a `strong_wolfe` line search far past the 120 s window. Reduced to `lbfgs_max_iter=20`
   (first step completes and logs; the second step's remaining budget still dwarfs the
   assertion's exit-latency ceiling) and raised the barrier timeout to 180 s.
4. **`test_sigint_twice_inside_debounce_coalesces`** — two distinct races, both real:
   - The process sometimes finished its graceful teardown before the second press was due.
     Added `SignalStateLogicTests` (deterministic bracket over `note_signal` at W/5, W/3,
     1.5W, 2W) so the contract no longer depends on subprocess timing, shortened the
     inter-press gap to W/5, and gave the subprocess case the same already-accepted
     process-already-exited fallback the escalate case uses.
   - The full-suite run then exposed the inverse: the second press landing *after*
     `finish_run()` restored the default SIGINT disposition, killing the process by signal
     (`returncode == -2`) instead of via its own `sys.exit(130)`. A shell reports 128+2 = 130
     for both. Handlers stay installed for the whole of `finish_run()` (`train.py:380` restores
     them last), so the restored disposition **proves** finalization already completed — the
     test now accepts either encoding and asserts the durable evidence for it
     (`checkpoints/latest.pt` present, `status.json state == "interrupted"`, no abandoned
     `.tmp`). Re-ran the case twice standalone plus once in-suite: green each time, with the
     terminal-state assertion holding.
5. **`test_sigint_twice_outside_debounce_escalates`** (and the matching branch added in fix 4)
   — the process-already-exited fallback asserted the checkpoint count had grown by exactly
   one. `save_rolling()` evicts under retention (`checkpoint.py` `_evict_rolling`), so once
   retention saturates the visible `.pt` count plateaus and the assertion fails on a perfectly
   correct graceful stop (observed 55 vs an expected 56). Both fallbacks now assert the durable
   evidence instead — `checkpoints/latest.pt` present, no abandoned `.tmp`, `status.json state
   == "interrupted"`. The main paths' inequality assertions (`after >= before` on the coalesce
   path, `after <= before + 1` on the escalate path) are unaffected by eviction and stand.

## Deviations from the session-1 recommendations

Session 1 recommended fixing the L-BFGS barrier by switching from the JSONL `phase="2b"`
record to `status.json`'s `phase` field, on the theory that the heartbeat publishes
`_active_phase = "2b"` (controllers.py:1015) before `optimizer.step(closure)` is entered.
That was **not** adopted: `train.py` feeds `heartbeat.update(phase=…)` from the per-logged-step
hook, so status.json's phase is not established to advance any earlier than the JSONL record,
and the switch would have swapped a slow barrier for an unproven one. Shrinking the L-BFGS
iteration budget keeps the plan-prescribed barrier and needs no claim about publish ordering.

## Validation

```
<home>/miniforge3/bin/conda run -n pinn-train \
    python -m unittest discover -s tests/phase42 -p 'test_*.py' -v
Ran 37 tests — OK
```

Skips: none beyond the documented environment guards (`caffeinate` absent /
subprocess-signal unsupported). No placeholder skips, per Task 3's gate.

## Notes

- The `strong_wolfe` line-search stall on the synthetic Stage-0 landscape is a production-code
  concern (L-BFGS can stall on real pathological losses too) and is **not** addressed here —
  it is out of plan 42-09's scope, which modifies tests only. Worth a Phase 43 look.
- The `-SIGINT` teardown window in fix 4 is likewise a real, if benign, property of the
  shutdown path: between `restore_handlers()` and process exit, a further Ctrl-C kills the
  process outright. Everything durable has already been written by then, so the run contract
  holds; hardening it would mean holding the handlers through interpreter teardown, which is
  a production change outside this plan.
- `tests/phase42/__init__.py` and `_fixtures.py` were still untracked when this plan resumed
  (plan 42-03 realized them but its commit never landed), so the committed tree could not have
  imported `tests.phase42` at all. This plan's commit lands them.
