#!/usr/bin/env python3
"""
Rigorous verification of LaTeX -> Markdown conversions using canonicalization
and hash-based multiset matching for special blocks.
"""

import re
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Set
import sys

# ----------------------------------------------------------------------
# Extraction functions (adapted from strict_comparison.py)
# ----------------------------------------------------------------------

def balanced_braces_extract(text: str, start_pos: int):
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

def extract_latex_display_math(content: str) -> List[str]:
    """Extract display math environments: \[ ... \], $$ ... $$, and equation/align/etc environments."""
    math_blocks = []
    # Environments: equation, align, align*, cases, gather, multline
    env_pattern = re.compile(r'\\(begin|end)\{(equation|align\*?|cases|gather|multline)\}')
    pos = 0
    while pos < len(content):
        # Look for $$ ... $$ (raw LaTeX display math)
        if content[pos:pos+2] == '$$':
            end = content.find('$$', pos+2)
            if end != -1:
                math = content[pos+2:end].strip()
                if math:  # Only add non-empty
                    math_blocks.append(math)
                pos = end + 2
                continue
        # Look for \[
        if content[pos:pos+2] == '\\[':
            end = content.find('\\]', pos+2)
            if end != -1:
                math = content[pos+2:end].strip()
                if math:  # Only add non-empty
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
                if inner:  # Only add non-empty
                    math_blocks.append(inner)
                pos = start + end_match.end()
                continue
        pos += 1
    return math_blocks

def extract_latex_inline_math(content: str) -> List[str]:
    """Extract inline math \(...\) and $...$ (but NOT $$...$$ display math)."""
    inline = []
    # First, remove all $$...$$ display math blocks to avoid false matches
    content_without_display = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
    # Also remove \[...\] blocks
    content_without_display = re.sub(r'\\\[.*?\\\]', '', content_without_display, flags=re.DOTALL)

    # $...$ pattern (non-greedy) - now safe since display math is removed
    dollar_matches = re.findall(r'\$([^$]+)\$', content_without_display)
    inline.extend([m.strip() for m in dollar_matches if m.strip()])
    # \(...\)
    paren_matches = re.findall(r'\\\(([^)]+)\\\)', content_without_display)
    inline.extend([m.strip() for m in paren_matches if m.strip()])
    return inline

def extract_latex_code_blocks(content: str) -> List[str]:
    """Extract lstlisting (code body only), verbatim, algorithm, and tikzpicture environments."""
    code_blocks = []
    # lstlisting with optional args - capture ONLY the code body, ignore [options]
    lst_matches = re.findall(r'\\begin\{lstlisting\}(?:\[.*?\])?(.*?)\\end\{lstlisting\}', content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in lst_matches])
    # verbatim
    verb_matches = re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}', content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in verb_matches])
    # algorithm environments - extract full environment for comparison
    alg_matches = re.findall(r'\\begin\{algorithm\}(.*?)\\end\{algorithm\}', content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in alg_matches])
    # tikzpicture environments - extract for comparison with fenced latex blocks
    tikz_matches = re.findall(r'\\begin\{tikzpicture\}(.*?)\\end\{tikzpicture\}', content, flags=re.DOTALL)
    code_blocks.extend([m.strip() for m in tikz_matches])
    # Filter out empty blocks
    return [b for b in code_blocks if b]

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

def extract_latex_comments(content: str) -> List[str]:
    """Extract comment and authcommentenv environments from LaTeX."""
    comments = []
    # \begin{comment}...\end{comment}
    comment_matches = re.findall(r'\\begin\{comment\}(.*?)\\end\{comment\}', content, flags=re.DOTALL)
    comments.extend(comment_matches)
    # \begin{authcommentenv}...\end{authcommentenv}
    authcomment_matches = re.findall(r'\\begin\{authcommentenv\}(.*?)\\end\{authcommentenv\}', content, flags=re.DOTALL)
    comments.extend(authcomment_matches)
    return comments

