# Specs Bundle — Issue 02 (Derived Artifact)

Build date: 2026-06-11. This file is a packaging artifact: the original spec
snapshot files in `research_package/specs/` govern. Content between BEGIN/END
delimiters is byte-identical to the originals (SHA-256-verified at build time).

## Contents

| File | Bytes |
|------|-------|
| `02-data-pipeline-and-validation.md` | 29,548 |
| `ctl_instruction.md` | 68,520 |
| `data_quality_assessment.md` | 29,983 |
| `pinn_architecture.md` | 56,675 |
| `sampling_method.md` | 22,236 |

===== BEGIN FILE 02-data-pipeline-and-validation.md =====
# 02 — Data Pipeline and Validation

## Executive Summary

This document consolidates all identified findings, critical issues, and open decisions related to the data processing pipeline, validation protocol, and file-format handling across the three-body PINN training stack. Source material is drawn from the 2026-04-27 comprehensive technical audit, the Issue on Data Validation Protocol, the Causal Training Mismatch resolution blueprint, and cherry-picked unique content from `next steps.txt` and `next-step-for-data-processing-pipeline.txt`.

The pipeline spans four stages: (1) IC generation via Sobol quasi-random and hierarchical sampling, (2) prescreening via short leapfrog integration to reject unstable configurations, (3) Brutus high-precision integration using the Bulirsch-Stoer method with GMP/MPFR arbitrary-precision arithmetic, and (4) metrics extraction for energy, momentum, and angular momentum conservation. The processed data feeds the PINN training loop through a DataLoader that must handle non-contiguous IDs, blacklist filtering, gold-standard subset gaps, snapshot completeness validation, and cross-folder parameter heterogeneity.

**Readiness assessment:** Two critical blockers (B-06 missing validation gate, B-11 non-contiguous ID handling) plus several major inconsistencies must be resolved before training can proceed. The pipeline produces correct physics — but the gap between pipeline output and training input is unbridged.

### Temporal Resolution Bridging

The pipeline produces Brutus outputs at three discrete `dt_out` values: 0.01 (gold-standard, high resolution, ~1000 snapshots per trajectory), 0.08 (hierarchical base, medium resolution, ~125 snapshots), and 0.17 (standard quasi-random base, low resolution, ~59 snapshots). This 17x variation in temporal resolution creates a fundamental challenge for the PINN training loop:

1. **Collocation density mismatch:** A uniform collocation point count applied across all trajectories gives low-resolution data effectively 17x fewer points per unit of physical time than high-resolution data — the network gets systematically less constraint in physical regions dominated by low-resolution trajectories.
2. **SASD floor effect:** Stiffness-Aware Sampling Density is computed on available snapshots. In low-resolution trajectories, rapid close encounters may span only 1-2 sample points, making the SASD metric blind to interior stiffness spikes.
3. **Stage boundary artifacts:** Curriculum stages are assigned from invariants computed on ICs alone, but the `dt_out` variation means a Stage-k trajectory at high resolution contains radically different training information than the same stage at low resolution.

**Resolution approach** (per audit M16): supplemental collocation points per trajectory should scale as `dt_base / dt_out`, where `dt_base=0.01` is the high-resolution baseline. Gold trajectories get 1× supplemental collocation, hierarchical base trajectories get 0.125×, and standard base trajectories get ~0.059×. This concentrates collocation density on high-resolution trajectories where the underlying dynamics are best resolved. The DataLoader must expose per-trajectory `dt_out` metadata so the batch constructor can adapt. See also M16 in the findings table below. <!-- Reverted to audit M16 line 163 verbatim: n_col_per_traj = base_n_col * (dt_base / dt_out). The earlier inverted form misread the audit's data-aware-density intent. -->

---

## Decisions Requiring Human Approval

> These items require explicit human approval before implementation. Items tagged CRITICAL alter the locked framework methodology.

### [ROUTINE] D-03 — Processed training data format (HDF5 vs .npy vs txt/json)

**Status:** Awaiting human approval
**Source:** issues/02-data-pipeline-and-validation.md, "Open Decisions" section
**Conflict with current SOT:** No — the SOT already recommends HDF5/.npy

What the SOT says today:
- `ctl_instruction.md` Step 1 item 6 explicitly recommends HDF5 or .npy for processed training data.
- `data-processing-pipeline-full.py` already implements HDF5 output.
- The SOT does not specify txt/json as an alternative — that question was raised only in the issue doc.

What is being asked:
- Confirm HDF5 as the primary format, with .npy as acceptable alternative per the SOT, and optionally add JSON export for inspection only.

