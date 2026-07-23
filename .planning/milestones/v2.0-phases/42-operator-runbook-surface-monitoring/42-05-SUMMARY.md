---
phase: 42-operator-runbook-surface-monitoring
plan: 05
status: complete
completed: 2026-07-19
---

# Plan 42-05 Summary

## What was built

The TensorBoard secondary view + per-time-bin residual panel (OPS-03 / OPS-04b)
as a `SummaryWriter`-backed sink fed from the same widened `_log_step` record as
the JSONL log, plus the realized `test_residual_panel` suite.

### 1. TbSink (`pinn/training/tb_sink.py`)

`TbSink(logging.Handler)` on the `pinn.training` logger tree — the same attach
shape as the 42-04 JSONL/human handlers, so all three sinks fan out from the one
CTX-65 emission point:

- Owns a `torch.utils.tensorboard.SummaryWriter(log_dir=runs/<name>/tb/)`; `torch`
  is imported lazily in `__init__` so the class stays importable/pure and is
  instantiated only at the composition root (Anti-Pattern #5). `add_scalar`
  enqueues onto the writer's OWN background thread — no matplotlib, no synchronous
  plotting in the step loop (CTX-69 async constraint; `grep -c matplotlib` = 0).
- `emit` consumes the widened `extra=` step record (`event=="step"`) and fans out:
  the OPS-03 canonical scalars (`total`, `loss_*`, `lambda_*`, `grad_norm`, `lr`,
  `s_per_step`, `eta_seconds`); `residuals/bin_{n:02d}` from each `residuals_bin_*`
  field (OPS-04b, TB-only — 42-04 filters this family out of the JSONL, so TbSink
  is its SOLE consumer, cycle-2 HIGH-1); and `causal/w_min|w_mean|w_max|front_idx`
  from the `w_*`/`front_idx` fields (the `causal/*` TB-side rename, CTX-70).
- Null policy: a `None` field (absent this step) is skipped; NaN / `0.0` / `-1`
  are REAL readings and always emit — a collapsed `w_n` and a stalled front
  (`front_idx=-1`, guaranteed ≥ -1 by 42-01's `default=-1`) are exactly the
  silent-failure signal the panel exists to surface (cycle-2 agy HIGH).
- CTX-69 warn-once guard: `SummaryWriter` construction and every
  `add_scalar`/`flush`/`close` are wrapped; the first failure logs ONE warning to
  `pinn.training.tb_sink` and later failures stay silent — a monitoring fault
  never aborts the run it observes (threat T-42-04). `close()` flushes/closes the
  writer for the terminal path.

### 2. test_residual_panel (`tests/phase42/test_residual_panel.py`)

Realized the 42-03 stub (production-symbol `_require` skip guard dropped; the
pinn-train availability guard kept so a torch/tensorboard-less interpreter skips
cleanly). Three tests:

- **OPS-04b presence** — drives the real `RunController._log_step` emission point
  with the widened causal fields for several steps, then reads back via
  `EventAccumulator` and asserts `residuals/bin_*` + `causal/*` are present with a
  consistent 1:1-per-record step count.
- **Collapse/NaN round-trip** — a collapsed record (`w_n→0`, `front_idx=-1`,
  `residuals_bin_00=NaN`) still emits the whole panel, and the written NaN reads
  back as NaN via `EventAccumulator` (Pitfall 3: the low-level event-file loader
  would zero it — `EventAccumulator` is used exclusively; `grep EventFileLoader`=0).
- **CTX-69 warn-once** — a forced `add_scalar` failure logs exactly one warning
  and never propagates into the step loop.

## Deviation (execution note)

Plan Task 2 specified driving the presence test through `run_stage(0)`. That is
structurally infeasible with the synthetic Stage-0 fixture: the fixture's stub
source holds 8 records but the Stage-0 replay batch requires 240
(`StageZeroUnderpopulated: 8 < 240`, `pinn/data/batches.py`), and the stub loss
(`make_stub_model` + default `LossConfig`) computes no causal residuals, so even a
runnable `run_stage(0)` would emit step records WITHOUT the `residuals_bin_*`/`w_*`
fields the panel asserts. The faithful OPS-04b integration — "a real widened
record fans out to the correct TB tags" — is therefore driven through the genuine
`RunController._log_step` (the single CTX-65 emission point, exercising the real
`residuals_bin_{n:02d}` enumeration and `w_*` extraction in controllers.py) rather
than the full optimizer/batch. This exercises the controllers.py → TbSink
field-name contract that OPS-04b is about; it does not weaken the assertions.
`run_one_step` (referenced by the `_fixtures.run_synthetic_steps` helper) does not
exist in `pinn/`, so it was not an alternative.

## Verification

Env: `conda run -n pinn-train`.

- `tests.phase42.test_residual_panel -v`: **3/3 pass**, not skipped ✓
- Task 1 inline smoke — `TbSink(dir).emit(record_with_NaN)` writes TB event data
  (dir non-empty) and does not raise → `OK tb` ✓
- `grep -c matplotlib pinn/training/tb_sink.py` = 0 ✓
- CTX-70 tag names (`residuals/bin_`, `causal/w_min`, `causal/front_idx`) present
  in `tb_sink.py` ✓
- `grep -c EventAccumulator` = 8 (≥1) AND `grep -c EventFileLoader` = 0 ✓
- Collapse/NaN test asserts the panel still emits and the NaN survives the
  `EventAccumulator` round trip ✓
- `python -m py_compile` clean on both owned files ✓

## Files modified

- `pinn/training/tb_sink.py` (new) — `TbSink` (`SummaryWriter` wrapper;
  `residuals/bin_{n:02d}` + `causal/w_min|w_mean|w_max|front_idx` tags; null
  policy; warn-once guard; `flush()`/`close()`).
- `tests/phase42/test_residual_panel.py` — realized OPS-04b presence
  (`EventAccumulator` readback via the real `_log_step` fan-out) + collapse/NaN +
  CTX-69 warn-once tests.
