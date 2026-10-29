---
phase: 65-probe-on-the-record-fit-harness
plan: "02"
subsystem: testing
tags: [pinn, diagnostic-harness, data-boundary, stage0-admission, recorded-normalizer, physical-windows, tdd]

requires:
  - phase: 65-probe-on-the-record-fit-harness
    provides: Wave 0 module conventions, the four tests/phase65 modules and the sealed variant registry
  - phase: 60-single-system-learnability
    provides: INST-05 data seam (load_arm_data, DataContext, ArmData, RecordView), pinned split_allowlist.py and learnability_data.py, EXPECTED_STATS_SHA256
  - phase: 59-read-only-baseline-scorecard
    provides: evidence/audit/reader_acceptance.json normalizer block and its committed manifest digest
provides:
  - Stage0TrainingReader, require_stage0_training and the all-key prevalidation adapter: train split plus manifest orbit stage 0 before every read, exists or path resolution
  - open_diagnostic_context: the guarded context built from committed metadata only, with the process open attestation as the second independent test-split check
  - load_recorded_stats: the retained IC13 normalizer hydrated from the Phase 59 reader-acceptance evidence under a three-way digest check
  - validate_window / physical_window / the windowed load_diagnostic_data: exact float64 windows with locked-T tau and separately recorded physical time
affects: [65-03, 65-04, 65-05, 65-06]

actuals:
  tokens: 16680   # chars/4 over the realized diff (66719 chars across the four task commits)
  tasks: 2
  commits: 4

tech-stack:
  added: []
  patterns:
    - "Admission precedes I/O: the split allowlist is required to be train and the manifest orbit stage required to be 0 before any reader, exists or path call, for target and ancillary keys alike, with all assigned keys validated as a set before the first read"
    - "Evidence-first hydration: the Phase 59 evidence file is hashed before parsing, checked against the committed manifest entry, and the hydrated statistics must reproduce stats_digest, the recorded stats_sha256 and EXPECTED_STATS_SHA256 before any data access"
    - "Sentinel-keyed defaults: omitting window_length keeps the scored horizon while an explicit value (including None) is validated, so a fail-closed check cannot be silently bypassed by a defaulted argument"

key-files:
  created:
    - pinn/verification/diagnostic_data.py
  modified:
    - tests/phase65/test_contracts.py
    - tests/phase65/test_isolation.py

key-decisions:
  - "Manifest stage is read at the orbit level (the group signature's base_stage); the split schema forces every gold record's own stage label to UNASSIGNED, so a record-level stage check would refuse every gold key forever. Both stage readings are recorded on every open"
  - "window_length uses a sentinel default: omitted means the scored horizon (the Task 65-02-01 call sites stay unchanged), while an explicit value — including None — goes through validate_window and a non-real number refuses"
  - "Two intentional time grids: the recorded times_physical/tau are the exact float64 record grid, the same array the score and beside views carry, while tau_ic13 keeps the resident float32 snapshot times so the training tensor stays bitwise equal to the load_arm_data seam"
  - "The under-two-samples refusal necessarily follows the target read (the record's timestamps are needed to count retained samples); only windows outside (0, 10] refuse before any read"

patterns-established:
  - "Guarded-reader subclassing: Stage0TrainingReader stays an AllowlistedCorpusReader so production_reference.load_reference's type check and the whole preprocessing chain are reused unchanged; the pinned modules are never edited"
  - "Independent double check: the process open attestation counts every corpus open by split, refusing withheld basenames, as a second test-split guard beside the admission boundary"

requirements-completed: []   # DIAG-09 and INST-08 span later Phase 65 plans; this plan alone completes neither

