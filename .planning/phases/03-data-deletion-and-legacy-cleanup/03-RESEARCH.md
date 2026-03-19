# Phase 3: Data Deletion and Legacy Cleanup - Research

**Researched:** 2026-03-19
**Domain:** Filesystem cleanup, git-tracked file removal, build artifact purging
**Confidence:** HIGH

## Summary

Phase 3 is a destructive cleanup phase that removes redundant data directories, legacy documentation, Python bytecode caches, and LaTeX build artifacts. The phase is straightforward in concept but requires careful ordering: git-tracked files must be removed via `git rm`, gitignored files via filesystem `rm`, and a post-cleanup verification must confirm nothing was missed.

The key complexity lies in two areas: (1) two of the seven targets (`paper_templates/old_templates/` and `brutus_simulation_documentation/`) are git-tracked and require `git rm -r` to properly remove from both the working tree and the index, and (2) the `naming.py` file contains legacy `_for_gold_standard` mappings explicitly annotated for Phase 3 deletion that should be cleaned up as part of this phase. Additionally, `analysis/utils.py` has residual hardcoded `ic_raw` references that were listed in PATH-06 requirements but not addressed in Phase 1 execution -- these should be cleaned up now.

**Primary recommendation:** Split into two logical groups: (1) data directory deletion + code cleanup for `naming.py` and `analysis/utils.py` residuals, (2) build artifact purging (`__pycache__`, LaTeX artifacts) + legacy directory removal via `git rm`.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DEL-01 | `ic_hierarchical_for_gold_standard/` deleted | Directory exists (4857 files, 19MB), gitignored via `simulation_data/Data/ic_final/` pattern -- filesystem `rm -rf` sufficient |
| DEL-02 | `ic_standard_quasi_random_for_gold_standard/` deleted | Directory exists (2565 files, 10MB), gitignored -- filesystem `rm -rf` sufficient |
| DEL-03 | `ic_raw/` deleted | Directory exists (8869 files across 2 subdirs, 35MB), gitignored via explicit pattern -- filesystem `rm -rf` sufficient |
| CLN-01 | `paper_templates/old_templates/` deleted | Directory exists (14 items, 4.2MB), 4 files git-tracked (refs.bib, temp_v2.tex, temp_v2Notes.bib, wordcount.sh) -- requires `git rm -r` |
| CLN-02 | `brutus_simulation_documentation/` deleted | Directory exists (3 .txt files, 72KB), all git-tracked -- requires `git rm -r` |
| CLN-03 | All project `__pycache__/` removed (outside `.venv/`, `.git/`, `reference-code/`) | 8 directories found in scope, all gitignored -- filesystem `rm -rf` sufficient |
| CLN-04 | LaTeX build artifacts removed | 40+ files across `paper_templates/mdpi_template/`, `pinn_instruction/` subdirectories, all gitignored -- filesystem `rm` sufficient |
</phase_requirements>

## Standard Stack

This phase requires no external libraries. All operations use standard Unix/Git commands.

### Core Tools
| Tool | Purpose | Why Standard |
|------|---------|--------------|
| `rm -rf` | Remove gitignored directories and files | Standard POSIX filesystem deletion |
| `git rm -r` | Remove git-tracked directories | Properly stages removal in index + deletes from working tree |
| `find ... -exec rm` | Bulk artifact cleanup | Standard pattern for scattered file removal |

## Architecture Patterns

### Deletion Categories

There are three distinct categories of deletion targets, each requiring different handling:

**Category A: Gitignored data directories (DEL-01, DEL-02, DEL-03)**
- `simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard/` (4857 files, 19MB)
- `simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard/` (2565 files, 10MB)
- `simulation_data/Data/ic_raw/` (8869 files across 2 subdirs, 35MB)
- **Method:** `rm -rf` -- these are NOT in git index, covered by `.gitignore`
- **No git operation needed:** These directories have never been committed

**Category B: Git-tracked legacy directories (CLN-01, CLN-02)**
- `paper_templates/old_templates/` (4 tracked files + gitignored build artifacts)
- `brutus_simulation_documentation/` (3 tracked .txt files)
- **Method:** `git rm -r` to remove from index, then confirm working tree is clean
- **Tracked files:**
  - `paper_templates/old_templates/refs.bib`
  - `paper_templates/old_templates/temp_v2.tex`
  - `paper_templates/old_templates/temp_v2Notes.bib`
  - `paper_templates/old_templates/wordcount.sh`
  - `brutus_simulation_documentation/1st_run_terminal_output.txt`
  - `brutus_simulation_documentation/2_run_terminal_output.txt`
  - `brutus_simulation_documentation/3_run_terminal_output.txt`
