# Review of Framework Markdown Verification Report

This report documents the Phase 13 audit of the `review-of-framework` sub-document
(LaTeX entry: `pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex`,
7 active `\input` directives at lines 13-19) against its single pandoc-converted
markdown candidate. The audit follows the Phase 10/11/12 audit -> fix -> verify
pattern, adapted per Phase 13 decisions D-39 through D-49 for a single-candidate
workflow (CAND-02). Wave 1 (this skeleton) records candidate provenance and the
vacuous-policy baseline; Wave 2 populates the per-section audits and applies
markdown-only fixes; Wave 3 promotes the corrected candidate to the authoritative
path and finalises the report.

## Starting Candidate Provenance

The Phase 13 audit uses a single pandoc-converted markdown candidate. CAND-02
applies — no diff-score ranking is needed because no other candidates exist.
This subsection replaces Phase 12's `## Candidate Comparison` (D-39, D-42).
No `## Selected Baseline` subsection follows because the single candidate IS
the baseline.

| Field | Value |
|---|---|
| Source path | `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md` |
| File size | 59360 bytes (verified by `wc -c`) |
| Line count | 533 (verified by `wc -l`) |
| Conversion tool | pandoc 3.7.0.2 |
| Date observed | 2026-05-05 |
| CAND-02 status | Applies — single candidate, no ranking |
| CLEAN-02 status | N/A — no losing candidates to archive (D-40) |

Live evidence (captured 2026-05-05 from the repository working tree):

```
$ wc -l pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md
     533 pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md
$ wc -c pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md
   59360 pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md
```

## Vacuous Policy Checks (D-47)

The review-of-framework source has structural simplicity that vacuously satisfies
several inherited decisions. Each absence is verified by live grep against the
entry file plus the 7 active section files (D-47); the candidate-side check for
pandoc-injected reference artifacts uses the same pattern (D-48).

| Check | Source pattern | Count | Inherited decision vacuously satisfied | Status |
|---|---|---:|---|---|
| Comment blocks | `\begin{comment}` | 0 across entry + 7 sections | D-05, D-09 (AUDIT-03 / FIDEL-06 source side) | VACUOUS PASS |
| Author comments | `\authcomment{` | 0 across entry + 7 sections | D-06, D-07 | VACUOUS PASS |
| Inactive sections | `*_inactive.tex` | 0 files | D-34, D-35, D-38 (FIDEL-06 file side) | VACUOUS PASS |
| Citations | `\cite{` | 0 across entry + 7 sections | D-27, D-28 (FIDEL-03 source side) | VACUOUS PASS |
| Bibliography entries | `\bibitem{` | 0 across entry + 7 sections | D-37 | VACUOUS PASS |

Per D-48: candidate searched for `[@refN]` injected pandoc citation artifacts —
count: 0 (D-48 vacuously satisfied).

Live evidence (captured 2026-05-05 from the repository working tree). Each
per-file count below is `0`; totals are the sum across all 8 listed files
(entry + 7 sections):

```
$ SECTIONS_DIR="pinn_instruction/original_latex/review-of-framework/review_of_framework/sections"
$ ENTRY="pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex"

$ grep -c '\\begin{comment}' "$ENTRY" "$SECTIONS_DIR"/*.tex
pinn_instruction/.../review_of_framework.tex:0
pinn_instruction/.../sections/architectural_initialization_refinements.tex:0
pinn_instruction/.../sections/conclusion_and_recommendations.tex:0
pinn_instruction/.../sections/data_scaling_normalization.tex:0
pinn_instruction/.../sections/executive_summary.tex:0
pinn_instruction/.../sections/foundational_physical_metrics.tex:0
pinn_instruction/.../sections/multi_component_loss_framework.tex:0
pinn_instruction/.../sections/training_sampling_strategy.tex:0
                                                          (total: 0)

$ grep -c '\\authcomment{'   "$ENTRY" "$SECTIONS_DIR"/*.tex   # all 0  (total: 0)
$ grep -c '\\cite{'          "$ENTRY" "$SECTIONS_DIR"/*.tex   # all 0  (total: 0)
$ grep -c '\\bibitem{'       "$ENTRY" "$SECTIONS_DIR"/*.tex   # all 0  (total: 0)
$ ls "$SECTIONS_DIR"/*_inactive.tex 2>/dev/null | wc -l       # 0

$ CAND="pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md"
$ grep -cE '\[@ref[0-9]+\]' "$CAND"                            # 0
```

## Promotion Action

