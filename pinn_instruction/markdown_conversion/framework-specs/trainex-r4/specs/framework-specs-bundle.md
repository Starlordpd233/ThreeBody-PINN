---
title: Trainex R4 Framework-Specs Bundle — locked spec excerpts (SIREN initialization, causal weighting, loss assembly, optimizer schedule)
role: excerpted locked framework-spec sections for the trainex-r4 research round; authoritative as a statement of what the contract currently says
status: active
created: 2026-10-04
source_baseline: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
access_mode: open-book
---

# Framework-Specs Bundle (trainex-r4)

This bundle is **upload attachment 2 of 3** for the trainex-r4 research round.
It assembles the locked framework-spec sections that bear on the round's five
questions: the SIREN initialization scale and the skip/power stack, the
architectural hyperparameters, the physics residual and causal weighting as
amended by v2.3 Phase 56, the initial-condition loss, the loss-balancing warmup
and clip guard, the optimizer split and gradient clipping, the Stage-0
curriculum, the total-loss assembly, the Adam and L-BFGS phases, and the stage
transition criteria.

**These sections are authoritative locked spec — hard constraints as a
statement of what the contract currently says.** A research answer that
proposes changing a number, formula, threshold, or normative decision stated
here must say so explicitly, name the contract marker it amends, and never
silently override it. Amending a locked contract on this project requires an
explicit owner re-ratification with recorded provenance.

**Route B — paths are retained.** This round runs open-book. Repository paths
inside the spec prose are reproduced unmodified, because the research agent has
read-only repository access and can resolve them. Nothing in this bundle has
been scrubbed, condensed, or re-worded.

**Extraction method (verifiable).** Each excerpt runs from its start heading up
to, but not including, the next heading named for it, located by exact
full-line match in the file at commit `735e2ae8d5ec30b9915ec9172ac06965fbaa8afb`. To re-derive any excerpt:

```
git show 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb:<path> | sed -n '<a>,<b>p'
```

**Fidelity note on line numbers.** The `Source:` lines give line ranges **as of
the pinned baseline commit**. `pinn_architecture.md` was edited during v2.3
(Phases 53 and 56), so line anchors quoted in older planning documents are
stale. Resolve any spec anchor by content match, never by trusting a line
number found elsewhere.

---

## Excerpt — §2.1 The Sinusoidal Activation (SIREN) + §2.2 A Principled Initialization Scheme for SIREN Layers

Source: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:127-205`

*Why it is in this round:* Carries the `first_omega_0 = 30` sentence and the Phase 56 NOT-AMENDED record beside it (question Q3).

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:127-205 -->

## 2.1 The Sinusoidal Activation (SIREN): The Key to Derivative Fidelity

The foundational element of the network's layers is the Sinusoidal
Representation Network (SIREN) activation function. This choice is not a
tunable hyperparameter but a mandatory architectural feature dictated by
the physics of the $\mathrm{N}$-body problem. A standard neural network
layer performs an affine transformation followed by a non-linear
activation. In a SIREN layer, this activation is the sine function[5]:
$$\phi_i(\mathrm{x}) = \sin(\mathrm{W}_i \mathrm{x} + \mathrm{b}_i)$$
where $\mathrm{x}$ is the input to the layer, and $\mathrm{W}_i$ and
$\mathrm{b}_i$ are the trainable weight matrix and bias vector,
respectively.

The primary motivation for this choice lies in the properties of its
derivatives. The derivative of a sinusoidal function is another
sinusoid, merely phase-shifted and scaled. For a single neuron with
activation
$\phi(\mathrm{x}) = \sin(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b}))$,
the chain rule gives:
$$\frac{\mathrm{d} \phi}{\mathrm{d} \mathrm{x}} = \omega_0 \mathrm{w} \cos(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b})) = \omega_0 \mathrm{w} \sin(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b}) + \frac{\pi}{2})$$

This property is recursive; higher-order derivatives of the network's
output with respect to its input remain well-behaved, smooth, sinusoidal
functions. This is a stark contrast to common activations like ReLU,
whose second derivatives are ill-defined or zero almost everywhere,
making them fundamentally unsuited for problems where the loss function
depends on second-order derivatives, as is the case for the
$\mathrm{N}$-body problem's physics residual.[1] The SIREN architecture
thus provides an exceptionally strong inductive bias for representing
the smooth, continuous solutions and their derivatives required by the
governing physical laws. This directly overcomes the spectral bias of
standard MLPs, which struggle to represent the high-frequency details
inherent in chaotic trajectories and their derivatives.[2] By using
SIREN, the network is inherently capable of representing the complex
natural signals that arise from physical systems.[8]

## 2.2 A Principled Initialization Scheme for SIREN Layers

The successful training of a deep SIREN is critically dependent on a
specific, principled initialization scheme. Naive initialization will
cause the distribution of activations to either collapse to zero or
explode into saturated regimes, halting the learning process. The
confusion between different documents regarding the hyperparameter
$\omega_0$ is resolved here by adhering to the original,
mathematically-derived SIREN initialization scheme, which is designed to
preserve the distribution of activations as they propagate through the
network.[5]

This scheme is not a heuristic but a carefully designed solution to two
distinct challenges: representation and trainability. It treats the
first layer of the network differently from all subsequent hidden
layers.

1.  **First Layer (for representation):** The initial frequency parameter
    `first_omega_0` is fixed at `30` and is not scheduled during training.
    A high initial frequency injects a high-frequency Fourier basis that
    helps the network overcome spectral bias from the outset. There is no
    epochwise or optimizer-step `omega0` scheduler. If `first_omega_0` is
    ever retuned, it is changed only as a stage-boundary ablation with a
    fresh re-initialization between runs — never mutated inside a run.

> **Phase 56 contract: `first_omega_0` fixed-at-30 sentence NOT AMENDED (SPEC-01; SCOPE-38; `54-RULING.md` checkpoint ② Block 2; grounded by `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`).** This contract was reviewed as part of the checkpoint-② recalibration adjudication and is **NOT AMENDED**: the ratified disposition is the retain option the ruling records (C1/D3-A), keeping `first_omega_0` fixed at `30` under the existing no-scheduler / fresh-reinitialization contract exactly as stated in the paragraph above. Phase 20 ARCH-01 remains this contract's acceptance criterion, unchanged, and the value carries forward byte-identical — no numeric change, no rewording, no added numeric bound. This record does not decide the treatment of §2.4 Table 1's Recommended-Value column heading or its `first_omega_0` row: that reconciliation is an open item tracked as GAP-56-02 and is deliberately left untouched by Phase 56.

2.  **Subsequent Hidden Layers (for Trainability):** For all other
    hidden layers, the weights $\mathrm{W}$ are initialized from a
    different uniform distribution,
    $\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]$.\
    The crucial difference is that the initialization range is **divided by** $\text{hidden\_omega\_0}$ (here $\text{hidden\_omega\_0} = 1$), following the standard SIREN initialization.
    This specific scaling is mathematically derived to ensure that the
    pre-activations (the inputs to the sine function) maintain a
    standard normal distribution throughout the network's depth. This,
    in turn, keeps the sine activations in a dynamic, non-saturated
    range, preventing the frequency of the network's output from growing
    uncontrollably with depth. This careful, layer-dependent
    initialization is what makes deep SIRENs trainable by ensuring
    stable gradient flow.[1]

    Author Comment: All of these fields with `\text{xxx}` are not rnedered correctly and show up in the preview as raw literal text strings. The examples are the hidden omega 0, and first omega, etc. 


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:127-205 -->

---

## Excerpt — §2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation

Source: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:206-263`

*Why it is in this round:* The skip/power stack whose ablation is deferred (question Q3).

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:206-263 -->

## 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation

While the SIREN initialization enables training, pushing to the depths
required for chaotic dynamics (e.g., 12 layers) requires stabilization
of the residual connections. This report adopts an advanced ResNet
variant with a project-specific (author) modification: **Layer
Normalization (LayerNorm)** applied to the skip path before the power
term. This LayerNorm stabilizer is an author addition for this project —
it is **not** part of the original SQR-SkipResNet formulation — and it
is applied on the skip/power branch only. This resolves gradient
instability while preserving the architecture's benefits for chaotic
systems.

