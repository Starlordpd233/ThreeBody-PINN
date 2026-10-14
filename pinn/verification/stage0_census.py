"""Phase 59 (FEAS-02; D-12, D-13, D-31, D-32): the Stage-0 difficulty census, the reader acceptance and the panels.

The census reads the corpus only through the allowlist. It never names a
corpus folder, never builds the admitted-set adapter, and constructs no
optimizer. Validation rows carry the agreement check only; their difficulty
fields stay empty. Panels come from the frozen rule and from nothing else.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.adapter import measure_dt_out
from pinn.physics_residual import softened_acceleration
from pinn.verification import evidence_io, production_reference, split_allowlist
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.production_reference import (
    NormalizerRecoveryError,
    fallback_normalizer_from_allowlist,
    load_reference,
    load_retained_checkpoint,
    monitor_batch_reproduction,
    recover_normalizer_from_checkpoint,
    stats_digest,
)
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    AllowlistedCorpusReader,
    SplitAllowlist,
    expected_splits_sha256,
    install_open_attestation,
    resolve_data_root,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TWO_PI = 2.0 * np.pi
_QUANTILES = (0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100)
_COLUMNS = (
    "split",
    "id",
    "N_in",
    "N_in_max_step_rad",
    "N_in_base_assisted",
    "base_cross_check_flag",
    "N_out",
    "N_out_max_step_rad",
    "sep_min",
    "sep_max",
    "acc_min",
    "acc_max",
    "phase_accuracy_0.01",
    "phase_accuracy_0.1",
    "base_dt",
    "samples_per_inner_period",
    "inner_pair",
    "closest_pair_t0",
    "pair_tracking_ok",
    "gold_base_max_dev",
    "gold_n_times",
    "base_n_times",
)
_DIFFICULTY_FIELDS = (
    "N_in",
    "N_in_max_step_rad",
    "N_in_base_assisted",
    "base_cross_check_flag",
    "N_out",
    "N_out_max_step_rad",
    "sep_min",
    "sep_max",
    "acc_min",
    "acc_max",
    "phase_accuracy_0.01",
    "phase_accuracy_0.1",
    "base_dt",
    "samples_per_inner_period",
)
_RUN_NAME = "stage0-v23g7-seed42"
_INIT_FILE = "stage-0-init.pt"
PRODUCER_MODULES = (
    "pinn/verification/stage0_census.py",
    "pinn/verification/split_allowlist.py",
    "pinn/verification/production_reference.py",
    "pinn/verification/evidence_io.py",
    "pinn/verification/feasibility_scorecard.py",
)


class CensusHalt(RuntimeError):
    """A fail-closed stop. The panels are not written."""


def orbit_normal(v0, vdot0):
    """Unit normal of the initial separation and its u-derivative."""
    left = np.asarray(v0, dtype=np.float64).reshape(3)
    right = np.asarray(vdot0, dtype=np.float64).reshape(3)
    cross = np.cross(left, right)
    norm = float(np.linalg.norm(cross))
    scale = float(np.linalg.norm(left) * np.linalg.norm(right))
    if (
        not np.isfinite(norm)
        or not np.isfinite(scale)
        or scale == 0.0
        or norm < 1e-12 * scale
    ):
        raise CensusHalt(
            "orbit normal is undefined: the separation and its derivative are nearly parallel"
        )
    return cross / norm


def _angle_steps(vectors, normal):
    stacked = np.asarray(vectors, dtype=np.float64)
    if stacked.ndim != 2 or stacked.shape[1] != 3 or stacked.shape[0] < 2:
        raise CensusHalt("revolution count needs at least two 3-vectors")
    cross = np.cross(stacked[:-1], stacked[1:])
    triple = cross @ np.asarray(normal, dtype=np.float64).reshape(3)
    dots = np.sum(stacked[:-1] * stacked[1:], axis=1)
    return np.arctan2(triple, dots)


def unwrapped_turns(vectors, normal):
    """Return (turns, max |step|). Each step is the principal angle."""
    steps = _angle_steps(vectors, normal)
    if not np.all(np.isfinite(steps)):
        raise CensusHalt("an unwrapped angle step is not finite")
    return float(steps.sum() / _TWO_PI), float(np.max(np.abs(steps)))


def _window(reference, t_max):
    times = np.asarray(reference.times, dtype=np.float64)
    mask = times <= float(t_max) + 1e-9
    if int(np.count_nonzero(mask)) < 2:
        raise CensusHalt("fewer than two samples at or below t_max")
    positions = np.asarray(reference.positions, dtype=np.float64)[mask]
    velocities = np.asarray(reference.velocities, dtype=np.float64)[mask]
    masses = np.asarray(reference.masses, dtype=np.float64).reshape(3)
    return times[mask], positions, velocities, masses


def _pair_slots(reference):
    pair = tuple(int(slot) for slot in reference.inner_pair)
    if len(pair) != 2 or pair[0] == pair[1] or any(slot not in (0, 1, 2) for slot in pair):
        raise CensusHalt(f"inner pair {pair} is not two distinct body slots")
    outer = ({0, 1, 2} - set(pair)).pop()
    return pair[0], pair[1], outer


def _separation(positions, velocities, first, second):
    vector = positions[:, second, :] - positions[:, first, :]
    derivative = velocities[:, second, :] - velocities[:, first, :]
    return vector, derivative


def inner_revolutions(reference, *, t_max):
    """Gold-grid inner turns about the initial orbit normal, for t <= t_max."""
    _times, positions, velocities, _masses = _window(reference, t_max)
    first, second, _outer = _pair_slots(reference)
    vector, derivative = _separation(positions, velocities, first, second)
    normal = orbit_normal(vector[0], derivative[0])
    turns, max_step = unwrapped_turns(vector, normal)
    return {"turns": turns, "max_step_rad": max_step}


def outer_revolutions(reference, *, t_max):
    """Fractional outer turns. The vector is r_c minus the inner-pair centre of mass."""
    _times, positions, velocities, masses = _window(reference, t_max)
    first, second, outer = _pair_slots(reference)
    inner_mass = float(masses[first] + masses[second])
    if inner_mass <= 0.0 or not np.isfinite(inner_mass):
        raise CensusHalt("inner-pair mass is not positive")
    centre = (
        masses[first] * positions[:, first, :] + masses[second] * positions[:, second, :]
    ) / inner_mass
    centre_velocity = (
        masses[first] * velocities[:, first, :] + masses[second] * velocities[:, second, :]
    ) / inner_mass
    vector = positions[:, outer, :] - centre
    derivative = velocities[:, outer, :] - centre_velocity
    normal = orbit_normal(vector[0], derivative[0])
    turns, max_step = unwrapped_turns(vector, normal)
    return {"turns": turns, "max_step_rad": max_step}


def assisted_base_revolutions(reference, *, t_max):
    """Mean-motion-assisted unwrap on the base grid.

    Velocities are dr'/du. A step with non-positive osculating 1/a keeps its
    principal angle and is not assisted.
    """
    times, positions, velocities, masses = _window(reference, t_max)
    first, second, _outer = _pair_slots(reference)
    mu = float(masses[first] + masses[second])
    if mu <= 0.0 or not np.isfinite(mu):
        raise CensusHalt("inner-pair mass is not positive")
    characteristic = float(reference.T)
    if characteristic <= 0.0 or not np.isfinite(characteristic):
        raise CensusHalt("characteristic time is not positive")
    vector, derivative = _separation(positions, velocities, first, second)
    normal = orbit_normal(vector[0], derivative[0])
    steps = _angle_steps(vector, normal)
    du = np.diff(times / characteristic)
    radius = np.linalg.norm(vector, axis=1)
    speed_sq = np.sum(derivative * derivative, axis=1)
    inverse_a = 2.0 / radius - speed_sq / mu
    valid = np.isfinite(inverse_a[:-1]) & (inverse_a[:-1] > 0.0) & np.isfinite(du)
    corrected = np.array(steps, copy=True)
    if np.any(valid):
        semi = 1.0 / inverse_a[:-1][valid]
        mean_motion = np.sqrt(mu / semi**3)
        predicted = mean_motion * du[valid]
        corrected[valid] = steps[valid] + _TWO_PI * np.round(
            (predicted - steps[valid]) / _TWO_PI
        )
    if not np.all(np.isfinite(corrected)):
        raise CensusHalt("an assisted angle step is not finite")
    return float(corrected.sum() / _TWO_PI)


def separation_range(reference, *, t_max):
    """Minimum and maximum of the three pairwise distances on t <= t_max."""
    _times, positions, _velocities, _masses = _window(reference, t_max)
    distances = []
    for left, right in ((0, 1), (0, 2), (1, 2)):
        distances.append(np.linalg.norm(positions[:, left, :] - positions[:, right, :], axis=1))
    stacked = np.concatenate(distances)
    if not np.all(np.isfinite(stacked)):
        raise CensusHalt("a pairwise separation is not finite")
    return float(stacked.min()), float(stacked.max())


def acceleration_range(reference, *, t_max):
    """Minimum and maximum body acceleration magnitude in the r' frame."""
    _times, positions, _velocities, masses = _window(reference, t_max)
    acceleration = softened_acceleration(
        positions,
        masses,
        dtype=torch.float64,
        device=torch.device("cpu"),
    )
    magnitude = torch.linalg.vector_norm(acceleration, dim=-1)
    if not torch.isfinite(magnitude).all():
        raise CensusHalt("a softened acceleration is not finite")
    return float(magnitude.min()), float(magnitude.max())


