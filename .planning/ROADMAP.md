# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- **v1.0 Codebase Cleanup** - Phases 1-4 (shipped 2026-03-20)
- **v1.1 LaTeX Modularization Verification** - Phases 5-8 (shipped 2026-03-22)
- **v1.2 PINN Implementation Readiness** - Phase 9 (in progress)
- **v1.3 Markdown Conversion Verification & Correction** - Phases 10-15 (planning)

## Phases

### v1.0-v1.2 (Shipped / In Progress)

<details>
<summary>v1.0 Codebase Cleanup (Phases 1-4) — SHIPPED 2026-03-20</summary>

- [x] Phase 1: Code Rewrites and Validation (3/3 plans) - completed 2026-03-18
- [x] Phase 2: Documentation Updates (3/3 plans) - completed 2026-03-19
- [x] Phase 3: Data Deletion and Legacy Cleanup (2/2 plans) - completed 2026-03-19
- [x] Phase 4: Stale Reference Fixes (2/2 plans) - completed 2026-03-20

</details>

<details>
<summary>v1.1 LaTeX Modularization Verification (Phases 5-8) — SHIPPED 2026-03-22</summary>

- [x] **Phase 5: Content Completeness Verification** - Automated diff confirms no content lost or added across all 5 structures (completed 2026-03-21)
- [x] **Phase 6: Preamble Parity Verification** - Package, macro, and command declarations match between original and modular preambles (completed 2026-03-21)
- [x] **Phase 7: Structure Fidelity Verification** - Section hierarchy, labels, references, citations, and floats preserved across all 5 structures (completed 2026-03-21)
- [x] **Phase 8: Compilability Verification** - All 5 modular structures compile cleanly with 0 errors and 0 new warnings (completed 2026-03-22)

</details>

<details>
<summary>v1.2 PINN Implementation Readiness (Phase 9) — IN PROGRESS</summary>

- [ ] **Phase 9: Issues Directory Consolidation** - Reorganize 7 files into 3 thematic documents with migration tracking

</details>

### v1.3 Markdown Conversion Verification & Correction (Phases 10-15)

**Milestone Goal:** Verify every markdown conversion against its LaTeX source section-by-section, fix all errors to achieve one-to-one injection fidelity, and produce one authoritative `.md` file per source document.

- [ ] **Phase 10: CTL-Instruction Verification** - 8 sections, 3 markdown candidates, heavy math — hardest first to validate the approach
- [ ] **Phase 11: Data-Quality-Assessment Verification** - 7 sections, 2 markdown candidates, cross-reference heavy
- [ ] **Phase 12: PINN-Architecture Verification** - 7 active + 3 inactive sections, 3 markdown candidates, comment exclusion
- [ ] **Phase 13: Review-of-Framework Verification** - 7 sections, 1 pandoc candidate, sub-document structure
- [ ] **Phase 14: Stage-Strategy-Revision Verification** - 6 sections, 1 pandoc candidate, table normalization
- [ ] **Phase 15: Sampling-Method Verification** - Monolithic source, 2 markdown candidates, split-on-section-boundaries

## Phase Details

### Prior Milestones (v1.0-v1.2)

<details>
<summary>Phases 1-9 details (click to expand)</summary>

### Phase 5: Content Completeness Verification
**Goal**: User can confirm that every line of content from the original monolithic .tex files is present in the modular sections
**Depends on**: Phase 4
**Requirements**: CONT-01, CONT-02, CONT-03
**Success Criteria** (what must be TRUE):
  1. Running a single script produces a diff report for all 5 structures
  2. Missing lines identified with file name, line number, and context
  3. Extraneous lines identified with file name, line number, and context
  4. Report clearly states "no differences found" per structure when complete
**Plans**: 1 plan
- [x] 05-01-PLAN.md

### Phase 6: Preamble Parity Verification
**Goal**: Every package, macro, and command definition from original preamble exists in modular preamble
**Depends on**: Phase 5
**Requirements**: PREAMB-01, PREAMB-02, PREAMB-03
**Success Criteria** (what must be TRUE):
  1. Script reports all `\usepackage` declarations with presence checks
  2. All custom command definitions verified present
  3. Package options compared exactly, mismatches flagged
**Plans**: 1 plan
- [x] 06-01-PLAN.md

### Phase 7: Structure Fidelity Verification
**Goal**: Structural LaTeX elements faithfully preserved in modular output
**Depends on**: Phase 5
**Requirements**: STRUCT-01, STRUCT-02, STRUCT-03, STRUCT-04, STRUCT-05
**Success Criteria** (what must be TRUE):
  1. Section hierarchy compared side by side with differences flagged
  2. Every `\label` confirmed present in modular sections
  3. Every `\ref`, `\cite`, and bibliography command confirmed present
  4. Every float environment and content confirmed preserved