**Deferred to Wave 3** (NOT executed now — Wave 2 needs the candidate at its
current `pandoc_conversion/` path so section-scoped edits land in a stable
location before the move).

Planned Wave-3 promotion command (D-43):

```bash
git mv pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md \
       pinn_instruction/markdown_conversion/review_of_framework.md
```

After this move the candidate's role transitions from "pandoc output" to
"authoritative markdown" at the canonical lowercase_underscore path that
matches the source subdirectory name `review_of_framework/`. No `_archive/`
directory is created in Phase 13 (D-40, CLEAN-02 N/A).

## Section Audit

Each subsection below corresponds to one of the 7 active source files imported
by `review_of_framework.tex` (lines 13-19), in source order. Each is marked
`**Status:** PENDING` in Wave 1; Wave 2 will populate the discrepancy table,
content audit, and (where applicable) formula or table cell-by-cell checklists,
and flip status to PASS once all open discrepancies are resolved. The
LaTeX -> markdown heading map for FIDEL-05 (Phase 13 source uses no
`\subsubsection`): `\section` -> `#`, `\subsection` -> `##`, `\paragraph` -> `####`.

### 1. executive_summary.tex

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-02-01 | Conversion | MINOR | `executive_summary.tex:9` | `review_of_ctl-pinn_framework.md:8` | Pandoc-escaped prose bracket pair `\[-1, 1\]` rendered the literal range token; source uses plain `[-1, 1]`. Replaced with unescaped `[-1, 1]`. | Fixed |

**Content audit:**
- Heading: `\section*{Executive Summary}` → `# Executive Summary` — MATCH (line 1, starred form rendered as `#`)
- Lead paragraph (`\section*` followed by prose): source line 4 → candidate line 2 — MATCH
- Second paragraph introducing the five-item summary: source line 6 → candidate line 4 — MATCH
- `\begin{enumerate}` 5-item list (Foundational Physical Metrics; Data Scaling and Normalization; Network Architecture and Initialization; Loss Function Framework; Training and Data Sampling Strategy): source lines 7-13 → candidate lines 6, 8, 10, 12, 14 — MATCH; numbering 1-5 preserved as `1.` through `5.`; bold `\textbf{...}` rendered as `**...**`; `\texttt{}` rendered as inline backticks
- Inline math (`$\tau_L$`, `$L/L_{\max}$`, `$\omega_0$`) — MATCH
- Closing paragraph: source line 14 → candidate line 16 — MATCH
- LaTeX hyphenation hint `con\-cerning` (source line 10) collapsed to plain `concerning` (candidate line 10) — MATCH (correct pandoc behavior; not a discrepancy)
- `\addcontentsline{toc}{section}{...}` and `\clearpage` (source lines 3, 16) — non-rendering directives, correctly omitted from candidate

**Pandoc artifact sweep (section line range 1-17):**
- `^\\-` count in section 1: 0 (no escaped-dash list markers in this section; `\begin{enumerate}` rendered as `1.` numbered list)
- `\\[` count in section 1: 1 occurrence at candidate line 8 — fixed (RoF-13-02-01)
- Post-fix `^\\-` count: 0; post-fix `\\[` count: 0

---

### 2. foundational_physical_metrics.tex (math-heavy)

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-02-02 | Conversion | MINOR | `foundational_physical_metrics.tex:20, 25, 31, 36` | `review_of_ctl-pinn_framework.md:38, 40, 46, 48` | Pandoc escaped 4 indented `- ` list markers (4-space indented under enumerate item 1) as `    \- `; source uses plain `- `. Replaced 4 occurrences with `    - `. | Fixed |
| RoF-13-02-03 | Conversion | MINOR | `foundational_physical_metrics.tex:46, 49, 51, 54, 57, 59, 61, 63, 66, 71, 75` | `review_of_ctl-pinn_framework.md:56, 58, 60, 62, 64, 66, 68, 70, 72, 74` | Pandoc escaped 10 indented `- ` list markers (4-space indented under enumerate item 2) as `    \- `; source uses plain `- `. Replaced 10 occurrences with `    - `. | Fixed |
| RoF-13-02-04 | Conversion | MINOR | `foundational_physical_metrics.tex:95, 98, 100, 102, 104, 106, 111, 114, 116, 118, 120, 122` | `review_of_ctl-pinn_framework.md:92, 94, 96, 98, 100, 102, 106, 108, 110, 112, 114, 116` | Pandoc escaped 12 unindented `- ` list markers (worker function and orchestrator bullets) as `\- `; source uses plain `- `. Replaced 12 occurrences with `- `. | Fixed |

