# Phase 50: Valid Stage-0 Re-Run - Context

**Gathered:** 2026-08-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 50 **executes** the first Stage-0 training runs that are actually the
specified experiment. Phases 46–49 repaired the frame, built the `S_H` pipeline,
conformed the loss math, and shipped the conformance gate — all proven on
deterministic fixtures. This phase is the first real-corpus contact for every one
of those repairs, and it owns exactly RUN-01 and RUN-02:

- **RUN-01** — Stage-0 runs end-to-end under the corrected recipe: preflight
  clean with zero unwaived divergences at run start and across stage boundaries,
  and runtime invariants A/B holding for a full run. Iteration inside the phase
  is **conformance-only** (SCOPE-29).
- **RUN-02** — the three-seed band is re-established, matching the v2.0 protocol
  so the runs are comparable, with validation `ε_H` recorded and characterized
  across the three seeds.

Two obligations deferred into this phase by earlier owner rulings are discharged
here as a by-product, not as separate scope:

- The **first authoritative real-corpus `S_H` / `ε_H` / `N_train`** (Phase 47
  closed on deterministic implementation evidence; owner ruling 2026-07-30,
  Option B, explicitly routed the real-corpus number to Phase 50).
- The **conformance gate's first execution against real data** (Phase 49 D-29
  proved the gate dataset-free and D-30 required it be built so this first
  contact is low-risk).

**What this phase deliberately does NOT do.** No held-out evaluation, no
`pinn/evaluate.py` invocation, no `evaluation/` directory, no materialization of
the `test` split (SCOPE-28 — the single look is Phase 51's; Phase 50 derives its
pre-registered structural candidate from non-held-out evidence, and Phase 51
rechecks the EVAL-01 preconditions before evaluation). No hyperparameter adjusted against an observed
result, under any name (SCOPE-29). No framework-spec edit (SCOPE-30). No
Stage-1+ or PLAT-01..07 work (SCOPE-27). No re-opening of any Phase 46/47/48/49
decision, and no re-audit of the component math. No verdict on the design — that
is Phase 51's, and this phase must not pre-empt it with a validation-side number.

</domain>

<decisions>
## Implementation Decisions

Thirty decisions, D-01..D-30. Each is grounded in a cited owner ruling, a locked
scope boundary, an observed property of the shipped code, or a re-derivable
measurement stated inline. Nothing here selects a value by looking at what a run
produced — that is the boundary the whole phase exists to hold.

Two things are deliberately **not** decided and are reserved to the owner:
whether an invariant-B HALT changes `N` (D-19), and what happens if no seed is
eligible (D-11).

### Recipe, budget, and what "the v2.0 protocol" means

- **D-01 [BUDGET — the shipped Stage-0 config, not the v2.0 smoke budget]:** The
  three graded runs execute at `stage.max_epochs = 1000` and `stage.n_adam =
  1000` — the values committed in `configs/stage0-example.yaml`. Grounding,
  three-fold:
  1. The owner ratified invariant-B `N = 500` on 2026-08-05 **explicitly as
     `0.5 · N_Adam,0`**, against the Phase-49 D-19 evidence packet whose stated
     run-length anchors were "the shipped Stage-0 config: `N_Adam,0 = 1000`,
     `max_epochs = 1000`". At a 300-step budget that window is arithmetically
     unreachable, invariant B can never trip, and roadmap success criterion 2
     ("invariants A/B hold for a **full run**") becomes unfalsifiable. Running
     the band at 300 would quietly convert a ratified gate into decoration.
  2. The v2.0 pilot config carries `run.smoke: true` (`runs/stage0-pilot-seed41/
     config.yaml`) — it is the ACC-02 ~5-minute mechanical smoke budget, not a
     Stage-0 production budget.
  3. `ctl_instruction.md` marks `MAX_EPOCHS`, the stagnation window, retry
     limits, and the epoch tables **"provisional pending FUT Stage-0 pilot
     calibration" (SCOPE-14)** — the spec records the *form* and delegates the
     value. The spec is not silent here; it assigns the value to the calibrated
     artifact, and `configs/stage0-example.yaml` is that artifact — the file the
     owner has ratified values into four times (R-1 guards, R-2 `recover_retries`,
     D4-a `wall_clock_ceiling_s`, and `front_advance_window_n`).

  **Not SCOPE-29 tuning:** 1000 was committed long before any conformant number
  existed and is not selected against an observed result.

  **Fresh-run Stage-0 ceiling:** SCOPE-27 authorizes Stage 0 and forbids Stage
  1+. The current ordinary fresh launch loops after a Stage-0 `ADVANCE`, creates
  `stage-1-init`, and begins Stage 1; the existing `--hold-stage` switch is only
  legal with a resume and therefore cannot protect this band. Before the first
  smoke, add the narrow `--stage-0-only` conformance switch. On a fresh Stage-0
  `ADVANCE` it saves/logs the Stage-0 final boundary and returns success before
  incrementing the stage, invoking `stage_factory`, running a Stage-1
  conformance hook, writing `stage-1-init`, promoting the checkpoint store, or
  rewarming for Stage 1. It is invalid with `--resume`; ordinary invocations are
  unchanged. Every Phase-50 launch uses it and verifies that all persisted stage
  fields equal zero and no Stage-1 checkpoint exists. This is the minimum
  implementation needed to enforce the already-ratified scope boundary, not
  PLAT-01..07 work and not a recipe change.
  — **Reversibility:** reversible — a config literal; the cost of being wrong is
  re-running the band (~25 min, D-16), and no evaluation budget is at risk.

