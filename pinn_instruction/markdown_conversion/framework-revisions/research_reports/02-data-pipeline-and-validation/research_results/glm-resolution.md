# Resolution Document — Issue 02: Data Pipeline and Validation

**Date:** 2026-06-10  
**Author:** Independent Senior Research Analyst  
**Package inventory (10 files received):** `README.md`, `framed-research-questions.md`, `claims-table.md`, `consolidated-context.md`, `ERRATUM-2026-06-10.md`, `specs/02-data-pipeline-and-validation.md`, `specs/ctl_instruction.md`, `specs/pinn_architecture.md`, `specs/sampling_method.md`, `specs/data_quality_assessment.md`

---

## §0 Scope and Decision Standard

### Scope

This document resolves every question posed in `framed-research-questions.md` (Q-A1 through Q-A6, Q-B1 through Q-B4, Q-C1 through Q-C4). The questions cover three clusters:

- **Cluster A** — Ingestion & Selection (Stage 4→5 validation gate, non-contiguous IDs, blacklist consumption, missing-gold fallback, footer heterogeneity, storage format)
- **Cluster B** — Sampling, Precision & Global Scale (points-per-trajectory, mass-drift protocol, float64 sufficiency, D convention)
- **Cluster C** — Validation Metrics (SCS, SASD, IPR, PSC data-side definitions)

### Exclusions (per Doc-03 Scope Boundary)

The following are **not answered** and are noted as deferred forward-references only:

- **M16** — `dt_out` collocation-density scaling (deferred to doc-03, SCOPE-11)
- **G6** — Causal-training Option A vs Option B (deferred to doc-03)
- **Training-loop usage** of SCS/SASD/IPR/PSC — SASD-weighted collocation sampling, IPR-as-ALM-noise-floor, PSC-governed curriculum replay (deferred to doc-03)

### Decision Standard

Each recommendation is evaluated against:

1. The six locked Hard Constraints (14D input contract, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 dual-epsilon, post-v1.3 SCS gate, PHYS-01 D convention)
2. Verified dataset facts from `claims-table.md` (distinguishing `verified` from `claimed-unverified`)
3. First-principles reasoning from computational physics and data-engineering practice
4. The ERRATUM-2026-06-10 corrections, which revise the file-naming narrative and recharacterize "partial"/"minimal" footer populations

No recommendation relies on a `claimed-unverified` figure without explicit conditional flagging. Where evidence is insufficient, I say so and specify what would resolve the question.

---

## §1 Executive Decision Summary

1. **Q-A1:** A completeness gate IS required between Stage 4 and Stage 5. It should enforce `final_timestep >= 9.5` (the grounded rule) and a snapshot-count floor of `n_snapshots >= 2` (minimal viability), not the issue doc's `>= 200` for Stage 4+. The `>= 200` threshold is unjustified for standard trajectories with ~59 snapshots (CLM-10) and would reject the entire standard dataset.

2. **Q-A2:** The ID→trajectory mapping must use an `id_to_path` dictionary built from filesystem scan at DataLoader init. Linear indexing is prohibited. The actual gap magnitudes (CLM-01: 31.2% standard; CLM-02: 2.9% hierarchical) make the contract essential for standard data and desirable for hierarchical.

3. **Q-A3:** The blacklist must be loaded at DataLoader init and blacklisted IDs excluded. Exclusions must be logged (count + per-ID logging at DEBUG level). The 65-ID count (CLM-03) is directly observable; the consumption-status finding is the core issue.

4. **Q-A4:** **Insufficient evidence to assert a fallback.** Neither the package nor the dataset facts determine whether skipping to Stage 6 or admitting a flagged low-fidelity sample is correct. This is a **Phase-26 STOP-gap candidate**. I provide the conditional analysis: if training stability requires gold-fidelity verification, option 1 (skip to Stage 6) is safer; if data completeness is paramount, option 2 (flagged low-fidelity) preserves the 184 IDs.

5. **Q-A5:** Footer handling must use folder-default parameters (CLM-09) when a file has no `Result:` footer (ERRATUM Correction 2: 1,550 hierarchical + 701 standard + 219 standard-gold files have no footer at all). Tolerance provenance must be represented as an enum: `DIRECT` (footer has `tol`) or `INFERRED_FOLDER_DEFAULT` (no footer or no `tol` in footer).

6. **Q-A6:** HDF5 is the primary format for training-data storage, with `.npy` as an acceptable alternative per the existing spec. An optional JSON export for inspection only is endorsed. This is a storage decision with zero methodology consequence.

7. **Q-B1:** A fixed 32 points per trajectory is infeasible for standard data. The correct contract is an adaptive cap: `n_pts = min(n_pts_max, int(floor_fraction * n_snapshots))` with `floor_fraction = 0.5` and `n_pts_max = 32`. For standard (~59 snapshots) this yields ~29 points; for hierarchical (~125) yields 32; for gold (~1000) yields 32.

8. **Q-B2:** The pipeline must verify mass consistency between IC and Brutus `t=0` using `np.allclose(m_IC, m_Brutus_t0, rtol=1e-15)` on a sample of at least 1,000 pairs. If the failure rate exceeds 1%, switch to `decimal.Decimal` for mass parsing. If the failure rate is zero, document IC masses as canonical.

9. **Q-B3:** `float64` is sufficient for all validation metrics given the Brutus convergence tolerances (CLM-09: 1e-13 to 1e-15). `float64` relative precision (~1e-16) provides 1–3 guard digits. `decimal.Decimal` is required only for the mass-consistency verification step (Q-B2), not for runtime metric computation.

10. **Q-B4:** The data pipeline must use the locked raw-mass convention `D = (G·T²)^(1/3) ≈ 4.6416`. Adopting the issue doc's `D = 6.694` would violate Hard Constraint 6 and require rewriting every residual, Hamiltonian, COM, and invariant formula. The reconciliation is: the issue doc's formula is correct under a mass-fraction convention (`m_i' = m_i / M_tot`), but the project has locked the raw-mass convention.

11. **Q-C1:** The correct SCS definition is the locked log-drift convention: `ε_H = max_t |(H(t) − H(0))/H(0)|`, `SCS = log₁₀(ε_H)`, reject gate `SCS > −5`. The issue doc's ratio thresholds (`1e-6` / `1e-8`) are raw-drift numbers, not log-drift scores. The `1e-6` ratio threshold corresponds to `SCS = −6`, which is *stricter* than the locked gate (`SCS > −5`). The `1e-8` threshold corresponds to `SCS = −8`, stricter still. These cannot be reconciled without overriding the locked gate; the locked gate governs.

12. **Q-C2:** SASD data-side definition: `SASD_i = Δt_i · ‖a(t_i)‖ / ‖v(t_i)‖`, computed in scaled units using the static validation epsilon `ε = 1e-10` for force computation. Flag criterion: `max(SASD) > 0.5` (the trajectory turns significantly between samples). A robust variant using acceleration curvature is noted.

13. **Q-C3:** IPR data-side definition uses cubic Hermite spline interpolation of the Brutus snapshot data, evaluated at synthetic collocation points between snapshots. The gravitational force in the IPR residual uses the **static validation epsilon** `ε = 1e-10` (per Hard Constraint 4: validation metrics run with static `ε = 1e-10`). The issue doc's use of `ε = 1e-5` for IPR contradicts the locked dual-epsilon split.

