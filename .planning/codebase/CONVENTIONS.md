# Coding Conventions

**Analysis Date:** 2026-04-27

## Naming Patterns

**Python Files:**
- snake_case: `ic_generation_utils.py`, `stage2_prescreening_revised_auto.py`, `data_structures.py`, `com_transform_brutus.py`
- All lowercase, words separated by underscores. Numbers used where disambiguation needed.

**Python Functions:**
- snake_case: `compute_forces()`, `load_ic_file()`, `prescreen_ic()`, `validate_dataset()`, `calculate_total_energy()`
- Numba JIT-decorated functions use identical naming, no prefix/suffix to indicate JIT status.

**Python Variables:**
- snake_case: `min_sep_overall`, `energy_error`, `positions_transformed`, `dataset_configs`
- Module-level constants: UPPER_CASE (`TMAX`, `DT`, `ENERGY_ERROR_THRESHOLD`, `G = 1.0`, `BRUTUS_PARAMS`)

**Python Classes:**
- PascalCase: `EnhancedThreeBodySampler`, `ValidationConfig`, `Validator`, `ValidationLogger`, `SimulationMetadata`, `RawTrajectoryData`, `ScaledTrajectoryData`, `ProcessedTrajectory`
- All dataclasses follow PascalCase naming.

**C++ Files:**
- PascalCase for main classes: `Brutus.cpp`, `Brutus.h`, `Star.cpp`, `Star.h`, `Cluster.cpp`, `Cluster.h`, `Bulirsch_Stoer.cpp`, `Bulirsch_Stoer.h`
- Tool files lowercase: `main.cpp`, `test_libs.cpp`

**C++ Classes:**
- PascalCase: `Brutus`, `Star`, `Cluster`, `Bulirsch_Stoer`

**C++ Methods:**
- Mixed conventions: some snake_case (`get_eta()`, `get_numBits()`, `set_tolerance()`), some camelCase (`calcAcceleration()`, `updatePositions()`, `updateVelocities()`). No single standard.

**C++ Variables:**
- snake_case: `num_bits`, `t_begin`, `t_end`, `data`, `dt_step`, `tcpu_step`
- Single-letter names common in physics code: `r`, `v`, `a`, `m`, `t`, `N`

**LaTeX Files:**
- Descriptive names: `main_CTL.tex`, `preamble_CTL.tex`, `01_intro.tex`, `02_data_characterization.tex`
- Section files numbered for ordering, section names in snake_case

## Code Style

**Formatting:**
- No formatter configured for Python or C++. No `.flake8`, `.pylintrc`, `pyproject.toml`, `.editorconfig`, or `.clang-format` in project root.
- Python indentation: 4 spaces (consistent across all files)
- C++ indentation: 2 spaces (consistent within `brutus_Newton-main/`)
- Line spacing: blank lines between function definitions, dense within functions
- Shebang `#!/usr/bin/env python3` used on some standalone scripts (prescreening, validator.py, test_pipeline.py) but not all (`ic_generation_utils.py`, `parsing.py`, `calculate_metrics.py`)

**Linting:**
- No linting tools configured for this project. No ESLint, Ruff, Flake8, Clang-Format, or similar.
- Reference-code directories have their own linter configs (e.g., PyTorch has `.flake8`, `.clang-format`, PINA has `.pylintrc`) but these are not project-standard.

## Import Organization

**Python Import Order (observed pattern):**

```python
# 1. Standard library
import sys
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict, List, Optional, Any

# 2. Third-party (numpy, scipy, numba, torch)
import numpy as np
from scipy.stats import qmc, norm
from numba import jit
import torch
import torch.nn as nn

# 3. Project-local (relative)
from .datastructures import ValidationReport, ValidationIssue
from .config import config
from ..utils.logging import get_logger

# 4. Project-local (absolute with sys.path manipulation) - used in older scripts
sys.path.insert(0, '<home>/Desktop/3_body_problem/simulation_data/Scripts/ic_generation')
from ic_generation_utils import continuation_enhanced_ic_generation
```

Observed patterns by file:
- `simulation_data/Validation/dataset_readiness_checks/validator.py` -- relative imports (`.datastructures`, `.config`)
- `simulation_data/Scripts/ic_generation/generate_ics.py` -- `sys.path.insert()` then bare import (`generate_ics.py:7-10`)
- `simulation_data/Scripts/ic_generation/ic_generation_utils.py` -- standard + third-party imports, no sys.path manipulation
- `pinn/basic_architecture.py` -- standard + third-party only (no project-local imports)
- `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` -- mixed: standard lib first, then numpy, then numba, then stdlib typing imports (unusual order: `from typing import ...` placed after `import time` at line 13)
- `simulation_data/Data/testing_data/test_pipeline.py` -- standard lib first, then sys.path manipulation for local imports

