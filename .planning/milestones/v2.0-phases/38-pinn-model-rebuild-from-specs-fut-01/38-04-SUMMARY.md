---
phase: 38-pinn-model-rebuild-from-specs-fut-01
plan: "04"
subsystem: verification
tags: [pytorch, autograd, gradcheck, residual, brutus, evidence]
requires:
  - phase: 38-03
    provides: "PHYS-02 residual, softened acceleration, and a read-only trajectory loader"
  - phase: 37
    provides: "explicit runtime precision/device selection and probe-evidence grammar"
provides:
  - "Standalone fp64-CPU residual gradcheck with machine-readable evidence"
  - "Dual-gate ground-truth residual probe for force-energy and u-leaf Newtonian checks"
affects: [38-06, 43-training-pilot]
tech-stack:
  added: []
  patterns: ["explicit precision/device CLI arms", "exclusive timestamped evidence directories", "atomic evidence writes", "read-only Brutus trajectory validation"]
key-files:
  created:
    - pinn/verification/gradcheck_probe.py
    - pinn/verification/residual_probe.py
    - tests/phase38/test_gradcheck_probe.py
    - tests/phase38/test_residual_probe.py
    - .planning/phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/gradcheck/20260713T121039Z/raw.json
    - .planning/phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/gradcheck/20260713T121039Z/summary.md
  modified: []
key-decisions:
  - "Use direct autograd of softened potential for Gate A and u-coordinate finite differences for Gate B."
  - "Reject evidence roots inside simulation_data to preserve the read-only dataset boundary."
  - "Require explicit --precision and --device arms for both probes."
metrics:
  duration: "9 minutes"
  completed: "2026-07-13"
  tasks_completed: 3
  files_created: 6
status: complete
---

# Phase 38 Plan 04: Rung 2 and 3 Probe Summary

Standalone fp64-CPU residual gradcheck and dual-gate ground-truth residual probes now produce exclusive, provenance-bound evidence without writing to simulation data.

## Performance

- **Duration:** 9 minutes
- **Started:** 2026-07-13T12:03:22Z
- **Completed:** 2026-07-13T12:11:58Z
- **Tasks:** 3/3
- **Files created:** 6

## Accomplishments

- Added a CLI gradcheck probe that records the torch build, pre-import fallback state, resolved runtime arm, tolerances, outcome, and exception details in JSON and Markdown evidence.
- Added a read-only Brutus trajectory residual probe with independent force-energy and u-leaf Newtonian gates, softening/minimum-separation provenance, COM offset, and exclusion counts.
- Added contract tests that exercise all required explicit CLI arms, evidence structure, failure paths, D scaling, non-overwriting output, and the no-implicit-precision-default rule.
- Recorded a durable fp64-CPU gradcheck PASS at `evidence/gradcheck/20260713T121039Z/`.

## Task Commits

1. **Task 1: Rung probe contract tests** — `833f13f4` (`test`)
2. **Task 2: FP64 CPU gradcheck probe** — `27a99d61` (`feat`)
3. **Task 3: Dual-gate residual probe** — `6de10709` (`feat`)
4. **Required runtime evidence: fp64 CPU gradcheck PASS** — `13783afd` (`evidence`)

## Files Created

- `pinn/verification/gradcheck_probe.py` — explicit-arm PyTorch residual gradcheck CLI and evidence writer.
- `pinn/verification/residual_probe.py` — read-only trajectory loader, Gate A force-energy check, and Gate B u-leaf Newtonian check.
- `tests/phase38/test_gradcheck_probe.py` — gradcheck CLI, runtime, and evidence contracts.
- `tests/phase38/test_residual_probe.py` — deterministic Brutus fixture and dual-gate contracts.
- `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/gradcheck/20260713T121039Z/raw.json` — machine-readable fp64-CPU PASS evidence.
- `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/gradcheck/20260713T121039Z/summary.md` — human-readable fp64-CPU PASS evidence.

## Decisions Made

- Gate A differentiates the softened potential with `torch.autograd.grad` and compares it directly with `softened_acceleration`; it does not use finite differences for that identity.
- Gate B converts raw Brutus positions and velocities with the documented `D` and `T` scaling, differentiates with respect to normalized time `u`, and compares acceleration against the softened force.
- Evidence directories use an exclusive UTC timestamp suffix and atomic writes. Both probes reject a user-selected evidence root under `simulation_data/`.

## Verification

- `\/Users\/<user>\/miniforge3\/bin\/conda run -n pinn-train python -m unittest tests.phase38.test_gradcheck_probe tests.phase38.test_residual_probe -v` — passed (8 tests).
- `\/Users\/<user>\/miniforge3\/bin\/conda run -n pinn-train python -m pinn.verification.gradcheck_probe --precision float64 --device cpu` — passed; recorded fp64-CPU evidence.
- `graphify update .` — passed.
- `git diff --check` — passed.

## TDD Gate Compliance

- RED: `833f13f4` added both probe contract suites before their modules existed; all eight tests skipped on the expected missing imports.
- GREEN: `27a99d61` and `6de10709` implemented the probes and made all eight tests pass.
- REFACTOR: not needed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Protect the read-only dataset boundary from probe output**
- **Found during:** Tasks 2 and 3
- **Issue:** A caller-controlled `--evidence-root` could otherwise place probe output below `simulation_data/`, violating the plan's read-only-data requirement.
- **Fix:** Resolve the evidence root before writing and reject any path contained by `simulation_data/`; retain exclusive directory creation and atomic writes for evidence integrity.
- **Files modified:** `pinn/verification/gradcheck_probe.py`, `pinn/verification/residual_probe.py`
- **Verification:** Combined probe tests pass and `git status --short simulation_data/` is empty.

### Blocking Environment Adjustment

- The plan's bare `conda` command was unavailable on `PATH`. Validation used the repository's known Miniforge executable at `<home>/miniforge3/bin/conda`; no dependency or configuration changed.

## Known Stubs

None. Created and modified files were scanned for placeholder text, empty UI-facing values, and unwired mock data.

## STOP-Protocol Gaps

None. The implementation follows the Phase 38 grounding sources and did not require a new semantic, process-schema, or cross-phase decision.

## Next Phase Readiness

- Plan 38-06 can statically audit the explicit precision/device arms and evidence grammar.
- Production residual evidence requires an operator-selected real Brutus trajectory via `residual_probe.py --path ...` or a validated `--variant-id`; this repository worktree intentionally contains no bulk simulation payload.

## Self-Check: PASSED

- All six created artifacts listed above exist in the worktree.
- Task and evidence commits `833f13f4`, `27a99d61`, `6de10709`, and `13783afd` exist in Git history.
