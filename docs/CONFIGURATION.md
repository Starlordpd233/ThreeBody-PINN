<!-- generated-by: gsd-doc-writer -->

# CONFIGURATION

This project does not use a traditional `.env` file or a single centralized config file. Configuration is distributed across three layers:

1. **Framework specs** under `pinn_instruction/markdown_conversion/framework-specs/` (authoritative methodology, frozen/active status by file)
2. **Pipeline scripts** under `simulation_data/Scripts/` (Python IC generation, prescreening, Brutus runners, metrics)
3. **Brutus build config** under `brutus_Newton-main/makefile` (C++ arbitrary-precision integrator)

This document enumerates the configurable values in each layer, their defaults, and their authoritative source. It is not a runbook for changing them — see `docs/runbooks/` for operational procedures.

---

## 1. Framework Specs (Authoritative)

The framework specs live under `pinn_instruction/markdown_conversion/framework-specs/`. Each spec has a distinct edit status under the v1.6 governance rules.

| File | Status | Edit policy (v1.6) | Purpose |
|---|---|---|---|
| `ctl_instruction.md` | Active | Spec-edit target for v1.4 / v1.5 / v1.6 | CTL methodology, input-vector formulation, curriculum staging, dataset comparison table |
| `pinn_architecture.md` | Active | Spec-edit target for v1.4 / v1.5 / v1.6 | Network architecture, AD contract, output head, SQR-SkipResNet-SIREN blueprint |
| `sampling_method.md` | **FROZEN** | Read-only by default; revisions only on explicit user instruction triggered by verified data-feasibility issues | Historical record of how the existing training data was produced; generation is complete and will not be re-run |
| `framework-revisions/data_quality_assessment.md` | Read-only research report | Characterize only; do not edit | Research report, not an authoritative spec |
| `trainex-r1/` | Active | Authoritative trainex (training-execution) research round | Decomposition + PH inventory from the foundational trainex research round |

**Spec-edit scope for v1.6 (SCOPE-13):** `ctl_instruction.md` and `pinn_architecture.md` are the only spec-edit targets (unchanged from v1.4/v1.5). The `pinn/` live-code ban is in effect: live code in `pinn/` is NOT a grounding source for v1.4/v1.5/v1.6 spec decisions (forward-pointing handoff only, e.g., `NN-CODE-DIVERGENCE.md`, `pinn/STATUS.md`).

---

## 2. Dataset Variant Naming

The dataset is organized by IC type and a *gold-standard* subset flag. There are two IC-type families (`hierarchical`, `standard_quasi_random`), and each can be either a base variant or a `*_gold_standard` subset. The naming is consistent across the four pipeline stages.

### 2.1 IC families

| IC type | Generator | Description |
|---|---|---|
| `hierarchical` | `generate_stable_hierarchical_systems` in `ic_generation_utils.py` | Stable hierarchical triple systems; inner binary `a_inner ~ U(0.1, 0.3)`; outer body `3-10x` inner separation; Kozai–Lidov stability enforced |
| `standard_quasi_random` | `EnhancedThreeBodySampler` in `ic_generation_utils.py` | Sobol-based 6D (position+velocity) quasi-random sampling; `epsilon=0.05` minimum separation; non-zero initial velocities; scale range `[0.8, 1.2]` |

The `gold_standard` tag is applied as a **subset** within each family — files promoted to the gold-standard subset are those that meet higher-precision Brutus simulation success criteria. It is not a third IC type; it is a membership flag.

### 2.2 Directory naming convention (end-to-end)

The four pipeline stages use a consistent directory naming pattern. The pipeline always appends the type, and may append `_gold_standard` for the high-precision subset.

