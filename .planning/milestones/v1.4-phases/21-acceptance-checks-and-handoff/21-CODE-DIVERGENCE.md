# Phase 21 Code Divergence Inventory

This file is a forward-pointing FUT-01 hand-off artifact. Per the 2026-05-19 user directive, live `pinn/` code is not v1.4 evidence and was not inspected as grounding during Phase 21 repair.

Phase 21's disposable probes validate the v1.4 framework specs for implementability. They are not production code and do not prove the v1.3-era `pinn/` implementation is aligned.

| Spec target validated by probe | FUT-01 implication | FUT-01 priority |
|---|---|---|
| Raw-mass nondimensionalization uses `D^3 = G*T^2` and no free residual `G` coefficient. | Rebuilt preprocessing/residual code should preserve raw masses and the `D = (G*T^2)^(1/3)` scaling convention unless a future mass-fraction rewrite is explicitly planned. | HIGH |
| Output positions are hard-projected to zero mass-weighted COM using ordered raw masses. | Rebuilt model output path should apply the architectural COM projection before losses, diagnostics, and evaluation consumers. | HIGH |
| Derivatives are componentwise with respect to canonical `u=t/T`, not vector-Jacobian products over summed outputs. | Rebuilt physics residual and conservation losses should compute full componentwise Jacobians/Hessians or equivalent, not `grad(r.sum(), u)` shortcuts. | HIGH |
| Matched-Plummer force residual and matched-Plummer Hamiltonian share `epsilon_train = 1e-5` and the same `r_safe` denominator. | Rebuilt physics and energy-loss code should use one matched training-time softening contract for residual force and `H_epsilon`. | HIGH |
| Loss dry run requires SIREN, skip/power branch, `LayerNorm(elementwise_affine=False)`, 14D input, 9D output, and finite data/IC/physics/energy/angular loss scalars. | Rebuilt architecture/loss code should instantiate the v1.4 SQR-SkipResNet-SIREN contract rather than a generic MLP placeholder. | HIGH |

**Not FUT-01 evidence:**

- The disposable probes under `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/`.
- The numerical values in `21-PROBE-RESULTS.md` beyond their role as v1.4 spec consistency checks.
- Any inference about current `pinn/` implementation behavior.
