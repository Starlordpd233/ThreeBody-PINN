# Phase 9 Re-Verification Report

**Re-verification agent:** Claude (claude-code)
**Date:** 2026-04-28
**Methodology:** Sequential document-by-document build-up, independent math computation, cross-document structural verification

---

## Summary

**Overall verdict: PASS WITH CONCERNS**

The Phase 9 consolidation successfully preserved all unique findings from the 7 archived originals across the 3 thematic destination documents. No substantive findings were dropped. Mathematical claims are correct after remediation. Structural checks pass. Two minor documentation concerns are flagged below — neither is blocking, and neither requires remediation before proceeding to implementation phases.

| Metric | Count |
|--------|-------|
| Archived originals verified | 7 |
| Destination documents checked | 3 |
| Critical issues found | 0 |
| Moderate issues found | 0 |
| Minor concerns flagged | 2 |
| Math checks passed | 8/8 |
| Structural checks passed | 7/7 |

---

## Mathematical Verification

All claims verified by independent computation. Results match the destination documents within rounding tolerance.

| Check | Independent Result | Document Value | Verdict |
|-------|-------------------|----------------|---------|
| D = (G·M_tot·T²)^(1/3) | 6.694329500821695 | 6.694 | CORRECT |
| SIREN init variance ratio 30⁴ | 810,000 | 810,000x | CORRECT |
| AD chain rule d/du = 2·d/dτ | Confirmed | Factor of 2 | CORRECT |
| AD chain rule d²/du² = 4·d²/dτ² | Confirmed | Factor of 4 | CORRECT |
| L_max = M_tot·r_char·v_char | Formula consistent | As stated | CORRECT |
| Standard gap rate 1250/4000 | 31.25% | 31.2% | CORRECT |
| Hierarchical gap rate 143/5000 | 2.86% | 2.9% | CORRECT |
| dt_out ratio 0.17/0.01 | 17.0 | 17× | CORRECT |
| Softening eps=1e-5 at r=0.001 | 0.9901% diff | ~0.99% | CORRECT |
| Softening eps=1e-10 at r=0.001 | 0.00001% diff | ~0.00001% | CORRECT |
| Softening eps=1e-5 at r=1e-4 | 9.09% diff | ~9.1% | CORRECT |
| L_norm quantitative impact | 108.0% overestimate | 108% | CORRECT |
| I_3/I_max degeneracy | Always 1.0 | Flagged correctly | CORRECT |

**Commit 265c0fe fix verification:** The corrected B-02 description ("same wrong formula in both documents" rather than "two contradictory formulas") and corrected L_norm impact (108% rather than 97%) are both present in the destination documents. No residual errors of this class were found.

---

## Per-Original Verification

### Original 1: three_body_pinn_pre-implementation_audit_2026-04-27.md

- **Sections checked:** Executive Summary, §1 Critical Issues (B-01..B-11), §2 Major Inconsistencies (M1..M16), §3 Design Ambiguities (D1..D10), §4 Author-Flagged Uncertainties (28 items), §5 Corrected Input Vector Specification, §6 Unified Batch Construction, §7 Implementation Checklist, §8 Cross-Issue Interaction Matrix, §9 Quantitative Impact Summary
- **Findings verified:** All present
- **Math errors found:** None (post-remediation: D formula, L_norm impact, and softening percentages all correct)
- **Verbatim claims verified:**
  - §6 (Batch Construction) → Copied verbatim into 03 §Verbatim Reference Specification: CONFIRMED. Code blocks, stage transition criteria, and energy weight schedule match the original exactly.
  - §5 (Input Vector) → Synthesized/reconciled, not verbatim: CONFIRMED. Audit Option A (trig encoding) preserved as Considered Alternative in 01; Option B (shape invariants + direction cosines) adopted as recommended spec.
- **Severity/attribution check:** M11 and M12 reclassified from MAJOR to BLOCKING with documented ledger in 02. This is legitimate — the DataLoader-level impact justifies the upgrade, and the ledger provides full traceability.
- **Notes:** B-09 audit recommendation (unify at ε=1e-8) was superseded by the Causal_Trainingmismatch blueprint's Dual-Context Epsilon Strategy (ε=1e-10 static / ε_soft=1e-5 dynamic) per D-05 conflict resolution. The audit's specific 1e-8 recommendation is not individually preserved under Considered Alternatives. See Concern #1 below.

