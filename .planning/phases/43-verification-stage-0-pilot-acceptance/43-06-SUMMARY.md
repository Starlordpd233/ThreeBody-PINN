---
phase: 43-verification-stage-0-pilot-acceptance
plan: 06
subsystem: verification-acceptance
tags: [acc-02, smoke, d4-a, r-1, b-5, honesty, owner-ratification]
status: complete
requires:
  - phase: 43-01
    provides: "verify ladder, verdict marker, and tests/phase43 scaffold"
  - phase: 43-03
    provides: "real-data _SOURCE_FACTORY wiring, s_per_step accessor/forecast, and configs/smoke.yaml"
  - phase: 43-04
    provides: "duration gate reading the fresh-green verify marker before launch"
provides:
  - "Owner-ratified B-5 RESUME_FIELD_REGISTRY disposition (ratify-current, unchanged)"
  - "Real ordinary ACC-02 smoke run over the real admitted corpus: 300/300 gap-free steps, 32 identities, checkpoints 100/158/200/300, one SIGTERM interrupt + --resume latest to finished"
  - "Owner-ratified R-1 loss_explosion_ceiling = 1e11 (via delegation), revisable at ACC-05"
  - "Owner-ratified D4-a wall_clock_ceiling_s = 120 (explicit selection), persisted in configs/stage0-example.yaml"
  - "data.blacklist_path config seam threaded through DataConfig / pinn.train / AdmittedSetAdapter"
affects: [43-07, 43-08, milestone-acceptance]
tech-stack:
  added: []
  patterns:
    - "Honest fail-closed evidence recording: a refused/interrupted run names its disposition and leaves metrics null, never fabricated (SPEC R2)"
    - "Owner-carved seams (B-5, R-1, D4-a) surfaced as evidence; the agent never self-ratifies a value"
key-files:
  created:
    - tests/phase43/test_smoke.py
    - tests/phase43/test_real_data_smoke_config.py
  modified:
    - configs/smoke.yaml
    - configs/stage0-example.yaml
    - pinn/train.py
    - pinn/training/config.py
    - .planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md
key-decisions:
  - "B-5: owner ratified RESUME_FIELD_REGISTRY as-is, unchanged (2026-07-21)."
  - "R-1: owner delegated loss_explosion_ceiling to best judgement; ratified at 1e11, calibrated from the diagnostic run's ~4e9 observed peak (~25x headroom); explicitly revisable at ACC-05 (2026-07-21)."
  - "D4-a: owner explicitly selected wall_clock_ceiling_s = 120 s from presented options (not delegated) — ~10x the measured ~9-12 s normal inter-checkpoint interval, well under the ~270-305 s production forecast, bounding a stall to <=2 min (2026-07-21)."
  - "rolling_keep bumped 3->4 in configs/smoke.yaml (Rule 3 operational auto-fix, not an owner-carved seam) after Attempt 1 evicted checkpoint 100 under one off-cadence interrupt."
requirements-completed: [ACC-02]
coverage:
  - id: D1
    description: "The real ordinary train smoke (python -m pinn.train --config configs/smoke.yaml, no bespoke harness) runs 32 admitted trajectories / 300 steps over the real corpus, produces checkpoints 100/200/300, survives one SIGTERM interrupt plus --resume latest to finished, and records measured s_per_step + persisted timing forecast."
    requirement: ACC-02
    verification:
      - kind: unit
        ref: "tests/phase43/test_smoke.py::RealSmokeArtifactTests"
        status: pass
      - kind: integration
        ref: "tests/phase43/test_real_data_smoke_config.py::BlacklistPathResolutionTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "B-5 (RESUME_FIELD_REGISTRY) and D4-a (wall_clock_ceiling_s) are owner-ratified, not agent-selected, and persist at their exact owner-approved targets."
    requirement: ACC-02
    verification:
      - kind: unit
        ref: "tests.phase41.test_resume (30/30, registry unchanged)"
        status: pass
      - kind: other
        ref: "python -c \"from pinn.training.config_yaml import load_config; assert float(load_config('configs/stage0-example.yaml').run.checkpoint.wall_clock_ceiling_s) == 120.0\""
        status: pass
    human_judgment: false
  - id: D3
    description: "The Stage-0 smoke's loss is bounded but non-descending within the 300-step Adam budget — recorded honestly as an ACC-05 pilot watch-item, never presented as convergence."
    verification: []
    human_judgment: true
    rationale: "Whether this non-descending pattern resolves with a longer curriculum/budget is an open scientific question for the ACC-05 Stage-0 pilot, not something this plan's mechanical smoke can adjudicate."
