"""Phase 43 / ACC-03 (43-02 Task 1) — the position-only Hamiltonian gate metric.

Renders the authoritative post-v1.3 acceptance gate (``ctl_instruction.md``
§2.4.5 clause 5 / ``REQUIREMENTS.md`` ACC-03) from a MODEL's predicted
positions, rather than from a parsed Brutus trajectory. The evaluator
(``pinn/evaluate.py``) runs the model forward pass exactly once under
``.eval()`` + ``torch.no_grad()`` and hands the detached predicted positions
here; this module NEVER differentiates w.r.t. the input time leaf — velocity
is obtained by finite-differencing the predicted positions over the persisted
monotone snapshot times (one-sided endpoint, centered interior — the same
scheme ``pinn.data.adapter.AdmittedSetAdapter.acceleration_magnitudes`` uses
for its own finite difference), so the forward pass genuinely stays no-grad
(review HIGH: "pred_velocities derivation conflicts with the mandated no-grad
forward").

Gate contract (43-SPEC.md / ``ctl_instruction.md`` §2.4.5 clause 5):

* Hamiltonian ``H = T + V`` is computed on detached CPU float64 tensors using
  the Plummer potential-only softening ``eps_inv = 1e-10`` — NEVER the
  training-time softening ``pinn.constants.EPS_SOFT = 1e-5`` (distinct
  quantities; matched-Plummer form only, PHYS-03 anti-pattern avoided).
* Per-trajectory ``eps_H = max_t |(H(t) - H(0)) / H(0)|``.
* The TEST-SET aggregate ``eps_H`` is the WORST (maximum) finite
  per-trajectory ``eps_H``; ``SCS = log10(aggregate eps_H)`` is derived ONLY
  from that aggregate — never averaged, never per-trajectory-gated separately.
* ``gate_verdict`` is the single source of truth for PASS/FAIL: FAIL for any
  non-finite aggregate, FAIL for ``eps_H > 1e-5`` (equivalently
  ``SCS > -5``); the boundary itself PASSES (SPEC edge R3 / prohibition 1 —
  reject is a STRICT inequality, never rendered backwards).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import torch

__all__ = [
    "EPS_INV",
    "GATE_EPS_H_REJECT_THRESHOLD",
    "GATE_SCS_REJECT_THRESHOLD",
    "TrajectoryGateMetrics",
    "AggregateGateMetrics",
    "finite_difference_velocity",
    "matched_plummer_hamiltonian_series",
    "trajectory_eps_h",
    "compute_trajectory_gate_metrics",
    "aggregate_test_eps_h",
    "scs_from_eps_h",
    "gate_verdict",
    "aggregate_gate_verdict",
]

# Validation-gate Plummer softening (``ctl_instruction.md`` §2.4.5 clause 5 /
# §Numerical notes and defaults) — DISTINCT from the training-time softening
# ``pinn.constants.EPS_SOFT = 1e-5``. Never substitute one for the other.
EPS_INV = 1e-10

# The authoritative post-v1.3 acceptance gate (REQUIREMENTS.md ACC-03):
# REJECT if eps_H > 1e-5, equivalently REJECT if SCS > -5. Both boundaries
# PASS (strict-inequality reject only).
GATE_EPS_H_REJECT_THRESHOLD = 1e-5
GATE_SCS_REJECT_THRESHOLD = -5.0

_N_BODIES = 3
_N_DIMS = 3
_PAIRS = ((0, 1), (0, 2), (1, 2))


def _as_cpu_f64(value) -> torch.Tensor:
    """Detach + coerce to a plain CPU float64 tensor (never grad-tracked)."""
    tensor = torch.as_tensor(value)
    return tensor.detach().to(dtype=torch.float64, device="cpu")


# ---------------------------------------------------------------------------
# No-grad finite-difference velocity (review HIGH fix).
# ---------------------------------------------------------------------------


def finite_difference_velocity(positions, times) -> torch.Tensor:
    """Derive velocity from predicted positions via finite differences only.

    One-sided (forward/backward) endpoint differences plus a centered interior
    difference over the persisted monotone snapshot ``times`` — the model
    forward pass that produced ``positions`` never needs ``requires_grad``.

    Args:
        positions: ``(T, 3, 3)`` predicted positions (body, coord).
        times: ``(T,)`` strictly increasing snapshot times.

    Returns:
        ``(T, 3, 3)`` velocity, on a detached CPU float64 tensor.
    """
    with torch.no_grad():
        pos = _as_cpu_f64(positions)
        t = _as_cpu_f64(times)
        if t.dim() != 1:
            raise ValueError(f"times must be 1-D; got shape {tuple(t.shape)}")
        n = int(t.shape[0])
        if n < 2:
            raise ValueError(
                "finite_difference_velocity requires at least two time samples "
                f"(got {n})"
            )
        if not bool(torch.all(t[1:] > t[:-1])):
            raise ValueError("times must be strictly increasing")
        if pos.shape[0] != n or pos.shape[-2:] != (_N_BODIES, _N_DIMS):
            raise ValueError(
                f"positions must have shape (T, 3, 3) with T={n} matching times; "
                f"got {tuple(pos.shape)}"
            )
        velocity = torch.empty_like(pos)
        velocity[0] = (pos[1] - pos[0]) / (t[1] - t[0])
        velocity[-1] = (pos[-1] - pos[-2]) / (t[-1] - t[-2])
        if n > 2:
            denom = (t[2:] - t[:-2]).reshape(-1, 1, 1)
            velocity[1:-1] = (pos[2:] - pos[:-2]) / denom
        return velocity


# ---------------------------------------------------------------------------
# Matched-Plummer Hamiltonian (float64 CPU, eps_inv=1e-10).
# ---------------------------------------------------------------------------


def matched_plummer_hamiltonian_series(
    positions, velocities, masses, *, eps_inv: float = EPS_INV
) -> torch.Tensor:
    """Per-snapshot ``H(t) = T(t) + V(t)`` on detached CPU float64 tensors.

    ``T = 0.5 * sum_i m_i * ||v_i||^2``; ``V = -sum_{i<j} m_i*m_j / r_safe_ij``
    with the Plummer potential-only softening ``r_safe = sqrt(||r_i-r_j||^2 +
    eps_inv^2)`` (``ctl_instruction.md`` §2.4.5 clause 5 / Step-3 item 1) — the
    SAME matched-Plummer pair form throughout (PHYS-03: never mix an additive
    softening with a squared-norm one).

    Args:
        positions: ``(T, 3, 3)`` positions (body, coord).
        velocities: ``(T, 3, 3)`` velocities, same shape as ``positions``.
        masses: the 3 ordered RAW masses, shape ``(3,)``.
        eps_inv: the Plummer softening (default ``EPS_INV = 1e-10``; NEVER the
            training-time ``pinn.constants.EPS_SOFT = 1e-5``).

    Returns:
        ``(T,)`` Hamiltonian series on a detached CPU float64 tensor.
    """
    with torch.no_grad():
        pos = _as_cpu_f64(positions)
        vel = _as_cpu_f64(velocities)
        m = _as_cpu_f64(masses).reshape(_N_BODIES)
        if pos.shape[-2:] != (_N_BODIES, _N_DIMS) or vel.shape != pos.shape:
            raise ValueError(
                "positions/velocities must both be (T, 3, 3) with matching "
                f"shapes; got positions={tuple(pos.shape)} "
                f"velocities={tuple(vel.shape)}"
            )

        speed_sq = (vel ** 2).sum(dim=-1)  # (T, 3): ||v_i||^2 per body
        kinetic = 0.5 * (m.reshape(1, _N_BODIES) * speed_sq).sum(dim=-1)  # (T,)

        eps_sq = float(eps_inv) ** 2
        potential = torch.zeros(pos.shape[0], dtype=torch.float64)
        for i, j in _PAIRS:
            r_ij = pos[:, i, :] - pos[:, j, :]
            r_safe = torch.sqrt((r_ij ** 2).sum(dim=-1) + eps_sq)
            potential = potential - m[i] * m[j] / r_safe

        return kinetic + potential


# ---------------------------------------------------------------------------
# Per-trajectory eps_H + worst-trajectory aggregation + SCS + verdict.
# ---------------------------------------------------------------------------


def trajectory_eps_h(hamiltonian_series) -> float:
    """``eps_H = max_t |(H(t) - H(0)) / H(0)|`` for one trajectory.

    A non-finite or exactly-zero ``H(0)`` (denominator) and any non-finite
    ``H(t)`` both yield an honest non-finite ``eps_H`` (never a silently
    dropped or fabricated number) — ``gate_verdict``/``aggregate_test_eps_h``
    then FAIL on it rather than this function raising.
    """
    h = _as_cpu_f64(hamiltonian_series)
    if h.dim() != 1 or h.shape[0] < 1:
        raise ValueError(
            f"hamiltonian_series must be a 1-D tensor with >= 1 entry; got "
            f"shape {tuple(h.shape)}"
        )
    h0 = h[0]
    if not bool(torch.isfinite(h0)) or float(h0) == 0.0:
        return float("nan")
    drift = torch.abs((h - h0) / h0)
    if not bool(torch.isfinite(drift).all()):
        return float("inf") if bool(torch.isinf(drift).any()) else float("nan")
    return float(torch.max(drift))


@dataclass(frozen=True)
class TrajectoryGateMetrics:
    """One trajectory's gate evidence: the full Hamiltonian series + eps_H."""

    hamiltonian_series: torch.Tensor
    eps_h: float