**Content audit:**
- Heading: `\section{Foundational Physical Metrics for Curriculum Design}` → `# Foundational Physical Metrics for Curriculum Design` (candidate line 18) — MATCH
- Subsection: `\subsection{Defining and Implementing Lyapunov Time...}` → `## Defining and Implementing Lyapunov Time ($\tau_L$) and Maximum Angular Momentum ($L/L_{\max}$) Computations` (candidate line 22) — MATCH; `\texorpdfstring` collapsed to inline math correctly
- Subsection: `\subsection{Establishing a Robust Pipeline for Global Scale Computation}` → `## Establishing a Robust Pipeline for Global Scale Computation` (candidate line 78) — MATCH
- Paragraph headings: `\paragraph{Context and Validation}` → `#### Context and Validation` (candidate lines 26, 82) — MATCH; `\paragraph{Proposed Solution and Implementation}` → `#### Proposed Solution and Implementation` (candidate lines 32, 86) — MATCH (FIDEL-05 heading map applied)
- Lead prose paragraph (source line 3) → candidate line 20 — MATCH
- `\begin{enumerate}` 2-item top-level list (Maximum Angular Momentum; Lyapunov Time): source lines 15-77 → candidate `1.` and `2.` numbered items at lines 36, 52 — MATCH (numbering preserved)
- Inline math (`$\tau_L$`, `$L/L_{\max}$`, `$L_{\max}$`, `$E$`, `$M_{\text{total}}$`, `$\mathbf{r}'_i$`, `$\mathbf{v}'_i$`, `$\delta_0$`, `$\epsilon_{\text{pert}}$`, `$\Delta t$`, `$\delta_1$`, `$a_1$`, `$\lambda$`, `$T_{\text{horizon}}$`, `$N_{\text{steps}}$`) — MATCH throughout
- `\texttt{...}` (`CTL-instruction-final.tex`, `compute_single_trajectory_properties`, `compute_globals`, `ProcessPoolExecutor`, `executor.map`, `tqdm`, `next steps.txt`, `E_scale`, `smin_scale`, `ic_*.txt`) → backtick-rendered code spans — MATCH
- `\textbf{...}` rendered as `**...**` throughout — MATCH
- `\allowbreak` directive (source line 87) — non-rendering hyphenation hint, correctly omitted

**Formula checklist (FIDEL-01 per D-14):**

| # | Source location | LaTeX form (one-line excerpt) | Candidate location | Markdown form (one-line excerpt) | Status |
|---|---|---|---|---|---|
| 1 | `foundational_physical_metrics.tex:21-23` | `\begin{equation} \mathbf{L} = \sum_{i=1}^{3} m_i (\mathbf{r}'_i \times \mathbf{v}'_i) \quad \rightarrow \quad L = \|\|\mathbf{L}\|\| \end{equation}` | `review_of_ctl-pinn_framework.md:38` | `$$\mathbf{L} = \sum_{i=1}^{3} m_i (\mathbf{r}'_i \times \mathbf{v}'_i) \quad \rightarrow \quad L = \|\|\mathbf{L}\|\|$$` | MATCH |
| 2 | `foundational_physical_metrics.tex:26-29` | `\begin{align} r_{\text{char}} &= \frac{1}{3} \sum_{i<j} \|\|\mathbf{r}'_i - \mathbf{r}'_j\|\| \\ v_{\text{char}} &= \sqrt{\frac{2\|E\|}{M_{\text{total}}}} \quad \text{where} \quad M_{\text{total}} = \sum_{i=1}^{3} m_i \end{align}` | `review_of_ctl-pinn_framework.md:40-44` | `$$\begin{aligned} r_{\text{char}} &= ... \\ v_{\text{char}} &= \sqrt{\frac{2\|E\|}{M_{\text{total}}}} \quad \text{where} \quad M_{\text{total}} = \sum_{i=1}^{3} m_i \end{aligned}$$` | MATCH (`align` → `aligned` per pandoc convention; `equation*` semantics preserved) |
| 3 | `foundational_physical_metrics.tex:32-34` | `\begin{equation} L_{\max} = M_{\text{total}} \cdot r_{\text{char}} \cdot v_{\text{char}} \end{equation}` | `review_of_ctl-pinn_framework.md:46` | `$$L_{\max} = M_{\text{total}} \cdot r_{\text{char}} \cdot v_{\text{char}}$$` | MATCH |
| 4 | `foundational_physical_metrics.tex:67-69` | `\begin{equation} \lambda \approx \frac{1}{T_{\text{horizon}}} \sum_{i=1}^{N_{\text{steps}}} \ln(a_i) \end{equation}` | `review_of_ctl-pinn_framework.md:72` | `$$\lambda \approx \frac{1}{T_{\text{horizon}}} \sum_{i=1}^{N_{\text{steps}}} \ln(a_i)$$` | MATCH |
| 5 | `foundational_physical_metrics.tex:72-74` | `\begin{equation} \tau_L = \frac{1}{\lambda} \end{equation}` | `review_of_ctl-pinn_framework.md:74` | `$$\tau_L = \frac{1}{\lambda}$$` | MATCH |
| 6 | `foundational_physical_metrics.tex:123-126` | `\begin{align} E_{\text{scale}} &= \|\text{median}(\{E_j\})\| + 10^{-8} \\ s_{\text{min\_scale}} &= \text{median}(\{r_{\text{char},j}\}) \end{align}` | `review_of_ctl-pinn_framework.md:116-120` | `$$\begin{aligned} E_{\text{scale}} &= \|\text{median}(\{E_j\})\| + 10^{-8} \\ s_{\text{min\_scale}} &= \text{median}(\{r_{\text{char},j}\}) \end{aligned}$$` | MATCH |