| Stage | Path pattern | Examples |
|---|---|---|
| Raw ICs (external) | `$IC_RAW_DIR/<ic_type>/` | `ic_hierarchical/`, `ic_standard_quasi_random/` |
| Final ICs (post-prescreen) | `simulation_data/Data/ic_final/<ic_type>/` | `ic_hierarchical/`, `ic_standard_quasi_random/` |
| Brutus output | `simulation_data/Data/brutus_output/brutus_<ic_type>[_gold_standard]/` | `brutus_hierarchical/`, `brutus_hierarchical_gold_standard/`, `brutus_standard_quasi_random/`, `brutus_standard_quasi_random_gold_standard/` |
| Metrics | `simulation_data/Data/metrics/sim_result_metric_<ic_type>[_gold_standard]/` | `sim_result_metric_hierarchical/`, `sim_result_metric_hierarchical_gold_standard/`, `sim_result_metric_standard/`, `sim_result_metric_standard_gold_standard/` |

**Naming note:** For the metrics layer, `sim_result_metric_standard` corresponds to the `standard_quasi_random` IC type (the `standard` prefix is the metrics-file prefix, not the IC-type literal). The gold-standard files use the metrics prefix `hierarchical` / `standard` (not `hierarchical_gold_standard` / `standard_gold_standard`) — see `METRICS_PREFIXES` in `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`.

### 2.3 Gold-completeness state (v1.5; carried into v1.6 unchanged)

Per GAP-29-01 (resolved 2026-06-16): 117 ICs are validated as gold, 67 are permanent `gold_counterpart=absent`, and 0 are promoted. The 184 → 67 cascade is deferred to FUT-01. (Verified against `.planning/milestones/v1.5-GAPS.md` GAP-29-01 and the Phase 29 verification record.)

### 2.4 Dataset comparison (per `ctl_instruction.md` Table `tab:brutus_compare`)

| Set | IC Type | Tolerance | Word Length | dt_out | Temporal Density vs. baseline |
|---|---|---:|---:|---:|---|
| Set 1a (4857 files) | Hierarchical | `1e-15` | 130 | 0.08 | 1x (baseline) |
| Set 1b (2749 files) | Standard | `1e-13` | 118 | 0.17 | 1x (baseline) |
| Set 2a (4857 files) | Hierarchical | `1e-13` | 130 | **0.01** | **8x** |
| Set 2b (2565 files) | Standard | `1e-13` | 130 | **0.01** | **17x** |

Total: 15,028 IC + Brutus-output pairs were generated for the v1.3-era training data. Final file counts are subject to prescreening and Brutus computational feasibility.

---

## 3. Environment Variables

| Variable | Required by | Default | Description |
|---|---|---|---|
| `IC_RAW_DIR` | `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`, `simulation_data/Scripts/ic_generation/ic_generation_utils.py` | **Required — startup fails if unset** | Path to the external `ic_raw` directory holding pre-prescreening ICs (`ic_hierarchical/`, `ic_standard_quasi_random/`). Set with `export IC_RAW_DIR=/path/to/ic_raw`. Required because raw ICs are kept external to the repo. |

There is no `.env`, `.env.example`, or `.env.sample` file in the repository root. `IC_RAW_DIR` is the only environment-driven configuration for the **simulation pipeline**. The v2.0 trainex training code (`pinn/`) adds its own variables — see §3.1.

### 3.1 Trainex training env vars (v2.0)

The v2.0 trainex training code under `pinn/` reads two additional environment variables:

| Variable | Read by | Purpose |
|---|---|---|
| `GSD_DATA_ROOT` | `pinn/data/adapter.py`, `pinn/train.py`, `pinn/training/config.py` | Overrides the dataset root the Stage-0 data adapter reads from. |
| `GSD_ALLOW_PARTIAL_DATA_ROOT` | same | Companion flag controlling whether a partial / fixture-scale data root is accepted instead of requiring the full dataset. See `pinn/data/adapter.py` for exact semantics. |

---

## 4. Pipeline Stage Configuration

### 4.1 IC generation defaults (`ic_generation_utils.py`)

