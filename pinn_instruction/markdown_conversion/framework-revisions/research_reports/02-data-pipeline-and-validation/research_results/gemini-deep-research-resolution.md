# Research Task: Resolution Document for a Data-Pipeline and Validation Issue Set

Date: June 10, 2026

Package Inventory:
- `RESEARCH-CONTEXT-MASTER.md`
- `DELIVERY-NOTE.md`
- `specs/02-data-pipeline-and-validation.md`
- `specs/ctl_instruction.md`
- `specs/pinn_architecture.md`
- `specs/sampling_method.md`
- `specs/data_quality_assessment.md`

## §0 Scope and decision standard

This comprehensive resolution document is the product of an exhaustive technical analysis of the
issue-02 external-research package, commonly referred to as the "Data Pipeline and Validation"
subset. The analysis strictly targets the optimization of data validation protocols and pipeline
fidelity required for training a Causal Physics-Informed Neural Network (CTL-PINN) on chaotic
three-body gravitational data. [^1] The primary objective of this report is to adjudicate a series
of unresolved technical conflicts, evaluate candidate recommendations, and produce a unified,
authoritative set of operational protocols that bridge the computational gap between
arbitrary-precision numerical integration and continuous causal deep learning architectures.

The evaluation framework operates under a strict epistemological hierarchy established by the
package manifest. [^1] Specifically, the locked framework specifications—namely `ctl_instruction.md`,
`pinn_architecture.md`, `sampling_method.md`, and `data_quality_assessment.md`—are treated as the
absolute and canonical sources of truth.

These documents dictate immutable boundary conditions such as the 14-dimensional input contract
(comprising normalized time and a 13-component initial condition vector), the Jacobi IC13
convention, the mass-weighted center of mass projection head, and the post-v1.3 Symplectic
Conservation Score (SCS) filtering gate. [^1] Consequently, the thematic issue document
(`02-data-pipeline-and-validation.md`) is analyzed strictly as a non-authoritative collection of
candidate claims, field observations, and hypotheses subject to adversarial adjudication. [^1]
Recommendations proposed within the issue document are systematically overridden, refined, or wholly
rejected whenever they conflict with the established physical mechanics of the computational
pipeline or the locked project conventions.

A significant boundary condition governing this analysis is the explicit truncation of the provided
research context master file. The directive mandates investigating and answering every question in
the master document's "Framed Research Questions" section (PKG-02) and evaluating the "CLM Claims
Register" (PKG-03). [^1] However, analysis of the pristine snapshot of `RESEARCH-CONTEXT-MASTER.md`
reveals that the specific, enumerated research questions (e.g., Q-01, Q-02) and the exact tabular
entries mapping dataset figures to verification statuses are fundamentally unavailable in the
provided baseline due to a document truncation immediately following the presentation of the
source-treatment conventions. [^1] As strict adherence to the rules of evidence prohibits guessing
unstated facts or hallucinating repository content, this document fulfills its mandate by
functionally promoting the specific, contested pipeline findings identified in the issue document
(B-06, B-11, M11, M12, M13, D7, M16) alongside the explicit "Seed Conflict" to the status of primary
research questions. [^1] Furthermore, external dependencies such as the live
`pinn/data-processing-pipeline-full.py` codebase are strictly excluded from the analysis pursuant to
the 2026-05-19 SCOPE-10 directive, reinforcing the self-contained nature of this adjudication. [^1]
All dataset figures referenced indirectly are explicitly tracked via CLM identifiers and are treated
as claimed-unverified hypotheses unless corroborated by fundamental physical laws or established
specification errata. [^1]

## §1 Executive decision summary

The technical audit of the data processing pipeline identifies a sophisticated multi-stage
architecture designed to transition from geometric stochastic sampling to highly converged numerical
arrays, culminating in continuous neural network optimization. [^1] The pipeline is initiated via a
geometric sampling methodology that utilizes low-discrepancy scrambled Sobol sequences and
hierarchical mass distributions to generate a vast parameter space of initial conditions. [^1] These
configurations are subjected to a sequential filtering cascade: an immediate static collision
filter, a low-precision Leapfrog prescreening integration, and finally, an arbitrary-precision
integration executed by the Brutus C++ engine utilizing the Bulirsch-Stoer extrapolation method.
[^1] The overarching conclusion of this analysis is that while the numerical generation phases are
physically sound, the programmatic interface connecting the Brutus output to the Causal PINN
DataLoader lacks the rigorous phase-space continuity checks required by causal learning
architectures. This oversight jeopardizes the temporal causality essential for gradient propagation
within the network.

The pipeline architecture requires immediate fortification to prevent corrupted or incompatible
numerical meshes from poisoning the training landscape. To this end, a comprehensive suite of
resolutions has been formulated. The implementation of a rigorous TrajectoryValidator at the
DataLoader boundary is mandated to block causal firewalls resulting from incomplete temporal arrays.
[^1] The system's indexing paradigm must be fundamentally restructured through a dynamic
`id_to_path` dictionary, recognizing that non-contiguous trajectory identifiers are the
mathematically guaranteed byproduct of the pipeline's rigorous prescreening filters rather than
structural anomalies. [^1] Furthermore, the ingestion of known problematic configurations via a
loaded blacklist must be enforced to protect the network's bounded Layer Normalization architecture
from extreme coordinate singularities. [^1]

