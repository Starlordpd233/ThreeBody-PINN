"""Phase 59 (FEAS-07; D-16): the nearest-neighbour copy.

A validation system is predicted with the Brutus trajectory of the
Euclidean-nearest Stage-0 training system in production-normalized IC13. The
copy is slot-wise in canonical order, which is what a network trained on the
neighbour would output; scoring uses the query's inner pair. The copy's
``eps_H`` uses the neighbour's own masses and Brutus velocities (assumption
A9). No validation system may be its own neighbour.
"""

from __future__ import annotations

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.physics_residual import softened_acceleration


_GRID_TOLERANCE = 1e-9
_COPY_EPS_SOFT = 1e-12


def nearest_training_neighbour(query_key, query_ic13, candidates):
    """The candidate nearest to ``query_ic13`` as ``(RecordKey, distance)``.

    ``candidates`` is a sequence of ``(RecordKey, normalized IC13)``. Ties go to
    the lower key. An empty pool, or a pool that holds the query key, raises
    ``ValueError``.
    """
    if not candidates:
        raise ValueError("the candidate pool is empty")
    query = np.asarray(query_ic13, dtype=np.float64).reshape(13)
    best = None
    for key, vector in candidates:
        if key == query_key:
            raise ValueError(f"query {key} is among the candidates")
        distance = float(np.linalg.norm(np.asarray(vector, dtype=np.float64).reshape(13) - query))
        if best is None or (distance, key) < best:
            best = (distance, key)
    return best[1], best[0]


def _clipped(reference, t_max):
    times = np.asarray(reference.times, dtype=np.float64).reshape(-1)
    keep = times <= float(t_max) + _GRID_TOLERANCE
    return (
        times[keep],
        np.asarray(reference.positions, dtype=np.float64)[keep],
        np.asarray(reference.velocities, dtype=np.float64)[keep],
    )


def copy_prediction(query_gold_reference, neighbour_gold_reference, *, t_max=T_CHARACTERISTIC_TIME):
    """The neighbour's positions, velocities and masses on the query's grid.

    Both grids are clipped to ``t <= t_max`` and must agree within 1e-9;
    otherwise ``ValueError``. Returns ``(positions, velocities, masses, times)``
    with the query's times.
    """
    query_times, _query_positions, _query_velocities = _clipped(query_gold_reference, t_max)
    times, positions, velocities = _clipped(neighbour_gold_reference, t_max)
    if times.shape != query_times.shape:
        raise ValueError(
            f"grids differ in length: query {query_times.size}, neighbour {times.size}"
        )
    gap = float(np.max(np.abs(times - query_times), initial=0.0))
    if gap > _GRID_TOLERANCE:
        raise ValueError(f"grids differ by {gap!r}")
    masses = np.asarray(neighbour_gold_reference.masses, dtype=np.float64).reshape(3)
    return positions, velocities, masses, query_times


def copy_accelerations(neighbour_gold_reference, *, t_max=T_CHARACTERISTIC_TIME):
    """Newtonian acceleration of the copied Brutus trajectory (eps_soft 1e-12, CPU float64)."""
    _times, positions, _velocities = _clipped(neighbour_gold_reference, t_max)
    masses = np.asarray(neighbour_gold_reference.masses, dtype=np.float64).reshape(3)
    acceleration = softened_acceleration(
        positions, masses, eps_soft=_COPY_EPS_SOFT,
        dtype=torch.float64, device=torch.device("cpu"),
    )
    return acceleration.numpy()


__all__ = [
    "copy_accelerations",
    "copy_prediction",
    "nearest_training_neighbour",
]
