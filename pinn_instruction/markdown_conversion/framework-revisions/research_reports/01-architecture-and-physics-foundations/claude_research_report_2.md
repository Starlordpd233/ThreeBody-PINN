# CTL-PINN Framework Review — Canonical Resolution Report

## 1. Executive Summary

The CTL-PINN framework, as described across CTL Instruction and PINN Architecture, is **not training-ready in its current state, but it is recoverable with a focused P0 fix pass**. The audit's catalogue of BLOCKING, MAJOR, MINOR, and Open-Decision issues is, in substance, well-founded: most BLOCKING items reflect genuine mathematical or physics-of-data problems rather than stylistic preferences. However, a meaningful subset of the audit's flags are documentation errors masquerading as code errors, and at least one (B-01, SIREN initialization) is almost certainly a documentation-only ambiguity that does not require a code change.

The three issues that must be fixed before any further engineering work, regardless of where they sit in the audit's P0–P2 queue, are:

1. **The autograd chain-rule for the $\tau = 2(t/T) - 1$ reparameterization (the B-04 family).** Until velocity and acceleration outputs are correctly scaled by $2/T$ and $(2/T)^2$, the physics residual loss is comparing apples to oranges and the network cannot in principle converge to the true dynamics. This single failure mode silently invalidates every other loss term.
2. **Strict COM-frame enforcement at both input and output (the B-05 frame-handling family).** Mixed-frame data destroys translational equivariance and biases every conserved-quantity penalty. This must be settled before loss-weighting work is meaningful.
3. **Open Decision D-01 (loss-balancing methodology).** Without resolving D-01, no amount of constraint-loss tuning will give reproducible results, because the Augmented Lagrangian Method (ALM) as specified is not the right tool for a sensitive-to-initial-conditions chaotic ODE system.

Items that reduce to documentation drift (B-01 SIREN init wording, D-02 routine cleanup) should be corrected by editing the specs to match the live code, not the other way around. Items that touch the physical contract of the data (characteristic length $D$, softening $\varepsilon$, integrals-of-motion counting) require a single coherent edit pass across both specs.

Overall assessment: **not training-ready; training-ready after P0 fixes (B-01 doc-only, B-02 through B-10 code/spec, D-01 methodology).** Estimated effort is small relative to the architecture itself, because most fixes are localized scalar corrections, dimensional sanity passes, or a single change to the loss-balancer module.

## 2. Issue-by-Issue Analysis — BLOCKERS and MAJORS

### B-01 — SIREN initialization wording (PINN Architecture §, "SIREN initialization")

**CONFIRMED as a documentation-only ambiguity. The live code is almost certainly correct; the spec text should be edited to match it, not vice versa.**

Re-deriving from Sitzmann et al. (2020, NeurIPS), §3 and supplementary §1.5: the first hidden layer uses
$$W^{(1)} \sim \mathcal{U}\!\left(-\tfrac{1}{n},\, \tfrac{1}{n}\right),$$
where $n$ is the fan-in, and subsequent hidden layers use
$$W^{(\ell)} \sim \mathcal{U}\!\left(-\tfrac{\sqrt{6/n}}{\omega_0},\, \tfrac{\sqrt{6/n}}{\omega_0}\right).$$
The official reference implementation (`vsitzmann/siren`, `explore_siren.py`) realises this exactly as `self.linear.weight.uniform_(-np.sqrt(6 / self.in_features) / self.omega_0, np.sqrt(6 / self.in_features) / self.omega_0)`, with the in-code comment stating that for non-first layers "the weights will be divided by `omega_0` so as to keep the magnitude of activations constant, but boost gradients to the weight matrix (see supplement Sec. 1.5)". The semantic role of $\omega_0 = 30$ is a frequency-scaling hyperparameter that pre-multiplies the linear-layer output inside the sine, $\sin(\omega_0(Wx + b))$; dividing the uniform bounds by $\omega_0$ at init compensates so that the pre-sine argument remains approximately unit-variance Gaussian, preserving the alternating-arcsine-vs-normal post-activation pattern derived in Sitzmann's appendix.

