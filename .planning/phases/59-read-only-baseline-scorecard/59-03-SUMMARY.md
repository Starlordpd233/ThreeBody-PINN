---
phase: 59-read-only-baseline-scorecard
plan: 03
subsystem: verification
tags: [split-allowlist, audit-hook, normalizer-recovery, static-guards, feas-02, diag-07]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Frozen scorecard and the FEAS-01 scorer, without opening the corpus
provides:
  - Hash-checked train/validation allowlist that refuses a test key before any path exists
  - Production reference trajectories, inner-pair slots, and checkpoint normalizer recovery
  - Glob-discovered static guards over Phase 59 modules, evidence scripts, and tests
affects: [59-04, 59-05, 59-06, 59-07, 59-08, 59-09]

actuals:
  tokens: 22007
  tasks: 3
  commits: 6
plan_head_before: beb02244c35b69850072d9aeae995ba34199d13d

tech-stack:
  added: []
  patterns:
    - "Phase 59 corpus reads go through SplitAllowlist.require before any path is built"
    - "Resident records replay the adapter per-file seams and the float32 cast, never the admitted-set adapter"
    - "Static scans are globbed at run time and each detector is proven on an injected violation"

key-files:
  created:
    - pinn/verification/split_allowlist.py
    - pinn/verification/production_reference.py
    - tests/phase59/_corpus_fixtures.py
    - tests/phase59/test_split_allowlist.py
    - tests/phase59/test_production_reference.py
    - tests/phase59/test_static_guards.py
  modified:
    - tests/phase39/test_prohibitions.py

key-decisions:
  - "Checkpoint record keys are the three-element list from controllers._record_key_payload, not a dict"
  - "ReferenceTrajectory keeps dt_out provenance so the resident record matches the trainer field"
  - "FEAS-02, FEAS-07, FEAS-08, and DIAG-07 stay pending because later plans also declare them"

patterns-established:
  - "Open attestation is a process-global audit hook and is exercised only in a subprocess"
  - "Phase 59 module docstrings start with Phase 59 so glob discovery cannot miss a new module"

requirements-completed: [FEAS-02, FEAS-07, FEAS-08, DIAG-07]

coverage:
  - id: D1
    description: "Hash-checked train/validation allowlist refuses a test-split key before any path is built, including on the real corpus"
    requirement: FEAS-02
    verification:
      - kind: unit
        ref: "tests/phase59/test_split_allowlist.py#ManifestHashTests,RefusalBeforeOpenTests,RefusalPrecedesIOTests,AllowedReadTests,RecordEnumerationTests,ExpectedHashTests,CliFreezeGuardTests,ProhibitionsAllowlistTests"
        status: pass
      - kind: integration
        ref: "pinn.verification.split_allowlist.probe train admitted and test refused_before_path"
        status: pass
    human_judgment: false
  - id: D2
    description: "Audit hook blocks a withheld basename, records an allowed open, and ignores opens outside the data root"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_split_allowlist.py#AuditHookTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Reference trajectories, inner-pair slots, seam-equivalent resident records, and normalizer recovery from stage-0-init.pt"
    requirement: FEAS-02
    verification:
      - kind: unit
        ref: "tests/phase59/test_production_reference.py#ReferenceTests,PairTrackingTests,SeamEquivalenceTests,NormalizerRecoveryTests,MonitorReproductionTests"
        status: pass
      - kind: integration
        ref: "recover_normalizer_from_checkpoint stage-0-init.pt residual 1.192e-7 over 256 keys"
        status: pass
    human_judgment: false
  - id: D4
    description: "Glob-discovered static guards, including injected-violation self-tests, over modules, evidence scripts, and tests"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_static_guards.py#DiscoveryTests,UnlistedModuleTests,ForbiddenNameTests,EvaluatorImportTests,ImportSurfaceTests,CorpusTokenTests,TorchLoadTests,SurveyNonGatingTests,DetectorSelfTests"
        status: pass
    human_judgment: false

duration: 27 min
completed: 2026-10-14
status: complete
---

# Phase 59 Plan 03: Corpus Choke Point Summary

**One allowlisted reader refuses held-out files before a path exists, and reference rows match the trainer's preprocessing**

## Performance

- **Duration:** 27 min
- **Started:** 2026-10-14T02:37:09Z
- **Completed:** 2026-10-14T03:04:18Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- `SplitAllowlist` checks the generation-7 splits SHA-256, admits only train and validation keys, and raises `SplitRefused` before a test-split path is built. A real train record admits; a real test record is refused. Neither probe line contains a filesystem path.
- `load_reference` follows the production per-file seams. On TinyCorpus, `resident_record` matches an oracle the test composes itself. The stage-0-init normalizer recovers with residual `1.192e-7` over 256 record keys.
- Static guards discover Phase 59 modules, evidence scripts, and tests by glob. Each detector fails on an injected violation. No scanned file constructs the admitted-set adapter or imports the held-out evaluator.

## Task Commits

Each task was committed atomically:

1. **Task 1: Tracer — one allowlisted record read, and a test-split record refused before its path exists** - `e91d953b` (feat)
2. **Task 2: Open attestation, reference trajectories, and normalizer recovery** - `4a1dfff9` (test, RED), `44a74c2d` (feat, GREEN)
3. **Task 3: Static guards** - `62f544a9` (test)

**Plan metadata:** this commit (docs)

## Files Created/Modified

