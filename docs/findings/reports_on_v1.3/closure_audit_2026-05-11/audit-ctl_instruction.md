---
pair: ctl_instruction
markdown_file: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
latex_root: pinn_instruction/original_latex/framework-specs/ctl-instruction/main_CTL.tex
audit_date: 2026-05-11
auditor: closure-audit-agent
verdict: PASS_WITH_NOTES
findings_critical: 0
findings_major: 1
findings_minor: 1
findings_info: 5
deletion_verdicts:
  - file: docs/findings/reports_on_v1.3/audit_2026-05-07/audit-ctl_instruction.md
    verdict: SAFE_TO_DELETE
    rationale: Superseded by this closure audit; all 12 findings reconciled and re-verified against current file state
  - file: pinn_instruction/markdown_conversion/verification_reports/ctl_instruction_verification_report.md
    verdict: SAFE_TO_DELETE
    rationale: Superseded by two rounds of audit; F1/recall scoring captured in embedded evidence below
---

## Executive Summary

This closure audit re-verifies `ctl_instruction.md` against its LaTeX source (`main_CTL.tex` plus 8 `\include{}`d section files plus `preamble_CTL.tex`) and reconciles all findings from three prior reports: the 2026-05-07 per-pair audit (12 findings), the MASTER-AUDIT-v1.3.md (cross-pair synthesis), and the verification report (18 pre-existing items).

The markdown is a **substantively faithful** conversion of the LaTeX source. All titles, authorship metadata, section headings, equations (52+ expressions), tables (4), code listings (8), numeric threshold values, stage criteria, and visible `\authcomment{}` blocks (8) were verified line-by-line against the LaTeX sources. No CRITICAL mathematical errors, missing sections, or corrupted values were found.

Since the prior audit (2026-05-07), a targeted fix wave (Phase 15.1-03, Tasks 1-6, commits `58ae45c` through `08e4433`) resolved 6 of 7 prior MINOR findings: Pandoc anchor placeholders removed, code-fence attribute strings stripped, `{.uri}` class artifacts cleaned, escaped `\"` quotes restored, and empty TikZ figure blocks replaced with descriptive blockquote notes. The remaining prior MINOR (Source Issues appendix) and all five prior INFO findings persist as non-defect observations.

However, the cross-reference fix (Task 2, commit `f4027cd`) introduced a **regression**: the `Item~\ref{item:eqs}` replacement at md:656-657 produced duplicated text, a broken epsilon symbol (`$varepsilon$` missing backslash), and a truncated sentence missing the final clause "enter $s_{\min}$ or any denominator besides $V$". This is the sole MAJOR finding, confined to two lines with a one-line fix.

**Bottom line:** PASS_WITH_NOTES. Zero CRITICAL defects. One MAJOR regression (newly discovered, localized). One MINOR (editorial appendix, known). Five INFO (non-defect observations). The path to PASS is a single 3-line edit.

## Findings

### MAJOR

**ID**: CTL-CLOSURE-MAJ-001
**Description**: Regression from cross-reference fix commit `f4027cd` -- garbled paragraph with duplicated text, broken epsilon symbol, and truncated sentence in the Numerical Notes subsection.
**Location**: `ctl_instruction.md:655-657`
**LaTeX** (`sections/04_phase1_data_prep.tex:408-410`):
```latex
Unless otherwise specified, use double precision for all invariants. The softening
$\varepsilon=10^{-10}$ in Item~\ref{item:eqs} is a safe default in scaled units and
\emph{does not} enter $s_{\min}$ or any denominator besides $V$.
```
**Markdown** (`ctl_instruction.md:655-657`):
```
Unless otherwise specified, use double precision for all invariants. The
softening $\varepsilon=10^{-10}$ in
softening $varepsilon=10^{-10}$ in the total energy definition (see above) is a safe default in scaled units and *does not*
```
**Verdict**: NEW (regression introduced by fix commit `f4027cd`)

**Defects identified:**
1. Line 656 is a duplicate fragment: "softening $\varepsilon=10^{-10}$ in" -- the edit failed to merge this with the replacement line.
2. Line 657: `$varepsilon=10^{-10}$` is missing the LaTeX backslash -- should be `$\varepsilon=10^{-10}$`.
3. The sentence is truncated at "*does not*" -- missing the final clause "enter $s_{\min}$ or any denominator besides $V$".
4. The original LaTeX cross-reference `Item~\ref{item:eqs}` was replaced with an overreaching substitution. The fix commit's diff shows `old_string` included the entire tail of the sentence (including "enter $s_{\min}$...") but `new_string` omitted it.