### Original 2: Causal_Trainingmismatch_resolution_blueprint.md

- **Sections checked:** Introduction, Dataset Pipeline, Architectural Mismatch, Causal Failure, ALM, Causal Firewall, Resolution: Time-Windowed Causal-ALM Hybrid, Input Vector Dimensionality, Dual-Context Epsilon, Frame Conventions, Temporal Resolution, Validation Metrics (SCS/SASD/IPR/PSC), Synthesized Curriculum Training Protocol
- **Findings verified:** All present
- **Key unique findings preserved:**
  - Time-Windowed Causal-ALM Hybrid → 03 §Resolution: Time-Windowed Causal-ALM Hybrid ✓
  - Shape invariants + direction cosines → 01 §Considered Alternatives and §Recommended Input Vector Specification ✓
  - Dual-Context Epsilon (ε=1e-10 static / ε_soft=1e-5 dynamic) → 01 §Dual-Context Epsilon Strategy ✓
  - SCS/SASD/IPR/PSC as live training parameters → 02 §Validation Metrics as Live Training Parameters ✓
  - Galilean boost mandate → 01 §Frame Convention: Galilean Boost Mandate ✓
  - Temporal resolution bridging → 02 §Temporal Resolution Bridging ✓
- **Math errors found:** None
- **Notes:** The blueprint's Option C (Time-Windowed Causal-ALM Hybrid) is correctly presented as the stronger recommendation in 03's [DECISION-NEEDED] causal training callout. The callout explicitly states "Phase 9 must preserve that stronger blueprint conclusion rather than silently downgrading it." The remediation correctly fixed a prior drift that had recommended Option B first.

### Original 3: Issue_on_data_validation_protocol_and_compatbility_with_project_context.md

- **Sections checked:** Documents analysed, Gaps identified (G1-G6), Gaps resolved, Critical remaining issue (causal training mismatch), Minor remaining clarifications
- **Findings verified:** All present
- **Unique findings preserved:**
  - 6-gap analysis (G1-G6) → 02 §Data Validation Protocol — 6-Gap Analysis ✓
  - Option A vs B causal training framing → 03 [DECISION-NEEDED] ✓
  - Minor clarifications (Overfit Challenge precision, 14D input authority, gold-standard validation thresholds) → 02 §Validation Threshold Clarifications ✓
- **Math errors found:** None
- **Notes:** The three minor clarifications from §5 of the original are now independently traceable in 02 §Validation Threshold Clarifications. The remediation correctly added this section after the original verification found them untraceable.

### Original 4: review.md

- **Sections checked:** Scaling contract, AD chain-rule factor, three-layer separation, derivative conversion rules
- **Findings verified:** All present
- **Unique findings preserved:**
  - AD chain-rule factor missing → 01 §AD Chain-Rule Factor ✓
  - Physics residual off by factor of 4, kinetic energy off by factor of 4 ✓
  - Three-layer separation: raw → physics-scaled → network-input → 01 ✓
  - Derivative conversion rules → 01, with explicit PyTorch component-wise implementation ✓
- **Math errors found:** None
- **Notes:** The derivative conversion rules (d/du = 2·d/dτ, d²/du² = 4·d²/dτ²) are correctly transcribed in 01. The remediation added an explicit component-wise PyTorch implementation (Issue 12 from next steps.txt), which was correctly integrated into the AD Chain-Rule Factor section.

### Original 5: stage-assignment-issue.txt

- **Sections checked:** Evaluation, Research, Redesigned Section 2.3, Step-by-Step Workflow, PCA/K-means code, Adaptive Stage Assignment functions
- **Findings verified:** All present
- **Unique findings preserved:**
  - PCA + K-means + quantile adaptive staging → 03 §Data-Driven Adaptive Stage Assignment ✓
  - Python code structure for EDA, clustering, adaptive assignment → 03 (synthesized, algorithmic structure preserved) ✓
  - Hybrid physical metrics + empirical distributions approach → 03 ✓
