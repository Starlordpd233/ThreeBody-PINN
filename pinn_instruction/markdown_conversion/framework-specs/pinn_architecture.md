---
author: Starlordpd233
date: 2026-03-21
---

# A Definitive Implementation Blueprint for a Hybrid SQR-SkipResNet-SIREN PINN with Soft Conservation Regularization for $\mathrm{N}$-Body Dynamics

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
long-term physical plausibility.[^1]

A generic neural network architecture, such as a standard Multi-Layer
Perceptron (MLP), lacks the specific structural priors necessary to
handle this confluence of challenges. Such models often suffer from a
\"spectral bias,\" a tendency to learn low-frequency functions more
easily, which makes them struggle to represent the high-frequency
components inherent in chaotic dynamics.[^2] More critically, enforcing
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
forces that govern celestial motion.[^1]

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
    with high fidelity.[^1]

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
    functions, making it well-suited for deep architectures.[^1]

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
activation. In a SIREN layer, this activation is the sine function[^5]:
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
$\mathrm{N}$-body problem's physics residual.[^1] The SIREN architecture
thus provides an exceptionally strong inductive bias for representing
the smooth, continuous solutions and their derivatives required by the
governing physical laws. This directly overcomes the spectral bias of
standard MLPs, which struggle to represent the high-frequency details
inherent in chaotic trajectories and their derivatives.[^2] By using
SIREN, the network is inherently capable of representing the complex
natural signals that arise from physical systems.[^8]

## 2.2 A Principled Initialization Scheme for SIREN Layers

The successful training of a deep SIREN is critically dependent on a
specific, principled initialization scheme. Naive initialization will
cause the distribution of activations to either collapse to zero or
explode into saturated regimes, halting the learning process. The
confusion between different documents regarding the hyperparameter
$\omega_0$ is resolved here by adhering to the original,
mathematically-derived SIREN initialization scheme, which is designed to
preserve the distribution of activations as they propagate through the
network.[^5]

This scheme is not a heuristic but a carefully designed solution to two
distinct challenges: representation and trainability. It treats the
first layer of the network differently from all subsequent hidden
layers.

1.  To optimize network stability during chaotic stages, we dynamically
    schedule the initial frequency parameter,
    $\texttt{first\_omega\_0}$, using an exponential decay. This ensures
    stable representation as complexity increases:

    ``` {.python language="Python" caption="Listing 1: Implementation of Dynamic Frequency Scheduling"}
    import math

    def update_omega0(epoch, total_epochs):
        initial_omega = 30.0   # Initial high-frequency
        final_omega = 10.0     # Stabilizing value  
        decay_rate = 5.0       # Controls decay
        return final_omega + (initial_omega - final_omega) * \
               math.exp(-decay_rate * epoch / total_epochs)
    ```

    **Rationale**:

    - **Initial high-frequency (30)**: Essential for early stages to
      overcome spectral bias.

    - **Exponential reduction to 10**: Ensures smoother representation
      in chaotic dynamics, reducing numerical instabilities and
      promoting stable training.

    **[Need more detail on this dynamic scheduling for omega_0. Is it based on stages? How do we dynamically adjust it? Based on epochs? Need more details on this.]**