duration: 3h11m (includes two owner-decision pauses: B-5 Task 1, D4-a Task 3)
completed: 2026-07-22
status: complete
---

# Phase 43 Plan 06: Real ACC-02 Smoke + B-5/D4-a Owner Ratification Summary

**Real ordinary Stage-0 smoke over the actual admitted corpus (32 trajectories, 300 gap-free steps, checkpoints 100/158/200/300, one SIGTERM interrupt + resume to finished, s_per_step≈0.1157) with B-5, R-1, and D4-a all owner-ratified — B-5 and R-1 via explicit instruction/delegation earlier in the plan, D4-a (wall_clock_ceiling_s=120) via the owner's explicit selection that resolved this continuation's blocking checkpoint.**

## Performance

- **Duration:** ~3h 11min end to end (includes two blocking owner-decision pauses — Task 1's B-5 checkpoint and Task 3's D4-a checkpoint — not continuous agent work)
- **Started:** 2026-07-21T20:23:24-07:00 (Task 1 commit)
- **Completed:** 2026-07-21T23:34:51-07:00 (Task 3 evidence commit)
- **Tasks:** 3 (Task 1: B-5 checkpoint; Task 2: execute + record real smoke; Task 3: D4-a checkpoint)
- **Files modified:** 7 (`configs/smoke.yaml`, `configs/stage0-example.yaml`, `pinn/train.py`, `pinn/training/config.py`, `tests/phase43/test_smoke.py`, `tests/phase43/test_real_data_smoke_config.py`, evidence README)

## Accomplishments

- **Task 1 (B-5):** Owner ratified `RESUME_FIELD_REGISTRY` as-is, unchanged (`ratify-current`, 2026-07-21). 34-field registry (27 IDENTITY + 7 OPERATIONAL) recorded in evidence with full disposition; `tests.phase41.test_resume` 30/30 unchanged.
- **Task 2 (real ACC-02 smoke):** Ran the ordinary `python -m pinn.train --config configs/smoke.yaml` against the real admitted corpus. First honestly failed closed on a genuine pre-existing wiring gap (DI-43-06-01: blacklist path never threaded through `DataConfig`/`_build_admitted_sources`); fixed under owner authorization (Option A: legacy Documentation blacklist designated authoritative). Re-run then surfaced a second genuine finding (DI-43-06-02: the provisional 1e6 `loss_explosion_ceiling` trips against real-corpus raw physics-residual scale at step 2); an owner-authorized diagnostic (guard temporarily lifted, non-committed) established the loss stays finite/bounded but non-descending across 300 steps, informing the owner's R-1 delegation to 1e11. The accepted acceptance run (Attempt 2, after a Rule-3 `rolling_keep` 3→4 bump) is the plan's evidentiary basis: 300/300 unique gap-free steps, checkpoints 100/158/200/300 all present, `s_per_step=0.11570`, forecast `34.71 s`, R-1 headroom ~21.7x, zero non-finite steps.
- **Task 3 (D4-a, this continuation):** Owner explicitly selected `wall_clock_ceiling_s = 120` from presented options (measured ~9-12 s normal interval, ~270-305 s production forecast, prior 3600 s template placeholder). Persisted in `configs/stage0-example.yaml`'s active `run.checkpoint` mapping; the stale commented guard example (`loss_explosion_ceiling: 1.0e6`) was also fixed to `1.0e11` per owner authorization in the same edit, with an honest comment recording R-1's 2026-07-21 ratification and revisability at ACC-05.
- Activated `tests/phase43/test_smoke.py::RealSmokeArtifactTests` (skip-to-green; no source edit needed) — 9/9 pass, 0 skips. Full `tests/phase43` discovery sweep: 160/160 pass.

