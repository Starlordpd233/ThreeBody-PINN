---
phase: 49-conformance-gate
plan: 01
subsystem: conformance
tags: [phys-05, preflight, scheduled-weights, curriculum, pytest]

requires:
  - phase: 48-loss-math-conformance
    provides: "ScheduledWeights state_dict contract, locked loss catalog, and atomic artifact I/O"
provides:
  - "Exact PHYS-05 per-stage lambda-max table and locked lambda_data assertion"
  - "Fail-closed, deterministic preflight.json recorder/loader"
  - "Run-start and stage-boundary conformance-hook enforcement"
affects: [49-02, 49-03, 49-04, 49-05, 49-06, stage0-training]

actuals:
  tokens: 8683
  tasks: 3
  commits: 4

tech-stack:
  added: []
  patterns:
    - "state_dict-only exact table assertions with locked and advisory tiers"
    - "atomic sorted JSON event artifacts with fail-closed schema validation"

key-files:
  created:
    - pinn/conformance/__init__.py
    - pinn/conformance/table.py
    - pinn/conformance/preflight.py
    - tests/phase49/__init__.py
    - tests/phase49/test_gate01_table.py
  modified:
    - pinn/constants.py
    - pinn/train.py
    - pinn/training/controllers.py

key-decisions:
  - "The canonical PHYS-05 table remains separate from ScheduledWeights defaults; the gate reads live state_dict caps."
  - "lambda_ic is advisory while lambda_data is locked and checked from LossWeights dataclass metadata without constructing a weight object."
  - "Stage-2 refusal without a stage factory is preserved as the intended D-06 behavior."
  - "The D-31/SCOPE-32 minimum subset is shaped as a conformance module that later charter work can subsume."

patterns-established:
  - "Preflight refusal records a failed event before main() returns through finish_run."
  - "CurriculumController receives a keyword-only hook and passes its current scheduler after any stage rebind."

requirements-completed: [GATE-01]

coverage:
  - id: D1
    description: "Exact PHYS-05 table assertion reads ScheduledWeights.state_dict and enforces locked/advisory tiers."
    requirement: GATE-01
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate01_table.py - full suite"
        status: pass
      - kind: unit
        ref: "tests/phase49/test_gate01_table.py -k formula"
        status: pass
    human_judgment: false
  - id: D2
    description: "Run-start preflight persists passed and failed assertion evidence, including refusal-before-exit ordering."
    requirement: GATE-01
    verification:
      - kind: e2e
        ref: "tests/phase49/test_gate01_table.py::EntrypointTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "CurriculumController re-asserts entered stages and refuses an un-rebound Stage-2 scheduler."
    requirement: GATE-01
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate01_table.py -k stage2_fails or stage_boundary"
        status: pass
      - kind: unit
        ref: "tests/phase40/test_controllers.py tests/phase41/test_controllers_ext.py"
        status: pass
    human_judgment: false

duration: 50min
completed: 2026-08-04
status: complete
---

# Phase 49 Plan 01: Conformance Gate Summary

**Exact PHYS-05 table enforcement with deterministic preflight evidence at run start and curriculum stage boundaries**

## Performance

- **Duration:** ~50 min
- **Started:** 2026-08-04T20:30:00-07:00
- **Completed:** 2026-08-04T20:40:00-07:00
- **Tasks:** 3
- **Files modified:** 8

## Accomplishments

- Added the seven-stage PHYS-05 lambda table, exact equality checks, warmup formula validation, and locked `lambda_data` metadata check.
- Added atomic, sorted, schema-versioned `preflight.json` recording with recursive Phase-46 `gate_*` key rejection and artifact-first refusal evidence.
- Wired one run-start composition entry point and a keyword-only `CurriculumController` hook at both stage dispatch sites; proved the intentional Stage-2 refusal without a stage factory.
- Added dataset-free tests for pass/trip paths, state_dict-vs-current behavior, one-ulp exactness, advisory lambda_IC, formula identity, data-term validation, ordering, and deterministic serialization.

## Task Commits

1. **Task 1: End-to-end PHYS-05 table gate at run start** - `12cb85ce` (RED tests), `d126a212` (implementation)
2. **Task 2: Stage-boundary re-assertion and D-06 refusal** - `2b62d150` (stage-hook tests; implementation is included in the tracer's coupled source commit `d126a212`)
3. **Task 3: Exactness, formula, and advisory trip coverage** - `374edd31`

## Files Created/Modified

- `pinn/constants.py` - PHYS-05 canonical literals and provenance comments.
- `pinn/conformance/table.py` - exact state-dict table assertion and locked/advisory checks.
- `pinn/conformance/preflight.py` - atomic recorder, fail-closed loader, and run-start composition seam.
- `pinn/train.py` - run-start refusal path and stage-boundary hook closure.
- `pinn/training/controllers.py` - keyword-only conformance hook at top-of-step and post-rebind points.
- `tests/phase49/test_gate01_table.py` - complete GATE-01 unit and entrypoint coverage.

## Decisions Made

- Kept stage-specific values out of `ScheduledWeights`; conformance compares its live serialized state to the canonical table.
- Treated `lambda_ic` as advisory per D-03, while checking `lambda_data` as a locked, side-effect-free dataclass default.
- Preserved the no-factory Stage-2 refusal rather than introducing prohibited multi-stage platform behavior.

## Deviations from Plan

### Sequencing deviation

The `CurriculumController` hook implementation landed in the Task-1 tracer source commit (`d126a212`) because the run-start closure and controller seam are coupled through `pinn/train.py`; Task 2's dedicated commit contains its stage-boundary trip and ordering tests.

### Existing-suite contract conflict

`tests/phase41/test_train_entrypoint.py` retains a fixture with `loss.lambda_e_max: 1.0`, which now correctly violates the locked Stage-0 PHYS-05 row (`0.0`). Its 16 launch-based tests therefore return the new fail-closed refusal. The fixture is outside this plan's owned paths and was intentionally not changed; the focused Phase-49 and controller suites remain green.

## Issues Encountered

- The phase41 fixture conflict above is the only known regression. No changes were made to `pinn/training/slbfgs_preflight.py` or `pinn/training/scheduled_weights.py`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

The `run_start_preflight(config, scheduled_weights, run_dir)` seam is ready for the census/register composition in Plan 49-04, and the recorder is available for later stage-boundary and runtime evidence extensions.

## Self-Check: PASSED

- Summary file exists at the required phase path.
- Commits `12cb85ce`, `d126a212`, `2b62d150`, and `374edd31` exist in git history.
- `git diff --check` reports no whitespace errors for the summary.

---
*Phase: 49-conformance-gate*
*Completed: 2026-08-04*
