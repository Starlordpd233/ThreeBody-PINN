---
phase: 42-operator-runbook-surface-monitoring
plan: 02
status: complete
completed: 2026-07-19
---

# Plan 42-02 Summary

## What was built

Two owner-owned configuration seams the downstream sinks depend on:

### 1. MonitorConfig under `run.monitor`

- `@dataclass(frozen=True) class MonitorConfig` in `pinn/training/config.py` with fields:
  - `heartbeat_secs: int = 30` (heartbeat timing)
  - `staleness_factor: int = 3` (heartbeat staleness multiplier)
  - `tb_histogram_every: int = 100` (TB w_n-histogram thinning cadence)
  - `mem_every: int = 100` (periodic `mem:` line cadence)
- All fields validated via existing `_require_int` helper in `__post_init__`
- `RunConfig.monitor: MonitorConfig = field(default_factory=MonitorConfig)` with `isinstance` guard
- Registered in `config_yaml.py` import block AND `_resolve_nested_cls` known-name dict (`"MonitorConfig": MonitorConfig`)
- Fail-closed: unknown `run.monitor.*` keys raise `ConfigKeyError` (tested)

### 2. Provisional STEP_LOG_FIELDS registry

- New `pinn/training/step_log.py` with `STEP_LOG_FIELDS` dict-of-descriptors
- Registers every CANONICAL JSONL key: `event`, `step`, `stage`, `phase`, `epoch`, `loss_data`/`loss_ic`/`loss_phys`/`loss_energy`/`loss_angmom`, `total`, `lambda_data`/`lambda_ic`/`lambda_phys`/`lambda_e`/`lambda_l`, `grad_norm`, `w_min`/`w_mean`/`w_max`/`front_idx`, `lr`, `s_per_step`, `eta_seconds`, `step_completed`
- `step_completed` tagged with distinct provenance as emission-completeness metadata (not B-2 loss/metric)
- Deliberately absent: `residuals_bin_*` (TB-only, OPS-04b), `finite`/`nonfinite_keys` (sink-added, CTX-67) — documented in module docstring
- `step_log_fields_provisional_entry()` bridge appended to `TrainingConfig.provisional_fields()` via ImportError-guarded import
- All entries tagged `provisional: True` with provenance stating owner-ratification-before-run-#1

## Verification

- `MonitorConfig()` defaults: heartbeat_secs=30, staleness_factor=3 ✓
- `RunConfig().monitor` is `MonitorConfig` ✓
- Unknown `run.monitor.bogus_key` raises `ConfigKeyError` ✓
- All 25 required STEP_LOG_FIELDS keys present ✓
- No `residuals_bin_*` keys registered ✓
- `step_completed` provenance marks emission-completeness metadata ✓
- `step_log_fields_provisional_entry()` appears in `TrainingConfig().provisional_fields()` ✓
- Phase 40 config + Phase 41 config-yaml tests: 50/50 pass ✓

## Files modified

- `pinn/training/config.py` — MonitorConfig dataclass + RunConfig.monitor field + provisional_fields bridge
- `pinn/training/config_yaml.py` — MonitorConfig import + _resolve_nested_cls registration
- `pinn/training/step_log.py` (new) — STEP_LOG_FIELDS registry + provisional entry bridge