def samples_per_inner_period(n_in, base_dt, *, T):
    """(T / N_in) / base_dt. The inner period is T / N_in."""
    return float(T) / float(n_in) / float(base_dt)


def phase_accuracy(n_in, delta):
    """Phase figure delta / (2 pi N_in)."""
    return float(delta) / (_TWO_PI * float(n_in))


def gold_base_agreement(base_ref, gold_ref):
    """Max |r_gold - r_base| / R_sys over base times and bodies.

    Each base time must match a gold time within 1e-9. R_sys is the maximum
    body radius on the base trajectory.
    """
    base_times = np.asarray(base_ref.times, dtype=np.float64)
    gold_times = np.asarray(gold_ref.times, dtype=np.float64)
    base_positions = np.asarray(base_ref.positions, dtype=np.float64)
    gold_positions = np.asarray(gold_ref.positions, dtype=np.float64)
    radii = np.linalg.norm(base_positions, axis=-1)
    r_sys = float(np.max(radii))
    if not np.isfinite(r_sys) or r_sys <= 0.0:
        raise CensusHalt("R_sys is not positive")
    worst = 0.0
    for time_value, position in zip(base_times, base_positions):
        delta = np.abs(gold_times - float(time_value))
        index = int(np.argmin(delta))
        if float(delta[index]) > 1e-9:
            raise CensusHalt(
                f"base time {float(time_value)!r} has no gold sample within 1e-9"
            )
        difference = np.linalg.norm(gold_positions[index] - position, axis=-1)
        worst = max(worst, float(np.max(difference) / r_sys))
    return worst