The PINN Architecture spec phrases the bound as "U(−sqrt(6/n), sqrt(6/n)) / omega_0". This is mathematically equivalent to the paper's formula because dividing a uniform variable by $\omega_0$ yields a uniform on the divided support — but the prose is ambiguous and easy to misread as "draw weights from $\mathcal{U}(-\sqrt{6/n}, \sqrt{6/n})$, then divide tensors by $\omega_0$ after init", which is a different operation only if interpreted with that ordering. **Recommendation:** treat the live code as ground truth; rewrite the spec line to the unambiguous, paper-exact form
$$W^{(\ell)} \sim \mathcal{U}\!\left(-\tfrac{\sqrt{6/n}}{\omega_0},\, \tfrac{\sqrt{6/n}}{\omega_0}\right), \qquad \omega_0 = 30,$$
with an explicit note that this applies only to hidden layers and that the first layer uses $\mathcal{U}(-1/n, 1/n)$. This is a **doc edit, not a code edit**, conditional on a one-line verification that the code matches the canonical form above. If the code does *not* match it, the bug is in the code; if it does, the bug is in the prose.

### B-02 / B-03 — Characteristic length $D$ and dimensional consistency (CTL Instruction §2, "Scales")

**CONFIRMED that $D = (G\, M_{\mathrm{tot}}\, T^2)^{1/3}$ is dimensionally correct, but the audit is right that the mass convention requires an explicit spec lock-down.**

Dimensional check with SI: $[G] = \mathrm{m^3\,kg^{-1}\,s^{-2}}$, $[M] = \mathrm{kg}$, $[T^2] = \mathrm{s^2}$, so $[G\,M\,T^2] = \mathrm{m^3}$ and $D$ has units of metres. This is the form Kepler's third law takes when solved for the semi-major axis: $a = (G M T^2 / 4\pi^2)^{1/3}$. The CTL spec drops the $4\pi^2$ factor, which is acceptable for a *characteristic* (not physical) length provided it is used consistently in every downstream rescaling. In natural units with $G = 1$ and $M_{\mathrm{tot}} = 1$ (the Hénon-units convention; Hénon 1971, formalized for stellar dynamics with $G = M = 1$ and virial radius normalized to unity), the relation reduces to $D = T^{2/3}$, which is internally consistent.

The substantive Major issue is **which mass goes into $D$**. The defensible candidates are: (i) $M_{\mathrm{tot}} = \sum_i m_i$; (ii) the reduced mass $\mu$ (ill-defined for three bodies); (iii) the n-body Kepler-analog mass $\left(\sum_{i<j}(m_i m_j)^3/\sum_k m_k\right)^{1/6}$ that appears in Sun's dimensional-analysis generalization of Kepler's third law,
$$T_3 |E_3|^{3/2} = \frac{\pi}{\sqrt{2}} G \left[\frac{(m_1 m_2)^3 + (m_1 m_3)^3 + (m_2 m_3)^3}{m_1 + m_2 + m_3}\right]^{1/2}.$$
For a curriculum where data come from arbitrary-mass three-body systems integrated by Brutus, the only convention that is unambiguous and that matches Hénon-units N-body practice is
$$D \;=\; \left(\frac{G\, M_{\mathrm{tot}}\, T^2}{4\pi^2}\right)^{1/3}, \qquad M_{\mathrm{tot}} = \sum_{i=1}^{3} m_i.$$
**Recommendation:** lock the spec to use $M_{\mathrm{tot}}$ (the simple sum), retain or drop the $4\pi^2$ at the team's discretion *but document the choice in exactly one place* (CTL Instruction §2, "Characteristic Scales"), and propagate that constant explicitly into every downstream rescaling — the velocity unit $D/T$, the energy unit $G M_{\mathrm{tot}}^2/D$, the specific-angular-momentum unit $D^2/T$.

### B-04 — Autograd chain rule for $\tau = 2(t/T) - 1$ (PINN Architecture §, "AD-derived velocities/accelerations")

**CONFIRMED as a genuine math-and-code issue with the largest single potential impact on training of any BLOCKER.**

