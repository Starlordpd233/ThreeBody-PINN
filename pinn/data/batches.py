"""DATA-05 replay/lookahead selection and fixed two-point-set batches.

The public ``source`` seam is the memory-only StageQuery produced by DATA-04.
Phase 40 supplies ``StageIndex.from_split(adapter, manifest, "train")`` so no
validation/test key can enter a training batch.  This module owns neither epoch
iteration nor Phase-40 adaptive/residual-aware collocation density.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

from pinn.data.types import RecordKey, StageZeroUnderpopulated


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


__all__ = ["SelectedStageRecords", "select_stage_records"]
