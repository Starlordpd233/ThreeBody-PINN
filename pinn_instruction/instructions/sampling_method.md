<div align="center">

# A Unified Pipeline for Generating High-Fidelity Three-Body Initial Conditions

</div>

Methodology Description

June 15, 2025

## Overview of the Data Generation Pipeline

[Critical Update: The script preserves virial ratio in hierarchical ICs (masses normalized consistently with velocities). For quasi-random, scaling is **enabled** in the main block with range (0.8, 1.2), which distorts the virial ratio by $s^{3}$—see documented warning in "Global Scaling (Optional)". The default would preserve it, but scaling is explicitly enabled for variety.]

Generating high-quality training data for a Physics-Informed Neural Network (PINN) tasked with solving the three-body problem is a non-trivial challenge. The chaotic nature of many three-body systems means that a significant fraction of randomly generated initial conditions (ICs) will lead to computationally expensive simulations that are ultimately unusable due to poor energy conservation.

To address this, we adopt a multi-stage pipeline designed to progressively filter and refine the set of initial conditions, ensuring that only the most promising candidates are passed to the high-precision integrator, Brutus. This pipeline consists of three main stages:

1. Stage 1: Hierarchical & Quasi-Random Sampling. We begin by generating a diverse set of initial conditions: an algorithm to generate hierarchical three-body systems; and another one using a quasi-random sampling method which adopts a Sobol sequence to ensure uniform coverage of the parameter space. This stage includes several enhancements to the baseline sampling method.

2. Stage 2: Pre-screening for Short-Term Stability. Before committing to a full Brutus simulation, we use a rapid, low-precision Leapfrog integrator to quickly assess the short-term stability of each IC. This step efficiently weeds out configurations that are guaranteed to become unstable.

3. Stage 3: Adaptive Brutus Parameterization. For the ICs that pass the pre-screening, we analyze their intrinsic properties (e.g., timescales, minimum separation) to assign them to different "regimes". Each regime is then simulated with a tailored set of Brutus parameters to balance computational cost with the required accuracy.

This document details the first two stages of this pipeline.

## Stage 1: Hierarchical Initial Conditions Generation

The hierarchical initial conditions (ICs) are generated using the `generate_stable_hierarchical_systems` algorithm implemented in the accompanying Python script. The procedure is:

1. Mass sampling: Draw the inner mass ratio $q_{\text{inner}} \sim U(0.1, 1.0)$ and outer mass ratio $q_{\text{outer}} \sim U(0.1, 2.0)$. Sample a base mass $m_{1} \sim U(m_{\text{min}}, m_{\text{max}})$ (default $m_{\text{min}}=0.5, m_{\text{max}}=1.5$). Set $m_{2}=q_{\text{inner}}m_{1}$, $m_{3}=q_{\text{outer}}(m_{1}+m_{2})$, then normalize $(m_{1}, m_{2}, m_{3})$ so that $m_{1}+m_{2}+m_{3}=3$.

2. Hierarchical separation ratio: Compute the Kozai-Lidov stability threshold

$$
\min_{\text{ratio}} = 2.8 \left(\frac{1 + q_{\text{outer}}}{1 + e_{\text{outer}}}\right)^{2/5} \quad (\text{with } e_{\text{outer}} \leq 0.5),
$$

then draw the hierarchy ratio $\mathcal{R} \sim U(\max(3, \min_{\text{ratio}}), 10)$.

3. Orbital elements: Sample inner semi-major axis $a_{\text{inner}} \sim U(0.1, 0.3)$, set $a_{\text{outer}}=\mathcal{R} a_{\text{inner}}$. Sample eccentricities $e_{\text{inner}}, e_{\text{outer}} \sim U(0, 0.3)$ and mean anomalies $M_{\text{inner}}, M_{\text{outer}} \sim U(0, 2\pi)$.

4. Radial distances and speeds: Compute

$$
r_{\text{inner}} = a_{\text{inner}} \left(1 - e_{\text{inner}} \cos M_{\text{inner}}\right), \quad v_{\text{inner}} = \sqrt{\frac{m_{1} + m_{2}}{r_{\text{inner}}}},
$$

$$
r_{\text{outer}} = a_{\text{outer}} \left(1 - e_{\text{outer}} \cos M_{\text{outer}}\right), \quad v_{\text{outer}} = \sqrt{\frac{m_{1} + m_{2} + m_{3}}{r_{\text{outer}}}}.
$$

5. Inclination perturbation: Draw a small inclination $\iota \sim U(0, 0.1)$ for the inner binary.

