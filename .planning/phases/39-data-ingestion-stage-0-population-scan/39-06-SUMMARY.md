---
phase: 39-data-ingestion-stage-0-population-scan
plan: "06"
subsystem: data
tags: [population-scan, persisted-labels, atomic-json, split-manifest, readiness]

# Dependency graph
requires:
  - phase: 39-03
    provides: "AdmittedSetAdapter residency, persisted labels, disposition accounting, version state, and resident-byte observability"
  - phase: 39-04
    provides: "Canonical split writer and train-restricted StageIndex.from_split diagnostic seam"
provides:
  - "Deterministic DATA-06 population evidence derived from persisted admitted-record labels"
  - "Sole-classifier read-only s0 sensitivity sweep with portable minimum-separation evidence"
  - "Atomic scan CLI that materializes and hashes splits.json before SPEC-bound readiness exit 0/2"
affects: [39-07, 40-training-loop]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Persisted StageLabel values own report membership; classifier reuse is diagnostic-only"
    - "Sibling-temp flush/fsync/replace protects deterministic JSON and scan-log writes"
    - "Admitted/full Stage-0 count is the sole fatal operand; train count is downstream-only evidence"

key-files:
  created:
    - pinn/data/stage_scan.py
  modified:
    - tests/phase39/test_stage_scan.py

key-decisions:
  - "Bind DATA-06 readiness exclusively to stage0_full_split_count with threshold 240; stage0_train_split_count cannot change the verdict."
  - "Use record.stage_label for all population membership and call classify_stage_label only for the reversible {0.5,1,2} sensitivity grid."
  - "Materialize and hash the canonical splits.json before building readiness evidence, including on the fatal exit-2 path."
  - "Attach the complete report to the existing canonical StageZeroUnderpopulated instance because its frozen constructor accepts only observed and threshold."

patterns-established:
  - "Population evidence contains structural counts, unique resident bytes, exact sorted s_min values, quantiles, per-variant/fidelity views, and no source paths."
  - "CLI readiness produces only exit 0 or 2 after preserving splits.json, stage_population.json, and scan.log."

requirements-completed: [DATA-06]

coverage:
  - id: D1
    description: "Persisted-label population counts, gold fail-closed semantics, resident-byte accounting, portable s_min evidence, and sole-seam sensitivity diagnostics"
    requirement: DATA-06
    verification:
      - kind: unit
        ref: "tests/phase39/test_stage_scan.py#PopulationReportContract"
        status: pass
    human_judgment: false
  - id: D2
    description: "Admitted/full Stage-0 fatal boundaries at 0, 239, and 240 with diagnostic-only train count and complete fatal report retention"
    requirement: DATA-06
    verification:
      - kind: unit
        ref: "tests/phase39/test_stage_scan.py#PopulationReportContract.test_full_count_zero_and_239_raise_with_complete_report_attached"
        status: pass
      - kind: integration
        ref: "tests/phase39/test_stage_scan.py#PopulationReportContract.test_full_ge_240_with_low_train_split_is_nonfatal"
        status: pass
    human_judgment: false
  - id: D3
    description: "Atomic canonical report bytes, corpus-root rejection, canonical split materialization/hash identity, all CLI flags, and deterministic PASS/fatal artifacts"
    requirement: DATA-06
    verification:
      - kind: unit
        ref: "tests/phase39/test_stage_scan.py#PopulationReportWriterContract"
        status: pass
      - kind: integration
        ref: "tests/phase39/test_stage_scan.py#StageScanCliContract"
        status: pass
    human_judgment: false

# Metrics
duration: 17min
completed: 2026-07-15
status: complete
---

# Phase 39 Plan 06: Deterministic Stage-0 Population Scan Summary

**DATA-06 now has a portable persisted-label population report and atomic CLI whose sole fatal operand is the admitted/full Stage-0 count, with canonical split bytes retained and hashed before either exit 0 or exit 2.**

## Performance

- **Duration:** 17 min
- **Started:** 2026-07-15T11:00:00Z
- **Completed:** 2026-07-15T11:17:06Z
- **Tasks:** 2
- **Files modified:** 2 production/test files (plus this summary)

## Accomplishments

- Built deterministic population evidence from admitted records' persisted `StageLabel` values, including record and physical-key counts, unique resident tensor bytes, exact sorted float64 minimum-separation values, quantiles, per-variant/fidelity distributions, and explicit zero-gold-numeric enforcement.
- Added the reversible `{0.5, 1, 2} * interim_s0` diagnostic sweep through the sole shared `classify_stage_label` seam without changing persisted labels, thresholds, residency, or adding Stage 2-6.
- Bound `StageZeroUnderpopulated` exclusively to `stage0_full_split_count < 240`; a train-restricted count below 240 remains diagnostic Phase-40 evidence and cannot alter DATA-06 readiness.
- Added canonical atomic `stage_population.json` and `scan.log` writers plus a testable CLI that materializes `splits.json`, records its SHA-256/size/byte identity before readiness, forwards every explicit adapter/split option, and preserves fatal artifacts before exit 2.

## Task Commits

Both tasks followed RED -> GREEN TDD and were committed atomically through `scripts/agent-commit`:

