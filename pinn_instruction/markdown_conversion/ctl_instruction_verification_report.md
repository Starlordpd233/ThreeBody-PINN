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

### 01_intro.tex - Important Note

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-01-000 | text | INFO | `01_intro.tex:1-4` | `ctl_instruction.md:9-14` | Section heading and architecture-file pointer preserved. | No fix needed |

### 02_data_characterization.tex - Characterizing and Organizing the Multi-Fidelity Simulation Data

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-02-001 | table | MAJOR | `02_data_characterization.tex:5-21`, `tab:brutus_compare` | `ctl_instruction.md:21-32` | Candidate table preserved content but conversion collapsed the header into an unreadable simple table. | Fixed |
| CTL-02-002 | comment | MINOR | `02_data_characterization.tex:70-74` | `ctl_instruction.md:107-114` | Visible `\authcomment{...}` was rendered as a Pandoc style span rather than a plain visible markdown note. | Fixed |
| CTL-02-003 | comment | INFO | `02_data_characterization.tex:218-232`, `02_data_characterization.tex:235-263` | Converted body | Excluded `comment` environment headings are absent from the converted body. | Verified |

| Check item | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| Table `tab:brutus_compare` | `02_data_characterization.tex:5-21` | `ctl_instruction.md:21-32` | PASS | Dataset rows, tolerances, word lengths, `dt_out`, temporal-density increases, caption, and label are preserved. |
| Visible author note | `02_data_characterization.tex:70-74` | `ctl_instruction.md:111-118` | PASS | Preserved as `> **Author note:** ...`. |
| Excluded comment headings | `02_data_characterization.tex:218-263` | Converted body | PASS | `Assessing Data Suitability and Generation Methodology` and `A Multi-Fidelity Curriculum Learning Framework` are absent. |

### 03_data_glimpse.tex - A Glimpse at the Data

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-03-000 | text | INFO | `03_data_glimpse.tex:1-80` | `ctl_instruction.md:269-338` | Initial-condition sample, Brutus-output sample, file glob references, and listing labels are preserved. | No fix needed |

| Check item | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| Initial-condition file glob | `03_data_glimpse.tex:7` | `ctl_instruction.md:277` | PASS | `ic_hierarchical_*.txt` remains visible as a link. |
| Brutus-output file glob | `03_data_glimpse.tex:24` | `ctl_instruction.md:293` | PASS | `brutus_hierarchical_*.txt` remains visible as a link. |
| Initial-condition listing | `03_data_glimpse.tex:13-21` | `ctl_instruction.md:285-288` | PASS | Numeric sample preserved. |
| Brutus-output listing | `03_data_glimpse.tex:43-77` | `ctl_instruction.md:318-335` | PASS | Header/body snapshot structure preserved. |

### 04_phase1_data_prep.tex - Phase 1 - Data Preparation and Stratification

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-04-001 | comment | MINOR | `04_phase1_data_prep.tex:79-81` | `ctl_instruction.md:415-418` | Visible Step 2.5 `\authcomment{...}` was rendered as a Pandoc style span and introduced word-join spacing errors. | Fixed |
| CTL-04-002 | comment | MINOR | `04_phase1_data_prep.tex:397`, `04_phase1_data_prep.tex:406`, `04_phase1_data_prep.tex:434`, `04_phase1_data_prep.tex:519`, `04_phase1_data_prep.tex:549` | `ctl_instruction.md:652-795` | Visible section 04 `\authcomment{...}` notes were rendered as Pandoc style spans rather than plain visible markdown notes. | Fixed |
| CTL-04-003 | comment | INFO | `04_phase1_data_prep.tex:245-290` | Converted body | Excluded velocity-position angle comment block is absent from the converted body. | Verified |

