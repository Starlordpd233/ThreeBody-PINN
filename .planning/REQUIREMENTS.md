# Requirements: 3-Body Problem Codebase Cleanup

**Defined:** 2026-03-18
**Core Value:** Every active script, validation tool, and documentation file must correctly resolve IC paths after consolidation

## v1 Requirements

### Code Path Rewrites

- [x] **PATH-01**: `run_brutus_hierarchical_only_mac_gold_standard.py` IC_DIR points to `ic_hierarchical/` instead of `ic_hierarchical_for_gold_standard/`
- [x] **PATH-02**: `config.py` ic_dir entries for both hierarchical_gold and standard_gold point to base IC folders
- [x] **PATH-03**: `naming.py` folder-to-name mappings updated with legacy comments for backwards compatibility
- [ ] **PATH-04**: Debug scripts (`audit_and_backfill_brutus_result_footers.py`, `compare_ic_brutus_files.py`) reference base IC paths instead of gold IC paths
- [ ] **PATH-05**: All gold IC filename assumptions changed from `ic_*_gold_XXXX.txt` pattern to `ic_*_XXXX.txt` pattern
- [ ] **PATH-06**: Stage 1/2 scripts (`stage2_prescreening_revised_auto.py`, `FINAL_ic_generator_enhanced.py`, `prescreening_utils.py`, `analysis/utils.py`, `example_incremental_workflow.py`) use configurable `IC_RAW_DIR` env var instead of hardcoded `simulation_data/Data/ic_raw/` paths

### Validation

- [ ] **VALD-01**: `correspondence.py` handles 184-ID standard_gold subset gap without false failures
- [ ] **VALD-02**: Exclusion list of 184 IDs documented at `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`

### Documentation

- [x] **DOCS-01**: `DATASET_DOCUMENTATION.md` describes exactly 2 IC folders, explains `ic_raw/` removal, and documents 184-ID subset relationship
- [ ] **DOCS-02**: `simulation_data/Documentation/README.md` directory tree and tables reflect new 2-folder layout
- [ ] **DOCS-03**: Root `README.md` updated to reference only 2 IC folders
- [x] **DOCS-04**: Agent instruction files (`CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `ANTIGRAVITY.md`) dataset inventory sections updated

### Data Deletion

- [ ] **DEL-01**: `simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard/` deleted after code rewrites verified
- [ ] **DEL-02**: `simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard/` deleted after code rewrites verified
- [ ] **DEL-03**: `simulation_data/Data/ic_raw/` deleted after code rewrites verified

### Legacy Cleanup

- [ ] **CLN-01**: `paper_templates/old_templates/` directory deleted
- [ ] **CLN-02**: `brutus_simulation_documentation/` directory deleted
- [ ] **CLN-03**: All project `__pycache__/` directories removed (outside `.venv/`, `.git/`, `reference-code/`)
- [ ] **CLN-04**: LaTeX build artifacts (`.synctex.gz`, `.aux`, `.fls`, `.fdb_latexmk`, `.out`) removed from project

## v2 Requirements

### Future Cleanup

- **FUT-01**: Consider `.git/` history pruning via `git gc --aggressive` or BFG
- **FUT-02**: Consider consolidating `pinn_instruction/` from 3 formats to 1

## Out of Scope

| Feature | Reason |
|---------|--------|
| `.git/` pruning | Risky for shared history, user deferred |
| Brutus C++ changes | Integrator is stable, not part of cleanup |
| Archived/debug script deletion | User chose to keep these scripts |
| `pinn_instruction/` consolidation | User chose to keep all 3 formats |
| `Qwen3.5-2B-4bit/` removal | Actively used by user |
| `reference-code/` removal | Actively referenced by user |
| Preflight backups | User handles backups independently |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PATH-01 | Phase 1 | Complete |
| PATH-02 | Phase 1 | Complete |
| PATH-03 | Phase 1 | Complete |
| PATH-04 | Phase 1 | Pending |
| PATH-05 | Phase 1 | Pending |
| PATH-06 | Phase 1 | Pending |
| VALD-01 | Phase 1 | Pending |
| VALD-02 | Phase 1 | Pending |
| DOCS-01 | Phase 2 | Complete |
| DOCS-02 | Phase 2 | Pending |
| DOCS-03 | Phase 2 | Pending |
| DOCS-04 | Phase 2 | Complete |
| DEL-01 | Phase 3 | Pending |
| DEL-02 | Phase 3 | Pending |
| DEL-03 | Phase 3 | Pending |
| CLN-01 | Phase 3 | Pending |
| CLN-02 | Phase 3 | Pending |
| CLN-03 | Phase 3 | Pending |
| CLN-04 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---
*Requirements defined: 2026-03-18*
*Last updated: 2026-03-18 after roadmap creation (compressed from 5 phases to 3 for coarse granularity)*