6. Position vectors:

$$
\mathbf{x}_{1} = -\frac{m_{2}}{m_{1} + m_{2}} r_{\text{inner}} \left(\cos \iota \hat{\mathbf{x}} + \sin \iota \hat{\mathbf{z}}\right),
$$

$$
\mathbf{x}_{2} = +\frac{m_{1}}{m_{1} + m_{2}} r_{\text{inner}} \left(\cos \iota \hat{\mathbf{x}} + \sin \iota \hat{\mathbf{z}}\right),
$$

$$
\mathbf{x}_{\text{COM}} = -\frac{m_{3}}{m_{1} + m_{2} + m_{3}} r_{\text{outer}} \hat{\mathbf{x}},
$$

$$
\mathbf{x}_{3} = +\frac{m_{1} + m_{2}}{m_{1} + m_{2} + m_{3}} r_{\text{outer}} \hat{\mathbf{x}}.
$$

Shift $\mathbf{x}_{1}, \mathbf{x}_{2}$ by $\mathbf{x}_{\text{COM}}$.

7. Velocity vectors:

$$
\mathbf{v}_{1} = \left(0, -\frac{m_{2}}{m_{1} + m_{2}} v_{\text{inner}}, 0\right), \quad \mathbf{v}_{2} = \left(0, \frac{m_{1}}{m_{1} + m_{2}} v_{\text{inner}}, 0\right),
$$

$$
\mathbf{v}_{\text{COM}} = \left(0, -\frac{m_{3}}{m_{1} + m_{2} + m_{3}} v_{\text{outer}}, 0\right), \quad \mathbf{v}_{3} = \left(0, \frac{m_{1} + m_{2}}{m_{1} + m_{2} + m_{3}} v_{\text{outer}}, 0\right).
$$

Add $\mathbf{v}_{\text{COM}}$ to each of $\mathbf{v}_{1}, \mathbf{v}_{2}$.

8. Gaussian perturbation: Add a small random perturbation drawn from $\mathcal{N}(0, 0.01)$ to each component of $\mathbf{x}_{i}$ and $\mathbf{v}_{i}$.

This procedure mirrors exactly the logic and parameter choices in `FINAL_ic_generator_enhanced.py`.

## Stage 2: Enhanced Quasi-Random Sampling

The foundation of our pipeline is a hybrid quasi-random sampling method designed to generate a diverse set of initial conditions for a planar, equal-mass three-body system.

### 1 Core Sampling Methodology

The fundamental idea is to fix one particle and sample the second from a well-defined space using a low-discrepancy sequence.

- Fix Particle 1: Particle 1 is fixed at $p_{1}=(1, 0, 0)$ on the unit sphere.
- Sample Particle 2: Particle 2, $p_{2}$, is sampled quasi-uniformly from the 3-D hemisphere defined by $\{x \leq 0, x^{2} + y^{2} + z^{2} \leq 1\}$.
- Set Particle 3: Particle 3 is set as $p_{3}=-(p_{1} + p_{2})$ to maintain the system's center of mass at the origin for the equal-mass case.

### 1.1 Low-Discrepancy Engine: Sobol Sequence

We use a Sobol sequence, a type of low-discrepancy sequence, to ensure that every finite batch of samples covers the parameter space evenly, minimizing both "clumping" and "voids".

- Dimension: A Sobol engine with base 6 dimensions (3 for position + 3 for velocity) is used, plus optional extras (e.g., 1 for global scaling if enabled via `scale_range`).
- Scrambling: Scrambling is enabled (e.g., `qmc.Sobol(scramble=True)`). This feature preserves the determinism and uniformity of the sequence while breaking up any residual lattice artifacts that could introduce bias.

### 1.2 Mapping Sobol Numbers to Physical Coordinates

The quasi-random numbers $(u_{1}, u_{2}, \dots) \in (0, 1)^{d}$ generated by the Sobol engine must be mapped to the desired physical coordinates.

#### Direction on the Unit Sphere

1. The polar angle $\theta$ is set using the transformation $\cos \theta = 1 - 2u_{1}$, which ensures a uniform distribution with respect to the solid angle.
2. The azimuthal angle is set as $\phi = 2\pi u_{2}$.
3. To enforce the $x \leq 0$ constraint, we mirror points that fall in the wrong hemisphere by replacing $\phi$ with $(\phi + \pi) \pmod{2\pi}$, which preserves uniformity without resorting to inefficient rejection sampling.

#### Radial Distance and Scaling

