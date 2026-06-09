---
edl_id: EDL-19-01
linked_gap: GAP-19-01
status: RESOLVED-WITH-INSTRUCTION (AMENDED)
phase: 19-physics-and-loss-contracts
topic: epsilon_H energy-drift denominator floor — Option C resolution (amended)
created: 2026-05-26
amended: 2026-05-26
amended_by: D-20 in .planning/milestones/v1.4-phases/19-physics-and-loss-contracts/19-CONTEXT.md
canonical: false
---

> **AMENDED 2026-05-26.** The formula in the prose below, `epsilon_H = max(1e-4 * S_H, 1e-12)`, was amended later the same day by user instruction. The canonical contract is `epsilon_H = 1e-4 * S_H` with **no fallback floor**; `S_H` must be finite and strictly positive or preprocessing/metadata validation MUST fail. Canonical records: `.planning/milestones/v1.4-phases/19-physics-and-loss-contracts/19-GAPS.md` (GAP-19-01 resolution note) and `.planning/milestones/v1.4-phases/19-physics-and-loss-contracts/19-CONTEXT.md` D-20. This EDL support brief is non-canonical and is preserved as a historical record of the user's original Option C selection.

According to a document from 2026-05-26, the current resolved framework keeps the raw-mass nondimensionalization (D=(GT^2)^{1/3}), uses ordered raw masses in the residual/Hamiltonian formulas, and rejects switching to the (GM_{\rm tot})-scaled convention unless the whole framework is rewritten in mass fractions. The same resolution defines the matched-Plummer Hamiltonian and the energy drift formula, but leaves (\epsilon_H) unbound; the attached EDL confirms this is the open `GAP-19-01` decision.

## Decision: **Option C — scale-relative rule**

Use a dataset-level absolute energy floor:

\[
\boxed{
\epsilon_H=\max\left(10^{-4}S_H,\ 10^{-12}\right)
}
\]

where (S_H) is computed once after final preprocessing, in float64, using the same matched-Plummer Hamiltonian components used by the training loss:

\[
K_{0,j}=\frac12\sum_i m_i\lVert v'_{0,i,j}\rVert^2
\]

\[
U^{abs}*{0,j}=\sum*{i<k}\frac{m_i m_k}
{\sqrt{\lVert r'*{0,i,j}-r'*{0,k,j}\rVert^2+\epsilon_{train}^2}}
\]

\[
\boxed{
S_H=\operatorname{median}*{j\in\mathcal D*{train}}
\left(K_{0,j}+U^{abs}_{0,j}\right)
}
\]

Then keep the original loss denominator exactly as:

\[
|H_{\epsilon}(r'_0,v'_0)|+\epsilon_H.
\]

Do **not** tie (\epsilon_H) to (\epsilon_{train}), (\epsilon_{inv}), or (\epsilon_L). Those have different physical/numerical roles; the EDL explicitly distinguishes (\epsilon_H) as a scalar conservation-drift denominator floor, not a distance, invariant, or angular-momentum floor.

## Why this rule

A fixed value such as (10^{-8}) is not well-defined under the project's own scaling unless it is anchored to a Hamiltonian scale. The EDL correctly flags that a familiar numerical floor would be arbitrary here unless justified for the dimensionless Hamiltonian magnitudes.

The rule above treats (\epsilon_H) as an **absolute tolerance inside a relative-error normalization**. That is the right numerical pattern when the reference quantity can be zero or near-zero: relative normalization alone becomes ill-conditioned near zero, so a positive absolute scale must be supplied. Python's own `math.isclose` documentation makes the same point for comparisons to zero, and NumPy warns that absolute tolerances must be chosen for the scale of the problem when the reference magnitude is small. ([Python documentation][1]) ([NumPy][2])

Use (K+|U|), not (|H|), to define (S_H). Near-zero (H=K-|U|) can arise from physical cancellation between kinetic and potential energy; using (\operatorname{median}|H_0|) as the scale can collapse exactly in the regime where the denominator problem matters. (K+|U|) measures the active dynamical energy scale without being destroyed by near-parabolic cancellation.

