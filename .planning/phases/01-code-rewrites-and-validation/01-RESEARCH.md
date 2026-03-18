# Phase 1: Code Rewrites and Validation - Research

**Researched:** 2026-03-18
**Domain:** Python path management, IC file resolution, dataset validation
**Confidence:** HIGH

## Summary

This phase addresses path consolidation in a 3-body simulation codebase where gold-standard IC folders (`ic_hierarchical_for_gold_standard/`, `ic_standard_quasi_random_for_gold_standard/`) must be removed from script references, and the `ic_raw/` directory must be externalized via environment variable.

The codebase has 4 dataset variants tracked in `config.py`: hierarchical, hierarchical_gold, standard, standard_gold. Gold variants reference separate Brutus output folders that remain distinct; only IC paths need updating to point to base folders.

**Primary recommendation:** Update `config.py` IC paths for gold variants to use base folders, add `IC_RAW_DIR` env var to Stage 1/2 scripts with strict error on missing, update 7 debug/validation scripts to remove gold path references.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.x | Script runtime | Existing codebase standard |
| numpy | existing | Numerical operations | Used throughout pipeline |
| pathlib | builtin | Path manipulation | Modern Python path handling |
| os.environ | builtin | Environment variables | External configuration |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| scipy.stats.qmc | existing | Sobol sequence generation | IC generation scripts |
| numba | existing | JIT compilation | Prescreening integration loops |
| json | builtin | Configuration/storage | Processing indices, blacklists |
| glob/re | builtin | File pattern matching | Filename extraction |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `IC_RAW_DIR` env var | Config file (YAML/JSON) | Env var simpler, no new deps; config file more flexible but overkill |
| `os.environ.get()` | `os.environ[]` with try/except | Direct access with clear error message preferred for strict failure |
| `pathlib.Path` | `os.path.join()` | pathlib more readable, better cross-platform |

**Installation:** No new packages needed. All changes use existing dependencies.

## Architecture Patterns

### Recommended Project Structure

Scripts fall into 3 categories:
1. **Validation system** (`dataset_readiness_checks/`) - uses centralized `config.py`
2. **Pipeline scripts** (IC generation, prescreening) - maintain own paths, add `IC_RAW_DIR`
3. **Debug utilities** - ad-hoc scripts needing individual path fixes

```
simulation_data/
├── Validation/
│   ├── dataset_readiness_checks/
│   │   ├── config.py              # Central path config (4 variants)
│   │   ├── utils/naming.py        # Filename pattern utilities
│   │   └── modules/correspondence.py  # 1:1 IC-Brutus validation
│   └── prescreening/
│       ├── stage2_prescreening_revised_auto.py  # Uses IC_RAW_DIR
│       ├── prescreening_utils.py   # Uses IC_RAW_DIR
│       └── utilities/example_incremental_workflow.py  # Uses IC_RAW_DIR
├── Scripts/
│   ├── ic_generation/
│   │   ├── FINAL_ic_generator_enhanced.py  # Uses IC_RAW_DIR (to rename)
│   │   └── generate_enhanced_ics.py        # Import runner (to rename)
│   ├── brutus_runners/
│   │   └── run_brutus_hierarchical_only_mac_gold_standard.py  # Gold IC path
│   └── debug/
│       ├── compare_ic_brutus_files.py      # Gold IC path
│       ├── audit_and_backfill_brutus_result_footers.py  # Gold IC path
│       └── renaming/
│           ├── rename_ic_hierarchical_gold.py  # Gold IC path
│           └── rename_ic_standard_gold.py      # Gold IC path
└── Documentation/
    ├── DATASET_DOCUMENTATION.md    # Update: 2 IC folders
    ├── README.md                   # Update: 2-folder layout
    └── standard_quasi_random_ids_not_in_gold.md  # 184-ID exclusion list
```

### Pattern 1: Environment Variable with Strict Error

**What:** Externalize `IC_RAW_DIR` path configuration with clear error message

**When to use:** Scripts that read from `ic_raw/` subdirectories