def remove_latex_comments(content: str) -> str:
    """Remove comment environments from LaTeX content."""
    # Remove \begin{comment}...\end{comment}
    content = re.sub(r'\\begin\{comment\}.*?\\end\{comment\}', '', content, flags=re.DOTALL)
    # Remove \begin{authcommentenv}...\end{authcommentenv}
    content = re.sub(r'\\begin\{authcommentenv\}.*?\\end\{authcommentenv\}', '', content, flags=re.DOTALL)
    # Remove \authcomment{} macros
    content = re.sub(r'\\authcomment\{[^}]+\}', '', content)
    return content

def extract_markdown_blockquotes(content: str) -> List[str]:
    """Extract blockquoted sections (lines starting with >)."""
    lines = content.split('\n')
    blockquotes = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('>'):
            # Start of a blockquote
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i])
                i += 1
            blockquotes.append('\n'.join(quote_lines))
        else:
            i += 1
    return blockquotes

def remove_markdown_blockquotes(content: str) -> str:
    """Remove blockquoted sections from Markdown content."""
    lines = content.split('\n')
    result = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('>'):
            # Skip this blockquote
            while i < len(lines) and lines[i].strip().startswith('>'):
                i += 1
        else:
            result.append(lines[i])
            i += 1
    return '\n'.join(result)

# ----------------------------------------------------------------------
# Shared helper: fence-aware extraction
# ----------------------------------------------------------------------
def find_fenced_blocks(content: str, include_quoted: bool = True) -> List[Tuple[int, int, bool, str]]:
    """Find all fenced code blocks in Markdown content.

    Args:
        content: The Markdown content to search
        include_quoted: If True, also find fences inside blockquotes (> ```lang)

    Returns:
        List of tuples (start_line, end_line, is_quoted, language)
        where start_line and end_line are inclusive line indices.
    """
    lines = content.split('\n')
    fences = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        is_quoted = False
        lang = ''

        # Check for blockquoted fence: > ```lang
        if include_quoted and line.startswith('>'):
            # Remove the quote prefix and check for fence
            after_quote = line.lstrip('>').strip()
            if after_quote.startswith('```'):
                is_quoted = True
                # Extract language
                lang_match = re.match(r'```(\w*)', after_quote)
                if lang_match:
                    lang = lang_match.group(1).lower()
            else:
                i += 1
                continue

        # Check for normal fence: ```lang
        if not is_quoted and line.startswith('```'):
            lang_match = re.match(r'```(\w*)', line)
            if lang_match:
                lang = lang_match.group(1).lower()
            is_quoted = False
        elif not is_quoted:
            i += 1
            continue

        # If we found a fence, find its closing pair
        start_line = i
        i += 1
        while i < len(lines):
            end_line = lines[i].strip()
            # Check for matching closing fence (same quote level)
            if is_quoted:
                if end_line.startswith('>'):
                    after_quote = end_line.lstrip('>').strip()
                    if after_quote == '```':
                        fences.append((start_line, i, is_quoted, lang))
                        break
            else:
                if end_line == '```':
                    fences.append((start_line, i, is_quoted, lang))
                    break
            i += 1
        i += 1

    return fences

def is_line_in_fence(line_idx: int, fences: List[Tuple[int, int, bool, str]]) -> bool:
    """Check if a line index is within any fenced block."""
    for start, end, _, _ in fences:
        if start <= line_idx <= end:
            return True
    return False

def extract_markdown_display_math(content: str) -> List[str]:
    """Extract $$ ... $$ blocks (excluding fenced code blocks)."""
    # Find all fenced blocks to exclude
    fences = find_fenced_blocks(content, include_quoted=True)
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        # Skip fenced blocks
        if is_line_in_fence(i, fences):
            i += 1
            continue

        # Look for $$ ... $$ (may span multiple lines)
        line = lines[i]
        if '$$' in line:
            # Find opening $$
            open_idx = line.find('$$')
            if open_idx != -1:
                # Start collecting the math content
                math_start = i
                math_content = line[open_idx + 2:]

                # Check if closing $$ is on same line
                close_idx = math_content.find('$$')
                if close_idx != -1:
                    # Single-line display math
                    math = math_content[:close_idx].strip()
                    if math:
                        result.append(math)
                    i += 1
                    continue

                # Multi-line display math - find closing
                i += 1
                while i < len(lines):
                    # Skip fenced blocks while looking for closing
                    if is_line_in_fence(i, fences):
                        i += 1
                        continue

                    if '$$' in lines[i]:
                        close_idx = lines[i].find('$$')
                        if close_idx != -1:
                            # Found closing
                            math_content += '\n' + lines[i][:close_idx]
                            math = math_content.strip()
                            if math:
                                result.append(math)
                            i += 1
                            break
                    math_content += '\n' + lines[i]
                    i += 1
                continue

        i += 1

    return result

