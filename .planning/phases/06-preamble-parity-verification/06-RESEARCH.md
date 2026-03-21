# Phase 6: Preamble Parity Verification - Research

**Researched:** 2026-03-21
**Domain:** Python LaTeX preamble parsing, regex-based declaration extraction, set comparison
**Confidence:** HIGH

## Summary

This phase requires building a Python script (`verify_preamble.py`) that extracts and compares all preamble declarations between original monolithic LaTeX files and their modular preamble files for each of the 5 structures. The preamble contains three categories of declarations that must be verified: (1) `\usepackage` declarations with exact options, (2) custom command definitions (`\newcommand`, `\renewcommand`, `\DeclareMathOperator`), and (3) custom environment definitions (`\newenvironment`). Additionally, package configuration blocks (`\hypersetup`, `\geometry`, `\lstset`, `\lstdefinestyle`, `\definecolor`, `\setcitestyle`, `\usetikzlibrary`) must be compared for exact parity.

The core technical challenge is preamble extraction: the original monolithic files have everything inline before `\begin{document}`, while modular versions split the preamble across `main.tex` (containing `\documentclass` and sometimes packages like geometry/inputenc/fontenc) and a separate `preamble.tex` (containing the domain-specific packages, macros, and configurations). One structure (Data-quality-assessment) has a particularly complex split where some packages appear in `main.tex` alongside `\documentclass` but NOT in `preamble.tex`. The verification script must combine `main.tex` pre-`\begin{document}` content with the resolved `\input{preamble}` content to form the complete "modular preamble."

**Primary recommendation:** Extract preamble content from original files (everything between `\documentclass` and `\begin{document}`), combine modular main.tex pre-document content with resolved preamble.tex, then parse each using regex to extract structured declarations. Compare declarations as normalized sets with exact option matching. Report matches, mismatches, and missing items in a Markdown report following the same format as Phase 5.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PREAMB-01 | All `\usepackage` declarations from original preamble appear in modular preamble for each structure | Regex extraction of `\usepackage[opts]{pkg}` from both sides, normalized comparison with comma-separated package splitting (e.g., `{amsmath, amssymb, amsfonts}` treated as 3 separate packages). Report per-structure with missing/extra packages flagged. |
| PREAMB-02 | All custom `\newcommand`, `\renewcommand`, `\newenvironment` definitions preserved | Regex extraction including `\DeclareMathOperator` (used in ctl-instruction). Full definition body comparison, not just command name, to catch option count or body differences. |
| PREAMB-03 | Package options (e.g., `[H]` for float, encoding options) match exactly | Options extracted as part of `\usepackage[options]{package}` parsing. Exact string match on options after whitespace normalization. Mismatches flagged with both original and modular values shown side-by-side. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.12.2 | Runtime environment | Project standard, same as Phase 5 |
| re | (built-in) | Regex-based LaTeX declaration extraction | Handles all preamble constructs; project uses regex extensively |
| pathlib.Path | (built-in) | File path handling | Project standard across all scripts |
| dataclasses | (built-in) | Structure and declaration data models | Used in Phase 5 for Structure definitions |
| argparse | (built-in) | CLI argument parsing | Consistent with Phase 5 script interface |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| difflib | (built-in) | Text comparison for multi-line config blocks | For comparing `\hypersetup{}`, `\lstset{}`, and other multi-line blocks |
| datetime | (built-in) | Report timestamp | For generated report metadata |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Custom regex parsing | pylatexenc library | External dependency; our preambles are simple enough for regex |
| Custom regex parsing | TexSoup library | External dependency; overkill for preamble-only parsing |
| Set comparison | difflib.SequenceMatcher | Set comparison is more appropriate since declaration order doesn't matter |

**Installation:**
No installation required -- all dependencies are Python built-in modules.

**Version verification:**
```bash
python3 --version
# Python 3.12.2
```

## Architecture Patterns

### Recommended Project Structure
```
pinn_instruction/original_latex/
  verification/
    verify_content.py              # Phase 5 (exists)
    content_verification_report.md # Phase 5 output (exists)
    verify_preamble.py             # Phase 6 script (NEW)
    preamble_verification_report.md # Phase 6 output (NEW)
```

