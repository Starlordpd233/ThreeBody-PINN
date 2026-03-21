#!/usr/bin/env python3
"""
verify_structure.py

Phase 7: Structure Fidelity Verification
Verifies that structural LaTeX elements -- section hierarchy, labels, references,
citations, and float environments -- are faithfully preserved in the modular
sections for all 5 structures.

Covers:
  - STRUCT-01: Section/subsection hierarchy
  - STRUCT-02: \\label declarations
  - STRUCT-03: \\ref, \\eqref, \\autoref references
  - STRUCT-04: \\cite commands and bibliography declarations
  - STRUCT-05: Float environments (figure, table, longtable)

Usage:
    python verify_structure.py                    # Verify all 5 structures
    python verify_structure.py --structure pinn   # Verify specific structure
    python verify_structure.py --output report.md # Custom output path
    python verify_structure.py --verbose          # Show progress
"""

import re
import argparse
from pathlib import Path
from difflib import unified_diff
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict, Set
from datetime import datetime


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Structure:
    """Definition of a LaTeX structure to verify."""
    name: str
    original: Path
    modular: Path
    sections_dir: str = "sections"
    inactive_files: Optional[List[str]] = None


@dataclass
class SectionHeading:
    """A section heading with its level and title."""
    level: str      # "part", "section", "subsection", "subsubsection", "paragraph", "subparagraph"
    title: str      # The title text (without optional short title)
    line_num: int   # Line number in source (for reporting)


@dataclass
class FloatEnv:
    """A float environment (figure, table, or longtable)."""
    env_type: str     # "figure", "table", "longtable"
    content: str      # Full content including \\begin and \\end
    start_line: int   # Starting line number


# ---------------------------------------------------------------------------
# Structure definitions (all 5) - copied verbatim from verify_content.py
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def normalize_line_endings(content: str) -> str:
    """Normalize to Unix line endings.

    Args:
        content: Text content with potentially mixed line endings

    Returns:
        Content with all line endings normalized to LF
    """
    return content.replace('\r\n', '\n').replace('\r', '\n')


def resolve_includes(content: str, base_dir: Path, depth: int = 0) -> str:
    """Recursively resolve \\input{} and \\include{} directives.

    Per D-03: Full recursive reassembly - resolve all \\input{}/\\include{}
    to produce flat file.

    Args:
        content: LaTeX content with include directives
        base_dir: Directory containing the main.tex file
        depth: Recursion depth (prevents infinite loops, max 10)

    Returns:
        Flat content with all includes resolved
    """
    if depth > 10:  # Safety limit per research pitfall
        return content

    # Match \input{file} or \include{file}
    # Pattern captures: leading whitespace, full command, path, trailing whitespace
    pattern = re.compile(r'^(\s*)(\\(?:input|include)\{([^}]+)\})(\s*)$', re.MULTILINE)

    def replace_include(match: re.Match) -> str:
        full_match = match.group(2)
        include_path = match.group(3)
        # Add .tex extension if not present
        if not include_path.endswith('.tex'):
            include_path += '.tex'

        file_path = base_dir / include_path
        if not file_path.exists():
            # Return original if file not found (preserve for error reporting)
            return full_match

        included_content = file_path.read_text(encoding='utf-8')
        included_content = normalize_line_endings(included_content)
        # Recursively resolve includes in the included file
        # Note: per research pitfall #6, we do NOT add \\clearpage for \\include{}
        return resolve_includes(included_content, file_path.parent, depth + 1)

    return pattern.sub(replace_include, content)


def strip_comments(content: str) -> str:
    """Remove LaTeX comment lines (lines starting with %).

    Args:
        content: LaTeX content with comment lines

    Returns:
        Content with comment lines removed
    """
    lines = content.split('\n')
    return '\n'.join(line for line in lines if not line.strip().startswith('%'))


# ---------------------------------------------------------------------------
# Section hierarchy extraction (STRUCT-01) - per D-04, D-05, D-06
# ---------------------------------------------------------------------------

# Regex pattern for sectioning commands including \part (per RESEARCH.md open question #1)
SECTION_PATTERN = re.compile(
    r'\\(part|section|subsection|subsubsection|paragraph|subparagraph)'
    r'(?:\s*\[[^\]]*\])?'  # Optional short title [Short]
    r'\s*\{([^}]+)\}',      # Main title {Title}
    re.MULTILINE
)