The precise mathematical update rules are as follows:

1.  For odd-numbered layers ($l = 1, 3, 5, \ldots$):

$$\mathbf{x}^{(l)} = f_{\text{sr}}^{(l)}(\mathbf{x}^{(l-1)}) + \left(\text{LayerNorm}(\mathbf{x}^{(l-1)})\right)^p$$

    where:

    - $f_{\text{sr}}^{(l)}$: SIREN block (SineLayer)

    - $\text{LayerNorm}(\mathbf{x})$: Normalizes input to zero mean and
      unit variance per feature

    - $p = 2$: Power term fixed at 2 (element-wise squaring)

2.  For even-numbered layers ($l = 2, 4, 6, \ldots$):

$$\mathbf{x}^{(l)} = f_{\text{pn}}^{(l)}(\mathbf{x}^{(l-1)})$$

### Critical Rationale for LayerNorm

A critical enhancement to the standard SQR-SkipResNet is the application
of Layer Normalization to the skip path *before* the element-wise
squaring operation. During simulated close encounters, the inputs to
these layers (which represent positions and velocities) can vary over
orders of magnitude. Without normalization, the squaring operation would
amplify these large values, leading to catastrophic gradient explosions.
By normalizing the input on the skip path to have zero mean and unit
variance, this modification stabilizes the training process while
preserving the expressive power of the non-linear power term, which is
crucial for modeling the sharp transitions characteristic of close
encounters.

The default contract uses `elementwise_affine=False` (no learnable
affine parameters on the normalizer). Enabling affine parameters
(`elementwise_affine=True`) or removing LayerNorm entirely are optional
future ablations, not the Phase 20 default.

### Power Term Justification

The power term $p = 2$ remains critical for modeling non-smooth
dynamics. For 3-body systems, close encounters produce
velocity/acceleration spikes that require quadratic interaction terms to
resolve. $\text{LayerNorm}$ ensures this term remains bounded.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:206-263 -->

---

## Excerpt — §2.4 Finalized Architectural Hyperparameters

Source: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:264-283`

*Why it is in this round:* Depth, width, `first_omega_0`, `hidden_omega_0`, skip cadence, power term `p = 2`. GAP-56-02 (deferred) concerns this table's column header.

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:264-283 -->

## 2.4 Finalized Architectural Hyperparameters
Author Comment: I'm not sure why this section is formatted like this. It looks like broken syntax to me and it displays in the preview simply as a paragraph. Look into this.

**Table 1: Architectural hyperparameters of the SQR-SkipResNet-SIREN backbone**

| **Hyperparameter** | **Recommended Value** | **Rationale & Justification** |
| --- | --- | --- |
| Backbone | SQR-SkipResNet with SIREN layers | Superior stability and convergence for non-smooth dynamics, ideal for modeling close encounters in chaotic systems. |
| Depth | 12 hidden layers (6 SQR-SkipResNet blocks) | Provides a good balance between the expressive power needed for chaotic dynamics and the trainability on modest hardware. |
| Width | 256 neurons/layer | A strong default that balances model expressivity and computational cost, avoiding the diminishing returns of excessively wide layers.[1] |
| Activation | $\sin(\mathrm{x})$ (SIREN) | The $\mathrm{C}^\infty$-smoothness is mathematically essential for accurately calculating the second-order derivatives required in the physics loss.[1] |
| LayerNorm | elementwise_affine=False, eps=1e-5 | Stabilizes skip path gradients without restricting feature learning. Applied only to odd layers. |
| first_omega_0 | 30 | A high initial frequency injects a high-frequency basis into the network, helping it overcome spectral bias from the outset.[1] |
| hidden_omega_0 | 1 | This value is used within the principled weight initialization formula for hidden layers to ensure a stable distribution of activations, enabling deep network training.[1] |
| Weight Init. (First) | $\mathrm{U}\left[-\frac{1}{n_{\text{in}}}, \frac{1}{n_{\text{in}}}\right]$ | The mathematically-derived initialization for the first SIREN layer to create a random Fourier feature mapping.[1] |
| Weight Init. (Hidden) | $\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]$ | The principled initialization for all subsequent SIREN layers, designed to preserve activation variance and enable stable training of deep sinusoidal networks.[1] |
| Skip Cadence | Alternating (per SQR SkipResNet) | The alternating pattern of plain and power-enhanced residual layers effectively balances feature transformation and stable gradient flow.[1] |
| Power Term (p) | 2 (element-wise square) | Empirical results demonstrate that $p=2$ provides significant improvements in stability and accuracy without excessive computational overhead.[1] |
| Output Activation | None (Linear) | The final layer must be linear to allow the predicted positions to take on any real value required by the physical system. |


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:264-283 -->

---

## Excerpt — §3.2 Physics Residual Term, including the three Phase 56 contract blocks

Source: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:385-508`

*Why it is in this round:* The causal weights `w_n`, the amended exponent argument `R̃_b = R̄_b / R_ref`, the frozen `R_ref` procedure, and the 4096-row / 16-bin collocation contract (questions Q1, Q2, Q5).

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:385-508 -->

## 3.2 Physics Residual Term ($\mathcal{L}_{\text{physics}}$): Enforcing Newtonian Dynamics

This term is the heart of the \"physics-informed\" paradigm. It enforces
the governing laws of physics---in this case, Newton's law of universal
gravitation---across the entire solution domain, not just at the
discrete points where training data is available. This is what endows
the network with the ability to generalize and make physically
consistent predictions at any point in time.

The physics residual, $f_i(u_n)$, for each body $\mathrm{i}$ is defined
as the discrepancy between the acceleration predicted by the neural
network (via automatic differentiation) and the acceleration dictated by
the gravitational forces from all other bodies $\mathrm{j}$:

The softened gravitational force between bodies i and j uses the
Plummer-softened distance:

$$r_{safe,ij} = \sqrt{||r'_{\theta,j}(u_n) - r'_{\theta,i}(u_n)||^2 + \epsilon_{train}^2}$$

where $\epsilon_{train} = 10^{-5}$ (`10^-5`) is the training-time softening
parameter. The force per unit mass is:

$$F_{ij} = m_j \frac{r'_{\theta,j}(u_n) - r'_{\theta,i}(u_n)}{r_{safe,ij}^3}$$

The residual is:

$$f_i(u_n) = a'_{\theta,i}(u_n) - \sum_{j \neq i} F_{ij}$$

The raw-mass nondimensionalization convention absorbs `G`; no free
dimensionless gravitational coefficient appears in the scaled residual.

where:

- $u_n$ : Normalized physics time coordinate $t_n/T$

- $r'$ : Positions scaled by $D$ (characteristic length)

- $a'$ : Accelerations scaled by $D/T^2$

- $m_j$ : Masses (unchanged, as $G=1$ in the dimensionless system)

- $\epsilon_{train} = 10^{-5}$ (`10^-5`) : Training-time Plummer softening parameter to prevent
  division by zero during close encounters

Define the per-time residual energy as:

$$\bar R_n = \frac{1}{3}\sum_{i=1}^{3} \| f_i(u_n) \|^2.$$

For sorted collocation times $u_1 < \cdots < u_{N_t}$, the default
causal weights are:

$$w_1 = 1,\qquad
w_n = \exp\left(-\eta_c \sum_{m=1}^{n-1} \operatorname{stopgrad}(\bar R_m)\right),
\quad n>1.$$

The default physics loss consumed by $L_{total}$ is therefore:

$$L_{phys}^{causal} = \frac{1}{N_t} \sum_{n=1}^{N_t} w_n \bar R_n.$$

The unweighted mean $\frac{1}{N_t}\sum_n \bar R_n$ may be logged as a
diagnostic, but it is not the default training loss.

The governing form of the exponent's argument under the ratified
recalibration is given by the Phase 56 contract below.