14. **Q-C4:** PSC data-side definition: Shannon entropy of data-point counts across a discretized phase-space grid. Grid construction: partition the 6D phase space `(r₁₂, r₂₃, r₃₁, v₁₂, v₂₃, v₃₁)` into equal-volume bins; `H_data = −Σ_k p_k log(p_k)` where `p_k` is the fraction of trajectory-time-points in bin `k`. Use K optimization via maximum-likelihood or rule-of-thumb bin count.

---

## §2 Decision Matrix

| Question ID | One-Line Verdict | Confidence |
|---|---|---|
| Q-A1 | Completeness gate required; enforce `final_timestep >= 9.5` + `n_snapshots >= 2`; reject `>= 200` threshold | High |
| Q-A2 | `id_to_path` dictionary from filesystem scan; no linear indexing | High |
| Q-A3 | Blacklist loaded at DataLoader init; exclusions logged; fail-loud on blacklisted ID in batch | High |
| Q-A4 | STOP-gap — insufficient evidence to choose fallback | Medium |
| Q-A5 | Folder-default fallback (CLM-09); provenance enum DIRECT/INFERRED_FOLDER_DEFAULT | High |
| Q-A6 | HDF5 primary; `.npy` acceptable; optional JSON inspection export; zero methodology impact | High |
| Q-B1 | Adaptive cap `n_pts = min(32, int(0.5 * n_snapshots))` | High |
| Q-B2 | `np.allclose(rtol=1e-15)` on ≥1000 pairs; if failure >1%, use `decimal.Decimal` | Medium |
| Q-B3 | `float64` sufficient for all metrics; `Decimal` only for mass-consistency check | High |
| Q-B4 | Use locked `D ≈ 4.6416`; `D = 6.694` requires convention rewrite violating Hard Constraint 6 | High |
| Q-C1 | Locked log-drift gate `SCS > −5` governs; ratio thresholds are different quantities | High |
| Q-C2 | `SASD_i = Δt_i · ‖a‖/‖v‖` in scaled units; flag at `max(SASD) > 0.5`; static `ε = 1e-10` | Medium |
| Q-C3 | Cubic Hermite IPR with static validation `ε = 1e-10`; issue doc's `ε = 1e-5` contradicts locked split | High |
| Q-C4 | Shannon entropy on discretized phase-space grid; 6D pairwise-distance/velocity binning | Medium |

---

## §3 Resolutions — Cluster A: Ingestion & Selection

### Q-A1 (B-06) — Stage 4 → Stage 5 Validation Gate

**Verdict / Recommendation:**

A completeness/validity gate must sit between Stage 4 (metrics) and Stage 5 (training). The gate should enforce:

1. **`final_timestep >= 9.5`** — This is the grounded completeness rule from README Completeness Checks (consolidated-context.md, Completeness Checks section; CLM-11: rule grounded, prevalence claimed-unverified).
2. **`n_snapshots >= 2`** — A trajectory must have at least two snapshots to define a temporal interval. This is the minimum viability condition for any time-series training sample.
3. **NOT `snapshot_count >= 200` for Stage 4+** — The issue doc's proposed `>= 200` threshold would reject all standard trajectories (~59 snapshots per CLM-10) and all hierarchical trajectories (~125 per CLM-10). Only gold trajectories (~1000) would pass. This would eliminate the majority of the dataset from training, which is clearly not the intent.
4. **Blacklist exclusion** (addressed separately in Q-A3 but also enforced at this gate).

The gate must be enforced at DataLoader initialization, not at batch-construction time. Rejected trajectories must be logged with rejection reason.

**Reasoning:**

The issue doc correctly identifies the gap: `calculate_metrics.py` processes all files including partial/errored runs (consolidated-context.md, calculate_metrics.py provenance excerpt), and no downstream check exists. However, the proposed `snapshot_count >= 200` threshold is misaligned with the actual data distribution. The README itself warns against hard-coding snapshot counts (consolidated-context.md, Snapshot count warning: "Avoid hard-coding exact expected snapshot counts"). A snapshot count of 200 is only achievable at gold resolution (`dt_out = 0.01`), not at standard (`dt_out = 0.17`) or hierarchical (`dt_out = 0.08`) resolution. The `final_timestep >= 9.5` rule is the primary completeness signal and must be re-validated at DataLoader init since it is currently checked only at Stage 3.

**Evidence:**

- `consolidated-context.md` — Completeness Checks: `final_timestep >= 9.5` is the primary check; README warns against hard-coding snapshot counts.
- `claims-table.md` CLM-10 — Snapshot counts ~59 / ~125 / ~1000 (claimed-unverified; README warns against hard-coding).
- `claims-table.md` CLM-11 — `final_timestep >= 9.5` rule grounded; prevalence claimed-unverified.
- `02-data-pipeline-and-validation.md` lines 57, 283, 326–331 — Issue doc proposes `>= 200` (non-authoritative).

**Confidence:** High  
**Key factor that would change answer:** Empirical verification that a significant fraction of standard/hierarchical trajectories fail `final_timestep >= 9.5` (CLM-11 prevalence is unverified).

**Verification suggestion:** Run `final_timestep` check on all Brutus output files and report the pass/fail count per variant. Count trajectories with `n_snapshots < 2` across all variants.

**Proposed specification text for `ctl_instruction.md`:**

Insert after the DataLoader Requirements section (or as a new subsection in Step 1):

> **DataLoader Completeness Gate (PIPE-01).** At DataLoader initialization, every trajectory must satisfy:
> 1. `final_timestep >= 9.5` (grounded in README Completeness Checks);
> 2. `n_snapshots >= 2` (minimum temporal viability);
> 3. Not blacklisted (see Blacklist Consumption contract).
> Trajectories failing any check are excluded from the index and logged with the failure reason. No `snapshot_count` floor above 2 is imposed at the data-loading stage; sampling-ratio limits are handled at batch-construction time (see Q-B1).

---

### Q-A2 (B-11) — Non-contiguous IDs (ID ≠ Array Index)

**Verdict / Recommendation:**

The correct ID→trajectory mapping contract requires:

1. At DataLoader initialization, scan all Brutus output folders and build an `id_to_path` dictionary mapping each numeric ID (extracted from the filename) to its full filesystem path.
2. A `TrajectoryIndex` class exposing `get_by_id(file_id)` that returns the path and metadata.
3. **No code path may assume `ID == array_index` or use dense linear indexing.** All curriculum and stage-assignment logic must use the `TrajectoryIndex` for ID resolution.
4. The gold/non-gold variant is determined by the **folder path** (per ERRATUM Correction 1: gold Brutus output filenames do NOT carry a `_gold_` infix; gold status is encoded only in the folder name). The numeric ID is shared across base and gold folders for the same trajectory.

**Reasoning:**

The gap magnitudes are substantial. For standard data, CLM-01 claims 1,250 gaps out of 4,000 nominal IDs (31.2% gap rate). For hierarchical, CLM-02 claims 143 out of 5,000 (2.9%). Even if these figures are unverified, the consolidated-context.md File Naming Conventions section explicitly states: "Non-contiguous IDs are intentional — caused by generation continuation, prescreen rejection, and failed Brutus runs. The numeric ID is NOT an index; gaps exist (CLM-01, CLM-02)." This is a direct dataset documentation statement. Any linear-indexing assumption will produce wrong mappings for standard data at minimum, and potentially for hierarchical data as well.

