# Migration Manifest

Per-section provenance map tracing every major heading from the 7 archived originals to their destination(s) in the 3 consolidated thematic docs.

**Doc keys:** `01` = 01-architecture-and-physics-foundations.md, `02` = 02-data-pipeline-and-validation.md, `03` = 03-curriculum-and-training-loop.md

---

## three_body_pinn_pre-implementation_audit_2026-04-27.md (archived)

| Original section | Destination | Notes |
|---|---|---|
| Executive Summary | 01, 02, 03 §Executive Summary | Synthesized |
| §1 Critical Issues B-01..B-11 | 01 §Confirmed Findings (B-01..B-05, B-09, B-10); 02 §Confirmed Findings (B-06, B-11); 03 §Confirmed Findings (B-07, B-08) | Synthesized |
| §2 Major Inconsistencies M1..M16 | 01 §Confirmed Findings (M1-M5, M8-M10); 02 §Confirmed Findings (M11-M13); 03 §Confirmed Findings (M6-M7, M14-M16) | Synthesized |
| §3 Design Ambiguities D1..D10 | 01 §Confirmed Findings (D1-D4, D6, D8-D10); 02 §Confirmed Findings (D7); 03 §Confirmed Findings (D5) | Synthesized |
| §4 Author-Flagged Uncertainties | 01, 02, 03 §Confirmed Findings | Synthesized |
| §5 Corrected Input Vector Specification | 01 §Recommended Input Vector Specification; 01 §Considered Alternatives | Synthesized/reconciled. Audit Option A trig encoding is preserved as a considered alternative; the consolidated recommended spec uses Option B shape invariants + direction cosines. Not copied verbatim. |
| §6 Unified Batch Construction Specification | 03 §Verbatim Reference Specification | Copied verbatim |
| §7 Implementation Checklist | 03 §Implementation Checklist; 01, 02 §Recommended Resolutions | Synthesized |
| §8 Cross-Issue Interaction Matrix | README.md; 01, 02, 03 §Cross-Issue Interactions | Synthesized |
| §9 Quantitative Impact Summary | 01 §Quantitative Impact of D Formula Error | Synthesized |

**Unique findings preserved:**
- [x] B-01..B-11, M1..M16, D1..D10, 28 author uncertainties → distributed across 01/02/03
- [x] §5 input vector spec reconciled (→ 01); §6 verbatim batch construction (→ 03)
- [x] §7 Implementation Checklist P0..P4 (→ 03); §9 Quantitative Impact (→ 01)

---

## Causal_Trainingmismatch_resolution_blueprint.md (archived)

| Original section | Destination | Notes |
|---|---|---|
| Introduction, Dataset Pipeline | 01, 02, 03 §Executive Summary | Synthesized |
| Architectural Mismatch, Causal Failure, ALM, Firewall | 03 §Causal Training Mismatch; §ALM Parameter Update Spec | Synthesized |
| Resolution: Time-Windowed Causal-ALM Hybrid | 03 §Resolution: Time-Windowed Causal-ALM Hybrid | Synthesized |
| Architectural/Dataset Inconsistencies | 01 §Open Decisions, §Dual-Context Epsilon; 02 §Temporal Resolution Bridging | Synthesized |
| Validation Metrics (SCS, SASD, IPR, PSC) | 02 §Symplectic Conservation Score et seq. | Synthesized |
| Synthesized Curriculum Training Protocol | 03 §Training Phases | Synthesized |
| Conclusion, Works Cited | — | Archived only |

**Unique findings preserved:**
- [x] Time-Windowed Causal-ALM Hybrid (→ 03)
- [x] Shape invariants vs trig encoding (→ 01 §Considered Alternatives)
- [x] Dual-Context Epsilon: eps=1e-10 static, eps_soft=1e-5 dynamic (→ 01)
- [x] SCS/SASD/IPR/PSC as live training parameters (→ 02)
- [x] Galilean boost mandate + temporal resolution bridging (→ 01, 02, 03)

---

## Issue_on_data_validation_protocol_and_compatbility_with_project_context.md (archived)

| Original section | Destination | Notes |
|---|---|---|
| Documents analysed | — | Archived only |
| Gaps identified | 02 §Data Validation Protocol — 6-Gap Analysis | Synthesized |
| Gaps resolved by PINN/CTL docs | 02 §Data Validation Protocol | Synthesized |
| Causal training mismatch | 03 §Causal Training Mismatch | Synthesized |
| Minor clarifications | 02 §Validation Thresholds; 01, 03 §Open Decisions | Synthesized |
| Recommended information package | — | Archived only |

