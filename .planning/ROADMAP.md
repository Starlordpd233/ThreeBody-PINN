# Roadmap: 3-Body Problem Codebase Cleanup

## Overview

This cleanup consolidates duplicate IC datasets, updates all code paths and documentation to reference a 2-folder IC layout, then removes redundant data folders and legacy artifacts. The ordering is strict: code rewrites and validation first, documentation second, destructive deletion last. Every active script and doc must resolve correct paths before any folder is removed.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Code Rewrites and Validation** - Rewrite all gold IC paths to base folders, externalize ic_raw references, and make correspondence validation subset-aware (completed 2026-03-18)
- [x] **Phase 2: Documentation Updates** - Update all documentation to reflect the consolidated 2-IC-folder layout and externalized ic_raw behavior (completed 2026-03-19)
- [x] **Phase 3: Data Deletion and Legacy Cleanup** - Remove redundant IC folders, ic_raw, legacy directories, and build artifacts (completed 2026-03-19)
- [ ] **Phase 4: Stale Reference Fixes** - Fix stale code imports, documentation references, and agent file drift missed by phase-level verifiers (gap closure)

## Phase Details

### Phase 1: Code Rewrites and Validation
**Goal**: Every script and validation tool resolves IC paths correctly against the 2 base IC folders, with no references to gold IC folders or in-repo ic_raw
**Depends on**: Nothing (first phase)
**Requirements**: PATH-01, PATH-02, PATH-03, PATH-04, PATH-05, PATH-06, VALD-01, VALD-02
**Success Criteria** (what must be TRUE):
  1. Running `grep -r` for `ic_hierarchical_for_gold_standard` and `ic_standard_quasi_random_for_gold_standard` across active scripts returns zero matches
  2. Running `grep -r` for `ic_hierarchical_gold_` and `ic_standard_gold_` filename patterns across active scripts returns zero matches
  3. Stage 1/2 scripts accept an `IC_RAW_DIR` environment variable and do not contain hardcoded `simulation_data/Data/ic_raw/` paths
  4. Correspondence validation for standard_gold correctly excludes the 184 known IDs without false failures, and the 184-ID exclusion list exists at `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`
**Plans**: 3 plans in 2 waves

Plans:
- [x] 01-01: Update config.py and naming.py gold IC paths to base folders (Wave 1)
- [x] 01-02: Update debug scripts and add IC_RAW_DIR to Stage 1/2 scripts (Wave 2)
- [x] 01-03: Add 184-ID exclusion loading to correspondence.py (Wave 2)

### Phase 2: Documentation Updates
**Goal**: All documentation accurately describes the consolidated 2-IC-folder layout, externalized ic_raw, and the 184-ID subset relationship
**Depends on**: Phase 1
**Requirements**: DOCS-01, DOCS-02, DOCS-03, DOCS-04
**Success Criteria** (what must be TRUE):
  1. `DATASET_DOCUMENTATION.md` describes exactly 2 IC folders under `ic_final/`, explains ic_raw removal, and documents the 184-ID subset relationship
  2. Root `README.md` and `simulation_data/Documentation/README.md` reference only `ic_hierarchical/` and `ic_standard_quasi_random/` as IC folders
  3. All agent instruction files (`CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `ANTIGRAVITY.md`) dataset inventory sections list only 2 IC folders and note externalized ic_raw
**Plans**: 3 plans in 2 waves

Plans:
- [x] 02-01: Update DATASET_DOCUMENTATION.md for 2-folder layout, ic_raw externalization, 184-ID reference (Wave 1)
- [x] 02-02: Update README.md files for consolidated IC layout (Wave 2)
- [x] 02-03: Update all 4 agent instruction files with identical Section 3.2 (Wave 2)

### Phase 3: Data Deletion and Legacy Cleanup
**Goal**: All redundant IC folders, ic_raw, legacy directories, and build artifacts are removed from the filesystem
**Depends on**: Phase 1, Phase 2
**Requirements**: DEL-01, DEL-02, DEL-03, CLN-01, CLN-02, CLN-03, CLN-04
**Success Criteria** (what must be TRUE):
  1. Only `ic_hierarchical/` and `ic_standard_quasi_random/` exist under `simulation_data/Data/ic_final/` — no `_for_gold_standard` folders remain
  2. `simulation_data/Data/ic_raw/` does not exist
  3. `paper_templates/old_templates/` and `brutus_simulation_documentation/` do not exist
  4. No `__pycache__/` directories exist in project scope (outside `.venv/`, `.git/`, `reference-code/`), and no stray LaTeX build artifacts (`.synctex.gz`, `.aux`, `.fls`, `.fdb_latexmk`, `.out`) remain
**Plans**: 2 plans in 1 wave

Plans:
- [x] 03-01: Clean code references and delete redundant IC/ic_raw data directories (Wave 1)
- [x] 03-02: Remove legacy directories, purge build artifacts, update STRUCTURE.md (Wave 1)

### Phase 4: Stale Reference Fixes
**Goal**: All stale code imports, documentation filename references, and agent instruction file drift from Phase 1 renames and Phase 3 deletions are resolved
**Depends on**: Phase 1, Phase 2, Phase 3
**Requirements**: PATH-06, DOCS-02, DOCS-04
**Gap Closure**: Closes gaps from v1.0 milestone audit
**Success Criteria** (what must be TRUE):
  1. `test_pipeline.py` imports `ic_generation_utils` (not `FINAL_ic_generator_enhanced`) and runs without `ModuleNotFoundError`
  2. `generate_ics.py` print statements reference `$IC_RAW_DIR` path, not `ic_raw_datasets/`
  3. `simulation_data/Documentation/README.md` has zero references to `FINAL_ic_generator_enhanced.py`, `generate_enhanced_ics.py`, or unqualified `Data/ic_raw/`
  4. `AGENTS.md` Section 3.2 matches CLAUDE.md/GEMINI.md/ANTIGRAVITY.md (2 IC folders, IC_RAW_DIR, no `_for_gold_standard`)
  5. All agent instruction files and root README.md reference `ic_generation_utils.py` and `generate_ics.py` (renamed filenames)
  6. REQUIREMENTS.md checkboxes for PATH-04, PATH-05, PATH-06, VALD-01, VALD-02 are marked `[x]`
**Plans**: 2 plans in 1 wave

Plans:
- [ ] 04-01-PLAN.md — Fix stale code references and documentation filenames (PATH-06, DOCS-02)
- [ ] 04-02-PLAN.md — Update agent instruction files and REQUIREMENTS.md bookkeeping (DOCS-04)

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Code Rewrites and Validation | 3/3 | Complete   | 2026-03-18 |
| 2. Documentation Updates | 3/3 | Complete | 2026-03-19 |
| 3. Data Deletion and Legacy Cleanup | 2/2 | Complete | 2026-03-19 |
| 4. Stale Reference Fixes | 0/2 | Planned | — |
