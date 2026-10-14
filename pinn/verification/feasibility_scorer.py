"""Phase 59 (FEAS-01): the feasibility scorer.

The module is read-only. It opens no file, writes nothing, constructs no
optimizer, and keeps no module-level mutable state. Imports are limited to
the standard library, numpy, torch, and ``pinn.*`` (D-37). Tier-defining
``eps_H`` uses the gate's own Hamiltonian and ``trajectory_eps_h`` on caller-
supplied velocities. ``finite_difference_context`` is refused here; it is not
a tier-defining velocity source (D-30).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.training.validation_gate import json_safe_float
from pinn.verification import gate_metrics
from pinn.verification.feasibility_scorecard import tier_of

__all__ = [
    "FRAME_NAME",
    "VELOCITY_SOURCES",
    "TIER_DEFINING_SOURCES",
    "ScoringInputError",
    "ScoreResult",
    "position_errors",
    "tier_defining_error",
    "valid_horizon",
    "eps_h_from_velocities",
    "score_trajectory",
]

FRAME_NAME = "r_prime_u"
VELOCITY_SOURCES = frozenset(
    {"autograd", "analytic", "brutus", "finite_difference_context"}
)
TIER_DEFINING_SOURCES = VELOCITY_SOURCES - {"finite_difference_context"}

_CONTEXT_COLUMN_MESSAGE = (
    "finite_difference_context is a context column, never tier-defining"
)


class ScoringInputError(ValueError):
    """The arrays, inner pair, or velocity source cannot be scored."""


def _json_number(value: float):
    return json_safe_float(float(value))


def _max_with_nan(values: np.ndarray) -> float:
    """Maximum, or NaN when any entry is NaN (an Inf stays Inf)."""
    array = np.asarray(values, dtype=np.float64)
    if np.isnan(array).any():
        return float("nan")
    return float(np.max(array))


def _as_positions(value, *, what: str) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if array.ndim != 3 or array.shape[1:] != (3, 3):
        raise ScoringInputError(
            f"{what} must have shape (N_t, 3, 3); got {tuple(array.shape)}"
        )
    if array.shape[0] < 2:
        raise ScoringInputError(
            f"{what} must cover at least two scoring times; got {array.shape[0]}"
        )
    return array


def _inner_pair(inner_pair) -> tuple[int, int]:
    if isinstance(inner_pair, (str, bytes)) or not isinstance(inner_pair, (tuple, list)):
        raise ScoringInputError(
            "inner_pair must be two distinct body indices in {0, 1, 2}"
        )
    if len(inner_pair) != 2:
        raise ScoringInputError(
            "inner_pair must be two distinct body indices in {0, 1, 2}"
        )
    indices = []
    for index in inner_pair:
        if isinstance(index, bool) or not isinstance(index, (int, np.integer)):
            raise ScoringInputError(
                "inner_pair must be two distinct body indices in {0, 1, 2}"
            )
        indices.append(int(index))
    a, b = indices
    if a not in (0, 1, 2) or b not in (0, 1, 2) or a == b:
        raise ScoringInputError(
            "inner_pair must be two distinct body indices in {0, 1, 2}"
        )
    return a, b


def _as_masses(masses) -> np.ndarray:
    array = np.asarray(masses, dtype=np.float64).reshape(-1)
    if array.shape != (3,):
        raise ScoringInputError(
            f"masses must have shape (3,); got {tuple(np.asarray(masses).shape)}"
        )
    return array


def _as_times(times, n_times: int) -> np.ndarray:
    array = np.asarray(times, dtype=np.float64).reshape(-1)
    if array.shape != (n_times,):
        raise ScoringInputError(
            f"times must have shape ({n_times},); got {tuple(array.shape)}"
        )
    return array


@dataclass(frozen=True)
class ScoreResult:
    """One scored trajectory. ``h`` follows the scorecard's delta order.

    ``physics_residual_mean`` and ``physics_residual_max`` are not part of
    this core result. Plan 59-02 task 3 adds them as labelled context only.
    """

    E: float
    e_sys_max: float
    e_in_max: float
    h: tuple[tuple[float, float], ...]
    eps_h: float
    tier: int
    velocity_source: str
    grid: str
    frame: str
    n_times: int
    R_sys: float

    @property
    def h_by_delta(self) -> Mapping[float, float]:
        return {delta: value for delta, value in self.h}

    def to_json_dict(self) -> dict:
        """Plain JSON types. Non-finite floats use the ``json_safe_float`` sentinels."""
        return {
            "E": _json_number(self.E),
            "e_sys_max": _json_number(self.e_sys_max),
            "e_in_max": _json_number(self.e_in_max),
            "h": [
                [_json_number(delta), _json_number(value)] for delta, value in self.h
            ],
            "eps_h": _json_number(self.eps_h),
            "tier": int(self.tier),
            "velocity_source": self.velocity_source,
            "grid": self.grid,
            "frame": self.frame,
            "n_times": int(self.n_times),
            "R_sys": _json_number(self.R_sys),
        }


def position_errors(pred_positions, ref_positions, inner_pair):
    """Return ``(e_sys, e_in, R_sys)`` for one frame.

    ``R_sys`` is the maximum reference radius. ``e_sys(t)`` is the largest
    body error at that time divided by ``R_sys``. ``e_in(t)`` is the inner
    separation error divided by the reference separation.
    """
    pred = _as_positions(pred_positions, what="pred_positions")
    ref = _as_positions(ref_positions, what="ref_positions")
    if pred.shape != ref.shape:
        raise ScoringInputError(
            "pred_positions and ref_positions must have the same shape; "
            f"got {tuple(pred.shape)} and {tuple(ref.shape)}"
        )
    a, b = _inner_pair(inner_pair)
    radii = np.linalg.norm(ref, axis=-1)
    r_sys = float(np.max(radii))
    body_error = np.linalg.norm(pred - ref, axis=-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        e_sys = np.max(body_error, axis=-1) / r_sys
        separation = ref[:, b, :] - ref[:, a, :]
        predicted_separation = pred[:, b, :] - pred[:, a, :]
        e_in = np.linalg.norm(predicted_separation - separation, axis=-1) / np.linalg.norm(
            separation, axis=-1
        )
    return e_sys, e_in, r_sys


def tier_defining_error(e_sys, e_in) -> float:
    """``max_t max(e_sys, e_in)``. Any NaN makes the result NaN."""
    e_sys_array = np.asarray(e_sys, dtype=np.float64).reshape(-1)
    e_in_array = np.asarray(e_in, dtype=np.float64).reshape(-1)
    if e_sys_array.shape != e_in_array.shape:
        raise ScoringInputError(
            "e_sys and e_in must have the same length; "
            f"got {e_sys_array.shape[0]} and {e_in_array.shape[0]}"
        )
    return _max_with_nan(np.maximum(e_sys_array, e_in_array))


def valid_horizon(e_sys, e_in, times, *, delta, T) -> float:
    """First scoring time where ``max(e_sys, e_in) > delta``, divided by ``T``.

    Returns 1.0 when no scoring time crosses ``delta``. ``times`` are the
    reference's native output times.
    """
    e_sys_array = np.asarray(e_sys, dtype=np.float64).reshape(-1)
    e_in_array = np.asarray(e_in, dtype=np.float64).reshape(-1)
    time_array = np.asarray(times, dtype=np.float64).reshape(-1)
    if e_sys_array.shape != e_in_array.shape or time_array.shape != e_sys_array.shape:
        raise ScoringInputError(
            "e_sys, e_in, and times must share one scoring-time length"
        )
    crossed = np.flatnonzero(np.maximum(e_sys_array, e_in_array) > float(delta))
    if crossed.size == 0:
        return 1.0
    return float(time_array[int(crossed[0])] / float(T))


def eps_h_from_velocities(positions, velocities, masses) -> float:
    """``eps_H`` from explicit velocities through the gate's own Hamiltonian.

    This is the only ``eps_H`` path used for tiers. Inputs are converted to
    detached CPU float64 tensors inside ``gate_metrics``.
    """
    pos = _as_positions(positions, what="positions")
    vel = np.asarray(velocities, dtype=np.float64)
    if vel.shape != pos.shape:
        raise ScoringInputError(
            "velocities must have the same shape as positions; "
            f"got {tuple(vel.shape)} and {tuple(pos.shape)}"
        )
    mass = _as_masses(masses)
    series = gate_metrics.matched_plummer_hamiltonian_series(
        torch.as_tensor(pos, dtype=torch.float64, device=torch.device("cpu")),
        torch.as_tensor(vel, dtype=torch.float64, device=torch.device("cpu")),
        torch.as_tensor(mass, dtype=torch.float64, device=torch.device("cpu")),
    )
    return float(gate_metrics.trajectory_eps_h(series))


def score_trajectory(
    pred_positions,
    pred_velocities,
    ref_positions,
    masses,
    inner_pair,
    times,
    *,
    velocity_source,
    scorecard,
    grid,
    frame=FRAME_NAME,
    T=T_CHARACTERISTIC_TIME,
):
    """Score one trajectory and tier it through the loaded scorecard.

    ``velocity_source`` must be tier-defining. ``finite_difference_context``
    raises ``ScoringInputError``.
    """
    if velocity_source not in TIER_DEFINING_SOURCES:
        if velocity_source == "finite_difference_context":
            raise ScoringInputError(_CONTEXT_COLUMN_MESSAGE)
        raise ScoringInputError(
            f"velocity_source {velocity_source!r} is not tier-defining"
        )
    pred = _as_positions(pred_positions, what="pred_positions")
    ref = _as_positions(ref_positions, what="ref_positions")
    vel = np.asarray(pred_velocities, dtype=np.float64)
    if vel.shape != pred.shape or pred.shape != ref.shape:
        raise ScoringInputError(
            "pred_positions, pred_velocities, and ref_positions must share "
            f"shape (N_t, 3, 3); got {tuple(pred.shape)}, {tuple(vel.shape)}, "
            f"{tuple(ref.shape)}"
        )
    time_array = _as_times(times, int(pred.shape[0]))
    mass = _as_masses(masses)
    e_sys, e_in, r_sys = position_errors(pred, ref, inner_pair)
    position_error = tier_defining_error(e_sys, e_in)
    deltas = scorecard.section("metrics")["valid_horizon_deltas"]
    horizon = tuple(
        (
            float(delta),
            valid_horizon(e_sys, e_in, time_array, delta=float(delta), T=T),
        )
        for delta in deltas
    )
    eps_h = eps_h_from_velocities(pred, vel, mass)
    tier = tier_of(position_error, eps_h, scorecard=scorecard)
    return ScoreResult(
        E=float(position_error),
        e_sys_max=_max_with_nan(e_sys),
        e_in_max=_max_with_nan(e_in),
        h=horizon,
        eps_h=float(eps_h),
        tier=int(tier),
        velocity_source=str(velocity_source),
        grid=grid,
        frame=frame,
        n_times=int(pred.shape[0]),
        R_sys=float(r_sys),
    )
