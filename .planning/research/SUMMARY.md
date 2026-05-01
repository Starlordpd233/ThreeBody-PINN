# Project Research Summary

**Project:** Three-Body Physics-Informed LLM -- v1.3 Markdown Conversion Verification
**Domain:** Document conversion verification (LaTeX source vs. markdown output)
**Researched:** 2026-04-30
**Confidence:** HIGH

## Executive Summary

This is a **document fidelity verification task**: confirm that 6 markdown files in `pinn_instruction/markdown_conversion/` are exact one-to-one textual reproductions of their LaTeX sources, and fix any discrepancies found. The task is mechanical (compare text A to text B), not generative (do not re-convert or regenerate). Experts in this domain build lightweight, deterministic verification scripts using standard library tools -- the work is string comparison, not machine learning.

The recommended approach is **stdlib-first with per-document scripts and a shared utility module**. Python's `difflib` (section-by-section unified diffs), `re` (math/reference extraction), and `pathlib` (filesystem traversal) cover the entire core workflow with zero new dependencies. Optional libraries (`pylatexenc`, `mistune`, `pypandoc`) are available as diagnostic tools but should only be installed when a concrete limitation of the stdlib approach is demonstrated. The architecture follows a script-per-phase pattern established in v1.1 Phases 5-8: one verification script per LaTeX source, all importing from a single `md_verification_utils.py`.

The key risk is **false negatives in math verification**. A naive regex such as `r'\$(.+?)\$'` will silently mis-extract math formulas with nested braces or inline text, producing a diff report showing "no discrepancies" when formulas were never even compared. Prevention: use a state-machine parser for math extraction, and cross-validate formula counts against `pylatexenc` when regex is the primary tool. Secondary risks include pandoc artifact noise obscuring real diffs (normalize before comparison) and section heading mapping drift causing entire sections to show as changed (explicit mapping tables with first-3-lines validation).

## Key Findings

### Recommended Stack

Stdlib-first by design. This is a text comparison task; the entire verification workflow is covered by Python standard library modules. Add libraries only when a concrete limitation is hit.

**Core technologies (stdlib, zero install):**
- `difflib`: Section-by-section unified diffs via `SequenceMatcher.get_opcodes()` and `unified_diff()`. The workhorse of verification. Already proven in Phases 5-8.
- `re`: Math formula extraction (`$...$`, `$$...$$`, `\[...\]`), cross-reference extraction (`\ref`, `\cite`, `\label`), heading boundary detection. Sufficient for well-delimited patterns.
- `pathlib`: Filesystem traversal of `sections/` directories. Cleaner than `os.path`; matches existing project patterns.
- `argparse`: CLI for verification scripts. Each script needs `--source-dir`, `--markdown-file`, `--output-dir`, `--verbose` flags.

**Optional libraries (install only when concretely needed):**
- `pylatexenc` (v2.10): LaTeX AST parsing via `latexwalker`. Use as cross-validation when regex extraction counts don't match. Needed only for documents with deeply nested LaTeX in text.
- `mistune` (v3.1.4): Markdown AST parsing for structural comparison. Needed only if heading hierarchy or list nesting drift must be detected.
- `pypandoc` (v1.15+): Programmatic pandoc invocation for AST-level structural diff. Pandoc 3.7.0.2 already installed at `/opt/homebrew/bin/pandoc`.

**Explicitly avoid:**
| What | Why |
|------|-----|
| TexSoup | Dormant since August 2020, no modern LaTeX support |
| SymPy parse_latex | Cannot handle physics notation (vectors, norms, bra-ket, `\mathcal`) |
| Pandoc re-conversion | Destroys manual corrections; verification is fix-in-place, not regenerate |
| LaTeXML / plasTeX | Full document processing frameworks; massive overkill for text comparison |
| deepdiff | Deep object comparison; adds dependency for capability already in `difflib` |
| MathJax/KaTeX rendering | We verify text fidelity, not visual rendering; adds browser/JS complexity |
| AI/LLM-based comparison | Non-deterministic, hallucination risk on a mechanical task |

