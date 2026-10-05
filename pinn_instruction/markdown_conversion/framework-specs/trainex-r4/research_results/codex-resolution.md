---
title: Trainex R4 Codex research result
role: returned research report; candidate findings and owner-gated options
status: active
created: 2026-10-04
agent: Codex
access_mode: open-book
source_baseline: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
live_tree_pin: b09c4c8cfd22429e0d14482c355719f862a54e6f
branch: milestone/v2.3
worktree: <home>/Desktop/3_body_problem/.worktrees/trainex
verification_status: pending independent ERW Rule-19 verification
report_body_sha256: 634c5fdd045a4c14b0e91451e6959fb22c3bbcaba831becf21ecf3709abefdb1
---

# Trainex R4 Codex research result

This file preserves the research report delivered in this chat. The owner explicitly requested saving the result on 2026-10-04, after the read-only investigation. Statements below about no file edits and unchanged Git state describe that investigation, before this authorized delivery write. The report does not constitute the independent Rule-19 verification report, a consolidated resolution document, or an owner ruling.

<!-- BEGIN RESEARCH REPORT -->
**The main finding is a conformance failure: generation 7 did not evaluate the intended multi-trajectory physics objective.** Its sampler generated correctly attributed collocation rows, but the controller evaluated every row using one trajectory’s IC and masses. The recorded stall is real; attributing it to the ratified recipe is therefore premature.

This report follows the requested five-part contract. No files were edited, no experiments or training were run, no evaluation was invoked, and no commit was made.

The engagement used `<home>/Desktop/3_body_problem/.worktrees/trainex`, branch `milestone/v2.3`, at commit `b09c4c8cfd22429e0d14482c355719f862a54e6f`. The relevant production files and live specifications match the generation-7 run commit `629b1a6ca4462915b6340a59b8d4e3ad8df75d8b` byte for byte.

Evidence labels below mean **RV**: repository-verified; **PD**: package-derived; **L**: published literature; **A**: independent analysis.

## 1. Premise-challenge findings

### P1. The executed physics calculation discards collocation identities

**RV, high confidence.** The sampler constructs each collocation row’s IC, masses, and record key. The controller then selects the first replay identity, constructs a trajectory callable around that identity, and consumes only the collocation times. Every physics microbatch evaluates that same callable and mass vector. See [batches.py:492](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/data/batches.py:492), [controllers.py:1075](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:1075), [controllers.py:1128](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:1128), and [controllers.py:1760](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:1760).

The intended bin residual is

\[
\bar R_b=\frac1{256}\sum_{s\in b}
R(u_s,IC_s,m_s).
\]

The executed residual is

\[
\bar R_b^{\mathrm{executed}}=\frac1{256}\sum_{s\in b}
R(u_s,IC_{\mathrm{anchor}},m_{\mathrm{anchor}}).
\]

**RV.** This conflicts with the locked selected-slot contract and the owner’s explicit instruction to replace one-anchor physics with contributions from all selected slots. It is not an unresolved interpretation of “time allocation.” See [pinn_architecture.md:456](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:456) and [57-GAPS.md:214](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-GAPS.md:214).

Consequently, F-12’s counts, normalization, and prefix arithmetic are supported, but its premise that the complete ratified recipe executed is contradicted.

### P2. The production conformance evidence misses this failure

**RV, high confidence.** The verifier checks that *generated* collocation keys contain multiple identities, then calls the single-anchor calculation. Its output field `"anchor_only": false` is a literal constant. Finite, nonzero aggregate physics gradients cannot establish that each row’s IC reached the model. See [phase57_production_conformance.py:408](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/verification/phase57_production_conformance.py:408) and [phase57_production_conformance.py:533](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/verification/phase57_production_conformance.py:533).

This weakens the package’s production-conformance premise without disputing the recorded GATE-04 arithmetic.

### P3. The frozen monitor effectively scores one identity

**RV.** Restricted, non-executing inspection of retained checkpoint metadata found 4096 monitor rows, 256 distinct keys, and 16 rows per key. Its first identity is `('hierarchical', 'base', 28)`. However, monitor evaluation rebuilds the same single-anchor context. Thus its physics residuals describe that fixed identity at the frozen times, rather than the recorded 256-identity population. See [controllers.py:931](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:931) and [controllers.py:1044](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:1044).