| Formula ID | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| `item:eqs` | `04_phase1_data_prep.tex:113-129` | `ctl_instruction.md:451-461` | PASS | Total energy, potential energy, virial ratio, and `s_min` formulas preserved with `item:eqs` anchor. |
| `item:lnorm` | `04_phase1_data_prep.tex:131-146` | `ctl_instruction.md:463-483` | PASS | Angular momentum, characteristic scales, `L_max`, and `L_norm` formulas preserved with `item:lnorm` anchor. |
| `item:inorm` | `04_phase1_data_prep.tex:172-185` | `ctl_instruction.md:488-499` | PASS | Inertia tensor and normalized inertia formulas preserved with `item:inorm` anchor and reference to `item:lnorm`. |
| Shape invariants | `04_phase1_data_prep.tex:232-241` | `ctl_instruction.md:567-582` | PASS | `I_1`, `I_2`, and `I_3` formulas preserved. |
| `item:lyap` | `04_phase1_data_prep.tex:293-391` | `ctl_instruction.md:542-649` | PASS | Rosenstein-style estimator steps and code listing preserved with `item:lyap` anchor. |
| Normalization formulas | `04_phase1_data_prep.tex:471-516` | `ctl_instruction.md:719-746` | PASS | Component-wise normalization code and normalized-scale formulas preserved. |
| Input vector formulas | `04_phase1_data_prep.tex:575-603` | `ctl_instruction.md:797-827` | PASS | Time normalization, IC vector, input vector, and `t'` formula preserved. |

| Check item | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| Heading hierarchy | `04_phase1_data_prep.tex:1,5,52,78,99,421,610` | `ctl_instruction.md:336,341,384,413,429,676,829` | PASS | Section, Step 1, Step 2, Step 2.5, Step 3, Step 4, and Step 5 preserved. |
| Labels and refs | `sec:ctl:step3`, `item:eqs`, `item:lnorm`, `item:inorm`, `item:lyap`, `Item~\ref{item:lnorm}` | `ctl_instruction.md:429,451,463,488,542,495` | PASS | Labels preserved or mapped to markdown anchors/references. |
| Visible author notes | `04_phase1_data_prep.tex:79,397,406,434,519,549` | `ctl_instruction.md:415,652,654,692,748,791` | PASS | Preserved as plain `> **Author note:** ...` blocks. |

### 05_phase2_training_loop.tex - Phase 2 - The Definitive CTL-PINN Training Loop

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-05-001 | comment | MINOR | `05_phase2_training_loop.tex:3-13` | `ctl_instruction.md:840-856` | Visible opening `\authcomment{...}` was rendered as a Pandoc style span rather than a plain visible markdown note. | Fixed |
| CTL-05-002 | table | MINOR | `05_phase2_training_loop.tex:105-116` | `ctl_instruction.md:971-976` | Mini-batch composition table was preserved but rendered as an alignment table that was hard to scan. | Fixed |
| CTL-05-003 | table | MINOR | `05_phase2_training_loop.tex:125-135` | `ctl_instruction.md:986-990` | Curriculum-aware clipping table was preserved but rendered as an alignment table that was hard to scan. | Fixed |
| CTL-05-004 | comment | MINOR | `05_phase2_training_loop.tex:166-174` | `ctl_instruction.md:1024-1034` | Visible stage-transition `\authcomment{...}` was rendered as a Pandoc style span rather than a plain visible markdown note. | Fixed |
| CTL-05-005 | table | MINOR | `05_phase2_training_loop.tex:203-214` | `ctl_instruction.md:1065-1071` | Consolidated hyperparameter schedule was preserved but rendered as an alignment table that was hard to scan. | Fixed |
| CTL-05-006 | comment | INFO | `05_phase2_training_loop.tex:51-58`, `05_phase2_training_loop.tex:237-643` | Converted body | Excluded training-loop comment ranges are absent from the converted body. | Verified |

| Formula/Table ID | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| Total loss | `05_phase2_training_loop.tex:44-49` | `ctl_instruction.md:917-921` | PASS | Total loss formula and stage index `k` preserved. |
| ALM multiplier update | `05_phase2_training_loop.tex:65-80` | `ctl_instruction.md:923-935` | PASS | `lambda_p`, `v_p`, and `mu_p` updates preserved. |
| Mini-batch composition | `05_phase2_training_loop.tex:105-116` | `ctl_instruction.md:971-976` | PASS | Replay and lookahead rows preserved in a readable markdown table. |
| Adaptive clipping schedule | `05_phase2_training_loop.tex:125-135` | `ctl_instruction.md:986-990` | PASS | Stage bands and clipping constants preserved. |
| Termination criterion | `05_phase2_training_loop.tex:138-141` | `ctl_instruction.md:992-995` | PASS | Plateau derivative formula preserved. |
| Stage-transition criteria | `05_phase2_training_loop.tex:176-199` | `ctl_instruction.md:1039-1061` | PASS | Training loss, validation loss, physics residual, and energy-drift formulas preserved. |
| Consolidated hyperparameter schedule | `05_phase2_training_loop.tex:203-214` | `ctl_instruction.md:1065-1071` | PASS | Stage rows, Adam LR, clip `C`, energy weight, and L-BFGS type preserved. `tab:C_schedule` occurs only in the excluded comment range and is documented here rather than added to the converted body. |