- The radial distance $r$ is calculated from $u_{3}$ using the cube root, $r = u_{3}^{1/3}$, to ensure the sample is uniform by volume.

#### Global Scaling (Optional)

An optional global scaling factor $s$ can be applied to all positions and velocities for added variety in system size. It uses an additional Sobol dimension, mapping $u_{4}$ to a user-defined range $[s_{\min}, s_{\max}]$ (default: [1.0, 1.0], disabling it) via $s = s_{\min} + (s_{\max} - s_{\min})u_{4}$. For example, the script's main block enables it with [0.8, 1.2] for quasi-random generation.

When enabled, positions scale by $s$ and velocities by $s$. Impact on Virial Ratio: This changes $Q = 2T / |U|$ by a factor of $s^{3}$ (kinetic energy scales as $s^{2}$, potential as $s^{-1}$). Disable if preserving virial equilibrium is required.

#### Velocity Sampling

The next three Sobol coordinates $(u_{4}, u_{5}, u_{6})$ are mapped to a 3D velocity vector $\mathbf{v}$ using inverse transform sampling from a normal distribution with mean 0 and standard deviation $\sigma = \text{velocity\_scale}$ (default 0.1):

$$
v_{i} = \Phi^{-1} \left(u_{3+i}; \mu = 0, \sigma = \text{velocity\_scale}\right), \quad i = 1, 2, 3.
$$

The sampler then enforces total momentum conservation by adjusting the velocity of the fixed particle so that $\sum_{i} m_{i} \mathbf{v}_{i} = 0$.

### 2 Enhancements to the Sampling Algorithm

To improve the quality and diversity of the generated ICs, we introduce the following enhancements.

#### 2.1 Sampling Non-Zero Initial Velocities

In this implementation, initial velocities for free particles are always sampled from a normal distribution using the inverse CDF and Sobol numbers. We can sample initial velocities using additional dimensions from the Sobol sequence.

- Required Dimensions: Sampling a 3D velocity vector for each of the two free particles would require 6 additional Sobol dimensions. However, we can sample velocities for just one particle and derive the others from physical constraints (e.g., total momentum).
- Velocity Sampling Strategy: A simple approach is to sample each velocity component from a normal distribution, where the Sobol coordinates are mapped to the normal distribution using the inverse transform sampling method (quantile function). The standard deviation of this distribution becomes a tunable hyperparameter.

#### 2.2 Initial Collision Avoidance: The Role of $\epsilon$

The sampling script includes a safeguard to reject any sample where the pairwise distance between any two bodies falls below a prescribed threshold, $\epsilon$.

- Purpose: The primary role of $\epsilon$ at this stage is to provide a quick, computationally cheap check to avoid immediate singularities and clear-cut unstable configurations.
- Setting $\epsilon$: This value is set to be 0.05 in the implementation. This ensures that obviously problematic ICs are discarded immediately, saving the cost of even a fast Leapfrog integration.

#### Recommended Scale

If Stage 2 Leapfrog test flags approaches below 0.10, pick $\epsilon \approx 0.05$. Starting from 0.01 is not wrong, but it may leave many obviously-bad ICs for the next stage, increasing the pre-screening burden. Conversely, too large an $\epsilon$ biases the spatial distribution by carving out a forbidden core.

#### Practical Strategy

- Begin with $\epsilon \approx 0.05$
- Monitor the rejection ratio during Stage 1. If < 1% of proposals are rejected, you can afford to tighten $\epsilon$ a bit; if > 30% are rejected and most would also fail Stage 2 anyway, loosen it.
- Keep $\epsilon$ fixed once you are satisfied; later tuning has diminishing returns because Stage 2 already provides a dynamic safety net.

## Stage 3: Pre-Screening of Generated ICs for Short-Term Stability

The ICs generated in Stage 1 are diverse but may still contain many that are dynamically unstable. Running these through the high-precision Brutus integrator is computationally wasteful. Therefore, Stage 2 acts as an essential intermediate filter.

### 3 The Pre-Screening Rationale

#### Implementation Details

- Integration parameters: The Leapfrog integrator runs with a fixed step size `dt = 0.0001` over a total duration of `t_max = 1.0`.
- Energy error threshold: `ENERGY_ERROR_THRESHOLD = 0.01` (i.e., 1%).
- Minimum separation threshold: `MIN_DISTANCE_THRESHOLD = 0.01`.
- Virial ratio bounds: Defaults to `VIRIAL_RATIO_MIN = 0.001` and `VIRIAL_RATIO_MAX = 2.0`, with optional percentile-based adaptive thresholds when `USE_PERCENTILE_THRESHOLDS = True`.
- Angular momentum filter: Disabled by default (`MIN_ANGULAR_MOMENTUM = 0.0`); can be enabled or set adaptively via percentiles.
- Dataset handling: The script loops over both hierarchical and quasi-random sampling directories and skips already-processed IC files based on recorded hashes.

