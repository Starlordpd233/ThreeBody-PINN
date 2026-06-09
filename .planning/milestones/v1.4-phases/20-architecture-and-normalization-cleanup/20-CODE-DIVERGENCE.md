# Phase 20 Code Divergence Inventory

This file is a forward-pointing FUT-01 hand-off artifact. It records where v1.3-era `pinn/` implementation files are expected to diverge from the Phase 20 framework-spec contracts. Per the 2026-05-19 user directive, live `pinn/` code is not v1.4 evidence and is not used as grounding for the spec decisions below.

This inventory aggregates the FUT-01 Hand-off Notes from the seven Phase 20 evidence packets (B-01, B-10, M5, M8, M9, M10, D-02-NORM). Most Phase 20 findings are naming/documentation cleanup with no formula or code change; this table is expectedly sparse. Row-level `FUT-01 priority` values are non-binding hand-off hints; FUT-01 planning may revise them.

| Surface | Live code (file:line) | Spec target (Phase 20 decision) | FUT-01 item | FUT-01 priority |
|---|---|---|---|---|
| LayerNorm affine default | `pinn/basic_architecture.py` (v1.3-era uses `elementwise_affine=True`) | `elementwise_affine=False` default contract (M8 verdict, `pinn_architecture.md`) | Change LayerNorm initialization from `elementwise_affine=True` to `elementwise_affine=False` to match the v1.4 spec contract. | MEDIUM |
| I_3 ratio-form descriptor and staging map | `pinn/data-processing-pipeline-full.py` (v1.3-era may contain issue-doc's sorted-distance normalization) | Raw `I_3 ∈ [0, 1/3]`, staging map `I_3^{in} = 6·I_3 − 1`, metadata-only scope (M5 verdict, `ctl_instruction.md`) | Compute `I_3` as the ratio-form descriptor with raw range `[0, 1/3]` and, for staging/metadata use, map via `I_3^{in} = 6·I_3 − 1`. Do NOT implement the issue-doc's `2*(I_i/I_max) − 1` sorted-distance normalization. | HIGH |
| SIREN omega0 init (already consistent) | `pinn/basic_architecture.py:37` (v1.3-era already divides by `self.omega_0`) | `first_omega_0=30`, `hidden_omega_0=1`, divide-by-`hidden_omega_0`, no in-run scheduler (B-01/B-10 verdicts, `pinn_architecture.md`) | Verify v1.3-era init matches the v1.4 fixed contract. FUT-01 rebuilds from the v1.4 spec; the v1.3-era code is already consistent. No divergence fix needed. | LOW |

**Not FUT-01-applicable (no code divergence):**
- **B-10** (dynamic scheduler removal): Spec cleanup removes scheduler guidance that was never runtime-effective (omega0 is initialization-only).
- **M9** (energy normalization support): Documents dataset-occupied range; no formula change. `tanh(E / E_scale)` preserved as-is.
- **M10** (mass normalization support): Documents dataset-occupied range; no formula change. `tanh((m_i - mu)/(sigma + 10^-8))` preserved as-is.
- **D-02-NORM** (I_norm naming): Naming conventions in the framework spec only; no v1.3-era code divergence created.
