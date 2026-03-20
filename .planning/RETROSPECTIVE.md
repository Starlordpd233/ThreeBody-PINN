# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — Codebase Cleanup

**Shipped:** 2026-03-20
**Phases:** 4 | **Plans:** 10 | **Sessions:** 3

### What Was Built
- Consolidated IC folders from 4 to 2 (removed duplicate gold IC folders)
- Externalized raw ICs via `IC_RAW_DIR` environment variable
- Added 184-ID gold subset exclusion for standard quasi-random configurations
- Removed legacy directories (`old_templates/`, `brutus_simulation_documentation/`) and build artifacts
- Fixed all stale code imports, documentation references, and agent instruction file drift

### What Worked
- Strict phase ordering (code → docs → deletion) prevented broken references
- Wave-based parallelization of independent plans within phases
- Verification agents caught stale references that phase-level verifiers missed (Phase 4 gap closure)
- Archiving milestone artifacts kept ROADMAP.md and REQUIREMENTS.md at constant size

### What Was Inefficient
- Phase 4 (stale reference fixes) shouldn't have been needed — Phase 1 verifiers should have caught renamed file references in docs and agent files
- Agent instruction file drift (AGENTS.md diverging from CLAUDE.md) happened because Section 3.2 was updated in 3 of 4 files during Phase 2

### Patterns Established
- Phase ordering: code rewrites → documentation → destructive deletion (strict dependency)
- Agent instruction files must be updated identically (all 4 files, same section)
- Verification agents run after phase completion to catch cross-file reference drift
- Milestone archival: roadmap + requirements → `milestones/v{X}-*.md`, originals collapsed/deleted

### Key Lessons
1. Grep-based verification should run across ALL file types (code, docs, agent files) during phase verification, not just code
2. When renaming files, track both import references AND documentation filename mentions separately
3. Agent instruction files with duplicated sections (like Section 3.2) are a maintenance risk — one missed update creates drift

### Cost Observations
- Model mix: primarily sonnet (planning/execution), opus used for verification agents
- Sessions: 3 (spread across 2026-03-18 to 2026-03-20)
- Notable: 10 plans executed with zero regressions; Phase 4 was the only "rework" and it was pre-planned gap closure

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | 3 | 4 | Established GSD workflow: strict phase ordering, wave parallelization, post-phase verification |

### Cumulative Quality

| Milestone | Plans | Verification Score | Regressions |
|-----------|-------|-------------------|-------------|
| v1.0 | 10 | 9/9 (Phase 4) | 0 |

### Top Lessons (Verified Across Milestones)

1. Strict phase dependency ordering (code → docs → deletion) prevents broken references
2. Post-phase verification agents catch what inline verifiers miss
3. Duplicated content across files (agent instruction sections) creates drift risk
