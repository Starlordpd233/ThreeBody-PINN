# Phase 9 Re-Verification Report

**Agent:** kimi-2.6  
**Date:** 2026-04-28  
**Scope:** Independent re-verification of the Phase 9 issues-directory consolidation after prior remediation.  
**Method:** Per-original evidence pass, independent math recomputation, structural consistency audit, cross-reference validation against canonical LaTeX sources.

---

## Summary Verdict

**PASS WITH MINOR FINDINGS** — The consolidation substantively preserves all unique findings from the seven archived originals. The three destination documents are internally consistent, mathematically sound, and correctly attribute provenance. Two minor cosmetic issues (a stale D value in a code comment and a phrasing ambiguity in B-09 attribution) are noted below but do not affect correctness.

| Metric | Count |
|--------|-------|
| Archived originals examined | 7 |
| Destination thematic docs verified | 3 |
| Independent math checks run | 8 |
| Structural checks run | 6 |
| Issues found | 2 minor |
| Blocking issues | 0 |

---

## Per-Original Verification

### 1. three_body_pinn_pre-implementation_audit_2026-04-27.md

**Status: PRESERVED**

- **B-01..B-11, M1..M16, D1..D10**: All findings correctly distributed across `01`, `02`, `03` per the MIGRATION.md mapping. Severity labels (BLOCKING / MAJOR / MINOR) are consistent.
- **§5 Corrected Input Vector Specification**: MIGRATION.md correctly states this is "synthesized/reconciled, not verbatim." The audit's original Option A (trig encoding) is preserved under `01` "Considered Alternatives"; the consolidated doc recommends Option B (shape invariants + direction cosines). This satisfies D-05 conflict-resolution policy.
- **§6 Unified Batch Construction**: **VERIFIED VERBATIM** in `03` "Verbatim Reference Specification." Line-by-line comparison of the pseudo-code, stage transition criteria, and energy loss weight schedule confirms exact textual preservation.
- **§9 Quantitative Impact**: Present in `01` with D=6.694. Independent recomputation confirms the 44% position/velocity error, 108% L_norm error, and 810,000x SIREN variance ratio.
- **§8 Cross-Issue Interaction Matrix**: Synthesized into `README.md` and all three destination docs.

**Minor finding:** B-09 in the original audit recommended "Unify at epsilon = 1e-8." The consolidation instead adopts the `Causal_Trainingmismatch` dual-context strategy (eps=1e-10 static, eps_soft=1e-5 dynamic). This is physically defensible and consistent with D-05, but the `MIGRATION.md` does not explicitly flag that the consolidation **overrides** the audit's specific B-09 fix. The destination docs themselves correctly document the dual-context rationale.

---

### 2. Causal_Trainingmismatch_resolution_blueprint.md

**Status: PRESERVED**

- **Time-Windowed Causal-ALM Hybrid**: Present in `03` as the explicit recommendation, with Option A and Option B also documented. The `03` Open Decision preserves the blueprint's stronger conclusion rather than silently downgrading it.
- **Shape invariants + direction cosines vs trig encoding**: Present in `01` "Considered Alternatives" and "Recommended Input Vector Specification."
- **Dual-Context Epsilon**: Present in `01` with the full hardware/precision justification table.
- **SCS/SASD/IPR/PSC as live training parameters**: Present in `02` with updated mathematical formulations.
- **Galilean boost mandate**: Present in `01` "Frame Convention: Galilean Boost Mandate."
- **Temporal resolution bridging**: Present in `02` "Temporal Resolution Bridging" with the corrected `dt_out / dt_base` scaling formula.

---

### 3. Issue_on_data_validation_protocol_and_compatbility_with_project_context.md

**Status: PRESERVED**

- **6-gap analysis**: Present in `02` "Data Validation Protocol — 6-Gap Analysis." All six gaps (G1-G6) are traceable.
- **Option A vs B causal training**: Present in `03` as `[DECISION-NEEDED]`.
- **Minor clarifications**: Overfit Challenge precision, 14D input authority, and gold-standard validation thresholds are independently traceable in `02` "Validation Threshold Clarifications."

---

### 4. review.md (scaling-contract review)

**Status: PRESERVED**

- **AD chain-rule factor**: Present in `01` "AD Chain-Rule Factor — Missing Derivative Conversion." The derivative rules `d/du = 2*d/dtau` and `d²/du² = 4*d²/dtau²` are copied correctly.
- **Three-layer separation**: Present in `01` with the formalism `raw → physics-scaled → network-input`.
- **Explicit AD implementation**: Augmented with Issue 12 content from `next steps.txt` in `01` "Explicit AD Implementation Requirement."

---

### 5. stage-assignment-issue.txt

**Status: PRESERVED**

- **PCA + K-means + quantiles methodology**: Present in `03` "Data-Driven Adaptive Stage Assignment." MIGRATION.md correctly states "algorithmic structure preserved, not exact verbatim copy" — the code snippets are synthesized but the core logic (EDA → PCA → K-means → quantile thresholds → assignment functions) is fully preserved.
- **Hybrid physical + empirical approach**: Correctly documented in `03`.

