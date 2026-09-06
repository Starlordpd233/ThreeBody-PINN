---
author: Starlordpd233
date: 2026-03-21
---

# A Definitive Implementation Blueprint for a Hybrid SQR-SkipResNet-SIREN PINN with Soft Conservation Regularization for $\mathrm{N}$-Body Dynamics

**Notation convention - locked vs. default values.** Two inline markers record the
ratification status of a numeric value in this specification and in
`ctl_instruction.md`. **[LOCKED]** marks a value that is owner-ratified and
contract-fixed: the value binds as written, and overriding it is a violation
rather than a tuning choice. **[DEFAULT]** marks an illustrative default: a value
offered as a reasonable starting point, which a later phase may change without
re-ratification. A marker attaches to a value, not to a table row, so the same
convention applies to markdown table cells, prose bullets, and displayed LaTeX
lines alike. The markers are machine-checkable status annotations, distinct from
the preserved editorial notes recorded in SI-PINN-002, which were historically
rendered as bold bracketed text of the same shape. This convention governs both
framework specs; Phase 53 applies it only within Section 4.1 of this file and
makes no marker edits in `ctl_instruction.md`.

# 1. Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems

The accurate and long-term simulation of $\mathrm{N}$-body gravitational
systems, particularly the notoriously chaotic three-body problem,
presents a formidable challenge for traditional numerical and machine
learning methods alike. The dynamics are characterized by an extreme
sensitivity to initial conditions, where infinitesimal perturbations can
lead to exponentially divergent trajectories over time. Furthermore, the
solutions often contain a complex mixture of smooth, quasi-periodic
motion and sharp, high-frequency events that occur during close
encounters between bodies. A successful predictive model must therefore
not only capture these multi-scale temporal features with high fidelity
but also adhere to fundamental global conservation laws, such as the
conservation of total energy and angular momentum, to ensure its
long-term physical plausibility.[1]

A generic neural network architecture, such as a standard Multi-Layer
Perceptron (MLP), lacks the specific structural priors necessary to
handle this confluence of challenges. Such models often suffer from a
\"spectral bias,\" a tendency to learn low-frequency functions more
easily, which makes them struggle to represent the high-frequency
components inherent in chaotic dynamics.[2] More critically, enforcing
the governing physical laws---in this case, Newton's laws of
motion---within a Physics-Informed Neural Network (PINN) framework
requires the computation of high-order derivatives of the network's
output. For the $\mathrm{N}$-body problem, this involves calculating the
second derivative of the predicted position with respect to time,
$\frac{\mathrm{d}^2 \mathrm{r}}{\mathrm{d} t^2}$, to form the physics
residual term in the loss function. Common activation functions like the
Rectified Linear Unit (ReLU) are fundamentally unsuitable for this task.
While computationally efficient, ReLU produces a piecewise linear
output, meaning its first derivative is piecewise constant and its
second derivative is a series of Dirac delta functions (i.e., zero
almost everywhere). This mathematical property makes it impossible to
represent the smooth, continuously varying gravitational
forces that govern celestial motion.[1]

To overcome these fundamental limitations, a more principled approach is
required---one where the architecture itself imparts a strong inductive
bias that aligns with the underlying physics. The framework detailed in
this report proposes a hybrid PINN that is not an arbitrary collection
of techniques but a meticulously co-designed system. Each architectural
component is deliberately chosen to counteract a specific,
well-understood failure mode of standard models when applied to chaotic
physical systems. This synergistic design methodically addresses the
core requirements of the problem:

1.  **Derivative Fidelity:** To accurately enforce the physics residual,
    the network must be built with an activation function that is
    infinitely differentiable ($\mathrm{C}^\infty$) and whose
    derivatives are well-behaved. The Sinusoidal Representation Network
    (SIREN) architecture, which uses the sine function as its
    nonlinearity, is the ideal choice. The derivative of a sinusoid is
    another sinusoid, merely phase-shifted, a property that is preserved
    for higher-order derivatives. This provides a powerful inductive
    bias towards learning smooth functions whose derivatives are also
    smooth, a property essential for minimizing the physics residual
    with high fidelity.[1]

2.  **Expressivity and Training Stability:** Capturing the intricate
    complexity of chaotic trajectories requires a network with
    significant expressive capacity, which is typically achieved through
    depth. However, training very deep neural networks is notoriously
    difficult due to the well-known problems of vanishing and exploding
    gradients. The Residual Network (ResNet) backbone provides a
    solution by incorporating \"skip\" connections that create an
    identity mapping shortcut, allowing gradients to flow unimpeded
    through the network's depth. This report specifies the use of a
    particularly effective variant, the Power-Enhanced SkipResNet
    (SQR-SkipResNet), which has been empirically shown to provide more
    stable gradient flow and superior performance on non-smooth
    functions, making it well-suited for deep architectures.[1]

3.  **Long-Term Physical Plausibility:** Even a PINN that perfectly
    satisfies the local, instantaneous equations of motion can
    accumulate numerical drift over long time horizons, leading to
    unphysical outcomes such as a gradual increase or decrease in the
    total energy of an isolated system. The proposed architecture keeps
    the model as a position-prediction network and incorporates global
    conservation behavior as soft penalty terms in the loss. The energy
    term evaluates the analytic matched-Plummer Hamiltonian $H_\epsilon$
    from predicted positions and AD-derived velocities, then penalizes
    drift from the initial value. The angular-momentum term similarly
    penalizes componentwise drift from the initial angular momentum.
    These are soft conservation regularizers, not hard conservation laws
    and not architecture-level conservation constraints.

