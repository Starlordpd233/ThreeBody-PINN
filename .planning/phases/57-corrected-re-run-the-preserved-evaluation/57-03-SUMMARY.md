---
phase: 57-corrected-re-run-the-preserved-evaluation
plan: "03"
subsystem: training
tags: [pytorch, configuration, checkpoint, lbfgs, invariant-b, r-ref, stage-0]

requires:
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: "57-02's amended 4096-row production path, frozen R_ref normalization, and telemetry"
  - phase: 56-contract-amendment-train-free-gate
    provides: "The governed phase56-r-ref-stage0/v1 artifact schema and frozen-reference contract"
provides:
  - "Strict Phase-57 run construction for exact 4096-row physics batches and one provenance-checked R_ref artifact"
  - "One training-only frozen invariant-B monitor plus hash-validated L-BFGS segment samples/weights across checkpoint resume"
  - "Seed-42 calibration smoke and seed-41/42/43 graded configs with machine-derived comparability delta"
affects: [57-04, 57-05, RUN-04, RUN-05]

actuals:
  tokens: 17583
  tasks: 3
  commits: 4
plan_head_before: 47ff3418add8fb18d6e0a79b7aefb90f72ec6874
commits: 4

tech-stack:
  added: []
  patterns:
    - "Amended recipe fields are an explicit config opt-in; run construction fails closed on any partial opt-in, reduced count, or invalid R_ref artifact."
    - "Checkpoint freeze state uses weights-only-safe tensors/primitives with identity, tensor, sample, and weight hashes checked before restore."
    - "Invariant-B consumes a single training-only monitor snapshot while front_advance_window_n remains an independent accepted-step deadline."

key-files:
  created:
    - configs/stage0-v23-smoke.yaml
    - configs/stage0-v23-seed41.yaml
    - configs/stage0-v23-seed42.yaml
    - configs/stage0-v23-seed43.yaml
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/57-CONFIG-DELTA.md
  modified:
    - pinn/training/config.py
    - pinn/train.py
    - pinn/loss_catalog.py
    - pinn/training/controllers.py
    - pinn/training/checkpoint.py
    - pinn/training/run_metadata.py

key-decisions:
  - "Pre-Phase-57 configs remain backward-compatible; only configs that explicitly bind collocation_count and r_ref_artifact_path enter the strict amended path."
  - "The v2.3 smoke and graded runs use the full 240-row replay pool so the seed-42 smoke and graded split inputs are identical under the ratified 4096-row allocation."
  - "The monitor and active L-BFGS segment are persisted as separate checkpoint surfaces from invariant_b_state; missing or hash-mismatched amended state refuses resume rather than redrawing."

requirements-completed: [RUN-04, RUN-05]

coverage:
  - id: D1
    description: "Strict amended config construction binds exactly 4096 physics rows and a validated frozen R_ref artifact."
    requirement: RUN-04
    verification:
      - kind: unit
        ref: "tests.phase57.test_runtime_freeze.ConfigProtocolTests + tests.phase57.test_recipe_production_path.ProductionPathContractTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "One training-only monitor and immutable L-BFGS sample/weight state survive checkpoint serialization and restore."
    requirement: RUN-04
    verification:
      - kind: unit
        ref: "tests.phase57.test_runtime_freeze.MonitorContractTests, WindowContractTests, LbfgsFreezeTests"
        status: pass
      - kind: unit
        ref: "tests.phase41.test_controllers_ext (22/22)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Smoke and three graded configs encode the corrected recipe and only approved seed/name/budget/operational differences."
    requirement: RUN-05
    verification:
      - kind: unit
        ref: "tests.phase57.test_runtime_freeze.ConfigProtocolTests + tests.phase50.test_validation_full_pool.ValidationFullPoolTests (11/11)"
        status: pass
      - kind: other
        ref: "strict-load of all four configs and governed R_ref artifact under pinn-train"
        status: pass
    human_judgment: false

duration: 45min
completed: 2026-09-08
status: complete
---

# Phase 57 Plan 03: Runtime Freeze and Derived Config Summary

**Strict 4096-row/R_ref launch binding, hash-validated monitor and L-BFGS resume state, and a comparable v2.3 smoke/three-seed config band are now committed.**

## Performance