All 6 display-math blocks match source LaTeX exactly (modulo the standard `align` → `aligned` pandoc rewriting for use inside `$$...$$`).

**Pandoc artifact sweep (section line range 18-122):**
- `^\\-` count in section 2 (pre-fix): 26 (14 indented `    \-` + 12 unindented `\-`); all confirmed pandoc artifacts (source uses plain `- ` markers on those exact lines); preserved-as-legitimate count: 0
- `\\[` count in section 2: 0 (no escaped prose brackets; the `\sum`, `\frac`, `\sqrt` etc. are all inside `$...$` and unescaped)
- Post-fix `^\\-` count: 0; post-fix `\\[` count: 0

---

### 3. data_scaling_normalization.tex (table-heavy)

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-02-05 | Conversion | MINOR | `data_scaling_normalization.tex:7, 60, 63` | `review_of_ctl-pinn_framework.md:134, 188, 192` | Pandoc escaped 6 prose `[-1, 1]` / `[0, 1]` / `[t, IC]` bracket pairs as `\[...\]`; source uses plain unescaped form. Replaced 6 occurrences with unescaped equivalents (1 on candidate line 134, 2 on line 188, 3 on line 192). | Fixed |
| RoF-13-02-06 | Conversion | MINOR | `data_scaling_normalization.tex:25, 27, 29, 31, 35` | `review_of_ctl-pinn_framework.md:142, 144, 146, 148, 150, 152, 154` | Pandoc escaped 7 list `- ` markers (the `- \textbf{Time Normalization:}` / `Spatial and Velocity Scaling:` / characteristic length / characteristic velocity / position-scaling / velocity-scaling / inverse-transformation bullets) as `\-`; source uses plain `- `. Replaced 7 occurrences with `- `. | Fixed |
| RoF-13-02-07 | table | MINOR | `data_scaling_normalization.tex:67-98` | `review_of_ctl-pinn_framework.md:197-214` | Pandoc rendered the 13-row `\begin{longtable}` "Definitive Input Vector Specification" using grid-table format (`+----+----+`, `+:===+:===+`) with `\endhead` continuation artifacts: 1 duplicate header row, 2 LaTeX `Table N -- continued from previous page` / `Continued on next page` marker rows, plus 14 row-separator `+----+` lines. **D-29 applied — converted to GFM pipe-table** (Phase 11 precedent: DQA-02-001 in `data_quality_assessment_verification_report.md` converted a pandoc multiline table to GFM). Removed: 14 row-separator lines, 1 duplicate header row, 2 continuation marker rows. Net: grid table replaced with single 13-row GFM pipe-table preceded by 5-column header and `:---` alignment row, with the `\caption{Definitive Input Vector Specification}` rendered as a trailing `: Definitive Input Vector Specification` caption line per pandoc convention. | Fixed |
| RoF-13-02-08 | Conversion | MINOR | `data_scaling_normalization.tex:83-96` (table cells in `[-1, 1]` / `[0, 1]` Final Range column) | `review_of_ctl-pinn_framework.md:199-212` | Pandoc escaped all 14 `[-1, 1]` / `[0, 1]` table-cell range values inside the longtable as `\[-1, 1\]` / `\[0, 1\]`; source uses unescaped form. Folded into the table conversion (RoF-13-02-07) — the rebuilt GFM table writes all 14 ranges unescaped. | Fixed |