The gold-side mapping adds a further complication: the same numeric ID exists in both base and gold folders. The variant is disambiguated by folder, not by filename infix (ERRATUM Correction 1).

**Evidence:**

- `consolidated-context.md` — File Naming Conventions: non-contiguous IDs are intentional.
- `claims-table.md` CLM-01 (1,250/4,000 standard gaps, claimed-unverified), CLM-02 (143/5,000 hierarchical gaps, claimed-unverified).
- `ERRATUM-2026-06-10.md` Correction 1: gold filenames carry no `_gold_` infix.

**Confidence:** High  
**Key factor that would change answer:** Empirical verification of CLM-01 and CLM-02 gap counts (Phase 24 DATA-01). Even if the exact gap counts differ, the fact of non-contiguity is stated in dataset documentation and is not in dispute.

**Verification suggestion:** Build the `id_to_path` dictionary and verify that (a) no ID maps to a wrong trajectory, and (b) the 10 randomly selected gapped IDs from the issue doc's verification checklist all resolve correctly.

**Proposed specification text for `ctl_instruction.md`:**

Insert in the DataLoader Requirements section:

> **ID Resolution Contract (PIPE-02).** The DataLoader must build an `id_to_path` mapping by scanning all Brutus output folders at initialization. The mapping key is the numeric ID extracted from the filename. The mapping value includes the full filesystem path and the variant (determined by folder location, not filename). No code path may assume dense linear indexing (ID == array index). Curriculum stage assignment and batch construction must use the `TrajectoryIndex` for all ID resolution.

---

### Q-A3 (M11) — Blacklist Loading / Consumption

**Verdict / Recommendation:**

1. The blacklist (`problematic_ics_blacklist.json`) must be loaded at DataLoader `__init__`.
2. Blacklisted IDs must be excluded from the `TrajectoryIndex` (they must not appear in any batch).
3. The exclusion count must be logged at initialization (INFO level): `"Blacklist loaded: {N} IDs excluded ({N_hier} hierarchical, {N_std} standard)"`.
4. If a blacklisted ID appears in a batch request, this must raise a hard error (not a warning).
5. The blacklist consumption status must be verified as part of the DataLoader acceptance test.

**Reasoning:**

The core M11 finding — that the blacklist is not loaded — is a data-integrity gap. The blacklist count (CLM-03: 65 IDs = 2 hierarchical + 63 standard) is directly observable in the JSON file, though marked `claimed-unverified` pending Phase 24. The severity reclassification from MAJOR to BLOCKING is justified: silently admitting blacklisted ICs corrupts the training data at ingestion time, and the corruption is invisible without explicit checking. The consumption status (whether the DataLoader actually enforces the exclusion) is a separate question from the count, and it is the critical one. A DataLoader that can silently admit known-bad ICs fails a minimal correctness bar.

**Evidence:**

- `02-data-pipeline-and-validation.md` line 59, 76, 341 — M11 finding (non-authoritative).
- `claims-table.md` CLM-03 — 65 IDs (claimed-unverified; count observable in JSON).
- `consolidated-context.md` — Blacklist summary: `hierarchical: [123, 253]`, `standard: [21, 30, 52, ...]`, total 65.

**Confidence:** High  
**Key factor that would change answer:** Phase 24 DATA-02 verification that the blacklist file is intact and the 65-ID count is correct. Even if the count differs, the loading mechanism is required regardless of count.

**Verification suggestion:** Unit test: load the blacklist, attempt to access a known-blacklisted ID through the DataLoader, confirm a hard error is raised. Confirm the exclusion count matches the JSON file.

**Proposed specification text for `ctl_instruction.md`:**

Insert in the DataLoader Requirements section:

> **Blacklist Consumption Contract (PIPE-03).** The DataLoader must load `problematic_ics_blacklist.json` at initialization and exclude all listed IDs from the `TrajectoryIndex`. The exclusion count (hierarchical and standard) must be logged at INFO level. Any attempt to construct a batch containing a blacklisted ID must raise a hard error. The blacklist consumption status is an acceptance-test requirement.

---

### Q-A4 (M13) — 184 Standard IDs Without a Gold Counterpart (Fallback Policy)

**Verdict / Recommendation:**

**Insufficient evidence to assert a fallback. This is a Phase-26 STOP-gap candidate.**

The package provides two candidate fallbacks but no basis for choosing between them:

- **Option 1 (skip to Stage 6):** Safe — ensures that only gold-verified data enters Stage 5. But it means 184 standard IDs have no high-resolution training path, which may reduce curriculum coverage in Stage 5 and increase the data jump between Stage 4 and Stage 6.
- **Option 2 (admit flagged low-fidelity standard sample):** Preserves the 184 IDs in the training pool but introduces a fidelity mismatch — the network trains on standard-resolution data in a stage designed for gold-resolution refinement. The `warning flag` would need to propagate through the loss computation so that the training loop can weight standard-fidelity samples differently, but training-loop weighting is out of scope (deferred to doc-03).

**Conditional analysis:**

- If Stage 5's pedagogical purpose is high-resolution refinement of trajectories already learned at low resolution (which is consistent with the CTL framework's design — see `ctl_instruction.md` Stage 2 and Stage 5 descriptions), then **Option 1** is more principled: a trajectory that has no gold data cannot participate in high-resolution refinement and should skip ahead.
- If Stage 5's purpose includes first-exposure training on chaotic trajectories (regardless of fidelity), then **Option 2** is necessary to avoid a coverage gap.

The resolution depends on the training-loop semantics of Stage 5, which is partially a doc-03 question (training-loop usage). The data-side contract can only specify: "the DataLoader must expose a `has_gold_counterpart` flag for each standard ID, and the 184 IDs without gold counterparts must be queryable."

**Evidence:**

- `claims-table.md` CLM-04 (184 standard IDs without gold, verified), CLM-05 (2,749 base vs 2,565 gold, verified).
- `consolidated-context.md` — Full list of 184 IDs from `standard_quasi_random_ids_not_in_gold.md`.
- `02-data-pipeline-and-validation.md` line 65, 316, 342 — M13 finding with two candidate options (non-authoritative).
- `ctl_instruction.md` Stage 5 description — Stage 5 is "High-Resolution Chaotic Orbits" using Set 2b (gold), same criteria as Stage 4.

**Confidence:** Medium  
**Key factor that would change answer:** A determination of whether Stage 5 training is strictly a refinement stage (gold data required) or also a first-exposure stage (standard data acceptable with fidelity flag). This is a training-loop design decision.

**Verification suggestion:** The downstream adjudication should determine Stage 5's role relative to fidelity requirements before closing this item.

**Proposed specification text for `ctl_instruction.md`:**

> **Gold-Counterpart Availability Contract (PIPE-05).** The DataLoader must expose a `has_gold_counterpart: bool` flag for every standard quasi-random ID. The set of 184 IDs lacking gold counterparts (CLM-04, verified) must be queryable. The fallback policy for these IDs at Stage 5 is a **STOP-gap** pending training-loop design determination (doc-03).

---

### Q-A5 (D7) — Footer / Parameter Heterogeneity

