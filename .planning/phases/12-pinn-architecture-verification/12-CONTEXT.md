# Phase 12: PINN-Architecture Verification - Context

**Gathered:** 2026-05-05
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify the PINN-architecture markdown conversion against its 7 active LaTeX source sections, select the best of 3 markdown candidates via diff-scoring and human sanity-check, confirm that all 3 inactive sections are properly excluded (no content leakage), correct markdown-only conversion discrepancies, archive the 2 unselected candidates with provenance, and produce `pinn_instruction/markdown_conversion/pinn_architecture.md` as the authoritative one-to-one faithful markdown reproduction of the active PINN-architecture source.

This phase follows the Phase 10/11 audit→fix→verify→archive→report pattern. The key distinction is the `%\input` exclusion mechanism: unlike Phase 10's `\begin{comment}` blocks, PINN-architecture uses LaTeX comments to exclude entire section files. This requires a different verification approach for inactive content absence.

In scope:
- Compare all 3 PINN-architecture markdown candidates against the 7 active LaTeX source sections.
- Select the best candidate using mechanical diff scoring plus human sanity-check with focus on inactive content leakage.
- Audit the selected candidate section-by-section in source order (7 active sections).
- Verify that all 3 inactive sections (`*_inactive.tex`) are absent from the final markdown.
- Fix markdown conversion discrepancies only.
- Preserve LaTeX source content faithfully, including suspected source-level issues.
- Fully audit bibliography.tex (it IS imported by main_pinn.tex, unlike Phase 11's orphaned bibliography).
- Archive 2 unselected candidates with provenance README.
- Add/update the markdown conversion index.

Out of scope:
- Documenting content of the 3 inactive section files.
- Editing PINN-architecture LaTeX source files.
- Fixing suspected factual, mathematical, or methodological issues in the converted body.
- Reconciling PINN-architecture with other instruction documents.
- Building a new markdown generation or verification pipeline.
- Auditing inactive sections for future reference — this phase confirms exclusion only.

</domain>

<decisions>
## Implementation Decisions

### Candidate Baseline (carried from Phase 10)
- **D-01:** Rank all 3 PINN-architecture markdown candidates by diff score before selecting a baseline.
- **D-02:** Perform a human sanity-check of the top-ranked candidate before editing. Human inspection can override the raw score when math, table, reference, structure fidelity, or inactive-content leakage is worse in the mechanically top-ranked file.
- **D-03:** Candidate comparison report must include both overall scores and per-section scores.
- **D-04:** Candidate scoring should normalize away formatting-only noise: whitespace, line wrapping, and harmless markdown escaping. Do not normalize away content changes, math changes, reference drift, table cell changes, hierarchy changes, or inactive-section content leakage.

### Inactive Section Exclusion (new — Phase 12 specific)
- **D-34:** Verify inactive section exclusion using a hybrid approach: (1) structural check that markdown section count/order matches the 7 active imports in main_pinn.tex, (2) content search for distinctive key terms from the 3 inactive files to confirm absence. The verification report explicitly lists the 3 inactive files and confirms each is absent.
- **D-35:** Inactive section content is NOT documented in the authoritative markdown's metadata section. The phase goal is exclusion verification, not content preservation. Future phases can audit inactive files separately if needed.
- **D-38:** The final verification report includes an explicit confirmation section: "Inactive Section Exclusion: All 3 inactive sections (input_vector_inactive.tex, advanced_training_inactive.tex, consolidated_blueprint_inactive.tex) are confirmed absent from the authoritative markdown."

### Comment and Exclusion Policy (adapted from Phase 10)
- **D-05 through D-09 (adapted):** PINN-architecture uses `%\input` file-level exclusion instead of `\begin{comment}` blocks. The verification mechanism changes (per D-34), but the policy remains: excluded content must be absent from the final markdown. The source has no `\authcomment{}` notes.

### Audit Workflow (carried from Phase 10)
- **D-10:** Audit the selected candidate section-by-section in source order (7 active sections).
- **D-11:** Each section audit records a pass/fail summary plus a discrepancy table.
- **D-12:** Discrepancy rows include type, severity, source location, markdown location, and fix status.
- **D-13:** Severity labels: `BLOCKING`, `MAJOR`, `MINOR`, `INFO`.
- **D-14:** Math-heavy sections require a formula-by-formula checklist. `physics_constrained_loss.tex` (15383 bytes) and `sqr_skipresnet_siren_backbone.tex` (11171 bytes) are the primary math-heavy sections.
- **D-15:** Final verification requires zero open discrepancies plus a fix log.

### Bibliography Handling (new — Phase 12 specific)
- **D-37:** bibliography.tex IS in audit scope (unlike Phase 11's orphaned bibliography). It is imported by main_pinn.tex (line 30) and contains `\bibitem` entries that require full fidelity verification. Verify all bibliography entries match.

### Correction Authority (carried from Phase 10)
- **D-16:** Apply markdown-only corrections. PINN-architecture LaTeX is ground truth.
- **D-17:** Preserve suspected source-level issues exactly in the markdown body; document them in the appended metadata section.
- **D-18:** Source-level issue notes live in a clearly separated `Source Issues / Notes for Future Reconciliation` section at the end of the markdown.
- **D-19:** The appended source-issues section is metadata — excluded from fidelity comparison.
- **D-20:** Fix discrepancies with small section-scoped edits, not whole-file rewrites.
- **D-21:** Log every fix with discrepancy ID, section, and fix summary.

### Report and Archive Layout (adapted from Phase 10/11)
- **D-36:** Authoritative filename: `pinn_instruction/markdown_conversion/pinn_architecture.md` (lowercase, underscores, matching Phase 10/11 convention).
- **D-31:** Verification report lives in `pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md`.
- **D-32:** The 2 unselected candidates move to `pinn_instruction/markdown_conversion/_archive/pinn-architecture/` with a `README.md` documenting provenance and why each was not selected.
- **D-26:** Update `pinn_instruction/markdown_conversion/README.md` with the Phase 12 row.

### Claude's Discretion
- Exact diff-score implementation and normalization details (per D-04 constraints).
- Exact search terms used for inactive content verification (per D-34 hybrid approach).
- Exact verification report filename and structure within `verification_reports/`.
- Exact discrepancy ID format, as long as IDs remain stable and map from audit table to fix log.
- Which candidate wins mechanical diff scoring — determined by measurement, not preference.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Context
- `.planning/PROJECT.md` — v1.3 milestone goal, active markdown-conversion requirements, source-of-truth boundaries, out-of-scope rules.
- `.planning/REQUIREMENTS.md` — v1.3 requirement IDs: `CAND-01`, `AUDIT-*`, `FIDEL-*`, `CLEAN-*`, `CROSS-*`. Phase 12 covers exactly these requirements.
- `.planning/ROADMAP.md` — Phase 12 goal, dependencies, success criteria, "inactive sections correctly excluded" annotation.
- `.planning/STATE.md` — current milestone state, Phases 10-11 complete.
- `.planning/phases/10-ctl-instruction-verification/10-CONTEXT.md` — established the audit→fix→verify→archive pattern and decision IDs D-01 through D-26.
- `.planning/phases/11-data-quality-assessment-verification/11-CONTEXT.md` — adapted the pattern for simpler source, established D-27 through D-33, verification_reports/ directory convention.
- `.planning/phases/10-ctl-instruction-verification/10-01-SUMMARY.md` through `10-03-SUMMARY.md` — Phase 10 execution records for reference on plan structure.
- `.planning/phases/11-data-quality-assessment-verification/11-01-SUMMARY.md` through `11-03-SUMMARY.md` — Phase 11 execution records for reference on plan structure.

### PINN-Architecture LaTeX Source
- `pinn_instruction/original_latex/pinn-architecture/main_pinn.tex` — source entry point showing canonical import order (7 active imports, 3 commented `%\input`).
- `pinn_instruction/original_latex/pinn-architecture/preamble.tex` — source macros and definitions.
- `pinn_instruction/original_latex/pinn-architecture/sections/foundational_principles.tex` — active section 1 (6270 bytes).
- `pinn_instruction/original_latex/pinn-architecture/sections/sqr_skipresnet_siren_backbone.tex` — active section 2 (11171 bytes), math-heavy.
- `pinn_instruction/original_latex/pinn-architecture/sections/physics_constrained_loss.tex` — active section 3 (15383 bytes), largest, heavy math on loss functions.
- `pinn_instruction/original_latex/pinn-architecture/sections/training_optimization_strategy.tex` — active section 4.
- `pinn_instruction/original_latex/pinn-architecture/sections/inference_and_output.tex` — active section 5.
- `pinn_instruction/original_latex/pinn-architecture/sections/blueprint_summary.tex` — active section 6.
- `pinn_instruction/original_latex/pinn-architecture/sections/bibliography.tex` — active section 7 (imported by main_pinn.tex, unlike Phase 11's orphaned bibliography).
- `pinn_instruction/original_latex/pinn-architecture/sections/input_vector_inactive.tex` — inactive (commented in main_pinn.tex line 16). NOT in audit scope.
- `pinn_instruction/original_latex/pinn-architecture/sections/advanced_training_inactive.tex` — inactive (commented in main_pinn.tex line 24). NOT in audit scope.
- `pinn_instruction/original_latex/pinn-architecture/sections/consolidated_blueprint_inactive.tex` — inactive (commented in main_pinn.tex line 26). NOT in audit scope.

### Markdown Candidates
- `pinn_instruction/markdown_conversion/pinn_architecture.md` — top-level candidate (52885 bytes).
- `pinn_instruction/markdown_conversion/pinn_architecture_v2.md` — second top-level candidate (46355 bytes).
- `pinn_instruction/markdown_conversion/pandoc_conversion/PINN_architecture_plan.md` — pandoc candidate (51268 bytes).

### Output Locations
- `pinn_instruction/markdown_conversion/pinn_architecture.md` — final authoritative markdown (D-36).
- `pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md` — verification report (D-31).
- `pinn_instruction/markdown_conversion/README.md` — shared index to update with Phase 12 row.
- `pinn_instruction/markdown_conversion/_archive/pinn-architecture/README.md` — archive provenance README (D-32).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The PINN-architecture source is already modularized with 10 section files in `sections/`, 7 active (imported by main_pinn.tex) and 3 inactive (commented). Phase 12 audits in exact source order without inventing section boundaries.
- The 3 markdown candidates already exist with varying sizes (52885, 46355, 51268 bytes). Larger candidates may contain inactive-section content — a key check during human sanity-score.
- Phase 10 established the complete audit→fix→verify→archive pattern with 3 plans. Phase 11 followed the same structure. Phase 12 reuses this proven workflow.

### Established Patterns
- Documentation work uses plain Markdown, not a documentation framework.
- Verification reports live in `verification_reports/` subdirectory (established Phase 11).
- Severity labels: `BLOCKING / MAJOR / MINOR / INFO`.
- LaTeX sources are ground truth; markdown gets corrected, never the reverse.
- One phase per LaTeX source, same audit→fix→verify→report cycle.
- Authoritative filenames use lowercase with underscores (ctl_instruction.md, data_quality_assessment.md).

### Integration Points
- `pinn_instruction/markdown_conversion/pinn_architecture.md` becomes the canonical PINN-architecture artifact.
- `pinn_instruction/markdown_conversion/README.md` gains a Phase 12 row — the index grows with each completed phase.
- `pinn_instruction/markdown_conversion/_archive/pinn-architecture/` keeps 2 unselected candidates inspectable.

### Key Distinction from Prior Phases
- Phase 10 had `\begin{comment}...\end{comment}` blocks for exclusion.
- Phase 12 has `%\input` file-level exclusion — different mechanism, same policy goal (excluded content absent).
- Phase 11's bibliography.tex was orphaned (not imported). Phase 12's bibliography.tex IS imported and requires full audit.

</code_context>

<specifics>
## Specific Ideas

- Treat inactive-section exclusion verification as the critical success criterion. The ROADMAP explicitly requires "no content leakage" — the human sanity-check should specifically look for section headings, key terms, or content from the 3 inactive files in each candidate.
- The `physics_constrained_loss.tex` section is the largest (15383 bytes) and likely contains the most complex math. Allocate extra formula-by-formula checklist time for this section.
- Candidate size ordering: pinn_architecture.md (52885) > pandoc (51268) > v2 (46355). If the largest candidate contains inactive content (leakage), the diff score may penalize it appropriately, but human sanity-check should confirm.
- The bibliography.tex IS imported by main_pinn.tex (line 30). Unlike Phase 11 where bibliography.tex was excluded, this bibliography must be audited for all `\bibitem` entry fidelity.

</specifics>

<deferred>
## Deferred Ideas

- Documenting the content of the 3 inactive section files in the authoritative markdown's metadata. Phase 12 confirms exclusion only — content preservation for inactive files belongs in a future phase if needed.
- Fixing suspected source-level mathematical, factual, or methodological issues in PINN-architecture. Phase 12 documents these in the appended source-issues section, does not correct them.
- Cross-document reconciliation between PINN-architecture and other instruction documents (CTL, sampling-method, data-quality-assessment, review-of-framework, stage-strategy-revision). v1.3 preserves source-specific content.
- Building shared automated markdown-verification tooling for all 6 documents. Deferred to v2.
- Auditing the 3 inactive section files for future reference. Phase 12 scope is exclusion verification only.

</deferred>

---

*Phase: 12-PINN-Architecture Verification*
*Context gathered: 2026-05-05*