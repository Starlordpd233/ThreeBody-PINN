---
phase: 48-loss-math-conformance
plan: 01
subsystem: training-losses
tags: [pytorch, controller, causal-loss, huber, conformance, tdd]

# Dependency graph
requires:
  - phase: 47-frame-completion-s-h-pipeline
    provides: Run-level eps_H assembly and its boundary regression proof
provides:
  - Controller-side Rbar assembly using one vector-space average per time index
  - Explicit owner-ratified mean-Huber denominator provenance
  - Dataset-free assembly-boundary and hand-oracle regression coverage
affects: [48-02, 48-03, 48-04, phase-49-invariant-enforcement]

# Actuals (#2632)
actuals:
  tokens: 2023
  tasks: 2
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Real controller-to-catalog seam interception with synthetic residuals
    - Independent float64 elementwise Huber oracle over 9*N_t entries

key-files:
  created:
    - tests/phase48/__init__.py
    - tests/phase48/test_loss_math_conformance.py
  modified:
    - pinn/training/controllers.py
    - pinn/loss_catalog.py

key-decisions:
  - "Rbar is assembled as sum(residual**2, body/component)/3 before the existing causal consumer."
  - "data_huber_loss retains .mean(), explicitly documented as sum(Huber)/(9*N_t) under GAP-45-01/D-01."
  - "No neighboring loss path, lambda, training run, evaluator, or framework spec was changed."

patterns-established:
  - "Assembly-boundary probes must intercept the actual controller-to-catalog argument."
  - "Math conformance tests use independent float64 hand oracles rather than copied production helpers."

requirements-completed: [CONF-04, CONF-07, TEST-02]

coverage:
  - id: D1
    description: "Controller passes exact /3 Rbar through the real causal_physics_loss seam."
    requirement: CONF-04
    verification:
      - kind: integration
        ref: "tests/phase48/test_loss_math_conformance.py#test_rbar_assembly_value"
        status: pass
      - kind: unit
        ref: ".venv/bin/python -m pytest -q tests/phase40/test_controllers.py tests/phase41/test_controllers_ext.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "Mean-Huber data loss matches an independent sum/(9*N_t) oracle across both branches and multiple time counts."
    requirement: CONF-07
    verification:
      - kind: unit
        ref: "tests/phase48/test_loss_math_conformance.py#test_data_huber_mean_matches_hand_oracle"
        status: pass
      - kind: unit
        ref: ".venv/bin/python -m pytest -q tests/phase38/test_loss_catalog.py tests/phase40/test_optimizer_phase.py -k 'data_huber or chunked_accumulation'"
        status: pass
    human_judgment: false
  - id: D3
    description: "Existing eps_H assembly proof remains green alongside the new Rbar boundary proof."
    requirement: TEST-02
    verification:
      - kind: integration
        ref: "tests/phase47/test_conf03_eps_h_wiring.py#test_eps_h_assembly_value"
        status: pass
      - kind: other
        ref: ".venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py tests/phase38/test_loss_catalog.py tests/phase47/test_conf03_eps_h_wiring.py tests/phase40/test_controllers.py tests/phase41/test_controllers_ext.py tests/phase40/test_optimizer_phase.py"
        status: pass
    human_judgment: false

# Metrics
duration: 7 min
completed: 2026-08-03
status: complete
---

# Phase 48 Plan 01: Loss-Math Conformance Summary

**Controller Rbar now follows the locked /3 vector-space reduction, while mean-Huber L_data remains numerically unchanged and independently defended.**

## Performance

- **Duration:** 7 min
- **Started:** 2026-08-03T01:19:45Z
- **Completed:** 2026-08-03T01:26:56Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Corrected `RunController._non_data_terms` to pass `(residual ** 2).sum(dim=(-2, -1)) / 3.0` into the existing `causal_physics_loss` consumer.
- Documented the owner-ratified `data_huber_loss` reduction as `sum(Huber)/(9*N_t)` without changing `.mean()` numeric behavior.
- Added dataset-free, train-free assembly-boundary and independent float64 Huber oracle tests; retained the Phase 47 `eps_H` boundary proof.

## Task Commits

Each task was committed atomically (Task 1 used the required RED/GREEN gates):

1. **Task 1 RED: Carry one exact Rbar value through controller loss assembly** - `cf225bd7` (test)
2. **Task 1 GREEN: Carry one exact Rbar value through controller loss assembly** - `4f707510` (feat)
3. **Task 2: Lock the existing mean-Huber L_data contract with a hand oracle** - `ce22991e` (docs)

## Files Created/Modified

- `pinn/training/controllers.py` - Produces the canonical per-time `/3` residual statistic.
- `pinn/loss_catalog.py` - Records the explicit mean-Huber denominator/provenance.
- `tests/phase48/__init__.py` - Declares dataset-free/train-free Phase 48 test scope.
- `tests/phase48/test_loss_math_conformance.py` - Intercepts Rbar at the real controller seam and checks independent Huber oracles.

## Decisions Made

- Preserved the existing causal catalog consumer and downstream weighted mean; only the upstream controller reduction changed.
- Preserved the existing mean-Huber implementation because it already equals the owner-ratified `sum(Huber)/(9*N_t)` value.
- Kept all work inside Plan 48-01; no training/evaluation run, framework-spec edit, recipe tuning, Phase 49 enforcement, or neighboring verified-clean loss rewrite was performed.

## Deviations from Plan

None - plan executed exactly as written. The shared Phase 48 test module was created in the Task 1 RED commit and includes Task 2's independent oracle because both tasks own the same test file; Task 2 therefore needed only its planned provenance-only source edit.

## Issues Encountered

None. The expected RED failure demonstrated the pre-change `/9` behavior, then the targeted and full Plan 48-01 regression suites passed after the fix.

## Auth Gates

None - no external service or authentication was required.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. Synthetic fixture data is intentional test isolation, not a production stub.

## Next Phase Readiness

Plan 48-01 is complete and ready for the remaining Phase 48 plans. The controller now supplies the conformant upstream Rbar statistic that later causal-clip work consumes.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/48-loss-math-conformance/48-01-SUMMARY.md`.
- Task commits `cf225bd7`, `4f707510`, and `ce22991e` are present in Git history.
- `git diff --check` passes.

---
*Phase: 48-loss-math-conformance*
*Plan: 01*
*Completed: 2026-08-03*