**Verdict / Recommendation:**

1. **When a file has a `Result:` footer containing `tol`:** Use the footer value directly. Provenance = `DIRECT`.
2. **When a file has no `Result:` footer (ERRATUM Correction 2: 1,550 hierarchical + 701 standard + 219 standard-gold files):** Use the folder-default `tol` from CLM-09. Provenance = `INFERRED_FOLDER_DEFAULT`.
3. **When a file has a `Result:` footer but `tol` is absent:** Use the folder-default `tol`. Provenance = `INFERRED_FOLDER_DEFAULT`.
4. The folder-default parameters per variant (CLM-09, verified) are:

| Variant | Default tol | Default dt_out |
|---|---|---|
| Standard quasi-random | 1e-13 | 0.17 |
| Hierarchical base | 1e-15 | 0.08 |
| Gold standard (both) | 1e-13 | 0.01 |

5. The `tol_confidence` field should be an enum: `{DIRECT, INFERRED_FOLDER_DEFAULT}` — not the issue doc's `'direct'` vs `'inferred'` strings, to avoid typos and ensure type safety.
6. At DataLoader initialization, log the count of inferred tolerances per variant.

**Reasoning:**

The ERRATUM (Correction 2) significantly revises the footer picture: "partial" and "minimal" footer files contain NO `Result:` footer at all — no `eta`, no `tol`, no `Lw`, no energy fields. The earlier consolidated-context.md statement that "All Brutus output files contain a `Result:` footer" is incorrect. This means the fallback-to-folder-default path is needed for 2,470 files out of ~15,028 (about 16.4%). The folder defaults are verified (CLM-09), so the inference is well-grounded. The two-value provenance enum captures the only distinction that matters: did the `tol` value come from the file itself or from the folder default?

**Evidence:**

- `ERRATUM-2026-06-10.md` Correction 2 — 1,550 + 701 + 219 files have no footer.
- `claims-table.md` CLM-07 (219 minimal-footer files, verified count, character corrected by ERRATUM), CLM-08 (592 `tol=1e-14` files, verified), CLM-09 (folder defaults, verified).
- `consolidated-context.md` — Brutus Parameters by Variant (subject to ERRATUM corrections).

**Confidence:** High  
**Key factor that would change answer:** A finding that some variant folders contain files with `tol` values inconsistent with the folder default (e.g., the 592 files at `tol=1e-14` in the standard gold folder where the default is `1e-13`). This is already documented (CLM-08) and does not affect the fallback policy — those files have DIRECT provenance because they have footers with `tol`.

**Verification suggestion:** Parse all 15,028 files, assign provenance, and verify that the DIRECT-count and INFERRED-count per variant match the ERRATUM figures.

**Proposed specification text for `ctl_instruction.md`:**

> **Footer-Handling Contract (PIPE-06).** When loading Brutus metadata, parse the `Result:` footer if present. If the footer contains `tol`, record the value with provenance `DIRECT`. If the file has no `Result:` footer or the footer lacks `tol`, record the folder-default `tol` (CLM-09) with provenance `INFERRED_FOLDER_DEFAULT`. The `tol_provenance` field is an enum `{DIRECT, INFERRED_FOLDER_DEFAULT}`. Log the count of inferred tolerances per variant at DataLoader initialization.

---

### Q-A6 (D-03) — Processed Training-Data Format (HDF5 vs .npy vs txt/json)

**Verdict / Recommendation:**

1. **HDF5 (`.h5`) is the primary format** for processed training data.
2. **NumPy (`.npy`) is an acceptable alternative** per the existing spec (`ctl_instruction.md` Step 1 item 6).
3. **An optional JSON export** may be provided for inspection and debugging only — not for training-time loading.
4. **txt/json is NOT acceptable as the primary training format** due to parsing overhead (10–100× slower than HDF5 reads), lack of compression, and lack of hierarchical grouping.
5. **Zero methodology consequence** — this is a storage and performance decision that does not alter any computation, normalization, or training parameter.

**Reasoning:**

The framework spec already recommends HDF5 or `.npy` (`ctl_instruction.md` Step 1 item 6). The question of migrating to txt/json was raised only in the issue doc and has no spec support. HDF5 provides zero-copy tensor loading, built-in compression, and hierarchical grouping — all essential for a dataset of ~15,028 trajectories with hundreds of snapshots each (~4.8 GB total). The only advantage of txt/json is human readability, which is adequately served by an optional export mode. No first-principles analysis suggests that the storage format affects the physics or the training methodology.

**Evidence:**

- `ctl_instruction.md` Step 1 item 6 — "Save parsed objects for all simulations into an efficient format like HDF5 or NumPy (.npy) files."
- `02-data-pipeline-and-validation.md` lines 27–49, 173–190, 262–277 — Format question (non-authoritative).
- `consolidated-context.md` — Dataset size: ~4.86 GB total.

**Confidence:** High  
**Key factor that would change answer:** A finding that HDF5 is unavailable on the target deployment platform (extremely unlikely for scientific computing).

**Verification suggestion:** Confirm that the DataLoader reads HDF5 files correctly on the target platform and that an optional JSON export produces inspectable output for 10 sample trajectories.

**Proposed specification text for `ctl_instruction.md`:**

No change needed — the existing Step 1 item 6 already specifies HDF5 or `.npy`. Add an informational note:

> **Storage Format (PIPE-10).** The primary processed-training-data format is HDF5 (`.h5`). NumPy (`.npy`) is an acceptable alternative per Step 1 item 6. An optional JSON export mode may be provided for inspection only; JSON is not a training-path format.

---

## §4 Resolutions — Cluster B: Sampling, Precision & Global Scale

### Q-B1 (M12) — Points-per-Trajectory Feasibility

**Verdict / Recommendation:**

The fixed 32-points-per-trajectory batch spec (`ctl_instruction.md` §Mini-Batch Construction, line 1201: `n_pts` e.g., 32) is infeasible for standard trajectories with ~59 snapshots (CLM-10). The correct contract is an **adaptive cap**:

```
n_pts = min(n_pts_max, int(floor_fraction * n_snapshots))
```

with parameters:
- `n_pts_max = 32` (the existing spec maximum)
- `floor_fraction = 0.5` (sample at most 50% of available snapshots to avoid overfitting to the discrete grid)

This yields:
- Standard (~59 snapshots): `min(32, int(0.5 * 59)) = min(32, 29) = 29`
- Hierarchical (~125 snapshots): `min(32, int(0.5 * 125)) = min(32, 62) = 32`
- Gold (~1000 snapshots): `min(32, int(0.5 * 1000)) = min(32, 500) = 32`

The 50% floor fraction ensures that no variant samples more than half its available snapshots, which preserves the gap between data points for the physics residual to operate. For standard trajectories, the 54% sampling ratio the issue doc identifies (32/59) is reduced to 49% (29/59), which is marginal but feasible.

**Reasoning:**

The issue doc's proposed `n_pts = min(32, int(0.5 * n_snapshots))` (P1-4) is correct in form. I adopt it with the same `floor_fraction = 0.5` and `n_pts_max = 32`. The justification for the 50% cap is that a PINN's physics residual evaluates at collocation points between data points; sampling more than half the available snapshots reduces the inter-point gap and limits the physics residual's effectiveness. The choice of 0.5 is a reasonable default but could be tuned in doc-03 (training-loop scope).

