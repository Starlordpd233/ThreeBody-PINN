**Optimization of Data Validation Protocols for Causal Physics-Informed Learning in Chaotic N-Body Regimes**

**Research Report**

*April 27, 2026*

---

# 1 Introduction: The Intersection of Arbitrary-Precision Numerics and Causal Deep Learning

The integration of high-fidelity numerical analysis with deep learning represents a paradigm shift in the study of chaotic dynamical systems. The specific research stack under analysis---comprising the Brutus arbitrary-precision integrator written in C++, a Python-based data processing pipeline, and a Causal Training Labeled Physics-Informed Neural Network (CTL-PINN)---targets one of the most enduring challenges in classical mechanics: the Three-Body Problem. This system is characterized by non-linear interactions, extreme sensitivity to initial conditions, and phase space structures defined by the coexistence of stable invariant tori and chaotic seas. The successful modeling of such a system using neural networks requires a rigorous reassessment of what constitutes "high-quality" training data. Unlike traditional supervised learning tasks where data quality is often synonymous with label accuracy or noise reduction, the chaotic N-body problem imposes strict geometric and dynamical constraints---specifically symplectic conservation and phase space continuity---that must be preserved to ensure the learned model is physically viable.

The primary objective of this report is to define a comprehensive strategy for assessing training data quality prior to full model training. The analysis is driven by the unique requirements of the CTL-PINN architecture, which enforces temporal causality in the learning process, thereby making the model highly sensitive to the temporal coherence and physical consistency of the input data. We evaluate the comparative efficacy of static pre-training validation versus dynamic trial training, ultimately proposing a hybrid "Staged Gate" protocol. Furthermore, we develop a set of mathematically grounded metrics tailored to the arbitrary-precision nature of the Brutus dataset, ensuring that the inductive biases of the neural network align with the symplectic geometry of the underlying Hamiltonian physics.

## 1.1 The Computational Landscape: Brutus and the Bulirsch-Stoer Algorithm

To understand the data quality requirements, one must first analyze the source of the data. The Brutus code differs fundamentally from the symplectic integrators (such as Leapfrog or Wisdom-Holman) typically used in large-scale N-body simulations. Symplectic integrators preserve the geometric properties of the Hamiltonian flow (such as phase space volume) over long time scales but do so at the cost of local accuracy, often introducing a bounded energy error that oscillates but does not grow secularly. In contrast, Brutus utilizes the Bulirsch-Stoer algorithm combined with arbitrary-precision arithmetic to generate "converged" solutions.

The Bulirsch-Stoer method is an extrapolation scheme. It computes the solution at a future time $t + H$ by subdividing the interval $H$ into substeps, performing the integration with a modified midpoint method, and then extrapolating the results to zero step size using rational functions. Brutus iteratively increases the precision (word length $L$) and decreases the tolerance parameter $\epsilon$ until the solution converges to a specified number of significant digits. This implies that a Brutus-generated trajectory is not merely an approximation; within the specified precision, it is a "true" numerical solution that shadows the exact mathematical trajectory of the system.

However, this high fidelity comes with a specific data characteristic: non-uniform temporal sampling. The adaptive step-size controller in Brutus shrinks the time step $\Delta t$ dramatically during close encounters (pericenter passages) to maintain accuracy as the gravitational forces $F \propto 1/r^2$ diverge. Conversely, during excursive phases where bodies are widely separated, $\Delta t$ increases. While this is efficient for integration, it presents a "spectral bias" challenge for neural networks, which typically assume uniform sampling or at least sampling densities that correlate with the local Lipschitz constant of the target function in a way that is compatible with gradient descent dynamics. Consequently, "good" data for Brutus---defined by convergence---is not necessarily "good" data for a CTL-PINN without rigorous validation of its sampling density and local stiffness properties.

## 1.2 The Learning Architecture: Causal Training Labeled PINN (CTL-PINN)

The target model is a CTL-PINN. This architecture represents a refinement of the standard PINN formulation designed specifically for time-dependent evolution equations. Standard PINNs often suffer from "temporal causality violation," where the optimizer attempts to minimize the residual at a late time $t=T$ before having adequately resolved the solution at $t=0$. In chaotic systems, this is catastrophic because the solution at $t=T$ is exponentially sensitive to the trajectory at $t < T$. If the early trajectory is not learned correctly, the physics loss at later times provides incorrect gradient information, leading to convergence to unphysical local minima.

