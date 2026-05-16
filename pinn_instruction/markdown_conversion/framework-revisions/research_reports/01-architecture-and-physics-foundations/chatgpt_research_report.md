# CTL-PINN Architecture and Physics Foundations Audit — Reformatted Markdown

## 1. Executive Summary

My overall assessment is that the framework is **not yet ready for implementation**, but not for exactly the reasons the consolidated review claims.

The most serious **confirmed blockers** in the supplied specifications are:

1. An unresolved and mathematically under-specified input/output gauge for the 14D conditioning vector.
2. Inconsistent handling of COM-frame targets.
3. Incorrect automatic-differentiation usage for time derivatives.
4. An internally inconsistent softened dynamics contract between the physics residual and the energy regularizer.

By contrast, the review's claim that the characteristic length must be changed from

$$
D = (G T^2)^{1/3}
$$

to

$$
D = (G M_{\mathrm{tot}} T^2)^{1/3}
$$

is **not correct under the mass convention actually written in the CTL and PINN specs**. That alternative length scale is valid only if all equations are simultaneously rewritten using normalized masses

$$
\mu_i = \frac{m_i}{M_{\mathrm{tot}}}.
$$

The supplied markdown files are therefore closer to being salvageable than the review suggests, but they still require a disciplined contract rewrite before training.

The highest-confidence conclusions are:

- The hidden-layer SIREN initialization used in the supplied `pinn_architecture.md` is already aligned with the original SIREN derivation. The review is only partially right because the bad formula appears to be an upstream source-document problem, not a problem in the supplied markdown spec.
- The review is right that the input-vector contract is broken across documents, but its preferred “shape invariants + direction cosines” repair is not sufficient for raw Cartesian COM-frame outputs.
- The review is right that derivative handling is wrong in spirit, but it understates the severity: the current formulation drops required chain-rule factors **and** collapses a 9D output derivative into a vector-Jacobian product with `grad_outputs=ones`, which is not the same object as the componentwise time derivative needed for velocities and accelerations.
- The softening problem is worse than reported, because the force law and energy law in the supplied PINN spec are not gradients of the same softened potential.

My smallest mathematically sound repair, without changing the SQR-SkipResNet-SIREN backbone or the CTL curriculum logic, is:

1. Keep the current raw-mass scaling convention and therefore keep

   $$
   D = (G T^2)^{1/3}.
   $$

2. Introduce one unified preprocessing transform that performs COM recentering, zero-momentum boosting, and a **canonical rotation gauge** before invariant computation or supervision.
3. Fix AD derivatives with explicit componentwise Jacobians and the missing factors of $2$ and $4$.
4. Replace the current softened force/potential pair with one consistent softened Hamiltonian.
5. Remove epochwise $\omega_0$ scheduling from the spec.
6. Lock one 14D input contract in both documents.

With those changes, the framework becomes internally coherent enough to test empirically.

---

## 2. Issue-by-Issue Analysis: Blocking Findings

### B-01 — SIREN Hidden-Layer Initialization

**Review reference:** “Confirmed Findings,” row B-01.  
**Affected specs:** `pinn_architecture.md`, section “A Principled Initialization Scheme for SIREN Layers,” plus the architecture summary table.

#### Assessment: Partially confirmed

The review is correct about the underlying mathematics. For hidden SIREN layers with activation

$$
\sin(\omega_0 W x + b),
$$

the principled hidden-layer initialization is

$$
W \sim \mathcal{U}
\left[
-\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0},
\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0}
\right].
$$

The original SIREN derivation treats the first layer differently, choosing small first-layer weights while using a larger fixed $\omega_0$ to span multiple periods over the input domain.

However, the **supplied markdown architecture file already uses the correct hidden-layer divide-by-$\omega_0$ formula**. The problem is not present in the user-provided markdown spec itself. The review is therefore right about the upstream source discrepancy, but wrong if read as a defect in the supplied markdown specification.

#### Solution

Keep the current markdown formula and explicitly freeze the SIREN contract as:

$$
W^{(0)}
\sim
\mathcal{U}
\left[
-\frac{1}{n_{\mathrm{in}}},
\frac{1}{n_{\mathrm{in}}}
\right],
$$