The issue doc's reclassification from MAJOR to BLOCKING is justified: with 59 available snapshots and a fixed 32-point requirement, the DataLoader cannot construct valid batches for standard data without the adaptive cap.

**Evidence:**

- `ctl_instruction.md` line 1201 — `n_pts` e.g., 32.
- `claims-table.md` CLM-10 — ~59 / ~125 / ~1000 snapshots per variant (claimed-unverified; README warns against hard-coding).
- `02-data-pipeline-and-validation.md` lines 60, 77, 286 — M12 finding and P1-4 proposal (non-authoritative).

**Confidence:** High  
**Key factor that would change answer:** Empirical verification of actual snapshot counts (CLM-10). If standard trajectories have significantly fewer than 59 snapshots on average, the floor fraction may need to be raised.

**Verification suggestion:** Construct batches for 100 randomly selected standard trajectories using the adaptive cap. Verify that `n_pts` is always ≤ `n_snapshots` and that the sampling ratio never exceeds 50%.

**Proposed specification text for `ctl_instruction.md`:**

Replace the `n_pts` specification in §Mini-Batch Construction:

> **Adaptive Points-per-Trajectory Contract (PIPE-04).** The number of time points sampled per trajectory is `n_pts = min(n_pts_max, int(floor_fraction * n_snapshots))`, where `n_pts_max = 32`, `floor_fraction = 0.5`, and `n_snapshots` is the trajectory's actual snapshot count. This ensures the sampling ratio never exceeds 50% of available data points and caps at the spec maximum.

---

### Q-B2 — Footer / Mass-Drift Protocol

**Verdict / Recommendation:**

The data pipeline must verify mass consistency between IC files and Brutus `t=0` output using the following protocol:

1. **Sample size:** Parse at least 1,000 IC–Brutus pairs (covering all four variants proportionally).
2. **Comparison method:** For each pair, compare `m_IC` vs `m_Brutus_t0` using `np.allclose(m_IC, m_Brutus_t0, rtol=1e-15)`.
3. **Decision rule:**
   - If the failure rate is **0%**: Document IC masses as canonical. Use IC masses for all downstream computation. No `decimal.Decimal` parsing needed.
   - If the failure rate is **> 0% and ≤ 1%**: Use `decimal.Decimal` for mass parsing in the affected files only. Log each mismatched pair at WARNING level.
   - If the failure rate is **> 1%**: Switch to `decimal.Decimal` for all mass parsing. Investigate root cause (text rounding, integrator issue).
4. **Fallback:** If `decimal.Decimal` parsing is required, parse the `t=0` snapshot masses from the Brutus output using `decimal.Decimal` and use those as the canonical masses.

**Reasoning:**

Brutus uses arbitrary-precision arithmetic (GMP/MPFR), so masses should be preserved exactly within the integrator. However, text output may round at the rendering stage. The `rtol=1e-15` threshold is appropriate because `float64` has ~1e-16 relative precision, and Brutus convergence tolerances range from 1e-13 to 1e-15 (CLM-09). Any mass drift larger than 1e-15 in float64 representation indicates either text rounding or a genuine integrator artifact. The sample size of 1,000 provides statistical confidence: if the true failure rate is 0.1%, the probability of detecting at least one failure is ≈1 − (0.999)^1000 ≈ 63%.

**Evidence:**

- `02-data-pipeline-and-validation.md` lines 196–207, P2-2 line 292 — Mass-drift protocol (non-authoritative).
- `claims-table.md` CLM-09 — Folder-default tolerances (1e-13 to 1e-15).
- `data_quality_assessment.md` §1.1 — Brutus uses Bulirsch-Stoer with arbitrary-precision arithmetic.

**Confidence:** Medium  
**Key factor that would change answer:** Empirical results of the mass-consistency probe (Phase 24 DATA-05). If the failure rate is unexpectedly high, the root cause may require a different remediation.

**Verification suggestion:** Run the mass-consistency probe on 1,000 pairs and report the failure rate. If zero failures, confirm IC masses match Brutus `t=0` masses to `float64` precision.

**Proposed specification text for `ctl_instruction.md`:**

Insert in Step 2.1 (Parser contract and mass-invariance check):

> **Mass-Consistency Verification Protocol (PIPE-07).** Before training, verify mass consistency between IC and Brutus `t=0` output: parse ≥1,000 IC–Brutus pairs, compare with `np.allclose(rtol=1e-15)`. If failure rate = 0%, document IC masses as canonical. If failure rate > 0%, switch to `decimal.Decimal` parsing for affected files and use Brutus `t=0` masses as canonical. Log all mismatches.

---

### Q-B3 — Precision Handling (float64 Sufficiency; Decimal-for-Masses)

**Verdict / Recommendation:**

1. **`float64` is sufficient for all validation metrics** (SCS, SASD, IPR, PSC) and for all runtime data loading and computation.
2. **`float64` relative precision (~1e-16)** provides 1–3 guard digits beyond the Brutus convergence tolerances (CLM-09: 1e-13 to 1e-15), which is adequate for validation.
3. **`decimal.Decimal` is required only for the mass-consistency verification step** (Q-B2) — specifically for parsing `t=0` snapshot masses when the `np.allclose(rtol=1e-15)` check fails.
4. **No other component** of the data pipeline or training loop requires arbitrary-precision parsing.

**Reasoning:**

The Brutus output files contain 30–40 significant digits, but this precision is only meaningful relative to the integrator's convergence tolerance. For the standard and gold variants (tol = 1e-13), `float64` provides 3 guard digits. For the hierarchical base variant (tol = 1e-15), `float64` provides 1 guard digit. This is the same reasoning the issue doc uses, and it is sound. The dual-epsilon constraint (Hard Constraint 4) already establishes that validation metrics run at `ε = 1e-10`, which is well within `float64` precision. The only scenario where `float64` is insufficient is exact mass comparison, because text rounding can introduce errors at the 1e-16 level — hence the `decimal.Decimal` fallback in Q-B2.

**Evidence:**

- `02-data-pipeline-and-validation.md` lines 208–216 — Precision handling analysis (non-authoritative, but the float64-precision argument is correct).
- `claims-table.md` CLM-09 — Folder-default tolerances: std 1e-13, hier 1e-15, gold 1e-13.
- `pinn_architecture.md` §3.2 — Training-time softening `ε_train = 1e-5`; validation uses static `ε = 1e-10`.
- `data_quality_assessment.md` §1.1 — Brutus convergence is to specified tolerance.

**Confidence:** High  
**Key factor that would change answer:** A finding that the Brutus output rendering introduces systematic rounding beyond 1e-13 for a significant fraction of trajectories. The mass-drift probe (Q-B2) would detect this.

**Verification suggestion:** Compare `float64`-parsed and `Decimal`-parsed positions for 100 Brutus output files. Confirm that the maximum relative difference is below the variant-specific tolerance.

**Proposed specification text for `ctl_instruction.md`:**

Insert in Step 2.1 after the mass-consistency protocol:

> **Precision Handling (PIPE-08).** All validation metrics and training-data loading use `float64`. `decimal.Decimal` is used only for mass-consistency verification when the `float64` comparison fails (see Mass-Consistency Verification Protocol). No arbitrary-precision parsing is required for position, velocity, or acceleration data at any pipeline stage.

