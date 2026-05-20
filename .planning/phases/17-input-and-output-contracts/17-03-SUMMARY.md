---
phase: 17-input-and-output-contracts
plan: 03
subsystem: pinn-framework-spec
tags: [cleanup-gate, code-divergence, ac-io-04, fut-01, no-live-code-evidence]

# Dependency graph
requires:
  - phase: 17-input-and-output-contracts
    provides: "17-01 input contract and 17-02 output contract are both summarized and verified"
provides:
  - "AC-IO-04 cleanup gate: stale 11D/12D/trig-angle/direct-velocity wording absent from normative framework-spec prose before Source Issues metadata"
  - "Phase 17 FUT-01 hand-off inventory in 17-CODE-DIVERGENCE.md"
  - "Full Phase 17 shell validation suite result for B-03, B-04, B-06, M1, and M2"
affects: [18, 19, 20, 21, FUT-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Divergence inventory: five-column Markdown schema from GAP-17-04"
    - "FUT-01 priority values are non-binding hand-off hints per GAP-17-11"
    - "Source Issues metadata remains untouched until Phase 21 VER-06"

key-files:
  created:
    - ".planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md - FUT-01 hand-off inventory for Phase 17 spec-vs-code divergences"
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md - Metadata-only cleanup for legacy invariant/mass-fraction/velocity-angle wording"

key-decisions:
  - "Applied D-10: invariant-heavy descriptors and orientation summaries are metadata only under the Jacobi-state IC contract."
  - "Applied D-13: AC-IO-04 is a Phase 17-local cleanup check, not a Phase 16 ledger row."
  - "Applied D-14: Phase 17 records live-code divergence for FUT-01 only and does not edit pinn/*.py."
  - "Applied D-15: pinn/STATUS.md is not created during Phase 17."
  - "Applied GAP-17-11: row-level FUT-01 priority values remain non-binding hints."

patterns-established:
  - "Code divergence rows list live code file:line references only as FUT-01 hand-off context, not v1.4 evidence."
  - "Historical author-note wording can remain in normative files only when explicitly labeled non-normative and outside stale negative-grep terms."

requirements-completed:
  - IO-04
  - VER-05

# Metrics
duration: ~35min
completed: 2026-05-20T02:39:16Z
---

# Phase 17 P03: Cleanup And Divergence Inventory Summary

**Phase 17 now has a clean active input/output contract surface plus a FUT-01 inventory for all known P01/P02 implementation divergences.**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-05-20T02:05Z (approx)
- **Completed:** 2026-05-20T02:39:16Z
- **Tasks:** 3 plan tasks + plan summary
- **Files modified:** 2 plus this summary

## Accomplishments

- Cleaned `ctl_instruction.md` so legacy invariant-heavy, mass-fraction, and velocity-angle wording is explicitly metadata-only or removed from the final network IC-slot path.
- Created `17-CODE-DIVERGENCE.md` with the resolved D-14 five-column schema and all eight Phase 17 FUT-01 hand-off rows.
- Verified B-03, B-04, B-06, M1, and M2 ledger rows remain `VERIFIED`.
- Confirmed no `pinn/STATUS.md` exists and no `pinn/*.py` files have staged or unstaged diffs.

## Task Commits

1. **Task 1: Run stale-wording audit and clean framework specs** - `a39697c` (docs: clean obsolete input output wording)
2. **Task 2: Create `17-CODE-DIVERGENCE.md` for FUT-01 hand-off** - `cbc8c67` (docs: record input output code divergence)
3. **Task 3: Full Phase 17 validation** - no code/doc edit needed after verification; results recorded in this summary.

## Files Created/Modified

- `.planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md` - New FUT-01 hand-off inventory with AC-IO-04 marker, D-14 schema, and non-binding priority note.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - Legacy invariant/mass-fraction/velocity-angle prose cleaned to match the Phase 17 Jacobi-state IC contract.

## Dimensionality Classification

Remaining pre-Source-Issues dimensionality mentions were classified as follows:

- `ctl_instruction.md` canonical: final `14D` network input `[\tau, IC_{13}]`; primary `13-component` Jacobi-state contract; training-loop `14-dimensional` input bullet.
- `ctl_instruction.md` historical-labeled: two author-note `14-dimensional` / `14th-dimentional` questions are explicitly labeled historical, pre-Phase-17, and non-normative.
- `pinn_architecture.md` canonical: Section 5.2 `14-dimensional` network input and Implementation Blueprint `14-dimensional` row both back-reference the canonical `IC_{13}` contract.
- No normative pre-Source-Issues `11D`, `12D`, unqualified trig-angle, or direct-velocity output wording remains.

## Verification

- **Task 1 negative cleanup gate:** PASS - no stale `12D input vector`, `12-dimensional input vector`, `11-component IC`, direct velocity-output wording, or `5 values for 3 trigonometrically encoded angles` before Source Issues metadata.
- **Task 2 AC-IO-04 artifact gate:** PASS - divergence inventory exists with AC-IO-04, FUT-01 priority, all eight expected rows, no `pinn/STATUS.md`, and no `pinn/` diff.
- **Task 3 full Phase 17 suite:** PASS - required evidence packets and divergence file exist, canonical 14D/IC_13/COM/AD markers are present, all in-scope ledger rows are `VERIFIED`, and no `pinn/` diff exists.

## Deviations from Plan

None - plan scope and source boundaries were followed. The Task 1 cleanup also removed stale-adjacent mass-fraction and velocity-angle normalization prose in `ctl_instruction.md`; this was within the plan's obsolete contract wording scope and was grounded by D-07/D-10.

## Issues Encountered

- Three read-only sidecar agents were dispatched for stale-wording, verification, and divergence grounding. They did not return before local verification completed, so they were closed without using their output.

## Gap Handling

No new STOP gaps were encountered. All decisions used by this plan were already `LOCKED` or `RESOLVED-WITH-INSTRUCTION` in `17-CONTEXT.md` / `17-GAPS.md`.

## Next Phase Readiness

Phase 17 has no remaining incomplete plan summaries. The next workflow step is phase-goal verification and, if it passes, Phase 17 completion bookkeeping.

---
*Phase: 17-input-and-output-contracts*
*Completed: 2026-05-20*
