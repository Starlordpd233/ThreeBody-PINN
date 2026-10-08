---
title: "Trainex R4 Ruling — the owner-delegated picks on the consolidated decision sheet"
round: trainex-r4
role: "ERW Rule-13 ruling record: the picks on JD-0 to JD-11, the answers to OQ-1 to OQ-5, the experiment authorizations, and the design of the next run"
status: active
created: 2026-10-07
ruling_authority: "owner-delegated on 2026-10-07 to the in-repo agent, Claude Code (claude-opus-5-5)"
decision_sheet: "trainex-r4-resolution-doc.md (commit 53b7c008), section CANDIDATE-SHEET"
ruling_tree_pin: dcaea44667a3b0dfe5a7ca5e2035439f54ee5893
---

# Trainex R4 — Decision-Sheet Ruling

## Authority

- **Date:** 2026-10-07.
- **Owner instruction (verbatim):** *"So, I shouldn't be ruling on anything. I
  think you're more intelligent and informed at these things than I am. So
  proceed to the next thing and let me know what the logical next step is and
  then we can head to that and start tackling it."*
- **What the delegation covers.** The picks on the consolidated decision sheet
  (`JD-0` to `JD-11`), the answers to its owner questions (`OQ-1` to `OQ-5`),
  and which experiments (`JX-1` to `JX-10`) are authorized. Like the owner's
  2026-09-04 delegation (`54-RULING.md:45-46`), it covers this sheet only.
- **What the ruling rests on:**
  - the consolidated document (`trainex-r4-resolution-doc.md`, `53b7c008`);
  - the Rule-19 verification (Part 1 `b4b975e9` and `d97328d4`; Part 2
    `654d6ffe`);
  - the re-framing ruling R-1 to R-7 (`DELIVERY-NOTE.md`);
  - the facts re-read for this ruling, cited where they are used.
- **What it does not do:**
  - It spends no held-out evaluation and authorizes no graded run. Stage-1+
    and PLAT-01..07 stay blocked.
  - It moves no locked value. Three answers need spec text that settles a
    silence or an inconsistency (`JD-1`, `OQ-2`, `OQ-3`). The next milestone
    drafts that text as formal amendments; the owner sees each one and may
    veto it.
  - It reverses no owner ruling. Option A of 2026-09-07, rulings A1 and B2,
    and the graded-run rules of `57-RULING.md` stand.
- **Nothing has run.** The authorizations below take effect in the next
  milestone.

**Citation shorthand.**

- `codex:N` and `claude:N` are lines of `research_results/codex-resolution.md`
  and `research_results/claude-resolution.md`.
- `V:N` is a line of the Rule-19 verification report,
  `docs/work/reviews/cross_cutting/trainex-r4/2026-10-07-trainex-r4-rule19-claim-verification.md`.
- `pinn_architecture.md` and `ctl_instruction.md` are the framework specs in
  `pinn_instruction/markdown_conversion/framework-specs/`.
- `54-RULING.md` is in `.planning/phases/54-recalibration-decision-grounding/`;
  `57-GAPS.md` and `57-RULING.md` are in
  `.planning/phases/57-corrected-re-run-the-preserved-evaluation/`.
- `DELIVERY-NOTE.md` and `trainex-r4-resolution-doc.md` sit beside this file.
  Every other path is relative to the repository root.

## The governing choice: what the next run is for

The sheet's four disputes are whether `JD-2` names a remedy now, and the
defaults of `JD-4`, `JD-6` and `JD-7`. They come down to one question
(`trainex-r4-resolution-doc.md`, JOIN-6): is the next run a narrow control, as
Codex designs it, or an informative pilot, as Claude designs it?

**Ruling.** The next run is the corrected control: the ratified recipe,
executed as specified. It runs in a diagnostic mode. Nothing stops or switches
the run early, and each rule that would have done so is recorded instead.

**Why:**

1. **No conformant run exists yet** (`JG-1`). The first one should answer one
   question cleanly: does executing the ratified recipe as specified restore
   the front's progress? A run that also changed the loss weights, the guard's
   statistic or the optimizer sequence could not pin a change in behavior on
   any one of them (`codex:369`).