2.  **Subsequent Hidden Layers (for Trainability):** For all other
    hidden layers, the weights $\mathrm{W}$ are initialized from a
    different uniform distribution,
    $\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]$.\
    The hidden_omega_0 parameter is also set to 1. The crucial
    difference is the scaling of the initialization range by $\omega_0$.
    This specific scaling is mathematically derived to ensure that the
    pre-activations (the inputs to the sine function) maintain a
    standard normal distribution throughout the network's depth. This,
    in turn, keeps the sine activations in a dynamic, non-saturated
    range, preventing the frequency of the network's output from growing
    uncontrollably with depth. This careful, layer-dependent
    initialization is what makes deep SIRENs trainable by ensuring
    stable gradient flow.[^1]

    **[Need confirmation on this hidden layer's detail. Need to make sure the formula is correct according to the original SIREN paper?]**

## 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation

While the SIREN initialization enables training, pushing to the depths
required for chaotic dynamics (e.g., 12 layers) requires stabilization
of the residual connections. This report recommends adopting an advanced
ResNet variant with a critical modification: **Layer Normalization
(LayerNorm)** applied to the skip path before the power term. This
resolves gradient instability while preserving the architecture's
benefits for chaotic systems.

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

### Power Term Justification

The power term $p = 2$ remains critical for modeling non-smooth
dynamics. For 3-body systems, close encounters produce
velocity/acceleration spikes that require quadratic interaction terms to
resolve. $\text{LayerNorm}$ ensures this term remains bounded.

## 2.4 Finalized Architectural Hyperparameters

::: {#tab:architectural_hyperparameters}
  **Hyperparameter**      **Recommended Value**                                                                                                                                                                                             **Rationale & Justification**
  ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Backbone                SQR-SkipResNet with SIREN layers                                                                                                                                                                                  Superior stability and convergence for non-smooth dynamics, ideal for modeling close encounters in chaotic systems.
  Depth                   12 hidden layers (6 SQR-SkipResNet blocks)                                                                                                                                                                        Provides a good balance between the expressive power needed for chaotic dynamics and the trainability on modest hardware.
  Width                   256 neurons/layer                                                                                                                                                                                                 A strong default that balances model expressivity and computational cost, avoiding the diminishing returns of excessively wide layers.[^1]
  Activation              $\sin(\mathrm{x})$ (SIREN)                                                                                                                                                                                        The $\mathrm{C}^\infty$-smoothness is mathematically essential for accurately calculating the second-order derivatives required in the physics loss.[^1]
  LayerNorm               elementwise_affine=True, eps=1e-5                                                                                                                                                                                 Stabilizes skip path gradients without restricting feature learning. Applied only to odd layers.
  first_omega_0           30                                                                                                                                                                                                                A high initial frequency injects a high-frequency basis into the network, helping it overcome spectral bias from the outset.[^1]
  hidden_omega_0          1                                                                                                                                                                                                                 This value is used within the principled weight initialization formula for hidden layers to ensure a stable distribution of activations, enabling deep network training.[^1]
  Weight Init. (First)    $\mathrm{U}\left[-\frac{1}{n_{\text{in}}}, \frac{1}{n_{\text{in}}}\right]$                                                                                                                                        The mathematically-derived initialization for the first SIREN layer to create a random Fourier feature mapping.[^1]
  Weight Init. (Hidden)   $\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]$   The principled initialization for all subsequent SIREN layers, designed to preserve activation variance and enable stable training of deep sinusoidal networks.[^1]
  Skip Cadence            Alternating (per SQR SkipResNet)                                                                                                                                                                                  The alternating pattern of plain and power-enhanced residual layers effectively balances feature transformation and stable gradient flow.[^1]
  Power Term (p)          2 (element-wise square)                                                                                                                                                                                           Empirical results demonstrate that $p=2$ provides significant improvements in stability and accuracy without excessive computational overhead.[^1]
  Output Activation       None (Linear)                                                                                                                                                                                                     The final layer must be linear to allow the predicted positions to take on any real value required by the physical system.

  : Table 1: Architectural hyperparameters of the SQR-SkipResNet-SIREN backbone
:::

# 3. The Multi-Component, Physics-Constrained Loss Function

The training of the PINN is guided by a composite loss function that
simultaneously optimizes for three distinct yet complementary
objectives: fidelity to observed data, adherence to the governing laws
of physics, and soft conservation of total system energy and angular
momentum. This multi-component objective enables the network to learn
solutions that are not only accurate but also physically plausible and
generalizable beyond the specific training data points.

The default Phase 19 training objective is:

$$L_total = L_data + \lambda_{IC} \cdot L_IC + \lambda_{phys} \cdot L_phys^causal + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$

Canonical text form: `L_total = L_data + λ_IC · L_IC + λ_phys · L_phys^causal + λ_E · L_E + λ_L · L_L`.

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

$$L_data = \frac{1}{N_t} \sum_n \sum_i \operatorname{Huber}_{\delta_r}(r_{\theta,i}'(u_n) - r_i'(u_n))$$

where $\delta_r = 1$ is the default Huber transition. The previous
MAE/L1 data-loss prose is replaced by this Huber contract.

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

  **[Comment: This above batch construction is not consistent with the CTL instruction plan. Look into this.]**

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

The physics loss is then formulated as the mean squared norm of this
residual vector, summed over all bodies and evaluated over a set of
$N_{\text{col}}$ collocation points:
$$L_{phys} = \frac{1}{N_{\text{col}}} \sum_{k=1}^{N_{\text{col}}} \sum_{i=1}^{N} \| f_i(u_k) \|^2$$

**Collocation Point Sampling:**

The collocation points are sampled according to the following strategy:

``` {.python language="Python" caption="Listing 3: Collocation Points Sampling"}
import numpy as np

def sample_collocation_points(t_min, t_max, n_col, strategy='uniform', 
                            traj_data=None):
    """
    Sample collocation points for physics and energy loss evaluation.
    
    Args:
        t_min, t_max: Normalized time domain boundaries (e.g., [-1, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
        traj_data: Optional trajectory data for adaptive strategy
    
    Returns:
        t_col: Array of sampled time points
    """
    if strategy == 'uniform':
        t_col = np.random.uniform(t_min, t_max, size=(n_col,))
        
    elif strategy == 'adaptive':
        if traj_data is None:  # This line needs proper indentation
            raise ValueError("Adaptive strategy requires traj_data")
        # Bias sampling toward high-acceleration regions
        weights = np.abs(traj_data['accelerations']).max(axis=1)
        
        # Safety check for degenerate cases
        if weights.sum() < 1e-8:
            weights = np.ones_like(weights)
            
        weights /= weights.sum()  # Normalize
        t_col = np.random.choice(traj_data['times'], 
                                size=n_col, p=weights)
    else:
        raise ValueError("Invalid strategy")
        
    return t_col
```

Minimizing this term forces the network to learn a function
$\mathrm{r}_\theta(t')$ that is also a solution to the governing
ordinary differential equations (ODEs).

## 3.3 Initial Condition Anchor Loss ($L_IC$)

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
quadratic penalty enforces hard IC anchoring at `u=0`. $L_data$ uses
Huber (resolution §8.2) because data targets along the
curriculum-sampled trajectory are noisier and benefit from
outlier-robust loss.

## 3.4 Soft Energy Conservation Regularizer ($L_E$): Enforcing a Global Conservation Law

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

$$L_E = \frac{1}{N} \sum_n \operatorname{Huber}(\Delta H_n, \delta=1.0)$$

where

$$\Delta H_n = \frac{H_\epsilon(r_\theta'(u_n), v_\theta'(u_n)) - H_\epsilon(r_0', v_0')}{|H_\epsilon(r_0', v_0')| + \epsilon_H}$$

The relative drift symbol is `ΔH_n`.

$$epsilon_H = 1e-4 * S_H$$

$$S_H = median_train(K0 + Uabs0)$$

and $\delta = 1.0$ is the Huber transition.

$S_H$ is computed once in float64 after final
COM/zero-momentum/gauge/scaling preprocessing over the training split
using the matched-Plummer Hamiltonian components with
$\epsilon_{train} = 10^{-5}$ (`10^-5`). Persist both $S_H$ and `epsilon_H` in training metadata. $S_H$ must be finite and strictly positive; $S_H <= 0$ or non-finite $S_H$ is a preprocessing/metadata validation failure. Do not apply a fallback numeric floor. Use `epsilon_H` only in $|H_0| + epsilon_H$. Phase 21 reports activation behavior only and must not reselect `epsilon_H` unless a new user instruction opens a replacement gap.

The FUT-01 divergence handoff must flag executable training metadata as
divergent if it omits $S_H$ or `epsilon_H`, computes $S_H$ from a
different split or preprocessing stage, computes $S_H$ per minibatch,
uses a fixed numeric `epsilon_H`, or applies a max/fallback floor that is
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

- **Softening Parameter:** The same value $\epsilon_{train} = 10^{-5}$ (`10^-5`)
  is used consistently in both the physics residual and energy
  calculations to prevent numerical instabilities during close
  encounters.

- **Collocation Points:** The same set of $N_{\text{col}}$ points is
  used for both physics and energy loss evaluation to ensure
  computational efficiency.

## 3.5 Angular Momentum Conservation Loss ($L_L$)

$$L_L = (1/(3N_t)) \sum_n \sum_\alpha \operatorname{Huber}\left(\frac{L_{\theta,\alpha}'(u_n) - L_{0,\alpha}'}{L_{scale}}, \delta=1.0\right)$$

where $\alpha \in \{x, y, z\}$, $L_{scale} = ||L_0'|| + \epsilon_L$,
and $\epsilon_L = 10^{-8}$ (`10^-8`) is a numerical-stability scale grounded in
resolution §8.6 and distinct from softening $\epsilon_{train}$ /
$\epsilon_{inv}$ and from $\epsilon_H$ (resolved by D-20 as a
dataset-scale Hamiltonian floor, not a softening parameter).
Componentwise angular momentum Huber loss on relative angular-momentum
drift follows resolution §8.6. The velocity $v_\theta'(u_n)$ used to
compute $L_\theta'(u_n)$ comes from the PHYS-02 componentwise
normalized-time AD contract.

# 4. Advanced Training and Optimization Strategy

Successfully training the network requires a sophisticated approach to
navigate the complex, non-convex loss landscape and handle numerical
instabilities.

## 4.1 Loss Balancing via Warmup Schedule (PHYS-05)

$$L_total = L_data + \lambda_{IC} \cdot L_IC + \lambda_{phys} \cdot L_phys^causal + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$

Canonical text form: `L_total = L_data + λ_IC · L_IC + λ_phys · L_phys^causal + λ_E · L_E + λ_L · L_L`.

where:

- $L_data$: Huber loss on position predictions, $\delta_r = 1$ default
  (resolution §8.2).
- $L_IC$: Initial condition anchor (position + velocity at `u=0`),
  $\lambda_{IC} = 1$ default.
- $L_phys^causal$: Physics residual with causal weighting
  $w_n = exp(-\eta_c \sum_{m<n} stopgrad(\bar R_m))$, $w_1 = 1$,
  $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
  causal exponent to avoid underflow, but do not choose a numeric
  clipping bound in Phase 19; surface a gap if one is needed.
  The causal exponent clip is required only to avoid underflow.
- $L_E$: Soft energy conservation regularizer,
  see §3.4.
- $L_L$: Angular momentum conservation loss, see §3.5.
- No dedicated L_P term: linear momentum is enforced structurally by
  the Phase 17 COM projection head / zero-momentum output contract, so a
  separate linear-momentum loss would be redundant.

The warmup schedule is:

- $I_{warm} = min(2000, 0.1 \cdot N_{Adam,k})$
- $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
  default $\lambda_{phys}^{max}(k) = 1$
- $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in
  \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in
  \{5,6\}\}$
- $\lambda_E(k, i)$ and $\lambda_L(k, i)$ warm up linearly with
  $i/I_{warm}$

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

As a P2 ablation, an augmented Lagrangian method may be applied to scalar conservation constraints only:

- **Constraints:** c_E = RMS_n(ΔH_n) (energy drift), c_{L,α} = RMS_n((L'_θ,α(u_n) - L_0,α') / L_scale) (angular momentum drift per component).
- **Never apply ALM to the dense ODE residual.**
- **Dual-variable updates:** Only between Adam epochs or between deterministic refinement passes. Never update dual variables during L-BFGS or inside a line search.
- **Logging:** Log constraint values before and after each dual-variable update.
- **Default:** ALM is OFF. The default loss is the penalty-term formulation in §3-§4 above.

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

A significant challenge arises from the inverse-square distance terms in
the loss function, which can explode during simulated close encounters.
To prevent a single event from destabilizing the optimizer, adaptive
gradient clipping is essential. A robust strategy is to clip the global
L2 norm of the gradients relative to their recent typical magnitude.

``` {.python language="Python" caption="Listing 6: Adaptive Gradient Clipping Logic"}
# Maintain a queue/list of the last 100 gradient norms
grad_history = [] 

# In training loop, after loss.backward():
total_norm = torch.norm(torch.stack([torch.norm(p.grad.detach()) for p in model.parameters()]))
grad_history.append(total_norm)
if len(grad_history) > 100:
    grad_history.pop(0)

# Clip norm to 5x the median of recent norms
clip_value = 5.0 * torch.median(torch.stack(grad_history))
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)

# Then, call optimizer.step()
```

# 5. Inference and Trajectory Generation

Once the model is trained, it can be used as a high-fidelity function
approximator to generate entire trajectories on demand.

## 5.1 Generating a Trajectory

To predict the evolution of a system from a given initial condition
($IC$), the following procedure is used:

1.  **Define Evaluation Times:** Create a fine-grained array of time
    points, $t_{eval}$, over the desired simulation interval (e.g.,
    10,000 points from $t=0$ to $t_{max}$). Normalize these time points
    to the model's input range of $[-1, 1]$.

2.  **Predict Positions:** For each normalized time point in $t_{eval}$,
    feed it concatenated with the constant $IC$ vector into the trained
    network. This will produce a continuous trajectory of the system's
    positions, $r_{\theta}(t_{eval})$.

3.  **Derive Kinematics (Optional):** If velocities or accelerations are
    needed for analysis, they can be derived at any evaluation point by
    using automatic differentiation on the network with respect to the
    time input.

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
DeepXDE.[^14]

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

  -------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Component**                                **Definitive Specification**                                                                                                                                                                                                              **Justification**
  **Unit System**                              A non-dimensional system is used where the gravitational constant $G=1$.\                                                                                                                                                                 Simplifies the governing physical equations and improves the numerical stability of the model during training.
                                               • **Characteristic Time:** $T=t_{max}$ (max time in dataset).\                                                                                                                                                                            
                                               • **Characteristic Length:** $D=\sqrt[3]{GT^{2}}$.                                                                                                                                                                                        

  **Backbone**                                 **SQR-SkipResNet** with **12 hidden layers** and a **width of 256 neurons**.\                                                                                                                                                             The deep architecture provides the expressive power needed for chaotic dynamics. The SQR-SkipResNet variant with LayerNorm provides superior gradient stability for non-smooth dynamics, which is ideal for modeling close encounters.
                                               • **Odd Layers:** $\mathbf{x}^{(l)} = f_{\text{sr}}^{(l)}(\mathbf{x}^{(l-1)}) + (\mathrm{LayerNorm}(\mathbf{x}^{(l-1)}))^2$.\                                                                                                             
                                               • **Even Layers:** Plain block, $\mathbf{x}^{(l)} = f_{\text{pn}}^{(l)}(\mathbf{x}^{(l-1)})$.\                                                                                                                                            
                                               • **Layer Norm:** Applied to skip path on odd layers only, with `elementwise_affine=True` and `eps=1e-5`.                                                                                                                                 

  **Activation**                               **SIREN ($\sin(x)$)** for all hidden layers.                                                                                                                                                                                              The sine function is infinitely differentiable ($C^{\infty}$), which is a mathematical necessity for accurately computing the second-order derivatives ($\frac{d^{2}r}{dt^{2}}$) required in the physics loss term.

  **Initialization**                           A principled, two-part SIREN initialization scheme:\                                                                                                                                                                                      A high initial frequency (`first_omega_0`) helps overcome spectral bias. The specific scaling for hidden layers ensures a stable distribution of activations, making the deep network trainable.
                                               • **First Layer:** `first_omega_0 = 30`. Weights from $U[-\frac{1}{n_{in}}, \frac{1}{n_{in}}]$.\                                                                                                                                          
                                               • **Hidden Layers:** `hidden_omega_0 = 1`. Weights from $U[-\frac{\sqrt{6/n_{in}}}{1}, \frac{\sqrt{6/n_{in}}}{1}]$.                                                                                                                       

  **Input Vector**                             A **14-dimensional vector** built from the bounded network time coordinate and the ordered Jacobi-state initial-condition vector; see Section 5.2 "Network Input Contract" for the canonical formula and back-reference to `ctl_instruction.md` Step 4.                                                                                                                                                                                                                                                                                                                                                                                                                            This formulation provides a physically-grounded and injective (unambiguous) representation of the initial state, which is critical for a conditional network to learn correctly.

  **Output**                                   A **9-dimensional position vector** `[r1(u), r2(u), r3(u)]` with a linear (no activation) final layer. Velocities ($v'=\frac{dr'}{du}$) and accelerations ($a'=\frac{d^{2}r'}{du^{2}}$) are derived via componentwise **Automatic Differentiation (AD)** from the projected positions.   Predicting only positions simplifies the network architecture. Deriving kinematics via AD hard-codes their fundamental physical relationship, ensuring they are satisfied by construction to machine precision.

  **Data Loss ($L_data$)**                     **Huber loss** on scaled projected positions with default $\delta_r=1$.                                                                                                                                                                      Huber is the default data contract because it is smoother than pure L1 and less brittle than L2 for chaotic trajectory samples.

  **IC Loss ($L_IC$)**                         **IC anchor** on predicted position and AD-derived velocity at `u=0`, with $\beta_v=1$ and $\lambda_{IC}=1$ default.                                                                                              Anchors the learned trajectory to the Phase 18 preprocessed initial state before later collocation points are optimized.

  **Physics Loss ($L_phys$)**                  **Causal-weighted residual** using the matched Plummer force denominator $r_{safe,ij}=\sqrt{||r_j'-r_i'||^2+\epsilon_{train}^2}$ with $\epsilon_{train}=10^{-5}$.                             This loss enforces the governing ordinary differential equations across the entire solution domain, not just at data points, allowing the model to generalize and make physically consistent predictions.

  **Total Loss ($L_total$)**                   $L_total = L_data + \lambda_{IC} \cdot L_IC + \lambda_{phys} \cdot L_phys^causal + \lambda_E \cdot L_E + \lambda_L \cdot L_L$.                                                                                                                        Combines data fidelity, IC anchoring, causal physics residual, energy drift, and angular-momentum drift terms in the default penalty-term formulation.

  **Energy Loss ($L_E$)**                      **Huber Loss ($\delta=1.0$)** on relative drift of the analytic matched-Plummer Hamiltonian $H_\epsilon$ (`H_ε`) using `epsilon_H = 1e-4 * S_H`.                                                      soft conservation regularizer; the network predicts positions and does not parameterize a Hamiltonian.

  **Angular Momentum Loss ($L_L$)**            **Componentwise Huber loss** on relative angular-momentum drift with $L_{scale}=||L_0'||+\epsilon_L$ and $\epsilon_L=10^{-8}$.                                                                                                      Enforces angular-momentum conservation as a soft penalty distinct from physics softening and from the energy denominator floor.

  **Optional ALM P2 Ablation**                 Optional P2 ablation for scalar conservation constraints only; never part of the default loss and never applied to the dense ODE residual.                                                                                                      Documents future experimentation boundaries without changing the baseline training contract.
  -------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  : Table 2: Consolidated Implementation Blueprint Summary

