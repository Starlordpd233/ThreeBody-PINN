---
phase: 55-architecture-characterization-probe
plan: 01
subsystem: testing
tags: [pinn, verification, architecture-characterization, causal-weights, inst-04]

requires:
  - phase: 38-pinn-model-rebuild-from-specs-fut-01
    provides: ArchitectureSpec, build_network, componentwise_du, softened_acceleration
  - phase: 40-train-adam-lbfgs-stage0-loop
    provides: causal_physics_loss, CollocationSampler, trainer residual composition
affects: [56-contract-amendment-train-free-gate, 55-02, 55-03, 55-04]

provides:
  - SweepCase frozen validated input dataclass
  - ArchitectureCharacterizationResult frozen output dataclass
  - DEFAULT_CASES six audited rows as run_sweep default
  - measure_case initialization-only seven-quantity pipeline
  - run_sweep multi-case driver
  - tests/phase55 tracer, Tier-1 invariant, SC3 mutation, and re-homed prohibition suite

actuals:
  tokens: 6461
  tasks: 3
  commits: 3
plan_head_before: 0c0edd9cc69ecc2f060c0a317220c36fa253a461

tech-stack:
  added: []
  patterns:
    - derive-from-trainer-primitives (SC3 mutation proof)
    - numpy.median even-N convention
    - dtype-derived causal clamp floor via resolve_causal_clip_facts
    - DEFAULT_CASES as data, not a parallel code path (D-02)

key-files:
  created:
    - pinn/verification/architecture_characterization_probe.py
    - tests/phase55/__init__.py
    - tests/phase55/test_architecture_characterization.py
  modified: []

key-decisions:
  - "D-01 tier 1: invariant-bound suite over all six audited cases, not exact-value fixtures"
  - "D-02: DEFAULT_CASES is run_sweep's default argument, not a hard-coded second path"
  - "Even-N median is numpy.median (mean of two central order statistics), not torch.median"

patterns-established:
  - "Pattern: measure_case mirrors controllers.py traj / componentwise_du / softened_acceleration / rbar / causal_physics_loss composition with data and optimizer removed"
  - "Pattern: front_idx is the trainer max(n for w > 0.5, default=-1) formula"
  - "Pattern: Phase-38 glob checks that 55-02 will exclude are re-homed in tests/phase55 before the exclusion lands"

requirements-completed: [INST-04]

coverage:
  - id: D1
    description: measure_case reports all seven INST-04 quantities for one seeded case at initialization with no data, optimizer, or training step
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_tracer_single_case_reports_all_seven_quantities
        status: pass
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_tracer_case_is_deterministic_across_two_calls
        status: pass
    human_judgment: false
  - id: D2
    description: run_sweep() with no arguments measures the six audited cases and satisfies Tier-1 invariant bounds
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_invariant_bounds_six_cases
        status: pass
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_default_cases_are_the_six_audited_rows
        status: pass
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_causal_weights_pinned_at_dtype_clamp_floor
        status: pass
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_norm_convention_matches_audit_rbar_identity
        status: pass
    human_judgment: false
  - id: D3
    description: Probe quantities move in lock-step when trainer primitives are mutated, proving SC3 derivation
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_derives_from_trainer_implementation
        status: pass
    human_judgment: false
  - id: D4
    description: SweepCase fail-closed validation rejects malformed label, seed, masses, and ic13_mode before any tensor is built
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_sweep_case_rejects_malformed_fields
        status: pass
    human_judgment: false
  - id: D5
    description: Phase-38 set_default_dtype, is_available, and v1.3-import guarantees are re-homed locally for this module
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_module_has_no_global_default_mutation_or_device_probe
        status: pass
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_module_has_no_v1_3_era_imports
        status: pass
    human_judgment: false

duration: 27min
completed: 2026-09-06
status: complete
---

# Phase 55 Plan 01: Architecture Characterization Probe Core Summary

**Initialization-only probe that reports all seven INST-04 quantities from the trainer's own AD, force, and causal-weight functions, with a six-case Tier-1 invariant net and an SC3 mutation proof**

## Performance

- **Duration:** 27 min
- **Started:** 2026-09-06T02:43:45Z
- **Completed:** 2026-09-06T03:11:03Z
- **Tasks:** 3
- **Files modified:** 3 created

## Accomplishments

