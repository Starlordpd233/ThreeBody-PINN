# Section 1: Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems

The accurate and long-term simulation of $\mathrm{N}$-body gravitational systems, particularly the notoriously chaotic three-body problem, presents a formidable challenge for traditional numerical and machine learning methods alike. The dynamics are characterized by an extreme sensitivity to initial conditions, where infinitesimal perturbations can lead to exponentially divergent trajectories over time. Furthermore, the solutions often contain a complex mixture of smooth, quasi-periodic motion and sharp, high-frequency events that occur during close encounters between bodies. A successful predictive model must therefore not only capture these multi-scale temporal features with high fidelity but also adhere to fundamental global conservation laws, such as the conservation of total energy and angular momentum, to ensure its long-term physical plausibility.$^1$

A generic neural network architecture, such as a standard Multi-Layer Perceptron (MLP), lacks the specific structural priors necessary to handle this confluence of challenges. Such models often suffer from a \"spectral bias,\" a tendency to learn low-frequency functions more easily, which makes them struggle to represent the high-frequency components inherent in chaotic dynamics.$^2$ More critically, enforcing the governing physical laws---in this case, Newton's laws of motion---within a Physics-Informed Neural Network (PINN) framework requires the computation of high-order derivatives of the network's output. For the $\mathrm{N}$-body problem, this involves calculating the second derivative of the predicted position with respect to time, $\frac{\mathrm{d}^2 \mathrm{r}}{\mathrm{d} t^2}$, to form the physics residual term in the loss function. Common activation functions like the Rectified Linear Unit (ReLU) are fundamentally unsuitable for this task. While computationally efficient, ReLU produces a piecewise linear output, meaning its first derivative is piecewise constant and its second derivative is a series of Dirac delta functions (i.e., zero almost everywhere). This mathematical property makes it impossible to accurately represent the smooth, continuously varying gravitational forces that govern celestial motion.$^1$

To overcome these fundamental limitations, a more principled approach is required---one where the architecture itself imparts a strong inductive bias that aligns with the underlying physics. The framework detailed in this report proposes a hybrid PINN that is not an arbitrary collection of techniques but a meticulously co-designed system. Each architectural component is deliberately chosen to counteract a specific, well-understood failure mode of standard models when applied to chaotic physical systems. This synergistic design methodically addresses the core requirements of the problem:

1.  **Derivative Fidelity:** To accurately enforce the physics residual, the network must be built with an activation function that is infinitely differentiable ($\mathrm{C}^\infty$) and whose derivatives are well-behaved. The Sinusoidal Representation Network (SIREN) architecture, which uses the sine function as its nonlinearity, is the ideal choice. The derivative of a sinusoid is another sinusoid, merely phase-shifted, a property that is preserved for higher-order derivatives. This provides a powerful inductive bias towards learning smooth functions whose derivatives are also smooth, a property essential for minimizing the physics residual with high fidelity.$^1$

2.  **Expressivity and Training Stability:** Capturing the intricate complexity of chaotic trajectories requires a network with significant expressive capacity, which is typically achieved through depth. However, training very deep neural networks is notoriously difficult due to the well-known problems of vanishing and exploding gradients. The Residual Network (ResNet) backbone provides a solution by incorporating \"skip\" connections that create an identity mapping shortcut, allowing gradients to flow unimpeded through the network's depth. This report specifies the use of a particularly effective variant, the Power-Enhanced SkipResNet (SQR-SkipResNet), which has been empirically shown to provide more stable gradient flow and superior performance on non-smooth functions, making it well-suited for deep architectures.$^1$

3.  **Long-Term Physical Plausibility:** Even a PINN that perfectly satisfies the local, instantaneous equations of motion can accumulate numerical drift over long time horizons, leading to unphysical outcomes such as a gradual increase or decrease in the total energy of an isolated system. While specialized architectures like Hamiltonian Neural Networks (HNNs) can enforce energy conservation by construction through a symplectic structure, they often impose rigid constraints on the network's form (e.g., requiring the use of canonical coordinates) that can limit its flexibility as a general function approximator.$^1$ The proposed architecture adopts a more pragmatic and flexible approach by incorporating the principle of energy conservation as a \"soft\" constraint within the loss function. This HNN-style energy regularizer penalizes the network for any deviation of the predicted total energy from its known initial value, guiding the optimization process toward solutions that lie on or near the constant-energy manifold defined by the initial conditions. This strategy provides the primary benefit of an HNN---energy conservation---without its restrictive architectural costs, thereby improving the long-term physical plausibility of the model's predictions.$^1$

