---
phase: 59-read-only-baseline-scorecard
plan: 04
subsystem: verification
tags: [evidence, sha256, scorecard-freeze, guardrails, gate-g1, feas-01]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Frozen scorecard, SCORECARD_SHA256, and the four decision-source pins
provides:
  - Shared evidence writer with canonical JSON, redaction, the freeze guard, the launch lock, and the 600 s runtime gate
  - Independent verifier for commit order, area manifests, Gate G1, guardrails, and the final findings contract
  - Evidence README that later Phase 59 plans follow
affects: [59-05, 59-06, 59-07, 59-08, 59-09, 59-10]

actuals:
  tokens: 37233
  tasks: 3
  commits: 7
plan_head_before: ffc8c3925f7b96a14e243413de688e27d0caf273

tech-stack:
  added: []
  patterns:
    - "Phase 59 evidence is canonical JSON with non-finite floats as string sentinels"
    - "The verifier never imports evidence_io; re-derivation is a --check subprocess"
    - "Survey and diag07 results are accepted only with a matching completion marker"

key-files:
  created:
    - pinn/verification/evidence_io.py
    - tests/phase59/test_evidence_io.py
    - tests/phase59/test_evidence_verifier.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/README.md
  modified: []

key-decisions:
  - "The corpus guard refuses data_root's parent only when that directory is named simulation_data"
  - "README re-derivation commands name python -B -m, not an absolute interpreter path, so tracked evidence contains no home directory"
  - "FEAS-01, FEAS-02, FEAS-07, FEAS-08, and DIAG-07 stay pending because later plans also declare them"

patterns-established:
  - "One long step at a time through evidence/logs/launch.lock.log; stale recovery refuses a live foreign pid"
  - "Area manifests record freeze_commit and produced_at_head; --require-committed checks both"

requirements-completed: [FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07]

coverage:
  - id: D1
    description: "Canonical evidence writer refuses home and corpus paths, pins the freeze, and enforces one launch lock plus the 600 s runtime gate"
    requirement: FEAS-01
    verification:
      - kind: unit
        ref: "tests/phase59/test_evidence_io.py#CanonicalJsonTests,RedactionTests,RootGuardTests,AtomicWriteTests,ManifestTests,CommandRedactionTests,FreezeGuardTests,ModuleHashTests,MemoryPreflightTests,CompletionMarkerTests,LaunchLockTests,RuntimeGateTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "scorecard-frozen prints SCORECARD-FROZEN-OK on the real worktree only when the four frozen files and the decision-source pins still match"
    requirement: FEAS-01
    verification:
      - kind: unit
        ref: "tests/phase59/test_evidence_verifier.py#ScorecardFrozenTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py scorecard-frozen"
        status: pass
    human_judgment: false
  - id: D3
    description: "Area manifests, producer hashes, completion markers, and an independent Gate G1 recomputation"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_evidence_verifier.py#ManifestTests,AreaContractTests,RederiveTests,AuditTests,Diag07Tests,FreezeInAreaTests,RequireCommittedTests,ProducerHashTests,CompletionMarkerTests"
        status: pass
      - kind: other
        ref: "ast import scan prints VERIFIER-INDEPENDENT"
        status: pass
    human_judgment: false
  - id: D4
    description: "Guardrails re-hash the generation-7 seed42 and smoke run files and refuse a home path in tracked evidence"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_evidence_verifier.py#GuardrailTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py guardrails"
        status: pass
    human_judgment: false
  - id: D5
    description: "final checks a complete evidence tree and the README lists every subcommand and OK token"
    requirement: FEAS-02
    verification:
      - kind: unit
        ref: "tests/phase59/test_evidence_verifier.py#FinalTests"
        status: pass
      - kind: unit
        ref: "unittest discover -s tests/phase59 -p test_*.py (152 tests)"
        status: pass
    human_judgment: false

duration: 37 min
completed: 2026-10-14
status: complete
---

# Phase 59 Plan 04: Evidence Writer and Verifier Summary

**Shared evidence writer and an independent verifier that proves the scorecard was frozen before any result, including Gate G1 recomputed from the frozen rule**

## Performance

- **Duration:** 37 min
- **Started:** 2026-10-14T03:07:24Z
- **Completed:** 2026-10-14T03:44:29Z
- **Tasks:** 3
- **Files modified:** 5

## Accomplishments

- Evidence writes are canonical JSON, atomic, and refused when they contain the home directory, the data root, or a path under `simulation_data`.
- `scorecard-frozen` passes on this worktree: the four frozen files and the decision-source pins still match commit `4ea3b1bc`.
- Area checks, `--require-committed`, producer hashes, completion markers, and an independent `g1_fires` recomputation are in the verifier. The verifier does not import `evidence_io`.
- Guardrails re-hashed the generation-7 seed42 and smoke runs and printed `GUARDRAILS-OK`. The evidence README is the contract for plans 59-05 through 59-10.

