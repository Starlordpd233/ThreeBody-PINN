# Phase 9 Re-Verification Report (Independent)

**Re-verification date:** 2026-04-29
**Agent:** claude-opus-4-7
**Scope:** Independently re-verify Phase 9's issues-directory consolidation against the seven archived originals, the three thematic destination docs, and the canonical CTL/PINN LaTeX sources, without trusting the prior `PASS AFTER REMEDIATION` verdict in `09-VERIFICATION-REPORT.md`.
**Method:** Per-original sequential verification (audit → causal blueprint → validation protocol → review.md → stage-assignment → pipeline note → next steps), plus independent recomputation of every numerical claim and a full structural pass over the destination docs and `MIGRATION.md`.
**Source files used:** All 7 archives, the 3 destinations, `MIGRATION.md`, `README.md`, `09-CONTEXT.md`, the existing `09-VERIFICATION-REPORT.md` (read-only), `pinn_instruction/original_latex/ctl-instruction/sections/04_phase1_data_prep.tex`, `pinn_instruction/original_latex/pinn-architecture/sections/sqr_skipresnet_siren_backbone.tex`, `pinn_instruction/original_latex/pinn-architecture/sections/input_vector_inactive.tex`, `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`.

---

## Summary

- **Overall verdict:** **PASS WITH MINOR CONCERNS**
- **Issue counts (this re-verification):** 0 critical, 4 moderate, 5 minor
- **Headline result:** The consolidation faithfully preserves the substantive content of all seven archived originals across the three destination docs. All math claims that I could re-derive match the destinations' stated values, with one exception: the `## Quantitative Impact of D Formula Error` table in `01` carries forward labels that are inconsistent with the underlying scaling formulas (see Math Verification §Q-IMPACT). The structural claims (DECISION-NEEDED distribution, verbatim §6, audit-§5-as-synthesis, no-86-mapped-sections claim) all hold up under independent inspection.
- **What changed vs the prior `PASS AFTER REMEDIATION`:** The prior remediation pass correctly addressed every issue it claimed to address. This independent re-verification additionally surfaces the Quantitative Impact math discrepancy, the misleading section naming for `02 §Data Validation Protocol — 6-Gap Analysis`, and a few smaller documentation gaps that were not part of the prior remediation scope.

---

## Per-Original Verification

Each original was read in full, then mapped to its destination sections via `MIGRATION.md`, then verified for completeness, accuracy, attribution, and downstream consistency. Cumulative evidence carried forward across originals.

### 1. `three_body_pinn_pre-implementation_audit_2026-04-27.md` (38 KB, structural spine)

- **Sections checked:** Executive Summary, §1 Critical Issues B-01..B-11, §2 Major Inconsistencies M1..M16, §3 Design Ambiguities D1..D10, §4 Author-Flagged Uncertainties (28-item summary), §5 Corrected Input Vector Spec, §6 Unified Batch Construction, §7 Implementation Checklist P0..P4, §8 Cross-Issue Interaction Matrix, §9 Quantitative Impact Summary.
- **Findings verified:** All 11 critical blockers, 16 major inconsistencies, and 10 design ambiguities are present in the destinations and routed correctly:
  - 01: B-01..B-05, B-09, B-10, M1-M5, M8-M10, D1-D4, D6, D8-D10
  - 02: B-06, B-11, M11/M12 (re-classified BLOCKING via explicit `Severity Reclassification Ledger`), M13, D7
  - 03: B-07, B-08, M6-M7, M14-M16, D5
