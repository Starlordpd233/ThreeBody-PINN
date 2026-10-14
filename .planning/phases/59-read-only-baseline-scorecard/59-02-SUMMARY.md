---
phase: 59-read-only-baseline-scorecard
plan: 02
subsystem: verification
tags: [feasibility-scorer, autograd, eps-h, unittest, feas-01]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Frozen scorecard, load_scorecard, and tier_of
provides:
  - FEAS-01 scorer with position errors, horizons, gate eps_H, and scorecard tiers
  - Closed-form known-error fixtures and D-10 tests
  - Network autograd velocity path and labelled context columns
affects: [59-03, 59-08, 59-09, 60-feasibility-rungs]

actuals:
  tokens: 13257
  tasks: 3
  commits: 6

tech-stack:
  added: []
  patterns:
    - "Tier-defining eps_H calls matched_plummer_hamiltonian_series and trajectory_eps_h with an explicit velocity"
    - "Network positions use the trainer closure; dr'/du is vmap(jacrev), never a summed VJP"
    - "Finite-difference eps_H and the R_ref physics residual are context fields and are not arguments of tier_of"

key-files:
  created:
    - pinn/verification/feasibility_scorer.py
    - tests/phase59/_fixtures.py
    - tests/phase59/test_scorer_known_errors.py
    - tests/phase59/test_scorer_network.py
  modified: []

key-decisions:
  - "finite_difference_context is refused by score_trajectory; fd_context_eps_h is the only finite-difference eps_H"
  - "A constant 5% scale of the rigid orbit leaves eps_H at roundoff, so the frame test applies that same 1.05 factor on the later half of the native times"
  - "The central-difference check is the vector relative error at step 1e-6 and tolerance 1e-6"
  - "FEAS-01 stays pending because plans 59-04 and 59-10 also declare it"

patterns-established:
  - "ScoreResult.h is a tuple of (delta, value) in scorecard order, exposed by h_by_delta"
  - "Non-finite metric floats serialize with json_safe_float sentinels"
  - "network_trajectory saves model.training, calls eval, and restores the prior mode in finally"

requirements-completed: [FEAS-01]

coverage:
  - id: D1
    description: "Reference scored against itself through the frozen scorecard, including Tier 3 on the Lagrange orbit"
    requirement: FEAS-01
    verification:
      - kind: unit
        ref: "tests/phase59/test_scorer_known_errors.py#SelfTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "D-10 known-error cases: offset, time shift, vis-viva velocity scaling, inner-pair phase, and frame invariance"
    requirement: FEAS-01
    verification:
      - kind: unit
        ref: "tests/phase59/test_scorer_known_errors.py#OffsetTests,TimeShiftTests,VelocityScalingTests,VacuityGuardTests,InnerPairPhaseTests,FrameInvarianceTests,NonFiniteAndInputTests,DeterminismTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Network autograd velocities, non-interference, context columns, and the finite-difference velocity-source ban"
    requirement: FEAS-01
    verification:
      - kind: unit
        ref: "tests/phase59/test_scorer_network.py#AutogradVelocityTests,NonInterferenceTests,ChunkingTests,ScoreNetworkTests,FiniteDifferenceContextTests,ResidualContextTests,ScorerVelocitySourceTests,PublicSurfaceTests"
        status: pass
    human_judgment: false

duration: 24 min
completed: 2026-10-14
status: complete
---

# Phase 59 Plan 02: Feasibility Scorer Summary

**FEAS-01 scorer with gate eps_H, scorecard tiers, known-error orbits, and autograd network velocities**

## Performance

- **Duration:** 24 min
- **Started:** 2026-10-14T02:09:28Z
- **Completed:** 2026-10-14T02:33:47Z
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments

- A reference scored against itself returns zero position error, both horizons at 1, and the gate's own eps_H. The exact Lagrange orbit is Tier 3 through the frozen scorecard.
- Offset, time shift, vis-viva velocity scaling, and an inner-pair phase error match the imposed formulas. Fixtures do not import `pinn.verification`.
- Networks are scored with autograd `dr'/du` from the trainer's closure. Parameters and `.grad` stay untouched. Finite-difference eps_H and the R_ref physics residual are context only.

## Task Commits

Each task was committed atomically:

1. **Task 1: Tracer — a reference scored against itself through the frozen scorecard** - `2582b51e` (feat)
2. **Task 2: The D-10 known-error tests** - `c566ab14` (test, RED), `d11ee1ba` (feat, GREEN)
3. **Task 3: The network autograd path and labelled context columns** - `77de0396` (test, RED), `b081b0e5` (feat, GREEN)

**Plan metadata:** this commit (docs)

## Files Created/Modified

- `pinn/verification/feasibility_scorer.py` - Position errors, horizons, gate eps_H, tiers, network autograd path, and context columns
- `tests/phase59/_fixtures.py` - Lagrange rotation, hierarchical circular orbit, eccentric homographic solution, and inner-pair rotation
- `tests/phase59/test_scorer_known_errors.py` - Self-score and D-10 known-error tests
- `tests/phase59/test_scorer_network.py` - Autograd, non-interference, residual context, and the velocity-source AST guard

## Decisions Made

