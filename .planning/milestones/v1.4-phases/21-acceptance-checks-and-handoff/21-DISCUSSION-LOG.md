---
phase: 21
slug: acceptance-checks-and-handoff
status: repaired
created: 2026-06-08
mode: recovery
---

# Phase 21 Discussion Log

## 2026-06-08 Recovery Start

User supplied `docs_temp/work/reviews/current_state_of_phase21.md` and instructed the agent to properly fill in the missed Phase 21 work from the beginning.

Initial facts established:

- Git branch: `milestone/v1.4`, ahead of `origin/milestone/v1.4` by 65 commits.
- Existing user-owned working-tree changes were present outside the Phase 21 repair scope.
- `v1.4-pre-phase-21` tag already existed at the pre-Phase-21 checkpoint.
- GSD init reported Phase 21 found with two plans and zero summaries, so both `21-01-PLAN.md` and `21-02-PLAN.md` were incomplete from GSD's perspective.

## Decisions

### D-21-DISC-01: Treat Prior Probe Results as Untrusted Until Re-Run

The previous `21-PROBE-RESULTS.md` contained PASS claims without raw stdout evidence. The repair re-ran every probe and captured stdout files before updating results.

### D-21-DISC-02: Use `.venv/bin/python`

System `python3` lacked required packages, while `.venv/bin/python` had Python 3.12.13, NumPy 2.2.0, and Torch 2.12.0. Section 10 and the plan verification command now use the repo-local interpreter.

### D-21-DISC-03: Repair Probe Fidelity Before Closure Artifacts

The scaling probe was changed to non-unit scaling cases, the force-energy probe was aligned to the matched-Plummer force/Hamiltonian gradient contract, and the loss-stability probe was changed from a dummy linear layer to a representative SIREN/skip/LayerNorm dry run.

### D-21-DISC-04: Do Not Create Missing `SI-PINN-001`

`SI-PINN-001` appears in planning references but not in the framework-spec SI sections. The repair records the absence instead of synthesizing a new retired SI block.

### D-21-DISC-05: Backfill GSD Artifacts Without Inventing Open Gaps

The repair creates the missing context, research, discussion, gaps, validation, verification, UAT, code-divergence, and per-plan summary files. `21-GAPS.md` records zero open STOP gaps and a retroactive grounding audit for the decisions reviewed during repair.

## User Questions

None asked during the repair pass. The user gave direct instruction to proceed with strict repair from the beginning.