- **Verbatim §6:** Verified by `diff` between archive lines 290–410 and `03` lines 555–679. Only differences are trailing-whitespace and blank-line normalization; no semantic divergence. Section 6.1, 6.2 (full pseudo-code), 6.3 (stage transition criteria + threshold table), and 6.4 (`get_lambda_E` function) all match exactly.
- **§5 reconciliation:** Audit §5 was Option A (trigonometric encoding). The destination's `01 §Recommended Input Vector Specification` is Option B (shape invariants + direction cosines), labeled `(OPTION B — PROVISIONAL)`. The audit's Option A is preserved under `01 §Considered Alternatives`. `MIGRATION.md` correctly says "Synthesized/reconciled. Audit Option A trig encoding is preserved as a considered alternative; the consolidated recommended spec uses Option B shape invariants + direction cosines. Not copied verbatim." This matches what is on disk.
- **§9 quantitative impact:** Only the D-formula portion is migrated to `01 §Quantitative Impact of D Formula Error`. The other §9 rows (epsilon, COM, 14D, trig_vec, replay/lookahead, separate collocation, SIREN, stage criteria) are captured in the corresponding finding sections rather than as a single table. Acceptable, but see Unresolved §1 below.
- **Notes / deviations:**
  1. **B-09 resolution changed from audit's recommendation.** The audit recommended unifying softening at `epsilon = 1e-8` (compromise between CTL's 1e-10 and PINN's 1e-5). The destination adopts the **dual-context strategy** (`eps=1e-10` static / `eps_soft=1e-5` dynamic) from the Causal Training Mismatch blueprint instead. This is mathematically and operationally stronger, but the audit's specific 1e-8 recommendation is not preserved under "Considered Alternatives" anywhere in the destinations.
  2. **B-02 wording change (verified correct against LaTeX).** The audit alleged "two contradictory formulas" (CTL `cbrt(3GT^2)`, PINN `sqrt(3GT^2)`). The destination changed this to "the same wrong formula in both documents: `D = cbrt(G*T^2) ≈ 4.64`, omitting M_tot=3." I cross-checked both LaTeX sources directly:
     - `ctl-instruction/sections/04_phase1_data_prep.tex:59` — `D = \sqrt[3]{G T^2}` (no `M_tot`); claimed value `D ≈ 4.6416`.
     - `pinn-architecture/sections/input_vector_inactive.tex:58–60` — same formula `D = \sqrt[3]{G T^2}`, same claimed value `≈ 4.6416`. (Note: this section is `input_vector_inactive.tex` and is currently `%`-commented-out in `main_pinn.tex:16`.)
     The destination's reframing is **factually accurate** against current LaTeX. The audit's original "two contradictory formulas" wording was the audit's own transcription error.
  3. **M16 formula corrected from audit's inverse direction.** The audit said `n_col_per_traj = base_n_col * (dt_base / dt_out)`, which would give *fewer* collocation points to *low-resolution* trajectories — backwards from the intent of compensating for sparse Brutus snapshots. The destinations (`02 §Temporal Resolution Bridging`, `02 P1-8`, `03 M16`, `03 P3-9`) all use the corrected `n_col = base * (dt_out / dt_base)`, giving 1×/8×/17× for gold/hierarchical/standard. The corrected direction is physically right, but `MIGRATION.md` does not log this as an explicit correction of the audit's formula. See Unresolved §4 below.

### 2. `Causal_Trainingmismatch_resolution_blueprint.md` (48 KB)

- **Sections checked:** Introduction, Dataset Pipeline, Architectural Mismatch (causal vs ALM), Causal Failure mode, Causal Mechanics, ALM section, Causal Firewall, Resolution: Time-Windowed Causal-ALM Hybrid, Architectural/Dataset Inconsistencies (Input Vector / Softening / Frame / Temporal Resolution), Validation Metrics (SCS/SASD/IPR/PSC), Synthesized Curriculum Training Protocol (Phases 1–4).
- **Findings verified:**
  - Time-Windowed Causal-ALM Hybrid → `03 §Resolution: Time-Windowed Causal-ALM Hybrid` and `03 [DECISION-NEEDED]` callout listing Options A/B/C with explicit recommendation language preserving the blueprint's stronger conclusion.
  - Augmented 14-D shape-invariant vector → `01 §Recommended Input Vector Specification (Option B — Provisional)`.
  - Dual-context epsilon → `01 §Dual-Context Epsilon Strategy`.
  - Galilean Boost mandate → `01 §Frame Convention: Galilean Boost Mandate`.
  - Temporal-resolution bridging → `02 §Temporal Resolution Bridging`.
  - SCS/SASD/IPR/PSC redesign → `02 §Validation Metrics as Live Training Parameters`.
  - Synthesized Curriculum Training Protocol Phases 1–4 → `03 §Training Phases`.
- **Notable interpretive synthesis (acceptable):** The blueprint's text for SCS thresholds is degenerate (`"Any trajectory resulting in an $SCS > -6$ must be outright rejected"` — missing the `10^` prefix). The destination correctly reconstructs this as `SCS > 1e-6` (Phase 1 screening) and `SCS < 1e-8` (Stage 5 tightening) and supplies the explicit formula `SCS = max_t |H(t) - H(0)| / |H(0)|`. This is a defensible repair of a source-side typo.
- **Drop:** Only the `Conclusion` and `Works cited` sections were intentionally not migrated. Acceptable per `MIGRATION.md` ("Archived only").

