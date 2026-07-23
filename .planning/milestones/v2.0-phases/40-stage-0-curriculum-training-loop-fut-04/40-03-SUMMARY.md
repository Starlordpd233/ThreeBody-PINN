---
phase: 40-stage-0-curriculum-training-loop-fut-04
plan: 03
type: execute
wave: 2
execution_status: completed
executed_at: 2026-07-17T09:05Z
review_status: verified
---

# Plan 40-03 Execution Summary

## Scope

Built the two smallest standalone driver pieces for the Phase-40 training loop:
the collocation sampler interface (TRAIN-04) and the sL-BFGS preflight typed
refusal (TRAIN-07). Both are interface/contract deliverables — dataset-free,
unittest-based, and green before any downstream integrator (40-05 RunController,
40-06 CurriculumController) lands.

## Artifacts landed

| File | Deliverable |
|---|---|
| `pinn/training/collocation_sampler.py` | `CollocationSampler` — uniform + adaptive (model, last_residuals) hook, caller-owned-RNG validation |
| `pinn/training/slbfgs_preflight.py` | `StochasticLBFGSNotImplemented` (typed exception carrying `.stage`) + `check_stage_preflight(stage)` |
| `tests/phase40/test_collocation_sampler.py` | TRAIN-04 contract: exact-N, [0, T] bounds, hook signature spy, non-Generator TypeError, global-RNG-untouched |
| `tests/phase40/test_slbfgs_preflight.py` | TRAIN-07 contract: {0,1,2} pass; {3,4,5,6} raise with non-empty message + `.stage` |

## Verification

```
<home>/miniforge3/envs/pinn-train/bin/python -m unittest \
  tests.phase40.test_collocation_sampler \
  tests.phase40.test_slbfgs_preflight \
  tests.phase40.test_prohibitions
# Ran 40 tests in 0.038s — OK
```

Each task's verify gate pairs its new test module with `test_prohibitions`
(re-run on every production-module change, per plan).

## Key design decisions

- **Adaptive hook is a side-effect observation seam.** The locked contract is the
  `(model, last_residuals)` call signature (D5-b / LOOP-03); the adaptive
  *density algorithm* is deferred to PLAT-05 (RESEARCH A4). The sampler invokes
  the hook for its side effect and produces a uniform fallback that satisfies
  the exact-N / in-bounds guarantees regardless. The hook's return value is
  ignored — PLAT-05 will own the density strategy.
- **RNG validation deferred to call time** (mirrors `pinn/data/batches._require_local_rng`,
  which runs inside `sample_collocation_points`, not at construction). A
  non-`numpy.random.Generator` raises `TypeError` on `uniform()`/`adaptive()`.
- **`T_CHARACTERISTIC_TIME` sourced from `pinn.constants`** — no literal `10.0`
  in the module.
- **`StochasticLBFGSNotImplemented`** mirrors the Phase-39 typed-sentinel
  exception pattern (`StageZeroUnderpopulated` / `DataVersionHashMismatch`):
  constructor stores `self.stage`, message cites the PLAT-02 deferral rationale.

## Prohibitions satisfied

- Stages ≥ 3 are a typed refusal, never a silent skip (TRAIN-07 / SPEC
  Prohibition 2).
- Global numpy/torch RNG is never touched; every RNG argument is caller-owned
  (TypeError on non-Generator).
- `test_prohibitions` passes with both new modules landed (no v1.3 tokens, no
  global-default mutation, no `.is_available(` probe, no `simulation_data`
  corpus-path access).

## Dependencies

- `depends_on: [40-01]` — satisfied (40-01 scaffold landed: `tests/phase40/`
  package, `_SKIP_PHRASE`, `_fixtures.make_stub_model`, `test_prohibitions`).
- No dependency on 40-02; 40-03 is standalone.

## Commit

`feat(40-03): add collocation sampler and sL-BFGS preflight typed refusal`
