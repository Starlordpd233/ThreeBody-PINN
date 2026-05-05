# Phase 13: Review-of-Framework Verification - Context

**Gathered:** 2026-05-05
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify the single pandoc markdown candidate (`pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md`, 533 lines) against the 7 active LaTeX sub-document sections under `pinn_instruction/original_latex/review-of-framework/review_of_framework/`, correct markdown-only conversion discrepancies, and produce `pinn_instruction/markdown_conversion/review_of_framework.md` as the authoritative one-to-one faithful markdown reproduction.

This phase follows the Phase 10/11/12 audit→fix→verify pattern. The key distinctions are: (a) only one markdown candidate exists — CAND-02 applies, no diff-scoring or `_archive/` needed; (b) the source is structurally simpler than Phases 10–12 with no comment blocks, no inactive sections, no citations, and no bibliography; (c) the LaTeX source is nested two directories deep under a parent (`review-of-framework/`) shared with Phase 14's stage-strategy-revision sub-document.

In scope:
- Validate the single pandoc candidate as the starting baseline (no ranking required).
- Audit the candidate section-by-section in source order against the 7 active sections.
- Fix markdown conversion discrepancies only.
- Preserve LaTeX source content faithfully, including any suspected source-level issues.
- Produce a verification report with explicit "Vacuous Policy Checks" confirming the absence of comment blocks, inactive sections, citations, and bibliography entries in the source.
- Write the authoritative markdown to `pinn_instruction/markdown_conversion/review_of_framework.md`.
- Add a Phase 13 row to `pinn_instruction/markdown_conversion/README.md` indicating the parent dir `review-of-framework/` (shared with Phase 14).

Out of scope:
- Editing review-of-framework LaTeX source files.
- Fixing suspected factual, mathematical, or methodological issues in the converted body.
- Reconciling review-of-framework with other instruction documents.
- Auditing the sibling `stage_strat_revision/` sub-document (that is Phase 14).
- Building a new markdown generation or verification pipeline.
- Executing Phase 13 before Phase 12 final verification is complete (treated as soft prerequisite — planning may proceed).

</domain>

<decisions>
## Implementation Decisions

### Single-Candidate Baseline (Phase 13 specific — CAND-02)
- **D-39:** Use `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md` as the starting baseline directly. CAND-02 applies — no diff-score ranking against other candidates is needed because no other candidates exist.
- **D-40:** No `_archive/` directory is created for Phase 13. CLEAN-02 does not apply because there are no losing candidates to archive. The verification report explicitly notes "Single pandoc candidate; CLEAN-02 N/A" so future readers do not look for missing archive contents.
- **D-41:** Plan structure mirrors Phases 10–12 (3 plans): P1 candidate validation + report skeleton (provenance note in lieu of ranking), P2 section-by-section audit + fixes, P3 promotion + index update + final verification. Decision rationale: muscle memory from prior phases outweighs the modest savings of collapsing to 2 plans, and a separate "validation + report skeleton" plan keeps the provenance note auditable.
- **D-42:** P1 produces a "Starting Candidate Provenance" note (not a ranking report) recording: source file path, file size, line count, conversion tool (pandoc), date observed, and confirmation that CAND-02 applies.

### Authoritative Filename and Location
- **D-43:** Authoritative filename: `pinn_instruction/markdown_conversion/review_of_framework.md` (lowercase with underscores, matches the source subdirectory name `review_of_framework/`). Aligns with the lowercase_underscore convention from D-23/D-30/D-36 and creates filename symmetry with the source dir structure.
- **D-44:** Verification report filename: `pinn_instruction/markdown_conversion/verification_reports/review_of_framework_verification_report.md` (matches the established `verification_reports/` location from D-31).

### Sub-Document Index Handling (Phase 13 specific)
- **D-45:** `pinn_instruction/markdown_conversion/README.md` uses a flat index (one row per phase). Phase 13 row: title "Review of Framework", links to `review_of_framework.md` and the verification report. The row's metadata column notes "LaTeX parent dir: `review-of-framework/` (shared with Phase 14: stage-strategy-revision)" so readers see the source grouping without nested README structure.
- **D-46:** Do NOT create a grouped/nested section in the README for Phase 13+14. The flat index is preferred for symmetry with Phases 10–12 rows and to keep the index readable as Phases 14–15 are added.

### Vacuous Policy Verification (Phase 13 specific)
- **D-47:** The verification report includes an explicit "Vacuous Policy Checks" subsection that confirms by inspection:
  - 0 `\begin{comment}...\end{comment}` blocks in the 7 active source sections (D-05/D-09 vacuously satisfied).
  - 0 `\authcomment{}` author notes (D-06/D-07 vacuously satisfied).
  - 0 inactive section files (D-34/D-35/D-38 vacuously satisfied — no `*_inactive.tex` exist).
  - 0 `\cite{}` commands and 0 `\bibitem` entries in the 7 active sources (D-27/D-28/D-37 vacuously satisfied — no bibliography file imported).
