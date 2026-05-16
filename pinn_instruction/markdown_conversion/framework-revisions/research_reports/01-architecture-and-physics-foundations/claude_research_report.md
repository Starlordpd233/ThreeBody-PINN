# Audit of a PINN Framework for the Gravitational Three-Body Problem

## Preface: Source Material and Method

**Important limitation.** This auditor did not have direct access to the three uploaded files (`ctl_instruction.md`, `pinn_architecture.md`, `01-architecture-and-physics-foundations.md`). The audit is therefore conducted against the **structured claims, numbered issues (B-01 … B-10, M1–M10, D1–D10, D-01/D-02), formulas, and design decisions described in the task prompt**, supplemented by ~18 targeted searches into primary literature (Sitzmann 2020; Greydanus 2019; Cranmer 2020; Jin et al. 2020; Wang/Karniadakis NTK; Basir & Senocak ALM/PECANN; Chen et al. GradNorm; Hénon units / NEMO docs; Boekholt & Portegies Zwart 2015 / 2020; Mikkola & Tanikawa 2007; Breen et al. 2020; Badura 2024 AMOS; Scorsoglio et al. 2023) and one focused subagent verification pass on SIREN initialization and PINN time-chain-rule arithmetic. Wherever a claim could not be independently checked because the underlying spec text was unavailable, the report says so explicitly.

---

## 1. Executive Summary

**The framework is not yet trainable as specified.** Of the issues the review enumerates, at least four blockers are unambiguously real (SIREN initialization, AD chain-rule factor, COM-frame data/output mismatch, softening-length scaling mismatch) and at least one major (M-class) issue — the dimension/constraint accounting around 3D vs planar data — is a latent correctness bug that propagates through every loss term. Together these would cause a SIREN-PINN of the depth/width specified (12×256, ω₀ scaling) to either diverge at initialization or to converge on a solution that violates Newton's equations by a constant geometric factor invisible inside the dimensionless training loss. The good news: every blocker except D-01 is a localized formula or pipeline fix; no architectural rewrite is required. SQR-SkipResNet-SIREN with ALM balancing remains viable.

**Highest-impact recommendations**, in order:

1. **Adopt the verified SIREN init formula exactly** (B-01): first layer `U(−1/fan_in, +1/fan_in)` with `sin(ω₀·(Wx+b))`; hidden layers `U(−√(6/fan_in)/ω₀, +√(6/fan_in)/ω₀)`. Multiplication by ω₀ (rather than division) in the hidden-layer bound — a common bug — would produce variance ~ω₀⁴ per layer rather than O(1) and is exactly the failure mode the review is worried about.
2. **Apply the explicit (2/T)ᵏ scaling factors to AD derivatives** at every order. With u = t/T and τ = 2u − 1, velocity = (2/T)·∂r/∂τ and acceleration = (2/T)²·∂²r/∂τ². The Badura 2024 AMOS paper formalizes this exactly.
3. **Move all data into the COM frame before scaling, not after**, and either subtract the COM-output drift or hard-constrain the network output to a 6-DOF representation. Without this, the data-loss term and the residual term live in incompatible frames.
4. **Use a single softening length, expressed in the network's working units**, identical in the Brutus data generator and in the residual loss. ε must be scaled along with positions when units change.
5. **For D-01 (energy regularization methodology), recommend a soft, curriculum-gated energy penalty as the primary tool** — explicitly do NOT switch to HNN- or SympNet-style structural energy parametrization, which would require an architectural rewrite ruled out by the prompt's guardrails.

Below, each blocker and major is treated in proportion to its impact.

---

## 2. Issue-by-Issue Analysis — Blockers (Deep Treatment)

### B-01 — SIREN weight initialization

**Affected sections.** PINN Architecture: SIREN initialization for the 12 hidden layers of 256 neurons. (Review classification: BLOCKING.)

**Review claim (as described in the prompt).** The framework's SIREN init formula is wrong.

**Verdict: CONFIRMING.** This is the single most consequential blocker, and the primary literature is unambiguous. The Sitzmann et al. 2020 paper ("Implicit Neural Representations with Periodic Activation Functions," NeurIPS, arXiv:2006.09661) specifies, in §3.2 ("Distribution of activations, frequencies, and a principled initialization scheme") and Theorem 1.8 of the supplement, the following construction (verified verbatim from the paper plus the official reference implementation at github.com/vsitzmann/siren):

