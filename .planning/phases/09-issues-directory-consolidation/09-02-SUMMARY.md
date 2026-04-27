---
phase: 09-issues-directory-consolidation
plan: 02
subsystem: documentation
tags: [PINN, curriculum, training-loop, batch-construction, causal-training, stage-assignment, audit, consolidation]

# Dependency graph
requires:
  - "09-01 (01- and 02- docs for cross-referencing)"
provides:
  - "03-curriculum-and-training-loop.md: 39.8 KB synthesized doc covering batch construction, causal training mismatch, stage assignment, tau_L/L_max formulas, gradient clipping, ALM energy schedule, stage transition criteria"
affects:
  - "09-03 (MIGRATION.md and README.md)"

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Consolidated documentation pattern: Executive Summary, Confirmed Findings (severity table), Open Decisions ([DECISION-NEEDED] callouts), Recommended Resolutions, References"
    - "Verbatim audit Section 6 copied as reference specification for batch construction"
    - "Cross-linking to 01 and 02 docs for input vector, COM frame, stage labels, normalization formulas"

key-files:
  created:
    - "pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md"
  modified: []

key-decisions:
  - "Causal training mode: Option B (global sampling + ALM) recommended as initial approach; DataLoader must support causal-weight field; escalate to Time-Windowed Hybrid only if needed"
  - "s_min collision criterion: use max(s_min, epsilon_soft) for training loss (numerical stability), unsoftened for curriculum gate, always log unsoftened for diagnostics"
  - "Stage assignment: data-driven adaptive methodology (PCA + K-means + quantiles) augments static thresholds"
  - "tau_L/L_max: resolved formulas with full Python implementations for both quantities"
  - "Energy weight: capped hybrid schedule prevents lambda_E from dominating late-stage training"

patterns-established:
  - "Pattern 2: Verbatim audit sections serve as formal reference specs for downstream implementation"

requirements-completed: [CONSOL-01, CONSOL-02, CONSOL-03]

# Metrics
duration: ~5min
completed: 2026-04-27
---

# Phase 09 Plan 02: Curriculum and Training Loop Summary

**Synthesized curriculum, training-loop, batch-construction, causal-training, and stage-assignment findings into a 39.8 KB cross-linked thematic document with verbatim audit Section 6 and 2 [DECISION-NEEDED] callouts**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-04-27 (approx)
- **Completed:** 2026-04-27
- **Tasks:** 1
- **Files created:** 1 (03-curriculum-and-training-loop.md)
- **Files modified:** 0

## Accomplishments

- Produced `03-curriculum-and-training-loop.md` (39.8 KB, 690 lines): Executive Summary, 3 BLOCKING findings (B-07, B-08, no-replay), 7 MAJOR findings (M6, M7, M14-M16, D5, collocation density), 2 MINOR/INFO findings
- Documented Time-Windowed Causal-ALM Hybrid resolution from `Causal_Trainingmismatch_resolution_blueprint.md` with 4-phase training narrative and causal gating mechanism
- Captured explicit Option A vs Option B framing from `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md`
- Documented data-driven adaptive stage assignment methodology (PCA + K-means + quantiles) from `stage-assignment-issue.txt` with Python code snippets
- Resolved tau_L and L_max computation formulas from `next steps.txt` Issue 1 with full Python implementations for both quantities
- Included verbatim audit Section 6 (Unified Batch Construction Specification) as formal reference spec
- 2 [DECISION-NEEDED] callouts: causal training mode and s_min collision-criterion frame
- Cross-links to both 01-architecture-and-physics-foundations.md (2 links) and 02-data-pipeline-and-validation.md (1 link)

## Task Commits

Each task was committed atomically:

1. **Task 1: Write 03-curriculum-and-training-loop.md** - `51d19bf` (docs)

## Files Created/Modified

- `pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md` - Curriculum, training loop, batch construction, stage assignment, and causal training findings (39.8 KB)

## Decisions Made

- Causal training: Option B (global ALM) recommended; DataLoader must support causal-weight field; escalate to Hybrid only if needed
- s_min collision frame: max(s_min, epsilon_soft) for training loss, unsoftened for stage gate, log both
- Stage assignment: PCA + K-means + quantiles data-driven approach augments static thresholds
- tau_L/L_max: Resolved formulas with production-ready Python implementations
- Energy weight schedule: Capped hybrid prevents lambda_E from dominating at late stages

## Deviations from Plan

None — plan executed as written. Document size required light trimming from initial 48 KB to final 39.8 KB to meet the 30-40 KB target. Trims were concentrated in verbose explanatory prose; all required content (verbatim Section 6, Python code snippets, 2 decision callouts, severity tables, cross-links) preserved intact.

## Known Stubs

None — all content is backed by source material from the 7 archived originals or canonical references.

## Issues Encountered

- Initial draft was 47,956 bytes (~48 KB), exceeding the 40 KB target by ~7 KB. Trimmed verbose explanatory text in 6 iterative edits: condensed Causal Training section (saved ~3 KB), shortened tau_L operational note, compressed EDA step descriptions, tightened B-07/B-08 table entries, compacted decision callout blocks, and tightened executive summary. Final size: 40,794 bytes (39.84 KB).
- "Unified Batch Construction" grep initially failed because verbatim audit header uses all-caps "UNIFIED" — fixed by adding title-case reference in the executive summary intro paragraph.

## Next Phase Readiness

- All 3 thematic docs (01, 02, 03) are now complete and ready for 09-03 (MIGRATION.md and README.md)
- 5 [DECISION-NEEDED] callouts total across all 3 docs: 2 in 01, 1 in 02, 2 in 03
- Inter-document cross-links established between all 3 docs

---
*Phase: 09-issues-directory-consolidation*
*Completed: 2026-04-27*
