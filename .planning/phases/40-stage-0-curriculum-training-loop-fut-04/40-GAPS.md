# Phase 40 Gap Register

## GAP-40-01 — Representing the stage-exit machine's mid-flight "no exit decision" state

- **Decision point:** `StageExitMachine.evaluate(...)` must return something when
  the stage is mid-flight — the four-criterion ADVANCE gate is not passing, no
  NaN/Inf occurred, and the epoch budget is not exhausted. The three locked
  dispositions (ADVANCE / RECOVER / HALT) all describe *exiting* the stage; none
  describes "keep training". How that state is represented in the return type is
  not specified anywhere in the corpus.
- **Where in artifact:** `40-04-PLAN.md` Task 1 (`stage_exit.py` — the
  `StageDisposition` enum and the `else continue` branch of the evaluation
  order); consumed by `40-05-PLAN.md` Task 2 (`RunController.run_stage`) and
  `40-06-PLAN.md` Task 1 (`CurriculumController` dispatch).
- **Task context:** Incorporating cross-AI plan-review cycle-2 finding H1 while
  revising the Phase 40 plan set (reviewer `claude`; single-reviewer HIGH — the
  panel degraded to 2 of 4 usable reviewers, so absence of a second opinion is
  not evidence of absence).
- **Classification:** semantic — it is the return type of the load-bearing
  "no fallback advancement" safety contract (CURR-03), and 40-05/40-06 both
  dispatch on it.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1928`
    — "the training loop's stage-exit decision is an operational state machine
    with **three dispositions: ADVANCE, RECOVER, and HALT/REVIEW**." This
    *positively grounds* the three-member enum and *rules out* the reviewer's
    suggested fix of adding a fourth `CONTINUE` disposition. It does not say what
    the machine returns when none of the three fires.
  - `ctl_instruction.md` §"Stage Transition Criteria" (criterion 1, ~:1955-1962)
    — defines the plateau check at epoch `i` against `i − patience`, and defines
    HALT as *reaching* the max-epoch budget "without satisfying the ADVANCE
    success gate". Both presuppose evaluations that fire nothing, but neither
    names the resulting value.
  - `.planning/REQUIREMENTS.md:62` (TRAIN-06) — lists the same three
    dispositions; silent on the not-exiting case.
  - `.planning/phases/40-.../40-SPEC.md` R6 + AC — same three; silent.
  - `.planning/phases/40-.../40-CONTEXT.md` — `grep` for `CONTINUE` /
    "continue training" over ctl_instruction.md, REQUIREMENTS.md, 40-CONTEXT.md
    and 40-SPEC.md returns **zero hits**. No prior user decision, no `✅ LOCKED`
    CTX entry, and no planning artifact answers it.
- **Mathematical / engineering grounding:** The stage-exit machine is a total
  function from the observed training signals to a decision, and its codomain is
  the safety contract: CURR-03's central guarantee is that *no* condition other
  than the four-criterion conjunction may increment the stage. The mid-flight
  state is not a fourth kind of exit — it is the *absence* of an exit decision,
  and the distinction is load-bearing rather than cosmetic. If the not-exiting
  value is folded into the enum (option A), the type no longer means "the stage
  ended, and this is how", and a caller writing `match disposition` can silently
  treat a still-training stage as a terminal one; if it is expressed as absence
  (option B), the type system forces every call site to distinguish "no decision
  yet" from "a decision was made", which is precisely the invariant CURR-03
  exists to protect. Option C admits states that cannot occur in the domain
  (`should_exit=False` alongside `disposition=ADVANCE`), i.e. it makes an invalid
  configuration representable — the standard failure mode of splitting one
  decision across two fields. The choice therefore changes which errors are
  *possible*, not merely how the code reads, and every option is behaviorally
  identical in the happy path, which is exactly why an executor would pick one
  without noticing it had decided anything.
- **Agent was tempted to:** Adopt option B (`StageExitOutcome.disposition:
  StageDisposition | None`) directly and note the choice in the plan, on the
  reasoning that it preserves the locked three-disposition set while making the
  not-exiting case unignorable. That would have been an invented semantics for
  the safety contract's own type — the exact failure mode the STOP protocol
  exists to prevent — so it is surfaced instead.
- **What the user needs to decide:**
  - **A.** Add a fourth `CONTINUE` member to `StageDisposition`. (Reviewer's
    suggestion. Note this contradicts `ctl_instruction.md:1928`'s "three
    dispositions" and lets `CONTINUE` be mistaken for a terminal exit.)
  - **B.** `StageExitOutcome.disposition: StageDisposition | None`, where `None`
    means "no exit decision fired; keep training". Keeps the locked three-member
    set intact; forces callers to handle absence. *(Planner recommendation.)*
  - **C.** A separate boolean (`should_exit`) alongside `disposition`. Weakest —
    the two fields can disagree, making an invalid state representable.
- **Confidence of impact:** HIGH — it is the return type of the no-fallback-
  advancement contract; `40-04` Task 1, `40-05` Task 2 and `40-06` Task 1 all
  depend on it, and an executor choosing silently at implementation time would
  bake an unreviewed representation into the phase's central safety surface.
- **Status:** OPEN — blocks `40-04` Task 1, `40-05` Task 2, `40-06` Task 1.
  `40-01`, `40-02`, `40-03`, and `40-04` Tasks 2–3 are independent and proceed
  (Waves 1–2 are unaffected).
- **Resolution note:** _(empty — awaiting user instruction)_

## GAP-40-02 — Relationship between `MAX_EPOCHS` and `N_Adam,k`

- **Decision point:** `MAX_EPOCHS` (per-stage, CTX-39) and `N_Adam,k` (the Adam
  epoch budget and cosine `T_max`, CTX-48) are both config-required and
  owner-picked, but nothing states their relationship: does `MAX_EPOCHS` bound
  the whole stage (Adam + L-BFGS) or the Adam phase alone, and is
  `N_Adam,k ≤ MAX_EPOCHS` an invariant the config must enforce?
- **Where in artifact:** `40-05-PLAN.md` Task 2 — the acceptance criterion that a
  descending L_phys curve "exits the Adam phase at N_Adam,k … yielding HALT/REVIEW
  (max-epoch-without-gate)"; `40-04-PLAN.md` Task 2 (`config.py`, which would own
  any cross-field invariant).
- **Task context:** Incorporating cross-AI plan-review cycle-2 finding M2
  (2-reviewer agreement: `claude-glm` + `claude`) while revising the Phase 40
  plan set.
- **Classification:** semantic — it determines which terminal state a real run
  reaches, and therefore whether the phase's own HALT acceptance criterion is
  provable.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:660`
    — the ONLY occurrence of `N_{Adam,k}` in the entire framework-spec corpus,
    where it appears solely as an input to the warmup formula
    `I_warm = min(2000, 0.1 · N_Adam,k)`. It is never defined, bounded, or
    related to any other budget.
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1994`
    — the per-stage `MAX_EPOCHS` table, the stagnation window, and the
    percentile-10 relaxation are **claimed-unverified (D5-05; CLM-08/09)** and
    "not transcribed as locked thresholds". The spec gives the *form* (HALT on
    reaching the budget without the gate) but no value and no relationship.
  - `.planning/phases/40-.../40-CONTEXT.md` CTX-39 and CTX-48 — both route the
    values to the owner as config-required "raise if unset"; neither states a
    relationship between them.
  - `.planning/REQUIREMENTS.md` SCOPE-19 — owner-carved decisions are "built as
    seams, not invented", which forbids the planner minting the invariant.
- **Mathematical / engineering grounding:** The stage is a two-phase optimization
  (Adam for at most `N_Adam,k` epochs → plateau handoff → L-BFGS), and
  `MAX_EPOCHS` is the guard that guarantees termination. Which counter the guard
  measures determines the reachable terminal states of a non-converging run. If
  `MAX_EPOCHS` bounds the whole stage and `N_Adam,k < MAX_EPOCHS`, a monotonically
  descending curve exhausts the Adam budget without ever firing the plateau
  detector, the gate is unmet, max-epoch is *not* reached, and the machine lands
  in GAP-40-01's unrepresented state — the run has nowhere defined to go, which
  is why the two gaps are one decision. If instead `N_Adam,k ≥ MAX_EPOCHS`, Adam
  exhaustion coincides with max-epoch and the HALT criterion is provable as
  written, but that reading makes `MAX_EPOCHS` effectively an Adam-phase bound,
  which contradicts the plain sense of "per-stage max-epoch budget" and would
  leave the L-BFGS phase unbounded. The relationship is thus not bookkeeping
  trivia: it selects which of two mutually exclusive readings of the spec's
  termination guarantee the implementation encodes, and one of them makes a
  stated Phase-40 acceptance criterion unprovable.
- **Agent was tempted to:** Adopt option A (`MAX_EPOCHS` bounds the whole stage;
  `TrainingConfig.__post_init__` validates `N_Adam,k ≤ MAX_EPOCHS`) because it
  matches the plain reading and makes 40-05's descending-curve criterion provable.
  That would invent a cross-field config invariant the corpus never states, on a
  pair of values SCOPE-19 explicitly reserves for the owner.
- **What the user needs to decide:**
  - **A.** `MAX_EPOCHS` bounds the WHOLE stage (Adam + L-BFGS); `TrainingConfig`
    validates `N_Adam,k ≤ MAX_EPOCHS` at construction. Requires an accompanying
    rule for "Adam budget exhausted without a plateau, stage budget remaining".
    *(Planner recommendation.)*
  - **B.** `N_Adam,k ≥ MAX_EPOCHS`, so Adam exhaustion == max-epoch. Makes 40-05's
    criterion provable as written; reads MAX_EPOCHS as an Adam-phase bound and
    leaves L-BFGS unbounded.
  - **C.** Independent budgets; exhausting `N_Adam,k` without a plateau handoff is
    itself a stagnation trigger → HALT/REVIEW, reusing the spec's existing
    stagnation path. Requires calling exhaustion "stagnation", which the spec does
    not define.
- **Confidence of impact:** MEDIUM-HIGH — it does not change the gate or the
  science, but it determines the terminal state of every non-converging run, it
  gates a stated Phase-40 acceptance criterion, and it must be resolved jointly
  with GAP-40-01 (option A leaves the mid-flight state reachable; option B does
  not).
- **Status:** OPEN — blocks the HALT-specific half of `40-05` Task 2's
  descending-curve acceptance criterion and any cross-field invariant in `40-04`
  Task 2's config. The bounded-loop and never-ADVANCE assertions hold under every
  option and proceed now.
- **Resolution note:** _(empty — awaiting user instruction)_