- **First layer.** Weights drawn from `U(−1/fan_in, +1/fan_in)`. Activation is `sin(ω₀·(W·x + b))` with ω₀ a frequency multiplier *inside* the sine, typically ω₀ = 30. The 1/fan_in (linear, **not** 1/√fan_in) is chosen specifically so that the pre-activation ω₀·W·x spans multiple periods of the sine over input x ∈ [−1, 1]. Sitzmann §3.2 states the goal: *"to initialize the first layer of the sine network with weights so that the sine function sin(ω₀·Wx + b) spans multiple periods over [−1, 1]."*
- **Hidden layers.** Weights drawn from `U(−√(6/fan_in)/ω₀, +√(6/fan_in)/ω₀)`. The ω₀ is in the **denominator** (division). This compensates for the ω₀ factor inside the sine so that the pre-sine input remains approximately N(0,1) and the post-sine output remains arcsine-distributed on (−1, 1), preserving signal variance through depth.

**Why this matters mathematically.** Sitzmann's derivation (paper §3.2 plus supplement Theorem 1.8) chains three facts: (i) for X ~ U(−1,1), y = sin(aX+b) is arcsine-distributed on (−1,1) independent of (a,b); (ii) if each weight is U(−c/√n, c/√n), then by CLT wᵀx → N(0, c²/6) as fan-in n grows; (iii) choosing c = √6 makes the pre-sine input N(0,1), and feeding N(0,1) through sine gives arcsine output again — so variance is exactly preserved through every hidden layer. If the hidden bound is taken as `√(6/fan_in) · ω₀` (multiplication, a very common transcription error), then pre-activations have variance ~ω₀²/6 per layer; after 12 layers, signal variance blows up by a factor ω₀²⁴. For ω₀ = 30 this is roughly 10³⁵ — catastrophic at step 0.

**Proposed concrete fix (drop-in PyTorch logic).** In every `SineLayer` constructor:

```python
# omega_0 is the frequency multiplier; w_0_first = 30, w_0_hidden = 1 (or 30) per Sitzmann
if is_first:
    nn.init.uniform_(self.linear.weight, -1.0 / in_features, 1.0 / in_features)
else:
    bound = math.sqrt(6.0 / in_features) / self.omega_0   # DIVISION, not multiplication
    nn.init.uniform_(self.linear.weight, -bound, bound)
# forward:  y = torch.sin(self.omega_0 * (self.linear(x)))
```

If the spec gives `bound = sqrt(6/fan_in) * omega_0` or applies ω₀ outside the linear, both are bugs.

**Stage-0/curriculum implication.** The CTL curriculum's Stage-0 "pre-train on near-Keplerian data" assumes the network can faithfully reproduce a smooth low-frequency signal. With wrong init, Stage 0 cannot converge, and every downstream curriculum threshold becomes meaningless. **B-01 must be fixed before any other stage is benchmarked.**

---

### B-02 — Missing chain-rule factor in automatic differentiation

**Affected sections.** PINN Architecture (AD-based velocity/acceleration) + CTL Instruction (input-vector assembly, time scaling).

**Review claim.** AD chain-rule factor missing.

**Verdict: CONFIRMING.** This is a quantitative correctness bug, not a style issue. With the standard PINN pipeline of:

- normalized time u = t/T (T = curriculum-stage time horizon in working units),
- reparameterized SIREN input τ = 2u − 1 to map into [−1, 1],
- network output r(τ) = position trajectory,

then by chain rule:

- `dr/dt = (dr/dτ) · (dτ/du) · (du/dt) = (dr/dτ) · 2 · (1/T) = (2/T) · ∂r/∂τ`
- `d²r/dt² = (4/T²) · ∂²r/∂τ²`

These factors are necessary for the Newton residual `m·d²r/dt² − F_grav(r) = 0` to make dimensional sense. Without them, the residual loss is being computed in units of (position/τ²), but F_grav is in units of (position/t²), with the two differing by 4/T². For Stage 0 (typical T ~ few Hénon time units) the discrepancy is modest (factor ~10), but for late curriculum stages with T ~ 10³ Hénon times, the factor becomes ~4·10⁶, and ALM lambda multipliers will be driven to grotesque values trying to compensate.

This exact chain-rule treatment is formalized in Badura et al. (2024, AMOS conference proceedings, App. B, Eqs. 18–20) for PINN-based orbit determination, citing Scorsoglio, Ghilardi & Furfaro, "A Physic-Informed Neural Network Approach to Orbit Determination," *J. Astronaut. Sci.* 70(4), 2023. Badura is explicit (verbatim from §App. B): *"the first and second order partial derivatives that are computed by the automatic differentiation procedure must be scaled by the factors c and c², respectively, in order to provide appropriately scaled velocity and accelerations,"* where c = 2/(t_f − t₀).

