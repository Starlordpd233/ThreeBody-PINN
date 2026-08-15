---
phase: 50-valid-stage-0-re-run
plan: 04
subsystem: training
tags: [validation, conformance, C-09, GAP-50-02, full-pool]

requires:
  - phase: 50-02
    provides: generation-2 terminal record and GAP-50-01/02 ruling
provides:
  - full-pool validation selector select_validation_records
  - RunController._validation_batch over the entire held-out Stage-<=k pool
  - closed C-09 divergence with passing proof test
  - two open qualifications for spec-silent RNG coupling and snapshot resampling
  - generation-3 pre-registration amendment and open ledger slot
affects: [50-05-generation-3-run-window, 50-03-evidence-extraction]

actuals:
  tokens: 18000
  tasks: 4
  commits: 4

tech-stack:
  added: []
  patterns:
    - validation identity set is sorted(records_at_or_below(k)) with no sampling
    - empty held-out pool raises ValidationPoolEmpty fail-closed

key-files:
  created:
    - tests/phase50/__init__.py
    - tests/phase50/_fixtures.py
    - tests/phase50/test_validation_full_pool.py
    - .planning/phases/50-valid-stage-0-re-run/COVERAGE.md
    - .planning/phases/50-valid-stage-0-re-run/50-04-SUMMARY.md
  modified:
    - pinn/data/types.py
    - pinn/data/batches.py
    - pinn/training/controllers.py
    - pinn/train.py
    - pinn/conformance/divergence_register.json
    - pinn/conformance/register.py
    - tests/phase40/test_optimizer_phase.py
    - .planning/phases/50-valid-stage-0-re-run/50-PRE-REGISTRATION.md
    - .planning/phases/50-valid-stage-0-re-run/50-CONFIG-DELTA.md
    - .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md

key-decisions:
  - "Validation identity set is exactly sorted(validation_source.records_at_or_below(k)); no sampling, no lookahead."
  - "DATA-05 replay_count stays 240; no constant equals the observed 227."
  - "Shared-RNG coupling and per-event snapshot resampling are recorded as open qualifications, not repaired."
  - "Generation-3 source identity is 312f3080ab50e35be18ba87c9f0618866265b227 (C-09)."

patterns-established:
  - "Held-out validation uses select_validation_records; train batches keep select_stage_records."
  - "Empty validation pool raises ValidationPoolEmpty, mirroring ValidationGateUnavailable."

requirements-completed: [RUN-01, RUN-02]

coverage:
  - id: D1
    description: Full-pool validation selector and end-to-end tracer that a pool smaller than replay_count no longer raises StageZeroUnderpopulated
    requirement: RUN-01
    verification:
      - kind: unit
        ref: tests/phase50/test_validation_full_pool.py#ValidationFullPoolTests.test_validation_pool_below_replay_count_no_longer_raises
        status: pass
    human_judgment: false
  - id: D2
    description: Guard suite pins full-pool identity, no lookahead, event determinism, untouched 240+16 train path, empty-pool refusal, and blacklist/non-Set-1a rejection
    requirement: RUN-01
    verification:
      - kind: unit
        ref: tests/phase50/test_validation_full_pool.py#ValidationFullPoolTests
        status: pass
    human_judgment: false
  - id: D3
    description: Closed C-09 divergence with both ctl_instruction.md citations and a passing proof test, plus two open qualifications
    requirement: RUN-02
    verification:
      - kind: unit
        ref: tests/phase50/test_validation_full_pool.py#ValidationFullPoolTests.test_validation_pool_below_replay_count_no_longer_raises
        status: pass
      - kind: other
        ref: python -c REGISTER-OK/PROOF-TEST-OK against pinn/conformance/divergence_register.json
        status: pass
    human_judgment: false
  - id: D4
    description: Generation-3 pre-registration amendment with byte-identical selection_policy, verified config non-delta, and open ledger scaffold
    requirement: RUN-02
    verification:
      - kind: other
        ref: python -c PREREG-OK/LEDGER-SCAFFOLD-OK plus git show hash re-derivation
        status: pass
    human_judgment: false

duration: 18min
completed: 2026-08-15
status: complete
---

# Phase 50 Plan 04: Full-Pool Validation Repair Summary

**`_run_validation` now evaluates the entire held-out Stage-<=k validation pool with no replay draw and no lookahead; C-09 is closed; generation 3 has a source identity and an open ledger slot**

## Performance

- **Duration:** 18 min
- **Started:** 2026-08-15T02:18:34Z
- **Completed:** 2026-08-15T02:36:02Z
- **Tasks:** 4
- **Files modified:** 16

## Accomplishments

- Added `ValidationPoolEmpty`, `select_validation_records`, and `RunController._validation_batch`; `_run_validation` no longer calls `_stage_batch`.
- Pinned the repaired population from both sides: validation is the full sorted held-out pool; training still draws exactly 240 replay + 16 lookahead.
- Closed register entry C-09 against both `ctl_instruction.md` sections, with a passing proof test. Recorded the shared-RNG coupling and per-event snapshot resampling as open qualifications.
- Amended `50-PRE-REGISTRATION.md` for generation 3 with a byte-identical `selection_policy`, a verified config non-delta, and an open generation-3 ledger scaffold.

## Task Commits

Each task was committed atomically:

