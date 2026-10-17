"""Phase 59 survey: tau_L estimator, stage rule, pick rule, outputs and guard order.

Synthetic data only. No test in this module reads the real corpus. The literal
transcription of the spec snippet (ctl_instruction.md:1369-1435) lives here and
is used only as the oracle for the vectorized estimator.
"""

from __future__ import annotations

import contextlib
import io
import json
import math
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from pinn.data.types import PhysicalKey, RecordKey
from pinn.verification import dataset_survey, evidence_io, split_allowlist
from pinn.verification.dataset_survey import (
    CSV_COLUMNS,
    NO_PICK_REASON,
    NOT_APPLICABLE_HIERARCHICAL,
    PRODUCER_MODULES,
    SurveyHalt,
    assign_stage,
    build_survey_outputs,
    delay_embed,
    divergence_curve,
    fit_lyapunov,
    lyapunov_time,
    main,
    nearest_neighbours,
    pick_median,
    resample_linear,
    spearman_rank_correlation,
    stage3_thresholds,
    survey_system,
    write_survey_outputs,
)
from pinn.verification.evidence_io import (
    FreezeNotEstablished,
    LaunchRefused,
    MemoryPreflightError,
)
from pinn.verification.feasibility_scorecard import load_scorecard
from tests.phase59._fixtures import hierarchical_circular, lagrange_rotation

DT = 0.01


def literal_lyapunov(positions, dt=0.01, embedding_dim=5, delay=10, theiler_window=100):
    """Loop-for-loop transcription of the spec snippet, with numpy for scipy.

    Only squareform(pdist(...)) is replaced, by an explicit pairwise loop. The
    divergence list, its per-lag pair counts, the iteration bound and the
    neighbour indices are returned so the test can compare each of them.
    """
    if positions.ndim == 1:
        positions = positions[:, np.newaxis]
    n_points = len(positions)
    embedded = np.zeros(
        (n_points - (embedding_dim - 1) * delay, embedding_dim * positions.shape[1])
    )
    for i in range(embedded.shape[0]):
        for j in range(embedding_dim):
            start_idx = i + j * delay
            embedded[i, j * positions.shape[1] : (j + 1) * positions.shape[1]] = positions[
                start_idx
            ]
    size = embedded.shape[0]
    dist_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(i + 1, size):
            value = np.sqrt(np.sum((embedded[i] - embedded[j]) ** 2))
            dist_matrix[i, j] = value
            dist_matrix[j, i] = value
    np.fill_diagonal(dist_matrix, np.inf)
    for i in range(dist_matrix.shape[0]):
        for j in range(
            max(0, i - theiler_window), min(dist_matrix.shape[0], i + theiler_window + 1)
        ):
            dist_matrix[i, j] = np.inf
    neighbor_indices = np.argmin(dist_matrix, axis=1)
    max_iter = n_points - (embedding_dim - 1) * delay - np.max(neighbor_indices)
    divergence = []
    counts = []
    for k in range(max_iter):
        distances = []
        for i in range(len(neighbor_indices)):
            idx1 = i + k
            idx2 = neighbor_indices[i] + k
            if idx1 < embedded.shape[0] and idx2 < embedded.shape[0]:
                dist = np.linalg.norm(embedded[idx1] - embedded[idx2])
                if dist > 1e-9:
                    distances.append(np.log(dist))
        if distances:
            divergence.append(np.mean(distances))
            counts.append(len(distances))
    return {
        "divergence": divergence,
        "counts": counts,
        "max_iter": int(max_iter),
        "neighbours": neighbor_indices,
    }


def synthetic_series(seed, n=300):
    """Three incommensurate sines per channel plus a small fixed-seed random walk."""
    rng = np.random.default_rng(seed)
    t = np.arange(n, dtype=np.float64)
    columns = []
    for channel in range(9):
        amplitude = rng.uniform(0.5, 1.5, 3)
        frequency = np.array(
            [1 / (97.0 + 3 * channel), 1 / (131.0 + 5 * channel), 1 / (173.0 + 7 * channel)]
        )
        phase = rng.uniform(0, 6.28, 3)
        columns.append(
            sum(
                amplitude[q] * np.sin(2 * np.pi * frequency[q] * t + phase[q])
                for q in range(3)
            )
        )
    walk = 0.02 * np.cumsum(rng.standard_normal((n, 9)), axis=0)
    return np.stack(columns, axis=1) + walk


def rules():
    return load_scorecard().section("survey_rules")


class TauLOracleTests(unittest.TestCase):
    def _agree(self, series, *, dim, delay, theiler, minimum_range):
        literal = literal_lyapunov(
            series, dt=DT, embedding_dim=dim, delay=delay, theiler_window=theiler
        )
        # The literal bound must be long enough that a straight-line fit means something.
        self.assertGreaterEqual(literal["max_iter"], minimum_range)
        embedded = delay_embed(series, dim=dim, delay=delay)
        neighbours = nearest_neighbours(embedded, theiler=theiler)
        np.testing.assert_array_equal(neighbours, literal["neighbours"])
        curve, counts = divergence_curve(embedded, neighbours, min_distance=1e-9)
        length = len(literal["divergence"])
        self.assertGreaterEqual(curve.size, length)
        np.testing.assert_allclose(curve[:length], literal["divergence"], rtol=0.0, atol=1e-12)
        np.testing.assert_array_equal(counts[:length], literal["counts"])
        steps = np.arange(length) * DT
        literal_slope = float(np.polyfit(steps, literal["divergence"], 1)[0])
        fit = fit_lyapunov(
            curve, counts, dt=DT, rule="window", window=(length - 0.5) * DT, min_points=2
        )
        self.assertEqual(fit["fit_points"], length)
        self.assertAlmostEqual(fit["slope"] / literal_slope, 1.0, delta=1e-12)

    def test_default_settings_match_the_literal_loop(self):
        self._agree(synthetic_series(2), dim=5, delay=10, theiler=100, minimum_range=10)

    def test_smaller_settings_match_the_literal_loop(self):
        self._agree(synthetic_series(39, n=150), dim=3, delay=4, theiler=12, minimum_range=10)

    def test_the_spec_bound_collapses_where_the_vectorized_curve_does_not(self):
        series = synthetic_series(0)
        literal = literal_lyapunov(series)
        self.assertEqual(literal["max_iter"], 1)
        embedded = delay_embed(series, dim=5, delay=10)
        neighbours = nearest_neighbours(embedded, theiler=100)
        curve, _counts = divergence_curve(embedded, neighbours, min_distance=1e-9)
        self.assertGreater(curve.size, 50)

    def test_horizon_stops_after_the_count_falls_under_half(self):
        series = synthetic_series(0)
        embedded = delay_embed(series, dim=5, delay=10)
        neighbours = nearest_neighbours(embedded, theiler=100)
        full, full_counts = divergence_curve(embedded, neighbours, min_distance=1e-9)
        cut, cut_counts = divergence_curve(
            embedded, neighbours, min_distance=1e-9, horizon=5
        )
        boundary = int(np.flatnonzero(full_counts < full_counts[0] / 2.0)[0])
        self.assertEqual(cut.size, boundary + 1)
        np.testing.assert_array_equal(cut, full[: cut.size])
        np.testing.assert_array_equal(cut_counts, full_counts[: cut.size])

    def test_delay_embedding_rows_are_lagged_copies(self):
        series = np.arange(30, dtype=np.float64).reshape(10, 3)
        embedded = delay_embed(series, dim=3, delay=2)
        self.assertEqual(embedded.shape, (6, 9))
        np.testing.assert_array_equal(embedded[1], np.concatenate([series[1], series[3], series[5]]))
        with self.assertRaises(ValueError):
            delay_embed(series, dim=6, delay=2)

    def test_resample_interpolates_linearly_and_keeps_the_endpoints(self):
        times = np.array([0.0, 0.5, 1.0])
        positions = np.zeros((3, 3, 3))
        positions[:, 0, 0] = [0.0, 1.0, 4.0]
        grid, resampled = resample_linear(times, positions, dt=0.25, t_max=1.0)
        np.testing.assert_allclose(grid, [0.0, 0.25, 0.5, 0.75, 1.0])
        self.assertEqual(resampled.shape, (5, 9))
        np.testing.assert_allclose(resampled[:, 0], [0.0, 0.5, 1.0, 2.5, 4.0])

    def test_resample_uses_samples_past_the_window_and_refuses_a_short_record(self):
        times = np.array([0.0, 0.7, 1.4])
        positions = np.zeros((3, 3, 3))
        positions[:, 0, 0] = [0.0, 7.0, 14.0]
        _grid, resampled = resample_linear(times, positions, dt=0.5, t_max=1.0)
        np.testing.assert_allclose(resampled[:, 0], [0.0, 5.0, 10.0])
        with self.assertRaises(ValueError):
            resample_linear(times[:2], positions[:2], dt=0.5, t_max=1.0)

    def test_neighbours_stay_outside_the_theiler_window_and_empty_rows_are_minus_one(self):
        series = synthetic_series(5, n=80)
        embedded = delay_embed(series, dim=2, delay=3)
        neighbours = nearest_neighbours(embedded, theiler=10)
        index = np.arange(neighbours.size)
        self.assertTrue(np.all(np.abs(neighbours - index) > 10))
        # On this smooth series the nearest admissible row sits right at the window edge,
        # so one step too wide or too narrow a window changes the smallest gap from 11.
        self.assertEqual(int(np.abs(neighbours - index).min()), 11)
        everything = nearest_neighbours(embedded[:15], theiler=20)
        self.assertTrue(np.all(everything == -1))
        curve, counts = divergence_curve(embedded[:15], everything, min_distance=1e-9)
        self.assertEqual((curve.size, counts.size), (0, 0))


