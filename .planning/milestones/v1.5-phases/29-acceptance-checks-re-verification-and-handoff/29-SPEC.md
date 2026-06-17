# Phase 29: Acceptance Checks, Re-verification, and Handoff - Specification

**Created:** 2026-06-16
**Ambiguity score:** 0.08 (gate: <= 0.20)
**Requirements:** 5 locked

## Goal

Phase 29 closes v1.5 by producing named closure artifacts that re-run the full `AC-PIPE-*` / `AC-VAL-*` acceptance suite, reconcile the issue ledger and remaining `SI-*` entries, record the FUT-01 handoff, and explicitly reconcile the updated standard-gold completeness decision before any PSC/VAL-04 closure language changes.

## Background

Phase 29 follows Phases 25-28. Phase 25 created the issue-ledger machinery and lifecycle; Phase 26 landed DataLoader ingestion and selection contracts; Phase 27 landed sampling, precision, `dt_out`/stage-query, and global-scale contracts; Phase 28 landed and verified SCS, SASD, and IPR while user-deferring PSC/VAL-04.

The current authoritative planning state says Phase 28 is closed and Phase 29 is ready. It also still describes PSC as carried forward to a first-run sanity check "once the gold dataset (missing-67/OI-7b) is complete." During this spec round, the user clarified a newer locked premise: the full 184 standard-gold rerun has already been attempted; 117 staged outputs validate, 67 remain physically irreducible gold holes, and those 67 should be treated as permanent `gold_counterpart = absent` cases rather than as a future rerun backlog. Direct local observation agrees that the staging area contains outputs and manifest entries for all 184 documented IDs, with 117 validation passes and 67 failures; however, the canonical gold output folder and tracked planning artifacts have not yet been reconciled to that 184 -> 67 outcome. Phase 29 must surface and reconcile that stale-state boundary before using PSC/gold-completeness language as closure evidence.

The physics and engineering stakes behind the validation suite are:

- SCS is the data-side Hamiltonian relative-drift gate: `eps_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(eps_H)`, reject if `SCS > -5`.
- SASD is a scale-invariant local timestep adequacy diagnostic, using `dt * ||a|| / ||v||` at both interval endpoints to flag under-sampled close-encounter stiffness without rejecting a trajectory outright.
- IPR is a dimensionful acceleration-squared interpolation residual computed in raw `G = 1` units; the raw/scaled unit pin matters because the same numeric threshold differs by about 464x under the locked scale transform.
- PSC is a report-only occupancy-entropy diagnostic whose pooled population and weighting are sensitive to the final standard/gold population. It remains deferred until the 184 -> 67 gold-completeness reconciliation is made explicit in repo artifacts and the user reopens or resolves the PSC composition choice.

## Requirements

1. **Named closure artifacts**: Phase 29 produces concrete closure artifacts with stable names: `29-SPEC.md`, `29-UAT.md`, `29-HANDOFF.md`, and a FUT-01 divergence/handoff artifact.
   - Current: Phase 29 has no phase directory and no SPEC, UAT, or handoff artifact. Earlier phases recorded local summaries, but there is no Phase 29 closure surface.
   - Target: `.planning/phases/29-acceptance-checks-re-verification-and-handoff/` contains `29-SPEC.md`, `29-UAT.md`, `29-HANDOFF.md`, and a FUT-01 divergence/handoff artifact that downstream work can cite.
   - Acceptance: A structural check lists all named artifacts; each file states its source evidence, requirement coverage, and closure status.

2. **Full acceptance-suite rerun**: Phase 29 re-runs the full existing `AC-PIPE-*` and `AC-VAL-*` suite for confidence in the information and design, not merely a narrow terminal-state check.
   - Current: Individual phases recorded passing acceptance checks as their contracts landed, but v1.5 has no final full-suite rerun after Phase 28 closure and the 184 -> 67 gold-completeness clarification.
   - Target: `29-UAT.md` records a full rerun of every applicable `AC-PIPE-*` and `AC-VAL-*` acceptance check, naming the command or function, input data, pass criterion, result, and evidence location. Required checks that cannot be executed because their owning contract is user-deferred must be marked `DEFERRED` with the blocker and decision record.
   - Acceptance: `29-UAT.md` contains a pass/fail table for the full suite; every non-deferred row has an executed result, and every deferred row cites the exact blocker rather than being counted as passed.

