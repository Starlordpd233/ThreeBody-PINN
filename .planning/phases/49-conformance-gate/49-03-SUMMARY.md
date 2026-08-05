---
phase: 49-conformance-gate
plan: 03
subsystem: training-checkpoint-resume
tags: [pytorch, checkpoints, resume, invariant-b, schema-versioning]

requires:
  - phase: 49-conformance-gate
    provides: StepGuards invariant-B state accessors and runtime invariant checks from plan 49-02
provides:
  - Schema-v2 checkpoint payloads carrying invariant-B high-water and advance-step state
  - Fail-closed resume restoration with required-key, explicit-None, and malformed-state handling
  - Boundary-exact regression proof that a stall continues across resume
affects: [phase-49-conformance-gate, future-training-resume, GATE-03]

actuals:
  tokens: 3687
  tasks: 2
  commits: 4

tech-stack:
  added: []
  patterns:
    - Symbolic checkpoint schema versioning with additive payload fields
    - Keyword-only provider injection for controller-owned checkpoint composition
    - Restore-boundary validation that distinguishes missing state from explicit None

key-files:
  created:
    - tests/phase49/test_gate03_resume.py
  modified:
    - pinn/training/checkpoint.py
    - pinn/training/controllers.py
    - pinn/train.py

key-decisions:
  - "Use the D-17 preferred schema-bump route: persist invariant-B state instead of silently re-arming on resume."
  - "Keep invariant_b_state out of _CTX53_REQUIRED_KEYS for Phase 41 compatibility; enforce its required presence at the v2 train restore boundary."
  - "Permit explicit None only for no-provider constructions; production train payloads pass the live StepGuards provider."

patterns-established:
  - "All production checkpoint payload sites read state from step_guards.invariant_b_state_dict()."
  - "CurriculumController checkpoint anchors use an optional callable provider, preserving existing constructor call sites."

requirements-completed: [GATE-03]

coverage:
  - id: D1
    description: "Schema-v2 checkpoint payloads persist invariant-B state and dynamic schema versioning."
    requirement: GATE-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate03_resume.py -k payload or schema"
        status: pass
    human_judgment: false
  - id: D2
    description: "Invariant-B state restores across a checkpoint and trips at the continued-window boundary."
    requirement: GATE-03
    verification:
      - kind: integration
        ref: "tests/phase49/test_gate03_resume.py::test_restore_preserves_stall_window_across_resume_boundary"
        status: pass
    human_judgment: false
  - id: D3
    description: "Schema-v1, missing-key, malformed-state, and explicit-None resume outcomes are covered."
    requirement: GATE-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate03_resume.py"
        status: pass
    human_judgment: false

duration: 20min
completed: 2026-08-05
status: complete
---

# Phase 49 Plan 03: Resume-Safe Invariant-B Checkpoints Summary

**Schema-v2 checkpoints now carry invariant-B state, and resume refuses any payload that could silently re-arm the stall window.**

## Performance

- **Duration:** 20 min
- **Started:** 2026-08-05T05:48:00Z (approximate)
- **Completed:** 2026-08-05T06:09:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Bumped the single `CHECKPOINT_SCHEMA_VERSION` source of truth from 1 to 2 and added an additive `invariant_b_state` payload key without changing the Phase 41 required-key contract.
- Threaded live `StepGuards.invariant_b_state_dict` through every production checkpoint path and the `CurriculumController` anchor provider seam.
- Added restore-boundary enforcement: missing state refuses loudly, malformed state delegates to fail-closed `StepGuards` validation, and explicit `None` preserves initialized state.
- Proved the persisted high-water window trips one step after the non-trip boundary across resume, while stale schema-v1 payloads fail structural validation.

## Task Commits

Each TDD task was committed atomically (RED test, then GREEN implementation):

1. **Task 1 RED: Schema/payload tests** — `7e83fac7`
2. **Task 1 GREEN: Schema bump and payload threading** — `5dd9c8b9`
3. **Task 2 RED: Resume continuity/refusal tests** — `fa68d3fd`
4. **Task 2 GREEN: Restore boundary** — `6f20bdde`

## Files Created/Modified

- `pinn/training/checkpoint.py` - Schema version 2 single source of truth.
- `pinn/training/controllers.py` - Additive payload field and optional invariant-B provider for curriculum anchors.
- `pinn/train.py` - Live state provider wiring and fail-closed resume restoration.
- `tests/phase49/test_gate03_resume.py` - Payload, round-trip, boundary, stale-schema, missing-key, malformed-state, and explicit-None tests.

## Decisions Made

- Followed the research verdict's D-17 preferred route and did not use re-arm-and-record fallback.
- Enforced the v2 required key at the restore boundary rather than expanding `_CTX53_REQUIRED_KEYS`, preserving all Phase 41 hand-built payloads byte-for-byte.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Test bug] Added the local StepGuards fixture required by the new resume tests.**
- **Found during:** Task 2 (resume continuity/refusal tests)
- **Issue:** Initial tests referenced an undefined `_make_guards` helper.
- **Fix:** Added a dataset-free local fixture with the existing Phase 41 guard configuration shape.
- **Files modified:** `tests/phase49/test_gate03_resume.py`
- **Verification:** Full focused checkpoint/resume/invariant selection passed (132 tests).
- **Committed in:** `6f20bdde`

**Total deviations:** 1 auto-fixed test issue.
**Impact on plan:** No production scope expansion; the fixture only supports the declared tests.

## Issues Encountered

- The requested `tests/phase41/test_train_entrypoint.py` regression suite currently has 16 pre-existing failures at Wave 2's PHYS-05 preflight (`lambda_e_max expected 0.0, actual 1.0`) in legacy Phase 41 configs. The failures occur before checkpoint/resume logic; no Phase 41 files or unrelated configuration were changed.
- Direct regression checks remain green: `test_resume.py` (30), `test_gate03_invariants.py` (22), `test_checkpoint.py` + `test_controllers_ext.py` (70), and `test_gate03_resume.py` (10). The Phase 41 diff gate is empty.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

GATE-03 checkpoint continuity is ready for phase-level verification. The Phase 41 train-entrypoint preflight mismatch should be tracked by the phase orchestrator as an existing Wave 2 regression, not attributed to this plan.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/49-conformance-gate/49-03-SUMMARY.md`.
- Task commits `7e83fac7`, `5dd9c8b9`, `fa68d3fd`, and `6f20bdde` are present in git history.
- Summary content passes `git diff --check`.

---
*Phase: 49-conformance-gate*
*Completed: 2026-08-05*
