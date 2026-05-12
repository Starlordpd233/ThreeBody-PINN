---
pair: stage_strat_revision
markdown_file: pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md
latex_root: pinn_instruction/original_latex/framework-revisions/review-of-framework/stage_strat_revision/stage_strat_revision.tex
audit_date: 2026-05-11
auditor: closure-audit-agent
verdict: PASS_WITH_NOTES
findings_critical: 0
findings_major: 2
findings_minor: 2
findings_info: 5
deletion_verdicts:
  - file: docs/findings/reports_on_v1.3/audit_2026-05-07/audit-stage_strat_revision.md
    verdict: SAFE_TO_DELETE
    rationale: All 16 findings reconciled in this closure audit; pair-specific evidence fully incorporated below.
  - file: docs/findings/reports_on_v1.3/audit_2026-05-07/MASTER-AUDIT-v1.3.md
    verdict: KEEP_AS_HISTORICAL
    rationale: Cross-pair master audit covering all 6 conversion pairs; contains cross-cutting analysis and Wave A/B/C fix prioritization not replicated here.
  - file: docs/findings/reports_on_v1.3/previous_audits/stage_strat_revision.md
    verdict: SAFE_TO_DELETE
    rationale: All 6 issues reconciled below; tab-byte fix verification and proposed-fix text captured in Embedded Evidence section.
  - file: pinn_instruction/markdown_conversion/verification_reports/stage_strat_revision_verification_report.md
    verdict: KEEP_AS_HISTORICAL
    rationale: Phase 14 verification report documents the pandoc conversion workflow, per-section audit results, and fix log (SSR-14-NN-NN IDs); historically significant for conversion provenance.
---

## Executive Summary

This closure audit evaluates the current state (2026-05-11) of `stage_strat_revision.md` against its LaTeX source after Phase 15.1 fix waves (A, B, C). Of the 16 findings from the prior May 7 audit and 6 findings from the earlier report, **the vast majority are RESOLVED**: title, abstract, heading hierarchy, Phase II intro paragraph, Table 3 format, bibliography heading, author/date, TOC, tab-byte corruption in Table 4, and all pandoc artifacts have been fixed. Math, tables, code, and bibliography content are fully faithful to source.

However, **one CRITICAL regression** was introduced during Phase 15.1 Wave A: the `\authcomment{}` rendering (`**[I'm not sure what this s is referring to...]**`) was deleted and never restored. Additionally, the restored Source Issues section is now stale (it claims the authcomment renders as bold text in the markdown, which is no longer true) and omits the documented I3 schema inconsistency. Two long-standing MINOR issues (unresolvable "Section 1.2" cross-reference, missing Part labels in H1 headings) also persist.

**Verdict: FAIL** -- the deleted authcomment is a content fidelity regression that must be fixed before this conversion can claim to be a faithful representation of the LaTeX source. All other content is PASS-quality with only cosmetic MINOR notes.

## Findings

### CRITICAL

**C-1: `\authcomment{}` content deleted (REGRESSION)**

- **Category:** Content omission
- **Markdown loc:** between lines 136 and 138 (absent)
- **LaTeX loc:** `sections/algorithmic_workflow.tex:34`
- **LaTeX source:** `\authcomment{I'm not sure what this s is referring to. Should we look for the exact value used in the sampling script?}`
- **Defect:** Before Phase 15.1 Wave A (commit `ef79bd0`), the markdown contained the rendered authcomment as `**[I'm not sure what this s is referring to. Should we look for the exact value used in the sampling script?]**` at line 111 of the old file. Wave A commit `ef79bd0` deleted this line (visible in `git diff ef79bd0^..ef79bd0`) and it was never restored in subsequent Waves B or C.
- **Impact:** A LaTeX-author comment present in the source document is entirely absent from the markdown conversion. The preamble defines `\authcomment` as `\textcolor{red}{\textbf{[#1]}}` -- this is structured, intentional content in the LaTeX source, not a formatting artifact.
- **Evidence (git):**
  ```
  $ git show ef79bd0^:pinn_instruction/markdown_conversion/stage_strat_revision.md | grep -n "not sure"
  111:**[I'm not sure what this s is referring to. Should we look for the exact value used in the sampling script?]**
  ```
  The current file has no match for "I'm not sure" or "not sure what this" anywhere.
