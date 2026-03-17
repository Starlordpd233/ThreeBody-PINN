#!/usr/bin/env python3
"""
Spot-check script to verify critical content preservation in LaTeX to Markdown conversion.

Extracts and compares:
- Display math blocks
- Code listings
- Table content
"""

import re
from pathlib import Path
from typing import List


def extract_display_math_latex(content: str) -> List[str]:
    """Extract display math from LaTeX."""
    math_blocks = []

    # Extract equation environments
    envs = ['equation', 'align', 'align\\*', 'cases', 'gather', 'multline']
    for env in envs:
        pattern = rf'\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}'
        matches = re.findall(pattern, content, flags=re.DOTALL)
        math_blocks.extend([m.strip() for m in matches])

    # Extract \[ ... \] blocks
    matches = re.findall(r'\\\[(.*?)\\\]', content, flags=re.DOTALL)
    math_blocks.extend([m.strip() for m in matches])

    return math_blocks


def extract_display_math_markdown(content: str) -> List[str]:
    """Extract display math from Markdown."""
    # Extract $$ ... $$ blocks
    matches = re.findall(r'\$\$(.*?)\$\$', content, flags=re.DOTALL)
    return [m.strip() for m in matches]


def extract_code_blocks_latex(content: str) -> List[str]:
    """Extract code blocks from LaTeX."""
    code_blocks = []

    # Extract lstlisting
    matches = re.findall(r'\\begin\{lstlisting\}(?:\[.*?\])?(.*?)\\end\{lstlisting\}',
                        content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in matches])

    # Extract verbatim
    matches = re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',
                        content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in matches])

    return code_blocks


def extract_code_blocks_markdown(content: str) -> List[str]:
    """Extract code blocks from Markdown."""
    # Extract ```...``` blocks
    matches = re.findall(r'```[a-z]*\n(.*?)\n```', content, flags=re.DOTALL)
    return [m.strip() for m in matches]


def spot_check_file(tex_file: Path, md_file: Path):
    """Perform spot-check on a file pair."""
    print(f"\n{'='*70}")
    print(f"Spot-Checking: {tex_file.name}")
    print(f"{'='*70}\n")

    # Read files
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Check display math
    print("📐 DISPLAY MATH BLOCKS")
    print("-" * 70)
    tex_math = extract_display_math_latex(tex_content)
    md_math = extract_display_math_markdown(md_content)

    print(f"LaTeX has {len(tex_math)} display math blocks")
    print(f"Markdown has {len(md_math)} display math blocks")

    if len(tex_math) > 0:
        print(f"\n Sample LaTeX math block #1:")
        print(f"  {tex_math[0][:100]}..." if len(tex_math[0]) > 100 else f"  {tex_math[0]}")

    if len(md_math) > 0:
        print(f"\n Sample Markdown math block #1:")
        print(f"  {md_math[0][:100]}..." if len(md_math[0]) > 100 else f"  {md_math[0]}")

    # Check if first math block content is similar
    if len(tex_math) > 0 and len(md_math) > 0:
        # Remove environments and whitespace for comparison
        tex_clean = re.sub(r'\\(begin|end)\{.*?\}', '', tex_math[0]).strip()
        md_clean = md_math[0].strip()

        # Check if core content is preserved (allowing for whitespace differences)
        tex_tokens = set(re.findall(r'[a-zA-Z0-9_{}\\]+', tex_clean))
        md_tokens = set(re.findall(r'[a-zA-Z0-9_{}\\]+', md_clean))

        overlap = len(tex_tokens & md_tokens)
        tex_only = len(tex_tokens - md_tokens)

        print(f"\n Math content check:")
        print(f"  Shared tokens: {overlap}")
        print(f"  LaTeX-only tokens: {tex_only}")
        if overlap / len(tex_tokens) > 0.8:
            print(f"  ✓ Math content preserved")
        else:
            print(f"  ⚠ Possible math content loss")

    # Check code blocks
    print(f"\n\n💻 CODE BLOCKS")
    print("-" * 70)
    tex_code = extract_code_blocks_latex(tex_content)
    md_code = extract_code_blocks_markdown(md_content)

    print(f"LaTeX has {len(tex_code)} code blocks")
    print(f"Markdown has {len(md_code)} code blocks")

    if len(tex_code) > 0:
        print(f"\n Sample LaTeX code block #1 ({len(tex_code[0])} chars):")
        lines = tex_code[0].split('\n')
        print(f"  Lines: {len(lines)}")
        print(f"  First line: {lines[0][:70]}...")

    if len(md_code) > 0:
        print(f"\n Sample Markdown code block #1 ({len(md_code[0])} chars):")
        lines = md_code[0].split('\n')
        print(f"  Lines: {len(lines)}")
        print(f"  First line: {lines[0][:70]}...")

    # Check tables
    print(f"\n\n📊 TABLES")
    print("-" * 70)
    tex_tables = len(re.findall(r'\\begin\{(table|longtable)\}', tex_content))
    md_tables = len(re.findall(r'\| *--- *\|', md_content))

    print(f"LaTeX has {tex_tables} table environments")
    print(f"Markdown has {md_tables} table headers (separator lines)")

    if tex_tables == md_tables:
        print("  ✓ Table count matches")
    else:
        print(f"  ⚠ Table count mismatch ({tex_tables} vs {md_tables})")

    # Check for preserved comments
    print(f"\n\n💬 COMMENTS")
    print("-" * 70)
    tex_comments = len(re.findall(r'\\authcomment\{', tex_content))
    md_comments = len(re.findall(r'> \*\*AUTHOR COMMENT:\*\*', md_content))

    print(f"LaTeX has {tex_comments} author comments")
    print(f"Markdown has {md_comments} preserved author comments")

    if tex_comments == md_comments:
        print("  ✓ All author comments preserved")
    elif md_comments >= tex_comments * 0.9:
        print("  ✓ Most author comments preserved")
    else:
        print(f"  ⚠ Some author comments may be missing")


def main():
    """Run spot-checks on all converted files."""
    base_dir = Path("<home>/Desktop/3_body_problem/paper_templates/pinn_instruction")
    md_dir = base_dir / "markdown_conversions"

    files = [
        ("CTL-instruction-final.tex", "CTL-instruction-final.md"),
        ("sampling_method_instruction.tex", "sampling_method_instruction.md"),
        ("PINN_architecture_plan.tex", "PINN_architecture_plan.md")
    ]

    for tex_name, md_name in files:
        tex_path = base_dir / tex_name
        md_path = md_dir / md_name

        if tex_path.exists() and md_path.exists():
            spot_check_file(tex_path, md_path)

    print(f"\n{'='*70}")
    print("Spot-check complete!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