This philosophy of pragmatic hybridization, which strategically borrows the most critical benefits from multiple advanced paradigms while avoiding their most restrictive drawbacks, is a central theme of the proposed design. The resulting model is a synergistic whole, where the SQR-SkipResNet enables the necessary depth for expressivity, the SIREN activations provide the derivative fidelity required for physics enforcement, and the HNN-style loss term ensures the long-term stability essential for physical realism.

# The SQR-SkipResNet-SIREN Backbone: A Deep Dive into the Core Architecture

This section provides the definitive, mathematically-grounded specifications for each component of the neural network's core structure. Every choice is justified by its contribution to the model's ability to represent complex physical phenomena accurately and to be trained stably.

## The Sinusoidal Activation (SIREN): The Key to Derivative Fidelity

The foundational element of the network's layers is the Sinusoidal Representation Network (SIREN) activation function. This choice is not a tunable hyperparameter but a mandatory architectural feature dictated by the physics of the $\mathrm{N}$-body problem. A standard neural network layer performs an affine transformation followed by a non-linear activation. In a SIREN layer, this activation is the sine function$^5$: $$\phi_i(\mathrm{x}) = \sin(\mathrm{W}_i \mathrm{x} + \mathrm{b}_i)$$ where $\mathrm{x}$ is the input to the layer, and $\mathrm{W}_i$ and $\mathrm{b}_i$ are the trainable weight matrix and bias vector, respectively.

The primary motivation for this choice lies in the properties of its derivatives. The derivative of a sinusoidal function is another sinusoid, merely phase-shifted and scaled. For a single neuron with activation $\phi(\mathrm{x}) = \sin(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b}))$, the chain rule gives: $$\frac{\mathrm{d} \phi}{\mathrm{d} \mathrm{x}} = \omega_0 \mathrm{w} \cos(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b})) = \omega_0 \mathrm{w} \sin(\omega_0 (\mathrm{w} \cdot \mathrm{x} + \mathrm{b}) + \frac{\pi}{2})$$

This property is recursive; higher-order derivatives of the network's output with respect to its input remain well-behaved, smooth, sinusoidal functions. This is a stark contrast to common activations like ReLU, whose second derivatives are ill-defined or zero almost everywhere, making them fundamentally unsuited for problems where the loss function depends on second-order derivatives, as is the case for the $\mathrm{N}$-body problem's physics residual.$^1$ The SIREN architecture thus provides an exceptionally strong inductive bias for representing the smooth, continuous solutions and their derivatives required by the governing physical laws. This directly overcomes the spectral bias of standard MLPs, which struggle to represent the high-frequency details inherent in chaotic trajectories and their derivatives.$^2$ By using SIREN, the network is inherently capable of representing the complex natural signals that arise from physical systems.$^8$

## A Principled Initialization Scheme for SIREN Layers

The successful training of a deep SIREN is critically dependent on a specific, principled initialization scheme. Naive initialization will cause the distribution of activations to either collapse to zero or explode into saturated regimes, halting the learning process. The confusion between different documents regarding the hyperparameter $\omega_0$ is resolved here by adhering to the original, mathematically-derived SIREN initialization scheme, which is designed to preserve the distribution of activations as they propagate through the network.$^5$

This scheme is not a heuristic but a carefully designed solution to two distinct challenges: representation and trainability. It treats the first layer of the network differently from all subsequent hidden layers.

1.  To optimize network stability during chaotic stages, we dynamically schedule the initial frequency parameter, $\texttt{first\_omega\_0}$, using an exponential decay. This ensures stable representation as complexity increases:

    ```python
    import math

    def update_omega0(epoch, total_epochs):
        initial_omega = 30.0   # Initial high-frequency
        final_omega = 10.0     # Stabilizing value  
        decay_rate = 5.0       # Controls decay
        return final_omega + (initial_omega - final_omega) * \
               math.exp(-decay_rate * epoch / total_epochs)
    ```

    **Rationale**:

    - **Initial high-frequency (30)**: Essential for early stages to overcome spectral bias.

    - **Exponential reduction to 10**: Ensures smoother representation in chaotic dynamics, reducing numerical instabilities and promoting stable training.

    **[Need more detail on this dynamic scheduling for omega_0. Is it based on stages? How do we dynamically adjust it? Based on epochs? Need more details on this.]**

