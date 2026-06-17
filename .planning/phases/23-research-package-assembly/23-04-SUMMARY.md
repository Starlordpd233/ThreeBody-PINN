---
phase: 23-research-package-assembly
plan: 04
subsystem: documentation-assembly
tags: [research-package, framed-questions, neutral-framing, hard-constraints, PKG-02]

# Dependency graph
requires:
  - phase: 23-03
    provides: research_package/claims-table.md (CLM IDs) and intact specs/ snapshots
provides:
  - research_package/framed-research-questions.md (PKG-02) with hard-constraints preamble and per-finding neutral questions
affects: [23-05, 24-empirical-dataset-verification, 25-evidence-framework, 26-ingestion-contracts, 27-sampling-contracts, 28-validation-metrics-contracts]

# Tech tracking
tech-stack:
  added: []
  patterns: [neutral external-research framing (EDL precedent), per-finding question blocks grouped by downstream cluster, CLM-ID figure referencing, hard-constraints preamble verbatim from locked specs]

key-files:
  created:
    - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/framed-research-questions.md
  modified: []

key-decisions:
  - "SCS gate cited only to data_quality_assessment.md (lines 120/130/234 + SI-DQA-003), annotated as a read-only research report; never placed in an editable spec (Pitfall 1)"
  - "Both known conflicts (SCS ratio thresholds, D=6.694) posed with both positions and the locked counter-position cited, unsettled (D-09)"
  - "M13 fallback posed with both options (skip to Stage 6 vs flagged low-fidelity) and annotated a Phase-26 STOP-gap candidate; no fallback asserted (Pitfall 6)"
  - "Doc-03 items (M16, G6, training-loop metric usage) appear only as deferred forward-references, not questions (Pitfall 4)"
  - "Every issue-doc proposal qualified as 'the issue doc proposes/recommends X (non-authoritative)'; no imperative carried (Pitfall 2)"

patterns-established:
  - "Per-finding neutral question block: (i) issue-doc position + line citation, (ii) framework-spec position or silent, (iii) dataset facts by CLM ID"
  - "Inventory coverage table accounting for every item in 23-RESEARCH.md finding inventory with disposition + CLM IDs + downstream phase"

requirements-completed: [PKG-02]

# Metrics
duration: 12min
completed: 2026-06-10
---

# Phase 23 Plan 04: Framed Research Questions Summary

**PKG-02 framed-research-questions.md authored: a hard-constraints preamble carrying the six locked v1.4 conventions verbatim plus every contested/unverified in-scope issue-02 finding posed as an explicit neutral question grouped by the three downstream-contract clusters — no agent decision smuggled**

## Performance

- **Duration:** ~12 min
- **Tasks:** 2
- **Files modified:** 1 (created)

## Accomplishments
- Authored the source-treatment framing (D-09): both the issue doc and its Recommended Resolutions stated non-authoritative, with the SCS-threshold seed conflict as the worked example, and the `pinn/` "Canonical" citation explicitly overridden (SCOPE-10)
- Authored the hard-constraints preamble (D-10): the six locked v1.4 conventions reproduced verbatim with spec citations (14D contract, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening + dual-epsilon, post-v1.3 SCS gate, PHYS-01 D convention); the SCS gate cited only to the read-only DQA report; the two distinct `ε_H` meanings kept disjoint
- Stated the doc-03 scope boundary: M16, G6, and training-loop metric usage as deferred forward-references
- Posed every in-scope finding as a neutral question across three clusters (Q-A1..Q-A6 ingestion, Q-B1..Q-B4 sampling/precision/global-scale, Q-C1..Q-C4 validation metrics), each citing the issue-doc position, the spec position, and dataset facts by CLM ID
- Both known conflicts (SCS thresholds, D=6.694) and the M13 fallback posed without settling; M13 annotated a Phase-26 STOP-gap candidate
- Added the inventory coverage table (23 rows) accounting for every item in 23-RESEARCH.md, and a Return Format that constrains the external research to expectations only (no prescribed schema)

## Task Commits

Each task was committed atomically via `scripts/agent-commit`:

1. **Task 1 (T-23-04-01): Hard-constraints preamble + source-treatment framing + doc-03 boundary** - `a678acb` (docs)
2. **Task 2 (T-23-04-02): Per-finding neutral questions + coverage table + Return Format** - `dbe18e8` (docs)

## Files Created
- `research_package/framed-research-questions.md` (473 lines) - PKG-02 framed-questions document: hard-constraints preamble, source-treatment framing, doc-03 boundary, three clusters of neutral per-finding questions, inventory coverage table, Return Format

## Decisions Made
- Cited the SCS gate exclusively to `data_quality_assessment.md` (its only written home) with the SI-DQA-003 / STATE.md ratification as authority, annotated "read-only research report" — satisfies the locked-convention-as-hard-constraint requirement without implying the gate lives in an editable spec (RESEARCH Open Question 1; mechanical/presentation choice)
- Posed M13 with both candidate fallbacks neutrally and flagged it a Phase-26 STOP-gap candidate rather than asserting a policy (RESEARCH Open Question 2)
- Mapped each issue-doc Recommended Resolution (P1-1..P2-2) into its corresponding question as a non-authoritative proposal rather than a settled fix
- Kept the validation raw-drift gate `ε_H` disjoint from the training energy-denominator floor `ε_H = 1e-4·S_H` (Pitfall 1/3)

## Deviations from Plan

None - plan executed exactly as written.

## Governance / STOP-Protocol Notes

No source-silent semantic, process-schema, or cross-phase decision was forced. Every contested finding (the two known conflicts and the M13 fallback) is grounded by the plan and the locked CONTEXT decisions as "pose neutrally / do not settle," so no gap was opened. `23-GAPS.md` and `.planning/milestones/v1.5-GAPS.md` remain uncreated (no gap surfaced). No edit to any source spec, `data_quality_assessment.md`, `sampling_method.md`, or `pinn/` content. Work committed on `milestone/v1.5`.

## Issues Encountered
None.

## User Setup Required
None.

## Next Phase Readiness
- PKG-02 is complete; the research package now carries snapshots, claims table, consolidated context, and framed questions
- Plan 05 (manifest/README + delivery note + STATE.md gate-open) can proceed, indexing framed-research-questions.md alongside the other package artifacts
- No blockers

## Self-Check: PASSED

- `research_package/framed-research-questions.md` verified present on disk
- Both task commits (a678acb, dbe18e8) verified in git log
- Task 1 greps: six locked conventions present (10); SCS gate cited to DQA (2), never to an editable spec (0); non-authoritative framing + seed conflict present; `pinn/` override present; doc-03 boundary present
- Task 2 greps: three cluster headings (23); in-scope findings (56 ≥ 10); CLM references (37 ≥ 5); doc-03 leakage as a question (0); M13 both options + STOP candidate present
- Inventory coverage table accounts for all 23 finding-inventory items

---
*Phase: 23-research-package-assembly*
*Completed: 2026-06-10*
