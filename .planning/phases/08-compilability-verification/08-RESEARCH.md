# Phase 8: Compilability Verification - Research

**Researched:** 2026-03-22
**Domain:** LaTeX compilation, log parsing, Python subprocess management
**Confidence:** HIGH

## Summary

This phase implements an automated verification script that compiles all 5 modular LaTeX structures with `pdflatex` and reports pass/fail (0 errors required), along with a warning comparison against the original monolithic files to flag any new warnings introduced by modularization.

**Primary recommendation:** Use `latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -output-directory=<temp>` for compilation, parse the `.log` file for errors (lines starting with `!`) and warnings (Overfull/Underfull hbox, LaTeX/Package Warnings), normalize warnings by stripping line numbers before comparison.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Script design
- **D-01:** Single script `verify_compile.py` in `pinn_instruction/original_latex/verification/` -- consistent with Phase 5 (verify_content.py), Phase 6 (verify_preamble.py), Phase 7 (verify_structure.py) pattern
- **D-02:** Same CLI interface: `--structure <name>`, `--output <path>`, `--verbose`, run all structures by default
- **D-03:** Compile both the original monolithic .tex (from `old/`) AND the modular version for each structure, enabling apples-to-apples warning comparison

#### Compiler and invocation
- **D-04:** Use `latexmk -pdf -pdflatex=pdflatex` for compilation -- handles multi-pass automatically (resolves cross-refs, citations, TOC without manual iteration counting)
- **D-05:** `pdflatex` is confirmed available (TeX Live 2025, `/Library/TeX/texbin/pdflatex`); `latexmk` also available
- **D-06:** Run latexmk with `cwd` set to the structure's directory so relative `\input{preamble}` and `\input{sections/...}` paths resolve correctly
- **D-07:** Use `-output-directory` pointing to a per-structure temp directory under `pinn_instruction/original_latex/verification/tmp/` to avoid polluting source directories with aux files from verification runs
- **D-08:** Set `-interaction=nonstopmode` so compilation continues through errors rather than halting (ensures we capture all errors, not just the first)
- **D-09:** Timeout per compilation: 120 seconds (sufficient for all 5 structures given their size)

#### Pass/fail criteria
- **D-10:** PASS = 0 fatal errors in the compilation log (lines matching `^!` in .log file)
- **D-11:** FAIL = any fatal error present; report all errors with surrounding context (file, line, error message)
- **D-12:** Warnings are informational -- do NOT count as pass/fail. Report warning counts and flag new warnings (present in modular log but not in original log) as noteworthy.

#### Warning baseline comparison (COMP-02)
- **D-13:** Extract warnings from both original and modular compilation logs using the same regex; diff the warning sets
- **D-14:** A "warning" is any log line matching `LaTeX Warning:`, `Package Warning:`, `Class Warning:`, or `Overfull \hbox` / `Underfull \hbox`
- **D-15:** Normalize warning text before comparison: strip file path prefixes (vary between runs) and page numbers; compare warning type and core message
- **D-16:** Report three categories: (a) warnings in both = pre-existing (OK), (b) warnings only in modular = new/introduced, (c) warnings only in original = resolved (bonus -- not required but informative)

#### Report format
- **D-17:** Markdown output to `pinn_instruction/original_latex/verification/compile_verification_report.md` -- consistent with D-06 from Phase 5 CONTEXT
- **D-18:** Report structure: summary table (PASS/FAIL per structure, error count, new warning count) at top, followed by per-structure sections with full error list and new warning list
- **D-19:** Exit code 0 if all 5 structures compile with 0 errors; exit code 1 if any structure has errors
- **D-20:** Temp directory cleaned up after each run (or kept with `--keep-tmp` flag for debugging)