2.  **Subsequent Hidden Layers (for Trainability):** For all other hidden layers, the weights $\mathrm{W}$ are initialized from a different uniform distribution, $\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]$.\
    The hidden_omega_0 parameter is also set to 1. The crucial difference is the scaling of the initialization range by $\omega_0$. This specific scaling is mathematically derived to ensure that the pre-activations (the inputs to the sine function) maintain a standard normal distribution throughout the network's depth. This, in turn, keeps the sine activations in a dynamic, non-saturated range, preventing the frequency of the network's output from growing uncontrollably with depth. This careful, layer-dependent initialization is what makes deep SIRENs trainable by ensuring stable gradient flow.$^1$

    **[Need confirmation on this hidden layer's detail. Need to make sure the formula is correct according to the original SIREN paper?]**

## The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation

While the SIREN initialization enables training, pushing to the depths required for chaotic dynamics (e.g., 12 layers) requires stabilization of the residual connections. This report recommends adopting an advanced ResNet variant with a critical modification: **Layer Normalization (LayerNorm)** applied to the skip path before the power term. This resolves gradient instability while preserving the architecture's benefits for chaotic systems.

The precise mathematical update rules are as follows:

1.  For odd-numbered layers ($l = 1, 3, 5, \ldots$): $$\mathbf{x}^{(l)} = f_{\text{sr}}^{(l)}(\mathbf{x}^{(l-1)}) + \left(\text{LayerNorm}(\mathbf{x}^{(l-1)})\right)^p$$ where:

    - $f_{\text{sr}}^{(l)}$: SIREN block (SineLayer)

    - $\text{LayerNorm}(\mathbf{x})$: Normalizes input to zero mean and unit variance per feature

    - $p = 2$: Power term fixed at 2 (element-wise squaring)

2.  For even-numbered layers ($l = 2, 4, 6, \ldots$): $$\mathbf{x}^{(l)} = f_{\text{pn}}^{(l)}(\mathbf{x}^{(l-1)})$$

### Critical Rationale for LayerNorm
A critical enhancement to the standard SQR-SkipResNet is the application of Layer Normalization to the skip path *before* the element-wise squaring operation. During simulated close encounters, the inputs to these layers (which represent positions and velocities) can vary over orders of magnitude. Without normalization, the squaring operation would amplify these large values, leading to catastrophic gradient explosions. By normalizing the input on the skip path to have zero mean and unit variance, this modification stabilizes the training process while preserving the expressive power of the non-linear power term, which is crucial for modeling the sharp transitions characteristic of close encounters.

### Power Term Justification
The power term $p = 2$ remains critical for modeling non-smooth dynamics. For 3-body systems, close encounters produce velocity/acceleration spikes that require quadratic interaction terms to resolve. $\text{LayerNorm}$ ensures this term remains bounded.

## Finalized Architectural Hyperparameters


  **Hyperparameter**      **Recommended Value**                                                                                                                                                                       **Rationale & Justification**
  ----------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                                                                                                                                                      
  **Hyperparameter**      **Recommended Value**                                                                                                                                                                       **Rationale & Justification**
  Backbone                SQR-SkipResNet with SIREN layers                                                                                                                                                            Superior stability and convergence for non-smooth dynamics, ideal for modeling close encounters in chaotic systems.
  Depth                   12 hidden layers (6 SQR-SkipResNet blocks)                                                                                                                                                  Provides a good balance between the expressive power needed for chaotic dynamics and the trainability on modest hardware.
  Width                   256 neurons/layer                                                                                                                                                                           A strong default that balances model expressivity and computational cost, avoiding the diminishing returns of excessively wide layers.$^1$
  Activation              $\sin(\mathrm{x})$ (SIREN)                                                                                                                                                                  The $\mathrm{C}^\infty$-smoothness is mathematically essential for accurately calculating the second-order derivatives required in the physics loss.$^1$
  LayerNorm               elementwise_affine=True, eps=1e-5                                                                                                                                                           Stabilizes skip path gradients without restricting feature learning. Applied only to odd layers.
  first_omega_0           30                                                                                                                                                                                          A high initial frequency injects a high-frequency basis into the network, helping it overcome spectral bias from the outset.$^1$
  hidden_omega_0          1                                                                                                                                                                                           This value is used within the principled weight initialization formula for hidden layers to ensure a stable distribution of activations, enabling deep network training.$^1$
  Weight Init. (First)    $\mathrm{U}\left[-\frac{1}{n_{\text{in}}}, \frac{1}{n_{\text{in}}}\right]$                                                                                                                  The mathematically-derived initialization for the first SIREN layer to create a random Fourier feature mapping.$^1$
  Weight Init. (Hidden)   $\mathrm{U}\left[-\frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}, \frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}\right]$ **[I believe this formula for initialization is incorrect]**   The principled initialization for all subsequent SIREN layers, designed to preserve activation variance and enable stable training of deep sinusoidal networks.$^1$
  Skip Cadence            Alternating (per SQR SkipResNet)                                                                                                                                                            The alternating pattern of plain and power-enhanced residual layers effectively balances feature transformation and stable gradient flow.$^1$
  Power Term (p)          2 (element-wise square)                                                                                                                                                                     Empirical results demonstrate that $p=2$ provides significant improvements in stability and accuracy without excessive computational overhead.$^1$
  Output Activation       None (Linear)                                                                                                                                                                               The final layer must be linear to allow the predicted positions to take on any real value required by the physical system.

  : Architectural hyperparameters of the SQR-SkipResNet-SIREN backbone (continued)


