---
phase: 43-verification-stage-0-pilot-acceptance
plan: 07
subsystem: verification-acceptance
tags: [acc-05, pilot, seed-band, r-1, r-2, owner-ratification, config]
status: complete
requires:
  - phase: 43-06
    provides: "Real ACC-02 smoke evidence plus owner-ratified B-5, R-1 loss ceiling, and D4-a checkpoint ceiling"
provides:
  - "Validated run.recover_retries YAML seam wired exactly into CurriculumController"
  - "Three-seed real admitted-data Stage-0 pilot evidence with raw losses, validation, memory, timing, artifact hashes, and transparent spread calculations"
  - "Owner-ratified R-1/R-2 values persisted exactly in configs/stage0-example.yaml with dated sign-off"
affects: [43-08, milestone-acceptance, training-guardrails]
tech-stack:
  added: []
  patterns:
    - "Owner-owned operational values travel through a validated config seam and are never replaced by an implicit controller literal"
    - "Calibration evidence retains every seed and derives candidates from raw observations before owner ratification"
key-files:
  created:
    - .planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md
    - .planning/phases/43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md
    - tests/phase43/test_pilot_calibration.py
  modified:
    - configs/stage0-example.yaml
    - pinn/training/config.py
    - pinn/training/config_yaml.py
    - pinn/train.py
key-decisions:
  - "R-1/R-2 owner ratification (2026-07-22): loss_explosion_ceiling=100000000000.0, disk_floor_fraction=0.05, memory_watermark_fraction=0.7, recover_retries=0; persist without rounding, reinterpretation, or substitution."
  - "Three completed seeds provide HIGH calibration confidence while not establishing convergence: final validation relative span is 3.8224247683129153 and two seeds ended with worsening validation trends."
patterns-established:
  - "Pilot calibration records raw per-seed artifacts and exact spread math alongside candidate-to-observation references."
  - "Superseded checkpoint state remains auditable while current status and supported config are unambiguously owner-ratified."
requirements-completed: [ACC-05]
coverage:
  - id: D1
    description: "run.recover_retries accepts only non-negative integers, round-trips through YAML, and is handed to CurriculumController without a literal bypass."
    requirement: ACC-05
    verification:
      - kind: unit
        ref: "tests.phase43.test_pilot_calibration.RecoverRetryConfigTests and TrainRecoverRetryHandoffTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Three real admitted-data seeds are retained in the pilot record with complete artifacts, raw observations, seed-band spread, and explicit confidence handling for divergence/fewer-than-two completions."
    requirement: ACC-05
    verification:
      - kind: unit
        ref: "tests.phase43.test_pilot_calibration.PilotCalibrationEvidenceTests"
        status: pass
      - kind: other
        ref: ".planning/phases/43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md#phase43-pilot-schema"
        status: pass
    human_judgment: false
  - id: D3
    description: "The exact owner-provided R-1/R-2 values are active in supported Stage-0 config and the calibration record carries the dated owner sign-off."
    requirement: ACC-05
    verification:
      - kind: integration
        ref: "python -c config load/assert for loss_explosion_ceiling=100000000000.0, disk_floor_fraction=0.05, memory_watermark_fraction=0.7, recover_retries=0"
        status: pass
      - kind: manual_procedural
        ref: "Owner response at Plan 43-07 Task 3 checkpoint, recorded in 43-CALIBRATION.md on 2026-07-22"
        status: pass
    human_judgment: false
duration: 40min (includes blocking owner-decision continuation)
completed: 2026-07-22
---

# Phase 43 Plan 07: Stage-0 Pilot Calibration and R-1/R-2 Ratification Summary

**Three real admitted-data Stage-0 seeds produced a traceable calibration band, and the owner ratified the exact supported guard/recovery configuration: `100000000000.0`, `0.05`, `0.7`, and `0`.**

## Performance