> **Phase 35 contract: causal-training mode (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04; grounded by the resolution doc §1.1, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` GAP-32-01, and `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-04-causal-training-mode.md`).** This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`. Dense-residual ALM is rejected from the default loss, optional scalar-conservation ALM remains deferred P2 only, and the numeric causal-exponent clip bound is deferred to FUT. Option C time-windowed causal mechanics are not commissioned.

> **Phase 56 contract: causal-exponent argument amended (SPEC-01; SPEC-06; `54-RULING.md` checkpoint ② Block 1; owner delegation 2026-09-04; grounded by `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`).** The causal-weight coefficient retains its fixed ratified value `eta_c = 1`; what the exponent consumes is amended from the raw per-point residual to the frozen-reference normalized bin residual: `Rtilde_b = Rbar_b / R_ref`, so the causal weights are `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rtilde_m))`, formed as one batch-global exclusive sixteen-term prefix over the sixteen bin means — never over the collocation rows and never over a flattened ordering. This amendment supersedes Phase 35 D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A (LOSS-04; AC-LOSS-04), and the supersession reaches only the exponent's raw-residual argument and its one-point-per-prefix-term structure. New decision provenance: Owner instruction on 2026-09-04 expressly delegated checkpoint-② adjudication to the Codex primary agent using its best mathematical and scientific reasoning. After reading the trainex-r3 candidate document, Rule-19 verification report, premise adjudication, intake record, and routed gaps, that adjudication ratified `A1 + B2 (residual-wide) + C1 + D3 + E1`. This supersedes the Phase 35 ruling only as to the exponent's raw-residual argument and one-point-per-prefix-term structure; `η_c = 1` remains fixed. The Phase 35 contract blockquote directly above is retained as the historical record of the partially superseded ruling; where the two differ, this Phase 56 block governs. Re-issued acceptance criterion: AC-LOSS-04 is re-issued without a new identifier: the default Stage-0 causal loss uses exactly `η_c = 1`, `n_col = 4096` total per training batch, `M = 16` fixed equal-`u` bins with exactly 256 rows per bin, `R̃_b = R̄_b/R_ref`, one batch-global exclusive 16-bin prefix, and residual-wide normalization. Each of the fixed six initialization-probe cases uses exactly 4096 recorded-seed stratified times (256 per bin); `R_ref` is the finite positive median of the resulting 96 raw bin means, is detached and frozen, all 96 constituents and provenance are retained, and every trigger named in the checkpoint-② discharge section invalidates it. Raw and normalized diagnostics are both recorded; raw-unit thresholds are never silently applied to normalized values. GATE-04 must evaluate the actual full vectors and fail closed on any non-finite input, any floor-bound initialization weight, a degenerate weight vector, or a front that cannot respond to controlled residual reduction. A resampled training-batch front is diagnostic only; invariant-B evidence follows the fixed-monitor boundary above. GAP-54-06's L-BFGS question is not part of this criterion and must be settled at checkpoint ③ before RUN-04. This amendment does not decide the second-optimizer-phase and L-BFGS causal-weight recomputation semantics, which remain deferred to the Phase 57 owner checkpoint ③ (GAP-54-06), and it does not decide the train-free gate's condition-(ii) pass criterion, which is unratified and tracked as GAP-56-01.

> **Phase 56 contract: frozen residual reference (SPEC-01; GATE-04; GAP-54-03 RESOLVED-WITH-INSTRUCTION; `54-RULING.md` checkpoint ② B2 residual-wide; grounded by `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`).** The normalized bin residual is the raw bin mean divided by the frozen reference: `Rtilde_b = Rbar_b / R_ref`. The reference is the finite positive median of the 96 raw bin means produced at initialization by the fixed six-case GATE-04 probe — six cases times 16 bins — with each case using its recorded probe seed and exactly 4096 stratified times, 256 per bin. The statistic is a median under the convention that averages the two central order statistics of an even-length sample, so the value is reproducible by hand from the 96 recorded constituents; this is the convention the committed probe module records, and it differs from the lower-of-two convention some tensor libraries use. The reference is detached and frozen for the whole of Stage 0, is used in both the causal exponent and the outer training physics loss — the residual-wide application the ruling ratified — and is never updated online. All 96 constituents, the six cases, the statistic, the tree and configuration identity, and the invalidation inputs are persisted alongside the value. Reference invalidation (transcribed verbatim from `54-RULING.md`): Re-measure `R_ref` and re-run GATE-04 after any change to `first_omega_0`, depth, width, power-skip exponent, LayerNorm placement or stabilizer, initialization bounds, `D`, `T`, `epsilon_soft`, IC13 normalization, `n_col`, `M`, count unit, selected-slot semantics, or bin/allocation semantics. A resource failure at the ratified total batch count is a fail-closed result, not permission to reduce the count silently. This block fixes no numeric value of the reference: the ratified object is the procedure, and each gate run computes and persists its own value.

> **Phase 56 contract: collocation allocation and time draw amended (SPEC-06; SPEC-01; `54-RULING.md` checkpoint ② Block 4; GAP-39-12 RESOLVED-WITH-INSTRUCTION / owner-delegated Option C superseded in part; grounded by `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` and `.planning/milestones/v2.0-phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md`).** The collocation total is 4096 rows total per training batch — a total per batch, not a count per trajectory — and the ratified total is exact rather than a recommended range; it is not a tunable. The batch is stratified across 16 fixed equal-`u` bins: the first fifteen are half-open on the upper edge and the last is closed on both edges, so a time falling exactly on an interior boundary belongs to the bin that boundary opens, and the domain endpoint belongs to the final bin. Each bin holds exactly 256 rows, a bin residual is the mean over its 256 rows, and empty bins are impossible by construction, so the degenerate empty-input case cannot arise. Exactly one batch-global exclusive 16-term prefix is formed over the 16 bin means — never over the 4096 rows and never over a flattened ordering — so the ordering is the bin index and is stable. Batch allocation and bin policy (transcribed verbatim from `54-RULING.md`): The fixed bins are `[b/16,(b+1)/16)` for `b=0…14` and `[15/16,1]` for the last. In a 256-slot batch, draw one point per selected slot inside every bin. In a replay-only 240-slot batch, first draw one point per slot in every bin (`3840` rows), then use one canonical seeded permutation of the 240 slots: bins 0–14 each give a second draw to the next disjoint 16-slot slice of that permutation, and bin 15 gives a second draw to its first 16 slots. Each bin therefore has exactly 256 rows; 224 slots have 17 rows and 16 slots have 18, matching GAP-39-12's near-even quota. A bin residual is the mean over its 256 rows. Empty bins are impossible, and the causal prefix is one batch-global 16-bin prefix. This re-ratifies the time allocation only; energy continues to reuse the physics set. Microbatching preserves complete bin aggregates and never resets the prefix. This amendment supersedes GAP-39-12 RESOLVED-WITH-INSTRUCTION / owner-delegated Option C (2026-07-14) only as to that ruling's independent full-domain time-draw clause and nothing else; its total-budget, selected-slot multiplicity, exact-cardinality, near-even identity weighting, seeded determinism, and shared physics/energy-set requirements remain in force. Re-issued acceptance criterion: A full 256-slot batch emits exactly 4096 physics rows as one independently sampled time in each of 16 fixed bins for every selected slot. A 240-slot replay-only batch uses the seeded 3840-plus-256 remainder construction stated above, yielding exactly 256 rows per bin and per-slot totals 17 or 18. Replacement multiplicity is preserved; every bin is non-empty by construction; each bin residual is the mean of exactly 256 rows; one batch-global exclusive prefix is formed over the 16 bin means; energy reuses the same set; and microbatching preserves complete bin aggregates and never resets the prefix. Under SPEC-06, the collocation total the calibration binds to is the 4096-row total per training batch stated above; any change to that total, to the bin count, to the count unit, to the selected-slot semantics, or to the bin or allocation semantics invalidates the frozen reference and requires it to be re-measured and the train-free gate re-run, cross-referencing the invalidation list in the frozen-residual-reference block above rather than restating it.

**Run-driver reconciliation (SPEC-06; SCOPE-33; D-03).** The current run driver (`pinn/train.py:1033`) hard-codes `collocation_count = 16`, a count per call rather than the ratified per-batch total; the ratified calibration above binds instead to the 4096-row total per training batch, stratified across the 16 fixed bins with one batch-global exclusive 16-term prefix. The two are therefore divergent today. This divergence is disposed of here, in specification prose, under SPEC-06: the FUT-01 trainer rebuild must honour the ratified 4096-total / 16-bin structure, and no production Python file is edited by this milestone (SCOPE-33) to reconcile it.

**Collocation Point Sampling:**

The collocation points are sampled according to the following strategy:

``` {.python language="Python" caption="Listing 3: Collocation Points Sampling"}
import numpy as np

def sample_collocation_points(u_min=0.0, u_max=1.0, n_col=4096, strategy='uniform',
                            traj_data=None):
    """
    Sample normalized physics-time collocation points u in [0, 1].
    
    Args:
        u_min, u_max: Normalized physics-time boundaries (default: [0, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
        traj_data: Optional trajectory data for adaptive strategy
    
    Returns:
        u_col: Array of sampled normalized physics-time points
    """
    if strategy == 'uniform':
        u_col = np.random.uniform(u_min, u_max, size=(n_col,))
        
    elif strategy == 'adaptive':
        if traj_data is None:
            raise ValueError("Adaptive strategy requires traj_data")
        # Bias sampling toward high-acceleration regions
        weights = np.abs(traj_data['accelerations']).max(axis=1)
        
        # Safety check for degenerate cases
        if weights.sum() < 1e-8:
            weights = np.ones_like(weights)
            
        weights /= weights.sum()  # Normalize
        u_col = np.random.choice(traj_data['u'],
                                size=n_col, p=weights)
    else:
        raise ValueError("Invalid strategy")
        
    return u_col
```

**Recommended-range wording reconciliation (SPEC-06; D-11; closes 53-UNSWEPT-INVENTORY item 5).** Listing 3's docstring above still carries the `recommended: 2048-4096` range wording for `n_col`; that wording is historical. Under the ratified calibration, the collocation total is `n_col = 4096` rows total per training batch, fixed and exact rather than a tunable range. The listing above is left runnable and byte-unchanged; this paragraph is the reconciliation, not an edit to the listing.

Minimizing this term forces the network to learn a function
$\mathrm{r}_\theta(u)$ that is also a solution to the governing ordinary
differential equations (ODEs) in the normalized physics-time coordinate.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:385-508 -->

---

## Excerpt — §3.3 Initial Condition Anchor Loss

Source: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:509-532`

*Why it is in this round:* Defines the IC term, which dominates the logged total loss in the generation-7 run (master F-row on loss magnitudes).

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:509-532 -->

## 3.3 Initial Condition Anchor Loss ($L_{IC}$)

$$L_{IC} = L_{IC,r} + \beta_v L_{IC,v}$$

$$L_{IC,r} = (1/3) \sum_i ||r_{\theta,i}'(0) - r_i'(0)||^2$$

$$L_{IC,v} = (1/3) \sum_i ||v_{\theta,i}'(0) - v_i'(0)||^2$$

where $\beta_v = 1$ (`β_v = 1`) default, $\lambda_{IC} = 1$ default, and ablation
range $[0.1, 10]$. The velocity $v_\theta'(0)$ comes from the PHYS-02
componentwise normalized-time AD contract. This term is mandatory
(resolution §8.3).

This position and velocity anchor is evaluated at normalized physics
time `u=0`; because the network input uses $\tau = 2u - 1$, the
corresponding network-time input is `τ=-1`.

$L_{IC}$ uses squared error (not Huber): IC values come from
deterministic Phase 18 FRAME-01 preprocessing and are not outliers, so a
quadratic penalty enforces hard IC anchoring at `u=0`. $L_{data}$ uses
Huber (resolution §8.2) because data targets along the
curriculum-sampled trajectory are noisier and benefit from
outlier-robust loss.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:509-532 -->

---

## Excerpt — §4.1 Loss Balancing via Warmup Schedule (PHYS-05), incl. the causal-exponent clip guard

Source: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:669-724`

*Why it is in this round:* The `λ_phys` warmup (`I_warm`) and the clip's underflow-only purpose.

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:669-724 -->

## 4.1 Loss Balancing via Warmup Schedule (PHYS-05)

$$L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$

Canonical text form: $L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$.

where:

- $L_{data}$: Huber loss on position predictions, $\delta_r = 1$ default
  (resolution §8.2).
- $L_{IC}$: Initial condition anchor (position + velocity at `u=0`),
  $\lambda_{IC} = 1$ default.
- $L_{phys}^{causal}$: Physics residual with causal weighting
  $w_n = exp(-\eta_c \sum_{m<n} stopgrad(\bar R_m))$, $w_1 = 1$,
  $\eta_c = 1$ default. The exponent's governing argument is amended in §3.2 by the Phase 56 contract's re-issued acceptance criterion (AC-LOSS-04), not restated here. Use `stopgrad` in weights by default. Clip the
  causal exponent to avoid underflow, but do not choose a numeric
  clipping bound in Phase 19; surface a gap if one is needed.
  The causal exponent clip is required only to avoid underflow.

> **Phase 56 contract: causal-exponent clip underflow-only purpose NOT AMENDED (SPEC-01; SCOPE-38; GATE-04; `54-RULING.md` checkpoint ② Block 3; grounded by `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`).** This contract is **NOT AMENDED**: the ratified disposition is the retain option the ruling records (E1/D5-A), keeping the causal exponent clip's underflow-only purpose exactly as stated above. The dtype- and device-derived normal-floor guard (resolved at runtime by `resolve_causal_clip_facts`, never a copied literal) and the Phase 35 deferred-numeric-bound guard both stand unchanged; no numeric clipping bound is chosen by this record, and that deferral stands. The ruling's observability addendum is transcribed here: implementations additionally reject non-finite values before clipping, log the unclipped exponent and a per-step guard-binding count, and fail the train-free gate (GATE-04) if the guard binds at initialization. This added logging and gate-refusal behaviour is observability, not a repurposing of the clip as a floor-raiser.

- $L_{E}$: Soft energy conservation regularizer,
  see §3.4.
- $L_{L}$: Angular momentum conservation loss, see §3.5.
- No dedicated L_P term: linear momentum is enforced structurally by
  the Phase 17 COM projection head / zero-momentum output contract, so a
  separate linear-momentum loss would be redundant.

The warmup schedule is:

- $I_{warm} = min(2000, 0.1 \cdot N_{Adam,k})$
- $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
  $\lambda_{phys}^{max}(k) = 1$ **[LOCKED]**
- $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$ **[LOCKED]**
- $\lambda_E(k, i)$ and $\lambda_L(k, i)$ warm up linearly with
  $i/I_{warm}$

> **Phase 53 contract: PHYS-05 per-stage table locked and locked-vs-default convention (SPEC-02; SPEC-03; GAP-45-03 owner ruling 2026-07-24, option A; grounded by .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md).** The full PHYS-05 per-stage λ^max(k) table above binds for every stage k, boundary rows included - not merely the warmup form together with the cap at one. Preflight asserts the entire table at run start and at every stage boundary; overriding any tabulated value is a violation. The warmup form itself (the warmup-iteration count and the linear ramp) is retained under the Phase 35 LOSS-02 contract below; the locked-value markers bind the ruled per-stage values, not the ramp shape. This site is the locked-vs-default convention's first and only application in this phase; the default and recommended wordings elsewhere in this file are deliberately left unmarked and are inventoried, with per-item reasoning, in `.planning/phases/53-narrow-spec-codification/53-UNSWEPT-INVENTORY.md`. Generalization of the convention to other spec tables was explicitly NOT decided by this ruling (consequence 5), and remains open.

> **Phase 35 contract: energy-loss weights (LOSS-02; M15 rejected as issue-doc replacement; AC-LOSS-02; grounded by the resolution doc §1.9 and `.planning/phases/35-loss-energy-weight-contracts/evidence/m15-energy-weight-schedule.md`).** Retain the PHYS-05 warmup schedule above with `lambda_E^max <= 1` and scheduled conservation weights at or below one. The issue-doc cap-table replacement and stale high-energy-weight premise are rejected, not adopted as a locked schedule. Before any future control law, log weighted losses, scheduled weights, and gradient statistics; automatic dominance reweighting is deferred until measured weighted-loss/gradient evidence exists.

> **Phase 35 guard: source precedence and deferred values (LOSS-02 / LOSS-03 / LOSS-04; AC-LOSS-02 / AC-LOSS-03 / AC-LOSS-04).** The Phase 35 evidence packets supersede issue-doc replacement proposals for this component catalog: Option C windowed-causal mechanics are not commissioned, automatic dominance reweighting is deferred, dense-residual ALM is rejected from the default loss, stage-indexed Huber-delta calibration is deferred, and `ctl_instruction.md` remains the total-loss assembly home while this file remains the component-formula home.

Optimizer-phase semantics:

- During Adam epochs: $\lambda$ values may be scheduled per the warmup
  schedule; no dual variables are updated.
- During L-BFGS: $\lambda$ values are frozen; no dual updates inside a
  line search.
- Stage-boundary transitions: re-warmup applies per the new stage's
  $\lambda^{max}$ values.

The default loss is the penalty-term formulation above. Scalar
conservation augmented-Lagrangian machinery is not part of the baseline
training contract and is documented separately as the P2 ablation below.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:669-724 -->

---

## Excerpt — §4.3 Two-Phase Optimization + §4.4 Adaptive Gradient Clipping

Source: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:748-814`

*Why it is in this round:* The Adam→L-BFGS split and the gradient clipping the run uses (questions Q1, Q4).

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:748-814 -->

## 4.3 Two-Phase Optimization

To achieve both efficient exploration and high-precision convergence, a
two-phase optimization strategy is employed.

1.  **Phase 1 (Exploration):** The initial training phase utilizes the
    **Adam optimizer**. Its adaptive learning rates and momentum-based
    updates are well-suited for navigating the highly non-convex loss
    landscape in the early stages of training, efficiently finding a
    good basin of attraction.

2.  **Phase 2 (Fine-Tuning):** Once the Adam optimizer has converged,
    the process can be switched to a quasi-Newton method like **L-BFGS**
    to \"polish\" the solution. Because full-batch L-BFGS is
    memory-intensive, a mini-batch variant (Stochastic L-BFGS) is
    recommended for larger datasets.

## 4.4 Adaptive Gradient Clipping

> **Phase 34 contract: adaptive median-based gradient clipping (LOOP-04; M14 modified/accept-resolution; AC-LOOP-04; grounded by the resolution doc §1.8 and `evidence/m14-gradient-clipping.md`).**

A significant challenge arises from the inverse-square distance terms in
the loss function, which can explode during simulated close encounters.
To prevent a single event from destabilizing the optimizer, adaptive
gradient clipping is essential. A robust strategy is to clip the global
L2 norm of the gradients relative to their recent typical magnitude.

The merged clipping mechanism is **locked**: during Adam epochs only,
the clip value is the product of the curriculum-aware stage multiplier
$C_{\text{stage}}$ and the median of recent global gradient norms,
computed over a rolling window of recent global gradient norms. The
per-stage multiplier $C_{\text{stage}}$ is defined canonically in
`ctl_instruction.md` under **Adaptive Median-Based Gradient Clipping**
(AC-LOOP-04); this section owns the mechanism, not the schedule values.
The fixed multiplier `5.0` that appeared in the pre-Phase-34
`pinn_architecture.md` pseudocode is the Stage 2/3 instance
($C_{\text{stage}} = 5$) or a fallback, not an additional multiplier.

**Adam-only scope.** No gradient clipping is applied during L-BFGS
refinement; the line-search trust region already bounds the step.

``` {.python language="Python" caption="Listing 6: Adaptive Gradient Clipping Logic (normative spec contract — not executable; FUT-01/FUT-04 implements)"}
# Maintain a queue/list of the last 100 gradient norms
grad_history = [] 

# In training loop, after loss.backward():
total_norm = torch.norm(torch.stack([torch.norm(p.grad.detach()) for p in model.parameters()]))
grad_history.append(total_norm)
if len(grad_history) > 100:
    grad_history.pop(0)

# Clip norm to C_stage times the median of recent norms
clip_value = C_stage * torch.median(torch.stack(grad_history))
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)