Causal training addresses this by introducing a weighting mechanism $w(t)$ into the loss function: $$\mathcal{L}(\theta) = \sum_{i=1}^{N_t} w_i \mathcal{L}_i(\theta) \tag{1}$$ where the weights $w_i$ are dynamically adjusted based on the cumulative loss at previous time steps. Typically, $w_i \propto \exp(-\lambda \sum_{j < i} \mathcal{L}_j)$. This forces the network to learn the trajectory sequentially, respecting the arrow of time.

This architectural choice imposes strict requirements on the training data. The data must be *causally continuous*. A gap in the data, a region of unphysical noise, or a "stiffness spike" (an under-resolved close encounter) at $t_{early}$ will result in a high residual $\mathcal{L}_{early}$. The causal weighting mechanism will then suppress the weights for all $t > t_{early}$ to zero, effectively halting the training process. Thus, for CTL-PINNs, data quality is not just about global accuracy; it is about the *continuity of learnability* along the temporal axis. A single "bad" segment renders the entire subsequent trajectory useless for training.

# 2 Assessment Strategy: Trade-offs Between Pre-Training Validation and Trial Training

The central strategic question is how to validate this complex data. The research identifies two primary methodologies: Static Pre-Training Validation (analyzing the dataset $\mathcal{D}$ itself) and Dynamic Trial Training (analyzing the interaction between $\mathcal{D}$ and the model $M$). Relying solely on one introduces significant risks.

## 2.1 Static Pre-Training Validation

This approach involves calculating physical and statistical metrics on the raw Brutus output (CSV/HDF5 files) before any tensor operations are initiated.

#### Advantages:

- **Computational Scalability:** Static checks are typically $O(N)$ or $O(N \log N)$ operations performed on CPUs. This is orders of magnitude cheaper than the iterative backpropagation required for training.

- **Physical Interpretability:** Errors detected here are directly mapped to physical concepts. If the angular momentum vector $\mathbf{L}$ precesses in a supposedly isolated system, the integration error is undeniable. This provides a clear "reject" criterion.

- **Sanitization:** It prevents "poisoning" the batch normalization statistics of a neural network. If a dataset contains outliers (e.g., numerical singularities where position $x \to \infty$ or $NaN$), these can skew the mean and variance statistics of the input layers, destabilizing the initialization of the entire network.

#### Limitations:

- **Invisibility of Optimization Landscapes:** A trajectory may be physically valid (conserves energy, continuous) but possess extremely high frequency components that are difficult for a Multi-Layer Perceptron (MLP) to resolve due to spectral bias. Static analysis cannot easily measure "spectral learnability" without performing Fourier transforms that may themselves suffer from sampling artifacts.

- **Interpolation Blindness:** PINNs evaluate residuals at *collocation points* which may not coincide with data points. Static analysis of discrete data points $t_i$ does not guarantee that the implicit interpolant between $t_i$ and $t_{i+1}$ is physical. If the Brutus time-step was too large, the "straight line" or "spline" connecting the points might violate conservation laws, even if the points themselves do not.

## 2.2 Dynamic Trial Training

This strategy involves training the specific CTL-PINN architecture on a small subset of the data (e.g., a single trajectory or a few batches) for a limited number of epochs.

#### Advantages:

- **Gradient Pathology Detection:** This is the only way to detect "exploding" or "vanishing" gradients caused by the specific interplay of the data's dynamic range and the network's activation functions. For N-body problems, where forces can scale by orders of magnitude during collisions, this is a critical check.

- **Causal Weight Verification:** It validates that the causal propagation mechanism is functioning. If the weights $w(t)$ do not advance past $t=0$ after 1000 epochs, it indicates that the initial conditions or the first few steps are "too stiff" for the current learning rate/architecture configuration.

- **Hyperparameter Sensitivity Check:** It helps distinguish between "bad data" and "bad hyperparameters."

#### Limitations:

- **Cost:** Requires GPU resources and significant time overhead per dataset if not strictly capped.

- **False Negatives:** A successful trial training on an "easy" segment of the orbit does not guarantee success on a "chaotic scattering" segment. The trial set must be carefully selected to be representative of the hardest physics.

- **Overfitting Ambiguity:** A model might easily overfit a single trajectory (memorization) without learning the underlying physics laws, providing a false sense of data quality. "Success" in trial training (low loss) might just mean the network is large enough to memorize noise.

## 2.3 The Optimal Strategy: The "Staged Gate" Protocol

