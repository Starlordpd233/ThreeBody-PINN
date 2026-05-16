# Comprehensive Analysis and Resolution Report: CTL-PINN Framework for the Three-Body Problem

**Disclaimer:** This document is for informational purposes only and does not constitute professional, financial, engineering, or safety-critical advice. The implementation of complex neural network architectures for chaotic dynamical systems carries inherent computational and theoretical risks.

**Key Points:**
- **Readiness Assessment:** The framework is currently **not ready for implementation**. Fundamental mathematical discrepancies block execution.
- **Critical Interventions:** The characteristic length ($D$) scaling and the Automatic Differentiation (AD) chain-rule applications contain systemic mathematical errors that will prevent the Physics-Informed Neural Network (PINN) from learning valid dynamics.
- **Architectural Corrections:** SIREN weight initialization and dynamic $\omega_0$ scheduling are incorrectly specified in the documentation and must be aligned with established literature. 
- **Input Vector Finalization:** Option B (Shape Invariants + Direction Cosines) is strongly recommended over trigonometric encodings to avoid gimbal lock during chaotic scattering.

The Curriculum-Trained Physics-Informed Neural Network (CTL-PINN) framework for the three-body problem presents a highly sophisticated, synergistic approach to modeling chaotic dynamics. By fusing a Sinusoidal Representation Network (SIREN) with a Power-Enhanced SkipResNet (SQR-SkipResNet) and an Augmented Lagrangian Method (ALM) for physics constraints, the architecture is theoretically well-equipped to handle the non-linear, multi-scale nature of gravitational interactions. However, the foundational specifications currently contain severe mathematical and geometric misalignments. 

This report provides an exhaustive issue-by-issue analysis of the consolidated "Architecture & Physics Foundations Review." It evaluates all BLOCKING and MAJOR issues, resolves the open decisions regarding the input vector space, triages minor issues, and exposes critical unflagged gaps that were missed in previous audits.

## 1. Executive Summary

While the live codebase occasionally sidesteps the documentation's flaws (such as the SIREN initialization bug), the theoretical blueprint contains contradictions that will systematically corrupt the network's physics loss and curriculum staging. The framework's overarching readiness and core components are assessed as follows:

1. **Readiness Assessment:** The framework is explicitly **not ready for implementation**. Moving forward without rectifying the core scaling and derivative errors will result in a catastrophically failed training loop.
2. **Blockers & Major Issues:** The most severe issues stem from dimensional scaling errors (characteristic length $D$) and missing chain-rule factors in the automatic differentiation pipeline. Furthermore, SIREN weight initialization, constraint counting errors, layer normalization attribution, and normalization range mappings contain severe discrepancies that must be rectified.
3. **Open Decisions:** Option B (Shape Invariants + Direction Cosines) is strongly recommended for the 14-D input vector to circumvent chaotic gimbal lock. The $I_{\text{norm}}$ definition must be wrapped in a `tanh` activation for all network inputs.
4. **Minor Issues Triage:** Issue D4 (COM for Brutus outputs) was elevated to MAJOR. Issues D2/D3 require ablation studies, while D6/D8 are confirmed and deferred. Issues D1, D9, and D10 have been explicitly triaged and resolved, prioritizing $D=6.694$ scaling implementation from day one.
5. **Cross-Issue Dependencies:** The priority queue is validated with critical modifications, ensuring that $D$ scaling, AD chain-rules, and COM transformations strictly block all downstream architectural tasks.
6. **Unflagged Gaps:** A rigorous independent review discovered two critical unflagged gaps regarding missing mass scaling parameters in both the physics residual ($\mathcal{L}_{\text{physics}}$) and the Hamiltonian Energy Regularizer ($\mathcal{L}_{\text{energy}}$), as well as a severe ALM momentum desynchronization vulnerability. 

## 2. Issue-by-Issue Analysis (Blockers & Major)

This section systematically verifies and resolves the most critical findings from the audit, ensuring that the theoretical documentation matches both the mathematical reality of the N-body problem and the computational realities of deep learning.

