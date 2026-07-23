---
phase: 43-verification-stage-0-pilot-acceptance
plan: 03
subsystem: training-composition
tags: [config-seam, admitted-data, split-manifest, timing-calibration, preflight, ACC-02]
status: complete
requires:
  - 43-01 (pinn.verify fingerprint + atomic marker reuse)
  - pinn/data/{adapter,splits,batches}.py (DATA-01/04/05 pipeline)
  - pinn/training/{config,config_yaml,controllers,atomic_io}.py
provides:
  - "DataConfig source/root seam + run.smoke + stage.replay_count"
  - "CPU/fp32 admitted composition with frozen runs/<run>/splits.json"
  - "pinn.training.timing fail-closed fresh-launch calibration"
  - "RunController.s_per_step read-only EMA + replay_count threading"
  - "CTX-79-preserving data-reachability preflight"
affects:
  - 43-04 (launch >30-min gate consumes forecast_from_calibration)
  - 43-06 (Stage-0 smoke run uses configs/smoke.yaml)
  - 43-07 (pilot reuses admitted composition + splits.json)
tech-stack:
  added: []
  patterns:
    - "keyed-YAML optional section (data) with fail-loud unknown-key dotting"
    - "fail-closed fingerprinted artifact (mirrors pinn.verify marker)"
    - "replay-budget threading via the public DATA-05 pipeline (no bespoke loader)"
key-files:
  created:
    - pinn/training/timing.py
    - configs/smoke.yaml
    - tests/phase43/test_real_data_smoke_config.py
    - tests/phase43/test_timing_calibration.py
  modified:
    - pinn/training/config.py
    - pinn/training/config_yaml.py
    - pinn/train.py
    - pinn/training/controllers.py
key-decisions:
  - "replay_count threaded through RunController via the public DATA-05 functions (select_stage_records/sample_data_points/sample_collocation_points) rather than editing the non-owned batches.py; None delegates to build_stage_batch byte-for-byte"
  - "timing calibration reuses pinn.verify.current_fingerprint so a calibration and a verify marker certify the same runtime+code identity; forecast is s_per_step * requested_steps, fail-closed on every degraded record"
  - "data section is optional in keyed YAML (pre-43-03 configs default to the synthetic source); unknown data.* keys still fail loud"
requirements-completed: [ACC-02]
duration: ~2h
completed: 2026-07-21
coverage:
  - id: config-seam
    description: "Validated data.source/root, run.smoke, stage.replay_count on the frozen config + optional keyed-YAML data section."
    requirement: ACC-02
    verification:
      - kind: test
        ref: tests/phase43/test_real_data_smoke_config.py#ConfigSeamTests
        status: pass
      - kind: test
        ref: tests/phase43/test_real_data_smoke_config.py#SmokeYamlTests
        status: pass
    human_judgment: false
  - id: admitted-composition
    description: "CPU/fp32 AdmittedSetAdapter regardless of MPS model runtime; atomic runs/<run>/splits.json before batches; train/val StageIndex views only."
    requirement: ACC-02
    verification:
      - kind: test
        ref: tests/phase43/test_real_data_smoke_config.py#AdmittedCompositionTests
        status: pass
    human_judgment: false
  - id: replay-32-selection
    description: "The existing DATA-05 selector honors replay_count=32 and RunController threads it while an unset budget preserves the 240 population."
    requirement: ACC-02
    verification:
      - kind: test
        ref: tests/phase43/test_real_data_smoke_config.py#ReplayCountSelectionTests
        status: pass
    human_judgment: false
  - id: timing-calibration
    description: "Fail-closed fresh-launch calibration: valid record yields s_per_step*requested_steps; absent/malformed/non-finite/invalid/stale/mismatched/git-unavailable yield no forecast; writer refuses non-finite/non-positive."
    requirement: ACC-02
    verification:
      - kind: test
        ref: tests/phase43/test_timing_calibration.py#CalibrationForecastTests
        status: pass
      - kind: test
        ref: tests/phase43/test_timing_calibration.py#SPerStepPropertyTests
        status: pass
    human_judgment: false
  - id: data-reachability-preflight
    description: "CTX-79-preserving preflight refuses a missing/unresolvable corpus root before construction, naming both locked fallbacks; existing roots pass."
    requirement: ACC-02
    verification:
      - kind: test
        ref: tests/phase43/test_real_data_smoke_config.py#DataReachabilityPreflightTests
        status: pass
    human_judgment: false
---

# Phase 43 Plan 03: Real-Data Smoke Composition & Timing Inputs Summary

Built the real-data composition and persisted timing inputs that make the ACC-02
smoke, the evaluator, and the >30-minute launch gate executable — a validated
config seam, a CPU/fp32 admitted source with a frozen leakage-free split
manifest, a fail-closed fresh-launch timing calibration, and a CTX-79-preserving
data-reachability preflight — **without changing any data/model/loop mechanics**.

- **Duration:** ~2h · **Completed:** 2026-07-21
- **Tasks:** 3/3 · **Files:** 4 created, 4 modified · **Tests:** 33 (all pass)

## Accomplishments

