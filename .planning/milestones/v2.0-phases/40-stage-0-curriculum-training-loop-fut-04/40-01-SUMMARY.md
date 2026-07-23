---
status: consumed
purpose: implementation-plan
created: 2026-07-17
milestone: v2.0
phase: 40-stage-0-curriculum-training-loop-fut-04
retirement_trigger: Phase 40 fully executed and verified (all 6 plans green)
execution_status: complete
executed_at: 2026-07-17
review_status: verified
---

# Plan 40-01 Summary — Dataset-free Phase-40 test contract + pinn/training skeleton

## Objective

Stand up the dataset-free Phase-40 test contract and the empty `pinn/training/` package so every subsequent TRAIN-01..07 module lands against a ready test harness. This is the Nyquist Wave-0 foundation: shared skip phrase, shared stub batch source + stub model, and the mechanical prohibitions audit that every later production-module change re-runs.

## Files produced

- `pinn/training/__init__.py` — minimal side-effect-free package marker (docstring states importing performs NO model build and NO dataset discovery; `__all__ = []`; full barrel re-exports deferred to plan 40-06).
- `tests/phase40/__init__.py` — `_SKIP_PHRASE = "skipped Phase40 production symbol"` + `__all__`.
- `tests/phase40/_fixtures.py` — `_StubSource` (duck-typed `StageQuery` mirroring `StageIndex`), `make_stub_source`, `make_stub_split_sources` (disjoint train/validation pair mirroring `StageIndex.from_split` over `"train"`/`"validation"` — NOT a split flag), `make_stub_model` (CPU/float64 `build_network(ArchitectureSpec(), ...)` with explicit dtype/device args).
- `tests/phase40/test_prohibitions.py` — `discover_training_modules()` (non-recursive glob, filesystem-driven), `executable_source`/`executable_source_from_text`, four ban families (v1.3 tokens, global-default mutation, `.is_available(` call-form probe, `simulation_data` corpus path), and `NonFiniteContractTests` with three detectors (`defines_or_imports_exception` over `grad_clip.py`, `has_nonfinite_raise_flag` over every module, `catches_around_clip` over `controllers.py`) plus `DetectorSelfTests` synthetic-violation proofs. Named-module halves are `.is_file()`-guarded (vacuous at Wave 1, armed automatically when 40-02/40-05 land).

## Verification

```
# Task 1: fixtures + real build_stage_batch on both split stubs
python -c "import numpy as np, torch; from tests.phase40 import _SKIP_PHRASE; import tests.phase40._fixtures as f; from pinn.data.batches import build_stage_batch; assert _SKIP_PHRASE=='skipped Phase40 production symbol'; m=f.make_stub_model(); tr,va=f.make_stub_split_sources(); assert set(tr.record_keys()).isdisjoint(set(va.record_keys())); b=build_stage_batch(tr, stage=0, rng=np.random.default_rng(0), dtype=torch.float64, device=torch.device('cpu')); assert b.data_points is not None; bv=build_stage_batch(va, stage=0, rng=np.random.default_rng(1), dtype=torch.float64, device=torch.device('cpu')); assert bv.data_points is not None"
→ fixtures + REAL build_stage_batch on both split stubs OK
  model: SQRSkipResNetSIREN | train keys: 300 | val keys: 300
  batch data_points shape: (7680, 14) | collocation: (4096, 14)

# Task 2: prohibitions audit (16 tests)
python -m unittest tests.phase40.test_prohibitions -v
→ Ran 16 tests in 0.001s. OK
```

## Notes

- Recovered pos1 of watchdog chain `phase-40-execution` (prior session a1d1 died mid-execution with stale enrollment, no work produced). Stale enrollment backed up to `.git/live-monitor/chains/phase-40-execution/positions/1/enrollment.json.stale-backup-*.json` and reclaimed.
- The v1 token ban includes both hyphen and underscore variants (`data-handling`/`data_handling`, `data-processing-pipeline-full`/`data_processing_pipeline_full`) matching the phase39 precedent, so an `import data_handling` re-introduction is caught.
- `catches_around_clip` scopes to handler-bearing `Try` nodes only, so 40-05's required bare `try/finally` (no handlers) restoring `model.train()` cannot trip it — proven by a `DetectorSelfTests` case.
