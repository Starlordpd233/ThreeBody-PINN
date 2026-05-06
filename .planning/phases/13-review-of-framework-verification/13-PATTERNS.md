# Phase 13: Review-of-Framework Verification - Pattern Map

**Mapped:** 2026-05-05
**Files analyzed:** 7 (3 plan files, 1 verification report, 1 authoritative markdown, 1 README index modify, 3 SUMMARYs implied)
**Analogs found:** 7 / 7 — Phase 12 is the canonical template; Phase 11 supplies the single-candidate (CAND-02) variations.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.planning/phases/13-review-of-framework-verification/13-01-PLAN.md` | planning/plan-file | document-build (skeleton + provenance) | `.planning/phases/12-pinn-architecture-verification/12-01-PLAN.md` | role-match (Phase 12 had multi-candidate scoring; Phase 13 substitutes a Provenance Note per D-42) |
| `.planning/phases/13-review-of-framework-verification/13-02-PLAN.md` | planning/plan-file | section-by-section audit + fixes | `.planning/phases/12-pinn-architecture-verification/12-02-PLAN.md` | exact (same 2-task split: sections 1–N, sections N+1–7) |
| `.planning/phases/13-review-of-framework-verification/13-03-PLAN.md` | planning/plan-file | promotion + index + finalize | `.planning/phases/12-pinn-architecture-verification/12-03-PLAN.md` | role-match (Phase 12 had `_archive/` + Source Issues; Phase 13 drops `_archive/` per D-40) |
| `pinn_instruction/markdown_conversion/verification_reports/review_of_framework_verification_report.md` | documentation/discrepancy+fix-log | document-build across 3 plans | `pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md` | exact for audit/fix-log/final-verification structure; Provenance Note + Vacuous Policy Checks subsection are Phase 13 substitutions for Candidate Comparison + Excluded Inactive Sections |
| `pinn_instruction/markdown_conversion/review_of_framework.md` | documentation/authoritative-markdown | `git mv` from `pandoc_conversion/` + section-scoped edits + appended Source Issues | `pinn_instruction/markdown_conversion/pinn_architecture.md` | exact for placement and Source Issues append; promotion uses `git mv` (no copy semantics) per Pitfall 6 in 13-RESEARCH.md |
| `pinn_instruction/markdown_conversion/README.md` (modify — append row) | documentation/index | row-append | Existing rows for Phases 10–12 in same file | exact (4-column flat table; D-45 says use existing format with parent-dir metadata in source/title cell) |
| `.planning/phases/13-review-of-framework-verification/13-{01,02,03}-SUMMARY.md` | planning/executor-summary | end-of-wave summary | `.planning/phases/12-pinn-architecture-verification/12-{01,02,03}-SUMMARY.md` | exact (YAML front-matter + Tasks Completed + Deviations + Commits + optional Verification Results table) |

**No analogs needed:** None. Every Phase 13 deliverable maps to a Phase 12 (and 11) precedent.

**No file produced (despite Phase 12 producing it):** `_archive/review-of-framework/README.md` and `_archive/review-of-framework/<unselected>.md` — D-40 explicitly forbids `_archive/` for this phase (CLEAN-02 N/A, single candidate).

---

## Pattern 1 — Plan-file pattern (`13-01/02/03-PLAN.md`)

**Authoritative analog:** `.planning/phases/12-pinn-architecture-verification/12-01-PLAN.md` (and `12-02`, `12-03`).

### Structural elements (copy verbatim)

1. **YAML front-matter** at the top of every plan file. Field set observed in `12-01-PLAN.md:1-29`:

   ```yaml
   ---
   phase: 12-pinn-architecture-verification
   plan: 01
   type: execute
   wave: 1
   depends_on: []          # [12-01] for plan 02; [12-02] for plan 03
   files_modified:
     - <relative path>
   autonomous: true
   requirements: [CAND-01, AUDIT-03]   # Phase 12's IDs; Phase 13 uses CAND-02 + applicable IDs
   must_haves:
     truths:
       - "<observable assertion 1>"
       - "<observable assertion 2>"
     artifacts:
       - path: "<file>"
         provides: "<purpose>"
         min_lines: <n>
     key_links:
       - from: "<source artifact>"
         to: "<target artifact>"
         via: "<mechanism>"
         pattern: "<pattern name>"
   ---
   ```

   Phase 13 substitutions:
   - `phase: 13-review-of-framework-verification`
   - `plan: 01` / `02` / `03`
   - `requirements: [CAND-02, AUDIT-03]` for plan 01; `[AUDIT-01, AUDIT-02, FIDEL-01..FIDEL-06, CLEAN-01]` for plan 02; `[CLEAN-01, CLEAN-03, CROSS-01, CROSS-02]` for plan 03 (drop `CLEAN-02` — N/A per D-40).

2. **Body sections in fixed order** (observed in `12-01-PLAN.md:31-240`):

   - `<objective>` — 2–3 sentence purpose + output statement
   - `<execution_context>` — `@`-prefixed absolute paths to upstream artifacts
   - `<context>` — `@`-prefixed absolute paths to read-first inputs
   - `<interfaces>` (inside `<context>`) — HTML-comment-block of canonical structural facts (e.g., active-import line numbers)
   - `<tasks>` containing one or more `<task type="auto">` blocks
   - `<threat_model>` — Trust Boundaries table + STRIDE Threat Register
   - `<verification>` — bulleted checklist of post-conditions
   - `<success_criteria>` — bulleted requirement-ID coverage
   - `<output>` — instruction to create `13-XX-SUMMARY.md`

3. **Per-task XML structure** (observed in `12-01-PLAN.md:73-132`):

   ```xml
   <task type="auto">
     <name>Task N: <imperative description></name>
     <files><comma-separated absolute or repo-relative paths></files>
     <read_first>
       - <bullet list of files with one-line context>
     </read_first>
     <action>
       <step-by-step description; multi-paragraph allowed>
     </action>
     <verify>
       <automated>grep -c "<pattern>" <file></automated>
     </verify>
     <done>
       <one-paragraph completion criteria>
     </done>
   </task>
   ```

4. **Read-first lists** (`12-01-PLAN.md:76-89`) — list every file the executor must consult before writing. Always include:
   - The phase's CONTEXT.md and prior plan SUMMARYs (Phase 12-01-PLAN read 12-CONTEXT, 10-01-SUMMARY, 11-01-SUMMARY).
   - Source files with byte counts annotated in parentheses (`12-01-PLAN.md:81-87`).
   - The phase's prior verification report when this plan modifies it (`12-02-PLAN.md:84-89`).

### Acceptance-criteria format

- **`<verify><automated>` tag:** A single shell `grep -c` (or `ls | wc -l`) command with an inline expected count or threshold. Examples from Phase 12:
  - `12-01-PLAN.md:127`: `grep -c "Candidate Comparison\|Selected Baseline\|..." <report> | awk '{sum+=$1} END {print sum " sections (expected 6+)"}'`
  - `12-02-PLAN.md:122-123`: `grep -c "### Section 1: foundational_principles\|### Section 2: ..." <report>`
  - `12-03-PLAN.md:171-172`: `grep -c "pinn_architecture" pinn_instruction/markdown_conversion/README.md`

- **`<done>` block:** One paragraph (no bullets) stating the post-condition in the past tense, naming the artifacts created/modified and the most important content invariants.

- **`<success_criteria>` body section:** Bulleted list mapping each requirement ID covered by this plan to a one-line evidence statement. Example from `12-02-PLAN.md:213-223`.

### Phase 13 plan-file mapping

- **`13-01-PLAN.md`** mirrors `12-01-PLAN.md` but replaces multi-candidate scoring (Tasks 1–2) with a single "Starting Candidate Provenance" task and a "Vacuous Policy Checks" grep task. Task 3 (record promotion action + skeleton) is preserved verbatim in shape; promotion target path becomes `pinn_instruction/markdown_conversion/review_of_framework.md` (D-43). The Plan-1 `requirements:` line drops `CAND-01` and adds `CAND-02`.
- **`13-02-PLAN.md`** mirrors `12-02-PLAN.md` directly. Task 1 audits sections 1–4 (executive_summary → architectural_initialization_refinements); Task 2 audits sections 5–7 (multi_component_loss_framework → conclusion_and_recommendations). RESEARCH.md Open Question #5 explicitly recommends this split. Add a pandoc-artifact-sweep step (29 `\-`, 23 `\[`, 1 longtable continuation, grid-tables) inside both tasks per RESEARCH.md Pattern 3.
- **`13-03-PLAN.md`** mirrors `12-03-PLAN.md` with two structural deletions: Task 2 (archive unselected candidates with provenance README) is removed entirely (D-40), and the Final Verification bullet about D-38 inactive exclusion is replaced with the Vacuous Policy Checks summary (D-47). The README-index update task (Phase 12 Task 3, Step 1) keeps its row format but adds parent-dir metadata `LaTeX parent: review-of-framework/ (shared with Phase 14: stage-strategy-revision)` per D-45.

---

## Pattern 2 — Discrepancy-report pattern (verification report)

**Authoritative analog:** `pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md` (394 lines).
**Phase 11 cross-reference for single-table-vs-prose substitutions:** `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` (124 lines).

### Top-level section order (copy verbatim, with Phase 13 substitutions)

| # | Phase 12 section heading | Phase 13 equivalent |
|---|--------------------------|---------------------|
| 1 | `# PINN Architecture Markdown Verification Report` (line 1) | `# Review of Framework Markdown Verification Report` |
| 2 | `## Candidate Comparison` (lines 3–55) | `## Starting Candidate Provenance` (D-42 — short paragraph + small data table; no scoring) |
| 3 | `## Selected Baseline` (lines 57–79) | OMIT (no selection in single-candidate workflow). Promotion target named in Provenance Note instead. |
| 4 | `## Excluded Inactive Sections` (lines 81–139) | `## Vacuous Policy Checks` (D-47) — table with 5 rows, all `Count: 0`, all status `VACUOUS PASS` |
| 5 | `## Promotion Action` (lines 141–154) | Same heading; same "Deferred to Wave 3" pattern; `git mv` from `pandoc_conversion/review_of_ctl-pinn_framework.md` to `markdown_conversion/review_of_framework.md` (D-43) |
| 6 | `## Section Audit` (lines 156–351) with 7 `###` subsections | Same heading; 7 `###` subsections in source order: 1. executive_summary 2. foundational_physical_metrics (math) 3. data_scaling_normalization (table) 4. architectural_initialization_refinements 5. multi_component_loss_framework (math+code) 6. training_sampling_strategy 7. conclusion_and_recommendations (table) |
| 7 | `## Fix Log` (lines 354–362) | Same heading; same 3-column table (`ID \| Section \| Fix summary`) |
| 8 | `## Source Issues / Notes for Future Reconciliation` (lines 364–368) | Same heading; if no issues, single bulleted "No source-level issues identified during Phase 13 audit." per Phase 12 Task 1's no-issues fallback (`12-03-PLAN.md:91`) |
| 9 | `## Final Verification` (lines 370–394) | Same heading + table; CLEAN-02 row replaced with "Single pandoc candidate; CLEAN-02 N/A (D-40)"; D-38 inactive-exclusion row replaced with vacuous-policy summary (D-47/D-48) |

### Per-section audit subsection format (copy verbatim)

From `pinn_architecture_verification_report.md:158-178` (Section 1, no discrepancies) and `:181-213` (Section 2, math-heavy with discrepancies):

```markdown
### N. <source>.tex[ (math-heavy)| (largest, math-heavy)]

**Status:** PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| RoF-13-NN-NN | <type> | <BLOCKING\|MAJOR\|MINOR\|INFO> | <source>.tex:LL-LL | review_of_framework.md:LL-LL | <one-sentence issue> | Fixed \| Accepted as-is \| No fix needed |
| — | — | — | — | — | No discrepancies found | — |   ← when section has zero issues

**Content audit:**
- Heading: `\section{...}` → `# ...` — MATCH
- <Subsection / Subsubsection / Subsection> — MATCH
- <Prose paragraphs / lists / code blocks / inline math> — MATCH

**Formula checklist (<count> display math + <count> code blocks):**
1. <Formula name>: $<formula>$ — LaTeX `\[...\]` → Markdown `$$...$$` — MATCH
2. ...

---
```

Phase 13 specifics (from RESEARCH.md):
- Math-heavy formula checklists are mandatory for Section 2 (`foundational_physical_metrics.tex`, ~6 display math) and Section 5 (`multi_component_loss_framework.tex`, ~3 display math + ~40-line code block) per D-14.
- Cell-by-cell table verification mandatory for Section 3 (13-row Definitive Input Vector Specification longtable) and Section 7 (6-row Consolidated Hyperparameter Schedule) per FIDEL-04.
- "MATCH" is the Phase 12 verb for a verified-equivalent comparison; reuse it.

### Discrepancy ID format

- **Phase 12 used:** `PINN-12-{plan}-{NN}` — e.g., `PINN-12-01-BASELINE`, `PINN-12-02-01` (`pinn_architecture_verification_report.md:188, 358-362`).
- **Phase 11 used:** `DQA-{section}-{NNN}` and `DQA-{phase}-{plan}-BASELINE` — e.g., `DQA-01-001`, `DQA-11-01-BASELINE`.
- **Phase 13 recommended:** `RoF-13-{plan}-{NN}` (consistent with D-12 and Phase 12 form). Source-issue IDs use `SI-RoF-NNN` (Phase 12: `SI-PINN-001..003`).

Severity values are exactly: `BLOCKING`, `MAJOR`, `MINOR`, `INFO` (Phase 12: 4 levels; consistent across Phases 10–12).
Type values from Phase 12: `Conversion` (most common), `text`, `table`, `structure`, `citation`, `figure`, `comment`. Phase 13 will primarily use `Conversion` for the pandoc-artifact items (`\-`, `\[`, longtable headers, grid-table format).

### Phase 13–specific subsections to insert

**`## Starting Candidate Provenance`** — substitutes for Phase 12's `## Candidate Comparison` (D-42 fields):

```markdown
## Starting Candidate Provenance

The Phase 13 audit uses a single pandoc-converted markdown candidate. CAND-02 applies — no diff-score ranking is needed because no other candidates exist.

| Field | Value |
|---|---|
| Source path | `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md` |
| File size | <wc -c bytes> |
| Line count | 533 (verified by `wc -l`) |
| Conversion tool | pandoc 3.7.0.2 |
| Date observed | 2026-05-05 |
| CAND-02 status | Applies — single candidate, no ranking |
| CLEAN-02 status | N/A — no losing candidates to archive (D-40) |
```

**`## Vacuous Policy Checks`** — substitutes for Phase 12's `## Excluded Inactive Sections` (D-47 wording in RESEARCH.md Pattern 2):

```markdown
## Vacuous Policy Checks (D-47)

The review-of-framework source has structural simplicity that vacuously satisfies several inherited decisions. Each absence is verified by grep:

| Check | Source pattern | Count | Inherited decision vacuously satisfied | Status |
|---|---|---:|---|---|
| Comment blocks | `\begin{comment}` | 0 | D-05, D-09 (AUDIT-03 / FIDEL-06 source side) | VACUOUS PASS |
| Author comments | `\authcomment{` | 0 | D-06, D-07 | VACUOUS PASS |
| Inactive sections | `*_inactive.tex` | 0 | D-34, D-35, D-38 | VACUOUS PASS |
| Citations | `\cite{` | 0 | D-27, D-28 (FIDEL-03 source side) | VACUOUS PASS |
| Bibliography entries | `\bibitem{` | 0 | D-37 | VACUOUS PASS |

Per D-48: candidate searched for `[@refN]` injected pandoc citation artifacts — count: 0. (If non-zero: list locations and apply D-27 strip-policy.)
```

---

## Pattern 3 — Fix-log pattern

**Authoritative analog:** `pinn_architecture_verification_report.md:354-362` (5 entries, 3-column table).

**Verbatim shape:**

```markdown
## Fix Log

| ID | Section | Fix summary |
|---|---|---|
| RoF-13-01-BASELINE | Global | review_of_ctl-pinn_framework.md confirmed as single candidate (CAND-02). Vacuous Policy Checks recorded. |
| RoF-13-02-NN | Section <N> (<source>) | <past-tense one-sentence fix description>. |
| ...                | ...                  | ...                                            |
```

**Conventions copied from Phase 12:**
- The first row is always `<PHASE-PLAN>-BASELINE` (Phase 12: `PINN-12-01-BASELINE`, line 358; Phase 11: `DQA-11-01-BASELINE`).
- Subsequent rows are ordered by discrepancy ID, not by severity.
- Fix summary verbs are past-tense and name the concrete change: "Removed duplicate table header row...", "Documented expected pandoc behavior...", "Replaced `\-` markers with plain dashes..." Phase 12 examples at lines 360–362.
- Entries with severity `INFO` and `Fix status: Accepted as-is` still appear in the log (Phase 12 line 359 — `PINN-12-02-01`).

**Phase 13 fix-log seed entries (predicted from RESEARCH.md):**
- `RoF-13-01-BASELINE` (Global) — single-candidate baseline + vacuous policy.
- `RoF-13-02-01..29` (per section) — `\-` escaped-dash list markers replaced with plain `- `.
- `RoF-13-02-NN` (per section) — `\[...\]` escaped prose brackets replaced with `[...]`.
- One entry for the longtable continuation-row deletion in Section 3 (mirrors `PINN-12-02-02`/`-03`).
- One entry per grid-table → GFM conversion if D-29 is enforced (Open Question #1 in RESEARCH.md).

---

## Pattern 4 — Final canonical markdown placement pattern

**Authoritative analog placement decisions:**

| Concern | Phase 12 placement | Phase 13 placement |
|---------|--------------------|--------------------|
| Authoritative file path | `pinn_instruction/markdown_conversion/pinn_architecture.md` | `pinn_instruction/markdown_conversion/review_of_framework.md` (D-43; lowercase_underscore matches source subdir name) |
| Source-of-promotion path | Selected baseline already at the canonical path (no move needed) | `pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md` |
| Promotion mechanism | n/a (top-level winner) — but Phase 11 used `git mv` from `pandoc_conversion/` for this same situation | `git mv pinn_instruction/markdown_conversion/pandoc_conversion/review_of_ctl-pinn_framework.md pinn_instruction/markdown_conversion/review_of_framework.md` per RESEARCH.md "Code Examples" → "Promotion (Wave 3)" and Pitfall 6 |
| `_archive/` directory | Created at `_archive/pinn-architecture/` with README + 2 candidates | NOT CREATED (D-40; CLEAN-02 N/A) |
| Source Issues metadata | Appended at end of authoritative markdown after horizontal rule (`pinn_architecture.md:Source Issues / Notes for Future Reconciliation` section, see `12-03-SUMMARY.md:43-46`) | Same pattern; if no source-level issues during audit, append a single bulleted "No source-level issues identified during Phase 13 audit." |
| Verification report path | `verification_reports/pinn_architecture_verification_report.md` | `verification_reports/review_of_framework_verification_report.md` (D-44; matches D-31 subdir convention) |
| README index row position | Appended after Phase 11 row (line 9 of `markdown_conversion/README.md`) | Append after Phase 12 row (will be line 10) |

**Verified directory layout to replicate (from `pinn_instruction/markdown_conversion/`):**

```
pinn_instruction/markdown_conversion/
├── ctl_instruction.md                            # Phase 10 authoritative
├── data_quality_assessment.md                    # Phase 11 authoritative
├── pinn_architecture.md                          # Phase 12 authoritative
├── review_of_framework.md                        # Phase 13 NEW (D-43)
├── sampling_method.md                            # legacy (pre-v1.3 audit)
├── README.md                                     # 4-column flat index (modify: append row)
├── verification_reports/
│   ├── ctl_instruction_verification_report.md
│   ├── data_quality_assessment_verification_report.md
│   ├── pinn_architecture_verification_report.md
│   └── review_of_framework_verification_report.md   # Phase 13 NEW (D-44)
├── pandoc_conversion/
│   └── review_of_ctl-pinn_framework.md           # SOURCE for Phase 13 promotion (will be moved out)
└── _archive/
    ├── ctl-instruction/
    ├── data-quality-assessment/
    └── pinn-architecture/
    # NO review-of-framework/ subdirectory (D-40)
```

---

## Pattern 5 — Naming conventions

### Plan/SUMMARY filenames

- `<phase_num>-<plan_num>-PLAN.md` — `13-01-PLAN.md`, `13-02-PLAN.md`, `13-03-PLAN.md` (zero-padded; observed in `12-01-PLAN.md`, `11-01-PLAN.md`).
- `<phase_num>-<plan_num>-SUMMARY.md` — `13-01-SUMMARY.md`, etc. (`12-01-SUMMARY.md` etc.)
- Phase-level artifacts: `<phase_num>-CONTEXT.md`, `<phase_num>-RESEARCH.md`, `<phase_num>-PATTERNS.md`, `<phase_num>-VERIFICATION.md`. (Phase 13's `13-CONTEXT.md` and `13-RESEARCH.md` already exist.)

### Phase directory naming

- `.planning/phases/<phase_num>-<kebab-case-name>/` — e.g., `12-pinn-architecture-verification/`, `11-data-quality-assessment-verification/`. Phase 13's directory `13-review-of-framework-verification/` already follows this pattern.

### Discrepancy / fix IDs

- Phase 10: `CTL-...` prefix.
- Phase 11: `DQA-...` prefix; baseline ID `DQA-11-01-BASELINE`; section IDs `DQA-NN-NNN`; source-issue IDs `SI-DQA-NNN`.
- Phase 12: `PINN-12-{plan}-{NN}`; baseline `PINN-12-01-BASELINE`; source-issue IDs `SI-PINN-NNN`.
- **Phase 13 recommended:** `RoF-13-{plan}-{NN}`; baseline `RoF-13-01-BASELINE`; source-issue IDs `SI-RoF-NNN`. (Stable from audit table to fix log per D-12.)

### Authoritative-markdown filenames (lowercase_underscore convention)

- `ctl_instruction.md`, `data_quality_assessment.md`, `pinn_architecture.md`, `sampling_method.md`, **`review_of_framework.md`** (D-43; matches source subdir name `review_of_framework/`).
- Verification reports add `_verification_report.md` suffix to the same stem.
- `_archive/<kebab-case>/README.md` uses kebab-case for the subdirectory name (`pinn-architecture`, `data-quality-assessment`, `ctl-instruction`).

### README index row format

From `pinn_instruction/markdown_conversion/README.md:5-9`:

```markdown
| Source | Authoritative markdown | Verification report | Candidate archive |
|---|---|---|---|
| <Source title> | [`<file>.md`](<file>.md) | [`verification_reports/<file>_verification_report.md`](verification_reports/<file>_verification_report.md) | [`_archive/<kebab>/README.md`](_archive/<kebab>/README.md) |
```

**Phase 13 row** (D-45/D-46 — flat index, parent-dir metadata in source-title cell, NO `_archive` link):

```markdown
| Review of Framework<br>*(LaTeX parent: `review-of-framework/`, shared with Phase 14: stage-strategy-revision)* | [`review_of_framework.md`](review_of_framework.md) | [`verification_reports/review_of_framework_verification_report.md`](verification_reports/review_of_framework_verification_report.md) | N/A — single candidate |
```

The `N/A — single candidate` text is the planner's call (D-46 mandates flat index but doesn't lock the wording). Keep all four columns populated so the table stays rectangular.

---

## Pattern 6 — Anti-patterns to avoid

There is **no `REVISION_LOG.md`** in `.planning/phases/13-*/` or in the Phase 12 directory. The closest course-correction artifacts are:

1. **`12-01-SUMMARY.md:64-71` (Auto-fixed Issues — Rule 3 Blocking):** Files were initially created at project root paths instead of inside the worktree's git copy. Fix: re-create inside the worktree path.
   - **Phase 13 implication:** Plan files must use absolute paths via `@<home>/Desktop/3_body_problem/...` in `<execution_context>` and `<context>` blocks, not relative paths. The executor agent reads in a worktree; the orchestrator runs at the repo root. Keep paths absolute.

2. **`11-REVIEW.md` warnings (WR-01, WR-02, WR-03):** Phase 11's archive contained:
   - 33 unresolved `[?]` placeholder citations in the archived candidate (warning that the audit-fix discipline did not extend into archived files).
   - Disagreement between verification report and archive README on placeholder citation count.
   - Corrupted HTML table in the archived candidate that was not flagged in-file.
   - **Phase 13 implication:** None directly (no archive). But the underlying lesson — **never let two artifacts disagree on the same fact** — applies to the Provenance Note's line count vs `wc -l` output, and to the Vacuous Policy Checks counts vs the actual grep results. Run the greps live during Wave 1 and quote the numbers; do not paraphrase.

3. **Pitfalls in 13-RESEARCH.md (lines 454–584)** — six anti-patterns the planner should bake into the plan files:
   - **Pitfall 1:** Treating Vacuous Policy Checks as implicit (omit the subsection because everything is zero). D-47 mandates the explicit subsection. **Plan-file mitigation:** Wave-1 task `<done>` clause must list the Vacuous Policy Checks subsection as a verifiable artifact, not a comment.
   - **Pitfall 2:** Conflating pandoc artifacts (`\-`, `\[`) with source-level content meant to be preserved per CROSS-01. **Plan-file mitigation:** Wave-2 task `<action>` block must distinguish "source content (preserve)" from "conversion artifact (fix)".
   - **Pitfall 3:** Math-heavy section underaudit (Sections 2 and 5). **Plan-file mitigation:** Section-2 and Section-5 audit subsections require an explicit "Formula checklist" mini-table per D-14 — same shape as Phase 12 lines 205–212 and 237–251.
   - **Pitfall 4:** Skipping cell-by-cell table audit. **Plan-file mitigation:** Section-3 (13-row spec table) and Section-7 (6-row hyperparameter table) need a per-row checklist; the verification report must show MATCH per row, not "Status: PASS" alone.
   - **Pitfall 5:** Subsection heading drift (`####` vs `##` confusion). **Plan-file mitigation:** Wave-1 records a heading map (`\section`→`#`, `\subsection`→`##`, `\paragraph`→`####`) once; Wave-2 audits cite the map.
   - **Pitfall 6:** Promotion path ambiguity (`git mv` vs `cp + delete`). **Plan-file mitigation:** Wave-3 Task 1 specifies `git mv` literally in the `<action>` block, with the exact source/target paths.

4. **Bulk find/replace anti-pattern (RESEARCH.md line 419):** Do not bulk find/replace `\-` or `\[ \]` across the candidate. Apply section-scoped fixes per D-20. Some `\[ \]` may legitimately appear inside code fences or display-math contexts where the escape is correct.
   - **Plan-file mitigation:** Wave-2 task `<action>` block names "section-scoped fix" verbatim, mirroring Phase 12 Plan-2 Task 1 step "apply a small section-scoped fix to pinn_architecture.md (per D-20)" (`12-02-PLAN.md:120`).

5. **Re-running pandoc anti-pattern (RESEARCH.md lines 405–407):** REQUIREMENTS.md "Out of Scope" forbids re-running pandoc on the candidate. Any manual fixes already in the candidate would be discarded.
   - **Plan-file mitigation:** Plan files must NOT include any pandoc invocation in `<action>` blocks. The `pandoc 3.7.0.2` line in RESEARCH.md "Standard Stack" is reference-only.

6. **Editing LaTeX source anti-pattern:** LaTeX is ground truth (D-13). All fixes go into the markdown.
   - **Plan-file mitigation:** The `files_modified:` YAML list in every Wave-2 plan must NOT include any path under `pinn_instruction/original_latex/`. Phase 12's Wave-2 list (`12-02-PLAN.md:7-9`) is `[pinn_architecture.md, pinn_architecture_verification_report.md]` only.

---

## Summary for the planner

- **Mirror Phase 12 plan files directly** for shape (YAML front-matter, `<objective>`/`<execution_context>`/`<context>`/`<tasks>`/`<verification>`/`<success_criteria>`/`<output>`).
- **Substitute single-candidate adaptations** at three specific points: (a) Plan-1 Task-1 becomes a Provenance Note + Vacuous Policy Checks instead of multi-candidate scoring; (b) Plan-3 drops the archive task entirely; (c) the verification report's heading list swaps `Candidate Comparison` for `Starting Candidate Provenance` and `Excluded Inactive Sections` for `Vacuous Policy Checks`.
- **Use `git mv` for promotion** from `pandoc_conversion/review_of_ctl-pinn_framework.md` to `markdown_conversion/review_of_framework.md` in Wave 3.
- **Discrepancy ID prefix `RoF-13-`** keeps the Phase-12 `<DOC>-<PHASE>-<PLAN>-<NN>` shape.
- **Append the Phase 13 row to `markdown_conversion/README.md` only** (no `_archive/review-of-framework/` directory). Source-title cell carries the parent-dir metadata for Phase 14 discoverability.
- **Source Issues / Notes for Future Reconciliation** is appended to the authoritative markdown verbatim per Phase 12 (`12-03-SUMMARY.md:43-46`), with the no-issues fallback mirroring `12-03-PLAN.md:91`.
