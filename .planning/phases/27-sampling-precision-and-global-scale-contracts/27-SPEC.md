# Phase 27: Sampling, Precision, and Global-Scale Contracts - Specification

**Created:** 2026-06-13
**Ambiguity score:** 0.13 (gate: <= 0.20)
**Requirements:** 4 locked

## Goal

Framework specs lock four data-side contracts for sampling, precision, metadata exposure, and global-scale computation, with each contract grounded in Phase 24 verified dataset facts, Phase 25 evidence packets, and v1.4 physics conventions before Phase 28 and FUT-01 depend on them.

## Background

Phase 27 continues the v1.5 post-gate adjudication sequence after Phase 26. Phase 26 already landed DataLoader ingestion and selection contracts for admission gating, ID resolution, blacklist exclusion, gold counterpart handling, footer metadata, and the user-locked HDF5 training-data format. Phase 27 owns the remaining pipeline contracts listed in `.planning/REQUIREMENTS.md` as PIPE-04, PIPE-07, PIPE-08, and PIPE-09.

The current framework specs still need the Phase 27 data-side contracts made explicit. Phase 24 verified the relevant empirical anchors: DATA-06 corrected the snapshot medians to 61 standard-base, 127 hierarchical-base, and 1003 gold; DATA-05 found 70 stale base-hierarchical mass mismatches, then the targeted rerun remediation validated 70/70 replacements at float64 mass equality. Phase 25 already recorded the M12 verdict as `accept-third-position`: use `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` sampled without replacement, default cap 32, and reject the unevidenced `0.5 * n_snapshots` factor. Phase 25 also recorded the `compute_globals` D conflict as `accept-resolution`, rejecting the issue-doc `D = 6.694` / `M_tot_ref` convention in favor of the v1.4 raw-mass PHYS-01 convention.

## Requirements

