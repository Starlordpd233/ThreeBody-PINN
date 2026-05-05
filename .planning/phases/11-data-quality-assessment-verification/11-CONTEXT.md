# Phase 11: Data-Quality-Assessment Verification - Context

**Gathered:** 2026-05-05
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify the data-quality-assessment markdown conversion against its LaTeX source section-by-section, select the best of 2 candidates, strip injected `[@refN]` citations not present in the source, fix HTML table corruption, archive the unselected candidate, and produce `pinn_instruction/markdown_conversion/data_quality_assessment.md` as the authoritative one-to-one faithful markdown reproduction.

This phase follows the Phase 10 audit→fix→verify→archive pattern. The source is simpler than CTL: no comment blocks, no author notes, zero citations in the LaTeX body, only 2 tables, only 1 `\label`.

In scope:
- Compare the 2 markdown candidates against the 6 active LaTeX source sections.
- Rank candidates by diff score with human sanity-check override.
- Strip all `[@refN]` inline citations — the LaTeX body has zero citations.
- Convert HTML tables to clean GitHub-flavored markdown tables, verified cell-by-cell.
- Audit the selected candidate section-by-section.
- Fix markdown conversion discrepancies only.
- Preserve LaTeX source content faithfully.
- Archive the unselected candidate with provenance.
- Update the shared markdown conversion index.

Out of scope:
- bibliography.tex — orphaned source file (never imported by main.tex), excluded entirely.
- Editing LaTeX source files.
- Reconciling data-quality-assessment with other instruction documents.
- Building automated verification tooling (deferred to v2).
</domain>

<decisions>
## Implementation Decisions

### Candidate Baseline (carried from Phase 10)
- **D-01:** Rank both markdown candidates by diff score before selecting a baseline.
- **D-02:** Perform a human sanity-check of the top-ranked candidate before editing. Human inspection can override the raw score.
- **D-03:** Candidate comparison report must include both overall and per-section scores.
- **D-04:** Normalize away formatting-only noise (whitespace, line wrapping, harmless escaping). Do not normalize content, math, reference, table, or hierarchy changes.

### Citation Handling (new — Phase 11 specific)
- **D-27:** Strip all `[@refN]` inline citations from the markdown body. The LaTeX source body has zero `\cite{}` commands — any citations in the markdown are post-conversion additions. The body must match the LaTeX source exactly.
- **D-28:** bibliography.tex is excluded from audit scope entirely. It is never `\input`'d by main.tex, contains 33 `\bibitem` entries never cited in the body, and is not mentioned in the verification report.

### Table Handling (new — Phase 11 specific)
- **D-29:** Convert all HTML `<table>` markup to clean GitHub-flavored markdown tables. Verify cell-by-cell against the LaTeX source. The 2 tables in `assessment_strategy.tex` are the only tables affected.

### Comment and Exclusion Policy (carried from Phase 10, vacuously satisfied)
- **D-05 through D-09:** The data-quality-assessment source has no `\begin{comment}` environments and no `\authcomment{…}` author notes. These policies carry forward but require no action.

### Audit Workflow (carried from Phase 10)
- **D-10:** Audit the selected candidate section-by-section in source order (6 active sections).
- **D-11:** Each section audit records a pass/fail summary plus a discrepancy table.
- **D-12:** Discrepancy rows include type, severity, source location, markdown location, and fix status.
- **D-13:** Severity labels: `BLOCKING`, `MAJOR`, `MINOR`, `INFO`.
- **D-14:** Math-heavy sections require a formula-by-formula checklist. The data-quality-assessment source has significant math content in `data_quality_metrics.tex` and other sections.
- **D-15:** Final verification requires zero open discrepancies plus a fix log.

### Correction Authority (carried from Phase 10)
- **D-16:** Apply markdown-only corrections. LaTeX is ground truth.
- **D-17:** Preserve suspected source-level issues exactly in the markdown body; document them in the appended metadata section.
- **D-18:** Source-level issue notes live in a clearly separated `Source Issues / Notes for Future Reconciliation` section at the end of the markdown.
- **D-19:** The appended source-issues section is metadata — excluded from fidelity comparison.
- **D-20:** Fix discrepancies with small section-scoped edits, not whole-file rewrites.
- **D-21:** Log every fix with discrepancy ID, section, and fix summary.

### Report and Archive Layout (adapted from Phase 10)
- **D-30:** Authoritative filename: `pinn_instruction/markdown_conversion/data_quality_assessment.md`.
- **D-31:** Verification reports live in `pinn_instruction/markdown_conversion/verification_reports/`. Phase 11 report: `verification_reports/data_quality_assessment_verification_report.md`. Phase 10's report was moved here for consistency.
- **D-32:** Unselected candidate archived to `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/` with a `README.md` documenting provenance and why it was not selected.
- **D-33:** Audit scope: 6 active sections only. bibliography.tex excluded (D-28).
- **D-26:** Update `pinn_instruction/markdown_conversion/README.md` index with the Phase 11 row.