def closest_pair_at_t0(reference):
    """Sorted slots of the closest pair at the first sample. Ties take the lower slots."""
    position = np.asarray(reference.positions, dtype=np.float64)[0]
    pairs = ((0, 1), (0, 2), (1, 2))
    best = min(
        pairs,
        key=lambda pair: (float(np.linalg.norm(position[pair[0]] - position[pair[1]])), pair),
    )
    return tuple(best)


def _count_times(reference, t_max):
    times = np.asarray(reference.times, dtype=np.float64)
    return int(np.count_nonzero(times <= float(t_max) + 1e-9))


def _permutations_differ(base_ref, gold_ref):
    return not np.array_equal(
        np.asarray(base_ref.permutation),
        np.asarray(gold_ref.permutation),
    )


def _blank_row(split, identifier, inner_pair, closest, tracking, deviation, gold_count, base_count):
    row = {name: None for name in _COLUMNS}
    row.update(
        {
            "split": split,
            "id": int(identifier),
            "inner_pair": tuple(inner_pair),
            "closest_pair_t0": tuple(closest),
            "pair_tracking_ok": bool(tracking),
            "gold_base_max_dev": float(deviation),
            "gold_n_times": int(gold_count),
            "base_n_times": int(base_count),
        }
    )
    return row


def census_row(base_ref, gold_ref, *, split, scorecard):
    """One census row. Validation rows leave every difficulty field empty."""
    if gold_ref is None:
        raise CensusHalt("gold record is absent")
    if _permutations_differ(base_ref, gold_ref):
        raise CensusHalt(f"base and gold permutations differ for id {base_ref.record_key.id}")
    for reference in (base_ref, gold_ref):
        if float(reference.T) != float(T_CHARACTERISTIC_TIME):
            raise CensusHalt("reference T is not the characteristic time")
    rules = scorecard.section("census_rules")
    grid = scorecard.section("scoring_grid")
    t_max = float(grid["t_max"])
    inner = tuple(int(slot) for slot in base_ref.inner_pair)
    closest = closest_pair_at_t0(base_ref)
    gold_closest = closest_pair_at_t0(gold_ref)
    tracking = closest == inner and gold_closest == tuple(int(slot) for slot in gold_ref.inner_pair)
    deviation = gold_base_agreement(base_ref, gold_ref)
    identifier = int(base_ref.record_key.id)
    row = _blank_row(
        split,
        identifier,
        inner,
        closest,
        tracking,
        deviation,
        _count_times(gold_ref, t_max),
        _count_times(base_ref, t_max),
    )
    if split == "validation":
        return row
    if split != "train":
        raise CensusHalt(f"split {split} is not train or validation")
    inner_count = inner_revolutions(gold_ref, t_max=t_max)
    outer_count = outer_revolutions(gold_ref, t_max=t_max)
    limit = float(rules["unwrap_max_step_rad"])
    if inner_count["max_step_rad"] >= limit or outer_count["max_step_rad"] >= limit:
        raise CensusHalt(
            f"id {identifier} unwrap step reached {limit} "
            f"(inner {inner_count['max_step_rad']}, outer {outer_count['max_step_rad']})"
        )
    n_in = float(inner_count["turns"])
    if not np.isfinite(n_in) or n_in <= 0.0:
        raise CensusHalt(f"id {identifier} inner turn count is not positive")
    assisted = float(assisted_base_revolutions(base_ref, t_max=t_max))
    sep_min, sep_max = separation_range(gold_ref, t_max=t_max)
    acc_min, acc_max = acceleration_range(gold_ref, t_max=t_max)
    base_dt = float(measure_dt_out(np.asarray(base_ref.times, dtype=np.float64)))
    if not np.isfinite(base_dt) or base_dt <= 0.0:
        raise CensusHalt(f"id {identifier} base dt is not positive")
    relative = abs(assisted - n_in) / n_in
    row.update(
        {
            "N_in": n_in,
            "N_in_max_step_rad": float(inner_count["max_step_rad"]),
            "N_in_base_assisted": assisted,
            "base_cross_check_flag": bool(relative > float(rules["base_cross_check_flag_relative"])),
            "N_out": float(outer_count["turns"]),
            "N_out_max_step_rad": float(outer_count["max_step_rad"]),
            "sep_min": float(sep_min),
            "sep_max": float(sep_max),
            "acc_min": float(acc_min),
            "acc_max": float(acc_max),
            "phase_accuracy_0.01": phase_accuracy(n_in, 0.01),
            "phase_accuracy_0.1": phase_accuracy(n_in, 0.1),
            "base_dt": base_dt,
            "samples_per_inner_period": samples_per_inner_period(
                n_in, base_dt, T=float(base_ref.T)
            ),
        }
    )
    return row


