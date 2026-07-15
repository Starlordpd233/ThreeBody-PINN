"""Deterministic DATA-06 population evidence over persisted Stage labels.

The admitted-set adapter classifies records before residency through
``pinn.data.stages.classify_stage_label``.  This module treats that persisted
field as authoritative for report membership.  The classifier is called here
only for the explicitly diagnostic, read-only threshold-sensitivity sweep.
"""

from __future__ import annotations

import math
from types import SimpleNamespace
from typing import Any, Iterable

from pinn.data.splits import StageIndex
from pinn.data.stages import classify_stage_label
from pinn.data.types import (
    Fidelity,
    PhysicalKey,
    RecordKey,
    StageLabel,
    StageZeroUnderpopulated,
    Variant,
)


_SCHEMA_VERSION = "phase39-stage-population/v1"
_FATAL_THRESHOLD = 240
_SWEEP_MULTIPLIERS = (0.5, 1.0, 2.0)
_LABEL_ORDER = ("0", "1", "UNASSIGNED")


def _materialize_records(source: Any) -> tuple[Any, ...]:
    """Materialize one admitted source once without reopening the corpus."""
    records = getattr(source, "records", None)
    if records is not None:
        materialized = records() if callable(records) else records
        return tuple(materialized)

    admitted_records = getattr(source, "admitted_records", None)
    if admitted_records is not None:
        materialized = (
            admitted_records() if callable(admitted_records) else admitted_records
        )
        return tuple(materialized)

    record_keys = getattr(source, "record_keys", None)
    get = getattr(source, "get", None)
    if callable(record_keys) and callable(get):
        return tuple(get(key) for key in tuple(record_keys()))

    try:
        return tuple(iter(source))
    except TypeError as exc:
        raise TypeError(
            "source must be an admitted-set adapter or expose records()/iteration"
        ) from exc


def _record_identity(record: Any) -> tuple[RecordKey, PhysicalKey]:
    record_key = getattr(record, "record_key", None)
    physical_key = getattr(record, "physical_key", None)
    if not isinstance(record_key, RecordKey):
        raise TypeError(f"record.record_key must be RecordKey; got {record_key!r}")
    if not isinstance(physical_key, PhysicalKey):
        raise TypeError(
            f"record.physical_key must be PhysicalKey; got {physical_key!r}"
        )
    if record_key.physical_key != physical_key:
        raise ValueError(
            "record physical identity disagrees with record_key: "
            f"{physical_key!r} != {record_key.physical_key!r}"
        )
    return record_key, physical_key


def _enum_value(value: Any, enum_type: type, field: str) -> str:
    if isinstance(value, enum_type):
        return str(value.value)
    if isinstance(value, str):
        return value
    raise TypeError(f"record.{field} must be {enum_type.__name__}; got {value!r}")


def _variant_fidelity(record: Any, record_key: RecordKey) -> tuple[str, str]:
    variant = _enum_value(getattr(record, "variant", None), Variant, "variant")
    fidelity = _enum_value(getattr(record, "fidelity", None), Fidelity, "fidelity")
    if (variant, fidelity) != (record_key.variant, record_key.fidelity):
        raise ValueError(
            "record variant/fidelity disagrees with record_key: "
            f"{(variant, fidelity)!r} != "
            f"{(record_key.variant, record_key.fidelity)!r}"
        )
    return variant, fidelity


def _label_name(record: Any, record_key: RecordKey) -> str:
    label = getattr(record, "stage_label", None)
    if not isinstance(label, StageLabel):
        raise TypeError(
            "record.stage_label must be the persisted StageLabel value; "
            f"got {label!r}"
        )
    if label is StageLabel.UNASSIGNED:
        return "UNASSIGNED"
    numeric = int(label.value)
    if numeric not in (0, 1):
        raise ValueError(f"unsupported numeric Stage label {numeric!r}")
    if (record_key.variant, record_key.fidelity) != ("hierarchical", "base"):
        if record_key.fidelity == "gold":
            raise ValueError(
                "gold_numeric_stage_count must be 0; "
                f"gold record {record_key!r} has numeric label {numeric}"
            )
        raise ValueError(
            "numeric labels contain only original/base hierarchical Set 1a; "
            f"got {record_key!r}"
        )
    return str(numeric)


def _minimum_separation(record: Any) -> float:
    value = getattr(record, "min_separation", None)
    if value is None:
        value = getattr(record, "s_min", None)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"record minimum separation must be numeric; got {value!r}")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"record minimum separation must be finite; got {result!r}")
    return result