def extract_markdown_inline_math(content: str) -> List[str]:
    """Extract $...$ inline math (excluding fenced blocks and display math)."""
    # Find all fenced blocks to exclude
    fences = find_fenced_blocks(content, include_quoted=True)
    lines = content.split('\n')

    # Build content outside of fences
    non_fence_lines = []
    for i, line in enumerate(lines):
        if not is_line_in_fence(i, fences):
            non_fence_lines.append(line)
    content_outside_fences = '\n'.join(non_fence_lines)

    # Also remove display math $$...$$ to avoid false matches
    content_outside_fences = re.sub(r'\$\$.*?\$\$', '', content_outside_fences, flags=re.DOTALL)

    # Now extract $...$
    matches = re.findall(r'\$([^$]+)\$', content_outside_fences)
    return [m.strip() for m in matches]

def extract_markdown_code_blocks(content: str) -> List[str]:
    """Extract fenced code blocks ```...``` (including quoted fences > ```), excluding table-containing fences."""
    fences = find_fenced_blocks(content, include_quoted=True)
    lines = content.split('\n')
    code_blocks = []

    # Get all table-containing latex fences to exclude
    table_fences = set()
    for start, end, is_quoted, lang in fences:
        if lang == 'latex':
            # Check if this fence contains a table
            block_lines = []
            for i in range(start + 1, end):
                line = lines[i]
                if is_quoted and line.strip().startswith('>'):
                    line = line.lstrip('>').lstrip()
                block_lines.append(line)
            block_content = '\n'.join(block_lines)
            if '\\begin{table}' in block_content or '\\begin{longtable}' in block_content:
                table_fences.add((start, end))

    for start, end, is_quoted, lang in fences:
        # Skip fences that contain tables
        if (start, end) in table_fences:
            continue

        # Extract the code content (excluding fence lines)
        # For quoted fences, we need to handle the > prefix
        if is_quoted:
            # Remove the > prefix from each line
            block_lines = []
            for i in range(start + 1, end):
                line = lines[i]
                if line.strip().startswith('>'):
                    # Remove the quote prefix
                    line = line.lstrip('>').lstrip()
                block_lines.append(line)
            block_content = '\n'.join(block_lines).strip()
            if block_content:  # Only add non-empty
                code_blocks.append(block_content)
        else:
            # Normal fence
            block_lines = lines[start + 1:end]
            block_content = '\n'.join(block_lines).strip()
            if block_content:  # Only add non-empty
                code_blocks.append(block_content)

    return code_blocks

def extract_markdown_tables(content: str) -> List[Tuple[str, str]]:
    """Extract Markdown table blocks (pipe tables) or fenced latex blocks with tables.
    Returns list of (type, content) where type is 'latex' or 'pipe'.
    Includes quoted fences (> ```latex) containing tables."""
    tables = []
    lines = content.split('\n')
    i = 0

    # Get all fenced latex blocks first
    fences = find_fenced_blocks(content, include_quoted=True)
    latex_fences = [(s, e, iq) for s, e, iq, lang in fences if lang == 'latex']

    # Check for fenced latex blocks containing table/longtable environments
    for start, end, is_quoted in latex_fences:
        block_lines = []
        for j in range(start + 1, end):
            line = lines[j]
            if is_quoted and line.strip().startswith('>'):
                line = line.lstrip('>').lstrip()
            block_lines.append(line)
        block_content = '\n'.join(block_lines)

        if '\\begin{table}' in block_content or '\\begin{longtable}' in block_content:
            tables.append(('latex', block_content))

    # Now look for pipe tables (lines starting with |) outside of any fence
    while i < len(lines):
        # Skip if inside any fence
        if is_line_in_fence(i, fences):
            i += 1
            continue

        # Check for Markdown tables (lines starting with |)
        if lines[i].startswith('|'):
            # Start of a table
            table_lines = []
            while i < len(lines) and not is_line_in_fence(i, fences) and lines[i].startswith('|'):
                table_lines.append(lines[i])
                i += 1
            tables.append(('pipe', '\n'.join(table_lines)))
        else:
            i += 1

    return tables