- **D-02 [WHAT RUN-02 COMPARABILITY ACTUALLY REQUIRES]:** "Matching the v2.0
  protocol" is comparability at the **protocol** layer, not byte-identity of
  config. Byte-identity is impossible by construction: CONF-06 alone moves
  `loss.lambda_e_max` from `1.0` to `0.0`, and repairing the recipe is this
  milestone's entire purpose. What is held identical to v2.0:
  - the three seed values `41, 42, 43`, one run each;
  - `data.source: admitted` over the same corpus with the same DI-43-06-01
    blacklist (`../Documentation/problematic_ics_blacklist.json`);
  - `run.precision: float32`, `run.device: mps`, and the same environment
    fingerprint (verified 2026-08-11 in `pinn-train`: python `3.11.15`, torch
    `2.12.1`, MPS available — the exact triple in every pilot `summary.json`
    `header.env_fingerprint`);
  - `opt.validation_every: 100` and `run.log_every: 50`;
  - the same run-record artifact set and the same `runs/<name>/` contract.

- **D-03 [THE OPTIMIZATION-PATH AND WORKLOAD DELTAS ARE RECORDED CONFOUNDS, NOT HIDDEN ONES]:** Any v2.2-vs-v2.0 outcome difference is confounded between the
  conformance repair and more than a 3.33× step-count change. `n_adam` 300→1000
  also moves PHYS-05 `I_warm=floor(0.1N)` from 30→100 (first logged full-physics
  step 31→101), extends CosineAnnealingLR `T_max` 300→1000, and increases planned
  validation opportunities 3→10. Separately, the v2.0 smoke used
  `stage.replay_count: 32`, while omission in the Phase-50 graded configs resolves
  to the DATA-05 default 240: a 7.5× training-batch identity/workload change.
  Phase 44 ranked "undertrained budget" as a live hypothesis, so these intertwined
  changes matter directly to DIAG-05 and prohibit causal attribution. The delta —
  and every other deliberate difference from the v2.0 pilot config — is
  enumerated in a committed **config-delta record**, and a register
  `qualification` entry is added so the caveat travels into every run record
  automatically rather than depending on someone remembering. Phase 50 does
  **not** add a 300-step matched arm to isolate the confound: that is measurement
  beyond RUN-01/RUN-02 and is recorded as a deferred idea.

- **D-04 [PER-RUN COMMITTED CONFIGS, DIFFERING ONLY IN `seed` AND `run_name`]:**
  Four new configs are committed (`run_name` and `run.seed` are config fields with
  no CLI override, so per-seed files are structurally required): one smoke config
  and three graded configs. The three graded configs are **byte-identical except
  `run.seed` and `run.run_name`**, and a `diff` proving that is captured as phase
  evidence — so "the band varied only the seed" is a verified receipt rather than
  an assertion. `run.smoke` is absent (false) in all three. The committed
  `configs/stage0-example.yaml` and `configs/smoke.yaml` are **not edited**; they
  are copied, per the operator runbook's Configure step.

- **D-05 [LOGGING LITERAL IS PROTOCOL PARITY, CURRENTLY INERT]:**
  `run.log_every: 50` — the v2.0 pilot literal rather than the shipped example's
  `100`. The current loop emits `train.log.jsonl` every step and does not consume
  this field, so it does not change diagnostic density in this code state. This
  discrepancy is recorded explicitly rather than
  absorbed silently because SCOPE-29's boundary is what protects the phase, and
  the classification must be defensible: `log_every` enters no loss term, no
  optimizer state, no data selection, and no gate threshold. It changes only how
  any emitted record today.

- **D-06 [EVERYTHING ELSE IS THE SHIPPED CONFIG, UNTOUCHED]:** The R-1 guard
  thresholds (`1e11` / `0.05` / `0.7`), R-2 `recover_retries: 0`, the D4-a
  `wall_clock_ceiling_s: 120`, `front_advance_window_n: 500`, `loss.lambda_e_max:
  0.0`, the stage-exit thresholds, and the monitor block are carried verbatim
  from `configs/stage0-example.yaml`. Each is either owner-ratified or a
  Phase-46..49 conformance outcome. Any change to any of them inside this phase
  is prohibited unless it passes the D-18 conformance-repair test.

### The seed band, and pre-registering everything Phase 51 will need

- **D-07 [THE SPLIT IS SEED-DEPENDENT — this is why pre-registration is mandatory]:** `splits.json` is partitioned with the **run seed**
  (`_partition_by_signature(records, seed, ratios)`; `SplitManifest.seed` equals
  `run.seed` in all three v2.0 pilots), at ratios `train 0.8 / validation 0.1 /
  test 0.1` over 7,606 physical-key groups — seed 42 yields train 6,085 /
  validation 762 / test 759. **Each seed therefore has a different held-out set,
  and one seed's test keys are another seed's training keys.** Choosing which run
  to evaluate after seeing its numbers would both cherry-pick and scramble
  train/test membership across the band. Every selection rule this phase can fix
  is therefore fixed in writing, in the phase's pre-registration record, **before
  the first graded run starts**.

- **D-08 [PRE-REGISTERED SUBMISSION CANDIDATE: seed 42]:** The run offered to
  Phase 51 for the single EVAL-01 evaluation is the **seed-42** run. Grounding:
  v2.0 spent its single look on seed 42, so seed 42's held-out set is the same
  physical population on which `ε_H = 237.2086` was measured — making the new
  number directly comparable and giving DIAG-05 the strongest re-derivation
  basis available. No metric, from any run, may influence this choice.
  — **Reversibility:** one-way in effect — Phase 51 spends the only authorized
  evaluation on this run; a different candidate chosen after numbers exist is not
  recoverable, because the leakage cannot be un-seen.

- **D-09 [PRE-REGISTERED CHECKPOINT: `checkpoints/best.pt`]:** `pinn/evaluate.py`
  takes an explicit `--checkpoint`, so *which* checkpoint is a real decision and
  is pre-registered here rather than picked in Phase 51 after validation curves
  are visible. The rule is the v2.0 rule: `runs/<run>/checkpoints/best.pt`
  (`runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`
  `checkpoint_path`). `best.pt` is selected by the run's own in-flight retention
  policy — an automatic rule that predates every Phase-50 number — not by a human
  reading a chart afterwards.

