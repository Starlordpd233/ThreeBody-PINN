"""Phase 59 (FEAS-08; D-18, D-19, D-20, D-21, D-33): the read-only whole-dataset survey.

The survey reads every training-split record through the allowlist, gives each
record a diagnostic stage label, measures how hard each stage is, ranks the
stages against the curriculum order, and picks the two FEAS-09 probe systems by
their frozen rule. It reports and never gates: no training, evaluation or rung
module imports it.

The labels are diagnostic. Stages 0 and 1 come from the splits manifest.
Stages 2 to 6 apply the spec criteria (ctl_instruction.md:138-264) in
ascending precedence, with Stage 6 the residual. The official stage mapping
beyond Stages 0 and 1 stays owner-pending (ctl_instruction.md:326-347). tau_L
is the spec's revisable Rosenstein-style baseline, whose final form is also
owner-pending (D-33-07). The v1.3-era estimator is cross-check material only
and is not imported here. The vectorized estimator below is tested against a
literal transcription of the spec snippet (ctl_instruction.md:1369-1435).

Every threshold and setting comes from the frozen scorecard's survey_rules
section. The survey owns its own predicates for Stages 2 to 6 and does not
extend the production Stage-0/1 classifier.
"""

from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import io
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from pinn.verification import evidence_io, split_allowlist
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.production_reference import load_reference
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    AllowlistedCorpusReader,
    SplitAllowlist,
    expected_splits_sha256,
    install_open_attestation,
    resolve_data_root,
)
from pinn.verification.stage0_census import (
    CensusHalt,
    acceleration_range,
    inner_revolutions,
    outer_revolutions,
    phase_accuracy,
    separation_range,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
PRODUCER_MODULES = (
    "pinn/verification/dataset_survey.py",
    "pinn/verification/stage0_census.py",
    "pinn/verification/split_allowlist.py",
    "pinn/verification/production_reference.py",
    "pinn/verification/evidence_io.py",
    "pinn/verification/feasibility_scorecard.py",
)
EXPECTED_TRAINING_RECORDS = 12023
PREFLIGHT_REQUIRED_BYTES = 2 * 1024**3
NO_PICK_REASON = (
    "stage has no labelled training-split record; no substitute without owner sight"
)
NOT_APPLICABLE_HIERARCHICAL = "not applicable: no hierarchical split"
UNLABELLED = "unlabelled"
_PRECEDENCE = ("0", "1", "2", "3", "4a", "4b", "5", "6")
_FIDELITY_ORDER = {"base": 0, "gold": 1}
_EXP_LIMIT = 709.0
_STAGE6_S_MIN = 0.5
_STAGE6_ABS_E = 0.01
_HIERARCHICAL_MEASURES = ("N_in", "N_out", "phase_accuracy_0.1", "phase_accuracy_0.01")
_MEASURES = (
    "closest_approach",
    "acc_min",
    "acc_max",
    "N_in",
    "N_out",
    "phase_accuracy_0.1",
    "phase_accuracy_0.01",
    "tau_L_primary",
    "error_growth",
)
# (measure, which direction is harder). Stages are ordered by the stage median.
_DIRECTIONS = (
    ("N_in", "larger"),
    ("acc_max", "larger"),
    ("closest_approach", "smaller"),
    ("tau_L_primary", "smaller"),
    ("error_growth", "larger"),
    ("phase_accuracy_0.1", "smaller"),
)
CSV_COLUMNS = (
    "variant",
    "fidelity",
    "id",
    "stage_label",
    "stage_substage",
    "stage_rule",
    "stage_source",
    "E",
    "Q",
    "s_min",
    "l_ratio",
    "stage3_criterion_computable",
    "stage6_clause",
    "closest_approach",
    "acc_min",
    "acc_max",
    "N_in",
    "N_out",
    "phase_accuracy_0.1",
    "phase_accuracy_0.01",
    "tau_L_primary",
    "tau_L_status",
    "tau_L_reason",
    "tau_L_w1",
    "tau_L_w2",
    "tau_L_w3",
    "error_growth",
    "fit_points_primary",
)
_LABEL_SOURCES = {
    "0": "splits manifest (record stage 0)",
    "1": "splits manifest (record stage 1)",
    "2": "spec criterion: hierarchical gold records are the Stage 2 data source",
    "3": "spec criterion: Stage 3 percentile gating on standard base records",
    "4a": "spec criterion: tau_L above 5 on standard base records",
    "4b": "spec criterion: tau_L above 2 and at most 5 on standard base records",
    "5": "spec criterion: tau_L above 2 on standard gold records",
    "6": "spec criterion: residual, all remaining data (ctl_instruction.md:252-253)",
    UNLABELLED: "none: tau_L could not be computed, so the record is not pushed into a stage",
}


class SurveyHalt(RuntimeError):
    """A fail-closed stop. Nothing is written."""


def _finite(value):
    if value is None:
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _window_label(window):
    return f"w{float(window):g}"


def _tau_keys(label):
    if label == "primary":
        return "tau_L_primary", "tau_L_status"
    return f"tau_L_{label}", f"tau_L_{label}_status"


@functools.lru_cache(maxsize=1)
def _frozen_unwrap_limit():
    return float(load_scorecard().section("census_rules")["unwrap_max_step_rad"])


def _require_frozen_modes(rules):
    """Refuse a scorecard that says something this tool does not implement."""
    cfg = rules["tau_L"]
    expectations = (
        (tuple(rules["precedence"]), _PRECEDENCE, "precedence"),
        (rules["stage0_1_source"], "splits_manifest_record_stage", "stage0_1_source"),
        (rules["stage2_source"], "hierarchical_gold_records", "stage2_source"),
        (rules["stage3"]["source"], "standard_base", "stage3.source"),
        (rules["stage3"]["percentile_population"], "training_split_standard_base", "stage3.percentile_population"),
        (rules["stage3"]["E_comparison"], "le", "stage3.E_comparison"),
        (rules["stage3"]["l_ratio_comparison"], "ge", "stage3.l_ratio_comparison"),
        (rules["stage4"]["source"], "standard_base_not_stage3", "stage4.source"),
        (rules["stage5"]["source"], "standard_gold", "stage5.source"),
        (rules["stage5"]["criteria"], "tau_L_gt_2", "stage5.criteria"),
        (rules["stage6"]["rule"], "residual", "stage6.rule"),
        (rules["stage6"]["clause_recorded"], "s_min_lt_0.5_or_abs_E_lt_0.01", "stage6.clause_recorded"),
        (rules["stage1_substages"]["1a"], "E_ge_minus_0.5_and_E_lt_minus_0.1", "stage1_substages.1a"),
        (
            rules["stage1_substages"]["1b"],
            "E_lt_minus_0.5_and_l_ratio_ge_0.1_and_l_ratio_lt_0.5",
            "stage1_substages.1b",
        ),
        (rules["tau_not_computable"], "unlabelled_with_reason", "tau_not_computable"),
        (cfg["positions"], "r_com_ordered", "tau_L.positions"),
        (cfg["time"], "raw_t", "tau_L.time"),
        (cfg["resample"], "linear", "tau_L.resample"),
        (cfg["primary_fit"], "half_pairs", "tau_L.primary_fit"),
        (cfg["non_positive_slope"], "infinite", "tau_L.non_positive_slope"),
        (
            rules["error_growth"],
            "exp_T_over_tau_L_with_T_10_and_1_when_tau_L_infinite",
            "error_growth",
        ),
        (rules["ordering_statistic"], "stage_median", "ordering_statistic"),
        (rules["ordering_agreement"], "spearman_rank_with_average_ties", "ordering_agreement"),
        (rules["picks"]["stage4b"], "median_tau_L_primary", "picks.stage4b"),
        (rules["picks"]["stage6"], "median_s_min_invariant_at_t0", "picks.stage6"),
        (rules["picks"]["nearest"], "abs_value_minus_numpy_median", "picks.nearest"),
        (rules["picks"]["tie_break"], "lowest_id_then_base_before_gold", "picks.tie_break"),
        (rules["picks"]["empty_stage"], "record_no_substitute_without_owner", "picks.empty_stage"),
    )
    for found, wanted, name in expectations:
        if found != wanted:
            raise SurveyHalt(
                f"frozen survey rule {name} is {found!r}, not the {wanted!r} "
                "this tool implements"
            )


# --- the tau_L estimator -----------------------------------------------------


def resample_linear(times, positions, *, dt, t_max):
    """Linear resampling onto 0, dt, ..., t_max. Returns (grid, x) with x shaped (n, 9).

    The record must cover the whole grid. The grid is the output window; every
    input sample is used, so a coarse record is interpolated, not extrapolated.
    """
    stamps = np.asarray(times, dtype=np.float64).reshape(-1)
    series = np.asarray(positions, dtype=np.float64)
    if series.ndim == 3:
        series = series.reshape(series.shape[0], -1)
    if series.ndim != 2 or series.shape[0] != stamps.shape[0] or stamps.shape[0] < 2:
        raise ValueError("times and positions do not describe a series of at least two samples")
    if not np.all(np.isfinite(stamps)) or not np.all(np.isfinite(series)):
        raise ValueError("the record holds a non-finite time or position")
    if not np.all(np.diff(stamps) > 0.0):
        raise ValueError("record times do not strictly increase")
    count = int(math.floor(float(t_max) / float(dt) + 1e-9)) + 1
    grid = np.arange(count, dtype=np.float64) * float(dt)
    if stamps[0] > 1e-9 or stamps[-1] < grid[-1] - 1e-9:
        raise ValueError(
            f"record covers t = {stamps[0]!r} to {stamps[-1]!r}, not the whole window "
            f"0 to {grid[-1]!r}"
        )
    resampled = np.empty((count, series.shape[1]), dtype=np.float64)
    for channel in range(series.shape[1]):
        resampled[:, channel] = np.interp(grid, stamps, series[:, channel])
    return grid, resampled


def delay_embed(x, *, dim, delay):
    """Delay-coordinate embedding. Row i is x[i], x[i + delay], ..., x[i + (dim - 1) delay]."""
    series = np.asarray(x, dtype=np.float64)
    if series.ndim != 2:
        raise ValueError("embedding needs a two-dimensional series")
    rows = series.shape[0] - (int(dim) - 1) * int(delay)
    if rows < 1:
        raise ValueError("the series is too short for the embedding")
    return np.concatenate(
        [series[j * int(delay) : j * int(delay) + rows] for j in range(int(dim))],
        axis=1,
    )


def nearest_neighbours(emb, *, theiler):
    """Index of each row's nearest other row outside the Theiler window.

    The diagonal and every |i - j| <= theiler are excluded. The first index wins
    a tie. A row with no admissible neighbour gets -1 and is left out later.
    """
    points = np.asarray(emb, dtype=np.float64)
    if int(theiler) < 0:
        raise ValueError("the Theiler window is negative")
    if not np.all(np.isfinite(points)):
        raise ValueError("the embedding holds a non-finite value")
    rows = points.shape[0]
    centred = points - points.mean(axis=0)
    squares = np.einsum("ij,ij->i", centred, centred)
    squared = squares[:, None] + squares[None, :] - 2.0 * (centred @ centred.T)
    index = np.arange(rows)
    squared[np.abs(index[:, None] - index[None, :]) <= int(theiler)] = np.inf
    nearest = np.argmin(squared, axis=1).astype(np.int64)
    nearest[~np.isfinite(squared[index, nearest])] = -1
    return nearest


def divergence_curve(emb, nn, *, min_distance, horizon=None):
    """Mean log divergence of each (i, nn[i]) pair at lag k, and the pair count at each k.

    A pair counts at lag k while both i + k and nn[i] + k stay inside the series
    and its distance exceeds min_distance. The curve stops at the first lag with
    no pair. With a horizon, it also stops once at least that many lags are
    computed and the count has fallen under half its lag-0 value: the frozen
    fits read nothing past those two limits. horizon=None computes every lag.
    """
    points = np.asarray(emb, dtype=np.float64)
    neighbours = np.asarray(nn)
    rows = points.shape[0]
    first = np.flatnonzero(neighbours >= 0).astype(np.int64)
    if first.size == 0:
        return np.empty(0, dtype=np.float64), np.empty(0, dtype=np.int64)
    second = neighbours[first].astype(np.int64)
    reach = rows - 1 - np.maximum(first, second)
    order = np.argsort(-reach, kind="stable")
    first, second, reach = first[order], second[order], reach[order]
    negative_reach = -reach
    curve = []
    counts = []
    under_half = False
    lag = 0
    while True:
        usable = int(np.searchsorted(negative_reach, -lag, side="right"))
        if usable == 0:
            break
        gap = points[first[:usable] + lag] - points[second[:usable] + lag]
        distance = np.sqrt(np.einsum("ij,ij->i", gap, gap))
        kept = distance > float(min_distance)
        count = int(np.count_nonzero(kept))
        if count == 0:
            break
        curve.append(float(np.mean(np.log(distance[kept]))))
        counts.append(count)
        if count < counts[0] / 2.0:
            under_half = True
        lag += 1
        if horizon is not None and lag >= int(horizon) and under_half:
            break
    return np.asarray(curve, dtype=np.float64), np.asarray(counts, dtype=np.int64)


def _not_computable(reason, fit_points=0):
    return {
        "status": "not_computable",
        "tau_L": None,
        "slope": None,
        "fit_points": int(fit_points),
        "reason": str(reason),
    }


def fit_lyapunov(div, n_pairs, *, dt, rule, window=None, min_points=2):
    """Straight-line fit of the divergence curve. tau_L is the inverse slope per time unit.

    rule "half_pairs" fits the lags before the first one whose pair count is under
    half its lag-0 count. rule "window" fits the lags with k * dt < window. Fewer
    than min_points gives status not_computable with a reason. A slope of zero or
    less gives status infinite (tau_L = inf).
    """
    curve = np.asarray(div, dtype=np.float64)
    counts = np.asarray(n_pairs)
    if curve.size == 0:
        return _not_computable("the divergence curve is empty")
    if rule == "half_pairs":
        under = np.flatnonzero(counts < counts[0] / 2.0)
        selected = np.arange(int(under[0]) if under.size else curve.size)
    elif rule == "window":
        if window is None:
            raise ValueError("rule window needs a window")
        selected = np.flatnonzero(np.arange(curve.size) * float(dt) < float(window))
    else:
        raise ValueError(f"unknown fit rule {rule!r}")
    if selected.size < int(min_points):
        return _not_computable(
            f"{int(selected.size)} point(s) in the fit range, fewer than {int(min_points)}",
            selected.size,
        )
    steps = selected.astype(np.float64) * float(dt)
    try:
        slope = float(np.polyfit(steps, curve[selected], 1)[0])
    except (np.linalg.LinAlgError, ValueError) as exc:
        return _not_computable(f"the line fit failed: {exc}", selected.size)
    if not math.isfinite(slope):
        return _not_computable("the fitted slope is not finite", selected.size)
    if slope <= 0.0:
        return {
            "status": "infinite",
            "tau_L": math.inf,
            "slope": slope,
            "fit_points": int(selected.size),
            "reason": None,
        }
    return {
        "status": "finite",
        "tau_L": 1.0 / slope,
        "slope": slope,
        "fit_points": int(selected.size),
        "reason": None,
    }


def lyapunov_time(reference, *, rules):
    """tau_L fits for one record: "primary" (half-pairs) and one per sensitivity window.

    Computed on the COM-ordered positions in raw time units, linearly resampled
    to the frozen dt over the frozen window. A record that cannot be resampled
    or yields no usable curve reports not_computable with the reason.
    """
    cfg = rules["tau_L"]
    dt = float(cfg["dt"])
    t_max = float(cfg["t_max"])
    windows = [float(window) for window in cfg["sensitivity_fit_windows"]]
    min_points = int(cfg["min_fit_points"])

    def every_fit(reason):
        fits = {"primary": _not_computable(reason)}
        for window in windows:
            fits[_window_label(window)] = _not_computable(reason)
        return fits

    try:
        _grid, resampled = resample_linear(
            reference.times, reference.positions_com_ordered, dt=dt, t_max=t_max
        )
        embedded = delay_embed(
            resampled, dim=int(cfg["embedding_dim"]), delay=int(cfg["delay"])
        )
        neighbours = nearest_neighbours(embedded, theiler=int(cfg["theiler_window"]))
    except ValueError as exc:
        return every_fit(str(exc))
    horizon = int(math.floor(max(windows) / dt + 1e-6)) + 1
    curve, counts = divergence_curve(
        embedded, neighbours, min_distance=float(cfg["min_distance"]), horizon=horizon
    )
    if curve.size == 0:
        return every_fit(
            "no neighbour pair above the minimum distance outside the Theiler window"
        )
    fits = {
        "primary": fit_lyapunov(
            curve, counts, dt=dt, rule=str(cfg["primary_fit"]), min_points=min_points
        )
    }
    for window in windows:
        fits[_window_label(window)] = fit_lyapunov(
            curve, counts, dt=dt, rule="window", window=window, min_points=min_points
        )
    return fits


def _error_growth(fit, *, horizon):
    """exp(horizon / tau_L); 1 when tau_L is infinite; absent when not computable."""
    if fit["status"] == "not_computable":
        return None
    if fit["status"] == "infinite":
        return 1.0
    exponent = float(horizon) / float(fit["tau_L"])
    return math.inf if exponent > _EXP_LIMIT else math.exp(exponent)


# --- stage labels ------------------------------------------------------------


def stage3_thresholds(rows, *, rules):
    """E and l_ratio percentiles over the training-split standard base rows (linear)."""
    spec = rules["stage3"]
    base = [
        row for row in rows if row["variant"] == "standard" and row["fidelity"] == "base"
    ]
    energies = np.asarray([float(row["E"]) for row in base if _finite(row["E"])])
    ratios = np.asarray([float(row["l_ratio"]) for row in base if _finite(row.get("l_ratio"))])
    if energies.size == 0 or ratios.size == 0:
        raise SurveyHalt("no standard base row has a finite E and l_ratio for the Stage 3 percentiles")
    return {
        "E25": float(np.percentile(energies, float(spec["E_percentile"]), method="linear")),
        "L75": float(np.percentile(ratios, float(spec["l_ratio_percentile"]), method="linear")),
        "E_population": int(energies.size),
        "l_ratio_population": int(ratios.size),
    }


def _tau_view(row, window):
    value_key, status_key = _tau_keys("primary" if window is None else window)
    return row[status_key], row[value_key]


def _stage1_substage(row):
    energy = row.get("E")
    ratio = row.get("l_ratio")
    if _finite(energy) and -0.5 <= float(energy) < -0.1:
        return "1a"
    if (
        _finite(energy)
        and _finite(ratio)
        and float(energy) < -0.5
        and 0.1 <= float(ratio) < 0.5
    ):
        return "1b"
    return "1-none"


def _decision(label, rule, source, *, substage=None, stage3_computable=None, clause=False):
    return {
        "label": label,
        "substage": substage,
        "rule": rule,
        "source": source,
        "stage3_criterion_computable": stage3_computable,
        "stage6_clause": bool(clause),
    }


def assign_stage(row, *, stage3, rules, window=None):
    """Diagnostic stage for one record, with the rule and the source that produced it.

    Ascending precedence from the frozen survey_rules, Stage 6 the residual. A
    record whose tau_L cannot be computed is unlabelled, never pushed into a
    stage. window=None reads the primary tau_L; a window label such as "w1"
    reads that sensitivity fit instead.
    """
    variant = row["variant"]
    fidelity = row["fidelity"]
    energy = row.get("E")
    s_min = row.get("s_min")
    clause = bool(
        _finite(s_min)
        and _finite(energy)
        and (float(s_min) < _STAGE6_S_MIN or abs(float(energy)) < _STAGE6_ABS_E)
    )
    if variant == "hierarchical" and fidelity == "base":
        stage = row.get("manifest_stage")
        if stage in (0, 1):
            label = str(int(stage))
            return _decision(
                label,
                f"splits_manifest_stage_{label}",
                "manifest",
                substage=_stage1_substage(row) if label == "1" else None,
                clause=clause,
            )
        return _decision(UNLABELLED, "manifest_stage_unassigned", "manifest", clause=clause)
    if variant == "hierarchical" and fidelity == "gold":
        return _decision("2", "hierarchical_gold_record", "spec_criterion", clause=clause)
    if variant != "standard" or fidelity not in ("base", "gold"):
        raise SurveyHalt(f"record {variant}/{fidelity} is not one of the four surveyed kinds")
    status, tau = _tau_view(row, window)
    stage4 = rules["stage4"]
    a_gt = float(stage4["a_tau_L_gt"])
    b_gt = float(stage4["b_tau_L_gt"])
    b_le = float(stage4["b_tau_L_le"])
    if fidelity == "gold":
        if status == "not_computable":
            return _decision(UNLABELLED, "tau_L_not_computable", "spec_criterion", clause=clause)
        if float(tau) > b_gt:
            return _decision("5", f"standard_gold_and_tau_L_gt_{b_gt:g}", "spec_criterion", clause=clause)
        return _decision("6", "residual_after_stages_0_to_5", "spec_criterion", clause=clause)
    spec = rules["stage3"]
    q_min = float(spec["Q_min"])
    q_max = float(spec["Q_max"])
    computable = _finite(energy) and _finite(row.get("Q")) and _finite(row.get("l_ratio"))
    if (
        computable
        and float(energy) <= float(stage3["E25"])
        and float(row["l_ratio"]) >= float(stage3["L75"])
        and q_min <= float(row["Q"]) <= q_max
    ):
        return _decision(
            "3",
            f"E_le_E25_and_l_ratio_ge_L75_and_Q_between_{q_min:g}_and_{q_max:g}",
            "spec_criterion",
            stage3_computable=True,
            clause=clause,
        )
    if status == "not_computable":
        return _decision(
            UNLABELLED, "tau_L_not_computable", "spec_criterion",
            stage3_computable=bool(computable), clause=clause,
        )
    if float(tau) > a_gt:
        return _decision(
            "4a", f"tau_L_gt_{a_gt:g}", "spec_criterion",
            stage3_computable=bool(computable), clause=clause,
        )
    if b_gt < float(tau) <= b_le:
        return _decision(
            "4b", f"tau_L_gt_{b_gt:g}_and_le_{b_le:g}", "spec_criterion",
            stage3_computable=bool(computable), clause=clause,
        )
    return _decision(
        "6", "residual_after_stages_0_to_5", "spec_criterion",
        stage3_computable=bool(computable), clause=clause,
    )


# --- picks and ranking -------------------------------------------------------


def pick_median(rows, value_key):
    """The row whose value is nearest np.median of the finite values.

    Ties go to the lowest id, then base before gold. None when no value is finite.
    """
    candidates = [row for row in rows if _finite(row.get(value_key))]
    if not candidates:
        return None
    median = float(np.median(np.asarray([float(row[value_key]) for row in candidates])))
    return min(
        candidates,
        key=lambda row: (
            abs(float(row[value_key]) - median),
            int(row["id"]),
            _FIDELITY_ORDER[row["fidelity"]],
            str(row["variant"]),
        ),
    )


def _average_ranks(values):
    array = np.asarray(values, dtype=np.float64).reshape(-1)
    order = np.argsort(array, kind="mergesort")
    ordered = array[order]
    ranks = np.empty(array.size, dtype=np.float64)
    start = 0
    while start < array.size:
        stop = start
        while stop + 1 < array.size and ordered[stop + 1] == ordered[start]:
            stop += 1
        ranks[order[start : stop + 1]] = 0.5 * (start + stop) + 1.0
        start = stop + 1
    return ranks


def spearman_rank_correlation(a, b):
    """Spearman rank correlation with average ranks for ties. NaN when a side is constant."""
    left = _average_ranks(a)
    right = _average_ranks(b)
    if left.size != right.size or left.size < 2:
        raise ValueError("Spearman needs two equal-length series of at least two values")
    left = left - left.mean()
    right = right - right.mean()
    denominator = math.sqrt(float(np.dot(left, left)) * float(np.dot(right, right)))
    if denominator == 0.0:
        return math.nan
    return float(np.dot(left, right) / denominator)


# --- one system --------------------------------------------------------------


def _hierarchical_measures(gold, key, *, t_max):
    """N_in, N_out and the phase-accuracy figure, from the gold record of one system."""
    inner = inner_revolutions(gold, t_max=t_max)
    outer = outer_revolutions(gold, t_max=t_max)
    limit = _frozen_unwrap_limit()
    if inner["max_step_rad"] >= limit or outer["max_step_rad"] >= limit:
        raise SurveyHalt(
            f"{evidence_io.record_key_str(key)} unwrap step reached {limit} "
            f"(inner {inner['max_step_rad']}, outer {outer['max_step_rad']})"
        )
    n_in = float(inner["turns"])
    if not math.isfinite(n_in) or n_in <= 0.0:
        raise SurveyHalt(f"{evidence_io.record_key_str(key)} inner turn count is not positive")
    return {
        "N_in": n_in,
        "N_out": float(outer["turns"]),
        "phase_accuracy_0.1": phase_accuracy(n_in, 0.1),
        "phase_accuracy_0.01": phase_accuracy(n_in, 0.01),
    }


def _store_tau(row, fits, *, horizon):
    primary = fits["primary"]
    row["tau_L_primary"] = primary["tau_L"]
    row["tau_L_status"] = primary["status"]
    row["tau_L_reason"] = primary["reason"]
    row["fit_points_primary"] = int(primary["fit_points"])
    row["error_growth"] = _error_growth(primary, horizon=horizon)
    for label, fit in fits.items():
        if label == "primary":
            continue
        value_key, status_key = _tau_keys(label)
        row[value_key] = fit["tau_L"]
        row[status_key] = fit["status"]


def _record_row(reference, key, *, rules, t_max, shared):
    row = {name: None for name in CSV_COLUMNS}
    row.update(
        {
            "variant": key.variant,
            "fidelity": key.fidelity,
            "id": int(key.id),
            "manifest_stage": reference.manifest_stage,
            "E": float(reference.E),
            "Q": float(reference.Q),
            "s_min": float(reference.s_min),
            "l_ratio": None if reference.l_ratio is None else float(reference.l_ratio),
        }
    )
    closest, _farthest = separation_range(reference, t_max=t_max)
    acc_min, acc_max = acceleration_range(reference, t_max=t_max)
    row.update(
        closest_approach=float(closest),
        acc_min=float(acc_min),
        acc_max=float(acc_max),
    )
    if shared is not None:
        row.update(shared)
    _store_tau(row, lyapunov_time(reference, rules=rules), horizon=t_max)
    return row


def _load_or_halt(reader, key):
    try:
        return load_reference(reader, key)
    except split_allowlist.NotAdmitted as exc:
        raise SurveyHalt(
            f"{evidence_io.record_key_str(key)} was not admitted ({exc.disposition})"
        ) from exc


def survey_system(reader, allowlist, physical_key, *, rules, record_keys=None):
    """Rows for one physical system: its base record and, when present, its gold record.

    The inner and outer turn counts and the phase-accuracy figure are measured
    once, on the gold record of a hierarchical system, and reported on both of
    its rows. Standard rows leave them empty. Arrays are dropped before return.
    """
    if record_keys is None:
        record_keys = [
            key for key in allowlist.records("train") if key.physical_key == physical_key
        ]
    keys = {key.fidelity: key for key in record_keys}
    if "base" not in keys:
        raise SurveyHalt(f"{evidence_io.record_key_str(physical_key)} has no base record")
    t_max = float(rules["tau_L"]["t_max"])
    shared = None
    if physical_key.variant == "hierarchical":
        if "gold" not in keys:
            raise SurveyHalt(
                f"{evidence_io.record_key_str(physical_key)} has no gold record, "
                "so its inner turns cannot be counted"
            )
        gold = _load_or_halt(reader, keys["gold"])
        try:
            shared = _hierarchical_measures(gold, keys["gold"], t_max=t_max)
        except CensusHalt as exc:
            raise SurveyHalt(f"{evidence_io.record_key_str(keys['gold'])}: {exc}") from exc
        finally:
            del gold
    rows = []
    for fidelity in ("base", "gold"):
        key = keys.get(fidelity)
        if key is None:
            continue
        reference = _load_or_halt(reader, key)
        try:
            rows.append(_record_row(reference, key, rules=rules, t_max=t_max, shared=shared))
        except CensusHalt as exc:
            raise SurveyHalt(f"{evidence_io.record_key_str(key)}: {exc}") from exc
        finally:
            del reference
    return rows


# --- evidence ---------------------------------------------------------------


def _cell(value):
    if value is None:
        return ""
    if isinstance(value, (bool, np.bool_)):
        return "true" if bool(value) else "false"
    if isinstance(value, (float, np.floating)):
        number = float(value)
        if math.isnan(number):
            return "NaN"
        if math.isinf(number):
            return "Infinity" if number > 0 else "-Infinity"
        return repr(number)
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    return str(value)


def survey_csv(rows):
    """Header plus one row per record, in the order given. Floats use repr."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    for row in rows:
        writer.writerow([_cell(row.get(name)) for name in CSV_COLUMNS])
    return buffer.getvalue()


def _summary(values):
    array = np.asarray(
        [float(value) for value in values if _finite(value)], dtype=np.float64
    )
    if array.size == 0:
        return {"n": 0, "min": None, "p10": None, "median": None, "p90": None, "max": None}
    return {
        "n": int(array.size),
        "min": float(array.min()),
        "p10": float(np.percentile(array, 10, method="linear")),
        "median": float(np.percentile(array, 50, method="linear")),
        "p90": float(np.percentile(array, 90, method="linear")),
        "max": float(array.max()),
    }


def _stage_block(stage_rows, label):
    hierarchical = any(row["variant"] == "hierarchical" for row in stage_rows)
    measures = {}
    for name in _MEASURES:
        summary = _summary(row.get(name) for row in stage_rows)
        if name in _HIERARCHICAL_MEASURES and not hierarchical:
            summary["not_applicable"] = NOT_APPLICABLE_HIERARCHICAL
        if name in ("tau_L_primary", "error_growth"):
            summary["n_infinite"] = int(
                sum(1 for row in stage_rows if row.get(name) is not None and math.isinf(row[name]))
            )
        measures[name] = summary
    statuses = [row["tau_L_status"] for row in stage_rows]
    return {
        "count": len(stage_rows),
        "label_source": _LABEL_SOURCES[label],
        "measures": measures,
        "tau_L_counts": {
            "finite": statuses.count("finite"),
            "infinite": statuses.count("infinite"),
            "not_computable": statuses.count("not_computable"),
        },
    }


def _difficulty_ordering(per_stage, precedence):
    position = {label: index for index, label in enumerate(precedence)}
    result = {}
    for measure, direction in _DIRECTIONS:
        medians = {
            label: per_stage[label]["measures"][measure]["median"]
            for label in precedence
            if per_stage[label]["measures"][measure]["n"] > 0
        }
        sign = 1.0 if direction == "larger" else -1.0
        hardness = {label: sign * float(value) for label, value in medians.items()}
        order = sorted(hardness, key=lambda label: (-hardness[label], position[label]))
        rho = None
        if len(hardness) >= 2:
            rho = spearman_rank_correlation(
                [position[label] for label in hardness],
                [hardness[label] for label in hardness],
            )
            rho = rho if math.isfinite(rho) else None
        result[measure] = {
            "harder_is": direction,
            "stage_medians": medians,
            "order_hardest_to_easiest": order,
            "stages_compared": [label for label in precedence if label in hardness],
            "spearman_with_curriculum": rho,
        }
    return result


def _record_name(row):
    return f"{row['variant']}/{row['fidelity']}/{int(row['id'])}"


def _pick_entry(candidates, value_key, *, rule):
    pick = pick_median(candidates, value_key)
    if pick is None:
        return {"no_pick": NO_PICK_REASON}
    values = [float(row[value_key]) for row in candidates if _finite(row.get(value_key))]
    return {
        "record": _record_name(pick),
        "value": float(pick[value_key]),
        "median": float(np.median(np.asarray(values))),
        "rule": rule,
        "n_candidates": len(values),
        "_variant": pick["variant"],
    }


def _sensitivity_entry(window_entry, primary_entry):
    record = window_entry.get("record")
    differs = record != primary_entry.get("record")
    entry = {key: value for key, value in window_entry.items() if not key.startswith("_")}
    entry.pop("rule", None)
    entry["differs_from_primary"] = bool(differs)
    return entry


def _pick_block(rows, labels_by_window, window_labels, *, stage, value_key_for, rule):
    """One FEAS-09 pick, plus the same pick under each sensitivity window."""
    def members(window):
        return [row for row, label in zip(rows, labels_by_window[window]) if label == stage]

    primary = _pick_entry(members("primary"), value_key_for("primary"), rule=rule)
    sensitivity = {}
    for window in window_labels:
        entry = _pick_entry(members(window), value_key_for(window), rule=rule)
        sensitivity[window[1:]] = _sensitivity_entry(entry, primary)
    block = {key: value for key, value in primary.items() if not key.startswith("_")}
    block["sensitivity"] = sensitivity
    return block, primary.get("_variant")


def _sorted_rows(rows, rules):
    order = {
        label: index
        for index, label in enumerate(tuple(rules["precedence"]) + (UNLABELLED,))
    }
    return sorted(
        rows,
        key=lambda row: (
            order[row["stage_label"]],
            row["variant"],
            row["fidelity"],
            int(row["id"]),
        ),
    )


def _fmt(value):
    return format(float(value), ".4g")


def _stage_sentence(label, block):
    count = block["count"]
    if count == 0:
        return None
    measures = block["measures"]
    parts = []
    n_in = measures["N_in"]
    if n_in["n"] > 0:
        parts.append(
            f"a median of {_fmt(n_in['median'])} inner laps by t = 10 "
            f"(10th to 90th percentile {_fmt(n_in['p10'])} to {_fmt(n_in['p90'])})"
        )
    else:
        parts.append("no inner-lap count (no hierarchical split)")
    closest = measures["closest_approach"]
    parts.append(
        f"a median closest approach of {_fmt(closest['median'])} "
        f"(smallest {_fmt(closest['min'])})"
    )
    peak = measures["acc_max"]
    parts.append(f"a median peak acceleration of {_fmt(peak['median'])}")
    tau = measures["tau_L_primary"]
    counts = block["tau_L_counts"]
    growth = measures["error_growth"]
    if tau["n"] > 0 and growth["n"] > 0:
        parts.append(
            f"a median tau_L of {_fmt(tau['median'])} over {tau['n']} finite readings "
            f"({counts['infinite']} infinite, {counts['not_computable']} not computable), "
            f"so a small starting error grows by about {_fmt(growth['median'])} by t = 10"
        )
    else:
        parts.append(
            f"no finite tau_L ({counts['infinite']} infinite, "
            f"{counts['not_computable']} not computable)"
        )
    return f"Stage {label} has {count} records with " + "; ".join(parts) + "."


def _ordering_sentence(measure, entry):
    rho = entry["spearman_with_curriculum"]
    order = ", ".join(entry["order_hardest_to_easiest"]) or "none"
    agree = "undefined" if rho is None else _fmt(rho)
    return (
        f"By {measure} ({entry['harder_is']} is harder) the stages rank {order} from "
        f"hardest to easiest; the Spearman rank correlation with the curriculum order "
        f"is {agree} over {len(entry['stages_compared'])} stages."
    )


def _pick_sentence(name, entry):
    if "no_pick" in entry:
        return f"{name}: {entry['no_pick']}."
    moves = [
        f"{window} time unit(s): {item.get('record', 'no pick')} "
        f"({'differs' if item['differs_from_primary'] else 'same'})"
        for window, item in sorted(entry["sensitivity"].items())
    ]
    return (
        f"{name} probe system is {entry['record']} with value {_fmt(entry['value'])} "
        f"against a stage median of {_fmt(entry['median'])} over {entry['n_candidates']} "
        f"candidates; under the sensitivity fit windows it is {'; '.join(moves)}."
    )


def survey_summary(survey, picks, rules):
    """Plain-language summary. The first heading is fixed."""
    precedence = tuple(rules["precedence"])
    per_stage = survey["per_stage"]
    population = survey["population"]
    stage3 = survey["stage3"]
    lines = [
        "## In plain language",
        "",
        f"This survey reads all {population['total']} training-split records and asks how "
        "hard each stage is: how fast the inner pair spins, how close bodies come, how "
        "violent the accelerations are, and how quickly a small error grows (the "
        "Lyapunov time, tau_L). Every stage label and every tau_L value here is "
        "diagnostic. The official stage mapping beyond Stages 0 and 1 is owner-pending, "
        "and nothing in this survey gates a result.",
        "",
    ]
    for label in precedence + (UNLABELLED,):
        sentence = _stage_sentence(label, per_stage[label]) if label != UNLABELLED else None
        if label == UNLABELLED and per_stage[label]["count"] > 0:
            sentence = (
                f"{per_stage[label]['count']} records are unlabelled because tau_L could "
                "not be computed for them."
            )
        if sentence:
            lines.extend([sentence, ""])
    if per_stage["3"]["count"] == 0:
        q_low, q_high = stage3["Q_range_of_standard_base"]
        lines.extend(
            [
                f"Stage 3 is empty. It needs a virial ratio between {_fmt(stage3['Q_window'][0])} "
                f"and {_fmt(stage3['Q_window'][1])}, and the standard base records span only "
                f"{_fmt(q_low)} to {_fmt(q_high)}.",
                "",
            ]
        )
    for measure, _direction in _DIRECTIONS:
        ordering = survey["difficulty_ordering"]["measures"][measure]
        lines.extend([_ordering_sentence(measure, ordering), ""])
    lines.extend(
        [
            _pick_sentence("The Stage 4b", picks["stage4b"]),
            _pick_sentence("The Stage 6", picks["stage6"]),
            "",
            "Reminder: the labels and tau_L are diagnostic, the official mapping is "
            "owner-pending, and these picks are the pre-declared rule's output, not a "
            "judgment about which system is most informative.",
            "",
            "## Numbers",
            "",
            f"- Records surveyed: {population['total']}",
            f"- Stage 3 records: {per_stage['3']['count']}",
            f"- Unlabelled records: {per_stage[UNLABELLED]['count']}",
            "",
        ]
    )
    return "\n".join(lines)


def build_survey_outputs(rows, scorecard):
    """Everything the survey writes, built in memory from the measured rows."""
    rules = scorecard.section("survey_rules")
    precedence = tuple(rules["precedence"])
    window_labels = [_window_label(window) for window in rules["tau_L"]["sensitivity_fit_windows"]]
    work = [dict(row) for row in rows]
    thresholds = stage3_thresholds(work, rules=rules)
    for row in work:
        decision = assign_stage(row, stage3=thresholds, rules=rules)
        row.update(
            stage_label=decision["label"],
            stage_substage=decision["substage"],
            stage_rule=decision["rule"],
            stage_source=decision["source"],
            stage3_criterion_computable=decision["stage3_criterion_computable"],
            stage6_clause=decision["stage6_clause"],
        )
    work = _sorted_rows(work, rules)
    labels_by_window = {"primary": [row["stage_label"] for row in work]}
    for window in window_labels:
        labels_by_window[window] = [
            assign_stage(row, stage3=thresholds, rules=rules, window=window)["label"]
            for row in work
        ]
    per_stage = {
        label: _stage_block([row for row in work if row["stage_label"] == label], label)
        for label in precedence + (UNLABELLED,)
    }
    base_rows = [row for row in work if row["variant"] == "standard" and row["fidelity"] == "base"]
    q_values = [float(row["Q"]) for row in base_rows if _finite(row["Q"])]
    population = {"total": len(work), "by_variant_and_fidelity": {}}
    for variant in ("hierarchical", "standard"):
        for fidelity in ("base", "gold"):
            population["by_variant_and_fidelity"][f"{variant}/{fidelity}"] = sum(
                1 for row in work if row["variant"] == variant and row["fidelity"] == fidelity
            )
    sensitivity = {}
    for window, labels in labels_by_window.items():
        sensitivity[window] = {
            label: labels.count(label)
            for label in ("3", "4a", "4b", "5", "6", UNLABELLED)
        }
    plain = (
        f"Read-only survey of all {len(work)} training-split records. Each record has a "
        "diagnostic stage label with its rule and source, and each stage is measured for "
        "inner laps, closest approach, acceleration, the Lyapunov time tau_L and the error "
        "growth exp(10 / tau_L). The labels and tau_L are diagnostic, the official stage "
        "mapping beyond Stages 0 and 1 is owner-pending, and nothing here gates a result."
    )
    survey = {
        "schema": "phase59-survey/v1",
        "plain_language": plain,
        "scorecard_sha256": scorecard.sha256,
        "producer_sha256": evidence_io.module_hashes(PRODUCER_MODULES, repo_root=_REPO_ROOT),
        "labels_are_diagnostic": True,
        "official_mapping": "owner_pending",
        "precedence": list(precedence),
        "tau_L_settings": rules["tau_L"],
        "population": population,
        "stage3": {
            "E25": thresholds["E25"],
            "L75": thresholds["L75"],
            "E_population": thresholds["E_population"],
            "l_ratio_population": thresholds["l_ratio_population"],
            "Q_window": [float(rules["stage3"]["Q_min"]), float(rules["stage3"]["Q_max"])],
            "count": per_stage["3"]["count"],
            "Q_range_of_standard_base": [min(q_values), max(q_values)] if q_values else [None, None],
        },
        "per_stage": per_stage,
        "stage1_substages": {
            name: sum(
                1
                for row in work
                if row["stage_label"] == "1" and row["stage_substage"] == name
            )
            for name in ("1a", "1b", "1-none")
        },
        "difficulty_ordering": {
            "statistic": rules["ordering_statistic"],
            "agreement": rules["ordering_agreement"],
            "measures": _difficulty_ordering(per_stage, precedence),
        },
        "sensitivity": sensitivity,
    }
    pick_rules = rules["picks"]
    suffix = f"nearest={pick_rules['nearest']}; tie_break={pick_rules['tie_break']}"
    stage4b, variant_4b = _pick_block(
        work,
        labels_by_window,
        window_labels,
        stage="4b",
        value_key_for=lambda window: _tau_keys(window)[0],
        rule=f"{pick_rules['stage4b']}; {suffix}",
    )
    stage6, variant_6 = _pick_block(
        work,
        labels_by_window,
        window_labels,
        stage="6",
        value_key_for=lambda window: "s_min",
        rule=f"{pick_rules['stage6']}; {suffix}",
    )
    applicability = {}
    for name, variant in (("stage4b", variant_4b), ("stage6", variant_6)):
        if variant == "standard":
            applicability[name] = NOT_APPLICABLE_HIERARCHICAL
    picks = {
        "schema": "phase59-feas09-picks/v1",
        "plain_language": (
            "The two FEAS-09 probe systems chosen by the frozen rule: the training-split "
            "record nearest the median tau_L of Stage 4b and nearest the median t = 0 "
            "minimum separation of Stage 6, with the pick repeated under each tau_L "
            "sensitivity window. The stage labels are diagnostic and the official mapping "
            "is owner-pending."
        ),
        "scorecard_sha256": scorecard.sha256,
        "producer_sha256": evidence_io.module_hashes(PRODUCER_MODULES, repo_root=_REPO_ROOT),
        "stage4b": stage4b,
        "stage6": stage6,
        "formula_applicability": applicability,
    }
    return {
        "rows": work,
        "csv": survey_csv(work),
        "survey": survey,
        "picks": picks,
        "summary": survey_summary(survey, picks, rules),
    }


def write_survey_outputs(
    evidence_dir, outputs, *, data_root, command, utc_started, monotonic_started, preflight
):
    """Write the survey files, then survey.done.json as the last write.

    A run that stops before the marker leaves no marker, so a partial set is
    never accepted. Returns the SHA-256 of every file written.
    """
    directory = Path(evidence_dir)
    directory.mkdir(parents=True, exist_ok=True)
    digests = {}
    digests["survey_records.csv"] = evidence_io.write_text(
        directory / "survey_records.csv", outputs["csv"], data_root=data_root
    )
    digests["survey.json"] = evidence_io.write_json(
        directory / "survey.json", outputs["survey"], data_root=data_root
    )
    digests["picks.json"] = evidence_io.write_json(
        directory / "picks.json", outputs["picks"], data_root=data_root
    )
    digests["summary.md"] = evidence_io.write_text(
        directory / "summary.md", outputs["summary"], data_root=data_root
    )
    digests["files_opened.json"] = evidence_io.write_json(
        directory / "files_opened.json",
        evidence_io.files_opened_record("dataset_survey", outputs["attestation_summary"]),
        data_root=data_root,
    )
    digests["provenance.json"] = evidence_io.write_json(
        directory / "provenance.json",
        evidence_io.provenance_record(
            "dataset_survey",
            command,
            data_root=data_root,
            data_root_source=outputs["data_root_source"],
            utc_started=utc_started,
            monotonic_started=monotonic_started,
        ),
        data_root=data_root,
    )
    evidence_io.write_completion_marker(
        directory,
        "survey",
        command=command,
        utc_started=utc_started,
        utc_finished=datetime.now(timezone.utc).isoformat(),
        elapsed_seconds=time.monotonic() - float(monotonic_started),
        result_paths=[
            directory / name
            for name in (
                "survey_records.csv",
                "survey.json",
                "picks.json",
                "summary.md",
                "files_opened.json",
            )
        ],
        preflight=preflight,
    )
    digests["survey.done.json"] = hashlib.sha256(
        (directory / "survey.done.json").read_bytes()
    ).hexdigest()
    return digests


# --- driving the survey ------------------------------------------------------


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


def _training_systems(allowlist):
    systems = {}
    for key in allowlist.records("train"):
        systems.setdefault(key.physical_key, []).append(key)
    return {physical: tuple(keys) for physical, keys in sorted(systems.items())}


def collect_survey(args):
    """Pass 1: measure every training-split record. No label is assigned yet."""
    scorecard, allowlist, reader, attestation, data_root, source = _open_context(args)
    rules = scorecard.section("survey_rules")
    _require_frozen_modes(rules)
    if float(scorecard.section("scoring_grid")["t_max"]) != float(rules["tau_L"]["t_max"]):
        raise SurveyHalt("scoring_grid.t_max differs from survey_rules.tau_L.t_max")
    systems = _training_systems(allowlist)
    total = len(systems)
    rows = []
    for index, (physical, keys) in enumerate(systems.items(), start=1):
        rows.extend(survey_system(reader, allowlist, physical, rules=rules, record_keys=keys))
        if index == total or index % int(args.progress_every) == 0:
            print(f"survey {index}/{total} systems, {len(rows)} records", file=sys.stderr)
    if len(rows) != EXPECTED_TRAINING_RECORDS:
        raise SurveyHalt(
            f"surveyed {len(rows)} training-split records, expected {EXPECTED_TRAINING_RECORDS}"
        )
    return {
        "scorecard": scorecard,
        "rows": rows,
        "attestation": attestation,
        "data_root": data_root,
        "data_root_source": source,
    }


def _sample_mode(args):
    """Print the first N training systems of each variant as JSON lines. Writes nothing."""
    scorecard, allowlist, reader, _attestation, _root, _source = _open_context(args)
    rules = scorecard.section("survey_rules")
    _require_frozen_modes(rules)
    systems = _training_systems(allowlist)
    chosen = []
    for variant in ("hierarchical", "standard"):
        chosen.extend([key for key in systems if key.variant == variant][: int(args.sample)])
    rows = []
    for physical in chosen:
        rows.extend(
            survey_system(reader, allowlist, physical, rules=rules, record_keys=systems[physical])
        )
    thresholds = stage3_thresholds(rows, rules=rules)
    print(
        "SURVEY-SAMPLE stage 3 percentiles come from the sampled standard base rows only: "
        f"E25 {thresholds['E25']!r} L75 {thresholds['L75']!r}",
        file=sys.stderr,
    )
    for row in rows:
        decision = assign_stage(row, stage3=thresholds, rules=rules)
        row.update(
            stage_label=decision["label"],
            stage_substage=decision["substage"],
            stage_rule=decision["rule"],
            stage_source=decision["source"],
            stage3_criterion_computable=decision["stage3_criterion_computable"],
            stage6_clause=decision["stage6_clause"],
        )
    for row in _sorted_rows(rows, rules):
        print(json.dumps(evidence_io.json_safe(row), sort_keys=True, allow_nan=False))
    return 0


def _compare(path, raw, label):
    if not evidence_io.bytes_identical(path, raw):
        print(f"SURVEY-CHECK-DIFF: {label}", file=sys.stderr)
        return False
    return True


def _assert_opened_zeros(attestation, directory):
    summary = attestation.summary()
    for key in ("test_split_opened", "blocked_attempts", "refused_before_open"):
        if summary.get(key) != 0:
            print(f"SURVEY-CHECK-DIFF: live {key} is {summary.get(key)}", file=sys.stderr)
            return False
    path = directory / "files_opened.json"
    if path.is_file():
        payload = json.loads(path.read_text(encoding="utf-8"))
        for key in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            if payload.get(key) != 0:
                print(f"SURVEY-CHECK-DIFF: files_opened {key}", file=sys.stderr)
                return False
    return True


def _survey_mode(args, *, check, command, started_wall, started, preflight):
    collected = collect_survey(args)
    outputs = build_survey_outputs(collected["rows"], collected["scorecard"])
    directory = _evidence_dir(args, "survey")
    if check:
        same = _compare(directory / "survey_records.csv", outputs["csv"].encode("utf-8"), "survey_records.csv")
        same = _compare(
            directory / "survey.json", evidence_io.canonical_json_bytes(outputs["survey"]), "survey.json"
        ) and same
        same = _compare(
            directory / "picks.json", evidence_io.canonical_json_bytes(outputs["picks"]), "picks.json"
        ) and same
        same = _compare(directory / "summary.md", outputs["summary"].encode("utf-8"), "summary.md") and same
        same = _assert_opened_zeros(collected["attestation"], directory) and same
        if not same:
            return 1
        print("SURVEY-CHECK-OK")
        return 0
    outputs["attestation_summary"] = collected["attestation"].summary()
    outputs["data_root_source"] = collected["data_root_source"]
    write_survey_outputs(
        directory,
        outputs,
        data_root=collected["data_root"],
        command=command,
        utc_started=started_wall,
        monotonic_started=started,
        preflight=preflight,
    )
    return 0


def _refusal_text(exc):
    text = str(exc)
    return text if text.startswith("LAUNCH-REFUSED") else f"LAUNCH-REFUSED: {text}"


def _record_failure(reason, run_id, evidence_root):
    try:
        evidence_io.record_long_step_failure(reason, run_id=run_id, evidence_root=evidence_root)
    except evidence_io.LaunchRefused as exc:
        print(f"SURVEY-LOCK: could not record the failure: {exc}", file=sys.stderr)


def _long_step(args, *, command, started_wall, started):
    step = "survey_check" if args.check else "survey"
    evidence_root = Path(args.evidence_root) if args.evidence_root else None
    try:
        run_id = evidence_io.begin_long_step(
            "survey", step, command=command, evidence_root=evidence_root
        )
    except evidence_io.LaunchRefused as exc:
        print(_refusal_text(exc), file=sys.stderr)
        return 6
    released = False
    try:
        try:
            preflight = evidence_io.memory_preflight(PREFLIGHT_REQUIRED_BYTES)
        except evidence_io.MemoryPreflightError as exc:
            print(f"SURVEY-PREFLIGHT: {exc}", file=sys.stderr)
            released = True
            _record_failure(f"SURVEY-PREFLIGHT: {exc}", run_id, evidence_root)
            return 3
        code = _survey_mode(
            args,
            check=bool(args.check),
            command=command,
            started_wall=started_wall,
            started=started,
            preflight=preflight,
        )
        released = True
        if code == 0:
            evidence_io.end_long_step(run_id, evidence_root=evidence_root)
        else:
            _record_failure(f"{step} finished with exit code {code}", run_id, evidence_root)
        return code
    except BaseException as exc:
        if not released:
            _record_failure(f"{type(exc).__name__}: {exc}", run_id, evidence_root)
        raise


def _parse_args(argv):
    parser = argparse.ArgumentParser(prog="dataset_survey")
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--evidence-root", default=None)
    parser.add_argument("--progress-every", type=int, default=500)
    return parser.parse_args(argv)


def _run(argv, *, started_wall, started):
    args = _parse_args(argv)
    command = [
        "python",
        "-m",
        "pinn.verification.dataset_survey",
        *(sys.argv[1:] if argv is None else [str(item) for item in argv]),
    ]
    try:
        freeze = evidence_io.require_frozen_scorecard(_REPO_ROOT)
    except evidence_io.FreezeNotEstablished as exc:
        print(f"FREEZE-REFUSED: {exc}", file=sys.stderr)
        return 1
    print(f"FREEZE-OK {freeze['freeze_commit']}", file=sys.stderr)
    if int(args.progress_every) < 1:
        raise SurveyHalt("--progress-every must be at least 1")
    if args.sample is not None or args.stdout:
        if args.sample is None or not args.stdout or args.check:
            raise SurveyHalt("--sample and --stdout are a read-only pair")
        if int(args.sample) < 1:
            raise SurveyHalt("--sample must be at least 1")
        return _sample_mode(args)
    return _long_step(args, command=command, started_wall=started_wall, started=started)


def main(argv=None) -> int:
    """Survey CLI. The freeze guard runs before any lock, memory check or corpus read."""
    started_wall = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    try:
        return _run(argv, started_wall=started_wall, started=started)
    except SurveyHalt as exc:
        print(f"SURVEY-HALT: {exc}", file=sys.stderr)
        return 2
    except split_allowlist.SplitRefused as exc:
        print(f"SplitRefused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "CSV_COLUMNS",
    "PRODUCER_MODULES",
    "SurveyHalt",
    "assign_stage",
    "build_survey_outputs",
    "collect_survey",
    "delay_embed",
    "divergence_curve",
    "fit_lyapunov",
    "lyapunov_time",
    "main",
    "nearest_neighbours",
    "pick_median",
    "resample_linear",
    "spearman_rank_correlation",
    "stage3_thresholds",
    "survey_csv",
    "survey_system",
    "write_survey_outputs",
]