In the domain of continuous learning fidelity, an adaptive thresholding logic for batch collocation
point selection has been approved to prevent standard-resolution trajectories from forcing the
network into pure interpolation blindness. [^1] The analysis authorizes a "graceful degradation"
fallback strategy for missing gold-standard subsets, prioritizing dataset volume and phase-space
entropy over strict curriculum segregation. [^1] Metadata heterogeneity surrounding Bulirsch-Stoer
tolerance parameters is addressed through deterministic defaults, acknowledging that physical
conservation metrics supersede text schemas. [^1] Concurrently, the uniform collocation density
model is replaced with a temporally scaled, probability-weighted architecture, ensuring that deep
gravitational encounters are structurally represented in the loss landscape. [^1] Finally, the
critical "Seed Conflict" regarding the Symplectic Conservation Score is decisively resolved by
rejecting the mathematically flawed issue document thresholds in favor of the physically verified
and locked post-v1.3 parameters derived from the canonical specification errata. [^1]

## §2 Decision matrix

The following matrix standardizes the operative adjudications, correlating the foundational issue
identifiers with their specified resolutions and assigning a confidence metric derived from the
available evidence and first-principles physics.

| Question / Issue ID | Subject Domain | One-Line Verdict / Recommendation | Confidence |
| --- | --- | --- | --- |
| B-06 | Pipeline Gating | Mandate TrajectoryValidator at DataLoader init to block causal firewalls. | High |
| B-11 | Dataset Indexing | Implement TrajectoryIndex mapping to resolve $O(N)$ static/dynamic filter gaps. | High |
| M11 | Blacklist Handling | Enforce blacklist load at training time to protect LayerNorm and SIREN gradients. | High |
| M12 | Batch Sampling | Adopt adaptive $0.5 \times n\_snapshot$ cap to prevent interpolation blindness. | High |
| M13 | Curriculum Gaps | Allow low-fidelity fallback with metadata flags for missing gold-standard IDs. | Medium |
| D7 | Footer Metadata | Infer tol=1e-13 for incomplete footers; add `tol_confidence` classification flag. | High |
| M16 | Temporal Scaling | Scale collocation dynamically via `dt_base` / `dt_out` with SASD probability weights. | High |
| Seed Conflict | Validation Threshold | Reject > 1e-6; enforce authoritative SCS > -5 derived from SI-DQA-002 correction. | High |

## §3 Resolutions

The ensuing subsections deliver exhaustive technical adjudications for the operative issues,
formulated as functional research queries in the absence of the truncated PKG-02 registry. [^1] Each
resolution synthesizes mathematical principles, computational architectures, and empirical
constraints to forge a deployable, specification-ready protocol.

## §3.1 Resolution: B-06 (Missing Validation Gate)

### Verdict / recommendation

The architecture requires the mandatory implementation of a strict TrajectoryValidator module, which
must be executed synchronously during the DataLoader's __init__ sequence. The validator must
programmatically parse the metadata of each trajectory candidate and enforce a tiered conditional
logic protocol prior to admitting the tensor into the active training loop. Specifically, for
trajectories designated for Stage 4 and Stage 5 curriculum learning, the validator must require
`snapshot_count` >= 200. For trajectories designated for Stages 0 through 3, the system must require
`snapshot_count` >= 2. Across all stages universally, the module must assert that `final_timestep`
>= 9.5. Any trajectory failing these temporal continuity conditions must be entirely purged from the
ingestion queue. The total rejection volume, alongside the unique identifiers of the discarded
files, must be written to standard output and logged in a dedicated pipeline rejection registry to
preserve operational traceability.

### Reasoning

The necessity of a rigorous validation gate is deeply rooted in the structural vulnerabilities of
the Causal Physics-Informed Neural Network architecture. [^1] Standard neural networks are
fundamentally unsuited for chaotic dynamical systems because they attempt to globally optimize the
loss landscape simultaneously. In a three-body regime, this induces a temporal causality violation,
where the network attempts to resolve late-stage, high-frequency scattering dynamics before
establishing the prerequisite early-stage trajectories. [^1] To counteract this phenomenon, the
CTL-PINN employs a causal training methodology characterized by a dynamic loss weighting mechanism,
$w(t)$, which propagates sequentially across the temporal axis. [^1] This ensures that the physics
residual penalty is only enforced on subsequent time steps once the precursor steps have
sufficiently converged.

However, this sophisticated sequential mechanism introduces a critical vulnerability defined in the
mathematical specifications as the "Causal Firewall" effect. [^1] The automated pipeline utilizes a
`calculate_metrics.py` script that indiscriminately processes all Brutus output files, inadvertently
enveloping partial, errored, or structurally truncated runs where the integration failed to reach
physical completion. [^1] If the DataLoader lacks a completeness gate, these truncated files are
ingested into the training batch. When the temporal array $t$ abruptly terminates or exhibits a
non-physical boundary, the automatic differentiation logic—which computes the second derivative of
the predicted positions with respect to time ( $\frac{d^{2}r}{dt^{2}}$ ) to construct Newton's
equations of gravity—encounters a massive mathematical singularity. [^1] This boundary discontinuity
produces an instantaneous, catastrophic physics residual spike. [^1]

Because the causal weighting algorithm governs the entire forward pass, it interprets this residual
spike as a failure in the local physical manifold. Consequently, it forces the causal weights for
all subsequent time steps to vanish ( $w_t \to 0$ ). [^1] This action effectively "kills" the
gradient flow to the deep Sinusoidal Representation Network (SIREN) layers, severing the network's
capacity to adjust its parameters. The parameters governing the later trajectory dynamics fail to
receive gradients and drift randomly, initiating localized network collapse. The existing validity
signal (`final_timestep` >= 9.5) is wholly insufficient because it is executed exclusively during
the Stage 3 runner scripts prior to the complex Brutus integration and is never re-validated upon
neural network ingestion. [^1] Therefore, a TrajectoryValidator that guarantees mathematical
completeness and phase-space continuity is an absolute architectural prerequisite to isolate the
causal learning environment from the causal firewall effect.

### Evidence

