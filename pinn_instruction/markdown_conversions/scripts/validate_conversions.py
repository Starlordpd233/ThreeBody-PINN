#!/usr/bin/env python3
"""
Validation script for LaTeX to Markdown conversions.

Checks:
- Count of math environments (inline and display)
- Count of code blocks (lstlisting/verbatim to fenced code)
- Count of tables
- Count of algorithms/TikZ figures
- Count of comment blocks
"""

import re
from pathlib import Path
from typing import Dict, Tuple


def count_latex_elements(content: str) -> Dict[str, int]:
    """Count various elements in LaTeX content."""
    counts = {}

    # Count inline math ($ ... $)
    counts['inline_math'] = len(re.findall(r'\$[^$]+\$', content))

    # Count display math environments
    display_envs = ['equation', 'align', 'align\\*', 'cases', 'gather', 'multline']
    counts['display_math'] = sum(
        len(re.findall(rf'\\begin\{{{env}\}}', content))
        for env in display_envs
    )
    # Also count \[ ... \]
    counts['display_math'] += len(re.findall(r'\\\[', content))

    # Count code blocks
    counts['code_blocks'] = (
        len(re.findall(r'\\begin\{lstlisting\}', content)) +
        len(re.findall(r'\\begin\{verbatim\}', content))
    )

    # Count tables
    counts['tables'] = (
        len(re.findall(r'\\begin\{table\}', content)) +
        len(re.findall(r'\\begin\{longtable\}', content))
    )

    # Count algorithms
    counts['algorithms'] = len(re.findall(r'\\begin\{algorithm\}', content))

    # Count TikZ figures
    counts['tikz'] = len(re.findall(r'\\begin\{tikzpicture\}', content))

    # Count comment blocks
    counts['comment_blocks'] = len(re.findall(r'\\begin\{comment\}', content))
    counts['authcomments'] = len(re.findall(r'\\authcomment\{', content))
    counts['authcomment_env'] = len(re.findall(r'\\begin\{authcommentenv\}', content))

    return counts


def count_markdown_elements(content: str) -> Dict[str, int]:
    """Count various elements in Markdown content."""
    counts = {}

    # Count inline math ($ ... $)
    counts['inline_math'] = len(re.findall(r'\$[^$]+\$', content))

    # Count display math ($$ ... $$)
    counts['display_math'] = len(re.findall(r'\$\$', content)) // 2  # Divide by 2 for pairs

    # Count fenced code blocks (```...```)
    counts['code_blocks'] = len(re.findall(r'```', content)) // 2  # Divide by 2 for pairs

    # Count tables (look for Markdown table rows with |)
    table_lines = [line for line in content.split('\n') if line.strip().startswith('|')]
    # Rough estimate: count of table separator lines (|---|---|)
    counts['tables'] = len([line for line in table_lines if '---' in line])

    # Count algorithm/tikz blocks (preserved as latex code blocks)
    counts['algorithms'] = len(re.findall(r'```latex.*?\\begin\{algorithm\}', content, flags=re.DOTALL))
    counts['tikz'] = len(re.findall(r'\\begin\{tikzpicture\}', content))

    # Count preserved comment blocks
    counts['comment_blocks'] = len(re.findall(r'> \*\*COMMENTED SECTION:\*\*', content))
    counts['authcomments'] = len(re.findall(r'> \*\*AUTHOR COMMENT:\*\*', content))

    return counts


def validate_file_pair(tex_file: Path, md_file: Path) -> Tuple[bool, str]:
    """Validate a LaTeX/Markdown file pair."""
    print(f"\n{'='*70}")
    print(f"Validating: {tex_file.name} -> {md_file.name}")
    print(f"{'='*70}")

    # Read files
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Count elements
    tex_counts = count_latex_elements(tex_content)
    md_counts = count_markdown_elements(md_content)

    # Report counts
    print("\nElement Count Comparison:")
    print(f"{'Element':<25} {'LaTeX':<10} {'Markdown':<10} {'Status':<10}")
    print(f"{'-'*55}")

    all_good = True
    for key in tex_counts:
        tex_val = tex_counts[key]
        md_val = md_counts.get(key, 0)

        # Allow some tolerance for inline math (can be embedded in other structures)
        if key == 'inline_math':
            status = "✓" if abs(tex_val - md_val) <= tex_val * 0.1 else "⚠"
        # For comments, we may have combined some types
        elif 'comment' in key:
            status = "✓" if md_val > 0 or tex_val == 0 else "⚠"
        else:
            status = "✓" if tex_val == md_val else "⚠"

        if status == "⚠":
            all_good = False

        print(f"{key:<25} {tex_val:<10} {md_val:<10} {status:<10}")

    # Check file sizes (Markdown should be similar order of magnitude)
    tex_size = len(tex_content)
    md_size = len(md_content)
    size_ratio = md_size / tex_size if tex_size > 0 else 0

    print(f"\nFile Sizes:")
    print(f"  LaTeX:    {tex_size:,} bytes")
    print(f"  Markdown: {md_size:,} bytes")
    print(f"  Ratio:    {size_ratio:.2f}")

    if size_ratio < 0.5:
        print("  ⚠ Warning: Markdown file significantly smaller than LaTeX")
        all_good = False
    elif size_ratio > 0.7 and size_ratio < 1.3:
        print("  ✓ Size ratio looks reasonable")

    return all_good, md_file.name


def main():
    """Validate all three conversions."""
    base_dir = Path("<home>/Desktop/cursor/paper_templates/pinn_instruction")
    md_dir = base_dir / "markdown_conversions"

    files_to_check = [
        ("CTL-instruction-final.tex", "CTL-instruction-final.md"),
        ("sampling_method_instruction.tex", "sampling_method_instruction.md"),
        ("PINN_architecture_plan.tex", "PINN_architecture_plan.md")
    ]

    all_results = []

    for tex_name, md_name in files_to_check:
        tex_path = base_dir / tex_name
        md_path = md_dir / md_name

        if not tex_path.exists():
            print(f"⚠ LaTeX file not found: {tex_path}")
            continue

        if not md_path.exists():
            print(f"⚠ Markdown file not found: {md_path}")
            continue

        success, filename = validate_file_pair(tex_path, md_path)
        all_results.append((filename, success))

    # Summary
    print(f"\n{'='*70}")
    print("VALIDATION SUMMARY")
    print(f"{'='*70}")

    for filename, success in all_results:
        status = "✓ PASS" if success else "⚠ REVIEW NEEDED"
        print(f"{filename:<45} {status}")

    if all(success for _, success in all_results):
        print("\n✓ All conversions validated successfully!")
    else:
        print("\n⚠ Some conversions need review. Check warnings above.")


if __name__ == "__main__":
    main()