This philosophy of pragmatic hybridization, which combines
architecture-level derivative fidelity with loss-level physics
constraints, is a central theme of the proposed design. The resulting
model is a synergistic whole, where the SQR-SkipResNet enables the
necessary depth for expressivity, the SIREN activations provide the
derivative fidelity required for physics enforcement, and the soft
conservation regularizers improve long-term physical plausibility.

Author Comment: Again, all the superscript instances are rendered as raw literal strings in the preview. Fix this carefully.

# 2. The SQR-SkipResNet-SIREN Backbone: A Deep Dive into the Core Architecture

This section provides the definitive, mathematically-grounded
specifications for each component of the neural network's core
structure. Every choice is justified by its contribution to the model's
ability to represent complex physical phenomena accurately and to be
trained stably.

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

# 3. The Multi-Component Loss Function (Physics-Constrained)

The training of the PINN is guided by a composite loss function that
simultaneously optimizes for three distinct yet complementary
objectives: fidelity to observed data, adherence to the governing laws
of physics, and soft conservation of total system energy and angular
momentum. This multi-component objective enables the network to learn
solutions that are not only accurate but also physically plausible and
generalizable beyond the specific training data points.

The default Phase 19 training objective is:

$$L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$

Author Comment: the above formula is not written in the correct syntax. We need to fix it so that it will be rendered correctly in markdown preview in Cursor.

Canonical text form: $L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$.

Author Comment: the above canonical text form is also rendered in raw text strings in preview.

This is the baseline penalty-term formulation. No dual variables are
part of the default training loss; the scalar-conservation augmented
Lagrangian option is documented only as a P2 ablation in §4.2.

## 3.1 Data Fidelity Term ($\mathcal{L}_{\text{data}}$): Anchoring to Ground Truth

The purpose of the data fidelity term is to ensure that the network's
predictions align with the high-precision trajectory data generated by a
trusted numerical integrator. This term grounds the general,
physically-plausible solution learned by the PINN to the specific
trajectory defined by a given set of initial conditions.

The data fidelity loss uses a Huber contract on scaled projected
positions:

$$L_{data} = \frac{1}{N_t \, N_b \, d} \sum_{n} \sum_{i} \sum_{c} \operatorname{Huber}_{\delta_r}(r_{\theta,i,c}'(u_n) - r_{i,c}'(u_n))$$

Author Comment: again, the syntax is broken

where $\delta_r = 1$ is the default Huber transition. The previous
MAE/L1 data-loss prose is replaced by this Huber contract.

The reduction is the mean over time, bodies, and spatial components: the sum
above is normalized by $N_t \, N_b \, d$, equivalently $1/(9 N_t)$ at $N_b = 3$
bodies and $d = 3$ spatial components. This reduction was ratified by the owner
on 2026-07-31 at the Phase 48 checkpoint (GAP-45-01, option A).

> **Phase 53 contract: $L_{data}$ component reduction (SPEC-04; GAP-45-01 owner ruling 2026-07-31, option A; grounded by .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md).** The ratified reduction is the per-coordinate mean of the Huber residual over the time, body, and spatial-component axes. Both readings were presented to the owner against retained Stage-0 run magnitudes: the implemented per-coordinate mean produced run-average values of 0.1539..0.1630, where the sum-over-components reading produced 1.3852..1.4673 - exactly 9x, which is 3 bodies times 3 spatial components. This edit does not amend a contract-marked value: the adjacent Phase 35 LOSS-01 block fixes scaling, units, and component-math ownership but does not state the reduction, and the reduction was genuinely undetermined - which is precisely why GAP-45-01 had to exist - so correcting the displayed formula resolves an ambiguity rather than superseding a ruling. The shipped implementation already computes this reduction (CONF-07 Complete); this edit changes no code.

