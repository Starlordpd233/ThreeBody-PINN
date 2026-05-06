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

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-02-10 | Conversion | MINOR | `multi_component_loss_framework.tex:13, 18, 23` | `review_of_ctl-pinn_framework.md:267, 269, 271` | Pandoc escaped 3 unindented `\- ` list markers (the L_data / L_physics / L_energy validation checklist bullets in subsection 5.1) as `\-`; source uses plain `- `. Replaced 3 occurrences with `- `. | Fixed |

**Content audit:**
- Heading: `\section{A Rigorous Framework for the Multi-Component Loss Function}` → `# A Rigorous Framework for the Multi-Component Loss Function` (candidate line 251) — MATCH
- Subsections (4 total): `\subsection{Clarifying the Use of Scaled Quantities in All Loss Components}` → `## Clarifying the Use of Scaled Quantities in All Loss Components` (candidate line 255) — MATCH; `\subsection{State Management and Integration of ALM Parameters}` → `## State Management and Integration of ALM Parameters` (candidate line 275) — MATCH; `\subsection{Reference Implementation for Automatic Differentiation (AD) of Kinematics}` → `## Reference Implementation for Automatic Differentiation (AD) of Kinematics` (candidate line 305) — MATCH; `\subsection{Selecting an Appropriate Huber Loss Delta (\texorpdfstring{$\delta$}{delta}) for Normalized Energy}` → `## Selecting an Appropriate Huber Loss Delta ($\delta$) for Normalized Energy` (candidate line 364) — MATCH; `\texorpdfstring` collapsed to inline math correctly
- Paragraph headings: 4 `\paragraph{Context and Validation}` → 4 `#### Context and Validation` at candidate lines 259, 279, 309, 368 — MATCH; 4 `\paragraph{Proposed Solution and Implementation}` → 4 `#### Proposed Solution and Implementation` at candidate lines 263, 283, 313, 372 — MATCH; 1 `\paragraph{Justification}` → `#### Justification` at candidate line 376 — MATCH (FIDEL-05 heading map applied; `\paragraph{Proposed Solution and Imple\-mentation}` source line 9 hyphenation hint correctly collapsed to plain `Implementation` in candidate)
- Lead prose paragraph (source line 2) → candidate line 253 — MATCH
- 3-item top-level list under "Proposed Solution and Implementation" of subsection 5.1 (`L_data` / `L_physics` / `L_energy` validation bullets): source lines 12-26 → candidate lines 267, 269, 271 — MATCH; bullet rendering preserved as `- **...**` after `\-` artifact removal; pandoc inlined the `\begin{equation}` blocks into the bullet text using inline `$$...$$` form (correct pandoc behavior; semantically equivalent display math)
- Numbered enumerate list under "Proposed Solution and Implementation" of subsection 5.2 (Storage and Scope; Update Timing with 5-step nested enumerate; Persistence Across Curriculum Stages): source lines 37-49 → candidate lines 287-303 — MATCH; both top-level `1.` `2.` `3.` and nested `1.` through `5.` numbering preserved (note: pandoc rendered the nested enumerate inside item 2 with a 4-space-indented body)
- LaTeX em-dash directive `\textemdash` (source line 7, twice surrounding `$\mathcal{L}_{\text{data}}$, $\mathcal{L}_{\text{physics}}$, and $\mathcal{L}_{\text{energy}}$`) collapsed to `---` (candidate line 261) — MATCH
- `\texttt{...}` (`PINN_architecture_plan.tex`, `self.lambda_p = torch.tensor(0.0)`, `loss.backward()`, `optimizer.step()`, `optimizer.zero_grad()`, `create_graph=True`, `torch.autograd.grad`) — backtick-rendered code spans MATCH
- `\textbf{...}` rendered as `**...**` throughout — MATCH (including `\boldsymbol{\delta = 0.1}` rendered as `$\boldsymbol{\delta = 0.1}$`)
- `\allowbreak` directive (source line 47, inside `\texttt{PINN\_\allowbreak architecture\_\allowbreak plan.tex}`) — non-rendering hyphenation hint, correctly omitted (candidate renders the texttt as `PINN_architecture_plan.tex` clean)
- Inline math (`$\mathcal{L}_{\text{data}}$`, `$\mathcal{L}_{\text{physics}}$`, `$\mathcal{L}_{\text{energy}}$`, `$\mathbf{r}'_{\text{pred}}$`, `$\mathbf{r}'_{\text{true}}$`, `$\mathbf{r}_{\text{true}} / D$`, `$\lambda_p$`, `$\mu_p$`, `$v_p$`, `$\delta = 1.0$`, `$\delta = 0.1$`, `$|\Delta H_k|$`) — MATCH throughout