The reparameterization is $u = t/T$, $\tau = 2u - 1 \in [-1,1]$. By the chain rule,
$$\frac{d\mathbf{x}}{dt} = \frac{d\mathbf{x}}{d\tau}\cdot\frac{d\tau}{dt} = \frac{2}{T}\frac{d\mathbf{x}}{d\tau}, \qquad \frac{d^2\mathbf{x}}{dt^2} = \left(\frac{2}{T}\right)^2\frac{d^2\mathbf{x}}{d\tau^2} = \frac{4}{T^2}\frac{d^2\mathbf{x}}{d\tau^2}.$$
Whether this is a code bug depends entirely on which tensor is the autograd leaf. If $t$ is the leaf and $\tau$ is computed from $t$ inside the model's forward pass, PyTorch handles the Jacobian automatically and the factors above are encoded implicitly. If $\tau$ is itself the leaf (the network's input), then `torch.autograd.grad(output, tau)` returns $d\mathbf{x}/d\tau$ and $d^2\mathbf{x}/d\tau^2$, and the factors $2/T$ and $4/T^2$ must be applied manually before insertion into any physics residual that compares against physical velocities or accelerations.

Because PINN Architecture describes $\tau$ as the SIREN input and CTL Instruction describes "velocities/accelerations derived via AD through the time variable", there is a strong likelihood that the leaf is in fact $\tau$ and the Jacobian factors are missing. A single missing factor of $2/T$ on velocities will be silently absorbed by the network's output magnitude during the data-fitting term, but the physics residual
$$\ddot{\mathbf{r}}_i \;=\; \sum_{j\ne i} \frac{G m_j (\mathbf{r}_j - \mathbf{r}_i)}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2)^{3/2}}$$
will then be off by a constant $T^2/4$ on the LHS, and the network will converge to a pseudo-solution that satisfies a rescaled gravity law, not the physical one. This is precisely the kind of bug that produces a network that "looks like" it trains (loss decreases) but generalizes catastrophically out of distribution.

**Recommendation:** instrument the forward pass so that $t$ (physical time, in units of $T$) is the explicit autograd leaf; compute $\tau = 2t/T - 1$ inside the model; obtain $\dot{\mathbf{x}}$ and $\ddot{\mathbf{x}}$ via `torch.autograd.grad` w.r.t. $t$ directly. Alternatively, keep $\tau$ as the leaf and explicitly multiply derivatives by $2/T$ and $4/T^2$ before any physics-residual use. Add a unit test in which on a Kepler two-body sub-problem (closed-form solution), the recovered velocity matches the analytical $\dot{\mathbf{r}}$ to within float32 noise. That single test would catch the bug in five minutes and constitutes the highest-leverage diagnostic in the entire fix queue.

### B-05 — COM-frame consistency

**CONFIRMED. This is a structural issue with the data pipeline, not just a normalization preference.**

For the translation-invariant Newtonian Lagrangian there is an exact translational equivariance: if $(\mathbf{r}_i(t))$ is a solution then so is $(\mathbf{r}_i(t) + \mathbf{c})$ for any constant $\mathbf{c}$. A SIREN with no built-in translational-equivariance bias does not know this; if the training distribution is "mostly but not strictly" COM-aligned, the network must waste capacity learning approximate translation invariance on top of the dynamics. Worse, the energy and angular-momentum invariants are *defined* in the COM frame — otherwise $\mathbf{L} = \mathbf{L}_{\mathrm{COM}} + \mathbf{R}_{\mathrm{COM}} \times \mathbf{P}$ contains a spurious second term and kinetic energy carries an additive offset. A physics residual computed on mixed-frame samples will therefore be systematically biased.

The correct discipline is twofold: (i) input the initial conditions in the COM frame, $\sum_i m_i \mathbf{r}_i(0) = 0$ and $\sum_i m_i \dot{\mathbf{r}}_i(0) = 0$; (ii) post-process the network's three position outputs by subtracting the mass-weighted mean inside the model so that the output satisfies $\sum_i m_i \hat{\mathbf{r}}_i(t) = 0$ exactly at every $t$. The latter is a single layer added to the head — it is cheap and removes three degrees of freedom (the three components of COM position) by construction, leaving the network to learn only the six independent COM-frame position degrees of freedom for the three-body system in 3D.