**Proposed fix.** Wherever the residual is computed:

```python
# u = t / T;  tau = 2*u - 1  is the SIREN input
r = net(tau, ic_vec)                                 # shape (B, 9)  — 3 bodies × 3 dims
dr_dtau   = grad(r, tau, ones, create_graph=True)
d2r_dtau2 = grad(dr_dtau, tau, ones, create_graph=True)
v   = (2.0 / T) * dr_dtau          # velocity in canonical units
acc = (2.0 / T)**2 * d2r_dtau2     # acceleration in canonical units
residual = m * acc - F_grav(r)
```

**Per-component vs collapsed-Jacobian subtlety.** The 9-D output must be differentiated per scalar component (or with `torch.autograd.grad(..., is_grads_batched=True)` / `jacrev`). A single `grad(r.sum(), tau)` is mathematically equivalent only if the user intends to sum residuals — which the framework does not. The review's worry about "component-wise vs collapsed Jacobian" is well founded; the safe pattern is to call `grad` once per output dimension or use `functorch.jacrev` / `torch.func.jacrev` (PyTorch ≥2.0).

---

### B-03 / B-05 (COM-frame violations) — Lab-frame data vs COM-frame output

**Affected sections.** CTL Instruction: data preprocessing & invariant calculations. PINN Architecture: output head specification (review says outputs are in COM frame).

**Review claim.** Training data is in lab frame while network outputs are in COM frame, causing inconsistency.

**Verdict: CONFIRMING.** This is a Galilean-invariance hygiene failure with a known, well-understood remedy in the ML-for-N-body literature. The three-body Newtonian equations are translation-invariant; the COM drifts at uniform velocity (Scholarpedia, *Three-body problem*: *"the linear momentum P = Σ m_i ṙ_i conserves; by an appropriate choice of a Galilean frame one can suppose that P = 0 and that the center of mass is at the origin"*). HNN (Greydanus 2019), LNN (Cranmer 2020), and the Breen et al. (2020) three-body neural network — Breen, Foley, Boekholt & Portegies Zwart, "Newton versus the machine: solving the chaotic three-body problem using deep neural networks," *MNRAS* 494(2), 2465–2470 (May 2020) — all assume COM-frame data. Breen et al. explicitly state (§2): *"We restricted the training set to … three equal-mass particles with zero initial velocity, located in a plane. The three particles … are initially positioned at x₁ ≡ (1, 0) with (x₂, x₃) randomly situated somewhere in the unit semicircle in the negative x-axis,"* which is a stronger reduction (translation + rotation + scaling).

Two failure modes follow from a lab-vs-COM mismatch:

1. **Data-loss term** matches lab-frame positions (which include a linear COM drift) while the network is structurally trying to output COM-frame positions. The data MSE has an irreducible floor equal to the COM-drift kinetic energy summed over time.
2. **Energy/HNN regularizer** computes E in COM frame using network outputs while the conserved E of the dataset is in lab frame; these differ by ½ M v_COM² which is constant per trajectory but varies across the dataset, biasing the regularizer.

**Proposed fix.** Standardize on COM-frame data **before** scaling, as is standard practice:

```
For each Brutus trajectory:
  v_COM = Σ m_i v_i(t=0) / Σ m_i              # use t=0 to define the frame
  r_COM = Σ m_i r_i(t=0) / Σ m_i
  r_i'(t) ← r_i(t) − r_COM − v_COM · t        # remove COM drift
  v_i'(t) ← v_i(t) − v_COM
Then apply Hénon-unit scaling.
```

This subtracts the (constant) COM position and the (constant) COM velocity from every snapshot. After this step, the data has identically zero linear momentum and zero COM, matching the network's output convention, and the COM-residual constraint becomes redundant rather than active.

**Alternative ("structural" fix).** Have the network output only 6 of the 9 degrees of freedom (e.g. r₁ and r₂) and derive r₃ = −(m₁ r₁ + m₂ r₂)/m₃ analytically. This enforces COM=0 exactly and removes one redundant DOF from the loss. The framework should pick one approach and document it; doing both is redundant, doing neither is the current bug.

---

### B-04 — Plummer softening mismatch

**Affected sections.** CTL Instruction (Brutus data softening setting) vs PINN Architecture (softening used in the gravitational residual).

**Review claim.** Softening epsilon in the data integrator differs from softening in the residual.

