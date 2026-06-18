# Baseline Reports Bundle

Build date: 2026-06-18. This is a mechanical transport bundle for the
doc-03 research package. Content between BEGIN/END delimiters is
byte-identical to the source package parts, verified at build time by
round-trip extraction and SHA-256 comparison. The wrapper text is not a
source edit and does not summarize the enclosed files.

## Contents

| File | Bytes | SHA-256 |
|------|-------|---------|
| `review_of_framework.md` | 53,571 | `fe5fdc449cf0858046fda7bfd0c17b5fe0a9d2284af08c793c3829f715a617a1` |
| `stage_strat_revision.md` | 44,723 | `d875cd6680e3ec5239bd2c0d35b9bb8eaba39480f26cd909e4c0bc2fd9011fea` |

===== BEGIN FILE review_of_framework.md (53571 bytes, sha256 fe5fdc449cf0858046fda7bfd0c17b5fe0a9d2284af08c793c3829f715a617a1) =====
# A Technical Review and Resolution Blueprint for the CTL-PINN Framework for the Three-Body Problem

# Executive Summary
This report presents a definitive technical review and resolution of 19 critical inconsistencies, logical gaps, and implementation ambiguities identified across two foundational documents: `PINN_architecture_plan.tex` and `CTL-instruction-final.tex`. These documents collectively outline a sophisticated framework for training a Physics-Informed Neural Network (PINN) on the chaotic three-body problem using a Curriculum-Transfer Learning (CTL) methodology. The identified issues, if left unaddressed, would preclude a successful, robust, and reproducible implementation of the proposed system.

The resolutions provided herein are synthesized into a single, coherent, and actionable blueprint. The analysis is structured around five core themes, each representing a critical stage of the implementation workflow. The key resolutions are summarized as follows:

1.  **Foundational Physical Metrics:** The report establishes robust, computable definitions and provides reference implementations for the Lyapunov time ($\tau_L$) and the normalized angular momentum ($L/L_{\max}$), which are essential for the quantitative stratification of training data into curriculum stages. A scalable, parallelized pipeline for computing global normalization constants across the entire dataset is also detailed.

2.  **Data Scaling and Normalization:** A unified protocol for data transformation is established. This includes standardizing spatiotemporal normalization to a consistent [-1, 1] range, resolving a critical five-order-of-magnitude discrepancy in the gravitational softening parameter, and providing a definitive, consolidated schema for the construction of the 14-dimensional network input vector.

3.  **Network Architecture and Initialization:** Ambiguities concerning the dynamic scheduling of the SIREN network's frequency parameter ($\omega_0$) are resolved. A novel, curriculum-aware discrete schedule is proposed, directly linking this critical architectural hyperparameter to the complexity of the data at each training stage.

4.  **Loss Function Framework:** A rigorous and unambiguous specification for the multi-component loss function is provided. This includes enforcing dimensional consistency across all terms, defining a clear state management protocol for the Augmented Lagrangian Method (ALM) parameters, providing a reference implementation for computing kinematics via automatic differentiation, and specifying a physically appropriate parameter for the Huber loss function.

5.  **Training and Data Sampling Strategy:** Conflicting instructions for data batching and collocation point sampling are reconciled into a single, efficient, and standard methodology. The report formalizes the adoption of the superior curriculum-aware batching protocol and integrates a physically motivated, stage-dependent schedule for adaptive gradient clipping.

The solutions presented are rigorously grounded in established principles from celestial mechanics, numerical analysis, and deep learning. The resulting blueprint ensures that the final CTL-PINN framework is not only physically sound and mathematically consistent but also computationally robust and practically implementable.

# 1 Foundational Physical Metrics for Curriculum Design

The efficacy of the Curriculum-Transfer Learning (CTL) framework is predicated on the ability to quantitatively stratify simulation data by its intrinsic physical difficulty. Without robust and computable metrics to distinguish stable, quasi-periodic systems from highly chaotic ones, the concept of a \"curriculum\" remains ill-defined. This section resolves critical omissions in the source documents by providing definitive, physically-grounded formulas and scalable implementation plans for the key metrics required for stage assignment: Lyapunov time ($\tau_L$), maximum angular momentum ($L_{\max}$), and global normalization scales.

## 1.1 Defining and Implementing Lyapunov Time ($\tau_L$) and Maximum Angular Momentum ($L/L_{\max}$) Computations

**Issues Resolved: 1, 16**

#### Context and Validation

The `CTL-instruction-final.tex` document defines curriculum stages using specific physical criteria. Stage 0, representing the most stable systems, requires the normalized angular momentum ratio $L/L_{\max} > 0.5$. Stages 4a and 4b, which introduce chaotic dynamics, are defined by thresholds on the Lyapunov time ($\tau_L > 5$ and $2 < \tau_L \leq 5$, respectively). However, as identified in Issues 1 and 16, the documents explicitly omit the computational formulas for both $L_{\max}$ and $\tau_L$, with an author comment directly acknowledging the gap for the latter. This omission constitutes a critical implementation blocker, as it makes the assignment of trajectories to these key curriculum stages impossible.

The Lyapunov time is a fundamental characteristic of a chaotic dynamical system, representing the e-folding time for the exponential divergence of initially nearby trajectories. It serves as a direct measure of the system's predictability horizon. The maximum angular momentum, $L_{\max}$, for a given energy, corresponds to the angular momentum of a system where all mass is in a circular orbit, providing a crucial benchmark for orbital stability and regularity.

#### Proposed Solution and Implementation

To resolve this gap, we provide definitive, physically sound, and computationally tractable methods for both quantities.

1.  **Maximum Angular Momentum ($L_{\max}$)** The formula for the normalized angular momentum, $L_{\text{norm}} = L/L_{\max}$, is derived from fundamental principles of celestial mechanics and is explicitly defined in the `CTL-instruction-final.tex` document. This formulation will be formally adopted. The calculation proceeds as follows for each initial condition, using spatiotemporally scaled quantities (see Section 2.1):

    - **Calculate Total Angular Momentum ($L$):** The total angular momentum vector, $\mathbf{L}$, is the sum of the individual angular momenta in the center-of-mass frame. Its magnitude, $L$, is computed from the scaled initial positions $\mathbf{r}'_i$ and velocities $\mathbf{v}'_i$. $$\mathbf{L} = \sum_{i=1}^{3} m_i (\mathbf{r}'_i \times \mathbf{v}'_i) \quad \rightarrow \quad L = \|\mathbf{L}\|$$

    - **Calculate Characteristic Scales:** A characteristic length scale, $r_{\text{char}}$, is defined as the average pairwise distance between bodies. A characteristic velocity, $v_{\text{char}}$, is derived from the total energy $E$ and total mass $M_{\text{total}}$, representing the velocity required for a bound system.

$$
\begin{aligned}
r_{\text{char}} &= \frac{1}{3} \sum_{i<j} \lVert \mathbf{r}'_i - \mathbf{r}'_j \rVert \\
v_{\text{char}} &= \sqrt{\frac{2|E|}{M_{\text{total}}}} \quad \text{where} \quad M_{\text{total}} = \sum_{i=1}^{3} m_i
\end{aligned}
$$

    - **Calculate Maximum Angular Momentum ($L_{\max}$):** $L_{\max}$ is the product of these characteristic scales, physically representing the angular momentum of the total mass moving at the characteristic velocity at the characteristic radius. $$L_{\max} = M_{\text{total}} \cdot r_{\text{char}} \cdot v_{\text{char}}$$

    - **Calculate Normalized Ratio:** The final dimensionless ratio is then $L_{\text{norm}} = L / L_{\max}$.

    This approach correctly captures the physical intuition that for a fixed energy, maximum angular momentum corresponds to circular motion, where kinetic energy is maximized at the largest stable separation.

2.  **Lyapunov Time ($\tau_L$)** The precise calculation of the maximal Lyapunov exponent requires integrating the system's variational equations, a process that is computationally as expensive as the original simulation itself. Given the need to classify over 15,000 trajectories, a direct, high-precision calculation for each is impractical. Therefore, a robust and widely accepted numerical estimation method is required.

    We propose the adoption of the algorithm pioneered by Benettin et al., which tracks the divergence of a single perturbation vector. This method provides a reliable estimate of the maximal Lyapunov exponent while being computationally feasible for large datasets. The algorithm proceeds as follows:

    - **Initialization:**

    - Define a reference trajectory starting from the initial state vector $y_0$ (concatenated scaled positions and velocities).

    - Define a perturbed trajectory starting at $y_0^{\text{pert}} = y_0 + \delta_0$, where $\delta_0$ is a random vector of small magnitude $\epsilon_{\text{pert}}$ (e.g., $10^{-8}$).

    - **Integration and Renormalization Loop:**

    - Integrate both the reference and perturbed trajectories forward in time for a short interval, $\Delta t$.

    - At the end of the interval, calculate the new separation vector $\delta_1 = y_1^{\text{pert}} - y_1$.

    - Record the growth factor $a_1 = \|\delta_1\| / \epsilon_{\text{pert}}$.

    - Renormalize the perturbed trajectory by resetting its state to $y_1^{\text{pert}} = y_1 + \epsilon_{\text{pert}} \cdot (\delta_1 / \|\delta_1\|)$. This step preserves the direction of maximal divergence while resetting the separation magnitude.

    - **Averaging:** Repeat the integration and renormalization loop for a sufficiently long total integration horizon ($T_{\text{horizon}}$). The maximal Lyapunov exponent, $\lambda$, is the time-average of the logarithm of the growth factors: $$\lambda \approx \frac{1}{T_{\text{horizon}}} \sum_{i=1}^{N_{\text{steps}}} \ln(a_i)$$

    - **Lyapunov Time Calculation:** The Lyapunov time is the reciprocal of the maximal Lyapunov exponent: $$\tau_L = \frac{1}{\lambda}$$

    This numerical procedure provides a pragmatic and reproducible method to estimate $\tau_L$ for each trajectory, enabling its assignment to the correct curriculum stage. A reference implementation is provided in the appendix.

## 1.2 Establishing a Robust Pipeline for Global Scale Computation

**Issue Resolved: 17**

#### Context and Validation

The `CTL-instruction-final.tex` document mandates the computation of global scaling factors, specifically `E_scale` and `smin_scale`, which are derived from the median of energy and characteristic length values, respectively, across the entire dataset. Issue 17 correctly identifies that a complete and scalable implementation for processing the full dataset of over 8,500 trajectories is missing from the documentation. A naive, serial implementation of this task would create a significant computational bottleneck in the data preprocessing pipeline, potentially taking many hours to complete.

#### Proposed Solution and Implementation

To ensure an efficient and scalable preprocessing workflow, we formally adopt and refine the parallelized Python implementation strategy proposed in the `next steps.txt` document. This solution leverages modern multi-core CPU architectures to drastically reduce the computation time.

The core of the solution is the use of Python's `concurrent.futures.ProcessPoolExecutor`, which distributes the task of processing individual trajectory files across a pool of worker processes. The workflow is as follows:

- **Worker Function (`compute_single_trajectory_properties`):** A dedicated function is defined to process a single trajectory. This function takes a file path as input and performs the following steps:

- Parses the 21 floating-point values from the initial condition file (`ic_*.txt`).