def compute_trajectory_gate_metrics(
    positions, times, masses, *, eps_inv: float = EPS_INV
) -> TrajectoryGateMetrics:
    """Finite-difference velocity -> matched-Plummer H(t) -> eps_H, for ONE
    trajectory. Pure composition of the functions above; no additional logic."""
    velocity = finite_difference_velocity(positions, times)
    h_series = matched_plummer_hamiltonian_series(
        positions, velocity, masses, eps_inv=eps_inv
    )
    return TrajectoryGateMetrics(
        hamiltonian_series=h_series, eps_h=trajectory_eps_h(h_series)
    )


def aggregate_test_eps_h(per_trajectory_eps_h: Sequence[float]) -> float:
    """Worst-trajectory (maximum) aggregate over a test set's eps_H values.

    Any non-finite per-trajectory ``eps_H`` makes the aggregate non-finite
    (``nan``) — the aggregate is never silently computed from only the finite
    subset (SPEC prohibition: no fabricated / dropped nonfinite metric).
    """
    values = [float(v) for v in per_trajectory_eps_h]
    if not values:
        raise ValueError(
            "aggregate_test_eps_h requires at least one trajectory's eps_H"
        )
    if not all(math.isfinite(v) for v in values):
        return float("nan")
    return max(values)


def scs_from_eps_h(eps_h: float) -> float:
    """``SCS = log10(eps_H)``, derived ONLY from the (already aggregated)
    eps_H — never recomputed or averaged independently."""
    v = float(eps_h)
    if not math.isfinite(v) or v < 0.0:
        return float("nan")
    if v == 0.0:
        return float("-inf")
    return math.log10(v)