**RV/A.** Training anchors also have an ordering bias: sampled replay keys are sorted, and the controller chooses the smallest. This favors low-ranked keys; it does not establish that those keys are physically easier or harder. See [batches.py:76](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/data/batches.py:76).

### P4. Adam exhaustion would not start L-BFGS under this configuration

**RV, high confidence.** F-05’s budget-exhaustion handoff description is incomplete in a consequential way. Both `n_adam` and `max_epochs` equal 1000. After full Adam exhaustion, remaining refinement budget is zero, and the controller returns through the stage-exit path without running L-BFGS. See [configuration:24](<home>/Desktop/3_body_problem/.worktrees/trainex/configs/stage0-v23g7-seed42.yaml:24) and [controllers.py:2690](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:2690).

An earlier plateau could leave refinement budget. Independently reconstructing its detector from the completed logs found a maximum qualifying streak of **6**, against the required **50**. See [controllers.py:546](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:546).

### P5. Generations 6 and 7 are not two independent demonstrations of the timeout

**RV.** Their configurations differ only in run name, and their telemetry shares a substantial initial trajectory. Generation 6 ended through process loss at step 513, only 160 updates after its last front advance at 353. It did not exhaust the 500-step window. The earlier “two independent runs … stalled” wording overstates the evidence. See [blocked-state-g6.json:13](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json:13) and [the challenged wording:105](<home>/Desktop/3_body_problem/.worktrees/trainex/docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md:105).

### P6. Two numerical interpretations need qualification

**RV.** “Applied gradient” means multiplication by the scheduled loss weight, before Adam preconditioning. “Raw physics gradient” already includes the physics loss’s `R_ref` normalization. These are not measurements of each term’s optimizer update. See [controllers.py:1993](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:1993).

**RV.** F-06’s weighted-sum equality holds to float32 rounding, rather than literal equality between printed values summed in double precision. The maximum relative discrepancy is approximately \(1.14\times10^{-7}\). This is ordinary rounding, not evidence of incorrect loss assembly. See [training log:57](<home>/Desktop/3_body_problem/.worktrees/trainex/runs/stage0-v23g7-seed42/logs/train.log.jsonl:57).

## 2. Diagnosis

### The published method

