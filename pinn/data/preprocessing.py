"""Phase 39 — pure CTL preprocessing, invariants, and IC13 transforms.

Implements ``ctl_instruction.md`` Step 2 (Unified Preprocessing Pipeline),
Step 3 (invariants), and the normalization half of Step 4 (network input
assembly), over raw float64 NumPy arrays. No dtype/device conversion, no
corpus I/O, and no numeric Stage-0/1 classification happen here (GAP-39-08:
that is the sole responsibility of ``pinn/data/stages.py``).

Locked pipeline order (``ctl_instruction.md:789-801``)::

    parse -> mass-invariance check -> COM recenter -> zero-momentum boost ->
    canonical ordering -> canonical rotation gauge -> global scaling ->
    assertions and stored metadata.

``D_CHARACTERISTIC_LENGTH`` is imported from ``pinn.constants`` (the locked
raw-mass ``D ~ 4.6416`` convention, PIPE-09); no mass-fraction ``6.694`` path
is selectable here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME

# ---------------------------------------------------------------------------
# Static-invariant softening (ctl_instruction.md §3, distinct from the
# training-time PHYS-03 softening ``pinn.constants.EPS_SOFT == 1e-5``).
# ---------------------------------------------------------------------------

EPS_INV = 1e-10

# Rotation-gauge degeneracy guard (ctl_instruction.md §2.4).
ETA_GAUGE = 1e-8

# Step 2.6 postcondition tolerances.
_COM_TOL = 1e-12
_MOMENTUM_TOL = 1e-12

# Mass-invariance gate (ctl_instruction.md §2.1).
MASS_INVARIANCE_TOL = 1e-15

_N_BODIES = 3


class MassInvarianceError(ValueError):
    """Per-body mass varies across the trajectory beyond ``MASS_INVARIANCE_TOL``."""


class GaugeDegenerateError(ValueError):
    """The primary Jacobi vector ``rho`` is too small to fix a rotation gauge
    (``gauge_degenerate_rho``, ctl_instruction.md §2.4)."""


class PreprocessAssertionError(ValueError):
    """A Step-2.6 COM/momentum postcondition failed after preprocessing."""


@dataclass
class PreprocessedTrajectory:
    """The gauge-fixed, scaled trajectory + frame/gauge metadata (§2.6)."""

    masses_ordered: Any        # (3,) raw ordered masses (unscaled)
    permutation: Any           # (3,) canonical-order indices into the input
    r_com_ordered: Any         # (Nt, 3, 3) positions: COM/boost-gauged + canonically ordered.
                               # NOT rotation-gauged, NOT scaled by D. CONF-08 resident surface.
    v_com_ordered: Any         # (Nt, 3, 3) velocities: same two transforms only.
    r0_gauge: Any              # (3, 3) initial positions, ordered+gauged+scaled
    v0_gauge: Any              # (3, 3) initial velocities, ordered+gauged+scaled
    r_gauge: Any               # (Nt, 3, 3) full trajectory positions, scaled
    v_gauge: Any                # (Nt, 3, 3) full trajectory velocities, scaled
    R0: Any                     # (3, 3) rotation matrix
    R_COM0: Any                 # (3,) initial COM position
    V_COM: Any                  # (3,) COM velocity
    D: float
    T: float
    V: float


def check_mass_invariance(masses_per_snapshot):
    """``max_{t,i} |m_i(t) - m_i(0)| < 1e-15`` (§2.1). Raises
    :class:`MassInvarianceError` on violation; returns the observed max drift.
    """
    arr = np.asarray(masses_per_snapshot, dtype=np.float64)
    if arr.ndim == 1:
        return 0.0
    drift = float(np.max(np.abs(arr - arr[0])))
    if drift >= MASS_INVARIANCE_TOL:
        raise MassInvarianceError(
            f"mass invariance violated: max drift {drift!r} >= {MASS_INVARIANCE_TOL!r}"
        )
    return drift


def _com_recenter_and_boost(times, positions, velocities, masses):
    """§2.2: COM recenter + zero-momentum boost, applied to ALL variants."""
    M = float(np.sum(masses))
    r0 = positions[0]
    v0 = velocities[0]
    R_COM0 = np.sum(masses[:, None] * r0, axis=0) / M
    V_COM = np.sum(masses[:, None] * v0, axis=0) / M

    t = np.asarray(times, dtype=np.float64)
    r_bar = positions - R_COM0[None, None, :] - V_COM[None, None, :] * t[:, None, None]
    v_bar = velocities - V_COM[None, None, :]
    return r_bar, v_bar, R_COM0, V_COM


def _canonical_order(masses, r_bar0, v_bar0):
    """§2.3: sort bodies by descending mass, then position norm, velocity norm,
    then original file order (stable sort preserves the final tie-break)."""
    n = masses.shape[0]
    pos_norm = np.linalg.norm(r_bar0, axis=1)
    vel_norm = np.linalg.norm(v_bar0, axis=1)
    order = np.arange(n)  # original file order (last tie-break, stable sort)
    # Sort ascending on negated keys == descending on the real keys; np.lexsort
    # ranks by the LAST key first, so list keys with the primary key last.
    keys = (order, -vel_norm, -pos_norm, -masses)
    permutation = np.lexsort(keys)
    return permutation


def _rotation_gauge(masses, r_bar0, v_bar0, D, T):
    """§2.4: canonical rotation gauge from the Jacobi basis at t=0."""
    m1, m2, m3 = masses[0], masses[1], masses[2]
    rho = r_bar0[1] - r_bar0[0]
    lam = r_bar0[2] - (m1 * r_bar0[0] + m2 * r_bar0[1]) / (m1 + m2)

    V = D / T
    eps_rho = ETA_GAUGE * D
    eps_lambda = ETA_GAUGE * D
    eps_v = ETA_GAUGE * V

    rho_norm = float(np.linalg.norm(rho))
    if rho_norm <= eps_rho:
        raise GaugeDegenerateError("gauge_degenerate_rho")
    e_x = rho / rho_norm

    lam_perp = lam - np.dot(lam, e_x) * e_x
    lam_perp_norm = float(np.linalg.norm(lam_perp))

    if lam_perp_norm > eps_lambda:
        e_y = lam_perp / lam_perp_norm
    else:
        rho_dot = v_bar0[1] - v_bar0[0]
        lambda_dot = v_bar0[2] - (m1 * v_bar0[0] + m2 * v_bar0[1]) / (m1 + m2)
        candidates = [rho_dot, lambda_dot, v_bar0[0], v_bar0[1], v_bar0[2]]
        e_y = None
        for c in candidates:
            c_perp = c - np.dot(c, e_x) * e_x
            c_perp_norm = float(np.linalg.norm(c_perp))
            if c_perp_norm > eps_v:
                e_y = c_perp / c_perp_norm
                break
        if e_y is None:
            # Fixed coordinate basis vector least aligned with e_x.
            basis = np.eye(3)
            alignment = np.abs(basis @ e_x)
            fallback = basis[int(np.argmin(alignment))]
            f_perp = fallback - np.dot(fallback, e_x) * e_x
            e_y = f_perp / float(np.linalg.norm(f_perp))
        # Deterministic sign: keep lambda_y >= 0 whenever numerically meaningful.
        if np.dot(lam_perp, e_y) < 0:
            e_y = -e_y

    e_z = np.cross(e_x, e_y)
    R0 = np.stack([e_x, e_y, e_z], axis=0)
    return R0


def preprocess_trajectory(times, positions, velocities, masses):
    """Run the full §2.1-2.6 pipeline over one raw float64 trajectory.

    ``positions``/``velocities`` are ``(Nt, 3, 3)``; ``masses`` is ``(3,)``
    (cross-snapshot mass invariance is enforced upstream at parse time, before
    this call -- see ``pinn/data/types.py::ParsedTrajectory``). Raises
    :class:`GaugeDegenerateError` or :class:`PreprocessAssertionError` on a
    §2.4/§2.6 failure (caller quarantines/rejects, consistent with the §2.1
    mass-invariance failure pattern).
    """
    times = np.asarray(times, dtype=np.float64)
    positions = np.asarray(positions, dtype=np.float64)
    velocities = np.asarray(velocities, dtype=np.float64)
    masses = np.asarray(masses, dtype=np.float64)

    r_bar, v_bar, R_COM0, V_COM = _com_recenter_and_boost(times, positions, velocities, masses)

    permutation = _canonical_order(masses, r_bar[0], v_bar[0])
    masses_ordered = masses[permutation]
    r_bar = r_bar[:, permutation, :]
    v_bar = v_bar[:, permutation, :]

    D = D_CHARACTERISTIC_LENGTH
    T = T_CHARACTERISTIC_TIME
    R0 = _rotation_gauge(masses_ordered, r_bar[0], v_bar[0], D, T)

    r_gauge_pre = np.einsum("ij,tbj->tbi", R0, r_bar)
    v_gauge_pre = np.einsum("ij,tbj->tbi", R0, v_bar)

    V = D / T
    r_scaled = r_gauge_pre / D
    v_scaled = v_gauge_pre / V

    com_norm = float(np.linalg.norm(np.sum(masses_ordered[:, None] * r_scaled[0], axis=0)))
    momentum_norm = float(np.linalg.norm(np.sum(masses_ordered[:, None] * v_scaled[0], axis=0)))
    if com_norm >= _COM_TOL or momentum_norm >= _MOMENTUM_TOL:
        raise PreprocessAssertionError(
            f"COM/momentum postcondition failed: com_norm={com_norm!r} "
            f"momentum_norm={momentum_norm!r}"
        )

    return PreprocessedTrajectory(
        masses_ordered=masses_ordered, permutation=permutation,
        r_com_ordered=r_bar, v_com_ordered=v_bar,
        r0_gauge=r_scaled[0], v0_gauge=v_scaled[0],
        r_gauge=r_scaled, v_gauge=v_scaled,
        R0=R0, R_COM0=R_COM0, V_COM=V_COM, D=D, T=T, V=V,
    )


# ---------------------------------------------------------------------------
# Step 3: invariants (E, Q, s_min, L_norm/l_ratio).
# ---------------------------------------------------------------------------

@dataclass
class Invariants:
    E: float
    Q: float
    s_min: float
    l_ratio: Any        # None when L_max is degenerate.
    l_ratio_reason: Any  # None, or "degenerate_Lmax".


def _pairwise_norms(r):
    return [float(np.linalg.norm(r[i] - r[j])) for i in range(_N_BODIES) for j in range(i + 1, _N_BODIES)]


def compute_invariants(masses, r0, v0):
    """Compute ``(E, Q, s_min, L_norm)`` from ONE scaled initial condition
    (``ctl_instruction.md`` §3.1-3.2). ``r0``/``v0`` are ``(3, 3)``."""
    masses = np.asarray(masses, dtype=np.float64)
    r0 = np.asarray(r0, dtype=np.float64)
    v0 = np.asarray(v0, dtype=np.float64)

    T_kin = 0.5 * float(np.sum(masses * np.sum(v0 * v0, axis=1)))
    V_pot = 0.0
    for i in range(_N_BODIES):
        for j in range(i + 1, _N_BODIES):
            r_safe = np.sqrt(np.sum((r0[i] - r0[j]) ** 2) + EPS_INV ** 2)
            V_pot -= masses[i] * masses[j] / r_safe
    E = T_kin + V_pot
    Q = 2.0 * T_kin / abs(V_pot) if V_pot != 0.0 else float("inf")
    s_min = min(_pairwise_norms(r0))

    l_ratio, l_ratio_reason = compute_l_ratio(masses, r0, v0, E)
    return Invariants(E=E, Q=Q, s_min=s_min, l_ratio=l_ratio, l_ratio_reason=l_ratio_reason)


def compute_l_ratio(masses, r0, v0, E, l_max_floor=1e-10):
    """``L_norm = L / L_max`` with the mandatory degenerate-``L_max`` guard
    (Phase 33 contract, ``ctl_instruction.md`` §3 item 2). Raw, un-clipped; no
    global clamp. Returns ``(None, "degenerate_Lmax")`` when ``L_max`` is
    non-finite or below ``l_max_floor`` (near-zero ``|E|`` / near-collision)."""
    masses = np.asarray(masses, dtype=np.float64)
    r0 = np.asarray(r0, dtype=np.float64)
    v0 = np.asarray(v0, dtype=np.float64)

    L_vec = np.sum([masses[i] * np.cross(r0[i], v0[i]) for i in range(_N_BODIES)], axis=0)
    L = float(np.linalg.norm(L_vec))
    r_char = float(np.mean(_pairwise_norms(r0)))
    M_total = float(np.sum(masses))
    v_char = np.sqrt(2.0 * abs(E) / M_total) if M_total > 0 else float("nan")
    L_max = M_total * r_char * v_char

    if not np.isfinite(L_max) or L_max < l_max_floor:
        return None, "degenerate_Lmax"
    return L / L_max, None


# ---------------------------------------------------------------------------
# Step 4: IC13 assembly + admitted-population normalization.
# ---------------------------------------------------------------------------

IC13_SIZE = 13


def build_raw_ic13(masses_ordered, r0_gauge, v0_gauge, E):
    """Assemble the exact 13-component raw (pre-normalization) IC vector::

        [m1, m2, m3, rho_x, lambda_x, lambda_y,
         rho_dot_x, rho_dot_y, rho_dot_z,
         lambda_dot_x, lambda_dot_y, lambda_dot_z, E]

    (``ctl_instruction.md`` §4 network-input contract). Positions retained are
    ONLY ``rho_x``, ``lambda_x``, ``lambda_y`` (the FRAME-01 gauge); velocities
    remain fully 3D.
    """
    masses_ordered = np.asarray(masses_ordered, dtype=np.float64)
    r0_gauge = np.asarray(r0_gauge, dtype=np.float64)
    v0_gauge = np.asarray(v0_gauge, dtype=np.float64)
    m1, m2 = masses_ordered[0], masses_ordered[1]

    rho = r0_gauge[1] - r0_gauge[0]
    lam = r0_gauge[2] - (m1 * r0_gauge[0] + m2 * r0_gauge[1]) / (m1 + m2)
    rho_dot = v0_gauge[1] - v0_gauge[0]
    lam_dot = v0_gauge[2] - (m1 * v0_gauge[0] + m2 * v0_gauge[1]) / (m1 + m2)

    return np.array([
        masses_ordered[0], masses_ordered[1], masses_ordered[2],
        rho[0], lam[0], lam[1],
        rho_dot[0], rho_dot[1], rho_dot[2],
        lam_dot[0], lam_dot[1], lam_dot[2],
        E,
    ], dtype=np.float64)


@dataclass
class NormalizationStats:
    slot_means: Any     # (12,) -- the 12 pre-energy IC13 slots
    slot_stds: Any
    e_scale: float


def compute_normalization_stats(raw_ic13_population, trajectory_energies):
    """Admitted-population per-slot mean/std over the first 12 IC13 slots plus
    the trajectory-energy scale (``ctl_instruction.md`` §2.5/§4)::

        E_scale = |median(trajectory E)| + 1e-8
    """
    pop = np.asarray(raw_ic13_population, dtype=np.float64)
    if pop.ndim != 2 or pop.shape[1] != IC13_SIZE:
        raise ValueError(f"raw_ic13_population must be (N, {IC13_SIZE}); got {pop.shape}")
    slot_means = np.mean(pop[:, :12], axis=0)
    slot_stds = np.std(pop[:, :12], axis=0)
    e_scale = float(abs(np.median(np.asarray(trajectory_energies, dtype=np.float64))) + 1e-8)
    return NormalizationStats(slot_means=slot_means, slot_stds=slot_stds, e_scale=e_scale)


def normalize_ic13(raw_ic13, stats: NormalizationStats):
    """``z_in = tanh((z - mu) / (sigma + 1e-8))`` for the 12 mass/Jacobi slots
    and ``tanh(E / E_scale)`` for the final energy slot."""
    raw_ic13 = np.asarray(raw_ic13, dtype=np.float64)
    normalized_first_12 = np.tanh((raw_ic13[:12] - stats.slot_means) / (stats.slot_stds + 1e-8))
    normalized_energy = np.tanh(raw_ic13[12] / stats.e_scale)
    return np.concatenate([normalized_first_12, [normalized_energy]]).astype(np.float64)