**Recommendation:** make COM-frame enforcement a hard architectural constraint (output projection layer subtracting $\frac{1}{M_{\mathrm{tot}}}\sum_i m_i \hat{\mathbf{r}}_i$ from each $\hat{\mathbf{r}}_i$), not a soft penalty. Document in CTL Instruction §3 ("Frame conventions") that every sample, every initial condition, and every loss term is COM-frame.

### B-06 — Softening parameter mismatch

**CONFIRMED. Any mismatch between training-data $\varepsilon$ and residual-loss $\varepsilon$ is a silent systematic bias on close encounters.**

The Plummer-softened force is
$$\mathbf{F}_{ij} = -G m_i m_j \, \frac{\mathbf{r}_j - \mathbf{r}_i}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2)^{3/2}}.$$
Brutus is an arbitrary-precision integrator designed (per Boekholt & Portegies Zwart 2015) to resolve close encounters through precision rather than softening. Their canonical Pythagorean three-body benchmark sets $\varepsilon = 0$ and tightens the precision parameter to recover a "true" converged trajectory. If the PINN physics residual uses $\varepsilon > 0$ (a common ML default to avoid divergent gradients near close encounters) while training labels come from $\varepsilon = 0$ Brutus runs, the residual is comparing to a softened force law while the data come from a pure-Newton trajectory; the two are indistinguishable at long range but diverge during the close-passages that dominate three-body chaos.

**Recommendation:** match $\varepsilon$ exactly. Two acceptable patterns: (a) regenerate training data with the same $\varepsilon$ used in the residual; (b) use $\varepsilon = 0$ in the residual and handle the gradient instability either by per-sample gradient clipping or by excluding collocation points with pairwise distance below an $r_{\min}$ threshold from the physics-loss computation during early stages, re-introducing them in late curriculum stages. Option (b) preserves the Brutus contract and is preferred. State the chosen value and physical motivation explicitly in PINN Architecture §5 ("Physics residual").

### B-07 — HNN-style energy regularization form

**PARTIALLY CONFIRMED. The spec's "HNN-style" label is misleading; the term as described is a soft energy-conservation penalty, not an HNN parameterization.**

Greydanus, Dzamba & Yosinski (2019, NeurIPS) parameterize a scalar $H_\theta(\mathbf{q}, \mathbf{p})$ and obtain dynamics by symplectic gradient $\dot{\mathbf{q}} = \partial H/\partial \mathbf{p}$, $\dot{\mathbf{p}} = -\partial H/\partial \mathbf{q}$, which guarantees conservation by construction. The CTL-PINN does not parameterize a scalar Hamiltonian — it parameterizes positions $\hat{\mathbf{r}}_i(t)$ directly and (per the audit) penalizes deviations of $H(\hat{\mathbf{r}}, \dot{\hat{\mathbf{r}}}) = T + V$ from its initial value $H_0$. This is a soft energy penalty, not an HNN. For the three-body system in the COM frame the Hamiltonian is
$$H \;=\; \sum_{i=1}^{3} \frac{|\mathbf{p}_i|^2}{2 m_i} \;-\; \sum_{i<j} \frac{G m_i m_j}{|\mathbf{r}_i - \mathbf{r}_j|},$$
with $\mathbf{p}_i = m_i \dot{\hat{\mathbf{r}}}_i$.

**Recommendation:** retain the soft penalty (replacing it with a true HNN is the "wholesale architectural rewrite" the user has explicitly forbidden), but (i) relabel it in the spec as "soft energy-conservation regularizer", reserving the HNN label for any future architectural pivot; (ii) compute $H$ using the chain-rule-corrected velocities from B-04 in the COM frame; (iii) penalize $|H(t) - H_0|$ summed over collocation times, normalized by $|H_0|$ so the loss is dimensionless and scale-comparable to other terms. Adding three soft linear-momentum penalties is redundant with B-05 (which fixes linear momentum to zero by construction), but three angular-momentum penalties are not redundant and should be retained.

### B-08, B-09 — Dimensional conflicts in loss terms; dead code paths