1. **Task 39-06-01 RED: population report contract** — `8fdaee74` (test)
2. **Task 39-06-01 GREEN: deterministic persisted-label report** — `ac43d1c` (feat)
3. **Task 39-06-02 RED: atomic writer and CLI contract** — `9a1dd16` (test)
4. **Task 39-06-02 GREEN: split-first scan orchestration and exits** — `1cb2670` (feat)

**Plan metadata:** this SUMMARY only; parent phase orchestration owns shared STATE/ROADMAP/REQUIREMENTS updates.

## Files Created/Modified

- `pinn/data/stage_scan.py` — portable population-report builder, fatal boundary, sensitivity diagnostics, atomic writers, split identity log, CLI flags, and exit semantics.
- `tests/phase39/test_stage_scan.py` — activated and expanded DATA-06 report, boundary, portability, writer, manifest, CLI, flag-forwarding, and fatal-artifact coverage.

## Decisions Made

- **Treat persisted labels as authoritative.** Report membership reads only `record.stage_label`; the classifier is invoked solely for a clearly labeled, read-only sensitivity sweep.
- **Keep readiness independent of split ratios.** The admitted/full Stage-0 count is the only DATA-06 operand; the train count is reported for Phase 40 without becoming a second gate.
- **Persist split evidence before the verdict.** `main` writes the real DATA-04 manifest, verifies two byte reads, records its SHA-256 and byte size, then evaluates population readiness.
- **Keep report bytes portable at creation.** Structural identity, counts, hashes, and classifier provenance are retained while corpus roots, source paths, usernames, and hostnames never enter the report.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking canonical-exception interface gap] Attached the fatal report after constructing the frozen exception**
- **Found during:** Task 39-06-01 GREEN fatal-boundary implementation
- **Issue:** The existing canonical `StageZeroUnderpopulated` constructor accepts only `observed` and `threshold`, while Plan 39-06 requires the fully built report to travel on the exception so the CLI can persist it before exit 2.
- **Fix:** Constructed the canonical exception with its supported arguments, attached the completed report as `error.report`, and raised the same exception type. No shared type or cross-plan file was changed.
- **Files modified:** `pinn/data/stage_scan.py`, `tests/phase39/test_stage_scan.py`
- **Verification:** `PopulationReportContract.test_full_count_zero_and_239_raise_with_complete_report_attached`; `StageScanCliContract.test_cli_fatal_writes_report_manifest_and_log_before_exit_two`
- **Committed in:** `ac43d1c`, exercised end-to-end in `1cb2670`

---

**Total deviations:** 1 auto-fixed canonical-interface gap. **Impact:** the required fatal report remains available without changing the shared exception constructor or DATA-06 semantics.

## Issues Encountered

- Full Phase-39 discovery has one confirmed pre-existing integration error: `test_adapter.EndToEndIntegrationTests.test_full_chain_wires_without_breaking_module_boundaries` calls `build_stage_batch(adapter, stage=0)` without its required `rng`, `dtype`, and `device` keyword arguments. `git show b776410f` confirms both the required signature and stale test call existed at this plan's starting commit. The remaining 218 tests pass, including every stage-scan and prohibition test; fixing the unrelated DATA-05 test is outside Plan-39-06 ownership.

## Known Stubs

None. No TODO/FIXME, placeholder result, empty UI data source, threshold ratification, alternate classifier, or deferred implementation remains in the files changed by this plan.

## User Setup Required

None for implementation verification. Real-corpus execution and evidence closeout remain Plan 39-07 responsibilities and were not run by this plan.

## Next Phase Readiness

- Plan 39-07 can invoke `python -m pinn.data.stage_scan --run-dir X`, verify the retained manifest/report/log byte identities, and perform the real-corpus evidence closeout.
- Phase 40 can consume the diagnostic train-split Stage-0 count without changing DATA-06's admitted/full readiness invariant.
- No Plan-39-07 evidence, review artifact, STATE, ROADMAP, REQUIREMENTS, or shared review file was modified here.

## Verification

- `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stage_scan -v` — **PASS**, 16 tests, 0 failures, 0 skips.
- `$HOME/miniforge3/envs/pinn-train/bin/python -m py_compile pinn/data/stage_scan.py tests/phase39/test_stage_scan.py` — **PASS**.
- `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py' -v` — **218/219 PASS**; one confirmed pre-existing DATA-05 integration-call error described above. All 16 stage-scan tests and all static prohibition tests pass.
- `git diff --check b776410f..HEAD -- pinn/data/stage_scan.py tests/phase39/test_stage_scan.py` — **PASS**.

## Self-Check: PASSED (Plan-Owned Deliverables)

- `pinn/data/stage_scan.py`, `tests/phase39/test_stage_scan.py`, and this SUMMARY exist on disk.
- TDD commits `8fdaee74`, `ac43d1c`, `9a1dd16`, and `1cb2670` exist in `milestone/v2.0` history.
- The focused Plan-39-06 suite passes 16/16 with no skips; all owned stage-scan and static-prohibition checks are green.
- The full discovery command is **not claimed as passing**: it ran 219 tests with 218 passes and one confirmed pre-existing DATA-05 stale-call error present at `b776410f`.
- Shared STATE, ROADMAP, REQUIREMENTS, Plan-39-07, and review artifacts were not modified by this executor.

---
*Phase: 39-data-ingestion-stage-0-population-scan*
*Completed: 2026-07-15*
