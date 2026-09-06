---
status: complete
phase: 55-architecture-characterization-probe
source: [55-01-SUMMARY.md, 55-02-SUMMARY.md, 55-03-SUMMARY.md, 55-04-SUMMARY.md]
started: 2026-09-06T10:16:48Z
updated: 2026-09-06T10:16:48Z
---

## Current Test

[testing complete]

<!--
Retroactive UAT for Phase 55 (architecture characterization probe). All four
plan SUMMARYs carry a structured `coverage:` block; `gsd-tools query
uat.classify-coverage` returns `mode: coverage`, `all_auto_covered: true`,
`present: []` for every one — 20 deliverables, zero human-judgment checkpoints.
Per verify-work #1602 each deliverable is recorded pre-resolved as
`result: pass, source: automated`; a single confirmation summary was presented
to the operator in place of per-test interrogation. Covering suite re-run this
pass: `.venv/bin/python -m pytest tests/phase55/ -q` -> 46 passed.
No `<human-check>` blocks exist in any Phase 55 plan (55-VERIFICATION.md:
"Human Verification Required: None"). No cold-start smoke test injected — no
server / database / migration / startup file is in the phase change set.
-->

## Tests

### 1. Seven architecture-only quantities at initialization (55-01 D1)
expected: `measure_case` reports ‖r′‖, ‖v′‖, ‖a′‖, ‖F_grav‖, min pairwise separation, median R̄, the full causal weight vector, and front_idx for one seeded case with no data file, no optimizer, no training step; deterministic across two calls
result: pass
source: automated
coverage_id: 55-01-D1

### 2. Default six-case sweep + Tier-1 invariant bounds (55-01 D2)
expected: `run_sweep()` with no arguments measures the six audited cases; front_idx==0, 1e9<R̄<1e11, ‖F_grav‖ O(1), min-sep ≫ eps_soft for all six; DEFAULT_CASES is exactly the six audited rows; causal_weights[0]==1.0 with w[1:] at the dtype clamp floor; R̄ == ‖a′‖²/3 identity holds
result: pass
source: automated
coverage_id: 55-01-D2

### 3. SC3 derivation from the trainer implementation (55-01 D3)
expected: reported R̄, causal weights and derivative norms move in lock-step when a trainer primitive is mutated on the probe module (mutation proof, not an import check)
result: pass
source: automated
coverage_id: 55-01-D3

### 4. SweepCase fail-closed validation (55-01 D4)
expected: malformed `label`, `seed`, `masses`, or `ic13_mode` raise `ValueError` before any tensor is built
result: pass
source: automated
coverage_id: 55-01-D4

### 5. Phase-38 guarantees re-homed locally (55-01 D5)
expected: the `set_default_dtype`, `is_available`, and v1.3-import guarantees are re-homed into `tests/phase55/` for this module before the Phase-38 glob exclusion lands
result: pass
source: automated
coverage_id: 55-01-D5

### 6. Zero-argument CLI reproduces the six audited rows (55-02 D1)
expected: `python -m pinn.verification.architecture_characterization_probe` with no args measures the six DEFAULT_CASES rows at float64/CPU and exits 0
result: pass
source: automated
coverage_id: 55-02-D1

### 7. `--cases-config` surface + malformed rejection (55-02 D2)
expected: `--cases-config` drives an arbitrary case list; a malformed entry raises `ValueError` naming the field before any run directory is allocated
result: pass
source: automated
coverage_id: 55-02-D2

### 8. Atomic evidence writer with full provenance (55-02 D3)
expected: each run writes `raw.json` + `summary.md` into a non-overwriting UTC directory via `atomic_write_text`; the provenance record carries argv, command, git sha + availability, worktree dirty flag, Torch/NumPy versions, timestamp, conventions and clip facts
result: pass
source: automated
coverage_id: 55-02-D3

### 9. Evidence root inside `simulation_data/` rejected (55-02 D4)
expected: an `--evidence-root` beneath `simulation_data/` is refused before any directory is created
result: pass
source: automated
coverage_id: 55-02-D4

### 10. `main` exit code is not a recipe verdict (55-02 D5)
expected: `main` returns 0 on a completed measurement and non-zero only when the measurement did not complete; the record key set is fixed so no verdict field can be added silently
result: pass
source: automated
coverage_id: 55-02-D5

### 11. Phase-38 prohibition glob excludes the probe by one documented entry (55-02 D6)
expected: the probe is in `_EXCLUDE_SUFFIXES` with a D-02 rationale; every other module's assertions are unchanged; discovery does not list the probe
result: pass
source: automated
coverage_id: 55-02-D6

### 12. Ratified 4096 / 256 / 16 stratification helper (55-03 D1)
expected: `stratified_collocation_times` returns 4096 ascending times with exactly 256 entries in each of 16 ratified bins
result: pass
source: automated
coverage_id: 55-03-D1

### 13. Bin-mean reduction + rejection cases (55-03 D2)
expected: `bin_mean_residuals` returns 16 closed-form arithmetic means on a synthetic array and raises `ValueError` on a length mismatch, an out-of-range bin index, or an empty bin
result: pass
source: automated
coverage_id: 55-03-D2

### 14. D-03 helpers unreachable from the default sweep (55-03 D3)
expected: an AST call-graph closure from `run_sweep`/`measure_case`/`main` reaches neither new-structure helper (with a non-vacuity guard)
result: pass
source: automated
coverage_id: 55-03-D3

### 15. Default path passes exactly DEFAULT_N_COL residuals (55-03 D4)
expected: every `causal_physics_loss` call in the default `run_sweep()` and `main([])` receives exactly `DEFAULT_N_COL` (16) values
result: pass
source: automated
coverage_id: 55-03-D4

### 16. D-03 containment: no R_ref / GATE-04 evidence produced (55-03 D5)
expected: Phase 55 produced no 4096-structure measurement and no `R_ref`; `rg R_ref` / `GATE-04` in the probe and evidence returns no matches; committed `configuration.n_col` is 16
result: pass
source: automated
coverage_id: 55-03-D5

### 17. Committed exact-value fixture compared field-for-field (55-04 D1)
expected: `tests/phase55/fixtures/six_case_baseline.json` with `_meta` provenance is compared to fresh sweep output at the recorded `relative_tolerance` (1e-9)
result: pass
source: automated
coverage_id: 55-04-D1

### 18. Fixture is tamper-evident and read-only in the suite (55-04 D2)
expected: perturbing a copy of the baseline fails the comparison; the on-disk sha256 is unchanged across the whole suite run; no write-mode handle to the fixture exists in the suite
result: pass
source: automated
coverage_id: 55-04-D2

### 19. One committed re-derivable evidence run (55-04 D3)
expected: exactly one committed zero-argument CLI evidence run under `evidence/probe/` records the command, git tree state, and the full six-row output
result: pass
source: automated
coverage_id: 55-04-D3

### 20. Audit §6b decade cross-check (55-04 D4)
expected: the reproduction matches the 2026-08-17 residual-frame conformance audit §6b table at decade resolution — `front_idx = 0` and median `R̄` in the 10¹⁰ decade in every row
result: pass
source: automated
coverage_id: 55-04-D4

## Summary

total: 20
passed: 20
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none]
