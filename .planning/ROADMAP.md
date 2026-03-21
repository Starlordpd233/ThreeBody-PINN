# Roadmap: 3-Body Problem Physics-Informed LLM

## Milestones

- **v1.0 Codebase Cleanup** - Phases 1-4 (shipped 2026-03-20)
- **v1.1 LaTeX Modularization Verification** - Phases 5-8 (in progress)

## Phases

v1.0 Codebase Cleanup (Phases 1-4) - SHIPPED 2026-03-20

- [x] Phase 1: Code Rewrites and Validation (3/3 plans) - completed 2026-03-18
- [x] Phase 2: Documentation Updates (3/3 plans) - completed 2026-03-19
- [x] Phase 3: Data Deletion and Legacy Cleanup (2/2 plans) - completed 2026-03-19
- [x] Phase 4: Stale Reference Fixes (2/2 plans) - completed 2026-03-20

### v1.1 LaTeX Modularization Verification (In Progress)

**Milestone Goal:** Rigorously verify that 5 modular LaTeX structures faithfully preserve the content, style, format, and components of their original monolithic LaTeX files via automated Python diffing scripts.

- [x] **Phase 5: Content Completeness Verification** - Automated diff confirms no content lost or added across all 5 structures (completed 2026-03-21)
- [x] **Phase 6: Preamble Parity Verification** - Package, macro, and command declarations match between original and modular preambles (completed 2026-03-21)
- [ ] **Phase 7: Structure Fidelity Verification** - Section hierarchy, labels, references, citations, and floats preserved across all 5 structures
- [ ] **Phase 8: Compilability Verification** - All 5 modular structures compile cleanly with 0 errors and 0 warnings

## Phase Details

### Phase 5: Content Completeness Verification
**Goal**: User can confirm that every line of content from the original monolithic .tex files is present in the modular sections, and no extraneous content was introduced
**Depends on**: Phase 4
**Requirements**: CONT-01, CONT-02, CONT-03
**Success Criteria** (what must be TRUE):
  1. Running a single script produces a diff report for all 5 structures comparing original monolithic .tex against concatenated modular sections
  2. Any lines present in the original but missing from modular output are identified with file name, line number, and surrounding context
  3. Any lines present in modular output but absent from the original are identified with file name, line number, and surrounding context
  4. When content is fully preserved, the report clearly states "no differences found" per structure
**Plans**: 1 plan

Plans:
- [x] 05-01-PLAN.md - Create verify_content.py script and run verification for all 5 structures

### Phase 6: Preamble Parity Verification
**Goal**: User can confirm that every package, macro, and command definition from the original preamble exists in the modular preamble for all 5 structures
**Depends on**: Phase 5
**Requirements**: PREAMB-01, PREAMB-02, PREAMB-03
**Success Criteria** (what must be TRUE):
  1. Running a script reports all `\usepackage` declarations found in the original and whether each appears in the modular preamble
  2. All custom command definitions (`\newcommand`, `\renewcommand`, `\newenvironment`) from the original are verified present in the modular preamble
  3. Package options (e.g., `[H]` for float, encoding options, font sizes) are compared exactly, with mismatches flagged
**Plans**: 1 plan

Plans:
- [x] 06-01-PLAN.md - Create verify_preamble.py script and run preamble parity verification for all 5 structures

### Phase 7: Structure Fidelity Verification
**Goal**: User can confirm that the structural LaTeX elements (section hierarchy, cross-references, citations, and float environments) are faithfully preserved in modular output for all 5 structures
**Depends on**: Phase 5
**Requirements**: STRUCT-01, STRUCT-02, STRUCT-03, STRUCT-04, STRUCT-05
**Success Criteria** (what must be TRUE):
  1. A report shows section/subsection hierarchy from both original and modular output side by side, with any ordering or nesting differences flagged
  2. Every `\label` declaration from the original is confirmed present in the modular sections, with missing labels listed
  3. Every `\ref`, `\eqref`, `\autoref`, `\cite`, and bibliography command from the original is confirmed present in the modular sections, with missing references listed
  4. Every float environment (`\begin{figure}`, `\begin{table}`, `\begin{longtable}`) and its content are confirmed preserved, with missing or altered floats listed
**Plans**: 2 plans

Plans:
- [x] 07-01-PLAN.md - Create verify_structure.py script to extract and verify structural elements (sections, labels, refs, citations, floats) for all 5 structures
- [x] 07-02-PLAN.md - Fix structural fidelity gaps (ctl-instruction section ordering, pinn-architecture float content)

### Phase 8: Compilability Verification
**Goal**: User can confirm that every modular structure compiles to PDF without errors or unexpected warnings
**Depends on**: Phase 6, Phase 7
**Requirements**: COMP-01, COMP-02
**Success Criteria** (what must be TRUE):
  1. A script compiles all 5 modular structures with pdflatex (or lualatex) and reports pass/fail per structure with 0 errors required for pass
  2. Warning count per structure is reported, and any warnings not present in the original compilation are flagged as new
**Plans**: 1 plan

Plans:
- [ ] 08-01-PLAN.md - Create verify_compile.py script to compile all 5 structures with latexmk and compare warnings against originals

## Progress

**Execution Order:**
Phases execute in numeric order: 5 -> 6 -> 7 -> 8
(Phases 6 and 7 both depend on Phase 5 but are independent of each other; Phase 8 depends on both 6 and 7)

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Code Rewrites and Validation | v1.0 | 3/3 | Complete | 2026-03-18 |
| 2. Documentation Updates | v1.0 | 3/3 | Complete | 2026-03-19 |
| 3. Data Deletion and Legacy Cleanup | v1.0 | 2/2 | Complete | 2026-03-19 |
| 4. Stale Reference Fixes | v1.0 | 2/2 | Complete | 2026-03-20 |
| 5. Content Completeness Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 6. Preamble Parity Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 7. Structure Fidelity Verification | v1.1 | 2/2 | Complete | 2026-03-21 |
| 8. Compilability Verification | v1.1 | 0/1 | Not started | - |