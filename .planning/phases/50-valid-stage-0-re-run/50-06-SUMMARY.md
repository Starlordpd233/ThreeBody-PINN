---
phase: 50-valid-stage-0-re-run
plan: 06
subsystem: training-runtime
tags: [pinn, mps, validation-gate, causal-telemetry, diagnosis, conformance-repair]

requires:
  - phase: 50-valid-stage-0-re-run
    provides: generation-3 terminal record, GAP-50-03 Option A, 50-03 terminal evidence
provides:
  - "MPS-safe detach-CPU-then-float64 prediction normalization in compute_validation_gate"
  - "Deterministic training-owned causal telemetry across validation-step logging"
  - "Bounded diagnosis with grounded_causal_front_repair: none-in-current-sources"
affects: [50-07-normal-evidence-tooling, 50-08-owner-checkpoint]

actuals:
  tokens: 11000
  tasks: 3
  commits: 5

tech-stack:
  added: []
  patterns:
    - "Match gate_metrics _as_cpu_f64 order for any backend tensor entering the validation metric"
    - "Snapshot training causal stash before validation compose; pass explicit _log_step kwargs"
    - "Classify conversion, telemetry overwrite, and causal-front remedy as three separate findings"

key-files:
  created:
    - tests/phase50/test_causal_telemetry.py
    - .planning/phases/50-valid-stage-0-re-run/evidence/causal-front-diagnosis.md
    - .planning/phases/50-valid-stage-0-re-run/50-06-SUMMARY.md
  modified:
    - pinn/training/validation_gate.py
    - pinn/training/controllers.py
    - tests/phase46/test_gate_composition.py
    - tests/phase46/test_validation_wiring.py

key-decisions:
  - "MPS prediction conversion follows detach then CPU then float64; metric/frame/population/thresholds unchanged"
  - "telemetry_overwrite_proven: true on Adam and L-BFGS validation-step logs; snapshot repair only"
  - "grounded_causal_front_repair: none-in-current-sources; later_generation_likelihood_claim: prohibited"
  - "REQUIREMENTS.md RUN-01 checkbox not flipped (D-30); this plan is a conformance repair, not experiment completion"

patterns-established:
  - "Target-host MPS regressions must assert availability rather than skip"
  - "Causal-front HALT evidence is recorded separately from telemetry provenance"

requirements-completed: []

coverage:
  - id: D1
    description: "MPS float32 predictions are detached, moved to CPU, then cast to float64 before the unchanged validation metric; production wiring publishes a healthy sidecar"
    requirement: RUN-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_gate_composition.py#test_mps_float32_prediction_is_detached_cpu_then_float64_before_metric"
        status: pass
      - kind: unit
        ref: "tests/phase46/test_validation_wiring.py#test_production_mps_path_publishes_and_revalidates_sidecar"
        status: pass
    human_judgment: false
  - id: D2
    description: "Training-step causal statistics passed to StepGuards and written to the step record stay training-owned when validation runs between them"
    requirement: RUN-01
    verification:
      - kind: unit
        ref: "tests/phase50/test_causal_telemetry.py#test_adam_validation_step_keeps_training_owned_causal_telemetry"
        status: pass
      - kind: unit
        ref: "tests/phase50/test_causal_telemetry.py#test_lbfgs_validation_step_keeps_training_owned_causal_telemetry"
        status: pass
    human_judgment: false
  - id: D3
    description: "Diagnosis records grounded_causal_front_repair: none-in-current-sources and leaves later-generation authorization to Plan 50-08"
    verification:
      - kind: other
        ref: ".planning/phases/50-valid-stage-0-re-run/evidence/causal-front-diagnosis.md"
        status: pass
    human_judgment: true
    rationale: "The no-remedy classification is a source-grounding record, not a numeric test; the owner still owns the later-generation decision"

duration: 11min
completed: 2026-08-15
status: complete
---

# Phase 50 Plan 06: MPS Conversion, Causal Telemetry, and Bounded Diagnosis Summary

