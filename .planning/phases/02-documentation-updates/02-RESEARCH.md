# Phase 2: Documentation Updates - Research

**Researched:** 2026-03-19
**Domain:** Documentation updates for consolidated IC layout, externalized ic_raw, and 184-ID subset relationship
**Confidence:** HIGH

## Summary

Phase 2 updates all project documentation to reflect the post-consolidation state: exactly 2 IC folders (`ic_hierarchical/` and `ic_standard_quasi_random/`), externalized `ic_raw` via `IC_RAW_DIR` environment variable, and the 184-ID subset relationship between standard and gold-standard datasets. This is purely a documentation phase - no code modifications are required. All documentation should reflect the post-Phase-3 state where gold IC folders are deleted but gold Brutus output folders remain.

**Primary recommendation:** Update documentation files in order of specificity: DATASET_DOCUMENTATION.md (primary spec) first, then README.md files, then agent instruction files with identical dataset inventory sections.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions

#### ic_raw Externalization Documentation
- Comprehensive explanation in DATASET_DOCUMENTATION.md
- Document the `IC_RAW_DIR` environment variable, expected directory structure, and error behavior
- Include concrete export example: `export IC_RAW_DIR=/path/to/ic_raw` with note about expected subdirectories (`ic_hierarchical/`, `ic_standard_quasi_random/`)
- Explain why ic_raw was externalized (raw ICs are large, user-managed, not tracked in repo)

#### 184-ID Subset Relationship
- Reference the exclusion list file rather than duplicating explanations
- Point to `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` as the canonical source
- Brief note: "184 standard quasi-random IDs are not in the gold subset - see standard_quasi_random_ids_not_in_gold.md for the complete list"
- Single source of truth avoids sync issues

#### Agent Instruction Files
- All 4 files (CLAUDE.md, GEMINI.md, QWEN.md, ANTIGRAVITY.md) get identical dataset inventory sections
- Consistent updates across all agents - easier to maintain
- Update the dataset inventory section to list only 2 IC folders and note ic_raw externalization

#### Directory Trees
- Remove gold IC folders (`ic_hierarchical_for_gold_standard/`, `ic_standard_quasi_random_for_gold_standard/`) from all directory tree listings
- Reflects the post-Phase-3 state - cleaner, no confusing "deleted" annotations
- Gold Brutus output folders remain in trees (they still exist)

#### Gold Brutus Outputs Distinction
- Add explicit note clarifying that gold Brutus output folders still exist
- Explain: "Gold-standard Brutus outputs (brutus_hierarchical_gold_standard/, brutus_standard_quasi_random_gold_standard/) still exist. Only the gold IC input folders were duplicates and have been removed."
- Prevents confusion about why gold outputs exist but gold IC inputs don't

#### Changelog/Update Notes
- Add "Last updated" note to each modified documentation file
- Include brief summary of changes: "Updated 2026-03-19: Consolidated IC layout (removed gold IC folders, externalized ic_raw)"
- Helps readers understand what changed and when

### Claude's Discretion

- Exact wording for each documentation section
- Placement of changelog notes (header vs footer)
- How much of the old gold IC folder content to preserve as historical context vs remove entirely
- Specific section structure for agent instruction files

### Deferred Ideas (OUT OF SCOPE)

None - discussion stayed within phase scope

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DOCS-01 | DATASET_DOCUMENTATION.md describes exactly 2 IC folders, explains ic_raw removal, and documents 184-ID subset relationship | See Section "DATASET_DOCUMENTATION.md Updates" below - specific sections identified |
| DOCS-02 | simulation_data/Documentation/README.md directory tree and tables reflect new 2-folder layout | See Section "README.md Updates" below - directory tree and tables need updates |
| DOCS-03 | Root README.md updated to reference only 2 IC folders | See Section "Root README.md Updates" below - dataset layout section needs update |
| DOCS-04 | Agent instruction files (CLAUDE.md, GEMINI.md, QWEN.md, ANTIGRAVITY.md) dataset inventory sections updated | See Section "Agent Instruction Files Updates" below - identical Section 3.2 updates |

</phase_requirements>

