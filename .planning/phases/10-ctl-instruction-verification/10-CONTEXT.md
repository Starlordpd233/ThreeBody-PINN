# Phase 10: CTL-Instruction Verification - Context

**Gathered:** 2026-05-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify the CTL instruction markdown conversion against the CTL LaTeX source section-by-section, select the best starting markdown candidate, correct markdown-only conversion discrepancies, archive the two unselected candidates, and produce `pinn_instruction/markdown_conversion/ctl_instruction.md` as the authoritative one-to-one faithful markdown reproduction of the CTL source.

This phase is the first v1.3 phase, even though it is global Phase 10 in the roadmap. The user explicitly acknowledged that v1.2 Phase 9 is incomplete and currently being finished. Phase 10 context/planning may proceed, but Phase 10 execution should continue to treat Phase 9 final verification as the prerequisite gate from the roadmap.

In scope:
- Compare all 3 CTL markdown candidates against the CTL LaTeX source.
- Select the best candidate using mechanical diff scoring plus human sanity-check.
- Audit the selected candidate section-by-section against the 8 CTL source sections.
- Fix markdown conversion discrepancies only.
- Preserve LaTeX source content faithfully, including suspected source-level issues.
- Append source-level math/factual concerns to the authoritative markdown as clearly separated metadata.
- Archive unselected CTL markdown candidates with provenance.
- Add/update the markdown conversion index.

Out of scope:
- Editing CTL LaTeX source files.
- Fixing suspected factual, mathematical, or methodological issues in the converted body.
- Reconciling CTL with other instruction documents.
- Building a new markdown generation or verification pipeline.
- Executing Phase 10 before the Phase 9 prerequisite is verified.

</domain>

<decisions>
## Implementation Decisions

### Candidate Baseline
- **D-01:** Rank all 3 CTL markdown candidates by diff score before selecting a baseline.
- **D-02:** Perform a human sanity-check of the top-ranked candidate before editing. Human inspection can override the raw score when math, table, reference, or structure fidelity is worse in the mechanically top-ranked file.
- **D-03:** Candidate comparison report must include both overall scores and per-section scores.
- **D-04:** Candidate scoring should normalize away formatting-only noise: whitespace, line wrapping, and harmless markdown escaping. Do not normalize away content changes, math changes, reference drift, table cell changes, or hierarchy changes.

### Comment and Exclusion Policy
- **D-05:** Exclude LaTeX `\begin{comment}...\end{comment}` environments from the final authoritative markdown.
- **D-06:** Preserve visible `\authcomment{...}` author notes from the source in the markdown.
- **D-07:** Render preserved `\authcomment{...}` text as a visible markdown note/callout so the author-note status remains clear.
- **D-08:** Verification report must list excluded comment-environment ranges so omissions are auditable without copying excluded content into the final markdown.
- **D-09:** Commented-out section headings from excluded comment blocks must be absent entirely from the final markdown body: no headings, anchors, or placeholders.

### Audit Workflow
- **D-10:** Audit the selected CTL candidate section-by-section in source order, following the modular `.tex` sequence.
- **D-11:** Each section audit records a pass/fail summary plus a discrepancy table.
- **D-12:** Discrepancy rows include type, severity, source location, markdown location, and fix status.
- **D-13:** Severity labels are `BLOCKING`, `MAJOR`, `MINOR`, and `INFO`, matching the Phase 9 issue-doc convention.
- **D-14:** Math-heavy sections require a formula-by-formula checklist inside the section audit. Every displayed equation and important inline formula should be explicitly checked.
- **D-15:** Final verification evidence requires zero open discrepancies plus a fix log. Every recorded discrepancy must be closed or explicitly accepted as a non-issue.