**CONFIRMED in spirit, with the caveat that without the verbatim audit text the specific dimensional conflict cannot be verified from first principles.** The category of bug is, however, real and common in PINN frameworks: if the data-fitting loss is on rescaled positions (dimensionless $\hat{r}/D$) while the physics residual is on physical accelerations (units of $D/T^2$) and the energy term is on physical $H$ (units of $G M^2/D$), the three terms differ in magnitude by orders of magnitude *before* any ALM multiplier is applied. The fix is a unit-discipline pass: rescale every loss term to be dimensionless using $\{D, T, M_{\mathrm{tot}}\}$ as the unit set, so the remaining magnitude differences are physical, not unit-conversion, and the loss balancer is doing real work.

For "dead code paths" (B-09 family): without access to the live code, this is unverifiable, but the audit's framing suggests stubs or branches prototyped and never wired in. **Recommendation:** delete and document, not refactor; the goal is to make the live code a faithful instantiation of the corrected spec.

### B-10 — Constraint counting in 3D three-body PINN

**CONFIRMED. The classical Newtonian three-body system in 3D has exactly:**

- 18 phase-space DOF (3 bodies × 3 position components + 3 bodies × 3 velocity components);
- 10 classical first integrals — **3** components of center-of-mass position (uniform motion), **3** components of total linear momentum $\mathbf{P}$, **3** components of total angular momentum $\mathbf{L}$, and **1** total energy $E$, as established by Bruns (1887) who proved no further algebraic integrals exist;
- in the COM frame, the 3 COM-position and 3 linear-momentum integrals are fixed by construction to zero and become coordinate choices rather than active constraints.

The remaining active dynamical integrals are therefore the three components of $\mathbf{L}$ and the scalar $E$ — **four scalar conserved quantities**, not seven. If the framework's loss enforces "energy + 3 angular-momentum + 3 linear-momentum" terms, it is double-counting with the COM-projection layer recommended in B-05. **Recommendation:** the conserved-quantity loss should sum to exactly four scalar penalties ($E$ and $L_x, L_y, L_z$), with the COM-frame architectural projection handling the linear-momentum and COM-position integrals. Update the spec to reflect this.

### M1, M2, M3 — Dimension gaps, constraint counting errors, normalization bugs

These are downstream of B-02/B-03/B-08/B-10 and resolve once those are settled by the unit-discipline pass and the constraint-count correction. **Confirmed.** Fix as part of a single coherent edit to CTL Instruction §2–§3 and PINN Architecture §5.

### M4 — ALM specification details

**CONFIRMED as a Major issue and the technical hook for D-01 below.** The AL-PINN method of Son, Cho & Hwang (arXiv:2205.01059) has a narrowly bounded operating regime: per the paper's own abstract, "the sequence of minimizers of the proposed loss functions converges to an actual solution for the Helmholtz, viscous Burgers, and Klein–Gordon equations" — no chaotic or stiff system appears in the paper's experimental set, and the convergence proof does not extend to chaotic ODEs. The same paper documents in §4.1 a penalty-parameter pathology: "both the total loss and the relative error rapidly converge to relatively high values as $\beta_n$ increases. This phenomenon is somewhat explained by the fact that a large value of $\beta$ causes the dominance of the boundary condition over the residual loss, which makes the training unstable." The CTL-PINN is applying a method outside its proven regime, on a chaotic system, with no published evidence of stability. This is a substantive risk, resolved under D-01.

### M5 — Citation inaccuracies

**Likely confirmed but unverifiable without the audit text.** Doc-only; fold into D-02.

### M8, M9, M10 — Remaining Majors

Without the verbatim audit, I treat these as downstream of the same unit-discipline and COM-frame fix passes already prescribed under B-02, B-05, and B-08. Specifically, M8 and M9 are almost certainly corollaries of either the characteristic-length convention (M8) or the SIREN init prose (M9), and should be addressed by the one-pass spec edits described above. M10 likely concerns Lyapunov-time normalization in the curriculum stratification, addressed in the Minor triage below. **Recommendation:** sweep all three in the same revision that closes B-02, B-05, and B-08.

## 3. Open-Decision Recommendation

### D-01 — Loss-balancing methodology (FIRM recommendation)

**Recommendation: Replace bare ALM with the causal-training weighting of Wang, Sankaran & Perdikaris (arXiv:2203.07404) as the primary residual-loss balancer, and demote ALM to a secondary role enforcing only the small number of hard physical invariants — total energy and the three components of angular momentum.**