**Path Aliases:**
- No path aliases configured in `pyproject.toml` or any import mapping.

**C++ Include Order:**
- Project headers first, then standard library
- `#include "Brutus.h"` precedes `#include <vector>` in `Brutus.cpp`
- `main.cpp` places third-party headers (`mpreal.h`) after standard includes

## Error Handling

**Python Patterns:**
1. Try/except with specific exceptions: `except ImportError as e:` (`test_pipeline.py:101`), `except Exception as e:` (`stage2_prescreening_revised_auto.py:230`)
2. Some bare except patterns in commented code (legacy): `stage2_prescreening_revised_auto.py:276` (in comment block)
3. Graceful fallback: prescreening copies ICs directly if dependencies are missing (`test_pipeline.py:105-112`)
4. `pinn/data-handling/core/com_transform_brutus.py` raises `ValueError` for data inconsistency (`com_transform_brutus.py:56`)
5. `simulation_data/Validation/dataset_readiness_checks/utils/logging.py` provides `@handle_validation_errors` decorator that catches `FileNotFoundError`, `PermissionError`, and generic `Exception`, returning empty lists (`logging.py:150-168`)
6. Some scripts propagate unhandled exceptions silently (they crash)

**C++ Patterns:**
- Return codes used: `main()` in `main.cpp` returns `0` on error conditions (`main.cpp:259`)
- `cerr` output for error messages (`main.cpp:257-258`)
- No exception handling observed; relies on program termination via `return 0`
- No RAII wrapper classes for resources

## Logging

**Python:**
- Primary: `print()` statements used in vast majority of scripts (`stage2_prescreening_revised_auto.py`, `calculate_metrics.py`, `test_pipeline.py`)
- Structured logging: `simulation_data/Validation/dataset_readiness_checks/utils/logging.py` implements a full `logging` module-based system with `ValidationLogger` singleton, console + file handlers, `TimedOperation` context manager, log levels mapped to validation severities
- Log files saved to `Validation/dataset_readiness_checks/logs/validation_YYYYMMDD_HHMMSS.log`
- No logger used in `pinn/` modules (they use print statements or docstring examples)

**C++:**
- `cout` for output (stdout), `cerr` for diagnostic/error messages (`main.cpp:257-258, 314-326`)
- Commented-out `cerr` for progress/debug messages (`main.cpp:276, 284, 300, 306, 328`)
- No logging framework or timestamps

## Comments

**When to Comment:**
- Module-level docstrings present on most Python files, describing purpose and usage
- Inline comments used for physics explanations (energy calculation in `main.cpp:21-48`, leapfrog step in `stage2_prescreening_revised_auto.py:133-149`)
- Function-level docstrings vary: Google-style (Args/Returns) in newer code (`validator.py:66-75`, `ic_generation_utils.py:62-80`), narrative-style in older code
- C++ has virtually no function-level comments (`Brutus.cpp`, `Cluster.cpp`, `Bulirsch_Stoer.cpp`)
- Commented-out code blocks present in both Python (`stage2_prescreening_revised_auto.py:252-293`) and C++ (`main.cpp:82-98, 304-305`)

**JSDoc/TSDoc:**
- Not applicable (no TypeScript/JavaScript in project)

## Function Design

**Python:**
- Functions are typically 5-50 lines with clear single responsibility
- Most functions accept configuration via parameters, but many read module-level globals (e.g., `TMAX`, `DT` in `stage2_prescreening_revised_auto.py`)
- Return values: mixed -- some return tuples, some return dicts, some return None and mutate state
- Default parameter values used extensively (`stage2_prescreening_revised_auto.py:295-296`)
- Numba JIT decorator used on computational functions with explicit type signatures in docstrings

**C++:**
- Constructor overloading: `Brutus` has 5 constructors with escalating parameter sets (`Brutus.cpp:10-68`)
- Methods are short and single-purpose (3-30 lines)
- `vector<mpreal>` used as primary data container; no custom data structures beyond classes

## Module Design

**Python Exports:**
- `__init__.py` files exist in subpackages: `pinn/data-handling/__init__.py`, `pinn/data-handling/core/__init__.py`, `simulation_data/Validation/__init__.py`
- No explicit `__all__` definitions found
- The `data-processing-pipeline-full.py` inlines all module code rather than importing (self-described as a "modular pipeline" but all in one file, `data-processing-pipeline-full.py:1-15`)