class TauLDegenerateTests(unittest.TestCase):
    def test_a_single_point_is_not_computable_with_a_reason(self):
        for rule, window in (("half_pairs", None), ("window", 0.005)):
            fit = fit_lyapunov(
                np.array([0.5, 0.6, 0.7]) if window else np.array([0.5]),
                np.array([10, 9, 8]) if window else np.array([10]),
                dt=DT,
                rule=rule,
                window=window,
                min_points=2,
            )
            self.assertEqual(fit["status"], "not_computable")
            self.assertTrue(fit["reason"])
            self.assertIsNone(fit["tau_L"])

    def test_an_empty_curve_is_not_computable(self):
        fit = fit_lyapunov(
            np.empty(0), np.empty(0, dtype=int), dt=DT, rule="half_pairs", min_points=2
        )
        self.assertEqual(fit["status"], "not_computable")
        self.assertIn("empty", fit["reason"])

    def test_a_decreasing_curve_is_infinite(self):
        steps = np.arange(40) * DT
        fit = fit_lyapunov(
            0.7 - 0.2 * steps, np.full(40, 50), dt=DT, rule="half_pairs", min_points=2
        )
        self.assertEqual(fit["status"], "infinite")
        self.assertTrue(math.isinf(fit["tau_L"]))
        self.assertLess(fit["slope"], 0.0)

    def test_a_quarter_per_time_unit_gives_four(self):
        steps = np.arange(60) * DT
        fit = fit_lyapunov(
            0.25 * steps + 0.3, np.full(60, 50), dt=DT, rule="half_pairs", min_points=2
        )
        self.assertEqual(fit["status"], "finite")
        self.assertAlmostEqual(fit["tau_L"], 4.0, places=9)
        self.assertEqual(fit["fit_points"], 60)

    def test_a_stationary_record_returns_not_computable_without_raising(self):
        reference = SimpleNamespace(
            times=np.linspace(0.0, 10.0, 11),
            positions_com_ordered=np.ones((11, 3, 3)),
        )
        fits = lyapunov_time(reference, rules=rules())
        self.assertEqual(set(fits), {"primary", "w1", "w2", "w3"})
        for fit in fits.values():
            self.assertEqual(fit["status"], "not_computable")
            self.assertIn("minimum distance", fit["reason"])

    def test_a_record_that_stops_before_the_window_is_not_computable(self):
        times = np.linspace(0.0, 5.0, 51)
        reference = SimpleNamespace(
            times=times, positions_com_ordered=np.zeros((51, 3, 3)) + times[:, None, None]
        )
        fits = lyapunov_time(reference, rules=rules())
        for fit in fits.values():
            self.assertEqual(fit["status"], "not_computable")
            self.assertIn("window", fit["reason"])

    def test_a_real_looking_orbit_yields_a_finite_or_infinite_reading(self):
        times = np.arange(0.0, 10.0001, 0.01)
        positions, _velocities = hierarchical_circular(times)
        reference = SimpleNamespace(times=times, positions_com_ordered=positions)
        fits = lyapunov_time(reference, rules=rules())
        self.assertIn(fits["primary"]["status"], ("finite", "infinite"))
        self.assertEqual(fits["primary"]["fit_points"] > 2, True)


class HalfPairsTests(unittest.TestCase):
    def test_the_primary_fit_stops_before_the_first_count_under_half(self):
        counts = np.array([100, 90, 80, 60, 50, 49, 30, 20])
        curve = np.array([0.0, 0.01, 0.02, 0.03, 0.04, 99.0, 150.0, 400.0])
        fit = fit_lyapunov(curve, counts, dt=DT, rule="half_pairs", min_points=2)
        self.assertEqual(fit["fit_points"], 5)
        self.assertAlmostEqual(fit["slope"], 1.0, places=9)
        self.assertAlmostEqual(fit["tau_L"], 1.0, places=9)

    def test_a_count_of_exactly_half_is_still_inside_the_range(self):
        counts = np.array([100, 60, 50, 50, 49])
        fit = fit_lyapunov(
            np.arange(5) * DT, counts, dt=DT, rule="half_pairs", min_points=2
        )
        self.assertEqual(fit["fit_points"], 4)

    def test_without_a_count_under_half_the_whole_curve_is_used(self):
        fit = fit_lyapunov(
            np.arange(7) * DT, np.array([9, 9, 8, 8, 7, 6, 5]), dt=DT, rule="half_pairs",
            min_points=2,
        )
        self.assertEqual(fit["fit_points"], 7)

    def test_window_fits_use_k_times_dt_below_the_window(self):
        curve = np.arange(400) * DT * 0.3
        counts = np.full(400, 10)
        for window, expected in ((1.0, 100), (2.0, 200), (3.0, 300)):
            fit = fit_lyapunov(
                curve, counts, dt=DT, rule="window", window=window, min_points=2
            )
            self.assertEqual(fit["fit_points"], expected, window)
            self.assertAlmostEqual(fit["slope"], 0.3, places=9)

    def test_a_window_longer_than_the_curve_uses_what_exists(self):
        fit = fit_lyapunov(
            np.arange(30) * DT, np.full(30, 4), dt=DT, rule="window", window=3.0, min_points=2
        )
        self.assertEqual(fit["fit_points"], 30)

    def test_an_unknown_rule_is_refused(self):
        with self.assertRaises(ValueError):
            fit_lyapunov(np.arange(5) * DT, np.full(5, 4), dt=DT, rule="whole", min_points=2)


