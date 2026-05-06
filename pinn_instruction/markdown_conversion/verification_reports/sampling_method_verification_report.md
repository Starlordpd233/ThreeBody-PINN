# Sampling Method Markdown Verification Report

**Phase:** 15 | **Plan:** 02 | **Wave:** 2
**Source:** `pinn_instruction/original_latex/sampling-method/sampling_method_instruction.tex` (241 lines, 18,931 bytes)
**Date:** 2026-05-06

## Candidate Comparison

| Metric | Candidate A | Candidate B (winner) |
|--------|-------------|----------------------|
| Path | `pinn_instruction/markdown_conversion/sampling_method.md` | `pinn_instruction/markdown_conversion/pandoc_conversion/sampling_method_instruction.md` |
| Lines | 223 | 198 → 206 (after fixes) |
| Bytes | 16,817 | 16,562 |
| Overall F1 | 0.791 (P=0.784, R=0.798) | **0.856** (P=0.875, R=0.838) |
| Heading-fidelity | 1/10 | **10/10** |

### Per-Section F1 Scores

| Section | Title | Candidate A | Candidate B |
|---------|-------|-------------|-------------|
| Section 1 | Overview of the Data Generation Pipeline | 0.219 | **0.228** |
| Section 2 | Stage 1: Hierarchical Initial Conditions Generation | 0.080 | **0.131** |
| Section 3 | Stage 2: Enhanced Quasi-Random Sampling | 0.024 | **0.026** |
| Section 4 | Core Sampling Methodology | 0.298 | **0.337** |
| Section 5 | Enhancements to the Sampling Algorithm | 0.236 | **0.251** |
| Section 6 | Stage 3: Pre-Screening of Generated ICs for Short-Term Stability | 0.036 | **0.038** |
| Section 7 | The Pre-Screening Rationale | 0.096 | **0.103** |
| Section 8 | Pre-Screening Criteria | 0.162 | **0.180** |
| Section 9 | A Coordinated Strategy for Minimum Distance | 0.153 | **0.159** |
| Section 10 | Execution and Final Quality Control | 0.089 | **0.096** |

Candidate B leads all 10 sections on per-section F1.

### Human Inspection Notes

| Check | Candidate A | Candidate B |
|-------|-------------|-------------|
| FIDEL-01 (align* equations, src:64-69, 72-77) | Equations present but rendered as individual `$$` blocks; uses `\text{inner}` vs source `\rm inner` | Equations preserved in `$$\begin{aligned}...\end{aligned}` matching source `align*` structure; `\rm` matches source |
| FIDEL-06 (authcomment, src:26) | Present: line 13, `[Critical Update: ... virial ratio ... $s^{3}$ ...]` | Present: line 2, `[**Critical Update: ... virial ratio ... $s^3$ ...**]` |
| AUDIT-03 (comment block, src:130-134) | No content from comment block detected | No content from comment block detected |
| FIDEL-05 (heading hierarchy) | 1 top-level `#` (document title, not in source); 10 sections rendered as `##`/`###`/`####` | 10 top-level `#` headings matching source `\section`/`\section*` boundaries verbatim |

## Selected Baseline

**Selected candidate:** `pinn_instruction/markdown_conversion/pandoc_conversion/sampling_method_instruction.md` (Candidate B)
**Promoted target:** `pinn_instruction/markdown_conversion/sampling_method.md`
**Selection rationale:** Candidate B achieves higher overall F1 (0.856 vs 0.791), leads all 10 per-section F1 scores, and has perfect heading-fidelity (10/10 vs 1/10). Candidate B also preserves the `align*` equation structure more faithfully (using `\begin{aligned}...\end{aligned}` matching the source `align*` environment, whereas Candidate A flattens to individual `$$` blocks and alters subscript notation from `\rm` to `\text{}`). Both candidates correctly preserve the visible `\authcomment{}` at source line 26 and correctly exclude the `\begin{comment}...\end{comment}` block at lines 130-134.
**Override used:** no
**Promotion action:** `git mv pandoc_conversion/sampling_method_instruction.md sampling_method.md` (replaced existing candidate A at authoritative path)
**Unselected candidate backup:** `/tmp/sampling_method.candidateA.backup.md` (223 lines, 16,817 bytes)

## Excluded Comment Ranges