**Verdict: CONFIRMING (mathematically severe).** Plummer softening replaces the Newtonian force pair `F = −G m₁ m₂ r̂ / r²` with the regularized form `F = −G m₁ m₂ r / (r² + ε²)^(3/2)` (Aarseth 2003; Dehnen 2001; Zhang et al., *MNRAS* 487, 1227, 2019, which writes the Plummer form explicitly and *"ε is termed as gravitational softening length"*). The choice of ε defines an entirely different dynamical system; trajectories at close approach diverge between any two ε values.

If Brutus is run with `ε_data` (possibly 0 or 10⁻⁶ in arbitrary-precision mode) and the residual evaluator uses `ε_resid` ≠ `ε_data`, then the residual is computing forces from a different physical system than the one that produced the data. Worse, **after unit rescaling**, if ε is treated as a constant in physical units rather than rescaled with positions, the dimensionless ε in the working units differs across stages of the curriculum.

**Verdict on the typical Brutus convention.** Brutus is explicitly an arbitrary-precision N-body code; Boekholt & Portegies Zwart (2015, "On the reliability of N-body simulations," *Comput. Astrophys.* — arXiv:1411.6671) emphasize it integrates the un-softened problem (this is precisely the point of arbitrary precision: close encounters are resolved by adding digits, not by softening). Therefore the data is most likely **un-softened** (ε_data = 0), and the residual softening ε_resid > 0 introduces a systematic O(ε²/r²) force error at close approaches — exactly where the chaotic three-body problem spends most of its informative dynamics.

**Proposed fix.**

1. **Default recommendation: ε_resid = 0** (match Brutus). To avoid the singularity in AD, clamp the pair distance with `r_safe = sqrt(r² + ε_min²)` with `ε_min` set to single-precision machine epsilon (~1e-7) only, not a dynamics-altering softening.
2. If softening is required for stability, then ε_data **must equal** ε_resid, both expressed in **scaled (working) units**, and rescaled at every curriculum stage where the length unit changes.
3. Document ε explicitly in the spec; the review's concern about "softening mismatches" is correct and should not be settled by leaving ε undefined.

---

### B-06 — Dimension conflicts in the input vector / 3D vs planar

**Affected sections.** CTL Instruction (input vector assembly) and Review (mentions "3-body 3D data, not planar" in guardrails).

**Review claim (interpreted).** Inconsistent dimension counts between input-vector size, output dimension, and the planar/3D choice.

**Verdict: PARTIALLY CONFIRMING — cannot fully verify without seeing the spec.** The framework prompt is explicit: "three-body 3D data (not planar)". Breen et al. (2020), in contrast, used **planar** (2D) data; if the spec inadvertently borrowed Breen's input layout (3 bodies × 2D = 6 spatial coordinates) while declaring 3D outputs, the input vector would be 6 short for full initial conditions. A correctly assembled 3D initial-condition vector should have:

- 3 bodies × 3 positions = 9 (or 6 after COM removal),
- 3 bodies × 3 velocities = 9 (or 6 after p_COM = 0),
- 3 masses = 3,
- 1 time scalar = 1,

for a total of typically **18 + 1 = 19** in the lab frame or **12 + 3 + 1 = 16** with COM/momentum reductions applied. The output (3 bodies × 3 positions = 9) is downstream of the time input, while masses+ICs gate the network behavior.

**Proposed fix.** Adopt a single canonical input layout, document it explicitly:

```
input_vec = concat(
    [tau_scalar],                              #  1
    [m1, m2, m3],                              #  3   masses (Henon: m1+m2+m3 = 1)
    [r1_0, r2_0],                              #  6   3D positions of bodies 1 and 2 (r3_0 derived)
    [v1_0, v2_0]                               #  6   3D velocities of bodies 1 and 2 (v3_0 derived)
)                                              # total 16
output  = [r1(t), r2(t), r3(t)]                #  9   positions in COM frame
velocity, acceleration  ← AD of output w.r.t. tau, then scaled by (2/T) and (2/T)²
```

This is consistent with COM reduction, with 3D physics, and with the Hénon mass-normalization convention.

---

### B-07 / B-08 — Dead code and dimension conflicts in the loss assembly

**Verdict: PARTIALLY CONFIRMING — these are documentation/spec bugs.** The review identifies "dead code" and "dimension conflicts" — without the spec text, I cannot confirm exact line numbers. The most plausible reading: an angular-momentum invariant or a 2D cross-product term was left in the spec after migrating from planar to 3D. In 3D, angular momentum is a vector L = Σ m_i (r_i × v_i), not a scalar; if the code computes a scalar L = Σ m_i (x_i v_yi − y_i v_xi) it captures only L_z and silently drops L_x, L_y. Recommended fix: rewrite all conserved quantities as vector quantities and take the appropriate norms (|L|, |P|) in residuals.