def tau_keys(label):
    if label == "primary":
        return "tau_L_primary", "tau_L_status"
    return f"tau_L_{label}", f"tau_L_{label}_status"


def set_tau(row, label, value):
    value_key, status_key = tau_keys(label)
    row[value_key] = value
    if value is None:
        row[status_key] = "not_computable"
    elif math.isinf(value):
        row[status_key] = "infinite"
    else:
        row[status_key] = "finite"


def make_row(
    variant,
    fidelity,
    ident,
    *,
    manifest_stage="UNASSIGNED",
    E=-8.0,
    Q=0.05,
    s_min=0.3,
    l_ratio=0.02,
    tau=(5.0, 5.0, 5.0, 5.0),
    N_in=None,
):
    row = {name: None for name in CSV_COLUMNS}
    row.update(
        variant=variant,
        fidelity=fidelity,
        id=ident,
        manifest_stage=manifest_stage,
        E=E,
        Q=Q,
        s_min=s_min,
        l_ratio=l_ratio,
        closest_approach=0.01 * (ident + 1),
        acc_min=1.0,
        acc_max=100.0 * (ident + 1),
    )
    if N_in is not None:
        row.update(
            N_in=N_in,
            N_out=1.5,
            **{
                "phase_accuracy_0.1": 0.1 / (2.0 * math.pi * N_in),
                "phase_accuracy_0.01": 0.01 / (2.0 * math.pi * N_in),
            },
        )
    for label, value in zip(("primary", "w1", "w2", "w3"), tau):
        set_tau(row, label, value)
    primary = tau[0]
    row["tau_L_reason"] = "synthetic not computable" if primary is None else None
    row["fit_points_primary"] = 0 if primary is None else 100
    if primary is None:
        row["error_growth"] = None
    elif math.isinf(primary):
        row["error_growth"] = 1.0
    else:
        row["error_growth"] = math.exp(10.0 / primary)
    return row


STAGE3 = {"E25": -9.0, "L75": 0.05}


def standard_base(**kw):
    return make_row("standard", "base", 7, **kw)


def label_of(row, **kw):
    return assign_stage(row, stage3=STAGE3, rules=rules(), **kw)


class StageRuleTests(unittest.TestCase):
    def test_manifest_stages_keep_their_labels_and_sources(self):
        zero = label_of(make_row("hierarchical", "base", 1, manifest_stage=0, E=-8.0, l_ratio=0.6))
        self.assertEqual((zero["label"], zero["source"]), ("0", "manifest"))
        self.assertIn("manifest", zero["rule"])
        self.assertIsNone(zero["substage"])
        one = label_of(make_row("hierarchical", "base", 1, manifest_stage=1, E=-8.0, l_ratio=0.3))
        self.assertEqual((one["label"], one["source"]), ("1", "manifest"))

    def test_stage_one_substages(self):
        def sub(E, l_ratio):
            return label_of(
                make_row("hierarchical", "base", 1, manifest_stage=1, E=E, l_ratio=l_ratio)
            )["substage"]

        self.assertEqual(sub(-0.3, 0.6), "1a")
        self.assertEqual(sub(-0.5, 0.6), "1a")
        self.assertEqual(sub(-3.5, 0.3), "1b")
        self.assertEqual(sub(-3.5, 0.7), "1-none")
        self.assertEqual(sub(-0.1, 0.3), "1-none")
        self.assertEqual(sub(-3.5, None), "1-none")

    def test_an_unassigned_hierarchical_base_record_is_unlabelled(self):
        decision = label_of(make_row("hierarchical", "base", 1, manifest_stage="UNASSIGNED"))
        self.assertEqual(decision["label"], "unlabelled")
        self.assertEqual(decision["source"], "manifest")

    def test_hierarchical_gold_is_stage_two(self):
        decision = label_of(make_row("hierarchical", "gold", 1, tau=(None,) * 4))
        self.assertEqual((decision["label"], decision["source"]), ("2", "spec_criterion"))

    def test_stage_three_bounds_are_inclusive_at_the_virial_window(self):
        def stage(**kw):
            fields = dict(E=-9.0, l_ratio=0.05, Q=1.0, tau=(3.0,) * 4)
            fields.update(kw)
            return label_of(standard_base(**fields))["label"]

        self.assertEqual(stage(Q=0.9), "3")
        self.assertEqual(stage(Q=1.1), "3")
        self.assertEqual(stage(Q=1.0), "3")
        self.assertEqual(stage(Q=0.8999999), "4b")
        self.assertEqual(stage(Q=1.1000001), "4b")
        self.assertEqual(stage(E=-8.999999), "4b")
        self.assertEqual(stage(l_ratio=0.0499999), "4b")

    def test_stage_three_wins_whatever_tau_says(self):
        for tau in (math.inf, None, 1.0, 3.0):
            decision = label_of(standard_base(E=-12.0, l_ratio=0.2, Q=1.0, tau=(tau,) * 4))
            self.assertEqual(decision["label"], "3", tau)

    def test_an_undefined_l_ratio_cannot_satisfy_stage_three_and_is_flagged(self):
        decision = label_of(standard_base(E=-12.0, l_ratio=None, Q=1.0, tau=(3.0,) * 4))
        self.assertEqual(decision["label"], "4b")
        self.assertIs(decision["stage3_criterion_computable"], False)
        defined = label_of(standard_base(E=-1.0, l_ratio=0.2, Q=0.01, tau=(3.0,) * 4))
        self.assertIs(defined["stage3_criterion_computable"], True)

    def test_standard_base_tau_thresholds(self):
        def stage(tau):
            return label_of(standard_base(tau=(tau,) * 4))["label"]

        self.assertEqual(stage(5.0), "4b")
        self.assertEqual(stage(5.0000001), "4a")
        self.assertEqual(stage(2.0), "6")
        self.assertEqual(stage(2.0000001), "4b")
        self.assertEqual(stage(math.inf), "4a")
        self.assertEqual(stage(0.5), "6")
        self.assertEqual(stage(None), "unlabelled")

    def test_standard_gold_tau_thresholds(self):
        def stage(tau):
            return label_of(make_row("standard", "gold", 7, tau=(tau,) * 4))["label"]

        self.assertEqual(stage(2.5), "5")
        self.assertEqual(stage(1.5), "6")
        self.assertEqual(stage(2.0), "6")
        self.assertEqual(stage(math.inf), "5")
        self.assertEqual(stage(None), "unlabelled")

    def test_an_unlabelled_record_names_the_reason_it_could_not_be_staged(self):
        decision = label_of(standard_base(tau=(None,) * 4))
        self.assertEqual(decision["rule"], "tau_L_not_computable")
        self.assertEqual(decision["source"], "spec_criterion")

    def test_a_window_label_reads_the_sensitivity_fit_instead(self):
        row = standard_base(tau=(1.0, 3.0, 6.0, None))
        self.assertEqual(label_of(row)["label"], "6")
        self.assertEqual(label_of(row, window="w1")["label"], "4b")
        self.assertEqual(label_of(row, window="w2")["label"], "4a")
        self.assertEqual(label_of(row, window="w3")["label"], "unlabelled")

    def test_the_stage_six_clause_is_recorded_and_never_decides_the_label(self):
        near = label_of(standard_base(s_min=0.3, E=-8.0, tau=(10.0,) * 4))
        self.assertIs(near["stage6_clause"], True)
        self.assertEqual(near["label"], "4a")
        far = label_of(standard_base(s_min=0.9, E=-8.0, tau=(10.0,) * 4))
        self.assertIs(far["stage6_clause"], False)
        weak = label_of(standard_base(s_min=0.9, E=-0.005, tau=(10.0,) * 4))
        self.assertIs(weak["stage6_clause"], True)

    def test_an_unknown_kind_of_record_halts(self):
        with self.assertRaises(SurveyHalt):
            label_of(make_row("exotic", "base", 1))

    def test_stage_three_percentiles_use_standard_base_rows_only(self):
        rows = [
            standard_base(E=-10.0 + index, l_ratio=0.01 * (index + 1)) for index in range(5)
        ]
        rows[0]["id"] = 1
        rows.append(make_row("hierarchical", "base", 1, E=-500.0, l_ratio=9.0))
        rows.append(make_row("standard", "gold", 1, E=-500.0, l_ratio=9.0))
        rows.append(standard_base(E=-3.0, l_ratio=None))
        thresholds = stage3_thresholds(rows, rules=rules())
        self.assertEqual(thresholds["E_population"], 6)
        self.assertEqual(thresholds["l_ratio_population"], 5)
        expected_e = float(np.percentile([-10, -9, -8, -7, -6, -3], 25))
        self.assertAlmostEqual(thresholds["E25"], expected_e, places=12)
        self.assertAlmostEqual(thresholds["L75"], 0.04, places=12)

    def test_stage_three_percentiles_halt_without_a_standard_base_row(self):
        with self.assertRaises(SurveyHalt):
            stage3_thresholds([make_row("hierarchical", "base", 1)], rules=rules())