def select_panels(train_rows, validation_ids, *, scorecard):
    """Apply the frozen panel rule. Ties take the lower id. Nothing is redrawn."""
    rule = scorecard.section("panel_rule")
    population = int(rule["population_size"])
    if len(train_rows) != population:
        raise CensusHalt(
            f"training population {len(train_rows)} != panel_rule.population_size {population}"
        )
    identifiers = [int(row["id"]) for row in train_rows]
    if len(identifiers) != len(set(identifiers)):
        raise CensusHalt("training ids are not unique")
    n_in = np.array([float(row["N_in"]) for row in train_rows], dtype=np.float64)
    percentiles = [int(item) for item in rule["singles_percentiles"]]
    targets = np.percentile(n_in, percentiles, method="linear")
    minimum = float(rule["singles_min_samples_per_inner_period"])
    eligible = [
        row for row in train_rows if float(row["samples_per_inner_period"]) >= minimum
    ]
    if len(eligible) < len(percentiles):
        raise CensusHalt("not enough systems have 3 base samples per inner period")
    singles = []
    chosen = set()
    for percentile, target in zip(percentiles, targets):
        target = float(target)
        best = min(
            eligible,
            key=lambda row: (abs(float(row["N_in"]) - target), int(row["id"])),
        )
        if int(best["id"]) in chosen:
            raise CensusHalt(f"single id {int(best['id'])} was picked twice")
        chosen.add(int(best["id"]))
        singles.append(
            {
                "percentile": int(percentile),
                "target": target,
                "id": int(best["id"]),
                "N_in": float(best["N_in"]),
                "samples_per_inner_period": float(best["samples_per_inner_period"]),
            }
        )
    ordered = sorted(train_rows, key=lambda row: (float(row["N_in"]), int(row["id"])))
    parts = np.array_split(np.arange(len(ordered)), int(rule["family_size"]))
    expected = [int(item) for item in rule["family_bin_sizes"]]
    sizes = [int(part.size) for part in parts]
    if sizes != expected:
        raise CensusHalt(f"family bin sizes {sizes} != {expected}")
    family = []
    for index, part in enumerate(parts):
        members = [ordered[int(offset)] for offset in part]
        values = np.array([float(row["N_in"]) for row in members], dtype=np.float64)
        median = float(np.median(values))
        remaining = [row for row in members if int(row["id"]) not in chosen]
        if not remaining:
            raise CensusHalt(f"family bin {index} is empty after excluding singles")
        best = min(
            remaining,
            key=lambda row: (abs(float(row["N_in"]) - median), int(row["id"])),
        )
        if int(best["id"]) in chosen:
            raise CensusHalt(f"family id {int(best['id'])} repeats a single")
        chosen.add(int(best["id"]))
        family.append(
            {
                "bin": int(index),
                "size": int(part.size),
                "median": median,
                "id": int(best["id"]),
                "N_in": float(best["N_in"]),
            }
        )
    validation = sorted(int(item) for item in validation_ids)
    expected_validation = int(rule["validation_panel_size"])
    if len(validation) != expected_validation or len(set(validation)) != len(validation):
        raise CensusHalt(
            f"validation panel has {len(set(validation))} distinct ids, "
            f"expected {expected_validation}"
        )
    return {"singles": singles, "family": family, "validation": validation}


def _stage0_base_keys(allowlist, split):
    return allowlist.records(split, variant="hierarchical", fidelity="base", stage=0)


def _gold_index(allowlist, split):
    keys = allowlist.records(
        split, variant="hierarchical", fidelity="gold", stage="UNASSIGNED"
    )
    return {int(key.id): key for key in keys}


def _load_or_halt(reader, key):
    try:
        return load_reference(reader, key)
    except split_allowlist.NotAdmitted as exc:
        raise CensusHalt(
            f"id {int(key.id)} {key.fidelity} was not admitted ({exc.disposition})"
        ) from exc


def _row_for(reader, base_key, gold_key, split, scorecard):
    if gold_key is None:
        raise CensusHalt(f"gold record is absent for id {int(base_key.id)}")
    base = _load_or_halt(reader, base_key)
    gold = _load_or_halt(reader, gold_key)
    try:
        return census_row(base, gold, split=split, scorecard=scorecard)
    finally:
        del base, gold


def _producer():
    return evidence_io.module_hashes(PRODUCER_MODULES, repo_root=_REPO_ROOT)


def _plain_float(value):
    return format(float(value), ".12g")


def _part_in(median):
    return int(round(1.0 / float(median)))


def _distribution(values):
    array = np.asarray(list(values), dtype=np.float64)
    return {
        "count": int(array.size),
        "quantiles": {
            str(quantile): float(np.percentile(array, quantile, method="linear"))
            for quantile in _QUANTILES
        },
    }


