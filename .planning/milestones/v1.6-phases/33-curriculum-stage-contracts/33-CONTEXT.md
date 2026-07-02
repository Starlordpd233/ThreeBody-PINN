# Phase 33: Curriculum-Stage Contracts - Context

**Gathered:** 2026-06-22
**Status:** Ready for planning
**Mode:** `$gsd-discuss-phase 33 --auto`

<domain>

## Phase Boundary

Phase 33 plans the v1.6 curriculum-stage spec edits. It will transcribe
grounded, owner-ratified curriculum contracts into `ctl_instruction.md`, with
limited `pinn_architecture.md` cross-links only when needed. It must not run the
admitted-set EDA, Stage-0 pilot, training loop, or any code/data implementation.

</domain>

<spec_lock>

## Requirements (locked via SPEC.md)

**6 requirements are locked.** See `33-SPEC.md` for full requirements,
boundaries, edge coverage, prohibitions, and acceptance criteria.

Downstream agents MUST read `33-SPEC.md` before planning or implementing.
Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Planning and execution for Phase 33 artifacts under
  `.planning/phases/33-curriculum-stage-contracts/`.
- Framework-spec edits to `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  for the curriculum-stage contracts.
- Narrow `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  cross-links only when required to keep the existing architecture contract
  consistent with the curriculum-stage text.
- Evidence-backed acceptance checks for Phase 33 spec edits.
- Phase 32 / Phase 33 issue-ledger lifecycle synchronization only where a Phase
  33 plan explicitly requires it.

**Out of scope (from SPEC.md):**
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

</spec_lock>

<decisions>

## Implementation Decisions

### Adaptive Stage Assignment

- **D-33-01:** Use the packet-first / defer-floor disposition from
  `GAP-33-01`: Phase 33 specifies admitted-set EDA, robust transforms, PCA,
  clustering, quantile thresholds, and stable `record_key` labels, but does not
  lock the population safeguard value.
- **D-33-02:** Do not adopt `stage_strat_revision.md` Table 4 wholesale because
  it erases existing Stage-2 hierarchical-gold and Stage-5 quasi-random-gold
  refinement roles.
- **D-33-03:** Treat the actual admitted-set EDA run and any population-floor
  owner policy as FUT, not Phase 33 execution.

### `L_max`, `tau_L`, and Metadata

- **D-33-04:** Use `L_max = M_tot * r_char * sqrt(2 * |E| / M_tot)` as a
  characteristic angular-momentum scale, not a global maximum.
- **D-33-05:** Preserve the v1.5-locked raw-mass `D ~= 4.6416` convention and
  reject `D = 6.694` for the active scale.
- **D-33-06:** Keep `tau_L` excluded from `IC13`; it is staging/evaluation
  metadata only.
- **D-33-07:** Retain the current Rosenstein-style estimator as a revisable
  baseline. Do not normatively adopt the issue-doc shadow method, its
  `epsilon_pert` / `epsilon_soft` parameters, or the unspecified PCA+Rosenstein
  shortcut.

### Stage Transitions

- **D-33-08:** Model transitions as an operational state machine:
  ADVANCE only on an approved success gate, RECOVER for NaN/Inf rollback and
  bounded retry, and HALT/REVIEW for max-epoch or stagnation unless the owner
  later authorizes degraded advancement.
- **D-33-09:** Keep all numeric thresholds, epoch tables, stagnation windows,
  retry limits, and percentile relaxations provisional pending FUT Stage-0 pilot
  calibration.

### Stage 0-6 Inventory and Gates

- **D-33-10:** Store raw, unclipped `L_norm` as staging / diagnostic metadata
  and require explicit nonfinite / near-degenerate `L_max` handling.
- **D-33-11:** Do not authorize a global `L_norm` clamp. Do not lock
  `np.clip(L_norm, 0, 1)` as the stage gate in Phase 33.
- **D-33-12:** Define the Stage 0-6 inventory, per-stage criteria, cumulative
  replay behavior, and Stage-6 catch-all while marking unverified trajectory
  counts as claimed / FUT.

### `s_min`, Epsilon, and Cross-Phase Handoffs

- **D-33-13:** Transcribe Phase 32's D-05 owner instruction: the curriculum
  Stage-6 collision gate uses unsoftened geometric `s_min`; loss-side
  matched-Plummer softening belongs to Phase 35.
- **D-33-14:** When static invariant epsilon appears in curriculum metadata,
  transcribe Phase 32's D-06 owner instruction: offline invariants retain
  `epsilon_inv = 1e-10`, while training keeps `epsilon_train = 1e-5`.
- **D-33-15:** Cross-link Phase 34 / Phase 35 responsibilities only as handoffs;
  do not plan their contracts as Phase 33 work.

### Planning Workflow

- **D-33-16:** The roadmap says Phase 33 has `UI hint: no`; if the plan-phase UI
  gate reports a frontend block, planning should proceed with `--skip-ui`.