class PickRuleTests(unittest.TestCase):
    def _rows(self, values):
        return [
            {"variant": "standard", "fidelity": fidelity, "id": ident, "v": value}
            for ident, fidelity, value in values
        ]

    def test_the_pick_is_the_record_nearest_the_median(self):
        rows = self._rows([(1, "base", 1.0), (2, "base", 2.0), (3, "base", 2.9), (4, "base", 10.0)])
        self.assertEqual(pick_median(rows, "v")["id"], 3)

    def test_an_exact_tie_takes_the_lower_id(self):
        rows = self._rows([(5, "base", 1.0), (9, "base", 2.0), (4, "base", 3.0), (6, "base", 4.0)])
        self.assertEqual(pick_median(rows, "v")["id"], 4)

    def test_an_exact_tie_on_one_id_takes_base_before_gold(self):
        rows = self._rows([(8, "gold", 2.0), (8, "base", 2.0), (9, "base", 3.0)])
        pick = pick_median(rows, "v")
        self.assertEqual((pick["id"], pick["fidelity"]), (8, "base"))

    def test_non_finite_values_are_ignored(self):
        rows = self._rows([(1, "base", math.inf), (2, "base", None), (3, "base", 4.0)])
        self.assertEqual(pick_median(rows, "v")["id"], 3)
        self.assertIsNone(pick_median(self._rows([(1, "base", math.inf), (2, "base", None)]), "v"))
        self.assertIsNone(pick_median([], "v"))

    def test_an_empty_stage_returns_no_pick_with_the_frozen_reason(self):
        entry = dataset_survey._pick_entry([], "tau_L_primary", rule="r")
        self.assertEqual(entry, {"no_pick": NO_PICK_REASON})
        self.assertIn("no substitute without owner sight", NO_PICK_REASON)


class SpearmanTests(unittest.TestCase):
    def test_identical_rankings_give_one_and_reversed_give_minus_one(self):
        self.assertAlmostEqual(spearman_rank_correlation([1, 2, 3, 4], [10, 20, 30, 40]), 1.0, places=12)
        self.assertAlmostEqual(spearman_rank_correlation([1, 2, 3, 4], [40, 30, 20, 10]), -1.0, places=12)

    def test_ties_use_average_ranks(self):
        value = spearman_rank_correlation([1, 2, 2, 3], [1, 2, 3, 4])
        self.assertAlmostEqual(value, 3.0 / math.sqrt(10.0), places=12)

    def test_a_constant_side_is_undefined_and_a_short_series_is_refused(self):
        self.assertTrue(math.isnan(spearman_rank_correlation([1, 2, 3], [5, 5, 5])))
        with self.assertRaises(ValueError):
            spearman_rank_correlation([1], [1])
        with self.assertRaises(ValueError):
            spearman_rank_correlation([1, 2], [1, 2, 3])


def synthetic_rows():
    """A small population of every kind: hierarchical 0..2, standard 0..9 (id 3 has no gold)."""
    rows = []
    for ident, (stage, n_in) in enumerate(((0, 12.0), (0, 18.0), (1, 30.0))):
        for fidelity in ("base", "gold"):
            rows.append(
                make_row(
                    "hierarchical",
                    fidelity,
                    ident,
                    manifest_stage=stage if fidelity == "base" else "UNASSIGNED",
                    E=-8.0 - ident,
                    Q=1.0,
                    s_min=0.05,
                    l_ratio=0.6 if stage == 0 else 0.3,
                    tau=(20.0 + ident,) * 4,
                    N_in=n_in,
                )
            )
    taus = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, math.inf, None]
    for ident, tau in enumerate(taus):
        windows = (tau, 1.0, tau, tau) if ident == 4 else (tau,) * 4
        invariants = dict(
            E=-9.0 + 0.1 * ident, Q=0.01 * (ident + 1), s_min=0.15 + 0.02 * ident,
            l_ratio=0.01 * (ident + 1),
        )
        rows.append(make_row("standard", "base", ident, tau=(tau,) + windows[1:], **invariants))
        if ident != 3:
            rows.append(make_row("standard", "gold", ident, tau=(tau,) + windows[1:], **invariants))
    return rows


class SurveyOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scorecard = load_scorecard()
        cls.outputs = build_survey_outputs(synthetic_rows(), cls.scorecard)

    def test_csv_header_order_cells_and_row_order(self):
        lines = self.outputs["csv"].splitlines()
        self.assertEqual(lines[0].split(","), list(CSV_COLUMNS))
        records = [dict(zip(CSV_COLUMNS, line.split(","))) for line in lines[1:]]
        self.assertEqual(len(records), len(synthetic_rows()))
        order = ["0", "1", "2", "3", "4a", "4b", "5", "6", "unlabelled"]
        positions = [order.index(record["stage_label"]) for record in records]
        self.assertEqual(positions, sorted(positions))
        keys = [(r["stage_label"], r["variant"], r["fidelity"], int(r["id"])) for r in records]
        for left, right in zip(keys, keys[1:]):
            if left[0] == right[0]:
                self.assertLessEqual(left[1:], right[1:])
        infinite = [r for r in records if r["variant"] == "standard" and r["id"] == "8" and r["fidelity"] == "base"]
        self.assertEqual(infinite[0]["tau_L_primary"], "Infinity")
        self.assertEqual(infinite[0]["tau_L_status"], "infinite")
        self.assertEqual(infinite[0]["error_growth"], "1.0")
        missing = [r for r in records if r["variant"] == "standard" and r["id"] == "9" and r["fidelity"] == "base"]
        self.assertEqual(missing[0]["tau_L_primary"], "")
        self.assertEqual(missing[0]["error_growth"], "")
        self.assertEqual(missing[0]["stage_label"], "unlabelled")
        standard = [r for r in records if r["variant"] == "standard"]
        self.assertTrue(all(r["N_in"] == "" for r in standard))
        self.assertTrue(all(r["N_in"] != "" for r in records if r["variant"] == "hierarchical"))
        self.assertIn(infinite[0]["stage6_clause"], ("true", "false"))
        self.assertIn("Infinity", self.outputs["csv"])

    def test_survey_json_headline_fields(self):
        survey = self.outputs["survey"]
        self.assertEqual(survey["schema"], "phase59-survey/v1")
        self.assertTrue(survey["labels_are_diagnostic"])
        self.assertEqual(survey["official_mapping"], "owner_pending")
        self.assertEqual(survey["scorecard_sha256"], self.scorecard.sha256)
        self.assertEqual(survey["population"]["total"], len(synthetic_rows()))
        self.assertEqual(
            survey["population"]["by_variant_and_fidelity"],
            {"hierarchical/base": 3, "hierarchical/gold": 3, "standard/base": 10, "standard/gold": 9},
        )
        self.assertIn("diagnostic", survey["plain_language"])

    def test_producer_hashes_name_the_six_modules_and_match_the_files(self):
        for name in ("survey", "picks"):
            producers = self.outputs[name]["producer_sha256"]
            self.assertEqual(set(producers), set(PRODUCER_MODULES))
        self.assertEqual(
            self.outputs["survey"]["producer_sha256"],
            evidence_io.module_hashes(PRODUCER_MODULES),
        )

    def test_every_stage_is_present_with_a_label_source_and_stage_three_is_reported_empty(self):
        per_stage = self.outputs["survey"]["per_stage"]
        for label in ("0", "1", "2", "3", "4a", "4b", "5", "6", "unlabelled"):
            self.assertIn(label, per_stage)
            self.assertTrue(per_stage[label]["label_source"])
        self.assertEqual(per_stage["3"]["count"], 0)
        stage3 = self.outputs["survey"]["stage3"]
        self.assertEqual(stage3["count"], 0)
        self.assertAlmostEqual(stage3["Q_range_of_standard_base"][0], 0.01, places=12)
        self.assertAlmostEqual(stage3["Q_range_of_standard_base"][1], 0.10, places=12)
        self.assertEqual(stage3["Q_window"], [0.9, 1.1])
        self.assertEqual(per_stage["unlabelled"]["count"], 2)
        self.assertEqual(per_stage["4b"]["count"], 4)
        self.assertEqual(per_stage["6"]["count"], 6)

    def test_stage_measures_summarise_finite_values_and_mark_hierarchical_only_columns(self):
        per_stage = self.outputs["survey"]["per_stage"]
        self.assertEqual(per_stage["0"]["measures"]["N_in"]["n"], 2)
        self.assertAlmostEqual(per_stage["0"]["measures"]["N_in"]["median"], 15.0, places=12)
        self.assertEqual(
            per_stage["4b"]["measures"]["N_in"]["not_applicable"], NOT_APPLICABLE_HIERARCHICAL
        )
        self.assertNotIn("not_applicable", per_stage["0"]["measures"]["N_in"])
        tau_4b = per_stage["4b"]["measures"]["tau_L_primary"]
        self.assertEqual((tau_4b["n"], tau_4b["min"], tau_4b["max"]), (4, 2.5, 5.0))
        self.assertAlmostEqual(tau_4b["median"], 3.5, places=12)
        self.assertEqual(
            per_stage["5"]["tau_L_counts"], {"finite": 4, "infinite": 1, "not_computable": 0}
        )
        self.assertEqual(per_stage["5"]["measures"]["tau_L_primary"]["n_infinite"], 1)
        self.assertEqual(per_stage["unlabelled"]["tau_L_counts"]["not_computable"], 2)
        for name in ("tau_L_primary", "error_growth", "closest_approach", "acc_min", "acc_max"):
            for key in ("n", "min", "p10", "median", "p90", "max"):
                self.assertIn(key, per_stage["4b"]["measures"][name])

    def test_difficulty_ordering_uses_stage_medians_and_a_spearman_figure(self):
        measures = self.outputs["survey"]["difficulty_ordering"]["measures"]
        n_in = measures["N_in"]
        self.assertEqual(n_in["harder_is"], "larger")
        self.assertEqual(n_in["stage_medians"], {"0": 15.0, "1": 30.0, "2": 18.0})
        self.assertEqual(n_in["order_hardest_to_easiest"], ["1", "2", "0"])
        self.assertAlmostEqual(n_in["spearman_with_curriculum"], 0.5, places=12)
        tau = measures["tau_L_primary"]
        self.assertEqual(tau["harder_is"], "smaller")
        self.assertNotIn("3", tau["stage_medians"])
        self.assertEqual(
            set(measures),
            {"N_in", "acc_max", "closest_approach", "tau_L_primary", "error_growth", "phase_accuracy_0.1"},
        )

    def test_stage_one_substages_and_the_sensitivity_counts(self):
        survey = self.outputs["survey"]
        self.assertEqual(survey["stage1_substages"], {"1a": 0, "1b": 1, "1-none": 0})
        sensitivity = survey["sensitivity"]
        self.assertEqual(set(sensitivity), {"primary", "w1", "w2", "w3"})
        self.assertEqual(sensitivity["primary"]["4b"], 4)
        self.assertEqual(sensitivity["w1"]["4b"], 3)
        self.assertEqual(sensitivity["w1"]["6"], 8)
        self.assertEqual(sensitivity["w2"], sensitivity["primary"])

    def test_picks_follow_the_frozen_rule_and_report_the_window_sensitivity(self):
        picks = self.outputs["picks"]
        self.assertEqual(picks["schema"], "phase59-feas09-picks/v1")
        four_b = picks["stage4b"]
        self.assertEqual(four_b["record"], "standard/base/4")
        self.assertEqual(four_b["value"], 3.0)
        self.assertAlmostEqual(four_b["median"], 3.5, places=12)
        self.assertEqual(four_b["n_candidates"], 4)
        self.assertIn("median_tau_L_primary", four_b["rule"])
        self.assertTrue(four_b["sensitivity"]["1"]["differs_from_primary"])
        self.assertEqual(four_b["sensitivity"]["1"]["record"], "standard/base/5")
        self.assertFalse(four_b["sensitivity"]["2"]["differs_from_primary"])
        self.assertFalse(four_b["sensitivity"]["3"]["differs_from_primary"])
        six = picks["stage6"]
        self.assertEqual(six["record"], "standard/base/1")
        self.assertEqual(six["n_candidates"], 6)
        self.assertIn("median_s_min_invariant_at_t0", six["rule"])
        for entry in (four_b, six):
            self.assertEqual(set(entry["sensitivity"]), {"1", "2", "3"})
        self.assertEqual(
            picks["formula_applicability"],
            {"stage4b": NOT_APPLICABLE_HIERARCHICAL, "stage6": NOT_APPLICABLE_HIERARCHICAL},
        )

    def test_an_empty_probe_stage_records_no_pick_and_no_substitute(self):
        rows = [
            row for row in synthetic_rows()
            if not (row["variant"] == "standard" and row["id"] in (3, 4, 5, 6))
        ]
        picks = build_survey_outputs(rows, self.scorecard)["picks"]
        self.assertEqual(picks["stage4b"]["no_pick"], NO_PICK_REASON)
        self.assertNotIn("record", picks["stage4b"])
        self.assertNotIn("stage4b", picks["formula_applicability"])
        self.assertIn("stage6", picks["formula_applicability"])

    def test_summary_opens_in_plain_language_and_states_the_diagnostic_caveat(self):
        summary = self.outputs["summary"]
        headings = [line for line in summary.splitlines() if line.startswith("## ")]
        self.assertEqual(headings[0], "## In plain language")
        self.assertIn("diagnostic", summary)
        self.assertIn("owner-pending", summary)
        self.assertIn("Stage 3 is empty", summary)
        self.assertIn("standard/base/4", summary)
        self.assertNotIn("/Users/", summary)

    def test_building_twice_gives_identical_bytes(self):
        again = build_survey_outputs(synthetic_rows(), self.scorecard)
        self.assertEqual(again["csv"], self.outputs["csv"])
        self.assertEqual(again["summary"], self.outputs["summary"])
        for name in ("survey", "picks"):
            self.assertEqual(
                evidence_io.canonical_json_bytes(again[name]),
                evidence_io.canonical_json_bytes(self.outputs[name]),
            )

    def test_the_serialized_evidence_has_no_home_path_and_infinity_is_a_string(self):
        for name in ("survey", "picks"):
            raw = evidence_io.canonical_json_bytes(self.outputs[name]).decode("ascii")
            self.assertNotIn("/Users/", raw)
            json.loads(raw)
        self.assertEqual(
            evidence_io.canonical_json_bytes({"x": math.inf}).decode("ascii").count("Infinity"), 1
        )