The non-authoritative issue document accurately flags the missing Stage 4-to-5 gate as a blocking
vulnerability capable of halting pipeline execution. [^1] More authoritatively,
`data_quality_assessment.md` documents the exact mathematical mechanics of the "Causal Firewall"
effect, detailing how continuous causal links are destroyed by residual spikes, forcing the temporal
weights to zero and inducing gradient starvation. [^1]

### Confidence

High. The fundamental architectural reliance of the CTL-PINN on temporal continuity renders this
gate a non-negotiable physical requirement. The single theoretical factor that could alter this
stance is a fundamental re-engineering of the network architecture away from Causal PINNs toward a
non-sequential, purely global evaluation paradigm. Such a structural shift is expressly prohibited
by the locked `pinn_architecture.md` and `data_quality_assessment.md` specifications.

### Verification suggestion

To empirically verify the implementation of the TrajectoryValidator, the validation team should
deliberately inject ten artificially truncated .hdf5 trajectory files (e.g., configurations
terminating at t = 5.0 or containing fewer than 50 snapshots) into the Stage 4 training directory.
Upon initializing the DataLoader, the diagnostic output should confirm that the validator
successfully flags and isolates exactly ten trajectories. Subsequent execution of the training loop
must demonstrate stable gradient propagation without triggering a vanishing gradient collapse or
causal weight nullification.

### Proposed specification text

Anchor Target: specs/02-data-pipeline-and-validation.md (To be promoted to authoritative pipeline
operations manual).

"A TrajectoryValidator module must be instantiated within the primary DataLoader initialization
sequence prior to batch construction. The validator shall strictly parse the metadata of each
trajectory and programmatically assert that `snapshot_count` >= 200 for data routed to Stages 4 and
5, or `snapshot_count` >= 2 for Stages 0 through 3. Furthermore, it must assert that
`final_timestep` >= 9.5 across all configurations. Files violating these spatial-temporal conditions
shall be explicitly dropped from the active dataset map. Their discrete identifiers must be recorded
in a dedicated pipeline rejection log to preserve causal loss weighting integrity and prevent
downstream gradient starvation."

## §3.2 Resolution: B-11 (Non-Contiguous IDs)

### Verdict / recommendation

The overarching system architecture must permanently abolish the programmatic assumption that a
trajectory's physical file ID directly and linearly corresponds to its numerical array index within
the DataLoader sequence. The engineering logic must be rewritten to dynamically construct an
`id_to_path` hash map by actively enumerating the physical, on-disk files during the dataset
initialization phase. Concurrently, the pipeline must implement a robust TrajectoryIndex wrapper
class equipped with a dedicated `get_by_id` (`file_id`) method, strictly enforcing associative
lookups for all Curriculum Training Loop (CTL) batch generation and preventing index-based fatal
runtime errors.

### Reasoning

The phenomenon of non-contiguous trajectory identifiers within the finalized dataset is
fundamentally misunderstood by the legacy DataLoader implementation. A 31.2% gap rate in the
standard dataset and a 2.9% gap rate in the hierarchical dataset are not indicators of a data
generation failure, an anomalous bug, or a corrupted storage array. [^1] Rather, these gaps are the
mathematically guaranteed, intended byproduct of the multi-stage rigorous filtering architecture
defined in the sampling methodology specification. [^1]

The data generation pipeline relies on sequential ID stamping immediately upon the mathematical
formulation of an initial condition, well before its physical viability is established. In Stage 2,
the pipeline generates planar, equal-mass systems evenly across the parameter space using a
low-discrepancy scrambled Sobol sequence. [^1] The Sobol sequence allocates coordinates mapped to a
3D hemisphere, transforming uniformly distributed variables into physical polar angles, azimuthal
angles, and radial distances. [^1] However, this purely geometric sampling has no intrinsic
understanding of gravitational mechanics. Consequently, a static initial collision avoidance filter
is mandated. Any sampled configuration where the pairwise distance between bodies at $t = 0$ falls
below a critical threshold ( $\epsilon = 0.05$ ) is instantly rejected to prevent computationally
disastrous integration of immediate singularities. [^1]

Following this static filter, the surviving trajectories are subjected to a Stage 3 dynamic
prescreening gate. A specialized JIT-compiled Leapfrog integrator computes the short-term evolution
of the system at a fixed step size of $dt = 0.0001$. The trajectory is actively monitored and
subsequently discarded if the relative energy error
$\left|\left(E_{\text{current}} - E_{\text{init}}\right)/E_{\text{init}}\right|$ exceeds 1%, or if
the dynamic minimum separation between any two bodies drops below 0.01 during the evolution. [^1]
Adaptive thresholding logic also filters based on virial ratios and angular momentum boundaries.

Because the identifier assignment precedes these static and dynamic purging mechanisms, the final
cohort of high-fidelity, Brutus-integrated datasets natively inherits a heavily fragmented
sequential structure. The legacy assumption within the Curriculum Training Loop that array indices
map uniformly to file IDs predictably induces "file not found" or "out of bounds" exceptions. [^1]
By decoupling the file ID from the tensor array index via an associative `id_to_path` dictionary,
the pipeline honors the physical realities of initial condition filtering without sacrificing
operational execution speed or memory efficiency.

### Evidence

The authoritative `sampling_method.md` specification explicitly dictates the multi-tiered rejection
criteria ( $\epsilon = 0.05_{static gate}, 0.01_{dynamic Leapfrog gate, 1\% energy error threshold}$
) that mathematically necessitate the creation of sequence gaps during generation. [^1] The
non-authoritative issue document identifies the index assumption as a blocking failure,
corroborating the architectural mismatch. [^1]

### Confidence

High. The logical requirement for an associative map stems directly from the immutable physical
mechanics of the Stage 2 and Stage 3 filtering process. No viable alternative mathematical
explanation exists for the consistent presence of ID gaps, rendering index-based mapping permanently
obsolete.

