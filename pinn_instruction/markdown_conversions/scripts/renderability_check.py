#!/usr/bin/env python3
"""
Renderability check for LaTeX -> Markdown conversions.
Checks:
1. No raw LaTeX sectioning/list environments in prose (outside code fences).
2. Valid Markdown tables (proper header separator, consistent columns).
3. YAML frontmatter sanity (bounded by ---, no broken lines).
4. No stray LaTeX column spec fragments in table rows.
"""

import re
from pathlib import Path
from typing import List, Tuple

def check_frontmatter(content: str) -> Tuple[bool, List[str]]:
    """Check YAML frontmatter."""
    issues = []
    lines = content.split('\n')
    if len(lines) < 2 or lines[0] != '---':
        issues.append("Missing frontmatter start '---'")
        return False, issues
    # Find second '---'
    end_idx = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_idx = i
            break
    if end_idx == -1:
        issues.append("Missing frontmatter end '---'")
        return False, issues
    # Check frontmatter lines for broken fields
    for idx, line in enumerate(lines[1:end_idx], start=1):
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) < 2 or parts[1].strip() == '':
                issues.append(f"Line {idx+1}: Frontmatter field missing value: {line}")
    return len(issues) == 0, issues

def is_inside_code_block(line_idx: int, code_block_starts: List[int], code_block_ends: List[int]) -> bool:
    """Check if line index is inside a code block."""
    for start, end in zip(code_block_starts, code_block_ends):
        if start <= line_idx <= end:
            return True
    return False

def find_code_blocks(content: str) -> Tuple[List[int], List[int]]:
    """Find start and end line indices of fenced code blocks, including those inside blockquotes."""
    starts = []
    ends = []
    lines = content.split('\n')
    in_block = False
    block_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Check for fenced code blocks (with or without blockquote prefix)
        if stripped.startswith('```'):
            if not in_block:
                starts.append(i)
                in_block = True
                block_start = i
            else:
                ends.append(i)
                in_block = False
    # If block not closed, ignore
    if in_block:
        starts.pop()
    return starts, ends


def is_inside_quoted_code_block(line_idx: int, lines: List[str]) -> bool:
    """Check if a line is inside a code block that is inside a blockquote.

    Looks backwards from current line to find if we're inside a ```...``` fence
    that is preceded by blockquote markers (>).
    """
    # Scan backwards from current line
    i = line_idx
    while i >= 0:
        line = lines[i].strip()

        # If we hit a line that's not a blockquote line and not a fence, we exit
        if not line.startswith('>') and '```' not in line:
            return False

        # If we find an opening fence on a blockquote line, we found a quoted code block
        if line.startswith('>') and '```' in line:
            return True

        # If we find a fence without blockquote prefix, not a quoted code block
        if '```' in line and not line.startswith('>'):
            return False

        i -= 1

    return False

def check_stray_latex(content: str) -> Tuple[bool, List[str]]:
    """Check for stray LaTeX commands outside code blocks."""
    # Patterns to flag (these should not appear in prose)
    patterns = [
        (r'\\section\*?\{', 'Raw LaTeX sectioning'),
        (r'\\subsection\*?\{', 'Raw LaTeX subsection'),
        (r'\\subsubsection\*?\{', 'Raw LaTeX subsubsection'),
        (r'\\begin\{itemize\}', 'Raw LaTeX itemize env'),
        (r'\\end\{itemize\}', 'Raw LaTeX itemize env'),
        (r'\\begin\{enumerate\}', 'Raw LaTeX enumerate env'),
        (r'\\end\{enumerate\}', 'Raw LaTeX enumerate env'),
        (r'\\FloatBarrier', 'FloatBarrier command'),
        (r'\\begin\{table\}', 'Raw LaTeX table env'),
        (r'\\end\{table\}', 'Raw LaTeX table env'),
        (r'\\begin\{longtable\}', 'Raw LaTeX longtable env'),
        (r'\\end\{longtable\}', 'Raw LaTeX longtable env'),
        (r'\\begin\{algorithm\}', 'Raw LaTeX algorithm env'),
        (r'\\end\{algorithm\}', 'Raw LaTeX algorithm env'),
        (r'\\begin\{tikzpicture\}', 'Raw LaTeX tikz picture env'),
        (r'\\end\{tikzpicture\}', 'Raw LaTeX tikz picture env'),
    ]
    starts, ends = find_code_blocks(content)
    lines = content.split('\n')
    issues = []
    for i, line in enumerate(lines):
        # Skip if inside a regular code block
        if is_inside_code_block(i, starts, ends):
            continue
        # Skip if inside a code block that's inside a blockquote
        if is_inside_quoted_code_block(i, lines):
            continue
        for pattern, desc in patterns:
            if re.search(pattern, line):
                issues.append(f"Line {i+1}: {desc}: {line.strip()[:80]}")
    return len(issues) == 0, issues

