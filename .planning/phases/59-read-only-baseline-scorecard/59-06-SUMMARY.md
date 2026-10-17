---
phase: 59-read-only-baseline-scorecard
plan: 06
subsystem: verification
tags: [feas-08, feas-09, survey, tau-l, predictability-envelope, stage-labels, diagnostic]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Frozen scorecard (survey_rules), allowlisted corpus doorway and production reference, the Stage-0 census helpers, and the evidence writer with the launch lock, memory preflight and completion marker
provides:
  - A unit-tested read-only survey tool (pinn/verification/dataset_survey.py) whose vectorized tau_L estimator equals a literal transcription of the spec snippet, with the frozen stage rule and pick rule
  - Committed survey evidence over all 12,023 training-split records with per-stage measures, the predictability envelope for Stages 4b and 6, and the difficulty ordering against the curriculum order
  - The FEAS-09 probe picks, standard/base/2279 (Stage 4b) and standard/base/3418 (Stage 6), with their sensitivity report
affects: [59-10, 60]

actuals:
  tokens: 0  # not measured: the plan ran across two sessions
  tasks: 3
  commits: 3
plan_head_before: ca1db001d34bbea293110561a7cc20acfc5fbfd2

tech-stack:
  added: []
  patterns:
    - "The survey reads every threshold and tau_L setting from the frozen survey_rules section and refuses a scorecard that says something it does not implement"
    - "Long survey steps run detached under the one-launch lock, after a 2 GiB vm_stat preflight, and are accepted only with survey.done.json written last"

key-files:
  created:
    - pinn/verification/dataset_survey.py
    - tests/phase59/test_survey.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/survey_records.csv
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/survey.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/picks.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/summary.md
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/files_opened.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/provenance.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/survey.done.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/survey/MANIFEST.json
  modified: []

key-decisions:
  - "Stage labels are diagnostic. Stages 0 and 1 come from the splits manifest, Stages 2 to 6 from the spec criteria in ascending precedence with Stage 6 the residual, and the official mapping stays owner-pending."
  - "The FEAS-09 picks are the pre-declared rule's output, nearest np.median with ties to the lowest id and then base before gold. Both picks change under each sensitivity window. That is reported and not acted on (D-20)."
  - "Task 3 cites the Task 2 detached --check (byte-identical, SURVEY-CHECK-OK, EXIT=0) instead of repeating it, because no input changed (expensive-validation rule). Plan 59-10's final check re-derives once more."

patterns-established:
  - "An evidence area is committed only after its detached run and detached --check both end with EXIT=0 and its completion marker verifies"

requirements-completed: []

coverage:
  - id: D1
    description: "tau_L estimator against the literal spec loop, degenerate fits, the half-pairs and window rules, the stage rule, the pick rule, Spearman, and the guard, lock and marker order"
    requirement: FEAS-08
    verification:
      - kind: unit
        ref: "tests/phase59/test_survey.py#TauLOracleTests,TauLDegenerateTests,HalfPairsTests,StageRuleTests,PickRuleTests,SpearmanTests,GuardOrderTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Committed survey over 12,023 training-split records, test split not opened, re-derived byte-identically by --check"
    requirement: FEAS-08
    verification:
      - kind: integration
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py survey --skip-rederive --require-committed"
        status: pass
    human_judgment: true
    rationale: "The verifier checks hashes, the freeze order and the open counts. What the envelope means for a per-system 1e-5 energy bar at Stages 4b and 6 is the judgment Plan 59-10 writes."
  - id: D3
    description: "FEAS-09 picks by the frozen median rule, with the sensitivity windows reported"
    requirement: FEAS-08
    verification:
      - kind: integration
        ref: ".planning/phases/59-read-only-baseline-scorecard/evidence/survey/picks.json"
        status: pass
    human_judgment: false

duration: 86min
completed: 2026-10-16
status: complete
---

# Phase 59 Plan 06: Read-Only Whole-Dataset Survey Summary

**All 12,023 training-split records were surveyed read-only. Stage 4b (654 records) has a median tau_L of 2.98, so a small starting error grows about 29-fold by t = 10. Stage 6 (269 records) has a median tau_L of 1.71, a 352-fold growth. The FEAS-09 probes are standard/base/2279 (Stage 4b) and standard/base/3418 (Stage 6). No test-split file was opened, and nothing gates on these labels.**

