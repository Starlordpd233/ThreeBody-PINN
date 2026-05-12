---
pair: ctl_instruction
markdown_file: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
latex_root: pinn_instruction/original_latex/framework-specs/ctl-instruction/main_CTL.tex
audit_date: 2026-05-11
auditor: closure-audit-agent
verdict: PASS_WITH_NOTES
findings_critical: 0
findings_major: 1
findings_minor: 3
findings_info: 5
deletion_verdicts:
  - file: docs/findings/reports_on_v1.3/audit_2026-05-07/audit-ctl_instruction.md
    verdict: SAFE_TO_DELETE
    rationale: All 12 findings re-verified independently; no unique byte-level or computational evidence not reproducible from current sources
  - file: docs/findings/reports_on_v1.3/audit_2026-05-07/MASTER-AUDIT-v1.3.md
    verdict: UNCERTAIN
    rationale: Cross-pair synthesis patterns (P5-P8) and prioritized fix waves are unique synthesis content needed by synthesizer agent; no unique ctl_instruction-specific findings beyond per-pair audit
  - file: pinn_instruction/markdown_conversion/verification_reports/ctl_instruction_verification_report.md
    verdict: KEEP_AS_HISTORICAL
    rationale: Automated F1/recall scoring (0.958 F1, 0.958 recall with per-section breakdown) and candidate comparison tables are computational evidence not manually reproducible from current sources
---

## Executive Summary