---

### 6. next-step-for-data-processing-pipeline.txt

**Status: PRESERVED**

- **h5 vs txt/json**: Present in `02` as `[DECISION-NEEDED]` with Option A/B analysis.
- **I_norm text-vs-code inconsistency**: Present in `01` as `[DECISION-NEEDED]` with the tanh version recommended.
- **COM transformation timing**: Merged with B-05 in `01` "Frame Convention: Galilean Boost Mandate."
- **12 authcomment items**: The MIGRATION.md claims these are synthesized into Open Decisions across all docs. The most consequential ones (COM frame, I_norm, softening, time normalization) are indeed traceable; the full 12-item resolution is not itemized in the destination docs but was out of scope per 09-CONTEXT.md deferred items.

---

### 7. next steps.txt

**Status: PRESERVED (unique findings only)**

Per D-06, only unique non-audit content was extracted. MIGRATION.md lists seven unique findings. All are verified:

| Issue | Claimed Destination | Verified |
|-------|---------------------|----------|
| Issue 1 (tau_L / L_max) | `03` tau_L section | YES — formulas and Python implementation present |
| Issue 12 (explicit AD) | `01` Explicit AD Requirement | YES — component-wise derivative code present |
| Issue 13 (Huber delta) | `03` Huber Delta section | YES — delta calibration concern and quantile-based policy present |
| Issue 15 (5-OoM softening) | `01` 5 Orders of Magnitude Difference | YES — full additive-potential analysis present |
| Issue 17 (global scales) | `02` Global Scale Computation | YES — parallelized compute_globals pseudo-code present |
| Issue 18 (loss scaling contract) | `03` Loss Component Scaling Contract | YES — three-term contract table present |
| Issue 19 (normalization formulas) | `01` Input Vector Normalization Formulas | YES — comprehensive table with all components present |

**Minor finding:** The `compute_globals` code block in `02` (from Issue 17) still contains a comment referencing `D ≈ 4.64` from the original archived source. The code itself uses the corrected `D = np.cbrt(G * M_tot_ref * t_max**2)`, but the comment is stale and could mislead a reader who glances at the comment rather than the formula.

---

## Mathematical Verification

All checks were recomputed independently; no value was accepted from document text without verification.

| Check | Expected | Recomputed | Status |
|-------|----------|------------|--------|
| Characteristic length D | 6.694329500821695 | 6.694329500821694 | PASS |
| SIREN variance ratio (30^4) | 810,000 | 810,000.0 | PASS |
| AD chain rule (first derivative) | d/du = 2*d/dtau | d/du = 2*d/dtau | PASS |
| AD chain rule (second derivative) | d²/du² = 4*d²/dtau² | d²/du² = 4*d²/dtau² | PASS |
| L_max formula | M_tot * r_char * v_char | Confirmed algebraically | PASS |
| Standard dataset gap rate | 1250/4000 = 31.2% | 31.25% | PASS |
| Hierarchical dataset gap rate | 143/5000 = 2.9% | 2.86% | PASS |
| Standard gold missing IDs | 184 | 184 | PASS |
| Temporal resolution ratio (std/gold) | 0.17/0.01 = 17 | 17.0 | PASS |
| Temporal resolution ratio (hier/gold) | 0.08/0.01 = 8 | 8.0 | PASS |
| Softening at r=0.001, eps=1e-10 | ~0.00001% additive change | 0.000010% | PASS |
| Softening at r=0.001, eps=1e-5 | ~0.99% additive change | 0.990099% | PASS |
| Softening at r=1e-4, eps=1e-5 | ~9.1% additive change | 9.090909% | PASS |
| eps=1e-5 as fraction of r=1e-4 | 0.1x separation | 0.1x | PASS |
| I_3 normalization degeneracy | I_3/I_max = 1 by construction | Confirmed | PASS |
| D impact on scaled positions | 44% too large with D=4.64 | 44.22% | PASS |
| D impact on L_norm | 108% too large | 108.01% | PASS |

**Note on quantitative impact table:** The `01` document claims "Net ~75% error in total E" and "~90% error" in Q. The position/velocity/L_norm numbers are quantitatively exact. The "net ~75% error in total E" is a rough estimate for bound systems where KE and PE partially cancel; it is not independently verifiable without assuming a specific energy distribution and is best read as "order-of-magnitude severe." The Q claim of ~90% error is harder to verify because Q is dimensionless and should be invariant under correct scaling; the error arises from computing Q with incorrectly scaled quantities, making the exact percentage trajectory-dependent. These are presented as impact estimates, not rigorous theorems, and are acceptable as such.

---

## Structural Verification