### 3. `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` (8 KB)

- **Sections checked:** Documents analysed, §2 Gaps identified from initial two documents (six original gaps), §3 Gaps resolved by PINN/CTL documents, §4 Critical remaining issue (causal training mismatch), §5 Minor remaining clarifications (three items), §6 Recommended information package.
- **Findings verified:**
  - §4 Causal training mismatch (Option A vs Option B framing) → `03 §Causal Training Mismatch: Option A vs Option B` and `03 [DECISION-NEEDED]` callout, augmented with the blueprint's Option C (Hybrid). Correct synthesis.
  - §5 Three minor clarifications → `02 §Validation Threshold Clarifications` (Overfit Challenge precision, 14D input authority, gold-standard validation thresholds). All three are present and independently traceable. ✓
- **Concern (moderate):** **The `02 §Data Validation Protocol — 6-Gap Analysis` table does NOT contain the original's six gaps.** The original's §2 lists pre-agent unknowns (uniform vs non-uniform sampling, COM/momentum handling, dataset variants in scope, CTL-PINN architecture role, numerical environment, Overfit Challenge precision). The destination's six gaps are an entirely different set framed around audit findings (B-06 validator, B-11 IDs, M11 blacklist, M13 gold counterpart, M12/M16 dt_out, G6 causal mismatch). Only the causal-mismatch gap maps directly. The `MIGRATION.md` row "Gaps identified from initial two documents → 02 §Data Validation Protocol — 6-Gap Analysis | Synthesized" is misleading because the synthesis substitutes a different gap list rather than restating the original's six. The original's six gaps *are* recovered scattered across `01 §Frame Convention` (COM), `02 §Validation Threshold Clarifications` (Overfit), `02 §Precision Handling in Validation` (numerical env), `02 §Dataset Inventory` (variants in scope), etc., so no content is lost — only the section attribution is misleading. See Unresolved §2 below.

### 4. `review.md` (6 KB, scaling-contract review)

- **Sections checked:** Scaling-contract validation, AD chain-rule factor finding, Three-layer separation proposal, Forward/inverse derivative conversion rules.
- **Findings verified:**
  - AD chain-rule conversion (`d/du = 2*d/dτ`, `d²/du² = 4*d²/dτ²`) → `01 §AD Chain-Rule Factor` lines 64-67, transcribed verbatim with the correct factors.
  - Impact (physics residual off by 4×, kinetic energy off by 4×) → preserved verbatim.
  - Three-layer separation `(t,r,v)_raw → (u,r',v')_physics-scaled → (τ, IC_norm)_network-input` → preserved verbatim.
  - Inverse formulas `v = (2D/T) * dr'/dτ`, `a = (4D/T²) * d²r'/dτ²` → preserved verbatim.
- **Minor drop:** The original's clarifying note that the inverse maps recover **BRUTUS dataset units** (not SI/cgs) was not migrated. This is a documentation-clarity loss only.
- **No conflict with audit's D=6.694:** The reviewer accepted CTL's existing `D ≈ 4.6416` as internally consistent with the rescaling math; they did not propose changing D. The audit's separate B-02 fix (use `D = cbrt(G*M_tot*T^2)`) is a different choice of scaling convention that is compatible with the chain-rule analysis but produces a different numerical D.

### 5. `stage-assignment-issue.txt` (10 KB)

- **Sections checked:** Evaluation of the data-driven proposal, ML best-practices research, Redesigned Section 2.3 (EDA, PCA, K-means, quantiles), Step-by-Step Workflow, EDA Python snippet, `assign_stages` Python snippet, Integration with CTL framework.
- **Findings verified:**
  - Methodology (transition from fixed thresholds to data-adaptive) → `03 §Data-Driven Adaptive Stage Assignment` with all five rationale points preserved.
  - EDA workflow steps 1–6 → `03 §Methodology` Step 1 (lines 120–127).
  - PCA + K-means + quantile code → `03 §Step 2` (lines 130–158). Algorithmic structure matches; visualization-only lines (`sns.heatmap`, `plt.show`) and a trailing `print()` are removed. `MIGRATION.md` correctly states "algorithmic structure preserved, not exact verbatim copy."
  - `assign_stages` function → `03 §Step 3` (lines 162–184). Logic and stage-assignment indices match the original.
  - Safeguards and Integration notes → preserved.
