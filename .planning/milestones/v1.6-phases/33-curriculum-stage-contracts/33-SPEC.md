# Phase 33: Curriculum-Stage Contracts - Specification

## Goal

Phase 33 makes `ctl_instruction.md` state one coherent set of curriculum-stage
contracts: adaptive stage assignment, `tau_L` / `L_max` computation, dual-path
stage transitions, the Stage 0-6 inventory and gates, and the `s_min` stage-gate
frame.

The contracts must be grounded in Phase 32 verdicts, v1.5-verified dataset facts,
locked v1.4/v1.5 conventions, and the resolved Phase 33 gap entries. They are
spec contracts only: the admitted-set EDA run, Stage-0 pilot calibration, training
loop implementation, and any data regeneration remain FUT work.

## Background

- Phase 33 is the first v1.6 contract transcription phase after Phase 32's
  evidence framework. It consumes Phase 32's ledger, evidence packets, and
  owner-ratified decisions before planning any framework-spec edits.
- The roadmap and requirements define the phase as `CURR-01` through `CURR-05`
  and limit v1.6 spec edits to `ctl_instruction.md` and, when necessary,
  `pinn_architecture.md`.
- Existing Phase 33 STOP gaps `GAP-33-01`, `GAP-33-02`, and `GAP-33-03` are
  `RESOLVED-WITH-INSTRUCTION` and supersede earlier roadmap / requirements
  phrasing where those sources made owner-pending values look locked.
- The UI plan gate currently reports a frontend block for this phase, but the
  roadmap's Phase 33 `UI hint` is `no` and the phase has no frontend deliverable.
  Planning may use `--skip-ui` for this phase rather than generating a UI-SPEC.

## Requirements

### R1. Adaptive stage-assignment contract (`CURR-01`)

The framework specs must define data-driven adaptive stage assignment as an
offline methodology contract:

- admitted-set EDA, robust transforms, PCA, clustering, and quantile thresholds
  may calibrate or augment the static theoretical anchors;
- stable integer labels must be materialized by `record_key`;
- existing Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement
  roles must not be erased by adopting `stage_strat_revision.md` Table 4
  wholesale;
- the per-stage population safeguard value is owner-pending after the FUT
  admitted-set EDA and must not be locked as 5%, `>10%`, or an adaptive rule in
  Phase 33.

### R2. `L_max`, `tau_L`, and staging-metadata contract (`CURR-02`)

The framework specs must define:

- `L_max` as the characteristic angular-momentum scale, not a proven global
  maximum;
- the current formula as `L_max = M_tot * r_char * sqrt(2 * |E| / M_tot)`,
  equivalent to `M_total * r_char * v_char` when `v_char` is the characteristic
  speed;
- the v1.5-locked raw-mass `D ~= 4.6416` convention as the active scale and the
  issue-doc `D = 6.694` claim as rejected;
- `tau_L` as staging / evaluation metadata, deliberately excluded from `IC13`;
- the current Rosenstein-style trajectory estimator as a revisable baseline
  only.

The shadow-trajectory method, `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10`
parameters, time-unit convention, fit windows, uncertainty handling, final stage
thresholds, and fast PCA+Rosenstein shortcut remain owner-pending or rejected as
normative contracts per `GAP-33-02`.

### R3. Dual-path stage-transition contract (`CURR-03`)

The framework specs must define a stage-transition state machine:

- **ADVANCE:** allowed only when the approved success gate passes, including
  training plateau, validation stability, and stage-dependent physics-residual
  and energy-drift criteria;
- **RECOVER:** used for NaN/Inf rollback and bounded retry;
- **HALT/REVIEW:** used for max-epoch or stagnation unless the owner explicitly
  authorizes degraded advancement.

Thresholds, epoch tables, stagnation windows, retry limits, and percentile
relaxation values are provisional pending FUT Stage-0 pilot calibration.

### R4. Stage 0-6 inventory and gating contract (`CURR-04`)

The framework specs must define the Stage 0-6 inventory, per-stage criteria,
cumulative replay behavior, and Stage-6 catch-all handling. The contract must:

- store raw, unclipped `L_norm` as staging / diagnostic metadata;
- require explicit nonfinite and near-degenerate `L_max` handling;
- state that no global `L_norm` clamp is authorized;
- state that the M6 `np.clip(L_norm, 0, 1)` stage-gate is not locked and remains
  owner-pending admitted-set evidence;
- cite stage trajectory counts as v1.5-verified only when those counts have
  verified support, otherwise mark them as claimed / FUT.

### R5. `s_min` curriculum stage-gate frame (`CURR-05`)

The framework specs must define the curriculum stage gate using unsoftened
geometric `s_min` for the Stage-6 collision gate. Loss-side matched-Plummer
softening remains distinct and belongs to Phase 35. The unsoftened value must be
logged for diagnostics.

### R6. Source discipline and STOP behavior

Phase 33 must not invent source-silent semantic or process-artifact decisions.
If a required contract point is not answered by the accepted sources, resolved
gap notes, or locked v1.4/v1.5 conventions, work that depends on it must stop and
the gap must be recorded in `33-GAPS.md` and the v1.6 milestone gap index.

## Boundaries

### In scope

- Planning and execution for Phase 33 artifacts under
  `.planning/phases/33-curriculum-stage-contracts/`.
- Framework-spec edits to `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  for the curriculum-stage contracts above.
- Narrow `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  cross-links only when required to keep the existing architecture contract
  consistent with the curriculum-stage text.
- Evidence-backed acceptance checks for the Phase 33 spec edits.
- Updates to Phase 32 / Phase 33 issue-ledger status only when the Phase 33 plan
  explicitly requires lifecycle synchronization for consumed rows.

### Out of scope

- Editing `sampling_method.md`, `data_quality_assessment.md`,
  `review-of-framework.md`, or `stage-strat-revision.md`.
- Editing or using `pinn/` live code as grounding.
- Running admitted-set EDA, Stage-0 pilot calibration, dataset regeneration, or
  training-loop experiments.
- Implementing training-loop code, DataLoader changes, causal windows, ALM, loss
  schedules, or replay/lookahead batching.
- Locking owner-pending values: population safeguard, final `tau_L` estimator /
  units / thresholds, clipped `L_norm` gate, or Stage-0 pilot thresholds.
- Resolving Phase 34 training-loop contracts or Phase 35 loss contracts beyond
  explicit handoff notes needed to avoid contradiction.

## Constraints

- Source hierarchy and STOP protocol in `AGENTS.md` are mandatory.
- v1.6 is specwork-only; framework spec targets are `ctl_instruction.md` and
  limited `pinn_architecture.md` cross-links.
- The issue doc and resolution doc are candidate / non-authoritative sources;
  locked v1.4 and v1.5 outcomes constrain interpretation.
- Phase 33 must consume Phase 32's D-05 owner instruction: unsoftened geometric
  `s_min` for the curriculum stage gate, with loss-side matched-Plummer
  softening kept separate.
- Phase 33 must consume Phase 32's D-06 owner instruction only where static
  invariants affect curriculum metadata: offline invariants retain
  `epsilon_inv = 1e-10`; training keeps `epsilon_train = 1e-5`.
- Commits must use `scripts/agent-commit` with explicit owned paths; unrelated
  dirty files must not be staged.

## Acceptance Criteria

- [ ] `33-SPEC.md`, `33-CONTEXT.md`, and planning artifacts exist under
  `.planning/phases/33-curriculum-stage-contracts/`.
- [ ] Every `CURR-01` through `CURR-05` requirement appears in at least one
  Phase 33 plan's `requirements` field.
- [ ] Planned framework-spec edits target only `ctl_instruction.md` and any
  necessary `pinn_architecture.md` cross-links.
- [ ] The plan includes explicit checks proving that forbidden paths remain
  unmodified.
- [ ] The plan requires exact-source checks for the adaptive-stage assignment,
  `L_max` / `tau_L`, stage-transition state machine, Stage 0-6 inventory,
  raw-`L_norm` metadata / guard, and unsoftened `s_min` stage gate.