### 06_advanced_considerations.tex - Advanced Considerations and Best Practices

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-06-001 | comment | MINOR | `06_advanced_considerations.tex:15` | `ctl_instruction.md:1127-1131` | Visible `\authcomment{...}` under Prediction Horizon was rendered inline as a Pandoc style span rather than a plain visible markdown note. | Fixed |

| Check item | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| Evaluation metrics list | `06_advanced_considerations.tex:5-34` | `ctl_instruction.md:1112-1162` | PASS | Conservation, prediction horizon, long-term statistics, and short-term error metrics preserved. |
| Prediction-horizon author note | `06_advanced_considerations.tex:15` | `ctl_instruction.md:1127-1131` | PASS | Preserved as `> **Author note:** ...`. |
| Reproducibility content carried in source file | `06_advanced_considerations.tex:39-68` | `ctl_instruction.md:1177-1209` | PASS | Reproducibility heading, Hydra YAML stack, and launch command preserved. |

### 07_reproducibility.tex - Reproducibility Note

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-07-000 | structure | INFO | `07_reproducibility.tex:1` | `ctl_instruction.md:1177-1209` | File is empty in the modular source; the reproducibility section appears in `06_advanced_considerations.tex` and is preserved there. | No fix needed |

### appendix.tex - Supplementary Figures

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| CTL-A-000 | figure | INFO | `appendix.tex:2-69` | `ctl_instruction.md:1211-1231` | Both figure captions and labels are represented in markdown as HTML figure blocks. | No fix needed |

| Check item | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| Figure `fig:step2_data_workflow` | `appendix.tex:28-30` | `ctl_instruction.md:1213-1219` | PASS | Caption and label preserved. |
| Figure `fig:step2to5_workflow` | `appendix.tex:65-66` | `ctl_instruction.md:1221-1231` | PASS | Caption, label, and reference to `fig:step2_data_workflow` preserved. |

## Fix Log

| ID | Section | Fix summary |
|---|---|---|
| CTL-10-01-BASELINE | Candidate selection | Created candidate comparison, selected existing `ctl_instruction.md`, and recorded comment-exclusion ranges. |
| CTL-02-001 | `02_data_characterization.tex` | Rebuilt `tab:brutus_compare` as a readable markdown table while preserving label, caption, rows, and numeric values. |
| CTL-02-002 | `02_data_characterization.tex` | Converted visible author note from Pandoc style span to a plain markdown author-note blockquote. |
| CTL-04-001 | `04_phase1_data_prep.tex` | Converted Step 2.5 author note to a plain markdown blockquote and repaired conversion-only spacing joins in the note text. |
| CTL-04-002 | `04_phase1_data_prep.tex` | Converted remaining visible section 04 author notes to plain markdown blockquotes. |
| CTL-05-001 | `05_phase2_training_loop.tex` | Converted opening training-loop author note to a plain markdown blockquote. |
| CTL-05-002 | `05_phase2_training_loop.tex` | Rebuilt mini-batch composition as a readable markdown table. |
| CTL-05-003 | `05_phase2_training_loop.tex` | Rebuilt curriculum-aware clipping schedule as a readable markdown table. |
| CTL-05-004 | `05_phase2_training_loop.tex` | Converted stage-transition author note to a plain markdown blockquote. |
| CTL-05-005 | `05_phase2_training_loop.tex` | Rebuilt consolidated hyperparameter schedule as a readable markdown table. |
| CTL-06-001 | `06_advanced_considerations.tex` | Converted Prediction Horizon author note to a plain markdown blockquote inside the list item. |

## Source Issues / Notes for Future Reconciliation

| ID | Source section | Markdown heading | Note |
|---|---|---|---|
| SI-CTL-001 | `04_phase1_data_prep.tex`, `05_phase2_training_loop.tex`, `appendix.tex` | `Step 4: Formulating the Input Vector`, `Data Flow During Training`, `Supplementary Figures` | The source alternates between 11/12-dimensional and 13/14-dimensional input-vector descriptions. The converted body preserves the LaTeX source exactly; the appended note in `ctl_instruction.md` is metadata for future reconciliation. |

## Final Verification

- Open discrepancies: 0
- Zero open discrepancies: yes
- Converted body excludes appended source-issue metadata from fidelity comparison: yes
- Fix log complete: yes
