# Phase 68: Yardstick specification

**Created:** 2026-11-08
**Ambiguity score:** 0.070, gate at or below 0.20
**Requirements:** 3 locked, YARD-01 through YARD-03

## Goal

Produce a reproducible audit of the metrics that judge trajectory accuracy and
energy conservation, then use its evidence to support the owner's decisions
about energy measurement and the project's success criteria.

## Background

Phase 66 established a replicated single-orbit position fit with a smaller
network. It did not establish generalization to new initial conditions or
identify which of its changed settings enabled the fit. Phase 67 completed
the registered depth, learning-rate, time-input and window-length experiments.
Only the highest learning rate produced a confirmed effect, worsening the
fit. The other ladders remained unsettled at their registered budgets.

The frozen FEAS-01 scorer measures position error and uses explicit velocities
for tier-defining energy drift. The production validation gate and held-out
evaluator instead derive velocities by finite differences. GAP-59-08 records
that this route can fail even Brutus's correct trajectories. Conversely, a
constant position prediction can conserve its own energy perfectly while
predicting the orbit incorrectly. Energy conservation alone therefore cannot
establish trajectory accuracy.

The missing deliverable is a complete, committed, re-derivable known-answer
table across these measurement routes, including the floor at the native
0.01 gold cadence, followed by an evidence-based owner decision packet.
Phase 68 audits the existing definitions; finding a defective metric is a
valid audit result and does not authorize changing it.

### Owner direction

The owner selected option 3, leave the proof-of-concept target open until
Phase 68 presents its evidence, on 2026-11-08:

```owner-quote
option 3. We don't want to rush to making a conclusion. I think if Phase 68 can provide us with more evidence to help us gather more insight, I think that would definitely be my option as well.
```

This instruction fixes the sequence, evidence before conclusions. It selects
none of charter rows C-2 or C-4 through C-7 and changes no locked value.
Technical analysis proceeds under PROJECT.md's standing GSD decision
delegation. The expressly reserved owner checkpoint remains in force.

## Requirements

1. **YARD-01:** Audit every judging metric and gate on Brutus's exact answer and the constant predictor for Stage-0 training panel systems 1632, 851 and 4658, including the finite-difference energy-error floor at the native 0.01 gold cadence, and commit a re-derivable result table.
   - Current: The frozen scorer, production gate calculations, prior baseline
     records and GAP-59-08 exist. They do not yet constitute Phase 68's complete
     audit of both known answers across all required routes.
   - Target: A committed table and reproducible audit cover FEAS-01's
     position metrics, valid horizons, energy drift and tiers, plus the energy
     calculations used by the production validation gate and held-out
     evaluator. An inventory identifies each metric's definition, actual
     implementation, existing bar and gating or context-only role. Values
     without a ratified bar are labelled context, with no invented verdict.
   - Acceptance: Every required metric and gate has an identifiable result
     for both answers on all three systems. The table shows measured values,
     existing thresholds, observed verdicts and expected known-answer
     behavior, including discrepancies. It identifies the input records,
     sample counts, time ranges, grids, units, frames, masses, body order and
     velocity sources needed to reproduce each result. Audit evidence proves
     TRAIN-only access, no training and no held-out evaluation spend.

2. **YARD-02:** After the audit, present evidence-backed C-7 measurement options to the owner, record the owner's explicit choice verbatim, close GAP-59-08 only on that instruction, and route required amendments to v2.6.
   - Current: GAP-59-08 is OPEN. Charter C-7 offers autograd velocities,
     finite differences on a dense grid, or retaining the existing gate.
     None has been selected by this spec interview.
   - Target: A plain-language recommendation compares the charter's A, B and
     C against the committed audit, including what the gold-cadence result
     establishes and leaves unknown. The owner chooses at checkpoint 2.
     The ruling and the original gap register cite each other. Any resulting
     evaluator, validation-gate or framework-spec amendment is handed to v2.6.
   - Acceptance: The recommendation cites the audit and states its limits.
     The owner's C-7 answer is quoted verbatim and the gap is closed only
     with that instruction and its consequences recorded. If C-7 is left
     open, the gap remains OPEN and YARD-02 remains unsatisfied; the phase
     cannot silently close around it. Independent audit work may continue.