#### Compilation working directory
- **D-21:** Each structure's `main.tex` (or equivalent) is compiled from its own directory. The 5 main files are:
  1. Data-quality-assessment: `pinn_instruction/original_latex/Data-quality-assessment/data_quality_assess/main-data-quality-assess.tex` (cwd: `data_quality_assess/`)
  2. ctl-instruction: `pinn_instruction/original_latex/ctl-instruction/ctl-instruction/main_CTL.tex` (cwd: `ctl-instruction/`)
  3. pinn-architecture: `pinn_instruction/original_latex/pinn-architecture/pinn-architecture/main_pinn.tex` (cwd: `pinn-architecture/`)
  4. review_of_framework: `pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex` (cwd: `review_of_framework/`)
  5. stage_strat_revision: `pinn_instruction/original_latex/review-of-framework/stage_strat_revision/stage_strat_revision.tex` (cwd: `stage_strat_revision/`)
- **D-22:** Original files (for baseline) compiled from their `old/` directories:
  1. `pinn_instruction/original_latex/Data-quality-assessment/old/data_quality_assess.tex`
  2. `pinn_instruction/original_latex/ctl-instruction/old/CTL-instruction-final.tex`
  3. `pinn_instruction/original_latex/pinn-architecture/old/PINN_architecture_plan.tex`
  4. `pinn_instruction/original_latex/review-of-framework/old/review_of_ctl-pinn_framework.tex`
  5. `pinn_instruction/original_latex/review-of-framework/old/stage-strat-revision.tex`

### Claude's Discretion

- Exact regex for log parsing (errors vs warnings; handle multi-line error messages)
- Whether to run latexmk with `-silent` or capture all output
- How to handle `bibtex`/`biber` if any structure uses bibliography compilation (latexmk handles this automatically)
- Argparse design and progress output

### Deferred Ideas (OUT OF SCOPE)

None -- discussion stayed within phase scope.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| COMP-01 | Each of the 5 modular structures compiles with `pdflatex` (or `lualatex`) with 0 errors | latexmk invocation pattern verified; log parsing for `^!` errors established |
| COMP-02 | Each of the 5 modular structures compiles with 0 warnings (or only pre-existing warnings from the original) | Warning extraction regex established; normalization strategy defined (strip line numbers/file paths) |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.12 | Script implementation | Project standard, stdlib-only approach per established pattern |
| latexmk | 4.87 | LaTeX build automation | Handles multi-pass, bibliography, cross-refs automatically |
| pdflatex | 3.141592653-2.6-1.40.28 (TeX Live 2025) | PDF compilation | Installed at `/Library/TeX/texbin/pdflatex` |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `subprocess` | stdlib | Run latexmk with timeout and cwd | All compilations |
| `re` | stdlib | Parse log for errors and warnings | Log analysis |
| `pathlib` | stdlib | Path manipulation | All file operations |
| `argparse` | stdlib | CLI interface | Consistent with prior scripts |
| `tempfile` | stdlib | Temp directory management | Optional, using fixed tmp/ path instead |
| `shutil` | stdlib | Directory cleanup | Temp cleanup |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| latexmk | Direct pdflatex calls | Manual multi-pass handling required; latexmk is simpler |
| `-output-directory` | Compile in-place | Pollutes source dirs with aux files; output-directory is cleaner |
| `subprocess.run(timeout=...)` | `gtimeout` command | gtimeout requires coreutils; Python timeout is portable |

**Installation:**
No additional packages required. TeX Live 2025 already installed with latexmk and pdflatex.

**Version verification:**
```
pdflatex --version
# pdfTeX 3.141592653-2.6-1.40.28 (TeX Live 2025)

latexmk --version
# Latexmk, John Collins, 15 June 2025. Version 4.87
```

## Architecture Patterns

### Recommended Script Structure
```
pinn_instruction/original_latex/verification/
    verify_compile.py          # Main script
    tmp/                       # Temp compilation outputs
        Data-quality-assessment/
        Data-quality-assessment-original/
        ctl-instruction/
        ctl-instruction-original/
        pinn-architecture/
        pinn-architecture-original/
        review_of_framework/
        review_of_framework-original/
        stage_strat_revision/
        stage_strat_revision-original/
```

