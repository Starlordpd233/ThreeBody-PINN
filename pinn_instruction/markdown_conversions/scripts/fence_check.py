#!/usr/bin/env python3
"""
Fence integrity and H1 title check for Markdown files.
"""

import re
import sys
from pathlib import Path

def find_code_blocks(content: str):
    """Return (starts, ends) line indices of fenced code blocks.
    Adapted from renderability_check.py"""
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

def is_inside_code_block(line_idx: int, starts, ends) -> bool:
    """Check if line index is inside a code block."""
    for start, end in zip(starts, ends):
        if start <= line_idx <= end:
            return True
    return False

def check_fence_integrity(content: str):
    """Check balanced code fences and display-math fences."""
    lines = content.split('\n')
    starts, ends = find_code_blocks(content)
    issues = []

    # Code fence balance: each start must have an end
    if len(starts) != len(ends):
        issues.append(f"Unbalanced code fences: {len(starts)} starts, {len(ends)} ends")

    # Display-math fence balance: count '$$' not inside code blocks
    math_fence_count = 0
    for i, line in enumerate(lines):
        if is_inside_code_block(i, starts, ends):
            continue
        # Count occurrences of '$$' in line (non-overlapping)
        count = line.count('$$')
        math_fence_count += count
    if math_fence_count % 2 != 0:
        issues.append(f"Unbalanced display-math fences: found {math_fence_count} '$$' tokens (must be even)")

    return issues

def check_h1_title(content: str):
    """Check that after frontmatter there is exactly one H1 title line."""
    lines = content.split('\n')
    # Find frontmatter bounds
    if not (len(lines) >= 2 and lines[0] == '---'):
        return ["No frontmatter start '---'"]
    end_idx = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_idx = i
            break
    if end_idx == -1:
        return ["No frontmatter end '---'"]
    # After frontmatter, skip blank lines
    i = end_idx + 1
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    # Now count H1 lines (starting with '# ')
    h1_lines = []
    for idx in range(i, len(lines)):
        if lines[idx].startswith('# '):
            h1_lines.append(idx)
    if len(h1_lines) == 0:
        return ["Missing H1 title after frontmatter"]
    if len(h1_lines) > 1:
        return [f"Multiple H1 titles at lines {h1_lines}"]
    # Optionally ensure no other H1 later (already caught)
    return []

def check_file(md_path: Path):
    """Run fence and title checks."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    issues.extend(check_fence_integrity(content))
    issues.extend(check_h1_title(content))

    if issues:
        print(f"\n{md_path.name}: FAIL")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n{md_path.name}: PASS")
        return True

def main():
    md_dir = Path("<home>/Desktop/cursor/paper_templates/pinn_instruction/markdown_conversions")
    files = [
        "CTL-instruction-final.md",
        "sampling_method_instruction.md",
        "PINN_architecture_plan.md"
    ]
    all_pass = True
    for fname in files:
        md_path = md_dir / fname
        if md_path.exists():
            if not check_file(md_path):
                all_pass = False
        else:
            print(f"File not found: {md_path}")
            all_pass = False
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()