- **D-10 [INELIGIBILITY-ONLY FALLBACK ORDER: 42 → 41 → 43]:** If the seed-42 run
  is **structurally ineligible** — `eval01_precondition_i` false, a guard or
  invariant HALT, a `disposition` other than `finished`, or absent validation
  gate metrics — the candidate moves to seed 41, then seed 43, in that fixed
  order. The fallback fires **only** on eligibility, **never** on a metric's
  value: a seed-42 run that is eligible and looks bad is still the submission.

- **D-11 [NO ELIGIBLE SEED IS AN OWNER CHECKPOINT, NOT A WORKAROUND]:** If none
  of the three runs is eligible, Phase 50 does not manufacture a candidate,
  relax a precondition, or waive an entry. It records the state, writes the gap,
  and routes to the owner; Phase 51 does not open. This is the protection EVAL-01
  precondition (i) exists to give, and it only works if the agent is willing to
  end the phase without a candidate.

- **D-12 [SPLIT REPRODUCTION IS VERIFIED, NOT ASSUMED]:** Each graded run's
  `splits.json` sha256 is compared against the retained v2.0 pilot baseline,
  pinned here so the check is re-derivable without recomputation:

  | seed | v2.0 `splits.json` sha256 |
  |---|---|
  | 41 | `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86` |
  | 42 | `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903` |
  | 43 | `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172` |

  The seed-42 digest is independently corroborated: it is byte-equal to
  `splits_sha256` inside the v2.0 evaluation receipt, so it is the identity the
  `ε_H = 237.21` measurement was actually taken against. An exact match is the
  evidence that the held-out population is unchanged since v2.0; **a mismatch is
  not a failure but a mandatory qualification** — it means the admitted
  population moved (the CONF-02 admission-path change is the expected candidate),
  the v2.0 comparison is no longer like-for-like, and that fact must travel into
  Phase 51 and Phase 52. Either outcome is recorded; neither is a licence to
  adjust anything.

### First contact: the calibration smoke is a hard precondition

- **D-13 [THE SMOKE IS ENFORCED BY THE DURATION GATE, NOT CHOSEN]:**
  `_check_duration_gate` (`pinn/train.py:576-627`) refuses any non-smoke launch
  that has no valid persisted timing calibration matching the launch's **full**
  fingerprint — device, dtype, torch version, python version, **and `git_head`**.
  The persisted `runs/.calibration/stage0-timing.json` records `git_head:
  ae250c77371b3e2f0128eb4c5e20c9419b53b2bf` (2026-07-22, v2.0 era) and
  `s_per_step: 0.10190`; HEAD is now `a7d355dc`. It cannot match. Phase 50
  therefore **opens with an ACC-02 smoke on the current code state** — this is a
  discovered precondition of the shipped code, not a discretionary de-risking
  step, and the plan must sequence it first or every graded launch refuses.

- **D-14 [THE SMOKE IS ALSO THE GATE'S AND `S_H`'s FIRST REAL-CORPUS CONTACT]:**
  The same run discharges Phase 49 D-30's de-risking intent and Phase 47's
  deferred obligation at smoke cost rather than on a graded run: it is the first
  execution of preflight, the PHYS-05 table assertion, the placeholder census,
  the divergence-register load, and the `S_H` median reduction against the
  admitted corpus. Its `training_metadata.json` (`s_h`, `eps_h`, `n_train`) is
  captured as the **first authoritative real-corpus record**, closing the
  2026-07-30 Option-B deferral.

- **D-15 [THE SMOKE CARRIES `front_advance_window_n: 500`]:** `configs/smoke.yaml`
  leaves its `run.invariants` block empty, which puts invariant B in record-only
  mode and routes the run down a *different* preflight path than the graded runs
  (the affirmative `invariant_b_window` check in `REQUIRED_RUN_START_CHECKS`).
  The Phase-50 smoke config sets `N = 500` — the owner-ratified value, copied,
  not chosen — so first contact walks the identical path the graded runs will.
  It changes no training math: the window cannot elapse inside 300 steps, so
  `N` is exercised as a preflight fact rather than as a trip.

- **D-16 [`S_H` CROSS-CHECK: the smoke runs at seed 42]:** `S_H` is the median
  over the **train split** pool, and `stage.replay_count` narrows only the
  per-batch replay identity count without touching the split — so a seed-42 smoke
  and the seed-42 graded run must first have byte-identical `splits.json` (which
  proves the complete serialized train/validation/test membership is identical)
  and then produce **exactly equal** `s_h` and `n_train`. Equal count and median
  alone are many-to-one and are not accepted as a membership proof.
  That equality is asserted as phase evidence. A mismatch means the statistic is
  not a function of `(corpus, seed)` alone, which is a defect to route as a gap,
  never a number to accept.

- **D-17 [NO COMMIT BETWEEN THE CALIBRATION AND THE GRADED RUNS]:** Because the
  calibration fingerprint pins `git_head` (`git rev-parse HEAD` — commit identity
  only), a commit landing between the
  smoke and a graded launch invalidates the calibration and the launch refuses.
  The execution order is therefore: **land every code/config commit the phase
  needs → run the smoke → run all three graded seeds → only then commit the
  evidence extraction.** Runtime paths must also be byte-clean at every boundary,
  and corpus/environment/config identities define a band generation. If a
  code/config commit becomes necessary mid-band, close the current generation
  terminally and archive every attempt. Before a later full rerun, revise and
  commit the pre-registration source-identity binding while keeping the selection
  policy bytes unchanged; the new commit becomes that generation's ancestor.
  Then rerun smoke and all graded seeds, so nothing is mixed or discarded. This is a real
  constraint on GSD's per-plan commit cadence and must shape the wave structure.
  — **Reversibility:** costly — a mid-band commit does not corrupt anything, but
  it invalidates the band and costs a full re-run of every completed seed.

