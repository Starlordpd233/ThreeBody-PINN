"""Leakage-free DATA-04 splits and the memory-only StageQuery seam.

Every admitted record already carries its authoritative GAP-39-08
``stage_label``.  This module never reclassifies it and never accepts a second
stage map.  Physical siblings are grouped before local RNG is used, then each
complete ``(variant, base-stage-or-missing, gold-stage-or-missing)`` signature
is apportioned independently with Hamilton largest remainder.

Phase 40's train-only boundary is intentionally explicit::

    build_stage_batch(StageIndex.from_split(adapter, manifest, "train"), ...)

``source`` is the admitted-set adapter.  Materialization happens once through
its memory-only accessors; no disk format is consulted by splitting or query.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR
import enum
import json
from types import MappingProxyType
from typing import Any, Iterable, Mapping

import numpy as np

from pinn.data.types import (
    MISSING_BASE,
    MISSING_GOLD,
    PhysicalKey,
    RecordKey,
    StageLabel,
)


_SPLIT_NAMES = ("train", "validation", "test")
_ALGORITHM = "group-signature-hamilton-v1"


def _materialize_records(source: Any) -> tuple[Any, ...]:
    """Materialize one admitted-set source exactly once, entirely in memory."""
    records = getattr(source, "records", None)
    if records is not None:
        return tuple(records() if callable(records) else records)

    admitted_records = getattr(source, "admitted_records", None)
    if admitted_records is not None:
        return tuple(
            admitted_records() if callable(admitted_records) else admitted_records
        )

    record_keys = getattr(source, "record_keys", None)
    get = getattr(source, "get", None)
    if callable(record_keys) and callable(get):
        keys = tuple(record_keys())
        return tuple(get(key) for key in keys)

    try:
        return tuple(iter(source))
    except TypeError as exc:
        raise TypeError(
            "source must be an admitted-set adapter or expose records()/iteration"
        ) from exc


def _record_key(record: Any) -> RecordKey:
    key = getattr(record, "record_key", None)
    if not isinstance(key, RecordKey):
        raise TypeError(f"record.record_key must be RecordKey; got {key!r}")
    physical = getattr(record, "physical_key", None)
    if not isinstance(physical, PhysicalKey):
        raise TypeError(f"record.physical_key must be PhysicalKey; got {physical!r}")
    if physical != key.physical_key:
        raise ValueError(
            f"record physical identity disagrees with record_key: {physical!r} != "
            f"{key.physical_key!r}"
        )
    return key


def _stage_label(record: Any) -> StageLabel:
    label = getattr(record, "stage_label", None)
    if not isinstance(label, StageLabel):
        raise TypeError(
            "record.stage_label must be the persisted StageLabel value; "
            f"got {label!r}"
        )
    return label


def _numeric_stage(stage: Any) -> int:
    if isinstance(stage, StageLabel):
        if stage is StageLabel.UNASSIGNED:
            raise ValueError("UNASSIGNED is not a numeric stage")
        return int(stage.value)
    if isinstance(stage, bool) or not isinstance(stage, int) or stage < 0:
        raise TypeError(f"stage must be a non-negative int or numeric StageLabel; got {stage!r}")
    return stage


def _validated_records(records: Iterable[Any]) -> tuple[Any, ...]:
    by_key: dict[RecordKey, Any] = {}
    for record in records:
        key = _record_key(record)
        label = _stage_label(record)
        if key in by_key:
            raise ValueError(f"duplicate admitted record_key {key!r}")
        if label is not StageLabel.UNASSIGNED:
            if key.fidelity == "gold":
                raise ValueError(
                    "gold_numeric_stage_count must be 0; "
                    f"gold record {key!r} has {label!r}"
                )
            if (key.variant, key.fidelity) != ("hierarchical", "base"):
                raise ValueError(
                    "numeric stage pools contain only original/base hierarchical "
                    f"Set 1a records; got {key!r}"
                )
        by_key[key] = record
    return tuple(by_key[key] for key in sorted(by_key))


class StageIndex:
    """Immutable, memory-only index over persisted admitted-record labels."""

    __slots__ = (
        "_records",
        "_labels",
        "_pools",
        "_blacklisted_physical_keys",
        "_locked",
    )

    def __init__(self, records):
        self._initialize(records, frozenset())

    def __setattr__(self, name, value):
        if getattr(self, "_locked", False):
            raise AttributeError("StageIndex is immutable")
        object.__setattr__(self, name, value)

    def _initialize(self, records, blacklisted_physical_keys):
        validated = _validated_records(tuple(records))
        by_key = {record.record_key: record for record in validated}
        labels = {key: record.stage_label for key, record in by_key.items()}
        pools = {
            stage: tuple(key for key in sorted(labels) if labels[key].value == stage)
            for stage in (0, 1)
        }
        object.__setattr__(self, "_records", MappingProxyType(by_key))
        object.__setattr__(self, "_labels", MappingProxyType(labels))
        object.__setattr__(self, "_pools", MappingProxyType(pools))
        object.__setattr__(
            self, "_blacklisted_physical_keys", frozenset(blacklisted_physical_keys)
        )
        object.__setattr__(self, "_locked", True)

    @classmethod
    def _with_blacklist(cls, records, blacklisted_physical_keys):
        instance = object.__new__(cls)
        instance._initialize(records, blacklisted_physical_keys)
        return instance

    @classmethod
    def from_split(cls, source, manifest, split_name="train"):
        """Build one split-restricted index directly from the admitted adapter."""
        if split_name not in _SPLIT_NAMES:
            raise ValueError(f"split_name must be one of {_SPLIT_NAMES}; got {split_name!r}")
        records = _materialize_records(source)
        allowed = manifest.physical_keys(split_name)
        selected = [record for record in records if _record_key(record).physical_key in allowed]
        blacklist = getattr(source, "blacklisted_physical_keys", frozenset())
        return cls._with_blacklist(selected, blacklist)

    @property
    def stage_labels(self) -> Mapping[RecordKey, StageLabel]:
        return self._labels

    @property
    def blacklisted_physical_keys(self) -> frozenset[PhysicalKey]:
        return self._blacklisted_physical_keys

    @property
    def gold_numeric_stage_count(self) -> int:
        return 0

    def record_keys(self) -> tuple[RecordKey, ...]:
        return tuple(self._records)

    def get(self, key: RecordKey) -> Any:
        return self._records[key]

    def n_snapshots(self, key: RecordKey) -> int:
        return int(self._records[key].n_snapshots)

    def dt_out(self, key: RecordKey) -> float:
        record = self._records[key]
        if hasattr(record, "dt_out_measured"):
            return float(record.dt_out_measured)
        return float(record.dt_out)

    def stage_label(self, key: RecordKey) -> StageLabel:
        return self._labels[key]

    def has_stage(self, stage) -> bool:
        numeric = _numeric_stage(stage)
        return bool(self._pools.get(numeric, ()))

    def records_at(self, stage) -> tuple[RecordKey, ...]:
        return self._pools.get(_numeric_stage(stage), ())

    def records_at_or_below(self, stage) -> tuple[RecordKey, ...]:
        numeric = _numeric_stage(stage)
        return tuple(
            key
            for key in self._records
            if self._labels[key] is not StageLabel.UNASSIGNED
            and int(self._labels[key].value) <= numeric
        )

    def is_blacklisted(self, physical_key: PhysicalKey) -> bool:
        return physical_key in self._blacklisted_physical_keys


@dataclass(frozen=True)
class SplitRatios:
    train: float = 0.8
    validation: float = 0.1
    test: float = 0.1

    def __post_init__(self) -> None:
        values = (self.train, self.validation, self.test)
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
            raise TypeError("split ratios must be real numbers")
        if any(not np.isfinite(value) or value < 0.0 for value in values):
            raise ValueError("split ratios must be finite and non-negative")
        if sum(Decimal(str(value)) for value in values) != Decimal("1"):
            raise ValueError(f"split ratios must sum to 1; got {values!r}")

    def as_dict(self) -> dict[str, float]:
        return {name: float(getattr(self, name)) for name in _SPLIT_NAMES}


Signature = tuple[str, Any, Any]


def _json_stage(value: Any) -> Any:
    if value is MISSING_BASE:
        return "MISSING_BASE"
    if value is MISSING_GOLD:
        return "MISSING_GOLD"
    if isinstance(value, enum.Enum):
        return value.value
    return value


def _signature_dict(signature: Signature) -> dict[str, Any]:
    return {
        "variant": signature[0],
        "base_stage": _json_stage(signature[1]),
        "gold_stage": _json_stage(signature[2]),
    }


def _signature_sort_key(signature: Signature) -> str:
    return json.dumps(_signature_dict(signature), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class SignatureSummary:
    signature: Signature
    quota: Mapping[str, float]
    counts: Mapping[str, int]
    deviations: tuple[Mapping[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "signature": _signature_dict(self.signature),
            "quota": dict(self.quota),
            "counts": dict(self.counts),
            "deviations": [dict(item) for item in self.deviations],
        }


@dataclass(frozen=True)
class SplitGroup:
    physical_key: PhysicalKey
    signature: Signature
    split: str
    records: tuple[Any, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "physical_key": {
                "variant": self.physical_key.variant,
                "id": self.physical_key.id,
            },
            "signature": _signature_dict(self.signature),
            "split": self.split,
            "records": [
                {
                    "variant": record.record_key.variant,
                    "fidelity": record.record_key.fidelity,
                    "id": record.record_key.id,
                    "stage": _json_stage(record.stage_label),
                }
                for record in self.records
            ],
        }


@dataclass(frozen=True)
class SplitManifest:
    seed: int
    ratios: Mapping[str, float]
    signature_summaries: tuple[SignatureSummary, ...]
    groups: tuple[SplitGroup, ...]
    path: Any = None
    schema_version: int = 1
    algorithm: str = _ALGORITHM
    tie_order: tuple[str, ...] = _SPLIT_NAMES

    @property
    def signatures(self) -> tuple[Signature, ...]:
        return tuple(summary.signature for summary in self.signature_summaries)

    @property
    def splits(self) -> Mapping[str, tuple[RecordKey, ...]]:
        split_records = {}
        for split_name in _SPLIT_NAMES:
            records = [
                record.record_key
                for group in self.groups
                if group.split == split_name
                for record in group.records
            ]
            if split_name != "train":
                records.sort()
            split_records[split_name] = tuple(records)
        return MappingProxyType(split_records)

    def physical_keys(self, split_name: str) -> frozenset[PhysicalKey]:
        if split_name not in _SPLIT_NAMES:
            raise ValueError(f"split_name must be one of {_SPLIT_NAMES}; got {split_name!r}")
        return frozenset(
            group.physical_key for group in self.groups if group.split == split_name
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "algorithm": self.algorithm,
            "seed": self.seed,
            "ratios": dict(self.ratios),
            "tie_order": list(self.tie_order),
            "signatures": [summary.to_dict() for summary in self.signature_summaries],
            "groups": [group.to_dict() for group in self.groups],
        }


def _signature_for_group(records: tuple[Any, ...]) -> Signature:
    variant = records[0].record_key.variant
    by_fidelity = {}
    for record in records:
        key = record.record_key
        if key.variant != variant:
            raise ValueError("one physical group cannot contain multiple variants")
        if key.fidelity in by_fidelity:
            raise ValueError(
                f"physical group has duplicate {key.fidelity!r} record for {key.physical_key!r}"
            )
        by_fidelity[key.fidelity] = record

    base = by_fidelity.get("base")
    gold = by_fidelity.get("gold")
    base_stage = MISSING_BASE if base is None else _json_stage(base.stage_label)
    if gold is None:
        gold_stage = MISSING_GOLD
    else:
        if gold.stage_label is not StageLabel.UNASSIGNED:
            raise ValueError(
                "gold_numeric_stage_count must be 0 while constructing split signature"
            )
        gold_stage = "UNASSIGNED"
    return (variant, base_stage, gold_stage)


def _hamilton_counts(size: int, ratios: SplitRatios):
    ratio_values = [Decimal(str(getattr(ratios, name))) for name in _SPLIT_NAMES]
    quotas = [Decimal(size) * value for value in ratio_values]
    floors = [int(quota.to_integral_value(rounding=ROUND_FLOOR)) for quota in quotas]
    remaining = size - sum(floors)
    order = sorted(
        range(len(_SPLIT_NAMES)),
        key=lambda index: (-(quotas[index] - floors[index]), index),
    )
    counts = list(floors)
    for index in order[:remaining]:
        counts[index] += 1
    return quotas, counts


def _partition_by_signature(records, seed, ratios) -> SplitManifest:
    """Pure complete-signature Hamilton partition used by the manifest writer."""
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise TypeError(f"seed must be a non-negative int; got {seed!r}")
    if not isinstance(ratios, SplitRatios):
        if isinstance(ratios, Mapping):
            ratios = SplitRatios(**ratios)
        else:
            raise TypeError("ratios must be SplitRatios or a split-name mapping")

    admitted = _validated_records(tuple(records))
    if not admitted:
        raise ValueError("cannot partition an empty admitted set")

    grouped: dict[PhysicalKey, list[Any]] = {}
    for record in admitted:
        grouped.setdefault(record.record_key.physical_key, []).append(record)

    signature_groups: dict[Signature, list[tuple[PhysicalKey, tuple[Any, ...]]]] = {}
    for physical_key in sorted(grouped):
        members = tuple(sorted(grouped[physical_key], key=lambda item: item.record_key))
        signature = _signature_for_group(members)
        signature_groups.setdefault(signature, []).append((physical_key, members))

    summaries = []
    assignments: dict[PhysicalKey, tuple[str, Signature, tuple[Any, ...], int]] = {}
    for signature_index, signature in enumerate(sorted(signature_groups, key=_signature_sort_key)):
        members = sorted(signature_groups[signature], key=lambda item: item[0])
        rng = np.random.default_rng(np.random.SeedSequence([seed, signature_index]))
        permutation = rng.permutation(len(members)).tolist()
        permuted = [members[index] for index in permutation]
        quotas, count_values = _hamilton_counts(len(members), ratios)
        counts = dict(zip(_SPLIT_NAMES, count_values))
        quota_dict = {
            name: float(quota) for name, quota in zip(_SPLIT_NAMES, quotas)
        }
        deviations = tuple(
            {
                "split": name,
                "quota": quota_dict[name],
                "count": counts[name],
                "delta": float(Decimal(counts[name]) - quotas[index]),
            }
            for index, name in enumerate(_SPLIT_NAMES)
            if Decimal(counts[name]) != quotas[index]
        )
        summaries.append(
            SignatureSummary(
                signature=signature,
                quota=MappingProxyType(quota_dict),
                counts=MappingProxyType(counts),
                deviations=deviations,
            )
        )

        cursor = 0
        for split_name in _SPLIT_NAMES:
            stop = cursor + counts[split_name]
            for local_order, (physical_key, group_records) in enumerate(
                permuted[cursor:stop], start=cursor
            ):
                if physical_key in assignments:
                    raise AssertionError(f"physical key assigned twice: {physical_key!r}")
                assignments[physical_key] = (
                    split_name,
                    signature,
                    group_records,
                    local_order,
                )
            cursor = stop
        if cursor != len(permuted):
            raise AssertionError("Hamilton counts did not consume the signature")

    if set(assignments) != set(grouped):
        raise AssertionError("every physical key must be assigned exactly once")

    groups = tuple(
        SplitGroup(
            physical_key=physical_key,
            signature=assignments[physical_key][1],
            split=assignments[physical_key][0],
            records=assignments[physical_key][2],
        )
        for physical_key in sorted(assignments)
    )
    manifest = SplitManifest(
        seed=seed,
        ratios=MappingProxyType(ratios.as_dict()),
        signature_summaries=tuple(summaries),
        groups=groups,
    )

    seen = {}
    for split_name, record_keys in manifest.splits.items():
        for key in record_keys:
            previous = seen.setdefault(key.physical_key, split_name)
            if previous != split_name:
                raise AssertionError(f"physical key spans {previous!r} and {split_name!r}")
    return manifest


__all__ = ["SplitManifest", "SplitRatios", "StageIndex", "write_split_manifest"]
