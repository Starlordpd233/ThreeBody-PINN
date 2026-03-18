# Phase 1: Code Rewrites and Validation - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Every script and validation tool resolves IC paths correctly against the 2 base IC folders (`ic_hierarchical/` and `ic_standard_quasi_random/`), with no references to gold IC folders or in-repo `ic_raw`. Gold-standard simulations are complete — no new gold runs expected. This phase rewrites code only; data deletion happens in Phase 3.

</domain>

<decisions>
## Implementation Decisions

### IC_RAW_DIR Externalization
- Stage 1/2 scripts use `IC_RAW_DIR` environment variable instead of hardcoded absolute paths
- Single env var pointing to parent directory; scripts expect `ic_hierarchical/` and `ic_standard_quasi_random/` subdirectories underneath (same structure as current `ic_raw/`)
- If `IC_RAW_DIR` is not set: raise a clear error with example export command showing expected structure (`export IC_RAW_DIR=/path/to/ic_raw` with note about expected subdirectories)
- No fallback to default path — strict error forces explicit configuration for reproducibility
- Update `FINAL_ic_generator_enhanced.py` default logic (lines 594-600) to check `IC_RAW_DIR`; `generate_enhanced_ics.py` inherits the change automatically since it doesn't override `directory`

### IC Generation File Renaming
- Rename `FINAL_ic_generator_enhanced.py` to `ic_generation_utils.py` (core utilities/library)
- Rename `generate_enhanced_ics.py` to `generate_ics.py` (runner/entry point)
- Update internal import in `generate_ics.py` to reference new module name

### 184-ID Exclusion Handling
- `correspondence.py` loads excluded IDs dynamically at runtime from `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`
- Exclusion list format: simple numbered list, one ID per line (e.g., `0042`), with header explaining context
- Reporting: summary count at end of validation output — "184 IDs excluded per standard_quasi_random_ids_not_in_gold.md (expected subset gap)." No per-ID noise.
- Count guard: if parsed ID count doesn't match expected 184, log WARNING but continue validation — "WARNING: Expected 184 excluded IDs, found N. Exclusion list may be outdated."

### Debug Script Scope
- Update ALL 4 debug scripts that reference gold paths (not just the 2 in PATH-04):
  - `audit_and_backfill_brutus_result_footers.py` (PATH-04)
  - `compare_ic_brutus_files.py` (PATH-04)
  - `debug/renaming/rename_ic_hierarchical_gold.py`
  - `debug/renaming/rename_ic_standard_gold.py`
- Include a full codebase grep sweep as a planning task to catch any references outside explicitly listed scripts (notebooks, documentation, imports)
- For `prescreening_utils.py` (PATH-06): let planner/researcher check if it actually references `ic_raw` before deciding whether to update

### Filename Pattern Transition
- Gold runs are complete — no new gold-standard simulations expected
- Scripts update to reference base IC folders only; gold IC folders are no longer accessed by any script after Phase 1
- Let planner/researcher investigate actual filenames in gold folders to determine if any renaming logic is needed in code
- Phase 3 deletes orphaned gold folders

### Config Centralization
- Keep path resolution separate: `config.py` stays scoped to validation (`dataset_readiness_checks/`), pipeline scripts maintain their own path logic + `IC_RAW_DIR`
- No new shared paths module — avoid coupling between unrelated scripts
- `config.py` keeps 4 dataset variants (hierarchical, hierarchical_gold, standard, standard_gold) but updates gold variant `ic_dir` entries to point to base IC folders instead of `_for_gold_standard` folders
- Gold variants still needed because Brutus output folders are separate (`brutus_hierarchical_gold_standard/` etc.)

### Verification Approach
- Run 4 grep-based success criteria to confirm zero gold/ic_raw references in active scripts
- Run `correspondence.py` for `standard_gold` variant to verify 184-ID exclusion works without false failures
- Separate full codebase grep sweep as a distinct verification step (broader patterns to catch edge cases outside explicitly listed scripts)