**Unique findings preserved:**
- [x] Option A vs B causal training (→ 03)
- [x] 6-gap analysis + resolution table (→ 02)
- [x] Overfit Challenge precision, 14D input authority, gold-standard thresholds (→ 02)

---

## review.md (archived)

| Original section | Destination | Notes |
|---|---|---|
| Scaling contract, AD chain-rule, three-layer separation, derivative rules | 01 §AD Chain-Rule Factor | Synthesized; derivative rules verbatim |

**Unique findings preserved:**
- [x] AD chain-rule factor missing (physics residual 4x off, KE 4x off) (→ 01)
- [x] Three-layer separation: raw → physics-scaled → network-input (→ 01)
- [x] Derivative conversion rules (→ 01, verbatim)

---

## stage-assignment-issue.txt (archived)

| Original section | Destination | Notes |
|---|---|---|
| Evaluation, Research, Redesigned Section 2.3, Workflow | 03 §Data-Driven Adaptive Stage Assignment §Methodology | Synthesized |
| PCA, K-means, stage assignment code | 03 §Data-Driven Adaptive Stage Assignment | Synthesized |

**Unique findings preserved:**
- [x] Data-driven adaptive stage assignment: PCA + K-means + quantiles (→ 03)
- [x] Python code for EDA, clustering, adaptive assignment (→ 03)
- [x] Hybrid physical + empirical distributions approach (→ 03)

---

## next-step-for-data-processing-pipeline.txt (archived)

| Original section | Destination | Notes |
|---|---|---|
| Data stratification methodology | 03 §Data-Driven Adaptive Stage Assignment | Merged |
| h5 vs txt/json format | 02 §File Format: h5 vs txt/json | Synthesized |
| Data preprocessing steps | 02 §DataLoader Requirements | Synthesized |
| I_norm text-vs-code | 01 §Input Vector Normalization; §Open Decisions | Synthesized |
| 12 author-flagged \authcomment items | 01, 02, 03 §Open Decisions | Synthesized |
| Grok: COM transformation | 01 §Frame Convention: Galilean Boost | Merged with B-05, M3 |

**Unique findings preserved:**
- [x] h5 vs txt/json (→ 02); I_norm text-vs-code (→ 01)
- [x] COM transform order + 12 \authcomment items (→ 01, 02, 03)

---

## next steps.txt (archived)

| Original section | Destination | Notes |
|---|---|---|
| Issue 1: tau_L and L_max formula | 03 §tau_L and L_max Formula Resolution | Extracted |
| Issues 2–11, 14, 16 | — | Archived only; superseded by audit |
| Issue 12: AD velocities/accelerations | 01 §Explicit AD Implementation Requirement | Extracted |
| Issue 13: Huber loss parameter | 03 §Huber Delta for Normalized Energy | Extracted |
| Issue 15: Softening (5-OoM) | 01 §5 Orders of Magnitude Difference | Extracted |
| Issue 17: Global scale computation | 02 §Global Scale Computation | Extracted |
| Issue 18: Loss components | 03 §Loss Component Scaling Contract | Extracted |
| Issue 19: Normalization formulas | 01 §Input Vector Normalization Formulas | Extracted |

**Unique findings preserved:**
- [x] Issue 1: tau_L/L_max formulas + Python (→ 03)
- [x] Issue 15: softening 5-OoM analysis (→ 01)
- [x] Issue 17: compute_globals pseudo-code (→ 02)
- [x] Issue 12: component-wise AD derivatives (→ 01)
- [x] Issue 13: Huber δ calibration (→ 03)
- [x] Issue 18: loss-component scaling contract (→ 03)
- [x] Issue 19: normalization formulas table (→ 01)

---

## Summary

| Metric | Count |
|--------|-------|
| Archived originals | 7 |
| Destination thematic docs | 3 |
| Explicit provenance table rows | 40 |
| Verbatim-copied formal specs | 1 (`three_body_pinn_pre-implementation_audit_2026-04-27.md` §6) |
| Unique findings preserved | 36 |

All 7 originals archived with git history in `archive/`. The manifest now avoids unverifiable aggregate section counts and records non-verbatim synthesis explicitly.