- **Recommended fix:** Re-insert `**[I'm not sure what this s is referring to. Should we look for the exact value used in the sampling script?]**` between the normalized virial ratio definition (end of line 136) and the "Contingency Plan" paragraph (line 138), matching its position in `algorithmic_workflow.tex:34`.

### MAJOR

**M-1: Source Issues section is stale (references deleted content)**

- **Category:** Metadata accuracy
- **Markdown loc:** line 421
- **Defect:** The Source Issues section states: "The single `\authcomment{}` at `algorithmic_workflow.tex:34` renders as bold text in the markdown, which is acceptable per D-58 and does not require separate documentation." This statement is factually incorrect -- the authcomment no longer renders as bold text in the markdown because it was deleted (see C-1).
- **Recommended fix:** Update the Source Issues section to either (a) document that the authcomment was intentionally removed with rationale, or (b) note it was restored and renders as bold text, depending on resolution of C-1.

**M-2: Source Issues section omits documented I3 schema inconsistency**

- **Category:** Metadata completeness
- **Markdown loc:** lines 419-421 (Source Issues section) vs. lines 151-152 (body text blockquote)
- **Defect:** The Source Issues section opens with "No source-level issues identified during Phase 14 audit." However, the body text at lines 151-152 contains a detailed blockquote documenting a source-document inconsistency: the Phase I "Invariant Calculation" body text enumerates Shape Invariants as `I1, I2, I3` but the DataFrame schema table only has `I1, I2` columns (no `I3`). This is a bona fide source-level issue that should be cross-referenced from the Source Issues section.
- **Recommended fix:** Add a brief note in the Source Issues section referencing the I3 schema inconsistency documented in the body, or update the "No source-level issues" claim.

### MINOR

**M-N1: "Section 1.2" cross-reference is unresolvable in markdown**

- **Category:** Cross-references
- **Markdown loc:** line 130 -- "the full suite of physical invariants defined in Section 1.2."
- **LaTeX loc:** `sections/algorithmic_workflow.tex:21`
- **Defect:** LaTeX auto-numbers sections within each `\part{}`, so "Section 1.2" resolves in the PDF to Part I, Section 2 ("A Lexicon of Difficulty Metrics for the Three-Body Problem"). The markdown carries the prose forward but uses unnumbered headings, so the reader cannot resolve "Section 1.2".
- **Recommended fix:** Either add section numbers to all headings (mirroring PDF numbering) or rewrite the cross-reference as "the full suite of physical invariants defined in A Lexicon of Difficulty Metrics for the Three-Body Problem above."

**M-N2: Part labels missing from H1 headings**

- **Category:** Headings
- **Markdown loc:** lines 28, 108, 238, 381
- **LaTeX loc:** `\part{Foundational Principles...}`, `\part{A Revised Algorithmic Workflow...}`, `\part{Implementation and Validation Protocol}`, `\part{Conclusions and Recommendations}`
- **Defect:** The PDF renders "Part I", "Part II", "Part III", "Part IV" prominently before each `\part{}` title. The markdown TOC (lines 8-22) references "Part I", "Part II", etc., but the actual H1 headings (`# Foundational Principles...`) omit these labels.
- **Recommended fix:** Prefix the four `#` part headings with "Part I. ", "Part II. ", "Part III. ", "Part IV. " respectively.

### INFO

**I-1: All 13 MAJOR/CRITICAL findings from May 7 audit now RESOLVED**

The following findings from `audit_2026-05-07/audit-stage_strat_revision.md` are confirmed resolved:
- Finding 1 (CRITICAL): Title now present at line 1
- Finding 2 (CRITICAL): Abstract now present at lines 24-27
- Finding 3 (MAJOR): Phase I-IV headings promoted from `###` to `##`
- Finding 4 (MAJOR): Part III sections promoted from `###` to `##`
- Finding 5 (MAJOR): Subsections demoted from `####` to `###`
- Finding 6 (MAJOR): Phase II intro paragraph restored at line 157
- Finding 7 (MAJOR): Table 3 converted from pandoc grid to GFM pipe table (lines 184-192)
- Finding 8 (MAJOR): `## References` heading added at line 397
- Finding 9 (MAJOR): Author and date present at lines 2-4
- Finding 10 (MAJOR): Hand-curated TOC present at lines 6-22
- Finding 14 (INFO): Tab-byte corruption in Table 4 fixed (verified: lines 226-232 have correct `\tau_L` and `\text{norm}`)
- Finding 16 (INFO): No pandoc artifacts present (verified: zero hits for `\toprule`, `\midrule`, `\hypertarget`, `\hl{`, `reference-type="ref"`, `{#item:`, `{.uri}`, escaped `\[N\]`, escaped `\"`)

