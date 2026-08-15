# Phase 50 Gap Register — Valid Stage-0 Re-Run

Phase-local STOP-protocol gap register for Phase 50 (milestone v2.2). Each entry
is a source-silent decision that this phase **surfaced** rather than decided, per
the CLAUDE.md / AGENTS.md STOP protocol. The milestone-wide index is
`.planning/milestones/v2.2-GAPS.md`.

This register is written by the Phase 50 orchestrator (parent session), not by a
subagent — per governance, the parent owns gap-register writes. The plan 50-02
executor surfaced the finding and correctly declined to resolve it.

## GAP-50-01 — Graded seed 41 dies at first validation because the Stage-0 validation pool is 227 identities and DATA-05 `replay_count` is 240. What, if anything, may change before a later generation launches graded seeds?

- **Decision point:** The graded recipe’s DATA-05 default `replay_count=240`
  requires a Stage-0 replay pool of at least 240 identities, sampled without
  replacement. Seed 41’s **validation** `records_at_or_below(0)` pool has **227**,
  so `select_stage_records` raises DATA-06 `StageZeroUnderpopulated` at the first
  validation (`validation_every=100`). Train (`n_train=1812`) is large enough, so
  Adam ran 99 finite steps; the first val batch is impossible at 240. The smoke
  used explicit `replay_count: 32`, so 227 ≥ 32 and it finished. What, if
  anything, should change before a later generation may launch graded seeds?

- **Where in artifact:**
  `runs/stage0-rerun-seed41` at step 100; `pinn/data/batches.py` (the
  `StageZeroUnderpopulated` check); launch transcript
  `.planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-seed41-attempt-01-invocation-01-train.txt`
  (`Stage-0 population 227 < required 240`); generation-2 closeout
  `.planning/phases/50-valid-stage-0-re-run/50-02-SUMMARY.md` and
  `evidence/terminal-manifest.json`.

- **Task context:** Plan 50-02 Task 2, seed 41, band generation 2, executed during
  `/gsd-execute-phase 50 --wave 2` after the owner authorized a fresh generation
  at `7dd9ad92`. Generation 1 had already closed terminally on an operational
  wrapper timeout. Smoke of generation 2 finished (`SMOKE-OK`). Seeds 42 and 43
  were not launched.

- **Classification:** **semantic** (dataset-vs-recipe first contact; also a
  preflight-coverage gap). Not operational coordination: a different ruling
  changes whether graded launches are legal, whether validation may use a
  smaller pool, or whether Phase 50 stops.

- **Source silence:**
  - `50-CONTEXT.md` D-03 records 32-vs-240 as a **confound** (smoke explicit 32
    vs graded unset → DATA-05 default 240), not as a population floor or as a
    rule for what to do when the **validation** split is the short pool.
  - `50-PRE-REGISTRATION.md` pins splits and source-config identity, not a
    Stage-0-per-split count that would have refused seed 41 before launch.
  - DATA-06 makes `|pool| < replay_count` fatal, but does not say what to do
    when that shortfall appears on **validation** after preflight already
    passed and train-side Adam has already run.
  - SCOPE-29 / D-19 forbid changing a hyperparameter because 227 was observed.
    They do not say whether a later generation may add a preflight check that
    would have caught 227 < 240, or change how validation constructs a batch,
    without citing 227 as the new recipe number.

- **Mathematical / engineering grounding:**
  Replay draws **without replacement** from the Stage-0 identities in the
  requested split. If `|D≤0 ∩ split| < replay_count`, no legal batch exists.
  That is a set-cardinality constraint, not a loss-tuning knob. The train split
  at Stage 0 is 1812 ≥ 240, so the training loop is well-defined for 99 steps.
  The validation split at Stage 0 is 227 < 240, so the first required val batch
  is undefined. Lowering `replay_count` from 240 to 227 (or to the smoke’s 32)
  would make the batch exist, but it would be choosing the recipe from the
  observed count. Adding a preflight refusal on `|val ∩ D≤0| < replay_count`
  would have stopped before Adam without changing 240. Changing the validation
  sampler to allow a smaller pool, or to draw val batches from a different
  source, is a different contract than DATA-05/06 currently state.