**Content audit:**
- Heading: `\section{Unifying Data Scaling and Normalization Protocols}` → `# Unifying Data Scaling and Normalization Protocols` (candidate line 124) — MATCH
- Subsections: `\subsection{Standardization of Spatiotemporal Normalization and Unit Conversion}` → `## Standardization of Spatiotemporal Normalization and Unit Conversion` (candidate line 128) — MATCH; `\subsection{Consistent Application of Numerical Softening Parameters}` → `## Consistent Application of Numerical Softening Parameters` (candidate line 164) — MATCH; `\subsection{Finalized Normalization Schema for the Input Vector}` → `## Finalized Normalization Schema for the Input Vector` (candidate line 182) — MATCH
- Paragraph headings: `\paragraph{Context and Validation}` → `#### Context and Validation` (candidate lines 132, 168, 186) — 3 occurrences MATCH; `\paragraph{Proposed Solution and Implementation}` → `#### Proposed Solution and Implementation` (candidate lines 138, 172, 190) — 3 occurrences MATCH; `\paragraph{Justification}` → `#### Justification` (candidate line 176) — MATCH (FIDEL-05 heading map applied)
- Lead prose paragraph (source line 2) → candidate line 126 — MATCH
- 4-item top-level list under "Proposed Solution and Implementation" of subsection 3.1 (Time Normalization; Spatial and Velocity Scaling with 4-item nested list; Inverse Transformation): source lines 14-40 → candidate lines 142-160 — MATCH; bullet rendering preserved as `- **...**` after `\-` artifact removal
- Inline math (`$t' = t/T$`, `$t \in [0, T]$`, `$[0, 1]$`, `$T = t_{\max} = 10$`, `$D = \sqrt[3]{G T^2} \approx 4.6416$`, `$V = D / T \approx 0.46416$`, `$\mathbf{r}'_i = \mathbf{r}_i / D$`, `$\mathbf{v}'_i = \mathbf{v}_i / V$`, `$\epsilon = 10^{-10}$`, `$\epsilon_{\text{soft}} = 10^{-5}$`, `$\boldsymbol{\epsilon_{\text{soft}} = 10^{-5}}$`) — MATCH throughout
- Display math: `\begin{equation}` block at source lines 16-18 → candidate inline `$$t' = 2 \left( \frac{t}{T} \right) - 1$$` (candidate line 142) — MATCH (pandoc inlined the equation environment into the bullet text); `\begin{align}` block at source lines 36-40 → candidate `$$\begin{aligned} t &= ... \\ \mathbf{r} &= \mathbf{r}' \cdot D \\ \mathbf{v} &= \mathbf{v}' \cdot V \end{aligned}$$` (candidate lines 155-160) — MATCH (`align` → `aligned` per pandoc convention)
- `\texttt{...}` (`PINN_architecture_plan.tex`, `CTL-instruction-final.tex`, `physical_to_scaled`, `scaled_to_physical`, `tanh`) — backtick-rendered code spans MATCH
- `\textbf{...}` rendered as `**...**` throughout — MATCH (including inline `\boldsymbol{...}` rendered as `$\boldsymbol{...}$`)
- LaTeX hyphenation hints `Imple\-mentation` (source line 62) collapsed to plain `Implementation` (candidate line 190) — MATCH (correct pandoc behavior; not a discrepancy); `\allowbreak` directive (source line 47) inside `\texttt{PINN\_\allowbreak architecture\_\allowbreak plan.tex}` collapsed correctly to `PINN_architecture_plan.tex` in candidate
- `\renewcommand{\arraystretch}{1.2}` and `\renewcommand{\arraystretch}{1.0}` (source lines 67, 98) — non-rendering directives, correctly omitted from candidate

**Table cell-by-cell verification (FIDEL-04 per D-15) — 13 rows × 5 columns of "Definitive Input Vector Specification":**