For full details and install commands, see [STACK.md](./STACK.md).

### Expected Features

**Table stakes (verification is incomplete without these):**

| Feature | Why Required |
|---------|-------------|
| Section-by-section line diff (LaTeX vs MD) | Modular sources split into `sections/`; whole-file diff is unreadable for 800+ lines |
| Math formula extraction (state-machine, not regex) | Formulas are highest-value content; regex silently fails on nested braces |
| Cross-reference extraction (`\ref`, `\cite`, `\label`) | References must be preserved in markdown; verify presence, not formatting |
| Commented-out content detection | `\begin{comment}...\end{comment}` blocks intentionally excluded from markdown |
| Candidate selection (multiple .md files) | 4 of 6 documents have 2-3 competing markdown files; must pick best starting point |

**Differentiators (make verification reliable, not just functional):**

| Feature | Value |
|---------|-------|
| Normalized math comparison (whitespace-insensitive, delimiter-agnostic) | Prevents false positives from trivial formatting differences |
| Discrepancy categorization (math vs text vs structure vs ref) | Makes fix prioritization clear; math errors critical, formatting cosmetic |
| Re-diff confirmation (fix -> re-diff -> confirm zero diffs) | Prevents regressions and incomplete fixes |
| Shared utility module (`md_verification_utils.py`) | Avoids copy-pasting extraction/diff logic across 6 scripts |

**Anti-features (explicitly excluded from verification tooling):**

| What | Why Excluded |
|------|-------------|
| SymPy-based math equivalence checking | Can't handle physics notation; wrong tool for text comparison |
| Visual rendering comparison | Massive complexity (headless browser, JS runtime); non-deterministic |
| AI/LLM-based discrepancy detection | Non-deterministic, may hallucinate; task is mechanical |
| Auto-fixing discrepancies | Risk of scripts deleting formulas; all fixes must be human-reviewed |
| Pandoc re-conversion | Destroys manual corrections already applied |
| Cross-document consistency checking | Out of scope; inter-document inconsistencies are preserved per PROJECT.md |

For the full feature landscape and dependency tree, see [FEATURES.md](./FEATURES.md).

### Architecture Approach

**Pattern:** One shared utility module + six per-document verification scripts. Each script follows the same pipeline: parse CLI args -> split sections -> extract/compare math, refs -> run unified diff -> write categorized report -> re-run after fixes to confirm zero diffs.

**Architecture diagram:**
```
md_verification_utils.py
  (split_sections, extract_math, extract_refs,
   normalize_math, diff_sections, categorize_discrepancy)
       |
       | imported by all 6 phase scripts
       |
  verify_ctl.py (CTL-instruction, 8 sections, 3 candidates)
  verify_data.py (Data-quality-assessment, 7 sections)
  verify_pinn.py (PINN-architecture, 7 active + 3 inactive sections)
  verify_review.py (Review-of-framework, 7 sections, 2 sub-documents)
  verify_stage.py (Stage-strat-revision, 6 sections)
  verify_sample.py (Sampling-method, monolithic, no sections/)
```

**Three core patterns:**
1. **Extract -> Normalize -> Compare**: For both math formulas and cross-references, always normalize before comparison. Strip delimiters, collapse whitespace, canonicalize `\[...\]` to `$$...$$`. This prevents false positives from trivial formatting differences.
2. **Section-Aware Diffing**: Never diff whole files. Split both source and target into named sections first, then diff each section independently. A heading shift at line 10 making the entire rest of the file show as changed is unacceptable.
3. **Candidate Selection by Diff Score**: When 2-3 markdown files exist for the same source, diff each against the source and pick the one with fewest diff lines. This is quantitative, not subjective.

**Monolithic handling:** Sampling-method is a single `.tex` file without a `sections/` directory. The shared utility module detects this and splits on `\section{...}` boundaries within the single file instead of reading individual `.tex` files.