## Standard Stack

### Documentation Tools
| Tool | Purpose | Notes |
|------|---------|-------|
| Markdown | Primary format | All docs use standard markdown |
| Code blocks | Directory trees | Use fenced code blocks with no language specifier |
| Tables | Dataset inventory | Use pipe-delimited tables for file counts |

### No External Libraries Required
This phase involves only text editing of markdown files. No package installations needed.

## Architecture Patterns

### Recommended Documentation Update Order

```
1. DATASET_DOCUMENTATION.md (primary spec)
   - All other docs reference this as source of truth
   - Update first to establish canonical language

2. simulation_data/Documentation/README.md
   - References DATASET_DOCUMENTATION.md
   - Directory tree and pipeline diagrams

3. Root README.md
   - Project overview
   - Links to detailed docs

4. Agent instruction files (CLAUDE.md, GEMINI.md, QWEN.md, ANTIGRAVITY.md)
   - Identical Section 3.2 updates
   - Copy same content to all 4 files
```

### Pattern: Changelog Note Placement

**Recommended:** Place at the top of the file, after the title block but before the table of contents. This ensures visibility without disrupting the document structure.

```markdown
# Document Title

**Last Updated:** YYYY-MM-DD

> **Recent Changes:** Brief summary of what changed

---

## Table of Contents
...
```

### Pattern: Gold IC Folder Removal

When removing gold IC folders from documentation:

1. **Directory trees:** Simply delete the lines referencing gold IC folders
2. **Tables:** Remove rows for gold IC folders, keep gold Brutus output rows
3. **Explanatory text:** Replace 4-folder language with 2-folder language
4. **Add clarification note:** Explain why gold outputs still exist but gold ICs don't

### Anti-Patterns to Avoid

- **Don't** add "DELETED" annotations in directory trees - just remove the lines
- **Don't** keep gold IC folder entries "for historical context" - causes confusion
- **Don't** duplicate the 184-ID list in multiple places - reference the exclusion file
- **Don't** forget to update file counts if they're mentioned in prose

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Changelog format | Custom format per file | Consistent pattern | Easier to maintain |
| 184-ID explanation | Duplicate list | Reference exclusion file | Single source of truth |
| Agent file content | Different sections per file | Identical Section 3.2 | Consistency, maintainability |

## Common Pitfalls

### Pitfall 1: Inconsistent File Counts
**What goes wrong:** Prose mentions file counts that don't match tables
**Why it happens:** Tables updated but surrounding prose wasn't
**How to avoid:** Search for all numeric file counts (e.g., "4,857", "2,749") and verify consistency
**Warning signs:** Tables show one number, prose mentions another

### Pitfall 2: Orphaned Cross-References
**What goes wrong:** Documentation links to gold IC folders that no longer exist
**Why it happens:** Only explicit folder listings were updated, not prose references
**How to avoid:** Grep for all instances of "gold_standard" and "for_gold" in documentation
**Warning signs:** Links or references to deleted folders

### Pitfall 3: Agent File Drift
**What goes wrong:** Agent instruction files have different dataset inventory sections
**Why it happens:** Each file updated independently without synchronization
**How to avoid:** Use exact same text block for Section 3.2 in all 4 files
**Warning signs:** GEMINI.md has different IC folder list than CLAUDE.md

### Pitfall 4: Missing Gold Output Clarification
**What goes wrong:** Users confused why gold Brutus outputs exist but gold ICs don't
**Why it happens:** Documentation removes gold IC folders without explanation
**How to avoid:** Add explicit note: "Gold Brutus outputs exist; gold IC folders were duplicates"
**Warning signs:** Questions about missing gold IC inputs

## Code Examples

### Updated Section 3.2 for Agent Instruction Files