**Repaired the MPS validation conversion and the proven training-versus-validation causal-telemetry overwrite, then recorded that current sources contain no independently grounded causal-front behavioral repair.**

## Performance

- **Duration:** 11 min
- **Started:** 2026-08-15T12:53:26Z
- **Completed:** 2026-08-15T13:04:09Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Closed the locked-host TypeError: `compute_validation_gate` now detaches the prediction, moves it to CPU, then casts to `float64` before the unchanged `gate_metrics` consumer. A production-path MPS regression publishes and revalidates a sidecar; an MPS skip is an assertion failure.
- Proved that validation compose overwrote `_last_widened_details` between StepGuards and `_log_step` on both Adam and L-BFGS validation-step boundaries (`telemetry_overwrite_proven: true`). Snapshotted training `w_n_stats` and residuals immediately after the training compose and passed those explicit values to `_log_step`.
- Wrote `evidence/causal-front-diagnosis.md` with `grounded_causal_front_repair: none-in-current-sources` and `later_generation_likelihood_claim: prohibited`. Did not reopen GAP-50-03, launch a run, or change `N`/recipe/config.

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: failing MPS conversion regression** - `7a587f9f` (test)
2. **Task 1 GREEN: CPU-before-float64 prediction conversion** - `169b7abe` (feat)
3. **Task 2 RED: failing causal telemetry ownership regression** - `9b0311d7` (test)
4. **Task 2 GREEN: training causal snapshot before validation** - `1c4836cb` (feat)
5. **Task 3: bounded diagnosis + this SUMMARY** - this commit (fix/docs)

**Plan metadata:** this commit

_Note: TDD tasks produced RED then GREEN commits._

## Files Created/Modified

- `pinn/training/validation_gate.py` - detach → CPU → float64 prediction normalization
- `pinn/training/controllers.py` - immutable training causal snapshot passed to `_log_step`
- `tests/phase46/test_gate_composition.py` - target-MPS metric-input regression
- `tests/phase46/test_validation_wiring.py` - production MPS sidecar wiring regression
- `tests/phase50/test_causal_telemetry.py` - training-versus-validation sentinel ownership
- `.planning/phases/50-valid-stage-0-re-run/evidence/causal-front-diagnosis.md` - bounded diagnosis
- `.planning/phases/50-valid-stage-0-re-run/50-06-SUMMARY.md` - this summary

## Decisions Made

- Validation conversion is a D-19 conformance repair justified by the existing `_as_cpu_f64` contract, not by the seed-41 HALT number.
- Telemetry repair was taken only after the new regression failed on the current implementation. Guard ordering and the causal formula were left unchanged.
- No causal-front behavioral remedy exists in current sources. Plan 50-08 owns the owner decision on any later generation.

## Deviations from Plan

None - plan executed exactly as written.

**Total deviations:** 0
**Impact on plan:** None.

## Issues Encountered

None beyond the already-known generation-3 invariant-B HALT and validation TypeError. Those remain historical facts; GAP-50-03 Option A is untouched.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for Plan 50-07 (normal evidence tooling) and Plan 50-08 (owner checkpoint). No smoke, graded seed, or generation-4 preregistration is authorized by this plan. RUN-01/RUN-02 remain unflipped. `final_band_generation` remains null.

## Self-Check: PASSED

- `tests.phase46.test_gate_composition` + `tests.phase46.test_validation_wiring` + `tests.phase50.test_causal_telemetry`: 49 passed, including the new MPS and telemetry regressions.
- `git log --oneline --grep=50-06` returns the Task 1/2 commits plus this close-out.
- Diagnosis contains `grounded_causal_front_repair: none-in-current-sources` and `later_generation_likelihood_claim: prohibited`.
- No recipe, config, threshold, seed-order, or evaluation artifact changed.

---
*Phase: 50-valid-stage-0-re-run*
*Completed: 2026-08-15*
