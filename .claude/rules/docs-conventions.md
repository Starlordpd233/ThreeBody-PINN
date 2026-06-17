## Docs/ Folder Conventions

**Full authoritative rules:** `docs/README.md`. This file summarizes the rules agents must follow when writing to `docs/`.

### Directory taxonomy

| Path | Purpose |
|---|---|
| `docs/runbooks/` | Operational procedures (migration, maintenance, EDL) |
| `docs/work/plans/<milestone>/<phase>/` | Implementation, remediation, execution plans |
| `docs/work/reviews/<milestone>/<phase>/` | Reviews, audits, critiques, verification reports |
| `docs/work/designs/<milestone>/<phase>/` | Design docs, strategy alternatives (pre-implementation) |
| `docs/archive/` | Approved-retention files only (mirrors active structure) |

Milestone nesting: `milestone_v<m#>/<phase-number>-<topic>/` or `cross_cutting/<topic>/`.

### Frontmatter schema (required for all new files under docs/work/)

```yaml
---
status: active | consumed | retirement-proposed | archived | retained
purpose: implementation-plan | review-findings | verification-report | design | runbook | governance | migration | other
created: YYYY-MM-DD
milestone: v#.# (or "untracked")
phase: <slug> (or "cross-cutting")
retirement_trigger: <when this file is no longer needed>
---
```

Invalid status values: `complete`, `completed`, `done`, `draft`, `wip`, or any qualified string.

### Prohibited actions

- Do NOT create new files in legacy paths: `docs/superpowers/`, `docs/user_plans/`, `docs/plans/`, `docs/findings/`, `docs/migration/`, `docs/brainstorms/`.
- Do NOT nest plans inside designs (`docs/work/designs/plans/`) or vice versa.
- Do NOT create folders named after agents, skills, workflows, or tools.
- Do NOT use dash-encoded phase numbers — `20.5` not `20-5`.
- Do NOT use bare filenames: `review1.md`, `final.md`, `notes.md`, filenames with spaces.
- Do NOT delete, move, or archive docs files without the full audit-and-approval process in `docs/README.md`.
- Do NOT move docs artifacts outside `docs/`.

### Before writing any file to docs/

1. Confirm the target directory matches the purpose (plans → plans/, reviews → reviews/, designs → designs/).
2. Confirm the target directory is NOT a legacy path.
3. Include the full frontmatter block.
4. Use a date-prefixed filename: `YYYY-MM-DD-<descriptive-slug>.md`.
