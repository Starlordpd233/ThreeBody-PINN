---
title: Trainex R4 Claude research result
role: returned research report; candidate findings and owner-gated options
status: active
created: 2026-10-06
agent: Claude Code (claude-opus-5-5), with three read-only Opus sub-agents
access_mode: open-book
source_baseline: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
live_tree_pin: 9bebe667b520e25e0bea5b84eeb0a4fc7168a9e5
branch: milestone/v2.3
worktree: <home>/Desktop/3_body_problem/.worktrees/trainex
verification_status: pending independent ERW Rule-19 verification
report_body_sha256: 58051ae1aac97925c36c99acf51381b6f2dbf7987190153c98b8db493e308e7e
---

# Trainex R4 Claude research result

This file preserves the research report delivered in this chat. The owner
explicitly requested saving the result on 2026-10-06, after the read-only
investigation.

- **Statements in the report about the investigation.** Where the report says no
  file was edited, no commit was made, and Git state was unchanged, it describes
  the investigation before this save.
- **The returned header.** The returned file's YAML header has been folded into
  this file's frontmatter.
- **What is not committed.** The analysis scripts, the reconstructed anchor
  sequence, and the sub-agents' working files that Appendix A names stayed in the
  session's scratchpad directory. The report records their SHA-256 digests.
- **The body.** It is reproduced as returned between the markers.
  `report_body_sha256` is the SHA-256 of that text with leading and trailing
  whitespace stripped. This is the same convention as `codex-resolution.md`.

<!-- BEGIN RESEARCH REPORT -->
# Trainex R4 — Research Report

## 0. Engagement record and reading guide

**What this is.** This report answers the trainex-r4 research prompt
(`research_package/RESEARCH-AGENT-PROMPT.md`). It follows the five-part output
contract in master §9:

1. premise-challenge findings;
2. a diagnosis for Q1–Q5;
3. options;
4. gaps;
5. a claims-and-uncertainty register.

The diagnosis comes before any option, as the owner chose.

**Engagement pin (ERW Rule 20).** The tree I read was:

- worktree `<home>/Desktop/3_body_problem/.worktrees/trainex`;
- branch `milestone/v2.3`;
- commit `9bebe667b520e25e0bea5b84eeb0a4fc7168a9e5`;
- engagement date 2026-10-06, America/Chicago.

The working tree carried unrelated uncommitted changes at engagement:
`.planning/config.json`, one v2.2 design doc, and untracked tooling folders. None of
them lies under `pinn/`, `configs/`, `runs/`, `tests/`, or the framework specs.

Every code file the diagnosis relies on is byte-identical between generation 7's run
commit `629b1a6c…` and this pin (`git diff --stat 629b1a6c HEAD` over `pinn/training/controllers.py`,
`pinn/data/batches.py`, `pinn/loss_catalog.py`, `pinn/physics_residual.py`,
`pinn/network.py`, `pinn/training/grad_clip.py`, `pinn/training/scheduled_weights.py`,
`pinn/train.py`, `pinn/training/config.py` is empty). Line numbers below therefore
describe the code that ran.

**What I did, and what I did not do.** Everything below is read-only:

- **Edits and runs.** I edited no repository file and made no commit. I ran no
  training and invoked no evaluation.
- **Model computation.** I ran no model forward or backward pass. The only Python I
  executed reads logs, TensorBoard events, checkpoint tensors (`torch.load(...,
  weights_only=True)`), configs, and code. All scripts live outside the repository,
  run with `python -B` so no bytecode lands in the tree.
- **One sub-agent did run forward passes.** The F-row verifier re-ran the frozen
  invariant-B monitor on retained checkpoints, from checkpoint contents only: model
  weights plus the serialized monitor batch, on CPU float32 with no data source. This
  is the same class of read-only measurement as the package's own Part B replay. It
  reproduced Part B's values. No other model computation was performed.
- **Dataset reads.** Two analyses read files from the corpus:
  - the anchor reconstruction (§3.0, E-A) read the row count of the
    training- and validation-split `brutus_hierarchical` files (4,113 files);
  - the physical-scale computation (E-E) read positions, velocities, and masses
    of the 1,812 Stage-0 training trajectories.

  **No test-split file was opened.** The scripts exclude test IDs from
  `splits.json` before any file is touched. The owner should decide whether
  reading training and validation data files counts as "read-only analysis of
  retained logs and checkpoints". I treated it as permitted because it is
  metadata or training data and spends nothing. The disclosure is here so the
  ruling can be made.
- **Independence.** I did not read
  `research_results/codex-resolution.md`. The trainex-r3 (H-03) extract was
  prepared by a sub-agent into a separate file, and I read it only after writing
  my own derivations in §3.7.

**Evidence labels.** Every claim carries one of:

- **[PKG]** — package-derived (master, specs bundle, evidence bundle), not re-derived;
- **[REPO `path:line`]** — repository-verified this session;
- **[LIT]** — published literature (author, title, venue, year);
- **[OWN]** — my own analysis or derivation.

A claim derived from a run artifact cites the artifact path and key. For
`train.log.jsonl`, line *n* is step *n*.

**Re-derivability.** Appendix A lists every analysis script with its SHA-256 and
its decisive output. The most important one is the per-step anchor
reconstruction. It is self-validating: its replayed RNG state equals the numpy RNG
state saved in all seven retained generation-7 checkpoints.

---

## 1. Headline

**The run did not test the recipe the package describes.** Two facts overturn the
package's framing. Both are verified in code and in the run's own retained state.

1. **One trajectory per step, not 256 (PC-1).** The executed loss evaluates the
   physics residual and the IC term on **one trajectory per step**, the "anchor":
   the lowest-ID trajectory among that step's 240 replay draws.
   - The 4,096 "collocation rows, 256 per bin" are 4,096 *times* of that one
     trajectory, not one time per selected slot.
   - The frozen invariant-B monitor scores **one** training trajectory (ID 28)
     rather than its 256 frozen slots.
   - Over 951 steps the physics and IC terms saw **40 distinct trajectories**,
     and **74.7 % of steps used one of the 10 lowest-ID Stage-0 trajectories**.
   - The Phase-57 plan made "every selected slot contributes physics gradients"
     a must-have, and the Phase-57 research listed "one anchor" as nonconformant.
     The conformance verifier's anchor check passes by construction.
2. **The causal physics term was effectively not trained (PC-2).** Under the
   residual-wide `R_ref` normalization, the physics gradient was
   2.8 × 10⁴ – 2.6 × 10⁶ times smaller than the IC gradient (F-08). Under Adam that
   makes the physics term a passenger. The run's own natural experiment confirms it:
   - **What the experiment is.** On the 57 occasions when the same anchor appears
     on two consecutive steps, the second step measures the effect of one update
     made on that anchor's own loss terms.
   - **IC loss** fell in 65 % of those cases (median −28 %).
   - **Physics loss** fell in only 42 % (median change ≈ 0).
   - **The S₂ prefix sum** (bins 0–2) fell in 49 %.

   The front advanced because the network shed its spurious initial amplitude:
   - the output-layer gain fell to 0.668×, and every bin's residual fell
     2.3–5.6× roughly uniformly;
   - the validation energy-drift metric stayed at a median ≈ 0.98 from step 100
     to step 900.

   That pattern is not a causal sweep through time.

**What the evidence does and does not support.** With those facts in place, the
five questions resolve differently from how they are framed:

- **The "stall" is mostly a property of the guard's statistic, not of learning.**
  - **Progress continued inside the window.** Between the 401–500 and 901–951
    blocks, the training population's median S₂ (the normalized residual summed
    over bins 0–2) fell from 2.33 to 0.99, while the learning rate fell about 40×.
    The window held only 23.6 % of the run's cumulative learning-rate mass.
  - **The monitor's high-water mark was set at a transient.** The mark of 2 was
    set at step 450, during a high-volatility phase.
  - **The timing is not reproducible.** Generations 6 and 7 used *identical*
    batch sequences, yet their monitor trajectory's S₁ differed 3× by step 409 from
    float nondeterminism alone.
- **The R_ref-relative front cannot certify physics (Q2).** A fully advanced front
  still allows an RMS residual of about 3.0 × 10⁴. That is **190× the median true
  acceleration** in the same units.
- **L-BFGS was unreachable in this configuration (PC-3).**
  - `max_epochs == n_adam` leaves the second phase a zero budget at budget exhaustion.
  - The plateau hand-off needs 50 consecutive qualifying steps; the longest run was 6.
- **The SIREN initialization scale (Q3) is an upstream contributor, not a proven
  root.** It sets the scale gap that the `R_ref` normalization bridged:
  - `R_ref` corresponds to an RMS residual about 890× the median true acceleration;
  - the initial velocity error was about 170 against true speeds of about 2.

  Its share against the power-skip stack is not decomposed by any existing
  measurement (§5, gap G-3).

**Suggested defaults, for the owner's ruling (§4 has the menus):**

- Restore per-slot conformance and re-measure `R_ref`, then re-run GATE-04.
- Restore gradient balance between the IC and physics terms before any further
  graded run.
- Replace the single-trajectory high-water guard with a smoothed multi-slot
  statistic measured in learning-rate units.
- Gate stage success on an absolute physical criterion, keeping the relative front
  for pacing.
- Run the cheap read-only experiments (E2, E3, E4, E9) first. Several of them can
  falsify the diagnosis above without a training run.

---

## 2. Part 1 — Premise-challenge findings (ERW Rule 17)

Statuses:

- **CONTRADICTED** — the repository shows the package premise is false as stated.
- **QUALIFIED** — the premise is true but incomplete in a way that changes the
  reading.
- **CONFIRMED** — the premise holds; a caveat is noted where one applies.

Findings are ordered by consequence. Per-row checks of F-01…F-18 are in §2.13. A
sub-agent ran an independent per-row verification, and its result is folded in
there.

### PC-1 (CONTRADICTED) — The executed loss is single-trajectory per step, not per selected slot; so is the invariant-B monitor

**The package says.**

- The ratified recipe draws 4,096 collocation rows per batch, 256 per bin, from
  the 256 selected trajectory slots: master §4.1, F-12, and the Phase-56 contract in
  `pinn_architecture.md:456` (specs bundle).
- The re-issued acceptance criterion reads: "A full 256-slot batch emits exactly
  4096 physics rows as one independently sampled time in each of 16 fixed bins for
  every selected slot".
- 57-RULING §2 defines the monitor as "one training-only monitoring context …
  Its selected training identities, collocation rows, bin assignments, and normalized
  times remain unchanged" [PKG].

**The repository shows** [REPO]:

1. **The sampler is conformant.** It materializes per-row identities: each of the
   4,096 rows carries its own slot's `tau_ic13`, `masses` and `record_keys`
   (`pinn/data/batches.py:488-507`).
2. **The loss discards the per-row identity and keeps only the times.**
   - `_build_anchor_context` picks one anchor, `keys[0]`
     (`pinn/training/controllers.py:1075-1079`), and builds the trajectory function
     from that anchor's `ic13` and `masses` (`:1081-1095`).
   - Its own comment says "Only the TIME dimension is consumed here"
     (`:1118-1128`; times taken at `:1128`).
   - Every physics row is then evaluated on the anchor's trajectory, both in the
     monolithic path (`:1169-1181`) and in the microbatched Adam path production ran
     (`_collocation_chunk_raw`, `:1746-1770`).
   - The IC term is that one anchor's IC (`:1857-1864`).
   - Across `pinn/`, the per-row `tau_ic13`/`masses` are only serialized and hashed
     (`controllers.py:320-334`, `:409-410`). No loss reads them.
3. **The anchor is the lowest ID among the step's 240 replay draws.**
   - `_sample_keys` returns `tuple(sorted(...))` (`pinn/data/batches.py:76-78`), and
     `keys[0]` is the replay minimum.
   - With a Stage-0 training pool of N₀ = 1,812, P(anchor = rank r) =
     C(N₀−r, 239)/C(N₀, 240). That gives P(rank 1) = 13.25 % and mean rank 7.5. The
     effective number of distinct anchors (1/Σp²) is 14.1 [OWN; script `pool.py`].
4. **The reconstruction is exact.** I reconstructed the per-step anchor
   sequence by replaying the run's numpy RNG stream from metadata alone.
   - **Inputs:** `splits.json`, plus per-file row counts of training and
     validation files; every Stage-0 trajectory has 126 snapshots.
   - **Validation:** the replay reproduces the frozen monitor batch's replay and
     lookahead keys exactly. Its RNG state equals the numpy state saved in
     `stage-0-init.pt`, `best.pt` (after step 900 and validation), `step-000931.pt`,
     `step-000941.pt`, `step-000951.pt`, `failure-stage-0-step-951.pt` (after the
     halted iteration-952 draw) and `latest.pt` [OWN; Appendix A, `anchors.py`].
   - **Result over the 951 completed steps:**
     - The physics and IC terms saw **40 distinct trajectories**.
     - **74.7 %** of steps used one of the 10 lowest-ID Stage-0 trajectories.
     - IDs 0 and 1 alone took 132 and 111 steps.
   - **The monitor.** It is the anchor of its own frozen batch, **trajectory 28**
     (Stage-0 rank 13; the checkpoint `front_monitor.batch.replay_keys` begins
     `[28, 90, 104, 147, 167]`). It was the training anchor on **31** steps: 17, 179,
     204, 232, 271, 286, 290, 296, 330, 334, 336, 350, 409, 470, 476, 477, 481, 551,
     624, 642, 687, 704, 709, 738, 757, 785, 813, 892, 901, 908, 943.
   - A sub-agent rebuilt the monitor from checkpoint contents alone: weights plus the
     serialized frozen batch, CPU float32, no data source. It reproduced the verdict
     packet's replay values and confirmed that all 4,096 monitor times are evaluated
     on trajectory 28's `IC13`.
5. **The project's own Phase-57 records required per-slot evaluation and listed
   one-anchor execution as nonconformant:**
   - `57-RESEARCH.md:70` — the pre-57 controller "select[s] one anchor identity";
   - `:138` — "Remove anchor-only physics from the production causal path; consume
     every selected-slot row";
   - `:188` — "setting 4096 while keeping random global times, **one anchor**, or
     per-microbatch prefixes is still nonconformant";
   - `57-02-PLAN.md:23`, `:84` — must-have: "every selected slot contributes physics
     gradients".

   `57-02-SUMMARY.md:100` and `:106` record the task as "Replace anchor-only physics
   with complete normalized causal loss". The implementation replaced only the *time
   source*. The updated regression test proves only that poisoned *times* propagate
   (`tests/phase40/test_optimizer_phase.py:686-720`).
6. **The conformance verifier's anchor check passes by construction.**
   - It asserts that the *sampler's emitted* row keys are not all one identity
     (`pinn/verification/phase57_production_conformance.py:408-411`).
   - It then calls the anchor path (`:413-415`) and writes the literal
     `"anchor_only": False` (`:533`).
   - Its synthetic source was built so that "accidental anchor-only paths [would be]
     observable" (`:251-254`). No assertion uses that.
7. **The validation path is single-trajectory and single-point.**
   - `_run_validation` requests `collocation_count=1` (`controllers.py:1384`).
   - It anchors on the lowest-ID validation trajectory, which is always **ID 12**
     (`:1385`; `select_validation_records` returns the sorted pool).
   - So `val_phys`, which feeds ADVANCE criterion 3, is one time point on one fixed
     validation trajectory.

**Consequences for this round.**

- **(a) Invariant B tracked one training trajectory**, not the 256 frozen
  identities 57-RULING describes.
- **(b) The training-batch front is not a resampled estimate of the monitor's
  front.** Each step it is a *different trajectory's* front. The identity of the
  anchor explains 51 % / 28 % / 21 % of the detrended variance of `log R̃` in bins
  0 / 1 / 2. By contrast, re-sampling the times of the same trajectory at fixed
  parameters moves S₁ and S₂ by only about 4–8 % (step 901 vs `best.pt`; step 943 vs
  steps 941 and 951) [OWN; `anal1.py`].
- **(c) The IC term's step-to-step swings (F-07) are a single-trajectory quantity.**
  The swings depend strongly on how often that trajectory has been the anchor:
  - ID 0 (132 steps) ended with IC loss 26–59;
  - the monitor's trajectory 28 (31 steps) ended at 2.3 × 10³ – 2.2 × 10⁴;
  - the run-minimum IC loss of 25.7 at step 947 is ID 0 [OWN; `anal5.py`].
- **(d) `R_ref` and GATE-04 were measured on single-trajectory cases.** These are six
  (network seed, IC) pairs with 4,096 stratified times each
  (`pinn/verification/gate04_train_free.py:703-754`; sub-agent file A, §E3).
  - They are therefore consistent with the anchor path, not with per-slot
    evaluation.
  - A conformant per-slot estimator changes "count unit, selected-slot semantics".
    Both are named invalidation triggers (`pinn_architecture.md:454`), so `R_ref`
    and GATE-04 must be redone after any conformance fix.