- **D-18 [EXECUTION ORDER AND THE VERIFY-LADDER CONTINGENCY]:** smoke → seed 41 →
  seed 42 → seed 43, ascending, matching the v2.0 pilots' own execution order.
  If the smoke's measured `s_per_step × 1000` exceeds 1800 s, the graded launches
  additionally require a fresh GREEN full-fingerprint verify marker; the response
  is to run `python -m pinn.verify`, **never** to reduce the budget. Reducing the
  experiment to fit an operational limit is tuning by another name. The scalar
  must **not** be treated as a scientific ETA: the smoke and graded replay
  workloads differ.

### Iteration policy — SCOPE-29 made operational

- **D-19 [THE ONLY LEGAL EDIT INSIDE THIS PHASE IS A CONFORMANCE REPAIR]:** The
  classification test, applied to every proposed change: *does this bring the
  implementation closer to a locked spec value, an owner ruling, or a Phase-46..49
  contract — justified **without reference to what a run produced**?* If yes, it
  is a conformance repair and is allowed only after terminal closeout and a new
  pre-band pre-registration/source-identity commit. If the justification requires citing an
  observed number, it is tuning and is prohibited, whatever it is called
  ("obviously too small", "just to get past this", "provisional"). Any repair
  re-runs the **full band** at the new code state (D-17); selection-policy bytes
  remain identical, source identities are rebound before launch, and seeds are
  never mixed across code states.

- **D-20 [AN INVARIANT-B HALT IS AN OWNER CHECKPOINT, NOT A NUMBER TO ADJUST]:**
  With `N = 500` and the v2.0 observation of `front_idx = 0` across 1,500/1,500
  logged steps in 5/5 runs, a HALT at around step 501 is a live possibility — it
  is precisely the "too small HALTs a healthy-but-slow run" direction the
  Phase-49 D-19 packet named to the owner before they chose 500. If it fires: the
  run is recorded as HALTed, the failure bundle and the full `front_idx`
  high-water trajectory are preserved, a gap is written, and the situation is
  routed to the owner. **`N` is not raised, softened, re-marked provisional, or
  bypassed by any agent** — Phase-49 D-18/D-21 stand unchanged. A gate that HALTs
  the run it was built to catch has worked, and reporting that honestly is the
  deliverable.

- **D-21 [PREFLIGHT REFUSAL AND GUARD TRIPS]:** A preflight refusal is expected to
  be *informative* — it names a conformance defect Phases 46–49 missed — and the
  response is the D-19 repair loop plus a register entry. **No waiver is minted
  here:** Phase 49 D-26 established that the register grants no authority and
  that this milestone defines no waiver policy (that is the charter workstream,
  SCOPE-32). A Tier-1/2 guard trip (loss explosion, disk floor, memory watermark)
  is a *run outcome*, not an interruption. Loss explosion, non-finite, intrinsic
  memory, and unknown causes STOP. Exactly one fresh retry per logical run and
  band generation is allowed only for positively identified/remediated disk or
  external-memory pressure, after immutable archive+hash preservation; this
  Phase-50 rule supersedes the ordinary runbook resume response. `recover_retries`
  stays `0`. No Phase-50 resume is admissible: CTX-53 restores model, optimizer,
  schedule/controller, main RNG, and invariant state but omits the independent
  CollocationSampler RNG, so even a journal-aligned checkpoint cannot prove the
  same optimization trajectory. Every interruption closes terminally; any later
  continuation requires an amended plan and a fresh generation from step zero.

- **D-22 [NO RUN IS SILENTLY DISCARDED]:** Every launch that starts — refused,
  HALTed, failed, superseded, or graded — is listed in a committed **run ledger**
  with a provisional pre-spawn invocation and a closed post-exit observation:
  exact command, timestamps/exit, transcript hash, config/corpus/environment/
  calibration identity, per-exit artifact hashes, and why the attempt is or is
  not part of the final band. Fresh retries are new attempts; resumes are
  prohibited and any unexpected resume history is terminal evidence.
  Generation-scoped cleanliness receipts and
  `pinn.verify` invocations/markers are likewise enumerated by path and hash. The
  band Phase 51 sees must be the whole record, not the surviving subset. The
  protection against a quiet retry loop is that retries are visible; this is the
  phase-local analog of the v2.0 receipt discipline.

- **D-23 [THE HELD-OUT SET IS NOT TOUCHED, AND THAT IS CHECKED]:** No
  `pinn/evaluate.py` invocation, no `runs/<run>/evaluation/` directory, no
  `evaluation-attempt.json`, no materialization of the `test` split. The
  **absence** of an `evaluation/` directory under every Phase-50 run is asserted
  as closing evidence, so "we did not spend the look" is a checked fact rather
  than a claim — the D-16/D-25 Phase-49 principle (a check that cannot fail is
  not coverage) applied to a prohibition.

### What "validation ε_H recorded and characterized" produces

