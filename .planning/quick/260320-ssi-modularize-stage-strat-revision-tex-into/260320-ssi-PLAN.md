---
phase: quick
plan: 260320-ssi
type: execute
wave: 1
depends_on: []
files_modified:
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/main.tex
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/preamble.tex
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/abstract.tex
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/foundational_principles.tex
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/algorithmic_workflow.tex
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/implementation_validation_protocol.tex
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/conclusions_recommendations.tex
  - pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/bibliography.tex
autonomous: true
requirements: []

must_haves:
  truths:
    - "Modularized project compiles to identical PDF as the original (same page count, no errors or warnings)"
    - "All 4 \\part{} commands, all sections, all tables, and the lstlisting block are preserved"
    - "Original stage-strat-revision.tex remains untouched"
    - "Cross-references (tab:invariants, tab:dataframe, tab:framework_comparison, tab:final_stages) resolve correctly"
    - "\\authcomment macro works in the modularized output"
  artifacts:
    - path: "pinn_instruction/original_latex/review-of-framework/stage_strat_revision/main.tex"
      provides: "Document root with \\documentclass, \\input{preamble}, title block, \\input{sections/...} calls, \\end{document}"
      contains: "\\input{preamble}"
    - path: "pinn_instruction/original_latex/review-of-framework/stage_strat_revision/preamble.tex"
      provides: "All packages, geometry, hypersetup, lstdefinestyle pythonstyle, lstset, \\authcomment macro"
      contains: "pythonstyle"
    - path: "pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/foundational_principles.tex"
      provides: "Part I content: Sections 1.1-1.3, description env, tab:invariants table"
      contains: "tab:invariants"
    - path: "pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/algorithmic_workflow.tex"
      provides: "Part II content: Sections 2.1-2.4, tab:dataframe, tab:framework_comparison, tab:final_stages longtable"
      contains: "longtable"
    - path: "pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/implementation_validation_protocol.tex"
      provides: "Part III content: lstlisting (~110 lines Python), Sections 3.1-3.3"
      contains: "lstlisting"
    - path: "pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/conclusions_recommendations.tex"
      provides: "Part IV content: conclusions and enumerate recommendations"
      contains: "\\part{Conclusions"
    - path: "pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/bibliography.tex"
      provides: "thebibliography environment (16 references)"
      contains: "thebibliography"
  key_links:
    - from: "main.tex"
      to: "preamble.tex"
      via: "\\input{preamble}"
      pattern: "\\\\input\\{preamble\\}"
    - from: "main.tex"
      to: "sections/*.tex"
      via: "\\input{sections/...}"
      pattern: "\\\\input\\{sections/"
    - from: "preamble.tex"
      to: "algorithmic_workflow.tex"
      via: "pythonstyle lstlisting style used by lstlisting block"
      pattern: "pythonstyle"
    - from: "preamble.tex"
      to: "all section files"
      via: "\\authcomment macro used in foundational_principles.tex"
      pattern: "\\\\authcomment"
---

<objective>
Modularize stage-strat-revision.tex into a multi-file LaTeX project following the same pattern used for review_of_framework.

Purpose: Improve maintainability of the 509-line stage-strat-revision.tex by splitting into a main driver, preamble, and per-part section files.
Output: 8 files in stage_strat_revision/ directory that compile to identical PDF as the original.
</objective>

<execution_context>
@<home>/.claude-xiaomi/get-shit-done/workflows/execute-plan.md
@<home>/.claude-xiaomi/get-shit-done/templates/summary.md
</execution_context>

<context>
@pinn_instruction/original_latex/review-of-framework/stage-strat-revision.tex
@pinn_instruction/original_latex/review-of-framework/review_of_framework/main.tex
@pinn_instruction/original_latex/review-of-framework/review_of_framework/preamble.tex

Reference pattern from review_of_framework/ (prior modularization 260320-sh3):
- main.tex: \\documentclass, \\input{preamble}, title block, \\begin{document}, \\maketitle, \\input{sections/...}, \\end{document}
- preamble.tex: all packages, geometry, hypersetup, lstdefinestyle, lstset
- Section files: content only (no \\begin{document})

Key differences from review_of_framework pattern:
- Uses letterpaper (not a4paper)
- Uses pythonstyle (not mystyle)
- Has \\part{} commands (review_of_framework does not)
- Has \\authcomment macro (unique)
- Has longtable environment

