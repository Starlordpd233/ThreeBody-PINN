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
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-17) — `40-04` Task 1, `40-05`
  Task 2, `40-06` Task 1 unblocked.
- **Resolution note:** The user delegated the ruling to the agent's best judgment
  (2026-07-17: "rule on gap 40 01 and 02 using your best judgement…"). ERW triage:
  **not ERW-grade** — a type-representation decision with zero scientific content;
  all governing facts are in-corpus (the `ctl_instruction.md:1928` three-disposition
  lock; CURR-03 no-fallback semantics), and external literature adds no signal.

  **Ruling: Option B** — `StageExitOutcome.disposition: StageDisposition | None`,
  where `None` means "no exit decision fired; keep training."
  - Option A rejected: a fourth `CONTINUE` member contradicts the positively-grounded
    three-disposition lock and corrupts the enum's meaning ("the stage exited, and
    this is how"); a `match` arm could silently treat a still-training stage as
    terminal.
  - Option C rejected: splitting one decision across `should_exit` + `disposition`
    makes the invalid state (`should_exit=False`, `disposition=ADVANCE`)
    representable — the standard two-field failure mode.
  - Option B is representationally honest (mid-flight is the *absence* of an exit
    decision, not a fourth kind of one), keeps the locked three-member enum intact,
    and forces every dispatch site to handle absence under type narrowing; enum
    members are truthy, so even sloppy truthiness cannot mistake `None` for an exit.

  Bound consequences: the no-fallback test assertion shape is
  `outcome.disposition is None`; `StageExitMachine.evaluate` has codomain
  `StageDisposition | None`, while `RunController.run_stage(k)` KEEPS its
  non-Optional `-> StageDisposition` signature — its loop consumes `None` internally
  by continuing training, and the GAP-40-02 ruling guarantees a non-None disposition
  by `MAX_EPOCHS` — so `CurriculumController` (40-06) dispatches on exactly the three
  members and never receives the mid-flight state. Resolved jointly with GAP-40-02.

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
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-17) — the HALT-specific half of
  `40-05` Task 2's descending-curve criterion and `40-04` Task 2's cross-field
  invariant unblocked.
- **Resolution note:** Same delegation as GAP-40-01 (user, 2026-07-17). ERW triage:
  **not ERW-grade** — budget-accounting/termination semantics decidable from the
  spec's own formulas plus short, uncontroversial termination analysis; the numeric
  *values* of `MAX_EPOCHS` and `N_Adam,k` remain owner-picked config (CTX-39/48),
  informed by the Stage-0 pilot, unchanged by this ruling.

  **Ruling: Option A** — `MAX_EPOCHS` bounds the WHOLE stage (Adam + L-BFGS epochs
  combined); `TrainingConfig` validates `N_Adam,k ≤ MAX_EPOCHS` at construction.
  Equality is legal (zero L-BFGS headroom: the stage-exit poll at the shared
  boundary fires HALT before any L-BFGS epoch runs). Grounds:
  1. **Termination** — a guard guarantees termination only if it dominates every
     loop in the stage. Option B makes `MAX_EPOCHS` an Adam-phase bound and leaves
     the L-BFGS loop unbounded: no termination proof exists for a non-converging run.
  2. **The spec's HALT wording is stage-scoped** — "if a **stage** reaches its
     **per-stage** max-epoch budget without satisfying the ADVANCE success gate"
     (`ctl_instruction.md:1988`) — not Adam-phase-scoped.
  3. **The cosine schedule completes at `T_max = N_Adam,k`** (CTX-48), and
     `I_warm = min(2000, 0.1·N_Adam,k)` (`pinn_architecture.md:660`) likewise treats
     `N_Adam,k` as the planned Adam-phase duration — a subordinate budget *inside*
     the stage budget, which is exactly what `N_Adam,k ≤ MAX_EPOCHS` encodes.

  **Accompanying sub-rule (the case option A required):** exhausting `N_Adam,k`
  WITHOUT a plateau is a normal **handoff to L-BFGS**, not a fault. The Adam phase
  ends at `min(first plateau-fire epoch, N_Adam,k)`; both routes proceed to L-BFGS.
  Rejected alternatives for this sub-case: (i) HALT-at-exhaustion (≈ option C) would
  mint a third HALT trigger the spec does not define (its two: per-stage max-epoch
  without gate; validation stagnation over the stagnation window), would misreport a
  healthy still-descending run as a failure, and would make legitimate ADVANCE
  unreachable for any run whose Adam budget is under-provisioned; (ii) continuing
  Adam past `T_max` is unscheduled behavior (torch `CosineAnnealingLR` is periodic
  past `T_max` — the LR climbs back up). L-BFGS with strong-Wolfe line search needs
  no plateau precondition; the plateau detector is the *early-switch optimization*,
  the budget the deterministic backstop — the standard two-phase PINN pattern.
  Option C as a whole is rejected for the same trigger-minting reason.

  **Loop consequences (fills the L-BFGS bound 40-05 left unstated):** the L-BFGS
  phase consumes at most the remaining `MAX_EPOCHS − adam_epochs_used` stage budget;
  `RunController` polls `StageExitMachine` during the phase and returns the FIRST
  non-None disposition; at `epoch_count == MAX_EPOCHS` without the gate the poll
  returns HALT by construction, so `run_stage` always terminates with a non-None
  disposition. The two handoff triggers stay distinguishable in the CTX-45 handoff
  event payload (`trigger=plateau` vs `trigger=budget-exhausted`), preserving the
  SPEC TRAIN-02 acceptance's faithful reading: the *plateau* handoff never fires on
  a descending curve.

  **AC amendment (40-05 Task 2):** the descending-curve criterion becomes — with a
  fixture where `N_Adam,k < MAX_EPOCHS`, a descending `L_phys` curve exits Adam at
  exactly `N_Adam,k` without the plateau detector firing (exhaustion-handoff), runs
  bounded L-BFGS, and terminates HALT/REVIEW (max-epoch-without-gate) at
  `MAX_EPOCHS`, never ADVANCE. Resolved jointly with GAP-40-01: option A makes the
  mid-flight state reachable by design, and it is represented as
  `disposition = None` per that ruling.