> **Phase 35 contract: loss scaling and units (LOSS-01; NS-18 modified; AC-LOSS-01; grounded by the resolution doc §1.14 and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md`).** `pinn_architecture.md` is the canonical component-math home for data, physics, energy, and angular-momentum terms; `ctl_instruction.md` owns total-loss assembly and methodology cross-references by stable section heading plus AC ID. The component contract uses dimensionless `u=t/T` and `r'=r/D`, projected scaled positions for Huber data loss, ordered raw mass metadata where COM/force terms require masses, matched `epsilon_train = 1e-5` for force and Hamiltonian terms, separate data-fidelity snapshot points from physics/energy collocation points, the IC anchor, the angular-momentum regularizer, and no linear-momentum / no-linear-momentum-loss term.

where:

- $u_n = t_n/T$ is the normalized physics time coordinate

- $r'_{\theta,i}(u_n)$ is the network's predicted **scaled
  position** vector (the direct output of the network)

- $r'_i(u_n)$ is the ground truth position from the BRUTUS
  data, **scaled by the characteristic length $D$** (i.e.,
  $r'_{\text{true}} = r_{\text{true}}/D$)

- $N_t$ is the number of sampled time points in a training batch

**Batch Construction:**

The data points are sampled from the BRUTUS trajectory snapshots as
follows:

``` {.python language="Python" caption="Listing 2: Data Batch Construction"}
def get_batch(batch_size, points_per_trajectory=32):
    """
    Sample batch_size trajectories from the dataset.
    For each trajectory, sample points_per_trajectory time points.
    
    Returns:
        t_k: Time points sampled from BRUTUS snapshots
        r_true: Corresponding ground-truth positions
        
    Shapes: (batch_size * points_per_trajectory, ...)
    """
    # Implementation details depend on dataset structure
    return t_k, r_true

# Total data points per batch
N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192
```

The time points $t_k$ are sampled from the discrete BRUTUS trajectory
snapshots available in the training dataset, representing specific
moments where high-precision numerical integration data is available.

> **Phase 34 contract: batch-construction reconciliation (SI-PINN-003; ctl canonical; AC-LOOP-02; grounded by the resolution doc §1.5 claim matrix B07-04 and `ctl_instruction.md` Mini-Batch Construction).**
>
> *Note (PIPE-04): `points_per_trajectory=32` and `N_data = batch_size * points_per_trajectory` are code defaults/illustrations only, not the spec contract. The operative data-loss sampling rule is `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` without replacement, defined canonically in `ctl_instruction.md` Mini-Batch Construction. The data-side loader also exposes `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)` for stage-aware trajectory selection (PIPE-08, `ctl_instruction.md` §2.6). A verifier confirms `pinn_architecture.md` agrees with the canonical ctl contract and carries no contradictory copy here.*

**Loss Integration Note:**\
The data term is unweighted in the default objective. Physics and
conservation terms are balanced by scheduled scalar weights, not by
default ALM dual updates.

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

Minimizing this term forces the network to learn a function
$\mathrm{r}_\theta(u)$ that is also a solution to the governing ordinary
differential equations (ODEs) in the normalized physics-time coordinate.

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

## 3.4 Soft Energy Conservation Regularizer ($L_{E}$): Enforcing a Global Conservation Law

While the physics residual enforces the local, instantaneous laws of
motion, it does not explicitly guarantee the conservation of global
quantities over long time horizons. For an isolated mechanical system
like the $\mathrm{N}$-body problem, the total energy is one such
conserved quantity. The energy loss is a soft conservation regularizer:
the network predicts positions at each time step, velocities and
accelerations are computed via componentwise automatic differentiation,
and the analytic matched-Plummer Hamiltonian $H_\epsilon$ (`H_ε`) is
evaluated from the predicted positions and AD-derived velocities. This
penalty term discourages drift from the initial energy value; it is a
soft constraint, not a hard conservation law. The network does not
parameterize a Hamiltonian.

The matched-Plummer potential energy is:

$$V_\epsilon = -\sum_{i<j} \frac{m_i m_j}{r_{safe,ij}}$$

using the same $r_{safe,ij} = \sqrt{||r'_j - r'_i||^2 + \epsilon_{train}^2}$
as the residual force term. The matched-Plummer Hamiltonian is
$H_\epsilon = T' + V_\epsilon$ where $T'$ is the dimensionless kinetic
energy.

**Energy Conservation Regularizer (PHYS-04):**

$$L_{E} = \frac{1}{N} \sum_n \operatorname{Huber}(\Delta H_n, \delta=1.0)$$

where

$$\Delta H_n = \frac{H_\epsilon(r_\theta'(u_n), v_\theta'(u_n)) - H_\epsilon(r_0', v_0')}{|H_\epsilon(r_0', v_0')| + \epsilon_H}$$

The relative drift symbol is $\Delta H_n$.

$$epsilon_H = 1e-4 * S_H$$

$$S_H = median_train(K0 + Uabs0)$$

and $\delta = 1.0$ is the Huber transition.

> **Phase 35 contract: energy Huber delta (LOSS-03; NS-13 defer / deferred calibration; AC-LOSS-03; grounded by the resolution doc §1.13 and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-13-energy-huber-delta.md`).** The normalized-energy Huber transition is named `delta_E = 1.0` for Phase 35 traceability and remains the configurable current baseline. Calibration to a smaller range such as `0.01-0.1`, any stage-indexed Huber delta table, and any median/quantile replacement are deferred until normalized `|Delta H|` quantiles, linear-branch occupancy, validation energy drift, and weighted gradients are measured.

$S_H$ is computed once in float64 after final
COM/zero-momentum/gauge/scaling preprocessing over the training split
using the matched-Plummer Hamiltonian components with
$\epsilon_{train} = 10^{-5}$. (Author Comment: I am not sure why there is a duplicate 10^-5 here)Persist both $S_H$ and $\epsilon_H$ in training metadata. $S_H$ must be finite and strictly positive; $S_H \leq 0$ or non-finite $S_H$ is a preprocessing/metadata validation failure. Do not apply a fallback numeric floor. Use $\epsilon_H$ only in $|H_0| + \epsilon_H$. Phase 21 reports activation behavior only and must not reselect $\epsilon_H$ unless a new user instruction opens a replacement gap.

**Dual-epsilon visibility (IPR cross-reference; VAL-03).** The training-time softening $\epsilon_{train} = 10^{-5}$ above is distinct from the data-side validation softening $\epsilon_{inv} = 10^{-10}$ used by the Interpolation Physics Residual (IPR) admission diagnostic in `ctl_instruction.md` Step-1A `Data-side quality-metric contracts`. Data-side IPR (validation, $\epsilon_{inv} = 10^{-10}$) and any training-loop `IPR_train` noise-floor role (training, $\epsilon_{train} = 10^{-5}$, deferred to doc-03) are different quantities and must not be conflated. This note states the separation; it does not alter the PHYS-04 / HC-4 training contracts above.

The FUT-01 divergence handoff must flag executable training metadata as
divergent if it omits $S_H$ or $\epsilon_H$, computes $S_H$ from a
different split or preprocessing stage, computes $S_H$ per minibatch,
uses a fixed numeric $\epsilon_H$, or applies a max/fallback floor that is
not present in this canonical contract.

The term "Hamiltonian" here refers to the analytic energy function
$H_\epsilon$, not to a neural-network-parameterized Hamiltonian.

**Initial Energy Calculation:**

The initial energy $H_0$ is precomputed during dataset preprocessing:

``` {.python language="Python" caption="Listing 5: Initial Energy Calculation in Dataset Preprocessing"}
class TrajectoryDataset:
    def __init__(self, trajectory_data):
        # ... other initialization ...

        # Precompute H_0 for each trajectory
        self.H_0_values = {}
        for traj_id, traj in trajectory_data.items():
            self.H_0_values[traj_id] = self.compute_initial_energy(
                r0_prime=traj['r0_scaled'],  # Already scaled by D
                v0_prime=traj['v0_scaled'],  # Already scaled by D/T
                masses=traj['masses']
            )

    def compute_initial_energy(self, r0_prime, v0_prime, masses):
        """Compute H_0 in dimensionless units (G=1)"""
        H_0 = 0.0
        epsilon_train = 1e-5  # Training-time Plummer softening parameter

        # Fixed for 3-body problem
        N_bodies = 3

        # 1. KINETIC ENERGY (dimensionless)
        for i in range(N_bodies):
            H_0 += 0.5 * masses[i] * np.sum(v0_prime[i]**2)

        # 2. POTENTIAL ENERGY (dimensionless)
        for i in range(N_bodies):
            for j in range(i+1, N_bodies):
                r_vec = r0_prime[i] - r0_prime[j]
                r_sq = np.sum(r_vec**2)
                r_safe = np.sqrt(r_sq + epsilon_train**2)
                H_0 -= masses[i] * masses[j] / r_safe

        return H_0
```

**Key Implementation Notes:**

- **Unit System Consistency:** All quantities (positions $r'$,
  velocities $v'$, and initial energy $H_0$) must be expressed in the
  same non-dimensional ($G = 1$) system of units.

- **Softening Parameter:** The same value $\epsilon_{train} = 10^{-5}$ (author comment: again duplicate number)
  is used consistently in both the physics residual and energy
  calculations to prevent numerical instabilities during close
  encounters.

- **Collocation Points:** The same set of $N_{\text{col}}$ points is
  used for both physics and energy loss evaluation to ensure
  computational efficiency.

## 3.5 Angular Momentum Conservation Loss ($L_{L}$)

$$L_{L} = \frac{1}{3N_t} \sum_n \sum_\alpha \operatorname{Huber}\left(\frac{L_{\theta,\alpha}'(u_n) - L_{0,\alpha}'}{L_{scale}}, \delta=1.0\right)$$

where $\alpha \in \{x, y, z\}$, $L_{scale} = ||L_0'|| + \epsilon_L$,
and $\epsilon_L = 10^{-8}$ is a numerical-stability scale grounded in
resolution §8.6 and distinct from softening $\epsilon_{train}$ /
$\epsilon_{inv}$ and from $\epsilon_H$ (resolved by D-20 / GAP-19-01 as a
dataset-scale Hamiltonian floor, not a softening parameter).
Componentwise angular momentum Huber loss on relative angular-momentum
drift follows resolution §8.6. The velocity $v_\theta'(u_n)$ used to
compute $L_\theta'(u_n)$ comes from the PHYS-02 componentwise
normalized-time AD contract.

> **Phase 35 contract: angular-momentum component role (LOSS-01; NS-18 modified; AC-LOSS-01; grounded by `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md`).** $L_L$ remains a soft angular-momentum regularizer in the default component catalog; it does not authorize a separate linear-momentum loss.

# 4. Advanced Training and Optimization Strategy

Successfully training the network requires a sophisticated approach to
navigate the complex, non-convex loss landscape and handle numerical
instabilities.

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
  $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
  causal exponent to avoid underflow, but do not choose a numeric
  clipping bound in Phase 19; surface a gap if one is needed.
  The causal exponent clip is required only to avoid underflow.
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

## 4.2 Optional ALM Ablation (P2)

> **Phase 34 contract: ALM parameter update / `mu_p` clamp (LOOP-05; deferred; AC-LOOP-05; grounded by the resolution doc §1.18 and `evidence/alm-mu-p-clamp.md`).**

Default: ALM is OFF. The default training loss is the penalty-term formulation in §3–§4 above; it has no `mu_p` and no dense-residual ALM update. Dense-residual ALM is rejected from the default loss.

ALM remains an optional scalar-conservation add-on only. If a future optional scalar-conservation ALM ablation is fully specified (constraint normalization, penalty-update law, state reset/persistence, and update cadence), its dual-variable update may run under `torch.no_grad()`:

- Moving-average variance / second-moment update for `lambda_p` and `mu_p` in RMSprop style.
- Clamp `mu_p` to `[1e-4, 100]` after each update.

These `lambda_p`/`mu_p` mechanics are **deferred** and **conditional**; they are **not adopted into the default training loop** and may not be used until the ablation specification closes GAP-19.

As a P2 ablation, an augmented Lagrangian method may be applied to scalar conservation constraints only:

- **Constraints:** $c_E = \mathrm{RMS}_n(\Delta H_n)$ (energy drift), $c_{L,\alpha} = \mathrm{RMS}_n((L'_{\theta,\alpha}(u_n) - L'_{0,\alpha}) / L_{scale})$ (angular momentum drift per component). (Author Comment: this syntax is not ideal since it invovles math equations/formula; it should properly use correct markdown render-friendly syntax)
- **Never apply ALM to the dense ODE residual.**
- **Dual-variable updates:** Only between Adam epochs or between deterministic refinement passes. Never update dual variables during L-BFGS or inside a line search.
- **Logging:** Log constraint values before and after each dual-variable update.
- **Default: ALM is OFF.** The default loss is the penalty-term formulation in §3-§4 above.

This P2 ablation is not part of the baseline training contract. It is documented for completeness and for future experimentation.

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

# 5. Inference and Trajectory Generation

Once the model is trained, it can be used as a high-fidelity function
approximator to generate entire trajectories on demand.

## 5.1 Generating a Trajectory

To predict the evolution of a system from a given initial condition
($IC$), the following procedure is used:

1.  **Define Evaluation Times:** Create a fine-grained array of physical
    evaluation times, $t_{eval}$, over the desired simulation interval
    (e.g., 10,000 points from $t=0$ to $t_{max}$). Convert them to
    normalized physics time $u_{eval}=t_{eval}/T$. The model wrapper
    computes the bounded network coordinate $\tau = 2u - 1$ internally.

2.  **Predict Positions:** For each normalized physics-time point in
    $u_{eval}$, let the model wrapper concatenate $\tau = 2u-1$ with the
    constant $IC$ vector before calling the trained network. This produces
    a continuous trajectory of the system's positions, $r_{\theta}(u_{eval})$.

3.  **Derive Kinematics (Optional):** If velocities or accelerations are
    needed for analysis, derive them by differentiating with respect to
    the canonical autograd leaf $u$. The $2\times$ and $4\times$ chain-rule
    factors apply only to an implementation path that differentiates
    directly with respect to $\tau$.

## 5.2 Output Layer and Kinematic Consistency via Automatic Differentiation

### Network Input Contract

**Input Vector** A **14-dimensional vector** `[\tau, IC_{13}]`, where `u=t/T` is the autograd leaf and `\tau=2u-1` is the bounded network time coordinate. `IC_{13}` is the ordered Jacobi-state initial-condition vector defined canonically in `ctl_instruction.md` Step 4:

$$
IC_{13} = [m_1, m_2, m_3, \rho_x, \lambda_x, \lambda_y,
\dot{\rho}_x, \dot{\rho}_y, \dot{\rho}_z,
\dot{\lambda}_x, \dot{\lambda}_y, \dot{\lambda}_z, E].
$$

Mass, Jacobi-position, and Jacobi-velocity slots are independently normalized with `tanh((z - mu_z)/(sigma_z + 10^-8))` after the Phase 18 (FRAME-01) preprocessing contract. The energy slot uses `tanh(E / E_scale)` with `E_scale = |median_traj(E)| + 10^-8`. Componentwise derivative tests for the `u -> tau -> r` chain are specified in Phase 19 (PHYS-02).

### Output Layer

The network architecture is simplified and physical consistency is
hard-coded by predicting only positions and deriving all other kinematic
quantities via automatic differentiation (AD). This is a core design
principle of PINNs, supported by established frameworks like
DeepXDE.[14]

The final layer of the SQR-SkipResNet-SIREN network is a standard linear
layer without any activation function. This is crucial as it allows the
network's outputs---the predicted positions---to take on any real value
required by the physical system. The output is a 9-dimensional vector
representing the concatenated positions of the three bodies at a given
time $\mathrm{t}$:
$$\mathrm{r}_\theta(\mathrm{t}) = [\mathrm{r}_1(\mathrm{t}), \mathrm{r}_2(\mathrm{t}), \mathrm{r}_3(\mathrm{t})]$$

Crucially, the network does not predict velocities or accelerations
directly. Instead, these kinematic quantities are derived from the
projected position outputs using componentwise AD with respect to the
normalized physics-time input, $u=t/T$. The velocity vector is computed
as the first-order derivative of the projected position vector, and the
acceleration vector is computed as the second-order derivative:
$$v_\theta'(u) = \frac{d r_\theta'(u)}{d u} \quad \text{and} \quad a_\theta'(u) = \frac{d^2 r_\theta'(u)}{d u^2}$$

By computing derivatives via AD, the fundamental kinematic relationships
between position, velocity, and acceleration
$(\mathrm{v} = \mathrm{r}', \mathrm{a} = \mathrm{r}'')$ are satisfied by
construction to machine precision. This hard-codes a significant portion
of the problem's physics into the model, simplifies the network
architecture (as no extra heads are needed for velocity or
acceleration), and makes the overall learning task more tractable.

## 5.3 Output Frame and File Format

For consistency and physical correctness, the output of the model must
be clearly defined.

- **Reference Frame:** The predicted positions, $r_{\theta}(t)$, are in
  the **Center of Mass (COM) frame**. This is consistent with the use of
  translation-invariant quantities in the input vector.

The raw network head emits unconstrained positions

$$
\tilde r_\theta(u, IC_{13}) = [\tilde r_1, \tilde r_2, \tilde r_3] \in \mathbb{R}^9.
$$

Before any downstream consumer sees this output, the model applies a hard mass-weighted COM projection:

$$
R_{\mathrm{COM}} = \frac{\sum_{j=1}^3 m_j \tilde r_j}{\sum_{j=1}^3 m_j},
\qquad
r_i = \tilde r_i - R_{\mathrm{COM}}, \qquad i \in \{1,2,3\}.
$$

Here `m_j` denotes the ordered raw pre-tanh mass metadata supplied by the Phase 18 (FRAME-01) preprocessing output; it is not the normalized mass slot inside `IC_{13}`.

The projected positions

$$
r_\theta = [r_1, r_2, r_3]
$$

are the only positions consumed by data loss, physics residuals, IC loss, conservation loss, diagnostics, and evaluation metrics. The projection is architectural, not a soft penalty.

This projection is the model-output side of the Phase 18 FRAME-02
assertion: for every projected output, the mass-weighted position COM
is zero by construction. Since velocities and accelerations are
automatic derivatives of the projected positions, their mass-weighted
COM derivatives are zero by the same projection identity. Phase 21
executes the numerical acceptance checks; this section only states the
architectural guarantee.

### 5.3.1 Normalized-Time Derivative Contract (PHYS-02)

> **Phase 35 contract: componentwise AD and tau/u boundary (LOSS-01; NS-12 accepted and NS-18 modified; AC-LOSS-01-AD; grounded by the resolution doc §§1.12/1.14, `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-12-componentwise-ad.md`, and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md`).** The canonical autograd leaf is `u=t/T`. When differentiating with respect to `u`, velocity and acceleration use `dr'/du` and `d^2r'/du^2` with no chain factor; the factors `2` and `4` apply only to a direct `tau = 2u - 1` leaf. Componentwise derivatives are required and the summed-output VJP remains forbidden; executable batching and performance strategy remain FUT.

**Three-layer separation:** $(t, r, v)_{raw} \rightarrow (u, r', v')_{physics} \rightarrow (\tau, IC_{13})_{network}$ where `u=t/T` and $\tau = 2u - 1$.

**Canonical autograd leaf:** `u=t/T`. When the code path differentiates
with respect to `u`:

- $v' = dr'/du$ (velocity in scaled time, no chain-rule factor)
- $a' = d^2r'/du^2$ (acceleration in scaled time, no chain-rule factor)

**Conditional chain-rule factors for τ/tau:** If a code path
differentiates directly with respect to $\tau = 2u - 1$ (rather than
`u`), then:

- $v' = 2 \cdot dr'/d\tau$
- $a' = 4 \cdot d^2r'/d\tau^2$

These factors apply ONLY to the $\tau$-leaf code path.

**Componentwise derivatives required:** The residual and Hamiltonian
require all nine derivatives $dr'_{i,\alpha}/du$ ($i \in \{1,2,3\}$,
$\alpha \in \{x,y,z\}$). The following anti-pattern is FORBIDDEN:

**Forbidden:** `torch.autograd.grad(r.sum(), u, create_graph=True)` --
this computes a vector-Jacobian product against an all-ones covector,
not the nine individual derivatives.

**Acceptable patterns:**

- `torch.func.jacrev` + `vmap` over the batch dimension
- Explicit loop over the 9 projected output components
- Equivalent full-Jacobian method

**Worked synthetic-trajectory test:** For the test trajectory
$r'(u) = [sin(2πu), cos(2πu), u²]$ (one body, three components), the
symbolic derivatives are:

- $dr'/du = [2π cos(2πu), -2π sin(2πu), 2u]$
- $d^2r'/du^2 = [-4π² sin(2πu), -4π² cos(2πu), 2]$

AD outputs must match these symbolic derivatives to numerical
tolerance. Executable tolerance and the disposable probe belong to Phase
21 VER-04 / AC-PHYS-02.

```python
# Spec-illustrative AD pattern (not FUT-01 implementation prescription):
# Option A: jacrev + vmap for batched trajectories
from torch.func import jacrev, vmap

def model_single(u_scalar, ic13):
    """Single-trajectory forward pass."""
    tau = (2 * u_scalar - 1).reshape(1)  # u=0 maps to tau=-1
    ic13_vec = ic13.reshape(-1)
    return net(torch.cat([tau, ic13_vec]))

# dr'/du for all 9 output components on one trajectory:
drdu_single = jacrev(model_single, argnums=0)(u_scalar, ic13)  # shape (9,)

# Batch over trajectories:
drdu_batch = vmap(lambda u_b, ic_b: jacrev(model_single, argnums=0)(u_b, ic_b))(u_batch, ic13_batch)

# Option B: explicit per-component loop
# derivatives = []
# for k in range(9):
#     grad_k = torch.autograd.grad(r_prime[k], u, create_graph=True)[0]
#     derivatives.append(grad_k)
# drdu = torch.stack(derivatives)  # shape (9, 1)
```

- **Output File Format:** The final generated trajectory should be saved
  in a structured format, such as a CSV file, for easy analysis and
  visualization. Each row should represent a single time step.

- **Output Definition:** The output at each network forward pass is
  strictly the positions of the three bodies at a single normalized
  input time $t'$; velocities and accelerations are derived via AD.

**Example CSV Output Format:**

    time,x1,y1,z1,x2,y2,z2,x3,y3,z3
    0.00,-0.98,0.20,0.00,0.49,-0.10,0.00,0.49,-0.10,0.00
    0.01,-0.97,0.21,0.00,0.48,-0.11,0.00,0.49,-0.10,0.00
    ...

The section below is weirdly formatted and written out even in the original markdown file. However, it seems to render correctly render in the preview, so I'm not sure how to best approach this syntax fix here.

**Table 2: Consolidated Implementation Blueprint Summary**

| **Component** | **Definitive Specification** | **Justification** |
| --- | --- | --- |
| **Unit System** | A non-dimensional system is used where the gravitational constant $G=1$.<br>• **Characteristic Time:** $T=t_{max}$ (max time in dataset).<br>• **Characteristic Length:** $D=\sqrt[3]{GT^{2}}$. | Simplifies the governing physical equations and improves the numerical stability of the model during training. |
| **Backbone** | **SQR-SkipResNet** with **12 hidden layers** and a **width of 256 neurons**.<br>• **Odd Layers:** $\mathbf{x}^{(l)} = f_{\text{sr}}^{(l)}(\mathbf{x}^{(l-1)}) + (\mathrm{LayerNorm}(\mathbf{x}^{(l-1)}))^2$.<br>• **Even Layers:** Plain block, $\mathbf{x}^{(l)} = f_{\text{pn}}^{(l)}(\mathbf{x}^{(l-1)})$.<br>• **Layer Norm:** Applied to skip path on odd layers only, with `elementwise_affine=False` and `eps=1e-5`. | The deep architecture provides the expressive power needed for chaotic dynamics. The SQR-SkipResNet variant with LayerNorm provides superior gradient stability for non-smooth dynamics, which is ideal for modeling close encounters. |
| **Activation** | **SIREN ($\sin(x)$)** for all hidden layers. | The sine function is infinitely differentiable ($C^{\infty}$), which is a mathematical necessity for accurately computing the second-order derivatives ($\frac{d^{2}r}{dt^{2}}$) required in the physics loss term. |
| **Initialization** | A principled, two-part SIREN initialization scheme:<br>• **First Layer:** `first_omega_0 = 30`. Weights from $U[-\frac{1}{n_{in}}, \frac{1}{n_{in}}]$.<br>• **Hidden Layers:** `hidden_omega_0 = 1`. Weights from $U[-\frac{\sqrt{6/n_{in}}}{1}, \frac{\sqrt{6/n_{in}}}{1}]$. | A high initial frequency (`first_omega_0`) helps overcome spectral bias. The specific scaling for hidden layers ensures a stable distribution of activations, making the deep network trainable. |
| **Input Vector** | A **14-dimensional vector** built from the bounded network time coordinate and the ordered Jacobi-state initial-condition vector; see Section 5.2 "Network Input Contract" for the canonical formula and back-reference to `ctl_instruction.md` Step 4. | This formulation provides a physically-grounded and injective (unambiguous) representation of the initial state, which is critical for a conditional network to learn correctly. |
| **Output** | A **9-dimensional position vector** `[r1(u), r2(u), r3(u)]` with a linear (no activation) final layer. Velocities ($v'=\frac{dr'}{du}$) and accelerations ($a'=\frac{d^{2}r'}{du^{2}}$) are derived via componentwise **Automatic Differentiation (AD)** from the projected positions. | Predicting only positions simplifies the network architecture. Deriving kinematics via AD hard-codes their fundamental physical relationship, ensuring they are satisfied by construction to machine precision. |
| **Data Loss ($L_{data}$)** | **Huber loss** on scaled projected positions with default $\delta_r=1$. | Huber is the default data contract because it is smoother than pure L1 and less brittle than L2 for chaotic trajectory samples. |
| **IC Loss ($L_{IC}$)** | **IC anchor** on predicted position and AD-derived velocity at `u=0`, with $\beta_v=1$ and $\lambda_{IC}=1$ default. | Anchors the learned trajectory to the Phase 18 preprocessed initial state before later collocation points are optimized. |
| **Physics Loss ($L_{phys}$)** | **Causal-weighted residual** using the matched Plummer force denominator $r_{safe,ij}=\sqrt{\|\|r_j'-r_i'\|\|^2+\epsilon_{train}^2}$ with $\epsilon_{train}=10^{-5}$. | This loss enforces the governing ordinary differential equations across the entire solution domain, not just at data points, allowing the model to generalize and make physically consistent predictions. |
| **Total Loss ($L_{total}$)** | $L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$. | Combines data fidelity, IC anchoring, causal physics residual, energy drift, and angular-momentum drift terms in the default penalty-term formulation. |
| **Energy Loss ($L_{E}$)** | **Huber Loss ($\delta=1.0$)** on relative drift of the analytic matched-Plummer Hamiltonian $H_\epsilon$ (`H_ε`) using `epsilon_H = 1e-4 * S_H`. | soft conservation regularizer; the network predicts positions and does not parameterize a Hamiltonian. |
| **Angular Momentum Loss ($L_L$)** | **Componentwise Huber loss** on relative angular-momentum drift with $L_{scale}=\|\|L_0'\|\|+\epsilon_L$ and $\epsilon_L=10^{-8}$. | Enforces angular-momentum conservation as a soft penalty distinct from physics softening and from the energy denominator floor. |
| **Optional ALM P2 Ablation** | Optional P2 ablation for scalar conservation constraints only; never part of the default loss and never applied to the dense ODE residual. | Documents future experimentation boundaries without changing the baseline training contract. |