### Pattern 1: Preamble Extraction from Original Monolithic Files
**What:** Extract everything between `\documentclass` (inclusive) and `\begin{document}` (exclusive) from the original monolithic .tex file.
**When to use:** For all 5 original files.
**Key insight:** The "preamble" in LaTeX is everything between `\documentclass{}` and `\begin{document}`. This includes `\usepackage` declarations, configuration blocks (`\hypersetup{}`, `\geometry{}`, `\lstset{}`), custom command definitions, and metadata (`\title{}`, `\author{}`, `\date{}`).
**Example:**
```python
def extract_preamble(content: str) -> str:
    """Extract preamble: content between \\documentclass and \\begin{document}.

    Returns the preamble text, including \\documentclass line but excluding
    \\begin{document} line.
    """
    lines = content.split('\n')
    start = None
    end = None
    for i, line in enumerate(lines):
        if re.match(r'\s*\\documentclass', line) and start is None:
            start = i
        if re.match(r'\s*\\begin\{document\}', line):
            end = i
            break
    if start is not None and end is not None:
        return '\n'.join(lines[start:end])
    return ''
```

### Pattern 2: Modular Preamble Assembly
**What:** Combine `main.tex` preamble section with resolved `\input{preamble}` content to form the complete modular preamble.
**When to use:** For modular structures where preamble is split between main.tex and preamble.tex.
**Key insight:** The modular "preamble" is NOT just preamble.tex. It's the union of:
  1. Everything in main.tex before `\begin{document}` (includes `\documentclass`, possibly some packages, `\title`, `\author`, `\date`)
  2. The content of the file referenced by `\input{preamble...}` in main.tex

For Data-quality-assessment, this is particularly important: main.tex contains `\documentclass`, geometry, inputenc, fontenc, lmodern, babel packages inline, PLUS `\input{preamble}` which has the rest. Without combining both, packages from main.tex would appear "missing" from the modular preamble.

**Special cases by structure:**
- **Data-quality-assessment:** preamble.tex does NOT contain `\documentclass`; main.tex has it inline with some packages
- **ctl-instruction:** preamble_CTL.tex CONTAINS `\documentclass` -- the main.tex just does `\input{preamble_CTL}`. The entire preamble is self-contained in preamble_CTL.tex
- **pinn-architecture:** preamble.tex does NOT contain `\documentclass`; main.tex has `\documentclass{article}` then `\input{preamble}`
- **review_of_framework:** preamble.tex does NOT contain `\documentclass`; main.tex has `\documentclass[11pt, a4paper]{article}` then `\input{preamble}`
- **stage_strat_revision:** preamble.tex does NOT contain `\documentclass`; main.tex has `\documentclass[11pt, letterpaper]{article}` then `\input{preamble}`

**Example:**
```python
def assemble_modular_preamble(main_content: str, main_dir: Path) -> str:
    """Assemble the full modular preamble by resolving \\input{preamble...}.

    Reads main.tex, resolves any \\input{preamble*} directives, and returns
    the combined preamble content (everything before \\begin{document}).
    """
    # Resolve \input{} directives in main_content
    resolved = resolve_preamble_inputs(main_content, main_dir)
    # Extract preamble from the resolved content
    return extract_preamble(resolved)
```

### Pattern 3: \usepackage Declaration Parsing
**What:** Parse `\usepackage[options]{package}` declarations, handling comma-separated packages and multi-line option blocks.
**When to use:** For PREAMB-01 and PREAMB-03 verification.
**Key insight:** Some files use `\usepackage{amsmath, amssymb, amsfonts}` (comma-separated), which is equivalent to three separate `\usepackage` calls. The parser must split these into individual package entries. Options must be preserved exactly for PREAMB-03.
**Example:**
```python
@dataclass
class PackageDecl:
    """A single \\usepackage declaration."""
    name: str           # e.g., "amsmath"
    options: str = ""   # e.g., "utf8" or "dvipsnames" or ""

def parse_usepackage(preamble: str) -> list[PackageDecl]:
    """Extract all \\usepackage declarations from preamble text.

    Handles:
    - \\usepackage{package}
    - \\usepackage[options]{package}
    - \\usepackage{pkg1, pkg2, pkg3} (comma-separated)
    """
    pattern = re.compile(
        r'\\usepackage'
        r'(?:\[([^\]]*)\])?'   # Optional [options]
        r'\{([^}]+)\}',        # {package(s)}
        re.MULTILINE
    )

    results = []
    for match in pattern.finditer(preamble):
        options = (match.group(1) or '').strip()
        packages_str = match.group(2)

        # Split comma-separated packages
        packages = [p.strip() for p in packages_str.split(',')]
        for pkg in packages:
            if pkg:  # Skip empty strings
                results.append(PackageDecl(name=pkg, options=options))

    return results
```