**Barrel Files:**
- Not used in Python code
- C++ headers serve as interfaces for their respective `.cpp` files

## C++ Conventions (Detailed)

**Include Guards:**
- Traditional `#ifndef`/`#define`/`#endif` using double-underscore style:
  ```cpp
  #ifndef __Brutus_h
  #define __Brutus_h
  // ...
  #endif
  ```
- Guard naming: `__ClassName_h` (`Brutus.h:7-8`, `Star.h:9-10`, `Cluster.h:11-12`, `Bulirsch_Stoer.h:4-5`)

**Namespace Usage:**
- `using namespace std;` and `using namespace mpfr;` placed in headers (`Star.h:2,7`, `Cluster.h:2`, `Brutus.h:8`, `main.cpp:4,14`)
- This is a general C++ anti-pattern (namespace pollution in headers) but consistent across the codebase

**Member Visibility:**
- Largely public member data: `Cluster.h` has all members in `public:` zone (`Cluster.h:15-45`)
- `Brutus.h` has private data members and public methods (`Brutus.h:10-23` private, `:25-49` public)
- `Star.h` uses `public:` explicitly (`Star.h:13`)

**Inheritance:**
- `Cluster` inherits from `Star`: `class Cluster : public Star` (`Cluster.h:14`)

**Operator Overloading:**
- `friend ostream & operator <<` used for output in both `Star.h:22-26` and `Cluster.h:39-44`

**Memory Management:**
- All objects on stack or by-value in `std::vector`
- No smart pointers (`shared_ptr`, `unique_ptr`)
- No explicit `new`/`delete` in implementation code
- `mpreal` arbitrary-precision floats allocated as string values: `mpreal x = "1.234567890123456789";`

**Const-Correctness:**
- Partially applied: `Cluster::Cluster(vector<mpreal> data)` takes by value (copies large vectors)
- `Brutus.h:30-33` constructors take `vector<mpreal> &data` (mutable reference) and `mpreal &tolerance` (non-const reference) where const reference would be appropriate
- `main.cpp:21-49` `calculate_total_energy()` takes `const vector<mpreal>& data` -- the one example of proper const-reference usage

**Makefile:**
- Located at `brutus_Newton-main/Makefile`
- Compiler: `g++` with flags `-O3 -std=c++11 -DMPFR_USE_NO_MACRO -DMPFR_USE_INTMAX_T`
- Simple object-file based build, no dependency tracking beyond manual listing
- Targets: `all` (builds `brutus` binary), `clean` (removes objects and binary)
- No `test` target, no `check` target, no `install` target
- Hardcoded paths: `BREW_PREFIX = /opt/homebrew`, `HOME_DIR = <home>` (`Makefile:3-4`)

## LaTeX Conventions

**Document Structure:**
- Modular compilation: main file `\input{s preamble}` followed by `\include{sections/...}` for each section
- Section files prefixed with 2-digit numbers for order: `01_intro.tex`, `02_data_characterization.tex`, etc.
- Inactive sections stored as `_inactive.tex` suffix (e.g., `consolidated_blueprint_inactive.tex`)
- Documentation class: `\documentclass{article}`

**Standard Packages (from `preamble_CTL.tex`):**
- Core: `amsmath`, `amssymb`, `booktabs`, `geometry` (a4paper, 1in margins)
- Links: `hyperref` (colorlinks with blue/magenta/cyan)
- Algorithms: `algorithm`, `algpseudocode`
- Formatting: `float`, `makecell`, `xcolor` (dvipsnames), `tikz`
- Listings: `listings` with `showstringspaces=false`

**Custom Commands:**
- `\authcomment{#1}` for author comments in red bold
- `\authcommentenv` environment for multi-paragraph comments
- `\DeclareMathOperator{\median}{median}`

**Naming convention across LaTeX documents:**
- `preamble_CTL.tex`, `preamble.tex` -- loaded by main file
- `main_CTL.tex`, `main_pinn.tex`, `main-data-quality-assess.tex` -- root documents
- Section files: `NN_descriptive_name.tex`

## Configuration Management

**Hardcoded Values (prevalent):**
- Absolute paths with `<home>/` occur 160 times across 25+ Python files (`simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py:32`, `simulation_data/Scripts/metrics_calculation/calculate_metrics.py:16`, `simulation_data/Validation/prescreening/prescreening_utils.py:209`)
- Scientific constants hardcoded: `G = 1.0` (`stage2_prescreening_revised_auto.py:36`), `time_threshold = 9.5` (`test_pipeline.py:267`)
- Prescreening parameters hardcoded at module level: `TMAX = 1.0`, `DT = 0.0001`, `ENERGY_ERROR_THRESHOLD = 0.01` (`stage2_prescreening_revised_auto.py:19-23`)
- Brutus parameters hardcoded in runner scripts as dicts