**I-2: No pandoc artifacts detected**

Full artifact scan results (all zero):
- `\toprule` / `\midrule` / `\bottomrule`: 0 hits
- `\hypertarget`: 0 hits
- `\hl{`: 0 hits
- `reference-type="ref"`: 0 hits
- `{#item:` anchor placeholders: 0 hits
- `{.uri}` class: 0 hits
- `{.python language="Python"}` code-fence attribute strings: 0 hits
- Escaped `\[N\]` citation brackets: 0 hits
- Escaped `\"` quotes: 0 hits
- `<span style="color: red">` spans: 0 hits (verified per audit spec item 16)

**I-3: No TikZ figures in LaTeX source**

This document contains no `\tikz` or `tikzpicture` environments. Audit spec item 14 is vacuously satisfied.

**I-4: All mathematical expressions match LaTeX source**

Spot-checked all 10 display equations and all inline math (30+ instances). All formulas are character-for-character faithful to the LaTeX source. Verified:
- Total Mechanical Energy (line 46): LaTeX-by-LaTeX match
- Virial Ratio (line 48): match
- Normalized Angular Momentum (line 50): match
- Minimum Initial Separation (line 52): match
- Lyapunov Time (line 54): match
- Shape Invariants I1, I2, I3 (line 56): match
- Virial scaling derivation (line 136): match
- Normalized virial ratio (line 136): match
- Validation loss L_data (line 375): match

All 4 tables verified cell-by-cell against LaTeX source. All 113 lines of Python code verified line-for-line.

**I-5: Em-dashes properly converted**

LaTeX `---` (em-dash) sequences converted to Unicode `—` (U+2014). Verified example: `foundational_principles.tex:72` `not excessively bound---a clear signature` rendered at line 82 as `not excessively bound—a clear signature`.

## Reconciliation Table

### From audit_2026-05-07/audit-stage_strat_revision.md (May 7, 2026)