- **Post git-rm:** The gitignored artifacts in `old_templates/` (PDF, .aux, .synctex.gz, etc.) will remain as orphaned files. Must `rm -rf` the directory after `git rm`.

**Category C: Scattered build artifacts (CLN-03, CLN-04)**
- 8 `__pycache__/` directories (all gitignored)
- 40+ LaTeX build artifact files across multiple directories (all gitignored)
- **Method:** `find` + `rm` patterns
- **Exclusion zones:** `.venv/`, `.git/`, `reference-code/`

### Code Cleanup Tasks

Two code files need modification as part of this phase:

**1. `naming.py` legacy mappings (lines 172, 174)**
```python
# Current (with Phase 3 deletion comments):
'ic_hierarchical_for_gold_standard': 'hierarchical_gold',  # Legacy path - Phase 3 deletion
'ic_standard_quasi_random_for_gold_standard': 'standard_gold',  # Legacy path - Phase 3 deletion
```
These two lines should be removed. The directories they map to will no longer exist.

**2. `analysis/utils.py` residual `ic_raw` references (lines 158, 169, 501)**
- Line 158: Comment referencing `ic_raw/` in path structure
- Line 169: References `'ic_raw_datasets'` directory name
- Line 501: Hardcoded default parameter `ic_base_dir: str = '<home>/.../ic_raw/ic_hierarchical/'`

This file was listed in PATH-06 requirements but was not addressed in Phase 1 execution. The `load_metrics()` default parameter at line 501 is a hardcoded absolute path to `ic_raw` that will break after deletion. This should be changed to use `IC_RAW_DIR` or have the default removed (require explicit argument).

### STRUCTURE.md Update

`.planning/codebase/STRUCTURE.md` references the old 4-folder IC layout and mentions `brutus_simulation_documentation/`. After deletion, this file should be updated to reflect reality:
- Line 26: Change "4 variant folders" to "2 variant folders"
- Line 27: Remove `ic_raw/` reference
- Line 58: Remove `brutus_simulation_documentation/` line
- Lines 80-86: Remove `_for_gold_standard` rows from Dataset Variant Folders table

### Recommended Execution Order

```
1. Pre-deletion verification
   - Confirm Phase 1 and Phase 2 are complete
   - Verify no code references to _for_gold_standard folders (except naming.py legacy lines)

2. Code cleanup
   - Remove naming.py legacy lines (172, 174)
   - Fix analysis/utils.py ic_raw references

3. Git-tracked directory removal
   - git rm -r paper_templates/old_templates/
   - git rm -r brutus_simulation_documentation/
   - rm -rf to clean remaining gitignored artifacts

4. Gitignored data directory removal
   - rm -rf simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard/
   - rm -rf simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard/
   - rm -rf simulation_data/Data/ic_raw/

5. Build artifact cleanup
   - find + rm for __pycache__/ (excluding .venv, .git, reference-code)
   - find + rm for LaTeX artifacts (excluding .venv, .git)

6. Update STRUCTURE.md

7. Post-deletion verification
   - Verify ic_final/ contains exactly 2 subdirectories
   - Verify ic_raw/ does not exist
   - Verify old_templates/ and brutus_simulation_documentation/ do not exist
   - Verify zero __pycache__/ in scope
   - Verify zero LaTeX artifacts in scope
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Finding scattered artifacts | Manual path lists | `find` with exclusion patterns | Artifacts can appear in unexpected locations |
| Removing git-tracked dirs | `rm -rf` alone | `git rm -r` then `rm -rf` orphans | `rm` alone leaves stale index entries |

**Key insight:** The critical distinction is tracked vs. untracked. Using `rm -rf` on git-tracked files leaves ghost entries in the index that cause confusing `git status` output. Always use `git rm` for tracked content.

## Common Pitfalls

### Pitfall 1: Using `rm` on git-tracked files
**What goes wrong:** `rm -rf paper_templates/old_templates/` deletes files but git index still has them, showing as deleted-but-not-staged.
**Why it happens:** Git tracks files in two places: working tree and index.
**How to avoid:** Use `git rm -r` for tracked directories. This removes from both.
**Warning signs:** `git status` shows "deleted: ..." in red (unstaged) after rm.

### Pitfall 2: Forgetting gitignored files alongside tracked files
**What goes wrong:** `git rm -r paper_templates/old_templates/` removes only tracked files. Gitignored build artifacts (PDF, .aux, .synctex.gz) remain as orphan files in the directory.
**Why it happens:** `git rm` only operates on indexed files.
**How to avoid:** After `git rm -r`, check if the directory still exists and `rm -rf` it if so.
**Warning signs:** `ls paper_templates/old_templates/` still shows files after git rm.

### Pitfall 3: Not excluding reference-code from __pycache__ cleanup
**What goes wrong:** Deleting `__pycache__` in `reference-code/` modifies third-party code.
**Why it happens:** The requirement explicitly excludes `.venv/`, `.git/`, `reference-code/`.
**How to avoid:** Use `-not -path '*/reference-code/*'` in find commands.
**Warning signs:** Find returns paths under reference-code/.

### Pitfall 4: Forgetting to clean up code references after deletion
**What goes wrong:** `naming.py` still maps deleted directories, causing runtime confusion.
**Why it happens:** The Phase 3 deletion comments were left as breadcrumbs but could be forgotten.
**How to avoid:** Remove the legacy lines in the same phase that deletes the directories.
**Warning signs:** grep for `_for_gold_standard` in Python files returns matches.

### Pitfall 5: analysis/utils.py hardcoded ic_raw path
**What goes wrong:** `load_metrics()` default argument points to deleted `ic_raw/` directory, causing FileNotFoundError.
**Why it happens:** This file was in PATH-06 scope but was not addressed in Phase 1.
**How to avoid:** Fix the default parameter before or during directory deletion.
**Warning signs:** grep for `/ic_raw/` in Python files returns matches in analysis/utils.py.

## Code Examples

### Removing git-tracked directory with mixed content
```bash
# Step 1: Remove tracked files from git index + working tree
git rm -r paper_templates/old_templates/