| Source file | Lines | Status | Evidence |
|-------------|-------|--------|----------|
| `sampling_method_instruction.tex` | 130-134 | Absent from converted body | Grep for unique tokens from `\begin{comment}...\end{comment}` block (`scale_range = (1.0,1.0), i.e., no scaling`) returns 0 in both candidates |

The comment block contains a duplicate Global Scaling itemized list that is also present in the non-commented source lines 117-128. Both candidates correctly contain the Global Scaling content from the non-commented section and do not reproduce the commented-out duplicate.

## Vacuous Policy Checks

| Policy | Source count | Candidate A count | Candidate B count | Status |
|--------|-------------|-------------------|-------------------|--------|
| Tables (`\begin{table\|tabular\|longtable\|tabularx}`) | 0 | 0 | 0 | VACUOUS PASS |
| Citations (`\cite{}`) | 0 | 0 | 0 | VACUOUS PASS |
| Bibitems (`\bibitem{}`) | 0 | 0 | 0 | VACUOUS PASS |
| References (`\ref{}`) | 0 | 0 | 0 | VACUOUS PASS |
| Labels (`\label{}`) | 0 | 0 | 0 | VACUOUS PASS |
| Inactive sections (`*_inactive.tex`) | 0 | N/A | N/A | VACUOUS PASS |

**D-48 evidence:** Both candidates searched for `[@refN]` pandoc citation injection pattern — count: 0 in Candidate A, 0 in Candidate B. No pandoc-3.x noise artifacts detected in either candidate.

Comment blocks and authcomments are NOT vacuous: source has 1 `\begin{comment}` block (lines 130-134) and 1 `\authcomment{}` (line 26). These are handled in `## Excluded Comment Ranges` and Section 1's FIDEL-06 audit respectively.

## Promotion Action

**COMPLETED** — Candidate B promoted via move to `pinn_instruction/markdown_conversion/sampling_method.md`. Existing candidate A backed up to `/tmp/sampling_method.candidateA.backup.md`. Loser A will be archived to `_archive/sampling-method/` in Wave 3.

## Section Audit

### 1. Overview of the Data Generation Pipeline

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| SM-15-02-01 | text | MINOR | sampling_method_instruction.tex:26 | sampling_method.md:2 | Pandoc over-escaped `\*\*enabled\*\*` inside authcomment bold — should render as `**enabled**` | Fixed |
| SM-15-02-02 | text | MINOR | sampling_method_instruction.tex:26,34 | sampling_method.md:2,12 | Pandoc escaped quotes `\"...\"` in authcomment and pipeline prose — should be plain `"` in markdown | Fixed (2 occurrences) |

**Content audit:**
- Heading: `\section*{Overview...}` → `# Overview of the Data Generation Pipeline` — MATCH
- `\authcomment{...}` at source line 26 preserved as bold callout `**[Critical Update: ... virial ratio ... $s^3$ ...]**` at markdown line 2 — MATCH (FIDEL-06)
- Prose paragraphs (lines 28-29) match source — MATCH
- Enumerated list (lines 31-35): 3 items converted to numbered list with bold stage names — MATCH (FIDEL-02)
- Closing sentence "This document details the first two stages" — MATCH
- Source comment `% Hierarchical ICs section inserted here` correctly excluded — MATCH

**Authcomment preservation:** Present at markdown line 2 — content matches source line 26 `\authcomment{Critical Update: ...}` including virial-ratio scaling note and Global Scaling reference — MATCH

---

### 2. Stage 1: Hierarchical Initial Conditions Generation

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| SM-15-02-03 | math | MINOR | sampling_method_instruction.tex:48-50 | sampling_method.md:21 | Kozai-Lidov stability threshold: display math `\[...\]` collapsed into inline `$$` with lead-in text on same line | Fixed — separated lead-in from display block |
| SM-15-02-04 | math | MINOR | sampling_method_instruction.tex:54-60 | sampling_method.md:25-27 | Two separate display equations (`r_inner`/`v_inner` and `r_outer`/`v_outer`) merged into single `$$...$$` block | Fixed — restored two separate display blocks |