Options on the table:
- Option A: Keep HDF5 as primary (matches SOT and current implementation).
- Option B: Add .npy as acceptable alternative (matches SOT's "HDF5 or .npy" recommendation).
- Option C (supplemental): Add optional JSON export for inspection and debugging only — not for training.

Why this needs YOU (the framework owner):
- Methodology impact: zero. This is a storage format decision that does not alter any methodology. The SOT already recommends HDF5/.npy. The only new element is the optional JSON export for human inspection, which is additive and non-breaking.

Cross-link: see [Open Decisions](#open-decisions) for full rationale.

## Confirmed Findings

### BLOCKING (Must resolve before training)

| ID | Severity | Finding | Location | Fix |
|----|----------|---------|----------|-----|
| B-06 | **BLOCKING** | No validation gate between Stage 4 (metrics) and Stage 5 (training). `calculate_metrics.py` processes ALL Brutus files including partial/errored runs. The only validity signal (`final_timestep >= 9.5`) runs at Stage 3 runner scripts, never re-validated at DataLoader init. | `README.md` lines 677-678; CTL Stage 4→5 gap | Insert `TrajectoryValidator` at DataLoader init: enforce `snapshot_count >= 200` for Stage 4+, `>= 2` for Stage 0-3, AND `final_timestep >= 9.5`. Log rejections. |
| B-11 | **BLOCKING** | Non-contiguous IDs break curriculum mapping. Standard dataset: 1,250 gaps out of 4,000 (31.2% gap rate). Hierarchical: 143/5,000 (2.9%). CTL assumes ID == array index. | `README.md` lines 148-153; CTL stage assignment logic | Build `id_to_path` dictionary from actual on-disk filenames at DataLoader init. `TrajectoryIndex` class with `get_by_id(file_id)` method. Never assume ID == index. |
| M11 | **BLOCKING** | Blacklist (`problematic_ics_blacklist.json`, 65 IDs) not loaded by current runners or DataLoader. Blacklisted ICs can silently enter training. *(Re-classified from audit MAJOR to BLOCKING for this consolidation: the DataLoader cannot ship with silently-corrupted training data.)* | `README.md` line 1011 | Load blacklist in DataLoader `__init__` and exclude. Log exclusion count. |
| M12 | **BLOCKING** | Standard trajectories (dt_out=0.17, ~59 snapshots) cannot support 32 points/trajectory (54% sampling ratio). The CTL batch spec assumes 32 points but standard trajectories don't have enough snapshots. *(Re-classified from audit MAJOR to BLOCKING for this consolidation: 54% sampling is infeasible and blocks batch construction.)* | `README.md` dt_out table; CTL Sec 5.3.2 | Adaptive cap: `n_pts = min(32, int(0.5 * n_snapshots))`. For standard: ~29 points. |
### MAJOR (Degrades correctness)

| ID | Severity | Finding | Resolution Strategy |
|----|----------|---------|---------------------|
| M13 | MAJOR | 184 standard IDs have no gold counterpart — Stage 5 training data is incomplete for these IDs. Placed in MAJOR rather than BLOCKING: gold-standard data is a quality upgrade, not a hard prerequisite for training. Training can proceed with standard-fidelity fallback. | Check gold counterpart existence before Stage 5 assignment. Skip to Stage 6 if no gold data, or use low-fidelity standard fallback with warning flag. |
| D7 | MAJOR | 219 standard gold files have minimal footers (no tol parameter). Folder default is tol=1e-13 but 592 files in the same folder have tol=1e-14. | Use folder-level default 1e-13. Add `tol_confidence` flag: 'direct' (footer has tol) vs 'inferred' (minimal footer). Log count of inferred tolerances. |
| — | MAJOR | `dt_out` heterogeneity (M16): collocation density is uniform across 17× dt_out range. Resolution and canonical ownership live in `03-curriculum-and-training-loop.md` MAJOR table (training loop is the implementer of dt_out-aware collocation scaling). | See M16 in 03. |
| — | MAJOR | Brutus output files use two different parameter sets within the same folder. Footer schema varies — some files omit `eta`, a small subset of standard-quasi-random gold omit both `eta` and `tol`. | Prefer actual `Result:` values when present. Fall back to folder defaults when absent. Treat footer as metadata only — completeness gate uses final timestamp, not footer presence. |

### Severity Reclassification Ledger

The 2026-04-27 audit classified M11 and M12 as MAJOR. This consolidation intentionally reclassifies them as BLOCKING for the data-loading phase:

| ID | Audit Severity | Consolidated Severity | Rationale |
|----|----------------|-----------------------|-----------|
| M11 | MAJOR | BLOCKING | A DataLoader that can silently admit blacklisted ICs would corrupt training data at ingestion time. |
| M12 | MAJOR | BLOCKING | The documented 32-points-per-trajectory batch contract is infeasible for standard trajectories with ~59 snapshots unless adaptive capping is implemented. |

### MINOR / INFO

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| — | INFO | Result footer paths can be macOS or Windows style and reference multiple IC folders. Do not use them as authoritative mapping. | Use numeric ID-to-path mapping from filesystem, not footer paths. |
| — | INFO | Standard gold provenance: no runner script in repo. Treat provenance as partial unless recovered from external logs. | Document the provenance gap; don't block execution on it. |

---

## Pipeline Validation Gaps (G1-G6) Synthesized from Audit Findings

**Source:** Audit B-06, B-11, M11, M12/M16, M13. This table is audit-derived and uses the archived `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` §2 only as framing context; it is not a literal restatement of that document's original six pre-agent gaps. G6 is added for the causal-training architectural decision.

The following six pipeline validation gaps between the documented validation protocol and what the CTL-PINN training framework actually requires are synthesized from audit findings (G1-G5) plus the causal-training architectural decision (G6):

<!-- Section retitled and source citation rewritten: G1–G5 are audit findings (B-06, B-11, M11, M12/M16, M13), not items literally enumerated in the validation-protocol issue's §2. -->

| Gap | Description | Resolution Status |
|-----|-------------|-------------------|
| G1 | No trajectory-completeness gate between metrics and training | **Open** — addressed by B-06 TrajectoryValidator |
| G2 | Non-contiguous ID handling assumed but not implemented | **Open** — addressed by B-11 TrajectoryIndex |
| G3 | Blacklist not loaded at training time | **Open** — addressed by M11 fix |
| G4 | Gold-standard subset gaps not handled (184 missing standard IDs) | **Open** — addressed by M13 fix |
| G5 | dt_out heterogeneity not accounted for in batch construction | **Open** — addressed by M12/M16 fixes |
| G6 | Causal training mismatch not resolved — Option A vs Option B framing | **Open** — surfaced as an open decision in `03-curriculum-and-training-loop.md` |

Gaps G1-G5 are pipeline-level issues with clear technical fixes described in the audit. Gap G6 is an architectural decision that spans the data pipeline (DataLoader must support whatever training mode is chosen) and the training loop; it is flagged in `03-curriculum-and-training-loop.md`.

---

## Validation Threshold Clarifications

**Source:** `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` §5.

Three minor validation-protocol clarifications are preserved here so future agents do not have to recover them from the archive:

| Clarification | Consolidated Guidance |
|---------------|----------------------|
| Overfit Challenge precision | Treat `<1e-6` as a diagnostic overfit challenge on a small controlled subset in scaled units, not as the production curriculum advancement threshold. Production stage progression should follow the CTL thresholds in `03-curriculum-and-training-loop.md` (Stage 0 starts at `epsilon_phys = 5e-3`; late stages tighten toward `1e-4`) unless a human reviewer explicitly changes them. |
| Input vector dimensionality | Use the 14D contract in `01-architecture-and-physics-foundations.md`: normalized time plus a 13-component IC vector. Older 12D/11D statements are superseded documentation defects. |
| Gold-standard validation thresholds | Gold-standard data (`dt_out=0.01`) is not assumed to pass automatically. Apply the same completeness and conservation gates, then record stricter/variant-specific threshold decisions explicitly. Gold resolution reduces SASD risk, but SCS/IPR still detect integrator drift and interpolation residuals. |

---

## Validation Metrics as Live Training Parameters

**Source:** `Causal_Trainingmismatch_resolution_blueprint.md`

The four pre-training data quality metrics must transition from static diagnostic flags into fundamental, governing parameters of the training loop:

### Symplectic Conservation Score (SCS)

Measures the maximum normalized deviation of the Hamiltonian over the trajectory duration. In the updated framework, SCS serves as the primary, non-negotiable filter against Brutus integration errors BEFORE data enters the ALM.

- **Phase 1 screening:** Any trajectory with `SCS > 1e-6` must be outright rejected during static pre-screening
- **Stage 5 tightening:** For high-resolution chaotic-orbit data (dt=0.01), threshold tightens to `SCS < 1e-8`
- **Rationale:** The ALM explicitly incorporates an energy regularizer. Feeding it data with intrinsic integration drift creates an unsolvable optimization paradox — the network is penalized for not conserving energy that the ground truth itself doesn't conserve

Computed using the unsoftened static epsilon (ε = 1e-10):

```
SCS = max_t |H(t) - H(0)| / |H(0)|
```

### Stiffness-Aware Sampling Density (SASD)

Quantifies the ratio of discrete time step to local characteristic timescale:

```
SASD_i = Δt_i * ||a(t_i)|| / ||v(t_i)||
```

**If max SASD exceeds a critical threshold** for a low-resolution trajectory, the trajectory turns significantly between data points. Such data must be flagged and resampled at higher resolution (dt=0.01).

**During training:** Collocation point sampling probability is weighted by the SASD profile — points in high-curvature regions get more collocation samples, ensuring ALM penalty multipliers apply strongest constraints where they're most needed.

### Interpolation Physics Residual (IPR)

Evaluates whether the continuous manifold implied by discrete data points satisfies Newton's laws. Tests a piecewise Cubic Hermite Interpolating Polynomial against the equations of motion.

**Updated role:** The IPR establishes the theoretical lower bound (noise floor) for the ALM physics penalty. Computed using the network's dynamic softening constant (ε = 1e-5):

```
IPR = (1/M) * Σ |d²q_spline/dt²(τ_k) - F_gravity^{ε=1e-5}(q_spline(τ_k))|²
```

If the network's physics loss drops below the pre-calculated IPR, the SIREN has discovered a more physically accurate continuous trajectory than spline interpolation can provide. At this threshold, ALM halts increases to the penalty parameter μ_p.

### Phase Space Coverage Entropy (PSC)

Computes Shannon entropy of data points across a discretized phase space grid, quantifying training data diversity. **Governs the curriculum replay mechanism:** trajectories are sampled inversely proportional to their phase space bin density, ensuring extreme high-stiffness events (s_min < 0.5) are consistently over-represented in mini-batches.

---

## File Format: h5 vs txt/json

**Source:** `next-step-for-data-processing-pipeline.txt`

The current pipeline stores processed data in HDF5 (`.h5`) format via `data-processing-pipeline-full.py`. The format question was raised: should the training data store migrate to `.txt` or `.json` for easier extraction and inspection?

**HDF5 advantages:**
- Hierarchical dataset organization (natural fit for trajectory groups, stage strata, and per-trajectory arrays)
- Zero-copy reads into NumPy/PyTorch tensors — no parsing overhead at training time
- Compression (gzip/lzf) reduces storage for ~15K trajectories with hundreds of snapshots each
- Industry standard for scientific computing and deep learning datasets

**txt/json advantages:**
- Human-readable and inspectable without specialized tools
- No HDF5 library dependency
- Easier to version-control individual trajectories

See Open Decisions below for the callout.

---

## Brutus Output Handling

### Footer/Mass Drift Protocol

**Source:** Audit B-06, D6

Brutus outputs are parsed as text from the integrator's stdout. Key structural notes:

1. **Completeness gate:** `final_timestamp >= 9.5` is the mandatory rule. Do not rely on `Result:` footer presence — many files omit it.
2. **Footer schema variance:** Files can omit `eta`, `tol`, or both. Use folder defaults as fallback (see D7 above).
3. **Mass drift check:** Brutus arbitrary-precision arithmetic should preserve masses exactly, but text output may round. Protocol: parse 1000 IC-Brutus pairs, compare `m_IC` vs `m_Brutus_t=0` with `np.allclose(rtol=1e-15)`. If mismatch: use `decimal.Decimal` for mass parsing. If match: document IC masses as canonical.
4. **OS-dependent paths:** Result footer paths may be macOS or Windows style. Never use as authoritative mapping — use numeric ID from filesystem.
5. **Parameter heterogeneity:** Multiple tol, Lw values exist within the same folder. Prefer actual `Result:` values when present.

### Precision Handling in Validation

**Source:** `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` (Gap 5), Audit D6

Brutus output files contain 30-40 significant digits of precision, rendered as text. The validation pipeline operates in double-precision floating point (`float64`). This loss of precision is acceptable for validation metrics — the Brutus convergence tolerance is typically 1e-13 to 1e-15, so `float64` (relative precision ~1e-16) preserves approximately 1-3 guard digits beyond the Brutus tolerance.

**When arbitrary precision is needed:** For mass consistency verification between IC and Brutus output, parse the t=0 snapshot masses with `decimal.Decimal` for exact comparison. If masses match to 1e-15 relative tolerance in float64, document IC masses as canonical and use float64 throughout. If mismatch is detected due to text rounding, retain `Decimal` parsing for mass values specifically — masses are only 3 scalars per trajectory, so the overhead is minimal.

**Validation code constraint:** All validation metrics (SCS, SASD, IPR, PSC) run on CPU in `float64` before data reaches the GPU training loop. The dual-epsilon strategy (see `01-architecture-and-physics-foundations.md`) means validation uses static eps=1e-10 while training uses dynamic eps_soft=1e-5 — validation metrics evaluate true Newtonian fidelity, not the regularized physics the network actually trains on.

### Global Scale Computation

**Source:** `next steps.txt` (Issue 17, cherry-picked unique content)

The `compute_globals` function must process all IC files across the entire dataset to derive median-based scales:

```python
def compute_globals(ic_files, t_max=10.0, G=1.0, eps=1e-10):
    N = len(ic_files)
    all_E = np.zeros(N)
    all_r_char = np.zeros(N)
    
    M_tot_ref = 3.0
    D = np.cbrt(G * M_tot_ref * t_max**2)  # Corrected B-02 scale: D = 6.694 for G=1, M_tot=3, T=10
    V = D / t_max
    
    for j, filename in enumerate(ic_files):
        m, r_raw, v_raw = parse_ic_file(filename)
        r_prime = r_raw / D
        v_prime = v_raw / V
        
        # Compute E (scaled) using static epsilon
        T = np.sum(0.5 * m * np.sum(v_prime**2, axis=1))
        V_pot = 0.0
        for i in range(3):
            for k in range(i+1, 3):
                r_ik = np.linalg.norm(r_prime[i] - r_prime[k]) + eps
                V_pot -= m[i] * m[k] / r_ik
        all_E[j] = T + V_pot
        
        # Compute r_char (scaled)
        pairwise = [np.linalg.norm(r_prime[i] - r_prime[k]) for i in range(3) for k in range(i+1, 3)]
        all_r_char[j] = np.mean(pairwise)
    
    E_scale = np.abs(np.median(all_E)) + 1e-8
    smin_scale = np.median(all_r_char)
    
    return {'E_scale': E_scale, 'smin_scale': smin_scale, 'Q_scale': 0.5}
```

**Note:** The code above is the corrected B-02 form. Older source snippets used `D = cbrt(G * t_max^2)`, which gives D ≈ 4.64 and omits `M_tot=3`. The `compute_globals` function must be re-run with corrected D = cbrt(G * M_tot * t_max^2) = 6.694.

---

## Open Decisions

> **[DECISION-NEEDED]** File format for processed training data: keep HDF5 (`.h5`) or migrate to text/JSON (`.txt`/`.json`)?
>
> **Option A — Keep HDF5:**
> - Pros: Zero-copy tensor loading, built-in compression, hierarchical grouping natural for trajectory stages, industry standard for ML datasets
> - Cons: Requires `h5py` dependency, not human-readable without tools
> - Current state: already implemented in `data-processing-pipeline-full.py`
>
> **Option B — Migrate to txt/json:**
> - Pros: Human-readable, no specialized library needed, version-control friendly
> - Cons: Parsing overhead at training time (~10-100× slower than HDF5 reads), larger storage (no compression), no hierarchical grouping — would need directory conventions to replace HDF5 groups
>
> **Recommendation:** Keep HDF5 for the training data store (performance-critical path). Add an optional JSON export mode for inspection and debugging, but do not replace the primary format. This gives both speed (training) and inspectability (debugging).
>
> **Resolve before finalizing the DataLoader implementation.**

---

## Recommended Resolutions

1. **P1-1 — Implement TrajectoryValidator:** Snapshot-count gate (≥200 for Stage 4+), final-timestamp gate (≥9.5), blacklist exclusion. Insert between metrics loading and batch construction.
2. **P1-2 — Build TrajectoryIndex:** `id_to_path` dictionary from actual filesystem filenames. `get_by_id(file_id)` method. Never assume dense linear indexing.
3. **P1-3 — Load and enforce blacklist:** Load `problematic_ics_blacklist.json` at DataLoader init. Log exclusion count. Fail loudly if a blacklisted ID appears in a batch.
4. **P1-4 — Adaptive points-per-trajectory:** `n_pts = min(32, int(0.5 * n_snapshots))` for standard trajectories (~29 points for dt_out=0.17).
5. **P1-5 — Gold counterpart check:** Before Stage 5 assignment, verify gold counterpart exists. If missing: skip to Stage 6 or flag for low-fidelity fallback.
6. **P1-6 — SASD-weighted collocation:** Use stiffness profile to weight collocation point sampling density.
7. **P1-7 — Recompute global scales with corrected D=6.694:** Rerun `compute_globals` after D fix. Update all E_scale, smin_scale values.
8. **P1-8 — Add dt_out-aware collocation scaling:** Scale supplemental `n_col_per_traj` proportional to `dt_base / dt_out`: `n_col = base_n_col * (dt_base / dt_out)`. For dt_base=0.01: gold gets 1×, hierarchical base gets 0.125×, standard base gets ~0.059×. Adjust `base_n_col` to meet total collocation budget (~10,000-50,000 points per batch). <!-- Reverted to audit M16 line 163 verbatim form. -->
9. **P2-1 — Add tol_confidence flag:** 'direct' vs 'inferred' for files with minimal footers. Log count of inferred tolerances during DataLoader init so training logs provide full provenance.
10. **P2-2 — Batch-verify 100 IC-Brutus mass pairs:** Compare `m_IC` vs `m_Brutus_t=0` with `np.allclose(rtol=1e-15)`. If mismatch: use `decimal.Decimal` for mass parsing. If match: document IC masses as canonical.

**Verification checklist after resolutions are implemented:**
- [ ] `TrajectoryValidator` rejects at least one known-incomplete trajectory in unit test
- [ ] `TrajectoryIndex.get_by_id()` returns correct path for 10 randomly selected gapped IDs
- [ ] Blacklist load produces exactly 65 excluded IDs
- [ ] Adaptive n_pts: standard trajectory with 59 snapshots gets n_pts=29; gold with 1000 snapshots gets n_pts=128
- [ ] Gold counterpart check logs exactly 184 missing IDs for standard quasi-random
- [ ] Global scales are recomputed and differ from current values by amounts consistent with D=4.64 to D=6.694 correction
- [ ] Tol confidence: at least 219 standard gold files have 'inferred' flag; hierarchical gold files have 'direct' flag

---

## Dataset Inventory and Key Parameters

### Dataset Variants

| Variant | IC Count | Brutus Output Count | dt_out (typical) | tol (typical) | Notes |
|---------|----------|---------------------|------------------|---------------|-------|
| Hierarchical | ~5,000 | ~4,857 | 0.08 (base), 0.01 (gold) | 1e-15 (base), 1e-13 (gold) | Near-planar, small inclinations, COM perturbed |
| Standard quasi-random | ~4,000 | ~2,749 (base), ~2,565 (gold) | 0.17 (base), 0.01 (gold) | 1e-13 | Full 3D, exactly equal masses, COM=0 by construction |

**Key anomalies:**
- Hierarchical COM is NOT zero after Gaussian perturbation (|COM| ~ 9e-3) — see `01-architecture-and-physics-foundations.md` COM frame section
- 184 standard IDs have no gold counterpart — these cannot enter Stage 5 training
- ID gaps are intentional (generation continuation, prescreen rejection, failed Brutus runs) — linear indexing produces wrong mappings
- Gold standard quasi-random folder has 2,565 files vs 2,749 in base IC folder

### Pipeline Stage Checklist

| Stage | Input | Processing | Output | Validation |
|-------|-------|------------|--------|------------|
| 1 — IC Generation | Sobol sequences / orbital elements | `generate_ics.py` | IC text files (3 lines, mass+pos+vel) | IC_RAW_DIR set, files written |
| 2 — Prescreening | IC files | Short leapfrog integration (TMAX=1.0, DT=0.0001) | Filtered IC list | Energy error < 0.01, min distance > 0.01 |
| 3 — Brutus Integration | Filtered ICs | Bulirsch-Stoer with GMP/MPFR | Brutus output files (snapshot format) | timeout=3000s, final_timestep >= 9.5 |
| 4 — Metrics | Brutus outputs | `calculate_metrics.py` | JSON metrics per trajectory | Energy, momentum, angular momentum drift |
| **GAP** | — | **TrajectoryValidator (NOT YET IMPLEMENTED)** | — | snapshot_count, completeness, blacklist |
| 5 — PINN Training | Validated trajectories | DataLoader → SQR-SkipResNet-SIREN | Trained model | Training loss, validation metrics |

The gap between Stage 4 and Stage 5 is the most critical pipeline deficiency — see B-06 above.

---

## DataLoader Requirements (Implementation Spec)

The DataLoader is the bridge between the Brutus output filesystem and the PINN training loop. It must handle all of the following:

1. **ID resolution:** Build `id_to_path` dict by scanning all Brutus output folders. Never assume dense linear indexing.
2. **Completeness gate:** For each trajectory, verify `final_timestamp >= 9.5` AND `snapshot_count` meets stage minimums.
3. **Blacklist exclusion:** Load `problematic_ics_blacklist.json` at init. Skip blacklisted IDs. Log count.
4. **Gold counterpart check:** For Stage 5+, verify gold data exists. Use `standard_quasi_random_ids_not_in_gold.md` exclusion list.
5. **Mass/time parsing:** Parse with `decimal.Decimal` for exact precision when needed; `float64` sufficient for most use cases.
6. **IC-to-Brutus mapping:** Match by numeric ID. File names do not encode "gold" — the folder defines the variant.
7. **Footer handling:** Parse `Result:` when present for tol/eta metadata. Fall back to folder defaults when absent. Never fail on missing footer.
8. **Stage-aware sampling:** Support `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)` queries for CTL batch construction.
9. **SASD profile caching:** Pre-compute stiffness profiles during init for collocation weighting.
10. **COM transform:** Apply unified COM transformer (per `01-architecture-and-physics-foundations.md`) during data loading, not during preprocessing.

---

## References

- [01-architecture-and-physics-foundations.md](01-architecture-and-physics-foundations.md) — 14-D input vector spec (data pipeline must produce this); COM frame transformation (validation must apply same transform); normalization formulas table (canonical location); dual-epsilon strategy (validation uses static eps=1e-10, training uses dynamic eps=1e-5).
- [03-curriculum-and-training-loop.md](03-curriculum-and-training-loop.md) — Stage assignment criteria (pipeline outputs stage labels); SCS/SASD/IPR/PSC as live training parameters (data side feeds training loop); replay/lookahead batch construction (DataLoader must support stage queries).
- [Canonical: Dataset Documentation](../../simulation_data/Documentation/README.md) — Authoritative dataset spec, anomalies, dt_out per variant, completeness rules. Do NOT duplicate content from here.
- [Canonical: data-processing-pipeline-full.py](../../pinn/data-processing-pipeline-full.py) — Current IC vector assembly and staging logic.
- [Canonical: calculate_metrics.py](../../simulation_data/Scripts/metrics_calculation/calculate_metrics.py) — Conservation metrics extraction.

---

*End of 02-data-pipeline-and-validation.md*

*This document synthesized from 7 source files archived in `archive/`. See `MIGRATION.md` for per-section provenance.*

===== END FILE 02-data-pipeline-and-validation.md =====

===== BEGIN FILE ctl_instruction.md =====
---
author:
- Starlordpd233
date: June 2025
title: Final CTL Instruction on Training PINNs for the Three-Body
  Problem
---

# Important Note

This instruction details the curriculum learning framework for training
a specific type of PINN designed for this research that focuses on the
three-body problem. For any information regarding the architecture and
structure of the neural network, please refer to the
`PINN_architecture_plan.tex` file.

# Characterizing and Organizing the Multi-Fidelity Simulation Data

## Existing Training Dataset

<a id="tab:brutus_compare"></a>

| Parameter | Dataset/Number of Files | IC Type | tolerance | Word Length | dt out | Temporal Density Increase |
|---|---|---|---|---:|---:|---|
| **Original** | Set 1a (4857) | Hierarchical | $1\text{e-}15$ | 130 | 0.08 | Baseline (1x) |
|  | Set 1b (4857) | Standard | $1\text{e-}13$ | 118 | 0.17 | Baseline (1x) |
| **New** | Set 2a (2749) | Hierarchical | $1\text{e-}13$ | 130 | **0.01** | **8x** |
|  | Set 2b (2565) | Standard | $1\text{e-}13$ | 130 | **0.01** | **17x** |

*Table `tab:brutus_compare`: Comparative Analysis of BRUTUS Training Datasets. The new dataset provides a dramatic 8-fold to 17-fold increase in the temporal resolution of the ground-truth trajectories.*

For **Set 1a Hierarchical**, 5000 raw ICs were generated; **Set 1b
Standard**, 4000. For both types of ICs, **Set 2a Hierarchical** and
**Set 2b Standard**, the same number of ICs were used. However, these
are just the raw ICs. The actual number of IC files left are subject to
the prescreening result. Furthermore, the number of BRUTUS output files
are even less due to the computational limitation. The final number of
BRUTUS output files are in the above table -- for each set, it is the
same number for both the IC files and the BRUTUS output files. In total
there were 15,028 pairs of IC and BRUTUS output files generated for
training data, ready to be parsed in the next stage for preparing this
training data.

## Multi-Fidelity Dataset and Physical Invariants

A robust training dataset is crucial for PINNs on the three-body
problem. We utilize two complementary sources of simulated trajectories:
(1) High-fidelity "hierarchical" simulations, and (2) Lower-fidelity
"quasi-random" simulations. The hierarchical dataset consists of
stable three-body configurations (a tightly bound binary with a distant
tertiary companion) generated with a small time step ($dt \approx 0.08$)
for high precision. The quasi-random dataset covers a broad variety of
chaotic configurations generated by random initial conditions (using
Sobol quasi-random sampling for good coverage) and integrated with a
larger time step ($dt \approx 0.17$) for efficiency. All simulations are
done with the Brutus N-body integrator - a high-precision solver - but
the second dataset, being more random, is considered "low-fidelity"
due to slightly lower precision and more chaotic behavior. Each
simulation's initial conditions determine the system's characteristics.
We compute five key physical invariants or properties from the initial
state of each simulation, which serve as quantitative difficulty
metrics:

- **Total Mechanical Energy ($E$):** The sum of kinetic and potential
  energy of the system. $E<0$ indicates a bound (stable) system, with
  more negative $E$ meaning a deeper gravitational well (tighter
  binding). Values near zero indicate marginally bound or unbound
  systems which tend to be more chaotic. (Bound systems satisfy $E<0$;
  as a guideline, "Stage 0" easiest cases have $E<-0.5$ in normalized
  units.)

- **Total Angular Momentum Magnitude ($L$) and $L/L_{\max}$:** $L$ is
  the magnitude of the total angular momentum vector. We often normalize
  it by $L_{\max}$, the theoretical maximum angular momentum for the
  system's energy (which corresponds to all mass moving on a circular
  orbit for that energy). A high $L/L_{\max}$ (close to 1) means
  near-circular orbits (stable); a low ratio means elongated or radial
  orbits that lead to closer encounters and chaos. (For example, Stage 0
  requires $L/L_{\max}>0.5$ - reasonably high angular momentum.)

- **Virial Ratio (Q):** The ratio $2T/|V|$ of twice the total kinetic
  energy to the absolute potential energy at $t=0$. For bound stable
  systems in virial equilibrium, $Q \approx 1$. Significant deviations
  (too low or high) imply an imbalance (e.g. too much kinetic energy or
  too much potential energy) that can lead to expansion or collapse.
  Moderate ranges around 1 indicate stability (Stage 0 uses
  $0.7 \le Q \le 1.3$ as a criterion).

- **Minimum Initial Separation ($s_{\min}$):** The smallest distance
  between any two bodies in the initial configuration. A larger
  $s_{\min}$ means the bodies are well separated initially, reducing the
  chance of immediate close encounters. Very small initial separations
  (two bodies almost colliding at $t=0$) indicate extremely challenging
  cases that can cause numerical difficulties and chaotic scattering.
  Stage 0 imposes $s_{\min}>2$ (in code units) to avoid any incipient
  close approaches.

All data is normalized to dimensionless code units for training (e.g.,
positions and distances scaled by a characteristic length, velocities by
a characteristic orbital velocity) to keep values typically in $[-1,1]$.
A consistent normalization is applied across the entire dataset, which
aids network training by ensuring inputs and outputs are on comparable
scales.

## Multi-Stage Data Stratification by Difficulty (Revised to handle the issue that virial ratio is not preserved for quasi-random IC sampling)

> **Author note:** I have a suggestion: how about we give the entire IC files a scan
> using some algorithms and analyze the gathered data from there, to first
> get an insight on what the data looks like, and then we can decide on
> the criteria for each stage? This will be a good starting point
> considering that simply designing the criteria based on theoretical
> values might not be the best way to go espesically since my IC sampling
> method is complicated -- virial ratio is not preserved for quasi-random
> IC sampling.

With these invariants computed for all simulated trajectories, we can
quantitatively stratify the data from "easy" ( stable, regular motion)
to "hard" (chaotic, complex outcomes). The simulations are binned into
a multi-stage curriculum based on thresholds of the invariants. The
binning strategy (summarized from Table 1 of the original document) is
as follows:

- **Stage 0: Easiest, highly stable systems.** Data source:
  high-fidelity hierarchical simulations only (Set 1a).

  - **Criteria:**

    - Total Mechanical Energy: $E < -0.5$

    - Angular Momentum Ratio: $\frac{L}{L_{\max}} > 0.5$

    - Virial Ratio: $0.7 \leq Q \leq 1.3$

    - Minimum Initial Separation: $s_{\min} > 2$

  - **Description:** Tightly bound binaries with near-virial equilibrium
    and well-separated initial positions. Ideal for initial training due
    to smooth trajectories.

- **Stage 1: Still stable but slightly more complex.** Data source:
  remaining hierarchical simulations, divided into two sub-stages to
  introduce one complexity at a time (Set 1a).

  - **Stage 1a: Moderately Stable (Energy Relaxed)**

    - **Criteria:**

      - $-0.5 \leq E < -0.1$

      - $\frac{L}{L_{\max}} > 0.5$

      - $0.7 \leq Q \leq 1.3$

      - $s_{\min} > 2$

    - **Description:** Systems with moderately reduced binding energy
      while maintaining orbital stability.

  - **Stage 1b: Moderately Stable (Angular Momentum Relaxed)**

    - **Criteria:**

      - $E < -0.5$

      - $0.1 \leq \frac{L}{L_{\max}} < 0.5$

      - $0.7 \leq Q \leq 1.3$

      - $s_{\min} > 2$

    - **Description:** Systems with moderately reduced angular momentum
      (eccentric orbits) but strong binding energy.

- **Stage 2 (High-Resolution Refinement of Stable Orbits):** Data
  source: High-resolution hierarchical simulations (Set 2a).

  - **Criteria:** Union of Stage 0 and Stage 1 criteria

  - **Description:** This is the first critical revision. After
    mastering stable orbits in a low-resolution format, the model is now
    tasked with refining its predictions using the high-resolution
    BRUTUS output of the *same* physical systems (with the same
    hierarhical IC files used for **Stage 0** and **Stage 1**). Because
    the underlying physics is simple and already learned, the network
    can focus its capacity entirely on fitting the more detailed
    temporal signal without the compounding difficulty of chaotic
    dynamics.

- **Stage 3: Moderately Chaotic (Low-Fidelity)** Data source:
  low-fidelity quasi-random simulations (Set 1b).

  - **Criteria:**

    - $E \leq E^{\mathrm{LF}}_{25\%}$ (top 25% most bound in LF dataset)

    - $\frac{L}{L_{\max}} \geq L^{\mathrm{LF}}_{75\%}$ (top 25% highest
      angular momentum)

    - $0.9 \leq Q \leq 1.1$

  - **Description:** Least chaotic systems from low-fidelity data.
    Introduces early chaos while maintaining relative stability.

- **Stage 4: Fully chaotic regimes, introduced in steps.** Data source:
  Remaining low-fidelity data (Set 1b).

  - **Stage 4a: Chaotic (Long Predictability Horizon)**

    - **Data Source:** Remaining low-fidelity simulations

    - **Criteria:**

      - $\tau_L > 5$ (Lyapunov time $>$ 5 code units)

    - **Description:** Systems with moderate chaos and relatively long
      predictability horizons.

  - **Stage 4b: Highly Chaotic (Short Predictability Horizon)**

    - **Data Source:** Remaining low-fidelity simulations

    - **Criteria:**

      - $2 < \tau_L \leq 5$

    - **Description:** Systems with strong chaos and limited
      predictability.

- **Stage 5: High-Resolution Chaotic Orbits** Data source:
  High-resolution chaotic simulations (Set 2b).

  - **Criteria:** Same as Stage 4

  - **Description:** High-temporal-resolution trajectories of chaotic
    systems. Focuses on resolving close encounters.

- **Stage 6: Near-collision and extreme cases.** Data source: All
  remaining data; HF+LF

  - **Criteria:**

    $s_{\min} < 0.5$ **OR** $|E| < 0.01$

  - **Description:** Near-collision scenarios and borderline unbound
    systems.

Crucially, each subsequent stage's training set includes all data from
previous stages (curriculum replay) plus the new subset. This means by
the time we reach Stage 5 or 6, the training data is the entire dataset.
However, because the model has been gradually brought along this path,
it is not learning from scratch on this complex set; it has a strong
foundation from simpler cases. The staged curriculum defined above is
empirically designed to ensure a smooth progression from stable to
chaotic dynamics, aligning with human intuition of difficulty - initial
stages cover basic Keplerian motion and conservation laws, and later
stages add perturbations, resonances, and eventually close encounters
and escapes. This invariant-based stratification is mathematically sound
in that each invariant correlates with aspects of the equations of
motion's behavior (stability, boundedness, etc.), providing a principled
way to rank problem instances by difficulty.

# A Glimpse at the Data

**Analysis of Data Formats:**

The data pipeline begins with two types of raw text files for each
simulation instance: one specifying the initial conditions and another
containing the time-series output from the Brutus N-body integrator.

#### Initial Conditions (ic_hierarchical_\*.txt)

This is a 3-line text file containing 21 space-delimited,
double-precision floating-point numbers. These numbers represent the
complete initial state vector of the three-body system at time $t=0$.
The structure is a flattened array corresponding to the seven state
variables for each of the three bodies for each line. Together, it can
be represented as:
`[m1, x1, y1, z1, vx1, vy1, vz1, m2, x2, y2, z2, vx2, vy2, vz2, m3, x3, y3, z3, vx3, vy3, vz3]`.
This file is the primary source for calculating the conditional input
vector for the PINN.

```python
1.3490330328149076 -0.9689510833073296 0.007710980988132066 -0.015155493143494857 0.003082579960339502 -0.9723812422861391 0.01317780514703599 0.3068019185652623 -0.6619848581497906 -0.005365500630046534 0.0070754473066994734 0.002840479118371817 1.3293141254107488 -0.013692746386640507 1.3441650486198304 1.1354206743022845 -0.0016313630906544987 0.002882937931195984 0.00441920746565285 0.6549777259648452 0.001846566609351255
```

#### Brutus Simulation Output (brutus_hierarchical_\*.txt)

This is a time-series data file that provides the ground-truth
trajectories for the data-fidelity loss term, $\mathcal{L}_{data}$. The
file is structured as a sequence of blocks, where each block corresponds
to a specific snapshot in time. Each block begins with a header line
containing three values: the simulation time `t`, the number of bodies
`N` (which is always 3), and `t_cpu` (CPU Time). This header is followed
by `N` lines, where each line contains the seven state variables
(`m, x, y, z, vx, vy, vz`) for one of the three bodies at that specific
time `t`.

Thus, every Brutus output file has a repetitive block format that
contains:

- Header: `t, N, t_cpu`

- Body 1: `m1, x1, y1, z1, vx1, vy1, vz1`

- Body 2: `m2, x2, y2, z2, vx2, vy2, vz2`

- Body 3: `m3, x3, y3, z3, vx3, vy3, vz3`

A raw sample output from a Brutus simulation file is shown below,
illustrating the data format for a few time steps:

```python
0 3 0
1.3490330328149076 -0.9689510833073296 0.0077109809881320658 -0.015155493143494857 0.0030825799603395022 -0.97238124228613909 0.01317780514703599
0.30680191856526229 -0.66198485814979058 -0.0053655006300465337 0.0070754473066994734 0.002840479118371817 1.3293141254107488 -0.013692746386640507
1.3441650486198304 1.1354206743022845 -0.0016313630906544987 0.002882937931195984 0.0044192074656528501 0.65497772596484516 0.001846566609351255

0.080000000000000002 3 2.17338
1.3490330328149076 -0.95746912715152098388870457096922081377499 -0.068395326027771184330918692421700212149959 -0.013374646173250254126208350188876903106782 0.27927408182448689800114515637261157892989 -0.90345482920569108996083189130475635165807 0.030685786229670570110204639660396401512047
0.30680191856526229 -0.70556381350356795672897465039496696390801 0.093633356547250511770656254567903108831681 0.002818445191678544590613756190767057248414 -1.0718184960048500457752700625063898462062 1.0286823897602963737557930793641611624554 -0.089839191865848882805429923629505460110143
1.3441650486198304 1.1344968129380317254090080254393242791445 0.050753329467245612450222255049915160172 0.0030230315435012235246815871672795058650157 -0.027484630586336917599520346861990470320003 0.65442004534327653581772256816764955369181 0.0016553927250949034582096866402066475866725
```

In the following sections, we lay out a detailed, three-phase
implementation plan for the CTL-PINN training methodology. This guide is
intended to be sufficiently complete for reproducibility and practical
deployment of the model. We assume the datasets (hierarchical and
quasi-random simulations) have been generated as described in Section 2
and the supporting data pipeline document. The implementation is broken
into: Phase 1: Data preparation and curriculum setup, Phase 2: The
CTL-PINN training loop, and Phase 3: Active learning-based data
enhancement.

# Phase 1 - Data Preparation and Stratification

[Note: All code for this section is in the code folder for
pinn.]{style="color: blue"}
Author Comment: I believe this is another case for broken syntax or stale code from conversion. Also, this not estatement itself is outdated since all the code in the code folder is already outdated and unusuable.

## Step 1: Parse Raw Simulation Data

1.  Read the corresponding `ic_.txt` and `brutus_.txt` files.

2.  From the `ic_.txt` file, parse the initial state variables. This
    file may be a single line with 21 space-delimited floating-point
    values or three lines (one per body) with 7 values each:
    `[m, x, y, z, vx, vy, vz]`. Store these as NumPy arrays: masses as
    (3,), initial positions as (3,3), and initial velocities as (3,3).
    Use a dedicated parsing function to handle both formats robustly.

3.  From the `brutus_.txt` file, parse the time-series data. The file
    consists of repetitive blocks, each starting with a header line
    (`t, N=3, t_cpu`) followed by three lines of body states
    (`m, x, y, z, vx, vy, vz`). Iterate through blocks, skipping empty
    lines and handling an optional trailing 'Result:' line (which may
    contain energies like E_initial, E_final, dE/E—extract these into
    metadata). Store times as (T,), positions as (T,3,3), velocities as
    (T,3,3), and any metadata (e.g., cpu_times, energies). Gracefully
    handle short/incomplete files (e.g., fewer than 2 snapshots) by
    returning empty arrays and logging warnings.

4.  Infer metadata (e.g., dataset_type: 'hierarchical' or
    'quasi-random'; fidelity: 'high' or 'low'; dt_out: inferred from
    timestamps or defaults like 0.08/0.17) from filenames and Brutus
    content. This supports stratification and scaling for both data
    types.

5.  Combine parsed data into a structured object (e.g., a dataclass like
    RawTrajectoryData) that includes metadata, masses, initials, and
    time-series. For efficiency in global scaling (Step 2), parse IC
    files independently when possible (globals only need initials, not
    full Brutus time-series).

6.  Save parsed objects for all simulations into an efficient format
    like HDF5 or NumPy (.npy) files. This avoids repeated text parsing
    and accelerates loading during training. Use parallel processing if
    parsing large batches (e.g., via concurrent.futures for IC-only
    globals).

This parsing ensures consistency across all training data, preparing it
for dimensionless scaling in Step 2.

## Step 2: Unified Preprocessing Pipeline

Every IC/BRUTUS pair passes through one deterministic preprocessing transform
before any invariant calculation, stage assignment, or network input assembly.
The pipeline order is fixed:

parse -> mass-invariance check -> COM recenter -> zero-momentum boost ->
canonical ordering -> canonical rotation gauge -> global scaling ->
assertions and stored metadata.

The same transform is applied to hierarchical and quasi-random data and to
every BRUTUS snapshot, producing one frame, gauge, and scale convention shared
by initial conditions, BRUTUS targets, and model-output references.

### 2.1 Parser contract and mass-invariance check

Step 1 parses masses, positions, and velocities in float64 from the `ic_.txt`
and `brutus_.txt` files. Step 2.1 supplements Step 1 with the Phase 18
preprocessing contract and mass-invariance gate; it does not move Step 1
content or renumber the document. Before any training use, verify mass
invariance across the trajectory:

```text
max_t,i |m_i(t) - m_i(0)| < 1e-15
```

in float64 parse space. If this check fails, reject the trajectory or
quarantine it for parser debugging. This mass-invariance gate also carries the
folded-in B-11 (COM <-> mass consistency) assertion: the COM transform in 2.2
and every BRUTUS-snapshot correction require consistent masses between the IC
and the BRUTUS output.

### 2.2 COM recenter and zero-momentum boost

Apply a universal center-of-mass recenter and zero-momentum (Galilean) boost to
**all** datasets -- hierarchical and quasi-random -- regardless of whether they
are believed to already be in the COM frame.

For each trajectory, define

```text
M        = sum_i m_i
R_COM(0) = (1/M) sum_i m_i r_i(0)
V_COM    = (1/M) sum_i m_i v_i(0)
```

For every snapshot time `t_n`,

```text
bar r_i(t_n) = r_i(t_n) - R_COM(0) - V_COM t_n
bar v_i(t_n) = v_i(t_n) - V_COM
```

For the initial condition this gives `sum_i m_i bar r_i(0) = 0` and
`sum_i m_i bar v_i(0) = 0`. For an isolated Newtonian system the transformed
trajectory remains a valid solution in the COM frame.

### 2.3 Canonical ordering

After the COM recenter and zero-momentum boost, sort body labels
deterministically so that different permutations of the same physical system
yield identical input vectors. Order the three bodies by:

1. descending raw mass `m_i`;
2. tie-break by descending `||bar r_i(0)||` (COM-corrected initial-position norm);
3. tie-break by descending `||bar v_i(0)||` (COM-corrected initial-velocity norm);
4. final tie-break by original file order.

Canonical ordering operates on the raw masses and the COM-corrected `bar r` /
`bar v` from 2.2 -- not on scaled coordinates. The same permutation is applied
to the masses, every initial-condition quantity, every BRUTUS target snapshot,
and every residual, Hamiltonian, COM projection, and evaluation output. This
removes permutation ambiguity without requiring a permutation-equivariant
architecture.

### 2.4 Canonical rotation gauge

After canonical ordering, fix the initial orientation with a canonical rotation
gauge. Define the Jacobi position vectors

```text
rho    = bar r_2(0) - bar r_1(0)
lambda = bar r_3(0) - (m_1 bar r_1(0) + m_2 bar r_2(0)) / (m_1 + m_2)
```

#### Degeneracy thresholds

The rotation-gauge degeneracy thresholds are dimensionless relative thresholds,
not raw-coordinate constants. Let

```text
eta_gauge = 1e-8
```

Because the rotation gauge is applied after COM recentering, the zero-momentum
boost, and canonical ordering but **before** global scaling (2.5), define the
raw-space thresholds from the global Phase 18 scale constants `D`, `T`, `V`
(defined in 2.5):

```text
epsilon_rho    = eta_gauge * D
epsilon_lambda = eta_gauge * D
epsilon_v      = eta_gauge * V,   V = D / T
```

Equivalently, the implementation may compare the dimensionless ratios
`||rho||/D`, `||lambda_perp||/D`, and `||c_perp||/V` against `eta_gauge`.
`eta_gauge` is a numerical geometry guard for stable rotation-matrix
construction; it is **not** a physics softening parameter and is **not** tied to
`epsilon_train` or `epsilon_inv`. Numeric acceptance-check pass criteria for
`AC-FRAME-*` remain Phase 21 (VER-01/VER-04) scope.

#### Basis construction

The primary Jacobi vector is admissible only if `||rho|| > epsilon_rho`
(equivalently `||rho||/D > eta_gauge`). If this condition fails, classify the
trajectory as `gauge_degenerate_rho` and reject or quarantine it for
near-collision review, consistent with the 2.1 mass-invariance failure pattern;
the executor must **not** invent an arbitrary `e_x` axis. Otherwise set

```text
e_x = rho / ||rho||
```

Remove the `e_x` component from `lambda`:

```text
lambda_perp = lambda - (lambda dot e_x) e_x
```

If `||lambda_perp|| > epsilon_lambda` (equivalently `||lambda_perp||/D > eta_gauge`),
set

```text
e_y = lambda_perp / ||lambda_perp||
```

Otherwise the initial geometry is collinear; use the collinear fallback. For
each velocity-like candidate in the ordered list

```text
c in { rho_dot, lambda_dot, bar v_1(0), bar v_2(0), bar v_3(0) }
rho_dot    = bar v_2(0) - bar v_1(0)
lambda_dot = bar v_3(0) - (m_1 bar v_1(0) + m_2 bar v_2(0)) / (m_1 + m_2)
```

compute `c_perp = c - (c dot e_x) e_x` and pick the first candidate satisfying
`||c_perp||/V > eta_gauge` (equivalently `||c_perp|| > epsilon_v`). Set
`e_y = c_perp / ||c_perp||`. If no candidate passes, choose the fixed coordinate
basis vector least aligned with `e_x`, project it perpendicular to `e_x`, and
normalize.

After selecting `e_y` from the first admissible velocity-candidate projection in
the collinear fallback branch, orient its sign deterministically: if
`lambda_perp dot e_y < 0`, replace `e_y` with `-e_y`. This keeps
`lambda_y >= 0` whenever the sign is numerically meaningful; for exact collinear
geometries `lambda_y = 0` and the fallback candidate order supplies the
deterministic sign.

Set

```text
e_z = e_x x e_y
R_0 = [e_x^T; e_y^T; e_z^T]
```

Apply the same rotation to every snapshot:

```text
r_i^g(t_n) = R_0 bar r_i(t_n)
v_i^g(t_n) = R_0 bar v_i(t_n)
```

The canonical gauge ensures that, at `t = 0`,

```text
rho^g    = (rho_x, 0, 0)
lambda^g = (lambda_x, lambda_y, 0),   lambda_y >= 0
```

up to numerical tolerance.

#### FRAME-04 3D-Cartesian output guard

The rotation gauge fixes only the **initial** orientation of the Jacobi
positions. The Jacobi velocities remain fully 3D, the trajectory evolves in
full 3D, and the model output remains 9D Cartesian positions for the three
bodies. The output is **not planar** and **not invariant-only** -- the gauge
constrains only the initial Jacobi-position orientation, not the dimensionality
of the dynamics.

### 2.5 Global scaling

After the frame and gauge transforms, scale by the global constants. Define
these once across the entire dataset (all trajectories):

```markdown
T = t_max = 10
D = (G*T**2)^(1/3)
r_i' = r_i^g / D
v_i' = v_i^g / V
V = D / T
```

With `G = 1`, `D ~ 4.6416`. Although global scaling commutes algebraically with
COM subtraction, the documented order -- COM/boost first, scaling last -- is
required for auditability and to avoid mixed-frame intermediate files. Compute
all subsequent invariants (`E`, `s_min`, etc.) from the scaled `r'` and `v'`.

**Governing Mathematical Convention (locked Phase 19, PHYS-01):** The
characteristic length scale $D = (G T^2)^{1/3} \approx 4.6416$ is derived from
raw-mass nondimensionalization. Substituting $r = D r'$, $t = T u$ into
Newton's equation and demanding the dimensionless residual
$\frac{d^2 \mathbf{r}'_i}{du^2} = \sum_j m_j \frac{\mathbf{r}'_j - \mathbf{r}'_i}{\lVert \mathbf{r}'_j - \mathbf{r}'_i \rVert^3}$ (with raw masses
$m_i$, not mass fractions) forces $D^3 = G T^2$. The alternative
$D = (G M_{\mathrm{tot}} T^2)^{1/3} \approx 6.694$ is correct only under a mass-fraction
convention rewrite ($m_i' = m_i / M_{\mathrm{tot}}$) that would require touching every
residual, Hamiltonian, angular-momentum, COM, and invariant formula in the
framework. The mass-fraction alternative is documented as a future rewrite
only and is not adopted in v1.4. See
`.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/B-02.md`
for the full EVID-05 adjudication.

Global normalization scales (computed after scaling all trajectories):

- $E_{\mathrm{scale}} = \lvert \mathrm{median}(\{E_j\}) \rvert + 10^{-10}$
- $s_{\min,\mathrm{scale}} = \mathrm{median}(\{r_{\mathrm{char},j}\})$, where
  $r_{\mathrm{char},j} = \frac{1}{3} \sum_{i<k} \lVert \mathbf{r}'_{i,j} - \mathbf{r}'_{k,j} \rVert$
- $Q_{\mathrm{scale}}$ remains fixed at $0.5$.

Author Comment: so far all the inline math notations that have this format `xxxx` are rendered as literal text strings in the preview and are not readable. Consider changing this syntax in a way that is machine-reading friendly and also renders correctly and nicely for human reader reading in preview.

### 2.6 Assertions and stored metadata

After preprocessing, assert the center-of-mass and total-momentum conditions on
every preprocessed sample:

```markdown
||sum_i m_i r_i'|| < 1e-12
||sum_i m_i v_i'|| < 1e-12
```

A trajectory failing either assertion is rejected or quarantined, consistent
with the 2.1 mass-invariance failure pattern.

Each trajectory record stores the following metadata:

```text
traj_id
raw_file_paths
ordered_raw_masses: (3,)
permutation: (3,)
R0: (3,3)
R_COM0: (3,)
V_COM: (3,)
D, T, V
r0_prime_ordered_gauge: (3,3)
v0_prime_ordered_gauge: (3,3)
times_raw: (Nt,)
u: (Nt,)
tau: (Nt,)
r_true_prime_ordered_gauge: (Nt,3,3)
v_true_prime_ordered_gauge: (Nt,3,3)  # optional but recommended
IC13: (13,)
invariants: E, Q, s_min, L_vec, L_norm, I_norm_raw, I1, I2, I3, tau_L
brutus_tolerance, word_length, dt_out, trustworthy_horizon
```

Raw masses are always available separately from the network-facing mass
channels. Step 3 consumes the COM-corrected, canonically ordered, gauge-fixed,
scaled state and the metadata produced here.

## Step 3: Necessary Calculations of Invariants (for Stage Assignment and Input Vector Formulation)

#### Scope and preconditions.

All quantities in this section are computed from the *scaled* initial
conditions $\{(\mathbf r'_i,\mathbf v'_i)\}_{i=1}^3$ and from the BRUTUS
trajectory output. Verification that the ICs are in the center-of-mass
(COM) frame with zero total momentum is a *precondition* established by the
Step 2 Unified Preprocessing Pipeline and asserted in Step 2.6 before any
calculations proceed.

#### Outputs of this step.

Given one IC (plus its associated trajectory), Step 3 deterministically
returns the tuple
$$\mathcal{I} = \big(E,\;Q,\;s_{\min},\;L_{\mathrm{norm}},\;I_{\mathrm{norm,raw}},\; \tau_L,\; m_1, m_2, m_3,\; I_1, I_2, I_3 \big),$$
which is then consumed by the stage-assignment rules in §4.4 and retained
as metadata alongside the Step 4 network input assembly. By default, stage
gating uses $(E,Q,s_{\min},L_{\mathrm{norm}},\tau_L)$;
$I_{\mathrm{norm,raw}}$ is available for additional heuristics; shape
invariants ($I_1, I_2, I_3$) are metadata diagnostics only and are not
final network IC slots under the Phase 17 input contract.

1.  **Total energy $E$, virial ratio $Q$, and minimal separation
    $s_{\min}$.**

    $$\begin{aligned}
        T &= \tfrac12 \sum_{i=1}^{3} m_i \,\lVert \mathbf v'_i \rVert^2, \\
        \varepsilon_{\mathrm{inv}} &= 10^{-10}, \\
        r_{\mathrm{safe},ij} &= \sqrt{\lVert \mathbf r'_i - \mathbf r'_j \rVert^2 + \varepsilon_{\mathrm{inv}}^2}, \\
        V &= - \sum_{1\le i<j\le 3} \frac{m_i m_j}{r_{\mathrm{safe},ij}}, \\
        E &= T + V, \qquad
        Q \;=\; \frac{2\,T}{\lvert V \rvert}, \qquad
        s_{\min} \;=\; \min_{1\le i<j\le 3} \lVert \mathbf r'_i - \mathbf r'_j \rVert.

    \end{aligned}$$

    We use the Plummer form $r_{\mathrm{safe}} = \sqrt{\lVert \mathbf{r}'_i - \mathbf{r}'_j \rVert^2 + \varepsilon_{\mathrm{inv}}^2}$ with
    static-invariant softening $\varepsilon_{\mathrm{inv}} = 10^{-10}$
    (in scaled units) *only in $V$* to prevent singularities. The
    geometric quantity $s_{\min}$ is computed from true pairwise
    separations (no softening).

    **anti-pattern (PHYS-03):** Do not mix additive $(\lVert \mathbf{r} \rVert + \epsilon)$ with Plummer $\sqrt{\lVert \mathbf{r} \rVert^2 + \epsilon^2}$ forms. Do not mix
    $(\lVert \mathbf{r} \rVert + \epsilon)^{-3}$ force with $(\lVert \mathbf{r} \rVert + \epsilon)^{-1}$ potential. The
    chosen pair must appear identically in residual and Hamiltonian. The
    static-invariant softening $\varepsilon_{\mathrm{inv}} = 10^{-10}$ is context-specific for
    offline invariant computation and is distinct from the training-time
    softening $\varepsilon_{\mathrm{train}} = 10^{-5}$ used in the `pinn_architecture.md` PHYS-03 residual and energy contracts.

    Author Comment: this section is a syntax disaster. ALl the raw latex syntax are broken in rendered preview, and they show up as literal text strings. The other syntax are also incorrect for proper markdown file. Carefully look into this and think about how to fix it. Maintaining the exact, identifical math equation and expressions is of the utmost importance here. The following sections after this and below this should also be carefully examined.

2.  **Normalized angular momentum $L_{\mathrm{norm}}$.**

    $$\begin{aligned}
        \mathbf L &= \sum_{i=1}^3 m_i \,(\mathbf r'_i \times \mathbf v'_i), \qquad
        L = \lVert \mathbf L \rVert, \\
        r_{\mathrm{char}} &= \frac{1}{3} \sum_{1\le i<j\le 3} \lVert \mathbf r'_i - \mathbf r'_j \rVert, \qquad
        v_{\mathrm{char}} = \sqrt{\frac{2\,\lvert E \rvert}{M_{\mathrm{tot}}}}, \\
        L_{\max} &= M_{\mathrm{tot}} \, r_{\mathrm{char}} \, v_{\mathrm{char}}, \qquad
        L_{\mathrm{norm}} = \frac{L}{L_{\max}}.

    \end{aligned}$$

    This $L_{\max}$ is *canonical* in CTL and represents
    the characteristic circular‐orbit scale at energy $E$. All other
    historical variants are deprecated.

    ```python
    def compute_L_norm(m, r_prime, v_prime, E, eps=1e-10):
        L_vec = np.sum([m[i] * np.cross(r_prime[i], v_prime[i]) for i in range(3)], axis=0)
        L = np.linalg.norm(L_vec)
        pairwise = [np.linalg.norm(r_prime[i] - r_prime[j]) for i in range(3) for j in range(i+1, 3)]
        r_char = np.mean(pairwise)
        M_total = np.sum(m)
        v_char = np.sqrt(2 * np.abs(E) / M_total + eps)
        L_max = M_total * r_char * v_char
        return L / (L_max + eps)
    ```

3.  **Normalized moment of inertia $I_{\mathrm{norm,raw}}$.** Let $I(\mathbf r')$ be the inertia tensor about
    COM:
    $$\mathbf I \;=\; \sum_{i=1}^{3} m_i \Big( \lVert \mathbf r'_i \rVert^2 \,\mathbf I_{3\times 3}
                                            - \mathbf r'_i (\mathbf r'_i)^{\!\top} \Big).$$
    We use its trace as a rotationally invariant scalar and normalize by
    the characteristic scale of the normalized angular momentum (see above):
    $$I_{\mathrm{norm,raw}} \;=\; \frac{\mathrm{tr}(\mathbf I)}{M_{\mathrm{tot}}\, r_{\mathrm{char}}^{\,2}}.$$
    (This quantity is not required for default stage gating but is
    retained as a robust, scale‑consistent descriptor of spatial
    extent.)

    ```python
    import numpy as np

        def compute_normalized_inertia(m, r_prime, r_char, eps=1e-10):
            """Compute raw normalized moment of inertia per text definition (using scaled data from Step 2).
            No bounding here; normalization to [-1,1] deferred to input prep.
            """
            I_tensor = np.zeros((3,3))
            for i in range(3):
                ri = r_prime[i]  # Already in COM frame
                ri_norm_sq = np.dot(ri, ri)
                outer = np.outer(ri, ri)
                I_tensor += m[i] * (ri_norm_sq * np.eye(3) - outer)
            
            I_trace = np.trace(I_tensor)
            M_total = np.sum(m)
            denom = M_total * max(r_char**2, eps)
            I_norm_raw = I_trace / denom  # Raw value, potentially >1 or <0 (though typically positive)
            
            if not np.isfinite(I_norm_raw):
                raise ValueError("Non-finite I_norm_raw computed; check inputs.")
            
            return I_norm_raw
    ```

4.  **Universal Shape Invariants ($I_1, I_2, I_3$).** Let
    $d_{12} = ||\mathbf{r}'_1 - \mathbf{r}'_2||$,
    $d_{13} = ||\mathbf{r}'_1 - \mathbf{r}'_3||$, and
    $d_{23} = ||\mathbf{r}'_2 - \mathbf{r}'_3||$ be the three mutual
    distances. Sort these as
    $d_{\text{short}} \leq d_{\text{mid}} \leq d_{\text{long}}$.

    $$\begin{aligned}
        I_1 &= \frac{d_{\text{short}}}{d_{\text{long}}} \in [0, 1] \\
        I_2 &= \frac{d_{\text{mid}}}{d_{\text{long}}} \in [I_1, 1] \\
        I_3 &= \frac{d_{\text{short}} + d_{\text{mid}} - d_{\text{long}}}{d_{\text{short}} + d_{\text{mid}} + d_{\text{long}}} \in [0, 1/3]
        
    \end{aligned}$$

    The raw shape invariant $I_3 \in [0, 1/3]$ (0 for the degenerate collinear
    configuration, $1/3$ for the equilateral configuration). For staging/metadata
    use it is linearly mapped to $[-1, 1]$ via $I_3^{\mathrm{in}} = 6\,I_3 - 1$.
    $I_3$ is a metadata diagnostic and is not a network IC slot under the Phase 17
    input contract.

5.  **Lyapunov time $\tau_L$ via a Rosenstein-style estimator.**
    We estimate the largest Lyapunov
    exponent directly from the BRUTUS trajectory positions using a
    robust method inspired by Rosenstein et al. and the implementation
    in 'ChaosTools.jl'. This approach is applicable to both hierarchical
    and quasi-random configurations as it operates directly on the
    time-series data.

    1.  *Uniform Cadence:* The trajectory is first resampled to a
        uniform time step $\Delta t$ using linear interpolation. This is
        crucial for consistent analysis, especially if the BRUTUS output
        has adaptive time steps.

    2.  *Delay-Coordinates Embedding:* The 9-dimensional state vector
        (positions of the three bodies) is embedded in a
        higher-dimensional space to reconstruct the attractor's
        geometry. We use a standard embedding dimension (e.g., $d=5$)
        and a delay $\tau$ determined from the first minimum of the
        mutual information of the time series.

    3.  *Finding Nearest Neighbors:* For each point in the embedded
        trajectory, we find its nearest neighbor. To avoid spurious
        correlations, we enforce a Theiler window, excluding neighbors
        that are too close in time.

    4.  *Divergence Curve:* We then calculate the average logarithmic
        divergence of these neighbor pairs as they evolve in time. This
        gives us a curve
        $E(k) \approx \lambda_{\max} \cdot k \cdot \Delta t + E(0)$,
        where $k$ is the number of time steps.

    5.  *Linear Regression:* The largest Lyapunov exponent,
        $\lambda_{\max}$, is estimated by finding the slope of the
        linear region of the divergence curve.

    6.  *Lyapunov Time:* The Lyapunov time is then calculated as
        $\tau_L = 1/\lambda_{\max}$. If $\lambda_{\max} \le 0$, we
        consider the system to be regular and set $\tau_L = \infty$.

    ```python
    import numpy as np
        from scipy.spatial.distance import pdist, squareform

        def lyapunov_time_from_trajectory(
            positions,
            dt=0.01,
            embedding_dim=5,
            delay=10,
            theiler_window=100
        ):
            """
            Estimates the Lyapunov time from trajectory data using a method
            inspired by Rosenstein et al.
            """
            # Ensure positions is a 2D array
            if positions.ndim == 1:
                positions = positions[:, np.newaxis]

            # Delay embedding
            N = len(positions)
            embedded_trajectory = np.zeros((N - (embedding_dim - 1) * delay, embedding_dim * positions.shape[1]))
            for i in range(embedded_trajectory.shape[0]):
                for j in range(embedding_dim):
                    start_idx = i + j * delay
                    end_idx = start_idx + 1
                    embedded_trajectory[i, j*positions.shape[1]:(j+1)*positions.shape[1]] = positions[start_idx]

            # Find nearest neighbors
            dist_matrix = squareform(pdist(embedded_trajectory, 'euclidean'))
            np.fill_diagonal(dist_matrix, np.inf)

            # Apply Theiler window
            for i in range(dist_matrix.shape[0]):
                for j in range(max(0, i - theiler_window), min(dist_matrix.shape[0], i + theiler_window + 1)):
                    dist_matrix[i, j] = np.inf

            neighbor_indices = np.argmin(dist_matrix, axis=1)

            # Calculate divergence
            max_iter = N - (embedding_dim - 1) * delay - np.max(neighbor_indices)
            divergence = []
            for k in range(max_iter):
                distances = []
                for i in range(len(neighbor_indices)):
                    idx1 = i + k
                    idx2 = neighbor_indices[i] + k
                    if idx1 < embedded_trajectory.shape[0] and idx2 < embedded_trajectory.shape[0]:
                        dist = np.linalg.norm(embedded_trajectory[idx1] - embedded_trajectory[idx2])
                        if dist > 1e-9: # Avoid log(0)
                            distances.append(np.log(dist))
                if distances:
                    divergence.append(np.mean(distances))

            if not divergence:
                return np.inf # Not enough points to calculate divergence

            # Linear regression to find the Lyapunov exponent
            time_steps = np.arange(len(divergence)) * dt
            coeffs = np.polyfit(time_steps, divergence, 1)
            lambda_max = coeffs[0]

            if lambda_max <= 0:
                return np.inf

            return 1.0 / lambda_max
    ```

6.  **Normalized Masses ($m_1, m_2, m_3$).** Extract the masses directly
    from the scaled ICs (they are dimensionless in G=1 units). These are
    used for input vector assembly.

    > **Author note:** We need the code snippets here for this.

> **Author note:** The two paragraphs below are suspicious. We need to carefully
> examine them.

#### Numerical notes and defaults.

Unless otherwise specified, use double precision for all invariants. The
static-invariant Plummer softening $\varepsilon_{\mathrm{inv}}=10^{-10}$
in the total energy definition (see above) is a safe default in scaled units
and *does not* enter $s_{\min}$ or any denominator besides $V$.

#### Sanity checks (quick tests).

Before large‑scale runs:

- *Two‑body limit* ($m_3\!\to 0$): expect $Q\!\approx\!1$, large
  $L_{\mathrm{norm}}$, and $\tau_L\!\to\!\infty$.

- *Equal‑mass symmetric triples*: invariants cluster tightly across
  random seeds, and $\tau_L$ varies smoothly with small IC
  perturbations.

## Step 4: Formulating the Input Vector: Canonical Ordering, Normalization, and Assembly

#### Scope.

Using the invariants and quantities computed in Step 3 (e.g., $E$, $Q$,
$s_{\min}$, $L_{\text{norm}}$, $I_{\text{norm,raw}}$, $I_1$, $I_2$, $I_3$,
masses), this step applies canonical ordering, computes the scaled
Jacobi-state variables, normalizes each network IC slot, and assembles
the final 14D network input vector $[\tau, IC_{13}]$ for the PINN per
the Phase 17 input contract. The invariant-heavy descriptors above are
retained as metadata for curriculum staging, diagnostics, loss scaling,
and reporting only; they are no longer final network IC slots.

1.  **Canonical ordering.** Canonical ordering is already applied in
    Step 2.3; Step 4 consumes the ordered, gauge-fixed, scaled state.

2.  **Apply Normalization to $[-1,1]$.** The final network IC slots are
    normalized only after the Phase 18 (FRAME-01) preprocessing contract
    has produced the ordered raw masses and Jacobi-state scalars. The
    legacy invariant-heavy quantities computed above are retained as
    metadata for staging, diagnostics, loss scaling, and reports; they are
    not concatenated into the final `IC_{13}` vector.

    > **Historical author note (pre-Phase 17; retained as a non-normative
    > question):** Confirm that all components in the IC vector are in the
    > range $[-1,1]$ and that it is the final form that will be fed to the
    > PINN.

    #### Mathematical Guarantees

    This parameterization satisfies several critical requirements:

    1.  **Deterministic gauge-fixed representation**: The canonical ordering ensures that different
        permutations of the same physical system yield identical input
        vectors.

        **IC13 Validity (locked Phase 19, PHYS-06):** The final IC13 is a redundant but reconstructive fixed-gauge initial-state encoding. It is not justified by constraint counting against a reduced phase space. Its validity comes from COM removal, zero-momentum boost, canonical ordering, canonical rotation, and retention of the independent Jacobi position/velocity degrees of freedom -- as locked by Phase 17 (IO-02) and Phase 18 (FRAME-01). The canonical preprocessing pipeline (Step 2) deterministically produces a gauge-fixed IC encoding that uniquely represents the trajectory up to the symmetries already removed. See `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/M4.md` for the full EVID-05 adjudication.

    2.  **Continuity**: All network IC slots vary continuously with the
        preprocessed initial conditions, ensuring smooth neural network
        training.

    3.  **Universality**: No special cases or singularities for specific
        configurations (unlike orbital elements).

    4.  **Physical Interpretability**: Each component has clear physical
        meaning, aiding in model interpretation and debugging.

    #### Numerical Implementation Considerations

    When implementing this transformation, careful attention must be paid
    to numerical stability in the metadata calculations and the final
    Jacobi-state slot assembly:

    - Use the static-invariant Plummer form with $\varepsilon_{\mathrm{inv}} = 10^{-10}$
      in potential energy calculations to avoid division by zero

    - Verify momentum conservation after canonical ordering:
      $||\sum m_i \mathbf{v}'_i|| < 10^{-12}$

    - Use dataset-wide statistics for normalization scales to ensure
      consistency

    This universal parameterization provides a robust foundation for the
    PINN that works equally well for all types of three-body initial
    conditions, from highly hierarchical systems to chaotic quasi-random
    configurations.

    > **Historical author note (pre-Phase 17; retained as a non-normative
    > question):** Confirm on this mathematcial guarantees' arguments and the
    > numerical implementation's purpose and validity. If confirmed, how
    > should we integrate and implement this into the existing workflow?
    > Also, we have to add the time t into this vector to achieve the
    > final 14-dimensional input vector ready to be fed to the PINN.

#### Network input contract

The network input is exactly

$$
x_{\mathrm{net}} = [\tau, IC_{13}], \qquad \tau = 2u - 1,\qquad u=t/T.
$$

For the normalized-time derivative contract (autograd leaf, chain-rule factors,
componentwise derivatives, and synthetic-trajectory test), see pinn_architecture.md PHYS-02 contract.

The primary initial-condition vector is the 13-component Jacobi-state contract

$$
IC_{13} = [m_1, m_2, m_3, \rho_x, \lambda_x, \lambda_y,
\dot{\rho}_x, \dot{\rho}_y, \dot{\rho}_z,
\dot{\lambda}_x, \dot{\lambda}_y, \dot{\lambda}_z, E].
$$

The mass entries are ordered raw masses before normalization. Canonical body ordering, frame recentering, momentum boost, rotation gauge, and scaling order are defined in Phase 18 (FRAME-01); this section only states the network-facing IC vector after that preprocessing contract is applied.

After preprocessing, define scaled Jacobi state variables:

$$
\rho' = r_2'(0)-r_1'(0),
$$

$$
\lambda' = r_3'(0)-\frac{m_1r_1'(0)+m_2r_2'(0)}{m_1+m_2}.
$$

The position slots retained in `IC_{13}` are $\rho_x$, $\lambda_x$, and $\lambda_y$ after the Phase 18 (FRAME-01) gauge. The velocity slots remain fully 3D:

$$
\dot{\rho}'=(\dot{\rho}_x,\dot{\rho}_y,\dot{\rho}_z), \qquad
\dot{\lambda}'=(\dot{\lambda}_x,\dot{\lambda}_y,\dot{\lambda}_z).
$$

Mass, Jacobi-position, and Jacobi-velocity slots are normalized independently with dataset-wide statistics computed after preprocessing:

$$
z^{in} = \tanh\left(\frac{z-\mu_z}{\sigma_z + 10^{-8}}\right).
$$

| Slot group | Pre-tanh scalar $z$ | Network value |
|---|---|---|
| Ordered raw masses | $m_i$ for $i \in \{1,2,3\}$ | $\tanh\!\left(\frac{m_i - \mu_{m_i}}{\sigma_{m_i} + 10^{-8}}\right)$ |
| Jacobi position slots | $\rho_x$, $\lambda_x$, $\lambda_y$ | $\tanh\!\left(\frac{z - \mu_z}{\sigma_z + 10^{-8}}\right)$ |
| Jacobi velocity slots | $\dot{\rho}_x$, $\dot{\rho}_y$, $\dot{\rho}_z$, $\dot{\lambda}_x$, $\dot{\lambda}_y$, $\dot{\lambda}_z$ | $\tanh\!\left(\frac{z - \mu_z}{\sigma_z + 10^{-8}}\right)$ |
| Energy slot | $E$ | $\tanh\!\left(\frac{E}{E_{\mathrm{scale}}}\right)$, where $E_{\mathrm{scale}} = \lvert \mathrm{median}_{\mathrm{traj}}(E) \rvert + 10^{-8}$ |

The energy normalization maps any real $E$ into the network range $(-1, 1)$ via $\tanh(E / E_{\mathrm{scale}})$. For the documented bound-system dataset, $E_{\mathrm{norm}}$ occupies $[-1, 0)$ — the positive side of the tanh input range is unused because bound systems have $E < 0$. This is acceptable for SIREN and is not a normalizer correctness failure (see `simulation_data/Documentation/README.md` for data-generation regimes).

The mass slots are normalized per slot with dataset-wide statistics. For hierarchical ICs, the dataset-occupied $m_{\mathrm{norm}}$ range is asymmetric; this asymmetry carries mass hierarchy information and is not a centering or correctness failure.

The old invariant-heavy descriptors ($Q$, $s_{\min}$, $\mathbf{L}_{\mathrm{vec}}$, $L_{\mathrm{norm}}$, $I_{\mathrm{norm,raw}}$, $I_1$, $I_2$, $I_3$, $\tau_L$, and orientation summaries) remain available as curriculum, diagnostics, loss-scaling, and reporting metadata. They are not final network IC slots under the Phase 17 input contract.

The network time coordinate is centered around zero by the linear map $\tau = 2u - 1$ with $u = t/T$ (where $T = t_{\max}$ is the characteristic time), which aligns with the periodic activation functions (e.g., SIREN) and improves training dynamics. The autograd leaf is `u`; the model wrapper computes `tau` internally.

Author Comment: again the syntax issues here above in the `` format are all broken and need fixing. 

## Step 5: Curriculum Stage Assignment

Now, assign a curriculum stage label (an integer from 0 to 6) to each
simulation. This is achieved by applying the specific threshold criteria
defined in this document in section 2.3 on 'Multi-Stage Data
Stratification by Difficulty'. This process should be fully automated in
a script that reads the table of computed invariants and outputs a
mapping from each simulation ID to its assigned stage index.

# Phase 2 - The Definitive CTL-PINN Training Loop

> **Historical author note (pre-Phase 17; retained as a non-normative
> question):** My biggest question now for this training loop is that: how are we
> feeding the exact input vector and brutus simulation data into the
> network? We need a very specific description that clearly tells me what
> the input format is going to be. For example, right now I know that our
> input vector is a 14th-dimentional input vector; but my question is that
> since the brutus simulation data has a bunch of time series and time
> snapshots, at each which there is a set of 3-body positions and
> velocities, how are we handing the Brutus simulation data to this neural
> network? Like how do we use the Brutus simulation data in this workflow?
> and how do we input it together with the input vector? In which step?
> After the network output a predicted trajectory do we just give it the
> brutus ground-truth data and let it optimize based on that? This ties to
> my bigger question that what is the network ultimately doing? Looking at
> the PINN docment section 5.2 on "5.2 Output Layer and Kinematic
> Consistency via Automatic Differentiation", is the ouptut file going to
> be something similar to a brutus output file, sort of acting as a
> replacement for the brutus algorithm?

The CTL framework breaks the cycle of needing complex data to learn
physics while requiring basic physics to handle complex data by
progressing through stages of increasing difficulty. This section
provides a complete specification for the Phase 2 training loop,
detailing the optimization strategy within each curriculum stage. The
loop involves macro-level curriculum progression, meso-level two-phase
optimization per stage, and micro-level techniques like lookahead
sampling for smooth transitions.

## Overview: The Two-Phase Optimization Strategy

Within each curriculum stage, a two-phase strategy leverages a
stochastic optimizer for exploration and a quasi-Newton method for
refinement:

- **Phase 2a: Adam-driven Exploration** - Uses Adam to explore the loss
  landscape and find a good basin.

- **Phase 2b: L-BFGS Refinement** - Approximates the Hessian to drive
  down residuals precisely.

### Data Flow During Training

The data flow for each training step is as follows:

1. **Input**: The model receives the 14-dimensional network input `[\tau, IC_{13}]`, where `u=t/T` is the autograd leaf and `\tau=2u-1`.

2. **Network Prediction**: The network emits a raw 9D position head for the three bodies. The architecture applies the hard mass-weighted COM projection defined in `pinn_architecture.md` before any loss, residual, diagnostic, or evaluation metric consumes the output. The projection weights are ordered raw pre-tanh mass metadata supplied by the Phase 18 (FRAME-01) preprocessing output, not the normalized `IC_{13}` mass slots. Velocities and accelerations are AD-derived from the projected positions; the network does not directly output velocities.

3.  **Loss Computation**: The default Phase 19 loss terms are computed:

    - $\mathcal{L}_{\text{data}}$: Compares the network's predicted
      positions with the ground-truth trajectories from the Brutus
      simulations.

    - $\mathcal{L}_{\text{IC}}$: Anchors predicted position and velocity at
      `u = 0`.

    - $\mathcal{L}_{\text{phys}}^{\text{causal}}$: Calculates the causally
      weighted residual of Newton's equations of motion by using automatic
      differentiation to get the second derivative of the network's position
      output.

    - $\mathcal{L}_{E}$: Penalizes relative drift from the system's known
      initial energy as a soft conservation regularizer.

    - $\mathcal{L}_{L}$: Penalizes componentwise relative angular-momentum
      drift.

4.  **Backpropagation**: The gradients of the total loss function flow
    back through the network to update the model's weights; gradients
    are computed by comparing predictions directly to Brutus
    ground-truth snapshots at sampled t values.

## Loss Function Formulation

### Phase 2: Total Training Loss

The default training loss is:

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{data}} + \lambda_{\mathrm{IC}} \, \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{phys}} \, \mathcal{L}_{\mathrm{phys}}^{\mathrm{causal}} + \lambda_E \, \mathcal{L}_E + \lambda_L \, \mathcal{L}_L
$$