**Formula checklist (FIDEL-01 per D-14):**

| # | Source location | LaTeX form (one-line excerpt) | Candidate location | Markdown form (one-line excerpt) | Status |
|---|---|---|---|---|---|
| 1 | `multi_component_loss_framework.tex:14-16` | `\begin{equation} \mathcal{L}_{\text{data}} = \frac{1}{N_{\text{data}}} \sum_{k=1}^{N_{\text{data}}} \|\|\mathbf{r}'_{\text{pred}}(t'_k) - \mathbf{r}'_{\text{true}}(t'_k)\|\|_1 \end{equation}` | `review_of_ctl-pinn_framework.md:267` (inlined into bullet) | `$$\mathcal{L}_{\text{data}} = \frac{1}{N_{\text{data}}} \sum_{k=1}^{N_{\text{data}}} \|\|\mathbf{r}'_{\text{pred}}(t'_k) - \mathbf{r}'_{\text{true}}(t'_k)\|\|_1$$` | MATCH |
| 2 | `multi_component_loss_framework.tex:19-21` | `\begin{equation} f_i(t') = \mathbf{a}'_{\theta}(t', i) - \sum_{j \neq i} m_j \frac{\mathbf{r}'_{\theta}(t', j) - \mathbf{r}'_{\theta}(t', i)}{(\|\|\mathbf{r}'_{\theta}(t', j) - \mathbf{r}'_{\theta}(t', i)\|\| + \epsilon_{\text{soft}})^3} \end{equation}` | `review_of_ctl-pinn_framework.md:269` (inlined into bullet) | `$$f_i(t') = \mathbf{a}'_{\theta}(t', i) - \sum_{j \neq i} m_j \frac{\mathbf{r}'_{\theta}(t', j) - \mathbf{r}'_{\theta}(t', i)}{(\|\|\mathbf{r}'_{\theta}(t', j) - \mathbf{r}'_{\theta}(t', i)\|\| + \epsilon_{\text{soft}})^3}$$` | MATCH |
| 3 | `multi_component_loss_framework.tex:24-26` | `\begin{equation} H_{\text{total}}(\mathbf{r}', \mathbf{v}') = \sum_{i=1}^{N} \frac{1}{2} m_i \|\|\mathbf{v}'_i\|\|^2 - \sum_{i<j} \frac{m_i m_j}{\|\|\mathbf{r}'_i - \mathbf{r}'_j\|\| + \epsilon_{\text{soft}}} \end{equation}` | `review_of_ctl-pinn_framework.md:271` (inlined into bullet) | `$$H_{\text{total}}(\mathbf{r}', \mathbf{v}') = \sum_{i=1}^{N} \frac{1}{2} m_i \|\|\mathbf{v}'_i\|\|^2 - \sum_{i<j} \frac{m_i m_j}{\|\|\mathbf{r}'_i - \mathbf{r}'_j\|\| + \epsilon_{\text{soft}}}$$` | MATCH |

All 3 display-math blocks match source LaTeX exactly. Pandoc inlined the `\begin{equation}` environments at the end of each list-item bullet text using `$$...$$`; this is correct pandoc behavior for equation environments inside list items and preserves both the bullet/equation association and the math content verbatim.

