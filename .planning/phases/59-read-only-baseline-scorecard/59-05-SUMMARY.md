---
phase: 59-read-only-baseline-scorecard
plan: 05
subsystem: verification
tags: [census, reader-acceptance, panel-rule, feas-02, gap-59-10]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Allowlisted reader, production reference trajectories, evidence writer and verifier, and the frozen scorecard
provides:
  - Stage-0 census functions and the frozen panel rule, tested on synthetic orbits and three real training systems
  - Reader acceptance against generation 7's resident monitor batch, committed as the audit area with the owner-accepted GAP-59-10 IC13 deviation
  - The Stage-0 difficulty census over 1,812 training and 227 validation systems, and the three singles, the 16-system family and the 227-system validation panel, committed as the census area
affects: [59-06, 59-07, 59-08, 59-09, 59-10, 60]

actuals:
  tokens: 176310
  tasks: 3
  commits: 12
plan_head_before: 0f100e4c3bf48cdbf88df03e5ccd98a9ab0632fa

tech-stack:
  added: []
  patterns:
    - "N_in is the gold-grid unwrap of the inner separation about the t=0 normal, clipped to t <= 10"
    - "Validation census rows keep every difficulty field empty; panels come only from the frozen rule"
    - "An owner-accepted deviation is a named block in the evidence record, and the independent verifier checks it against a ceiling it holds itself"

key-files:
  created:
    - pinn/verification/stage0_census.py
    - tests/phase59/test_census.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/audit/reader_acceptance.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/audit/summary.md
    - .planning/phases/59-read-only-baseline-scorecard/evidence/census/census.csv
    - .planning/phases/59-read-only-baseline-scorecard/evidence/census/census.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/census/summary.md
  modified:
    - tests/phase59/test_evidence_verifier.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py

key-decisions:
  - "GAP-59-10 says the acceptance records passed against the frozen value exactly as measured. This plan reads that as passed false beside the owner_accepted_deviation block, and the verifier requires that pairing."
  - "The verifier holds the ruled ceiling (2**-23) itself, so an edited record cannot raise it."
  - "The deviation applies only while the frozen value is still 1e-7 and the normalizer was recovered from the checkpoint inside 1e-6."
  - "FEAS-02 stays pending in REQUIREMENTS.md because Plans 59-03, 59-04, and 59-10 also declare it."

patterns-established:
  - "CensusHalt prints CENSUS-HALT, writes nothing, and exits 2"
  - "Every census and acceptance mode runs inline, ends with the runtime gate, and records its WALL-SECONDS"

requirements-completed: [FEAS-02]

coverage:
  - id: D1
    description: "Gold-grid revolution counts, gold-base agreement, and the frozen panel rule, with validation difficulty fields left empty"
    requirement: FEAS-02
    verification:
      - kind: unit
        ref: "tests/phase59/test_census.py#UnwrapTests,OuterRevolutionsTests,AssistedBaseTests,GoldBaseAgreementTests,PairTrackingTests,PanelRuleTests,PhaseAccuracyTests,ValidationRowTests,FreezeGuardCallTests"
        status: pass
      - kind: integration
        ref: "python -B -m pinn.verification.stage0_census --ids 1632,851,4658 --stdout"
        status: pass
    human_judgment: false
  - id: D2
    description: "The acceptance continues past an IC13 residual above the frozen 1e-7, up to exactly 2**-23, with the owner_accepted_deviation block, and the verifier accepts only that case"
    requirement: FEAS-02
    verification:
      - kind: unit
        ref: "tests/phase59/test_census.py#AcceptanceDeviationTests"
        status: pass
      - kind: unit
        ref: "tests/phase59/test_evidence_verifier.py#AuditDeviationTests"
        status: pass
    human_judgment: true
    rationale: "The ruling's wording 'records passed against the frozen value exactly as measured' was read as passed false. The owner should confirm that reading."
  - id: D3
    description: "Reader acceptance: the allowlisted reader reproduces generation 7's monitor batch (8,192 rows, 256 identities) and the checkpoint normalizer, committed as the audit area"
    requirement: FEAS-02
    verification:
      - kind: integration
        ref: "python -B -m pinn.verification.stage0_census --acceptance --check"
        status: pass
      - kind: integration
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py audit --skip-rederive --require-committed"
        status: pass
    human_judgment: false
  - id: D4
    description: "Difficulty census over 1,812 training and 227 validation systems and the three frozen-rule panels, committed as the census area"
    requirement: FEAS-02
    verification:
      - kind: integration
        ref: "python -B -m pinn.verification.stage0_census --check"
        status: pass
      - kind: integration
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py census --skip-rederive --require-committed"
        status: pass
    human_judgment: false

