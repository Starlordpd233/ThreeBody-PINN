# Phase 2: Documentation Updates - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Update all documentation to accurately describe the consolidated 2-IC-folder layout, externalized ic_raw, and the 184-ID subset relationship. Documentation changes only — no code modifications. Phase 3 deletes data folders after documentation is updated.

</domain>

<decisions>
## Implementation Decisions

### ic_raw Externalization Documentation
- Comprehensive explanation in DATASET_DOCUMENTATION.md
- Document the `IC_RAW_DIR` environment variable, expected directory structure, and error behavior
- Include concrete export example: `export IC_RAW_DIR=/path/to/ic_raw` with note about expected subdirectories (`ic_hierarchical/`, `ic_standard_quasi_random/`)
- Explain why ic_raw was externalized (raw ICs are large, user-managed, not tracked in repo)

### 184-ID Subset Relationship
- Reference the exclusion list file rather than duplicating explanations
- Point to `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` as the canonical source
- Brief note: "184 standard quasi-random IDs are not in the gold subset — see standard_quasi_random_ids_not_in_gold.md for the complete list"
- Single source of truth avoids sync issues

### Agent Instruction Files
- All 4 files (CLAUDE.md, GEMINI.md, QWEN.md, ANTIGRAVITY.md) get identical dataset inventory sections
- Consistent updates across all agents — easier to maintain
- Update the dataset inventory section to list only 2 IC folders and note ic_raw externalization

### Directory Trees
- Remove gold IC folders (`ic_hierarchical_for_gold_standard/`, `ic_standard_quasi_random_for_gold_standard/`) from all directory tree listings
- Reflects the post-Phase-3 state — cleaner, no confusing "deleted" annotations
- Gold Brutus output folders remain in trees (they still exist)

### Gold Brutus Outputs Distinction
- Add explicit note clarifying that gold Brutus output folders still exist
- Explain: "Gold-standard Brutus outputs (brutus_hierarchical_gold_standard/, brutus_standard_quasi_random_gold_standard/) still exist. Only the gold IC input folders were duplicates and have been removed."
- Prevents confusion about why gold outputs exist but gold IC inputs don't

### Changelog/Update Notes
- Add "Last updated" note to each modified documentation file
- Include brief summary of changes: "Updated 2026-03-19: Consolidated IC layout (removed gold IC folders, externalized ic_raw)"
- Helps readers understand what changed and when

### Claude's Discretion
- Exact wording for each documentation section
- Placement of changelog notes (header vs footer)
- How much of the old gold IC folder content to preserve as historical context vs remove entirely
- Specific section structure for agent instruction files

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Documentation to Update
- `simulation_data/Documentation/DATASET_DOCUMENTATION.md` — Primary dataset spec. Must describe 2 IC folders, ic_raw externalization, 184-ID subset. (DOCS-01)
- `simulation_data/Documentation/README.md` — Documentation directory overview. Update directory tree and tables for 2-folder layout. (DOCS-02)
- `README.md` (root) — Project overview. Reference only 2 IC folders. (DOCS-03)
- `CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `ANTIGRAVITY.md` (root) — Agent instruction files. Update dataset inventory sections identically. (DOCS-04)

### Reference Files
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` — 184-ID exclusion list (created in Phase 1). Reference this in docs rather than duplicating.
- `.planning/phases/01-code-rewrites-and-validation/01-CONTEXT.md` — Phase 1 context with ic_raw externalization design decisions

### Prior Phase Context
- Phase 1 established: IC_RAW_DIR pattern, 184-ID exclusion loading in correspondence.py, gold IC folders no longer accessed by scripts

</canonical_refs>

<code_context>
## Existing Code Insights

### Documentation Structure
- `DATASET_DOCUMENTATION.md` is large (34KB) — planner should identify specific sections to update, not rewrite entire file
- `README.md` files have directory trees rendered as code blocks — these need manual updates
- Agent instruction files are nearly identical (~12KB each) — same dataset inventory section can be copied to all 4

### Established Patterns
- Documentation uses markdown with code blocks for directory trees
- Section headers follow consistent hierarchy
- "Last updated" dates are used in some docs

### Integration Points
- Phase 1 created the 184-ID exclusion list file — docs should reference it
- Phase 3 will delete gold IC folders — docs should reflect post-deletion state

</code_context>

<specifics>
## Specific Ideas

- All 4 agent instruction files should have identical dataset inventory sections for consistency
- Changelog notes should be brief but informative — what changed and when
- Gold Brutus output folders are NOT being deleted — this distinction needs to be clear in docs

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-documentation-updates*
*Context gathered: 2026-03-19*