**Code block verbatim verification (subsection 5.3 PyTorch reference implementation):**

| Aspect | Source (`multi_component_loss_framework.tex:59-104`) | Candidate (`review_of_ctl-pinn_framework.md:317-360`) | Status |
|---|---|---|---|
| Code block delimiters | `\begin{lstlisting}` / `\end{lstlisting}` | 4-space indented code block (pandoc default rendering for lstlisting) | MATCH (correct pandoc behavior for lstlisting → indented code block) |
| Function signature | `def compute_kinematics(network_output_r, time_input_t):` | `def compute_kinematics(network_output_r, time_input_t):` | MATCH (argument names verified verbatim) |
| Docstring opening | `"""` | `"""` | MATCH |
| Docstring `Args:` block | `network_output_r (torch.Tensor)` / `time_input_t (torch.Tensor)` / `Shape: (N_points, 9)` / `Shape: (N_points, 1)` | identical | MATCH |
| Docstring `Returns:` block | `velocities_v (torch.Tensor)` / `accelerations_a (torch.Tensor)` / `Shape (N_points, 9)` (twice) | identical | MATCH |
| Gradient enable check | `if not time_input_t.requires_grad:` / `time_input_t.requires_grad_(True)` | identical | MATCH |
| First derivative comment | `# Compute first derivative (velocities)` | identical | MATCH |
| `grad_outputs_v` setup | `grad_outputs_v = torch.ones_like(network_output_r)` | identical | MATCH |
| First `torch.autograd.grad` call | `velocities_v, = torch.autograd.grad(outputs=network_output_r, inputs=time_input_t, grad_outputs=grad_outputs_v, create_graph=True)` | identical | MATCH |
| `create_graph=True` comment | `# CRITICAL: Retain graph for second derivative` | `# CRITICAL: Retain graph for second derivative` | MATCH (verbatim, including capitalization "CRITICAL" and the colon) |
| Second derivative comment | `# Compute second derivative (accelerations)` | identical | MATCH |
| `grad_outputs_a` setup | `grad_outputs_a = torch.ones_like(velocities_v)` | identical | MATCH |
| Second `torch.autograd.grad` call | `accelerations_a, = torch.autograd.grad(outputs=velocities_v, inputs=time_input_t, grad_outputs=grad_outputs_a, create_graph=False)` | identical | MATCH |
| `create_graph=False` comment | `# Not needed for second derivative` | `# Not needed for second derivative` | MATCH |
| Return statement | `return velocities_v, accelerations_a` | identical | MATCH |

The `compute_kinematics` PyTorch reference implementation is preserved verbatim. All argument names (`network_output_r`, `time_input_t`), the critical `create_graph=True`/`False` keyword arguments, and the explanatory comments (notably `# CRITICAL: Retain graph for second derivative`) are character-for-character identical to the LaTeX source.

**Pandoc artifact sweep (section line range 251-378):**
- `^\\-` count in section 5 (pre-fix): 3 (all confirmed pandoc artifacts at candidate lines 267, 269, 271; source uses plain `- ` markers); preserved-as-legitimate count: 0
- `\\[` count in section 5: 0 (no escaped prose brackets; the inline `$...$` math is correctly unescaped)
- Post-fix `^\\-` count: 0; post-fix `\\[` count: 0

