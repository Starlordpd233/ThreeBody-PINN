#!/usr/bin/env python3
"""
convert_latex_to_md.py

Converts 6 LaTeX source files to Markdown using pandoc v3.7.0.2.
Pre-processes custom macros, replaces unconvertible elements (TikZ, algorithms),
runs pandoc, then post-processes output for clean rendering.

Usage:
    python convert_latex_to_md.py
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PANDOC = "/opt/homebrew/bin/pandoc"
SOURCE_DIR = Path("<home>/Desktop/3_body_problem/pinn_instruction/original_latex")
TARGET_DIR = Path("<home>/Desktop/3_body_problem/pinn_instruction/instructions/pandoc_conversion")

FILE_MAP = [
    {
        "source": "ctl-instruction/CTL-instruction-final.tex",
        "target": "CTL-instruction-final.md",
    },
    {
        "source": "pinn-architecture/PINN_architecture_plan.tex",
        "target": "PINN_architecture_plan.md",
    },
    {
        "source": "review-of-framework/review_of_ctl-pinn_framework.tex",
        "target": "review_of_ctl-pinn_framework.md",
    },
    {
        "source": "review-of-framework/stage-strat-revision.tex",
        "target": "stage-strat-revision.md",
    },
    {
        "source": "sampling-method/sampling_method_instruction.tex",
        "target": "sampling_method_instruction.md",
    },
    {
        "source": "trainingData-quality-assessment/data_quality_assess.tex",
        "target": "data_quality_assess.md",
    },
]

# ---------------------------------------------------------------------------
# TikZ diagram text replacements
# ---------------------------------------------------------------------------

TIKZ_FIGURE_REPLACEMENTS = {
    "fig:step2_data_workflow": r"""\begin{quote}
\textbf{Figure: COM Frame Verification and Input Construction Workflow}

\begin{enumerate}
\item \textbf{Sampled ICs} (start)
\item Decision: \textbf{COM Frame?}
  \begin{itemize}
  \item No $\rightarrow$ \textbf{Transform to COM}
  \item Yes $\rightarrow$ \textbf{Verify $\sum m_i v_i = 0$}
  \end{itemize}
\item Both paths converge to: \textbf{Compute Physics Invariants}
\item \textbf{Build 14D PINN Input}
\end{enumerate}

\emph{Workflow diagram for COM-frame verification and input construction (Step~2 Preprocessing).}
\end{quote}""",

    "fig:step2to5_workflow": r"""\begin{quote}
\textbf{Figure: End-to-End Data Processing Flow (Steps 2--5)}

\begin{enumerate}
\item \textbf{Step 2: Preprocessing} $\rightarrow$ produces Scaled ICs
\item \textbf{Step 3: Invariant Calculation} $\rightarrow$ stores invariants ($E, Q, s_{\min}, L_{\text{norm}}, I_{\text{norm}}, \tau_L$)
\item Parallel branches (both using stored invariants):
  \begin{itemize}
  \item \textbf{Step 4: Input Vector Construction} $\rightarrow$ \textbf{Compute additional features} (reuses invariants)
  \item \textbf{Step 5: Stage Assignment}
  \end{itemize}
\end{enumerate}

\emph{Steps~4 and~5 run in parallel after Step~3 computes and stores invariants.}
\end{quote}""",
}

# ---------------------------------------------------------------------------
# Algorithm environment replacement
# ---------------------------------------------------------------------------

ALGORITHM_REPLACEMENT = r"""\begin{quote}
\textbf{Algorithm 1: Adaptive Median Gradient Clipping} ($H=100$, $C=5$, $\varepsilon=10^{-6}$)

\textbf{Require:} Model parameters $\theta$; history deque $\mathcal{H}$ with capacity $H$.

\begin{enumerate}
\item $g \leftarrow \lVert \nabla_\theta \mathcal{L} \rVert_2$ \quad (Current global gradient norm)
\item Push $g$ into $\mathcal{H}$, pop oldest if $|\mathcal{H}| > H$
\item $\tilde{g} \leftarrow \operatorname{median}(\mathcal{H})$
\item $t \leftarrow C\,\tilde{g}$ \quad (Dynamic threshold)
\item \textbf{If} $g > t$: \quad (Only rescale when necessary)
  \begin{enumerate}
  \item $\alpha \leftarrow \dfrac{t}{g + \varepsilon}$
  \item \textbf{For all} $p \in \theta$ with $p.\text{grad} \neq \text{None}$: \; $p.\text{grad} \gets \alpha\, p.\text{grad}$
  \end{enumerate}
