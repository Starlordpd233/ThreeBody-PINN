# Phase 28: Validation-Metrics Contracts - Specification

**Created:** 2026-06-14
**Ambiguity score:** 0.13 (gate: <= 0.20)
**Requirements:** 4 locked

## Goal

Framework specs carry one canonical, data-side contract for each of the four validation metrics - SCS, SASD, IPR, and PSC - threshold-aligned to the locked post-v1.3 gate and the v1.4 physics outcomes, with every training-loop usage deferred to the doc-03 milestone via recorded forward-references.

## Background

Phase 28 continues the v1.5 post-gate adjudication sequence after Phase 27, under the Phase 25 machinery (evidence packet before any spec edit, same-commit ledger wiring, phase-exit only at `VERIFIED`/`DEFERRED`). Phase 27 landed the four sampling/precision/metadata/global-scale contracts (PIPE-04/07/08/09); its PIPE-09 spec edit fixed `compute_globals` to the v1.4 raw-mass PHYS-01 D convention and explicitly left the SCS threshold definition to Phase 28. The SCS definition therefore consumes the now-locked Phase 27 global-scale contract.

The four validation metrics are currently defined only in non-editable sources: the read-only `data_quality_assessment.md` (DQA - a non-authoritative research report, but per the resolution doc the sole written home of the locked SCS gate and the SASD/IPR/PSC definitions) and the non-authoritative issue-02. They are NOT yet carried as canonical contracts in the editable framework specs (`ctl_instruction.md`, `pinn_architecture.md`).

Grounded anchors for the four contracts:
- **SCS** is currently `SCS = log10(epsilon_H)` with the locked post-v1.3 gate `\epsilon_H > 10^{-5}` / `SCS > -5`. issue-02 carries conflicting ratio-based thresholds (`SCS > 1e-6` / `< 1e-8`); Phase 25 recorded this as an EVID-10 conflict to be resolved (not transcribed), with the spec edit landing in Phase 28 (VAL-01).
- **SASD** (Stiffness-Aware Sampling Density) is defined in the DQA with a low-resolution floor-effect caveat; its training-side collocation use (M16) is out of scope.
- **IPR** is defined in the DQA as an interpolation physics residual with a dual-epsilon construction; its ALM noise-floor role is training-side and out of scope.
- **PSC** is defined in the DQA as a dataset-level, report-only phase-space coverage measure (Shannon occupancy entropy); its replay-governance use is training-side and out of scope.

The consolidated resolution doc (candidate verdict source) resolved the validation cluster as Q-C1 (SCS), Q-C2 (SASD), Q-C3 (IPR), Q-C4 (PSC) and explicitly **flags genuine forks** that it did not consider settled: Q-C2 SASD endpoint choice (both-endpoints vs left-endpoint, "flagged for sign-off"), Q-C3 IPR units (raw vs scaled, an approximately 464x gate difference - "the consequential one", adopted on a placement inference with a calibration tripwire), and Q-C4 PSC composition (a dedup-plus-weighting synthesis "present in neither input", with a verification run specified). These forks are adjudicated during execution against the dataset and first principles under the EVID-10 / Phase 25 protocol - and surfaced to the user where the resolution doc requests sign-off - rather than pre-decided here.

## Requirements

1. **Canonical SCS contract** (VAL-01): Framework specs carry exactly one SCS contract whose definition and threshold align with the locked post-v1.3 gate, with the issue-02 ratio-based thresholds resolved through the EVID-10 record rather than transcribed.
   - Current: SCS is defined only in the read-only DQA (`SCS = log10(epsilon_H)`, gate `\epsilon_H > 10^{-5}` / `SCS > -5`) and the non-authoritative issue-02, which carries conflicting ratio-based thresholds (`SCS > 1e-6` / `< 1e-8`). The editable framework specs carry no canonical SCS contract; Phase 27 PIPE-09 left SCS to this phase.
   - Target: `ctl_instruction.md` (and/or `pinn_architecture.md`) carries one canonical SCS contract - definition and threshold aligned with `\epsilon_H > 10^{-5}` / `SCS > -5`; the issue-02 ratio thresholds are adjudicated through the EVID-10 record (verified, corrected, or rejected), not transcribed.
   - Acceptance: AC-VAL-01 passes by showing the framework spec states a single SCS definition and threshold aligned to `\epsilon_H > 10^{-5}` / `SCS > -5`, the issue-02 ratio thresholds do not appear as the canonical threshold, and an EVID-10 conflict record backs the adjudication.

