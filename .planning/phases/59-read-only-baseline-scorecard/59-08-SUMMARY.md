---
phase: 59-read-only-baseline-scorecard
plan: 08
subsystem: verification
tags: [feas-07, two-kepler, nearest-neighbour, baselines, counting-rule, comparison-points]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: The frozen scorecard and FEAS-01 scorer, the allowlisted corpus doorway and production reference, the committed census panels, and the audit normalizer fingerprint
provides:
  - The two-Kepler comparison formula (pinn/verification/two_kepler.py), proven against an independent RK4 integrator
  - The nearest-neighbour copy (pinn/verification/nn_copy.py) in production-normalized IC13
  - The baselines runner (pinn/verification/baselines.py) with --panel singles --stdout, the full run and a byte-identical --check, importable by the Phase-60 harness
  - Committed baselines evidence. The formula reaches Tier 1 or better on 1 of 1812 Stage-0 training systems and 0 of 227 validation systems; the copy on 0 of 227
affects: [59-10, 60]

actuals:
  tokens: 0  # not measured: the plan ran interleaved with 59-09 in one session
  tasks: 3
  commits: 6
plan_head_before: 0d57e8f9

tech-stack:
  added: []
  patterns:
    - "A comparison point is scored by the same score_trajectory the networks face, with its own velocity source (analytic for the formula, brutus for the copy)"
    - "The FEAS-01(i) physics-residual columns are attached with dataclasses.replace and never change E or a tier"

key-files:
  created:
    - pinn/verification/two_kepler.py
    - pinn/verification/nn_copy.py
    - pinn/verification/baselines.py
    - tests/phase59/test_two_kepler.py
    - tests/phase59/test_nn_copy.py
    - tests/phase59/test_baselines.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/two_kepler.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/two_kepler_population.csv
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/nn_copy.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/baselines.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/summary.md
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/files_opened.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/provenance.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/baselines/MANIFEST.json
  modified: []

key-decisions:
  - "The formula is propagated from each system's gold t = 0 state. The base-grid columns use the same prediction evaluated at the base times, and a base/gold permutation mismatch halts the run (the census already proved none exists)."
  - "The unbound test is |v|^2 >= 2 mu / r exactly as the plan states it, so the parabolic boundary is not applicable rather than a near-infinite ellipse."
  - "The candidate pool must equal both the allowlist's Stage-0 training base keys and the census training ids, or the run halts."

patterns-established:
  - "An inline evidence step records WALL-SECONDS for the run and for --check, and the SUMMARY quotes both against the 600 s budget"

requirements-completed: []

coverage:
  - id: D1
    description: "Kepler propagator against RK4, identity, unbound, decoupled fixture, conservation, frame and acceleration tests"
    requirement: FEAS-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_two_kepler.py#KeplerVsRK4Tests,IdentityTests,UnboundTests,DecoupledFixtureTests,ConservationTests,FrameTests,KeplerAccelerationTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Nearest neighbour, candidate pool, self-match refusal, copy grid, determinism and the copy residual column"
    requirement: FEAS-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_nn_copy.py#NearestTests,CandidatePoolTests,SelfMatchTests,CopyPredictionTests,DeterminismTests,CopyResidualTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Public surface for Phase 60, the FEAS-09 not-applicable entries, and a decoupled formula row"
    requirement: FEAS-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_baselines.py#PublicSurfaceTests,Feas09Tests,FormulaRowTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Committed baselines evidence, re-derived byte for byte, committed after the freeze"
    requirement: FEAS-07
    verification:
      - kind: integration
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py baselines --skip-rederive --require-committed"
        status: pass
    human_judgment: true
    rationale: "The verifier checks hashes, coverage and commit order. What the comparison points mean for the counting rule and the verdict is read in plan 59-10."

duration: 75min
completed: 2026-10-16
status: complete
---

# Phase 59 Plan 08: The Comparison Points Summary

**No. The two-Kepler formula does not already reach Tier 1 on Stage 0. It reaches Tier 1 or better on 1 of 1812 training systems and 0 of 227 validation systems, with a median E of 0.99 and 0.94. Copying the nearest training system reaches Tier 1 on 0 of 227 validation systems, with a median E of 2.14.**

## In plain language

Before any network is trained, we scored two yardsticks it has to beat, with the same scorer the networks will face. The first is a formula a physics student could write: treat the inner pair and the outer body as two separate textbook orbits. It starts exactly right, but the third body's pull slowly bends the real orbits away from it. On one typical system the inner pair is off by 0.2% at t = 0.1, by 6% at t = 1 and by 43% at t = 10. So on all but one system its error over the 10-unit window is far above the Tier-1 line of 0.1. The second yardstick copies the most similar training system's real orbit. It does worse (median E 2.14), because a nearby starting point still drifts onto a different orbit within the window. So 1,812 systems do not cover Stage 0 densely enough for simple lookup to work. A network therefore counts only if it beats both, and both set a low bar: neither reaches Tier 1 on the validation panel.

## Performance