## In plain language

We looked at every later stage of the training data, without training anything, to see how hard each stage is. Stages 0 to 2 are the gentle hierarchical systems: a small error barely grows by t = 10 (about 1.1 to 1.2 times). Stage 4b grows such an error about 29 times and Stage 6 about 350 times, and their bodies come about twice as close as in Stages 0 to 2 (Stage 6 about five times as close), with peak accelerations about 6 to 34 times larger than Stage 0's. On three of the four measures that cover all seven non-empty stages, the difficulty order agrees well with the curriculum order (Spearman 0.89 to 0.93). Stage 3 is empty, because its virial-ratio window (0.9 to 1.1) is never reached by the standard base records, which span 0.0006 to 0.12. One record is unlabelled because its trajectory stops at t = 9.86, short of the 10-unit window. The two probe systems for Phase 60 were chosen by the frozen median rule. All of this is diagnostic: the official stage mapping and the tau_L method stay with the owner.

## Performance

- **Duration:** about 86 min (Task 1 and the Task 2 runs in the earlier session; Task 3 and closeout in this resume)
- **Started:** 2026-10-17T00:14Z (executor launch); resumed 2026-10-17T01:30Z
- **Completed:** 2026-10-17T01:40Z
- **Tasks:** 3 of 3
- **Files created:** 10 (2 code and test files, 8 evidence files)
- **Long runs (detached, one at a time, preflight bar unchanged at 2147483648 bytes):**

| Run | Started (UTC) | Exit | Elapsed | `ru_maxrss` | Note |
|---|---|---|---|---|---|
| Survey pass | 2026-10-17T00:41:31Z | 0 | 457.6 s | 507 MB | preflight 7.9 GB available; the committed files |
| Survey `--check` | after 00:49Z | 0 | about 8 min | n/a | SURVEY-CHECK-OK, byte-identical, wrote nothing |

- **Retained logs:** `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/beea9c78-634d-42db-a091-86fa23b14af1/scratchpad/59-06/survey.log` and `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/beea9c78-634d-42db-a091-86fa23b14af1/scratchpad/59-06/survey_check.log`. The in-repo copies under `evidence/survey/logs/` are git-ignored.
- **Broad test run:** `unittest discover -s tests/phase59 -p 'test_*.py'` at the final code state: 282 tests OK in 132.1 s, exit 0.

## Accomplishments