**Content audit:**
- Heading: `\section*{Stage 1: Hierarchical Initial Conditions Generation}` → `# Stage 1: Hierarchical Initial Conditions Generation` — MATCH
- Introductory prose (source line 43) — MATCH
- `\texttt{generate\_stable\_hierarchical\_systems}` → `` `generate_stable_hierarchical_systems` `` — MATCH
- 8-item enumerated list converted to numbered list:
  - Item 1 (Mass sampling, source lines 46): inline math preserved — MATCH
  - Item 2 (Hierarchical separation ratio, source lines 47-51): Kozai-Lidov formula fixed (SM-15-02-03) — MATCH
  - Item 3 (Orbital elements, source line 52): inline math — MATCH
  - Item 4 (Radial distances and speeds, source lines 53-60): display math fixed (SM-15-02-04) — MATCH
  - Item 5 (Inclination perturbation, source line 62): inline math — MATCH
  - Item 6 (Position vectors, source lines 64-69): `align*` → `$$\begin{aligned}...\end{aligned}`` — MATCH (FIDEL-01)
  - Item 7 (Velocity vectors, source lines 72-77): `align*` → `$$\begin{aligned}...\end{aligned}`` — MATCH (FIDEL-01)
  - Item 8 (Gaussian perturbation, source line 79): inline math — MATCH
- Closing sentence (source line 82) — MATCH

**Formula checklist:**

| # | Source location | LaTeX form | Markdown location | Markdown form | Status |
|---|-----------------|------------|-------------------|---------------|--------|
| 1 | sampling_method_instruction.tex:64-69 | `\begin{align*} \mathbf{x}_1 &= -\frac{m_2}{m_1+m_2}\,r_{\rm inner}... \end{align*}` | sampling_method.md:31-37 | `$$\begin{aligned} \mathbf{x}_1 &= -\frac{m_2}{m_1+m_2}\,r_{\rm inner}... \end{aligned}$$` | MATCH |
| 2 | sampling_method_instruction.tex:72-77 | `\begin{align*} \mathbf{v}_1 &= \bigl(0,\,-\tfrac{m_2}{m_1+m_2}v_{\rm inner}... \end{align*}` | sampling_method.md:39-45 | `$$\begin{aligned} \mathbf{v}_1 &= \bigl(0,\,-\tfrac{m_2}{m_1+m_2}v_{\rm inner}... \end{aligned}$$` | MATCH |

Both align* blocks faithfully converted to `$$\begin{aligned}...\end{aligned}`` with identical mathematical content. `\rm` subscripts preserved as `\rm` in markdown — MATCH (FIDEL-01)

---

### 3. Stage 2: Enhanced Quasi-Random Sampling

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| — | — | — | — | — | No discrepancies found | — |

**Content audit:**
- Heading: `\section*{Stage 2: Enhanced Quasi-Random Sampling}` → `# Stage 2: Enhanced Quasi-Random Sampling` — MATCH
- Single prose sentence (source lines 85-86): "The foundation of our pipeline..." — MATCH

Note: Section 3 is a 3-line banner (source lines 84-86) with no subsections, math, or lists. Content matches verbatim.

---

### 4. Core Sampling Methodology

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| SM-15-02-05 | math | INFO | sampling_method_instruction.tex:148 | sampling_method.md:106 | `\texorpdfstring{$\epsilon$}{epsilon}` in subsection heading — pandoc renders as `$\epsilon$`, standard behavior | Noted — renders correctly |
| SM-15-02-06 | text | MINOR | sampling_method_instruction.tex:96 | sampling_method.md:66 | Pandoc escaped quotes `\"clumping\"` and `\"voids\"` — should be plain `"` in markdown | Fixed |

**Content audit:**
- Heading: `\section{Core Sampling Methodology}` → `# Core Sampling Methodology` — MATCH
- Introductory prose (source line 88) — MATCH
- Itemized list for particle sampling (source lines 89-93): 3 bullets converted to `-` list items — MATCH (FIDEL-02)
- `\subsection{Low-Discrepancy Engine: Sobol Sequence}` → `## Low-Discrepancy Engine: Sobol Sequence` — MATCH
- Sobol prose (source lines 96-100) — MATCH
- `\subsection{Mapping Sobol Numbers to Physical Coordinates}` → `## Mapping Sobol Numbers to Physical Coordinates` — MATCH
- `\subsubsection*{Direction on the Unit Sphere}` → `### Direction on the Unit Sphere` — MATCH
  - 3-item enumerated list (source lines 106-110) converted to numbered list — MATCH
