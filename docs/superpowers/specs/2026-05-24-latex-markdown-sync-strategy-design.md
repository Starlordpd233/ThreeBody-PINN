---
title: LaTeX-Markdown Sync Strategy
date: 2026-05-24
status: draft (audit-revised; pending GSD integration decision)
scope: cross-milestone (v1.4, v1.5, v1.6, v1.6.5-latex-sync)
authors: [user, claude]
---

# LaTeX-Markdown Sync Strategy

## Purpose

Establish a sustainable workflow for keeping `pinn_instruction/original_latex/framework-specs/` `.tex` sources usable as documentation while active framework-spec authoring happens in `pinn_instruction/markdown_conversion/framework-specs/`. Pre-Genesis v1.4 history includes some direct LaTeX edits, so Genesis must backfill and classify existing drift instead of assuming LaTeX is uniformly stale. After Genesis, content milestones use markdown-only authoring except for explicitly authorized hotfixes; a dedicated milestone (`v1.6.5-latex-sync`) then refreshes the LaTeX derivative.

## Authority direction

**Markdown is the active authoring source. LaTeX is a one-way derivative refreshed during dedicated sync milestones.**

Repo-visible evidence supporting this direction:

- `.planning/milestones/v1.3-ROADMAP.md` (Phases 10–15.1): established each markdown spec as the "authoritative, one-to-one faithful reproduction of its LaTeX source." Multiple phase goal statements use this or closely equivalent phrasing.
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md` (historically at `docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md`, deleted 2026-05-24) row F: states the LaTeX is "no longer authoritative for v1.4."

This design (its Genesis commit, below) formalizes the operational regime that follows: markdown authoring + deferred LaTeX sync.

## Goals and non-goals

**Goals.**
- Markdown changes are recorded immediately and atomically (no separate bookkeeping step that can be forgotten).
- LaTeX is refreshed in one focused milestone after v1.4 / v1.5 / v1.6 close, producing buildable PDFs.
- Verification gates make missing or wrong sync work mechanically detectable.
- Future milestones (issues 02 and 03) reuse the same machinery without re-design.

**Non-goals.**
- Bidirectional sync (LaTeX → markdown). Not in scope; would require conflict-resolution logic.
- Automated regeneration (pandoc -o into the tree). Explicitly forbidden — would clobber manual LaTeX corrections.
- `framework-revisions/` documents. Out of scope; if a future milestone touches them, that milestone defines its own SECTION-MAP and drift index.
- `pinn/` live code. Remains NOT a grounding source per existing v1.4 governance.

## Architecture (three artifacts, one final sync milestone)

### Artifact 1 — `pinn_instruction/markdown_conversion/SECTION-MAP.md` (built once at Genesis)

Append-only baseline mapping markdown heading ranges to LaTeX section files. Provides stable section IDs that drift rows reference. Construction is evidence-guided rather than positional: LaTeX `\include`/`\input` order and markdown headings are aligned by title and document structure, allowing N:1 and 1:N mappings where the sources differ. Sub-anchors are lower-level headings within each parent that deserve stable reference IDs.

**Conventions:**

- **Section ID format**: `{spec-slug}:{section-file-stem}` (kebab-case). Optional sub-anchor: `#{stable-slug}`.
- **Underscore vs hyphen** (intentional): Section IDs use hyphens (`04-phase1-data-prep`); LaTeX filenames preserve original underscores (`04_phase1_data_prep.tex`). Sync agents MUST NOT auto-convert.
- **Per-row `target_tex: none` override**: drift rows may set `target_tex: none` even when section_id maps to a real .tex file. This means the specific change has no LaTeX impact while the section overall still has a counterpart.
- **`:meta` suffix**: reserved for changes truly outside any section (YAML frontmatter, pre-H1 content). NOT used for "no LaTeX impact" — use `target_tex: none` on a real section_id instead.
- **`:preamble` suffix** (reserved): used when an intentional markdown change demands a LaTeX preamble update. Maps to `preamble*.tex`.
- **Source-issue metadata sections**: markdown-only reconciliation notes get named section IDs (for example, `ctl-instruction:source-issues`) with `Target .tex` = `none`. They are tracked so content changes are visible, but they never create LaTeX sync work.
- **Tex-only entries**: active LaTeX files with no markdown counterpart are listed in SECTION-MAP as `tex-only` rows so sync agents know they are intentional, not missing markdown. They do not create drift rows unless later markdown content targets them.
- **Cross-cutting commits (post-baseline)**: in Task column, use `cross-cutting/<short-descriptor>` (free-form kebab-case label).
- **Path format for `Target .tex`**: repo-relative paths from repository root. Reserved value `none`.

