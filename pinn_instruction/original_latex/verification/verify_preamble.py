#!/usr/bin/env python3
"""
verify_preamble.py

Phase 6: Preamble Parity Verification
Verifies that every package, command, environment, operator, and configuration
block from original monolithic .tex preambles is present in the modular
preambles for all 5 structures.

Covers:
  - PREAMB-01: \\usepackage declarations with options
  - PREAMB-02: \\newcommand, \\renewcommand, \\newenvironment, \\DeclareMathOperator
  - PREAMB-03: Configuration blocks (\\hypersetup, \\geometry, \\lstset,
               \\lstdefinestyle, \\definecolor, \\setcitestyle, \\usetikzlibrary)

Usage:
    python verify_preamble.py                    # Verify all 5 structures
    python verify_preamble.py --structure pinn   # Verify specific structure
    python verify_preamble.py --output report.md # Custom output path
    python verify_preamble.py --verbose          # Show progress
"""

import re
import argparse
from pathlib import Path
from difflib import unified_diff
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict
from datetime import datetime


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class PreambleStructure:
    """Definition of a LaTeX structure for preamble verification."""
    name: str
    original: Path       # Path to original monolithic .tex
    modular_main: Path   # Path to modular main.tex


@dataclass
class PackageDecl:
    """A single \\usepackage declaration."""
    name: str           # e.g., "amsmath"
    options: str = ""   # e.g., "utf8" or "" (normalized: stripped whitespace)


@dataclass
class CommandDef:
    """A command/environment/operator definition."""
    kind: str        # "newcommand", "renewcommand", "newenvironment", "DeclareMathOperator"
    name: str        # e.g., "\\vect", "authcommentenv", "\\median"
    full_text: str   # Complete definition text for comparison (whitespace-normalized)


@dataclass
class ConfigBlock:
    """A configuration block declaration."""
    command: str     # e.g., "hypersetup", "lstset", "geometry", etc.
    name: str = ""   # For named blocks like \\lstdefinestyle{mystyle} or \\definecolor{codegreen}
    content: str = "" # Full block content (whitespace-normalized)


# ---------------------------------------------------------------------------
# Structure definitions (all 5)
# ---------------------------------------------------------------------------

STRUCTURES = [
    PreambleStructure(
        name="Data-quality-assessment",
        original=Path("pinn_instruction/original_latex/Data-quality-assessment/old/data_quality_assess.tex"),
        modular_main=Path("pinn_instruction/original_latex/Data-quality-assessment/data_quality_assess/main-data-quality-assess.tex"),
    ),
    PreambleStructure(
        name="ctl-instruction",
        original=Path("pinn_instruction/original_latex/ctl-instruction/old/CTL-instruction-final.tex"),
        modular_main=Path("pinn_instruction/original_latex/ctl-instruction/ctl-instruction/main_CTL.tex"),
    ),
    PreambleStructure(
        name="pinn-architecture",
        original=Path("pinn_instruction/original_latex/pinn-architecture/old/PINN_architecture_plan.tex"),
        modular_main=Path("pinn_instruction/original_latex/pinn-architecture/pinn-architecture/main_pinn.tex"),
    ),
    PreambleStructure(
        name="review_of_framework",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/review_of_ctl-pinn_framework.tex"),
        modular_main=Path("pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex"),
    ),
    PreambleStructure(
        name="stage_strat_revision",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/stage-strat-revision.tex"),
        modular_main=Path("pinn_instruction/original_latex/review-of-framework/stage_strat_revision/stage_strat_revision.tex"),
    ),
]


# ---------------------------------------------------------------------------
# Preamble extraction and assembly
# ---------------------------------------------------------------------------

def extract_preamble(content: str) -> str:
    """Extract everything between \\documentclass (inclusive) and \\begin{document} (exclusive).

    Args:
        content: Full LaTeX file content.

    Returns:
        Preamble text from \\documentclass line up to (but not including) \\begin{document}.
        Returns '' if either marker not found.
    """
    lines = content.split('\n')
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None and re.match(r'^\s*\\documentclass', line):
            start = i
        if re.match(r'^\s*\\begin\{document\}', line):
            end = i
            break
    if start is None or end is None:
        return ''
    return '\n'.join(lines[start:end])