For the full architecture with anti-patterns and component boundaries, see [ARCHITECTURE.md](./ARCHITECTURE.md).

### Critical Pitfalls

Top 5 pitfalls ordered by severity:

1. **Regex silently fails on nested LaTeX braces.** A non-greedy regex `r'\$(.+?)\$'` stops at the first `$`, mis-extracting formulas with inline text or nested structures. This produces false negatives -- diff reports show "no discrepancies" but formulas were never compared. **Prevention:** Use a state-machine parser for math extraction. Cross-validate formula counts against `pylatexenc` output.

2. **Pandoc-generated artifacts treated as discrepancies.** Pandoc adds `{#id .class}` heading anchors, `:::` fenced divs, and `{style="..."}` color spans. Different `.md` files may have been cleaned to different degrees. Verification on uncleaned markdown produces hundreds of trivial diffs that obscure real discrepancies. **Prevention:** Normalize both LaTeX source and markdown before comparison -- strip pandoc artifacts and LaTeX boilerplate.

3. **Comment block content flagged as "missing."** `\begin{comment}...\end{comment}` blocks are intentionally excluded from markdown. If verification treats commented-out blocks as source, it flags valid markdown as incomplete. **Prevention:** Strip comment blocks from LaTeX source before comparison. For pinn-architecture, explicitly exclude the 3 `*_inactive.tex` files.

4. **Math delimiter mismatch (`\[...\]` vs `$$...$$`).** LaTeX uses `\[...\]` for display math; pandoc converts to `$$...$$`. Verification flags every display math formula as different even though content is identical. **Prevention:** Normalize all math delimiters to canonical form before comparison.

5. **Section heading mapping drift.** LaTeX sections are `\section{Data Preparation}` with files like `04_phase1_data_prep.tex`; markdown sections are `## Data Preparation`. A wrong mapping makes every line show as a diff. **Prevention:** Build explicit mapping table per document. Validate by checking that the first 3 lines of each mapped section pair match.

For phase-specific warnings and the full "what not to use" rationale, see [PITFALLS.md](./PITFALLS.md).

## Implications for Roadmap

The milestone defines 6 phases, one per LaTeX source document. Research confirms this structure and provides specific guidance on ordering, dependencies, and per-phase risk mitigation.

### Pre-Phase 0: Build Shared Utilities

Before any document verification begins, build `md_verification_utils.py`. This is not a separate phase but a prerequisite that must exist before Phase 10a can run.

**Delivers:** `md_verification_utils.py` with `split_sections()`, `extract_math()`, `extract_refs()`, `normalize_math()`, `diff_sections()`, `categorize_discrepancy()`, `select_best_candidate()`.

**Rationale:** Every phase script imports from this module. Building it first prevents duplicated logic and inconsistent extraction across documents. The module handles both modular and monolithic source structures transparently.

### Phase 10a: CTL-Instruction Verification

**Rationale:** Start here because this is the most complex document -- 8 sections, 3 competing markdown candidates, math-heavy content with stage criteria containing inline formulas. Proving the tooling works on the hardest case validates the entire approach. This document is most likely to expose regex limitations (Pitfall 1) and pandoc artifacts (Pitfall 2), forcing any needed optional-library decisions early.

**Delivers:** Authoritative `ctl-instruction.md` with zero diffs against LaTeX source. Verification script `verify_ctl_instruction.py`.

**Addresses:** Candidate selection (3 candidates to score), math formula audit (heavy use of display math in stage criteria), cross-reference audit.

**Avoids:** Regex-on-nested-math (Pitfall 1) -- use pylatexenc as cross-check. Pandoc artifact noise (Pitfall 2) -- normalize all 3 candidates before scoring.

### Phase 10b: Data-Quality-Assessment Verification

**Rationale:** Moderate complexity. 7 sections, heavy `\ref` and `\cite` usage. Following CTL-instruction, the verification pattern is established; this phase exercises cross-reference extraction in depth (Pitfall 6).

