---
phase: 59-read-only-baseline-scorecard
plan: 01
subsystem: verification
tags: [scorecard, sha256, unittest, feasibility, scope-42]

requires: []
provides:
  - Frozen feasibility scorecard JSON and strict SHA-256 loader
  - Pre-registered tier, counting, decision, budget, polish, G1, and JX-1 rule functions
  - Plain-language scorecard and the phase-start freeze record
affects: [59-02, 59-04, 60-feasibility-rungs, gate-g1]

actuals:
  tokens: 25979
  tasks: 3
  commits: 5

tech-stack:
  added: []
  patterns:
    - "Frozen JSON artifact plus strict loader: canonical bytes, exact keys, value checks, SHA-256 last"
    - "Rule functions take a loaded Scorecard and read constants from it"

key-files:
  created:
    - pinn/verification/artifacts/feasibility_scorecard_v1.json
    - pinn/verification/feasibility_scorecard.py
    - tests/phase59/__init__.py
    - tests/phase59/test_scorecard.py
    - tests/phase59/test_scorecard_rules.py
    - .planning/phases/59-read-only-baseline-scorecard/59-SCORECARD.md
    - .planning/phases/59-read-only-baseline-scorecard/evidence/scorecard-freeze.json
  modified: []

key-decisions:
  - "Task 1 landed as one tracer commit so phase_start_head stays the commit before the first Phase 59 execution commit"
  - "An improvement rate with no finite reference-window reading raises OwnerRouted instead of inventing a number"
  - "FEAS-01 stays pending because plans 59-02, 59-04, and 59-10 also declare it"

patterns-established:
  - "Scorecard sections are read-only mappings; nested lists are tuples"
  - "Unknown or missing keys fail with one sorted dotted path before the hash check"

requirements-completed: [FEAS-01]

coverage:
  - id: D1
    description: "Canonical scorecard JSON, strict loader, and inclusive tier_of boundary rule"
    requirement: FEAS-01
    verification:
      - kind: unit
        ref: "tests/phase59/test_scorecard.py#FrozenFileTests,StrictLoaderTests,GoldenValueTests,TierTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Pre-registered counting, decision, budget, polish, Gate G1, and JX-1 rule functions"
    requirement: FEAS-01
    verification:
      - kind: unit
        ref: "tests/phase59/test_scorecard_rules.py"
        status: pass
      - kind: unit
        ref: "tests/phase59/test_scorecard.py#PublicSurfaceTests.test_exports_every_pre_registered_name"
        status: pass
    human_judgment: false
  - id: D3
    description: "Plain-language scorecard and freeze record pinning the JSON, rule module, document, and decision sources"
    requirement: FEAS-01
    verification:
      - kind: other
        ref: "FREEZE-RECORD-OK and DECISION-SOURCES-PINNED-OK one-liners in 59-01-PLAN.md Task 3"
        status: pass
    human_judgment: false

duration: 16 min
completed: 2026-10-14
status: complete
---

# Phase 59 Plan 01: Read-Only Baseline Scorecard Summary

**Frozen feasibility ruler: canonical scorecard JSON, strict SHA-256 loader, pre-registered rule functions, and a plain-language twin locked before any real-data result**

## Performance

- **Duration:** 16 min
- **Started:** 2026-10-14T01:46:44Z
- **Completed:** 2026-10-14T02:02:24Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- The machine scorecard holds the pre-registered metrics, tiers, counting and decision rules, budget and polish rules, G2 grid 60/120/240/480, cadence, panel rule, census and survey rules, Gate G1, and DIAG-07 tolerances.
- `load_scorecard()` rejects unknown or missing keys, non-canonical bytes, and any SHA-256 other than `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`. `tier_of` is inclusive at every bound.
- The rule functions read those constants from the loaded file. The plain-language document and `evidence/scorecard-freeze.json` pin the JSON, the rule module, and the decision sources. `phase_start_head` is `f3d2f42044ec7d53c8b42dc264866a3a5daab432`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Tracer — scorecard file, strict loader, and tier rule** - `bae63f02` (feat)
2. **Task 2: Pre-registered rule functions** - `04980af4` (test, RED), `0aac08d8` (feat, GREEN)
3. **Task 3: Plain-language scorecard and freeze record** - `4ea3b1bc` (feat)

