---
phase: 43-verification-stage-0-pilot-acceptance
plan: 10
subsystem: held-out-evaluation-authorization
tags: [acc-03, canonical-output, atomic-claim, o-excl, tdd, fail-closed]
status: complete
requires:
  - phase: 43-02
    provides: "synthetic held-out evaluator, fixed gate metrics, and one-time receipt contract"
  - phase: 43-review
    provides: "CR-01 alternate-output replay and CR-02 non-atomic pre-access claim findings"
provides:
  - "One canonical <run_dir>/evaluation authority path for every held-out evaluation"
  - "Durable evaluation-attempt.json claim created atomically before admitted-corpus access"
  - "Synthetic replay, crash, pre-access, and concurrent-claim regression coverage"
affects: [phase-43-verification, held-out-acceptance, evaluation-receipts]
tech-stack:
  added: []
  patterns:
    - "Manifest-only validation precedes a durable O_CREAT|O_EXCL authorization claim"
    - "Failed, abandoned, concurrent, and completed attempts all consume the once-only budget"
key-files:
  created: []
  modified:
    - pinn/evaluate.py
    - tests/phase43/test_evaluate_gate.py
key-decisions:
  - "Use persisted SplitManifest test membership for the empty-split refusal before any claim or corpus access."
  - "Retain the fixed attempt record on every path; successful gate rendering atomically marks it completed after the receipt is written."
patterns-established:
  - "Run-owned authorization: caller output paths cannot relocate evaluation state away from <run_dir>/evaluation."
  - "Crash-safe single use: claim before access, never unlink the claim, then finalize it without reopening the budget."
requirements-completed: [ACC-03]
coverage:
  - id: D1
    description: "A checkpoint can evaluate only into its owning run's canonical evaluation directory; alternate output replay is refused."
    requirement: ACC-03
    verification:
      - kind: unit
        ref: "tests/phase43/test_evaluate_gate.py#ClosedEvaluationFlowTests.test_second_evaluation_cannot_redirect_to_an_alternate_output"
        status: pass
    human_judgment: false
  - id: D2
    description: "The fixed attempt is claimed before held-out materialization, survives injected failure, and admits only one concurrent claimant."
    requirement: ACC-03
    verification:
      - kind: unit
        ref: "tests/phase43/test_evaluate_gate.py#ClosedEvaluationFlowTests.test_attempt_is_claimed_before_test_split_materialization"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_evaluate_gate.py#ClosedEvaluationFlowTests.test_post_claim_failure_preserves_attempt_and_refuses_retry"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_evaluate_gate.py#ClosedEvaluationFlowTests.test_preexisting_attempt_refuses_a_concurrent_claim"
        status: pass
      - kind: other
        ref: "two-thread _claim_evaluation_attempt synthetic race probe"
        status: pass
    human_judgment: false
  - id: D3
    description: "An empty persisted test split is refused before the once-only attempt is consumed."
    requirement: ACC-03
    verification:
      - kind: unit
        ref: "tests/phase43/test_evaluate_gate.py#ClosedEvaluationFlowTests.test_empty_test_refusal_does_not_consume_the_attempt"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_evaluate_edge_cases.py#EmptyTestSetTests"
        status: pass
    human_judgment: false
duration: 6min
completed: 2026-07-22
---

# Phase 43 Plan 10: Once-Only Evaluation Enforcement Summary

**Each run now owns exactly one canonical evaluation path and durably consumes its held-out budget before admitted-corpus access, preventing redirected replay, crash erasure, and concurrent double evaluation.**

## Performance

- **Duration:** 6 min
- **Started:** 2026-07-23T01:47:52Z
- **Completed:** 2026-07-23T01:53:31Z
- **Tasks:** 2
- **Files modified:** 2 task artifacts

## Accomplishments

- Bound `evaluate_run` to exactly `<run_dir>/evaluation`; any other resolved `--output` raises the existing typed `OutputPathEscapeError` before a claim or held-out access.
- Added a fixed `evaluation-attempt.json` created with `os.O_CREAT | os.O_EXCL`, file `fsync`, and directory `fsync` before adapter construction or `StageIndex.from_split(..., "test")`.
- Preserved failed/abandoned attempt claims, finalized successful PASS/FAIL evaluations to a completed attempt after receipt creation, and locked replay/crash/race behavior with synthetic-only regressions.

