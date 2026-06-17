# Docs Folder Guidelines

This folder contains project documentation and lifecycle-managed work artifacts. Keep it organized by document purpose, not by which agent, skill, or workflow created the document.

Everything already inside `docs/` stays governed inside `docs/`. Do not move a `docs/` artifact into `.planning/`, `pinn_instruction/`, source code folders, or another non-docs location as part of cleanup. If content from a docs artifact must become canonical elsewhere, that is separate user-approved work; the original docs artifact must still be retired through the lifecycle rules below.

## Core Rules

- Use purpose-based folders. A plan is a plan, even if Superpowers, GSD, a user prompt, or another agent produced it.
- Do not create new folders named after an agent, skill, workflow, or tool unless the folder documents that tool itself.
- Keep the root of `docs/` sparse. Root-level files should be durable entry points or project-wide guidance.
- New temporary work artifacts belong under `docs/work/`.
- Work artifacts are deletion candidates after they have served their purpose, but deletion always requires an audit, a proposal, and explicit user approval.
- Review and finding documents require finding-by-finding closeout before deletion can be proposed.
- Archive is for approved retention, not for dumping stale files.
- Phase numbers in docs names and paths use decimals, not dash-encoded decimals. Use `20.5`, not `20-5`, `20_5`, or `20p5`.

## Directory Layout

Preferred structure for new docs:

```text
docs/
  README.md
  git-guidelines.md

  runbooks/
    EDL/
    maintenance/
    migration/

  work/
    plans/
      milestone_v1.4/
        20.5-sampling-coordinate-allocation/
    reviews/
      milestone_v1.4/
        20.5-sampling-coordinate-allocation/
    designs/
      milestone_v1.4/
        20.5-sampling-coordinate-allocation/

  archive/
    README.md
    work/
      plans/
      reviews/
      designs/
    runbooks/
```

The legacy path names `docs/plans/`, `docs/findings/`, `docs/superpowers/`, and `docs/user_plans/` are reserved for already-started work; do not create new content in these paths. Do not add new files there unless you are intentionally completing already-started work in that exact legacy path. Future cleanup should migrate files within `docs/` or retire them only after the reference-audit and approval rules below are satisfied.

## Root Files

The root of `docs/` is for durable, project-wide entry points.

Root should contain:

- `README.md`: these docs-folder rules.
- `git-guidelines.md`: project-wide Git policy referenced by repo governance.
- Rare durable guidance that applies across the whole repository.

Root should not contain:

- Implementation plans.
- Review reports.
- Temporary agent artifacts.
- Migration notes.
- Scratch files.
- One-off design drafts.

## `docs/runbooks/`

Use `docs/runbooks/` for operational procedures that someone may need to execute later.

Examples:

- Migration and restore procedures.
- Environment setup procedures.
- Repeatable maintenance workflows.
- Safety-sensitive operational checklists.

Use subfolders by operation family:

```text
docs/runbooks/migration/
docs/runbooks/setup/
docs/runbooks/maintenance/
```

Runbooks are not automatically deleted after one use. They may still be retired when obsolete, but only through the same audit, proposal, and approval process.

## `docs/work/`

Use `docs/work/` for lifecycle-managed work artifacts. Files here are useful during a task, phase, review, or design discussion, but they are not assumed to be permanent.

Every file under `docs/work/` should be considered a future deletion candidate unless it is explicitly retained or archived.

### `docs/work/plans/`

Use this folder for implementation and execution plans.

Put these here:

- Agent-generated implementation plans.
- User-requested implementation plans.
- Remediation plans.
- Execution plans for docs-specific, repo-specific, or cross-cutting work.
- Phase or milestone plans that do not already belong to an active GSD phase artifact.

Do not put these here:

- Review findings.
- Audit reports.
- Final project guidance.
- Canonical framework specs.

Lifecycle proof for plans is lightweight. Before proposing deletion, an agent must show that the plan was executed, superseded, or absorbed, and that the file is no longer referenced.

### `docs/work/reviews/`

Use this folder for reviews, audits, critiques, verification reports, and any document that contains findings.

Put these here:

- Plan reviews.
- Code reviews.
- Spec reviews.
- Audit reports.
- Verification and reverification reports.
- Critique documents with actionable findings.

Review documents have a stricter lifecycle. Before proposing deletion, an agent must perform finding-by-finding closeout.

Each finding or major concern must be classified as one of:

- `addressed`
- `superseded`
- `not applicable`
- `open`

