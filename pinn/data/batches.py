"""DATA-05 replay/lookahead selection and fixed two-point-set batches.

The public ``source`` seam is the memory-only StageQuery produced by DATA-04.
Phase 40 supplies ``StageIndex.from_split(adapter, manifest, "train")`` so no
validation/test key can enter a training batch.  This module owns neither epoch
iteration nor Phase-40 adaptive/residual-aware collocation density.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.types import (
    DataFidelityPoints,
    FixedBatch,
    PhysicsCollocationPoints,
    RecordKey,
    StageZeroUnderpopulated,
)


class SelectedStageRecords(NamedTuple):
    """Explicit replay/lookahead identity sets selected for one fixed batch."""

    replay: tuple[RecordKey, ...]
    lookahead: tuple[RecordKey, ...]


def _require_local_rng(rng) -> np.random.Generator:
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be a caller-owned numpy.random.Generator")
    return rng


def _is_blacklisted(source, key: RecordKey) -> bool:
    blacklisted = getattr(source, "blacklisted_physical_keys", frozenset())
    if key.physical_key in blacklisted:
        return True
    predicate = getattr(source, "is_blacklisted", None)
    return bool(callable(predicate) and predicate(key.physical_key))


def _validate_numeric_pool(source, keys, *, pool_name: str) -> tuple[RecordKey, ...]:
    validated = tuple(sorted(keys))
    for key in validated:
        if not isinstance(key, RecordKey):
            raise TypeError(f"{pool_name} member must be RecordKey; got {key!r}")
        if (key.variant, key.fidelity) != ("hierarchical", "base"):
            raise ValueError(
                f"{pool_name} contains non-original/base hierarchical Set 1a key {key!r}"
            )
        if _is_blacklisted(source, key):
            raise ValueError(f"{pool_name} contains blacklisted physical key {key.physical_key!r}")
    return validated


def _sample_keys(pool, *, count: int, replace: bool, rng) -> tuple[RecordKey, ...]:
    indices = rng.choice(len(pool), size=count, replace=replace)
    return tuple(sorted(pool[int(index)] for index in np.atleast_1d(indices)))


def select_stage_records(
    source,
    *,
    stage: int,
    rng: np.random.Generator,
    replay_count: int = 240,
    lookahead_count: int = 16,
) -> SelectedStageRecords:
    """Select cumulative replay and adjacent-stage lookahead identities.

    Replay is sampled without replacement from ``D<=stage``.  The adjacent
    pool is absent when ``has_stage(stage + 1)`` is false; a nonempty pool below
    ``lookahead_count`` is padded with replacement, while a large enough pool is
    sampled without replacement.  Every candidate is validated before RNG use
    so a blacklisted/gold/non-Set-1a injection cannot hide outside the draw.
    """
    rng = _require_local_rng(rng)
    if isinstance(stage, bool) or not isinstance(stage, int) or stage < 0:
        raise TypeError(f"stage must be a non-negative int; got {stage!r}")
    if replay_count <= 0 or lookahead_count < 0:
        raise ValueError("replay_count must be positive and lookahead_count non-negative")
    if getattr(source, "gold_numeric_stage_count", None) != 0:
        raise ValueError("gold_numeric_stage_count must be exactly 0 before selection")

    replay_pool = _validate_numeric_pool(
        source, source.records_at_or_below(stage), pool_name="replay pool"
    )
    if len(replay_pool) < replay_count:
        raise StageZeroUnderpopulated(len(replay_pool), replay_count)
    replay = _sample_keys(replay_pool, count=replay_count, replace=False, rng=rng)

    next_stage = stage + 1
    if not source.has_stage(next_stage):
        lookahead = ()
    else:
        lookahead_pool = _validate_numeric_pool(
            source, source.records_at(next_stage), pool_name="lookahead pool"
        )
        if not lookahead_pool:
            raise ValueError(
                f"source reports has_stage({next_stage}) but records_at is empty"
            )
        lookahead = _sample_keys(
            lookahead_pool,
            count=lookahead_count,
            replace=len(lookahead_pool) < lookahead_count,
            rng=rng,
        )

    _validate_numeric_pool(source, replay, pool_name="selected replay")
    _validate_numeric_pool(source, lookahead, pool_name="selected lookahead")
    return SelectedStageRecords(replay=replay, lookahead=lookahead)


# Frozen Wave-0 name retained as an identity alias; there is one selector.
select_batch_trajectories = select_stage_records


def allocate_collocation_quota(
    identity_count: int,
    collocation_count: int,
    rng: np.random.Generator,
) -> tuple[int, ...]:
    """Allocate exact GAP-39-12 Option-C near-even identity quotas."""
    rng = _require_local_rng(rng)
    if isinstance(identity_count, bool) or not isinstance(identity_count, int):
        raise TypeError("identity_count must be an int")
    if identity_count <= 0:
        raise ValueError("identity_count must be positive")
    if isinstance(collocation_count, bool) or not isinstance(collocation_count, int):
        raise TypeError("collocation_count must be an int")
    if collocation_count < 0:
        raise ValueError("collocation_count must be non-negative")

    quotient, remainder = divmod(collocation_count, identity_count)
    counts = np.full(identity_count, quotient, dtype=np.int64)
    if remainder:
        recipients = rng.permutation(identity_count)[:remainder]
        counts[recipients] += 1
    result = tuple(int(value) for value in counts)
    assert sum(result) == collocation_count
    assert set(result).issubset({quotient, quotient + 1})
    assert sum(value == quotient + 1 for value in result) == remainder
    assert max(result) - min(result) <= 1
    return result


def _to_numpy(value, *, name: str) -> np.ndarray:
    if isinstance(value, torch.Tensor):
        value = value.detach().cpu().numpy()
    array = np.asarray(value)
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be finite")
    return array


def _source_record(source, key: RecordKey):
    get = getattr(source, "get", None)
    if not callable(get):
        raise TypeError("StageQuery source must expose get(key)")
    return get(key)


def _source_snapshot(source, accessor: str, key: RecordKey) -> np.ndarray:
    value = getattr(source, accessor, None)
    if not callable(value):
        raise TypeError(f"StageQuery source must expose {accessor}(key)")
    return _to_numpy(value(key), name=accessor)


def _acceleration_weights(source, key: RecordKey, times: np.ndarray) -> np.ndarray:
    direct = getattr(source, "acceleration_magnitudes", None)
    if callable(direct):
        weights = _to_numpy(direct(key), name="acceleration_magnitudes")
    else:
        velocities = _source_snapshot(source, "snapshot_velocities", key)
        if velocities.shape[0] != times.shape[0]:
            raise ValueError("snapshot velocity/time cardinality mismatch")
        edge_order = 2 if times.shape[0] >= 3 else 1
        acceleration = np.gradient(velocities, times, axis=0, edge_order=edge_order)
        weights = np.linalg.norm(acceleration.reshape(times.shape[0], -1), axis=1)
    weights = np.asarray(weights, dtype=np.float64).reshape(-1)
    if weights.shape != times.shape:
        raise ValueError("acceleration weights must have one value per snapshot")
    if np.any(weights < 0.0):
        raise ValueError("acceleration weights must be non-negative")
    return weights


def _gumbel_top_k(weights: np.ndarray, count: int, rng) -> np.ndarray:
    if count == 0:
        return np.empty(0, dtype=np.int64)
    safe = np.maximum(weights, np.finfo(np.float64).tiny)
    scores = np.log(safe) + rng.gumbel(size=len(safe))
    chosen = np.argpartition(scores, -count)[-count:]
    order = np.lexsort((chosen, -scores[chosen]))
    return chosen[order].astype(np.int64, copy=False)


def _torch_tensor(value, *, dtype, device):
    return torch.as_tensor(value, dtype=dtype, device=device)


def sample_data_points(
    source,
    record_keys,
    *,
    rng: np.random.Generator,
    dtype,
    device,
    n_pts_cap: int = 32,
) -> DataFidelityPoints:
    """Sample observed snapshots with the CTL 50/50 Gumbel/uniform rule."""
    rng = _require_local_rng(rng)
    if getattr(source, "gold_numeric_stage_count", None) != 0:
        raise ValueError("gold_numeric_stage_count must be exactly 0 before assembly")
    if isinstance(n_pts_cap, bool) or not isinstance(n_pts_cap, int) or n_pts_cap <= 0:
        raise ValueError("n_pts_cap must be a positive int")
    keys = _validate_numeric_pool(source, record_keys, pool_name="data point identities")
    if not keys:
        raise ValueError("data point sampling requires at least one identity")

    sampled_times: list[float] = []
    sampled_ic13: list[np.ndarray] = []
    sampled_masses: list[np.ndarray] = []
    sampled_targets: list[np.ndarray] = []
    provenance_keys: list[RecordKey] = []
    snapshot_indices: list[int] = []
    sampling_kinds: list[str] = []

    for key in keys:
        _validate_numeric_pool(source, (key,), pool_name="data point identity")
        record = _source_record(source, key)
        times = _source_snapshot(source, "snapshot_times", key).astype(np.float64, copy=False)
        positions = _source_snapshot(source, "snapshot_positions", key)
        if times.ndim != 1 or positions.shape != (len(times), 3, 3):
            raise ValueError("snapshot times/positions must have shapes (N,) and (N,3,3)")
        declared_n = int(source.n_snapshots(key))
        if declared_n != len(times) or int(record.n_snapshots) != len(times):
            raise ValueError("declared and resident snapshot counts disagree")
        n_pts = min(n_pts_cap, len(times))
        weighted_count = n_pts // 2
        weights = _acceleration_weights(source, key, times)
        weighted = _gumbel_top_k(weights, weighted_count, rng)
        remaining = np.setdiff1d(np.arange(len(times)), weighted, assume_unique=True)
        uniform_count = n_pts - weighted_count
        uniform = np.atleast_1d(
            rng.choice(remaining, size=uniform_count, replace=False)
        ).astype(np.int64, copy=False)

        record_ic13 = _to_numpy(record.ic13, name="ic13").reshape(13)
        record_masses = _to_numpy(record.masses, name="masses").reshape(3)
        for index, kind in (
            *((int(value), "acceleration") for value in weighted),
            *((int(value), "uniform") for value in uniform),
        ):
            sampled_times.append(float(times[index]))
            sampled_ic13.append(record_ic13)
            sampled_masses.append(record_masses)
            sampled_targets.append(positions[index].reshape(9))
            provenance_keys.append(key)
            snapshot_indices.append(index)
            sampling_kinds.append(kind)

    times_tensor = _torch_tensor(sampled_times, dtype=dtype, device=device)
    tau = 2.0 * (times_tensor / T_CHARACTERISTIC_TIME) - 1.0
    ic13_tensor = _torch_tensor(np.stack(sampled_ic13), dtype=dtype, device=device)
    tau_ic13 = torch.cat((tau.reshape(-1, 1), ic13_tensor), dim=1)
    masses = _torch_tensor(np.stack(sampled_masses), dtype=dtype, device=device)
    targets = _torch_tensor(np.stack(sampled_targets), dtype=dtype, device=device)
    if tau_ic13.shape != (len(provenance_keys), 14) or masses.shape[1:] != (3,):
        raise AssertionError("model-facing data point shapes are not (N,14)/(N,3)")
    return DataFidelityPoints(
        tau_ic13=tau_ic13,
        masses=masses,
        targets=targets,
        times=times_tensor,
        record_keys=tuple(provenance_keys),
        snapshot_indices=tuple(snapshot_indices),
        sampling_kinds=tuple(sampling_kinds),
    )


def sample_collocation_points(
    source,
    record_keys,
    *,
    rng: np.random.Generator,
    dtype,
    device,
    collocation_count: int = 4096,
) -> PhysicsCollocationPoints:
    """Draw global-[0,10] physics points under balanced identity quotas."""
    rng = _require_local_rng(rng)
    if collocation_count <= 0:
        raise ValueError("collocation_count must be positive")
    identities = tuple(sorted(set(record_keys)))
    identities = _validate_numeric_pool(
        source, identities, pool_name="collocation identities"
    )
    quotas = allocate_collocation_quota(len(identities), collocation_count, rng)

    assigned: list[tuple[RecordKey, float]] = []
    for key, count in zip(identities, quotas):
        for value in rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=count):
            assigned.append((key, float(value)))
    assigned.sort(key=lambda item: (item[0], item[1]))
    if len(assigned) != collocation_count:
        raise AssertionError("collocation allocation did not preserve total cardinality")

    times = _torch_tensor([item[1] for item in assigned], dtype=dtype, device=device)
    ic13_rows = []
    mass_rows = []
    keys = []
    for key, _time in assigned:
        _validate_numeric_pool(source, (key,), pool_name="emitted collocation identity")
        record = _source_record(source, key)
        ic13_rows.append(_to_numpy(record.ic13, name="ic13").reshape(13))
        mass_rows.append(_to_numpy(record.masses, name="masses").reshape(3))
        keys.append(key)
    tau = 2.0 * (times / T_CHARACTERISTIC_TIME) - 1.0
    ic13 = _torch_tensor(np.stack(ic13_rows), dtype=dtype, device=device)
    tau_ic13 = torch.cat((tau.reshape(-1, 1), ic13), dim=1)
    masses = _torch_tensor(np.stack(mass_rows), dtype=dtype, device=device)
    return PhysicsCollocationPoints(
        times=times,
        tau_ic13=tau_ic13,
        masses=masses,
        record_keys=tuple(keys),
    )


def build_stage_batch(
    source,
    *,
    stage: int,
    rng: np.random.Generator,
    dtype,
    device,
    collocation_count: int = 4096,
) -> FixedBatch:
    """Build one DATA-05 fixed batch without owning epochs or adaptive density."""
    selected = select_stage_records(source, stage=stage, rng=rng)
    selected_keys = selected.replay + selected.lookahead
    data_points = sample_data_points(
        source, selected_keys, rng=rng, dtype=dtype, device=device
    )
    collocation_points = sample_collocation_points(
        source,
        selected_keys,
        rng=rng,
        dtype=dtype,
        device=device,
        collocation_count=collocation_count,
    )
    _validate_numeric_pool(
        source, data_points.record_keys, pool_name="emitted data identities"
    )
    _validate_numeric_pool(
        source, collocation_points.record_keys, pool_name="emitted collocation identities"
    )
    return FixedBatch(
        data_points=data_points,
        collocation_points=collocation_points,
        replay_keys=selected.replay,
        lookahead_keys=selected.lookahead,
    )


__all__ = [
    "SelectedStageRecords",
    "allocate_collocation_quota",
    "build_stage_batch",
    "sample_collocation_points",
    "sample_data_points",
    "select_stage_records",
]