- `score_trajectory` accepts only `autograd`, `analytic`, and `brutus`. `fd_context_eps_h` is the labelled finite-difference column.
- The physics residual is stored on `ScoreResult` and is not passed to `tier_of`.
- FEAS-01 is not marked complete in `REQUIREMENTS.md`. Plans 59-04 and 59-10 still declare it.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Frame test uses a time-split 5% radial scale**
- **Found during:** Task 2 (known-error tests)
- **Issue:** A constant 5% scale of the rigid Lagrange orbit leaves both eps_H values at roundoff (~1e-16). Their relative difference is then O(1), so the stated relative 1e-9 check cannot pass for a correct scorer and cannot catch a crossed frame (Pitfall 11).
- **Fix:** Apply the same 1.05 radial factor in both frames on the later half of the native times. E still agrees to absolute 1e-12. eps_H is about 0.095 and agrees to relative ~1e-15. A crossed velocity frame fails that check. No tolerance number was changed.
- **Files modified:** `tests/phase59/test_scorer_known_errors.py`
- **Verification:** `FrameInvarianceTests` passes; a crossed-frame probe relative error is about 0.78.
- **Committed in:** `c566ab14` (Task 2 RED)

**2. [Rule 1 - Bug] Central-difference agreement is the vector relative error**
- **Found during:** Task 3 (network path)
- **Issue:** At step 1e-6, per-component relative error reaches 1.4e-4 on small velocity entries because of truncation. The vectors themselves agree: `||dv|| / ||v||` is 2.3e-7.
- **Fix:** The test keeps step 1e-6 and tolerance 1e-6, applied to the vector norm. Componentwise agreement with `componentwise_du` stays absolute 1e-12.
- **Files modified:** `tests/phase59/test_scorer_network.py`
- **Verification:** `AutogradVelocityTests` passes.
- **Committed in:** `b081b0e5` (Task 3 GREEN)

**3. [Rule 1 - Bug] Residual identity allows four float64 ulps**
- **Found during:** Task 3 (network path)
- **Issue:** `|d|^2 / 3 / R_ref` from `torch.dot` and from the body-averaged reduction differ by one unit in the last place (`...896e-13` versus `...898e-13`).
- **Fix:** The test bounds that difference by four float64 epsilons. It does not add a physics tolerance.
- **Files modified:** `tests/phase59/test_scorer_network.py`
- **Verification:** `ResidualContextTests` passes.
- **Committed in:** `b081b0e5` (Task 3 GREEN)

**4. [Rule 2 - Missing Critical] Docstring records the single R_ref read**
- **Found during:** Task 3 (network path)
- **Issue:** Task 1's docstring said the module opens no file. `load_governed_r_ref` reads `r_ref_stage0.json`.
- **Fix:** The docstring says the only read is that artifact through `load_frozen_r_ref_artifact`. The module still writes nothing.
- **Files modified:** `pinn/verification/feasibility_scorer.py`
- **Verification:** `load_governed_r_ref()` equals `load_frozen_r_ref_artifact` on the governed path.
- **Committed in:** `b081b0e5` (Task 3 GREEN)

---

**Total deviations:** 4 auto-fixed (2 bug, 1 blocking, 1 missing critical)
**Impact on plan:** The numeric checks stay the plan's 1e-12 and 1e-9 / 1e-6 figures. The two test-shape changes keep those checks from being vacuous or from failing on float rounding. No scorecard byte changed.

## TDD Gate Compliance

Task 1 is a tracer, not `tdd="true"`. Tests and scorer landed together in `2582b51e`.

Task 2 is `tdd="true"`. RED commit `c566ab14` precedes GREEN commit `d11ee1ba`. `gsd-tools check tdd-red-evidence` returned `RED_EVIDENCE_OK` (`target_test_failed`) for `test_scaled_velocities_match_vis_viva` at exit 1, assertion `unexpectedly None : eccentric_homographic`. The scorer formulas from Task 1 already matched the known errors, so GREEN added only the fixtures. No REFACTOR commit.

Task 3 is `tdd="true"`. RED commit `77de0396` precedes GREEN commit `b081b0e5`. The same check returned `RED_EVIDENCE_OK` for `test_matches_componentwise_du_and_central_difference` at exit 1, assertion `unexpectedly None : network_trajectory`. No REFACTOR commit.

| Plan | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 59-02 task 1 (tracer, not tdd) | — | 2582b51e | — | Not a TDD task |
| 59-02 task 2 | c566ab14 | d11ee1ba | — | Pass |
| 59-02 task 3 | 77de0396 | b081b0e5 | — | Pass |

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for 59-03. The scorer is importable through the exported names. Wave 2 still has the corpus choke point and the evidence writer. Do not edit the frozen scorecard, `SCORECARD_SHA256`, or `feasibility_scorecard.py`. FEAS-01 remains pending until 59-04 and 59-10 finish. `.planning/codebase/` was left unchanged: the new module is another file in `pinn/verification/`.

## Self-Check: PASSED

- `conda run -n pinn-train python -B -m unittest tests.phase59.test_scorer_known_errors -v`: 11 tests, OK. Classes SelfTests, OffsetTests, TimeShiftTests, VelocityScalingTests, VacuityGuardTests, InnerPairPhaseTests, FrameInvarianceTests, NonFiniteAndInputTests, and DeterminismTests passed.
- `python -B -c` fixture import scan printed `FIXTURES-INDEPENDENT`.
- `sorted(VELOCITY_SOURCES)` printed `['analytic', 'autograd', 'brutus', 'finite_difference_context']`.
- `conda run -n pinn-train python -B -m unittest tests.phase59.test_scorer_network tests.phase59.test_scorer_known_errors -v`: 20 tests, OK. All eight network classes passed, including the injected-violation self-test.
- Adjacent regression (Phase 39 prohibitions, splits, adapter, Phase 46 isolation, and the two Phase 38 scans): 177 tests, OK.
- `unittest discover -s tests/phase59 -p 'test_*.py'`: 78 tests, OK.
- Scorecard bytes were not in the diff. `git status` shows no edits outside this plan's files and the pre-existing dirty paths.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-14*