- **Agent was tempted to:** reduce graded `replay_count` to 227 or 32 so seeds
  42/43 could run. Rejected: that cites the run (SCOPE-29 / D-19). Also tempted
  to treat D-03’s 32-vs-240 confound as already authorizing 32 on graded configs.
  Rejected: D-03 names a confound to carry, not a recipe edit.

- **What the user needs to decide:**
  - **A.** Keep 240. Treat 227 as an admission/split/population fact. A later
    generation still needs a **non-numeric** contract for how validation
    constructs a 240-identity batch (or a preflight refusal) before any graded
    launch.
  - **B.** Change the validation batch rule (for example, allow a smaller val
    pool or a different source) **only** if that is already a locked DATA-05/06
    / owner contract, not because 227 was seen.
  - **C.** Accept this terminal record and stop Phase 50 graded execution until
    a later milestone.

- **Confidence of impact:** **HIGH** — no seed-42/43 band exists; D-16 and
  RUN-02 cannot close; 50-03 must not synthesize a candidate. `final_band_generation`
  is null.

- **Status:** `RESOLVED-WITH-INSTRUCTION`

- **Resolution note:** Owner delegated the ruling to the orchestrator on
  2026-08-13 ("I don't know what's the answer here. decide on this following
  your best reasoning"). **Option A.** Keep DATA-05 `replay_count=240`. Do not
  set it to 227 or to the smoke's 32 because this run observed 227 (SCOPE-29 /
  D-19). Do not start 50-03. Do not launch another 50-02 generation in this
  wave.

  What A means here, grounded in already-locked text rather than in 227:
  DATA-06's readiness fatal is `stage0_full_split_count` (`stage_scan.py`
  `readiness_operand`; train-split count is `diagnostic_only_phase40`). That
  full-count check already passed (`n_train=1812`). Seed 41 died because
  `_run_validation` calls the same DATA-05 `_stage_batch` / `select_stage_records`
  unique-without-replacement draw on the **validation** source
  (`train.py` documents `build_stage_batch` for both splits). On this pinned
  split that val-side Stage-0 pool is 227, so graded 240 is structurally
  unsatisfiable without one of: (i) a later split/admission change that makes
  `|val ∩ D≤0| >= 240` without targeting the observed 227, or (ii) an
  owner-ratified val-batch rule that is not the train-side unique-240 draw.
  Neither (i) nor (ii) is authorized as a silent 50-02 edit. The next work is
  a planned 50-01 / new-plan step to choose (i) or (ii). Wave 2 stays on the
  generation-2 terminal record (`8847995`).

  **Superseded in part by GAP-50-02** (2026-08-13), which is the planned step
  this note calls for. GAP-50-01's own ruling — keep `replay_count = 240`,
  never set from the observed 227 — stands unchanged and is preserved by
  GAP-50-02's resolution.

## GAP-50-02 — GAP-50-01 deferred the (i)/(ii) fork to a planned step. Which rule constructs the Stage-0 **validation** batch, given that DATA-05 `replay_count = 240` stays fixed?

- **Decision point:** GAP-50-01 kept `replay_count = 240` and explicitly deferred
  the operative choice: either (i) a split/admission change making
  `|val ∩ D≤0| >= 240` without targeting the observed 227, or (ii) an
  owner-ratified validation-batch rule that is not the train-side
  unique-240 draw. This entry resolves that fork. It decides **what "the
  validation set" means** to the ADVANCE success gate — not any numeric value.