def synthetic_reference(variant, fidelity, ident, *, stage="UNASSIGNED"):
    times = np.arange(0.0, 10.0001, 0.01)
    if variant == "hierarchical":
        positions, velocities = hierarchical_circular(times)
        inner = (0, 1)
    else:
        positions, velocities, _omega = lagrange_rotation(times)
        inner = (0, 1)
    return SimpleNamespace(
        record_key=RecordKey(variant, fidelity, ident),
        times=times,
        positions=positions,
        velocities=velocities,
        positions_com_ordered=positions,
        masses=np.array([1.0, 0.8, 0.6]),
        inner_pair=inner,
        T=1.0,
        E=-8.0,
        Q=0.5,
        s_min=0.1,
        l_ratio=0.55,
        manifest_stage=stage,
    )


class SurveySystemTests(unittest.TestCase):
    def _run(self, variant, fidelities, ident=7):
        references = {
            RecordKey(variant, fidelity, ident): synthetic_reference(
                variant, fidelity, ident, stage=0 if fidelity == "base" else "UNASSIGNED"
            )
            for fidelity in fidelities
        }
        with patch.object(
            dataset_survey, "load_reference", side_effect=lambda reader, key: references[key]
        ):
            return survey_system(
                None, None, PhysicalKey(variant, ident), rules=rules(),
                record_keys=tuple(references),
            )

    def test_a_hierarchical_system_reports_its_gold_lap_count_on_both_rows(self):
        base, gold = self._run("hierarchical", ("base", "gold"))
        self.assertEqual((base["fidelity"], gold["fidelity"]), ("base", "gold"))
        omega_in = math.sqrt(1.8 / 0.1**3)
        expected = omega_in * 10.0 / (2.0 * math.pi)
        self.assertAlmostEqual(base["N_in"] / expected, 1.0, delta=1e-3)
        self.assertEqual(base["N_in"], gold["N_in"])
        self.assertEqual(base["N_out"], gold["N_out"])
        self.assertAlmostEqual(
            base["phase_accuracy_0.1"], dataset_survey.phase_accuracy(base["N_in"], 0.1), places=15
        )
        self.assertEqual(base["manifest_stage"], 0)

    def test_every_row_carries_scalars_tau_fits_and_the_error_growth_rule(self):
        for row in self._run("hierarchical", ("base", "gold")):
            for name in CSV_COLUMNS:
                self.assertIn(name, row)
            self.assertIn(row["tau_L_status"], ("finite", "infinite", "not_computable"))
            for label in ("w1", "w2", "w3"):
                self.assertIn(row[f"tau_L_{label}_status"], ("finite", "infinite", "not_computable"))
            for value in row.values():
                self.assertNotIsInstance(value, np.ndarray)
            if row["tau_L_status"] == "finite":
                self.assertAlmostEqual(
                    row["error_growth"], math.exp(10.0 / row["tau_L_primary"]), places=9
                )
            elif row["tau_L_status"] == "infinite":
                self.assertEqual(row["error_growth"], 1.0)
            else:
                self.assertIsNone(row["error_growth"])
            self.assertGreater(row["closest_approach"], 0.0)
            self.assertLessEqual(row["acc_min"], row["acc_max"])

    def test_standard_rows_leave_the_hierarchical_columns_empty(self):
        rows = self._run("standard", ("base", "gold"))
        for row in rows:
            for name in ("N_in", "N_out", "phase_accuracy_0.1", "phase_accuracy_0.01"):
                self.assertIsNone(row[name], name)

    def test_a_system_without_a_gold_record_gives_one_row(self):
        rows = self._run("standard", ("base",))
        self.assertEqual([row["fidelity"] for row in rows], ["base"])

    def test_a_hierarchical_system_without_gold_halts(self):
        references = {RecordKey("hierarchical", "base", 7): synthetic_reference("hierarchical", "base", 7, stage=0)}
        with patch.object(dataset_survey, "load_reference", side_effect=lambda r, k: references[k]):
            with self.assertRaises(SurveyHalt):
                survey_system(None, None, PhysicalKey("hierarchical", 7), rules=rules(), record_keys=tuple(references))

    def test_a_system_without_a_base_record_halts(self):
        with self.assertRaises(SurveyHalt):
            survey_system(
                None, None, PhysicalKey("standard", 7), rules=rules(),
                record_keys=(RecordKey("standard", "gold", 7),),
            )

    def test_an_aliased_lap_count_halts_instead_of_reporting(self):
        with patch.object(
            dataset_survey, "inner_revolutions",
            return_value={"turns": 5.0, "max_step_rad": math.pi},
        ):
            with self.assertRaises(SurveyHalt):
                self._run("hierarchical", ("base", "gold"))

    def test_a_record_that_was_not_admitted_halts(self):
        key = RecordKey("standard", "base", 7)
        error = split_allowlist.NotAdmitted(key, "reject", ("synthetic",))
        with patch.object(dataset_survey, "load_reference", side_effect=error):
            with self.assertRaises(SurveyHalt):
                survey_system(None, None, PhysicalKey("standard", 7), rules=rules(), record_keys=(key,))


class _Attestation:
    def summary(self):
        return split_allowlist.OpenAttestation("explicit").summary()


FREEZE = {"freeze_commit": "f" * 40, "head": "a" * 40}
PREFLIGHT = {"available_bytes": 3 * 1024**3, "required_bytes": 2 * 1024**3, "source": "vm_stat"}


def collected_for(directory):
    return {
        "scorecard": load_scorecard(),
        "rows": synthetic_rows(),
        "attestation": _Attestation(),
        "data_root": Path(directory) / "data",
        "data_root_source": "explicit",
    }