\end{enumerate}
\end{quote}"""

# ---------------------------------------------------------------------------
# Utility: brace-depth-aware content extractor
# ---------------------------------------------------------------------------

def extract_braced_content(text: str, start: int):
    """Return (content, end_pos) for the brace-group starting at `start`.

    `start` must point to the opening `{`. Handles `\\` escape sequences
    so escaped braces do not affect depth.
    """
    assert text[start] == "{", f"Expected '{{' at pos {start}, got {text[start]!r}"
    depth = 1
    i = start + 1
    while i < len(text) and depth > 0:
        ch = text[i]
        if ch == "\\":
            i += 2  # skip escaped character (e.g. \{ or \\)
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        i += 1
    return text[start + 1 : i - 1], i


def replace_macro(text: str, macro_re: str, replacement_fn) -> str:
    """Replace all occurrences of `\\macro{...}` using brace-depth matching.

    `macro_re` is a regex that matches up to and including the opening `{`
    (the opening brace is consumed and handled here, so it must NOT be in macro_re).
    `replacement_fn(content) -> str` receives the inner content and returns the
    replacement string.
    """
    pattern = re.compile(macro_re + r"\{")
    result = []
    pos = 0
    while pos < len(text):
        m = pattern.search(text, pos)
        if not m:
            result.append(text[pos:])
            break
        result.append(text[pos : m.start()])
        brace_start = m.end() - 1  # position of opening {
        content, end_pos = extract_braced_content(text, brace_start)
        result.append(replacement_fn(content))
        pos = end_pos
    return "".join(result)


# ---------------------------------------------------------------------------
# Pre-processing steps
# ---------------------------------------------------------------------------

def strip_macro_definitions(text: str) -> str:
    """Remove macro/env definition lines that should not appear in output."""
    # Single-line patterns to remove entirely
    patterns = [
        r"^\\renewcommand\\theadfont\{\\bfseries\}[ \t]*$",
        r"^\\renewcommand\{\\arraystretch\}\{[^}]*\}[ \t]*$",
        r"^\\DeclareMathOperator\{\\median\}\{median\}[ \t]*$",
        r"^\\newcommand\{\\authcomment\}.*$",
        r"^\\newcommand\{\\vect\}\[1\]\{.*\}.*$",
        r"^\\newcommand\{\\norm\}\[1\]\{.*\}.*$",
        # Comment lines describing authcomment
        r"^%.*[Dd]efines.*authcomment.*$",
        r"^%.*[Uu]sage.*authcomment.*$",
        r"^%.*[Dd]efines.*environment.*$",
        r"^%.*[Uu]sage.*authcommentenv.*$",
        # authcommentenv multi-line environment definition
        r"^\\newenvironment\{authcommentenv\}.*$",
        r"^\s*\{\\par\\begingroup\\color\{Red\}.*$",
        r"^\s*\{]\\\}\\endgroup\\par\}.*$",
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.MULTILINE)
    return text


def expand_vect(text: str) -> str:
    """\\vect{x} -> \\mathbf{x}"""
    return replace_macro(text, r"\\vect", lambda c: f"\\mathbf{{{c}}}")


def expand_norm(text: str) -> str:
    """\\norm{x} -> \\|x\\|"""
    return replace_macro(text, r"\\norm", lambda c: f"\\|{c}\\|")


def expand_authcomment(text: str) -> str:
    """\\authcomment{text} -> \\textbf{[text]}"""
    return replace_macro(text, r"\\authcomment", lambda c: f"\\textbf{{[{c}]}}")


def expand_median(text: str) -> str:
    r"""\\median -> \\operatorname{median} (definition line already stripped)"""
    # Already stripped definition line; now replace uses
    return re.sub(r"\\median(?![a-zA-Z@])", r"\\operatorname{median}", text)


def expand_thead(text: str) -> str:
    """\\thead{text} -> text (replace internal \\\\ with space for table headers)"""
    def _replace(content: str) -> str:
        # \\ inside thead means line break within the cell header — replace with space
        content = content.replace("\\\\", " ")
        return content
    return replace_macro(text, r"\\thead", _replace)


def fix_double_backslash_commands(text: str) -> str:
    """Fix \\\\emph{ -> \\emph{ (typo in CTL file)."""
    text = text.replace("\\\\emph{", "\\emph{")
    text = text.replace("\\\\textbf{", "\\textbf{")
    text = text.replace("\\\\textit{", "\\textit{")
    return text


def replace_tikz_figures(text: str) -> str:
    """Replace \\begin{figure}...\\end{figure} blocks containing TikZ with text descriptions.

    Matches on \\label{label} (not \\ref{label}) to avoid false matches in captions.
    """
    for label, replacement in TIKZ_FIGURE_REPLACEMENTS.items():
        # Match \label{label} specifically to distinguish from \ref{label}
        pattern = re.compile(
            r"\\begin\{figure\}.*?\\label\{" + re.escape(label) + r"\}.*?\\end\{figure\}",
            re.DOTALL,
        )
        repl_literal = replacement
        text = pattern.sub(lambda m, r=repl_literal: r, text)
    return text


def replace_algorithm_env(text: str) -> str:
    """Replace \\begin{algorithm}...\\end{algorithm} with readable pseudocode."""
    pattern = re.compile(
        r"\\begin\{algorithm\}.*?\\end\{algorithm\}",
        re.DOTALL,
    )
    repl = ALGORITHM_REPLACEMENT
    return pattern.sub(lambda m, r=repl: r, text)


def preprocess(text: str) -> str:
    """Apply all pre-processing transformations in order."""
    text = strip_macro_definitions(text)
    text = expand_vect(text)
    text = expand_norm(text)
    text = expand_authcomment(text)
    text = expand_median(text)
    text = expand_thead(text)
    text = fix_double_backslash_commands(text)
    text = replace_tikz_figures(text)
    text = replace_algorithm_env(text)
    return text


# ---------------------------------------------------------------------------
# Post-processing steps
# ---------------------------------------------------------------------------

def clean_code_blocks(text: str) -> str:
    """Normalize pandoc code block attribute syntax to simple language tags."""
    # ``` {.python ...} -> ```python
    text = re.sub(r"``` \{\.(\w+)[^}]*\}", r"```\1", text)
    # ``` {language="Python" ...} -> ```python
    text = re.sub(r'``` \{[^}]*language="([Pp]ython)"[^}]*\}', "```python", text)
    # ``` {.python} (no extra attrs) -> ```python
    text = re.sub(r"``` \{\.(\w+)\}", r"```\1", text)
    # ``` {} -> ```
    text = re.sub(r"``` \{[^}]*\}", "```", text)
    return text


def infer_code_language(text: str) -> str:
    """Tag untagged code blocks that contain Python code."""
    PYTHON_SIGNALS = ("import ", "def ", "class ", "torch.", "np.", "pd.",
                      "return ", "for ", "if ", "elif ", "else:", "print(",
                      "    #", "self.")
    lines = text.split("\n")
    result = []
    i = 0
    while i < len(lines):
        if lines[i].rstrip() == "```":
            # Collect block content
            block_lines = []
            j = i + 1
            while j < len(lines) and lines[j].rstrip() != "```":
                block_lines.append(lines[j])
                j += 1
            block_text = "\n".join(block_lines)
            if any(sig in block_text for sig in PYTHON_SIGNALS):
                result.append("```python")
            else:
                result.append(lines[i])
        else:
            result.append(lines[i])
        i += 1
    return "\n".join(result)


def fix_escaped_brackets(text: str) -> str:
    """Fix \\[ and \\] that pandoc escapes inside bold text from authcomment expansion."""
    # **\[comment\]** -> **[comment]**
    text = re.sub(r"\*\*\\\[", "**[", text)
    text = re.sub(r"\\\]\*\*", "]**", text)
    # Also fix standalone escaped brackets that should be literal
    # Be careful not to touch math \[...\] — pandoc converts those to $$...$$
    # by the time we run, so remaining \[ is from text context
    return text


def clean_color_spans(text: str) -> str:
    """Remove HTML-style color span attributes that pandoc may emit."""
    text = re.sub(r'\{style="color:\s*[^"]+"\}', "", text)
    text = re.sub(r'\{color="[^"]+"\}', "", text)
    return text


def clean_fenced_divs(text: str) -> str:
    """Remove all pandoc fenced div markers (opening and closing :::)."""
    # Remove ALL lines starting with 3+ colons (opening :::{.class} and closing :::)
    text = re.sub(r"^:{3,}.*$", "", text, flags=re.MULTILINE)
    return text


def fix_math_artifacts(text: str) -> str:
    """Fix common pandoc math conversion artifacts."""
    # Remove \hfill that leaks into text outside math
    text = re.sub(r"\\hfill(?!\{)", " ", text)
    return text


def clean_leading_hrule(text: str) -> str:
    """Remove a leading horizontal rule that comes from \\hrule in the LaTeX preamble.

    A long dash line (---+) at the very start of a markdown file can be
    misinterpreted as YAML front matter by some renderers.
    """
    # Remove a thematic break (4+ dashes on its own line) at the very start of the file
    text = re.sub(r"^\-{4,}\s*\n+", "", text)
    return text


def clean_heading_anchors(text: str) -> str:
    """Remove pandoc heading anchor syntax {#id .class} that clutter headings.

    Standard markdown renderers render these as literal text in the heading.
    """
    # Remove { ... } suffixes from ATX headings like: # Title {#id .unnumbered}
    text = re.sub(r"(#{1,6} .+?) \{[^}]+\}\s*$", r"\1", text, flags=re.MULTILINE)
    return text


def collapse_blank_lines(text: str) -> str:
    """Reduce runs of 4+ blank lines to 3 max."""
    return re.sub(r"\n{4,}", "\n\n\n", text)


def postprocess(text: str) -> str:
    """Apply all post-processing transformations in order."""
    text = clean_leading_hrule(text)
    text = clean_heading_anchors(text)
    text = clean_code_blocks(text)
    text = infer_code_language(text)
    text = fix_escaped_brackets(text)
    text = clean_color_spans(text)
    text = clean_fenced_divs(text)
    text = fix_math_artifacts(text)
    text = collapse_blank_lines(text)
    return text


# ---------------------------------------------------------------------------
# Pandoc conversion
# ---------------------------------------------------------------------------

def run_pandoc(input_path: Path, output_path: Path) -> tuple[bool, str]:
    """Run pandoc and return (success, stderr)."""
    cmd = [
        PANDOC,
        "-f", "latex",
        "-t", "markdown",
        "--wrap=none",
        "--markdown-headings=atx",
        str(input_path),
        "-o", str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stderr.strip()


# ---------------------------------------------------------------------------
# Main conversion pipeline
# ---------------------------------------------------------------------------

def convert_file(source_path: Path, target_path: Path) -> tuple[bool, str]:
    """Convert a single .tex file to .md. Returns (success, message)."""
    # 1. Read source
    try:
        tex_content = source_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Read error: {e}"

    # 2. Pre-process
    preprocessed = preprocess(tex_content)

    # 3. Write temp .tex, run pandoc, read output
    tmp_in = None
    tmp_out = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write(preprocessed)
            tmp_in = Path(f.name)

        tmp_out = tmp_in.with_suffix(".md")

        success, stderr = run_pandoc(tmp_in, tmp_out)
        if not success:
            return False, f"Pandoc failed: {stderr}"
        if stderr:
            print(f"    pandoc warnings: {stderr[:200]}")

        md_content = tmp_out.read_text(encoding="utf-8")

    finally:
        if tmp_in and tmp_in.exists():
            tmp_in.unlink()
        if tmp_out and tmp_out.exists():
            tmp_out.unlink()

    # 4. Post-process
    final_content = postprocess(md_content)

    # 5. Write output
    try:
        target_path.write_text(final_content, encoding="utf-8")
    except Exception as e:
        return False, f"Write error: {e}"

    lines = len(final_content.splitlines())
    size = len(final_content.encode("utf-8"))
    return True, f"{lines} lines, {size:,} bytes"


def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for file_info in FILE_MAP:
        source = SOURCE_DIR / file_info["source"]
        target = TARGET_DIR / file_info["target"]
        print(f"Converting: {file_info['source']}")

        if not source.exists():
            msg = "SOURCE NOT FOUND"
            print(f"  ERROR: {source}")
            results.append((file_info["source"], "MISSING", msg))
            continue

        success, msg = convert_file(source, target)
        status = "OK" if success else "FAILED"
        print(f"  -> {target.name} [{status}] {msg}")
        results.append((file_info["source"], status, msg))

    # Summary
    print("\n" + "=" * 70)
    print("Conversion Summary")
    print("=" * 70)
    for source, status, msg in results:
        name = Path(source).name
        print(f"  {status:6s}  {name:45s}  {msg}")

    ok = sum(1 for _, s, _ in results if s == "OK")
    total = len(results)
    print(f"\n{ok}/{total} files converted successfully.")

    if ok < total:
        print("\nFailed files:")
        for source, status, msg in results:
            if status != "OK":
                print(f"  {source}: {msg}")


if __name__ == "__main__":
    main()