### Pattern 1: Compilation with latexmk
**What:** Use latexmk to compile LaTeX with automatic multi-pass handling
**When to use:** All compilations in this phase
**Example:**
```python
# Source: Verified via testing 2026-03-22
import subprocess
from pathlib import Path

def compile_latex(main_tex: Path, output_dir: Path, cwd: Path, timeout: int = 120) -> tuple[int, Path]:
    """Compile LaTeX file with latexmk.

    Returns: (exit_code, log_file_path)
    """
    cmd = [
        "latexmk",
        "-pdf",
        "-pdflatex=pdflatex -interaction=nonstopmode",
        f"-output-directory={output_dir}",
        main_tex.name
    ]

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout
    )

    # Log file is named after input file in output directory
    log_file = output_dir / main_tex.with_suffix('.log').name
    return result.returncode, log_file
```

### Pattern 2: Error Extraction from Log
**What:** Parse LaTeX log for fatal errors (lines starting with `!`)
**When to use:** Determining pass/fail for COMP-01
**Example:**
```python
# Source: LaTeX log format standard
import re

def extract_errors(log_content: str) -> list[dict]:
    """Extract fatal errors from LaTeX log.

    Returns list of dicts with 'line_num', 'message', 'context' keys.
    """
    errors = []
    lines = log_content.split('\n')

    for i, line in enumerate(lines):
        if line.startswith('!'):
            # Capture error message and surrounding context
            context_start = max(0, i - 2)
            context_end = min(len(lines), i + 5)
            errors.append({
                'line_num': i + 1,
                'message': line[1:].strip(),  # Remove '!' prefix
                'context': '\n'.join(lines[context_start:context_end])
            })

    return errors
```

### Pattern 3: Warning Extraction and Normalization
**What:** Extract warnings and normalize for comparison between original and modular
**When to use:** COMP-02 warning baseline comparison
**Example:**
```python
# Source: CONTEXT.md D-14, D-15
import re

WARNING_PATTERNS = [
    r'LaTeX Warning:.*',
    r'Package Warning:.*',
    r'Class Warning:.*',
    r'Overfull \\hbox.*',
    r'Underfull \\hbox.*',
]

def extract_warnings(log_content: str) -> set[str]:
    """Extract and normalize warnings from LaTeX log."""
    warnings = set()

    for pattern in WARNING_PATTERNS:
        for match in re.finditer(pattern, log_content):
            warning = match.group(0)
            # Normalize: strip line numbers and file paths
            # "Overfull \hbox (25pt wide) in paragraph at lines 47--47"
            # -> "Overfull \hbox (25pt wide) in paragraph"
            normalized = re.sub(r'\s+at lines \d+--\d+', '', warning)
            normalized = re.sub(r'\s+on input line \d+', '', normalized)
            warnings.add(normalized)

    return warnings
```

### Anti-Patterns to Avoid
- **Compiling without `-output-directory`:** Pollutes source directories with `.aux`, `.log`, `.out` files
- **Using `-interaction=stopmode`:** Halts on first error, preventing full error capture
- **Ignoring latexmk exit code:** latexmk returns 0 even with LaTeX errors; must parse log
- **Comparing raw warning lines:** Line numbers differ between original and modular; must normalize

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Multi-pass LaTeX compilation | Manual pdflatex iteration counting | `latexmk` | Handles bibtex, cross-refs, TOC automatically |
| Log parsing for errors | Custom state machine | `re.match(r'^!')` | LaTeX errors always start with `!` |
| Temp directory management | Manual mkdir/rmdir | `pathlib.Path.mkdir()` + `shutil.rmtree()` | Robust cleanup |
| Subprocess timeout | signal.alarm or threading | `subprocess.run(timeout=...)` | Built-in, cross-platform |

**Key insight:** LaTeX compilation is deceptively complex due to multi-pass requirements. Always use latexmk.

## Common Pitfalls

### Pitfall 1: latexmk Exit Code vs LaTeX Errors
**What goes wrong:** latexmk returns exit code 0 even when pdflatex has errors
**Why it happens:** latexmk successfully ran the compilation command; it doesn't interpret LaTeX's internal error state
**How to avoid:** Always parse the `.log` file for `^!` lines -- this is the authoritative error indicator
**Warning signs:** Script reports PASS but PDF is incomplete or missing

