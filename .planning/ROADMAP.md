# Roadmap: 3-Body Problem Codebase Cleanup

## Overview

This cleanup consolidates duplicate IC datasets, updates all code paths and documentation to reference a 2-folder IC layout, then removes redundant data folders and legacy artifacts. The ordering is strict: code rewrites and validation first, documentation second, destructive deletion last. Every active script and doc must resolve correct paths before any folder is removed.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Code Rewrites and Validation** - Rewrite all gold IC paths to base folders, externalize ic_raw references, and make correspondence validation subset-aware
- [ ] **Phase 2: Documentation Updates** - Update all documentation to reflect the consolidated 2-IC-folder layout and externalized ic_raw behavior
- [ ] **Phase 3: Data Deletion and Legacy Cleanup** - Remove redundant IC folders, ic_raw, legacy directories, and build artifacts

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
**Plans**: TBD

Plans:
- [ ] 01-01: TBD
- [ ] 01-02: TBD

### Phase 2: Documentation Updates
**Goal**: All documentation accurately describes the consolidated 2-IC-folder layout, externalized ic_raw, and the 184-ID subset relationship
**Depends on**: Phase 1
**Requirements**: DOCS-01, DOCS-02, DOCS-03, DOCS-04
**Success Criteria** (what must be TRUE):
  1. `DATASET_DOCUMENTATION.md` describes exactly 2 IC folders under `ic_final/`, explains ic_raw removal, and documents the 184-ID subset relationship
  2. Root `README.md` and `simulation_data/Documentation/README.md` reference only `ic_hierarchical/` and `ic_standard_quasi_random/` as IC folders
  3. All agent instruction files (`CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `ANTIGRAVITY.md`) dataset inventory sections list only 2 IC folders and note externalized ic_raw
**Plans**: TBD

Plans:
- [ ] 02-01: TBD

### Phase 3: Data Deletion and Legacy Cleanup
**Goal**: All redundant IC folders, ic_raw, legacy directories, and build artifacts are removed from the filesystem
**Depends on**: Phase 1, Phase 2
**Requirements**: DEL-01, DEL-02, DEL-03, CLN-01, CLN-02, CLN-03, CLN-04
**Success Criteria** (what must be TRUE):
  1. Only `ic_hierarchical/` and `ic_standard_quasi_random/` exist under `simulation_data/Data/ic_final/` — no `_for_gold_standard` folders remain
  2. `simulation_data/Data/ic_raw/` does not exist
  3. `paper_templates/old_templates/` and `brutus_simulation_documentation/` do not exist
  4. No `__pycache__/` directories exist in project scope (outside `.venv/`, `.git/`, `reference-code/`), and no stray LaTeX build artifacts (`.synctex.gz`, `.aux`, `.fls`, `.fdb_latexmk`, `.out`) remain
**Plans**: TBD

Plans:
- [ ] 03-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Code Rewrites and Validation | 0/? | Not started | - |
| 2. Documentation Updates | 0/? | Not started | - |
| 3. Data Deletion and Legacy Cleanup | 0/? | Not started | - |
