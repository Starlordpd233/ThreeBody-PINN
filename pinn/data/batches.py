"""DATA-05 replay/lookahead selection and fixed two-point-set batches.

The public ``source`` seam is the memory-only StageQuery produced by DATA-04.
Phase 40 supplies ``StageIndex.from_split(adapter, manifest, "train")`` so no
validation/test key can enter a training batch.  This module owns neither epoch
iteration nor Phase-40 adaptive/residual-aware collocation density.
"""

from __future__ import annotations

from typing import NamedTuple, Sequence

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.types import (
    DataFidelityPoints,
    FixedBatch,
    PhysicsCollocationPoints,
    RecordKey,
    StageZeroUnderpopulated,
    ValidationPoolEmpty,
)

# ---------------------------------------------------------------------------
# Ratified §3.2 allocation constants (pinn_architecture.md "Phase 56 contract:
# collocation allocation and time draw amended"; 54-RULING.md "Batch
# allocation and bin policy"). Independently defined here (by content, not by
# import) rather than imported from ``pinn.verification.architecture_
# characterization_probe`` -- the data layer does not depend on verification
# tooling, and ``tests/phase57/_fixtures.py`` documents this same
# independent-re-derivation convention.
RATIFIED_N_BINS = 16
RATIFIED_PER_BIN = 256
RATIFIED_TOTAL = RATIFIED_N_BINS * RATIFIED_PER_BIN
FULL_BATCH_SLOTS = 256
REPLAY_ONLY_SLOTS = 240


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


def select_validation_records(source, *, stage: int) -> SelectedStageRecords:
    """Select the entire held-out Stage-<=k validation pool.

    The identity set is ``sorted(source.records_at_or_below(stage))`` — the
    same population ``compute_validation_gate`` already reads. There is no
    replay draw and no lookahead set: ``ctl_instruction.md`` scopes
    ``B_replay = 240`` to a training batch ("Mini-Batch Construction with
    Lookahead Sampling") and puts the ADVANCE success gate on "the held-out
    validation set". This selector takes no ``rng``, no ``replay_count``, and
    no ``lookahead_count``; the absence of those parameters is the contract.
    """
    if getattr(source, "gold_numeric_stage_count", None) != 0:
        raise ValueError("gold_numeric_stage_count must be exactly 0 before selection")
    if isinstance(stage, bool) or not isinstance(stage, int) or stage < 0:
        raise TypeError(f"stage must be a non-negative int; got {stage!r}")

    pool = _validate_numeric_pool(
        source, source.records_at_or_below(stage), pool_name="validation pool"
    )
    if not pool:
        raise ValidationPoolEmpty(stage, split="validation")
    return SelectedStageRecords(replay=pool, lookahead=())


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


def _uniform_time_in_bin(
    rng: np.random.Generator, bin_id: int, *, n_bins: int, t_max: float,
) -> float:
    """One §3.2 fixed-bin uniform draw.

    Bins ``0 .. n_bins - 2`` are half-open on the upper edge
    (``[lo, hi)`` via ``numpy``'s own ``[low, high)`` convention); bin
    ``n_bins - 1`` is CLOSED on both ends, admitted via the same
    ``nextafter``-then-clip construction ``stratified_collocation_times``
    (Phase 55) already uses for the identical bin-edge contract.
    """
    lo = (bin_id / n_bins) * t_max
    if bin_id < n_bins - 1:
        hi = ((bin_id + 1) / n_bins) * t_max
        return float(rng.uniform(lo, hi))
    if lo >= t_max:
        return float(t_max)
    return float(min(rng.uniform(lo, np.nextafter(t_max, np.inf)), t_max))


def _stratified_full_slot_rows(
    record_keys: Sequence[RecordKey],
    *,
    rng: np.random.Generator,
    n_bins: int = RATIFIED_N_BINS,
    t_max: float = T_CHARACTERISTIC_TIME,
) -> list[tuple[RecordKey, float]]:
    """54-RULING.md 256-slot rule: one row per selected slot inside every bin.

    Iterates ``record_keys`` BY POSITION (not by unique value) so a repeated
    key occupying two distinct slots is treated as two independent slots,
    preserving replacement/duplicate multiplicity exactly as the input
    selection produced it.
    """
    rows: list[tuple[RecordKey, float]] = []
    for bin_id in range(n_bins):
        for key in record_keys:
            rows.append((key, _uniform_time_in_bin(rng, bin_id, n_bins=n_bins, t_max=t_max)))
    return rows