def extract_sections(content: str) -> List[SectionHeading]:
    """Extract all section headings with their levels and titles.

    Per D-04: Extract ordered flat list of sectioning commands.
    Per D-06: Strip whitespace from extracted titles before comparison.

    Args:
        content: LaTeX content to extract sections from

    Returns:
        Ordered list of SectionHeading objects
    """
    results = []
    for match in SECTION_PATTERN.finditer(content):
        level = match.group(1)
        title = match.group(2).strip()  # Strip whitespace per D-06
        # Count line number from content start
        line_num = content[:match.start()].count('\n') + 1
        results.append(SectionHeading(level=level, title=title, line_num=line_num))
    return results


# ---------------------------------------------------------------------------
# Label extraction (STRUCT-02) - per D-07
# ---------------------------------------------------------------------------

LABEL_PATTERN = re.compile(r'\\label\{([^}]+)\}')


def extract_labels(content: str) -> Set[str]:
    """Extract all \\label declarations, deduplicated.

    Per D-07: Extract all \\label{...} declarations from original;
    verify each appears in modular assembled content.

    Args:
        content: LaTeX content to extract labels from

    Returns:
        Deduplicated set of label strings
    """
    return set(match.group(1).strip() for match in LABEL_PATTERN.finditer(content))


# ---------------------------------------------------------------------------
# Reference extraction (STRUCT-03) - per D-08, D-09
# ---------------------------------------------------------------------------

REF_PATTERN = re.compile(r'\\(?:ref|eqref|autoref)\{([^}]+)\}')


def extract_refs(content: str) -> Set[str]:
    """Extract all \\ref, \\eqref, \\autoref references, deduplicated.

    Per D-08: Extract all \\ref{...}, \\eqref{...}, \\autoref{...} from original.
    Per D-09: Only check presence -- do not verify cross-reference validity.

    Args:
        content: LaTeX content to extract references from

    Returns:
        Deduplicated set of reference strings
    """
    return set(match.group(1).strip() for match in REF_PATTERN.finditer(content))


# ---------------------------------------------------------------------------
# Citation extraction (STRUCT-04) - per D-10, D-11, D-12
# ---------------------------------------------------------------------------

CITE_PATTERN = re.compile(r'\\(?:cite|citep|citet|citealt|nocite)\{([^}]+)\}')
BIBLIOGRAPHY_PATTERN = re.compile(r'\\bibliography\{([^}]+)\}')
PRINTBIB_PATTERN = re.compile(r'\\printbibliography')
THEBIBLIOGRAPHY_PATTERN = re.compile(r'\\begin\{thebibliography\}')


def extract_citation_keys(content: str) -> Set[str]:
    """Extract all citation keys, handling multi-key citations.

    Per D-10: Extract all \\cite{...}, \\citep{...}, \\citet{...},
    \\citealt{...}, \\nocite{...} from original.
    Per D-12: For multi-key citations, split on commas and track each key individually.

    Args:
        content: LaTeX content to extract citation keys from

    Returns:
        Deduplicated set of citation key strings
    """
    keys = set()
    for match in CITE_PATTERN.finditer(content):
        key_str = match.group(1)
        # Split on commas for multi-key citations per D-12
        for key in key_str.split(','):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


def extract_bibliography_decls(content: str) -> List[str]:
    """Extract \\bibliography{...}, \\printbibliography, and thebibliography declarations.

    Per D-11: Extract \\bibliography{...} and \\printbibliography declarations.

    Args:
        content: LaTeX content to extract bibliography declarations from

    Returns:
        List of declaration strings (e.g., "bibliography:file", "printbibliography", "thebibliography")
    """
    results = []

    # \\bibliography{file}
    for match in BIBLIOGRAPHY_PATTERN.finditer(content):
        results.append(f"bibliography:{match.group(1)}")

    # \\printbibliography (biblatex)
    if PRINTBIB_PATTERN.search(content):
        results.append("printbibliography")

    # \\begin{thebibliography} (inline bibliography)
    if THEBIBLIOGRAPHY_PATTERN.search(content):
        results.append("thebibliography")

    return results