def _csv_cell(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return repr(float(value))
    if isinstance(value, tuple):
        return f"{int(value[0])}-{int(value[1])}"
    return str(int(value) if isinstance(value, (int, np.integer)) else value)


def census_csv(rows):
    """Header plus one row per system. Floats use repr. None is an empty cell."""
    ordered = sorted(rows, key=lambda row: (0 if row["split"] == "train" else 1, int(row["id"])))
    lines = [",".join(_COLUMNS)]
    for row in ordered:
        lines.append(",".join(_csv_cell(row[name]) for name in _COLUMNS))
    return "\n".join(lines) + "\n"


def _quantile(distribution, quantile):
    return float(distribution["quantiles"][str(quantile)])


def census_summary(census_payload, panels):
    """Plain-language census. The first heading is fixed."""
    n_in = census_payload["distributions"]["N_in"]
    samples = census_payload["distributions"]["samples_per_inner_period"]
    phase = census_payload["phase_accuracy"]
    below = census_payload["distributions"]["samples_below"]
    singles = panels["singles"]
    single_text = ", ".join(
        f"id {item['id']} (N_in {_plain_float(item['N_in'])}, "
        f"{_plain_float(item['samples_per_inner_period'])} base samples per inner period)"
        for item in singles
    )
    lines = [
        "## In plain language",
        "",
        "This census counts inner laps for the 1,812 Stage-0 training systems "
        "and checks that the reader agrees with the gold sibling.",
        f"The median system completes {_plain_float(_quantile(n_in, 50))} inner laps by t = 10. "
        f"The 10th percentile completes {_plain_float(_quantile(n_in, 10))} "
        f"and the 90th completes {_plain_float(_quantile(n_in, 90))}.",
        "The phase-accuracy figure is how precisely a network must time those laps. "
        f"For a 10% end-point miss the median figure is {_plain_float(phase['0.1']['median'])}, "
        f"about 1 part in {phase['0.1']['one_part_in']}. "
        f"For a 1% miss it is {_plain_float(phase['0.01']['median'])}, "
        f"about 1 part in {phase['0.01']['one_part_in']}.",
        f"On the base grid, {below['below_2']} training systems have fewer than 2 samples "
        f"per inner period, {below['below_3']} have fewer than 3, and "
        f"{below['below_5']} have fewer than 5.",
        f"The three single systems are the eligible systems nearest the 10th, 50th and "
        f"90th percentiles of N_in: {single_text}. "
        "A system is eligible only when the base grid has at least 3 samples per inner "
        "period. An equal distance picks the lower id.",
        "The 16-system family takes one system from each bin of the census sorted by "
        "inner laps, so the family spans the census. "
        "The validation panel is all 227 Stage-0 validation systems, and those systems "
        "were not given difficulty numbers. No test-split file was opened.",
        "",
        "## Numbers",
        "",
        f"- Training systems: {census_payload['population']['train']}",
        f"- Validation systems: {census_payload['population']['validation']}",
        f"- Pair-tracking failures: {census_payload['checks']['pair_tracking_failures']}",
        "- Gold-base max deviation: "
        f"{_plain_float(census_payload['checks']['gold_base_max_deviation'])}",
        f"- Largest inner unwrap step: {_plain_float(census_payload['checks']['unwrap_max_step_rad'])}",
        f"- Base cross-check flags: {census_payload['checks']['base_cross_check_flags']}",
        "",
    ]
    return "\n".join(lines)


def build_census_payload(rows, scorecard):
    """census.json body except the csv hash, which the caller fills in."""
    train = [row for row in rows if row["split"] == "train"]
    validation = [row for row in rows if row["split"] == "validation"]
    samples = [float(row["samples_per_inner_period"]) for row in train]
    sample_array = np.asarray(samples, dtype=np.float64)
    distributions = {
        "N_in": _distribution(row["N_in"] for row in train),
        "N_out": _distribution(row["N_out"] for row in train),
        "samples_per_inner_period": _distribution(samples),
        "phase_accuracy_0.1": _distribution(row["phase_accuracy_0.1"] for row in train),
        "phase_accuracy_0.01": _distribution(row["phase_accuracy_0.01"] for row in train),
        "acc_max": _distribution(row["acc_max"] for row in train),
        "sep_min": _distribution(row["sep_min"] for row in train),
        "samples_below": {
            "below_2": int(np.sum(sample_array < 2.0)),
            "below_3": int(np.sum(sample_array < 3.0)),
            "below_5": int(np.sum(sample_array < 5.0)),
        },
    }
    median_01 = _quantile(distributions["phase_accuracy_0.01"], 50)
    median_10 = _quantile(distributions["phase_accuracy_0.1"], 50)
    deviations = [float(row["gold_base_max_dev"]) for row in rows]
    return {
        "schema": "phase59-census/v1",
        "plain_language": (
            "Inner-lap census of the 1,812 Stage-0 training systems, plus the "
            "agreement check on the 227 validation systems. "
            f"The median phase-accuracy figure at 10% is {_plain_float(median_10)} "
            f"(about 1 part in {_part_in(median_10)})."
        ),
        "scorecard_sha256": scorecard.sha256,
        "producer_sha256": _producer(),
        "population": {"train": len(train), "validation": len(validation)},
        "distributions": distributions,
        "checks": {
            "pair_tracking_failures": int(sum(not row["pair_tracking_ok"] for row in rows)),
            "gold_base_max_deviation": float(max(deviations)),
            "gold_base_tolerance": float(scorecard.section("scoring_grid")["gold_base_agreement_max"]),
            "unwrap_max_step_rad": float(max(row["N_in_max_step_rad"] for row in train)),
            "base_cross_check_flags": int(sum(bool(row["base_cross_check_flag"]) for row in train)),
        },
        "phase_accuracy": {
            "0.01": {"median": median_01, "one_part_in": _part_in(median_01)},
            "0.1": {"median": median_10, "one_part_in": _part_in(median_10)},
        },
    }


def build_panels_payload(panels, scorecard, csv_sha256):
    single_ids = ", ".join(str(item["id"]) for item in panels["singles"])
    return {
        "schema": "phase59-panels/v1",
        "plain_language": (
            "Three single systems, a 16-system family, and all 227 Stage-0 "
            f"validation systems, chosen only by the frozen panel rule. Singles: {single_ids}."
        ),
        "scorecard_sha256": scorecard.sha256,
        "producer_sha256": _producer(),
        "rule": scorecard.section("panel_rule"),
        "census_csv_sha256": csv_sha256,
        "singles": panels["singles"],
        "family": panels["family"],
        "validation": panels["validation"],
    }


def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _require_census_checks(rows, scorecard):
    tolerance = float(scorecard.section("scoring_grid")["gold_base_agreement_max"])
    limit = float(scorecard.section("census_rules")["unwrap_max_step_rad"])
    failures = [int(row["id"]) for row in rows if not row["pair_tracking_ok"]]
    if failures:
        raise CensusHalt(
            f"pair tracking failed for {len(failures)} systems; first id {failures[0]}"
        )
    worst = max(float(row["gold_base_max_dev"]) for row in rows)
    if worst > tolerance:
        raise CensusHalt(f"gold-base agreement {worst} exceeds {tolerance}")
    for row in rows:
        if row["split"] != "train":
            continue
        if float(row["N_in_max_step_rad"]) >= limit or float(row["N_out_max_step_rad"]) >= limit:
            raise CensusHalt(f"id {row['id']} unwrap step reached {limit}")
    return worst


def _open_context(args):
    scorecard = load_scorecard()
    allowlist = SplitAllowlist.from_manifest(
        _REPO_ROOT / GENERATION7_SPLITS_REL,
        expected_sha256=expected_splits_sha256(_REPO_ROOT),
    )
    data_root, source = resolve_data_root(args.data_root)
    attestation = install_open_attestation(
        data_root=data_root,
        data_root_source=source,
        withheld_basenames=allowlist.withheld_basenames(),
        split_by_basename=allowlist.split_by_basename(),
    )
    reader = AllowlistedCorpusReader(
        allowlist=allowlist,
        data_root=data_root,
        data_root_source=source,
    )
    return scorecard, allowlist, reader, attestation, data_root, source


def _evidence_dir(args, area):
    if args.evidence_root:
        root = Path(args.evidence_root)
        if not root.is_absolute():
            root = Path.cwd() / root
    else:
        root = _REPO_ROOT / evidence_io.EVIDENCE_ROOT_REL
    return root / area


def _parse_ids(text):
    pieces = [part.strip() for part in str(text).split(",")]
    if not pieces or any(not part for part in pieces):
        raise CensusHalt("--ids is empty")
    identifiers = []
    for part in pieces:
        if not part.isascii() or not part.isdigit():
            raise CensusHalt(f"id {part} is not an integer")
        identifiers.append(int(part))
    return identifiers


def _stdout_rows(args):
    scorecard, allowlist, reader, _attestation, _root, _source = _open_context(args)
    train = {int(key.id): key for key in _stage0_base_keys(allowlist, "train")}
    gold = _gold_index(allowlist, "train")
    for identifier in _parse_ids(args.ids):
        base_key = train.get(identifier)
        if base_key is None:
            raise CensusHalt(f"id {identifier} is outside the Stage-0 training split")
        row = _row_for(reader, base_key, gold.get(identifier), "train", scorecard)
        print(json.dumps(evidence_io.json_safe(row), sort_keys=True, allow_nan=False))
    return 0


def _batch_keys(payload):
    data = payload["front_monitor"]["batch"]["data"]
    found = []
    seen = set()
    for item in data["record_keys"]:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            raise CensusHalt("checkpoint record key must be a variant, fidelity, id list")
        key = (str(item[0]), str(item[1]), int(item[2]))
        if key in seen:
            continue
        seen.add(key)
        found.append(production_reference._record_key(item))
    return tuple(found)


def _normalizer_block(stats, source, residual, tolerance, deviation):
    means = np.asarray(stats.slot_means, dtype=np.float64).reshape(-1)
    stds = np.asarray(stats.slot_stds, dtype=np.float64).reshape(-1)
    return {
        "source": source,
        "checkpoint": _INIT_FILE,
        "slot_means": [float(value) for value in means],
        "slot_stds": [float(value) for value in stds],
        "e_scale": float(stats.e_scale),
        "max_abs_residual": float(residual),
        "tolerance": float(tolerance),
        "deviation": bool(deviation),
        "stats_sha256": stats_digest(stats),
    }


def _presence_or_halt(presence):
    for name, counts in sorted(presence.items()):
        if int(counts["existing"]) != int(counts["manifest"]):
            raise CensusHalt(
                f"{name} has {counts['existing']} files on disk "
                f"and {counts['manifest']} manifest records"
            )


def run_acceptance(args):
    """Prove the allowlisted reader matches the retained monitor batch."""
    scorecard, allowlist, reader, attestation, data_root, source = _open_context(args)
    if len(allowlist.manifest.groups) != 7606:
        raise CensusHalt(f"splits groups {len(allowlist.manifest.groups)} != 7606")
    if len(allowlist.allowed) != 6847 or len(allowlist.withheld) != 759:
        raise CensusHalt(
            f"splits allowed {len(allowlist.allowed)} withheld {len(allowlist.withheld)} "
            "!= 6847 and 759"
        )
    presence = production_reference.allowlisted_file_presence(reader, allowlist)
    _presence_or_halt(presence)
    base_train = (
        presence["train/hierarchical/base"]["manifest"]
        + presence["train/standard/base"]["manifest"]
    )
    base_validation = (
        presence["validation/hierarchical/base"]["manifest"]
        + presence["validation/standard/base"]["manifest"]
    )
    if base_train != 6085 or base_validation != 762:
        raise CensusHalt(
            f"base presence is train {base_train} validation {base_validation}, "
            "expected 6085 and 762"
        )
    payload, checkpoint = load_retained_checkpoint(
        _REPO_ROOT, _RUN_NAME, _INIT_FILE, expected_step=0
    )
    tolerance = float(scorecard.section("diag07")["tolerances"]["normalizer_recovery_max_abs"])
    ic13_tolerance = float(
        scorecard.section("diag07")["tolerances"]["monitor_reproduction_ic13_abs"]
    )
    try:
        recovered = recover_normalizer_from_checkpoint(
            reader, payload, tolerance=tolerance
        )
        stats = recovered["stats"]
        residual = float(recovered["residual"])
        normalizer_source = str(recovered["source"])
        deviation = False
    except NormalizerRecoveryError as exc:
        fallback = fallback_normalizer_from_allowlist(reader, allowlist)
        stats = fallback["stats"]
        normalizer_source = str(fallback["source"])
        deviation = True
        text = str(exc)
        marker = "residual "
        if marker not in text:
            raise CensusHalt(f"normalizer recovery failed without a residual: {text}") from exc
        residual = float(text.split(marker, 1)[1].split(" ", 1)[0])
    references = {
        key: load_reference(reader, key) for key in _batch_keys(payload)
    }
    report = monitor_batch_reproduction(
        payload, references, stats, ic13_tolerance=ic13_tolerance
    )
    if (
        report["passed"] is not True
        or int(report["rows"]) != 8192
        or int(report["identities"]) != 256
        or int(report["mismatches_targets"]) != 0
        or int(report["mismatches_times"]) != 0
        or int(report["mismatches_masses"]) != 0
    ):
        raise CensusHalt(
            "monitor batch reproduction failed: "
            f"rows {report['rows']}, identities {report['identities']}, "
            f"targets {report['mismatches_targets']}, "
            f"times {report['mismatches_times']}, "
            f"masses {report['mismatches_masses']}, "
            f"ic13 {report['ic13_max_abs']}"
        )
    reproduction = {
        "checkpoint": checkpoint["path"],
        "checkpoint_sha256": checkpoint["sha256"],
        "global_step": int(checkpoint["global_step"]),
        "rows": int(report["rows"]),
        "identities": int(report["identities"]),
        "mismatches_targets": int(report["mismatches_targets"]),
        "mismatches_times": int(report["mismatches_times"]),
        "mismatches_masses": int(report["mismatches_masses"]),
        "ic13_max_abs": float(report["ic13_max_abs"]),
        "ic13_tolerance": float(ic13_tolerance),
        "passed": True,
    }
    acceptance = {
        "schema": "phase59-reader-acceptance/v1",
        "plain_language": (
            "The allowlisted reader reproduced the trainer's resident monitor "
            f"batch ({reproduction['rows']} rows, {reproduction['identities']} identities) "
            f"with normalizer residual {residual!r} and deviation {str(deviation).lower()}."
        ),
        "scorecard_sha256": scorecard.sha256,
        "producer_sha256": _producer(),
        "data_root_source": source,
        "splits": {
            "sha256": allowlist.manifest_sha256,
            "expected_from": "generation-7-retention",
            "groups": len(allowlist.manifest.groups),
            "allowed_physical_keys": len(allowlist.allowed),
            "withheld_physical_keys": len(allowlist.withheld),
        },
        "file_presence": presence,
        "monitor_batch_reproduction": reproduction,
        "normalizer": _normalizer_block(
            stats, normalizer_source, residual, tolerance, deviation
        ),
    }
    summary = _acceptance_summary(acceptance)
    return {
        "acceptance": acceptance,
        "summary": summary,
        "attestation": attestation,
        "data_root": data_root,
        "data_root_source": source,
    }


def _acceptance_summary(acceptance):
    normalizer = acceptance["normalizer"]
    report = acceptance["monitor_batch_reproduction"]
    deviation = "true" if normalizer["deviation"] else "false"
    return "\n".join(
        [
            "## In plain language",
            "",
            "This check asks whether the allowlisted reader sees the same numbers "
            "the trainer stored in its Stage-0 monitor batch.",
            f"The reader matched the trainer's own resident numbers: {report['rows']} rows, "
            f"{report['identities']} identities, and no mismatch in targets, times, or masses. "
            f"The largest IC13 difference is {report['ic13_max_abs']!r}.",
            f"The normalizer residual is {normalizer['max_abs_residual']!r} "
            f"against tolerance {normalizer['tolerance']!r}. Deviation is {deviation}.",
            "No held-out file was opened. The test split was not read.",
            "",
        ]
    )


def _compare(path, raw, label):
    if not evidence_io.bytes_identical(path, raw):
        print(f"CENSUS-CHECK-DIFF: {label}", file=sys.stderr)
        return False
    return True


def _assert_opened_zeros(attestation, directory):
    summary = attestation.summary()
    for key in ("test_split_opened", "blocked_attempts", "refused_before_open"):
        if summary.get(key) != 0:
            print(f"CENSUS-CHECK-DIFF: live {key} is {summary.get(key)}", file=sys.stderr)
            return False
    path = directory / "files_opened.json"
    if path.is_file():
        payload = json.loads(path.read_text(encoding="utf-8"))
        for key in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            if payload.get(key) != 0:
                print(f"CENSUS-CHECK-DIFF: files_opened {key}", file=sys.stderr)
                return False
    return True


def _write_records(directory, attestation, data_root, source, started_wall, started, tool):
    evidence_io.write_json(
        directory / "files_opened.json",
        evidence_io.files_opened_record(tool, attestation.summary()),
        data_root=data_root,
    )
    evidence_io.write_json(
        directory / "provenance.json",
        evidence_io.provenance_record(
            tool,
            sys.argv,
            data_root=data_root,
            data_root_source=source,
            utc_started=started_wall,
            monotonic_started=started,
        ),
        data_root=data_root,
    )


def _acceptance_mode(args, *, check, started_wall, started):
    result = run_acceptance(args)
    directory = _evidence_dir(args, "audit")
    acceptance_bytes = evidence_io.canonical_json_bytes(result["acceptance"])
    summary_bytes = result["summary"].encode("utf-8")
    if check:
        same = _compare(directory / "reader_acceptance.json", acceptance_bytes, "reader_acceptance.json")
        same = _compare(directory / "summary.md", summary_bytes, "audit summary.md") and same
        same = _assert_opened_zeros(result["attestation"], directory) and same
        if not same:
            return 1
        print("AUDIT-CHECK-OK")
        return 0
    evidence_io.write_json(
        directory / "reader_acceptance.json",
        result["acceptance"],
        data_root=result["data_root"],
    )
    evidence_io.write_text(
        directory / "summary.md",
        result["summary"],
        data_root=result["data_root"],
    )
    _write_records(
        directory,
        result["attestation"],
        result["data_root"],
        result["data_root_source"],
        started_wall,
        started,
        "stage0_census --acceptance",
    )
    return 0


def _training_count():
    path = _REPO_ROOT / "runs" / _RUN_NAME / "training_metadata.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return int(payload["n_train"])


def collect_census(args):
    """Load every Stage-0 train and validation row. Do not select panels yet."""
    scorecard, allowlist, reader, attestation, data_root, source = _open_context(args)
    if _training_count() != 1812:
        raise CensusHalt(f"training_metadata n_train {_training_count()} != 1812")
    rows = []
    populations = {}
    for split, expected in (("train", 1812), ("validation", 227)):
        bases = _stage0_base_keys(allowlist, split)
        gold = _gold_index(allowlist, split)
        if len(bases) != expected:
            raise CensusHalt(f"{split} Stage-0 population {len(bases)} != {expected}")
        populations[split] = len(bases)
        total = len(bases)
        for index, base_key in enumerate(bases, start=1):
            rows.append(
                _row_for(reader, base_key, gold.get(int(base_key.id)), split, scorecard)
            )
            if index == total or index % 500 == 0:
                print(f"census {split} {index}/{total}", file=sys.stderr)
    return {
        "scorecard": scorecard,
        "rows": rows,
        "populations": populations,
        "attestation": attestation,
        "data_root": data_root,
        "data_root_source": source,
    }


def _census_bytes(rows, scorecard):
    _require_census_checks(rows, scorecard)
    train = [row for row in rows if row["split"] == "train"]
    validation_ids = [int(row["id"]) for row in rows if row["split"] == "validation"]
    panels = select_panels(train, validation_ids, scorecard=scorecard)
    csv_text = census_csv(rows)
    payload = build_census_payload(rows, scorecard)
    payload["census_csv_sha256"] = _sha256_text(csv_text)
    panel_payload = build_panels_payload(panels, scorecard, payload["census_csv_sha256"])
    summary = census_summary(payload, panels)
    return {
        "csv": csv_text.encode("utf-8"),
        "census": evidence_io.canonical_json_bytes(payload),
        "panels": evidence_io.canonical_json_bytes(panel_payload),
        "summary": summary.encode("utf-8"),
        "payload": payload,
        "panels_payload": panel_payload,
    }


def _census_mode(args, *, check, started_wall, started):
    collected = collect_census(args)
    rendered = _census_bytes(collected["rows"], collected["scorecard"])
    directory = _evidence_dir(args, "census")
    if check:
        same = _compare(directory / "census.csv", rendered["csv"], "census.csv")
        same = _compare(directory / "census.json", rendered["census"], "census.json") and same
        same = _compare(directory / "panels.json", rendered["panels"], "panels.json") and same
        same = _compare(directory / "summary.md", rendered["summary"], "census summary.md") and same
        same = _assert_opened_zeros(collected["attestation"], directory) and same
        if not same:
            return 1
        print("CENSUS-CHECK-OK")
        return 0
    evidence_io.write_text(
        directory / "census.csv",
        rendered["csv"].decode("utf-8"),
        data_root=collected["data_root"],
    )
    evidence_io.write_json(
        directory / "census.json",
        rendered["payload"],
        data_root=collected["data_root"],
    )
    evidence_io.write_json(
        directory / "panels.json",
        rendered["panels_payload"],
        data_root=collected["data_root"],
    )
    evidence_io.write_text(
        directory / "summary.md",
        rendered["summary"].decode("utf-8"),
        data_root=collected["data_root"],
    )
    _write_records(
        directory,
        collected["attestation"],
        collected["data_root"],
        collected["data_root_source"],
        started_wall,
        started,
        "stage0_census",
    )
    return 0


def _parse_args(argv):
    parser = argparse.ArgumentParser(prog="stage0_census")
    parser.add_argument("--ids", default=None)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--acceptance", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--evidence-root", default=None)
    return parser.parse_args(argv)


