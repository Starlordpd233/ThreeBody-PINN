---
phase: 43-verification-stage-0-pilot-acceptance
plan: 09
subsystem: verification-authorization
tags: [acc-01, duration-gate, strict-cpu, marker-schema, tdd, fail-closed]
status: complete
requires:
  - phase: 43-01
    provides: "ordered verify ladder, marker writer, and freshness authorization predicate"
  - phase: 43-03
    provides: "persisted Stage-0 timing calibration and duration forecast"
  - phase: 43-04
    provides: "fresh-launch duration gate wired before run-directory construction"
provides:
  - "Strict-CPU-aware effective runtime identity shared by smoke calibration, duration forecast, and verify-marker authorization"
  - "Fail-closed verify-marker authorization requiring the current schema, exact ordered ladder, strict booleans, and complete fingerprint keys"
affects: [phase-43-verification, long-run-authorization, stage0-timing-calibration]
tech-stack:
  added: []
  patterns:
    - "Authorization artifacts fingerprint the runtime that training executes, not merely the requested config"
    - "Marker writers may retain broad result rendering while authorization readers enforce the complete schema"
key-files:
  created: []
  modified:
    - pinn/train.py
    - pinn/verify.py
    - tests/phase43/test_verify_gate.py
    - tests/phase43/test_verify_ladder.py
key-decisions: []
patterns-established:
  - "Pure effective-runtime labels preserve strict-determinism reseeding at the existing runtime-resolution call site"
  - "Marker schema checks validate expected keys as a subset, preserving forward-compatible extra fingerprint fields"
requirements-completed: [ACC-01]
coverage:
  - id: D1
    description: "Strict CPU determinism authorizes and persists timing under float64/cpu even when the config requests float32/mps."
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_strict_cpu_gate_uses_effective_float64_cpu_fingerprint"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_strict_cpu_smoke_calibration_uses_effective_runtime_labels"
        status: pass
    human_judgment: false
  - id: D2
    description: "Only a current-schema marker with the exact ordered ladder, strict boolean passes, and complete fingerprint identity can authorize a long run."
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerFreshnessTests"
        status: pass
      - kind: other
        ref: "forged_marker_accepted probe"
        status: pass
    human_judgment: false
duration: 7min
completed: 2026-07-22
---

# Phase 43 Plan 09: Long-Run Authorization Hardening Summary

**The long-run gate now binds calibration and verification authority to the effective strict-CPU runtime, and only a complete current-schema ordered marker can grant authorization.**

## Performance

- **Duration:** 7 min
- **Started:** 2026-07-23T01:36:45Z
- **Completed:** 2026-07-23T01:43:10Z
- **Tasks:** 2
- **Files modified:** 4 task artifacts

## Accomplishments

- Added `_effective_runtime_labels(config)` and used it for both smoke timing writes and duration-gate fingerprints, closing the requested-MPS versus effective-CPU authorization mismatch without moving or duplicating the strict-determinism reseed.
- Hardened `marker_is_green_and_fresh` to require `MARKER_SCHEMA_VERSION`, the exact ordered `LADDER`, strict `True` booleans, and all six runtime/code fingerprint keys before granting authority.
- Added TDD regressions for strict-CPU calibration/authorization plus forged, duplicate, reordered, missing, extra, stale-schema, truthy-non-bool, and incomplete-fingerprint markers while retaining a writer-produced positive control.

## Task Commits

Each TDD gate was committed atomically:

1. **Task 1 RED: effective-runtime authorization regressions** — `15602bb7` (test)
2. **Task 1 GREEN: strict-CPU-aware timing and gate identity** — `3c55d1e0` (fix)
3. **Task 2 RED: complete marker-schema regressions** — `4e522164` (test)
4. **Task 2 GREEN: fail-closed marker authorization schema** — `305184f8` (fix)

**Plan metadata:** this closeout commit (`docs(43-09): complete authorization hardening plan`).

## TDD Evidence

- **Task 1 RED:** `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verify_gate -v` ran 18 tests and failed as expected with 1 error (strict-CPU gate searched for `float32/mps`) plus 1 failure (smoke wrote `float32/mps`).
- **Task 1 GREEN:** the same command ran 18 tests, all passing.
- **Task 2 RED:** `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verify_ladder -v` ran 49 tests and failed as expected on the five reproduced acceptance bypasses.
- **Task 2 GREEN:** the same command ran 49 tests, all passing.

## Files Created/Modified

- `pinn/train.py` — pure effective-runtime label helper plus strict-CPU-aware calibration and gate fingerprinting.
- `pinn/verify.py` — complete marker ladder, schema-version, and fingerprint-shape authorization validation.
- `tests/phase43/test_verify_gate.py` — strict-CPU effective fingerprint and smoke-calibration regressions.
- `tests/phase43/test_verify_ladder.py` — malformed-marker refusal matrix and writer-produced green-marker positive control.

## Decisions Made

None - followed the plan's grounded authorization contracts. The strict-determinism reseed remains only in `_resolve_runtime_spec`, and `ladder_is_green` remains available for writer verdict rendering while the read/authorize path performs the stronger validation.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The RED failures were expected TDD evidence and flipped to GREEN without changing scope.

## Verification

- `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verify_gate tests.phase43.test_verify_ladder -v` — **67/67 pass**.
- Independent forged-marker probe — **PASS**, printed `forged_marker_accepted=False` for five duplicate `not_a_rung` records.
- Effective-runtime probe — **PASS**, `_effective_runtime_labels` returned `float64/cpu` and matched `RuntimeSpec.precision/requested_device`, `torch.float64`, and CPU.
- Malformed-rung adversarial probe — **PASS**, string, non-mapping, and truthy-non-bool rung containers all refused without exceptions.
- `git diff --check d2223515..305184f8 -- pinn/train.py pinn/verify.py tests/phase43/test_verify_gate.py tests/phase43/test_verify_ladder.py` — **PASS**.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- CR-03 and CR-04 are closed with TDD evidence; Plan 43-10 can address the next independent review finding.
- `ACC-01` was already marked Complete in `.planning/REQUIREMENTS.md`; no requirements mutation was needed.
- Per the worktree single-writer contract, this executor did not modify the already-dirty `.planning/STATE.md` or `.planning/ROADMAP.md`; the execute-phase orchestrator owns their post-plan synchronization.

## Known Stubs

None. The only newly added empty container is a test-local capture map populated during the assertion path; it is not a production or UI placeholder.

## Self-Check: PASSED

- `43-09-SUMMARY.md` and all four modified task artifacts exist on disk.
- Commits `15602bb7`, `3c55d1e0`, `4e522164`, and `305184f8` exist in Git history and each contains only its declared owned file.
- The exact plan-level verification command passed 67/67 tests, including the exactly-1800-second boundary and no-calibration refusal regressions.
- The cumulative task diff contains only `pinn/train.py`, `pinn/verify.py`, `tests/phase43/test_verify_gate.py`, and `tests/phase43/test_verify_ladder.py`.
- No held-out evaluator command, evaluation evidence mutation, network endpoint, auth path, package install, or schema mutation occurred.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-22*