**Required fix (replace md:655-657):**
```
Unless otherwise specified, use double precision for all invariants. The
softening $\varepsilon=10^{-10}$ in the total energy definition (see above) is a safe default in scaled units and *does not* enter $s_{\min}$ or any denominator besides $V$.
```

### MINOR

**ID**: CTL-CLOSURE-MIN-001
**Description**: "Source Issues / Notes for Future Reconciliation" appendix has no LaTeX origin.
**Location**: `ctl_instruction.md:1211-1220`
**LaTeX**: (none -- editorial addition with no LaTeX counterpart)
**Markdown** (`ctl_instruction.md:1211-1220`):
```
# Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the converted source body and are excluded from fidelity comparison in `ctl_instruction_verification_report.md`.

## SI-CTL-001: Input-vector dimensionality inconsistency
...
```
**Verdict**: STILL_OPEN -- Carried forward from prior Finding 1. The section was not addressed by the 15.1-03 fix wave and remains in the markdown body. The section self-identifies as metadata and explicitly states it is excluded from fidelity comparison. Low risk. Cross-pair consistency decision pending (retain vs. remove vs. sidecar).

### INFO

**ID**: CTL-CLOSURE-INFO-001
**Description**: `\DeclareMathOperator{\median}{median}` from LaTeX preamble emitted as `\mathop{\mathrm{median}}` -- visually and semantically equivalent.
**Location**: `ctl_instruction.md:405, 407`; LaTeX: `preamble_CTL.tex:30` and `04_phase1_data_prep.tex:71-72`
**Prior Finding**: 8 (2026-05-07 audit)
**Verdict**: STILL_OPEN -- Not a defect. No fix needed.

**ID**: CTL-CLOSURE-INFO-002
**Description**: LaTeX source itself oscillates between describing an 11/12-dimensional input vector and a 13/14-dimensional input vector. Markdown preserves this source-level inconsistency faithfully.
**Location**: `ctl_instruction.md:447, 557, 583-593, 597, 800, 884`; LaTeX: `04_phase1_data_prep.tex:426, 556, 582, 597` and `05_phase2_training_loop.tex:29`
**Prior Finding**: 9 (2026-05-07 audit)
**Verdict**: STILL_OPEN -- Source-level issue, not a conversion defect. Documented in SI-CTL-001.

**ID**: CTL-CLOSURE-INFO-003
**Description**: `07_reproducibility.tex` is empty in the modular LaTeX source (1 byte newline only). Actual reproducibility content lives in `06_advanced_considerations.tex:39-68` and is faithfully rendered under `# Reproducibility Note (Ignore Now and Come Back Later)` in the markdown.
**Location**: LaTeX: `sections/07_reproducibility.tex` (empty); Markdown: `ctl_instruction.md:1172`
**Prior Finding**: 10 (2026-05-07 audit)
**Verdict**: STILL_OPEN -- Correctly handled. No fix needed.

**ID**: CTL-CLOSURE-INFO-004
**Description**: LaTeX source uses hard-coded `\S4.4` cross-reference with no matching labeled section. Markdown preserves verbatim as `§4.4`.
**Location**: `ctl_instruction.md:444`; LaTeX: `sections/04_phase1_data_prep.tex:114`
**Prior Finding**: 11 (2026-05-07 audit)
**Verdict**: STILL_OPEN -- Source-level issue. Markdown faithfully preserves the source text.

**ID**: CTL-CLOSURE-INFO-005
**Description**: Code listings inside enumerated items carry a 4-space leading indent inherited from LaTeX `lstlisting` placement inside `enumerate`. This is semantically faithful and renders identically.
**Location**: `ctl_instruction.md:502-525, 580-646`; LaTeX: `sections/04_phase1_data_prep.tex:188-227, 310-388`
**Prior Finding**: 12 (2026-05-07 audit)
**Verdict**: STILL_OPEN -- No fix needed. Informational only.

## Reconciliation Table

### From audit_2026-05-07/audit-ctl_instruction.md (per-pair audit, 12 findings)