### B-01: SIREN Initialization Mismatch
**Context:** The `pinn_architecture.md` document (Section 2.2 "A Principled Initialization Scheme for SIREN Layers" and Section 2.4 "Finalized Architectural Hyperparameters", Table 1) defines the hidden-layer weight initialization formula as scaling *with* $\omega_0$ (i.e., $\mathcal{U}[-\frac{\omega_0}{6 n_{in}}, \dots]$).
**Analysis:** I fully confirm the audit's finding that this formula is incorrect and catastrophic. The original Sitzmann et al. (2020) formulation mandates that pre-activations (the input to the sine function) maintain a standard normal distribution to prevent the frequency from growing uncontrollably with depth [cite: 1, 2, 3]. To achieve this, the weights must be drawn from $\mathcal{U}(-\sqrt{6/n}, +\sqrt{6/n})$. If a custom hidden $\omega_0$ is utilized (though typically $\omega_0 = 1$ for hidden layers), the bounds must be *divided* by $\omega_0$ [cite: 1, 3]. Scaling the variance by a factor of 30 rather than dividing by it would exponentially explode the activation variance across 12 layers.
**Resolution:** The live code (`basic_architecture.py`) is correct. The `pinn_architecture.md` specification must be rewritten to explicitly state:
$$W_i \sim \mathcal{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\omega_0}, \frac{\sqrt{6/n_{\text{in}}}}{\omega_0}\right]$$

### B-02: Characteristic Length ($D$) Formula
**Context:** The `ctl_instruction.md` document (Section Phase 1 - Step 2: "Preprocessing: Scaling to Dimensionless Units") and `pinn_architecture.md` (Section 5.3 "Output Frame and File Format", Table 2) define $D = \sqrt[3]{G T^2}$, omitting total mass.
**Analysis:** I confirm this is a critical dimensional error. From Kepler's Third Law and basic dimensional analysis of Newton's gravitational constant ($[G] = L^3 M^{-1} T^{-2}$), a characteristic length scale derived from time and gravity *must* incorporate mass. Specifically, $L^3 = G M T^2$. Omitting $M_{\text{tot}}$ assumes $M_{\text{tot}} = 1$. In a hierarchical three-body problem where masses sum to approximately 3, this introduces a systematic scaling error of $3^{1/3} \approx 1.44$. All scaled positions, velocities, and energies would be fundamentally distorted. Specifically, this omission introduces relative errors of 44.22% for scaled positions and velocities, 108.01% for scaled kinetic energy and raw scaled angular momentum, -30.66% for scaled potential magnitude, and a severe 200.00% distortion in the virial ratio.
**Resolution:** Adopt the correct formula globally:
$$D = (G \cdot M_{\text{tot}} \cdot T^2)^{1/3}$$
*Note:* This correction triggers a massive hidden dependency regarding the physics residual, which is addressed in Section 6 of this report.