### Correction Authority
- **D-16:** Apply markdown-only corrections. CTL LaTeX is the ground truth and must not be edited in Phase 10.
- **D-17:** If LaTeX contains a suspected factual or mathematical problem, preserve it exactly in the converted markdown body and document it separately for future reconciliation.
- **D-18:** Source-level issue notes live inside the authoritative markdown file, appended at the end in a clearly separated section such as `Source Issues / Notes for Future Reconciliation`.
- **D-19:** The converted source body remains one-to-one faithful to LaTeX. The appended source-issues section is metadata and must be excluded from fidelity comparison.
- **D-20:** Fix actual conversion discrepancies with small section-scoped edits, not whole-file rewrites.
- **D-21:** Log every conversion fix with discrepancy ID, section, and fix summary.

### Report and Archive Layout
- **D-22:** Final verification report lives next to the authoritative markdown in `pinn_instruction/markdown_conversion/`.
- **D-23:** The authoritative CTL markdown filename is `pinn_instruction/markdown_conversion/ctl_instruction.md`.
- **D-24:** The 2 unselected CTL candidates move to `pinn_instruction/markdown_conversion/_archive/ctl-instruction/`.
- **D-25:** Archive directory must include a `README.md` documenting candidate provenance, score, and why each archived file was not selected.
- **D-26:** Add or update `pinn_instruction/markdown_conversion/README.md` as the index pointing readers to the authoritative CTL markdown and its verification report. This index should be designed to scale to all 6 future authoritative markdowns.

### Claude's Discretion
- Exact diff-score implementation and normalization details, as long as formatting-only noise is normalized and content/math/ref/table/hierarchy changes are not hidden.
- Exact markdown callout format for `\authcomment{...}`, as long as it is plain Markdown and visibly distinct from normal prose.
- Exact verification report filename, as long as it lives next to `pinn_instruction/markdown_conversion/ctl_instruction.md` and is clearly linked from `pinn_instruction/markdown_conversion/README.md`.
- Exact discrepancy ID format, as long as IDs remain stable and map from audit table to fix log.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Context
- `.planning/PROJECT.md` — v1.3 milestone goal, active markdown-conversion requirements, source-of-truth boundaries, and out-of-scope rules.
- `.planning/REQUIREMENTS.md` — v1.3 requirement IDs: `CAND-*`, `AUDIT-*`, `FIDEL-*`, `CLEAN-*`, and `CROSS-*`.
- `.planning/ROADMAP.md` — Phase 10 goal, dependencies, success criteria, and execution order.
- `.planning/STATE.md` — current milestone state and explicit note that Phase 9 is pending final verification.
- `.planning/phases/09-issues-directory-consolidation/09-CONTEXT.md` — recent severity-label convention and current Phase 9 prerequisite context.
- `.planning/phases/08-compilability-verification/08-CONTEXT.md` — prior verification-report style and LaTeX source path conventions.
- `.planning/phases/07-structure-fidelity-verification/07-CONTEXT.md` — prior structure-fidelity checks, especially section/reference/float comparison patterns.

### CTL LaTeX Source
- `pinn_instruction/original_latex/ctl-instruction/main_CTL.tex` — CTL source entry point and canonical section order.
- `pinn_instruction/original_latex/ctl-instruction/preamble_CTL.tex` — source macros and comment/note definitions, including `\authcomment`.
- `pinn_instruction/original_latex/ctl-instruction/sections/01_intro.tex` — CTL section 1.
- `pinn_instruction/original_latex/ctl-instruction/sections/02_data_characterization.tex` — CTL section 2; contains comment environments and visible author notes.
- `pinn_instruction/original_latex/ctl-instruction/sections/03_data_glimpse.tex` — CTL section 3.
- `pinn_instruction/original_latex/ctl-instruction/sections/04_phase1_data_prep.tex` — CTL section 4; heavy math, labels, visible author notes, and comment environments.
- `pinn_instruction/original_latex/ctl-instruction/sections/05_phase2_training_loop.tex` — CTL section 5; training-loop math, tables, visible author notes, and comment environments.
- `pinn_instruction/original_latex/ctl-instruction/sections/06_advanced_considerations.tex` — CTL section 6.
- `pinn_instruction/original_latex/ctl-instruction/sections/07_reproducibility.tex` — CTL section 7.
- `pinn_instruction/original_latex/ctl-instruction/sections/appendix.tex` — CTL appendix; includes figure references and labels.