3. **Issue-ledger closure**: Phase 29 closes the v1.5 issue ledger only after every in-scope row is at `VERIFIED` or explicitly documented `DEFERRED`.
   - Current: `24-ISSUE-LEDGER.md` records the Phase 25 lifecycle and many verified rows, with PSC/VAL-04 deferred. The ledger still needs final milestone-level closure after the full acceptance rerun.
   - Target: The issue ledger is reconciled against the final acceptance rerun results, stale or contradictory status notes are corrected, and no in-scope finding remains `PENDING`, `IN_PROGRESS`, or `FIX_APPLIED` at closure.
   - Acceptance: A ledger audit in `29-UAT.md` reports counts by status, identifies every `DEFERRED` row and its blocker, and confirms there are zero non-terminal in-scope rows.

4. **SI-ledger and FUT-01 handoff**: Phase 29 reviews `SI-DQA-002`, `SI-DQA-003`, and `SI-PINN-002`, then records v1.5 handoff decisions for fixed, intentionally unchanged, deferred, and FUT-01 implementation-shaped findings.
   - Current: The remaining Source-Issue entries were preserved through v1.4 and are explicitly assigned to Phase 29 by VER-12. DataLoader-implementation-shaped findings from v1.5 also need a clean FUT-01 handoff because v1.5 settles specs but does not implement production loader or training code.
   - Target: `29-HANDOFF.md` reviews each remaining `SI-*` entry for issue-02 relevance and either retires it with a resolving back-reference or preserves it with a written reason. The FUT-01 divergence/handoff artifact records every DataLoader, TrajectoryValidator, TrajectoryIndex, metric, data-format, and gold-counterpart implementation obligation that must be rebuilt from the settled specs.
   - Acceptance: `29-HANDOFF.md` has explicit rows for `SI-DQA-002`, `SI-DQA-003`, and `SI-PINN-002`; the FUT-01 handoff artifact has explicit rows for each implementation-shaped v1.5 finding, with no live `pinn/` code treated as grounding.

5. **Gold-completeness and PSC reconciliation**: Phase 29 reconciles the stale 184-missing/gold-completable planning state against the user-locked 184 -> 67 rerun outcome before changing PSC/VAL-04 status.
   - Current: Planning artifacts still describe PSC/VAL-04 as deferred until gold completeness is achieved, while the user clarified that the full 184 rerun already occurred and the residual 67 missing gold trajectories are permanent. Local staging evidence shows 184 staged outputs, 117 validation passes, 67 failures, 0 promoted into the final gold output folder.
   - Target: Phase 29 records the final standard-gold state as a milestone fact: which 117 outputs are validated/promoted or intentionally left staged, which 67 are permanent `gold_counterpart = absent`, and which planning/spec/ledger records are stale because they still assume 184 eventual gold completions. PSC remains `DEFERRED` unless the user explicitly reopens and resolves GAP-28-03 / VAL-04 after this reconciliation.
   - Acceptance: `29-UAT.md` includes a gold-completeness reconciliation table with counts, evidence paths, and the disposition of the 67 irreducible holes; any PSC/VAL-04 row remains `DEFERRED` with the updated blocker unless a separate user instruction resolves GAP-28-03.

## Boundaries

**In scope:**
- Create and maintain the Phase 29 closure artifacts: `29-SPEC.md`, `29-UAT.md`, `29-HANDOFF.md`, and one FUT-01 divergence/handoff artifact.
- Re-run the full applicable `AC-PIPE-*` and `AC-VAL-*` suite for confidence, recording commands/functions, data, pass criteria, results, and evidence.
- Reconcile the v1.5 issue ledger to terminal states (`VERIFIED` or explicitly documented `DEFERRED`).
- Review and reconcile `SI-DQA-002`, `SI-DQA-003`, and `SI-PINN-002` per VER-12.
- Record the FUT-01 implementation handoff for DataLoader-facing, TrajectoryValidator-facing, TrajectoryIndex-facing, metric, data-format, and gold-counterpart obligations.
- Reconcile the standard-gold 184 -> 67 rerun outcome against stale repo planning/spec records before using gold-completeness language in PSC closure.

**Out of scope:**
- Production DataLoader, TrajectoryValidator, TrajectoryIndex, training-loop, or live `pinn/` implementation work - v1.5 remains spec-side; FUT-01 implements.
- Inventing or landing a canonical PSC/VAL-04 composition - PSC remains user-deferred unless the user explicitly resolves GAP-28-03 after the gold-completeness reconciliation.
- Retrying the 67 irreducible gold failures as a gap-filling activity - the user has clarified they are permanent absent gold counterparts.
- Editing `sampling_method.md` or `data_quality_assessment.md` - SCOPE-08 and SCOPE-09 remain in force.
- Treating live `pinn/` code as grounding - SCOPE-10 remains in force.
- Maintaining LaTeX/PDF publication parity - final publication sync is deferred until later implementation/training stability.

## Constraints

