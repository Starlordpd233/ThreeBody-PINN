#!/usr/bin/env python3
"""
Strict comparison of LaTeX and Markdown conversions for special blocks.
Extracts metadata, display math, inline math, code blocks, tables using
brace-balanced parsing where needed.
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import sys

def balanced_braces_extract(text: str, start_pos: int) -> Optional[Tuple[int, int]]:
    """Given a string and starting position of '{', return indices of matching '}'.
    Returns (start, end) inclusive, or None if unbalanced."""
    if start_pos >= len(text) or text[start_pos] != '{':
        return None
    depth = 1
    i = start_pos + 1
    while i < len(text) and depth > 0:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    if depth == 0:
        return (start_pos, i - 1)
    return None

def extract_latex_metadata(content: str) -> Dict[str, str]:
    """Extract title, author, date using brace-balanced parsing."""
    metadata = {}
    # Pattern for \title{...}, \author{...}, \date{...}
    patterns = [('title', r'\\title'), ('author', r'\\author'), ('date', r'\\date')]
    for key, pat in patterns:
        for match in re.finditer(pat, content):
            # Find next '{' after the macro
            idx = match.end()
            while idx < len(content) and content[idx].isspace():
                idx += 1
            if idx < len(content) and content[idx] == '{':
                brace = balanced_braces_extract(content, idx)
                if brace:
                    start, end = brace
                    # Extract content inside braces, excluding braces
                    inner = content[start+1:end].strip()
                    metadata[key] = inner
                    break  # take first occurrence
    return metadata

def extract_latex_display_math(content: str) -> List[str]:
    """Extract display math environments and \[ ... \] with balanced braces."""
    math_blocks = []
    # Environments: equation, align, align*, cases, gather, multline
    env_pattern = re.compile(r'\\(begin|end)\{(equation|align\*?|cases|gather|multline)\}')
    pos = 0
    while pos < len(content):
        # Look for \[
        if content[pos:pos+2] == '\\[':
            end = content.find('\\]', pos+2)
            if end != -1:
                math = content[pos+2:end].strip()
                math_blocks.append(math)
                pos = end + 2
                continue
        # Look for \begin{...}
        begin_match = re.search(r'\\begin\{(equation|align\*?|cases|gather|multline)\}', content[pos:])
        if begin_match:
            env = begin_match.group(1)
            start = pos + begin_match.start()
            # Find matching \end{env}
            pattern = r'\\end\{' + re.escape(env) + r'\}'
            end_match = re.search(pattern, content[start:])
            if end_match:
                end = start + end_match.start()
                inner = content[start + begin_match.end():end].strip()
                math_blocks.append(inner)
                pos = start + end_match.end()
                continue
        pos += 1
    return math_blocks

def extract_latex_inline_math(content: str) -> List[str]:
    """Extract inline math $...$ and \(...\) with balanced dollar signs? Assume no nested $."""
    inline = []
    # $...$ pattern (non-greedy)
    dollar_matches = re.findall(r'\$([^$]+)\$', content)
    inline.extend([m.strip() for m in dollar_matches])
    # \(...\)
    paren_matches = re.findall(r'\\\(([^)]+)\\\)', content)
    inline.extend([m.strip() for m in paren_matches])
    return inline

def extract_latex_code_blocks(content: str) -> List[str]:
    """Extract lstlisting and verbatim environments."""
    code_blocks = []
    # lstlisting
    lst_matches = re.findall(r'\\begin\{lstlisting\}(.*?)\\end\{lstlisting\}', content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in lst_matches])
    # verbatim
    verb_matches = re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}', content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in verb_matches])
    return code_blocks

def extract_latex_tables(content: str) -> List[str]:
    """Extract table environments (tabular inside). Returns list of raw LaTeX table code."""
    tables = []
    # Find \begin{table}...\end{table}
    table_matches = re.findall(r'\\begin\{table\}.*?\\end\{table\}', content, flags=re.DOTALL)
    tables.extend(table_matches)
    # longtable
    longtable_matches = re.findall(r'\\begin\{longtable\}.*?\\end\{longtable\}', content, flags=re.DOTALL)
    tables.extend(longtable_matches)
    return tables

def extract_markdown_frontmatter(content: str) -> Dict[str, str]:
    """Extract YAML frontmatter."""
    metadata = {}
    if content.startswith('---'):
        lines = content.split('\n')
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break
        if end_idx > 0:
            for line in lines[1:end_idx]:
                if ':' in line:
                    key, val = line.split(':', 1)
                    metadata[key.strip()] = val.strip()
    return metadata

def extract_markdown_display_math(content: str) -> List[str]:
    """Extract $$ ... $$ blocks."""
    matches = re.findall(r'\$\$(.*?)\$\$', content, flags=re.DOTALL)
    return [m.strip() for m in matches]

def extract_markdown_inline_math(content: str) -> List[str]:
    """Extract $...$ inline math."""
    matches = re.findall(r'\$([^$]+)\$', content)
    return [m.strip() for m in matches]

def extract_markdown_code_blocks(content: str) -> List[str]:
    """Extract fenced code blocks ```...```."""
    matches = re.findall(r'```[a-z]*\n(.*?)\n```', content, flags=re.DOTALL)
    return [m.strip() for m in matches]

def extract_markdown_tables(content: str) -> List[str]:
    """Extract Markdown table blocks (lines starting with |) or fenced latex blocks with tables."""
    tables = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        # Check for Markdown tables (lines starting with |)
        if lines[i].startswith('|'):
            # Start of a table
            table_lines = []
            while i < len(lines) and lines[i].startswith('|'):
                table_lines.append(lines[i])
                i += 1
            tables.append('\n'.join(table_lines))
        # Check for fenced latex blocks containing table/longtable environments
        elif lines[i].strip().startswith('```') and 'latex' in lines[i].lower():
            # Start of a fenced latex block
            fence_start = i
            i += 1
            # Find the closing fence
            while i < len(lines) and not lines[i].strip().startswith('```'):
                i += 1
            # Check if this block contains a table/longtable environment
            if i < len(lines):
                block_content = '\n'.join(lines[fence_start+1:i])
                if '\\begin{table}' in block_content or '\\begin{longtable}' in block_content:
                    tables.append(block_content)
            i += 1  # Move past closing fence
        else:
            i += 1
    return tables

def normalize_whitespace(text: str) -> str:
    """Normalize whitespace: replace multiple spaces/newlines with single space."""
    return ' '.join(text.split())

def compare_blocks(tex_blocks: List[str], md_blocks: List[str], category: str, file_name: str):
    """Compare two lists of blocks, report mismatches."""
    tex_norm = [normalize_whitespace(b) for b in tex_blocks]
    md_norm = [normalize_whitespace(b) for b in md_blocks]
    # Simple count comparison
    if len(tex_norm) != len(md_norm):
        print(f"  ⚠ {category}: count mismatch LaTeX={len(tex_norm)} Markdown={len(md_norm)}")
        # Try to match by content
        # For simplicity, just report missing
        for i, block in enumerate(tex_norm[:3]):
            if i >= len(md_norm):
                print(f"    Missing in Markdown: {block[:80]}...")
        for i, block in enumerate(md_norm[:3]):
            if i >= len(tex_norm):
                print(f"    Extra in Markdown: {block[:80]}...")
    else:
        # Compare each pair
        mismatches = []
        for idx, (t, m) in enumerate(zip(tex_norm, md_norm)):
            if t != m:
                mismatches.append(idx)
        if mismatches:
            print(f"  ⚠ {category}: {len(mismatches)}/{len(tex_norm)} blocks differ")
            for idx in mismatches[:2]:
                print(f"    Block {idx}: LaTeX: {tex_blocks[idx][:80]}...")
                print(f"            Markdown: {md_blocks[idx][:80]}...")
        else:
            print(f"  ✓ {category}: all {len(tex_norm)} blocks match")

def compare_file(tex_path: Path, md_path: Path):
    """Compare a LaTeX/Markdown file pair."""
    print(f"\n{'='*70}")
    print(f"Strict comparison: {tex_path.name}")
    print(f"{'='*70}")
    with open(tex_path, 'r', encoding='utf-8') as f:
        tex_content = f.read()
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Metadata
    tex_meta = extract_latex_metadata(tex_content)
    md_meta = extract_markdown_frontmatter(md_content)
    print("\n📄 METADATA")
    for key in ['title', 'author', 'date']:
        t = tex_meta.get(key, '')
        m = md_meta.get(key, '')
        if t != m:
            print(f"  ⚠ {key}: mismatch")
            print(f"    LaTeX: {t[:100]}")
            print(f"    Markdown: {m[:100]}")
        else:
            print(f"  ✓ {key}: match")
    # Display math
    tex_display = extract_latex_display_math(tex_content)
    md_display = extract_markdown_display_math(md_content)
    compare_blocks(tex_display, md_display, "Display math", tex_path.name)
    # Inline math
    tex_inline = extract_latex_inline_math(tex_content)
    md_inline = extract_markdown_inline_math(md_content)
    compare_blocks(tex_inline, md_inline, "Inline math", tex_path.name)
    # Code blocks
    tex_code = extract_latex_code_blocks(tex_content)
    md_code = extract_markdown_code_blocks(md_content)
    compare_blocks(tex_code, md_code, "Code blocks", tex_path.name)
    # Tables
    tex_tables = extract_latex_tables(tex_content)
    md_tables = extract_markdown_tables(md_content)
    compare_blocks(tex_tables, md_tables, "Tables", tex_path.name)
    # Additional check for raw LaTeX tables preserved as code blocks
    # Not implemented

def main():
    base_dir = Path("<home>/Desktop/cursor/paper_templates/pinn_instruction")
    md_dir = base_dir / "markdown_conversions"
    pairs = [
        ("CTL-instruction-final.tex", "CTL-instruction-final.md"),
        ("sampling_method_instruction.tex", "sampling_method_instruction.md"),
        ("PINN_architecture_plan.tex", "PINN_architecture_plan.md")
    ]
    for tex_name, md_name in pairs:
        tex_path = base_dir / tex_name
        md_path = md_dir / md_name
        if tex_path.exists() and md_path.exists():
            compare_file(tex_path, md_path)
        else:
            print(f"Missing file: {tex_path} or {md_path}")

if __name__ == "__main__":
    main()