- [ ] The plan carries `GAP-33-01`, `GAP-33-02`, and `GAP-33-03` resolutions
  forward as constraints rather than reopening or silently overriding them.
- [ ] Any newly discovered source-silent semantic or process-artifact decision
  is recorded as a STOP gap before dependent spec edits proceed.
- [ ] No admitted-set EDA, Stage-0 pilot, dataset regeneration, or training-loop
  implementation is run during Phase 33.

## Edge Coverage

| Edge | Status | Required Handling |
|------|--------|-------------------|
| Population safeguard value (`5%` / `>10%` / adaptive) | backstop | Keep owner-pending after FUT admitted-set EDA; do not lock a value in Phase 33. |
| `tau_L` estimator / time units / thresholds | backstop | Retain Rosenstein-style baseline as revisable; do not adopt shadow/Benettin or PCA shortcut normatively. |
| `L_norm` exceeds 1 or `L_max` is nonfinite / near-degenerate | covered | Store raw `L_norm`; require explicit guard and diagnostics; no global clamp. |
| Stage-transition failure triggers | covered | Route failure through RECOVER or HALT/REVIEW, not degraded automatic advancement. |
| Stage count claims without v1.5 verification | backstop | Mark as claimed/FUT unless a verified source supports the count. |
| `s_min` loss-side vs stage-gate confusion | covered | Stage gate uses unsoftened geometric `s_min`; loss-side softening belongs to Phase 35. |
| UI plan-gate false positive | covered | Treat Phase 33 as non-frontend per roadmap `UI hint: no`; use `--skip-ui` during planning if needed. |

## Prohibitions (must-NOT)

- Must NOT lock the population safeguard value in Phase 33.
- Must NOT adopt `stage_strat_revision.md` Table 4 wholesale.
- Must NOT adopt the issue-doc shadow-trajectory method, the unspecified
  PCA+Rosenstein shortcut, or any final `tau_L` threshold as normative.
- Must NOT reintroduce `D = 6.694` as the active scale.
- Must NOT put `tau_L` or `L_norm` into `IC13`.
- Must NOT authorize a global `L_norm` clamp or lock `np.clip(L_norm, 0, 1)` as
  the stage gate.
- Must NOT soften the curriculum stage gate's `s_min` by assumption.
- Must NOT edit read-only reports, frozen specs, live `pinn/` code, or generated
  data.

## Ambiguity Report

| Dimension | Score | Min | Status | Notes |
|-----------|-------|-----|--------|-------|
| Goal Clarity | 0.93 | 0.75 | met | Roadmap and requirements name the five curriculum-stage contracts and target specs. |
| Boundary Clarity | 0.91 | 0.70 | met | v1.6 specwork-only scope, target files, forbidden files, and FUT exclusions are explicit. |
| Constraint Clarity | 0.89 | 0.65 | met | STOP protocol, source hierarchy, Phase 32 verdicts, and resolved Phase 33 gaps constrain the work. |
| Acceptance Criteria | 0.88 | 0.70 | met | Requirements map to five contract groups with concrete backstop checks. |
| **Ambiguity** | 0.09 | <=0.20 | met | Gate passed after applying resolved gap instructions and source-discipline constraints. |

Status: met = dimension meets the workflow minimum; no dimension is below
minimum.

## Interview Log

- **Initial assessment:** Phase 33 was underspecified where roadmap /
  requirements phrasing appeared to lock owner-pending values for population
  safeguard, `tau_L`, and `L_norm`.
- **Auto round:** Because `$gsd-spec-phase 33 --auto` was requested, the workflow
  selected the documented grounded defaults already recorded in `33-GAPS.md`:
  defer population-safeguard value, keep `tau_L` estimator owner-pending, and
  store raw `L_norm` while deferring any clipped gate.
- **Gate result:** The resolved gap notes plus Phase 32's D-05/D-06 owner
  instructions make the phase clear enough to proceed to discussion and
  planning. New source-silent decisions still trigger STOP.

---

*Phase: 33-curriculum-stage-contracts*
*Spec generated: 2026-06-22*