# The Multi-Component, Physics-Constrained Loss Function

The training of the PINN is guided by a composite loss function that simultaneously optimizes for three distinct yet complementary objectives: fidelity to observed data, adherence to the governing laws of physics, and conservation of total system energy. This multi-component objective function, as detailed in the Augmented Lagrangian Method (ALM) with a separate energy regularization term, enables the network to learn solutions that are not only accurate but also physically plausible and generalizable beyond the specific training data points. Specifically, the total loss function combines the data fidelity term $\mathcal{L}_{\text{data}}$ and the physics adherence term $\mathcal{L}_{\text{physics}}$ through the ALM framework, which introduces a Lagrange multiplier $\lambda_p$ and a quadratic penalty term with coefficient $\mu_p$. Additionally, a separate energy conservation term $\mathcal{L}_{\text{energy}}$ is included with a weight $\lambda_E(k)$ that is dynamically adjusted based on the curriculum stage. The complete total loss is thus expressed as:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda_p \mathcal{L}_{\text{physics}} + \frac{\mu_p}{2} \mathcal{L}_{\text{physics}}^2 + \lambda_E(k) \mathcal{L}_{\text{energy}}$$

**ALM Initialization:**

The initial values for the ALM parameters are as follows:

- $\lambda_p = 0.0$ (Initial Lagrange multiplier)

- $\mu_p = 0.01$ (Initial penalty coefficient)

- $v_p = 0.0$ (Exponential moving average of $\mathcal{L}_{\text{physics}}^2$)

- $\beta = 0.99$ (Momentum for $v_p$)

- $\gamma = 0.01$ (Base learning rate for $\mu_p$ update)

- $\epsilon = 1 \times 10^{-8}$ (Numerical stability constant)

## Data Fidelity Term ($\mathcal{L}_{\text{data}}$): Anchoring to Ground Truth

The purpose of the data fidelity term is to ensure that the network's predictions align with the high-precision trajectory data generated by a trusted numerical integrator. This term grounds the general, physically-plausible solution learned by the PINN to the specific trajectory defined by a given set of initial conditions. While Mean Squared Error (MSE) is a common choice, Mean Absolute Error (MAE) is often more robust to the occasional large deviations or outliers that can occur in chaotic simulations. For this reason, the data fidelity loss is defined using the L1 norm$^1$:

The data fidelity loss is defined using the L1 norm on the **scaled positions**:

$$\mathcal{L}_{\text{data}} = \frac{1}{N_{\text{data}}} \sum_{k=1}^{N_{\text{data}}} ||r'_{\text{pred}}(t'_k) - r'_{\text{true}}(t'_k)||_1$$

where:

- $t'_k$ is the normalized time coordinate in $[-1, 1]$

- $r'_{\text{pred}}(t'_k)$ is the network's predicted **scaled position** vector (the direct output of the network)

- $r'_{\text{true}}(t'_k)$ is the ground truth position from the BRUTUS data, **scaled by the characteristic length $D$** (i.e., $r'_{\text{true}} = r_{\text{true}}/D$)

- $N_{\text{data}}$ is the number of data points in a training batch

- $|| \cdot ||_1$ denotes the L1 norm

**Batch Construction:**

The data points are sampled from the BRUTUS trajectory snapshots as follows:

```python
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
```python

The time points $t_k$ are sampled from the discrete BRUTUS trajectory snapshots available in the training dataset, representing specific moments where high-precision numerical integration data is available. **[Comment: This above batch construction is not consistent with the CTL instruction plan. Look into this.]**

**Key ALM Integration Note:**\
The data term is no longer weighted by a fixed parameter. Instead, its influence is automatically balanced against the physics constraint through the ALM framework. The effective weight of the physics term becomes $(\lambda_p + \mu_p \mathcal{L}_{\text{physics}})$, which adapts during training:

- When physics loss is high $\rightarrow$ ALM increases $\lambda_p$ $\rightarrow$ physics term gets more weight

- When physics loss is low $\rightarrow$ ALM stabilizes $\lambda_p$ $\rightarrow$ balanced optimization

- The adaptive $\mu_p$ prevents oscillations by adjusting based on the variance of physics loss

## Physics Residual Term ($\mathcal{L}_{\text{physics}}$): Enforcing Newtonian Dynamics

This term is the heart of the \"physics-informed\" paradigm. It enforces the governing laws of physics---in this case, Newton's law of universal gravitation---across the entire solution domain, not just at the discrete points where training data is available. This is what endows the network with the ability to generalize and make physically consistent predictions at any point in time.

The physics residual, $f_i(t')$, for each body $\mathrm{i}$ is defined as the discrepancy between the acceleration predicted by the neural network (via automatic differentiation) and the acceleration dictated by the gravitational forces from all other bodies $\mathrm{j}$: $$f_i(t') = a'_{\theta}(t', i) - \sum_{j \neq i} m_j \frac{r'_{\theta}(t', j) - r'_{\theta}(t', i)}{(\|r'_{\theta}(t', j) - r'_{\theta}(t', i)\| + \epsilon_{\text{soft}})^3}$$