## Task Commits

Task 1 (B-5 checkpoint):
1. **Task 1: Owner ratifies B-5 before the first real run** — `8c36b790` (evidence)

Task 2 (execute + record the real smoke — multiple sub-attempts, each committed atomically):
2. **Task 2 Attempt 1: honest fail-closed smoke (DI-43-06-01 surfaced)** — `293e527d` (evidence)
3. **Task 2 fix: thread data.blacklist_path to resolve DI-43-06-01** — `464fd40d` (fix)
4. **Task 2 diagnostic: R-1/D4-a guard-lifted observation run (not acceptance)** — `16b70ca2` (evidence)
5. **Task 2: ratify R-1 loss_explosion_ceiling at 1e11 via owner delegation** — `9cd5e853` (fix)
6. **Task 2 auto-fix: bump smoke rolling_keep 3->4 (Rule 3)** — `4ea595bd` (fix)
7. **Task 2 Attempt 2 (ACCEPTED): record real ACC-02 acceptance smoke run** — `ddf86fea` (evidence)

Task 3 (D4-a checkpoint — this continuation):
8. **Task 3: persist owner-ratified D4-a wall clock ceiling in stage0 template** — `386f2ee2` (feat)
9. **Task 3: record D4-a owner sign-off at 120 s** — `54a50b89` (evidence)

**Plan metadata:** (this commit) — `docs(43-06): complete real acc-02 smoke ratification plan`

_Note: this plan is not TDD-flagged; commits follow the evidence/fix rhythm dictated by the honest fail-closed → owner-decision → re-run cycle rather than RED/GREEN/REFACTOR._

## Files Created/Modified

- `configs/smoke.yaml` — added `data.blacklist_path` (owner-designated legacy blacklist) and bumped `run.checkpoint.rolling_keep` 3→4 (Rule 3 auto-fix).
- `configs/stage0-example.yaml` — D4-a `run.checkpoint.wall_clock_ceiling_s: 120` (owner-ratified, this continuation); fixed stale commented `loss_explosion_ceiling` guard example to `1.0e11`.
- `pinn/train.py` — `_resolve_admitted_data_root()` / `_resolve_blacklist_path()`; `_build_admitted_sources` now threads `blacklist_path` into `AdmittedSetAdapter` (DI-43-06-01 fix).
- `pinn/training/config.py` — `DataConfig.blacklist_path: Optional[str] = None`; `_PROVISIONAL_LOSS_EXPLOSION_CEILING` changed from `1.0e6` to `1.0e11` (R-1 ratification); constant name and provisional-registry entry deliberately left as-is.
- `tests/phase43/test_smoke.py` — real-data success-path artifact tests (`RealSmokeArtifactTests`), honesty-guard tests, corpus-reachability test.
- `tests/phase43/test_real_data_smoke_config.py` — `BlacklistPathResolutionTests` (8 tests: config-seam validation, relative/absolute/None resolution, `TinyCorpus` integration, missing-file fail-closed regression).
- `.planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md` — full, append-only evidentiary record of B-5, DI-43-06-01/02, the diagnostic run, the accepted acceptance smoke, and D4-a.

## Decisions Made

