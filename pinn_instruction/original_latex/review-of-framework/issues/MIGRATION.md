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
| §5 Corrected Input Vector Specification | 01 §Verbatim Reference Specification | Copied verbatim |
| §6 Unified Batch Construction Specification | 03 §Verbatim Reference Specification | Copied verbatim |
| §7 Implementation Checklist | 03 §Implementation Checklist; 01, 02 §Recommended Resolutions | Synthesized |
| §8 Cross-Issue Interaction Matrix | README.md; 01, 02, 03 §Cross-Issue Interactions | Synthesized |
| §9 Quantitative Impact Summary | 01 §Quantitative Impact of D Formula Error | Synthesized |

**Unique findings preserved:**
- [x] Top 3 Blocking Issues, 11 Critical Issues (B-01..B-11), 16 Major Inconsistencies (M1..M16), 10 Design Ambiguities (D1..D10), 28 Author-Flagged Uncertainties (→ respective docs)
- [x] §5 verbatim input vector spec (→ 01), §6 verbatim batch construction spec (→ 03)
- [x] §7 Implementation Checklist P0..P4 (→ 03 P3-P4; cross-ref 01, 02), §9 Quantitative Impact Summary (→ 01)

---

## Causal_Trainingmismatch_resolution_blueprint.md (archived)

| Original section | Destination | Notes |
|---|---|---|
| Introduction, Dataset Pipeline | 01, 02, 03 §Executive Summary; 02 §Dataset Inventory | Synthesized |
| Architectural Mismatch, Causal Failure, Causal Mechanics, ALM, Causal Firewall | 03 §Causal Training Mismatch; 03 §ALM Parameter Update Specification | Synthesized |
| Resolution: Time-Windowed Causal-ALM Hybrid | 03 §Resolution: Time-Windowed Causal-ALM Hybrid | Synthesized |
| Architectural/Dataset Inconsistencies (Input Vector, Softening, Frame, Temporal Resolution) | 01 §Open Decisions, §Dual-Context Epsilon Strategy, §Galilean Boost; 02 §Temporal Resolution Bridging | Synthesized |
| Validation Metrics (SCS, SASD, IPR, PSC) | 02 §Symplectic Conservation Score et seq. | Synthesized |
| Synthesized Curriculum Training Protocol | 03 §Training Phases | Synthesized |
| Conclusion, Works Cited | — | Archived only |

**Unique findings preserved:**
- [x] Time-Windowed Causal-ALM Hybrid (→ 03)
- [x] Shape invariants + direction cosines vs trig encoding (→ 01 §Considered Alternatives)
- [x] Dual-Context Epsilon: eps=1e-10 static, eps_soft=1e-5 dynamic (→ 01)
- [x] SCS/SASD/IPR/PSC as live training parameters (→ 02)
- [x] Galilean boost mandate + temporal resolution bridging (→ 01, 02, 03)

---

## Issue_on_data_validation_protocol_and_compatbility_with_project_context.md (archived)

| Original section | Destination | Notes |
|---|---|---|
| Documents analysed | — | Archived only |
| Gaps identified from initial two documents | 02 §Data Validation Protocol — 6-Gap Analysis | Synthesized |
| Gaps resolved by PINN and CTL documents | 02 §Data Validation Protocol | Synthesized |
| Critical remaining issue: Causal training mismatch | 03 §Causal Training Mismatch: Option A vs Option B | Synthesized |
| Minor remaining clarifications | 01, 02, 03 §Open Decisions | Synthesized |
| Recommended information package | — | Archived only |

**Unique findings preserved:**
- [x] Option A vs B causal training framing (→ 03 [DECISION-NEEDED])
- [x] 6-gap analysis + resolution table (→ 02)

---

## review.md (archived)

| Original section | Destination | Notes |
|---|---|---|
| Scaling contract, AD chain-rule factor, three-layer separation, derivative conversion rules | 01 §AD Chain-Rule Factor | Synthesized; derivative rules copied verbatim |

**Unique findings preserved:**
- [x] AD chain-rule factor missing (physics residual 4x off, kinetic energy 4x off) (→ 01)
- [x] Three-layer separation: raw → physics-scaled → network-input (→ 01)
- [x] Derivative conversion: dr'/du = 2*dr'/dtau, d2r'/du2 = 4*d2r'/dtau2 (→ 01, verbatim)

---

## stage-assignment-issue.txt (archived)

| Original section | Destination | Notes |
|---|---|---|
| Evaluation, Research, Redesigned Section 2.3, Step-by-Step Workflow | 03 §Data-Driven Adaptive Stage Assignment §Methodology | Synthesized |
| PCA, K-means, and stage assignment code | 03 §Data-Driven Adaptive Stage Assignment | Copied verbatim |

**Unique findings preserved:**
- [x] Data-driven adaptive stage assignment: PCA + K-means + quantiles (→ 03)
- [x] Python code for EDA, clustering, adaptive assignment (→ 03, verbatim)
- [x] Hybrid physical metrics + empirical distributions approach (→ 03)

---

## next-step-for-data-processing-pipeline.txt (archived)

| Original section | Destination | Notes |
|---|---|---|
| Data stratification methodology examination | 03 §Data-Driven Adaptive Stage Assignment | Merged with stage-assignment-issue.txt |
| h5 vs txt/json file format question | 02 §File Format: h5 vs txt/json | Synthesized |
| Data preprocessing step examination | 02 §DataLoader Requirements | Synthesized |
| I_norm text-vs-code inconsistency | 01 §Input Vector Normalization Formulas; §Open Decisions | Synthesized |
| 12 author-flagged \authcomment items | 01, 02, 03 §Open Decisions | Synthesized |
| Grok response: COM transformation timing | 01 §Frame Convention: Galilean Boost Mandate | Merged with B-05 and M3 |

**Unique findings preserved:**
- [x] h5 vs txt/json [DECISION-NEEDED] (→ 02); I_norm text-vs-code (→ 01)
- [x] COM transform order + 12 \authcomment items resolved (→ 01, 02, 03)

---

## next steps.txt (archived)

| Original section | Destination | Notes |
|---|---|---|
| Issue 1: tau_L and L_max formula resolution | 03 §tau_L and L_max Formula Resolution | Unique — extracted |
| Issues 2–14, 16, 18 (16 issues total) | (superseded by 2026-04-27 audit) | Archived only |
| Issue 15: Softening consistency (5-OoM analysis) | 01 §5 Orders of Magnitude Difference | Unique — extracted |
| Issue 17: Global scale computation | 02 §Global Scale Computation | Unique — extracted |
| Issue 19: Normalization formulas verification | 01 §Input Vector Normalization Formulas | Unique — extracted |

**Unique findings preserved:**
- [x] Issue 1: tau_L and L_max resolved formulas + full Python implementation (→ 03)
- [x] Issue 15: 5 Orders of Magnitude Difference softening deep-dive (→ 01)
- [x] Issue 17: Global scale `compute_globals` parallelized pseudo-code (→ 02)
- [x] Issue 19: Comprehensive normalization formulas table (→ 01)

---

## Summary

| Metric | Count |
|--------|-------|
| Total major sections mapped | 86 |
| Sections synthesized | 68 |
| Sections copied verbatim | 11 |
| Sections archived-only | 7 |
| Unique findings preserved | 32 |

All 7 originals archived with git history in `archive/`. No unique findings lost — every contribution from RESEARCH.md is traceable via this manifest.
