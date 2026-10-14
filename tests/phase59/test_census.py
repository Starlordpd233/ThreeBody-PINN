"""Phase 59 census row, revolution counters, and frozen panel rule.

Synthetic orbits only. No test in this module reads the real corpus.
"""

from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.verification.evidence_io import FreezeNotEstablished
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.stage0_census import (
    CensusHalt,
    assisted_base_revolutions,
    census_row,
    closest_pair_at_t0,
    gold_base_agreement,
    main,
    orbit_normal,
    outer_revolutions,
    phase_accuracy,
    select_panels,
    unwrapped_turns,
)
from tests.phase59._fixtures import hierarchical_circular


def _circular_vectors(turns, samples_per_turn, *, retrograde=False):
    count = int(round(abs(turns) * samples_per_turn))
    sign = -1.0 if retrograde else 1.0
    theta = np.linspace(0.0, sign * turns * 2.0 * np.pi, count + 1)
    vectors = np.stack(
        [np.cos(theta), np.sin(theta), np.zeros_like(theta)],
        axis=1,
    )
    return vectors


def _kepler_reference(eccentricity=0.3, samples_per_period=2.5, periods=8):
    """Eccentric relative Kepler orbit. Time unit is u, so T = 1."""
    mu = 1.0
    semi_major = 1.0
    mean_motion = float(np.sqrt(mu / semi_major**3))
    period = 2.0 * np.pi / mean_motion
    step_count = int(round(periods * samples_per_period))
    times = np.arange(step_count + 1, dtype=np.float64) * (period / samples_per_period)
    mean_anomaly = mean_motion * times
    eccentric = np.array(mean_anomaly, copy=True)
    for _ in range(30):
        eccentric = eccentric - (
            eccentric - eccentricity * np.sin(eccentric) - mean_anomaly
        ) / (1.0 - eccentricity * np.cos(eccentric))
    radius_x = semi_major * (np.cos(eccentric) - eccentricity)
    radius_y = semi_major * np.sqrt(1.0 - eccentricity**2) * np.sin(eccentric)
    eccentric_rate = mean_motion / (1.0 - eccentricity * np.cos(eccentric))
    velocity_x = -semi_major * np.sin(eccentric) * eccentric_rate
    velocity_y = (
        semi_major * np.sqrt(1.0 - eccentricity**2) * np.cos(eccentric) * eccentric_rate
    )
    relative = np.stack([radius_x, radius_y, np.zeros_like(times)], axis=1)
    relative_velocity = np.stack(
        [velocity_x, velocity_y, np.zeros_like(times)],
        axis=1,
    )
    positions = np.zeros((times.size, 3, 3), dtype=np.float64)
    velocities = np.zeros_like(positions)
    positions[:, 0, :] = -0.5 * relative
    positions[:, 1, :] = 0.5 * relative
    velocities[:, 0, :] = -0.5 * relative_velocity
    velocities[:, 1, :] = 0.5 * relative_velocity
    reference = SimpleNamespace(
        times=times,
        positions=positions,
        velocities=velocities,
        masses=np.array([0.5, 0.5, 1.0]),
        inner_pair=(0, 1),
        T=1.0,
    )
    return reference, float(periods)


def _body(times, positions, *, identifier=1, inner_pair=(0, 1), permutation=None):
    count = len(times)
    return SimpleNamespace(
        times=np.asarray(times, dtype=np.float64),
        positions=np.asarray(positions, dtype=np.float64),
        velocities=np.zeros((count, 3, 3), dtype=np.float64),
        masses=np.array([1.0, 1.0, 1.0]),
        inner_pair=tuple(inner_pair),
        permutation=np.arange(3) if permutation is None else np.asarray(permutation),
        T=float(T_CHARACTERISTIC_TIME),
        record_key=SimpleNamespace(id=int(identifier)),
    )


class UnwrapTests(unittest.TestCase):
    def test_fine_circular_orbit_counts_seven_and_a_quarter_turns(self):
        vectors = _circular_vectors(7.25, samples_per_turn=400.0)
        turns, max_step = unwrapped_turns(vectors, np.array([0.0, 0.0, 1.0]))
        self.assertAlmostEqual(turns, 7.25, delta=1e-9)
        self.assertLess(max_step, np.pi)

    def test_retrograde_orbit_is_negative(self):
        vectors = _circular_vectors(7.25, samples_per_turn=400.0, retrograde=True)
        turns, _max_step = unwrapped_turns(vectors, np.array([0.0, 0.0, 1.0]))
        self.assertAlmostEqual(turns, -7.25, delta=1e-9)

    def test_coarse_sampling_reaches_the_alias_bound(self):
        step = 2.0 * np.pi / 0.4
        theta = np.arange(4, dtype=np.float64) * step
        vectors = np.stack([np.cos(theta), np.sin(theta), np.zeros_like(theta)], axis=1)
        _turns, max_step = unwrapped_turns(vectors, np.array([0.0, 0.0, 1.0]))
        # atan2's float image of an exact half-turn sits one ulp under pi.
        self.assertGreaterEqual(max_step, np.nextafter(np.pi, 0.0))


