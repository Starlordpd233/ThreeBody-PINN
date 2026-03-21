#!/usr/bin/env python3
"""
verify_content.py

Phase 5: Content Completeness Verification
Verifies that every line of content from original monolithic .tex files
is present in the modular sections, with no extraneous content introduced.

Usage:
    python verify_content.py                    # Verify all 5 structures
    python verify_content.py --structure pinn   # Verify specific structure
    python verify_content.py --output report.md # Custom output path
    python verify_content.py --verbose          # Show progress
"""

import re
import argparse
from pathlib import Path
from difflib import unified_diff
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
from datetime import datetime


@dataclass
class Structure:
    """Definition of a LaTeX structure to verify."""
    name: str
    original: Path
    modular: Path
    sections_dir: str = "sections"
    inactive_files: Optional[List[str]] = None


# Define the 5 structures
STRUCTURES = [
    Structure(
        name="Data-quality-assessment",
        original=Path("pinn_instruction/original_latex/Data-quality-assessment/old/data_quality_assess.tex"),
        modular=Path("pinn_instruction/original_latex/Data-quality-assessment/data_quality_assess/main-data-quality-assess.tex"),
    ),
    Structure(
        name="ctl-instruction",
        original=Path("pinn_instruction/original_latex/ctl-instruction/old/CTL-instruction-final.tex"),
        modular=Path("pinn_instruction/original_latex/ctl-instruction/ctl-instruction/main_CTL.tex"),
        # Uses \include{} instead of \input{}
    ),
    Structure(
        name="pinn-architecture",
        original=Path("pinn_instruction/original_latex/pinn-architecture/old/PINN_architecture_plan.tex"),
        modular=Path("pinn_instruction/original_latex/pinn-architecture/pinn-architecture/main_pinn.tex"),
        inactive_files=["input_vector_inactive", "advanced_training_inactive", "consolidated_blueprint_inactive"],
    ),
    Structure(
        name="review_of_framework",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/review_of_ctl-pinn_framework.tex"),
        modular=Path("pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex"),
    ),
    Structure(
        name="stage_strat_revision",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/stage-strat-revision.tex"),
        modular=Path("pinn_instruction/original_latex/review-of-framework/stage_strat_revision/stage_strat_revision.tex"),
    ),
]


def normalize_line_endings(content: str) -> str:
    """Normalize to Unix line endings.

    Args:
        content: Text content with potentially mixed line endings

    Returns:
        Content with all line endings normalized to LF
    """
    return content.replace('\r\n', '\n').replace('\r', '\n')


def resolve_includes(content: str, base_dir: Path, depth: int = 0) -> str:
    """Recursively resolve \\input{} and \\include{} directives.

    Per D-01: Full recursive reassembly - resolve all \\input{}/\\include{}
    to produce flat file.

    Args:
        content: LaTeX content with include directives
        base_dir: Directory containing the main.tex file
        depth: Recursion depth (prevents infinite loops, max 10)

    Returns:
        Flat content with all includes resolved
    """
    if depth > 10:  # Safety limit per research pitfall
        return content

    # Match \input{file} or \include{file}
    # Pattern captures: leading whitespace, full command, path, trailing whitespace
    pattern = re.compile(r'^(\s*)(\\(?:input|include)\{([^}]+)\})(\s*)$', re.MULTILINE)

    def replace_include(match: re.Match) -> str:
        full_match = match.group(2)
        include_path = match.group(3)
        # Add .tex extension if not present
        if not include_path.endswith('.tex'):
            include_path += '.tex'

        file_path = base_dir / include_path
        if not file_path.exists():
            # Return original if file not found (preserve for error reporting)
            return full_match

        included_content = file_path.read_text(encoding='utf-8')
        included_content = normalize_line_endings(included_content)
        # Recursively resolve includes in the included file
        # Note: per research pitfall #1, we do NOT add \clearpage for \include{}
        return resolve_includes(included_content, file_path.parent, depth + 1)

    return pattern.sub(replace_include, content)


def normalize_whitespace(content: str) -> str:
    """Normalize whitespace for content comparison.

    Per D-03:
    - Strip trailing whitespace from each line
    - Collapse multiple blank lines to single blank line
    - Preserve indentation (leading whitespace)

    Args:
        content: Text content to normalize

    Returns:
        Normalized content
    """
    lines = content.split('\n')

    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in lines]

    # Collapse multiple blank lines to single blank line
    result = []
    prev_blank = False
    for line in lines:
        is_blank = line == ''
        if is_blank and prev_blank:
            continue  # Skip consecutive blank lines
        result.append(line)
        prev_blank = is_blank

    return '\n'.join(result)