- **Where in artifact:**
  `pinn/training/controllers.py:774-782` (`RunController._run_validation` calls
  `_stage_batch` on `self._validation_source`), routing to
  `pinn/training/controllers.py:732-770` (`_stage_batch`) and
  `pinn/data/batches.py:66-117` (`select_stage_records`, the DATA-05 draw and the
  DATA-06 `StageZeroUnderpopulated` raise at line 93-94).

- **Task context:** Planning the continuation of Phase 50 after plan 50-02's
  generation-2 terminal closeout (`8847995`), under `/gsd-plan-phase 50` on
  2026-08-13. No run was launched while this was open.

- **Classification:** **semantic** (which population a held-out measurement is
  taken over), with a **cross-phase reframing** component: the answer changes
  whether Phase 50 can produce a band at all, and therefore whether Phase 51's
  single authorized look is reachable.

- **Source silence — and where the source is NOT silent:**
  - `ctl_instruction.md:1815-1817` is **not** silent on scope: the canonical
    batch-construction contract opens *"For a 256-trajectory **training** batch
    at curriculum stage k"* and defines `B_replay = 240` inside it. It says
    nothing about validation-batch construction.
  - `ctl_instruction.md:1938-1940` is **not** silent on the measurement
    population: *"ADVANCE is permitted only when the approved success gate
    passes on the **held-out validation set** (hold-out 10-20% of cumulative
    data per stage)"*; criterion 4 (`:1976`) is `(1/N_traj) Σ_{j=1}^{N_traj}`
    over that set.
  - `ctl_instruction.md:1825-1831` (batch edge-case policy, GAP-34-01 option A)
    resolves the undersized **look-ahead** pool by padding with replacement and
    is silent on an undersized replay pool — because the replay pool is a
    training-split object where the case does not arise (`n_train = 1812`).
  - `50-CONTEXT.md:121, 259-260` records `replay_count` as narrowing "only the
    per-batch replay identity count" over "the **train split** pool"; it does
    not state a validation-batch rule.
  - What no source states is whether SCOPE-29 permits repairing this
    train-rule-applied-to-validation divergence **inside** v2.2 rather than
    deferring it. That is the owner-gated part, and is why this is routed rather
    than decided silently.

- **Mathematical / engineering grounding:**
  Two independent defects, one blocking and one silent.

  1. *Blocking (set cardinality).* `select_stage_records` draws `replay_count`
     identities **without replacement** from `records_at_or_below(stage)` of the
     supplied source. When that source is the validation split at stage 0,
     `|pool| = 227 < 240`, so no legal draw exists and DATA-06 fires. This is a
     cardinality constraint, not a tuning knob. It cannot be cleared by any
     choice that leaves a 240-wide without-replacement draw on a 227-wide pool.

  2. *Silent (estimator inconsistency).* ADVANCE criterion 2 is
     `L_val(i) <= min_{j<=i} L_val(j)`. A running minimum over a sequence is a
     valid stage-exit signal only when each term estimates the **same**
     quantity. Under the current construction each validation event draws a
     *fresh* random 240-identity subset, so `L_val(i)` and `L_val(j)` are
     estimates on different subsets; their difference mixes real improvement
     with subset-swap noise, and a running minimum is biased downward by that
     noise (it selects the luckiest subset, not the best model). Evaluating the
     entire held-out pool sets the identity-sampling variance of the comparison
     to exactly zero and makes the criterion mean what it says. The same holds
     for criterion 3 (`L_phys^val < eps_phys`) and criterion 4's `(1/N_traj) Σ`,
     which the spec writes as a sum over the validation set, not over a sample
     of it.

  A third, structural observation: the codebase already contains the correct
  construction one seam away. `compute_validation_gate`
  (`pinn/training/validation_gate.py`) — the locked Phase 46/49 INST-01 gate that
  fires on the *same* `validation_every` branch as `_run_validation`
  (`pinn/train.py:1075-1093`, the "gate-aligned validation seam (46-07)") —
  evaluates `sorted(validation_source.records_at_or_below(stage))`: the full
  pool, deterministic order, no RNG, no lookahead, empty pool fatal. The two
  consumers of "the validation set" at one event disagree about what it is.

  Cost is not a constraint. `collocation_count` is a **total** budget allocated
  near-evenly across identities (`allocate_collocation_quota`,
  `pinn/data/batches.py:124-150`), and validation passes `1`; so the collocation
  work is identical under either rule, and the data-point work at stage 0 falls
  from 256 identities (240 replay + 16 lookahead) to 227.