**Classification.** This is an implementation non-conformance against the ratified
contract *as the project itself read it* (57-02 must-haves). The executed run did
not match the specification, which is the trainex-r3 pattern recurring. An owner
may still prefer to ratify anchor semantics instead. That choice is §4 decision D0.

### PC-2 (CONTRADICTED in substance) — The causal physics term was effectively not trained; the run measured something other than causal training

**The package says** [PKG].

- The stall is framed as a causal-weighting and front-pace question (prompt "The
  problem"; master §4).
- `54-RULING` point 2 (H-01) holds that residual-wide normalization "addresses the
  established severe physics/data conditioning mismatch".

**The repository shows.**

1. **The logged gradient ratio rules out physics influence under Adam.**
   - The applied IC gradient norm exceeded the applied physics norm by
     2.78 × 10⁴ – 2.62 × 10⁶ on every diagnostic step (F-08 [PKG]; re-verified by
     sub-agent).
   - Adam's update is `−lr · m̂/(√v̂+ε)`, with both moments built from the *summed*
     gradient. A component 10⁻⁴–10⁻⁶ of the dominant one contributes the same tiny
     fraction of the update [OWN].
   - The retained optimizer state shows a noise-dominated regime: median
     |m̂|/√v̂ = 0.039 at step 951 (p90 0.115). Gradient clipping never bound (peak
     norm/threshold 0.73) [OWN; `ckpt.py`].
   - The imbalance was measurable **before the run**. The Phase-57 production
     conformance record shows, at initialization, raw IC gradient 3.80 × 10⁸, physics
     215 and data 60.3
     (`.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/production-conformance.json:107-110`).
2. **Natural experiment from the run's own data.**
   - **Method.** When the same anchor occurs on consecutive steps, the second step's
     forward pass measures the effect of exactly one update on that anchor's own
     terms.
   - **Generation 7, 57 such pairs:** IC loss decreased in **65 %** (median
     Δlog₁₀ = −0.144, about −28 %). The normalized physics loss decreased in **42 %**
     (median +0.002). S₂ = R̃₀+R̃₁+R̃₂ decreased in 49 % (median 0.000).
   - **Generation 6, 32 pairs:** IC loss decreased in 69 %, physics in 41 %, S₂ in
     38 % [OWN; `anal3.py`].
   - Each update reliably lowers its anchor's IC loss. It does not lower that
     anchor's physics residual.
3. **The front moved by amplitude shrinkage, not by a causal sweep.**
   - The output-layer weight norm fell 1.7525 → 1.1715 (×0.668). All 9 rows shrank
     alike (≈0.59 → ≈0.39), while hidden-layer norms rose 1–2 % [OWN; `norms.py`].
   - For fixed hidden features the curvature scales with the head, so the squared
     residual scales with 0.668² ≈ 0.45 in every bin.
   - The population's median per-bin R̃ fell 2.3–5.6× from steps 1–100 to steps
     852–951 *in every bin* — bins 13–15 by 2.3–2.9× [OWN; `anal4.py`].
   - A causal sweep predicts early bins first and late bins held back by small
     weights. The data show a near-uniform drop. That fits the residual being
     dominated by the network's own curvature.
   - At initialization ‖a′‖ ≈ 1.9–2.4 × 10⁵ against ‖F_grav‖ ≈ 3–6 in the Phase-55
     probe, and R̄ ≈ ‖a′‖²/3 holds to four figures. Shrinking that curvature shrinks
     every bin's residual whether or not physics is learned
     (`.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/raw.json`,
     per sub-agent file A §E1).
4. **No absolute physics improvement.** The in-run validation gate covers all 227
   validation trajectories at steps 100…900.
   - Median per-trajectory energy drift `eps_H = max_t |H(t)−H(0)|/|H(0)|` was
     0.983–0.990 at every check, with no trend.
   - No trajectory fell below 0.5. The gate threshold is 10⁻⁵
     (`runs/stage0-v23g7-seed42/validation_gate/step-00000{100…900}.json`;
     definition `pinn/verification/gate_metrics.py:180-200`, threshold `:64`).

**Consequence.**

- Generation 7 tested IC-plus-data training of ~40 anchors with a causally weighted
  physics *diagnostic* attached. It did not test the causal-training recipe.
- Every question that asks why "the causal front" paced as it did has to be read
  through this. The front's motion is a byproduct of shedding initialization
  amplitude.
- §3 develops it.

### PC-3 (QUALIFIED) — L-BFGS was unreachable in the configuration that ran

**The package says.** F-05 and §4.1: "Handoff: to L-BFGS at budget exhaustion or at a
physics-loss plateau" [PKG].

**The repository shows.**

1. **The budget-exhaustion path gives L-BFGS zero budget.** On that path the
   remaining budget is `max(max_epochs − adam_epochs_used, 0)`, which is **0** when
   `max_epochs == n_adam == 1000`. The stage-exit machine is then polled once, and an
   unmet gate returns HALT (`controllers.py:2690-2707`; config F3 [PKG]).
2. **The plateau path could not fire.** The detector needs **50 consecutive**
   steps with per-step `Δlog₁₀ L_phys > −5 × 10⁻³` (`controllers.py:134-135`,
   `:518-562`). Its input is the per-step, single-anchor physics loss, which is
   noisy.
   - **Longest qualifying run:** 6 in generation 7, 4 in generation 6, 4 in the smoke.
   - **Resets** (steps with slope ≤ −5 × 10⁻³): 433 in generation 7.

   Confirmed by my replay (`plateau.py`) and independently by the verifier
   (`verify/log_checks_output.txt`, "F-05").

**Consequence.** Had invariant B not tripped, the stage would have ended at step
1000 with the learning rate at about 0, without L-BFGS, and HALTed unless the gate
passed. Q1 and Q4 should treat the second optimizer phase as **absent by
configuration**, not as untried by bad luck.

### PC-4 (CONTRADICTED) — Generations 6 and 7 are not independent; generation 6 never ran a full window

**The package says.** H-02, verdict-packet §4: "Two independent runs (gens 6 and 7)
stalled at the same index" [PKG, H-row].

**The repository shows.**

1. **Identical batch sequences.** The RNG stream that selects batches consumes
   random numbers as a function of pool sizes and per-key snapshot counts only:
   - `rng.choice` in `_sample_keys` (`batches.py:76-78`);
   - `rng.gumbel(size=n_snapshots)` (`:238`);
   - `rng.choice(remaining, …)` (`:292`);
   - fixed per-bin uniform draws (`:348-367`);
   - validation draws on a fixed pool.

   It never depends on model outputs. With the same seed, splits and code path,
   generations 6, 7 and the smoke drew **identical batch and anchor sequences**.
   - My replay matches generation 7's checkpoints exactly.
   - The verifier found the smoke and the graded run bit-identical at steps 1–2.
     They first differ at step 3, after the two learning-rate schedules diverge
     (`verify/log_checks_output.txt`).
   - All three runs score the same monitor trajectory, 28.
2. **Float32 nondeterminism alone makes training diverge chaotically.** On the
   *same* batches, trajectory 28's S₁ was:
   - equal to three decimals through step 271 (parameters bit-identical through about
     step 269, per the verifier);
   - 2.575 (generation 6) vs 1.856 (generation 7) at step 286;
   - **0.460 vs 1.296 at step 409** [OWN; `anal2.py`].

   The verifier measured the correlation of log IC loss between the two runs over
   steps 270–513 at 0.17, against 0.11 for a one-step-shifted control.
3. **Generation 6 never completed a window.** Its high-water mark reached 2 at
   step 353 and the process died at 513. It never had a 500-step window after its
   last advance (F-13 [PKG]), so it did not "stall" in invariant B's sense.

**Consequence.**

- There is one batch sequence, one monitor trajectory and one seed: one
  experiment observed twice through floating-point noise.
- When the front advances (353 vs 450) is **not reproducible** even under identical
  data order. It is the wrong unit for any rate claim.

### PC-5 (QUALIFIED) — An in-run absolute-accuracy measurement exists at known front states

**The package says.** Master §7, Q2: "No measurement relates an `R_ref`-relative front
state to absolute trajectory accuracy, because no evaluation was run at any front
state" [PKG].

**The repository shows.**

- The validation gate scored all 227 validation trajectories at every 100th step
  (`runs/stage0-v23g7-seed42/validation_gate/`).
- Its median `eps_H` was 0.986 / 0.983 / 0.984 / 0.984 / 0.984 / 0.986 / 0.990 /
  0.989 / 0.987 at steps 100…900. Every verdict was FAIL; the threshold is 10⁻⁵.
- Over the same steps the relative front went from 0 to 2, and the population median
  R̃ fell about 3×.
- **Caveats.** `eps_H` is a *self-consistency* metric. It measures the drift of the
  predicted trajectory's own matched-Plummer Hamiltonian, with velocities from
  finite differences of predicted positions (`gate_metrics.py:150-220`). It is not
  error against Brutus. It is also on the validation split, not the held-out test
  split.

**Consequence.** The relation Q2 asks about *is* observed once. Relative progress did
not move this absolute conservation metric at all.

### PC-6 (QUALIFIED) — "No further progress after step 450" applies to the guard statistic, not to the residuals

**The package says.**

- The prompt says the front "then made no further progress".
- H-02 reads the end state as "flat over the last 20 steps (1.192 → 1.189)" and says
  the front "oscillates; it does not creep" [PKG].

**The repository shows.**

- **The monitor's trajectory kept improving.** Trajectory 28's training-batch
  samples are the same trajectory measured on fresh times; at equal parameters they
  read within 4–8 % of the monitor. Its S₂ was about 2.1–2.6 at steps 470–481 and
  1.12–1.40 at steps 892–943.
- **The population kept improving.** Median S₂ was 2.33 in the 401–500 block and
  0.99 in the 901–951 block. Median S₁ fell 1.24 → 0.48 [OWN; `anal1.py`,
  `anal2.py`].
- **Flatness at the end reflects a vanishing learning rate.** The last 20 steps hold
  about 0.03 % of the run's cumulative learning rate.

**Reading.** The *prefix sums* crept steadily. The *discrete front* hovered around a
threshold. H-02's arithmetic (the 42 % reduction still needed) is right; its "does not
creep" is not.

### PC-7 (QUALIFIED) — F-09's "resampled training batches" mislabels the source of variation

**The package says.** F-09 attributes the training-batch front's spread to resampled
batches [PKG].

**The repository shows** (PC-1(b)):

- The dominant source is **which trajectory** the step evaluates. Time resampling
  is minor.
- The training-batch front reached 3 only on anchors 1 and 9, which had 111 and 70
  direct steps, plus once on anchor 22 (35 steps). The monitor's trajectory 28 had 31.

The 54-RULING premise behind the front-monitoring boundary still holds in direction:
a high-water mark over changing samples is biased upward. But its implied mechanism
(changing slots and times within a batch) does not match what was executed.

### PC-8 (QUALIFIED) — "Proven healthy at initialization" is narrower than it sounds

**The package says.** The prompt: the fix "was proven healthy at initialization
before any run was spent" [PKG].

**The repository shows.**

1. **GATE-04's controlled-reduction condition is algebraically guaranteed.**
   - Every residual is scaled by `α = ln(√2)/P₁₅`, so `w′₁₅ = 1/√2` by construction
     (57-RULING §1 [PKG]).
   - It confirms that the production code computes `exp(−prefix)` without floor
     clamping. It cannot test whether *training* moves residuals.
2. **GATE-04 ran single-trajectory cases with six different network seeds**
   (sub-agent file A §E3). So it did not exercise the per-slot semantics (PC-1).
3. **The initialization gradient imbalance (PC-2) was on record before the run**
   (`production-conformance.json:107-110`), and no gate examined it.

### PC-9 (QUALIFIED) — Epoch semantics: every "epoch" in the code is one optimizer step

**The repository shows.**

- `_global_epoch` increments once per Adam step (`controllers.py:2165-2167`), and the
  logged `epoch` equals `step`.
- Per step, therefore:
  - `max_epochs = 1000`;
  - the plateau criterion's "50 consecutive epochs";
  - `validation_every = 100`.
- The specs never define "epoch" for a replay batch scheme. A replay-coverage
  reading would make one Stage-0 pass ≈ 1,812/240 ≈ 7.6 steps.

**Consequence.** This is a definitional gap feeding Q4 (§5, G-6). It is recorded,
not resolved.

### PC-10 (QUALIFIED) — Physics/data balance was improved by `B2`, but the binding imbalance was always IC

H-01 point 2 is assessed in §3.7. Briefly:

- After `B2` the physics/data **raw-gradient** ratio is about 16–520×, for example
  raw physics 91–758 against applied data 1.45–5.78 (F-08 [PKG]). Physics still leads
  data.
- But IC exceeds physics by 2.8 × 10⁴ – 2.6 × 10⁶, and data by about 10⁷ – 10⁸.
- The ruling's conditioning analysis did not include the IC term. That term was
  dominant at initialization by about 10⁶ (PC-8.3).

### PC-11 (CONFIRMED) — The verbatim and arithmetic premises the package marks as established

**Confirmed, with the caveats noted:**

- **F-03, recomputed from the Part B raw output.** Bins 0–5 reduction factors are
  3.51, 2.73, 3.22, 2.21, 2.06, 1.51. The 16-bin median goes 1.1058 → 0.6578 (×1.68).
- **H-02's distance arithmetic, re-derived** [OWN]:
  - 1.1891 → 0.6931 is a 41.7 % reduction;
  - 3.88/0.693 = 5.6;
  - a full front needs a 15-bin mean below 0.0462;
  - that is 21.6× below R̃ = 1, or 23.9× below this monitor's initial median of 1.1058;
  - the raw bound is 9.13 × 10⁸.
- **F-04's learning-rate law.** The logged `lr` matches `10⁻³(1+cos(πs/1000))/2` to
  3.4 × 10⁻¹⁵ relative. That fits `T_max = n_adam = 1000`, with `lr` logged after
  `scheduler.step()` (sub-agent; `controllers.py:2162-2163`, `:2658-2660`).
- **F-06's warm-up.** `λ_phys = min(1, (step−1)/100)` exactly (sub-agent).

### PC-12 (QUALIFIED) — Monitor robustness was never part of the invariant-B ruling's test surface

**The repository shows.**

- The guard reads only the frozen monitor (`pinn/train.py:192-202`). Its state is a
  monotone high-water mark: "transient front regressions never reset the age"
  (`pinn/training/guards.py:597-631`).
- With the monitor being one trajectory (PC-1), the high-water mark is a **record
  statistic** of one noisy, threshold-discretized series. Its noise amplitude scales
  with the learning rate. Its "advance" timing differs by about 100 steps between two
  runs on identical data (PC-4).
- 57-RULING §2 added "no new front margin, observation cadence, or persistence-count
  threshold". Nothing in the record tests the statistic's variance.

### 2.13 Per-row status of F-01…F-18

An independent sub-agent checked every F-row against the live tree. Its report is
`scratchpad/r4/verify/f-row-verification.md`; its scripts and outputs sit beside it.

- **Part G.** It re-derived the digest. The script's SHA-256 `d28c7d92…` matches
  when the extracted text ends in exactly one newline. The output matches the
  bundle 180/180 lines, differing only in Markdown framing blank lines.
- **Monitor.** It recomputed the frozen monitor from checkpoint contents alone (CPU
  float32, no data source) and reproduced all 8 Part B rows to 4 decimal places.
- **Code identity.** `pinn/`, `configs/`, `runs/` and both live specs are
  byte-identical between the package baseline `735e2ae8` and this pin. `pinn/` is
  identical between generation 6's and generation 7's run commits.

| Row | Status | Note (my cross-reference) |
|---|---|---|
| F-01 | CONFIRMED | Record 952 is the halted iteration. The failure checkpoint's model equals step 951's and its RNG is one batch further. |
| F-02 | CONFIRMED (values); context | Every value is a **single-trajectory** quantity (trajectory 28) — PC-1. |
| F-03 | CONFIRMED | 3.507/2.732/3.216/2.205/2.055/1.512; median 1.1058 → 0.6578. |
| F-04 | QUALIFIED (minor) | `lr` at step s is the rate for update s+1. "0.001 at step 1" is 9.999975 × 10⁻⁴ rounded. |
| F-05 | **CONTRADICTED in part** | No L-BFGS at budget exhaustion when `max_epochs == n_adam`; plateau path inert — PC-3. `train.log:964` misleadingly logs a "budget-exhausted" hand-off after the invariant-B HALT (`controllers.py:2684-2688`, `:2998-3012`). |
| F-06 | CONFIRMED | `λ_phys = min(1, (step−1)/I_warm)` exactly. The warm-up tie to the Adam budget is the spec's formula (`pinn_architecture.md:699`), not a code choice. |
| F-07 | CONFIRMED (values); context | `loss_ic` and `loss_phys` are single-anchor, exposure-dependent quantities — PC-1(c). |
| F-08 | CONFIRMED | `raw` is the true global norm of the λ-free (still causally weighted, `R_ref`-normalized) term, pre-clip. |
| F-09 | CONFIRMED (values); framing qualified | "Resampled" mislabels the variation source — PC-7. |
| F-10 | QUALIFIED (minor) | The guard's fallback to training-batch stats is unreachable on the Adam path, so generation 7 read only the monitor. The spec cross-reference "the fixed-monitor boundary above" at `pinn_architecture.md:452` points at nothing in that file. |
| F-11 | CONFIRMED | Corroborated by GATE-04's stored late-bin-only diagnostics: all front 0. |
| F-12 | **QUALIFIED (material)** | Single-trajectory evaluation — PC-1. Five of six `R_ref` probe cases are synthetic (`ic13_mode: zero`, masses (1,1,1)), CPU float64. Training used dataset ICs in float32 on MPS. |
| F-13 | **QUALIFIED (material)** | Parameters bit-identical through ~step 269 (differences before that are evaluation noise). Identical batch and validation sequence for all 513 steps and the identical monitor — PC-4. |
| F-14 | QUALIFIED (minor) | The generation-5/6/7 smokes are **bit-exact reproductions**, not corroboration. The smoke monitor's instantaneous front was **0** again at steps 100/200/300, so its front-1 state at step 93 was transient — direct evidence for M1.2/M5.1. |
| F-15 | CONFIRMED | Its consequence for L-BFGS: PC-3. |
| F-16 | CONFIRMED | — |
| F-17 | CONFIRMED | — |
| F-18 | CONFIRMED | — |

**Bundle-internal (minor).** Part G's lead-in says the replay "scores the frozen
monitor at four checkpoints" (`v2.3-closure-evidence-bundle.md:1117`). The packet's
Appendix A and Part G's own notes say five generation-7 and three generation-6
checkpoints.

---

## 3. Part 2 — Diagnosis (master §5.1–§5.5, satisfying §5.6)

### 3.0 Shared evidence base (new read-only analyses, all re-derivable — Appendix A)

| ID | Analysis | What it establishes | Script |
|---|---|---|---|
| E-A | Exact per-step anchor reconstruction from the RNG and metadata, validated against the RNG state in 7 checkpoints | which trajectory each training step's physics and IC terms (and the training-batch front) measured; monitor = trajectory 28; validation anchor = 12 | `anchors.py`, `pool.py` |
| E-B | TensorBoard per-bin series (raw and normalized, steps 1–952) joined to E-A | the recomputed front equals the logged `front_idx` on every record; raw/`R_ref` = normalized to 8 × 10⁻⁸ | `tbjoin.py` |
| E-C | Same-trajectory, same-parameter comparisons (step 901 vs `best.pt`; step 943 vs 941/951) | time-resampling noise on S₁/S₂ is about 4–8 % | `anal1.py` |
| E-D | Natural experiment on consecutive same-anchor pairs | one update lowers the anchor's IC loss, not its physics residual (PC-2) | `anal3.py` |
| E-E | Physical scales of Stage-0 training trajectories | median per-body ‖a′‖ = 159 (p99 2,070); median ‖v′(0)‖ = 2.03; every `t_end` = 10 | `scales.py` |
| E-F | Checkpoint tensors | output-layer norm ×0.668; global drift 18 %; first-layer τ-frequency RMS 1.22 → 1.35; Adam \|m̂\|/√v̂ median 0.039; the clip never bound | `ckpt.py`, `norms.py` |
| E-G | Volatility and trend against learning rate | S₂ volatility shrinks with lr while IC volatility does not; late progress per unit lr is higher | `anal2.py` |
| E-H | Validation-gate records | median `eps_H` 0.983–0.990 at steps 100–900, no trend | inline (§2 PC-5) |

**Notation.**

- S_k = Σ_{b≤k} R̃_b. The front advances from k to k+1 only when S_k < ln 2 =
  0.6931 (F-11 [PKG]).
- "Full-LR-equivalent steps" is N_eff(t) = Σ_{s≤t} lr_s / lr₀.
- Under the executed cosine schedule, N_eff over all 1000 steps = **499.4**:
  - N_eff before step 450 = 381.4 (76.4 %);
  - N_eff between steps 450 and 951 = 118.0 (23.6 %) [OWN; `anal2.py`].

### 3.1 Q1 — the invariant-B window and the learning-rate schedule

> *"Is the coupling between the invariant-B window and a learning-rate schedule that
> decays inside it a design flaw, and how should the two relate?"*

**Short answer [OWN].** Yes, it is a design flaw. In this run, though, it was not the
*learning-rate decay* that stopped learning. Two things decided the trip:

- the guard's statistic — a monotone record over **one** trajectory's
  threshold-discretized, learning-rate-scaled noisy prefix sum (PC-1, PC-12);
- the fact that physics was not being trained at all (PC-2).

The decay mattered only in the last ~100–150 steps.

**The structural flaw is easy to state.**

- **Unit mismatch.** The cosine-to-zero schedule over 1000 steps contains about 500
  full-learning-rate-equivalent steps of optimizer motion *in total*. The window is
  500 *raw* steps. A window opening at step 450 holds only 118 full-learning-rate-
  equivalent steps.
- **Noise-scaled record statistic.** At high learning rate, records are set by
  noise. At low learning rate, only trend can set them, and the trend is starved.

Under this pairing the guard's verdict is a function of *where in the schedule* the
window falls, not of whether learning continues.

**Mechanisms the evidence admits.**

| # | Mechanism | Predicts for recorded quantities | Evidence (label) | Confidence | What would change it |
|---|---|---|---|---|---|
| M1.1 | **Learning-rate starvation.** Progress per step ∝ lr, so the 94× decay in the window starves it | ln S_k declines ∝ cumulative lr; per-unit-lr progress constant; population S₂ flat once lr ≪ lr₀ | **Against:** population median S₂ fell 2.33 → 0.99 between blocks 401–500 and 901–951, while lr fell ~40× and only 23.6 % of lr mass remained. Per unit cumulative lr, late progress was *higher*: d ln S₂/d(Σlr) for trajectory 28 went −0.06 → −4.4 → −16.2 across the three thirds; anchors 1 and 9 behaved alike. **For:** the decline slowed in the last block (median S₂ 1.05 → 0.99 between 801–900 and 901–951) [OWN, E-B/E-G] | LOW as the cause of the trip; MEDIUM–HIGH that it throttled the last ~100–150 steps | a constant-lr replicate on the same batch sequence showing a much earlier front-3 record (E7) |
| M1.2 | **Record-statistic artefact.** The high-water mark of a single trajectory's noisy, thresholded S_k; records come from noise at high lr and from trend at low lr | high-water set at a transient during high-lr volatility; continuous S_k keeps falling after the last "advance"; advance timing irreproducible across numerically different runs | **For:** 2 at step 450, while trajectory 28's fresh-time samples nearby read S₁ = 1.30 (step 409) and 0.95–1.17 (470–481) — a ≥30 % excursion; resampling noise is only 4–8 % (E-C). Its S₂ fell ~2× after 450 (PC-6). Generations 6 and 7 advanced at 353 vs 450 on *identical* batches (PC-4). S₂ volatility per ≤10-step gap: median \|Δlog₁₀\| 0.088 at lr > 5 × 10⁻⁴ and 0.013 at lr < 10⁻⁴ (E-G) [OWN] | HIGH | a per-step monitor trace showing a sustained (not transient) S₁ < ln 2 from step 450 |
| M1.3 | **No physics learning.** The front moves only as initialization amplitude is shed under IC/data pressure, which decelerates as the IC fit improves and lr falls | uniform per-bin decline; head-norm shrinkage; one direct update does not lower the anchor's physics residual; absolute metric flat | **For:** PC-2 items 1–4 (E-D, E-F, E-H) [OWN] | HIGH that physics learning was negligible; MEDIUM that head shrinkage is the main channel (hidden layers also moved, split not decomposed) | E2 (Adam-preconditioned per-term decomposition) or E6 (λ_phys = 0 control) showing material physics influence |
| M1.4 | **Training on the monitor trajectory too rare.** 31 direct steps of 951; most motion comes from other anchors | anchors with more exposure reach deeper fronts; monitor lags the best-trained anchors | **For:** only anchors 1 and 9 (111 and 70 steps) reached front 3. IC error scales with exposure: anchor 0 ended at \|Δv′\| ≈ 5.8; trajectory 28 at ≈ 107 (E-A, `anal5.py`) [OWN] | MEDIUM — exposure and trajectory difficulty are confounded | E3 (front of non-anchor and low-exposure trajectories at fixed checkpoints) |

**Quantified against the front-advance condition** [OWN, from Part B raw output and
E-B].

- **At the trip.** The monitor's S₁ = 0.5505 (front 2 holds, 0.14 below ln 2) and
  S₂ = 1.1891. A new record needs S₂ < 0.6931, a 41.7 % fall (H-02 arithmetic,
  confirmed).
- **Noise cannot close that gap at the end.** The observed late volatility, median
  \|Δlog₁₀ S₂\| ≈ 0.013 (≈3 %) per occurrence, rules it out.
- **Trend could, in principle.** Trajectory 28's mid-window trend, about −0.0015
  per step in ln S₂ (S₂ ≈ 2.3 → 1.15 over steps ~475 → 943), would need ln(1.15/0.693)
  / 0.0015 ≈ **340 more steps at the mid-window learning rate**.
- **The schedule cannot supply it.** The schedule holds 0.6 full-learning-rate-
  equivalent steps after step 951.

**Telemetry (F-07, F-08) bearing.**

- **F-08 is the decisive fact for Q1.** The window measured an optimizer that was
  not optimizing the physics term (PC-2).
- **F-07's IC swings are mostly per-trajectory and per-exposure (PC-1(c)).** The
  same anchor's IC loss changes by a median factor ≈ 2 between occurrences ≤ 10 steps
  apart, at *every* learning rate. Median \|Δlog₁₀ IC\| was 0.30 / 0.28 / 0.35 /
  0.30 across the four lr bands (E-G).
- That is hypersensitivity of the network's `v′(0)` to its parameters. It does not
  decay with the learning rate.

**How the two should relate.** These are options, not a ruling (§4, D3/D4):

- (i) Express the window in an optimizer-motion unit (N_eff), or define it per phase.
- (ii) Use a continuous, smoothed statistic on a multi-slot frozen monitor, such as
  the regression slope of ln S_{front} over the window. Do not use a record of a
  thresholded single-trajectory value.
- (iii) Keep annealing tails and L-BFGS outside the liveness window, or give them
  their own criterion.

The literature has no counterpart to invariant B (§3.6). The causal-training papers
pair their weights with long budgets and slow decay.

**Discriminating experiments.** E2, E3, E6 and E7 in §3.9.

### 3.2 Q2 — the front criterion: relative to `R_ref` or absolute?

> *"Should the causal-front criterion measure progress relative to initialization
> (R_ref) or absolute physical accuracy?"*

**Short answer [OWN].** As a *success* criterion, the `R_ref`-relative front is
uninformative about physics.

- A fully advanced front still permits an RMS residual 190× the median true
  acceleration.
- It can be reached by shedding initialization amplitude alone.
- An absolute criterion is needed for stage success.

A relative front stays usable as a *pacing or liveness* signal, but only once
measured robustly (Q1, Q5). The published method sets its causal tolerance in the
residual's own units and tightens it by schedule (§3.6). That is the absolute
reading, made progressive.

**Arithmetic (equal bins; per-body RMS residual |f| ≈ √R̄)** [OWN, E-E;
`R_ref` = 1.9750 × 10¹⁰]:

| State | Condition | R̄ per bin | RMS \|f\| | ÷ median true ‖a′‖ (159) | ÷ p99 ‖a′‖ (2,070) |
|---|---|---|---|---|---|
| Initialization | R̃ ≈ 1 | 1.97 × 10¹⁰ | 1.41 × 10⁵ | ≈ 890× | ≈ 68× |
| Full front | Σ_{b≤14} R̃ < ln 2 ⇒ mean R̃ < 0.0462 | < 9.13 × 10⁸ | < 3.0 × 10⁴ | ≈ 190× | ≈ 15× |
| Physically meaningful (≤ 10 % of median ‖a′‖) | — | ≲ 2.5 × 10² | ≲ 16 | 0.1× | — |

- **In R̃ units**, physically meaningful residuals sit at about 10⁻⁸. The full-front
  bound is about 0.046, a gap of roughly 6–7 orders of magnitude.
- **GATE-04's stored condition-(iii) diagnostics show this directly** (sub-agent
  file A, §E3). Uniformly scaling a case's initialization residuals by 0.05 (a 20×
  drop in squared residual, 4.5× in amplitude) already gives front 9–15. Scaling by
  0.01 (100×, 10× in amplitude) gives front 15 in all six cases. Uniform shrinkage of
  that size advances or completes the front with no physics content.