- **B-5 (2026-07-21):** Owner ratified the current `RESUME_FIELD_REGISTRY` unchanged (`ratify-current`). No source edit; the unclassified-field-refuses-resume fail-safe stays locked.
- **R-1 (2026-07-21, delegation):** Owner delegated `loss_explosion_ceiling` to the executor's best judgement. Ratified at `1.0e11` — ~25x headroom above the diagnostic run's observed ~4e9 peak total loss. Explicitly revisable at the ACC-05 Stage-0 pilot; not assumed to generalize across seeds/corpora/stages. The `provisional_fields()` flag for this field deliberately still reports `True`, since R-1 covers all three `GuardConfig` thresholds as one shared seam and `disk_floor_fraction`/`memory_watermark_fraction` remain uncalibrated — a reporting-granularity question left open, not a value ambiguity.
- **D4-a (2026-07-21, explicit selection — this continuation):** Owner picked `wall_clock_ceiling_s = 120` directly (not delegated), from presented context: verified stall-bounding mechanism (OR'd with `every_n_steps`, never an abort trigger), measured ~9-12 s normal inter-checkpoint interval, ~270-305 s production forecast, and the prior 3600 s template placeholder. Rationale: ~10x normal interval (never fires healthy) while bounding a stall to <=2 min.
- **rolling_keep 3→4 (Rule 3, operational, not owner-carved):** `CheckpointCadence.rolling_keep`'s class default of 3 evicted checkpoint 100 under the plan's required one off-cadence SIGTERM interrupt. Bumped to 4 in `configs/smoke.yaml` — the minimal value tolerating exactly one off-cadence interrupt alongside the 3 required periodic saves. Not one of v2.0's five owner-carved seams (documented as an "operational hygiene bound" in `CheckpointCadence`'s docstring), so within executor auto-fix authority.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Threaded `data.blacklist_path` to resolve DI-43-06-01**
- **Found during:** Task 2, Attempt 1
- **Issue:** The ordinary `pinn.train` command refused fail-closed before any training step — `AdmittedSetAdapter._load_blacklist` defaulted to a nonexistent path under `simulation_data/Data/`, and `DataConfig` exposed no `blacklist_path` field to override it. A genuine pre-existing wiring gap, not something the smoke should patch around silently.
- **Fix:** Owner (Option A, 2026-07-21) designated the legacy Documentation blacklist as authoritative; `GIT_AGENT_OWNED_PATHS` was expanded to include `pinn/training/config.py:pinn/train.py:configs/smoke.yaml` for this narrow, explicitly-scoped fix. Added `DataConfig.blacklist_path`, `_resolve_admitted_data_root()`/`_resolve_blacklist_path()` in `pinn/train.py`, and the config value in `configs/smoke.yaml`. `pinn/data/adapter.py`'s fail-closed `load_blacklist_file` was left untouched.
- **Files modified:** `pinn/training/config.py`, `pinn/train.py`, `configs/smoke.yaml`
- **Verification:** `tests.phase43.test_real_data_smoke_config` 29/29; `tests.phase41.test_config_yaml` 35/35; `tests.phase41.test_resume` 30/30 (no regressions).
- **Committed in:** `464fd40d`

**2. [Rule 3 - Blocking, operational] Bumped `rolling_keep` 3->4 to preserve checkpoint 100 across one off-cadence interrupt**
- **Found during:** Task 2, Attempt 1 (post-R-1-ratification acceptance attempt)
- **Issue:** `TorchSaveCheckpointStore.save_rolling()` pools periodic and interrupt-time saves into one shared eviction set; the single required SIGTERM interrupt added a 4th `step-*.pt` entry, and the class default `rolling_keep=3` evicted checkpoint 100 — violating this plan's must_have (checkpoints 100/200/300 all present).
- **Fix:** Bumped `configs/smoke.yaml`'s `run.checkpoint.rolling_keep` to 4 (minimal value tolerating one off-cadence interrupt alongside 3 periodic saves). `rolling_keep` is documented as an operational hygiene bound, not one of v2.0's five owner-carved seams, so this is within executor auto-fix authority.
- **Files modified:** `configs/smoke.yaml`
- **Verification:** Attempt 2 re-run confirmed all 4 `step-*.pt` entries (100/158/200/300) coexist under `rolling_keep=4`, no eviction.
- **Committed in:** `4ea595bd`

---

**Total deviations:** 2 auto-fixed (both Rule 3 — blocking issues discovered while proving the real, unmodified mechanical wiring; neither is an owner-carved v2.0 seam).
**Impact on plan:** Both fixes were required to complete the plan's own must_have (a real, gap-free acceptance smoke with all three required checkpoints). Neither touched an owner-carved decision (D1-p, D4-a, R-1/R-2, B-5); the owner-carved R-1 finding (DI-43-06-02) was escalated, not auto-fixed.

