---
title: Trainex R2 Research Report — Stage-0 Physics-Gate Training-Recipe Questions (Q1–Q6)
role: external research agent report for the trainex-r2 round; one of several to be consolidated by the project owner
date: 2026-07-25
package_baseline: 9b1f0e7a4735df1c54867530cfd1f13b390e1514
entry_point: RESEARCH-CONTEXT-MASTER.md (read first, per its manifest and output contract)
status: complete
---

# Trainex R2 Research Report

## 0. Mandate, method, and evidence labeling

This report answers the six neutrally posed research questions in
`RESEARCH-CONTEXT-MASTER.md` §4 — Q1 training budget/steps, Q2 warmup +
learning-rate schedule, Q3 loss weighting/balancing (with the
normalization/data-scale sub-facet), Q4 Stage-0 curriculum pacing, Q5
evaluation policy, and Q6 dual-epsilon safety (owner-added 2026-07-24). It
recommends no remedy: remedy adjudication is owner-governed downstream. Each
answer frames trade-offs between plausible positions, states the evidence it
relied on, and poses discriminating evidence *as proposals requiring separate
owner authorization* — nothing was run, trained, or evaluated for this report.

**Scope note on sources (deviation from the master's §1, per commissioning
instruction).** The master states "you have no codebase access." The
commissioning prompt for this engagement explicitly overrides that: files
referenced inside the attachments but not attached are available in the
`trainex` worktree, and where an unattached reference matters to an answer I
was instructed to read it and record the gap. I therefore read, **read-only**
(no file was edited, no evaluator or training was invoked), the referenced
locked specs (`ctl_instruction.md`, `pinn_architecture.md`), the retained run
artifacts (`runs/stage0-pilot-seed42/` config, train log, validation records,
summary; sibling `validation.jsonl` files), the Phase-44 evidence tree
(`eps_h_distribution.json`, `loss_decomposition.json`, `seed_band.json`,
`manifest.json`, `44-GAPS.md`, `v2.1-GAPS.md`), the cited verification and
verdict documents (`38-VERIFICATION.md`, `43-CALIBRATION.md`, `43-VERDICT.md`),
and the executed training/evaluation code (`pinn/train.py`,
`pinn/training/*.py`, `pinn/loss_catalog.py`, `pinn/physics_residual.py`,
`pinn/evaluate.py`, `pinn/verification/gate_metrics.py`, probe and data-path
modules). Where even these sources are silent, the gap is recorded in §8.

**Evidence labels used throughout:**

- **[FACT]** — established content of the four attachments; cited to bare
  filename/section or an `F-` claims-register row. Relied on as ground truth.
- **[FACT-W]** — a fact verified in this engagement directly from a worktree
  file (spec, code, config, log, or retained evidence JSON), cited by filename
  (and line(s) where useful). These are checkable observations of what the
  locked spec says and what the executed artifacts contain; they are offered
  for owner verification, not as substitutes for the attachments.
- **[R-HYP]** — this report's own interpretive analysis. Same epistemic tier
  as the diagnosis's `[HYP]`/`H-` rows: **agent analysis, not established
  fact.** Nothing labeled [R-HYP] should be consolidated as established.
- `H-` rows are cited **only as hypotheses under challenge**, never as facts.
  §7 states explicitly where this report's evidence supports, qualifies, or
  contradicts each DIAG-04 ranking. No answer below treats an `H-` row as
  established; a per-question "claims relied on" line makes this auditable.

Locked spec content (`framework-specs-bundle.md`; the underlying
`ctl_instruction.md` / `pinn_architecture.md` sections) is treated as hard
constraint throughout. Where a worktree observation *conflicts* with a locked
number or formula, this report says so explicitly and does not silently
override either side — per the bundle's own instruction.

**Standing context (so this report stands alone).** The Stage-0 CTL-PINN
pilot's sole held-out physics-conservation gate rendered **FAIL**:
`eps_H = 237.2086056078468` against reject threshold `1e-5`
(`SCS = 2.3751304405952904` against `-5.0`), over 1,500 held-out trajectories
(F-01). The failure is uniform — 1500/1500 trajectories exceed the threshold
individually, `min = 0.9741251227996501`, so the best trajectory misses by
about five orders of magnitude (F-02) — and the headline is, by owner
instruction, the worst-case max, a verdict-neutral choice since the
population fails under any aggregate (F-15). The owner signed **adjust**
(2026-07-22): keep the mechanical Stage-0 slice, block platform expansion,
route this separately governed investigation; the held-out evaluator budget
is exhausted and must not be retried under current policy
(run-evidence-bundle.md Group 3; F-01).

---

## SV. Source-verification findings that bear on multiple questions

Six verification findings from the worktree pass are used by several answers
below. They are stated once here, with citations, and referenced as SV-1…SV-6.
Each is a checkable observation; the *interpretations* offered under each are
labeled [R-HYP].

### SV-1 — The executed pilot ran with the energy-conservation weight ACTIVE (λ_E → 1.0), not zero

The locked PHYS-05 schedule sets `lambda_E^max = lambda_L^max = 0` for Stage 0
(`k ∈ {0,1}`) (framework-specs-bundle.md Excerpt 5 [FACT]), and both
attachments read the pilot through that lens: "both conservation weights are
**zero throughout Stage 0** by the locked schedule" (Excerpt 5 "Why it matters
here"), "so the angular-momentum and energy terms contribute no gradient
signal during Stage 0 by design" (RESEARCH-CONTEXT-MASTER.md §4 Q3 facts
bullet), "consistent with the observed `lambda_l == 0.0`"
(run-evidence-bundle.md Group 4).

The retained artifacts show the executed run diverged from that schedule on
the energy weight:

- [FACT-W] The frozen pilot config sets `loss.lambda_e_max: 1.0`
  (`runs/stage0-pilot-seed42/config.yaml`; identically in `configs/smoke.yaml`
  and `configs/stage0-example.yaml`).
- [FACT-W] `runs/stage0-pilot-seed42/logs/train.log.jsonl` logs a per-step
  `lambda_e` field: 0.0 at step 1, ramping as (i−1)/30, equal to `lambda_phys`
  at every one of the 300 steps, reaching **1.0 at step 31 and staying 1.0
  through step 300**. Verified over all 300 records.
- [FACT-W] The diagnosis's own retained evidence records this:
  `evidence/diag02/loss_decomposition.json` →
  `phys05_interaction.lambda_values_at_final_step.loss_energy = 1.0` for **all
  four runs** (seeds 41/42/43 and smoke).
- [FACT-W] The seed-42 summary arithmetic confirms the weighted total includes
  the energy term and excludes the angular-momentum term:
  `total 650443456.0 ≈ phys 650400832.0 + ic 38527.19 + energy 4093.83 +
  data 0.1355` (angmom 587.65 absent) (`runs/stage0-pilot-seed42/summary.json`).
- [FACT-W] Mechanism: `pinn/train.py` (≈ lines 750–753) constructs
  `ScheduledWeights(n_adam, lambda_e_max=float(config.loss.lambda_e_max))` —
  the config surface exposes exactly one λ^max override (the energy one);
  `lambda_l_max` and `lambda_phys_max` use the code defaults (0.0 and 1.0).
  `pinn/training/scheduled_weights.py` documents the per-stage λ^max caps as
  "PROVISIONAL, config-overridable defaults carrying PHYS-05 / Phase-35
  LOSS-02 provenance — never cited as ratified, surfaced for ACC-05 pilot
  calibration," with the `λ_E^max ≤ 1` bound as the one hard cap.

