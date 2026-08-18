---
phase: 48-loss-math-conformance
plan: 03
subsystem: training-losses
tags: [pytorch, causal-loss, mps, metadata, conformance, tdd]

# Dependency graph
requires:
  - phase: 48-loss-math-conformance
    provides: Corrected controller-side /3 Rbar producer from Plan 48-01
provides:
  - Dtype/backend-derived causal exponent floor with strict-positive weights
  - Strict atomic training metadata provenance and resume binding for causal clip facts
  - CPU float32/float64 and real MPS float32 conformance/refusal coverage
affects: [phase-49-conformance-gate, phase-50-valid-stage-0-rerun]

# Actuals (#2632)
actuals:
  tokens: 10515
  tasks: 2
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Directed-up active-dtype log-tiny floor before causal exponentiation
    - Exact five-field runtime fact binding through atomic metadata and resume validation
    - Real MPS target-backend probe alongside CPU dtype matrix

key-files:
  created:
    - tests/phase48/test_clip_metadata.py
  modified:
    - pinn/loss_catalog.py
    - pinn/train.py
    - pinn/training/run_metadata.py
    - tests/phase38/test_loss_catalog.py
    - tests/phase47/test_conf02_s_h_pipeline.py
    - tests/phase47/test_conf03_eps_h_wiring.py
    - tests/phase48/test_loss_math_conformance.py

key-decisions:
  - "The causal exponent floor is derived from mathematical log(finfo(dtype).tiny), rounded in the active dtype/device, and advanced once with nextafter toward positive infinity when the initial representation is below the bound."
  - "Fresh and resumed setup paths derive the same five clip facts from the effective RuntimeSpec and enforce them through the existing strict training_metadata.json artifact before controller construction."
  - "The minimum weight remains an active-backend fact: CPU and MPS float32 exp kernels differ by one ulp, so resume compares the recorded value against the live runtime rather than regenerating it on another backend."

patterns-established:
  - "Causal conformance tests exercise no-op and former-underflow prefixes, detached exclusive-prefix gradients, sorted-time semantics, and real controller assembly."
  - "Metadata refusal tests name the offending field and direct operators to regenerate fresh setup artifacts instead of hand-editing."

requirements-completed: [CONF-05, TEST-01]

coverage:
  - id: D1
    description: "Runtime-derived causal clip facts clamp the loss exponent before exp and preserve w_1 = 1 with strict 0 < w_n <= 1 across CPU float32/float64 and real MPS float32."
    requirement: CONF-05
    verification:
      - kind: unit
        ref: "tests/phase48/test_loss_math_conformance.py#test_causal_clip_cpu_dtype_matrix"
        status: pass
      - kind: integration
        ref: "tests/phase48/test_loss_math_conformance.py#test_causal_clip_controller_seam"
        status: pass
      - kind: other
        ref: "<home>/miniforge3/bin/conda run -n pinn-train python -c '<locked torch 2.12.1 real MPS causal probe>'"
        status: pass
    human_judgment: false
  - id: D2
    description: "The strict training metadata artifact records and reloads the exact five causal clip facts, while fresh/resume mismatch, schema, field, and corruption cases fail closed with regeneration guidance."
    requirement: CONF-05
    verification:
      - kind: integration
        ref: "tests/phase48/test_clip_metadata.py#test_causal_clip_fresh_metadata_roundtrip"
        status: pass
      - kind: unit
        ref: "tests/phase48/test_clip_metadata.py#test_causal_clip_metadata_refuses_invalid_content"
        status: pass
    human_judgment: false
  - id: D3
    description: "The directly divergent zero-underflow expectation is corrected and Phase-47 metadata fixtures retain S_H and eps_H regression assertions under schema v2."
    requirement: TEST-01
    verification:
      - kind: unit
        ref: ".venv/bin/python -m pytest -q tests/phase38/test_loss_catalog.py tests/phase47/test_conf02_s_h_pipeline.py tests/phase47/test_conf03_eps_h_wiring.py tests/phase48/test_loss_math_conformance.py tests/phase48/test_clip_metadata.py"
        status: pass
    human_judgment: false

# Metrics
duration: 14 min
completed: 2026-08-03
status: complete
---

# Phase 48 Plan 03: Loss-Math Conformance Summary

**Causal supervision now has a dtype/backend-derived positive floor with exact strict metadata provenance and CPU/MPS conformance coverage.**

## Performance

- **Duration:** 14 min
- **Started:** 2026-08-03T01:58:24Z
- **Completed:** 2026-08-03T02:12:24Z
- **Tasks:** 2
- **Files modified:** 8

## Accomplishments