**Delivers:** Authoritative `data-quality-assessment.md` with zero diffs. Verification script `verify_data_quality.py`.

**Avoids:** Cross-reference format mismatch (Pitfall 6) -- compare reference IDs only, not formatting.

### Phase 10c: PINN-Architecture Verification

**Rationale:** Unique challenge: 7 active + 3 commented-out sections. This is the only document where comment stripping is a significant concern (Pitfall 3). The verification script must explicitly handle the 3 `*_inactive.tex` exclusions.

**Delivers:** Authoritative `pinn-architecture.md` with zero diffs. Verification script `verify_pinn_architecture.py`.

**Avoids:** Comment block false positives (Pitfall 3) -- verify comment stripping covers all 3 inactive section files.

### Phase 10d: Review-of-Framework Verification

**Rationale:** Highest structural complexity: two sub-documents (review_of_framework and stage_strat_revision) under one LaTeX source directory, each with its own `main.tex` + `sections/` and corresponding markdown file. Section mapping must handle two separate mapping tables (Pitfall 5).

**Delivers:** Two authoritative markdown files with zero diffs. Verification script `verify_review_framework.py`.

**Avoids:** Section mapping drift (Pitfall 5) -- build separate mapping table for each sub-document. Validate with first-3-lines check.

### Phase 10e: Stage-Strategy-Revision Verification

**Rationale:** 6 sections. Moderate complexity. After handling the 2-sub-document structure in Phase 10d, the verification pattern for sub-documents is established. This phase addresses blank-line normalization in table environments.

**Delivers:** Authoritative `stage_strat_revision.md` with zero diffs. Verification script `verify_stage_strat.py`.

**Avoids:** Blank line differences in table environments causing diff noise -- normalize blank lines before diff.

### Phase 10f: Sampling-Method Verification

**Rationale:** Monolithic document (single `.tex` file, no `sections/` directory). The verification script must split on `\section{...}` boundaries within a single file rather than reading individual `.tex` files. Placing this last means the shared utilities have already been validated on modular documents; adding monolithic support is the final edge case.

**Delivers:** Authoritative `sampling-method.md` with zero diffs. Verification script `verify_sampling_method.py`.

**Avoids:** Assuming modular structure -- the shared utility must handle monolithic split transparently (designed into `md_verification_utils.py` from the start).

### Phase Ordering Rationale

- **Dependency flow:** Pre-Phase 0 (shared utilities) -> Phase 10a (hardest case, validates tooling) -> Phase 10b-10c (exercise different extractors) -> Phase 10d-10e (sub-document structure) -> Phase 10f (monolithic edge case).
- **Hardest first:** CTL-instruction has 3 candidates, heavy math, complex section structure. If the tooling works here, it works everywhere. If regex fails here, pylatexenc gets installed early and benefits all subsequent phases.
- **Structural progression:** Modular (10a-10c) -> sub-document modular (10d-10e) -> monolithic (10f). Each step adds one structural variant.
- **No inter-phase dependencies between 10a-10f:** Each document is independent. Once shared utilities exist, phases could theoretically run in parallel. Sequential ordering is for learning and incremental tool refinement.

### Research Flags

**Phases likely needing deeper research during planning:**
- **Phase 10a (CTL-instruction):** Math extraction patterns. The state-machine parser design needs concrete validation against the actual LaTeX formulas in this document. If regex fails, pylatexenc integration must be designed.
- **Phase 10c (PINN-architecture):** Comment block detection. The `\begin{comment}...\end{comment}` pattern needs exact matching against the 3 inactive section files to ensure no edge cases.
- **Phase 10d (Review-of-framework):** Section mapping for 2-sub-document structure. The mapping table construction for 2 separate `main.tex` + `sections/` pairs under one source directory needs design.