```markdown
### 3.2 Dataset Variants (Folder Defines Variant)
- ICs (2 base folders):
  - `simulation_data/Data/ic_final/ic_hierarchical/`
  - `simulation_data/Data/ic_final/ic_standard_quasi_random/`
- Brutus outputs:
  - `simulation_data/Data/brutus_output/brutus_hierarchical/`
  - `simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/`
  - `simulation_data/Data/brutus_output/brutus_standard_quasi_random/`
  - `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/`

**Note:** Gold-standard Brutus output folders exist, but gold IC input folders have been removed. Gold runs read from the base IC folders. The `*_for_gold_standard` IC folders were duplicates and have been deleted.

**ic_raw externalization:** Raw IC storage is external to the repository. Set `IC_RAW_DIR` environment variable before running Stage 1/2 scripts:
```bash
export IC_RAW_DIR=/path/to/ic_raw  # Expected subdirs: ic_hierarchical/, ic_standard_quasi_random/
```

**Mapping rule**: The numeric ID maps IC to Brutus output. File names do **not** encode "gold"; the folder defines the variant.

**Gold-standard subset note**: Standard quasi-random gold Brutus outputs contain 2,565 files while the base IC folder contains 2,749. 184 IDs were not selected for gold-standard re-simulation - see `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` for the complete list.

**ID gaps**: Intentional and caused by generation continuation, prescreen rejection, and failed Brutus runs.
```

### ic_raw Externalization Documentation Block

```markdown
### ic_raw Externalization

Raw IC storage has been externalized from the repository. The `simulation_data/Data/ic_raw/` directory is no longer tracked in git.

**Configuration:**
```bash
export IC_RAW_DIR=/path/to/your/ic_raw
```

The directory pointed to by `IC_RAW_DIR` must contain:
- `ic_hierarchical/` - Raw hierarchical IC files
- `ic_standard_quasi_random/` - Raw standard quasi-random IC files

**Why externalized:** Raw IC files are large (multi-GB) and user-managed. Externalizing allows users to store raw ICs separately from the tracked repository while maintaining the same script interfaces.

**Error handling:** Stage 1/2 scripts raise a clear error if `IC_RAW_DIR` is not set, including the expected export command and directory structure.
```

### Gold Outputs Clarification Note

```markdown
### Gold-Standard Outputs

Gold-standard Brutus outputs remain in the repository:
- `brutus_hierarchical_gold_standard/` - 4,857 high-resolution trajectories
- `brutus_standard_quasi_random_gold_standard/` - 2,565 high-resolution trajectories

**Note:** The corresponding `ic_*_for_gold_standard/` IC folders were duplicates of the base IC folders and have been removed. Gold-standard runs read from the base IC folders (`ic_hierarchical/` and `ic_standard_quasi_random/`).

For standard quasi-random, 184 IDs in the base folder have no gold-standard counterpart - see `standard_quasi_random_ids_not_in_gold.md` for the list.
```

## State of the Art

| Old Documentation | Current Documentation | When Changed | Impact |
|-------------------|----------------------|--------------|--------|
| 4 IC folders listed | 2 IC folders listed | Phase 2 | Cleaner, no confusion |
| ic_raw in repo | ic_raw externalized | Phase 1 (code), Phase 2 (docs) | User-managed storage |
| No 184-ID documentation | Reference exclusion file | Phase 2 | Explicit subset handling |
| No gold output clarification | Explicit note | Phase 2 | No confusion about gold folders |

**Deprecated/outdated:**
- References to `ic_hierarchical_for_gold_standard/` - folder deleted in Phase 3
- References to `ic_standard_quasi_random_for_gold_standard/` - folder deleted in Phase 3
- References to `simulation_data/Data/ic_raw/` as in-repo directory - now externalized

## Open Questions

1. **Should DATASET_DOCUMENTATION.md changelog be a table or prose?**
   - Current format: Table at bottom
   - Recommendation: Keep existing table format, add new row for 2026-03-19 update