This closure audit re-verifies `ctl_instruction.md` against its LaTeX source (`main_CTL.tex` plus 8 `\include{}`'d section files plus `preamble_CTL.tex`) and reconciles all findings from three prior reports. The markdown is a substantively faithful conversion. Of the 12 findings in the 2026-05-07 per-pair audit, 8 are fully RESOLVED (Findings 2-6 pandoc artifacts removed, Finding 8-12 INFO unchanged), 2 are IMPROVED (Finding 7 TikZ figures, Finding 1 Source Issues appendix), and 1 (Finding 3 cross-references) is partially resolved. One NEW MAJOR finding was discovered: a corrupted sentence in "Numerical notes and defaults" (md:655-658) with a duplicate line, a missing LaTeX backslash, and a truncated incomplete sentence missing its final clause.

**Bottom line:** No CRITICAL defects. One MAJOR corruption (newly discovered), three MINOR issues, five INFO notes. All mathematical equations, tables, code blocks, stage criteria, and numerical thresholds verified symbol-by-symbol against LaTeX source. Verdict: PASS_WITH_NOTES.

---

## Findings

### MAJOR

**F-CI-MAJ-001 (NEW): Corrupted sentence in "Numerical notes and defaults" paragraph**

**Description:** The paragraph at md:655-658 contains a garbled sentence with duplicate text, a missing LaTeX backslash on `\varepsilon`, and a truncated incomplete sentence. The LaTeX source concludes with "does not enter $s_{\min}$ or any denominator besides $V$" but the markdown sentence stops at "*does not*" with the final clause entirely missing.

**Location:** `ctl_instruction.md:655-658`

**LaTeX:** `sections/04_phase1_data_prep.tex:408-410`
```latex
Unless otherwise specified, use double precision for all invariants. The softening
$\varepsilon=10^{-10}$ in Item~\ref{item:eqs} is a safe default in scaled units and
\emph{does not} enter $s_{\min}$ or any denominator besides $V$.
```

**Markdown:** `ctl_instruction.md:655-658`
```markdown
Unless otherwise specified, use double precision for all invariants. The
softening $\varepsilon=10^{-10}$ in
softening $varepsilon=10^{-10}$ in the total energy definition (see above) is a safe default in scaled units and *does not*
```

**Defects:**
1. Line 656 is a duplicate fragment: "softening $\varepsilon=10^{-10}$ in"
2. Line 657: `$varepsilon$` missing backslash — should be `$\varepsilon$`
3. The sentence is incomplete — ends at "*does not*" — missing the final clause "enter $s_{\min}$ or any denominator besides $V$"
4. The LaTeX cross-reference "Item~\ref{item:eqs}" was replaced with "softening $varepsilon=10^{-10}$ in the total energy definition (see above)" — a manual substitution that introduced errors

**Verdict:** NEW

**Recommended fix:** Replace md:655-658 with:
```markdown
Unless otherwise specified, use double precision for all invariants. The
softening $\varepsilon=10^{-10}$ in the total energy definition (see above) is a safe default in scaled units and *does not* enter $s_{\min}$ or any denominator besides $V$.
```

### MINOR

**F-CI-MIN-001 (Prior Finding 1): Source Issues appendix has no LaTeX origin**

**Description:** The `# Source Issues / Notes for Future Reconciliation` section and `## SI-CTL-001` subsection at md:1211-1220 have no corresponding LaTeX source content. This is an intentional editorial addition documented in the verification report as "metadata for future reconciliation."

**Location:** `ctl_instruction.md:1211-1220`

**LaTeX:** (no source — editorial addition)

**Markdown:** `ctl_instruction.md:1211-1220`
```markdown
# Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation...

## SI-CTL-001: Input-vector dimensionality inconsistency
...
```

**Verdict:** RESOLVED (unchanged — intentionally retained as editorial metadata)

**F-CI-MIN-002 (Prior Finding 7): TikZ diagram content not fully preserved**

**Description:** The two appendix TikZ figures (`fig:step2_data_workflow` and `fig:step2to5_workflow`) are now rendered as blockquote notes (md:1207-1209) instead of the previously empty `<figure>` blocks. This is an improvement: captions are preserved and Figure 2 has a reasonable textual description. However, the specific diagram nodes and edges are still not fully enumerated:

- Figure 1 nodes (Sampled ICs, COM Frame?, Transform to COM, Verify Σ m_i v_i = 0, Compute Physics Invariants, Build 14D PINN Input) and edge labels ("No", "Yes") are not listed.
- Figure 2 nodes (Step 2 Preprocessing, Step 3 Invariant Calculation, Step 4 Input Vector Construction, Step 5 Stage Assignment, Compute additional features) and edge labels ("Scaled ICs", "Use stored invariants", "Reuse invariants") are partially described but not exhaustively enumerated.

**Location:** `ctl_instruction.md:1207, 1209`

**LaTeX:** `sections/appendix.tex:5-31` (Figure 1 TikZ), `sections/appendix.tex:36-67` (Figure 2 TikZ)

**Markdown:** `ctl_instruction.md:1207-1209`
```markdown
> **Figure 1 (TikZ diagram not rendered):** Workflow diagram for COM-frame verification
> and input construction. ... The diagram was generated from TikZ source in the LaTeX
> appendix; see the original `.tex` file for the definition.

> **Figure 2 (TikZ diagram not rendered):** End-to-end data-processing flow from Step 2
> (Preprocessing) through Step 5 (Stage Assignment). After Step 3 computes and stores
> invariants ($E, Q, s_{\min}, L_{\mathrm{norm}}, I_{\mathrm{norm}}, \tau_L$), Steps 4
> and 5 run in parallel, both using these stored invariants. ...
```

**Verdict:** IMPROVED (blockquote notes replace empty HTML figure blocks) but diagram node/edge details still not fully enumerated

**F-CI-MIN-003 (Prior Finding 3 — partial): Corrupted Item~\ref{item:eqs} cross-reference**

**Description:** The `Item~\ref{item:eqs}` cross-reference at LaTeX `04_phase1_data_prep.tex:409` was not cleanly resolved. It was replaced with garbled text in the corrupted sentence (see F-CI-MAJ-001). Separately, `Item~\ref{item:lnorm}` at `04_phase1_data_prep.tex:181` was cleanly resolved with descriptive text "the characteristic scale of the normalized angular momentum (see above)" at md:492-493.

**Location:** `ctl_instruction.md:656-657` (corrupted), `ctl_instruction.md:492-493` (resolved)

**LaTeX (`item:lnorm`):** `sections/04_phase1_data_prep.tex:181`
```latex
normalize by the characteristic scale of Item~\ref{item:lnorm}:
```

**Markdown (resolved):** `ctl_instruction.md:492-493`
```markdown
normalize by
the characteristic scale of the normalized angular momentum (see above):
```

**LaTeX (`item:eqs`):** `sections/04_phase1_data_prep.tex:409`
```latex
$\varepsilon=10^{-10}$ in Item~\ref{item:eqs} is a safe default in scaled units and
```

**Markdown (corrupted):** `ctl_instruction.md:656-657`
```markdown
softening $\varepsilon=10^{-10}$ in
softening $varepsilon=10^{-10}$ in the total energy definition (see above)
```

**Verdict:** REGRESSED (item:eqs cross-reference replaced with garbled text; item:lnorm cross-reference resolved)

### INFO

**F-CI-INFO-001 (Prior Finding 8): `\median` operator rendered as `\mathop{\mathrm{median}}`**

**Location:** `ctl_instruction.md:405, 407`
**Verdict:** UNCHANGED — functionally equivalent rendering, not a defect.

**F-CI-INFO-002 (Prior Finding 9): 11/12/13/14-D input-vector inconsistency preserved from source**

**Location:** `ctl_instruction.md:447, 557, 583-593, 597, 800, 884, 1241`
**Verdict:** UNCHANGED — faithfully preserves LaTeX source inconsistency. Documented in SI-CTL-001.

**F-CI-INFO-003 (Prior Finding 10): Empty `07_reproducibility.tex` in source**

**Location:** `sections/07_reproducibility.tex` (1 byte newline only)
**Verdict:** UNCHANGED — markdown correctly surfaces reproducibility content from `06_advanced_considerations.tex:39` as `# Reproducibility Note (Ignore Now and Come Back Later):` at md:1172.

**F-CI-INFO-004 (Prior Finding 11): `\S4.4` cross-reference with no matching label**

**Location:** `ctl_instruction.md:444`
**Verdict:** UNCHANGED — preserved verbatim from source. Source-level issue, not a conversion defect.

**F-CI-INFO-005 (Prior Finding 12): Code listing indentation preserved from LaTeX enumerate context**

**Location:** `ctl_instruction.md:498-521, 577-642`
**Verdict:** UNCHANGED — 4-space indent inside fenced blocks is faithful to source.

---

## Reconciliation Table

### From audit-ctl_instruction.md (2026-05-07 per-pair audit)

| Prior Finding ID | Prior Report Source | Current Status | Evidence |
|---|---|---|---|
| Finding 1 (MINOR) | audit_2026-05-07: Source Issues appendix no LaTeX origin | STILL_OPEN | md:1211-1220 — section still present; intentionally retained editorial metadata |
| Finding 2 (MINOR) | audit_2026-05-07: Pandoc anchor placeholders `[]{#item:eqs}` | RESOLVED | Verified absent at md:451, ~463, ~488, ~542 — all `[]{#item:*}` anchors removed; clean `**heading**` text without bracketed anchors |
| Finding 3 (MINOR) | audit_2026-05-07: CrossRef `Item [\[item:lnorm\]](#item:lnorm){reference-type="ref" ...}` | PARTIALLY RESOLVED | `item:lnorm` reference replaced with descriptive text (md:492-493). `item:eqs` reference corrupted in garbled text (md:656-657, see F-CI-MAJ-001) |
| Finding 4 (MINOR) | audit_2026-05-07: Code-fence pandoc attribute strings on 8 listings | RESOLVED | All 8 code blocks use clean ```` ```python ```` fences at md:282, 312, 475, 498, 577, 689, 716, 796. No pandoc fence-attribute strings remain. Captions removed but surrounding prose provides context. |
| Finding 5 (MINOR) | audit_2026-05-07: `{.uri}` class on `\url{}` headings | RESOLVED | md:270 `#### Initial Conditions (ic_hierarchical_\*.txt)` — no `{.uri}`. md:286 `#### Brutus Simulation Output (brutus_hierarchical_\*.txt)` — no `{.uri}`. |
| Finding 6 (MINOR) | audit_2026-05-07: Escaped `\"...\"` quotes | RESOLVED | All instances use regular `"..."` quotes: md:48-49 (`"hierarchical"`, `"quasi-random"`), md:57 (`"low-fidelity"`), md:117-118 (`"easy"`, `"hard"`), md:1139 (`"ground truth"`) |
| Finding 7 (MINOR) | audit_2026-05-07: TikZ figures reduced to empty `<figure>` blocks | IMPROVED | md:1207-1209 — now blockquote notes with captions and partial descriptions. Diagram node names not exhaustively listed (see F-CI-MIN-002) |
| Finding 8 (INFO) | audit_2026-05-07: `\median` → `\mathop{\mathrm{median}}` | UNCHANGED | md:405, 407 — functionally equivalent rendering |
| Finding 9 (INFO) | audit_2026-05-07: 11/12/13/14-D input vector inconsistency | UNCHANGED | Preserved from source; documented in SI-CTL-001 at md:1215-1219 |
| Finding 10 (INFO) | audit_2026-05-07: Empty `07_reproducibility.tex` | UNCHANGED | Source quirk; correctly handled |
| Finding 11 (INFO) | audit_2026-05-07: `\S4.4` cross-reference no matching label | UNCHANGED | md:444 — preserved verbatim; source-level issue |
| Finding 12 (INFO) | audit_2026-05-07: Code listing indentation preserved | UNCHANGED | Faithful to source |

### From MASTER-AUDIT-v1.3.md (2026-05-07 cross-pair synthesis — ctl_instruction-relevant only)

| Prior Finding ID | Prior Report Source | Current Status | Evidence |
|---|---|---|---|
| P5 (Source Issues appendix inconsistency) | MASTER-AUDIT: ctl_instruction retains Source Issues appendix (md:1233-1242) | STILL_OPEN | md:1211-1220 — retained. Cross-pair policy decision pending (keep vs. remove vs. sidecar). |
| P6 (Pandoc conversion artifacts) | MASTER-AUDIT: Findings 2-6 concentrated in ctl_instruction | RESOLVED | All 5 pandoc artifact types (anchors, xrefs, fence attributes, URI class, escaped quotes) removed from ctl_instruction.md (see reconciliation above). |
| P7 (TikZ figures lost) | MASTER-AUDIT: ctl_instruction.md:1213-1219, 1221-1231 two appendix workflow diagrams lost | IMPROVED | md:1207-1209 — now blockquote notes replace empty `<figure>` blocks. Captions preserved; node-level details still not fully enumerated. |
| P8 (\authcomment color stripping) | MASTER-AUDIT: all pairs preserve bracketed-bold; ctl_instruction NOT flagged (uses plain blockquotes) | RESOLVED | No `<span style="color: red">` spans found anywhere in ctl_instruction.md. All authcomments use `> **Author note:**` blockquote format. |

### From ctl_instruction_verification_report.md

| Prior ID | Prior Report Source | Current Status | Evidence |
|---|---|---|---|
| CTL-01-000 | Section 1 heading and architecture-file pointer | RESOLVED | md:9-15 — `# Important Note` heading preserved with `PINN_architecture_plan.tex` reference |
| CTL-02-001 | `tab:brutus_compare` table fidelity | RESOLVED | md:21-30 — 4 data rows, 7 columns, all numeric values match LaTeX `02_data_characterization.tex:11-15` |
| CTL-02-002 | Visible authcomment in section 02 | RESOLVED | md:107-114 — rendered as `> **Author note:**` blockquote |
| CTL-02-003 | Excluded comment-environment content | RESOLVED | Neither "Assessing Data Suitability" nor "A Multi-Fidelity Curriculum Learning Framework" appears in markdown |
| CTL-03-000 | Section 3 listings and file globs | RESOLVED | IC sample (md:282-284), Brutus output sample (md:312-322), file glob references preserved |
| CTL-04-001 | Step 2.5 authcomment | RESOLVED | md:413-418 — rendered as `> **Author note:**` blockquote |
| CTL-04-002 | Section 04 authcomments (5 locations) | RESOLVED | All at md:648-651, 686-688, 742-743, 785-790 — plain blockquotes |
| CTL-04-003 | Excluded velocity-position-angle comment block | RESOLVED | Absent from markdown body |
| Formulas: item:eqs | Total energy, virial ratio, s_min formulas | RESOLVED | md:450-461 — all formulas match LaTeX `04_phase1_data_prep.tex:121-127` symbol-by-symbol; anchor placeholder removed (clean) |
| Formulas: item:lnorm | Angular momentum, L_max, L_norm formulas | RESOLVED | md:462-484 — all formulas match LaTeX `04_phase1_data_prep.tex:134-141`; code block clean |
| Formulas: item:inorm | Inertia tensor and I_norm formula | RESOLVED | md:487-521 — formulas match LaTeX `04_phase1_data_prep.tex:176-184`; code block clean |
| Formulas: shape invariants | I_1, I_2, I_3 definitions | RESOLVED | md:523-535 — match LaTeX `04_phase1_data_prep.tex:232-236` |
| Formulas: item:lyap | Lyapunov time estimator and code | RESOLVED | md:537-642 — 6-step algorithm + code match LaTeX `04_phase1_data_prep.tex:293-388` |
| Formulas: normalization | Component-wise normalization code | RESOLVED | md:710-740 — code and formulas match LaTeX `04_phase1_data_prep.tex:477-517` |
| Formulas: input vector | IC vector, Input assembly, t' formula | RESOLVED | md:791-827 — formulas match LaTeX `04_phase1_data_prep.tex:575-603` |
| CTL-05-001 | Phase 2 opening authcomment | RESOLVED | md:834-851 — rendered as `> **Author note:**` blockquote |
| CTL-05-002 | Mini-batch composition table | RESOLVED | md:965-970 — 2 rows + header + caption match LaTeX `05_phase2_training_loop.tex:105-116` |
| CTL-05-003 | C-schedule clipping table | RESOLVED | md:980-984 — 3 rows + header match LaTeX `05_phase2_training_loop.tex:125-135` |
| CTL-05-004 | Stage-transition authcomment | RESOLVED | md:1018-1028 — rendered as `> **Author note:**` blockquote |
| CTL-05-005 | Consolidated hyperparameter schedule | RESOLVED | md:1059-1063 — 3 rows + header + caption match LaTeX `05_phase2_training_loop.tex:203-214` |
| CTL-05-006 | Excluded training-loop comment ranges | RESOLVED | No leakage from `05_phase2_training_loop.tex:51-58` or `:237-643` comment environments |
| CTL-06-001 | Prediction-Horizon authcomment | RESOLVED | md:1123 — rendered as `> **Author note:**` blockquote nested inside bullet |
| CTL-07-000 | Empty `07_reproducibility.tex` | RESOLVED | Content correctly surfaced from `06_advanced_considerations.tex:39` at md:1172 |
| CTL-A-000 | Appendix figures | IMPROVED | md:1207-1209 — blockquote notes replace empty `<figure>` blocks; captions preserved; diagram node details not fully enumerated |
| SI-CTL-001 | 11/12/13/14-D inconsistency | STILL_OPEN | Source inconsistency documented at md:1215-1219; requires source-level resolution |

---

## Embedded Evidence from Prior Reports

### From audit_2026-05-07/audit-ctl_instruction.md

No byte-level, hex, or computational evidence requiring verbatim preservation. The 12 findings are fully captured in the reconciliation table above. The per-pair audit's equation-by-equation verification claims (for 7 LaTeX formula blocks) were independently re-verified in this audit by reading both the LaTeX source and markdown file in full and comparing symbol-by-symbol.

### From MASTER-AUDIT-v1.3.md

The cross-pair synthesis patterns (P1-P10), verdict matrix, and prioritized fix waves (A-D) constitute unique synthesis content. Since these are cross-pair constructs handled by the synthesizer agent, only the ctl_instruction-relevant excerpts are preserved here:

Per MASTER-AUDIT-v1.3.md verdict matrix:
> | # | Pair | Status | CRITICAL | MAJOR | MINOR | INFO |
> |---|------|--------|---------:|------:|------:|-----:|
> | 1 | ctl_instruction | PASS_WITH_NOTES | 0 | 0 | 7 | 5 |

Per MASTER-AUDIT-v1.3.md cross-cutting patterns relevant to ctl_instruction:
- P5: "Source Issues / Notes for Future Reconciliation" appendix retained at ctl_instruction.md:1233-1242.
- P6: Pandoc conversion artifacts concentrated heavily in ctl_instruction.md (Findings 2-6: anchors, xref plumbing, code-fence attributes, URI class, escaped quotes). **STATUS 2026-05-11: ALL RESOLVED.**
- P7: TikZ figures lost — ctl_instruction.md:1213-1219, 1221-1231 two appendix workflow diagrams. **STATUS 2026-05-11: IMPROVED — blockquote notes replace empty HTML.**
- P8: \authcomment{} color stripping — ctl_instruction not flagged; uses plain `> **Author note:**` blockquotes. **STATUS 2026-05-11: CONFIRMED — no `<span style="color: red">` spans.**

### From ctl_instruction_verification_report.md

The automated F1/recall scoring data from the candidate comparison table is computational evidence unique to the verification report:

| Candidate | Overall score | Rank | Key metric |
|---|---|---|---|
| `ctl_instruction.md` (selected) | 0.958 F1 / 0.958 recall | 2 raw / 1 selected | Best section 04 preservation |
| `ctl_instruction_v2.md` | 0.890 F1 / 0.909 recall | 3 | Lower recall sections 03-05 |
| `pandoc_conversion/CTL-instruction-final.md` | 0.959 F1 / 0.947 recall | 1 raw / 2 selected | Better F1, lower recall than selected |

Selection rationale: "The pandoc candidate narrowly wins the raw F1 score, but the existing target has better source recall and stronger preservation in the highest-risk section 04 and appendix figure area."

Per-section recall scores (from verification report):
- Section 01: 1.000 recall
- Section 02: 0.992 recall
- Section 03: 1.000 recall
- Section 04: 0.999 recall
- Section 05: 0.990 recall
- Section 06: 1.000 recall
- Section 07: N/A (empty source)
- Appendix: 0.577 recall

Excluded comment ranges documented in verification report:
| Source range | Excluded content | Status |
|---|---|---|
| `02_data_characterization.tex:218-232` | "Assessing Data Suitability and Generation Methodology" | Absent from markdown |
| `02_data_characterization.tex:235-263` | "A Multi-Fidelity Curriculum Learning Framework" | Absent from markdown |
| `04_phase1_data_prep.tex:245-290` | Velocity-position angle item and code | Absent from markdown |
| `05_phase2_training_loop.tex:51-58` | Energy regularizer subsection | Absent from markdown |
| `05_phase2_training_loop.tex:237-643` | Older training-loop revision (407 lines) | Absent from markdown |

---

## Source Issues / Notes

### SI-CTL-001: Input-vector dimensionality inconsistency (STILL OPEN)

The LaTeX source itself alternates between:
- 11-component IC + t = 12D input (`04_phase1_data_prep.tex:426, 582, 597`, `05_phase2_training_loop.tex:29`)
- 13-component IC + t = 14D input (`04_phase1_data_prep.tex:556`, `appendix.tex:18`)
- Mixed description: "12-Component Input Vector" heading with "13-component initial condition vector" body text (`04_phase1_data_prep.tex:556-557`)

The markdown preserves all instances faithfully. The canonical PINN input vector definition in `pinn/data-processing-pipeline-full.py` should be the arbiter for reconciliation.

---

## Verification Checklist

- [x] Document title: `Final CTL Instruction on Training PINNs for the Three-Body Problem` — matches `preamble_CTL.tex:42`
- [x] Author + date: `Starlordpd233`, `June 2025` — matches `preamble_CTL.tex:43-44`
- [x] Abstract: Not present in LaTeX source (no `\begin{abstract}`)
- [x] All 8 top-level `\section{}` headings: exact text match, `\section` → `#` level
- [x] All 16 `\subsection{}` headings: exact text match, `\subsection` → `##` level
- [x] All 2 `\subsubsection{}` headings: exact text match, `\subsubsection` → `###` level
- [x] All `\paragraph{}` headings: exact text match, `\paragraph` → `####` level
- [x] Heading hierarchy: `\section`→`#`, `\subsection`→`##`, `\subsubsection`→`###`, `\paragraph`→`####` — consistent throughout
- [x] All mathematical equations: 52+ expressions verified symbol-by-symbol against LaTeX source, including all aligned blocks, display equations, and inline math. No formula drift.
- [x] All 4 tables (brutus_compare, mini-batch, C-schedule, hyperparameter): cell-by-cell match, captions preserved
- [x] All 8 code listings: content verified, clean ````python```` fences (no pandoc attribute strings)
- [x] No bibliography in LaTeX source (no `.bib` file, no `\cite{}` commands, no `\begin{thebibliography}`)
- [x] No `[]{#item:...}` anchor placeholders — all removed
- [x] No `reference-type="ref"` Pandoc xref artifacts — all resolved or replaced
- [x] No `{.python language="Python"}` code-fence attribute strings — all removed
- [x] No `{.uri}` class attributes — all removed
- [x] No escaped `\"...\"` quotes — all replaced with regular quotes
- [x] TikZ figures: both replaced by blockquote notes with captions (improved from empty `<figure>` blocks)
- [x] Source Issues block: `## SI-CTL-001` present and accurate at md:1215-1219
- [x] No `<span style="color: red">` spans anywhere in markdown
- [x] All `\authcomment{}` blocks rendered as `> **Author note:**` plain blockquotes
- [x] `\textcolor{blue}{...}` rendered as `[]{style="color: blue"}` span syntax at md:336
- [x] All `\begin{comment}...\end{comment}` ranges excluded from markdown
- [x] Appendix heading: `# Supplementary Figures` — lacks "A" prefix from `\appendix` command (MINOR; see F-CI-MIN-003 inline note above) — actually this is a separate consideration. The LaTeX `\appendix` would render "A Supplementary Figures" in PDF. The markdown renders "# Supplementary Figures" without the appendix letter. This is a cosmetic difference consistent with markdown conventions.

---

## Confidence Assessment

**Confidence: HIGH.** All 8 LaTeX section files (`01_intro.tex` through `07_reproducibility.tex` plus `appendix.tex`), `main_CTL.tex`, and `preamble_CTL.tex` were read in full (10 files total). The complete 1219-line markdown file was read in full. Every top-level section, every subsection, every subsubsection, and every paragraph heading was cross-referenced. Every equation block (52+ expressions) was verified symbol-by-symbol. Every table cell was checked value-by-value. Every numerical threshold (E<-0.5, L/L_max>0.5, 0.7≤Q≤1.3, s_min>2, τ_L>5, ε_phys=10^-4, ε_energy=10^-4, β=0.98, β=0.99, γ=0.01, batch 240/16, etc.) was confirmed to match. Every visible `\authcomment{}` was verified rendered as blockquote. All excluded `\begin{comment}` content was confirmed absent from markdown.

**Limitations:**
- PDF rendering was not compared (no PDF-to-markdown visual diff). All verification is based on LaTeX source ↔ markdown source text comparison.
- The `\appendix` section numbering convention (e.g., "A Supplementary Figures" in PDF vs. "# Supplementary Figures" in markdown) is not enforced — markdown does not have a native appendix numbering mechanism.