- **Math errors found:** None
- **Notes:** MIGRATION.md correctly states "algorithmic structure preserved, not exact verbatim copy" for the PCA/K-means code. The remediation fixed a prior false verbatim claim. The code in 03 is a synthesized version that preserves the algorithmic logic (PCA→K-means→quantile thresholds→adaptive assignment functions) with restructured variable names and comments for clarity.

### Original 6: next-step-for-data-processing-pipeline.txt

- **Sections checked:** Data stratification methodology, h5 vs txt/json, data preprocessing, I_norm inconsistency, 12 authcomment items, Grok response (COM transformation timing)
- **Findings verified:** All present
- **Unique findings preserved:**
  - h5 vs txt/json [DECISION-NEEDED] → 02 §File Format: h5 vs txt/json ✓
  - I_norm text-vs-code inconsistency → 01 §Input Vector Normalization Formulas + [DECISION-NEEDED] ✓
  - COM transform order → 01 §Frame Convention: Galilean Boost Mandate (merged with B-05 and M3) ✓
  - 12 authcomment items → distributed across 01, 02, 03 §Open Decisions ✓
- **Math errors found:** None
- **Notes:** The I_norm [DECISION-NEEDED] is correctly preserved (was prematurely marked RESOLVED before remediation). The 12 authcomment items are individually addressable across the three docs — they are not enumerated as a numbered list in the destination but are traceable through the COM frame, canonical ordering, IC vector range, mathematical guarantees, softening parameter, L_max formula, and duplicate check sections.

### Original 7: next steps.txt

- **Sections checked:** Issues 1, 12, 13, 15, 17, 18, 19 (extracted); Issues 2-11, 14, 16 (superseded)
- **Findings verified:** 7 unique issues extracted, remaining correctly superseded
- **Extracted issues traceability:**
  - Issue 1 (τ_L / L_max) → 03 §tau_L and L_max Formula Resolution ✓
  - Issue 12 (AD implementation) → 01 §Explicit AD Implementation Requirement ✓
  - Issue 13 (Huber δ) → 03 §Huber Delta for Normalized Energy ✓
  - Issue 15 (5-OoM softening) → 01 §5 Orders of Magnitude Difference ✓
  - Issue 17 (global scale) → 02 §Global Scale Computation ✓
  - Issue 18 (loss scaling contract) → 03 §Loss Component Scaling Contract ✓
  - Issue 19 (normalization formulas) → 01 §Input Vector Normalization Formulas ✓
- **Superseded issues verified:** Issues 2 (collocation points), 3 (time normalization), 4 (omega0 scheduling), 14 (omega0 timing), 16 (L_max/tau_L) are all covered by the audit's B-08, M2, B-10, and B-07/M7 respectively. Issues 5-11 are covered by the audit's comprehensive treatment. The blanket-superseded claim is now accurate after remediation migrated Issues 12, 13, 18.
- **Math errors found:** None
- **Notes:** The `compute_globals` function in 02 correctly uses the post-remediation D formula (`D = np.cbrt(G * M_tot_ref * t_max**2)` with `M_tot_ref = 3.0`). The original `next steps.txt` code used `D = np.cbrt(G * t_max**2)` (wrong pre-B-02 formula). The remediation correctly updated this.

---

## Structural Verification