# ----------------------------------------------------------------------
# Canonicalization functions
# ----------------------------------------------------------------------

def normalize_whitespace(text: str) -> str:
    """Normalize whitespace: replace multiple spaces/newlines with single space."""
    return ' '.join(text.split())

def canonicalize_math(text: str) -> str:
    """Canonicalize math content: whitespace normalization only."""
    return normalize_whitespace(text)

def canonicalize_code(text: str) -> str:
    """Canonicalize code block: normalize line endings to \n, strip surrounding whitespace."""
    # Ensure \n line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Remove trailing newline
    text = text.strip()
    return text

def canonicalize_table_latex(text: str) -> str:
    """Canonicalize LaTeX table environment: aggressive whitespace normalization."""
    # Remove all whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def canonicalize_table_pipe(text: str) -> str:
    """Canonicalize Markdown pipe table: extract cell text content.
    This is a simplified version: remove separators, split by '|', strip whitespace and **."""
    lines = text.strip().split('\n')
    # Skip separator line (contains ---)
    rows = [line for line in lines if '---' not in line]
    cells = []
    for row in rows:
        # Split by '|', remove empty ends
        parts = row.split('|')
        if parts and parts[0] == '':
            parts = parts[1:]
        if parts and parts[-1] == '':
            parts = parts[:-1]
        for cell in parts:
            cell = cell.strip()
            # Remove bold markers **
            if cell.startswith('**') and cell.endswith('**'):
                cell = cell[2:-2]
            cells.append(cell)
    # Sort cells? Not appropriate. Keep order? We'll just join with space.
    return ' '.join(cells)

# ----------------------------------------------------------------------
# Hashing and multiset comparison
# ----------------------------------------------------------------------