def _stratified_replay_only_rows(
    record_keys: Sequence[RecordKey],
    *,
    rng: np.random.Generator,
    n_bins: int = RATIFIED_N_BINS,
    t_max: float = T_CHARACTERISTIC_TIME,
) -> list[tuple[RecordKey, float]]:
    """54-RULING.md replay-only rule: the 3840-plus-256-remainder construction.

    Pass one is :func:`_stratified_full_slot_rows` (one row per slot per bin).
    Pass two draws ONE canonical seeded permutation of the slot POSITIONS;
    bins ``0 .. n_bins - 2`` each take the next disjoint slice of that
    permutation (sized so the slices exactly partition every slot), and the
    last bin reuses the FIRST slice -- giving every slot exactly one extra
    row, and the first slice's slots a second extra row (the ratified
    17-rows / 18-rows split for the 240-slot shape).
    """
    n_slots = len(record_keys)
    rows = _stratified_full_slot_rows(record_keys, rng=rng, n_bins=n_bins, t_max=t_max)

    slice_size, remainder = divmod(n_slots, n_bins - 1)
    if remainder != 0:
        raise ValueError(
            f"sample_collocation_points: {n_slots} replay-only slots do not "
            f"evenly divide into {n_bins - 1} canonical-permutation slices; "
            f"the ratified replay-only construction requires an exact division"
        )
    permutation = rng.permutation(n_slots)
    for bin_id in range(n_bins - 1):
        recipients = permutation[bin_id * slice_size : (bin_id + 1) * slice_size]
        for slot_index in recipients:
            key = record_keys[int(slot_index)]
            rows.append((key, _uniform_time_in_bin(rng, bin_id, n_bins=n_bins, t_max=t_max)))
    last_bin = n_bins - 1
    for slot_index in permutation[:slice_size]:
        key = record_keys[int(slot_index)]
        rows.append((key, _uniform_time_in_bin(rng, last_bin, n_bins=n_bins, t_max=t_max)))
    return rows


def sample_collocation_points(
    source,
    record_keys,
    *,
    rng: np.random.Generator,
    dtype,
    device,
    collocation_count: int = RATIFIED_TOTAL,
) -> PhysicsCollocationPoints:
    """Draw physics collocation points for one fixed batch.

    At the ratified total (``collocation_count == RATIFIED_TOTAL == 4096``)
    this implements the exact §3.2 stratified allocation
    (``pinn_architecture.md`` "Phase 56 contract: collocation allocation and
    time draw amended"; 54-RULING.md "Batch allocation and bin policy"): a
    256-slot batch emits one row per selected slot inside every one of the 16
    fixed equal-``u`` bins, and a 240-slot replay-only batch uses the
    canonical seeded 3840-plus-256-remainder construction. A slot count that
    is neither 256 nor 240 at the ratified total has no defined stratified
    construction and is a fail-closed refusal -- never a silently
    non-stratified fallback (a resource failure at the ratified count is not
    permission to reduce it).

    For any OTHER ``collocation_count`` (a non-ratified, ad-hoc request --
    e.g. a small anchor-only physics draw predating this amendment), the
    legacy near-even per-slot-quota draw is preserved byte-for-byte: the
    canonical identities are the sorted selected-slot multiset, and
    ``allocate_collocation_quota`` divides ``collocation_count`` over the
    ``M = len(record_keys)`` selected slots (one quota per slot). A RecordKey
    that occupies ``k`` selected slots therefore accumulates ``k`` per-slot
    quotas of collocation rows, preserving the replacement-padded
    replay/lookahead weighting through the two-point-set batch.
    """
    rng = _require_local_rng(rng)
    if collocation_count <= 0:
        raise ValueError("collocation_count must be positive")

    # Every selected slot's key is validated up front, before any draw --
    # unchanged defense-in-depth regardless of which allocation path runs.
    for key in record_keys:
        if not isinstance(key, RecordKey):
            raise TypeError(f"collocation member must be RecordKey; got {key!r}")
        if (key.variant, key.fidelity) != ("hierarchical", "base"):
            raise ValueError(
                f"collocation contains non-original/base hierarchical Set 1a key {key!r}"
            )
        if _is_blacklisted(source, key):
            raise ValueError(f"collocation contains blacklisted physical key {key.physical_key!r}")

    if collocation_count == RATIFIED_TOTAL:
        n_slots = len(record_keys)
        if n_slots == FULL_BATCH_SLOTS:
            assigned = _stratified_full_slot_rows(record_keys, rng=rng)
        elif n_slots == REPLAY_ONLY_SLOTS:
            assigned = _stratified_replay_only_rows(record_keys, rng=rng)
        else:
            raise ValueError(
                f"sample_collocation_points: the ratified §3.2 16-bin stratified "
                f"allocation has no defined construction for {n_slots} selected "
                f"slots at the ratified total {RATIFIED_TOTAL} (only "
                f"{FULL_BATCH_SLOTS} full-slot or {REPLAY_ONLY_SLOTS} "
                f"replay-only are defined); refusing rather than falling back "
                f"to a non-stratified draw -- a resource failure is "
                f"fail-closed, never permission to reduce the ratified count "
                f"(pinn_architecture.md Phase-56 contract)"
            )
    else:
        # Legacy near-even per-slot quota draw, preserved byte-for-byte for
        # any caller requesting a non-ratified total.
        per_slot_quotas = allocate_collocation_quota(len(record_keys), collocation_count, rng)
        assigned = []
        for key, per_slot_count in zip(record_keys, per_slot_quotas):
            for value in rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=per_slot_count):
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
    collocation_count: int = RATIFIED_TOTAL,
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
    "FULL_BATCH_SLOTS",
    "RATIFIED_N_BINS",
    "RATIFIED_PER_BIN",
    "RATIFIED_TOTAL",
    "REPLAY_ONLY_SLOTS",
    "SelectedStageRecords",
    "allocate_collocation_quota",
    "build_stage_batch",
    "sample_collocation_points",
    "sample_data_points",
    "select_stage_records",
    "select_validation_records",
]