Each non-open item must cite the artifact, file, commit, or decision that resolves it. If any material finding remains `open`, the review document cannot be proposed for deletion.

### `docs/work/designs/`

Use this folder for design and brainstorming artifacts that are not canonical project specs.

Put these here:

- Design docs created before implementation planning.
- Strategy alternatives.
- Design reviews focused on direction rather than defect findings.
- Requirements or brainstorm artifacts whose purpose is to shape later work.

Do not put these here:

- Canonical framework specs.
- Finding-bearing review reports.
- Final governance rules.

Design docs can be deletion candidates after their decisions have been accepted, rejected, superseded, or absorbed into a later artifact.

## Milestone And Phase Paths

When a work artifact belongs to a milestone or phase, nest it by milestone and phase under the purpose folder.

Use:

```text
docs/work/plans/milestone_v1.4/20.5-sampling-coordinate-allocation/
docs/work/reviews/milestone_v1.4/20.5-sampling-coordinate-allocation/
docs/work/designs/milestone_v1.4/20.5-sampling-coordinate-allocation/
```

Do not use dash-encoded decimal phase numbers:

```text
20.5-sampling-coordinate-allocation/   # correct (dot notation, not dash)
```

For integer phases, use the integer phase number:

```text
20-architecture-and-normalization-cleanup/
22-framework-spec-cleanup/
```

For cross-cutting work that is not tied to a milestone or phase, use:

```text
docs/work/plans/cross_cutting/<topic>/
docs/work/reviews/cross_cutting/<topic>/
docs/work/designs/cross_cutting/<topic>/
```

## File Naming

Use dated, descriptive, lowercase filenames:

```text
YYYY-MM-DD-<phase-or-topic>-<artifact-kind>.md
```

Examples:

```text
2026-06-06-phase-20.5-plan-remediation-plan.md
2026-06-06-phase-20.5-plan-audit-report.md
2026-06-05-git-guideline-design.md
```

Avoid:

- `review1.md`
- `review2.md`
- `final.md`
- `notes.md`
- `previous_reports/`
- filenames with spaces
- phase numbers like `20-5` when the intended phase is `20.5`

Use `.md` for new documentation unless there is a specific reason to preserve another format.

## Lifecycle Metadata

New files under `docs/work/` should include a small frontmatter block:

```md
---
status: active
purpose: implementation-plan
created: 2026-06-07
milestone: v1.4
phase: 20.5-sampling-coordinate-allocation
retirement_trigger: work completed and reference audit passes
---
```

Allowed statuses:

- `active`: still needed for current or upcoming work.
- `consumed`: served its immediate purpose, but not yet proposed for deletion.
- `retirement-proposed`: audited and proposed for deletion or archive; waiting for user approval.
- `archived`: retained in `docs/archive/` after approval.
- `retained`: intentionally kept active or historical after review.

Allowed purposes:

- `implementation-plan`
- `review-findings`
- `verification-report`
- `design`
- `runbook`
- `governance`
- `migration`
- `other`

### Execution Provenance (plans)

Implementation and remediation plans additionally record execution provenance, set by the commit-behavior rules in `git-guidelines.md`:

- `execution_status`: `not-executed` (default; may be omitted), `first-pass-complete`, or `remediation-pass-N-complete`.
- `executed_at`: timestamp of the latest execution pass, with date, time, and timezone.
- `review_status`: `none` (default), `pending`, or `reviewed`.

These describe execution provenance and are orthogonal to the retention `status` key above. For commit cadence, report retention, and the marker trailers, see `git-guidelines.md` (Docs Plan-Review-Fix Lifecycle).

After an agent uses any file in `docs/` and finishes the work that depended on it, the agent must make an explicit lifecycle decision:

- Keep it `active`, with a reason.
- Mark it `consumed`, if it served its purpose but deletion has not been proposed.
- Mark it `retirement-proposed`, with audit evidence.
- Move it to `docs/archive/` only after approval.
- Delete it only after audit, proposal, and explicit user approval.

For legacy files without frontmatter, an agent may add a short lifecycle note near the top during cleanup or leave the status decision in the deletion or archive proposal.

## Deletion Policy

Deletion is the default retirement outcome for temporary implementation artifacts, but deletion is never automatic.

Before deleting any docs file, an agent must:

1. Confirm the document has served its purpose.
2. Run a reference audit across the repository.
3. For review documents, perform finding-by-finding closeout.
4. Prepare a deletion proposal.
5. Wait for explicit user approval.
6. Delete only the approved files.