3. **YARD-03:** After the audit and with the C-7 disposition stated, present evidence-backed choices for C-2 and C-4 through C-6, record each owner answer verbatim or explicitly open, and route amendments to v2.6 without preselecting a success target or pass bar.
   - Current: The charter contains proposed definitions of done and position
     and energy bars, alongside the locked held-out bar. Those proposals are
     not owner decisions. Today's instruction leaves them open for evidence.
   - Target: A decision packet relates the project's recorded learning and
     proof-of-concept purpose, the frozen comparison points, the new audit
     and relevant published evidence to each choice. It distinguishes
     single-orbit fitting from generalization. The owner sets the acceptable
     outcome and bars, with undecided rows explicitly recorded as open.
   - Acceptance: C-2, C-4, C-5 and C-6 each have an evidence-backed
     recommendation, practical consequences, and a verbatim answer or an
     explicit open status. The C-5 recommendation states its dependency on
     C-7. Published comparisons cite their sources and task differences;
     they are not treated as directly transferable pass bars. Required
     amendments, including any C-6 replacement and the C-11 evaluation-text
     rewrite, are routed to v2.6 without editing the framework specs here.

## Boundaries

**In scope:**

- A read-only audit using the frozen scorer and the gate calculations called
  by production validation and evaluation, on the three Stage-0 TRAIN systems.
- Both known answers, with the constant predictor's definition inherited
  from the existing time-mean baseline and its matching window.
- True recorded Brutus velocities beside finite-difference velocities,
  clearly distinguished, and measurement at the native 0.01 gold cadence.
- An inventory, reproducible results, known-answer discrepancies and the
  evidence necessary for the C-7, C-2 and C-4 through C-6 recommendations.
- The owner checkpoint, original gap disposition and amendment handoff.

**Out of scope:**

- Training, extending Phase 67 runs or adding architecture experiments.
  The approved phase is a yardstick audit.
- New validation- or test-split data access, a graded run, or execution of
  the held-out evaluator. SCOPE-45 preserves the evaluation unspent.
- Repairs to production metrics, a re-freeze of FEAS-01, framework-spec
  edits, or moving locked values. SCOPE-46 routes amendments to v2.6.
- Inventing a dense trajectory, interpolating gold samples and calling them
  new evidence, or regenerating data. C-7 B is assessed using the required
  existing gold cadence, with any remaining uncertainty stated.
- A redesign decision, final cause verdict or commissioning trainex-r5.
  Those are Phase 69's owner checkpoint.
- Choosing the proof-of-concept target before the audit. The owner selected
  evidence-first sequencing and retains that decision.

## Constraints

- Preserve SCOPE-45 through SCOPE-49, the frozen scorecard, panel selection
  and prior evidence. Use this Mac; budget any proposed substantial work
  before running it under the existing governance.
- Exercise the shared calculations used by the production callers without
  invoking the single-use evaluation path or creating evaluation receipts.
  Demonstrate which caller and calculation each table entry covers.
- Retain the scorer's existing position definitions and inclusive tiers:
  Tier 1 at E <= 0.1, Tier 2 at E <= 0.01 and epsilon_H <= 1e-3,
  Tier 3 at E <= 0.01 and epsilon_H <= 1e-5. Finite-difference energy is
  context-only for FEAS-01 tiers. No context column becomes a new gate.
- Retain the production rejection rule epsilon_H > 1e-5, inclusive pass at
  equality, SCS = log10(epsilon_H), and worst-trajectory aggregation.
  Distinguish gate softening eps_inv = 1e-10 from training eps_soft = 1e-5.
- Preserve existing non-finite behavior. A non-finite energy drift fails
  the energy gate. Zero energy drift legitimately maps to SCS = -infinity;
  that is distinct from a non-finite energy drift. A zero initial-energy
  denominator is not silently repaired into a passing score.
- A known-answer audit result is evidence about the named metric, route
  and sampled trajectories. It does not establish that every model must
  fail or that an unsettled fit is mathematically impossible.
- New source-silent decisions follow the applicable STOP protocol.
  Implementation design and artifact schemas belong to discuss/plan-phase.

## Acceptance Criteria

- [ ] YARD-01 has a committed inventory and complete results for both known
  answers on systems 1632, 851 and 4658, with every metric's bar or
  context-only role and the production caller it represents identified.
- [ ] Reference-versus-reference position error is checked against its
  known zero answer. All existing accuracy bars reject the constant
  predictor, or each discrepancy is explicitly reported as an audit finding.
- [ ] Every bar passed by the constant predictor is reported, including
  conservation measured relative to that prediction's own initial energy.
- [ ] The native 0.01 gold-cadence finite-difference energy floor is measured
  on all three systems beside the value from recorded Brutus velocities.
  Coarser-grid historical results are labelled separately, not substituted.
- [ ] The committed record identifies data, code and scorecard versions and
  the commands and input conventions needed to reproduce its table.