- `\subsubsection*{Radial Distance and Scaling}` → `### Radial Distance and Scaling` — MATCH
  - Single itemize item (source line 114) converted to `-` bullet — MATCH
- `\subsubsection*{Global Scaling (Optional)}` → `### Global Scaling (Optional)` — MATCH
  - Prose (source lines 117-120) — MATCH
  - Virial ratio impact note — MATCH
- `\subsubsection*{Velocity Sampling}` → `### Velocity Sampling` — MATCH
  - Inline math `$v_i = \Phi^{-1}(...)$` converted to inline `$$...$$` on same line — MATCH
  - Momentum conservation note — MATCH
- Comment block exclusion (source lines 130-134): `\begin{comment}...\end{comment}` content verified absent — grep for `scale_range = (1.0,1.0)` returns 0 — PASS (AUDIT-03, FIDEL-06)

**Comment-block exclusion:** Verified absent — no content from source lines 130-134 found in markdown — PASS

---

### 5. Enhancements to the Sampling Algorithm

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| — | — | — | — | — | No discrepancies found | — |

**Content audit:**
- Heading: `\section{Enhancements to the Sampling Algorithm}` → `# Enhancements to the Sampling Algorithm` — MATCH
- Introductory prose (source line 137) — MATCH
- `\subsection{Sampling Non-Zero Initial Velocities}` → `## Sampling Non-Zero Initial Velocities` — MATCH
  - Prose (source lines 140-141) — MATCH
  - Itemized list (source lines 143-146) converted to `-` bullets — MATCH
- `\subsection{Initial Collision Avoidance: The Role of $\epsilon$}` → `## Initial Collision Avoidance: The Role of $\epsilon$` — MATCH
  - Prose (source lines 149-150) — MATCH
  - `\epsilon` threshold value 0.05 — MATCH
  - Itemized list (source lines 151-154) converted to `-` bullets — MATCH
- `\textbf{Recommended Scale}` → `**Recommended Scale**` — MATCH
  - Prose (source lines 158) — MATCH
- `\textbf{Practical Strategy}` → `**Practical Strategy**` — MATCH
  - Itemized list (source lines 162-166) converted to `-` bullets — MATCH

---

### 6. Stage 3: Pre-Screening of Generated ICs for Short-Term Stability
**Status:** PENDING — Full audit deferred to Wave 2 Task 2 (Plan 02). 4-line banner section (source lines 170-173).

### 7. The Pre-Screening Rationale
**Status:** PENDING — Full audit deferred to Wave 2 Task 2 (Plan 02).

### 8. Pre-Screening Criteria
**Status:** PENDING — Full audit deferred to Wave 2 Task 2 (Plan 02).

### 9. A Coordinated Strategy for Minimum Distance
**Status:** PENDING — Full audit deferred to Wave 2 Task 2 (Plan 02).

### 10. Execution and Final Quality Control
**Status:** PENDING — Full audit deferred to Wave 2 Task 2 (Plan 02).

## Fix Log

| ID | Section | Fix summary |
|----|---------|-------------|
| SM-15-01-BASELINE | N/A | Initial baseline: Candidate B selected and promoted. 10 section audits PENDING for Wave 2. |
| SM-15-02-01 | Section 1 (Overview) | Fixed pandoc over-escaped `\*\*enabled\*\*` to `**enabled**` inside authcomment |
| SM-15-02-02 | Section 1 (Overview) | Fixed 2 occurrences of pandoc escaped quotes `\"...\"` to plain `"` (authcomment + pipeline prose) |
| SM-15-02-03 | Section 2 (Stage 1 Hierarchical) | Separated Kozai-Lidov display math from inline lead-in text; restored `$$...$$` display block |
| SM-15-02-04 | Section 2 (Stage 1 Hierarchical) | Split merged display block into two separate `$$...$$` blocks for radial distances/speeds equations |
| SM-15-02-05 | Section 4 (Core Sampling) | Noted `\texorpdfstring` in subsection heading — renders as `$\epsilon$`, standard pandoc behavior (INFO) |
| SM-15-02-06 | Section 4 (Core Sampling) | Fixed pandoc escaped quotes `\"clumping\"` and `\"voids\"` to plain `"` |

## Source Issues / Notes for Future Reconciliation

(Populated in Plan 03 — see CROSS-01)

## Final Verification

(Populated in Plan 03 — see CLEAN-03)