2. **Observing instead of halting loses nothing.**
   - The guard's only effect on training is to stop it. A run with the guard
     active is therefore the same run as one with the guard observing, cut
     short (up to floating-point nondeterminism).
   - The observing run records the step at which the ratified rule would have
     halted it. That is the readout Codex's control asks for, and the run also
     shows what happens after that step.
   - The extra cost is at most 500 steps, because the rule cannot halt before
     step 500 of a 1,000-step budget. At about 12 s per step that is about 1.7
     hours.
3. **The same holds for the plateau handoff.** The detector starts L-BFGS
   whenever it fires (`pinn/training/controllers.py:2169`, `:2200-2201`), which
   would end the Adam phase at a different step on each seed. Recording when it
   would fire, without acting on it, keeps the Adam phase the same length on
   every seed and still measures the detector.
4. **More than one seed.** One seed is one batch sequence (P-5), so a single
   run cannot separate the recipe's behavior from the order of its batches.

**What the control gives up.** It does not exercise L-BFGS, and it tests no
rebalancing. Those are later stages. The readout branches below choose between
them, and they are fixed now, before the run.

## The picks

| Decision | Pick | Why | Conditions and consequences |
|---|---|---|---|
| `JD-0` Conformance | **A** | Fixed by the owner's Option A (`57-GAPS.md:214-218`; R-3). Both reports suggest it | Physics rows, the monitor and validation each use their own slot's IC13 and masses. The gate tests what the loss evaluates: perturbing a non-anchor slot's IC13 must change both the physics loss and the IC loss, and the verifier records the IC and mass inputs it evaluated. Then `R_ref` is re-measured and GATE-04 re-run (`pinn_architecture.md:454`, `:456`), followed by the `OQ-1` check |
| `JD-1` The IC term over a batch | **B1**: the mean over the selected slots | The anchored term is biased, not only noisy. The anchor is the batch's lowest-ID replay trajectory (`pinn/training/controllers.py:1075-1079`, over keys sorted at `pinn/data/batches.py:78`), so IC training concentrates on a few trajectories (about 10–40, `claude:1398`). A mean over slots weighs every slot as the data term (`pinn/training/controllers.py:1865`) and the physics bins ("Replacement multiplicity is preserved", `pinn_architecture.md:456`) already do. A mean, not a sum, keeps the scale at which `λ_IC = 1` was ratified | Each slot's term is the spec's per-trajectory `L_IC`, unchanged (`pinn_architecture.md:511-515`), with `λ_IC = 1` and `β_v = 1`. A trajectory selected twice counts twice, as in the physics allocation. B2 and B3 are not adopted. The batch rule enters the spec as a clarifying amendment |
| `JD-2` Loss-gradient balance | **A**, then **B** for the control | Both reports measure before changing a weight (`codex:272`; `claude:1415-1420`). The control keeps the ratified weights because it is the ratified recipe's first conformant test, and R-2 makes the IC dominance a design concern "to be re-measured once the run conforms". Codex's B presupposes that the "owner wants a control" (`codex:277`) | `JX-1` runs first. Its conformant half at initialization is structural evidence and states what the control is expected to show. Adaptive `λ_IC` (C) is the pre-registered arm for readout branch (b); it then goes through amendment (the Phase-35 deferral, `pinn_architecture.md:708`, `:710`, and the `λ_IC` range). D is not adopted: it equalizes loss values, not gradients. E, the hard IC ansatz, stays deferred unless IC hypersensitivity persists after rebalancing. The authors' code puts the IC loss inside the causal exponent (`LR-6`); that design is noted for the rebalancing arm and not adopted, because it would amend the ratified causal-weight definition |
| `JD-3` Front meaning and stage success | **A** | Agreed. A relative front cannot certify absolute accuracy (R-2, structural) | The control reports absolute measures and gates on none of them: raw residuals, the IC position and velocity errors, trajectory errors against the reference data, and the energy drift `ε_H`, on training and validation trajectories. No test-split file is opened. The tolerances and the physical normalization (`JG-12`) are set after the control, from conformant evidence; `JX-4` informs the scale only |
| `JD-4` The invariant-B guard | **D** for the control | The argument under "The governing choice". It is also Claude's default for the next run (`claude:1448`) | The ratified rule (`57-RULING.md:95-107`) is computed at every step on the corrected 256-identity monitor and logged with its margins and the step at which it would halt. It halts nothing. The run spends no graded slot and no evaluation. After the control, B, C or the ratified rule is chosen from its traces. Graded runs keep the ratified rule and must refuse the observe-only mode |
| `JD-5` Learning-rate schedule | **A** | Agreed | Cosine over the Adam phase (`ctl_instruction.md:1805`), with `n_adam = 1000` and the existing 100-update warm-up (`pinn_architecture.md:699`). The constant-rate arm (`JX-7`) is pre-registered for readout branches (c) and (d) |
| `JD-6` L-BFGS and the plateau input | **A** for the control | It keeps the Adam phase the same length on every seed. Refinement comes after the Adam phase is shown to move the front (`codex:363`, "explicitly an Adam-only diagnostic control") | Adam-only by an explicit, logged configuration switch, not by `max_epochs == n_adam`, which a plateau firing bypasses. The plateau detector runs observe-only. B and C (reachable L-BFGS with explicit headroom; a smoothed or population plateau input) are the next stage under readout branch (a), where the ratified L-BFGS freeze (`57-RULING.md:112-124`) applies |
| `JD-7` Budget, seeds and the run | **Staged (A)**, on the project's three-seed band | No budget can be defended before a conformant run, and R-2 voids the Q4 answer. Seed 42 pairs the control with generation 7: batch selection does not depend on the model (P-5), so the control draws the same batches, and a difference between the runs belongs to the conformance change and its re-measured reference (`codex:369`). Seeds 41 and 43 complete the band the project used in v2.0 and planned in v2.3 | Stage 1 is 1,000 Adam steps per seed, with no completion forecast. Seed 42 runs first; seeds 41 and 43 follow, unless seed 42 exposes an implementation defect, which is fixed first. The pairing holds only if the corrected code consumes the batch random stream as before, and the plan checks this against the replayed sequence (verification Part 1, A.2). The stage-2 budget is set from the measured prefix reduction per full-rate-equivalent step (`claude:1475`). Checkpoint ④'s graded-seed rule (`57-RULING.md:24-25`) is unchanged |
| `JD-8` Causal coefficient | **A**: `η_c = 1` | Not isolated as a cause (`codex:312`); ruling A1 stands | — |
| `JD-9` Architecture | **A** | Agreed. Changing the representation together with conformance would confound both | `JX-5`'s split at the default architecture is authorized. Claude's sweep, which needs a verification-only path past `pinn/architecture_spec.py:71-130`, is deferred to readout branch (d) |
| `JD-10` Telemetry and verification gates | **A**: the union of both lists | Agreed. The missing measurements are why the last runs could not separate causes (Claude G-5, `claude:1616`) | Every step: the selected identities, and the monitor's prefixes, front, high-water mark and threshold margins. On the existing 50-step cadence: per-term gradient norms with Adam-preconditioned shares, and the IC position/velocity split. Also: the identity-dependent conformance assertion, the `train.log` hand-off message fix (`C-F05`), and per-identity monitor profiles (for `OQ-4`). The diagnostic modes are written into the run's configuration record, and a graded run refuses them |
| `JD-11` First authorizations | **A** | Agreed. Each read-only experiment can falsify a load-bearing reading in minutes to about an hour | See "The experiments". C, runs on the current non-conformant code, is declined |