### 6. training_sampling_strategy.tex

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-02-11 | Conversion | MINOR | `training_sampling_strategy.tex:7, 26, 57, 73` | `review_of_ctl-pinn_framework.md:390, 408, 440, 458` | Pandoc escaped 4 prose `[-1, 1]` bracket pairs (subsection 6.1 lead, Collocation Time Points definition, 50% Uniform Sampling bullet, For Physics and Energy Losses bullet) as `\[-1, 1\]`; source uses unescaped form. Replaced 4 occurrences with `[-1, 1]`. | Fixed |
| RoF-13-02-12 | Conversion | MINOR | `training_sampling_strategy.tex:15, 17` | `review_of_ctl-pinn_framework.md:398, 400` | Pandoc escaped 2 unindented `\- ` list markers (Data Points / Collocation Points definition bullets in subsection 6.1) as `\-`; source uses plain `- `. Replaced 2 occurrences with `- `. | Fixed |
| RoF-13-02-13 | Conversion | MINOR | `training_sampling_strategy.tex:24, 26, 32, 34` | `review_of_ctl-pinn_framework.md:406, 408, 414, 416` | Pandoc escaped 4 indented `    \- ` list markers (Data Time Points / Collocation Time Points / `L_data` / `L_physics-and-energy` bullets nested under enumerate items 1 and 3 in subsection 6.1) as `    \-`; source uses plain `    - `. Replaced 4 occurrences with `    - `. | Fixed |
| RoF-13-02-14 | Conversion | MINOR | `training_sampling_strategy.tex:50, 52, 57, 59` | `review_of_ctl-pinn_framework.md:434, 436, 440, 442` | Pandoc escaped 4 indented `    \- ` list markers (Replay / Lookahead / 50% Uniform / 50% Acceleration-Weighted bullets nested under enumerate items 1 and 2 in subsection 6.2) as `    \-`; source uses plain `    - `. Replaced 4 occurrences with `    - `. | Fixed |
| RoF-13-02-15 | Conversion | MINOR | `training_sampling_strategy.tex:73, 75` | `review_of_ctl-pinn_framework.md:458, 460` | Pandoc escaped 2 unindented `\- ` list markers (For Physics and Energy Losses / For the Data Fidelity Loss bullets in subsection 6.3) as `\-`; source uses plain `- `. Replaced 2 occurrences with `- `. | Fixed |
| RoF-13-02-16 | Conversion | MINOR | `training_sampling_strategy.tex:91, 93, 95` | `review_of_ctl-pinn_framework.md:480, 482, 484` | Pandoc escaped 3 indented `    \- ` list markers (Stages 0-1 / Stages 2-3 / Stages 4-6 clipping multiplier $C$ schedule bullets nested under enumerate item 2 in subsection 6.4) as `    \-`; source uses plain `    - `. Replaced 3 occurrences with `    - `. | Fixed |