| # | Source row (data_scaling_normalization.tex) | Candidate row (review_of_ctl-pinn_framework.md) | Component Name | Symbol | Calculation Formula | Normalization Formula | Final Range | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | line 83 | line 199 | Time | `$t'$` | `$t_{\text{phys}} \in [0, 10]$` | `$2 \cdot (t_{\text{phys}} / 10) - 1$` | `[-1, 1]` | MATCH |
| 2 | line 84 | line 200 | Normalized Mass 1 | `$m_1^{\text{norm}}$` | Mass fraction of body 1 | `$2 \cdot (m_1 / M_{\text{total}}) - 1$` | `[-1, 1]` | MATCH |
| 3 | line 85 | line 201 | Normalized Mass 2 | `$m_2^{\text{norm}}$` | Mass fraction of body 2 | `$2 \cdot (m_2 / M_{\text{total}}) - 1$` | `[-1, 1]` | MATCH |
| 4 | line 86 | line 202 | Normalized Mass 3 | `$m_3^{\text{norm}}$` | Mass fraction of body 3 | `$2 \cdot (m_3 / M_{\text{total}}) - 1$` | `[-1, 1]` | MATCH |
| 5 | line 87 | line 203 | Normalized Energy | `$E^{\text{norm}}$` | Total mechanical energy `$E=T+V$` | `$\tanh(E/E_{\text{scale}})$` | `[-1, 1]` | MATCH |
| 6 | line 88 | line 204 | Normalized Ang. Mom. | `$L_{\text{norm}}$` | `$L = \|\|\sum m_i (\mathbf{r}'_i \times \mathbf{v}'_i)\|\|$` | `$L / L_{\max}$` | `[0, 1]` | MATCH |
| 7 | line 89 | line 205 | Normalized Virial Ratio | `$Q^{\text{norm}}$` | `$Q = 2T / \|V\|$` | `$\tanh((Q - 1) / Q_{\text{scale}})$` | `[-1, 1]` | MATCH |
| 8 | line 90 | line 206 | Normalized Min. Sep. | `$s_{\min}^{\text{norm}}$` | `$s_{\min} = \min_{i<j} \|\|\mathbf{r}'_i - \mathbf{r}'_j\|\|$` | `$\tanh(s_{\min} / s_{\min\_\text{scale}})$` | `[-1, 1]` | MATCH |
| 9 | line 91 | line 207 | Shape Invariant 1 | `$I_1^{\text{norm}}$` | `$d_{\text{short}} / d_{\text{long}}$` | `$2 \cdot I_1 - 1$` | `[-1, 1]` | MATCH |
| 10 | line 92 | line 208 | Shape Invariant 2 | `$I_2^{\text{norm}}$` | `$d_{\text{mid}} / d_{\text{long}}$` | `$2 \cdot I_2 - 1$` | `[-1, 1]` | MATCH |
| 11 | line 93 | line 209 | Shape Invariant 3 | `$I_3$` | `$(d_{\text{sh}}+d_{\text{mid}}-d_{\text{lg}})/(d_{\text{sh}}+d_{\text{mid}}+d_{\text{lg}})$` | `$I_3$` (already in range) | `[-1, 1]` | MATCH |
| 12 | line 94 | line 210 | Velocity Angle 1 | `$\theta_1^{\text{norm}}$` | `$\text{angle}(\mathbf{r}'_1, \mathbf{v}'_1) / \pi$` | `$2 \cdot \theta_1 - 1$` | `[-1, 1]` | MATCH |
| 13 | line 95 | line 211 | Velocity Angle 2 | `$\theta_2^{\text{norm}}$` | `$\text{angle}(\mathbf{r}'_2, \mathbf{v}'_2) / \pi$` | `$2 \cdot \theta_2 - 1$` | `[-1, 1]` | MATCH |
| 14 | line 96 | line 212 | Normalized Inertia | `$I^{\text{norm}}$` | Trace of moment of inertia tensor | `$\tanh(I_{\text{trace}} / (M_{\text{total}} \cdot r_{\text{char}}^2))$` | `[-1, 1]` | MATCH |

All 14 data rows (the Time row plus the 13 IC components) match the source LaTeX cell-by-cell after the GFM rebuild. Note: the table semantically has 14 data rows although only 13 of them are IC components — the first row is the time coordinate, which together with the 13 IC components forms the 14-dimensional input vector (consistent with the source caption "Definitive Input Vector Specification" and the prose at source line 60 / candidate line 188 that describes a "14-dimensional input vector [t, IC]"). The 5-column header (`Component Name`, `Symbol`, `Calculation Formula (using scaled $\mathbf{r}'$, $\mathbf{v}'$)`, `Normalization Formula`, `Final Range`) matches source line 71 — MATCH. The caption `: Definitive Input Vector Specification` (candidate line 214) matches source line 69 `\caption{Definitive Input Vector Specification}` — MATCH.

