# Phase 15: Sampling-Method Verification - Research

**Researched:** 2026-05-05
**Domain:** Markdown conversion verification (LaTeX → Markdown fidelity, monolithic source, two markdown candidates, candidate selection required)
**Confidence:** HIGH (every count/path below verified by live grep / wc / ls in this research session)

## Phase Overview

Phase 15 verifies that one of two existing sampling-method markdown candidates is a one-to-one faithful reproduction of the **monolithic** LaTeX source `pinn_instruction/original_latex/sampling-method/sampling_method_instruction.tex` (241 lines, 18,931 bytes). Unlike Phases 10-14 (whose sources are modularized into per-section `.tex` files), the Phase 15 source has no `sections/` directory — logical sections are defined by `\section` and `\section*` boundaries inside the single `.tex` file. The audit therefore splits on those boundaries.

**What makes Phase 15 different from its peers:**

| Aspect | Phase 13 (most-recent peer) | Phase 14 (immediate predecessor) | Phase 15 (this phase) |
|--------|------------------------------|-----------------------------------|------------------------|
| Candidate count | 1 (CAND-02) | 1 (CAND-02) | **2 (CAND-01)** — selection + diff-score required |
| `_archive/` directory | Skipped (CLEAN-02 N/A) | Skipped (CLEAN-02 N/A) | **Created** (CLEAN-02 in scope) |
| LaTeX source layout | `sections/*.tex` (7 files) | `sections/*.tex` (6 files) | **Monolithic single file** |
| Section enumeration | `\input{sections/...}` order | `\input{sections/...}` order | **`\section` boundaries inside one file** |
| Comment blocks | 0 | (per Phase 14 research) | **1** (`\begin{comment}...\end{comment}` at lines 130-134) |
| `\authcomment{}` | 0 | 0 | **1** (line 26) |
| Citations / bibitems / refs / labels | 0 | (per Phase 14 research) | **0 / 0 / 0 / 0** |
| Tables | 0 | (multiple per Phase 14) | **0** |
| Display math | source has 0 (uses `$$...$$`) | (per Phase 14 research) | **2** (`align*` blocks at 64-69 and 72-77) |
| Phase 13 had a Phase-14 README sibling note | yes | n/a | **Phase 15 stands alone** — its source lives at `original_latex/sampling-method/`, not under any shared parent dir |