# Then, call optimizer.step()
```

**Deferred → FUT execution constants.** The exact early-stage value of
$C_{\text{stage}}$ within the Stage 0-1 range, the bootstrap median fallback
used before the history window is populated, the lower floor (e.g.
`1e-6`) on the median, and the gradient-history reset mechanics at stage
boundaries are routed to Phase 34/FUT calibration. They are explicitly
left open by the M14 packet owner-route and resolution-doc §1.8
(GAP-08); this contract does not invent them and does not tag the
early-stage value as locked.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:748-814 -->

---

## Excerpt — Step 5: Curriculum Stage Assignment

Source: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1600-1666`

*Why it is in this round:* Defines Stage 0, the only stage in scope.

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1600-1666 -->

## Step 5: Curriculum Stage Assignment

Now, assign a curriculum stage label (an integer from 0 to 6) to each
simulation. This is achieved by applying the specific threshold criteria
defined in this document in section 2.3 on 'Multi-Stage Data
Stratification by Difficulty'. This process should be fully automated in
a script that reads the table of computed invariants and outputs a
mapping from each simulation ID to its assigned stage index. The stage
mapping is keyed by `record_key`, never by positional index, per the
Step-1 ID-resolution contract (Step 1 item 7); only trajectories admitted
by the Step 1A gate appear in this mapping. (Stage-label obligation is
per-ID, not per-simulation: every Stage-4-admitted ID owes a Stage-5 gold
sample — GAP-26-01 resolved 2026-06-13, OI-7a; see the resolved
gold-counterpart note below.)