### Verification suggestion

Execute a dry run of the Curriculum Training Loop utilizing the newly integrated TrajectoryIndex
class on a controlled directory known to possess a simulated 30% gap rate. Monitor the diagnostic
logs and error streams during the automated extraction of 10,000 randomized batches. The successful
completion of this test without raising a single KeyError or IndexError will verify the associative
mapping.

## §3.3 Resolution: M11 (Unloaded Blacklist)

### Verdict / recommendation

The pipeline engineering must be modified to integrate the reading of the
problematic_ics_blacklist.json file directly into the core DataLoader initialization logic. The
array of blacklisted identifiers must be parsed into memory, and any matching trajectory file must
be forcefully and systematically excluded from the training set, utterly independent of its
performance on preceding static metric gates. The total integer count of excluded blacklisted files
must be logged to standard output alongside the initialization metadata.

### Reasoning

The omission of the problematic initial condition blacklist from the active ingestion sequence is
superficially categorized as a major data quality oversight, but within the highly specialized
context of the Power-Enhanced SkipResNet (SQR-SkipResNet) backbone, it represents a catastrophic
architectural vulnerability capable of permanently disabling the network. [^1] The chaotic dynamics
inherent to N-body systems naturally span immense physical scales; pairwise distances between
massive bodies can compress to $10^{-3}$ during close gravitational encounters and violently expand
to $10^{2}$ during subsequent excursive orbital phases. [^1]

To process these extreme ranges and prevent the associated velocity and acceleration spikes from
triggering exploding gradients, the neural architecture employs an intricate stabilization protocol.
The network heavily utilizes Layer Normalization (LayerNorm) applied exclusively on the identity
skip paths, operating in tandem with a quadratic power term $p = 2$ to bound the inputs prior to
element-wise squaring operations. [^1] The mathematical vulnerability arises when a blacklisted,
problematic initial condition—which intrinsically harbors unphysical coordinate singularities or
infinite velocities denoted computationally as $NaN_{or}Inf$ values—is unknowingly ingested into a
mini-batch. [^1]

Because the network logic normalizes inputs to a zero mean and unit variance across the feature
dimension, the introduction of a single infinite, undefined, or exponentially massive value
irreversibly skews the mean and variance computations for the entire local layer array. This
profound statistical skew immediately saturates the pre-activations of the subsequent hidden layers.
[^1] The SQR-SkipResNet backbone utilizes highly calibrated Sinusoidal Representation Network
(SIREN) layers formulated as
$\phi_{i}(\mathbf{x}) = \sin(\mathbf{W}_{i}\mathbf{x} + \mathbf{b}_{i})$. The architecture strictly
demands that pre-activations maintain a standard normal distribution to keep the sine functions in a
dynamic, non-saturated range, dictated by the precise initialization parameters where the first
layer leverages `first_omega_0` = 30 and hidden layers leverage `hidden_omega_0` = 1. [^1]

When normalization poisoning forces the inputs out of bounds, the SIREN layers saturate, losing
their capacity to represent smooth mathematical structures. Their critical capability to compute
well-behaved, higher-order continuous recursive derivatives—the very mechanism that overcomes the
spectral bias and zero-second-derivative failure inherent to standard ReLU networks—is entirely
neutralized. [^1] Consequently, the network's capacity to compute accurate physics residuals
collapses. The blacklist is the essential upstream defense mechanism against this specific form of
gradient destruction.

### Evidence

The issue document rightfully reclassifies M11 from a Major issue to a Blocking vulnerability,
acknowledging the silent corruption risks. [^1] `data_quality_assessment.md` documents the "Dead
Neuron Problem" and explicitly details the risk of unphysical values poisoning batch normalization
statistics across vast physical scales. [^1] Concurrently, `pinn_architecture.md` specifies the
LayerNorm structures and continuous $p = 2$ interaction operations that are fundamentally sensitive
to input scaling pathologies. [^1]

### Confidence

High. The underlying mathematics of Layer Normalization dictate that unphysical outliers are
completely destructive to the batch's gradient landscape. An unloaded blacklist guarantees
architectural saturation.

### Verification suggestion

Conduct an isolation test by examining the network's gradient norms with and without the blacklist
array loaded into memory. Deliberately initialize the DataLoader on a folder containing two known
blacklisted ICs alongside standard clean trajectories. A failure of the blacklist integration will
manifest algorithmically as immediate gradient explosions (yielding NaN gradients) and sudden
parameter nullification within the first 100 epochs of the training cycle.

## §3.4 Resolution: M12 (Sampling Ratio Infeasibility)

### Verdict / recommendation

The batch generation architecture must immediately adopt and enforce the adaptive thresholding
formula for collocation point selection:

$$
n \_ p t s = \min (3 2, \operatorname{int} (0. 5 \times n \_ s n a p s h o t s))
$$

per trajectory. [^1] The DataLoader's batch constructor must dynamically execute this logic sequence
based on the calculated temporal length of each individual incoming trajectory file.

### Reasoning

The structural formulation of the Physics-Informed Neural Network loss heavily relies on extracting
discrete "collocation points" along the temporal trajectory. [^1] These sampled nodes are utilized
to rigorously test the network's continuous predictions against the theoretical physics residual
penalty derived from Newton's equations of gravity. A systemic contradiction exists within the
legacy batch specification, which rigidly demands a fixed count of 32 sample points per trajectory.
[^1]

Standard tier trajectories are simulated with an output frequency designated by a

$$
d t \_ o u t = 0. 1 7
$$

