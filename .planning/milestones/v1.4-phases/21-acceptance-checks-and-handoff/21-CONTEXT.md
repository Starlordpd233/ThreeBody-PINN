---
phase: 21
slug: acceptance-checks-and-handoff
status: repaired
created: 2026-06-08
governance: "v1.4 STOP protocol, VER-04 disposable-probe rule, no live pinn/ grounding"
---

# Phase 21: Acceptance Checks and Handoff - Context

## Phase Boundary

Phase 21 closes the v1.4 validation and handoff requirements after Phase 20.5:

- `VER-01`: define numeric acceptance checks for scaling, COM, AD, force-energy, and loss stability.
- `VER-03`: produce a validation handoff for Phase 22 that states fixed, unchanged, deferred, and future-validation items.
- `VER-04`: execute the acceptance checks with disposable probes that test the v1.4 framework specs, not v1.3-era `pinn/` code.
- `VER-06`: reconcile framework-spec `SI-*` metadata entries with back-references for v1.4-resolved findings while preserving unrelated entries.
- `VER-05`: keep the verification loop honest: no closure claim without passing acceptance evidence.

The previous Phase 21 commit (`2f952cf`) added Section 10, two plans, probes, probe results, and a handoff, but left the phase structurally incomplete because the per-plan summaries and phase closure artifacts were absent. The repair pass on 2026-06-08 starts from those artifacts, replaces weak/fabricated evidence with captured stdout, and backfills the missing GSD closure set.

## Canonical References

- `.planning/REQUIREMENTS.md:60-65` - `VER-01`, `VER-03`, `VER-04`, `VER-05`, and `VER-06`.
- `.planning/ROADMAP.md:236-247` - Phase 21 goal, dependencies, and success criteria.
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:17-39` - current finding statuses, including M6/M7 deferrals.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:984-1009` - Section 10 acceptance checks and executable commands.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:360-420` - matched Plummer residual / physics loss contract.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:496-536` - matched-Plummer Hamiltonian and soft energy-regularizer contract.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1446-1448` - retired `SI-CTL-001` metadata entry.
- `pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md:425-427` - retired `SI-SSR-001` metadata entry.

## Implementation Decisions

### D-21-01: Repo-Local Python Is the Probe Interpreter

System `python3` resolves to a Python without `numpy` or `torch`, so the executable commands in Section 10 now use `.venv/bin/python`. The environment evidence is captured in `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/python_environment.stdout.txt`.

### D-21-02: Probe Results Must Point to Raw Stdout

`21-PROBE-RESULTS.md` is a summary only. The re-derivable evidence lives in per-probe stdout files under `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/`, with SHA-256 hashes recorded in the results file.

### D-21-03: Force-Energy Checks the Grounded Matched-Plummer Contract

The original Section 10 wording overclaimed a Hamiltonian-conservation test. The grounded spec says the network uses a soft conservation regularizer, does not parameterize a Hamiltonian, and evaluates the matched-Plummer Hamiltonian using the same `r_safe` denominator as the force residual. The repaired probe therefore checks finite `H_epsilon` and equality between the manual force residual and the negative Hamiltonian position gradient.

### D-21-04: Loss Stability Uses a Representative Spec Architecture

The loss-stability dry run must exercise SIREN, skip/power branches, and `LayerNorm(elementwise_affine=False)`. A plain `nn.Linear(14, 9)` is not a faithful probe for the Section 2-5 architecture contract.

### D-21-05: `SI-PINN-001` Is Not Synthesized

`VER-06` lists `SI-PINN-001` as a candidate, but `git grep` at `v1.4-pre-phase-21` and the current tree finds it only in planning references, not in a framework-spec `Source Issues` section. Creating a new retired entry would fabricate source-issue provenance. The repair records the absence and preserves existing unrelated entries.

## Execution Coordination Rules

- Do not use live `pinn/` implementation files as grounding evidence.
- Do not claim probe execution from summarized values; cite raw stdout evidence files.
- If a future probe failure reveals a source-silent semantic decision, add a full STOP-protocol entry to `21-GAPS.md` and stop the dependent work.
- Preserve unrelated user-owned working-tree changes outside the Phase 21 files touched by this repair.