- **D-24 [THE BAND RECORD — concrete contents]:** One committed band record
  carrying, per seed:
  - the eight `gate_*` keys projected **verbatim** from `summary.json`
    (`gate_eps_h`, `gate_scs`, `gate_verdict`, `gate_status`,
    `gate_n_trajectories`, `gate_n_nonfinite`, `gate_sidecar`,
    `gate_schema_version`) — never recomputed, per the Phase-46 D-19/D-20
    passthrough discipline;
  - the validation-`ε_H` trajectory across **all** validation events from
    `validation.jsonl` (10 events at `validation_every: 100` over 1000 steps),
    not just the terminal one;
  - every validation-referenced sidecar, plus the per-trajectory distribution
    from each run's terminal referenced `validation_gate/step-<8-digit>.json` —
    finite-only quantiles under an explicit method, strict finite tail above the
    sidecar threshold, and separately visible non-finite sentinel/reject counts — which is the
    uniform-vs-tail-driven structure Phase 44 had to reconstruct by hand;
  - `s_h`, `eps_h`, `n_train` from `training_metadata.json`;
  - the `front_idx` high-water trajectory (invariant B's own state);
  - final per-term losses from `summary.json` and INST-02 per-term gradient
    statistics from complete `train.log.jsonl` step records (summaries do not
    carry gradient telemetry);
  - `preflight_status`, `eval01_precondition_i`, `eval01_precondition_iii`, and
    the open-divergence list.

  Plus compound descriptive three-seed variation: relative span only for finite
  positive ratio-scale numbers with positive median, and absolute range in dex
  for signed logarithmic SCS. Because each seed changes both split membership and
  training randomness, n=3 spread is not isolated optimizer variance and supports
  no CI, significance, or causal attribution.

- **D-25 [CHARACTERIZATION IS DESCRIPTIVE — it grades nothing and feeds nothing]:**
  Validation `ε_H` is measured by INST-01 instrumentation **on the validation
  split**. It is not the held-out gate and it renders no verdict on the design —
  Phase 51's single evaluation does that. It may not be used to choose the
  submission seed (D-08/D-10), to choose a checkpoint (D-09), or to justify any
  parameter change (SCOPE-29). Its purposes are exactly three: satisfy RUN-02,
  feed DIAG-05's re-derivation in Phase 52, and let the owner see the state of the
  run before the look is spent. `gate_status` (instrumentation health) and
  `gate_verdict` (metric) stay distinct in every reported number, so an
  instrumentation failure can never render as a PASS — the Phase-46 D-28
  discipline this phase inherits.

- **D-26 [THE PHASE DOES NOT PRE-EMPT THE VERDICT]:** Phase 50's writing describes
  what the runs did. It does not conclude that the design works, that it fails,
  or that the v2.0 failure is explained — those are Phase 51's verdict and Phase
  52's DIAG-05 re-derivation respectively, and pre-empting them here would launder
  a validation-side number into a design-side claim.

### Evidence contract, execution environment, and governance

- **D-27 [EXECUTION LOCATION AND ENVIRONMENT]:** Runs execute **inline in
  `.worktrees/trainex` on `milestone/v2.2`**, under
  `<home>/miniforge3/bin/conda run -n pinn-train` (conda is off-PATH).
  Verified 2026-08-11: python `3.11.15`, torch `2.12.1`, `torch.backends.mps.
  is_available() == True` — byte-matching every v2.0 pilot's `env_fingerprint`,
  which is what preserves cross-milestone comparability. **Not** a fresh
  gsd-executor worktree: `runs/` is worktree-local and gitignored, the timing
  calibration lives at `runs/.calibration/`, and the v2.0 pilot artifacts this
  phase compares against are resident here.

- **D-28 [CORPUS RESOLUTION — no copy, and the partial copy is refused]:**
  `data.root` stays unset and resolves through `default_data_root()`
  (`pinn/data/adapter.py`), which derives the **main-repo** `simulation_data/Data`
  from the parent of `git rev-parse --git-common-dir` — deliberately not
  `--show-toplevel`, precisely so a linked worktree does not resolve to its own
  partial copy. Direct observation on 2026-08-12 found approximately 6.3 GiB and
  38,017 regular files under the main-root `simulation_data/Data`; that admitted
  corpus is therefore reachable from this worktree with no copy step. The
  worktree-local partial tree was approximately 2.7 MiB / 75 regular files on
  the same date and is rejected by
  `DataSourceRootIncomplete` rather than silently producing a green run over a
  tiny corpus. `GSD_DATA_ROOT` and `GSD_ALLOW_PARTIAL_DATA_ROOT` are **not** set —
  setting either would bypass the guard that protects this phase's whole result.

- **D-29 [EVIDENCE EXTRACTION IS MANDATORY — `runs/` never commits]:**
  `.gitignore` excludes `runs/` wholesale, so every artifact Phase 51 and Phase 52
  need must be copied into the committed phase tree at
  `.planning/phases/50-valid-stage-0-re-run/evidence/`. Minimum per run:
  `config.yaml` (the frozen resolved copy), `summary.json`, `summary.md`,
  `preflight.json`, `training_metadata.json`, `splits.json`, `curriculum.jsonl`,
  `validation.jsonl`, every sidecar referenced by its events (plus any forensic
  generations from unexpected resume history), and
  `status.json`; plus the run ledger (D-22), the band record (D-24), the
  config-delta record (D-03), and the pre-registration record (D-07..D-10) —
  which must be committed **before the first graded run**, proved by commit
  ancestry to the recorded band head (timestamps are labels, not proof).
  Checkpoints and TensorBoard event files stay
  out (size), while small `run_start_rng.pt` is retained as provenance and all
  checkpoint identities are hashed. Note `*.log` is globally gitignored, so
  `logs/train.log` cannot be committed without an explicit negation and is not retained;
  `train.log.jsonl` does not match the pattern and **is** retained — it is what
  Phase 44's forensics read. A failure bundle's `failure/tail.log` is copied to
  a tracked `failure/tail.log.txt` destination with source/copy hash equality.
  Each copied file records its source path and a
  sha256, so the extraction is provably faithful.

- **D-30 [GOVERNANCE — gaps, checkboxes, and the standing prohibitions]:** Any
  source-silent adjudication that real-corpus contact surfaces — a dataset fact
  interacting with a v1.5-locked contract, an `S_H` that fails validation, a
  preflight refusal whose correct repair is ambiguous, an invariant-B HALT — is
  recorded in `.planning/phases/50-valid-stage-0-re-run/50-GAPS.md`, indexed in
  `.planning/milestones/v2.2-GAPS.md`, and routed to the owner rather than
  decided inline (the build-track analog of the STOP protocol). REQUIREMENTS.md
  checkboxes for RUN-01/RUN-02 flip at the **phase verification act**, never by a
  plan — the Phase-47/49 precedent recorded in STATE.md. Commits go through
  `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`, explicit
  paths only, on `milestone/v2.2`, no protected-branch push.

### Claude's Discretion

The planner and executor own, without re-opening anything above: the exact run
and config file names (the only locked properties are that they are **distinct
from the v2.0 `stage0-pilot-seed4X` names** so v2.0 artifacts are preserved
intact, that the configs are committed, and that the three graded configs differ
only in `run.seed`/`run.run_name`); the wave decomposition and how D-17's
no-commit-mid-band constraint is expressed in it; the file format and layout of
the run ledger, band record, pre-registration record, and config-delta record;
which quantiles the D-24 distribution reports; whether the smoke and the band
extraction are one plan or several; attended (`python -m pinn.train`) versus
unattended (`scripts/train-unattended.sh`) launch; and the sha256 manifest format
for the evidence extraction. Those choices must preserve every decision above,
add no dependency, introduce no new threshold or selection rule, and change
nothing that enters a loss term, an optimizer, the data path, or a gate.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and owner-ratified boundaries

- `.planning/ROADMAP.md` §"Phase 50: Valid Stage-0 Re-Run" — goal, RUN-01/RUN-02,
  and the four success criteria (the proposal's exit criteria).
- `.planning/ROADMAP.md` §"Conformance discipline (applies to all phases)" — the
  hard boundaries, the binding evaluation policy, the grounding inputs, and the
  owner-checkpoint list (item ④, the Phase-51 verdict, is the next one).
- `.planning/REQUIREMENTS.md` — RUN-01, RUN-02, RUN-03, EVAL-01, and
  SCOPE-27..32 with the verbatim evaluation policy.
- `.planning/PROJECT.md` — the active v2.2 milestone and the owner-ratified
  evaluation-policy Key Decision (2026-07-25).
- `.planning/STATE.md` — Phase 49 closure, the 2026-08-05 `N = 500` ratification,
  "Phase 50 is authorized to be planned, not auto-launched", and the 2026-07-30
  Option-B deferral of the first real-corpus `S_H`/`ε_H`/`N_train` to this phase.
- `CLAUDE.md` / `AGENTS.md` — STOP-protocol spirit, source precedence, Git policy,
  and the `scripts/agent-commit` requirement.
- `docs/work/designs/cross_cutting/v2.2-milestone-proposal/2026-07-25-v2.2-roadmap-proposal.md`
  §"Phase 50" — the owner-ratified exit criteria this phase is measured against.

### The owner rulings this phase executes under

- `.planning/milestones/v2.2-GAPS.md` — GAP-46-01 (the RUN-03 evaluator-assembly
  obligation Phase 51 inherits), GAP-46-06 (the CONF-01 qualification that must
  travel with EVAL-01 precondition (ii)), GAP-46-07, GAP-47-01.
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md`
  §"GAP-45-04" — invariant A locked; invariant B stated with `N` owner-owned.
  **The grounding for D-20's refusal to touch `N`.**
- `.planning/phases/49-conformance-gate/49-CONTEXT.md` — D-14 (invariant B's
  operational form), D-18/D-19/D-21 (`N` is owner-owned; the evidence packet;
  no proxy), D-20 (the `N`-unset fail-closed state), D-24 (register contents),
  D-26 (the register creates no authority), D-27 (the `preflight.json` artifact
  and the `eval01_precondition_i` projection), D-29/D-30 (dataset-free proof and
  the explicit hand-off of first real-corpus contact to **this** phase).
- `.planning/phases/47-frame-completion-s-h-pipeline/47-CONTEXT.md` — the frame
  and `S_H`/`ε_H` decisions whose first real-corpus values this phase produces.
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-CONTEXT.md` —
  the `gate_*` vocabulary, the verbatim-passthrough discipline, and the
  `eval01_precondition_iii` sidecar/eligibility pattern D-24 consumes.
- `.planning/phases/49-conformance-gate/49-VERIFICATION.md` — what Phase 49
  verified 6/6 and the two eligibility gaps 49-09 closed.

### Operating surface

- `docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md` — the
  five entry points (Setup / Configure / Launch / Monitor / Resume), the error
  surface table D-21's responses come from, and the M5-Pro notes.
- `configs/stage0-example.yaml` — the shipped Stage-0 recipe D-01/D-06 copy from
  (owner-ratified R-1, R-2, D4-a, and `front_advance_window_n: 500`).
- `configs/smoke.yaml` — the ACC-02 smoke config D-13/D-15 copy and amend.

### Code seams this phase exercises (does not modify)

- `pinn/train.py:576-627` `_check_duration_gate` / `DurationGateError` — the
  fingerprinted calibration refusal that makes D-13's smoke mandatory.
- `pinn/train.py` `main()`, `guard_hook`, `finish_run` — the run-start preflight
  ordering and the fail-closed exit path.
- `pinn/training/timing.py`, `runs/.calibration/stage0-timing.json` — the
  persisted `s_per_step` calibration and its full fingerprint (`git_head`
  included).
- `pinn/data/adapter.py` `default_data_root` / `DataSourceRootMissing` /
  `DataSourceRootIncomplete`, `DATA_ROOT_ENV`, `ALLOW_PARTIAL_ENV` — D-28's
  corpus resolution and the partial-copy guard.
- `pinn/data/splits.py` `_partition_by_signature`, `SplitManifest` — D-07's
  seed-dependent partition and `splits.json` provenance.
- `pinn/training/run_metadata.py` `compute_s_h` / `validate_s_h` — the
  train-split median and its fail-closed validation (D-14/D-16).
- `pinn/conformance/{preflight,census,table,register}.py` and
  `pinn/conformance/divergence_register.json` — the gate this phase first runs
  against real data; `evaluate_eval01_precondition_i` is the eligibility
  predicate D-10 reads.
- `pinn/training/validation_gate.py` `sidecar_relative_path` /
  `publish_gate_sidecar` — the `validation_gate/step-<8-digit>.json` rows D-24
  aggregates.
- `pinn/training/summary.py` `_GATE_KEYS`, `_CONFORMANCE_KEYS`,
  `_eval01_precondition_i`, `_eval01_precondition_iii` — the verbatim projections
  D-24 copies rather than recomputes.
- `pinn/training/guards.py`, `pinn/training/controllers.py`,
  `pinn/training/checkpoint.py` — guard dispositions, the invariant-B state, and
  checkpoint retention (`best.pt`, D-09).
- `pinn/evaluate.py` — **read to understand the Phase-51 contract, not invoked**
  (D-23). Its `--checkpoint` argument is why D-09 pre-registers `best.pt`; its
  attempt/receipt single-use claim is per owning run.

### v2.0 baselines this phase is compared against

- `runs/stage0-pilot-seed41/`, `runs/stage0-pilot-seed42/`,
  `runs/stage0-pilot-seed43/` — the v2.0 pilot runs (gitignored, resident in this
  worktree): frozen `config.yaml`, `summary.json`, `splits.json`, and — for
  seed 42 only — `evaluation/evaluation-receipt.json` with `eps_h = 237.2086`,
  `scs = 2.3751`, `verdict = FAIL`, `checkpoint_path = checkpoints/best.pt`, and
  `splits_sha256` matching the D-12 table.
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md`
  and `43-CALIBRATION.md` — the `adjust` verdict and the owner-ratified
  operational seams.
- `.planning/milestones/v2.1-phases/44-*/44-DIAGNOSIS.md` and `44-ERRATUM.md` —
  the diagnosis DIAG-05 re-derives against this phase's conformant run; read for
  *what evidence the re-derivation will need*, so D-24 captures it the first time.

### Explicitly excluded source

- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` — not a
  grounding source (SCOPE-31). Its tuning analysis reasons about a recipe that
  did not run; consulting it here would re-contaminate the milestone with the
  false premise this effort exists to remove. Nothing in this phase needs it.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **The shipped run surface needs one narrow SCOPE-27 repair.** `python -m
  pinn.train --config <yaml>` otherwise continues from a successful Stage-0
  `ADVANCE` into Stage 1, while the existing `--hold-stage` is resume-only. Plan
  50-01 adds and tests a fresh-run-only `--stage-0-only` ceiling, then every
  Phase-50 invocation passes it through `scripts/train-unattended.sh`. No other
  production surface grows; any broader controller/platform change is a signal
  to re-check for scope creep.
- **`default_data_root()`** already solves the worktree/corpus problem via
  `git rev-parse --git-common-dir` — no data copy, no `GSD_DATA_ROOT`, and the
  partial worktree copy is actively refused. The stale advice in
  `configs/smoke.yaml`'s header comment ("run from the main-root checkout") is
  superseded by the code; the v2.0 pilots ran from this worktree with
  `data.root: null` and resolved correctly.
- **`summary.json` / `summary.md`** project the gate, conformance, final-loss, and
  environment fields D-24 needs. INST-02 gradient telemetry and step-local state
  come from complete `train.log.jsonl` records; summaries do not contain them:
  Phase-46 `gate_*` keys, Phase-49 `conformance` + `eval01_precondition_i`, the
  curriculum journal, final per-term losses, and the `header.env_fingerprint`
  that proves environment parity with v2.0.
- **The evaluation receipt is a worked provenance example.** The v2.0 seed-42
  receipt pins `checkpoint_sha256`, `config_sha256`, and `splits_sha256` — the
  same three identities Phase 50's pre-registration record should pin so Phase 51
  can prove it evaluated the run that was pre-registered.
- **`runs/.calibration/stage0-timing.json`** is a persisted, fingerprinted
  measurement artifact — the smoke re-writes it on success
  (`_write_smoke_timing_calibration`), so the calibration step is self-recording.

### Established Patterns

- **Strict JSON, `schema_version`, atomic write, re-validate on load** — every
  machine-read artifact in this codebase (`training_metadata.json` v2,
  `summary.json` v1, `preflight.json`, the gate sidecars, the register). Phase 50's
  new records (ledger, band record, pre-registration) follow it rather than
  inventing an informal sidecar.
- **Verbatim passthrough over recomputation** — persisted bytes are projected,
  never recalculated, and never null-collapsed. D-24 inherits this: the band
  record copies `gate_*` values, it does not recompute `ε_H`.
- **Instrumentation state and metric state stay distinct** (`gate_status` vs
  `gate_verdict`) so an instrumentation failure cannot render as a PASS.
- **Fail-closed refusal before construction** — the duration gate refuses before
  the run directory exists; preflight writes its artifact *then* exits non-zero.
  A refused Phase-50 launch therefore leaves evidence, and that evidence is part
  of the run ledger (D-22).
- **Evidence lives in the phase tree, artifacts live in `runs/`** — Phases 46 and
  47 both extracted committed evidence from gitignored run output
  (`.planning/phases/4X-*/evidence/`). Phase 50 follows the same shape.

### Integration Points

- **Config → duration gate → run directory:** the launch is refused before any
  run dir is created unless a same-`git_head` calibration exists (D-13/D-17).
- **Corpus → admission → `S_H` → `ε_H` → loss:** first real-corpus traversal of
  the Phase-47 pipeline; `training_metadata.json` is where it becomes durable.
- **`ScheduledWeights` + `TrainingConfig` + register → preflight →
  `preflight.json` → `summary.json` `conformance` + `eval01_precondition_i`:**
  first real-corpus traversal of the Phase-49 gate; this is the chain D-10 reads
  to decide eligibility.
- **Controller `w_n_stats` → `StepGuards` → invariant A/B → failure bundle:** the
  runtime half of the gate. Checkpoints carry invariant-B state but omit the
  separate CollocationSampler RNG, so Phase 50 forbids resume.
- **Validation loop → `gate_metrics` → `validation_gate/step-*.json` sidecar →
  `validation.jsonl` `gate_*` keys → `summary.json` + `eval01_precondition_iii`:**
  the INST-01 chain producing RUN-02's characterization input. Note the v2.0
  `validation.jsonl` records carry only `{final_val_loss, step, trend}` — the
  `gate_*` keys are new in v2.2 and are exactly what "validation carries a
  conservation signal where none exists" means in practice.
- **Run → Phase 51:** the pre-registration record (D-08/D-09/D-10) is the
  interface; Phase 51 verifies the three preconditions and invokes
  `pinn/evaluate.py --checkpoint runs/<pre-registered run>/checkpoints/best.pt`
  exactly once.

</code_context>

<specifics>
## Specific Ideas

- **The phase has one job and one temptation.** The job: produce a run that is
  the specified experiment. The temptation: after the first conformant number
  appears, adjust something. Every decision above is answerable to that — if a
  change's justification cites what a run produced, it is v2.3's work, not this
  phase's.
- **Pre-registration is the cheapest protection available, and it expires.**
  Seed choice, checkpoint choice, and fallback order cost nothing to fix in
  advance and cannot be honestly fixed afterwards, because the split is
  seed-dependent and one seed's test set is another's training set. Written
  before the first graded run, committed with a timestamp, they are a receipt.
  Written after, they are a rationalization.
- **The v2.0 pilot was a smoke, and calling it "the pilot" hid that.** Its config
  carries `run.smoke: true` and a 300-step budget. Reading "match the v2.0
  protocol" as "copy the v2.0 config" would silently run the first valid
  experiment at smoke budget and render the owner's ratified invariant-B window
  unreachable. Protocol comparability is the seeds, the corpus, the environment,
  and the artifact set — not the budget literal.
- **Three seeds, three held-out sets — and the milestone authorizes one look.**
  This is the structural reason the band cannot be scored and then chosen from.
  The band exists to characterize variance and to feed DIAG-05, not to nominate
  a winner.
- **An honest HALT is a deliverable.** If invariant B trips at ~step 501, the
  gate did exactly what the owner ratified it to do. The failure mode to guard
  against is not the HALT — it is an agent quietly raising `N` and reporting a
  clean run.
- **Two checks that cannot fail would be easy to write here** and both are
  forbidden by the same Phase-49 lesson: asserting "no evaluation was spent"
  without checking for the `evaluation/` directory (D-23), and asserting "the
  band varied only the seed" without diffing the configs (D-04).

</specifics>

<deferred>
## Deferred Ideas

- **A 300-step budget-matched arm** to isolate the conformance repair from the
  3.33× budget change (D-03). Legitimate measurement, but beyond RUN-01/RUN-02;
  it belongs to Phase 52's DIAG-05 if the re-derivation needs it, or to the owner
  if they want the tighter A/B.
- **Any recipe change suggested by the conformant numbers** — λ weights, learning
  rate, warmup, budget, clip bound, curriculum pacing. v2.3, with the trainex-r2
  resolution doc as a premise-qualified candidate verdict source (SCOPE-29/31).
- **Re-ruling `N` for invariant B** after observing a Phase-50 HALT — an owner
  decision the shipped config comment already anticipates ("retain this value
  verbatim unless the owner re-rules after a Phase-50 invariant-B HALT"). Routed
  as a gap (D-20), never taken here.
- **Stage-1+ advance, `stage_factory` multi-stage λ reconfiguration (PLAT-01),
  and sL-BFGS (PLAT-02)** — SCOPE-27; the gate's stage-2 refusal (Phase-49 D-06)
  is the correct behavior and stays.
- **Config-resolving `collocation_count`** (hard-coded 16 at `train.py:920`) and
  the `I_warm` integer-floor interpretation — both already open `qualification`
  entries in the register; changing either is a recipe surface (SCOPE-29).
- **Committing `logs/train.log`** — blocked by the global `*.log` ignore; would
  need an explicit negation like Phase 39's. Not needed:
  `train.log.jsonl` carries the machine-readable record (D-29).
- **The general verification-enforcement regime** — normative-statement index,
  full CI integration, waiver policy, thresholds X/M — charter workstream,
  SCOPE-32.
- **Spec-text amendments** — the four VER-20 routing items, Phase 52 (SCOPE-30).
- **Spending the single authorized evaluation** — Phase 51. Phase 50 produces the
  facts and pre-registration, then mechanically evaluates the four D-10
  structural-eligibility criteria without opening the held-out test split:
  `eval01_precondition_i`, the attempt-level guard/invariant rule, final process
  and ledger dispositions, and `eval01_precondition_iii` plus independent
  production-sidecar validation. Phase 51 rechecks those facts before it performs
  the one authorized evaluation.
- **Re-deriving the Phase 44 diagnosis** — Phase 52 (DIAG-05, the GAP-44-02
  obligation). D-24 exists so that re-derivation finds its evidence already
  captured rather than reconstructing it from logs.

### Reviewed Todos (not folded)

- **`d-06-static-epsilon-sensitivity-check`** (matched at score 0.20 on the
  lexical keyword "phase") — **not folded**, and below the fold threshold. A
  sensitivity study over a static epsilon is tuning-shaped work prohibited by
  SCOPE-29, and it is unrelated to executing a conformant run. Same disposition
  as Phases 48 and 49, for the same reason.
- **`trainex-r1-research-handoff`** — **not folded**. Research-administration
  work for the r1b tuning round; unrelated to Phase 50 and gated behind the
  SCOPE-29 boundary.

</deferred>

---

*Phase: 50-valid-stage-0-re-run*
*Context gathered: 2026-08-11*