def strip_scaffolding(content: str) -> str:
    """Remove LaTeX scaffolding lines that shouldn't be compared.

    Per D-02 and D-04: Remove lines matching scaffolding patterns.
    Also skip pure comment lines starting with % (except commented includes).

    Args:
        content: LaTeX content with scaffolding lines

    Returns:
        Content with scaffolding removed
    """
    lines = content.split('\n')
    result = []

    # Patterns for scaffolding lines to exclude
    scaffolding_patterns = [
        r'^\\documentclass\b',           # \documentclass{article}
        r'^\\input\{preamble',           # \input{preamble}, \input{preamble_CTL}
        r'^\\begin\{document\}',
        r'^\\end\{document\}',
        r'^\\maketitle\s*$',
        r'^\\input\{sections/',          # Section include directives
        r'^\\include\{sections/',        # Section include directives
        r'^%\s*\\input\{sections/',      # Commented-out section includes (inactive sections)
        r'^\\tableofcontents\s*$',       # May differ in placement
        r'^\\newpage\s*$',               # May differ in placement
        r'^\\thispagestyle\{[^}]*\}\s*$',  # Page style directives
        r'^\\vspace\{[^}]*\}\s*$',       # Vertical spacing
        r'^\\hrule\s*$',                 # Horizontal rules
    ]
    combined_pattern = re.compile('|'.join(scaffolding_patterns))

    for line in lines:
        stripped = line.strip()
        # Skip if matches scaffolding pattern
        if combined_pattern.match(stripped):
            continue
        # Skip pure comment lines (but not commented content like %\input{...})
        # Commented includes are already handled by the pattern above
        if stripped.startswith('%'):
            continue
        result.append(line)

    return '\n'.join(result)


def verify_structure(structure: Structure, base_path: Path) -> Tuple[bool, str, Dict]:
    """Verify a single structure.

    Process flow:
    1. Read original file, normalize line endings
    2. Resolve includes in original (some originals have \\input{} for preamble)
    3. Normalize whitespace
    4. Strip scaffolding
    5. Repeat steps 1-4 for modular file
    6. Generate unified diff with n=3 context
    7. Return (passed, diff_output, stats)

    Args:
        structure: Structure definition with paths
        base_path: Project root directory

    Returns:
        Tuple of (passed: bool, diff_output: str, stats: dict)
    """
    original_path = base_path / structure.original
    modular_path = base_path / structure.modular

    # Read and preprocess original
    original_content = original_path.read_text(encoding='utf-8')
    original_content = normalize_line_endings(original_content)
    original_content = resolve_includes(original_content, original_path.parent)
    original_content = normalize_whitespace(original_content)
    original_content = strip_scaffolding(original_content)

    # Read and preprocess modular
    modular_content = modular_path.read_text(encoding='utf-8')
    modular_content = normalize_line_endings(modular_content)
    modular_content = resolve_includes(modular_content, modular_path.parent)
    modular_content = normalize_whitespace(modular_content)
    modular_content = strip_scaffolding(modular_content)

    # Generate diff
    original_lines = original_content.split('\n')
    modular_lines = modular_content.split('\n')

    diff_lines = list(unified_diff(
        original_lines,
        modular_lines,
        fromfile=f'{structure.name}/original',
        tofile=f'{structure.name}/modular',
        n=3,  # 3 lines of context per D-05
        lineterm=''
    ))

    stats = {
        'original_lines': len(original_lines),
        'modular_lines': len(modular_lines),
        'diff_lines': len(diff_lines),
    }

    if diff_lines:
        return False, '\n'.join(diff_lines), stats
    else:
        return True, "No differences found.", stats


def main() -> int:
    """Main entry point for content verification.

    Returns:
        0 if all structures pass, 1 if any fail
    """
    parser = argparse.ArgumentParser(
        description='Verify LaTeX content completeness between monolithic and modular files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python verify_content.py                    # Verify all 5 structures
    python verify_content.py --structure pinn   # Verify only pinn-architecture
    python verify_content.py -v -o report.md    # Verbose with custom output
        """
    )
    parser.add_argument(
        '--structure', '-s',
        help='Verify specific structure (partial name match, e.g., "pinn" for pinn-architecture)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output report path (default: pinn_instruction/original_latex/verification/content_verification_report.md)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show progress information'
    )
    args = parser.parse_args()

    # Determine base path (project root)
    base_path = Path(__file__).resolve().parent.parent.parent.parent

    # Default output path per D-06
    output_path = args.output or base_path / 'pinn_instruction/original_latex/verification/content_verification_report.md'

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
        passed, diff, stats = verify_structure(structure, base_path)
        results.append((structure, passed, diff, stats))

    # Generate report
    report_lines = []
    report_lines.append("# Content Completeness Verification Report\n")
    report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"**Structures verified:** {len(results)}\n\n")

    # Summary table per D-07
    report_lines.append("## Summary\n")
    report_lines.append("| Structure | Status | Original Lines | Modular Lines |")
    report_lines.append("|-----------|--------|----------------|---------------|")
    for structure, passed, diff, stats in results:
        status = "PASS" if passed else "FAIL"
        report_lines.append(f"| {structure.name} | {status} | {stats['original_lines']} | {stats['modular_lines']} |")
    report_lines.append("")

    # Detailed results per D-07
    report_lines.append("\n## Detailed Results\n")
    for structure, passed, diff, stats in results:
        report_lines.append(f"\n### {structure.name}\n")
        # Per D-05: Note inactive sections if any
        if structure.inactive_files:
            report_lines.append(f"**Inactive sections excluded:** {', '.join(structure.inactive_files)}\n")
        # Per D-08: "No differences found." when content preserved
        report_lines.append(f"```\n{diff}\n```\n")

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(report_lines), encoding='utf-8')

    if args.verbose:
        print(f"\nReport written to: {output_path}")
        # Print summary to console
        for structure, passed, diff, stats in results:
            status = "PASS" if passed else "FAIL"
            print(f"  {structure.name}: {status} ({stats['original_lines']} original, {stats['modular_lines']} modular)")

    # Exit code: 0 if all pass, 1 if any fail
    all_passed = all(p for _, p, _, _ in results)
    return 0 if all_passed else 1


if __name__ == '__main__':
    exit(main())