| Prior Finding ID | Prior Report Source | Current Status + Evidence |
|---|---|---|
| Finding 1 (CRITICAL) — Missing title | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Title `# A Data-Driven Stage Assignment Framework for Curriculum Transfer Learning in N-Body Dynamics` present at line 1. |
| Finding 2 (CRITICAL) — Missing abstract | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Abstract present under `## Abstract` at lines 24-27. Verbatim match with `sections/abstract.tex:1-3`. |
| Finding 3 (MAJOR) — Phase I-IV at `###` not `##` | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Phase I at line 112 `##`, Phase II at line 155 `##`, Phase III at line 179 `##`, Phase IV at line 211 `##`. |
| Finding 4 (MAJOR) — Part III sections at `###` not `##` | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Reference Implementation at line 242 `##`, Advanced Architectural at line 361 `##`, Protocol for Curriculum Validation at line 365 `##`. |
| Finding 5 (MAJOR) — Subsections at `####` not `###` | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** All `\subsection{}` under Part II are at `###`: Pre-computation (line 116), Invariant Calculation (line 128), Correcting for Sampling Artifacts (line 132), Assembling DataFrame (line 140), Stratified Distribution (line 159), Correlation Analysis (line 165), Low-Dimensional Visualization (line 169), Stratifying Stable Subset (line 195), Stratifying Complex Subset (line 199), Definitive Assignment (line 215), Population Control (line 219). |
| Finding 6 (MAJOR) — Missing Phase II intro paragraph | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Paragraph "Before defining the final curriculum stages, it is essential to perform a thorough exploratory data analysis (EDA)..." present at lines 157-158. |
| Finding 7 (MAJOR) — Table 3 pandoc grid format | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Table 3 at lines 184-192 is a GFM pipe table with 3 columns and 5 data rows. Caption below as "*Table 3: Comparison of Original vs. Proposed Data-Driven Curriculum Framework*". |
| Finding 8 (MAJOR) — Bibliography missing heading | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** `## References` heading at line 397 precedes the 16-item numbered list. |
| Finding 9 (MAJOR) — Missing author/date | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Author `*An Award-Winning Writer*` at line 2. Date `*March 21, 2026*` at line 4. |
| Finding 10 (MAJOR) — Missing TOC | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Hand-curated `## Contents` TOC at lines 6-22 covering all Parts, sections, and subsections. |
| Finding 11 (MINOR) — "Section 1.2" broken cross-reference | audit_2026-05-07/audit-stage_strat_revision.md | **STILL_OPEN.** Line 130: "the full suite of physical invariants defined in Section 1.2." No numbered sections exist in markdown. See Finding M-N1. |
| Finding 12 (MINOR) — Missing Part labels | audit_2026-05-07/audit-stage_strat_revision.md | **STILL_OPEN.** H1 headings at lines 28, 108, 238, 381 omit "Part I"/"Part II"/"Part III"/"Part IV" prefixes. TOC includes them but headings do not. See Finding M-N2. |
| Finding 13 (MINOR) — `\authcomment{}` color loss | audit_2026-05-07/audit-stage_strat_revision.md | **REGRESSED.** The authcomment was previously present as `**[I'm not sure...]**` bold text (acceptable per old audit). It was deleted in Phase 15.1 Wave A (commit `ef79bd0`) and never restored. See Finding C-1. |
| Finding 14 (INFO) — Tab-byte corruption in Table 4 fixed | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** All `\tau_L` and `\text{norm}` in Table 4 (lines 226-232) verified correct. Hex inspection confirms no `0x09` tab bytes. |
| Finding 15 (INFO) — Source Issues appendix removed | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED (restored).** Source Issues section present at lines 419-421. However, its content is now stale (see Finding M-1). |
| Finding 16 (INFO) — No pandoc residue | audit_2026-05-07/audit-stage_strat_revision.md | **RESOLVED.** Artifact scan confirms zero hits for all pandoc residue patterns. See Finding I-2. |

### From previous_audits/stage_strat_revision.md (earlier report, NOT-FLAWLESS verdict)

| Prior Finding ID | Prior Report Source | Current Status + Evidence |
|---|---|---|
| Issue #1 (CRITICAL) — Tab-byte corruption in Table 4 | previous_audits/stage_strat_revision.md | **RESOLVED.** Fixed in Wave A (commit `ef79bd0`). Verified: lines 226-232 contain correct `\tau_L` and `\text{norm}`. |
| Issue #2 (MAJOR) — Missing title page, abstract, TOC | previous_audits/stage_strat_revision.md | **RESOLVED.** Title (line 1), abstract (lines 24-27), TOC (lines 6-22), author (line 2), date (line 4) all present. |
| Issue #3 (MAJOR) — Missing Part labels and section numbers | previous_audits/stage_strat_revision.md | **PARTIALLY RESOLVED.** Heading hierarchy is correct. Section numbers still absent (M-N1). Part labels still absent from H1 headings (M-N2). |
| Issue #4 (MAJOR) — Table 3 non-standard format | previous_audits/stage_strat_revision.md | **RESOLVED.** GFM pipe table at lines 184-192. |
| Issue #5 (MINOR) — Appended converter audit note | previous_audits/stage_strat_revision.md | **RESOLVED (restored).** The Source Issues section was removed in Wave A, then restored in a later wave. Currently present at lines 419-421. |
| Issue #6 (MINOR) — Heading hierarchy mismatch | previous_audits/stage_strat_revision.md | **RESOLVED.** All heading levels now match the canonical `# Part → ## Section → ### Subsection` hierarchy. |

### From MASTER-AUDIT-v1.3.md (cross-pair, stage_strat_revision entries only)