class OuterRevolutionsTests(unittest.TestCase):
    def test_outer_count_stays_fractional(self):
        count = 800
        theta = np.linspace(0.0, 0.6 * 2.0 * np.pi, count)
        positions = np.zeros((count, 3, 3), dtype=np.float64)
        velocities = np.zeros_like(positions)
        positions[:, 0, 0] = -0.1
        positions[:, 1, 0] = 0.1
        positions[:, 2, 0] = np.cos(theta)
        positions[:, 2, 1] = np.sin(theta)
        velocities[:, 2, 0] = -np.sin(theta)
        velocities[:, 2, 1] = np.cos(theta)
        reference = SimpleNamespace(
            times=theta,
            positions=positions,
            velocities=velocities,
            masses=np.array([1.0, 1.0, 1.0]),
            inner_pair=(0, 1),
        )
        result = outer_revolutions(reference, t_max=float(theta[-1]))
        self.assertAlmostEqual(result["turns"], 0.6, delta=1e-9)


class AssistedBaseTests(unittest.TestCase):
    def test_eccentric_orbit_assist_beats_plain_unwrap(self):
        reference, truth = _kepler_reference()
        separation = reference.positions[:, 1, :] - reference.positions[:, 0, :]
        derivative = reference.velocities[:, 1, :] - reference.velocities[:, 0, :]
        normal = orbit_normal(separation[0], derivative[0])
        plain, _max_step = unwrapped_turns(separation, normal)
        assisted = assisted_base_revolutions(reference, t_max=float(reference.times[-1]))
        self.assertLess(abs(assisted - truth) / truth, 0.01)
        self.assertGreater(abs(plain - truth) / truth, 0.10)


class GoldBaseAgreementTests(unittest.TestCase):
    def _pair(self, gold_shift=0.0, perturb=0.0):
        base_times = np.array([0.0, 0.08, 0.16])
        positions = np.zeros((3, 3, 3), dtype=np.float64)
        positions[:, 0, 0] = 2.0
        gold_times = np.linspace(0.0, 0.16, 17) + gold_shift
        gold_positions = np.broadcast_to(positions[0], (gold_times.size, 3, 3)).copy()
        if perturb:
            match = int(np.argmin(np.abs(gold_times - 0.08)))
            gold_positions[match, 0, 0] += perturb
        return (
            _body(base_times, positions),
            _body(gold_times, gold_positions),
        )

    def test_exact_grid_has_zero_deviation(self):
        base, gold = self._pair()
        self.assertEqual(gold_base_agreement(base, gold), 0.0)

    def test_small_shift_scales_by_system_radius(self):
        base, gold = self._pair(perturb=1e-7 * 2.0)
        self.assertAlmostEqual(gold_base_agreement(base, gold), 1e-7, delta=1e-15)

    def test_unmatched_base_time_halts(self):
        base, gold = self._pair(gold_shift=1e-8)
        with self.assertRaises(CensusHalt):
            gold_base_agreement(base, gold)


class PairTrackingTests(unittest.TestCase):
    def test_hierarchical_circular_closest_pair_is_the_inner_pair(self):
        times = np.linspace(0.0, 0.2, 8)
        positions, _velocities = hierarchical_circular(times)
        reference = SimpleNamespace(positions=positions)
        self.assertEqual(closest_pair_at_t0(reference), (0, 1))