- Added `resolve_causal_clip_facts` as the single source for active-dtype directed-up `log(finfo.tiny)` floors, formula/provenance identifiers, and minimum weights; `causal_physics_loss` clamps before exponentiation while retaining detached exclusive prefixes and the downstream mean.
- Extended `training_metadata.json` to schema v2 with exact causal precision, exponent floor, minimum weight, formula, and provenance fields; fresh writes are atomic and resumed runs re-derive and compare every field before controller construction.
- Added CPU float32/float64 boundary, no-op, former-underflow, sorted-time, detached-prefix, controller-seam, and real MPS float32 tests; corrected the old Phase-38 zero-weight assertion and updated Phase-47 metadata fixtures.

## Task Commits

Each task was committed atomically; Task 1 used the required RED/GREEN gates:

1. **Task 1 RED: Add causal clip lifecycle red gate** - `cbb78e24` (test)
2. **Task 1 GREEN: Bind runtime causal clip facts** - `513fe74b` (feat)
3. **Task 2: Cover causal clip dtype and metadata refusal matrix** - `bc6e5d3a` (test)

**Plan metadata:** final GSD state/roadmap/requirements metadata is committed separately with this summary.

## Files Created/Modified

- `pinn/loss_catalog.py` - Owns causal clip constants, fact derivation, and clamp-before-exp execution.
- `pinn/train.py` - Derives facts from the effective RuntimeSpec and binds them in fresh/resume metadata setup.
- `pinn/training/run_metadata.py` - Enforces schema v2, exact clip fields, atomic writes, and fail-closed resume matching.
- `tests/phase48/test_loss_math_conformance.py` - Covers CPU dtype matrix, MPS arm, detached-prefix behavior, and real controller seam.
- `tests/phase48/test_clip_metadata.py` - Covers fresh/resume round-trip and strict refusal matrix.
- `tests/phase38/test_loss_catalog.py` - Replaces obsolete exact-zero causal-weight expectation with strict positivity.
- `tests/phase47/test_conf02_s_h_pipeline.py` - Updates schema-v2 metadata fixtures while retaining S_H checks.
- `tests/phase47/test_conf03_eps_h_wiring.py` - Updates resume fixture binding while retaining eps_H assertions.

## Decisions Made

- Used the active dtype's mathematical `log(torch.finfo(dtype).tiny)` with upward-directed representable rounding, never an observed-outcome or user-tunable threshold.
- Kept the five persisted fields in the existing atomic `training_metadata.json` artifact; no sidecar, config knob, or alternate provenance source was introduced.
- Compared the recorded minimum weight against the live expected runtime on resume because CPU and MPS float32 exponential kernels differ by one ulp while sharing the same exponent floor.

## TDD Gate Compliance

- Task 1 RED failed at collection because the clip helper and metadata arguments were absent; Task 1 GREEN passed the tracer tests and was committed as `513fe74b`.
- Task 2 expanded coverage around the already-implemented behavior and corrected existing fixtures; its commit is a test commit with one Rule-1 backend-validation fix. No separate pre-implementation RED commit was needed for a new production behavior in this expansion task.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Preserve backend-specific float32 minimum-weight provenance**
- **Found during:** Task 2 (dtype/backend matrix and MPS metadata round-trip)
- **Issue:** torch 2.12.1's CPU and MPS float32 `exp(floor)` results differ by one ulp. Recomputing the minimum weight with a CPU kernel in the metadata validator would reject a valid real-MPS artifact.
- **Fix:** Validate the dtype-derived floor and field ranges centrally, then compare all five fields to the live runtime mapping; do not regenerate the backend-specific minimum weight on another backend.
- **Files modified:** `pinn/training/run_metadata.py`
- **Verification:** Real MPS metadata round-trip plus the locked direct MPS causal probe passed.
- **Committed in:** `bc6e5d3a`

---

**Total deviations:** 1 auto-fixed (Rule 1: 1)
**Impact on plan:** Necessary to preserve the required active-backend provenance; no scope expansion or new tuning surface.

## Issues Encountered

None beyond the backend-specific validation bug documented above. No authentication gate, package installation, training run, held-out evaluation, framework-spec edit, or source-silent adjudication gap occurred.

## Auth Gates

None - no external service or authentication was required.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. The synthetic sources and former-underflow residuals are intentional dataset-free conformance fixtures, not production placeholders.

## Next Phase Readiness

CONF-05 and TEST-01 are implemented and defended across the required CPU/MPS matrix. Plan 48-04 remains the next unexecuted plan; no training or evaluation was launched.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/48-loss-math-conformance/48-03-SUMMARY.md`.
- Task commits `cbb78e24`, `513fe74b`, and `bc6e5d3a` are present in Git history.
- Locked torch 2.12.1/MPS preflight and direct probe pass.
- Plan-scoped pytest verification passes (54 passed, 2 subtests).
- `git diff --check` passes.

---
*Phase: 48-loss-math-conformance*
*Plan: 03*
*Completed: 2026-08-03*