- **Generation 7 shows the mechanism live.** The head norm fell ×0.668, the
  per-bin medians fell 2.3–5.6× uniformly, and `eps_H` stayed flat (PC-2, PC-5).

**Mechanisms and readings.**

| # | Claim | Evidence | Confidence |
|---|---|---|---|
| R2.1 | The relative front measures shedding of initialization curvature while the residual is curvature-dominated (R̄ ≈ ‖a′‖²/3) | Phase-55 identity R̄ ≈ ‖a′‖²/3 to 4 significant figures at init (sub-agent file A §E1); uniform per-bin decline; head shrinkage [REPO/OWN] | HIGH |
| R2.2 | Relative progress did not move the in-run absolute metric | `eps_H` median 0.983–0.990, flat while the front went 0 → 2 (PC-5) [REPO] | MEDIUM — one run; `eps_H` is a conservation metric, not trajectory error |
| R2.3 | A relative criterion is still useful for pacing early in training | its sensitivity to uniform scaling is what makes it responsive at init (GATE-04 condition iii); also why it is no success signal | MEDIUM |
| R2.4 | A front can advance while the IC is unmet | the front reads only the physics residual. Without an IC anchor or hard constraint, a physics-satisfying trajectory with the wrong IC is admissible. This run had the reverse imbalance, but rebalancing (D1) makes it live | MEDIUM (analysis) |

**Telemetry bearing.**

- F-08 matters: with physics untrained, the front cannot be a physics-progress
  signal in this run.
- F-07 matters for R2.4. Any absolute success criterion must include the IC error,
  and IC error here is exposure-dependent: |Δv′| ≈ 5.8 for the best-trained anchor,
  ≈ 107 for the monitor trajectory, against true |v′(0)| ≈ 2.

**Discriminating experiments.**

- **E9 (read-only).** Score the monitor batch at retained checkpoints with residuals
  normalized by each slot's true acceleration scale instead of `R_ref`.
- **E3.** Use the existing validation-gate pipeline at checkpoints 0 and 951.

### 3.3 Q3 — the SIREN initialization scale `ω₀ = 30` and the deferred power-skip stack

> *"Is the SIREN initialization scale `ω₀ = 30` (with the deferred power-skip
> ablation) the root of the slow pace?"*

**Short answer [OWN].**

- **The initialization derivative scale is an upstream contributor,** not the proven
  root. It produced the three conditions under which physics went untrained:
  - `R_ref ≈ 2 × 10¹⁰`, so `B2` divided physics by that factor;
  - initial `‖v′‖ ≈ 240–330` against true speeds of about 2 — this is the IC
    dominance;
  - IC hypersensitivity.
- **Within that scale, most of the *amplification* is built in the hidden stack, but
  `ω₀` remains a multiplicative *lever* of uncertain strength.** This is analysis
  pending E5.
  - **The first layer's own τ-frequency is modest.** The spec's bound
    U[−1/n_in, 1/n_in] with n_in = 14 gives the τ-column an angular frequency 30·W_τ
    of at most 30/14 = **2.14** per unit τ. The RMS at initialization is **1.22**
    (E-F), about 2.4 per unit u.
  - **The network's measured effective frequency is far higher.** ‖a′‖/‖v′‖ ≈
    **585–847** per unit u, and ‖v′‖/‖r′‖ ≈ 230–330 (sub-agent file A, §E1). Roughly
    two orders of magnitude therefore arise after the first layer, in the 12-layer
    stack.
  - **This matches the audit's estimate.** The 2026-08-17 audit estimated, without
    measuring it, a LayerNorm-squared Jacobian of about 3 per odd layer across six
    odd layers (≈ 3⁶ ≈ 729).
  - **Read as a lever, `ω₀` is not small.** Derivatives pass *through* the first
    layer, so v′ ∝ ω₀ and a′ ∝ ω₀² **if the stack's gains were unchanged**. That
    would make R̄ ∝ ω₀⁴.
  - **LayerNorm argues against that law below a crossover.** The skip path is
    `LN(x)²` with LN scale-invariant: LN(c·h) = LN(h) for c²·var(h) ≫ ε. Once a
    smaller `ω₀` drives the first layer into its near-linear regime, the skip path's
    output and its τ-derivatives stop shrinking with `ω₀`.
    - My rough crossover estimate is `ω₀·σ_z ≈ 0.7`, i.e. `ω₀ ≈ 7`, with σ_z ≈ 0.1
      the first-layer pre-activation spread [OWN].
    - The response to lowering `ω₀` is then probably sub-quartic, and may saturate.
    - Neither law has been measured.
  - **Training did not reduce the first-layer τ-frequency.** Its RMS rose from 1.22
    to 1.35 and its maximum from 2.14 to 3.28 (E-F).
