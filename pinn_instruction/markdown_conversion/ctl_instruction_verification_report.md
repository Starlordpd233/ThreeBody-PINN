# CTL Instruction Markdown Verification Report

## CTL Candidate Comparison

Scoring normalized whitespace, line wrapping, escaped underscores, URI escaping, and harmless Markdown punctuation. Scores do not normalize away formula changes, table-cell changes, label/reference loss, missing prose, added prose, heading drift, or omitted visible `\authcomment{...}` text.

| Candidate | Overall score | Rank | Per-section score summary | Human inspection notes |
|---|---:|---:|---|---|
| `pinn_instruction/markdown_conversion/ctl_instruction.md` | 0.958 F1 / 0.958 recall | 2 raw / 1 selected | 01: 1.000 recall; 02: 0.992; 03: 1.000; 04: 0.999; 05: 0.990; 06: 1.000; 07: N/A; appendix: 0.577 | Best section 04 preservation, strongest appendix/figure preservation among top candidates, target path already contains labels and figure anchors. |
| `pinn_instruction/markdown_conversion/ctl_instruction_v2.md` | 0.890 F1 / 0.909 recall | 3 | 01: 1.000 recall; 02: 0.980; 03: 0.947; 04: 0.937; 05: 0.971; 06: 0.999; 07: N/A; appendix: 0.543 | Lower recall in sections 03-05; heading hierarchy is noisier because several code comments became headings. |
| `pinn_instruction/markdown_conversion/pandoc_conversion/CTL-instruction-final.md` | 0.959 F1 / 0.947 recall | 1 raw / 2 selected | 01: 1.000 recall; 02: 0.995; 03: 0.988; 04: 0.986; 05: 0.990; 06: 1.000; 07: N/A; appendix: 0.561 | Slightly better raw F1 and precision, but lower recall than the selected target and weaker section 04/appendix preservation. |

## Selected Baseline

- Selected candidate: `pinn_instruction/markdown_conversion/ctl_instruction.md`
- Promoted target: `pinn_instruction/markdown_conversion/ctl_instruction.md`
- Selection rationale: The pandoc candidate narrowly wins the raw F1 score, but the existing target has better source recall and stronger preservation in the highest-risk section 04 and appendix figure area. Human sanity-check therefore selected the existing target as the safest baseline.
- Override used: yes
- Promotion action: selected candidate already occupied `pinn_instruction/markdown_conversion/ctl_instruction.md`; no file move was needed during baseline promotion.

## Excluded Comment Ranges

| Source range | Excluded headings/content summary | Markdown status |
|---|---|---|
| `02_data_characterization.tex:218-232` | Commented `Assessing Data Suitability and Generation Methodology` subsection and data-quality-control discussion. | Absent from converted body |
| `02_data_characterization.tex:235-263` | Commented `A Multi-Fidelity Curriculum Learning Framework` section and curriculum rationale/path subsections. | Absent from converted body |
| `04_phase1_data_prep.tex:245-290` | Commented velocity-position angle item and sample angle-computation listing. | Absent from converted body |
| `05_phase2_training_loop.tex:51-58` | Commented energy regularizer subsection and formula. | Absent from converted body |
| `05_phase2_training_loop.tex:237-643` | Commented older training-loop revision, alternate mini-batch/gradient-clipping tables, and notes. | Absent from converted body |

## Section Audit

Section audits are added in source order by Plans 10-02 and 10-03.

## Fix Log

| ID | Section | Fix summary |
|---|---|---|
| CTL-10-01-BASELINE | Candidate selection | Created candidate comparison, selected existing `ctl_instruction.md`, and recorded comment-exclusion ranges. |

## Source Issues / Notes for Future Reconciliation

Pending section audit.

## Final Verification

Pending completion of section audits and archive/index work.