def run_main(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class GuardOrderTests(unittest.TestCase):
    def test_the_freeze_guard_stops_every_mode_before_the_lock_or_the_reader(self):
        for argv in (["--sample", "2", "--stdout"], [], ["--check"]):
            with patch(
                "pinn.verification.evidence_io.require_frozen_scorecard",
                side_effect=FreezeNotEstablished("frozen"),
            ), patch(
                "pinn.verification.dataset_survey.AllowlistedCorpusReader",
                side_effect=AssertionError("reader built"),
            ), patch(
                "pinn.verification.evidence_io.begin_long_step",
                side_effect=AssertionError("lock taken"),
            ), patch(
                "pinn.verification.evidence_io.memory_preflight",
                side_effect=AssertionError("memory checked"),
            ):
                code, _out, err = run_main(argv)
            self.assertEqual(code, 1, argv)
            self.assertIn("FREEZE-REFUSED", err)

    def test_a_refused_launch_returns_six_before_the_memory_check_or_the_reader(self):
        for argv in ([], ["--check"]):
            calls = []
            with tempfile.TemporaryDirectory() as tmp, patch(
                "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
            ), patch(
                "pinn.verification.evidence_io.begin_long_step",
                side_effect=LaunchRefused(
                    "LAUNCH-REFUSED: diag07/jx02 run abc pid 1 alive true started t"
                ),
            ), patch(
                "pinn.verification.evidence_io.memory_preflight",
                side_effect=lambda *a, **k: calls.append("preflight"),
            ), patch(
                "pinn.verification.dataset_survey.AllowlistedCorpusReader",
                side_effect=AssertionError("reader built"),
            ):
                code, _out, err = run_main(argv + ["--evidence-root", tmp])
                self.assertEqual(list(Path(tmp).rglob("*.json")), [])
            self.assertEqual(code, 6, argv)
            self.assertIn("LAUNCH-REFUSED: diag07/jx02", err)
            self.assertEqual(calls, [])

    def test_a_live_lock_held_by_another_step_is_named_and_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
        ), patch(
            "pinn.verification.evidence_io.memory_preflight",
            side_effect=AssertionError("memory checked"),
        ):
            holder = evidence_io.begin_long_step(
                "diag07", "jx02", command=["jx02"], evidence_root=Path(tmp)
            )
            code, _out, err = run_main(["--evidence-root", tmp])
            lock = Path(tmp) / "logs" / "launch.lock.log"
            self.assertTrue(lock.is_file())
            evidence_io.end_long_step(holder, evidence_root=Path(tmp))
        self.assertEqual(code, 6)
        self.assertIn("LAUNCH-REFUSED: diag07/jx02", err)

    def test_a_memory_shortfall_returns_three_records_the_failure_and_writes_nothing(self):
        for argv in ([], ["--check"]):
            with tempfile.TemporaryDirectory() as tmp, patch(
                "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
            ), patch(
                "pinn.verification.evidence_io.memory_preflight",
                side_effect=MemoryPreflightError("available 1 bytes < required 2147483648 bytes"),
            ), patch(
                "pinn.verification.dataset_survey.AllowlistedCorpusReader",
                side_effect=AssertionError("reader built"),
            ), patch(
                "pinn.verification.evidence_io.write_json", side_effect=AssertionError("wrote")
            ), patch(
                "pinn.verification.evidence_io.write_text", side_effect=AssertionError("wrote")
            ):
                code, _out, err = run_main(argv + ["--evidence-root", tmp])
                failures = (Path(tmp) / "logs" / "launch-failures.log").read_text(encoding="utf-8")
                self.assertFalse((Path(tmp) / "logs" / "launch.lock.log").exists())
                self.assertFalse((Path(tmp) / "survey").exists())
            self.assertEqual(code, 3, argv)
            self.assertIn("SURVEY-PREFLIGHT", err)
            record = json.loads(failures.splitlines()[-1])
            self.assertEqual(record["area"], "survey")
            self.assertIn("SURVEY-PREFLIGHT", record["reason"])

    def test_a_halt_after_the_lock_records_the_failure_with_the_run_id_and_writes_nothing(self):
        for argv, step in (([], "survey"), (["--check"], "survey_check")):
            with tempfile.TemporaryDirectory() as tmp, patch(
                "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
            ), patch(
                "pinn.verification.evidence_io.memory_preflight", return_value=PREFLIGHT
            ), patch(
                "pinn.verification.dataset_survey.collect_survey",
                side_effect=SurveyHalt("boom"),
            ), patch(
                "pinn.verification.evidence_io.write_json", side_effect=AssertionError("wrote")
            ), patch(
                "pinn.verification.evidence_io.write_text", side_effect=AssertionError("wrote")
            ):
                lock_path = Path(tmp) / "logs" / "launch.lock.log"
                real_begin = evidence_io.begin_long_step
                ids = []

                def begin(*args, **kwargs):
                    run_id = real_begin(*args, **kwargs)
                    ids.append(run_id)
                    return run_id

                with patch("pinn.verification.evidence_io.begin_long_step", side_effect=begin):
                    code, _out, err = run_main(argv + ["--evidence-root", tmp])
                failures = (Path(tmp) / "logs" / "launch-failures.log").read_text(encoding="utf-8")
                self.assertFalse(lock_path.exists())
                self.assertFalse((Path(tmp) / "survey").exists())
            self.assertEqual(code, 2, argv)
            self.assertIn("SURVEY-HALT: boom", err)
            record = json.loads(failures.splitlines()[-1])
            self.assertEqual(record["run_id"], ids[0])
            self.assertEqual(record["step"], step)
            self.assertIn("boom", record["reason"])

    def test_an_unexpected_error_after_the_lock_also_releases_it(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
        ), patch(
            "pinn.verification.evidence_io.memory_preflight", return_value=PREFLIGHT
        ), patch(
            "pinn.verification.dataset_survey.collect_survey", side_effect=RuntimeError("odd")
        ):
            with self.assertRaises(RuntimeError):
                run_main(["--evidence-root", tmp])
            self.assertFalse((Path(tmp) / "logs" / "launch.lock.log").exists())
            failures = (Path(tmp) / "logs" / "launch-failures.log").read_text(encoding="utf-8")
            self.assertIn("RuntimeError: odd", failures)

    def test_writes_end_with_the_completion_marker_and_the_lock_is_released_after_it(self):
        events = []
        real_json, real_text = evidence_io.write_json, evidence_io.write_text
        real_begin, real_end = evidence_io.begin_long_step, evidence_io.end_long_step

        def json_spy(path, payload, **kwargs):
            events.append(f"file:{Path(path).name}")
            return real_json(path, payload, **kwargs)

        def text_spy(path, text, **kwargs):
            events.append(f"file:{Path(path).name}")
            return real_text(path, text, **kwargs)

        def begin_spy(*args, **kwargs):
            events.append("lock")
            return real_begin(*args, **kwargs)

        def end_spy(*args, **kwargs):
            events.append("unlock")
            return real_end(*args, **kwargs)

        with tempfile.TemporaryDirectory() as tmp, patch(
            "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
        ), patch(
            "pinn.verification.evidence_io.memory_preflight",
            side_effect=lambda *a, **k: events.append("preflight") or PREFLIGHT,
        ), patch(
            "pinn.verification.dataset_survey.collect_survey",
            side_effect=lambda args: collected_for(tmp),
        ), patch("pinn.verification.evidence_io.write_json", side_effect=json_spy), patch(
            "pinn.verification.evidence_io.write_text", side_effect=text_spy
        ), patch("pinn.verification.evidence_io.begin_long_step", side_effect=begin_spy), patch(
            "pinn.verification.evidence_io.end_long_step", side_effect=end_spy
        ), patch(
            "pinn.verification.dataset_survey.AllowlistedCorpusReader",
            side_effect=AssertionError("reader built"),
        ):
            code, _out, _err = run_main(["--evidence-root", tmp])
            directory = Path(tmp) / "survey"
            self.assertTrue(evidence_io.completion_marker_ok(directory, "survey"))
            marker = json.loads((directory / "survey.done.json").read_text(encoding="utf-8"))
            self.assertEqual(
                set(marker["result_files"]),
                {"survey_records.csv", "survey.json", "picks.json", "summary.md", "files_opened.json"},
            )
            self.assertEqual(marker["preflight"]["required_bytes"], 2147483648)
            self.assertFalse((Path(tmp) / "logs" / "launch.lock.log").exists())
        self.assertEqual(code, 0)
        self.assertEqual(events[:2], ["lock", "preflight"])
        self.assertEqual(events[-2:], ["file:survey.done.json", "unlock"])
        self.assertEqual(
            events[2:-2],
            [
                "file:survey_records.csv",
                "file:survey.json",
                "file:picks.json",
                "file:summary.md",
                "file:files_opened.json",
                "file:provenance.json",
            ],
        )

    def test_check_never_writes_prints_ok_before_the_lock_is_released_and_flags_a_difference(self):
        real_end = evidence_io.end_long_step
        with tempfile.TemporaryDirectory() as tmp, patch(
            "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
        ), patch(
            "pinn.verification.evidence_io.memory_preflight", return_value=PREFLIGHT
        ), patch(
            "pinn.verification.dataset_survey.collect_survey",
            side_effect=lambda args: collected_for(tmp),
        ):
            code, _out, _err = run_main(["--evidence-root", tmp])
            self.assertEqual(code, 0)
            directory = Path(tmp) / "survey"
            before = {p.name: p.read_bytes() for p in directory.iterdir()}
            seen = []
            stdout = io.StringIO()

            def end_spy(*args, **kwargs):
                seen.append("SURVEY-CHECK-OK" in stdout.getvalue())
                return real_end(*args, **kwargs)

            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()), patch(
                "pinn.verification.evidence_io.end_long_step", side_effect=end_spy
            ), patch(
                "pinn.verification.evidence_io.write_json", side_effect=AssertionError("wrote")
            ), patch(
                "pinn.verification.evidence_io.write_text", side_effect=AssertionError("wrote")
            ), patch(
                "pinn.verification.evidence_io.write_completion_marker",
                side_effect=AssertionError("marked"),
            ):
                code = main(["--check", "--evidence-root", tmp])
            self.assertEqual(code, 0)
            self.assertEqual(seen, [True])
            self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})
            self.assertFalse((Path(tmp) / "logs" / "launch.lock.log").exists())
            (directory / "summary.md").write_text("changed\n", encoding="utf-8")
            code, out, err = run_main(["--check", "--evidence-root", tmp])
            self.assertEqual(code, 1)
            self.assertNotIn("SURVEY-CHECK-OK", out)
            self.assertIn("SURVEY-CHECK-DIFF: summary.md", err)
            self.assertFalse((Path(tmp) / "logs" / "launch.lock.log").exists())
            failures = (Path(tmp) / "logs" / "launch-failures.log").read_text(encoding="utf-8")
            self.assertIn("survey_check", failures)

    def test_write_survey_outputs_puts_the_marker_last_and_it_verifies(self):
        order = []
        real_json, real_text = evidence_io.write_json, evidence_io.write_text

        def json_spy(path, payload, **kwargs):
            order.append(Path(path).name)
            return real_json(path, payload, **kwargs)

        def text_spy(path, text, **kwargs):
            order.append(Path(path).name)
            return real_text(path, text, **kwargs)

        with tempfile.TemporaryDirectory() as tmp, patch(
            "pinn.verification.evidence_io.write_json", side_effect=json_spy
        ), patch("pinn.verification.evidence_io.write_text", side_effect=text_spy):
            outputs = build_survey_outputs(synthetic_rows(), load_scorecard())
            outputs["attestation_summary"] = _Attestation().summary()
            outputs["data_root_source"] = "explicit"
            digests = write_survey_outputs(
                Path(tmp) / "survey",
                outputs,
                data_root=Path(tmp) / "data",
                command=["python", "-m", "pinn.verification.dataset_survey"],
                utc_started="2026-10-16T00:00:00+00:00",
                monotonic_started=0.0,
                preflight=PREFLIGHT,
            )
            self.assertTrue(evidence_io.completion_marker_ok(Path(tmp) / "survey", "survey"))
            for name, digest in digests.items():
                self.assertEqual(len(digest), 64, name)
        self.assertEqual(order[-1], "survey.done.json")
        self.assertEqual(
            set(order[:-1]),
            {"survey_records.csv", "survey.json", "picks.json", "summary.md", "files_opened.json", "provenance.json"},
        )
        self.assertEqual(len(order), 7)

    def test_a_stale_marker_is_rejected_when_a_result_file_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            outputs = build_survey_outputs(synthetic_rows(), load_scorecard())
            outputs["attestation_summary"] = _Attestation().summary()
            outputs["data_root_source"] = "explicit"
            directory = Path(tmp) / "survey"
            write_survey_outputs(
                directory, outputs, data_root=Path(tmp) / "data", command=["x"],
                utc_started="2026-10-16T00:00:00+00:00", monotonic_started=0.0, preflight=PREFLIGHT,
            )
            (directory / "picks.json").write_text("{}\n", encoding="utf-8")
            self.assertFalse(evidence_io.completion_marker_ok(directory, "survey"))


