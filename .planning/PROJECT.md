# 3-Body Problem Codebase Cleanup

## What This Is

A cleanup and consolidation of the three-body simulation + CTL-PINN training repository. The project has accumulated duplicate IC datasets, transient pipeline data, and legacy build artifacts that inflate the 13 GB codebase. This work removes confirmed redundancies, updates all code paths and documentation, and leaves the repository with a clean, minimal data layout.

## Core Value

Every active script, validation tool, and documentation file must correctly resolve IC paths after consolidation — no broken references, no silent failures.

## Requirements

### Validated

- Hierarchical gold ICs are byte-identical to base hierarchical ICs (4857 files, verified)
- Standard gold ICs are a strict byte-identical subset of standard ICs (2565 of 2749 files, 184 IDs excluded)
- `simulation_data/Data/**` is git-ignored — filesystem backup required before data deletion
- Numeric ID extraction (`split('_')[-1]`) works identically with either naming convention

### Active

- [ ] Consolidate duplicate hierarchical gold IC folder into base `ic_hierarchical/`
- [ ] Consolidate standard gold IC subset into base `ic_standard_quasi_random/`
- [ ] Update all scripts referencing gold IC directories to use base IC folders
- [ ] Externalize `ic_raw/` paths in Stage 1/2 scripts via configurable env var
- [ ] Add subset-aware standard_gold validation (184-ID gap handling)
- [ ] Update all documentation to reflect 2-IC-folder layout
- [ ] Delete `ic_raw/`, both `_for_gold_standard/` IC folders
- [ ] Delete `paper_templates/old_templates/`, `brutus_simulation_documentation/`
- [ ] Clean `__pycache__/` and LaTeX build artifacts

### Out of Scope

- `.git/` pruning or `git gc` — risky for shared history
- Brutus C++ code changes — integrator is stable
- Archived/debug scripts — user chose to keep
- `pinn_instruction/` format consolidation — user chose to keep all formats
- `Qwen3.5-2B-4bit/` model — actively used
- `reference-code/` repos — actively referenced

## Context

- The repository implements a three-body simulation pipeline (Brutus integrator) and CTL-PINN training stack
- Gold-standard runs use identical ICs as normal runs but with tighter Brutus parameters (tol, dt_out)
- The `ic_hierarchical_for_gold_standard/` folder was created by renaming files with a `gold` prefix — content is identical
- The `ic_standard_quasi_random_for_gold_standard/` folder is a 2565-file subset of the 2749-file standard folder
- There is no runner script for standard quasi-random gold standard — provenance is mixed
- `ic_raw/` is the Stage 1 output consumed by Stage 2 prescreening — a transient pipeline artifact
- Detailed cleanup spec exists at `docs/plans/cleaning-3-body.md`

## Constraints

- **Data safety**: `simulation_data/Data/**` is git-ignored. Filesystem backup mandatory before any data deletion.
- **Code-first**: All path rewrites must be complete and verified before any folder deletion.
- **Subset awareness**: Standard gold validation must handle the 184-ID gap explicitly (not conflate with blacklist).
- **No Brutus changes**: `brutus_Newton-main/` is not modified.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Keep 2 IC folders, delete 4 | Gold ICs are duplicates/subsets of base ICs | — Pending |
| Externalize ic_raw via env var | Scripts need configurable raw IC path after in-repo deletion | — Pending |
| Create 184-ID exclusion list | Standard gold is a known subset; validation must be subset-aware | — Pending |
| Backup before delete | Git-ignored data cannot be recovered from git history | — Pending |

---
*Last updated: 2026-03-18 after initialization*