| Parameter | Default | Source / context |
|---|---|---|
| `epsilon` | `0.05` | Minimum allowed distance between particles (PDF recommendation) |
| `scale_range` | `(0.8, 1.2)` for standard; `(1.0, 1.0)` for hierarchical | Scale variation. Standard explicitly enables sampling-time size variability per `sampling_method.md` "Sampling-Time Size Variability" note (distorts virial ratio by `s^3`); hierarchical does not scale by default |
| `velocity_scale` | `0.1` | Standard deviation for non-zero velocity component sampling |
| Sobol dim | 3 + (1 if scaling) + (3 if velocity) + (3 if rotate) | Quasi-random coordinate allocation; per v1.4 Phase 20.5 lock, scale factor sits at `u_4` ahead of velocity coords `u_5`–`u_7` in the standard configuration |
| `seed` | `42` (standard) / `43` (hierarchical) | Sobol scrambling seed in `generate_ics.py` (standard `seed=42`, hierarchical `seed=43`). The metrics scripts contain no seed. |
| `mass` | `1.0` | Base mass unit (natural units; `G=1.0`) |
| Mass sampling (hierarchical) | `q_inner ~ U(0.1, 1.0)`, `q_outer ~ U(0.1, 2.0)`, `m_1 ~ U(0.5, 1.5)`, normalized to `m_1+m_2+m_3=3` | Per `sampling_method.md` Stage 1 |
| Hierarchical separation | `R ~ U(max(3, min_ratio), 10)` with `min_ratio = 2.8 * ((1 + q_outer) / 0.5) ** 0.4` | Kozai–Lidov stability threshold; source comment: `Assume max e_outer = 0.5` (denominator is the literal `0.5`, not `(1+e_outer)`) |

The driver script `simulation_data/Scripts/ic_generation/generate_ics.py` exposes two top-level toggles:

- `GENERATE_STANDARD` (default `True`)
- `GENERATE_HIERARCHICAL` (default `True`)

and per-type sample counts (`N_SAMPLES_STANDARD=2500`, `N_SAMPLES_HIERARCHICAL=1500`).

### 4.2 Prescreening thresholds (`stage2_prescreening_revised_auto.py`)

| Parameter | Value | Notes |
|---|---|---|
| `TMAX` | `1.0` | Leapfrog integration time |
| `DT` | `0.0001` | Leapfrog time step |
| `ENERGY_ERROR_THRESHOLD` | `0.01` | 1% relative energy error |
| `MIN_DISTANCE_THRESHOLD` | `0.01` | Minimum separation during integration |
| `VIRIAL_RATIO_MIN` | `0.001` | Revised (was `0.7`) — accepts cold systems |
| `VIRIAL_RATIO_MAX` | `2.0` | Revised (was `1.5`) — slightly wider upper bound |
| `MIN_ANGULAR_MOMENTUM` | `0.0` | Revised (was `0.1`) — no minimum |
| `USE_PERCENTILE_THRESHOLDS` | `True` | Adaptive filtering enabled |
| `VIRIAL_PERCENTILE_MIN` | `1` | Keep top 99% of systems |
| `VIRIAL_PERCENTILE_MAX` | `99.5` | Remove top 0.5% outliers |
| `ANGULAR_PERCENTILE_MIN` | `0` | No angular-momentum filtering |
| `G` | `1.0` | Gravitational constant (natural units) |

> **Note on virial ratio:** The `MIN_ANGULAR_MOMENTUM` and virial thresholds here are not the ratio-based SCS thresholds flagged in the v1.5 issue doc (`pinn_instruction/issues/02-data-pipeline-and-validation.md`). This script's thresholds are local prescreen-rejection criteria; the SCS adjudication was **resolved in v1.5 Phase 25 (EVID-10)** — the locked log-based gate `SCS > -5` / `eps_H > 1e-5` stands and the issue-02 ratio thresholds were rejected by name. Do not use this prescreening config as evidence for the SCS-threshold decision; see `ctl_instruction.md` Step-1A clause 5 for the canonical gate and `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md` for the adjudication record (archived with the v1.5 phases).