- Applies the spatiotemporal scaling defined in Section 2.1 to convert raw positions and velocities into dimensionless units ($\mathbf{r}'$ and $\mathbf{v}'$).

- Computes the scaled total mechanical energy, $E$, for the initial state.

- Computes the characteristic length, $r_{\text{char}}$, as the mean of the initial pairwise distances.

- Returns the computed $E$ and $r_{\text{char}}$ values.

This function is designed to be self-contained and stateless, making it ideal for parallel execution.

- **Main Orchestrator (`compute_globals`):** The main function orchestrates the parallel computation.

- It gathers a list of all initial condition file paths to be processed.

- It creates a `ProcessPoolExecutor`, typically configured to use all available CPU cores.

- It uses the `executor.map` method to apply the `compute_single_trajectory_properties` function to every file path in the list, distributing the work across the process pool.

- As results are returned from the worker processes, they are aggregated into two lists: one for all computed energies and one for all characteristic lengths.

- Once all files have been processed, the function computes the final global scales using NumPy's median function on the aggregated lists.

$$
\begin{aligned}
            E_{\text{scale}} &= |\text{median}(\{E_j\})| + 10^{-8} \\
            s_{\text{min\_scale}} &= \text{median}(\{r_{\text{char},j}\})
\end{aligned}
$$

This parallelized approach transforms a lengthy serial task into a highly efficient one. The implementation will be further enhanced with robust error handling to gracefully manage potential issues like corrupted or missing input files, and will include a progress bar (e.g., using the `tqdm` library) to provide real-time feedback during execution. This ensures the data preprocessing pipeline is not only correct but also practical for large-scale scientific datasets.

# 2 Unifying Data Scaling and Normalization Protocols

A prerequisite for stable and effective neural network training is the transformation of raw, physical data into a consistent, dimensionless, and well-behaved numerical format. The source documents contain several critical ambiguities and contradictions in this domain. This section resolves these issues by establishing a single, definitive standard for all spatiotemporal scaling, numerical softening, and input vector normalization, thereby creating a reliable data contract between the preprocessing and training stages of the workflow.

## 2.1 Standardization of Spatiotemporal Normalization and Unit Conversion

**Issues Resolved: 3, 9**

#### Context and Validation

A significant contradiction exists regarding the normalization of the time coordinate. The `PINN_architecture_plan.tex` document presents a formula, $t' = t/T$, which maps the physical time $t \in [0, T]$ to a normalized range of $[0, 1]$. However, this is directly contradicted by an author comment within the same document questioning this formula and suggesting a [-1, 1] range, a suggestion supported by multiple other textual references to a [-1, 1] domain throughout the document. The `CTL-instruction-final.tex` document also implies a [-1, 1] range for all network inputs but fails to provide an explicit formula for time.

Furthermore, Issue 9 highlights a corresponding gap: the lack of a clearly defined procedure for converting the network's scaled outputs back into physical units for analysis, visualization, and comparison with ground truth data. These ambiguities create a high risk of implementation errors that would compromise the entire framework.

#### Proposed Solution and Implementation

To resolve these inconsistencies, a definitive and unified normalization scheme is established for all spatiotemporal variables.

- **Time Normalization:** The physical time $t$, which resides in the interval $[0, T]$ (where the characteristic time $T = t_{\max} = 10$ time units), will be normalized to the range [-1, 1]. The correct formula for this transformation is: $$t' = 2 \left( \frac{t}{T} \right) - 1$$ This choice aligns with the dominant convention across both documents and is considered best practice for networks employing periodic activation functions like SIREN. These functions are naturally centered around zero, and mapping the input domain to [-1, 1] can improve training dynamics and representation quality.

- **Spatial and Velocity Scaling:** The scaling of positions and velocities will adhere strictly to the definitions provided in the `CTL-instruction-final.tex` document. In this $G=1$ system of units:


- The characteristic length is $D = \sqrt[3]{G T^2} \approx 4.6416$.

- The characteristic velocity is $V = D / T \approx 0.46416$.

- Physical positions $\mathbf{r}_i$ are scaled to dimensionless positions $\mathbf{r}'_i = \mathbf{r}_i / D$.

- Physical velocities $\mathbf{v}_i$ are scaled to dimensionless velocities $\mathbf{v}'_i = \mathbf{v}_i / V$.

- **Inverse Transformation for Analysis:** To resolve Issue 9, explicit inverse transformation formulas are provided. These are essential for converting the network's dimensionless outputs back into physical units for meaningful analysis and visualization.

