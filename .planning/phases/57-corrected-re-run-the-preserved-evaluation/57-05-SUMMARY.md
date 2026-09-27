---
phase: 57-corrected-re-run-the-preserved-evaluation
plan: "05"
subsystem: training
tags: [stage-0, run-window, blocked, provenance, mps]

requires:
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: "admitted generation-3 configs, final HEAD, Gate PASS, production conformance, and retained prior generations"
provides:
  - "An immutable generation-3 smoke attempt recorded as an operational environment block"
  - "A generation-scoped blocked-state record with preserved evaluation budget"
affects: [RUN-04, RUN-05, EVAL-02]

actuals:
  tasks: "2/3 completed; smoke attempted and blocked before graded launches"
  commits: 1

key-decisions:
  - "The exact admitted MPS smoke command was attempted; no CPU fallback, row-count reduction, or alternate environment was substituted."
  - "The MPS runtime-resolution failure is operational/incomplete, not the authorized invariant-B scientific terminal closure."
  - "The generation-1 blocked-state singleton remains unchanged; generation-3 evidence uses blocked-state-g3.json."

requirements-completed: []

coverage:
  - id: D9
    description: "The smoke launch used the admitted final HEAD and generation-3 config; no graded seed launched after the failure."
    requirement: RUN-04
    verification:
      - kind: other
        ref: "evidence/blocked-state-g3.json"
        status: pass
      - kind: other
        ref: "evidence/run-ledger.md generation 3 record"
        status: pass
    human_judgment: false
  - id: D16
    description: "The operational environment failure preserves evaluation and leaves the phase incomplete."
    requirement: RUN-05
    verification:
      - kind: other
        ref: "verify_phase57_evidence.py run-window (expected fail-closed)"
        status: pass
    human_judgment: false

duration: "under 1 minute"
completed: 2026-09-27
status: blocked
---

# Phase 57 Plan 05: Run Window Summary

The immutable run window was admitted at HEAD
`ad96e6f46b5c7fd5ac7faa8b23c438974373dc38`. The exact seed-42 smoke command
was launched with `--stage-0-only`, but the environment resolver failed before
optimization with:

> runtime resolve failed: The MPS backend is supported on macOS 14.0+. Current
> OS version can be queried using `sw_vers`

The attempt is recorded in `evidence/blocked-state-g3.json` and the generation
3 section of `evidence/run-ledger.md`. No graded seed, held-out split, or
evaluation artifact was launched or created. The verifier returns nonzero for
`run-window`, preserving the required incomplete disposition.

## Validation

- `verify_phase57_evidence.py admit-run-window` — **ADMIT-RUN-WINDOW-OK** before launch.
- `verify_phase57_evidence.py run-window` — **expected fail-closed** on the generation-3 operational block.
- `python -m unittest tests.phase57.test_evidence_ledger_v2 -q` — **16/16 passed**.
- `git diff --check` — **passed**.

## Next required action

Resolve the MPS runtime/environment incompatibility or provide a supported
execution environment. Any environment change requires a new admission check;
the generation-3 run window cannot resume from this pre-optimization failure.
