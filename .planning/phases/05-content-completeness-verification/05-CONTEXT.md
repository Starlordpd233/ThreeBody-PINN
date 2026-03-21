# Phase 5: Content Completeness Verification - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Automated Python script that verifies every line of content from original monolithic .tex files is present in the modular sections, and no extraneous content was introduced. Covers all 5 modular structures. Preamble-specific checks, structure fidelity, and compilability are separate phases (6, 7, 8).

</domain>

<decisions>
## Implementation Decisions

### Content reconstruction strategy
- **D-01:** Full recursive reassembly — resolve all `\input{}`/`\include{}` in the modular main.tex to produce a single flat file, then diff against the original monolithic .tex
- **D-02:** Exclude scaffolding lines from diff: `\documentclass`, `\input{preamble...}`, `\begin{document}`, `\end{document}`, `\maketitle`, bare `\input{sections/...}` include directives
- **D-03:** Whitespace normalization: collapse multiple blank lines to one, strip trailing whitespace, preserve indentation

### Inactive section handling
- **D-04:** Diff only active sections — commented-out `%\input{sections/..._inactive}` lines and their corresponding files are excluded from the diff
- **D-05:** Report must note which inactive section files exist and that they were intentionally excluded (pinn-architecture has 3: input_vector_inactive, advanced_training_inactive, consolidated_blueprint_inactive)

### Report format
- **D-06:** Output as Markdown file saved to `pinn_instruction/original_latex/verification/`
- **D-07:** Report structure: summary table (pass/fail per structure with line counts) at top, followed by detailed per-structure sections showing any diffs found
- **D-08:** When content is fully preserved for a structure, report states "no differences found" for that structure

### Script organization
- **D-09:** Per-phase scripts — Phase 5 creates `verify_content.py` in `pinn_instruction/original_latex/verification/`
- **D-10:** Future phases add their own scripts to the same directory (verify_preamble.py, verify_structure.py, verify_compile.py)

### Claude's Discretion
- Script naming conventions and argparse design
- Exact diff algorithm (unified diff, custom, etc.)
- Terminal output formatting (if any, beyond file generation)
- How to handle `\include{}` vs `\input{}` differences (page break semantics)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — standard Python diffing approaches are fine. The user wants rigor (every line accounted for) but pragmatic normalization (whitespace-insensitive where LaTeX doesn't care).

</specifics>

<canonical_refs>
## Canonical References

No external specs — requirements are fully captured in decisions above.

### File mapping (5 structures to verify)

1. **Data-quality-assessment**
   - Original: `pinn_instruction/original_latex/Data-quality-assessment/old/data_quality_assess.tex`
   - Modular: `pinn_instruction/original_latex/Data-quality-assessment/data_quality_assess/main-data-quality-assess.tex`
   - Sections: 7 files in `sections/`

2. **ctl-instruction**
   - Original: `pinn_instruction/original_latex/ctl-instruction/old/CTL-instruction-final.tex`
   - Modular: `pinn_instruction/original_latex/ctl-instruction/ctl-instruction/main_CTL.tex`
   - Sections: 8 files in `sections/` (uses `\include{}` not `\input{}`)

3. **pinn-architecture**
   - Original: `pinn_instruction/original_latex/pinn-architecture/old/PINN_architecture_plan.tex`
   - Modular: `pinn_instruction/original_latex/pinn-architecture/pinn-architecture/main_pinn.tex`
   - Sections: 10 files in `sections/` (7 active, 3 inactive/commented out)

4. **review_of_framework**
   - Original: `pinn_instruction/original_latex/review-of-framework/old/review_of_ctl-pinn_framework.tex`
   - Modular: `pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex`
   - Sections: 7 files in `sections/`

5. **stage_strat_revision**
   - Original: `pinn_instruction/original_latex/review-of-framework/old/stage-strat-revision.tex`
   - Modular: `pinn_instruction/original_latex/review-of-framework/stage_strat_revision/stage_strat_revision.tex`
   - Sections: 6 files in `sections/` (includes abstract.tex and bibliography.tex)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- No existing verification scripts in the repo — this is greenfield for the verification/ directory

### Established Patterns
- Project uses Python for all scripting (data pipeline, metrics, IC generation)
- No test framework currently in use — scripts are standalone

### Integration Points
- The verification/ directory will be shared across Phases 5-8
- Each phase adds its own script; report files accumulate in the same directory
- The 5 structure mappings (original → modular) defined above are reused across all phases

### Key structural observations
- Data-quality-assessment: preamble is inline in main.tex (not a separate \input{preamble})
- ctl-instruction: uses `\include{}` (inserts \clearpage) vs `\input{}` in others
- pinn-architecture: has `\documentclass{article}` in main.tex + separate preamble.tex
- review_of_framework: has inline formatting lines between \maketitle and sections (\thispagestyle, \vspace, \hrule)
- stage_strat_revision: has \tableofcontents + \newpage between preamble and first section

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 05-content-completeness-verification*
*Context gathered: 2026-03-21*
