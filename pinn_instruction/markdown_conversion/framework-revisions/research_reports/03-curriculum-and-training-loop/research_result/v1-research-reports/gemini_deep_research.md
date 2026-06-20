# Adjudication Report: Curriculum and Training Loop (CTL) Revision for the Three-Body PINN Framework

## Adjudication Framework and Epistemological Baselines

The formulation of a Curriculum and Training Loop (CTL) for a Physics-Informed Neural Network (PINN) designed to model the extreme chaotic dynamics of the three-body problem necessitates absolute rigor in managing multi-fidelity data, physical invariants, and gradient optimization protocols.[1] The present adjudication targets the "doc-03" framework revision, addressing profound structural contradictions between diverse documentation branches.[1] To systematically isolate architectural truths from uncalibrated design hypotheses, this evaluation operates under a strict, non-negotiable hierarchy of evidentiary precedence.

The adjudication architecture strictly invalidates the authority of live implementation code and issue documentation when they conflict with finalized framework specifications or historically locked mathematical boundaries.[1] The overarching constraints dictate that the framework specifications—primarily encompassing `ctl_instruction.md` and `pinn_architecture.md`—function as the singular, unyielding source of truth.[1] The non-authoritative issue document (`03-curriculum-and-training-loop.md`) and its associated resolution proposals are treated strictly as auditing materials requiring rigorous adjudication, rather than serving as authoritative implementation manuals.[1] Consequently, any invocation of live implementation scripts, such as `data-processing-pipeline-full.py` or `basic_architecture.py`, is unilaterally overridden by the written specifications, reflecting the principle that live code often harbors technical debt or unverified experimental branches that have not survived formal peer scrutiny.[1]

Furthermore, all architectural reasoning operates entirely beneath the boundary conditions established by the "SCOPE-12" hard constraints.[1] These constraints define locked mathematical outcomes from previous v1.4 and v1.5 validation phases, which cannot be reopened, contradicted, or renegotiated.[1] Any findings, stage transitions, batch constructions, or loss-scaling dynamics that form the "revisable baseline" must be mapped strictly within these fixed boundaries.[1]

A critical component of this epistemological framework is the treatment of numerical figures, population metrics, and transition thresholds. To maintain empirical integrity, all figures are presumed to be unverified claims unless they are actively backed by a committed dataset verdict logged within the formal verification pipeline.[1]

| Data Classification Paradigm | Treatment Protocol | Evidentiary Requirement |
|---|---|---|
| **SCOPE-12 Hard Constraints** | Immutable. All derivations must reconcile under these parameters. | Explicitly codified in `scope-12-hard-constraints.md` (e.g., 14D input, raw-mass length scale). |
| **Framework Specifications** | Authoritative baseline. Subject to revision only via formal adjudication of open research questions. | Present within `ctl_instruction.md` or `pinn_architecture.md`. |
| **Claimed-Unverified Figures** | Treated as untested design hypotheses. Excluded from foundational mathematical derivations. | Labeled `claimed-unverified` in the claims register (e.g., specific epoch tables, stage trajectory populations). |
| **Verified Facts** | Foundation for downstream calculations and empirical metrics. | Grounded by v1.5 DATA verdicts and designated as `verified` (e.g., verified median trajectory snapshots). |
| **Issue Document Proposals** | Evaluated critically. Subordinate to specifications. Often containing known errors or theoretical mismatches. | Contained within `03-curriculum-and-training-loop.md` or associated baseline reports. |

Where the underlying authoritative specifications are silent, truncated, or ambiguous concerning a specific architectural configuration, the evidentiary gap is explicitly documented.[1] Under no circumstances are synthetic resolutions, fabricated variables, or approximated thresholds injected into the structural logic to force a localized resolution.[1]

## Kinematic Non-Dimensionalization and Dimensionality Constraints

The fundamental stability of the continuous neural representation is directly predicated upon the accurate non-dimensionalization of celestial kinematics. Raw physical trajectories of three-body interactions span immense numerical magnitudes, guaranteeing severe catastrophic gradient failures and vanishing activations if fed into standard network architectures without rigorous preprocessing. The framework standardizes these inputs via scaling relationships parameterized by a characteristic length scale and predefined structural projection vectors.

### The Characteristic Length Scale Dispute

A foundational theoretical dispute exists regarding the appropriate normalization constant utilized to convert dimensional astronomical unit ranges into well-behaved code units.[1] The non-authoritative issue documentation argues for a characteristic length scale of $D = 6.694$, an assumption registered as the unverified claim CLM-01.[1] The derivation supporting this figure stems from a total-mass scaling formulation defined mathematically as $D = (G \cdot M_{tot\_ref} \cdot T^2)^{1/3}$, inherently assuming a reference total mass of $M_{tot\_ref} = 3.0$ and an arbitrary temporal scaling constant of $T_{scale} = 10$.[1]

Rigorous adjudication invalidates this total-mass paradigm completely. As established by the locked SCOPE-12 hard constraints (Item 6), and corroborated by the v1.5 Phase 25 documentation (EVID-10), the total-mass formulation was explicitly examined and formally rejected as an invalid scaling parameter for the present architecture.[1] The framework instead enforces the raw-mass non-dimensionalization convention, which yields $D = (G \cdot T^2)^{1/3} \approx 4.6416$ under the assumption that the gravitational constant $G = 1$.[1]

