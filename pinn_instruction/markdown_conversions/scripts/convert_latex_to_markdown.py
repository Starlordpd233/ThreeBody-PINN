#!/usr/bin/env python3
"""
Lossless LaTeX to Markdown Converter for PINN Instruction Documents

This script converts LaTeX documents to Markdown while preserving:
- Mathematical expressions (inline and display)
- Code listings and verbatim blocks
- Tables (including longtables)
- Algorithms and TikZ figures
- Comment blocks
- Bibliography and links

Author: Automated conversion script
"""

import re
import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import argparse


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


def extract_brace_content(text: str, pattern: str) -> List[str]:
    """Extract content from {braces} using brace-balanced parsing."""
    results = []
    for match in re.finditer(pattern, text):
        idx = match.end()
        # Skip whitespace
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx < len(text) and text[idx] == '{':
            brace = balanced_braces_extract(text, idx)
            if brace:
                start, end = brace
                inner = text[start+1:end].strip()
                results.append(inner)
    return results


class LaTeXToMarkdownConverter:
    """Converts LaTeX documents to Markdown with lossless preservation of content."""

    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.content = ""
        self.metadata = {}
        self.token_map = {}  # For placeholder token storage
        self.token_counter = 0

    def read_file(self) -> str:
        """Read the input LaTeX file."""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return f.read()

    def _make_token(self) -> str:
        """Generate a unique token for placeholder replacement."""
        self.token_counter += 1
        return f"@@TOKEN_{self.token_counter:06d}@@"

    def extract_metadata(self, content: str) -> str:
        """Extract title, author, and date from LaTeX preamble using brace-balanced parsing."""
        # Use brace-balanced extraction for metadata
        self.metadata['title'] = extract_brace_content(content, r'\\title')
        self.metadata['author'] = extract_brace_content(content, r'\\author')
        self.metadata['date'] = extract_brace_content(content, r'\\date')

        # Take first occurrence if multiple
        for key in self.metadata:
            if isinstance(self.metadata[key], list) and self.metadata[key]:
                self.metadata[key] = self.metadata[key][0]

        # Remove preamble (everything before \begin{document})
        doc_start = content.find(r'\begin{document}')
        if doc_start != -1:
            content = content[doc_start:]
            # Remove \begin{document} and \end{document}
            content = re.sub(r'\\begin\{document\}', '', content)
            content = re.sub(r'\\end\{document\}', '', content)
            # Remove \maketitle
            content = re.sub(r'\\maketitle', '', content)

        return content.strip()

    def _extract_and_replace_blocks(self, content: str) -> str:
        """Extract special blocks (code, math, tables, etc.) and replace with tokens.
        Returns tokenized content."""
        # Order matters: extract larger blocks first to avoid nested conflicts
        # Comments first (they may contain other blocks)
        content = self._extract_comments(content)
        # Code listings
        content = self._extract_code_listings(content)
        # Display math
        content = self._extract_display_math(content)
        # Tables
        content = self._extract_tables(content)
        # Algorithms and TikZ
        content = self._extract_algorithms_tikz(content)
        return content

    def _process_blocks(self):
        """Convert stored blocks to their final Markdown representation."""
        for token, data in list(self.token_map.items()):
            if data['type'] == 'code':
                # Process code listing
                options = data.get('options', '')
                code = data.get('code', '')
                # Extract language, caption, label
                lang = ''
                caption = ''
                label = ''
                if options:
                    lang_match = re.search(r'language=(\w+)', options)
                    if lang_match:
                        lang = lang_match.group(1).lower()
                    caption_match = re.search(r'caption=\{(.+?)\}', options, re.DOTALL)
                    if caption_match:
                        caption = caption_match.group(1)
                    label_match = re.search(r'label=\{(.+?)\}', options, re.DOTALL)
                    if label_match:
                        label = label_match.group(1)
                # Build result
                result_lines = []
                if caption:
                    result_lines.append(f"**Caption:** {caption}")
                if label:
                    result_lines.append(f"**Label:** {label}")
                result_lines.append(f"```{lang}")
                result_lines.append(code.strip())
                result_lines.append("```")
                data['processed'] = '\n'.join(result_lines)
            elif data['type'] == 'display_math':
                # Keep original LaTeX math content, wrap with $$
                math_content = data['content'].strip()
                data['processed'] = f"$$\n{math_content}\n$$"
            elif data['type'] == 'table':
                # Decide simple vs complex table conversion
                # For now, preserve as fenced LaTeX block
                data['processed'] = f"```latex\n{data['original']}\n```"
            elif data['type'] == 'algorithm':
                data['processed'] = f"```latex\n{data['original']}\n```"
            elif data['type'] == 'tikz':
                data['processed'] = f"```latex\n{data['original']}\n```"
            elif data['type'] == 'comment':
                # Convert to blockquote with LaTeX-to-Markdown conversions
                comment_text = data['content'].strip()

                # First, convert all section commands (starred and unstarred)
                comment_text = re.sub(r'\\section\*?\{(.+?)\}', r'## \1', comment_text)
                comment_text = re.sub(r'\\subsection\*?\{(.+?)\}', r'### \1', comment_text)
                comment_text = re.sub(r'\\subsubsection\*?\{(.+?)\}', r'#### \1', comment_text)
                comment_text = re.sub(r'\\paragraph\*?\{(.+?)\}', r'**\1**', comment_text)

                # Convert algorithm environments to fenced latex blocks
                comment_text = re.sub(r'\\begin\{algorithm\}(.*?)\\end\{algorithm\}',
                                     lambda m: f"\n```latex\n{m.group(0)}\n```\n", comment_text, flags=re.DOTALL)

                # Convert table environments to fenced latex blocks
                comment_text = re.sub(r'\\begin\{table\}(.*?)\\end\{table\}',
                                     lambda m: f"\n```latex\n{m.group(0)}\n```\n", comment_text, flags=re.DOTALL)

                # Apply inline formatting conversions
                comment_text = self.convert_inline_formatting(comment_text)
                # Convert LaTeX lists to Markdown
                comment_text = self.convert_lists(comment_text)
                # Convert inline math \(...\) to $...$
                comment_text = re.sub(r'\\\(([^)]+)\\\)', r'$\1$', comment_text)
                # Handle \texorpdfstring
                comment_text = re.sub(r'\\texorpdfstring\{([^}]+)\}\{[^}]+\}', r'\1', comment_text)

                lines = comment_text.split('\n')
                blockquote = ["", "> **COMMENTED SECTION:**", ">"]
                for line in lines:
                    blockquote.append(f"> {line}")
                blockquote.append("")
                data['processed'] = '\n'.join(blockquote)
            else:
                # Fallback: keep original
                data['processed'] = data['original']

    def _restore_blocks(self, content: str) -> str:
        """Replace tokens with processed block content."""
        for token, data in self.token_map.items():
            if 'processed' in data:
                content = content.replace(token, data['processed'])
        return content

    def _extract_code_listings(self, content: str) -> str:
        """Extract lstlisting and verbatim environments."""
        # lstlisting with optional options - FIXED: proper regex escaping
        pattern = r'\\begin\{lstlisting\}(?:\[(.*?)\])?(.*?)\\end\{lstlisting\}'
        def replace(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'code',
                'original': match.group(0),
                'options': match.group(1) if match.group(1) else '',
                'code': match.group(2)
            }
            return token
        content = re.sub(pattern, replace, content, flags=re.DOTALL)
        # verbatim environment - FIXED: proper regex escaping
        pattern = r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}'
        def replace_verb(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'code',
                'original': match.group(0),
                'code': match.group(1)
            }
            return token
        content = re.sub(pattern, replace_verb, content, flags=re.DOTALL)
        return content

    def _extract_display_math(self, content: str) -> str:
        """Extract display math environments: $$...$$, \\[...\\], and equation/align/etc."""
        # First, extract raw $$...$$ display math (must be before environments to avoid conflicts)
        pattern = r'\$\$(.*?)\$\$'
        def replace_dollar(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'display_math',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace_dollar, content, flags=re.DOTALL)

        # Square bracket display math \\[ ... \\] - FIXED: proper escaping
        pattern = r'\\\[(.*?)\\\]'
        def replace_sb(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'display_math',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace_sb, content, flags=re.DOTALL)

        # Math environments: equation, align, align*, cases, gather, multline
        math_envs = ['equation', 'align', 'align\\*', 'cases', 'gather', 'multline']
        for env in math_envs:
            pattern = r'\\begin\{' + env + r'\}(.*?)\\end\{' + env + r'\}'
            def replace(match, env=env):
                token = self._make_token()
                self.token_map[token] = {
                    'type': 'display_math',
                    'original': match.group(0),
                    'content': match.group(1)
                }
                return token
            content = re.sub(pattern, replace, content, flags=re.DOTALL)

        return content

    def _extract_tables(self, content: str) -> str:
        """Extract table and longtable environments."""
        # table environment - FIXED: proper regex escaping
        pattern = r'\\begin\{table\}(.*?)\\end\{table\}'
        def replace(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'table',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace, content, flags=re.DOTALL)
        # longtable environment - FIXED: proper regex escaping
        pattern = r'\\begin\{longtable\}(.*?)\\end\{longtable\}'
        def replace_long(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'table',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace_long, content, flags=re.DOTALL)
        return content

    def _extract_algorithms_tikz(self, content: str) -> str:
        """Extract algorithm and tikzpicture environments."""
        # algorithm environment - FIXED: proper regex escaping
        pattern = r'\\begin\{algorithm\}(.*?)\\end\{algorithm\}'
        def replace(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'algorithm',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace, content, flags=re.DOTALL)
        # tikzpicture environment - FIXED: proper regex escaping
        pattern = r'\\begin\{tikzpicture\}(.*?)\\end\{tikzpicture\}'
        def replace_tikz(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'tikz',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace_tikz, content, flags=re.DOTALL)
        return content

    def _extract_comments(self, content: str) -> str:
        """Extract comment and authcommentenv environments."""
        # comment environment - FIXED: proper regex escaping
        pattern = r'\\begin\{comment\}(.*?)\\end\{comment\}'
        def replace(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'comment',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace, content, flags=re.DOTALL)
        # authcommentenv environment - FIXED: proper regex escaping
        pattern = r'\\begin\{authcommentenv\}(.*?)\\end\{authcommentenv\}'
        def replace_auth(match):
            token = self._make_token()
            self.token_map[token] = {
                'type': 'comment',
                'original': match.group(0),
                'content': match.group(1)
            }
            return token
        content = re.sub(pattern, replace_auth, content, flags=re.DOTALL)
        # authcomment macro (inline) - we'll keep as is for now
        return content

    def convert_sections(self, content: str) -> str:
        """Convert LaTeX section commands to Markdown headings."""
        # \section and \section* -> ##
        content = re.sub(r'\\section\*?\{(.+?)\}', r'## \1', content)
        # \subsection and \subsection* -> ###
        content = re.sub(r'\\subsection\*?\{(.+?)\}', r'### \1', content)
        # \subsubsection and \subsubsection* -> ####
        content = re.sub(r'\\subsubsection\*?\{(.+?)\}', r'#### \1', content)
        # \paragraph -> **bold**
        content = re.sub(r'\\paragraph\{(.+?)\}', r'**\1**', content)

        return content

    def convert_inline_formatting(self, content: str) -> str:
        """Convert inline formatting commands."""
        # \textbf{} -> **...**
        content = re.sub(r'\\textbf\{(.+?)\}', r'**\1**', content)
        # \emph{} -> *...*
        content = re.sub(r'\\emph\{(.+?)\}', r'*\1*', content)
        # \textit{} -> *...*
        content = re.sub(r'\\textit\{(.+?)\}', r'*\1*', content)
        # \texttt{} -> `...`
        content = re.sub(r'\\texttt\{(.+?)\}', r'`\1`', content)
        # \textcolor{color}{text} -> text (preserve text, ignore color for markdown)
        content = re.sub(r'\\textcolor\{[^}]+\}\{(.+?)\}', r'\1', content)

        return content

    def convert_lists(self, content: str) -> str:
        """Convert LaTeX lists to Markdown, handling optional arguments and nested lists."""
        # Process nested lists from innermost to outermost
        max_iterations = 50  # Prevent infinite loops

        # Process itemize environments with optional arguments
        iteration = 0
        while r'\begin{itemize}' in content and iteration < max_iterations:
            prev_content = content
            # Pattern with optional arguments like [label=...]
            pattern = r'\\begin\{itemize\}(?:\[.*?\])?(.*?)\\end\{itemize\}'
            def replace_itemize(match):
                items_text = match.group(1)
                # Split by \item (with optional argument)
                items = re.split(r'\\item(?:\[.*?\])?\s+', items_text)
                md_items = []
                for item in items:
                    item = item.strip()
                    if item:
                        md_items.append(f"- {item}")
                return '\n'.join(md_items)
            content = re.sub(pattern, replace_itemize, content, flags=re.DOTALL)
            if content == prev_content:
                break
            iteration += 1

        # Process enumerate environments with optional arguments
        iteration = 0
        while r'\begin{enumerate}' in content and iteration < max_iterations:
            prev_content = content
            pattern = r'\\begin\{enumerate\}(?:\[.*?\])?(.*?)\\end\{enumerate\}'
            def replace_enumerate(match):
                items_text = match.group(1)
                items = re.split(r'\\item(?:\[.*?\])?\s+', items_text)
                md_items = []
                counter = 1
                for item in items:
                    item = item.strip()
                    if item:
                        md_items.append(f"{counter}. {item}")
                        counter += 1
                return '\n'.join(md_items)
            content = re.sub(pattern, replace_enumerate, content, flags=re.DOTALL)
            if content == prev_content:
                break
            iteration += 1

        # Process description environments with optional arguments
        iteration = 0
        while r'\begin{description}' in content and iteration < max_iterations:
            prev_content = content
            pattern = r'\\begin\{description\}(?:\[.*?\])?(.*?)\\end\{description\}'
            def replace_description(match):
                items_text = match.group(1)
                # Split by \item but keep label
                items = re.findall(r'\\item(?:\[([^\]]*)\])?\s*(.*?)(?=\\item|$)', items_text, flags=re.DOTALL)
                md_items = []
                for i, (label, body) in enumerate(items):
                    body = body.strip()
                    if label:
                        md_items.append(f"**{label}** {body}")
                    else:
                        md_items.append(f"- {body}")
                return '\n'.join(md_items)
            content = re.sub(pattern, replace_description, content, flags=re.DOTALL)
            if content == prev_content:
                break
            iteration += 1

        return content

    def convert_math(self, content: str) -> str:
        """Preserve math expressions - inline with $ and display with $$."""
        # Display math environments - preserve the LaTeX inside
        # equation, align, cases, etc.
        math_envs = ['equation', 'align', 'align\\*', 'cases', 'gather', 'multline']

        for env in math_envs:
            pattern = r'\\begin\{' + env + r'\}(.*?)\\end\{' + env + r'\}'
            content = re.sub(pattern, lambda m: f"$$\n{m.group(1).strip()}\n$$",
                           content, flags=re.DOTALL)

        # Square bracket display math \[ ... \] -> $$ ... $$
        content = re.sub(r'\\\[(.*?)\\\]', r'$$\n\1\n$$', content, flags=re.DOTALL)

        # Inline math is already in $ ... $ format, so we keep it as is
        # Just need to handle \( ... \) -> $ ... $
        content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)

        # Handle \texorpdfstring{A}{B} -> keep A
        content = re.sub(r'\\texorpdfstring\{([^}]+)\}\{[^}]+\}', r'\1', content)

        return content

    def convert_code_listings(self, content: str) -> str:
        """Convert lstlisting and verbatim to fenced code blocks."""
        def replace_listing(match):
            options = match.group(1) if match.group(1) else ''
            code = match.group(2)

            # Extract language from options
            lang_match = re.search(r'language=(\w+)', options)
            lang = lang_match.group(1).lower() if lang_match else ''

            # Extract caption and label
            caption_match = re.search(r'caption=\{(.+?)\}', options, re.DOTALL)
            label_match = re.search(r'label=\{(.+?)\}', options, re.DOTALL)

            result = []
            if caption_match:
                result.append(f"**Caption:** {caption_match.group(1)}")
            if label_match:
                result.append(f"**Label:** {label_match.group(1)}")

            result.append(f"```{lang}")
            result.append(code.strip())
            result.append("```")

            return '\n'.join(result)

        # lstlisting with options
        content = re.sub(r'\\begin\{lstlisting\}\[(.*?)\](.*?)\\end\{lstlisting\}',
                        replace_listing, content, flags=re.DOTALL)

        # lstlisting without options
        def replace_simple_listing(match):
            code = match.group(1)
            return f"```\n{code.strip()}\n```"

        content = re.sub(r'\\begin\{lstlisting\}(.*?)\\end\{lstlisting\}',
                        replace_simple_listing, content, flags=re.DOTALL)

        # verbatim environment
        content = re.sub(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',
                        lambda m: f"```\n{m.group(1).strip()}\n```",
                        content, flags=re.DOTALL)

        return content

    def convert_tables(self, content: str) -> str:
        """Convert LaTeX tables to Markdown tables - with safe fallback to fenced LaTeX."""
        def is_simple_table(tabular_content: str) -> bool:
            """Check if table can be safely converted to Markdown."""
            # Complex indicators that should trigger fallback:
            # - @{} column specs
            # - p{} column specs
            # - \\thead{...} with line breaks
            # - \\multicolumn
            # - \\endfirsthead, \\endhead, etc. (longtable headers)
            if '@{' in tabular_content:
                return False
            if re.search(r'p\{[^}]+\}', tabular_content):
                return False
            if '\\thead{' in tabular_content:
                return False
            if '\\multicolumn{' in tabular_content:
                return False
            if '\\endfirsthead' in tabular_content or '\\endhead' in tabular_content:
                return False
            return True

        def extract_table_content(match):
            full_table = match.group(0)

            # Extract caption and label
            caption_match = re.search(r'\\caption\{(.+?)\}', full_table, re.DOTALL)
            label_match = re.search(r'\\label\{(.+?)\}', full_table)

            # Extract tabular content - match column spec more carefully
            tabular_match = re.search(r'\\begin\{tabular\}(?:\[[^\]]*\])?\{([^}]+)\}(.*?)\\end\{tabular\}',
                                     full_table, flags=re.DOTALL)
            if not tabular_match:
                return f"```latex\n{full_table}\n```"

            col_spec = tabular_match.group(1)
            tabular_content = tabular_match.group(2)

            # Check if simple enough to convert
            if not is_simple_table(tabular_content):
                return f"```latex\n{full_table}\n```"

            # Process table rows
            # Remove \toprule, \midrule, \bottomrule, \hline
            tabular_content = re.sub(r'\\toprule|\\midrule|\\bottomrule|\\hline', '', tabular_content)

            # Split into rows (split by \\)
            rows = [r.strip() for r in tabular_content.split(r'\\') if r.strip()]

            # Process each row
            md_rows = []
            for i, row in enumerate(rows):
                # Remove \thead{} wrappers - handle nested braces
                while r'\thead{' in row:
                    row = re.sub(r'\\thead\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', r'\1', row)

                # Remove \makecell{} wrappers
                while r'\makecell{' in row:
                    row = re.sub(r'\\makecell\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', r'\1', row)

                # Replace & with |
                cells = [cell.strip() for cell in row.split('&')]

                # Clean cells - remove extra LaTeX commands
                cells = [re.sub(r'\\text\{([^}]+)\}', r'\1', cell) for cell in cells]

                md_row = '| ' + ' | '.join(cells) + ' |'
                md_rows.append(md_row)

                # Add header separator after first row
                if i == 0:
                    separator = '| ' + ' | '.join(['---'] * len(cells)) + ' |'
                    md_rows.append(separator)

            # Build result
            result = []
            if caption_match:
                result.append(f"**Table:** {caption_match.group(1)}")
            if label_match:
                result.append(f"**Label:** {label_match.group(1)}")
            result.append('')
            result.extend(md_rows)
            result.append('')

            return '\n'.join(result)

        # Convert table environments
        content = re.sub(r'\\begin\{table\}.*?\\end\{table\}',
                        extract_table_content, content, flags=re.DOTALL)

        # Convert longtable environments similarly
        def extract_longtable_content(match):
            full_table = match.group(0)

            # Extract caption and label
            caption_match = re.search(r'\\caption\{(.+?)\}', full_table, re.DOTALL)
            label_match = re.search(r'\\label\{(.+?)\}', full_table)

            # Remove longtable header markers
            content = re.sub(r'\\endfirsthead|\\endhead|\\endfoot|\\endlastfoot', '', full_table)

            # Extract rows between \begin{longtable} and \end{longtable}
            longtable_match = re.search(r'\\begin\{longtable\}\{[^}]+\}(.*?)\\end\{longtable\}',
                                       full_table, flags=re.DOTALL)
            if not longtable_match:
                return f"```latex\n{full_table}\n```"

            table_content = longtable_match.group(1)

            # Check if simple enough to convert
            if not is_simple_table(table_content):
                return f"```latex\n{full_table}\n```"

            # Remove decorative rules
            table_content = re.sub(r'\\toprule|\\midrule|\\bottomrule|\\hline', '', table_content)

            # Split into rows
            rows = [r.strip() for r in table_content.split(r'\\') if r.strip() and not re.match(r'\\(caption|label)', r)]

            # Process rows
            md_rows = []
            for i, row in enumerate(rows):
                row = re.sub(r'\\thead\{([^}]+)\}', r'\1', row)
                row = re.sub(r'\\makecell\{([^}]+)\}', r'\1', row)
                cells = [cell.strip() for cell in row.split('&')]
                md_row = '| ' + ' | '.join(cells) + ' |'
                md_rows.append(md_row)

                if i == 0:
                    separator = '| ' + ' | '.join(['---'] * len(cells)) + ' |'
                    md_rows.append(separator)

            result = []
            if caption_match:
                result.append(f"**Table:** {caption_match.group(1)}")
            if label_match:
                result.append(f"**Label:** {label_match.group(1)}")
            result.append('')
            result.extend(md_rows)
            result.append('')

            return '\n'.join(result)

        content = re.sub(r'\\begin\{longtable\}.*?\\end\{longtable\}',
                        extract_longtable_content, content, flags=re.DOTALL)

        return content

    def convert_algorithms(self, content: str) -> str:
        """Preserve algorithm and TikZ environments as LaTeX code blocks."""
        def preserve_algorithm(match):
            alg_content = match.group(1)

            # Extract caption if present
            caption_match = re.search(r'\\caption\{(.+?)\}', alg_content, re.DOTALL)
            label_match = re.search(r'\\label\{(.+?)\}', alg_content)

            result = []
            if caption_match:
                result.append(f"**Algorithm:** {caption_match.group(1)}")
            if label_match:
                result.append(f"**Label:** {label_match.group(1)}")
            result.append('')
            result.append("```latex")
            result.append(match.group(0))
            result.append("```")

            return '\n'.join(result)

        # Preserve algorithm environments
        content = re.sub(r'\\begin\{algorithm\}(.*?)\\end\{algorithm\}',
                        preserve_algorithm, content, flags=re.DOTALL)

        # Preserve TikZ pictures
        def preserve_tikz(match):
            result = ["```latex", match.group(0), "```"]
            return '\n'.join(result)

        content = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
                        preserve_tikz, content, flags=re.DOTALL)

        # Preserve figure environments containing TikZ
        content = re.sub(r'\\begin\{figure\}.*?\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}.*?\\end\{figure\}',
                        preserve_tikz, content, flags=re.DOTALL)

        return content

    def convert_comments(self, content: str) -> str:
        """Convert comment blocks to visible Markdown blockquotes."""
        # Convert \begin{comment}...\end{comment} to blockquote
        def replace_comment(match):
            comment_text = match.group(1).strip()
            # Convert to blockquote with clear marker
            lines = comment_text.split('\n')
            blockquote = ["", "> **COMMENTED SECTION:**", ">"]
            for line in lines:
                blockquote.append(f"> {line}")
            blockquote.append("")
            return '\n'.join(blockquote)

        content = re.sub(r'\\begin\{comment\}(.*?)\\end\{comment\}',
                        replace_comment, content, flags=re.DOTALL)

        # Convert \authcomment{} to visible blocks
        def replace_authcomment(match):
            comment_text = match.group(1)
            return f"\n> **AUTHOR COMMENT:** {comment_text}\n"

        content = re.sub(r'\\authcomment\{(.+?)\}', replace_authcomment, content)

        # Convert authcommentenv environment
        def replace_authcommentenv(match):
            comment_text = match.group(1).strip()
            lines = comment_text.split('\n')
            result = ["", "> **AUTHOR COMMENT:**", ">"]
            for line in lines:
                result.append(f"> {line}")
            result.append("")
            return '\n'.join(result)

        content = re.sub(r'\\begin\{authcommentenv\}(.*?)\\end\{authcommentenv\}',
                        replace_authcommentenv, content, flags=re.DOTALL)

        return content

    def convert_links(self, content: str) -> str:
        """Convert LaTeX hyperlinks to Markdown."""
        # \url{...} -> <...>
        content = re.sub(r'\\url\{([^}]+)\}', r'<\1>', content)

        # \href{url}{text} -> [text](url)
        content = re.sub(r'\\href\{([^}]+)\}\{([^}]+)\}', r'[\2](\1)', content)

        return content

    def convert_bibliography(self, content: str) -> str:
        """Convert thebibliography environment to Markdown reference list."""
        def replace_bibliography(match):
            bib_content = match.group(1)

            # Extract bibitem entries
            items = re.findall(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem|$)',
                             bib_content, flags=re.DOTALL)

            result = ["## References", ""]
            for label, text in items:
                text = text.strip()
                # Clean up the text
                text = re.sub(r'\\url\{([^}]+)\}', r'[\1](\1)', text)
                result.append(f"**[{label}]** {text}")
                result.append("")

            return '\n'.join(result)

        content = re.sub(r'\\begin\{thebibliography\}\{[^}]+\}(.*?)\\end\{thebibliography\}',
                        replace_bibliography, content, flags=re.DOTALL)

        return content

    def clean_latex_commands(self, content: str) -> str:
        """Remove or convert remaining LaTeX commands."""
        # Remove \maketitle (leftover from preamble removal)
        content = re.sub(r'\\maketitle', '', content)

        # Remove labels (they're already extracted in tables/figures)
        content = re.sub(r'\\label\{[^}]+\}', '', content)

        # Remove \noopname
        content = re.sub(r'\\noopname\s*', '', content)

        # Remove \indent
        content = re.sub(r'\\indent\s*', '', content)

        # Remove \vspace and \hspace
        content = re.sub(r'\\[hv]space\*?\{[^}]+\}', '', content)

        # Remove FloatBarrier
        content = re.sub(r'\\FloatBarrier', '', content)

        # Clean up multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Clean up spaces before punctuation
        content = re.sub(r'\s+([.,;:!?])', r'\1', content)

        return content

    def generate_frontmatter(self) -> str:
        """Generate YAML frontmatter from metadata."""
        if not self.metadata:
            return ""

        frontmatter = ["---"]
        if 'title' in self.metadata and self.metadata['title']:
            title = self.metadata['title']
            # Escape special YAML characters if needed
            if ':' in title or '"' in title:
                title = f'"{title}"'
            frontmatter.append(f"title: {title}")
        if 'author' in self.metadata and self.metadata['author']:
            author = self.metadata['author']
            if ':' in author or '"' in author:
                author = f'"{author}"'
            frontmatter.append(f"author: {author}")
        if 'date' in self.metadata and self.metadata['date']:
            date = self.metadata['date']
            if ':' in date or '"' in date:
                date = f'"{date}"'
            frontmatter.append(f"date: {date}")
        frontmatter.append("---")
        frontmatter.append("")

        # Add title as H1
        if 'title' in self.metadata and self.metadata['title']:
            frontmatter.append(f"# {self.metadata['title']}")
            frontmatter.append("")
        if 'author' in self.metadata and self.metadata['author']:
            frontmatter.append(f"**Author:** {self.metadata['author']}")
        if 'date' in self.metadata and self.metadata['date']:
            frontmatter.append(f"**Date:** {self.metadata['date']}")
        frontmatter.append("")

        return '\n'.join(frontmatter)

    def convert_authcomment(self, content: str) -> str:
        """Convert \\authcomment{...} inline macros to blockquote format."""
        # Convert authcomment to visible blockquote format
        def replace_authcomment(match):
            comment_text = match.group(1).strip()
            return f"\n> **AUTHOR COMMENT:** {comment_text}\n"
        content = re.sub(r'\\authcomment\{(.+?)\}', replace_authcomment, content, flags=re.DOTALL)
        return content

    def convert(self):
        """Main conversion pipeline."""
        print(f"Converting {self.input_file} to {self.output_file}...")

        # Read file
        content = self.read_file()

        # Extract metadata and remove preamble
        content = self.extract_metadata(content)

        # Reset token storage
        self.token_map = {}
        self.token_counter = 0

        # Convert authcomment inline macros first (before block extraction)
        content = self.convert_authcomment(content)

        # Extract special blocks and replace with tokens
        content = self._extract_and_replace_blocks(content)

        # Process blocks (convert to Markdown representations)
        self._process_blocks()

        # Apply text conversions to tokenized content
        content = self.convert_sections(content)  # Convert headings (including starred)
        content = self.convert_lists(content)  # Convert lists
        content = self.convert_inline_formatting(content)  # Convert formatting
        # Convert inline math: \(...\) -> $...$
        content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)
        content = self.convert_links(content)  # Convert hyperlinks
        content = self.convert_bibliography(content)  # Convert bibliography
        content = self.clean_latex_commands(content)  # Clean up remaining LaTeX (safe)

        # Restore processed blocks
        content = self._restore_blocks(content)

        # Generate frontmatter
        frontmatter = self.generate_frontmatter()

        # Combine and write
        final_content = frontmatter + content

        # Write output
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"✓ Conversion complete: {self.output_file}")


def main():
    """Convert all three instruction files."""
    base_dir = Path("<home>/Desktop/cursor/pinn_instruction")
    output_dir = base_dir / "markdown_conversions"

    files_to_convert = [
        ("CTL-instruction-final.tex", "CTL-instruction-final.md"),
        ("sampling_method_instruction.tex", "sampling_method_instruction.md"),
        ("PINN_architecture_plan.tex", "PINN_architecture_plan.md")
    ]

    for input_file, output_file in files_to_convert:
        input_path = base_dir / input_file
        output_path = output_dir / output_file

        if not input_path.exists():
            print(f"⚠ Warning: {input_path} not found, skipping...")
            continue

        converter = LaTeXToMarkdownConverter(str(input_path), str(output_path))
        converter.convert()

    print("\n✓ All conversions complete!")


if __name__ == "__main__":
    main()