- [ ] Threshold checks preserve equality and either-side behavior for the
  existing tiers and energy gate. Horizon crossing remains strictly above
  its existing delta; the aggregate uses the worst trajectory, not a mean.
- [ ] Missing required rows, refused inputs, zero denominators and
  non-finite measurements cannot be omitted or counted as successful
  coverage. Existing refusal or failure behavior is retained and reported.
- [ ] Equal numeric results retain their system, prediction, metric and
  velocity-route identities. Presentation order does not merge or reassign
  a result. Rounded display values do not determine pass/fail.
- [ ] Frame, time normalization, grid, body order, masses and velocity
  sources match the existing contracts and are labelled in the evidence.
- [ ] The audit demonstrates zero validation/test-split opens, zero training,
  no graded run and no invocation or receipt of the preserved evaluation.
- [ ] The C-7 recommendation follows the committed audit and compares A,
  B and C with evidence and uncertainty. Its ruling quotes the owner's
  explicit C-7 answer; only then is GAP-59-08 closed with a cross-reference.
- [ ] If the owner has not answered C-7, the gap stays OPEN and YARD-02
  stays unsatisfied. Re-running the audit cannot supply or alter that answer.
- [ ] C-2, C-4, C-5 and C-6 each have a recommendation with evidence,
  consequences and a verbatim answer or explicit open status. Re-presenting
  the packet does not turn an open row into an approved recommendation.
- [ ] C-6 and C-7 each require their own explicit answer under the charter's
  reply rule. The option 3 interview answer or blanket approval of other
  rows is not counted as either answer.
- [ ] The amendment handoff identifies each affected contract, the owner
  instruction it follows and its v2.6 destination. Production metrics,
  framework specs, frozen definitions and prior results remain unchanged.
- [ ] The report must not hide a correct-answer failure, omit a constant
  predictor's passing conservation result, or present conservation alone
  as evidence of trajectory accuracy.
- [ ] Recommendations must not present an unsettled Phase 67 result as a
  confirmed cause, a TRAIN-only fit as new-IC generalization, or the sampled
  finite-difference floor as a proof of representational impossibility.
- [ ] The decision record must not invent a success target, numeric bar,
  C-6/C-7 answer or gap closure from silence or from today's sequencing choice.

## Edge Coverage

**Coverage:** 15/15 applicable edges resolved, 0 unresolved.

The canonical edge-probe engine proposed 14 rows. Manual review added the
YARD-01 representation edge. All are resolved with verification: explicit,
through the acceptance criteria above. Technical dispositions apply the
existing contracts under PROJECT.md's standing delegation; no new numeric
default or owner choice is selected. Engine shapes are numeric-range,
collection and io for YARD-01, and text and stateful for YARD-02 and YARD-03.

| Category | Requirement | Status | Verification | Resolution / Reason |
|---|---|---|---|---|
| boundary | YARD-01 | resolved | explicit | Existing threshold equality and either-side semantics, strict horizon crossing and worst-case aggregation remain explicit. |
| adjacency | YARD-01 | resolved | explicit | Equal values from different systems, predictions or velocity routes remain distinct labelled results. |
| empty | YARD-01 | resolved | explicit | Missing rows, refused inputs, zero denominators and non-finite results cannot disappear or count as passing coverage. |
| ordering | YARD-01 | resolved | explicit | Presentation order cannot change row identity, body order or worst-case aggregation. |
| precision | YARD-01 | resolved | explicit | Existing numerical conventions and non-finite behavior remain; rounded displays never drive verdicts. |
| concurrency | YARD-01 | resolved | explicit | Read-only audit calculations do not invoke the held-out path, write its receipt or authorize other work. |
| encoding | YARD-01 | resolved | explicit | Manually raised: frame, time normalization, grid, body order, masses and velocity-source labels identify each measurement. |
| empty | YARD-02 | resolved | explicit | An absent C-7 answer leaves GAP-59-08 OPEN and YARD-02 unsatisfied. |
| encoding | YARD-02 | resolved | explicit | Capture the owner's C-7 answer verbatim, separately from the agent recommendation. |
| idempotency | YARD-02 | resolved | explicit | Re-running an audit cannot supply or change an owner answer or silently close the gap. |
| concurrency | YARD-02 | resolved | explicit | Commit evidence before the recommendation; owner instruction precedes closure; independent audit work remains allowed. |
| empty | YARD-03 | resolved | explicit | An unanswered charter row is explicitly open; its proposed answer is not approval. |
| encoding | YARD-03 | resolved | explicit | Record each owner answer verbatim and attach it to the named charter row. |
| idempotency | YARD-03 | resolved | explicit | Re-presenting the packet does not promote open rows to accepted choices. |
| concurrency | YARD-03 | resolved | explicit | Evidence precedes decisions; C-5 states the C-7 dependency; amendments follow instruction and go to v2.6. |

