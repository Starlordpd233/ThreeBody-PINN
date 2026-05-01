# Feature Landscape: Stack Additions for Markdown Verification

**Domain:** LaTeX-to-Markdown conversion verification -- stack additions needed
**Researched:** 2026-04-30

## Table Stakes for Verification Tooling

Features the verification scripts must provide. Missing = verification is incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Section-by-section line diff (LaTeX vs MD) | Modular LaTeX sources split into `sections/`; verification must compare section-to-section | Low | `difflib.unified_diff()` on per-section text blocks. Stdlib, zero dependencies. |
| Math formula extraction (both LaTeX and MD) | Formulas are the highest-value content; every `$...$`, `$$...$$`, `\[...\]` block must be extracted and compared | Medium | State-machine parser (not regex alone) for nested math. Fallback: pylatexenc latexwalker for complex LaTeX. |
| Cross-reference extraction (`\ref`, `\cite`, `\label`) | References must be preserved in markdown; verification confirms they appear in the right sections | Low | Regex on `\ref{...}`, `\cite{...}`, `\label{...}`. Compare reference IDs, not formatting. |
| Commented-out content detection | `\begin{comment}...\end{comment}` blocks intentionally excluded from markdown; must not flag as missing | Low | Strip comment blocks from LaTeX before comparison; verify zero comment content in markdown |
| Candidate selection (multiple .md files) | 4 of 6 documents have 2-3 competing markdown files; must pick best starting point | Low | Score each candidate by diff count against source; pick lowest |

## Differentiators for Quality Verification

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Normalized math comparison (whitespace-insensitive, delimiter-agnostic) | Prevents false positives when `$x^2$` vs `$ x^2 $` or `$$...$$` vs `\[...\]` | Low | Canonicalize: strip delimiters, collapse whitespace, normalize `\[` -> `$$` |
| Discrepancy categorization (math vs text vs structure vs ref) | Makes fix prioritization clear; math errors critical, formatting cosmetic | Low | Tag each diff block by type; generate categorized summary report |
| Re-diff confirmation (fix -> re-diff -> confirm zero diffs) | Prevents regressions and incomplete fixes | Low | After each fix round, re-run script. Phase done only when diff is empty. |
| Shared utility module (`md_verification_utils.py`) | Avoids copy-pasting extraction/diff logic across 6 phase scripts | Low | Single importable module with `split_sections()`, `extract_math()`, `normalize_math()`, `diff_sections()` |

## What NOT to Build Into Verification

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| SymPy-based math equivalence checking | Can't handle physics notation (vectors, norms, bra-ket, multi-letter variables). Wrong tool for text-comparison. | Text-level comparison of formula source strings |
| Visual rendering comparison (MathJax/KaTeX in headless browser) | Massive complexity (puppeteer, JS runtime), non-deterministic. Formulas can render identically despite source differences. | Compare source text directly |
| AI/LLM-based discrepancy detection | Non-deterministic, may hallucinate fixes, adds latency and cost. The task is mechanical. | Deterministic `difflib` comparison |
| Auto-fixing discrepancies | A script might "fix" math by deleting it. All fixes must be human-reviewed. | Flag discrepancies; human fixes each one |
| Pandoc re-conversion of entire documents | Destroys manual corrections already applied. Defeats the purpose of fixing existing files. | Edit existing markdown in place for specific discrepancies |
| Cross-document consistency checking | Out of scope per PROJECT.md. Inter-document inconsistencies are preserved. | One-to-one injection fidelity: markdown = LaTeX source exactly |

## Feature Dependencies

```
Section splitting (LaTeX + MD)
    ├── Math extraction (state-machine or pylatexenc)
    │   └── Normalize math → Compare math pairs
    ├── Cross-reference extraction (regex)
    │   └── Compare reference IDs
    ├── Text content diff (difflib)
    │   └── Categorized discrepancy report
    └── Candidate selection (if multiple .md exist)
        └── Pick best → copy to authoritative dir
```

## Recommended Phase Workflow

Each of the 6 phases (one per LaTeX source) follows this sequence:

1. **Candidate selection** (if multiple .md exist): diff each candidate against source; pick lowest-diff-count one
2. **Section splitting**: parse LaTeX `sections/*.tex` and markdown `#/##` headings into named blocks
3. **Math audit**: extract all formulas from both; normalize; compare pair-wise; flag all mismatches
4. **Cross-reference audit**: extract all `\ref`, `\cite`, `\label` from both; verify presence in markdown
5. **Text diff**: `difflib.unified_diff()` per section pair; categorize discrepancies
6. **Discrepancy report**: write categorized report to phase directory
7. **Fix cycle**: human fixes discrepancies in markdown; re-run script; confirm zero diffs

## Sources

- Project file: `.planning/PROJECT.md` -- Milestone definition, one-to-one injection fidelity, scope -- HIGH confidence
- Existing conversion: `pinn_instruction/markdown_conversion/pandoc_conversion/convert_latex_to_md.py` -- Pre/post-processing patterns -- HIGH confidence
- Python stdlib docs: `difflib`, `re`, `pathlib`, `argparse` -- All available in Python 3.12.2 on M2 Mac -- HIGH confidence
- [pylatexenc docs](https://pylatexenc.readthedocs.io/) -- LaTeX AST parsing for edge cases -- HIGH confidence
- [mistune PyPI](https://pypi.org/project/mistune/) -- Markdown AST parsing (optional) -- HIGH confidence