1. **Points-per-trajectory contract**: Framework specs define the M12 data-loss sampling rule as `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, sampled without replacement, with `n_pts_cap` defaulting to 32 as a configurable cap and no `0.5 * n_snapshots` factor.
   - Current: The roadmap still names the candidate `min(32, int(0.5 * n_snapshots))`, while the Phase 25 M12 evidence packet rejects the `0.5` factor and locks the third-position rule.
   - Target: `ctl_instruction.md` carries the adjudicated M12 contract, cites the verified DATA-06 snapshot distributions, exposes `n_snapshots(traj)` and `dt_out(traj)` as metadata, and states that the deferred M16 collocation-density question is not part of this phase.
   - Acceptance: AC-PIPE-04 passes by showing the framework spec states `min(n_pts_cap, n_snapshots)` without replacement, default cap 32, no `0.5 * n_snapshots` rule, and cites the M12 evidence packet plus DATA-06 medians.

2. **Precision and mass policy**: Framework specs define float64 as sufficient for data-side metrics and invariants, with `decimal.Decimal` allowed only as a failure classifier for the IC-to-Brutus t=0 mass gate, not as the normal parsing or metric-computation path.
   - Current: The issue doc proposed Decimal parsing if the mass probe mismatched; Phase 24 showed the 70 mismatches were stale base-hierarchical Brutus outputs, and the validated reruns passed mass equality at float64.
   - Target: `ctl_instruction.md` and any architecture-side precision note state that current IC masses are canonical, the old mismatching artifacts are not a precision failure, float64 is the validation metric contract, and Decimal is limited to diagnosing a future failed mass-gate comparison.
   - Acceptance: AC-PIPE-07 passes by showing the specs name float64 sufficiency, the Decimal-only-as-classifier policy, the DATA-05 rerun remediation evidence, and a fail condition for any future mass-gate mismatch.

3. **dt_out metadata and stage-query interface**: Framework specs define the data-side `dt_out` and stage-query contract: the DataLoader exposes per-trajectory `dt_out` and `n_snapshots` metadata and provides `sample_replay(n, max_stage)` plus `sample_lookahead(n, stage)` selection interfaces.
   - Current: Phase 26 footer handling already measures `dt_out` independently of footer/default metadata, but Phase 27 still needs the explicit data-side query contract and G5 closure path.
   - Target: `ctl_instruction.md` and `pinn_architecture.md` define the metadata fields and query interface as data-side contracts, while explicitly deferring M16 collocation scaling and training-loop use of those fields to the doc-03 milestone.
   - Acceptance: AC-PIPE-08 passes by showing the specs expose `dt_out` and `n_snapshots`, define both stage-query methods, preserve footer/default provenance rules from PIPE-06, and contain a doc-03 forward-reference for M16 rather than a training policy.

4. **Global-scale computation convention**: Framework specs define `compute_globals` consistently with the v1.4 raw-mass PHYS-01 D convention and explicitly reject the issue-doc `D = 6.694` / `M_tot_ref` recomputation claim.
   - Current: Phase 25 recorded the `compute_globals` conflict in `compute-globals-D.md` as `accept-resolution`, but the Phase 27 spec edit has not yet landed.
   - Target: `ctl_instruction.md` carries the global-scale contract using the raw-mass PHYS-01 convention, rejects `M_tot_ref` parameterization and `D = 6.694`, records the E-scale floor convention where relevant, and leaves Phase 28 SCS threshold definition to the validation-metrics phase.
   - Acceptance: AC-PIPE-09 passes by showing the framework spec matches the EVID-10 `compute-globals-D.md` verdict, rejects the issue-doc convention by name, and does not reintroduce `D = 6.694` or `M_tot_ref` as the canonical scale.

## Boundaries

**In scope:**
- Adjudicate and land framework-spec contracts for PIPE-04, PIPE-07, PIPE-08, and PIPE-09.
- Consume Phase 24 verified facts and Phase 25 evidence packets as grounding sources before any spec edit.
- Update the Phase 24 issue ledger rows for M12, G5, mass-drift/footer precision, and D=6.694 according to the Phase 25 lifecycle rules.
- Define and execute per-finding acceptance checks AC-PIPE-04, AC-PIPE-07, AC-PIPE-08, and AC-PIPE-09 before marking rows `VERIFIED`.
- Re-verify previously verified Phase 26 findings only where a Phase 27 edit could regress their contracts.

**Out of scope:**
- FUT-01 DataLoader implementation or live `pinn/` code changes - v1.5 is spec-side and live `pinn/` code is not grounding.
- doc-03 collocation-density, training-loop sampling, or M16 policy - Phase 27 only records the forward interface and defers the consuming policy.
- Phase 28 validation metric definitions for SCS, SASD, IPR, and PSC - those are owned by the next phase.
- Changes to `sampling_method.md` - frozen by default under SCOPE-08 unless the user explicitly instructs otherwise.
- Edits to `data_quality_assessment.md` - read-only under SCOPE-09.
- New processed-training-data format decisions - HDF5 was user-locked in Phase 26 under PIPE-10.

## Constraints

- STOP protocol applies in full: source-silent semantic, process-schema, or cross-phase decisions must be recorded as gaps and surfaced to the user.
- Source hierarchy follows v1.5 governance: resolution doc is the candidate verdict source, issue doc is non-authoritative, on-disk dataset and `simulation_data/Scripts/` are grounding, and live `pinn/` code is not grounding.
- Spec edit targets are `ctl_instruction.md` and `pinn_architecture.md` only, unless the user explicitly changes scope.
- Phase 27 must preserve Phase 26 verified contracts and the Phase 25 issue-ledger lifecycle: `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` or explicit `DEFERRED`.
- Any acceptance-check claim must name the exact evidence packet, spec section, and pass/fail command or check used to verify it.

## Acceptance Criteria

- [ ] AC-PIPE-04 verifies the M12 points-per-trajectory contract in the framework specs: `min(n_pts_cap, n_snapshots)`, no `0.5 * n_snapshots`, without-replacement sampling, default cap 32, and DATA-06 grounding.
- [ ] AC-PIPE-07 verifies the precision contract in the framework specs: float64 sufficiency, Decimal only as mass-gate failure classifier, DATA-05 rerun remediation consumed, and no stale-artifact interpretation as a precision failure.
- [ ] AC-PIPE-08 verifies the data-side `dt_out` and stage-query contract: per-trajectory `dt_out` and `n_snapshots` metadata, `sample_replay(n, max_stage)`, `sample_lookahead(n, stage)`, and doc-03 deferral for M16.
- [ ] AC-PIPE-09 verifies the global-scale contract: v1.4 raw-mass PHYS-01 D convention preserved, `D = 6.694` and `M_tot_ref` rejected by name, and Phase 28 SCS usage left to the validation-metrics phase.
- [ ] The Phase 24 issue ledger rows touched by Phase 27 end in `VERIFIED` or explicitly documented `DEFERRED`, with evidence packet links and last-updated dates.
- [ ] Previously verified Phase 26 rows are re-checked if a Phase 27 edit touches shared spec sections.

## Ambiguity Report

| Dimension           | Score | Min   | Status | Notes |
|---------------------|-------|-------|--------|-------|
| Goal Clarity        | 0.92  | 0.75  | met    | Four PIPE deliverables are named in roadmap and requirements. |
| Boundary Clarity    | 0.84  | 0.70  | met    | User approved the four-contract definition of done; out-of-scope list excludes FUT-01, doc-03, Phase 28, frozen/read-only specs. |
| Constraint Clarity  | 0.86  | 0.65  | met    | Grounding, STOP protocol, edit targets, and source hierarchy are explicit. |
| Acceptance Criteria | 0.80  | 0.70  | met    | Per-contract AC IDs and ledger closure checks are named. |
| **Ambiguity**       | 0.13  | <=0.20| met    | Gate passed after one interview round. |

Status: met = meets minimum; below = planner treats as assumption.

## Interview Log

| Round | Perspective | Question summary | Decision locked |
|-------|-------------|------------------|-----------------|
| 1 | Researcher | Should Phase 27 done mean four spec contracts landed, each with evidence/acceptance checks and ledger rows moved to `VERIFIED` or `DEFERRED`? | Yes. Phase 27 closes the four contract rows; Phase 29 still performs final milestone-wide acceptance. |
| 1 | Researcher | Can the M12, PIPE-07, and PIPE-09 conventions be treated as locked for the spec? | Yes. M12 uses `min(n_pts_cap, n_snapshots)` with cap 32 and no `0.5` factor; PIPE-07 uses float64 with Decimal only as classifier; PIPE-09 rejects `D = 6.694` and keeps the v1.4 raw-mass convention. |
| 1 | Researcher | Are there extra out-of-scope items beyond FUT-01 implementation, doc-03 training policy, Phase 28 metrics, frozen `sampling_method.md`, and read-only `data_quality_assessment.md`? | No additional exclusions were added; those boundaries are carried forward. |

---

*Phase: 27-sampling-precision-and-global-scale-contracts*
*Spec created: 2026-06-13*
*Next step: $gsd-discuss-phase 27 - implementation decisions (how to build what's specified above)*