class PanelRuleTests(unittest.TestCase):
    def _scorecard(self):
        return load_scorecard()

    def _population(self, count, *, samples=None, n_in=None):
        if n_in is None:
            n_in = np.arange(count, dtype=np.float64)
        if samples is None:
            samples = np.full(count, 10.0)
        return [
            {
                "id": index,
                "N_in": float(n_in[index]),
                "samples_per_inner_period": float(samples[index]),
            }
            for index in range(count)
        ]

    def test_rule_picks_percentiles_ties_and_even_bin_medians(self):
        scorecard = self._scorecard()
        samples = np.full(1812, 10.0)
        samples[181] = 2.999
        samples[182] = 3.0
        rows = self._population(1812, samples=samples)
        validation = list(range(100000, 100227))
        first = select_panels(rows, validation, scorecard=scorecard)
        second = select_panels(rows, validation, scorecard=scorecard)
        self.assertEqual(first, second)
        targets = np.percentile(np.arange(1812, dtype=np.float64), [10, 50, 90], method="linear")
        self.assertEqual(
            [item["target"] for item in first["singles"]],
            [float(target) for target in targets],
        )
        self.assertEqual(first["singles"][0]["id"], 182)
        self.assertEqual(first["singles"][0]["samples_per_inner_period"], 3.0)
        self.assertNotIn(181, [item["id"] for item in first["singles"]])
        self.assertEqual(first["singles"][1]["id"], 905)
        self.assertEqual(
            [item["size"] for item in first["family"]],
            [114] * 4 + [113] * 12,
        )
        family_ids = [item["id"] for item in first["family"]]
        single_ids = [item["id"] for item in first["singles"]]
        self.assertEqual(len(family_ids), len(set(family_ids)))
        self.assertTrue(set(family_ids).isdisjoint(single_ids))
        ordered = sorted(rows, key=lambda row: (row["N_in"], row["id"]))
        first_bin = [ordered[index]["N_in"] for index in range(114)]
        self.assertEqual(len(first_bin), 114)
        self.assertEqual(first["family"][0]["median"], float(np.median(first_bin)))
        self.assertEqual(first["validation"], validation)

    def test_short_population_halts(self):
        rows = self._population(1811)
        with self.assertRaises(CensusHalt):
            select_panels(rows, list(range(227)), scorecard=self._scorecard())

    def test_duplicate_single_halts(self):
        rows = self._population(1812, n_in=np.ones(1812))
        with self.assertRaises(CensusHalt):
            select_panels(
                rows,
                list(range(100000, 100227)),
                scorecard=self._scorecard(),
            )


class PhaseAccuracyTests(unittest.TestCase):
    def test_named_preview_figure(self):
        self.assertEqual(phase_accuracy(18.61, 0.1), 0.1 / (2 * np.pi * 18.61))


class ValidationRowTests(unittest.TestCase):
    def test_validation_row_skips_difficulty_and_panels_read_ids_only(self):
        times = np.array([0.0, 1.0, 2.0])
        positions = np.zeros((3, 3, 3), dtype=np.float64)
        positions[:, 1, 0] = 0.1
        positions[:, 2, 0] = 1.0
        base = _body(times, positions, identifier=7)
        gold = _body(times, positions, identifier=7)
        scorecard = load_scorecard()
        blocked = (
            "inner_revolutions",
            "outer_revolutions",
            "assisted_base_revolutions",
            "separation_range",
            "acceleration_range",
        )
        with patch.multiple(
            "pinn.verification.stage0_census",
            **{name: patch_raise() for name in blocked},
        ):
            row = census_row(base, gold, split="validation", scorecard=scorecard)
        for name in (
            "split",
            "id",
            "inner_pair",
            "closest_pair_t0",
            "pair_tracking_ok",
            "gold_base_max_dev",
            "gold_n_times",
            "base_n_times",
        ):
            self.assertIsNotNone(row[name])
        self.assertEqual(row["split"], "validation")
        self.assertEqual(row["id"], 7)
        self.assertEqual(row["inner_pair"], (0, 1))
        self.assertEqual(row["closest_pair_t0"], (0, 1))
        self.assertTrue(row["pair_tracking_ok"])
        self.assertEqual(row["gold_n_times"], 3)
        self.assertEqual(row["base_n_times"], 3)
        for name in (
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
        ):
            self.assertIsNone(row[name])
        train = [
            {"id": index, "N_in": float(index), "samples_per_inner_period": 10.0}
            for index in range(1812)
        ]
        validation_ids = [row["id"], *range(1000, 1226)]
        panels = select_panels(train, validation_ids, scorecard=scorecard)
        self.assertIn(row["id"], panels["validation"])
        self.assertEqual(len(panels["validation"]), 227)


def patch_raise():
    def _raise(*_args, **_kwargs):
        raise AssertionError("difficulty function called")

    return _raise


class FreezeGuardCallTests(unittest.TestCase):
    def test_every_mode_stops_before_the_reader(self):
        modes = (
            ["--ids", "1", "--stdout"],
            ["--acceptance"],
            [],
            ["--check"],
        )
        for argv in modes:
            with patch(
                "pinn.verification.evidence_io.require_frozen_scorecard",
                side_effect=FreezeNotEstablished("frozen"),
            ), patch(
                "pinn.verification.stage0_census.AllowlistedCorpusReader",
                side_effect=AssertionError("reader built"),
            ):
                code = main(argv)
            self.assertNotEqual(code, 0, argv)


if __name__ == "__main__":
    unittest.main()