### Pattern 4: Command/Environment Definition Parsing
**What:** Extract `\newcommand`, `\renewcommand`, `\newenvironment`, and `\DeclareMathOperator` definitions with their full bodies.
**When to use:** For PREAMB-02 verification.
**Key insight:** These definitions vary in complexity:
- Simple: `\newcommand{\vect}[1]{\mathbf{#1}}`
- Multi-line: `\newenvironment{authcommentenv}{\par\begingroup...}{]\endgroup\par}`
- Operator: `\DeclareMathOperator{\median}{median}`
- Renewcommand: `\renewcommand\theadfont{\bfseries}`

The parser needs brace-depth tracking for multi-line definitions. For verification purposes, comparing the full definition text (normalized for whitespace) is more robust than parsing internal structure.

**Example:**
```python
@dataclass
class CommandDef:
    """A custom command or environment definition."""
    kind: str        # "newcommand", "renewcommand", "newenvironment", "DeclareMathOperator"
    name: str        # e.g., "\\vect", "authcommentenv", "\\median"
    full_text: str   # The complete definition text for comparison
```

### Pattern 5: Configuration Block Comparison
**What:** Compare multi-line configuration blocks like `\hypersetup{...}`, `\geometry{...}`, `\lstset{...}`, etc.
**When to use:** For PREAMB-03 (package options/configuration must match exactly).
**Key insight:** These blocks are semantically part of the preamble but are not `\usepackage` declarations. They configure packages that were loaded via `\usepackage`. The script should:
1. Extract the full block (handling nested braces)
2. Normalize whitespace within the block
3. Compare the normalized text

Configuration block types found across the 5 structures:
- `\hypersetup{...}` -- 4 of 5 structures (not pinn-architecture)
- `\geometry{...}` -- 4 of 5 structures (not data-quality-assessment, which uses geometry package option)
- `\lstset{...}` -- 4 of 5 structures (not data-quality-assessment)
- `\lstdefinestyle{name}{...}` -- 2 structures (review_of_framework, stage_strat_revision)
- `\definecolor{name}{...}{...}` -- 2 structures (review_of_framework, stage_strat_revision)
- `\setcitestyle{...}` -- 1 structure (pinn-architecture)
- `\usetikzlibrary{...}` -- 1 structure (ctl-instruction)

### Pattern 6: Reuse Phase 5 Structure Definitions
**What:** Reuse the same 5-structure mapping from Phase 5's verify_content.py.
**When to use:** For consistency across verification scripts.
**Key insight:** The `Structure` dataclass and `STRUCTURES` list from Phase 5 can be adapted. Phase 6 needs the same original/modular path mappings. The preamble-specific fields (like which preamble file to look for) can be added.

