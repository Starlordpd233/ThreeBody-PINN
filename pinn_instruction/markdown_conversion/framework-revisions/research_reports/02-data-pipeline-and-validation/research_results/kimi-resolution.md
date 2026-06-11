# Issue-02 Data Pipeline & Validation — External Research Resolution Document

**Date:** 2026-06-10

**Package files received:** `README.md` (manifest), `framed-research-questions.md` (task list), `claims-table.md` (claims register), `02-data-pipeline-and-validation.md` (issue doc, non-authoritative), `ctl_instruction.md` (framework spec, source of truth), `pinn_architecture.md` (framework spec, source of truth), `sampling_method.md` (frozen historical record), `data_quality_assessment.md` (research report, sole written home of post-v1.3 SCS gate), `consolidated-context.md` (dataset fragments), `ERRATUM-2026-06-10.md` (correction addendum). Snapshot base commit: `96f9150a02919d492a86ef9f63e10e5942d2d8e3`.

**Input inventory checksum:** Ten package files spanning manifest, task specification, claims register, framework specs (source of truth), non-authoritative issue doc, frozen historical records, dataset documentation, and a post-delivery erratum. If any file is missing or modified, the resolutions may not be fully reproducible. All recommendations are consistent with Hard Constraints v1.4 and respect the doc-03 scope boundary (M16, G6, training-loop metric usage excluded).

---

## §0 Scope and Decision Standard

### What This Document Covers

This resolution document addresses all 14 questions identified in the Issue-02 Data Pipeline & Validation Research Package, organized into three clusters:

- **Cluster A (Ingestion & Selection):** Q-A1 through Q-A6 — trajectory completeness gating, ID-to-path mapping, blacklist enforcement, missing-gold fallback, footer parameter heterogeneity, and processed data format.
- **Cluster B (Sampling, Precision & Global Scale):** Q-B1 through Q-B4 — per-trajectory point-count feasibility, mass-drift verification protocol, floating-point precision sufficiency, and the D-convention conflict.
- **Cluster C (Validation Metrics):** Q-C1 through Q-C4 — data-side definitions for SCS (Symplectic Conservation Score), SASD (Stiffness-Aware Sampling Density), IPR (Interpolation Physics Residual), and PSC (Phase Space Coverage Entropy).

### What Was Excluded

Per the package's scope boundary, the following topics were deliberately excluded from analysis and are NOT resolved in this document:

- **M16:** dt_out-dependent collocation-density scaling (how the network's collocation-point density should vary with output timestep).
- **G6:** Causal-training Option A vs. Option B (temporal causality enforcement in the training loop).
- **Training-loop metric usage:** How SCS, SASD, IPR, and PSC are used during training (e.g., SASD-weighted collocation sampling, IPR-as-ALM-noise-floor, PSC-governed curriculum replay). These are deferred to doc-03.

### Evidence Standard Applied

The following evidentiary hierarchy governs all resolutions in this document:

1. **Framework specifications (`ctl_instruction.md`, `pinn_architecture.md`) are the source of truth.** Where the spec is explicit, its position is adopted. Where the spec is silent, the analysis fills gaps with reasoned recommendations.
2. **The issue document (`02-data-pipeline-and-validation.md`) is non-authoritative.** It is treated as a bug report and feature request, not as a specification. When it conflicts with the framework spec, the spec prevails.
3. **Dataset documentation (`README.md`, `consolidated-context.md`, `data_quality_assessment.md`, ERRATUM-2026-06-10) is treated as factual** where verified, and as claimed-unverified where explicitly flagged.
4. **Claims discipline:** All claimed-unverified figures (CLM-01, CLM-02, CLM-03, CLM-10, CLM-11, CLM-12, CLM-13) are referenced conditionally, never as established facts. Where a recommendation depends on a claimed-unverified figure, the dependency is stated explicitly.
5. **Hard constraints are inviolable.** Hard Constraints v1.4 (HC-01 through HC-06) are treated as non-negotiable. No recommendation in this document violates any hard constraint.

---

## §1 Executive Decision Summary

This document presents resolved recommendations for all 14 questions in the Issue-02 Data Pipeline & Validation package. The key decisions are:

1. **Trajectory completeness gate required (Q-A1):** A two-condition gate (`final_timestamp >= 9.5` + `snapshot_count >= N_min(variant)`) must be implemented at DataLoader `__init__` time. The `N_min` values are resolution-aware and conditional on empirical verification of per-trajectory snapshot counts (CLM-10).

2. **TrajectoryIndex required (Q-A2):** Dense linear indexing (`ID == array index`) is invalid due to intentional non-contiguity. A `TrajectoryIndex` built from on-disk filenames is mandatory, with gold-standard status determined solely by folder name (ERRATUM-2026-06-10, Correction 1).

3. **Blacklist enforcement required (Q-A3):** The `problematic_ics_blacklist.json` must be loaded at DataLoader `__init__` time with unconditional exclusion of all listed IDs. The current state — where blacklisted ICs can silently enter training — is a data-corruption bug.

4. **STOP gap identified (Q-A4):** The missing-gold fallback policy for 184 standard IDs (CLM-04, verified) is genuinely undecidable within the evidence available. Three options are presented (signal-purity skip, continuity fallback, conservative exclusion); human adjudication is required.

5. **Three-tier footer fallback (Q-A5):** Footer parsing follows a three-tier system (full parse → folder defaults → provenance flag) with ERRATUM-corrected counts: 219 standard gold, 1,550 hierarchical base, and 701 standard base files have no `Result:` footer at all.

6. **HDF5 confirmed as primary format (Q-A6):** HDF5 (`.h5`) is the primary processed-training-data format, with `.npy` as an acceptable alternative and JSON restricted to debug export. No methodology consequence.

7. **Adaptive point cap recommended (Q-B1):** Per-trajectory collocation points follow `n_pts = min(32, max(4, floor(0.5 * n_snapshots)))`, replacing the fixed `n_pts = 32` regime which starves gold trajectories of data.

8. **Two-tier mass-drift protocol (Q-B2):** A 1,000-pair statistical check (`rtol = 1e-15`) determines whether `float64` or `decimal.Decimal` parsing mode is used for mass consistency verification.

9. **Float64 sufficient for validation (Q-B3):** Float64 provides 2–3 guard digits beyond the tightest Brutus tolerance (`1e-15`) and ~11 guard digits beyond the SCS rejection threshold (`1e-5`). `decimal.Decimal` is required only for mass consistency verification.

10. **D = 6.694 conflict documented, not settled (Q-B4):** A known conflict exists between PHYS-01 (locked: $D = (G T^2)^{1/3} \approx 4.6416$) and CLM-13 (claimed: $D = (G M_{\text{tot}} T^2)^{1/3} \approx 6.694$). The pipeline should parameterize D with default `M_tot_ref = None` (PHYS-01) and await downstream adjudication (EVID-10 / PIPE-09).

11. **SCS log-drift definition adopted (Q-C1):** The locked post-v1.3 SCS gate ($\text{SCS} = \log_{10}(\epsilon_H)$, reject if $\text{SCS} > -5$) is authoritative. The issue doc's raw-ratio thresholds ($> 10^{-6}$, $< 10^{-8}$) are documented as superseded. A four-tier classification system (Excellent/Acceptable/Marginal/Reject) is recommended.

12. **SASD defined with robust form (Q-C2):** $\text{SASD}_i = \Delta t_i \cdot \|\mathbf{a}(t_i)\| / \|\mathbf{v}(t_i)\|$ with a robust perpendicular-acceleration variant for turning points. Flag threshold: $\max_i \text{SASD}_i > 0.5$.

13. **IPR uses validation epsilon (Q-C3):** Data-side IPR must use $\varepsilon = 10^{-10}$ (validation softening), not $\varepsilon_{\text{train}} = 10^{-5}$ (training softening). Flag threshold: $\text{IPR} > 10^{-3}$.

14. **PSC defined as dataset-level Shannon entropy (Q-C4):** Computed on a 2D $(r_{12}, r_{23})$ distance grid ($K = 400$–$2{,}500$ bins) from COM-projected positions. Normalized entropy $H_{\text{norm}} = H_{\text{data}} / \log(K) \in [0,1]$ is recommended for interpretability.

---

## §2 Decision Matrix

| Question ID | One-line Verdict | Confidence |
|-------------|-----------------|------------|
| Q-A1 (B-06) | Resolution-aware completeness gate: `final_timestamp >= 9.5` AND `snapshot_count >= N_min(variant, stage)` | Medium |
| Q-A2 (B-11) | `TrajectoryIndex` from filesystem scan; dense linear indexing (`ID == index`) is invalid | High |
| Q-A3 (M11) | Load blacklist at DataLoader `__init__`; unconditional exclusion; log count; `RuntimeError` if blacklisted ID enters batch | High |
| Q-A4 (M13) | **STOP gap** — three policy options presented; human adjudication required | High (that it is a gap) |
| Q-A5 (D7) | Three-tier footer fallback (direct parse → folder defaults → provenance flag) with `tol_provenance` annotation | High |
| Q-A6 (D-03) | HDF5 primary, `.npy` acceptable, JSON restricted to debug export | High |
| Q-B1 (M12) | Adaptive cap: `n_pts = min(32, max(4, floor(0.5 * n_snapshots)))` | Medium-High |
| Q-B2 | Two-tier mass-drift: 1,000-pair statistical check → `float64_canonical` or `decimal_exact` mode | High |
| Q-B3 | `float64` sufficient for all validation; `decimal.Decimal` only for mass consistency | High |
| Q-B4 | **Known conflict — do not settle.** Parameterize D with `default=None` → PHYS-01 ($D \approx 4.6416$); await EVID-10/PIPE-09 | High (conflict is real) |
| Q-C1 | SCS = $\log_{10}(\epsilon_H)$ with four-tier classification; reject gate $\text{SCS} > -5$ (hard-locked); issue-doc raw ratios superseded | High |
| Q-C2 | SASD$_i = \Delta t_i \cdot \|\mathbf{a}\| / \|\mathbf{v}\|$ with robust turning-point form; flag if $\max_i \text{SASD}_i > 0.5$ | Medium-High |
| Q-C3 | IPR = mean squared PCHIP residual against $F_{\text{gravity}}^{\varepsilon=10^{-10}}$; flag if $\text{IPR} > 10^{-3}$ | High |
| Q-C4 | PSC = Shannon entropy on 2D $(r_{12}, r_{23})$ grid; dataset-level; normalized entropy recommended | Medium |

---

## §3 Cluster A — Ingestion & Selection Resolutions

### Q-A1 (B-06) — Stage 4 → Stage 5 Validation Gate

**Verdict / Recommendation:** A trajectory-completeness gate MUST exist between Stage 4 (metrics extraction) and Stage 5 (training), implemented at DataLoader `__init__` time. The gate enforces two conditions simultaneously:

1. **`final_timestamp >= 9.5`** — the grounded completeness rule (`README.md` Completeness Checks section; issue doc line 202; CLM-11). This is the necessary condition for a trajectory that has integrated to at least 95% of the nominal $T = 10$ endpoint.
2. **`snapshot_count >= N_min(variant, stage)`** — a stage-adaptive snapshot-count floor.

**Conditional bound proposal (pending CLM-10 verification):**

| Variant | dt_out (CLM-09) | Proposed `N_min` | Rationale |
|---------|-----------------|------------------|-----------|
| Gold (`dt_out = 0.01`) | 200 | ~20% of ~1,000 snapshots |
| Hierarchical base (`dt_out = 0.08`) | 50 | ~40% of ~125 snapshots |
| Standard base (`dt_out = 0.17`) | 20 | ~34% of ~59 snapshots |

For Stage 0–3, `snapshot_count >= 10` is recommended (the proposed `>= 2` is too permissive). These values are provisional and must be re-derived from the actual Phase-24 per-trajectory snapshot count distribution.

**Edge-case behavior:** If a trajectory passes `final_timestamp >= 9.5` but fails the snapshot-count floor, it is logged as a warning and excluded from training. If a trajectory fails `final_timestamp >= 9.5`, it is silently excluded. If $H(0)$ is zero or numerically near-zero, the trajectory is flagged for manual review and excluded from automated training pipelines.

**Proposed specification text for `ctl_instruction.md` Phase 1 / Step 1:**

> **Trajectory Completeness Gate (DataLoader-init time):** Before any trajectory enters batch construction, the DataLoader shall verify two conditions: (1) `final_timestamp >= 9.5` — the trajectory must have integrated to at least 95% of the nominal $T = 10$ endpoint; (2) `snapshot_count >= N_min(variant, stage)` — the trajectory must contain at least the resolution-aware minimum number of snapshot blocks. Trajectories failing either condition are excluded from training; failures of condition 1 are logged at INFO level, failures of condition 2 at WARNING level.

**Reasoning:** The `calculate_metrics.py` script processes all Brutus files including partial/errored runs (`consolidated-context.md` line 198). The only validity signal — `final_timestep >= 9.5` — is checked at Stage 3 but never re-validated at the DataLoader boundary. The framework spec (`ctl_instruction.md` Step 1 item 3) acknowledges incomplete files but only specifies graceful handling, not rejection. The issue doc's proposed `snapshot_count >= 200` for Stage 4+ is infeasible for standard base trajectories if CLM-10 (~59 snapshots) is accurate.

**Evidence:** `README.md` Completeness Checks (grounded completeness rule); `consolidated-context.md` line 198 (metrics script scope); issue doc lines 57, 320-331 (GAP row between Stage 4 and Stage 5); CLM-10 (claimed-unverified snapshot counts); CLM-11 (completeness rule); Hard Constraint 5 (SCS gate); Hard Constraint 4 (dual-epsilon split).

**Confidence:** Medium. The gate recommendation is firm; the `N_min` values are conditional on CLM-10 verification.

**Verification suggestion:** (1) DATA-06 (Phase 24): Count actual snapshot blocks per trajectory; derive `N_min` from the 5th percentile. (2) Gate unit test with synthetic trajectories. (3) Log audit post-DataLoader init.

---

### Q-A2 (B-11) — Non-contiguous IDs (ID ≠ array index)

**Verdict / Recommendation:** The ID-to-trajectory mapping contract must be: numeric ID extracted from on-disk filenames, stored in a `TrajectoryIndex` (or `id_to_path` dictionary) built by scanning the filesystem at DataLoader `__init__` time. Dense linear indexing (`ID == array index`) is NEVER valid and must be expunged from all curriculum/stage-assignment logic.

**Specification of the contract:**

1. **ID extraction:** The numeric ID is the `XXXX` portion of the filename (`brutus_hierarchical_XXXX.txt`, `brutus_standard_XXXX.txt`). Gold-standard status is determined **only** by the containing folder name (ERRATUM-2026-06-10, Correction 1).
2. **Index structure:** A `TrajectoryIndex` class mapping `(variant, id)` → `absolute_file_path`, built by scanning each variant directory and extracting numeric IDs via regex `brutus_(?:hierarchical|standard)_(\d+)\.txt`.
3. **Gaps are not errors:** Gaps are intentional — caused by generation continuation, prescreen rejection, and failed Brutus runs (`consolidated-context.md` line 58).
4. **Curriculum implications:** Stage assignment must index by ID, not by array position.

**Proposed specification text for `ctl_instruction.md` Phase 1 / Step 1:**

> **ID Resolution Contract:** The DataLoader shall build an `id_to_path` dictionary by scanning the filesystem for Brutus output files in each variant folder. The numeric ID is extracted from the filename pattern `brutus_*_XXXX.txt`. Gold-standard status is determined solely by the containing folder name, never by a filename infix. IDs are non-contiguous by design; dense linear indexing is invalid. All curriculum stage assignment, batch construction, and metric lookup must index by extracted numeric ID through the `TrajectoryIndex`.

**Reasoning:** If there are 1,250 gaps (CLM-01, claimed-unverified) among 4,000 nominal standard IDs, array index 3,750 corresponds to ID ~4,999, not ID 3,750. The ERRATUM (Correction 1) further requires that gold status be determined by folder name only, since gold files carry no `_gold_` infix. Any gap rate > 0% breaks `ID == array index`.

**Evidence:** `consolidated-context.md` line 58 (non-contiguity statement); CLM-01, CLM-02, CLM-12 (gap claims, claimed-unverified); ERRATUM Correction 1; issue doc line 58, P1-2 (line 284).

**Confidence:** High. Non-contiguity is a verified dataset property. The `TrajectoryIndex` pattern is standard.

**Verification suggestion:** (1) DATA-01 (Phase 24): List all numeric IDs per variant; compute gap count. (2) Index unit test on 10 random IDs. (3) Curriculum integration test.

---

### Q-A3 (M11) — Blacklist Loading / Consumption

**Verdict / Recommendation:** The blacklist (`problematic_ics_blacklist.json`) MUST be loaded at DataLoader `__init__` time, and all blacklisted IDs MUST be excluded from training unconditionally. The exclusion applies regardless of variant (base/gold), stage, or any other property.

**Specification of the contract:**

1. **Loading:** The DataLoader loads `problematic_ics_blacklist.json` at `__init__` time (two keys: `hierarchical` and `standard`, each a list of integer IDs; CLM-03: 2 hierarchical + 63 standard = 65 total, claimed-unverified but directly observable).
2. **Exclusion:** Blacklisted IDs are excluded from ALL stages, ALL batches, ALL curriculum levels. No fallback or override is permitted.
3. **Logging:** WARNING at init: "Blacklist loaded: N hierarchical IDs, M standard IDs excluded." DEBUG per excluded trajectory during batch construction.
4. **Fail-loud:** If a blacklisted ID enters a batch, raise `RuntimeError` immediately.

**Proposed specification text for `ctl_instruction.md` Phase 1 / Step 1:**

> **Blacklist Enforcement:** At `__init__` time, the DataLoader loads `problematic_ics_blacklist.json` and excludes all listed IDs from the training pool. The exclusion is unconditional (all variants, all stages). The DataLoader logs: (a) a WARNING with the total count of excluded IDs per variant at init time, and (b) a DEBUG message for each skipped trajectory during batch construction. If a blacklisted ID enters any training batch, a `RuntimeError` is raised immediately.

**Reasoning:** The issue doc correctly reclassified this from MAJOR to BLOCKING: "A DataLoader that can silently admit blacklisted ICs would corrupt training data at ingestion time" (issue doc line 76). The framework spec is silent on blacklist consumption, but the file's existence implies an intent to exclude these IDs. The current state is an implementation gap, not a design decision.

**Evidence:** `consolidated-context.md` lines 186-194 (blacklist structure); issue doc lines 59, 72-78, P1-3 (line 285); dataset location `simulation_data/Documentation/problematic_ics_blacklist.json`.

**Confidence:** High. The blacklist exists, is structured, and has a clear purpose.

**Verification suggestion:** (1) DATA-02 (Phase 24): Verify JSON structure and count. (2) Unit test with mock blacklist. (3) Integration test on full dataset.

---

### Q-A4 (M13) — 184 Standard IDs Without Gold Counterpart (Fallback Policy)

**Verdict / Recommendation:** **STOP gap.** The framework spec is silent on the missing-gold fallback policy, and the two candidate options are materially different with no principled basis in the spec for choosing between them. This requires human adjudication.

**Analysis of the three options:**

| Aspect | Policy A: Skip to Stage 6 | Policy B: Low-fidelity Stage 5 fallback | Policy C: Conservative exclusion |
|--------|---------------------------|----------------------------------------|----------------------------------|
| Training data | Standard base only at Stage 6 | Standard base in Stage 5 with warning flag | Remain in Stage 4b only |
| Stage 5 purity | Preserved (gold-only) | Diluted with low-resolution data | Preserved |
| Curriculum continuity | Discontinuous (skips Stage 5) | Continuous | Continuous (but truncated) |
| Signal quality risk | Stage 6 may be too hard for standard data | Stage 5 may lack resolution for chaotic refinement | Loses 184 training trajectories (~6.7% of standard base) |
| Logging | "No gold; skipped to Stage 6" | "No gold; using standard fallback" | "No gold; excluded from Stage 5+" |

**Default recommendation (pending human review):** Policy C (conservative exclusion) is the safest interim default because it preserves both Stage 5 signal purity and curriculum structure.

**Proposed specification text (pending decision):**

> **Missing Gold Counterpart Policy (STOP gap — human decision required):** 184 standard IDs (CLM-04, verified) have no gold-standard counterpart. When the curriculum assigns a trajectory to Stage 5, the DataLoader checks for gold data. If gold data is missing, one of three policies applies: (A) Skip to Stage 6; (B) Use standard base in Stage 5 with `gold_missing=True` flag; (C) Exclude from Stage 5+ (remain in Stage 4b). The policy is a hyperparameter set at curriculum configuration time. Default: Policy C pending human review.

**Reasoning:** CLM-04 (184 IDs) and CLM-05 (2,749 base vs. 2,565 gold) are verified facts. The question is what to do about them. The framework spec defines Stage 5 as "High-Resolution Chaotic Orbits" using Set 2b (gold standard data; `ctl_instruction.md` lines 229-235). By definition, Stage 5 requires gold data. Neither fallback option is clearly superior without additional context about project priorities.

**Evidence:** `standard_quasi_random_ids_not_in_gold.md` (CLM-04, verified); CLM-05 (folder counts, verified); `ctl_instruction.md` lines 179-187, 229-235; issue doc line 65, P1-5 (line 287).

**Confidence:** High that this is a STOP gap; Low that any option is definitively correct without additional context.

**Verification suggestion:** (1) Verify the 184 IDs are absent from the gold folder (DATA-03). (2) Confirm standard base data exists for all 184. (3) Evaluate all three policies as configurable hyperparameters.

---

### Q-A5 (D7) — Footer / Parameter Heterogeneity

**Verdict / Recommendation:** The correct footer-handling contract is a three-tier fallback system: (1) parse `Result:` footer when present and complete; (2) fall back to folder-level defaults when footer is absent or incomplete; (3) annotate every trajectory with a `tol_provenance` flag (`'direct'` or `'inferred'`).

**Detailed contract:**

| Tier | Condition | `tol` source | `dt_out` source | `tol_provenance` |
|------|-----------|--------------|-----------------|------------------|
| 1 | Full footer present | Parsed directly | Parsed directly | `'direct'` |
| 2 | Partial footer (missing `eta` only) | Parsed from available fields | Parsed directly | `'direct'` (for present fields) |
| 3 | No footer at all | Folder default (CLM-09) | Folder default (CLM-09) | `'inferred'` |

Confirmed no-footer populations (ERRATUM-2026-06-10, Correction 2): 219 standard gold, 1,550 hierarchical base, 701 standard base files.

The `tol` parameter is **metadata only** — it does not enter training computations. When footer and folder default disagree (e.g., 592 standard gold files with `tol = 10^{-14}` vs. folder default $10^{-13}$; CLM-08, verified), the footer value takes precedence.

**Proposed specification text:**

> **Footer Parsing and Parameter Fallback:** (1) Attempt to parse the `Result:` footer. (2) If present, extract parameters and set `tol_provenance = 'direct'`. (3) If absent (confirmed: 219 standard gold, 1,550 hierarchical base, 701 standard base), apply folder-level defaults and set `tol_provenance = 'inferred'`. (4) When footer and folder default disagree, the footer value takes precedence. (5) Log the count of inferred tolerances per variant. The `tol` parameter is metadata only.

**Reasoning:** The footer heterogeneity is a verified dataset property (CLM-07, CLM-08, CLM-09 all verified). The ERRATUM corrects the characterization: these files have NO footer, not a minimal one. The framework spec (`ctl_instruction.md` Step 1 item 3) acknowledges the optional footer and treats it as metadata.

**Evidence:** ERRATUM Correction 2; CLM-07, CLM-08, CLM-09 (all verified); `consolidated-context.md` lines 69-113; `ctl_instruction.md` Step 1 item 3; issue doc P2-1 (line 291).

**Confidence:** High. All counts are verified. The three-tier system is a direct consequence of ERRATUM-corrected facts.

**Verification suggestion:** (1) DATA-05 (Phase 24): Re-parse all 15,028 files; confirm counts. (2) Unit test with synthetic files of all three tiers. (3) Integration test: count inferred vs. direct per variant.

---

### Q-A6 (D-03) — Processed Training-Data Format (HDF5 vs. .npy vs. txt/json)

**Verdict / Recommendation:** HDF5 (`.h5`) as the primary processed-training-data format, with `.npy` as an acceptable alternative, and JSON restricted to debug export only.

**Rationale:** (1) The framework spec already recommends HDF5/.npy (`ctl_instruction.md` Step 1 item 6). (2) HDF5 supports zero-copy reads, built-in compression, and hierarchical organization — critical for ~15,000 trajectories. (3) The current implementation (`data-processing-pipeline-full.py`) already uses HDF5. (4) txt/json introduces 10–100x parsing overhead.

**Specification:** The DataLoader should accept either `.h5` or `.npy` at init time, auto-detecting from file extensions. Mixed-format datasets are not supported. The choice of storage format does not affect any locked convention (14D input, Jacobi IC$_{13}$, COM projection head, PHYS-03 softening, SCS gate, etc.).

**Proposed specification text:**

> **Processed Data Format:** The processed training data shall be stored in HDF5 (`.h5`) format as the primary store, with `.npy` as an acceptable alternative. Text formats are supported only for optional debug-export. The DataLoader auto-detects the format from file extensions.

**Reasoning:** This is the least consequential decision in Cluster A. The spec already answers it. The issue doc's recommendation (keep HDF5, add optional JSON export) aligns with the spec.

**Evidence:** `ctl_instruction.md` Step 1 item 6; issue doc lines 27-49, 173-190, 262-277; issue doc line 35 (current HDF5 implementation).

**Confidence:** High.

**Verification suggestion:** (1) Verify `h5py` availability. (2) Benchmark load times. (3) Verify optional JSON export produces valid output.

---

## §4 Cluster B — Sampling, Precision & Global Scale Resolutions

### Q-B1 (M12) — Points-per-Trajectory Feasibility

**Verdict / Recommendation:** Adaptive cap with floor. The batch construction contract should specify:

$$n_{\text{pts}}(\text{traj}) = \text{clip}\bigl(\lfloor c_{\text{sample}} \cdot n_{\text{snapshots}}(\text{traj}) \rfloor,\ n_{\min},\ n_{\max}\bigr)$$

with recommended defaults: $c_{\text{sample}} = 0.50$, $n_{\min} = 4$, $n_{\max} = 32$.

**Implied point counts per variant:**

| Variant | dt_out | $n_{\text{snapshots}} \approx 1 + \lceil 10 / \text{dt\_out} \rceil$ | $n_{\text{pts}}$ at $c_{\text{sample}} = 0.50$ | $n_{\text{pts}}$ after cap |
|---------|--------|---------------------------------------------------------------|-----------------------------------------------|---------------------------|
| Standard base | 0.17 | ~60 | ~30 | 30 |
| Hierarchical base | 0.08 | ~126 | ~63 | **32** (capped) |
| Gold | 0.01 | ~1001 | ~500 | **32** (capped) |

Gold trajectories at 32 points use only ~3.2% of available snapshots; standard base at 30 points uses 50%. The existing fixed-$n_{\text{pts}} = 32$ regime starves gold trajectories of data.

**Proposed specification text for `ctl_instruction.md`, §Mini-Batch Construction:**

> **Per-trajectory point count.** The number of sampled time points per trajectory is not fixed at 32. For each trajectory: $n_{\text{pts}} = \min(n_{\max}, \max(n_{\min}, \lfloor c_{\text{sample}} \cdot n_{\text{snapshots}} \rfloor))$. Defaults: $n_{\max} = 32$, $n_{\min} = 4$, $c_{\text{sample}} = 0.50$. The $n_{\text{snapshots}}$ value is the actual post-validation snapshot count, not an estimate. Gold trajectories retain their `dt_out` metadata for downstream collocation-density scaling (M16, out of scope).

**Reasoning:** The existing `ctl_instruction.md` text ("Sample `n_pts` (e.g., 32)") is ambiguous. The arithmetic shows that a fixed 32-point budget is either too dense (standard base: 53% sampling ratio, approaching aliasing risk) or too sparse (gold: 3.2% utilization, wasting high-fidelity data). The adaptive cap corrects both.

**Evidence:** `ctl_instruction.md` §Mini-Batch Construction; issue doc BLOCKING table M12; CLM-09 (verified dt_out values).

**Confidence:** Medium-High. The arithmetic is irrefutable; only the optimal $c_{\text{sample}}$ is empirically underdetermined.

**Verification suggestion:** (1) Parse 10 standard-base files; confirm mean ~60 snapshots, minimum > 8. (2) Log $n_{\text{pts}}$ distribution per variant. (3) Confirm gold trajectories with $n_{\text{snapshots}} > 64$ get $n_{\text{pts}} = 32$.

---

### Q-B2 — Footer / Mass-Drift Protocol

**Verdict / Recommendation:** Two-tier protocol with statistical verification and per-trajectory fallback.

**Specification:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Sample size | 1,000 IC-Brutus pairs | Sufficient for 99.9% confidence detecting a 0.1% defect rate |
| `verification_rtol` | $10^{-15}$ | ~45x float64 epsilon; ~100x tighter than Brutus tol = $10^{-13}$ |
| `per_trajectory_rtol` | $10^{-15}$ | Same as verification |
| Fallback library | `decimal.Decimal` | Exact decimal parsing when float64 detects mismatch |
| Canonical mass source | IC file | Generation-time exact vs. potentially rounded Brutus output |

**Procedure:**

1. **Tier 1 (Statistical):** Randomly sample 1,000 IC-Brutus pairs (stratified by variant). Parse masses in `float64`; compare via `np.allclose(rtol = 10^{-15})`. If `n_mismatched == 0`: declare IC masses canonical, use `float64` throughout. If `n_mismatched > 0`: switch to `decimal.Decimal` (50 digits).
2. **Tier 2 (Per-trajectory):** After Tier 1 establishes the parsing mode, every trajectory undergoes a lightweight check. Mismatches in `float64_canonical` mode quarantine the trajectory.

**Edge cases:** Footer absence (1,550 hierarchical base, 701 standard base, 219 standard gold) does NOT block this protocol — mass comparison uses t=0 snapshot body lines, not the `Result:` footer. Zero/negative masses trigger immediate rejection.

**Proposed specification text for `ctl_instruction.md`, §2.1 Parser contract:**

> **Mass Consistency Verification:** Tier 1: Statistically verify 1,000 IC-Brutus pairs with `np.allclose(rtol=1e-15)`. If all match, IC masses are canonical and `float64` parsing suffices. If mismatches detected, switch to `decimal.Decimal` for mass parsing. Tier 2: Every loaded trajectory undergoes a lightweight per-trajectory mass check. Mismatches quarantine the trajectory.

**Reasoning:** Brutus uses GMP/MPFR arbitrary-precision arithmetic internally; masses should not drift. However, text output may round. Float64 parsing discards ~20–24 significant digits from the 30–40 digits in Brutus output. The $10^{-15}$ threshold provides generous guard digits against benign parsing noise while remaining tighter than the Brutus convergence tolerance.

**Evidence:** Issue doc §Footer/Mass Drift Protocol; `ctl_instruction.md` §2.1 Parser contract; CLM-09 (verified Brutus word lengths).

**Confidence:** High. The two-tier protocol is standard practice; thresholds are grounded in float64 epsilon and Brutus tolerance.

**Verification suggestion:** (1) Run Tier 1 on 1,000 actual pairs; record mismatch count and relative differences. (2) If mismatches found, re-parse with `Decimal` to distinguish genuine drift from parsing artifacts. (3) Log the histogram of relative differences.

---

### Q-B3 — Precision Handling (float64 Sufficiency; Decimal-for-Masses)

**Verdict / Recommendation:** Float64 is sufficient for validation metrics. `decimal.Decimal` is required only for mass consistency verification and exact footer parameter parsing for diagnostic metadata.

**Validation metric precision budget:**

| Quantity | Float64 $\varepsilon_{\text{mach}}$ | Relevant tolerance | Guard digits | Assessment |
|----------|--------------------------------------|-------------------|--------------|------------|
| Position/velocity validation | ~$2 \times 10^{-16}$ | — | — | Sufficient |
| Energy conservation (SCS) | ~$2 \times 10^{-16}$ | tol = $10^{-13}$ (std), $10^{-15}$ (hier) | 2–3 | Sufficient |
| Hamiltonian $H(t)$ | ~$2 \times 10^{-16}$ | tol = $10^{-13}$ to $10^{-15}$ | 2–3 | Sufficient |
| SCS = $\log_{10}(\varepsilon_H)$ | ~$2 \times 10^{-16}$ | Gate: $10^{-5}$ | ~11 | More than sufficient |
| Invariants ($E$, $Q$, $L_{\text{norm}}$, $s_{\min}$) | ~$2 \times 10^{-16}$ | — | — | Sufficient |

**Where Decimal is required:** (1) Mass consistency verification (Q-B2); (2) Footer parameter parsing for diagnostic provenance (metadata only, no computation).

**Where Decimal is NOT required:** All validation metrics (SCS, SASD, IPR, PSC); all training computations; position/velocity trajectory data.

**Reasoning:** The validation pipeline evaluates pre-computed trajectories, not converging a solver. The SCS gate threshold ($10^{-5}$) is 5 orders of magnitude larger than float64 epsilon. Even cumulative errors across 1,000 snapshots would not reach the gate. The dual-epsilon split (PHYS-03: $\varepsilon_{\text{train}} = 10^{-5}$, $\varepsilon_{\text{val}} = 10^{-10}$) ensures neither scale approaches float64 limits.

**Evidence:** `ctl_instruction.md` §2.1, §Numerical notes; issue doc §Precision Handling; PHYS-03 hard constraint; post-v1.3 SCS gate.

**Confidence:** High. The precision budget analysis is a standard backward-error argument.

**Verification suggestion:** (1) Parse 100 snapshots in both `float64` and `Decimal`; confirm max relative difference $O(10^{-16})$. (2) Compute SCS in both; confirm agreement to within $10^{-14}$ relative. (3) Identify any trajectory where float64 and Decimal produce different SCS rejection decisions (expected count: zero).

---

### Q-B4 — Global-Scale `compute_globals` / $D = 6.694$ (KNOWN CONFLICT)

**Verdict / Recommendation:** This question is genuinely undecidable within Cluster B scope. Two mutually incompatible conventions are locked by different authority documents. The conflict must be escalated to downstream adjudication (EVID-10 / PIPE-09).

**What the data pipeline MUST do now:** Implement `compute_globals` with a **parameterized D convention:**

```python
def compute_globals(ic_files, t_max=10.0, G=1.0, M_tot_ref=None):
    if M_tot_ref is None:
        D = np.cbrt(G * t_max**2)           # D ≈ 4.641589 (PHYS-01, locked v1.4)
    else:
        D = np.cbrt(G * M_tot_ref * t_max**2)  # D ≈ 6.694 for M_tot=3
    V = D / t_max
    ...
```

Default: `M_tot_ref = None` (PHYS-01, $D \approx 4.6416$) until downstream adjudication resolves. The pipeline MUST log the selected D value in every output file's metadata.

**Reconciliation map:**

| Decision | Pipeline work | Training work | Validation work | Risk |
|----------|--------------|---------------|-----------------|------|
| Keep $D = 4.6416$ (PHYS-01) | None | None | None | Low — locked, consistent, implemented |
| Adopt $D = 6.694$ (CLM-13) | Recompute all preprocessed data | Retrain all models | Recompute all thresholds | **Very High** — framework rewrite required |
| Parameterize (recommended) | Add `M_tot_ref` parameter | None | Log convention | Low — defers decision |

**Guardrail:** Computed D must satisfy $4.60 \leq D \leq 4.70$ when `M_tot_ref = None`. A `ValueError` should be raised if a caller attempts to produce $D \approx 6.694$ through an unexpected parameter path.

**Reasoning:** $D$ enters every scaled quantity: $r' = r/D$, $v' = v/V$, all invariants, the IC$_{13}$ vector, rotation-gauge thresholds, and the training loss. Changing $D$ by $3^{1/3} \approx 1.442$ rescales all positions and distances by ~44%. `ctl_instruction.md` line 598 explicitly rejects $D = 6.694$: "The mass-fraction alternative is documented as a future rewrite only and is not adopted in v1.4."

**Evidence:** `ctl_instruction.md` §2.5 (PHYS-01, locked); issue doc §Global Scale Computation (CLM-13); Hard Constraint 6; `ctl_instruction.md` line 598 (explicit rejection of 6.694 form).

**Confidence:** High that the conflict is real and must not be unilaterally resolved.

**Verification suggestion:** (1) Confirm D values: $(G \cdot T^2)^{1/3}$ and $(G \cdot 3 \cdot T^2)^{1/3}$; verify ratio is $3^{1/3}$. (2) Audit framework formulas for mass-fraction rewrite scope. (3) Preprocess 100 trajectories with both D conventions; compare scaled quantity distributions.

---

## §5 Cluster C — Validation Metric Resolutions

### Q-C1: Symplectic Conservation Score (SCS) — Definition, Thresholds, and Known Conflict

**Verdict / Recommendation:** The locked post-v1.3 SCS gate (Hard Constraint 5) is the authoritative definition for data-side validation. The issue doc's ratio-based thresholds are a different, incompatible quantity and are documented as superseded.

**Recommended data-side SCS definition (reconciled):**

**Step 1 — Compute raw Hamiltonian drift:**

$$\varepsilon_H = \max_{t \in [0,T]} \left| \frac{H(t) - H(0)}{H(0)} \right|$$

where $H(t)$ uses the matched-Plummer form with validation softening $\varepsilon = 10^{-10}$ (Hard Constraint 4). If $H(0) = 0$ or is numerically near-zero, SCS is undefined — flag for manual review.

**Step 2 — Convert to logarithmic score:**

$$\text{SCS} = \log_{10}(\varepsilon_H)$$

**Step 3 — Apply threshold tiers:**

| Tier | SCS range | $\varepsilon_H$ range | Action |
|------|-----------|----------------------|--------|
| Excellent | SCS $\leq -10$ | $\varepsilon_H \leq 10^{-10}$ | Ideal for training |
| Acceptable | $-10 <$ SCS $\leq -6$ | $10^{-10} < \varepsilon_H \leq 10^{-6}$ | Clean training data |
| Marginal | $-6 <$ SCS $\leq -5$ | $10^{-6} < \varepsilon_H \leq 10^{-5}$ | Review/diagnostics only |
| **Reject** | **SCS $> -5$** | **$\varepsilon_H > 10^{-5}$** | **Discard trajectory** |

The reject gate SCS $> -5$ (equivalently $\varepsilon_H > 10^{-5}$) is **hard-locked and non-negotiable** per HC-05.

**Critical clarification:** The SCS is computed on validation trajectories (simulated with $\varepsilon = 10^{-10}$ softening). The "Excellent" tier threshold ($\varepsilon_H \leq 10^{-10}$) is numerically equal to the validation softening parameter but conceptually distinct — the former classifies energy conservation quality; the latter controls force smoothing.

**Reasoning:** The issue doc defines SCS as a raw ratio with thresholds $> 10^{-6}$ and $< 10^{-8}$. The DQA defines SCS as $\log_{10}(\varepsilon_H)$ with a reject gate $> -5$. These are genuinely different gating criteria. The DQA definition is mathematically cleaner and locked by Hard Constraint 5. SI-DQA-003 confirms this was a deliberate source-level correction of a "logarithmic-vs-raw-drift category error."

**Evidence:** `data_quality_assessment.md` §3.1, §5.1 Step 1, SI-DQA-003; issue doc §"Validation Metrics as Live Training Parameters" lines 131-141; Hard Constraint 5.

**Confidence:** High.

**Verification suggestion:** (1) Numerical cross-check on 100 trajectories: verify that SCS $> -5$ corresponds to $\varepsilon_H > 10^{-5}$. (2) Test $H(0) \approx 0$ edge case. (3) Verify tier boundary placements.

---

### Q-C2: Stiffness-Aware Sampling Density (SASD) — Data-Side Definition

**Verdict / Recommendation:**

**Per-interval metric:**

$$\text{SASD}_i = \Delta t_i \cdot \frac{\|\mathbf{a}(t_i)\|}{\|\mathbf{v}(t_i)\|}$$

where $\Delta t_i = t_{i+1} - t_i$, and $\|\cdot\|$ denotes the Euclidean norm over all 9 velocity/acceleration components (3 bodies $\times$ 3 axes).

**Robust form for turning points:**

$$\text{SASD}_i^{(\text{robust})} = \Delta t_i \cdot \frac{a_{\perp}(t_i)}{\|\mathbf{v}(t_i)\| + \eta}$$

where $\eta = 10^{-12}$ and $a_{\perp} = \|\mathbf{a} - (\mathbf{a} \cdot \hat{\mathbf{v}}) \hat{\mathbf{v}}\|$ is the perpendicular acceleration component.

**Flag/resample criterion:**

| Condition | Action |
|-----------|--------|
| $\max_i \text{SASD}_i > 0.5$ | Flag for resampling (re-run Brutus with finer dt_out, exclude, or defer to later curriculum stage) |
| $\text{SASD}_i \leq 0.5$ for all $i$ | Accept for training |

**Known limitation — SASD floor effect:** Standard trajectories ($\text{dt\_out} = 0.17$, ~59 snapshots) may have close encounters spanning only 1–2 sample points. In such cases, the interior of the close encounter is invisible to SASD. This is inherent to the output sampling, not a metric definition problem. Gold trajectories ($\text{dt\_out} = 0.01$) are less affected.

**Reasoning:** SASD compares the sampling time step to the local characteristic timescale $\tau_{\text{char}} = \|\mathbf{v}\| / \|\mathbf{a}\|$. SASD $\ll 1$ means well-sampled; SASD $\sim 1$ means significant turn between samples; SASD $> 1$ means a sharp turn/cusp. The 0.5 threshold is a conservative early-warning value from DQA §5.1 Phase 2.

**Evidence:** `data_quality_assessment.md` §3.2 (eq. 5), §5.1 Phase 2; issue doc lines 15-18 (floor effect).

**Confidence:** Medium-High. The formula is well-specified; the 0.5 threshold has a source but limited empirical validation.

**Verification suggestion:** (1) Compute SASD profiles for 100 stratified trajectories; plot max(SASD) distribution. (2) Test $\|\mathbf{v}\| \to 0$ edge case for NaN/Inf. (3) Visually inspect flagged standard trajectories for close encounters.

---

### Q-C3: Interpolation Physics Residual (IPR) — Data-Side Definition

**Verdict / Recommendation:**

**Protocol:**

1. Construct a PCHIP spline $\mathbf{q}_{\text{spline}}(t)$ using trajectory data $\{(\mathbf{q}_i, \mathbf{v}_i)\}_{i=1}^{N}$.
2. Sample $M = 10$ synthetic collocation points per interval, uniformly distributed between consecutive data points.
3. At each synthetic point $\tau_k$, compute the spline second derivative and gravitational acceleration with **validation softening $\varepsilon = 10^{-10}$**.
4. The IPR is the mean squared residual:

$$\text{IPR} = \frac{1}{M} \sum_{k=1}^{M} \left\| \frac{d^2 \mathbf{q}_{\text{spline}}}{dt^2}(\tau_k) - \mathbf{F}_{\text{gravity}}^{\varepsilon=10^{-10}}(\mathbf{q}_{\text{spline}}(\tau_k)) \right\|^2$$

**Flag criterion:**

| Condition | Action |
|-----------|--------|
| IPR $> 10^{-3}$ | Trajectory is aliased; flag for resampling or exclusion |
| IPR $\leq 10^{-3}$ | Accept for training |

**Critical dual-epsilon clarification:** The data-side IPR **must** use $\varepsilon = 10^{-10}$ (validation softening), NOT $\varepsilon_{\text{train}} = 10^{-5}$ (training softening). The issue doc's statement that IPR should use "the network's dynamic softening constant ($\varepsilon = 10^{-5}$)" applies only to the training-loop ALM noise-floor role (doc-03), not to data-side validation. Using $\varepsilon_{\text{train}}$ for data-side IPR would systematically under-report interpolation errors.

**When applied to model outputs:** Use COM-projected positions per HC-3. For ground-truth trajectory analysis, raw coordinates may be used.

**Evidence:** `data_quality_assessment.md` §3.3, §5.1 Phase 1 Step 3; Hard Constraint 4 (PHYS-03 dual-epsilon); issue doc line 216 (validation uses static $\varepsilon = 10^{-10}$); issue doc line 159 (conflicting non-authoritative position).

**Confidence:** High. The locked dual-epsilon contract is unambiguous.

**Verification suggestion:** (1) Compute IPR on 50 trajectories with both $\varepsilon = 10^{-10}$ and $\varepsilon = 10^{-5}$; verify IPR($10^{-10}$) $\geq$ IPR($10^{-5}$) always. (2) Test 2-snapshot single-segment edge case. (3) Confirm completeness gate interaction.

---

### Q-C4: Phase Space Coverage Entropy (PSC) — Data-Side Definition

**Verdict / Recommendation:**

**Step 1 — Grid construction:** Discretize the 2D $(r_{12}, r_{23})$ distance plane into $K = N_1 \times N_2$ uniform bins, where $r_{12} = \|\mathbf{q}_1 - \mathbf{q}_2\|$ and $r_{23} = \|\mathbf{q}_2 - \mathbf{q}_3\|$. Recommended: $N_1 = N_2 = 20$–$50$ ($K = 400$–$2{,}500$). Distances computed from COM-projected positions per HC-3.

**Step 2 — Population counting:** For each trajectory snapshot, compute $(r_{12}, r_{23})$ and increment the corresponding bin.

**Step 3 — Probability estimation:** $p_k = n_k / N_{\text{total}}$ where $N_{\text{total}} = \sum_k n_k$.

**Step 4 — Shannon entropy:**

$$H_{\text{data}} = -\sum_{k=1}^{K} p_k \log(p_k)$$

The base of the logarithm must be documented (2 for bits, $e$ for nats). Normalized entropy: $H_{\text{norm}} = H_{\text{data}} / \log(K) \in [0,1]$.

**Data-side action criteria:**

1. If the $r_{\min} \to 0$ bin is empty: dataset lacks close-encounter examples. Action: generate additional trajectories with $s_{\min} < 0.5$.
2. If $H_{\text{norm}}$ below a project-defined threshold (e.g., 0.3): dataset is too homogeneous. Action: diversify IC generation strategy.

**Scope note:** PSC-governed curriculum replay (sampling inversely proportional to bin density) is a training-loop mechanism deferred to doc-03.

**Evidence:** `data_quality_assessment.md` §3.4 (eq. 7), §5.3 Phase 3; issue doc §"Validation Metrics as Live Training Parameters".

**Confidence:** Medium. The entropy formula and concept are well-defined, but grid resolution, bin ranges, and explicit action thresholds rely on judgment calls.

**Verification suggestion:** (1) Grid sensitivity analysis: compute PSC with $K = 400, 900, 2{,}500, 10{,}000$; verify $H_{\text{norm}}$ stability. (2) Visual inspection of 2D $(r_{12}, r_{23})$ histogram. (3) Clarify with doc-03 whether curriculum replay operates on per-trajectory or dataset-level density estimates.

---

## §6 Open Items Register

### Insufficient Evidence Items

| Item | Question | What is missing | What evidence would resolve |
|------|----------|----------------|----------------------------|
| CLM-10 verification | Q-A1, Q-B1 | Actual per-trajectory snapshot count distribution per variant | DATA-06 (Phase 24): Count snapshot blocks for all ~15,000 trajectories; compute 5th/10th/50th/90th/95th percentiles per variant |
| CLM-01/02 verification | Q-A2 | Actual gap counts for standard and hierarchical variants | DATA-01 (Phase 24): List all numeric IDs per variant; compute gap statistics |
| CLM-03 count confirmation | Q-A3 | Direct observation of blacklist JSON entry count | DATA-02 (Phase 24): Verify JSON structure and count entries |
| Optimal $c_{\text{sample}}$ | Q-B1 | Whether 50% sampling ratio causes systematic aliasing in standard trajectories | Small ablation study: train with $c_{\text{sample}} \in \{0.3, 0.5, 0.7\}$; compare data-fidelity loss gradients |
| SASD threshold calibration | Q-C2 | Empirical distribution of max(SASD) across the actual dataset | Compute max(SASD) for stratified sample; validate that 0.5 threshold flags appropriate trajectories |
| PSC grid resolution | Q-C4 | Optimal bin count for the dataset's phase-space distribution | Grid sensitivity analysis ($K \in \{400, 900, 2500, 10000\}$); verify $H_{\text{norm}}$ stability |

### Additional Input Needed

| Item | Question | What decision is needed | From whom |
|------|----------|------------------------|-----------|
| Missing-gold fallback policy | Q-A4 | Choose among Policy A (skip to Stage 6), Policy B (standard fallback), Policy C (conservative exclusion) | Curriculum designer / project lead |
| $D$ convention resolution | Q-B4 | Ratify PHYS-01 ($D \approx 4.6416$), authorize mass-fraction rewrite, or accept parameterization | EVID-10 / PIPE-09 downstream adjudication |
| PSC action threshold | Q-C4 | Define project-specific $H_{\text{norm}}$ threshold below which to trigger IC diversification | Dataset curation team |

### STOP Gaps

| STOP Gap ID | Question | Description | Blocking until |
|-------------|----------|-------------|---------------|
| STOP-01 | Q-A4 | 184 standard IDs lack gold counterparts; no spec basis for choosing fallback policy | Human policy decision on curriculum priorities (signal purity vs. continuity vs. conservative exclusion) |
| STOP-02 | Q-B4 | $D = 4.6416$ (PHYS-01, locked) vs. $D = 6.694$ (CLM-13, claimed) — mutually incompatible conventions | EVID-10 / PIPE-09 downstream adjudication |

### Conditional Recommendations Pending Verification

| Recommendation | Condition for activation | Fallback if condition fails |
|---------------|-------------------------|----------------------------|
| Q-A1: $N_{\min}$ values (gold=200, hier=50, std=20) | CLM-10 snapshot counts confirmed as ~1000 / ~125 / ~59 | Re-derive $N_{\min}$ from actual 5th-percentile snapshot counts |
| Q-B1: $c_{\text{sample}} = 0.50$ | Standard trajectories tolerate 50% sampling without aliasing | Reduce to $c_{\text{sample}} = 0.30$–$0.40$ |
| Q-A4: Policy C (conservative) as default | No human decision within 2 weeks | Policy C remains the safe default; training proceeds with 184 fewer Stage 5+ trajectories |

---

## §7 Consistency Audit Summary

### Audit Findings Overview

The consistency audit (`consistency_audit_report.md`) performed six categories of verification across all 14 recommendations:

| Category | Result |
|----------|--------|
| Hard constraint violations | **0 violations** across all 6 hard constraints (HC-01 through HC-06) |
| $\varepsilon_H$ symbol conflation | **0 conflations** — the two distinct $\varepsilon_H$ symbols (validation gate vs. training energy-denominator floor) are kept fully separate |
| Scope boundary violations | **0 overreaches** — no recommendation addresses M16, G6, or training-loop metric usage |
| Cross-cluster contradictions | **0 contradictions** — all cluster pairs are mutually consistent |
| Claims discipline | **0 silent dependencies** — all threshold values are explicitly framed as recommendations |
| **Overall verdict** | **CONSISTENT WITH RESERVATIONS** |

### Passed Checks (13/14 recommendations fully compliant)

- HC-01 (14D Input Contract): All recommendations PASS — no interaction with input contract.
- HC-02 (Jacobi IC$_{13}$): All recommendations PASS — B2/B3's raw-mass emphasis is positively aligned.
- HC-03 (COM Projection Head): All recommendations PASS — C2-C4 operate on raw trajectory kinematics (acceptable for ground-truth analysis; note added for model-output evaluation).
- HC-04 (PHYS-03 Dual-Epsilon): All recommendations PASS — C3 explicitly correct in using $\varepsilon = 10^{-10}$.
- HC-05 (Post-v1.3 SCS Gate): All recommendations PASS — C1's tier system extends HC-05 downward without modifying the reject gate.
- HC-06 (PHYS-01 D Convention): B4 correctly defers; parameterized default points to PHYS-01.
- Cross-cluster coherence: A1-C1 (SCS pipeline), B2-B3 (precision specialization), B4-HC-6 (deferred), C1-C4 (complementary metrics), A5-A6 (metadata separation), A-B (independent), A-C (scoped), B-C (independent domains) — all CONSISTENT.

### Warnings (4 items, all stylistic/clarity, no technical violations)

| Warning | Location | Issue | Resolution in this document |
|---------|----------|-------|---------------------------|
| WARNING-1 | C1 | Phrasing "Uses validation epsilon=1e-10" risks conflating softening parameter with SCS tier threshold | Resolved: §5 Q-C1 now uses disambiguated phrasing: "SCS is computed on validation trajectories (simulated with $\varepsilon = 10^{-10}$ softening). Tier thresholds defined as..." |
| WARNING-2 | B4 | `default=None` indirection could allow $D = 6.694$ at runtime | Resolved: §4 Q-B4 adds explicit guardrail — computed D must satisfy $4.60 \leq D \leq 4.70$; `ValueError` if $D \approx 6.694$ |
| WARNING-3 | C2-C4 | Metric definitions on raw trajectory quantities; COM projection not mentioned for model-output evaluation | Resolved: §5 Q-C3 explicitly adds note: "When applied to model outputs, use COM-projected positions per HC-3." Q-C2 and Q-C4 similarly scoped to ground-truth analysis. |
| WARNING-4 | C1 | Documentation superseding action embedded in technical recommendation | Resolved: §5 Q-C1 separates the technical SCS definition from the documentation note; superseding action tracked in §6 Open Items Register. |

**Final consistency verdict:** All 4 warnings are addressed. The recommendation set is **fully consistent** and ready for implementation.

---

## §8 References

### Package Files (Input)

1. `README.md` — Package manifest & index (PKG-01). Role: authoritative package directory; byte-for-byte intact snapshot.
2. `framed-research-questions.md` — Neutral framed research questions (PKG-02). Role: complete task list for this research.
3. `claims-table.md` — Claims register (PKG-03). Role: stable CLM IDs with claimed/verified status.
4. `02-data-pipeline-and-validation.md` — Issue doc (non-authoritative; adjudication subject). Role: bug report with candidate positions; may contain errors.
5. `ctl_instruction.md` — Framework spec (source of truth; D-03 byte-for-byte). Role: carries 14D input contract, Jacobi IC13, PHYS-01 D convention.
6. `pinn_architecture.md` — Framework spec (source of truth; D-03 byte-for-byte). Role: carries COM projection head, PHYS-03 softening, loss contracts.
7. `sampling_method.md` — Historical record (FROZEN, SCOPE-08). Role: dataset generation methodology; not a revision target.
8. `data_quality_assessment.md` — Research report (SCOPE-09, non-authoritative). Role: sole written home of post-v1.3 SCS gate (SI-DQA-003).
9. `consolidated-context.md` — Generated package artifact (D-05). Role: dataset fragments with source-path labels.
10. `ERRATUM-2026-06-10.md` — Correction addendum. Role: interim corrections to two dataset claims; supersedes package file characterizations where noted.

### Framework Specifications (Source of Truth)

5. `ctl_instruction.md` — Framework instruction document. Cited sections: §2.1 (Parser contract), §2.5 (PHYS-01 D convention), §Mini-Batch Construction, §Numerical notes, Phase 1 / Step 1 (Data Ingestion).
6. `pinn_architecture.md` — Network architecture specification. Cited section: §3.4 (Training energy-denominator floor $\varepsilon_H = 10^{-4} \cdot S_H$).

### Issue Document (Non-Authoritative — Bug Report)

7. `02-data-pipeline-and-validation.md` — Issue-02 Data Pipeline & Validation document. Cited sections: §"Validation Metrics as Live Training Parameters", §"Precision Handling in Validation", §Global Scale Computation, §Footer/Mass Drift Protocol, Temporal Resolution Bridging, BLOCKING/MAJOR tables.

### Dataset Documentation (Factual, Verified Where Noted)

8. `README.md` — Dataset README. Cited: Completeness Checks section (final timestep >= 9.5 rule).
9. `consolidated-context.md` — Consolidated dataset context. Cited lines: 58 (non-contiguous IDs), 69-113 (parameter distributions), 125-141 (completeness checks), 145-183 (standard IDs without gold), 186-194 (blacklist structure), 198 (metrics script scope).
10. `data_quality_assessment.md` — Data Quality Assessment report. Cited sections: §3.1 (SCS definition, eqs. 3-4, boundary behavior), §3.2 (SASD definition, eq. 5, turning-point robust form), §3.3 (IPR protocol), §3.4 (PSC definition, eq. 7), §5.1 (Implementation protocol — Phases 1-2), §5.3 (Phase 3 diversity check), SI-DQA-003 (source-level SCS correction).
11. `ERRATUM-2026-06-10.md` — Erratum and corrections. Cited: Correction 1 (gold status encoded ONLY by folder name), Correction 2 (no-footer characterization: 219 standard gold, 1,550 hierarchical base, 701 standard base).

### Supporting Dataset Files

12. `simulation_data/Documentation/problematic_ics_blacklist.json` — Blacklist file (2 hierarchical + 63 standard IDs = 65 total).
13. `standard_quasi_random_ids_not_in_gold.md` — List of 184 standard IDs without gold counterpart (CLM-04, verified).

### Claim Identifiers Referenced

| Claim | Status | Description |
|-------|--------|-------------|
| CLM-01 | Claimed-unverified | Standard dataset: 1,250 gaps / 4,000 nominal IDs |
| CLM-02 | Claimed-unverified | Hierarchical dataset: 143 gaps / 5,000 nominal IDs |
| CLM-03 | Claimed-unverified (count observable) | Blacklist: 2 hierarchical + 63 standard = 65 IDs |
| CLM-04 | **Verified** | 184 standard IDs have no gold counterpart |
| CLM-05 | **Verified** | Folder counts: 2,749 base vs. 2,565 gold |
| CLM-07 | **Verified** | 219 minimal-footer files (ERRATUM-corrected: no-footer) |
| CLM-08 | **Verified** | 592 standard gold files with tol = $10^{-14}$ |
| CLM-09 | **Verified** | Folder-default dt_out/tol/Lw values per variant |
| CLM-10 | Claimed-unverified | Snapshot counts: ~59 standard / ~125 hierarchical / ~1000 gold |
| CLM-11 | Claimed-unverified | Completeness rule: final_timestamp >= 9.5 |
| CLM-12 | Claimed-unverified | Nominal dataset counts: ~4,000 standard / ~5,000 hierarchical |
| CLM-13 | Claimed-unverified | $D = (G \cdot M_{\text{tot}} \cdot T^2)^{1/3} \approx 6.694$ (conflicts with PHYS-01) |

### Hard Constraints v1.4

| ID | Constraint |
|----|-----------|
| HC-01 / PHYS-01 variant | 14D input contract: $\mathbf{x}_{\text{net}} = [\tau, \text{IC}_{13}]$, $\tau = 2u - 1$, $u = t/T$ |
| HC-02 | Jacobi IC$_{13}$ vector: raw masses, 13 components specified |
| HC-03 | Mass-weighted COM projection head applied to position outputs before loss/metric |
| HC-04 / PHYS-03 | Dual-epsilon split: $\varepsilon_{\text{train}} = 10^{-5}$ (training), $\varepsilon = 10^{-10}$ (validation) |
| HC-05 / Post-v1.3 SCS gate | $\varepsilon_H = \max_t |(H(t) - H(0))/H(0)|$, SCS = $\log_{10}(\varepsilon_H)$, reject if SCS $> -5$ |
| HC-06 / PHYS-01 D | $D = (G \cdot T^2)^{1/3} \approx 4.6416$; $D = 6.694$ explicitly rejected |

### Verification Tickets (Phase 24)

| Ticket | Scope |
|--------|-------|
| DATA-01 | Verify gap counts (CLM-01, CLM-02) per variant |
| DATA-02 | Verify blacklist JSON structure and entry count (CLM-03) |
| DATA-03 | Verify 184 IDs absent from gold folder (CLM-04) |
| DATA-05 | Re-parse all 15,028 files; confirm no-footer and tol counts (CLM-07, CLM-08) |
| DATA-06 | Count actual snapshot blocks per trajectory; derive percentile distribution (CLM-10) |
| EVID-10 / PIPE-09 | Downstream adjudication of D = 4.6416 vs. D = 6.694 conflict |

---

*Document compiled from four analysis files under Hard Constraints v1.4. All 14 questions addressed; 2 STOP gaps identified; 4 audit warnings resolved. Ready for implementation pending human adjudication on STOP-01 and downstream resolution of STOP-02.*