- **No existing measurement decomposes the two factors.**
  `ArchitectureSpec` rejects every non-default depth, width, `p`, `ω₀` and LayerNorm
  setting (`pinn/architecture_spec.py:71-130`, per sub-agent file A §0). Gap G-3.

**Mechanisms.**

| # | Mechanism | Predicts | Evidence | Confidence | Changes it |
|---|---|---|---|---|---|
| M3.1 | The initialization derivative scale creates the conditions for PC-2 (IC dominance; tiny normalized physics gradients) and IC hypersensitivity | large ‖v′(0)‖ error, huge IC gradients, IC loss swinging ~2× per recurrence at any lr | IC raw gradient 3.80 × 10⁸ vs physics 215 at initialization (`production-conformance.json:107-110`); median `grad_norm` 1.34 × 10⁸; E-G [REPO/OWN] | HIGH that the scale feeds these; MEDIUM on "root" | E5 showing a smaller-gain init leaves IC/physics ratios unchanged |
| M3.2a | The first layer is where the amplification happens | first-layer τ-frequency ≫ 1 | **Against:** max 2.14, RMS 1.22 (first-principles bound + checkpoint) [OWN] | LOW | — |
| M3.2b | **`ω₀` is a strong lever:** R̄ ∝ ω₀⁴, so lowering `ω₀` cuts the residual scale steeply | ‖v′‖ ∝ ω₀ and ‖a′‖ ∝ ω₀² across ω₀ ∈ {1, 5, 10, 30} | **For:** chain rule with fixed stack gains. **Against:** `LN` scale-invariance re-normalizes the skip path once the first layer is near-linear (crossover ≈ ω₀ 7, my rough estimate) [OWN] | UNDETERMINED (both arguments analytic) | E5 sweep of ω₀ with the stack fixed |
| M3.3 | **The power-skip `LN(x)²` stack** builds most of the amplification | derivative gain ≈ 2·\|LN(x)\|/σ(x) per odd layer, compounding over 6 blocks | consistent with the 585–847 measured frequency vs ≤ 4.3 from the first layer; the per-layer gain estimate is unmeasured (audit D1) [REPO/OWN] | MEDIUM | E5 with the power branch removed or LayerNorm moved |
| M3.4 | Plain SIREN depth (12 layers) contributes frequency mixing beyond the power branch | harmonics from composed sines | not separated by any measurement | LOW–MEDIUM | E5 depth sweep |

**Telemetry bearing.**

- F-07: the initial IC loss of ~4 × 10⁴ is the squared `v′` error, which is the
  initialization's first-derivative scale.
- F-08: the 10⁴–10⁶ gradient ratios are that scale squared against the
  `R_ref`-normalized physics.

**Governance note.** Any change here means a fresh re-initialization ablation. It
invalidates `R_ref` and needs owner ratification (`pinn_architecture.md:184-188`;
`54-RULING`). The read-only decomposition E5 needs no amendment, since it only
*measures* alternative initializations, but it does need code paths that
`ArchitectureSpec` currently refuses (G-3).

### 3.4 Q4 — a realistic Stage-0 step budget for the front to cross 16 bins

> *"What Stage-0 step budget is realistic for the front to cross 16 bins?"*

**Short answer [OWN].** No defensible number follows from this evidence. Under the
executed recipe the question is ill-posed: the physics term is untrained (PC-2), and
the front's progress is the rate of amplitude shedding. Any extrapolation would
estimate how fast the network shrinks its spurious curvature, not how fast it learns
physics.

What the evidence *does* fix:

- **Cost per step.** ≈12 s/step on MPS (mean 12.07 over generation 7's 951 logged records, `train.log` `s/step`). Generation 7's 951
  steps took 11,662 s wall-clock, including validation and checkpoints (F1
  `wall_clock_secs` [PKG]). So 10⁴ steps ≈ 1.4 days and 10⁵ steps ≈ 2 weeks per seed
  on this hardware.
- **The executed configuration had no L-BFGS (PC-3).** The spec's two-phase budget
  was never exercised.
- **An amplitude-shedding extrapolation, labeled as such.** The population median
  S₁₄ fell from 28.9 (steps 1–100) to 9.08 (steps 852–951), about −0.00136 per step
  in ln. Crossing ln 2 at that average rate would take
  ln(9.08/0.693)/0.00136 ≈ **1,900 further steps at a schedule that supplies them**.
  Two things argue against reaching it:
  - the trajectory-28 monitor sits above the population;
  - amplitude shedding must saturate once IC and data fits stop rewarding smaller
    gains.
- **The literature's causal-training budgets are 10⁵–3 × 10⁵ iterations per ε stage
  or time window.** One jaxpi configuration uses 2 × 10⁴ (§3.6.2). So a conformant,
  physics-active run could plausibly need about two orders of magnitude more steps
  than 1000. Only a calibration run can say.

**Mechanisms bearing on the budget.**

| # | Mechanism | Implication | Confidence |
|---|---|---|---|
| M4.1 | Under the current dynamics, front speed = amplitude-shedding speed | the budget estimate is not about physics; reaching 16 bins this way certifies nothing (Q2) | HIGH |
| M4.2 | After conformance (D0) and loss rebalancing (D1), front speed reflects physics learning plus exposure per trajectory | the budget must be measured after D0 and D1 | MEDIUM |
| M4.3 | Late bins need physics propagation, not shrinkage: the causal-weighting rationale | budgets scale with the number of bins that must each "turn on" in sequence | LOW–MEDIUM (literature-based) |

**Discriminating experiment.** E8 is a diagnostic calibration pilot under the
corrected recipe, with invariant B observe-only, recording N_eff per bin advance.
A budget should be set as a multiple of the measured crossing time.

### 3.5 Q5 — the 1↔2 oscillation and what the monitor exposes

> *"Does the front's oscillation between 1 and 2 point at a stability issue the
> frozen monitor exposes but the training batches hide?"*

**Short answer [OWN].** The monitor exposes no hidden stability issue that the
training batches conceal. The two measure different things:

- the monitor measures **one** trajectory (28) at frozen times;
- the training batch measures **a different trajectory each step**.

The 1↔2 oscillation is **threshold hovering**. Trajectory 28's S₁ trended down through
ln 2 late in the run (0.728 at step 900; 0.549–0.551 at 931–951; fresh-time samples
0.53–0.94 over steps 738–943), with parameter-driven volatility on top.

There is a genuine stability issue, but it is visible in *both* telemetries:

- the IC term is hypersensitive: about 2× swings per recurrence at every learning
  rate (E-G);
- training trajectories diverge chaotically under float32 nondeterminism (PC-4).

**Mechanisms.**

| # | Mechanism | Predicts | Evidence | Confidence |
|---|---|---|---|---|
| M5.1 | **Threshold hovering:** a single-trajectory S₁ near ln 2 with noise | front flips 1↔2 with no regime change; flip rate falls with lr | S₁ values above; volatility vs lr (E-G) | HIGH |
| M5.2 | **Cross-anchor interference:** updates on other anchors (97 % of steps for trajectory 28) perturb its early-time fit | monitor moves between its own direct steps; direct steps do not systematically improve its physics | E-D natural experiment; IC error of trajectory 28 still \|Δv′\| ≈ 107 at the end | MEDIUM–HIGH |
| M5.3 | **Training batches hide instability through resampling** (the framing in the question) | same-trajectory training samples would scatter far more than the monitor | **Against:** same-parameter resampling changes S₁/S₂ by only 4–8 % (E-C). Batch variance is mostly anchor identity (PC-1(b)) | HIGH against |
| M5.4 | **Optimization chaos** amplifies tiny numeric differences | identical-data replicates diverge within ~300 steps | PC-4 (S₁ 0.460 vs 1.296 at step 409) | HIGH |

**Telemetry bearing.**

- F-07: the IC swings are the visible symptom of M5.2/M5.4 hypersensitivity.
- F-09's histogram is a histogram over **anchors**, mostly 10 trajectories (PC-7).
- F-13: the generation-6/7 comparison quantifies M5.4.

**Discriminating experiments.**

- **E4 (read-only).** Score trajectory 28 on K fresh stratified time draws at each
  retained checkpoint. That bounds measurement noise directly; E-C already gives two
  points.
- **E3.**
- **Telemetry for the next run (§4.3):** log the monitor's S_k every step, plus the
  anchor or slot identity.

### 3.6 Source method re-verified (§5.6(d)) — literature

**Provenance.** A read-only sub-agent read the primary sources directly. It used
the arXiv LaTeX source, PDF text for page and equation numbers, publisher metadata,
and the authors' official code at pinned commits. Every statement below carries the
location the notes record (`scratchpad/r4/lit-notes.md`, item IDs in brackets).
Where a statement is the notes' or my paraphrase, it says so.

**The journal version was not accessible.** ScienceDirect returned HTTP 403, and the
OSTI "fulltext" link serves the arXiv v1 PDF. Any change of method in the 2024
journal text is therefore **unverified** [lit-notes §1.4].

#### 3.6.1 Identification

The causal weighting in `pinn_architecture.md` §3.2 is the method of:

- **Sifan Wang, Shyam Sankaran, Paris Perdikaris**, "Respecting causality is all
  you need for training physics-informed neural networks", arXiv:2203.07404 [cs.LG],
  v1 only, 14 March 2022 [LIT; C1.x].
- **Published as** "Respecting causality for training physics-informed neural
  networks", *Computer Methods in Applied Mechanics and Engineering* 421 (2024),
  article 116813, doi:10.1016/j.cma.2024.116813. Metadata verified; full text not
  accessed [LIT].

**Practitioner restatements and the authors' code:**

- Wang, Sankaran, Wang & Perdikaris, "An Expert's Guide to Training
  Physics-informed Neural Networks", arXiv:2308.08468, 2023. No journal version
  found [LIT; E2.x].
- Wang, Li, Chen & Perdikaris, "PirateNets: Physics-informed Deep Learning with
  Residual Adaptive Networks", *JMLR* 25(402):1–51, 2024 [LIT; P3.x].
- The official code bases `PredictiveIntelligenceLab/CausalPINNs` @ `0d1d83f` and
  `PredictiveIntelligenceLab/jaxpi` @ `f944a0c` (main) and `9b5196b` (pirate) [LIT;
  K1.x, J4.x].

**The project's specification cites none of these.** The identification converges
with trainex-r3 JOIN-2 (§3.7.4).

#### 3.6.2 What the method says, in its own terms

**(1) How the causal parameter is set or scheduled.**

- **Definition.** The 2022 paper defines `w_i = exp(−ε Σ_{k=1}^{i−1} L_r(t_k, θ))`,
  where "ε will be referred to as a *causality parameter* that controls the
  steepness of the weights" (§3, Eq. 3.2, p. 6) [C1.7].
- **Scale dependence.** The paper ties the mechanism to residual magnitude:
  "L_r(t_i, θ) will not be minimized unless all previous residuals … decrease to some
  small value such that w_i is large enough" (§3, p. 6) [C1.8].
- **Sensitivity and annealing.** It reports sensitivity and prescribes annealing:
  > "choosing a large ε value can result in a more difficult optimization problem,
  > because the temporal residuals at earlier times have to decrease to a very small
  > value … we employ an annealing strategy for adjusting ε using an increasing
  > sequence of values {ε_i}, which gradually increases the strength with which the
  > PDE residual constraint is enforced" (§3, p. 7) [C1.13]
- **Algorithm 1.**
  - It loops ε over `[10⁻², 10⁻¹, 10⁰, 10¹, 10²]` with at most S steps each.
  - It breaks to the next ε when `min_i w_i > δ`. The recommended values are
    "λ_ic = 10³, δ = 0.99" (Algorithm 1, p. 8) [C1.14–C1.15].
  - The paper's only single-ε run is an illustration with ε = 100 (§3, p. 6) [C1.18].
- **The authors' later practice uses a fixed "causal tolerance".**
  - The Expert's Guide default is `ε = 1.0` (Alg. 1 footer, p. 4) [E2.6], with the
    advice to "choose a moderately large ε to ensure that all temporal weights can
    properly converge to 1 at the end of training. If this is not the case, it would
    be advisable to slightly reduce the value of ε" (§5.1, p. 7) [E2.9].
  - jaxpi configurations use 1.0 mostly, but also 0.1, 5.0 and 10⁻². They pair it
    with 16–32 chunks, fixed budgets and no δ stopping [J4.x, T4.1–T4.2].
- **Residual normalization.**
  - In every source, ε multiplies **raw** mean-squared residual losses [C1.7, E2.3,
    J4.2, K1.6]. No source normalizes residuals by a reference measured at
    initialization (silence 1).
  - The Expert's Guide states that PDE-residual losses "cannot be normalized during
    the pre-processing step" and handles scale through gradient-norm loss weights
    instead (§5.2, p. 7) [E2.11].
  - It assumes non-dimensionalization makes variables O(1) [E2.19–E2.20].

**(2) How training progress is expected to move the weights.**

- On Allen–Cahn the paper reports:
  > "the initial temporal weights are all zero except for t = 0 … Throughout the
  > rest of the training, more temporal weights are activated, and eventually, all
  > of them converge to 1 as the PDE residual loss is properly minimized" (§3, p. 6)
  > [C1.20]
- It proposes `min_i w_i > δ` as "an effective stopping criterion for assessing the
  convergence" that also "yields trained models with superior predictive accuracy"
  (§3, pp. 6–7) [C1.16].
- On the chaotic Lorenz system, training past the criterion gave "slightly lower"
  loss but "less accurate" predictions, which the authors read as over-fitting
  (§5.1, p. 11) [C1.19].
- The Expert's Guide uses `min_t w(t) → 1` as the convergence signal (appendix
  captions) [E2.10]. jaxpi only logs the minimum weight [J4.4].
- **The indicator is the minimum weight reaching ~1. There is no intermediate
  "front".**

**(3) How the optimizer schedule interacts with the weights.**

- **2022 paper, all benchmarks:** "the Adam optimizer with default settings … and
  an exponential learning rate decay with a decay-rate of 0.9 every 5,000 training
  iterations" (§5, p. 11) [C1.24].
  - Caps are **10⁵–3 × 10⁵ iterations per ε stage per time window** (App. C,
    Table 4) [T1.2].
  - Lorenz used 40 windows of Δt = 0.5, a 5 × 512 MLP, a **hard IC**, N_t = 256
    full batch, and reached relative L² errors of about 1 × 10⁻² (App. E; §5.1)
    [C1.30–C1.34].
- **Expert's Guide and jaxpi:** Adam at 10⁻³ with exponential decay 0.9 every
  2,000–5,000 steps; 10⁵–3 × 10⁵ steps [E2.15–E2.16, T2.1, T4.1].
  **PirateNets** adds a 5,000-step linear warm-up [P3.1].
- **No cosine annealing, no L-BFGS hand-off, and no 10³-step budgets** appear in
  any causal-training source (silences 6–7). L-BFGS appears in the related
  literature only in Krishnapriyan et al. [K5.1.4].
- **The interaction itself is not stated** (silence 4). In the authors' Lorenz code
  the Adam state and iteration count carry across ε stages within a window, and each
  window starts from a fresh network [K1.3]. jaxpi re-creates model and optimizer per
  window [J4.9].
- **Implication** [OWN arithmetic on the published schedule]: over a 500-step window
  the published decay changes the learning rate by 0.9^(500/5000) ≈ 0.99. Over
  10⁵ steps it falls about 8× (0.9²⁰ ≈ 0.12). Generation 7's cosine fell about 94×
  inside the window.

#### 3.6.3 Every point where this project departs from the source