duration: 145min
completed: 2026-10-14
status: complete
---

# Phase 59 Plan 05: Stage-0 Census Summary

**The allowlisted reader matches generation 7's monitor batch (IC13 residual 2**-23 recorded as the owner-accepted GAP-59-10 deviation), and the frozen rule picks singles 1632, 851 and 4658 from the 1,812 Stage-0 training systems**

In plain language: before measuring how hard the Stage-0 target is, we proved our reader sees the same numbers the trainer saw. Targets, times and masses match bit for bit on all 8,192 monitor rows. The one soft spot is the normalized IC13 inputs, which differ from the trainer's by one float32 rounding step (2**-23, about 1.19e-07), a hair over the frozen 1e-07 bar. The owner accepted that as a recorded deviation with the bar unchanged. With the reader proven, we counted the inner laps for every Stage-0 training system and let the frozen rule choose the three single systems, the 16-system family and the validation panel. No held-out file was opened.

## Performance

- **Duration:** about 145 min in total. The first session ran about 90 min to the acceptance halt. This resume ran about 55 min (started 2026-10-15T02:40:00Z, finished 2026-10-15T03:40:00Z, approximate).
- **Tasks:** 3 of 3
- **Files:** 16 in the resume commits (4 code and test files, 12 evidence files), plus this summary, STATE.md and ROADMAP.md
- **Wall times (W1), every run under the 600 s budget, none took a launch slot:**

| Step | WALL-SECONDS |
|---|---|
| Tracer `--ids 1632,851,4658 --stdout` | 0.5377 first session, 0.5416 rerun on the final code |
| `--acceptance` | 2.6045 |
| `--acceptance --check` | 2.3750 |
| census (default mode) | 55.2034 |
| `--check` | 55.5000 |

The verifier's own commands, which re-derive through `--check`, took 3.77 s elapsed for `audit` and 57.58 s for `census`. The complete console output of each run is retained in the session scratchpad outside the repository.

## Accomplishments

- **Census and panels.** Median system makes 18.61 inner laps by t = 10 (10th percentile 10.47, 90th 39.35, range 2.82 to 101.74). A network must time those laps to about 1 part in 1,169 for a 10% end-point miss and 1 part in 11,692 for 1%. On the base grid 28 training systems have fewer than 2 samples per inner period, 148 fewer than 3, and 545 fewer than 5.
- **Panels, by the frozen rule only.** Singles at the 10th, 50th and 90th percentile of N_in: id 1632 (N_in 10.472, 11.94 base samples per period), id 851 (18.612, 6.72) and id 4658 (39.349, 3.18). Family of 16, one per bin of sizes 114 x 4 and 113 x 12, ids 3891, 4345, 1709, 4513, 1250, 3970, 2270, 4189, 3589, 2021, 1610, 367, 4056, 2777, 2303, 1383 (N_in 8.92 to 52.53). Validation panel: all 227 ids. The three singles are the research preview's ids and agree with it to 0.02%.
- **Checks that passed before any panel was chosen.** Pair tracking failures 0; gold-base maximum deviation 9.684781553938387e-07 against the 1e-6 limit; largest inner unwrap step 3.0733 rad, under pi; 18 training systems carry the base cross-check flag (the mean-motion-assisted base count differs from N_in by more than 2%).
- **Reader acceptance.** 8,192 rows and 256 identities with zero target, time and mass mismatches; normalizer recovered from `stage-0-init.pt` with residual 1.1920928955078125e-07 against the 1e-6 limit (no fallback); IC13 maximum difference 1.1920928955078125e-07, recorded as the GAP-59-10 deviation.
- **Read limits held.** Both areas report `test_split_opened` 0, `blocked_attempts` 0 and `refused_before_open` 0. The acceptance opened 512 training files; the census opened 3,624 training and 454 validation files. Validation rows have no difficulty numbers (D-40).
- **Re-derivable and ordered.** `--acceptance --check` printed AUDIT-CHECK-OK and `--check` printed CENSUS-CHECK-OK. After the commits, `verify_phase59_evidence.py audit` (AUDIT-DEVIATION line, then AUDIT-OK) and `census` (CENSUS-OK) pass with `--skip-rederive --require-committed`, and `scorecard-frozen` still prints SCORECARD-FROZEN-OK.