- `measure_case` builds a seeded `ArchitectureSpec` network, draws 16 sorted collocation times, and reports median `‖r′‖`, `‖v′‖`, `‖a′‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the causal weight vector, and `front_idx` with no data, optimizer, or training step.
- `run_sweep()` with no arguments measures the six audited rows (`41`, `42`, `43`, `0`, `7`, `41-variable-mass`); every row has `front_idx == 0` and `1e9 < R̄ < 1e11`.
- Every physics quantity is produced by `causal_physics_loss`, `componentwise_du`, and `softened_acceleration`, proven by a mutation test that scales each binding and asserts the reported field moves by the same factor.
- Tier-1 bounds, the Frobenius `R̄ ≈ ‖a′‖²/3` identity, the dtype-derived clamp floor, the strict `w > 0.5` `front_idx` boundary, and the `numpy.median` even-N convention are locked as tests.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end single-case characterization** - `44155884` (feat)
2. **Task 2: Six audited default cases and Tier-1 invariant-bound suite** - `6654b078` (test)
3. **Task 3: SC3 derivation proof and re-homed prohibition assertions** - `09095aa2` (test)

**Plan metadata:** pending this SUMMARY commit

## Files Created/Modified

- `pinn/verification/architecture_characterization_probe.py` - SweepCase, ArchitectureCharacterizationResult, DEFAULT_CASES, measure_case, run_sweep
- `tests/phase55/__init__.py` - phase test package marker
- `tests/phase55/test_architecture_characterization.py` - tracer, Tier-1, boundary, median, SC3 mutation, and re-homed prohibition tests

## Decisions Made

- Followed CONTEXT.md D-01 (Tier-1 invariant bounds in this plan; exact-value fixture is 55-04) and D-02 (`DEFAULT_CASES` is `run_sweep`'s default value, not a second code path).
- Documented even-N median as `numpy.median` (arithmetic mean of the two central order statistics), explicitly not `torch.median`'s lower-of-two, in the module docstring, `MEDIAN_CONVENTION`, and every result's `median_convention` field.
- Clamp floor is always `resolve_causal_clip_facts(dtype, device)['causal_clip_min_weight']`; tests contain no floor literal.

## Deviations from Plan

### Auto-fixed Issues

None.

### Execution notes (non-blocking)

**1. [Rule 3 - Blocking] DEFAULT_CASES landed in the Task 1 commit**
- **Found during:** Task 1
- **Issue:** The plan allowed an empty-tuple placeholder if Task 2 had not run yet, and preferred landing both in one commit if Task 2 ran in the same session.
- **Fix:** Populated the six audited `DEFAULT_CASES` in the Task 1 module commit. Task 2 added the Tier-1 tests and exported `DEFAULT_N_COL`.
- **Files modified:** `pinn/verification/architecture_characterization_probe.py`
- **Verification:** `run_sweep()` returns the six labels with `front_idx == 0` and `1e9 < R̄ < 1e11`
- **Committed in:** `44155884` (Task 1)

**2. [process] Tracer TDD used the plan's SkipTest import guard rather than an assertion-RED commit**
- **Found during:** Task 1
- **Issue:** `_load_probe()` skips while the module is absent, matching `tests/phase38/test_residual_probe.py`. A tests-only commit would skip, which is not GSD assertion-RED.
- **Fix:** Implemented the module in the same Task 1 commit after the skip-guard suite existed; GREEN was 3 passed.
- **Impact:** None on shipped behavior.

---

**Total deviations:** 2 documented (1 same-session DEFAULT_CASES landing, 1 TDD skip-guard analog). No scope creep.
**Impact on plan:** Both notes follow the plan's own same-session preference and the specified skip-guard analog.

## Issues Encountered

- Full-suite `pytest tests/ -q` (661.80s) reported 51 failed / 1611 passed / 3 skipped. None of the failures are in `tests/phase55/` or reference the new probe. The 14 STATE.md-documented phase43/watchdog failures remain. Additional failures are archived-milestone / spec-history tests (`tests/phase38` spec SHA and git-history, `tests/phase47`, `tests/phase49`, `tests/phase50`) uncoupled from this plan's files. Phase 38 glob checks that scan the new module (`set_default_dtype`, `is_available`, argparse precision default, v1.3 tokens) passed.
- `run_sweep()` completed in 0.83s, well under the 30-second feedback budget.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for 55-02: CLI / `--cases-config` / evidence writer, plus the documented `_EXCLUDE_SUFFIXES` entry in `tests/phase38/test_prohibitions.py`.
- Do not add argparse precision defaults until that exclusion lands.
- Do not implement 55-03 4096-bin helpers or 55-04 exact-value fixtures in this module yet.

## Self-Check: PASSED

- FOUND: `pinn/verification/architecture_characterization_probe.py`
- FOUND: `tests/phase55/__init__.py`
- FOUND: `tests/phase55/test_architecture_characterization.py`
- FOUND: commit `44155884` feat(55-01): implement architecture characterization probe core
- FOUND: commit `6654b078` test(55-01): add six-case tier-1 invariant bound suite
- FOUND: commit `09095aa2` test(55-01): prove probe derives from trainer primitives
- FOUND: `.venv/bin/python -m pytest tests/phase55/ -q` — 28 passed

---
*Phase: 55-architecture-characterization-probe*
*Completed: 2026-09-06*
