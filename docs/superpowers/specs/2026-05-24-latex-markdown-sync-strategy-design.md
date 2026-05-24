---
title: LaTeX-Markdown Sync Strategy
date: 2026-05-24
status: draft (pending user approval)
scope: cross-milestone (v1.4, v1.5, v1.6, v1.6.5-latex-sync)
authors: [user, claude]
---

# LaTeX-Markdown Sync Strategy

## Purpose

Establish a sustainable workflow for keeping `pinn_instruction/original_latex/framework-specs/` `.tex` sources usable as documentation, given that v1.4+ phase work edits only the corresponding markdown sources at `pinn_instruction/markdown_conversion/framework-specs/`. The repository will accumulate ~3 issue-thematic milestones (v1.4, v1.5, v1.6) of markdown drift; a dedicated milestone (`v1.6.5-latex-sync`) then refreshes the LaTeX derivative.

## Authority direction

**Markdown is the active authoring source. LaTeX is a one-way derivative refreshed during dedicated sync milestones.**

Repo-visible evidence supporting this direction:

- `.planning/milestones/v1.3-ROADMAP.md` (Phases 10–15.1): established each markdown spec as the "authoritative, one-to-one faithful reproduction of its LaTeX source." Multiple phase goal statements (lines 9, 27, 48, 71, 94, 116, 138) use this exact phrasing.
- `docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md` row F: states the LaTeX is "no longer authoritative for v1.4."

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

Frozen baseline mapping markdown heading ranges to LaTeX section files. Provides stable section IDs that drift rows reference. Mostly mechanical to construct: LaTeX `\include`/`\input` order pairs 1:1 with markdown H1 headings; sub-anchors are H2-headings within each parent that deserve stable reference IDs.

**Conventions:**

- **Section ID format**: `{spec-slug}:{section-file-stem}` (kebab-case). Optional sub-anchor: `#{stable-slug}`.
- **Underscore vs hyphen** (intentional): Section IDs use hyphens (`04-phase1-data-prep`); LaTeX filenames preserve original underscores (`04_phase1_data_prep.tex`). Sync agents MUST NOT auto-convert.
- **Per-row `target_tex: none` override**: drift rows may set `target_tex: none` even when section_id maps to a real .tex file. This means the specific change has no LaTeX impact while the section overall still has a counterpart.
- **`:meta` suffix**: reserved for changes truly outside any section (YAML frontmatter, pre-H1 content). NOT used for "no LaTeX impact" — use `target_tex: none` on a real section_id instead.
- **`:preamble` suffix** (reserved): used when an intentional markdown change demands a LaTeX preamble update. Maps to `preamble*.tex`.
- **Cross-cutting commits (post-baseline)**: in Task column, use `cross-cutting/<short-descriptor>` (free-form kebab-case label).
- **Path format for `Target .tex`**: repo-relative paths from repository root. Reserved value `none`.

**Reserved Identifiers table** (per spec):
- `ctl-instruction:meta`, `ctl-instruction:preamble`
- `pinn-architecture:meta`, `pinn-architecture:preamble`
- `sampling-method:meta` (no preamble; packages inlined in monolithic .tex)

**Layout column** (per row in per-spec tables):
- `section-file` (ctl-instruction, pinn-architecture): each row's target is a standalone `.tex` file
- `in-file-section` (sampling-method): single monolithic `.tex` with `\section*{}` boundaries; rows include an in-file anchor (the exact `\section*{...}` heading text)

**Lines (frozen at genesis YYYY-MM-DD)**: per-section line ranges are a frozen snapshot at Genesis. Never maintained as markdown evolves; useful only for archaeology against historical commits near Genesis.

**Active-only filter**: inactive `\input` lines (commented in main `.tex`) are excluded from SECTION-MAP. Inactive `.tex` files exist on disk but are unreachable through SECTION-MAP. Re-activating a dormant section is an explicit decision (uncomment + new rows), never implicit.

**Out of scope for SECTION-MAP**: `framework-revisions/` docs.

**Construction method (for reproducibility):**
1. List LaTeX section files in `\include`/`\input` order from each main `.tex`. List markdown H1 headings (`^# `). Pair 1:1 by order.
2. Verify titles align (allow paraphrase). Flag any mismatch as a gap and stop.
3. For each parent section, list H2 headings inside markdown. Pick which deserve stable sub-anchor IDs (typically: named "Step N" or "Section N.N").

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
- **Status**: `pending` / `synced` / `synced-early` / `synced-hotfix` / `noop`.

**Append-only update rule**: each markdown-touching task creates new row(s) even on a re-visited section. Multiple tasks touching the same section → multiple rows (one per task). The `Status` field is the only mutable cell.

**Lifecycle (LOCKED — five states; no expansion):**
- `pending`: row created; sync not yet performed.
- `synced`: final sync milestone applied the markdown→LaTeX edit and rebuilt PDF.
- `synced-early`: PERMANENT TERMINAL HISTORICAL STATUS. Once set by interim partial sync, never transitions further. Records that an interim sync was performed on that section.
- `synced-hotfix`: set by an authorized hotfix commit (touches markdown + .tex + drift row in one commit).
- `noop`: target_tex=none; no sync action ever required.