# ---------------------------------------------------------------------------
# Float environment extraction (STRUCT-05) - per D-13, D-14, D-15
# ---------------------------------------------------------------------------

FLOAT_TYPES = ['figure', 'table', 'longtable']


def extract_floats(content: str) -> List[FloatEnv]:
    """Extract all float environments with depth tracking.

    Per D-13: Extract full content of each \\begin{figure}...\\end{figure},
    \\begin{table}...\\end{table}, \\begin{longtable}...\\end{longtable} block.
    Per D-15: Use environment depth tracking (same pattern as Phase 6 config block extraction).

    Args:
        content: LaTeX content to extract floats from

    Returns:
        List of FloatEnv objects with full content including begin/end markers
    """
    results = []
    lines = content.split('\n')

    # Pattern for float environment starts
    start_pattern = re.compile(r'\\begin\{(' + '|'.join(FLOAT_TYPES) + r')\}')

    i = 0
    while i < len(lines):
        match = start_pattern.search(lines[i])
        if match:
            env_type = match.group(1)
            # Track depth to find matching \\end per D-15 and pitfall #3
            # Only track depth for this specific env type
            depth = 1
            start_line = i + 1
            content_lines = [lines[i]]

            j = i + 1
            while j < len(lines) and depth > 0:
                line = lines[j]
                content_lines.append(line)
                # Count \\begin and \\end for this env type only
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


# ---------------------------------------------------------------------------
# Comparison functions
# ---------------------------------------------------------------------------

def compare_sections(original: List[SectionHeading], modular: List[SectionHeading]) -> Dict:
    """Compare section hierarchies sequentially.

    Per D-05: Compare sequentially -- report any ordering differences,
    missing sections, or extra sections. Side-by-side display for easy human review.

    Args:
        original: Sections from original content
        modular: Sections from modular content

    Returns:
        Dict with keys: match, count_original, count_modular, differences
    """
    differences = []

    # Sequential comparison per D-05
    max_len = max(len(original), len(modular))
    for i in range(max_len):
        orig = original[i] if i < len(original) else None
        mod = modular[i] if i < len(modular) else None

        if orig is None:
            differences.append({
                'level': mod.level,
                'original_title': None,
                'modular_title': mod.title,
                'issue': "extra in modular"
            })
        elif mod is None:
            differences.append({
                'level': orig.level,
                'original_title': orig.title,
                'modular_title': None,
                'issue': "missing in modular"
            })
        elif orig.level != mod.level:
            differences.append({
                'level': orig.level,
                'original_title': orig.title,
                'modular_title': mod.title,
                'issue': f"level mismatch: {orig.level} vs {mod.level}"
            })
        elif orig.title != mod.title:
            differences.append({
                'level': orig.level,
                'original_title': orig.title,
                'modular_title': mod.title,
                'issue': "title mismatch"
            })

    return {
        'match': len(differences) == 0,
        'count_original': len(original),
        'count_modular': len(modular),
        'differences': differences,
    }


def compare_sets(original: Set[str], modular: Set[str], category: str) -> Dict:
    """Compare sets of labels, refs, or citation keys.

    Args:
        original: Set from original content
        modular: Set from modular content
        category: Category name for reporting

    Returns:
        Dict with keys: match, count_original, count_modular, missing, extra
    """
    missing = sorted(original - modular)
    extra = sorted(modular - original)

    return {
        'match': len(missing) == 0 and len(extra) == 0,
        'count_original': len(original),
        'count_modular': len(modular),
        'missing': missing,
        'extra': extra,
    }


def compare_citations(orig_keys: Set[str], mod_keys: Set[str],
                      orig_bib: List[str], mod_bib: List[str]) -> Dict:
    """Compare citation keys and bibliography declarations.

    Args:
        orig_keys: Citation keys from original
        mod_keys: Citation keys from modular
        orig_bib: Bibliography declarations from original
        mod_bib: Bibliography declarations from modular

    Returns:
        Dict with keys: match, keys_result, bib_result
    """
    keys_result = compare_sets(orig_keys, mod_keys, "citation_keys")

    # Bibliography declarations comparison
    missing_bib = [b for b in orig_bib if b not in mod_bib]
    extra_bib = [b for b in mod_bib if b not in orig_bib]

    bib_result = {
        'match': len(missing_bib) == 0 and len(extra_bib) == 0,
        'count_original': len(orig_bib),
        'count_modular': len(mod_bib),
        'missing': missing_bib,
        'extra': extra_bib,
    }

    return {
        'match': keys_result['match'] and bib_result['match'],
        'keys_result': keys_result,
        'bib_result': bib_result,
    }


