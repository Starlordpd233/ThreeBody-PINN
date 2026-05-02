# Phase 10: CTL-Instruction Verification - Research

**Researched:** 2026-05-02
**Status:** Complete

## Research Question

What needs to be known to plan Phase 10 well?

Phase 10 verifies one CTL markdown conversion against its LaTeX source and produces a single authoritative markdown file. The work is documentation fidelity work, not implementation of the CTL method itself.

## Source Inventory

### LaTeX Source

- `pinn_instruction/original_latex/ctl-instruction/main_CTL.tex` defines the canonical source order.
- `pinn_instruction/original_latex/ctl-instruction/preamble_CTL.tex` defines macros, including visible author comments.
- `pinn_instruction/original_latex/ctl-instruction/sections/01_intro.tex` has 4 lines.
- `pinn_instruction/original_latex/ctl-instruction/sections/02_data_characterization.tex` has 265 lines.
- `pinn_instruction/original_latex/ctl-instruction/sections/03_data_glimpse.tex` has 80 lines.
- `pinn_instruction/original_latex/ctl-instruction/sections/04_phase1_data_prep.tex` has 634 lines.
- `pinn_instruction/original_latex/ctl-instruction/sections/05_phase2_training_loop.tex` has 653 lines.
- `pinn_instruction/original_latex/ctl-instruction/sections/06_advanced_considerations.tex` has 68 lines.
- `pinn_instruction/original_latex/ctl-instruction/sections/07_reproducibility.tex` has 1 line.
- `pinn_instruction/original_latex/ctl-instruction/sections/appendix.tex` has 69 lines.

### Markdown Candidates

- `pinn_instruction/markdown_conversion/ctl_instruction.md` - existing top-level CTL conversion and final authoritative target path.
- `pinn_instruction/markdown_conversion/ctl_instruction_v2.md` - alternate top-level CTL conversion.
- `pinn_instruction/markdown_conversion/pandoc_conversion/CTL-instruction-final.md` - pandoc-generated CTL conversion.

The candidates have different line counts and heading styles, so candidate selection must not rely on line count alone. It must normalize formatting-only noise while preserving meaningful content differences.

## Source Features That Affect Planning

### Comment Handling

The CTL source contains `comment` environments that must be excluded:

- `02_data_characterization.tex`: lines 218-232.
- `02_data_characterization.tex`: lines 235-263.
- `04_phase1_data_prep.tex`: lines 245-290.
- `05_phase2_training_loop.tex`: lines 51-58.
- `05_phase2_training_loop.tex`: lines 237-643.

Visible `\authcomment{...}` notes are not excluded. They are source-visible content and must be preserved as explicit markdown notes/callouts.

### Heavy Audit Sections

The highest-risk sections are:

- `04_phase1_data_prep.tex`: invariants, labels, normalization, Lyapunov formulas, input vector formulation, author notes.
- `05_phase2_training_loop.tex`: loss formulas, ALM updates, stage transition criteria, tables, and a large excluded comment block.
- `appendix.tex`: figures, captions, and `\ref{...}` references.

These sections should receive formula-by-formula and table-by-table verification.

## Planning Implications

### Recommended Plan Split

Use three sequential plans:

1. Candidate comparison and baseline promotion.
2. Section audit and correction for source sections 01-04.
3. Section audit and correction for source sections 05-appendix, final verification, archive, and index.

This keeps edits section-scoped while allowing the selected baseline to be promoted before detailed audit begins.

### Baseline Promotion Rule

Because the final authoritative filename is fixed as `ctl_instruction.md`, Plan 10-01 must handle the case where the selected candidate is not currently at that path.

If `ctl_instruction.md` is selected, leave it in place. If another candidate is selected, preserve the current `ctl_instruction.md` in `_archive/ctl-instruction/` before promoting the selected candidate into `ctl_instruction.md`.

### Report Strategy

Use one final report next to the authoritative markdown:

- `pinn_instruction/markdown_conversion/ctl_instruction_verification_report.md`

The report should accumulate candidate scores, excluded comment ranges, per-section audit tables, formula checklists, fix log, source-issue notes, and final zero-open-discrepancy status.

## Validation Architecture

Validation for this phase is documentation-oriented and mostly grep/read driven:

- Candidate inventory: all three candidates are named in the report.
- Source order: the report lists all 8 source section files.
- Comment exclusion: excluded ranges are listed in the report, and excluded headings do not appear in the final converted body.
- Author notes: `authcomment` source notes appear as visible markdown notes/callouts.
- Section audit: each source section has a report subsection with pass/fail and discrepancy table.
- Math audit: heavy sections contain formula checklist tables.
- Fix traceability: every conversion fix has a discrepancy ID, section, and fix summary.
- Authority: `ctl_instruction.md` exists as final authoritative markdown, unselected candidates are archived, and `README.md` points to the authoritative file and report.

## Risks

- Replacing `ctl_instruction.md` with another selected candidate can lose the original candidate unless the plan archives it first.
- Appended source-issue notes can contaminate fidelity comparison unless explicitly excluded from final comparison.
- Visible author comments can be mistaken for excluded comments. The plan must distinguish `\authcomment{...}` from `comment` environments.
- Moving a pandoc candidate out of `pandoc_conversion/` can affect provenance if the archive README does not document the move.

## Research Complete

Planning should proceed with three sequential plans and explicit validation gates for candidate selection, source-order section audit, and final archive/index creation.