where each term is defined by name in the PHYS-05 loss-term catalog in
`pinn_architecture.md` ($\mathcal{L}_{\mathrm{data}}$, $\mathcal{L}_{\mathrm{IC}}$, $\mathcal{L}_{\mathrm{phys}}^{\mathrm{causal}}$, $\mathcal{L}_E$, and $\mathcal{L}_L$).
The loss-balancing contract, warmup schedule, and optimizer-phase semantics
are defined in the PHYS-05 training-loss contract in `pinn_architecture.md`.

**Optimizer-phase semantics (PHYS-05):** During Adam epochs, hyperparameters
(`λ` values) may be scheduled per the warmup schedule. During L-BFGS, `λ`
values are frozen and no dual updates occur inside a line search.
Stage-boundary transitions apply re-warmup per the new stage's
`λ_phys^max` / `λ_E^max` / `λ_L^max`.

**Causal weighting (PHYS-05 default):** Dense ODE residuals use causal weighting `w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))`, `w_1 = 1`, `η_c = 1`
default, with stopgrad in weights by default to prevent the weight mechanism
from becoming an adversarial term. The exponent must be clipped to avoid
underflow, but Phase 19 does not choose a numeric clipping bound; surface a
gap if execution requires one.

The previous pseudo-ALM formulation (`L_data + λ_p·L_phys + (μ_p/2)·L_phys² + λ_E(k)·L_energy`) is rejected because squaring a nonnegative MSE produces a quartic residual that does not represent a standard equality-constrained augmented Lagrangian. Optional ALM for scalar conservation constraints only is documented as a P2 ablation in the PHYS-05 ablation section of `pinn_architecture.md`.

