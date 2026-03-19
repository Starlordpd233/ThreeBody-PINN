# Phase 4: Stale Reference Fixes - Research

**Researched:** 2026-03-19
**Domain:** Cross-file reference consistency (code imports, documentation filenames, agent instructions)
**Confidence:** HIGH

## Summary

Phase 4 is a gap closure phase with no new capabilities. It fixes stale references left behind by Phase 1 renames (`FINAL_ic_generator_enhanced.py` to `ic_generation_utils.py`, `generate_enhanced_ics.py` to `generate_ics.py`) and Phase 3 deletions (`_for_gold_standard` IC folders, `ic_raw/` directory). The milestone audit identified 3 partially-satisfied requirements (PATH-06, DOCS-02, DOCS-04) due to references that were missed by phase-level verifiers but caught by the cross-phase integration checker.

The scope is well-bounded: a finite set of files with specific line numbers identified in the audit report. The work divides cleanly into (1) code fixes (broken import in `test_pipeline.py`, stale print in `generate_ics.py`), (2) documentation fixes (`simulation_data/Documentation/README.md`, root `README.md`), and (3) agent instruction file updates (AGENTS.md Section 3.2 + stale filenames in non-3.2 sections of CLAUDE.md, GEMINI.md, ANTIGRAVITY.md, AGENTS.md). There are also secondary stale references in `DATASET_DOCUMENTATION.md`, `run_brutus_both_type_simple.py`, and `pinn_instruction/instructions/sampling_method.md` not flagged in the audit but discovered during research.

**Primary recommendation:** Treat this as a systematic grep-and-replace phase, organized by file type (code first, then documentation, then agent instructions), with a final full-project grep verification to confirm zero remaining stale references.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **QWEN.md Resolution:** Check git history (QWEN.md existed, was updated in Phase 2, then deleted in commit c0c83e4). AGENTS.md is the actual 4th agent instruction file. Update AGENTS.md Section 3.2 to match CLAUDE.md/GEMINI.md/ANTIGRAVITY.md. Update DOCS-04 requirement description to reflect actual set of agent files.
- **Stale Filename Scope:** Fix ALL stale references project-wide, not just the files explicitly flagged in the audit. Old names: `FINAL_ic_generator_enhanced.py` to `ic_generation_utils.py`, `generate_enhanced_ics.py` to `generate_ics.py`. Also fix stale `ic_raw` / `ic_raw_datasets` references.
- **test_pipeline.py Fix:** Fix broken import `from FINAL_ic_generator_enhanced import ...` to `from ic_generation_utils import ...`. Check for other stale references in the same file.
- **generate_ics.py Print Statement:** Fix line 56 print referencing `ic_raw_datasets/` to reflect IC_RAW_DIR externalization pattern.
- **simulation_data/Documentation/README.md Cleanup:** Fix lines 22-23, 25, 70, 272, 349-350. Update filenames, fix Interaction Diagram to show IC_RAW_DIR instead of `Data/ic_raw/`, update Stage 2 Input reference.
- **AGENTS.md Section 3.2 Update:** Apply canonical Section 3.2 content from CLAUDE.md. Must show: 2 IC folders, IC_RAW_DIR externalization note, no `_for_gold_standard` directories. Also fix stale filenames in non-Section-3.2 areas.
- **REQUIREMENTS.md Bookkeeping:** PATH-04, PATH-05, VALD-01, VALD-02 checkboxes already fixed. PATH-06 checkbox will be fixed after this phase. Do NOT backfill SUMMARY frontmatter.

### Claude's Discretion
- Exact ordering of file updates within the phase
- Whether to combine all filename updates into one task or split by file type (code vs docs)
- How to handle any additional stale references discovered during implementation

