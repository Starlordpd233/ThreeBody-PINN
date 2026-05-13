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
- [Canonical: Dataset Documentation](../../../../simulation_data/Documentation/README.md) — Authoritative dataset spec, anomalies, dt_out per variant, completeness rules. Do NOT duplicate content from here.
- [Canonical: data-processing-pipeline-full.py](../../../../pinn/data-processing-pipeline-full.py) — Current IC vector assembly and staging logic.
- [Canonical: calculate_metrics.py](../../../../simulation_data/Scripts/metrics_calculation/calculate_metrics.py) — Conservation metrics extraction.

---

*End of 02-data-pipeline-and-validation.md*

*This document synthesized from 7 source files archived in `archive/`. See `MIGRATION.md` for per-section provenance.*