The research suggests that the optimal strategy is a hybrid **Staged Gate Protocol**. This prioritizes the low-cost elimination of obviously bad data (Static Validation) before incurring the cost of probing subtle learnability issues (Trial Training).

**Phase 1: The Physics Gate (Static)**
- **Input:** Raw Brutus Trajectories.
- **Action:** Rigorous checking of conservation laws (Energy, Momentum) and symplectic consistency.
- **Outcome:** Binary Pass/Fail. Trajectories with drift $> \delta_{tol}$ are discarded immediately. This filters out integration failures.

**Phase 2: The Stiffness Gate (Static)**
- **Input:** Physically valid trajectories.
- **Action:** Analysis of Sampling Density vs. Local Curvature (using the SASD metric defined below).
- **Outcome:** Flagging. Trajectories are not discarded but marked as "High Stiffness." These require either resampling (running Brutus again with tighter tolerance) or specific "Curriculum Learning" schedules (introducing them later in training).

**Phase 3: The Learnability Gate (Dynamic)**
- **Input:** A stratified sample of Phase 2 survivors (specifically including High Stiffness cases).
- **Action:** "Overfit Challenge." Train the CTL-PINN on this single trajectory to machine precision.
- **Outcome:** Architectural Validation. If the model cannot overfit a single valid trajectory, the *architecture* (not the data) is insufficient (e.g., too shallow, wrong activation function).


<a id="tab:assessment_strategies"></a>

| Feature              | Pre-Training Validation (Static) | Trial Training (Dynamic) | Staged Gate Protocol (Hybrid) |
|----------------------|----------------------------------|--------------------------|-------------------------------|
| **Primary Metric**   | Physical Conservation, Continuity | Convergence Rate, Loss Value | Composite Score |
| **Computational Cost** | Low (CPU) | High (GPU) | Optimized (CPU first, GPU second) |
| **Detects**          | Integration Errors, Outliers | Gradient Issues, Hyperparams | Both + Architecture Mismatch |
| **Risk Addressed**   | Garbage In, Garbage Out | Model Divergence | Systemic Failure |
| **Blind Spot**       | Neural Network Inductive Bias | Physical Validity of Minima | None |

Table 1: Comparative Analysis of Assessment Strategies


# 3 Mathematically Grounded Metrics for Data Quality

To operationalize the Staged Gate Protocol, we must define specific metrics. These metrics extend beyond simple error checking; they quantify the *fitness* of the data for the specific task of causal physics-informed learning.

## 3.1 Symplectic Conservation Score (SCS)

While Brutus is an arbitrary-precision integrator, it is not inherently symplectic (it does not strictly preserve phase space volume by construction, unlike Leapfrog). However, for the data to be valid training material for a physics-informed model, it must exhibit the properties of a conservative Hamiltonian system $H(\mathbf{q}, \mathbf{p})$.

#### Derivation:

The Hamiltonian for the N-body problem is: $$H = \sum_{i} \frac{\mathbf{p}_i^2}{2m_i} - \sum_{i < j} \frac{G m_i m_j}{|\mathbf{q}_i - \mathbf{q}_j|} \tag{2}$$ For a physically valid solution, $\frac{dH}{dt} = 0$. In numerical data, errors manifest as energy drift.

#### Metric Definition:

We define the Symplectic Conservation Score ($SCS$) as the maximum normalized deviation of the Hamiltonian over the trajectory duration $T$: $$SCS = \log_{10} \left( \max_{t \in [0, T]} \left| \frac{H(t) - H(0)}{H(0)} \right| \right) \tag{3}$$

#### Thresholds for CTL-PINN:

- **$SCS < -10$:** Excellent. Brutus has converged to high precision. Ideal for training.

- **$-10 < SCS < -6$:** Acceptable. The drift is likely below the noise floor of the neural network's float32/float64 arithmetic.

- **$SCS > -4$:** Reject. The trajectory exhibits significant physical violation. A PINN trained on this will face conflicting gradients: the data loss (trying to fit the drift) and the physics loss (trying to enforce $\dot{H}=0$) will fight, leading to convergence failure.

**Insight:** In chaotic systems, energy error often grows linearly or quadratically with time in non-symplectic integrators. A high SCS suggests the integrator step size was too large for the chaotic amplification factor of the specific orbit.

## 3.2 Stiffness-Aware Sampling Density (SASD)