### Deferred Ideas (OUT OF SCOPE)
- SUMMARY frontmatter `requirements_completed` backfill -- non-blocking bookkeeping, not worth a phase
- `paper_templates/mdpi_template/` residual `.bbl`/`.blg` files -- out of CLN-04 scope, minor
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PATH-06 | Stage 1/2 scripts use configurable IC_RAW_DIR -- **gap: stale references in `test_pipeline.py` and `generate_ics.py`** | Full inventory of stale code references compiled with line numbers; `test_pipeline.py` line 61 broken import, `generate_ics.py` line 56 stale print |
| DOCS-02 | `simulation_data/Documentation/README.md` reflects new 2-folder layout -- **gap: stale filenames and `ic_raw/` in Interaction Diagram** | Lines 22-23, 25, 70, 272, 308, 349-350 identified with exact old/new values |
| DOCS-04 | Agent instruction files dataset inventory sections updated -- **gap: AGENTS.md Section 3.2 not updated, stale filenames in non-3.2 sections** | AGENTS.md Section 3.2 still lists 4 IC folders (lines 94, 96); 4 stale filename occurrences in each of CLAUDE.md, GEMINI.md, ANTIGRAVITY.md, AGENTS.md; canonical Section 3.2 content documented |
</phase_requirements>

## Standard Stack

Not applicable -- this phase involves text replacements in Python scripts and Markdown files. No libraries to install.