- **D-48:** If the pandoc candidate is found to inject `[@refN]` or other citation-like artifacts not present in the source, treat them as conversion fidelity issues per D-27's strip-policy and remove them. Document the count and locations in the verification report.

### Phase Ordering and Phase 12 Status
- **D-49:** Phase 12 execution is in progress (12-03 plan not yet complete) at the time of Phase 13 context gathering. Following the same precedent as Phase 10's acknowledgment of incomplete Phase 9, Phase 13 context gathering and planning may proceed, but Phase 13 EXECUTION should treat Phase 12 final verification as the prerequisite gate per ROADMAP dependency ordering.

### Carried Forward (will not re-decide)

#### From Phase 10 (D-01–D-26)
- Audit→fix→verify pattern, severity labels (BLOCKING/MAJOR/MINOR/INFO), per-section pass/fail tables, discrepancy rows with type+severity+source-loc+md-loc+fix-status, formula-by-formula checklists for math-heavy sections, markdown-only corrections, ground-truth status of LaTeX source, `Source Issues / Notes for Future Reconciliation` metadata section appended to the authoritative markdown, small section-scoped edits over rewrites, fix log mapping discrepancy IDs to fixes, lowercase_underscore filename convention, README index update.

#### From Phase 11 (D-27, D-29–D-33)
- D-27 strip-injected-citations policy (vacuously satisfied for source; applied to candidate if injected).
- D-29 GFM table format (applies if any HTML tables found in candidate — to be verified during audit).
- D-31 `verification_reports/` subdir convention.
- D-33 audit scope is active sections only (vacuously: no inactive sections to exclude here).

#### From Phase 12 (D-34, D-35, D-38)
- Inactive-section absence verification methodology (vacuously satisfied — no inactive sections in source).

### Claude's Discretion
- Exact wording of the "Vacuous Policy Checks" subsection within the verification report.
- Exact format of the "Starting Candidate Provenance" note in P1 output.
- Exact text of the parent-dir metadata column entry in the README index row.
- Exact discrepancy ID format, as long as IDs remain stable and map from audit table to fix log (consistent with D-12).
- Whether to surface line-count or byte-count comparisons in the audit (either is acceptable evidence).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Context
- `.planning/PROJECT.md` — v1.3 milestone goal, active markdown-conversion requirements (MD-CONV-04 covers Phase 13), source-of-truth boundaries, out-of-scope rules.
- `.planning/REQUIREMENTS.md` — v1.3 requirement IDs covered by Phase 13: `CAND-02`, `AUDIT-01`, `AUDIT-02`, `AUDIT-03`, `FIDEL-01`–`FIDEL-06`, `CLEAN-01`, `CLEAN-03`, `CROSS-01`, `CROSS-02`. CLEAN-02 is N/A for this phase (single candidate).
- `.planning/ROADMAP.md` — Phase 13 goal, dependencies (Phase 10), success criteria.
- `.planning/STATE.md` — current milestone state; Phase 12 in progress at time of Phase 13 context gathering.
- `.planning/phases/10-ctl-instruction-verification/10-CONTEXT.md` — established the audit→fix→verify→archive pattern and decision IDs D-01–D-26.
- `.planning/phases/11-data-quality-assessment-verification/11-CONTEXT.md` — established `verification_reports/` subdir, citation-strip policy D-27, simpler-source workflow patterns; D-30, D-31, D-32, D-33 directly reused (with D-32 N/A for single-candidate Phase 13).
- `.planning/phases/12-pinn-architecture-verification/12-CONTEXT.md` — most recent Phase 10/11 derivative; D-34/D-35/D-38 inactive-section policy carries forward (vacuously satisfied here).
- `.planning/phases/10-ctl-instruction-verification/10-01-SUMMARY.md` through `10-03-SUMMARY.md` — Phase 10 execution records for plan structure reference.
- `.planning/phases/11-data-quality-assessment-verification/11-01-SUMMARY.md` through `11-03-SUMMARY.md` — Phase 11 execution records for plan structure reference.

