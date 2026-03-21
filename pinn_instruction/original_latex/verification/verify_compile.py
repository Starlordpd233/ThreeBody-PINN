#!/usr/bin/env python3
"""
verify_compile.py

Phase 8: Compilability Verification
Compiles all 5 modular LaTeX structures with latexmk, reports pass/fail based on
error count, and compares warnings against original monolithic files to flag any
new warnings introduced by modularization.

Usage:
    python verify_compile.py                    # Compile all 5 structures
    python verify_compile.py --structure pinn   # Compile specific structure
    python verify_compile.py --output report.md # Custom output path
    python verify_compile.py --verbose          # Show progress
    python verify_compile.py --keep-tmp         # Keep temp compilation files
"""

import re
import subprocess
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set, Optional
from datetime import datetime
from shutil import rmtree


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CompileStructure:
    """Definition of a LaTeX structure for compilation verification."""
    name: str
    original: Path       # Path to original monolithic .tex in old/
    modular: Path        # Path to modular main.tex


# ---------------------------------------------------------------------------
# Structure definitions (all 5)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Warning patterns (per D-14)
# ---------------------------------------------------------------------------

WARNING_PATTERNS = [
    r'LaTeX Warning:.*',
    r'Package Warning:.*',
    r'Class Warning:.*',
    r'Overfull \\hbox.*',
    r'Underfull \\hbox.*',
]


# ---------------------------------------------------------------------------
# Compilation function (per D-04 through D-09)
# ---------------------------------------------------------------------------