- **D-33-17:** Plans must include forbidden-path guards for read-only reports,
  frozen specs, live `pinn/` code, and unrelated dirty files.

### the agent's Discretion

The planner may decide the number of Phase 33 plan files and task grouping, as
long as every `CURR-01` through `CURR-05` requirement appears in a plan
`requirements` field and the plan remains executable by `$gsd-execute-phase`.

</decisions>

<canonical_refs>

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase Requirements

- `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md` - Locked Phase 33
  requirements, boundaries, edge coverage, prohibitions, and ambiguity report.
- `.planning/ROADMAP.md` - v1.6 roadmap; Phase 33 goal, dependency, success
  criteria, and non-UI hint.
- `.planning/REQUIREMENTS.md` - `CURR-01` through `CURR-05`, `SCOPE-12`
  through `SCOPE-15`, and v1.6 traceability.
- `.planning/STATE.md` - Current project state and accumulated v1.6 decisions.
- `AGENTS.md` - STOP protocol, v1.6 source hierarchy, specwork-only boundary,
  and commit protocol.

### Phase 33 Gap Decisions

- `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md` - Resolved
  `GAP-33-01`, `GAP-33-02`, and `GAP-33-03`; these supersede older
  owner-pending phrasing.
- `.planning/milestones/v1.6-GAPS.md` - Milestone-wide gap index, if a new
  Phase 33 STOP gap must be added.

### Phase 32 Evidence and Ledger

- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md`
  - D-05 / D-06 owner decisions and downstream Phase 33 rows.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-05-s-min-frame.md`
  - D-05 evidence packet: unsoftened geometric stage gate and loss-side
  matched-Plummer separation.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-06-epsilon-strategy.md`
  - D-06 evidence packet: dual-context epsilon instruction for offline
  invariants vs training.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md`
  - Active raw-mass `D ~= 4.6416` convention and rejection of `D = 6.694`.

### Candidate and Readiness Sources

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`
  - Candidate resolution sections 1.2, 1.6, 1.7, 1.11, 1.15, and 1.17.
- `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md`
  - Finding map and Phase 33 direction preview.
- `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md`
  - READY-WITH-CAVEATS gate and caveats C-04, C-11, C-12 relevant to Phase 33.

### Framework Specs and Read-Only Sources

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` -
  Primary Phase 33 edit target.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` -
  Cross-link target only when needed for architectural consistency.
- `pinn_instruction/issues/03-curriculum-and-training-loop.md` -
  Non-authoritative issue document; use only through source hierarchy.
- `pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md`
  - Read-only source; do not adopt Table 4 wholesale.
- `pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md`
  - Read-only source.
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md`
  - Read-only source.

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- Phase 32 evidence packet and ledger artifacts show the expected adjudication
  style for line-range citations, before/after notes, acceptance checks, and
  STOP-safe owner routing.
- Existing GSD planning artifacts under Phase 32 show the expected PLAN task XML
  structure and validation strategy shape.

### Established Patterns

- Phase plans should use explicit `<read_first>`, `<action>`, `<verify>`, and
  `<acceptance_criteria>` blocks with concrete file paths and source assertions.
- Verification for specwork phases should be deterministic `rg` / `python3`
  source checks and forbidden-path guards, not runtime training probes.
- Commits must use `scripts/agent-commit` with owned paths; no broad staging.

### Integration Points

- The eventual Phase 33 execution integrates with `ctl_instruction.md` as the
  primary spec target.
- Any `pinn_architecture.md` edit must be a cross-link or consistency patch
  justified by the curriculum-stage contract.
- The Phase 32 issue ledger remains the coordination point for consumed rows and
  downstream Phase 34 / Phase 35 handoffs.

</code_context>

<specifics>

## Specific Ideas

- Treat owner-pending values as explicit contract holes with FUT owner routing,
  not as planner discretion.
- Use exact phrases in planned checks for high-risk prohibitions: `No global
  clamp is authorized`, `not a proven global maximum`, `revisable baseline`,
  `unsoftened geometric s_min`, and `epsilon_inv = 1e-10`.
- Plans should include a check that no Phase 33 diff touches read-only reports,
  frozen specs, live `pinn/` code, or the unrelated dirty docs plan.

</specifics>

<deferred>

## Deferred Ideas

- Admitted-set EDA and population-floor owner policy are FUT after Phase 33.
- Final `tau_L` estimator, time-unit convention, fit parameters, uncertainty
  flags, and thresholds are owner-pending.
- `np.clip(L_norm, 0, 1)` as a possible derived stage-gate value remains
  owner-pending admitted-set evidence.
- Stage-0 pilot calibration owns transition thresholds, stagnation windows, and
  retry limits.
- Phase 34 owns replay/lookahead batching, batch construction, collocation
  scaling, ALM, and training-side metric contracts.
- Phase 35 owns loss-side softened `s_min`, loss scaling, energy weighting,
  Huber delta, and causal training mode.

</deferred>

---

*Phase: 33-curriculum-stage-contracts*
*Context gathered: 2026-06-22*