| Prior Finding ID | Severity | Current Status | Evidence |
|---|---|---|---|
| Finding 1 | MINOR | STILL_OPEN (→ CTL-CLOSURE-MIN-001) | Source Issues appendix at md:1211-1220, unchanged. Intentional editorial metadata. |
| Finding 2 | MINOR | RESOLVED | Commit `58ae45c` removed all 4 `[]{#item:*}` anchor placeholders. Verified absent at md:451, 463, 488, 542. |
| Finding 3 | MINOR | REGRESSED (→ CTL-CLOSURE-MAJ-001) | Commit `f4027cd` fixed item:lnorm (md:493: "the normalized angular momentum (see above)") but botched item:eqs (md:656-657: garbled text, broken epsilon, truncated sentence). |
| Finding 4 | MINOR | RESOLVED | Commit `34c30ea` replaced all 8 pandoc fence openings with ` ```python `. Verified at md:282, 312, 476, 502, 580, 695, 722, 802. |
| Finding 5 | MINOR | RESOLVED | Commit `825f6c2` stripped `{.uri}` class from 2 headings. md:270, 286 now plain text in parentheses. |
| Finding 6 | MINOR | RESOLVED | Commit `96fe7b1` replaced 7 escaped `\"` with plain `"`. Verified at md:48, 49, 57, 69, 117, 118, 1139. |
| Finding 7 | MINOR | RESOLVED (IMPROVED) | Commit `08e4433` replaced empty `<figure>` blocks with descriptive blockquote notes at md:1207-1209. Captions preserved; diagram nodes summarized in prose. |
| Finding 8 | INFO | STILL_OPEN (→ CTL-CLOSURE-INFO-001) | `\median` → `\mathop{\mathrm{median}}` -- equivalent rendering. No fix needed. |
| Finding 9 | INFO | STILL_OPEN (→ CTL-CLOSURE-INFO-002) | 11/12/13/14-D inconsistency preserved from source. |
| Finding 10 | INFO | STILL_OPEN (→ CTL-CLOSURE-INFO-003) | Empty `07_reproducibility.tex` correctly handled. |
| Finding 11 | INFO | STILL_OPEN (→ CTL-CLOSURE-INFO-004) | `\S4.4` cross-reference preserved verbatim. Source-level issue. |
| Finding 12 | INFO | STILL_OPEN (→ CTL-CLOSURE-INFO-005) | Code listing indentation preserved. No fix needed. |

### From MASTER-AUDIT-v1.3.md (cross-pair synthesis, ctl_instruction-relevant items)

| Prior Finding ID | Current Status | Evidence |
|---|---|---|
| P5 (Source Issues appendix inconsistency) | STILL_OPEN | md:1211-1220 retained. Inconsistent with pairs where it was removed (review_of_framework, sampling_method, stage_strat_revision). Policy decision pending. |
| P6 (Pandoc conversion artifacts) | RESOLVED | All 5 prior pandoc artifact types (anchors, xref plumbing, fence attributes, URI class, escaped quotes) removed by 15.1-03 fix wave. Xref fix introduced regression (CTL-CLOSURE-MAJ-001). |
| P7 (TikZ figures lost) | RESOLVED | md:1207-1209 -- blockquote notes replace empty HTML. Captions preserved. |
| P8 (\authcomment color stripping) | NOT APPLICABLE | ctl_instruction uses plain `> **Author note:**` blockquotes. No `<span style="color: red">` spans. Consistent with markdown convention. |

### From ctl_instruction_verification_report.md (pre-existing items, re-verified)

All 23 verification-report items (CTL-01-000 through CTL-A-000 plus formula blocks and SI-CTL-001) were re-verified against the current file:

| Category | Items | Verdict |
|---|---|---|
| Section headings (8 sections) | CTL-01-000, CTL-03-000, CTL-07-000 | All RESOLVED -- headings match LaTeX source |
| Tables (4) | CTL-02-001, CTL-05-002, CTL-05-003, CTL-05-005 | All RESOLVED -- cell-by-cell match against LaTeX |
| Authcomments (8) | CTL-02-002, CTL-04-001, CTL-04-002, CTL-05-001, CTL-05-004, CTL-06-001 | All RESOLVED -- rendered as `> **Author note:**` blockquotes |
| Excluded comment ranges (5) | CTL-02-003, CTL-04-003, CTL-05-006 | All RESOLVED -- confirmed absent from markdown body |
| Formula blocks (7) | item:eqs, item:lnorm, item:inorm, shape invariants, item:lyap, normalization, input vector | All RESOLVED -- symbol-by-symbol match against LaTeX source |
| Appendix figures | CTL-A-000 | RESOLVED (IMPROVED) -- blockquote notes replace empty `<figure>` blocks |
| Source Issues | SI-CTL-001 | STILL_OPEN -- source-level inconsistency, documented in markdown |

### Spot-check: all numerical thresholds verified unchanged

Every numerical threshold was re-verified against the current file. All match the LaTeX source:

| Threshold | LaTeX source | Markdown | Status |
|---|---|---|---|
| Stage 0: E < -0.5 | 02_data_characterization.tex:86 | md:128 | MATCH |
| Stage 0: L/L_max > 0.5 | 02_data_characterization.tex:87 | md:130 | MATCH |
| Stage 0: 0.7 ≤ Q ≤ 1.3 | 02_data_characterization.tex:88 | md:132 | MATCH |
| Stage 0: s_min > 2 | 02_data_characterization.tex:89 | md:134 | MATCH |
| Stage 1a: -0.5 ≤ E < -0.1 | 02_data_characterization.tex:104 | md:148 | MATCH |
| Stage 1b: 0.1 ≤ L/Lmax < 0.5 | 02_data_characterization.tex:117 | md:165 | MATCH |
| Stage 3: 0.9 ≤ Q ≤ 1.1 | 02_data_characterization.tex:151 | md:199 | MATCH |
| Stage 4a: τ_L > 5 | 02_data_characterization.tex:167 | md:213 | MATCH |
| Stage 4b: 2 < τ_L ≤ 5 | 02_data_characterization.tex:177 | md:224 | MATCH |
| Stage 6: s_min < 0.5 or \|E\| < 0.01 | 02_data_characterization.tex:199 | md:242 | MATCH |
| ε (softening) = 10^{-10} | 04_phase1_data_prep.tex:128 | md:458-459 | MATCH |
| E_scale: \|median({E_j})\| + 10^{-10} | 04_phase1_data_prep.tex:71 | md:405 | MATCH |
| Q_scale = 0.5 (fixed) | 04_phase1_data_prep.tex:74 | md:411 | MATCH |
| ALM: β=0.99, γ=0.01, ε=1e-8 | 05_phase2_training_loop.tex:79 | md:929 | MATCH |
| Adam: β1=0.9, β2=0.999, ε=1e-8 | 05_phase2_training_loop.tex:95 | md:954-955 | MATCH |
| LR_k = 10^{-3} × (0.7)^k | 05_phase2_training_loop.tex:93 | md:949 | MATCH |
| Batch: B_≤k=240, B_k+1=16 | 05_phase2_training_loop.tex:111-112 | md:967-968 | MATCH |
| Clip C: 7-10, 5, 3 | 05_phase2_training_loop.tex:131-133 | md:982-984 | MATCH |
| Plateau: d(log10 L_phys)/d(epoch) > -5×10^{-3} for 50 | 05_phase2_training_loop.tex:141 | md:989 | MATCH |
| L-BFGS early: history=10, Wolfe, max 20-50 | 05_phase2_training_loop.tex:154 | md:1003-1004 | MATCH |
| sL-BFGS later: batch=32, interval=10 | 05_phase2_training_loop.tex:160-161 | md:1010-1011 | MATCH |
| Transition: β=0.98, patience=200, ε_train=10^{-5} | 05_phase2_training_loop.tex:181 | md:1039 | MATCH |
| Transition: ε_phys=10^{-4}, ε_energy=10^{-4} | 05_phase2_training_loop.tex:192,199 | md:1050,1055 | MATCH |
| L-BFGS: Full-Batch (0-1), Full-Batch/sL-BFGS (2-3), sL-BFGS (4-6) | 05_phase2_training_loop.tex:209-211 | md:1061-1063 | MATCH |
| λ_E: 10^{k-3} | 05_phase2_training_loop.tex:209-211 | md:1061-1063 | MATCH |

## Embedded Evidence from Prior Reports

### From audit_2026-05-07/audit-ctl_instruction.md

The prior auditor verified all 12 findings listed in the reconciliation table above. Re-verification in this closure audit confirms those findings remain accurate for the current file state. No unique byte-level or hex evidence requiring verbatim preservation beyond what is captured in the reconciliation table and findings sections above.

### From MASTER-AUDIT-v1.3.md (ctl_instruction-relevant excerpts)

Per the master audit verdict matrix:
> | # | Pair | Status | CRITICAL | MAJOR | MINOR | INFO |
> |---|------|--------|---------:|------:|------:|-----:|
> | 1 | ctl_instruction | PASS_WITH_NOTES | 0 | 0 | 7 | 5 |

Per the master audit cross-cutting patterns:
- **P5**: "Source Issues / Notes for Future Reconciliation" appendix retained at ctl_instruction.md:1233-1242. STATUS 2026-05-11: STILL_OPEN (md:1211-1220, unchanged).
- **P6**: Pandoc conversion artifacts concentrated in ctl_instruction. STATUS 2026-05-11: 5 of 6 artifact types RESOLVED; cross-reference fix REGRESSED (CTL-CLOSURE-MAJ-001).
- **P7**: TikZ figures lost. STATUS 2026-05-11: RESOLVED -- blockquote notes replace empty HTML.
- **P8**: \authcomment{} color stripping -- not flagged for ctl_instruction.

Per the master audit prioritized fix list relevant to ctl_instruction:
- Wave C (MINOR sweeps): Pandoc artifact strip on ctl_instruction -- COMPLETED (Tasks 1-6).
- Wave D (Optional): TikZ diagram restoration -- COMPLETED (Task 6, blockquote notes). Source Issues appendix policy -- PENDING.

### From ctl_instruction_verification_report.md

The automated F1/recall scoring from the candidate comparison table:

| Candidate | Overall score | Rank | Notes |
|---|---|---|---|
| `ctl_instruction.md` (selected) | 0.958 F1 / 0.958 recall | 2 raw / 1 selected | Best section 04 preservation |
| `ctl_instruction_v2.md` | 0.890 F1 / 0.909 recall | 3 | Lower recall in sections 03-05 |
| `pandoc_conversion/CTL-instruction-final.md` | 0.959 F1 / 0.947 recall | 1 raw / 2 selected | Better F1, lower recall than selected |

Per-section recall scores:
- Section 01: 1.000 | Section 02: 0.992 | Section 03: 1.000 | Section 04: 0.999 | Section 05: 0.990 | Section 06: 1.000 | Section 07: N/A (empty source) | Appendix: 0.577

Excluded comment ranges (all confirmed still absent from current markdown):

| LaTeX source range | Excluded content | Status |
|---|---|---|
| `02_data_characterization.tex:218-232` | Assessing Data Suitability and Generation Methodology | Confirmed absent |
| `02_data_characterization.tex:235-263` | A Multi-Fidelity Curriculum Learning Framework | Confirmed absent |
| `04_phase1_data_prep.tex:245-290` | Velocity-position angle item and code | Confirmed absent |
| `05_phase2_training_loop.tex:51-58` | Energy regularizer subsection | Confirmed absent |
| `05_phase2_training_loop.tex:237-643` | Older training-loop revision (407 lines) | Confirmed absent |

## Source Issues / Notes

### SI-CTL-001: Input-vector dimensionality inconsistency (source-level, preserved)

- **Source sections:** `04_phase1_data_prep.tex`, `05_phase2_training_loop.tex`, `appendix.tex`
- **Markdown locations:** `ctl_instruction.md:447, 557, 583-593, 597, 800, 884, 1216-1220`
- **Note:** The LaTeX source alternates between describing an 11-component IC plus time as a 12-dimensional input and a 13-component IC plus time as a 14-dimensional input. All instances are preserved faithfully in the markdown and documented in the SI-CTL-001 note at md:1216-1220. This should be reconciled against the canonical PINN input-vector definition in `pinn/data-processing-pipeline-full.py` in a future source-level update.

### SI-CTL-002: `\S4.4` hard-coded cross-reference (source-level, preserved)

- **Source section:** `04_phase1_data_prep.tex:114`
- **Markdown location:** `ctl_instruction.md:444`
- **Note:** The LaTeX source uses `\S4.4` to reference the stage-assignment section, but no section in the document carries the "4.4" numbering. Markdown preserves this verbatim. Should be replaced with a proper `\ref{}` in a future source-level update.

### SI-CTL-003: Regression risk from Pandoc artifact cleanup (methodology note)

- **Source commit:** `f4027cd` (Task 2: replace pandoc cross-reference artifacts)
- **Note:** The edit operation used to fix Pandoc cross-reference artifacts produced garbled text when the old_string/new_string boundaries did not properly account for surrounding line breaks and LaTeX math delimiters. The item:lnorm fix at md:493 was clean; the item:eqs fix at md:656-657 was not. Future Pandoc artifact cleanup passes should verify not only that the target artifact is removed but also that adjacent text lines, math tokens (especially backslash-escaped symbols like `\varepsilon`), and sentence endings remain intact. This finding is specific to ctl_instruction.md but the methodology note applies to all 6 pairs.