**Gold-counterpart contract (data-side, mandatory).** A standard
`physical_key` may lack a gold-resolution realization (verified: 184
standard IDs have no gold counterpart). The loader MUST handle this as a
data-side invariant, independently of any Stage-5 fallback policy:

- The gold-missing set is computed at init as the set difference of the
  scanned base and gold ID sets, cross-checked against the verified 184-ID
  list in `standard_quasi_random_ids_not_in_gold.md` (discrepancies
  logged). The set is never hard-coded.
- Each `physical_key` carries metadata `gold_counterpart ∈ {present,
  absent}`.
- The Stage-5 stratum (Set 2b, gold standard) is built by iterating the
  gold folder's actual files, never by base-ID lookup into the gold index
  (which would manufacture 184 spurious misses by construction).
- A base-fidelity record is never silently substituted into a
  gold-resolution slot.

> **RESOLVED — Stage-5 labels attach to IDs (GAP-26-01, framework-owner
> ruling 2026-06-13, OI-7a).** The label-semantics question — do Stage-5
> stage labels attach to *simulations* (`record_key`) or to *IDs* — is
> ruled in favor of **IDs**: every Stage-4-admitted ID owes a Stage-5
> gold sample. Under this ruling the 184 standard IDs without a gold
> counterpart are **genuine Stage-5 gold holes** (the per-simulation
> no-fallback entailment is rejected, because it presupposed the
> simulations reading). The resolution is a **data-generation
> remediation, not a loader fallback**: the framework owner directed that
> the missing gold counterparts for the 184 standard IDs be **re-simulated
> to restore a 1:1 base:gold correspondence** (OI-7b, activated 2026-06-13).
> No base→gold substitution is introduced (the mandatory data-side
> contract above already forbids it and stays in force), and no silent
> skip. **Pending re-simulation**, each affected ID carries
> `gold_counterpart = absent` and contributes no gold Stage-5 sample; the
> loader's gold-missing set (the set-difference machinery in the contract
> above) is the **remediation backlog**, expected to be empty once the
> re-simulated gold trajectories land and validate. **Forward dependency
> (not yet executed):** the 184 gold re-simulations are a data-generation
> prerequisite for a complete gold Stage-5 stratum (OI-7b). See
> `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/m13-gold-counterpart.md`.