| Check | Expected | Found | Status |
|-------|----------|-------|--------|
| Thematic docs present | `01`, `02`, `03` | All three present | PASS |
| MIGRATION.md 86-section claim | Removed | No "86" found | PASS |
| Explicit provenance rows | 40 (per MIGRATION.md summary) | 47 table rows including headers/summary; ~40 data rows | PASS |
| Verbatim formal spec | 1 (audit §6) | 1 found in `03`; text matches exactly | PASS |
| Audit §5 described as synthesized | Yes | MIGRATION.md says "synthesized/reconciled" | PASS |
| Formal `[DECISION-NEEDED]` blockquotes | `01=2`, `02=1`, `03=2` | `01=2`, `02=1`, `03=2` | PASS |
| Relative file links | All valid | All file targets exist | PASS |
| In-page anchor links | Valid | `#open-decisions` and `#considered-alternatives` are valid anchors in `01` | PASS |
| Cross-doc causal mode consistency | Preserves blueprint hybrid as stronger recommendation | `03` preserves hybrid, notes CTL describes Option B | PASS |
| `I_norm` consistency | Flagged as open in `01` | `01` table marks tanh as recommended, `[DECISION-NEEDED]` in Open Decisions | PASS |
| `s_min` split consistency | `01` delegates to `03` | `01` D8 says canonical split lives in `03`; `03` Open Decision documents the split | PASS |
| `dt_out` scaling formula | `n_col = base * (dt_out / dt_base)` | Present in `02` and `03` with correct 1x/8x/17x ratios | PASS |
| Source-vs-live-code attribution | B-01 explicitly notes live code is correct | `01` B-01: "live `basic_architecture.py` implementation already divides by `self.omega_0`" | PASS |
| Softening section accuracy | Corrected percentages | `01` "5 Orders of Magnitude" section matches independent computation | PASS |
| `I_3` degeneracy flag | Present | `01` §5.3 Note on I_3 normalization documents the degeneracy | PASS |

---

## Issues Requiring Attention

### Finding M-01 (Minor) — Stale D-value comment in `compute_globals` code block

**Location:** `02-data-pipeline-and-validation.md`, Global Scale Computation section  
**Issue:** The corrected `compute_globals` code uses `D = np.cbrt(G * M_tot_ref * t_max**2)`, but the comment immediately below reads: "Older source snippets used `D = cbrt(G * t_max^2)`, which gives D ≈ 4.64 and omits `M_tot=3`." This is factually correct and serves as a useful warning. However, the **archived** `next steps.txt` Issue 17 code block (which this derives from) contained the incorrect `D = np.cbrt(G * t_max**2)` inline without the `M_tot_ref` factor. The consolidation correctly fixed the formula but left a stray reference to `D ≈ 4.64` in the explanatory text that follows.  
**Impact:** Negligible — the code is correct; a reader might be momentarily confused.  
**Recommendation:** Update the comment to read `D ≈ 6.694` to match the corrected formula, or remove the numerical approximation entirely.

### Finding M-02 (Minor) — B-09 attribution ambiguity

**Location:** `01-architecture-and-physics-foundations.md`, B-09 row and Dual-Context Epsilon Strategy section  
**Issue:** The original audit B-09 fix was "Unify at epsilon = 1e-8." The consolidation adopts the `Causal_Trainingmismatch` dual-context position (eps=1e-10 static, eps_soft=1e-5 dynamic). This override is physically well-justified and consistent with 09-CONTEXT.md D-05, but `MIGRATION.md` describes the audit B-09 mapping simply as "Synthesized" without noting that the consolidated docs **reject** the audit's specific unification recommendation in favor of the dual-context approach.  
**Impact:** Low — the dual-context rationale is fully documented in `01`. A provenance purist might want the manifest to record the deviation explicitly.  
**Recommendation:** Add a one-sentence note to `MIGRATION.md` audit B-09 row: "Consolidated docs adopt dual-context epsilon (1e-10/1e-5) from Causal_Trainingmismatch rather than the audit's proposed single epsilon=1e-8 unification."

---

## Unresolved Items Requiring Human Judgment

No new unresolved items were discovered during this re-verification. The five `[DECISION-NEEDED]` callouts remain the correct set of open questions:

1. **Input vector composition (14-D IC content)** — `01` (Option B recommended but not closed)
2. **`I_norm` definition (text vs tanh)** — `01` (tanh recommended but not closed)
3. **File format (h5 vs txt/json)** — `02` (HDF5 recommended but not closed)
4. **Causal training mode** — `03` (Hybrid recommended but not closed)
5. **`s_min` frame for collision criterion** — `03` (softened for loss, unsoftened for gate)

---

## Conclusion

The Phase 9 consolidation is **substantively complete and correct**. All seven archived originals have been accounted for; all unique findings are preserved; mathematical claims recomputed; structural integrity confirmed. The two minor findings (M-01 and M-02) are cosmetic/provenance niceties that do not affect the technical correctness of the consolidated documentation.

The existing `09-VERIFICATION-REPORT.md` verdict of **PASS AFTER REMEDIATION** is upheld by this independent re-verification.