## Source Structure (exact line boundaries):

Lines 1-61: Document class + preamble (packages, geometry, hypersetup, lstdefinestyle pythonstyle, lstset, \\authcomment)
Lines 63-66: Title block (\\title, \\author, \\date)
Lines 68-76: \\begin{document}, \\maketitle, abstract, \\tableofcontents, \\newpage
Lines 78-137: \\part{Foundational Principles} + Sections 1.1-1.3 + description env + tab:invariants table[H]
Lines 139-173: Section 1.3 continued (Core Techniques: PCA, Clustering, Quantile Binning)
Lines 174-229: \\part{A Revised Algorithmic Workflow} + Section 2.1 + tab:dataframe table[H]
Lines 230-285: Sections 2.2-2.3 (EDA, Adaptive Criteria) + tab:framework_comparison table[H]
Lines 287-335: Section 2.4 + tab:final_stages longtable
Lines 337-458: \\part{Implementation and Validation Protocol} + lstlisting (~110 lines Python) + Section 3.1
Lines 460-474: Sections 3.2-3.3
Lines 476-487: \\part{Conclusions and Recommendations} + enumerate
Lines 489-507: thebibliography (16 references)
Line 509: \\end{document}

Labels: tab:invariants (line 127), tab:dataframe (line 218), tab:framework_comparison (line 261), tab:final_stages (line 301)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create preamble.tex and main.tex</name>
  <files>pinn_instruction/original_latex/review-of-framework/stage_strat_revision/preamble.tex, pinn_instruction/original_latex/review-of-framework/stage_strat_revision/main.tex</files>
  <action>
Create the target directory structure and two driver files:

1. Create directories: `stage_strat_revision/` and `stage_strat_revision/sections/`

2. Create `preamble.tex` containing lines 3-61 of the source (everything between \documentclass and the title block):
   - All \usepackage commands (inputenc, amsmath, amssymb, amsfonts, graphicx, geometry, booktabs, longtable, listings, xcolor, hyperref, caption, float)
   - \newcommand{\authcomment}...
   - \geometry{letterpaper, total={6.5in,9in}, left=1in, top=1in}
   - \hypersetup{...} with pdftitle and pdfpagemode=FullScreen
   - \definecolor for codegreen, codegray, codepurple, backcolour
   - \lstdefinestyle{pythonstyle}{...}
   - \lstset{style=pythonstyle}
   - NO \documentclass, NO \begin{document}

3. Create `main.tex`:
   - \documentclass[11pt, letterpaper]{article}
   - \input{preamble}
   - \title{...}, \author{...}, \date{...} (lines 64-66)
   - \begin{document}
   - \maketitle
   - \input{sections/abstract}
   - \tableofcontents
   - \newpage
   - \input{sections/foundational_principles}
   - \input{sections/algorithmic_workflow}
   - \input{sections/implementation_validation_protocol}
   - \input{sections/conclusions_recommendations}
   - \input{sections/bibliography}
   - \end{document}

Follow the exact pattern from review_of_framework/main.tex (task 260320-sh3).
  </action>
  <verify>
    <automated>ls -la pinn_instruction/original_latex/review-of-framework/stage_strat_revision/{main.tex,preamble.tex}</automated>
  </verify>
  <done>main.tex and preamble.tex exist with correct structure; preamble contains pythonstyle definition and authcomment macro; main.tex has 6 \input calls for sections</done>
</task>

<task type="auto">
  <name>Task 2: Create section files (Part I and Part II)</name>
  <files>pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/abstract.tex, pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/foundational_principles.tex, pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/algorithmic_workflow.tex</files>
  <action>
Create three section files with content extracted from the source. Each file contains ONLY the content (no \documentclass, no \begin{document}, no preamble).

1. `sections/abstract.tex` — lines 71-73:
   - \begin{abstract}...\end{abstract}

2. `sections/foundational_principles.tex` — lines 78-173:
   - \part{Foundational Principles of Data-Driven Curriculum Stratification for Physical Systems}
   - Opening paragraph
   - \section{The Rationale for Adaptive Curricula in Physics Simulations} (1.1)
   - \section{A Lexicon of Difficulty Metrics for the Three-Body Problem} (1.2) with \begin{description}...\end{description}
   - \begin{table}[H] \label{tab:invariants}...\end{table}
   - \section{Core Techniques for Data-Driven Stratification} (1.3)
   - \subsection{Dimensionality Reduction with PCA...}
   - \subsection{Unsupervised Clustering...}
   - \subsection{Quantile-Based Binning...}

