# Phase 7: Structure Fidelity Verification - Research

**Researched:** 2026-03-21
**Domain:** Python LaTeX structural element extraction, regex-based parsing, presence verification
**Confidence:** HIGH

## Summary

This phase requires building a Python script (`verify_structure.py`) that extracts and verifies structural LaTeX elements are faithfully preserved in the modular output compared to the original monolithic files for all 5 structures. The structural elements to verify are: (1) section/subsection hierarchy (STRUCT-01), (2) label declarations (STRUCT-02), (3) cross-references (STRUCT-03), (4) citations and bibliography (STRUCT-04), and (5) float environments including figures, tables, and longtables (STRUCT-05).

The core technical approach reuses the modular content assembly from Phase 5 (resolve all `\input{}`/`\include{}` directives to produce flat assembled content) and applies category-specific extraction using regex patterns. Unlike Phase 5 which performed line-by-line diffing, Phase 7 performs structural element extraction and presence verification. The verification is "presence-based" (are all original elements present in modular?) rather than "exact-diff" (which could be confused by whitespace differences that don't affect LaTeX structure).

**Primary recommendation:** Reuse Phase 5's `resolve_includes()` function for modular assembly, apply regex extraction for each structural category, compare extracted sets using Python set operations with deduplication, and generate a Markdown report following the established format from Phases 5 and 6.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Script design:**
- **D-01:** Single script `verify_structure.py` in `pinn_instruction/original_latex/verification/` -- consistent with Phase 5 (verify_content.py) and Phase 6 (verify_preamble.py) pattern
- **D-02:** Same CLI interface: `--structure <name>`, `--output <path>`, `--verbose`, run all structures by default
- **D-03:** Same modular content assembly as Phase 5: full recursive resolution of `\input{}`/`\include{}` from the modular main.tex to produce flat assembled content, then extract structural elements

**Section hierarchy (STRUCT-01):**
- **D-04:** Extract ordered flat list of `\section`, `\subsection`, `\subsubsection`, `\paragraph`, `\subparagraph` commands (with their title text) from both original and assembled modular content
- **D-05:** Compare sequentially -- report any ordering differences, missing sections, or extra sections. Side-by-side display (original vs modular) for easy human review
- **D-06:** Strip whitespace from extracted titles before comparison; ignore optional short-title arguments (e.g., `\section[short]{Long Title}` -> compare only "Long Title")

**Label and reference checking (STRUCT-02, STRUCT-03):**
- **D-07:** Extract all `\label{...}` declarations from original; verify each appears in modular assembled content. Report missing labels.
- **D-08:** Extract all `\ref{...}`, `\eqref{...}`, `\autoref{...}` from original; verify each appears in modular assembled content. Report missing references.
- **D-09:** Only check presence -- do not verify that referenced labels are defined (cross-reference validity is a compilation concern, Phase 8)

**Citation and bibliography (STRUCT-04):**
- **D-10:** Extract all `\cite{...}`, `\citep{...}`, `\citet{...}`, `\citealt{...}`, `\nocite{...}` from original; verify each appears in modular assembled content
- **D-11:** Extract `\bibliography{...}` and `\printbibliography` declarations from original; verify presence in modular content
- **D-12:** For multi-key citations like `\cite{key1,key2,key3}`, split on commas and track each key individually

**Float environments (STRUCT-05):**
- **D-13:** Extract full content of each `\begin{figure}...\end{figure}`, `\begin{table}...\end{table}`, `\begin{longtable}...\end{longtable}` block from both original and modular assembled content
- **D-14:** Compare float count per type (must match); compare full content of each float using difflib -- flag any content differences within floats (missing captions, altered labels, dropped rows)
- **D-15:** Use brace/environment depth tracking for extraction (same pattern as Phase 6 config block extraction)

**Inactive section handling:**
- **D-16:** Exclude inactive section files for pinn-architecture (input_vector_inactive, advanced_training_inactive, consolidated_blueprint_inactive) -- same as Phase 5 D-04. Do not report structural elements from inactive files as missing.

**Report format:**
- **D-17:** Markdown output to `pinn_instruction/original_latex/verification/structure_verification_report.md` -- consistent with D-06 from Phase 5 CONTEXT
- **D-18:** Report structure: summary table (pass/fail per structure) at top, followed by per-structure detail sections with subsections for each check category (sections, labels, refs, citations, floats)
- **D-19:** Exit code 0 if all structures pass all checks; exit code 1 if any structure has any mismatch

### Claude's Discretion

- Exact regex patterns for extraction (handles multiline titles, optional arguments, etc.)
- Argparse design and progress output
- Whether to deduplicate labels/refs before comparison (reasonable to deduplicate)
- Handling of `\input{}`-only vs `\include{}`-only structures (ctl-instruction uses `\include{}`)

### Deferred Ideas (OUT OF SCOPE)

None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| STRUCT-01 | Section/subsection hierarchy in modular output matches original for all 5 structures | Regex extraction of `\section`, `\subsection`, `\subsubsection`, `\paragraph`, `\subparagraph` with title text; ordered comparison with side-by-side display. Handles optional short-title arguments `[short]` by extracting only the main title. |
| STRUCT-02 | All `\label` declarations from original are present in modular sections | Regex extraction `\label{...}` from assembled content; set comparison with deduplication. Presence check only (not cross-reference validity). |
| STRUCT-03 | All `\ref`, `\eqref`, `\autoref` references from original are present in modular sections | Regex extraction of all three reference forms; set comparison with deduplication. Presence check only (per D-09). |
| STRUCT-04 | All `\cite` and `\bibliography`/`\printbibliography` references preserved | Regex extraction of `\cite`, `\citep`, `\citet`, `\citealt`, `\nocite`; split multi-key citations on commas. Extract `\bibliography{...}` and `\printbibliography` separately. |
| STRUCT-05 | All figure/table float environments preserved with their content | Environment depth tracking to extract complete `\begin{figure}...\end{figure}`, `\begin{table}...\end{table}`, `\begin{longtable}...\end{longtable}` blocks. Compare count per type and full content using difflib. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.12.2 | Runtime environment | Project standard, same as Phases 5 and 6 |
| re | (built-in) | Regex-based LaTeX element extraction | Handles all structural constructs; proven in Phases 5 and 6 |
| pathlib.Path | (built-in) | File path handling | Project standard across all scripts |
| dataclasses | (built-in) | Structure and element data models | Used in Phases 5 and 6 |
| argparse | (built-in) | CLI argument parsing | Consistent with Phases 5 and 6 script interface |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| difflib | (built-in) | Float content comparison | For comparing float environment content within blocks |
| datetime | (built-in) | Report timestamp | For generated report metadata |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Custom regex parsing | pylatexenc library | External dependency; our structures are simple enough for regex |
| Custom regex parsing | TexSoup library | External dependency; overkill for structural element extraction |
| Presence verification | Full LaTeX parsing | We only need presence verification; full parsing is overkill |

**Installation:**
No installation required -- all dependencies are Python built-in modules.

**Version verification:**
```bash
python3 --version
# Python 3.12.2
```

## Architecture Patterns

### Recommended Project Structure
```
pinn_instruction/original_latex/
  verification/
    verify_content.py              # Phase 5 (exists)
    content_verification_report.md # Phase 5 output (exists)
    verify_preamble.py             # Phase 6 (exists)
    preamble_verification_report.md # Phase 6 output (exists)
    verify_structure.py            # Phase 7 script (NEW)
    structure_verification_report.md # Phase 7 output (NEW)
```

### Pattern 1: Reuse Phase 5 Content Assembly
**What:** Reuse the `resolve_includes()` function from Phase 5 to produce flat assembled content from modular files.
**When to use:** For all 5 structures, to produce comparable content.
**Key insight:** The modular content must be fully resolved (all `\input{}`/`\include{}` directives expanded) before structural elements can be extracted. Phase 5 already has a proven implementation.
**Example (from verify_content.py):**
```python
def resolve_includes(content: str, base_dir: Path, depth: int = 0) -> str:
    """Recursively resolve \\input{} and \\include{} directives."""
    if depth > 10:  # Safety limit
        return content

    pattern = re.compile(r'^(\s*)(\\(?:input|include)\{([^}]+)\})(\s*)$', re.MULTILINE)

    def replace_include(match: re.Match) -> str:
        include_path = match.group(3)
        if not include_path.endswith('.tex'):
            include_path += '.tex'
        file_path = base_dir / include_path
        if not file_path.exists():
            return match.group(2)
        included_content = file_path.read_text(encoding='utf-8')
        return resolve_includes(included_content, file_path.parent, depth + 1)

    return pattern.sub(replace_include, content)
```

### Pattern 2: Section Hierarchy Extraction
**What:** Extract ordered list of sectioning commands with their titles.
**When to use:** For STRUCT-01 verification.
**Key insight:** LaTeX section commands can have optional short titles: `\section[Short]{Full Title}`. The verification should compare the main title only. Titles may span multiple lines (rare but possible). Strip whitespace before comparison.
**Example:**
```python
@dataclass
class SectionHeading:
    """A section heading with its level and title."""
    level: str      # "section", "subsection", "subsubsection", "paragraph", "subparagraph"
    title: str      # The title text (without optional short title)
    line_num: int   # Line number in source (for reporting)

SECTION_PATTERN = re.compile(
    r'\\(section|subsection|subsubsection|paragraph|subparagraph)'
    r'(?:\s*\[[^\]]*\])?'  # Optional short title [Short]
    r'\s*\{([^}]+)\}',      # Main title {Title}
    re.MULTILINE
)

def extract_sections(content: str) -> List[SectionHeading]:
    """Extract all section headings with their levels and titles."""
    results = []
    for match in SECTION_PATTERN.finditer(content):
        level = match.group(1)
        title = match.group(2).strip()  # Strip whitespace
        # Count line number from content start
        line_num = content[:match.start()].count('\n') + 1
        results.append(SectionHeading(level=level, title=title, line_num=line_num))
    return results
```

### Pattern 3: Label Extraction
**What:** Extract all `\label{...}` declarations.
**When to use:** For STRUCT-02 verification.
**Key insight:** Labels can appear in various contexts: section labels (`\section{...}\label{sec:intro}`), figure labels, table labels, equation labels. The regex captures all. Deduplicate before comparison (same label appearing twice in one file is a LaTeX error anyway).
**Example:**
```python
LABEL_PATTERN = re.compile(r'\\label\{([^}]+)\}')

def extract_labels(content: str) -> Set[str]:
    """Extract all \\label declarations, deduplicated."""
    return set(match.group(1).strip() for match in LABEL_PATTERN.finditer(content))
```

### Pattern 4: Reference Extraction
**What:** Extract all `\ref{...}`, `\eqref{...}`, `\autoref{...}` references.
**When to use:** For STRUCT-03 verification.
**Key insight:** These three reference forms have different semantics but all reference labels. The verification only checks presence (the referenced label might not exist -- that's a compilation issue for Phase 8). Deduplicate before comparison.
**Example:**
```python
REF_PATTERN = re.compile(r'\\(?:ref|eqref|autoref)\{([^}]+)\}')

def extract_refs(content: str) -> Set[str]:
    """Extract all \\ref, \\eqref, \\autoref references, deduplicated."""
    return set(match.group(1).strip() for match in REF_PATTERN.finditer(content))
```

### Pattern 5: Citation Extraction
**What:** Extract all citation commands and their keys.
**When to use:** For STRUCT-04 verification.
**Key insight:** Citation commands can have multiple keys: `\cite{key1,key2,key3}`. Each key must be tracked individually. Different citation commands (`\cite`, `\citep`, `\citet`, `\citealt`, `\nocite`) all reference bibliography entries.
**Example:**
```python
CITE_PATTERN = re.compile(r'\\(?:cite|citep|citet|citealt|nocite)\{([^}]+)\}')

def extract_citation_keys(content: str) -> Set[str]:
    """Extract all citation keys, handling multi-key citations."""
    keys = set()
    for match in CITE_PATTERN.finditer(content):
        key_str = match.group(1)
        # Split on commas for multi-key citations
        for key in key_str.split(','):
            key = key.strip()
            if key:
                keys.add(key)
    return keys

def extract_bibliography_decls(content: str) -> List[str]:
    """Extract \\bibliography{...} and \\printbibliography declarations."""
    results = []
    # \\bibliography{file}
    for match in re.finditer(r'\\bibliography\{([^}]+)\}', content):
        results.append(f"bibliography:{match.group(1)}")
    # \\printbibliography (biblatex)
    if re.search(r'\\printbibliography', content):
        results.append("printbibliography")
    return results
```

### Pattern 6: Float Environment Extraction
**What:** Extract complete figure, table, and longtable environments with their content.
**When to use:** For STRUCT-05 verification.
**Key insight:** Float environments use `\begin{env}...\end{env}` syntax. The content between can span many lines and include nested environments (e.g., `tabular` inside `table`). Environment depth tracking is required to correctly identify the end of each float.
**Example:**
```python
@dataclass
class FloatEnv:
    """A float environment (figure, table, or longtable)."""
    env_type: str     # "figure", "table", "longtable"
    content: str      # Full content including \\begin and \\end
    start_line: int   # Starting line number

def extract_floats(content: str) -> List[FloatEnv]:
    """Extract all float environments with depth tracking."""
    results = []
    lines = content.split('\n')

    # Patterns for float environment starts
    float_types = ['figure', 'table', 'longtable']
    start_pattern = re.compile(r'\\begin\{(' + '|'.join(float_types) + r')\}')

    i = 0
    while i < len(lines):
        match = start_pattern.search(lines[i])
        if match:
            env_type = match.group(1)
            # Track depth to find matching \\end
            depth = 1
            start_line = i + 1
            content_lines = [lines[i]]

            j = i + 1
            while j < len(lines) and depth > 0:
                line = lines[j]
                content_lines.append(line)
                # Count \\begin and \\end for this env type
                depth += line.count(f'\\begin{{{env_type}}}')
                depth -= line.count(f'\\end{{{env_type}}}')
                j += 1

            results.append(FloatEnv(
                env_type=env_type,
                content='\n'.join(content_lines),
                start_line=start_line
            ))
            i = j
        else:
            i += 1

    return results
```

### Pattern 7: Reuse STRUCTURES List from Phases 5 and 6
**What:** Copy the exact STRUCTURES list with file path mappings.
**When to use:** For consistency across all verification scripts.
**Key insight:** The same 5 structures, same original/modular path mappings. Add `inactive_files` field for pinn-architecture.
**Example (from verify_content.py):**
```python
@dataclass
class Structure:
    """Definition of a LaTeX structure to verify."""
    name: str
    original: Path
    modular: Path
    inactive_files: Optional[List[str]] = None

STRUCTURES = [
    Structure(
        name="Data-quality-assessment",
        original=Path("pinn_instruction/original_latex/Data-quality-assessment/old/data_quality_assess.tex"),
        modular=Path("pinn_instruction/original_latex/Data-quality-assessment/data_quality_assess/main-data-quality-assess.tex"),
    ),
    Structure(
        name="ctl-instruction",
        original=Path("pinn_instruction/original_latex/ctl-instruction/old/CTL-instruction-final.tex"),
        modular=Path("pinn_instruction/original_latex/ctl-instruction/ctl-instruction/main_CTL.tex"),
    ),
    Structure(
        name="pinn-architecture",
        original=Path("pinn_instruction/original_latex/pinn-architecture/old/PINN_architecture_plan.tex"),
        modular=Path("pinn_instruction/original_latex/pinn-architecture/pinn-architecture/main_pinn.tex"),
        inactive_files=["input_vector_inactive", "advanced_training_inactive", "consolidated_blueprint_inactive"],
    ),
    Structure(
        name="review_of_framework",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/review_of_ctl-pinn_framework.tex"),
        modular=Path("pinn_instruction/original_latex/review-of-framework/review_of_framework/review_of_framework.tex"),
    ),
    Structure(
        name="stage_strat_revision",
        original=Path("pinn_instruction/original_latex/review-of-framework/old/stage-strat-revision.tex"),
        modular=Path("pinn_instruction/original_latex/review-of-framework/stage_strat_revision/stage_strat_revision.tex"),
    ),
]
```

### Anti-Patterns to Avoid
- **Only checking labels exist in modular without checking refs:** STRUCT-02 and STRUCT-03 are separate for a reason. A label might exist but references to it might be missing.
- **Comparing float content character-by-character:** Whitespace differences don't affect LaTeX compilation. Use whitespace-normalized content comparison or difflib.
- **Treating `\include{}` same as `\input{}` for content:** While Phase 5's `resolve_includes()` handles both by expanding content, be aware that `\include` adds `\clearpage` in LaTeX compilation. For structural verification, content expansion is sufficient.
- **Reporting cross-reference errors:** Per D-09, we only check presence. Undefined references (refs to non-existent labels) are a Phase 8 compilation concern.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Environment depth tracking for floats | Complex state machine | Simple depth counter | LaTeX environments nest predictably; increment on `\begin{type}`, decrement on `\end{type}` |
| Set comparison for labels/refs | Ordered list comparison | Python set operations | Presence is order-independent; `original_labels - modular_labels` gives missing immediately |
| Float content comparison | Character-by-character diff | `difflib.unified_diff()` | Proven in Phase 5; handles whitespace-normalized comparison |

**Key insight:** Structural element extraction is regex-friendly because LaTeX commands follow predictable patterns. The complexity is in multi-line content extraction (floats), which requires depth tracking but is still straightforward.

## Common Pitfalls

### Pitfall 1: Optional Short Titles in Sections
**What goes wrong:** `\section[Short]{Long Title}` -- the optional `[Short]` argument is included in the title comparison, causing false mismatches.
**Why it happens:** A naive regex might capture the entire `\section[Short]{Long Title}` without distinguishing the optional argument.
**How to avoid:** The regex pattern must explicitly skip the optional `[...]` argument: `\\section(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}`. The capturing group only gets the main title.
**Warning signs:** Section titles appearing with bracket notation like "Short]Long Title" instead of "Long Title".

### Pitfall 2: Multi-Key Citations
**What goes wrong:** `\cite{key1,key2,key3}` is treated as a single citation key "key1,key2,key3" instead of three separate keys.
**Why it happens:** Naive extraction captures the entire brace content without splitting.
**How to avoid:** After extracting the citation key string, split on commas and strip whitespace from each part. Each part is a separate key.
**Warning signs:** Citation keys containing commas reported as missing, when individual keys exist.

### Pitfall 3: Nested Environments in Floats
**What goes wrong:** A `table` environment contains a `tabular` environment, and the depth tracking stops at the first `\end{table}` found inside `tabular` (which doesn't exist), causing extraction to run to end of file.
**Why it happens:** Different environment types have independent `\begin`/`\end` pairs. Tracking only `\begin{table}`/`\end{table}` depth is correct.
**How to avoid:** Track depth only for the specific environment type being extracted. A `tabular` inside a `table` does not affect the `table` depth counter.
**Warning signs:** Float content extending to end of file, or missing subsequent floats.

### Pitfall 4: Inactive Sections in pinn-architecture
**What goes wrong:** Labels defined in inactive sections (e.g., `input_vector_inactive.tex`) are reported as missing from modular output.
**Why it happens:** The modular main_pinn.tex has these sections commented out (`%\input{sections/input_vector_inactive}`), but the original file contains the content.
**How to avoid:** After resolving includes, check if the main.tex has commented-out `\input` directives for inactive files. Exclude structural elements from inactive files from the comparison. Or simpler: since Phase 5 D-04 already excludes inactive content from the diff, follow the same pattern.
**Warning signs:** Labels like `tab:training_hyperparameters` reported as missing when they're in an inactive section.

### Pitfall 5: Whitespace in Titles
**What goes wrong:** `\section{Introduction }` (trailing space) vs `\section{Introduction}` reported as different sections.
**Why it happens:** Whitespace is preserved in the extracted title.
**How to avoid:** Strip whitespace from extracted titles before comparison. Per D-06: "Strip whitespace from extracted titles before comparison".
**Warning signs:** Section titles reported as different when they appear identical visually.

### Pitfall 6: `\include` vs `\input` Handling
**What goes wrong:** ctl-instruction uses `\include{sections/01_intro}` which in LaTeX inserts `\clearpage`. The content assembly might not handle this correctly.
**Why it happens:** `\include` is semantically different from `\input` in LaTeX compilation (adds page break), but for content assembly, both just expand to included content.
**How to avoid:** Phase 5's `resolve_includes()` already handles both by treating them identically for content expansion. For structural verification, this is correct -- we're checking the content, not the page breaks.
**Warning signs:** Content from ctl-instruction sections not appearing in assembled output.

## Code Examples

Verified patterns from existing project code:

### Main Verification Loop
```python
def verify_structure(structure: Structure, base_path: Path, verbose: bool = False) -> Dict:
    """Verify a single structure for all STRUCT requirements.

    Returns dict with:
        passed: bool
        sections: dict with match status
        labels: dict with match status
        refs: dict with match status
        citations: dict with match status
        floats: dict with match status
    """
    original_path = base_path / structure.original
    modular_path = base_path / structure.modular

    # Read and resolve
    original_content = original_path.read_text(encoding='utf-8')
    original_content = normalize_line_endings(original_content)
    original_content = resolve_includes(original_content, original_path.parent)

    modular_content = modular_path.read_text(encoding='utf-8')
    modular_content = normalize_line_endings(modular_content)
    modular_content = resolve_includes(modular_content, modular_path.parent)

    # Extract and compare each category
    sections_result = compare_sections(
        extract_sections(original_content),
        extract_sections(modular_content)
    )

    labels_result = compare_sets(
        extract_labels(original_content),
        extract_labels(modular_content),
        category="labels"
    )

    refs_result = compare_sets(
        extract_refs(original_content),
        extract_refs(modular_content),
        category="refs"
    )

    citations_result = compare_citations(
        extract_citation_keys(original_content),
        extract_citation_keys(modular_content),
        extract_bibliography_decls(original_content),
        extract_bibliography_decls(modular_content)
    )

    floats_result = compare_floats(
        extract_floats(original_content),
        extract_floats(modular_content)
    )

    passed = (
        sections_result['match'] and
        labels_result['match'] and
        refs_result['match'] and
        citations_result['match'] and
        floats_result['match']
    )

    return {
        'passed': passed,
        'sections': sections_result,
        'labels': labels_result,
        'refs': refs_result,
        'citations': citations_result,
        'floats': floats_result,
    }
```

### Section Comparison with Side-by-Side Display
```python
def compare_sections(original: List[SectionHeading], modular: List[SectionHeading]) -> Dict:
    """Compare section hierarchies sequentially.

    Returns dict with:
        match: bool
        count_original: int
        count_modular: int
        differences: List of tuples (level, original_title, modular_title, issue)
    """
    differences = []

    # Sequential comparison
    max_len = max(len(original), len(modular))
    for i in range(max_len):
        orig = original[i] if i < len(original) else None
        mod = modular[i] if i < len(modular) else None

        if orig is None:
            differences.append((mod.level, None, mod.title, "extra in modular"))
        elif mod is None:
            differences.append((orig.level, orig.title, None, "missing in modular"))
        elif orig.level != mod.level:
            differences.append((orig.level, orig.title, mod.title, f"level mismatch: {orig.level} vs {mod.level}"))
        elif orig.title != mod.title:
            differences.append((orig.level, orig.title, mod.title, "title mismatch"))

    return {
        'match': len(differences) == 0,
        'count_original': len(original),
        'count_modular': len(modular),
        'differences': differences,
    }
```

## Concrete Structural Element Inventory (from source analysis)

The following is an inventory of structural elements found in the 5 structures, verified by grep analysis of actual files:

### Labels Found
| Structure | Labels | Examples |
|-----------|--------|----------|
| pinn-architecture | 3 | `tab:architectural_hyperparameters`, `tab:training_hyperparameters`, `tab:blueprint_summary` |
| ctl-instruction | 10+ | `tab:brutus_compare`, `sec:ctl:step3`, `item:eqs`, `item:lnorm`, `fig:step2_data_workflow` |
| review_of_framework | 2 | `tab:input_vector`, `tab:hyperparameter_schedule` |
| stage_strat_revision | 4 | `tab:invariants`, `tab:dataframe`, `tab:framework_comparison`, `tab:final_stages` |
| Data-quality-assessment | 1 | `tab:assessment_strategies` |

### Float Environments Found
| Structure | figure | table | longtable |
|-----------|--------|-------|-----------|
| pinn-architecture | 0 | 1 | 2 |
| ctl-instruction | 2 | 5 | 0 |
| review_of_framework | 0 | 2 | 1 |
| stage_strat_revision | 0 | 3 | 1 |
| Data-quality-assessment | 0 | 1 | 0 |

### Section Hierarchy Patterns
- All structures use `\section` and `\subsection`
- Some use `\subsubsection` and `\paragraph`
- stage_strat_revision uses `\part` for major divisions
- Optional short titles are rare but present (e.g., `\paragraph{Derivation:}`)

### Citation Variants
- `\cite{...}` - standard citation (all structures)
- `\citep{...}` - parenthetical citation (natbib style)
- `\citet{...}` - textual citation (natbib style)
- No `\citealt` or `\nocite` found in current files
- Multi-key citations: `\cite{ref8, ref10}` (comma-separated)

### Bibliography Declarations
- `\begin{thebibliography}{99}...\end{thebibliography}` (inline bibliography)
- `\bibliography{...}` (external .bib file - not found in these structures)
- `\printbibliography` (biblatex - not found in these structures)

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual visual inspection of section structure | Automated extraction and comparison | This phase | Consistent, repeatable, catches missing sections |
| Checking compilation for undefined references | Presence verification before compilation | This phase | Catches missing labels/refs before Phase 8 |
| Manual float counting | Automated extraction with depth tracking | This phase | Catches missing/altered floats reliably |

**Deprecated/outdated:**
- Line-by-line diffing for structural elements: False positives from whitespace, false negatives from reordering
- Manual section counting: Error-prone, doesn't detect title changes

## Open Questions

1. **Should we verify `\part` hierarchy in stage_strat_revision?**
   - What we know: stage_strat_revision uses `\part{...}` for major divisions, which is above `\section` in the hierarchy.
   - What's unclear: The CONTEXT.md D-04 lists only `\section`, `\subsection`, `\subsubsection`, `\paragraph`, `\subparagraph` -- not `\part`.
   - Recommendation: Include `\part` in the extraction pattern. It's a valid LaTeX sectioning command and should be verified for completeness.

2. **How to handle `\subparagraph`?**
   - What we know: Rarely used but valid LaTeX sectioning command.
   - What's unclear: Whether any of the 5 structures use it.
   - Recommendation: Include in the extraction pattern for completeness. If none use it, the extraction simply returns nothing.

3. **Should we verify `\caption` content within floats?**
   - What we know: Float content comparison (D-14) includes checking for "missing captions".
   - What's unclear: Whether caption text should be compared verbatim or just presence checked.
   - Recommendation: The full float content comparison using difflib will naturally catch caption differences. No special handling needed.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None (standalone scripts) |
| Config file | None -- scripts are self-contained |
| Quick run command | `python pinn_instruction/original_latex/verification/verify_structure.py --structure pinn -v` |
| Full suite command | `python pinn_instruction/original_latex/verification/verify_structure.py -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| STRUCT-01 | Section hierarchy matches | functional | `python verify_structure.py -v` | Wave 0 (to create) |
| STRUCT-02 | All labels present | functional | `python verify_structure.py -v` | Wave 0 (to create) |
| STRUCT-03 | All refs present | functional | `python verify_structure.py -v` | Wave 0 (to create) |
| STRUCT-04 | All citations preserved | functional | `python verify_structure.py -v` | Wave 0 (to create) |
| STRUCT-05 | All floats preserved | functional | `python verify_structure.py -v` | Wave 0 (to create) |

### Sampling Rate
- **Per task commit:** Run `python verify_structure.py --structure <name> -v` after script creation/modification
- **Per wave merge:** Run full verification for all structures
- **Phase gate:** All 5 structures pass all 5 STRUCT checks before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `pinn_instruction/original_latex/verification/verify_structure.py` -- main verification script
- [ ] Framework install: None needed -- uses only Python built-ins

## Sources

### Primary (HIGH confidence)
- Direct grep analysis of all 5 original monolithic .tex files and modular files for structural elements
- Phase 5 research (05-CONTEXT.md) and implementation (verify_content.py) -- established patterns for structure definitions, file resolution, and report generation
- Phase 6 research (06-RESEARCH.md) and implementation (verify_preamble.py) -- established patterns for brace-depth tracking and config block extraction

### Secondary (MEDIUM confidence)
- LaTeX sectioning command syntax -- standard LaTeX behavior for optional short titles and section hierarchy
- LaTeX citation command syntax -- natbib and standard `\cite` variants

### Tertiary (LOW confidence)
- None -- all findings verified from actual project files

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- Python built-ins only, identical to Phases 5 and 6
- Architecture: HIGH -- Reuses proven patterns from Phases 5 and 6; structural elements are straightforward to extract
- Pitfalls: HIGH -- Identified from concrete file structure analysis (optional short titles, multi-key citations, nested environments, inactive sections)

**Research date:** 2026-03-21
**Valid until:** 30 days (stable Python libraries, LaTeX files unlikely to change significantly)