**Reserved Identifiers table** (per spec):
- `ctl-instruction:meta`, `ctl-instruction:preamble`
- `pinn-architecture:meta`, `pinn-architecture:preamble`
- `sampling-method:meta` (no preamble; packages inlined in monolithic .tex)

**Layout column** (per row in per-spec tables):
- `section-file` (ctl-instruction, pinn-architecture): each row's target is a standalone `.tex` file
- `in-file-section` (sampling-method): single monolithic `.tex` with `\section*{}` boundaries; rows include an in-file anchor (the exact `\section*{...}` heading text)
- `tex-only`: active LaTeX section/input exists but no markdown heading maps to it

**Lines (frozen at genesis YYYY-MM-DD)**: per-section line ranges are a frozen snapshot at Genesis. Never maintained as markdown evolves; useful only for archaeology against historical commits near Genesis.

**Active-only filter**: inactive `\input` lines (commented in main `.tex`) are excluded from SECTION-MAP. Inactive `.tex` files exist on disk but are unreachable through SECTION-MAP. Re-activating a dormant section is an explicit decision (uncomment + new rows), never implicit.

**Mutability rule**: existing `Section ID`, `Layout`, and `Target .tex` mappings are frozen after Genesis. SECTION-MAP may append rows for new sections, re-activated dormant `.tex` files, section splits/merges, or newly discovered tex-only entries. Section-title text is informational and may be updated when headings are renamed. Deleted or merged sections keep their historical section IDs; new rows describe the deletion/merge action.

**Out of scope for SECTION-MAP**: `framework-revisions/` docs.

**Construction method (for reproducibility):**
1. List active LaTeX section files from each main `.tex`, excluding commented `\input`/`\include` lines and excluding preamble files unless a `:preamble` row is needed.
2. Extract markdown headings with a fenced-code-block-aware parser. Grep-only `^# ` is forbidden because code comments inside fenced Python/text blocks produce false headings.

   ```python
   in_code_block = False
   for line_number, line in enumerate(open("spec.md"), start=1):
       if line.strip().startswith("```"):
           in_code_block = not in_code_block
       elif not in_code_block and line.startswith("# "):
           print(f"L{line_number}: {line.strip()}")
   ```

3. Align markdown headings to LaTeX targets by title and local context. Allow multiple markdown headings to share one target `.tex`, one markdown heading to cover multiple `.tex` targets, markdown-only metadata headings with `Target .tex` = `none`, and tex-only active inputs with `Layout` = `tex-only`.
4. Verify titles align (allow paraphrase). If a mismatch changes sync semantics, stop and surface a gap; if it is presentation-only, record the mapping note in SECTION-MAP.
5. For each parent section, list lower-level headings inside markdown with the same code-block-aware parser. Pick which deserve stable sub-anchor IDs (typically: named "Step N" or "Section N.N").

### Artifact 2 — `.planning/milestones/v1.X-LATEX-DRIFT.md` (live drift index, one per content milestone)

Append-only table. Maintained during each content milestone. One row per (task, file, section_id) tuple touched by a framework-spec commit.

**Row schema:**

```
| Phase | Plan | Task | File | Section ID | Section Title (info) | Change Summary | Target .tex | Status |
```

- **Phase**: integer phase number, or `cross-cutting` for commits not under any GSD phase.
- **Plan**: e.g., `18-01`, or `—` for cross-cutting.
- **Task**: full task ID (e.g., `18-01-02`), `cross-cutting/<descriptor>` (post-baseline), or short SHA (pre-baseline retro rows).
- **File**: filename of the markdown spec touched (e.g., `ctl_instruction.md`).
- **Section ID**: stable ID from SECTION-MAP (e.g., `ctl-instruction:04-phase1-data-prep#step2-pipeline`).
- **Section Title**: informational current heading text; not load-bearing.
- **Change Summary**: ≤2 sentences. What changed (not why; "why" lives in phase summaries and gap registers).
- **Target .tex**: repo-relative path from repository root, or `none`.
- **Status**: `pending` / `synced` / `synced-early` / `synced-hotfix` / `noop` / `superseded` / `cancelled`.