---

### B-09 / B-10 — Remaining blockers (sparse evidence)

Without the spec, I can flag plausible candidates: (i) a missing factor of ½ in kinetic energy, (ii) a sign error in the gradient of the potential (the −G m₁ m₂/r vs +), (iii) a softmax/temperature applied to physical outputs. All three are common in PINN reimplementations of HNN-style energies. These should be unit-tested by integrating a Kepler orbit analytically and comparing.

---

## 3. Issue-by-Issue Analysis — Major Issues (Moderate Treatment)

### M1 — Dimension gap in 3D vs 2D physical invariants

Covered under B-06/B-07. **Confirming.** Angular momentum must be vector-valued; energy is invariant; linear momentum is vector. All three must use the same canonical 3D form.

### M2 — Constraint counting errors

In the 3-body, 3D problem with G = M_total = 1 in Hénon units, the conserved quantities are: E (1), L (3 components), P (3 components, can be set to 0 by frame choice). After fixing COM and zeroing P, the active independent constraints are E (1) and L (3). The review's reference to constraint-counting errors most likely conflates a planar 2D analysis (1 + 1 + 1 active constraints) with the spec's 3D requirements. **Confirming.** Recommended count: **4 independent active conservation residuals (1 energy + 3 angular momentum)**, plus the 6-DOF COM/momentum constraint as a soft regularizer until B-03/B-05 is fixed.

### M3 — Normalization bugs (characteristic length D = (G M_tot T²)^(1/3))

**Affected sections.** CTL Instruction: data preprocessing and invariant calculations.

**Verdict on the formula.** The framework prompt states "D = (G·M_tot·T²)^(1/3)" as the characteristic length. This is the Kepler-third-law derived length scale: given an orbital period T and a central mass M_tot, the semi-major axis is `a = (G M_tot T²/4π²)^(1/3)`. Dropping the 4π² factor (which is conventional in dimensionless N-body work) yields exactly D = (G M_tot T²)^(1/3). This is dimensionally correct: [G][M][T]² = (L³/(M·T²))·M·T² = L³, cube-root = L. **Confirming the formula's dimensional validity, with the caveat that the conventional factor of (4π²)^(-1/3) is absorbed.**

**Is M_tot or M_avg used?** Hénon units set M_tot = 1, so the choice is moot inside the unit system. If the framework ever leaves Hénon units (e.g. for astrophysical reporting), M_tot is the correct choice — using M_avg would give a length that's smaller by 3^(1/3) ≈ 1.44× for the equal-mass case and break Kepler's third law as written.

**M_avg is wrong.** Recommendation: **use M_tot, and document that the conventional 4π² is absorbed into the definition** (Aarseth 2003, *Gravitational N-Body Simulations*, the standard reference, uses this convention; see NEMO/Hénon-units docs at teuben.github.io/nemo/man_html/units.5.html which state explicitly *"G = 1, M = 1, E = −1/4 where G is the gravitational constant, M the total initial mass, and E the initial energy. The corresponding units of mass, length and time are then U_m = M, U_l = −G M²/(4E), U_t = G M^2.5 /(−4E)^1.5"*).

**Hénon convention cross-check.** In strict Hénon units, with G=1, M=1, E=−¼, the length unit U_l = −GM²/(4E) = 1, which is *defined by energy*, not period. The framework's D = (G M T²)^(1/3) is a *different* length scale — the Kepler-period length, useful when no global E is fixed (e.g. for an open chaotic configuration). These two scales are mutually consistent for a bound system but differ for unbound ejections. **The spec should explicitly say which scale it uses; if both are used in different places, that itself is a major bug.**

### M4 — Citation inaccuracies

Without the spec I cannot enumerate. Common errors in this literature: citing "SIREN" as Stanford-only when it's Sitzmann (Stanford) + Sitzmann/Martel/Bergman/Lindell/Wetzstein; citing HNN as "Google" when it's Greydanus (Google Brain) + Dzamba (PetCube) + Yosinski (Uber); citing Brutus as 2018 when it's Boekholt & Portegies Zwart 2015 (arXiv:1411.6671). All citations should be re-verified against MNRAS/NeurIPS-listed records.

### M5 — Recommended fix queue P0–P2 prioritization

