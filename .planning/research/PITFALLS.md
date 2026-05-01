# Domain Pitfalls: LaTeX-to-Markdown Verification Stack

**Domain:** LaTeX-to-Markdown conversion verification -- tool and approach pitfalls
**Researched:** 2026-04-30

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: Regex fails on nested LaTeX braces in math mode

**What goes wrong:** A regex like `r'\$(.+?)\$'` (non-greedy) stops at the first `$` it finds, even if nested. `$\text{if } x > 0$ then $y = 1$` gets extracted as one broken block. More dangerously, `$\frac{a}{b}$` with simple content extracts correctly -- so the bug only manifests on specific formulas, giving false confidence.

**Why it happens:** Regular expressions (even with `re.DOTALL`) cannot correctly track balanced delimiters without a stack.

**Consequences:** Math formulas silently mis-extracted. Diff report says "no discrepancies" but formulas weren't even compared. **False negative** -- worst kind of bug in verification.

**Prevention:**
1. Use a state-machine parser for math extraction, not regex alone
2. Cross-validate: count math blocks from regex vs. pylatexenc. If counts differ, regex missed something.
3. Install pylatexenc only when a concrete extraction mismatch is confirmed

**Detection:** Compare math block counts from regex extraction vs. pylatexenc AST walk. Any discrepancy = regex bug.

### Pitfall 2: Pandoc-generated artifacts treated as discrepancies

**What goes wrong:** Pandoc adds syntax to markdown: `{#id .class}` heading anchors, `:::` fenced divs, `{style="..."}` color spans. The existing `convert_latex_to_md.py` post-processes to strip these. If verification runs on uncleaned markdown, these artifacts appear as discrepancies when they are expected pandoc behavior.

**Why it happens:** Different markdown files may have been cleaned to different degrees (top-level .md vs pandoc_conversion/ .md).

**Consequences:** Hundreds of trivial diffs (every heading shows `{#id}` vs no anchor). Obscures real discrepancies.

**Prevention:** Normalize both LaTeX source and markdown before comparison: strip pandoc artifacts (heading anchors, fenced divs, code block attrs), strip LaTeX boilerplate (preamble, `\begin{document}`).

**Detection:** If diffs are predominantly `- ## Heading {#id .class}` vs `+ ## Heading` -- pandoc artifacts not normalized.

### Pitfall 3: Comment block content flagged as "missing"

**What goes wrong:** LaTeX sources use `\begin{comment}...\end{comment}` to exclude content. If verification treats commented-out blocks as source, it flags valid markdown (which correctly excludes them) as "missing content."

**Consequences:** Hundreds of false-positive discrepancies. Manual review wastes time on intentionally excluded content.

**Prevention:** Strip `\begin{comment}...\end{comment}` blocks from LaTeX source before comparison. For pinn-architecture, explicitly exclude the 3 `*_inactive.tex` files from the section list.

### Pitfall 4: Math delimiter mismatch (`\[...\]` vs `$$...$$`)

**What goes wrong:** LaTeX uses `\[...\]` for display math. Pandoc converts to `$$...$$`. Verification flags every display math formula as different even though content is identical.

**Consequences:** Spam in diff reports; real math discrepancies buried in noise.

**Prevention:** Normalize all math delimiters to canonical form before comparison. `\[...\]` and `$$...$$` are equivalent for comparison purposes.

## Moderate Pitfalls

### Pitfall 5: Section heading mapping drift

**What goes wrong:** LaTeX sections are `\section{Data Preparation}` with files like `04_phase1_data_prep.tex`. Markdown sections are `## Data Preparation`. The verification script needs a mapping table. Wrong mapping means every line shows as a diff.

**Consequences:** Perfectly correct markdown flagged as "totally wrong" -- trust in verification tool collapses.

**Prevention:** Build mapping table explicitly per document. Validate by checking that first few lines of each mapped section pair match. Print summary: "Mapped LaTeX section 04_phase1_data_prep -> Markdown ## Data Preparation (first 3 lines match: YES/NO)."