parameter, yielding an average length of approximately 59 discrete snapshot arrays. [^1] Attempting
to forcibly extract 32 discrete points from a constrained 59-point trajectory necessitates a 54%
sampling ratio. Such an exceptionally high sampling density inadvertently perverts the fundamental
learning objective of the network. Instead of learning to extrapolate a continuous, smooth physical
manifold, the architecture is forced to sample nearly every available discrete computational step
within the low-resolution standard data array. This transforms the complex regression task into an
exercise in strict mathematical memorization of a low-fidelity discrete mesh.

This dynamic acutely degrades the network's Interpolation Physics Residual (IPR) capabilities. [^1]
The IPR framework computes a piecewise Cubic Hermite Interpolating Polynomial (PCHIP) over the
available data points, measuring the theoretical lower bound noise floor. [^1] When the network
memorizes the discrete mesh, it effectively overfits to the minuscule extrapolation errors inherent
to the Bulirsch-Stoer adaptive step-size calculations at those specific time nodes, rather than
generalizing the underlying Hamiltonian dynamics governed by the matched-Plummer constraint (
$H_{\epsilon}$ ).¹ By implementing the adaptive bounding cap of
$\min(32,0.5 \times n_{\text{snapshots}})$, the standard trajectories will yield a calculated
maximum of approximately 29 points. [^1] This mathematical ceiling ensures that the system's
sampling ratio never statistically exceeds 50%. Preserving this structural gap between sampled
points is mandatory; it forces the deep alternating layers of the SQR-SkipResNet backbone to
synthesize a generalized, fully continuous mathematical function across the intervening temporal
space rather than passively mimicking the local numerical outputs.

### Evidence

The `02-data-pipeline-and-validation.md` document definitively highlights the 54% sampling ratio
paradox and mathematically proposes the adaptive cap as a mitigation strategy. [^1] Furthermore, the
`data_quality_assessment.md` spec warns extensively against the phenomenon of "interpolation
blindness" and the spectral bias that occurs when neural networks fail to resolve the continuous
causal link between discrete evaluation nodes. [^1]

### Confidence

High. The implementation of a hardcoded scalar batch requirement is fundamentally and mathematically
incompatible with the highly heterogeneous, variable-length outputs natively generated by the Brutus
integrator's adaptive step-size controller. Dynamic bounding is the only physically viable
resolution.

### Verification suggestion

Initiate the DataLoader and intercept the batch output tensors prior to network input. Analyze the
temporal sequence length dimension of the returned arrays. The validation logic should confirm that
the maximum sampled point dimension dynamically caps at 29 for standard-tier input files (`dt_out` =
0.17), successfully reaching the absolute upper boundary of 32 only when parsing hierarchical or
high-density gold-standard tier files.

## §3.5 Resolution: M13 (Gold-Standard Subset Gaps)

### Verdict / recommendation

For the precise subset of 184 standard dataset IDs that lack a fully corresponding high-fidelity
gold-standard counterpart ( $dt\_out = 0.01$ ), the system architecture must implement a controlled
"graceful degradation" fallback protocol. The DataLoader logic must systematically verify the
existence of the gold file. If the verification fails, it must deliberately load the available
low-fidelity standard file (`dt_out` = 0.17) and programmatically append a boolean metadata flag
identified as `is_fidelity_fallback` = True. These flagged files must be permitted to participate in
the Stage 5 curriculum training loop, expressly overriding suggestions to unilaterally skip or
quarantine the IDs.

### Reasoning

The success of the Causal PINN in navigating highly chaotic dynamical regimes is heavily predicated
on massive dataset volume and exhaustive phase-space coverage. [^1] Within the data quality
assessment framework, Phase Space Coverage Entropy ( $H_{data}$ ) is established as a supreme metric
governing overall dataset composition. [^1] The methodology discretizes the phase space into a grid
of K bins, evaluating data diversity through Shannon Entropy mechanics. A low entropy value implies
highly clustered, mathematically similar orbits that critically fail to capture the nuanced physics
of boundary close encounters and chaotic scattering phases. [^1]

While it is undisputed that high-resolution gold-standard trajectories provide exceptionally dense
temporal arrays optimized for enforcing the soft matched-Plummer Hamiltonian ( $H_{\epsilon}$ ) loss
regularizer [^1], the outright exclusion of 184 physically stable configurations severely and
artificially reduces the global phase-space entropy of the dataset. The SQR-SkipResNet backbone is
not fragile; it leverages robust, infinitely differentiable ( $C^{\infty}$ ) SIREN layers designed
to execute deep, stable interpolation sequences. [^1] Therefore, the network maintains the profound
capability to extract highly meaningful, low-frequency dynamic orbital trends even from
standard-resolution (dt = 0.17) data.

Permitting these files to act as fallbacks prioritizes mathematical diversity over narrow temporal
precision. However, the `is_fidelity_fallback` = True boolean flag is of critical operational
importance. It permits the downstream architecture—specifically the probabilistic stiffness-aware
weighting mechanisms—to identify the low-resolution nature of the tensor. If the local curvature of
the fallback trajectory implies a severe high-frequency interaction event, the network logic can
dynamically de-prioritize the specific trajectory, acknowledging that the coarse dt = 0.17 temporal
sampling lacks the density to accurately resolve the interaction.

### Evidence

The `02-data-pipeline-and-validation.md` document rightfully classifies the 184 missing gold
counterparts as a Major issue (which degrades correctness) rather than a Blocking issue, noting
specifically that training can successfully proceed utilizing a standard-fidelity fallback
structure. [^1] The canonical `data_quality_assessment.md` spec establishes Phase Space Entropy,
dataset diversity, and importance resampling as mathematically paramount to preventing spectral bias
in PINN performance. [^1]

### Confidence

Medium. Integrating low-resolution tensors into the late-stage high-resolution curriculum loops
carries a fractional risk of re-introducing localized spectral bias. However, the overarching
preservation of dataset volume and system entropy is probabilistically far more beneficial to the
final generalized model capability.

### Verification suggestion