If the user does not approve deletion, the file must remain in `docs/` and should be marked `active`, `retained`, or `archived`, depending on the user's instruction.

## Reference Audit Before Deletion

No docs file may be deleted until an agent can show that it is not still used, referenced, or tied to other project artifacts.

The audit must check at least:

- Exact path references.
- Markdown links.
- Bare filename references.
- Filename stem references.
- Title or heading references when the title is meaningful.
- References from `AGENTS.md`.
- References from `.planning/`.
- References from `pinn_instruction/`.
- References from other docs files.
- References from source code, scripts, manifests, and config files.

Use `rg` and include hidden project folders such as `.planning/`:

```sh
target='docs/work/reviews/milestone_v1.4/20.5-sampling-coordinate-allocation/2026-06-06-phase-20.5-plan-audit-report.md'
base="$(basename "$target")"
stem="${base%.md}"

rg --hidden --glob '!.git/*' -n --fixed-strings "$target" .
rg --hidden --glob '!.git/*' -n --fixed-strings "$base" .
rg --hidden --glob '!.git/*' -n --fixed-strings "$stem" .
```

If references are found, deletion is blocked unless the proposal explains why the references are obsolete or how they will be updated with approval.

## Review Closeout Before Deletion

Review and finding documents require stricter proof than implementation plans.

A deletion proposal for a review document must include:

- The reviewed document path.
- The review document path.
- A list of every finding or major concern.
- Status for each finding: `addressed`, `superseded`, `not applicable`, or `open`.
- Evidence for each non-open finding.
- A statement that no open material findings remain.
- Reference-audit results.

If the review report contains vague or overlapping findings, the agent must consolidate them carefully before closeout and explain the consolidation.

## Deletion Proposal Format

A deletion proposal should include:

```text
Deletion proposal:
- File: <docs path>
- Type: plan | review | design | runbook | other
- Purpose served: <short explanation>
- Replacement or consuming artifact: <path, commit, or decision>
- Reference audit: <commands run and result summary>
- Review closeout: <required for review/finding docs>
- Proposed action: delete
- Approval needed: yes
```

Do not delete the file until the user clearly approves the proposal.

## Archive Policy

Archive only when deletion is not appropriate but the file is no longer active.

Good archive candidates:

- Historical runbooks that still explain an important migration or recovery event.
- Final or consolidated reviews that preserve important provenance.
- Superseded plans that explain why a major correction happened.
- Documents still referenced by active project artifacts.
- Documents the user explicitly asks to retain.

Poor archive candidates:

- Duplicate intermediate plans.
- Review drafts whose findings were fully consolidated elsewhere.
- Scratch notes.
- Files with no remaining references or unique value.
- Local artifacts such as `.DS_Store`.

Archive mirrors the active structure:

```text
docs/archive/work/reviews/milestone_v1.4/20.5-sampling-coordinate-allocation/
docs/archive/work/plans/cross_cutting/git-guidelines/
docs/archive/runbooks/migration/
```

Each archived subtree should include a `README.md` that explains:

- What was archived.
- Why deletion was not chosen.
- What artifact superseded or consumed the archived docs.
- Whether the archived docs are retained permanently or can be revisited later.

## Cleanup Boundaries

Docs cleanup must not silently change project truth.

- Do not delete, move, or archive docs files without the required audit and approval.
- Do not move docs artifacts outside `docs/`.
- Do not use archive as a dumping ground.
- Do not preserve a stale file just because it was user-authored or agent-authored. Authorship is not the retention criterion.
- Do preserve or archive a file when it still has unresolved findings, active references, or historical value the user has approved.
- Do not create new duplicate buckets such as `docs/superpowers/plans/` or `docs/user_plans/`.

## Prior Legacy Folders (Cleanup Record)

As of a prior cleanup pass, the following legacy folders were retired from the `docs/` tree:

- `docs/plans/`
- `docs/findings/`
- `docs/superpowers/`
- `docs/user_plans/`
- `docs/migration/`

This section is retained as a record of that cleanup. Any future cleanup pass must respect the same rules in this README:

- Audit references before proposing deletion.
- Use finding-by-finding closeout for reviews.
- Ask for approval before deletion.
- Keep all docs-folder retirement actions inside `docs/`.
- Migrate legacy docs only to new locations inside `docs/`.
- Use decimal phase numbers for new names and paths.