coverage:
  - id: D1
    description: "Stage-0 training admission boundary: valid stage-0 train keys read; validation, test, Stage-1, UNASSIGNED and unknown keys refuse before any reader, exists or path call; an invalid ancillary key blocks an otherwise valid target with zero opens; the seven committed Phase 60 arms admit on metadata alone; the process attestation refuses a withheld key and construction needs metadata only"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_isolation.py#Stage0AdmissionTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_isolation.py#Stage0LoadTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_isolation.py#CommittedArmBoundaryTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_isolation.py#AttestationIntegrationTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Recorded normalizer hydration: reader_acceptance.json reproduces EXPECTED_STATS_SHA256 with the committed evidence digest checked before parsing; changed evidence, tampered statistics, zero stds, substituted subsets, wrong or missing digests halt; no recovery, refit or record read during hydration or context construction"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_contracts.py#RecordedNormalizerTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Physical windows and coordinates: exact endpoint membership with nextafter-below/above, duplicate/unsorted/non-finite time refusals, out-of-domain windows (including NaN, infinity, non-numbers and an explicit None) refused before any read, at-least-two-samples refusal, tau on the locked T_CHARACTERISTIC_TIME never rescaled, one shared ordered time grid across target rows, scores and comparisons, retained indices recorded, and the full window bitwise-matching the existing scored horizon"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_contracts.py#WindowBoundaryTests"
        status: pass
    human_judgment: false

duration: 23 min
completed: 2026-10-29
status: complete
---

# Phase 65 Plan 02: Probe on the Record & Fit Harness — Stage-0 Data Boundary Summary

**One guarded Stage-0 training data seam: train-split-plus-manifest-stage-0 admission before every corpus operation, the retained IC13 normalizer hydrated exactly from hash-checked Phase 59 evidence under a three-way digest check, and exact float64 physical windows whose tau uses the locked characteristic time.**

## Performance

- **Duration:** about 23 min across two executor sessions (2026-10-29 03:41–04:04 UTC), including an interruption between sessions (see Deviations)
- **Started:** 2026-10-29T03:41:00Z (first executor session; the first task commit is 03:44:20Z)
- **Completed:** 2026-10-29T04:04:26Z
- **Tasks:** 2 of 2
- **Files modified:** 1 created (`pinn/verification/diagnostic_data.py`), 2 test files extended
- **Verify latency:** the two-module verify command runs 52 tests in 0.93 s; the full Phase 65 suite runs 83 tests in 1.49 s

## Accomplishments