Execute a comparative analysis of the dataset's global Phase Space Coverage Entropy ( $H_{data}$ )
immediately before and after integrating the 184 fallback tensors into the ingestion stream. The
computed Shannon Entropy metric should demonstrate a marginal but measurable increase. Concurrently,
track the aggregate validation loss to ensure the inclusion of the lower-fidelity data does not
induce a disproportionate global residual spike.

## §3.6 Resolution: D7 (Minimal Footers and Tol Parameter Heterogeneity)

### Verdict / recommendation

To resolve the metadata heterogeneity surrounding the 219 standard gold files missing explicit
string tolerance metadata, the pipeline logic must dynamically assign the folder-level default
tolerance parameter of tol = 1e-13. Concurrently, the parser must inject a specialized
`tol_confidence` metadata string key into the generated trajectory dictionary. The assigned value
shall strictly evaluate to 'direct' if the parameter was explicitly parsed from the raw file's
footer string, or 'inferred' if the parameter was absent and populated via the default fallback
mechanic. The integer count of all inferred instances must be logged. The trajectory completeness
gate must strictly prioritize the `final_timestep` value and the physical conservation metrics over
the schema completeness of the text footer.

### Reasoning

The high-precision integration of chaotic initial conditions relies on the Brutus C++ engine, which
executes the Bulirsch-Stoer extrapolation method intertwined with arbitrary-precision arithmetic
libraries such as GMP/MPFR. [^1] The local truncation error of the integrator, governing the bounds
of physical precision, is strictly controlled by the tolerance (tol) parameter. [^1] The discovery
that 592 files explicitly define a strict 1e-14 tolerance while 219 files omit the string entirely
introduces an epistemological anomaly in the data provenance record. [^1]

However, executing a pipeline halt or initiating massive recalculations over absent text metadata
fundamentally contradicts the physics-first philosophy underpinning the entire data validation
protocol. The physical validity and learnability of a three-body trajectory is not mathematically
proven by the syntax of its trailing text footer, but by the irrefutable evidence of its inherent
physical conservation laws. These laws are quantified algorithmically through the Symplectic
Conservation Score (SCS) and the Interpolation Physics Residual (IPR). [^1] If an integrated
trajectory completes its required temporal evolution without failing ( `final_timestep` ≥ 9.5 ) and
achieves a highly stabilized Hamiltonian drift resulting in an SCS ≤ -5 [^1], the mathematical
structure of its physical manifold is irrefutably intact. This physical integrity holds true
regardless of whether the system utilized a $10^{-13}$ or $10^{-14}$ tolerance bound during its
derivation. Tracking the differential origin of the parameter via the `tol_confidence` flag provides
an exhaustive data provenance record suitable for forensic error-traceability, fulfilling the
administrative requirements without manifesting as an artificial, non-physical roadblock to the
continuous learning cycle.

### Evidence

The issue document precisely identifies the specific numeric subset of 219 minimal footers and the
competing 1e-14 boundary level present in adjacent files. [^1] Crucially,
`data_quality_assessment.md` establishes that dynamic metrics such as Hamiltonian drift, local
curvature, and phase-space entropy supersede raw numeric integration tags when dictating a
trajectory's ultimate viability for Causal PINN ingestion. [^1]

### Confidence

High. While administrative metadata standardization is a requirement for reproducibility, physical
conservation metrics serve as the absolute and supreme arbiter of valid mathematical data in
physics-informed learning frameworks.

### Verification suggestion

Initialize the modified parser algorithm over the target directory containing the standard gold
subset. Programmatically assert that the resulting dataset compilation yields exactly 219 unique
dictionary objects mapping to `tol_confidence` == 'inferred' and exactly 592 objects mapping to
`tol_confidence` == 'direct'.

## §3.7 Resolution: M16 (Temporal Resolution & Collocation Density Heterogeneity)

### Verdict / recommendation

The neural architecture must execute a fundamental paradigm shift, transitioning from a uniform,
naive collocation density model to a mathematically rigorous, temporally scaled,
probability-weighted architecture. The DataLoader module must be configured to dynamically expose
the unique `dt_out` parameter bound to each trajectory tensor.

The batch constructor must then calculate and allocate supplemental collocation points utilizing the
following strict inverse-scaling formula:

$$
\mathrm {n\_col\_per\_traj} = \text { base\_n\_col} \times \left(\frac {\mathrm {dt\_base}}{\mathrm {dt\_out}}\right)
$$

where the highest-resolution tier, `dt_base` = 0.01 , serves as the immovable mathematical baseline.
[^1]

Crucially, the subsequent allocation of these calculated points must not be distributed uniformly
across the temporal domain axis. Instead, they must be probabilistically clustered utilizing the
trajectory's continuous Stiffness-Aware Sampling Density (SASD) profile acting as the core weighting
function. This ensures node density is focused precisely on the localized regions of extreme
temporal curvature.

### Reasoning

The pipeline's reliance on three discrete, highly stratified temporal resolutions (

$$
d t \_ o u t \in \{0. 0 1, 0. 0 8, 0. 1 7 \}
$$

) generates a profound systemic vulnerability computationally categorized as a "collocation density
mismatch". [^1] If the network architecture applies a purely uniform sampling regime across these
disparate outputs, a standard-tier trajectory generated at dt = 0.17 effectively receives exactly
seventeen times fewer physics-sampling points per absolute physical second compared to a
high-fidelity gold trajectory at dt = 0.01 .