**Phases with well-documented patterns (skip research-phase):**
- **Phase 10b (Data-quality-assessment):** Standard modular document, established pattern from 10a. No novel challenges.
- **Phase 10e (Stage-strat-revision):** Sub-document pattern established in 10d. Only novelty is table blank-line normalization.
- **Phase 10f (Sampling-method):** Monolithic handling is a known pattern with existing solutions (parse on `\section{...}`). The shared utility's monolithic path can be designed upfront.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All core tools are Python stdlib (stable API, well-documented). Optional libraries verified via PyPI and GitHub (pylatexenc active through Feb 2025, mistune 3.1.4 current). Alternatives explicitly excluded with documented reasons. |
| Features | HIGH | Table stakes derived from PROJECT.md requirements and the concrete LaTeX source structure in `pinn_instruction/original_latex/`. All feature decisions trace to a specific document characteristic or conversion artifact. Anti-features justified with concrete counter-examples. |
| Architecture | HIGH | Pattern established by v1.1 Phases 5-8 (script-per-task + shared logic). Monolithic handling is the only novel pattern and has a well-understood solution (split on `\section{...}`). Component boundaries are simple (1 shared module, 6 importers). |
| Pitfalls | HIGH | All pitfalls are concrete and verifiable. Regex limitation on nested braces is a known CS fact. Pandoc artifacts are observable in existing conversion outputs. Comment blocks and delimiter mismatches have precise detection criteria. Phase-specific warnings mapped to specific document characteristics. |

**Overall confidence: HIGH**

All four research dimensions converge on a clear, well-scoped approach. The task is mechanical (text comparison), the tools are stdlib, the architecture is proven (prior phases), and the pitfalls are concrete with explicit prevention strategies. There are no novel domains, no dependency uncertainties, and no architectural ambiguities.

### Gaps to Address

Research was conclusive across all four dimensions. The following are implementation-level decisions deferred to planning, not research gaps:

- **State-machine parser design**: The exact state transitions and edge cases for math extraction need a concrete implementation. Research confirms regex alone is insufficient; the specific state machine is a design task during Phase 10a planning.
- **Section mapping table format**: The exact format (dict, YAML, inline constants) for per-document section name mappings is a minor implementation choice with no research dependency.
- **Discrepancy report format**: Whether reports are Markdown, plaintext, or JSON is a UX decision that affects no technical dependency.
- **Candidate selection for 4 documents with variants**: Which of the 2-3 competing markdown files is the best starting candidate for CTL and PINN-architecture -- requires content comparison during those phases.

## Sources

### Primary (HIGH confidence)
- `.planning/PROJECT.md` -- Milestone definition, 6-phase structure, one-to-one injection fidelity, scope boundaries
- `pinn_instruction/markdown_conversion/pandoc_conversion/convert_latex_to_md.py` -- Existing conversion pipeline, pre/post-processing patterns, pandoc path
- Python stdlib docs (`difflib`, `re`, `pathlib`, `argparse`) -- All available in Python 3.12.2 on M2 Mac, stable APIs
- [pylatexenc PyPI](https://pypi.org/project/pylatexenc/) -- v2.10 stable, LaTeX AST parsing, active development through Feb 2025
- [mistune PyPI](https://pypi.org/project/mistune/) -- v3.1.4, BSD-3-Clause, pure Python markdown parser
- [TexSoup GitHub](https://github.com/alvinwan/TexSoup) -- v0.3.1, dormant since Aug 2020 (confirms exclusion)
- [SymPy Parsing docs](https://docs.sympy.org/latest/modules/parsing.html) -- `parse_latex` limitations documented (confirms exclusion)

### Secondary (MEDIUM confidence)
- `.planning/phases/` -- Phase 5-8 verification scripts establishing the script-per-task + shared-logic pattern
- `pinn_instruction/original_latex/` -- 6 LaTeX source directories confirming section counts and monolithic/modular structure

### Tertiary (LOW confidence)
- None. All research is based on existing project files, stdlib documentation, or verified PyPI package states.

---
*Research completed: 2026-04-30*
*Ready for roadmap: yes*