## Footnotes

[^1]: Power-enhanced ResNet for Function Approximation.pdf
[^2]: PIG: PHYSICS-INFORMED GAUSSIANS AS ADAPTIVE PARAMETRIC MESH REPRESENTATIONS - OpenReview, accessed June 25, 2025, <https://openreview.net/pdf/ba580795154cc26f5abe3ab4feab161a5246c2f3.pdf>
[^3]: PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://www.researchgate.net/publication/386575809_PIG_Physics-Informed_Gaussians_as_Adaptive_Parametric_Mesh_Representations>
[^4]: PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://openreview.net/forum?id=y5B0ca4mit>
[^5]: Implicit Neural Representations with Periodic Activation Functions, accessed June 25, 2025, <http://arxiv.org/pdf/2006.09661>
[^6]: Implicit Neural Representations with Periodic Activation Functions - NIPS, accessed June 25, 2025, <https://proceedings.neurips.cc/paper/2020/file/53c04118df112c13a8c34b38343b9c10-Paper.pdf>
[^7]: jaeminoh/Siren PINNs: Solving various PDEs by employing Siren, with JAX implementation., accessed June 25, 2025, <https://github.com/jaeminoh/Siren_PINNs>
[^8]: Implicit Neural Representations with Periodic Activation Functions - Vincent Sitzmann, accessed June 25, 2025, <https://www.vincentsitzmann.com/siren/>
[^9]: Implicit Neural Representations with Periodic Activation Functions | NeurIPS 2020, accessed June 25, 2025, <https://www.computationalimaging.org/publications/siren/>
[^10]: Gentle Introduction to SIREN - Nail Ibrahimli - TU Delft 3D Geoinformation, accessed June 25, 2025, <https://3d.bk.tudelft.nl/nail/siren/>
[^11]: Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - arXiv, accessed June 25, 2025, <https://arxiv.org/html/2310.15690v2>
[^12]: Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/382109760_Power-Enhanced_Residual_Network_for_Function_Approximation_and_Physics-Informed_Inverse_Problems>
[^13]: Physics-Informed with Power-Enhanced Residual Network for Interpolation and Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/374946733_Physics-Informed_with_Power-Enhanced_Residual_Network_for_Interpolation_and_Inverse_Problems>
[^14]: Software | PNNL, accessed June 25, 2025, <https://www.pnnl.gov/projects/philms/software>
[^15]: lululxvi/deepxde: A library for scientific machine learning and physics-informed learning - GitHub, accessed June 25, 2025, <https://github.com/lululxvi/deepxde>
[^16]: DeepXDE: A Deep Learning Library for Solving Differential Equations | SIAM Review - myqcloud.com, accessed June 25, 2025, <https://pdf-1307664364.cos.ap-chengdu.myqcloud.com/%E8%AE%BA%E6%96%87%E5%8F%82%E8%80%83/PINN/DeepXDE-%20A%20Deep%20Learning%20Library%20for%20Solving%20Differential%20Equations.pdf>
[^17]: omniscientoctopus/Physics-Informed-Neural-Networks: Investigating PINNs - GitHub, accessed June 25, 2025, <https://github.com/omniscientoctopus/Physics-Informed-Neural-Networks>

---

## Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the faithful converted body and are excluded from fidelity comparison per D-19.

### SI-PINN-002: Author comments preserved in converted body

- **Section:** Sections 2, 3 (sqr_skipresnet_siren_backbone, physics_constrained_loss)
- **Description:** 3 author comments from the LaTeX source (`\authcomment{}`) are preserved in the converted body as bold bracketed text (`**[...]**`). These are editorial notes from the original authors, not content discrepancies:
  1. "Need more detail on this dynamic scheduling for omega_0" (Section 2)
  2. "Need confirmation on this hidden layer's detail" (Section 2)
  3. "Comment: This above batch construction is not consistent with the CTL instruction plan" (Section 3)
- **Status:** Documented for future reconciliation — author should resolve these notes before training implementation

### SI-PINN-003: Batch construction inconsistency with CTL instruction plan

- **Section:** Section 3 (physics_constrained_loss) — Data Batch Construction code block
- **Description:** The author comment "This above batch construction is not consistent with the CTL instruction plan" flags a methodological inconsistency between the data sampling strategy described here and the CTL curriculum training plan. This should be investigated and resolved during training implementation.
- **Status:** Documented for future reconciliation

---

*End of faithful converted body. Source Issues section above is metadata excluded from fidelity comparison (D-19).*