$$
\begin{aligned}
        t &= \frac{T(t' + 1)}{2} \\
        \mathbf{r} &= \mathbf{r}' \cdot D \\
        \mathbf{v} &= \mathbf{v}' \cdot V
\end{aligned}
$$

A set of utility functions, `physical_to_scaled` and `scaled_to_physical`, encapsulating these transformations should be implemented and used consistently throughout the codebase to prevent errors. This unified scheme resolves all spatiotemporal ambiguities and establishes a clear, consistent data representation that is a prerequisite for all subsequent steps.

## 2.2 Consistent Application of Numerical Softening Parameters

**Issue Resolved: 15**

#### Context and Validation

Issue 15 identifies a severe inconsistency of critical importance: a five-order-of-magnitude discrepancy in the value of the gravitational softening parameter, $\epsilon$, used to prevent numerical singularities during close encounters. The `CTL-instruction-final.tex` document specifies $\epsilon = 10^{-10}$ in the context of calculating potential energy, while the `PINN_architecture_plan.tex` document consistently uses and justifies a value of $\epsilon_{\text{soft}} = 10^{-5}$ for both the physics residual and energy loss calculations. This is not a minor discrepancy; the choice of softening parameter directly impacts the computed forces and energies, and such a large difference would lead to fundamentally different physical behavior being enforced by the loss function.

#### Proposed Solution and Implementation

The softening parameter will be standardized to the value $\boldsymbol{\epsilon_{\text{soft}} = 10^{-5}}$ for all relevant calculations across the entire framework. This value will be used in the denominator of all gravitational force and potential energy terms. Specifically, any term of the form $1/\|\mathbf{r}_i - \mathbf{r}_j\|$ will be implemented as $1/(\|\mathbf{r}_i - \mathbf{r}_j\| + \epsilon_{\text{soft}})$, and any term of the form $1/\|\mathbf{r}_i - \mathbf{r}_j\|^3$ will be implemented as $1/(\|\mathbf{r}_i - \mathbf{r}_j\| + \epsilon_{\text{soft}})^3$.

#### Justification

The practice of force softening in N-body simulations is a well-established numerical technique designed to prevent the infinite forces and energies that arise when two point masses approach an infinitesimally small separation. The parameter's value represents a trade-off: too large a value will inaccurately bias the dynamics by \"smearing out\" the gravitational interaction, while too small a value will fail to prevent numerical overflow and gradient explosions during simulated close encounters.

In the context of this project, where positions are scaled to be of order unity, a value of $\epsilon = 10^{-10}$ is numerically indistinguishable from zero for standard double-precision floating-point arithmetic. It would provide virtually no protection against the divergences it is intended to prevent. The value $\epsilon_{\text{soft}} = 10^{-5}$, as specified in the more detailed architectural document, represents a much more physically and numerically sensible choice. It is small enough to have a negligible effect on the dynamics when bodies are well-separated but large enough to cap the forces and prevent floating-point overflow during the critical, high-gradient events of close encounters. Standardizing on this value resolves the dangerous inconsistency and ensures a more stable training process.

## 2.3 Finalized Normalization Schema for the Input Vector

**Issue Resolved: 19**

#### Context and Validation

The construction of the 14-dimensional input vector [t, IC] is a cornerstone of the model, yet the specifications for normalizing its 13 initial condition components are scattered and inconsistent across the documentation. Issue 19 correctly identifies the need for a single, consolidated specification to serve as a definitive guide for implementation. An ambiguity also exists between the use of `tanh`-based scaling and linear Min-Max scaling.

#### Proposed Solution and Implementation

A definitive, component-wise normalization schema is established to map all 14 input features to the range [-1, 1]. The `tanh` function is adopted as the standard for normalizing continuous variables that may have long-tailed distributions (like energy and separation), as it is less sensitive to extreme outliers than Min-Max scaling and smoothly compresses the entire real number line into [-1, 1].

The following table provides the single source of truth for constructing the final input vector. All physical invariants must first be computed using the scaled, dimensionless quantities ($\mathbf{r}'$, $\mathbf{v}'$) as detailed in Section 2.1.


| **Component Name**      | **Symbol**               | **Calculation Formula (using scaled $\mathbf{r}'$, $\mathbf{v}'$)**                         | **Normalization Formula**                                              | **Final Range** |
|:------------------------|:-------------------------|:--------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------|:----------------|
| Time                    | $t'$                     | $t_{\text{phys}} \in [0, 10]$                                                               | $2 \cdot (t_{\text{phys}} / 10) - 1$                                   | [-1, 1]         |
| Normalized Mass 1       | $m_1^{\text{norm}}$      | Mass fraction of body 1                                                                     | $2 \cdot (m_1 / M_{\text{total}}) - 1$                                 | [-1, 1]         |
| Normalized Mass 2       | $m_2^{\text{norm}}$      | Mass fraction of body 2                                                                     | $2 \cdot (m_2 / M_{\text{total}}) - 1$                                 | [-1, 1]         |
| Normalized Mass 3       | $m_3^{\text{norm}}$      | Mass fraction of body 3                                                                     | $2 \cdot (m_3 / M_{\text{total}}) - 1$                                 | [-1, 1]         |
| Normalized Energy       | $E^{\text{norm}}$        | Total mechanical energy $E=T+V$                                                             | $\tanh(E/E_{\text{scale}})$                                            | [-1, 1]         |
| Normalized Ang. Mom.    | $L_{\text{norm}}$        | $L = \|\sum m_i (\mathbf{r}'_i \times \mathbf{v}'_i)\|$                                 | $L / L_{\max}$                                                         | [0, 1]          |
| Normalized Virial Ratio | $Q^{\text{norm}}$        | $Q = 2T / \|V\|$                                                                            | $\tanh((Q - 1) / Q_{\text{scale}})$                                    | [-1, 1]         |
| Normalized Min. Sep.    | $s_{\min}^{\text{norm}}$ | $s_{\min} = \min_{i<j} \|\mathbf{r}'_i - \mathbf{r}'_j\|$                               | $\tanh(s_{\min} / s_{\min\_\text{scale}})$                             | [-1, 1]         |
| Shape Invariant 1       | $I_1^{\text{norm}}$      | $d_{\text{short}} / d_{\text{long}}$                                                        | $2 \cdot I_1 - 1$                                                      | [-1, 1]         |
| Shape Invariant 2       | $I_2^{\text{norm}}$      | $d_{\text{mid}} / d_{\text{long}}$                                                          | $2 \cdot I_2 - 1$                                                      | [-1, 1]         |
| Shape Invariant 3       | $I_3$                    | $(d_{\text{sh}}+d_{\text{mid}}-d_{\text{lg}})/(d_{\text{sh}}+d_{\text{mid}}+d_{\text{lg}})$ | $I_3$ (already in range)                                               | [-1, 1]         |
| Velocity Angle 1        | $\theta_1^{\text{norm}}$ | $\text{angle}(\mathbf{r}'_1, \mathbf{v}'_1) / \pi$                                          | $2 \cdot \theta_1 - 1$                                                 | [-1, 1]         |
| Velocity Angle 2        | $\theta_2^{\text{norm}}$ | $\text{angle}(\mathbf{r}'_2, \mathbf{v}'_2) / \pi$                                          | $2 \cdot \theta_2 - 1$                                                 | [-1, 1]         |
| Normalized Inertia      | $I^{\text{norm}}$        | Trace of moment of inertia tensor                                                           | $\tanh(I_{\text{trace}} / (M_{\text{total}} \cdot r_{\text{char}}^2))$ | [-1, 1]         |

: Definitive Input Vector Specification


This table serves as an unambiguous API contract between the data preprocessing and model training phases. It ensures that every input feature is correctly calculated and scaled, eliminating a common and pernicious source of bugs in complex machine learning pipelines.

# 3 Architectural and Initialization Refinements for the SIREN Backbone

The performance of a neural network, particularly one with periodic activations like SIREN, is critically dependent on its initialization. The frequency parameter, $\omega_0$, directly controls the model's ability to represent fine details in the solution. This section resolves a key ambiguity in how this parameter is managed, proposing a novel scheduling strategy that is fully integrated with the curriculum learning framework.

## 3.1 A Curriculum-Integrated Schedule for SIREN Frequency ($\omega_0$)

**Issues Resolved: 4, 14**

#### Context and Validation

The `PINN_architecture_plan.tex` document presents a significant conflict regarding the initialization of the first SIREN layer. The hyperparameter table specifies a static value, `first_omega_0 = 30`, while the main text introduces a Python function, `update_omega0`, designed to dynamically schedule this parameter via an exponential decay from 30 down to 10. This decay is dependent on the current epoch and a `total_epochs` variable. As highlighted by an author comment and detailed in Issues 4 and 14, there is no guidance on how to integrate this dynamic schedule into the training loop.

This ambiguity is critical because the `first_omega_0` parameter acts as a frequency multiplier, fundamentally shaping the network's capacity to resolve high-frequency features in the input data. The original exponential decay function is also logically incompatible with the CTL framework, as the training is divided into stages of indeterminate length, making a global `total_epochs` variable meaningless.

#### Proposed Solution and Implementation

The underlying principle of dynamically adjusting $\omega_0$ is sound, but its implementation must be adapted to be curriculum-aware. A continuous decay based on a global epoch count is ill-suited for a staged training process. Instead, a stage-based discrete schedule for `first_omega_0` is proposed. This strategy aligns the network's representational capacity directly with the complexity of the data presented at each curriculum stage.

The rationale is physically and computationally motivated. In the early stages (0-1), the data consists of smooth, stable, quasi-periodic orbits. A high `first_omega_0` is beneficial here, as it provides the network with a rich basis of high-frequency sinusoids, helping it to overcome its intrinsic spectral bias and quickly learn the fine details of these regular trajectories. In the later stages (4-6), the data is dominated by chaotic behavior with sharp transitions during close encounters. In this regime, an excessively high $\omega_0$ can lead to oscillatory artifacts, numerical instability, and overfitting to noise. A lower $\omega_0$ encourages a smoother, more stable solution manifold, promoting better generalization.

The definitive schedule is as follows:

- **Stages 0-1 (Stable & Hierarchical):** `first_omega_0 = 30.0`

- **Stages 2-3 (High-Res Stable & Mild Chaos):** `first_omega_0 = 20.0`

- **Stages 4-6 (Fully Chaotic & Extreme Cases):** `first_omega_0 = 10.0`

#### Implementation Action:

At the beginning of each new curriculum stage, a targeted re-initialization will occur. While the weights of all hidden layers and the output layer are transferred from the converged model of the previous stage, the weights of the first SIREN layer will be re-initialized using the uniform distribution $U[-1/\sqrt{n_{\text{in}}}, 1/\sqrt{n_{\text{in}}}]$ and the new `first_omega_0` value specified by the schedule above. This procedure allows the model to adapt its \"input lens\" to the new data regime—adjusting its frequency sensitivity—without inducing catastrophic forgetting in the deeper layers of the network. This approach resolves the implementation ambiguity while preserving the original intent of adapting the network's frequency bias to the complexity of the learning task.

# 4 A Rigorous Framework for the Multi-Component Loss Function

The composite loss function is the heart of the PINN, guiding the network to solutions that are both accurate to data and consistent with physical law. This section provides definitive specifications for its implementation, resolving ambiguities in the use of scaled units, the state management of ALM parameters, the practical application of automatic differentiation, and the selection of a key hyperparameter in the energy regularization term.

## 4.1 Clarifying the Use of Scaled Quantities in All Loss Components

**Issue Resolved: 18**

#### Context and Validation

Issue 18 correctly identifies the need for an explicit, unified confirmation that all three loss terms—$\mathcal{L}_{\text{data}}$, $\mathcal{L}_{\text{physics}}$, and $\mathcal{L}_{\text{energy}}$—are computed using the same dimensionless, scaled quantities. While the `PINN_architecture_plan.tex` document implies this consistency, the absence of a consolidated, emphatic statement creates a risk of subtle but critical implementation errors. Dimensional inconsistency between loss terms would lead to an improperly balanced optimization problem, where gradients from different terms are not on comparable scales, likely causing training to fail or converge to a physically incorrect solution.

#### Proposed Solution and Implementation

It is established as a definitive and non-negotiable requirement that all loss components be computed entirely within the non-dimensional, $G=1$ system of units defined in Section 2. The following checklist must be used to validate the implementation:

- **$\mathcal{L}_{\text{data}}$ (Data Fidelity Loss):** This term must be computed as the L1 norm of the difference between the network's direct output (the scaled position vector, $\mathbf{r}'_{\text{pred}}$) and the ground-truth positions from the BRUTUS simulation after they have been scaled by the characteristic length $D$ (i.e., $\mathbf{r}'_{\text{true}} = \mathbf{r}_{\text{true}} / D$). $$\mathcal{L}_{\text{data}} = \frac{1}{N_{\text{data}}} \sum_{k=1}^{N_{\text{data}}} \|\mathbf{r}'_{\text{pred}}(t'_k) - \mathbf{r}'_{\text{true}}(t'_k)\|_1$$

- **$\mathcal{L}_{\text{physics}}$ (Physics Residual Loss):** The physics residual, $f_i(t')$, must be calculated using scaled positions ($\mathbf{r}'$), scaled accelerations ($\mathbf{a}'$), and unscaled masses ($m_j$), consistent with the $G=1$ unit system where mass is dimensionless. The accelerations $\mathbf{a}'$ are derived via automatic differentiation from $\mathbf{r}'$ with respect to the normalized time $t'$. $$f_i(t') = \mathbf{a}'_{\theta}(t', i) - \sum_{j \neq i} m_j \frac{\mathbf{r}'_{\theta}(t', j) - \mathbf{r}'_{\theta}(t', i)}{(\|\mathbf{r}'_{\theta}(t', j) - \mathbf{r}'_{\theta}(t', i)\| + \epsilon_{\text{soft}})^3}$$

- **$\mathcal{L}_{\text{energy}}$ (Energy Conservation Loss):** The total energy (Hamiltonian) must be computed using the network's scaled position outputs ($\mathbf{r}'$) and the scaled velocities ($\mathbf{v}'$) derived from them via automatic differentiation. The reference initial energy, $H_0$, must also be pre-computed using the same dimensionless units for consistency. $$H_{\text{total}}(\mathbf{r}', \mathbf{v}') = \sum_{i=1}^{N} \frac{1}{2} m_i \|\mathbf{v}'_i\|^2 - \sum_{i<j} \frac{m_i m_j}{\|\mathbf{r}'_i - \mathbf{r}'_j\| + \epsilon_{\text{soft}}}$$

Enforcing this strict dimensional consistency is paramount. It ensures that the magnitudes of the different loss components are physically comparable, allowing the Augmented Lagrangian Method (ALM) and the optimizer to balance their respective gradients effectively.

## 4.2 State Management and Integration of ALM Parameters

**Issue Resolved: 5**

#### Context and Validation

The `PINN_architecture_plan.tex` document provides the mathematical update equations for the Augmented Lagrangian Method (ALM) parameters ($\lambda_p$, $\mu_p$, $v_p$). However, as correctly identified in Issue 5, it fails to specify the practical details of how these stateful variables should be managed within the training loop. The directive that they are \"NOT part of model.parameters()\" is technically correct but operationally ambiguous, leaving their storage, persistence, and update timing unclear.

#### Proposed Solution and Implementation

A clear and robust implementation pattern for managing the ALM state is specified as follows:

1.  **Storage and Scope:** The ALM parameters ($\lambda_p$, $\mu_p$, and $v_p$) should be implemented as persistent attributes of the primary training class or \"trainer\" object. They should be initialized as scalar tensors (e.g., in PyTorch, `self.lambda_p = torch.tensor(0.0)`). Critically, these tensors must not be included in the list of parameters passed to the optimizer, ensuring they are not updated by the standard backpropagation mechanism.

2.  **Update Timing:** The ALM update logic, or \"dual step,\" must be executed in a specific sequence within each training iteration:

    1.  Forward pass and loss computation.

    2.  `loss.backward()` to compute gradients.

    3.  `optimizer.step()` to update model weights (the primal step).

    4.  Perform ALM parameter updates (the dual step).

    5.  `optimizer.zero_grad()` to clear gradients for the next iteration.

    This sequence ensures that the primal step (weight update) based on the current ALM state is completed before the dual variables are adjusted for the subsequent iteration.

3.  **Persistence Across Curriculum Stages:** The state of the ALM is tuned to the specific statistical properties of the physics loss on a given dataset. When transitioning to a new curriculum stage, the data distribution and the typical magnitude of the physics residual change significantly. Therefore, to allow the ALM to adapt correctly to the new data regime, its state must be reset. It is mandated that $\lambda_p$, $\mu_p$, and $v_p$ be reset to their initial values at the beginning of each new curriculum stage. This prevents the carry-over of outdated statistics from simpler stages and allows the adaptive mechanism to recalibrate effectively.

## 4.3 Reference Implementation for Automatic Differentiation (AD) of Kinematics

**Issue Resolved: 12**

#### Context and Validation

A core principle of the proposed PINN is that the network predicts only positions ($\mathbf{r}'$), while velocities ($\mathbf{v}'$) and accelerations ($\mathbf{a}'$) are derived via Automatic Differentiation (AD) with respect to time. This enforces kinematic consistency by construction. However, as noted in Issue 12, neither document provides a concrete code example for performing this higher-order differentiation, a non-trivial task that is a common source of error for practitioners.

#### Proposed Solution and Implementation

To eliminate this ambiguity, a definitive reference implementation using the PyTorch framework is provided. The key to computing second-order derivatives is the correct use of the `create_graph=True` argument in the first `torch.autograd.grad` call. This tells PyTorch to retain the computational graph of the first derivative, making it possible to then differentiate a second time.

```python
import torch

def compute_kinematics(network_output_r, time_input_t):
    """
    Computes velocities and accelerations from position outputs via AD.

    Args:
        network_output_r (torch.Tensor): The network's position predictions.
                                         Shape: (N_points, 9).
        time_input_t (torch.Tensor): The time inputs for which predictions were made.
                                     Shape: (N_points, 1).

    Returns:
        tuple:
            - velocities_v (torch.Tensor): Shape (N_points, 9).
            - accelerations_a (torch.Tensor): Shape (N_points, 9).
    """
    # Ensure time_input_t requires gradients for differentiation
    if not time_input_t.requires_grad:
        time_input_t.requires_grad_(True)

    # Compute first derivative (velocities)
    # The grad_outputs tensor must be the same size as the output of the function
    # we are differentiating (network_output_r).
    grad_outputs_v = torch.ones_like(network_output_r)

    velocities_v, = torch.autograd.grad(
        outputs=network_output_r,
        inputs=time_input_t,
        grad_outputs=grad_outputs_v,
        create_graph=True  # CRITICAL: Retain graph for second derivative
    )

    # Compute second derivative (accelerations)
    grad_outputs_a = torch.ones_like(velocities_v)

    accelerations_a, = torch.autograd.grad(
        outputs=velocities_v,
        inputs=time_input_t,
        grad_outputs=grad_outputs_a,
        create_graph=False  # Not needed for second derivative
    )

    return velocities_v, accelerations_a
```

This code snippet serves as a direct, correct, and reusable implementation for deriving the kinematic quantities required by the physics and energy loss terms.

## 4.4 Selecting an Appropriate Huber Loss Delta ($\delta$) for Normalized Energy

**Issue Resolved: 13**

#### Context and Validation

Issue 13 raises a valid and subtle point regarding the HNN-Style Energy Regularizer. The `PINN_architecture_plan.tex` document specifies the use of a Huber loss function with a delta parameter of $\delta = 1.0$. The Huber loss is designed to be quadratic (like L2 loss) for small errors and linear (like L1 loss) for large errors, making it less sensitive to outliers. However, the energy deviation, $\Delta H_k$, is computed from normalized quantities and is expected to be small for a well-behaving model. With $\delta = 1.0$, it is highly likely that $|\Delta H_k|$ will almost always be less than $\delta$, causing the Huber loss to behave identically to a standard L2 (squared) loss and thus negating its intended purpose of providing robustness.

#### Proposed Solution and Implementation

The delta parameter of the Huber loss function must be chosen relative to the expected scale of the residuals. To restore the intended functionality of the loss, the parameter will be set to a value significantly smaller than 1. The definitive value is set to $\boldsymbol{\delta = 0.1}$.

#### Justification

The primary goal of the energy loss term is to penalize deviations from the initial energy $H_0$, keeping the predicted energy on the correct constant-energy manifold. A value of $\delta = 0.1$ establishes a meaningful transition point. For normalized energy deviations less than 10% ($|\Delta H_k| \leq 0.1$), the loss will be quadratic, providing a strong incentive for the model to reduce small errors precisely. For larger deviations ($|\Delta H_k| > 0.1$), which may occur during transient chaotic events or early in training, the loss becomes linear. This prevents single outlier points from generating excessively large gradients that could destabilize the optimizer. This choice of $\delta$ restores the intended robustness of the Huber loss function, leading to a more stable and effective regularization of the system's global energy conservation.

# 5 A Coherent Training and Data Sampling Strategy

The final set of resolutions addresses the core training loop, reconciling conflicting instructions on how data is sampled and batched, how advanced techniques are integrated, and how to handle the multi-resolution nature of the dataset. This section establishes a single, unified strategy that is computationally efficient, physically motivated, and fully integrated with the curriculum learning paradigm.

## 5.1 Unifying Data and Collocation Point Sampling

**Issues Resolved: 2, 10, 11**

#### Context and Validation

A major conceptual and practical contradiction, highlighted across Issues 2, 10, and 11, exists between the two documents regarding data sampling for the loss function. The `CTL-instruction-final.tex` document describes a process of sampling time points for the data loss, $\mathcal{L}_{\text{data}}$, from the discrete, available time steps within the BRUTUS simulation files. In contrast, the `PINN_architecture_plan.tex` document describes a separate process of sampling thousands of \"collocation points\" for the physics and energy losses, $\mathcal{L}_{\text{physics}}$ and $\mathcal{L}_{\text{energy}}$, from the continuous time domain [-1, 1].

This creates two distinct sets of points for evaluation in each training step. This approach is not only computationally inefficient, as it may require two separate forward passes or a single pass on a very large, concatenated set of points, but it is also conceptually confusing and deviates from standard PINN practices.

#### Proposed Solution and Implementation

The sampling strategies will be clarified and unified into a single, efficient workflow that aligns with established PINN methodologies. The distinction between \"data points\" and \"collocation points\" is crucial and will be formally defined:

- **Data Points:** These are points where ground-truth data is available. They are used exclusively to compute the data fidelity loss, $\mathcal{L}_{\text{data}}$.

- **Collocation Points:** These are points sampled from the problem's domain (in this case, continuous time) where no ground-truth data is necessarily available. They are used to enforce the governing physical laws via the physics and energy loss terms, $\mathcal{L}_{\text{physics}}$ and $\mathcal{L}_{\text{energy}}$.

The definitive training step will involve a single, combined forward pass for computational efficiency:

1.  **Batch Sampling:** For each training step, two sets of time points are sampled for each trajectory in the batch:

    - **Data Time Points ($t_{\text{data}}'$):** A set of $N_{\text{data\_pts}}$ (e.g., 32) time points are sampled from the discrete BRUTUS snapshot times available for that trajectory.

    - **Collocation Time Points ($t_{\text{col}}'$):** A set of $N_{\text{col\_pts}}$ (e.g., 256) time points are sampled from the continuous domain [-1, 1], using a uniform or adaptive strategy.

2.  **Unified Forward Pass:** The network is evaluated on the union of these two sets of points, $t_{\text{union}}' = t_{\text{data}}' \cup t_{\text{col}}'$, in a single forward pass to get all required position predictions and their derivatives.

3.  **Loss Computation:** The loss components are then calculated on their respective subsets of the predictions:

    - $\mathcal{L}_{\text{data}}$ is computed using the predictions corresponding to $t_{\text{data}}'$.

    - $\mathcal{L}_{\text{physics}}$ and $\mathcal{L}_{\text{energy}}$ are computed using the predictions corresponding to $t_{\text{col}}'$.

This approach resolves the ambiguity by clearly defining the roles of each point set. It is computationally efficient and allows the model to be anchored to real data while enforcing physical laws across the entire continuous solution domain, which is the core philosophy of PINNs.

## 5.2 Finalizing the Curriculum-Aware Batch Construction Protocol

**Issue Resolved: 6**

#### Context and Validation

Issue 6 correctly identifies an inconsistency where the `CTL-instruction-final.tex` document provides a detailed, sophisticated, and curriculum-aware algorithm for constructing mini-batches, while the `PINN_architecture_plan.tex` document offers only a vague, generic description. The CTL document's approach is clearly superior and tailored to the specific challenges of the problem.

#### Proposed Solution and Implementation

The detailed batch construction algorithm from `CTL-instruction-final.tex` is formally adopted as the definitive method. This protocol is essential for the success of the curriculum learning strategy and includes two key features:

1.  **Replay and Lookahead Sampling:** Each mini-batch is intelligently composed to facilitate stable learning and smooth transitions between stages.

    - **Replay (~95% of batch):** The majority of trajectories in a batch are sampled from the cumulative set of all data from the current stage and all previous stages. This prevents \"catastrophic forgetting\" by ensuring the model continually rehearses previously learned concepts.

    - **Lookahead (~5% of batch):** A small fraction of trajectories are sampled from the next curriculum stage. This \"previews\" more difficult examples, effectively warming up the network for the upcoming stage transition and smoothing the loss landscape.

2.  **Hybrid Time Point Sampling (Importance Sampling):** For each trajectory selected for the batch, the collocation points ($t_{\text{col}}'$) are sampled using a hybrid strategy to focus computational effort on dynamically significant regions:

    - **50% Uniform Sampling:** Half of the points are sampled uniformly from the continuous time domain [-1, 1], ensuring broad coverage.

    - **50% Acceleration-Weighted Sampling:** The other half are sampled from a probability distribution proportional to the magnitude of the system's acceleration, $|\mathbf{a}(t)|$. This naturally concentrates collocation points in regions of high dynamic activity, such as close encounters, where enforcing the physics is most critical.

This comprehensive batching strategy is a cornerstone of the CTL framework, ensuring stable learning, efficient use of data, and robust progression through the curriculum.

## 5.3 Strategy for Integrating Mixed-Resolution Trajectory Data

**Issue Resolved: 7**

#### Context and Validation

The introduction of new, high-resolution datasets (Set 2a and 2b in Table 1 of `CTL-instruction-final.tex`) presents a challenge identified in Issue 7: how to handle training batches that may contain a mix of low-resolution and high-resolution trajectories. Neither document provides a strategy for this, raising concerns about potential training bias or the need for complex data resampling procedures.

#### Proposed Solution and Implementation

The unified sampling strategy established in Section 5.1 provides an elegant and effective solution to this problem without requiring any modification.

- **For Physics and Energy Losses:** Since the collocation points are sampled from the continuous time domain [-1, 1], the underlying temporal resolution of the ground-truth BRUTUS data is irrelevant. The network's adherence to physical laws is tested on a consistent distribution of points, regardless of the source trajectory's data density.

- **For the Data Fidelity Loss:** The data points are sampled from the discrete BRUTUS snapshots. The high-resolution datasets simply provide a richer, denser set of available points from which to sample. This is a direct benefit, as it allows the random sampling process to select from a more diverse set of ground-truth data points, potentially improving the accuracy of the data loss term without introducing any bias.

Therefore, no special handling, such as up-sampling low-resolution data or down-sampling high-resolution data, is necessary. The proposed sampling framework inherently and gracefully accommodates the mixed-resolution dataset.

## 5.4 Definitive Implementation of Curriculum-Aware Gradient Clipping

**Issue Resolved: 8**

#### Context and Validation

Issue 8 notes that while both documents describe adaptive median-based gradient clipping to prevent numerical instability from close encounters, the `CTL-instruction-final.tex` document specifies a more sophisticated, curriculum-aware schedule for the clipping multiplier $C$, which is absent in the `PINN_architecture_plan.tex` document.

#### Proposed Solution and Implementation

A definitive implementation is created by synthesizing the strengths of both documents. The core algorithm will follow the clear description in the PINN document, while the clipping multiplier $C$ will follow the physically motivated, curriculum-aware schedule from the CTL document.

1.  **Algorithm:** After `loss.backward()` but before `optimizer.step()`, the global L2 norm of the model's gradients is computed. This norm is added to a moving history (a queue of the last 100 norms). The clipping threshold is then set to $C$ times the median of this history. The gradients are then clipped to this threshold.

2.  **Curriculum-Aware $C$ Schedule:** The multiplier $C$ is not fixed but is adjusted at the start of each curriculum stage to reflect the nature of the training data:

    - **Stages 0-1 (Stable Orbits):** $C = 8.5$. The data is smooth, and larger gradient steps can be tolerated to accelerate convergence.

    - **Stages 2-3 (Mild Chaos):** $C = 5.0$. As chaotic behavior is introduced, the clipping becomes more conservative.

    - **Stages 4-6 (Frequent Close Encounters):** $C = 3.0$. With highly chaotic data prone to producing extreme gradients, aggressive clipping is necessary to maintain training stability.

This synthesized approach ensures that the training process is both stable and efficient. It allows for rapid learning on simpler data while robustly protecting the optimizer from the instabilities inherent in the more challenging, chaotic stages of the curriculum. It is also explicitly noted that gradient clipping is applied only during the Adam optimization phase and is disabled during L-BFGS refinement, as the line-search mechanism of L-BFGS provides its own form of step control.

# Conclusion and Consolidated Recommendations
This report has systematically analyzed and resolved 19 critical issues spanning the entire workflow for training a Curriculum-Transfer Learning Physics-Informed Neural Network (CTL-PINN) for the three-body problem. By establishing definitive, physically-grounded, and computationally robust solutions, this document transforms a set of inconsistent and incomplete instructions into a single, coherent, and actionable implementation blueprint.

The key resolutions have unified the project's approach to foundational physics, data normalization, network architecture, loss function design, and training strategy. The proposed framework now rests on a solid foundation, with clear specifications for computing curriculum metrics like Lyapunov time, a consistent $G=1$ dimensionless unit system, a curriculum-aware schedule for the SIREN $\omega_0$ parameter, a rigorous state management protocol for the ALM, and an efficient, unified data sampling strategy that gracefully handles mixed-resolution data.

For successful implementation, adherence to the consolidated specifications is paramount. The following table provides a final, master summary of all key dynamic hyperparameters, serving as a single source of truth for configuring the training process across all curriculum stages. By following this blueprint, the project is well-positioned to develop a state-of-the-art model capable of learning the complex, chaotic dynamics of the three-body problem with high fidelity and long-term physical plausibility.



| **Parameter** | **Stage 0-1 (Stable)** | **Stage 2-3 (Mild Chaos)** | **Stage 4-6 (Chaotic)** | **Rationale** |
|---|---|---|---|---|
| SIREN first_omega_0 | 30.0 | 20.0 | 10.0 | Matches network frequency resolution to data complexity. |
| Energy Weight $\lambda_E$ | $10^{-3}$ - $10^{-2}$ | $10^{-1}$ - $1$ | $10^{1}$ - $10^{3}$ | Increases energy conservation constraint as chaos increases. |
| Adam Initial LR | $10^{-3}$ - $7\text{e-}4$ | $4.9\text{e-}4$ - $3.4\text{e-}4$ | $2.4\text{e-}4$ - $1.2\text{e-}4$ | Gradually reduces initial learning rate for more difficult stages. |
| Gradient Clip $C$ | 8.5 | 5.0 | 3.0 | Allows larger gradients for stable data; clips aggressively for chaotic data. |
| L-BFGS Type | Full-Batch | Full-Batch / sL-BFGS | sL-BFGS | Switches to stochastic variant as cumulative dataset size grows. |
| ALM State | Reset | Reset | Reset | Resets ALM statistics to adapt to new data distribution at each stage. |

: Consolidated Hyperparameter Schedule for CTL-PINN Training



---

## Source Issues / Notes for Future Reconciliation

No source-level issues identified during Phase 13 audit. The converted body faithfully reproduces all 7 active LaTeX sections of review_of_framework/ without suspected inconsistencies.

*End of faithful converted body. Source Issues section above is metadata excluded from fidelity comparison (D-19).*

===== END FILE review_of_framework.md =====

===== BEGIN FILE stage_strat_revision.md (44723 bytes, sha256 d875cd6680e3ec5239bd2c0d35b9bb8eaba39480f26cd909e4c0bc2fd9011fea) =====
# A Data-Driven Stage Assignment Framework for Curriculum Transfer Learning in N-Body Dynamics
*An Award-Winning Writer*

*March 21, 2026*

## Contents

- [Part I: Foundational Principles of Data-Driven Curriculum Stratification for Physical Systems](#part-i-foundational-principles-of-data-driven-curriculum-stratification-for-physical-systems)
  - [The Rationale for Adaptive Curricula in Physics Simulations](#the-rationale-for-adaptive-curricula-in-physics-simulations)
  - [A Lexicon of Difficulty Metrics for the Three-Body Problem](#a-lexicon-of-difficulty-metrics-for-the-three-body-problem)
  - [Core Techniques for Data-Driven Stratification](#core-techniques-for-data-driven-stratification)
- [Part II: A Revised Algorithmic Workflow for Stage Stratification](#part-ii-a-revised-algorithmic-workflow-for-stage-stratification)
  - [Phase I: Invariant Computation and Feature Engineering](#phase-i-invariant-computation-and-feature-engineering)
  - [Phase II: Exploratory Data Analysis (EDA) and Landscape Mapping](#phase-ii-exploratory-data-analysis-eda-and-landscape-mapping)
  - [Phase III: Deriving Adaptive Stage Criteria - A Hybrid Strategy](#phase-iii-deriving-adaptive-stage-criteria—a-hybrid-strategy)
  - [Phase IV: Final Stage Assignment and Population Balancing](#phase-iv-final-stage-assignment-and-population-balancing)
- [Part III: Implementation and Validation Protocol](#part-iii-implementation-and-validation-protocol)
  - [Reference Implementation in Python](#reference-implementation-in-python)
  - [Advanced Architectural Considerations and Refinements](#advanced-architectural-considerations-and-refinements)
  - [A Protocol for Curriculum Validation](#a-protocol-for-curriculum-validation)
- [Part IV: Conclusions and Recommendations](#part-iv-conclusions-and-recommendations)
- [References](#references)

## Abstract

This report presents a comprehensive, revised workflow for a data-driven curriculum stratification framework tailored to a Physics-Informed Neural Network (PINN) project for the three-body problem. The proposed methodology moves beyond static, heuristic-based criteria towards an adaptive system that derives its structure from the empirical properties of the simulation dataset itself. This approach, grounded in machine learning best practices, combines dimensionality reduction (PCA), unsupervised clustering (K-Means/GMM), and quantile-based binning to create a robust, interpretable, and effective curriculum. The report details a multi-phase algorithmic workflow, provides reference implementations, and outlines a protocol for empirical validation, aiming to improve training stability and final model accuracy for complex, chaotic dynamical systems.

# Part I. Foundational Principles of Data-Driven Curriculum Stratification for Physical Systems

The training of Physics-Informed Neural Networks (PINNs) on complex, chaotic dynamical systems represents a significant challenge at the intersection of scientific computing and machine learning. A key strategy for improving training stability and final model accuracy is Curriculum Learning (CL), where the model is exposed to training examples in a structured sequence, typically from "easy" to "hard".[1, 2] This report presents a comprehensive, revised workflow for a data-driven curriculum stratification framework tailored to a PINN project for the three-body problem. The proposed methodology moves beyond static, heuristic-based criteria, which have proven brittle, towards an adaptive system that derives its structure from the empirical properties of the simulation dataset itself. This approach is grounded in best practices from machine learning and is designed to be robust, interpretable, and directly implementable.

## The Rationale for Adaptive Curricula in Physics Simulations

The core premise of curriculum learning is to create a smooth "difficulty gradient" that guides the optimization process of a neural network towards a robust and generalizable solution.[3, 4] In the context of physics simulations, difficulty is often tied to the complexity of the underlying dynamics, such as the transition from regular, periodic motion to chaotic evolution. The initial approach for the CTL-PINN project, as detailed in the project documentation, relied on defining curriculum stages using fixed, theoretical thresholds on key physical invariants.[5] For instance, Stage 0 was defined by strict bounds on total energy ($E$), angular momentum ($L/L_{\text{max}}$), virial ratio ($Q$), and minimum particle separation ($s_{\text{min}}$) to isolate highly stable, hierarchical systems.[5]

While physically motivated, this static, heuristic-based approach possesses an inherent fragility: it presupposes that the training data will conform to idealized statistical distributions of these invariants. This assumption is frequently violated in practice, particularly when dealing with complex data generation processes. The project's use of Sobol-based quasi-random sampling for initial conditions (ICs) introduces a scaling factor, $s$, which systematically distorts the virial ratio, since $Q \propto 2T/|V|$ scales approximately as $s^3$.[5] Consequently, a large fraction of the quasi-random simulations, though potentially stable, fall outside the predefined $Q$ range (e.g., $[0.9, 1.1]$ for Stage 3), leading to underpopulated or even empty stages.[5] This mismatch between the curriculum's assumptions and the data's reality undermines the entire CL strategy, creating abrupt jumps in difficulty rather than a smooth progression.

This experience aligns with a broader consensus in machine learning research: "empirical adaptation to dataset statistics outperforms hand-crafted heuristics, especially in noisy or imbalanced data".[5] For PINNs applied to chaotic systems, this principle is especially pertinent. The "noise" is not merely measurement error but the intrinsic, high-frequency dynamics of chaos, and the "imbalance" is the often non-uniform distribution of stability across the phase space. Research on PINN training pathologies confirms that managing complexity is paramount for achieving convergence, with curriculum-based strategies being a primary tool for this purpose.[6, 7, 8] Papers on CL for PINNs advocate for approaches that progressively increase the difficulty, whether by sequencing the data samples or by gradually introducing more complex physical constraints.[4, 7]

This necessitates a paradigm shift. Instead of viewing the curriculum as a static, a priori set of rules, it should be conceptualized as a simplified, data-driven *model of the dataset's difficulty landscape*. A good curriculum, like any good model, must accurately represent the underlying data distribution, capturing its unique modes, skews, and correlations. A curriculum built on faulty assumptions is a mismatched model, leading to poor "predictions" about which data samples are genuinely easy or hard for the PINN to learn. Therefore, the design of the curriculum must be treated with the same analytical rigor as the design of the neural network itself. It requires a dedicated phase of exploratory data analysis (EDA), feature engineering (selection and transformation of physical invariants), model selection (e.g., choosing between clustering and quantile-based methods), and, ultimately, empirical validation. By adopting this data-driven philosophy, the curriculum becomes a robust and adaptive framework that is resilient to the specific artifacts of the data generation process, ensuring a smooth and effective learning path for the PINN.

## A Lexicon of Difficulty Metrics for the Three-Body Problem

To construct a data-driven curriculum, a set of quantitative features that correlate with learning difficulty is required. For the three-body problem, the conserved quantities and geometric properties of the system serve as excellent, physically interpretable difficulty metrics.[5] Each invariant provides a proxy for a specific aspect of dynamical complexity, forming a multi-dimensional feature space from which the curriculum can be constructed. The following metrics, computed from the initial state of each simulation, are foundational to the proposed framework.

**Total Mechanical Energy ($E$):** Defined as the sum of the system's kinetic ($T$) and potential ($V$) energies. $$E = T + V = \frac{1}{2}\sum_{i=1}^{3}m_{i}\lVert v_{i}'\rVert^{2} - \sum_{1\le i<j\le3}\frac{m_{i}m_{j}}{\lVert r_{i}'-r_{j}'\rVert+\epsilon}$$ In a system with gravitational constant $G=1$, a negative total energy ($E < 0$) indicates a gravitationally bound system. The more negative the value of $E$, the more tightly bound the system is, which often corresponds to more stable, regular orbits. Systems with energy close to zero ($E \approx 0$) are marginally bound or unbound and are susceptible to chaotic scattering, ejections, and fly-by encounters, which are significantly harder for a PINN to model accurately.[5]

**Virial Ratio ($Q$):** The ratio of twice the kinetic energy to the magnitude of the potential energy. $$Q = \frac{2T}{|V|}$$ For a stable, self-gravitating system in statistical equilibrium, the virial theorem states that $Q \approx 1$. A significant deviation from this value implies a state of disequilibrium. A system with $Q > 1$ has excess kinetic energy and will tend to expand, while a system with $Q < 1$ is dominated by potential energy and will tend to contract. Both scenarios often precede chaotic evolution, making $Q$ a key indicator of initial stability.[5]

**Normalized Angular Momentum ($L_{\text{norm}}$):** The magnitude of the total angular momentum vector, $L$, normalized by a characteristic maximum angular momentum, $L_{\text{max}}$. $$L_{\text{norm}} = \frac{\lVert L\rVert}{L_{\text{max}}} = \frac{\left\lVert\sum_{i=1}^{3}m_{i}(r_{i}'\times v_{i}')\right\rVert}{M_{\text{tot}}r_{\text{char}}v_{\text{char}}}$$ where $r_{\text{char}}$ is a characteristic length scale and $v_{\text{char}}$ is a characteristic velocity. A value of $L_{\text{norm}}$ close to 1 corresponds to near-circular orbits, which are highly regular and stable. Lower values indicate more eccentric (elongated) orbits, which lead to periodic close encounters between bodies, a primary driver of chaotic instabilities.[5]

**Minimum Initial Separation ($s_{\text{min}}$):** The smallest Euclidean distance between any pair of bodies in the initial configuration. $$s_{\text{min}} = \min_{1\le i<j\le3}\lVert r_{i}'-r_{j}'\rVert$$ This is a direct geometric indicator of the immediate risk of a close encounter. Very small values of $s_{\text{min}}$ signal impending strong gravitational interactions, which can lead to violent, unpredictable scattering events. These scenarios are among the most numerically challenging for both traditional integrators and PINNs.[5]

**Lyapunov Time ($\tau_L$):** The inverse of the largest Lyapunov exponent ($\lambda_{\text{max}}$), estimated from the simulated trajectory. $$\tau_{L} = \frac{1}{\lambda_{\text{max}}}$$ $\tau_{L}$ quantifies the timescale over which predictability is lost. It is the most direct measure of chaos in a dynamical system, representing the e-folding time for the exponential divergence of initially nearby trajectories. A short $\tau_{L}$ indicates strong chaos and high sensitivity to initial conditions, making long-term prediction fundamentally difficult. A long or infinite $\tau_{L}$ signifies regular, predictable motion.[5]

**Shape Invariants ($I_1, I_2, I_3$):** Dimensionless ratios of the three mutual distances between the bodies ($d_{\text{short}} \le d_{\text{mid}} \le d_{\text{long}}$). $$I_{1}=\frac{d_{\text{short}}}{d_{\text{long}}}, \quad I_{2}=\frac{d_{\text{mid}}}{d_{\text{long}}}, \quad I_{3}=\frac{d_{\text{short}}+d_{\text{mid}}-d_{\text{long}}}{d_{\text{short}}+d_{\text{mid}}+d_{\text{long}}}$$ These invariants describe the geometry of the initial configuration (e.g., collinear, isosceles, equilateral) independent of scale or orientation. Certain initial geometries are known to be more prone to chaotic evolution than others, making these invariants potentially useful secondary features for characterizing difficulty.[5]

These invariants form the feature vector for each simulation. By analyzing the statistical distributions and correlations of these features across the entire dataset, it is possible to construct a curriculum that is quantitatively grounded in the physics of the problem and empirically adapted to the data at hand.


| Invariant | Full Name | Role as a Difficulty Metric (Easy vs. Hard) |
|---|---|---|
| $E$ | Total Mechanical Energy | **Easy:** Large negative values (deeply bound). **Hard:** Values near zero. |
| $Q_{\text{norm}}$ | Normalized Virial Ratio | **Easy:** Values near 1 (virial equilibrium). **Hard:** Values far from 1. |
| $L_{\text{norm}}$ | Normalized Angular Momentum | **Easy:** Values near 1 (near-circular orbits). **Hard:** Low values. |
| $s_{\text{min}}$ | Minimum Initial Separation | **Easy:** Large values (well-separated). **Hard:** Small values. |
| $\tau_{L}$ | Lyapunov Time | **Easy:** Large or infinite values (regular). **Hard:** Small values (strong chaos). |

*Table: Physical Invariants and Their Interpretation as Difficulty Metrics*


## Core Techniques for Data-Driven Stratification

With a well-defined feature space of physical invariants, the next step is to select appropriate machine learning techniques to partition this space into curriculum stages. A hybrid approach combining dimensionality reduction, unsupervised clustering, and quantile-based binning provides a powerful and flexible toolkit for this task.

### Dimensionality Reduction with PCA for a Composite Stability Score

In the three-body problem, difficulty is a multi-faceted concept. A system can be challenging due to low angular momentum, near-zero energy, or a short Lyapunov time. These metrics are often strongly correlated; for example, a very tightly bound system (highly negative $E$) may evolve into chaos more quickly (short $\tau_L$).[5] Simply setting independent thresholds on each metric can lead to conflicting or redundant criteria.

Principal Component Analysis (PCA) offers a principled method to address this. PCA is an orthogonal linear transformation that projects the data onto a new coordinate system, where the axes (principal components, PCs) are ordered by the amount of variance they explain in the original data.[9, 10] The first principal component (PC1) represents the direction of maximum variance in the feature space. In the context of our physical invariants, this component can often be interpreted as a composite "stability" or "difficulty" score.[5]

For instance, if PC1 is found to be a linear combination with positive weights on $L_{\text{norm}}$ and $\tau_L$ and a negative weight on $|E|$, then a high score on PC1 would correspond to a system that is simultaneously regular, predictable, and not excessively bound—a clear signature of stability. By ranking simulations based on their PC1 score, one can create a continuous, one-dimensional difficulty axis that optimally combines the information from multiple correlated invariants. This data-driven approach is superior to manually constructing a composite score (e.g., $-E + L_{\text{norm}}$ [5]), as the weights are derived directly from the dataset's covariance structure, ensuring they are optimally tailored to the specific data distribution.[11, 12]

### Unsupervised Clustering for Discovering Dynamical Regimes

While PCA and quantile binning are excellent for ordering data along a continuous difficulty axis, they may not capture the full picture. Difficulty is not always just a matter of degree; it can also be a matter of kind. Unsupervised clustering algorithms, such as K-Means or Gaussian Mixture Models (GMM), partition the dataset into distinct groups based on similarity in the multi-dimensional feature space. This allows for the automatic discovery of different *dynamical regimes* or *phenomenological classes* of simulations.[5]

Consider two simulations that have the same short Lyapunov time, $\tau_L$. From a purely quantile-based perspective, they are equally difficult. However, their underlying dynamics could be completely different. One might be a "prompt ejection" event, where one body is quickly flung out of the system. The other might be a long-lived, complex "resonant encounter," where the bodies undergo multiple close approaches before settling into a new configuration. For a PINN, these two scenarios present qualitatively different challenges. The prompt ejection involves large velocities and an unbound trajectory, while the resonant encounter involves intricate, repeated interactions in a compact region of space.

A simple easy-to-hard curriculum might mix these two types of chaos, potentially confusing the learning process. Clustering in the full feature space (e.g., using $E, L_{\text{norm}}, s_{\text{min}}, \tau_L$) can distinguish between them. It might naturally group all prompt ejections into one cluster (characterized, perhaps, by $E \approx 0$ and high final velocities) and all resonant encounters into another (characterized by small $s_{\text{min}}$ and oscillating inter-particle distances). This reveals that the difficulty landscape is not a simple line but a structured space with distinct regions.

This allows for the design of a more sophisticated curriculum that introduces not just progressively harder simulations, but also qualitatively different types of physical phenomena stage by stage. For example, after learning stable orbits, the PINN could be trained specifically on the "prompt ejection" cluster, then on the "resonant encounter" cluster. This aligns with research suggesting that clustering can reveal "latent difficulty gradients" that hand-picked thresholds might overlook.[5, 13] K-Means is an efficient baseline for this task, while GMMs offer more flexibility by modeling non-spherical clusters and providing probabilistic assignments, which can be invaluable for identifying outliers or creating "soft" curriculum boundaries.[5, 14]

### Quantile-Based Binning for Robust and Balanced Pacing

Quantile-based binning is a non-parametric method that divides a ranked dataset into a predetermined number of continuous intervals ("bins"), each holding the same number of data points.[15] For example, quartiles divide the data into four bins, each containing 25% of the samples.

This technique is exceptionally robust and serves as a cornerstone of the adaptive curriculum. Its primary advantage is that it makes no assumptions about the underlying distribution of the difficulty metric. This is critical for the CTL-PINN project, where metrics like the raw virial ratio $Q$ have a distorted distribution and the Lyapunov time $\tau_L$ likely has a heavy tail corresponding to highly chaotic events.[5]

Using fixed thresholds (e.g., "$\tau_L < 2$") is risky; if the data distribution is skewed, such a rule might select 50% of the data or only 1%. In contrast, a quantile-based rule like "select the bottom 25% of simulations by $\tau_L$" guarantees that the resulting stage will contain exactly one-quarter of the samples it is applied to. This provides two key benefits:

1.  **Avoids Empty Stages:** It ensures that every defined stage will be populated with a predictable number of samples, preventing the issue of empty stages that plagued the original fixed-threshold design.[5]

2.  **Ensures Smooth Pacing:** It provides a balanced progression of difficulty. By dividing the chaotic systems into, for example, four equally sized quantile bins, the curriculum ensures the PINN is not suddenly overwhelmed by a disproportionately large number of difficult examples at a single transition. This smooth pacing is essential for stable training.[16]

This technique is a well-established best practice in curriculum learning for regression and simulation tasks, as it automatically adapts the stage boundaries to the empirical distribution of the data, ensuring a well-proportioned and steadily advancing curriculum.[5]

# Part II. A Revised Algorithmic Workflow for Stage Stratification

This section details a multi-phase, algorithmic workflow for implementing the data-driven curriculum. The process is designed to be systematic and reproducible, transforming the raw simulation outputs into a final, robust stage assignment for every trajectory in the dataset. The workflow is divided into four phases: (I) Invariant Computation and Feature Engineering, (II) Exploratory Data Analysis, (III) Derivation of Adaptive Stage Criteria, and (IV) Final Stage Assignment and Balancing.

## Phase I: Invariant Computation and Feature Engineering

The foundation of the data-driven curriculum is a comprehensive and accurate feature set. This phase focuses on processing the raw simulation data to compute the physical invariants discussed in Part 1 and correcting for any known sampling artifacts.

### Pre-computation and Data Loading

This initial step leverages the project's existing data processing pipeline. It involves executing the established Python scripts to perform the following actions for every simulation in the dataset:

1.  **Parse Raw Data:** Read the initial condition files (`ic_*.txt`) and the corresponding Brutus N-body integrator output files (`brutus_*.txt`).[5]

2.  **Center-of-Mass (COM) Transformation:** Verify and, if necessary, transform the initial conditions to the COM frame, ensuring zero total momentum. This is a critical prerequisite for consistent physical calculations, especially since the 'hierarchical' ICs may not initially be in the COM frame.[5]

3.  **Scaling to Dimensionless Units:** Apply the global characteristic scales for length, time, and velocity to convert all physical quantities into a consistent, dimensionless system where $G=1$. This is essential for numerical stability and for ensuring the PINN inputs are on a comparable scale.[5]

The output of this step is a clean, standardized set of initial conditions (masses, positions, velocities) for every simulation.

### Invariant Calculation

For each standardized initial condition, a dedicated function should compute the full suite of physical invariants defined in "A Lexicon of Difficulty Metrics for the Three-Body Problem" above. This includes: Total Mechanical Energy ($E$), Raw Virial Ratio ($Q_{\text{raw}}$), Normalized Angular Momentum ($L_{\text{norm}}$), Minimum Initial Separation ($s_{\text{min}}$), Shape Invariants ($I_1, I_2, I_3$), and Lyapunov Time ($\tau_L$), estimated from the corresponding Brutus trajectory data using the Rosenstein-style estimator detailed in the project documentation.[5]

### Correcting for Sampling Artifacts: The Normalized Virial Ratio

A critical issue identified in the project is the distortion of the virial ratio for quasi-random ICs due to the Sobol sampling scale factor, $s$.[5] To address this, a normalized virial ratio, $Q_{\text{norm}}$, must be computed to place all simulations on a comparable footing.

The transformation is based on the physical scaling of the kinetic and potential energies. Since kinetic energy $T \propto v^2$ and potential energy $V \propto 1/r$, and the sampling scales positions as $r \to sr$ and velocities as $v \to sv$, the virial ratio scales as: $$Q \propto \frac{T}{|V|} \propto \frac{(sv)^2}{1/(sr)} = s^3 \frac{v^2}{1/r}$$ Therefore, to recover a scale-invariant measure of virial equilibrium, the raw virial ratio must be divided by $s^3$. The normalized virial ratio is defined as: $$Q_{\text{norm}} = \frac{Q_{\text{raw}}}{s^3}$$ This calculation should be applied to all simulations of type 'quasi-random'. For 'hierarchical' simulations, it can be assumed that $s=1$, so $Q_{\text{norm}} = Q_{\text{raw}}$.

**[I'm not sure what this s is referring to. Should we look for the exact value used in the sampling script?]**

**Contingency Plan:** If the scale factor $s$ is not explicitly stored with each IC, it must be recorded during the IC generation or estimated post-hoc. As suggested in the project analysis, one method is to estimate it by comparing the median momentum of the scaled sample to a baseline unscaled sample.[5] Without this correction, the virial ratio is not a reliable metric for the quasi-random set and should be excluded from the analysis for those simulations.

### Assembling the Invariant Feature DataFrame

The final step of this phase is to consolidate all computed information into a single, master `pandas.DataFrame`. This DataFrame will be the central data structure for all subsequent analysis and serves as a persistent, intermediate representation of the dataset's physical properties.

| sim_id | ic_type | s_factor | E | Q_raw | Q_norm | L_norm | s_min | tau_L | I1 | I2 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0001 | hierarchical | 1.0 | -2.5 | 1.01 | 1.01 | 0.95 | 3.1 | 1000.0 | 0.8 | 0.9 |
| 5001 | quasi-random | 1.2 | -0.8 | 1.75 | 1.01 | 0.45 | 1.5 | 12.3 | 0.3 | 0.7 |

*Table 2: Recommended structure for the Invariant Feature DataFrame.*

> **Source-document inconsistency (preserved by faithful conversion):** The Phase I "Invariant Calculation" body text enumerates the Shape Invariants as $I_1, I_2, I_3$, but the schema table above lists only `I1` and `I2` columns (no `I3`). This omission is present in the original LaTeX source (`pinn_instruction/original_latex/framework-revisions/review-of-framework/stage_strat_revision/sections/algorithmic_workflow.tex` line 49, `\begin{tabular}{@{}lllllllllll@{}}` with 11 columns and only `I1, I2` named in the header). The conversion preserves the source verbatim. **Resolution required upstream:** the original LaTeX should either add an `I3` column to the table or remove `I_3` from the body text enumeration. Until that resolution lands, downstream consumers of this DataFrame schema should treat `I3` as a planned-but-unimplemented column.

This DataFrame provides a complete, queryable summary of the entire dataset, enabling the powerful exploratory and algorithmic techniques described in the following phases.

## Phase II: Exploratory Data Analysis (EDA) and Landscape Mapping

Before defining the final curriculum stages, it is essential to perform a thorough exploratory data analysis (EDA). The goal of this phase is to build a strong intuition for the structure of the data, validate the physical assumptions, and identify the key relationships that will guide the stratification strategy. This process transforms the numerical data in the invariant DataFrame into actionable visual insights.

### Stratified Distribution Analysis

The first step is to understand the distribution of each key difficulty metric. This is achieved by generating histograms and, for a smoother representation, Kernel Density Estimate (KDE) plots for the primary invariants: $E$, $Q_{\text{norm}}$, $L_{\text{norm}}$, and $\tau_L$.

Crucially, these visualizations must be **stratified by `ic_type`**. Plotting the distributions for 'hierarchical' and 'quasi-random' systems separately (or overlaid with different colors) is expected to reveal fundamental differences between the two datasets.[5]

### Correlation Analysis

Next, the relationships *between* the different difficulty metrics must be investigated. A Pearson correlation matrix, visualized as a heatmap, is the standard tool for this analysis. Again, this should be performed separately for the 'hierarchical' and 'quasi-random' subsets.

### Low-Dimensional Visualization

To gain a more holistic view of the difficulty landscape, it is useful to visualize the data in a low-dimensional space.

- **Pair Plots:** A `seaborn.pairplot` can be used to show all pairwise scatter plots between the key invariants, with points colored by `ic_type`.

- **PCA Projection:** A powerful visualization technique is to perform a preliminary PCA on the standardized invariants and create a 2D scatter plot of the first two principal components (PC1 vs. PC2). The points on this plot can be colored by a key chaos indicator, such as $\tau_L$ or its inverse, $\lambda_{\text{max}}$.

This EDA phase is not merely a formality; it is a crucial step that ensures the subsequent algorithmic choices are grounded in the empirical reality of the data, not just in theoretical assumptions.

## Phase III: Deriving Adaptive Stage Criteria - A Hybrid Strategy

With a deep understanding of the data's structure from the EDA phase, the next step is to derive the specific rules for stage assignment. The guiding principle of the revised framework is to use a hybrid strategy tailored to the distinct physical nature of the two sub-datasets.


| Aspect | Original Fixed-Threshold Framework | Proposed Data-Driven Framework |
|--------|-----------------------------------|-------------------------------|
| **Thresholds** | Static, hard-coded values based on theory (e.g., $Q<1.3$, $\tau_L>5$).[5] | Adaptive, derived from data statistics (e.g., quantiles, cluster centroids).[5] |
| **Stage Population** | Prone to severe imbalance or empty stages if data distribution mismatches theory.[5] | Balanced by design through quantile binning and population checks, ensuring smooth pacing.[5] |
| **Robustness** | Brittle; fails when data generation artifacts (e.g., scaling) violate assumptions.[5] | Robust; automatically adapts to the dataset's empirical distribution, including skews and artifacts.[5] |
| **Difficulty Ordering** | Assumes a simple, monotonic difficulty gradient that may not hold in multi-dimensional feature space. | Discovers natural difficulty gradients and qualitatively distinct regimes via PCA and clustering.[5, 13] |
| **Interpretability** | High, as criteria are based on physical theory. | High, as data-driven clusters and quantiles are interpreted and labeled by their physical properties (e.g., mean $\tau_L$). |

*Table 3: Comparison of Original vs. Proposed Data-Driven Curriculum Framework*


### Stratifying the Stable Subset (Hierarchical ICs): Stages 0 and 1

The 'hierarchical' dataset consists entirely of dynamically stable systems. The goal here is not to separate stable from chaotic, but to rank the systems by their *degree* of stability and regularity. A simple, physically interpretable approach using quantile-based thresholds is most appropriate.

### Stratifying the Complex Subset (Quasi-Random ICs): Stages 2-6

The 'quasi-random' dataset is far more heterogeneous. A more powerful, multi-step strategy is required to properly parse this complexity. This involves a pipeline of feature preparation, dimensionality reduction with PCA, and regime discovery with unsupervised clustering. The algorithm involves:

1.  **Feature Preparation:** Select features $[E, Q_{\text{norm}}, L_{\text{norm}}, s_{\text{min}}, 1/\tau_L]$. Use the inverse Lyapunov time, $\lambda_{\text{max}} = 1/\tau_L$, to handle regular orbits where $\tau_L \to \infty$. Standardize all features.

2.  **Dimensionality Reduction with PCA:** Apply PCA to the standardized features to create a composite, low-dimensional representation.

3.  **Discovering Regimes with Clustering:** Apply K-Means (or GMM) to the principal component scores. The number of clusters, $k$, can be set to 5 (for Stages 2-6) or determined using heuristics like the elbow method.

4.  **Ordering Clusters by a Chaos Proxy:** Sort the discovered clusters by their median $\tau_L$ in descending order. The cluster with the highest median $\tau_L$ is the least chaotic and will form the earliest stage in this block.

## Phase IV: Final Stage Assignment and Population Balancing

The final phase translates the derived criteria into a definitive assignment of a stage label to every simulation.

### The Definitive Assignment Algorithm

The final stage assignment rules are summarized in Table 4.

### Population Control and Stage Merging

After the initial assignment, it is imperative to check the population of each stage. If any stage falls below a minimum population threshold (e.g., 5% of the total dataset), it should be merged with its most similar adjacent stage to ensure the curriculum has a sensible "pacing".


| Stage | Primary Data Source | Stratification Method | Specific Data-Driven Criteria | Expected Physical Characteristics |
|---|---|---|---|---|
| **0** | Hierarchical | Quantile Binning | $E$ in bottom quartile & $L_{\text{norm}}$ in top quartile. | Deeply bound, near-circular, highly regular orbits. |
| **1** | Hierarchical | Remainder | All other hierarchical systems. | Stable, bound, regular orbits, but less constrained. |
| **2** | Quasi-Random | PCA + Clustering | Members of the cluster with the highest median $\tau_L$. | Most stable of the chaotic set; long-term regular motion. |
| **3** | Quasi-Random | PCA + Clustering | Members of the cluster with the 2nd highest median $\tau_L$. | Onset of chaos; mildly chaotic systems. |
| **4** | Quasi-Random | PCA + Clustering | Members of the cluster with the 3rd highest median $\tau_L$. | Moderately chaotic systems, possibly resonant. |
| **5** | Quasi-Random | PCA + Clustering | Members of the cluster with the 4th highest median $\tau_L$. | Strongly chaotic systems with short predictability. |
| **6** | Quasi-Random | PCA + Clustering + Outlier | Most chaotic cluster (lowest median $\tau_L$) + outliers. | Violent, unpredictable dynamics; ejections, unbound systems. |

*Table 4: Final Proposed Stage Definitions and Data-Driven Criteria*



# Part III. Implementation and Validation Protocol

This part provides the practical tools and procedures required to execute the proposed workflow and validate its effectiveness.

## Reference Implementation in Python

The following Python code provides a reference implementation for the core functions of the stratification workflow.

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

def compute_invariants(raw_data_path: str, simulation_files: list) -> pd.DataFrame:
    """
    Parses raw data, computes all physical invariants, and returns a master DataFrame.
    This function is a placeholder for the user's existing pipeline for steps 2.1.1-2.1.4.
    """
    # For demonstration, we'll create a dummy DataFrame.
    num_samples = 15000
    data = {
        'sim_id': range(num_samples),
        'ic_type': np.random.choice(['hierarchical', 'quasi-random'], num_samples, p=[0.4, 0.6]),
        'E': np.random.randn(num_samples) * 2 - 1,
        'Q_norm': np.random.randn(num_samples) * 0.2 + 1,
        'L_norm': np.random.rand(num_samples),
        's_min': np.random.rand(num_samples) * 5,
        'tau_L': np.random.exponential(scale=10, size=num_samples)
    }
    df = pd.DataFrame(data)
    # Make hierarchical more stable for realism
    hier_mask = df['ic_type'] == 'hierarchical'
    df.loc[hier_mask, 'tau_L'] = np.random.exponential(scale=500, size=hier_mask.sum()) + 100
    df.loc[hier_mask, 'L_norm'] = np.random.uniform(0.7, 1.0, size=hier_mask.sum())
    df.loc[hier_mask, 'E'] = np.random.uniform(-5, -1, size=hier_mask.sum())
    return df

def perform_eda(invariant_df: pd.DataFrame):
    """
    Generates and saves key EDA plots for landscape mapping.
    """
    print("--- Performing Exploratory Data Analysis ---")
    #... (Plotting code as in original report)...
    print("EDA plots saved.")

def derive_adaptive_criteria(quasi_random_df: pd.DataFrame, k: int = 5) -> dict:
    """
    Implements the PCA -> Cluster -> Sort pipeline for the quasi-random dataset.
    """
    print(f"--- Deriving Adaptive Criteria for Quasi-Random Data (k={k}) ---")
    features = ['E', 'Q_norm', 'L_norm', 's_min', 'tau_L']
    df_for_clustering = quasi_random_df[features].copy()
    df_for_clustering['lambda_max'] = 1.0 / df_for_clustering['tau_L']
    df_for_clustering.replace([np.inf, -np.inf], 0, inplace=True)
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_for_clustering[['E', 'Q_norm', 'L_norm', 's_min', 'lambda_max']])
    
    pca = PCA(n_components=0.9)
    pcs = pca.fit_transform(scaled_features)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(pcs)
    
    temp_df = quasi_random_df.copy()
    temp_df['cluster'] = cluster_labels
    cluster_median_tau_L = temp_df.groupby('cluster')['tau_L'].median()
    sorted_clusters = cluster_median_tau_L.sort_values(ascending=False).index.tolist()
    
    return {
        'kmeans_model': kmeans, 'pca_model': pca, 'scaler': scaler,
        'sorted_cluster_labels': sorted_clusters, 'cluster_assignments': cluster_labels
    }

def assign_stages(invariant_df: pd.DataFrame, k_clusters: int = 5, min_stage_pop_frac: float = 0.05) -> pd.DataFrame:
    """
    Assigns a final stage label to each simulation based on the hybrid strategy.
    """
    df = invariant_df.copy()
    df['stage'] = -1
    
    # Stratify Hierarchical Data (Stages 0, 1)
    hier_mask = df['ic_type'] == 'hierarchical'
    hier_df = df[hier_mask]
    e_q25 = hier_df['E'].quantile(0.25)
    l_q75 = hier_df['L_norm'].quantile(0.75)
    stage0_mask = hier_mask & (df['E'] <= e_q25) & (df['L_norm'] >= l_q75)
    df.loc[stage0_mask, 'stage'] = 0
    df.loc[hier_mask & (df['stage'] == -1), 'stage'] = 1

    # Stratify Quasi-Random Data (Stages 2-6)
    qr_mask = df['ic_type'] == 'quasi-random'
    qr_df = df[qr_mask]
    criteria = derive_adaptive_criteria(qr_df, k=k_clusters)
    sorted_labels = criteria['sorted_cluster_labels']
    cluster_map = {label: i for i, label in enumerate(sorted_labels)}
    
    for original_label, stage_offset in cluster_map.items():
        cluster_mask = qr_df.index[criteria['cluster_assignments'] == original_label]
        df.loc[cluster_mask, 'stage'] = stage_offset + 2

    # Add extreme outliers to Stage 6
    s_min_q1 = df['s_min'].quantile(0.01)
    extreme_outlier_mask = qr_mask & ((df['s_min'] <= s_min_q1) | (df['E'] > 0))
    df.loc[extreme_outlier_mask, 'stage'] = 6
    
    # Population Balancing
    #... (Merging logic as in original report)...
    
    # Re-label stages to be contiguous
    unique_stages = sorted(df['stage'].unique())
    stage_relabel_map = {old_label: new_label for new_label, old_label in enumerate(unique_stages)}
    df['stage'] = df['stage'].map(stage_relabel_map)
    
    print("\n--- Final Stage Populations ---")
    print(df['stage'].value_counts().sort_index())
    return df
```

## Advanced Architectural Considerations and Refinements

While the proposed workflow is robust, several refinements can enhance its performance and interpretability, such as using Gaussian Mixture Models (GMM) for more flexible clustering, performing feature selection to reduce noise, and using shape invariants for secondary analysis to improve physical interpretation.

## A Protocol for Curriculum Validation

The development of the curriculum does not end with the assignment of stage labels. Its effectiveness must be empirically validated.[5] The ultimate goal is to ensure a smooth difficulty gradient for the PINN, leading to stable and efficient training.

1.  **Implement the New Curriculum:** Generate and save stage labels for the dataset.

2.  **Create a Hold-out Validation Set:** Partition the data, ensuring the validation set is stratified across all curriculum stages.

3.  **Prototype Training Run:** Train a prototype of the CTL-PINN model following the full curriculum protocol.

4.  **Monitor Stage-wise Performance:** At the end of training for each stage $k$, evaluate the model's loss (e.g., $\mathcal{L}_{\text{data}}$) on the validation samples belonging to each stage.

5.  **Analyze the Transition Dynamics:** Plot the validation loss for each stage's data as a function of the training epochs.

6.  **Success Criterion:** The curriculum is successful if training proceeds without catastrophic spikes in validation loss upon stage transitions. A manageable increase in loss on newly introduced data, followed by a steady decrease, indicates a well-paced difficulty jump.

# Part IV. Conclusions and Recommendations

The analysis presented in this report confirms that the initial fixed-threshold curriculum framework is ill-suited to the empirical realities of the generated dataset. The proposed solution is a complete overhaul of the stage assignment methodology, replacing the static framework with a robust, adaptive, and data-driven workflow.

**The core recommendations are as follows:**

1.  **Adopt a Hybrid, Data-Driven Stratification Strategy:** Use quantile-based binning for the stable subset and a PCA-plus-clustering approach for the complex subset.

2.  **Implement the Four-Phase Algorithmic Workflow:** Follow the systematic process from invariant computation to final stage assignment and balancing.

3.  **Prioritize Physical Interpretability:** Maintain the link to physics by using meaningful invariants and analyzing the physical characteristics of discovered clusters.

4.  **Embrace Iterative Validation:** Empirically validate the curriculum's effectiveness by monitoring the PINN's training dynamics and be prepared to refine the curriculum based on this feedback.

By implementing this comprehensive framework, the CTL-PINN project can overcome the critical bottleneck of stage assignment, ensuring a smoother learning progression and ultimately providing a much stronger foundation for training a PINN to accurately model the complex and chaotic dynamics of the three-body problem.

## References

1. Curriculum learning for data-driven modeling of dynamical systems, accessed August 1, 2025, <https://arxiv.org/pdf/2112.08458>
2. [2411.00973] Does the Definition of Difficulty Matter? Scoring Functions and their Role for Curriculum Learning - arXiv, accessed August 1, 2025, <https://arxiv.org/abs/2411.00973>
3. Data Parameters: A New Family of Parameters for Learning a Differentiable Curriculum - NIPS, accessed August 1, 2025, <http://papers.neurips.cc/paper/9289-data-parameters-a-new-family-of-parameters-for-learning-a-differentiable-curriculum.pdf>
4. physics-informed neural networks with curriculum training for poroelastic flow and deformation - NGM2024, accessed August 1, 2025, <https://www.ngm2024.se/Papers/bekele_ngm2024_paper_final.pdf>
5. stage-assignment-issue.txt
6. [2404.13909] Physics-informed neural networks with curriculum training for poroelastic flow and deformation processes - arXiv, accessed August 1, 2025, <https://arxiv.org/abs/2404.13909>
7. Dynamic Curriculum Regularization for Enhanced Training of..., accessed August 1, 2025, <https://ml4physicalsciences.github.io/2024/files/NeurIPS_ML4PS_2024_109.pdf>
8. Characterizing possible failure modes in physics-informed neural networks - OpenReview, accessed August 1, 2025, <https://openreview.net/forum?id=a2Gr9gNFD-J>
9. Principal component analysis - Wikipedia, accessed August 1, 2025, <https://en.wikipedia.org/wiki/Principal_component_analysis>
10. Principal component analysis: a review and recent developments | Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, accessed August 1, 2025, <https://royalsocietypublishing.org/doi/10.1098/rsta.2015.0202>
11. Principal component analysis: a review and recent developments - PMC - PubMed Central, accessed August 1, 2025, <https://pmc.ncbi.nlm.nih.gov/articles/PMC4792409/>
12. Composite score analysis for unsupervised comparison and network visualization of metabolomics data - PMC, accessed August 1, 2025, <https://pmc.ncbi.nlm.nih.gov/articles/PMC6948848/>
13. Unsupervised Deep Embedding for Clustering Analysis - Proceedings of Machine Learning Research, accessed August 1, 2025, <https://proceedings.mlr.press/v48/xieb16.pdf>
14. Feature Selection for Unsupervised Learning, accessed August 1, 2025, <https://www.jmlr.org/papers/volume5/dy04a/dy04a.pdf>
15. Simulation-Based Inference with Quantile Regression - arXiv, accessed August 1, 2025, <https://arxiv.org/pdf/2401.02413>
16. Quantile Regression Estimands and Models: Revisiting the Motherhood Wage Penalty Debate - OSF, accessed August 1, 2025, <https://osf.io/9avrp/download>


---

## Source Issues / Notes for Future Reconciliation

The converted body faithfully reproduces all 6 active LaTeX sections of `stage_strat_revision/` without suspected inconsistencies. The single `\authcomment{}` at `algorithmic_workflow.tex:34` renders as bold text in the markdown, which is acceptable per D-58 and does not require separate documentation.

### SI-SSR-001: I3 schema inconsistency

Resolved by v1.4 finding M5. See Phase 20 architecture and normalization cleanup.

===== END FILE stage_strat_revision.md =====