**Plans**: 2 plans
- [x] 07-01-PLAN.md
- [x] 07-02-PLAN.md

### Phase 8: Compilability Verification
**Goal**: Every modular structure compiles to PDF without errors or unexpected warnings
**Depends on**: Phase 6, Phase 7
**Requirements**: COMP-01, COMP-02
**Success Criteria** (what must be TRUE):
  1. Script compiles all 5 structures and reports pass/fail with 0 errors required for pass
  2. Warning count reported; warnings not present in original flagged as new
**Plans**: 1 plan
- [x] 08-01-PLAN.md

### Phase 9: Issues Directory Consolidation
**Goal:** Reorganize 7 scattered issue reports into 2-3 thematic documents eliminating duplication
**Depends on**: None
**Requirements**: CONSOL-01, CONSOL-02, CONSOL-03
**Success Criteria** (what must be TRUE):
  1. All 7 existing files merged into 2-3 new thematic files
  2. No unique findings lost in consolidation
  3. Each thematic document has distinct purpose with no overlapping coverage
  4. Original files archived or deleted with migration note
**Plans**: 3 plans
- [ ] 09-01-PLAN.md
- [ ] 09-02-PLAN.md
- [ ] 09-03-PLAN.md

</details>

### Phase 10: CTL-Instruction Verification
**Goal**: The ctl-instruction markdown is the authoritative, one-to-one faithful reproduction of its LaTeX source — all formulas, text, references, tables, and structure match exactly
**Depends on**: Phase 9 completion (v1.2 prerequisite)
**Requirements**: CAND-01, AUDIT-01, AUDIT-02, AUDIT-03, FIDEL-01, FIDEL-02, FIDEL-03, FIDEL-04, FIDEL-05, FIDEL-06, CLEAN-01, CLEAN-02, CLEAN-03, CROSS-01, CROSS-02
**Success Criteria** (what must be TRUE):
  1. User can inspect a diff-score comparison report showing all 3 markdown candidates ranked, with the best candidate selected and rationale documented
  2. User can open the verification report and see every discrepancy found across all 8 sections, categorized by type (math/text/ref/table/hierarchy/comment) with exact locations
  3. User can compare the corrected markdown against the LaTeX source section-by-section and observe zero meaningful differences (comment blocks excluded)
  4. User can find the 2 unselected markdown files archived in `_archive/` with a README documenting provenance and why they were not chosen
  5. User can read the final verification report confirming zero-diff status with a complete fix log
**Plans**: TBD
**UI hint**: no

### Phase 11: Data-Quality-Assessment Verification
**Goal**: The data-quality-assessment markdown is the authoritative, one-to-one faithful reproduction of its LaTeX source — all cross-references, citations, tables, and prose match exactly
**Depends on**: Phase 10
**Requirements**: CAND-01, AUDIT-01, AUDIT-02, AUDIT-03, FIDEL-01, FIDEL-02, FIDEL-03, FIDEL-04, FIDEL-05, FIDEL-06, CLEAN-01, CLEAN-02, CLEAN-03, CROSS-01, CROSS-02
**Success Criteria** (what must be TRUE):
  1. User can inspect a diff-score comparison report showing both markdown candidates ranked, with the best candidate selected and rationale documented
  2. User can open the verification report and see every discrepancy found across all 7 sections, categorized by type with exact locations — with special attention to cross-reference and citation fidelity
  3. User can compare the corrected markdown against the LaTeX source section-by-section and observe zero meaningful differences (comment blocks excluded)
  4. User can find the unselected markdown file archived in `_archive/` with a README documenting provenance
  5. User can read the final verification report confirming zero-diff status with a complete fix log
**Plans**: TBD
**UI hint**: no

### Phase 12: PINN-Architecture Verification
**Goal**: The pinn-architecture markdown is the authoritative, one-to-one faithful reproduction of its LaTeX source active sections — with commented-out and inactive sections correctly excluded
**Depends on**: Phase 10
**Requirements**: CAND-01, AUDIT-01, AUDIT-02, AUDIT-03, FIDEL-01, FIDEL-02, FIDEL-03, FIDEL-04, FIDEL-05, FIDEL-06, CLEAN-01, CLEAN-02, CLEAN-03, CROSS-01, CROSS-02
**Success Criteria** (what must be TRUE):
  1. User can inspect a diff-score comparison report showing all 3 markdown candidates ranked, with the best candidate selected and rationale documented
  2. User can open the verification report and confirm that all 3 inactive sections (`*_inactive.tex`) are properly excluded from the markdown — no content leakage
  3. User can compare the corrected markdown against the 7 active LaTeX sections and observe zero meaningful differences
  4. User can find the 2 unselected markdown files archived in `_archive/` with a README documenting provenance
  5. User can read the final verification report confirming zero-diff status with explicit confirmation of inactive section exclusion