| Prior Finding ID | Prior Report Source | Current Status + Evidence |
|---|---|---|
| CRIT-4 — Missing title | MASTER-AUDIT-v1.3.md | **RESOLVED.** Title at line 1. |
| CRIT-5 — Missing abstract | MASTER-AUDIT-v1.3.md | **RESOLVED.** Abstract at lines 24-27. |
| MAJ-10 — Phase I-IV at `###` | MASTER-AUDIT-v1.3.md | **RESOLVED.** All four Phase headings at `##` level. |
| MAJ-11 — Part III sections at `###` | MASTER-AUDIT-v1.3.md | **RESOLVED.** All three Part III sections at `##` level. |
| MAJ-12 — Subsections at `####` | MASTER-AUDIT-v1.3.md | **RESOLVED.** All 11 subsections at `###` level. |
| MAJ-13 — Missing Phase II intro | MASTER-AUDIT-v1.3.md | **RESOLVED.** Paragraph present at lines 157-158. |
| MAJ-14 — Table 3 pandoc grid | MASTER-AUDIT-v1.3.md | **RESOLVED.** GFM pipe table at lines 184-192. |
| MAJ-15 — Bibliography missing heading | MASTER-AUDIT-v1.3.md | **RESOLVED.** `## References` at line 397. |
| MAJ-16 — Author/date omitted | MASTER-AUDIT-v1.3.md | **RESOLVED.** Author at line 2, date at line 4. |
| MAJ-17 — TOC omitted | MASTER-AUDIT-v1.3.md | **RESOLVED.** TOC at lines 6-22. |
| P5 (cross-cutting) — Source Issues removed | MASTER-AUDIT-v1.3.md | **RESOLVED (restored).** Source Issues section present at lines 419-421. |
| P3 (cross-cutting) — Section numbering loss | MASTER-AUDIT-v1.3.md | **STILL_OPEN.** See M-N1. Section numbers not added to headings. |
| P4 (cross-cutting) — Heading hierarchy wrong | MASTER-AUDIT-v1.3.md | **RESOLVED.** Hierarchy now correct: `# Part → ## Section → ### Subsection`. |

### From stage_strat_revision_verification_report.md (Phase 14 verification)

| Prior Finding ID | Prior Report Source | Current Status + Evidence |
|---|---|---|
| SSR-14-02-09 (INFO) — authcomment accepted per D-58 | verification_reports/stage_strat_revision_verification_report.md | **REGRESSED.** The authcomment rendering that was accepted as bold text in Phase 14 was deleted in Phase 15.1 Wave A. See Finding C-1. |
| SSR-14-02-10 (MINOR) — Heading hierarchy fixed | verification_reports/stage_strat_revision_verification_report.md | **RESOLVED.** All heading levels now correct. |
| "Overall Status: PASS" verdict | verification_reports/stage_strat_revision_verification_report.md | **OVERTURNED.** The Phase 14 PASS verdict was disputed by the May 7 audit and is now further undermined by the authcomment deletion regression (C-1). |

## Embedded Evidence from Prior Reports

### From previous_audits/stage_strat_revision.md (Issue #1 -- tab-byte corruption)

The earlier report provided detailed hex evidence for the tab-byte corruption that was subsequently fixed. The corrected lines (now verified in the current file) are reproduced here as the canonical fix specification:

```
| **0** | Hierarchical | Quantile Binning | $E$ in bottom quartile & $L_{\text{norm}}$ in top quartile. | Deeply bound, near-circular, highly regular orbits. |
| **1** | Hierarchical | Remainder | All other hierarchical systems. | Stable, bound, regular orbits, but less constrained. |
| **2** | Quasi-Random | PCA + Clustering | Members of the cluster with the highest median $\tau_L$. | Most stable of the chaotic set; long-term regular motion. |
| **3** | Quasi-Random | PCA + Clustering | Members of the cluster with the 2nd highest median $\tau_L$. | Onset of chaos; mildly chaotic systems. |
| **4** | Quasi-Random | PCA + Clustering | Members of the cluster with the 3rd highest median $\tau_L$. | Moderately chaotic systems, possibly resonant. |
| **5** | Quasi-Random | PCA + Clustering | Members of the cluster with the 4th highest median $\tau_L$. | Strongly chaotic systems with short predictability. |
| **6** | Quasi-Random | PCA + Clustering + Outlier | Most chaotic cluster (lowest median $\tau_L$) + outliers. | Violent, unpredictable dynamics; ejections, unbound systems. |
```

These lines are confirmed present and correct at lines 226-232 of the current markdown.

### From audit_2026-05-07/audit-stage_strat_revision.md (Phase II intro paragraph)