- **Duration:** approximately 45 minutes
- **Started:** 2026-09-08 (execution session)
- **Completed:** 2026-09-08
- **Tasks:** 3/3
- **Files modified:** 11 (including 5 created artifacts)

## Accomplishments

- Added frozen-recipe configuration fields and a single-read `phase56-r-ref-stage0/v1` artifact validator. Corrected configs cannot lower the 4096-row count, omit the artifact, or bypass normalization; legacy callers without the opt-in remain compatible.
- Added a dedicated training-only monitor state with 4096-row/16-bin provenance and a serialized L-BFGS segment carrying fixed samples, detached weights, counters, and hashes. Checkpoint restore validates all state before re-entry and refuses incomplete amended state.
- Added `stage0-v23-smoke.yaml` (seed 42) and `stage0-v23-seed{41,42,43}.yaml` with distinct run names, 240-row replay pools, N=500, and the corrected R_ref path. `57-CONFIG-DELTA.md` records recursive YAML differences generated from the predecessor and final configs.

## Task Commits

Each task was committed atomically:

1. **Task 1: Bind strict 4096-row and frozen-R_ref runtime configuration** — `96d9a9a3` (`feat(57-03)`)
2. **Task 2: Persist one monitor and immutable L-BFGS segment state** — `ac53a5e6` (`feat(57-03)`)
3. **Task 3: Derive the final smoke and three graded configs** — `b671e4ad` (`feat(57-03)`)

The post-summary resume-safety correction is `2ddd89ef` (`fix(57-03)`).

## Validation Evidence

- `python -m unittest tests.phase57.test_runtime_freeze tests.phase57.test_recipe_production_path tests.phase50.test_causal_telemetry tests.phase50.test_validation_full_pool tests.phase41.test_controllers_ext -v` — **56/56 passed**.
- `python -m unittest tests.phase57.test_runtime_freeze.ConfigProtocolTests tests.phase57.test_recipe_production_path.ProductionPathContractTests -v` — **6/6 passed**.
- `python -m unittest tests.phase57.test_runtime_freeze.MonitorContractTests tests.phase57.test_runtime_freeze.WindowContractTests tests.phase57.test_runtime_freeze.LbfgsFreezeTests tests.phase50.test_causal_telemetry.CausalTelemetryOwnershipTests -v` — **11/11 passed**.
- `python -m unittest tests.phase57.test_runtime_freeze.ConfigProtocolTests tests.phase50.test_validation_full_pool.ValidationFullPoolTests -v` — **11/11 passed**.
- Strict-loaded all four final configs and `pinn/verification/artifacts/r_ref_stage0.json`; R_ref validated as `19749775821.24417`.
- `python -m compileall -q` over all modified Python modules — passed.

The complete `tests/phase57` discovery currently reports 15 failures and 4 errors in the later Plan 57-04 GATE-04/evaluation-boundary/candidate contracts; those files and artifacts are intentionally not part of this plan. Two optional adjacent modules use pytest, which is intentionally absent from the mandated `pinn-train` environment, so they were not run there.

## Decisions Made

- The new recipe is opt-in at the config boundary to preserve the established small synthetic/unit-test path while making every v2.3 launch explicit and fail-closed.
- The smoke materializes the same 240-row Stage-0 replay pool as the graded configs; this is required for the later byte-identical seed-42 split cross-check and is recorded in the config delta.
- Monitor state is independent from `invariant_b_state`, and the L-BFGS segment state remains active through interruption/resume paths; only a completed segment clears its active state.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] Added frozen-weight support to the causal loss**

- **Found during:** Task 2
- **Issue:** The planned L-BFGS contract supplied `frozen_weights`, but `causal_physics_loss` had no parameter and would recompute weights from every trial residual.
- **Fix:** Added a validated detached `frozen_weights` path that keeps trial residual gradients live while skipping prefix/weight recomputation.
- **Files modified:** `pinn/loss_catalog.py`
- **Verification:** `LbfgsFreezeTests` and the Phase-50 causal telemetry tests passed.
- **Committed in:** `ac53a5e6`

**2. [Rule 2 - Missing critical functionality] Added the required smoke/graded metadata consistency helper**