## Phase 2a: Adam-driven Exploration

The initial phase uses Adam for robust navigation of non-convex loss
landscapes.

### Initialization

At the beginning of a new stage $k$:

- Load network weights from the converged model of stage $k-1$ (if
  $k > 0$).

- **Critical**: Completely reset Adam's internal state (momentum
  buffers) to prevent biased gradient statistics from prior data.

- Set initial learning rate: $\text{LR}_k = 10^{-3} \times (0.7)^k$.

- Initialize a cosine annealing scheduler to decay the learning rate
  over the phase.

- Set Adam parameters: $\beta_1 = 0.9$, $\beta_2 = 0.999$,
  $\epsilon=1e-8$.

### Mini-Batch Construction with Lookahead Sampling

For batch size B (e.g., 256), reserve $\rho_{\text{lookahead}}$ (e.g.,
5%) for lookahead sampling to smooth stage transitions. Sample
$n_{\text{pts}}$ (e.g., 32) time points per trajectory: 50% uniform from
$[0, T]$, 50% weighted by acceleration norm (prioritizes close
encounters).

| Portion | Purpose | Symbol | Size |
|---|---|---|---:|
| Replay set | Prevent forgetting of material from stages $0 \ldots k$ (ensures curriculum replay) | $B_{\leq k}$ | 240 |
| Look-ahead set | "Preview" data from the next stage $k+1$ | $B_{k+1}$ | 16 |

*Mini-batch composition for batch size = 256.*

### Adaptive Median-Based Gradient Clipping

Use adaptive global-norm clipping to handle gradient explosions from
close encounters; threshold is $C$ times the moving median of recent
norms.

**Curriculum-aware $C$ schedule:**

| Curriculum stage | Data difficulty | C |
|---|---|---:|
| 0--1 | quasi-periodic orbits | 7--10 |
| 2--3 | onset of mild chaos | 5 |
| 4--6 | frequent close encounters | 3 |

### Termination Criterion

Hand off to L-BFGS when the physics loss plateaus:
$$\frac{d(\log_{10} \mathcal{L}_{\text{phys}})}{d(\text{epoch})} > -5 \times 10^{-3} \quad \text{for 50 consecutive epochs}$$

## Phase 2b: High-Precision L-BFGS Refinement

Hand off to L-BFGS to polish the solution and minimize residuals.

### Optimizer Selection by Dataset Size

The L-BFGS variant depends on cumulative dataset size.

**Early Stages (0-2): Full-Batch L-BFGS**

- Use standard full-batch on the entire dataset.

- Parameters: history size: 10, line search: "Wolfe", max iterations:
  20-50.

**Later Stages (3-6): Stochastic L-BFGS (sL-BFGS)**

- Switch to mini-batch variant for memory efficiency.

- Parameters: batch size: 32, curvature interval: update every 10
  iterations.

**Important**: No gradient clipping during L-BFGS, as line-search
creates a trust region.

## Stage Transition Criteria

> **Author note:** Now, for this, we will need to look at how the first stage goes
> when the actual process starts. All of this transition creteria is
> theoretical now, and it will heavily depend on what the actual situation
> is like. Because I only have a limited amount of training data, maybe
> not even enough, I would not expect the network to perform
> extraodinarily well. All I have to see is that the network has the
> potential to do something similar to a 3-body integrator and that it has
> the potential to become better with more training data and optimization.
> Based on this, how should we handle the stage transition criteria
> depending on the actual situations that might happen? Should we first
> test train stage 0 and see how it goes and then go from there?

Advance to the next stage only when all four criteria are met on the
validation set (hold-out 10-20% of cumulative data per stage).

### 1. Training Loss Plateau

Relative change in smoothed total loss below threshold:
$$\frac{|\mathcal{L}_{\text{smooth}}(i) - \mathcal{L}_{\text{smooth}}(i - \text{patience})|}{\mathcal{L}_{\text{smooth}}(i)} < \epsilon_{\text{plateau}}$$
where
$\mathcal{L}_{\text{smooth}}(i) = \beta \cdot \mathcal{L}_{\text{smooth}}(i-1) + (1-\beta) \cdot \mathcal{L}_{\text{train,total}}(i)$,
$\beta = 0.98$, patience = 200, $\epsilon_{\text{plateau}} = 10^{-5}$.
Initialize $\mathcal{L}_{\text{smooth}}(0)$ as the first computed loss.

### 2. Validation Loss Stability

Current validation loss $\leq$ minimum seen in stage:
$$\mathcal{L}_{\text{val}}(i) \leq \min_{j \leq i} \mathcal{L}_{\text{val}}(j)$$

### 3. Physics Residual Threshold

Validation physics loss below threshold:
$$\mathcal{L}_{\text{phys}}^{\text{val}} < \epsilon_{\text{phys}} \quad (\epsilon_{\text{phys}} = 10^{-4})$$

### 4. Energy Conservation Check

Average relative energy drift below threshold, using the persisted
PHYS-04/D-20 (GAP-19-01) energy denominator floor `epsilon_H = 1e-4 * S_H`:
$$\frac{1}{N_{\text{traj}}} \sum_{j=1}^{N_{\text{traj}}} \frac{|H_j(t_{\text{final}}) - H_j(0)|}{|H_j(0)| + \epsilon_H} < \epsilon_{\text{energy}} \quad (\epsilon_{\text{energy}} = 10^{-4})$$

## Consolidated Hyperparameter Schedule

| Stage | Adam LR (Initial) | Clip `C` | Loss-weight schedule | L-BFGS Type |
|---|---|---:|---|---|
| 0-1 | $10^{-3} \times (0.7)^k$ | 7-10 | See PHYS-05 warmup schedule in `pinn_architecture.md` | Full-Batch |
| 2-3 | $10^{-3} \times (0.7)^k$ | 5 | See PHYS-05 warmup schedule in `pinn_architecture.md` | Full-Batch / sL-BFGS |
| 4-6 | $10^{-3} \times (0.7)^k$ | 3 | See PHYS-05 warmup schedule in `pinn_architecture.md` | sL-BFGS |

*Stage-by-stage guide for key dynamic hyperparameters.*

## Implementation Notes

- **Monitoring**: Use TensorBoard to log loss components
  ($\mathcal{L}_{\text{data}}, \mathcal{L}_{\text{IC}}, \mathcal{L}_{\text{phys}}^{\text{causal}}, \mathcal{L}_{E}, \mathcal{L}_{L}$),
  scheduled loss weights, gradient statistics, and conservation metrics.

- **Checkpointing**: Save model checkpoints after each stage completion.

- **Error Handling/Edge Cases**: Monitor for NaN gradients during close
  encounters; if encountered, follow the PHYS-03 training-softening ablation
  contract in `pinn_architecture.md` or tighten clipping. Do not ad hoc alter
  the static-invariant `epsilon_inv` used for offline invariant computation.

- **Reproducibility**: Drive runs from a three-level Hydra YAML
  configuration:

  - `stage.yaml` -- curriculum definition and dataset indices.

  - `opt.yaml` -- optimizer settings, learning-rate schedule, clip
    norms.

  - `loss.yaml` -- default loss weights, PHYS-05 warmup schedule, causal
    residual settings, conservation regularizer scales, and tolerances.

With the training complete, we next discuss some additional
considerations: potential architectural tweaks to further improve
performance (especially on modest hardware), evaluation metrics to
quantify success, and overall recommendations.

# Advanced Considerations and Best Practices

## Evaluation Metrics and Validation

Evaluating a PINN on a chaotic problem demands more than just looking at
mean squared errors. As noted, even a physically correct model will
eventually diverge from the ground truth trajectory due to chaos, so we
need robust, physics-informed metrics:

- **Conservation of Invariants:** We track how well the model conserves
  total energy $E$ and total angular momentum $L$ over long
  trajectories. To test this, we can take a given initial condition
  (perhaps one from the test set or even outside the training set), use
  the PINN to predict its state over a long time (many Lyapunov times),
  and then compute $E$ and $L$ at each step from the PINN's output.
  Ideally, these should remain nearly constant (within a small drift).
  In our results, the final model shows minimal energy drift (e.g.,
  relative energy error staying below $0.1\%$ over very long times) even
  when the trajectory itself has diverged from the exact solution. This
  indicates the model has truly learned the physics law (Newton's
  $1/r^2$ force and corresponding conservation laws). If a model had low
  MSE for a while but eventually grew large errors and showed energy not
  conserved (drifting significantly), that would be a red flag that it
  was not capturing the true dynamics properly.

- **Prediction Horizon (Lyapunov Time):**

  > **Author note:** Should we also use the same definition here for the Lyapunov time from section 2.3 'Necessary Calculations of Invariants'?

  We quantify how
  long the model's predictions remain accurate in a chaotic sense by
  measuring the prediction horizon in units of Lyapunov time. For a
  given initial condition with Lyapunov time $\tau_L$, we find the time
  $T_{\text{pred}}$ at which the PINN's trajectory error (compared to a
  high-precision reference) becomes of order 1 (say the separation
  between PINN and true solution equals the size of the system). We then
  express $T_{\text{pred}}$ in terms of $\tau_L$. A good model might
  achieve $T_{\text{pred}} \approx \tau_L$ or even a bit more, meaning
  it can predict about as far as the chaos inherently allows. A poor
  model would have $T_{\text{pred}} \ll \tau_L$, meaning it diverges
  much sooner than it should. In testing our model, we found that it can
  often reach on the order of $1-2\tau_L$ of accurate prediction, which
  is reasonable given that beyond that, even the notion of a single
  "ground truth" trajectory is ambiguous due to chaos.

- **Long-Term Statistical Properties:** Another evaluation (if one
  doesn't want to rely on having ground truth for long times) is to
  check statistical properties. For example, in a chaotic three-body
  system, one might look at distribution of outcomes (like what fraction
  of systems eventually experience an ejection, or distribution of
  closest approach distances, etc.) as predicted by the PINN vs by
  direct simulation. This is more advanced and not explicitly in our
  docs, but it's a way to evaluate if the PINN at least gets the
  qualitative long-term behavior correct.

- **Standard Error Metrics on Short-Term Predictions:** Of course, we
  still use traditional metrics on short timescales. For instance, for
  each trajectory we can compute the mean squared error up to some fixed
  time (maybe up to one Lyapunov time, or some number of orbits). This
  gives a measure of how well the PINN fits the training data. During
  training, we monitor such metrics stage-wise to ensure the model is
  fitting the data within each stage's scope.

For deployment, the conservation laws metric is particularly important.
It means that if we use the PINN as a surrogate simulator, it will not
exhibit unphysical energy drift, so its outputs will remain physically
plausible even if they deviate from the exact path. This is crucial for
chaotic systems: we often care more that the solution behaves like a
real system (conserving invariants, eventually ergodically exploring
phase space, etc.) than tracking a specific trajectory indefinitely. In
our case, after the final active learning fine-tuning, the model passes
these tests: it conserves $E$ and $L$ to high precision and yields
prediction horizons proportional to the system's $\tau_L$ (which is
essentially the best one can hope for without true deterministic
tracking beyond chaos).

# Reproducibility Note (Ignore Now and Come Back Later):

All the above steps (data parsing, training loop, etc.) have been
described at a conceptual level. For actual code, one would implement
these in Python using libraries like PyTorch or TensorFlow for the PINN,
and perhaps JAX for automatic differentiation speed. The step-by-step
guide has provided all necessary components: how to compute losses, how
to schedule training, etc. As long as these instructions are followed
and the hyperparameters are tuned within reasonable ranges, one should
be able to reproduce the results.

Key details like resetting optimizer states, using full-batch L-BFGS
after plateau, updating loss weights dynamically, and using cumulative
data for replay are essential for success and have been explicitly
noted.

Most importantly, for rigorous provenance we drive every training run
from a three-level Hydra YAML stack:

- `stage.yaml` -- curriculum definition and data-set indices\ (Author Comment: why is there a "\" sign here and in the next line?)

- `opt.yaml` -- optimiser, learning-rate schedule, clip norms

- `loss.yaml` -- default loss weights, PHYS-05 warmup schedule, causal
  residual settings, conservation regularizer scales, and tolerances

A typical run is launched with:

    python train.py --config-dir conf --config-name stage.yaml

This command writes the fully resolved configuration into the run
folder, so every figure in the paper can be reproduced bit-for-bit.

# Supplementary Figures

> **Figure 1 (TikZ diagram not rendered):** Workflow diagram for COM-frame verification and input construction. This figure belongs to the *end of Step 2* (Preprocessing) and is reproduced here in the Appendix for reference. The diagram was generated from TikZ source in the LaTeX appendix; see the original `.tex` file for the definition.

> **Figure 2 (TikZ diagram not rendered):** End-to-end data-processing flow from Step 2 (Preprocessing) through Step 5 (Stage Assignment). After Step 3 computes and stores invariants ($E, Q, s_{\min}, L_{\mathrm{norm}}, I_{\mathrm{norm,raw}}, \tau_L$), Steps 4 and 5 run in parallel, both using these stored invariants. This complements Figure 1 above. The diagram was generated from TikZ source in the LaTeX appendix; see the original `.tex` file for the definition.

# Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the converted source body and were excluded from v1.3 fidelity comparisons.

## SI-CTL-001: Input-vector dimensionality inconsistency

Resolved by v1.4 finding B-03. See Phase 17 input contract.

===== END FILE ctl_instruction.md =====

===== BEGIN FILE data_quality_assessment.md =====
**Optimization of Data Validation Protocols for Causal Physics-Informed Learning in Chaotic N-Body Regimes**

**Research Report**

*April 27, 2026*

---

# 1 Introduction: The Intersection of Arbitrary-Precision Numerics and Causal Deep Learning

The integration of high-fidelity numerical analysis with deep learning represents a paradigm shift in the study of chaotic dynamical systems. The specific research stack under analysis—comprising the Brutus arbitrary-precision integrator written in C++, a Python-based data processing pipeline, and a Causal Training Labeled Physics-Informed Neural Network (CTL-PINN)—targets one of the most enduring challenges in classical mechanics: the Three-Body Problem. This system is characterized by non-linear interactions, extreme sensitivity to initial conditions, and phase space structures defined by the coexistence of stable invariant tori and chaotic seas. The successful modeling of such a system using neural networks requires a rigorous reassessment of what constitutes "high-quality" training data. Unlike traditional supervised learning tasks where data quality is often synonymous with label accuracy or noise reduction, the chaotic N-body problem imposes strict geometric and dynamical constraints—specifically symplectic conservation and phase space continuity—that must be preserved to ensure the learned model is physically viable.

The primary objective of this report is to define a comprehensive strategy for assessing training data quality prior to full model training. The analysis is driven by the unique requirements of the CTL-PINN architecture, which enforces temporal causality in the learning process, thereby making the model highly sensitive to the temporal coherence and physical consistency of the input data. We evaluate the comparative efficacy of static pre-training validation versus dynamic trial training, ultimately proposing a hybrid "Staged Gate" protocol. Furthermore, we develop a set of mathematically grounded metrics tailored to the arbitrary-precision nature of the Brutus dataset, ensuring that the inductive biases of the neural network align with the symplectic geometry of the underlying Hamiltonian physics.

## 1.1 The Computational Landscape: Brutus and the Bulirsch-Stoer Algorithm

To understand the data quality requirements, one must first analyze the source of the data. The Brutus code differs fundamentally from the symplectic integrators (such as Leapfrog or Wisdom-Holman) typically used in large-scale N-body simulations. Symplectic integrators preserve the geometric properties of the Hamiltonian flow (such as phase space volume) over long time scales but do so at the cost of local accuracy, often introducing a bounded energy error that oscillates but does not grow secularly. In contrast, Brutus utilizes the Bulirsch-Stoer algorithm combined with arbitrary-precision arithmetic to generate "converged" solutions.

The Bulirsch-Stoer method is an extrapolation scheme. It computes the solution at a future time $t + H$ by subdividing the interval $H$ into substeps, performing the integration with a modified midpoint method, and then extrapolating the results to zero step size using rational functions. Brutus iteratively increases the precision (word length $L$) and decreases the tolerance parameter $\epsilon$ until the solution converges to a specified number of significant digits. This implies that a Brutus-generated trajectory is not merely an approximation; within the specified precision, it is a "true" numerical solution that shadows the exact mathematical trajectory of the system.

However, this high fidelity comes with a specific data characteristic: non-uniform temporal sampling. The adaptive step-size controller in Brutus shrinks the time step $\Delta t$ dramatically during close encounters (pericenter passages) to maintain accuracy as the gravitational forces $F \propto 1/r^2$ diverge. Conversely, during excursive phases where bodies are widely separated, $\Delta t$ increases. While this is efficient for integration, it presents a "spectral bias" challenge for neural networks, which typically assume uniform sampling or at least sampling densities that correlate with the local Lipschitz constant of the target function in a way that is compatible with gradient descent dynamics. Consequently, "good" data for Brutus—defined by convergence—is not necessarily "good" data for a CTL-PINN without rigorous validation of its sampling density and local stiffness properties.

## 1.2 The Learning Architecture: Causal Training Labeled PINN (CTL-PINN)

The target model is a CTL-PINN. This architecture represents a refinement of the standard PINN formulation designed specifically for time-dependent evolution equations. Standard PINNs often suffer from "temporal causality violation," where the optimizer attempts to minimize the residual at a late time $t=T$ before having adequately resolved the solution at $t=0$. In chaotic systems, this is catastrophic because the solution at $t=T$ is exponentially sensitive to the trajectory at $t < T$. If the early trajectory is not learned correctly, the physics loss at later times provides incorrect gradient information, leading to convergence to unphysical local minima.

Causal training addresses this by introducing a weighting mechanism $w(t)$ into the loss function: $$\mathcal{L}(\theta) = \sum_{i=1}^{N_t} w_i \mathcal{L}_i(\theta) \tag{1}$$ where the weights $w_i$ are dynamically adjusted based on the cumulative loss at previous time steps. Typically, $w_i \propto \exp(-\lambda \sum_{j < i} \mathcal{L}_j)$. This forces the network to learn the trajectory sequentially, respecting the arrow of time.

This architectural choice imposes strict requirements on the training data. The data must be *causally continuous*. A gap in the data, a region of unphysical noise, or a "stiffness spike" (an under-resolved close encounter) at $t_{early}$ will result in a high residual $\mathcal{L}_{early}$. The causal weighting mechanism will then suppress the weights for all $t > t_{early}$ to zero, effectively halting the training process. Thus, for CTL-PINNs, data quality is not just about global accuracy; it is about the *continuity of learnability* along the temporal axis. A single "bad" segment renders the entire subsequent trajectory useless for training.

# 2 Assessment Strategy: Trade-offs Between Pre-Training Validation and Trial Training

The central strategic question is how to validate this complex data. The research identifies two primary methodologies: Static Pre-Training Validation (analyzing the dataset $\mathcal{D}$ itself) and Dynamic Trial Training (analyzing the interaction between $\mathcal{D}$ and the model $M$). Relying solely on one introduces significant risks.

## 2.1 Static Pre-Training Validation

This approach involves calculating physical and statistical metrics on the raw Brutus output (CSV/HDF5 files) before any tensor operations are initiated.

#### Advantages:

- **Computational Scalability:** Static checks are typically $O(N)$ or $O(N \log N)$ operations performed on CPUs. This is orders of magnitude cheaper than the iterative backpropagation required for training.

- **Physical Interpretability:** Errors detected here are directly mapped to physical concepts. If the angular momentum vector $\mathbf{L}$ precesses in a supposedly isolated system, the integration error is undeniable. This provides a clear "reject" criterion.

- **Sanitization:** It prevents "poisoning" the batch normalization statistics of a neural network. If a dataset contains outliers (e.g., numerical singularities where position $x \to \infty$ or $NaN$), these can skew the mean and variance statistics of the input layers, destabilizing the initialization of the entire network.

#### Limitations:

- **Invisibility of Optimization Landscapes:** A trajectory may be physically valid (conserves energy, continuous) but possess extremely high frequency components that are difficult for a Multi-Layer Perceptron (MLP) to resolve due to spectral bias. Static analysis cannot easily measure "spectral learnability" without performing Fourier transforms that may themselves suffer from sampling artifacts.

- **Interpolation Blindness:** PINNs evaluate residuals at *collocation points* which may not coincide with data points. Static analysis of discrete data points $t_i$ does not guarantee that the implicit interpolant between $t_i$ and $t_{i+1}$ is physical. If the Brutus time-step was too large, the "straight line" or "spline" connecting the points might violate conservation laws, even if the points themselves do not.

## 2.2 Dynamic Trial Training

This strategy involves training the specific CTL-PINN architecture on a small subset of the data (e.g., a single trajectory or a few batches) for a limited number of epochs.

#### Advantages:

- **Gradient Pathology Detection:** This is the only way to detect "exploding" or "vanishing" gradients caused by the specific interplay of the data's dynamic range and the network's activation functions. For N-body problems, where forces can scale by orders of magnitude during collisions, this is a critical check.

- **Causal Weight Verification:** It validates that the causal propagation mechanism is functioning. If the weights $w(t)$ do not advance past $t=0$ after 1000 epochs, it indicates that the initial conditions or the first few steps are "too stiff" for the current learning rate/architecture configuration.

- **Hyperparameter Sensitivity Check:** It helps distinguish between "bad data" and "bad hyperparameters."

#### Limitations:

- **Cost:** Requires GPU resources and significant time overhead per dataset if not strictly capped.

- **False Negatives:** A successful trial training on an "easy" segment of the orbit does not guarantee success on a "chaotic scattering" segment. The trial set must be carefully selected to be representative of the hardest physics.

- **Overfitting Ambiguity:** A model might easily overfit a single trajectory (memorization) without learning the underlying physics laws, providing a false sense of data quality. "Success" in trial training (low loss) might just mean the network is large enough to memorize noise.

## 2.3 The Optimal Strategy: The "Staged Gate" Protocol

The research suggests that the optimal strategy is a hybrid **Staged Gate Protocol**. This prioritizes the low-cost elimination of obviously bad data (Static Validation) before incurring the cost of probing subtle learnability issues (Trial Training).

**Phase 1: The Physics Gate (Static)**
- **Input:** Raw Brutus Trajectories.
- **Action:** Rigorous checking of conservation laws (Energy, Momentum) and symplectic consistency.
- **Outcome:** Binary Pass/Fail. Trajectories with drift $> \delta_{tol}$ are discarded immediately. This filters out integration failures.

**Phase 2: The Stiffness Gate (Static)**
- **Input:** Physically valid trajectories.
- **Action:** Analysis of Sampling Density vs. Local Curvature (using the SASD metric defined below).
- **Outcome:** Flagging. Trajectories are not discarded but marked as "High Stiffness." These require either resampling (running Brutus again with tighter tolerance) or specific "Curriculum Learning" schedules (introducing them later in training).

**Phase 3: The Learnability Gate (Dynamic)**
- **Input:** A stratified sample of Phase 2 survivors (specifically including High Stiffness cases).
- **Action:** "Overfit Challenge." Train the CTL-PINN on this single trajectory to machine precision.
- **Outcome:** Architectural Validation. If the model cannot overfit a single valid trajectory, the *architecture* (not the data) is insufficient (e.g., too shallow, wrong activation function).


<a id="tab:assessment_strategies"></a>

| **Feature**          | **Pre-Training Validation (Static)** | **Trial Training (Dynamic)** | **Staged Gate Protocol (Hybrid)** |
|----------------------|----------------------------------|--------------------------|-------------------------------|
| **Primary Metric**   | Physical Conservation, Continuity | Convergence Rate, Loss Value | Composite Score |
| **Computational Cost** | Low (CPU) | High (GPU) | Optimized (CPU first, GPU second) |
| **Detects**          | Integration Errors, Outliers | Gradient Issues, Hyperparams | Both + Architecture Mismatch |
| **Risk Addressed**   | Garbage In, Garbage Out | Model Divergence | Systemic Failure |
| **Blind Spot**       | Neural Network Inductive Bias | Physical Validity of Minima | None |

Table 1: Comparative Analysis of Assessment Strategies


# 3 Mathematically Grounded Metrics for Data Quality

To operationalize the Staged Gate Protocol, we must define specific metrics. These metrics extend beyond simple error checking; they quantify the *fitness* of the data for the specific task of causal physics-informed learning.

## 3.1 Symplectic Conservation Score (SCS)

While Brutus is an arbitrary-precision integrator, it is not inherently symplectic (it does not strictly preserve phase space volume by construction, unlike Leapfrog). However, for the data to be valid training material for a physics-informed model, it must exhibit the properties of a conservative Hamiltonian system $H(\mathbf{q}, \mathbf{p})$.

#### Derivation:

The Hamiltonian for the N-body problem is: $$H = \sum_{i} \frac{\mathbf{p}_i^2}{2m_i} - \sum_{i < j} \frac{G m_i m_j}{|\mathbf{q}_i - \mathbf{q}_j|} \tag{2}$$ For a physically valid solution, $\frac{dH}{dt} = 0$. In numerical data, errors manifest as energy drift.

#### Metric Definition:

We distinguish the raw trajectory-level Hamiltonian drift from its logarithmic score. The raw drift over the trajectory duration $T$ is: $$\epsilon_H = \max_{t \in [0, T]} \left| \frac{H(t) - H(0)}{H(0)} \right| \tag{3}$$ The Symplectic Conservation Score ($SCS$) is the base-10 logarithm of this raw drift: $$SCS = \log_{10}(\epsilon_H) \tag{4}$$ Throughout this document, $\epsilon_H$ denotes the raw Hamiltonian drift; $SCS$ denotes its base-10 logarithm. If $H(0)$ is zero or numerically near zero, $SCS$ is undefined; flag the trajectory for manual review or resimulation rather than forcing it through the logarithmic gate.

#### Thresholds for CTL-PINN:

- **$SCS \leq -10$ ($\epsilon_H \leq 10^{-10}$):** Excellent. Brutus has converged to high precision; ideal for training.

- **$-10 < SCS \leq -6$ ($10^{-10} < \epsilon_H \leq 10^{-6}$):** Acceptable. The drift is small enough that the trajectory data and Hamiltonian-conservation loss should remain mutually consistent during training.

- **$-6 < SCS \leq -5$ ($10^{-6} < \epsilon_H \leq 10^{-5}$):** Marginal. Keep only for review, diagnostics, or resampling decisions; do not use as clean training data without explicit justification.

- **$SCS > -5$ ($\epsilon_H > 10^{-5}$):** Reject. The trajectory exhibits significant Hamiltonian drift. A PINN trained on this will face conflicting gradients: the data loss tries to fit the drifting trajectory while the physics loss tries to enforce $\dot{H}=0$, leading to convergence failure.

#### Boundary Behavior:

The original thresholds used strict excellent, acceptable, and reject bands around $-10$, $-6$, and $-4$, leaving $SCS = -10$, $SCS = -6$, and the interval $[-6, -4]$ underdefined. The corrected thresholds close these gaps with non-strict boundaries and introduce a Marginal band for $-6 < SCS \leq -5$.

**Insight:** In chaotic systems, energy error often grows linearly or quadratically with time in non-symplectic integrators. A high SCS suggests the integrator step size was too large for the chaotic amplification factor of the specific orbit.

## 3.2 Stiffness-Aware Sampling Density (SASD)

Stiffness is the primary cause of failure for neural ODE solvers and PINNs. It occurs when the timescales of the system's components vary by orders of magnitude—common in N-body problems during close encounters where the dynamical time $\tau \sim \sqrt{r^3/GM}$ shrinks rapidly. Brutus handles this adaptively, but if the output data is saved at fixed intervals (or if the adaptive steps are too coarse for the *network's* capacity), the data will be "aliased" relative to the physics.

#### Metric Derivation:

We define a local stiffness proxy based on the curvature of the trajectory, which correlates with the acceleration magnitude $\|\mathbf{a}\|$. The sampling density is $\rho(t) = 1/\Delta t_i$. The metric compares the time step $\Delta t_i$ to the local characteristic timescale $\tau_{char} = \frac{\|\mathbf{v}\|}{\|\mathbf{a}\|}$ (time to change velocity direction significantly).

#### Metric Definition:

$$SASD_i = \frac{\Delta t_i}{\tau_{char}(t_i)} = \Delta t_i \cdot \frac{\|\mathbf{a}(t_i)\|}{\|\mathbf{v}(t_i)\|} \tag{5}$$ (To avoid division by zero at turning points, a more robust form uses the radius of curvature $\rho_{curv} = v^2/a_{\perp}$).

#### Interpretation:

- **$SASD \ll 1$:** The trajectory is over-sampled. The path between points is effectively linear. Safe for training.

- **$SASD \sim 1$:** The trajectory turns significantly between data points.

- **$SASD > 1$:** The trajectory is under-sampled. The particle performs a "sharp turn" or "cusp" between data points.

**Risk to CTL-PINN:** A high SASD value implies that the "causal link" between $t_i$ and $t_{i+1}$ is broken. The physics residual $\mathcal{L}_{physics}$ evaluated at a collocation point *between* these data points (using interpolation) will be massive because the interpolant cannot capture the cusp. This stops the propagation of causal weights. Data with $SASD > 0.5$ should be flagged for resampling.

## 3.3 Interpolation Physics Residual (IPR)

This is a critical "second-order" metric. PINNs do not just learn the data points; they learn a continuous manifold. Therefore, the *interpolant* implied by the data must satisfy the physics. If we use Cubic Hermite Splines (which preserve positions and velocities) to interpolate the Brutus data, does this spline satisfy Newton's laws? 

#### Protocol:

1.  Construct a piecewise Cubic Hermite Interpolating Polynomial (PCHIP) $\mathbf{q}_{spline}(t)$ using the data $\{(\mathbf{q}_i, \mathbf{v}_i)\}$.

2.  Sample $M$ synthetic "collocation points" $\tau_k$ uniformly distributed *between* the data points.

3.  Calculate the physics residual at these synthetic points: $$IPR = \frac{1}{M} \sum_{k=1}^{M} \left\| \frac{d^2 \mathbf{q}_{spline}}{dt^2}(\tau_k) - \mathbf{F}_{gravity}(\mathbf{q}_{spline}(\tau_k)) \right\|^2 \tag{6}$$

#### Relevance:

If $IPR$ is high, it means that even though the data points are correct, the "shape" of the trajectory between them (as defined by standard interpolation) is unphysical. This indicates that the data density is insufficient to constrain the continuous solution space of the PINN. The network will struggle to find a function that fits both the data points and the physics equation between them, leading to "wobbling" or high-frequency artifacts. This metric directly predicts the "Physics Loss" component of the PINN training.

## 3.4 Phase Space Coverage Entropy (PSC)

Chaotic systems are ergodic (or have ergodic components). For a model to generalize, the training data must cover the relevant phase space structures—both the stable regions (quasi-periodic orbits) and the unstable regions (close encounters, scattering). A dataset biased towards one will fail on the other.

#### Metric Definition:

We discretize the phase space of interest (e.g., the $r_{12}, r_{23}$ distance plane or the Poincaré section) into a grid of $K$ bins. Let $p_k$ be the probability of a data point falling into bin $k$. The Shannon Entropy is: $$H_{data} = - \sum_{k=1}^{K} p_k \log p_k \tag{7}$$

#### Application:

- **Low Entropy:** The data is clustered in a small region (e.g., all particles far apart). The model will fail to learn close-encounter dynamics.

- **High Entropy:** The data explores diverse configurations.

- **Stiffness Coverage Ratio:** Specifically check the bin corresponding to $r_{min} \to 0$. If this bin is empty, the dataset lacks the "hard" physics examples necessary to train the network to handle singularities. The report recommends "Importance Sampling" to enrich the dataset with these high-stiffness events.

# 4 Risks to Model Parameters and Causal Training Dynamics

The user query specifically asks to address "risks to model parameters." In the context of CTL-PINNs and chaotic data, these risks are non-trivial and often structural.

## 4.1 The Causal "Firewall" Effect

The causal loss weighting is defined as $w_i = f(\sum_{j<i} \mathcal{L}_j)$.

- **Risk:** If the data contains a single "bad" point (high IPR or SASD) at time $t_{bad}$, the residual $\mathcal{L}(t_{bad})$ remains high. Consequently, the weights for all $t > t_{bad}$ vanish ($w_t \to 0$).
- **Parameter Consequence:** The gradients $\frac{\partial \mathcal{L}}{\partial \theta}$ for parameters governing the late-time behavior become zero. These parameters effectively "die" or drift randomly. The model learns the trajectory perfectly up to $t_{bad}$ and then flatlines. This is a specific failure mode of causal training that does not exist in standard PINNs (which would just average the error globally).
- **Mitigation:** The SASD metric acts as a pre-training filter to prevent these "causal firewalls."

## 4.2 The Dead Neuron Problem in N-Body Scaling

N-body data is scale-invariant but numerically vast. Distances can range from $10^{-3}$ (close encounter) to $10^2$ (ejection).

- **Risk:** If the data is fed raw into the network, the inputs will push the neurons into the saturation regions of their activation functions (e.g., $\tanh(100) \approx 1$, gradient $\approx 0$).
- **Parameter Consequence:** Vanishing gradients in the first layer. In a deep network, this prevents feature extraction.
- **Mitigation:** The validation pipeline must include a Normalization Check. Calculate the Kullback-Leibler (KL) divergence between the input data distribution and a standard normal distribution $\mathcal{N}(0, 1)$. If $D_{KL}$ is high, the data requires log-scaling or robust standardization (e.g., using median and IQR instead of mean/std to handle outliers) before training.

## 4.3 Spectral Bias and High-Frequency Oscillations

Neural networks satisfy a "Spectral Bias" principle—they learn low-frequency functions quickly and high-frequency functions slowly.

- **Risk:** Chaotic trajectories often possess a broad frequency spectrum. If the data contains high-frequency oscillations (e.g., a tight binary subsystem orbiting a third body), the PINN will smooth over them, effectively learning a "mean field" approximation rather than the true dynamics.
- **Parameter Consequence:** The weights responsible for high-frequency features will not converge within standard training times.
- **Mitigation:** Use the IPR metric to detect high-frequency content. If detected, the architecture should be augmented with Fourier Feature mappings (positional encoding) to shift the spectral bias of the network.

# 5 Detailed Implementation Protocol: The "Staged Gate" Workflow

This section synthesizes the research into a coherent, actionable workflow for the research team.

## 5.1 Phase 1: Data Ingestion and Static Auditing (CPU)

This phase runs on the entire generated dataset.

1.  **Load and Normalize:**

    - Load $(\mathbf{q}, \mathbf{p}, t)$ from Brutus output.

    - Check for NaN or Inf.

    - Compute trajectory-level $\epsilon_H$ (raw Hamiltonian drift) and $SCS = \log_{10}(\epsilon_H)$. **Gate:** Reject if $\epsilon_H > 10^{-5}$, equivalently if $SCS > -5$.

2.  **Stiffness Analysis:**

    - Compute accelerations $\mathbf{a}_i$ and velocities $\mathbf{v}_i$.

    - Compute $SASD$ profile.

    - **Gate:** If $\max(SASD) > 0.5$, flag for "Resampling." Do not train on this trajectory yet. It requires finer Brutus output steps.

3.  **Manifold Check (IPR):**

    - Fit Cubic Hermite Spline.

    - Sample 10 synthetic points per interval.

    - Compute $IPR$.

    - **Gate:** If $IPR > 10^{-3}$, the data is aliased. Reject or Resample.

## 5.2 Phase 2: The "Overfit Challenge" (GPU)

This phase runs on a randomly selected *subset* (e.g., 1%) of the passing data to validate the configuration.

1.  **Setup:** Initialize the exact CTL-PINN architecture intended for full training.

2.  **Challenge:** Attempt to overfit a *single* stiff trajectory (one that passed Phase 1 but had high SASD).

3.  **Monitoring:**

    - Track Loss $\mathcal{L}_{train}$.

    - Track Causal Weights $w(t)$ evolution.

    - Track Gradient Norms $\|\nabla_\theta \mathcal{L}\|$.

4.  **Success Criteria:**

    - $\mathcal{L}_{train}$ converges to machine precision ($< 10^{-6}$).

    - Causal weights propagate to $t=T$ (i.e., the "firewall" is breached).

5.  **Diagnostic:**

    - If loss plateaus: Architecture is too small (under-parameterized).

    - If weights don't propagate: Causal parameter $\lambda$ is too high (too strict).

    - If gradients explode: Normalization is incorrect.

## 5.3 Phase 3: Dataset Composition and Augmentation

1.  **Diversity Check:** Compute Phase Space Entropy ($H_{data}$) on the accepted dataset.

2.  **Balancing:** If the dataset is dominated by stable orbits (low entropy), use **Importance Resampling**. Run Brutus specifically initialized in "chaotic" regions (e.g., using the figure-8 or Pythagorean 3-body initial conditions) to generate more high-entropy examples.

3.  **Symmetry Augmentation:** Apply $SO(3)$ rotations and translations to valid trajectories to increase dataset size without computational cost, ensuring the PINN learns rotational invariance.

# 6 Synthesis and Conclusion

The development of a robust CTL-PINN for the Three-Body Problem requires moving beyond the notion of data "accuracy" to the more complex notion of data "fitness for causal learning." The analysis reveals that the primary risks—spectral bias, causal firewalls, and dead gradients—stem from the mismatch between the continuous nature of the PINN and the discrete, variable-density nature of the Brutus data.

By implementing the **Staged Gate Protocol**, the research team can decouple these risks. Phase 1 (Static) ensures the physics is sound and the sampling density is sufficient to support a continuous manifold (low IPR). Phase 2 (Dynamic) ensures the network architecture has the capacity to resolve the specific stiffness profile of the data without gradient pathologies.

This rigorous, multi-layered approach ensures that the computational investment in arbitrary-precision data generation yields a dataset that is not just numerically correct, but algorithmically effective for training the next generation of physics-informed neural solvers.

## 6.1 Recommendations for Future Work

- **Curriculum Learning:** Implement a curriculum where the model is trained first on "easy" (low SASD) trajectories and progressively introduced to "hard" (chaotic, high SASD) trajectories. This stabilizes the causal weights.

- **Adaptive Activation Functions:** Investigate using adaptive activation functions (like Rowdy or locally adaptive sine) to handle the varying frequency content of the N-body problem better than fixed Tanh/ReLU.

- **Symplectic Neural Networks:** Consider modifying the architecture to be inherently symplectic (HNN), moving conservation from a soft loss term to a hard architectural constraint, which reduces the data quality burden regarding energy drift.

# Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the converted source body and were excluded from v1.3 fidelity comparisons.

## SI-DQA-001: Orphaned bibliography.tex — 33 references never cited in body

- Source section: `bibliography.tex` (orphaned — never imported by `main-data-quality-assess.tex`).
- Markdown heading: N/A (excluded from conversion — bibliography is not part of the audit corpus per D-28).
- Note: The LaTeX source includes `sections/bibliography.tex` with 33 `\bibitem` entries, but `main-data-quality-assess.tex` contains zero `\input{sections/bibliography}` lines and the body contains zero `\cite{}` commands. The 33 references are inaccessible in the compiled LaTeX output. Both markdown candidates independently fabricated reference lists (top-level: 32 numbered entries with `## References` heading; pandoc: 32 unnumbered entries with orphan `99` token). These fabricated reference lists were stripped during Phase 11 Plan 02 as they represent content not present in the LaTeX source body. The question of whether the 33 references should be reconnected to the document body with proper `\cite{}` commands is a LaTeX source edit — outside v1.3 scope.

## SI-DQA-002: Superseded — initial audit missed SCS gate inconsistency

- Source sections: `data_quality_metrics.tex` and `implementation_protocol.tex`.
- Markdown headings: `3.1 Symplectic Conservation Score (SCS)` and `5.1 Phase 1: Data Ingestion and Static Auditing (CPU)`.
- Note: The Phase 11 section-by-section audit recorded "no source-level concerns" here. That finding was incorrect: a logarithmic-vs-raw-drift category error in the Phase 1 SCS gate was missed. See **SI-DQA-003** for the correction.

## SI-DQA-003: Source-level SCS gate inconsistency corrected

- Source sections: `data_quality_metrics.tex` and `implementation_protocol.tex`.
- Markdown headings: `3.1 Symplectic Conservation Score (SCS)` and `5.1 Phase 1: Data Ingestion and Static Auditing (CPU)`.
- Note: The original LaTeX source defined $SCS$ as a logarithmic value but used the raw-drift threshold syntax `|SCS| > 10^{-5}` in the Phase 1 gate. The source has been corrected to distinguish raw Hamiltonian drift $\epsilon_H$ from logarithmic score $SCS = \log_{10}(\epsilon_H)$, and the gate now reads $\epsilon_H > 10^{-5}$, equivalently $SCS > -5$. The Reject threshold was tightened from `SCS > -4` to `SCS > -5` under the ratified gate-led policy.

===== END FILE data_quality_assessment.md =====

===== BEGIN FILE pinn_architecture.md =====
---
author: Starlordpd233
date: 2026-03-21
---

# A Definitive Implementation Blueprint for a Hybrid SQR-SkipResNet-SIREN PINN with Soft Conservation Regularization for $\mathrm{N}$-Body Dynamics

# 1. Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems

The accurate and long-term simulation of $\mathrm{N}$-body gravitational
systems, particularly the notoriously chaotic three-body problem,
presents a formidable challenge for traditional numerical and machine
learning methods alike. The dynamics are characterized by an extreme
sensitivity to initial conditions, where infinitesimal perturbations can
lead to exponentially divergent trajectories over time. Furthermore, the
solutions often contain a complex mixture of smooth, quasi-periodic
motion and sharp, high-frequency events that occur during close
encounters between bodies. A successful predictive model must therefore
not only capture these multi-scale temporal features with high fidelity
but also adhere to fundamental global conservation laws, such as the
conservation of total energy and angular momentum, to ensure its
long-term physical plausibility.[1]