def normalize_float_content(content: str) -> str:
    """Normalize float content for comparison.

    Strips trailing whitespace per line, collapses blank lines.

    Args:
        content: Float environment content

    Returns:
        Normalized content string
    """
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    # Collapse multiple blank lines to single
    result = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return '\n'.join(result)


def compare_floats(original: List[FloatEnv], modular: List[FloatEnv]) -> Dict:
    """Compare float environments between original and modular.

    Per D-14: Compare float count per type (must match); compare full content
    of each float using difflib -- flag any content differences.

    Args:
        original: Floats from original content
        modular: Floats from modular content

    Returns:
        Dict with keys: match, counts_by_type, content_differences
    """
    # Count by type
    orig_by_type: Dict[str, int] = {}
    mod_by_type: Dict[str, int] = {}
    for f in original:
        orig_by_type[f.env_type] = orig_by_type.get(f.env_type, 0) + 1
    for f in modular:
        mod_by_type[f.env_type] = mod_by_type.get(f.env_type, 0) + 1

    # Check counts match per D-14
    all_types = set(orig_by_type.keys()) | set(mod_by_type.keys())
    count_match = all(orig_by_type.get(t, 0) == mod_by_type.get(t, 0) for t in all_types)

    # Content comparison using difflib per D-14
    content_differences = []

    if len(original) == len(modular):
        # Compare floats in order, by type
        for i, (orig_f, mod_f) in enumerate(zip(original, modular)):
            if orig_f.env_type != mod_f.env_type:
                content_differences.append({
                    'index': i,
                    'issue': f"type mismatch: {orig_f.env_type} vs {mod_f.env_type}"
                })
            else:
                orig_norm = normalize_float_content(orig_f.content)
                mod_norm = normalize_float_content(mod_f.content)
                if orig_norm != mod_norm:
                    diff_lines = list(unified_diff(
                        orig_norm.split('\n'),
                        mod_norm.split('\n'),
                        fromfile=f'original/{orig_f.env_type}[{i}]',
                        tofile=f'modular/{mod_f.env_type}[{i}]',
                        lineterm=''
                    ))
                    content_differences.append({
                        'index': i,
                        'env_type': orig_f.env_type,
                        'issue': 'content mismatch',
                        'diff': '\n'.join(diff_lines)
                    })
    else:
        # Count mismatch - report as difference
        content_differences.append({
            'index': 0,
            'issue': f"float count mismatch: {len(original)} vs {len(modular)}"
        })

    return {
        'match': count_match and len(content_differences) == 0,
        'counts_original': orig_by_type,
        'counts_modular': mod_by_type,
        'count_match': count_match,
        'content_differences': content_differences,
    }


# ---------------------------------------------------------------------------
# Inactive section handling (per D-16)
# ---------------------------------------------------------------------------

def get_inactive_content(main_content: str, base_dir: Path, inactive_files: List[str]) -> str:
    """Extract content from inactive section files.

    Per D-16: For pinn-architecture, exclude structural elements from inactive files.
    This function extracts the content from inactive files for comparison exclusion.

    Args:
        main_content: Content of the main.tex file
        base_dir: Directory containing main.tex
        inactive_files: List of inactive file names (without .tex extension)

    Returns:
        Concatenated content from all inactive section files
    """
    inactive_content = []

    for inactive_name in inactive_files:
        # Look for commented-out include: %\input{sections/...} or %\include{sections/...}
        pattern = re.compile(
            rf'%\s*\\(?:input|include)\{{sections/{re.escape(inactive_name)}(?:\.tex)?\}}',
            re.MULTILINE
        )
        if pattern.search(main_content):
            # This is indeed an inactive section, read its content
            inactive_path = base_dir / "sections" / f"{inactive_name}.tex"
            if inactive_path.exists():
                content = inactive_path.read_text(encoding='utf-8')
                inactive_content.append(content)

    return '\n'.join(inactive_content)