where:

- $t'$ : Normalized time in $[-1, 1]$

- $r'$ : Positions scaled by $D$ (characteristic length)

- $a'$ : Accelerations scaled by $D/T^2$

- $m_j$ : Masses (unchanged, as $G=1$ in the dimensionless system)

- $\epsilon_{\text{soft}} = 10^{-5}$ : Softening parameter to prevent division by zero during close encounters

The physics loss is then formulated as the mean squared norm of this residual vector, summed over all bodies and evaluated over a set of $N_{\text{col}}$ collocation points: $$\mathcal{L}_{\text{physics}} = \frac{1}{N_{\text{col}}} \sum_{k=1}^{N_{\text{col}}} \sum_{i=1}^{N} || f_i(t'_k) ||^2$$

**Collocation Point Sampling:**

The collocation points are sampled according to the following strategy:

```python
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
```python

Minimizing this term forces the network to learn a function $\mathrm{r}_\theta(t')$ that is also a solution to the governing ordinary differential equations (ODEs).

**ALM Implementation Details:**

The influence of the physics term is controlled adaptively through the Lagrange multiplier $\lambda_p$ and the penalty coefficient $\mu_p$. After each optimization step (primal step), these parameters are updated in a dual step as follows:

1.  **Update the Lagrange Multiplier ($\lambda_p$):** The multiplier is updated via gradient ascent, which naturally increases the penalty when the physics residual is large.

    $$\lambda_p \leftarrow \lambda_p + \mu_p \mathcal{L}_{\text{physics}}$$

2.  **Update the Adaptive Penalty ($\mu_p$):** The penalty coefficient is updated using a method inspired by the RMSprop optimizer to ensure stability.

    - First, update a moving average of the squared physics loss, $v_p$:

      $$v_p \leftarrow \beta v_p + (1 - \beta) \mathcal{L}_{\text{physics}}^2$$

    - Next, update the penalty parameter $\mu_p$. Based on the RMSprop analogy, the robust update rule is:

      $$\mu_p \leftarrow \frac{\gamma}{\sqrt{v_p + \epsilon}}$$

3.  **Gradient Handling:**\
    -- $\lambda_p$ must be treated as a non-trainable scalar updated via code (not autograd)\
    -- $\mu_p$ is a dynamic parameter updated algorithmically (excluded from backpropagation)

```python
# In the training loop, after optimizer.step():
with torch.no_grad():
    # 1. Update Lagrange multiplier (gradient ascent)
    lambda_p += mu_p * physics_loss.item()
    
    # 2. Update moving average of squared physics loss
    v_p = beta * v_p + (1 - beta) * (physics_loss.item() ** 2)
    
    # 3. Update adaptive penalty (RMSprop-inspired)
    mu_p = gamma / (np.sqrt(v_p + epsilon))  # Note: using np.sqrt
    
    # 4. Clamp mu_p to prevent runaway values
    mu_p = np.clip(mu_p, 1e-4, 100)  # Changed from torch.clamp to np.clip
    
# Note: lambda_p, mu_p, v_p are NOT part of model.parameters()
# They are maintained as separate scalars with requires_grad=False
```python

## HNN-Style Energy Regularizer ($\mathcal{L}_{\text{energy}}$): Enforcing a Global Conservation Law

While the physics residual enforces the local, instantaneous laws of motion, it does not explicitly guarantee the conservation of global quantities over long time horizons. For an isolated mechanical system like the $\mathrm{N}$-body problem, the total energy is one such conserved quantity. The energy loss term is designed to combat the long-term energy drift that can plague standard PINN models by explicitly penalizing deviations from this fundamental conservation law.$^1$

The total energy of the $\mathrm{N}$-body system, its Hamiltonian $H_{\text{total}}$, is the sum of the total kinetic energy $(T)$ and the total potential energy $(V)$:

$$H_{\text{total}}(r', v') = T + V = \sum_{i=1}^N \frac{1}{2} m_i ||v'_i||^2 - \sum_{i<j} \frac{m_i m_j}{||r'_i - r'_j|| + \epsilon_{\text{soft}}}$$

This represents the total energy in the non-dimensional unit system. The positions ($r'$) and velocities ($v'$) are the scaled outputs from the network. The initial energy, $H_0$, must also be computed in these same dimensionless units for the loss term to be consistent.\
The energy loss term penalizes any deviation of the predicted total energy from its initial total energy, $H_0$, which is a constant calculated from the known initial conditions. The loss is computed over the same set of $N_{\text{col}}$ collocation points as the physics loss:

$$\mathcal{L}_{\text{energy}} = \frac{1}{N_{\text{col}}} \sum_{k=1}^{N_{\text{col}}} L_\delta(\Delta H_k)$$

where:

1.  $\Delta H_k = H_{\text{total}}(r_\theta(t'_k), v_\theta(t'_k)) - H_0$

2.  $H_0$ is the precomputed initial energy for each trajectory (See the code below for the exact calculation.)

3.  $L_\delta$ is the Huber loss with $\delta = 1.0$: $$L_\delta(a) =
        \begin{cases}
            \frac{1}{2} a^2 & \text{for } |a| \leq \delta \\
            \delta (|a| - \frac{1}{2} \delta) & \text{for } |a| > \delta
        \end{cases}$$

**Initial Energy Calculation:**

The initial energy $H_0$ is precomputed during dataset preprocessing:

```python
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
    epsilon_soft = 1e-5  # Same softening parameter
    
    # Fixed for 3-body problem
    N_bodies = 3
    
    # 1. KINETIC ENERGY (dimensionless)
    for i in range(N_bodies):
        H_0 += 0.5 * masses[i] * np.sum(v0_prime[i]**2)
    
    # 2. POTENTIAL ENERGY (dimensionless)
    for i in range(N_bodies):
        for j in range(i+1, N_bodies):
            r_ij = np.linalg.norm(r0_prime[i] - r0_prime[j])
            H_0 -= masses[i] * masses[j] / (r_ij + epsilon_soft)
            
    return H_0
```python

**Energy Regularization Schedule:**

The weight of the energy loss term is scheduled according to the curriculum stage:

$$\lambda_E(k) = 10^{k-3} \quad \text{for } k \in \{0, 1, \ldots, 6\}$$

This results in the following stage-specific values:

- Stage 0: $\lambda_E = 10^{-3} = 0.001$

- Stage 1: $\lambda_E = 10^{-2} = 0.01$

- Stage 2: $\lambda_E = 10^{-1} = 0.1$

- Stage 3: $\lambda_E = 10^{0} = 1$

- Stage 4: $\lambda_E = 10^{1} = 10$

- Stage 5: $\lambda_E = 10^{2} = 100$

- Stage 6: $\lambda_E = 10^{3} = 1000$

**Key Implementation Notes:**

- **Unit System Consistency:** All quantities (positions $r'$, velocities $v'$, and initial energy $H_0$) must be expressed in the same non-dimensional ($G = 1$) system of units.

- **Softening Parameter:** The same value $\epsilon_{\text{soft}} = 10^{-5}$ is used consistently in both the physics residual and energy calculations to prevent numerical instabilities during close encounters.

- **Collocation Points:** The same set of $N_{\text{col}}$ points is used for both physics and energy loss evaluation to ensure computational efficiency.

# Advanced Training and Optimization Strategy

Successfully training the network requires a sophisticated approach to navigate the complex, non-convex loss landscape and handle numerical instabilities.

## Adaptive Loss Balancing via ALM

The balance between the data fidelity term ($\mathcal{L}_{\text{data}}$) and the physics residual term ($\mathcal{L}_{\text{physics}}$) is handled automatically by the Adaptive Augmented Lagrangian Method (ALM). The influence of the physics term is controlled adaptively through the Lagrange multiplier $\lambda_p$ and the penalty coefficient $\mu_p$. These parameters are updated algorithmically after each optimization step, outside of the standard backpropagation graph.

## Two-Phase Optimization

To achieve both efficient exploration and high-precision convergence, a two-phase optimization strategy is employed.

1.  **Phase 1 (Exploration):** The initial training phase utilizes the **Adam optimizer**. Its adaptive learning rates and momentum-based updates are well-suited for navigating the highly non-convex loss landscape in the early stages of training, efficiently finding a good basin of attraction.

2.  **Phase 2 (Fine-Tuning):** Once the Adam optimizer has converged, the process can be switched to a quasi-Newton method like **L-BFGS** to \"polish\" the solution. Because full-batch L-BFGS is memory-intensive, a mini-batch variant (Stochastic L-BFGS) is recommended for larger datasets.

## Adaptive Gradient Clipping

A significant challenge arises from the inverse-square distance terms in the loss function, which can explode during simulated close encounters. To prevent a single event from destabilizing the optimizer, adaptive gradient clipping is essential. A robust strategy is to clip the global L2 norm of the gradients relative to their recent typical magnitude.

```python
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
```python

# Inference and Trajectory Generation

Once the model is trained, it can be used as a high-fidelity function approximator to generate entire trajectories on demand.

## Generating a Trajectory

To predict the evolution of a system from a given initial condition ($IC$), the following procedure is used:

1.  **Define Evaluation Times:** Create a fine-grained array of time points, $t_{eval}$, over the desired simulation interval (e.g., 10,000 points from $t=0$ to $t_{max}$). Normalize these time points to the model's input range of $[-1, 1]$.

2.  **Predict Positions:** For each normalized time point in $t_{eval}$, feed it concatenated with the constant $IC$ vector into the trained network. This will produce a continuous trajectory of the system's positions, $r_{\theta}(t_{eval})$.

3.  **Derive Kinematics (Optional):** If velocities or accelerations are needed for analysis, they can be derived at any evaluation point by using automatic differentiation on the network with respect to the time input.

## Output Layer and Kinematic Consistency via Automatic Differentiation

The network architecture is simplified and physical consistency is hard-coded by predicting only positions and deriving all other kinematic quantities via automatic differentiation (AD). This is a core design principle of PINNs, supported by established frameworks like DeepXDE.$^{14}$

The final layer of the SQR-SkipResNet-SIREN network is a standard linear layer without any activation function. This is crucial as it allows the network's outputs---the predicted positions---to take on any real value required by the physical system. The output is a 9-dimensional vector representing the concatenated positions of the three bodies at a given time $\mathrm{t}$: $$\mathrm cl r_\theta(\mathrm{t}) = [\mathrm{r}_1(\mathrm{t}), \mathrm{r}_2(\mathrm{t}), \mathrm{r}_3(\mathrm{t})]$$

Crucially, the network does not predict velocities or accelerations directly. Instead, these kinematic quantities are derived from the position outputs using AD with respect to the time input, $t$. The velocity vector is computed as the first-order derivative of the position vector, and the acceleration vector is computed as the second-order derivative$^1$: $$\mathrm{v}_\theta(\mathrm{t}) = \frac{\mathrm{d} \mathrm{r}_\theta(\mathrm{t})}{\mathrm{d} \mathrm{t}} \quad \text{and} \quad \mathrm{a}_\theta(\mathrm{t}) = \frac{\mathrm{d}^2 \mathrm{r}_\theta(\mathrm{t})}{\mathrm{d} \mathrm{t}^2}$$

By computing derivatives via AD, the fundamental kinematic relationships between position, velocity, and acceleration $(\mathrm{v} = \mathrm{r}', \mathrm{a} = \mathrm{r}'')$ are satisfied by construction to machine precision. This hard-codes a significant portion of the problem's physics into the model, simplifies the network architecture (as no extra heads are needed for velocity or acceleration), and makes the overall learning task more tractable.

## Output Frame and File Format

For consistency and physical correctness, the output of the model must be clearly defined.

- **Reference Frame:** The predicted positions, $r_{\theta}(t)$, are in the **Center of Mass (COM) frame**. This is consistent with the use of translation-invariant quantities in the input vector.

- **Output File Format:** The final generated trajectory should be saved in a structured format, such as a CSV file, for easy analysis and visualization. Each row should represent a single time step.

- **Output Definition:** The output at each network forward pass is strictly the positions of the three bodies at a single normalized input time $t'$; velocities and accelerations are derived via AD.

**Example CSV Output Format:**

    time,x1,y1,z1,x2,y2,z2,x3,y3,z3
    0.00,-0.98,0.20,0.00,0.49,-0.10,0.00,0.49,-0.10,0.00
    0.01,-0.97,0.21,0.00,0.48,-0.11,0.00,0.49,-0.10,0.00
    ...


  -------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Component**                                **Definitive Specification**                                                                                                                                                                                                              **Justification**

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

  **Input Vector**                             A **14-dimensional vector** `[t, IC]`, where `t` is time normalized to $[-1,1]$ and `IC` is a 13-component vector of initial conditions. The IC vector contains:\                                                                         This formulation provides a physically-grounded and injective (unambiguous) representation of the initial state, which is critical for a conditional network to learn correctly.
                                               • 3 masses.\                                                                                                                                                                                                                              
                                               • 5 physical invariants.\                                                                                                                                                                                                                 
                                               • 5 values for 3 trigonometrically encoded angles.                                                                                                                                                                                        

  **Output**                                   A **9-dimensional position vector** `[r1(t), r2(t), r3(t)]` with a linear (no activation) final layer. Velocities ($v=\frac{dr}{dt}$) and accelerations ($a=\frac{d^{2}r}{dt^{2}}$) are derived via **Automatic Differentiation (AD)**.   Predicting only positions simplifies the network architecture. Deriving kinematics via AD hard-codes their fundamental physical relationship, ensuring they are satisfied by construction to machine precision.

  **Data Loss ($\mathcal{L}_{data}$)**         **Mean Absolute Error (MAE / L1 Norm)** of the predicted positions against the ground truth data.                                                                                                                                         MAE is more robust to the occasional large deviations and outliers that are common in chaotic N-body simulations compared to MSE.

  **Physics Loss ($\mathcal{L}_{physics}$)**   **Mean Squared Error (MSE)** of the physics residual. The residual is the difference between the network's AD-computed acceleration and the acceleration calculated from Newton's law of gravitation (in $G=1$ units).                    This loss enforces the governing ordinary differential equations across the entire solution domain, not just at data points, allowing the model to generalize and make physically consistent predictions.

  **Energy Loss ($\mathcal{L}_{energy}$)**     **Huber Loss ($\delta=1.0$)** on the deviation between the network's predicted total energy (Hamiltonian) and the pre-computed, constant initial energy ($H_0$), all in $G=1$ units.                                                      Enforces the global conservation of energy, which combats long-term numerical drift and improves the physical plausibility of the simulation over long time horizons.
  -------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  : Consolidated Implementation Blueprint Summary


17 Power-enhanced ResNet for Function Approximation.pdf PIG: PHYSICS-INFORMED GAUSSIANS AS ADAPTIVE PARAMETRIC MESH REPRESENTATIONS - OpenReview, accessed June 25, 2025, <https://openreview.net/pdf/ba580795154cc26f5abe3ab4feab161a5246c2f3.pdf> PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://www.researchgate.net/publication/386575809_PIG_Physics-Informed_Gaussians_as_Adaptive_Parametric_Mesh_Representations> PIG: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations, accessed June 25, 2025, <https://openreview.net/forum?id=y5B0ca4mit> Implicit Neural Representations with Periodic Activation Functions, accessed June 25, 2025, <http://arxiv.org/pdf/2006.09661> Implicit Neural Representations with Periodic Activation Functions - NIPS, accessed June 25, 2025, <https://proceedings.neurips.cc/paper/2020/file/53c04118df112c13a8c34b38343b9c10-Paper.pdf> jaeminoh/Siren PINNs: Solving various PDEs by employing Siren, with JAX implementation., accessed June 25, 2025, <https://github.com/jaeminoh/Siren_PINNs> Implicit Neural Representations with Periodic Activation Functions - Vincent Sitzmann, accessed June 25, 2025, <https://www.vincentsitzmann.com/siren/> Implicit Neural Representations with Periodic Activation Functions \| NeurIPS 2020, accessed June 25, 2025, <https://www.computationalimaging.org/publications/siren/> Gentle Introduction to SIREN - Nail Ibrahimli - TU Delft 3D Geoinformation, accessed June 25, 2025, <https://3d.bk.tudelft.nl/nail/siren/> Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - arXiv, accessed June 25, 2025, <https://arxiv.org/html/2310.15690v2> Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/382109760_Power-Enhanced_Residual_Network_for_Function_Approximation_and_Physics-Informed_Inverse_Problems> Physics-Informed with Power-Enhanced Residual Network for Interpolation and Inverse Problems - ResearchGate, accessed June 25, 2025, <https://www.researchgate.net/publication/374946733_Physics-Informed_with_Power-Enhanced_Residual_Network_for_Interpolation_and_Inverse_Problems> Software \| PNNL, accessed June 25, 2025, <https://www.pnnl.gov/projects/philms/software> lululxvi/deepxde: A library for scientific machine learning and physics-informed learning - GitHub, accessed June 25, 2025, <https://github.com/lululxvi/deepxde> DeepXDE: A Deep Learning Library for Solving Differential Equations \| SIAM Review - myqcloud.com, accessed June 25, 2025, <https://pdf-1307664364.cos.ap-chengdu.myqcloud.com/%E8%AE%BA%E6%96%87%E5%8F%82%E8%80%83/PINN/DeepXDE-%20A%20Deep%20Learning%20Library%20for%20Solving%20Differential%20Equations.pdf> omniscientoctopus/Physics-Informed-Neural-Networks: Investigating PINNs - GitHub, accessed June 25, 2025, <https://github.com/omniscientoctopus/Physics-Informed-Neural-Networks>