**Environment Variables:**
- `IC_RAW_DIR` -- required for IC generation and prescreening (`stage2_prescreening_revised_auto.py:39-45`, `prescreening_utils.py:213-219`)
- `IC_RAW_DIR` points to external storage for raw IC files that are git-ignored

**Config Classes:**
- `ValidationConfig` dataclass in `simulation_data/Validation/dataset_readiness_checks/config.py` -- most structured config approach, supports `from_yaml()`/`to_yaml()` (`config.py:146-165`)
- Default config instance created at module level: `config = ValidationConfig()` (`config.py:169`)

**CLI Arguments:**
- C++ brutus: positional args for tolerance, wordLength, t_begin, t_end, dt, N, file_in (`main.cpp:1`)
- Python: `argparse` used in `prescreening_utils.py` for utility commands (`prescreening_utils.py:204-281`)
- Other scripts use module-level dicts or hardcoded values, not CLI args

## Path Handling

**Mixed approach:**
- `os.path.join()`, `os.path.basename()`, `os.path.exists()` used in prescreening and most older scripts
- `pathlib.Path` used in newer code: `pinn/data-handling/core/`, `simulation_data/Validation/dataset_readiness_checks/`, `simulation_data/Data/testing_data/test_pipeline.py`
- Both `os.path` and `pathlib` sometimes used in the same file (e.g., `test_pipeline.py` uses `Path` for dirs but `os.path` not imported)

## Commit Message Conventions

**Format:** Conventional Commits style with scopes:

```
type(scope): description
```

**Types observed (last 50 commits):**
- `docs` -- documentation changes (dominant, ~75% of commits)
- `feat` -- new features/scripts added
- `fix` -- bug fixes
- `refactor` -- code restructuring
- `chore` -- maintenance tasks

**Scope patterns:**
- Phase numbers: `08-01`, `07-02`, `06-01`, `05-01` (sub-phase identifiers)
- Phase groups: `phase-05`, `phase-07`, `phase-08`, `phase-09`
- Component: `planning`, `latex`, `quick-YYYYMMDD`
- No scope on general commits: `docs:`, `refactor:`

**Example commit messages:**
```
docs(planning): create Phase 9 issues directory consolidation plans
feat(08-01): add verify_compile.py for LaTeX compilation verification
fix(07-02): correct pinn-architecture longtable formatting for float fidelity
refactor(latex): flatten nested LaTeX directories and remove obsolete files
chore(08-01): add tmp directory placeholder for compilation outputs
```

**Commit description style:**
- Imperative mood ("create", "add", "correct", "flatten")
- Lowercase first word after colon
- No period at end
- 50-80 character subjects

## Git Hooks

- Installed hooks (all git-lfs related): `post-checkout`, `post-commit`, `post-merge`, `pre-push`
- All four hooks simply invoke `git lfs` commands; no linting or testing hooks
- Not installed: `pre-commit`, `commit-msg`, `prepare-commit-msg`

## CI/CD Configuration

- `.github/workflows/` contains Gemini AI agent dispatch workflows only:
  - `gemini-dispatch.yml`, `gemini-invoke.yml`, `gemini-review.yml`, `gemini-triage.yml`, `gemini-scheduled-triage.yml`
- No build verification, test execution, linting, or deployment workflows

## Anti-Patterns to Avoid (New Code)

1. **Do not hardcode absolute paths.** Use `pathlib.Path(__file__).resolve().parent` or environment variables (`stage2_prescreening_revised_auto.py:39-45` shows the right pattern for `IC_RAW_DIR`). 160 existing hardcoded path occurrences should not be replicated.

2. **Do not use `sys.path.insert()` for imports.** Follow the package pattern in `simulation_data/Validation/dataset_readiness_checks/` using relative imports (`.module`, `..package`).

3. **Do not use `using namespace std;` in C++ headers.** Keep namespace declarations in `.cpp` files only.

4. **Do not use `#ifndef __ClassName_h` double-underscore guards.** Use single underscore: `#ifndef BRUTUS_H` or `#pragma once`.

5. **Use `pathlib.Path`** for new code, not `os.path`. The project is migrating this direction (validator, parsing.py use it).

6. **Use `logging` module** for new code that needs structured output, following the `ValidationLogger` pattern in `simulation_data/Validation/dataset_readiness_checks/utils/logging.py`.

---

*Convention analysis: 2026-04-27*