A generic neural network architecture, such as a standard Multi-Layer
Perceptron (MLP), lacks the specific structural priors necessary to
handle this confluence of challenges. Such models often suffer from a
\"spectral bias,\" a tendency to learn low-frequency functions more
easily, which makes them struggle to represent the high-frequency
components inherent in chaotic dynamics.[2] More critically, enforcing
the governing physical laws---in this case, Newton's laws of
motion---within a Physics-Informed Neural Network (PINN) framework
requires the computation of high-order derivatives of the network's
output. For the $\mathrm{N}$-body problem, this involves calculating the
second derivative of the predicted position with respect to time,
$\frac{\mathrm{d}^2 \mathrm{r}}{\mathrm{d} t^2}$, to form the physics
residual term in the loss function. Common activation functions like the
Rectified Linear Unit (ReLU) are fundamentally unsuitable for this task.
While computationally efficient, ReLU produces a piecewise linear
output, meaning its first derivative is piecewise constant and its
second derivative is a series of Dirac delta functions (i.e., zero
almost everywhere). This mathematical property makes it impossible to
represent the smooth, continuously varying gravitational
forces that govern celestial motion.[1]

To overcome these fundamental limitations, a more principled approach is
required---one where the architecture itself imparts a strong inductive
bias that aligns with the underlying physics. The framework detailed in
this report proposes a hybrid PINN that is not an arbitrary collection
of techniques but a meticulously co-designed system. Each architectural
component is deliberately chosen to counteract a specific,
well-understood failure mode of standard models when applied to chaotic
physical systems. This synergistic design methodically addresses the
core requirements of the problem:

1.  **Derivative Fidelity:** To accurately enforce the physics residual,
    the network must be built with an activation function that is
    infinitely differentiable ($\mathrm{C}^\infty$) and whose
    derivatives are well-behaved. The Sinusoidal Representation Network
    (SIREN) architecture, which uses the sine function as its
    nonlinearity, is the ideal choice. The derivative of a sinusoid is
    another sinusoid, merely phase-shifted, a property that is preserved
    for higher-order derivatives. This provides a powerful inductive
    bias towards learning smooth functions whose derivatives are also
    smooth, a property essential for minimizing the physics residual
    with high fidelity.[1]

2.  **Expressivity and Training Stability:** Capturing the intricate
    complexity of chaotic trajectories requires a network with
    significant expressive capacity, which is typically achieved through
    depth. However, training very deep neural networks is notoriously
    difficult due to the well-known problems of vanishing and exploding
    gradients. The Residual Network (ResNet) backbone provides a
    solution by incorporating \"skip\" connections that create an
    identity mapping shortcut, allowing gradients to flow unimpeded
    through the network's depth. This report specifies the use of a
    particularly effective variant, the Power-Enhanced SkipResNet
    (SQR-SkipResNet), which has been empirically shown to provide more
    stable gradient flow and superior performance on non-smooth
    functions, making it well-suited for deep architectures.[1]

3.  **Long-Term Physical Plausibility:** Even a PINN that perfectly
    satisfies the local, instantaneous equations of motion can
    accumulate numerical drift over long time horizons, leading to
    unphysical outcomes such as a gradual increase or decrease in the
    total energy of an isolated system. The proposed architecture keeps
    the model as a position-prediction network and incorporates global
    conservation behavior as soft penalty terms in the loss. The energy
    term evaluates the analytic matched-Plummer Hamiltonian $H_\epsilon$
    from predicted positions and AD-derived velocities, then penalizes
    drift from the initial value. The angular-momentum term similarly
    penalizes componentwise drift from the initial angular momentum.
    These are soft conservation regularizers, not hard conservation laws
    and not architecture-level conservation constraints.

This philosophy of pragmatic hybridization, which combines
architecture-level derivative fidelity with loss-level physics
constraints, is a central theme of the proposed design. The resulting
model is a synergistic whole, where the SQR-SkipResNet enables the
necessary depth for expressivity, the SIREN activations provide the
derivative fidelity required for physics enforcement, and the soft
conservation regularizers improve long-term physical plausibility.

Author Comment: Again, all the superscript instances are rendered as raw literal strings in the preview. Fix this carefully.

# 2. The SQR-SkipResNet-SIREN Backbone: A Deep Dive into the Core Architecture

This section provides the definitive, mathematically-grounded
specifications for each component of the neural network's core
structure. Every choice is justified by its contribution to the model's
ability to represent complex physical phenomena accurately and to be
trained stably.

## 2.1 The Sinusoidal Activation (SIREN): The Key to Derivative Fidelity

The foundational element of the network's layers is the Sinusoidal
Representation Network (SIREN) activation function. This choice is not a
tunable hyperparameter but a mandatory architectural feature dictated by
the physics of the $\mathrm{N}$-body problem. A standard neural network
layer performs an affine transformation followed by a non-linear
activation. In a SIREN layer, this activation is the sine function[5]:
$$\phi_i(\mathrm{x}) = \sin(\mathrm{W}_i \mathrm{x} + \mathrm{b}_i)$$
where $\mathrm{x}$ is the input to the layer, and $\mathrm{W}_i$ and
$\mathrm{b}_i$ are the trainable weight matrix and bias vector,
respectively.

The primary motivation for this choice lies in the properties of its
derivatives. The derivative of a sinusoidal function is another
sinusoid, merely phase-shifted and scaled. For a single neuron with
activation
$\phi(\mathrm{x}) = \sin(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b}))$,
the chain rule gives:
$$\frac{\mathrm{d} \phi}{\mathrm{d} \mathrm{x}} = \omega_0 \mathrm{w} \cos(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b})) = \omega_0 \mathrm{w} \sin(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b}) + \frac{\pi}{2})$$

This property is recursive; higher-order derivatives of the network's
output with respect to its input remain well-behaved, smooth, sinusoidal
functions. This is a stark contrast to common activations like ReLU,
whose second derivatives are ill-defined or zero almost everywhere,
making them fundamentally unsuited for problems where the loss function
depends on second-order derivatives, as is the case for the
$\mathrm{N}$-body problem's physics residual.[1] The SIREN architecture
thus provides an exceptionally strong inductive bias for representing
the smooth, continuous solutions and their derivatives required by the
governing physical laws. This directly overcomes the spectral bias of
standard MLPs, which struggle to represent the high-frequency details
inherent in chaotic trajectories and their derivatives.[2] By using
SIREN, the network is inherently capable of representing the complex
natural signals that arise from physical systems.[8]

## 2.2 A Principled Initialization Scheme for SIREN Layers

The successful training of a deep SIREN is critically dependent on a
specific, principled initialization scheme. Naive initialization will
cause the distribution of activations to either collapse to zero or
explode into saturated regimes, halting the learning process. The
confusion between different documents regarding the hyperparameter
$\omega_0$ is resolved here by adhering to the original,
mathematically-derived SIREN initialization scheme, which is designed to
preserve the distribution of activations as they propagate through the
network.[5]

This scheme is not a heuristic but a carefully designed solution to two
distinct challenges: representation and trainability. It treats the
first layer of the network differently from all subsequent hidden
layers.

1.  **First Layer (for representation):** The initial frequency parameter
    `first_omega_0` is fixed at `30` and is not scheduled during training.
    A high initial frequency injects a high-frequency Fourier basis that
    helps the network overcome spectral bias from the outset. There is no
    epochwise or optimizer-step `omega0` scheduler. If `first_omega_0` is
    ever retuned, it is changed only as a stage-boundary ablation with a
    fresh re-initialization between runs — never mutated inside a run.

2.  **Subsequent Hidden Layers (for Trainability):** For all other
    hidden layers, the weights $\mathrm{W}$ are initialized from a
    different uniform distribution,
    $\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]$.\
    The crucial difference is that the initialization range is **divided by** $\text{hidden\_omega\_0}$ (here $\text{hidden\_omega\_0} = 1$), following the standard SIREN initialization.
    This specific scaling is mathematically derived to ensure that the
    pre-activations (the inputs to the sine function) maintain a
    standard normal distribution throughout the network's depth. This,
    in turn, keeps the sine activations in a dynamic, non-saturated
    range, preventing the frequency of the network's output from growing
    uncontrollably with depth. This careful, layer-dependent
    initialization is what makes deep SIRENs trainable by ensuring
    stable gradient flow.[1]

    Author Comment: All of these fields with `\text{xxx}` are not rnedered correctly and show up in the preview as raw literal text strings. The examples are the hidden omega 0, and first omega, etc. 

## 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation

While the SIREN initialization enables training, pushing to the depths
required for chaotic dynamics (e.g., 12 layers) requires stabilization
of the residual connections. This report adopts an advanced ResNet
variant with a project-specific (author) modification: **Layer
Normalization (LayerNorm)** applied to the skip path before the power
term. This LayerNorm stabilizer is an author addition for this project —
it is **not** part of the original SQR-SkipResNet formulation — and it
is applied on the skip/power branch only. This resolves gradient
instability while preserving the architecture's benefits for chaotic
systems.

The precise mathematical update rules are as follows:

1.  For odd-numbered layers ($l = 1, 3, 5, \ldots$):

$$\mathbf{x}^{(l)} = f_{\text{sr}}^{(l)}(\mathbf{x}^{(l-1)}) + \left(\text{LayerNorm}(\mathbf{x}^{(l-1)})\right)^p$$

    where:

    - $f_{\text{sr}}^{(l)}$: SIREN block (SineLayer)

    - $\text{LayerNorm}(\mathbf{x})$: Normalizes input to zero mean and
      unit variance per feature

    - $p = 2$: Power term fixed at 2 (element-wise squaring)

2.  For even-numbered layers ($l = 2, 4, 6, \ldots$):

$$\mathbf{x}^{(l)} = f_{\text{pn}}^{(l)}(\mathbf{x}^{(l-1)})$$

### Critical Rationale for LayerNorm

A critical enhancement to the standard SQR-SkipResNet is the application
of Layer Normalization to the skip path *before* the element-wise
squaring operation. During simulated close encounters, the inputs to
these layers (which represent positions and velocities) can vary over
orders of magnitude. Without normalization, the squaring operation would
amplify these large values, leading to catastrophic gradient explosions.
By normalizing the input on the skip path to have zero mean and unit
variance, this modification stabilizes the training process while
preserving the expressive power of the non-linear power term, which is
crucial for modeling the sharp transitions characteristic of close
encounters.

The default contract uses `elementwise_affine=False` (no learnable
affine parameters on the normalizer). Enabling affine parameters
(`elementwise_affine=True`) or removing LayerNorm entirely are optional
future ablations, not the Phase 20 default.

### Power Term Justification

The power term $p = 2$ remains critical for modeling non-smooth
dynamics. For 3-body systems, close encounters produce
velocity/acceleration spikes that require quadratic interaction terms to
resolve. $\text{LayerNorm}$ ensures this term remains bounded.

## 2.4 Finalized Architectural Hyperparameters
Author Comment: I'm not sure why this section is formatted like this. It looks like broken syntax to me and it displays in the preview simply as a paragraph. Look into this.

**Table 1: Architectural hyperparameters of the SQR-SkipResNet-SIREN backbone**

| **Hyperparameter** | **Recommended Value** | **Rationale & Justification** |
| --- | --- | --- |
| Backbone | SQR-SkipResNet with SIREN layers | Superior stability and convergence for non-smooth dynamics, ideal for modeling close encounters in chaotic systems. |
| Depth | 12 hidden layers (6 SQR-SkipResNet blocks) | Provides a good balance between the expressive power needed for chaotic dynamics and the trainability on modest hardware. |
| Width | 256 neurons/layer | A strong default that balances model expressivity and computational cost, avoiding the diminishing returns of excessively wide layers.[1] |
| Activation | $\sin(\mathrm{x})$ (SIREN) | The $\mathrm{C}^\infty$-smoothness is mathematically essential for accurately calculating the second-order derivatives required in the physics loss.[1] |
| LayerNorm | elementwise_affine=False, eps=1e-5 | Stabilizes skip path gradients without restricting feature learning. Applied only to odd layers. |
| first_omega_0 | 30 | A high initial frequency injects a high-frequency basis into the network, helping it overcome spectral bias from the outset.[1] |
| hidden_omega_0 | 1 | This value is used within the principled weight initialization formula for hidden layers to ensure a stable distribution of activations, enabling deep network training.[1] |
| Weight Init. (First) | $\mathrm{U}\left[-\frac{1}{n_{\text{in}}}, \frac{1}{n_{\text{in}}}\right]$ | The mathematically-derived initialization for the first SIREN layer to create a random Fourier feature mapping.[1] |
| Weight Init. (Hidden) | $\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]$ | The principled initialization for all subsequent SIREN layers, designed to preserve activation variance and enable stable training of deep sinusoidal networks.[1] |
| Skip Cadence | Alternating (per SQR SkipResNet) | The alternating pattern of plain and power-enhanced residual layers effectively balances feature transformation and stable gradient flow.[1] |
| Power Term (p) | 2 (element-wise square) | Empirical results demonstrate that $p=2$ provides significant improvements in stability and accuracy without excessive computational overhead.[1] |
| Output Activation | None (Linear) | The final layer must be linear to allow the predicted positions to take on any real value required by the physical system. |

# 3. The Multi-Component, Physics-Constrained Loss Function

The training of the PINN is guided by a composite loss function that
simultaneously optimizes for three distinct yet complementary
objectives: fidelity to observed data, adherence to the governing laws
of physics, and soft conservation of total system energy and angular
momentum. This multi-component objective enables the network to learn
solutions that are not only accurate but also physically plausible and
generalizable beyond the specific training data points.

The default Phase 19 training objective is:

$$L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$

Author Comment: the above formula is not written in the correct syntax. We need to fix it so that it will be rendered correctly in markdown preview in Cursor.

Canonical text form: $L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$.

Author Comment: the above canonical text form is also rendered in raw text strings in preview.

This is the baseline penalty-term formulation. No dual variables are
part of the default training loss; the scalar-conservation augmented
Lagrangian option is documented only as a P2 ablation in §4.2.

## 3.1 Data Fidelity Term ($\mathcal{L}_{\text{data}}$): Anchoring to Ground Truth

The purpose of the data fidelity term is to ensure that the network's
predictions align with the high-precision trajectory data generated by a
trusted numerical integrator. This term grounds the general,
physically-plausible solution learned by the PINN to the specific
trajectory defined by a given set of initial conditions.

The data fidelity loss uses a Huber contract on scaled projected
positions:

$$L_{data} = \frac{1}{N_t} \sum_n \sum_i \operatorname{Huber}_{\delta_r}(r_{\theta,i}'(u_n) - r_i'(u_n))$$

Author Comment: again, the syntax is broken

where $\delta_r = 1$ is the default Huber transition. The previous
MAE/L1 data-loss prose is replaced by this Huber contract.

where:

- $u_n = t_n/T$ is the normalized physics time coordinate

- $r'_{\theta,i}(u_n)$ is the network's predicted **scaled
  position** vector (the direct output of the network)