- **Found during:** Task 3
- **Issue:** The task contract required a byte-identical `splits.json` and exact `s_h`/`n_train` assertion, but `run_metadata.py` exposed no helper.
- **Fix:** Added `assert_smoke_matches_graded` with persisted-byte/path extraction and fail-closed scalar checks.
- **Files modified:** `pinn/training/run_metadata.py`
- **Verification:** ConfigProtocolTests passed and a direct equal-metadata probe returned `True`.
- **Committed in:** `b671e4ad`

**3. [Rule 2 - Required recipe compatibility] Set the final configs' replay pool to 240**

- **Found during:** Task 3
- **Issue:** The predecessor smoke used 32 replay identities, which has no ratified 4096-row replay-only allocation and could not produce a split matching graded seed 42.
- **Fix:** All four final configs use the full 240-row Stage-0 replay pool while preserving the predecessor values elsewhere.
- **Files modified:** `configs/stage0-v23-*.yaml`, `57-CONFIG-DELTA.md`
- **Verification:** Strict config/validation tests passed; the machine-derived delta records the change.
- **Committed in:** `b671e4ad`

**4. [Rule 3 - Blocking bookkeeping] Repaired the legacy STATE.md position for current GSD tooling**

- **Found during:** State/roadmap updates
- **Issue:** `state.advance-plan` could not parse the existing prose-only plan position, and after the parser-compatible label was added it recalculated the milestone phase count/percentage from an incomplete view of archived summaries.
- **Fix:** Added the parser-required labeled position, ran the available state/roadmap handlers, then restored disk-derived `completed_phases: 4`, `completed_plans: 27`, `percent: 90`, and the Plan-57-04 resume pointer while preserving the valid Plan-57-03 metric entry.
- **Files modified:** `.planning/STATE.md`
- **Verification:** Summary/commit self-check passed; roadmap reports 3/6 Phase-57 plans complete and the state frontmatter matches the on-disk summary count.
- **Committed in:** final metadata commit

**5. [Rule 1 - Resume-safety bug] Reject incomplete amended runtime state**

- **Found during:** post-summary checkpoint audit
- **Issue:** An amended controller could accept a checkpoint missing the new monitor/segment keys and retain freshly constructed state instead of refusing resume.
- **Fix:** Require both additive keys for amended resumes and validate the persisted segment counters before rebuilding its carrier.
- **Files modified:** `pinn/training/controllers.py`
- **Verification:** The 56-test focused suite passed after the fix.
- **Committed in:** `2ddd89ef`

**Total deviations:** 5 auto-fixed (Rules 1–3)
**Impact on plan:** Each addition was required by an explicit task behavior or by the ratified 4096-row allocation; no scientific value was retuned and no run/evaluation was launched.

## TDD Gate Compliance

The task markers are `tdd="true"`, but this checkout has `workflow.tdd_mode: false`. The intentional RED contracts were already committed by Plan 57-01, and this plan reused those tests before each implementation slice; no test files needed modification. The focused GREEN verifications above pass. No separate RED evidence file was generated because the canonical checker expects Node/TAP output while these mandated tests are stdlib `unittest`.

## Issues Encountered

- The full Phase-57 discovery remains red only at later-wave contracts (GATE-04 condition-ii implementation, canonical evaluator boundary, and candidate eligibility), which are the next plan's scope.
- `tests.phase48.test_gradient_observability` and `tests.phase49.test_gate03_resume` import pytest; the required `pinn-train` environment intentionally has no pytest, so no dependency was installed or changed.
- Existing unrelated dirty/untracked files remain untouched in the worktree.

## User Setup Required

None — no external service or credential configuration is required.

## Next Phase Readiness

Plan 57-04 can proceed. The run path now binds exact collocation/R_ref configuration, preserves the invariant-B monitor and L-BFGS segment across resume, and provides the final v2.3 config band/delta. RUN-04 remains blocked until Plan 57-04's separate production verification and a fresh complete GATE-04 PASS; no smoke, graded run, or held-out evaluation was started.

---
*Phase: 57-corrected-re-run-the-preserved-evaluation*
*Completed: 2026-09-08*

## Self-Check: PASSED

- Summary and all five Task-3 artifacts exist.
- Task commits `96d9a9a3`, `ac53a5e6`, `b671e4ad`, and resume-safety fix `2ddd89ef` are present in git history.
- `git diff --check` reports no whitespace errors.