**Content audit:**
- Heading: `\section{A Coherent Training and Data Sampling Strategy}` → `# A Coherent Training and Data Sampling Strategy` (candidate line 380) — MATCH
- Subsections (4 total): `\subsection{Unifying Data and Collocation Point Sampling}` → `## Unifying Data and Collocation Point Sampling` (candidate line 384) — MATCH; `\subsection{Finalizing the Curriculum-Aware Batch Construction Protocol}` → `## Finalizing the Curriculum-Aware Batch Construction Protocol` (candidate line 420) — MATCH; `\subsection{Strategy for Integrating Mixed-Resolution Trajectory Data}` → `## Strategy for Integrating Mixed-Resolution Trajectory Data` (candidate line 446) — MATCH; `\subsection{Definitive Implementation of Curriculum-Aware Gradient Clipping}` → `## Definitive Implementation of Curriculum-Aware Gradient Clipping` (candidate line 464) — MATCH
- Paragraph headings: 4 `\paragraph{Context and Validation}` → 4 `#### Context and Validation` at candidate lines 388, 424, 450, 468 — MATCH; 4 `\paragraph{Proposed Solution and Implementation}` → 4 `#### Proposed Solution and Implementation` at candidate lines 394, 428, 454, 472 — MATCH (FIDEL-05 heading map applied)
- Lead prose paragraph (source line 2) → candidate line 382 — MATCH
- 2-item top-level list under "Proposed Solution and Implementation" of subsection 6.1 (Data Points / Collocation Points definitional bullets): source lines 14-17 → candidate lines 398, 400 — MATCH after `\-` removal
- 3-item top-level enumerate under subsection 6.1 (Batch Sampling with 2 indented sub-bullets; Unified Forward Pass; Loss Computation with 2 indented sub-bullets): source lines 20-36 → candidate lines 404-416 — MATCH; both top-level `1.` `2.` `3.` and indented sub-bullets render correctly after `\-` removal
- 2-item enumerate under subsection 6.2 (Replay and Lookahead Sampling with 2 indented sub-bullets; Hybrid Time Point Sampling with 2 indented sub-bullets): source lines 46-61 → candidate lines 432-442 — MATCH after `\-` removal
- 2-item top-level list under subsection 6.3 (For Physics and Energy Losses; For the Data Fidelity Loss): source lines 72-75 → candidate lines 458, 460 — MATCH after `\-` removal
- 2-item enumerate under subsection 6.4 (Algorithm; Curriculum-Aware $C$ Schedule with 3 indented sub-bullets for Stages 0-1, 2-3, 4-6): source lines 86-95 → candidate lines 476-484 — MATCH after `\-` removal
- LaTeX directives `\textasciitilde` (source lines 50, 52, before "95%" / "5%") collapsed to `\~` (escaped tilde, candidate lines 434, 436) — MATCH (correct pandoc behavior; the tilde is escaped to prevent markdown interpreting it, semantically equivalent)
- `\allowbreak` directives (source lines 42, 45, 67, 82) inside `\texttt{...}` collapsed correctly: `\texttt{CTL-instruction-\allowbreak final.tex}` → `CTL-instruction-final.tex` and `\texttt{PINN\_\allowbreak architecture\_\allowbreak plan.tex}` → `PINN_architecture_plan.tex` (correct pandoc behavior; non-rendering hyphenation hints)
- `clip\-ping` hyphenation hint (source line 82) collapsed to plain `clipping` (candidate line 470) — MATCH (correct pandoc behavior)
- `\texttt{...}` (`CTL-instruction-final.tex`, `PINN_architecture_plan.tex`, `loss.backward()`, `optimizer.step()`) — backtick-rendered code spans MATCH
- `\textbf{...}` rendered as `**...**` throughout — MATCH
- Inline math (`$\mathcal{L}_{\text{data}}$`, `$\mathcal{L}_{\text{physics}}$`, `$\mathcal{L}_{\text{energy}}$`, `$N_{\text{data\_pts}}$`, `$N_{\text{col\_pts}}$`, `$t_{\text{data}}'$`, `$t_{\text{col}}'$`, `$t_{\text{union}}' = t_{\text{data}}' \cup t_{\text{col}}'$`, `$|\mathbf{a}(t)|$`, `$C$`, `$C = 8.5$`, `$C = 5.0$`, `$C = 3.0$`) — MATCH throughout

**Pandoc artifact sweep (section line range 380-486):**
- `^\\-` count in section 6 (pre-fix): 15 (2 unindented in 6.1 + 4 indented in 6.1 + 4 indented in 6.2 + 2 unindented in 6.3 + 3 indented in 6.4 = 15; all confirmed pandoc artifacts; source uses plain `- ` markers); preserved-as-legitimate count: 0
- `\\[` count in section 6 (pre-fix): 4 (all confirmed pandoc-escaped prose `[-1, 1]` brackets; source uses unescaped form on those exact lines)
- Post-fix `^\\-` count: 0; post-fix `\\[` count: 0

### 7. conclusion_and_recommendations.tex (table)

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-02-17 | table | MINOR | `conclusion_and_recommendations.tex:9-27` | `review_of_ctl-pinn_framework.md:496-512` (pre-fix; rebuilt at lines 497-506 post-fix) | Pandoc rendered the 6-row `\begin{tabular}` "Consolidated Hyperparameter Schedule" using pandoc multiline-table format (3 long `-{>=100}` separator lines at original candidate lines 496, 498, 510 plus blank-line row separators). **D-29 applied — converted to GFM pipe-table** (Phase 11 precedent: DQA-02-001 in `data_quality_assessment_verification_report.md` converted a pandoc multiline table to GFM). Removed: 3 long-dash separator lines and inter-row blank lines. Caption preserved as trailing `: Consolidated Hyperparameter Schedule for CTL-PINN Training`. | Fixed |