### B-03, B-04, M1, M2: Input Vector Dimensionality and Composition
**Context:** Discrepancies exist across `ctl_instruction.md` (Section Phase 1 - Step 4: "Assemble the Final 12-Component Input Vector") and `pinn_architecture.md` (Section 5.3, Table 2) claiming the input vector is 12D, 13D, or 14D. Furthermore, the 5 "orientation" slots in the Initial Condition (IC) vector are disputed.
**Analysis:** I confirm the severity of this inconsistency. A neural network requires a rigid, static input dimension for its first linear layer. The framework cannot proceed until this is locked. The 14D formulation (1 Time component + 13 IC components) provides the requisite information to fully constrain the 9 degrees of freedom of a 3-body system in a COM frame. The composition of this vector is resolved in the "Open Decisions" section below.
**Resolution:** Standardize the architecture to a strict 14D input vector: $[t', \text{IC}_{13D}]$.

### B-05 & M3: COM Frame Violation and Scaling Order
**Context:** Hierarchical ICs are perturbed out of the Center of Mass (COM) frame, but the PINN output assumes a COM frame, as noted in `ctl_instruction.md` (Section Phase 1 - Step 2.5: "Verify Center-of-Mass (COM) Frame") and `pinn_architecture.md` (Section 5.3 "Output Frame and File Format").
**Analysis:** I fully confirm this finding. If the initial conditions possess a net momentum, the network is forced to learn a continuous Galilean translation superimposed on complex non-linear dynamics. Neural networks struggle significantly with mixed reference frames because it destroys the translational invariance inductive bias. Furthermore, scaling coordinates before zeroing the COM permanently bakes scaled offset artifacts into the trajectories.
**Resolution:** Implement a strict preprocessing pipeline ordering:
1. Calculate raw COM position and velocity.
2. Shift all raw ICs and Brutus trajectory snapshots to the COM frame.
3. Assert that total momentum is $< 10^{-12}$.
4. Apply the characteristic scaling factors ($D$ and $V$).

### B-09: Softening Parameter ($\epsilon$) Mismatch
**Context:** The framework uses $\epsilon=10^{-10}$ for calculating invariants and curriculum stages (`ctl_instruction.md` Section Phase 1 - Step 3: "Necessary Calculations of Invariants"), but $\epsilon_{\text{soft}}=10^{-5}$ for the neural network's loss function (`pinn_architecture.md` Section 3.2 "Physics Residual Term" and Section 3.3 "HNN-Style Energy Regularizer").
**Analysis:** I dispute the previous audit's recommendation to unify this at $10^{-8}$ and strongly endorse the "Dual-Context Epsilon Strategy." Neural network training on GPUs using FP32 arithmetic is highly susceptible to gradient explosions and NaN propagation. When $r \to 0$ during close encounters, the $1/r^3$ derivative in the physics loss will overflow FP32 limits without a sufficient regularization floor (like $10^{-5}$). Conversely, curriculum stage assignment happens on CPUs in FP64 arithmetic. Using $10^{-10}$ allows the curriculum to accurately shadow unsoftened Hamiltonian dynamics.
**Resolution:** Maintain the dual-context approach. Explicitly document that the network learns Hamiltonian dynamics regularized by a microscopic GPU-precision floor, not "softened physics."

### B-10: Dynamic $\omega_0$ Scheduling
**Context:** `update_omega0()` decays `first_omega_0` from 30 to 10 over epochs in `pinn_architecture.md` (Section 2.2 "A Principled Initialization Scheme...", Listing 1).
**Analysis:** I confirm this is dead code based on a fundamental misunderstanding of the SIREN architecture. The $\omega_0$ parameter dictates the spatial frequency of the initial weights before training begins. Dynamically altering a scalar multiplier in an initialization function during the training loop has absolutely zero effect on the instantiated weight matrices [cite: 1, 3]. 
**Resolution:** Delete the scheduling function. Lock `first_omega_0 = 30` and `hidden_omega_0 = 1`. 

### AD Chain-Rule Factor Missing
**Context:** The network takes normalized time $\tau \in [-1, 1]$ but must evaluate physics in dimensionless time $u = t/T$ per `pinn_architecture.md` (Section 3.2 "Physics Residual Term" and Section 5.2 "Output Layer and Kinematic Consistency...").
**Analysis:** I confirm this is a catastrophic mathematical oversight. Because $\tau = 2u - 1$, the first derivative $d/du = 2(d/d\tau)$ and the second derivative $d^2/du^2 = 4(d^2/d\tau^2)$. If the PINN calculates acceleration directly from $d^2/d\tau^2$ without multiplying by 4, the network will attempt to learn a gravitational force that is four times weaker than reality. This will irreparably conflict with the data fidelity loss, causing the Augmented Lagrangian Method (ALM) parameters to oscillate wildly and fail to converge.
**Resolution:** The explicit PyTorch component-wise derivative code provided in the review must be adopted, ensuring `acceleration_u = 4.0 * acceleration_tau` is explicitly hard-coded into the physics residual calculation.

### M4: Constraint Counting Error
**Context:** Documented in `ctl_instruction.md` (Section Phase 1 - Step 4: "Mathematical Guarantees").
**Analysis:** The text claims "13 constraints for 8-D reduced phase space." This is a fundamental mathematical error in identifying the degrees of freedom. A three-body system begins with 18 degrees of freedom ($3 \text{ bodies} \times 3 \text{ spatial coordinates} \times 2 \text{ for position/velocity}$). Subtracting 3 for COM position, 3 for COM momentum, and 3 for overall SO(3) rotational invariance leaves exactly 9 degrees of freedom, not 8.
**Resolution:** Correct the documentation to accurately reflect the topology: "9 constraints reduce 18-DOF to 9 dimensions."

### M5: $I_3$ Normalization Mapping
**Context:** Outlined in `ctl_instruction.md` (Section Phase 1 - Step 4: "Apply Normalization").
**Analysis:** The document claims that the third shape invariant $I_3$ is "already in [-1,1]". However, the underlying formula dictates $I_i / I_{\max}$, which strictly places the value within the positive domain of $[0,1]$. Passing an asymmetric positive domain into a layer optimized for zero-centered inputs destabilizes the initial SIREN activations.
**Resolution:** Apply the normalization mapping `I3_norm = 2*I3 - 1` to strictly enforce the `[-1,1]` boundary constraint.

### M8: LayerNorm Attribution
**Context:** Described in `pinn_architecture.md` (Section 2.3 "The Power-Enhanced SkipResNet...").
**Analysis:** The documentation attributes the application of LayerNorm on the skip path to the original SQR-SkipResNet paper. However, a review of the foundational SQR-SkipResNet literature confirms that the original architecture contains no such LayerNorm application.
**Resolution:** Re-attribute this explicitly as a custom author modification designed to bound the quadratic power term during extreme gradient spikes common in close encounters.

### M9: $E_{\text{norm}}$ Range Unused
**Context:** Documented in `ctl_instruction.md` (Section Phase 1 - Step 4: "Apply Normalization").
**Analysis:** The normalization formula relies on `tanh(E / E_scale)`. Because all bound systems inherently have $E < 0$, the resulting mapping exclusively occupies the domain `[-1, 0)`. The positive input range is mathematically never utilized by the network.
**Resolution:** This asymmetric saturation is acceptable for SIREN networks provided the architecture is explicitly aware of it. Document clearly that the positive range is unused and verify that this lack of symmetry does not bias the first-layer spectral density.

### M10: $m_{\text{norm}}$ Range Asymmetry
**Context:** Outlined in `ctl_instruction.md` (Section Phase 1 - Step 4: "Apply Normalization").
**Analysis:** The mass normalization formula consistently yields values spanning roughly `[-0.93, 0.585]` for hierarchical mass distributions, failing to center perfectly on zero. 
**Resolution:** This is physically accurate and mathematically acceptable. The asymmetry inherently encodes the explicit mass hierarchy information, allowing the network to distinguish primary, secondary, and tertiary bodies without requiring an artificial zero-centered shift.

## 3. Open Decisions Recommendation

The framework requires definitive human approval on two key decisions before implementation can begin. The following are the robust architectural recommendations for both.

### D-01: 14-D Input Vector Composition
**Recommendation: Strictly adopt Option B (Shape Invariants + Direction Cosines).**

The decision between trigonometric encoding (Option A) and shape invariants with direction cosines (Option B) dictates how the network understands the spatial configuration of the three-body system. 

| Feature / Metric | Option A: Trigonometric Encoding | Option B: Shape Invariants + Direction Cosines |
| :--- | :--- | :--- |
| **Data Components** | $\sin(\theta_L), \cos(\theta_L), \sin(\phi_L), \cos(\phi_L), \sin(\gamma_{orb})$ | $I_1, I_2, I_3$ (Mutual Distances), $\cos(\theta), \sin(\theta)$ |
| **Reference Frame Reliance** | Heavily relies on spherical coordinate alignment (external frame). | Describes internal triangle geometry independently of external rotation. |
| **Chaotic Regime Stability** | **Poor.** Vulnerable to "Gimbal Lock." If orbital plane flips, derivatives of $\phi_L$ explode to infinity. | **Excellent.** Shape invariants and direction cosines have no coordinate singularities at the poles. |
| **Gradient Behavior** | Injects massive, erratic gradient spikes during close-encounter ejections (Stages 4-6). | Continuous and smooth through all physical encounters (except direct, hard collisions). |
| **Injectivity** | Topological discontinuities can confuse network phase-space mapping. | Highly unique, over-determined mapping of the system's state. |
| **Final Recommendation** | **REJECTED** | **APPROVED / STRONGLY RECOMMENDED** |

Option A proposes encoding the angular momentum vector via spherical coordinates. While common in rigid-body dynamics, this formulation is disastrous for chaotic scattering events. When the angular momentum vector aligns near the z-axis ($\theta_L \approx 0$ or $\pi$), the system enters "gimbal lock." The azimuthal angle $\phi_L$ becomes mathematically undefined, and its derivatives approach infinity. In Stages 4 through 6 of the curriculum, violent ejections and orbital plane flipping are common. Passing near a coordinate singularity will flood the network's first layer with extreme gradient spikes, destroying the Adam optimizer's momentum buffers.

Option B proposes replacing this with shape invariants ($I_1, I_2, I_3$) and direction cosines ($\cos(\theta), \sin(\theta)$). This formulation is vastly superior because mutual distances perfectly define the internal triangle of the three bodies independently of their absolute rotation. They are continuous and smooth through all physical encounters. Direction cosines smoothly track the tilt of the orbital plane without requiring an azimuthal angle, entirely bypassing gimbal lock. Because the bodies are already canonically sorted by mass and distance, this provides a fully unique, over-determined mapping of the system's state without topological discontinuities.

### D-02: $I_{\text{norm}}$ Definition
**Recommendation: Adopt the `tanh` wrapper globally for network inputs.**

The CTL text defines $I_{\text{norm}}$ as a raw ratio, while the code wraps it in `tanh`. Because the moment of inertia traces can spike during highly expansive trajectories (especially for marginally bound systems in Stage 6), feeding raw unbounded values into a SIREN network will force the pre-activations far out of their standard normal distribution, severely hampering the network's spectral learning capabilities. Wrapping the ratio in `tanh` perfectly maps the domain to $[-1, 1]$, satisfying the input contract required by the $\omega_0=30$ initialization [cite: 1, 3]. The CTL text must be updated to match the code perfectly.

## 4. Minor Issues Triage

The minor issues identified in the audit require the following explicit triage treatments to ensure no hidden blockers emerge during late-stage training:

*   **D1 (What exactly are the 3 angles for trigonometric encoding?):** *Defer / Resolved.* Because Option B (Shape Invariants + Direction Cosines) has been strongly recommended and selected over Option A, defining the exact trigonometric angles is rendered obsolete. 
*   **D2 & D3 (LayerNorm affine parameters):** *Confirm Ablation.* The SQR-SkipResNet literature does not mandate LayerNorm. Adding it stabilizes the power-term amplifications during close encounters, but setting `affine=True` allows the network to learn a scale ($\gamma$) and shift ($\beta$). In a SIREN architecture, learnable affine transformations *before* the sine activation can overwrite the carefully controlled frequency spectrum. Set `affine=False` as the default until ablation proves otherwise.
*   **D4 (COM for Brutus outputs):** *Elevate to MAJOR.* The Brutus outputs must absolutely be checked and corrected for COM drift. High-precision integrators can accumulate round-off errors over thousands of time steps, leading to a slow drift of the system's barycenter. If the PINN's data loss ($\mathcal{L}_{\text{data}}$) trains on drifting targets, it will attempt to model numerical error as physical forces. Apply the Galilean boost to Brutus data automatically.
*   **D6 (Mass drift in Brutus):** *Defer.* Mass is a constant parameter in Brutus. A simple `np.allclose()` assertion at data loading is sufficient.
*   **D8 (Stage 6 Collision Softening):** *Confirm.* Use raw, unsoftened $s_{\min}$ for stage logic to ensure rigorous ground-truth classification. Use $\max(s_{\min}, \epsilon_{\text{soft}})$ exclusively inside the network's loss functions.
*   **D9 (Is the orientation representational gap fatal?):** *Defer / Resolved.* The audit noted potential issues with replacing trigonometric angles. The recommended Option B utilizing direction cosines cleanly and fully closes this representational gap, rendering the concern resolved.
*   **D10 (Can training start with standard SIREN init while D formula is being fixed?):** *Elevate to Priority P0.* Yes. Training can and should commence with the corrected $D=6.694$ value immediately from day one to avoid costly, mandatory retraining later.

## 5. Cross-Issue Dependencies

The implementation priority queue provided in the audit is validated, provided the critical modifications listed below are strictly enforced. The dependencies cascade linearly, and attempting to train the model out of order will result in silently corrupted models.

1. **The Dimension Update (P0-1):** Fixing $D = (G \cdot M_{\text{tot}} \cdot T^2)^{1/3}$ is the absolute ground zero of the project. Because $D$ dictates $r'$, $v'$, and all subsequent invariants ($E, L_{\text{norm}}, Q, s_{\min}$), *every single data file* and stage assignment threshold must be recomputed before any other action is taken. 
2. **The Chain-Rule Fix (P0-5):** Once the data is properly scaled, the network must accurately map AD derivatives to physical derivatives. This must be implemented alongside the hidden unflagged gap identified below.
3. **The SIREN Contract (P0-2 & P0-6):** Only after the physical data is correct can the neural architecture be stabilized by fixing the hidden layer initialization and stripping the dead $\omega_0$ scheduling code.

## 6. What Was NOT Flagged (Critical Uncovered Gaps)

Diligent mathematical review of the interactions between the documents reveals two severe gaps that the previous audits completely missed.

### Unflagged Gap 1: Physics Residual and Hamiltonian Mass Scaling Discrepancy
The audit correctly identified that the characteristic length $D$ must include total mass: $D = (G \cdot M_{\text{tot}} \cdot T^2)^{1/3}$. However, neither the authors nor the audit traced how this change propagates into the physics residual equation ($\mathcal{L}_{\text{physics}}$) or the Hamiltonian Energy Regularizer ($\mathcal{L}_{\text{energy}}$). 

If we start with Newton's law:
$$\frac{d^2 \mathbf{r}_i}{dt^2} = G \sum_{j \neq i} \frac{m_j (\mathbf{r}_j - \mathbf{r}_i)}{|\mathbf{r}_j - \mathbf{r}_i|^3}$$
And substitute the scaled variables $t = T \cdot u$ and $\mathbf{r} = D \cdot \mathbf{r}'$:
$$\frac{D}{T^2} \frac{d^2 \mathbf{r}'_i}{du^2} = G \sum_{j \neq i} \frac{m_j D (\mathbf{r}'_j - \mathbf{r}'_i)}{D^3 |\mathbf{r}'_j - \mathbf{r}'_i|^3}$$
$$\frac{d^2 \mathbf{r}'_i}{du^2} = \frac{G T^2}{D^3} \sum_{j \neq i} \frac{m_j (\mathbf{r}'_j - \mathbf{r}'_i)}{|\mathbf{r}'_j - \mathbf{r}'_i|^3}$$
Substituting the corrected $D^3 = G \cdot M_{\text{tot}} \cdot T^2$, the coefficient $\frac{G T^2}{D^3}$ perfectly simplifies to $\frac{1}{M_{\text{tot}}}$. 

Therefore, the true dimensionless equation of motion is:
$$a'_i = \frac{1}{M_{\text{tot}}} \sum_{j \neq i} \frac{m_j (\mathbf{r}'_j - \mathbf{r}'_i)}{|\mathbf{r}'_j - \mathbf{r}'_i|^3}$$

However, `pinn_architecture.md` Section 3.2 defines the residual without this mass factor, explicitly stating: *"Masses (unchanged, as G=1 in the dimensionless system)"*. 
**Resolution:** This is a fatal omission. If the physics residual does not include the $1/M_{\text{tot}}$ division (or equivalently, if the raw masses $m_j$ are not scaled to mass fractions $m'_j = m_j / M_{\text{tot}}$ before entering the loss calculation), the network will attempt to learn accelerations that are intrinsically mismatched to the data loss. The physics loss implementation must divide the gravitational sum by $M_{\text{tot}}$.

**The Next Logical Question: Does $\mathcal{L}_{\text{energy}}$ also require this adjustment?**
Yes. In the PINN Architecture Document (Section 3.3), the Hamiltonian $H_{\text{total}}$ is defined using the raw unscaled masses $m_i$ alongside the scaled dimensionless kinematics ($r', v'$). The true kinetic energy relies on $v_i^2$, which scales as $\frac{D^2}{T^2} v_i'^2$, and potential energy relies on $1/r_{ij}$, which scales as $1/(D r_{ij}')$. Because $\frac{D^2}{T^2} = \frac{M_{\text{tot}}}{D}$ (derived from $D^3 = G M_{\text{tot}} T^2$), calculating the Hamiltonian with raw masses fundamentally breaks the conservation of energy mapping in dimensionless space. 
To maintain thermodynamic and kinetic energy conservation, the $\mathcal{L}_{\text{energy}}$ implementation must explicitly scale the raw input masses to mass fractions ($m'_i = m_i / M_{\text{tot}}$) or apply a global conversion scalar to the baseline $H_0$ target. Failure to implement this parallel correction ensures the energy loss term will forever fight the physics residual term, preventing the network from reaching convergence.

### Unflagged Gap 2: ALM Moving Average De-synchronization
The Augmented Lagrangian Method (ALM) relies on an exponential moving average of the squared physics loss ($v_p$) to adaptively update the penalty coefficient $\mu_p$. `pinn_architecture.md` specifies an "adaptive" collocation point sampling strategy that biases sampling toward high-acceleration regions. 
If the collocation points change dynamically and drastically from batch to batch, the baseline variance of $\mathcal{L}_{\text{physics}}$ will fluctuate wildly. The ALM's momentum buffer $\beta = 0.99$ assumes a relatively stationary loss landscape. Rapid fluctuations caused by adaptive point sampling will cause $\mu_p$ to destabilize, oscillating between under-penalizing physics (leading to non-physical solutions) and over-penalizing physics (stalling convergence).
**Resolution:** During early training stages (Stages 0-2), enforce the `uniform` collocation point strategy to allow $v_p$ and $\mu_p$ to stabilize. Only introduce `adaptive` collocation sampling in Stages 4-6 when the network requires high-density sampling around close encounters, and consider reducing the ALM momentum $\beta$ to 0.90 to allow it to react faster to sampling-induced variance.

**Sources:**
1. [computationalimaging.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhmJaxQlB8KTOgmqot9-MSZ60UM9wnZU77BpkaLhQBbVnzdajgEZkYjkeQ8cEmlPwM0rKDT8vSsRahQwBqzidr5DC-vr3ovKyA3-y8KkpTJDV8lX4WBGDMhOgTF8vZAvMtkb8kvDl1IipRPR5F)
2. [neurips.cc](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEg7OKf36xhvWu0cC2pVWOMvT5I_3yhqxVml5wBjjhltBCeq6ng0Op2l5VZEDGwuOkI3RfPUlP6XFnbq-1chN5YcPjs8IKYFgiBg2BnRYBifkznh9_v9rnDv1BgUBie_wESe5q__eiYFoF60TrwZ8iHZDlBL5Y6fhGXupsqGEPy4-dFuevBG5n9x6-MLtvX)
3. [emergentmind.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHWv6j8gOdk0VMlzHNDwNO9mJjAX_RKawVICT8S9-YOFtzN9bP6K5kDafzmaCRIHCtnzjkQCEVLQcM435hqruqWZet8qtm6fEKpuxj-OO9uMoSOtEoax7e9RoMeFb-KNe05xWni3fZS8cKq4g==)