### Anti-Patterns to Avoid
- **Parsing only preamble.tex and ignoring main.tex:** The modular preamble is split across BOTH files. Failing to combine them will report false "missing" packages (especially for Data-quality-assessment where geometry, inputenc, fontenc, lmodern, babel are in main.tex).
- **Treating comma-separated packages as a single package:** `\usepackage{amsmath, amssymb, amsfonts}` is THREE packages, not one. Must split on commas.
- **Ignoring \documentclass options:** `\documentclass[11pt, a4paper]{article}` vs `\documentclass{article}` is a meaningful difference. The `\documentclass` line should be compared but is not a `\usepackage`.
- **Forgetting configuration blocks:** `\hypersetup`, `\lstset`, `\geometry` etc. are not packages but are part of the preamble configuration that must match. PREAMB-03 specifically requires "package options" to match -- this extends to package configuration blocks.
- **Not normalizing trailing whitespace in options:** The original `filecolor=magenta,      ` (with trailing spaces) vs modular `filecolor=magenta,` should be treated as equal.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Brace-depth matching for multi-line blocks | Character-by-character state machine | Simple depth counter with string accumulation | LaTeX braces are simple: increment on `{`, decrement on `}`, no escape handling needed (LaTeX uses `\{` for literal braces, but these don't appear in preamble declarations) |
| Package list comparison | Ordered list comparison | Set comparison with frozenset | Package loading order rarely matters in LaTeX; what matters is presence and options |
| Multi-line text comparison | Custom diff | `difflib.unified_diff()` for config blocks | Same approach proven in Phase 5 |

**Key insight:** The preamble parsing problem is well-suited to regex because LaTeX preambles follow predictable patterns. The constructs are: `\usepackage[opts]{pkg}`, `\newcommand{name}[nargs]{body}`, `\newenvironment{name}{begin}{end}`, and configuration blocks `\command{...}`. All can be captured with regex + brace-depth counting.

## Common Pitfalls

### Pitfall 1: Data-quality-assessment Split Preamble
**What goes wrong:** The modular Data-quality-assessment has packages in BOTH main.tex (geometry, inputenc, fontenc, lmodern, babel) AND preamble.tex (amsmath, amssymb, booktabs, hyperref, enumitem, xcolor). If only preamble.tex is parsed, 5 packages appear missing.
**Why it happens:** This structure was modularized differently from the others -- it kept some "universal" packages in main.tex alongside `\documentclass`.
**How to avoid:** Always assemble the complete modular preamble by resolving `\input{preamble}` in main.tex FIRST, then extracting everything before `\begin{document}` from the resolved content.
**Warning signs:** Data-quality-assessment shows 5+ missing packages while others show 0.

### Pitfall 2: ctl-instruction Preamble Contains \documentclass
**What goes wrong:** The ctl-instruction's `preamble_CTL.tex` contains the `\documentclass{article}` line (unusual -- other structures put this only in main.tex). If the parser expects preamble.tex to NOT have `\documentclass`, it may mishandle this structure.
**Why it happens:** The modularization for ctl-instruction was done differently -- preamble_CTL.tex is self-contained with documentclass.
**How to avoid:** Use the "resolve input then extract preamble" approach uniformly. The main_CTL.tex is just `\input{preamble_CTL}\n\begin{document}\n...`. Resolving the input produces a normal file with `\documentclass` at top.
**Warning signs:** `\documentclass` appears twice or preamble extraction fails for ctl-instruction.

### Pitfall 3: Comma-Separated Packages
**What goes wrong:** `\usepackage{amsmath, amssymb, amsfonts}` in stage_strat_revision is treated as one "package" named "amsmath, amssymb, amsfonts" instead of three separate packages.
**Why it happens:** Naive regex captures the entire `{...}` content as one package name.
**How to avoid:** After extracting the package string, split on commas and strip whitespace. Each resulting name is a separate package.
**Warning signs:** "amsmath, amssymb, amsfonts" appears as a single missing/extra package, and "amsmath" appears separately.

### Pitfall 4: \renewcommand Without Braces Around Name
**What goes wrong:** ctl-instruction has `\renewcommand\theadfont{\bfseries}` (no braces around `\theadfont`). A regex expecting `\renewcommand{name}` will miss this.
**Why it happens:** LaTeX allows `\renewcommand\cmd{body}` as a shorthand for `\renewcommand{\cmd}{body}`.
**How to avoid:** The regex pattern must handle both `\renewcommand{\\cmd}` and `\renewcommand\\cmd` (with or without braces around the command name).
**Warning signs:** `\renewcommand\theadfont` not detected in ctl-instruction preamble.

### Pitfall 5: Title/Author/Date as Preamble Content
**What goes wrong:** `\title{}`, `\author{}`, and `\date{}` appear in the preamble (before `\begin{document}`) but are metadata, not packages or commands. If the script tries to compare these, differences in how they're split between main.tex and preamble.tex will cause false mismatches.
**Why it happens:** Different structures place `\title`/`\author`/`\date` differently -- some in main.tex, some in preamble_CTL.tex.
**How to avoid:** Explicitly exclude `\title{}`, `\author{}`, `\date{}` from the comparison scope. These are not packages, macros, or commands -- they're document metadata. The requirements (PREAMB-01, -02, -03) specifically target packages and command definitions, not metadata.
**Warning signs:** Title/author/date differences reported as preamble mismatches.

### Pitfall 6: Whitespace Differences in Configuration Blocks
**What goes wrong:** The original `stage-strat-revision.tex` has `filecolor=magenta,      ` (trailing spaces after comma) while the modular version has `filecolor=magenta,` (no trailing spaces). This should NOT be flagged as a mismatch.
**Why it happens:** Manual editing introduced whitespace differences.
**How to avoid:** Normalize all configuration block content: strip trailing whitespace per line, collapse multiple spaces to one, before comparing.
**Warning signs:** Spurious mismatches in `\hypersetup` or `\lstset` blocks due to trailing whitespace.

## Code Examples

Verified patterns from project source analysis:

### Complete Verification Flow
```python
#!/usr/bin/env python3
"""
verify_preamble.py

Phase 6: Preamble Parity Verification
Verifies that all package declarations, custom commands, and package options
from original monolithic .tex preambles are preserved in the modular preambles
for all 5 structures.

Usage:
    python verify_preamble.py                    # Verify all 5 structures
    python verify_preamble.py --structure pinn   # Verify specific structure
    python verify_preamble.py --verbose          # Show progress
"""

import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class PackageDecl:
    """A single \\usepackage declaration."""
    name: str
    options: str = ""

    def normalized_key(self) -> str:
        """Return a normalized key for comparison."""
        return f"[{self.options}]{{{self.name}}}" if self.options else f"{{{self.name}}}"


@dataclass
class CommandDef:
    """A custom command or environment definition."""
    kind: str        # newcommand, renewcommand, newenvironment, DeclareMathOperator
    name: str        # Command or environment name
    full_text: str   # Full definition text for comparison


@dataclass
class ConfigBlock:
    """A package configuration block (\\hypersetup, \\lstset, etc.)."""
    command: str     # e.g., "hypersetup", "lstset", "geometry"
    content: str     # The full block content (normalized)


@dataclass
class PreambleData:
    """Parsed preamble contents."""
    documentclass: str = ""           # Full \documentclass line
    packages: List[PackageDecl] = field(default_factory=list)
    commands: List[CommandDef] = field(default_factory=list)
    config_blocks: List[ConfigBlock] = field(default_factory=list)
```

### Brace-Depth Block Extraction
```python
def extract_braced_block(content: str, start_pos: int) -> tuple[str, int]:
    """Extract a brace-delimited block starting at the first '{' from start_pos.

    Args:
        content: Full text
        start_pos: Position to start searching for '{'

    Returns:
        Tuple of (block content including braces, end position)
    """
    # Find the opening brace
    brace_start = content.index('{', start_pos)
    depth = 0
    pos = brace_start

    while pos < len(content):
        if content[pos] == '{':
            depth += 1
        elif content[pos] == '}':
            depth -= 1
            if depth == 0:
                return content[brace_start:pos + 1], pos + 1
        pos += 1

    # Unmatched brace - return what we have
    return content[brace_start:], len(content)
```

### Package Comparison Logic
```python
def compare_packages(
    original: list[PackageDecl],
    modular: list[PackageDecl]
) -> dict:
    """Compare two lists of package declarations.

    Returns dict with:
        matched: list of packages present in both with same options
        missing: list of packages in original but not in modular
        extra: list of packages in modular but not in original
        option_mismatches: list of packages present in both but with different options
    """
    orig_by_name = {p.name: p for p in original}
    mod_by_name = {p.name: p for p in modular}

    matched = []
    missing = []
    extra = []
    option_mismatches = []

    for name, orig_pkg in orig_by_name.items():
        if name in mod_by_name:
            mod_pkg = mod_by_name[name]
            if orig_pkg.options == mod_pkg.options:
                matched.append(orig_pkg)
            else:
                option_mismatches.append({
                    'name': name,
                    'original_options': orig_pkg.options,
                    'modular_options': mod_pkg.options,
                })
        else:
            missing.append(orig_pkg)

    for name, mod_pkg in mod_by_name.items():
        if name not in orig_by_name:
            extra.append(mod_pkg)

    return {
        'matched': matched,
        'missing': missing,
        'extra': extra,
        'option_mismatches': option_mismatches,
    }
```

## Concrete Preamble Inventory (from source analysis)

The following is an exhaustive inventory of every preamble construct found in all 5 structures, verified by reading the actual files. This inventory defines exactly what the verification script must detect.

### Structure 1: Data-quality-assessment

**Original (`data_quality_assess.tex`):**
- `\documentclass[11pt, a4paper]{article}`
- Packages (11): geometry[a4paper, top=2.5cm, bottom=2.5cm, left=2cm, right=2cm], inputenc[utf8], fontenc[T1], lmodern, babel[english], amsmath, amssymb, booktabs, hyperref, enumitem, xcolor
- Commands (2): `\newcommand{\vect}[1]{\mathbf{#1}}`, `\newcommand{\norm}[1]{\left\lVert#1\right\rVert}`
- Config blocks (1): `\hypersetup{colorlinks=true, linkcolor=blue, filecolor=magenta, urlcolor=cyan, citecolor=red}`

**Modular (main.tex + preamble.tex combined):**
- Same 11 packages (5 in main.tex, 6 in preamble.tex)
- Same 2 commands (in preamble.tex)
- Same hypersetup (in preamble.tex)

### Structure 2: ctl-instruction

**Original (`CTL-instruction-final.tex`):**
- `\documentclass{article}`
- Packages (15): inputenc[utf8], amsmath, amssymb, booktabs, geometry, hyperref, comment, url, algorithm, algpseudocode, listings, float, makecell, xcolor[dvipsnames], tikz
- Commands (1): `\newcommand{\authcomment}[1]{\textcolor{Red}{\textbf{[#1]}}}`
- Renewcommands (1): `\renewcommand\theadfont{\bfseries}`
- Environments (1): `\newenvironment{authcommentenv}{...}{...}`
- Operators (1): `\DeclareMathOperator{\median}{median}`
- Config blocks (3): `\hypersetup{...}`, `\geometry{a4paper, margin=1in}`, `\lstset{showstringspaces=false}`
- TikZ (1): `\usetikzlibrary{shapes.geometric, arrows.meta, positioning}`

**Modular (preamble_CTL.tex -- self-contained, includes \documentclass):**
- Identical content -- preamble_CTL.tex is a verbatim copy of the original preamble

### Structure 3: pinn-architecture

**Original (`PINN_architecture_plan.tex`):**
- `\documentclass{article}`
- Packages (15): inputenc[utf8], amsmath, amssymb, booktabs, geometry, hyperref, natbib, enumitem, tabularx, float, placeins, longtable, comment, listings, xcolor
- Commands (1): `\newcommand{\authcomment}[1]{\textcolor{red}{\textbf{[#1]}}}`
- Config blocks (3): `\geometry{a4paper, margin=1in}`, `\lstset{...}`, `\setcitestyle{super,open={},close={}}`

**Modular (main.tex `\documentclass` + preamble.tex):**
- preamble.tex has all 15 packages, the command, and all 3 config blocks
- main.tex has `\documentclass{article}` only (plus `\input{preamble}`)

### Structure 4: review_of_framework

**Original (`review_of_ctl-pinn_framework.tex`):**
- `\documentclass[11pt, a4paper]{article}`
- Packages (14): inputenc[utf8], amsmath, amssymb, amsfonts, graphicx, booktabs, longtable, geometry, hyperref, listings, xcolor, enumitem, float, caption
- Commands (0)
- Config blocks (4): `\geometry{a4paper, margin=1in}`, `\hypersetup{...}`, `\lstdefinestyle{mystyle}{...}`, `\lstset{style=mystyle}`
- Colors (4): `\definecolor{codegreen}`, `\definecolor{codegray}`, `\definecolor{codepurple}`, `\definecolor{backcolour}`

**Modular (main.tex `\documentclass[11pt, a4paper]{article}` + preamble.tex):**
- preamble.tex has all 14 packages, all config blocks, all color definitions
- main.tex has `\documentclass[11pt, a4paper]{article}` + `\input{preamble}`

### Structure 5: stage_strat_revision

**Original (`stage-strat-revision.tex`):**
- `\documentclass[11pt, letterpaper]{article}`
- Packages (11, but one line has 3 comma-separated): inputenc[utf8], amsmath, amssymb, amsfonts, graphicx, geometry, booktabs, longtable, listings, xcolor, hyperref, caption, float (13 actual packages, 11 `\usepackage` calls)
- Commands (1): `\newcommand{\authcomment}[1]{\textcolor{red}{\textbf{[#1]}}}`
- Config blocks (4): `\geometry{letterpaper, total={6.5in, 9in}, left=1in, top=1in}`, `\hypersetup{...}`, `\lstdefinestyle{pythonstyle}{...}`, `\lstset{style=pythonstyle}`
- Colors (4): `\definecolor{codegreen}`, `\definecolor{codegray}`, `\definecolor{codepurple}`, `\definecolor{backcolour}`

**Modular (main.tex `\documentclass[11pt, letterpaper]{article}` + preamble.tex):**
- preamble.tex has the same comma-separated `\usepackage{amsmath, amssymb, amsfonts}`, all other packages, command, config blocks, colors
- main.tex has `\documentclass[11pt, letterpaper]{article}` + `\input{preamble}`

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual visual comparison of preambles | Automated extraction and set comparison | This phase | Consistent, repeatable, catches option-level differences |
| Treating preamble.tex as the entire modular preamble | Assembling from main.tex + resolved preamble.tex | This phase | Handles Data-quality-assessment correctly |
| String equality comparison | Normalized set comparison with category-specific parsing | Standard practice | Order-independent, whitespace-tolerant, semantically correct |

**Deprecated/outdated:**
- Byte-level comparison of preamble files: Fails due to whitespace, ordering, and split-file differences
- Manual counting of `\usepackage` lines: Error-prone, doesn't catch option mismatches

## Open Questions

1. **Should `\documentclass` options be compared?**
   - What we know: Different structures use different options (`[11pt, a4paper]` vs `[11pt, letterpaper]` vs no options). The original and modular versions of each structure should have identical `\documentclass` lines.
   - What's unclear: PREAMB-01/02/03 explicitly target `\usepackage`, `\newcommand`/`\renewcommand`/`\newenvironment`, and package options. `\documentclass` is not mentioned.
   - Recommendation: Include `\documentclass` comparison as a bonus check (informational, not pass/fail) since it's trivially easy and useful. Flag it separately from the PREAMB requirements.

2. **Should `\title`/`\author`/`\date` be compared?**
   - What we know: These appear in the preamble (before `\begin{document}`) in all structures. In modular versions, they may be in main.tex or preamble.tex.
   - What's unclear: These are document metadata, not package/macro declarations.
   - Recommendation: Exclude from comparison. They are not part of PREAMB-01/02/03 requirements. Including them would complicate the comparison without adding value.

3. **How to handle the trailing whitespace in `\hypersetup` for data_quality_assess?**
   - What we know: The original has `filecolor=magenta,      ` (trailing spaces) while the modular version may differ.
   - What's unclear: Whether this was normalized during modularization.
   - Recommendation: Normalize trailing whitespace within config blocks before comparison. This follows the same principle as Phase 5's whitespace normalization (D-03).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None (standalone scripts) |
| Config file | None -- scripts are self-contained |
| Quick run command | `python pinn_instruction/original_latex/verification/verify_preamble.py --structure data-quality -v` |
| Full suite command | `python pinn_instruction/original_latex/verification/verify_preamble.py -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PREAMB-01 | All `\usepackage` from original in modular preamble | functional | `python verify_preamble.py -v` | Wave 0 (to create) |
| PREAMB-02 | All `\newcommand`/`\renewcommand`/`\newenvironment` preserved | functional | `python verify_preamble.py -v` | Wave 0 (to create) |
| PREAMB-03 | Package options match exactly | functional | `python verify_preamble.py -v` | Wave 0 (to create) |

### Sampling Rate
- **Per task commit:** Run `python verify_preamble.py --structure <name> -v` after script creation/modification
- **Per wave merge:** Run full verification for all structures
- **Phase gate:** All 5 structures pass all 3 PREAMB checks before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `pinn_instruction/original_latex/verification/verify_preamble.py` -- main verification script
- [ ] Framework install: None needed -- uses only Python built-ins

## Sources

### Primary (HIGH confidence)
- Direct file analysis of all 5 original monolithic .tex files and all 5+ modular preamble files -- every construct cataloged by reading actual files
- Phase 5 research (05-RESEARCH.md) and implementation (verify_content.py) -- established patterns for structure definitions, file resolution, and report generation
- Phase 5 CONTEXT.md -- locked decision D-10 specifies `verify_preamble.py` as the Phase 6 script name

### Secondary (MEDIUM confidence)
- LaTeX `\usepackage` syntax -- standard LaTeX behavior for comma-separated packages and optional arguments
- LaTeX `\newcommand`/`\renewcommand` syntax -- both `\renewcommand{\cmd}` and `\renewcommand\cmd` forms are valid

### Tertiary (LOW confidence)
- None -- all findings verified from actual project files

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- Python built-ins only, identical to Phase 5
- Architecture: HIGH -- All 5 preamble structures fully analyzed from actual files, every construct inventoried
- Pitfalls: HIGH -- Identified from concrete file structure differences (inline preamble, self-contained preamble_CTL, comma-separated packages, renewcommand without braces)

**Research date:** 2026-03-21
**Valid until:** 30 days (stable Python libraries, LaTeX files unlikely to change)