> **Phase 33 contract: stage-label materialization (CURR-01; D-33-01,
> D-33-02, D-33-03; AC-CURR-01; grounded by GAP-33-01).** The offline
> admitted-set EDA -> robust transforms -> PCA -> clustering -> quantile
> threshold methodology (see "Multi-Stage Data Stratification by Difficulty"
> Phase 33 contract above) **augments** the static theoretical anchors and
> materializes a stable integer stage label keyed by `record_key` for every
> Step-1A-admitted trajectory. Stage labels are integers 0..6 from the inventory
> defined in §2.3; the mapping is **owner-pending** the FUT admitted-set EDA
> run (SCOPE-15). The **population safeguard value is owner-pending** the FUT
> admitted-set EDA; no 5% / `>10%` / adaptive floor is locked in Phase 33. The
> Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles are
> preserved.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1600-1666 -->

---

## Excerpt — Loss Function Formulation — Phase 2: Total Training Loss

Source: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1742-1787`

*Why it is in this round:* How the causally weighted physics term enters the total loss beside the data, IC, energy, and angular-momentum terms.

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1742-1787 -->

## Loss Function Formulation

### Phase 2: Total Training Loss

The default training loss is:

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{data}} + \lambda_{\mathrm{IC}} \, \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{phys}} \, \mathcal{L}_{\mathrm{phys}}^{\mathrm{causal}} + \lambda_E \, \mathcal{L}_E + \lambda_L \, \mathcal{L}_L
$$

where each term is defined by name in the PHYS-05 loss-term catalog in
`pinn_architecture.md` ($\mathcal{L}_{\mathrm{data}}$, $\mathcal{L}_{\mathrm{IC}}$, $\mathcal{L}_{\mathrm{phys}}^{\mathrm{causal}}$, $\mathcal{L}_E$, and $\mathcal{L}_L$).
The loss-balancing contract, warmup schedule, and optimizer-phase semantics
are defined in the PHYS-05 training-loss contract in `pinn_architecture.md`.

> **Phase 35 contract: loss scaling and units (LOSS-01; NS-18 modified / NS-12 accepted; AC-LOSS-01 / AC-LOSS-01-AD; grounded by the resolution doc §§1.12/1.14 and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md` / `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-12-componentwise-ad.md`).** This `ctl_instruction.md` section owns dimensionless total-loss assembly and methodology; `pinn_architecture.md` owns the component math in **Data Fidelity Term**, **Physics Residual Term**, **Soft Energy Conservation Regularizer**, **Angular Momentum Conservation Loss**, and **Loss Balancing via Warmup Schedule (PHYS-05)**. The assembly contract keeps all terms in the same dimensionless coordinate system (`u=t/T`, `tau = 2u - 1`, scaled positions `r'=r/D`), preserves the Phase 34 separation between data-fidelity snapshot points and physics/energy collocation points, and records that energy reuses the physics collocation set. Component details remain in `pinn_architecture.md`: Huber data loss on projected scaled positions, componentwise AD with conditional tau/u chain factors, matched `epsilon_train = 1e-5` in physics and energy, raw-mass force/COM metadata, the IC anchor, the angular-momentum regularizer, and no linear-momentum / no-linear-momentum-loss term.

> **Phase 35 contract: energy-loss weights (LOSS-02; M15 rejected as issue-doc replacement; AC-LOSS-02; grounded by the resolution doc §1.9 and `.planning/phases/35-loss-energy-weight-contracts/evidence/m15-energy-weight-schedule.md`).** Total-loss assembly retains the PHYS-05 schedule in `pinn_architecture.md` with `lambda_E^max <= 1` and scheduled conservation weights at or below one. The issue-doc replacement schedule and stale high-weight premise are rejected, not adopted. Before any future control law, training instrumentation must log weighted losses, scheduled weights, and gradient statistics; automatic dominance reweighting is deferred until measured weighted-loss/gradient evidence exists.

> **Phase 35 contract: energy Huber delta (LOSS-03; NS-13 defer / deferred calibration; AC-LOSS-03; grounded by the resolution doc §1.13 and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-13-energy-huber-delta.md`).** Total-loss assembly uses the `pinn_architecture.md` **Soft Energy Conservation Regularizer** component as the canonical math home and keeps `delta_E = 1.0` as the configurable current baseline. Any stage-indexed or quantile-calibrated Huber transition is deferred until normalized `|Delta H|` quantiles, linear-branch occupancy, validation energy drift, and weighted gradients are measured.

**Optimizer-phase semantics (PHYS-05):** During Adam epochs, hyperparameters
(`λ` values) may be scheduled per the warmup schedule. During L-BFGS, `λ`
values are frozen and no dual updates occur inside a line search.
Stage-boundary transitions apply re-warmup per the new stage's
`λ_phys^max` / `λ_E^max` / `λ_L^max`.

> **Phase 35 contract: causal-training mode (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04; grounded by the resolution doc §1.1, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` GAP-32-01, and `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-04-causal-training-mode.md`).** Total-loss assembly uses the `pinn_architecture.md` **Physics Residual Term** component as the canonical math home for the per-time causal weighting and keeps `w_1 = 1` and `eta_c = 1` as the current defaults; the causal-weight formula body is defined there (see AC-LOSS-04) and is not restated in this assembly file. Dense-residual pseudo-ALM is rejected from the default loss, optional scalar-conservation ALM remains deferred P2 only, Option C / windowed-causal mechanics are not commissioned, and the numeric causal-exponent clip bound is deferred to FUT.

> **Phase 35 guard: source precedence and assembly ownership (LOSS-02 / LOSS-03 / LOSS-04; AC-LOSS-02 / AC-LOSS-03 / AC-LOSS-04).** Stale issue-doc replacement constructs are not default loss contracts: automatic dominance reweighting is deferred; dense-residual ALM is rejected from the default loss; Option C / windowed-causal mechanics are not commissioned; stage-indexed Huber calibration is deferred. This file owns total-loss assembly and methodology, while `pinn_architecture.md` remains the component-formula home.

**Causal weighting (PHYS-05 default):** Dense ODE residuals use the owner-ratified causal weighting baseline above, with stopgrad in weights by default to prevent the weight mechanism from becoming an adversarial term. The exponent must be clipped to avoid underflow, but no numeric clipping bound is selected in Phase 35; the bound remains deferred to FUT.

The previous pseudo-ALM formulation (`L_data + λ_p·L_phys + (μ_p/2)·L_phys² + λ_E(k)·L_energy`) is rejected because squaring a nonnegative MSE produces a quartic residual that does not represent a standard equality-constrained augmented Lagrangian. Optional ALM for scalar conservation constraints only is documented as a P2 ablation in the PHYS-05 ablation section of `pinn_architecture.md`.

**Per-step ordering skeleton (Adam epoch).** The default training step follows this order, treating each loss term as an opaque input whose component definition, weight schedule (`λ_E`, `λ_L`, etc.), and Huber-δ calibration are owned by Phase 35. The placeholder `L_total` names the assembled scalar loss:

1. **Forward pass** over the concatenated data-fidelity and collocation point sets.
2. **Assemble** the total loss `L_total` (\mathcal{L}_{\text{total}}) from the named loss components using the current scheduled weights.
3. **Backward pass** to compute gradients (`L_total.backward()`).
4. **Adam-only median-based global gradient clip**, using the mechanism defined canonically in `pinn_architecture.md` §4.4 **Adaptive Gradient Clipping** (AC-LOOP-04); this section does not restate the formula.
5. **`optimizer.step()`** to update network weights.
6. **Optional scalar-ALM dual update**, applicable only to the optional scalar-conservation ALM ablation documented in `pinn_architecture.md` §4.2 (LOOP-05 deferred); the default training step has **no** dense-residual ALM update.

During L-BFGS, no gradient clipping is applied and no dual variables are updated inside a line search.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1742-1787 -->

---

## Excerpt — Phase 2a: Adam-driven Exploration + Phase 2b: High-Precision L-BFGS Refinement