**Atomicity rule**: every commit modifying `pinn_instruction/markdown_conversion/framework-specs/*.md` MUST also modify the current milestone's `v1.X-LATEX-DRIFT.md` in the same commit (single-commit pattern).

### Artifact 3 — `.planning/milestones/latex-drift-gates.sh` (canonical verification script)

Header-aware (parses column positions from header row), hard-blocking (returns nonzero on any gate failure), accumulates per-gate failures before exit.

**Invocation:**
```
bash .planning/milestones/latex-drift-gates.sh <SYNC_START> <SYNC_END>
```

Discovers `v1.*-LATEX-DRIFT.md` files in `.planning/milestones/` via glob. Override flag: `--drift-files <f1> <f2> ...`.

Missing future drift files (e.g., v1.5 hasn't started) are treated as zero-row pass-through. Permits the same script to run during v1.4 phase verification.

### Final sync milestone — `v1.6.5-latex-sync`

Standalone GSD milestone. Inputs: SECTION-MAP + all three drift indexes + current markdown + lagging LaTeX. Outputs: updated `.tex` files + rebuilt PDFs + all drift rows terminal + tag `latex-sync-v1`.

**Phase A — Plan & Group.**
- Read SECTION-MAP and all three drift files.
- Group rows by `Target .tex`. For `in-file-section` Layout rows, group includes in-file anchors.
- Output: `.planning/milestones/v1.6.5-latex-sync/SYNC-PLAN.md`.
- Flag overlapping targets (same `(File, Section ID)` across `synced-early` and `pending` rows) for manual review.
- **Close Phase A by tagging `latex-sync-v1-start`** — clean rollback point.

**Phase B-{ctl, pinn-arch, sampling} — Apply + Build-clean (per-spec plans, sequential).**
- For each row (chronological by Source): open target `.tex` (or navigate to in-file anchor for sampling-method), apply semantic content from markdown, fix LaTeX-specific syntax per the authority-split rule.
- **Authority split rule**: markdown is authoritative for semantic content; LaTeX is authoritative for LaTeX-specific syntax and presentation (math environments, `\ref{}` cross-references, theorem environments, table column widths, `\textsubscript{}`, citation keys). When faithful copy produces a LaTeX error, fix at the LaTeX layer with restructuring that doesn't change meaning. If fix would alter semantic meaning, stop and surface a gap.
- **Commit cadence**: per-section-file batching (one apply commit per `.tex` file, batching all drift rows that target it). Build-fix commits are separate and follow.
- **Sequential execution**: the three B-N plans run sequentially in one branch; they share drift files which would merge-conflict on parallel branches.
- **Build-repair recording**: sync-time preamble/build fixes are recorded in `SYNC-PLAN.md` (Build-Repairs Applied subsection) and the sync milestone verification artifact. NOT new drift rows. Drift rows are exclusively for markdown content changes.

**Phase C — Verify, Tag, Close.**
- Run all four gates of `latex-drift-gates.sh`.
- Verify all three PDFs built fresh via `latexmk`; capture evidence in `.planning/milestones/v1.6.5-latex-sync/VERIFICATION.md`.
- Tag `latex-sync-v1`.
- Update `pinn_instruction/markdown_conversion/README.md` and `SECTION-MAP.md` preamble: "Last sync: v1.6.5 (YYYY-MM-DD)."

### Effort estimate

~10–20 hours focused work across 2–4 sessions, dominated by Phase B apply+build-fix loops. Variance dominated by `ctl_instruction.md`, which receives the most edits across content milestones.

## Per-task workflow (active content milestones)

```
1. Implement markdown edit (working tree)
2. Run task verification
3. Self-check: did this task modify framework-specs/*.md?
4. If yes:
   - For each (file, section_id) pair touched, APPEND a new row to v1.X-LATEX-DRIFT.md.
     A single task touching two files produces two rows; a single task touching two
     sections within one file produces two rows. Never edit a pre-existing row.
   - Use SECTION-MAP to resolve section_id and target_tex (repo-relative).
5. Stage the markdown change AND the drift-file change together.
6. Commit once. The commit's diff must contain both.
```

## Verification gates

### Gate 1 — drift-row closure

Every non-`noop` row across all discovered drift files reaches a terminal status. Recovery: classify open rows; route to Phase B-N apply, status correction, or Gate 4 escalation.

### Gate 2 — target-edit coverage by status

| Status | Required range |
|---|---|
| `synced` | `SYNC_START..SYNC_END` |
| `synced-early` | `DRIFT_BASELINE..SYNC_END` |
| `synced-hotfix` | `DRIFT_BASELINE..SYNC_START` |
| `noop` | (no check) |

Recovery: per row, status either wrong (demote to `pending`) or apply work missed (route to Phase B-N).

### Gate 3 — PDF freshness & integrity

All three PDFs exist, non-empty. Mtime is a helper signal only — file system clocks drift, git checkout preserves mtime. Authoritative freshness proof: `latexmk` invocation evidence captured in `.planning/milestones/v1.6.5-latex-sync/VERIFICATION.md` per spec. `.log`/`.fls`/`.aux` files remain gitignored — only excerpts and exit codes are committed via the verification artifact. Recovery: re-run `latexmk -pdf -interaction=nonstopmode`; commit rebuilt PDF; update verification artifact.

### Gate 4 — sync milestone does NOT modify framework-spec markdown (HARD BLOCK)

Zero commits in `SYNC_START..SYNC_END` modify `pinn_instruction/markdown_conversion/framework-specs/*.md`. Recovery: revert violating commits, route the markdown defect through normal content workflow on the appropriate content milestone branch, re-tag `latex-sync-v1-start`, restart range accounting.

## Genesis (turn-on commit)

Single atomic commit producing:

1. `pinn_instruction/markdown_conversion/SECTION-MAP.md` (new) — conventions, reserved IDs (incl. `<spec>:meta` and `<spec>:preamble`), per-spec tables with repo-relative `.tex` paths and Layout column.
2. `.planning/milestones/v1.4-LATEX-DRIFT.md` (new) — preamble pointing at gate script; header row; ~8–9 retro rows for Phases 17/18 + `d3fcff9` noop row.
3. `.planning/milestones/latex-drift-gates.sh` (new) — canonical header-aware verification script.
4. `.planning/PROJECT.md` (edit) — append one Key Decisions table row formalizing the regime.
5. `.planning/REQUIREMENTS.md` (edit) — insert new `## Cross-Milestone Requirements` section between Future Requirements (L60+) and Scope Boundaries (L67) containing `REQ-DOC-01`.
6. `.planning/ROADMAP.md` (edit) — insert v1.6.5 entry in milestones list at L10; append v1.6.5 phase-details subsection.
7. `AGENTS.md` (edit) — insert new `## CRITICAL GOVERNANCE: LaTeX-Markdown Sync Discipline` section after existing v1.4 governance block, before "Git Branch Awareness" block. `CLAUDE.md` and `GEMINI.md` inherit via symlink; no separate edits.
8. `git tag drift-baseline-v1.4 <Genesis-sha>`.

Commit message: `docs(latex-sync): Genesis — establish markdown-authoritative sync regime, SECTION-MAP, drift baseline, governance`.

### Backfill row inventory (Phase 17/18 + d3fcff9)

Approximate rows to be created at Genesis (path examples use repo-relative form):

- Phase 17-01 → ctl_instruction §Step 4 Input Vector → `pinn_instruction/original_latex/framework-specs/ctl-instruction/sections/04_phase1_data_prep.tex`
- Phase 17-02 → pinn_architecture §inference COM projection → `pinn_instruction/original_latex/framework-specs/pinn-architecture/sections/inference_and_output.tex`
- Phase 17-03 cleanup → ctl_instruction (small wording fixes)
- Phase 18-01 (Step 2 unified pipeline) → ctl_instruction §Step 2 → `…/sections/04_phase1_data_prep.tex`
- Phase 18-01 (verify) → pinn_architecture §inference COM projection (prose verify, FRAME-02)
- Phase 18-02 → sampling §Stage 1 hierarchical → `…/sampling-method/sampling_method_instruction.tex` (in-file-section)
- Phase 18-02 → sampling §Stage 2 quasi-random → same target
- Phase 18-02 post-review → sampling §Stage 2 quasi-random → same target
- d3fcff9 cross-cutting → ctl_instruction §appendix#source-issues → target_tex: `none`, status: `noop`

Estimated total: ~8–9 rows.

## Local tooling propagation (FOLLOW-UP, NOT Genesis prerequisite)

Profile-level updates (12 local profiles per session S36) modify user-local agent tooling — out of Genesis scope. The canonical gate script lives in-repo; phase verification works correctly without any local tooling updates.

**Blast-radius warning:**
- Touches workflow `.md` / skill `.md` files only across up to 12 profiles.
- Reversible (snapshot prior content).
- Confirm each profile's GSD version matches source before applying.

**Suggested follow-up task:** `local-tooling-sync-latex-drift-discipline`. Created post-Genesis; runs independent of Phase 19 readiness. Recommended ordering: AFTER Genesis lands, BEFORE Phase 19's first markdown-touching task — so close-out prompts are in place when Phase 19 starts. Phase 19 can begin without it; the in-repo gate script enforces the discipline regardless.

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
6. Genesis pre-conditions on the v1.4 phase pipeline (Genesis can land independently of Phase 19 planning state, my assumption).
7. Local tooling propagation timing (proposed: after Genesis, before Phase 19's first markdown-touching task).

## Cross-references

- v1.3-ROADMAP authority claim: `.planning/milestones/v1.3-ROADMAP.md` Phases 10–15.1
- LaTeX-no-longer-authoritative statement: `docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md` row F
- Hotfix precedent: commit `0708a56`
- Cross-cutting commit example: commit `d3fcff9`
- Active v1.4 governance block (sibling of this design's discipline block): `AGENTS.md` "CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones"
- v1.4 phase summaries (Phases 17, 18) for retro-row backfill source material: `.planning/phases/17-input-and-output-contracts/`, `.planning/phases/18-frame-and-gauge-contracts/`