### Review-of-Framework LaTeX Source (Sub-Document)
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex` — source entry point showing canonical import order (7 active `\input` directives, no commented imports).
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/preamble.tex` — source macros and definitions.
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/executive_summary.tex` — active section 1 (~16 lines).
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/foundational_physical_metrics.tex` — active section 2 (~129 lines, math-heavy).
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/data_scaling_normalization.tex` — active section 3 (~100 lines).
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/architectural_initialization_refinements.tex` — active section 4 (~27 lines).
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/multi_component_loss_framework.tex` — active section 5 (~116 lines, math-heavy).
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/training_sampling_strategy.tex` — active section 6 (~98 lines).
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/conclusion_and_recommendations.tex` — active section 7 (~27 lines).

### Markdown Candidate (Single)
- `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md` — pandoc candidate (533 lines). Used directly as starting baseline per CAND-02 / D-39.

### Output Locations
- `pinn_instruction/markdown_conversion/review_of_framework.md` — final authoritative markdown (D-43).
- `pinn_instruction/markdown_conversion/verification_reports/review_of_framework_verification_report.md` — verification report (D-44).
- `pinn_instruction/markdown_conversion/README.md` — shared index to update with Phase 13 row including parent-dir metadata (D-45).

### Sibling Sub-Document (Phase 14 — context only, NOT in audit scope)
- `pinn_instruction/original_latex/review-of-framework/stage_strat_revision/` — Phase 14's source. Shares parent dir `review-of-framework/`. Mentioned in Phase 13's README index row metadata but not audited here.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The review-of-framework source is already modularized with 7 active section files in `sections/`, all imported by `review_of_framework.tex`. No commented `\input` directives. Phase 13 audits in exact source order without inventing section boundaries.
- Only one markdown candidate exists (the pandoc conversion, 533 lines). Source totals ~513 lines across 7 sections — candidate is roughly the same scale, suggesting reasonable conversion fidelity at first glance.
- Phases 10/11/12 established the complete audit→fix→verify pattern. Phase 13 reuses the structure with single-candidate adaptations (D-39–D-42).

### Established Patterns
- Documentation work uses plain Markdown, not a documentation framework.
- Verification reports live in `verification_reports/` subdirectory (Phase 11 / D-31).
- Severity labels: `BLOCKING / MAJOR / MINOR / INFO`.
- LaTeX sources are ground truth; markdown gets corrected, never the reverse.
- One phase per LaTeX source/sub-document, same audit→fix→verify→report cycle.
- Authoritative filenames use lowercase with underscores (`ctl_instruction.md`, `data_quality_assessment.md`, `pinn_architecture.md`, now `review_of_framework.md`).

### Integration Points
- `pinn_instruction/markdown_conversion/review_of_framework.md` becomes the canonical artifact for this sub-document.
- `pinn_instruction/markdown_conversion/README.md` gains a Phase 13 row indicating shared parent dir with Phase 14's eventual `stage_strat_revision.md`.
- No `_archive/` directory created for Phase 13 (single candidate; D-40).

### Key Distinctions from Prior Phases
- Single-candidate workflow (CAND-02) — Phase 13 is the first v1.3 phase to skip diff-scoring/ranking. Phase 14 will follow the same pattern.
- Sub-document parent-dir structure — Phase 13 source is two directories deep, unlike Phases 10–12 single-level sources. README index row carries parent-dir metadata to disambiguate.
- Vacuous policy load — no comment blocks, no inactive sections, no citations, no bibliography. The verification report explicitly documents these absences (D-47).

</code_context>

<specifics>
## Specific Ideas

- Treat Phase 13 as the simplest v1.3 phase by structural complexity: single candidate, simple source, no exclusion mechanics. The audit should still be thorough — simplicity reduces volume of work, not rigor of comparison.
- The source has 2 math-heavy sections (`foundational_physical_metrics.tex` ~129 lines and `multi_component_loss_framework.tex` ~116 lines). Allocate formula-by-formula checklist time to these per D-14.
- The pandoc candidate has ~533 lines vs source ~513 lines, a 4% size delta. Roughly comparable scale suggests conversion fidelity is in the right ballpark, but per-section line counts should be sanity-checked during P1.
- The "Starting Candidate Provenance" note replaces the multi-candidate ranking report from Phases 10–12. Keep it short — one paragraph plus a small data table is sufficient.
- The README index row should make the parent-dir relationship discoverable without forcing readers into nested navigation. A simple metadata column ("LaTeX parent: review-of-framework/") suffices.
- Watch for pandoc-injected reference artifacts (`[@refN]`, footnote-style numerics) in the candidate even though the source has no citations — D-27/D-48 explicitly cover this.

</specifics>

<deferred>
## Deferred Ideas

- Reconciling review-of-framework with other instruction documents (CTL, sampling-method, data-quality-assessment, pinn-architecture, stage-strategy-revision). v1.3 preserves source-specific content; cross-document reconciliation is deferred to a separate future task.
- Auditing the sibling `stage_strat_revision/` sub-document — that is explicitly Phase 14's scope, not Phase 13.
- Fixing suspected source-level mathematical, factual, or methodological issues in review-of-framework. Phase 13 documents these in the appended `Source Issues / Notes for Future Reconciliation` section per D-17/D-18 but does not correct them.
- Building shared automated markdown-verification tooling for all 6 documents. Deferred to v2 per REQUIREMENTS.md AUTO-01/02/03.
- Producing a unified parent-doc README under `pinn_instruction/original_latex/review-of-framework/` that describes the relationship between the two sub-documents. Out of scope for v1.3 — markdown_conversion/README.md is the discoverability layer.

</deferred>

---

*Phase: 13-Review-of-Framework Verification*
*Context gathered: 2026-05-05*