## Task Commits

1. **Task 1: Census rows, revolution counters and the panel rule (tracer)** - `f54eded0` (feat), first session. Gate re-run on the final code: the three tracer ids give N_in 10.471994, 18.612048 and 39.349227 (0.019%, 0.011% and 0.002% from the preview 10.47, 18.61, 39.35), pair tracking true, gold-base deviation at most 6.3e-10.
2. **Task 2: Reader acceptance on real data** - `81cc511d` (test, RED), `f77c3490` (feat, GREEN), `24f47296` (evidence, audit area).
3. **Task 3: Full census, panels and census evidence** - `af13a180` (evidence, census area).

**Plan metadata:** `1b31079c` (docs: the first-session halt record, now superseded by this summary) and the closeout commit that adds this summary, STATE.md and ROADMAP.md.

## Files Created/Modified

- `pinn/verification/stage0_census.py` - census, acceptance and panel rule; now carries the GAP-59-10 deviation
- `tests/phase59/test_census.py` - nine original classes plus `AcceptanceDeviationTests`
- `tests/phase59/test_evidence_verifier.py` - `AuditDeviationTests`
- `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` - audit check accepts the owner-accepted deviation only
- `.planning/phases/59-read-only-baseline-scorecard/evidence/audit/` - `reader_acceptance.json` (SHA-256 11a6cf7b...), `summary.md`, `files_opened.json`, `provenance.json`, `MANIFEST.json`
- `.planning/phases/59-read-only-baseline-scorecard/evidence/census/` - `census.csv` (f73c91b3...), `census.json` (cf68e32d...), `panels.json` (56ad5185...), `summary.md`, `files_opened.json`, `provenance.json`, `MANIFEST.json`

## Decisions Made

- The ruled ceiling lives in the verifier as a constant, not in the record. A record with a raised `accepted_ic13_max_abs`, a different date, another gap id, a moved `frozen_tolerance`, `passed` true, any mismatch, or a normalizer fallback is refused with a message naming the field.
- The producer applies the deviation only when the frozen value is still 1e-7 and the normalizer came from the checkpoint. If either changes, the run halts instead of reusing a ruling about a different situation.
- The audit summary sentence "Deviation is false" now reads "The normalizer fallback deviation is false", so it cannot be confused with the GAP-59-10 deviation printed just above it.

## Deviations from Plan

### Owner-instructed

**1. [Owner ruling GAP-59-10] The reader acceptance continues past the IC13 residual 2**-23**
- **Found during:** Task 2 (the first real acceptance run, in the first session)
- **Issue:** The monitor IC13 maximum, 1.1920928955078125e-07, is above the frozen `monitor_reproduction_ic13_abs` of 1e-7. The first session halted. The owner ruled option A on 2026-10-14: keep the frozen value, record a deviation, ceiling exactly 2**-23.
- **Fix:** `stage0_census --acceptance` records `passed` against the frozen value as measured (false) and an `owner_accepted_deviation` block (gap, frozen_tolerance, accepted_ic13_max_abs, resolved) instead of raising CensusHalt. The audit `summary.md` and `plain_language` say so in words. The verifier prints `AUDIT-DEVIATION` and accepts the case only on the conditions listed under Decisions Made. No DIAG-07 overlay module, scorecard file, `scorecard-freeze.json`, `59-CONTEXT.md` or `59-RESEARCH.md` was edited.
- **Files modified:** `pinn/verification/stage0_census.py`, `tests/phase59/test_census.py`, `tests/phase59/test_evidence_verifier.py`, and `evidence/verify_phase59_evidence.py`. The verifier file is outside this plan's original `files_modified`, as the ruling directed.
- **Verification:** RED first. Two census tests and the verifier's accepts-the-block test failed on assertions about the planned behavior, and the halting guards passed by design. After GREEN: 26 targeted tests, then 70 tests with the guard scans and the whole verifier module, then all 186 tests under `tests/phase59`.
- **Committed in:** `81cc511d` (RED), `f77c3490` (GREEN)
- **Plan criterion changed:** Task 2 asked for `passed true`. The record has `passed` false with the block, which is how this plan reads the ruling. If the owner meant `passed` true, change `passed` in `run_acceptance`, the matching rule in the verifier's `_check_ic13_deviation` and the tests that pin it, rerun `--acceptance` (3 s), rewrite the audit manifest and recommit. Nothing else reads it.