def gate_verdict(eps_h: float) -> str:
    """The single source of truth for PASS/FAIL.

    FAIL for a non-finite ``eps_h``; FAIL for ``eps_h > 1e-5`` (equivalently
    ``SCS > -5``, since ``SCS = log10(eps_h)`` is monotone); PASS otherwise,
    INCLUDING the exact boundary ``eps_h == 1e-5`` (strict-inequality reject —
    SPEC edge R3 / prohibition 1). Deliberately the ONLY verdict function (no
    parallel SCS-based check) so the gate is never rendered as two
    independently-driftable booleans.
    """
    v = float(eps_h)
    if not math.isfinite(v):
        return "FAIL"
    if v > GATE_EPS_H_REJECT_THRESHOLD:
        return "FAIL"
    return "PASS"


@dataclass(frozen=True)
class AggregateGateMetrics:
    """The rendered test-set gate: aggregate eps_H, its SCS, and the verdict."""

    eps_h: float
    scs: float
    verdict: str


def aggregate_gate_verdict(per_trajectory_eps_h: Sequence[float]) -> AggregateGateMetrics:
    """Worst-trajectory aggregation -> SCS -> verdict, in one composed call."""
    agg_eps_h = aggregate_test_eps_h(per_trajectory_eps_h)
    return AggregateGateMetrics(
        eps_h=agg_eps_h,
        scs=scs_from_eps_h(agg_eps_h),
        verdict=gate_verdict(agg_eps_h),
    )
