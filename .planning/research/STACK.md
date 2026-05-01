# Stack Research: LaTeX-to-Markdown Conversion Verification

**Domain:** Document conversion verification (LaTeX source vs. markdown output)
**Researched:** 2026-04-30
**Confidence:** HIGH

## Recommended Stack

### Core Verification Scripting (Standard Library)

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| `difflib` (stdlib) | Python 3.12+ | Section-by-section unified diffs | `SequenceMatcher.get_opcodes()` gives programmatic change blocks; `unified_diff()` produces human-readable output. Already used successfully in Phases 5-8. Zero dependencies. |
| `re` (stdlib) | Python 3.12+ | Math formula extraction, cross-reference matching | Sufficient for extracting `$...$`, `$$...$$`, `\[...\]` math blocks, `\ref{...}`, `\label{...}`, `\cite{...}` from both LaTeX and markdown. Regex is the right tool for well-delimited patterns like these. |
| `pathlib` (stdlib) | Python 3.12+ | Filesystem traversal of section directories | Cleaner than `os.path`; matches existing project patterns in `convert_latex_to_md.py`. |
| `argparse` (stdlib) | Python 3.12+ | CLI for verification scripts | Each verification phase script needs `--source-dir`, `--markdown-file`, `--output-dir`, `--verbose` flags. argparse is standard and sufficient. |

### Supporting Libraries (Install Only What Is Used)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `pylatexenc` | 2.10 | Parse LaTeX AST for structural extraction | Use `latexwalker` to walk section files and extract math environments, headings, cross-reference nodes when regex is insufficient for nested structures. NOT needed for simple cases — regex handles 90% of extraction. Install only when a specific phase encounters nested-LaTeX that regex can't handle. |
| `mistune` | 3.1.4 | Parse markdown AST for structural comparison | Use when you need to compare document structure (heading hierarchy, list nesting) between LaTeX and markdown. NOT needed for line-by-line math/text comparison — difflib handles that. Install only if structural mismatch detection is needed. |
| `pypandoc` | 1.15+ | Programmatic pandoc invocation for AST comparison | Can output pandoc's native AST (JSON) for both LaTeX and markdown, enabling AST-level structural diff. Useful as a cross-check: convert both source and markdown to pandoc AST and compare. But adds pandoc dependency (already installed at `/opt/homebrew/bin/pandoc`). |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `pandoc` (already installed) | Convert LaTeX ↔ markdown via native AST | `/opt/homebrew/bin/pandoc` — confirmed path. Use `pandoc -f latex -t native` for AST extraction if structural comparison needed. NOT for regeneration — use only for diagnostic AST dumps. |
| `diff` (macOS built-in) | Quick manual spot checks | `diff -u <(extract_math_section.tex) <(extract_math_section.md)` for one-off formula checks during debugging. |

## Installation

```bash
# Core verification — NO new dependencies needed.
# difflib, re, pathlib, argparse are all stdlib.

# Optional: install only when a specific phase needs it
pip install pylatexenc==2.10       # Only if regex fails on nested LaTeX
pip install mistune==3.1.4          # Only if structural AST comparison needed
pip install pypandoc==1.15          # Only if pandoc-native AST diff needed
```

**Default approach:** Write Phase 10 scripts with stdlib only. Add a library ONLY when a concrete limitation (e.g., nested `\textbf{... $x^2$ ...}` that regex mangles) is hit in a specific phase.

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| stdlib `re` for math extraction | `pylatexenc.latexwalker` | When LaTeX source has deeply nested math in text (e.g., `\textbf{... $\frac{a}{b}$ ...}`) |
| `difflib.unified_diff()` for section comparison | `pypandoc` AST comparison | When you need to verify structural fidelity (heading levels, list nesting) not just text |
| Manual section-by-section diff | `deepdiff` on structured dicts | Only if comparing named-section dictionaries rather than sequential line-by-line |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **TexSoup** | Dormant since August 2020. No updates in 5+ years. Does not handle modern LaTeX command syntax. | `pylatexenc` (actively maintained, last update Feb 2025) |
| **SymPy `parse_latex`** | Cannot handle physics notation: `\vec`, `\mathbf`, `\norm`, `\mathcal`, bra-ket, multi-letter variables. Designed for pure math, not physics-heavy documents. | Regex-based extraction + manual review for physics formulas |
| **`latex2sympy3`** | Same limitations as SymPy — built on ANTLR grammar for math LaTeX, not general LaTeX documents. Wrong tool: we need text extraction, not symbolic equivalence checking. | Not needed for verification — just compare rendered formula text |
| **Pandoc re-conversion** | The task is to VERIFY and FIX existing markdown files, not regenerate them. Running pandoc again would overwrite manual corrections. The existing `convert_latex_to_md.py` already handles pandoc conversion; the new work is verification. | Section-by-section diffing of existing files against source |
| **LaTeXML / plasTeX** | Full LaTeX document processing frameworks. Heavy, complex, designed for LaTeX→XML/HTML conversion, not for diff verification. Massive overkill for comparing a few hundred lines of content per section. | `difflib` + `re` (lightweight, built-in) |
| **`deepdiff`** | Deep object comparison library. Compares Python dicts/lists recursively. Overkill for line-by-line text comparison — adds a dependency for capability already in stdlib `difflib`. | `difflib.SequenceMatcher` (stdlib, designed for text sequences) |
| **MathJax/KaTeX for rendering** | We are NOT verifying visual rendering fidelity. We are verifying that the markdown math text faithfully transcribes the LaTeX math source. Rendering adds unnecessary complexity (browser, JS runtime). | Text-level math comparison: extract → normalize → diff |
| **AI/LLM-based comparison** | Adds latency, cost, and non-determinism. The comparison task is mechanical (does text A match text B?) — AI adds no value and introduces hallucination risk. | Deterministic text diffing |
| **Building a new conversion pipeline** | Explicitly out of scope per milestone definition. The task is verification and correction of existing files. | Work with existing pandoc outputs; fix discrepancies in place |