def compile_structure(main_tex: Path, output_dir: Path, timeout: int = 120) -> Tuple[int, Path]:
    r"""Compile LaTeX file with latexmk.

    Per D-06: Run latexmk with cwd set to the structure's directory so relative
    \input{preamble} and \input{sections/...} paths resolve correctly.

    Per D-07: Use -output-directory pointing to a temp directory.

    Per D-08: Set -interaction=nonstopmode so compilation continues through errors.

    Per D-09: 120 second timeout per compilation.

    Args:
        main_tex: Path to main .tex file
        output_dir: Directory for output files (will be created)
        timeout: Compilation timeout in seconds

    Returns:
        Tuple of (return_code, log_file_path)
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "latexmk",
        "-pdf",
        "-pdflatex=pdflatex -interaction=nonstopmode",
        f"-output-directory={output_dir}",
        main_tex.name
    ]

    result = subprocess.run(
        cmd,
        cwd=main_tex.parent,
        capture_output=True,
        text=True,
        timeout=timeout
    )

    log_file = output_dir / main_tex.with_suffix('.log').name
    return result.returncode, log_file


# ---------------------------------------------------------------------------
# Error extraction (per D-10, D-11)
# ---------------------------------------------------------------------------

def extract_errors(log_content: str) -> List[Dict]:
    """Extract fatal errors from LaTeX log (lines starting with !).

    Per D-10: PASS = 0 fatal errors (lines matching ^! in .log file).
    Per D-11: Report all errors with surrounding context.

    Args:
        log_content: Full content of the .log file.

    Returns:
        List of dicts with 'line_num', 'message', 'context' keys.
    """
    errors = []
    lines = log_content.split('\n')

    for i, line in enumerate(lines):
        if line.startswith('!'):
            context_start = max(0, i - 2)
            context_end = min(len(lines), i + 5)
            errors.append({
                'line_num': i + 1,
                'message': line[1:].strip(),  # Remove '!' prefix
                'context': '\n'.join(lines[context_start:context_end])
            })

    return errors


# ---------------------------------------------------------------------------
# Warning extraction and normalization (per D-14, D-15)
# ---------------------------------------------------------------------------

def extract_warnings(log_content: str) -> Set[str]:
    r"""Extract and normalize warnings from LaTeX log.

    Per D-14: A "warning" is any log line matching LaTeX Warning:, Package Warning:,
    Class Warning:, or Overfull \hbox / Underfull \hbox.

    Per D-15: Normalize warning text before comparison: strip line numbers and
    file paths (vary between runs).

    Args:
        log_content: Full content of the .log file.

    Returns:
        Set of normalized warning strings.
    """
    warnings = set()

    for pattern in WARNING_PATTERNS:
        for match in re.finditer(pattern, log_content):
            warning = match.group(0)
            # Normalize: strip line numbers and file paths per D-15
            # "Overfull \hbox (25pt wide) in paragraph at lines 47--47"
            # -> "Overfull \hbox (25pt wide) in paragraph"
            normalized = re.sub(r'\s+at lines \d+--\d+', '', warning)
            normalized = re.sub(r'\s+on input line \d+', '', normalized)
            warnings.add(normalized)

    return warnings


# ---------------------------------------------------------------------------
# Warning comparison (per D-16)
# ---------------------------------------------------------------------------

def compare_warnings(original_warnings: Set[str], modular_warnings: Set[str]) -> Dict:
    """Compare warning sets between original and modular.

    Per D-16: Report three categories:
    - (a) warnings in both = pre-existing (OK)
    - (b) warnings only in modular = new/introduced
    - (c) warnings only in original = resolved (bonus)

    Args:
        original_warnings: Warnings from original monolithic compilation.
        modular_warnings: Warnings from modular compilation.

    Returns:
        Dict with 'pre_existing', 'new', 'resolved' keys.
    """
    return {
        'pre_existing': sorted(original_warnings & modular_warnings),
        'new': sorted(modular_warnings - original_warnings),
        'resolved': sorted(original_warnings - modular_warnings),
    }


# ---------------------------------------------------------------------------
# Structure verification
# ---------------------------------------------------------------------------

def verify_structure(structure: CompileStructure, base_path: Path, tmp_dir: Path, verbose: bool = False) -> Dict:
    """Compile both original and modular, compare results.

    Args:
        structure: CompileStructure definition with paths.
        base_path: Project root directory.
        tmp_dir: Base temp directory for compilation outputs.
        verbose: Print progress information.

    Returns:
        Dict with pass/fail status, errors, and warning comparison.
    """
    # Resolve paths
    original_path = base_path / structure.original
    modular_path = base_path / structure.modular

    # Create output directories
    orig_output = tmp_dir / f"{structure.name}-original"
    mod_output = tmp_dir / structure.name

    results = {
        'name': structure.name,
        'original_path': str(original_path),
        'modular_path': str(modular_path),
    }

    # Compile original for baseline
    if verbose:
        print(f"  Compiling original: {structure.name}...")
    try:
        _, orig_log_path = compile_structure(original_path, orig_output)
        orig_log = orig_log_path.read_text(encoding='utf-8', errors='replace') if orig_log_path.exists() else ''
        orig_errors = extract_errors(orig_log)
        orig_warnings = extract_warnings(orig_log)
    except subprocess.TimeoutExpired:
        results['original_error'] = 'Compilation timeout'
        orig_errors = [{'line_num': 0, 'message': 'Compilation timeout', 'context': ''}]
        orig_warnings = set()
    except Exception as e:
        results['original_error'] = str(e)
        orig_errors = [{'line_num': 0, 'message': str(e), 'context': ''}]
        orig_warnings = set()

    # Compile modular
    if verbose:
        print(f"  Compiling modular: {structure.name}...")
    try:
        _, mod_log_path = compile_structure(modular_path, mod_output)
        mod_log = mod_log_path.read_text(encoding='utf-8', errors='replace') if mod_log_path.exists() else ''
        mod_errors = extract_errors(mod_log)
        mod_warnings = extract_warnings(mod_log)
    except subprocess.TimeoutExpired:
        results['modular_error'] = 'Compilation timeout'
        mod_errors = [{'line_num': 0, 'message': 'Compilation timeout', 'context': ''}]
        mod_warnings = set()
    except Exception as e:
        results['modular_error'] = str(e)
        mod_errors = [{'line_num': 0, 'message': str(e), 'context': ''}]
        mod_warnings = set()

    # Compare results
    warning_comparison = compare_warnings(orig_warnings, mod_warnings)

    results.update({
        'passed': len(mod_errors) == 0,
        'modular_errors': mod_errors,
        'modular_error_count': len(mod_errors),
        'original_warning_count': len(orig_warnings),
        'modular_warning_count': len(mod_warnings),
        'new_warning_count': len(warning_comparison['new']),
        'warning_comparison': warning_comparison,
    })

    return results


# ---------------------------------------------------------------------------
# Report generation (per D-17, D-18)
# ---------------------------------------------------------------------------

def generate_report(results: List[Dict]) -> str:
    """Generate Markdown compilation verification report.

    Per D-17: Markdown output to compile_verification_report.md.
    Per D-18: Report structure: summary table at top, followed by per-structure
    sections with full error list and new warning list.

    Args:
        results: List of verification result dicts.

    Returns:
        Complete Markdown report string.
    """
    lines = []
    lines.append("# Compilation Verification Report\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Structures verified:** {len(results)}\n")

    # Summary table per D-18
    lines.append("## Summary\n")
    lines.append("| Structure | Status | Errors | Warnings | New Warnings |")
    lines.append("|-----------|--------|--------|----------|--------------|")
    for r in results:
        status = "PASS" if r['passed'] else "FAIL"
        lines.append(
            f"| {r['name']} "
            f"| {status} "
            f"| {r['modular_error_count']} "
            f"| {r['modular_warning_count']} "
            f"| {r['new_warning_count']} |"
        )
    lines.append("")

    # Detailed results
    lines.append("## Detailed Results\n")
    for r in results:
        lines.append(f"### {r['name']}\n")

        # Status
        if r['passed']:
            lines.append("**Status:** PASS - Compiled with 0 errors\n")
        else:
            lines.append(f"**Status:** FAIL - {r['modular_error_count']} error(s)\n")

        # Errors
        if r['modular_errors']:
            lines.append("#### Errors\n")
            for err in r['modular_errors']:
                lines.append(f"- Line {err['line_num']}: {err['message']}")
                if err['context']:
                    lines.append(f"```\n{err['context']}\n```\n")

        # Warnings
        wc = r['warning_comparison']
        lines.append("#### Warnings\n")
        lines.append(f"- Pre-existing (in both): {len(wc['pre_existing'])}")
        lines.append(f"- New (only in modular): {len(wc['new'])}")
        lines.append(f"- Resolved (only in original): {len(wc['resolved'])}")

        if wc['new']:
            lines.append("\n**New warnings introduced by modularization:**")
            for w in wc['new'][:10]:  # Limit to first 10
                lines.append(f"- {w[:100]}{'...' if len(w) > 100 else ''}")
        lines.append("")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main entry point (per D-02, D-19, D-20)
# ---------------------------------------------------------------------------

def main() -> int:
    """Main entry point for compilability verification.

    Per D-02: Same CLI interface: --structure <name>, --output <path>, --verbose,
    run all structures by default.

    Per D-19: Exit code 0 if all 5 structures compile with 0 errors; exit code 1
    if any structure has errors.

    Per D-20: Temp directory cleaned up after each run (or kept with --keep-tmp).

    Returns:
        0 if all structures pass, 1 if any fail.
    """
    parser = argparse.ArgumentParser(
        description='Verify LaTeX compilability for modular structures.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python verify_compile.py                    # Verify all 5 structures
    python verify_compile.py --structure pinn   # Verify only pinn-architecture
    python verify_compile.py -v --keep-tmp      # Verbose, keep temp files
        """
    )
    parser.add_argument(
        '--structure', '-s',
        help='Verify specific structure (partial name match, e.g., "pinn" for pinn-architecture)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output report path (default: pinn_instruction/original_latex/verification/compile_verification_report.md)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show progress information'
    )
    parser.add_argument(
        '--keep-tmp',
        action='store_true',
        help='Keep temporary compilation files for debugging'
    )
    args = parser.parse_args()

    # Determine base path (project root)
    base_path = Path(__file__).resolve().parent.parent.parent.parent

    # Temp directory for compilation outputs
    tmp_dir = base_path / 'pinn_instruction/original_latex/verification/tmp'

    # Default output path per D-17
    output_path = args.output or base_path / 'pinn_instruction/original_latex/verification/compile_verification_report.md'

    # Filter structures if specified
    structures = STRUCTURES
    if args.structure:
        structures = [s for s in STRUCTURES if args.structure.lower() in s.name.lower()]
        if not structures:
            print(f"No structures found matching '{args.structure}'")
            return 1

    # Clean tmp directory per D-20
    if tmp_dir.exists():
        rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Verify each structure
    results = []
    for structure in structures:
        if args.verbose:
            print(f"Verifying: {structure.name}...")
        result = verify_structure(structure, base_path, tmp_dir, args.verbose)
        results.append(result)
        if args.verbose:
            status = "PASS" if result['passed'] else "FAIL"
            print(f"  -> {status} ({result['modular_error_count']} errors, {result['new_warning_count']} new warnings)")

    # Generate report
    report = generate_report(results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')

    if args.verbose:
        print(f"\nReport written to: {output_path}")

    # Cleanup per D-20
    if not args.keep_tmp and tmp_dir.exists():
        rmtree(tmp_dir)

    # Exit code per D-19
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    exit(main())