**Append-only update rule**: each markdown-touching task creates new row(s) even on a re-visited section. Multiple tasks touching the same section → multiple rows (one per task). Row content from `Phase` through `Target .tex` is immutable after creation. The `Status` field is the only mutable cell, and it is updated only during sync operations, authorized hotfixes, cancellation/revert bookkeeping, or correction bookkeeping.

**Lifecycle (LOCKED — seven states; expansion requires a design revision):**
- `pending`: row created; sync not yet performed.
- `synced`: final sync milestone applied the markdown→LaTeX edit and rebuilt PDF.
- `synced-early`: terminal historical status. Records that an interim sync was performed on that section before the final sync milestone. If later found incorrect, the row is marked `superseded`; it does not transition back to `pending`.
- `synced-hotfix`: set by an authorized hotfix commit (touches markdown + .tex + drift row in one commit).
- `noop`: target_tex=none; no sync action ever required.
- `superseded`: terminal correction status. Used when a prior `synced-early` or `synced-hotfix` row was applied to the wrong content, wrong section, or stale markdown version. The correcting work creates a new `pending` row for the same section_id, applies it during sync, and records the reason in `SYNC-PLAN.md`.
- `cancelled`: terminal status for a committed row whose markdown change was later withdrawn or reverted before final sync. The Change Summary or `SYNC-PLAN.md` must identify the cancelling commit or user decision.

**Atomicity rule**: every commit modifying `pinn_instruction/markdown_conversion/framework-specs/*.md` MUST also modify the current milestone's `v1.X-LATEX-DRIFT.md` in the same commit (single-commit pattern). Merge commits do not create duplicate rows when all merged commits already contain drift rows and the merge resolution does not alter framework-spec markdown. Any cherry-pick or merge conflict resolution that changes framework-spec markdown must create or update the destination milestone's drift row in the same commit. Rebase does not change row identity because rows are keyed by phase/plan/task, not final commit SHA.

### Artifact 3 — `.planning/milestones/latex-drift-gates.sh` (canonical verification script)

Header-aware (parses column positions from header row), hard-blocking (returns nonzero on any gate failure), accumulates per-gate failures before exit.

**Invocation (content-milestone mode):**
```
bash .planning/milestones/latex-drift-gates.sh --content-range <BASE_REF> <HEAD_REF> --milestone v1.X
```

This mode is run during GSD phase verification when a phase may have touched `pinn_instruction/markdown_conversion/framework-specs/*.md`. It checks commit-level atomicity: every framework-spec markdown commit in the range also touches the current milestone drift file. Missing future drift files are created by the workflow before the first framework-spec edit in that milestone.

**Invocation (sync-milestone mode):**
```
bash .planning/milestones/latex-drift-gates.sh <SYNC_START> <SYNC_END>
```

`SYNC_START` and `SYNC_END` are git refs (tags or SHAs). The script uses `git log SYNC_START..SYNC_END -- <path>` for target-edit coverage. `DRIFT_BASELINE` is derived from the `drift-baseline-*` tag unless explicitly overridden.