**Plan metadata:** this commit (docs)

## Files Created/Modified

- `pinn/verification/artifacts/feasibility_scorecard_v1.json` - Canonical frozen scorecard
- `pinn/verification/feasibility_scorecard.py` - Strict loader and pre-registered rules
- `tests/phase59/__init__.py` - Package docstring only
- `tests/phase59/test_scorecard.py` - Frozen-file, loader, golden, tier, and public-surface tests
- `tests/phase59/test_scorecard_rules.py` - Boundary tables for every rule function
- `.planning/phases/59-read-only-baseline-scorecard/59-SCORECARD.md` - Plain-language twin
- `.planning/phases/59-read-only-baseline-scorecard/evidence/scorecard-freeze.json` - SHA-256 freeze record and decision-source pins

## Decisions Made

- Task 1 is a tracer, not `tdd="true"`. Its tests and loader landed in one commit so the JSON-adding commit's parent, recorded as `phase_start_head`, is the commit before Phase 59's first execution commit.
- Nested JSON lists are stored as tuples inside read-only mappings. Callers cannot mutate a loaded scorecard.
- If an arm is still improving only because the reference window has no finite reading, `budget_outcome` raises `OwnerRouted` rather than dividing by a missing reference.
- FEAS-01 is not marked complete in `REQUIREMENTS.md`. Plans 59-02, 59-04, and 59-10 also declare it, and those plans have no summary yet.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Undefined improvement rate is owner-routed**
- **Found during:** Task 2 (rule functions)
- **Issue:** The inconclusive rate divides by the reference-window best `E`. That value does not exist when the only reason `still_improving` is true is a finite final reading and an empty reference window.
- **Fix:** Raise `OwnerRouted` with the message that the rate is not determinable. Do not invent a numeric rate.
- **Files modified:** `pinn/verification/feasibility_scorecard.py`
- **Verification:** The stated still-improving and budget-outcome boundary tests pass. This empty-reference rate path is not a separate asserted case.
- **Committed in:** `0aac08d8` (Task 2 GREEN)

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** The guard stops a divide-by-missing-reference from becoming a silent number. No threshold was added.

## TDD Gate Compliance

Task 2 is `tdd="true"`. RED commit `04980af4` precedes GREEN commit `0aac08d8`. `gsd-tools check tdd-red-evidence` returned `RED_EVIDENCE_OK` (`target_test_failed`) for `test_true_when_tier_counts_and_error_is_strictly_below_formula` at exit 1, assertion `unexpectedly None : counts`. No REFACTOR commit.

Task 1 is a tracer without `tdd="true"`. Its tests and implementation share `bae63f02`. A test-only commit before the JSON would have made `phase_start_head` that test commit instead of `f3d2f42044ec7d53c8b42dc264866a3a5daab432`.

| Plan | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 59-01 task 2 | 04980af4 | 0aac08d8 | — | Pass |
| 59-01 task 1 (tracer, not tdd) | — | bae63f02 | — | Not a TDD task |

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for 59-02. The frozen file, loader, and rule functions are committed. Wave 2 must not edit the JSON, `pinn/verification/feasibility_scorecard.py`, `59-SCORECARD.md`, or `evidence/scorecard-freeze.json`. FEAS-01 remains pending until the scorer plans finish. The `.planning/codebase/` map was left unchanged: the new module follows the existing `pinn/verification/` package and does not add a directory pattern.

## Self-Check: PASSED

- `tests/phase59` discovery: 58 tests, OK.
- Adjacent regression (`tests.phase39.test_prohibitions`, `test_splits`, `test_adapter`, `tests.phase46.test_isolation`, and the two Phase 38 prohibition methods): 177 tests, OK.
- `FREEZE-RECORD-OK` and `DECISION-SOURCES-PINNED-OK` printed before the freeze commit. The freeze commit `4ea3b1bc` names only `59-SCORECARD.md` and `evidence/scorecard-freeze.json`.
- Import roots of `feasibility_scorecard.py` are stdlib only. `r_ref_stage0.json` was not modified.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-14*
