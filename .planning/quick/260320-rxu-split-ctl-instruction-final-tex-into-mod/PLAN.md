# Quick Task PLAN: Split CTL-instruction-final.tex into Modular Structure

**Task ID:** 260320-rxu
**Source:** `pinn_instruction/original_latex/ctl-instruction/CTL-instruction-final.tex` (1830 lines)
**Plan reference:** `docs/plans/splitting_latex.md`

## Target Structure

```
pinn_instruction/ctl-instruction/
├── main_CTL.tex
├── preamble_CTL.tex
├── sections/
│   ├── 01_intro.tex            % Sec 1: Important Note + Sec 3: Multi-Fidelity Curriculum
│   ├── 02_data_characterization.tex  % Sec 2: Characterizing and Organizing...
│   ├── 03_data_glimpse.tex     % Sec 4: A Glimpse at the Data
│   ├── 04_phase1_data_prep.tex % Sec 5: Phase 1 - Data Preparation
│   ├── 05_phase2_training_loop.tex % Sec 6: Phase 2 Definitive + Sec 7 (commented old)
│   ├── 06_advanced_considerations.tex % Sec 8: Advanced Considerations
│   ├── 07_reproducibility.tex  % Sec 9: Reproducibility Note
│   └── appendix.tex            % Appendix A
├── figures/
└── listings/
```

## Source Line Ranges

| File | Lines | Document Section(s) |
|---|---|---|
| preamble_CTL.tex | 1-45 | packages, lstset, commands, title/author/date |
| main_CTL.tex | — | new skeleton |
| 01_intro.tex | 50-322 | \section{Important Note} + \section{A Multi-Fidelity Curriculum Learning Framework} |
| 02_data_characterization.tex | 59-292 | \section{Characterizing and Organizing...} |
| 03_data_glimpse.tex | 324-404 | \section{A Glimpse at the Data} |
| 04_phase1_data_prep.tex | 405-1038 | \section{Phase 1 - Data Preparation and Stratification} |
| 05_phase2_training_loop.tex | 1039-1691 | \section{Phase 2 - The Definitive CTL-PINN Training Loop} + commented \section{Phase 2 - CTL-PINN Training Loop (needs revision)} |
| 06_advanced_considerations.tex | 1692-1759 | \section{Advanced Considerations and Best Practices} |
| 07_reproducibility.tex | 1760-1760 | \section{Reproducibility Note} |
| appendix.tex | 1761-1829 | \appendix + \section{Supplementary Figures} |

## Key Details
- Lines 47-48: `\begin{document}` and `\maketitle` → move to main_CTL.tex
- Section 2 (lines 59-292) overlaps with 01_intro's range because the document renumbers after Section 3 insertion — extract Section 2 FIRST, then the remaining sections
- Comment blocks: lines 276-290, 293-320, 649-694, 1089-1096, 1275-1681 — all must be preserved in their respective section files
- lstlisting blocks: ~15 total across sections — preserved as-is
- The old Section 7 (commented out, lines 1276-1681) goes into 05_phase2_training_loop.tex

## Tasks

1. Create directory structure
2. Write preamble_CTL.tex (lines 1-45)
3. Write main_CTL.tex (new skeleton)
4. Write 01_intro.tex (lines 50-57 Section 1 + lines 294-322 Section 3)
5. Write 02_data_characterization.tex (lines 59-292 Section 2)
6. Write 03_data_glimpse.tex (lines 324-404 Section 4)
7. Write 04_phase1_data_prep.tex (lines 405-1038 Section 5)
8. Write 05_phase2_training_loop.tex (lines 1039-1691 Sections 6+7)
9. Write 06_advanced_considerations.tex (lines 1692-1759 Section 8)
10. Write 07_reproducibility.tex (line 1760 Section 9)
11. Write appendix.tex (lines 1761-1829)
12. Verify: pdflatex main_CTL.tex compiles clean

## Verification
- `pdflatex main_CTL.tex` runs without errors
- All original content preserved (diff source sections vs new files)
- No duplicate or missing lines at section boundaries