1. **Task 1: Full-pool validation selector and tracer** - `84595d0dd9c2ddd628e108a5130f493754762dfb` (feat)
2. **Task 2: Guard suite and stub docstring correction** - `bc1deb849f8d82165fea3f5d6faf12cb8218cb69` (test)
3. **Task 3: C-09 register + qualifications + COVERAGE.md** - `312f3080ab50e35be18ba87c9f0618866265b227` (fix) — **generation-3 source identity**
4. **Task 4: Generation-3 pre-registration, config non-delta, ledger scaffold, SUMMARY** - this commit (plan)

_Note: Task 2 full hash is recorded from `git log` at SUMMARY write; Task 4 hash is this commit._

## Files Created/Modified

- `pinn/data/types.py` — `ValidationPoolEmpty`
- `pinn/data/batches.py` — `select_validation_records` (no rng, no replay_count, no lookahead, no `_sample_keys`, no `has_stage`)
- `pinn/training/controllers.py` — `_validation_batch`; `_run_validation` switched off `_stage_batch`
- `pinn/train.py` — `_synthetic_split_sources` docstring no longer claims the 240 floor applies to validation; defaults stay 240/240
- `pinn/conformance/divergence_register.json` — C-09 closed; VALIDATION-TRAIN-RNG-COUPLING and VALIDATION-SNAPSHOT-RESAMPLING open
- `pinn/conformance/register.py` — `_resolve_proof_test` also accepts `path.py.Class.method` so the plan's unittest proof invocation resolves
- `tests/phase50/` — tracer + six guards
- `tests/phase40/test_optimizer_phase.py` — validation-wiring spy retargeted to `_validation_batch`
- `.planning/phases/50-valid-stage-0-re-run/COVERAGE.md` — no-external-API declaration
- `.planning/phases/50-valid-stage-0-re-run/50-PRE-REGISTRATION.md` — generation-3 amendment
- `.planning/phases/50-valid-stage-0-re-run/50-CONFIG-DELTA.md` — generation 3 config delta verified identical
- `.planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md` — open generation-3 scaffold; generations 1/2 and `final_band_generation` untouched

## Decisions Made

Followed GAP-50-02 Option A as locked. `replay_count` remains 240. No constant equals 227. Train-side `_stage_batch` is behaviorally untouched. The two spec-silent observations were recorded, not repaired.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Phase-40 validation-wiring spy still wrapped `build_stage_batch`**
- **Found during:** Task 3 (phase40 discover)
- **Issue:** `test_validation_pass_wiring_is_real_and_matches_direct_recompute` captured `batch` from `build_stage_batch` on the validation source. After the repair `_run_validation` no longer calls that path, so the spy never saw a batch.
- **Fix:** Spy `_validation_batch` instead.
- **Files modified:** `tests/phase40/test_optimizer_phase.py`
- **Verification:** that test plus full `discover -s tests/phase40` 170 passed
- **Committed in:** `312f3080ab50e35be18ba87c9f0618866265b227` (Task 3)

**2. [Rule 1 - Bug] Plan verify's unittest invocation cannot load `path::Class::method`**
- **Found during:** Task 3 register proof-test gate
- **Issue:** The register schema requires `path::node` for closed entries; the plan verify runs `unittest` after replacing `/` and `.py`, which leaves `::` and fails to import. Existing C-01..C-08 use pytest node ids and are executed by a pytest meta-test; pytest is absent here.
- **Fix:** Accept `path.py.Class.method` in `_resolve_proof_test` and store C-09's `proof_test` in that form so both the register resolver and the plan's unittest invocation succeed. The named test exists and passes.
- **Files modified:** `pinn/conformance/register.py`, `pinn/conformance/divergence_register.json`
- **Verification:** `REGISTER-OK` / `PROOF-TEST-OK`; `load_divergence_register()` accepts C-09
- **Committed in:** `312f3080ab50e35be18ba87c9f0618866265b227` (Task 3)

---

**Total deviations:** 2 auto-fixed (2 Rule 1)
**Impact on plan:** Both were required for the stated Task 3 gates (phase40 zero failures; PROOF-TEST-OK). No recipe, threshold, or train-path change.

## Issues Encountered

- Pre-repair RED observed and recorded: `StageZeroUnderpopulated: Stage-0 population 50 < required 240` from `_run_validation` → `_stage_batch` → `select_stage_records`.
- Phase 47/48/49 under `unittest discover` fail at import with `ModuleNotFoundError: No module named 'pytest'` (phase47 2 errors, phase48 4 errors, phase49 7 errors). Pre-existing; pytest was not installed; not treated as a new failure.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for 50-05. Generation 3 must open at a head strictly after source identity `312f3080ab50e35be18ba87c9f0618866265b227`. `replay_count` is still 240. `final_band_generation` is still null. Do not start 50-03 until a band exists. 50-05 is `autonomous: false` and carries an owner checkpoint before the graded band.

## Validation Evidence

- Phase 50: 7 tests, OK
- Phase 40: 170 tests, OK (after wiring-spy retarget)
- Phase 41: 197 tests, OK
- TRACER-OK, GUARDS-OK, REGISTER-OK, PROOF-TEST-OK, PREREG-OK, LEDGER-SCAFFOLD-OK, TERMINAL-UNTOUCHED
- `selection_policy_sha256` recomputed equal to stored `c634aaac74aee5ef123b848bcb3816a09d90c5a9a24123adb598796ccef9873b`
- Four config hashes and `committed_config_set_sha256` re-derived from `git show HEAD:<path>` and `git show 312f3080:<path>` and matched
- No `227` constant introduced; `n_train`/`n_validation` stub defaults remain 240
- 50-01/50-02 PLAN.md and SUMMARY.md untouched

## Self-Check: PASSED

---
*Phase: 50-valid-stage-0-re-run*
*Completed: 2026-08-15*