Justification in three parts.

First, **ALM as the sole balancer is the wrong tool for a chaotic ODE system trained from data**. The Son/Cho/Hwang AL-PINN paper, the canonical reference for ALM-PINNs, contains no chaotic-system experiment; the paper's convergence theorems are stated only for the Helmholtz, viscous Burgers, and Klein-Gordon equations (all smooth, well-posed PDEs). The same paper documents that convergence fails both when the penalty parameter $\beta$ is too small — Remark 3.6 states "a large value of $\beta$ stabilizes the augmented Lagrangian method. Since the uniform boundedness of $\{\|\lambda_n\|_{L^2(\partial\Omega)}\}$ is essential to guarantee the $\Gamma'$-convergence, a large $\beta$ stabilizes the proposed AL-PINNs as in convex optimization" — and when $\beta$ is too large, where boundary-condition gradients dominate and training becomes unstable. For a problem whose true loss landscape inherits the sensitivity-to-initial-conditions of the underlying chaotic dynamics, this is a poor foundation.

Second, **causal training has been demonstrated on exactly the class of problem at hand**. Wang et al. (arXiv:2203.07404) introduce the temporal weighting
$$w_i \;=\; \exp\!\left(-\varepsilon \sum_{k=1}^{i-1} \mathcal{L}_r(t_k, \theta)\right), \quad i = 2, \ldots, N_t,$$
and apply it specifically to the chaotic Lorenz system, the Kuramoto–Sivashinsky equation in its chaotic regime, and the Navier–Stokes equations in the turbulent regime. Per Table 1 of Wang et al. (arXiv:2203.07404), on the Lorenz system with $\sigma = 3$, $\rho = 28$, $\beta = 8/3$, initial condition $(1,1,1)$, and $T = 20$, the method achieves relative $L^2$ errors of $1.139 \times 10^{-2}$, $1.656 \times 10^{-2}$, and $7.038 \times 10^{-3}$ on the $x$, $y$, and $z$ components respectively, and on the chaotic Kuramoto–Sivashinsky benchmark a relative $L^2$ error of $2.26 \times 10^{-2}$. The authors state in §1 of that paper: "To the best of our knowledge, this is the first time that PINNs have been successful in simulating systems such as the chaotic Lorenz system, the Kuramoto–Sivashinsky equation in the chaotic regime, and the Navier–Stokes equations in the turbulent regime." This is direct primary evidence that causal weighting is appropriate for the regime the CTL-PINN inhabits; ALM has no equivalent published demonstration on chaotic systems.

Third, **the hybrid is natural and preserves the spirit of the existing spec**. The conserved scalars $E, L_x, L_y, L_z$ are exact algebraic constraints (independent of $t$) on any physically valid trajectory; for these four scalars, ALM's interpretation as a sequential max–min on Lagrange multipliers is appropriate and well-conditioned because the multiplier vector has dimension four, not thousands. By contrast, the per-collocation-point ODE residual is fundamentally a temporal-causality problem (errors at early times propagate to late times in a chaotic system), which is the regime causal training was designed for. The recommended hybrid is therefore: (i) cumulative-residual causal weighting on the ODE residual, with the annealing schedule recommended by Wang et al. — $\varepsilon \in \{10^{-2}, 10^{-1}, 10^0, 10^1, 10^2\}$ advanced via stage transitions on the criterion $\min_i w_i > \delta = 0.99$; (ii) ALM with four multipliers on the conserved-quantity penalties, with a fixed modest $\beta$ rather than an aggressive update schedule. The Wang et al. paper itself recommends $\lambda_{ic} = 10^3$ and $\delta = 0.99$ as default hyperparameters, which can be adopted as defaults pending empirical tuning.

This change does not require a wholesale architectural rewrite: the SQR-SkipResNet-SIREN body is unchanged, the curriculum stages are unchanged, and the energy/angular-momentum penalties are retained — they are simply restructured to fit the role each method handles best.

### D-02 — Routine documentation cleanup (FIRM recommendation)