- **Population:** hierarchical base 3,886, hierarchical gold 3,886, standard base 2,199, standard gold 2,052 (total 12,023). `files_opened.json` shows 15,909 training opens, 0 validation opens, 0 test-split opens, 0 blocked attempts and 0 refusals before open.
- **Diagnostic stage counts:** 0 = 1,812; 1 = 2,074; 2 = 3,886; 3 = 0; 4a = 1,404; 4b = 654; 5 = 1,923; 6 = 269; unlabelled = 1.
- **Envelope at Stages 4b and 6 (medians, for Plan 59-10's plausibility reading):**

| Stage | n | tau_L | error growth e^{10/tau_L} | closest approach | acc_min | acc_max |
|---|---|---|---|---|---|---|
| 4b | 654 | 2.984 | 28.5 | 0.0170 | 4.40 | 3,504 |
| 6 | 269 | 1.706 | 351.6 | 0.00708 | 6.24 | 19,934 |

- **Difficulty ordering against the curriculum (Spearman):** tau_L 0.93, acc_max 0.89, closest approach 0.89, error growth 0.64 (seven stages each). N_in and phase accuracy cover only the three hierarchical stages (0.5 each).
- **Stage 3:** E25 = -9.740 and L75 = 0.0408 over the 2,199 standard base records. The count is 0 because no standard base record has a Q inside [0.9, 1.1].
- **FEAS-09 picks** (`picks.json`, both `formula_applicability`: "not applicable: no hierarchical split"):
  - Stage 4b: `standard/base/2279`, tau_L 2.984 (the stage median, 654 candidates). Window picks: 1 unit `standard/base/1916`, 2 units `standard/base/281`, 3 units `standard/base/73`. All differ from the primary pick.
  - Stage 6: `standard/base/3418`, t = 0 s_min 0.2657 (the median, 269 candidates). Window picks: 1 unit `standard/base/512`, 2 units `standard/base/1074`, 3 units `standard/base/509`. All differ.
- **Hashes:** `survey.json` `0e3295edff60c8e09c8e629b4b2a2d63a7e62d66d405e4c08db805120fa720a1`, `picks.json` `b6836d5095edc12b9b7af873bfd5b6cb82fdeeb2e5c34e1c75b608810cda7317`. MANIFEST.json pins every area file against freeze commit `4ea3b1bc` and produced_at_head `e858628a`.

## Task Commits

1. **Task 1: tracer (estimator, stage rule, pick rule, CLI, 78 tests)**: `e858628a` (feat). The commit body records the real 3-per-variant sample and a 200-per-variant smoke (792 records, no halt, 28 s, 354 MiB).
2. **Task 2: full survey and `--check`**: detached runs on the `e858628a` code, no code change. The result files are committed in Task 3's evidence commit.
3. **Task 3: manifest, verifier and commit-order check**: `04e17dac` (evidence).

**Plan metadata:** the docs commit that carries this summary.

## Files Created/Modified

- `pinn/verification/dataset_survey.py`: the read-only survey (tau_L estimator, stage and pick rules, per-stage measures, ordering, CLI with `--check`)
- `tests/phase59/test_survey.py`: the seven behavior classes, with the literal spec-loop oracle inside the test file only
- `.planning/phases/59-read-only-baseline-scorecard/evidence/survey/{survey_records.csv, survey.json, picks.json, summary.md, files_opened.json, provenance.json, survey.done.json, MANIFEST.json}`: the committed survey evidence

## Decisions Made

See `key-decisions` above.

## Deviations from Plan

None in this resume. The executor was cut off after both detached runs had finished cleanly and before Task 3. This session checked the Task 2 acceptance criteria against the files on disk, confirmed the code had not changed since `e858628a` (the producer hashes stay valid), and completed Task 3 as written. Nothing was re-run.

## Issues Encountered

- **The unlabelled record's reason shows numpy reprs.** `standard/base/3362` reads "record covers t = np.float64(0.0) to np.float64(9.859999999999998), not the whole window 0 to np.float64(10.0)". The content is correct (that trajectory ends at t = 9.86, so tau_L over [0, 10] is not computable, and the record is reported, not pushed into a stage). The wording is cosmetic. Changing it would change the producer hash and require a new run, so it was left as is.
- **Every sensitivity window moves both picks.** Plan 59-10 or the owner may want to note this when reading the probes. Under D-20 it is reported and not acted on.
- **`provenance.json` records `worktree_dirty: true`.** This comes from the owner's uncommitted files (`.planning/config.json`, the v2.2 design brief), not from this plan's paths.

## Authentication Gates

None.

## Known Stubs

None.

## Threat Flags

None. All reads go through the allowlist and the attestation; no new endpoint or file-access pattern.

## User Setup Required

None.

## Next Phase Readiness

- The launch lock is free. 59-08 (two-Kepler formula) and 59-09 (JX-2 to JX-5, 6 GiB bar) remain in Wave 4.
- FEAS-08 stays pending in `REQUIREMENTS.md`. Plans 59-03 and 59-10 also declare it, and Plan 59-10's final check re-derives the survey once more.
- Plan 59-10 quotes the Stage 4b and Stage 6 envelope above for its plausibility reading of a per-system 1e-5 energy bar. It must label that reading as a judgment.

## Self-Check: PASSED

The two code and test files and the eight evidence files exist; commits `e858628a` and `04e17dac` exist. The Task 2 verify chain printed SURVEY-MARKER-OK (both logs end EXIT=0, SURVEY-CHECK-OK present). `verify_phase59_evidence.py manifest --area survey --write` printed MANIFEST-SURVEY-OK, `survey --skip-rederive` printed SURVEY-OK before the commit, `scorecard-frozen` printed SCORECARD-FROZEN-OK, and `survey --skip-rederive --require-committed` printed SURVEY-OK after it. The 282-test Phase 59 suite passes.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-16*
