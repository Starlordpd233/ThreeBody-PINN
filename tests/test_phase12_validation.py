#!/usr/bin/env python3
"""
Phase 12 Validation Tests

Automated verification for the PINN Architecture Verification phase.
Checks structural properties of generated artifacts against plan requirements.

Run: python3 tests/test_phase12_validation.py
"""

import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to Phase 12 artifacts
ARCHITECTURE_MD = os.path.join(PROJECT_ROOT, "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md")
# REPORT_MD was pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md.
# The report artifact was retired after v1.3 closure; report-only checks remain skipped.
INDEX_MD = os.path.join(PROJECT_ROOT, "pinn_instruction/markdown_conversion/README.md")

# Inactive terms that should NOT appear in the faithful converted body.
# Note: "Consolidated Implementation Blueprint" is excluded because it
# appears in the active Section 6 (blueprint_summary.tex) table caption.
INACTIVE_TERMS = [
    "Input Vector Formulation",
    "14-dimensional injective",
    "Advanced Training Dynamics",
    "Curriculum-Aware Energy Regularization",
]

results = {"pass": 0, "fail": 0, "errors": []}


def check(name, condition, detail=""):
    if condition:
        results["pass"] += 1
        print(f"  PASS: {name}")
    else:
        results["fail"] += 1
        msg = f"  FAIL: {name}"
        if detail:
            msg += f" ({detail})"
        print(msg)
        results["errors"].append(msg)


def test_clean_01_authoritative_markdown_exists():
    """CLEAN-01: Single authoritative markdown at target path."""
    check("CLEAN-01: pinn_architecture.md exists", os.path.isfile(ARCHITECTURE_MD))
    if os.path.isfile(ARCHITECTURE_MD):
        check("CLEAN-01: pinn_architecture.md > 200 lines",
              len(open(ARCHITECTURE_MD).readlines()) >= 200)


def test_clean_03_report_structure():
    """CLEAN-03: Verification report has all required sections. (SKIPPED: report artifact retired after v1.3 closure)"""
    print("  SKIP: CLEAN-03 — verification report artifact retired after v1.3 closure")
    return
    if not os.path.isfile(REPORT_MD):
        check("CLEAN-03: report exists", False)
        return

    content = open(REPORT_MD).read()
    required_sections = [
        "## Candidate Comparison",
        "## Selected Baseline",
        "## Excluded Inactive Sections",
        "## Section Audit",
        "## Fix Log",
        "## Source Issues",
        "## Final Verification",
    ]
    for section in required_sections:
        check(f"CLEAN-03: report has '{section}'", section in content)

    check("CLEAN-03: zero PENDING audits",
          "PENDING" not in content or content.count("PENDING") == 0,
          f"found {content.count('PENDING')} PENDING")

    check("CLEAN-03: D-38 explicit text present",
          "All 3 inactive sections (input_vector_inactive.tex, advanced_training_inactive.tex, consolidated_blueprint_inactive.tex) are confirmed absent" in content)


def test_cand_01_candidate_comparison():
    """CAND-01: Candidate comparison with F1/recall scores. (SKIPPED: report artifact retired after v1.3 closure)"""
    print("  SKIP: CAND-01 — verification report artifact retired after v1.3 closure")
    return
    if not os.path.isfile(REPORT_MD):
        check("CAND-01: report exists", False)
        return
    content = open(REPORT_MD).read()
    check("CAND-01: Candidate Comparison section exists",
          "## Candidate Comparison" in content)
    check("CAND-01: F1 mentioned in comparison",
          "F1" in content)
    check("CAND-01: recall mentioned in comparison",
          "recall" in content.lower())


def test_audit_01_section_audits():
    """AUDIT-01: 7 section audit subsections in report. (SKIPPED: report artifact retired after v1.3 closure)"""
    print("  SKIP: AUDIT-01 — verification report artifact retired after v1.3 closure")
    return
    if not os.path.isfile(REPORT_MD):
        check("AUDIT-01: report exists", False)
        return
    content = open(REPORT_MD).read()
    sections = [
        "foundational_principles",
        "sqr_skipresnet_siren_backbone",
        "physics_constrained_loss",
        "training_optimization",
        "inference_and_output",
        "blueprint_summary",
        "bibliography",
    ]
    for sec in sections:
        check(f"AUDIT-01: section audit for {sec}",
              sec in content)


def test_audit_02_fix_log():
    """AUDIT-02: Fix log has discrepancy entries. (SKIPPED: report artifact retired after v1.3 closure)"""
    print("  SKIP: AUDIT-02 — verification report artifact retired after v1.3 closure")
    return
    if not os.path.isfile(REPORT_MD):
        check("AUDIT-02: report exists", False)
        return
    content = open(REPORT_MD).read()
    check("AUDIT-02: Fix Log section exists", "## Fix Log" in content)
    # Look for fix log entries with PINN-12- prefix
    fixes = re.findall(r"PINN-12-\d{2}-\d+", content)
    check("AUDIT-02: fix log has entries", len(fixes) > 0,
          f"found {len(fixes)} fix entries")