2. **SASD contract** (VAL-02): Framework specs define SASD with its formula, its data-side computation contract, and the low-resolution floor-effect caveat, with training-side collocation weighting deferred to doc-03.
   - Current: SASD is defined only in the read-only DQA; the editable specs carry no SASD contract. The resolution doc flags a Q-C2 fork (both-endpoints vs left-endpoint formula) for evidence-backed sign-off.
   - Target: framework specs define SASD with its formula, its data-side computation contract, and the low-resolution floor-effect caveat; training-side collocation weighting is deferred to the doc-03 milestone via a recorded forward-reference.
   - Acceptance: AC-VAL-02 passes by showing the spec carries a SASD formula, a data-side computation contract, the low-resolution floor-effect caveat, and a doc-03 forward-reference for collocation weighting, with the Q-C2 endpoint choice backed by the EVID-10 record (or surfaced as a gap).

3. **IPR contract** (VAL-03): Framework specs define IPR with its formula and dual-epsilon consistency with the v1.4 PHYS-03 outcome, with its ALM noise-floor role recorded as a doc-03 forward-reference.
   - Current: IPR is defined only in the read-only DQA (an interpolation physics residual of the form `IPR = (1/M) * sum_k || q''_spline(tau_k) - F_gravity^{eps}(q_spline(tau_k)) ||^2`); the editable specs carry no IPR contract. The resolution doc flags Q-C3 units (raw vs scaled, ~464x gate difference) as the consequential fork.
   - Target: framework specs define IPR with its formula and its dual-epsilon consistency with the v1.4 PHYS-03 softening outcome; its ALM noise-floor role is recorded as a doc-03 forward-reference.
   - Acceptance: AC-VAL-03 passes by showing the spec carries an IPR formula, dual-epsilon consistency with the PHYS-03 outcome, and a doc-03 forward-reference for the ALM noise-floor role, with the Q-C3 unit choice backed by the EVID-10 record (or surfaced as a gap).

4. **PSC contract** (VAL-04): Framework specs define PSC with its formula and its data-side computation contract, with replay-governance use deferred to doc-03.
   - Current: PSC is defined only in the read-only DQA (a dataset-level, report-only phase-space occupancy measure); the editable specs carry no PSC contract. The resolution doc flags Q-C4 (dedup-plus-weighting composition) as a synthesis present in neither consolidation input, with a verification run specified.
   - Target: framework specs define PSC with its formula and its data-side computation contract; its replay-governance use is deferred to the doc-03 milestone via a recorded forward-reference.
   - Acceptance: AC-VAL-04 passes by showing the spec carries a PSC formula, a data-side computation contract, and a doc-03 forward-reference for replay-governance use, with the Q-C4 composition backed by the EVID-10 record / specified verification run (or surfaced as a gap).

## Boundaries