def resolve_preamble_inputs(content: str, base_dir: Path) -> str:
    """Resolve \\input{...} directives within content.

    Handles:
    - \\input{preamble_CTL} in ctl-instruction
    - \\input{preamble} in pinn-architecture, review_of_framework, stage_strat_revision
    - Data-quality-assessment has NO \\input{preamble} (all inline) -- no resolution needed

    Args:
        content: LaTeX content potentially containing \\input{} directives.
        base_dir: Directory containing the main.tex file.

    Returns:
        Content with \\input{} directives replaced by file contents.
    """
    pattern = re.compile(r'^(\s*)\\input\{([^}]+)\}(.*)$', re.MULTILINE)

    def replace_input(match: re.Match) -> str:
        leading = match.group(1)
        input_path = match.group(2)
        trailing = match.group(3)
        # Add .tex extension if missing
        if not input_path.endswith('.tex'):
            input_path += '.tex'
        file_path = base_dir / input_path
        if not file_path.exists():
            return match.group(0)  # Preserve original if file not found
        included = file_path.read_text(encoding='utf-8')
        return included

    return pattern.sub(replace_input, content)


def assemble_modular_preamble(main_path: Path) -> str:
    """Read main.tex, resolve \\input directives, then extract preamble.

    Args:
        main_path: Path to the modular main.tex file.

    Returns:
        Extracted preamble text after input resolution.
    """
    content = main_path.read_text(encoding='utf-8')
    resolved = resolve_preamble_inputs(content, main_path.parent)
    return extract_preamble(resolved)


# ---------------------------------------------------------------------------
# Parsing: packages
# ---------------------------------------------------------------------------

def parse_usepackage(preamble: str) -> List[PackageDecl]:
    """Parse all \\usepackage declarations from preamble text.

    Handles comma-separated package names: \\usepackage{amsmath, amssymb, amsfonts}
    becomes 3 separate PackageDecl entries sharing the same options.

    Args:
        preamble: Preamble text to parse.

    Returns:
        List of PackageDecl objects.
    """
    results = []
    # Strip comment lines before parsing
    lines = preamble.split('\n')
    cleaned = '\n'.join(line for line in lines if not line.strip().startswith('%'))

    pattern = re.compile(r'\\usepackage(?:\[([^\]]*)\])?\{([^}]+)\}')
    for match in pattern.finditer(cleaned):
        options = (match.group(1) or '').strip()
        pkg_str = match.group(2)
        # Split on commas for multi-package declarations
        packages = [p.strip() for p in pkg_str.split(',') if p.strip()]
        for pkg in packages:
            results.append(PackageDecl(name=pkg, options=options))
    return results


# ---------------------------------------------------------------------------
# Parsing: brace tracking helper
# ---------------------------------------------------------------------------