2. **How much historical context to preserve about gold IC folders?**
   - Option A: Remove all mentions, document only current state
   - Option B: Brief note in a "Historical Notes" section
   - Recommendation: Use option A (current state only) with clarification note about why gold outputs still exist

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Manual verification |
| Config file | None |
| Quick run command | `grep -r "for_gold_standard" simulation_data/Documentation/` |
| Full suite command | Multiple grep checks (see below) |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DOCS-01 | DATASET_DOCUMENTATION.md has 2 IC folders, ic_raw note, 184-ID reference | manual | `grep -c "ic_hierarchical_for_gold_standard" simulation_data/Documentation/DATASET_DOCUMENTATION.md` (should return 0) | N/A |
| DOCS-02 | README.md directory tree reflects 2-folder layout | manual | `grep -c "ic_hierarchical_for_gold_standard" simulation_data/Documentation/README.md` (should return 0) | N/A |
| DOCS-03 | Root README.md references only 2 IC folders | manual | `grep -c "for_gold_standard" README.md` (should return 0) | N/A |
| DOCS-04 | All 4 agent files have identical Section 3.2 | manual | `diff <(grep -A 20 "3.2 Dataset Variants" CLAUDE.md) <(grep -A 20 "3.2 Dataset Variants" GEMINI.md)` | N/A |

### Sampling Rate
- **Per task commit:** Verify changed file manually
- **Per wave merge:** Run grep checks on all documentation
- **Phase gate:** All grep checks return 0 for gold IC folder references

### Wave 0 Gaps
None - this is a documentation update phase with manual verification.

## Sources

### Primary (HIGH confidence)
- `.planning/phases/02-documentation-updates/02-CONTEXT.md` - User decisions and constraints
- `simulation_data/Documentation/DATASET_DOCUMENTATION.md` - Current state, sections to update
- `simulation_data/Documentation/README.md` - Current state, directory tree
- `README.md` (root) - Current state, dataset layout section
- `CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `ANTIGRAVITY.md` - Current Section 3.2
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` - 184-ID exclusion list (canonical reference)

### Secondary (MEDIUM confidence)
- `.planning/phases/01-code-rewrites-and-validation/01-CONTEXT.md` - Phase 1 decisions that Phase 2 documents
- `.planning/REQUIREMENTS.md` - Requirement definitions for DOCS-01 through DOCS-04

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Markdown documentation, no external dependencies
- Architecture: HIGH - Clear update order and patterns defined
- Pitfalls: HIGH - Based on common documentation maintenance issues

**Research date:** 2026-03-19
**Valid until:** 30 days (stable documentation phase)

---

## Appendix: Specific Section Updates Required

### DATASET_DOCUMENTATION.md (~828 lines)

**Sections requiring updates:**

1. **Header (line 3):** Update "Last Updated" date
2. **Section 2 "Dataset Variants and Inventory" (lines 47-93):**
   - Remove rows for `ic_hierarchical_for_gold_standard/` and `ic_standard_quasi_random_for_gold_standard/`
   - Update prose to mention 2 IC folders instead of 4
   - Add ic_raw externalization note
   - Add 184-ID subset explanation referencing exclusion file
3. **Section 6.1 "Stage 1: IC Generation" (lines 279-299):**
   - Update `ic_raw` path references
   - Add IC_RAW_DIR documentation
4. **Section 9.5 "Gold Standard Subset is Not Simply a Filter" (lines 544-552):**
   - Update to reference exclusion file
   - Clarify gold IC folder removal
5. **Changelog (lines 818-824):** Add new entry for 2026-03-19

### simulation_data/Documentation/README.md (~378 lines)

**Sections requiring updates:**

1. **Stage 1 Output (line 36-38):** Update `Data/ic_raw/` to note externalization
2. **Stage 2 Output (lines 69-76):** Remove gold IC folders from output list
3. **Dataset Inventory (lines 209-227):** Remove gold IC folder rows from table
4. **Folder Structure (lines 331-378):** Remove gold IC folders from directory tree

### Root README.md (~169 lines)

**Sections requiring updates:**

1. **Current Status Snapshot (lines 12-14):** Update IC folder counts
2. **Dataset Layout section (lines 109-124):** Remove gold IC folder references, add clarification

### Agent Instruction Files (CLAUDE.md, GEMINI.md, QWEN.md, ANTIGRAVITY.md)

**Sections requiring updates:**

1. **Section 3.2 "Dataset Variants (Folder Defines Variant)" (lines 91-108):**
   - Update IC folder list to 2 folders
   - Add ic_raw externalization note
   - Add 184-ID subset reference
   - Add gold outputs clarification
   - Same content for all 4 files