## Prohibitions

**Coverage:** 3/3 applicable prohibitions resolved, 0 unresolved.

The adversarial recall pass considered each requirement, then removed routine
engineering concerns already covered by the edge criteria. The retained
items concern truthful scientific reporting and the owner's authority.
They use verification: judgment because interpretation and fidelity to an
owner's instruction require review, not a text-matching assertion.

| Prohibition | Requirement | Status | Verification / Reason |
|---|---|---|---|
| MUST NOT conceal a correct-answer failure or a constant predictor's passing conservation result, or sell conservation as trajectory accuracy. | YARD-01 | resolved | judgment; compare the report against the complete known-answer table and the stated metric meanings. |
| MUST NOT turn unsettled results, TRAIN-only fits or a sampled numerical floor into an unsupported causal, generalization or impossibility claim. | YARD-01, YARD-03 | resolved | judgment; compare claims with their cited records, tasks and limitations. |
| MUST NOT invent owner approval of a target, bar, C-6/C-7 choice or gap closure from silence or the option 3 sequencing answer. | YARD-02, YARD-03 | resolved | judgment; compare the decision record with verbatim owner instructions and the charter reply rule. |

## Ambiguity Report

| Dimension | Initial score | After round 1 | Minimum | Status | Notes |
|---|---|---|---|---|---|
| Goal clarity | 0.90 | 0.95 | 0.75 | pass | Audit evidence precedes conclusions and reserved choices. |
| Boundary clarity | 0.95 | 0.95 | 0.70 | pass | Read-only TRAIN audit; changes route to v2.6. |
| Constraint clarity | 0.85 | 0.90 | 0.65 | pass | Existing definitions and evaluation isolation remain binding. |
| Acceptance criteria | 0.80 | 0.90 | 0.70 | pass | Complete evidence, honest discrepancies and explicit owner dispositions. |
| Ambiguity | 0.118 | 0.070 | at most 0.20 | pass | 1 - (0.35*0.95 + 0.25*0.95 + 0.20*0.90 + 0.20*0.90). |

These scores describe clarity of the required work. They do not resolve the
scientific questions or the deliberately pending owner choices.

## Interview Log

| Round | Perspective | Question summary | Answer and decision locked |
|---|---|---|---|
| 1 | Researcher | Choose unseen Stage-0 generalization, a one-system result, or leave the target open until the yardstick evidence. | Owner chose option 3 in the quote above. Phase 68 gathers evidence and presents recommendations before asking for a target or bars. |
| Post-gate | Failure analysis and boundary review | Correct-answer failure, constant-predictor conservation, incomplete tables and absent owner instructions. | Agent applied existing contracts under the standing technical delegation. Fifteen explicit edges and three judgment prohibitions preserve evidence and owner authority. |

The ambiguity gate passed after round 1. Further rounds were unnecessary.
The original request to produce the specification continues under the
owner-approved evidence-first scope. No charter option is auto-selected.

## Grounding

- `.planning/REQUIREMENTS.md`, YARD-01 through YARD-03, SCOPE-45 through
  SCOPE-49 and owner checkpoint 2.
- `.planning/ROADMAP.md`, Phase 68 goal and five success criteria.
- `.planning/PROJECT.md`, current v2.5 milestone and standing GSD decision
  delegation dated 2026-10-28.
- `.planning/phases/64-feasibility-verdict/64-CHARTER.md`, purpose C-1,
  choices C-2 and C-4 through C-7, C-11 and the explicit reply rule.
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`,
  GAP-59-08's measured defect, alternatives and dependency-scoped block.
- `.planning/phases/66-small-network-control/66-VERIFICATION.md`, the
  replicated position fit and its single-orbit scope.
- `.planning/phases/67-design-settings-ladders/67-CLOSEOUT.md` and
  `67-VERIFICATION.md`, unsettled outcomes and the unchanged yardstick handoff.
- `pinn/verification/artifacts/feasibility_scorecard_v1.json`,
  `feasibility_scorer.py`, `feasibility_scorecard.py` and `gate_metrics.py`;
  `pinn/training/validation_gate.py` and `pinn/evaluate.py`, actual calculations
  and callers explicitly included by YARD-01.
- Owner instruction quoted above, 2026-11-08. The metric audit has not run
  in this spec session; the acceptance checkboxes describe Phase 68's work.

---

*Phase: 68-yardstick*
*Spec created: 2026-11-08*
*Next step: $gsd-discuss-phase 68, implementation decisions for this scope.*