Source: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1788-1921`

*Why it is in this round:* The initial learning rate, the cosine annealing "over the phase", the L-BFGS handoff criterion, and the L-BFGS segment (questions Q1, Q4).

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1788-1921 -->

## Phase 2a: Adam-driven Exploration

The initial phase uses Adam for robust navigation of non-convex loss
landscapes.

### Initialization

At the beginning of a new stage $k$:

- Load network weights from the converged model of stage $k-1$ (if
  $k > 0$).

- **Critical**: Completely reset Adam's internal state (momentum
  buffers) to prevent biased gradient statistics from prior data.

- Set initial learning rate: $\text{LR}_k = 10^{-3} \times (0.7)^k$.

- Initialize a cosine annealing scheduler to decay the learning rate
  over the phase.

- Set Adam parameters: $\beta_1 = 0.9$, $\beta_2 = 0.999$,
  $\epsilon=1e-8$.

### Mini-Batch Construction with Lookahead Sampling

> **Phase 34 contract: replay/lookahead batch construction (LOOP-01; provisional; AC-LOOP-01; grounded by the resolution doc §1.4 and `evidence/b-07-replay-lookahead-batching.md`).** This `ctl_instruction.md` section is the **canonical** batch-construction contract (SI-PINN-003); `pinn_architecture.md` points here rather than duplicating the rule.

For a 256-trajectory training batch at curriculum stage $k$:

- **Replay set** `B_replay = 240` trajectories drawn from stages $\leq k$ ($B_{\text{replay}} = 240$).
- **Look-ahead set** `B_lookahead = 16` trajectories drawn from stage $k+1$ ($B_{\text{lookahead}} = 16$), **gated by `has_stage(k+1)`**.
- **Per-trajectory data-loss point count** `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, sampled **without replacement**; `n_pts_cap = 32`.

All values are tagged **provisional** (B-07 `modified`: "provisional defaults, not verified optimums").

> **D-04 causal-mode compatibility note (LOSS-04; RESOLVED-WITH-INSTRUCTION Option A).** GAP-32-01 ratified the current per-time causal weighting baseline for Phase 35, so this batch-construction contract does not add Option C / windowed-causal mechanics; that design is not commissioned and not part of the default loss. The replay/lookahead contract remains compatible with the retained Option A because no future-window partitioning is introduced.

> **Phase 34 contract: batch edge-case policy (LOOP-01; provisional; resolved by owner instruction — GAP-34-01 RESOLVED-WITH-INSTRUCTION 2026-06-25, Option A via UAT).** The three batch edge cases flagged by B-07 §1.4 as needing determinism are resolved by owner-ratified **Option A**, each carrying the LOOP-01 `provisional` tag (B-07 `modified`):
>
> 1. **Final stage** — when `has_stage(k+1)` is false there is no look-ahead set, so the batch trains on the **replay set only** (`B_lookahead = 0`).
> 2. **Undersized look-ahead pool** — when the stage `k+1` pool has fewer than `B_lookahead = 16` eligible trajectories, the look-ahead set is **padded by sampling with replacement** from the available pool, holding the batch size fixed at `B_replay + B_lookahead = 240 + 16`.
> 3. **Replay sampling** — the replay set is **sampled without replacement** across the epoch (standard once-per-epoch coverage).
>
> These are provisional defaults (B-07 `modified`), not verified optimums; owner-ratified Option A — see `34-GAPS.md` GAP-34-01 (RESOLVED-WITH-INSTRUCTION).

> **Phase 34 contract: data versus collocation points (LOOP-02; provisional; AC-LOOP-02; grounded by the resolution doc §1.5 and `evidence/b-08-data-vs-collocation-points.md`).**

The training batch consists of two logically independent point sets:

1. **Data-fidelity points**: sampled from the discrete BRUTUS trajectory snapshots (the replay/lookahead trajectories above), used for the Huber data loss $\mathcal{L}_{\text{data}}$.
2. **Collocation points**: continuous samples from $[0,T]$ for the physics residual $\mathcal{L}_{\text{phys}}^{\text{causal}}$ and the energy residual $\mathcal{L}_E$ (energy reuses the physics collocation set).

A single concatenated forward pass over both point sets is permitted for implementation efficiency, but it does **not** merge the loss roles: data loss is evaluated only at snapshot times, and physics/energy losses are evaluated only at their respective collocation times. The budgets `8192` data points and `4096` collocation points are **provisional/example budgets** (B-08 `modified`); the actual data count follows the per-trajectory cap `min(n_pts_cap, n_snapshots(traj))`.

> **Phase 34 contract: mixed time sampling (LOOP-03; data retained / collocation deferred; grounded by the resolution doc §§1.4–1.5 and the B-07/B-08 evidence packets).**

- **Data-fidelity points — 50/50 retained:** The existing 50/50 split (uniform + acceleration-weighted, without replacement, Gumbel-top-k) is **retained** for data-fidelity points. For `n_pts(traj)` points, draw `k_w = floor(n_pts/2)` acceleration-norm-weighted samples, then `n_pts - k_w` uniform samples from the remainder.
- **Collocation points — 50/50 deferred:** A mandatory 50/50 mixed continuous collocation sampler is **deferred** (B-08 / GAP-06); Phase 34 does not mandate it. The current uniform/adaptive collocation choices remain usable.

