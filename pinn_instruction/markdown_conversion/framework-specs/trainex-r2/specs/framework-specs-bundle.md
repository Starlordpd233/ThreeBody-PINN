---
title: Trainex R2 Framework-Specs Bundle — locked spec excerpts
role: excerpted locked framework-spec sections for the trainex-r2 research round; sections are authoritative (locked hard constraints), not open to challenge
status: active
created: 2026-07-24
source_baseline: 9b1f0e7a4735df1c54867530cfd1f13b390e1514
self_contained: true
---

# Framework-Specs Bundle (trainex-r2)

This bundle is **upload attachment 3 of at most 5** for the trainex-r2 research
round. It assembles the locked framework-spec sections that bear on the five
trainex-r2 research questions (gate definition, Stage-0 curriculum, the loss
catalog, the PHYS-05 warmup schedule, and the input/output + COM-projection
contract).

**These sections are authoritative locked spec — hard constraints.** The spec
text is reproduced faithfully and is *not* open to challenge by the research
agent: a number, formula, threshold, or normative decision stated here is the
locked contract, and a research answer that conflicts with it must say so
explicitly rather than silently override it.

**Self-containment / path-abbreviation convention.** The original spec prose
points at repository-internal evidence packets for provenance (paths into the
repo's planning and milestone trees). Those pointers are abbreviated to their
**bare filename in square brackets** so this bundle carries no repository path
(a reader outside the repository cannot resolve them anyway). Numeric values,
formulas, thresholds, and normative wording (what is retained / rejected /
deferred) are reproduced **unmodified**. Where a condensed annotation replaces
a provenance blockquote, it preserves the normative decision and labels itself
"[normative content retained, provenance path abbreviated]".

---

## Excerpt 1 — Two-sided physics-conservation admission gate

Source: ctl_instruction.md:565-580

> 5. Conservation gate (locked post-v1.3; SI-DQA-003). With H evaluated in
> float64 using Plummer softening `eps = 1e-10` in V:
> `eps_H = max_t |(H(t) - H(0)) / H(0)|`, `SCS = log10(eps_H)`.
> REJECT if `SCS > -5` (equivalently `eps_H > 1e-5`). `SCS = -5` exactly is
> Marginal: admitted, flagged for review. If `|H(0)|` is numerically near zero,
> SCS is undefined: QUARANTINE for manual review; do not introduce a denominator
> floor. If `eps_H = 0`, set `SCS = -inf` and label the trajectory Excellent.
> Store per-trajectory `eps_H`, `SCS`, and band label (Excellent <= -10;
> Acceptable (-10,-6]; Marginal (-6,-5]; Reject > -5). This clause TRANSCRIBES
> the locked gate into an editable spec; it implements, and does not re-open,
> Hard Constraint 5. Under the locked global scaling, Hamiltonian values scale
> as `H' = D*H`, so `eps_H` and the SCS band decision are invariant to
> raw/scaled units; by convention the admission check is computed from the raw
> parsed arrays. This validation-gate `eps_H` is distinct from the training-loss
> `eps_H = 1e-4*S_H` in `pinn_architecture.md` §3.4: same glyph, different
> quantity, and this gate is not changed by that training symbol.

**Why it matters here:** this is the gate the Stage-0 pilot fails
(`eps_H = 237.2086…` vs reject `1e-5`; see the run-evidence bundle). Note the
two `eps_H` glyphs: the **admission/evaluation gate** `eps_H = max_t |ΔH/H₀|`
(this excerpt) is a different quantity from the **training-loss energy-floor
symbol** `eps_H = 1e-4·S_H` (Excerpt 4 / §3.4).

---

## Excerpt 2 — Stage-0 definition and Stage 0/1 curriculum criteria

Source: ctl_instruction.md:138-202

> - **Stage 0: Easiest, highly stable systems.** Data source:
>   high-fidelity hierarchical simulations only (Set 1a).
>   - **Criteria:**
>     - Total Mechanical Energy: $E < -0.5$
>     - Angular Momentum Ratio: $\frac{L}{L_{\max}} > 0.5$
>     - Virial Ratio: $0.7 \leq Q \leq 1.3$
>     - Minimum Initial Separation: $s_{\min} > s_0$
>   - **Description:** Tightly bound binaries with near-virial equilibrium
>     and well-separated initial positions. Ideal for initial training due
>     to smooth trajectories.
>
> - **Stage 1: Still stable but slightly more complex.** Data source:
>   remaining hierarchical simulations, divided into two sub-stages to
>   introduce one complexity at a time (Set 1a).
>   - **Stage 1a: Moderately Stable (Energy Relaxed)**
>     - **Criteria:**
>       - $-0.5 \leq E < -0.1$
>       - $\frac{L}{L_{\max}} > 0.5$
>       - $0.7 \leq Q \leq 1.3$
>       - $s_{\min} > s_0$
>     - **Description:** Systems with moderately reduced binding energy
>       while maintaining orbital stability.
>   - **Stage 1b: Moderately Stable (Angular Momentum Relaxed)**
>     - **Criteria:**
>       - $E < -0.5$
>       - $0.1 \leq \frac{L}{L_{\max}} < 0.5$
>       - $0.7 \leq Q \leq 1.3$
>       - $s_{\min} > s_0$
>     - **Description:** Systems with moderately reduced angular momentum
>       (eccentric orbits) but strong binding energy.
>
> - **Stage 2 (High-Resolution Refinement of Stable Orbits):** Data source:
>   High-resolution hierarchical simulations (Set 2a).
>   - **Criteria:** Union of Stage 0 and Stage 1 criteria

The Stage-0/1 minimum-separation criterion $s_{\min} > s_0$ uses a
**data-derived threshold** $s_0$ (interim floor $s_0 = 0.01$ until the
admitted-set $s_{\min}$ distribution ratifies it); the earlier fixed
$s_{\min} > 2$ was proven geometrically unsatisfiable by the frozen sampling
envelope (scaled $s_{\min} \in [0.015, 0.084]$).

---

## Excerpt 3 — Cumulative curriculum replay and stage inventory

Source: ctl_instruction.md:262-294

> Crucially, each subsequent stage's training set includes all data from
> previous stages (curriculum replay) plus the new subset. This means by
> the time we reach Stage 5 or 6, the training data is the entire dataset.
> However, because the model has been gradually brought along this path, it
> is not learning from scratch on this complex set; it has a strong
> foundation from simpler cases. The staged curriculum defined above is
> empirically designed to ensure a smooth progression from stable to
> chaotic dynamics…

Phase 33 contract (stage inventory, abridged): the list above is the full
Stage 0–6 inventory — each stage named with its data source, criteria, and
description; no Stage-7+ is defined. **Cumulative replay** is the rule: each
subsequent stage's training set includes all data from previous stages plus
the new subset. **Stage-6 catch-all** (`s_min < 0.5` OR `|E| < 0.01`) absorbs
the near-collision tail across both fidelities. Stage trajectory counts cited
without supporting verification evidence are marked **claimed** or **FUT**, not
**verified**.

---

## Excerpt 4 — Loss catalog: the five penalty terms and total assembly

Source: pinn_architecture.md §3.1-3.5 (lines 292-623) and §10 total-loss table (line 989)

This is the **complete default penalty-term loss catalog**. No dual variables
are part of the default training loss; the scalar-conservation augmented
Lagrangian is documented only as a P2 ablation.

**Total loss assembly (the form consumed by training):**

> $$L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$
> *(pinn_architecture.md §4.1 line 635; total-loss table line 989. Combines
> data fidelity, IC anchoring, causal physics residual, energy drift, and
> angular-momentum drift terms in the default penalty-term formulation.)*

**§3.1 Data fidelity $L_{data}$** (Source: pinn_architecture.md:292-323):

> The data fidelity loss uses a Huber contract on scaled projected positions:
> $$L_{data} = \frac{1}{N_t} \sum_n \sum_i \operatorname{Huber}_{\delta_r}(r_{\theta,i}'(u_n) - r_i'(u_n))$$
> where $\delta_r = 1$ is the default Huber transition. … $u_n = t_n/T$ is the
> normalized physics time coordinate; $r'_{\theta,i}(u_n)$ is the network's
> predicted **scaled position** vector (the direct output of the network);
> $r'_i(u_n)$ is the ground truth position from the BRUTUS data, **scaled by
> the characteristic length $D$** ($r'_{\text{true}} = r_{\text{true}}/D$); and
> $N_t$ is the number of sampled time points in a training batch.

**§3.2 Physics residual $L_{phys}^{causal}$** (Source: pinn_architecture.md:362-422):

> The softened gravitational force between bodies i and j uses the
> Plummer-softened distance:
> $$r_{safe,ij} = \sqrt{||r'_{\theta,j}(u_n) - r'_{\theta,i}(u_n)||^2 + \epsilon_{train}^2}$$
> where $\epsilon_{train} = 10^{-5}$ is the training-time softening parameter.
> The force per unit mass is:
> $$F_{ij} = m_j \frac{r'_{\theta,j}(u_n) - r'_{\theta,i}(u_n)}{r_{safe,ij}^3}$$
> The residual is:
> $$f_i(u_n) = a'_{\theta,i}(u_n) - \sum_{j \neq i} F_{ij}$$
> Define the per-time residual energy $\bar R_n = \frac{1}{3}\sum_{i=1}^{3} \| f_i(u_n) \|^2$. For sorted collocation times, the default causal weights are:
> $$w_1 = 1,\qquad w_n = \exp\left(-\eta_c \sum_{m=1}^{n-1} \operatorname{stopgrad}(\bar R_m)\right), \quad n>1.$$
> The default physics loss consumed by $L_{total}$ is therefore:
> $$L_{phys}^{causal} = \frac{1}{N_t} \sum_{n=1}^{N_t} w_n \bar R_n.$$
> The unweighted mean may be logged as a diagnostic, but it is not the default
> training loss.

Phase 35 contract on the causal mode [normative content retained, provenance
path abbreviated]: the per-time causal weighting is the default
($w_1 = 1$, $w_n = \exp(-\eta_c \sum_{m<n}\operatorname{stopgrad}(\bar R_m))$,
$\eta_c = 1$); dense-residual ALM is rejected from the default loss; optional
scalar-conservation ALM remains deferred (P2 only); the numeric causal-exponent
clip bound is deferred (required only to avoid underflow).

**§3.3 Initial-condition anchor $L_{IC}$** (Source: pinn_architecture.md:473-495):

> $$L_{IC} = L_{IC,r} + \beta_v L_{IC,v}$$
> $$L_{IC,r} = (1/3) \sum_i ||r_{\theta,i}'(0) - r_i'(0)||^2$$
> $$L_{IC,v} = (1/3) \sum_i ||v_{\theta,i}'(0) - v_i'(0)||^2$$
> where $\beta_v = 1$ default, $\lambda_{IC} = 1$ default, and ablation range
> $[0.1, 10]$. … This position and velocity anchor is evaluated at normalized
> physics time `u=0`; because the network input uses $\tau = 2u - 1$, the
> corresponding network-time input is `τ=-1`. $L_{IC}$ uses squared error (not
> Huber); $L_{data}$ uses Huber.

**§3.4 Soft energy conservation regularizer $L_E$** (Source: pinn_architecture.md:497-536):

> The energy loss is a soft conservation regularizer: the network predicts
> positions at each time step, velocities and accelerations are computed via
> componentwise automatic differentiation, and the analytic matched-Plummer
> Hamiltonian $H_\epsilon$ is evaluated from the predicted positions and
> AD-derived velocities. … The network does not parameterize a Hamiltonian.
> The matched-Plummer potential energy is:
> $$V_\epsilon = -\sum_{i<j} \frac{m_i m_j}{r_{safe,ij}}$$
> using the same $r_{safe,ij}$ as the residual force term. The matched-Plummer
> Hamiltonian is $H_\epsilon = T' + V_\epsilon$ where $T'$ is the dimensionless
> kinetic energy.
> $$L_{E} = \frac{1}{N} \sum_n \operatorname{Huber}(\Delta H_n, \delta=1.0)$$
> where
> $$\Delta H_n = \frac{H_\epsilon(r_\theta'(u_n), v_\theta'(u_n)) - H_\epsilon(r_0', v_0')}{|H_\epsilon(r_0', v_0')| + \epsilon_H}$$
> $$\epsilon_H = 1e-4 * S_H$$
> $$S_H = median\_train(K0 + Uabs0)$$
> and $\delta = 1.0$ is the Huber transition.

Phase 35 contract on the energy Huber delta [normative content retained,
provenance path abbreviated]: the normalized-energy Huber transition is named
`delta_E = 1.0` and remains the configurable current baseline; calibration to a
smaller range, any stage-indexed Huber-delta table, and any median/quantile
replacement are deferred until normalized $|\Delta H|$ quantiles, linear-branch
occupancy, validation energy drift, and weighted gradients are measured.

**§3.5 Angular-momentum conservation loss $L_L$** (Source: pinn_architecture.md:611-623):

> $$L_{L} = \frac{1}{3N_t} \sum_n \sum_\alpha \operatorname{Huber}\left(\frac{L_{\theta,\alpha}'(u_n) - L_{0,\alpha}'}{L_{scale}}, \delta=1.0\right)$$
> where $\alpha \in \{x, y, z\}$, $L_{scale} = ||L_0'|| + \epsilon_L$, and
> $\epsilon_L = 10^{-8}$ is a numerical-stability scale … distinct from
> softening $\epsilon_{train}$ / $\epsilon_{inv}$ and from $\epsilon_H$ (a
> dataset-scale Hamiltonian floor, not a softening parameter).

Phase 35 contract on the angular-momentum role [normative content retained,
provenance path abbreviated]: $L_L$ remains a soft angular-momentum regularizer
in the default component catalog; it does not authorize a separate
linear-momentum loss (linear momentum is enforced structurally by the COM
projection head — Excerpt 6).

---

## Excerpt 5 — PHYS-05 loss-balancing warmup schedule

Source: pinn_architecture.md §4.1 (lines 633-682)

> ## 4.1 Loss Balancing via Warmup Schedule (PHYS-05)
> (total loss assembly quoted in Excerpt 4)
>
> where:
> - $L_{data}$: Huber loss on position predictions, $\delta_r = 1$ default.
> - $L_{IC}$: Initial condition anchor (position + velocity at `u=0`),
>   $\lambda_{IC} = 1$ default.
> - $L_{phys}^{causal}$: Physics residual with causal weighting
>   $w_n = exp(-\eta_c \sum_{m<n} stopgrad(\bar R_m))$, $w_1 = 1$,
>   $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
>   causal exponent to avoid underflow, but do not choose a numeric clipping
>   bound in Phase 19; surface a gap if one is needed.
> - $L_{E}$: Soft energy conservation regularizer, see §3.4.
> - $L_{L}$: Angular momentum conservation loss, see §3.5.
> - No dedicated L_P term: linear momentum is enforced structurally by the
>   COM projection head / zero-momentum output contract, so a separate
>   linear-momentum loss would be redundant.
>
> The warmup schedule is:
> - $I_{warm} = min(2000, 0.1 \cdot N_{Adam,k})$
> - $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
>   default $\lambda_{phys}^{max}(k) = 1$
> - $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$
> - $\lambda_E(k, i)$ and $\lambda_L(k, i)$ warm up linearly with $i/I_{warm}$
>
> Optimizer-phase semantics:
> - During Adam epochs: $\lambda$ values may be scheduled per the warmup
>   schedule; no dual variables are updated.
> - During L-BFGS: $\lambda$ values are frozen; no dual updates inside a line
>   search.
> - Stage-boundary transitions: re-warmup applies per the new stage's
>   $\lambda^{max}$ values.

Phase 35 contract on the energy-loss weights [normative content retained,
provenance path abbreviated]: retain the PHYS-05 warmup schedule above with
`lambda_E^max <= 1` and scheduled conservation weights at or below one; the
issue-doc cap-table replacement and stale high-energy-weight premise are
**rejected**, not adopted as a locked schedule; before any future control law,
log weighted losses, scheduled weights, and gradient statistics; automatic
dominance reweighting is deferred until measured weighted-loss/gradient evidence
exists.

**Why it matters here:** the pilot's `lambda_phys` reaches 1.0 at step 31 and
`lambda_l == 0.0` at all 300 steps (see run-evidence bundle, DIAG-02). Under
this schedule, with `k` (stage) in `{0,1}` for Stage 0, `lambda_E^max =
lambda_L^max = 0` — i.e. both conservation weights are **zero throughout
Stage 0** by the locked schedule. A research answer about loss weighting or
warmup must engage this schedule directly rather than assume generic defaults.

---

## Excerpt 6 — Input vector, output head, and the mass-weighted COM projection

Source: pinn_architecture.md:805-886

> **Input Vector** A **14-dimensional vector** `[\tau, IC_{13}]`, where `u=t/T`
> is the autograd leaf and `\tau=2u-1` is the bounded network time coordinate.
> `IC_{13}` is the ordered Jacobi-state initial-condition vector defined
> canonically in `ctl_instruction.md` Step 4:
> $$IC_{13} = [m_1, m_2, m_3, \rho_x, \lambda_x, \lambda_y, \dot{\rho}_x, \dot{\rho}_y, \dot{\rho}_z, \dot{\lambda}_x, \dot{\lambda}_y, \dot{\lambda}_z, E].$$
> Mass, Jacobi-position, and Jacobi-velocity slots are independently normalized
> with `tanh((z - mu_z)/(sigma_z + 10^-8))` after the Phase 18 (FRAME-01)
> preprocessing contract. The energy slot uses `tanh(E / E_scale)` with
> `E_scale = |median_traj(E)| + 10^-8`.
>
> **Output Layer** … The final layer … is a standard linear layer without any
> activation function. … The output is a 9-dimensional vector representing the
> concatenated positions of the three bodies …
> $$r_\theta(t) = [r_1(t), r_2(t), r_3(t)]$$
> The network does not predict velocities or accelerations directly. Instead,
> these kinematic quantities are derived from the projected position outputs
> using componentwise automatic differentiation … with respect to the normalized
> physics-time input, $u=t/T$:
> $$v_\theta'(u) = \frac{d r_\theta'(u)}{d u} \quad \text{and} \quad a_\theta'(u) = \frac{d^2 r_\theta'(u)}{d u^2}$$
>
> **Output Frame** The predicted positions are in the **Center of Mass (COM)
> frame**. The raw network head emits unconstrained positions
> $$\tilde r_\theta(u, IC_{13}) = [\tilde r_1, \tilde r_2, \tilde r_3] \in \mathbb{R}^9.$$
> Before any downstream consumer sees this output, the model applies a **hard
> mass-weighted COM projection**:
> $$R_{\mathrm{COM}} = \frac{\sum_{j=1}^3 m_j \tilde r_j}{\sum_{j=1}^3 m_j}, \qquad r_i = \tilde r_i - R_{\mathrm{COM}}, \qquad i \in \{1,2,3\}.$$
> Here `m_j` denotes the ordered raw pre-tanh mass metadata supplied by the
> Phase 18 (FRAME-01) preprocessing output; it is not the normalized mass slot
> inside `IC_{13}`. The projected positions $r_\theta = [r_1, r_2, r_3]$ are
> the **only** positions consumed by data loss, physics residuals, IC loss,
> conservation loss, diagnostics, and evaluation metrics. The projection is
> **architectural, not a soft penalty**. … for every projected output, the
> mass-weighted position COM is zero by construction.

**Why it matters here:** this is the context for the normalization / data-scale
sub-facet of the loss-weighting question — the IC/vector are dataset-normalized
via `tanh`, the output carries a hard COM projection, and there is no separate
linear-momentum term (structural). The roughly ten-order separation between
`loss_phys ≈ 1e9` and `loss_data ≈ 0.1` observed in the pilot (DIAG-02) must be
read against this normalization and projection contract.

---

*End of framework-specs bundle. All excerpts are locked, authoritative spec
(hard constraints); the research agent treats them as ground truth, not as
challengeable design intent. Provenance pointers inside the original prose were
abbreviated to bare filenames for self-containment; no numeric, formula,
threshold, or normative decision was modified.*