def extract_braced_block(content: str, start_pos: int) -> Tuple[str, int]:
    """Extract a brace-delimited block starting from start_pos.

    Starting from start_pos, finds the next '{', tracks brace depth,
    and returns the block content (including braces) and the position
    after the closing brace.

    Args:
        content: Full text to search.
        start_pos: Position to start scanning from.

    Returns:
        Tuple of (block content including braces, position after closing brace).
        Returns ('', start_pos) if no opening brace found.
    """
    # Find the opening brace
    idx = content.find('{', start_pos)
    if idx == -1:
        return ('', start_pos)

    depth = 0
    block_start = idx
    i = idx
    while i < len(content):
        ch = content[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return (content[block_start:i + 1], i + 1)
        i += 1
    # Unbalanced braces -- return what we have
    return (content[block_start:], len(content))


# ---------------------------------------------------------------------------
# Parsing: command definitions
# ---------------------------------------------------------------------------

def parse_command_defs(preamble: str) -> List[CommandDef]:
    """Parse \\newcommand, \\renewcommand, \\newenvironment, \\DeclareMathOperator.

    Handles both:
    - \\renewcommand{\\theadfont}{\\bfseries}  (standard form with braces)
    - \\renewcommand\\theadfont{\\bfseries}     (no-braces form)

    Args:
        preamble: Preamble text to parse.

    Returns:
        List of CommandDef objects.
    """
    results = []
    # Strip comment lines
    lines = preamble.split('\n')
    cleaned = '\n'.join(line for line in lines if not line.strip().startswith('%'))

    # --- newcommand / renewcommand ---
    # Match both forms: \renewcommand{\cmd} and \renewcommand\cmd
    cmd_pattern = re.compile(
        r'(\\(?:new|renew)command)\s*(\{\\[^}]+\}|\\[a-zA-Z]+)'
    )
    for match in cmd_pattern.finditer(cleaned):
        cmd_type = match.group(1)  # \newcommand or \renewcommand
        cmd_name_raw = match.group(2)  # {\vect} or \theadfont
        # Normalize name: strip outer braces if present
        if cmd_name_raw.startswith('{') and cmd_name_raw.endswith('}'):
            cmd_name = cmd_name_raw[1:-1]  # e.g., \vect
        else:
            cmd_name = cmd_name_raw  # e.g., \theadfont

        kind = "newcommand" if "new" in cmd_type and "renew" not in cmd_type else "renewcommand"

        # Extract the full definition: everything from the match start through
        # all braced blocks (optional [nargs] + {body})
        full_start = match.start()
        pos = match.end()

        # Skip optional whitespace
        while pos < len(cleaned) and cleaned[pos] in ' \t':
            pos += 1

        # Check for optional argument count [N]
        if pos < len(cleaned) and cleaned[pos] == '[':
            bracket_end = cleaned.find(']', pos)
            if bracket_end != -1:
                pos = bracket_end + 1

        # Skip whitespace before body
        while pos < len(cleaned) and cleaned[pos] in ' \t':
            pos += 1

        # Extract body block(s)
        if pos < len(cleaned) and cleaned[pos] == '{':
            _, pos = extract_braced_block(cleaned, pos)

        full_text = cleaned[full_start:pos].strip()
        # Normalize whitespace in full_text
        full_text = _normalize_definition(full_text)
        results.append(CommandDef(kind=kind, name=cmd_name, full_text=full_text))

    # --- newenvironment ---
    env_pattern = re.compile(r'\\newenvironment\{([^}]+)\}')
    for match in env_pattern.finditer(cleaned):
        env_name = match.group(1)
        full_start = match.start()
        pos = match.end()

        # Skip whitespace
        while pos < len(cleaned) and cleaned[pos] in ' \t\n':
            pos += 1

        # Extract begin_def block
        if pos < len(cleaned) and cleaned[pos] == '{':
            _, pos = extract_braced_block(cleaned, pos)

        # Skip whitespace between blocks
        while pos < len(cleaned) and cleaned[pos] in ' \t\n':
            pos += 1

        # Extract end_def block
        if pos < len(cleaned) and cleaned[pos] == '{':
            _, pos = extract_braced_block(cleaned, pos)

        full_text = cleaned[full_start:pos].strip()
        full_text = _normalize_definition(full_text)
        results.append(CommandDef(kind="newenvironment", name=env_name, full_text=full_text))

    # --- DeclareMathOperator ---
    op_pattern = re.compile(r'\\DeclareMathOperator\{([^}]+)\}\{([^}]+)\}')
    for match in op_pattern.finditer(cleaned):
        op_name = match.group(1)  # e.g., \median
        full_text = match.group(0).strip()
        full_text = _normalize_definition(full_text)
        results.append(CommandDef(kind="DeclareMathOperator", name=op_name, full_text=full_text))

    return results


def _normalize_definition(text: str) -> str:
    """Normalize whitespace in a definition string for comparison.

    Strips trailing whitespace per line, collapses blank lines.

    Args:
        text: Definition text.

    Returns:
        Normalized definition text.
    """
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    # Collapse multiple blank lines to single
    result = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return '\n'.join(result)


# ---------------------------------------------------------------------------
# Parsing: configuration blocks
# ---------------------------------------------------------------------------

def parse_config_blocks(preamble: str) -> List[ConfigBlock]:
    """Parse configuration blocks from preamble text.

    Detects: \\hypersetup, \\geometry, \\lstset, \\lstdefinestyle, \\definecolor,
    \\setcitestyle, \\usetikzlibrary.

    Args:
        preamble: Preamble text to parse.

    Returns:
        List of ConfigBlock objects.
    """
    results = []
    # Strip comment lines
    lines = preamble.split('\n')
    cleaned = '\n'.join(line for line in lines if not line.strip().startswith('%'))

    # --- definecolor: \definecolor{name}{model}{spec} ---
    color_pattern = re.compile(
        r'\\definecolor\s*\{([^}]+)\}\s*\{([^}]+)\}\s*\{([^}]+)\}'
    )
    for match in color_pattern.finditer(cleaned):
        name = match.group(1).strip()
        full_text = match.group(0).strip()
        full_text = _normalize_config(full_text)
        results.append(ConfigBlock(command="definecolor", name=name, content=full_text))

    # --- Simple braced blocks (no name argument) ---
    simple_commands = ['hypersetup', 'geometry', 'lstset', 'setcitestyle']
    for cmd in simple_commands:
        pattern = re.compile(r'\\' + cmd + r'\s*\{')
        for match in pattern.finditer(cleaned):
            block_text, end_pos = extract_braced_block(cleaned, match.start() + len(cmd) + 1)
            full_text = '\\' + cmd + block_text
            full_text = _normalize_config(full_text)
            results.append(ConfigBlock(command=cmd, name="", content=full_text))

    # --- lstdefinestyle: \lstdefinestyle{name}{...} ---
    style_pattern = re.compile(r'\\lstdefinestyle\s*\{([^}]+)\}\s*\{')
    for match in style_pattern.finditer(cleaned):
        style_name = match.group(1).strip()
        # Find the second braced block (the style definition)
        after_name = match.end() - 1  # Position just before the opening {
        block_text, end_pos = extract_braced_block(cleaned, after_name)
        full_text = '\\lstdefinestyle{' + style_name + '}' + block_text
        full_text = _normalize_config(full_text)
        results.append(ConfigBlock(command="lstdefinestyle", name=style_name, content=full_text))

    # --- usetikzlibrary: \usetikzlibrary{...} ---
    tikz_pattern = re.compile(r'\\usetikzlibrary\s*\{')
    for match in tikz_pattern.finditer(cleaned):
        block_text, end_pos = extract_braced_block(cleaned, match.start() + len('\\usetikzlibrary'))
        full_text = '\\usetikzlibrary' + block_text
        full_text = _normalize_config(full_text)
        results.append(ConfigBlock(command="usetikzlibrary", name="", content=full_text))

    return results


def _normalize_config(text: str) -> str:
    """Normalize whitespace in a configuration block for comparison.

    Strips trailing whitespace per line, collapses multiple spaces
    within values to single space, collapses blank lines.

    Args:
        text: Configuration block text.

    Returns:
        Normalized configuration text.
    """
    lines = text.split('\n')
    normalized = []
    for line in lines:
        line = line.rstrip()
        # Collapse multiple spaces to single (but preserve leading indent)
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        stripped = re.sub(r'  +', ' ', stripped)
        normalized.append(indent + stripped)
    # Collapse multiple blank lines to single
    result = []
    prev_blank = False
    for line in normalized:
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return '\n'.join(result)


# ---------------------------------------------------------------------------
# Parsing: documentclass
# ---------------------------------------------------------------------------

def parse_documentclass(preamble: str) -> str:
    """Extract the full \\documentclass line for informational comparison.

    Args:
        preamble: Preamble text.

    Returns:
        The full \\documentclass declaration string, or '' if not found.
    """
    match = re.search(r'\\documentclass(?:\[([^\]]*)\])?\{([^}]+)\}', preamble)
    if match:
        return match.group(0)
    return ''


# ---------------------------------------------------------------------------
# Comparison functions
# ---------------------------------------------------------------------------

def compare_packages(original: List[PackageDecl], modular: List[PackageDecl]) -> Dict:
    """Compare package declarations between original and modular preambles.

    Args:
        original: Packages from original preamble.
        modular: Packages from modular preamble.

    Returns:
        Dict with keys: matched, missing, extra, option_mismatches.
    """
    orig_by_name: Dict[str, PackageDecl] = {}
    for p in original:
        orig_by_name[p.name] = p
    mod_by_name: Dict[str, PackageDecl] = {}
    for p in modular:
        mod_by_name[p.name] = p

    matched = []
    missing = []
    extra = []
    option_mismatches = []

    for name, orig_pkg in orig_by_name.items():
        if name in mod_by_name:
            mod_pkg = mod_by_name[name]
            if orig_pkg.options == mod_pkg.options:
                matched.append(name)
            else:
                option_mismatches.append({
                    'name': name,
                    'original_options': orig_pkg.options,
                    'modular_options': mod_pkg.options,
                })
        else:
            missing.append(name)

    for name in mod_by_name:
        if name not in orig_by_name:
            extra.append(name)

    return {
        'matched': sorted(matched),
        'missing': sorted(missing),
        'extra': sorted(extra),
        'option_mismatches': option_mismatches,
    }


def compare_commands(original: List[CommandDef], modular: List[CommandDef]) -> Dict:
    """Compare command/environment/operator definitions.

    Args:
        original: Definitions from original preamble.
        modular: Definitions from modular preamble.

    Returns:
        Dict with keys: matched, missing, extra, body_mismatches.
    """
    def key(c: CommandDef) -> Tuple[str, str]:
        return (c.kind, c.name)

    orig_by_key: Dict[Tuple[str, str], CommandDef] = {}
    for c in original:
        orig_by_key[key(c)] = c
    mod_by_key: Dict[Tuple[str, str], CommandDef] = {}
    for c in modular:
        mod_by_key[key(c)] = c

    matched = []
    missing = []
    extra = []
    body_mismatches = []

    for k, orig_cmd in orig_by_key.items():
        if k in mod_by_key:
            mod_cmd = mod_by_key[k]
            if orig_cmd.full_text == mod_cmd.full_text:
                matched.append(f"{k[0]}:{k[1]}")
            else:
                body_mismatches.append({
                    'kind': k[0],
                    'name': k[1],
                    'original': orig_cmd.full_text,
                    'modular': mod_cmd.full_text,
                })
        else:
            missing.append(f"{k[0]}:{k[1]}")

    for k in mod_by_key:
        if k not in orig_by_key:
            extra.append(f"{k[0]}:{k[1]}")

    return {
        'matched': sorted(matched),
        'missing': sorted(missing),
        'extra': sorted(extra),
        'body_mismatches': body_mismatches,
    }


def compare_config_blocks(original: List[ConfigBlock], modular: List[ConfigBlock]) -> Dict:
    """Compare configuration blocks between original and modular preambles.

    Args:
        original: Config blocks from original preamble.
        modular: Config blocks from modular preamble.

    Returns:
        Dict with keys: matched, missing, extra, content_mismatches.
    """
    def key(c: ConfigBlock) -> Tuple[str, str]:
        return (c.command, c.name)

    orig_by_key: Dict[Tuple[str, str], ConfigBlock] = {}
    for c in original:
        orig_by_key[key(c)] = c
    mod_by_key: Dict[Tuple[str, str], ConfigBlock] = {}
    for c in modular:
        mod_by_key[key(c)] = c

    matched = []
    missing = []
    extra = []
    content_mismatches = []

    for k, orig_blk in orig_by_key.items():
        if k in mod_by_key:
            mod_blk = mod_by_key[k]
            if orig_blk.content == mod_blk.content:
                label = f"{k[0]}" + (f"({k[1]})" if k[1] else "")
                matched.append(label)
            else:
                diff = list(unified_diff(
                    orig_blk.content.split('\n'),
                    mod_blk.content.split('\n'),
                    fromfile=f'original/{k[0]}' + (f'({k[1]})' if k[1] else ''),
                    tofile=f'modular/{k[0]}' + (f'({k[1]})' if k[1] else ''),
                    lineterm='',
                ))
                label = f"{k[0]}" + (f"({k[1]})" if k[1] else "")
                content_mismatches.append({
                    'label': label,
                    'diff': '\n'.join(diff),
                })
        else:
            label = f"{k[0]}" + (f"({k[1]})" if k[1] else "")
            missing.append(label)

    for k in mod_by_key:
        if k not in orig_by_key:
            label = f"{k[0]}" + (f"({k[1]})" if k[1] else "")
            extra.append(label)

    return {
        'matched': sorted(matched),
        'missing': sorted(missing),
        'extra': sorted(extra),
        'content_mismatches': content_mismatches,
    }


# ---------------------------------------------------------------------------
# Structure verification
# ---------------------------------------------------------------------------

def verify_structure(structure: PreambleStructure, base_path: Path,
                     verbose: bool = False) -> Dict:
    """Orchestrate preamble parity verification for one structure.

    Args:
        structure: PreambleStructure definition.
        base_path: Project root directory.
        verbose: Print progress information.

    Returns:
        Dict with all comparison results and pass/fail status.
    """
    original_path = base_path / structure.original
    modular_main_path = base_path / structure.modular_main

    # 1. Extract original preamble
    original_content = original_path.read_text(encoding='utf-8')
    original_preamble = extract_preamble(original_content)

    # 2. Assemble modular preamble (read main.tex, resolve inputs, extract preamble)
    modular_preamble = assemble_modular_preamble(modular_main_path)

    if verbose:
        print(f"  Original preamble: {len(original_preamble.split(chr(10)))} lines")
        print(f"  Modular preamble:  {len(modular_preamble.split(chr(10)))} lines")

    # 3. Parse both preambles
    orig_packages = parse_usepackage(original_preamble)
    mod_packages = parse_usepackage(modular_preamble)

    orig_commands = parse_command_defs(original_preamble)
    mod_commands = parse_command_defs(modular_preamble)

    orig_configs = parse_config_blocks(original_preamble)
    mod_configs = parse_config_blocks(modular_preamble)

    orig_docclass = parse_documentclass(original_preamble)
    mod_docclass = parse_documentclass(modular_preamble)

    # 4. Compare
    pkg_result = compare_packages(orig_packages, mod_packages)
    cmd_result = compare_commands(orig_commands, mod_commands)
    cfg_result = compare_config_blocks(orig_configs, mod_configs)

    docclass_match = orig_docclass == mod_docclass

    # 5. Determine pass/fail
    passed = (
        len(pkg_result['missing']) == 0
        and len(pkg_result['extra']) == 0
        and len(pkg_result['option_mismatches']) == 0
        and len(cmd_result['missing']) == 0
        and len(cmd_result['extra']) == 0
        and len(cmd_result['body_mismatches']) == 0
        and len(cfg_result['missing']) == 0
        and len(cfg_result['extra']) == 0
        and len(cfg_result['content_mismatches']) == 0
        and docclass_match
    )

    return {
        'passed': passed,
        'docclass_original': orig_docclass,
        'docclass_modular': mod_docclass,
        'docclass_match': docclass_match,
        'packages': pkg_result,
        'commands': cmd_result,
        'configs': cfg_result,
        'counts': {
            'pkg_total': len(set(p.name for p in orig_packages)),
            'pkg_matched': len(pkg_result['matched']),
            'cmd_total': len(orig_commands),
            'cmd_matched': len(cmd_result['matched']),
            'cfg_total': len(orig_configs),
            'cfg_matched': len(cfg_result['matched']),
        },
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(results: List[Tuple[PreambleStructure, Dict]]) -> str:
    """Generate a Markdown preamble verification report.

    Args:
        results: List of (structure, result_dict) tuples.

    Returns:
        Complete Markdown report string.
    """
    lines = []
    lines.append("# Preamble Parity Verification Report\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Structures verified:** {len(results)}\n")

    # Summary table
    lines.append("## Summary\n")
    lines.append("| Structure | Packages | Commands | Config Blocks | Status |")
    lines.append("|-----------|----------|----------|---------------|--------|")
    for structure, result in results:
        c = result['counts']
        status = "PASS" if result['passed'] else "FAIL"
        lines.append(
            f"| {structure.name} "
            f"| {c['pkg_matched']}/{c['pkg_total']} "
            f"| {c['cmd_matched']}/{c['cmd_total']} "
            f"| {c['cfg_matched']}/{c['cfg_total']} "
            f"| {status} |"
        )
    lines.append("")

    # Detailed results
    lines.append("## Detailed Results\n")
    for structure, result in results:
        lines.append(f"### {structure.name}\n")

        # Documentclass
        if result['docclass_match']:
            lines.append(f"**Documentclass:** `{result['docclass_original']}` -- MATCH\n")
        else:
            lines.append(f"**Documentclass:** MISMATCH")
            lines.append(f"- Original: `{result['docclass_original']}`")
            lines.append(f"- Modular: `{result['docclass_modular']}`\n")

        # Packages (PREAMB-01)
        pkg = result['packages']
        lines.append("#### Packages (PREAMB-01)\n")
        lines.append(f"**Matched ({len(pkg['matched'])}):** {', '.join(pkg['matched']) or 'none'}")
        lines.append(f"**Missing ({len(pkg['missing'])}):** {', '.join(pkg['missing']) or 'none'}")
        lines.append(f"**Extra ({len(pkg['extra'])}):** {', '.join(pkg['extra']) or 'none'}")
        if pkg['option_mismatches']:
            lines.append(f"**Option mismatches ({len(pkg['option_mismatches'])}):**")
            for m in pkg['option_mismatches']:
                lines.append(f"- `{m['name']}`: original=[{m['original_options']}] vs modular=[{m['modular_options']}]")
        else:
            lines.append("**Option mismatches (0):** none")
        lines.append("")

        # Commands & Environments (PREAMB-02)
        cmd = result['commands']
        lines.append("#### Commands & Environments (PREAMB-02)\n")
        lines.append(f"**Matched ({len(cmd['matched'])}):** {', '.join(cmd['matched']) or 'none'}")
        lines.append(f"**Missing ({len(cmd['missing'])}):** {', '.join(cmd['missing']) or 'none'}")
        lines.append(f"**Extra ({len(cmd['extra'])}):** {', '.join(cmd['extra']) or 'none'}")
        if cmd['body_mismatches']:
            lines.append(f"**Body mismatches ({len(cmd['body_mismatches'])}):**")
            for m in cmd['body_mismatches']:
                lines.append(f"- `{m['kind']}:{m['name']}`:")
                lines.append(f"  - Original: `{m['original']}`")
                lines.append(f"  - Modular: `{m['modular']}`")
        else:
            lines.append("**Body mismatches (0):** none")
        lines.append("")

        # Configuration Blocks (PREAMB-03)
        cfg = result['configs']
        lines.append("#### Configuration Blocks (PREAMB-03)\n")
        lines.append(f"**Matched ({len(cfg['matched'])}):** {', '.join(cfg['matched']) or 'none'}")
        lines.append(f"**Missing ({len(cfg['missing'])}):** {', '.join(cfg['missing']) or 'none'}")
        lines.append(f"**Extra ({len(cfg['extra'])}):** {', '.join(cfg['extra']) or 'none'}")
        if cfg['content_mismatches']:
            lines.append(f"**Content mismatches ({len(cfg['content_mismatches'])}):**")
            for m in cfg['content_mismatches']:
                lines.append(f"- `{m['label']}`:")
                lines.append(f"```diff\n{m['diff']}\n```")
        else:
            lines.append("**Content mismatches (0):** none")
        lines.append("")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Main entry point for preamble parity verification.

    Returns:
        0 if all structures pass, 1 if any fail.
    """
    parser = argparse.ArgumentParser(
        description='Verify preamble parity between original monolithic and modular LaTeX files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python verify_preamble.py                    # Verify all 5 structures
    python verify_preamble.py --structure pinn   # Verify only pinn-architecture
    python verify_preamble.py -v -o report.md    # Verbose with custom output
        """
    )
    parser.add_argument(
        '--structure', '-s',
        help='Verify specific structure (partial name match, e.g., "pinn" for pinn-architecture)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output report path (default: pinn_instruction/original_latex/verification/preamble_verification_report.md)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show progress information'
    )
    args = parser.parse_args()

    # Determine base path (project root)
    base_path = Path(__file__).resolve().parent.parent.parent.parent

    # Default output path
    output_path = args.output or base_path / 'pinn_instruction/original_latex/verification/preamble_verification_report.md'

    # Filter structures if specified
    structures = STRUCTURES
    if args.structure:
        structures = [s for s in STRUCTURES if args.structure.lower() in s.name.lower()]
        if not structures:
            print(f"No structures found matching '{args.structure}'")
            return 1

    # Verify each structure
    results = []
    for structure in structures:
        if args.verbose:
            print(f"Verifying: {structure.name}...")
        result = verify_structure(structure, base_path, verbose=args.verbose)
        results.append((structure, result))
        if args.verbose:
            status = "PASS" if result['passed'] else "FAIL"
            c = result['counts']
            print(f"  -> {status} (packages: {c['pkg_matched']}/{c['pkg_total']}, "
                  f"commands: {c['cmd_matched']}/{c['cmd_total']}, "
                  f"configs: {c['cfg_matched']}/{c['cfg_total']})")

    # Generate and write report
    report = generate_report(results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')

    if args.verbose:
        print(f"\nReport written to: {output_path}")

    # Exit code: 0 if all pass, 1 if any fail
    all_passed = all(r['passed'] for _, r in results)
    return 0 if all_passed else 1


if __name__ == '__main__':
    exit(main())