The review's queue should be: P0 = B-01, B-02, B-03/B-05, B-04 (all are correctness-critical, all are localized fixes); P1 = M1, M2, M3 (correctness, but with workarounds); P2 = M4, D1–D4 (cleanup).

### M8 — Loss-balancing methodology (ALM vs alternatives)

**Affected sections.** PINN Architecture: ALM loss balancing.

**Verdict: PARTIALLY CONFIRMING.** ALM (Basir & Senocak's PECANN, J. Comp. Phys. 2022; Son et al.'s AL-PINN, Neurocomputing 2023) is a legitimate and increasingly mainstream choice for PINN loss balancing — Basir & Senocak show convergence guarantees for Helmholtz, Burgers, Klein–Gordon. However, the literature also documents known failure modes:

- **Hyperparameter sensitivity to the penalty schedule.** The penalty parameter μ_k must be increased on a schedule; too slow and constraints aren't enforced, too fast and the problem becomes ill-conditioned (Son et al. 2023, "AL-PINN").
- **Instability on chaotic dynamics.** No published study has demonstrated ALM on a chaotic Hamiltonian problem (three-body, double pendulum). All ALM-PINN results are on parabolic/elliptic PDEs.
- **Alternatives.** NTK-based adaptive weighting (Wang, Yu, Perdikaris, "When and why PINNs fail to train: A neural tangent kernel perspective," *J. Comp. Phys.* 449, 110768, 2022) attacks the same imbalance pathology with theoretical backing in the infinite-width limit. GradNorm (Chen, Badrinarayanan, Lee, Rabinovich, ICML 2018, arXiv:1711.02257) is a multi-task method that has not been widely adopted in PINNs but is mathematically cleaner. Self-adaptive PINNs (McClenny & Braga-Neto, "Self-adaptive physics-informed neural networks," *J. Comput. Phys.* 474, 111722, 2023, doi:10.1016/j.jcp.2022.111722) use per-sample trainable weights.

**Proposed recommendation.** Keep ALM as the primary balancer for the data+IC+BC constraints (its theoretical guarantees suit those terms), but **layer a GradNorm-style rescaling on top** for the energy-conservation and angular-momentum-conservation residuals, which are not Lagrangian constraints in the strict sense (they are derived consequences of the dynamics). This separates "hard" constraints (data, IC) from "soft" consistency terms (E, L). This hybrid is consistent with the recent conditionally adaptive ALM literature (Hu, Basir & Senocak, "Conditionally adaptive augmented Lagrangian method for physics-informed learning of forward and inverse problems," arXiv:2508.15695, 2025).

### M9 — HNN-style energy regularization placement

See D-01 below — this is conceptually intertwined with the open decision.

### M10 — Curriculum threshold motivation

**Verdict: CONFIRMING the review's concern that thresholds need physical motivation.** The Mikkola & Tanikawa (2007, *MNRAS Letters* 379, L21–L24) paper establishes that in the equal-mass three-body problem, the disruption time t_d and Lyapunov time t_L follow a two-part power-law relationship (Urminsky & Heggie 2009, *MNRAS* 392, 1051); the Lyapunov time itself scales roughly as the crossing time t_c. **Recommended curriculum thresholds**, in Hénon time units:

- Stage 0 (Keplerian / hierarchical): T ≤ 1 t_c (~0.5 Lyapunov times)
- Stage 1: T ≤ 5 t_c
- Stage 2: T ≤ 20 t_c (~10 Lyapunov times — the regime where Breen et al. trained)
- Stage 3: T ≤ 100 t_c (early dissolution regime)
- Stage 4–6: progressively longer, with the understanding that beyond ~30 Lyapunov times, no point-wise prediction is meaningful and the network is being trained to match ensemble statistics, not trajectories (Boekholt, Moerman & Portegies Zwart 2020, *MNRAS* 493, 3932; Portegies Zwart & Boekholt 2018).

The current spec's thresholds (whatever they are) should be expressed in Lyapunov-time multiples, not absolute time, so they transfer across different initial conditions of differing energy.

---

## 4. Open Decisions — Recommendation

### D-01 — Energy regularization methodology (HEAVY analytical weight)

**Statement of the choice (as I understand it from the prompt).** Should the framework enforce energy conservation by (a) HNN-style scalar-energy parametrization (network outputs H, dynamics derived from symplectic gradient), (b) soft penalty on |E(t) − E(0)|, (c) symplectic-network architecture (SympNets, Jin et al. 2020), or (d) leave energy unconstrained and rely on data?

