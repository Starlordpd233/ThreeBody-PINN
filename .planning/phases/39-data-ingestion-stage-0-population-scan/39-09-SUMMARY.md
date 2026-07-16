---
status: active
purpose: implementation-plan
created: '2026-07-15'
milestone: v2.0
phase: 39-data-ingestion-stage-0-population-scan
retirement_trigger: Phase 39 closes and the summary is consumed by verify-work.
execution_status: executed
executed_at: '2026-07-15T22:21:00'
review_status: passed
---

# Plan 39-09 Summary: Fail-closed adapter and CLI safety configuration

## Objective

Close the DATA-01 memory-safety bypass by validating every residency/configuration input before corpus work.

## Changes

### `pinn/data/adapter.py`

Added `_validate_adapter_config(capacity_bytes, memory_watermark, interim_s0, device)` — a fail-closed boundary called at the top of `AdmittedSetAdapter.__init__`, before `_resolve_root`, `_scan_and_admit`, tensor materialization, or memory logging:

- **capacity_bytes**: positive finite integer (rejects bool, 0, negative, NaN, Inf).
- **memory_watermark**: finite in `(0, 1]` (rejects NaN, Inf, 0, negative, >1).
- **interim_s0**: finite and positive (rejects NaN, Inf, 0, negative).
- **device**: normalized through `torch.device` and required to have `type == "cpu"` (rejects `meta`, `cuda`, `mps`, and malformed devices).

The normalized CPU device is stored in `self._device`; `classifier_interim_s0` is stored as `float(interim_s0)`.

### `pinn/data/stage_scan.py`

`main()` now runs a finite/range preflight before constructing `AdmittedSetAdapter`, printing a `stderr` error and returning exit code 1 on invalid `--memory-capacity-bytes`, `--memory-watermark`, or `--interim-s0`. The adapter options dict now passes `device="cpu"` explicitly (D-03 CPU residency contract).

### `tests/phase39/test_adapter.py`

Added `AdapterConfigValidationTests` (19 tests): table-driven rejection matrix via `_rejects_before_side_effects`, which patches `_resolve_root` to raise if reached — proving validation runs before any corpus-side effect. Covers capacity (0, negative, NaN, Inf, bool), watermark (NaN, Inf, 0, negative, >1, bool), interim_s0 (NaN, Inf, 0, negative), device (`meta`, `cuda`, `mps`), plus a positive control that valid CPU defaults still initialize.

### `tests/phase39/test_stage_scan.py`

Added 11 CLI tests to `StageScanCliContract`: each invalid flag (`--memory-capacity-bytes` 0/negative, `--memory-watermark` NaN/Inf/0/negative/>1, `--interim-s0` NaN/Inf/0) asserts a nonzero exit code and that the mocked `AdmittedSetAdapter` factory is `assert_not_called()`. Added `test_cli_forwards_explicit_device_cpu` confirming `device="cpu"` reaches the adapter. Updated `test_cli_forwards_all_explicit_adapter_and_split_flags` to expect `device="cpu"`.

## Verification

```
$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_stage_scan -v
```

120 tests, 0 failures.
