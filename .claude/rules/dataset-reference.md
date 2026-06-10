---
paths:
  - "simulation_data/**"
  - "brutus_Newton-main/**"
---

## Data Pipeline Stages

1. **Stage 1 IC generation** — Standard quasi-random (Sobol) and hierarchical ICs.
   - Scripts: `simulation_data/Scripts/ic_generation/ic_generation_utils.py`, `simulation_data/Scripts/ic_generation/generate_ics.py`
   - Defaults: epsilon=0.05, velocity_scale=0.1, Sobol scrambling enabled.
2. **Stage 2 prescreening** — Short leapfrog integration to reject unstable ICs.
   - Script: `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`
   - Defaults: TMAX=1.0, DT=0.0001, ENERGY_ERROR_THRESHOLD=0.01, MIN_DISTANCE_THRESHOLD=0.01.
3. **Stage 3 Brutus integration**
   - Main runner: `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`
   - Gold hierarchical: `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py`
   - No in-repo runner for standard quasi-random gold outputs. Timeout: 3000s per simulation.
4. **Metrics** — `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`
5. **PINN preprocessing** — `pinn/data-processing-pipeline-full.py`

## Dataset Variants (Folder Defines Variant)

ICs (2 base folders):
- `simulation_data/Data/ic_final/ic_hierarchical/`
- `simulation_data/Data/ic_final/ic_standard_quasi_random/`

Brutus outputs:
- `simulation_data/Data/brutus_output/brutus_hierarchical/`
- `simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/`
- `simulation_data/Data/brutus_output/brutus_standard_quasi_random/`
- `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/`

**Mapping rule**: The numeric ID maps IC to Brutus output. File names do **not** encode "gold"; the folder defines the variant.

**ic_raw externalization**: Set `IC_RAW_DIR` environment variable before running Stage 1/2 scripts:
```bash
export IC_RAW_DIR=/path/to/ic_raw  # Expected subdirs: ic_hierarchical/, ic_standard_quasi_random/
```

**Gold-standard subset note**: Standard quasi-random gold Brutus outputs contain 2,565 files while the base IC folder contains 2,749. 184 IDs not selected — see `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`.

**ID gaps**: Intentional — caused by generation continuation, prescreen rejection, and failed Brutus runs.

## Typical Brutus Parameter Sets (Verify with Result: when present)

- Hierarchical: tol=1e-15, Lw=130, dt_out=0.08
- Standard quasi-random: tol=1e-13, Lw=118, dt_out=0.17
- Hierarchical gold: tol=1e-13, Lw=130, dt_out=0.01
- Standard gold: most commonly tol=1e-13 or 1e-14, Lw=130, dt_out=0.01

`dt_out` is the output sampling interval, not the internal adaptive step size.

## Data Formats

### IC File Format
```
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
```

### Brutus Output Format
```
# Snapshot header: t N t_cpu
0.000 3 0.00123
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3

[optional] Result: filename=... N=... t_begin=... t_end=... dt=... eta=... tol=... Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
```

Body lines can contain 30-40 significant digits. Parse as strings or Decimal for exact precision.

### Mandatory Parsing Rules
1. **Completeness check**: Use final timestamp >= 9.5. Do not rely on `Result:`.
2. **Result footer is optional**: Many files omit it. Treat it as metadata only.
3. **OS-dependent paths**: `Result: filename=` may be macOS or Windows style.
4. **t_end varies**: Some runs end at 10.01 or 10.03 when `dt_out` does not divide 10 exactly.

## Physical Conventions

### Units and Dimensionality
- Natural units with **G = 1** and total mass approximately **3**.
- Data is **3D**, not planar. Standard quasi-random can have large |z|; hierarchical tends near-planar.

### Mass and COM Properties
- **Standard quasi-random**: masses exactly 1.0, COM and total momentum exactly 0 by construction.
- **Hierarchical**: masses vary, normalized to total mass ~3. COM/momentum enforced then **perturbed** with Gaussian noise (sigma=0.01) — **not** exactly 0. Recenter/reboost before analysis if exact COM frame is required.

### Sampling Notes (Standard Quasi-Random)
- p1 fixed at (1, 0, 0); p2 sampled on hemisphere with x <= 0; p3 = -(p1 + p2).
- Velocity components sampled from Normal(0, velocity_scale) via Sobol inverse CDF.
- Global scaling enabled in `generate_ics.py` with `scale_range=(0.8, 1.2)`: both positions and velocities scale by s; virial ratio scales as Q ~ s^3.

### Sampling Notes (Hierarchical)
- Inner binary semi-major axis: a ~ 0.1-0.3. Outer body separation: 3-10x inner.
- Small inner inclination; Gaussian perturbations applied (sigma=0.01).

## Build and Run Brutus

```bash
cd brutus_Newton-main
make clean
make

./brutus 1e-15 130 0 10 0.08 3 /abs/path/ic.txt > /abs/path/output.txt
```

## Pipeline Commands

```bash
python simulation_data/Scripts/ic_generation/generate_ics.py
python simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py
python simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py
python simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py
python simulation_data/Scripts/metrics_calculation/calculate_metrics.py
```

## Validation and Quality Assurance

**Completeness check** (mandatory): final_timestamp >= 9.5 before processing any Brutus output.

Conservation metrics: `simulation_data/Data/metrics/` — energy, momentum, angular momentum drift.
- Escape: max separation > 100. Collision: min separation < 0.01.

Provenance files:
- Prescreening logs: `simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_hierarchical.json` and `processing_index_ic_standard_quasi_random.json`
- Footer audit reports: `simulation_data/Validation/audit_reports/` (most recent: `footer_audit_20251224_170141.md`)
- Audit script: `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`
- Failed ICs: `simulation_data/Documentation/problematic_ics_blacklist.json`

**Validation checklist:**
- [ ] Final timestep >= 9.5
- [ ] Result footer handled (or fallback used)
- [ ] IC file format validated
- [ ] Metrics JSON produced for each output
- [ ] COM/momentum handling chosen explicitly for hierarchical ICs

## Known Issues and Gotchas

- **Result footer presence variation**: Many files have no `Result:` footer at all — 1,550 in `brutus_hierarchical`, 701 in `brutus_standard_quasi_random`, 219 in `brutus_standard_quasi_random_gold_standard` (verified 2026-06-10; matches the missing-footer counts in `footer_audit_20251224_170141.md`). Footers that are present carry the full schema including `eta` and `tol`. Fall back to folder defaults when the footer is absent.
- **Parameter heterogeneity**: Multiple tol, Lw values exist within the same folder. Prefer actual `Result:` values when present.
- **Standard gold provenance**: No runner script in repo; treat provenance as partial.
- **OS path variance**: Result footer paths can be macOS or Windows; do not use them as an authoritative mapping.
- **Hierarchical COM offset**: Post-perturbation COM and momentum are not zero; recenter if needed.