def _run(argv, *, started_wall, started):
    args = _parse_args(argv)
    try:
        freeze = evidence_io.require_frozen_scorecard(_REPO_ROOT)
    except evidence_io.FreezeNotEstablished as exc:
        print(f"FREEZE-REFUSED: {exc}", file=sys.stderr)
        return 1
    print(f"FREEZE-OK {freeze['freeze_commit']}", file=sys.stderr)
    if args.ids or args.stdout:
        if not (args.ids and args.stdout) or args.acceptance or args.check:
            raise CensusHalt("--ids and --stdout are a read-only pair")
        return _stdout_rows(args)
    if args.acceptance:
        return _acceptance_mode(args, check=args.check, started_wall=started_wall, started=started)
    return _census_mode(args, check=args.check, started_wall=started_wall, started=started)


def main(argv=None) -> int:
    """Census CLI. The freeze guard runs before any corpus or checkpoint read."""
    started_wall = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    try:
        code = _run(argv, started_wall=started_wall, started=started)
    except CensusHalt as exc:
        print(f"CENSUS-HALT: {exc}", file=sys.stderr)
        code = 2
    except split_allowlist.SplitRefused as exc:
        print(f"SplitRefused: {exc}", file=sys.stderr)
        code = 2
    gate = evidence_io.runtime_gate(time.monotonic() - started, label="CENSUS")
    if gate != 0:
        return gate
    return code


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "PRODUCER_MODULES",
    "CensusHalt",
    "acceleration_range",
    "assisted_base_revolutions",
    "census_row",
    "closest_pair_at_t0",
    "gold_base_agreement",
    "inner_revolutions",
    "main",
    "orbit_normal",
    "outer_revolutions",
    "phase_accuracy",
    "samples_per_inner_period",
    "select_panels",
    "separation_range",
    "unwrapped_turns",
]