**Content audit:**
- Heading: `\section*{Conclusion and Consolidated Recommendations}` → `# Conclusion and Consolidated Recommendations` (candidate line 488) — MATCH (starred form rendered as `#`)
- Lead prose paragraph (source line 3) → candidate line 489 — MATCH
- Second paragraph (source line 5) → candidate line 491 — MATCH
- Third paragraph introducing the master table (source line 7) → candidate line 493 — MATCH
- `\addcontentsline{toc}{section}{Conclusion and Consolidated Recommendations}` (source line 2) — non-rendering directive, correctly omitted from candidate
- `\renewcommand{\arraystretch}{1.2}` and `\renewcommand{\arraystretch}{1.0}` (source lines 13, 26) — non-rendering directives, correctly omitted
- `\begin{table}[H]` / `\centering` / `\label{tab:hyperparameter_schedule}` (source lines 9-12) — non-rendering directives, correctly omitted
- Caption: `\caption{Consolidated Hyperparameter Schedule for CTL-PINN Training}` (source line 11) → `: Consolidated Hyperparameter Schedule for CTL-PINN Training` (candidate line 506) — MATCH (pandoc trailing-caption convention preserved)
- Table column header: 5-column header (`Parameter`, `Stage 0-1 (Stable)`, `Stage 2-3 (Mild Chaos)`, `Stage 4-6 (Chaotic)`, `Rationale`) at source line 16 → candidate line 497 — MATCH (all `\textbf{...}` wrappers preserved as `**...**` in the GFM-rebuilt header)

**Table cell-by-cell verification (FIDEL-04 per D-15) — 6 rows × 5 columns of "Consolidated Hyperparameter Schedule for CTL-PINN Training":**

| # | Source row (conclusion_and_recommendations.tex) | Candidate row (review_of_ctl-pinn_framework.md) | Parameter | Stage 0-1 (Stable) | Stage 2-3 (Mild Chaos) | Stage 4-6 (Chaotic) | Rationale | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | line 18 | line 499 | SIREN first\_omega\_0 | 30.0 | 20.0 | 10.0 | Matches network frequency resolution to data complexity. | MATCH |
| 2 | line 19 | line 500 | Energy Weight `$\lambda_E$` | `$10^{-3}$ - $10^{-2}$` | `$10^{-1}$ - $1$` | `$10^{1}$ - $10^{3}$` | Increases energy conservation constraint as chaos increases. | MATCH |
| 3 | line 20 | line 501 | Adam Initial LR | `$10^{-3}$ - $7\text{e-}4$` | `$4.9\text{e-}4$ - $3.4\text{e-}4$` | `$2.4\text{e-}4$ - $1.2\text{e-}4$` | Gradually reduces initial learning rate for more difficult stages. | MATCH |
| 4 | line 21 | line 502 | Gradient Clip `$C$` | 8.5 | 5.0 | 3.0 | Allows larger gradients for stable data; clips aggressively for chaotic data. | MATCH |
| 5 | line 22 | line 503 | L-BFGS Type | Full-Batch | Full-Batch / sL-BFGS | sL-BFGS | Switches to stochastic variant as cumulative dataset size grows. | MATCH |
| 6 | line 23 | line 504 | ALM State | Reset | Reset | Reset | Resets ALM statistics to adapt to new data distribution at each stage. | MATCH |

All 6 data rows match the source LaTeX cell-by-cell after the GFM rebuild. Notes on cell-level fidelity: (a) source `SIREN first\_omega\_0` LaTeX-escapes the underscore for `\texttt`-free typesetting, but pandoc passed through the raw token in the multiline table without backticks and we preserved `SIREN first_omega_0` (single-token, matches the prose at source line 38 / candidate line 499 where `first_omega_0` is unambiguous); (b) source uses LaTeX `\text{e-}4` for the `7e-4`-style numerals — preserved verbatim in inline math `$7\text{e-}4$` etc.; (c) all `$\lambda_E$`, `$C$` cell tokens preserved as inline math with `$...$` delimiters.