def check_tables(content: str) -> Tuple[bool, List[str]]:
    """Check Markdown tables for validity."""
    starts, ends = find_code_blocks(content)
    lines = content.split('\n')
    issues = []
    i = 0
    while i < len(lines):
        if is_inside_code_block(i, starts, ends):
            i += 1
            continue
        line = lines[i].rstrip()
        # Look for a line that starts with '|' and contains '---'
        if line.startswith('|') and '---' in line:
            # This is a separator line
            # Find preceding line (header)
            if i == 0 or not lines[i-1].startswith('|'):
                issues.append(f"Line {i+1}: Table separator without header row")
                # Skip checking rows because no valid header
                j = i + 1
                while j < len(lines) and lines[j].strip() != '' and lines[j].startswith('|'):
                    j += 1
                i = j
                continue
            # Count columns in header and separator
            header_cols = lines[i-1].count('|') - 1  # exclude leading/trailing
            sep_cols = line.count('|') - 1
            if header_cols != sep_cols:
                issues.append(f"Line {i+1}: Column count mismatch: header {header_cols}, separator {sep_cols}")
            # Check for stray LaTeX column spec fragments
            if re.search(r'@\{\}|p\{.*?\}|l|c|r', line):
                issues.append(f"Line {i+1}: Stray LaTeX column spec fragment: {line}")
            # Check following rows until empty line or non-table row
            j = i + 1
            while j < len(lines) and lines[j].strip() != '' and lines[j].startswith('|'):
                row = lines[j]
                row_cols = row.count('|') - 1
                if row_cols != header_cols:
                    issues.append(f"Line {j+1}: Row column count mismatch: expected {header_cols}, got {row_cols}")
                # Check for stray LaTeX commands
                if '\\thead' in row or '\\multicolumn' in row or '\\textbf' in row:
                    # allow \textbf? maybe okay, but flag for review
                    issues.append(f"Line {j+1}: Possible LaTeX command in table cell: {row[:80]}")
                j += 1
            i = j
        else:
            i += 1
    return len(issues) == 0, issues

def check_file(md_path: Path):
    """Run all checks on a Markdown file."""
    print(f"\n{'='*70}")
    print(f"Checking renderability of: {md_path.name}")
    print(f"{'='*70}")
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    all_issues = []

    # Frontmatter check
    if content.startswith('---'):
        ok, issues = check_frontmatter(content)
        if not ok:
            all_issues.extend(issues)
        else:
            print("✓ Frontmatter syntax OK")
    else:
        print("⚠ No frontmatter detected")

    # Stray LaTeX check
    ok, issues = check_stray_latex(content)
    if ok:
        print("✓ No stray LaTeX commands in prose")
    else:
        all_issues.extend(issues)
        print(f"⚠ {len(issues)} stray LaTeX command(s) found")

    # Table check
    ok, issues = check_tables(content)
    if ok:
        print("✓ Tables appear valid")
    else:
        all_issues.extend(issues)
        print(f"⚠ {len(issues)} table issue(s) found")

    # Summary
    if all_issues:
        print(f"\nISSUES ({len(all_issues)}):")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("\n✓ All renderability checks passed!")

def main():
    md_dir = Path("<home>/Desktop/3_body_problem/paper_templates/pinn_instruction/markdown_conversions")
    files = [
        "CTL-instruction-final.md",
        "sampling_method_instruction.md",
        "PINN_architecture_plan.md"
    ]
    for fname in files:
        md_path = md_dir / fname
        if md_path.exists():
            check_file(md_path)
        else:
            print(f"File not found: {md_path}")

if __name__ == "__main__":
    main()