# Sampling Method Markdown Verification Report

**Phase:** 15 | **Plan:** 01 | **Wave:** 1
**Source:** `pinn_instruction/original_latex/sampling-method/sampling_method_instruction.tex` (241 lines, 18,931 bytes)
**Date:** 2026-05-06

## Candidate Comparison

| Metric | Candidate A | Candidate B (winner) |
|--------|-------------|----------------------|
| Path | `pinn_instruction/markdown_conversion/sampling_method.md` | `pinn_instruction/markdown_conversion/pandoc_conversion/sampling_method_instruction.md` |
| Lines | 223 | 198 |
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
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02). Key checks: FIDEL-06 authcomment preservation (source line 26 — virial-ratio scaling note).

### 2. Stage 1: Hierarchical Initial Conditions Generation
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02). Key checks: FIDEL-01 align* blocks (source lines 64-69, 72-77 — position and velocity vector equations).

### 3. Stage 2: Enhanced Quasi-Random Sampling
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02). 3-line banner section (source lines 84-86).

### 4. Core Sampling Methodology
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02). Key checks: AUDIT-03 comment block exclusion (source lines 130-134).

### 5. Enhancements to the Sampling Algorithm
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02).

### 6. Stage 3: Pre-Screening of Generated ICs for Short-Term Stability
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02). 4-line banner section (source lines 170-173).

### 7. The Pre-Screening Rationale
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02).

### 8. Pre-Screening Criteria
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02).

### 9. A Coordinated Strategy for Minimum Distance
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02).

### 10. Execution and Final Quality Control
**Status:** PENDING — Full audit deferred to Wave 2 (Plan 02).

## Fix Log

| ID | Section | Fix summary |
|----|---------|-------------|
| SM-15-01-BASELINE | N/A | Initial baseline: Candidate B selected and promoted. 10 section audits PENDING for Wave 2. |

## Source Issues / Notes for Future Reconciliation

(Populated in Plan 03 — see CROSS-01)

## Final Verification

(Populated in Plan 03 — see CLEAN-03)
