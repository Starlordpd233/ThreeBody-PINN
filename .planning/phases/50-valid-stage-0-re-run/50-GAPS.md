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

- **Status:** `OPEN`

- **Resolution note:**
