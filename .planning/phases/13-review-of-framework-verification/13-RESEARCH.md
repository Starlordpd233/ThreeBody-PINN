# Phase 13: Review-of-Framework Verification - Research

**Researched:** 2026-05-05
**Domain:** Markdown conversion verification (LaTeX → Markdown fidelity, single pandoc candidate, sub-document source)
**Confidence:** HIGH

## Summary

Phase 13 audits a single pandoc-converted markdown
(`pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md`,
533 lines) against 7 active LaTeX section files under
`pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/`,
fixes markdown-only conversion artifacts, and promotes the corrected file to
`pinn_instruction/markdown_conversion/review_of_framework.md` as the authoritative
v1.3 markdown for this sub-document.

This is the simplest v1.3 phase by structural complexity:

- **No candidate selection** — CAND-02 applies (single pandoc file, no diff-scoring).
- **No `_archive/` directory** — CLEAN-02 N/A (no losing candidates).
- **Vacuous policy load** — verified by direct grep of the 7 source files: 0 `\begin{comment}`
  blocks, 0 `\authcomment{}` author notes, 0 `\cite{}` markers, 0 `\bibitem` entries,
  0 inactive `*_inactive.tex` files. AUDIT-03 / FIDEL-06 are vacuously satisfied at
  the source side.
- **Confirmed pandoc artifacts in candidate** that will need fixing:
  29 `\-` escaped-dash list markers, 23 `\[...\]` escaped square-bracket prose
  (e.g., `\[-1, 1\]`), 1 longtable pagination duplicate-header artifact in the
  input-vector specification table, and pandoc grid-table format (`+----+`) for
  the same table.

The phase mirrors Phases 10/11/12's three-wave audit→fix→verify→report pattern,
adapted per CONTEXT.md decisions D-39–D-48. The math-heavy sections
(`foundational_physical_metrics.tex` 129 lines, `multi_component_loss_framework.tex`
116 lines) require formula-by-formula checklists per the inherited D-14 policy.

**Primary recommendation:** Follow the Phase 12 three-wave plan structure with a
single-candidate adaptation in Wave 1 (provenance note instead of ranking report),
no archive step in Wave 3, and an explicit "Vacuous Policy Checks" subsection per D-47.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Single-Candidate Baseline (Phase 13 specific — CAND-02)
- **D-39:** Use `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md`
  as the starting baseline directly. CAND-02 applies — no diff-score ranking against
  other candidates is needed because no other candidates exist.
- **D-40:** No `_archive/` directory is created for Phase 13. CLEAN-02 does not apply
  because there are no losing candidates to archive. The verification report explicitly
  notes "Single pandoc candidate; CLEAN-02 N/A" so future readers do not look for missing
  archive contents.
- **D-41:** Plan structure mirrors Phases 10–12 (3 plans): P1 candidate validation +
  report skeleton (provenance note in lieu of ranking), P2 section-by-section audit + fixes,
  P3 promotion + index update + final verification. Decision rationale: muscle memory from
  prior phases outweighs the modest savings of collapsing to 2 plans, and a separate
  "validation + report skeleton" plan keeps the provenance note auditable.
- **D-42:** P1 produces a "Starting Candidate Provenance" note (not a ranking report)
  recording: source file path, file size, line count, conversion tool (pandoc), date observed,
  and confirmation that CAND-02 applies.

#### Authoritative Filename and Location
- **D-43:** Authoritative filename: `pinn_instruction/markdown_conversion/review_of_framework.md`
  (lowercase with underscores, matches the source subdirectory name `review_of_framework/`).
  Aligns with the lowercase_underscore convention from D-23/D-30/D-36 and creates filename
  symmetry with the source dir structure.
- **D-44:** Verification report filename:
  `pinn_instruction/markdown_conversion/verification_reports/review_of_framework_verification_report.md`
  (matches the established `verification_reports/` location from D-31).

#### Sub-Document Index Handling (Phase 13 specific)
- **D-45:** `pinn_instruction/markdown_conversion/README.md` uses a flat index (one row
  per phase). Phase 13 row: title "Review of Framework", links to `review_of_framework.md`
  and the verification report. The row's metadata column notes "LaTeX parent dir:
  `review-of-framework/` (shared with Phase 14: stage-strategy-revision)" so readers
  see the source grouping without nested README structure.
- **D-46:** Do NOT create a grouped/nested section in the README for Phase 13+14. The
  flat index is preferred for symmetry with Phases 10–12 rows and to keep the index
  readable as Phases 14–15 are added.

#### Vacuous Policy Verification (Phase 13 specific)
- **D-47:** The verification report includes an explicit "Vacuous Policy Checks" subsection
  that confirms by inspection:
  - 0 `\begin{comment}...\end{comment}` blocks in the 7 active source sections
    (D-05/D-09 vacuously satisfied).
  - 0 `\authcomment{}` author notes (D-06/D-07 vacuously satisfied).
  - 0 inactive section files (D-34/D-35/D-38 vacuously satisfied — no `*_inactive.tex` exist).
  - 0 `\cite{}` commands and 0 `\bibitem` entries in the 7 active sources
    (D-27/D-28/D-37 vacuously satisfied — no bibliography file imported).
- **D-48:** If the pandoc candidate is found to inject `[@refN]` or other citation-like
  artifacts not present in the source, treat them as conversion fidelity issues per D-27's
  strip-policy and remove them. Document the count and locations in the verification report.

#### Phase Ordering and Phase 12 Status
- **D-49:** Phase 12 execution is in progress (12-03 plan not yet complete) at the time
  of Phase 13 context gathering. Following the same precedent as Phase 10's acknowledgment
  of incomplete Phase 9, Phase 13 context gathering and planning may proceed, but Phase 13
  EXECUTION should treat Phase 12 final verification as the prerequisite gate per ROADMAP
  dependency ordering.

#### Carried Forward Decisions (will not re-decide)
- **From Phase 10 (D-01–D-26):** Audit→fix→verify pattern, severity labels
  (BLOCKING/MAJOR/MINOR/INFO), per-section pass/fail tables, discrepancy rows with
  type+severity+source-loc+md-loc+fix-status, formula-by-formula checklists for math-heavy
  sections, markdown-only corrections, ground-truth status of LaTeX source, `Source Issues /
  Notes for Future Reconciliation` metadata section appended to the authoritative markdown,
  small section-scoped edits over rewrites, fix log mapping discrepancy IDs to fixes,
  lowercase_underscore filename convention, README index update.
- **From Phase 11 (D-27, D-29–D-33):** D-27 strip-injected-citations policy (vacuously
  satisfied for source; applied to candidate if injected). D-29 GFM table format (applies
  if any HTML tables found in candidate — confirmed candidate uses pandoc grid tables,
  see Architecture Patterns section). D-31 `verification_reports/` subdir convention.
  D-33 audit scope is active sections only (vacuously: no inactive sections to exclude here).
- **From Phase 12 (D-34, D-35, D-38):** Inactive-section absence verification methodology
  (vacuously satisfied — no inactive sections in source).

### Claude's Discretion
- Exact wording of the "Vacuous Policy Checks" subsection within the verification report.
- Exact format of the "Starting Candidate Provenance" note in P1 output.
- Exact text of the parent-dir metadata column entry in the README index row.
- Exact discrepancy ID format, as long as IDs remain stable and map from audit table to
  fix log (consistent with D-12).