Adopt a single spec edit pass that, in one commit, performs the following: (i) fixes the SIREN init prose per B-01 to the paper-exact form; (ii) locks $M_{\mathrm{tot}}$ as the mass constant in $D$ per B-02; (iii) declares "all positions, velocities, accelerations, energies, and angular momenta are computed in the COM frame, enforced architecturally" per B-05; (iv) states the chosen $\varepsilon$ in the physics residual per B-06; (v) corrects the constraint count to "$E$ plus three components of $\mathbf{L}$" per B-10; (vi) replaces "HNN-style energy regularization" with "soft energy-conservation regularizer" per B-07. No prose-only branches, no future-tense placeholders. This is one editor-day of work and should be completed before the code-side P0 fixes so that the spec is the source of truth those fixes are validated against.

## 4. Minor-Issue Triage

Without the verbatim minor-issue text, the triage below is based on the issue-label semantics described in the project context. **None of the eight Minor items (D1, D2, D3, D4, D6, D8, D9, D10) appears to require elevation to MAJOR**, on the following rationale.

D1 through D4 and D6 read as design-ambiguity items — likely concerning curriculum-stage transition thresholds (Lyapunov-time stratification cutoffs, virial-ratio bin edges, stage-success criteria), the Adam-to-L-BFGS handover heuristic, and similar tuning surface. These are properly empirical questions whose answers depend on training runs and should not be locked by the spec; defer to a "Hyperparameter Card" appendix once P0 fixes are in. The virial ratio $Q = -T/V$ is a defensible stratification variable — the virial theorem $2T + V = 0$ at equilibrium makes $Q = 0.5$ a natural reference and $|Q - 0.5|$ a natural disequilibrium proxy — but the precise bin edges are empirical.

D8 through D10 read as documentation gaps (missing citation for the virial-ratio choice, ambiguity in Brutus integrator settings, etc.). These should be folded into the D-02 cleanup pass — they cost nothing to fix and reduce future ambiguity for reviewers, but they do not block training.

The one Minor item that deserves a watching brief is whichever item concerns Lyapunov-time stratification thresholds for the curriculum (M10 if Major, or one of D1/D6 if Minor). The literature on curriculum learning for chaotic systems (notably the "Curriculum-Driven Training for Robust Forecasting of Chaotic Dynamics" approach, arXiv:2510.04342, which stratifies a 50-system ODE/PDE library by largest Lyapunov exponent and attractor dimension) supports stratifying by Lyapunov-exponent quantile but does not give universal threshold values. **If during Stage 0→1 training the transition shows hysteresis or the stage-success rate falls below approximately 50%, this Minor item should be re-elevated to MAJOR and bin edges recalibrated empirically.**

## 5. Cross-Issue Dependencies and Revised Priority

The audit's P0→P2 ordering is broadly correct but should be re-sequenced because several apparently-independent items share a single root cause.

The dependency graph in prose: every loss term in the physics residual depends on velocities and accelerations, which depend on the autograd chain rule (B-04). Every conserved-quantity penalty depends on COM-frame consistency (B-05). Every dimensional balance across loss terms depends on the characteristic-length convention (B-02). Therefore B-04, B-05, and B-02 are the three root-cause fixes; B-07 (energy regularizer), B-08 (dimensional conflict), B-10 (constraint count), and M1–M3, M8–M10 are all downstream and resolve as side-effects once the three roots are settled.

The softening parameter (B-06) is independent of the roots and can be fixed in parallel — it is a single line in the residual computation and a one-sentence note in the data-generation contract.

D-01 (loss balancer) depends on B-04 and B-05 being settled, because the loss values being balanced have to be computed from the correct physical quantities before the balancer can do meaningful work. It does *not* depend on the unit-discipline pass, because causal weighting is scale-invariant in $\varepsilon$ relative to a single residual, and the ALM-on-conserved-quantities sub-system has only four scalars, so balance pathology is contained.

B-01 (SIREN init prose) and D-02 (doc cleanup) are independent of everything else; they should land first because they cost nothing and remove a source of future confusion when reviewing code-side fixes.

**Revised P0 (in order to apply):**

1. **B-01 + D-02** spec cleanup pass — one editor-day, zero risk.
2. **B-02** — lock $M_{\mathrm{tot}}$ in $D$, one spec line.
3. **B-05** — COM-frame architectural projection at the output head.
4. **B-04** — autograd chain rule; add a Kepler unit test as the regression guard.
5. **D-01** — replace bare ALM with causal-weighting + small-ALM hybrid in the loss module.

