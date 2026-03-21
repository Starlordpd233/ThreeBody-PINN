# Requirements: Three-Body LaTeX Modularization Verification

**Defined:** 2026-03-21
**Core Value:** Simulation dataset and data pipeline are clean, validated, and correctly processed

## v1.1 Requirements

Requirements for LaTeX modularization verification. Each maps to roadmap phases.

### Content Completeness

- [x] **CONT-01**: Automated script compares original monolithic .tex against concatenated modular sections with whitespace normalization for all 5 structures
- [x] **CONT-02**: Dropped-line report identifies any lines present in original but missing from modular sections, with surrounding context
- [x] **CONT-03**: No extraneous content report identifies any lines in modular sections not present in original

### Preamble Parity

- [x] **PREAMB-01**: All `\usepackage` declarations from original preamble appear in modular preamble for each structure
- [x] **PREAMB-02**: All custom `\newcommand`, `\renewcommand`, `\newenvironment` definitions preserved
- [x] **PREAMB-03**: Package options (e.g., `[H]` for float, encoding options) match exactly

### Structure Fidelity

- [x] **STRUCT-01**: Section/subsection hierarchy in modular output matches original for all 5 structures
- [x] **STRUCT-02**: All `\label` declarations from original are present in modular sections
- [x] **STRUCT-03**: All `\ref`, `\eqref`, `\autoref` references from original are present in modular sections
- [x] **STRUCT-04**: All `\cite` and `\bibliography`/`\printbibliography` references preserved
- [x] **STRUCT-05**: All figure/table float environments (`\begin{figure}`, `\begin{table}`, `\begin{longtable}`) preserved with their content

### Compilability

- [ ] **COMP-01**: Each of the 5 modular structures compiles with `pdflatex` (or `lualatex`) with 0 errors
- [ ] **COMP-02**: Each of the 5 modular structures compiles with 0 warnings (or only pre-existing warnings from the original)

## Future Requirements

None — this is a standalone verification milestone.

## Out of Scope

| Feature | Reason |
|---------|--------|
| PDF visual diff (pixel-level) | Compilation success + content parity is sufficient |
| Page count comparison | User explicitly excluded |
| sampling-method verification | No modular structure exists for it |
| Fixing any issues found | This milestone only identifies issues; fixes are separate |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CONT-01 | Phase 5 | Complete |
| CONT-02 | Phase 5 | Complete |
| CONT-03 | Phase 5 | Complete |
| PREAMB-01 | Phase 6 | Complete |
| PREAMB-02 | Phase 6 | Complete |
| PREAMB-03 | Phase 6 | Complete |
| STRUCT-01 | Phase 7 | Complete |
| STRUCT-02 | Phase 7 | Complete |
| STRUCT-03 | Phase 7 | Complete |
| STRUCT-04 | Phase 7 | Complete |
| STRUCT-05 | Phase 7 | Complete |
| COMP-01 | Phase 8 | Pending |
| COMP-02 | Phase 8 | Pending |

**Coverage:**
- v1.1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0

---
*Requirements defined: 2026-03-21*
*Last updated: 2026-03-21 after roadmap creation*