## Task Commits

Each TDD gate was committed atomically:

1. **Task 2 RED: single-use evaluation regressions** — `c9a6f010` (test)
2. **Task 1 GREEN: canonical output and atomic attempt claim** — `58366ec7` (fix)

**Plan metadata:** this closeout commit (`docs(43-10): complete evaluation claim hardening plan`).

## TDD Evidence

- **RED:** `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_evaluate_gate -v` ran 13 tests and failed as expected on exactly four reproduced bypasses: alternate-output replay, absent pre-materialization claim, missing claim after injected failure, and acceptance of a pre-existing concurrent claim. The empty-test non-consumption control passed.
- **GREEN:** the same command ran 13 tests, all passing.

## Files Created/Modified

- `pinn/evaluate.py` — canonical run-owned output check, fixed attempt schema/path, durable exclusive claim, fail-closed prior-attempt refusal, and completed-attempt finalization.
- `tests/phase43/test_evaluate_gate.py` — synthetic alternate-output, claim-order, injected-failure, concurrent-attempt, and empty-pre-access regressions.

## Decisions Made

- Used `SplitManifest.fixed_order("test")` to reject a persisted empty test split before claiming; this is manifest metadata only and avoids admitted-corpus access.
- Placed the exclusive claim before `AdmittedSetAdapter` construction, which is stricter than merely placing it before `StageIndex.from_split`: any corpus-load exception now leaves honest consumed-attempt evidence.
- Kept `evaluation-attempt.json` at its fixed path after success and atomically changed its status to `completed`; no path removes a claim or recreates a clean evaluation window.

## Deviations from Plan

None - plan executed exactly as written. The RED test commit precedes GREEN production code because both tasks are explicitly TDD.

## Issues Encountered

None. The four RED failures were expected evidence and flipped to GREEN without touching the real held-out evaluator or expanding scope.

## Verification

- `<home>/miniforge3/envs/pinn-train/bin/python -c "import ast; ast.parse(open('pinn/evaluate.py').read()); print('parse-ok')"` — **PASS**, printed `parse-ok`.
- `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_evaluate_gate -v` — **13/13 pass** using `TinyCorpus` synthetic fixtures only.
- `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_evaluate_gate tests.phase43.test_evaluate_edge_cases tests.phase43.test_summary_enrichment -v` — **28/28 pass**.
- Independent two-thread `_claim_evaluation_attempt` race probe — **PASS**, printed `concurrent-claim-ok results=['claimed', 'refused']` and left one fixed attempt file.
- Independent source-order probe — **PASS**, proved claim call `<` adapter construction `<` `StageIndex.from_split`, confirmed canonical equality is present, and found no attempt unlink.
- Independent synthetic finalization probe — **PASS**, printed `attempt-finalization-ok status=completed receipt_exists=True`.
- `git diff --check c9a6f01^..58366ec -- pinn/evaluate.py tests/phase43/test_evaluate_gate.py` — **PASS**.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- CR-01 and CR-02 are closed with structural enforcement and adversarial synthetic evidence; the exhausted real held-out receipt remains untouched.
- `ACC-03` was already marked Complete in `.planning/REQUIREMENTS.md`; no requirements mutation was needed.
- Per the worktree single-writer contract, this executor did not modify the already-dirty `.planning/STATE.md` or `.planning/ROADMAP.md`; the execute-phase orchestrator owns their post-plan synchronization.

## Known Stubs

None. The attempt's `in_progress` state is a durable operational record for an active or abandoned evaluation, not placeholder output.

## Self-Check: PASSED

- `pinn/evaluate.py`, `tests/phase43/test_evaluate_gate.py`, and `43-10-SUMMARY.md` exist on disk.
- Commits `c9a6f010` and `58366ec7` exist in Git history and each contains only its declared owned file.
- The exact plan-level test command passed 13/13; the neighboring evaluator/summary slice passed 28/28.
- GSD coverage classification parsed all three deliverables with `all_auto_covered: true` and no schema errors.
- No real held-out evaluator invocation, real receipt mutation, package install, network endpoint, auth path, or unrelated file change occurred.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-22*