The pre-screening script uses a fast, low-precision N-body integrator (a JIT-compiled Leapfrog integrator) to simulate each IC for a short period (e.g., $t_{\max}=1.0$). Its goal is not to produce an accurate trajectory but to quickly identify ICs that exhibit signs of instability, such as:

- Rapid energy non-conservation.
- Extremely close encounters between particles during the short simulation.

### 4 Pre-Screening Criteria

The pre-screening script evaluates each IC against several criteria to determine its stability. An IC must pass all these checks to be considered "stable" and move on to Stage 3.

1. Short-Term Energy Conservation: The script calculates the relative energy error, $|(E_{\text{current}} - E_{\text{init}}) / E_{\text{init}}|$, during the Leapfrog integration. If this error exceeds a modest threshold (e.g., 1%), the IC is flagged as unstable.
2. Dynamic Minimum Separation: The script tracks the minimum separation between any two bodies throughout the short integration. If this distance ever drops below a hardcoded threshold (e.g., 0.01), the IC is immediately rejected as it indicates a close encounter that Brutus would struggle with.
3. Virial Ratio: The script filters for ICs with $Q = 2T / |U|$ within the default bounds $0.001 \leq Q \leq 2.0$, or uses percentile-based adaptive thresholds when enabled.
4. Angular Momentum: Optionally filters for ICs with total angular momentum $|\sum_{i} m_{i} \mathbf{r}_{i} \times \mathbf{v}_{i}|$ above `MIN_ANGULAR_MOMENTUM` (default 0.0), or using adaptive percentile thresholds if enabled.
5. Adaptive Threshold Computation: To enhance the robustness and adaptability of the pre-screening filters, adaptive thresholds for Virial Ratio and Angular Momentum are computed based on a representative subset of the dataset. The sample size for adaptive threshold calculation is dynamically set to ensure statistical robustness:

$$
\text{sample\_size} = \min(1000, \max(200, |0.05 \times \text{total\_files}|))
$$

Thresholds are determined using percentile-based computations from these samples:
- Virial Ratio thresholds: between the `VIRIAL_PERCENTILE_MIN` and `VIRIAL_PERCENTILE_MAX` percentiles.
- Minimum Angular Momentum threshold: `ANGULAR_PERCENTILE_MIN` percentile (optional).

### 5 A Coordinated Strategy for Minimum Distance

It is crucial to understand the distinct but complementary roles of the minimum distance parameters across the pipeline:

- `epsilon` (in Stage 1 - Sampling): This is a static, initial filter. It is applied once to the $t=0$ configuration. Its purpose is to perform a cheap rejection of ICs that are "born" in a near-collision state.
- `min_distance_threshold` (in Stage 2 - Pre-screening): This is a dynamic, short-term filter. It checks for close encounters that occur during the brief Leapfrog integration. An IC might have a perfectly acceptable initial separation but be on an immediate collision course, which this check will catch. It is a more robust filter than the static `epsilon`.
- `min_sep` (in Stage 3 - Adaptive Brutus): This is not a filter, but a diagnostic metric. For the ICs that have passed the first two stages, this value (calculated from the initial state) is used to categorize the system into a specific regime (e.g., "standard," "hierarchical," "close_low_L"). This categorization then determines the precise (and often very stringent) Brutus parameters that will be used for the final, high-fidelity simulation.

By using these three parameters in a coordinated fashion, we create an efficient and intelligent pipeline that maximizes the quality of the final dataset while minimizing wasted computational resources.

### 6 Execution and Final Quality Control

The provided scripts facilitate the automation of this entire stage, creating a master script to run all generated simulations in parallel. After the simulations are complete, a final quality control check is essential. This involves parsing the Brutus output to:

1. Verify Energy Conservation: Confirm that the relative energy error $|\Delta E / E|$ remains below the target threshold (e.g., $10^{-4}$) for the entire duration of the simulation.
2. Check Momentum Conservation: Ensure the total momentum of the system remained close to zero.
3. Confirm Completion: Check that the simulation ran to the specified $t_{\text{end}}$ without premature termination.

Only the data from simulations that pass this final, rigorous quality control check should be considered "gold standard" data, suitable for training a high-fidelity PINN.