What this does and does not establish: the F-08 register row ("`lambda_phys =
1.0` from step 31; `lambda_l = 0.0` at all 300 steps") remains exactly true —
it is silent on `lambda_e`. But the package's framing that the energy term
contributed *no gradient signal in Stage 0 by design* does **not** describe the
executed run: `loss_energy` (raw values ≈ 1.7e3–1.6e4 across the run) entered
the trained total at weight 1.0 for ~90% of the steps. Two readings are
possible and **neither is adjudicated here**: (a) the config exercised a
calibration freedom the code explicitly marks provisional/config-overridable,
so the run is a legitimate Stage-0 calibration variant of PHYS-05; (b) the run
silently diverged from the locked stage table that the trainex-r2 bundle
presents as a hard constraint. The attachments cannot distinguish (a) from (b)
— no ratification record for `lambda_e_max: 1.0` appears in 43-CALIBRATION.md's
owner-ratified values (R-1/R-2/D4-a cover guards, retries, checkpoint ceiling
only [FACT-W]). Recorded as gap RG-01. [R-HYP] Materiality caveat: with
`loss_phys` ≈ 2.0e7–3.7e9 against `loss_energy` ≈ 1.7e3–1.6e4, the energy
term's share of the trained total was ~1e-5 at the final step, so the
divergence plausibly did not drive the outcome — but loss-value shares are not
gradient shares, and per-term gradient norms were not logged (SV-5), so
materiality is not established.

### SV-2 — The causal weighting operated in a fully collapsed regime for the entire run: physics supervision effectively reached only the earliest collocation time

- [FACT-W] `pinn/train.py` (≈ line 755) hardcodes `collocation_count=16`; the
  sampler draws 16 i.i.d. uniform times in [0, T=10] each step
  (`pinn/training/collocation_sampler.py`), sorted ascending in the anchor
  context (`pinn/training/controllers.py` ≈ 484–499).
- [FACT-W] Every one of the 300 logged steps of `stage0-pilot-seed42` records
  `w_max = 1.0`, `w_mean = 0.0625` (= 1/16 exactly), `w_min = 0.0`, and
  `front_idx = 0` (train.log.jsonl, all records verified).
  `front_idx` is defined in `pinn/training/controllers.py` (≈ 570–572) as the
  largest collocation index with causal weight w > 0.5, −1 if none: 0 means
  only the first collocation time carried weight above 0.5. `w_mean = 1/16`
  with `w_max = 1` and `w_min = 0` means w₁ = 1 and all fifteen later weights
  ≈ 0 to float precision. The diagnosis evidence records `front_idx: 0` at the
  spike step for **all four runs**
  (`evidence/diag02/loss_decomposition.json`, per-run `warmup_spike`).
- [FACT-W] No causal-exponent clip is implemented: `pinn/loss_catalog.py`
  (`causal_physics_loss`, ≈ 228–231) states "The exponent is left unclipped
  except by the natural finite range of exp (the spec defers a numeric clip
  bound to FUT); underflow drives w_n → 0, which is correct causal gating."
  The locked spec indeed defers the numeric clip bound
  (framework-specs-bundle.md Excerpt 5 [FACT]; ctl_instruction.md ≈ line 1773:
  "The exponent must be clipped to avoid underflow, but no numeric clipping
  bound is selected… deferred to FUT" [FACT-W]).
- [R-HYP] Arithmetic of the collapse: with η_c = 1 and the run's residual
  magnitudes (logged `loss_phys` — the causally weighted mean actually trained,
  per the log's `total` arithmetic — between 2.0e7 and 3.7e9), the exclusive
  prefix sum in `w_n = exp(−η_c Σ_{m<n} R̄_m)` exceeds the float32/float64
  underflow range (≈88/≈745) after the first collocation point at every step
  of every run: the collapse is a structural consequence of residual scale,
  not a transient. Under collapse, `L_phys^causal ≈ R̄₁/16`, so the trained
  physics signal at the final seed-42 step (`loss_phys = 6.504e8`) corresponds
  to a first-collocation-time residual energy R̄₁ ≈ 1.0e10.

Consequence stated neutrally: for the whole 300-step budget, the *effective*
physics-residual supervision covered ~1/16 of the sampled time domain — the
earliest sampled time only (resampled each step) — while the held-out gate
measures `max_t` drift over the full trajectory (Excerpt 1). Whether this is
"correct causal gating" (the code's reading: with enormous early-time
residuals, later times *should* be masked until the front advances) or a
mechanism that prevented the physics term from ever constraining late-time
behavior within this budget is exactly the kind of question Q2–Q4 pose; both
readings are laid out there.

### SV-3 — The learning-rate schedule is spec-pinned (but outside the attached excerpts), and the executed schedule matches it

- [FACT-W] `ctl_instruction.md` (≈ 1795–1809, "Phase 2a: Adam-driven
  Exploration → Initialization") locks: initial LR per stage
  `LR_k = 10⁻³ × (0.7)^k`; a cosine-annealing scheduler decaying over the
  phase; Adam β₁ = 0.9, β₂ = 0.999, ε = 1e-8; and a full reset of Adam state
  at each stage start. The "Consolidated Hyperparameter Schedule" table
  (≈ 1999–2004) repeats `10⁻³ × (0.7)^k` for stages 0–1.
- [FACT-W] The implementation matches: `pinn/training/controllers.py`
  (≈ 1192–1218) builds Adam with `lr = cfg.opt.lr_for_stage(k)` and
  `CosineAnnealingLR(T_max = max(n_adam_k, 1))` (η_min = 0 default); the pilot
  config sets `adam_lr_base: 0.001`, `adam_lr_decay: 0.7`
  (`runs/stage0-pilot-seed42/config.yaml`). The logged per-step `lr` traces the
  cosine from ≈1.0e-3 (step 1) through exactly 7.5e-4 (step 100) to 0.0
  (step 300) (train.log.jsonl [FACT-W]) — consistent with the four spike-step
  lr values in F-07.
- Therefore F-07's "seed42 spiked at peak lr = 7.5e-4" is best read as: all
  four runs share one deterministic lr(step) curve; the spikes landed at
  different steps, hence different lr values, and seed42's (step 100) landed
  highest on the curve. There is **no LR warmup**: the schedule starts at the
  stage maximum; only the loss weights warm up (30 steps; SV-1). [FACT-W]

Also spec-relevant and absent from the attachments: adaptive median-based
gradient clipping is part of the locked recipe and ran every Adam step —
clip = C_stage · median(last ≤100 pre-clip global norms), Stage-0/1 C_stage
locked only as the range 7–10 (implementation default 8.5, provisional,
config-overridable), median floor 1e-6, Adam-only
(pinn_architecture.md §4.4; ctl_instruction.md ≈ 1855–1890;
`pinn/training/grad_clip.py`) [FACT-W]. The logged `grad_norm` values
(3.0e8–7.1e13 across seed 42's run) are **pre-clip** norms
(`GradClipOutcome.total_norm` docstring) [FACT-W]; applied updates were
bounded by the adaptive clip. None of this clipping context appears in the
attached materials; it matters for how Q2 reads the "spike" evidence.

### SV-4 — Frame/scale contract of the executed data path vs the locked component math (the normalization sub-facet made concrete)

The locked component contract is dimensionless: data loss compares the
network's predicted **scaled** positions r′ against ground truth **scaled by
D** (`r′_true = r_true/D`), with u = t/T (pinn_architecture.md §3.1, quoted in
framework-specs-bundle.md Excerpt 4 [FACT]; Phase-35 LOSS-01 contract block in
§3.1 [FACT-W]). The residual/force operator with **raw masses and G absorbed
into D** is exactly force-consistent in that scaled frame (D³ = G·T², so
T²/D³ = 1; `pinn/constants.py` PIPE-09 note; `pinn/physics_residual.py`
docstring) [FACT-W].

What the executed pipeline does:

- [FACT-W] The production adapter materializes the **raw parsed Brutus
  arrays** as the per-trajectory tensors: `positions=parsed_brutus.positions`
  flow into `_trajectory_tensors` unmodified (`pinn/data/adapter.py`, admission
  pass ≈ 843–875 and materialization ≈ 918–939). `snapshot_positions()` returns
  these raw arrays; `pinn/data/batches.py` (`sample_data_points`, ≈ 240–275)
  passes them through as the data-loss `targets` with no /D scaling; no
  division by D exists anywhere on the training target path (grep across
  `network.py`, `com_projection.py`, `batches.py`, `adapter.py`,
  `controllers.py`).
- [FACT-W] The scaled/gauge-fixed system **is** computed — but only for
  metadata: `pinn/data/preprocessing.py` (≈ 193–217) COM-recenters, canonically
  reorders bodies (descending mass; ≈ 109–120), applies the rotation gauge,
  and scales `r/D`, `v/(D/T)`; the results feed IC13 (then tanh-normalized)
  and the stage-label invariants (computed from the *scaled* initial state
  with ε = 1e-10; ≈ 237–255). The full scaled trajectory (`pre.r_gauge`) is
  discarded for training purposes.
- [FACT-W] Consequently the executed run pairs: gauge-fixed, scaled,
  tanh-normalized IC13 inputs and canonically ordered masses **with raw-frame,
  raw-order, unscaled position targets**; and the IC anchor compares the
  network's du-derivative velocity at u=0 against the **raw dt-frame** first
  snapshot velocity (`pinn/training/controllers.py` ≈ 463–466, 511–519).
- [FACT-W] The Phase-38 proof rungs — the machinery-integrity evidence behind
  F-06 — ran in the **scaled** frame: the residual probe divides positions by
  D and converts velocities by T/D (`pinn/verification/residual_probe.py`
  lines 142, 194), and the overfit probe fits `fixture.positions / D`
  (`pinn/verification/overfit_probe.py` ≈ 309–312). 38-VERIFICATION.md Rung 3
  records force–energy consistency at 1.5e-15 and a u-leaf ODE residual median
  relative error 0.0065 **on the scaled arrays** — i.e., the residual operator
  is verified to vanish on ground truth in the scaled frame.
- [R-HYP] Implication if the raw corpus is in G=1 N-body units (which the
  admission/scaling prose implies but this report cannot confirm without the
  gitignored corpus): a trajectory that satisfies d²r/dt² = force(r) in raw
  units satisfies d²r/du² = T²·force(r) = 100·force(r) in the u-leaf — so the
  coded residual `a′ − force` does **not** vanish on raw-frame ground truth
  (it evaluates to ≈ 99·force), and the data term (pulling toward raw targets)
  and physics term (pulling toward the scaled-frame EOM) become mutually
  unsatisfiable; similarly the model's hard zero-COM output cannot match
  raw-frame targets whose COM is nonzero or drifting, and the IC velocity
  anchor is off by the frame factor even at a perfect fit. This is a candidate
  *mechanism* squarely inside DIAG-04 candidate 4's territory (H-06,
  normalization/data-scale mismatch) that the retained DIAG-01..03 outputs
  neither examined nor could have excluded. It is stated here as hypothesis,
  not finding: whether the corpus units, body ordering, and COM state actually
  produce a live inconsistency is checkable but was not checked against data
  (no corpus payload in the worktree; SCOPE-23 forbids new runs). Discriminating
  checks are posed under Q3.

### SV-5 — Instrumentation actually available vs what the questions need

- [FACT-W] The step log carries 27 fields including per-term raw losses, the
  five λ values, global pre-clip grad_norm, lr, causal-weight stats
  (w_min/w_mean/w_max/front_idx), finiteness, and per-bin residuals to the TB
  sink; it does **not** carry per-term gradient norms, clip-applied vs pre-clip
  update magnitude, or any energy-drift proxy of the gate's form. The Phase-35
  contract explicitly requires "before any future control law, log weighted
  losses, scheduled weights, and gradient statistics" (Excerpt 5 [FACT]) — the
  pilot logged weighted losses and scheduled weights but only a single global
  gradient norm.
- [FACT-W] Validation ran only at steps 100/200/300 (`opt.validation_every:
  100`), producing three points per run; the `trend` field is a last-window
  comparison to the previous record (`pinn/train.py` `_append_validation_record`)
  — which is exactly why 43-CALIBRATION ("2/3 worsened", last-window) and
  DIAG-03 ("1/3 worsened", first-vs-last) disagree while both are faithful
  (F-11/F-12). The validation loss itself is the λ-weighted total on a
  validation batch whose non-data terms are computed on a single anchor
  trajectory (SV-6), so it is phys-dominated and anchor-noisy.
- [FACT-W] `best.pt` — the checkpoint the sole evaluation consumed — is
  selected by lowest validation total (`pinn/train.py` checkpoint hook), i.e.,
  effectively by the physics-residual value on validation anchors, not by any
  energy-drift measure.

### SV-6 — Batch and term topology of the executed run differs from the canonical batch contract

- [FACT-W] Canonical contract: 256-trajectory batches (240 replay + 16
  lookahead), per-trajectory data-point cap `n_pts = min(32, n_snapshots)`,
  collocation budget provisional ≈4096, energy loss reusing the physics
  collocation set (ctl_instruction.md ≈ 1811–1847, all tagged provisional).
- [FACT-W] Executed: `replay_count: 32` (config seam, 43-03 ACC-02),
  **16** collocation points, and — structurally — the physics, energy,
  angular-momentum, and IC terms are computed each step on **one anchor
  trajectory** (the first replay key) with its ground-truth h₀/L₀
  (`pinn/training/controllers.py` ≈ 441–500, 511–580; module docstring notes
  `eps_h` is "a provisional |h0|·1e-4 scale (mirrors the documented
  eps_h = 1e-4·S_H form; no S_H pipeline exists yet upstream)"). The spec's
  training-loss energy floor `ε_H = 1e-4·S_H`, S_H = median_train(K0+Uabs0)
  (Excerpt 4 §3.4 [FACT]) is therefore implemented as a per-anchor
  `|h0|·1e-4 + 1e-12` stand-in. Also minor: the implemented per-time residual
  energy is the mean over 9 components, `(1/9)Σᵢ‖fᵢ‖²`, where §3.2 defines
  `R̄_n = (1/3)Σᵢ‖fᵢ‖²` — a factor-3 scale difference inside the causal
  exponent and the physics loss (`controllers.py` ≈ 534) [FACT-W].
- [FACT-W] Two-phase optimization never ran its second phase: with
  `n_adam = max_epochs = 300` the L-BFGS budget was zero; all 300 steps are
  phase "2a", and the stage machine returned HALT at step 300
  (`runs/stage0-pilot-seed42/curriculum.jsonl`: `{"disposition": "HALT",
  "from_stage": 0, "to_stage": 0}`), the CURR-03 ADVANCE gate (four criteria,
  including validation physics loss < 1e-4 and mean relative energy drift
  < 1e-4, all provisional) being far from met (validation totals ~7.8e7–1.9e9)
  (ctl_instruction.md ≈ 1922–1998; `pinn/training/stage_exit.py`) [FACT-W].

---

## Q1 — Training budget / steps

**The question.** Given that validation was still moving at 300 steps yet a
single trajectory reached a floor in 176, what is the principled way to decide
whether and how much more budget the Stage-0 population run should receive —
and what evidence would separate a pure budget shortfall from the
population-scale generalization shortfall?

### Evidence base

All four runs finished 300/300 finite steps (F-10). Validation was still
moving at step 300, with the direction verdict depending on the definition —
1/3 seeds worsened first-vs-last, 2/3 last-window; neither adjudicated
(F-11, F-12; 44-DIAGNOSIS.md §4). The Phase-38 single-trajectory overfit
control reached its ≥1e3 data-loss reduction (`L0/Lf = 1097.6107…`) in 176
steps (F-06). The budget is a
recipe parameter, not a locked invariant (RESEARCH-CONTEXT-MASTER.md §4 Q1
spec position; the per-stage MAX_EPOCHS/N_Adam tables are explicitly
"claimed-unverified… provisional pending Stage-0 pilot calibration",
ctl_instruction.md ≈ 1994–1997 [FACT-W]). Wall-clock cost of the current
budget is small: 195.7–201.9 s per 300-step run on the pilot hardware
(run-evidence-bundle.md Group 2). DIAG-04 candidate 5 ("insufficient budget")
is ranked Weak and explicitly confounded with candidate 1 (H-07, H-03 — agent
analysis, not established).

### Analysis

**(a) The 176-step comparator is weaker than the question's framing implies.**
The confound the master names is budget-vs-population-scale. The worktree
evidence adds that the Phase-38 control also differed from the pilot in
*recipe*, not just population size: it optimized the **data term only** at a
**constant lr = 1e-4** (vs the five-term composite at cosine 1e-3→0), with a
`zeros(13)` placeholder IC13, on **D-scaled** targets through the probe-local
loader, and its soft-energy term was "not evaluated" (38-VERIFICATION.md
Rung 4 [FACT-W]; the retained `seed_band.json` itself carries these caveats,
including "different optimizer/training context… vs the Stage-0 curriculum
training" [FACT-W]; SV-4). So "one trajectory floors in 176 steps" bounds what
the *architecture plus a data-only objective in the verified frame* needs; it
does not calibrate what the *pilot recipe on the pilot data path* needs per
trajectory. Any budget rule that extrapolates from 176 steps inherits those
differences. [R-HYP]

**(b) Under the locked schedules, "more steps" is not a single-variable
change.** Three couplings are structural: (i) `I_warm = min(2000,
floor(0.1·N_Adam,k))` — extending N stretches the λ warmup proportionally
until the 2000 cap (Excerpt 5 [FACT]; `scheduled_weights.py` [FACT-W]);
(ii) the cosine LR schedule anneals over exactly `T_max = n_adam` — extending
N reshapes lr(step) everywhere, and the locked spec pins the cosine + base LR
(SV-3), so a "same-schedule, more-steps" arm is not expressible without either
holding T_max fixed (diverging from "decay over the phase") or rescaling
(changing every step's lr); and (iii) the budget splits between Adam
(`n_adam`) and L-BFGS headroom (`max_epochs − n_adam`) — the pilot allocated
zero polish budget, so the locked two-phase strategy's Phase 2b has never run
on population data (SV-6). A principled budget rule must state which of these
co-varies with N; otherwise "budget" silently bundles warmup pacing (Q4) and
LR schedule (Q2) changes. [R-HYP grounded in locked formulas]

**(c) What "still moving" can and cannot support.** With
`validation_every = 100`, each run has three validation points, the trend
field is a two-point last-window comparison, and the validation total is
phys-dominated and computed on a single validation anchor per pass
(SV-5, SV-6). The first-vs-last vs last-window disagreement (F-12) is not a
data conflict but a definition gap — and with three points, *any* trend
statistic is fragile. Meanwhile the distance to the gate is five orders of
magnitude at the population's best (`min eps_H = 0.9741…` vs 1e-5, F-02), while
the best observed within-run validation improvement across 300 steps is about
one order (seed 42: 8.38e8 → 7.85e7 [FACT-W validation.jsonl]). Whether that
gap is closable by steps at all is exactly what the retained evidence cannot
say — but the magnitudes mean a budget rule that merely says "train until the
3-point trend flattens" would be making a ~5-order extrapolation from a
~1-order observation. [R-HYP] Seed variance compounds this: the final
validation relative span across seeds is 3.8224247683129153 (F-13), measured
over per-seed validation splits that are not even the same populations
(F-14) — so a budget rule keyed to validation magnitudes needs both a shared
split and a seed-replication requirement before its trigger is meaningful.

### Trade-offs between plausible positions

- **Extend budget on the unchanged recipe (pure-budget arm).** For: cleanest
  single-variable evidence *given* a fixed policy for (b)'s couplings; cheap
  (~200 s per 300 steps observed). Against: if any structural mechanism
  (SV-2's collapsed causal front, SV-4's frame question) binds, added steps
  measure the plateau of a mis-specified objective, and the arm spends budget
  to learn mainly that the trend flattens far from the gate.
- **Pair budget with population-size scaling (deconfounding design).** For:
  directly addresses the H-03/H-07 confound — train at fixed recipe on nested
  subsets (e.g., 1, small-n, full population; the exact sizes are a design
  choice for the owner) and at two or more budgets, reading whether
  per-trajectory train fit at fixed budget degrades with population size
  (capacity-limited signature) or improves uniformly with budget at fixed
  population (budget-limited signature). Against: multiplies run count; and
  the single-trajectory cell only reproduces the Phase-38 comparison if the
  recipe is also aligned, otherwise it re-imports (a).
- **Gate budget decisions on training-side gate-proxies rather than loss
  trends.** For: the gate is `max_t |ΔH/H(0)|`; a budget rule keyed to an
  offline drift proxy on *training/validation* data (never the held-out set;
  Q5 governance untouched) measures distance-to-gate in the gate's own units,
  which loss totals do not. Against: requires new instrumentation (SV-5) and
  an owner-authorized computation; and the proxy-vs-gate relationship is
  itself unmeasured (metrics live on different data and statistics).

### What a complete answer specifies (structure only)

A defensible budget rule for the Stage-0 population would specify: (1) a
pre-registered stopping/plateau criterion with the trend definition fixed in
advance (resolving the F-12 ambiguity) and a validation cadence dense enough
to support it; (2) the co-variation policy for the three locked couplings in
(b) (I_warm, cosine horizon, Adam/L-BFGS split), stated explicitly so "budget"
is a defined treatment; (3) the deconfounding grid — budget × population-size
cells sufficient to distinguish the budget-limited from capacity-limited
signatures, with the recipe held fixed across cells and, if the Phase-38 rung
is to serve as an anchor cell, a like-for-like reconciliation of its recipe
differences (objective, lr, frame; SV-4); (4) gate-aligned progress
observables (an offline drift proxy and tail statistics on training-side data,
since the locked gate is a worst-case max — F-15) with pre-registered
thresholds for "budget is helping"; and (5) identical held-out-*validation*
split governance across seeds so cross-seed magnitudes become comparable
(F-14 shows they currently are not). Every measurement above is a proposal
requiring owner authorization (SCOPE-23); none is performed or promised here.

**Claims relied on:** F-02, F-06, F-07, F-10, F-11, F-12, F-13, F-14, F-15;
H-03/H-07 cited as challengeable context only. Worktree: SV-2, SV-3, SV-4,
SV-5, SV-6; 38-VERIFICATION.md; seed_band.json; validation.jsonl;
ctl_instruction.md budget/N_Adam provisionality. No H-row treated as
established.

---

## Q2 — Warmup + learning-rate schedule

**The question.** How should warmup and the learning-rate schedule be designed
for this Stage-0 population, and what per-step evidence would distinguish a
benign finite warmup transient from a pathology that contributes to the
physics-gate failure?

### Evidence base

Every run showed a finite spike of 3.7e9–6.1e9 in total loss, ≥99.998%
`loss_phys`, with pre-clip `grad_norm ≈ 5–7e13`; seed 42's spike (step 100)
sat at lr = 7.5e-4; all runs finished 300/300 finite (F-07, F-10). λ_phys
reached 1.0 at step 31 in all runs (F-08). Spec position: the PHYS-05 warmup
schedule and causal weighting η_c = 1 (Excerpt 5, §3.2 [FACT]); plus, from the
worktree: the LR contract `LR_k = 10⁻³·0.7^k` with cosine annealing over the
phase and full Adam-state reset per stage (ctl_instruction.md ≈ 1795–1809
[FACT-W], SV-3); adaptive median gradient clipping every Adam step with
Stage-0/1 C_stage locked only as a 7–10 range (SV-3); no LR warmup anywhere in
spec or code; and the causal-weight collapse regime (SV-2). DIAG-04
candidate 3 ("optimization/warmup pathology") is Moderate (H-05 — challengeable
context).

### Analysis

**(a) Three distinct timescales are being conflated by the word "warmup."**
The λ ramp completes at step 31 (I_warm = 30). The LR cosine peaks at step 1
and decays monotonically. The spikes occur at steps 100–194 — 70 to 164 steps
*after* the λ warmup ends, at mid-schedule LR values. So the spike is not the
λ ramp arriving; on the retained evidence it is a mid-run transient of an
already fully-weighted objective. [FACT-W timing; R-HYP reading] This matters
for the question's own framing: "warmup pathology" as a candidate should be
split into (i) the λ ramp (steps 1–31; observed grad_norm grew from 3.0e8 at
step 1 to ~2.0e12 at ramp end, reaching 3.6e13 two steps later [FACT-W]),
(ii) the no-warmup LR start (full 1e-3 at
step 1 against an untrained SIREN), and (iii) mid-run spikes under causal
collapse. Each has different per-step signatures.

**(b) The clipping context changes what the spike numbers mean.** The
5–7e13 norms are pre-clip; every step's applied update was bounded by
C_stage·median(window) with C_stage(0-1) implemented at 8.5 (provisional
within the locked 7–10 range) (SV-3). A spike step's update is therefore
capped at ≈8.5× the recent median update scale — which is consistent with
"finite spikes, no non-finite steps, run continues" (F-10) without implying
the optimizer absorbed a 7e13-magnitude step. Conversely, persistent norms in
the 1e12–1e13 band mean the *median itself* was enormous, so clipping mostly
did not bind between spikes. Any pathology-vs-benign adjudication should
therefore examine clip_value, pre-clip norm, and applied-update magnitude
per step — only the pre-clip norm was logged (SV-5). [FACT-W + R-HYP]

**(c) The causal-collapse regime is the schedule-level structure most
directly connected to the gate's form.** Under SV-2, physics supervision
never extended past the earliest of 16 collocation times in any run, while
the gate is a max-over-time drift. Two readings, posed neutrally:
(i) *Working as designed*: causal gating is supposed to withhold late-time
supervision until early-time residuals fall; the pilot simply never earned
front advancement within 300 steps — the schedule is fine and the budget or
capacity is the binding constraint (connects to Q1/H-03). (ii) *Schedule
pathology*: with residual magnitudes set by the SIREN's ω₀ = 30 second
derivatives and (possibly) the SV-4 frame question, the exponent
η_c·ΣR̄ was astronomically past underflow from step 1, so the front *could
not* advance on any relevant timescale — the deferred exponent clip (Excerpt 5;
implemented as no clip) plus η_c = 1 made L_phys^causal ≈ R̄₁/16 for the whole
run, i.e., the effective objective differed structurally from the nominal
one. Under (ii) the "spike" facts are secondary; the primary optimization
fact is the collapse. The retained evidence cannot pick between (i) and (ii);
the per-step evidence below can. [R-HYP]

### Trade-offs between plausible positions

- **Keep the locked no-LR-warmup cosine as-is** (it is spec text, SV-3): For:
  the runs were finite and improving on data/IC terms early; the schedule is
  locked and simple. Against: the full-strength 1e-3 start against ω₀ = 30
  SIREN curvature coincides with the largest early grad norms; whether that
  seeded the Adam second-moment state with spike-scale statistics (an
  optimizer-memory effect that outlasts the ramp) is unmeasured. Changing it
  is a spec-conflicting move that would need explicit owner action; the
  research answer is to *measure*, not assume, its contribution.
- **Treat η_c / the exponent clip as the schedule's live design surface.**
  For: the spec itself defers the numeric clip bound and mandates clipping "to
  avoid underflow" (Excerpt 5; ctl ≈ 1773) — the implementation's no-clip
  choice, with its "underflow is correct causal gating" rationale
  (loss_catalog.py), is exactly the deferred decision surfacing in behavior
  (SV-2). A clip bound (or η_c value) determines whether the causal front can
  move at these residual scales. Against: with R̄ ~ 1e8–1e10, no plausible
  clip bound alone re-opens later times *unless* residual scale itself falls
  (Q3's normalization sub-facet); a clip choice made in isolation may be
  cosmetic. Either way this is a spec-completion decision reserved to the
  owner; posing it is in scope, choosing it is not.
- **Reallocate budget across the two locked phases (Adam vs L-BFGS).** For:
  Phase 2b is locked recipe and has never run at population scale (SV-6); its
  trust-region behavior is a different optimization regime the pilot never
  sampled. Against: L-BFGS on a collapsed causal objective inherits the same
  effective-objective question; and frozen λ during 2b (Excerpt 5) means it
  cannot fix weighting issues.

### Per-step evidence that would discriminate benign transient vs contributing pathology (structure only; owner-gated proposals)

A complete answer would pre-register per-step logging of: pre-clip norm,
clip_value, applied-update norm, and per-term gradient norms (the Phase-35
contract's own precondition for any future control law — Excerpt 5); the
causal-weight distribution (w stats and front_idx are already logged — their
full-run traces should be first-class evidence, not incidental fields);
Adam second-moment summary statistics around spike steps (optimizer-memory
test for (a)); residual-by-collocation-time profiles (already TB-sunk as
`residuals_bin_*` [FACT-W step_log.py]); and recovery half-life of total loss
after each spike. The discriminating readouts: a benign transient shows
post-spike recovery to the pre-spike trend with no persistent change in
per-term gradient shares or front_idx; a contributing pathology shows
spike-correlated durable regression in gate-aligned proxies (offline drift on
training-side data) or a front that never advances while early-time residuals
stagnate — measured, not asserted. An LR/warmup ablation grid (the DIAG-04
proposed test, still a proposal) only becomes interpretable once those
per-step observables exist; running it before the instrumentation would
reproduce the current situation in which "spike" is visible but its
consequence is not.

**Claims relied on:** F-07, F-08, F-10; H-05 as challengeable context.
Worktree: SV-2, SV-3, SV-5, SV-6; ctl_instruction.md ≈ 1795–1809, ≈ 1855–1890,
≈ 1773; loss_catalog.py; grad_clip.py; train.log.jsonl sweeps. No H-row
treated as established.

---

## Q3 — Loss weighting / balancing (including the normalization / data-scale sub-facet)

**The question.** How should the loss terms be weighted/balanced for the
Stage-0 population — including how to treat the ≈10-order scale separation
between the physics and data terms and the Stage-0 zeroing of the conservation
weights — and what evidence distinguishes intended dominance from a weighting
that contributes to the gate failure?

### Evidence base

`loss_phys` carries ≈99.998–99.999% of every spike and dominates cumulative
raw and λ-weighted aggregation in every run (F-07, F-09); `lambda_l = 0.0` at
all 300 steps (F-08); the locked PHYS-05 table zeroes both conservation
weights for k ∈ {0,1} (Excerpt 5 [FACT]); the loss catalog and total assembly
are locked (Excerpt 4); the sub-facet reads `loss_phys ≈ 1e9` vs
`loss_data ≈ 0.1` against the tanh input normalization, the hard COM
projection, and the structural linear-momentum treatment (Excerpt 6). From
the worktree: SV-1 (the executed run's λ_E was 1.0, not 0), SV-2 (causal
collapse makes the trained physics term ≈ R̄₁/16), SV-4 (the frame/scale
contract of the executed data path vs §3.1 and the probe-verified residual
frame), SV-5 (no per-term gradient logging), SV-6 (single-anchor non-data
terms; per-anchor ε_H stand-in for the spec's 1e-4·S_H; factor-3 R̄
definition difference). DIAG-04 candidates 2 and 4 are Moderate-tied
(H-04, H-06 — challengeable context).

### Analysis

**(a) The question's own premise must be split before it can be answered.**
The "Stage-0 zeroing of the conservation weights" holds in the executed run
for λ_L only; λ_E ramped to 1.0 with λ_phys and stayed there (SV-1). So the
executed pilot is evidence about a recipe with an *active* energy
regularizer whose raw magnitude (~1.7e3–1.6e4) was nonetheless ~3–6 orders
below `loss_phys` across the run — i.e., even with λ_E = 1, the energy term was a whisper in
the trained total. Any answer that engages "the locked Stage-0 zeroing" as the
reason the gate quantity received no training pressure is engaging a premise
the run artifacts contradict on the energy side; the accurate statement is
that the energy term was *weighted in* but *scale-dominated out*, and the
angular-momentum term was weighted out by schedule. Adjudicating whether the
λ_E divergence was sanctioned calibration or config drift is the owner's call
(RG-01); both readings leave the dominance analysis below intact. [FACT-W]

**(b) What the ≈10-order separation is and is not evidence of.** Three
compatible-with-evidence readings, none established:

1. *Faithful reporting of a badly-fit model in a consistent frame.* A
   second-derivative residual through an ω₀ = 30 first-layer SIREN generically
   produces |a′| of order (2ω₀)² ≈ 3.6e3 per unit amplitude before training
   adapts amplitudes; squared and summed, R̄ ~ 1e7–1e10 is the *expected*
   scale of an unconverged network's residual, while Huber-δ=1 data loss on
   O(1) scaled positions is bounded near ~|error|. Under this reading the gap
   is a property of underfit + squared-vs-Huber loss forms, not of
   mis-normalization, and it would shrink as fit improves. [R-HYP; network.py
   ω₀ = 30 FACT-W]
2. *Frame inconsistency inflating the residual floor* (the SV-4 mechanism):
   if the executed raw-frame targets are inconsistent with the scaled-frame
   residual operator, the residual cannot vanish even at a perfect data fit
   (≈99·force on truth), and data vs physics become structurally opposed —
   dominance then reflects an unsatisfiable objective, not emphasis. [R-HYP,
   checkable]
3. *Intended physics-first dominance.* λ_phys = 1 is the locked default; the
   Phase-35 contract explicitly **rejected** the high-energy-weight cap-table
   replacement and deferred automatic dominance reweighting "until measured
   weighted-loss/gradient evidence exists" (Excerpt 5 [FACT]). Under this
   reading, dominance is the design, and the missing item is the mandated
   gradient evidence, not a new weighting. 

The three readings make different predictions and are separable by cheap,
train-free computations (below). Note also that "the 10-order gap" is
measured between a causally-collapsed physics value (≈R̄₁/16, SV-2) and a
32-trajectory Huber mean — both ends of the comparison are recipe-specific
statistics, not canonical term magnitudes. [R-HYP]

**(c) Loss values are the wrong units for the dominance question; the locked
contract itself says what the right units are.** Gradient shares decide what
the optimizer follows. The data term's Huber form bounds its per-point
gradient; the physics term is an unbounded squared form; the IC term is a
squared anchor of magnitude ~3e3–8.7e4 [FACT-W log]. The Phase-35 precondition
("log weighted losses, scheduled weights, and gradient statistics" before any
control law — Excerpt 5) is precisely the missing measurement: the pilot
logged one global pre-clip norm (SV-5). Any weighting/balancing answer that
precedes per-term gradient-norm evidence would be repeating the step the
locked spec already refused. [FACT + R-HYP]

**(d) The normalization sub-facet has a concrete, decidable core.** Beyond
tanh-input/LayerNorm generalities (which DIAG-04 already noted as contradicting
evidence for H-06), the worktree pass isolates specific, testable normalization
questions: (i) does the executed data-target path implement §3.1's
`r′_true = r_true/D` (SV-4 says no /D is applied on the training path, while
the Phase-38 probes that validated the residual operator did scale — this is
either an implementation divergence from a locked formula or a deliberate
identity if the corpus is pre-scaled; RG-02); (ii) the training-loss energy
floor `ε_H = 1e-4·S_H` is implemented as a per-anchor `|h0|·1e-4` stand-in
(SV-6, RG-03); (iii) the implemented R̄ is (1/9)Σ‖f‖² vs the locked (1/3)Σ‖f‖²
(factor 3 inside the causal exponent; SV-6, RG-04); (iv) the IC velocity
anchor compares a du-derivative to a raw dt-frame velocity (SV-4). Each is a
place where "normalization/data-scale mismatch" stops being a vibe and becomes
an inspectable equation. None of these observations is a remedy
recommendation; each is a candidate *cause locus* for the owner to weigh.

### Trade-offs between plausible positions

- **Dominance is intended; keep λ ≡ (1,1,1,λ_E^max,0) and gather the mandated
  gradient evidence first.** For: spec-conservative; Phase-35's rejection of
  reweighting-without-evidence is itself locked normative text. Against: if
  reading 2 in (b) holds, no λ vector fixes an inconsistent frame, and
  gradient statistics alone won't reveal that — the frame checks in (e) are
  the decisive complement.
- **Dominance is an artifact to be balanced (λ- or scale-side).** For: the
  gate quantity is energy drift; a training signal ~4–5 orders below the
  physics term (even at λ_E = 1) cannot express gate preference; balancing
  would let conservation terms speak. Against: the loss catalog and the
  ≤1 conservation-weight cap are locked (Excerpt 4/5); "balance" via λ_E>1 is
  spec-forbidden, and balance via residual rescaling is a spec change to §3.2;
  moreover under causal collapse the physics term's *effective* content is
  R̄₁ only — rebalancing against a collapsed term may just re-weight noise
  (SV-2). Any such change is owner/spec territory; this report only maps it.
- **Treat the sub-facet as primary: verify frames/scales before any weighting
  question.** For: reading 2 is the only one of (b)'s three that makes the
  weighting question moot, and it is the cheapest to falsify (below). Against:
  if the frame checks come back clean, this path spent time confirming the
  status quo — though that confirmation itself retires H-06's strongest form.

### Evidence that would distinguish intended dominance from harmful weighting (structure only; owner-gated proposals)

1. **Residual-on-stored-targets check (train-free, decisive for (b)-2):**
   evaluate the coded residual operator on ground-truth arrays exactly as the
   training path serves them (raw), and again under the §3.1 scaled
   convention (as the Phase-38 probe did). Near-zero in one frame and
   ~(T²−1)·force-scale in the other settles the executed-frame question by
   computation, with no training and no held-out access. Pass/fail structure:
   the frame in which the residual vanishes on truth is the frame the
   operator is consistent with; the frame the targets are actually served in
   is then either the same (H-06's frame form retired) or different (a
   concrete, spec-cited inconsistency for owner adjudication).
2. **Perturbation response curve:** residual magnitude vs controlled position
   noise around truth, giving the expected R̄ at the observed data-loss level;
   compares against the observed 1e8–1e10 to test reading 1 quantitatively.
3. **Per-term gradient statistics** (the Phase-35 precondition) over a short
   authorized run or from checkpoint back-analysis: shares of ∥∇θ∥ by term,
   before/after clip — the direct dominance measurement the loss values proxy
   badly.
4. **λ-weighting / balancing ablation on the population** (the DIAG-04
   proposed test) — only after 1–3, since its interpretation is conditional
   on frame consistency and on gradient (not loss) shares. All four are
   proposals for owner authorization; none is run or promised here.

**Claims relied on:** F-07, F-08, F-09; H-04, H-06 as challengeable context.
Worktree: SV-1, SV-2, SV-4, SV-5, SV-6; pinn_architecture.md §3.1/§3.2/§3.4;
preprocessing.py; adapter.py; batches.py; overfit_probe.py; residual_probe.py;
38-VERIFICATION.md; network.py. No H-row treated as established. (Where this
section reasons from H-06's territory it does so to *test* it, per the
master's §3 instruction.)

---

## Q4 — Stage-0 curriculum pacing

**The question.** Within the Stage-0 budget, how should curriculum stage
progression and the PHYS-05 weight ramps be paced relative to each other, and
what evidence bears on whether the current pacing is appropriate for gate
compliance?

### Evidence base

λ_phys reached 1.0 at step 31 in all runs (F-08); the recipe is Stage-0-only
under cumulative replay (Excerpts 2–3 [FACT]); PHYS-05 re-warmup applies at
stage boundaries (Excerpt 5). Worktree: I_warm = floor(0.1·300) = 30 exactly
matches the observed step-31 saturation (`scheduled_weights.py` [FACT-W]);
the run's stage never changed (stage 0 at all steps; HALT at 300, SV-6); the
CURR-03 stage-exit gate is a four-criterion conjunction, all thresholds
provisional pending exactly this pilot's calibration (ctl_instruction.md
≈ 1922–1998 [FACT-W]); `front_idx` — named in the master's "what a complete
answer specifies" — is the *causal-front* index in the step log, and it
stayed 0 at every step of every run (SV-2 [FACT-W]; the term does not appear
in the specs, RG-05). No DIAG-04 candidate maps 1:1 to this question (master
§4 Q4).

### Analysis

**(a) In a Stage-0-only run there is no stage progression to pace; the
realized "curriculum" is entirely intra-stage, and it has three actual axes.**
(i) *Weight pacing*: the λ ramp — 10% of the budget by locked formula, done at
step 31, energy included at weight 1.0 per SV-1. (ii) *Time-domain pacing*:
the causal weighting is, functionally, a within-trajectory curriculum over
time — and its front never advanced past the first of 16 collocation times
(SV-2). (iii) *Optimizer-phase pacing*: Adam→L-BFGS, of which the second
phase received zero budget (SV-6). Of these, only (i) behaved as the nominal
schedule describes. The pilot's realized pacing was therefore: full-strength
five-term objective from step 31, physics supervision confined to the
earliest sampled time throughout, no polish phase, HALT at the budget wall
with the ADVANCE gate unmet by roughly eleven orders on its physics criterion
(final validation total 7.85e7 — phys-dominated per SV-5 — against the
provisional ε_phys = 1e-4). [FACT-W]

**(b) The ramp-vs-collapse ordering is the pacing fact the attachments could
not see.** The λ ramp paces how fast the physics term's *weight* arrives; the
causal mechanism paces how far along the trajectory that term's *coverage*
extends. In the executed run the first completed in 31 steps while the second
never started moving. Whether the right reading is "the front is the pacing
mechanism and it correctly refused to advance" or "the front is the pacing
mechanism and it was structurally unable to advance at these residual scales"
is the same fork as Q2(c) — but for Q4 the salient point is that *both*
readings imply the λ ramp is not the operative pacing bottleneck: pacing
questions about Stage 0 are mostly questions about what governs front
advancement (residual scale — Q3's sub-facet; η_c and the deferred clip —
Q2; collocation count 16 — SV-6). [R-HYP]

**(c) Budget coupling makes "pacing within the 300-step budget" partly a
budget question.** I_warm = 0.1·N and cosine T_max = N (SV-3): any
budget change re-paces the ramp and the LR decay simultaneously (Q1(b)). A
pacing answer "within the 300-step budget" holds those fixed by definition —
in which case the free pacing surfaces are the causal mechanism's parameters
(owner/spec-gated), the collocation budget (16 executed vs ~4096 provisional
canonical, SV-6), the replay budget (32 executed vs 240 canonical), and the
Adam/L-BFGS split. It is a fact worth surfacing that the executed pilot's
batch/collocation topology sits far below the canonical provisional contract
(SV-6) — the pilot paced through a much sparser sampling of the stage than
the batch contract describes, which bears on whether "Stage-0 pacing" as
executed is the thing the spec's pacing was designed for. [FACT-W]

**(d) The stage-exit machinery behaved as locked, and its calibration is
explicitly this pilot's job.** HALT (not a silent advance) is the contracted
outcome for an unmet gate at budget exhaustion; CURR-03's thresholds are
provisional "pending FUT Stage-0 pilot calibration" [FACT-W]. So the pacing
question has a governance edge: the pilot was, by spec text, supposed to
*produce* the calibration for these pacing-relevant thresholds; a research
answer should treat ε_phys/ε_energy/patience values as open calibration
outputs, not as constraints to pace against.

### Trade-offs between plausible positions

- **Pace by residual-earned progression (trust the causal front).** For:
  internally consistent with the locked causal default; front_idx is already
  logged, giving a natural pacing observable; no new mechanism. Against: at
  observed residual scales the front is immobile (SV-2), so "earned
  progression" degenerates to "no progression" for the whole budget; pacing
  by an observable that never moves provides no control.
- **Pace by schedule (λ ramps and fixed fractions, as PHYS-05 does).** For:
  deterministic, budget-coupled by locked formula, and demonstrably executed
  as written. Against: the executed evidence shows schedule-paced weights
  arriving long before the objective's coverage (front) or the data fit is
  ready to use them — the spike steps land *after* full weights on a collapsed
  objective; whether that ordering helps or hurts gate compliance is exactly
  what the retained evidence cannot resolve.
- **Pace by gate-aligned observables.** For: the gate is max-over-time drift;
  a pacing rule keyed to time-resolved drift/residual profiles (which times
  are "learned") would connect pacing to the gate's own structure. Against:
  requires the Q2/Q3 instrumentation first; risks inventing a new mechanism
  where the locked spec already has two (ramp + causal front).

### What a complete answer specifies (structure only)

The joint timeline — lr(step) [locked cosine], λ(step) [locked ramp],
causal-front trajectory front_idx(step), collocation/replay budgets, and the
Adam/L-BFGS split — stated together as one pacing object; the observables that
show whether pacing helps gate compliance: front_idx traces,
residual-by-time-bin profiles (`residuals_bin_*` already exist in the TB
stream, SV-5), per-term weighted-loss and gradient shares over the ramp
window, and a training-side max-over-time drift proxy sampled at a
pre-registered cadence; and the decision rule for what "pacing is
inappropriate" would look like against those observables (e.g., weights
saturating while coverage/front and drift-proxy remain unmoved — stated as a
*form*, with thresholds left to owner calibration per CURR-03's own
provisionality). A curriculum-pacing/stage-progression study (the master's
proposed direction) stays a proposal requiring owner authorization; this
report neither runs nor promises it.

**Claims relied on:** F-07, F-08, F-10; Excerpts 2, 3, 5. Worktree: SV-1,
SV-2, SV-3, SV-5, SV-6; curriculum.jsonl; stage_exit.py; ctl_instruction.md
≈ 1922–1998. H-rows: none required; candidates 2–5 touched only as
cross-cutting context per the master. No H-row treated as established.

---

## Q5 — Evaluation policy (governance / evidence design only)

**The question.** If a future held-out evaluation were ever authorized, what
evidence, governance, and acceptance structure would it require, given that
the current evaluator budget is exhausted and the population fails the gate
under any aggregate statistic?

This section proposes no evaluation and requests none; it specifies the
structure a future, owner-authorized evaluation would need. The exhaustion
record is taken as binding: two failed attempts plus one completed FAIL, all
audited; "the final invocation regardless of outcome; it must not be retried";
any later evaluation "requires a new, explicitly changed owner policy and a
separately governed evidence boundary" (run-evidence-bundle.md Group 3; F-01).

### Analysis — what the audited history teaches the future policy

**(a) The budget was largely consumed by wiring, not science.** Attempts 1
and 2 failed on a missing `blacklist_path` and an MPS float64 conversion —
infrastructure faults — with attempt 2's exposure honestly recorded as
ambiguous ("held-out split records and predictions were likely processed"
before failure) (Group 3 [FACT]). A future policy must decide *in advance*
how infrastructure failure interacts with budget: the strict reading (any
invocation consumes budget — the current single-use machinery encodes this at
the artifact level via an exclusive-create attempt claim that is "intentionally
never removed", `pinn/evaluate.py` [FACT-W]) prevents retry-shopping but
spends scientific budget on dtype bugs; a lenient reading (pre-data-access
failures don't consume) requires a bright-line, auditable definition of
"held-out data touched," which attempt 2 shows is genuinely hard to draw
after the fact. A middle structure the history itself suggests: mandatory
pre-flight of the *entire* evaluator path on synthetic or training-side data
under the frozen config (both observed failure modes — config wiring and
dtype conversion — are of the kind such a pre-flight plausibly surfaces
[R-HYP]), with the held-out
invocation authorized only after a green pre-flight, and the existing digest
verification (the three input digests were verified before attempt 3 [FACT])
retained as the immediate pre-invocation step. Posed as structure; the
strictness choice is the owner's.

**(b) The current held-out set is analytically consumed beyond the budget
ledger.** Its per-trajectory distribution is published in the attachments
(F-03) and its identity is pinned (splits_sha256, Group 1). Any
recipe change motivated by DIAG-01's distributional facts is, weakly but
irreducibly, fit to that set. A future policy therefore faces a fork:
**fresh draw** (stronger inference; requires the admitted-set governance to
support carving a second, never-touched test split — whether enough admitted
data exists for this is not stated in the attachments, RG-06) vs **reuse with
pre-registration** (cheaper; requires treating the published statistics as
prior knowledge and pre-registering the decision rule before invocation to
cap adaptive-overfitting concerns). A hybrid (reuse for infrastructure
pre-flight is impossible — reuse touches the set — but a *sequestered subset*
policy could stage exposure) is also available. Trade-offs, not a
recommendation.

**(c) Selection policy must be pre-registered next time.** The evaluated
checkpoint was seed 42's `best.pt` — best.pt is selected by lowest validation
total (a phys-dominated, single-anchor statistic; SV-5 [FACT-W]), seed 42 was
the seed with the healthiest validation ("Healthy validation for seed 42",
Group 3), and seed 42's validation split is byte-identical to the smoke's
(F-14). No attachment states the rule by which that seed/checkpoint was
chosen for the sole invocation (RG-07). A future evaluation's evidence value
depends on fixing, in advance: which seed(s), which checkpoint-selection
statistic (and whether it is gate-aligned at all — the current selector is
not), and whether the held-out verdict is claimed for "the recipe" (then the
seed must be pre-registered or multiple seeds evaluated) or for "this
checkpoint" only.

**(d) Acceptance structure under a locked worst-case-max gate.** The gate
statistic is locked: worst-case max over trajectories, strict-inequality
reject at 1e-5, non-finite ⇒ FAIL (F-15; Excerpt 1; gate_metrics.py enforces
max-aggregation and honest NaN propagation [FACT-W]). Given verdict-neutrality
at the population's current state (F-02), a future evaluation designed only to
re-render PASS/FAIL has low information value unless preceded by evidence
that the gate quantity has plausibly moved ~5+ orders. Structure a future
policy can specify without touching the gate: (i) *pre-conditions* — a
pre-registered training-side evidence bar (offline drift proxies on
train/validation data, tail-focused because the gate is a max: p99/max
proxies, not means) that must be met before the invocation is authorized;
(ii) *graded evidence readout* — the locked per-trajectory band vocabulary
already exists (Excellent ≤ −10; Acceptable (−10,−6]; Marginal (−6,−5];
Reject > −5, Excerpt 1), so metrics.json's per-trajectory array can be
band-histogrammed to make even a FAIL informative for the next decision,
without altering the pass rule; (iii) *artifact completeness* — per-trajectory
SCS was not persisted last time (F-05); a future run should pre-register the
full artifact schema (per-trajectory eps_H *and* bands, aggregate, receipts,
digests) so no follow-up forensics is blocked; (iv) *invocation-count and
failure semantics* fixed in advance per (a).

### What a complete answer specifies (structure only)

A future-evaluation charter with: the new owner policy statement that
supersedes the exhaustion record (explicitly, in writing, per Group 3's own
language); the evidence boundary (fresh-draw vs pre-registered-reuse, with
data-governance implications resolved); the pre-flight and
budget-consumption rules for infrastructure failure; pre-registered seed,
checkpoint-selection, and cadence rules; the pre-condition evidence bar on
training-side, gate-aligned, tail-focused proxies; and the readout schema
(bands + per-trajectory artifacts) — all fixed before any invocation. Nothing
here proposes running one now.

**Claims relied on:** F-01, F-02, F-03, F-05, F-14, F-15; Group 1–3 of
run-evidence-bundle.md. Worktree: evaluate.py single-use machinery;
gate_metrics.py; SV-5. H-rows: none. No H-row treated as established.

---

## Q6 — Dual-epsilon safety on the admitted set (owner-added spec-verification question)

**The question.** What evidence and acceptance structure would confirm that
the locked dual-epsilon choice (`epsilon_train = 1e-5` vs
`epsilon_inv = 1e-10`) is safe on the admitted set — i.e., that the
train-vs-validate softening gap does not move any stage label or trip any
validation gate differently at close encounters?

### Evidence base

Locked facts: `ε_train = 1e-5` softens the training-loss distance (residual
force and matched-Plummer training Hamiltonian, Excerpt 4 §3.2/§3.4);
`ε_inv = 1e-10` softens the admission gate and the held-out gate (Excerpt 1;
metrics.md in Group 1); the two agree to ~10 digits at ordinary separations
and diverge only at the tightest encounters; the choice is locked (v1.6) and
was ratified on first-principles/lock-consistency grounds without a measured
sensitivity study (master §4 Q6). Admitted-set geometry: Stage-0/1 requires
`s_min > s_0` with interim `s_0 = 0.01` **in scaled code units**; the frozen
sampling envelope has scaled `s_min ∈ [0.015, 0.084]`; Stage 6 catches
`s_min < 0.5` OR `|E| < 0.01` (Excerpts 2–3; ctl_instruction.md ≈ 97–128, 257
[FACT-W]). Worktree consumer inventory (which computation uses which ε, and
in which frame):

| Consumer | ε used | Frame | Source [FACT-W] |
|---|---|---|---|
| Admission gate `eps_H`/SCS on ground truth | 1e-10 | raw parsed arrays (per locked convention) | Excerpt 1; ctl ≈ 565–580 |
| Stage-label invariants (E, Q, s_min, L/Lmax) | 1e-10 | **scaled, gauge-fixed initial state** | preprocessing.py ≈ 237–255 |
| Training residual force | 1e-5 | network/scaled convention (see SV-4) | physics_residual.py; constants.py |
| Training energy loss H_ε | 1e-5 | same as residual | loss_catalog.py `soft_energy_loss` |
| Held-out gate H(t) on predictions | 1e-10 | model-output frame, CPU float64, FD velocities | gate_metrics.py; evaluate.py |

No DIAG-04 candidate maps here (the question post-dates the diagnosis).

### Analysis

**(a) First-principles size of the divergence, at the admitted set's own
geometry [R-HYP arithmetic, illustration only].** For a Plummer pair term,
the relative potential perturbation between the two softenings at separation
r ≫ ε_train is ≈ (ε_train² − ε_inv²)/(2r²) ≈ 5×10⁻¹¹/r². At the interim
Stage-0 floor s₀ = 0.01: ≈ 5×10⁻⁷. At the frozen envelope's tightest
admitted encounter (0.015): ≈ 2.2×10⁻⁷. Three locked reference scales sit
around these numbers: the reject threshold 1e-5 (one-plus orders above), the
Acceptable/Marginal band edge 1e-6 (within one order), and the Excellent band
edge 1e-10 (three-plus orders **below**). Read against the question's own
framing: at admitted separations the dual-ε gap appears comfortably inside
the *reject* margin but is **not** small against the finer band edges, and
Stage-6's `|E| < 0.01` catch-all shrinks the |H₀| denominators that normalize
drift, amplifying any ε-induced shift for exactly the trajectories with the
tightest encounters. This is the quantitative reason the owner's proposed
census-by-stage is the right shape: the risk is stage-graded by construction.
(These arithmetic illustrations set no acceptance number; the locked
thresholds themselves are the only numeric anchors used.)

**(b) The verification design needs an ε-*frame* audit, not just an ε-value
audit.** The inventory above shows the two ε values are applied in three
different frames: raw arrays (admission), scaled initial states (stage
labels), and model-output/prediction series (held-out gate). A nominal length
1e-10 is a different physical length in raw vs scaled coordinates (factor
D ≈ 4.64). The locked text asserts band-decision invariance to raw/scaled
units for the admission check under the global scaling H′ = D·H (Excerpt 1),
which covers the admission gate; it does not by itself state the frame
convention for every other consumer. A safety confirmation should therefore
enumerate each consumer's (ε, frame) pair — the table above is a starting
inventory from code — and confirm each matches its locked intent, because a
frame slip changes the *effective* softening by ~4.64× and hence the
divergence-band population. (This interacts with SV-4/RG-02 but is separable
from it.) [FACT-W inventory; R-HYP significance]

**(c) Two label/gate surfaces are ε-sensitive in structurally different
ways.** (i) *Threshold-adjacent labels*: a stage label or band label moves
only if the trajectory sits within the ε-induced shift of a locked boundary
(E near −0.5/−0.1/|E| = 0.01; s_min near s₀ — s_min itself is
softening-independent geometry, but E and Q are potential-dependent). The
census therefore needs, per stage, the *distance-to-boundary distribution*
of E/Q, not just counts in a separation band. (ii) *The QUARANTINE rule*:
Excerpt 1's "|H(0)| numerically near zero ⇒ QUARANTINE, no denominator
floor" has no quantified "near zero" anywhere in the gate clause
(ctl ≈ 565–580 [FACT-W]; RG-08) — an ε-induced |H₀| shift near that
unquantified boundary is a *gate-path* change (scored vs quarantined), which
is exactly the kind of "trips a validation gate differently" event the
question names. Stage-0's `E < −0.5` keeps its members far from this surface;
the exposure concentrates in the Stage-6 catch-all. [FACT-W + R-HYP]

### What the evidence and acceptance structure would be (structure only; owner-gated proposal, per the master's Q6 direction)

1. **Census:** on the admitted set, per curriculum stage: the distribution of
   minimum pairwise separation over each full trajectory (not just s_min at
   t=0, since the gate integrates over t); the count of trajectories whose
   tightest encounter enters the divergence band — with the band *defined
   relative to locked thresholds* (e.g., separations at which the induced
   |ΔH/H₀| perturbation exceeds the finest locked decision edge it could
   move: 1e-10 for band labels, 1e-5 for the reject rule, the E-boundaries
   for stage labels), rather than by any new free parameter; and the
   distance-to-boundary distributions of (c)(i).
2. **Dual computation:** offline invariants (E; admission eps_H/SCS/bands)
   computed under both softenings for every trajectory in the band plus a
   control sample outside it, in each consumer's own locked frame per (b)'s
   inventory.
3. **Movement report at the label/gate level (the acceptance surface the
   owner asked for):** for each consumer — admission verdict
   (admit/Marginal/QUARANTINE/reject), band label, stage label — the count of
   trajectories whose *decision* changes between softenings. Pass structure:
   zero decision movements confirms safety on the admitted set as-is; any
   movement is itemized with its distance-to-boundary and stage.
4. **Reopening decision rule (structure):** pre-register, before running, what
   movement pattern would warrant surfacing the locked choice for owner
   review — e.g., any admission-verdict or stage-label movement at all vs
   band-label movement only vs movement confined to QUARANTINE-boundary cases
   — and record the chosen rule in the gap register either way. The rule's
   content is the owner's; its pre-registration is the structural
   requirement.
5. **Frame audit:** the (ε, frame) inventory of (b) confirmed against locked
   intent for all five consumers, since a frame slip silently rescales
   everything in 1–4.

This design runs nothing now (SCOPE-23) and sets no numeric bands beyond the
locked thresholds it reuses; both operationalizations of "divergence band"
(machine-agreement digits per the master's ~10-digit note, or
locked-threshold-relative as above) are laid out for the owner to choose
between.

**Claims relied on:** F-01, F-15; Excerpts 1–4; master §4 Q6 provenance
block. Worktree: constants.py; gate_metrics.py; preprocessing.py ≈ 237–255;
evaluate.py; ctl_instruction.md ≈ 97–128, 257, 565–580. H-rows: none. No
H-row treated as established.

---

## 7. The DIAG-04 rankings, tested against this report's evidence

Per the master's §3, every `H-` row is agent analysis to challenge. This
section states, per row, whether the verification pass supports, qualifies,
or contradicts it. These assessments are themselves [R-HYP] — inputs to the
owner's consolidation, not adjudications.

- **H-01 / H-03 (population-scale generalization shortfall; Strong; "no
  contradicting evidence").** The *supporting* leg (uniform 1500/1500 failure,
  F-02) is untouched. The *control* leg — "yet the network fits one
  trajectory" — is weaker than the table implies, and the "no contradicting
  evidence" cell no longer reads cleanly: the Phase-38 rung differed from the
  pilot in objective (data-only), LR (constant 1e-4), IC13 (zeros
  placeholder), and — most materially — target frame (D-scaled probe path vs
  raw-frame production path; SV-4), caveats the retained `seed_band.json`
  itself partially records. The uniform failure is equally consistent with a
  population-scale capacity shortfall and with any recipe-level mechanism
  that applies to every trajectory identically (SV-2's collapsed physics
  supervision; SV-4's frame question, if live). Strong support for "the
  failure is population-wide" stands; Strong support for "population *scale*
  is the distinguishing cause" is not established by DIAG-01..03 alone.
- **H-04 (loss-term imbalance; Moderate).** Qualified in both directions. The
  dominance facts (F-07, F-09) hold, and the executed λ vector was not the
  locked Stage-0 vector (λ_E = 1.0, SV-1) — so the pilot does not actually
  instantiate the "conservation weights zero by design" configuration the
  question set describes. At the same time, loss-value dominance remains an
  ambiguous proxy absent per-term gradient evidence (SV-5), which the locked
  Phase-35 contract itself demands before any reweighting conclusion.
- **H-05 (optimization/warmup pathology; Moderate).** Sharpened rather than
  resolved: the spikes are post-warmup events under a clipped Adam
  (SV-2/SV-3), and the standing optimization-level structure is the causal
  collapse (w₁-only supervision for 300/300 steps in all runs), which the
  DIAG-02 evidence recorded (front_idx 0 at spikes) but did not surface. The
  "not catastrophic" contradicting evidence (finite runs) stands.
- **H-06 (normalization/data-scale mismatch; Moderate).** This row gains the
  most: the sub-facet now has concrete, checkable candidate loci — the
  unscaled training-target path vs §3.1's `r_true/D` and vs the probe-verified
  scaled residual frame (SV-4), the per-anchor ε_H stand-in vs `1e-4·S_H`, the
  (1/9) vs (1/3) R̄ factor, and the du-vs-dt IC velocity comparison (SV-6).
  None of these is established as *the* cause; each is a specific equation to
  verify rather than a generic "scale gap" — and the train-free
  residual-on-stored-targets check (Q3(e)1) discriminates directly.
- **H-07 (insufficient budget; Weak).** The Weak ranking leaned on the
  176-step Phase-38 comparator; since that comparator differs from the pilot
  in recipe and frame (Q1(a)), it neither supports nor refutes a budget story
  cleanly. Budget remains confounded — now with recipe mechanisms as well as
  population scale — which argues for the deconfounding design of Q1 rather
  than for moving the rank in either direction.
- **H-02 / H-08 (pre-registered rubric; tie handling).** No evidence found
  against the process claims; the rubric discipline is visible in the
  retained evidence files (pre-registered D-05 criterion in diag01
  [FACT-W]).

## 8. Gaps register

Gaps are numbered RG-nn. "Attachment-silent" means the four attached files do
not state it; "resolved from worktree" means this report answered it from the
repository per the commissioning override, with the citation given;
"silent everywhere" means neither source answers it. Gaps are outputs, not
complaints; several are candidate rows for the consolidated register.

| ID | Gap | Status |
|----|-----|--------|
| RG-01 | **Provenance/authorization of `loss.lambda_e_max: 1.0` in the smoke/pilot configs.** The locked PHYS-05 table sets λ_E^max = 0 for Stage 0; the code marks the caps "provisional, config-overridable… never cited as ratified"; the configs set 1.0; the run executed 1.0 (SV-1). No attachment mentions it; 43-CALIBRATION's ratification record covers guards/retries/checkpoint-ceiling only. Whether λ_E^max = 1.0 was an owner-sanctioned calibration choice or unratified drift is **silent everywhere** and materially affects how Q3's "Stage-0 zeroing" premise should be consolidated. | Attachment-silent; worktree establishes the fact of the divergence, not its authorization. |
| RG-02 | **Executed target-frame vs §3.1's `r′_true = r_true/D`.** The production data path serves raw parsed positions as targets while IC13/masses are gauge-fixed/ordered, and the probe-verified residual frame is the scaled one (SV-4). Whether the raw corpus units make this an identity (corpus pre-scaled) or a live inconsistency is **not determinable from the worktree** (corpus payload gitignored/absent). The train-free check in Q3(e)1 would settle it. | Attachment-silent; worktree establishes the code path; data-level truth unresolved. |
| RG-03 | **Training-loss ε_H implemented as per-anchor `|h0|·1e-4 + 1e-12`, not the locked `1e-4·S_H` (S_H = median_train(K0+Uabs0)).** Code comments flag it as provisional ("no S_H pipeline exists yet upstream"). Not mentioned in any attachment. | Attachment-silent; resolved from worktree (controllers.py ≈ 30–36, 478–482). |
| RG-04 | **R̄ factor: implementation uses mean over 9 components ((1/9)Σ‖f‖²) where §3.2 locks (1/3)Σ‖f‖².** Factor-3 inside the causal exponent and physics loss. Immaterial at observed magnitudes [R-HYP], but it is a locked-formula divergence. | Attachment-silent; resolved from worktree (controllers.py ≈ 534). |
| RG-05 | **`front_idx` is undefined in the attachments and the specs.** The master's Q4 asks how "stage / front_idx progression" should be paced, but the term exists only in the implementation (largest causal-weight index > 0.5). | Attachment-silent; resolved from worktree (controllers.py ≈ 570–572). |
| RG-06 | **Whether admitted data exists to support a fresh held-out draw** (Q5's fresh-vs-reuse fork). Population counts by split are not in the attachments; splits.json was not parsed for this report. | Silent in attachments; unresolved here (checkable in worktree; not needed for the structural answer). |
| RG-07 | **The selection rule that made seed 42's `best.pt` the sole evaluated checkpoint.** best.pt's selector (lowest validation total) is code-visible, but why seed 42 rather than 41/43 carried the one authorized invocation is stated nowhere. | Silent everywhere (43-VERDICT reports the fact, not the rule). |
| RG-08 | **"Numerically near zero" |H(0)| (QUARANTINE trigger) is unquantified** in the gate clause; the locked text simultaneously forbids a denominator floor. Interacts with Q6's movement census at the Stage-6 catch-all. | Silent everywhere (ctl ≈ 565–580 checked). |
| RG-09 | **Which λ^max values in PHYS-05 are locked vs "default".** Excerpt 5 presents the schedule inside a bundle labeled "authoritative locked spec — hard constraints," yet the same text calls λ_phys^max(k)=1 a "default," the Phase-35 annotation retains the schedule with `λ_E^max ≤ 1` as the cap, and the implementation treats the per-stage values as config-overridable provisional defaults. The lock boundary (schedule *form* + ≤1 cap locked; per-stage values calibration-open?) is not stated crisply anywhere. This is the governance question underneath RG-01. | Ambiguous in attachments; worktree shows the implementation's reading; not adjudicated. |
| RG-10 | **Per-term gradient statistics were never logged** although the locked Phase-35 contract names them the precondition for any dominance/reweighting decision (Excerpt 5). The pilot's 27-field log has one global pre-clip norm (SV-5). An instrumentation gap, not a data gap. | Attachment-silent as a gap; resolved from worktree (step_log.py fields). |
| RG-11 | **The causal-exponent clip bound remains deferred in spec and unimplemented in code**, and at pilot residual scales the un-clipped exponent collapses all but the first collocation weight for the entire run (SV-2). The spec's own "surface a gap if one is needed" condition (Excerpt 5) appears to have been met by the pilot; no attachment surfaces it. | Attachment-silent; resolved from worktree (loss_catalog.py; ctl ≈ 1773; train.log.jsonl). |
| RG-12 | **Frame convention per ε_inv consumer** (raw vs scaled vs model-output frame) is stated only for the admission check (raw, with the H′ = D·H invariance note). The stage-label invariants use the scaled frame (code-verified); the held-out gate operates on model outputs whose frame is whatever training induced (RG-02-dependent). A one-page locked inventory would close this. | Partially resolved from worktree (Q6(b) table); locked-intent statement silent. |
| RG-13 | **Trend/plateau definition for budget decisions.** F-12's 1/3-vs-2/3 disagreement traces to two legitimate definitions over three validation points; no source designates one for future budget rules. | Silent everywhere; both definitions documented (train.py; diag03). |

## 9. Compliance statement

- **No remedy is recommended anywhere in this report.** Where the evidence
  isolates a candidate mechanism (SV-1, SV-2, SV-4, SV-6), it is posed as a
  fact-plus-readings for owner adjudication, with discriminating checks
  stated as owner-authorization-gated proposals (SCOPE-23/D-14 posture).
  No experiment, training run, or evaluation was executed, commissioned, or
  promised.
- **No `H-` row is treated as established.** H-rows are cited only as
  hypotheses (Q1–Q3 context; §7 challenges). New interpretive claims
  introduced here are labeled [R-HYP] and carry the same non-established
  status.
- **Locked spec is treated as a hard constraint.** Where executed artifacts
  diverge from locked text (SV-1, RG-02/03/04), the report says so explicitly
  and overrides neither side; where this report's answers touch spec-owned
  surfaces (η_c, clip bound, λ caps, LR schedule), it maps the decision space
  and leaves the decision to the owner.
- **Source-access deviation is disclosed** (§0): the commissioning prompt's
  codebase-access override of the master's "attached files only" clause was
  used, read-only; every worktree-derived claim is labeled [FACT-W] with a
  file citation so the owner can re-verify each independently. Repository
  files were not edited.

*End of report. Prepared for consolidation with other agents' trainex-r2
reports; all per-question sections list the F-/H- rows and worktree sources
relied on.*