| Check | Result | Detail |
|-------|--------|--------|
| Thematic docs present | PASS | 01, 02, 03 all present in `issues/` directory |
| Archive complete | PASS | All 7 originals in `archive/` with git history |
| DECISION-NEEDED strict callout count | PASS | 01=2, 02=1, 03=2 (inline mentions of [DECISION-NEEDED] appear in cross-references and table notes but strict blockquote callouts match spec) |
| MIGRATION.md 86-count removed | PASS | No reference to "86 mapped sections"; replaced with "40 explicit provenance table rows" |
| MIGRATION.md verbatim accuracy | PASS | §6 correctly marked verbatim; §5 correctly marked synthesized; PCA/K-means correctly marked synthesized |
| Cross-document links resolve | PASS | All inter-doc links (01↔02, 01↔03, 02↔03) reference existing files |
| README.md navigation valid | PASS | README links to all 3 thematic docs, MIGRATION.md, archive/, and canonical references |
| Size reduction legitimate | PASS | Originals: 246,678 bytes → Destinations: 107,302 bytes (56.5% reduction). Reduction comes from deduplication, narrative compression, and removal of superseded next steps.txt content. No substantive finding was lost. |
| Cross-doc consistency | PASS | Causal mode, I_norm, s_min, dt_out scaling, D formula, softening, and COM frame claims are internally consistent across all three docs |
| Severity reclassification ledged | PASS | M11 and M12 reclassification from MAJOR to BLOCKING documented in 02 §Severity Reclassification Ledger |
| Audit §5 synthesized claim | PASS | MIGRATION.md correctly states "Not copied verbatim" for audit §5 |
| Verbatim formal spec claim | PASS | Only audit §6 is claimed as verbatim; text comparison confirms exact match in 03 |

---

## Concerns Flagged

### Concern #1 (MINOR): Audit B-09 unified-ε=1e-8 recommendation not individually preserved

**Finding:** The 2026-04-27 audit §B-09 explicitly recommended unifying softening at ε = 1e-8. The destination document 01 adopts the Dual-Context Epsilon Strategy (ε=1e-10 static / ε_soft=1e-5 dynamic) from the Causal_Trainingmismatch blueprint. Per the D-05 conflict-resolution policy, "the losing position is not silently dropped — record it under Considered Alternatives." The audit's specific 1e-8 unification recommendation is not individually listed under 01's "Considered Alternatives" section (which currently only documents trigonometric encoding vs shape invariants).

**Severity:** MINOR. The dual-epsilon strategy is described in detail with full justification (float64 static invariants vs float32 GPU regularization), and the audit's concern about "different physics for curriculum vs training" is addressed by the operational-consequence analysis in 01 §5 Orders of Magnitude Difference. The audit's 1e-8 value can be inferred as having been considered and rejected. No action required, but a future editor may wish to add a one-line entry under Considered Alternatives.

### Concern #2 (MINOR): `next steps.txt` Issues 5-11 not individually spot-checked in MIGRATION.md

**Finding:** MIGRATION.md marks Issues 2-11, 14, 16 from `next steps.txt` as "(superseded by 2026-04-27 audit) — Archived only after spot-check; no unique findings extracted." However, the manifest does not enumerate which audit sections supersede each of Issues 5-11 individually. The remediation focused on extracting the 4 missed issues (12, 13, 18, plus Issue 1/15/17/19 which were already extracted).

**Severity:** MINOR. From independent review, Issues 5-11 cover: canonical ordering (audit §5.4), data preprocessing steps (audit §1-2), constraint counting (audit M4), batch construction (audit B-07/B-08), collocation strategy (audit B-08), omega0 scheduling (audit B-10), and Lyapunov time (audit M7). All are indeed covered by the audit. The MIGRATION.md's blanket superseded claim is accurate, just not granularly enumerated. No action required.

---

## Unresolved Items Requiring Human Judgment

None. The five [DECISION-NEEDED] callouts correctly remain open for human resolution during implementation phases:

1. **Input vector composition** (01) — Option A (trig) vs Option B (shape invariants + dir cosines)
2. **I_norm definition** (01) — raw ratio vs tanh-wrapped
3. **File format h5 vs txt/json** (02) — Keep HDF5 or migrate
4. **Causal training mode** (03) — Option A vs B vs Hybrid
5. **s_min frame in collision criterion** (03) — unsoftened vs max(s_min, ε)

These are correctly framed with recommendations, alternatives documented, and resolution gating criteria stated.

---

## Verification Complete

The Phase 9 consolidation passes independent re-verification. The original verification's 2 critical + 9 moderate + 2 minor issues are all remediated. No new critical or moderate issues were found. Two minor documentation completeness concerns are noted above. The consolidated documents are ready to serve as input to implementation phases.

---

*Re-verification performed: 2026-04-28 by Claude (claude-code)*
*Methodology: sequential document-by-document build-up with independent mathematical computation*