## The owner questions

| Question | Answer | Why |
|---|---|---|
| `OQ-1` GATE-04 probe realism | Keep the ratified six-case probe for `R_ref` and GATE-04; no amendment now. Add one check on the data the run reads: with the re-measured `R_ref`, the frozen monitor's 256 training identities at initialization must not give floor-bound or degenerate weights (GATE-04's own fail-closed conditions, `pinn_architecture.md:452`). If the probe passes and the monitor fails, stop: the probe is amended to training-split ICs before any run | What matters is whether the causal weights respond on the trajectories the run trains on. The check tests that directly, with an existing criterion and no new threshold (Claude G-8, `claude:1619`) |
| `OQ-2` What an "epoch" is | One optimizer step, for budgets, the plateau window, the validation cadence and the replay rule. The replay sampler stays as executed | The spec's own per-step skeleton calls a training step an "Adam epoch" (`ctl_instruction.md:1777`), the code counts in steps (`claude:1617`), and every budget record is in steps. Under this reading the Phase-34 replay rule means no trajectory repeats within a step's replay draw, which the code satisfies (`V:311-315`). Only the parenthesis "(standard once-per-epoch coverage)" (`ctl_instruction.md:1829`) suggests a pass over the pool, and a clarifying amendment rewrites it. Pass-over-pool coverage is not adopted. Drawing 240 of 1,812 per step gives each trajectory about 132 ± 11 draws in 1,000 steps, a small spread, and a new sampler would break the seed-42 pairing (`JD-7`) |
| `OQ-3` Spec cross-reference | Fix by amendment: transcribe the invariant-B monitor contract (`57-RULING.md:93-110`) into the spec, where `pinn_architecture.md:452` cites "the fixed-monitor boundary above" | The cross-reference points at nothing in that file (Claude G-15, `claude:1626`). No value changes |
| `OQ-4` Causal weights across trajectories | Keep the ratified batch-global 16-bin prefix (`pinn_architecture.md:452`). The control logs per-identity prefix profiles on the monitor. If a minority of identities dominates the bin means and holds the front, the question is reopened with that evidence | Every causal-training source read is single-IC (departure L-6), so only conformant data can answer it (Claude G-9, `claude:1620`) |
| `OQ-5` Why 0.5 and N = 500 | No derivation is recorded. They are owner rulings (`57-RULING.md` §2), and they stand for graded runs. The control records the evidence a redesign needs: the corrected monitor's noise band and record timing. `JD-4`'s choice after the control uses it | Claude G-4 (`claude:1615`) |