> **Per-trajectory data-loss point count and snapshot metadata.** `n_pts_cap` defaults to 32 (the spec's example value; not evidence-based -- revisit with admitted-set snapshot distributions; exposed as a configuration knob). The 50/50 composition is realized as: `k_w = floor(n_pts/2)` acceleration-norm-weighted draws without replacement (Gumbel-top-k), then `n_pts - k_w` uniform draws without replacement from the remainder; all draws from a seeded generator. The loader exposes `n_snapshots(traj)` and `dt_out(traj)` as metadata (forward interface for the deferred M16 collocation-density question -- doc-03; not used here). **No `0.5 x n_snapshots` factor is imposed** (unevidenced; see Q-B1 resolution).
>
> Citation: locked M12 verdict in `evidence/m11-m12-severity.md` (Phase 25 EVID-10). Verified snapshot-count medians (DATA-06, CLM-10): 61 standard-base / 127 hierarchical-base / 1003 gold. These are population medians, not hard per-file guarantees.

> **Phase 34 contract: `dt_out`-aware collocation scaling (LOOP-06; deferred; AC-LOOP-06; grounded by the resolution doc §1.10 and `evidence/m16-dt-out-collocation-scaling.md`).**
>
> `dt_out`-aware collocation scaling is **deferred to FUT**. The loader keeps `dt_out(traj)` and `n_snapshots(traj)` exposed as metadata, and the present fixed/configurable collocation budget is retained. The audit direction `n_col \propto dt_base/dt_out` is recorded **only** as a deferred candidate direction — not as a locked or probe-able contract — and the inverse form `n_col \propto dt_out/dt_base` is explicitly **not adopted**. The v1.5 SCOPE-11/PIPE-08 forward-reference is **realized-as-deferred**.

### Adaptive Median-Based Gradient Clipping

> **Phase 34 contract: curriculum-aware C-schedule (LOOP-04; M14 modified/accept-resolution; AC-LOOP-04; grounded by the resolution doc §1.8 and `evidence/m14-gradient-clipping.md`).**

Use adaptive global-norm clipping to handle gradient explosions from
close encounters. The clipping **mechanism** is defined canonically in
`pinn_architecture.md` §4.4 **Adaptive Gradient Clipping** (AC-LOOP-04):
during Adam only, the global L2 norm is clipped to the
$C_{\text{stage}} \cdot \text{median}$ value over a rolling window of
recent global gradient norms. This section owns only the per-stage
multiplier $C_{\text{stage}}$.

**Curriculum-aware $C_{\text{stage}}$ schedule (locked):**

| Curriculum stage | Data difficulty | $C_{\text{stage}}$ |
|---|---|---:|
| 0-1 | quasi-periodic orbits | 7-10 |
| 2-3 | onset of mild chaos | 5 |
| 4-6 | frequent close encounters | 3 |

The Stage 2/3 value $C_{\text{stage}} = 5$ (hence the fixed `5.0`
multiplier in the pre-Phase-34 `pinn_architecture.md` pseudocode) is the
instance that explains that pseudocode; it is also the natural fallback
when no stage-specific value is selected.

**Adam-only scope.** No gradient clipping during L-BFGS, as line-search
creates a trust region.

**Deferred → FUT execution constants.** The exact early-stage
$C_{\text{stage}}$ within the Stage 0-1 range, the bootstrap median fallback
used before the history window is populated, the lower floor (e.g.
`1e-6`) on the median, and the gradient-history reset mechanics at stage
boundaries are routed to Phase 34/FUT calibration. They are explicitly
left open by the M14 packet owner-route and resolution-doc §1.8
(GAP-08); this contract does not invent them and does not tag the
early-stage value as locked.

### Termination Criterion

Hand off to L-BFGS when the physics loss plateaus:
$$\frac{d(\log_{10} \mathcal{L}_{\text{phys}})}{d(\text{epoch})} > -5 \times 10^{-3} \quad \text{for 50 consecutive epochs}$$

## Phase 2b: High-Precision L-BFGS Refinement

Hand off to L-BFGS to polish the solution and minimize residuals.

### Optimizer Selection by Dataset Size

The L-BFGS variant depends on cumulative dataset size.

**Early Stages (0-2): Full-Batch L-BFGS**

- Use standard full-batch on the entire dataset.

- Parameters: history size: 10, line search: "Wolfe", max iterations:
  20-50.

**Later Stages (3-6): Stochastic L-BFGS (sL-BFGS)**

- Switch to mini-batch variant for memory efficiency.

- Parameters: batch size: 32, curvature interval: update every 10
  iterations.

**Important**: No gradient clipping during L-BFGS, as line-search
creates a trust region.


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1788-1921 -->

---

## Excerpt — Stage Transition Criteria + Consolidated Hyperparameter Schedule

Source: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1922-2011`

*Why it is in this round:* Stage-exit conditions, the provisional per-stage epoch budget, and the consolidated schedule (question Q4).

<!-- BEGIN VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1922-2011 -->

## Stage Transition Criteria

> **Phase 33 contract: dual-path stage-transition state machine (CURR-03;
> D-33-08, D-33-09; AC-CURR-03; grounded by the resolution doc §1.11 and
> `evidence/d5-stage-transitions.md`).** Within each curriculum stage, the
> training loop's stage-exit decision is an operational state machine with
> three dispositions: **ADVANCE**, **RECOVER**, and **HALT/REVIEW**. There is
> no automatic fallback-advancement path: a stage that cannot reach the
> approved success gate either retries transient numerical failure via
> **RECOVER** or blocks progression via **HALT/REVIEW** until the owner
> explicitly authorizes degraded advancement. All numeric thresholds, epoch
> tables, stagnation windows, retry limits, and percentile relaxations in
> this section are **provisional pending FUT Stage-0 pilot calibration**
> (SCOPE-14); the spec records the *form* of the success gate and the
> state-machine contract, not calibrated values.

**ADVANCE — the only path to the next stage.** ADVANCE is permitted only when
the approved success gate passes on the held-out validation set (hold-out
10-20% of cumulative data per stage). The success gate is the conjunction of
the four criteria below: training-loss plateau, validation-loss stability, the
stage-dependent physics-residual threshold, and the energy-conservation check.
The issue-doc "fallback advancement" framing that treats `MAX_EPOCHS`,
stagnation, or NaN/Inf as alternate *advancement* triggers is **rejected**: it
silently relaxes the success criterion. Those conditions instead route to
**HALT/REVIEW** or **RECOVER** below.

### 1. Training-Loss Plateau (ADVANCE criterion 1 of 4)

Relative change in smoothed total loss below threshold:
$$\frac{|\mathcal{L}_{\text{smooth}}(i) - \mathcal{L}_{\text{smooth}}(i - \text{patience})|}{\mathcal{L}_{\text{smooth}}(i)} < \epsilon_{\text{plateau}}$$
where
$\mathcal{L}_{\text{smooth}}(i) = \beta \cdot \mathcal{L}_{\text{smooth}}(i-1) + (1-\beta) \cdot \mathcal{L}_{\text{train,total}}(i)$,
$\beta = 0.98$, patience = 200, $\epsilon_{\text{plateau}} = 10^{-5}$.
Initialize $\mathcal{L}_{\text{smooth}}(0)$ as the first computed loss. These
numeric values are provisional pending Stage-0 pilot calibration.

### 2. Validation-Loss Stability (ADVANCE criterion 2 of 4)

Current validation loss $\leq$ minimum seen in stage:
$$\mathcal{L}_{\text{val}}(i) \leq \min_{j \leq i} \mathcal{L}_{\text{val}}(j)$$

### 3. Physics-Residual Threshold (ADVANCE criterion 3 of 4, stage-dependent)

Validation physics loss below threshold:
$$\mathcal{L}_{\text{phys}}^{\text{val}} < \epsilon_{\text{phys}} \quad (\epsilon_{\text{phys}} = 10^{-4})$$
The per-stage `epsilon_phys` table that appears in the issue doc is
**claimed-unverified** (D5-05; CLM-08/09) and is not transcribed as locked;
the threshold value remains provisional pending Stage-0 pilot calibration.

### 4. Energy-Conservation Check (ADVANCE criterion 4 of 4)

Average relative energy drift below threshold, using the persisted
PHYS-04/D-20 (GAP-19-01) energy denominator floor `epsilon_H = 1e-4 * S_H`
(unchanged by Phase 33):
$$\frac{1}{N_{\text{traj}}} \sum_{j=1}^{N_{\text{traj}}} \frac{|H_j(t_{\text{final}}) - H_j(0)|}{|H_j(0)| + \epsilon_H} < \epsilon_{\text{energy}} \quad (\epsilon_{\text{energy}} = 10^{-4})$$

**RECOVER — transient numerical failure, not a progression path.** If training
produces NaN or Inf gradients (typically during close-encounter stages), the
loop rolls back to the last well-formed checkpoint and retries with a bounded
retry budget. RECOVER does not advance the curriculum; it restores a
numerically valid state from which ADVANCE can be re-evaluated. Retry limits
are provisional pending Stage-0 pilot calibration. If the retry budget is
exhausted without restoring a valid state, the stage transitions to
**HALT/REVIEW**, not to ADVANCE.

**HALT/REVIEW — blocked progression, owner authorization required for any
degraded advancement.** If a stage reaches its per-stage max-epoch budget
without satisfying the ADVANCE success gate, or if validation loss stagnates
above the ADVANCE threshold for the stagnation window, the loop halts and
surfaces the stage for owner review. No automatic degraded advancement is
authorized: advancing the curriculum past a failed success gate requires an
explicit owner decision (logged in the gap register with the justification
and the relaxation applied). The per-stage `MAX_EPOCHS` table, the stagnation
window, and the percentile-10 relaxation that appear in the issue doc are
**claimed-unverified** (D5-05; CLM-08/09) and are not transcribed as locked
thresholds; they remain provisional pending Stage-0 pilot calibration.

## Consolidated Hyperparameter Schedule

| Stage | Adam LR (Initial) | Clip `C` | Loss-weight schedule | L-BFGS Type |
|---|---|---|---|---|
| 0-1 | $10^{-3} \times (0.7)^k$ | See AC-LOOP-04 | See PHYS-05 warmup schedule in `pinn_architecture.md` | Full-Batch |
| 2-3 | $10^{-3} \times (0.7)^k$ | See AC-LOOP-04 | See PHYS-05 warmup schedule in `pinn_architecture.md` | Full-Batch / sL-BFGS |
| 4-6 | $10^{-3} \times (0.7)^k$ | See AC-LOOP-04 | See PHYS-05 warmup schedule in `pinn_architecture.md` | sL-BFGS |

*Stage-by-stage guide for key dynamic hyperparameters. The canonical
C-schedule values live only in the Adaptive Median-Based Gradient
Clipping section above (AC-LOOP-04); this table points to them rather
than duplicating them.*


<!-- END VERBATIM pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1922-2011 -->

---