**Pandoc artifact sweep (section line range 124-218):**
- `^\\-` count in section 3 (pre-fix): 7 (all confirmed pandoc artifacts at candidate lines 142, 144, 146, 148, 150, 152, 154; source uses plain `- ` markers); preserved-as-legitimate count: 0
- `\\[` count in section 3 (pre-fix): 23 total (~9 prose + ~14 table cells; all pandoc artifacts; source uses unescaped `[-1, 1]` / `[0, 1]` / `[t, IC]`)
- Grid-table separator (`+---`) count in section 3 (pre-fix): 14 lines (1 top + 1 header-bottom + 13 row-bottoms); all removed during D-29 GFM conversion
- Continuation marker count in section 3 (pre-fix): 2 (`Table -- continued from previous page` at original line ~199 and `Continued on next page` at original line ~203; both removed)
- Duplicate header row count in section 3 (pre-fix): 1 (header row replicated for the `\endhead` continuation context; removed)
- Post-fix `^\\-` count: 0; post-fix `\\[` count: 0; post-fix grid-separator count: 0; post-fix continuation marker count: 0; post-fix duplicate header row count: 0

### 4. architectural_initialization_refinements.tex

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-02-09 | Conversion | MINOR | `architectural_initialization_refinements.tex:19, 21, 23` | `review_of_ctl-pinn_framework.md:241, 243, 245` | Pandoc escaped 3 list `- \textbf{Stages ...}` markers (the SIREN `first_omega_0` schedule bullets) as `\-`; source uses plain `- `. Replaced 3 occurrences with `- `. | Fixed |

**Content audit:**
- Heading: `\section{Architectural and Initialization Refinements for the SIREN Backbone}` → `# Architectural and Initialization Refinements for the SIREN Backbone` (candidate line 219) — MATCH
- Subsection: `\subsection{A Curriculum-Integrated Schedule for SIREN Frequency (\texorpdfstring{$\omega_0$}{omega\_0})}` → `## A Curriculum-Integrated Schedule for SIREN Frequency ($\omega_0$)` (candidate line 223) — MATCH; `\texorpdfstring{$\omega_0$}{omega\_0}` collapsed to inline math correctly
- Paragraph headings: `\paragraph{Context and Validation}` → `#### Context and Validation` (candidate line 227) — MATCH; `\paragraph{Proposed Solution and Implementation}` → `#### Proposed Solution and Implementation` (candidate line 233) — MATCH; `\paragraph{Implementation Action:}` → `#### Implementation Action:` (candidate line 247) — MATCH (FIDEL-05 heading map applied; trailing colon preserved)
- Lead prose paragraph (source line 2) → candidate line 221 — MATCH
- 3-item list of stage-based schedule (Stages 0-1; Stages 2-3; Stages 4-6): source lines 19-23 → candidate lines 241, 243, 245 — MATCH; `\textbf{...}` rendered as `**...**`; `\texttt{first\_omega\_0 = 30.0}` / `20.0` / `10.0` rendered as backtick code spans with the underscore unescaped
- "Issues Resolved: 4, 14" label: source line 5 (`\textbf{Issues Resolved: 4, 14}`) → candidate line 225 (`**Issues Resolved: 4, 14**`) — MATCH
- Inline math (`$\omega_0$`, `$U[-1/\sqrt{n_{\text{in}}}, 1/\sqrt{n_{\text{in}}}]$`) — MATCH throughout
- `\texttt{...}` (`PINN_architecture_plan.tex`, `first_omega_0 = 30`, `update_omega0`, `total_epochs`, `first_omega_0`) — backtick-rendered code spans MATCH
- LaTeX em-dash directive `\textemdash` (source line 27, twice) collapsed to `---` (candidate line 249) — MATCH (correct pandoc behavior; source uses LaTeX em-dash macro, candidate uses ASCII triple-hyphen which renders as em-dash in markdown)

**Pandoc artifact sweep (section line range 219-249):**
- `^\\-` count in section 4 (pre-fix): 3 (all confirmed pandoc artifacts at candidate lines 241, 243, 245; source uses plain `- ` markers on those exact lines); preserved-as-legitimate count: 0
- `\\[` count in section 4: 0 (no escaped prose brackets; the `[-1/\sqrt{n_{\text{in}}}, 1/\sqrt{n_{\text{in}}}]` is correctly inside `$...$` and unescaped)
- Post-fix `^\\-` count: 0; post-fix `\\[` count: 0

### 5. multi_component_loss_framework.tex (math + code)

