# Architecture Patterns: Markdown Verification Scripts

**Domain:** LaTeX-to-Markdown conversion verification
**Researched:** 2026-04-30

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  md_verification_utils.py                    │
│  (shared: split_sections, extract_math, extract_refs,       │
│   normalize_math, diff_sections, categorize_discrepancy)    │
└──────────────────────┬──────────────────────────────────────┘
                       │ imported by all 6 phase scripts
       ┌───────────────┼───────────────┬───────────────┐
       ▼               ▼               ▼               ▼
  verify_ctl.py  verify_data.py  verify_pinn.py  verify_review.py
  verify_stage.py  verify_sample.py

Each script:
  1. Parse CLI args (--source-dir, --markdown-file, --output-dir)
  2. Split LaTeX sections/ into named blocks
  3. Split markdown into corresponding named sections
  4. For each section pair:
     a. Extract math formulas -> compare
     b. Extract cross-references -> compare
     c. Run unified diff on text content
  5. Write categorized discrepancy report
  6. After fixes: re-run to confirm zero differences
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| `md_verification_utils.py` | Section splitting, math extraction, ref extraction, normalization, diff helpers | Imported by all phase scripts; no I/O of its own |
| `verify_<document>.py` (x6) | Document-specific verification: handles that document's section structure, known quirks | `md_verification_utils.py`, reads `.tex` and `.md` files, writes discrepancy reports |
| Discrepancy report (.txt or .md) | Human-readable list of all differences, categorized by type | Read by human reviewer; no programmatic consumer |
| Fixed markdown (.md) | The output of each phase: a corrected markdown file | Written by human editor; verified by re-running phase script |

### Data Flow

```
LaTeX source (sections/*.tex)  --+
                                  +--> Section splitter --> Named sections dict
Markdown file (single .md)     --+
                                          |
                    +---------------------+
                    v                     v                     v
              Math extractor       Ref extractor         Text diff
              (state machine)      (regex on both)       (difflib)
                    |                     |                     |
                    v                     v                     v
              Math pairs list       Ref pairs list       Unified diff lines
                    |                     |                     |
                    +---------------------+---------------------+
                                          v
                                Discrepancy categorizer
                                          |
                                          v
                                Categorized report
                                (math / ref / text / structure)
```

## Patterns to Follow

### Pattern 1: Extract -> Normalize -> Compare

For both math formulas and cross-references, the pipeline is always extract, normalize, then compare. Normalization prevents false positives from trivial formatting differences.

```python
def normalize_math(formula: str) -> str:
    """Normalize a LaTeX math formula for comparison."""
    f = formula.strip()
    # Strip outer delimiters
    if f.startswith("$$"): f = f[2:]
    if f.endswith("$$"): f = f[:-2]
    if f.startswith("$"): f = f[1:]
    if f.endswith("$"): f = f[:-1]
    if f.startswith("\\["): f = f[2:]
    if f.endswith("\\]"): f = f[:-2]
    # Collapse whitespace
    f = " ".join(f.split())
    return f
```

### Pattern 2: Section-Aware Diffing

Instead of diffing whole files (unreadable for 800+ lines), split both source and target into named sections first, then diff each section independently.

```python
def split_latex_sections(sections_dir: Path) -> dict[str, str]:
    """Read all .tex files in sections/ and return {name: content} dict."""
    sections = {}
    for f in sorted(sections_dir.glob("*.tex")):
        name = f.stem  # e.g., "01_intro", "04_phase1_data_prep"
        sections[name] = f.read_text(encoding="utf-8")
    return sections

def split_markdown_sections(md_file: Path) -> dict[str, str]:
    """Split markdown by ## or # headings into {name: content} dict."""
    # Use regex to find heading boundaries
    # Map heading text to section names (may need manual mapping table)
    ...
```

### Pattern 3: Candidate Selection by Diff Score

When 2-3 markdown files exist for the same LaTeX source, pick the best one quantitatively.

```python
def select_best_candidate(tex_sections: dict, candidates: list[Path]) -> Path:
    """Return the candidate markdown with fewest diff lines."""
    scores = {}
    for candidate in candidates:
        md_sections = split_markdown_sections(candidate)
        total_diffs = sum(
            len([l for l in difflib.unified_diff(
                tex_sections.get(name, "").splitlines(),
                md_sections.get(name, "").splitlines(),
                lineterm=""
            ) if l.startswith(("+", "-"))])
            for name in tex_sections
        )
        scores[candidate] = total_diffs
    return min(scores, key=scores.get)
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Whole-file diff without section splitting
**What:** Running `difflib.unified_diff()` on two 800-line files
**Why bad:** A heading shift at line 10 makes the entire rest of the file show as changed. Impossible to tell which sections actually differ.
**Instead:** Split into sections first, then diff each section independently.

### Anti-Pattern 2: Using regex inside math mode
**What:** Treating math extraction as a flat regex `r'\$(.+?)\$'`
**Why bad:** Regex can't track nested delimiters. `$\text{if } x > 0$ then $y = 1$` gets mis-extracted.
**Instead:** Use a simple state machine: track whether you're inside `$`, `$$`, `\[`, `\]`. For complex cases, fall back to pylatexenc's latexwalker.

### Anti-Pattern 3: Regenerating markdown from scratch
**What:** Running pandoc again when discrepancies are found
**Why bad:** Destroys manual corrections already applied. Replaces problem rather than fixing it.
**Instead:** Edit the existing markdown file in place. Only fix specific discrepancies.

### Anti-Pattern 4: One mega-script for all documents
**What:** A single script handling all 6 documents with if/elif branches
**Why bad:** Different documents have different section structures, quirks, edge cases. Monolithic script becomes unmaintainable.
**Instead:** One script per document + one shared utility module. Each script is 50-100 lines of document-specific logic.

## Monolithic vs Modular Handling

Sampling-method is a single `.tex` file without a `sections/` directory. The verification scripts detect this via an `is_monolithic` flag:

| Aspect | Modular | Monolithic (sampling-method) |
|--------|---------|------------------------------|
| Source files | `main.tex` + `sections/*.tex` | Single `.tex` file |
| Section extraction | Parse each file individually | Split single file on `\section{...}` |
| Section naming | Filename-derived | Heading-text-derived |
| Math extraction | Per-section | Whole-file then section-attributed |

The shared utility module handles both paths transparently.

## Sources

- Project file: `.planning/PROJECT.md` -- Phase structure, one per document -- HIGH confidence
- Prior art: Phases 5-8 verification scripts -- Established pattern of script-per-task + shared logic -- HIGH confidence
- Python docs: `difflib` module -- `unified_diff`, `SequenceMatcher` API -- HIGH confidence (stdlib, stable)
- pylatexenc docs: `latexwalker` -- LaTeX AST for edge cases when regex fails -- HIGH confidence