## Issues Encountered

- **DI-43-06-01 (RESOLVED):** genuine pre-existing blacklist-wiring gap, fixed under explicit owner authorization (see Deviations above).
- **DI-43-06-02 (RESOLVED):** the provisional `loss_explosion_ceiling` default (1e6) tripped against the real corpus's raw physics-residual scale at step 2 — a genuine finding, not a mechanical bug. Owner-authorized diagnostic runs (guard temporarily lifted for observation only, never committed at the lifted value) established the loss stays finite and bounded but does not resolve to a small controlled value within 300 steps; owner then delegated R-1 to best judgement, ratified at 1e11.
- **R2 honesty note (not a defect):** the accepted acceptance smoke's loss is bounded but **non-descending** across the full 300-step Adam budget (`validation.trend: "worsening"` at step 300; per-third medians ~4.0-4.3e8 with no downward trend). This is explicitly recorded as an **ACC-05 Stage-0 pilot watch-item** — the mechanical pipeline (launch/admit/train/checkpoint/interrupt/resume/finish/measure) is proven correct; whether the loss actually descends given a longer curriculum/budget is a separate, unresolved scientific question deliberately left open for the pilot, never characterized as convergence.
- **Surfaced but unresolved (by design):** `run.guards.loss_explosion_ceiling`'s entry in `TrainingConfig.provisional_fields()` still reports `provisional: True` even after R-1's value ratification, because R-1 is documented as one shared seam spanning all three `GuardConfig` thresholds and `disk_floor_fraction`/`memory_watermark_fraction` remain uncalibrated. Splitting the reporting mechanism to distinguish a ratified value from an unratified sibling was judged out of scope for this plan; the rationale is recorded in `pinn/training/config.py` and the evidence README, available for a future plan to resolve without re-touching the ratified value.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Both of 43-06's blocking owner checkpoints (B-5 Task 1, D4-a Task 3) are closed; R-1 (surfaced mid-plan as DI-43-06-02) is also closed via delegation.
- Real ACC-02 smoke evidence, measured timing (`s_per_step` range 0.094-0.1157, smoke forecast 34.71 s, production Stage-0 forecast ~270-305 s/run), and the D4-a ceiling are now available inputs for Phase 43's remaining plans.
- **43-07 (Stage-0 pilot + seed-band calibration, R-1/R-2 owner pause)** and **43-08 (go/adjust/rethink verdict, ACC-06 owner pause)** remain pending; this plan does not mark Phase 43 or milestone v2.0 complete. The ACC-05 loss-trend watch-item (non-descending within 300 steps) is the most important open item for 43-07 to observe over a longer run.

## Known Stubs

None. No hardcoded empty/placeholder values were introduced; the diagnostic run's guard-lifted config lived only in the scratchpad and was never committed.

## Self-Check: PASSED

- `configs/stage0-example.yaml`, `configs/smoke.yaml`, `pinn/train.py`, `pinn/training/config.py`, `tests/phase43/test_smoke.py`, `tests/phase43/test_real_data_smoke_config.py`, and the evidence README all exist on disk (all pre-continuation files carried over from prior tasks; `configs/stage0-example.yaml` verified modified this continuation).
- All 9 commits above (`8c36b790`, `293e527d`, `464fd40d`, `16b70ca2`, `9cd5e853`, `4ea595bd`, `ddf86fea`, `386f2ee2`, `54a50b89`) present in `git log --oneline --all`.
- `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_smoke -v` — 9/9 pass, 0 skips.
- `~/miniforge3/envs/pinn-train/bin/python -c "from pinn.training.config_yaml import load_config; cfg = load_config('configs/stage0-example.yaml'); assert float(cfg.run.checkpoint.wall_clock_ceiling_s) == 120.0"` — passes, prints `D4-a persisted: 120.0`.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-22*