- $r'_i(u_n)$ is the ground truth position from the BRUTUS
  data, **scaled by the characteristic length $D$** (i.e.,
  $r'_{\text{true}} = r_{\text{true}}/D$)

- $N_t$ is the number of sampled time points in a training batch

**Batch Construction:**

The data points are sampled from the BRUTUS trajectory snapshots as
follows:

``` {.python language="Python" caption="Listing 2: Data Batch Construction"}
def get_batch(batch_size, points_per_trajectory=32):
    """
    Sample batch_size trajectories from the dataset.
    For each trajectory, sample points_per_trajectory time points.
    
    Returns:
        t_k: Time points sampled from BRUTUS snapshots
        r_true: Corresponding ground-truth positions
        
    Shapes: (batch_size * points_per_trajectory, ...)
    """
    # Implementation details depend on dataset structure
    return t_k, r_true

# Total data points per batch
N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192
```

The time points $t_k$ are sampled from the discrete BRUTUS trajectory
snapshots available in the training dataset, representing specific
moments where high-precision numerical integration data is available.

  **[Author Comment: This above batch construction is not consistent with the CTL instruction plan. Look into this.]**

**Loss Integration Note:**\
The data term is unweighted in the default objective. Physics and
conservation terms are balanced by scheduled scalar weights, not by
default ALM dual updates.

## 3.2 Physics Residual Term ($\mathcal{L}_{\text{physics}}$): Enforcing Newtonian Dynamics

This term is the heart of the \"physics-informed\" paradigm. It enforces
the governing laws of physics---in this case, Newton's law of universal
gravitation---across the entire solution domain, not just at the
discrete points where training data is available. This is what endows
the network with the ability to generalize and make physically
consistent predictions at any point in time.

The physics residual, $f_i(u_n)$, for each body $\mathrm{i}$ is defined
as the discrepancy between the acceleration predicted by the neural
network (via automatic differentiation) and the acceleration dictated by
the gravitational forces from all other bodies $\mathrm{j}$:

The softened gravitational force between bodies i and j uses the
Plummer-softened distance:

$$r_{safe,ij} = \sqrt{||r'_{\theta,j}(u_n) - r'_{\theta,i}(u_n)||^2 + \epsilon_{train}^2}$$

where $\epsilon_{train} = 10^{-5}$ (`10^-5`) is the training-time softening
parameter. The force per unit mass is:

$$F_{ij} = m_j \frac{r'_{\theta,j}(u_n) - r'_{\theta,i}(u_n)}{r_{safe,ij}^3}$$

The residual is:

$$f_i(u_n) = a'_{\theta,i}(u_n) - \sum_{j \neq i} F_{ij}$$

The raw-mass nondimensionalization convention absorbs `G`; no free
dimensionless gravitational coefficient appears in the scaled residual.

where:

- $u_n$ : Normalized physics time coordinate $t_n/T$

- $r'$ : Positions scaled by $D$ (characteristic length)

- $a'$ : Accelerations scaled by $D/T^2$

- $m_j$ : Masses (unchanged, as $G=1$ in the dimensionless system)

- $\epsilon_{train} = 10^{-5}$ (`10^-5`) : Training-time Plummer softening parameter to prevent
  division by zero during close encounters

Define the per-time residual energy as:

$$\bar R_n = \frac{1}{3}\sum_{i=1}^{3} \| f_i(u_n) \|^2.$$

For sorted collocation times $u_1 < \cdots < u_{N_t}$, the default
causal weights are:

$$w_1 = 1,\qquad
w_n = \exp\left(-\eta_c \sum_{m=1}^{n-1} \operatorname{stopgrad}(\bar R_m)\right),
\quad n>1.$$

The default physics loss consumed by $L_{total}$ is therefore:

$$L_{phys}^{causal} = \frac{1}{N_t} \sum_{n=1}^{N_t} w_n \bar R_n.$$

The unweighted mean $\frac{1}{N_t}\sum_n \bar R_n$ may be logged as a
diagnostic, but it is not the default training loss.

**Collocation Point Sampling:**

The collocation points are sampled according to the following strategy:

``` {.python language="Python" caption="Listing 3: Collocation Points Sampling"}
import numpy as np

def sample_collocation_points(u_min=0.0, u_max=1.0, n_col=4096, strategy='uniform',
                            traj_data=None):
    """
    Sample normalized physics-time collocation points u in [0, 1].
    
    Args:
        u_min, u_max: Normalized physics-time boundaries (default: [0, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
        traj_data: Optional trajectory data for adaptive strategy
    
    Returns:
        u_col: Array of sampled normalized physics-time points
    """
    if strategy == 'uniform':
        u_col = np.random.uniform(u_min, u_max, size=(n_col,))
        
    elif strategy == 'adaptive':
        if traj_data is None:
            raise ValueError("Adaptive strategy requires traj_data")
        # Bias sampling toward high-acceleration regions
        weights = np.abs(traj_data['accelerations']).max(axis=1)
        
        # Safety check for degenerate cases
        if weights.sum() < 1e-8:
            weights = np.ones_like(weights)
            
        weights /= weights.sum()  # Normalize
        u_col = np.random.choice(traj_data['u'],
                                size=n_col, p=weights)
    else:
        raise ValueError("Invalid strategy")
        
    return u_col
```

Minimizing this term forces the network to learn a function
$\mathrm{r}_\theta(u)$ that is also a solution to the governing ordinary
differential equations (ODEs) in the normalized physics-time coordinate.

## 3.3 Initial Condition Anchor Loss ($L_{IC}$)

$$L_{IC} = L_{IC,r} + \beta_v L_{IC,v}$$

$$L_{IC,r} = (1/3) \sum_i ||r_{\theta,i}'(0) - r_i'(0)||^2$$

$$L_{IC,v} = (1/3) \sum_i ||v_{\theta,i}'(0) - v_i'(0)||^2$$

where $\beta_v = 1$ (`β_v = 1`) default, $\lambda_{IC} = 1$ default, and ablation
range $[0.1, 10]$. The velocity $v_\theta'(0)$ comes from the PHYS-02
componentwise normalized-time AD contract. This term is mandatory
(resolution §8.3).

This position and velocity anchor is evaluated at normalized physics
time `u=0`; because the network input uses $\tau = 2u - 1$, the
corresponding network-time input is `τ=-1`.

$L_{IC}$ uses squared error (not Huber): IC values come from
deterministic Phase 18 FRAME-01 preprocessing and are not outliers, so a
quadratic penalty enforces hard IC anchoring at `u=0`. $L_{data}$ uses
Huber (resolution §8.2) because data targets along the
curriculum-sampled trajectory are noisier and benefit from
outlier-robust loss.

## 3.4 Soft Energy Conservation Regularizer ($L_{E}$): Enforcing a Global Conservation Law

While the physics residual enforces the local, instantaneous laws of
motion, it does not explicitly guarantee the conservation of global
quantities over long time horizons. For an isolated mechanical system
like the $\mathrm{N}$-body problem, the total energy is one such
conserved quantity. The energy loss is a soft conservation regularizer:
the network predicts positions at each time step, velocities and
accelerations are computed via componentwise automatic differentiation,
and the analytic matched-Plummer Hamiltonian $H_\epsilon$ (`H_ε`) is
evaluated from the predicted positions and AD-derived velocities. This
penalty term discourages drift from the initial energy value; it is a
soft constraint, not a hard conservation law. The network does not
parameterize a Hamiltonian.

The matched-Plummer potential energy is:

$$V_\epsilon = -\sum_{i<j} \frac{m_i m_j}{r_{safe,ij}}$$

using the same $r_{safe,ij} = \sqrt{||r'_j - r'_i||^2 + \epsilon_{train}^2}$
as the residual force term. The matched-Plummer Hamiltonian is
$H_\epsilon = T' + V_\epsilon$ where $T'$ is the dimensionless kinetic
energy.

**Energy Conservation Regularizer (PHYS-04):**

$$L_{E} = \frac{1}{N} \sum_n \operatorname{Huber}(\Delta H_n, \delta=1.0)$$

where

$$\Delta H_n = \frac{H_\epsilon(r_\theta'(u_n), v_\theta'(u_n)) - H_\epsilon(r_0', v_0')}{|H_\epsilon(r_0', v_0')| + \epsilon_H}$$

The relative drift symbol is $\Delta H_n$.

$$epsilon_H = 1e-4 * S_H$$

$$S_H = median_train(K0 + Uabs0)$$

and $\delta = 1.0$ is the Huber transition.

$S_H$ is computed once in float64 after final
COM/zero-momentum/gauge/scaling preprocessing over the training split
using the matched-Plummer Hamiltonian components with
$\epsilon_{train} = 10^{-5}$. (Author Comment: I am not sure why there is a duplicate 10^-5 here)Persist both $S_H$ and $\epsilon_H$ in training metadata. $S_H$ must be finite and strictly positive; $S_H \leq 0$ or non-finite $S_H$ is a preprocessing/metadata validation failure. Do not apply a fallback numeric floor. Use $\epsilon_H$ only in $|H_0| + \epsilon_H$. Phase 21 reports activation behavior only and must not reselect $\epsilon_H$ unless a new user instruction opens a replacement gap.

The FUT-01 divergence handoff must flag executable training metadata as
divergent if it omits $S_H$ or $\epsilon_H$, computes $S_H$ from a
different split or preprocessing stage, computes $S_H$ per minibatch,
uses a fixed numeric $\epsilon_H$, or applies a max/fallback floor that is
not present in this canonical contract.

The term "Hamiltonian" here refers to the analytic energy function
$H_\epsilon$, not to a neural-network-parameterized Hamiltonian.

**Initial Energy Calculation:**

The initial energy $H_0$ is precomputed during dataset preprocessing:

``` {.python language="Python" caption="Listing 5: Initial Energy Calculation in Dataset Preprocessing"}
class TrajectoryDataset:
    def __init__(self, trajectory_data):
        # ... other initialization ...

        # Precompute H_0 for each trajectory
        self.H_0_values = {}
        for traj_id, traj in trajectory_data.items():
            self.H_0_values[traj_id] = self.compute_initial_energy(
                r0_prime=traj['r0_scaled'],  # Already scaled by D
                v0_prime=traj['v0_scaled'],  # Already scaled by D/T
                masses=traj['masses']
            )

    def compute_initial_energy(self, r0_prime, v0_prime, masses):
        """Compute H_0 in dimensionless units (G=1)"""
        H_0 = 0.0
        epsilon_train = 1e-5  # Training-time Plummer softening parameter

        # Fixed for 3-body problem
        N_bodies = 3

        # 1. KINETIC ENERGY (dimensionless)
        for i in range(N_bodies):
            H_0 += 0.5 * masses[i] * np.sum(v0_prime[i]**2)

        # 2. POTENTIAL ENERGY (dimensionless)
        for i in range(N_bodies):
            for j in range(i+1, N_bodies):
                r_vec = r0_prime[i] - r0_prime[j]
                r_sq = np.sum(r_vec**2)
                r_safe = np.sqrt(r_sq + epsilon_train**2)
                H_0 -= masses[i] * masses[j] / r_safe

        return H_0
```

**Key Implementation Notes:**

- **Unit System Consistency:** All quantities (positions $r'$,
  velocities $v'$, and initial energy $H_0$) must be expressed in the
  same non-dimensional ($G = 1$) system of units.

- **Softening Parameter:** The same value $\epsilon_{train} = 10^{-5}$ (author comment: again duplicate number)
  is used consistently in both the physics residual and energy
  calculations to prevent numerical instabilities during close
  encounters.

- **Collocation Points:** The same set of $N_{\text{col}}$ points is
  used for both physics and energy loss evaluation to ensure
  computational efficiency.

## 3.5 Angular Momentum Conservation Loss ($L_{L}$)

$$L_{L} = \frac{1}{3N_t} \sum_n \sum_\alpha \operatorname{Huber}\left(\frac{L_{\theta,\alpha}'(u_n) - L_{0,\alpha}'}{L_{scale}}, \delta=1.0\right)$$

where $\alpha \in \{x, y, z\}$, $L_{scale} = ||L_0'|| + \epsilon_L$,
and $\epsilon_L = 10^{-8}$ is a numerical-stability scale grounded in
resolution §8.6 and distinct from softening $\epsilon_{train}$ /
$\epsilon_{inv}$ and from $\epsilon_H$ (resolved by D-20 / GAP-19-01 as a
dataset-scale Hamiltonian floor, not a softening parameter).
Componentwise angular momentum Huber loss on relative angular-momentum
drift follows resolution §8.6. The velocity $v_\theta'(u_n)$ used to
compute $L_\theta'(u_n)$ comes from the PHYS-02 componentwise
normalized-time AD contract.

# 4. Advanced Training and Optimization Strategy

Successfully training the network requires a sophisticated approach to
navigate the complex, non-convex loss landscape and handle numerical
instabilities.

## 4.1 Loss Balancing via Warmup Schedule (PHYS-05)

$$L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$

Canonical text form: $L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$.

where:

- $L_{data}$: Huber loss on position predictions, $\delta_r = 1$ default
  (resolution §8.2).
- $L_{IC}$: Initial condition anchor (position + velocity at `u=0`),
  $\lambda_{IC} = 1$ default.
- $L_{phys}^{causal}$: Physics residual with causal weighting
  $w_n = exp(-\eta_c \sum_{m<n} stopgrad(\bar R_m))$, $w_1 = 1$,
  $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
  causal exponent to avoid underflow, but do not choose a numeric
  clipping bound in Phase 19; surface a gap if one is needed.
  The causal exponent clip is required only to avoid underflow.
- $L_{E}$: Soft energy conservation regularizer,
  see §3.4.
- $L_{L}$: Angular momentum conservation loss, see §3.5.
- No dedicated L_P term: linear momentum is enforced structurally by
  the Phase 17 COM projection head / zero-momentum output contract, so a
  separate linear-momentum loss would be redundant.

The warmup schedule is:

- $I_{warm} = min(2000, 0.1 \cdot N_{Adam,k})$
- $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
  default $\lambda_{phys}^{max}(k) = 1$
- $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$
- $\lambda_E(k, i)$ and $\lambda_L(k, i)$ warm up linearly with
  $i/I_{warm}$

Optimizer-phase semantics:

- During Adam epochs: $\lambda$ values may be scheduled per the warmup
  schedule; no dual variables are updated.
- During L-BFGS: $\lambda$ values are frozen; no dual updates inside a
  line search.
- Stage-boundary transitions: re-warmup applies per the new stage's
  $\lambda^{max}$ values.

The default loss is the penalty-term formulation above. Scalar
conservation augmented-Lagrangian machinery is not part of the baseline
training contract and is documented separately as the P2 ablation below.

## 4.2 Optional ALM Ablation (P2)

As a P2 ablation, an augmented Lagrangian method may be applied to scalar conservation constraints only:

- **Constraints:** $c_E = \mathrm{RMS}_n(\Delta H_n)$ (energy drift), $c_{L,\alpha} = \mathrm{RMS}_n((L'_{\theta,\alpha}(u_n) - L'_{0,\alpha}) / L_{scale})$ (angular momentum drift per component). (Author Comment: this syntax is not ideal since it invovles math equations/formula; it should properly use correct markdown render-friendly syntax)
- **Never apply ALM to the dense ODE residual.**
- **Dual-variable updates:** Only between Adam epochs or between deterministic refinement passes. Never update dual variables during L-BFGS or inside a line search.
- **Logging:** Log constraint values before and after each dual-variable update.
- **Default:** ALM is OFF. The default loss is the penalty-term formulation in §3-§4 above.

This P2 ablation is not part of the baseline training contract. It is documented for completeness and for future experimentation.

## 4.3 Two-Phase Optimization

To achieve both efficient exploration and high-precision convergence, a
two-phase optimization strategy is employed.

1.  **Phase 1 (Exploration):** The initial training phase utilizes the
    **Adam optimizer**. Its adaptive learning rates and momentum-based
    updates are well-suited for navigating the highly non-convex loss
    landscape in the early stages of training, efficiently finding a
    good basin of attraction.

2.  **Phase 2 (Fine-Tuning):** Once the Adam optimizer has converged,
    the process can be switched to a quasi-Newton method like **L-BFGS**
    to \"polish\" the solution. Because full-batch L-BFGS is
    memory-intensive, a mini-batch variant (Stochastic L-BFGS) is
    recommended for larger datasets.

## 4.4 Adaptive Gradient Clipping

A significant challenge arises from the inverse-square distance terms in
the loss function, which can explode during simulated close encounters.
To prevent a single event from destabilizing the optimizer, adaptive
gradient clipping is essential. A robust strategy is to clip the global
L2 norm of the gradients relative to their recent typical magnitude.

``` {.python language="Python" caption="Listing 6: Adaptive Gradient Clipping Logic"}
# Maintain a queue/list of the last 100 gradient norms
grad_history = [] 

# In training loop, after loss.backward():
total_norm = torch.norm(torch.stack([torch.norm(p.grad.detach()) for p in model.parameters()]))
grad_history.append(total_norm)
if len(grad_history) > 100:
    grad_history.pop(0)

# Clip norm to 5x the median of recent norms
clip_value = 5.0 * torch.median(torch.stack(grad_history))
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)

# Then, call optimizer.step()
```

# 5. Inference and Trajectory Generation

Once the model is trained, it can be used as a high-fidelity function
approximator to generate entire trajectories on demand.

## 5.1 Generating a Trajectory

To predict the evolution of a system from a given initial condition
($IC$), the following procedure is used:

1.  **Define Evaluation Times:** Create a fine-grained array of physical
    evaluation times, $t_{eval}$, over the desired simulation interval
    (e.g., 10,000 points from $t=0$ to $t_{max}$). Convert them to
    normalized physics time $u_{eval}=t_{eval}/T$. The model wrapper
    computes the bounded network coordinate $\tau = 2u - 1$ internally.

2.  **Predict Positions:** For each normalized physics-time point in
    $u_{eval}$, let the model wrapper concatenate $\tau = 2u-1$ with the
    constant $IC$ vector before calling the trained network. This produces
    a continuous trajectory of the system's positions, $r_{\theta}(u_{eval})$.

3.  **Derive Kinematics (Optional):** If velocities or accelerations are
    needed for analysis, derive them by differentiating with respect to
    the canonical autograd leaf $u$. The $2\times$ and $4\times$ chain-rule
    factors apply only to an implementation path that differentiates
    directly with respect to $\tau$.

## 5.2 Output Layer and Kinematic Consistency via Automatic Differentiation

### Network Input Contract

**Input Vector** A **14-dimensional vector** `[\tau, IC_{13}]`, where `u=t/T` is the autograd leaf and `\tau=2u-1` is the bounded network time coordinate. `IC_{13}` is the ordered Jacobi-state initial-condition vector defined canonically in `ctl_instruction.md` Step 4:

$$
IC_{13} = [m_1, m_2, m_3, \rho_x, \lambda_x, \lambda_y,
\dot{\rho}_x, \dot{\rho}_y, \dot{\rho}_z,
\dot{\lambda}_x, \dot{\lambda}_y, \dot{\lambda}_z, E].
$$

Mass, Jacobi-position, and Jacobi-velocity slots are independently normalized with `tanh((z - mu_z)/(sigma_z + 10^-8))` after the Phase 18 (FRAME-01) preprocessing contract. The energy slot uses `tanh(E / E_scale)` with `E_scale = |median_traj(E)| + 10^-8`. Componentwise derivative tests for the `u -> tau -> r` chain are specified in Phase 19 (PHYS-02).

### Output Layer

The network architecture is simplified and physical consistency is
hard-coded by predicting only positions and deriving all other kinematic
quantities via automatic differentiation (AD). This is a core design
principle of PINNs, supported by established frameworks like
DeepXDE.[14]

The final layer of the SQR-SkipResNet-SIREN network is a standard linear
layer without any activation function. This is crucial as it allows the
network's outputs---the predicted positions---to take on any real value
required by the physical system. The output is a 9-dimensional vector
representing the concatenated positions of the three bodies at a given
time $\mathrm{t}$:
$$\mathrm{r}_\theta(\mathrm{t}) = [\mathrm{r}_1(\mathrm{t}), \mathrm{r}_2(\mathrm{t}), \mathrm{r}_3(\mathrm{t})]$$

Crucially, the network does not predict velocities or accelerations
directly. Instead, these kinematic quantities are derived from the
projected position outputs using componentwise AD with respect to the
normalized physics-time input, $u=t/T$. The velocity vector is computed
as the first-order derivative of the projected position vector, and the
acceleration vector is computed as the second-order derivative:
$$v_\theta'(u) = \frac{d r_\theta'(u)}{d u} \quad \text{and} \quad a_\theta'(u) = \frac{d^2 r_\theta'(u)}{d u^2}$$

By computing derivatives via AD, the fundamental kinematic relationships
between position, velocity, and acceleration
$(\mathrm{v} = \mathrm{r}', \mathrm{a} = \mathrm{r}'')$ are satisfied by
construction to machine precision. This hard-codes a significant portion
of the problem's physics into the model, simplifies the network
architecture (as no extra heads are needed for velocity or
acceleration), and makes the overall learning task more tractable.

## 5.3 Output Frame and File Format

For consistency and physical correctness, the output of the model must
be clearly defined.

- **Reference Frame:** The predicted positions, $r_{\theta}(t)$, are in
  the **Center of Mass (COM) frame**. This is consistent with the use of
  translation-invariant quantities in the input vector.

The raw network head emits unconstrained positions

$$
\tilde r_\theta(u, IC_{13}) = [\tilde r_1, \tilde r_2, \tilde r_3] \in \mathbb{R}^9.
$$

Before any downstream consumer sees this output, the model applies a hard mass-weighted COM projection:

$$
R_{\mathrm{COM}} = \frac{\sum_{j=1}^3 m_j \tilde r_j}{\sum_{j=1}^3 m_j},
\qquad
r_i = \tilde r_i - R_{\mathrm{COM}}, \qquad i \in \{1,2,3\}.
$$

Here `m_j` denotes the ordered raw pre-tanh mass metadata supplied by the Phase 18 (FRAME-01) preprocessing output; it is not the normalized mass slot inside `IC_{13}`.

The projected positions

$$
r_\theta = [r_1, r_2, r_3]
$$

are the only positions consumed by data loss, physics residuals, IC loss, conservation loss, diagnostics, and evaluation metrics. The projection is architectural, not a soft penalty.

This projection is the model-output side of the Phase 18 FRAME-02
assertion: for every projected output, the mass-weighted position COM
is zero by construction. Since velocities and accelerations are
automatic derivatives of the projected positions, their mass-weighted
COM derivatives are zero by the same projection identity. Phase 21
executes the numerical acceptance checks; this section only states the
architectural guarantee.

### 5.3.1 Normalized-Time Derivative Contract (PHYS-02)

**Three-layer separation:** $(t, r, v)_{raw} \rightarrow (u, r', v')_{physics} \rightarrow (\tau, IC_{13})_{network}$ where `u=t/T` and $\tau = 2u - 1$.

**Canonical autograd leaf:** `u=t/T`. When the code path differentiates
with respect to `u`:

- $v' = dr'/du$ (velocity in scaled time, no chain-rule factor)
- $a' = d^2r'/du^2$ (acceleration in scaled time, no chain-rule factor)

**Conditional chain-rule factors for τ/tau:** If a code path
differentiates directly with respect to $\tau = 2u - 1$ (rather than
`u`), then:

- $v' = 2 \cdot dr'/d\tau$
- $a' = 4 \cdot d^2r'/d\tau^2$

These factors apply ONLY to the $\tau$-leaf code path.

**Componentwise derivatives required:** The residual and Hamiltonian
require all nine derivatives $dr'_{i,\alpha}/du$ ($i \in \{1,2,3\}$,
$\alpha \in \{x,y,z\}$). The following anti-pattern is FORBIDDEN:

**Forbidden:** `torch.autograd.grad(r.sum(), u, create_graph=True)` --
this computes a vector-Jacobian product against an all-ones covector,
not the nine individual derivatives.

**Acceptable patterns:**

- `torch.func.jacrev` + `vmap` over the batch dimension
- Explicit loop over the 9 projected output components
- Equivalent full-Jacobian method

**Worked synthetic-trajectory test:** For the test trajectory
$r'(u) = [sin(2πu), cos(2πu), u²]$ (one body, three components), the
symbolic derivatives are:

- $dr'/du = [2π cos(2πu), -2π sin(2πu), 2u]$
- $d^2r'/du^2 = [-4π² sin(2πu), -4π² cos(2πu), 2]$

AD outputs must match these symbolic derivatives to numerical
tolerance. Executable tolerance and the disposable probe belong to Phase
21 VER-04 / AC-PHYS-02.

```python
# Spec-illustrative AD pattern (not FUT-01 implementation prescription):
# Option A: jacrev + vmap for batched trajectories
from torch.func import jacrev, vmap

def model_single(u_scalar, ic13):
    """Single-trajectory forward pass."""
    tau = (2 * u_scalar - 1).reshape(1)  # u=0 maps to tau=-1
    ic13_vec = ic13.reshape(-1)
    return net(torch.cat([tau, ic13_vec]))

# dr'/du for all 9 output components on one trajectory:
drdu_single = jacrev(model_single, argnums=0)(u_scalar, ic13)  # shape (9,)

# Batch over trajectories:
drdu_batch = vmap(lambda u_b, ic_b: jacrev(model_single, argnums=0)(u_b, ic_b))(u_batch, ic13_batch)

# Option B: explicit per-component loop
# derivatives = []
# for k in range(9):
#     grad_k = torch.autograd.grad(r_prime[k], u, create_graph=True)[0]
#     derivatives.append(grad_k)
# drdu = torch.stack(derivatives)  # shape (9, 1)
```

- **Output File Format:** The final generated trajectory should be saved
  in a structured format, such as a CSV file, for easy analysis and
  visualization. Each row should represent a single time step.

- **Output Definition:** The output at each network forward pass is
  strictly the positions of the three bodies at a single normalized
  input time $t'$; velocities and accelerations are derived via AD.

**Example CSV Output Format:**

    time,x1,y1,z1,x2,y2,z2,x3,y3,z3
    0.00,-0.98,0.20,0.00,0.49,-0.10,0.00,0.49,-0.10,0.00
    0.01,-0.97,0.21,0.00,0.48,-0.11,0.00,0.49,-0.10,0.00
    ...

The section below is weirdly formatted and written out even in the original markdown file. However, it seems to render correctly render in the preview, so I'm not sure how to best approach this syntax fix here.

**Table 2: Consolidated Implementation Blueprint Summary**

| **Component** | **Definitive Specification** | **Justification** |
| --- | --- | --- |
| **Unit System** | A non-dimensional system is used where the gravitational constant $G=1$.<br>• **Characteristic Time:** $T=t_{max}$ (max time in dataset).<br>• **Characteristic Length:** $D=\sqrt[3]{GT^{2}}$. | Simplifies the governing physical equations and improves the numerical stability of the model during training. |
| **Backbone** | **SQR-SkipResNet** with **12 hidden layers** and a **width of 256 neurons**.<br>• **Odd Layers:** $\mathbf{x}^{(l)} = f_{\text{sr}}^{(l)}(\mathbf{x}^{(l-1)}) + (\mathrm{LayerNorm}(\mathbf{x}^{(l-1)}))^2$.<br>• **Even Layers:** Plain block, $\mathbf{x}^{(l)} = f_{\text{pn}}^{(l)}(\mathbf{x}^{(l-1)})$.<br>• **Layer Norm:** Applied to skip path on odd layers only, with `elementwise_affine=False` and `eps=1e-5`. | The deep architecture provides the expressive power needed for chaotic dynamics. The SQR-SkipResNet variant with LayerNorm provides superior gradient stability for non-smooth dynamics, which is ideal for modeling close encounters. |
| **Activation** | **SIREN ($\sin(x)$)** for all hidden layers. | The sine function is infinitely differentiable ($C^{\infty}$), which is a mathematical necessity for accurately computing the second-order derivatives ($\frac{d^{2}r}{dt^{2}}$) required in the physics loss term. |
| **Initialization** | A principled, two-part SIREN initialization scheme:<br>• **First Layer:** `first_omega_0 = 30`. Weights from $U[-\frac{1}{n_{in}}, \frac{1}{n_{in}}]$.<br>• **Hidden Layers:** `hidden_omega_0 = 1`. Weights from $U[-\frac{\sqrt{6/n_{in}}}{1}, \frac{\sqrt{6/n_{in}}}{1}]$. | A high initial frequency (`first_omega_0`) helps overcome spectral bias. The specific scaling for hidden layers ensures a stable distribution of activations, making the deep network trainable. |
| **Input Vector** | A **14-dimensional vector** built from the bounded network time coordinate and the ordered Jacobi-state initial-condition vector; see Section 5.2 "Network Input Contract" for the canonical formula and back-reference to `ctl_instruction.md` Step 4. | This formulation provides a physically-grounded and injective (unambiguous) representation of the initial state, which is critical for a conditional network to learn correctly. |
| **Output** | A **9-dimensional position vector** `[r1(u), r2(u), r3(u)]` with a linear (no activation) final layer. Velocities ($v'=\frac{dr'}{du}$) and accelerations ($a'=\frac{d^{2}r'}{du^{2}}$) are derived via componentwise **Automatic Differentiation (AD)** from the projected positions. | Predicting only positions simplifies the network architecture. Deriving kinematics via AD hard-codes their fundamental physical relationship, ensuring they are satisfied by construction to machine precision. |
| **Data Loss ($L_{data}$)** | **Huber loss** on scaled projected positions with default $\delta_r=1$. | Huber is the default data contract because it is smoother than pure L1 and less brittle than L2 for chaotic trajectory samples. |
| **IC Loss ($L_{IC}$)** | **IC anchor** on predicted position and AD-derived velocity at `u=0`, with $\beta_v=1$ and $\lambda_{IC}=1$ default. | Anchors the learned trajectory to the Phase 18 preprocessed initial state before later collocation points are optimized. |
| **Physics Loss ($L_{phys}$)** | **Causal-weighted residual** using the matched Plummer force denominator $r_{safe,ij}=\sqrt{\|\|r_j'-r_i'\|\|^2+\epsilon_{train}^2}$ with $\epsilon_{train}=10^{-5}$. | This loss enforces the governing ordinary differential equations across the entire solution domain, not just at data points, allowing the model to generalize and make physically consistent predictions. |
| **Total Loss ($L_{total}$)** | $L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$. | Combines data fidelity, IC anchoring, causal physics residual, energy drift, and angular-momentum drift terms in the default penalty-term formulation. |
| **Energy Loss ($L_{E}$)** | **Huber Loss ($\delta=1.0$)** on relative drift of the analytic matched-Plummer Hamiltonian $H_\epsilon$ (`H_ε`) using `epsilon_H = 1e-4 * S_H`. | soft conservation regularizer; the network predicts positions and does not parameterize a Hamiltonian. |
| **Angular Momentum Loss ($L_L$)** | **Componentwise Huber loss** on relative angular-momentum drift with $L_{scale}=\|\|L_0'\|\|+\epsilon_L$ and $\epsilon_L=10^{-8}$. | Enforces angular-momentum conservation as a soft penalty distinct from physics softening and from the energy denominator floor. |
| **Optional ALM P2 Ablation** | Optional P2 ablation for scalar conservation constraints only; never part of the default loss and never applied to the dense ODE residual. | Documents future experimentation boundaries without changing the baseline training contract. |

## References

[1] Power-enhanced ResNet for Function Approximation.pdf
[2] PIG: PHYSICS-INFORMED GAUSSIANS AS ADAPTIVE PARAMETRIC MESH REPRESENTATIONS - OpenReview, accessed June 25, 2025, <https://openreview.net/pdf/ba580795154cc26f5abe3ab4feab161a5246c2f3.pdf>
[3] PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://www.researchgate.net/publication/386575809_PIG_Physics-Informed_Gaussians_as_Adaptive_Parametric_Mesh_Representations>
[4] PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://openreview.net/forum?id=y5B0ca4mit>
[5] Implicit Neural Representations with Periodic Activation Functions, accessed June 25, 2025, <http://arxiv.org/pdf/2006.09661>
[6] Implicit Neural Representations with Periodic Activation Functions - NIPS, accessed June 25, 2025, <https://proceedings.neurips.cc/paper/2020/file/53c04118df112c13a8c34b38343b9c10-Paper.pdf>
[7] jaeminoh/Siren PINNs: Solving various PDEs by employing Siren, with JAX implementation., accessed June 25, 2025, <https://github.com/jaeminoh/Siren_PINNs>
[8] Implicit Neural Representations with Periodic Activation Functions - Vincent Sitzmann, accessed June 25, 2025, <https://www.vincentsitzmann.com/siren/>
[9] Implicit Neural Representations with Periodic Activation Functions | NeurIPS 2020, accessed June 25, 2025, <https://www.computationalimaging.org/publications/siren/>
[10] Gentle Introduction to SIREN - Nail Ibrahimli - TU Delft 3D Geoinformation, accessed June 25, 2025, <https://3d.bk.tudelft.nl/nail/siren/>
[11] Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - arXiv, accessed June 25, 2025, <https://arxiv.org/html/2310.15690v2>
[12] Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/382109760_Power-Enhanced_Residual_Network_for_Function_Approximation_and_Physics-Informed_Inverse_Problems>
[13] Physics-Informed with Power-Enhanced Residual Network for Interpolation and Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/374946733_Physics-Informed_with_Power-Enhanced_Residual_Network_for_Interpolation_and_Inverse_Problems>
[14] Software | PNNL, accessed June 25, 2025, <https://www.pnnl.gov/projects/philms/software>
[15] lululxvi/deepxde: A library for scientific machine learning and physics-informed learning - GitHub, accessed June 25, 2025, <https://github.com/lululxvi/deepxde>
[16] DeepXDE: A Deep Learning Library for Solving Differential Equations | SIAM Review - myqcloud.com, accessed June 25, 2025, <https://pdf-1307664364.cos.ap-chengdu.myqcloud.com/%E8%AE%BA%E6%96%87%E5%8F%82%E8%80%83/PINN/DeepXDE-%20A%20Deep%20Learning%20Library%20for%20Solving%20Differential%20Equations.pdf>
[17] omniscientoctopus/Physics-Informed-Neural-Networks: Investigating PINNs - GitHub, accessed June 25, 2025, <https://github.com/omniscientoctopus/Physics-Informed-Neural-Networks>

# 10. Numerical Acceptance Checks

### 10.1 Scaling Consistency
- **Pass Criterion**: Output variables computed via the length scaling $D = (G T^2)^{1/3}$ must match physical dimensions with `relative_error < 1e-10`.
- **Input Data**: Preprocessed network inputs.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_scaling.py`

### 10.2 COM Invariance
- **Pass Criterion**: Mass-weighted position projection head yields a net center of mass of exactly 0 (`abs(COM) < 1e-10`).
- **Input Data**: Forward pass position output tensor.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_com.py`