### Auto-fixed Issues (first session)

**2. [Rule 1 - Bug] Coarse-orbit test compares against the float just below pi**
- **Found during:** Task 1 (revolution counters)
- **Issue:** An exact half-turn sampled at 0.4 samples per turn makes `atan2` return 3.1415926535897927, one ulp under pi, so `>= pi` failed although the step is the alias bound.
- **Fix:** The test uses `np.nextafter(pi, 0)`. The counter is unchanged.
- **Files modified:** `tests/phase59/test_census.py`
- **Verification:** `tests.phase59.test_census` passes.
- **Committed in:** `f54eded0`

**3. [Rule 2 - Missing critical] Acceptance and census modes were written with the tracer**
- **Found during:** Task 1 (one CLI module)
- **Issue:** The freeze-guard test already calls those modes and the row builder is shared, so they could not honestly wait for Tasks 2 and 3.
- **Fix:** Both modes landed in the Task 1 module. Tasks 2 and 3 were still the first real runs.
- **Files modified:** `pinn/verification/stage0_census.py`
- **Verification:** Freeze-guard tests return non-zero before the reader is built; the real acceptance and census runs are described above.
- **Committed in:** `f54eded0`

---

**Total deviations:** 1 owner-instructed, 2 auto-fixed (1 bug, 1 missing critical)
**Impact on plan:** The test change does not move the alias bound. The owner-instructed deviation moved no frozen byte and widened nothing: the accepted case is one value, 2**-23.

### Process notes

- STATE.md and ROADMAP.md were edited by hand, as the 59-04 closeout did: the plan forbids gsd-tools state verbs and STATE.md is hand-maintained. ROADMAP changes only the Plans line (5/10) and the 59-05 checkbox. REQUIREMENTS.md is untouched.
- `commits: 12` is measured from the plan ledger. It counts six commits that are not 59-05's: five Plan 59-07 commits and the orchestrator's ruling commit `2ff434d4`, which landed between the halt and this resume. This plan's own commits are `f54eded0`, `1b31079c`, `81cc511d`, `f77c3490`, `24f47296`, `af13a180` and the closeout commit.
- `actuals.tokens` is chars/4 over the added lines of this plan's own files from the ledger base to the closeout, STATE.md excluded. Of the total, 147,472 tokens are the generated `census.csv`. The authored and small-evidence remainder is about 28,800.

## Issues Encountered

- **Near-limit values, all inside their frozen checks.** Gold-base maximum deviation is 96.8% of its 1e-6 limit, and the largest inner unwrap step is 97.8% of the pi alias bound. Both are worth a line on the findings page.
- **Untracked Plan 59-07 outputs.** `evidence/diag07/{jx10.json, files_opened_jx01_jx10.json, provenance_jx01_jx10.json, summary.md}` and the user-owned files listed in the repository git policy were not touched, staged or deleted. The launch lock was not used.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The census and the three panels are committed and verifiably later than the frozen scorecard. Plans 59-08 and 59-09 and Phase 60 read `census/panels.json` and `census/census.csv`; each should first run `verify_phase59_evidence.py census --skip-rederive --require-committed`.
- Plan 59-07 resumes next under the GAP-59-11 ruling (recorded in `59-GAPS.md`). Wave 4 (59-06, 59-08, 59-09) follows.
- FEAS-02 is not checked off in REQUIREMENTS.md; Plans 59-03, 59-04 and 59-10 also declare it.

## Self-Check: PASSED

All 14 created or changed evidence and code files exist; commits `f54eded0`, `1b31079c`, `81cc511d`, `f77c3490`, `24f47296` and `af13a180` exist; the Task 2 and Task 3 acceptance criteria were re-run programmatically (row counts, zero counts, panel distinctness, rule equality, no home paths) with every check passing, and the plan-level verification passed (186 tests under `tests/phase59`, the audit and census verifier tokens, `scorecard-frozen`).

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-14*