- **Agent was tempted to:** treat the undersized-look-ahead edge rule
  (`ctl_instruction.md:1828`, pad with replacement) as the nearest applicable
  precedent and pad the validation replay draw to 240 from the 227-identity
  pool. Rejected on the mathematics: with-replacement padding lets a held-out
  identity be counted more than once inside a `(1/N_traj) Σ` mean, which the
  spec writes over the set; it raises rather than removes the criterion-2
  variance; and it imports a training-batch edge rule into a held-out
  measurement, which is the very category error being repaired.

- **What the user needed to decide:** A — full held-out pool; B — pad the draw
  with replacement; C — re-split so `|val ∩ D≤0| >= 240`; D — stop Phase 50
  graded execution.

- **Confidence of impact:** **HIGH** — determines whether a band exists at all
  (D-16, RUN-02), and touches the producer of every stage-exit decision.

- **Status:** `RESOLVED-WITH-INSTRUCTION`

- **Resolution note:** Owner selected **Option A** on 2026-08-13 after being
  shown the three grounding facts above. `RunController._run_validation`
  evaluates the **entire held-out Stage-≤k validation pool** —
  `sorted(validation_source.records_at_or_below(k))` — with **no replay draw and
  no lookahead set**, matching the already-locked `compute_validation_gate`
  population and the spec's "held-out validation set" language.

  Boundaries carried by this ruling:

  - DATA-05 `replay_count = 240` is **unchanged** and remains the training-batch
    contract; the graded configs still leave `stage.replay_count` unset. No
    constant anywhere is set to 227, 240 → 227, or the smoke's 32. GAP-50-01's
    ruling is preserved, not reversed.
  - This is filed as a **conformance divergence repair** under SCOPE-29
    (repairing a divergence against the spec), on the CONF-08/CONF-09 precedent
    that magnitudes may move because the implementation becomes the specified
    one — not because a hyperparameter was fitted to an observed result. It
    gets a new `pinn/conformance/divergence_register.json` entry with a
    `spec_citation` and a `proof_test`, in the established `C-0N` shape.
  - Scope fence: `collocation_count` stays hard-coded at its current value
    (already carried as the open `COLLOCATION-COUNT-HARD-CODE` qualification),
    the train-side batch construction is untouched, and no threshold,
    `validation_every`, budget, or split is changed.
  - Sequencing: this is a runtime-source change, so per GAP-50-01's resolution
    it requires a new source-identity commit and pre-registration amendment
    before a **fresh full generation**. Generations 1 and 2 stay immutable
    terminal history; the repaired band is **generation 3** and re-runs the
    smoke plus all three seeds at one head. `--resume` remains forbidden.
    50-03 stays blocked until generation 3 produces a band.

## GAP-50-03 — Generation-3 seed 41 HALTed at step 501 because invariant B saw `front_idx` stay 0 for the full `N=500` window. What, if anything, happens before a later generation may continue?

- **Decision point:** After the C-09 repair, generation-3 seed 41 completed its first validation event without DATA-06 `StageZeroUnderpopulated`, then HALTed at step 501 because invariant B recorded no `front_idx` advance within `N=500` (`front_idx` stayed 0 on all logged steps). Seeds 42 and 43 were not launched. `final_band_generation` is null. What, if anything, may happen before a later generation continues?