- **Minor drop:** Specific paper citations (arXiv:2012.12883, arXiv:2208.04532, JMLR 24-1023, ICLR `Skva1xrtYX`, etc.) are not preserved. They were used only to back the methodology claim and are not load-bearing for implementation.

### 6. `next-step-for-data-processing-pipeline.txt` (6 KB)

- **Sections checked:** Top-level questions (PCA evaluation, file format, section-4 step exam, code/text consistency), Issues identified (I_norm), Prompt for AI (12 \authcomment items), Grok response (COM transformation timing).
- **Findings verified:**
  - File format question → `02 §File Format: h5 vs txt/json` with [DECISION-NEEDED] callout. Both pros/cons lists present and tradeoffs preserved.
  - I_norm text-vs-code inconsistency → `01 §Input Vector Normalization Formulas` table footnote AND `01 §Open Decisions` callout. Both halves of the inconsistency (raw `tr(I)/(M r_char^2)` text vs `tanh(...)` code) are preserved with `tanh` recommended provisionally pending LaTeX revision.
  - Grok COM-transformation analysis → `01 §Frame Convention: Galilean Boost Mandate`. Substantive content (transform IC pos/vel; transform Brutus time-series by IC-derived COM; don't transform masses/times) is preserved.
- **Concerns:**
  1. **Grok recommended COM AFTER step 2 (global scaling); destinations adopt audit's COM-FIRST ordering.** This is a deliberate override based on the audit's M3 finding that scaling preserves non-zero COM. The destination's choice is physically correct (scaling commutes with translation only when COM is already at origin). The original Grok recommendation is overridden, not preserved as alternative. Defensible because the audit's reasoning is stronger; flag for traceability.
  2. **MIGRATION.md claim "12 author-flagged \authcomment items resolved" is overstated.** The 12 items are at LaTeX line numbers 566, 767, 911, 920, 948, 1033, 1063, 1217, 1357, 1366, 1527, 1557. About six are substantive (COM, canonical-ordering details, IC-vector-bounds verification, mathematical-guarantees verification, softening accuracy, L_max formula consistency) and *are* captured in the destinations. About six are vague meta-comments ("what is this? why is it here?", "two paragraphs suspicious", duplicates of earlier items) that are not — and arguably cannot be — resolved by a documentation consolidation alone. They properly belong to a future LaTeX-revision phase. Flag for honesty about what `MIGRATION.md` is claiming.

### 7. `next steps.txt` (128 KB, oldest, mostly superseded)

- **Sections checked:** Issues 1, 2–11, 12, 13, 14, 15, 16, 17, 18, 19 (all 19 numbered issues).
- **Unique extracted findings — all present:**
  - Issue 1 (tau_L and L_max formulas) → `03 §tau_L and L_max Formula Resolution` with both `compute_L_norm` and `compute_tau_L` Python functions. The compute_globals snippet uses CTL's original `D = np.cbrt(G * T_scale**2) ≈ 4.64`; an explicit "Note on D value" at `03:321` flags that this must be replaced with `D = cbrt(G * M_tot * T_scale^2) = 6.694` per B-02 and that all `tau_L` and `L_norm` values must be recomputed. ✓
  - Issue 12 (explicit AD code requirement) → `01 §Explicit AD Implementation Requirement` provides a concrete `time_derivatives` PyTorch implementation that does **component-wise** derivatives (rather than a collapsed gradient of the summed 9-D output) and applies the τ→u factors of 2 and 4. Original Issue 12 only described the gap; destination synthesizes the fix.
  - Issue 13 (Huber δ for normalized energy) → `03 §Huber Delta for Normalized Energy` with the recommended starting policy `delta_energy = np.clip(np.quantile(abs_delta_H_train, 0.75), 0.01, 0.1)` and the rationale. ✓
  - Issue 15 (5-OoM softening) → `01 §5 Orders of Magnitude Difference — Softening Analysis` at r = 1, 0.01, 0.001, 1e-4. Independently re-derived numbers below.
  - Issue 17 (compute_globals) → `02 §Global Scale Computation` with the corrected `D = np.cbrt(G * M_tot_ref * t_max**2)` (with `M_tot_ref = 3.0`) and an explicit comment that older snippets used the wrong formula. ✓
  - Issue 18 (loss component scaling contract) → `03 §Loss Component Scaling Contract` as a three-row table summarizing required units, evaluation points, and AD chain-rule factors per loss term. ✓
  - Issue 19 (normalization formulas verification) → `01 §Input Vector Normalization Formulas` canonical table + `5.2 Component Specifications` table. All confirmed formulas present (E, s_min, m, Q, I, shape invariants, time, direction cosines). The original's flagged inconsistencies (time `[0,1]` vs `[-1,1]`; tanh vs Min-Max) are resolved in favor of `[-1,1]` and `tanh`.
- **Issues 2–11, 14, 16:** Confirmed as superseded by the 2026-04-27 audit (B-07/B-08 absorb collocation/batch issues; M2 absorbs time-normalization conflict; B-10 absorbs omega0 scheduling; B-09 absorbs softening unification; Issue 16 is a near-duplicate of Issue 1 and is covered by the same destination section).

---

## Mathematical Verification

Every numerical claim was recomputed directly with `python3` against canonical formulas. Where the result agrees with the destination, I mark `MATCH`; where it disagrees, I show both numbers.

### M-1 Characteristic length D — `MATCH`

```
D = (G * M_tot * T^2)^(1/3)  with G=1, M_tot=3, T=10
  = (3 * 100)^(1/3)
  = 6.6943295008216941
```

Destination claim `D = 6.694` ✓. The CTL/PINN LaTeX value `D ≈ 4.6416` corresponds to `(G*T^2)^(1/3) = 4.6415888336127784`, confirming both LaTeX sources omit `M_tot=3`. The audit's claim that PINN used `sqrt(3GT^2)` is **not** supported by the LaTeX (`input_vector_inactive.tex` has `\sqrt[3]{G T^2}`); the destination's reframing to "same wrong formula in both documents" is the **factually correct** description of the LaTeX state.

### M-2 SIREN init variance ratio — `MATCH`

```
omega0^4 = 30^4 = 810000
```

Destination claim "810,000× variance explosion at omega0=30" ✓. The variance of `U[-a,a]` is `a²/3`. Wrong-formula has `a ∝ omega0`, correct-formula has `a ∝ 1/omega0`, so variance ratio = `omega0^4`. ✓

### M-3 AD chain-rule factors — `MATCH`

```
u = (tau + 1) / 2  ⇒  du/dtau = 1/2
⇒ d/du = 2 * d/dtau
⇒ d^2/du^2 = 4 * d^2/dtau^2
```

Destination claim `d/du = 2*d/dtau`, `d²/du² = 4*d²/dtau²` ✓. Both factors are exact consequences of the linear time map.

### M-4 L_max formula — `MATCH (functional form)`

```
L_max = M_tot * r_char * v_char
v_char = sqrt(2 * |E| / M_tot)   (circular-orbit velocity at the system energy)
```

Destination uses this formula in `03 §tau_L and L_max Formula Resolution` (lines 200–243) and in the `01` normalization table for `L_norm_norm = 2*clip(L/L_max, 0, 1) - 1`. The clamping is explicit ✓.

### M-5 Dataset gap arithmetic — `MATCH`

| Claim | Recomputed | Match |
|-------|-----------|-------|
| Standard 1250/4000 → 31.2% gap | 31.25% | ✓ |
| Hierarchical 143/5000 → 2.9% gap | 2.86% | ✓ |
| Standard-gold missing 184 IDs | Verified by counting `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`: 18 lines × 10 IDs + 1 line × 4 IDs = 184 IDs | ✓ |

The 2,749 standard / 2,565 gold counts in the same file confirm `2749 − 2565 = 184`.

### M-6 Temporal-resolution ratio — `MATCH`

```
0.17 / 0.01 = 17.0   (standard / gold)
0.08 / 0.01 = 8.0    (hierarchical / gold)
```

Destination claim "17×" and "1×/8×/17× supplemental collocation" ✓. The corrected `n_col = base * (dt_out / dt_base)` gives the right direction (low-res trajectories get more collocation).

### M-7 Softening additive-potential analysis — `MATCH`

For `V = -1 / (r + eps)`:

| r | eps | V | % change vs V_unsoftened | Destination claim |
|---|-----|---|--------------------------|-------------------|
| 0.001 | 1e-5 | −990.099 | 0.9901% | "≈0.99%" ✓ |
| 0.001 | 1e-10 | −999.9999 | 1.000e-5 % | "≈0.00001%" ✓ |
| 1e-4 | 1e-5 | −9090.91 | 9.09% (eps is 0.1×r) | "0.1× separation / ≈9.1%" ✓ |
| 1e-4 | 1e-10 | −9999.99 | 1.000e-4 % | "≈0.0001%" ✓ |

All four softening rows in `01 §5 Orders of Magnitude Difference` reproduce within rounding. The remediation log's claim that prior small-eps values at r=0.001 and at r=1e-4 were corrected matches the file on disk.

### M-8 I_3 normalization degeneracy — `MATCH`

If `I_max = max(I_1, I_2, I_3) = I_3` after sorting, then `I_3/I_max = 1` by construction; the linear remap `2*1 - 1 = 1` puts it at the boundary and loses absolute scale information. Destination flags this in `01 §5.3 Shape Invariant and Direction Cosine Computation` with explicit guidance to either use raw pre-division `I_3` or a global `I_scale`. ✓

### M-Q-IMPACT (the one math discrepancy) — `01 §Quantitative Impact of D Formula Error` table

Let `k = D_correct / D_wrong = 6.694/4.6416 = 1.4422`. With `r' = r/D` and `v' = v/(D/T)`:

| Quantity | Scaling | True ratio (D_wrong / D_correct) | Destination's stated number |
|----------|---------|----------------------------------|----------------------------|
| `r'` | `∝ 1/D` | `k = 1.4422` ⇒ 44.22% larger | "44% too large" ✓ |
| `v'` | `∝ 1/D` | `k = 1.4422` ⇒ 44.22% larger | "44% too large" ✓ |
| KE `= 0.5·m·v'²` | `∝ k²` | `k² = 2.0801` ⇒ **108% larger** | "44% too large (KE)" ✗ |
| \|PE\| `∝ 1/r'` | `∝ 1/k` | `1/k = 0.6934` ⇒ **30.7% smaller** | "44% too small (PE)" ✗ |
| Sum `E_scaled` | mixed | not simply 75% | "Net ~75% error in total" ✗ (not derivable from the row's components) |
| `L = m·r'×v'` | `∝ k²` | `k² = 2.0801` ⇒ 108% larger | "108% too large" ✓ (consistent only if `L_norm` here means the raw scaled L, not the L/L_max ratio) |
| `Q = 2T/\|V\|` (virial) | `∝ k³` | `k³ = 3.0000` ⇒ **200% larger** | "Net ~90% error" ✗ |

**Conclusion:** The `r'` and `v'` rows are correct (linear in 1/D). The L row is correct *iff* "L_norm" denotes the raw scaled angular momentum (which it appears to in this table, since `L/L_max` would be invariant to the D choice). The KE/PE/Q rows show numbers that are inconsistent with the very scaling formulas they cite. The remediation log says it corrected "L_norm quantitative impact" from 77% to 108%; that fix is present, but the analogous fix for KE (44 → 108), PE (44 → 30.7), and Q (90 → 200) was not applied. See Unresolved §1.

### M-9 `compute_globals` D value (post-remediation) — `MATCH`

The destination's `02 §Global Scale Computation` block uses `M_tot_ref = 3.0` and `D = np.cbrt(G * M_tot_ref * t_max**2)`, with an explicit comment "Corrected B-02 scale: D = 6.694 for G=1, M_tot=3, T=10." ✓ The remediation log's claim that this block was updated is accurate.

---

## Structural Verification

### S-1 DECISION-NEEDED distribution — `MATCH`

Counting strict callouts (a `> **[DECISION-NEEDED]**` line that opens a multi-line blockquote, not in-text references):

| File | Strict callouts | All `[DECISION-NEEDED]` mentions |
|------|-----------------|----------------------------------|
| 01 | 2 (Input vector composition, I_norm definition) | 4 (2 callouts + 2 cross-refs) |
| 02 | 1 (file format h5 vs txt/json) | 3 (1 callout + 2 cross-refs) |
| 03 | 2 (Causal training mode, s_min frame) | 2 (both are callouts) |

Strict distribution `01=2, 02=1, 03=2` (total 5) ✓. This matches both the prior `09-VERIFICATION-REPORT.md` and `09-CONTEXT.md` D-12.

### S-2 `MIGRATION.md` aggregate counts — `MATCH (no 86-mapped-sections claim)`

`grep` for the strings "86 mapped" and "mapped sections" returns no hits in `MIGRATION.md`. The summary table uses defensible explicit counts: "Explicit provenance table rows | 40", "Verbatim-copied formal specs | 1", "Unique findings preserved | 36". Total table row count: 53 lines starting with `|`, of which the seven per-file `Original section | Destination | Notes` headers and one summary header explain the gap to the "40 provenance rows" summary value. ✓

### S-3 Verbatim §6 — `VERIFIED VERBATIM`

`diff` between archive `three_body_pinn_pre-implementation_audit_2026-04-27.md` lines 290–410 and destination `03-curriculum-and-training-loop.md` lines 555–679 shows only trailing-whitespace and blank-line differences. Section 6.1 (Design Principles), 6.2 (full training-step pseudo-code), 6.3 (stage transition criteria + threshold table), and 6.4 (`get_lambda_E` function) are all preserved without semantic change.

### S-4 Audit §5 correctly described as synthesized — `MATCH`

`MIGRATION.md` row for §5 says: "Synthesized/reconciled. Audit Option A trig encoding is preserved as a considered alternative; the consolidated recommended spec uses Option B shape invariants + direction cosines. Not copied verbatim." This matches what is on disk in `01 §Recommended Input Vector Specification (OPTION B — PROVISIONAL)` and `01 §Considered Alternatives`.

### S-5 Cross-reference resolution — `ALL RESOLVE`

All local cross-doc links (`01 ↔ 02 ↔ 03`, `MIGRATION.md`, `archive/`) and all canonical-ref paths (`PINN_architecture_plan.md`, `CTL-instruction-final.md`, `basic_architecture.py`, `data-processing-pipeline-full.py`, `simulation_data/Documentation/README.md`, `calculate_metrics.py`) resolve to existing files. README.md's three canonical refs also resolve.

### S-6 Cross-doc claim consistency — `MATCH`

| Topic | 01 says | 02 says | 03 says | Consistent? |
|-------|---------|---------|---------|-------------|
| Causal mode | (Open Decision lives in 03) | (gap G6 → 03) | `[DECISION-NEEDED]` Options A/B/C; recommends preserving blueprint Option C | ✓ |
| `I_norm` | `[DECISION-NEEDED]` recommends `tanh` | (cross-ref to 01) | (cross-ref to 01) | ✓ |
| `s_min` | D8: canonical split lives in 03 | n/a | `[DECISION-NEEDED]`: unsoftened for stage gate, `max(s_min, eps_soft)` for training-loss collision | ✓ |
| dt_out scaling | n/a | `n_col = base * (dt_out/dt_base)` (P1-8 + intro section) | `n_col = base * (dt_out/dt_base)` (M16 + P3-9) | ✓ |
| Source-vs-live-code (B-01) | "live `basic_architecture.py:37` already divides by omega0; this is a source-document defect" | n/a | n/a | ✓ |
| Dual-epsilon | `eps=1e-10` static, `eps_soft=1e-5` dynamic | "validation uses static eps=1e-10 while training uses dynamic eps_soft=1e-5"; `compute_globals` uses `eps=1e-10` | Phase 1 pre-screening uses `eps=1e-10`; `L_physics`/`L_energy` use `epsilon_soft=1e-5`; `s_min` decision uses `epsilon_soft=1e-5`; `compute_L_norm` uses `eps=1e-10` | ✓ |

No cross-doc contradictions detected.

### S-7 Severity Reclassification Ledger — `PRESENT`

`02 §Severity Reclassification Ledger` explicitly records the M11 (audit MAJOR → consolidated BLOCKING) and M12 (audit MAJOR → consolidated BLOCKING) reclassifications with rationale ("DataLoader cannot ship with silently-corrupted training data"; "32-points-per-trajectory batch contract is infeasible for standard trajectories"). This matches the prior remediation claim and is defensible.

### S-8 Size analysis — `MATCH`

Sources total ≈ 246.7 KB (38.1 + 48.7 + 8.3 + 6.4 + 6.2 + 10.7 + 128.3). Destinations total ≈ 107.3 KB (35.4 + 27.3 + 44.6). Ratio ≈ 43.5%, comfortably under the CONTEXT.md target of ≤ 80%. The size reduction is consistent with (a) deduplication, (b) cherry-picking only unique content from the 128 KB `next steps.txt`, and (c) dropping the audit's executive narrative in favor of structured tables.

---

## Unresolved Issues (require human judgment)

These are documentation-quality items I do not believe Phase 9's scope authorizes me to silently fix in the destinations. They should either be addressed by a follow-up patch to the consolidation or knowingly accepted.

1. **Quantitative Impact table (`01:309–316`) carries math errors.** Three of the five rows (KE, PE, Q) state percentages that are inconsistent with the scaling formulas they cite. The corrected values are: KE = 108% larger (not 44%), \|PE\| = 30.7% smaller (not 44%), Q = 200% larger (not 90%). Net E_scaled error is not a single percentage. The L_norm row (108%) is consistent only under the interpretation that "L_norm" here means raw scaled angular momentum L, not the L/L_max ratio used in the IC vector — this should be clarified inline. Recommended action: replace the table with the corrected values OR explicitly state which "L_norm" definition is in scope and recompute KE/PE/Q accordingly.

2. **`02 §Data Validation Protocol — 6-Gap Analysis` is misnamed.** The table contains six audit-derived gaps (B-06, B-11, M11, M13, M12/M16, G6 causal), not the original document's six gaps (uniform-vs-non-uniform sampling, COM/momentum handling, dataset variants in scope, CTL-PINN architecture role, numerical environment, Overfit Challenge precision). The original's gaps *are* preserved scattered across the destinations, but the section attribution implies a faithful restatement that doesn't exist. Recommended action: rename to "6-Gap Analysis (Pipeline-Level, Audit-Derived)" and add a parenthetical pointing to where the original's pre-agent gaps now live, or add a separate sub-table for the original's six gaps.

3. **Audit B-09 epsilon = 1e-8 alternative not preserved.** The audit's specific recommendation to unify softening at `eps = 1e-8` (compromise) was discarded in favor of the Causal blueprint's dual-context strategy (`1e-10` / `1e-5`). The dual-context strategy is stronger, but the audit's compromise position is now nowhere recoverable from the destinations. Recommended action: add a one-paragraph "Considered Alternative: unified `eps = 1e-8`" under `01 §Dual-Context Epsilon Strategy` so the choice between unified-vs-dual can be re-litigated by future readers.

4. **M16 formula correction not logged in `MIGRATION.md`.** The destinations correct the audit's `n_col = base * (dt_base/dt_out)` to `n_col = base * (dt_out/dt_base)` in four places, but `MIGRATION.md` does not flag this as a deliberate deviation from audit text. Recommended action: add a Notes-column annotation on the M16 row of the audit's manifest entry, e.g., "Formula direction inverted vs audit text to match the physical intent (low-res ⇒ more supplemental collocation)."

5. **Minor migration losses (informational only):**
   - `review.md`'s clarifying note that the inverse maps recover **BRUTUS dataset units** (not SI/cgs) is not preserved.
   - The audit's `§4 Author-Flagged Uncertainties` summary table (28-item severity breakdown: 8 CRITICAL, 10 MAJOR, 6 MINOR, 4 INFO) is not preserved as a single table; individual items are scattered.
   - The audit's `§9` table covers nine fix categories; the destination's `01 §Quantitative Impact of D Formula Error` covers only the D-related row. Other categories are recoverable from the per-finding sections, but the consolidated impact summary is not.
   - `next-step-for-data-processing-pipeline.txt`'s Grok recommendation to apply COM **after** Step 2 scaling is overridden by the audit's M3 COM-FIRST ordering (defensible; audit is physically right) but not preserved as Considered Alternative.
   - `MIGRATION.md`'s claim that "12 author-flagged \authcomment items resolved" is overstated; about half are vague meta-comments outside Phase 9's scope.

---

## Recommendation

The Phase 9 consolidation as it stands on disk **substantially preserves all unique findings from the seven archived originals**. No silent content loss was detected. The five DECISION-NEEDED callouts are correctly placed and the verbatim §6 is byte-equivalent (modulo whitespace) to the audit. Cross-document claims for causal mode, `I_norm`, `s_min`, dt_out scaling, source-vs-live-code attribution, and dual-epsilon are internally consistent.

The four moderate concerns (Quantitative Impact math, 6-Gap Analysis naming, B-09 alternative not preserved, M16 correction not logged) are documentation-clarity issues that do not invalidate the consolidation but should be patched before any downstream implementation phase quotes the affected sections.

The prior `PASS AFTER REMEDIATION` verdict in `09-VERIFICATION-REPORT.md` is broadly supported by this independent re-verification; the additional concerns surfaced here are issues the prior remediation did not target.

---

*End of independent re-verification report. The existing `09-VERIFICATION-REPORT.md` was not modified.*