- **Duration:** ~40 min end to end (includes the blocking Task 3 owner-decision continuation)
- **Started:** 2026-07-22T07:50:37Z
- **Completed:** 2026-07-22T08:30:24Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Exposed the existing recovery budget through validated `run.recover_retries` YAML/config plumbing and proved `pinn.train` passes that exact value to `CurriculumController` without a hidden literal.
- Ran and retained three real Stage-0 pilot seeds (41, 42, 43), each completing 300/300 finite steps, with raw final/peak losses, validation trend, MPS memory, wall-clock, timing EMA, checkpoint inventory, and SHA-256 evidence identities.
- Recorded transparent absolute/relative spread calculations and HIGH calibration confidence while explicitly preserving the non-convergence warning: final validation relative span was `3.8224247683129153`, with two worsening trends.
- Persisted the owner's exact R-1/R-2 values in `configs/stage0-example.yaml` and recorded dated owner sign-off in `43-CALIBRATION.md` without rounding, reinterpretation, or substitution.

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Add failing recover-retry config tests** — `27513a0e` (test)
2. **Task 1 GREEN: Expose the validated recover-retry config seam** — `ae250c77` (feat)
3. **Task 2: Record real three-seed pilot calibration evidence** — `371edbf1` (evidence)
4. **Task 3: Ratify pilot guard and recovery values** — `370b0216` (evidence)

**Plan metadata:** (this commit) — `docs(43-07): complete stage-0 pilot calibration plan`

## Files Created/Modified

- `pinn/training/config.py` — validates non-negative integer `run.recover_retries` and exposes it in resolved config/provisional-field reporting.
- `pinn/training/config_yaml.py` — documents the generic dataclass mapping used by the recovery seam.
- `pinn/train.py` — passes `config.run.recover_retries` directly to `CurriculumController`.
- `configs/stage0-example.yaml` — active owner-ratified R-1/R-2 values alongside the existing D4-a ceiling.
- `.planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md` — raw observations, exact spread math, candidate traceability, confidence limits, and dated owner ratification.
- `.planning/phases/43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md` — machine-readable `phase43-pilot/v1` evidence with artifact hashes for seeds 41–43.
- `tests/phase43/test_pilot_calibration.py` — config validation/handoff tests plus fixture-driven evidence, divergence-retention, and low-confidence tests.

## Decisions Made

- **R-1/R-2 (owner, 2026-07-22):** `loss_explosion_ceiling = 100000000000.0`, `disk_floor_fraction = 0.05`, `memory_watermark_fraction = 0.7`, and `recover_retries = 0`. These are the exact owner-provided values; the executor made no numerical choice.
- **Calibration interpretation:** Three completed seeds satisfy the plan's HIGH-confidence rule for an operational band, but the evidence is not a convergence claim. The large validation spread and two worsening trends remain inputs to Plan 43-08's evidence-grounded verdict.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The blocking owner-decision checkpoint was resolved by the exact 2026-07-22 owner response.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- ACC-05 is complete: the pilot band, confidence limits, candidates, exact owner ratification, and executable supported config are all recorded.
- Plan 43-08 may consume the seed band and owner-ratified thresholds when preparing the go/adjust/rethink evidence package.
- This plan does not start 43-08, render ACC-06, verify Phase 43, or close milestone v2.0.

## Known Stubs

- `pinn/training/config.py:121,131,135-136,213-215` retains legacy `PROVISIONAL` names/comments for D4-a and the disk/memory defaults. These labels are reporting metadata, not the supported Plan 43-07 configuration: `configs/stage0-example.yaml` explicitly supplies the owner-ratified values, and config-load assertions prove those exact values win. Renaming the shared historical constants/reporting registry is outside this plan and does not block ACC-05.

## Self-Check: PASSED

- All seven plan files exist on disk.
- Commits `27513a0e`, `ae250c77`, `371edbf1`, and `370b0216` exist in git history.
- `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_pilot_calibration -v` — 9/9 pass.
- `load_config('configs/stage0-example.yaml')` returns the exact owner values `100000000000.0`, `0.05`, `0.7`, and `0`.
- No new network endpoint, auth path, file-access trust boundary, or schema mutation was introduced beyond the plan's covered config/evidence boundary.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-22*