- `Stage0TrainingReader`/`require_stage0_training` admit only training-split orbits whose manifest stage (the group signature's `base_stage`) is 0, before any `read`, `exists` or `_brutus_path` call, and `load_diagnostic_data` validates the train, score and beside keys as a set before the first read, so an invalid ancillary key blocks an otherwise valid target with zero corpus opens. Validation, test, Stage-1, UNASSIGNED and unknown keys refuse; the reader stays an `AllowlistedCorpusReader`, so `production_reference.load_reference`'s type check and the whole preprocessing chain (residency, raw masses, IC13, body permutation) are reused unchanged, and an admitted record is bitwise identical to the plain `load_arm_data` path.
- `open_diagnostic_context` builds the guarded context from committed metadata only: the hash-checked generation-7 split manifest, the process open attestation (the second, independent test-split check, which refuses a withheld basename and counts every open by split), the Stage-0 reader, and the recorded normalizer. `open_real_context`, `recover_normalizer_from_checkpoint`, `fallback_normalizer_from_allowlist` and `compute_normalization_stats` are never invoked (proven by spies); the historical helper's 256-monitor recovery would include 16 Stage-1 identities outside this phase's read authority.
- `load_recorded_stats` hashes the Phase 59 `reader_acceptance.json` before parsing, checks the digest against the committed manifest entry, hydrates `NormalizationStats` from the recorded `slot_means`/`slot_stds`/`e_scale` (exactly 12 finite numbers each, no zero stds, non-zero finite e_scale), and requires `stats_digest(stats)`, the recorded `stats_sha256` and `EXPECTED_STATS_SHA256` (`77526e53…79f6`) to agree before any data access. Changed evidence, tampered statistics, substituted subsets and wrong or missing digests all halt as `DiagnosticDataRefused`.
- Windows are exact float64 masks `0 <= t <= window_length`: the upper endpoint is included exactly once, everything above it excluded (nextafter-below/above pinned), timestamps must be finite, distinct and strictly increasing (duplicates never duplicate a sample), at least two retained samples are required, and windows outside `(0, T_CHARACTERISTIC_TIME]` — including NaN, infinities, non-numbers and an explicit `None` — refuse before any read. `tau` is computed with the locked `T_CHARACTERISTIC_TIME`, never rescaled to the shorter window; the record carries `times_physical` and `tau` separately in float64 from the exact record grid, the same array the score and beside views carry. Omitting `window_length` keeps the scored horizon, so the Task 65-02-01 call sites are unchanged and the full window is bitwise the existing scored horizon.
- The record additions this plan requires are all present: `stats_sha256`, normalizer evidence path/hash, split-manifest hash (`splits_sha256`), the requested physical window, retained sample indices, physical-time and tau coordinates, and requested/opened keys with split and both stage readings (`refused_before_open`/`actual_opens` counters included).

## Task Commits

Each task followed RED → GREEN (TDD); each RED was machine-verified `RED_EVIDENCE_OK` (`check tdd-red-evidence`, per the RED commit records):

1. **65-02-01 enforce Stage-0 TRAIN before every corpus operation** — `56bac6e6` (test) + `b64f4ba0` (feat)
2. **65-02-02 hydrate retained statistics and preserve physical windows** — `dadb523b` (test) + `22768976` (feat)

**Plan metadata:** this commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_data.py` — the whole guarded seam: `Stage0TrainingReader`, `require_stage0_training`, `open_diagnostic_context`, `load_recorded_stats`, `validate_window`, `physical_window`, the windowed `load_diagnostic_data`, `one_orbit_spec`
- `tests/phase65/test_isolation.py` — admission, all-key prevalidation, attestation-integration, committed-arm and module-symbol tests (+325 lines with test_contracts)
- `tests/phase65/test_contracts.py` — `RecordedNormalizerTests` and `WindowBoundaryTests`

## Verification Commands and Outcomes

- `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase65.test_contracts tests.phase65.test_isolation -v` → 52 tests OK (exit 0)
- `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase65 -p 'test_*.py'` → 83 tests OK, 1.486 s (includes the 33-file pinned-digest guard: `load_protocol()` revalidates every `PINNED_MODULES` digest at the current tree; `split_allowlist.py` and `learnability_data.py` are byte-identical to their pinned state — `git status` shows no change to them)
- `git diff --check` → clean
- No real corpus record was opened by this plan: every read in the suite goes through the TinyCorpus fixture under a temporary root; the real split manifest, Phase 59 evidence and scorecard are metadata reads only; `open_diagnostic_context` is exercised with spies proving zero train/validation/test-split opens; no `runs/` tree was created

## Decisions Made

- **Stage semantics:** the manifest schema forces every gold record's own stage label to `UNASSIGNED` (`pinn/data/splits.py` refuses a numeric gold stage), so the admission stage is the orbit's — the group signature's `base_stage`. Both readings are recorded on every open; standard-variant (UNASSIGNED) and Stage-1 orbits refuse.
- **Sentinel default for `window_length`:** omitted keeps the scored horizon (all Task 65-02-01 call sites unchanged); an explicit value — including `None` — is validated by `validate_window`, and a non-real number refuses before any read.
- **Two intentional time grids:** the record's `times_physical`/`tau` are the exact float64 record grid (identical to the score/beside view grids, satisfying the one-ordered-grid acceptance criterion), while `tau_ic13` keeps the resident float32 snapshot times so the training tensor is bitwise the `load_arm_data` seam (pinned by `test_the_full_window_matches_the_existing_scored_horizon`).
- **Under-two-samples check placement:** counting retained samples requires the record's timestamps, so that refusal necessarily follows the target read; only out-of-domain windows refuse before any read, exactly as the plan's action sentence scopes it.

## Deviations from Plan

### Auto-fixed Issues

**1. [Process - Interruption/resume] Plan interrupted mid-GREEN of Task 65-02-02 and resumed by a fresh executor**
- **Found during:** Task 65-02-02 GREEN (previous executor session)
- **Issue:** the previous executor was interrupted after committing the Task 2 RED (`dadb523b`) with a partial, uncommitted GREEN draft in `pinn/verification/diagnostic_data.py` and `tests/phase65/test_contracts.py`; the draft left 3 of 52 tests failing.
- **Fix:** the uncommitted task-owned changes were inspected (not reverted): the hydration, context and windowing structure was correct and was kept; three defects were corrected — (a) `window_length=None` silently meant the scored horizon, defeating the committed RED contract that an explicit `None` refuses (replaced with a sentinel default distinguishing omitted from explicit), (b) the under-sample refusal messages wrote the digit "2" where the RED asserts the word "two", and (c) the recorded `times_physical`/`tau` used the float32-resident times, so the train grid differed from the score views by float32 rounding (now the exact float64 record grid, with `tau_ic13` deliberately kept on the resident times for seam parity). Three test-side bugs in the draft were also fixed (see Issues Encountered).
- **Files modified:** `pinn/verification/diagnostic_data.py`, `tests/phase65/test_contracts.py`
- **Verification:** the plan's verify command now exits 0 (52 tests); the full Phase 65 suite passes (83 tests).
- **Committed in:** `22768976` (Task 65-02-02 GREEN)

---

**Total deviations:** 1 auto-fixed (interruption/resume completing the interrupted GREEN)
**Impact on plan:** No scope creep. The committed RED contracts were honored, not weakened; the pinned allowlist and data modules are untouched.

## TDD Gate Compliance

Both tasks committed a `test(65-02)` RED before their `feat(65-02)` GREEN (`56bac6e6` → `b64f4fa0`; `dadb523b` → `22768976`), and each RED was machine-verified `RED_EVIDENCE_OK` at commit time (recorded in the RED commit bodies: Task 1 on the missing boundary symbols, Task 2 on the missing Task 2 symbols). No REFACTOR commit: the final implementation needed no post-GREEN cleanup.

## Issues Encountered

Three test-side bugs in the interrupted GREEN draft were corrected (test bugs, not contract changes — the same classification as Wave 0's GREEN-phase corrections):
- `WindowBoundaryTests._load` dropped an explicit `None` (`if window_length is not None`), so the committed `bad=None` subtest could never reach the implementation; the helper now forwards `None` through a sentinel and the implementation refuses it.
- The under-two-samples test initially asserted `actual_opens == 1` after calling `_gold_times()` through the same reader (cumulative count 2); it now asserts exactly one additional open.
- The adjacency assertion `np.testing.assert_array_equal(np.diff(times), np.diff(times))` compared an array to itself and asserted nothing; it now pins tau steps to the locked-T conversion of the physical steps (`np.diff(tau) == (2/T) · np.diff(times)` within 1e-14).

## User Setup Required

None — no external service configuration; everything runs on the local `pinn-train` environment.

## Known Stubs

None — every delivered path is real; no placeholder, TODO or unwired data source remains.

## Next Phase Readiness

- Plan 65-03 (production refusal wiring) can build on `require_not_diagnostic`/`DiagnosticArtifactRefused` from Wave 0 and the reader boundary here; `open_diagnostic_context` is the one entry the probe and fit use to acquire a faithful guarded context without reopening the normalizer population.
- The one-orbit gold spec, exact windows and recorded statistics are ready for the Phase 65 probe registration and the read-only reproduction; research A3 is resolved (recorded-statistics hydration replaces monitor recovery).
- No blocker. DIAG-09 and INST-08 stay open (later plans own them); the held-out evaluation remains unspent and no real corpus record was opened.

---
*Phase: 65-probe-on-the-record-fit-harness*
*Completed: 2026-10-29*

## Self-Check: PASSED

All three key files exist on disk; all five plan commits (`56bac6e6`, `b64f4ba0`, `dadb523b`, `22768976`, `e51ab3cd`, plus the SUMMARY hash correction `13588cd9`) are in history with `b64f4ba0` verified an ancestor of HEAD via `git merge-base --is-ancestor`; the RED/GREEN gate sequence is present for both tasks; the plan's verify command (52 tests) and the full Phase 65 suite (83 tests) exit 0 at the final tree.
