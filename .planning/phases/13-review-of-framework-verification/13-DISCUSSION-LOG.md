# Phase 13: Review-of-Framework Verification - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-05
**Phase:** 13-review-of-framework-verification
**Areas discussed:** Authoritative filename, Single-candidate workflow, Sub-document structure, Vacuous-policy verification

---

## Authoritative filename

| Option | Description | Selected |
|--------|-------------|----------|
| review_of_framework.md | Matches source directory name. Symmetry with how source is organized. Phase 14 sibling becomes stage_strat_revision.md. | ✓ |
| review_of_ctl_pinn_framework.md | Matches the pandoc file's content title 'A Technical Review and Resolution Blueprint for the CTL-PINN Framework'. Hyphen/underscore mismatch with sibling docs. | |
| review_of_ctlpinn_framework.md | Splits ambiguity: more descriptive than source dir, cleaner punctuation than the pandoc title. | |

**User's choice:** review_of_framework.md (recommended)
**Notes:** Aligns with the lowercase_underscore convention from D-23/D-30/D-36. Filename symmetry with source dir simplifies the parent-dir story for Phase 14.

---

## Single-candidate workflow

| Option | Description | Selected |
|--------|-------------|----------|
| 3 plans (mirror Phase 10–12) | P1: candidate validation + report skeleton (no ranking, just provenance note). P2: section-by-section audit + fixes. P3: promotion, index update, final verification. Mirrors prior phases' muscle memory. | ✓ |
| 2 plans (streamlined) | P1: audit + fixes (skip ranking entirely). P2: promotion, index, verification. Acknowledges that single-candidate work is simpler. | |

**User's choice:** 3 plans (mirror Phase 10–12) (recommended)
**Notes:** Muscle memory and consistency with Phases 10–12 outweigh modest plan-count savings. P1 produces a "Starting Candidate Provenance" note instead of a ranking report (D-42).

---

## Sub-document structure

| Option | Description | Selected |
|--------|-------------|----------|
| Flat index, parent-dir noted in metadata | One row in markdown_conversion/README.md per phase. Phase 13 row's metadata column notes shared LaTeX parent dir review-of-framework/ with Phase 14. | ✓ |
| Grouped section in README | Group Phases 13+14 under a 'review-of-framework parent' header in the README. Adds nesting to the index. | |

**User's choice:** Flat index, parent-dir noted in metadata (recommended)
**Notes:** Symmetry with Phases 10–12 README rows preserved. Parent-dir disambiguation visible without forcing nested navigation.

---

## Vacuous-policy verification

| Option | Description | Selected |
|--------|-------------|----------|
| Explicit verification | Verification report has a short 'Vacuous Policy Checks' section explicitly confirming: 0 comment blocks, 0 inactive sections, 0 \cite, 0 \bibitem. Reader can audit completeness without re-running greps. | ✓ |
| Implicit carryforward | Carry decisions D-05–D-09 and D-27 forward implicitly. Don't add a 'vacuous checks' section. Lighter report, but reader must trust prior phase patterns. | |

**User's choice:** Explicit verification (recommended)
**Notes:** Explicit absence-confirmation makes future audits self-contained. Also covers the case where the pandoc candidate injected `[@refN]` artifacts that need to be surfaced and stripped (D-48).

---

## Claude's Discretion

- Exact wording of the "Vacuous Policy Checks" subsection within the verification report.
- Exact format of the "Starting Candidate Provenance" note in P1 output.
- Exact text of the parent-dir metadata column entry in the README index row.
- Exact discrepancy ID format, as long as IDs remain stable and map from audit table to fix log.
- Whether to surface line-count or byte-count comparisons in the audit (either acceptable).

## Deferred Ideas

- Cross-document reconciliation between review-of-framework and other instruction documents.
- Auditing the sibling `stage_strat_revision/` sub-document (Phase 14's scope).
- Fixing suspected source-level issues — preserved in body, documented in metadata.
- Shared automated markdown-verification tooling — deferred to v2.
- Unified parent-doc README under `original_latex/review-of-framework/` — out of scope for v1.3.