**Pandoc artifact sweep (section line range 488-end):**
- `^\\-` count in section 7 (pre-fix): 0 (the conclusion section uses no list bullets in source)
- `\\[` count in section 7 (pre-fix): 0 (no escaped prose brackets)
- Multiline-table separator (`-{>=20}`) count in section 7 (pre-fix): 3 lines (top, between header and body, and closing); all removed during D-29 GFM conversion
- Post-fix `^\\-` count: 0; post-fix `\\[` count: 0; post-fix multiline-table separator count: 0; post-fix grid-table separator count: 0; the table is now a GFM pipe-table (1 header + 1 alignment + 6 data rows = 8 pipe-rows) followed by the trailing caption line

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
| RoF-13-02-10 | 5. multi_component_loss_framework.tex | Replaced 3 pandoc-escaped unindented `\- ` list markers (L_data / L_physics / L_energy validation checklist bullets) with `- ` at candidate lines 267, 269, 271. |
| RoF-13-02-11 | 6. training_sampling_strategy.tex | Replaced 4 pandoc-escaped prose `\[-1, 1\]` bracket pairs (subsection 6.1 lead, Collocation Time Points definition, 50% Uniform Sampling bullet, For Physics and Energy Losses bullet) with unescaped `[-1, 1]` at candidate lines 390, 408, 440, 458. |
| RoF-13-02-12 | 6. training_sampling_strategy.tex | Replaced 2 pandoc-escaped unindented `\- ` list markers (Data Points / Collocation Points definitional bullets in subsection 6.1) with `- ` at candidate lines 398, 400. |
| RoF-13-02-13 | 6. training_sampling_strategy.tex | Replaced 4 pandoc-escaped 4-space-indented `    \- ` list markers (Data Time Points / Collocation Time Points / L_data / L_physics-and-energy bullets nested under enumerate items 1 and 3 in subsection 6.1) with `    - ` at candidate lines 406, 408, 414, 416. |
| RoF-13-02-14 | 6. training_sampling_strategy.tex | Replaced 4 pandoc-escaped 4-space-indented `    \- ` list markers (Replay / Lookahead / 50% Uniform / 50% Acceleration-Weighted bullets nested under enumerate items 1 and 2 in subsection 6.2) with `    - ` at candidate lines 434, 436, 440, 442. |
| RoF-13-02-15 | 6. training_sampling_strategy.tex | Replaced 2 pandoc-escaped unindented `\- ` list markers (For Physics and Energy Losses / For the Data Fidelity Loss bullets in subsection 6.3) with `- ` at candidate lines 458, 460. |
| RoF-13-02-16 | 6. training_sampling_strategy.tex | Replaced 3 pandoc-escaped 4-space-indented `    \- ` list markers (Stages 0-1 / Stages 2-3 / Stages 4-6 clipping multiplier $C$ schedule bullets nested under enumerate item 2 in subsection 6.4) with `    - ` at candidate lines 480, 482, 484. |
| RoF-13-02-17 | 7. conclusion_and_recommendations.tex | Converted 6-row "Consolidated Hyperparameter Schedule for CTL-PINN Training" table from pandoc multiline-table format (3 long-dash separator lines + blank-line row separators) to GFM pipe-table (D-29 applied; Phase 11 DQA-02-001 precedent). Caption preserved as trailing `: Consolidated Hyperparameter Schedule for CTL-PINN Training` per pandoc convention. All 6 data rows verified cell-by-cell against `conclusion_and_recommendations.tex:18-23`. |

## Source Issues / Notes for Future Reconciliation

(Populated in Plan 03 — see CROSS-01 / D-17/D-18 inherited)

## Final Verification

(Populated in Plan 03 — see CLEAN-03 / D-47 / D-40)
