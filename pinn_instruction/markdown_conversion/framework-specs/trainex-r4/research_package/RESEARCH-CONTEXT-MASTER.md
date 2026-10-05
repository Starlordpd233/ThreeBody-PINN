---
title: Trainex R4 Research Context Master — Stage-0 Causal-Front Stall After the v2.3 Recalibration
package_for: trainex-r4 (single sub-package)
role: the external research agent's single entry point
status: active
created: 2026-10-04
source_baseline: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
self_contained: true
access_mode: open-book
---

# Trainex R4 Research Context Master — Stage-0 Causal-Front Stall After the v2.3 Recalibration

<!-- NEUTRALITY-BAN-BEGIN -->

## 0. The standing of the previous round and of the recipe it produced

This round follows `trainex-r3`, whose consolidated output informed the
v2.3 recalibration ruling (`54-RULING.md`, reproduced in full as Part C of
`v2.3-closure-evidence-bundle.md`). Two things about that history govern how
this round reads it.

**The ruling is a record of what ran; its reasoning is testable.** The
ratified recipe, `A1 + B2 (residual-wide) + C1 + D3 + E1`, is a hard
constraint as a statement of what generation 7 executed. The ruling's own
"scientific basis" paragraphs are analysis written before any run under the
recipe existed, and this packet lists them as challengeable (`H-01`). The
ruling also states its own limit, verbatim: *"this ruling does not claim the
recipe will train or achieve trajectory accuracy."*

**The trainex-r3 reports and resolution doc are prior analysis.** They were
written against initialization-only evidence, before any training run under
the recalibrated recipe. Their findings, including their source-method
identification and their capacity arguments, enter this round as `H-03`: to
be re-derived, not inherited. They live in the repository at
`pinn_instruction/markdown_conversion/framework-specs/trainex-r3/` and are not
attached.

## 1. Orientation

### 1.1 What happened

v2.2's conformant Stage-0 re-run halted because the causal weights were pinned
at the float32 floor from step 0: the unnormalized physics residual at
initialization was about `10¹⁰`. v2.3 recalibrated the causal weighting
against a frozen reference scale `R_ref = 1.9749775821244170e+10`, measured at
initialization, and proved the amended recipe train-free with GATE-04 before
spending a run (`F-12`).

Under that recipe the weights are no longer pinned, and the causal front left
the floor. It then stopped advancing. In generation 7, graded seed 42, the
frozen training-only monitor's front reached bin 2 by step 450 and did not
advance again. Invariant B tripped at step 951, when 501 steps had passed
without a new high-water mark against its `N = 500` window (`F-01`). A replay of
the frozen monitor put the normalized residual summed over bins 0–2 at 1.189 at
the trip, against the 0.693 needed to advance (`F-02`, `F-03`); the verdict
packet reads that as not a near miss (`H-02`).

Under the run's pre-registered rules, seeds 41 and 43 were not launched, and
the single held-out evaluation remains unspent (`F-17`, `F-18`). The owner
rendered the verdict `rethink` and routed this round to carry the verdict
packet's open questions (`58-VERDICT.md`, Part A).

### 1.2 What this round asks

Five questions, transcribed from the verdict packet's §6 in their original
order. That order carries no precedence. §5 states them with what the
evidence already fixes for each. The owner chose the deliverable's shape for
this round: **diagnosis first, then options** (§9).

### 1.3 What this packet does not do

This packet frames questions. It marks no default, orders no option, and picks
nothing; §10 states the check a reader can run to confirm that by inspection.
The external agent's deliverable is a different document governed by §9, and
the bar above binds this packet's voice, never §9's specification of that
deliverable.

The standing bars that bind every agent on this project, in-repo or external:

- no recipe value is tuned against these results without a new owner decision;
- the single held-out evaluation is spent only under owner policy;
- no training run is started;
- no framework specification is edited;
- Stage-1+ and the platform work stay blocked.

`self_contained: true` means this packet states its facts inline so it stands
alone. Under Route B the repository is an additional evidence source, not a
replacement for the package.

## 2. Manifest — what this round contains

**The three uploaded attachments** (ERW Rule 15 caps a sub-package at five):