**Phase 15's defining characteristics:**
1. **CAND-01 multi-candidate path** — the diff-score methodology established in Phases 10/11/12 is back in play (Phase 13/14 had only one candidate).
2. **Monolithic source** — the audit recipe must define how to slice on `\section`/`\section*` instead of on file boundaries.
3. **One real comment block** to exclude (`AUDIT-03` is non-vacuous for the first time since Phase 12, in this milestone's tail).
4. **One visible `\authcomment` author note** that must appear in the final markdown (per Phase 10 D-06: visible note, not excluded).

**Primary recommendation:** Adopt Phase 13's three-wave plan structure with three substitutions: (a) Wave 1 produces a Phase-10-style **diff-score Candidate Comparison** report instead of a single-candidate Provenance Note (the two candidates are described in `## Source Inventory` below), (b) Wave 2's per-section audit splits on `\section`/`\section*` boundaries inside the single `.tex` file using the verified line ranges below, (c) Wave 3 archives the **losing** candidate to `_archive/sampling-method/` with a provenance README mirroring `_archive/ctl-instruction/README.md`.

<user_constraints>
## User Constraints (from CONTEXT.md)

**No CONTEXT.md exists for Phase 15 yet** (this research is upstream of `/gsd-discuss-phase`). The planner should treat the entire phase scope as Claude's discretion bounded by REQUIREMENTS.md and ROADMAP.md, with the inherited locked decisions from Phases 10/11/12/13 as the baseline.

### Locked Decisions (inherited from prior v1.3 phases)

These are carried-forward decisions that the planner must honor without re-deciding (sourced from 13-CONTEXT.md "Carried Forward" section, which itself carries forward Phase 10/11/12 decisions). Phase 15 inherits ALL of these:

- **From Phase 10 (D-01–D-26):** Audit→fix→verify pattern, severity labels (BLOCKING/MAJOR/MINOR/INFO), per-section pass/fail tables, discrepancy rows with type+severity+source-loc+md-loc+fix-status, formula-by-formula checklists for math-heavy sections (D-14), markdown-only corrections (D-13: LaTeX is ground truth), `Source Issues / Notes for Future Reconciliation` metadata section appended to the authoritative markdown, small section-scoped edits over rewrites (D-20), fix log mapping discrepancy IDs to fixes, lowercase_underscore filename convention, README index update.
- **From Phase 11 (D-27, D-29–D-33):** D-27 strip-injected-citations policy (vacuously satisfied here for source; applied to candidates if injected). D-29 GFM table format (Phase 15 source has 0 tables — vacuous). D-31 `verification_reports/` subdir convention. D-33 active-section scope.
- **From Phase 12 (D-34, D-35, D-38):** Inactive-section absence verification methodology (vacuously satisfied — no `*_inactive.tex`).
- **From Phase 13 (D-47):** Vacuous Policy Checks subsection wording — explicit grep evidence for absence claims, not implicit.

### Claude's Discretion (Phase 15 specific — planner decides)
- Exact diff-score algorithm details (the methodology framework is locked from Phase 10; the specific per-section weighting can be planner-chosen).
- Whether to split Wave 2 audit into 1 task or 2 tasks (Phases 10/11/12/13 split into 2 — recommended).
- Whether to use `git mv` or copy semantics for the unselected candidate's archive move (Phase 10 used `git mv` for archiving — recommended).
- Whether the existing top-level `sampling_method.md` becomes the authoritative path automatically if selected, or if the path is fixed regardless of selection (recommended: target path is fixed at `pinn_instruction/markdown_conversion/sampling_method.md` — this matches Phase 10's "fixed target path" pattern in 10-01-PLAN.md task 2; if the existing file is the loser, it gets moved to `_archive/sampling-method/sampling_method.unselected.md` BEFORE the winner is promoted into its place).
- Discrepancy ID format (recommended: `SM-15-{plan}-{NN}` mirroring Phase 13's `RoF-13-{plan}-{NN}`).

### Deferred Ideas (OUT OF SCOPE — do NOT plan around)
- Reconciling sampling-method with other instruction documents (CTL, data-quality-assessment, pinn-architecture, review-of-framework, stage-strategy-revision). v1.3 preserves source-specific content per CROSS-01.
- Fixing suspected source-level mathematical, factual, or methodological issues in the sampling-method LaTeX. Document in appended Source Issues metadata, do not correct.
- Building shared automated markdown-verification tooling (deferred to v2 per REQUIREMENTS.md AUTO-01/02/03).
- Re-running pandoc on the candidate (REQUIREMENTS.md "Out of Scope" — destroys manual fixes).
- Modifying the LaTeX source (LaTeX is ground truth per inherited D-13).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CAND-01 | Multi-candidate diff-score selects best starting candidate | 2 candidates exist (`markdown_conversion/sampling_method.md` 223 lines, and `markdown_conversion/pandoc_conversion/sampling_method_instruction.md` 198 lines). Wave 1 ranks them per Phase 10 methodology. |
| AUDIT-01 | Section-by-section manual comparison of LaTeX against markdown | Source has **10 `\section`/`\section*` headings** (verified). Wave 2 audits each in source order against the selected candidate. |
| AUDIT-02 | Every discrepancy documented with section location, type, severity | Reuse Phase 13 discrepancy table format: `ID | Type | Severity | Source loc | Markdown loc | Issue | Fix status`. Recommended ID: `SM-15-{plan}-{NN}`. |
| AUDIT-03 | Comparison explicitly excludes `\begin{comment}...\end{comment}` blocks | **NON-VACUOUS** here. Source has **1 comment block at lines 130-134** (verified). The audit must explicitly skip those lines and the report must list the excluded range under `## Excluded Comment Ranges` (Phase 10 pattern). |
| FIDEL-01 | Every mathematical formula appears with accurate notation | Source has 2 display-math `align*` blocks (lines 64-69 and 72-77). Inline `$...$` math throughout. Both must be in the formula checklist. |
| FIDEL-02 | All prose, lists, code blocks, inline formatting match exactly | Standard prose audit. Watch for pandoc artifacts — both candidates have **0 escaped-dash markers, 0 `\[` escapes, 0 grid-table separators, 0 continuation markers, 0 `[@refN]` injections** (verified by grep). Note: candidate A `sampling_method.md` predates the pandoc_conversion/ candidate (March 19 vs March 20) and was likely hand-edited or generated by `convert_latex_to_md.py` co-located in the pandoc_conversion/ directory — its provenance differs and shows in heading depth (see CAND-01 section). |
| FIDEL-03 | All references preserved with correct target identifiers | **VACUOUSLY SATISFIED** (source has 0 `\cite{}`, 0 `\bibitem{}`, 0 `\ref{}`, 0 `\label{}` — verified). Document in Vacuous Policy Checks. |
| FIDEL-04 | All tables verified cell-by-cell | **VACUOUSLY SATISFIED** (source has 0 tables — verified by `grep -c '\\begin{table\|tabular\|longtable\|tabularx}'`). Document in Vacuous Policy Checks. |
| FIDEL-05 | Section hierarchy matches LaTeX source structure exactly | Source has 10 `\section`/`\section*` lines, 5 `\subsection`, 0 `\paragraph` (verified). Canonical map: `\section` / `\section*` → `#`, `\subsection` → `##`. Candidates DIVERGE on this — see "Heading Hierarchy Mismatch" in `## Candidate Selection Methodology`. |
| FIDEL-06 | Commented-out content absent from markdown | Source comment block at lines 130-134 must NOT appear in the markdown. The visible `\authcomment{...}` at line 26 MUST appear (per Phase 10 D-06: visible note). |
| CLEAN-01 | Each source has exactly one authoritative markdown file | Target path: `pinn_instruction/markdown_conversion/sampling_method.md` (the existing path). Whether the file there gets kept or replaced depends on Wave 1's selection. |
| CLEAN-02 | Unselected duplicate markdown files archived to `_archive/` with README | Archive directory: `pinn_instruction/markdown_conversion/_archive/sampling-method/` with provenance `README.md`. Mirror the format used at `_archive/ctl-instruction/README.md` (4-column table: file / original path / score-rank / disposition / reason). |
| CLEAN-03 | Verification report documents selection, discrepancies, fixes, zero-diff | Report at `pinn_instruction/markdown_conversion/verification_reports/sampling_method_verification_report.md`. |
| CROSS-01 | Inter-document inconsistencies preserved in markdown | Append Source Issues metadata section to authoritative markdown after a horizontal rule (Phase 13 pattern). |
| CROSS-02 | 6 phases execute sequentially following same audit pattern | Follow Phase 13 three-wave structure with Phase 10's two-candidate adaptations. |

**Note on traceability:** REQUIREMENTS.md table currently shows CAND-01 mapped to "Phases 10, 11, 12, 15" and CLEAN-02 mapped to "Phases 10, 11, 12, 15" — both confirm Phase 15's CAND-01 / CLEAN-02 are NON-VACUOUS and require the Phase 10/11/12 multi-candidate machinery, NOT the Phase 13/14 single-candidate path.
</phase_requirements>

## Source Inventory

### LaTeX Source (monolithic)

| Path | Lines | Bytes |
|------|-------|-------|
| `<home>/Desktop/3_body_problem/pinn_instruction/original_latex/sampling-method/sampling_method_instruction.tex` | 241 | 18,931 |

**No `sections/` subdirectory.** All content in one file. Verified live in this session.

### `\section` Boundary Map (the audit unit for AUDIT-01)

The 10 logical sections, in source order, are:

| # | Source line | Heading command | Title |
|---|-------------|-----------------|-------|
| 1 | 24 | `\section*` | Overview of the Data Generation Pipeline |
| 2 | 41 | `\section*` | Stage 1: Hierarchical Initial Conditions Generation |
| 3 | 84 | `\section*` | Stage 2: Enhanced Quasi-Random Sampling |
| 4 | 87 | `\section` | Core Sampling Methodology |
| 5 | 136 | `\section` | Enhancements to the Sampling Algorithm |
| 6 | 170 | `\section*` | Stage 3: Pre-Screening of Generated ICs for Short-Term Stability |
| 7 | 174 | `\section` | The Pre-Screening Rationale |
| 8 | 190 | `\section` | Pre-Screening Criteria |
| 9 | 215 | `\section` | A Coordinated Strategy for Minimum Distance |
| 10 | 230 | `\section` | Execution and Final Quality Control |

**`\section` vs `\section*`:** The starred form suppresses numbering but is structurally identical to `\section`. The audit treats both as top-level (`#` in markdown). Candidates may render them differently — see "Heading Hierarchy Mismatch" below.

**Per-section line ranges (source line N to source line of next \section minus 1, ending at line 241):**
1. 24-40 (Overview), 2. 41-83 (Stage 1), 3. 84-86 (Stage 2 banner), 4. 87-135 (Core Sampling), 5. 136-169 (Enhancements), 6. 170-173 (Stage 3 banner), 7. 174-189 (Rationale), 8. 190-214 (Criteria), 9. 215-229 (Min Distance), 10. 230-241 (Execution).

The two banner-like sections (3 at 84-86 and 6 at 170-173) are very short — they introduce a stage that is then broken into subsections that are themselves top-level `\section`s. Watch for this in candidate B's heading flattening.

### Markdown Candidates (two)

| Tag | Path | Lines | Bytes | Modified | Top-level `#` count |
|-----|------|-------|-------|----------|---------------------|
| **A** | `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/sampling_method.md` | 223 | 16,817 | 2026-03-19 22:38 | **1** (single document title at line 3) |
| **B** | `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/pandoc_conversion/sampling_method_instruction.md` | 198 | 16,562 | 2026-03-20 03:32 | **10** (matches the 10 `\section`/`\section*` boundaries verbatim) |

**Co-located conversion script:** `pinn_instruction/markdown_conversion/pandoc_conversion/convert_latex_to_md.py` exists alongside candidate B. It is NOT pandoc — it is a custom Python script. Despite the directory name `pandoc_conversion/`, candidate B is likely produced by this script (or by pandoc with subsequent edits). The planner's Wave 1 should record actual provenance (file mtimes, possible `git log` of either file) rather than assuming "pandoc".

**Pandoc artifact baseline (verified by grep — both candidates show 0 of every confirmed Phase 13 artifact pattern):**

| Pattern | Candidate A | Candidate B |
|---------|-------------|-------------|
| `^\-` escaped-dash list markers | 0 | 0 |
| `\[` escaped prose brackets | 0 | 0 |
| `^\+[-=:]` grid-table separators | 0 | 0 |
| `continued from previous page` / `Continued on next page` | 0 | 0 |
| `[@refN]` pandoc citation injections | 0 | 0 |

**Conclusion:** Neither candidate has the pandoc-3.x noise patterns that dominated Phase 13's Wave 2 work (29 escapes, 23 brackets, 1 longtable continuation in Phase 13). Phase 15 Wave 2 will focus instead on **structure fidelity** (heading hierarchy, AUDIT-03 comment block exclusion, FIDEL-01 align* equations, FIDEL-06 visible authcomment preservation) rather than artifact cleanup.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Markdown candidate diff-scoring | Documentation | CLI/Shell | Mechanical text comparison + human override per Phase 10 D-26 |
| `\section`-boundary slicing of monolithic source | CLI/Shell | — | `grep -n '^\\section'` produces deterministic boundary lines |
| Section-by-section audit | Documentation | CLI/Shell | grep/diff for evidence; manual reading for fidelity judgment |
| Vacuous policy verification | CLI/Shell | — | grep counts (here: tables, citations, refs, labels, bibitems) |
| Comment-block exclusion verification | CLI/Shell | — | grep for `\\begin{comment}` start line + `\\end{comment}` end line; verify candidate has no content from that source range |
| Verification report writing | Documentation | — | Markdown report generation |
| Promotion (winner → authoritative path) | CLI/Shell | git | `git mv` if winner is candidate B; preserve in place if winner is candidate A |
| Loser archival (CLEAN-02) | CLI/Shell | git | `git mv` to `_archive/sampling-method/` plus README write |
| Index update | Documentation | — | Phase 15 row added to `markdown_conversion/README.md` |

**Phase scope:** Documentation tier only. No runtime services, databases, or external APIs.

## Candidate Selection Methodology (CAND-01)

The diff-score algorithm is locked at the framework level (Phase 10 D-26: mechanical scoring + human-override). Phase 15 reuses the same shape:

### Step 1 — Normalize before scoring (per Phase 10 10-01-PLAN.md task 1 "Scoring rules"):
- Normalize whitespace, line wrapping, and harmless markdown escaping.
- Do NOT normalize away: formula changes, missing prose, added prose, heading-level drift, omitted visible `\authcomment{...}` text, or different handling of the comment block at source lines 130-134.

### Step 2 — Compute scores per candidate:
- **Overall score:** F1 of source-tokens-recalled vs candidate-tokens-emitted (Phase 10 used "F1" — see `_archive/ctl-instruction/README.md` rows showing `0.890 F1` and `0.959 F1`).
- **Per-section score:** Same F1, scoped to each of the 10 `\section`-bounded source ranges. Phase 10 produced 8 per-section scores; Phase 15 produces 10.
- **Heading-fidelity score:** Count of `#`-headings in the candidate that match the 10 source `\section`/`\section*` titles in order. **Candidate A (1 heading) will score 1/10 by this metric. Candidate B (10 headings) will score 10/10.** This will likely dominate selection — but the planner must still verify by reading the section body content, since heading absence may indicate a single-heading "document title" pattern with H2 sub-headings inside.

### Step 3 — Heading Hierarchy Mismatch (the structural decision driver):

Candidate A treats the document as a single-titled monograph with one `# ` at line 3 (`# A Unified Pipeline for Generating High-Fidelity Three-Body Initial Conditions` — a TITLE, not a `\section`-equivalent — note this title does NOT appear in the LaTeX source's `\section*` list). The 10 source sections are presumably mapped to `##`/`###` levels inside.

Candidate B has 10 top-level `#` headings exactly matching the 10 `\section`/`\section*` titles in source order. This matches the FIDEL-05 mapping rule (`\section` → `#`).

**Implication for selection:** Candidate B is structurally faithful to FIDEL-05 by default; candidate A requires the entire heading hierarchy to be re-leveled to comply. **Recommendation:** Bias toward candidate B unless its content fidelity (Wave 1 per-section audit sampling) is demonstrably worse on FIDEL-01 (the 2 align* equations) or FIDEL-06 (visible `\authcomment` preservation at source line 26).

### Step 4 — Human override:
Per Phase 10 D-26 (carried forward), the auditor may override the raw score winner if the loser has demonstrably better math, table, reference, or structure fidelity. Document the override and rationale.

### Step 5 — Output: `## Candidate Comparison` report section
Mirror Phase 10's `## CTL Candidate Comparison` format (10-01-PLAN.md task 1):
- Both candidate paths listed.
- Overall score per candidate.
- 10 per-section scores per candidate (matching the 10 `\section` boundaries).
- `Human inspection notes` column for math/table/reference/structure concerns.
- `## Selected Baseline` block with `Selected candidate:`, `Promoted target: pinn_instruction/markdown_conversion/sampling_method.md`, `Selection rationale:`, `Override used: yes/no`.

## Audit Pattern (AUDIT-01..03)

### Section split on `\section` boundaries (Phase 15 specific)

```bash
SRC="pinn_instruction/original_latex/sampling-method/sampling_method_instruction.tex"

# Extract the 10 section boundaries with their line numbers
grep -nE '^\\section\*?\{' "$SRC"

# Compute per-section line ranges (boundary line N to next boundary line - 1)
awk '/^\\section\*?\{/{print NR}' "$SRC"
```

The 10 ranges are tabulated above in `## Source Inventory`. The audit iterates them in source order; each becomes a `### N. <title>` subsection in the Section Audit block of the report.

### Discrepancy taxonomy (Phase 13 inherited)

For each section, the discrepancy table uses these column values:
- **Type:** `Conversion` | `text` | `table` | `structure` | `figure` | `math`
- **Severity:** `BLOCKING` | `MAJOR` | `MINOR` | `INFO`
- **ID format:** `SM-15-{plan}-{NN}` (recommendation; mirrors Phase 13 `RoF-13-{plan}-{NN}`)

### Per-section audit checklist

For each of the 10 sections:
1. **Heading map (FIDEL-05):** `\section` / `\section*` → `#`, `\subsection` → `##`, `\paragraph` → `####`. Verify the candidate's heading at the section's start line.
2. **Prose / lists / code blocks (FIDEL-02):** block-by-block comparison.
3. **Inline math:** verify `$...$` content matches.
4. **Display math (FIDEL-01):** required only for sections covering source lines 64-77 (Section 2 Stage 1 Hierarchical, lines 41-83 — contains both `align*` blocks). Build a 2-row formula checklist.
5. **Comment block exclusion (AUDIT-03 / FIDEL-06):** required only for the section covering source lines 130-134 (Section 4 Core Sampling Methodology, lines 87-135). Verify the candidate has no content from that range.
6. **Visible `\authcomment` preservation (FIDEL-06 inverse):** required only for the section covering source line 26 (Section 1 Overview, lines 24-40). Verify the long author note about virial-ratio scaling appears in the candidate as a callout/note/blockquote.

### Fix log format (inherited)

```
| ID | Section | Fix summary |
|----|---------|-------------|
| SM-15-02-01 | Section 4 (Core Sampling Methodology) | Removed pandoc-injected reproduction of comment-block lines 130-134. |
```

## Fidelity Requirements (FIDEL-01..06)

| Req | What counts as "meaningful difference" | Acceptable formatting variance |
|-----|----------------------------------------|--------------------------------|
| FIDEL-01 | Missing `align*` equation, altered LHS/RHS, dropped or inserted term, wrong subscript/superscript, lost virial-ratio formula | Whitespace inside `$$...$$`, line-wrapping inside math |
| FIDEL-02 | Dropped sentence, added prose, paraphrased phrasing, reordered list items | Whitespace, line wrap, harmless markdown escaping |
| FIDEL-03 | (Vacuous — source has 0 `\cite`/`\bibitem`/`\ref`/`\label`) | n/a |
| FIDEL-04 | (Vacuous — source has 0 tables) | n/a |
| FIDEL-05 | Heading-level drift (e.g., `\section` rendered as `##` instead of `#`), missing heading, reordered sections, extra heading | `\section*` rendered as `#` (acceptable — starred form is just unnumbered) |
| FIDEL-06 | Comment-block content from source lines 130-134 appearing in markdown (BLOCKING); visible `\authcomment{...}` from source line 26 missing from markdown (MAJOR — it's deliberately visible source content) | Authcomment may render as blockquote, callout, italic note, or admonition — any visible form is acceptable |

**FIDEL-06 is two-sided here** — it requires (a) excluded comment content absent AND (b) visible authcomment preserved. Phases 13/14 had a vacuously-empty version of (b); Phase 15 is the first phase since Phase 10 to have a non-zero `\authcomment` count.

## Cleanup Requirements (CLEAN-01..03)

### CLEAN-01 — Single authoritative markdown
**Target path:** `pinn_instruction/markdown_conversion/sampling_method.md`

The path is fixed. After Wave 3:
- If candidate A was selected: leave the file at this path (it was already the target). Apply Wave 2 fixes in place.
- If candidate B was selected: archive the existing candidate A to `_archive/sampling-method/sampling_method.unselected.md`, then `git mv pandoc_conversion/sampling_method_instruction.md sampling_method.md`. Apply Wave 2 fixes either before or after the move (Phase 13 applied fixes before the move; recommended).

### CLEAN-02 — Archive layout for the loser

```
pinn_instruction/markdown_conversion/_archive/sampling-method/
├── README.md                                # provenance + selection rationale
└── <unselected_candidate>.md                # the loser (preserved verbatim)
```

**README.md format** (mirror `_archive/ctl-instruction/README.md` verbatim, substituting paths and scores):

```markdown
# Sampling-Method Candidate Archive

## Candidate provenance

The authoritative sampling-method markdown for Phase 15 is `../../sampling_method.md`.
Selection rationale and final verification details are documented in
`../../verification_reports/sampling_method_verification_report.md`.

| Archived file | Original path | Score/rank | Disposition | Reason |
|---|---|---|---|---|
| `<filename>` | `pinn_instruction/markdown_conversion/<original>` | <F1>/rank N | Archived unselected candidate | <one-sentence reason> |
```

### CLEAN-03 — Verification report

**Path:** `pinn_instruction/markdown_conversion/verification_reports/sampling_method_verification_report.md`

**Required sections (mirror Phase 13 with Phase-10 substitutions):**
1. `# Sampling Method Markdown Verification Report`
2. `## Candidate Comparison` (NOT "Starting Candidate Provenance" — Phase 15 is multi-candidate)
3. `## Selected Baseline`
4. `## Excluded Comment Ranges` (Phase 10 pattern — Phase 13's "Vacuous Policy Checks" is non-vacuous here for AUDIT-03)
5. `## Vacuous Policy Checks` (still useful for the genuinely vacuous items: tables, citations, bibitems, refs, labels, inactive-files)
6. `## Promotion Action`
7. `## Section Audit` with 10 `### N. <title>` subsections
8. `## Fix Log`
9. `## Source Issues / Notes for Future Reconciliation`
10. `## Final Verification` (5-row PASS table mirroring Phase 13 with one row added: "Loser archived (CLEAN-02)")

## Cross-cutting Requirements (CROSS-01..02)

### CROSS-01 — Inter-document inconsistencies preserved
The visible `\authcomment{}` at source line 26 explicitly notes the virial-ratio distortion caused by global scaling. This is source content commenting on the methodology — preserve it verbatim, do NOT reconcile or "fix" it. After Wave 2, the authoritative markdown gets a Source Issues / Notes for Future Reconciliation section appended after a horizontal rule (Phase 13 pattern). If no source-level issues are surfaced during audit beyond what's already in the source body, use Phase 13's no-issues fallback wording.

### CROSS-02 — Sequential phase pattern
Phase 15 follows Phase 13's three-wave structure with the Phase 10 multi-candidate adaptations grafted onto Wave 1.

## Recommended Plan Structure

| Plan | Wave | Objective | Requirement IDs covered | Depends on |
|------|------|-----------|--------------------------|------------|
| **15-01** | 1 | Diff-score the 2 candidates, document selection, build verification report skeleton with the 10 PENDING `### ` audit stubs, record excluded comment ranges, record vacuous policy checks, promote the selected baseline to the fixed target path (preserving the loser temporarily; archive happens in 15-03) | CAND-01, AUDIT-03, FIDEL-03, FIDEL-04, FIDEL-06 (vacuous portion), CLEAN-01 (initial promotion) | — |
| **15-02** | 2 | Section-by-section audit of the 10 `\section`-bounded sections; apply markdown-only fixes section-scoped per D-20; populate the 10 audit subsections; handle the FIDEL-01 align* checklist for Section 2 (Stage 1) and the FIDEL-06 authcomment-visible check for Section 1 (Overview); split into 2 tasks (sections 1-5 and 6-10) | AUDIT-01, AUDIT-02, FIDEL-01, FIDEL-02, FIDEL-05, FIDEL-06 (visible authcomment + comment-block-exclusion verification) | 15-01 |
| **15-03** | 3 | Archive the unselected candidate to `_archive/sampling-method/` with provenance README, append Source Issues metadata to authoritative markdown, finalize the verification report (Promotion Action: COMPLETED; Final Verification table populated; Source Issues finalized), update `markdown_conversion/README.md` index with Phase 15 row | CLEAN-01 (final), CLEAN-02, CLEAN-03, CROSS-01, CROSS-02 | 15-02 |

**3 plans, 4 tasks total** (15-01 has 2-3 tasks, 15-02 has 2 tasks, 15-03 has 1 task). Mirrors Phase 13's plan-and-task counts.

**Why 3 plans not 2:** muscle memory consistency with Phases 10/11/12/13 (Phase 13 D-41 explicitly chose 3 over 2). Phase 15's CAND-01 + CLEAN-02 work makes Wave 1 and Wave 3 each substantial enough to justify their own plans.

## Validation Architecture

> Per `.planning/config.json` and the inherited Phase 13 pattern, treat `workflow.nyquist_validation` as enabled. This is a documentation verification phase — there is no test framework to invoke; validation is grep evidence + human inspection.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None — documentation verification phase |
| Config file | None |
| Quick run command | `grep -c "^### " pinn_instruction/markdown_conversion/verification_reports/sampling_method_verification_report.md` |
| Full suite command | `grep -nE "CAND-01\|AUDIT-01\|FIDEL-01\|CLEAN-01\|CLEAN-02\|CROSS-01" .planning/phases/15-sampling-method-verification/*-PLAN.md` |
| Estimated runtime | < 5 seconds |

### Phase Requirements → Verification Map

| Req ID | Behavior | Verification Method | Wave |
|--------|----------|---------------------|------|
| CAND-01 | 2-candidate diff-score selects best | `## Candidate Comparison` block has both candidate paths, overall scores, 10 per-section scores, `Selected candidate:` line | 1 |
| AUDIT-01 | Section-by-section comparison, all 10 sections | `grep -c "^### " <report>` returns at least 10 | 2 |
| AUDIT-02 | Discrepancy table per section | Discrepancy rows with ID/Type/Severity/Source loc/MD loc/Issue/Fix status columns | 2 |
| AUDIT-03 | Comment block at source 130-134 excluded | `## Excluded Comment Ranges` lists `sampling_method_instruction.tex:130-134` with status `Absent from converted body`; grep candidate for content from those source lines returns 0 | 1 (record), 2 (verify) |
| FIDEL-01 | 2 align* blocks present in markdown | Section 2 (Stage 1) audit subsection has 2-row formula checklist with MATCH for both | 2 |
| FIDEL-02 | Prose / lists match exactly | Per-section content audit | 2 |
| FIDEL-03 | (Vacuous) | Vacuous Policy Checks: 0 `\cite`/`\bibitem`/`\ref`/`\label` | 1 |
| FIDEL-04 | (Vacuous) | Vacuous Policy Checks: 0 tables | 1 |
| FIDEL-05 | Heading hierarchy matches | Section Audit subsections confirm `\section`/`\section*` → `#` mapping; 10 `#` headings in authoritative md | 2 |
| FIDEL-06 | Visible authcomment preserved (line 26); comment block excluded (lines 130-134) | Section 1 audit subsection cites the markdown line where the authcomment text appears as a callout/note; Section 4 audit verifies absence of comment-block content | 2 |
| CLEAN-01 | Single authoritative markdown at fixed target | `test -f pinn_instruction/markdown_conversion/sampling_method.md` succeeds | 1 + 3 |
| CLEAN-02 | Loser archived with README | `test -f pinn_instruction/markdown_conversion/_archive/sampling-method/README.md` AND `_archive/sampling-method/<loser>.md` exists | 3 |
| CLEAN-03 | Report has all 10 required sections | `grep -c "^## " <report>` returns at least 9 (Phase 13's 7 + `Excluded Comment Ranges` + `Selected Baseline`) | 3 |
| CROSS-01 | Source Issues appended to authoritative markdown | Last 30 lines of `sampling_method.md` contain `^---$` and `^## Source Issues` | 3 |
| CROSS-02 | 3-wave pattern executed | 3 PLAN files (15-01, 15-02, 15-03) and 3 SUMMARY files exist | All |

### Sampling Rate
- **Per task commit:** Auditor reviews task output before commit; report's grep checks must pass.
- **Per wave merge:** Full wave review before proceeding (10 PENDING → PASS conversions in Wave 2).
- **Phase gate:** Zero PENDING in report, all 10 audits PASS, Excluded Comment Ranges populated, Vacuous Policy Checks PASS, archive README exists, index updated.

### Wave 0 Gaps
- [ ] None — documentation verification has no test infrastructure to set up.

## Files To Be Created/Modified

| Path | Action | Wave | Authority |
|------|--------|------|-----------|
| `<home>/Desktop/3_body_problem/.planning/phases/15-sampling-method-verification/15-01-PLAN.md` | CREATE (planner output) | pre-Wave 1 | planner |
| `<home>/Desktop/3_body_problem/.planning/phases/15-sampling-method-verification/15-02-PLAN.md` | CREATE (planner output) | pre-Wave 2 | planner |
| `<home>/Desktop/3_body_problem/.planning/phases/15-sampling-method-verification/15-03-PLAN.md` | CREATE (planner output) | pre-Wave 3 | planner |
| `<home>/Desktop/3_body_problem/.planning/phases/15-sampling-method-verification/15-01-SUMMARY.md` | CREATE | end of Wave 1 | executor |
| `<home>/Desktop/3_body_problem/.planning/phases/15-sampling-method-verification/15-02-SUMMARY.md` | CREATE | end of Wave 2 | executor |
| `<home>/Desktop/3_body_problem/.planning/phases/15-sampling-method-verification/15-03-SUMMARY.md` | CREATE | end of Wave 3 | executor |
| `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/verification_reports/sampling_method_verification_report.md` | CREATE (skeleton W1, populate W2, finalize W3) | 1, 2, 3 | CLEAN-03 |
| `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/sampling_method.md` | MODIFY (in place if candidate A wins) OR CREATED via `git mv` (if candidate B wins; the existing file goes to archive first) | 1, 2 (audit fixes), 3 (Source Issues append) | CLEAN-01 |
| `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/pandoc_conversion/sampling_method_instruction.md` | MOVED to `_archive/sampling-method/` if it loses, OR moved to top-level `sampling_method.md` if it wins | 3 (or 1 if promoted early) | CLEAN-01/CLEAN-02 |
| `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/_archive/sampling-method/` | CREATE directory | 3 | CLEAN-02 |
| `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/_archive/sampling-method/README.md` | CREATE provenance README | 3 | CLEAN-02 |
| `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/_archive/sampling-method/<loser>.md` | MOVED via `git mv` from original location | 3 | CLEAN-02 |
| `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/README.md` | MODIFY (append Phase 15 row to flat 4-column index after Phase 13 row) | 3 | inherited D-45/D-46 |

**No files modified:** Any LaTeX source under `pinn_instruction/original_latex/` (REQUIREMENTS.md "Out of Scope"). Phase 10/11/12/13 rows in `markdown_conversion/README.md` (D-46 inherited).

**No `_archive/sampling-method/` README/file content beyond the loser:** the winner stays at `sampling_method.md`, not in archive.

## Open Questions / Risks

1. **Which candidate wins?** Cannot pre-decide — Wave 1 must run the diff-score and per-section audit. Heading-fidelity strongly favors candidate B (10/10 vs 1/10), but candidate A may have superior content fidelity if its `##`/`###` sub-hierarchy preserves the source structure under a single document title. The planner should NOT lock a winner in CONTEXT.md; let Wave 1 decide.

2. **Candidate B's true provenance.** The directory `pandoc_conversion/` contains `convert_latex_to_md.py` (a custom Python script), not pandoc output per se. The planner should record actual conversion-tool provenance in the Wave 1 Candidate Comparison section based on `git log` of either candidate, NOT assume "pandoc". Phase 13's research made this same assumption-vs-evidence distinction.

3. **Single-document-title pattern in candidate A.** Candidate A's `# A Unified Pipeline for Generating High-Fidelity Three-Body Initial Conditions` at line 3 is a TITLE that does not exist in the LaTeX source's `\section*` list. If candidate A wins, that title either needs to be (a) demoted to a non-heading preamble, (b) removed entirely, or (c) explicitly documented as an additive author preamble (which would violate FIDEL-02 "no added content"). Most likely outcome: the planner specifies in CONTEXT.md that candidate A's title-line gets demoted/removed during Wave 2 if candidate A is selected, with the change recorded as an `SM-15-02-NN` discrepancy.

4. **Authcomment rendering in candidates.** Wave 1 should sample both candidates' rendering of the source-line-26 `\authcomment{...}` (a long sentence about virial-ratio scaling) to inform the selection. If neither preserves it, that's a MAJOR FIDEL-06 issue regardless of winner — Wave 2 must restore it.

5. **Comment block (lines 130-134) treatment in candidates.** Wave 1 should grep both candidates for any tokens unique to lines 130-134 of source (the `\begin{comment}...\end{comment}` body) to detect leakage. If either candidate accidentally rendered the commented content, that's a BLOCKING FIDEL-06 issue.

6. **Stale `convert_latex_to_md.py`.** The pandoc_conversion/ directory contains a Python script. Phase 15 does NOT touch this script (REQUIREMENTS.md "Out of Scope" forbids re-conversion). Whether to leave it in `pandoc_conversion/`, move it to a tools directory, or delete it is OUT OF SCOPE for this phase — flag for housekeeping but do not action.

7. **Wave 2 task split.** Recommendation: split sections 1-5 / 6-10 (mirrors Phase 13). Section 2 is the largest by line count (43 source lines, 41-83) and contains both align* equations — anchor it in task 1. Section 6 is a 4-line banner — combine with sections 7-10 in task 2.

## Sources

### Primary (HIGH confidence — verified live in this session)
- `<home>/Desktop/3_body_problem/pinn_instruction/original_latex/sampling-method/sampling_method_instruction.tex` — 241 lines, 18,931 bytes; 10 `\section`/`\section*` boundaries at the lines tabulated above; 1 `\begin{comment}` at line 130, 1 `\end{comment}` at line 134; 1 `\authcomment{...}` at line 26; 0 `\cite`/`\bibitem`/`\ref`/`\label`; 0 tables; 2 display-math `align*` blocks at lines 64-69 and 72-77; 5 `\subsection`; 0 `\paragraph`.
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/sampling_method.md` (candidate A) — 223 lines, 16,817 bytes, mtime 2026-03-19; 1 top-level `#` heading.
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/pandoc_conversion/sampling_method_instruction.md` (candidate B) — 198 lines, 16,562 bytes, mtime 2026-03-20; 10 top-level `#` headings matching source order verbatim.
- Both candidates: 0 `^\-`, 0 `\[`, 0 `+---`, 0 continuation markers, 0 `[@refN]`.
- `_archive/ctl-instruction/README.md` — provenance README template.
- `_archive/` directory — confirmed pattern is `_archive/<phase-slug>/README.md + <unselected>.md`.
- `markdown_conversion/README.md` — flat 4-column index; current rows for Phases 10/11/12/13.

### Secondary (HIGH confidence — derived from prior phase artifacts)
- `.planning/phases/13-review-of-framework-verification/13-RESEARCH.md` — Phase 13 audit pattern, vacuous policy checks pattern (D-47), discrepancy ID format, three-wave plan structure, pitfall list.
- `.planning/phases/13-review-of-framework-verification/13-01-PLAN.md` / `13-02-PLAN.md` / `13-03-PLAN.md` — wave-by-wave task breakdowns.
- `.planning/phases/13-review-of-framework-verification/13-CONTEXT.md` — D-39 through D-49 locked decisions; D-49 prerequisite-gate pattern.
- `.planning/phases/13-review-of-framework-verification/VERIFICATION.md` — verdict/dimension structure for the eventual Phase 15 verification.
- `.planning/phases/10-ctl-instruction-verification/10-RESEARCH.md` and `10-01-PLAN.md` — diff-score scoring rules, heading-by-heading audit pattern, archive-on-promotion rule.
- `.planning/phases/10-ctl-instruction-verification/10-VALIDATION.md` — Phase 10 validation strategy template.
- `.planning/REQUIREMENTS.md` (lines 86, 99) — explicitly maps CAND-01 and CLEAN-02 to Phase 15.
- `.planning/ROADMAP.md` (lines 198-209) — Phase 15 success criteria.
- `.planning/STATE.md` (line 78) — Phase 15 row in v1.3 phase summary table: "monolithic source (no sections/ dir)".

### Tertiary (LOW — inferred, must verify in Wave 1)
- Candidate B's actual conversion provenance (pandoc vs `convert_latex_to_md.py` vs hand-edit) — needs `git log --follow` in Wave 1.

## RESEARCH COMPLETE

Phase 15 mirrors Phase 13's three-wave verification structure but reactivates Phase 10's two-candidate diff-score and `_archive/` machinery; the source's monolithic layout requires `\section`-boundary slicing across 10 logical sections (lines tabulated above), with one comment block (130-134) to exclude and one visible `\authcomment` (line 26) to preserve; both candidates are pandoc-artifact-clean, so Wave 2 work centers on heading hierarchy and FIDEL-01/06 fidelity rather than artifact cleanup.

---

**Files referenced in this research (absolute paths):**
- `<home>/Desktop/3_body_problem/pinn_instruction/original_latex/sampling-method/sampling_method_instruction.tex`
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/sampling_method.md`
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/pandoc_conversion/sampling_method_instruction.md`
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/pandoc_conversion/convert_latex_to_md.py`
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/_archive/ctl-instruction/README.md`
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/README.md`
- `<home>/Desktop/3_body_problem/.planning/REQUIREMENTS.md`
- `<home>/Desktop/3_body_problem/.planning/ROADMAP.md`
- `<home>/Desktop/3_body_problem/.planning/STATE.md`
- `<home>/Desktop/3_body_problem/.planning/phases/13-review-of-framework-verification/{13-RESEARCH.md, 13-CONTEXT.md, 13-01-PLAN.md, 13-02-PLAN.md, 13-03-PLAN.md, VERIFICATION.md}`
- `<home>/Desktop/3_body_problem/.planning/phases/10-ctl-instruction-verification/{10-RESEARCH.md, 10-VALIDATION.md, 10-01-PLAN.md}`