**Example:**
```python
# Source: Adapted from FINAL_ic_generator_enhanced.py lines 594-600
import os

IC_RAW_DIR = os.environ.get('IC_RAW_DIR')
if IC_RAW_DIR is None:
    raise RuntimeError(
        "IC_RAW_DIR environment variable not set. "
        "Export the path to your ic_raw directory: "
        "export IC_RAW_DIR=/path/to/ic_raw"
    )

IC_HIERARCHICAL_DIR = os.path.join(IC_RAW_DIR, 'ic_hierarchical')
IC_STANDARD_DIR = os.path.join(IC_RAW_DIR, 'ic_standard_quasi_random')
```

### Pattern 2: Centralized Config Path Updates

**What:** Update `config.py` dataset_variants dict to point gold IC paths to base folders

**When to use:** Validation system that needs 4-variant distinction for Brutus output folders

**Example:**
```python
# Source: config.py lines 42-59
self.dataset_variants = {
    "hierarchical": {
        "ic_dir": "Data/ic_final/ic_hierarchical",  # Unchanged
        "brutus_dir": "Data/brutus_output/brutus_hierarchical"
    },
    "hierarchical_gold": {
        "ic_dir": "Data/ic_final/ic_hierarchical",  # CHANGED: was ic_hierarchical_for_gold_standard
        "brutus_dir": "Data/brutus_output/brutus_hierarchical_gold_standard"  # Unchanged
    },
    # ... similar for standard/standard_gold
}
```

### Pattern 3: Runtime Exclusion List Loading

**What:** Load 184 excluded IDs from markdown file at runtime for correspondence validation

**When to use:** `correspondence.py` validating standard_gold subset

**Example:**
```python
# Source: correspondence.py is_blacklisted() function (lines 113-138)
def load_excluded_ids():
    """Load 184 excluded IDs from standard_quasi_random_ids_not_in_gold.md"""
    excluded = set()
    md_path = Path(__file__).parent.parent.parent / "Documentation" / "standard_quasi_random_ids_not_in_gold.md"
    if md_path.exists():
        with open(md_path) as f:
            for line in f:
                line = line.strip()
                # Parse numbered list format: "0038  0042  ..."
                for token in line.split():
                    if token.isdigit():
                        excluded.add(int(token))
    return excluded
```

### Anti-Patterns to Avoid
- **Hardcoded absolute paths:** Replace with `IC_RAW_DIR` + subdirectory
- **Silent fallbacks:** Raise error if `IC_RAW_DIR` not set; don't default silently
- **Filename pattern confusion:** Gold ICs use same `ic_hierarchical_XXXX.txt` pattern as base (folder defines variant, not filename)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Path externalization | Custom config parser | `os.environ.get()` | Simple, standard, no deps |
| Filename extraction | Manual string splitting | Regex `r'_(\d+)\.txt$'` | Handles edge cases |
| Exclusion list parsing | Hardcode 184 IDs in Python | Load from markdown file | Single source of truth, maintainable |
| Variant mapping | Ad-hoc if/else chains | Centralized `directory_mapping` dict in `naming.py` | Consistent, testable |

**Key insight:** Path consolidation is a configuration problem, not a code architecture problem. Keep changes minimal and localized.

## Common Pitfalls

### Pitfall 1: Filename Pattern Mismatch
**What goes wrong:** Assuming gold IC files have `ic_hierarchical_gold_XXXX.txt` pattern when they actually use `ic_hierarchical_XXXX.txt`

**Why it happens:** `config.py` IC patterns at lines 62-67 define:
```python
"hierarchical_gold": "ic_hierarchical_gold_{num:04d}.txt",  # WRONG if files don't have 'gold'
```
But actual files in `ic_hierarchical_for_gold_standard/` are named `ic_hierarchical_XXXX.txt`.

**How to avoid:** Verify actual filenames in gold folders before updating patterns. The folder defines the variant, not the filename.

**Warning signs:** `extract_file_numbers()` returns empty set; correspondence validation reports all files missing.

### Pitfall 2: Brutus Output Filename Pattern
**What goes wrong:** Changing Brutus output patterns when only IC patterns need fixing