- `pinn/verification/split_allowlist.py` - Hash-checked allowlist, per-file reader, probe CLI, and the open-attestation hook
- `pinn/verification/production_reference.py` - Reference trajectories, inner-pair slots, resident records, and checkpoint normalizer recovery
- `tests/phase59/_corpus_fixtures.py` - TinyCorpus plus a synthetic train/validation/test manifest
- `tests/phase59/test_split_allowlist.py` - Refusal, freeze-guard, and subprocess audit-hook tests
- `tests/phase59/test_production_reference.py` - Seam oracle, inner pair, normalizer, and monitor reproduction
- `tests/phase59/test_static_guards.py` - Glob discovery and injected-violation detectors
- `tests/phase39/test_prohibitions.py` - `ALLOWED_CORPUS_READERS` gains only `pinn/verification/split_allowlist.py`, plus three comment lines

## Decisions Made

- Retained `record_keys` are decoded as `[variant, fidelity, id]`, the list `pinn.training.controllers._record_key_payload` writes. The plan's brace notation pointed at that serializer.
- `ReferenceTrajectory` stores `dt_out_reference_provenance` so `resident_record` can fill the trainer's field. The plan's field list omitted it.
- FEAS-02, FEAS-07, FEAS-08, and DIAG-07 are not marked complete in `REQUIREMENTS.md`. Plans 59-04 through 59-10 still declare them.
- `actuals.tokens` is chars/4 of `git diff beb02244..62f544a9` (88031 / 4), the implementation diff before this summary.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Resident records keep dt_out provenance**
- **Found during:** Task 2 (reference trajectories)
- **Issue:** `resident_record` must expose `dt_out_reference_provenance`, but the listed `ReferenceTrajectory` fields did not carry it.
- **Fix:** The reference stores the footer provenance string from the allowlisted read and copies it onto the resident record.
- **Files modified:** `pinn/verification/production_reference.py`
- **Verification:** `SeamEquivalenceTests` passes, including `dt_out_measured`, `k0`, and `uabs0`.
- **Committed in:** `44a74c2d`

**2. [Rule 1 - Bug] Unlisted-module git log has no blank line after paths**
- **Found during:** Task 3 (static guards)
- **Issue:** `git log --name-only` prints a blank line between the subject and its paths, then the next subject immediately. Treating the blank as the end of the commit made the path look like the next subject, so the added-module list was empty.
- **Fix:** A `pinn/verification/` path stays attached to the current subject. Non-path lines start a new subject.
- **Files modified:** `tests/phase59/test_static_guards.py`
- **Verification:** `UnlistedModuleTests` finds `split_allowlist.py` and the other Phase 59 additions.
- **Committed in:** `62f544a9`

---

**Total deviations:** 2 auto-fixed (1 missing critical, 1 bug)
**Impact on plan:** No new threshold, hash, or allowlist rule. The provenance field is the trainer's existing string. The git parser follows the command the plan named.

## TDD Gate Compliance

Task 1 is a tracer, not `tdd="true"`. Tests and the reader landed together in `e91d953b`.

Task 2 is `tdd="true"`. RED commit `4a1dfff9` precedes GREEN commit `44a74c2d`. `gsd-tools check tdd-red-evidence` returned `RED_EVIDENCE_OK` (`target_test_failed`) for `test_load_reference_matches_the_preprocessed_trajectory` at exit 1, assertion `unexpectedly None`. Eight new tests failed; the eleven allowlist tests still passed. No REFACTOR commit.

Task 3 is `tdd="true"` and its only file is the test module. The first run failed `UnlistedModuleTests` on the assertion above. The parser fix and the passing guards are the one `test` commit `62f544a9`. There is no separate GREEN commit because there is no production module beyond the tests.

| Plan | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 59-03 task 1 (tracer, not tdd) | — | e91d953b | — | Not a TDD task |
| 59-03 task 2 | 4a1dfff9 | 44a74c2d | — | Pass |
| 59-03 task 3 | 62f544a9 | — | — | Test-only; first run failed, fix is in that commit |

## Issues Encountered

`NormalizerRecoveryTests` prints a numpy divide-by-zero `RuntimeWarning` while fitting the intentionally corrupted row. The test still raises `NormalizerRecoveryError`. The clean stage-0-init recovery does not warn.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for 59-04. The choke point, the reference path, and the guards are importable. Wave 2 still has the evidence writer. Do not edit the frozen scorecard, `SCORECARD_SHA256`, or the scorer's scoring rules. FEAS-02, FEAS-07, FEAS-08, and DIAG-07 remain pending until the later plans that declare them finish. `.planning/codebase/` was left unchanged: the new modules sit in the existing `pinn/verification/` package.

## Self-Check: PASSED

- `conda run -n pinn-train python -B -m unittest tests.phase59.test_split_allowlist -v`: 11 tests, OK, before the audit-hook tests landed. Eight classes passed.
- Real `probe('train')` admitted hierarchical base id 0 (126 snapshots). `probe('test')` returned `refused_before_path` for id 27. `PROBE-OK`. Neither JSON line contains `/Users/`.
- Adjacent regression after Task 1: 177 tests, OK.
- `unittest tests.phase59.test_production_reference tests.phase59.test_split_allowlist -v`: 19 tests, OK. `AuditHookTests` ran in subprocesses.
- `NORMALIZER-RECOVERY-OK 1.1920928955078125e-07 256`.
- `unittest tests.phase39.test_prohibitions`: 31 tests, OK.
- `unittest tests.phase59.test_static_guards -v`: 15 tests, OK. All nine classes passed.
- `unittest tests.phase59.test_split_allowlist tests.phase59.test_production_reference tests.phase59.test_static_guards -v`: 34 tests, OK.
- `unittest discover -s tests/phase59 -p 'test_*.py' -v`: 112 tests, OK.
- Adjacent regression at closeout: 177 tests, OK.
