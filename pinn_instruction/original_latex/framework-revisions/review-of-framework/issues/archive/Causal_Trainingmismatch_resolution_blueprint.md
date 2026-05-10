# Resolution of the Causal Training Mismatch and Protocol Reconciliation in Physics-Informed N-Body Dynamics

Introduction to the Computational and Architectural Paradigm

The integration of high-fidelity numerical analysis with deep learning represents a profound paradigm shift in the study of chaotic dynamical systems. The specific research architecture under analysis targets one of the most enduring and notoriously complex challenges in classical mechanics: the Three-Body Problem.<sup>[1](#works-cited)</sup> This system is fundamentally characterized by nonlinear gravitational interactions, extreme exponential sensitivity to initial conditions, and intricate phase space structures defined by the coexistence of stable invariant tori and chaotic regions.<sup>[1](#works-cited)</sup> The accurate and long-term simulation of such a system presents a formidable challenge for traditional numerical and machine learning methods alike, requiring an ensemble of techniques that can capture multi-scale temporal features with high fidelity while strictly adhering to fundamental global conservation laws.<sup>[1](#works-cited)</sup>

To generate the necessary ground-truth data, the pipeline leverages the Brutus arbitrary-precision integrator. Unlike traditional symplectic integrators such as Leapfrog or Wisdom-Holman, which preserve the geometric properties of the Hamiltonian flow over long time scales at the cost of local accuracy, Brutus utilizes the Bulirsch-Stoer algorithm.<sup>[1](#works-cited)</sup> This extrapolation scheme computes the solution at a future time by subdividing the interval, performing integration with a modified midpoint method, and extrapolating the results to zero step size using rational functions.<sup>[1](#works-cited)</sup> By iteratively increasing the precision (word length) and decreasing the tolerance parameter until convergence, Brutus generates a "true" numerical solution that accurately shadows the exact mathematical trajectory of the chaotic system.<sup>[1](#works-cited)</sup>

The resulting data is intended to train a highly specialized Physics-Informed Neural Network (PINN). The target architecture is a hybrid Sinusoidal Representation Network (SIREN) equipped with a Power-Enhanced SkipResNet (SQR-SkipResNet) backbone.<sup>[1](#works-cited)</sup> This network is trained under a meticulously phased Curriculum Learning (CTL) protocol designed to transition the model from simple Keplerian motion to highly chaotic scattering events.<sup>[1](#works-cited)</sup> However, a critical systemic conflict exists within the current theoretical framework: there is a profound architectural mismatch between the sequential causal time-weighting proposed for the network's training dynamics and the Augmented Lagrangian Method (ALM)-based global sampling strategy defined in the network's loss formulation.

Furthermore, severe operational inconsistencies span the provided documentation. These discrepancies encompass the dimensionality of the conditional input vector (the 12-dimensional formulation versus the 14-dimensional formulation), the magnitude of the gravitational softening constants applied to the physics residuals, the enforcement of Center of Mass (COM) reference frames across diverse datasets, and the baseline temporal resolution dictated by the simulation outputs.

This comprehensive report provides an exhaustive resolution to the causal-training mismatch, mathematically reconciling the data validation protocol with the curriculum training plan. By systematically addressing the identified inconsistencies, standardizing the input vector formulations, and updating the pre-training validation metrics, this analysis establishes a definitive, unified blueprint for modeling chaotic N-body dynamics through physics-informed deep learning.

# The Dataset Generation and Preprocessing Pipeline

Before addressing the algorithmic mismatches within the neural network, it is imperative to establish a rigorous understanding of the underlying data pipeline. The simulation data framework handles a complete four-stage data pipeline designed to produce the training datasets for the physics-informed architecture.<sup>[1](#works-cited)</sup> The repository is structurally organized into functional directories, isolating raw initial conditions, integrated trajectories, validation scripts, and final metrics.<sup>[1](#works-cited)</sup>

The generation of the data begins with the formulation of Initial Conditions (ICs). The pipeline generates raw ICs using enhanced Sobol-based quasi-random sampling alongside specific hierarchical system generation protocols.<sup>[1](#works-cited)</sup> The hierarchical dataset consists of stable three-body configurations, typically featuring a tightly bound binary subsystem with a distant tertiary companion.<sup>[1](#works-cited)</sup> These systems exhibit smooth, quasi-periodic motion. Conversely, the quasi-random dataset covers a broad variety of chaotic configurations generated through random initial conditions, representing a much higher degree of physical complexity and dynamical instability.<sup>[1](#works-cited)</sup>

Following generation, the data undergoes a prescreening phase. This second stage utilizes dynamic stability filtering with adaptive thresholds to eliminate inherently unstable or immediately divergent configurations before they consume extensive computational resources during integration.<sup>[1](#works-cited)</sup> The surviving configurations are advanced to the third stage, where the Brutus N-body simulator performs high-precision integration utilizing the Bulirsch-Stoer method with GMP/MPFR arbitrary precision arithmetic.<sup>[1](#works-cited)</sup> Finally, the fourth stage calculates the final simulation results and performance metrics.<sup>[1](#works-cited)</sup>

The resulting file schemas are highly specific. The Initial Condition files consist of exactly three lines, each representing one of the three celestial bodies. The data fields strictly follow the format of mass, three-dimensional position coordinates, and three-dimensional velocity coordinates, with all components stored as double-precision floating-point numbers.<sup>[1](#works-cited)</sup> The Brutus output files store the integrated trajectories using a snapshot-based structure. Each snapshot initiates with a header line containing the simulation time, the number of bodies, and the computational CPU time, followed by the physical state vectors of the bodies. The file concludes with a summary line documenting the integration parameters, initial energy, final energy, and the relative energy error.<sup>[1](#works-cited)</sup>

Despite the rigorous generation pipeline, the dataset contains documented anomalies and structural gotchas that must be accounted for in the data loading mechanisms of the training loop. Numerical ID ranges for the files contain significant gaps, resulting from the non-contiguous allocation of IDs during generation, the rejection of files during the dynamic prescreening phase, and the subsequent removal of "problematic" initial conditions that failed to converge during the Brutus execution.<sup>[1](#works-cited)</sup> Furthermore, a notable discrepancy exists within the "gold standard" datasets. While the hierarchical gold-standard trajectories serve as a complete, high-resolution copy of the base initial conditions, the standard quasi-random gold-standard dataset inexplicably excludes exactly 184 specific IDs that are present in the base set.<sup>[1](#works-cited)</sup> The dataloader driving the neural network must be programmed to dynamically handle these missing indices to prevent fatal iteration errors during batch construction.

<table><tr><td>Pipeline Component</td><td>Specification and Characteristics</td><td>Known Anomalies and Structural Notes</td></tr><tr><td>Stage 1: IC Generation</td><td>Sobol-based quasi-random and hierarchical sampling.</td><td>Raw IC storage is externalized; requires specific environment variables for pathing.</td></tr><tr><td>Stage 2: Prescreening</td><td>Dynamic stability filtering via adaptive thresholds.</td><td>Rejections create permanent numerical gaps in the sequential dataset IDs.</td></tr><tr><td>Stage 3: Integration</td><td>Brutus (Bulirsch-Stoer with arbitrary precision).</td><td>Integration failures are moved to a blacklist, furthering ID sequence fragmentation.</td></tr><tr><td>Stage 4: Metrics</td><td>Extraction of energy conservation and physical drift.</td><td>N/A</td></tr><tr><td>Data Schema (Input)</td><td>3 lines per file. Format: mass x y z vx vy vz.</td><td>Standard ICs use fixed mass of 1.0; hierarchical ICs vary but normalize total mass to 3.</td></tr><tr><td>Gold Standard Sets</td><td>High-resolution (dt_out = 0.01) trajectories.</td><td>Quasi-random gold standard is missing 184 files compared to the base dataset.</td></tr></table>

# The Architectural Mismatch: Causal Training Versus Global Optimization

The most severe structural pathology in the current methodology is the fundamental conflict between causal training principles and global Augmented Lagrangian enforcement. To successfully train a model on chaotic dynamics, the loss landscape must be carefully managed to prevent the network from converging to unphysical local minima.

# The Failure of Global Optimization in Chaotic Systems

Standard Physics-Informed Neural Networks evaluate physics residuals globally across the entire spatio-temporal domain simultaneously. They achieve this by uniformly or adaptively sampling collocation points across the domain and minimizing the aggregate error.<sup>[3](#works-cited)</sup>In systems governed by linear or mildly non-linear partial differential equations, this global approach is highly effective. However, in chaotic dynamical systems, this approach fails catastrophically.<sup>[5](#works-cited)</sup>

Chaotic trajectories exhibit an extreme sensitivity to initial conditions, characterized quantitatively by the Lyapunov time. Errors in predicting the system's state at an early time propagate and amplify exponentially as time advances. If a standard optimizer attempts to minimize a physics residual at a late time $t = T$ before the trajectory has been accurately resolved at an early time $t = 0$, it forces the network to learn based on erroneous, unphysical gradients.<sup>[1](#works-cited)</sup> The network essentially attempts to satisfy the governing equations based on a completely fabricated intermediate state, leading to a phenomenon known as temporal causality violation.<sup>[1](#works-cited)</sup>

# The Mechanics of Causal Training

To counteract this fatal vulnerability, recent advancements in deep learning for physical systems have introduced the concept of Causal Training. The proposed data quality assessment protocol leverages this mechanism by applying a dynamic, exponential weighting

function to the loss calculated at each time step.<sup>[1](#works-cited)</sup> The weighted loss is expressed mathematically as the sum of the product of the weights and the individual step losses. The crucial component is the weight adjustment formula, where the weight for a given time step is proportional to the exponential of the negative sum of all preceding losses, multiplied by a causal strictness parameter.<sup>[1](#works-cited)</sup>

This formula strictly enforces the "arrow of time." The loss weight for a future time step only becomes non-zero once the cumulative error of all preceding time steps has been minimized to a negligible value. By forcing the network to resolve the trajectory sequentially, the gradients backpropagated from late-time residuals are guaranteed to be physically meaningful, as they are anchored by an accurate historical trajectory.<sup>[1](#works-cited)</sup>

# The Augmented Lagrangian Method (ALM)

Conversely, the SQR-SkipResNet architectural blueprint dictates the use of the Augmented Lagrangian Method (ALM) to balance the multi-objective loss function.<sup>[1](#works-cited)</sup> The total loss is a composite of data fidelity, physics adherence, and energy conservation. The ALM framework controls the influence of the physics residual adaptively by utilizing a Lagrange multiplier and a quadratic penalty term.<sup>[1](#works-cited)</sup>

Following each optimization step, these ALM parameters are updated algorithmically. The Lagrange multiplier is updated via gradient ascent, naturally increasing the penalty when the physics residual is large. The penalty coefficient is updated using a robust, RMSprop-inspired moving average of the squared physics loss evaluated over the entire set of collocation points.<sup>[1](#works-cited)</sup> This global mechanism dynamically equilibrates the competing loss terms without requiring manual hyperparameter tuning.<sup>[4](#works-cited)</sup>

# The Architectural Paradox and the Causal Firewall

The paradox between these two advanced methodologies lies in their optimization dynamics. The Augmented Lagrangian Method fundamentally requires a global view of the constraint violations across the entire spatio-temporal domain to adapt its penalty parameters smoothly and effectively.<sup>[1](#works-cited)</sup> Causal weighting, by its very mathematical definition, actively masks future constraint violations from the optimizer until the present moment is fully resolved.<sup>[1](#works-cited)</sup> Integrating both natively into the same loss graph results in an algorithmic deadlock.

When causal weighting is naively applied as a scalar multiplier over a global ALM sampling strategy, it induces a documented failure mode termed the "Causal Firewall".<sup>[1](#works-cited)</sup> In the context of N-body dynamics, the system frequently experiences close encounters between celestial bodies. These pericenter passages create immense local curvature in the trajectory, manifesting numerically as a "stiffness spike".<sup>[1](#works-cited)</sup> If the network encounters an under-resolved stiffness spike at an early time, the local interpolation physics residual at that specific moment spikes dramatically.<sup>[1](#works-cited)</sup>

Consequently, the loss term for that specific moment becomes overwhelmingly large. The

exponential nature of the causal weight formula instantly reacts to this cumulative error spike, driving the weights for all subsequent future time steps effectively to zero.<sup>[1](#works-cited)</sup> This creates an impenetrable firewall. The gradients for any network parameters responsible for late-time behavior vanish entirely.<sup>[1](#works-cited)</sup>

Because the future errors are artificially multiplied by zero, the global ALM mechanism calculates a deceptively low overall variance for the physics residual. Thus, the ALM fails to increase the penalty parameter appropriately, as the masked global variance appears artificially stable. The network completely ceases to learn past the point of the close encounter, leaving the neurons responsible for future predictions in a state of random initialization or causing them to drift aimlessly. The model may perfectly memorize the smooth trajectory leading up to the close encounter, but it will flatline thereafter, entirely failing to simulate the chaotic scattering event.<sup>[1](#works-cited)</sup>

# Proposed Resolution: The Time-Windowed Causal-ALM Hybrid

To reconcile the sequential, time-respecting nature of causal training with the global stability and constraint-enforcement power of the Augmented Lagrangian Method, the standard unconstrained training loop must be abandoned. The resolution requires restructuring the optimization process into a Time-Windowed Causal-ALM Hybrid, drawing theoretical inspiration from recent advancements in constrained optimization for continuous-time physics models.<sup>[4](#works-cited)</sup>

Instead of applying causal weights as a continuous exponential decay scalar on the residual across the entire global interval, the temporal domain is discretely partitioned into overlapping causal windows.

# Localized ALM Execution

Within each actively advancing time window, the collocation points are sampled according to the local stiffness profile of the trajectory. The ALM parameters, specifically the Lagrange multiplier and the penalty coefficient, are initialized and iteratively updated purely locally for the data contained within this specific window. The loss function is evaluated as a localized composite of the data fidelity, the ALM-penalized physics residual, and the dynamically weighted energy conservation term.<sup>[1](#works-cited)</sup> By restricting the ALM's view to the current window, it is not artificially blinded by future causal weights, allowing the moving average of the squared physics loss to accurately reflect the true local constraint violations.<sup>[1](#works-cited)</sup>

# Causal Gating Mechanism

The causal weight formula is fundamentally redefined. It is no longer utilized as a soft multiplier on the loss gradients. Instead, causality acts as a hard algorithmic gating mechanism governing the transition between the partitioned time windows. The Adam optimization algorithm is strictly restricted to operating within the current active window until the ALM-penalized total residual for that window falls below a predefined, stringent causal tolerance threshold.<sup>[7](#works-cited)</sup>

Only when the neural network has successfully learned the dynamics within the current temporal segment, satisfying the Hamiltonian constraints enforced by the ALM, does the causal gate unlock.

# Structural State Propagation

Once the gating mechanism confirms the convergence of the current window, the temporal horizon expands. The network's finalized prediction at the end of the converged window acts as a hard initial condition constraint for the subsequent window, ensuring perfect continuity of the learned manifold.<sup>[4](#works-cited)</sup> The ALM penalty multipliers are carried forward into the next window to maintain optimization momentum.

Crucially, the causal masking of the deep future is achieved by structurally excluding any data points or collocation points beyond the active window from the current training batch. This architectural modification entirely prevents the Causal Firewall effect. Because future, highly chaotic close encounters are simply not passed to the optimizer until the preceding trajectory is mastered, they cannot trigger the exponential error spikes that cause gradient death.<sup>[1](#works-cited)</sup> This hybrid approach preserves the rigorous, hard-constraint enforcement capabilities of the Augmented Lagrangian while strictly respecting the causal arrow of time dictated by the physics of the system.

# Rectification of Architectural and Dataset Inconsistencies

Beyond the fundamental algorithmic mismatch, the provided protocol documents exhibit significant parameter inconsistencies that threaten to derail the training pipeline. These contradictions span the dimensionality of the input vectors, the numerical scaling of regularizing constants, the geometric reference frames, and the temporal sampling rates. They must be definitively resolved based on the physical constraints of the three-body problem and the inductive biases inherent to the SIREN architecture.

# Input Vector Dimensionality: Reconciling the 12D and 14D Paradigms

The neural network's architecture acts as a conditional generator. It takes a description of the system's initial state and a specific time, and outputs the physical coordinates of the bodies at that time. However, the documents conflict on how this initial state should be represented. The architectural blueprint specifies a 14-dimensional conditional input vector, comprising 3 masses, 5 physical invariants, and 5 values mapping 3 trigonometrically encoded angles.<sup>[1](#works-cited)</sup> Conversely, the curriculum training plan outlines a 12-dimensional vector, replacing the trigonometric angles with 3 shape invariants and a normalized moment of inertia scalar.<sup>[1](#works-cited)</sup>

The 14-dimensional formulation utilizing trigonometric angles is physically flawed for chaotic systems. Trigonometric representations of spatial orientation are inherently susceptible to coordinate singularities, commonly known as gimbal lock. During chaotic scattering events, the orbital plane of the interacting bodies can shift abruptly and violently. If the system's orientation aligns with the poles of the chosen coordinate system, the trigonometric derivatives explode, injecting undefined or massive gradients into the network's initial layers, instantly destabilizing the optimization process.<sup>[8](#works-cited)</sup>

In contrast, the 12-dimensional formulation utilizes universal Shape Invariants. These invariants are derived mathematically from the sorted mutual distances between the three bodies, representing the lengths of the shortest, middle, and longest sides of the triangle formed by the masses.<sup>[1](#works-cited)</sup> Shape invariants possess exceptional mathematical properties for machine learning: they are universally continuous, entirely non-singular, and intrinsically invariant to global spatial rotations. They perfectly describe the internal geometric configuration of the N-body system without relying on an arbitrary external reference frame.<sup>[1](#works-cited)</sup>

However, simply adopting the 12-dimensional vector breaks the meticulously designed initialization scheme of the SIREN architecture. The SIREN's first layer maps the input vector to a high-dimensional space of Fourier features. This mapping is governed by a highly specific frequency parameter initialized at a value of 30.<sup>[1](#works-cited)</sup> This parameter was mathematically derived and tuned specifically for the spectral bandwidth of a 14-dimensional input space.<sup>[1](#works-cited)</sup> Reducing the input dimensionality to 12 alters the frequency density, severely blunting the network's ability to overcome spectral bias.

To resolve this, the input vector must be standardized into an Augmented 14-Dimensional Shape-Invariant Vector. This formulation retains the superior physical properties of the shape invariants while completing the parameter space to satisfy the architectural constraints of the SIREN initialization. The final vector comprises:

1. Temporal Dimension: 1 component representing normalized simulation time.

2. Mass Distribution: 3 components for the normalized masses of the bodies.

3. Physical Invariants: 5 components quantifying the system's energy, virial ratio, minimum separation, angular momentum, and moment of inertia.

4. Universal Shape Invariants: 3 components defining the internal geometry of the interaction triangle.<sup>[1](#works-cited)</sup>

5. Orientation Cosines: 2 components mapping the spatial orientation of the normal vector of the system's initial invariant plane relative to the universal z-axis.

By utilizing direction cosines instead of Euler angles, the formulation avoids trigonometric singularities entirely while simultaneously providing the neural network with the necessary global orientation context required to map the internal triangle shape to the final 9-dimensional output coordinate space.<sup>[1](#works-cited)</sup>

<table><tr><td>Vector Component</td><td>Variable Notation</td><td>Dimensionality</td><td>Physical Justification and Resolution</td></tr><tr><td>Category</td><td></td><td></td><td>Benefit</td></tr><tr><td>Time Mapping</td><td>t'</td><td>1D</td><td>Normalized to [−1, 1] to align with SIREN periodic activations.</td></tr><tr><td>Mass Distribution</td><td>m1, m2, m3</td><td>3D</td><td>Dimensionless representation of body mass ratios.</td></tr><tr><td>Physical Invariants</td><td>E, Q, smin, L, I</td><td>5D</td><td>Quantifies binding energy, stability, and scale without spatial dependence.</td></tr><tr><td>Internal Geometry</td><td>I1, I2, I3</td><td>3D</td><td>Continuous, singularity-free shape invariants replacing flawed Euler angles.</td></tr><tr><td>Spatial Orientation</td><td>cos θ, sin θ</td><td>2D</td><td>Provides global orientation context while avoiding gimbal lock singularities.</td></tr><tr><td>Total Conditional Input</td><td>Xinput</td><td>14D</td><td>Maintains SIREN frequency injection density (ω0 = 30).</td></tr></table>

# Gravitational Softening Constants: The Dual-Context Paradigm

The integration of Newtonian gravity into numerical simulations often requires a softening constant, epsilon $\epsilon$ , to prevent the inverse-square force law from diverging to infinity as the distance between two bodies approaches zero.<sup>[11](#works-cited)</sup> The documents present a severe contradiction regarding the magnitude of this constant. The ALM physics loss formulation requires a softening parameter of $\epsilon = 10^{-5}$<sup>[1](#works-cited)</sup>, whereas the protocol for calculating the initial physical invariants mandates an exponentially smaller value of $\epsilon = 10^{-10}$.<sup>[1](#works-cited)</sup>

Gravitational softening fundamentally alters the physics of the simulation. At distances smaller than the softening length, the interaction ceases to be purely Newtonian, effectively replacing point masses with finite-density kernels, such as Plummer spheres.<sup>[11](#works-cited)</sup> Using a large softening constant artificially prevents close encounters, altering the chaotic scattering dynamics and introducing an unphysical bias into the trajectory.<sup>[13](#works-cited)</sup>

A single softening constant cannot simultaneously serve both the static data validation requirements and the dynamic requirements of neural network gradient descent. Therefore, a strict Dual-Context Epsilon Strategy must be instituted.

Static Invariant Calculation ( ) $\epsilon = 10^{-10}$ : When calculating the fundamental invariants (such as Total Energy and Virial Ratio) from the initial conditions prior to training, the processing is performed on CPUs utilizing double-precision (float64) arithmetic.<sup>[1](#works-cited)</sup> In this context, the softening must be negligible. Utilizing $\epsilon=10^{-10}$ ensures that the calculated physical invariants accurately shadow the true mathematical properties of the unsoftened Hamiltonian without introducing macroscopic bias.<sup>[1](#works-cited)</sup>

Dynamic Loss Optimization ( $\epsilon_{soft} = 10^{-5}$ ): During the backpropagation phase, the network computes the physics residual and energy conservation terms. These operations are performed on GPUs utilizing single-precision (float32) arithmetic. If the distance between predicted bodies approaches zero during a simulated close encounter, the inverse-square term diverges rapidly.<sup>[1](#works-cited)</sup> In single-precision arithmetic, this immediately triggers a numerical overflow, generating infinite or NaN gradients. These exploding gradients will instantly shatter the SQR-SkipResNet skip connections, overwhelming even the stabilizing effects of Layer Normalization.<sup>[1](#works-cited)</sup> Consequently $\epsilon=10^{-5}$ must be strictly enforced as a neural network regularization parameter within the PyTorch/JAX loss functions.<sup>[1](#works-cited)</sup> The network is not learning softened physics; it is learning exact Hamiltonian dynamics regularized by a microscopic floor precisely calibrated to match the limits of its numerical precision.

<table><tr><td>Processing Context</td><td>Hardware &amp; Precision</td><td>Epsilon Value (€)</td><td>Justification and Role</td></tr><tr><td>Pre-Training Validation</td><td>CPU / float64</td><td>10-10</td><td>Ensures calculated invariants (Energy, Virial Ratio) reflect true Newtonian physics without introducing finite-kernel bias.</td></tr><tr><td>Backpropagation (ALM Loss)</td><td>GPU / float32</td><td>10-5</td><td>Acts as numerical regularization to prevent gradient explosion and NaN propagation across skip connections during close encounters.</td></tr></table>

# Frame Conventions: Mandating the Center of Mass Boost

A critical anomaly identified in the curriculum data framework reveals that the hierarchical Initial Conditions are not generated in the Center of Mass (COM) frame; they possess a non-zero total momentum. Conversely, the quasi-random datasets are generated strictly within the COM frame.<sup>[1](#works-cited)</sup> This presents a massive structural problem, as the PINN architecture explicitly assumes that all predicted output positions are natively in the COM frame.<sup>[1](#works-cited)</sup>

Training a deep neural network on datasets with varying, translationally shifting coordinate systems completely destroys the inductive bias of the model. If a hierarchical system drifts uniformly across the coordinate space due to a net momentum vector, the network will be forced to expend vast amounts of its parameter capacity attempting to learn a simple, linear coordinate transformation, severely degrading its ability to learn the complex, underlying nonlinear gravitational dynamics.

To rectify this, an aggressive, automated Galilean boost must be mandated during the data preprocessing phase.<sup>[1](#works-cited)</sup> Before any physical invariants are calculated or any state vectors are scaled to dimensionless units, the pipeline must compute the system's global center of mass vector and velocity vector. All initial positions and velocities must then be mathematically transformed by subtracting these global vectors, perfectly centering the system. Only after this strict Galilean transformation is applied should the original, drifting coordinate references be discarded. This ensures that the injectivity of the augmented 14-dimensional input vector is perfectly preserved and that all training data uniformly aligns with the geometric output assumptions of the neural network.<sup>[1](#works-cited)</sup>

# Temporal Resolution: Bridging the Sampling Divide

The data pipeline utilizes a mixed temporal resolution scheme. The baseline datasets (Sets 1a and 1b) are integrated with a dt_out of 0.08 and 0.17, respectively.<sup>[1](#works-cited)</sup> However, Stages 2 and 5 of the curriculum mandate the use of high-resolution datasets (Sets 2a and 2b), which feature an 8-fold to 17-fold increase in temporal density, outputting at dt_out $= 0.01$.

Using a coarse temporal resolution of $dt = 0.17$ for a highly chaotic orbit is physically disastrous. During a close encounter, a pericenter passage may occur entirely between two discrete data points. The SIREN network, characterized by its continuous, infinitely differentiable nature, will attempt to fit a smooth mathematical spline through these widely spaced points.<sup>[1](#works-cited)</sup> Because the true physical path of the close encounter is highly curved and unrecorded, the network's interpolation will violently violate the conservation of energy. This massive physical violation will instantly inflate the ALM physics penalty term and artificially trigger the Causal Firewall, halting training.

The dt_out parameter is not merely a data logging convenience; it represents the Nyquist frequency of the physical simulation. The low-resolution integrations (0.08 and 0.17) are only physically permissible for the earliest stages of the curriculum (Stages 0, 1a, and 1b) because these specific hierarchical systems are selected for being highly stable, with deeply bound energy $E < -0.5$) and wide initial separations $s_{min} > 2$).<sup>[1](#works-cited)</sup> Their orbital velocities are relatively low, ensuring that the continuous interpolation between the coarse data points remains physically valid.

However, for any trajectory entering the chaotic regimes of Stages 3 through 6, the high-resolution integration of dt_out $= 0.01$ is strictly mandatory.<sup>[1](#works-cited)</sup>  If a trajectory from the low-resolution set exhibits a close encounter or significant velocity spike during pre-screening, it must be automatically rejected by the data validation protocol and specifically routed back to the Brutus integrator to be resampled at $dt = 0.01$ before it is permitted to enter the training loop.<sup>[1](#works-cited)</sup>

<table><tr><td>Curriculum Stage</td><td>Dynamic Regime</td><td>Allowed Base Resolution (dt_out)</td><td>Justification for Temporal Density</td></tr><tr><td>Stage 0 &amp; 1</td><td>Highly Stable (Keplerian)</td><td>0.08 _ 0.17</td><td>Low orbital velocities and wide separations (smin &gt; 2) prevent interpolation errors between coarse sampling points.</td></tr><tr><td>Stage 2</td><td>Stable Refinement</td><td>0.01</td><td>High-resolution data is used to polish the network's continuous representation of learned stable dynamics.</td></tr><tr><td>Stage 3 - 6</td><td>Chaotic / Close Encounters</td><td>0.01 (Strict)</td><td>High density is mandatory to prevent spectral aliasing and infinite gradients during rapid pericenter passages.</td></tr></table>

# Evolution of Pre-Training Data Validation Metrics

To support the Time-Windowed Causal-ALM Hybrid architecture and enforce the rectified dataset parameters, the four static and dynamic data quality metrics must be mathematically updated. These metrics must transition from being simple diagnostic flags into fundamental, governing parameters of the training loop.

# Symplectic Conservation Score (SCS)

The Symplectic Conservation Score originally measured the maximum normalized deviation of the Hamiltonian over the duration of the numerical trajectory.<sup>[1](#works-cited)</sup> In the updated framework, the SCS serves as the primary, non-negotiable filter against Brutus integration errors before the data is passed to the ALM. Because the Augmented Lagrangian Method explicitly incorporates an energy regularizer to optimize for global conservation 1, feeding the network data that contains intrinsic, numerical integration drift creates an unsolvable optimization paradox.

The metric is mathematically defined using the unsoftened static epsilon: $\epsilon = 10^{-10}$ ):

Any trajectory resulting in an $SCS > -6$ must be outright rejected during Phase 1 static $SCS > -6$ screening.<sup>[1](#works-cited)</sup> For the high-resolution Stage 5 data targeting complex chaotic orbits ( $dt = 0.01$ ), the threshold must be tightened to $SCS < -8$. This strict gating ensures that the neural $SCS < -8$ network learns the pure symplectic geometry of the Hamiltonian flow rather than inadvertently memorizing the numerical dissipation of the integrator.

# Stiffness-Aware Sampling Density (SASD)

The SASD metric quantifies the ratio of the discrete time step to the local characteristic timescale of the system's dynamics, effectively measuring local trajectory curvature.<sup>[1](#works-cited)</sup> In the hybrid architecture, SASD directly arbitrates the dt_out mismatch and fundamentally dictates the ALM collocation point sampling density.<sup>[1](#works-cited)</sup>

The formulation compares the time step to the ratio of velocity and acceleration:

$$
SASD_{i} = \Delta t_i \cdot \frac{||a(t_{i})||}{||v(t_{i})||}
$$

If the maximum SASD of a low-resolution trajectory exceeds a critical threshold, it implies that the trajectory turns significantly between data points. Such data must be flagged and resampled to the higher resolution standard.<sup>[1](#works-cited)</sup> More importantly, during the Causal-ALM training loop, the probability distribution for selecting synthetic collocation points is no longer uniform. Instead, the sampling is strictly weighted by the SASD profile of the target trajectory.<sup>[15](#works-cited)</sup> This targeted

sampling ensures that the ALM penalty parameter $\mu_p$ applies the strongest mathematical constraints precisely at the points of highest curvature, effectively neutralizing the inherent spectral bias of the neural network.<sup>[1](#works-cited)</sup>

# Interpolation Physics Residual (IPR)

The Interpolation Physics Residual evaluates whether the continuous manifold implied by the discrete data points satisfies Newton's laws. It tests a piecewise Cubic Hermite Interpolating Polynomial against the underlying equations of motion.<sup>[1](#works-cited)</sup> In the new architecture, the IPR transitions from a mere pre-training check to establishing the theoretical lower bound for the ALM physics penalty.

The residual is calculated over synthetic points $\tau_k$, but crucially, it must be evaluated using the network's dynamic softening constant ($\epsilon = 10^{-5}$) rather than the static constant 1 :

$$
IPR = \frac{1}{M} \sum_{k=1}^{M} \left| \frac{d^{2} q_{spline}}{dt^{2}} (\tau_k) - F_{gravity}^{\epsilon = 10^{-5}} (q_{spline}(\tau_k)) \right|^{2}
$$

This updated IPR value sets the noise floor for the ALM. If the neural network's internal physics loss drops below the pre-calculated IPR of the dataset, it indicates that the SIREN architecture has discovered a more physically accurate continuous trajectory than standard spline interpolation can provide. At this threshold, the ALM algorithms halt any further increases to the penalty parameter $\mu_p$<sup>[1](#works-cited)</sup>, preventing overfitting to numerical noise and signaling the optimizer to shift from exploration to high-precision refinement.<sup>[1](#works-cited)</sup>

# Phase Space Coverage Entropy (PSC)

Chaotic systems possess ergodic properties, meaning trajectories explore vast regions of phase space over time. The PSC metric calculates the Shannon entropy of the data points distributed across a discretized phase space grid, quantifying the diversity of the training data.<sup>[1](#works-cited)</sup> In the updated protocol, PSC governs the "Curriculum Replay" mechanism.<sup>[1](#works-cited)</sup>

As the training progresses from the stable early stages into the fully chaotic regimes (Stages 4 through 6), the replay buffer must not be overwhelmingly biased toward the highly stable, low-entropy data of Stage 0. Instead of utilizing uniform random sampling to construct the replay batches, trajectories are sampled inversely proportional to their phase space bin density. This entropy-guided sampling guarantees that extreme, high-stiffness events (such as configurations where $s_{min} < 0.5$ ) are consistently over-represented in the mini-batch.<sup>[1](#works-cited)</sup> Forcing the ALM to constantly evaluate gradients across both smooth quasi-periodic regions and high-frequency chaotic scattering regions simultaneously stabilizes the momentum parameters of the Adam optimizer, ensuring robust convergence.<sup>[1](#works-cited)</sup>

<table><tr><td>Validation Metric</td><td>Mathematical Focus</td><td>Role in the Time-Windowed Causal-ALM Hybrid Framework</td></tr><tr><td>SCS</td><td>Hamiltonian Deviation</td><td>Hard gate against integrator drift. Prevents ALM energy regularizer from failing due to flawed ground truth.</td></tr><tr><td>SASD</td><td>Curvature vs. Step Size</td><td>Dictates adaptive collocation sampling. Forces ALM penalties to focus on "stiffness spikes" during close encounters.</td></tr><tr><td>IPR</td><td>Continuous Spline Residual</td><td>Establishes the absolute noise floor for the physics loss, signaling the transition from Adam to L-BFGS refinement.</td></tr><tr><td>PSC</td><td>Phase Space Shannon Entropy</td><td>Governs the Curriculum Replay buffer. Ensures chaotic scattering events are over-represented to maintain gradient stability.</td></tr></table>

# The Synthesized Curriculum Training Protocol

By resolving the architectural mismatches, enforcing strict dataset conventions, and redefining the validation metrics, we can synthesize a unified, step-by-step implementation protocol. This workflow perfectly integrates the static data validation strategy with the advanced ALM-backed SQR-SkipResNet and the multi-stage curriculum progression.

Phase 1: Static Pre-Screening and Data Transformation (CPU Operations) The pipeline initiates by ingesting the raw initial conditions from the external storage directories. An automated Galilean boost is immediately applied to all vectors, strictly enforcing the Center of Mass coordinate system.<sup>[1](#works-cited)</sup> Any configuration violating momentum conservation post-boost is permanently discarded. Subsequently, the physical invariants, including the critical universal shape invariants $$(I_1, I_2, I_3)$$ , are computed using the unsoftened static constant ( $\epsilon = 10^{-10}$ ) to ensure true Newtonian fidelity.<sup>[1](#works-cited)</sup> The augmented 14-dimensional input vector is then assembled for each trajectory.<sup>[1](#works-cited)</sup> Finally, the metric gating process computes the Symplectic Conservation Score and the Stiffness-Aware Sampling Density profile. Trajectories exhibiting unacceptable integration drift or severe undersampling relative to their temporal resolution are flagged for high-precision resampling by the Brutus integrator.<sup>[1](#works-cited)</sup>

Phase 2: Curriculum Stage Initialization and IPR Bounding The validated trajectories are stratified into the seven primary curriculum stages (0 through 6) based on their binding energy, angular momentum ratios, and specifically their estimated Lyapunov time $(\tau_L)$ for the chaotic stages.<sup>[1](#works-cited)</sup> Prior to initiating the training loop for a specific stage, the Interpolation Physics Residual is computed for all active trajectories using the network's dynamic softening constant ($\epsilon = 10^{-5}$). This calculation establishes the absolute convergence floor for the Augmented Lagrangian physics penalties.<sup>[1](#works-cited)</sup>

Phase 3: The Time-Windowed Causal-ALM Training Loop (GPU Operations) For each active curriculum stage, the dataloader constructs mini-batches using the Phase Space Coverage metric to ensure a balanced, entropy-guided distribution of stable and chaotic trajectories from the current and all preceding stages.<sup>[1](#works-cited)</sup> The temporal domain of the simulation is divided into discrete causal windows. Within the active window, the Adam optimizer executes the Augmented Lagrangian Method. The data fidelity loss is evaluated against the Brutus snapshots, while the physics loss is evaluated over adaptive collocation points mapped probabilistically by the SASD profile.<sup>[1](#works-cited)</sup> The ALM penalty multipliers are updated dynamically based solely on the local residual of the current window.<sup>[1](#works-cited)</sup> The optimization continues until the total window loss converges below the causal tolerance threshold. Only then does the causal gating mechanism unlock, structurally advancing the time window and allowing the neural network to perceive the subsequent segment of the trajectory.

Phase 4: Refinement and Stage Transition Once the sequential causal windows have expanded to encompass the entire time domain and the Adam optimizer has driven the loss down to the pre-calculated IPR noise floor, control is transferred to the Stochastic L-BFGS optimizer.<sup>[1](#works-cited)</sup> This quasi-Newton method polishes the global solution to high precision. Gradient clipping, which is essential during the Adam phase to survive close encounters, is disabled during L-BFGS refinement to preserve the mathematical integrity of its line-search trust region.<sup>[1](#works-cited)</sup> Before advancing to the next, more complex curriculum stage, the protocol verifies that the network's inherent Hamiltonian prediction maintains a relative energy drift of less than $10^{-4}$ .<sup>[1](#works-cited)</sup> The curriculum then increments, drastically increasing the energy penalty weight dictated by the ALM schedule, thereby hardening the physical constraints as the neural network wades deeper into the chaotic regime.

# Conclusion

The chaotic Three-Body Problem cannot be accurately simulated by deep neural networks that treat time merely as a bulk spatial dimension, nor can it be resolved by sequential solvers that fail to strictly enforce global, long-term conservation laws. The initially documented approaches for this architecture presented a severe, fundamental mismatch: causal training forced a strict temporal masking that paralyzed future gradients, while the Augmented Lagrangian Method required global variance evaluation across the entire manifold to function.

By restructuring the framework into a Time-Windowed Causal-ALM Hybrid, this analysis successfully reconciles the methodologies. Causal learning now acts not as an exponential dampener, but as a rigid temporal gatekeeper, releasing overlapping, moving windows of time to the optimizer. Within these sequential windows, the Augmented Lagrangian Method aggressively enforces exact Newtonian mechanics via its dynamically scaling penalty multipliers.<sup>[4](#works-cited)</sup>

Furthermore, this exhaustive synthesis has rectified critical operational inconsistencies that would have otherwise led to catastrophic gradient failure. The input dimensionality has been definitively standardized as an Augmented 14-Dimensional vector that utilizes universal shape invariants, eliminating the threat of trigonometric singularities while preserving the frequency injection mapping required by the SIREN layers.<sup>[1](#works-cited)</sup> A strict dual-epsilon protocol ( $10^{-10}$ for static invariants, $10^{-5}$ for dynamic optimization) cleanly separates the requirement for ground-truth physical precision from the necessity of GPU network regularization.<sup>[1](#works-cited)</sup> The Center of Mass frame is now strictly enforced via Galilean pre-processing, ensuring geometric injectivity, and the sampling resolution is dynamically arbitrated by the underlying stiffness of the physics.<sup>[1](#works-cited)</sup>

By operationalizing the mathematically updated validation metrics (SCS, SASD, IPR, PSC) within this unified, highly structured curriculum protocol, researchers can guarantee that the vast computational investment required for arbitrary-precision N-body integration translates directly into a robust, physically plausible, and causality-respecting deep learning model.

# Works cited

1. main_CTL.pdf

2. Three-body problem - Wikipedia, accessed April 26, 2026, https://en.wikipedia.org/wiki/Three-body_problem

3. Respecting causality is all you need for training physics-informed neural networks - ar5iv, accessed April 26, 2026, https://ar5iv.labs.arxiv.org/html/2203.07404

4. Conditionally adaptive augmented Lagrangian method for physics-informed learning of forward and inverse problems using artificial neural networks - arXiv, accessed April 26, 2026, https://arxiv.org/html/2508.15695v1

5. Respecting causality is all you need for training physics-informed neural networks - arXiv, accessed April 26, 2026, https://arxiv.org/abs/2203.07404

6. Conditionally adaptive augmented Lagrangian method for physics-informed learning of forward and inverse problems using artificia - arXiv, accessed April 26, 2026, https://arxiv.org/pdf/2508.15695?

7. Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective - arXiv, accessed April 26, 2026, https://arxiv.org/html/2502.00604v1

8. An Introduction to the Classical Three-Body Problem, accessed April 26, 2026, https://www.ias.ac.in/article/fulltext/reso/024/01/0087-0114

9. The Three-Body Problem and the Shape Sphere - UC Santa Cruz, accessed April 26, 2026, https://peopleweb.prd.web.aws.ucsc.edu/~rmont/papers/math_monthly_triangles.

10. [1402.0841] The Three-body problem and the shape sphere - arXiv, accessed April 26, 2026, https://arxiv.org/abs/1402.0841

11. What is Gravitational softening length? - Astronomy Stack Exchange, accessed April 26, 2026, https://astronomy.stackexchange.com/questions/50106/what-is-gravitational-sof tening-length

12. Gravitational softening as a smoothing operation - Astronomy in Hawaii, accessed April 26, 2026, https://home.ifa.hawaii.edu/users/barnes/research/smoothing/soft.pdf

13. [astro-ph/0011568] Towards optimal softening in 3D N-body codes: I. Minimizing the force error - arXiv, accessed April 26, 2026, https://arxiv.org/abs/astro-ph/0011568

14. Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - ResearchGate, accessed April 26, 2026, https://www.researchgate.net/publication/382109760_Power-Enhanced_Residual _Network_for_Function_Approximation_and_Physics-Informed_Inverse_Problems

15. Causality-guided adaptive sampling method for physics-informed neural networks - ResearchGate, accessed April 26, 2026, https://www.researchgate.net/publication/383701268_Causality-guided_adaptive_ sampling_method_for_physics-informed_neural_networks