- Whether to surface line-count or byte-count comparisons in the audit (either is acceptable
  evidence).

### Deferred Ideas (OUT OF SCOPE)
- Reconciling review-of-framework with other instruction documents (CTL, sampling-method,
  data-quality-assessment, pinn-architecture, stage-strategy-revision). v1.3 preserves
  source-specific content; cross-document reconciliation is deferred to a separate future task.
- Auditing the sibling `stage_strat_revision/` sub-document — that is explicitly Phase 14's
  scope, not Phase 13.
- Fixing suspected source-level mathematical, factual, or methodological issues in
  review-of-framework. Phase 13 documents these in the appended `Source Issues / Notes for
  Future Reconciliation` section per D-17/D-18 but does not correct them.
- Building shared automated markdown-verification tooling for all 6 documents. Deferred
  to v2 per REQUIREMENTS.md AUTO-01/02/03.
- Producing a unified parent-doc README under
  `pinn_instruction/original_latex/review-of-framework/` that describes the relationship
  between the two sub-documents. Out of scope for v1.3 — markdown_conversion/README.md is
  the discoverability layer.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CAND-02 | Single-candidate sources skip selection and use pandoc candidate directly | One file at `pandoc_conversion/review_of_ctl-pinn_framework.md` (533 lines) — no other candidates exist. P1 emits a "Starting Candidate Provenance" note (D-42) instead of a ranking report. |