| # | Source (in its own terms) | This project | Consequence for Q1–Q5 |
|---|---|---|---|
| L-1 | ε annealed upward over 4 decades, advanced by `min_i w_i > 0.99` (2022) [C1.13–C1.15]; or a fixed tolerance with long budgets (later work) [E2.6, J4.x] | `η_c = 1` fixed; continuation explicitly declined (`54-RULING` A1) | The source's own calibration procedure is absent (as trainex-r3 also found) |
| L-2 | ε multiplies **raw** residual losses; `w_i > 0.99 ⇔ Σ_{k<i} L_r < 0.01005/ε`, an **absolute** tolerance in the problem's units, tightened by annealing [C1.7; OWN algebra] | Residuals divided by a frozen *initialization* reference; `w > 0.5 ⇔ Σ R̄ < 0.693·R_ref ≈ 1.37 × 10¹⁰`. Effective raw ε = 1/R_ref ≈ 5.1 × 10⁻¹¹, 8–9 orders below the smallest published value (10⁻³ in the authors' Lorenz code [K1.1], 10⁻² in the paper) | The front became an initialization-relative statistic. That is Q2's core (§3.2); no published method does this (silence 1) |
| L-3 | Progress indicator: `min_i w_i → 1`; used as a *success* and stopping criterion [C1.16, E2.10] | `front_idx = max{n : w_n > 0.5}` with a 500-step no-advance **failure** guard | No published counterpart (silences 2–3). The closest are δ = 0.99, Penwarden et al.'s δ = 0.95, and their 0.05 null-set rule [PW5.4.3–PW5.4.4] |
| L-4 | Adam with slow exponential decay over 10⁵–3 × 10⁵ steps | Cosine to 0 over 1,000 steps; L-BFGS hand-off designed but unreachable (PC-3) | Q1/Q4: the window/schedule coupling does not arise under published schedules; the budget is two orders below every published causal run |
| L-5 | IC strongly enforced: λ_ic = 100–10⁴ (2022) [C1.38–C1.39], a hard IC for Lorenz [C1.33], or gradient-norm-balanced λ_ic [E2.4, J4.7]. The paper frames fitting the IC *first* as the causal prerequisite [C1.21] | λ_IC = 1 on an un-normalized IC term whose gradient exceeds physics by 10⁴–10⁶, so physics is the passenger (PC-2) | The project inverted the source's balance. The source anchors the sweep at an enforced IC while physics still trains; here only the IC trained |
| L-6 | Single-IC forward problems: one network per problem or window [C1.35, J4.9] | One IC-conditioned network over many trajectories; per-step causal prefix over batch bins; executed on one anchor (PC-1) | No published guidance on aggregating causal weights across trajectories (gap G-9) |
| L-7 | No supervised data term with causal weights (silence 8) | Data Huber on snapshots of 256 trajectories | Unaddressed by the source |
| L-8 | First-order-in-time systems (silence 9) | Second-order ODE (a′ = d²r′/du²) | Unaddressed by the source |
| L-9 | tanh MLP or modified MLP, Glorot init, Fourier features with scale σ ∈ [1, 10] treated as a *tuned* knob [C1.40, E2.21]; sine activations mentioned only as an alternative [E2.18] | SIREN `ω₀ = 30`, 12 layers, `LN(x)²` power-skip | Q3: no causal-training source used this architecture (silence 10) |
| L-10 | Chunks M = 16–32 with tolerance 1.0 in later work (pairing undiscussed, silence 12) | M = 16 | Within range; the residual scale it is paired with is not (L-2) |

#### 3.6.4 Further literature bearing on the diagnosis

- **Gradient imbalance is a documented failure mode** (bears on PC-2 and D1).
  - Wang, Teng & Perdikaris, "Understanding and mitigating gradient flow pathologies
    in physics-informed neural networks", *SIAM J. Sci. Comput.* 43(5):A3055–A3081,
    2021 [LIT].
  - They identify "stiffness in the gradient flow dynamics" leading to "an unstable
    imbalance in the magnitude of the back-propagated gradients", and propose
    adaptive learning-rate annealing of loss weights [W5.2.1].
  - The Expert's Guide's version sets `λ̂_j = Σ_k‖∇L_k‖ / ‖∇L_j‖`, updated every
    f = 1,000 steps with moving average α = 0.9, so that "the norm of gradients of
    each weighted loss is equal to each other" (§5.2, p. 7) [E2.4–E2.6, E2.12].
  - The two papers use opposite moving-average conventions [lit-notes §4.3].
  - F-08 is a textbook instance of the pathology they treat.
- **PINNs on chaotic systems can satisfy physics with the wrong IC** (bears on R2.4
  and D2-A's IC criterion).
  - Steger, Rohrhofer & Geiger, "How PINNs Cheat: Predicting Chaotic Motion of a
    Double Pendulum", NeurIPS 2022 Workshop (DLDE) [LIT; abstract only, SG5.9.1].
  - They report that PINN optimization "consistently converges to physically correct
    solutions that violate the initial condition only marginally, but diverge
    significantly from the desired solution."
- **Deep networks' derivatives are badly conditioned at initialization; PirateNets
  starts the residual branches closed** (bears on Q3 and D6).
  - PirateNets attributes depth degradation to "non-suitable initialization schemes,
    which result in poor trainablity for the network derivatives" (abstract) [P3.4].
  - It initializes its residual gates α = 0 so the network starts as "a linear
    combination of the first layer embeddings" [P3.6]. Setting α = 1 "results in
    complete model collapse for deeper networks" [P3.7].
  - The project's six `LN(x)²` branches are fully active at initialization.
  - This is a literature-grounded candidate mechanism for the stack's derivative
    amplification, not a measurement on this network.
- **SIREN's `ω₀ = 30` was justified for a different setting** (bears on Q3).
  - Sitzmann et al., "Implicit Neural Representations with Periodic Activation
    Functions", NeurIPS 2020 [LIT].
  - They chose `ω₀` "so that the sine function sin(ω₀·W x + b) spans multiple periods
    over [−1, 1]. We found ω₀ = 30 to work well for all the applications in this
    work" (§3.2, p. 5) [S5.6.2], for normalized coordinate inputs [S5.6.3] and 5-layer
    MLPs [S5.6.6].
  - In this network the τ coordinate is one of 14 inputs under a U[−1/14, 1/14]
    bound, so the "multiple periods" rationale applies at only about 30/14 rad per
    unit τ (§3.3) [OWN].
- **The power-enhanced SkipResNet source uses no LayerNorm.**
  - Noorizadegan, Young, Hon & Chen, "Power-enhanced residual network for function
    approximation and physics-informed inverse problems", *Applied Mathematics and
    Computation* 480 (2024) 128910.
  - It uses tanh, `x⁽ˡ⁾ = f(x⁽ˡ⁻¹⁾) + (x⁽ˡ⁻¹⁾)ᵖ` on odd layers [NR5.7.1], and finds
    "a power of 2 is effective for networks with fewer than 30 hidden layers"
    [NR5.7.2].
  - A grep of the arXiv v2 source for LayerNorm or BatchNorm finds nothing
    [NR5.7.6]. This confirms the spec's statement that the LayerNorm is the project's
    own addition (`pinn_architecture.md:211-213`). The LayerNorm scale-invariance
    mechanism of §3.3 is therefore specific to this project and has no published
    characterization.
- **Curriculum and time-marching are the documented complements.**
  - Krishnapriyan, Gholami, Zhe, Kirby & Mahoney, "Characterizing possible failure
    modes in physics-informed neural networks", NeurIPS 2021: curriculum
    regularization that starts with "small coefficients … progressively increased",
    and sequence-to-sequence time marching [K5.1.2–K5.1.3].
  - Penwarden, Jagtap, Zhe, Karniadakis & Kirby, *J. Comput. Phys.* 493 (2023) 112464:
    ε-annealing "requires multiple passes over the entire domain … significantly
    increasing the computational cost and not guaranteeing convergence" [PW5.4.1].
- **Neural three-body context** (not PINNs).
  - Breen, Foley, Boekholt & Portegies Zwart, "Newton versus the machine", *MNRAS*
    494(2):2465–2470, 2020: a supervised 10 × 128 network trained on Brutus data
    performed best restricted to t ≲ 3.9 time units [B5.8.3].
  - Greydanus, Dzamba & Yosinski, "Hamiltonian Neural Networks", NeurIPS 2019: "both
    models struggled to accurately model the dynamics of the three-body problem"
    [H5.10.1].
  - Both suggest the 10-time-unit Stage-0 horizon is hard even with direct
    supervision.

#### 3.6.5 What the literature implies for each question (my reading, labeled [OWN])

| Question | Implication |
|---|---|
| Q1 | Under published practice, a liveness window would sit on an almost constant learning rate (~1 % change per 500 steps). The coupling is an artifact of the project's schedule and budget. The published progress signal is a success criterion (min w > δ), not a no-progress guard |
| Q2 | The published method *is* an absolute-tolerance method: ε sets the cumulative raw-residual target, tightened by annealing. The `R_ref` normalization converted it into a relative one, a departure without precedent. D2-B is the faithful reading; D2-A is the conservative one |
| Q3 | No literature covers SIREN + LayerNorm power-skip + causal weights. The closest guidance (PirateNets) points at fully active deep branches at initialization as the derivative pathology, consistent with M3.3 |
| Q4 | Published causal runs use 10⁵–3 × 10⁵ steps per stage or window. At this project's measured ≈12 s/step, 10⁵ steps ≈ 14 days per seed. A literature-scale budget is a compute decision (or a throughput-engineering one), not a tuning detail |
| Q5 | The literature reports no intermediate-front oscillation, because it monitors only the minimum weight. The over-fitting remark (C1.19) cautions against training long past a success criterion, not against oscillation |

### 3.7 Independent derivation of the H- rows, then comparison (§5.6(e))

Each subsection gives my derivation first, then agreement or disagreement with the
H-row. I wrote §3.7.1–§3.7.3 before reading the sub-agent's trainex-r3 extract;
§3.7.4 records the comparison made afterward.

#### 3.7.1 H-01 — `54-RULING` scientific basis, points 1–5

**Point 1 — flat-profile endpoint arithmetic.**

- **Derivation.** If every R̃_b = 1, the exclusive prefix at bin 15 is 15. Then:
  - w₁₅ = e⁻¹⁵ = 3.059 × 10⁻⁷;
  - the float32 smallest normal is 1.1755 × 10⁻³⁸, so ln = −87.3365;
  - the margin is 87.3365/15 = 5.82.
- **The actual vectors.** GATE-04's stored P₁₅ were 13.5–24.6 (sub-agent file A,
  Table 3b), so the minimum initialization weights were 1.3 × 10⁻⁶ to 2.1 × 10⁻¹¹.
  The training runs' smallest logged weight was 9.84 × 10⁻²³ (step 231 in both
  generations 6 and 7), an exponent of 50.7, against the 87.3 floor.
- **Verdict: agree.** The arithmetic holds; the clip never bound (see also point 5).

**Point 2 — "addresses the established severe physics/data conditioning mismatch".**

- **Derivation.**
  - *Before `B2`.* The 2026-08-17 audit measured a median raw physics/data
    gradient ratio of 6.3 × 10¹² on a v2.2 seed-41 run (sub-agent file A, §E2).
  - *After `B2`.* Raw physics 91–758 against applied data 1.45–5.78, a ratio of
    ~16–520 (F-08). The physics/data mismatch shrank by about 10 orders of
    magnitude.
  - *What the analysis left out.* The IC gradient was 3.8 × 10⁸ at initialization
    on the production path (`production-conformance.json:107-110`) and
    2.8 × 10⁴ – 2.6 × 10⁶ times the physics gradient throughout the run. That
    imbalance was never in the analysis. `B2` moved physics from *dominant* to
    *negligible*, because the term it rescaled was the only one rescaled.
- **Verdict: agree on the physics/data claim; disagree that conditioning was
  addressed.** The binding imbalance was always IC versus the rest (PC-2, PC-10).

**Point 3 — `ω₀` retained.** The ruling said that "even the optimistic fourth-power
estimate says the enumerated reductions are insufficient alone, while the frozen
measured reference removes raw initialization magnitude from the causal calibration."

- **Derivation.**
  - The frozen reference does remove initialization magnitude from the causal
    *exponent* and the *physics loss*. Weights began graded, not floored. Agree.
  - It does not remove it from the IC term, whose value is the first-derivative
    error squared: ‖Δv′‖ ≈ 170 at the start against true speeds ≈ 2.
  - Nor from the IC gradient (3.8 × 10⁸), nor from the IC hypersensitivity (E-G).
    The initialization scale therefore still shapes training (M3.1).
  - On the scaling law: R̄ ∝ ω₀⁴ holds only if the stack's gains do not depend on
    `ω₀`. LayerNorm scale-invariance argues they partly compensate below a crossover
    (§3.3, M3.2b). A fourth-power estimate may therefore *overstate* what lowering
    `ω₀` achieves. That cuts the same way as the ruling's conclusion (retain 30),
    for a different reason.
- **Verdict: agree with retaining `ω₀ = 30` as untested rather than refuted.
  Disagree that the frozen reference neutralizes the initialization scale for
  training.**

**Point 4 — separating 4,096 samples from a 16-term prefix.** The ruling said this
"makes `front_idx` denote a fixed time bin", while "a front from a resampled
training batch remains a stochastic diagnostic."

- **Derivation.** Correct in principle. In the executed code, though, the 4,096
  samples were one trajectory's times (PC-1). The training-batch front's
  stochasticity came mainly from *which trajectory*: 51 % of detrended bin-0 log
  variance, against 4–8 % for time resampling (PC-1(b), E-C).
- **Verdict: agree in principle; the executed instance differs.**

**Point 5 — the clip is a numerical guard.**

- **Derivation.** It never bound (point 1). It did not distort the run.
- **Verdict: agree.**

#### 3.7.2 H-02 — the verdict packet's readings