### Markdown Candidates
- `pinn_instruction/markdown_conversion/ctl_instruction.md` — existing top-level CTL candidate and target authoritative filename.
- `pinn_instruction/markdown_conversion/ctl_instruction_v2.md` — second top-level CTL candidate.
- `pinn_instruction/markdown_conversion/pandoc_conversion/CTL-instruction-final.md` — pandoc CTL candidate.

### Output Locations
- `pinn_instruction/markdown_conversion/ctl_instruction.md` — final authoritative CTL markdown after Phase 10.
- `pinn_instruction/markdown_conversion/README.md` — index to create/update for authoritative markdown files and verification reports.
- `pinn_instruction/markdown_conversion/_archive/ctl-instruction/README.md` — archive provenance README to create.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The CTL source is already modularized into 8 content files referenced by `main_CTL.tex`, so Phase 10 can audit in exact source order without inventing section boundaries.
- The 3 CTL markdown candidates already exist and have substantially different structures and lengths:
  - `pinn_instruction/markdown_conversion/ctl_instruction.md`
  - `pinn_instruction/markdown_conversion/ctl_instruction_v2.md`
  - `pinn_instruction/markdown_conversion/pandoc_conversion/CTL-instruction-final.md`
- Prior phase contexts establish report-driven verification as the project pattern.

### Established Patterns
- Documentation work uses plain Markdown, not a documentation framework.
- Source-adjacent reports are preferred when a report verifies a specific artifact.
- Phase 9 uses `BLOCKING / MAJOR / MINOR / INFO`; reuse these labels for discrepancy severity.
- Prior LaTeX verification phases treat source files as ground truth and compare derived artifacts against them.

### Integration Points
- `pinn_instruction/markdown_conversion/ctl_instruction.md` becomes the canonical CTL markdown artifact consumed by future readers and agents.
- `pinn_instruction/markdown_conversion/README.md` becomes the discoverability layer for this and future v1.3 authoritative markdowns.
- `pinn_instruction/markdown_conversion/_archive/ctl-instruction/` keeps duplicate CTL markdown conversions inspectable without ambiguity about the canonical file.

### Known Path Caveat
- Prior contexts reference `pinn_instruction/original_latex/verification/`, but that directory is not present in this checkout. Phase 10 should not assume prior verification scripts exist locally unless the planner re-discovers or recreates them.

</code_context>

<specifics>
## Specific Ideas

- Treat Phase 10 as the pilot phase for the v1.3 audit pattern because CTL is the hardest document: 8 sections, 3 candidates, heavy math, tables, labels, references, visible author notes, and excluded comment blocks.
- Do not let the appended `Source Issues / Notes for Future Reconciliation` section contaminate fidelity checks. The source-converted body is compared to LaTeX; appended metadata is compared only for intentional placement and clarity.
- Source-level concerns should refer back to exact headings, discrepancy IDs where relevant, and source/markdown locations. The goal is easy future reconciliation without altering the faithful conversion.
- Candidate selection should be explainable even when human inspection overrides the raw score. The report should state what the raw score preferred, what human inspection found, and why the final baseline was chosen.

</specifics>

<deferred>
## Deferred Ideas

- Fixing suspected source-level mathematical, factual, or methodological problems in CTL. Phase 10 documents these inside the authoritative markdown's appended source-issues section, but does not correct them.
- Cross-document reconciliation between CTL, PINN architecture, sampling method, data-quality assessment, review-of-framework, and stage-strategy-revision. v1.3 preserves source-specific content; reconciliation belongs to a later phase.
- Building shared automated markdown-verification tooling for all 6 documents. Current v1.3 requirements defer automation to v2.
- Updating Phase 9 outputs. Phase 9 is being completed separately and remains a prerequisite gate for executing v1.3 phases.

</deferred>

---

*Phase: 10-CTL-Instruction Verification*
*Context gathered: 2026-05-02*
