---
phase: 49-conformance-gate
plan: 02
subsystem: training-runtime
tags: [GATE-03, StepGuards, causal-weights, YAML, conformance]

# Dependency graph
requires:
  - phase: 49-conformance-gate
    provides: PHYS-05 run-start gate and existing StepGuards machinery from 49-01
provides:
  - Typed optional run.invariants.front_advance_window_n config owner slot
  - HALT-family invariant_a, invariant_b, and causal_stats_missing StepGuards
  - Guard-hook wiring for existing per-step causal statistics and collocation length
affects: [49-03 checkpoint resume, GATE-03 verification, Stage-0 conformance run]

# Actuals (#2632)
actuals:
  tokens: 7058
  tasks: 3
  commits: 6

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Optional owner-owned threshold uses None as explicit record-only state"
    - "Conformance invariants extend the existing HALT-family StepGuards path"
    - "Guard hook consumes controller._last_widened_details without new threading"

key-files:
  created:
    - tests/phase49/test_gate03_invariants.py
  modified:
    - pinn/training/config.py
    - pinn/training/config_yaml.py
    - pinn/training/guards.py
    - pinn/train.py
    - configs/stage0-example.yaml
    - configs/smoke.yaml

key-decisions:
  - "front_advance_window_n remains unset by default; None records invariant-B state without HALT"
  - "Invariant A/B and causal_stats_missing are HALT-family entries in StepGuards; RECOVER is never used"
  - "Existing STEP_LOG_FIELDS and failure-bundle paths remain unchanged"

patterns-established:
  - "Invariant B tracks a monotone front high-water mark and serializes state for plan 49-03"
  - "Physics-evaluated steps treat missing causal statistics as an explicit HALT"

requirements-completed: [GATE-03]

coverage:
  - id: D1
    description: "Optional InvariantsConfig validates the owner slot and fail-closed YAML mapping"
    requirement: GATE-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate03_invariants.py -k invariants_config"
        status: pass
      - kind: unit
        ref: "tests/phase40/test_config.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "Invariant A/B and causal_stats_missing trip HALT with saturation, high-water, and record-only coverage"
    requirement: GATE-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate03_invariants.py"
        status: pass
      - kind: unit
        ref: "tests/phase41/test_guards.py"
        status: pass
    human_judgment: false
  - id: D3
    description: "guard_hook forwards existing causal statistics and collocation length while retaining failure bundles"
    requirement: GATE-03
    verification:
      - kind: integration
        ref: "tests/phase49/test_gate03_invariants.py -k guard_hook"
        status: pass
      - kind: other
        ref: "step-log prefix grep and git diff immutability gate"
        status: pass
    human_judgment: false

# Metrics
duration: 7min
completed: 2026-08-04
status: complete
---

# Phase 49 Plan 02: GATE-03 Runtime Invariants Summary

**Typed record-only-until-owned-N invariant configuration, HALT-family causal-weight guards, and existing-statistics guard-hook wiring**

## Performance

- **Duration:** 7 minutes
- **Started:** 2026-08-04T22:05:31-07:00
- **Completed:** 2026-08-04T22:12:19-07:00
- **Tasks:** 3
- **Files modified:** 6 (plus one new test file)

## Accomplishments

- Added frozen `InvariantsConfig` with strict positive-int validation only when the owner supplies `front_advance_window_n`; `None` is a valid D-20 record-only state.
- Added `invariant_a`, `invariant_b`, and `causal_stats_missing` to the existing HALT-family `StepGuards` machinery, including monotone high-water state accessors for the next checkpoint plan.
- Wired `guard_hook` to the controller’s existing `_last_widened_details` statistics and per-step residual-bin length without changing `STEP_LOG_FIELDS` or the failure-bundle path.
- Added trip-focused tests for every new failure branch, invariant-B saturation/high-water behavior, record-only operation, YAML fail-closed parsing, and wiring-level statistics absence.

## Task Commits

Each TDD task was committed atomically (RED test followed by GREEN implementation):

1. **Task 1 RED:** add failing invariants config tests - `0e399d82`
2. **Task 1 GREEN:** add typed GATE-03 invariant config - `e0a69e45`
3. **Task 2 RED:** add failing runtime invariant tests - `0cb7f5ed`
4. **Task 2 GREEN:** enforce GATE-03 runtime invariants - `d067c2ee`
5. **Task 3 RED:** add guard hook wiring tests - `096371f2`
6. **Task 3 GREEN:** wire causal stats into guard hook - `25a59828`

## Files Created/Modified

- `pinn/training/config.py` - Optional typed invariant-B owner slot and `RunConfig.invariants` validation.
- `pinn/training/config_yaml.py` - Nested `InvariantsConfig` resolver registration.
- `pinn/training/guards.py` - Three HALT-family GATE-03 guards and serializable invariant-B state.
- `pinn/train.py` - Existing controller causal-statistics extraction and guard-hook forwarding.
- `configs/stage0-example.yaml` - Empty D-20 owner slot.
- `configs/smoke.yaml` - Empty D-20 owner slot.
- `tests/phase49/test_gate03_invariants.py` - Config, guard, state, and wiring coverage.

## Decisions Made

- Kept `front_advance_window_n` unset in shipped configs; no agent-selected or provisional N was introduced.
- Used the existing `StepGuards` ordering, family classification, HALT precedence, and failure bundle rather than creating a second guard path.
- Used the existing per-step causal statistics as the wiring source and did not add a JSONL field or second log.

## Deviations from Plan

None - implementation followed the plan. The only unresolved owner choice remains the intentionally unset N, which is the defined D-20 state rather than an implementation deviation.

## Issues Encountered

- The plan’s import smoke names `load_training_config`, but the repository’s established API is `load_config`; the supported import was verified successfully and no unrelated alias was added.
- `tests/phase41/test_train_entrypoint.py` remains red in 16 tests because its pre-existing fixtures omit the 49-01 PHYS-05 `lambda_e_max: 0.0` contract (`expected 0.0, actual 1.0`). This is outside Plan 49-02’s owned scope; `tests/phase41/test_guards.py` remains green.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 49-03 can thread `invariant_b_state_dict()` and `load_invariant_b_state()` through the checkpoint payload. The owner-controlled N remains intentionally unset, so invariant B is record-only and the single-evaluation precondition remains ineligible until owner ratification.

## Self-Check: PASSED

- Summary file exists at the required phase path.
- All six TDD task commit hashes are present in repository history.

---
*Phase: 49-conformance-gate*
*Completed: 2026-08-04*
