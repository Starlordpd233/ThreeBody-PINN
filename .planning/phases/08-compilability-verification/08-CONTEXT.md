# Phase 8: Compilability Verification - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Automated Python script that compiles all 5 modular LaTeX structures with pdflatex and reports pass/fail (0 errors required), along with a warning comparison against the original monolithic files to flag any new warnings introduced by the modularization. Content completeness (Phase 5), preamble parity (Phase 6), and structure fidelity (Phase 7) are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Script design
- **D-01:** Single script `verify_compile.py` in `pinn_instruction/original_latex/verification/` — consistent with Phase 5 (verify_content.py), Phase 6 (verify_preamble.py), Phase 7 (verify_structure.py) pattern
- **D-02:** Same CLI interface: `--structure <name>`, `--output <path>`, `--verbose`, run all structures by default
- **D-03:** Compile both the original monolithic .tex (from `old/`) AND the modular version for each structure, enabling apples-to-apples warning comparison

### Compiler and invocation
- **D-04:** Use `latexmk -pdf -pdflatex=pdflatex` for compilation — handles multi-pass automatically (resolves cross-refs, citations, TOC without manual iteration counting)
- **D-05:** `pdflatex` is confirmed available (TeX Live 2025, `/Library/TeX/texbin/pdflatex`); `latexmk` also available
- **D-06:** Run latexmk with `cwd` set to the structure's directory so relative `\input{preamble}` and `\input{sections/...}` paths resolve correctly
- **D-07:** Use `-output-directory` pointing to a per-structure temp directory under `pinn_instruction/original_latex/verification/tmp/` to avoid polluting source directories with aux files from verification runs
- **D-08:** Set `-interaction=nonstopmode` so compilation continues through errors rather than halting (ensures we capture all errors, not just the first)
- **D-09:** Timeout per compilation: 120 seconds (sufficient for all 5 structures given their size)

### Pass/fail criteria
- **D-10:** PASS = 0 fatal errors in the compilation log (lines matching `^!` in .log file)
- **D-11:** FAIL = any fatal error present; report all errors with surrounding context (file, line, error message)
- **D-12:** Warnings are informational — do NOT count as pass/fail. Report warning counts and flag new warnings (present in modular log but not in original log) as noteworthy.

### Warning baseline comparison (COMP-02)
- **D-13:** Extract warnings from both original and modular compilation logs using the same regex; diff the warning sets
- **D-14:** A "warning" is any log line matching `LaTeX Warning:`, `Package Warning:`, `Class Warning:`, or `Overfull \\hbox` / `Underfull \\hbox`
- **D-15:** Normalize warning text before comparison: strip file path prefixes (vary between runs) and page numbers; compare warning type and core message
- **D-16:** Report three categories: (a) warnings in both = pre-existing (OK), (b) warnings only in modular = new/introduced, (c) warnings only in original = resolved (bonus — not required but informative)

### Report format
- **D-17:** Markdown output to `pinn_instruction/original_latex/verification/compile_verification_report.md` — consistent with D-06 from Phase 5 CONTEXT
- **D-18:** Report structure: summary table (PASS/FAIL per structure, error count, new warning count) at top, followed by per-structure sections with full error list and new warning list
- **D-19:** Exit code 0 if all 5 structures compile with 0 errors; exit code 1 if any structure has errors
- **D-20:** Temp directory cleaned up after each run (or kept with `--keep-tmp` flag for debugging)

### Compilation working directory
- **D-21:** Each structure's `main.tex` (or equivalent) is compiled from its own directory. The 5 main files are:
  1. Data-quality-assessment: `pinn_instruction/original_latex/Data-quality-assessment/data_quality_assess/main-data-quality-assess.tex` (cwd: `data_quality_assess/`)
  2. ctl-instruction: `pinn_instruction/original_latex/ctl-instruction/ctl-instruction/main_CTL.tex` (cwd: `ctl-instruction/`)
  3. pinn-architecture: `pinn_instruction/original_latex/pinn-architecture/pinn-architecture/main_pinn.tex` (cwd: `pinn-architecture/`)
  4. review_of_framework: `pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex` (cwd: `review_of_framework/`)
  5. stage_strat_revision: `pinn_instruction/original_latex/review-of-framework/stage_strat_revision/stage_strat_revision.tex` (cwd: `stage_strat_revision/`)
- **D-22:** Original files (for baseline) compiled from their `old/` directories:
  1. `pinn_instruction/original_latex/Data-quality-assessment/old/data_quality_assess.tex`
  2. `pinn_instruction/original_latex/ctl-instruction/old/CTL-instruction-final.tex`
  3. `pinn_instruction/original_latex/pinn-architecture/old/PINN_architecture_plan.tex`
  4. `pinn_instruction/original_latex/review-of-framework/old/review_of_ctl-pinn_framework.tex`
  5. `pinn_instruction/original_latex/review-of-framework/old/stage-strat-revision.tex`

### Claude's Discretion
- Exact regex for log parsing (errors vs warnings; handle multi-line error messages)
- Whether to run latexmk with `-silent` or capture all output
- How to handle `bibtex`/`biber` if any structure uses bibliography compilation (latexmk handles this automatically)
- Argparse design and progress output

</decisions>

<specifics>
## Specific Ideas

- Use `subprocess.run()` with `capture_output=True` and `cwd` parameter — same as any Python shell invocation pattern
- The existing .pdf and .log files in each modular structure directory confirm previous successful compilation — script should still re-compile fresh to verify current state
- TeX Live 2025 is confirmed installed at `/Library/TeX/texbin/`

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Established verification scripts (implementation reference)
- `pinn_instruction/original_latex/verification/verify_content.py` — Phase 5: STRUCTURES list, argparse pattern, report generation
- `pinn_instruction/original_latex/verification/verify_preamble.py` — Phase 6: STRUCTURES list with exact file paths (copy verbatim for modular main paths)

### Phase 5 decisions (canonical for script structure and report format)
- `.planning/phases/05-content-completeness-verification/05-CONTEXT.md` — D-06, D-07, D-09 for report location, format, and naming

### Phase 8 structure file paths
- D-21 and D-22 above list the exact file paths for all 5 modular main files and 5 original files

### Requirements
- `.planning/REQUIREMENTS.md` — COMP-01 and COMP-02 definitions

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `verify_content.py` and `verify_preamble.py`: identical `STRUCTURES` list with modular main file paths — copy for modular compilation targets
- Both scripts: `argparse` CLI pattern, Markdown report generation, summary table format — replicate

### Established Patterns
- Python stdlib only: `re`, `argparse`, `pathlib`, `subprocess`, `tempfile`, `datetime`
- Scripts run from project root — paths relative to root, but compilation must use `cwd` per structure directory
- Markdown report with summary table + per-structure detail sections

### Integration Points
- Output goes to `pinn_instruction/original_latex/verification/` alongside the three prior phase reports
- Temp compilation outputs go to `pinn_instruction/original_latex/verification/tmp/` (cleaned after run)
- This is the final phase in v1.1 milestone — its report completes the verification suite

### Existing compilation artifacts
- All 5 modular structures already have `.pdf`, `.aux`, `.log` files from prior compilation — confirms pdflatex works
- The `old/` original directories have no existing aux/log files — script will compile them fresh for baseline
- latexmk `.fdb_latexmk` and `.fls` files exist for most structures — confirms latexmk was previously used

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 08-compilability-verification*
*Context gathered: 2026-03-21 via --auto mode*
