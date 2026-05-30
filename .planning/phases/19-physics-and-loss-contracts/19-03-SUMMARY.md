---
phase: 19-physics-and-loss-contracts
plan: 03
subsystem: pinn-framework-spec
tags: [hNN-cleanup, energy-regularizer, alm-ablation, cross-reference-validation, ac-phys-04, ac-phys-05]

# Dependency graph
requires:
  - phase: 19-physics-and-loss-contracts
    provides: "19-01 CTL-side total-loss formula and cross-reference targets"
  - phase: 19-physics-and-loss-contracts
    provides: "19-02 architecture-side PHYS-02/03/04/05 formula skeleton"
provides:
  - "HNN-style prose removed from active pinn_architecture.md sections"
  - "Energy term reframed as a soft conservation regularizer using analytic matched-Plummer Hamiltonian H_epsilon"
  - "Optional P2 ALM ablation appendix with scalar-conservation-only scope"
  - "Cross-reference anchors between ctl_instruction.md and pinn_architecture.md aligned for PHYS-02/03 and PHYS-05"
  - "Summary table aligned to L_data, L_IC, L_phys, L_E, and L_L default loss terms"
affects: [19-04, 20, 21, FUT-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Hamiltonian terminology is retained only for the analytic energy function H_epsilon, not architecture branding"
    - "ALM is documented only as optional P2 ablation, never as default dense-residual machinery"
    - "Cross-reference verifier expects CTL references to place pinn_architecture.md and PHYS-* markers on the same line"

key-files:
  created: []
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md - HNN prose rewrite, P2 ALM appendix, loss summary cleanup"
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md - Mechanical PHYS-02/PHYS-03 cross-reference anchor alignment"

key-decisions:
  - "Applied D-04/D-09: removed HNN-style architecture claims while preserving Hamiltonian as the analytic energy function."
  - "Applied D-05: documented optional ALM only as a P2 scalar-conservation ablation."
  - "Applied D-20: preserved epsilon_H = 1e-4 * S_H, training metadata persistence, and invalid S_H validation failure semantics."
  - "Resolved a mechanical cross-reference verifier mismatch by aligning CTL anchors without changing semantic content."

patterns-established:
  - "Read-only CTL verifier failures can require a targeted mechanical repair before closure when the plan explicitly treats unresolved CTL cross-reference defects as blockers."

requirements-completed:
  - PHYS-04
  - PHYS-05
  - VER-05

# Metrics
duration: ~25min
completed: 2026-05-30T00:00:00-04:00
---

# Phase 19 P03: Architecture Prose Cleanup Summary

**The architecture spec now describes energy and angular-momentum terms as soft conservation regularizers, with ALM confined to an optional P2 ablation.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-05-30
- **Completed:** 2026-05-30
- **Tasks:** 2 plan tasks plus targeted CTL anchor repair
- **Files modified:** 2 plus this summary

## Accomplishments

- Removed active HNN-style branding from `pinn_architecture.md` title/intro, loss overview, energy section, loss-balancing prose, and summary table.
- Renamed and rewrote the energy section around a soft conservation regularizer using analytic matched-Plummer `H_epsilon`.
- Added an optional ALM P2-ablation appendix limited to scalar conservation constraints, with default ALM off.
- Preserved D-20 `epsilon_H = 1e-4 * S_H`, training metadata persistence, and invalid `S_H` validation semantics.
- Aligned CTL cross-reference anchors so the Phase 19 verifier recognizes PHYS-02 and PHYS-03 links to `pinn_architecture.md`.

## Task Commits

1. **Task 1: HNN prose rewrite and P2 ALM appendix** - `d1280bf` (docs: complete HNN prose rewrite and add P2 ALM ablation)
2. **Targeted repair: align CTL cross-reference anchors** - `656fce4` (docs: align ctl cross-reference anchors)

## Files Created/Modified

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - HNN prose cleanup, P2 ALM appendix, loss summary and D-20 preservation.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - Mechanical PHYS-02/PHYS-03 cross-reference anchor alignment.

## Verification

- **Task 1 gate:** PASS - soft conservation regularizer language, energy-regularizer title, P2 ALM appendix, D-20 `epsilon_H` contract, metadata persistence, and no-HNN/no-pseudo-ALM negative checks passed.
- **Task 2 gate:** PASS after targeted CTL repair - both specs contain all total-loss terms, CTL contains `see pinn_architecture.md`, `pinn_architecture.md PHYS-02`, and `pinn_architecture.md PHYS-03` anchors, architecture forward references are satisfied, and no `pinn/` diff exists.
- **Plan key-link gate:** PASS - `pinn_architecture.md` links to `ctl_instruction.md` through the matching total-loss equation.

## Deviations from Plan

Task 2 initially blocked because the CTL PHYS-02 and PHYS-03 cross-references were semantically correct but split across lines in a way the verifier could not match. The plan explicitly blocks unresolved CTL cross-reference defects, so a targeted mechanical repair commit aligned those anchors before closure.

**Post-execution metadata note:** The `19-03-PLAN.md` `files_modified` frontmatter remains the original planned scope. This summary's "Files Created/Modified" section records the actual executed scope, including the targeted `ctl_instruction.md` anchor repair.

## Issues Encountered

None beyond the mechanical cross-reference anchor mismatch.

## Gap Handling

No STOP gaps were encountered. The CTL repair was presentation-only: it did not change the locked PHYS-02/PHYS-03 semantics.

## User Setup Required

None.

## Next Phase Readiness

Plan 19-04 can run the full Phase 19 structural verification, create `19-CODE-DIVERGENCE.md`, reserve AC-PHYS-02, and close the five findings through `VERIFIED` if checks pass.

## Self-Check: PASSED

- Active HNN-style framing is removed from `pinn_architecture.md`.
- Optional ALM is documented only as P2 ablation.
- No `pinn/` files were modified.

---
*Phase: 19-physics-and-loss-contracts*
*Completed: 2026-05-30*
