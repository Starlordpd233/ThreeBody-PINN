# Phase 7: Structure Fidelity Verification - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Automated Python script that verifies structural LaTeX elements — section hierarchy, labels, cross-references, citations, and float environments — are faithfully preserved in the modular structures compared to their originals. Covers all 5 structures. Content completeness (Phase 5), preamble parity (Phase 6), and compilability (Phase 8) are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Script design
- **D-01:** Single script `verify_structure.py` in `pinn_instruction/original_latex/verification/` — consistent with Phase 5 (verify_content.py) and Phase 6 (verify_preamble.py) pattern
- **D-02:** Same CLI interface: `--structure <name>`, `--output <path>`, `--verbose`, run all structures by default
- **D-03:** Same modular content assembly as Phase 5: full recursive resolution of `\input{}`/`\include{}` from the modular main.tex to produce flat assembled content, then extract structural elements

### Section hierarchy (STRUCT-01)
- **D-04:** Extract ordered flat list of `\section`, `\subsection`, `\subsubsection`, `\paragraph`, `\subparagraph` commands (with their title text) from both original and assembled modular content
- **D-05:** Compare sequentially — report any ordering differences, missing sections, or extra sections. Side-by-side display (original vs modular) for easy human review
- **D-06:** Strip whitespace from extracted titles before comparison; ignore optional short-title arguments (e.g., `\section[short]{Long Title}` → compare only "Long Title")

### Label and reference checking (STRUCT-02, STRUCT-03)
- **D-07:** Extract all `\label{...}` declarations from original; verify each appears in modular assembled content. Report missing labels.
- **D-08:** Extract all `\ref{...}`, `\eqref{...}`, `\autoref{...}` from original; verify each appears in modular assembled content. Report missing references.
- **D-09:** Only check presence — do not verify that referenced labels are defined (cross-reference validity is a compilation concern, Phase 8)

### Citation and bibliography (STRUCT-04)
- **D-10:** Extract all `\cite{...}`, `\citep{...}`, `\citet{...}`, `\citealt{...}`, `\nocite{...}` from original; verify each appears in modular assembled content
- **D-11:** Extract `\bibliography{...}` and `\printbibliography` declarations from original; verify presence in modular content
- **D-12:** For multi-key citations like `\cite{key1,key2,key3}`, split on commas and track each key individually

### Float environments (STRUCT-05)
- **D-13:** Extract full content of each `\begin{figure}...\\end{figure}`, `\begin{table}...\\end{table}`, `\begin{longtable}...\\end{longtable}` block from both original and modular assembled content
- **D-14:** Compare float count per type (must match); compare full content of each float using difflib — flag any content differences within floats (missing captions, altered labels, dropped rows)
- **D-15:** Use brace/environment depth tracking for extraction (same pattern as Phase 6 config block extraction)

### Inactive section handling
- **D-16:** Exclude inactive section files for pinn-architecture (input_vector_inactive, advanced_training_inactive, consolidated_blueprint_inactive) — same as Phase 5 D-04. Do not report structural elements from inactive files as missing.

### Report format
- **D-17:** Markdown output to `pinn_instruction/original_latex/verification/structure_verification_report.md` — consistent with D-06 from Phase 5 CONTEXT
- **D-18:** Report structure: summary table (pass/fail per structure) at top, followed by per-structure detail sections with subsections for each check category (sections, labels, refs, citations, floats)
- **D-19:** Exit code 0 if all structures pass all checks; exit code 1 if any structure has any mismatch

### Claude's Discretion
- Exact regex patterns for extraction (handles multiline titles, optional arguments, etc.)
- Argparse design and progress output
- Whether to deduplicate labels/refs before comparison (reasonable to deduplicate)
- Handling of `\input{}`-only vs `\include{}`-only structures (ctl-instruction uses `\include{}`)

</decisions>

<specifics>
## Specific Ideas

- Same file structure as verify_content.py and verify_preamble.py — STRUCTURES list with identical paths, same argparse interface, same Markdown report format. Planner should use those existing scripts as implementation references.
- The 5 structure path mappings are already established in both prior scripts — reuse exactly.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Established verification scripts (implementation reference)
- `pinn_instruction/original_latex/verification/verify_content.py` — Phase 5 script: STRUCTURES list, argparse pattern, recursive \input{} resolution, report generation structure
- `pinn_instruction/original_latex/verification/verify_preamble.py` — Phase 6 script: dataclass pattern, brace-depth environment extraction, same STRUCTURES list with exact file paths

### Phase 5 decisions (canonical for assembly and report format)
- `.planning/phases/05-content-completeness-verification/05-CONTEXT.md` — D-01 through D-10: assembly strategy, scaffolding exclusion, whitespace normalization, inactive section handling, report format

### Requirements
- `.planning/REQUIREMENTS.md` — STRUCT-01 through STRUCT-05 definitions

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `verify_content.py`: `resolve_inputs()` function — recursive \input{}/\include{} resolution, used for modular assembly. Reuse or replicate for verify_structure.py.
- `verify_preamble.py`: `assemble_modular_preamble()`, brace-depth tracking loop — reuse for float environment extraction.
- Both scripts: identical `STRUCTURES` list with 5 structure path definitions — copy verbatim.

### Established Patterns
- Python stdlib only (no external deps): `re`, `argparse`, `pathlib`, `dataclasses`, `difflib`, `datetime`
- Scripts run from project root — all paths are relative to root
- Dataclasses for typed extraction results
- Markdown report with summary table + per-structure sections

### Integration Points
- Output goes to `pinn_instruction/original_latex/verification/` alongside content_verification_report.md and preamble_verification_report.md
- Phase 8 (compilability) will also add a script to this directory

### Key structural observations (from prior phases)
- Data-quality-assessment: preamble inline in main.tex, no separate preamble.tex input
- ctl-instruction: uses `\include{}` (inserts \clearpage) — assembly must handle this
- pinn-architecture: 3 inactive section files excluded from verification
- review_of_framework: inline formatting lines (\thispagestyle, \vspace, \hrule) between \maketitle and first section
- stage_strat_revision: \tableofcontents + \newpage between preamble and first section

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 07-structure-fidelity-verification*
*Context gathered: 2026-03-21 via --auto mode*