- STOP protocol applies in full. Source-silent semantic, process-schema, or cross-phase decisions must be surfaced as gaps or explicit user decisions; Phase 29 must not silently resolve PSC composition or reinterpret the 67 permanent gold holes.
- The full acceptance-suite rerun must use disposable dataset and spec-consistency probes; probes must not touch `pinn/` production code.
- Required acceptance checks that cannot run because their contract is user-deferred must be recorded as `DEFERRED`, not `PASS`.
- Gold-completeness reconciliation must distinguish staged validation, promotion into canonical output folders, documentation updates, and normative spec/ledger updates. These are separate states and must not be collapsed.
- Commit hygiene follows project policy: explicit staging paths, `scripts/agent-commit`, agent ownership variables, and no broad staging.

## Acceptance Criteria

- [ ] `29-SPEC.md`, `29-UAT.md`, `29-HANDOFF.md`, and a FUT-01 divergence/handoff artifact exist under `.planning/phases/29-acceptance-checks-re-verification-and-handoff/`.
- [ ] `29-UAT.md` records a full rerun of every applicable `AC-PIPE-*` and `AC-VAL-*` check with command/function, data, pass criterion, result, and evidence path.
- [ ] The final issue-ledger audit shows every in-scope row at `VERIFIED` or explicitly documented `DEFERRED`, with zero `PENDING`, `IN_PROGRESS`, or `FIX_APPLIED` rows.
- [ ] `29-HANDOFF.md` explicitly reviews `SI-DQA-002`, `SI-DQA-003`, and `SI-PINN-002`, retiring or preserving each with a written reason.
- [ ] The FUT-01 handoff artifact identifies every v1.5 implementation-shaped contract and divergence obligation, without citing live `pinn/` code as grounding.
- [ ] The gold-completeness reconciliation records the 184 attempted reruns, 117 validated successes, 67 permanent absent gold counterparts, promotion/documentation status, and any stale repo artifacts requiring update.
- [ ] PSC/VAL-04 remains `DEFERRED` with an updated blocker unless a separate explicit user instruction resolves GAP-28-03 after gold-completeness reconciliation.
- [ ] Roadmap traceability is confirmed: all 36 v1.5 requirements map to exactly one phase, and Phase 29 covers VER-07, VER-08, VER-09, VER-11, and VER-12.

## Ambiguity Report

| Dimension           | Score | Min   | Status | Notes |
|---------------------|-------|-------|--------|-------|
| Goal Clarity        | 0.96  | 0.75  | met    | User confirmed concrete closure artifacts and full-suite confidence rerun; roadmap names ledger close, SI reconciliation, and handoff. |
| Boundary Clarity    | 0.92  | 0.70  | met    | PSC remains deferred unless separately reopened; FUT-01 implementation and live `pinn/` work excluded. |
| Constraint Clarity  | 0.86  | 0.65  | met    | STOP protocol, probe/no-`pinn` boundary, and gold-completeness reconciliation states are explicit. |
| Acceptance Criteria | 0.92  | 0.70  | met    | Pass/fail closure checks name artifacts, full rerun, ledger, SI, FUT-01, gold reconciliation, PSC, and traceability. |
| **Ambiguity**       | 0.08  | <=0.20| met    | Gate passed after one Socratic clarification round and evidence reconciliation. |

Status: met = meets minimum; below = planner treats as assumption.

## Interview Log

| Round | Perspective | Question summary | Decision locked |
|-------|-------------|------------------|-----------------|
| 1 | Researcher | Should Phase 29 lock concrete deliverable names now or only required contents? | Lock concrete artifacts: `29-SPEC.md`, `29-UAT.md`, `29-HANDOFF.md`, and a FUT-01 divergence/handoff artifact. |
| 1 | Simplifier | Should acceptance execution rerun the full existing suite or only closure probes? | Re-run the full existing `AC-PIPE-*` and `AC-VAL-*` suite for confidence in the information and design. |
| 1 | Boundary Keeper | Should PSC be phrased as deferred until future gold completion? | No. The user clarified the full 184 standard-gold rerun has occurred; residual missing gold parts are permanent. Phase 29 must reconcile stale repo state to the 117 success / 67 permanent-absent outcome before any PSC status change. |
| 1 | Failure Analyst | What repo evidence contradicts or qualifies the user's PSC clarification? | Local staging has 184 outputs and manifest entries, 117 validation passes, 67 failures, and 0 promoted final outputs; tracked planning still says PSC waits for gold completion. Phase 29 must reconcile those states explicitly. |

---

*Phase: 29-acceptance-checks-re-verification-and-handoff*
*Spec created: 2026-06-16*
*Next step: $gsd-discuss-phase 29 - implementation decisions (how to build what's specified above)*