## Stack Patterns by Phase

Each of the 6 phases follows the same verification pattern, just on different documents:

**Phase workflow per document:**
1. Select best candidate markdown (compare pandoc_conversion/ vs top-level .md)
2. Split LaTeX sections/ and markdown into named sections
3. For each section: extract math formulas, cross-references, textual content
4. Diff section content: `difflib.unified_diff(la_section_lines, md_section_lines)`
5. Report discrepancies categorized as: math, cross-reference, text, structure
6. Fix discrepancies in markdown
7. Re-diff to confirm zero differences

**Script naming convention (follow Phase 5-8 pattern):**
- `verify_ctl_instruction.py` — Phase 10a
- `verify_data_quality.py` — Phase 10b
- `verify_pinn_architecture.py` — Phase 10c
- `verify_review_framework.py` — Phase 10d
- `verify_stage_strat.py` — Phase 10e
- `verify_sampling_method.py` — Phase 10f

**Shared utilities** (one file, not one per phase):
- `md_verification_utils.py` — section splitting, math extraction, normalization, diff helpers

## Version Compatibility

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.12.2 | Confirmed on M2 Mac; all stdlib modules available |
| pandoc | 3.7.0.2 (Homebrew) | Already at `/opt/homebrew/bin/pandoc`; used only for diagnostic AST dumps |
| pylatexenc (optional) | 2.10 (stable) or 3.0a33 (pre-release) | 2.10 is 5 years old but stable and adequate for LaTeX parsing. 3.0a33 adds features but is pre-release. Prefer 2.10 for stability. |
| mistune (optional) | 3.1.4 | Current as of April 2026. Note: 3.1.0 renamed `axt_heading` → `atx_heading` — use 3.1.4 to avoid compat issues. |

## Key Design Decisions

1. **Stdlib-first by default.** This is a text comparison task, not a ML pipeline. `difflib` + `re` + `pathlib` cover the entire verification workflow. Add libraries only when a concrete limitation is hit.

2. **Math comparison is text-comparison, not semantic-equivalence.** We verify that `$\frac{dE}{dt}$` in LaTeX becomes `$\frac{dE}{dt}$` in markdown — same characters, same structure. We do NOT check that the formula is mathematically equivalent to some other representation. This simplifies the tooling enormously (no CAS needed).

3. **Pandoc is a diagnostic tool, not a conversion tool.** Use `pandoc -t native` to dump AST for debugging, but never re-run pandoc to overwrite manually-fixed markdown files.

4. **Script-per-phase, utility-per-project.** Each of the 6 documents gets its own verification script (different section structures, different known issues). Shared extraction/diff logic goes into `md_verification_utils.py`.

## Sources

- [pylatexenc PyPI](https://pypi.org/project/pylatexenc/) — v2.10 stable, 3.0a33 pre-release; LaTeX AST parsing via `latexwalker` — HIGH confidence
- [pylatexenc GitHub](https://github.com/phfaist/pylatexenc) — Active development through Feb 2025 — HIGH confidence
- [mistune PyPI](https://pypi.org/project/mistune/) — v3.1.4, BSD-3-Clause, pure Python markdown parser — HIGH confidence
- [mistune GitHub](https://github.com/lepture/mistune) — 3.1.x changelog confirms `axt_heading` rename — HIGH confidence
- [Python difflib docs](https://docs.python.org/3/library/difflib.html) — `SequenceMatcher`, `unified_diff`, `get_opcodes` — HIGH confidence (stdlib, stable API)
- [TexSoup GitHub](https://github.com/alvinwan/TexSoup) — v0.3.1, last release Aug 2020, dormant — HIGH confidence (confirmed via PyPI and GitHub)
- [SymPy Parsing docs](https://docs.sympy.org/latest/modules/parsing.html) — `parse_latex` limitations documented: no vectors, no bra-ket, no `\mathcal` — HIGH confidence
- Project file: `pinn_instruction/markdown_conversion/pandoc_conversion/convert_latex_to_md.py` — Existing conversion pipeline, pandoc path confirmed — HIGH confidence
- Project file: `.planning/PROJECT.md` — Milestone definition, phase structure, one-to-one injection fidelity requirement — HIGH confidence

---
*Stack research for: LaTeX-to-Markdown conversion verification*
*Researched: 2026-04-30*
