"""Phase 38 / NET-01 — locked science constants (spec-cited, single home).

Every value below is transcribed from the framework specs
(``ctl_instruction.md``, ``pinn_architecture.md``). Downstream modules
(network, residual, loss, probes) MUST import these names rather than
scattering literals. Constants are dtype-agnostic plain Python floats —
no precision/device default and no torch import (CTX-14 / CTX-20 / ENV-04).

This module does NOT import or copy the v1.3-era ``pinn/`` files
(``basic_architecture.py``, ``data-processing-pipeline-full.py``,
``data-handling/``); values are framework-spec-derived only (CTX-17).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Characteristic scales (dimensionless system)
# ---------------------------------------------------------------------------

# ctl_instruction.md §2.5 / PIPE-09 (line 1024): raw-mass convention
# D = (G T^2)^(1/3) ≈ 4.6416 with G = 1. The mass-fraction form
# D ≈ 6.694 is REJECTED and must not appear as a selectable value.
# Numeric value is cbrt(T^2) with T = 10 (PIPE-09 identity D^3 = G T^2).
D_CHARACTERISTIC_LENGTH = 100.0 ** (1.0 / 3.0)  # ≈ 4.6415888336...

# pinn_architecture.md Table 2 'Unit System' (line 980): Characteristic Time
# T = t_max; dataset horizon t_end = 10 fixes t_max = 10. Cross-checked by
# locked D = cbrt(G T^2) ≈ cbrt(100) via ctl_instruction.md §2.5 / PIPE-09.
# This is the normalizer for the u = t/T autograd leaf and the residual
# probe's r'→u finite-difference map (38-04 Gate B).
T_CHARACTERISTIC_TIME = 10.0

# ---------------------------------------------------------------------------
# Softening (PHYS-03 / training-time Plummer)
# ---------------------------------------------------------------------------

# pinn_architecture.md §3.2 / §3.4: training-time Plummer softening
# eps_soft = eps_train = 1e-5.
EPS_SOFT = 1e-5

# ---------------------------------------------------------------------------
# SIREN frequency (ARCH-01)
# ---------------------------------------------------------------------------

# pinn_architecture.md §2.2 / §2.4: first_omega_0 = 30.0, hidden_omega_0 = 1.0
# (ARCH-01 locked; no omega0 scheduler).
SIREN_FIRST_OMEGA_0 = 30.0
SIREN_HIDDEN_OMEGA_0 = 1.0

# ---------------------------------------------------------------------------
# Huber loss deltas
# ---------------------------------------------------------------------------

# pinn_architecture.md §3.1: data Huber delta_r = 1.
HUBER_DELTA_DATA = 1.0

# pinn_architecture.md §3.4: soft-energy Huber delta = 1.0.
HUBER_DELTA_ENERGY = 1.0

# pinn_architecture.md §3.5: angular-momentum Huber delta = 1.0.
HUBER_DELTA_ANGMOM = 1.0

# ---------------------------------------------------------------------------
# Angular-momentum floor + causal weights
# ---------------------------------------------------------------------------

# pinn_architecture.md §3.5: eps_L = 1e-8.
EPS_L = 1e-8

# pinn_architecture.md §3.2 (D-04 Option A): causal eta_c = 1, w_1 = 1.
CAUSAL_ETA_C = 1.0
CAUSAL_W1 = 1.0

# ---------------------------------------------------------------------------
# Time embedding (documented; consumers use the formula, not a free param)
# ---------------------------------------------------------------------------

# pinn_architecture.md §5.3.1: tau = 2u − 1 with t_tau ∈ [-1, 1].
# Encoded as the identity of the map; no free parameter beyond u = t/T.
# (Citation retained so CTX-15 source inspection finds §5.3.1.)
_TAU_MAP_DOC = "tau = 2u - 1; t_tau in [-1, 1] (pinn_architecture.md §5.3.1)"