def test_audit_03_inactive_exclusion():
    """AUDIT-03: Inactive section exclusion documented. (SKIPPED: report artifact retired after v1.3 closure)"""
    print("  SKIP: AUDIT-03 — verification report artifact retired after v1.3 closure")
    return
    if not os.path.isfile(REPORT_MD):
        check("AUDIT-03: report exists", False)
        return
    content = open(REPORT_MD).read()
    check("AUDIT-03: Excluded Inactive Sections present",
          "## Excluded Inactive Sections" in content)
    check("AUDIT-03: 3 inactive files listed",
          "input_vector_inactive" in content and
          "advanced_training_inactive" in content and
          "consolidated_blueprint_inactive" in content)


def test_fidel_05_section_hierarchy():
    """FIDEL-05: Numbered framework sections appear in source order."""
    if not os.path.isfile(ARCHITECTURE_MD):
        check("FIDEL-05: markdown exists", False)
        return
    lines = open(ARCHITECTURE_MD).readlines()
    # Find top-level headings outside code blocks
    in_code = False
    headings = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if not in_code and line.startswith("# "):
            headings.append((i, line.rstrip()))

    section_headings = [h for h in headings if re.match(r"# \d+\.", h[1])]
    expected = ["# 1.", "# 2.", "# 3.", "# 4.", "# 5.", "# 10."]
    check("FIDEL-05: current numbered section headings",
          len(section_headings) == len(expected),
          f"found {len(section_headings)}")

    for i, exp in enumerate(expected):
        if i < len(section_headings):
            check(f"FIDEL-05: {exp} present",
                  section_headings[i][1].startswith(exp),
                  f"got: {section_headings[i][1]}")


def test_fidel_06_inactive_content_absent():
    """FIDEL-06: Inactive content absent from markdown."""
    if not os.path.isfile(ARCHITECTURE_MD):
        check("FIDEL-06: markdown exists", False)
        return
    content = open(ARCHITECTURE_MD).read()

    # Exclude the Source Issues metadata section from this check (D-19)
    body = content
    if "## Source Issues / Notes for Future Reconciliation" in content:
        body = content.split("## Source Issues / Notes for Future Reconciliation")[0]

    for term in INACTIVE_TERMS:
        count = body.count(term)
        check(f"FIDEL-06: '{term}' absent from faithful body",
              count == 0, f"found {count} occurrences")


def test_cross_01_source_issues():
    """CROSS-01: Source Issues metadata appended."""
    if not os.path.isfile(ARCHITECTURE_MD):
        check("CROSS-01: markdown exists", False)
        return
    content = open(ARCHITECTURE_MD).read()
    check("CROSS-01: Source Issues section present",
          "## Source Issues / Notes for Future Reconciliation" in content)


def test_fidel_03_bibliography():
    """FIDEL-03: References section present with entries."""
    if not os.path.isfile(ARCHITECTURE_MD):
        check("FIDEL-03: markdown exists", False)
        return
    lines = open(ARCHITECTURE_MD).readlines()
    in_code = False
    in_bib = False
    bib_entries = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if not in_code and line.startswith("## References"):
            in_bib = True
            continue
        if in_bib and re.match(r"^\[\d+\]\s", stripped):
            bib_entries += 1

    check("FIDEL-03: References section present", in_bib)
    check("FIDEL-03: References has entries", bib_entries > 0,
          f"found {bib_entries} lines")


def test_cross_02_index_updated():
    """CROSS-02: Conversion index updated with Phase 12 row."""
    if not os.path.isfile(INDEX_MD):
        check("CROSS-02: index exists", False)
        return
    content = open(INDEX_MD).read()
    check("CROSS-02: Phase 12 row in index",
          "PINN Architecture" in content or "pinn_architecture" in content)


def main():
    print("=" * 60)
    print("Phase 12 Validation Tests")
    print("=" * 60)

    test_clean_01_authoritative_markdown_exists()
    test_clean_03_report_structure()
    test_cand_01_candidate_comparison()
    test_audit_01_section_audits()
    test_audit_02_fix_log()
    test_audit_03_inactive_exclusion()
    test_fidel_05_section_hierarchy()
    test_fidel_06_inactive_content_absent()
    test_cross_01_source_issues()
    test_fidel_03_bibliography()
    test_cross_02_index_updated()

    print("\n" + "=" * 60)
    print(f"Results: {results['pass']} passed, {results['fail']} failed")
    print("=" * 60)

    if results["fail"] > 0:
        print("\nFailures:")
        for err in results["errors"]:
            print(err)
        sys.exit(1)
    else:
        print("\nAll checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