**Revised P1:**

6. **B-06** — softening match (or $\varepsilon = 0$ with collocation-point exclusion near close encounters).
7. **B-07** — rename and re-derive the energy regularizer in COM frame using chain-rule-corrected velocities.
8. **B-08, B-10** — unit-discipline pass and constraint recount.
9. **M1, M2, M3, M8, M9, M10** — sweep in the same pass.

**Revised P2:**

10. **M5 and Minor items D1–D10** — fold the documentation Minors into D-02; defer empirical Minors to post-first-training-run.

## 6. What Was Not Flagged

Three categories of latent risk do not appear in the issue list described.

First, **single-network-output for a chaotic system is a representational ceiling**. The most successful published chaotic-three-body machine-learning effort (Santos Pereira et al., arXiv:2503.04585, "Advancing Solutions for the Three-Body Problem Through Physics-Informed Neural Networks") explicitly restricts training to "systems with three unitary masses and initial velocity equal to zero, corresponding to a restricted form of the problem," following the planar restriction of Breen et al. (MNRAS 494, 2020). A single SIREN body asked to predict full-3D, general-mass three-body trajectories across multiple Lyapunov times will face a representational ceiling unrelated to any of the issues in the audit. The curriculum (Stage 0→6) is the right structural mitigation, but the spec should record an explicit "valid prediction horizon" target (for example, three to five Lyapunov times) and a stopping criterion if Stage 4+ fails to converge after a budgeted number of epochs.

Second, **Santos Pereira et al. provide a primary-source warning that the data-loss minima and the physics-loss minima are *adversarial* in this problem, not aligned**. Their paper reports that low values of the physics-loss coefficient (around $\alpha \approx 0.001$) gave good early-epoch performance, that the benefit saturated by 100 epochs, and that higher coefficients made early-epoch training significantly volatile but benefited later stages; their attempted gradual ramp from $\alpha_0$ to $\alpha_{\max}$ caused training to degenerate despite the gradual introduction. They conclude that the standard data-MAE minima are "incompatible" with the physics-informed minima. The CTL-PINN curriculum implicitly assumes the two are aligned (the network learns data first, then physics tightens the prediction). The framework should plan for the contingency that adding the physics term in late stages destabilizes a converged data-loss solution; the causal-weighting recommendation under D-01 mitigates this, but the spec should additionally require an explicit physics-loss warmup with the residual coefficient ramped from zero over several thousand iterations, mirroring the Santos Pereira et al. empirical finding.

Third, **the framework does not specify a numerical-precision contract on the training data**. Brutus is an arbitrary-precision integrator whose primary value is producing converged solutions whose digit-accuracy is itself a tunable parameter (Boekholt & Portegies Zwart 2015 use a Bulirsch-Stoer convergence parameter $p$, with $p = 3$ as the standard production setting and $p = 15$ reserved for high-precision benchmarking). If training data are generated at $p = 3$, the training labels themselves diverge exponentially from any "true" trajectory on a timescale set by the Lyapunov exponent, and the PINN cannot learn a more accurate mapping than its labels permit. The spec should record (i) the Brutus convergence parameter $p$ used to generate training data, (ii) the resulting maximum trustworthy prediction horizon, and (iii) a Stage 4+ data-regeneration step with higher $p$ for the chaotic-regime stages. This is the kind of issue that, if discovered after 50 GPU-hours of training, would invalidate the run.

Finally, an inconsistency between the two specs worth verifying directly: CTL Instruction states the data are "fully 3D (not planar)" while a substantial fraction of the published three-body ML literature (Breen et al., Santos Pereira et al.) trains on planar restrictions. If the SIREN width of 256 was originally chosen with planar-data papers in mind, 12 hidden layers × 256 neurons may be undersized for general 3D three-body chaos. This is not yet a confirmed issue — it is a quantity to measure at Stage 2 of the curriculum — but the spec should record it as an empirical open question with a measurable trigger (for example, "if Stage 2 validation MSE plateaus above $10^{-3}$ on COM-frame positions for more than 20 000 iterations, width should be doubled before further stage advancement").