### 4.3 Brutus simulation parameters

Brutus is invoked as:

```bash
./brutus <tolerance> <word_length> <t_begin> <t_end> <dt_out> <n_particles> <input_ic> > <output>
```

The pipeline scripts fix the per-type parameter set. `t_begin=0`, `t_end=10`, `n_particles=3` are constant across all four variants.

| Variant | Tolerance | Word Length | dt_out | Source |
|---|---:|---:|---:|---|
| `hierarchical` (Set 1a) | `1e-15` | `130` | `0.08` | `run_brutus_both_type_simple.py`, `calculate_metrics.py` |
| `standard` (Set 1b) | `1e-13` | `118` | `0.17` | same |
| `hierarchical_gold_standard` (Set 2a) | `1e-13` | `130` | `0.01` | `calculate_metrics.py` (BRUTUS_PARAMS block) |
| `standard_gold_standard` (Set 2b) | `1e-13` | `130` | `0.01` | same |

> **Note on the Set 2 / gold_standard values:** The `run_brutus_hierarchical_only_mac_gold_standard.py` runner uses a *separate* parameter set (`tolerance=1e-13`, `word_length=130`, `dt_out=0.01`) when generating the gold-standard **hierarchical** subset. The `dt_out=0.01` values here match the Set 2 rows of the `ctl_instruction.md` table, and the `calculate_metrics.py` gold-standard param block records the same set, so the two sources agree.

### 4.4 Brutus runner tuning knobs

`run_brutus_both_type_simple.py` exposes additional runner-level settings (independent of per-IC Brutus parameters):

| Knob | Default | Description |
|---|---:|---|
| `HIERARCHICAL_ICS_PER_RUN` | `10` | Max hierarchical ICs processed per runner invocation |
| `STANDARD_ICS_PER_RUN` | `0` | Max standard ICs processed per runner invocation (disabled by default) |
| `TIMEOUT_SECONDS` | `3000` | Per-simulation timeout (50 min) |
| `LINE_COUNT_THRESHOLDS` (hierarchical) | `(600, 700)` | Expected output line range (~150–175 clusters) |
| `LINE_COUNT_THRESHOLDS` (standard) | `(250, 350)` | Expected output line range (~75–87 clusters) |

`run_brutus_hierarchical_only_mac_gold_standard.py` exposes `ICS_PER_RUN = 1000` (max ICs per invocation for the gold-standard run).

The output-validation logic in both runners checks that the final timestep reaches a `time_threshold` of `9.5` (i.e., simulation completed to near `t_end=10`).

---

## 5. Brutus Build Configuration (`brutus_Newton-main/makefile`)

Brutus is a C++ N-body integrator with arbitrary-precision arithmetic via GMP (`libgmp`, `libgmpxx`) and MPFR (`libmpfr`).

### 5.1 Build environment (paths)

| Variable | Default value | Purpose |
|---|---|---|
| `BREW_PREFIX` | `/opt/homebrew` | Homebrew prefix (M2 Mac default) |
| `HOME_DIR` | `<home>` | Home directory containing `src/mpreal` |
| `MPRLIB` | `$(HOME_DIR)/src/mpreal` | Path to the `mpreal` MPFR C++ wrapper library |
| `INCLUDE_DIRS` | `-I$(BREW_PREFIX)/include -I$(MPRLIB)` | Include paths |
| `LIB_DIRS` | `-L$(BREW_PREFIX)/lib` | Library link path |

> The current `makefile` is hard-wired to `<home>/...`. For a non-M2 or non-Homebrew environment, the file must be edited. (There is no `makefile.original` in the tree — only `makefile` — so keep a copy of the current file before editing if you need an upstream-default reference.)

### 5.2 Compiler settings