- **Where in artifact:** `runs/stage0-rerun-seed41/failure/trip.json` (`guard=invariant_b`, `step=501`, `threshold=500`, `threshold_provisional=false`); generation-3 seed-41 attempt 2 in `.planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md`; `.planning/phases/50-valid-stage-0-re-run/50-05-SUMMARY.md`; appended `generation_3` section of `evidence/terminal-manifest.json`.

- **Task context:** Plan 50-05 Task 4 / 50-02 Task 2, generation 3, after owner `proceed` (2026-08-15T03:02:42Z) and after the seed-41 first-validation proof. Closeout commit `7d910485`.

- **Classification:** **semantic** (owner-reserved invariant-B response; D-20). Also operational coordination for whether 42/43 may ever run at this head, and whether 50-03's terminal branch is the only remaining Phase-50 work.

- **Source silence:**
  - `50-CONTEXT.md` D-20 (lines 309–319): an invariant-B HALT is recorded, preserved, gapped, and routed to the owner; **`N` is not raised, softened, re-marked provisional, or bypassed by any agent.** D-20 does not choose among accept-the-HALT / authorize-remaining-seeds / re-rule-`N`.
  - Phase-49 D-18/D-21 lock `N=500` as owner-ratified and forbid agent edits of `N`. They do not say what Phase 50 does after the predicted ~step-501 HALT actually fires on the repaired recipe.
  - `50-05-PLAN.md` Task 4 treats this class as intrinsic: terminal immediately, no retry, no `--resume`, no `replay_count` edit, 42/43 not launched. It does not authorize a later generation or a remaining-seed amendment.
  - SCOPE-29 / D-19 forbid changing a hyperparameter because this run HALTed. They do not say whether a later generation may add a diagnostic or a different Stage-0 curriculum without citing the observed `front_idx` trajectory as the new recipe.

- **Mathematical / engineering grounding:** Invariant B is a high-water-mark window on the causal front. If `front_idx` never leaves 0, the window expires at step `N+1` for `N=500`, i.e. step 501. That is a defined gate, not a numerical glitch. The smoke (`replay_count=32`, 300 steps) never reached this window; the graded run (`replay_count=240`, 1000-step budget, `N=500`) did. A gate that HALTs the run it was built to catch has worked. Changing `N` after seeing this HALT would be tuning from a run outcome. Launching 42/43 at the same head after this class would spend the remaining band compute on the same recipe that just failed the owner-ratified window.

- **Agent was tempted to:** launch seeds 42 and 43 because DATA-06 is gone and RUN-02 still wants a three-seed band. Rejected: D-20 forbids treating this HALT as a number to walk around, and 50-05 Task 4 forbids further launches after this class.

- **What the user needs to decide:**
  - **A.** Accept the HALT record. No band. 50-03 stays on its terminal branch. Phase 50 does not launch another generation until the owner separately authorizes one.
  - **B.** Explicitly authorize remaining seeds 42 and 43 at this head, and amend the plan/acceptance criteria first. This generation's terminal closeout still stands until that amendment exists.
  - **C.** Re-rule `N` (owner only). Any such ruling still requires this generation to stay terminal and a new source-identity generation before another band. The agent must not propose a new `N` from the observed `front_idx` trajectory.

- **Confidence of impact:** **HIGH** — this decides whether Phase 51 ever gets a candidate from Phase 50, and whether RUN-02 can close.

- **Status:** `RESOLVED-WITH-INSTRUCTION`

- **Resolution note:** Owner selected **Option A** on 2026-08-15. Accept the generation-3 HALT record. No band. Seeds 42 and 43 stay unlaunched. `N=500` is unchanged. `final_band_generation` stays null. 50-03 remains on its terminal evidence branch only. Phase 50 does not launch another generation until the owner separately authorizes one. `--resume` remains forbidden. This does not re-rule invariant B and does not treat the observed `front_idx` trajectory as a licence to change any hyperparameter (D-20 / D-19 / SCOPE-29).