**Tools required:**
- Text editor / search-and-replace (handled by Claude's Edit tool)
- `grep -rn` for verification sweeps (handled by Grep tool)
- `git` for committing changes

## Architecture Patterns

### File Organization

The stale references are spread across three categories:

```
Code files (runtime impact):
├── simulation_data/Data/testing_data/test_pipeline.py          # Broken import (ModuleNotFoundError)
├── simulation_data/Scripts/ic_generation/generate_ics.py       # Stale print statement
└── simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py  # Comment-only

Documentation files (no runtime impact):
├── simulation_data/Documentation/README.md                     # 7 stale references
├── README.md (root)                                            # 2 stale references
├── simulation_data/Documentation/DATASET_DOCUMENTATION.md      # 6 stale references (discovered)
└── pinn_instruction/instructions/sampling_method.md            # 1 stale reference (discovered)

Agent instruction files (no runtime impact):
├── AGENTS.md                                                   # Section 3.2 + 4 stale filenames
├── CLAUDE.md                                                   # 4 stale filenames
├── GEMINI.md                                                   # 4 stale filenames
└── ANTIGRAVITY.md                                              # 4 stale filenames
```

### Pattern: Agent Instruction File Consistency

All 4 agent instruction files share identical content in Section 3.2. The canonical version is in CLAUDE.md (lines 91-112). AGENTS.md Section 3.2 (lines 91-107) is the only one NOT yet updated -- it still lists 4 IC folders including 2 deleted `_for_gold_standard` directories.

All 4 agent files have identical stale filenames in 4 non-3.2 locations:
- **Section 3.1** (line ~75): Pipeline stages -- `FINAL_ic_generator_enhanced.py`, `generate_enhanced_ics.py`
- **Section 5.3** (line ~161-169): Sampling notes -- `generate_enhanced_ics.py`
- **Section 7.2** (line ~212-220): Pipeline execution command -- `generate_enhanced_ics.py`
- **Section 10** (line ~273-281): Key files -- `FINAL_ic_generator_enhanced.py`

### Pattern: Replacement Map

| Old Reference | New Reference | Context |
|---------------|---------------|---------|
| `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` | Filename in paths and imports |
| `FINAL_ic_generator_enhanced` | `ic_generation_utils` | Python module name (no .py) |
| `generate_enhanced_ics.py` | `generate_ics.py` | Filename in paths and commands |
| `from FINAL_ic_generator_enhanced import` | `from ic_generation_utils import` | Python import statement |
| `ic_raw_datasets/ic_hierarchical/` | `$IC_RAW_DIR/ic_hierarchical/` (in prints) | Print statement in generate_ics.py |
| `Data/ic_raw/` (Interaction Diagram) | `$IC_RAW_DIR` or externalized note | README diagram |
| `ic_hierarchical_for_gold_standard/` | (remove line entirely) | AGENTS.md Section 3.2 |
| `ic_standard_quasi_random_for_gold_standard/` | (remove line entirely) | AGENTS.md Section 3.2 |

### Anti-Patterns to Avoid
- **Partial grep sweep:** Do NOT rely only on the audit report's line numbers. The audit missed `DATASET_DOCUMENTATION.md` (6 refs), `run_brutus_both_type_simple.py` (1 ref), and `pinn_instruction/instructions/sampling_method.md` (1 ref). Always do a full project grep at the end.
- **Modifying `.planning/` files:** The `.planning/` directory contains historical records (RESEARCH.md, PLAN.md, SUMMARY.md, etc.) that naturally reference old filenames as part of their history. Do NOT modify these.
- **Over-editing DATASET_DOCUMENTATION.md:** This file was marked complete for DOCS-01 in Phase 2. Its stale filename references are in sections describing the IC generation methodology. These should be updated to match current filenames, but the content itself was approved.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Finding stale references | Manual file-by-file inspection | `grep -rn 'FINAL_ic_generator_enhanced\|generate_enhanced_ics' --include='*.py' --include='*.md'` | Catches references the audit missed |
| Section 3.2 content | Writing from scratch | Copy from CLAUDE.md lines 91-112 | Canonical source already exists and is verified correct |

## Common Pitfalls

### Pitfall 1: Missing References Outside Audit Scope
**What goes wrong:** The audit identified specific line numbers in specific files, but additional stale references exist in files not covered by the audit (DATASET_DOCUMENTATION.md, run_brutus_both_type_simple.py, pinn_instruction/instructions/sampling_method.md).
**Why it happens:** The audit focused on the 3 partial requirements, not every file in the project.
**How to avoid:** Run a full-project grep for both old filenames after all targeted fixes. Fix any additional hits that are NOT in `.planning/` directories.
**Warning signs:** Grep returning hits after you think you are done.

### Pitfall 2: Editing Historical Planning Documents
**What goes wrong:** Changing old filenames in `.planning/phases/01-*/` documents breaks the historical record of what was planned and decided.
**Why it happens:** A naive grep-and-replace would hit these files.
**How to avoid:** Explicitly exclude `.planning/` from replacement scope. These files are archival.
**Warning signs:** Git diff showing changes to `*-PLAN.md`, `*-SUMMARY.md`, `*-RESEARCH.md` files.

### Pitfall 3: Inconsistent Section 3.2 Across Agent Files
**What goes wrong:** AGENTS.md Section 3.2 gets updated but doesn't exactly match the content in CLAUDE.md/GEMINI.md/ANTIGRAVITY.md.
**Why it happens:** Manual rewriting instead of copying the canonical version.
**How to avoid:** Copy CLAUDE.md lines 91-112 verbatim for the Section 3.2 replacement block. The canonical content includes: 2 IC base folders, 4 Brutus output folders, gold IC note, IC_RAW_DIR externalization note, mapping rule, gold-standard subset note, ID gaps note.
**Warning signs:** Diff between agent files' Section 3.2 content.

### Pitfall 4: test_pipeline.py Has More Than Just the Import Issue
**What goes wrong:** Only fixing line 61 and missing the `ic_raw` path reference at line 69.
**Why it happens:** The audit flagged the import break but the `ic_raw` path reference at line 69 (`TEST_DIR / "ic_raw"`) is for test data, not the externalized IC_RAW_DIR. This is test-local data and may be intentional.
**How to avoid:** Examine whether `ic_raw` references in test_pipeline.py are test-local paths (acceptable) or references to the deleted project-level `Data/ic_raw/` directory. The test creates its own local `ic_raw/` subdirectory under `TEST_DIR`, which is valid behavior.
**Warning signs:** Changing test-local paths that serve a different purpose than the project-level IC_RAW_DIR.

### Pitfall 5: generate_ics.py Print Statement Wording
**What goes wrong:** Replacing `ic_raw_datasets/ic_hierarchical/` with a literal `$IC_RAW_DIR/ic_hierarchical/` in a Python print, but the actual save location is determined by `ic_generation_utils.py` which uses `os.environ.get('IC_RAW_DIR')`.
**Why it happens:** The print is cosmetic -- it tells the user where files will be saved. The actual path logic is in `ic_generation_utils.py`.
**How to avoid:** Update the print to say something like `$IC_RAW_DIR/ic_hierarchical/` or reference the IC_RAW_DIR env var pattern. The CONTEXT.md says to reference `$IC_RAW_DIR` path.
**Warning signs:** Print says one thing, code does another.

## Comprehensive Stale Reference Inventory

### Code Files

#### `simulation_data/Data/testing_data/test_pipeline.py`
| Line | Current | Fix |
|------|---------|-----|
| 61 | `from FINAL_ic_generator_enhanced import continuation_enhanced_ic_generation` | `from ic_generation_utils import continuation_enhanced_ic_generation` |

**Note:** Lines 69, 84, 107, 108, 125, 126 reference `ic_raw` as a local test subdirectory (`TEST_DIR / "ic_raw"`). This is test-local data and is NOT the same as the deleted project-level `Data/ic_raw/`. These references are intentional and should NOT be changed.

#### `simulation_data/Scripts/ic_generation/generate_ics.py`
| Line | Current | Fix |
|------|---------|-----|
| 56 | `print("- Saves to ic_raw_datasets/ic_hierarchical/ folder")` | `print("- Saves to $IC_RAW_DIR/ic_hierarchical/ folder")` |

#### `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`
| Line | Current | Fix |
|------|---------|-----|
| 10 | `1. Generate ICs using generate_enhanced_ics.py` | `1. Generate ICs using generate_ics.py` |

### Documentation Files

#### `simulation_data/Documentation/README.md`
| Line | Current | Fix |
|------|---------|-----|
| 22 | `Scripts/ic_generation/generate_enhanced_ics.py` | `Scripts/ic_generation/generate_ics.py` |
| 23 | `Scripts/ic_generation/FINAL_ic_generator_enhanced.py` | `Scripts/ic_generation/ic_generation_utils.py` |
| 25 | `Configuration (in Scripts/ic_generation/generate_enhanced_ics.py):` | `Configuration (in Scripts/ic_generation/generate_ics.py):` |
| 70 | `**Input:** \`Data/ic_raw/\`` | `**Input:** Raw ICs from \`$IC_RAW_DIR\` (set environment variable)` |
| 272 | `Data/ic_raw/  [Stage 1 output - raw generated ICs]` | `$IC_RAW_DIR  [Stage 1 output - raw generated ICs, externalized]` |
| 308 | `python3 simulation_data/Scripts/ic_generation/generate_enhanced_ics.py` | `python3 simulation_data/Scripts/ic_generation/generate_ics.py` |
| 349 | `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` |
| 350 | `generate_enhanced_ics.py` | `generate_ics.py` |

#### `README.md` (root)
| Line | Current | Fix |
|------|---------|-----|
| 77 | `python3 simulation_data/Scripts/ic_generation/generate_enhanced_ics.py` | `python3 simulation_data/Scripts/ic_generation/generate_ics.py` |
| 149 | `generate_enhanced_ics.py` | `generate_ics.py` |

#### `simulation_data/Documentation/DATASET_DOCUMENTATION.md` (discovered -- not in audit)
| Line | Current | Fix |
|------|---------|-----|
| 256 | `simulation_data/Scripts/ic_generation/FINAL_ic_generator_enhanced.py` | `simulation_data/Scripts/ic_generation/ic_generation_utils.py` |
| 267 | `simulation_data/Scripts/ic_generation/generate_enhanced_ics.py` | `simulation_data/Scripts/ic_generation/generate_ics.py` |
| 282 | `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` |
| 291 | `generate_enhanced_ics.py` | `generate_ics.py` |
| 805 | `simulation_data/Scripts/ic_generation/FINAL_ic_generator_enhanced.py` | `simulation_data/Scripts/ic_generation/ic_generation_utils.py` |
| 806 | `simulation_data/Scripts/ic_generation/generate_enhanced_ics.py` | `simulation_data/Scripts/ic_generation/generate_ics.py` |

#### `pinn_instruction/instructions/sampling_method.md` (discovered -- not in audit)
| Line | Current | Fix |
|------|---------|-----|
| 89 | `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` |

### Agent Instruction Files

#### `AGENTS.md` -- Section 3.2 (lines 91-107)
Replace entire Section 3.2 with canonical content from CLAUDE.md lines 91-112. Key changes:
- Remove `ic_hierarchical_for_gold_standard/` (line 94)
- Remove `ic_standard_quasi_random_for_gold_standard/` (line 96)
- Add "ICs (2 base folders):" header
- Add gold IC removal note
- Add IC_RAW_DIR externalization note
- Add gold-standard subset note (184 IDs)

#### `AGENTS.md` -- Non-3.2 sections
| Line | Current | Fix |
|------|---------|-----|
| 75 | `FINAL_ic_generator_enhanced.py`, `generate_enhanced_ics.py` | `ic_generation_utils.py`, `generate_ics.py` |
| 164 | `generate_enhanced_ics.py` | `generate_ics.py` |
| 215 | `generate_enhanced_ics.py` | `generate_ics.py` |
| 276 | `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` |

#### `CLAUDE.md` -- Non-3.2 sections
| Line | Current | Fix |
|------|---------|-----|
| 75 | `FINAL_ic_generator_enhanced.py`, `generate_enhanced_ics.py` | `ic_generation_utils.py`, `generate_ics.py` |
| 169 | `generate_enhanced_ics.py` | `generate_ics.py` |
| 220 | `generate_enhanced_ics.py` | `generate_ics.py` |
| 281 | `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` |

#### `GEMINI.md` -- Non-3.2 sections
| Line | Current | Fix |
|------|---------|-----|
| 75 | `FINAL_ic_generator_enhanced.py`, `generate_enhanced_ics.py` | `ic_generation_utils.py`, `generate_ics.py` |
| 161 | `generate_enhanced_ics.py` (Note: CONTEXT.md says 161 but actual is 169) | `generate_ics.py` |
| 212 | `generate_enhanced_ics.py` (Note: CONTEXT.md says 212 but actual is 220) | `generate_ics.py` |
| 273 | `FINAL_ic_generator_enhanced.py` (Note: CONTEXT.md says 273 but actual is 281) | `ic_generation_utils.py` |

#### `ANTIGRAVITY.md` -- Non-3.2 sections
| Line | Current | Fix |
|------|---------|-----|
| 67 | `FINAL_ic_generator_enhanced.py`, `generate_enhanced_ics.py` | `ic_generation_utils.py`, `generate_ics.py` |
| 161 | `generate_enhanced_ics.py` | `generate_ics.py` |
| 212 | `generate_enhanced_ics.py` | `generate_ics.py` |
| 273 | `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` |

### REQUIREMENTS.md Bookkeeping
| Line | Current | Fix |
|------|---------|-----|
| 15 | `[ ] **PATH-06**:` | `[x] **PATH-06**:` (after all fixes verified) |
| 25 | `[ ] **DOCS-02**:` | `[x] **DOCS-02**:` (after all fixes verified) |
| 27 | `[ ] **DOCS-04**:` | `[x] **DOCS-04**:` (after all fixes verified) |

Also update DOCS-04 description to reference AGENTS.md instead of QWEN.md (QWEN.md was deleted in commit c0c83e4).

## QWEN.md Resolution

**Git history confirms:**
1. QWEN.md existed (commit 0cb3863 -- baseline)
2. Updated in Phase 2 (commit dd69c35 -- Section 3.2 update)
3. Deleted later (commit c0c83e4 -- `chore: remove QWEN.md agent instructions and Qwen 3.5 2B model artifacts`)

**Conclusion:** QWEN.md was intentionally deleted. AGENTS.md is the 4th agent instruction file. DOCS-04 requirement description should list `AGENTS.md` instead of (or alongside) the note about QWEN.md being removed. No need to recreate QWEN.md.

## Code Examples

### test_pipeline.py Import Fix
```python
# Line 61 - BEFORE:
from FINAL_ic_generator_enhanced import continuation_enhanced_ic_generation

# Line 61 - AFTER:
from ic_generation_utils import continuation_enhanced_ic_generation
```

### generate_ics.py Print Fix
```python
# Line 56 - BEFORE:
print("- Saves to ic_raw_datasets/ic_hierarchical/ folder")

# Line 56 - AFTER:
print("- Saves to $IC_RAW_DIR/ic_hierarchical/ folder")
```

### AGENTS.md Section 3.2 -- Canonical Content (from CLAUDE.md)
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

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Manual verification via grep |
| Config file | none |
| Quick run command | `grep -rn 'FINAL_ic_generator_enhanced\|generate_enhanced_ics' --include='*.py' --include='*.md' . \| grep -v '.planning/'` |
| Full suite command | Same as quick run + `python -c "from ic_generation_utils import continuation_enhanced_ic_generation"` import test |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PATH-06 | test_pipeline.py imports ic_generation_utils; generate_ics.py references $IC_RAW_DIR | smoke | `cd simulation_data/Scripts/ic_generation && python -c "from ic_generation_utils import continuation_enhanced_ic_generation; print('OK')"` | N/A (inline) |
| DOCS-02 | README.md has zero old filenames or unqualified ic_raw | grep | `grep -n 'FINAL_ic_generator_enhanced\|generate_enhanced_ics\|Data/ic_raw/' simulation_data/Documentation/README.md` (expect empty) | N/A (inline) |
| DOCS-04 | AGENTS.md Section 3.2 matches CLAUDE.md; no stale filenames in any agent file | grep | `grep -n 'FINAL_ic_generator_enhanced\|generate_enhanced_ics\|_for_gold_standard' AGENTS.md CLAUDE.md GEMINI.md ANTIGRAVITY.md` (expect empty) | N/A (inline) |

### Sampling Rate
- **Per task commit:** grep sweep for old filenames
- **Per wave merge:** Full grep + import verification
- **Phase gate:** Zero hits from full-project grep (excluding `.planning/`); import succeeds

### Wave 0 Gaps
None -- no test framework needed. Verification is grep-based.

## Open Questions

1. **DATASET_DOCUMENTATION.md stale references**
   - What we know: 6 references to old filenames found (lines 256, 267, 282, 291, 805, 806). DOCS-01 was marked complete in Phase 2, but these are filename references, not structural/content issues.
   - What's unclear: Whether updating these counts as re-opening DOCS-01 or is simply part of the Phase 4 filename sweep.
   - Recommendation: Fix them as part of the comprehensive sweep. They are clearly stale filenames, and the CONTEXT.md says "Fix ALL stale references project-wide."

2. **run_brutus_both_type_simple.py comment reference**
   - What we know: Line 10 has a comment `1. Generate ICs using generate_enhanced_ics.py`. This is a docstring comment, not a code import.
   - What's unclear: Whether this is considered in-scope for the phase.
   - Recommendation: Fix it. It is a stale filename reference in an active script, consistent with "fix ALL stale references."

3. **pinn_instruction/instructions/sampling_method.md reference**
   - What we know: Line 89 references `FINAL_ic_generator_enhanced.py`. This is a methodology instruction document.
   - What's unclear: Whether pinn_instruction docs are in scope.
   - Recommendation: Fix it. The CONTEXT.md says project-wide scope.

4. **test_pipeline.py ic_raw local directory references**
   - What we know: Lines 69, 84, 107, 108, 125, 126 reference `TEST_DIR / "ic_raw"` as a local test subdirectory.
   - What's unclear: Whether these should be changed. They create a test-local `ic_raw/` directory under `testing_data/`, which is NOT the same as the project-level `Data/ic_raw/` that was externalized.
   - Recommendation: Leave them as-is. These are test-internal paths, not references to the deleted project-level directory.

## Sources

### Primary (HIGH confidence)
- `.planning/v1.0-MILESTONE-AUDIT.md` -- Gap details with specific line numbers
- `.planning/phases/04-stale-reference-fixes/04-CONTEXT.md` -- User decisions
- `.planning/REQUIREMENTS.md` -- Requirement definitions and status
- Direct file reads of all affected files -- verified line numbers and current content
- `git log --all --oneline -- QWEN.md` -- QWEN.md history (existed, updated, deleted)
- Full-project grep for `FINAL_ic_generator_enhanced`, `generate_enhanced_ics`, `ic_raw_datasets` -- discovered additional stale references

### Secondary (MEDIUM confidence)
- CONTEXT.md line number references for GEMINI.md (lines 75, 161, 212, 273) -- verified against actual file content; line numbers match for ANTIGRAVITY.md but GEMINI.md actual lines differ slightly (169, 220, 281 not 161, 212, 273). Planner should use actual grep results, not hardcoded line numbers.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No libraries needed; pure text replacement
- Architecture: HIGH - Complete inventory of all stale references verified by grep
- Pitfalls: HIGH - Well-documented from audit report and direct file inspection

**Research date:** 2026-03-19
**Valid until:** Indefinite (this is a one-time cleanup phase with fixed scope)