# ---------------------------------------------------------------------------
# Main verification function
# ---------------------------------------------------------------------------

def verify_structure(structure: Structure, base_path: Path, verbose: bool = False) -> Dict:
    """Verify a single structure for all STRUCT requirements.

    Args:
        structure: Structure definition with paths
        base_path: Project root directory
        verbose: Print progress information

    Returns:
        Dict with all comparison results and pass/fail status
    """
    original_path = base_path / structure.original
    modular_path = base_path / structure.modular

    # 1. Read and resolve original content
    original_content = original_path.read_text(encoding='utf-8')
    original_content = normalize_line_endings(original_content)
    original_content = resolve_includes(original_content, original_path.parent)

    # 2. Read and resolve modular content
    modular_content = modular_path.read_text(encoding='utf-8')
    modular_content = normalize_line_endings(modular_content)
    modular_content = resolve_includes(modular_content, modular_path.parent)

    # 3. Handle inactive sections per D-16
    if structure.inactive_files:
        # Get inactive content to exclude from comparison
        inactive_content = get_inactive_content(
            modular_path.read_text(encoding='utf-8'),
            modular_path.parent,
            structure.inactive_files
        )
        if inactive_content:
            # Extract labels/refs from inactive content and remove from modular comparison
            inactive_labels = extract_labels(inactive_content)
            inactive_refs = extract_refs(inactive_content)
            inactive_cites = extract_citation_keys(inactive_content)
            if verbose and (inactive_labels or inactive_refs or inactive_cites):
                print(f"    Excluding inactive elements: {len(inactive_labels)} labels, "
                      f"{len(inactive_refs)} refs, {len(inactive_cites)} citations")

    # 4. Extract structural elements
    orig_sections = extract_sections(original_content)
    mod_sections = extract_sections(modular_content)

    orig_labels = extract_labels(original_content)
    mod_labels = extract_labels(modular_content)

    orig_refs = extract_refs(original_content)
    mod_refs = extract_refs(modular_content)

    orig_cites = extract_citation_keys(original_content)
    mod_cites = extract_citation_keys(modular_content)

    orig_bib = extract_bibliography_decls(original_content)
    mod_bib = extract_bibliography_decls(modular_content)

    orig_floats = extract_floats(original_content)
    mod_floats = extract_floats(modular_content)

    # 5. Handle inactive sections: remove inactive elements from modular comparison
    # We want to check: all original elements are in modular (minus inactive)
    if structure.inactive_files and inactive_content:
        # Remove inactive elements from what we expect in modular
        mod_labels = mod_labels - inactive_labels
        mod_refs = mod_refs - inactive_refs
        mod_cites = mod_cites - inactive_cites

    # 6. Compare each category
    sections_result = compare_sections(orig_sections, mod_sections)
    labels_result = compare_sets(orig_labels, mod_labels, "labels")
    refs_result = compare_sets(orig_refs, mod_refs, "refs")
    citations_result = compare_citations(orig_cites, mod_cites, orig_bib, mod_bib)
    floats_result = compare_floats(orig_floats, mod_floats)

    # 7. Determine overall pass/fail
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
        'counts': {
            'sections_original': len(orig_sections),
            'sections_modular': len(mod_sections),
            'labels_original': len(orig_labels),
            'labels_modular': len(mod_labels),
            'refs_original': len(orig_refs),
            'refs_modular': len(mod_refs),
            'cites_original': len(orig_cites),
            'cites_modular': len(mod_cites),
            'floats_original': len(orig_floats),
            'floats_modular': len(mod_floats),
        },
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(results: List[Tuple[Structure, Dict]]) -> str:
    """Generate a Markdown structure verification report.

    Per D-17, D-18: Markdown output with summary table and per-structure details.

    Args:
        results: List of (structure, result_dict) tuples

    Returns:
        Complete Markdown report string
    """
    lines = []
    lines.append("# Structure Fidelity Verification Report\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Structures verified:** {len(results)}\n")

    # Summary table per D-18
    lines.append("## Summary\n")
    lines.append("| Structure | Sections | Labels | Refs | Citations | Floats | Status |")
    lines.append("|-----------|----------|--------|------|-----------|--------|--------|")
    for structure, result in results:
        c = result['counts']
        status = "PASS" if result['passed'] else "FAIL"

        # Sections status
        sec_status = f"{c['sections_modular']}/{c['sections_original']}"
        if not result['sections']['match']:
            sec_status += " MISMATCH"

        # Labels status
        lbl_status = f"{c['labels_modular']}/{c['labels_original']}"
        if not result['labels']['match']:
            lbl_status += " MISMATCH"

        # Refs status
        ref_status = f"{c['refs_modular']}/{c['refs_original']}"
        if not result['refs']['match']:
            ref_status += " MISMATCH"

        # Citations status
        cite_status = f"{c['cites_modular']}/{c['cites_original']}"
        if not result['citations']['match']:
            cite_status += " MISMATCH"

        # Floats status
        float_status = f"{c['floats_modular']}/{c['floats_original']}"
        if not result['floats']['match']:
            float_status += " MISMATCH"

        lines.append(
            f"| {structure.name} "
            f"| {sec_status} "
            f"| {lbl_status} "
            f"| {ref_status} "
            f"| {cite_status} "
            f"| {float_status} "
            f"| {status} |"
        )
    lines.append("")

    # Detailed results per D-18
    lines.append("## Detailed Results\n")
    for structure, result in results:
        lines.append(f"### {structure.name}\n")

        # Note inactive sections if any
        if structure.inactive_files:
            lines.append(f"**Inactive sections excluded:** {', '.join(structure.inactive_files)}\n")

        # Sections (STRUCT-01)
        sec = result['sections']
        lines.append("#### Section Hierarchy (STRUCT-01)\n")
        lines.append(f"- Original: {sec['count_original']} sections")
        lines.append(f"- Modular: {sec['count_modular']} sections")
        if sec['match']:
            lines.append("- **Status:** MATCH\n")
        else:
            lines.append(f"- **Status:** MISMATCH ({len(sec['differences'])} differences)\n")
            # Side-by-side display per D-05
            lines.append("| # | Level | Original Title | Modular Title | Issue |")
            lines.append("|---|-------|----------------|---------------|-------|")
            for i, diff in enumerate(sec['differences']):
                lines.append(
                    f"| {i+1} "
                    f"| {diff['level']} "
                    f"| {diff['original_title'] or '(none)'} "
                    f"| {diff['modular_title'] or '(none)'} "
                    f"| {diff['issue']} |"
                )
            lines.append("")

        # Labels (STRUCT-02)
        lbl = result['labels']
        lines.append("#### Labels (STRUCT-02)\n")
        lines.append(f"- Original: {lbl['count_original']} labels")
        lines.append(f"- Modular: {lbl['count_modular']} labels")
        if lbl['match']:
            lines.append("- **Status:** MATCH\n")
        else:
            lines.append(f"- **Status:** MISMATCH\n")
            if lbl['missing']:
                lines.append(f"- **Missing in modular ({len(lbl['missing'])}):** {', '.join(lbl['missing'])}")
            if lbl['extra']:
                lines.append(f"- **Extra in modular ({len(lbl['extra'])}):** {', '.join(lbl['extra'])}")
            lines.append("")

        # References (STRUCT-03)
        ref = result['refs']
        lines.append("#### References (STRUCT-03)\n")
        lines.append(f"- Original: {ref['count_original']} references")
        lines.append(f"- Modular: {ref['count_modular']} references")
        if ref['match']:
            lines.append("- **Status:** MATCH\n")
        else:
            lines.append(f"- **Status:** MISMATCH\n")
            if ref['missing']:
                lines.append(f"- **Missing in modular ({len(ref['missing'])}):** {', '.join(ref['missing'])}")
            if ref['extra']:
                lines.append(f"- **Extra in modular ({len(ref['extra'])}):** {', '.join(ref['extra'])}")
            lines.append("")

        # Citations (STRUCT-04)
        cite = result['citations']
        lines.append("#### Citations & Bibliography (STRUCT-04)\n")
        keys = cite['keys_result']
        bib = cite['bib_result']
        lines.append(f"- Citation keys: {keys['count_original']} original, {keys['count_modular']} modular")
        lines.append(f"- Bibliography declarations: {bib['count_original']} original, {bib['count_modular']} modular")
        if cite['match']:
            lines.append("- **Status:** MATCH\n")
        else:
            lines.append(f"- **Status:** MISMATCH\n")
            if keys['missing']:
                lines.append(f"- **Missing citation keys ({len(keys['missing'])}):** {', '.join(keys['missing'])}")
            if keys['extra']:
                lines.append(f"- **Extra citation keys ({len(keys['extra'])}):** {', '.join(keys['extra'])}")
            if bib['missing']:
                lines.append(f"- **Missing bibliography declarations:** {', '.join(bib['missing'])}")
            if bib['extra']:
                lines.append(f"- **Extra bibliography declarations:** {', '.join(bib['extra'])}")
            lines.append("")

        # Floats (STRUCT-05)
        flt = result['floats']
        lines.append("#### Float Environments (STRUCT-05)\n")
        orig_counts = flt['counts_original']
        mod_counts = flt['counts_modular']
        lines.append(f"- Original: {sum(orig_counts.values())} floats ({orig_counts})")
        lines.append(f"- Modular: {sum(mod_counts.values())} floats ({mod_counts})")
        if flt['match']:
            lines.append("- **Status:** MATCH\n")
        else:
            lines.append(f"- **Status:** MISMATCH\n")
            if not flt['count_match']:
                lines.append("- **Count mismatch by type:**")
                for t in set(orig_counts.keys()) | set(mod_counts.keys()):
                    o = orig_counts.get(t, 0)
                    m = mod_counts.get(t, 0)
                    if o != m:
                        lines.append(f"  - {t}: {o} original vs {m} modular")
            for diff in flt['content_differences']:
                if 'diff' in diff:
                    lines.append(f"- **Content difference in {diff.get('env_type', 'float')} #{diff['index']}:**")
                    lines.append(f"```diff\n{diff['diff']}\n```\n")
                else:
                    lines.append(f"- **Issue:** {diff['issue']}\n")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Main entry point for structure fidelity verification.

    Returns:
        0 if all structures pass, 1 if any fail
    """
    parser = argparse.ArgumentParser(
        description='Verify structural LaTeX elements are preserved in modular sections.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python verify_structure.py                    # Verify all 5 structures
    python verify_structure.py --structure pinn   # Verify only pinn-architecture
    python verify_structure.py -v -o report.md    # Verbose with custom output
        """
    )
    parser.add_argument(
        '--structure', '-s',
        help='Verify specific structure (partial name match, e.g., "pinn" for pinn-architecture)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output report path (default: pinn_instruction/original_latex/verification/structure_verification_report.md)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show progress information'
    )
    args = parser.parse_args()

    # Determine base path (project root)
    base_path = Path(__file__).resolve().parent.parent.parent.parent

    # Default output path per D-17
    output_path = args.output or base_path / 'pinn_instruction/original_latex/verification/structure_verification_report.md'

    # Filter structures if specified
    structures = STRUCTURES
    if args.structure:
        structures = [s for s in STRUCTURES if args.structure.lower() in s.name.lower()]
        if not structures:
            print(f"No structures found matching '{args.structure}'")
            return 1

    # Verify each structure
    results = []
    for structure in structures:
        if args.verbose:
            print(f"Verifying: {structure.name}...")
        result = verify_structure(structure, base_path, verbose=args.verbose)
        results.append((structure, result))
        if args.verbose:
            status = "PASS" if result['passed'] else "FAIL"
            c = result['counts']
            print(f"  -> {status} (sections: {c['sections_modular']}/{c['sections_original']}, "
                  f"labels: {c['labels_modular']}/{c['labels_original']}, "
                  f"refs: {c['refs_modular']}/{c['refs_original']}, "
                  f"cites: {c['cites_modular']}/{c['cites_original']}, "
                  f"floats: {c['floats_modular']}/{c['floats_original']})")

    # Generate and write report
    report = generate_report(results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')

    if args.verbose:
        print(f"\nReport written to: {output_path}")

    # Exit code: 0 if all pass, 1 if any fail per D-19
    all_passed = all(r['passed'] for _, r in results)
    return 0 if all_passed else 1


if __name__ == '__main__':
    exit(main())