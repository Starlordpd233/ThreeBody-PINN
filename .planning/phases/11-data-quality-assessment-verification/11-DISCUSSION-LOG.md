# Phase 11: Data-Quality-Assessment Verification - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-05
**Phase:** 11-data-quality-assessment-verification
**Areas discussed:** Bibliography inclusion, HTML table correction, Authoritative filename, Report & archive layout, Section count & scope

---

## Bibliography Inclusion

| Option | Description | Selected |
|--------|-------------|----------|
| Strip all refs from body | Remove all [@refN] citations from markdown body to match LaTeX source exactly | ✓ |
| Keep refs, note as metadata | Keep citations but document in Source Issues appendix | |
| Include bibliography.tex as appendix | Keep body clean, append orphaned bibliography as separate section | |
| Exclude bibliography.tex | bibliography.tex is orphaned — never imported, not compiled | (initial recommendation) |

**User's choice:** Investigate further, then "Strip all refs from body"
**Notes:** Investigation revealed that both markdown candidates have reference material absent from the LaTeX source body (which has zero `\cite{}` commands). bibliography.tex has 33 `\bibitem` entries but is never `\input`'d by main.tex. The pandoc candidate injected 17 `[@refN]` citations into body text — a significant fidelity violation. The top-level candidate has a disconnected reference list at the end. Per one-to-one injection fidelity, the authoritative markdown body must match the LaTeX body exactly — zero citations.

**Follow-up decision (D-28):** bibliography.tex ignored completely. Not mentioned in verification report.

---

## HTML Table Correction

| Option | Description | Selected |
|--------|-------------|----------|
| Convert to markdown tables | Replace HTML tables with GitHub-flavored markdown, cell-by-cell verification against LaTeX | ✓ |
| Fix HTML in place | Correct HTML markup without format conversion | |
| Use pandoc table as reference | Use pandoc candidate's clean table as reference for correction | |

**User's choice:** Convert to markdown tables
**Notes:** The top-level candidate has a corrupted HTML table: "Risk Addressed" and "Blind Spot" rows are merged into one, values concatenated, missing spaces in headers. The pandoc candidate's table is clean. The 2 tables in `assessment_strategy.tex` are the only tables in the source.

---

## Authoritative Filename

| Option | Description | Selected |
|--------|-------------|----------|
| data_quality_assessment.md | Matches Phase 10 pattern — derived from LaTeX source directory name | ✓ |
| assess_data_quality.md | Reuse existing top-level candidate filename | |
| data_quality_assess.md | Reuse pandoc candidate filename | |

**User's choice:** data_quality_assessment.md
**Notes:** Consistent with Phase 10 naming convention (source directory → markdown filename). The source directory is `Data-quality-assessment`.

---

## Report & Archive Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Same as Phase 10 | Report next to authoritative file, archive under _archive/ | ✓ (adapted) |
| Separate reports dir | Reports in their own directory | |

**User's choice:** Same as Phase 10, but with a dedicated `verification_reports/` subdirectory
**Notes:** User created `pinn_instruction/markdown_conversion/verification_reports/` and moved Phase 10's report into it. README.md updated to point to the new path. This keeps `markdown_conversion/` clean as all 6 phases land. Phase 11 report goes to `verification_reports/data_quality_assessment_verification_report.md`. Archive goes to `_archive/data-quality-assessment/`.

---

## Section Count & Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Note as excluded orphan | Audit 6 sections, note bibliography.tex in report | |
| Audit it anyway | Include bibliography.tex as 7th audited section | |
| Ignore completely | Don't mention bibliography.tex at all | ✓ |

**User's choice:** Ignore completely
**Notes:** bibliography.tex is never imported by main.tex — it's not part of the compiled document. Audit covers 6 active sections only.

---

## Claude's Discretion

- Exact diff-score implementation and normalization details
- Exact markdown table format (GitHub-flavored)
- Exact verification report filename and structure within `verification_reports/`
- Exact discrepancy ID format
- Whether top-level or pandoc candidate wins mechanical diff scoring

## Deferred Ideas

- Fixing suspected source-level factual/methodological issues (→ metadata section only)
- Cross-document reconciliation (→ future milestone)
- Automated markdown verification tooling (→ v2)
- Reconnecting bibliography.tex references to body with proper `\cite{}` commands (→ LaTeX source edit, outside v1.3 scope)