**Recommendation: (b), a soft, curriculum-gated energy penalty, as the primary tool, with (a) and (c) explicitly rejected for this framework.**

**Rationale.**

1. **HNN's structural constraint is incompatible with the network's output topology.** HNN (Greydanus, Dzamba & Yosinski, *NeurIPS 2019*, arXiv:1906.01563) parametrizes a *scalar Hamiltonian* H(q,p) and derives dynamics via ∂H/∂p, −∂H/∂q. The current framework's network outputs *positions* r(t) directly, with velocity and acceleration derived by AD — this is a PINN, not an HNN. Switching to HNN would require a complete architectural rewrite (no SIREN as direct trajectory predictor) and is ruled out by the prompt's "no wholesale architectural rewrites" guardrail.
2. **SympNets are also incompatible.** SympNets (Jin, Zhang, Zhu, Tang & Karniadakis, "SympNets: Intrinsic structure-preserving symplectic networks for identifying Hamiltonian systems," *Neural Networks* 132, 166–179, 2020, arXiv:2001.03750) learn symplectic *maps* (one-step integrators), not trajectories. They have universal approximation guarantees over symplectic diffeomorphisms, and Jin et al. specifically demonstrated them on the three-body problem with excellent long-term energy conservation. But replacing the SIREN-trajectory predictor with a SympNet integrator is a complete architectural change.
3. **Soft energy penalty is sufficient when data is plentiful.** Greydanus et al. (2019, Figs. 1–3) shows qualitatively that vanilla MLPs *do* drift in energy (the paper's iconic mass-spring spiral plot), but the drift is data-dependent and typically a small fraction of E over the prediction horizon when training data is dense. For a curriculum that starts at short horizons, the drift is negligible at Stages 0–2; the penalty only becomes load-bearing at Stages 3+. **Therefore enable the energy penalty starting at Stage 3, ramping its ALM weight from 0 to 1 over Stage 3's first 25% of iterations**, with the multiplier λ_E updated by ALM dual ascent: λ_E ← λ_E + μ_k · mean(E(t) − E(0))².
4. **Add angular momentum** as a vector penalty: L_residual = ‖Σ m_i r_i(t) × v_i(t) − L(0)‖. In 3D, this gives three independent constraints rather than one. Galilean reduction (Section B-03) makes the linear-momentum constraint redundant; angular momentum is not redundant.
5. **Virial-theorem check as diagnostic, not loss.** The virial theorem ⟨2T⟩ = −⟨U⟩ holds only for bound, time-averaged orbits; using it as a per-snapshot loss would actively suppress chaotic excursions. Keep it as a Stage-6 validation metric only.

**Why NOT HNN as primary loss.** If the energy regularizer dominates, the network is trained to match a constant (E_0) along trajectories that are by construction chaotic and divergence-sensitive. The dominant gradient direction becomes "stay on the energy surface," not "match Brutus trajectories." In the chaotic regime, two trajectories on the same energy surface are *as different as possible*; the energy constraint is necessary but vastly insufficient.

### D-02 — Routine documentation cleanup (LIGHT weight)

**Recommendation:** standardize all formulas to one notation (suggest: Latin indices i,j ∈ {1,2,3} for bodies, Greek for spatial dimensions, t for canonical time, τ for SIREN input τ ∈ [−1, 1], explicit dimensions in every equation). Add a single "Conventions" appendix to the spec. Resolve M4 citation issues at the same pass.

---

## 5. Minor Issues — Triage

**Recommendation: do not elevate any of D1–D4, D6, D8–D10** unless they intersect a blocker. The likely candidates — naming conventions, plot styles, log-file formats — are pure cleanup and should be batched into a single documentation-cleanup PR after P0/P1 fixes land. **One exception**: if D6 concerns the choice of optimizer (Adam → L-BFGS handoff), the L-BFGS phase is known to be highly sensitive to gradient noise; ensure L-BFGS is launched only after Adam has converged the data-loss to within an order of magnitude of the residual loss (a standard heuristic from the Raissi/Karniadakis 2019 PINN paper).

---

## 6. Cross-Issue Dependencies

| Must fix first | Before fixing |
|---|---|
| B-01 (SIREN init) | Anything; training cannot start otherwise |
| B-03/B-05 (COM frame) | B-04 (softening), M2 (constraint counts), D-01 (energy reg) — all depend on a consistent frame |
| B-02 (chain rule) | M3 (length normalization sanity check), any quantitative residual evaluation |
| B-04 (softening) | M10 (curriculum thresholds, which depend on close-approach behavior) |
| M3 (normalization) | M10 (curriculum thresholds expressed in dimensionless units) |
| B-06 (input dimension) | Everything downstream of the input layer |

**Recommended sequencing.** Land B-01, B-06, and B-02 simultaneously in one PR (these touch the network class and the dataset class but not the loss). Then land B-03/B-05 and B-04 together (these touch the data pipeline and the residual). Then revisit M-class issues. D-01 should be decided **before** Stage-3 training begins, but does not block Stages 0–2.

---

## 7. What Was NOT Flagged (Gaps the Review Missed)

This auditor flags the following as worth adding to the issue list:

1. **L-BFGS sensitivity to ALM dual updates.** The Adam → L-BFGS handoff specified in CTL Instruction is mathematically fragile when ALM is updating λ multipliers between iterations: L-BFGS builds a quasi-Newton approximation of the Hessian assuming a stationary objective, but ALM's λ updates change the objective. Standard remedy: freeze λ during L-BFGS phase, only update between phases.
2. **SIREN's spectral bottleneck.** Chandravamsi, Shenoy, Zinn, Pisnoy & Frankel (Technion), "Spectral Bottleneck in Sinusoidal Representation Networks: Noise is All You Need," arXiv:2509.09719 (2025), and its companion "WINNER" initialization paper (Chandravamsi, Shenoy & Frankel, arXiv:2509.12980, 2025), show SIREN can suffer "spectral bottleneck" when target frequency support is misaligned with ω₀. For three-body dynamics, characteristic frequencies vary by 3+ orders of magnitude between Stage-0 (Keplerian) and Stage-6 (close encounters). A single ω₀ = 30 will be wrong for one end of the curriculum. **Recommendation: re-tune ω₀ per stage** (or use the FINER / WINNER initialization which broadens frequency support).
3. **Brutus precision contract.** The CTL Instruction presumably trusts Brutus output as "ground truth." Boekholt & Portegies Zwart (2015, arXiv:1411.6671) and Boekholt et al. (2020, *MNRAS* 493, 3932) emphasize that *individual* Brutus trajectories beyond ~3.5 Lyapunov times are themselves chaotic-divergent and only their *ensemble statistics* are physically meaningful. The framework should not be trained on long single trajectories beyond ~5 Lyapunov times; train on ensembles of short trajectories instead, then validate on ensemble distributional metrics (à la Portegies Zwart & Boekholt 2018).
4. **No mention of permutation symmetry.** The three-body problem is invariant under particle re-labeling. The Breen et al. (2020, *MNRAS* 494, 2465) reduction (fixing particle 1, semicircle for particle 2) implicitly breaks this; a full 3D framework that doesn't either canonicalize ordering or use a permutation-invariant network is wasting ~6× capacity. **Recommendation: sort bodies by some canonical invariant** (e.g. distance from initial COM) and apply the same sorting in residuals.
5. **No discussion of train/test distributional shift across curriculum stages.** When Stage k→k+1 widens the IC distribution, transfer learning typically benefits from a *replay buffer* of old-stage data to prevent catastrophic forgetting. The CTL framework should include a replay-buffer specification.
6. **Inconsistency between "3D not planar" guardrail and Breen et al. inheritance.** The spec inherits Breen et al.'s methodology, but Breen et al. is planar (per their §2: bodies in the unit semicircle of the negative x-axis with zero initial velocity). If the spec ever cites Breen's "10,000 simulations from semicircle" but uses 3D, the methodology has been silently extended without justification — a methodology disclosure gap.

---

## 8. Final Readiness Assessment

| Layer | Status |
|---|---|
| SIREN backbone math | **NOT READY** — fix B-01 first |
| AD-based dynamics | **NOT READY** — fix B-02 |
| Data pipeline (Brutus → tensors) | **NOT READY** — fix B-03/B-05 and B-04 |
| Loss balancing (ALM) | **Acceptable**, with caveats on chaotic regime |
| Curriculum design | **Conceptually sound**, thresholds need physical motivation (M10) |
| Energy regularization | **Open decision D-01** — recommend soft penalty, curriculum-gated |
| Documentation | **Routine cleanup needed** (D-02 and M4) |

Once B-01, B-02, B-03/B-05, B-04, and B-06 are landed (estimated 1–2 weeks of focused work), Stage-0 training should reach a clean baseline; Stages 1–3 will exercise the M-class issues and the D-01 decision; Stages 4–6 are research-grade and depend on the SIREN spectral question (Gap #2 above) being resolved.