**Why it happens:** Gold Brutus outputs use `brutus_hierarchical_gold_XXXX.txt` pattern (with 'gold' in name)

**How to avoid:** Verify actual Brutus filenames in `brutus_hierarchical_gold_standard/` folder before changing patterns.

**Warning signs:** Validation suddenly can't find any Brutus outputs for gold variant.

### Pitfall 3: Circular Path Dependencies
**What goes wrong:** Making `config.py` import from pipeline scripts or vice versa

**Why it happens:** Trying to "unify" all path handling in one module

**How to avoid:** Keep validation system (`config.py`) separate from pipeline scripts. Pipeline scripts use `IC_RAW_DIR` directly; validation uses centralized config.

**Warning signs:** Import errors, circular dependency warnings.

### Pitfall 4: 184-ID Exclusion Not Loaded
**What goes wrong:** `correspondence.py` reports 184 false failures for standard_gold

**Why it happens:** Exclusion list file not found or parsing fails silently

**How to avoid:** Add count guard with warning:
```python
if len(excluded) != 184:
    logging.warning(f"Expected 184 excluded IDs, found {len(excluded)}")
```

**Warning signs:** Validation summary shows "184 missing Brutus outputs" for standard_gold variant.

## Code Examples

### Loading Exclusion List at Runtime
```python
# Source: correspondence.py extension for VALD-01
from pathlib import Path

def load_standard_gold_exclusions():
    """Load 184 excluded IDs from markdown file."""
    excluded = set()
    md_path = Path(__file__).parent.parent.parent / "Documentation" / "standard_quasi_random_ids_not_in_gold.md"
    if not md_path.exists():
        logging.warning(f"Exclusion list not found: {md_path}")
        return excluded

    with open(md_path) as f:
        in_list = False
        for line in f:
            line = line.strip()
            if line.startswith('```') and line.endswith('```'):
                in_list = not in_list
                continue
            if in_list:
                for token in line.split():
                    if token.isdigit():
                        excluded.add(int(token))
    return excluded
```