## The experiments

| ID | Ruling | When | Note |
|---|---|---|---|
| `JX-1` Gradient decomposition | Authorized | Executed-batch half first; conformant half after the `JD-0` gate | Checkpoints 0, 900 and 951. Checkpoint 0 is the seed-42 initialization, before any training, so its conformant reading measures the recipe rather than the executed run, and R-2 lets it count as structural evidence. The readings at 900 and 951 are class `E` |
| `JX-2` Monitor noise | Authorized | First | It explains generation 7's stall. The corrected monitor's noise band comes from the control's own trace |
| `JX-3` Exposure panel | Authorized | First | Validation-split trajectories may be read (R-5); no test-split file is opened |
| `JX-4` Relative against absolute | Authorized | First | It informs `JD-3`'s scale only (R-2) |
| `JX-5` Initialization decomposition | Codex's split at the default architecture is authorized | First | Initialization only. Claude's sweep is deferred to readout branch (d) |
| `JX-6` λ_phys = 0 control | Declined | — | It would spend compute on the non-conformant objective, and its answer would describe the single-anchor run (R-2, R-3) |
| `JX-7` Constant rate against cosine | Deferred | Readout branches (c) and (d) | Conformant code only, with matched arms (`codex:131`) |
| `JX-8` Calibration pilot | The control is its stage 1 | After the `JD-0` gate, the `R_ref` re-measure, GATE-04 and the `OQ-1` check pass | — |
| `JX-9` Instrumentation | Rides on the control | — | It is `JD-10` |
| `JX-10` Verification completion | Authorized | First | It closes the verification's open forward-pass rows. Not a decision input |

**Model computation authorized:**

- forward and backward passes on retained checkpoints and on freshly
  initialized networks, for the experiments marked authorized;
- the control run, and only after its gates pass. It is the only training
  this ruling authorizes.

No evaluation is authorized, and no test-split file is opened.

## The control run, composed