Stiffness is the primary cause of failure for neural ODE solvers and PINNs. It occurs when the timescales of the system's components vary by orders of magnitude---common in N-body problems during close encounters where the dynamical time $\tau \sim \sqrt{r^3/GM}$ shrinks rapidly. Brutus handles this adaptively, but if the output data is saved at fixed intervals (or if the adaptive steps are too coarse for the *network's* capacity), the data will be "aliased" relative to the physics.

#### Metric Derivation:

We define a local stiffness proxy based on the curvature of the trajectory, which correlates with the acceleration magnitude $\|\mathbf{a}\|$. The sampling density is $\rho(t) = 1/\Delta t_i$. The metric compares the time step $\Delta t_i$ to the local characteristic timescale $\tau_{char} = \frac{\|\mathbf{v}\|}{\|\mathbf{a}\|}$ (time to change velocity direction significantly).

#### Metric Definition:

$$SASD_i = \frac{\Delta t_i}{\tau_{char}(t_i)} = \Delta t_i \cdot \frac{\|\mathbf{a}(t_i)\|}{\|\mathbf{v}(t_i)\|} \tag{4}$$ (To avoid division by zero at turning points, a more robust form uses the radius of curvature $\rho_{curv} = v^2/a_{\perp}$).

#### Interpretation:

- **$SASD \ll 1$:** The trajectory is over-sampled. The path between points is effectively linear. Safe for training.

- **$SASD \sim 1$:** The trajectory turns significantly between data points.

- **$SASD > 1$:** The trajectory is under-sampled. The particle performs a "sharp turn" or "cusp" between data points.

**Risk to CTL-PINN:** A high SASD value implies that the "causal link" between $t_i$ and $t_{i+1}$ is broken. The physics residual $\mathcal{L}_{physics}$ evaluated at a collocation point *between* these data points (using interpolation) will be massive because the interpolant cannot capture the cusp. This stops the propagation of causal weights. Data with $SASD > 0.5$ should be flagged for resampling.

## 3.3 Interpolation Physics Residual (IPR)

This is a critical "second-order" metric. PINNs do not just learn the data points; they learn a continuous manifold. Therefore, the *interpolant* implied by the data must satisfy the physics. If we use Cubic Hermite Splines (which preserve positions and velocities) to interpolate the Brutus data, does this spline satisfy Newton's laws? 

#### Protocol:

1.  Construct a piecewise Cubic Hermite Interpolating Polynomial (PCHIP) $\mathbf{q}_{spline}(t)$ using the data $\{(\mathbf{q}_i, \mathbf{v}_i)\}$.

2.  Sample $M$ synthetic "collocation points" $\tau_k$ uniformly distributed *between* the data points.

3.  Calculate the physics residual at these synthetic points: $$IPR = \frac{1}{M} \sum_{k=1}^{M} \left\| \frac{d^2 \mathbf{q}_{spline}}{dt^2}(\tau_k) - \mathbf{F}_{gravity}(\mathbf{q}_{spline}(\tau_k)) \right\|^2 \tag{5}$$

#### Relevance:

If $IPR$ is high, it means that even though the data points are correct, the "shape" of the trajectory between them (as defined by standard interpolation) is unphysical. This indicates that the data density is insufficient to constrain the continuous solution space of the PINN. The network will struggle to find a function that fits both the data points and the physics equation between them, leading to "wobbling" or high-frequency artifacts. This metric directly predicts the "Physics Loss" component of the PINN training.

## 3.4 Phase Space Coverage Entropy (PSC)

Chaotic systems are ergodic (or have ergodic components). For a model to generalize, the training data must cover the relevant phase space structures---both the stable regions (quasi-periodic orbits) and the unstable regions (close encounters, scattering). A dataset biased towards one will fail on the other.

#### Metric Definition:

We discretize the phase space of interest (e.g., the $r_{12}, r_{23}$ distance plane or the Poincaré section) into a grid of $K$ bins. Let $p_k$ be the probability of a data point falling into bin $k$. The Shannon Entropy is: $$H_{data} = - \sum_{k=1}^{K} p_k \log p_k \tag{6}$$

#### Application:

- **Low Entropy:** The data is clustered in a small region (e.g., all particles far apart). The model will fail to learn close-encounter dynamics.

- **High Entropy:** The data explores diverse configurations.

- **Stiffness Coverage Ratio:** Specifically check the bin corresponding to $r_{min} \to 0$. If this bin is empty, the dataset lacks the "hard" physics examples necessary to train the network to handle singularities. The report recommends "Importance Sampling" to enrich the dataset with these high-stiffness events.