### IC_RAW_DIR with Strict Error
```python
# Source: FINAL_ic_generator_enhanced.py lines 594-600 modification
import os

def get_ic_raw_dir():
    """Get IC_RAW_DIR from environment with strict error."""
    ic_raw_dir = os.environ.get('IC_RAW_DIR')
    if ic_raw_dir is None:
        raise RuntimeError(
            "IC_RAW_DIR environment variable not set. "
            "This script requires an external ic_raw directory with "
            "ic_hierarchical/ and ic_standard_quasi_random/ subdirectories.\n"
            "Example: export IC_RAW_DIR=/path/to/ic_raw"
        )
    return ic_raw_dir
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 4 IC folders (2 base + 2 gold) | 2 IC folders (base only) | Phase 1 | Gold ICs complete; folders redundant |
| Hardcoded `<home>/...` paths | `IC_RAW_DIR` env var | Phase 1 | Reproducibility, portability |
| Gold filenames `ic_*_gold_XXXX.txt` | Standard `ic_*_XXXX.txt` | Phase 1 | Folder defines variant, not filename |
| `ic_raw/` in repo | `IC_RAW_DIR` external | Phase 1 | Git ignore friendly, user-managed |

**Deprecated/outdated:**
- `ic_hierarchical_for_gold_standard/` folder references in scripts
- `ic_standard_quasi_random_for_gold_standard/` folder references in scripts
- Hardcoded `<home>/Desktop/3_body_problem/simulation_data/Data/ic_raw/` paths

## Open Questions

1. **Brutus output pattern for gold variants**: Need to verify actual filenames in `brutus_hierarchical_gold_standard/` and `brutus_standard_quasi_random_gold_standard/` folders to confirm pattern is `brutus_*_gold_{num:04d}.txt` vs `brutus_*_{num:04d}.txt`.

2. **`prescreening_utils.py` default paths**: Lines 209-211 have hardcoded defaults for `--index` and `--input-dir` args. Should these also use `IC_RAW_DIR` or are they acceptable as legacy defaults?

3. **`analysis/utils.py` line 169**: References `'ic_raw_datasets'` which differs from `ic_raw`. Is this intentional or a bug?

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None detected (no pytest/jest config found) |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PATH-01 | IC_DIR points to base folder | Manual verification | `grep -n "IC_DIR\|ic_hierarchical_for_gold_standard" run_brutus_hierarchical_only_mac_gold_standard.py` | ❌ Wave 0 |
| PATH-02 | config.py gold ic_dir entries | Manual verification | `grep -n "ic_dir.*gold" config.py` | ❌ Wave 0 |
| PATH-03 | naming.py mappings updated | Manual verification | `grep -n "_for_gold_standard" naming.py` | ❌ Wave 0 |
| PATH-04 | Debug scripts use base paths | Manual verification | `grep -rn "_for_gold_standard" Scripts/debug/` | ❌ Wave 0 |
| PATH-05 | Filename patterns updated | Manual verification | `grep -n "_gold_" config.py` | ❌ Wave 0 |
| PATH-06 | IC_RAW_DIR env var usage | Manual verification | `grep -n "IC_RAW_DIR\|ic_raw" Scripts/ic_generation/*.py Validation/prescreening/*.py` | ❌ Wave 0 |
| VALD-01 | correspondence.py handles 184 gaps | Manual test run | `python correspondence.py standard_gold` | ❌ Wave 0 |
| VALD-02 | Exclusion list documented | File existence check | `test -f standard_quasi_random_ids_not_in_gold.md` | ✅ Exists |

### Sampling Rate
- **Per task commit:** N/A (no test framework)
- **Per wave merge:** N/A
- **Phase gate:** Grep verification commands must return no matches for `_for_gold_standard` or hardcoded `<home>/.../ic_raw/`

### Wave 0 Gaps
- [ ] `tests/` directory does not exist — manual verification required
- [ ] Framework install: N/A — project uses manual verification

*(No test infrastructure exists; verification relies on grep-based success criteria and manual script execution)*

## Sources

### Primary (HIGH confidence)
- `simulation_data/Validation/dataset_readiness_checks/config.py` - Lines 42-75: 4-variant path configuration
- `simulation_data/Validation/dataset_readiness_checks/utils/naming.py` - Lines 165-181: directory-to-variant mapping
- `simulation_data/Validation/dataset_readiness_checks/modules/correspondence.py` - Lines 113-138: blacklist/exclusion handling
- `simulation_data/Scripts/ic_generation/FINAL_ic_generator_enhanced.py` - Lines 594-600: hardcoded ic_raw paths
- `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` - Lines 38-50: DATASET_CONFIGS with ic_raw paths
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` - 184-ID exclusion list (exists)

### Secondary (MEDIUM confidence)
- `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` - Lines 34-36: IC_DIR gold reference
- `simulation_data/Scripts/debug/compare_ic_brutus_files.py` - Lines 32-37: gold IC path references
- `simulation_data/Scripts/debug/renaming/rename_ic_hierarchical_gold.py` - Line 5: gold folder reference
- `simulation_data/Scripts/debug/renaming/rename_ic_standard_gold.py` - Line 5: gold folder reference
- `simulation_data/Validation/prescreening/prescreening_utils.py` - Lines 209-211: hardcoded defaults
- `simulation_data/Validation/analysis/utils.py` - Lines 157-171: ic_raw_datasets reference

### Tertiary (LOW confidence)
- `simulation_data/Validation/prescreening/utilities/example_incremental_workflow.py` - Line 13: ic_raw reference (example script, may be lower priority)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No new packages; existing Python/numpy/pathlib confirmed
- Architecture: HIGH - File contents verified via Read tool
- Pitfalls: MEDIUM - Based on code analysis; actual runtime behavior not tested
- Filename patterns: MEDIUM - config.py patterns verified; actual filesystem not checked for gold Brutus outputs

**Research date:** 2026-03-18
**Valid until:** 30 days (stable codebase; paths unlikely to change)