### 10.3 Componentwise AD on Synthetic Trajectory
- **Pass Criterion**: Network Jacobian matches analytical derivatives $r'(u)$ for the synthetic trajectory $r(u) = [\sin(2\pi u), \cos(2\pi u), u^2]$ with `relative_error < 1e-6`.
- **Input Data**: Synthetic 1D domain input $u \in [0, 1]$.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py`

### 10.4 Force-Energy Consistency
- **Pass Criterion**: The analytic matched-Plummer Hamiltonian is finite, and its negative position gradient yields accelerations matching the physical force residual with the same training-time Plummer softening. `relative_error < 1e-5`.
- **Input Data**: Network trajectory output.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_force_energy.py`

### 10.5 Loss Stability Dry Run
- **Pass Criterion**: Forward pass and loss computation (physics + IC + energy + angular momentum) yield finite scalars (no NaN/Inf).
- **Input Data**: Random uniform input tensors matching network architecture dimensions.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_loss_stability.py`

---

## Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the faithful converted body and are excluded from fidelity comparison per D-19.

### SI-PINN-002: Author comments preserved in converted body

- **Section:** Sections 2, 3 (sqr_skipresnet_siren_backbone, physics_constrained_loss)
- **Description:** 3 author comments from the LaTeX source (`\authcomment{}`) are preserved in the converted body as bold bracketed text (`**[...]**`). These are editorial notes from the original authors, not content discrepancies:
  1. "Need more detail on this dynamic scheduling for omega_0" (Section 2)
  2. "Need confirmation on this hidden layer's detail" (Section 2)
  3. "Comment: This above batch construction is not consistent with the CTL instruction plan" (Section 3)
- **Status:** Documented for future reconciliation — author should resolve these notes before training implementation

### SI-PINN-003: Batch construction inconsistency with CTL instruction plan

- **Section:** Section 3 (physics_constrained_loss) — Data Batch Construction code block
- **Description:** The author comment "This above batch construction is not consistent with the CTL instruction plan" flags a methodological inconsistency between the data sampling strategy described here and the CTL curriculum training plan. This should be investigated and resolved during training implementation.
- **Status:** Documented for future reconciliation

---

*End of faithful converted body. Source Issues section above is metadata excluded from fidelity comparison (D-19).*

===== END FILE pinn_architecture.md =====

===== BEGIN FILE sampling_method.md =====
# A Unified Pipeline for Generating High-Fidelity Three-Body Initial Conditions

*Methodology Description — June 15, 2025*

## Overview of the Data Generation Pipeline
**[Critical Update: The script preserves virial ratio in hierarchical ICs (masses normalized consistently with velocities). For quasi-random, sampling-time size scaling is **enabled** in the main block with range `[s_lo, s_hi] = [0.8, 1.2]`, which distorts the virial ratio by $s^3$ — see "Sampling-Time Size Variability" below. The default would preserve it, but scaling is explicitly enabled for variety. The Sobol coordinate allocation convention (locked in v1.4 Phase 20.5, matching `simulation_data/Scripts/ic_generation/ic_generation_utils.py`) places this scale factor at coordinate $u_4$ ahead of velocity coordinates $u_5$–$u_7$ in the standard configuration.]**

Generating high-quality training data for a Physics-Informed Neural Network (PINN) tasked with solving the three-body problem is a non-trivial challenge. The chaotic nature of many three-body systems means that a significant fraction of randomly generated initial conditions (ICs) will lead to computationally expensive simulations that are ultimately unusable due to poor energy conservation.

To address this, we adopt a multi-stage pipeline designed to progressively filter and refine the set of initial conditions, ensuring that only the most promising candidates are passed to the high-precision integrator, Brutus. This pipeline consists of three main stages:

1.  **Stage 1: Hierarchical & Quasi-Random Sampling.** We begin by generating a diverse set of initial conditions: an algorithm to generate hierarchical three-body systems; and another one using a quasi-random sampling method which adopts a Sobol sequence to ensure uniform coverage of the parameter space. This stage includes several enhancements to the baseline sampling method.

2.  **Stage 2: Pre-screening for Short-Term Stability.** Before committing to a full Brutus simulation, we use a rapid, low-precision Leapfrog integrator to quickly assess the short-term stability of each IC. This step efficiently weeds out configurations that are guaranteed to become unstable.

3.  **Stage 3: Adaptive Brutus Parameterization.** For the ICs that pass the pre-screening, we analyze their intrinsic properties (e.g., timescales, minimum separation) to assign them to different "regimes". Each regime is then simulated with a tailored set of Brutus parameters to balance computational cost with the required accuracy.

This document details the first two stages of this pipeline.

## Stage 1: Hierarchical Initial Conditions Generation
The hierarchical initial conditions (ICs) are generated using the `generate_stable_hierarchical_systems` algorithm implemented in the accompanying Python script. The procedure is:

1.  **Mass sampling:** Draw the inner mass ratio $q_{\rm inner}\sim U(0.1,1.0)$ and outer mass ratio $q_{\rm outer}\sim U(0.1,2.0)$. Sample a base mass $m_1\sim U(m_{\min},m_{\max})$ (default $m_{\min}=0.5$, $m_{\max}=1.5$). Set $m_2=q_{\rm inner}m_1$, $m_3=q_{\rm outer}(m_1+m_2)$, then normalize $(m_1,m_2,m_3)$ so that $m_1+m_2+m_3=3$.

2.  **Hierarchical separation ratio:** Compute the Kozai--Lidov stability threshold

$$\mathrm{min\_ratio} = 2.8\bigl(\tfrac{1+q_{\rm outer}}{1+e_{\rm outer}}\bigr)^{2/5}\quad(\text{with }e_{\rm outer}\le0.5),$$

then draw the hierarchy ratio $\mathcal{R}\sim U(\max(3,\mathrm{min\_ratio}),10)$.

3.  **Orbital elements:** Sample inner semi-major axis $a_{\rm inner}\sim U(0.1,0.3)$, set $a_{\rm outer}=\mathcal{R}\,a_{\rm inner}$. Sample eccentricities $e_{\rm inner},e_{\rm outer}\sim U(0,0.3)$ and mean anomalies $M_{\rm inner},M_{\rm outer}\sim U(0,2\pi)$.

4.  **Radial distances and speeds:** Compute

$$r_{\rm inner}=a_{\rm inner}\bigl(1-e_{\rm inner}\cos M_{\rm inner}\bigr),\quad
          v_{\rm inner}=\sqrt{\tfrac{m_1+m_2}{r_{\rm inner}}},$$

$$r_{\rm outer}=a_{\rm outer}\bigl(1-e_{\rm outer}\cos M_{\rm outer}\bigr),\quad
          v_{\rm outer}=\sqrt{\tfrac{m_1+m_2+m_3}{r_{\rm outer}}}.$$

5.  **Inclination perturbation:** Draw a small inclination $\iota\sim U(0,0.1)$ for the inner binary.

6.  **Position vectors:**

$$
\begin{aligned}
          \mathbf{x}_1 &= -\frac{m_2}{m_1+m_2}\,r_{\rm inner}\bigl(\cos\iota\,\hat{\mathbf{x}}+\sin\iota\,\hat{\mathbf{z}}\bigr),\\
          \mathbf{x}_2 &= +\frac{m_1}{m_1+m_2}\,r_{\rm inner}\bigl(\cos\iota\,\hat{\mathbf{x}}+\sin\iota\,\hat{\mathbf{z}}\bigr),\\
          \mathbf{x}_{\rm COM} &= -\frac{m_3}{m_1+m_2+m_3}\,r_{\rm outer}\,\hat{\mathbf{x}},\\
          \mathbf{x}_3 &= +\frac{m_1+m_2}{m_1+m_2+m_3}\,r_{\rm outer}\,\hat{\mathbf{x}}.
\end{aligned}
$$

Shift $\mathbf{x}_1,\mathbf{x}_2$ by $\mathbf{x}_{\rm COM}$.

7.  **Velocity vectors:**

$$
\begin{aligned}
          \mathbf{v}_1 &= \bigl(0,\,-\tfrac{m_2}{m_1+m_2}v_{\rm inner},\,0\bigr),\quad
          \mathbf{v}_2 = \bigl(0,\,\tfrac{m_1}{m_1+m_2}v_{\rm inner},\,0\bigr),\\
          \mathbf{v}_{\rm COM} &= \bigl(0,\,-\tfrac{m_3}{m_1+m_2+m_3}v_{\rm outer},\,0\bigr),\quad
          \mathbf{v}_3 = \bigl(0,\,\tfrac{m_1+m_2}{m_1+m_2+m_3}v_{\rm outer},\,0\bigr).
\end{aligned}
$$

Add $\mathbf{v}_{\rm COM}$ to each of $\mathbf{v}_1,\mathbf{v}_2$.

8.  **Gaussian perturbation:** Add a small random perturbation drawn from $\mathcal{N}(0,\,0.01)$ to each component of $\mathbf{x}_i$ and $\mathbf{v}_i$.

**FRAME-03 frame note:** Hierarchical generation enforces center of
mass and zero total momentum before this perturbation step. The later
Gaussian perturbation `N(0, 0.01)` is applied to all position and
velocity vectors, so the stored ICs can move out of the exact COM/P
frame. In a 500-file sample, observed offsets are `|COM|` median
approximately `9e-3` (95th approximately `1.8e-2`) and `|P|` median
approximately `3e-2` (95th approximately `5.5e-2`). The Phase 18
FRAME-01 unified preprocessing pipeline deterministically recenters and
reboosts these trajectories before training use.

This procedure mirrors exactly the logic and parameter choices in `FINAL_ic_generator_enhanced.py`.

## Stage 2: Enhanced Quasi-Random Sampling
The foundation of our pipeline is a hybrid quasi-random sampling method designed to generate a diverse set of initial conditions for a planar, equal-mass three-body system.

## 1. Core Sampling Methodology

The fundamental idea is to fix one particle and sample the second from a well-defined space using a low-discrepancy sequence.

- **Fix Particle 1:** Particle 1 is fixed at $p_1 = (1, 0, 0)$ on the unit sphere.

- **Sample Particle 2:** Particle 2, $p_2$, is sampled quasi-uniformly from the 3-D hemisphere defined by $\{x \le 0, x^2 + y^2 + z^2 \le 1\}$.

- **Set Particle 3:** Particle 3 is set as $p_3 = -(p_1 + p_2)$ to maintain the system's center of mass at the origin for the equal-mass case.

### 1.1 Low-Discrepancy Engine: Sobol Sequence

We use a Sobol sequence, a type of low-discrepancy sequence, to ensure that every finite batch of samples covers the parameter space evenly, minimizing both "clumping" and "voids".

- **Dimension:** The Sobol engine dimension is determined by which sampling features are enabled. Let $\delta_s = 1$ if sampling-time scaling is enabled (`scale_range[0]` $\neq$ `scale_range[1]`) and $0$ otherwise; let $\delta_v = 1$ if velocity sampling is enabled (`velocity_scale > 0`) and $0$ otherwise. The Sobol dimension is then $d = 3 + \delta_s + 3\delta_v$. This formula assumes `rotate=False` (the standard configuration): `ic_generation_utils.py` also exposes an optional `rotate` flag that would add 3 dimensions, but it is disabled by default and is a non-functional placeholder for a future rotation feature, not exercised by the existing dataset. See "Sobol Coordinate Allocation Convention" below for the layout. For the standard quasi-random configuration in `generate_ics.py` (`scale_range=(0.8, 1.2)`, `velocity_scale=0.1`), $\delta_s = \delta_v = 1$ and $d = 7$.

- **Scrambling:** Scrambling is enabled (e.g., `qmc.Sobol(scramble=True)`). This feature preserves the determinism and uniformity of the sequence while breaking up any residual lattice artifacts that could introduce bias.

### 1.2 Mapping Sobol Numbers to Physical Coordinates

The quasi-random numbers $(u_1, u_2, \dots) \in (0, 1)^d$ generated by the Sobol engine must be mapped to the desired physical coordinates.

#### Sobol Coordinate Allocation Convention

The Sobol coordinates $u_i$ use 1-based mathematical indexing throughout this document. Array indexing in implementation should be shifted accordingly.

The allocation order is **fixed**: position, then (optionally) scale, then (optionally) velocity. The dimension count $d = 3 + \delta_s + 3\delta_v$ (for `rotate=False`; see the §1.1 Dimension bullet) is conditional, but the order in which enabled features consume coordinates is invariant.

| Coordinate | Physical role | Drawn when |
|---|---|---|
| $u_1, u_2, u_3$ | Position of the free particle ($\theta, \phi, r$) | Always |
| $u_4$ | Sampling-time size scale factor $s$ | $\delta_s = 1$ only |
| $u_{4+\delta_s}, u_{5+\delta_s}, u_{6+\delta_s}$ | Velocity components of the free particle | $\delta_v = 1$ only |

For the standard configuration ($\delta_s = \delta_v = 1$): $u_1$–$u_3$ position, $u_4$ scale, $u_5$–$u_7$ velocity. When $\delta_s = 0$, no scale coordinate is drawn and velocity coordinates take indices $u_4$–$u_6$.

This convention prevents any Sobol coordinate from being reused for two independent physical quantities, and matches the implementation in `simulation_data/Scripts/ic_generation/ic_generation_utils.py` that generated the existing standard quasi-random dataset.

**Disambiguation note.** The sampling-time scale factor $s$ defined here is distinct from the preprocessing-time global scaling (by constants $D$, $V$, $T$) currently described in `ctl_instruction.md` Step 2 ("Preprocessing: Scaling to Dimensionless Units") and locked in v1.4 by Phase 18 (FRAME-01, the preprocessing/scaling order) and Phase 19 (PHYS-01, the $D = (G T^2)^{1/3}$ convention) per resolution doc §4.5 and §10.1. They apply at different pipeline stages: this sampling-time $s$ is applied at IC generation; preprocessing scaling is applied after canonical rotation.

#### Direction on the Unit Sphere
1.  The polar angle $\theta$ is set using the transformation $\cos\theta = 1 - 2u_1$, which ensures a uniform distribution with respect to the solid angle.

2.  The azimuthal angle is set as $\phi = 2 \pi u_2$.

3.  To enforce the $x \le 0$ constraint, we mirror points that fall in the wrong hemisphere by replacing $\phi$ with $(\phi + \pi) \pmod{2\pi}$, which preserves uniformity without resorting to inefficient rejection sampling.

#### Radial Distance and Scaling
- The radial distance $r$ is calculated from $u_3$ using the cube root, $r = u_3^{1/3}$, to ensure the sample is uniform by volume.

#### Sampling-Time Size Variability
An optional sampling-time size scale factor $s$ can be applied to all positions and velocities for added variety in system size. The scale factor is sourced from the 4th Sobol coordinate (per the Sobol Coordinate Allocation Convention above) and maps to a user-defined range $[s_{\mathrm{lo}}, s_{\mathrm{hi}}]$ (default: $[1.0, 1.0]$, which disables it: $\delta_s = 0$) via

$$s = s_{\mathrm{lo}} + (s_{\mathrm{hi}} - s_{\mathrm{lo}})\,u_4.$$

For example, the script's main block enables it with $[s_{\mathrm{lo}}, s_{\mathrm{hi}}] = [0.8, 1.2]$ for quasi-random generation.

When enabled, positions and velocities both scale by $s$. **Impact on virial ratio:** this changes $Q = 2T / |U|$ by a factor of $s^3$ (kinetic energy scales as $s^2$, potential as $s^{-1}$). Disable if preserving virial equilibrium is required. When $\delta_s = 0$, no Sobol coordinate is consumed for scaling and velocity coordinates take indices $u_4$–$u_6$ instead of $u_5$–$u_7$.

**Distinct from preprocessing-time scaling.** This sampling-time $s$ is applied at IC generation, **before** the preprocessing pipeline. The preprocessing pipeline subsequently nondimensionalizes the state by constants $D, V, T$ (see the Disambiguation note above). Because the characteristic time $T = t_{\max}$ is a global constant, the sampled $s$ survives preprocessing as variety in the dimensionless IC, manifesting through the virial-ratio distortion that propagates into $E$ and other invariants.

**Symbol note.** The bounds are $s_{\mathrm{lo}}$ (low) and $s_{\mathrm{hi}}$ (high). They are deliberately written `s_lo`/`s_hi` rather than `s_min`/`s_max` to avoid collision with the minimum pairwise separation invariant (denoted `s_min` in the resolution doc's invariant set).

#### Velocity Sampling

Per the Sobol Coordinate Allocation Convention, the velocity coordinates $(u_{4+\delta_s}, u_{5+\delta_s}, u_{6+\delta_s})$ are mapped to a 3D velocity vector $\mathbf{v}$ using inverse transform sampling from a normal distribution with mean 0 and standard deviation $\sigma = \text{velocity\_scale}$ (default 0.1):

$$v_i = \Phi^{-1}(u_{3+\delta_s+i};\,\mu=0,\,\sigma=\text{velocity\_scale}),\quad i=1,2,3.$$

For the standard configuration with $\delta_s = 1$, the velocity coordinates are $(u_5, u_6, u_7)$; when $\delta_s = 0$, they are $(u_4, u_5, u_6)$.

The sampler then enforces total momentum conservation for the equal-mass case
by setting `v1 = -v2/2` and `v3 = -v2/2`, so
$\sum_i m_i \mathbf{v}_i = 0$.

**FRAME-03 frame note:** For standard quasi-random ICs, equal-mass
positions set `p3 = -(p1 + p2)`, so position COM is zero by
construction. Velocities use `v1 = -v2/2` and `v3 = -v2/2`, so total
momentum is zero by construction for equal masses. The universal
FRAME-01 preprocessing pipeline still applies to standard quasi-random
ICs for consistency and assertion checks.

## 2. Enhancements to the Sampling Algorithm

To improve the quality and diversity of the generated ICs, we introduce the following enhancements.

### 2.1 Sampling Non-Zero Initial Velocities

In this implementation, initial velocities for free particles are always sampled from a normal distribution using the inverse CDF and Sobol numbers. We can sample initial velocities using additional dimensions from the Sobol sequence.

- **Required Dimensions:** Sampling a 3D velocity vector for each of the two free particles would require 6 additional Sobol dimensions. However, we can sample velocities for just one particle and derive the others from physical constraints (e.g., total momentum).

- **Velocity Sampling Strategy:** A simple approach is to sample each velocity component from a normal distribution, where the Sobol coordinates are mapped to the normal distribution using the inverse transform sampling method (quantile function). The standard deviation of this distribution becomes a tunable hyperparameter.

### 2.2 Initial Collision Avoidance: The Role of $\epsilon$

The sampling script includes a safeguard to reject any sample where the pairwise distance between any two bodies falls below a prescribed threshold, $\epsilon$.

- **Purpose:** The primary role of $\epsilon$ at this stage is to provide a quick, computationally cheap check to avoid immediate singularities and clear-cut unstable configurations.

- **Setting $\epsilon$:** This value is set to be 0.05 in the implementation. This ensures that obviously problematic ICs are discarded immediately, saving the cost of even a fast Leapfrog integration.

**Recommended Scale**

If Stage 2 Leapfrog test flags approaches below 0.10, pick $\epsilon \approx 0.05$. Starting from 0.01 is not wrong, but it may leave many obviously-bad ICs for the next stage, increasing the pre-screening burden. Conversely, too large an $\epsilon$ biases the spatial distribution by carving out a forbidden core.

**Practical Strategy**

- Begin with $\epsilon \approx 0.05$

- Monitor the rejection ratio during Stage 1. If $<1\%$ of proposals are rejected, you can afford to tighten $\epsilon$ a bit; if $>30\%$ are rejected and most would also fail Stage 2 anyway, loosen it.

- Keep $\epsilon$ fixed once you are satisfied; later tuning has diminishing returns because Stage 2 already provides a dynamic safety net

## Stage 3: Pre-Screening of Generated ICs for Short-Term Stability
The ICs generated in Stage 1 are diverse but may still contain many that are dynamically unstable. Running these through the high-precision Brutus integrator is computationally wasteful. Therefore, Stage 2 acts as an essential intermediate filter.

## 3. The Pre-Screening Rationale

### Implementation Details
- **Integration parameters:** The Leapfrog integrator runs with a fixed step size `dt = 0.0001` over a total duration of `t_max = 1.0`.

- **Energy error threshold:** `ENERGY_ERROR_THRESHOLD = 0.01` (i.e., 1%).

- **Minimum separation threshold:** `MIN_DISTANCE_THRESHOLD = 0.01`.

- **Virial ratio bounds:** Defaults to `VIRIAL_RATIO_MIN = 0.001` and `VIRIAL_RATIO_MAX = 2.0`, with optional percentile-based adaptive thresholds when `USE_PERCENTILE_THRESHOLDS = True`.

- **Angular momentum filter:** Disabled by default (`MIN_ANGULAR_MOMENTUM = 0.0`); can be enabled or set adaptively via percentiles.

- **Dataset handling:** The script loops over both hierarchical and quasi-random sampling directories and skips already-processed IC files based on recorded hashes.

The pre-screening script uses a fast, low-precision N-body integrator (a JIT-compiled Leapfrog integrator) to simulate each IC for a short period (e.g., $t_{max}=1.0$). Its goal is not to produce an accurate trajectory but to quickly identify ICs that exhibit signs of instability, such as:

- Rapid energy non-conservation.

- Extremely close encounters between particles during the short simulation.

## 4. Pre-Screening Criteria

The pre-screening script evaluates each IC against several criteria to determine its stability. An IC must pass all these checks to be considered "stable" and move on to Stage 3.

1.  **Short-Term Energy Conservation:** The script calculates the relative energy error, $|(E_{current} - E_{init}) / E_{init}|$, during the Leapfrog integration. If this error exceeds a modest threshold (e.g., 1%), the IC is flagged as unstable.

2.  **Dynamic Minimum Separation:** The script tracks the minimum separation between any two bodies throughout the short integration. If this distance ever drops below a hardcoded threshold (e.g., 0.01), the IC is immediately rejected as it indicates a close encounter that Brutus would struggle with.

3.  **Virial Ratio:** The script filters for ICs with $Q = 2T/|U|$ within the default bounds $0.001 \le Q \le 2.0$, or uses percentile-based adaptive thresholds when enabled.

4.  **Angular Momentum:** Optionally filters for ICs with total angular momentum $|\sum_i m_i\,\mathbf r_i \times \mathbf v_i|$ above `MIN_ANGULAR_MOMENTUM` (default 0.0), or using adaptive percentile thresholds if enabled.

5.  **Adaptive Threshold Computation:** To enhance the robustness and adaptability of the pre-screening filters, adaptive thresholds for Virial Ratio and Angular Momentum are computed based on a representative subset of the dataset. The sample size for adaptive threshold calculation is dynamically set to ensure statistical robustness:

    $$sample\_size = \min(1000, \max(200, \lvert 0.05 \times total\_files \rvert))$$

    Thresholds are determined using percentile-based computations from these samples:

    - Virial Ratio thresholds: between the `VIRIAL_PERCENTILE_MIN` and `VIRIAL_PERCENTILE_MAX` percentiles.

    - Minimum Angular Momentum threshold: `ANGULAR_PERCENTILE_MIN` percentile (optional).

## 5. A Coordinated Strategy for Minimum Distance

It is crucial to understand the distinct but complementary roles of the minimum distance parameters across the pipeline:

`epsilon` (in Stage 1 - Sampling):

:   This is a **static, initial filter**. It is applied once to the $t=0$ configuration. Its purpose is to perform a cheap rejection of ICs that are "born" in a near-collision state.

`min_distance_threshold` (in Stage 2 - Pre-screening):

:   This is a **dynamic, short-term filter**. It checks for close encounters that occur during the brief Leapfrog integration. An IC might have a perfectly acceptable initial separation but be on an immediate collision course, which this check will catch. It is a more robust filter than the static `epsilon`.

`min_sep` (in Stage 3 - Adaptive Brutus):

:   This is not a filter, but a **diagnostic metric**. For the ICs that have passed the first two stages, this value (calculated from the initial state) is used to categorize the system into a specific regime (e.g., "standard," "hierarchical," "close_low_L"). This categorization then determines the precise (and often very stringent) Brutus parameters that will be used for the final, high-fidelity simulation.

By using these three parameters in a coordinated fashion, we create an efficient and intelligent pipeline that maximizes the quality of the final dataset while minimizing wasted computational resources.

## 6. Execution and Final Quality Control

The provided scripts facilitate the automation of this entire stage, creating a master script to run all generated simulations in parallel. After the simulations are complete, a final quality control check is essential. This involves parsing the Brutus output to:

1.  **Verify Energy Conservation:** Confirm that the relative energy error $|\Delta E/E|$ remains below the target threshold (e.g., $10^{-4}$) for the entire duration of the simulation.

2.  **Check Momentum Conservation:** Ensure the total momentum of the system remained close to zero.

3.  **Confirm Completion:** Check that the simulation ran to the specified $t_{\mathrm{end}}$ without premature termination.

Only the data from simulations that pass this final, rigorous quality control check should be considered "gold standard" data, suitable for training a high-fidelity PINN.


---

## Source Issues / Notes for Future Reconciliation

No source-level issues identified during Phase 15 audit. The converted body faithfully reproduces all 10 sections of the monolithic `sampling_method_instruction.tex` source without suspected inconsistencies. All 10 section audits show `**Status:** PASS`.

===== END FILE sampling_method.md =====