def compute_hash(text: str) -> str:
    """Compute SHA256 hash of text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def compare_multiset(tex_blocks: List[str], md_blocks: List[str], canonicalize_func,
                     category: str, file_name: str) -> Tuple[bool, List[str]]:
    """Compare two lists of blocks via canonicalization and hash multiset.
    Returns (success, list_of_messages)."""
    # Canonicalize and hash
    tex_hashes = {}
    for block in tex_blocks:
        canon = canonicalize_func(block)
        h = compute_hash(canon)
        tex_hashes[h] = tex_hashes.get(h, 0) + 1
    md_hashes = {}
    for block in md_blocks:
        canon = canonicalize_func(block)
        h = compute_hash(canon)
        md_hashes[h] = md_hashes.get(h, 0) + 1

    # Compare
    all_hashes = set(tex_hashes.keys()) | set(md_hashes.keys())
    mismatches = []
    for h in all_hashes:
        t = tex_hashes.get(h, 0)
        m = md_hashes.get(h, 0)
        if t != m:
            mismatches.append((h, t, m))

    if not mismatches:
        return True, [f"✓ {category}: all blocks match (count {len(tex_blocks)})"]
    else:
        messages = [f"⚠ {category}: mismatched blocks"]
        for h, t, m in mismatches[:5]:  # limit output
            # Find example block with this hash
            example = None
            for block in tex_blocks:
                if compute_hash(canonicalize_func(block)) == h:
                    example = block[:200]
                    break
            if example is None:
                for block in md_blocks:
                    if compute_hash(canonicalize_func(block)) == h:
                        example = block[:200]
                        break
            messages.append(f"  Hash {h[:16]}...: LaTeX {t} vs Markdown {m}")
            messages.append(f"    Example: {example}")
        return False, messages

# ----------------------------------------------------------------------
# Main verification per file pair
# ----------------------------------------------------------------------

def verify_file_pair(tex_path: Path, md_path: Path) -> Tuple[bool, List[str]]:
    """Verify a single pair."""
    with open(tex_path, 'r', encoding='utf-8') as f:
        tex_content = f.read()
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    messages = []
    all_pass = True

    # Remove comment blocks from both sources (they're converted to blockquotes intentionally)
    tex_content_clean = remove_latex_comments(tex_content)
    md_content_clean = remove_markdown_blockquotes(md_content)

    # Display math
    tex_display = extract_latex_display_math(tex_content_clean)
    md_display = extract_markdown_display_math(md_content_clean)
    ok, msgs = compare_multiset(tex_display, md_display, canonicalize_math,
                                "Display math", tex_path.name)
    all_pass = all_pass and ok
    messages.extend(msgs)

    # Inline math
    tex_inline = extract_latex_inline_math(tex_content_clean)
    md_inline = extract_markdown_inline_math(md_content_clean)
    ok, msgs = compare_multiset(tex_inline, md_inline, canonicalize_math,
                                "Inline math", tex_path.name)
    all_pass = all_pass and ok
    messages.extend(msgs)

    # Code blocks
    tex_code = extract_latex_code_blocks(tex_content_clean)
    md_code = extract_markdown_code_blocks(md_content_clean)
    ok, msgs = compare_multiset(tex_code, md_code, canonicalize_code,
                                "Code blocks", tex_path.name)
    all_pass = all_pass and ok
    messages.extend(msgs)

    # Tables
    tex_tables = extract_latex_tables(tex_content_clean)
    md_tables_raw = extract_markdown_tables(md_content_clean)
    # Separate latex-fenced tables from pipe tables
    md_latex_tables = [content for typ, content in md_tables_raw if typ == 'latex']
    md_pipe_tables = [content for typ, content in md_tables_raw if typ == 'pipe']

    # First try to match LaTeX tables with fenced LaTeX tables
    ok1, msgs1 = compare_multiset(tex_tables, md_latex_tables, canonicalize_table_latex,
                                  "Tables (LaTeX fenced)", tex_path.name)
    # If there are pipe tables, we need a more sophisticated matching.
    # For simplicity, we'll just note.
    if md_pipe_tables:
        messages.append(f"⚠ Tables: {len(md_pipe_tables)} Markdown pipe tables present (need manual check)")
        all_pass = False

    all_pass = all_pass and ok1
    messages.extend(msgs1)

    return all_pass, messages

def main():
    base_dir = Path("<home>/Desktop/cursor/pinn_instruction")
    md_dir = base_dir / "markdown_conversions"
    pairs = [
        ("CTL-instruction-final.tex", "CTL-instruction-final.md"),
        ("sampling_method_instruction.tex", "sampling_method_instruction.md"),
        ("PINN_architecture_plan.tex", "PINN_architecture_plan.md")
    ]

    overall_pass = True
    for tex_name, md_name in pairs:
        tex_path = base_dir / tex_name
        md_path = md_dir / md_name
        if not tex_path.exists() or not md_path.exists():
            print(f"Missing file: {tex_path} or {md_path}")
            overall_pass = False
            continue

        print(f"\n{'='*70}")
        print(f"Rigorous verification: {tex_name}")
        print(f"{'='*70}")
        pass_flag, messages = verify_file_pair(tex_path, md_path)
        overall_pass = overall_pass and pass_flag
        for msg in messages:
            print(msg)

    print(f"\n{'='*70}")
    print("OVERALL RESULT")
    print(f"{'='*70}")
    if overall_pass:
        print("✓ All conversions PASS rigorous verification")
        sys.exit(0)
    else:
        print("⚠ Some conversions FAIL verification")
        sys.exit(1)

if __name__ == "__main__":
    main()