Sync mode discovers `v1.*-LATEX-DRIFT.md` files in `.planning/milestones/` via glob. Override flag: `--drift-files <f1> <f2> ...`. Missing future drift files (e.g., v1.5 hasn't started) are treated as zero-row pass-through.

### Final sync milestone — `v1.6.5-latex-sync`

Standalone GSD milestone. Inputs: SECTION-MAP + all three drift indexes + current markdown + lagging LaTeX. Outputs: updated `.tex` files + rebuilt PDFs + all drift rows terminal + tag `latex-sync-v1`.

**Phase A — Plan & Group.**
- Read SECTION-MAP and all three drift files.
- Group rows by `Target .tex`. For `in-file-section` Layout rows, group includes in-file anchors.
- Output: `.planning/milestones/v1.6.5-latex-sync/SYNC-PLAN.md`.
- Flag overlapping targets (same `(File, Section ID)` across `synced-early` and `pending` rows) for manual review.
- Flag targets whose Genesis backfill noted pre-Genesis direct LaTeX edits. Those sections require reconciliation, not blind markdown overwrite.
- **Close Phase A by tagging `latex-sync-v1-start`** — clean rollback point.

**Phase B-{ctl, pinn-arch, sampling} — Apply + Build-clean (per-spec plans, sequential).**
- For each row in drift-file order (oldest first; ties by Phase/Plan/Task): open target `.tex` (or navigate to in-file anchor for sampling-method), apply semantic content from markdown, fix LaTeX-specific syntax per the authority-split rule.
- **Authority split rule**: markdown is authoritative for semantic content; LaTeX is authoritative for LaTeX-specific syntax and presentation (math environments, `\ref{}` cross-references, theorem environments, table column widths, `\textsubscript{}`, citation keys). When faithful copy produces a LaTeX error, fix at the LaTeX layer with restructuring that doesn't change meaning. If fix would alter semantic meaning, stop and surface a gap.
- **Commit cadence**: per-section-file batching (one apply commit per `.tex` file, batching all drift rows that target it). Build-fix commits are separate and follow.
- **Sequential execution**: the three B-N plans run sequentially in one branch; they share drift files which would merge-conflict on parallel branches.
- **Cross-milestone batching**: if one `.tex` file has rows from multiple drift indexes, the apply commit message names all source milestones (for example, `sync(04_phase1_data_prep): apply v1.4 + v1.5 drift`). The commit still belongs to `v1.6.5-latex-sync`.
- **Build-repair recording**: sync-time preamble/build fixes are appended to `SYNC-PLAN.md` under `Build-Repairs Applied` and copied into the sync milestone verification artifact. They are NOT new drift rows. Drift rows are exclusively for markdown content changes.

**Authority split examples:**
- Display math: markdown `$$...$$` may become `equation`, `align`, or `\[...\]` according to the surrounding LaTeX style; the algebraic statement must not change.
- Inline math: preserve symbols and normalization conventions; use LaTeX syntax fixes such as `\textsubscript{}` only for rendering.
- Tables: markdown table content is semantic; LaTeX column widths, alignment, wrapping, and `tabular` environment choices are presentation.
- Cross-references: markdown anchors map to existing LaTeX `\label{}` / `\ref{}` where available; missing labels are added only when they preserve the same reference target.
- Code listings: markdown fenced-code content is semantic; caption/listing environment choice follows existing LaTeX conventions.
- Footnotes/citations: prose claim and citation key are semantic; citation command form follows the LaTeX bibliography setup.
- Theorem or definition blocks: statement content is semantic; environment choice is LaTeX presentation unless it changes numbering or referenced meaning.

**Phase C — Verify, Tag, Close.**
- Run all four gates of `latex-drift-gates.sh`.
- Verify all three PDFs built fresh via `latexmk`; capture evidence in `.planning/milestones/v1.6.5-latex-sync/VERIFICATION.md`.
- Tag `latex-sync-v1`.
- Update `pinn_instruction/markdown_conversion/README.md` and `SECTION-MAP.md` preamble: "Last sync: v1.6.5 (YYYY-MM-DD)."

### Effort estimate

~25–40 hours focused work across 4–6 sessions, dominated by Phase B apply+build-fix loops. Variance is dominated by `ctl_instruction.md` and `pinn_architecture.md`; `sampling_method.md` is expected to be a smaller share. Retroactive backfill misses are expensive: each missed section can add 2–5 hours of archaeology and correction.

## Per-task workflow (active content milestones)

```
1. Implement markdown edit (working tree)
2. Run task verification
3. Self-check: did this task modify framework-specs/*.md?
4. If yes:
   - If v1.X-LATEX-DRIFT.md does not exist for the active milestone, create it
     by copying the canonical header/preamble from the prior drift file.
   - For each (file, section_id) pair touched, APPEND a new row to v1.X-LATEX-DRIFT.md.
     A single task touching two files produces two rows; a single task touching two
     sections within one file produces two rows. Never edit a pre-existing row's
     immutable cells during content-milestone work.
   - Use SECTION-MAP to resolve section_id and target_tex (repo-relative).
   - If SECTION-MAP has no section_id for a new section, reactivated .tex file,
     split/merge, or deletion, append a SECTION-MAP row in the same task before
     adding the drift row.
5. Run latex-drift-gates.sh --content-range against the task range when available.
6. Stage the markdown change, drift-file change, and any SECTION-MAP change together.
7. Commit once. The commit's diff must contain all relevant files.
```

## Verification gates

### Gate 1 — drift-row closure

Every non-`noop` row across all discovered drift files reaches a terminal status (`synced`, `synced-early`, `synced-hotfix`, `superseded`, or `cancelled`). Recovery: classify open rows; route to Phase B-N apply, status correction, cancellation/supersession note, or Gate 4 escalation.

### Gate 2 — target-edit coverage by status

| Status | Required range |
|---|---|
| `synced` | `SYNC_START..SYNC_END` |
| `synced-early` | `DRIFT_BASELINE..SYNC_END` |
| `synced-hotfix` | `DRIFT_BASELINE..SYNC_START` |
| `noop` | (no check) |
| `superseded` | correcting row must be `synced` in `SYNC_START..SYNC_END` |
| `cancelled` | cancelling/reverting commit or user decision must be recorded |

Recovery: per row, status either wrong (demote to `pending`) or apply work missed (route to Phase B-N).

### Gate 3 — PDF freshness & integrity

Mechanical script check: all three PDFs exist, are non-empty, and have mtimes after `SYNC_START`. Human sign-off check: `latexmk` invocation evidence is captured in `.planning/milestones/v1.6.5-latex-sync/VERIFICATION.md` per spec. `.log`/`.fls`/`.aux` files remain gitignored — only excerpts and exit codes are committed via the verification artifact. Recovery: re-run `latexmk -pdf -interaction=nonstopmode`; commit rebuilt PDF; update verification artifact.

### Gate 4 — sync milestone does NOT modify framework-spec markdown (HARD BLOCK)

Zero commits in `SYNC_START..SYNC_END` modify `pinn_instruction/markdown_conversion/framework-specs/*.md`. Recovery: revert violating commits, route the markdown defect through normal content workflow on the appropriate content milestone branch, re-tag `latex-sync-v1-start`, restart range accounting.

## Genesis (turn-on commit)

Single atomic commit plus one post-commit tag producing:

1. `pinn_instruction/markdown_conversion/SECTION-MAP.md` (new) — conventions, reserved IDs (incl. `<spec>:meta` and `<spec>:preamble`), per-spec tables with repo-relative `.tex` paths and Layout column.
2. `.planning/milestones/v1.4-LATEX-DRIFT.md` (new) — preamble pointing at gate script; header row; computed retro rows for all pre-Genesis framework-spec markdown changes in the v1.4 branch history, including mixed markdown+LaTeX hotfixes.
3. `.planning/milestones/latex-drift-gates.sh` (new) — canonical header-aware verification script.
4. `.planning/PROJECT.md` (edit) — append one Key Decisions table row formalizing the regime.
5. `.planning/REQUIREMENTS.md` (edit) — insert new `## Cross-Milestone Requirements` section between Future Requirements (L60+) and Scope Boundaries (L67) containing `REQ-DOC-01`.
6. `.planning/ROADMAP.md` (edit) — insert v1.6.5 entry in milestones list at L10; append v1.6.5 phase-details subsection.
7. `AGENTS.md` (edit) — insert new `## CRITICAL GOVERNANCE: LaTeX-Markdown Sync Discipline` section after existing v1.4 governance block, before "Git Branch Awareness" block. `CLAUDE.md` and `GEMINI.md` inherit via symlink; no separate edits.
8. Post-commit step: `git tag drift-baseline-v1.4 <Genesis-sha>`.

Commit message: `docs(latex-sync): Genesis — establish markdown-authoritative sync regime, SECTION-MAP, drift baseline, governance`.

### Backfill row inventory (computed at Genesis)

Genesis MUST compute rows from the actual branch state at execution time, not from a static phase list. Use the v1.4 branch-root/pre-phase tag as `BACKFILL_START` and the Genesis parent as `BACKFILL_END`.

Procedure:
1. Enumerate markdown commits:

   ```bash
   git log --reverse --oneline BACKFILL_START..BACKFILL_END -- \
     'pinn_instruction/markdown_conversion/framework-specs/*.md'
   ```

2. For each commit, inspect `git show --stat` and `git show -- <file>` to identify touched framework-spec files and sections using SECTION-MAP.
3. If the same commit also touched target `.tex` and rebuilt PDF evidence exists, classify as `synced-hotfix`; if `.tex` was touched without enough build evidence, keep the row `pending` and add "LaTeX also edited pre-Genesis — reconcile both sources" to Change Summary.
4. Include known mixed hotfix `0708a56` as a `synced-hotfix` row for `pinn_architecture.md` / SQR-SkipResNet-SIREN backbone targeting `pinn_instruction/original_latex/framework-specs/pinn-architecture/sections/sqr_skipresnet_siren_backbone.tex`.
5. Include markdown-only metadata/source-issue commits with `Target .tex` = `none` and `Status` = `noop`.

Expected order of magnitude: ~15–20 rows if Genesis lands after Phases 17–18 only; more if additional v1.4 framework-spec commits land first. Allocate 4–6 hours for archaeology and row classification.

## Local tooling propagation (FOLLOW-UP, NOT Genesis prerequisite)

Profile-level updates (12 local profiles per session S36) modify user-local agent tooling — out of Genesis scope. The canonical gate script lives in-repo; phase verification works correctly without any local tooling updates.

**Blast-radius warning:**
- Touches workflow `.md` / skill `.md` files only across up to 12 profiles.
- Reversible (snapshot prior content).
- Confirm each profile's GSD version matches source before applying.

**Suggested follow-up task:** `local-tooling-sync-latex-drift-discipline`. Created post-Genesis; runs independent of Phase 19 readiness. Recommended ordering: AFTER Genesis lands, BEFORE the next framework-spec markdown-touching task — so close-out prompts are in place when active GSD work resumes. Active phase work can begin without it; the in-repo gate script enforces the discipline regardless.

## Tooling stance (recap)

- Manual LaTeX editing is primary.
- `pandoc` is diagnostic-only. No pandoc output may land in `pinn_instruction/original_latex/`. Section-scale regeneration is forbidden; fragment-scale cribbing for individual LaTeX constructs (a math env, a table row) is permitted with manual transcription. Spirit: if the agent is pandoc-ing entire sections, that's regeneration in disguise — stop and transcribe line-by-line.
- `latexmk -pdf -interaction=nonstopmode` is the build mechanism (matches existing toolchain).
- Git provides atomicity and traceability; the pre-sync tag `latex-sync-v1-start` enables clean rollback.
- No new build system, no CI auto-trigger, no markdown→LaTeX watcher, no editor-specific integrations.

## Remaining user-lock decisions (final acceptance items)

These were surfaced for explicit user confirmation in the brainstorming review; they remain open for the user to override at design-review or implementation-plan time:

1. Milestone slug `v1.6.5-latex-sync` (vs alternatives).
2. Canonical gate-script path `.planning/milestones/latex-drift-gates.sh` (vs alternatives).
3. PROJECT.md Key Decisions row outcome marker wording (`— Active (cross-milestone)` proposed).
4. `REQ-DOC-01` numbering (first in a fresh `REQ-DOC-*` namespace).
5. Genesis-commit-date timing (placeholder `<date>` filled at Genesis execution).
6. GSD integration depth: repo-only governance (`AGENTS.md` + `.planning/*` + gate script) vs also updating local GSD workflow/skill prompts so agents are reminded before planning/execution.
7. Local tooling propagation timing (proposed: after Genesis, before Phase 19's first markdown-touching task).
8. Whether `v1.6.5-latex-sync` should be inserted now as a deferred roadmap milestone, or held as a documented cross-milestone requirement until v1.4 closes.

## Cross-references

- v1.3-ROADMAP authority claim: `.planning/milestones/v1.3-ROADMAP.md` Phases 10–15.1
- LaTeX-no-longer-authoritative statement: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md` (historically at `docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md`, deleted 2026-05-24) row F
- Hotfix precedent: commit `0708a56`
- Cross-cutting commit example: commit `d3fcff9`
- Consolidated review that drove this revision: `docs/superpowers/specs/2026-05-24-latex-sync-strategy-consolidated-review.md`
- Active v1.4 governance block (sibling of this design's discipline block): `AGENTS.md` "CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones"
- v1.4 phase summaries and git history for retro-row backfill source material: `.planning/phases/17-input-and-output-contracts/`, `.planning/phases/18-frame-and-gauge-contracts/`, and the actual `BACKFILL_START..BACKFILL_END` commit range at Genesis time