- **Duration:** about 75 min, interleaved with 59-09 while that plan waited for memory
- **Tasks:** 3 of 3
- **Files created:** 14 (3 modules, 3 test files, 8 evidence files)
- **Runtime gate (W1, inline, budget 600 s):** the full run printed `WALL-SECONDS 64.63` and `--check` printed `WALL-SECONDS 65.86` with `BASELINES-CHECK-OK`. The `--panel singles --stdout` tracer took 0.62 s.
- **Broad test run (retained):** `unittest discover -s tests/phase59 -p 'test_*.py'` at `f101c36e`, 319 tests OK in 139.1 s, exit 0.

## Accomplishments

- **Formula population (gold grid, analytic velocities):**
  - Training: Tier 0 1811, Tier 1 1, Tier 2 0, Tier 3 0, not applicable 0.
  - Validation: 227 at Tier 0.
  - Panels: singles 3, family 16 and validation 227, all at Tier 0.
  - No system was unbound, so none is not applicable.
- **Copy (227 validation systems):** all at Tier 0, median E 2.14.
- **Residual context (median physics_residual_mean over the governed R_ref 1.97e10):** formula 2.8e-10 (training) and 2.6e-10 (validation); copy 1.9e-8. The copy's column is about 70 times the formula's, reflecting the neighbour's mass mismatch. It is labelled context only.
- **FEAS-09 (D-38):** both probes read "not applicable: no hierarchical split". The manifest confirms every one of the 3,886 training hierarchical base records has manifest stage 0 or 1.
- **Normalizer (D-35):** recovered from `stage-0-init.pt`, `stats_sha256` `77526e53...`, equal to the audit's.
- **Reads:** 4,334 training and 454 validation opens; 0 test-split opens, 0 blocked attempts, 0 refusals.
- **Hashes:** `two_kepler.json` `05a347a6...`, `nn_copy.json` `4334fc04...`, `baselines.json` `3d7b7a68...` (full values in the evidence commit body).

## Task Commits

1. **Task 1: two-Kepler formula and the singles tracer**: `87488725` (feat)
2. **Task 2: the copy and the full run**: `794ea751` (test, failing first), `d5c246a8` (feat)
3. **Task 3: public surface and the area check**: `c5c6cd18` (evidence), `b1d02d36` (test)

**Plan metadata:** the docs commit that carries this summary.

## Files Created/Modified

- `pinn/verification/two_kepler.py`: Kepler f-g propagator, two-orbit assembly, analytic accelerations, NotApplicable
- `pinn/verification/nn_copy.py`: nearest neighbour, copy prediction, copy accelerations
- `pinn/verification/baselines.py`: score_formula, score_copy, candidate_pool, feas09_record, with_residual_context, the CLI and --check
- `tests/phase59/test_two_kepler.py`, `test_nn_copy.py`, `test_baselines.py`: 21 tests
- `evidence/baselines/*`: the committed comparison points and their manifest

## Decisions Made

See `key-decisions` above.

## Deviations from Plan

### Auto-fixed issues

**1. [Rule 1 - Bug] The first test system's inner pair was too fast for the plan's finite-difference check.**
- **Found during:** Task 1
- **Issue:** with an inner separation of 0.12, a 1e-4 central difference carries about 3e-6 truncation error, above the plan's 1e-6 bar.
- **Fix:** the test system now uses an inner separation of 0.3. The formula itself was unchanged.
- **Commit:** `87488725`

**2. [Rule 1 - Bug] The unbound boundary test built the escape speed with a square root that does not round-trip.**
- **Found during:** Task 1
- **Fix:** the test uses mu = 2 so the escape speed is exactly 2. The module's check is now `|v|^2 >= 2 mu / r`, exactly as the plan states it.
- **Commit:** `87488725`

### Differences from the plan text (not deviations)

- Task 1 was committed as one feat commit. The tracer has no TDD flag, and its tests and code landed together after the tests ran.
- Task 3's test file was committed after the evidence commit, as its own test commit. It touches no evidence.

**Total deviations:** 2 test-construction fixes. No frozen value, tolerance or scorecard byte changed.

## Issues Encountered

- The 59-09 development runs were waiting for 6 GiB of free memory throughout this plan. The baselines need well under 1 GB and stay outside the launch lock (W2), so this plan was not blocked.

## Authentication Gates

None.

## Known Stubs

None.

## Threat Flags

None. Every read goes through the allowlist and the attestation; the candidate pool is checked against both the allowlist and the census.

## User Setup Required

None.

## Next Phase Readiness

- Both comparison points are committed before any rung (D-17), and `--require-committed` proves they were first committed after the freeze.
- Phase 60 imports `score_formula`, `score_copy` and `with_residual_context`. The formula does not apply to the two FEAS-09 probe systems.
- FEAS-07 stays pending in `REQUIREMENTS.md` until Plan 59-10's final check.

## Self-Check: PASSED

Every file and commit named here exists. After the evidence commit, `verify_phase59_evidence.py baselines --skip-rederive --require-committed` printed BASELINES-OK. Before it, `manifest --area baselines --write` printed MANIFEST-BASELINES-OK, `baselines --skip-rederive` printed BASELINES-OK, and `scorecard-frozen` printed SCORECARD-FROZEN-OK. The 319-test Phase 59 suite passes.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-16*