Physics-Informed Neural Networks learn their governing logic by continuously minimizing a complex
composite loss function. A critical sub-component of this function is the physics residual, which
evaluates the exact degree to which the network's continuous coordinate predictions obey the
theoretical differential laws of gravity. In the chaotic three-body paradigm, interactions are
heavily non-linear. If sparse, uniform collocation points span a violently complex close
gravitational encounter within a low-resolution standard trajectory, the neural network's
SQR-SkipResNet-SIREN backbone suffers from severe "spectral bias". [^1] The optimization landscape
favors low-frequency representations, leading the network to synthesize a smooth, simplistic
"mean-field" approximation of the tight binary orbital interaction, wholly failing to model the
high-frequency acceleration spikes characterizing the chaotic scattering event. [^1]

This systemic blindness is acutely compounded by the intrinsic limitations of the Stiffness-Aware
Sampling Density (SASD) metric. The SASD algorithm is mathematically designed to detect instances
where the numerical integrator's step size is excessively large relative to the system's local
characteristic physical timescale ( $\tau_{char} = ||v||/||a||$ ). [^1]

However, SASD operates under a "floor effect"; if the base temporal sampling is so incredibly low
that the entirety of a high-velocity close encounter mathematically transpires between just two
discrete integration nodes, the SASD metric is fundamentally blind to the event, registering no
stiffness anomaly. [^1]

Scaling the base collocation count inversely by the scalar `dt_base` / `dt_out` algorithmically
equalizes the base physical constraint density across all varying data fidelity tiers, forcing
low-resolution trajectories to generate synthetic evaluation nodes. By subsequently overlaying the
SASD-weighted probability distribution onto this scaled count, the framework mathematically
guarantees that the deep SIREN layers receive highly dense, localized recursive derivative signals
during the exact milliseconds of maximum physical acceleration.

### Evidence

The `02-data-pipeline-and-validation.md` document exhaustively defines the three resolution tiers
and mathematically proposes the inverse-scaling proportional equation. [^1] The
`data_quality_assessment.md` specification thoroughly details the formulation of the SASD metric,
defining the characteristic timescale and issuing severe warnings regarding the dangers of spectral
bias resulting from under-sampled physical cusps. [^1] Additionally, `pinn_architecture.md` dictates
the mathematical necessity of evaluating the matched-Plummer Hamiltonian ( $H_{\epsilon}$ ) to
resolve the sharp acceleration spikes inherent to close encounters. [^1]

### Confidence

High. The fundamental necessity of accurately resolving the highest-order derivatives of the
positional vector within a SIREN architecture dictates that temporal node density must dynamically
correlate with the local velocity-acceleration vectors defined by $T_{char}$. Inverse scaling
coupled with SASD probability weighting is the only viable mathematical defense against spectral
bias.

### Verification suggestion

To empirically verify the scaling dynamic, render a temporal histogram tracking the distribution of
selected collocation points for a known standard trajectory (dt = 0.17) executing a highly chaotic
close encounter sequence. The graphical output must display a massive, disproportionate density
spike exactly aligned with the physical timestamp of the orbital encounter, irrefutably
demonstrating that the `dt_out` scaling and the SASD weighting algorithms are actively and
dynamically molding the physical loss landscape.

## §3.8 Adjudicating the "Seed Conflict" (SCS Thresholds)

### Verdict / recommendation

The core recommendation outlined in the non-authoritative issue document—specifically proposing
Symplectic Conservation Score (SCS) gate ratios of >1e-6 for prescreening functionality and <1e-8
for Stage 5 high-resolution evaluation [^1] —is mathematically erroneous, definitionally flawed, and
strictly forbidden from production deployment.

The validation pipeline must exclusively implement and enforce the locked post-v1.3 gate officially
codified in the authoritative Data Quality Assessment specification. [^1] The singular, unified
threshold algorithm is to: Reject any trajectory where the raw Hamiltonian drift evaluates to
$\epsilon_{H} > 10^{-5}$, which computes mathematically and strictly to an SCS > -5.

The extremely tight 1e-6 target value is to be exclusively isolated and utilized solely as a
specialized diagnostic success criterion reserved for the minimal subset "Overfit Challenge" phase,
testing dynamic optimization constraints rather than acting as a universal production volume filter.
[^1]

### Reasoning

The profound discrepancy surrounding the Symplectic Conservation Score thresholds, identified by the
manifest as the "Seed Conflict," represents the most critical conceptual and mathematical
contradiction within the entire external research package. [^1]

Adjudicating this conflict requires a deep dive into the mathematical definitions of symplectic
conservation laws and a forensic cross-referencing against the explicitly documented specification
errata.

The mathematical formulation of the Symplectic Conservation Score is structurally defined as a
base-10 logarithmic transformation applied directly to the raw Hamiltonian drift of the system:

$$
S C S = \log_ {1 0} (\epsilon_ {H}) \quad . ^ {1} \text {Under this rigid definition, a physical drift limit of} 1 0 ^ {- 5} \text {translates}
$$

cleanly and directly to an integer SCS value of $-5$. The thematic issue document
(`02-data-pipeline-and-validation.md`) attempts to unilaterally declare an active rejection
threshold of SCS $>1\mathrm{e} - 6$. This proposition is mathematically illiterate and
fundamentally incompatible with the concept of logarithmic scoring. The standard scientific notation
1e-6 strictly applies to a linear error measurement bound ( $\epsilon_{H}$ ), not to the resulting
logarithmic output space of the SCS metric.

Further forensic investigation into the `data_quality_assessment.md` document reveals the explicit
origin of this mathematical conflation. A dedicated "Source Issues" tracking section details
historical tracking codes SI-DQA-002 and SI-DQA-003. [^1] This documented erratum explicitly
acknowledges that the original, legacy LaTeX source files suffered from a critical syntactic
inconsistency, failing to properly distinguish between the raw Hamiltonian drift variable (
$\epsilon_{H}$ ) and its transformed logarithmic representation ( $SCS$ ). The authoritative,
corrected specification explicitly recalibrated the mathematical reject gate to the standardized