| Reading | My derivation | Verdict |
|---|---|---|
| "Not a near miss" | S₂ = 1.1891 vs 0.6931 needs −41.7 %; noise at the final learning rate (\|Δlog₁₀ S₂\| ≈ 0.013) cannot close it, and the schedule had ≈ 0 N_eff left | **Agree** for the trip moment. The underlying S₂ was still falling (~2× after step 470; PC-6) |
| "The front oscillates; it does not creep" | The discrete front oscillated (S₁ hovering about ln 2); the prefix sums crept steadily (PC-6) | **Disagree** with "does not creep" |
| "Two independent runs (gens 6 and 7) stalled at the same index" | Identical batches, monitor and initial parameters; parameters bit-identical through ~step 269. Generation 6 never completed a window after its advance at step 353 (PC-4) | **Disagree** (not independent; generation 6 did not stall under invariant B's definition) |
| "Per-bin progress slows: the front reached 1 at step ~93 and 2 at step ~450, then nothing by 951" | Step 93 is the **smoke's** monitor (F-14), not the graded run's; the graded run's first front-1 step is unrecorded. The smoke's front-1 at 93 was itself transient: instantaneous front 0 at steps 100/200/300 (verifier) | **Qualify** (mixes two runs; the 93 figure is a transient) |
| "The window 450→950 coincided with the cosine lr falling ~100×" | 5.78 × 10⁻⁴ → 6.16 × 10⁻⁶ = 94×; window N_eff = 118 of 499.4 (23.6 %) | **Agree**, with the N_eff quantification |
| "A full front means about a 20× residual reduction with the raw residual still about 10⁹" | Mean R̃ < 0.0462 ⇒ 21.6× below R̃ = 1, or 23.9× below the monitor's initial median; raw 9.13 × 10⁸ | **Agree**. Add: that is still 190× the median physical acceleration (Q2) |

#### 3.7.3 H-03 — trainex-r3's source method and scaling-law dispute (my derivation first)

**Source method (JOIN-2).** My identification is the temporal causal weighting of
Wang, Sankaran & Perdikaris: an exclusive cumulative residual sum inside an
exponential, with a causality parameter ε. Exact bibliographic data and the method's
statements on ε scheduling, weight dynamics and optimizer schedule are in §3.6.

**Scaling law (JOIN-3), derived from the code.**

- **Where the amplification sits.** The first layer contributes an angular frequency
  of at most 30/14 per unit τ. Most amplification is built in the stack.
- **How `ω₀` acts.** It is a multiplicative lever whose strength depends on whether
  the stack's gains are invariant to the first layer's output scale. The `LN(x)²`
  skip path argues they are not.
- **Bottom line.** A pure ω₀⁴ law and a "stack-only" law are both unproven. Neither
  can be settled without E5.

#### 3.7.4 Comparison with the trainex-r3 record (written after reading the extract)

Source: sub-agent extract `scratchpad/r4/h03-extract.md`, which cites
`trainex-r3-resolution-doc.md` (RD), the open-book report `research_results/claude-resolution.md`
(OB), the closed-book report `research_results/chatgpt-resolution.md` (CB), and the
Rule-19 verification `2026-09-02-trainex-r3-rule19-claim-verification.md` (V), each
with line numbers.

**JOIN-2 (source method) — convergent.**

- My identification matches both r3 reports: Wang, Sankaran & Perdikaris, *CMAME*
  421 (2024) 116813, preprint arXiv:2203.07404 (2022).
- The vendored PINA implementation in this repository cites the same paper
  (`reference-code/reference_NNs/PINA-master/pina/solver/physics_informed_solver/causal_pinn.py:55-60`,
  per OB:164-170). It defaults `eps = 100` (`:76`).
- r3's Rule-19 pass routed every *published-content* claim (ε annealing, δ = 0.99, the
  Expert's-Guide default, IC weight) as NOT-VERIFIABLE-HERE (V:255-257, :1436). §3.6
  records what this round's literature pass read in the sources themselves.
- The r3 record states no source learning-rate schedule or iteration count. The
  sub-agent's negative search over OB, CB, RD and DN found none (extract §1.5).

**JOIN-3 (scaling law) — my derivation converges with the open-book mechanism; the
dispute stays open on the project's model.**

- OB derived the same LayerNorm scale-invariance argument (OB:65-76). Its clean-room
  re-implementation measured R̄ responding to `ω₀` as about ω₀^0.5: 1.63 decades for
  a 1000× cut, and saturating below ω₀ ≈ 10 (ratios 0.265 / 0.206 / 0.238 at
  ω₀ = 10 / 3 / 1). It put about 1.44 decades per SQR block (OB:78-91).
- Those numbers are on a **re-implementation**, routed NOT-VERIFIABLE-HERE (V:258-259).
- CB kept R̄ ∝ ω₀⁴ explicitly as a conditional heuristic (CB:338-360).
- The owner qualified the invariance as approximate under the finite stabilizer
  (GAP-54-08, `54-GAPS.md:324-328`). My use is consistent with that.
- **What this round adds:**
  - the first-layer bound of ≤ 2.14 per unit τ (RMS 1.22);
  - the observation that training *raised* the first-layer τ-frequency;
  - an estimated saturation onset near ω₀ ≈ 7. OB's clean-room table, read
    independently of mine, shows its knee between 10 and 3.

  None of these settles X-12. Only E5 (= r3's X-2) on the project's model does.

**Predictions against outcome.** The r3 round made several forward statements that
generation 7 now tests:

| r3 statement | Outcome in generation 7 | Reading |
|---|---|---|
| Residual-wide normalization moves physics/data raw-gradient imbalance from 12.8 to ≈ 2.6 decades (OB:709, R-09) | observed physics/data ≈ 1.2–2.7 decades (16–520×) | **Borne out** |
| "The `L_IC` velocity term … is untouched by every option on every menu … A recipe that passes GATE-04 can still be dominated by an IC anchor two decades above the data term" — recorded as G-9, not solved (OB:712-716); "it may leave physics/data/IC imbalance unresolved" (CB:537) | IC exceeded physics by 4.4–6.4 decades and data by ~7–8 decades in gradient norm | **Realized, more severely than stated** |
| "Dividing `R̄` by a constant is observationally equivalent to `λ_phys = 5.9×10⁻¹¹`, and `λ_phys^max = 1` is [LOCKED] … coherence warning" (OB:684) | the physics term's effective weight against IC was 10⁻⁴–10⁻⁶ in gradient norm | **Realized** |
| "Adam's scale invariance may absorb part of the intended rebalancing" (OB G-8) | Adam normalizes the *summed* gradient, so a term that is 10⁻⁶ of the sum stays negligible. The *relative* imbalance survived | **Did not mitigate** — G-8 concerned global rescaling; the binding problem was relative |
| Under a frozen reference, `front_idx` measures progress "against a fixed initialization scale rather than an absolute physical one"; N = 500 "should be re-ratified or explicitly carried over with a reason" (OB:770-774) | 57-RULING re-ratified N = 500 as a "new owner decision" with no stated quantitative rationale; the relative-vs-absolute gap is now quantified (Q2: full front ≈ 190× physical scale) | **Borne out** |
| "Four separate meanings of success … None automatically implies the next" (CB:561) | the front opened without any change in `eps_H` | **Borne out** |
| X-4: a short Stage-0 segment under the composed recipe before locking (OB:899-903) | not run before RUN-04; generation 7 became that segment, graded | — |

**The provenance of PC-2.**

- `54-RULING` point 2 is sourced from OB's physics/data analysis (PC-6, S2b; extract
  §4).
- The same report's IC caveat (G-9) and its λ_phys-equivalence warning (OB:684) are
  not carried into the ruling's scientific basis, which mentions physics/data only.
- The run then failed in the way G-9 anticipated.
- This is no criticism of the ruling's internal logic. It is a gap that travelled
  from a report's gap list into a ruling's omission.

### 3.8 Evidence limits (§5.6(f))

- **One seed and one monitor trajectory.** One graded seed exists (F-17). The smoke,
  generation 6 and generation 7 share **the same batch and anchor sequence and the
  same monitor trajectory** (PC-4). Every observation of the monitor is one trajectory
  (28) observed through three numerically different optimizations. Nothing here
  generalizes across seeds, trajectories or monitors.
- **Chaotic training dynamics.** Under identical data order, float32
  nondeterminism produces 3× differences in a trajectory's S₁ within ~140 steps of
  divergence. Single-run event timings, such as "the front advanced at step 450", are
  **not estimable quantities**. Only population and trend statistics are.
- **Natural-experiment sample sizes.** n = 57 (generation 7) and 32 (generation 6).
  The IC effect (65–69 % decreases) is distinguishable from 50 %. The physics null
  (41–42 %) bounds any *large* direct effect. It cannot exclude a small consistent
  physics effect hidden under per-step noise.
- **Coverage of the training-batch telemetry.** It covers only the 40 trajectories
  that served as anchors. There is **no measurement of generalization to
  never-anchored training trajectories** except through the validation gate's
  conservation metric (`eps_H`), which is not trajectory error.
- **Monitor sampling.** The frozen monitor was scored only at 5 generation-7 and 3
  generation-6 checkpoints. Trajectory 28's 31 training-batch samples are a proxy
  trace with 4–8 % resampling noise (E-C), not the monitor itself.
- **Gradient decomposition.** Per-term gradients exist on a 50-step cadence only, as
  global norms (F-08). No preconditioned, per-parameter or per-bin decomposition
  exists. The "physics untrained" conclusion rests on F-08 plus Adam's algebra plus
  E-D, not on a direct measurement of the update's composition (E2 would supply it).
- **Physical-scale figures.** These come from Brutus positions and masses of the
  1,812 Stage-0 training trajectories via the analytic Newtonian acceleration.
  Close-encounter tails (max ‖a′‖ 2.9 × 10⁴) are not representative; medians and p99
  are used.

### 3.9 Discriminating experiments (owner-gated proposals; none performed)

| ID | Measures | Outcomes and meaning | Cost | Needs a training run? |
|---|---|---|---|---|
| E2 | At checkpoints 0, 900 and 951, on the frozen monitor batch and on a conformant multi-slot batch: per-term gradients g_IC, g_phys, g_data; the cosine between them; and the share of the Adam-preconditioned update (from the stored moments) along −g_phys | share ≲ 10⁻⁴ ⇒ confirms PC-2 (physics passenger). share ≳ 10⁻² ⇒ PC-2 overstated; revisit M1.3 and M4.1 | minutes (forward and backward on retained checkpoints; MPS or CPU) | No — read-only |
| E3 | S_k profile and IC error, at checkpoints 0 and 951, for (a) high-exposure anchors, (b) never-anchored training trajectories, (c) validation trajectories | (b),(c) ≈ (a) ⇒ improvement is global (amplitude shedding). (b),(c) ≪ (a) ⇒ exposure-specific fitting; front = a training-exposure metric | ~45 s per trajectory-checkpoint (replay timing); about 1 h for 40 trajectory-checkpoints | No — read-only |
| E4 | Trajectory 28's S_k under K = 20 fresh stratified time draws at each retained checkpoint | measurement noise of the monitor estimator; separates estimator noise from parameter motion | ~15 min | No — read-only |
| E5 | **Initialization decomposition.** ‖v′‖, ‖a′‖, bin-mean R̄, per-term gradient norms at init on the six GATE-04 cases for ω₀ ∈ {1, 5, 10, 30} × power branch {on, off} × LayerNorm {on, off} (and depth {4, 8, 12}) | apportions the derivative scale (Q3). If the power branch dominates, the ω₀ question is moot | minutes; **needs a code path `ArchitectureSpec` currently rejects** (G-3) | No training; initialization-only computation |
| E6 | λ_phys = 0 control (IC + data only) on the same seed and batch sequence for ~500 steps | monitor trajectory and population S_k ≈ generation 7 ⇒ the causal physics term was irrelevant (confirms PC-2 causally) | ~1.7 h at ≈12 s/step | Yes (diagnostic, not graded) |
| E7 | Constant lr (5.8 × 10⁻⁴) vs the executed cosine on the same batch sequence, ≥ 2 numeric replicates each | separates M1.1 from M1.2; quantifies record-timing variance | ~3.3 h per 1000-step replicate | Yes |
| E8 | **Calibration pilot** under the corrected recipe (D0 + D1 + D3), invariant B observe-only, per-step monitor trace | N_eff per bin advance ⇒ budget (Q4); whether the front measures physics once physics is trained | n_steps × ≈12 s (mean 12.07 s/step in gen 7; 10⁴ steps ≈ 1.4 days) | Yes |
| E9 | Monitor batch at retained checkpoints with residuals divided by each slot's true ‖a′‖² scale (physical normalization) | where an "absolute" front would sit; with E3, links relative and absolute | minutes | No — read-only |

**Ordering for an owner who authorizes any.** E2 → E4 → E3 → E9 are read-only and
cheap, and could falsify PC-2 or the M1.2 reading before any run. E5 needs a narrow
code path. E6–E8 are runs.

---

## 4. Part 3 — Options (suggested defaults marked; the owner rules)

**Conventions.** Door classifications follow ERW Rule 7:

- **Two-way door** — committing is cheaply reversible. Revert the code or config,
  and no locked contract or evidence chain is consumed.
- **One-way door** — committing changes a locked contract, consumes a non-renewable
  resource (the held-out evaluation, a baseline's comparability), or sets a precedent
  that later rulings inherit.

Several options below are two-way in code but **require a formal amendment** of a
locked contract (SCOPE-38 discipline). That is flagged separately as "amendment".
Every default is a **suggestion**. Each option names the diagnostic outcome it
presupposes.

### D0 — Conformance of the executed loss and monitor (PC-1)

| Option | What it does | Presupposes | Mechanical trade-offs | Door |
|---|---|---|---|---|
| **D0-A — SUGGESTED DEFAULT** | Evaluate every collocation row on **its own slot's** `IC13` and masses (the batch already carries them, `batches.py:488-507`). Aggregate the IC term over all selected slots (the aggregation rule is gap G-1). Score the monitor over its 256 frozen identities. Make validation conformant (no `collocation_count=1`, no fixed anchor). Upgrade the conformance verifier to an identity-dependent assertion: perturbing a non-anchor slot's `IC13` must change the physics loss. Then re-measure `R_ref` with the conformant estimator and re-run GATE-04 | PC-1 (verified by code, exact RNG replay and the checkpoint-only monitor recomputation) | Same row count, so per-step cost roughly unchanged. The IC term needs 256 first derivatives at u = 0 (cheap). Physics and monitor estimates average 256 trajectories per bin, so variance falls and the front becomes a population statistic. `R_ref` changes value | **Two-way** in code. **Implements** the ratified contract as the project read it, so no amendment. **One-way** for evidence: generations 6 and 7 stop being comparable baselines |
| D0-B | Keep one trajectory per step but remove the bias: a uniformly random or round-robin anchor; monitor scores K fixed trajectories | that single-trajectory SGD on physics/IC is acceptable, and only the bias is the defect | Cheapest change. Physics gradient stays a 1-trajectory estimate per step; IC hypersensitivity is still felt one trajectory at a time | Two-way in code; **amendment** (anchor semantics would have to be ratified) |
| D0-C | Ratify the executed semantics as-is (lowest-ID anchor) | that PC-1 is a reading choice, not a defect | No code change. Training stays concentrated on ~10–40 trajectories; the monitor stays one trajectory | **One-way** in practice: canonizes a biased estimator for every later run |

**Cross-decision interactions.**

- D0 resets `R_ref` (D2) and the monitor (D3).
- It changes the IC gradient's variance but not its magnitude problem (D1).
- It invalidates any budget extrapolated from generation 7 (D5).

### D1 — Gradient balance among the IC, physics and data terms (PC-2)

| Option | What it does | Presupposes | Trade-offs | Door |
|---|---|---|---|---|
| **D1-A — SUGGESTED DEFAULT (branch on E2)** | Adaptive `λ_IC` set so ‖λ_IC∇L_IC‖ ≈ ‖∇L_phys‖. Use an EMA of gradient norms on a fixed cadence (the gradient-norm balancing of Wang, Teng & Perdikaris 2021 and the 2023 expert's guide, §3.6). Keep `λ_phys^max = 1` and `λ_data = 1` **unchanged**: they are locked or fixed (`pinn_architecture.md:699-701`; `loss_catalog.py:169-173`) | PC-2: physics share of the update ≲ 10⁻⁴ (E2 confirms) | Directly targets the measured 10⁴–10⁶ imbalance. Adds one state variable and a cadence. The weight will sit 3–5 orders below the [0.1, 10] ablation range, so IC enforcement weakens and D2-A's IC criterion becomes essential | Two-way in code; **amendment** (Phase 35 "automatic dominance reweighting is deferred until measured … gradient evidence exists" — F-08 is that evidence; `λ_IC` advisory range) |
| D1-B | Frozen initialization-reference normalization of the IC term (`IC_ref`, mirroring `B2`) | that loss-*value* parity is enough | Deterministic and simple. Equalizes values, not gradients. At initialization it would leave IC still ~50× physics in gradient (3.8 × 10⁸/4 × 10⁴ ≈ 10⁴ vs 215) [OWN estimate] | Two-way; **amendment** (L_IC definition) |
| D1-C | Hard IC constraint by an output ansatz (e.g. r′(u) = r′₀ + u·v′₀ + u²·N(u, IC)), removing L_IC | that IC dominance *and* IC hypersensitivity must both go | Removes the term and its 2×-per-recurrence volatility. Changes the output-head contract (COM projection) and the derivative structure; `R_ref` and GATE-04 must be redone; larger code change | **One-way** (architecture or output contract amendment) |
| D1-D | Change nothing in weighting | E2 shows physics share ≳ 10⁻² (PC-2 overstated) | No amendment; relies on D0 averaging | Two-way |

**Branch.**

- **E2 confirms PC-2** (expected given F-08, E-D and the initialization record): take
  D1-A. Keep D1-C as the deviation if E8 still shows IC hypersensitivity dominating
  after rebalancing.
- **E2 refutes PC-2:** take D1-D.

**Interactions.**

- With physics active, a front can advance with the IC unmet (R2.4), so D1-A needs
  D2-A's IC criterion.
- D1 interacts with D6: a lower initialization derivative scale shrinks the required
  rebalancing.
- D1 interacts with D4: the EMA cadence must be shorter than the learning-rate
  timescale.

### D2 — The front criterion (Q2)

| Option | What it does | Presupposes | Trade-offs | Door |
|---|---|---|---|---|
| **D2-A — SUGGESTED DEFAULT** | Two signals. (i) Keep the `R_ref`-relative front for **pacing and liveness only**, measured robustly (D3). (ii) Gate stage **success** on absolute criteria: physics residual normalized by a physical acceleration scale below a tolerance; IC error; and the existing energy gate (`eps_H`) | R2.1 and R2.2: the relative front is uninformative about physics; relative progress did not move `eps_H` | Keeps the ratified relative front intact. Needs a physical scale definition (G-7) and tolerances; ADVANCE thresholds are already "provisional pending Stage-0 pilot calibration" (`ctl_instruction.md`, specs bundle) | Two-way; owner calibration of provisional thresholds (no locked value moves) |
| D2-B | Re-base the causal normalization itself to a physical scale and treat `η_c` as an accuracy tolerance, with literature-style continuation (loose → strict) | that the causal weights should *be* the accuracy schedule, as in the published method (§3.6) | Aligns with the source method. Discards the `R_ref` construction; reopens `A1` ("do not add coefficient continuation") and `B2` | **One-way** (amends `A1`/`B2`; new gate design) |
| D2-C | Keep the relative front for both pacing and success | that relative progress tracks absolute accuracy | No change. Contradicted by PC-5 and R2.1 | Two-way, but presupposes a refuted reading |

**Interactions.** D2-B couples to D1, since physics-loss normalization sets balance.
D2-A's IC criterion is the safeguard D1-A requires.

### D3 — Invariant B, the liveness guard (Q1, Q5)

| Option | What it does | Presupposes | Trade-offs | Door |
|---|---|---|---|---|
| D3-A | A **continuous, smoothed** statistic on the multi-slot frozen monitor (after D0-A). Example: the least-squares slope of ln S_k for the next-to-advance prefix over the window must be negative beyond a noise band measured by E4. Window in **N_eff** (cumulative-lr) units. Guard suspended during warm-up and the annealing tail. Per-step monitor trace logged | M1.2/M5.1 (HIGH): the high-water record of a noisy single-trajectory threshold crossing is the flaw | Robust to transients and to lr-scaled noise; measures trend. Needs a noise band (E4/E8) and a slope threshold — new parameters | Two-way in code; **re-ratification** of 57-RULING checkpoint ③ semantics |
| D3-B | Minimal change: keep the high-water semantics, evaluate on the multi-slot monitor (D0-A), express N in N_eff units | that a population monitor removes enough noise for a record statistic | Smallest change. Records are still upward-biased by noise at high lr | Two-way; **re-ratification** of N's unit |
| **D3-C — SUGGESTED DEFAULT for the next run only** | Invariant B **observe-only** (log, no HALT) for the calibration pilot E8; choose D3-A or D3-B afterwards from its traces | that the next run is diagnostic, not graded | Prevents a guard verdict before the statistic is calibrated. Needs an owner decision that the pilot spends no graded slot and no evaluation | Two-way |
| D3-D | Keep as executed (500 raw steps; single-trajectory high-water) | M1.1 dominant and the statistic sound | Contradicted by the evidence | Two-way; presupposes refuted readings |

**Branch.** After E8:

- E8's traces show the population monitor's ln S_k trend is smooth relative to its
  noise: D3-B suffices.
- Otherwise: D3-A.

**Interactions.** D3 depends on D0 (monitor composition) and D4 (what an N_eff window
spans).

### D4 — Learning-rate schedule and optimizer-phase structure (Q1, Q4)

| Option | What it does | Presupposes | Trade-offs | Door |
|---|---|---|---|---|
| **D4-A — SUGGESTED DEFAULT** | Keep the spec's cosine annealing over the Adam phase. Set its length from E8 (`T_max = n_adam`, calibrated). Make L-BFGS reachable (`max_epochs > n_adam`). Feed the plateau detector a smoothed physics statistic, or the population monitor after D0-A, not the per-step single-anchor loss | PC-3; that within-spec choices suffice once D0/D1/D3 fix the larger issues | Stays inside the spec text ("decay the learning rate over the phase"; `n_adam` and `max_epochs` provisional). Needs the calibration pilot. Plateau smoothing is a code change to a CTX-46 detail | Two-way (provisional values; a code fix) |
| D4-B | Constant learning rate (or warm-up then constant) for the guarded exploration phase; anneal only in a final segment outside the liveness window; then L-BFGS | M1.1 matters more than the evidence shows | Removes the window/schedule coupling by construction. Departs from "cosine … over the phase"; loses annealing's noise reduction during exploration — E-G shows low lr made progress *more* efficient per unit lr | Two-way in code; **amendment** (schedule text) |
| D4-C | Literature-style slow exponential decay over a long budget (§3.6) | that the source method's schedule should be adopted wholesale | Matches published practice. Budget-heavy at ≈12 s/step | Two-way in code; **amendment** |

**Interactions.** D4 couples to D3 (window units), D5 (budget) and D1 (the EMA
cadence relative to lr changes).

### D5 — The Stage-0 step budget (Q4)

| Option | What it does | Presupposes | Trade-offs | Door |
|---|---|---|---|---|
| **D5-A — SUGGESTED DEFAULT** | Run calibration pilot E8 under D0 + D1 + D3-C, preferably ≥ 2 seeds (same-seed replicates share batches, PC-4). Set `n_adam` to a stated multiple of the measured N_eff per full front crossing | M4.1/M4.2: no defensible budget exists before the recipe trains physics | Costs a pilot (10⁴ steps ≈ 1.4 days per seed). Yields a measured number | Two-way (diagnostic run, no evaluation spent) |
| D5-B | Adopt a literature-scale budget a priori (≈10⁵ steps; the causal-training sources use 10⁵–3 × 10⁵) | that published budgets transfer to this problem and hardware | No pilot. ≈14 days per seed per attempt at ≈12 s/step, with no evidence the front crosses | Two-way in principle; costly in practice |
| D5-C | Keep 1000 steps | that 1000 steps suffice under the corrected recipe | Cheap. No evidence supports it | Two-way |

### D6 — SIREN `first_omega_0` and the power-skip stack (Q3)

| Option | What it does | Presupposes | Trade-offs | Door |
|---|---|---|---|---|
| **D6-A — SUGGESTED DEFAULT** | Authorize E5, an initialization-only decomposition with no training, through a **verification-only** path that admits non-default `ArchitectureSpec` values. Keep `ω₀ = 30` and the stack for the calibration pilot unless E5 shows one factor dominating *and* cheaply removable | M3.2b UNDETERMINED / M3.3 MEDIUM: both the lever strength and the shares are unknown | Minutes of compute. A narrow code path outside production; no amendment for measurement | Two-way |
| D6-B | Fresh-initialization ablation removing or altering the `LN(x)²` branch (stage-boundary ablation, per contract) | M3.3 holds | Likely the larger lever on derivative scale if M3.3 holds. Needs amendment, new `R_ref`, GATE-04 | **One-way** (architecture contract; new baselines) |
| D6-D | Gate the six `LN(x)²` branches with trainable scalars initialized at **0**, so the network starts shallow (the PirateNets α = 0 practice; *JMLR* 2024, P3.6–P3.7) | M3.3 holds (the active skip branches carry the amplification) | Literature-grounded for depth pathologies, but on a different architecture (no LayerNorm, no power term); removes the initial amplification while keeping depth capacity | **One-way** (architecture contract; `R_ref`) |
| D6-C | Fresh-initialization ablation lowering `first_omega_0` | M3.2b holds | Effect size undetermined: R̄ ∝ ω₀⁴ if the stack's gains were unchanged; LayerNorm scale-invariance argues for a sub-quartic, saturating response below ω₀ ≈ 7. Also weakens SIREN's spectral-bias rationale (`pinn_architecture.md:180-186`) | **One-way** (`ω₀` contract, `R_ref`) |

### D7 — Telemetry and verification gates required before the next run

| Option | What it does | Door |
|---|---|---|
| **D7-A — SUGGESTED DEFAULT** | Require before any run: per-step slot or anchor identity in the step log; per-step monitor S_k trace; per-term gradient norms plus Adam-preconditioned shares on a cadence; the identity-dependent conformance assertion (D0-A); the `train.log` hand-off message fix (F-05 note); the spec cross-reference fix at `pinn_architecture.md:452` | Two-way |
| D7-B | Require only the conformance assertion and slot logging | Two-way |

### D8 — Which read-only experiments to authorize first

| Option | What it does | Door |
|---|---|---|
| **D8-A — SUGGESTED DEFAULT** | Authorize E2, E4, E3 and E9 (read-only; minutes to ~1 h total) before any code change. Each can falsify a load-bearing reading here: PC-2, M1.2, M1.4 and R2.1 | Two-way |
| D8-B | Skip to D0-A and E8 | Two-way, but forgoes cheap falsification |
| D8-C | Also authorize E6 and E7 (diagnostic runs on the *current* code, ~1.7–7 h) | Two-way; spends compute on a nonconformant recipe |

### 4.1 Decision sheet

| Decision | Options | Suggested default | Door type | Presupposed diagnosis | Owner's pick |
|---|---|---|---|---|---|
| D0 Conformance of loss/monitor | A per-slot fix + `R_ref`/GATE-04 redo · B random/round-robin anchor · C ratify as-is | **D0-A** | two-way code / one-way evidence; no amendment | PC-1 (verified) | |
| D1 Gradient balance | A adaptive `λ_IC` (grad-norm) · B frozen `IC_ref` · C hard IC ansatz · D none | **D1-A**, branch on E2 (→ D1-D if E2 refutes PC-2; D1-C if hypersensitivity persists) | two-way code + amendment (A, B); one-way (C) | PC-2 | |
| D2 Front criterion | A relative pacing + absolute success · B physical normalization + `η_c` continuation · C relative for both | **D2-A** | two-way (provisional thresholds) | R2.1, R2.2 | |
| D3 Invariant B | A smoothed multi-slot trend in N_eff · B high-water on multi-slot in N_eff · C observe-only pilot · D as executed | **D3-C** for the pilot, then A or B by E8 | two-way + re-ratification (A, B) | M1.2/M5.1 | |
| D4 Schedule and phases | A cosine with calibrated `T_max`, reachable L-BFGS, smoothed plateau input · B constant then anneal · C slow exponential | **D4-A** | two-way (provisional values) | PC-3, M1.1 partial | |
| D5 Budget | A calibration pilot (≥ 2 seeds) · B literature-scale a priori · C keep 1000 | **D5-A** | two-way | M4.1, M4.2 | |
| D6 `ω₀` and power-skip | A E5 decomposition first · B power-branch ablation · C lower `ω₀` · D zero-initialized branch gates | **D6-A** | two-way (A); one-way (B, C, D) | M3.2b undetermined / M3.3 MEDIUM | |
| D7 Telemetry/verification gates | A full set · B minimal | **D7-A** | two-way | PC-1, M5.x | |
| D8 First experiments | A E2/E4/E3/E9 · B skip to fixes · C add E6/E7 | **D8-A** | two-way | PC-2, M1.2, M1.4, R2.1 falsifiable | |

### 4.2 Composed next-run recipe (cross-menu coherence check)

The suggested defaults assemble into one sequence. Every step is owner-gated.

1. **Read-only experiments first (D8-A).** Run E2, E4, E3 and E9 on retained
   checkpoints. Branch:
   - E2 refutes PC-2: replace D1-A with D1-D below.
   - E3 shows exposure-specific fitting: D0-A becomes more urgent; nothing else
     changes.
2. **Conformance (D0-A + D7-A).**
   - Implement per-slot physics, IC, monitor and validation evaluation, with the
     identity-dependent verifier assertion and the telemetry additions.
   - Re-measure `R_ref` under the conformant estimator. Whether the six probe cases
     should use dataset ICs rather than synthetic zero-`IC13` is gap G-8.
   - Re-run GATE-04. No locked value changes.
3. **Balance (D1-A).**
   - Adaptive `λ_IC` from a gradient-norm EMA on a fixed cadence.
   - Leave `λ_phys^max = 1`, `λ_data = 1` and `λ_E = λ_L = 0` at Stage 0 (the locked
     PHYS-05 table).
   - Amendment required for the `λ_IC` range and the Phase-35 deferral.
4. **Success gate (D2-A).**
   - Stage success on absolute criteria: a physically normalized residual tolerance,
     IC error, and `eps_H`.
   - The relative front is kept as a pacing signal.
5. **Schedule (D4-A).**
   - Cosine over a calibrated `n_adam` and a reachable L-BFGS phase
     (`max_epochs > n_adam`).
   - The plateau detector reads a smoothed population statistic.
6. **Guard (D3-C).** Invariant B observe-only for the pilot.
7. **Architecture (D6-A).** Unchanged (`ω₀ = 30`, stack). E5 runs in parallel and
   informs a later ablation decision.
8. **Calibration pilot (D5-A = E8).**
   - At least 2 seeds, per-step monitor traces and N_eff accounting.
   - The output sets `n_adam`, the D3 statistic and its noise band, and whether
     D1-C is needed.

**Coherence checks.**

- **Step order is forced.** Step 2 precedes everything because `R_ref`, the monitor
  and the IC term's meaning depend on it.
- **Steps 3 and 4 are a pair.** Rebalancing without an IC criterion can let the
  front certify a wrong-IC solution.
- **Steps 5 and 6 are coherent only together.** The guard must not read a window that
  the schedule starves.
- **Step 8 is the only source of a budget or guard parameter.**
- **Amendment surface.** No locked value moves. The amendments needed are:
  - the `λ_IC` range (advisory, but outside its stated ablation range);
  - the Phase-35 deferral of automatic dominance reweighting;
  - later, the invariant-B re-ratification.

  Every other change is a conformance fix or a provisional-value calibration.

### 4.3 What the runbook inherits

- **One seed is one batch sequence.** Batch selection consumes the RNG
  independently of the model. Same-seed replicates share batches and anchors and
  differ only by float nondeterminism (PC-4).
  - Independent replicates need different seeds.
  - Timing statistics need replicates: identical-data runs diverge 3× within ~140
    steps.
- **A reconstruction is always possible.** The per-step training identity can be
  rebuilt exactly from `splits.json`, snapshot counts and the seed, and validated
  against checkpoint RNG states (`anchors.py`). Log it directly from the next run.
- **The monitor can be scored from checkpoint contents alone.** The sub-agent's
  `monitor_recompute.py` pattern needs no data source. Use it for E2, E4 and E9.
- **Cost.** ≈12 s/step on MPS float32 at 4,096 rows and a 256-row microbatch.
  10⁴ steps ≈ 1.4 days.
- **Configuration traps.**
  - `max_epochs == n_adam` silently removes L-BFGS.
  - The plateau detector cannot fire on a per-step single-trajectory loss.
  - `train.log` misreports a budget-exhausted hand-off after a guard HALT.
- **Code paths that do not match their names or claims.**
  - `_build_anchor_context` consumes times only.
  - The verifier's `anchor_only: False` is a literal.
  - Validation uses `collocation_count=1` on fixed trajectory 12.
- **Invalidation discipline.** Any change in D0, D6 or the count/slot semantics
  invalidates `R_ref` and GATE-04. The current `R_ref` came from six single-trajectory
  probes, five of them with synthetic zero `IC13`.
- **Spec hygiene.**
  - `pinn_architecture.md:452` cites "the fixed-monitor boundary above", which does
    not exist in that file.
  - "Epoch" is undefined for replay batching; the code uses steps (G-6).
- **Standing boundaries carried forward.** No run before an owner ruling. The single
  held-out evaluation stays unspent. Stage-1+ and PLAT-01..07 stay blocked. No
  locked value moves without re-ratification.

---

## 5. Part 4 — Gaps (ERW Rule 9)

Each entry states what is silent or ambiguous, which sources were consulted, why it
matters, and what would resolve it. None is resolved here.

| ID | Gap | Consulted (and why silent) | Matters for | Would resolve it |
|---|---|---|---|---|
| G-1 | **How the IC term aggregates over a batch.** The spec defines `L_IC` for one trajectory; a per-slot implementation (D0-A) needs a rule: mean over slots, over unique identities, or weighted by replacement multiplicity | `pinn_architecture.md` §3.3 and §4.1 (specs bundle) define the term, not its batch reduction. `ctl_instruction.md` Phase 2 assembles terms without reductions. `57-02-SUMMARY.md:122` "preserved existing IC … behavior" records a choice, not a rule | D0, D1 | Owner ruling (semantic) |
| G-2 | **What Phase-56 Block 4 requires: per-slot *evaluation* of physics rows, or per-slot *time allocation* only** ("This re-ratifies the time allocation only") | `pinn_architecture.md:456` (allocation wording); `57-RESEARCH.md:138, :188` and `57-02-PLAN.md:23, :84` (the project's own per-slot reading). The verifier marks it an owner question | D0, every reading of generation 7 | Owner statement of semantics; PC-1 is CONTRADICTED under the project's documented reading |
| G-3 | **No `ω₀`/power-skip/depth decomposition on the project's model.** `ArchitectureSpec` refuses non-default values (`pinn/architecture_spec.py:71-130`); no `R_ref` exists for any alternative | sub-agent file A §0, §5; trainex-r3 OB clean-room numbers are routed NOT-VERIFIABLE-HERE (V:258-259) | Q3, D6 | E5 through an owner-authorized verification-only path |
| G-4 | **Origin of the 0.5 front threshold (prefix ln 2) and N = 500** | F-10 [PKG]; specs silent; literature has no counterpart (§3.6.3 L-3) | Q1, Q2, D3 | Owner rationale, or redesign (D3) |
| G-5 | **Missing measurements:** no per-step monitor trace; no generalization measurement for never-anchored trajectories; per-term gradients only as global norms every 50 steps; no Adam-preconditioned decomposition | master §7 [PKG]; run records | Q1, Q5, PC-2's strength | E2, E3, E4; D7-A telemetry |
| G-6 | **"Epoch" undefined for replay batching.** The code uses optimizer steps for `max_epochs`, the plateau window and validation cadence | `ctl_instruction.md` (bundle) uses "epoch" throughout without defining it for replay batches | Q4, D4/D5 | Owner definition |
| G-7 | **The physical normalization for an absolute success criterion** (per-slot ‖a′‖ scale, dataset scale, or a non-dimensional tolerance) | specs silent; the literature assumes O(1) non-dimensionalized residuals [E2.19–E2.20], which this residual is not at initialization | Q2, D2 | Owner choice informed by E9 |
| G-8 | **Probe-case realism for a conformant `R_ref`.** Five of six GATE-04 cases use synthetic zero `IC13` and masses (1,1,1) | `pinn_architecture.md:454` fixes "the fixed six-case GATE-04 probe" but not its relation to training ICs | D0-A step 2 | Owner ruling |
| G-9 | **Causal weighting across many trajectories per batch** (IC-conditioned networks): one batch-global prefix over batch-mean bins, or per-trajectory prefixes | every causal-training source is single-IC (§3.6.3 L-6) | D0, D2 | Owner ruling; possibly a research question |
| G-10 | **The source of float32/MPS nondeterminism is not isolated** | F-13 verifier note; run summaries | evidence design (replicates) | Engineering investigation |
| G-11 | **Whether external agents reading training/validation data files counts as permitted read-only analysis** | prompt and master §9 name logs and checkpoints only | procedure | Owner ruling (disclosed in §0) |
| G-12 | **No direct measurement of the IC term's hypersensitivity** (Jacobian of `v′(0)` with respect to parameters) | — | D1-C vs D1-A | E2 |
| G-13 | **The 2024 journal text of the source method was not accessed.** The authors' Lorenz code differs from the printed settings (σ, T, ε list, iteration caps) [lit O2] | publisher access denied | §3.6 completeness | Library access to *CMAME* 421, 116813 |
| G-14 | **Literature silence:** second-order-in-time systems, supervised data plus causal weights, causal weights with SIREN/LayerNorm stacks, and how the lr schedule should interact with the weights | lit-notes silences 4, 8–10 | Q1–Q4 | None available; empirical calibration (E8) |
| G-15 | **The invariant-B monitor contract lives only in 57-RULING.** The spec's cross-reference "fixed-monitor boundary above" (`pinn_architecture.md:452`) points at nothing in that file | verifier F-10 | D3 | Spec hygiene by owner amendment |

---

## 6. Part 5 — Claims-and-uncertainty register

Labels:

- **PKG** — package-derived;
- **REPO** — repository-verified this session, with `file:line`;
- **LIT** — literature (author, title, venue, year; item IDs refer to
  `lit-notes.md`);
- **OWN** — my own analysis (script names refer to Appendix A).

Confidence is about the claim as stated.

| ID | Claim | Label and citation | Confidence | Changes it |
|---|---|---|---|---|
| C-01 | The physics residual and IC term are computed on one anchor trajectory per step | REPO `pinn/training/controllers.py:1075-1079`, `:1081-1143`, `:1746-1770`, `:1857-1864` | HIGH | — |
| C-02 | Per-row collocation `tau_ic13`/`masses` are never consumed by any loss | REPO `controllers.py:320-334`, `:409-410`, `:1128` | HIGH | — |
| C-03 | The anchor is the lowest-ID of the step's 240 replay draws | REPO `pinn/data/batches.py:76-78`; `controllers.py:1079` | HIGH | — |
| C-04 | Anchor law over N₀ = 1,812: P(rank 1) = 13.25 %; mean rank 7.5; effective count 14.1 | OWN `pool.py`; REPO `runs/stage0-v23g7-seed42/splits.json` | HIGH | — |
| C-05 | The per-step anchor sequence is reconstructed exactly (RNG state equal to 7 checkpoints) | OWN `anchors.py` | HIGH | — |
| C-06 | 40 distinct anchors; 74.7 % of steps on the 10 lowest-ID trajectories | OWN `anal5.py` | HIGH | — |
| C-07 | The monitor scores trajectory 28 only; 31 direct anchor steps (listed in PC-1) | OWN `anchors.py`; verifier monitor recomputation | HIGH | — |
| C-08 | Validation physics/IC: `collocation_count=1`, fixed anchor 12 | REPO `controllers.py:1384-1385`; OWN | HIGH | — |
| C-09 | Phase-57 records required per-slot evaluation | REPO `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RESEARCH.md:70`, `:138`, `:188`; `57-02-PLAN.md:23`, `:84` | HIGH | owner ruling on G-2 |
| C-10 | The verifier's anchor check passes by construction | REPO `pinn/verification/phase57_production_conformance.py:408-415`, `:533` | HIGH | — |
| C-11 | Time-resampling noise on S₁/S₂ at equal parameters is ~4–8 % | OWN `anal1.py` (steps 901, 943) | MEDIUM–HIGH (two comparisons) | E4 |
| C-12 | Anchor identity explains 51/28/21 % of detrended log R̃ variance (bins 0/1/2) | OWN `anal1.py` | MEDIUM | — |
| C-13 | Applied IC/physics gradient ratio 2.78 × 10⁴ – 2.62 × 10⁶ | PKG F-08; re-derived by verifier | HIGH | — |
| C-14 | At initialization: raw IC gradient 3.80 × 10⁸, physics 215, data 60.3 | REPO `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/production-conformance.json:107-110` | HIGH | — |
| C-15 | Adam \|m̂\|/√v̂ median 0.039 at step 951; gradient clip never bound | OWN `ckpt.py` | HIGH | — |
| C-16 | One direct update lowers the anchor's IC loss in 65–69 % of cases and its physics loss in 41–42 % | OWN `anal3.py` (n = 57 and 32) | MEDIUM–HIGH | E2, E6 |
| C-17 | **The physics term was effectively untrained** (PC-2) | OWN from C-13 to C-16, C-18, C-19 + Adam algebra | HIGH (that its share was negligible) | E2 showing share ≳ 10⁻² |
| C-18 | Output-layer norm ×0.668; per-bin population medians fell 2.3–5.6× in every bin | OWN `norms.py`, `anal4.py` | HIGH (descriptive); MEDIUM as *the* channel | E2/E3 |
| C-19 | Validation `eps_H` median 0.983–0.990 at steps 100–900, flat | REPO `runs/stage0-v23g7-seed42/validation_gate/step-00000{100…900}.json`; `pinn/verification/gate_metrics.py:180-200` | HIGH | — |
| C-20 | L-BFGS unreachable: zero budget at exhaustion; plateau longest run 6 of 50 | REPO `controllers.py:2690-2707`, `:518-562`, `:134-135`; OWN `plateau.py`; verifier | HIGH | — |
| C-21 | Generations 6, 7 and the smoke share batch sequence, monitor and initialization | OWN; verifier (RNG draws per batch exactly 40,575; monitor hash `e4fa6a9d…`) | HIGH | — |
| C-22 | Float nondeterminism alone yields 3× S₁ differences (0.460 vs 1.296 at step 409) | OWN `anal2.py` | HIGH (descriptive) | — |
| C-23 | The window held N_eff 118.0 of 499.4 (23.6 %) | OWN `anal2.py` | HIGH | — |
| C-24 | Population median S₂ 2.33 → 0.99 inside the window | OWN `anal2.py` | HIGH (descriptive) | — |
| C-25 | Trajectory 28's S₂ ≈ 2.1–2.6 (470–481) → 1.12–1.40 (892–943) | OWN `anal1.py` (fresh-time proxy) | MEDIUM–HIGH | E4 |
| C-26 | S₂ volatility falls with lr; IC volatility (~2× per recurrence) does not | OWN `anal2.py` | MEDIUM | — |
| C-27 | Median true per-body ‖a′‖ 159 (p99 2,070); ‖v′(0)‖ 2.03 | OWN `scales.py` (Stage-0 training data) | HIGH | — |
| C-28 | A full front allows RMS \|f\| ≈ 3.0 × 10⁴ ≈ 190× the median ‖a′‖ | OWN arithmetic | HIGH | — |
| C-29 | IC error is exposure-dependent: \|Δv′\| ≈ 5.8 (ID 0) vs ≈ 107 (ID 28) at the end | OWN `anal5.py` | HIGH (descriptive) | — |
| C-30 | First-layer τ-frequency ≤ 2.14 per unit τ (RMS 1.22 → 1.35 after training) | REPO `pinn/network.py:81-82`; OWN `ckpt.py` | HIGH | — |
| C-31 | Measured ‖a′‖/‖v′‖ ≈ 585–847 per unit u at initialization | REPO Phase-55 probe `raw.json` (sub-agent file A §E1) | HIGH | — |
| C-32 | The response to lowering `ω₀` is likely sub-quartic and may saturate (LayerNorm scale-invariance) | OWN; convergent with trainex-r3 OB (clean-room, NOT-VERIFIABLE-HERE) | MEDIUM–LOW | E5 |
| C-33 | The stack builds most of the derivative amplification | OWN from C-30/C-31 | MEDIUM | E5 |
| C-34 | `R_ref` probe cases are single-trajectory; 5 of 6 synthetic | REPO `pinn/verification/gate04_train_free.py:703-754`; verifier | HIGH | — |
| C-35 | GATE-04's controlled reduction passes for any finite non-degenerate vector by construction | OWN on 57-RULING §1 [PKG] | HIGH | — |
| C-36 | The smoke's front-1 at step 93 was transient (instantaneous front 0 at steps 100/200/300) | verifier (checkpoint-only recomputation) | HIGH | — |
| C-37 | `train.log` misreports a budget-exhausted hand-off after the invariant-B HALT | REPO `runs/stage0-v23g7-seed42/logs/train.log:964`; `controllers.py:2684-2688` | HIGH | — |
| C-38 | The spec's "fixed-monitor boundary above" reference dangles | REPO `pinn_architecture.md:452` (verifier) | HIGH | — |
| C-39 | The source method is Wang, Sankaran & Perdikaris, arXiv:2203.07404 (2022), published *CMAME* 421, 116813 (2024) | LIT (metadata verified; journal text not accessed) | HIGH | journal text (G-13) |
| C-40 | The source anneals ε over [10⁻²…10²], stops each stage at min w > δ = 0.99, recommends λ_ic = 10³ | LIT Wang, Sankaran & Perdikaris, arXiv:2203.07404, 2022, §3 and Alg. 1, pp. 6–8 [C1.13–C1.16] | HIGH | — |
| C-41 | Later practice uses a fixed tolerance (mostly 1.0), 16–32 chunks, 10⁵–3 × 10⁵ steps | LIT Wang, Sankaran, Wang & Perdikaris, "An Expert's Guide …", arXiv:2308.08468, 2023 [E2.6, T2.1]; Wang, Li, Chen & Perdikaris, "PirateNets", *JMLR* 25, 2024 [T3.1]; jaxpi code [T4.x] | HIGH | — |
| C-42 | The sources apply ε to raw residuals; none normalizes by an initialization reference | LIT same sources [C1.7, E2.3, E2.11, J4.2, K1.6]; silence 1 | HIGH | — |
| C-43 | The sources use Adam with slow exponential decay; no cosine, no L-BFGS hand-off | LIT [C1.24, E2.15–E2.16, P3.1]; silences 6–7 | HIGH | — |
| C-44 | Expected weight dynamics: zero except t = 0, progressive activation, all → 1; min w is the convergence indicator | LIT arXiv:2203.07404, §3, p. 6 [C1.20, C1.16]; Expert's Guide [E2.10] | HIGH | — |
| C-45 | Gradient-norm loss balancing is the documented remedy for gradient imbalance | LIT Wang, Teng & Perdikaris, *SIAM J. Sci. Comput.* 43(5), 2021 [W5.2.x]; Expert's Guide [E2.4–E2.6] | HIGH (as their claim) | — |
| C-46 | PINNs on chaotic systems can converge to physically correct, wrong-IC solutions | LIT Steger, Rohrhofer & Geiger, NeurIPS 2022 Workshop (abstract) [SG5.9.1] | MEDIUM (abstract only) | full text |
| C-47 | Zero-initialized residual gates avoid derivative pathologies of deep PINNs | LIT PirateNets, *JMLR* 2024 [P3.4–P3.7] | HIGH as their claim; untested here | E5 / D6-D |
| C-48 | SIREN's `ω₀ = 30` was justified for [−1, 1] inputs and 5-layer MLPs | LIT Sitzmann et al., NeurIPS 2020, §3.2, p. 5 [S5.6.2–S5.6.6] | HIGH | — |
| C-49 | The power-enhanced SkipResNet source uses no LayerNorm and tanh; p = 2 for < 30 layers | LIT Noorizadegan et al., *Appl. Math. Comput.* 480, 2024 [NR5.7.x] | HIGH | — |
| C-50 | H-01 point 2 holds for physics/data but omits the IC term, which binds | OWN (§3.7.1) | HIGH | — |
| C-51 | H-02's "two independent runs" is false | OWN + verifier | HIGH | — |
| C-52 | trainex-r3 OB warned of IC dominance (G-9) and the λ_phys equivalence; the warning did not reach `54-RULING`'s basis | REPO via extract: OB `:712-716`, `:684`; `54-RULING.md` points 1–5 [PKG] | HIGH | — |
| C-53 | Step cost ≈ 12 s/step on MPS (mean 12.07) | REPO `runs/stage0-v23g7-seed42/logs/train.log` | HIGH | — |
| C-54 | **The diagnosis M1.2/M5.1** (record-statistic artefact and threshold hovering) explains the trip timing better than lr starvation (M1.1) | OWN §3.1, §3.5 | HIGH / MEDIUM–HIGH | E7, per-step monitor trace |

---

## Appendix A — Reproduction (read-only; scripts outside the repository)

**Location and run conditions.**

- Scripts live in `scratchpad/r4/` of this session, outside the repository. If the
  project wants them, copy them into the Rule-19 review folder.
- Python is `<home>/miniforge3/envs/pinn-train/bin/python -B`: torch
  2.12.1, numpy 2.4.6, tensorboard 2.21.0.
- No script writes inside the repository. `git status --short` was identical before
  and after every run (11 pre-existing entries).

| Script | SHA-256 | What it does | Decisive output |
|---|---|---|---|
| `pool.py` | `a9f24212e0185384e7818ed4658e8cda3d428469c3185b88b91fd866bad4c844` | Stage-0 pool from `splits.json`; exact anchor-rank law | N₀ = 1812; P(rank 1) = 0.1325; mean rank 7.52; effective anchors 14.07 |
| `anchors.py` | `3246b1ea9d54bfb602c56e852b8c2a6f0e5ccd6367f8c252cc374100855cfc91` | Replays the numpy RNG stream of `_stage_batch`/`_run_validation` from metadata (training/validation file row counts; test files excluded); validates against checkpoint RNG states | Monitor keys match; state after monitor = `stage-0-init.pt`; `best.pt` = (900, post_step); 931/941/951 = post_batch/post_step; failure = (952, post_batch); 40 distinct anchors; trajectory-28 steps listed |
| `tbjoin.py` | `ac2f7264ccfe0fef3031479110f8499bf6ff5847089e6c1cb4d0c9f2fdcdf8e3` | Extracts TensorBoard per-bin series for generations 7 and 6 | recomputed front == logged on every record; raw/`R_ref` consistency 8.2 × 10⁻⁸ |
| `anal1.py` | `b29ab614bbdb0bd02b347fa61189106f140a0206439cd67286840fb8159a2784` | Same-trajectory comparisons; variance decomposition; per-anchor fronts; trajectory-28 series | E-C; PC-1(b); PC-7 |
| `anal2.py` | `4426498c53c9674cb10e2f09baae578e37b3081d223ad0039281e6418a070130` | Generation 6 vs 7 on identical steps; cumulative lr; volatility vs lr; block trends | PC-4; §3.1 numbers |
| `anal3.py` | `dbdb1aabcfb677821b67cf8689aaf8f5237e4848ab9857a3c838724c805754ef` | Natural experiment on consecutive same-anchor pairs | PC-2 item 2 |
| `anal4.py` | `ab595a9fec2ceb62e30c1be4122f2b9c02bdfaf8bbf9a15543ebcfcb2ec2dc6b` | Per-bin population reduction; S₁₄ | PC-2 item 3; §3.4 |
| `anal5.py` | `06a0d0cfd26b2dad09b03bf3db4b6f97f6f739ec12558502d4273084be3ac432` | Realized anchor concentration; IC error by anchor | C-06, C-29 |
| `scales.py` | `57d9f62cac15a5b89ef4f06dcce1f7c12eed907dc25f651f8945cc588bfb0e39` | True ‖a′‖ and ‖v′(0)‖ for 1,812 Stage-0 training trajectories | median 159 / p99 2,070; ‖v′(0)‖ 2.03 |
| `ckpt.py` | `c35052264b48b28d47e286a56c6c1b6b6e85a7bb6922fe0655da22b8dbb75d12` | Parameter drift, first-layer τ-frequency, Adam moments, clip activity | E-F |
| `norms.py` | `cbbf91368a8b864cc94f95dd572724aebdde5b85f2959722db910ca4b48d2a84` | Weight norms across checkpoints | head 1.7525 → 1.1715 |
| `plateau.py` | `a29594ad16a7042b4aa436edb6e2487d85900304854a76e2583ff965a52442f7` | Plateau-detector replay on logged `loss_phys` | longest run 6 / 4 / 4 |

**The anchor sequence.**

- File: `anchor_sequence.json` (SHA-256
  `fcc80c0bbc395d2c0f1d005edef7b6e6d7bc8e9da16f2f06ecd1c7a3fcbdf6f0`).
- It records the anchor of each of the 952 iterations, the monitor anchor (28) and
  the validation anchor (12).

**Sub-agent artifacts (read-only), in `scratchpad/r4/`:**

- `verify/f-row-verification.md`, with its scripts, including the checkpoint-only
  `monitor_recompute.py` and the Part G re-derivation;
- `q3-evidence.md`;
- `h03-extract.md`;
- `lit-notes.md`.

**What a Rule-19 verifier should re-derive first:**

1. Run `anchors.py`. The RNG-state equalities are binary and decisive for PC-1's
   reconstruction.
2. Re-read `controllers.py:1075-1143` and `:1746-1770` for PC-1's mechanism.
3. Re-run `anal3.py` and `norms.py` for PC-2.
4. Recompute the arithmetic in §3.2 for Q2.
<!-- END RESEARCH REPORT -->