**L.** The source identification in H-03 is supported: Sifan Wang, Shyam Sankaran, and Paris Perdikaris, *Respecting causality for training physics-informed neural networks*, **Computer Methods in Applied Mechanics and Engineering**, 421, 116813, 2024. Its 2022 preprint describes exclusive-prefix exponential weights, detached weight gradients, increasing causal parameters `[0.01, 0.1, 1, 10, 100]`, and termination of each parameter loop when the minimum weight exceeds 0.99. Earlier residual descent opens later weights. Its optimizer uses gradual exponential decay, not this project’s cosine schedule or 500-step high-water timeout. [Primary paper](https://arxiv.org/pdf/2203.07404), [publication DOI](https://doi.org/10.1016/j.cma.2024.116813).

**L.** The author implementation also includes the IC loss in its causal exponent, uses Adam starting at \(10^{-3}\), and decays its rate by 0.9 every 5000 iterations. These are implementation settings, not universal requirements. [Author code](https://raw.githubusercontent.com/PredictiveIntelligenceLab/CausalPINNs/main/KS/chaotic_KS.py).

**L.** The later source matters. Wang, Sankaran, Hanwen Wang, and Perdikaris, *An Expert’s Guide to Training Physics-informed Neural Networks*, **arXiv**, 2023, uses fixed causal tolerance 1 and 16 chunks in several benchmark configurations, together with gradient-norm loss balancing. It recommends reducing causal strength when weights cannot approach one. Thus fixed \(\eta_c=1\) is not itself a violation of the published method family. [Primary paper](https://arxiv.org/pdf/2308.08468).

**RV/A.** The project’s coefficient acts on reference-normalized residuals, so its effective coefficient on raw residual energy is

\[
\eta_{\mathrm{raw}}=\frac1{R_{\mathrm{ref}}}
\approx5.06\times10^{-11}.
\]

Its separate IC loss, initialization-relative normalization, half-weight front, timeout, short cosine horizon, and single-anchor execution prevent direct transfer of the source’s convergence interpretation. See [loss_catalog.py:391](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/loss_catalog.py:391).

### Q1. Window versus learning-rate schedule

**Diagnosis:** the schedule offers a plausible contribution to slowing, but the evidence does not isolate it. The identity failure and IC-directed gradient are stronger established complications.

| Mechanism | Prediction | Existing discriminator | Confidence |
|---|---|---|---|
| Falling learning rate reduces optimization opportunity | Prefix reduction slows as the rate falls | Rate falls approximately 94-fold from logged steps 450 to 950; no matched alternative schedule exists | Medium as a contributor; low as sole cause |
| IC dominates the update-driving gradient | Physics improves mostly through changes useful to IC fitting | All 19 diagnostic gradients are overwhelmingly IC-directed before Adam | High for gradient domination; medium for causal contribution |
| Changing, biased anchors produce an uneven objective | Batch fronts improve differently from the fixed anchor | Executed identity selection and batch/monitor disagreement support this | High for mechanism; contribution unquantified |
| Gradient clipping suppresses progress | Norm exceeds clipping threshold | Reconstructed clipping never binds | Contradicted |

**RV.** IC exceeds the other active loss terms by at least **236.6×**. Its gradient exceeds physics by **27,797× to 2,616,396×**. At diagnostic steps,

\[
\frac{\|g_{\mathrm{phys}}+g_{\mathrm{data}}\|}
{\|g_{\mathrm{IC}}\|}
\le3.65\times10^{-5}.
\]

This establishes pre-Adam gradient domination, not zero physics influence after coordinatewise moment normalization. See [training log:50](<home>/Desktop/3_body_problem/.worktrees/trainex/runs/stage0-v23g7-seed42/logs/train.log.jsonl:50) and [training log:900](<home>/Desktop/3_body_problem/.worktrees/trainex/runs/stage0-v23g7-seed42/logs/train.log.jsonl:900).

**RV.** Adaptive clipping binds on none of the 952 recorded iterations; the largest norm/threshold ratio is 0.741. See [clipping rule:240](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/grad_clip.py:240).

**PD/A.** At the trip, advancing to bin 3 requires

\[
1.1891 \rightarrow <\ln2=0.693147,
\]

a further **41.7%** reduction in the relevant prefix. Raising the deadline alone supplies no evidence that this reduction will occur. See [retained replay:274](<home>/Desktop/3_body_problem/.worktrees/trainex/docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md:274).

**Owner-gated discriminator.** After conformance verification, compare matched cosine and constant-rate arms with identical initialization, draws, monitor, warmup, and update count. Measure continuous prefix reduction, IC fitting, and gradient allocation. Better prefix descent under constant rate would support schedule starvation; similar behavior would weaken it. This needs training. At the recorded runtime, 500 updates per arm cost roughly 100 minutes each, before overhead.

First, a retained-checkpoint fixed-training-panel decomposition could measure gradient directions and IC position/velocity contributions without training. It was not performed.

### Q2. Relative front versus absolute accuracy

**Diagnosis:** the front is an optimization diagnostic. It cannot certify physical accuracy.

**A, directly derived from the ratified formula.**

\[
\mathrm{front}\ge k+1
\iff
\sum_{b=0}^{k}\bar R_b
<R_{\mathrm{ref}}\ln2.
\]

A full front at bin 15 therefore implies only

\[
\frac1{15}\sum_{b=0}^{14}\bar R_b
<9.1263\times10^8.
\]

It does not bound bin 15’s residual, IC error, or trajectory error. Changing initialization and remeasuring the reference also changes this raw-unit tolerance. See [governing formula:452](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:452).

The candidate mechanisms are:

- **Relative descent without useful accuracy.** Predicts advancing weights while raw residuals or IC errors remain large. The retained replay and IC telemetry support this possibility.
- **Useful accuracy emerging with relative descent.** Predicts simultaneous improvements in absolute residuals, IC fitting, and trajectory error. Existing evidence does not establish that relationship.
- **Reference-dependent front changes.** Predicts different front states for equal raw errors under different reference scales. This follows algebraically.

**Owner-gated discriminator.** On fixed training-only fixtures, compare raw residuals, IC errors, and trajectory errors across retained checkpoints, without using the sole held-out evaluation. This needs no new training, but does require expressly authorized model scoring. A strong relationship would support the front’s usefulness as a progress indicator; weak agreement would support keeping accuracy decisions separate.

### Q3. SIREN scale and power-skip stack

**Diagnosis:** the stack can explain large derivative sensitivity, but neither \(\omega_0=30\) nor the skips are established as the root cause.

**RV.** The inspected AD path correctly differentiates the mapping \(\tau=2u-1\), and the IC reduction matches the specification. I found no duplicate factor of two or four, or missing body-average factor, explaining the large IC term. See [controllers.py:1091](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:1091), [physics_residual.py:128](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/physics_residual.py:128), and [loss_catalog.py:279](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/loss_catalog.py:279).

The admitted mechanisms are:

| Mechanism | Prediction | Present discrimination |
|---|---|---|
| High first-layer frequency creates large time and mixed parameter/time derivatives | Large acceleration and IC-velocity gradient contributions | Compatible with telemetry; position/velocity split is absent |
| LayerNorm and squared skips amplify downstream derivative sensitivity | Sensitivity persists despite reducing first frequency | Analytically possible; no actual-stack ablation exists |
| Force magnitude or acceleration/force cancellation dominates residual scale | Changing frequency alone gives limited improvement | No retained component decomposition |
| Uneven single-anchor exposure drives the observed behavior | Correct mixed-identity execution changes gradients and front behavior | Execution mismatch confirmed; effect needs measurement |

**L.** Sitzmann, Martel, Bergman, Lindell, and Wetzstein, *Implicit Neural Representations with Periodic Activation Functions*, **NeurIPS**, 2020, supports sinusoidal representations and their initialization scheme. It does not establish a universal fourth-power residual law for this project’s LayerNorm/power-skip stack. [Primary paper](https://arxiv.org/pdf/2006.09661), [official implementation](https://raw.githubusercontent.com/vsitzmann/siren/master/explore_siren.ipynb).

**A.** For \(h=\sin(\omega a)\) and downstream function \(G\),

\[
y''=J_Gh''+H_G[h',h'].
\]

Nominal \(\omega^4\) squared-residual scaling requires downstream derivatives, amplitudes, force terms, and cancellations to remain comparable. They need not. For example,

\[
\operatorname{LN}(\omega a)=
\frac{\omega(a-\bar a)}
{\sqrt{\omega^2\operatorname{Var}(a)+\epsilon}}
\]

approximately cancels the scale when the stabilizer is negligible. This rejects a universal extrapolation without proving the prior alternative empirical exponent.

**Owner-gated discriminator.** A train-free actual-stack decomposition should separate acceleration, force, IC position/velocity error, mixed derivatives, and skip contributions. Fresh-initialization frequency and skip ablations would follow only if that decomposition implicates them. Their normalization and raw-unit comparisons must remain explicit. No such probe was performed.

### Q4. Realistic Stage-0 budget

**Diagnosis:** the available evidence cannot identify a realistic completion budget.

**PD/A.** At step 951, the first six normalized bins alone sum to **3.8827**. They need more than **5.60×** further reduction before the remaining bins can fit inside the full-front prefix allowance. A linear extrapolation from the first two advances is unjustified. See [retained replay:274](<home>/Desktop/3_body_problem/.worktrees/trainex/docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md:274).

The alternatives are:

- **Insufficient optimization opportunity.** A longer adequately powered run would continue reducing early prefixes.
- **Objective imbalance or identity failure.** Additional updates under the same executed objective could remain inefficient.
- **Architecture or optimization barrier.** Prefix reduction would plateau despite adequate rate and balanced gradients.
- **Unexercised refinement.** L-BFGS might help, but no recorded run tests that possibility.

**RV.** The budget is explicitly provisional, and this configuration provides no refinement headroom after full Adam exhaustion. See [ctl_instruction.md:1994](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1994).

**L.** Published benchmark budgets are much larger, but are specific to their causal-parameter loops, time windows, networks, and equations. They are not a three-body budget estimate. [Causal-method paper, Appendix C](https://arxiv.org/pdf/2203.07404).

**Owner-gated discriminator.** Use staged diagnostic extensions after conformance and conditioning checks. Measure prefix reduction per update and per unit time. If refinement is tested, reserve explicit total-budget headroom without simultaneously changing Adam duration, cosine horizon, and warmup. Training is required; L-BFGS cost remains uncertain because one outer call can involve several closures.

### Q5. Front oscillation

**Diagnosis:** existing evidence proves threshold regression and recovery, not a dynamical instability or its frequency.

**PD/A.** At step 900, the prefix controlling entry to bin 2 is 0.7277, only 0.0346 above the threshold. By step 951 it is 0.5505, comfortably below it. The prefix controlling entry to bin 3 remains 1.1891. Thus losing and regaining bin 2 is compatible with failing to approach bin 3. See [replay output:271](<home>/Desktop/3_body_problem/.worktrees/trainex/docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md:271).

| Mechanism | Prediction | Existing evidence |
|---|---|---|
| Threshold sensitivity | Small continuous changes cause integer front changes | Supported near the bin-2 boundary |
| Parameter changes impair the fixed anchor temporarily | Fixed-monitor residual regresses despite batch improvements | Compatible with retained snapshots |
| Changing training anchors explain batch/monitor disagreement | Batch front varies without equivalent fixed-anchor improvement | Strongly supported by executed identity selection |
| Numerical instability | Nonfinite values, binding guards, or substantial arithmetic sensitivity | No nonfinite or clipping evidence supporting this explanation |

**RV.** The batch front changes 492 times, but those observations mix parameter changes with resampling and anchor selection. No per-step anchor identities or frozen-monitor residual trace exists in the retained scalar logs. See [training-record construction:1598](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:1598).

**Owner-gated discriminator.** Record continuous fixed-monitor prefixes, their threshold margins, and actual evaluated identities on a corrected diagnostic run. A retained-checkpoint fixed-panel comparison could first test whether regressions occur across several ICs or primarily the current monitor anchor. Neither measurement should alter the advancement rule before an owner ruling.

### Independent comparison with H-01 through H-03

| Prior analysis | Assessment |
|---|---|
| H-01: flat-profile endpoint arithmetic | Agree. \(e^{-15}=3.059\times10^{-7}\); normal-floor exponent margin is approximately 5.82. This is illustrative arithmetic. |
| H-01: normalization addresses conditioning | Agree narrowly for reducing physics scale. It does not establish balanced IC/data/physics gradients; current IC domination remains severe. |
| H-01: retain frequency pending evidence | Supported as a cautious diagnostic choice. No actual-stack causal comparison establishes a better value. |
| H-01: 16-bin prefix separates count from causal strength | Agree algebraically. Implementation still violates the preserved identity semantics. |
| H-01: clip should not manufacture progress | Agree. Existing logs show no binding causal-floor or adaptive-gradient clip. |
| H-02: not a near miss | Agree for the measured bin-3 prefix at the trip: 41.7% further reduction is required. This says nothing decisive about counterfactual training. |
| H-02: front oscillates rather than creeps | Narrow to observed regression/recovery. Sparse snapshots cannot characterize oscillation frequency. |
| H-02: two independent stalled runs | Disagree, for the independence and incomplete-timeout reasons above. |
| H-02: full front means about 20× reduction and raw residual about \(10^9\) | A flat order-one profile needs 21.64× reduction. The raw value is an upper bound on the first-15-bin mean, not a guaranteed residual level or accuracy certificate. |
| H-03: source identification | Agree after independent primary-source inspection. |
| H-03: stack scaling dispute | Remains unresolved empirically. The conditional fourth-power derivation does not apply universally to this stack. |

## 3. Options

These are recommendations for owner consideration. No option is selected or authorized by this report.

“Two-way” means the configuration or implementation choice is reversible with preserved artifacts. Executed compute cannot be recovered. Spending the held-out evaluation is a one-way evidence decision.

### D0. Restore and verify identity conformance

**Suggested default: A.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Correct row-wise IC/mass consumption and verify actual model inputs | P1 confirmed | Restores the existing contract; requires reference/gate provenance review before further diagnosis | Two-way implementation |
| B. Ratify single-anchor physics as a new design | Owner deliberately accepts biased, narrower training | Requires a specification amendment and redefinition of monitor claims | Two-way design; cannot retroactively make old execution conformant |
| C. Commission a broader trainer rebuild | Bounded correction proves impractical | Larger scope and verification cost | Two-way, expensive |

The decisive verification must observe evaluated IC/mass inputs, rather than merely generated metadata.

### D1. Address loss-gradient allocation

**Suggested default: A first; then branch on its result.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Fixed-panel decomposition before weight changes | Contribution of imbalance remains unresolved | Separates IC position/velocity, gradient alignment, and Adam effects | Two-way diagnostic |
| B. Retain weights in a controlled corrected run | Panel does not justify a balancing change, or owner wants a control | Preserves \(\lambda_{\mathrm{IC}}=\lambda_{\mathrm{phys}}^{\max}=1\) | Two-way configuration |
| C. Ratify fixed or adaptive balancing | Corrected objective still has harmful gradient imbalance | Requires explicit scales/control law; interacts with warmup and causal descent | Two-way configuration; changed objective provenance required |

**A.** Reducing \(\lambda_{\mathrm{IC}}\) to 0.1 alone would still leave the measured IC/physics ratios at least approximately 2780. It is not an evidence-backed cure. Increasing the locked physics cap silently is also unavailable.

At initialization, distinguish actual scheduled gradients, where \(\lambda_{\mathrm{phys}}=0\), from standardized diagnostic comparisons using \(\lambda_{\mathrm{phys}}=1\).

### D2. Relate schedule and timeout

**Suggested default: A for a diagnostic control; B only after a matched comparison supports it.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Preserve cosine/500-step rules in a corrected control | Need a comparable control | May halt again; does not promise completion | Two-way |
| B. Compare a constant-rate arm | Schedule starvation remains plausible after D0/D1 | Changes schedule while matching other inputs | Two-way |
| C. Ratify a phase-aware deadline or schedule | Matched evidence supports inadequate opportunity | Requires an explicit new monitoring/window contract | Two-way policy |

A longer timeout alone does not correct the zero-refinement-budget issue.

### D3. Define what the front means

**Suggested default: A.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Retain relative front as a progress diagnostic; retain separate accuracy gates | Q2 arithmetic accepted | Requires raw residual and IC reporting alongside the front | Two-way |
| B. Replace front threshold with an absolute-error criterion | Owner supplies a justified physical tolerance | Changes monitor semantics and reference dependence | Two-way amendment |
| C. Require both relative progress and absolute-error conditions | Owner wants a combined operational gate | More explicit criteria; thresholds require grounding | Two-way amendment |

### D4. Causal coefficient

**Suggested default: A until corrected evidence supports a change.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Retain \(\eta_c=1\) | Current coefficient not isolated as cause | Preserves the contract during conformance diagnosis | Two-way |
| B. Compare a weaker fixed coefficient | Corrected, adequately optimized prefixes remain over-restricted | Opens later bins at equal residuals; does not improve accuracy by itself | Two-way |
| C. Ratify continuation | Source-style staged strength fits the corrected problem | Adds parameter schedule and stopping semantics | Two-way, greater policy complexity |

Front movement induced by changing the coefficient cannot be counted as equivalent residual improvement.

### D5. Architecture

**Suggested default: A; branch to B or C only after decomposition.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Retain the current architecture during conformance diagnosis | Architecture contribution unresolved | Avoids simultaneous representation changes | Two-way |
| B. Fresh-initialization frequency ablation | Frequency-sensitive derivatives dominate | Invalidates reference provenance; requires fresh gate and raw-unit comparisons | Two-way, compute cost |
| C. Fresh-initialization skip ablation | Skip/LN derivatives dominate | Changes backbone behavior and reference calibration | Two-way, larger verification cost |

### D6. Budget and refinement

**Suggested default: A.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Staged diagnostic budgets; make no completion forecast | Current evidence insufficient | Limits spend while measuring marginal progress | Two-way |
| B. Add explicit L-BFGS headroom | Refinement is the next question | Increase total budget separately from Adam duration | Two-way; closure cost uncertain |
| C. Extend Adam duration | Corrected prefixes keep descending under adequate optimization | Also changes cosine horizon and warmup unless explicitly controlled | Two-way |

### D7. Monitor interpretation

**Suggested default: A.**

| Option | Presupposed diagnosis | Mechanical consequence and interaction | Door |
|---|---|---|---|
| A. Correct identity consumption; record continuous prefixes and evaluated identities | P3 confirmed | Preserves frozen sampling and existing threshold initially | Two-way |
| B. Ratify several fixed training-only panels | One panel inadequately represents population behavior | Requires aggregation and advancement rules | Two-way amendment |
| C. Add hysteresis/persistence | Corrected traces show operational threshold chatter | Could hide real regressions; requires explicit justification | Two-way amendment |

### Composed next-run recipe

**Suggested diagnostic configuration, conditional on owner approval and D0 verification:**

| Surface | Proposed control |
|---|---|
| Initialization | Fresh seed 42 |
| Architecture | Current 12-layer stack; `first_omega_0=30`; hidden frequency 1 |
| Physics identities | Each row uses its own recorded IC and masses |
| Collocation | 4096 rows, 16 bins, 256 rows per bin, existing slot-allocation rules |
| Causal coefficient | \(\eta_c=1\) |
| Reference | Existing six-case/96-bin procedure; revalidate or reissue provenance under the corrected execution |
| Loss weights | Existing values, only on D1’s retain-weights branch |
| Adam | Initial rate \(10^{-3}\), existing cosine schedule, `n_adam=1000` |
| Warmup | Existing 100-update ramp |
| Total budget | `max_epochs=1000`, explicitly an Adam-only diagnostic control |
| Monitor | Correct multi-identity consumption, fixed training-only samples |
| Timeout | Existing 500-step rule |
| Added observations | Continuous prefixes, actual evaluated identities, IC position/velocity split |
| Held-out evaluation | Preserved unspent |

**A.** This control tests corrected invocation plus any required reference recalibration. It does not isolate identity correction alone if the reference changes, and it does not promise a full front or L-BFGS.

If D1 shows persistent harmful imbalance, the next-run configuration remains conditional on the owner’s balancing ruling. A matched constant-rate arm belongs after that choice. If the owner instead commissions refinement, total-budget headroom must be explicit.

### What the runbook inherits

- A finding that emitted identity provenance does not prove evaluated identity conformance.
- A requirement for independent Rule-19 verification before these findings inform a ruling.
- Explicit separation of the front diagnostic, raw physical errors, IC fitting, and held-out accuracy.
- Explicit Adam and refinement budgets.
- Reference and gate provenance review after correction.
- All existing training, held-out evaluation, Stage-1+, and platform authorization boundaries.

### Decision sheet

| Decision | Options | Suggested default | Door type | Presupposed diagnosis | Owner’s pick |
|---|---|---|---|---|---|
| D0 Conformance | Correct / ratify anchor / rebuild | Correct and verify actual inputs | Two-way | Identity collapse confirmed | ___ |
| D1 Balancing | Decompose / retain / amend balancing | Decompose, then branch | Two-way | Harmful contribution unresolved | ___ |
| D2 Schedule/window | Control / constant-rate comparison / amend coupling | Corrected control, then comparison | Two-way | Schedule causality unresolved | ___ |
| D3 Front meaning | Diagnostic / absolute / combined | Diagnostic plus separate accuracy gates | Two-way | Relative front is not accuracy | ___ |
| D4 Coefficient | Retain / weaken / continue | Retain during diagnosis | Two-way | Coefficient not isolated | ___ |
| D5 Architecture | Retain / frequency / skip ablation | Retain, then branch on decomposition | Two-way | Architecture cause unresolved | ___ |
| D6 Budget | Staged / refinement headroom / longer Adam | Staged diagnostics | Two-way | Completion budget unknown | ___ |
| D7 Monitor | Correct and instrument / multiple panels / hysteresis | Correct and instrument | Two-way | Current scored population is wrong | ___ |

## 4. Gaps

1. **Scientific effect of correcting identity consumption.** No conformant training result under the intended mixed-identity objective exists in the inspected evidence.
2. **IC decomposition.** Retained scalar losses do not separate position and velocity contributions.
3. **Optimizer allocation.** Term norms do not establish gradient alignment or coordinatewise Adam effects.
4. **Reference disposition after correction.** Existing invalidation language requires provenance review; this report does not decide whether the numeric reference changes.
5. **Schedule causality.** No matched schedule comparison exists.
6. **Architecture causality.** No actual-stack derivative decomposition or controlled ablation establishes a scaling law.
7. **Completion budget.** No evidence supports a reliable update count for all 16 bins.
8. **Monitor dynamics.** Sparse replay snapshots cannot characterize instability or oscillation frequency.
9. **Population and seed coverage.** One graded seed and partially shared trajectories do not support seed-general conclusions.
10. **Accuracy calibration.** No established mapping connects this front threshold to acceptable trajectory error.

These gaps are research findings. I did not write gap registers or make specification decisions because the research prompt prohibits file changes.

## 5. Claims-and-uncertainty register

| Claim group | Evidence base | Disposition |
|---|---|---|
| F-01 | RV | Confirmed: 951 updates, halted record 952, correct trip hash and terminal state |
| F-02–03 | PD + A | Replay arithmetic rederived; model measurements inherited, not newly evaluated |
| F-04 | RV | Confirmed; logged rate is the next update’s rate |
| F-05 | RV | Adam-only records confirmed; exhaustion-to-L-BFGS premise contradicted for this config |
| F-06 | RV | Weights/warmup confirmed; total equality qualified by float32 rounding |
| F-07–08 | RV | Magnitudes confirmed; gradient interpretation qualified as pre-Adam |
| F-09 | RV | Histogram and 492 changes confirmed |
| F-10–11 | RV + A | Threshold and prefix dependency confirmed; monitor population interpretation corrected |
| F-12 | RV | Median reference and scalar recipe confirmed; complete identity conformance contradicted |
| F-13 | RV | Shared trajectory confirmed; independence claim rejected |
| F-14 | RV/PD | Smoke records confirmed; monitor advance timing inherited from retained summary |
| F-15–16 | RV | Provisional budget and retained architecture contracts confirmed |
| F-17–18 | RV records | Terminal records preserve later seeds and evaluation; no evaluation invoked here |
| H-01 | A | Arithmetic supported; conditioning and conformance implications narrowed |
| H-02 | A/RV | Distance arithmetic supported; independence and oscillation claims narrowed |
| H-03 | L/A | Method identification confirmed; stack scaling remains empirically unresolved |
| Identity failure causes the stall | A | Plausible, unmeasured |
| IC imbalance contributes to the stall | RV/A/L | Strong mechanism candidate; not isolated causally |
| LR decay causes the stall | RV/A | Plausible contribution; not isolated |
| \(\omega_0=30\) causes the stall | A | Unestablished |
| Clipping causes the stall | RV | Contradicted by reconstructed thresholds |

Read-only verification included:

- `git status --short --branch`, `git worktree list --porcelain`, and `git rev-parse HEAD`.
- `git diff 629b1a6ca4462915b6340a59b8d4e3ad8df75d8b HEAD -- pinn/training/controllers.py pinn/training/losses.py pinn/training/config.py pinn/verification/phase57_production_conformance.py`.
- Independent `python3 -B -` standard-library checks of file bytes, telemetry, the 96-value median, front arithmetic, plateau detection, and clipping thresholds.
- Restricted ZIP/`pickletools` inspection of checkpoint primitives, without executable deserialization.
- Comparison of all 11 specification excerpts and nine reproduced evidence excerpts with their baseline and live sources, excluding packaging fences and boundary newlines. All matched.
- `git diff --check`, which passed.

The final Git status matches the initial status. Existing changes were preserved. The report remains a candidate for the workflow’s separately recorded Rule-19 verification and owner ruling.
<!-- END RESEARCH REPORT -->