# 4 Risks to Model Parameters and Causal Training Dynamics

The user query specifically asks to address "risks to model parameters." In the context of CTL-PINNs and chaotic data, these risks are non-trivial and often structural.

## 4.1 The Causal "Firewall" Effect

The causal loss weighting is defined as $w_i = f(\sum_{j<i} \mathcal{L}_j)$.

- **Risk:** If the data contains a single "bad" point (high IPR or SASD) at time $t_{bad}$, the residual $\mathcal{L}(t_{bad})$ remains high. Consequently, the weights for all $t > t_{bad}$ vanish ($w_t \to 0$).
- **Parameter Consequence:** The gradients $\frac{\partial \mathcal{L}}{\partial \theta}$ for parameters governing the late-time behavior become zero. These parameters effectively "die" or drift randomly. The model learns the trajectory perfectly up to $t_{bad}$ and then flatlines. This is a specific failure mode of causal training that does not exist in standard PINNs (which would just average the error globally).
- **Mitigation:** The SASD metric acts as a pre-training filter to prevent these "causal firewalls."

## 4.2 The Dead Neuron Problem in N-Body Scaling

N-body data is scale-invariant but numerically vast. Distances can range from $10^{-3}$ (close encounter) to $10^2$ (ejection).

- **Risk:** If the data is fed raw into the network, the inputs will push the neurons into the saturation regions of their activation functions (e.g., $\tanh(100) \approx 1$, gradient $\approx 0$).
- **Parameter Consequence:** Vanishing gradients in the first layer. In a deep network, this prevents feature extraction.
- **Mitigation:** The validation pipeline must include a Normalization Check. Calculate the Kullback-Leibler (KL) divergence between the input data distribution and a standard normal distribution $\mathcal{N}(0, 1)$. If $D_{KL}$ is high, the data requires log-scaling or robust standardization (e.g., using median and IQR instead of mean/std to handle outliers) before training.

## 4.3 Spectral Bias and High-Frequency Oscillations

Neural networks satisfy a "Spectral Bias" principle---they learn low-frequency functions quickly and high-frequency functions slowly.

- **Risk:** Chaotic trajectories often possess a broad frequency spectrum. If the data contains high-frequency oscillations (e.g., a tight binary subsystem orbiting a third body), the PINN will smooth over them, effectively learning a "mean field" approximation rather than the true dynamics.
- **Parameter Consequence:** The weights responsible for high-frequency features will not converge within standard training times.
- **Mitigation:** Use the IPR metric to detect high-frequency content. If detected, the architecture should be augmented with Fourier Feature mappings (positional encoding) to shift the spectral bias of the network.

# 5 Detailed Implementation Protocol: The "Staged Gate" Workflow

This section synthesizes the research into a coherent, actionable workflow for the research team.

## 5.1 Phase 1: Data Ingestion and Static Auditing (CPU)

This phase runs on the entire generated dataset.

1.  **Load and Normalize:**

    - Load $(\mathbf{q}, \mathbf{p}, t)$ from Brutus output.

    - Check for NaN or Inf.

    - Compute $SCS$ (Energy Drift). **Gate:** Reject if $|SCS| > 10^{-5}$.

2.  **Stiffness Analysis:**

    - Compute accelerations $\mathbf{a}_i$ and velocities $\mathbf{v}_i$.

    - Compute $SASD$ profile.

    - **Gate:** If $\max(SASD) > 0.5$, flag for "Resampling." Do not train on this trajectory yet. It requires finer Brutus output steps.

3.  **Manifold Check (IPR):**

    - Fit Cubic Hermite Spline.

    - Sample 10 synthetic points per interval.

    - Compute $IPR$.

    - **Gate:** If $IPR > 10^{-3}$, the data is aliased. Reject or Resample.

## 5.2 Phase 2: The "Overfit Challenge" (GPU)

This phase runs on a randomly selected *subset* (e.g., 1%) of the passing data to validate the configuration.

1.  **Setup:** Initialize the exact CTL-PINN architecture intended for full training.

2.  **Challenge:** Attempt to overfit a *single* stiff trajectory (one that passed Phase 1 but had high SASD).

3.  **Monitoring:**

    - Track Loss $\mathcal{L}_{train}$.

    - Track Causal Weights $w(t)$ evolution.

    - Track Gradient Norms $\|\nabla_\theta \mathcal{L}\|$.