**Plans**: TBD
**UI hint**: no

### Phase 13: Review-of-Framework Verification
**Goal**: The review-of-framework markdown (single sub-document) is the authoritative, one-to-one faithful reproduction of its LaTeX source
**Depends on**: Phase 10
**Requirements**: CAND-02, AUDIT-01, AUDIT-02, AUDIT-03, FIDEL-01, FIDEL-02, FIDEL-03, FIDEL-04, FIDEL-05, FIDEL-06, CLEAN-01, CLEAN-03, CROSS-01, CROSS-02
**Success Criteria** (what must be TRUE):
  1. User can confirm the single pandoc candidate was used as the starting point — no candidate selection needed
  2. User can open the verification report and see every discrepancy found across all 7 sections, categorized by type with exact locations
  3. User can compare the corrected markdown against the LaTeX source section-by-section and observe zero meaningful differences
  4. User can read the final verification report confirming zero-diff status with a complete fix log
**Plans**: TBD
**UI hint**: no

### Phase 14: Stage-Strategy-Revision Verification
**Goal**: The stage-strat-revision markdown is the authoritative, one-to-one faithful reproduction of its LaTeX source — with tables verified cell-by-cell
**Depends on**: Phase 10
**Requirements**: CAND-02, AUDIT-01, AUDIT-02, AUDIT-03, FIDEL-01, FIDEL-02, FIDEL-03, FIDEL-04, FIDEL-05, FIDEL-06, CLEAN-01, CLEAN-03, CROSS-01, CROSS-02
**Success Criteria** (what must be TRUE):
  1. User can confirm the single pandoc candidate was used as the starting point — no candidate selection needed
  2. User can open the verification report and see every discrepancy found across all 6 sections, with tables verified cell-by-cell for correct content, structure, and formatting
  3. User can compare the corrected markdown against the LaTeX source section-by-section and observe zero meaningful differences
  4. User can read the final verification report confirming zero-diff status with a complete fix log
**Plans**: TBD
**UI hint**: no

### Phase 15: Sampling-Method Verification
**Goal**: The sampling-method markdown is the authoritative, one-to-one faithful reproduction of its monolithic LaTeX source
**Depends on**: Phase 10
**Requirements**: CAND-01, AUDIT-01, AUDIT-02, AUDIT-03, FIDEL-01, FIDEL-02, FIDEL-03, FIDEL-04, FIDEL-05, FIDEL-06, CLEAN-01, CLEAN-02, CLEAN-03, CROSS-01, CROSS-02
**Success Criteria** (what must be TRUE):
  1. User can inspect a diff-score comparison report showing both markdown candidates ranked, with the best candidate selected and rationale documented
  2. User can open the verification report and see every discrepancy found across all logical sections (split on `\section` boundaries) of the monolithic source, categorized by type with exact locations
  3. User can compare the corrected markdown against the LaTeX source and observe zero meaningful differences
  4. User can find the unselected markdown file archived in `_archive/` with a README documenting provenance
  5. User can read the final verification report confirming zero-diff status with a complete fix log
**Plans**: TBD
**UI hint**: no

## Execution Order

**Phases execute in numeric order:** 10 -> 11 -> 12 -> 13 -> 14 -> 15

Phases 11-15 all depend on Phase 10 (hardest first to validate the approach). Phases 11-15 are otherwise independent of each other but execute sequentially to allow incremental refinement of the audit pattern.

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Code Rewrites and Validation | v1.0 | 3/3 | Complete | 2026-03-18 |
| 2. Documentation Updates | v1.0 | 3/3 | Complete | 2026-03-19 |
| 3. Data Deletion and Legacy Cleanup | v1.0 | 2/2 | Complete | 2026-03-19 |
| 4. Stale Reference Fixes | v1.0 | 2/2 | Complete | 2026-03-20 |
| 5. Content Completeness Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 6. Preamble Parity Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 7. Structure Fidelity Verification | v1.1 | 2/2 | Complete | 2026-03-21 |
| 8. Compilability Verification | v1.1 | 1/1 | Complete | 2026-03-22 |
| 9. Issues Directory Consolidation | v1.2 | 0/3 | Not Started | — |
| 10. CTL-Instruction Verification | v1.3 | 3/3 | Complete   | 2026-05-02 |
| 11. Data-Quality-Assessment Verification | v1.3 | 0/TBD | Not Started | — |
| 12. PINN-Architecture Verification | v1.3 | 0/TBD | Not Started | — |
| 13. Review-of-Framework Verification | v1.3 | 0/TBD | Not Started | — |
| 14. Stage-Strategy-Revision Verification | v1.3 | 0/TBD | Not Started | — |
| 15. Sampling-Method Verification | v1.3 | 0/TBD | Not Started | — |

---
*Last updated: 2026-05-01 — v1.3 roadmap defined*
