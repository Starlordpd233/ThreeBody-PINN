---
paths:
  - "pinn/**"
  - "pinn_instruction/**"
  - ".planning/phases/**"
---

## PINN Architecture and Input Vector

> **Note (v1.4 update 2026-05-19):** During v1.4 and until FUT-01 ships, the framework specs (`pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` and `pinn_architecture.md`) are the authoritative source for input-vector and architecture content. The v1.3-era code in `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` is **NOT** authoritative — it is reference-only. FUT-01 will rebuild the code from the v1.4 specs.

### Architecture (SQR-SkipResNet-SIREN backbone)

Locked v1.4 architecture decisions (see `.planning/milestones/v1.4-phases/17-input-and-output-contracts/17-CONTEXT.md` Tier A):
- **Input**: 14 dims = `[τ, IC₁₃]` where `τ = 2u − 1`, autograd leaf `u = t/T` (D-03 LOCKED 2026-05-18)
- **Output**: 9 dims (3D positions for 3 bodies) with a hard mass-weighted COM projection head applied before any loss/metric (D-02 LOCKED 2026-05-18)

Preserved from v1.3, still subject to Phase 20 review (ARCH-01/02):
- **Hidden**: 12 layers × 256 neurons
- **SIREN**: first_omega_0=30.0, hidden_omega_0=1.0 — Phase 20 ARCH-01 will lock final values
- **Skip + LayerNorm**: power p=2, LayerNorm on odd layers — Phase 20 ARCH-02 will lock the affine default

### IC Vector (13 components — v1.4 contract under construction)

The v1.4 milestone replaces the v1.3-era IC vector with Jacobi-state IC₁₃ per resolution doc §5.3 — see `.planning/milestones/v1.4-phases/17-input-and-output-contracts/17-CONTEXT.md` D-01 (LOCKED 2026-05-18):

```
IC₁₃ = [m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]
```

All slots normalized via `tanh((z − μ_z) / (σ_z + 10⁻⁸))` with dataset-wide statistics. Mass slot encoding (raw vs fraction) is **GAP-17-01** — OPEN, awaiting user instruction.

**v1.3-era IC vector** (NOT authoritative; kept for FUT-01 reference only):
m1, m2, m3 (mass fractions), E, L_norm, Q, s_min, I1, I2, I3 (shape invariants), theta1, theta2, I_norm. All normalized to [-1, 1].

## PINN Development Commands

```bash
# Architecture sanity check
python pinn/basic_architecture.py

# Data processing (preprocessing + stage batches)
python pinn/data-processing-pipeline-full.py --input /path/to/preprocessed.h5 --output_dir /path/to/stage_data
```