### Pitfall 6: Cross-reference format mismatch

**What goes wrong:** LaTeX has `\ref{fig:workflow}` which pandoc converts to plain `fig:workflow` or `[fig:workflow](#fig:workflow)`. If verification expects LaTeX format, it flags every reference as broken.

**Prevention:** Extract reference IDs only (e.g., `fig:workflow`), not formatting. Check that the ID appears somewhere in the corresponding markdown section.

### Pitfall 7: Installing heavy dependencies prematurely

**What goes wrong:** Installing pylatexenc, mistune, pypandoc, and deepdiff before any phase work begins. Most won't be needed. Creates an implicit maintenance burden and makes the verification toolchain appear complex.

**Prevention:** Start with stdlib only. Add a library ONLY when a concrete limitation is hit. Demonstrate the limitation first (e.g., "regex extracted 42 math blocks but pylatexenc found 47").

## What NOT to Use -- With Explicit Reasons

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **TexSoup** | Dormant since August 2020 (v0.3.1). No updates in 5+ years. | `pylatexenc` (v2.10 stable, actively maintained through Feb 2025) |
| **SymPy `parse_latex`** | Cannot handle physics notation: `\vec`, `\mathbf`, `\norm`, `\mathcal`, bra-ket. Designed for pure math. | Regex-based extraction + manual review for physics formulas |
| **Pandoc re-conversion** | Destroys manual corrections. Defeats the purpose of fixing existing files. | Edit existing markdown in place; only fix specific discrepancies |
| **`deepdiff`** | Deep object comparison library. Overkill for line-by-line text diff -- adds dependency for stdlib capability. | `difflib.SequenceMatcher` (stdlib, designed for text sequences) |
| **MathJax/KaTeX rendering** | We verify text fidelity, not visual rendering. Adds browser/JS complexity. | Text-level math comparison: extract -> normalize -> diff |
| **AI/LLM-based comparison** | Adds latency, cost, non-determinism. Hallucination risk on a mechanical task. | Deterministic text diffing |
| **LaTeXML / plasTeX** | Full document processing frameworks. Massive overkill for text comparison. | `difflib` + `re` (built-in, lightweight) |
| **Building a new conversion pipeline** | Explicitly out of scope. Task is verification and correction of existing files. | Work with existing pandoc outputs; fix discrepancies in place |

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| CTL-instruction (math-heavy, 8 sections) | Nested math in stage criteria text (Pitfall 1) | Use pylatexenc as cross-check on math extraction |
| CTL-instruction (3 competing MD files) | Pandoc artifacts in one candidate but not another (Pitfall 2) | Normalize all candidates before comparison |
| PINN-architecture (10 sections, 3 inactive) | Commented-out sections look like missing (Pitfall 3) | Verify comment stripping covers 3 inactive section files |
| Review-of-framework (2 sub-documents) | Section mapping across 2 LaTeX dirs to 2 markdown files | Build separate mapping table for each sub-document |
| Data-quality-assessment (7 sections) | Cross-reference format (Pitfall 6) -- heavy `\ref` and `\cite` use | Compare reference IDs, not formatting |
| Sampling-method (monolithic) | Section splitting not applicable -- whole-file diff needed | Different approach from modular documents |
| Stage-strat-revision (6 sections) | Blank line differences in table environments | Normalize blank lines before diff |

## Sources

- `convert_latex_to_md.py` -- Pre/post-processing patterns (comment stripping, macro expansion, pandoc artifact cleaning) -- HIGH confidence
- Python docs: `re` module -- Known limitation: regular expressions cannot match balanced delimiters -- HIGH confidence
- [pylatexenc docs](https://pylatexenc.readthedocs.io/) -- LaTeX AST walker that handles nested braces -- HIGH confidence
- [TexSoup GitHub](https://github.com/alvinwan/TexSoup) -- v0.3.1, last release Aug 2020, dormant -- HIGH confidence
- `.planning/PROJECT.md` -- Scope: commented-out content excluded, inter-document inconsistencies preserved -- HIGH confidence