| # | Attachment | Treatment |
|---|---|---|
| 1 | `RESEARCH-CONTEXT-MASTER.md` — this file | The entry point. §3 fixes how to treat each source, §5 carries the questions, §9 the output contract. |
| 2 | `framework-specs-bundle.md` | Eleven verbatim excerpts of the locked framework specs at the baseline commit: SIREN initialization and the `first_omega_0` record, the skip/power stack, the hyperparameter table, §3.2 with its three Phase 56 contract blocks, the IC loss, the warmup and clip guard, the optimizer split and clipping, Stage 0, the total-loss assembly, the Adam and L-BFGS phases, and the stage transition criteria. **Hard constraint** as a statement of what the contract currently says. |
| 3 | `v2.3-closure-evidence-bundle.md` | Verbatim: the owner verdict (A), the verdict packet with its frozen-monitor replay (B), the recalibration ruling (C), the checkpoint ③/④ ruling (D), the Phase 56 front-index findings (E), and the terminal, trip, and config records (F1–F4). Plus one **derived** digest of the Git-tracked training logs (G), with its exact script and output. |

Each attachment is named here as it arrives on upload. In the repository all
three sit under the round root,
`pinn_instruction/markdown_conversion/framework-specs/trainex-r4/`: this file
and the evidence bundle in `research_package/`, and the specs bundle in
`specs/`.

Files at the round root that are **not** uploaded: `DELIVERY-NOTE.md`
(user-only routing), `RESEARCH-AGENT-PROMPT.md` (pasted, not attached), and
`research_results/` (filled at delivery).

**Route B means the attachments are not the boundary.** They frame the
questions and fix the baseline. The repository, including the full training
logs, checkpoints, and code, is an additional evidence source, and published
literature is a required one (§3).

## 3. Source tiering — how to treat each kind of content

- **Hard constraint (relied on as ground truth):**
  - the locked framework specs as they stand, with their owner-ratified
    contract markers (attachment 2);
  - the owner rulings: `54-RULING.md`'s disposition table, `57-RULING.md`,
    and `58-VERDICT.md`;
  - the run records: terminal state, trip record, configs, and the
    Git-tracked logs and checkpoints under `runs/stage0-v23g7-*` and
    `runs/stage0-v23g6-*`;
  - every `F-` row in §6.
- **Challengeable (to be tested rather than assumed):**
  - every `H-` row in §6;
  - the reasoning sections inside the reproduced documents, including
    `54-RULING.md`'s scientific basis and the verdict packet's "Reading"
    paragraphs and §4 strength column.
- **External published literature (required tier):** the causal-weighting
  scheme in `pinn_architecture.md` §3.2 is not original to this project, and
  the spec's reference list cites no source for it. Literature claims are cited
  by author, title, venue, and year, with the claim stated in the source's own
  terms. Where the literature and this project's formulation differ, the
  difference is itself a finding.
- **Repo-derived evidence (Route-B tier):** a claim derived from the live tree
  arrives as a checkable assertion carrying a `file:line`, not as an
  established fact. ERW Rule 19 requires every such claim to be independently
  verified in-repo, with the verification recorded, before it informs a
  decision.

**Anchor-resolution rule (read before resolving any citation).** Several
copies of each framework spec exist, with different line numbering. Only the
two live files are authoritative:

| Path | Lines | Standing |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | 1116 | **live locked spec** |
| `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | 2162 | **live locked spec** |
| `…/framework-specs/{integrity-r1,integrity-r2,trainex-r1}/specs/*.md` | various | frozen snapshots of earlier rounds — not authoritative |
| `…/framework-revisions/research_reports/{02-…,03-…}/…/specs/*.md` | various | frozen snapshots of earlier rounds — not authoritative |

Resolve every anchor by content against the live file. `pinn_architecture.md`
was edited in v2.3 (Phases 53 and 56), so anchors quoted inside older planning
documents are stale by construction.

Two path moves also matter:

- v2.2's phase folders now live under `.planning/milestones/v2.2-phases/`, so
  a citation of `.planning/phases/50-…` resolves there.
- v2.3's phase folders (53–58) remain at `.planning/phases/`.

## 4. What v2.3 established — the starting state for this round

### 4.1 The recipe that ran

The ratified recalibration (`F-12`) keeps `η_c = 1` and changes what the
exponent consumes. The causal weights are
`w_n = exp(-η_c · Σ_{m<n} stopgrad(R̃_m))`. Here `R̃_b = R̄_b / R_ref`, each
`R̄_b` is the mean over one of 16 fixed equal-time bins, and every training
batch has 4096 collocation rows, 256 per bin. The same frozen `R_ref`
normalizes the training physics loss.

`first_omega_0 = 30` and the clip's underflow-only purpose are recorded as NOT
AMENDED (`F-16`).

The training schedule:

- **Optimizer:** Adam with initial learning rate `10⁻³`, under cosine
  annealing whose length is the Adam budget `n_adam = 1000` (`F-04`).
- **Handoff:** to L-BFGS at budget exhaustion or at a physics-loss plateau
  (`F-05`).
- **Warmup:** the physics weight ramps from 0 to 1 over the first 100 steps.
- **Other weights:** the data and IC weights are 1; the energy and
  angular-momentum weights are 0 (`F-06`).

Invariant B reads one frozen training-only monitor:

- **Front:** the largest bin index `n` with `w_n > 0.5`.
- **Rule:** the front's high-water mark must advance within `N = 500` steps
  (`F-10`).

### 4.2 What the run did

- **The front.** The monitor's front went 0 → 2 by step 450, then stopped;
  at the trip it sat at 2, and earlier it had dropped back to 1 (`F-02`).
  - Moving from front `k` to `k+1` requires the normalized residual summed
    over bins `0..k` to fall below `ln 2 ≈ 0.693`.
  - That sum over bins 0–2 was 1.192, 1.182, and 1.189 at steps 931, 941,
    and 951.
- **Overall progress.** The median normalized bin residual fell 1.7× over the
  run (`F-03`).
- **Learning rate.** It fell from `5.78 × 10⁻⁴` at step 450 to
  `6.16 × 10⁻⁶` at step 950 (`F-04`).
- **Loss terms.** The IC term dominates the logged total loss at every
  completed step: it is at least 236 times the weighted physics and data terms
  combined (`F-07`).
  - It ranged from about `10²` to about `10⁵` across the tabulated steps, and
    from 25.7 to `1.77 × 10⁵` over all 951 completed steps. It moved sharply
    from step to step.
  - The normalized physics term ranged from 0.0733 to 0.192 at the
    tabulated steps, and from 0.0723 to 0.257 over all completed steps.
- **Gradients.** On the 19 steps with complete gradient statistics, the
  applied IC gradient norm exceeded the applied physics gradient norm by
  factors between `2.78 × 10⁴` and `2.62 × 10⁶` (`F-08`).
- **Training-batch front.** It ranged over 0–3 and changed 492 times. The
  monitor's high-water mark never passed 2 (`F-09`).

### 4.3 Where the definitions live

The locked framework specs do not define `front_idx`, its `0.5` threshold, or
invariant B's window. Those come from code and owner rulings (`F-10`).

The spec's learning-rate rule says to decay the rate "over the phase" and to
hand off to L-BFGS when the physics loss plateaus. The code ties the cosine
length and the physics warmup length to the configured Adam budget (`F-04`,
`F-05`, `F-06`).

The spec marks the per-stage epoch budget as provisional, pending Stage-0
calibration (`F-15`).

## 5. The framed questions

The five questions are the verdict packet's §6, verbatim. Each has a pointer
to the facts that bear on it and to the gaps §7 records for it. Their
numbering is for reference only.

### 5.1 Q1 — the invariant-B window and the learning-rate schedule

*"Is the coupling between the invariant-B window and a learning-rate schedule
that decays inside it a design flaw, and how should the two relate?"*

- **Bearing facts:** `F-01`, `F-02`, `F-04`, `F-05`, `F-06`, `F-10`.
- **Recorded gaps:** §7 Q1.

### 5.2 Q2 — the front criterion

*"Should the causal-front criterion measure progress relative to
initialization (R_ref) or absolute physical accuracy?"*

- **Bearing facts:** `F-02`, `F-03`, `F-10`, `F-11`, `F-12`.
- **Recorded gaps:** §7 Q2.

### 5.3 Q3 — the SIREN initialization scale and the skip/power stack

*"Is the SIREN initialization scale `ω₀ = 30` (with the deferred power-skip
ablation) the root of the slow pace?"*

- **Bearing facts:** `F-03`, `F-07`, `F-08`, `F-12`, `F-16`.
- **Recorded gaps:** §7 Q3.

### 5.4 Q4 — the Stage-0 step budget

*"What Stage-0 step budget is realistic for the front to cross 16 bins?"*

- **Bearing facts:** `F-02`, `F-03`, `F-04`, `F-05`, `F-15`.
- **Recorded gaps:** §7 Q4.

### 5.5 Q5 — the oscillation between bins 1 and 2

*"Does the front's oscillation between 1 and 2 point at a stability issue the
frozen monitor exposes but the training batches hide?"*

- **Bearing facts:** `F-02`, `F-07`, `F-09`, `F-11`, `F-13`.
- **Recorded gaps:** §7 Q5.

### 5.6 Requirements every answer carries

These constrain the *form* of an adequate answer. They name no value, no
direction, and no candidate.

**(a) Diagnosis before options.** For each question, state:

- the mechanisms the evidence admits;
- what each mechanism predicts for the quantities this package records (the
  replay sums in `F-02`, the logged series in Part G);
- which existing evidence, in the package or the repository, discriminates
  between them.

Where nothing existing discriminates, describe an experiment that would. For
each experiment, say what it measures, what each outcome would mean, roughly
what it costs, and whether it needs a new training run or can be done
read-only on retained checkpoints and logs. Experiments are proposals for the
owner to authorize, never actions.

**(b) The whole telemetry, not only the causal-weight arithmetic.** Account
for the logged loss-term magnitudes and the per-term gradient-norm ratios
(`F-07`, `F-08`), and say whether they bear on the question.

**(c) Quantified against the front-advance condition.** The front moves from
`k` to `k+1` only when the normalized residual summed over bins `0..k` falls
below `ln 2`. Late-bin changes cannot move it (`F-11`). State every
quantitative claim against that condition and against the replay's measured
distances (`F-02`, `F-03`).

**(d) The source method, re-verified.** `H-03` records the source method the
trainex-r3 round identified for the causal weighting. Independently identify
and cite the published method. State what it says, in its own terms, about the
following, and every point at which this project departs from it:

- how its causal parameter is set or scheduled;
- how training progress is expected to move the causal weights;
- how the optimizer schedule interacts with them.

**(e) Independent derivation before comparison.** For every `H-` row, derive
the result yourself first, then state agreement or disagreement with reasons.

**(f) Evidence limits stated.** State what one graded seed and one partly
shared trajectory (`F-13`) can and cannot support. No conclusion may rest on
seed coverage the evidence does not have.

## 6. Claims register

`F-` rows are established evidence a reader may rely on. `H-` rows are prior
analysis to challenge; each carries the label "agent analysis — not
established fact". Run artifacts are cited by repository path; Part letters
refer to `v2.3-closure-evidence-bundle.md`.

### F- rows (established evidence)

| ID | Claim (numbers verbatim) | Source | Status |
|---|---|---|---|
| F-01 | Generation-7 graded seed 42 tripped invariant B at step 951: `metric: steps_since_front_advance`, `value: 501.0`, `threshold: 500.0`, `threshold_provisional: false`; frozen-monitor `front_high_water: 2`, `last_advance_step: 450`; `not_launched`: seeds 41 and 43; `evaluation: preserved-unspent`; run at HEAD `629b1a6c…`. The trip record's `step: 951` is the number of completed Adam updates. The guard tripped on the next iteration, after its forward and backward pass and before its update; that halted iteration is logged as record 952 (`F-07`) | `runs/stage0-v23g7-seed42/failure/trip.json`; `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/terminal-state.json` (Parts F1, F2); `pinn/training/controllers.py:2105-2130` | established |
| F-02 | Frozen-monitor replay. Gen 7 step 0: front 0, bin 0 = 0.875, next weight 0.42. Step 900: front 1 (back from 2), bins 0–1 = 0.728, next weight 0.48. Steps 931 / 941 / 951: front 2, bins 0–2 = 1.192 / 1.182 / 1.189, next weight 0.30 / 0.31 / 0.30. Gen 6 steps 490 / 500 / 510: front 1 (back from 2), bins 0–1 = 0.954 / 0.805 / 0.789. Advancing from `k` to `k+1` needs the sum over bins `0..k` below 0.693 | verdict packet §3 and Appendix A (Part B) | established |
| F-03 | From initialization to step 951, per-bin normalized residuals in bins 0–5 fell 3.5×, 2.7×, 3.2×, 2.2×, 2.1×, 1.5×; the 16-bin median fell 1.7× (1.11 → 0.66); raw bin-0 residual went from `1.7 × 10¹⁰` to `4.9 × 10⁹`; bins 0–5 sum to 3.88 at step 951 | verdict packet §3 (Part B) | established |
| F-04 | The learning rate follows `CosineAnnealingLR` with `T_max = n_adam` and `n_adam: 1000`; logged `lr` 0.001 at step 1, `5.78e-4` at 450, `2.45e-5` at 900, `6.16e-6` at 950, `5.91e-6` at 951. The spec sets `LR_k = 10⁻³ × (0.7)^k` and "a cosine annealing scheduler to decay the learning rate over the phase" | `pinn/training/controllers.py:2658-2660`; `pinn/training/config.py:574`; `configs/stage0-v23g7-seed42.yaml` (Part F3); Part G; `ctl_instruction.md:1803`, `:1805` | established |
| F-05 | The spec hands off to L-BFGS "when the physics loss plateaus". The code hands off at Adam-budget exhaustion or at plateau detection on the physics loss. All 952 generation-7 graded log records (951 completed Adam steps and the halted iteration logged as step 952) are phase `2a` (Adam); L-BFGS never ran | `ctl_instruction.md:1894`; `pinn/training/controllers.py:2040-2042`, `:2169`, `:2201`; Part G | established |
| F-06 | `I_warm = min(2000, 0.1 · N_Adam,k)` and `λ_phys^max(k) = 1` **[LOCKED]**. Logged `lambda_phys` is 0.0 at step 1 and first reaches 1.0 at step 101 (graded) and step 31 (smoke, `n_adam: 300`). `lambda_data` and `lambda_ic` are 1.0 and `lambda_e` and `lambda_l` are 0.0 on every logged step. On every record, `total` equals the λ-weighted sum of the five loss terms | `pinn_architecture.md:699-701`; Part G | established |
| F-07 | Generation-7 graded logged loss terms. At the tabulated steps: `loss_ic` from 84.3 (step 900) to `8.2e+04` (step 200), changing by more than 10× between neighbouring tabulated steps (e.g. 84.3 at 900, 1.54e+03 at 931, 1.91e+04 at 941, 110 at 950); `loss_phys` (after `R_ref` normalization) from 0.0733 (step 951) to 0.192 (step 300); `loss_data` from 0.016 (step 931) to 0.0721 (step 1). Over all 951 completed steps: `loss_ic` from 25.7 (step 947) to `1.77e+05` (step 92), `loss_phys` from 0.0723 to 0.257, `loss_data` from 0.0158 to 0.0769, and `loss_ic` is at least 236 times `λ_phys · loss_phys + λ_data · loss_data` (the smallest ratio, 236.6, is at step 947). The trip record's values, `ic 1905.42`, `phys 0.0794`, `data 0.0163`, belong to the halted iteration logged as record 952, not to completed step 951 (`ic 2.83e+03`, `phys 0.0733`, `data 0.0164`) | Part G and its reading notes; `runs/stage0-v23g7-seed42/failure/trip.json` (Part F2); `pinn/training/controllers.py:2105-2130` | established |
| F-08 | On the 19 generation-7 graded steps with complete gradient statistics (every 50 steps), `applied_ic / applied_phys` ranges from `2.78e+04` (step 900) to `2.62e+06` (step 50); `applied_data` ranges from 1.45 to 5.78. `raw` is the global parameter-gradient L2 norm of the unweighted term; `applied = λ × raw` | Part G; `pinn/training/controllers.py:483-507` (canonical builder), `:1993-2009` (the microbatched Adam path these steps used, provenance `microbatch_pass2_diagnostic`) | established |
| F-09 | Generation-7 graded training-batch `front_idx` histogram over all 952 log records, including the halted record 952: `{0: 342, 1: 381, 2: 194, 3: 35}`, 492 step-to-step changes, first value 3 at step 677. The frozen monitor's high-water mark never exceeded 2. By ruling, a resampled training-batch front is diagnostic only and cannot satisfy invariant B | Part G; `terminal-state.json` (Part F1); `54-RULING.md` "Front-monitoring boundary" (Part C); `57-RULING.md` §2 (Part D) | established |
| F-10 | `front_idx` is the largest `n` with `w_n > 0.5`, computed in code for the frozen monitor and for training batches. Neither locked spec defines `front_idx`, its threshold, or invariant B's window: `pinn_architecture.md` mentions the front only inside the Phase 56 contract block at `:452` (GATE-04's front condition; training-batch front diagnostic only), and `ctl_instruction.md` has no occurrence. `N = 500` and the frozen training-only monitor are an owner ruling | `pinn/training/controllers.py:1058` (monitor), `:1241`, `:1974` (training batch); `pinn_architecture.md:452`; `57-RULING.md` §2 (Part D) | established |
| F-11 | Under the ratified formula, front 0 at initialization is the expected healthy result, and a residual reduction confined to late bins cannot move the front at any magnitude | `56-OPEN-ITEMS.md` Section 2 (Part E) | established |
| F-12 | The ratified recipe `A1 + B2 (residual-wide) + C1 + D3 + E1`: `η_c = 1` on `R̃_b = R̄_b / R_ref`; one frozen `R_ref` = median of 96 initialization bin means from the six-case GATE-04 probe, also applied to the training physics loss; `first_omega_0 = 30`; 4096 rows per batch in 16 equal bins (256 per bin) with one batch-global 16-term prefix; clip unchanged. Governed `R_ref = 1.9749775821244170e+10` (logged `r_ref` `19749775821.24417`). GATE-04 passed on the amended recipe | `54-RULING.md` disposition table (Part C); `pinn_architecture.md:452`, `:454`, `:456`; `pinn/verification/artifacts/r_ref_stage0.json`; Part G | established |
| F-13 | Generation-6 and generation-7 seed 42 share the seed and the configuration apart from `run.run_name`, and ran at commits `ef4764f9…` and `629b1a6c…`. Over steps 1–513: every compared logged field is bit-identical through step 8. At step 9, `w_min` and `loss_phys` differ (first differing digit 5 and 7). Through step 269, differences appear on only 68 steps and only in `loss_phys`, `loss_data`, `w_min`, and `w_mean`; `loss_ic`, `total`, and `grad_norm` stay bit-identical. Every step from 270 onward differs, and the first difference visible at three significant figures is at step 275. Generation 6's monitor high-water mark first reached 2 at step 353 and was still 2 at its last checkpoint, step 510; the process died at step 513. The verdict packet's replay of its checkpoints at steps 490, 500, and 510 found the monitor's instantaneous front back at 1 (`F-02`) | Part G comparison section and reading notes; `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json` (`invariant_b_state` of the step-510 checkpoint); verdict packet §3 (Part B) | established |
| F-14 | The generation-7 smoke (`n_adam: 300`) finished. Its monitor reached front 1 at step 93, the same as generation 6's smoke. Its training-batch front never exceeded 1 | `57-05-SUMMARY.md` "Descriptive record"; `configs/stage0-v23g7-smoke.yaml` (Part F4); Part G | established |
| F-15 | The spec records the per-stage `MAX_EPOCHS` table, the stagnation window, and the percentile-10 relaxation as **claimed-unverified** and "provisional pending Stage-0 pilot calibration". The run used `max_epochs: 1000`, `n_adam: 1000` | `ctl_instruction.md:1994-1997`; `configs/stage0-v23g7-seed42.yaml` (Part F3) | established |
| F-16 | `first_omega_0` is fixed at 30 and not scheduled during training, recorded by Phase 56 as NOT AMENDED. The power-skip stack is a future ablation outside the ratified surface set | `pinn_architecture.md:181`, `:188`; `54-RULING.md` "Scope and sequencing" (Part C); `.planning/milestones/v2.3-GAPS.md` GAP-54-02 disposition | established |
| F-17 | Only seed 42 produced a graded result under this recipe; seeds 41 and 43 were never run | `terminal-state.json` `not_launched` (Part F1) | established |
| F-18 | The single held-out evaluation is preserved unspent; spending it is governed by owner policy | `58-VERDICT.md` (Part A); `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/no-candidate.json` | established |

### H- rows (prior analysis — challenge)

| ID | Claim | Source | Label |
|---|---|---|---|
| H-01 | `54-RULING.md`'s scientific basis, points 1–5, written before any run under the recipe. Among them: applying the frozen normalization to the training physics loss "addresses the established severe physics/data conditioning mismatch" (point 2), and the flat-profile endpoint arithmetic (point 1), which the ruling itself calls illustrative | `54-RULING.md` "Checkpoint ② discharge — scientific basis" (Part C) | agent analysis — not established fact |
| H-02 | The verdict packet's readings: "not a near miss", "the front oscillates; it does not creep", the §4 strength column (including "two independent runs (gens 6 and 7) stalled at the same index", to be read against `F-13`), and the arithmetic that a full front means about a 20× residual reduction with the raw residual still about `10⁹` | verdict packet §3 "Reading" and §4 (Part B) | agent analysis — not established fact |
| H-03 | The trainex-r3 round's output: both returned reports, the consolidated resolution doc, and the Rule-19 verification report. The resolution doc's JOIN-2 records a source-method identification (Wang, Sankaran, Perdikaris, "Respecting causality for training physics-informed neural networks", *Computer Methods in Applied Mechanics and Engineering*), and its JOIN-3 records an unresolved scaling-law dispute on the SIREN scale | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/trainex-r3-resolution-doc.md` (JOIN-2, JOIN-3); `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md` | agent analysis — not established fact |

The register records claims. It does not order them by standing. A claim
whose standing is unclear from the sources belongs in the `H-` table with its
uncertainty stated.

## 7. What the assembled evidence cannot answer

This section records gaps. It does not resolve them. Each entry ends at the
statement of absence.

**Q1 — window and schedule.** The evidence contains one learning-rate schedule
and one window placement. No run under this recipe holds the learning rate
constant, moves the window, or lengthens the schedule. The evidence does not
separate the decaying rate from any other cause of slowing between steps 450
and 951.

**Q2 — the front criterion.** No source records why the threshold is `0.5`
(equivalently, a prefix sum of `ln 2`), and the locked specs do not define the
criterion at all (`F-10`). No measurement relates an `R_ref`-relative front
state to absolute trajectory accuracy, because no evaluation was run at any
front state.

**Q3 — SIREN scale and stack.** No run under this recipe changes
`first_omega_0` or removes the power-skip stack. The two factors' shares of the
initialization derivative scale are not decomposed, and the scaling-law
dispute recorded in `H-03` is unresolved.

**Q4 — step budget.** No run under this recipe goes past step 951. The L-BFGS
phase never ran, and the per-stage budget is provisional by the spec's own
statement (`F-15`).

**Q5 — oscillation.** The frozen monitor is scored only at five generation-7
checkpoints (steps 0, 900, 931, 941, 951) and three generation-6 checkpoints
(steps 490, 500, 510) (`F-02`). Its high-water mark and last-advance step are
kept in the checkpoints and the terminal record, and no per-step monitor trace
exists. The Git-tracked TensorBoard file under `runs/stage0-v23g7-seed42/tb/`
holds per-step training-batch values (the batch front, and the raw and
normalized per-bin residuals), not the monitor's. The relation between the IC
term's step-to-step swings (`F-07`) and the monitor's movement is not
measured.

**Cross-cutting — seeds and independence.** One graded seed exists (`F-17`),
and the two graded trajectories share that seed and their first few hundred
steps (`F-13`).

**Cross-cutting — gradient coverage.** Per-term gradient norms exist only on
the 50-step diagnostic cadence (`F-08`). No per-step or per-bin gradient
decomposition exists.

## 8. Provenance

- **Package baseline (`source_baseline`):**
  `735e2ae8d5ec30b9915ec9172ac06965fbaa8afb`.
  - It is the repository commit at assembly, and the ERW Rule-5 pin for both
    bundles and for every `file:line` in this packet.
  - The two framework specs and every reproduced source are unchanged
    between that commit and the commit that adds this package.
- **Run pins:**
  - Generation 7 ran at `629b1a6ca4462915b6340a59b8d4e3ad8df75d8b`, and
    generation 6 at `ef4764f92d9ad23fa90c936166137944dc5e4aea`.
  - The trip record's SHA-256 is
    `eb350b2985c7f7ee58f21716dd958bd9b4806ecb56474de58a0852fec04863a8`, as
    `terminal-state.json` records.
- **The ERW Rule-20 live-tree pin is not recorded here.** It belongs to the
  delivery note and is filled per engagement, because it records the tree an
  external agent actually saw.

<!-- NEUTRALITY-BAN-END -->

## 9. Output contract

This section specifies the deliverable the external research agent produces.
It is the one section of this packet that uses the vocabulary of marked
defaults, door classification, and decision sheets. ERW Rule 7 requires a
build-design deliverable to carry them, and that vocabulary describes the
agent's document, never this packet's own position.

**Shape (owner-chosen for this round): diagnosis first, then options.**
Produce one research report in five parts, in this order:

1. **Premise-challenge findings, up front (ERW Rule 17).** Test this packet's
   stated premises, every `F-` row, and every reading in the reproduced
   documents against the repository. Report contradictions as first-class
   findings ahead of everything else. An agent that finds a false premise and
   buries it has failed the round.
2. **Diagnosis, per question (Q1–Q5).** Satisfy §5.6. For each question, give:
   - the candidate mechanisms;
   - the evidence for and against each, with labels;
   - what each predicts for the recorded quantities;
   - the discriminating experiments, each proposed as an owner-gated option
     with its cost and whether it needs a training run.

   State a confidence for each mechanism and say what would change it.
3. **Options, per decision.** For each decision the diagnosis exposes, give:
   - an options menu of two to four options, with their mechanical-surface
     trade-offs and their cross-decision interactions;
   - for each option, **which diagnostic outcome it presupposes**;
   - a **suggested default, clearly marked**, on each menu;
   - a **one-way versus two-way door classification** on every suggested
     default and every deviation from it.

   Then add:
   - a fill-in **decision sheet** with columns decision | options | suggested
     default | door type | presupposed diagnosis | owner's pick;
   - a **composed next-run recipe** that assembles the suggested defaults
     into one coherent configuration, as a cross-menu coherence check;
   - a "what the runbook inherits" section.

   Where the right option depends on an experiment's outcome, say so and give
   the branch rather than forcing a single default.
4. **Gaps.** Where the attachments, the repository, and the literature are
   silent or ambiguous, record it (ERW Rule 9). A well-stated gap is a valued
   output.
5. **Claims-and-uncertainty register.** Label every claim by its evidence
   base: package-derived, repository-verified (with `file:line`), literature
   (author, title, venue, year), or your own analysis.

**The Rule 18 read-only bars, in the imperative.**

- Edit no file.
- Start no training run.
- Invoke no evaluation.
- Run no command with side effects, and make no commit.

This project's standing bars apply to external agents exactly as they apply
to in-repo agents: no held-out evaluation, no new training runs, no
framework-spec edits, and no remedy selection. Read-only analysis of retained
logs and checkpoints is permitted. Discriminating experiments are proposed,
never performed.

**The literature requirement.** §5.6(d) is mandatory. A report that answers
only from the repository and the attachments has left the round's required
evidence tier untouched.

**The Rule 19 notice.** Every repo-derived claim arrives as a checkable
assertion carrying a `file:line`. The project verifies each one in-repo, with
the verification recorded, before it informs any decision.

**Suggest defaults; never decide.** The consolidated decision sheet goes to
the owner as a candidate, not a ruling. Any change to a locked value is a
formal amendment requiring an explicit owner re-ratification.

## 10. Neutrality and fidelity self-audit

This section defines the checks the package must pass. It sits outside the
neutrality-ban region because it defines the checks. The results are recorded
in the round's audit report,
`docs/work/reviews/cross_cutting/trainex-r4/2026-10-04-trainex-r4-package-audit.md`,
and are not restated here.

| Check | Scope | Method |
|---|---|---|
| Bar A — scoped lexical ban | the region between the `NEUTRALITY-BAN` markers (§0–§8) | case-insensitive grep for `recommend`, `suggest`, `prefer`, `best`, `most likely`, `primary candidate`, `default to`, `should use`, `ranked`, `leading option`; expected empty |
| Bar A2 — Rule-7 carve-out present | §9 | case-insensitive count of lines matching `suggested default`, `one-way`, `two-way`, `decision sheet`; expected at least 4 |
| Bar B — questions verbatim | §5.1–§5.5 | each quoted question is byte-identical to the verdict packet's §6 bullet text (line breaks normalized) |
| Bar C — read-only boundary | framework specs, `pinn/`, `configs/`, `runs/`, `tests/` | `git diff --stat` over those paths in the package commit; expected empty |
| Bar D — pin consistency | master, both bundles, prompt, delivery note | the `source_baseline` hash is byte-identical everywhere it appears |
| Bar E — bundle fidelity | both bundles | each verbatim block equals `git show <baseline>:<path>` (or its `sed` range); the derived digest's script SHA-256 matches and its output re-derives |
| Bar F — citation resolution | every `path:line` cited in §4–§8 | the cited line exists at the baseline and carries the attributed content |
| Bar G — attachment cap | the prompt's attach list | at most five files |