$$
\epsilon_ {H} > 1 0 ^ {- 5}, \text {   or   interchangeably,   } S C S > - 5.
$$

Attempting to implement the issue document's excessively stringent, misinterpreted 1e-6 boundary
across the entire vast production pipeline would induce a systemic catastrophe. It would force the
algorithm to systematically and erroneously purge thousands of mathematically sound, "Marginal"
$(-6 < SCS \leq -5)$ class trajectories that display perfectly acceptable Hamiltonian drifts. This
aggressive culling would artificially starve the causal network of critical volume, aggressively
degrading the global Phase Space Coverage Entropy $(H_{data})$ necessary for generalized chaotic
sequence learning.

| Metric | Variable | Mathematical Definition | Valid Boundary Limit | Interpretation Error (Seed Conflict) |
| --- | --- | --- | --- | --- |
| Hamiltonian Drift | $\epsilon_H$ | Linear deviation from initial state | $\epsilon_H \leq 10^{-5}$ | Conflated with logarithmic scale in legacy issue doc |
| Symplectic Conservation Score | SCS | $\log_{10}(\epsilon_H)$ | $SCS \leq -5$ | Erroneously proposed as > 1e-6 |

### Evidence

The package manifest `RESEARCH-CONTEXT-MASTER.md` explicitly flags the "Seed Conflict" as a primary
structural contradiction between the legacy issue document and the locked, finalized post-v1.3 gate
rules. [^1] Most critically, the canonical `data_quality_assessment.md` specification explicitly
defines the $SCS = \log_{10}(\epsilon_{H})$ transform mapping and definitively corrects the gate to
$SCS > -5$ via the integrated erratum tracking code SI-DQA-002. [^1] Furthermore, the
`02-data-pipeline-and-validation.md` document possesses an internal contradiction, acknowledging
deep within its text that the < 1e-6 value is actually intended as a diagnostic tool for isolated
subset overfit challenges, actively contradicting its own header recommendation to deploy it as a
universal filter. [^1]

### Confidence

High. The adjudication relies entirely on explicit mathematical definitions (base-10 logarithmic
scaling) and explicitly documented, traceable LaTeX errata formalized within the canonical framework
specifications. The contradiction in the candidate issue document is a confirmed arithmetic taxonomy
error.

### Verification suggestion

Perform a code review on the active Python screening module responsible for phase 1 ingestion.
Locate the conditional operator tied to the Hamiltonian logic. Verify that the system explicitly
computes math.log10(epsilon_H) and strictly compares the resultant float against the integer value
-5. If the flawed linear threshold of 1e-6 or -6 is detected in the global production logic, raise
an immediate architectural exception.

## Open items register

In strict, unyielding compliance with the foundational rules of evidence and epistemological
boundary constraints, the following specific domains are formally logged as unresolvable items.
Their exclusion is a direct physical result of deliberate package truncation, explicit scope
exclusion, or missing external inputs beyond the boundary of the provided snapshot files.

### 1. Additional Input Needed: The PKG-02 Framed Research Questions Catalog.

**Missing Item:** The explicit textual enumeration of the overarching research questions (e.g.,
Q-01, Q-02) originally located within the truncated subsection of the `RESEARCH-CONTEXT-MASTER.md`
file. [^1]

**Systemic Impact:** While this formal report successfully inferred and executed the required
analytical targeting by systematically adjudicating the operational contradictions listed throughout
the `02-data-pipeline-and-validation.md` issue document [^1], a perfectly synchronized 1:1
question-to-answer mapping matrix is impossible without access to the localized source text string.

### 2. Additional Input Needed: The PKG-03 CLM Claims Register Data Table.

**Missing Item:** The complete, multi-row tabular dataset comprising the Claims Register (originally
sourced from `claims-table.md` ), which mathematically links unverified scatter plots and visual
figures to exact CLM-designated IDs and boolean verification states. [^1]

**Systemic Impact:** Specific dataset figures and numerical ratios embedded within visual matrices
could not be cross-referenced against confirmed verification statuses.

Consequently, all logic, recommendations, and thresholds generated within this report were derived
strictly from first-principles physics, mathematical taxonomy, and documented specification errata,
entirely bypassing any reliance on unverified statistical plots.

### 3. Additional Input Needed: The Interim Erratum text (`ERRATUM-2026-06-10.md`) and D-05 Consolidated Dataset Context.

**Missing Item:** The full textual context of the broader dataset domain and the expansive
correction provenance boundaries historically tracked within the interim erratum documentation. [^1]

**Systemic Impact:** While the most operationally critical corrections (e.g., the SI-DQA-002 SCS
logic repair) were successfully recovered from deep within the Data Quality Assessment framework
file [^1], broader, non-critical provenance history checks are fundamentally deferred pending
document restoration.

### 4. Out of Scope: The pinn/ Live Codebase Infrastructure.

- **Excluded Item:** The canonical Python operating script designated as
  `pinn/data-processing-pipeline-full.py` and its associated library ecosystem.

**Reason for Exclusion:** Access and evaluation are explicitly excluded per the 2026-05-19 SCOPE-10
directive, which definitively prohibits grounding analytical validation in active, unverified live
repository code blocks. [^1]

### 5. Out of Scope: Deep Stage 6 Architecture Methodologies.

- **Excluded Item:** The conceptual Gap G6, defined loosely as the "Causal training mismatch not
  resolved (Option A vs. Option B architectural decision)". [^1]

**Reason for Exclusion:** The overarching framework specification `pinn_architecture.md`
successfully and conclusively defines the core SQR-SkipResNet parameter interactions. [^1] However,
macro-level architectural routing choices extending beyond the strict boundary constraints of the
data-pipeline optimization process remain intentionally deferred to parallel architectural study
cohorts.

## Works cited

[^1]: `data_quality_assessment.md`