The May 7 audit identified the missing Phase II intro paragraph. The required text, which is now confirmed present at lines 157-158, is:

> Before defining the final curriculum stages, it is essential to perform a thorough exploratory data analysis (EDA). The goal of this phase is to build a strong intuition for the structure of the data, validate the physical assumptions, and identify the key relationships that will guide the stratification strategy. This process transforms the numerical data in the invariant DataFrame into actionable visual insights.

This matches `sections/algorithmic_workflow.tex:60` verbatim.

### From audit_2026-05-07/audit-stage_strat_revision.md (Table 3 GFM conversion)

The May 7 audit provided the recommended GFM pipe table format for Table 3. The current markdown at lines 184-192 matches this specification exactly, including all 5 data rows with correct cell content, bold first-column cells, and italic caption line below the table.

### From previous_audits/stage_strat_revision.md (Issue #2 -- proposed title/author/date/TOC/abstract block)

The earlier report's proposed fix for the missing front matter has been largely implemented. The title, author, date, abstract, and TOC are all present. However, the proposed section numbering scheme (e.g., `## 1. The Rationale...`, `## 4. Phase I...`) was not adopted; headings remain unnumbered. The proposed Part label prefixing (e.g., `# Part I. Foundational Principles...`) was also not adopted.

### From MASTER-AUDIT-v1.3.md (cross-cutting Wave A/B/C fix list)

The MASTER-AUDIT's prioritized fix list provided the roadmap for Phase 15.1:
- **Wave A (5 CRITICAL items):** Title, abstract, author/date for sampling_method, title for stage_strat_revision -- all addressed for this pair.
- **Wave B (17 MAJOR items):** Heading hierarchy, Phase II intro, Table 3, bibliography heading, author/date, TOC, Part labels -- all resolved for this pair except Part labels in H1 headings (M-N2).
- **Wave C (24 MINOR items):** Em-dashes, pandoc artifacts -- all resolved for this pair.

## Source Issues / Notes

### Documented source inconsistency (preserved in body)

The blockquote at lines 151-152 documents a known LaTeX source inconsistency: the Phase I body text enumerates Shape Invariants as `I1, I2, I3` but the DataFrame schema table (Table 2 at lines 144-149) lists only `I1, I2` columns. The LaTeX source at `algorithmic_workflow.tex:49` confirms the 11-column `tabular` header names only `I1, I2`. This is faithfully preserved in the conversion per the "preserve source verbatim" principle. Resolution requires an upstream LaTeX fix (either add `I3` column or remove `I_3` from body text enumeration).

### Authcomment deletion (regression)

The `\authcomment{}` from `algorithmic_workflow.tex:34` (`I'm not sure what this s is referring to. Should we look for the exact value used in the sampling script?`) was present in the pre-Phase-15.1 markdown as `**[I'm not sure what this s is referring to...]**` but was deleted in commit `ef79bd0` (Phase 15.1 Wave A). This deletion was not documented in any Phase 15.1 plan or fix log. See Finding C-1.

### Source Issues section staleness

The Source Issues section at lines 419-421 was removed in Wave A, then restored in a later wave with its original Phase 14 text intact. It was not updated to reflect Phase 15.1 changes. Specifically:
- It references `\authcomment{}` rendering as bold text, but the authcomment no longer exists in the markdown (C-1).
- It claims "No source-level issues identified" but the body documents the I3 schema inconsistency (lines 151-152).
See Findings M-1 and M-2.

### Heading numbering policy

Section numbers (1, 2, 3, 1.1, 1.2, etc.) from the PDF's LaTeX auto-numbering are not preserved in markdown headings. This causes the "Section 1.2" cross-reference at line 130 to be unresolvable. The MASTER-AUDIT-v1.3.md raised this as a cross-cutting policy question (item 1 in "Cross-pair consistency questions"): should headings carry explicit numeric prefixes or remain bare? This pair currently uses bare headings and has not adopted numeric prefixes. See Finding M-N1.

### Part label policy

Similarly, "Part I/II/III/IV" labels that the PDF renders before `\part{}` titles are included in the markdown TOC but not in the H1 headings themselves. This was raised in MASTER-AUDIT-v1.3.md (cross-cutting pattern P3). See Finding M-N2.