### Task 1 — Config seam + admitted composition + replay budget
- Added a frozen `DataConfig` (`source` ∈ {synthetic, admitted}, optional `root`),
  `run.smoke: bool`, and `stage.replay_count: Optional[int]` (positive when set)
  to `pinn/training/config.py`. Registered `data` as an **optional** keyed-YAML
  section in `config_yaml.py` — pre-43-03 configs default to the synthetic source,
  and unknown `data.*` keys still fail loud with the dotted path.
- In `pinn.train`, `_build_admitted_sources` constructs `AdmittedSetAdapter` on
  **CPU/float32 regardless of the MPS model runtime** (the adapter owns fp32 CPU
  tensors; batches move to the model device at sampling time), creates or reloads
  a deterministic `SplitManifest`, **atomically writes `runs/<run>/splits.json`
  before any batch**, and returns only the train/validation `StageIndex` views.
- `RunController` gained an optional `replay_count`; `_stage_batch` threads it
  through the **existing public DATA-05 pipeline** so the smoke selects ~32 while
  an unset budget delegates to `build_stage_batch` byte-for-byte (Phase-40/41/42
  behavior preserved). Added `configs/smoke.yaml` (MPS/fp32 model, 300 Stage-0
  steps, `checkpoint_every=100`, `replay_count=32`, `run.smoke: true`).

### Task 2 — Fresh-launch timing calibration
- New `pinn/training/timing.py`: `write_calibration` / `read_calibration` /
  `forecast_from_calibration` / `timing_fingerprint`, writing a versioned
  `runs/.calibration/stage0-timing.json` bound to device, dtype, torch/Python
  version, and Git head (reusing `pinn.verify.current_fingerprint`). Exposed
  `RunController.s_per_step` (read-only EMA). On a terminal-success smoke,
  `pinn.train` writes the calibration **only** from a finite positive measurement;
  a diverged/partial/NaN smoke writes no valid calibration and a fresh launch
  finds no forecast rather than an invented one (SPEC edge R2). The reader returns
  `s_per_step * requested_steps`, fail-closed on absent/malformed/invalid/stale/
  fingerprint-mismatched/git-unavailable records.

### Task 3 — CTX-79-preserving data-reachability preflight
- Added `DataReachabilityError` + `_admitted_data_preflight`: an admitted run
  resolves its corpus root (explicit `data.root`, else `default_data_root()`) and
  refuses a missing/non-directory/unresolvable root **before** runtime resolve,
  network build, adapter scan, or optimizer — a fail-closed message naming **both**
  locked CTX-79 fallbacks (main-root checkout, or a gitignored read-only Stage-0
  copy with `data.root`). Wired early in `main()` plus a fail-closed wrap around
  source construction so a reachable-but-empty/incomplete corpus is a clean
  refusal, never a half-started or silently-synthetic run.

## Deviations from Plan

**[Rule 3 — Blocking / owned-paths constraint] `replay_count` threaded in
`controllers.py` instead of `batches.py`.**
- **Found during:** Task 1.
- **Issue:** The plan's `stage.replay_count` must reach `select_stage_records`
  (whose default is 240), but the natural site — `build_stage_batch` in
  `pinn/data/batches.py` — is **not** in this plan's `files_modified` / owned
  paths, and the SPEC prohibits changing the adapter/data policy or building a
  bespoke smoke loader.
- **Fix:** `RunController._stage_batch` threads `replay_count` through the SAME
  public DATA-05 functions `build_stage_batch` itself calls
  (`select_stage_records` → `sample_data_points` → `sample_collocation_points`),
  and delegates to the untouched `build_stage_batch` when `replay_count is None`.
  No `batches.py` edit; no algorithm change; legacy behavior byte-for-byte.
- **Files modified:** `pinn/training/controllers.py`.
- **Verification:** `ReplayCountSelectionTests` (32 threaded, 240 default) + all
  125 phase-40/41 controller/config tests green.
- **Commit:** f406c669.

**Total deviations:** 1 (owned-paths-driven design choice). **Impact:** none on
behavior; the change is additive and fully covered by tests. No architectural
(Rule 4) changes were required; no STOP-protocol gaps were hit (v2.0 is a build
milestone and this is greenfield code from ratified specs).

## Notes / Follow-ups (not blocking)

- `_HAS_DATASET` / `identity_coverage_check(has_dataset=...)` is left at its
  synthetic default; wiring dataset-identity coverage for an actual admitted
  **run** is 43-06's concern (this plan delivers composition + tests, not the
  run). The calibration write path is exercised by unit tests; its live firing
  is covered when 43-06 runs `configs/smoke.yaml`.
- The calibration records `full_stage0_steps = config.stage.max_epochs` as its
  recorded budget; the **authoritative** launch forecast recomputes
  `s_per_step * requested_steps` from the launch's own declared budget (43-04).

## Verification

Required command:

```
$ ~/miniforge3/envs/pinn-train/bin/python -m unittest \
    tests.phase43.test_real_data_smoke_config tests.phase43.test_timing_calibration -v
...
Ran 33 tests in 0.262s

OK
```

Regression (no breakage from the config/controllers/train changes):
- `tests/phase43` (full): **74 passed**
- `tests/phase41` controllers/config/train-entrypoint/resume/determinism: **186 passed** across runs
- `tests/phase42` (subprocess `pinn.train` launches): **passed, 0 failures/errors**

## Self-Check: PASSED