**In scope:**
- Adjudicate and land framework-spec contracts for VAL-01, VAL-02, VAL-03, and VAL-04 (SCS, SASD, IPR, PSC) - data-side definitions only.
- Consume the read-only DQA metric texts, issue-02 (non-authoritative), the consolidated resolution doc (candidate verdict source), the on-disk dataset / `simulation_data/Scripts/`, and Phase 25 evidence packets / EVID-10 records as grounding before any spec edit.
- Resolve the issue-02 ratio-based SCS thresholds through the EVID-10 record against the locked gate (VAL-01), not by transcription.
- Record doc-03 forward-references for every deferred training-loop usage (SASD-weighted collocation/M16, IPR-as-ALM-noise-floor, PSC-governed replay).
- Update the Phase 24 issue-ledger rows for the VAL findings per the Phase 25 lifecycle; define and execute per-finding acceptance checks (AC-VAL-01..04) before marking rows `VERIFIED`.
- Re-verify previously verified Phase 26/27 findings only where a Phase 28 edit could regress a shared spec section (notably the PIPE-09 global-scale contract that feeds SCS).

**Out of scope:**
- Training-loop usage of any metric - SASD-weighted collocation (M16), IPR-as-ALM-noise-floor, PSC-governed curriculum replay - deferred to the doc-03 milestone (SCOPE-11, resolution-doc OI-10); Phase 28 records only the forward interface.
- FUT-01 DataLoader implementation or live `pinn/` code changes - v1.5 is spec-side and live `pinn/` code is not grounding (SCOPE-10).
- Edits to `data_quality_assessment.md` - read-only under SCOPE-09 (it remains the cited written home of the metric definitions, characterized not edited).
- Changes to `sampling_method.md` - frozen by default under SCOPE-08 unless the user explicitly instructs otherwise.
- Re-opening the Phase 27 PIPE-09 global-scale convention - locked in Phase 27; Phase 28 consumes it for SCS but does not re-decide it.
- Milestone-wide acceptance-check execution, ledger close, SI-ledger reconcile, and FUT-01 handoff - owned by Phase 29 (VER-07/08/09/11/12).

## Constraints