def _linear_quantile(values: tuple[float, ...], fraction: float) -> Any:
    if not values:
        return None
    position = (len(values) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[lower]
    weight = position - lower
    return values[lower] * (1.0 - weight) + values[upper] * weight


def _distribution(values: Iterable[float]) -> dict[str, Any]:
    ordered = tuple(sorted(float(value) for value in values))
    return {
        "count": len(ordered),
        "min": ordered[0] if ordered else None,
        "quantiles": {
            "q25": _linear_quantile(ordered, 0.25),
            "q50": _linear_quantile(ordered, 0.50),
            "q75": _linear_quantile(ordered, 0.75),
        },
        "max": ordered[-1] if ordered else None,
        "values": list(ordered),
    }


def _tensor_storage(tensor: Any) -> Any:
    accessor = getattr(tensor, "untyped_storage", None)
    if not callable(accessor):
        return None
    storage = accessor()
    size = int(storage.nbytes())
    return (int(storage.data_ptr()), size), size


def _record_resident_bytes(
    source: Any,
    record: Any,
    record_key: RecordKey,
    seen_storages: set[tuple[int, int]],
) -> int:
    direct = getattr(record, "resident_bytes", None)
    if direct is not None:
        if isinstance(direct, bool) or not isinstance(direct, int) or direct < 0:
            raise TypeError(f"record.resident_bytes must be non-negative int; got {direct!r}")
        return direct

    tensors = [
        getattr(record, name, None)
        for name in ("ic13", "masses", "raw_ic13")
    ]
    for accessor_name in (
        "snapshot_times",
        "snapshot_positions",
        "snapshot_velocities",
    ):
        accessor = getattr(source, accessor_name, None)
        if callable(accessor):
            tensors.append(accessor(record_key))

    total = 0
    for tensor in tensors:
        storage_info = _tensor_storage(tensor)
        if storage_info is None:
            continue
        identity, size = storage_info
        if identity in seen_storages:
            continue
        seen_storages.add(identity)
        total += size
    return total


def _classifier_view(record: Any, variant: str, fidelity: str) -> SimpleNamespace:
    return SimpleNamespace(
        variant=Variant(variant),
        fidelity=Fidelity(fidelity),
        E=float(record.E),
        l_ratio=record.l_ratio,
        Q=float(record.Q),
        s_min=_minimum_separation(record),
    )


def _sensitivity_sweep(
    records: tuple[Any, ...],
    identities: tuple[tuple[RecordKey, PhysicalKey, str, str, str], ...],
    classifier_floor: float,
    pairs: tuple[tuple[str, str], ...],
) -> dict[str, Any]:
    eligible = [
        (record, variant, fidelity)
        for record, identity in zip(records, identities)
        for _key, _physical, variant, fidelity, _label in (identity,)
        if (variant, fidelity) == ("hierarchical", "base")
    ]
    entries = []
    for multiplier in _SWEEP_MULTIPLIERS:
        sweep_floor = classifier_floor * multiplier
        per_pair = {pair: 0 for pair in pairs}
        observed = 0
        for record, variant, fidelity in eligible:
            label = classify_stage_label(
                _classifier_view(record, variant, fidelity),
                interim_s0=sweep_floor,
            )
            if label is not StageLabel.UNASSIGNED and int(label.value) == 0:
                observed += 1
                per_pair[(variant, fidelity)] += 1
        nested: dict[str, dict[str, int]] = {}
        for (variant, fidelity), count in sorted(per_pair.items()):
            nested.setdefault(variant, {})[fidelity] = count
        entries.append(
            {
                "multiplier": multiplier,
                "interim_s0": sweep_floor,
                "stage0_full_split_count": observed,
                "by_variant_fidelity": nested,
            }
        )
    return {
        "purpose": "diagnostic_only_reversible_grid",
        "multipliers": list(_SWEEP_MULTIPLIERS),
        "entries": entries,
    }


def _admission_state(source: Any, total: int) -> dict[str, Any]:
    folder_counts = getattr(source, "folder_counts", {})
    if not isinstance(folder_counts, dict):
        raise TypeError("source.folder_counts must be a mapping")
    normalized = {
        str(folder): {
            str(name): int(value)
            for name, value in sorted(counts.items())
        }
        for folder, counts in sorted(folder_counts.items())
    }
    return {"total_admitted": total, "per_folder": normalized}


def build_population_report(source: Any, manifest: Any = None) -> dict[str, Any]:
    """Build portable DATA-06 evidence and raise on admitted/full underpopulation.

    Membership comes only from each record's persisted label.  A supplied split
    manifest adds a train-only diagnostic through ``StageIndex.from_split``;
    that count never participates in readiness.
    """
    records = _materialize_records(source)
    if len({getattr(record, "record_key", None) for record in records}) != len(records):
        raise ValueError("duplicate admitted record_key")

    classifier_floor = float(getattr(source, "classifier_interim_s0", 0.01))
    if not math.isfinite(classifier_floor) or classifier_floor <= 0.0:
        raise ValueError(
            "source.classifier_interim_s0 must be finite and positive; "
            f"got {classifier_floor!r}"
        )

    identities = []
    stage_records = {label: [] for label in _LABEL_ORDER}
    stage_physical = {label: set() for label in _LABEL_ORDER}
    stage_bytes = {label: 0 for label in _LABEL_ORDER}
    separation_values: dict[tuple[str, str], list[float]] = {}
    unassigned_by_fidelity: dict[str, int] = {}
    seen_storages: set[tuple[int, int]] = set()
    gold_numeric = 0

    for record in records:
        record_key, physical_key = _record_identity(record)
        variant, fidelity = _variant_fidelity(record, record_key)
        label_name = _label_name(record, record_key)
        if fidelity == "gold" and label_name != "UNASSIGNED":
            gold_numeric += 1
        identities.append((record_key, physical_key, variant, fidelity, label_name))
        stage_records[label_name].append(record_key)
        stage_physical[label_name].add(physical_key)
        stage_bytes[label_name] += _record_resident_bytes(
            source, record, record_key, seen_storages
        )
        separation_values.setdefault((variant, fidelity), []).append(
            _minimum_separation(record)
        )
        if label_name == "UNASSIGNED":
            unassigned_by_fidelity[fidelity] = (
                unassigned_by_fidelity.get(fidelity, 0) + 1
            )

    if gold_numeric != 0 or getattr(source, "gold_numeric_stage_count", 0) != 0:
        raise ValueError(
            f"gold_numeric_stage_count must be 0; got {gold_numeric}"
        )

    stages = {
        label: {
            "record_count": len(stage_records[label]),
            "physical_key_count": len(stage_physical[label]),
            "resident_bytes": stage_bytes[label],
        }
        for label in _LABEL_ORDER
    }
    total_resident = sum(stage_bytes.values())
    source_resident = getattr(source, "resident_tensor_bytes", None)
    if callable(source_resident) and total_resident != int(source_resident()):
        raise ValueError(
            "per-stage resident bytes do not sum to source resident_tensor_bytes: "
            f"{total_resident} != {source_resident()}"
        )

    pairs = tuple(sorted(separation_values))
    per_pair_distribution: dict[str, dict[str, Any]] = {}
    for (variant, fidelity), values in sorted(separation_values.items()):
        per_pair_distribution.setdefault(variant, {})[fidelity] = _distribution(values)
    all_separations = [
        value
        for values in separation_values.values()
        for value in values
    ]

    full_count = len(stage_records["0"])
    train_count = None
    if manifest is not None:
        train_index = StageIndex.from_split(source, manifest, "train")
        train_count = len(train_index.records_at(0))

    canonical_hash = getattr(source, "_canonical_hash", None)
    report = {
        "schema_version": _SCHEMA_VERSION,
        "adapter": {
            "source_type": type(source).__name__,
            "record_count": len(records),
            "classifier": "pinn.data.stages.classify_stage_label",
        },
        "version_state": {
            "status": "deferred" if canonical_hash is None else "canonical_present",
            "canonical_data_version_hash": canonical_hash,
        },
        "admission": _admission_state(source, len(records)),
        "stages": stages,
        "unassigned_by_fidelity": dict(sorted(unassigned_by_fidelity.items())),
        "resident_tensor_bytes": total_resident,
        "s_min": _distribution(all_separations),
        "s_min_by_variant_fidelity": per_pair_distribution,
        "s0_sensitivity_sweep": _sensitivity_sweep(
            records,
            tuple(identities),
            classifier_floor,
            pairs,
        ),
        "interim_s0": classifier_floor,
        "interim_s0_status": "input_evidence_not_selected_output",
        "gold_numeric_stage_count": 0,
        "stage0_full_split_count": full_count,
        "stage0_train_split_count": train_count,
        "stage0_train_split_role": "diagnostic_only_phase40",
        "readiness_operand": "stage0_full_split_count",
        "fatal": False,
    }

    if full_count < _FATAL_THRESHOLD:
        report["fatal"] = {
            "type": "StageZeroUnderpopulated",
            "threshold": _FATAL_THRESHOLD,
            "observed": full_count,
            "operand": "stage0_full_split_count",
        }
        error = StageZeroUnderpopulated(
            observed=full_count,
            threshold=_FATAL_THRESHOLD,
        )
        error.report = report
        raise error

    return report


__all__ = ["build_population_report"]