## Task Commits

Each task was committed atomically:

1. **Task 1: Evidence writer and SCOPE-42 freeze check** - `437569c9` (test), `1b27531f` (feat)
2. **Task 2: Area manifests, area contracts, and Gate G1** - `4c331bf2` (test), `37664b3b` (feat)
3. **Task 3: Guardrails, final, and the evidence README** - `90739625` (test), `fc418004` (feat)

**Plan metadata:** recorded in the following docs commit.

## Files Created/Modified

- `pinn/verification/evidence_io.py` - Shared writer, freeze guard, launch lock, runtime gate
- `tests/phase59/test_evidence_io.py` - Writer, redaction, freeze, lock, and runtime tests
- `tests/phase59/test_evidence_verifier.py` - Commit-order, area, G1, guardrail, and final tests on temporary repositories
- `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` - Independent verifier
- `.planning/phases/59-read-only-baseline-scorecard/evidence/README.md` - JSON contracts and checker commands

## Decisions Made

- Refusing the grandparent of `data_root` would refuse the worktree itself, because this worktree lives inside the main checkout. The guard refuses `simulation_data` and the data root, and the main checkout's `simulation_data` only when `data_root`'s parent has that name.
- The README names `python -B -m ...` rather than the absolute pinn-train path. That path contains the home directory, which guardrails rejects in tracked evidence.
- FEAS-01, FEAS-02, FEAS-07, FEAS-08, and DIAG-07 stay pending in `REQUIREMENTS.md`. Later plans still declare them.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Freeze-in-area test passed a path to write_bytes**
- **Found during:** Task 2 (area checks)
- **Issue:** Restoring the rule module called `write_bytes` with a `Path`. That method requires bytes, so the test errored before the freeze assertion.
- **Fix:** Read the real module bytes and write those.
- **Files modified:** `tests/phase59/test_evidence_verifier.py`
- **Verification:** `FreezeInAreaTests` passes.
- **Committed in:** `37664b3b`

**2. [Rule 1 - Bug] Final test called a diag07 helper that is not on the shared fixture**
- **Found during:** Task 3 (final check)
- **Issue:** `FinalTests` called `self._jx`, which is defined on `Diag07Tests`.
- **Fix:** Call `Diag07Tests._jx(self, ...)`.
- **Files modified:** `tests/phase59/test_evidence_verifier.py`
- **Verification:** `FinalTests` passes.
- **Committed in:** `fc418004`

---

**Total deviations:** 2 auto-fixed (2 bugs)
**Impact on plan:** No new threshold, hash, or scoring rule. The frozen scorecard bytes were not edited.

## TDD Gate Compliance

`gsd-tools check tdd-red-evidence` returned `RED_EVIDENCE_OK` (`target_test_failed`) for each RED commit. No REFACTOR commit.

| Plan | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 59-04 task 1 (tracer; RED still committed first) | 437569c9 | 1b27531f | — | Pass |
| 59-04 task 2 | 4c331bf2 | 37664b3b | — | Pass |
| 59-04 task 3 | 90739625 | fc418004 | — | Pass |

Task 1's targeted assertion was `unexpectedly None` on `test_canonical_json_uses_sorted_keys_and_sentinels` (27 tests failed, none errored). Task 2's target was `test_manifest_round_trip_names_changed_missing_and_extra_files` (`manifest` absent from the command table). Task 3's target was `test_real_worktree_guardrails_ok` (`guardrails` absent).

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for 59-05. Producers should write through `evidence_io`, call `require_frozen_scorecard` before any corpus or checkpoint read, and follow `evidence/README.md`. Do not edit the frozen scorecard, `SCORECARD_SHA256`, or the scorer's scoring rules. `final` is not expected to pass until the later plans have written their areas and `59-FINDINGS.md`. `.planning/codebase/` was left unchanged: the new module sits in the existing `pinn/verification/` package.

## Self-Check: PASSED

- `unittest tests.phase59.test_evidence_io tests.phase59.test_evidence_verifier`: 36 tests, OK, after the area checks.
- Real `scorecard-frozen`: `SCORECARD-FROZEN-OK`.
- `unittest tests.phase39.test_prohibitions` plus the two Phase 38 prohibition methods: 33 tests, OK.
- `ast` import scan of the verifier: `VERIFIER-INDEPENDENT`.
- `unittest discover -s tests/phase59 -p 'test_*.py'`: 152 tests, OK.
- Real `guardrails`: `GUARDRAILS-OK`.
- `ls evidence/__pycache__ | wc -l`: 0.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-14*
