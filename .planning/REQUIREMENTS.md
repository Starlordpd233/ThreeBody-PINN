# Requirements: Three-Body LaTeX Markdown Conversion Verification

**Defined:** 2026-04-30
**Core Value:** Simulation dataset and data pipeline are clean, validated, and correctly processed

## v1.3 Requirements

Requirements for markdown conversion verification and correction. Each maps to a roadmap phase.

### Candidate Selection

- [x] **CAND-01**: For each LaTeX source with multiple markdown candidates, automated diff-score comparison selects the best starting candidate (fewest diff lines against source)
- [ ] **CAND-02**: Sources with only one markdown candidate (review-of-framework, stage-strat-revision) skip selection and use the existing file directly

### Audit & Comparison

- [ ] **AUDIT-01**: Section-by-section manual comparison of LaTeX source against markdown for all 6 source documents
- [ ] **AUDIT-02**: Every discrepancy found during audit is documented in a per-phase verification report with section location, type (math/text/ref/table/hierarchy/comment), and severity
- [x] **AUDIT-03**: Comparison explicitly excludes `\begin{comment}...\end{comment}` blocks from the LaTeX source before comparison

### Content Fidelity

- [ ] **FIDEL-01**: Every mathematical formula from the LaTeX source appears in the markdown with accurate notation and correct rendering (no missing terms, no altered symbols, no whitespace corruption)
- [ ] **FIDEL-02**: All prose text, lists, code blocks, and inline formatting match the LaTeX source exactly — no dropped sentences, no added content, no paraphrasing
- [ ] **FIDEL-03**: All `\ref`, `\cite`, `\label`, and bibliography references from the LaTeX source are preserved in the markdown with correct target identifiers
- [ ] **FIDEL-04**: All tables are verified cell-by-cell for correct content, structure, and formatting
- [ ] **FIDEL-05**: Section/subsection/paragraph hierarchy in markdown matches the LaTeX source structure exactly
- [ ] **FIDEL-06**: Commented-out content (`\begin{comment}...\end{comment}` blocks) is absent from the markdown; intentionally excluded sections (e.g., pinn-architecture `_inactive.tex` files) are confirmed excluded

### Cleanup & Authority

- [x] **CLEAN-01**: Each of the 6 LaTeX sources has exactly one authoritative markdown file when its phase completes
- [ ] **CLEAN-02**: Unselected duplicate markdown files are archived to an `_archive/` directory with a README explaining provenance
- [ ] **CLEAN-03**: Each phase produces a verification report documenting: candidate selected and why, all discrepancies found (with locations), all fixes applied, and final zero-diff confirmation

### Cross-Cutting

- [ ] **CROSS-01**: Inter-document inconsistencies in the LaTeX sources are preserved in the markdown — do NOT reconcile or resolve differences between source documents
- [ ] **CROSS-02**: The 6 phases execute sequentially; each phase is independent (different source document) but follows the same audit→fix→verify pattern

## v2 Requirements

Deferred to future release.

### Automation

- **AUTO-01**: Shared `md_verification_utils.py` utility module with section splitting, math extraction, reference extraction, normalization, and diff functions
- **AUTO-02**: Automated verification scripts for each of the 6 source documents
- **AUTO-03**: CI-compatible pass/fail exit codes for automated re-verification after future LaTeX edits

### Cross-Document

- **CROSS-03**: Cross-document consistency audit — identify and catalog inconsistencies between the 6 instruction documents
- **CROSS-04**: Resolve identified inconsistencies across documents (requires domain expert decisions)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Automated verification scripts | User chose manual comparison for this milestone; defer to v2 |
| Pandoc re-conversion of LaTeX sources | Destroys manual corrections already applied; verification is fix-in-place |
| Cross-document consistency checking | Explicitly excluded — inter-document inconsistencies are preserved |
| AI/LLM-based discrepancy detection | Non-deterministic; task is mechanical text comparison |
| PDF visual comparison | Compilation success is already verified (Phase 8); this is about source text fidelity |
| Modifying LaTeX source documents | LaTeX sources are the ground truth; only markdown gets fixed |
| Building a new markdown generation pipeline | This is verification and correction of existing files, not regeneration |

## Traceability

Which phases cover which requirements. Phase ranges indicate cross-cutting requirements verified in every phase. Specific phase numbers indicate requirements that apply only to certain phases.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CAND-01 | 10, 11, 12, 15 | Complete |
| CAND-02 | 13, 14 | Pending |
| AUDIT-01 | 10-15 | Pending |
| AUDIT-02 | 10-15 | Pending |
| AUDIT-03 | 10-15 | Complete |
| FIDEL-01 | 10-15 | Pending |
| FIDEL-02 | 10-15 | Pending |
| FIDEL-03 | 10-15 | Pending |
| FIDEL-04 | 10-15 | Pending |
| FIDEL-05 | 10-15 | Pending |
| FIDEL-06 | 10-15 | Pending |
| CLEAN-01 | 10-15 | Complete |
| CLEAN-02 | 10, 11, 12, 15 | Pending |
| CLEAN-03 | 10-15 | Pending |
| CROSS-01 | 10-15 | Pending |
| CROSS-02 | 10-15 | Pending |

**Coverage:**
- v1.3 requirements: 16 total
- Mapped to phases: 16/16 (100%)
- Unmapped: 0

**Mapping notes:**
- **CAND-01** (multi-candidate selection): Applies to Phases 10, 11, 12, 15 — documents with 2-3 competing markdown files
- **CAND-02** (single-candidate skip): Applies to Phases 13, 14 — documents with only pandoc conversions, no selection needed
- **CLEAN-02** (archive unselected): Applies to Phases 10, 11, 12, 15 — only phases with multiple candidates have files to archive
- All other requirements apply to every phase (10-15) — each phase performs the full audit→fix→verify→report cycle

---
*Requirements defined: 2026-04-30*
*Last updated: 2026-05-01 — traceability filled from ROADMAP.md*