### Claude's Discretion
- Exact diff-score implementation and normalization details (per D-04 constraints).
- Exact markdown table format (GitHub-flavored, with alignment pipes).
- Exact verification report filename and structure within `verification_reports/`.
- Exact discrepancy ID format, as long as IDs map from audit table to fix log.
- Whether the top-level or pandoc candidate wins mechanical diff scoring — determined by measurement, not preference.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Context
- `.planning/PROJECT.md` — v1.3 milestone goal, active markdown-conversion requirements, source-of-truth boundaries.
- `.planning/REQUIREMENTS.md` — v1.3 requirement IDs: `CAND-01`, `AUDIT-*`, `FIDEL-*`, `CLEAN-*`, `CROSS-*`. Phase 11 covers exactly these requirements.
- `.planning/ROADMAP.md` — Phase 11 goal, dependencies, success criteria, "cross-reference heavy" annotation (note: actual source has minimal refs — 1 label, 0 cites).
- `.planning/STATE.md` — current milestone state, Phase 10 complete.
- `.planning/phases/10-ctl-instruction-verification/10-CONTEXT.md` — established the audit→fix→verify→archive pattern that Phase 11 follows exactly.
- `.planning/phases/10-ctl-instruction-verification/10-01-SUMMARY.md` through `10-03-SUMMARY.md` — Phase 10 execution records for reference on plan structure and task breakdown.

### Data-Quality-Assessment LaTeX Source
- `pinn_instruction/original_latex/Data-quality-assessment/main-data-quality-assess.tex` — source entry point and canonical section order (6 sections imported; bibliography.tex NOT imported).
- `pinn_instruction/original_latex/Data-quality-assessment/sections/introduction.tex` — section 1.
- `pinn_instruction/original_latex/Data-quality-assessment/sections/assessment_strategy.tex` — section 2; contains the only 2 tables and the only `\label`.
- `pinn_instruction/original_latex/Data-quality-assessment/sections/data_quality_metrics.tex` — section 3; heavy math content.
- `pinn_instruction/original_latex/Data-quality-assessment/sections/model_parameter_risks.tex` — section 4.
- `pinn_instruction/original_latex/Data-quality-assessment/sections/implementation_protocol.tex` — section 5.
- `pinn_instruction/original_latex/Data-quality-assessment/sections/synthesis_conclusion.tex` — section 6.
- `pinn_instruction/original_latex/Data-quality-assessment/sections/bibliography.tex` — orphaned; NOT imported by main.tex. Excluded from audit scope per D-28.

### Markdown Candidates
- `pinn_instruction/markdown_conversion/assess_data_quality.md` — top-level candidate (394 lines). Contains HTML-corrupted table, no inline citations, disconnected reference list at end.
- `pinn_instruction/markdown_conversion/pandoc_conversion/data_quality_assess.md` — pandoc candidate (390 lines). Clean pandoc multiline table, 17 `[@refN]` inline citations injected into body.

### Output Locations
- `pinn_instruction/markdown_conversion/data_quality_assessment.md` — final authoritative markdown (D-30).
- `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` — verification report (D-31).
- `pinn_instruction/markdown_conversion/README.md` — shared index to update with Phase 11 row.
- `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md` — archive provenance README (D-32).
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The data-quality-assessment source is already modularized into 7 files under `sections/`, 6 of which are active. Phase 11 audits in exact source order without inventing section boundaries.
- The 2 markdown candidates already exist and are very close in size (394 vs 390 lines), suggesting similar conversion quality at a high level.
- Phase 10 established the complete audit→fix→verify→archive pattern with 3 plans (candidate selection, audit, fix+verify). Phase 11 reuses this structure.

### Established Patterns
- Documentation work uses plain Markdown, not a documentation framework.
- Verification reports live in `verification_reports/` subdirectory (established during Phase 11 context — Phase 10's report moved here for consistency).
- Phase 9/10 use `BLOCKING / MAJOR / MINOR / INFO` severity labels.
- LaTeX sources are ground truth; markdown gets corrected, never the reverse.
- One phase per LaTeX source, same audit→fix→verify→report cycle.

### Integration Points
- `pinn_instruction/markdown_conversion/data_quality_assessment.md` becomes the canonical markdown artifact for this source.
- `pinn_instruction/markdown_conversion/README.md` gains a Phase 11 row — the index grows with each completed phase.
- `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/` keeps the unselected candidate inspectable.

### Known Caveats
- The ROADMAP describes this phase as "cross-reference heavy" but the source has only 1 `\label` and 0 `\cite` commands. The audit should not over-invest in cross-reference checking — it's a minor aspect of this source.
- Both candidates have reference material not in the LaTeX source. The strip-all policy (D-27) means both candidates need citation removal regardless of which wins the diff-score comparison.
- The pandoc candidate has injected `[@refN]` citations in the body text; the top-level candidate has a disconnected reference list at the end. Both are fidelity violations.
</code_context>

<specifics>
## Specific Ideas

- Treat Phase 11 as a faster iteration of the Phase 10 pattern — the source is simpler (no comments, fewer refs, fewer candidates, 6 active sections vs 8).
- The HTML table corruption in the top-level candidate is the most visible bug to fix. The pandoc candidate's table is already correct, which may influence human sanity-check scoring.
- Citation stripping is a new discrepancy category not seen in Phase 10 — both candidates inject reference content absent from the LaTeX source. This is a conversion fidelity issue distinct from math/text/table/hierarchy errors.
- The two candidates are very close in size (394 vs 390 lines). Mechanical diff scoring may produce a near-tie, making the human sanity-check more important than in Phase 10 where candidates were clearly different.
</specifics>

<deferred>
## Deferred Ideas

- Fixing suspected source-level factual or methodological issues. Document in the appended metadata section, do not resolve.
- Cross-document reconciliation between data-quality-assessment and other instruction documents. v1.3 preserves source-specific content.
- Building automated markdown verification tooling. Deferred to v2.
- Resolving the question of whether the 33 references in bibliography.tex should be reconnected to the document body with proper `\cite{}` commands. That's a LaTeX source edit — outside v1.3 scope.
</deferred>

---

*Phase: 11-Data-Quality-Assessment Verification*
*Context gathered: 2026-05-05*