---

### Q-B4 — Global-Scale `compute_globals` / D = 6.694 (KNOWN CONFLICT)

**Verdict / Recommendation:**

**The data pipeline must use the locked raw-mass convention `D = (G·T²)^(1/3) ≈ 4.6416`.**

Adopting the issue doc's `D = (G·M_tot·T²)^(1/3) ≈ 6.694` would violate Hard Constraint 6 (PHYS-01) and require rewriting the following components:

1. Every residual in the physics loss (`pinn_architecture.md` §3.2)
2. The matched-Plummer Hamiltonian (`pinn_architecture.md` §3.4)
3. The angular-momentum loss (`pinn_architecture.md` §3.5)
4. The COM projection and assertion checks (`ctl_instruction.md` Step 2.2, 2.6)
5. All invariant computations (`ctl_instruction.md` Step 3)
6. The IC₁₃ normalization scales
7. The `compute_globals` function itself (which would need `M_tot` in every formula)

The issue doc's formula `D = cbrt(G · M_tot · t_max²)` is mathematically correct under a mass-fraction convention where `m_i' = m_i / M_tot`. In that convention, the dimensionless equation of motion becomes:

$$\frac{d^2 \mathbf{r}'_i}{du^2} = \sum_j m_j' \frac{\mathbf{r}'_j - \mathbf{r}'_i}{||\mathbf{r}'_j - \mathbf{r}'_i||^3}$$

with `D^3 = G · M_tot · T²`. But the project has locked the raw-mass convention where `m_i` (not `m_i/M_tot`) appears in the residuals, forcing `D^3 = G · T²`. These two conventions produce identical physics but different numerical values for `D` and all derived scales. They cannot be mixed.

**Reconciliation:** The issue doc's `D = 6.694` is not wrong — it is wrong *for this project's locked convention*. The locked convention was chosen explicitly and ratified (PHYS-01, Phase 19). Changing it would require touching every formula in the framework, which is precisely what `ctl_instruction.md` §2.5 line 598 warns against: "The alternative D = (G M_tot T²)^(1/3) ≈ 6.694 is correct only under a mass-fraction convention rewrite (m_i' = m_i / M_tot) that would require touching every residual, Hamiltonian, angular-momentum, COM, and invariant formula in the framework."

**Evidence:**

- `ctl_instruction.md` §2.5 (lines 581–604) — Locked PHYS-01 convention: `D = (G·T²)^(1/3) ≈ 4.6416`, explicit rejection of 6.694.
- `framed-research-questions.md` Hard Constraint 6 — Locked counter-position.
- `claims-table.md` CLM-13 — `D = 6.694` is a contested convention claim, not a dataset count.
- `02-data-pipeline-and-validation.md` lines 218–258, P1-7 line 289 — Issue doc position (non-authoritative).

**Confidence:** High  
**Key factor that would change answer:** A future user directive reopening PHYS-01. Under current hard constraints, this is settled.

**Verification suggestion:** Confirm that `compute_globals` uses `D = (G·T²)^(1/3)` and that all derived scales (`E_scale`, `smin_scale`) are consistent with this value.

**Proposed specification text:** No change — the existing `ctl_instruction.md` §2.5 already locks this convention. The issue doc's P1-7 ("Recompute global scales with corrected D=6.694") must be rejected.

---

## §5 Resolutions — Cluster C: Validation Metrics

### Q-C1 (SCS) — Symplectic Conservation Score (Definition + Thresholds, KNOWN CONFLICT)

**Verdict / Recommendation:**

**The locked log-drift definition and gate govern.** The correct SCS definition is:

- **Raw drift:** `ε_H = max_t |(H(t) − H(0)) / H(0)|`
- **Log score:** `SCS = log₁₀(ε_H)`
- **Reject gate:** `SCS > −5` (equivalently `ε_H > 10⁻⁵`)
- **Marginal band:** `−6 < SCS ≤ −5` (keep for review, not clean training)
- **Acceptable band:** `−10 < SCS ≤ −6`
- **Excellent:** `SCS ≤ −10`

The issue doc's ratio-based thresholds (`SCS > 1e-6` for Phase-1 screening, `SCS < 1e-8` for high-resolution) are **raw-drift numbers** expressed as ratios, not log-drift scores. The quantities are related by:

| Issue doc ratio threshold | Equivalent SCS | Relation to locked gate |
|---|---|---|
| `ε_H > 1e-6` | `SCS > −6` | Stricter than locked gate (−5) |
| `ε_H < 1e-8` | `SCS < −8` | Much stricter than locked gate |

**Reconciliation:** The issue doc and the locked gate use the same underlying quantity (`ε_H`) but express it in different units (raw ratio vs. logarithm). They are not contradictory — they are different representations of the same physics. The locked gate at `SCS > −5` (`ε_H > 10⁻⁵`) is the permissive bound; the issue doc's `1e-6` threshold is stricter. The locked gate is the ratified decision and governs. The issue doc's `1e-8` "tightening" for gold data is a training-loop policy suggestion (out of scope for data-side definition) and would need to be evaluated in doc-03.

**SCS must be computed with the static validation epsilon `ε = 1e-10`** for the gravitational force (per Hard Constraint 4: validation metrics run with `ε = 1e-10`). This is distinct from the training-time `ε_train = 1e-5`.

**Special case:** If `H(0)` is zero or near-zero, `SCS` is undefined. Flag such trajectories for manual review rather than forcing them through the logarithmic gate (per `data_quality_assessment.md` §3.1).

**Reasoning:**

The seed conflict is a units mismatch, not a physics disagreement. The issue doc writes the raw ratio (e.g., `1e-6`) while the locked convention writes the base-10 logarithm (e.g., `−6`). Once translated, the issue doc's Phase-1 threshold (`ε_H > 1e-6`, i.e., `SCS > −6`) is one order of magnitude stricter than the locked gate (`SCS > −5`). The locked gate was ratified by SI-DQA-003 after the original gate inconsistency was discovered. Adopting the issue doc's thresholds would override a locked convention.

**Evidence:**

- `data_quality_assessment.md` §3.1, §5.1, SI-DQA-003 — Locked SCS definition and gate.
- `framed-research-questions.md` Hard Constraint 5 — Post-v1.3 SCS gate locked at `SCS > −5`.
- `02-data-pipeline-and-validation.md` lines 129–141 — Issue doc ratio thresholds (non-authoritative).
- `pinn_architecture.md` §3.4 — Dual-epsilon split; `ε_train = 1e-5` for training, static `ε = 1e-10` for validation.

**Confidence:** High  
**Key factor that would change answer:** A future user directive reopening the SCS gate threshold.

**Verification suggestion:** Compute SCS for 100 trajectories from each variant using the locked definition. Verify that the pass/fail classification matches the locked gate.

**Proposed specification text for `data_quality_assessment.md` (sole written home):**

No change needed — the existing `data_quality_assessment.md` §3.1 already contains the correct definition and gate. The issue doc's ratio thresholds are noted as stricter-than-locked alternatives that would require a convention change to adopt.

---

### Q-C2 (SASD) — Stiffness-Aware Sampling Density (Data-Side)

**Verdict / Recommendation:**

The correct data-side SASD definition is:

$$SASD_i = \Delta t_i \cdot \frac{\|a(t_i)\|}{\|v(t_i)\|}$$

where:
- `Δt_i` is the time interval between consecutive snapshots (computed from Brutus output timestamps, not hard-coded)
- `a(t_i)` is the acceleration at time `t_i` (derived from the Brutus data, computed with the **static validation epsilon** `ε = 1e-10` for the gravitational force)
- `v(t_i)` is the velocity at time `t_i`
- All quantities are in **scaled units** (after the Phase 18 preprocessing contract)

**Flag/resample criterion:** `max(SASD) > 0.5` — the trajectory turns significantly between data points and should be flagged for review or higher-resolution re-simulation.

**Robust variant (recommended for implementation):** At turning points where `‖v‖ → 0`, the basic SASD diverges. A robust variant uses the curvature radius:

$$SASD_i^{robust} = \Delta t_i \cdot \sqrt{\frac{\|a(t_i)\|^2 - (a \cdot \hat{v})^2}{\|v(t_i)\|^2 + \epsilon_{SASD}^2}}$$

where `ε_SASD = 1e-10` prevents division by zero. This measures the angular turning rate more robustly.

**Reasoning:**

The SASD metric captures the ratio of the sampling interval to the local dynamical timescale. When `SASD > 1`, the trajectory completes a significant fraction of an orbit between snapshots, meaning the discrete data cannot faithfully represent the continuous physics. The `0.5` threshold is grounded in the data quality assessment report (`data_quality_assessment.md` §3.2: "Data with SASD > 0.5 should be flagged for resampling"). The use of `ε = 1e-10` for force computation follows from Hard Constraint 4 (validation uses static epsilon).

The issue doc's `ε = 1e-5` for IPR is a training-loop concern (out of scope). For data-side SASD, the validation epsilon is appropriate because SASD is a pre-training data-quality metric, not a training-loss component.

**Evidence:**

- `data_quality_assessment.md` §3.2 — SASD definition and flag criterion.
- `02-data-pipeline-and-validation.md` lines 143–153 — Issue doc SASD definition (non-authoritative; matches the DQA definition).
- `claims-table.md` CLM-09, CLM-10 — Per-variant `dt_out` and snapshot counts.

**Confidence:** Medium  
**Key factor that would change answer:** Empirical distribution of SASD across the dataset. If a large fraction of trajectories exceed the 0.5 threshold, the flag criterion may need adjustment or a tiered flagging system.

**Verification suggestion:** Compute SASD profiles for 100 trajectories per variant. Report the distribution of `max(SASD)` and the fraction exceeding 0.5 per variant.

**Proposed specification text for `data_quality_assessment.md`:**

Amend §3.2 with the robust variant and explicit epsilon:

> **SASD Data-Side Definition (VAL-02).** `SASD_i = Δt_i · ‖a(t_i)‖ / ‖v(t_i)‖` in scaled units, with gravitational acceleration computed using static validation softening `ε = 1e-10`. Flag criterion: `max(SASD) > 0.5`. Robust variant uses curvature-based formula with `ε_SASD = 1e-10` to prevent divergence at turning points. The time intervals `Δt_i` are computed from actual Brutus timestamps, not hard-coded.

---

### Q-C3 (IPR) — Interpolation Physics Residual (Data-Side, Dual-Epsilon)

**Verdict / Recommendation:**

The correct data-side IPR definition is:

1. **Construct** a piecewise Cubic Hermite Interpolating Polynomial (PCHIP) `q_spline(t)` from the Brutus snapshot data `{(q_i, v_i)}` at times `{t_i}`.
2. **Sample** `M` synthetic collocation points `{τ_k}` uniformly distributed between consecutive data points.
3. **Compute** the physics residual at these synthetic points:

$$IPR = \frac{1}{M} \sum_{k=1}^{M} \left\| \frac{d^2 q_{spline}}{dt^2}(\tau_k) - F_{gravity}^{\varepsilon=1e-10}(q_{spline}(\tau_k)) \right\|^2$$

4. **The gravitational force uses the static validation epsilon `ε = 1e-10`**, per Hard Constraint 4 (validation metrics run with `ε = 1e-10`).

**The issue doc's use of `ε = 1e-5` for IPR contradicts the locked dual-epsilon split.** The issue doc states IPR is "computed with the dynamic softening `ε = 1e-5`" (line 159). This is incorrect for a data-side metric. The dual-epsilon constraint explicitly assigns `ε = 1e-10` to validation and `ε = 1e-5` to training. IPR, as a pre-training data-quality metric, belongs on the validation side.

**Reasoning:**

The IPR's purpose is to evaluate whether the continuous manifold implied by the discrete data points satisfies Newton's laws. It is a data-quality check, not a training-loss component. The dual-epsilon split (Hard Constraint 4) was designed precisely for this distinction: validation metrics use the tighter epsilon to measure true Newtonian fidelity, while training uses the looser epsilon to regularize the physics loss. Using `ε = 1e-5` for IPR would soften the gravitational force during validation, masking close-encounter artifacts that the metric is designed to detect. This would defeat the purpose of the IPR as a data-quality gate.

**Flag criterion:** `IPR > 1e-3` — the data is aliased; reject or resample (per `data_quality_assessment.md` §5.1, Phase 1 Manifold Check).

**Evidence:**

- `data_quality_assessment.md` §3.3 — IPR definition (consistent with this recommendation).
- `02-data-pipeline-and-validation.md` lines 155–165 — Issue doc IPR definition with `ε = 1e-5` (non-authoritative; contradicts Hard Constraint 4).
- `pinn_architecture.md` §3.2 — Dual-epsilon split: validation `ε = 1e-10`, training `ε_train = 1e-5`.
- `ctl_instruction.md` ≈line 703 — Dual-epsilon split noted.

**Confidence:** High  
**Key factor that would change answer:** A finding that the Plummer softening at `ε = 1e-10` causes numerical instabilities in the IPR computation at close-encounter configurations. This is unlikely given that the validation metrics are designed to run at this epsilon.

**Verification suggestion:** Compute IPR for 50 trajectories per variant using both `ε = 1e-10` and `ε = 1e-5`. Report the difference in IPR values and confirm that `ε = 1e-10` does not produce NaN or Inf.

**Proposed specification text for `data_quality_assessment.md`:**

Amend §3.3 with explicit epsilon specification:

> **IPR Data-Side Definition (VAL-03).** IPR uses cubic Hermite spline interpolation of Brutus snapshot data, evaluated at synthetic collocation points between snapshots. The gravitational force in the residual uses the **static validation softening** `ε = 1e-10` (per the dual-epsilon contract, Hard Constraint 4). This is distinct from the training-time softening `ε_train = 1e-5` used in the physics loss. Flag criterion: `IPR > 1e-3`.

---

### Q-C4 (PSC) — Phase Space Coverage Entropy (Data-Side)

**Verdict / Recommendation:**

The correct data-side PSC definition is:

1. **Grid construction:** Partition the 6-dimensional pairwise-separation and pairwise-velocity phase space into equal-volume bins. The dimensions are `(r₁₂, r₂₃, r₃₁, v₁₂, v₂₃, v₃₁)` where `r_ij = ‖r'_i − r'_j‖` and `v_ij = ‖v'_i − v'_j‖` in scaled units. All pairwise quantities are permutation-invariant by construction (after canonical ordering).

2. **Bin count:** Use the rule-of-thumb `K = N^{2/(2+d)}` where `N` is the total number of data points and `d = 6` is the dimensionality. For ~15,000 trajectories × ~100 snapshots average ≈ 1.5M points, this gives `K ≈ 150`. Alternatively, use maximum-likelihood estimation (as in the Miller-Madow correction). The exact bin count is a tunable parameter; the definition requires only that a consistent method is documented.

3. **Entropy estimator:** Shannon entropy with bias correction:

$$H_{data} = -\sum_{k=1}^{K} \hat{p}_k \log(\hat{p}_k) + \frac{K - 1}{2N}$$

where `p̂_k = n_k / N` is the empirical probability and `(K−1)/(2N)` is the Miller-Madow bias correction for finite-sample entropy estimation.

4. **Stiffness-coverage submetric:** Additionally, compute the fraction of data points in the "close-encounter" bin where `min(r₁₂, r₂₃, r₃₁) < s_threshold` with `s_threshold = 0.5` (in scaled units, consistent with the Stage 6 criterion). If this fraction is zero, the dataset lacks close-encounter coverage.

**Reasoning:**

The PSC metric quantifies training-data diversity, which is essential for generalization in chaotic systems. The 6D pairwise-separation/velocity space is permutation-invariant (after canonical ordering) and captures the physically relevant degrees of freedom. The Miller-Madow correction addresses the well-known downward bias of the naive Shannon entropy estimator. The stiffness-coverage submetric addresses the specific risk identified in `data_quality_assessment.md` §3.4: "Specifically check the bin corresponding to `r_min → 0`. If this bin is empty, the dataset lacks the 'hard' physics examples."

The issue doc's definition (PSC = Shannon entropy of data points across a discretized phase-space grid) is consistent with this recommendation but underspecified. The grid construction and bias correction are necessary for the metric to be reproducible and comparable across datasets.

**Evidence:**

- `data_quality_assessment.md` §3.4 — PSC definition and stiffness-coverage analysis.
- `02-data-pipeline-and-validation.md` lines 167–169 — Issue doc PSC definition (non-authoritative; consistent but underspecified).

**Confidence:** Medium  
**Key factor that would change answer:** Empirical evaluation of the grid construction. If the 6D binning produces too many empty bins at the available sample size, a lower-dimensional projection (e.g., the `(r₁₂, r₂₃)` plane) may be more practical.

**Verification suggestion:** Compute PSC on the full dataset with `K = 150` bins. Report the entropy value, the fraction of occupied bins, and the stiffness-coverage fraction. Compare with a uniform-distribution baseline.

**Proposed specification text for `data_quality_assessment.md`:**

Amend §3.4 with the full specification:

> **PSC Data-Side Definition (VAL-04).** Phase Space Coverage Entropy is computed on a 6D pairwise `(r₁₂, r₂₃, r₃₁, v₁₂, v₂₃, v₃₁)` grid in scaled units, with equal-volume binning and bin count determined by `K = N^{2/(2+d)}` or maximum-likelihood estimation. The Shannon entropy with Miller-Madow bias correction is: `H_data = −Σ p̂_k log(p̂_k) + (K−1)/(2N)`. A stiffness-coverage submetric reports the fraction of data points with `min(r₁₂, r₂₃, r₃₁) < 0.5`.

---

## Open Items Register

| Item ID | Question | Description | Resolving Evidence |
|---|---|---|---|
| OPEN-01 | Q-A1 | Prevalence of `final_timestep >= 9.5` rule across dataset (CLM-11: claimed-unverified) | Phase 24 DATA-06: compute final_timestep distribution |
| OPEN-02 | Q-A4 | Fallback policy for 184 standard IDs without gold counterpart — STOP-gap | Training-loop design determination (doc-03): is Stage 5 strictly a refinement stage or also first-exposure? |
| OPEN-03 | Q-B1 | Actual snapshot counts per trajectory (CLM-10: claimed-unverified, ~59/~125/~1000) | Phase 24 DATA-06: count output rows per trajectory file |
| OPEN-04 | Q-B2 | Empirical failure rate of `np.allclose(rtol=1e-15)` mass-consistency check | Phase 24 DATA-05: parse 1000+ IC-Brutus pairs and compare masses |
| OPEN-05 | Q-C2 | Distribution of `max(SASD)` across the dataset; whether 0.5 threshold is appropriate | Compute SASD for representative sample per variant |
| OPEN-06 | Q-C4 | Practical bin count for 6D PSC grid at ~1.5M data points | Empirical grid-density analysis |

### Additional Input Needed

| Item ID | Missing Information | Context |
|---|---|---|
| AIN-01 | Blacklist loading/consumption status (Phase 24 DATA-02) | Q-A3 — the M11 finding that the blacklist is not loaded must be empirically confirmed |
| AIN-02 | Standard/hierarchical ID gap counts (Phase 24 DATA-01) | Q-A2 — CLM-01 and CLM-02 gap magnitudes are claimed-unverified |
| AIN-03 | Nominal IC counts (Phase 24 DATA-01) | Q-A2 — CLM-12 (~4000 standard / ~5000 hierarchical) is claimed-unverified |

---

## References

1. `specs/ctl_instruction.md` — Framework spec: preprocessing pipeline, input contract, stage assignment. Source commit `192c7c3c`.
2. `specs/pinn_architecture.md` — Framework spec: PINN architecture, loss function, dual-epsilon. Source commit `192c7c3c`.
3. `specs/data_quality_assessment.md` — Research report: SCS/SASD/IPR/PSC definitions, staged gate protocol. Source commit `d3fcff99`. Non-authoritative per manifest, but sole written home of the post-v1.3 SCS gate.
4. `specs/sampling_method.md` — FROZEN: dataset generation methodology. Source commit `916d3f84`.
5. `specs/02-data-pipeline-and-validation.md` — Adjudication subject (non-authoritative). Source commit `d43afcd6`.
6. `claims-table.md` — Claims register: CLM-01 through CLM-13. Generated in Phase 23.
7. `consolidated-context.md` — Dataset fragments. Generated in Phase 23.
8. `ERRATUM-2026-06-10.md` — Interim corrections to gold filenames and footer characterization. Dated 2026-06-10.
9. `framed-research-questions.md` — Research questions. Generated in Phase 23.
10. `README.md` — Package manifest. Generated in Phase 23.
11. Rosenstein, M. T., Collins, J. J., & De Luca, C. J. (1993). "A practical method for calculating largest Lyapunov exponents from small data sets." *Physica D*, 65(1–2), 117–134. — Referenced by the Lyapunov time estimator in `ctl_instruction.md` Step 3 item 5.
12. Sitzmann, V., Martel, J., Bergman, A., Lindell, D., & Wetzstein, G. (2020). "Implicit Neural Representations with Periodic Activation Functions." *NeurIPS 2020*. — SIREN architecture.
13. Miller, G. (1955). "Note on the bias of information estimates." *Information Theory in Psychology: Problems and Methods*, 95–100. — Miller-Madow bias correction for entropy estimation.
14. Paninski, L. (2003). "Estimation of entropy and mutual information." *Neural Computation*, 15(6), 1191–1253. — Entropy estimation methodology.