### Claude's Discretion
- Exact error message wording for IC_RAW_DIR
- How to parse IDs from the markdown exclusion list file
- Whether `prescreening_utils.py` and `analysis/utils.py` need IC_RAW_DIR updates (check actual references)
- Internal refactoring approach for each script (preserve public API, change internals)
- Order of script updates within the phase

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Path Configuration (validation system)
- `simulation_data/Validation/dataset_readiness_checks/config.py` — Centralized dataset variant definitions, IC/Brutus path resolution, filename patterns. Lines 48-75 define the 4-variant mapping that needs gold IC paths updated.
- `simulation_data/Validation/dataset_readiness_checks/utils/naming.py` — Directory-to-variant mapping, filename pattern matching. `map_directory_to_variant()` at lines 165-181 needs gold folder entries updated.

### Correspondence Validation
- `simulation_data/Validation/dataset_readiness_checks/modules/correspondence.py` — Correspondence validation logic. Lines 17-110 for main validation, lines 113-138 for blacklist/exclusion handling. Needs 184-ID subset awareness.
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` — 184-ID exclusion list (to be created by VALD-02). correspondence.py will parse this at runtime.

### IC Generation
- `simulation_data/Scripts/ic_generation/FINAL_ic_generator_enhanced.py` — Core IC generator with hardcoded ic_raw paths at lines 594-600. To be renamed to `ic_generation_utils.py`.
- `simulation_data/Scripts/ic_generation/generate_enhanced_ics.py` — Runner script that imports from FINAL_ic_generator. To be renamed to `generate_ics.py`.

### Prescreening
- `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` — Prescreener with hardcoded ic_raw absolute paths at lines 42, 47.

### Debug Scripts
- `simulation_data/Scripts/debug/compare_ic_brutus_files.py` — Gold path references at lines 32-37.
- `simulation_data/Scripts/debug/renaming/rename_ic_hierarchical_gold.py` — Gold folder reference at line 5.
- `simulation_data/Scripts/debug/renaming/rename_ic_standard_gold.py` — Gold folder reference at line 5.

### Brutus Runners
- `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` — Gold IC_DIR at lines 34-36, output filename pattern at line 108.

### Dataset Documentation
- `simulation_data/Documentation/DATASET_DOCUMENTATION.md` — Dataset spec and anomalies (source of truth per CLAUDE.md)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `config.py`: Already has `get_ic_dir()`, `get_brutus_dir()`, `get_ic_pattern()` accessors — just need path values updated, not new code
- `naming.py`: Has `extract_file_numbers()`, `map_directory_to_variant()` — update mappings, reuse existing logic
- `correspondence.py`: Has `is_blacklisted()` function (lines 113-138) that already handles variant-to-blacklist mapping — extend for 184-ID exclusion

### Established Patterns
- Pipeline scripts use hardcoded absolute paths (no config import pattern) — maintain this, just swap to IC_RAW_DIR
- Validation system centralizes through `config.py` — gold path updates go through config, not individual validation modules
- File numbering extraction uses regex/string parsing — same pattern for parsing exclusion list

### Integration Points
- `config.py` → all validation modules (`correspondence.py`, etc.) via `get_ic_dir()`, `get_brutus_dir()`
- `generate_ics.py` → `ic_generation_utils.py` via `continuation_enhanced_ic_generation()` import
- Exclusion list `.md` file → `correspondence.py` at runtime (new integration point)

</code_context>

<specifics>
## Specific Ideas

- User wants the IC generation files renamed for clarity: utility vs runner should be obvious from filename
- Error message for missing IC_RAW_DIR should include a concrete `export` command example
- Full codebase grep sweep should be a separate verification task, not combined with success criteria checks

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-code-rewrites-and-validation*
*Context gathered: 2026-03-18*