**Status:** PENDING — FIDEL-01 formula checklist required per D-14, plus
verbatim verification of the ~40-line `compute_kinematics` PyTorch code
block (argument names `network_output_r` / `time_input_t`, comment
"CRITICAL: Retain graph for second derivative", `create_graph=True`/`False`
values). Source is ~116 lines / 11550 bytes with ~3 display-math equations
expected (data loss L1, physics residual fi(t'), total Hamiltonian).

### 6. training_sampling_strategy.tex

**Status:** PENDING — prose + lists. Source is ~98 lines / 10645 bytes.
Wave 2 verifies heading map, prose paragraphs, list items, and any inline math.

### 7. conclusion_and_recommendations.tex (table)

**Status:** PENDING — FIDEL-04 cell-by-cell for the 6-row "Consolidated
Hyperparameter Schedule" table. Source is ~27 lines / 2954 bytes. Wave 2
verifies all rows cell-by-cell and applies any markdown-table reformat
needed for D-29 GFM compliance.

<!-- Phase 13 discrepancy IDs: RoF-13-{plan}-{NN}; baseline RoF-13-01-BASELINE; source-issue IDs SI-RoF-NNN; severity values BLOCKING|MAJOR|MINOR|INFO; type values Conversion|text|table|structure|figure (see 13-PATTERNS.md Pattern 2 line 178). -->

## Fix Log

| ID | Section | Fix summary |
|---|---|---|
| RoF-13-01-BASELINE | Global | review_of_ctl-pinn_framework.md confirmed as single candidate (CAND-02). Vacuous Policy Checks recorded with all source counts = 0 and candidate `[@refN]` count = 0. |
| RoF-13-02-01 | 1. executive_summary.tex | Replaced 1 pandoc-escaped prose bracket pair `\[-1, 1\]` with unescaped `[-1, 1]` at candidate line 8. |
| RoF-13-02-02 | 2. foundational_physical_metrics.tex | Replaced 4 pandoc-escaped 4-space-indented `    \- ` list markers (under enumerate item 1, "Maximum Angular Momentum") with `    - ` at candidate lines 38, 40, 46, 48. |
| RoF-13-02-03 | 2. foundational_physical_metrics.tex | Replaced 10 pandoc-escaped 4-space-indented `    \- ` list markers (under enumerate item 2, "Lyapunov Time") with `    - ` at candidate lines 56, 58, 60, 62, 64, 66, 68, 70, 72, 74. |
| RoF-13-02-04 | 2. foundational_physical_metrics.tex | Replaced 12 pandoc-escaped unindented `\- ` list markers (worker function and orchestrator bullets in subsection 2.2) with `- ` at candidate lines 92, 94, 96, 98, 100, 102, 106, 108, 110, 112, 114, 116. |
| RoF-13-02-05 | 3. data_scaling_normalization.tex | Replaced 6 pandoc-escaped prose bracket pairs (`\[-1, 1\]` / `\[0, 1\]` / `\[t, IC\]`) with unescaped equivalents at candidate lines 134, 188, 192. |
| RoF-13-02-06 | 3. data_scaling_normalization.tex | Replaced 7 pandoc-escaped `\- ` list markers (Time Normalization / Spatial-Velocity Scaling group / Inverse Transformation bullets) with `- ` at candidate lines 142, 144, 146, 148, 150, 152, 154. |
| RoF-13-02-07 | 3. data_scaling_normalization.tex | Converted 13-row "Definitive Input Vector Specification" longtable from pandoc grid-table to GFM pipe-table (D-29 applied; Phase 11 DQA-02-001 precedent). Removed 14 row-separator lines, 1 duplicate header row, and 2 LaTeX `Table -- continued from previous page` / `Continued on next page` continuation marker rows. Caption rendered as trailing `: Definitive Input Vector Specification` per pandoc convention. |
| RoF-13-02-08 | 3. data_scaling_normalization.tex | Folded into RoF-13-02-07: rebuilt GFM table writes all 14 `[-1, 1]` / `[0, 1]` Final Range cell values unescaped (originally pandoc-escaped as `\[-1, 1\]` / `\[0, 1\]` in 14 grid-table cells). |
| RoF-13-02-09 | 4. architectural_initialization_refinements.tex | Replaced 3 pandoc-escaped `\- ` list markers (the 3 stage-based `first_omega_0` schedule bullets) with `- ` at candidate lines 241, 243, 245. |

## Source Issues / Notes for Future Reconciliation

(Populated in Plan 03 — see CROSS-01 / D-17/D-18 inherited)

## Final Verification

(Populated in Plan 03 — see CLEAN-03 / D-47 / D-40)