## References

[1] Power-enhanced ResNet for Function Approximation.pdf
[2] PIG: PHYSICS-INFORMED GAUSSIANS AS ADAPTIVE PARAMETRIC MESH REPRESENTATIONS - OpenReview, accessed June 25, 2025, <https://openreview.net/pdf/ba580795154cc26f5abe3ab4feab161a5246c2f3.pdf>
[3] PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://www.researchgate.net/publication/386575809_PIG_Physics-Informed_Gaussians_as_Adaptive_Parametric_Mesh_Representations>
[4] PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://openreview.net/forum?id=y5B0ca4mit>
[5] Implicit Neural Representations with Periodic Activation Functions, accessed June 25, 2025, <http://arxiv.org/pdf/2006.09661>
[6] Implicit Neural Representations with Periodic Activation Functions - NIPS, accessed June 25, 2025, <https://proceedings.neurips.cc/paper/2020/file/53c04118df112c13a8c34b38343b9c10-Paper.pdf>
[7] jaeminoh/Siren PINNs: Solving various PDEs by employing Siren, with JAX implementation., accessed June 25, 2025, <https://github.com/jaeminoh/Siren_PINNs>
[8] Implicit Neural Representations with Periodic Activation Functions - Vincent Sitzmann, accessed June 25, 2025, <https://www.vincentsitzmann.com/siren/>
[9] Implicit Neural Representations with Periodic Activation Functions | NeurIPS 2020, accessed June 25, 2025, <https://www.computationalimaging.org/publications/siren/>
[10] Gentle Introduction to SIREN - Nail Ibrahimli - TU Delft 3D Geoinformation, accessed June 25, 2025, <https://3d.bk.tudelft.nl/nail/siren/>
[11] Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - arXiv, accessed June 25, 2025, <https://arxiv.org/html/2310.15690v2>
[12] Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/382109760_Power-Enhanced_Residual_Network_for_Function_Approximation_and_Physics-Informed_Inverse_Problems>
[13] Physics-Informed with Power-Enhanced Residual Network for Interpolation and Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/374946733_Physics-Informed_with_Power-Enhanced_Residual_Network_for_Interpolation_and_Inverse_Problems>
[14] Software | PNNL, accessed June 25, 2025, <https://www.pnnl.gov/projects/philms/software>
[15] lululxvi/deepxde: A library for scientific machine learning and physics-informed learning - GitHub, accessed June 25, 2025, <https://github.com/lululxvi/deepxde>
[16] DeepXDE: A Deep Learning Library for Solving Differential Equations | SIAM Review - myqcloud.com, accessed June 25, 2025, <https://pdf-1307664364.cos.ap-chengdu.myqcloud.com/%E8%AE%BA%E6%96%87%E5%8F%82%E8%80%83/PINN/DeepXDE-%20A%20Deep%20Learning%20Library%20for%20Solving%20Differential%20Equations.pdf>
[17] omniscientoctopus/Physics-Informed-Neural-Networks: Investigating PINNs - GitHub, accessed June 25, 2025, <https://github.com/omniscientoctopus/Physics-Informed-Neural-Networks>

