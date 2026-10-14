"""Phase 59 (D-03, D-12, D-31, D-35): production reference trajectories for Phase-59 tools.

Reference rows are the admitted, preprocessed trajectories the trainer sees.
This module never builds a corpus path and never names a corpus folder. It
only asks the allowlisted reader to read or check a record that reader already
refused or accepted.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.preprocessing import (
    NormalizationStats,
    build_raw_ic13,
    compute_invariants,
    compute_normalization_stats,
    normalize_ic13,
    preprocess_trajectory,
)
from pinn.data.types import Fidelity, RecordKey, StageLabel, Variant
from pinn.loss_catalog import _matched_plummer_components
from pinn.verification import split_allowlist


class NormalizerRecoveryError(ValueError):
    """The retained IC13 rows do not reproduce a normalizer inside tolerance."""


def inner_pair_slots(permutation):
    """Map IC-file bodies 1 and 2 through the canonical-order permutation."""
    inverse = np.argsort(np.asarray(permutation))
    return tuple(sorted((int(inverse[0]), int(inverse[1]))))


def _as_float64(array):
    return np.asarray(array, dtype=np.float64)


def _cast_float32(array):
    return torch.tensor(np.asarray(array, dtype=np.float64), dtype=torch.float32)


@dataclass(frozen=True)
class ReferenceTrajectory:
    record_key: RecordKey
    split: str
    grid: str
    times: object
    positions: object
    velocities: object
    positions_com_ordered: object
    masses: object
    permutation: object
    inner_pair: tuple
    raw_ic13: object
    E: float
    Q: float
    s_min: float
    l_ratio: object
    k0: float
    uabs0: float
    dt_out_measured: float
    dt_out_reference: object
    dt_out_reference_provenance: object
    n_snapshots: int
    D: float
    T: float
    manifest_stage: object


def load_reference(reader, key) -> ReferenceTrajectory:
    """Read one allowlisted record and apply the production preprocessing chain."""
    if not isinstance(reader, split_allowlist.AllowlistedCorpusReader):
        raise TypeError("reader must be an AllowlistedCorpusReader")
    if not np.isfinite(float(T_CHARACTERISTIC_TIME)):
        raise ValueError("characteristic time is not finite")
    admitted = reader.read(key)
    parsed = admitted.parsed_brutus
    pre = preprocess_trajectory(
        parsed.times, parsed.positions, parsed.velocities, parsed.masses
    )
    invariants = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
    raw_ic13 = build_raw_ic13(
        pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, invariants.E
    )
    kinetic0, potential0 = _matched_plummer_components(
        pre.r_gauge[0],
        pre.v_gauge[0],
        pre.masses_ordered,
        dtype=torch.float64,
        device=torch.device("cpu"),
    )
    return ReferenceTrajectory(
        record_key=key,
        split=admitted.split,
        grid=key.fidelity,
        times=_as_float64(parsed.times),
        positions=_as_float64(pre.r_gauge),
        velocities=_as_float64(pre.v_gauge),
        positions_com_ordered=_as_float64(pre.r_com_ordered),
        masses=_as_float64(pre.masses_ordered),
        permutation=np.asarray(pre.permutation),
        inner_pair=inner_pair_slots(pre.permutation),
        raw_ic13=_as_float64(raw_ic13),
        E=float(invariants.E),
        Q=float(invariants.Q),
        s_min=float(invariants.s_min),
        l_ratio=invariants.l_ratio,
        k0=float(kinetic0[0]),
        uabs0=float(abs(potential0[0])),
        dt_out_measured=float(admitted.dt_out_measured),
        dt_out_reference=admitted.dt_out_reference,
        dt_out_reference_provenance=admitted.dt_out_reference_provenance,
        n_snapshots=int(pre.r_gauge.shape[0]),
        D=float(pre.D),
        T=float(pre.T),
        manifest_stage=reader.allowlist.manifest_stage(key),
    )


def _stage_label(manifest_stage):
    if manifest_stage == "UNASSIGNED":
        return StageLabel.UNASSIGNED
    return StageLabel(int(manifest_stage))


def resident_record(reference, stats):
    """Float32 record with the adapter residency cast and acceleration callable."""
    times = _cast_float32(reference.times)
    positions = _cast_float32(reference.positions)
    velocities = _cast_float32(reference.velocities)

    def acceleration_magnitudes():
        count = int(times.shape[0])
        if count < 2:
            raise ValueError("record needs at least two snapshots")
        acceleration = torch.empty_like(velocities)
        acceleration[0] = (velocities[1] - velocities[0]) / (times[1] - times[0])
        acceleration[-1] = (
            (velocities[-1] - velocities[-2]) / (times[-1] - times[-2])
        )
        if count > 2:
            denominator = (times[2:] - times[:-2]).reshape(-1, 1, 1)
            acceleration[1:-1] = (velocities[2:] - velocities[:-2]) / denominator
        return torch.linalg.vector_norm(acceleration.reshape(count, -1), dim=1)

    return SimpleNamespace(
        record_key=reference.record_key,
        physical_key=reference.record_key.physical_key,
        variant=Variant(reference.record_key.variant),
        fidelity=Fidelity(reference.record_key.fidelity),
        ic13=_cast_float32(normalize_ic13(reference.raw_ic13, stats)),
        masses=_cast_float32(reference.masses),
        raw_ic13=_cast_float32(reference.raw_ic13),
        dt_out_measured=float(reference.dt_out_measured),
        dt_out_reference=reference.dt_out_reference,
        dt_out_reference_provenance=reference.dt_out_reference_provenance,
        n_snapshots=int(reference.n_snapshots),
        E=float(reference.E),
        l_ratio=reference.l_ratio,
        Q=float(reference.Q),
        min_separation=float(reference.s_min),
        k0=float(reference.k0),
        uabs0=float(reference.uabs0),
        stage_label=_stage_label(reference.manifest_stage),
        snapshot_times=times,
        snapshot_positions=positions,
        snapshot_velocities=velocities,
        acceleration_magnitudes=acceleration_magnitudes,
    )


def _record_key(value):
    # Retained checkpoints store the weights-only list written by
    # pinn.training.controllers._record_key_payload.
    if isinstance(value, (list, tuple)) and len(value) == 3:
        variant, fidelity, identifier = value
        return RecordKey(str(variant), str(fidelity), int(identifier))
    raise ValueError("checkpoint record key must be a variant, fidelity, id list")


def recover_ic13_normalizer(normalized_rows, row_keys, raw_ic13_by_key):
    """Fit the production tanh normalizer and return stats plus the residual."""
    stored = np.asarray(normalized_rows, dtype=np.float32)
    if stored.ndim != 2 or stored.shape[1] != 13:
        raise ValueError(f"normalized rows must have shape (N, 13); got {stored.shape}")
    if len(row_keys) != stored.shape[0]:
        raise ValueError("row_keys and normalized rows have different lengths")
    raws = np.stack([
        _as_float64(raw_ic13_by_key[key]) for key in row_keys
    ])
    clipped = np.clip(stored.astype(np.float64), -1.0 + 1e-7, 1.0 - 1e-7)
    transformed = np.arctanh(clipped)
    means = np.empty(12, dtype=np.float64)
    stds = np.empty(12, dtype=np.float64)
    ones = np.ones(stored.shape[0], dtype=np.float64)
    for slot in range(12):
        design = np.column_stack((ones, transformed[:, slot]))
        coefficient, _residual, _rank, _singular = np.linalg.lstsq(
            design, raws[:, slot], rcond=None
        )
        means[slot] = float(coefficient[0])
        stds[slot] = float(coefficient[1] - 1e-8)
    energy_x = transformed[:, 12]
    denominator = float(np.dot(energy_x, energy_x))
    if denominator == 0.0 or not np.isfinite(denominator):
        raise NormalizerRecoveryError("energy slot has no finite scale")
    e_scale = float(np.dot(raws[:, 12], energy_x) / denominator)
    stats = NormalizationStats(slot_means=means, slot_stds=stds, e_scale=e_scale)
    produced = {}
    for key, raw in raw_ic13_by_key.items():
        produced[key] = np.asarray(normalize_ic13(raw, stats), dtype=np.float32)
    residual = 0.0
    for index, key in enumerate(row_keys):
        difference = np.max(np.abs(
            produced[key].astype(np.float64) - stored[index].astype(np.float64)
        ))
        residual = max(residual, float(difference))
    return stats, residual


def _retention_sha256(repo_root, relative):
    path = split_allowlist._repo_root(repo_root) / split_allowlist.GENERATION7_RETENTION_REL
    payload = json.loads(path.read_text(encoding="utf-8"))
    target = relative.as_posix() if hasattr(relative, "as_posix") else str(relative)
    for entry in payload.get("files", ()):
        if entry.get("path") == target:
            return entry["sha256"]
    raise ValueError(f"retention manifest has no entry for {target}")


def load_retained_checkpoint(repo_root, run_name, file_name, *, expected_step):
    """Load one retention-pinned checkpoint. Refuse a hash or step mismatch."""
    relative = Path("runs") / run_name / "checkpoints" / file_name
    path = Path(repo_root) / relative
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    expected = _retention_sha256(repo_root, relative)
    if digest != expected:
        raise ValueError(f"checkpoint sha256 {digest} != retention {expected}")
    payload = torch.load(path, map_location="cpu", weights_only=True)
    step = int(payload["counters"]["global_step"])
    if step != int(expected_step):
        raise ValueError(f"checkpoint global_step {step} != expected {expected_step}")
    provenance = {
        "run": run_name,
        "file": file_name,
        "path": relative.as_posix(),
        "sha256": digest,
        "size_bytes": len(raw),
        "global_step": step,
    }
    return payload, provenance


def recover_normalizer_from_checkpoint(reader, payload, *, tolerance):
    data = payload["front_monitor"]["batch"]["data"]
    row_keys = tuple(_record_key(item) for item in data["record_keys"])
    unique = tuple(dict.fromkeys(row_keys))
    raw_by_key = {}
    for key in unique:
        raw_by_key[key] = load_reference(reader, key).raw_ic13
    rows = data["tau_ic13"][:, 1:14].detach().cpu().numpy()
    stats, residual = recover_ic13_normalizer(rows, row_keys, raw_by_key)
    if residual > tolerance:
        raise NormalizerRecoveryError(
            f"normalizer recovery residual {residual} exceeds {tolerance}"
        )
    return {
        "stats": stats,
        "residual": float(residual),
        "record_keys": unique,
        "source": "recovered_from_checkpoint",
    }


def fallback_normalizer_from_allowlist(reader, allowlist):
    raws = []
    energies = []
    for split in ("train", "validation"):
        for key in allowlist.records(split):
            if not reader.exists(key):
                continue
            try:
                reference = load_reference(reader, key)
            except split_allowlist.NotAdmitted:
                continue
            raws.append(reference.raw_ic13)
            energies.append(reference.E)
    if not raws:
        raise NormalizerRecoveryError("no admitted allowlisted record is available")
    stats = compute_normalization_stats(
        np.stack(raws), np.asarray(energies, dtype=np.float64)
    )
    return {
        "stats": stats,
        "source": "fallback_train_validation (deviation, GAP-59-06 option B)",
    }


def stats_digest(stats) -> str:
    payload = {
        "e_scale": repr(float(stats.e_scale)),
        "slot_means": [
            repr(float(value))
            for value in np.asarray(stats.slot_means, dtype=np.float64).reshape(-1)
        ],
        "slot_stds": [
            repr(float(value))
            for value in np.asarray(stats.slot_stds, dtype=np.float64).reshape(-1)
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def monitor_batch_reproduction(payload, references_by_key, stats, *, ic13_tolerance):
    data = payload["front_monitor"]["batch"]["data"]
    tau_ic13 = data["tau_ic13"]
    masses = data["masses"]
    targets = data["targets"]
    times = data["times"]
    count = int(times.shape[0])
    mismatches_targets = 0
    mismatches_times = 0
    mismatches_masses = 0
    ic13_max_abs = 0.0
    seen = set()
    for index in range(count):
        key = _record_key(data["record_keys"][index])
        seen.add(key)
        reference = references_by_key[key]
        reference_times = _cast_float32(reference.times)
        matches = (reference_times == times[index]).nonzero(as_tuple=False).reshape(-1)
        if int(matches.numel()) != 1:
            mismatches_times += 1
            continue
        snapshot = int(matches[0])
        reference_position = _cast_float32(reference.positions[snapshot]).reshape(-1)
        if not torch.equal(reference_position, targets[index].reshape(-1)):
            mismatches_targets += 1
        reference_mass = _cast_float32(reference.masses).reshape(-1)
        if not torch.equal(reference_mass, masses[index].reshape(-1)):
            mismatches_masses += 1
        expected_ic13 = _cast_float32(normalize_ic13(reference.raw_ic13, stats))
        difference = torch.max(torch.abs(expected_ic13 - tau_ic13[index, 1:14]))
        ic13_max_abs = max(ic13_max_abs, float(difference))
    passed = (
        mismatches_targets == 0
        and mismatches_times == 0
        and mismatches_masses == 0
        and ic13_max_abs <= ic13_tolerance
    )
    return {
        "rows": count,
        "identities": len(seen),
        "mismatches_targets": mismatches_targets,
        "mismatches_times": mismatches_times,
        "mismatches_masses": mismatches_masses,
        "ic13_max_abs": ic13_max_abs,
        "passed": passed,
    }


def allowlisted_file_presence(reader, allowlist):
    counts = {}
    for split in ("train", "validation"):
        for variant in ("hierarchical", "standard"):
            for fidelity in ("base", "gold"):
                keys = allowlist.records(
                    split, variant=variant, fidelity=fidelity
                )
                existing = sum(1 for key in keys if reader.exists(key))
                counts[f"{split}/{variant}/{fidelity}"] = {
                    "manifest": len(keys),
                    "existing": existing,
                }
    return counts


__all__ = [
    "NormalizerRecoveryError",
    "ReferenceTrajectory",
    "allowlisted_file_presence",
    "fallback_normalizer_from_allowlist",
    "inner_pair_slots",
    "load_reference",
    "load_retained_checkpoint",
    "monitor_batch_reproduction",
    "recover_ic13_normalizer",
    "recover_normalizer_from_checkpoint",
    "resident_record",
    "stats_digest",
]