- STOP protocol applies in full: source-silent semantic, process-schema, or cross-phase decisions are recorded as gaps and surfaced to the user, never invented. In particular, the resolution-doc forks Q-C2 (SASD endpoints), Q-C3 (IPR units), and Q-C4 (PSC composition) are flagged by the resolution doc itself for evidence-backed adjudication / sign-off - they must be settled against the dataset and first principles, and surfaced where the resolution doc requests sign-off, not adopted on the resolution doc's authority alone.
- Source hierarchy follows v1.5 governance: resolution doc is the candidate verdict source (not authoritative); issue-02 is non-authoritative; the read-only DQA is the cited written home of the metric definitions and the locked SCS gate; on-disk dataset and `simulation_data/Scripts/` are grounding; live `pinn/` code is not grounding.
- Spec-edit targets are `ctl_instruction.md` and `pinn_architecture.md` only, unless the user explicitly changes scope.
- Physics-consistency invariants: the SCS threshold must remain consistent with the locked post-v1.3 gate (`\epsilon_H > 10^{-5}` / `SCS > -5`); IPR must remain consistent with the v1.4 PHYS-03 dual-epsilon softening outcome; SCS consumes the Phase 27 PIPE-09 raw-mass global-scale convention.
- Phase 28 preserves the Phase 25 issue-ledger lifecycle (`PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, or explicit `DEFERRED`) and the same-commit ledger-wiring discipline; every acceptance-check claim names the exact evidence packet, spec section, and pass/fail check.

## Acceptance Criteria

- [ ] AC-VAL-01 verifies one canonical SCS contract in the framework specs: a single definition and threshold aligned to `\epsilon_H > 10^{-5}` / `SCS > -5`, the issue-02 ratio thresholds not transcribed as the canonical threshold, and an EVID-10 record backing the adjudication.
- [ ] AC-VAL-02 verifies the SASD contract: formula, data-side computation contract, low-resolution floor-effect caveat, and a doc-03 forward-reference for collocation weighting.
- [ ] AC-VAL-03 verifies the IPR contract: formula, dual-epsilon consistency with the v1.4 PHYS-03 outcome, and a doc-03 forward-reference for the ALM noise-floor role.
- [ ] AC-VAL-04 verifies the PSC contract: formula, data-side computation contract, and a doc-03 forward-reference for replay-governance use.
- [ ] Each resolution-doc fork consumed by Phase 28 (Q-C2 SASD endpoints, Q-C3 IPR units, Q-C4 PSC composition) is either backed by an EVID-10 record / evidence packet or surfaced as a gap for user decision - none adopted silently.
- [ ] The Phase 24 issue-ledger rows touched by Phase 28 end in `VERIFIED` or explicitly documented `DEFERRED`, with evidence-packet links and last-updated dates.
- [ ] Previously verified Phase 26/27 rows are re-checked where a Phase 28 edit touches a shared spec section (notably the PIPE-09 global-scale contract feeding SCS).

## Ambiguity Report

| Dimension           | Score | Min   | Status | Notes |
|---------------------|-------|-------|--------|-------|
| Goal Clarity        | 0.92  | 0.75  | met    | Four named metrics (SCS/SASD/IPR/PSC) with explicit per-metric success criteria in ROADMAP Phase 28 and REQUIREMENTS VAL-01..04. |
| Boundary Clarity    | 0.90  | 0.70  | met    | SCOPE-11 doc-03 boundary + per-requirement training-loop deferrals + two-file edit limit (SCOPE-08/09/10) + Phase 29 handoff exclusion. |
| Constraint Clarity  | 0.82  | 0.65  | met    | Locked SCS gate, PHYS-03 dual-epsilon, PIPE-09 dependency, Phase 25 machinery, and the flagged resolution-doc forks are explicit. |
| Acceptance Criteria | 0.80  | 0.70  | met    | Per-contract structural checks (AC-VAL-01..04), explicit fork-handling, and ledger-closure checks are named. |
| **Ambiguity**       | 0.13  | <=0.20| met    | Auto-derived from locked roadmap + requirements; gate passed without an interview round. |

Status: met = meets minimum; below = planner treats as assumption.

## Interview Log

Run under `--auto`: no interactive interview. Decisions auto-locked from the locked planning artifacts (ROADMAP Phase 28, REQUIREMENTS VAL-01..04, SCOPE-11) under the v1.5 STOP protocol; no source-silent semantic decision was required to write this spec.

| Round | Perspective         | Question summary | Decision locked |
|-------|---------------------|------------------|-----------------|
| 1 | Researcher (auto)       | What does Phase 28 "done" mean? | Four data-side metric contracts (SCS/SASD/IPR/PSC) landed in `ctl_instruction.md`/`pinn_architecture.md`, each with an evidence packet, an AC-VAL check, and an issue-ledger row at `VERIFIED`/`DEFERRED`; milestone-wide acceptance stays with Phase 29. Grounding: ROADMAP Phase 28 + VAL-01..04. |
| 2 | Simplifier (auto)       | Irreducible core? | One canonical contract per metric (definition/formula + data-side computation + threshold/consistency); nothing training-side. Grounding: VAL-01..04 + SCOPE-11. |
| 3 | Boundary Keeper (auto)  | What is explicitly NOT Phase 28? | Training-loop usage (M16/ALM/replay) -> doc-03; DQA read-only; `sampling_method.md` frozen; PIPE-09 not re-opened; Phase 29 owns acceptance/handoff. Grounding: SCOPE-08/09/10/11, OI-10. |
| 4 | Failure Analyst (auto)  | What would invalidate the contracts? | Silently adopting a resolution-doc fork (Q-C2/C3/C4) or transcribing the issue-02 ratio thresholds; each fork must be EVID-10-backed or surfaced as a gap, and the SCS threshold must stay consistent with the locked gate. Grounding: VAL-01 ("not transcribed"), resolution-doc fork flags, STOP protocol. |

---

*Phase: 28-validation-metrics-contracts*
*Spec created: 2026-06-14*
*Next step: /gsd-discuss-phase 28 - implementation decisions (how to build what's specified above)*