# 10. Numerical Acceptance Checks

### 10.1 Scaling Consistency
- **Pass Criterion**: Output variables computed via the length scaling $D = (G T^2)^{1/3}$ must match physical dimensions with `relative_error < 1e-10`.
- **Input Data**: Preprocessed network inputs.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_scaling.py`

### 10.2 COM Invariance
- **Pass Criterion**: Mass-weighted position projection head yields a net center of mass of exactly 0 (`abs(COM) < 1e-10`).
- **Input Data**: Forward pass position output tensor.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_com.py`

### 10.3 Componentwise AD on Synthetic Trajectory
- **Pass Criterion**: Network Jacobian matches analytical derivatives $r'(u)$ for the synthetic trajectory $r(u) = [\sin(2\pi u), \cos(2\pi u), u^2]$ with `relative_error < 1e-6`.
- **Input Data**: Synthetic 1D domain input $u \in [0, 1]$.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py`

### 10.4 Force-Energy Consistency
- **Pass Criterion**: The analytic matched-Plummer Hamiltonian is finite, and its negative position gradient yields accelerations matching the physical force residual with the same training-time Plummer softening. `relative_error < 1e-5`.
- **Input Data**: Network trajectory output.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_force_energy.py`

### 10.5 Loss Stability Dry Run
- **Pass Criterion**: Forward pass and loss computation (physics + IC + energy + angular momentum) yield finite scalars (no NaN/Inf).
- **Input Data**: Random uniform input tensors matching network architecture dimensions.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_loss_stability.py`

### 10.6 Held-Out Physics-Gate Aggregate Statistic

> **Phase 53 contract: held-out physics-gate aggregate statistic (SPEC-05; GAP-44-01 owner ruling 2026-07-23, option A; grounded by .planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md).** The ruling's mention of codifying this wording into `ctl_instruction.md` was availability language, not a ruling on placement; the definition is fixed here because the only held-out gate in that file is the per-stage curriculum ADVANCE gate, which is a different object. Mean and median over held-out trajectories remain quoted as distribution facts and are not gate numbers.

- **Headline statistic**: the worst-case max over held-out trajectories of the per-trajectory validation-gate `eps_H`, as already defined by the locked conservation gate in `ctl_instruction.md` (Step 1A, Trajectory Admission Gate). This subsection defines only the aggregate across trajectories; the within-trajectory reduction is fixed there and is not restated here.
- **Pass Criterion**: the gate fails if ANY held-out trajectory's `eps_H` exceeds `1e-5`. The comparison is strictly greater: a trajectory whose `eps_H` equals `1e-5` passes.
- **Headline citation**: when the aggregate is quoted from the ruling it carries the exact constant 237.2086056078468 with no rounding, consistent with `SCS = log10(max eps_H)`.
- **Non-gating distribution facts**: the mean and median over held-out trajectories are non-gating, reported for distribution context only; neither is a gate number.
- **Glyph disambiguation**: this validation-gate `eps_H` is distinct from the training-loss `eps_H = 1e-4*S_H` of Section 3.4: same glyph, different quantity.
- **Gate disambiguation**: this gate is distinct from the per-stage curriculum ADVANCE gate in `ctl_instruction.md` (Stage Transition Criteria). That gate's energy-conservation criterion is a different metric under a different reduction on both axes: a final-value reading within each trajectory and a mean across trajectories, where this gate takes a worst-case max on both.

---

## Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the faithful converted body and are excluded from fidelity comparison per D-19.

### SI-PINN-002: Author comments preserved in converted body

- **Section:** Sections 2, 3 (sqr_skipresnet_siren_backbone, physics_constrained_loss)
- **Description:** 3 author comments from the LaTeX source (`\authcomment{}`) are preserved in the converted body as bold bracketed text (`**[...]**`). These are editorial notes from the original authors, not content discrepancies:
  1. "Need more detail on this dynamic scheduling for omega_0" (Section 2)
  2. "Need confirmation on this hidden layer's detail" (Section 2)
  3. The batch-construction inconsistency comment (Section 3) — resolved under SI-PINN-003 by Phase 34; `pinn_architecture.md` §3.1 now points to the canonical `ctl_instruction.md` Mini-Batch Construction contract.
- **Status:** Documented for future reconciliation — author should resolve these notes before training implementation

### SI-PINN-003: Batch construction inconsistency with CTL instruction plan

- **Section:** Section 3 (physics_constrained_loss) — Data Batch Construction code block
- **Status:** RESOLVED — reconciled by Phase 34; `ctl_instruction.md` Mini-Batch Construction is the canonical batch-construction contract (SI-PINN-003; AC-LOOP-01/02); `pinn_architecture.md` §3.1 now points to it via the PIPE-04 pointer and no longer asserts an inconsistency.
- **Description:** The original author comment flagging a batch-construction inconsistency with the CTL curriculum training plan has been removed from §3.1 and reconciled by designating `ctl_instruction.md` as the single canonical home for batch construction.

---

*End of faithful converted body. Source Issues section above is metadata excluded from fidelity comparison (D-19).*