| Normalization Parameter | Formulation | Computed Value | Epistemological Status | Adjudicated Ruling |
|---|---|---|---|---|
| **Total-Mass Derivation** | $D = (G \cdot M_{tot\_ref} \cdot T^2)^{1/3}$ | 6.694 | CLM-01 (`claimed-unverified`) | **Rejected.** Contradicts Phase 25 EVID-10 validation. |
| **Raw-Mass Derivation** | $D = (G \cdot T^2)^{1/3}$ | $\approx 4.6416$ | CLM-19 (`verified`) | **Locked.** SCOPE-12 Hard Constraint. Mandatory for all downstream scaling. |

This raw-mass length scale ($D \approx 4.6416$) operates as an immutable boundary.[1] Therefore, all subsequent curriculum calculations, including the normalization of angular momentum metrics, spatial separation boundaries, and the derivation of predictable predictability horizons, must be reconstructed utilizing the raw-mass length scale to maintain topological consistency.[1]

### Continuous Temporal Domain Mapping

Neural architectures employing periodic activation functions, such as the SIREN networks designated for this implementation, exhibit maximum phase stability and optimal frequency generalization when inputs are constrained to a symmetric numerical boundary.[1] Consequently, the framework mandates the standardization of spatiotemporal normalization, specifically targeting the temporal input array.[1]

The physical integration time $t$ spans the interval $[0, T]$, where the characteristic maximal simulation time equates to $T = t_{\max} = 10$ code units.[1] To align this interval with the optimal neural domain, the continuous physical time $t$ undergoes an affine transformation mapping it to the normalized continuous range $[-1, 1]$.[1] This mapping is executed via the formalized temporal equation $t' = 2(t/T) - 1$.[1] In the context of PyTorch Automatic Differentiation operations, the intermediate temporal ratio $u = t/T$ operates as the foundational autograd leaf, ensuring that derived velocities and accelerations cleanly propagate through the chain rule mechanisms linking the continuous time domain to the spatial coordinates.[1]

### Neural Input Architecture and Spatial Projection