class ArgumentTests(unittest.TestCase):
    def test_sample_and_stdout_are_a_read_only_pair(self):
        for argv in (["--sample", "3"], ["--stdout"], ["--check", "--sample", "3", "--stdout"], ["--sample", "0", "--stdout"]):
            with patch(
                "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
            ), patch(
                "pinn.verification.evidence_io.begin_long_step",
                side_effect=AssertionError("lock taken"),
            ), patch(
                "pinn.verification.dataset_survey.AllowlistedCorpusReader",
                side_effect=AssertionError("reader built"),
            ):
                code, _out, err = run_main(argv)
            self.assertEqual(code, 2, argv)
            self.assertIn("SURVEY-HALT", err)

    def test_the_freeze_line_goes_to_stderr_and_a_bad_progress_interval_halts(self):
        with patch(
            "pinn.verification.evidence_io.require_frozen_scorecard", return_value=FREEZE
        ):
            code, out, err = run_main(["--progress-every", "0"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("FREEZE-OK " + "f" * 40, err)

    def test_the_cli_has_no_precision_option(self):
        source = Path(dataset_survey.__file__).read_text(encoding="utf-8")
        self.assertNotIn("--precision", source)


def thaw(value):
    """A deep mutable copy of the scorecard's immutable mappings and tuples."""
    if isinstance(value, Mapping):
        return {key: thaw(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [thaw(item) for item in value]
    return value


class FrozenModeTests(unittest.TestCase):
    def test_a_scorecard_that_says_something_else_is_refused(self):
        frozen = rules()
        self.assertIsNone(dataset_survey._require_frozen_modes(frozen))
        changed = thaw(frozen)
        changed["tau_L"]["primary_fit"] = "window"
        with self.assertRaises(SurveyHalt):
            dataset_survey._require_frozen_modes(changed)
        changed = thaw(frozen)
        changed["precedence"] = ["6", "5", "4b", "4a", "3", "2", "1", "0"]
        with self.assertRaises(SurveyHalt):
            dataset_survey._require_frozen_modes(changed)
        changed = thaw(frozen)
        changed["picks"]["tie_break"] = "highest_id"
        with self.assertRaises(SurveyHalt):
            dataset_survey._require_frozen_modes(changed)


if __name__ == "__main__":
    unittest.main()