# Step 2: Clean up remaining gitignored files (PDFs, build artifacts)
rm -rf paper_templates/old_templates/
```

### Safe __pycache__ cleanup with exclusions
```bash
find . -type d -name "__pycache__" \
  -not -path "./.venv/*" \
  -not -path "./.git/*" \
  -not -path "./reference-code/*" \
  -exec rm -rf {} +
```

### Safe LaTeX artifact cleanup
```bash
find . \( -name "*.synctex.gz" -o -name "*.aux" -o -name "*.fls" \
  -o -name "*.fdb_latexmk" -o -name "*.out" \) \
  -not -path "./.venv/*" \
  -not -path "./.git/*" \
  -exec rm -f {} +
```

### naming.py cleanup
```python
# REMOVE these two lines (172, 174):
# 'ic_hierarchical_for_gold_standard': 'hierarchical_gold',  # Legacy path - Phase 3 deletion
# 'ic_standard_quasi_random_for_gold_standard': 'standard_gold',  # Legacy path - Phase 3 deletion
```

### analysis/utils.py fix
```python
# Line 501: Change from hardcoded default to no default or IC_RAW_DIR
# Before:
def load_metrics(filepath: str, ic_base_dir: str = '<home>/Desktop/3_body_problem/simulation_data/Data/ic_raw/ic_hierarchical/') -> Dict:

# After (require explicit argument):
def load_metrics(filepath: str, ic_base_dir: Optional[str] = None) -> Dict:
```

## Inventory of All Deletion Targets

### Data Directories (gitignored, filesystem rm only)
| Path | Files | Size | Git Status |
|------|-------|------|------------|
| `simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard/` | 4857 | 19MB | gitignored |
| `simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard/` | 2565 | 10MB | gitignored |
| `simulation_data/Data/ic_raw/` | 8869 | 35MB | gitignored |

### Legacy Directories (git-tracked, require git rm)
| Path | Tracked Files | Size | Git Status |
|------|---------------|------|------------|
| `paper_templates/old_templates/` | 4 (.bib, .tex, .sh) + gitignored artifacts | 4.2MB | partially tracked |
| `brutus_simulation_documentation/` | 3 (.txt) | 72KB | fully tracked |

### __pycache__ Directories (8 total, all gitignored)
```
./pinn/data-handling/core/__pycache__
./pinn_instruction/__pycache__
./simulation_data/Scripts/ic_generation/__pycache__
./simulation_data/Validation/dataset_readiness_checks/utils/__pycache__
./simulation_data/Validation/dataset_readiness_checks/__pycache__
./simulation_data/Validation/dataset_readiness_checks/modules/__pycache__
./simulation_data/Validation/dataset_readiness_checks/reports/__pycache__
./simulation_data/Validation/__pycache__
```

### LaTeX Build Artifacts (40+ files, all gitignored)
Across these directories:
- `paper_templates/mdpi_template/` (10 files: paper.* and raw_template.*)
- `paper_templates/old_templates/` (5 files: temp_v2.* -- will be removed with directory)
- `pinn_instruction/review-of-framework/` (10 files)
- `pinn_instruction/pinn-architecture/` (5 files)
- `pinn_instruction/sampling-method/` (5 files)
- `pinn_instruction/ctl-instruction/` (5 files)
- `pinn_instruction/trainingData-quality-assessment/` (5 files)

### Code Files Needing Cleanup
| File | Lines | Issue |
|------|-------|-------|
| `simulation_data/Validation/dataset_readiness_checks/utils/naming.py` | 172, 174 | Legacy `_for_gold_standard` mappings with "Phase 3 deletion" comments |
| `simulation_data/Validation/analysis/utils.py` | 158, 169, 501 | Residual `ic_raw` references (PATH-06 residual) |

### Documentation Files Needing Update
| File | Lines | Issue |
|------|-------|-------|
| `.planning/codebase/STRUCTURE.md` | 26, 27, 58, 80-86 | References deleted directories and old 4-folder layout |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None -- no project test infrastructure exists |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DEL-01 | ic_hierarchical_for_gold_standard deleted | smoke | `test ! -d simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard && echo PASS` | N/A (shell check) |
| DEL-02 | ic_standard_quasi_random_for_gold_standard deleted | smoke | `test ! -d simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard && echo PASS` | N/A (shell check) |
| DEL-03 | ic_raw deleted | smoke | `test ! -d simulation_data/Data/ic_raw && echo PASS` | N/A (shell check) |
| CLN-01 | old_templates deleted | smoke | `test ! -d paper_templates/old_templates && echo PASS` | N/A (shell check) |
| CLN-02 | brutus_simulation_documentation deleted | smoke | `test ! -d brutus_simulation_documentation && echo PASS` | N/A (shell check) |
| CLN-03 | No __pycache__ in scope | smoke | `test $(find . -type d -name "__pycache__" -not -path "./.venv/*" -not -path "./.git/*" -not -path "./reference-code/*" \| wc -l) -eq 0 && echo PASS` | N/A (shell check) |
| CLN-04 | No LaTeX artifacts in scope | smoke | `test $(find . \( -name "*.synctex.gz" -o -name "*.aux" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" \) -not -path "./.venv/*" -not -path "./.git/*" \| wc -l) -eq 0 && echo PASS` | N/A (shell check) |

### Sampling Rate
- **Per task commit:** Run all 7 shell checks
- **Per wave merge:** Same (all checks are fast < 1 second)
- **Phase gate:** All 7 checks pass before `/gsd:verify-work`

### Wave 0 Gaps
None -- all validation is via shell existence checks, no test framework needed.

## Open Questions

1. **analysis/utils.py ic_raw default parameter**
   - What we know: Line 501 has hardcoded `<home>/.../ic_raw/ic_hierarchical/` as default. This was in PATH-06 scope but not addressed in Phase 1.
   - What's unclear: Whether this function is actively used and what callers pass for `ic_base_dir`.
   - Recommendation: Change default to `None` and require explicit argument, or use `IC_RAW_DIR` env var consistent with other scripts. Flag to planner as code cleanup within Phase 3 scope.

2. **STRUCTURE.md update scope**
   - What we know: `.planning/codebase/STRUCTURE.md` references deleted directories.
   - What's unclear: Whether updating planning metadata files is in scope for Phase 3 or deferred.
   - Recommendation: Include in Phase 3 since it documents current reality. Lightweight edit.

## Sources

### Primary (HIGH confidence)
- Direct filesystem inspection via `ls`, `du`, `find` commands
- Git index inspection via `git ls-files --cached`
- `.gitignore` analysis and `git check-ignore -v` verification
- Phase 1 verification report (`01-VERIFICATION.md`) confirming completion
- Phase 1 plan 02 (`01-02-PLAN.md`) confirming PATH-06 scope included `analysis/utils.py`
- `REQUIREMENTS.md` for requirement definitions

### Secondary (MEDIUM confidence)
- `.planning/codebase/STRUCTURE.md` for project layout documentation

## Metadata

**Confidence breakdown:**
- Deletion targets: HIGH - verified via direct filesystem inspection
- Git tracking status: HIGH - verified via git ls-files and git check-ignore
- Code cleanup (naming.py): HIGH - verified via grep, exact lines identified
- Code cleanup (analysis/utils.py): HIGH - verified via grep, exact lines identified
- Build artifact inventory: HIGH - verified via find commands

**Research date:** 2026-03-19
**Valid until:** 2026-04-19 (stable -- filesystem state changes only via explicit human action)