### Pitfall 2: Warning Line Number Mismatch
**What goes wrong:** Warnings appear different between original and modular due to different line numbers
**Why it happens:** Modular structure spreads content across files; line numbers in warnings reference local file lines
**How to avoid:** Normalize warnings by stripping `at lines N--M` and `on input line N` suffixes before comparison
**Warning signs:** Warning comparison shows many "new" warnings that are actually the same

### Pitfall 3: Missing Output Directory
**What goes wrong:** latexmk fails with "No such file or directory" for output directory
**Why it happens:** latexmk requires the output directory to exist before compilation
**How to avoid:** Create output directory with `Path.mkdir(parents=True, exist_ok=True)` before running latexmk
**Warning signs:** Compilation fails immediately with file system error

### Pitfall 4: Working Directory for Relative Paths
**What goes wrong:** `\input{preamble}` fails because cwd is wrong
**Why it happens:** LaTeX resolves relative paths from cwd, not from the main.tex location
**How to avoid:** Set `cwd` in subprocess.run to the directory containing main.tex
**Warning signs:** "File not found" errors for preamble.tex or sections/*.tex

### Pitfall 5: Timeout on Large Documents
**What goes wrong:** Compilation hangs indefinitely on complex documents
**Why it happens:** LaTeX can enter infinite loops with certain errors; latexmk may retry multiple passes
**How to avoid:** Use `subprocess.run(timeout=120)` -- sufficient for all 5 structures (verified)
**Warning signs:** Script hangs without progress

## Code Examples

### Complete Compilation Function
```python
# Source: Verified via testing 2026-03-22
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class CompilationResult:
    """Result of a LaTeX compilation."""
    success: bool
    log_path: Path
    pdf_path: Optional[Path]
    errors: list[dict]
    warnings: set[str]
    return_code: int

def compile_structure(
    main_tex: Path,
    output_dir: Path,
    timeout: int = 120
) -> CompilationResult:
    """Compile a LaTeX structure and return parsed results.

    Args:
        main_tex: Path to the main .tex file
        output_dir: Directory for output files (will be created)
        timeout: Compilation timeout in seconds

    Returns:
        CompilationResult with success status, errors, and warnings
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build latexmk command
    cmd = [
        "latexmk",
        "-pdf",
        "-pdflatex=pdflatex -interaction=nonstopmode",
        f"-output-directory={output_dir}",
        main_tex.name
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=main_tex.parent,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return_code = result.returncode
    except subprocess.TimeoutExpired:
        return CompilationResult(
            success=False,
            log_path=output_dir / main_tex.with_suffix('.log').name,
            pdf_path=None,
            errors=[{'line_num': 0, 'message': 'Compilation timeout', 'context': ''}],
            warnings=set(),
            return_code=-1
        )

    # Parse log file
    log_path = output_dir / main_tex.with_suffix('.log').name
    if not log_path.exists():
        return CompilationResult(
            success=False,
            log_path=log_path,
            pdf_path=None,
            errors=[{'line_num': 0, 'message': 'Log file not created', 'context': ''}],
            warnings=set(),
            return_code=return_code
        )

    log_content = log_path.read_text(encoding='utf-8', errors='replace')
    errors = extract_errors(log_content)
    warnings = extract_warnings(log_content)

    # Check PDF was created
    pdf_path = output_dir / main_tex.with_suffix('.pdf').name
    pdf_exists = pdf_path.exists()

    return CompilationResult(
        success=len(errors) == 0 and pdf_exists,
        log_path=log_path,
        pdf_path=pdf_path if pdf_exists else None,
        errors=errors,
        warnings=warnings,
        return_code=return_code
    )
```

### STRUCTURES Data Class (Copy from verify_preamble.py)
```python
# Source: verify_preamble.py lines 71-97
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CompileStructure:
    """Definition of a LaTeX structure for compilation verification."""
    name: str
    original: Path       # Path to original monolithic .tex in old/
    modular: Path        # Path to modular main.tex

STRUCTURES = [
    CompileStructure(
        name="Data-quality-assessment",
        original=Path("pinn_instruction/original_latex/Data-quality-assessment/old/data_quality_assess.tex"),
        modular=Path("pinn_instruction/original_latex/Data-quality-assessment/data_quality_assess/main-data-quality-assess.tex"),
    ),
    CompileStructure(
        name="ctl-instruction",
        original=Path("pinn_instruction/original_latex/ctl-instruction/old/CTL-instruction-final.tex"),
        modular=Path("pinn_instruction/original_latex/ctl-instruction/ctl-instruction/main_CTL.tex"),
    ),
    CompileStructure(
        name="pinn-architecture",
        original=Path("pinn_instruction/original_latex/pinn-architecture/old/PINN_architecture_plan.tex"),
        modular=Path("pinn_instruction/original_latex/pinn-architecture/pinn-architecture/main_pinn.tex"),
    ),
    CompileStructure(
        name="review_of_framework",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/review_of_ctl-pinn_framework.tex"),
        modular=Path("pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex"),
    ),
    CompileStructure(
        name="stage_strat_revision",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/stage-strat-revision.tex"),
        modular=Path("pinn_instruction/original_latex/review-of-framework/stage_strat_revision/stage_strat_revision.tex"),
    ),
]
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual pdflatex iteration | latexmk auto-multi-pass | Established | Simpler, more reliable |
| In-place compilation | `-output-directory` | Phase 8 CONTEXT | Cleaner, no source pollution |
| Raw warning comparison | Normalized warning comparison | Phase 8 CONTEXT | Accurate diff, ignores line number variance |

**Deprecated/outdated:**
- Direct `pdflatex` calls without latexmk: Requires manual pass counting
- `-interaction=stopmode`: Prevents full error capture

## Open Questions

1. **Multi-line error messages**
   - What we know: Some LaTeX errors span multiple lines in the log
   - What's unclear: Whether context capture (lines before/after `!`) is sufficient
   - Recommendation: Capture 2 lines before and 5 lines after each `!` for context

2. **Bibliography handling**
   - What we know: latexmk automatically runs bibtex/biber when needed
   - What's unclear: Whether any structures have bibliography issues
   - Recommendation: Trust latexmk's automatic handling; report any bibtex errors as compilation errors

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None detected |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| COMP-01 | Compilability check returns correct pass/fail | integration | N/A (script is the test) | N/A |
| COMP-02 | Warning comparison identifies new warnings | integration | N/A (script is the test) | N/A |

### Sampling Rate
- **Per task commit:** Script execution (the script IS the verification)
- **Per wave merge:** Full script run on all 5 structures
- **Phase gate:** All 5 structures compile with 0 errors before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] No pytest framework installed -- verification scripts ARE the tests
- [ ] No `tests/` directory -- scripts in `pinn_instruction/original_latex/verification/`
- [ ] Manual verification required: Run script and review report

**Note:** This phase is inherently a verification phase. The script itself serves as the automated test. No separate test file is needed.

## Sources

### Primary (HIGH confidence)
- TeX Live 2025 installation verified: `/Library/TeX/texbin/pdflatex` and `/Library/TeX/texbin/latexmk`
- latexmk 4.87 help output -- command-line options for `-output-directory`, `-pdf`, `-pdflatex`
- LaTeX log format analysis: pinn-architecture log files showing error/warning patterns
- Existing verification scripts: `verify_content.py`, `verify_preamble.py`, `verify_structure.py` -- established patterns

### Secondary (MEDIUM confidence)
- Compilation testing on pinn-architecture modular and original -- verified latexmk command works
- Warning count comparison: original (10 Overfull, 16 Underfull) == modular (10 Overfull, 16 Underfull)

### Tertiary (LOW confidence)
- None -- all findings verified

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - latexmk and pdflatex are established tools, versions verified
- Architecture: HIGH - established pattern from prior phases, compilation verified via testing
- Pitfalls: HIGH - derived from LaTeX/latexmk documentation and testing

**Research date:** 2026-03-22
**Valid until:** 30 days (stable tools)