"""Phase 59 (FEAS-07; D-15): the two-Kepler comparison formula.

The inner pair (IC-file bodies 1 and 2, tracked through the canonical
permutation as ``inner_pair``) moves on a Kepler orbit with
``mu = m_a + m_b``. The third body moves about the inner pair's centre of
mass on a Kepler orbit with ``mu = m_a + m_b + m_c``. Both orbits are
propagated analytically with Lagrange f and g functions, so velocities come
from the same solution, and the three positions are rebuilt about a centre
of mass that moves at the initial centre-of-mass velocity.

The same masses work unchanged in the pipeline frame ``(r', u)``, because
``mu T^2 / D^3 = mu`` when ``D^3 = T^2`` and ``G = 1``. An unbound inner or
outer orbit raises ``NotApplicable``; it is recorded, never patched.

Numpy and the standard library only. No file access.
"""

from __future__ import annotations

import numpy as np


_NEWTON_MAX_ITER = 60
_NEWTON_TOL = 1e-14
_NOT_HIERARCHICAL = "not applicable: no hierarchical split"


class NotApplicable(Exception):
    """The formula does not apply to this state. ``reason`` says why."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = str(reason)


def propagate_bound(s0, v0, mu, dt):
    """Propagate a bound Kepler orbit by each elapsed time in ``dt``.

    Returns ``(s, v)`` with shape ``(len(dt), 3)``. Raises ``NotApplicable``
    when the orbit is not bound (``1/a <= 0``) and ``RuntimeError`` when the
    Newton solve for the eccentric-anomaly change does not converge.
    """
    s0 = np.asarray(s0, dtype=np.float64).reshape(3)
    v0 = np.asarray(v0, dtype=np.float64).reshape(3)
    mu = float(mu)
    dt = np.asarray(dt, dtype=np.float64).reshape(-1)
    r0 = float(np.linalg.norm(s0))
    if not r0 > 0.0:
        raise NotApplicable("zero separation")
    speed_sq = float(np.dot(v0, v0))
    if speed_sq >= 2.0 * mu / r0:
        raise NotApplicable(f"unbound orbit (|v|^2 = {speed_sq!r} >= 2 mu / r = {2.0 * mu / r0!r})")
    a = 1.0 / (2.0 / r0 - speed_sq / mu)
    n = float(np.sqrt(mu / a ** 3))
    sigma = float(np.dot(s0, v0)) / float(np.sqrt(mu))
    k1 = 1.0 - r0 / a
    k2 = sigma / float(np.sqrt(a))
    mean = n * dt
    delta = mean.copy()
    for _ in range(_NEWTON_MAX_ITER):
        residual = delta - k1 * np.sin(delta) + k2 * (1.0 - np.cos(delta)) - mean
        slope = 1.0 - k1 * np.cos(delta) + k2 * np.sin(delta)
        step = residual / slope
        delta = delta - step
        tolerance = _NEWTON_TOL * max(1.0, float(np.max(np.abs(delta), initial=0.0)))
        if float(np.max(np.abs(step), initial=0.0)) <= tolerance:
            break
    else:
        raise RuntimeError("Kepler Newton solve did not converge")
    cos_d = np.cos(delta)
    sin_d = np.sin(delta)
    r = a + (r0 - a) * cos_d + sigma * float(np.sqrt(a)) * sin_d
    f = 1.0 - (a / r0) * (1.0 - cos_d)
    g = dt - (delta - sin_d) / n
    fdot = -(float(np.sqrt(mu * a)) / (r * r0)) * sin_d
    gdot = 1.0 - (a / r) * (1.0 - cos_d)
    s = f[:, None] * s0 + g[:, None] * v0
    v = fdot[:, None] * s0 + gdot[:, None] * v0
    return s, v


def _slots(inner_pair):
    a, b = (int(value) for value in inner_pair)
    if a == b or {a, b} - {0, 1, 2}:
        raise ValueError(f"inner_pair must name two distinct slots of 0, 1, 2; got {inner_pair!r}")
    c = ({0, 1, 2} - {a, b}).pop()
    return a, b, c


def two_kepler_prediction(r0, v0, masses, inner_pair, dt):
    """Positions and velocities ``(N, 3, 3)`` at each elapsed time in ``dt``."""
    r0 = np.asarray(r0, dtype=np.float64).reshape(3, 3)
    v0 = np.asarray(v0, dtype=np.float64).reshape(3, 3)
    masses = np.asarray(masses, dtype=np.float64).reshape(3)
    dt = np.asarray(dt, dtype=np.float64).reshape(-1)
    a, b, c = _slots(inner_pair)
    m_a, m_b, m_c = (float(masses[a]), float(masses[b]), float(masses[c]))
    m_ab = m_a + m_b
    total = m_ab + m_c
    s0 = r0[b] - r0[a]
    sdot0 = v0[b] - v0[a]
    pair0 = (m_a * r0[a] + m_b * r0[b]) / m_ab
    pairdot0 = (m_a * v0[a] + m_b * v0[b]) / m_ab
    lam0 = r0[c] - pair0
    lamdot0 = v0[c] - pairdot0
    com0 = (m_ab * pair0 + m_c * r0[c]) / total
    vcom = (m_ab * pairdot0 + m_c * v0[c]) / total
    try:
        s, sdot = propagate_bound(s0, sdot0, m_ab, dt)
    except NotApplicable as exc:
        raise NotApplicable(f"inner orbit: {exc.reason}") from exc
    try:
        lam, lamdot = propagate_bound(lam0, lamdot0, total, dt)
    except NotApplicable as exc:
        raise NotApplicable(f"outer orbit: {exc.reason}") from exc
    com = com0 + dt[:, None] * vcom
    pair = com - (m_c / total) * lam
    pairdot = vcom - (m_c / total) * lamdot
    positions = np.empty((dt.size, 3, 3), dtype=np.float64)
    velocities = np.empty_like(positions)
    positions[:, a] = pair - (m_b / m_ab) * s
    positions[:, b] = pair + (m_a / m_ab) * s
    positions[:, c] = com + (m_ab / total) * lam
    velocities[:, a] = pairdot - (m_b / m_ab) * sdot
    velocities[:, b] = pairdot + (m_a / m_ab) * sdot
    velocities[:, c] = vcom + (m_ab / total) * lamdot
    return positions, velocities


def two_kepler_accelerations(positions, masses, inner_pair):
    """The exact second derivative of the assembled positions, no softening."""
    positions = np.asarray(positions, dtype=np.float64).reshape(-1, 3, 3)
    masses = np.asarray(masses, dtype=np.float64).reshape(3)
    a, b, c = _slots(inner_pair)
    m_a, m_b, m_c = (float(masses[a]), float(masses[b]), float(masses[c]))
    m_ab = m_a + m_b
    total = m_ab + m_c
    s = positions[:, b] - positions[:, a]
    pair = (m_a * positions[:, a] + m_b * positions[:, b]) / m_ab
    lam = positions[:, c] - pair
    s_dd = -m_ab * s / np.linalg.norm(s, axis=-1, keepdims=True) ** 3
    lam_dd = -total * lam / np.linalg.norm(lam, axis=-1, keepdims=True) ** 3
    accelerations = np.empty_like(positions)
    accelerations[:, a] = -(m_c / total) * lam_dd - (m_b / m_ab) * s_dd
    accelerations[:, b] = -(m_c / total) * lam_dd + (m_a / m_ab) * s_dd
    accelerations[:, c] = (m_ab / total) * lam_dd
    return accelerations


def formula_applicability(variant):
    """``None`` for hierarchical records; the not-applicable string for standard ones (D-38)."""
    if variant == "hierarchical":
        return None
    if variant == "standard":
        return _NOT_HIERARCHICAL
    raise ValueError(f"unknown variant {variant!r}")


__all__ = [
    "NotApplicable",
    "formula_applicability",
    "propagate_bound",
    "two_kepler_accelerations",
    "two_kepler_prediction",
]
