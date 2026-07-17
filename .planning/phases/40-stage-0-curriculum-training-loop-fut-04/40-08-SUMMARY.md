---
phase: 40-stage-0-curriculum-training-loop-fut-04
plan: 08
subsystem: training
tags: [train-05, train-06, wr-01, wr-02, wr-03, wr-04, gap-closure, dtype-roundtrip, energy-floor, stagnation-halt, pinn-training-loop]

# Dependency graph
requires:
  - phase: 40-stage-0-curriculum-training-loop-fut-04 (plans 01-07)
    provides: GradClipper checkpoint surface; RunController._build_anchor_context; StageConfig provisional fields; StageExitMachine stagnation branch; CR-01/CR-02 recover-restore and boundary poll
provides:
  - "WR-01 closed: GradClipper state_dict/load_state_dict preserves run dtype via string-carried closed map (float32/float64)"
  - "WR-02 closed: eps_h reads StageConfig.energy_floor_factor; _EPS_H_SCALE_FACTOR removed"
  - "WR-03 closed: percentile_10_relaxation documented as owner-authorized degraded-advancement reserved seam (no auto wire, no HALT trigger)"
  - "WR-04 closed: stagnation-window HALT branch covered fire/no-fire/length-boundary"
affects: ["40-09 CR-03 stage_factory", "41 (resume/checkpoint dtype honesty)", "43 (ACC-05 calibration of energy_floor_factor + percentile_10_relaxation)"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Checkpoint dtype as plain string + closed 2-entry local map (weights_only-clean; never getattr(torch, untrusted))"
    - "Config-governed eps_h via nested StageConfig.energy_floor_factor with retained +1e-12 zero-denominator guard"
    - "Reserved-seam documentation for owner-only degraded advancement (no automatic consumer)"
    - "Stagnation HALT anti-vacuity via epoch_count < max_epochs (not val_stable=False alone)"

key-files:
  created:
    - .planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-08-SUMMARY.md
  modified:
    - pinn/training/grad_clip.py
    - pinn/training/controllers.py
    - pinn/training/config.py
    - tests/phase40/test_grad_clip.py
    - tests/phase40/test_optimizer_phase.py
    - tests/phase40/test_stage_exit.py

key-decisions:
  - "WR-01 uses state-carried dtype string + local closed map (not pinn.runtime; not RunController dtype threading)"
  - "WR-03 document-only disposition from ctl_instruction.md:1987-1997 — no automatic consumer, no HALT trigger (GAP-40-02 → A)"
  - "CR-03 / stage_factory deliberately out of scope (owned by 40-09); scheduled_weights.py and stage_exit.py byte-unchanged"

patterns-established:
  - "Gap-closure TDD for integrity findings: RED commit proves the defect, GREEN commit lands the minimal fix; SUMMARY records observed RED output"

requirements-completed: [TRAIN-05, TRAIN-06]

coverage:
  - id: D1
    description: "WR-01 / TRAIN-05: GradClipper checkpoint round trip preserves run dtype (float32 and float64); empty window round-trips; unknown dtype string raises ValueError naming it"
    requirement: "TRAIN-05"
    verification:
      - kind: unit
        ref: "tests/phase40/test_grad_clip.py#GradClipCheckpointRoundTripTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "WR-02 / TRAIN-06: StageConfig.energy_floor_factor governs eps_h in _build_anchor_context; default 1e-4 reproduces pre-fix scale; shadowing constant removed"
    requirement: "TRAIN-06"
    verification:
      - kind: unit
        ref: "tests/phase40/test_optimizer_phase.py#EnergyFloorFactorWiringTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "WR-03 / TRAIN-06: percentile_10_relaxation documented as reserved owner-authorized degraded-advancement seam; not wired; stage_exit.py unchanged"
    requirement: "TRAIN-06"
    verification:
      - kind: other
        ref: "pinn/training/config.py StageConfig.percentile_10_relaxation docstring; grep empty in stage_exit/controllers; existing test_config required-field coverage"
        status: pass
    human_judgment: false
  - id: D4
    description: "WR-04 / TRAIN-06: stagnation-window HALT fires when val never recovers running min for full window; companions for re-touch and length boundary; never ADVANCE"
    requirement: "TRAIN-06"
    verification:
      - kind: unit
        ref: "tests/phase40/test_stage_exit.py#StagnationWindowHaltTests"
        status: pass
    human_judgment: false

duration: 25min
completed: 2026-07-17
status: complete
---

# Phase 40 Plan 08: WR-01..WR-04 Integrity Gap Closure Summary

**Dtype-honest grad-clip resume, config-governed energy floor, reserved percentile-10 seam, and stagnation-HALT coverage**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-07-17T14:10:09Z
- **Completed:** 2026-07-17T14:18:00Z
- **Tasks:** 3
- **Files modified:** 6 code/test + SUMMARY/plan docs

## Accomplishments

- Closed **WR-01**: `GradClipper.state_dict` records window dtype as `"float32"`/`"float64"`; `load_state_dict` restores through a closed local map (T-40-11). Empty windows need no dtype. Unknown strings raise `ValueError` naming the value. No `pinn.runtime` import; clip formula / append-then-median / M1 non-finite contract untouched.
- Closed **WR-02**: `RunController._build_anchor_context` computes `eps_h = abs(h0) * float(self._config.stage.energy_floor_factor) + 1e-12`; deleted shadowing `_EPS_H_SCALE_FACTOR`. Default `1e-4` keeps the shipped scale.
- Closed **WR-03**: Documented `percentile_10_relaxation` as the owner-authorized degraded-advancement reserved seam (`ctl_instruction.md:1987-1997`); no automatic consumer, no HALT trigger, field remains CTX-39-required.
- Closed **WR-04**: Added fire / re-touch / length-boundary tests for the stagnation-window HALT branch; `stage_exit.py` byte-unchanged. Anti-vacuity is `epoch_count < max_epochs`.
- Full regression green: phase40 **156**, phase37 **55**, phase38 **128**, phase39 **264**. CR-01/CR-02 not regressed.

## Task Commits

Each task was committed atomically (TDD RED then GREEN for Tasks 1–2):

1. **Task 1 RED: WR-01 dtype round-trip tests** — `400b7757` (test)
2. **Task 1 GREEN: dtype-preserving load_state_dict** — `023db87d` (fix)
3. **Task 2 RED: energy_floor_factor override tests** — `a7928d75` (test)
4. **Task 2 GREEN: config-governed eps_h + WR-03 docstring** — `b9a4c657` (fix)
5. **Task 3: stagnation-window HALT coverage** — `b187daeb` (test)

**Plan metadata:** (this docs commit)

## Files Created/Modified

- `pinn/training/grad_clip.py` — string dtype in state_dict; closed-map restore (WR-01)
- `pinn/training/controllers.py` — eps_h from `energy_floor_factor`; remove `_EPS_H_SCALE_FACTOR` (WR-02)
- `pinn/training/config.py` — reserved-seam docstring for `percentile_10_relaxation` (WR-03)
- `tests/phase40/test_grad_clip.py` — `GradClipCheckpointRoundTripTests`
- `tests/phase40/test_optimizer_phase.py` — `EnergyFloorFactorWiringTests` + helper kwargs
- `tests/phase40/test_stage_exit.py` — `StagnationWindowHaltTests`

**Byte-unchanged (required):** `pinn/training/scheduled_weights.py`, `pinn/training/stage_exit.py`

## Decisions Made

- Followed plan mechanism for WR-01 (state-carried string + local closed dict); did not thread dtype from RunController or import `pinn.runtime`.
- Followed grounded WR-03 disposition: document only; no wire, no third HALT trigger (GAP-40-02 → A).
- Left CR-03 / stage_factory and related docstring corrections to **40-09**.

## Deviations from Plan

None — plan executed exactly as written.

### Observed RED output (required evidence)

**WR-01** (`GradClipCheckpointRoundTripTests` against pre-fix code):

```
FAIL: test_float32_round_trip_preserves_window_dtype_and_values
  AssertionError: 'dtype' not found in {'window': [3.0, 4.0, 5.0], ...}

FAIL: test_float32_clip_after_resume_matches_torch_median_reference
  AssertionError: torch.float64 != torch.float32

ERROR: test_float64_round_trip_preserves_window_dtype
  KeyError: 'dtype'

FAIL: test_unknown_dtype_string_raises_value_error_naming_it
  AssertionError: ValueError not raised

(empty-window case already OK pre-fix)
Ran 5 tests ... FAILED (failures=3, errors=1)
```

**WR-02** (`EnergyFloorFactorWiringTests` against pre-fix code):

```
OK: test_default_energy_floor_factor_matches_pre_fix_scale
FAIL: test_energy_floor_factor_override_changes_eps_h
  AssertionError: 110.000000000001 != 110000.0 within 12 places
  (override 1e-1 ignored; hardcoded 1e-4 still applied)
Ran 2 tests ... FAILED (failures=1)
```

## Post-fix suite counts

| Suite | Count | Result |
|-------|-------|--------|
| tests/phase40 | 156 | OK |
| tests/phase37 | 55 | OK |
| tests/phase38 | 128 | OK |
| tests/phase39 | 264 | OK |

Constraint greps: no `_EPS_H_SCALE_FACTOR` in controllers.py; no `percentile_10_relaxation` consumer in stage_exit.py/controllers.py; `scheduled_weights.py` and `stage_exit.py` diffs empty.

## Known Stubs

None introduced.

## Threat Flags

None beyond plan register. T-40-11 mitigated by closed dtype map + raise on unknown string.

## Self-Check: PASSED

- [x] `pinn/training/grad_clip.py` dtype map present; no hardcoded float64-only restore
- [x] Commits `400b7757`, `023db87d`, `a7928d75`, `b9a4c657`, `b187daeb` on branch
- [x] SUMMARY path exists
- [x] stage_exit.py / scheduled_weights.py unchanged
- [x] phase40 156 OK; CR-01/CR-02 tests still green via full suite
