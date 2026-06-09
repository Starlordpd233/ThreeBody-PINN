---
phase: 18-frame-and-gauge-contracts
status: passed
verified_at: 2026-05-21T05:33:17Z
requirements:
  - FRAME-01
  - FRAME-02
  - FRAME-03
  - FRAME-04
  - VER-05
source_plans:
  - 18-01-PLAN.md
  - 18-02-PLAN.md
  - 18-03-PLAN.md
source_summaries:
  - 18-01-SUMMARY.md
  - 18-02-SUMMARY.md
  - 18-03-SUMMARY.md
review:
  - 18-REVIEW.md
---

# Phase 18 Verification

## Verdict

`passed`

Phase 18 achieves its goal: the framework specs now define one unified
frame/gauge preprocessing contract across ICs and BRUTUS snapshots, connect
preprocessed-sample and model-output COM guarantees, reconcile hierarchical and
standard quasi-random sampling-frame behavior, preserve 3D Cartesian output
semantics, and record FUT-01 code divergence without modifying `pinn/`.

## Requirement Coverage

| Requirement | Evidence | Status |
|---|---|---|
| `FRAME-01` | `ctl_instruction.md` Step 2 defines the fixed order: parse, mass-invariance check, COM recenter, zero-momentum boost, canonical ordering, canonical rotation gauge, global scaling, then assertions and stored metadata. | PASS |
| `FRAME-02` | `ctl_instruction.md` asserts COM/total-momentum invariants for preprocessed samples; `pinn_architecture.md` defines the hard mass-weighted COM projection for model outputs using ordered raw mass metadata. | PASS |
| `FRAME-03` | `sampling_method.md` documents hierarchical post-perturbation COM/P offsets and standard quasi-random equal-mass COM/P-by-construction behavior, grounded in `simulation_data/`. | PASS |
| `FRAME-04` | `ctl_instruction.md` and `pinn_architecture.md` state that the rotation gauge fixes only the initial orientation and preserves full 3D, 9D Cartesian output positions. | PASS |
| `VER-05` | B-05 and M3 are `VERIFIED` in both evidence packets and the Phase 16 issue ledger after the full Phase 18 structural suite. | PASS |

## Automated Checks

| Check | Result |
|---|---|
| All three plan summaries exist and `phase-plan-index` reports no incomplete plans | PASS |
| Advisory code review artifact `18-REVIEW.md` has `status: clean` after one source-backed prose correction | PASS |
| Phase 16 regression doc checks | PASS |
| Phase 17 strict full suite | PASS |
| Phase 18 strict full suite from `18-VALIDATION.md` | PASS |
| Schema drift gate | PASS |
| Codebase drift gate | WARN only; non-blocking by workflow contract |
| `pinn/STATUS.md` absence and no staged/unstaged `pinn/` diff | PASS |

## Notes

- All Phase 18 gaps are `RESOLVED-WITH-INSTRUCTION`; no new gaps were encountered during phase-level verification.
- The mandatory review gate found one inherited quasi-random momentum sentence that conflicted with D-10's authoritative `simulation_data/` generator behavior. Commit `34cd746` corrected the sentence; the Phase 20.5 Sobol coordinate-allocation target text remains untouched.
- Codebase drift detection warned about structural elements outside the Phase 18 spec work (`.gitignore`, `AGENTS.md`, `ANTIGRAVITY.md`, `GEMINI.md`, and `tests/test_phase12_validation.py`). The gate is advisory/non-blocking and does not affect Phase 18 verification.
- Live `pinn/` code was not used as v1.4 grounding evidence. `pinn/` references in `18-CODE-DIVERGENCE.md` are FUT-01 hand-off coordinates only.

## Human Verification

None required.