The factor (10^{-4}) makes the floor inactive for ordinary bound samples. If (S_H\sim 1) and (|H_0|\sim 0.1) to (10), then adding (10^{-4}S_H) changes the denominator by (10^{-3}) to (10^{-5}) relative. But for (|H_0|\ll 10^{-4}S_H), the term switches from meaningless strict relative error to an absolute Hamiltonian drift penalty measured against a stable dataset energy scale.

The Huber term helps, but it does not eliminate the denominator problem. With (\operatorname{Huber}_{1.0}), large normalized residuals are put in the linear regime, but the derivative with respect to the raw Hamiltonian difference still carries the factor

\[
\frac{1}{|H_0|+\epsilon_H}.
\]

So (\epsilon_H) still controls worst-case sample weighting and gradient scale. PyTorch's HuberLoss documentation confirms that (\delta=1) is the standard transition setting, equivalent to SmoothL1Loss at that value. ([PyTorch Docs][3])

## Plausible (|H_0|) range

There is no strictly positive lower bound for bound Newtonian systems. Write (U^{abs}=-V>0) and (Q=2K/U^{abs}). Then

\[
H=K-U^{abs}=\left(\frac{Q}{2}-1\right)U^{abs}.
\]

Bound systems satisfy (H<0), i.e. (Q<2). Virialized systems with (Q\approx 1) have

\[
|H|\approx \frac12 U^{abs},
\]

so if the scaled separations and velocities are order-one, (|H_0|) is usually order (10^{-1}) to (10^1), with tighter hierarchical configurations plausibly larger. But as (Q\to 2^{-}), (H\to 0^{-}) even while (K) and (U^{abs}) remain finite. The CTL instruction also treats near-zero total mechanical energy as marginally bound or unbound and more chaotic, not as a mere numerical artifact; Stage 0 "easy" cases are instead described with (E<-0.5) in normalized units.

So near-zero (|H_0|) is physically meaningful. The denominator floor should not erase those samples; it should prevent them from dominating the conservation loss through an ill-conditioned relative normalization.

## Return instruction

```text
For GAP-19-01 / EDL-19-01, choose Option C.

Instruction:
Bind epsilon_H as a dataset-scale absolute Hamiltonian floor:
epsilon_H = max(1e-4 * S_H, 1e-12), where
S_H = median_train(K0 + Uabs0), computed once in float64 after final
preprocessing using the matched-Plummer Hamiltonian with epsilon_train=1e-5.
Persist S_H and epsilon_H in training metadata. Use epsilon_H only in the
energy-drift denominator |H0| + epsilon_H.

Rationale:
Near-zero H0 is physically meaningful for marginally bound trajectories,
but strict relative error is ill-conditioned there. The rule preserves
relative drift for ordinary bound systems while switching marginal-energy
samples to a controlled absolute-energy scale. Huber(delta=1) caps loss
values but does not remove denominator-driven gradient/sample weighting.

Scope:
Phase 19 may now claim a concrete L_E default. Phase 21 should only validate
the activation rate, e.g. report Pr(|H0| < epsilon_H) and quantiles of
|H0|/S_H; it should not be required to choose epsilon_H from scratch.
```

Key assumption: (S_H) is computed over the training split after the final canonical COM/zero-momentum/gauge/scaling pipeline, not per minibatch. A minibatch-dependent (S_H) would make the objective nonstationary.

[1]: https://docs.python.org/3/library/math.html?utm_source=chatgpt.com "math — Mathematical functions"
[2]: https://numpy.org/doc/2.3/reference/generated/numpy.isclose.html?utm_source=chatgpt.com "numpy.isclose — NumPy v2.3 Manual"
[3]: https://pytorch.org/docs/stable/generated/torch.nn.HuberLoss.html?utm_source=chatgpt.com "HuberLoss — PyTorch 2.12 documentation"
