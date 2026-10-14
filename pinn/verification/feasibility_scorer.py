"""Phase 59 (FEAS-01): the feasibility scorer.

The module is read-only. It writes nothing, constructs no optimizer, and
keeps no module-level mutable state. The only file it opens is the governed
R_ref artifact, read through ``load_frozen_r_ref_artifact``. Imports are
limited to the standard library, numpy, torch, and ``pinn.*`` (D-37).
Tier-defining ``eps_H`` uses the gate's own Hamiltonian and
``trajectory_eps_h`` on caller-supplied velocities.
``finite_difference_context`` is refused as a tier source (D-30). The
finite-difference value and the R_ref-normalized physics residual are
labelled context columns and are not arguments of ``tier_of``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Mapping

import numpy as np
import torch

from pinn.constants import EPS_SOFT, T_CHARACTERISTIC_TIME
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.training.config import R_REF_ARTIFACT_RELATIVE_PATH, load_frozen_r_ref_artifact
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
    "network_trajectory",
    "score_network",
    "fd_context_eps_h",
    "physics_residual_context",
    "load_governed_r_ref",
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


def _json_optional(value):
    if value is None:
        return None
    return _json_number(value)


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

    ``physics_residual_mean`` and ``physics_residual_max`` are labelled
    context only. ``tier_of`` and ``score_trajectory`` never read them.
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
    physics_residual_mean: float | None = None
    physics_residual_max: float | None = None

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
            "physics_residual_mean": _json_optional(self.physics_residual_mean),
            "physics_residual_max": _json_optional(self.physics_residual_max),
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


def load_governed_r_ref() -> float:
    """Read the governed Stage-0 ``R_ref``. One read, no rewrite."""
    root = Path(__file__).resolve().parents[2]
    return float(load_frozen_r_ref_artifact(root / R_REF_ARTIFACT_RELATIVE_PATH))


def physics_residual_context(positions, accelerations, masses, *, r_ref) -> dict:
    """Mean and max of the trainer's body-averaged squared residual over ``r_ref``.

    The force is ``softened_acceleration`` with ``EPS_SOFT`` and the scored
    system's ordered masses, in the same frame as ``positions``. Context only.
    """
    pos = np.asarray(positions, dtype=np.float64)
    acc = torch.as_tensor(accelerations, dtype=torch.float64, device=torch.device("cpu"))
    mass = np.asarray(masses, dtype=np.float64).reshape(-1)
    force = softened_acceleration(
        pos,
        mass,
        eps_soft=EPS_SOFT,
        dtype=torch.float64,
        device=torch.device("cpu"),
    )
    residual = acc - force
    rbar = (residual**2).sum(dim=(-2, -1)) / 3.0
    normalized = rbar / float(r_ref)
    return {"mean": float(normalized.mean()), "max": float(normalized.max())}


def _trainer_closure(model, ic13, masses, *, dtype, device):
    ic13_t = torch.as_tensor(np.asarray(ic13, dtype=np.float64), dtype=dtype, device=device)
    masses_t = torch.as_tensor(np.asarray(masses, dtype=np.float64), dtype=dtype, device=device)
    ic13_t = ic13_t.reshape(-1)
    masses_t = masses_t.reshape(-1)
    if ic13_t.shape != (13,):
        raise ScoringInputError(f"ic13 must have shape (13,); got {tuple(ic13_t.shape)}")
    if masses_t.shape != (3,):
        raise ScoringInputError(f"masses must have shape (3,); got {tuple(masses_t.shape)}")

    def traj(u_scalar):
        tau = (2.0 * u_scalar - 1.0).reshape(1)
        tau_ic13 = torch.cat([tau, ic13_t], dim=0).unsqueeze(0)
        pos = model(tau_ic13, masses_t.unsqueeze(0))
        return pos.reshape(3, 3)

    def flat_traj(u_scalar):
        return traj(u_scalar).reshape(-1)

    return traj, flat_traj


def network_trajectory(
    model,
    ic13,
    masses,
    times,
    *,
    dtype,
    device,
    microbatch_size=256,
    want_acceleration=False,
):
    """Positions and autograd ``dr'/du`` on the trainer's trajectory closure.

    ``u = t / T``. Each chunk is at most ``microbatch_size`` times. Velocities
    are ``vmap(jacrev)`` of the flattened closure, not a summed-output VJP.
    Accelerations, when requested, are ``componentwise_du``'s second derivative.
    The prior ``model.training`` mode is restored. No backward call is made.
    """
    if isinstance(microbatch_size, bool) or not isinstance(microbatch_size, int) or microbatch_size < 1:
        raise ScoringInputError("microbatch_size must be a positive int")
    time_array = np.asarray(times, dtype=np.float64).reshape(-1)
    if time_array.shape[0] < 2:
        raise ScoringInputError(
            f"times must cover at least two scoring times; got {time_array.shape[0]}"
        )
    u_all = time_array / float(T_CHARACTERISTIC_TIME)
    traj, flat_traj = _trainer_closure(model, ic13, masses, dtype=dtype, device=device)
    prior_training = bool(model.training)
    position_chunks = []
    velocity_chunks = []
    acceleration_chunks = []
    try:
        model.eval()
        for start in range(0, int(u_all.shape[0]), microbatch_size):
            u_chunk = torch.as_tensor(
                u_all[start : start + microbatch_size], dtype=dtype, device=device
            )
            positions = torch.func.vmap(flat_traj)(u_chunk)
            velocities = torch.func.vmap(torch.func.jacrev(flat_traj))(u_chunk)
            position_chunks.append(
                positions.detach().to(device="cpu", dtype=torch.float64).numpy().reshape(-1, 3, 3)
            )
            velocity_chunks.append(
                velocities.detach().to(device="cpu", dtype=torch.float64).numpy().reshape(-1, 3, 3)
            )
            if want_acceleration:
                _first, second = componentwise_du(traj, u_chunk)
                acceleration_chunks.append(
                    second.detach().to(device="cpu", dtype=torch.float64).numpy().reshape(-1, 3, 3)
                )
    finally:
        if prior_training:
            model.train()
        else:
            model.eval()
    positions_out = np.concatenate(position_chunks, axis=0)
    velocities_out = np.concatenate(velocity_chunks, axis=0)
    if want_acceleration:
        return positions_out, velocities_out, np.concatenate(acceleration_chunks, axis=0)
    return positions_out, velocities_out


def score_network(
    model,
    ic13,
    masses,
    ref_positions,
    inner_pair,
    times,
    *,
    scorecard,
    dtype,
    device,
    grid,
    microbatch_size=256,
):
    """Score a network with autograd velocities and the residual context column."""
    positions, velocities, accelerations = network_trajectory(
        model,
        ic13,
        masses,
        times,
        dtype=dtype,
        device=device,
        microbatch_size=microbatch_size,
        want_acceleration=True,
    )
    result = score_trajectory(
        positions,
        velocities,
        ref_positions,
        masses,
        inner_pair,
        times,
        velocity_source="autograd",
        scorecard=scorecard,
        grid=grid,
    )
    context = physics_residual_context(
        positions, accelerations, masses, r_ref=load_governed_r_ref()
    )
    return replace(
        result,
        physics_residual_mean=context["mean"],
        physics_residual_max=context["max"],
    )


def fd_context_eps_h(positions, times_u, masses) -> float:
    """Finite-difference ``eps_H`` labelled ``finite_difference_context``.

    Continuity with generation 7 only. Never tier-defining. GAP-59-08 owns
    the production-evaluator question and is not fixed here.
    """
    velocity = gate_metrics.finite_difference_velocity(positions, times_u)
    series = gate_metrics.matched_plummer_hamiltonian_series(positions, velocity, masses)
    return float(gate_metrics.trajectory_eps_h(series))