| AUDIT-01 | Section-by-section manual comparison of LaTeX against markdown | 7 active sections imported in known order from `review_of_framework.tex`. Wave 2 audits each in source order; report has 7 audit subsections. |
| AUDIT-02 | Every discrepancy documented with section location, type, severity | Reuse Phase 10/11/12 discrepancy table format (ID, type, severity, source-loc, md-loc, issue, fix-status). |
| AUDIT-03 | Comparison explicitly excludes `\begin{comment}...\end{comment}` blocks | Vacuously satisfied — 0 comment blocks in source (verified by grep). Document in "Vacuous Policy Checks" per D-47. |
| FIDEL-01 | Every mathematical formula appears with accurate notation | `foundational_physical_metrics.tex` (129 lines, ~6 display math: angular momentum sum, characteristic scales align, L_max product, Lyapunov exponent average, Lyapunov time, global scale align) and `multi_component_loss_framework.tex` (116 lines, ~3 display math: data loss L1, physics residual fi(t'), Hamiltonian) require formula-by-formula checklists per D-14. |
| FIDEL-02 | All prose, lists, code blocks, inline formatting match exactly | Standard Phase 10/11/12 prose audit. Special attention to candidate's 29 `\-` escaped-dash list markers and 23 `\[...\]` escaped prose brackets — both are pandoc artifacts, not faithful conversions. |
| FIDEL-03 | All references preserved with correct target identifiers | Vacuously satisfied — 0 `\cite{}`, 0 `\bibitem`, 0 `\ref` cross-references in source (verified by grep). Document in Vacuous Policy Checks per D-47. |
| FIDEL-04 | All tables verified cell-by-cell | One major table in source: 13-row "Definitive Input Vector Specification" longtable in `data_scaling_normalization.tex`. Candidate renders it as pandoc grid table with a duplicate header artifact (lines 199-204). One smaller "Consolidated Hyperparameter Schedule" table in `conclusion_and_recommendations.tex` (rendered as pandoc multiline table). Both require cell-by-cell verification per FIDEL-04 and possible GFM reformat per inherited D-29. |
| FIDEL-05 | Section hierarchy matches LaTeX source structure exactly | Confirmed candidate has 7 top-level `# ` headings matching the 7 active imports. Subsection (`##`) and paragraph (`####`) levels preserved. Wave 2 verifies subsection-by-subsection. |
| FIDEL-06 | Commented-out content absent from markdown | Vacuously satisfied — no comment blocks or inactive files in source. Document in Vacuous Policy Checks per D-47. |
| CLEAN-01 | Each source has exactly one authoritative markdown file | Target: `pinn_instruction/markdown_conversion/review_of_framework.md` per D-43. Wave 3 promotes the corrected candidate to this path. |
| CLEAN-03 | Verification report documents selection, discrepancies, fixes, zero-diff | Target: `pinn_instruction/markdown_conversion/verification_reports/review_of_framework_verification_report.md` per D-44. Includes Vacuous Policy Checks subsection per D-47. |
| CROSS-01 | Inter-document inconsistencies preserved in markdown | Source-level issues documented in appended metadata section, not corrected (D-17/D-18 inherited). The candidate's body discusses inconsistencies WITHIN the source documents — this discussion content is preserved as-is. |
| CROSS-02 | 6 phases execute sequentially following same audit pattern | Phase 13 follows the Phase 12 three-wave pattern with single-candidate adaptations (D-41). |

**N/A for Phase 13:** CAND-01 (no multi-candidate selection), CLEAN-02 (no archive),
inactive-section-exclusion (D-34/D-38) variants from Phase 12 (no inactive files).
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Markdown file comparison | Documentation | — | Pure file-system operations, no runtime components |
| Section-by-section audit | Documentation | CLI/Shell | grep/diff for evidence; manual reading for fidelity judgment |
| Vacuous policy verification | CLI/Shell | — | grep counts for `\begin{comment}`, `\authcomment`, `\cite`, `\bibitem`, `*_inactive.tex` |
| Pandoc artifact detection | CLI/Shell | — | grep patterns for `^\-`, `\\[`, longtable header duplication, grid-table syntax |
| Verification report writing | Documentation | — | Markdown report generation, file creation |
| Promotion (candidate → authoritative) | CLI/Shell | git | `git mv` (or copy) from `pandoc_conversion/` to top-level `markdown_conversion/` |
| Index update | Documentation | — | Phase 13 row added to `README.md` per D-45 |

**This phase is purely documentation tier.** No API, browser, database, or service
dependencies. All work is file-system operations on markdown and LaTeX files.

## Standard Stack

### Core
| Tool | Version (verified locally) | Purpose | Why Standard |
|------|----------------------------|---------|--------------|
| git | 2.50.1 | Promotion (`git mv`), commits per phase plan | Phase 10/11/12 established git-mv pattern; D-45 README update needs git tracking |
| grep / ugrep | 7.5.0 | Source vacuous-policy verification, candidate artifact detection | D-47 explicit vacuous checks; pandoc artifact counts |
| wc | (BSD wc) | Line/byte count for provenance note | D-42 records line count and file size |
| diff | Apple diff (BSD) | Optional side-by-side line comparison during audit | Manual evidence-gathering tool, not authoritative |

### Supporting
| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| pandoc | 3.7.0.2 | **Reference only** — for understanding likely conversion behaviors | NOT re-run; REQUIREMENTS.md "Out of Scope" forbids pandoc re-conversion ("destroys manual corrections"). Useful for reasoning about why a particular artifact appears. |
| head / tail | (BSD) | File segment inspection | Sampling specific sections during audit |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual section diff | Custom Python markdown-vs-LaTeX comparison script | Phase 10 established human-driven audit as the v1.3 method; AUTO-01/02/03 (automation) explicitly deferred to v2. |
| `wc -l` for line count | `awk 'END{print NR}'` | wc is universally available and matches Phase 10/11/12 evidence patterns. |
| Re-running pandoc to regenerate candidate | Edit-in-place candidate | Forbidden by REQUIREMENTS.md "Out of Scope" — would discard the v1.3 verification work. |

**Installation:** All tools verified available at the listed versions. No
package installation required.

**Version verification (verified 2026-05-05 in this session):**
```
$ command -v pandoc git grep wc diff
/opt/homebrew/bin/pandoc        # pandoc 3.7.0.2
/opt/homebrew/bin/git           # git version 2.50.1
ugrep                           # ugrep 7.5.0 aarch64-apple-darwin23.6.0
/usr/bin/wc                     # BSD wc (no --version)
diff                            # Apple diff (FreeBSD-derived)
```

[VERIFIED: local shell invocations 2026-05-05]

## Architecture Patterns

### System Architecture Diagram

```
                          Phase 13 Verification Flow
                          ==========================

Wave 1 (Plan 13-01): Candidate Validation + Report Skeleton
+--------------------------------------------------------------+
|  pandoc_conversion/review_of_ctl-pinn_framework.md (533 lines)|
|         (single pandoc candidate — D-39)                     |
|                          |                                   |
|                          v                                   |
|  Starting Candidate Provenance Note (D-42)                   |
|  - source path, file size, line count                        |
|  - conversion tool (pandoc 3.7.0.2)                          |
|  - date observed                                              |
|  - "CAND-02 applies — single candidate, no ranking"          |
|                          |                                   |
|                          v                                   |
|  Vacuous Policy Checks (D-47) — confirm BY GREP:             |
|  - 0 \begin{comment} in source     -> AUDIT-03 / FIDEL-06    |
|  - 0 \authcomment{} in source                                |
|  - 0 *_inactive.tex files                                    |
|  - 0 \cite{} in source             -> FIDEL-03               |
|  - 0 \bibitem entries in source                              |
|  - 0 [@refN] in candidate          -> D-48 strip if found    |
|                          |                                   |
|                          v                                   |
|  Verification Report Skeleton at                              |
|  verification_reports/review_of_framework_verification_report.md |
|  Sections: Provenance Note, Vacuous Policy Checks,            |
|            Section Audit (7 stubs PENDING),                   |
|            Fix Log (seed entry), Source Issues (placeholder), |
|            Final Verification (placeholder),                  |
|            Promotion Action (deferred to Wave 3)              |
+--------------------------------------------------------------+

Wave 2 (Plan 13-02): Section-by-Section Audit + Fixes
+--------------------------------------------------------------+
|  For each of 7 active sections in source order:               |
|    1. executive_summary.tex            (16 lines)             |
|    2. foundational_physical_metrics.tex (129 lines, math)     |
|    3. data_scaling_normalization.tex   (100 lines, table)     |
|    4. architectural_initialization_refinements.tex (27 lines) |
|    5. multi_component_loss_framework.tex (116 lines, math)    |
|    6. training_sampling_strategy.tex   (98 lines)             |
|    7. conclusion_and_recommendations.tex (27 lines, table)    |
|                          |                                   |
|                          v                                   |
|  Audit checks (per section):                                  |
|  - FIDEL-01 formula-by-formula checklist (sections 2 and 5)   |
|  - FIDEL-02 prose / lists / code blocks                       |
|  - FIDEL-04 table cell-by-cell (sections 3 and 7)             |
|  - FIDEL-05 heading hierarchy                                 |
|  - Pandoc artifact sweep:                                     |
|      * \- escaped dash list markers (29 known in candidate)   |
|      * \[...\] escaped prose brackets (23 known)              |
|      * grid-table -> GFM (D-29 inherited)                     |
|      * duplicate longtable headers                            |
|                          |                                   |
|                          v                                   |
|  Apply markdown-only fixes IN PLACE on the candidate file     |
|  (still at pandoc_conversion/ path during Wave 2)             |
|                          |                                   |
|                          v                                   |
|  Discrepancy table per section + Fix Log entries              |
+--------------------------------------------------------------+

Wave 3 (Plan 13-03): Promote + Index + Final Verification
+--------------------------------------------------------------+
|  Promotion (D-43):                                            |
|    git mv pinn_instruction/markdown_conversion/               |
|              pandoc_conversion/review_of_ctl-pinn_framework.md|
|         -> pinn_instruction/markdown_conversion/              |
|                            review_of_framework.md             |
|                          |                                   |
|                          v                                   |
|  Append Source Issues / Notes for Future Reconciliation       |
|  to authoritative markdown (D-17/D-18 inherited)              |
|                          |                                   |
|                          v                                   |
|  Update markdown_conversion/README.md (D-45)                  |
|  Add Phase 13 row with parent-dir metadata column noting      |
|    "LaTeX parent: review-of-framework/ (shared with Phase 14)"|
|                          |                                   |
|                          v                                   |
|  Finalize verification report:                                |
|  - All 7 sections Status: PASS                                |
|  - Zero open discrepancies                                    |
|  - Single pandoc candidate; CLEAN-02 N/A (D-40)               |
|  - Complete fix log                                           |
|  - Vacuous Policy Checks confirmed                            |
+--------------------------------------------------------------+
```

### Recommended Project Structure (Phase 13 outputs)

```
pinn_instruction/markdown_conversion/
+-- review_of_framework.md                   # NEW authoritative (D-43, Wave 3)
+-- README.md                                # MODIFIED — Phase 13 row added (D-45)
+-- verification_reports/
|   +-- review_of_framework_verification_report.md  # NEW (D-44, Waves 1-3)
+-- pandoc_conversion/
    +-- review_of_ctl-pinn_framework.md      # SOURCE for promotion; moved to top level by Wave 3
                                             # (or kept here if you prefer copy semantics — Wave 3 decides)

pinn_instruction/original_latex/review-of-framework/
+-- review_of_framework/                     # Phase 13's source sub-document
|   +-- review_of_framework.tex              # Entry point (7 active \input directives)
|   +-- preamble.tex                         # Reference only
|   +-- sections/
|       +-- executive_summary.tex                          # active 1 (16 lines)
|       +-- foundational_physical_metrics.tex              # active 2 (129 lines, MATH)
|       +-- data_scaling_normalization.tex                 # active 3 (100 lines, TABLE)
|       +-- architectural_initialization_refinements.tex   # active 4 (27 lines)
|       +-- multi_component_loss_framework.tex             # active 5 (116 lines, MATH+CODE)
|       +-- training_sampling_strategy.tex                 # active 6 (98 lines)
|       +-- conclusion_and_recommendations.tex             # active 7 (27 lines, TABLE)
+-- stage_strat_revision/                    # Phase 14's source — NOT in audit scope
```

### Pattern 1: Three-Wave Execution (mirrored from Phase 12 with CAND-02 adaptations)

**What:** Execute Phase 13 as 3 sequential plans:
- Wave 1 (13-01): Provenance note + Vacuous Policy Checks + report skeleton
- Wave 2 (13-02): Section-by-section audit + fixes
- Wave 3 (13-03): Promote + index update + final verification

Each wave depends on the prior wave's completion (D-41).

**Why three waves and not two:** D-41 explicitly chose 3 plans for muscle-memory
consistency with Phases 10–12 over the marginal savings of collapsing to 2.
The "Starting Candidate Provenance" output from Wave 1 still has audit value — it
records the file size, line count, and conversion-tool metadata that future readers
need to understand which file was used.

### Pattern 2: Vacuous Policy Checks Subsection (D-47)

**What:** A short report subsection that explicitly confirms — by grep evidence — that
the source contains zero of: `\begin{comment}` blocks, `\authcomment{}` markers,
`\cite{}` commands, `\bibitem` entries, and inactive section files.

**When to use:** Required in Wave 1's report skeleton; finalized in Wave 3.

**Example (skeleton form, populate with actual zero counts):**
```markdown
## Vacuous Policy Checks (D-47)

The review-of-framework source has structural simplicity that vacuously satisfies
several inherited decisions. Each absence is verified by grep:

| Check | Source Pattern | Count | Inherited Decision Vacuously Satisfied | Status |
|-------|----------------|-------|----------------------------------------|--------|
| Comment blocks | `\begin{comment}` | 0 | D-05, D-09 (AUDIT-03 / FIDEL-06 source side) | VACUOUS PASS |
| Author comments | `\authcomment{` | 0 | D-06, D-07 | VACUOUS PASS |
| Inactive sections | `*_inactive.tex` | 0 | D-34, D-35, D-38 | VACUOUS PASS |
| Citations | `\cite{` | 0 | D-27, D-28 (FIDEL-03 source side) | VACUOUS PASS |
| Bibliography entries | `\bibitem{` | 0 | D-37 | VACUOUS PASS |

Per D-48: candidate searched for `[@refN]` injected pandoc citation artifacts —
count: {actual count}. {If >0: list locations and apply D-27 strip-policy.}
```

### Pattern 3: Pandoc Artifact Sweep (Wave 2 audit responsibility)

**What:** During each section's audit, scan for pandoc-specific conversion artifacts
that are not faithful to the LaTeX source. The candidate has confirmed instances of
all three.

**Confirmed artifacts in this candidate (verified 2026-05-05):**

| Artifact | Pattern | Confirmed Count | Likely Severity | Fix Approach |
|----------|---------|-----------------|-----------------|--------------|
| Escaped-dash list markers | `^\-` (line starts with `\-`) | 29 | MINOR | Replace with `- ` (plain dash + space). Pandoc emits `\-` for `-` in some contexts to disambiguate from em-dash escapes. |
| Escaped prose brackets | `\[-1, 1\]` etc. | 23 | MINOR | Replace `\[` with `[` and `\]` with `]` in prose contexts (NOT inside math `$...$` or display `$$...$$`). |
| Longtable duplicate header rows | "Table -- continued from previous page" / "Continued on next page" rows in markdown grid-table | 1 (input-vector spec table, lines 199-204 in candidate) | MINOR | Delete the duplicate header rows. LaTeX `\endfirsthead` / `\endhead` is for PDF pagination only. Phase 12 fixed an identical pattern (PINN-12-02-02, PINN-12-02-03). |
| Pandoc grid-table format | `+----+---+` table syntax | 1 large table (input-vector specification) | INFO or MINOR | Inherited D-29 prefers GFM pipe-tables. The 13-row table is large; verify renderability first, then convert if D-29 is enforced. |

**Anti-pattern:** Don't fix these in bulk via global find/replace — some `\[ \]` may
appear inside code blocks or fenced regions where the escape is correct (or the
character is part of source content). Apply section-scoped fixes per D-20.

### Anti-Patterns to Avoid

- **Re-running pandoc.** REQUIREMENTS.md "Out of Scope" explicitly forbids it: any
  manual fixes already applied to the candidate would be discarded.
- **Modifying LaTeX source.** Same constraint — LaTeX is ground truth (D-13
  inherited).
- **Skipping the Vacuous Policy Checks subsection** because everything is zero. D-47
  requires explicit confirmation; future readers should not have to re-grep to know
  the source had no comments / citations / bibliography. Empty tables are fine; absence
  of the subsection is not.
- **Treating math-light sections as trivial.** Sections 1, 4, 7 (executive_summary,
  architectural_initialization_refinements, conclusion_and_recommendations) are short
  but section 7 contains a 6-row hyperparameter schedule table that requires FIDEL-04
  cell-by-cell verification.
- **Bulk find/replace on artifacts.** Apply section-scoped fixes per D-20; some `\[ \]`
  occurrences may legitimately escape brackets inside code or other contexts.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Candidate validation | Diff-scoring methodology applied to N=1 | "Starting Candidate Provenance" note (D-42 verbatim format) | Single-candidate workflow has no ranking step; provenance is sufficient. |
| Vacuous policy report | New section ordering | D-47 subsection wording with grep evidence | Locked decision; produce verbatim. |
| Verification report structure | Phase-13-specific layout | Phase 12 report template (Provenance/Vacuous Checks → Section Audit → Fix Log → Source Issues → Final Verification → Promotion Action) | Established pattern; users expect symmetry across Phases 10–14 reports. |
| Discrepancy ID format | New scheme | `RoF-13-XX-NN` (or planner-chosen stable format consistent with D-12) | IDs must remain stable from audit table to fix log. |
| Index README format | New table layout | Existing 4-column flat index format (Source / Authoritative markdown / Verification report / Candidate archive) with N/A for Phase 13's archive column per D-40 | D-45/D-46 specify flat index, parent-dir metadata can go in source column or as inline note. |
| Markdown line counts | Custom counting script | `wc -l` | Universal and matches Phase 10/11/12 evidence style. |

**Key insight:** Phase 13 introduces zero novel verification challenges. The single-
candidate adaptation (Provenance Note instead of Ranking Report) is the only structural
change from Phase 12, and it's specified down to the field list in D-42. Everything else
reuses prior phase patterns.

## Runtime State Inventory

> Not applicable — Phase 13 is pure documentation verification with no runtime services,
> databases, or live configuration.

| Category | Items Found | Action Required |
|----------|-------------|-----------------|
| Stored data | None — no databases or datastores | None |
| Live service config | None — no external services | None |
| OS-registered state | None — no systemd/launchd/pm2 tasks | None |
| Secrets/env vars | None — no credentials | None |
| Build artifacts | None — documentation-only phase | None |

**Phase scope:** Documentation file operations only. No runtime state categories apply.

## Common Pitfalls

### Pitfall 1: Treating Vacuous Checks as Implicit

**What goes wrong:** Auditor (or planner) concludes that since the source has zero
comment blocks, citations, etc., the verification report can simply omit the Vacuous
Policy Checks subsection.

**Why it happens:** Phases 10–12 had non-zero counts of these constructs, so the
"absence verification" pattern feels redundant when everything is zero.

**How to avoid:** D-47 mandates explicit confirmation. Include the subsection with
zero-count rows so future readers don't have to re-verify the assumption. The
subsection's value is documentation, not detection.

**Warning signs:** Verification report missing the Vacuous Policy Checks subsection;
report relies on phrases like "as in prior phases" instead of explicit grep counts.

### Pitfall 2: Conflating Pandoc Artifacts with Source Issues

**What goes wrong:** During audit, candidate's `\-` and `\[ \]` escapes get
misclassified as source-level issues that should be preserved per CROSS-01.

**Why it happens:** CROSS-01 says "preserve inter-document inconsistencies"; auditor
generalizes this to "preserve all unusual formatting."

**How to avoid:** Distinguish two categories:
1. **Source-level content** in the LaTeX (e.g., a formula choice, a description of
   inter-document inconsistency, a methodology argument) — preserved per CROSS-01.
2. **Pandoc conversion artifacts** in the markdown (e.g., `\-`, `\[`, duplicate header
   rows, grid-table syntax) — fixed per FIDEL-02 / FIDEL-04.

The test: if you re-typed the LaTeX source by hand into clean markdown, would this
artifact appear? If no, it's a conversion artifact, fix it.

**Warning signs:** Fix log entries that say "preserved per CROSS-01" for things that
are clearly pandoc output quirks (escapes, table format, pagination markers).

### Pitfall 3: Math-Heavy Section Underaudit (Sections 2 and 5)

**What goes wrong:** Auditor skims the math sections and marks them PASS without a
formula-by-formula checklist, because at-a-glance they look fine.

**Why it happens:** Pandoc 3.x usually preserves LaTeX math correctly inside `$...$`
and `$$...$$` delimiters, so most formulas DO render fine. The audit feels redundant.

**How to avoid:** Per D-14, math-heavy sections require a numbered formula checklist
in the audit subsection. Use the LaTeX source's display-math environments (`equation`,
`align`, `\[ ... \]`) as the canonical list; verify each one appears in the candidate
with matching content. The math-heavy sections in this phase are:

- **Section 2 (foundational_physical_metrics.tex, 129 lines):** ~6 display blocks —
  angular momentum sum (line 21-23), characteristic-scales align (line 26-29), L_max
  product (line 32-34), Lyapunov exponent average (line 67-69), Lyapunov time
  reciprocal (line 72-74), global-scale align (line 123-126).
- **Section 5 (multi_component_loss_framework.tex, 116 lines):** ~3 main display blocks
  for the data loss L1, physics residual fi(t'), and total Hamiltonian, plus a
  ~40-line PyTorch code block for `compute_kinematics` (verbatim — verify
  `create_graph=True` argument, comments, return types).

**Warning signs:** Section audit subsection has prose verification only and no formula
checklist. Section status is PASS with no enumerated math evidence.

### Pitfall 4: Table Cell-by-Cell Audit Skipped or Bulk-Verified

**What goes wrong:** The 13-row "Definitive Input Vector Specification" table in
Section 3 (data_scaling_normalization.tex) is marked verified without explicit cell
checks. Symbols, formulas, and ranges drift unnoticed.

**Why it happens:** The table is large (13 components × 5 columns = 65 cells) and the
candidate's grid-table format is hard to read at a glance. Auditor takes a shortcut.

**How to avoid:** FIDEL-04 requires cell-by-cell verification. Build a per-row
checklist with the LaTeX cell content vs. markdown cell content for the 13 rows.
Pay special attention to:
- Subscripts and superscripts inside `$...$` (e.g., `$m_1^{\text{norm}}$`,
  `$L_{\max}$`, `$s_{\min}^{\text{norm}}$`).
- The Final Range column entries `\[-1, 1\]` (escaped) vs. `[-1, 1]` (plain).
- The `Continued on next page` / `Table -- continued from previous page` artifact
  rows that should be deleted.

The smaller hyperparameter table in Section 7 (6 rows × 5 columns = 30 cells) is
also mandatory FIDEL-04 territory.

**Warning signs:** Section 3 or Section 7 audit has Status: PASS with no per-row
verification table.

### Pitfall 5: Subsection Heading Drift (#### vs ##)

**What goes wrong:** LaTeX uses `\paragraph{Context and Validation}` and
`\paragraph{Proposed Solution and Implementation}` as the third-level heading style.
Pandoc renders these as `####` (h4). Auditor sees the markdown is missing `###` (h3)
headings and flags this as a hierarchy error — but the source genuinely skips that
level.

**Why it happens:** LaTeX `\paragraph` is technically heading level 4 in `article`
class, even when it visually appears as a third-tier heading. The candidate's `####`
rendering is correct.

**How to avoid:** When auditing FIDEL-05, use the actual LaTeX heading commands as
ground truth, not visual hierarchy. Map `\section` → `#`, `\subsection` → `##`,
`\subsubsection` → `###`, `\paragraph` → `####`. The candidate already follows this
mapping correctly (verified in candidate's heading dump at lines 22, 26, 32, 78, 82, 86,
etc.).

**Warning signs:** Section audit flags missing `###` headings as MAJOR discrepancies
when source has `\paragraph` (not `\subsubsection`).

### Pitfall 6: Promotion Path / git mv vs cp Decision

**What goes wrong:** Wave 3 either copies the candidate (leaving a stale duplicate
at `pandoc_conversion/`) or moves it (breaking the historical pandoc-output reference).

**Why it happens:** D-43 specifies the authoritative path but doesn't lock the
move-vs-copy semantics; D-40 says no archive directory but doesn't say what to do
with the old `pandoc_conversion/` file.

**How to avoid:** Recommend `git mv` (move) — the candidate's role transitions from
"pandoc output" to "authoritative markdown" once Wave 2's fixes are applied. Leaving
a duplicate at `pandoc_conversion/` would create the same dual-source-of-truth problem
that v1.3 is trying to eliminate. Phase 12 used `git mv` for unselected candidates;
applying the same semantics to the selected (only) candidate keeps the pattern
consistent.

If the planner wants `cp` semantics for any reason, the old path's file should be
explicitly deleted by Wave 3 to avoid duplication. The planner must pick one of:
move OR (copy + delete original) — either yields a single canonical location.

**Warning signs:** After Wave 3, two near-identical files exist at
`pandoc_conversion/review_of_ctl-pinn_framework.md` AND
`markdown_conversion/review_of_framework.md`.

## Code Examples

Verified shell patterns for Phase 13 execution. All commands assume the working directory
is the repository root (`<home>/Desktop/3_body_problem`).

### Vacuous Policy Verification (Wave 1)

```bash
# Source-side absence checks — D-47
SECTIONS_DIR="pinn_instruction/original_latex/review-of-framework/review_of_framework/sections"
ENTRY="pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex"

echo "Comment blocks:"
grep -c '\\begin{comment}' "$ENTRY" "$SECTIONS_DIR"/*.tex
echo "Author comments:"
grep -c '\\authcomment{' "$ENTRY" "$SECTIONS_DIR"/*.tex
echo "Citations:"
grep -c '\\cite{' "$ENTRY" "$SECTIONS_DIR"/*.tex
echo "Bibitems:"
grep -c '\\bibitem{' "$ENTRY" "$SECTIONS_DIR"/*.tex
echo "Inactive section files:"
ls "$SECTIONS_DIR"/*_inactive.tex 2>/dev/null | wc -l

# Candidate-side D-48 check
CAND="pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md"
echo "Pandoc-injected citations [@refN]:"
grep -cE '\[@ref[0-9]+\]' "$CAND"
```

[VERIFIED: ran these queries during research 2026-05-05 — all source counts return 0;
candidate `[@refN]` count returns 0; D-48 vacuously satisfied.]

### Pandoc Artifact Detection (Wave 2)

```bash
CAND="pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md"

# Escaped-dash list markers
echo "\\- list markers:"; grep -cE '^\\-' "$CAND"
# Escaped prose brackets (excludes display math which uses $$ delimiters)
echo "\\[ escapes:"; grep -cE '\\\[' "$CAND"
# Longtable continuation artifacts
echo "Continuation marker rows:"
grep -nE 'continued from previous page|Continued on next page' "$CAND"
# Grid-table syntax (count of separator lines starting with '+')
echo "Grid-table separator lines:"
grep -cE '^\+[-=:]' "$CAND"
```

[VERIFIED: `\\-` → 29; `\\[` → 23; continuation markers → 1 table; grid-table separators
present in input-vector spec table.]

### Section Heading Extraction (FIDEL-05 evidence)

```bash
# Source: extract section/subsection commands in document order
ENTRY="pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex"
SECTIONS_DIR="pinn_instruction/original_latex/review-of-framework/review_of_framework/sections"

# Active imports in order (per D-39 / inherited D-13 ground truth)
grep -nE '^\\input\{sections' "$ENTRY"

# Per-file heading commands
for f in "$SECTIONS_DIR"/*.tex; do
  echo "=== $f ==="
  grep -nE '^\\(section|subsection|subsubsection|paragraph)\*?\{' "$f"
done

# Candidate: extract markdown headings in order
grep -nE '^#+ ' pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md
```

### Promotion (Wave 3)

```bash
# D-43: promote corrected candidate to authoritative path
git mv pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md \
       pinn_instruction/markdown_conversion/review_of_framework.md
git commit -m "phase(13-03): promote corrected review-of-framework markdown to authoritative path"
```

[CITED: pattern matches Phase 12 wave-3 plan steps]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Multi-candidate ranking with diff-scoring | Single-candidate provenance note | Phase 13 (D-39, D-42) | Eliminates ranking step; CAND-02 explicit. |
| `_archive/` directory per phase | Skipped when only one candidate exists | Phase 13 (D-40) | CLEAN-02 vacuous; no archive readme. |
| Implicit absence assumptions | Explicit "Vacuous Policy Checks" subsection | Phase 13 (D-47) | Self-contained audit trail; no re-grep needed. |
| Audit-first inactive-section search | Vacuous PASS by file enumeration | Phase 13 (D-34/D-35/D-38 inherited as vacuous) | No `*_inactive.tex` exists; structural+content search both vacuous. |

**Deprecated/outdated for this phase:**
- Diff-score F1/recall ranking methodology (no second candidate to compare against).
- Inactive-section content search with distinctive terms (no inactive files).
- Bibliography bibitem audit (no `\bibitem` entries; FIDEL-03 vacuously satisfied at source).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The `\-` line markers and `\[ \]` prose escapes in the candidate are pandoc artifacts (not faithful conversions of LaTeX source content). | Pattern 3 / Pitfall 2 | If they ARE faithful (e.g., source uses literal escaped brackets in some code block), fixing them would introduce a new fidelity issue. Wave 2 must verify per occurrence. [ASSUMED — based on pandoc 3.x escape behavior and source spot-checks; not fully cross-checked occurrence-by-occurrence] |
| A2 | The "Source Issues / Notes for Future Reconciliation" metadata pattern from D-17/D-18 (Phase 10 origin) applies unchanged to Phase 13. | Wave 3 deliverables | Low risk — Phase 11 and Phase 12 both used this pattern with no adaptation. [CITED: 12-CONTEXT.md decisions section, 12-03-PLAN.md task 1] |
| A3 | The candidate currently lives only at `pandoc_conversion/review_of_ctl-pinn_framework.md` and not elsewhere in the repo. | Wave 3 promotion | If a duplicate already exists at the target path or elsewhere, the move would conflict. [VERIFIED: `ls pinn_instruction/markdown_conversion/` shows only the 4 prior phases' authoritative files plus the pandoc_conversion subdir; no `review_of_framework.md` exists yet at the target path.] |
| A4 | Pandoc grid-tables (lines 196–233 of candidate) render acceptably in standard markdown viewers (GitHub, VS Code preview), so D-29 GFM conversion is a polish item rather than a blocking requirement. | Pattern 3 | If grid-tables fail to render in the target consumption context, MAJOR severity. [ASSUMED — needs planner decision; D-29 in Phase 11 was applied to HTML tables, not grid-tables, so this is an extension.] |
| A5 | The single-candidate workflow does not require a "candidate comparison" section in the report skeleton — the Provenance Note replaces it. | Wave 1 deliverable | Low risk — D-42 explicitly specifies the Provenance Note format and contents. |

**Open question for the planner:** A1 and A4 are the items most likely to need user
or planner judgment. See "Open Questions" section below.

## Open Questions

1. **Should pandoc grid-tables (in input-vector spec table) be converted to GFM?**
   - What we know: D-29 inherited from Phase 11 prefers GFM table format. Phase 11 applied
     it to HTML tables in the data-quality-assessment candidate.
   - What's unclear: D-29's text may not have anticipated pandoc grid-tables (which are a
     valid pandoc-extended markdown format and render fine in many viewers).
   - Recommendation: Planner reads `data_quality_assessment_verification_report.md` to see
     the exact D-29 wording and decides. If converting, the 13-row table conversion is a
     non-trivial Wave 2 task and should be its own discrepancy entry in the audit.

2. **Should `\-` and `\[ \]` escape fixes be MINOR or INFO severity?**
   - What we know: They're cosmetic — the rendered output looks fine in most markdown viewers
     (the `\` is a valid escape that preserves the literal character). But the LaTeX source
     uses `-` and `[ ]` directly without escapes, so the candidate is technically not a
     faithful character-level conversion.
   - What's unclear: D-12 leaves severity classification to discretion. Phase 10/11/12 used
     "MINOR" for similar pandoc-noise items.
   - Recommendation: Use MINOR for both, consistent with Phase 12's table-pagination artifact
     classification (PINN-12-02-02, PINN-12-02-03 were MINOR).

3. **`docs/findings/review_of_01.md` deletion (current git status shows `D` not staged):**
   - What we know: That file lived under `docs/findings/` and was added in commit `5e0e476`
     ("docs(findings): add archive-consolidation critique and Phase 1 review"). A copy
     exists at `docs/findings/verification_3_thematic_documents/review_of_01.md` (untracked
     directory in current status). The file relates to Phase 9's `issues/` thematic-document
     consolidation, not to Phase 13's pandoc-vs-LaTeX audit.
   - What's unclear: Whether the deletion is intentional housekeeping (the contents moved
     to the new `verification_3_thematic_documents/` subfolder) or accidental.
   - Recommendation: Phase 13 should NOT touch `docs/findings/`. The file is unrelated to
     Phase 13's scope (Phase 13 produces `pinn_instruction/markdown_conversion/...` artifacts,
     not `docs/findings/...`). Flag this in plan-level note so the planner doesn't accidentally
     restage it. The user may want to commit the deletion separately as housekeeping.

4. **Promotion semantics: `git mv` vs. `cp`?**
   - What we know: D-43 specifies the authoritative path; Phase 12 used `git mv` for the
     archive case.
   - What's unclear: Whether to keep the candidate at its original `pandoc_conversion/` path
     for historical reference.
   - Recommendation: Use `git mv` (move), consistent with Pitfall 6 above. Single source of
     truth at the new path; the git history preserves the rename.

5. **Should Wave 2 use multiple sub-tasks (one per section) or one big audit task?**
   - What we know: Phase 12-02-PLAN had 2 tasks (sections 1-3 and 4-7); Phase 11 used a
     similar split.
   - What's unclear: Whether Phase 13's 7 sections (with 2 of them substantial) is best
     split into 2 tasks (sections 1-4 and 5-7), 1 task, or per-section tasks.
   - Recommendation: Mirror Phase 12 — split into 2 tasks (sections 1-4 and sections 5-7),
     placing the largest math-heavy section (multi_component_loss_framework, 116 lines) at
     the start of task 2. This keeps task sizes balanced with prior phases.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| git | Promotion (`git mv`), commits | YES | 2.50.1 | — |
| grep / ugrep | Vacuous policy checks, artifact detection | YES | ugrep 7.5.0 | BSD grep |
| wc | Line/byte counts for provenance | YES | BSD wc | — |
| diff | Optional manual evidence-gathering during audit | YES | Apple/BSD diff | — |
| pandoc | Reference only (not re-run) | YES | 3.7.0.2 | not needed for execution |

[VERIFIED: all five tools queried in this research session 2026-05-05]

**Missing dependencies with no fallback:** None.
**Missing dependencies with fallback:** None.

## Validation Architecture

> `workflow.nyquist_validation` is treated as enabled by default (config not explicitly
> set to false). However, this is a documentation verification phase — there is no test
> framework to invoke.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None — documentation verification phase |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

**Note:** Phase 13 has no automated test suite. Validation is human inspection of the
verification report combined with grep evidence (Wave 1's vacuous-policy commands and
Wave 2's pandoc-artifact commands).

### Phase Requirements → Verification Map
| Req ID | Behavior | Verification Method | Wave |
|--------|----------|---------------------|------|
| CAND-02 | Single-candidate skip | Provenance Note presence + content (D-42) | Wave 1 |
| AUDIT-01 | Section-by-section comparison | 7 audit subsections present, each with content | Wave 2 |
| AUDIT-02 | Discrepancy documentation | Discrepancy tables in each audit subsection | Wave 2 |
| AUDIT-03 | Comment block exclusion | Vacuous Policy Checks subsection (D-47) | Wave 1 |
| FIDEL-01 | Formula accuracy | Formula checklists in sections 2 & 5 audit subsections | Wave 2 |
| FIDEL-02 | Prose fidelity | Prose verification in each audit subsection + pandoc artifact fixes | Wave 2 |
| FIDEL-03 | Reference fidelity | Vacuous Policy Checks (no `\cite`/`\bibitem`) | Wave 1 |
| FIDEL-04 | Table cell verification | Cell-by-cell tables for sections 3 & 7 audit subsections | Wave 2 |
| FIDEL-05 | Section hierarchy | Heading map in audit (7 `#`, expected `##`/`####` per source `\section`/`\subsection`/`\paragraph`) | Wave 1 sanity-check, Wave 2 confirm |
| FIDEL-06 | Inactive content absence | Vacuous Policy Checks (no `*_inactive.tex`) | Wave 1 |
| CLEAN-01 | Single authoritative file | File at `markdown_conversion/review_of_framework.md` post-Wave 3 | Wave 3 |
| CLEAN-03 | Verification report complete | Report has Provenance, Vacuous Policy Checks, 7 PASS audits, Fix Log, Source Issues, Final Verification | Wave 3 |
| CROSS-01 | Inter-doc inconsistencies preserved | Source Issues metadata appended (or empty placeholder per D-17/D-18) | Wave 3 |
| CROSS-02 | Sequential phase pattern | Phase 13 follows Phase 12 three-wave structure | Planner enforces |

### Sampling Rate
- **Per task commit:** Auditor reviews task output before commit.
- **Per wave merge:** Full wave review before proceeding.
- **Phase gate:** Zero open discrepancies, Vacuous Policy Checks PASS, index updated.

### Wave 0 Gaps
- [ ] None — documentation verification has no test infrastructure to set up.

## Security Domain

> Phase 13 has no user input, network access, database queries, authentication,
> or cryptographic operations. Security domain not applicable. The only execution
> action is `git mv` of a documentation file within the repository.

## Concrete File / Directory Deliverables

Files Phase 13 will produce (or modify). Every path verified to fit the existing repo
structure.

| Path | Action | Wave | Authority |
|------|--------|------|-----------|
| `pinn_instruction/markdown_conversion/verification_reports/review_of_framework_verification_report.md` | CREATE | Wave 1 (skeleton), Wave 2 (audit content), Wave 3 (final) | D-44 |
| `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md` | MODIFY in place during Wave 2; MOVED in Wave 3 | Wave 2 → 3 | D-39, D-43 |
| `pinn_instruction/markdown_conversion/review_of_framework.md` | CREATED via `git mv` from above; appended Source Issues metadata | Wave 3 | D-43, D-17/D-18 |
| `pinn_instruction/markdown_conversion/README.md` | MODIFY (add Phase 13 row with parent-dir metadata) | Wave 3 | D-45 |
| `.planning/phases/13-review-of-framework-verification/13-01-PLAN.md` | CREATE (planner output) | pre-Wave 1 | (not Phase 13 output — planner deliverable) |
| `.planning/phases/13-review-of-framework-verification/13-02-PLAN.md` | CREATE (planner output) | pre-Wave 2 | (not Phase 13 output — planner deliverable) |
| `.planning/phases/13-review-of-framework-verification/13-03-PLAN.md` | CREATE (planner output) | pre-Wave 3 | (not Phase 13 output — planner deliverable) |
| `.planning/phases/13-review-of-framework-verification/13-01-SUMMARY.md` | CREATE | end of Wave 1 | (executor output) |
| `.planning/phases/13-review-of-framework-verification/13-02-SUMMARY.md` | CREATE | end of Wave 2 | (executor output) |
| `.planning/phases/13-review-of-framework-verification/13-03-SUMMARY.md` | CREATE | end of Wave 3 | (executor output) |

**No files created:** `_archive/review-of-framework/` directory (D-40 explicitly forbids).

**No files modified:** Any LaTeX source file under `pinn_instruction/original_latex/`
(REQUIREMENTS.md "Out of Scope").

## Per-Requirement Implementation Guidance

Grouped by theme as requested, with concrete file/check guidance.

### CAND-02 (Single-candidate workflow)
- **What:** No multi-candidate ranking; use the only pandoc file directly.
- **How:** Wave 1 produces a "Starting Candidate Provenance" note in the report at
  `verification_reports/review_of_framework_verification_report.md` per D-42 format:
  source path, `wc -l` line count (533), `wc -c` byte count, conversion tool
  (pandoc 3.7.0.2), date observed, "CAND-02 applies — no ranking needed."

### AUDIT-01, AUDIT-02, AUDIT-03 (Audit and comparison)
- **AUDIT-01** (section-by-section): Wave 2 audits the 7 sections in source order
  (executive_summary → foundational_physical_metrics → data_scaling_normalization →
  architectural_initialization_refinements → multi_component_loss_framework →
  training_sampling_strategy → conclusion_and_recommendations). Each section gets a
  subsection in the report with a discrepancy table.
- **AUDIT-02** (every discrepancy documented): Use the Phase 12 discrepancy-table
  format: `ID | Type | Severity | Source loc | Markdown loc | Issue | Fix status`.
  ID format suggestion: `RoF-13-{plan}-{NN}` (e.g., `RoF-13-02-01`).
- **AUDIT-03** (comment-block exclusion): Vacuously satisfied. Document via the
  Vacuous Policy Checks subsection (D-47) with `grep -c '\\begin{comment}'` count = 0.

### FIDEL-01–FIDEL-06 (Content fidelity)
- **FIDEL-01** (formulas): Build formula-by-formula checklists for sections 2 and 5.
  Source has ~9 numbered display-math equations across these two sections plus inline
  math throughout. Wave 2 verifies each appears in the candidate with matching
  content. Pay attention to `\begin{equation}`, `\begin{align}`, `\[ ... \]` source
  forms versus candidate's `$$ ... $$` rendering.
- **FIDEL-02** (prose, lists, code): Standard prose comparison plus the pandoc artifact
  sweep (29 `\-` items, 23 `\[` items). Section 5 also has a ~40-line PyTorch code
  block (`compute_kinematics`) that must be verified verbatim including comments,
  argument names (`network_output_r`, `time_input_t`), critical comment marker
  (`CRITICAL: Retain graph for second derivative`), and `create_graph=True`/`False`
  values.
- **FIDEL-03** (references): Vacuously satisfied (no `\cite{}`, `\bibitem`, `\ref`,
  `\label` in source). Document in Vacuous Policy Checks subsection.
- **FIDEL-04** (tables): Two tables require cell-by-cell:
  - Section 3: 13-row "Definitive Input Vector Specification" longtable (currently
    pandoc grid-table at candidate lines 196-235).
  - Section 7: 6-row "Consolidated Hyperparameter Schedule" table at candidate lines
    516-530.
  Verify cell content for symbols, formulas, ranges; remove the duplicate-header
  artifact in the Section 3 table (lines 199-204 of candidate).
- **FIDEL-05** (section hierarchy): Confirmed candidate has 7 top-level `#` headings
  matching the 7 active imports. Sub-mapping: `\section` → `#`, `\subsection` → `##`,
  `\paragraph` → `####` (no `\subsubsection` used in source). Wave 1 records this
  mapping in the report; Wave 2 confirms per section.
- **FIDEL-06** (commented content absent): Vacuously satisfied (no comment blocks,
  no inactive files). Document in Vacuous Policy Checks.

### CLEAN-01, CLEAN-03 (Cleanup and authority)
- **CLEAN-01** (single authoritative file): Wave 3 promotes via `git mv` to
  `markdown_conversion/review_of_framework.md` per D-43. After promotion, no other
  copy exists at `pandoc_conversion/`.
- **CLEAN-03** (verification report): Wave 3 finalizes the report at
  `verification_reports/review_of_framework_verification_report.md` per D-44 with:
  Provenance Note, Vacuous Policy Checks, 7 audit subsections (all PASS), Fix Log,
  Source Issues, Final Verification, Promotion Action. Plus the explicit
  "Single pandoc candidate; CLEAN-02 N/A" note per D-40.

### CROSS-01, CROSS-02 (Cross-cutting)
- **CROSS-01** (preserve inter-document inconsistencies): The body of the candidate
  discusses inconsistencies between `PINN_architecture_plan.tex` and `CTL-instruction-final.tex`
  — this analysis content is the source itself, preserved verbatim. Wave 3 appends a
  Source Issues / Notes for Future Reconciliation section per D-17/D-18 inherited;
  if no source-level issues are surfaced during audit, place a brief "No source-level
  issues identified" note (Phase 12 pattern).
- **CROSS-02** (sequential phases, same audit pattern): Phase 13 follows Phase 12's
  three-wave structure with single-candidate adaptations (D-41). Phase 13 EXECUTION
  must wait for Phase 12 final verification per D-49; planning may proceed.

## Sources

### Primary (HIGH confidence)
- `.planning/phases/13-review-of-framework-verification/13-CONTEXT.md` — All locked
  decisions D-39 through D-49 and phase boundary.
- `.planning/phases/13-review-of-framework-verification/13-DISCUSSION-LOG.md` — Decision
  alternatives and rationale.
- `.planning/REQUIREMENTS.md` — All 14 Phase 13 requirement IDs and CLEAN-02 N/A note.
- `.planning/ROADMAP.md` — Phase 13 success criteria and milestone v1.3 placement.
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex` —
  Verified 7 active `\input` directives at lines 13–19. No commented imports present.
- `pinn_instruction/original_latex/review-of-framework/review_of_framework/sections/*.tex` —
  All 7 active section files exist with line counts as listed above. Verified zero
  `\begin{comment}`, zero `\authcomment{`, zero `\cite{`, zero `\bibitem{` via grep
  during this research session.
- `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md` —
  Single pandoc candidate, 533 lines. Verified 7 top-level `#` headings, 29 `^\-`
  escape lines, 23 `\\[` escapes, 1 longtable continuation artifact, 0 `[@refN]`
  citation injections.
- `.planning/phases/12-pinn-architecture-verification/12-RESEARCH.md` and
  `12-01-PLAN.md`/`12-02-PLAN.md`/`12-03-PLAN.md` — Three-wave methodology blueprint.
- `pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md` —
  Verification report template structure (used directly as Phase 13's report skeleton).

### Secondary (MEDIUM confidence)
- `.planning/phases/10-ctl-instruction-verification/10-CONTEXT.md` — Origin of D-01–D-26
  (audit→fix→verify pattern, severity labels, Source Issues metadata convention).
- `.planning/phases/11-data-quality-assessment-verification/11-CONTEXT.md` — Origin of
  D-27 (citation-strip), D-29 (GFM tables), D-31 (verification_reports/ subdir),
  D-33 (active-section scope).
- Phase 10/11/12 SUMMARY files in their respective phase directories — Audit-pattern
  examples and report style references.
- `pinn_instruction/markdown_conversion/README.md` — Existing index format (4-column
  flat table) that Phase 13 must extend.

### Tertiary (LOW confidence)
- Pandoc 3.x behavior around `\-` and `\[` escapes — based on observation of the
  candidate file output and not direct documentation. The fixes proposed in
  Pattern 3 / Pitfall 2 should be verified against actual rendering in Wave 2.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all 5 tools verified present locally with versions.
- Architecture: HIGH — 7-section source structure verified by file enumeration; 7 active
  imports verified by grep; candidate's 7 `#` headings verified.
- Vacuous policy: HIGH — all 5 absence claims verified by grep with count = 0.
- Pandoc artifacts: HIGH — counts verified live (29 `\-`, 23 `\[`, 1 continuation
  artifact, 0 `[@refN]`).
- Pitfalls: HIGH — Phase 12 patterns directly applicable; Phase 13 mostly inherits.

**Research date:** 2026-05-05
**Valid until:** 30 days — source files are LaTeX (immutable per CROSS-01 / "Out of
Scope") and the candidate file is checked into git.