| Surface | Setting | Source |
|---|---|---|
| Purpose | Diagnostic, not graded. It spends no graded slot and no evaluation | this ruling |
| Seeds | 42, then 41 and 43 | `JD-7` |
| Architecture | Unchanged: 12 × 256, `first_omega_0 = 30`, hidden frequency 1, power-skip and LayerNorm as ratified | `JD-9` |
| Physics, IC term, monitor, validation | Per slot; the IC term is the mean over slots | `JD-0`, `JD-1` |
| Collocation and causal weights | 4,096 rows in 16 bins of 256; `R̃_b = R̄_b / R_ref`; one batch-global 16-bin prefix; `η_c = 1` | `pinn_architecture.md:452-456`; `JD-8` |
| `R_ref` | Re-measured by the ratified six-case procedure; the `OQ-1` check must then pass | `JD-0`, `OQ-1` |
| Loss weights | As ratified: `λ_IC = 1`, `β_v = 1`, `λ_phys^max = 1` with its warm-up, `λ_data = 1` | `JD-2` |
| Optimizer | Adam from rate 10⁻³; cosine over `n_adam = 1000`; 100-update warm-up | `JD-5`; `codex:348-371` |
| L-BFGS | None, by explicit switch | `JD-6` |
| Plateau detector | Observe-only | `JD-6` |
| Guard | Observe-only; the ratified rule computed and logged at every step | `JD-4` |
| Replay sampler | As executed | `OQ-2` |
| Telemetry | The full set | `JD-10` |
| Held-out evaluation | Unspent | standing boundary |

## The readout, pre-registered

The readout comes after all three seeds, or after seed 42 alone if seed 42
exposes an implementation defect. It takes exactly one branch, and records the
evidence for the branch it takes. The front is always read together with the
absolute measures (`JD-3`).

- **(a) The front advances.** On at least two of the three seeds, the ratified
  rule would not have halted the run within its 1,000 steps.
  - Next, stage 2: set the budget from the measured rate, make L-BFGS
    reachable (`JD-6` B and C), choose the guard's statistic from the traces
    (`JD-4` B or C), and set the absolute tolerances (`JD-3`).
- **(b) The front stalls and physics is a passenger.** The ratified rule would
  have halted the run on at least two seeds, and physics' share of the
  Adam-preconditioned update along −g_phys is 10⁻⁴ or less. That threshold is
  Claude's own criterion for confirming PC-2 (`claude:1362`).
  - Next, the rebalancing arm: `JD-2` C, drafted as an amendment, on the same
    seeds.
- **(c) The front stalls as the learning rate decays.** The halts of (b), a
  physics share of 10⁻² or more, and a stall that begins as the cosine schedule
  decays.
  - Next, the schedule arm: `JX-7` on conformant code.
- **(d) Anything else.** For example: the seeds disagree; the share falls
  between 10⁻⁴ and 10⁻²; the stall has no schedule signature; or the front
  advances while the absolute errors stop falling.
  - Next, discriminate before changing the recipe: `JX-7`, the `JX-5` sweep,
    and more seeds as needed.

## Order of work in the next milestone

1. **Read-only measurements on retained checkpoints,** against the code that
   produced them: `JX-1` (executed half), `JX-2`, `JX-3`, `JX-4`, `JX-5`
   (split) and `JX-10`.
2. **Conformance and instrumentation:**
   - `JD-0`, `JD-1` and `JD-10`;
   - the diagnostic modes;
   - the clarifying amendments (`JD-1`'s batch rule, `OQ-2`, `OQ-3`).
3. **Gates:**
   - the identity-dependent conformance assertion;
   - the `R_ref` re-measure, the GATE-04 re-run and the `OQ-1` check;
   - then `JX-1`'s conformant half.
4. **The control run:** seed 42, then seeds 41 and 43.
5. **The readout,** by the branches above.

## Record

- **This file is the ruling.** Its picks are recorded as a project Key
  Decision (`.planning/PROJECT.md`, ERW Rule 13).
- **The consolidated document is unchanged.** It keeps its empty pick column,
  as its STANDING requires.
- **Later decisions.** A decision this ruling pre-registers is taken by its
  branch, and the evidence is recorded. A decision outside these branches goes
  back to the owner.