3. `sections/algorithmic_workflow.tex` — lines 174-335:
   - \part{A Revised Algorithmic Workflow for Stage Stratification}
   - \section{Phase I: Invariant Computation and Feature Engineering} (2.1) with subsections 2.1.1-2.1.4
   - \begin{table}[H] \label{tab:dataframe}...\end{table}
   - \section{Phase II: Exploratory Data Analysis (EDA) and Landscape Mapping} (2.2) with subsections
   - \begin{table}[H] \label{tab:framework_comparison}...\end{table}
   - \section{Phase III: Deriving Adaptive Stage Criteria} (2.3) with subsections
   - \section{Phase IV: Final Stage Assignment and Population Balancing} (2.4)
   - \begin{longtable}...\label{tab:final_stages}...\end{longtable}

CRITICAL: Preserve all labels (tab:invariants, tab:dataframe, tab:framework_comparison, tab:final_stages) exactly. The longtable must remain intact in algorithmic_workflow.tex. The \authcomment on line 207 must be preserved in foundational_principles.tex.
  </action>
  <verify>
    <automated>grep -c 'label{tab:' pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/{foundational_principles,algorithmic_workflow}.tex</automated>
  </verify>
  <done>3 section files exist with correct content boundaries; all 4 table labels present; longtable intact in algorithmic_workflow.tex; authcomment present in foundational_principles.tex</done>
</task>

<task type="auto">
  <name>Task 3: Create section files (Part III, Part IV, bibliography) and compile</name>
  <files>pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/implementation_validation_protocol.tex, pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/conclusions_recommendations.tex, pinn_instruction/original_latex/review-of-framework/stage_strat_revision/sections/bibliography.tex</files>
  <action>
Create the remaining three section files, then compile and verify.

1. `sections/implementation_validation_protocol.tex` — lines 337-474:
   - \part{Implementation and Validation Protocol}
   - \section{Reference Implementation in Python} (3.1)
   - \begin{lstlisting}...\end{lstlisting} (~110 lines Python code — MUST remain contiguous)
   - \section{Advanced Architectural Considerations and Refinements} (3.2)
   - \section{A Protocol for Curriculum Validation} (3.3) with enumerate

2. `sections/conclusions_recommendations.tex` — lines 476-487:
   - \part{Conclusions and Recommendations}
   - Paragraph + \textbf{...} + enumerate

3. `sections/bibliography.tex` — lines 489-507:
   - \newpage
   - \begin{thebibliography}{99}...\end{thebibliography}

4. Compile the modularized project:
   ```bash
   cd pinn_instruction/original_latex/review-of-framework/stage_strat_revision && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
   ```
   Run twice for cross-references. Check for errors/warnings.

5. Compare page count with original:
   ```bash
   pdfinfo main.pdf | grep Pages
   pdfinfo ../stage-strat-revision.pdf | grep Pages
   ```
   (If original PDF doesn't exist, compile it once for comparison.)
  </action>
  <verify>
    <automated>cd pinn_instruction/original_latex/review-of-framework/stage_strat_revision && pdflatex -interaction=nonstopmode main.tex 2>&1 | tail -5</automated>
  </verify>
  <done>All 8 files created; modularized project compiles with 0 errors; page count matches original; all cross-references resolve</done>
</task>

</tasks>

<verification>
- All 4 \part{} commands present across section files
- All 4 table labels (tab:invariants, tab:dataframe, tab:framework_comparison, tab:final_stages) resolve
- lstlisting block is contiguous in implementation_validation_protocol.tex
- longtable is intact in algorithmic_workflow.tex
- \authcomment macro works (defined in preamble.tex, used in foundational_principles.tex)
- Original stage-strat-revision.tex is untouched
</verification>

<success_criteria>
- 8 files created in stage_strat_revision/
- pdflatex compiles with 0 errors, 0 warnings, 0 undefined references
- Page count matches original
- All labels resolve across section boundaries
- Original file unchanged
</success_criteria>

<output>
After completion, create `.planning/phases/quick/quick-260320-ssi-SUMMARY.md`
</output>