| Variable | Value | Notes |
|---|---|---|
| `COMP` | `g++` | C++ compiler |
| `CFLAGS` | `-O3 -std=c++11 -DMPFR_USE_NO_MACRO -DMPFR_USE_INTMAX_T` | Optimization, language standard, MPFR macro-safety defines |
| `EXE` | `brutus` | Output binary name |

### 5.3 Linkage

The final link step is:

```makefile
$(CO) brutus main.o Brutus.o Bulirsch_Stoer.o Cluster.o Star.o Data_Handler.o Timer.o $(LIB_DIRS) -lgmpxx -lgmp -lmpfr
```

Required system libraries: `libgmpxx`, `libgmp`, `libmpfr`. Brutus cannot be built without these (or the `mpreal` headers in `$(MPRLIB)`).

### 5.4 Build targets

| Target | Effect |
|---|---|
| `make` (default) / `make all` | Builds the `brutus` executable |
| `make clean` | Removes object files, `brutus` binary, `*~`, `ccache/`, `.fuse*` |

### 5.5 Source files

| Object | Source | Notes |
|---|---|---|
| `main.o` | `main.cpp` | Entry point |
| `Brutus.o` | `Brutus.cpp` / `Brutus.h` | Top-level integrator class |
| `Bulirsch_Stoer.o` | `Bulirsch_Stoer.cpp` / `Bulirsch_Stoer.h` | Bulirsch–Stoer extrapolation integrator |
| `Cluster.o` | `Cluster.cpp` / `Cluster.h` | N-body cluster abstraction |
| `Star.o` | `Star.cpp` / `Star.h` | Single body |
| `Data_Handler.o` | `lib/Data_Handler/Data_Handler.cpp` / `lib/Data_Handler/Data_Handler.h` | I/O and output formatting |
| `Timer.o` | `lib/Timer/Timer.cpp` / `lib/Timer/Timer.h` | Timing utilities |

---

## 6. Required vs. Optional Settings (Summary)

| Setting | Layer | Behavior if missing |
|---|---|---|
| `IC_RAW_DIR` env var | Pipeline | **Runtime error** — `stage2_prescreening_revised_auto.py` and `ic_generation_utils.py` raise `RuntimeError` at startup |
| Brutus build (g++, GMP, MPFR, mpreal headers) | Brutus build | Build fails with linker errors (`-lgmpxx -lgmp -lmpfr` not found) |
| Brutus executable at `brutus_Newton-main/brutus` | Pipeline | Brutus runners fail when they call `subprocess` on the missing binary |
| Framework specs (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) | Methodology | Training pipeline has no authoritative methodology reference |
| Prescreening / Brutus / metrics Python scripts | Pipeline | Pipeline stage fails immediately when run |

There is no centralized config-validation step. Each stage's Python script reads its own constants and `IC_RAW_DIR` directly.

---

## 7. Per-Environment Overrides

There is no `NODE_ENV`-style mechanism, no `.env.development` / `.env.production` split, and no per-environment config file. The repo is a research project with a single canonical pipeline.

The only environment override for the simulation pipeline is the `IC_RAW_DIR` env var, which is read at runtime by both `ic_generation_utils.py` and `stage2_prescreening_revised_auto.py`. To point the pipeline at a different raw-IC location, export the variable before invoking the relevant stage. (The v2.0 trainex training code adds `GSD_DATA_ROOT` / `GSD_ALLOW_PARTIAL_DATA_ROOT`; see §3.1.)

The `makefile` path variables (`BREW_PREFIX`, `HOME_DIR`, `MPRLIB`) are also environment-overridable in principle (they are `make` variables, not environment variables), but the file currently has hard-coded absolute paths and no conditional logic. Any build on a non-M2 or non-`<home>` host requires editing the `makefile`.

---

## 8. See also

- `docs/runbooks/` — operational procedures (migration, EDL, etc.)
- `pinn_instruction/markdown_conversion/framework-specs/` — authoritative methodology specs
- `.planning/REQUIREMENTS.md` — requirements and scope rules
- `AGENTS.md` — agent operating instructions and STOP protocol
