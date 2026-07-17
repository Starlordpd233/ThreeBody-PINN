---
phase: 40-stage-0-curriculum-training-loop-fut-04
plan: 04
type: execute
wave: 2
execution_status: completed
executed_at: 2026-07-17T09:15Z
review_status: verified
---

# Plan 40-04 Execution Summary

## Scope

Built the stage-exit decision machine (TRAIN-06 / CURR-03) and the two Phase-41
seams controllers depend on: nested frozen `TrainingConfig` (CTX-42/39) and the
`CheckpointStore` protocol + naive `weights_only` torch impl (CTX-43/44).
Dataset-free, unittest-based; green before integrators 40-05 / 40-06.

## Artifacts landed

| File | Deliverable |
|---|---|
| `pinn/training/stage_exit.py` | `StageDisposition` (ADVANCE/RECOVER/HALT — three members), `StageExitOutcome` (`disposition: StageDisposition \| None`), `TotalLossPlateauSmoother` (β-EMA + patience), `StageExitMachine.evaluate(...)` pinned signature |
| `pinn/training/config.py` | `TrainingConfig` + nested `RunConfig`/`StageConfig`/`OptConfig`/`LossConfig`, `ConfigRequiredError`, provisional field enumeration, flat gate surface for StageExitMachine |
| `pinn/training/checkpoint.py` | `CheckpointStore` Protocol, `TorchSaveCheckpointStore` (torch.save / torch.load weights_only=True), `EmptyCheckpointStore` |
| `tests/phase40/test_stage_exit.py` | TRAIN-06 + M3 mechanism tests (local stub config, no config import) |
| `tests/phase40/test_config.py` | CTX-39 required fields, GAP-40-02 invariant, provisional enumeration, no YAML/precision |
| `tests/phase40/test_checkpoint.py` | round-trip, rollback, empty-store raise, weights_only flag, plain payload |

## Verification

```
<home>/miniforge3/envs/pinn-train/bin/python -m unittest \
  tests.phase40.test_stage_exit \
  tests.phase40.test_config \
  tests.phase40.test_checkpoint \
  tests.phase40.test_prohibitions -v
# Ran 59 tests in 0.044s — OK
```

Integration smoke: `StageExitMachine(TrainingConfig(...))` with flat history →
`StageDisposition.ADVANCE`.

## Key design decisions

- **GAP-40-01 → B (ruled):** mid-flight is `disposition is None`; enum stays
  three-member (ctl_instruction.md:1928). No CONTINUE member.
- **GAP-40-02 → A (ruled):** `max_epochs` bounds the whole stage;
  `n_adam ≤ max_epochs` validated at StageConfig construction (equality legal).
- **Criterion 1 mechanism (M3):** `TotalLossPlateauSmoother` is separately
  constructible and driven by raw history in tests — not a boolean stub.
- **Task 1 independence:** `test_stage_exit` injects a local SimpleNamespace;
  production `stage_exit.py` does not import `config.py`.
- **T-40-02 closed now:** every `torch.load` path passes `weights_only=True`.
- **No hardcoded gate thresholds** in `stage_exit.py`; all read from injected
  config. CTX-38 values live as provisional-tagged defaults on `StageConfig`.

## Watchdog

Position D of chain `phase-40-execution`, woke on C's
`phase-40-execution-3` done at head `b425231a` (plan 40-03).