## GAP-40-03 — Per-stage reconfiguration on ADVANCE (the CR-03 wiring gap)

- **Decision point:** `CurriculumController` holds ONE fixed
  `RunController`/`ScheduledWeights`/`TrainingConfig` triple for its whole
  lifetime. On ADVANCE it calls only `ScheduledWeights.rewarm()` — it never
  reconstructs `ScheduledWeights` with the new stage's `lambda^max`, and never
  swaps `TrainingConfig` (`n_adam`, `max_epochs`, `beta`, `eps_phys`,
  `eps_energy` stay pinned to stage 0's values for every later stage). Must
  Phase 40 wire real per-stage reconfiguration, or explicitly document the
  limitation as deferred?
- **Where in artifact:** `pinn/training/controllers.py` —
  `CurriculumController.__init__` (~699-734, the fixed triple) and `step()`'s
  ADVANCE branch (~837-847, `rewarm()`-only). Surfaced as CR-03 in
  `40-REVIEW.md` and as the SC1/TRAIN-01 truth failure in `40-VERIFICATION.md`.
- **Task context:** Planning gap closure for Phase 40 (`/gsd-plan-phase 40
  --gaps`) after verification returned `gaps_found` (3/5 roadmap SC verified).
- **Classification:** semantic (scope + physics correctness) — it determines
  whether the in-scope Stage 0-2 path trains stages 1-2 with their own
  `lambda^max` or silently with stage 0's.
- **Source silence:**
  - `40-SPEC.md:63` — in scope: "Two-phase Adam→L-BFGS closure loop, **Stage 0-2
    full-batch path only**". `40-SPEC.md:76` — out of scope: "Full multi-stage
    curriculum **beyond** the Stage 0-2 full-batch path — deferred PLAT-01".
    Read together these bound the deferral at "beyond Stage 0-2" but never state
    whether reconfiguration *within* 0-2 is required. The phrase is ambiguous
    between naming the *optimizer path* (full-batch L-BFGS is valid for 0-2;
    3-6 need sL-BFGS) and promising stages 1-2 are actually driven.
  - `.planning/ROADMAP.md` Phase 40 SC1 / `40-SPEC.md:27` (TRAIN-01 acceptance)
    — requires only that a forced ADVANCE yields `Δstage = +1` and a forced HALT
    yields `Δstage = 0`. Both pass today; the acceptance cannot discriminate the
    two readings.
  - Phase goal (ROADMAP) — "The trainer runs **Stage 0** end-to-end"; `40-SPEC.md:20`
    — "The v2.0 slice is **Stage-0-first**". Leans single-stage, but neither
    excludes 1-2 nor licenses shipping a curriculum loop that misconfigures them.
  - `ctl_instruction.md` CURR-03 gives per-stage transitions but does not speak
    to Python object lifetimes.
- **Mathematical / engineering grounding:** PHYS-05 makes `lambda_phys/E/L` a
  function of BOTH stage and epoch: `lambda_x(k, i) = lambda_x^max(k) ·
  min(1, i/I_warm)`, with the per-stage caps `lambda_x^max(k)` and
  `I_warm = min(2000, 0.1·N_Adam,k)` both keyed on `k`
  (`pinn_architecture.md` §4.1, `scheduled_weights.py:13-18`). `rewarm()` resets
  only the epoch counter `i` — it re-runs the ramp toward the SAME
  `lambda^max(k=0)` caps and the SAME `I_warm(N_Adam,0)`. So after ADVANCE the
  composed physics objective for stage 1 is `lambda^max(0)·ramp`, not
  `lambda^max(1)·ramp`: the loss being minimized is not the loss the curriculum
  specifies for that stage. This is a physics-objective error, not bookkeeping —
  the whole point of a curriculum is that the objective's weighting changes per
  stage. Crucially, `ScheduledWeights` is ALREADY designed per-stage: its
  constructor takes `n_adam` + `lambda_e_max`/`lambda_l_max` and its own docstring
  says "Construct **one instance per stage** with that stage's `N_Adam,k` and
  per-stage `lambda^max` caps" (`scheduled_weights.py:64-78`), and the module
  docstring asserts the RunController "constructs a new `ScheduledWeights` for
  that stage" at a boundary (`scheduled_weights.py:28-30`). CR-03 proves that
  documented contract false — the wiring, not the design, is missing. The
  asymmetry that decides the ruling: the per-stage `lambda^max` table is a
  *designed, provisional seam* (CTX-38), whereas per-stage `n_adam`/`max_epochs`/
  `eps_phys`/`eps_energy` are *owner-picked* values (CTX-39/48) for which the
  corpus supplies no per-stage table at all. Minting one would be exactly the
  invention SCOPE-19 forbids.
- **Agent was tempted to:** Implement a full `stage_factory` reconstructing
  `RunController` + `ScheduledWeights` + `TrainingConfig` per stage, because it
  reads "Stage 0-2 in scope" literally and makes the outer loop honest. That
  would require inventing a per-stage `n_adam`/`max_epochs`/`eps_*` table the
  corpus never provides and SCOPE-19 reserves for the owner.
- **What the user needs to decide:**
  - **A.** Full `stage_factory`: reconstruct `RunController`/`ScheduledWeights`/
    `TrainingConfig` per stage.
  - **B.** Document the PLAT-01 deferral: keep single-stage, fix the docstrings
    that claim otherwise.
  - **C.** Seam now, per-stage values deferred: inject a caller-supplied stage
    factory; reconstruct `ScheduledWeights` from it on ADVANCE; leave
    `TrainingConfig` owner-supplied through the same seam rather than invented.
- **Confidence of impact:** MEDIUM-HIGH — no effect on a Stage-0-only run (the
  v2.0 slice's actual target), but it silently corrupts the physics objective of
  any 0→1→2 progression, and it ships a module whose docstrings assert behavior
  the code does not have.
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-17)
- **Resolution note:** Same best-judgment delegation as GAP-40-01/GAP-40-02 (user,
  2026-07-17, on the `/gsd-plan-phase 40 --gaps` question). ERW triage: **not
  ERW-grade** — an object-lifetime/seam-placement decision resolvable from
  SCOPE-19 plus the module's own designed constructor contract; no new science.

  > **AMENDED 2026-07-17 by GAP-40-04 (read it with this entry).** The factory's
  > SHAPE below — `k -> (ScheduledWeights, TrainingConfig)` — is **superseded**:
  > it cannot reach the live objective, because `RunController` binds its own
  > `ScheduledWeights` at construction (`controllers.py:267`) and composes the
  > loss through it (`:479`). The factory yields the per-stage **`RunController`**
  > instead. The new-AC paragraph at the end of this entry is likewise **VOID**
  > (it is satisfiable without touching `RunController`) and is replaced by
  > GAP-40-04's ACs. Everything else here — Option C's policy, the `None` default,
  > the SCOPE-19 boundary, the docstring-correction mandate — stands unchanged.

  **Ruling: Option C** — add an injected per-stage seam; do not invent per-stage
  values. Concretely: `CurriculumController` accepts an optional caller-supplied
  `stage_factory` (a callable `k -> (ScheduledWeights, TrainingConfig)`, or the
  equivalent). When supplied, the ADVANCE branch reconstructs the stage's
  `ScheduledWeights` (and `TrainingConfig`) from it instead of calling bare
  `rewarm()`. When `None` (the default), behavior is today's single-stage path,
  and that limitation is stated explicitly in code + the docstrings. Grounds:
  1. **SCOPE-19 governs** — "owner-carved decisions are **built as seams, not
     invented**". The per-stage `lambda^max` caps are a designed seam (CTX-38);
     per-stage `n_adam`/`max_epochs`/`eps_phys`/`eps_energy` are owner-picked
     (CTX-39/48) with no per-stage table in the corpus. Option A must mint that
     table → forbidden. Option C supplies the seam and lets the owner fill it.
  2. **The module's own contract already requires it** — `scheduled_weights.py:28-30`
     and `:64-78` specify one instance per stage. Option B would resolve a
     documented-contract violation by deleting the contract, weakening PHYS-05's
     per-stage encoding to match an incomplete implementation. Wiring the seam
     honors the spec; rewriting the docstring to match the bug does not.
  3. **The SPEC's deferral is bounded at "beyond Stage 0-2"** (`40-SPEC.md:76`),
     so the 0-2 path is not licensed to be wrong; but the phase goal is
     Stage-0-first, so Phase 40 owes the *seam*, not an owner-calibrated
     per-stage table it cannot source. Option C is exactly that line.
  4. **Backward-compatible** — `stage_factory=None` preserves every existing
     Phase 40 test and the ratified Stage-0 default; no ratified behavior moves.

  **Docstring correction (mandatory under every option):** `scheduled_weights.py`
  (module docstring, `rewarm()`) and `controllers.py` must stop asserting
  unconditional per-stage reconstruction. They state the factual contract: the
  factory reconstructs per stage when supplied; without it the run is
  single-stage and stages ≥1 are not reconfigured (PLAT-01).

  **AC (new, TRAIN-01):** with a `stage_factory` supplying stage 1 a
  `lambda^max` distinct from stage 0's, a forced ADVANCE from stage 0 leaves the
  controller's live `ScheduledWeights` reporting **stage 1's** `lambda^max`
  (not stage 0's) — a behavioral assertion on the live object, not a spy
  call-count. With `stage_factory=None`, ADVANCE still yields `Δstage = +1`
  (the existing AC is unchanged and must still pass).

## GAP-40-04 — Does the `stage_factory`'s output reach a LIVE `RunController`?

- **Decision point:** GAP-40-03 → C rules that `CurriculumController` takes an
  optional `stage_factory` (`k -> (ScheduledWeights, TrainingConfig)`) and that
  "the ADVANCE branch reconstructs the stage's `ScheduledWeights` (and
  `TrainingConfig`) from it instead of calling bare `rewarm()`". It does not say
  whether those reconstructed objects are propagated into a **live**
  `RunController`, which binds its own `self._scheduled_weights` /
  `self._config` at construction and is the object that actually composes the
  objective. Must Phase 40 push the factory's output into the live
  `RunController` (and if so, through what surface), or is the seam scoped to
  the `CurriculumController`'s own references?
- **Where in artifact:** `pinn/training/controllers.py` —
  `RunController.__init__` (~266-267, `self._config = config`,
  `self._scheduled_weights = scheduled_weights`), `_compose_loss_terms` (~417-431)
  → `_run_adam_phase` (~479, `weights = self._scheduled_weights.current(epoch)`),
  and `CurriculumController.step()`'s ADVANCE branch (~837-847). Surfaced while
  planning CR-03 closure under `/gsd-plan-phase 40 --gaps`.
- **Task context:** Writing the Phase-40 gap-closure plan set (40-07/40-08) after
  `40-VERIFICATION.md` returned `gaps_found`. CR-01/CR-02/WR-01..05 are
  independent of this decision and are planned; CR-03 is halted on it.
- **Classification:** semantic (physics-objective correctness), with a
  process-artifact component (it also determines the correct wording of the
  docstring correction GAP-40-03 made "mandatory under every option").
- **Source silence:**
  - `40-GAPS.md` GAP-40-03 Ruling (this file, above) — names the factory tuple,
    the ADVANCE-branch reconstruction, the `stage_factory=None` default, and the
    new AC. The AC is scoped to a **forced** ADVANCE ("a forced ADVANCE from
    stage 0 leaves the controller's live `ScheduledWeights` reporting stage 1's
    `lambda^max`"), and by the T-40-09 construction guard a forced disposition
    **cannot coexist with a live `RunController`** — so the ruled AC is provably
    satisfiable without ever touching `RunController`, and the ruling never
    states whether that is sufficient or merely what the AC happens to test.
  - `40-REVIEW.md` CR-03's own suggested fix (~194-198) proposed a DIFFERENT
    shape — `stage_factory: Callable[[int], tuple[RunController,
    ScheduledWeights]]`, i.e. rebuilding the RunController itself. GAP-40-03's
    ruling deliberately chose `(ScheduledWeights, TrainingConfig)` instead, and
    did not say what becomes of the live RunController under that choice.
  - `40-SPEC.md:63` / `:76` — bounds the deferral at "beyond the Stage 0-2
    full-batch path (PLAT-01)"; silent on Python object lifetime.
  - `ctl_instruction.md` CURR-03 (~1922-1998) — per-stage transitions; silent on
    object lifetimes.
  - The codebase's own three ownership claims are **mutually inconsistent**, which
    is precisely why the ruling's silence is not resolvable by reading the code:
    `scheduled_weights.py:28-30` says the *RunController* "constructs a new
    `ScheduledWeights` for that stage"; `controllers.py:236-240` says the
    *RunController* is itself "Constructed once per stage" (i.e. the caller does
    it); `CurriculumController` holds ONE fixed `run_controller` for the whole
    run and loops `step()` over stages. No reading reconciles all three.
- **Mathematical / engineering grounding:** PHYS-05 makes the loss weights a
  function of BOTH stage and epoch — `lambda_x(k, i) = lambda_x^max(k) ·
  min(1, i/I_warm)`, with `lambda_x^max(k)` and `I_warm = min(2000, 0.1·N_Adam,k)`
  both keyed on `k` (`pinn_architecture.md` §4.1). The gradient a live run
  actually descends is composed in `RunController._compose_loss_terms`, which
  reads `self._scheduled_weights.current(epoch)` — the RunController's OWN
  binding. If ADVANCE rebinds only `CurriculumController._scheduled_weights`,
  then on a live 0→1→2 run the composed objective for stage 1 remains
  `lambda^max(0)·ramp` — bit-for-bit the CR-03 defect GAP-40-03's own grounding
  paragraph identifies as "a physics-objective error, not bookkeeping". The
  factory would then be a seam that changes no gradient ever computed, while
  *appearing* to have closed the finding — arguably worse than today's code,
  which at least has a coherent single-shared-object story (`test_controllers.py`
  `ComposedGateEarnedAdvanceTests` passes the SAME `ScheduledWeights` instance to
  both controllers, so rebinding one reference silently DIVERGES the two, leaving
  the RunController — the one that matters — on stage 0's caps). Conversely,
  propagating requires a `RunController` reconfiguration surface that the ruling
  never named and that the review's rejected option-A shape would have obtained a
  different way. The choice therefore decides whether the ruled seam corrects the
  physics objective or only the bookkeeping — not how the code reads.
- **Agent was tempted to:** Add a `RunController.reconfigure_for_stage(scheduled_weights,
  config)` method and call it from the ADVANCE branch whenever a live run
  controller is present, reasoning that GAP-40-03's ground 2 ("Wiring the seam
  honors the spec; rewriting the docstring to match the bug does not") entails it
  and that "you may refine the exact signature to fit the codebase" licenses it.
  That inference chain is long and contested (it invents a public API surface the
  ruling declined to name, on the exact axis where the ruling chose a narrower
  tuple than the review proposed), so it is surfaced instead of taken.
- **What the user needs to decide:**
  - **A.** Propagate: `CurriculumController`'s ADVANCE branch pushes the factory's
    `(ScheduledWeights, TrainingConfig)` into the live `RunController` through a
    new, narrow reconfiguration surface. Makes the seam correct the live
    objective; adds a `RunController` method the ruling did not name.
  - **B.** Do not propagate: the seam rebinds only the `CurriculumController`'s
    own references; the docstrings state that a live `RunController` retains its
    construction-time schedule, and per-stage RunController construction stays the
    caller's job (which `controllers.py:236-240` already claims). Satisfies the
    ruled AC exactly; leaves the live-run objective on stage 0's caps.
  - **C.** Widen the factory to `k -> (RunController, ScheduledWeights,
    TrainingConfig)` (the review's original CR-03 shape), so the caller supplies a
    fully-configured per-stage RunController. Most honest to "constructed once per
    stage"; contradicts GAP-40-03's chosen tuple and interacts with the T-40-09
    forced/live construction guard.
- **Confidence of impact:** MEDIUM-HIGH — no effect on a Stage-0-only run (the
  v2.0 slice's actual target) or on `stage_factory=None` (the ratified default),
  but it decides whether CR-03's closure is real or decorative for any 0→1→2
  progression, and it fixes the wording of the mandatory docstring correction.
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-17) — CR-03 unblocked; `40-09`
  authorized.
- **Resolution note:** Same best-judgment delegation as GAP-40-01/02/03 (user,
  2026-07-17). The gap is a direct sub-question of GAP-40-03, which the user
  delegated; it is resolved under that same delegation rather than re-asked. The
  planner was correct to STOP — GAP-40-03's ruling was underspecified, and its
  tuple shape was chosen before the `RunController` binding was analyzed. ERW
  triage: **not ERW-grade** — object-lifetime/seam placement; the governing fact
  is in-code.

  **Ruling: Option C** — widen the factory to yield the per-stage
  **`RunController`**. `stage_factory: Callable[[int], RunController] | None`
  (exact shape may be refined to fit the codebase; the policy may not). On
  ADVANCE the controller replaces its live `RunController` with
  `stage_factory(k+1)` and rebinds its own `ScheduledWeights` reference to that
  new controller's, so the two cannot diverge. **This SUPERSEDES GAP-40-03's
  `(ScheduledWeights, TrainingConfig)` tuple shape.** Everything else in
  GAP-40-03 stands: `stage_factory=None` remains the default and the ratified
  single-stage path; per-stage `n_adam`/`max_epochs`/`eps_*` are still never
  invented (SCOPE-19) — they arrive through the seam.

  Grounds:
  1. **`RunController`'s own docstring decides it** — "**Constructed once per
     stage** (mirroring `TrainingConfig`'s single-stage `StageConfig` and
     `ScheduledWeights`'s per-stage `lambda^max` caps)" (`controllers.py:232-239`).
     Option C is the only option that honors that documented lifetime. Option A
     contradicts it: adding an in-place reconfiguration surface makes
     `RunController` mutable across stages, which its own docstring says it is
     not. The three-way inconsistency the planner identified resolves in exactly
     one direction — the class already declares itself per-stage; the bug is that
     `CurriculumController` holds one forever.
  2. **Option B is rejected on GAP-40-03's own logic.** GAP-40-03's whole
     grounding is that stage 1 must not descend `lambda^max(0)`. `RunController`
     binds `self._scheduled_weights` at construction (`:267`) and composes the
     objective through it (`:479` `current(epoch)` → `_compose_loss_terms`), so a
     seam that stops at `CurriculumController`'s references never reaches the
     objective. That is strictly worse than honest documentation: it leaves the
     physics defect intact *behind a factory that looks like it fixed it*,
     defeating future detection. GAP-40-03 already rejected Option B for the
     mirror reason — do not resolve a documented-contract violation by deleting
     the contract.
  3. **One seam, not three.** `RunController` binds `ScheduledWeights`,
     `TrainingConfig`, AND `GradClipper` (the per-stage `C_stage`) at
     construction. A factory yielding the controller carries all per-stage
     collaborators through one seam; the tuple shape would need widening again
     the moment `C_stage` was noticed.
  4. **SCOPE-19 preserved** — caller-supplied, no invented per-stage table, no
     built-in default factory, default `None` preserves every existing test.

  **Model continuity (binding constraint).** Curriculum learning requires the
  network's weights to carry across stages — that is what makes it a curriculum;
  only the Adam state resets at a boundary (`40-SPEC.md` R2, "Adam-state reset at
  each stage boundary" — weights are not mentioned because they persist). A
  factory that constructs a fresh `RunController` must therefore be threaded the
  SAME model instance. Because a caller silently supplying a different model
  would discard all prior training with no symptom, `CurriculumController` MUST
  assert that `stage_factory(k+1)`'s model **is** (identity, not equality) the
  model it already held, and raise a typed error on mismatch. This enforces a
  spec-grounded invariant; it is not speculative defensive handling.

  **T-40-09 interaction.** `stage_factory` is a live-run construct (it yields
  live `RunController`s), so it is mutually exclusive with `forced_disposition`
  under the existing exactly-one-of guard: constructing with BOTH must raise
  `ForcedDispositionOnLiveRun` at construction, exactly as a live
  `run_controller` + `forced_disposition` does today.

  **AC replacement (GAP-40-03's new AC is VOID).** The planner correctly showed
  GAP-40-03's AC is provably satisfiable without ever touching `RunController`,
  because it is scoped to a *forced* ADVANCE and T-40-09 bars pairing
  `forced_disposition` with a live `RunController`. It is replaced by:
  - **Live-objective AC (TRAIN-01):** following the existing
    `ComposedGateEarnedAdvanceTests` pattern (an EARNED ADVANCE against a live,
    non-forced `RunController`), with a `stage_factory` whose stage 1 carries a
    `lambda^max` numerically distinct from stage 0's, assert that after the
    ADVANCE the controller's LIVE `RunController` composes the objective with
    **stage 1's** `lambda^max` — observed through the same
    `self._scheduled_weights.current(epoch)` → `_compose_loss_terms` path the
    objective actually uses (`:479`), asserted to floating tolerance. A spy
    call-count on the factory is NOT acceptable; the assertion must be on the
    composed weight value reaching the loss.
  - **Model-continuity AC:** across that same ADVANCE, the live model instance is
    unchanged (`is` identity) and its parameter tensors are unmodified by the
    swap; a factory returning a foreign model raises the typed error.
  - **Default-path AC (unchanged, must still pass):** with `stage_factory=None`,
    forced ADVANCE yields `Δstage = +1` and forced HALT yields `Δstage = 0`.

  **Addendum (2026-07-17) — anchor ordering, an interaction with 40-07's CR-01
  fix.** Raised by the planner while writing `40-09`; reviewed and ENDORSED as
  grounded (not a new gap). The ADVANCE swap MUST precede the
  `stage-{k+1}-init` checkpoint save. `ScheduledWeights.load_state_dict` restores
  `lambda_phys_max`/`lambda_e_max`/`lambda_l_max`/`n_adam_k`/`warmup_length`
  **from the payload** (`scheduled_weights.py:253-257`), so an init anchor
  serialized from the OLD (stage-k) controller but labelled `stage-{k+1}-init`
  would, on a stage-k+1 RECOVER, overwrite stage k+1's caps with stage k's —
  reintroducing CR-03 through the checkpoint path. This interaction only becomes
  live once 40-07 wires `RunController.load_state_dict()` into RECOVER (CR-01):
  before that fix the restored state was discarded, so the ordering was
  unobservable. The two gap closures are therefore coupled and must not be
  reordered. Grounding (short, uncontroversial): `_save_run_start_anchor`'s own
  docstring calls itself "the k=0 analog of the `stage-{k+1}-init` anchor the
  ADVANCE branch already saves at every later boundary"
  (`controllers.py:766-776`), and it saves `stage-0-init` from the stage-0
  controller *before* stage 0 is entered — so by the code's own stated analogy an
  init anchor carries the ENTERED stage's state, which is also what the name
  means. Carried in `40-09` as a `<derived_ordering_note>` with a dedicated AC
  (both payloads read back from the store) and threat `T-40-13`.

  **Docstring correction (now unblocked, wording fixed by this ruling):**
  `scheduled_weights.py:28-30` and `:221-226` and `controllers.py` must state the
  real contract — at a stage boundary the `CurriculumController` obtains that
  stage's `RunController` from the injected `stage_factory` (which carries the
  stage's `ScheduledWeights`/`TrainingConfig`/`GradClipper`), and when no factory
  is injected the run is single-stage and stages ≥1 are NOT reconfigured
  (PLAT-01). `RunController`'s "Constructed once per stage" docstring is now
  TRUE rather than aspirational, and stays.