$$
W^{(\ell \ge 1)}
\sim
\mathcal{U}
\left[
-\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0},
\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0}
\right].
$$

Add this clarification:

> $\omega_0$ is a fixed layer hyperparameter that must match the initialization contract. It is not a free epochwise scheduling knob.

This is a **document error**, not a current markdown-spec error.

---

### B-02 — Characteristic Length $D$

**Review reference:** “Confirmed Findings,” row B-02.  
**Affected specs:** `ctl_instruction.md`, “Step 2: Preprocessing: Scaling to Dimensionless Units”; `pinn_architecture.md`, blueprint summary table.

#### Assessment: Disputed

Under the equations actually written in the supplied specs, masses are **not** nondimensionalized by $M_{\mathrm{tot}}$. The CTL and PINN documents continue to use the raw $m_i$ in the scaled energy, angular momentum, physics residual, and energy regularizer.

If one scales only

$$
\mathbf{r}_i = D \mathbf{r}'_i,
\qquad
t = T u,
$$

while leaving $m_i$ unchanged, Newton's law becomes

$$
\frac{d^2 \mathbf{r}'_i}{d u^2}
=
\frac{G T^2}{D^3}
\sum_{j \ne i}
m_j
\frac{
\mathbf{r}'_j - \mathbf{r}'_i
}{
\left\lVert \mathbf{r}'_j - \mathbf{r}'_i \right\rVert^3
}.
$$

To preserve coefficient $1$ in front of the mass-weighted force term, the correct choice under this convention is

$$
D = (G T^2)^{1/3},
$$

which is exactly the convention written in the supplied CTL and PINN specs.

The review's proposed formula

$$
D = (G M_{\mathrm{tot}} T^2)^{1/3}
$$

is only correct if the dynamics are simultaneously rewritten in terms of normalized masses:

$$
\mu_i = \frac{m_i}{M_{\mathrm{tot}}}.
$$

That is a different scaling convention. The review skipped the second half of the contract.

#### Solution

Choose one convention and carry it through all formulas.

The **minimal-change** choice is to keep the current convention:

$$
D = (G T^2)^{1/3},
\qquad
V = \frac{D}{T},
$$

and retain raw masses in the scaled equations, energy, and residuals.

If the framework owner strongly prefers the review's mass-aware length scale, then all physics equations must be rewritten using normalized masses:

$$
\mu_i = \frac{m_i}{M_{\mathrm{tot}}},
$$

everywhere, not merely in the preprocessing line.

As written, the review's “fix $D=6.694$” would make the specs **less** self-consistent, not more.

---

### B-03 — Input-Vector Dimensionality Conflict

**Review reference:** “Confirmed Findings,” row B-03.  
**Affected specs:** `ctl_instruction.md`, “Step 4: Formulating the Input Vector”; `pinn_architecture.md`, blueprint summary table and input-vector description.

#### Assessment: Confirmed

The CTL spec describes an “11-component IC” and a “12-dimensional input vector,” while the architecture spec describes a 14D input with a 13-component IC vector.

This is a genuine contract break because all of the following depend on one fixed dimension:

- `n_in` for the first linear layer.
- Dataset assembly.
- Normalization.
- Checkpoint compatibility.
- Input serialization.

#### Solution

Lock the interface as

$$
x = [\tau, IC],
\qquad
\tau \in [-1,1],
\qquad
IC \in \mathbb{R}^{13}.
$$

Therefore the network input is

$$
x \in \mathbb{R}^{14}.
$$

Rewrite CTL Step 4 so it enumerates all 13 IC components in the same order as the architecture document.

This blocker cannot be fully closed until D-01 is resolved, because the unresolved five-slot subvector is exactly what keeps the count unstable.

---

### B-04 — Input-Vector Composition

**Review reference:** “Confirmed Findings,” row B-04 and “Open Decisions.”  
**Affected specs:** `ctl_instruction.md`, “Step 4”; `pinn_architecture.md`, input-vector summary; review “Decisions Requiring Human Approval” and “Open Decisions.”

#### Assessment: Problem confirmed; proposed solution disputed

The problem is real: the five disputed slots are unresolved across the documents.

However, the review's recommended Option B,

$$
[I_1, I_2, I_3, \cos\theta, \sin\theta],
$$

is **not sufficient** if the network is asked to predict raw Cartesian COM-frame trajectories.

Those two direction-cosine slots encode only the **inclination** of the invariant plane normal relative to the $z$-axis, not its azimuth. Therefore they do not fix the full 3D rotational gauge.

Option A is also not satisfactory as written, because using only

$$
\sin(\gamma_{\mathrm{orb}})
$$

loses phase information, and the spherical-angle representation becomes ill-conditioned when

$$
L_x = L_y = 0.
$$

Option C preserves more velocity geometry but still needs a gauge choice to become sensible.

#### Solution

Do **not** approve Option B as written.

The smallest sound repair is to add a deterministic **canonical rotation** in preprocessing, so the network is trained in a canonical COM frame rather than an arbitrary raw inertial orientation.

Once that gauge is fixed, the five disputed slots can be populated in a stable and near-minimal way. My recommended D-01 choice is given in the Open Decisions section below.

---

### B-05 — COM-Frame Violation

**Review reference:** “Confirmed Findings,” row B-05.  
**Affected specs:** `ctl_instruction.md`, “Step 2.5: Verify Center-of-Mass (COM) Frame”; `pinn_architecture.md`, “Output Frame and File Format.”

#### Assessment: Confirmed

The CTL document states that hierarchical ICs are not initially in the COM frame and that corresponding Brutus outputs may also require transformation. The PINN architecture explicitly assumes COM-frame outputs.

If targets are not in the same frame as the network's inductive bias and input invariants, the model is forced to learn arbitrary translational motion that should have been removed analytically.

#### Solution

Implement exactly one reusable preprocessing transform for both IC files and every Brutus snapshot.

Define

$$
\mathbf{R}_{\mathrm{COM}}
=
\frac{1}{M}
\sum_i
m_i \mathbf{r}_i,
\qquad
\mathbf{V}_{\mathrm{COM}}
=
\frac{1}{M}
\sum_i
m_i \mathbf{v}_i,
$$

where

$$
M = \sum_i m_i.
$$

Then transform

$$
\mathbf{r}_i^{\mathrm{COM}}
=
\mathbf{r}_i - \mathbf{R}_{\mathrm{COM}},
\qquad
\mathbf{v}_i^{\mathrm{COM}}
=
\mathbf{v}_i - \mathbf{V}_{\mathrm{COM}}.
$$

Assert after transformation:

$$
\left\lVert
\sum_i m_i \mathbf{r}_i^{\mathrm{COM}}
\right\rVert
<
10^{-12},
$$

$$
\left\lVert
\sum_i m_i \mathbf{v}_i^{\mathrm{COM}}
\right\rVert
<
10^{-12}.
$$

If D-01 adopts the canonical rotation recommended below, append that rotation to the same transformer so the pipeline has one unambiguous frame contract.

---

### B-09 — Softening Mismatch

**Review reference:** “Confirmed Findings,” row B-09.  
**Affected specs:** `ctl_instruction.md`, “Step 3” energy and stage features; `pinn_architecture.md`, “Physics Residual Term” and “HNN-Style Energy Regularizer.”

#### Assessment: Confirmed, but the review's resolution is incomplete

The review is right that the CTL and PINN specs currently use different $\epsilon$ values for invariant computation versus training losses.

But the more serious issue is that the supplied PINN spec uses a force law proportional to

$$
\frac{\Delta \mathbf{r}}{(r+\epsilon)^3},
$$

while its energy regularizer uses a potential proportional to

$$
-\frac{1}{r+\epsilon}.
$$

These are **not** force and potential from the same softened Hamiltonian.

Indeed,

$$
-\nabla
\left(
\frac{1}{r+\epsilon}
\right)
=
\frac{\Delta \mathbf{r}}{r(r+\epsilon)^2},
$$

not

$$
\frac{\Delta \mathbf{r}}{(r+\epsilon)^3}.
$$

So the physics residual and energy regularizer are currently enforcing different softened dynamics. The review noticed the epsilon mismatch but missed this deeper incompatibility.

#### Solution

First choose one softened Hamiltonian family for training. The cleanest option is Plummer softening:

$$
V_\epsilon
=
-
\sum_{i<j}
\frac{m_i m_j}{\sqrt{r_{ij}^2+\epsilon^2}},
$$

with matched acceleration

$$
\mathbf{a}_i
=
\sum_{j\ne i}
m_j
\frac{
\mathbf{r}_j-\mathbf{r}_i
}{
\left(r_{ij}^2+\epsilon^2\right)^{3/2}
}.
$$

This is a matched force/potential pair.

After that, decide the epsilon policy. A dual-context policy can be justified:

- Near-unsoftened invariants for curriculum metrics.
- Softened dynamics for training stability.

But it must be documented honestly as “different numerical roles,” not “the same physics.”

---

### B-10 — Dynamic $\omega_0$ Scheduling

**Review reference:** “Confirmed Findings,” row B-10 and “Dynamic Omega0 Scheduling — Removal.”  
**Affected specs:** `pinn_architecture.md`, “A Principled Initialization Scheme for SIREN Layers.”

#### Assessment: Partially confirmed

I agree that the epochwise scheduler should be removed from the specification.

However, I do **not** accept the review's reasoning without qualification. In standard SIREN, $\omega_0$ is not merely an initialization-only variable; it also appears in the forward-pass sine scaling.

The real problem is that the original SIREN derivation assumes a matched pair:

1. Fixed $\omega_0$.
2. Initialization calibrated to that fixed $\omega_0$.

Changing $\omega_0$ epoch by epoch either:

- Does nothing because it is dead code, or
- Changes the network's frequency scaling after initialization was chosen for a different value.

Both are bad, but they are different bads. From the supplied markdown files alone, I can confirm the **specification error**, but not whether the live implementation makes the function dead or active.

#### Solution

Delete epochwise $\omega_0$ scheduling from the architecture spec.

Use fixed values within a stage:

$$
\texttt{first\_omega\_0} = 30,
\qquad
\texttt{hidden\_omega\_0} = 1.
$$

If the curriculum owner wants stage-dependent frequency priors, do that only at **stage boundaries**, together with a newly documented reinitialization or a new model instance.

This is partly a **document error** and partly a potentially dead-code issue whose runtime status cannot be verified from the supplied files alone.

---

## 3. Issue-by-Issue Analysis: Major Findings

### M1 and M2 — IC-Vector Size and Total Input Size

**Review reference:** “Confirmed Findings,” rows M1 and M2.  
**Affected specs:** `ctl_instruction.md`, “Step 4”; `pinn_architecture.md`, blueprint summary table.

#### Assessment: Confirmed

M1 and M2 are the major-level manifestations of B-03.

The CTL document currently assembles 11 IC values, while the architecture document reserves space for 13 IC values and a 14D total input.

This cannot be left as “to be clarified later,” because it directly changes:

- `n_in`.
- Checkpoint shapes.
- Data-pipeline serialization.
- Normalization arrays.
- Model compatibility across stages.

#### Solution

Once D-01 is approved, publish a single canonical IC ordering and keep it fixed everywhere:

$$
IC =
[
m_1^{\mathrm{norm}},
m_2^{\mathrm{norm}},
m_3^{\mathrm{norm}},
E^{\mathrm{norm}},
L_{\mathrm{norm}}^{\mathrm{in}},
Q^{\mathrm{norm}},
s_{\min}^{\mathrm{norm}},
I_{\mathrm{norm}}^{\mathrm{in}},
g_1,
g_2,
g_3,
g_4,
g_5
].
$$

The meaning of

$$
g_1,\dots,g_5
$$

must be locked once and never reinterpreted differently across documents.

---

### M3 — Order of COM Transform and Scaling

**Review reference:** “Confirmed Findings,” row M3.  
**Affected specs:** `ctl_instruction.md`, “Step 2” and “Step 2.5.”

#### Assessment: Disputed as a mathematical bug; accepted as a clarity problem

Under the current convention, $D$ is a global constant and COM subtraction is linear. Therefore scaling and COM correction commute:

$$
\frac{\mathbf{r}_i-\mathbf{R}_{\mathrm{COM}}}{D}
=
\frac{\mathbf{r}_i}{D}
-
\frac{\mathbf{R}_{\mathrm{COM}}}{D},
$$

and

$$
\frac{\mathbf{v}_i-\mathbf{V}_{\mathrm{COM}}}{V}
=
\frac{\mathbf{v}_i}{V}
-
\frac{\mathbf{V}_{\mathrm{COM}}}{V}.
$$

So “COM must happen before scaling” is not, by itself, a mathematical necessity in the current framework.

The real issue is having a single formal transformer, not the order of two commuting linear operations.

#### Solution

Define one preprocessing function whose documented order is:

1. COM/boost correction.
2. Optional canonical rotation.
3. Scaling.

This order is easier to audit and reason about. But the current text should not be classified as a physics error solely because Step 2 is written before Step 2.5.

---

### M4 — Constraint Counting and Injectivity Argument

**Review reference:** “Confirmed Findings,” row M4.  
**Affected specs:** `ctl_instruction.md`, “Mathematical Guarantees” in Step 4.

#### Assessment: Partially confirmed

The CTL sentence claiming “13 constraints for an 8-dimensional reduced phase space” is wrong.

The review's arithmetic correction to

$$
18 - 3 - 3 - 3 = 9
$$

is the standard count for kinematic degrees of freedom after quotienting:

- Translations: $3$.
- Total momentum: $3$.
- Global rotation: $3$.

But that patch is still incomplete for the actual framework because the network currently predicts **raw Cartesian COM-frame trajectories**, not trajectories already quotiented by global rotation.

Therefore, the present “injectivity proof” in CTL is not established by merely changing $8$ to $9$.

#### Solution

Remove the current uniqueness claim and replace it with a conditional statement.

The IC descriptor is only plausibly injective **after a specified gauge choice**, including:

- COM frame.
- Zero total momentum.
- Canonical body ordering.
- Canonical rotation.

Without that gauge, the current proof sketch should be deleted rather than merely “arithmetically corrected.”

---

### M5 — $I_3$ Normalization

**Review reference:** “Confirmed Findings,” row M5.  
**Affected specs:** `ctl_instruction.md`, “Universal Shape Invariants” and “Apply Normalization to [-1,1].”

#### Assessment: Confirmed bug; review's numeric range disputed

The CTL document says $I_3$ is already in $[-1,1]$, which is false.

But the review's claim that the formula yields

$$
I_3 \in [0,1]
$$

is also too loose.

Because the mutual distances form a triangle, the triangle inequality implies

$$
0
\le
d_{\mathrm{short}} + d_{\mathrm{mid}} - d_{\mathrm{long}}
\le
\frac{1}{3}
\left(
d_{\mathrm{short}} + d_{\mathrm{mid}} + d_{\mathrm{long}}
\right).
$$

Therefore the actual range is

$$
I_3 \in \left[0,\frac{1}{3}\right].
$$

The review's proposed repair

$$
I_3^{\mathrm{norm}} = 2I_3 - 1
$$

does **not** map the attainable range to all of $[-1,1]$.

#### Solution

If keeping the current $I_3$ definition, the minimal correct normalization is

$$
I_3^{\mathrm{norm}} = 6I_3 - 1.
$$

A better long-run design is to revisit the three shape invariants during D-01, because they are partly redundant. But

$$
I_3^{\mathrm{norm}} = 6I_3 - 1
$$

is the correct local repair.

---

### AD Chain-Rule Factor and Derivative Collapse

**Review reference:** “AD Chain-Rule Factor — Missing Derivative Conversion” and “Explicit AD Implementation Requirement.”  
**Affected specs:** `pinn_architecture.md`, “Physics Residual Term,” “Energy Regularizer,” and “Output Layer and Kinematic Consistency via Automatic Differentiation”; `ctl_instruction.md`, time normalization in Step 4.

#### Assessment: Strongly confirmed; should be elevated to blocking in implementation

The network input is

$$
\tau = \frac{2t}{T} - 1.
$$

Equivalently,

$$
u = \frac{t}{T},
\qquad
\tau = 2u - 1.
$$

Autograd on the input coordinate produces derivatives with respect to $\tau$, not $u$ and not physical time $t$.

The required conversions are

$$
\frac{d}{du}
=
2\frac{d}{d\tau},
$$

and

$$
\frac{d^2}{du^2}
=
4\frac{d^2}{d\tau^2}.
$$

Therefore the correct network-derived dimensionless kinematics are

$$
\mathbf{v}'
=
\frac{d\mathbf{r}'}{du}
=
2
\frac{d\mathbf{r}'}{d\tau},
$$

and

$$
\mathbf{a}'
=
\frac{d^2\mathbf{r}'}{du^2}
=
4
\frac{d^2\mathbf{r}'}{d\tau^2}.
$$

In physical units,

$$
\mathbf{v}
=
\frac{D}{T}\mathbf{v}'
=
\frac{2D}{T}
\frac{d\mathbf{r}'}{d\tau},
$$

and

$$
\mathbf{a}
=
\frac{D}{T^2}\mathbf{a}'
=
\frac{4D}{T^2}
\frac{d^2\mathbf{r}'}{d\tau^2}.
$$

Additionally, using `autograd.grad` with

```python
grad_outputs=torch.ones_like(positions)
```

computes a vector-Jacobian product, not the full componentwise derivative tensor needed for a 9D position output.

#### Solution

Compute derivatives componentwise, or use a Jacobian API that returns the full output-by-input derivative.

The implementation contract should be:

$$
\mathbf{r}' = f_\theta(\tau, IC),
$$

$$
\frac{d\mathbf{r}'}{du}
=
2
\frac{\partial f_\theta}{\partial \tau},
$$

$$
\frac{d^2\mathbf{r}'}{du^2}
=
4
\frac{\partial^2 f_\theta}{\partial \tau^2}.
$$

Until this is fixed, the physics residual and the energy regularizer are numerically inconsistent with the stated preprocessing.

---

### M8 — LayerNorm Attribution

**Review reference:** “Confirmed Findings,” row M8.  
**Affected specs:** `pinn_architecture.md`, “The Power-Enhanced SkipResNet Formulation” and summary table.

#### Assessment: Confirmed

LayerNorm on the skip path is not part of the original Power-Enhanced SkipResNet paper. The current architecture may still be valid, but the attribution is wrong.

This is a **citation-and-design provenance** issue, not evidence that the LayerNorm variant is invalid.

#### Solution

Relabel LayerNorm as a **project-specific stabilization modification**.

If keeping it, the safer first-ablation default is:

```text
elementwise_affine = False
```

LayerNorm should be tested through ablation after the hard physics contracts are repaired.

---

### M9 and M10 — $E_{\mathrm{norm}}$ Range and Asymmetric Mass Normalization

**Review reference:** “Confirmed Findings,” rows M9 and M10.  
**Affected specs:** `ctl_instruction.md`, “Apply Normalization to [-1,1]”; `pinn_architecture.md`, summary table.

#### Assessment: Mostly disputed as bugs

The fact that

$$
E^{\mathrm{norm}}
=
\tanh\left(\frac{E}{E_{\mathrm{scale}}}\right)
$$

may occupy mostly the negative half-line if the dataset is mostly bound is not a correctness problem. It is simply a statement about the data manifold.

It is also not clear from the supplied files that all trajectories are guaranteed bound.

Likewise, the asymmetric range of normalized mass fractions is not a defect. It is an expected consequence of an asymmetric mass-ratio distribution and carries useful hierarchy information.

#### Solution

Demote both to documentation cleanup.

Add one sentence:

> The realized support of a normalized feature need not fill all of $[-1,1]$; asymmetry in $m_i^{\mathrm{norm}}$ is expected when the training distribution over mass ratios is asymmetric.

---

## 4. Open Decisions Recommendation

### D-01 — 14D Input-Vector Composition

I do **not** recommend approving the review's Option B as written.

Its final two slots,

$$
(\cos\theta, \sin\theta),
$$

encode only one rotational degree of freedom and are insufficient for raw Cartesian COM-frame targets.

I also do not recommend approving Option A as written, because

$$
[
\sin\theta_L,
\cos\theta_L,
\sin\phi_L,
\cos\phi_L,
\sin\gamma_{\mathrm{orb}}
]
$$

is not robustly injective:

- The $\phi_L$ parameterization is ill-conditioned at the poles.
- Using only $\sin\gamma_{\mathrm{orb}}$ loses orbital phase information.

Option C is the closest to usable, but only after the framework fixes the rotational gauge directly in preprocessing.

#### Recommendation

Adopt a **small but critical methodology change**: add a canonical rotation to the CTL preprocessing pipeline.

After COM recentering and momentum removal:

1. Compute the initial angular-momentum unit vector:

   $$
   \widehat{\mathbf{L}}(0)
   =
   \frac{\mathbf{L}(0)}
   {\lVert \mathbf{L}(0) \rVert}.
   $$

2. Rotate the system so

   $$
   \widehat{\mathbf{L}}(0)
   \mapsto
   \widehat{\mathbf{z}}.
   $$

3. Define the in-plane $+\widehat{\mathbf{x}}$ axis using the projected position of the canonically ordered heaviest body at $t=0$.
4. Define $+\widehat{\mathbf{y}}$ by a right-handed basis.
5. Apply that same rotation to the IC and to every target snapshot.
6. Store the inverse rotation for postprocessing back to the original COM frame.

This removes arbitrary global rotational gauge from the learning problem without changing the neural architecture.

Under that gauge-fixed pipeline, approve a **revised Option C** for the last five IC slots:

$$
[g_1,\dots,g_5]
=
[
I_1^{\mathrm{norm}},
I_2^{\mathrm{norm}},
I_3^{\mathrm{norm}},
c_1,
c_2
],
$$

where

$$
I_1^{\mathrm{norm}} = 2I_1 - 1,
$$

$$
I_2^{\mathrm{norm}} = 2I_2 - 1,
$$

$$
I_3^{\mathrm{norm}} = 6I_3 - 1,
$$

and

$$
c_i
=
\cos\theta_i
=
\frac{
\mathbf{r}'_i \cdot \mathbf{v}'_i
}{
\lVert \mathbf{r}'_i \rVert
\lVert \mathbf{v}'_i \rVert
+
\varepsilon
},
\qquad
i=1,2.
$$

Here $i=1,2$ refers to the first two canonically ordered bodies after canonical rotation.

The full recommended canonical 14D input is

$$
x =
[
\tau,
m_1^{\mathrm{norm}},
m_2^{\mathrm{norm}},
m_3^{\mathrm{norm}},
E^{\mathrm{norm}},
L_{\mathrm{norm}}^{\mathrm{in}},
Q^{\mathrm{norm}},
s_{\min}^{\mathrm{norm}},
I_{\mathrm{norm}}^{\mathrm{in}},
I_1^{\mathrm{norm}},
I_2^{\mathrm{norm}},
I_3^{\mathrm{norm}},
c_1,
c_2
].
$$

If the owner rejects canonical rotation and insists on raw Cartesian COM-frame targets, then none of the three currently documented options is sufficient, and D-01 should remain open rather than being “resolved” by Option B.

---

### D-02 — $I_{\mathrm{norm}}$: Raw Ratio Versus Tanh-Wrapped

I recommend approving the **tanh-wrapped form as the canonical network input** and keeping the raw ratio only as an intermediate physics descriptor:

$$
I_{\mathrm{norm}}^{\mathrm{raw}}
=
\frac{
\operatorname{tr}(I)
}{
M_{\mathrm{tot}} r_{\mathrm{char}}^2
},
$$

$$
I_{\mathrm{norm}}^{\mathrm{in}}
=
\tanh
\left(
I_{\mathrm{norm}}^{\mathrm{raw}}
\right).
$$

This reconciles the CTL text with the normalization code path and preserves the stated “all IC components into $[-1,1]$” contract.

This is a documentation decision, not a methodological one.

---

## 5. Minor Issues Triage

Most of the review's minor issues can remain minor **after** the core physics contract is repaired.

- D1 is documentation only.
- D2 and D3 should remain ablations, not preconditions.
- D4 and D6 are good engineering checks but not architectural blockers once a unified COM/mass-consistency transformer is in place.
- D8 is minor if the stage-gating metric is explicitly documented as unsoftened geometry rather than softened training physics.
- D10 is minor once the SIREN initialization contract is frozen.

The exception is **D9**. I would elevate D9 from minor to **blocking**, because the representational gap is not hypothetical: the review's preferred Option B does not provide enough information for raw Cartesian COM-frame prediction.

If the owner accepts the canonical-rotation recommendation above, D9 drops back down. Otherwise it should be treated as a first-tier blocker.

---

## 6. Cross-Issue Dependencies

The review's priority queue should be reordered.

The first dependency is **not** “fix $D$ to 6.694,” because that fix is tied to a different mass-scaling convention than the one the specs currently use.

The true first dependency is:

$$
\text{D-01} + \text{B-03} + \text{M1} + \text{M2} + \text{M4}.
$$

That is, decide the gauge and the exact 14D input contract first.

Then proceed in this order:

1. **Unify preprocessing.** Implement one transformer for COM correction, zero-momentum boosting, optional canonical rotation, and scaling. This closes B-05 and resolves the real content behind M3.
2. **Fix AD derivatives.** Compute componentwise time derivatives and apply the missing factors of $2$ and $4$. Until this is fixed, the physics loss is not the stated physics loss.
3. **Fix the softened dynamics contract.** Replace the current force/potential softening pair with one consistent softened Hamiltonian and state the epsilon policy explicitly.
4. **Lock the SIREN contract.** Retain the current hidden-layer initialization, remove epochwise $\omega_0$ scheduling, and then do citation-level cleanup on B-01 and M8.
5. **Run ablations and cleanup.** After the above, evaluate LayerNorm and complete remaining documentation tasks.

---

## 7. What Was Not Flagged

### Missed Issue 1 — Force–Energy Incompatibility Under Softening

The review flagged the epsilon mismatch but did not notice that the current softened force law and softened potential in `pinn_architecture.md` are not derivatives of one another.

This should be treated as a **new blocking issue**, because it breaks the internal contract between

$$
\mathcal{L}_{\mathrm{physics}}
$$

and

$$
\mathcal{L}_{\mathrm{energy}}.
$$

---

### Missed Issue 2 — D-01 Alternatives Are Mathematically Incomplete

The review's own D-01 alternatives are incomplete:

- Option A uses only $\sin\gamma_{\mathrm{orb}}$, which is not injective in orbital phase.
- Option B loses an orientation degree of freedom.
- M5 understates the $I_3$ range problem by treating

  $$
  I_3 \in [0,1]
  $$

  instead of the tighter range

  $$
  I_3 \in \left[0,\frac{1}{3}\right].
  $$

These are not stylistic problems. They materially affect whether the proposed IC vector can uniquely condition the network.

---

### Missed Issue 3 — The “ALM” Formulation Is Not a Standard Augmented Lagrangian

The supplied architecture defines

$$
\mathcal{L}_{\mathrm{total}}
=
\mathcal{L}_{\mathrm{data}}
+
\lambda_p \mathcal{L}_{\mathrm{physics}}
+
\frac{\mu_p}{2}
\mathcal{L}_{\mathrm{physics}}^2
+
\lambda_E
\mathcal{L}_{\mathrm{energy}},
$$

where $\mathcal{L}_{\mathrm{physics}}$ is already an MSE of residuals.

That makes the quadratic AL term effectively a **quartic penalty in the raw residual norm**.

A standard augmented Lagrangian would apply multipliers and quadratic penalties to the raw constraint, not to an already-squared scalar loss. Therefore the framework should either:

1. Reformulate this as a true ALM on pointwise residual constraints, or
2. Stop calling the current scalar rule “ALM” and treat it as an adaptive penalty heuristic.

The PINN optimization literature documents serious loss-balancing pathologies, which is why methods such as NTK weighting, GradNorm, and self-adaptive weighting exist. So the current ALM-like scalar rule should be treated as an empirical heuristic unless rewritten.

---

### Evidentiary Limitation

Because this audit was performed on the supplied markdown specifications rather than the live code, I cannot verify two implementation-state claims from the review with certainty:

1. Whether `update_omega0()` is actually dead code.
2. Whether the live derivative routine already avoids the collapsed vector-Jacobian pattern.

Where that distinction matters, I classify the issue as one of:

- **Document error**.
- **Code risk**.
- **Unverified implementation claim**.

I do not treat unverified implementation claims as confirmed code defects.