4.  **Success Criteria:**

    - $\mathcal{L}_{train}$ converges to machine precision ($< 10^{-6}$).

    - Causal weights propagate to $t=T$ (i.e., the "firewall" is breached).

5.  **Diagnostic:**

    - If loss plateaus: Architecture is too small (under-parameterized).

    - If weights don't propagate: Causal parameter $\lambda$ is too high (too strict).

    - If gradients explode: Normalization is incorrect.

## 5.3 Phase 3: Dataset Composition and Augmentation

1.  **Diversity Check:** Compute Phase Space Entropy ($H_{data}$) on the accepted dataset.

2.  **Balancing:** If the dataset is dominated by stable orbits (low entropy), use **Importance Resampling**. Run Brutus specifically initialized in "chaotic" regions (e.g., using the figure-8 or Pythagorean 3-body initial conditions) to generate more high-entropy examples.

3.  **Symmetry Augmentation:** Apply $SO(3)$ rotations and translations to valid trajectories to increase dataset size without computational cost, ensuring the PINN learns rotational invariance.

# 6 Synthesis and Conclusion

The development of a robust CTL-PINN for the Three-Body Problem requires moving beyond the notion of data "accuracy" to the more complex notion of data "fitness for causal learning." The analysis reveals that the primary risks---spectral bias, causal firewalls, and dead gradients---stem from the mismatch between the continuous nature of the PINN and the discrete, variable-density nature of the Brutus data.

By implementing the **Staged Gate Protocol**, the research team can decouple these risks. Phase 1 (Static) ensures the physics is sound and the sampling density is sufficient to support a continuous manifold (low IPR). Phase 2 (Dynamic) ensures the network architecture has the capacity to resolve the specific stiffness profile of the data without gradient pathologies.

This rigorous, multi-layered approach ensures that the computational investment in arbitrary-precision data generation yields a dataset that is not just numerically correct, but algorithmically effective for training the next generation of physics-informed neural solvers.

## 6.1 Recommendations for Future Work

- **Curriculum Learning:** Implement a curriculum where the model is trained first on "easy" (low SASD) trajectories and progressively introduced to "hard" (chaotic, high SASD) trajectories. This stabilizes the causal weights.

- **Adaptive Activation Functions:** Investigate using adaptive activation functions (like Rowdy or locally adaptive sine) to handle the varying frequency content of the N-body problem better than fixed Tanh/ReLU.

- **Symplectic Neural Networks:** Consider modifying the architecture to be inherently symplectic (HNN), moving conservation from a soft loss term to a hard architectural constraint, which reduces the data quality burden regarding energy drift.

# Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the converted source body and are excluded from fidelity comparison in `verification_reports/data_quality_assessment_verification_report.md`.

## SI-DQA-001: Orphaned bibliography.tex — 33 references never cited in body

- Source section: `bibliography.tex` (orphaned — never imported by `main-data-quality-assess.tex`).
- Markdown heading: N/A (excluded from conversion — bibliography is not part of the audit corpus per D-28).
- Note: The LaTeX source includes `sections/bibliography.tex` with 33 `\bibitem` entries, but `main-data-quality-assess.tex` contains zero `\input{sections/bibliography}` lines and the body contains zero `\cite{}` commands. The 33 references are inaccessible in the compiled LaTeX output. Both markdown candidates independently fabricated reference lists (top-level: 32 numbered entries with `## References` heading; pandoc: 32 unnumbered entries with orphan `99` token). These fabricated reference lists were stripped during Phase 11 Plan 02 as they represent content not present in the LaTeX source body. The question of whether the 33 references should be reconnected to the document body with proper `\cite{}` commands is a LaTeX source edit — outside v1.3 scope.

## SI-DQA-002: No source-level mathematical, factual, or methodological concerns identified

- Source sections: All 6 active sections (`introduction.tex`, `assessment_strategy.tex`, `data_quality_metrics.tex`, `model_parameter_risks.tex`, `implementation_protocol.tex`, `synthesis_conclusion.tex`).
- Markdown headings: All corresponding sections in `data_quality_assessment.md`.
- Note: No source-level mathematical, factual, or methodological concerns were identified during the Phase 11 section-by-section audit. The converted markdown body preserves the LaTeX source content exactly. Any discrepancies found were conversion artifacts (injected citations, HTML table corruption, description-list syntax) — all of which were fixed in the markdown without modifying any LaTeX source content.