The neural architecture strictly defines its input manifold to maintain physical determinism.[1] Under SCOPE-12 Constraint 1, the continuous PINN input is locked strictly to a 14-dimensional vector, encoded as $[ \tau, IC_{13} ]$.[1] The first dimension captures the scaled temporal coordinate $\tau$ (structurally equivalent to $t'$), establishing the continuous evaluation point for the network.[1] The subsequent 13 dimensions encapsulate the initial physical condition state, parameterized through a fixed-gauge Jacobi-state encoding.[1]

This $IC_{13}$ vector is synthesized through a highly regulated, locked preprocessing pipeline designed to eliminate redundant translational artifacts and rotational degrees of freedom.[1] The data undergoes rigorous center-of-mass (COM) removal, receives a zero-momentum inertial boost, and is organized into canonical spatial ordering under a canonical rotation gauge.[1] While this specific representation retains mathematically redundant elements relative to the minimal necessary phase-space coordinates, its reconstructive properties were explicitly locked during Phase 19 (PHYS-06) development.[1]

To complement the constrained input, the output spatial tensor is similarly governed by structural mechanics.[1] SCOPE-12 Constraint 3 mandates the application of a hard, mass-weighted center-of-mass projection head applied immediately to the raw 9D position output predicted by the network layers.[1] Crucially, this projection head is executed before the evaluation of any mathematical loss or gradient metric.[1] By forcing the spatial coordinates to satisfy barycentric equilibrium fundamentally, linear momentum conservation is structurally embedded into the manifold output itself.[1] This architectural design entirely bypasses the need for soft-penalty regularizations regarding linear momentum conservation, increasing the robustness of the residual physics loss.[1]

## Fundamental Physical Metrics and Parallel Scale Computations

The transition from dimensional celestial trajectories to a curriculum-ready tensor framework requires the global calculation of structural constraints across the entire dataset manifold.[1] To effectively stratify the curriculum, the architecture identifies defining physical invariants characterizing the initial system configuration at $t = 0$.[1] The processing of over 15,000 dense trajectory files demands significant computational throughput to extract the foundational constants without inducing hardware bottlenecks.[1]

The framework resolves this through a fully parallelized computational orchestrator leveraging native multi-processing.[1] The primary execution loop (`compute_globals`) distributes independent integration matrices across a process pool array.[1] Individual workers parse localized state vectors from designated flat-text initial condition records (e.g., `ic_hierarchical_*.txt`).[1] Each record contains exactly 21 floating-point dimensions corresponding to the flat sequence $[m_1, \mathbf{r}_1, \mathbf{v}_1, m_2, \mathbf{r}_2, \mathbf{v}_2, m_3, \mathbf{r}_3, \mathbf{v}_3]$.[1]

Once mapped to continuous dimensionless units utilizing the raw-mass $D$ scaling parameter, the workers isolate total mechanical energy matrices ($E$) and calculate characteristic interaction length boundaries ($r_{char}$) derived natively from mean pairwise distances.[1] The orchestrator subsequently aggregates the complete localized distributions, utilizing stable median calculations to bypass extreme chaotic outliers.[1] The derived global bounding parameters emerge as $E_{scale} = |\text{median}(\{E_j\})| + 10^{-8}$ and $s_{min\_scale} = \text{median}(\{r_{char,j}\})$.[1]

### Normalized Angular Momentum and Matrix Clamping Analysis

The dynamical stability of an arbitrary three-body configuration relies heavily on the distribution of angular momentum relative to the total bounding energy.[1] A system demonstrating maximum possible angular momentum for a given discrete energy state structurally collapses into highly predictable, near-circular planar orbits.[1] Conversely, a massive deficit in angular momentum forces the celestial masses into highly eccentric, plunging radial interactions that precipitate immediate chaotic breakdown and unpredictable scattering.[1]

To capture this property systematically, the framework computes the total angular momentum magnitude ($L$) utilizing standard cross-product mechanics applied to scaled coordinates: $\mathbf{L} = \sum m_i (\mathbf{r}'_i \times \mathbf{v}'_i) \rightarrow L = \|\mathbf{L}\|$.[1] This magnitude is subsequently mapped against the theoretical topological maximum ($L_{max}$), defined mathematically via total system properties: $L_{max} = M_{total} \cdot r_{char} \cdot v_{char}$.[1] The characteristic velocity limit is itself constrained by binding energy representations via $v_{char} = \sqrt{2|E|/M_{total}}$.[1]

The resulting scalar ratio $L_{norm} = L / L_{max}$ serves as a dominant heuristic determining curriculum staging, with high ratios mapping to initial stability phases.[1] However, Finding M6 within the technical documentation uncovers a critical numerical vulnerability in this sequence.[1] Due to floating-point truncation variances and minor precision overlaps during spatial scaling, the raw computation occasionally generates $L_{norm}$ configurations mathematically exceeding $1.0$.[1] If unchecked, executing the subsequent $2x-1$ mapping transformation upon a value exceeding unity pushes the resultant continuous variable out of bounds, destabilizing the initial condition vector structure.[1]

To rectify this data-side failure mode, an explicit algorithmic intervention is necessitated.[1] A hard threshold bounding protocol utilizing `np.clip(L_norm, 0, 1)` must be inserted into the processing chain directly following the ratio calculation, truncating errant boundaries before downstream vectorization algorithms ingest the values.[1]

### Lyapunov Time Divergence and State Vector Exclusion

To formally quantify the boundary separating predictable celestial motion from pure deterministic chaos, the framework calculates the Lyapunov Time ($\tau_L$).[1] This metric identifies the precise temporal horizon at which exponentially compounding chaotic interactions render continuous predictions fundamentally invalid.[1]

The evaluation array applies the classical Benettin numerical estimation approach to establish the maximal Lyapunov exponent ($\lambda$) across the trajectory space.[1] Initiating from the base state configuration $y_0$, a microscopic mathematical perturbation is introduced to generate a parallel phantom trajectory $y_0^{pert} = y_0 + \delta_0$, constrained strictly by an initialization magnitude of $\epsilon_{pert} = 10^{-8}$.[1] Both celestial configurations undergo synchronized forward integration across discrete intervals $\Delta t$.[1] Following evaluation, the continuous separation array $\delta_1 = y_1^{pert} - y_1$ is measured to extract a localized growth differential scalar $a_1 = \|\delta_1\| / \epsilon_{pert}$.[1]

Crucially, to prevent exponential overflow during integration, the phantom trajectory undergoes continuous structural renormalization mapping it backward to the perturbation limit while preserving its instantaneous directional gradient: $y_1^{pert} = y_1 + \epsilon_{pert} \cdot (\delta_1 / \|\delta_1\|)$.[1] Averaged continuously across a maximum temporal horizon, the exponent defines predictability: $\lambda \approx (1/T_{horizon}) \sum \ln(a_i)$, leading directly to the temporal metric $\tau_L = 1/\lambda$.[1]

Finding M7 exposes a structural ambiguity concerning the deployment of $\tau_L$.[1] The baseline specifications thoroughly document the calculation of $\tau_L$, yet paradoxically exclude the derived scalar from the final 13-dimensional initial condition state block.[1] The adjudication definitively resolves this finding: the omission is mathematically correct and must remain a fixed characteristic of the framework.[1] The Lyapunov timeframe is inherently a continuous dynamic outcome describing system evolution along a trajectory map; it is not an initial physical invariant inherent to the starting coordinates themselves.[1] Consequently, injecting $\tau_L$ into the $IC_{13}$ parameter space violates state-space definitions.[1] It must function exclusively as an external sorting heuristic utilized solely for mapping trajectories into appropriate chaotic curriculum stages.[1]

## Multi-Fidelity Dataset Architecture and Integration Parameters

The underlying trajectory database fueling the neural model represents a vast amalgamation of distinct celestial domains integrated using advanced N-body methodologies.[1] The structural complexity of chaotic interaction mandates a rigorous separation of input fidelity, balancing raw computational integration time against the necessity for hyper-dense temporal resolution during near-miss singularities.[1] The complete dataset represents a union of 15,028 individually verified physical combinations parsed directly from high-precision Brutus solver outputs.[1]

The trajectories are broadly classified across two dominant spatial paradigms [1]:

1. **High-Fidelity Hierarchical Domains:** These subsets represent mathematically stable celestial configurations, predominantly defined by tightly bound binary stars orbiting in resonance with a third, vastly distant companion body.[1] Their inherent stability permits extremely tight integration tolerances to capture long-term periodic smoothness.[1]
2. **Low-Fidelity Quasi-Random Domains:** Synthesized extensively via advanced Sobol quasi-random sequence sampling, this division forces bodies into chaotic, overlapping interaction geometries.[1] These sequences deliberately explore the unstable manifold space to map scattering dynamics and orbital breakdown.[1]

| Dataset Designation | Spatial Configuration Mode | File Count | Integrator Precision Tolerance | Word Length Parameter | Baseline Snapshot Frequency ($dt$) | Temporal Density Scaling |
|---|---|---|---|---|---|---|
| **Set 1a (Original)** | Hierarchical Structure | 4,857 | $1\text{e-}15$ | 130-bit | 0.08 | 1x Baseline Rate |
| **Set 1b (Original)** | Standard Quasi-Random | 4,857 | $1\text{e-}13$ | 118-bit | 0.17 | 1x Baseline Rate |
| **Set 2a (Resolution Upgrade)** | Hierarchical Structure | 2,749 | $1\text{e-}13$ | 130-bit | 0.01 | 8x Extreme Density |
| **Set 2b (Resolution Upgrade)** | Standard Quasi-Random | 2,565 | $1\text{e-}13$ | 130-bit | 0.01 | 17x Extreme Density |

The integration and verification pathways are mathematically constrained by SCOPE-12 Locked Contracts (Items 7).[1] These data-side pipeline limits govern precisely how trajectories bypass corruption logic.[1] Every validated phase utilizes explicit trajectory-admission gates mapped against robust blacklist-exclusion matrix filters to isolate systems manifesting immediate unrecoverable collapse outside the temporal bounds.[1] The validated trajectories then progress directly into the curriculum mapping schema.

## Curricular Stage Stratification and Evolutionary Progression

The foundational premise governing Curriculum-Transfer Learning (CTL) within PINNs states that neural models cannot adequately learn chaotic temporal boundaries without first internalizing foundational periodic truths.[1] The loss gradients originating from extreme close encounters generate chaotic gradient spikes that immediately corrupt early-stage generalized weight convergence.[1] Therefore, the framework dictates a rigorous seven-stage progression algorithm, evolving smoothly from highly predictable Keplerian mechanics toward entirely unbound scattering singularities.[1]

Because quasi-random Sobol sampling fundamentally strips away reliable preservation of the Virial ratio during initialization, an integrated stratification mechanism relying on dynamic bounds controls stage transitioning.[1] These parameters filter trajectories utilizing mechanical energy ($E$), angular momentum stability ($L/L_{max}$), Virial equilibrium defining gravitational collapse versus expansion ($Q = 2T / |V|$), and raw baseline body proximity ($s_{min}$).[1]

| Stage Identification | Fundamental Characterization | Staging Criteria Boundaries | Analytical Purpose within Architecture |
|---|---|---|---|
| **Stage 0** | Highest Stability | $E < -0.5$; $L/L_{max} > 0.5$; $0.7 \le Q \le 1.3$; $s_{min} > 2$ | Imprints baseline smooth-trajectory orbital mechanics. Filters solely tightly bound, wide-separated binaries in virial equilibrium.[1] |
| **Stage 1a** | Energy Relaxation | $-0.5 \le E < -0.1$; $L/L_{max} > 0.5$; $0.7 \le Q \le 1.3$; $s_{min} > 2$ | Introduces moderate gravitational well relaxation without sacrificing angular stability.[1] |
| **Stage 1b** | Angular Momentum Relaxation | $E < -0.5$; $0.1 \le L/L_{max} < 0.5$; $0.7 \le Q \le 1.3$; $s_{min} > 2$ | Plunges systems into severe eccentric modes while maintaining deep total binding energy.[1] |
| **Stage 2** | Temporal Refinement | Union matrix mapping Stage 0 + Stage 1 criteria constraints.[1] | Injects Set 2a ultra-high resolution temporal data to strictly evaluate temporal precision decoupled from novel topological chaos.[1] |
| **Stage 3** | Moderate Low-Fidelity Chaos | $E \le E^{LF}_{25\%}$; $L/L_{max} \ge L^{LF}_{75\%}$; $0.9 \le Q \le 1.1$ | Introduces quasi-random variables while protecting against severe divergence through strictly mapped percentage boundaries.[1] |
| **Stage 4a** | Chaos (Extended Horizon) | Predictability bound defined strictly by $\tau_L > 5$ code units. | Introduces fundamental chaotic drift possessing extensive predictable pathways before divergence.[1] |
| **Stage 4b** | Chaos (Terminal Horizon) | Highly restricted predictability matrix where $2 < \tau_L \le 5$ limits.[1] | Forces model to operate inside highly volatile regimes where deterministic divergence accelerates massively.[1] |
| **Stage 5** | Chaotic Temporal Refinement | Identical constraint matrix to combined Stage 4 boundaries.[1] | Pushes extreme snapshot-density Set 2b files through the system, testing resolution across chaotic fields.[1] |
| **Stage 6** | Extreme Collision / Scattering | $s_{min} < 0.5$ **OR** absolute energy limits measuring $\vert E\vert$ | |

### Empirical Validation Status of Demographic Trajectory Totals

A substantial documentation divergence exists regarding the empirical validation of the stage populations mapping across the stratification sequence.[1] The issue documentation asserts definitively modeled populations, notably dictating $\sim$1,200 trajectories assigned to Stage 0, scaling sequentially up through $\sim$1,600 trajectories terminating in Stage 4.[1] However, interrogation against the verification repository exposes all trajectory count approximations logged as CLM-02 through CLM-07 strictly as `claimed-unverified` parameters.[1]

These configurations represent speculative output boundaries designed by automated, uncalibrated stage-assignment systems that have not passed Phase-1 empirical verification thresholds.[1] Consequently, they remain entirely restricted by Future Empirical Check (FUT) gates and cannot function as foundational parameters determining maximum epoch allocations or mathematical loss plateau baselines.[1]

Equally critical, the generalized snapshot-per-trajectory estimations utilized in prior framework diagnostics (CLM-13: claiming $\sim$59 snapshots standard, $\sim$125 hierarchical, and $\sim$1000 gold) are explicitly overridden.[1] Computations must rely exclusively on the formally locked DATA-06 medians (CLM-16), validating the physical matrix boundaries at precisely **61 median standard outputs, 127 median hierarchical bounds, and exactly 1003 median high-density gold temporal snapshots**.[1]

### Unattainable Stage Transition Mechanics and Gating Triggers

Navigating across the predefined structural stages relies upon mathematical gating mechanics designed to evaluate network capability prior to escalating dynamical complexity.[1] Finding D5 outlines a debilitating theoretical failure originating from rigidly deterministic stage transition criteria.[1] The preceding specification dictated that the continuous neural architecture could only advance into a subsequent stage given an unbroken string of monotonically decreasing validation loss markers.[1]

Due to the stochastic nature of dense neural optimizations mapped across chaotic arrays experiencing constant micro-variations, enforcing strict monotonic loss reductions causes rapid evaluation stagnation.[1] In practice, models hit microscopic validation variance plateaus causing perpetual gating lockouts regardless of underlying generalizable convergence.[1] The adjudication dictates the implementation of dual-path progression matrices applied immediately from Stage 0.[1] A strict evaluation channel maintains primary validation authority based on complex mathematical tolerances. Simultaneously, a dynamic fallback architecture enforces transition escalations initiated via maximum computational epoch cutoffs or statistical stagnation quotas, alongside immediate mathematical rollback configurations if $NaN$ divergences are detected.[1]

## Tensor Batch Formulation and Dataloader Rectification

The optimization logic governing the ingestion of multi-fidelity datasets suffered massive procedural breakdown due to conflated dataloader designs. Two "BLOCKING" failures (B-07 and B-08) were definitively located within the core batch mechanisms.[1]

### The Replay Buffer Collapse and Lookahead Correction (B-07)

The core tenet of stable continuous learning mechanisms involves protecting foundational insights against catastrophic interference when processing novel chaotic inputs.[1] Finding B-07 exposes an operational reality where the underlying training loop bypassed completely the structured replay mechanisms detailed within the CTL manuals.[1] Instead, the dataloader executed a statistically flat, non-discriminatory fetch, populating batches using 256 random trajectories untethered to stage identity.[1]

A random batch matrix introduces dual catastrophic failure modes.[1] Firstly, the complete elimination of historical replay mechanics generates catastrophic forgetting; the network dynamically overwrites fundamental smooth-trajectory Keplerian physics parameters when abruptly swamped by chaotic scattering gradients.[1] Secondly, the lack of sequential lookahead exposure triggers violent and unpredictable loss explosions whenever arbitrary stage thresholds advance sequentially.[1]

The architectural fix mandates deploying a dual-phase tensor sampler.[1] The overall array structure must extract exactly 240 structured replay trajectories mathematically sourced from the total repository of current and completed historical archives (Stages $\le k$, mapped as $D_{\le k}$).[1] Furthermore, it necessitates the simultaneous extraction of 16 structured lookahead trajectories derived strictly from the immediate progressive threshold bounds (Stage $k+1$, mapped as $D_{k+1}$).[1] Each sampled path projects exactly 32 discrete internal time points, rigorously distributed through a 50/50 dual-matrix logic: half mapped across a perfectly uniform temporal spread bridging $[t_{min}, t_{max}]$, the other half dynamically distributed via acceleration-weighted parameters optimizing coordinate extraction near high-curvature periapsis zones.[1] (Parameters mapped under claimed-unverified classification CLM-12).[1]

### Isolation of Data-Fidelity and Collocation Matrices (B-08)

Finding B-08 uncovers an equally devastating dataloader collapse where physical reality constraints were fundamentally blended with mathematical interpolation constraints.[1] PINNs rely heavily on separate error topographies: data-fidelity vectors measure network accuracy mapped directly against discrete empirical simulation snapshots generated via the Brutus solver, while continuous collocation vectors track global compliance to overarching physical residual loss invariants extracted universally across the continuous coordinate plane.[1]

The prior iteration erroneously collapsed both requirements, evaluating them atop identical discrete trajectory points.[1] Such logic defeats continuous physics representations by tying differential solvers artificially to predefined output cadences.[1] To guarantee mathematically valid partial differential equation scaling, absolute detachment is required.[1]

| Point Generation Array | Discrete Temporal Volume | Extraction Methodology | Mathematical Validation Metric |
|---|---|---|---|
| **Data-Fidelity Architecture** | 8,192 Points per batch | Anchored rigorously to exact simulation time steps.[1] | Calculated via strict mathematical $L_1$ norm comparisons.[1] |
| **Global Collocation System** | 4,096 Points per batch | Floated dynamically across arbitrary temporal continuous domain mappings spanning $[t_{min}, t_{max}]$.[1] | Evaluated exclusively through physics constraint residuals and Hamiltonian energy conservation penalties.[1] |

Both disjointed arrays enforce identical 50/50 uniform and acceleration-weighted temporal distribution algorithms to ensure chaotic geometries are comprehensively enveloped.[1]

### Collocation Normalization Across Divergent Densities (M16)

Executing standardized global collocation parameters across datasets bearing vast variations in snapshot output densities introduces systemic bias into optimization gradients.[1] Finding M16 isolates a massive temporal imbalance wherein snapshot intervals mapping baseline hierarchical outputs ($dt \approx 0.08$) or quasi-random streams ($dt \approx 0.17$) exist alongside the radically dense gold standards ($dt = 0.01$) defining up to a 17-fold frequency disparity.[1]

Deploying static temporal point boundaries forces chaotic lower-resolution paths to bear massively inflated statistical relevance relative to their intrinsic spatial content, skewing physical residuals.[1] The mathematical resolution (mapped unverified under CLM-20 parameters) forces dynamic proportional constraints tracking temporal output scaling vectors.[1]

The calculation dictates evaluating density configurations relative to the benchmark $dt_{base} = 0.01$ output state via the formulated multiplier $n_{col} = base \cdot (dt_{base} / dt_{out})$.[1] Concurrently, this scales the standard baseline integrations to heavily diminished mathematical frequencies approximating $0.059$x normal volume, limits hierarchical domains to $\approx 0.125$x rates, and perfectly preserves gold pathways operating at $1.0$x saturation limits, neutralizing architectural imbalance entirely.[1]

## Structural Adjudications Governing Causal Regularization and Geometric Tolerances

The most complex challenges remaining for the framework require the definitive selection between competing conceptual paradigms regarding temporal causality enforcement and singularity geometric modeling.[1] These decisions remain officially unresolved pending framework-owner approval; the parameters, conflicts, and options are formally outlined to facilitate finalization.[1]

### The Causal-Training-Mode Discrepancy (D-04)

Modeling deeply chaotic trajectories utilizing physics-informed mechanisms routinely encounters catastrophic optimization failures stemming from temporal causality violations. If early portions of a celestial trajectory display minute positional deviations, the mathematically correct continuation along the phase space drives the simulation exponentially away from the expected future state. Standard neural networks inherently ignore causality, simultaneously penalizing minor late-stage deviances identically to early-stage structural errors, essentially pulling the coordinates toward physically impossible average pathways rather than true chaotic evolutions.[1]

Addressing this failure defines the single most consequential training-loop paradigm.[1] However, severe document contradictions obscure the official configuration.[1] The issue document claims that a methodology employing Global Sampling mapped to an Augmented Lagrangian Method (ALM) represents the current Source of Truth (SOT).[1] It cites sections outlining single forward passes mapped to total constraint-violation fields.[1]

Contradicting this directly, the unyielding authoritative framework specification (`ctl_instruction.md`) operates utilizing robust causal weighting matrices.[1] Operating as the PHYS-05 default mechanism, the formulation scales gradients explicitly via sequential loss progression arrays parameterized as $w_n = \exp(-\eta_c \cdot \sum_{m<n} \text{stopgrad}(\bar{R}_m))$ relying on exponent limits defining $\eta_c = 1$.[1] The mathematical specifications purposefully eliminate pseudo-ALM frameworks combining data loss, generic unscaled residual scalars, and unified energy vectors, retaining the ALM mechanism exclusively within specialized scalar Phase 2 ablations.[1] The overarching decision provides three distinct paradigms.

| Operational Design | Methodology | Optimization Dynamics and Risk Vectors |
|---|---|---|
| **Option A (Per-Time-Step Causal Weighting)** | Forces temporal sequences dictating $w_i \propto \exp(-\lambda \sum_{j<i} L_j)$ constraints.[1] | Maintains highly robust structural reality enforcing physical "arrows of time".[1] Vulnerable to "Causal Firewall" breakdowns where singular chaotic spikes occurring prematurely permanently collapse subsequent optimization gradients to zero.[1] |
| **Option B (Global Sampling / Dense ALM Array)** | Evaluates the complete time spectrum over continuous integration regions mapping $[t_{min}, t_{max}]$ simultaneously.[1] | Eliminates early gradient crashes allowing total topological evaluation across complex fields.[1] Highly susceptible to gross causality violations wherein volatile late-stage chaotic boundaries negatively corrupt smooth early-stage kinematic convergences.[1] |
| **Option C (Time-Windowed Causal-ALM Hybrid)** | Deploys advanced interlocking matrices partitioning continuous mapping limits into rigid overlapping sequence domains utilizing extreme local hard-gating.[1] | Provides optimal mathematical stabilization circumventing firewall events while preserving arrow metrics natively.[1] Implementation requires near-total reconstruction impacting Phase 2 dataloaders and stage gating systems.[1] |

### Geometric Coordinate Definitions for Collision Gating ($s_{min}$) (D-05)

Determining proximity bounds in gravitational structures necessitates extreme precision, particularly transitioning between macro-scale orbital measurements and microscopic numerical singular thresholds.[1] Minimum coordinate separation thresholds map to the scalar metric $s_{min}$ natively measuring initial interaction dimensions between bounded entities.[1]

Stage 6 configurations are governed purely by geometric proximity triggers established around measurements satisfying $s_{min} < 0.5$ boundaries to invoke severe scatter evaluations.[1] Standard implementation manuals invoke pure theoretical mathematical ranges mapping distances organically utilizing completely unsoftened metric variables for validation.[1] Contrastingly, the internal training loop specifications necessitate utilizing robust numerical dampening arrays enforcing constraints approximating $\epsilon_{soft} = 10^{-5}$ boundaries to eliminate unbounded division limits arising during coordinate intersection gradients.[1]

The pending framework-owner decision balances dual-resolution mechanisms [1]:

- **Option A:** Ensures strict adherence to source limits by running unsoftened pure measurements to govern macroscopic dataset transition gating logic to preserve initial ground truth, while isolating numerical limits measuring $\max(s_{min}, \text{eps\_soft} = 1\text{e-}5)$ universally mapping within discrete dynamic gradient networks to govern division safety loops.[1] Unsoftened coordinates are output securely into external analytical archives continuously.[1]
- **Option B:** Establishes mathematical unity forcing the $\max(s_{min}, \epsilon)$ transformation identically upon both data sorting protocols and neural network loss topographies equally.[1]

### The Epsilon Parameter Domain Discrepancy (D-06)

Compounding proximity logic disputes, the operational models currently harbor fatal order-of-magnitude divergences regarding applied softening parameter constants.[1] Computations governing underlying static potential energy derivations operate relying upon bounds restricted to exactly $\epsilon = 10^{-10}$.[1] However, the framework manuals highlight aggressively that such diminutive variables map identically to zero bounds inside baseline 32-bit GPU floating-point architecture fields, offering literally zero mathematical safety buffers.[1] Consequently, parallel internal limits restrict standard bounds to robust $\epsilon_{soft} = 10^{-5}$.[1]

Adjudication inherently forces alignment with SCOPE-12 Locked Item 4 metrics fixing loss-side physics-residual evaluations statically to $\epsilon_{train} = 1e-5$ incorporating standard matched-Plummer mathematical topology structured as $r_{safe} = \sqrt{\|\Delta r'\|^2 + \epsilon_{train}^2}$ while aggressively prohibiting generic linear additives.[1] The sole unresolved dynamic centers completely around how strictly static contexts integrate alongside the locked limit array.[1]

- **Option A:** Adopts universal $1e-5$ deployment models modifying pure static derivations entirely.
- **Option B:** Maintains a precise dual-context framework scaling static bounds parsed within complex 64-bit CPU configurations to exact $1e-10$ models while delegating all dynamic gradient operations inside GPU limits strictly to the protected $1e-5$ bounds.[1]
- **Option C:** Reverts models aggressively pushing generic $1e-10$ mappings over the full mathematical domain, openly discounting explicit documentation logic outlining severe convergence instability risks.[1]

## Continuous Physics Loss Regularizations and Gradient Telemetry

Ensuring accurate neural optimization inside chaotic domains relies upon sophisticated loss boundary scheduling matrices capable of limiting erratic spatial errors and suppressing catastrophic residual energy explosions natively.

### Energy Conservation Matrix Mitigation ($\lambda_E$) (M15)

The theoretical framework measures trajectory validity heavily based on absolute adherence to static Hamiltonian mechanical boundaries, particularly calculating mechanical binding loss over phase transitions.[1] The applied energy conservation limit ($\lambda_E$) serves to forcefully suppress predictions drifting structurally away from realistic limits.[1] Finding M15 identifies severe catastrophic failure configurations wherein standard late-stage parameters applying weights escalating upward toward limits approximating 1000 generate unmanageable optimization errors.[1] By scaling limits artificially high relative to native physical variances, the energy term swamps core coordinate positioning boundaries by factors expanding geometrically between 100x and 5000x margins.[1]

The solution requires mandatory hard-clamping models restricting variables via $\lambda_E(k) = \min(10^{k-3}, \text{cap}[k])$ distributions tracking progressively through sequence models mapping linearly across bounds starting at nominal 1 values up through hard terminal limits approximating 500.[1] (Metrics mapped unverified into CLM-11 parameters).[1] An active secondary heuristic requires runtime evaluation boundaries forcing real-time weight scaling compression whenever computed combinations violate basic scaling constraints defined via $(\lambda_E \cdot L_{energy}) > 10 \cdot L_{data}$ thresholds to prevent terminal run failures.[1]

### Continuous Adaptive Clipping Metrics (M14)

Optimization limits face conflicting array boundary definitions inside standard mathematical specifications.[1] Base PINN topologies define models capturing gradient normalizations utilizing strictly dynamic median historical rolling windows mapped inherently over discrete intervals.[1] Alternately, stage configuration models outline discrete static numerical step boundaries defining parameter array steps utilizing simple scalar integers.[1]

Finding M14 definitively forces unification combining both architectures continuously.[1] Parameters merge dynamically producing exact clipping targets evaluating constraints via $\text{clip\_value} = C_{stage} \cdot \text{median}(\text{grad\_norm\_history})$ boundaries.[1] The stage-aware parameter ($C_{stage}$ derived from `claimed-unverified` CLM-10 arrays) controls structural limits while native rolling windows govern immediate spatial tracking dynamics continuously.[1]

### ALM Variance Boundary Clamp Protocol

Integrating Augmented Lagrangian methodologies inside scalar Phase 2 bounds creates secondary optimization risks connected tightly to unbound structural variable drift tracking.[1] Specifically, formulas driving updating metrics for the parameter bounds defining moving-average limits managing $\mu_p$ scalar adjustments entirely lack limiting mathematical ceilings inherently.[1] Devoid of operational boundaries, volatile training runs precipitate immediate divergence pulling scalars asymptotically toward infinite bounds, breaking optimization loop geometries entirely.[1] To resolve structural deficiencies entirely, numerical clipping matrices utilizing standard mathematical array commands strictly evaluating limits constrained via `np.clip(mu_p, 1e-4, 100.0)` must insert fully inside operational update blocks natively.[1]

### Analytical Automatic Differentiation (AD) Fidelity and Topologies

Two critical optimization array components require fundamental architectural fixes concerning gradient tracking pathways.[1]

- **Component-Wise Kinematics (NS-12):** Initial theoretical outlines dictate velocity and acceleration tensor evaluations map cleanly utilizing strict PyTorch Automatic Differentiation matrices applied securely.[1] Live implementation parameters frequently circumvent strict chain-rule tracking formulas incorrectly utilizing total 9D state tensor summation properties representing generalized acceleration variables.[1] Finding NS-12 explicitly prohibits aggregated mapping derivatives.[1] Structural accuracy completely relies mapping pure discrete component-wise limits mapping temporal continuous fields mathematically onto corresponding unique geometric points strictly conforming identically against discrete continuous laws.[1]
- **Huber Parameter Calibration Dynamics (NS-13):** Evaluating relative performance boundaries applying energy differential scaling uses classical Huber models configured typically mapping values around generic $\delta = 1.0$ parameters.[1] Operating securely against fundamentally normalized input limits, broad limits entirely nullify Huber bounds reducing metrics functionally back mapping onto simplistic unbound $L_2$ properties failing entirely providing large-scale anomaly tracking.[1] Redefining bounds mandates initializing metrics securely across extremely tight $0.01$ parameters dynamically parsing measured quantile deviations directly extracted checking empirical bounds derived against absolute $|\Delta H|$ matrices mapped independently against specific curriculum sequences universally.[1]

## Evidentiary Boundaries and Tracked System Omissions

In strict adherence to the epistemological framework defined within the task adjudication sequence, analyzing theoretical constructs requires tracking transparent records detailing explicitly where fundamental material specifications suffer catastrophic missing boundary data configurations.[1]

Evaluations strictly bound against `doc-03` payload parameters expose massive source omissions invalidating deep parameter configurations.[1]

1. **Architecture Specifications:** Detailed continuous layer parameters, layer depth metrics, internal node frequency mapping, baseline loss limits defining topological initialization configurations referenced heavily relying upon standard target document matrices mapped globally as `pinn_architecture.md` (SHA-256 identifying `318f297a...`) exist entirely absent pulling through provided payload variables.[1]
2. **Sampling Framework Parameters:** Explicit programmatic boundary metrics defining pure theoretical Sobol generation patterns mapped against complex dataset integration mapping requirements existing naturally inside native `sampling_method.md` files structurally remain omitted from provided payloads.[1]
3. **Detailed Transition Modifications:** Deep metric evaluations detailing explicit transition alternative logic variables mapping natively inside `stage_strat_revision.md` specifications exist definitively outside the operational domain parsed through transport sequences.[1]
4. **Incomplete Interrogation Parameters:** Provided sequences determining core open research boundaries defining required decision thresholds display critical terminal truncation limits severing `framed-research-questions.md` text boundaries directly following causal limit mappings causing total analytical blackout measuring detailed option tracking regarding epsilon definitions independently.[1]

Any specific structural resolutions requested targeting these restricted bounds return formal "Insufficient Evidence" classifications registering directly mapping claims tracking limits effectively removing synthetic theoretical parameter generation variables universally.[1]

## Comprehensive Synthesis and Resolution Matrix

The adjudication of the multi-fidelity PINN framework targeting continuous complex three-body systems establishes a unified mathematical reality governed entirely underneath immutable fixed boundary constants restricting variables exactly against standard raw-mass non-dimensional mapping limits derived utilizing $D \approx 4.6416$ constraints while comprehensively overriding alternative total-mass theories structurally.[1]

Navigating dataset variables ranging structurally spanning deeply bound stable Keplerian dynamics advancing systematically toward unbounded hyper-dense terminal chaotic limits mapping 17-fold trajectory density variations relies comprehensively upon structural normalization bounds strictly utilizing derived empirical mapping constants fixing spatial matrices identically alongside $t' = 2(t/T) - 1$ mapping boundaries projecting temporal values into continuous variables efficiently.[1] Critical parameter logic fixes enforce absolute mathematical integrity isolating variables dynamically establishing clamping algorithms locking down derived angular limits neutralizing overflow arrays scaling above $1.0$ boundary limitations natively while aggressively excluding derived temporal matrices mapping Lyapunov parameters defining $\tau_L$ outside fixed $IC_{13}$ arrays universally.[1]

Optimization metrics advance structurally bypassing catastrophic replay collapse frameworks rebuilding dataloaders distributing purely defined 240+16 boundaries incorporating 50/50 temporal weighting formulas seamlessly isolating pure coordinate fidelity configurations capturing exactly 8192 parameters decoupled cleanly away targeting continuous collocation maps applying exactly 4096 separate nodes bounded strictly scaled proportionally correcting heavy matrix densities tracking explicit $n_{col} = base \cdot (dt_{base} / dt_{out})$ bounds cleanly maintaining accurate tensor normalization structures universally.[1]

Terminal framework finalization pathways require direct resolution determining final topology mapping configurations isolating critical conflict limits detailing ALM boundaries versus strictly mapped temporal causal weighting constraints definitively resolving conflicting parameter strategies spanning geometric unsoftened boundaries tracking exactly tracking analytical epsilon mapping variations restricting matrices accurately isolating operational boundaries safely inside formal double-precision configurations scaling matrices perfectly.[1]

## Works cited

1. 03-curriculum-and-training-loop.md
