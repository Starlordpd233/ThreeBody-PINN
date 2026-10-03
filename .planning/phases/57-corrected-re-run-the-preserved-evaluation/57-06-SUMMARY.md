---
phase: 57-corrected-re-run-the-preserved-evaluation
plan: "06"
subsystem: evaluation
tags: [eval-02, no-candidate, preserved-unspent, terminal]

requires:
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: "57-05's authorized invariant-B terminal closure (terminal-state.json) with the evaluation preserved-unspent"
provides:
  - "A durable no-candidate record bound to terminal-state.json; the single held-out evaluation is not spent"
affects: [EVAL-02]

plan_head_before: e0ec85f6
commits: 1

key-files:
  created:
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/no-candidate.json

key-decisions:
  - "On the authorized terminal branch, Task 1 writes no-candidate.json and stops before Task 2; no candidate is selected and no evaluator is invoked."

requirements-completed: []

coverage:
  - id: D4
    description: "No structural candidate is selected; the terminal branch leaves the evaluation demonstrably unspent."
    requirement: EVAL-02
    verification:
      - kind: other
        ref: "verify_phase57_evidence.py candidate / pre-evaluation / final (CANDIDATE-OK, PRE-EVALUATION-UNSPENT-OK, FINAL-UNSPENT-OK)"
        status: pass
    human_judgment: false

completed: 2026-10-03
status: complete
---

# 57-06 Summary — Preserved evaluation (unspent)

Plan 57-05 closed on the authorized invariant-B terminal branch: generation-7
graded seed 42 tripped invariant B at step 951. Task 1's precondition for that
branch holds, so the Phase-57 evidence builder's `candidate` command wrote
`evidence/no-candidate.json`:

```json
{"schema": "phase57-no-candidate/v1", "reason": "invariant_b_halt_no_advance",
 "owner_stop": true, "evaluation": "preserved-unspent",
 "terminal_state_sha256": "35fe3afd19ded9b2714c0ee45ab806fe2e19211c8897a5cab608be6bb6b7d941"}
```

Per Task 1, the plan stops before Task 2. No candidate was selected, no
readiness record was written, `pinn.evaluate` was not invoked, and no
`runs/stage0-v23g7-*/evaluation` directory exists. The one preserved held-out
look remains unspent.

## Task Commits

| Commit | Description |
|---|---|
| `280f6efd` | `evidence(57): record unspent no-candidate closure` |

## Validation Evidence

| Check | Result |
|---|---|
| `build_phase57_evidence.py candidate` | `NO-CANDIDATE-OK` |
| `verify_phase57_evidence.py candidate` | `RUN-WINDOW-TERMINAL-OK`, `CANDIDATE-OK` |
| `verify_phase57_evidence.py pre-evaluation` | `PRE-EVALUATION-UNSPENT-OK` |
| `verify_phase57_evidence.py final` (also re-run after commit `e0ec85f6`) | `FINAL-UNSPENT-OK` |
| `tests.phase57.test_gate_and_evaluation.EvidenceSelectionTests` | 7 tests OK |

## Deviations from Plan

- Task 1's automated verify list also names
  `tests.phase50.test_candidate_finalization.CandidateFinalizationTests`.
  Those tests fail for a reason that predates this plan: they still point at
  the pre-archive path `.planning/phases/50-valid-stage-0-re-run/evidence/`,
  which moved to `.planning/milestones/v2.2-phases/` in `12e16d7b`. They were
  not run as evidence here.

## Self-Check: PASSED
