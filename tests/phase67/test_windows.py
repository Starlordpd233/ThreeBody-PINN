"""Plan 67-03: EXP-05 sampled signed-lap windows and same-window baselines.

D-06's window intervention selects each physical prefix at the FIRST EXISTING
gold sample whose cumulative SIGNED inner-pair turns about the census initial
normal reach 1, 2, 5 and 10 laps — the exact float64 gold timestamp is the
endpoint, the retained grid is the loader's exact inclusive mask, the locked
global tau normalization is never rescaled, and no sample is interpolated.
Same-window constant and two-Kepler baselines are re-derived independently
through the frozen score_trajectory and must agree with the harness's own
comparison rows on exactly the selected samples.

Every orbit here is analytic (a planar inner pair with a prescribed separation
angle) or the synthetic Phase 60 corpus; no real corpus record is opened.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import math
import unittest
from types import SimpleNamespace

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.verification.diagnostic_data import (
    DiagnosticDataRefused,
    physical_window,
    validate_window,
)
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import score_trajectory
from pinn.verification.learnability_data import RecordView
from pinn.verification.two_kepler import NotApplicable, two_kepler_prediction

TWO_PI = 2.0 * np.pi
CPU = torch.device("cpu")
MODULE_NAME = "diagnostic_phase67_windows"
HEX64 = __import__("re").compile(r"^[0-9a-f]{64}$")


def _module(case):
    try:
        return importlib.import_module(f"pinn.verification.{MODULE_NAME}")
    except ImportError as exc:
        case.fail(f"pinn.verification.{MODULE_NAME} is missing: {exc}")


def _symbol(case, module, name):
    value = getattr(module, name, None)
    case.assertIsNotNone(value, f"{module.__name__}.{name} is missing")
    return value


def _planar_reference(
    times,
    theta_fn,
    dtheta_fn,
    *,
    radius=1.0,
    outer_distance=4.0,
    masses=(1.0, 1.0, 1.0),
    inner_pair=(0, 1),
):
    """A synthetic gold-like reference: a planar inner pair on a prescribed
    separation angle ``theta(t)`` with derivative ``dtheta(t)``, plus a static
    outer body.

    The census's ordered separation is ``r_second - r_first``; with
    ``dtheta(0) > 0`` the initial normal is ``+z`` and each signed atan2 step
    measures exactly the prescribed angle increment while per-step turns stay
    below half a turn.
    """
    times = np.asarray(times, dtype=np.float64).reshape(-1)
    theta = np.asarray(theta_fn(times), dtype=np.float64).reshape(-1)
    dtheta = np.asarray(dtheta_fn(times), dtype=np.float64).reshape(-1)
    first, second = int(inner_pair[0]), int(inner_pair[1])
    outer = ({0, 1, 2} - {first, second}).pop()
    mass = np.asarray(masses, dtype=np.float64).reshape(3)
    total = float(mass[first] + mass[second])
    separation = np.stack(
        (
            radius * np.cos(theta),
            radius * np.sin(theta),
            np.zeros_like(theta),
        ),
        axis=1,
    )
    separation_rate = np.stack(
        (
            -radius * dtheta * np.sin(theta),
            radius * dtheta * np.cos(theta),
            np.zeros_like(theta),
        ),
        axis=1,
    )
    count = times.size
    positions = np.zeros((count, 3, 3), dtype=np.float64)
    velocities = np.zeros((count, 3, 3), dtype=np.float64)
    positions[:, first, :] = -(mass[second] / total) * separation
    positions[:, second, :] = (mass[first] / total) * separation
    velocities[:, first, :] = -(mass[second] / total) * separation_rate
    velocities[:, second, :] = (mass[first] / total) * separation_rate
    positions[:, outer, :] = np.asarray([outer_distance, 0.0, 0.0])
    return SimpleNamespace(
        times=times,
        positions=positions,
        velocities=velocities,
        masses=mass,
        inner_pair=tuple(int(slot) for slot in inner_pair),
    )


def _uniform(rate_turns):
    """theta/dtheta builders for a uniform angular rate in turns per unit time."""
    return (
        lambda t: TWO_PI * rate_turns * t,
        lambda t: TWO_PI * rate_turns * np.ones_like(t),
    )


def _expected_first_crossing(theta, laps):
    """The earliest index whose analytic signed turns reach each lap count."""
    turns = (theta - theta[0]) / TWO_PI
    return {float(lap): int(np.flatnonzero(turns >= lap)[0]) for lap in laps}


def _windowed_data(reference, endpoint):
    """A loaded-data seam over one reference's exact inclusive window.

    Mirrors the loader's retained fields (``load_diagnostic_data``): the score
    view on the masked grid, ordered masses, and the first in-window snapshot
    as the recorded initial state.
    """
    times = np.asarray(reference.times, dtype=np.float64).reshape(-1)
    positions = np.asarray(reference.positions, dtype=np.float64)
    velocities = np.asarray(reference.velocities, dtype=np.float64)
    masses = np.asarray(reference.masses, dtype=np.float64).reshape(3)
    mask = physical_window(times, endpoint)
    view = RecordView(
        grid="gold",
        times=times[mask],
        positions=positions[mask],
        inner_pair=tuple(int(slot) for slot in reference.inner_pair),
        masses=masses,
    )
    return SimpleNamespace(
        score=view,
        masses=masses,
        true_r0=torch.as_tensor(positions[0], dtype=torch.float64),
        true_v0=torch.as_tensor(velocities[0], dtype=torch.float64),
    )


def _independent_constant_score(data, scorecard):
    """The window-mean constant with zero velocities, scored independently."""
    positions = np.asarray(data.score.positions, dtype=np.float64)
    constant = np.broadcast_to(
        positions.mean(axis=0, keepdims=True), positions.shape
    ).copy()
    return score_trajectory(
        constant,
        np.zeros_like(constant),
        positions,
        np.asarray(data.masses, dtype=np.float64),
        tuple(int(slot) for slot in data.score.inner_pair),
        np.asarray(data.score.times, dtype=np.float64),
        velocity_source="analytic",
        scorecard=scorecard,
        grid=data.score.grid,
    ).to_json_dict()


class LoaderWindowControlTests(unittest.TestCase):
    """The reused loader contracts the prefixes rely on (regression controls)."""

    def test_the_inclusive_mask_keeps_the_endpoint_and_nextafter_below_excludes_it(self):
        times = np.asarray([0.0, 0.5, 1.0, 1.5, 2.0])
        at_endpoint = physical_window(times, 1.0)
        self.assertEqual(
            [int(index) for index in np.flatnonzero(at_endpoint)], [0, 1, 2]
        )
        below = np.nextafter(1.0, -np.inf)
        self.assertEqual(
            [int(index) for index in np.flatnonzero(physical_window(times, below))],
            [0, 1],
        )
        above = np.nextafter(1.0, np.inf)
        self.assertEqual(
            [int(index) for index in np.flatnonzero(physical_window(times, above))],
            [0, 1, 2],
        )

    def test_validate_window_refuses_out_of_domain_lengths(self):
        for bad in (0.0, -1.0, 10.5, float("nan"), float("inf"), True, "1.0", None):
            with self.subTest(bad=bad):
                with self.assertRaises(DiagnosticDataRefused):
                    validate_window(bad)
        self.assertEqual(validate_window(0.5), 0.5)
        self.assertEqual(validate_window(10), 10.0)


class LapPrefixTests(unittest.TestCase):
    """first_lap_prefixes: the earliest signed-crossing gold sample per lap."""

    def test_a_uniform_circular_orbit_prefixes_end_at_the_earliest_signed_crossing(self):
        module = _module(self)
        times = np.linspace(0.0, 10.0, 1001)
        theta_fn, dtheta_fn = _uniform(1.05)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        prefixes = _symbol(self, module, "first_lap_prefixes")(reference)
        self.assertEqual(
            [prefix["requested_laps"] for prefix in prefixes], [1, 2, 5, 10]
        )
        theta = theta_fn(times)
        expected = _expected_first_crossing(theta, (1, 2, 5, 10))
        for prefix in prefixes:
            lap = float(prefix["requested_laps"])
            index = expected[lap]
            retained = times[: index + 1]
            self.assertEqual(prefix["crossing_index"], index, lap)
            self.assertEqual(prefix["preceding_index"], index - 1, lap)
            self.assertEqual(prefix["preceding_time"], float(times[index - 1]), lap)
            self.assertLess(prefix["preceding_turns"], lap, lap)
            self.assertGreaterEqual(prefix["actual_laps"], lap, lap)
            self.assertLess(prefix["actual_laps"], lap + 0.5, lap)
            # The endpoint is the exact float64 gold timestamp of the crossing
            # sample, and the inclusive mask retains exactly the prefix.
            self.assertEqual(prefix["requested_endpoint"], float(times[index]), lap)
            self.assertEqual(
                prefix["last_retained_timestamp"], prefix["requested_endpoint"], lap
            )
            self.assertEqual(prefix["sample_count"], index + 1, lap)
            # No earlier index reaches the requested count.
            earlier = (theta[:index] - theta[0]) / TWO_PI
            self.assertTrue(bool(np.all(earlier < lap)), lap)
            # Hashes: the retained physical grid and the locked global tau.
            self.assertRegex(prefix["physical_times_sha256"], HEX64)
            self.assertRegex(prefix["normalized_tau_sha256"], HEX64)
            self.assertEqual(
                prefix["physical_times_sha256"],
                hashlib.sha256(
                    np.ascontiguousarray(retained, dtype=np.float64).tobytes()
                ).hexdigest(),
                lap,
            )
            tau = 2.0 * (retained / T_CHARACTERISTIC_TIME) - 1.0
            self.assertEqual(
                prefix["normalized_tau_sha256"],
                hashlib.sha256(
                    np.ascontiguousarray(tau, dtype=np.float64).tobytes()
                ).hexdigest(),
                lap,
            )
            # The locked global tau is never rescaled to the shorter prefix.
            self.assertEqual(tau[0], -1.0)
            self.assertNotEqual(tau[-1], 1.0)
            rescaled = 2.0 * (retained / retained[-1]) - 1.0
            self.assertNotEqual(float(tau[-1]), float(rescaled[-1]))
            self.assertTrue(
                bool(np.any(np.abs(tau - rescaled) > 1e-9)),
                "tau matches a prefix-rescaled [-1, 1] grid",
            )
            self.assertLess(prefix["max_step_rad"], math.pi)

    def test_the_selected_endpoint_is_included_exactly_under_nextafter(self):
        module = _module(self)
        times = np.linspace(0.0, 10.0, 1001)
        theta_fn, dtheta_fn = _uniform(1.05)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        prefixes = _symbol(self, module, "first_lap_prefixes")(reference, (1, 2))
        for prefix in prefixes:
            endpoint = float(prefix["requested_endpoint"])
            index = int(prefix["crossing_index"])
            with self.subTest(laps=prefix["requested_laps"]):
                at_endpoint = physical_window(times, endpoint)
                self.assertEqual(int(at_endpoint.sum()), prefix["sample_count"])
                self.assertEqual(int(np.flatnonzero(at_endpoint)[-1]), index)
                below = np.nextafter(endpoint, -np.inf)
                self.assertEqual(
                    int(physical_window(times, below).sum()),
                    prefix["sample_count"] - 1,
                )
                above = np.nextafter(endpoint, np.inf)
                self.assertEqual(
                    int(physical_window(times, above).sum()),
                    prefix["sample_count"],
                )

    def test_a_variable_speed_orbit_matches_the_analytic_turn_counts(self):
        module = _module(self)
        times = np.linspace(0.0, 10.0, 1001)
        rate = 1.05
        wiggle = 0.05
        theta_fn = lambda t: TWO_PI * (rate * t + wiggle * np.sin(TWO_PI * t))
        dtheta_fn = lambda t: TWO_PI * (
            rate + wiggle * TWO_PI * np.cos(TWO_PI * t)
        ) * np.ones_like(t)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        prefixes = _symbol(self, module, "first_lap_prefixes")(reference)
        expected = _expected_first_crossing(theta_fn(times), (1, 2, 5, 10))
        for prefix in prefixes:
            lap = float(prefix["requested_laps"])
            self.assertEqual(prefix["crossing_index"], expected[lap], lap)

    def test_signed_reversals_do_not_count_as_extra_turns(self):
        module = _module(self)
        times = np.linspace(0.0, 10.0, 1001)
        rate = 1.05
        wiggle = 0.3  # theta'(t) < 0 on part of every cycle: real reversals
        theta_fn = lambda t: TWO_PI * (rate * t + wiggle * np.sin(TWO_PI * t))
        dtheta_fn = lambda t: TWO_PI * (
            rate + wiggle * TWO_PI * np.cos(TWO_PI * t)
        ) * np.ones_like(t)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        prefixes = _symbol(self, module, "first_lap_prefixes")(reference, (1,))
        self.assertEqual(len(prefixes), 1)
        prefix = prefixes[0]
        theta = theta_fn(times)
        signed = _expected_first_crossing(theta, (1,))[1.0]
        absolute_turns = np.concatenate(
            ([0.0], np.cumsum(np.abs(np.diff(theta)) / TWO_PI))
        )
        absolute = int(np.flatnonzero(absolute_turns >= 1.0)[0])
        # The reversals are real: absolute turning runs far ahead of signed.
        self.assertLess(absolute, signed)
        self.assertGreater(float(absolute_turns[-1]), float(prefix["actual_laps"]) + 1.0)
        # The prefix is the earliest SIGNED crossing, in chronological order.
        self.assertEqual(prefix["crossing_index"], signed)
        self.assertLess(prefix["preceding_turns"], 1.0)
        self.assertGreaterEqual(prefix["actual_laps"], 1.0)
        self.assertGreater(prefix["crossing_index"], absolute)

    def test_a_crossing_near_the_end_of_the_record_is_selected(self):
        module = _module(self)
        times = np.linspace(0.0, 10.0, 1001)
        theta_fn, dtheta_fn = _uniform(1.05)  # 10.5 total turns; lap 10 at t~9.52
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        prefixes = _symbol(self, module, "first_lap_prefixes")(reference, (10,))
        prefix = prefixes[0]
        expected = _expected_first_crossing(theta_fn(times), (10,))[10.0]
        self.assertEqual(prefix["crossing_index"], expected)
        self.assertGreater(prefix["requested_endpoint"], 9.0)
        self.assertLessEqual(prefix["requested_endpoint"], 10.0)
        self.assertGreaterEqual(prefix["actual_laps"], 10.0)
        self.assertLess(prefix["actual_laps"], 10.5)

    def test_unreached_requested_laps_refuse(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.0, 1001)
        theta_fn, dtheta_fn = _uniform(0.95)  # 9.5 total turns
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        first = _symbol(self, module, "first_lap_prefixes")
        with self.assertRaises(refused) as caught:
            first(reference)  # the default counts include 10 laps
        self.assertIn("10", str(caught.exception))
        prefixes = first(reference, (1, 2, 5))
        self.assertEqual([prefix["requested_laps"] for prefix in prefixes], [1, 2, 5])

    def test_an_endpoint_beyond_the_physical_window_refuses(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.5, 1051)
        theta_fn, dtheta_fn = _uniform(0.98)  # lap 10 crossing lands beyond t=10
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        with self.assertRaises(refused) as caught:
            _symbol(self, module, "first_lap_prefixes")(reference, (10,))
        self.assertIn("window", str(caught.exception))

    def test_duplicate_and_nonincreasing_times_refuse(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        theta_fn, dtheta_fn = _uniform(1.05)
        for label, times in (
            ("duplicate", [0.0, 0.5, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]),
            ("decreasing", [0.0, 0.5, 0.4, 1.0, 1.5, 2.0, 2.5, 3.0]),
        ):
            with self.subTest(label=label):
                reference = _planar_reference(np.asarray(times), theta_fn, dtheta_fn)
                with self.assertRaises(refused):
                    _symbol(self, module, "first_lap_prefixes")(reference, (1,))

    def test_nonfinite_data_refuses_before_any_search(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.0, 101)
        theta_fn, dtheta_fn = _uniform(1.05)
        clean = _planar_reference(times, theta_fn, dtheta_fn)
        for field, value in (
            ("positions", float("nan")),
            ("velocities", float("inf")),
        ):
            with self.subTest(field=field):
                broken = SimpleNamespace(
                    times=clean.times,
                    positions=np.array(clean.positions, dtype=np.float64, copy=True),
                    velocities=np.array(clean.velocities, dtype=np.float64, copy=True),
                    masses=clean.masses,
                    inner_pair=clean.inner_pair,
                )
                getattr(broken, field)[3, 1, 1] = value
                with self.assertRaises(refused):
                    _symbol(self, module, "first_lap_prefixes")(broken, (1,))
        with self.subTest(field="times"):
            broken = SimpleNamespace(**{**clean.__dict__})
            broken_times = np.array(clean.times, copy=True)
            broken_times[4] = float("nan")
            broken.times = broken_times
            with self.assertRaises(refused):
                _symbol(self, module, "first_lap_prefixes")(broken, (1,))
        with self.subTest(field="missing"):
            with self.assertRaises(refused):
                _symbol(self, module, "first_lap_prefixes")(SimpleNamespace(), (1,))

    def test_fewer_than_two_samples_refuse(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        reference = _planar_reference(
            np.asarray([0.0]), lambda t: np.zeros_like(t), lambda t: np.ones_like(t)
        )
        with self.assertRaises(refused):
            _symbol(self, module, "first_lap_prefixes")(reference, (1,))

    def test_an_undefined_orbit_normal_refuses(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.0, 101)
        # Radial separation: s and sdot are parallel, so the census normal is
        # undefined at the first sample.
        positions = np.zeros((times.size, 3, 3), dtype=np.float64)
        velocities = np.zeros((times.size, 3, 3), dtype=np.float64)
        separation = (1.0 + times)[:, None] * np.asarray([1.0, 0.0, 0.0])
        positions[:, 1, :] = separation
        velocities[:, 1, :] = np.asarray([1.0, 0.0, 0.0])
        reference = SimpleNamespace(
            times=times,
            positions=positions,
            velocities=velocities,
            masses=np.asarray([1.0, 1.0, 1.0]),
            inner_pair=(0, 1),
        )
        with self.assertRaises(refused):
            _symbol(self, module, "first_lap_prefixes")(reference, (1,))

    def test_angular_aliasing_refuses_through_the_census_limit(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.0, 11)  # dt = 1.0
        theta_fn, dtheta_fn = _uniform(0.75)  # 1.5*pi per step: at the limit
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        with self.assertRaises(refused) as caught:
            _symbol(self, module, "first_lap_prefixes")(reference, (1,))
        self.assertIn("3.141592653589793", str(caught.exception))

    def test_steps_just_under_the_census_limit_are_admitted(self):
        module = _module(self)
        times = np.linspace(0.0, 10.0, 11)
        theta_fn, dtheta_fn = _uniform(0.495)  # 0.99*pi per step, under the limit
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        prefixes = _symbol(self, module, "first_lap_prefixes")(reference, (1, 2))
        self.assertEqual(len(prefixes), 2)
        for prefix in prefixes:
            self.assertLess(prefix["max_step_rad"], math.pi)

    def test_a_grid_that_cannot_distinguish_requested_laps_refuses(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.0, 11)
        theta_fn, dtheta_fn = _uniform(0.31)  # 0.31 turns per 1.0 step, under pi
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        with self.assertRaises(refused) as caught:
            _symbol(self, module, "first_lap_prefixes")(reference, (1, 1.2))
        self.assertIn("distinguish", str(caught.exception))

    def test_a_record_not_starting_at_physical_zero_refuses(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.1, 10.0, 991)
        theta_fn, dtheta_fn = _uniform(1.05)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        with self.assertRaises(refused):
            _symbol(self, module, "first_lap_prefixes")(reference, (1,))

    def test_lap_count_inputs_are_validated(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.0, 101)
        theta_fn, dtheta_fn = _uniform(1.05)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        first = _symbol(self, module, "first_lap_prefixes")
        for bad in (None, (), 1, True, "1", (True,), (0.5,), (0,), (float("nan"),), (1, 1)):
            with self.subTest(bad=bad):
                with self.assertRaises(refused):
                    first(reference, bad)

    def test_the_rough_planning_duration_is_labelled_and_never_the_endpoint(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowPrefixRefused")
        times = np.linspace(0.0, 10.0, 1001)
        rate = 1.05
        theta_fn, dtheta_fn = _uniform(rate)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        first = _symbol(self, module, "first_lap_prefixes")
        plain = first(reference, (10,))
        self.assertNotIn("rough_planning_duration", plain[0])
        prefixes = first(reference, (10,), census_n_in=10.5)
        self.assertEqual(len(prefixes), 1)
        rough = prefixes[0]["rough_planning_duration"]
        self.assertAlmostEqual(
            rough["value"], 10.0 * T_CHARACTERISTIC_TIME / 10.5, places=12
        )
        self.assertIn("approximate", rough["note"].lower())
        self.assertIn("never the endpoint", rough["note"])
        self.assertNotEqual(rough["value"], prefixes[0]["requested_endpoint"])
        for bad in (True, 0, -1.0, float("nan"), "10.5"):
            with self.subTest(bad=bad):
                with self.assertRaises(refused):
                    first(reference, (10,), census_n_in=bad)

    def test_the_default_lap_counts_are_one_two_five_ten(self):
        module = _module(self)
        times = np.linspace(0.0, 10.0, 1001)
        theta_fn, dtheta_fn = _uniform(1.05)
        reference = _planar_reference(times, theta_fn, dtheta_fn)
        prefixes = _symbol(self, module, "first_lap_prefixes")(reference)
        self.assertEqual(
            [prefix["requested_laps"] for prefix in prefixes], [1, 2, 5, 10]
        )


class SameWindowExpectationTests(unittest.TestCase):
    """same_window_expectations: matched-window baselines, independently checked."""

    @classmethod
    def setUpClass(cls):
        cls.scorecard = load_scorecard()

    def test_short_window_constant_and_kepler_match_independent_recomputation(self):
        module = _module(self)
        first = _symbol(self, module, "first_lap_prefixes")
        expectations = _symbol(self, module, "same_window_expectations")
        times = np.linspace(0.0, 10.0, 1001)
        # Rate 0.3 turns/unit keeps the inner pair Kepler-bound for the frozen
        # formula while staying well under the census unwrap limit per step.
        reference = _planar_reference(times, *_uniform(0.3))
        prefix = first(reference, (1,))[0]
        data = _windowed_data(reference, prefix["requested_endpoint"])
        evidence = expectations(data, scorecard=self.scorecard, prefix=prefix)
        self.assertEqual(evidence["grid"], "gold")
        self.assertEqual(evidence["window"]["first_time"], 0.0)
        self.assertEqual(evidence["window"]["last_time"], prefix["requested_endpoint"])
        self.assertEqual(evidence["window"]["sample_count"], prefix["sample_count"])
        self.assertEqual(evidence["physical_times_sha256"], prefix["physical_times_sha256"])
        self.assertEqual(evidence["normalized_tau_sha256"], prefix["normalized_tau_sha256"])
        self.assertEqual(evidence["masses"], [1.0, 1.0, 1.0])
        self.assertEqual(evidence["inner_pair"], [0, 1])
        self.assertIn("GAP-59-08", evidence["gap_59_08"])
        # The constant row the harness would record equals a third, test-side
        # recomputation on exactly the selected samples.
        direct = _independent_constant_score(data, self.scorecard)
        self.assertIs(evidence["constant"]["agree"], True)
        self.assertEqual(evidence["constant"]["harness"]["score"], direct)
        self.assertEqual(evidence["constant"]["independent"]["score"], direct)
        # A short-window mean is not the full-window mean: the [0, 10] EXP-01
        # constant can never be borrowed for a shorter prefix.
        full_data = _windowed_data(reference, 10.0)
        full_direct = _independent_constant_score(full_data, self.scorecard)
        self.assertNotEqual(direct["E"], full_direct["E"])
        # The frozen two-Kepler formula applies on this bound configuration and
        # agrees between the harness row and the independent call.
        self.assertIs(evidence["two_kepler"]["applicable"], True)
        self.assertIs(evidence["two_kepler"]["agree"], True)
        elapsed = (
            np.asarray(data.score.times, dtype=np.float64)
            - float(np.asarray(data.score.times, dtype=np.float64)[0])
        ) / T_CHARACTERISTIC_TIME
        predicted, predicted_v = two_kepler_prediction(
            data.true_r0.detach().cpu().numpy().astype(np.float64),
            data.true_v0.detach().cpu().numpy().astype(np.float64),
            np.asarray(data.masses, dtype=np.float64),
            tuple(int(slot) for slot in data.score.inner_pair),
            elapsed,
        )
        direct_kepler = score_trajectory(
            predicted,
            predicted_v,
            np.asarray(data.score.positions, dtype=np.float64),
            np.asarray(data.masses, dtype=np.float64),
            tuple(int(slot) for slot in data.score.inner_pair),
            np.asarray(data.score.times, dtype=np.float64),
            velocity_source="analytic",
            scorecard=self.scorecard,
            grid=data.score.grid,
        ).to_json_dict()
        self.assertEqual(evidence["two_kepler"]["harness"]["score"], direct_kepler)
        self.assertEqual(evidence["two_kepler"]["independent"]["score"], direct_kepler)

    def test_formula_nonapplicability_is_explicit_and_never_a_score(self):
        module = _module(self)
        first = _symbol(self, module, "first_lap_prefixes")
        expectations = _symbol(self, module, "same_window_expectations")
        times = np.linspace(0.0, 10.0, 1001)
        # The kinematic planar fixture's inner pair is unbound for the frozen
        # two-Kepler formula: the refusal must stay explicit on both paths.
        reference = _planar_reference(times, *_uniform(1.05))
        prefix = first(reference, (1,))[0]
        data = _windowed_data(reference, prefix["requested_endpoint"])
        evidence = expectations(data, scorecard=self.scorecard, prefix=prefix)
        block = evidence["two_kepler"]
        self.assertIs(block["applicable"], False)
        self.assertEqual(block["harness"]["failure"], "not_applicable")
        self.assertEqual(block["independent"]["failure"], "not_applicable")
        self.assertEqual(block["harness"]["reason"], block["independent"]["reason"])
        self.assertIn("unbound", block["reason"])
        self.assertNotIn("score", block["harness"])
        self.assertNotIn("score", block["independent"])
        self.assertIs(block["agree"], True)

    def test_a_tampered_window_against_the_prefix_refuses(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowExpectationRefused")
        first = _symbol(self, module, "first_lap_prefixes")
        expectations = _symbol(self, module, "same_window_expectations")
        times = np.linspace(0.0, 10.0, 1001)
        reference = _planar_reference(times, *_uniform(0.3))
        prefixes = first(reference, (1, 2))
        # Data loaded on the two-lap window cannot present the one-lap prefix.
        other = _windowed_data(reference, prefixes[1]["requested_endpoint"])
        with self.assertRaises(refused):
            expectations(other, scorecard=self.scorecard, prefix=prefixes[0])

    def test_a_mismatched_grid_hash_refuses(self):
        module = _module(self)
        refused = _symbol(self, module, "WindowExpectationRefused")
        first = _symbol(self, module, "first_lap_prefixes")
        expectations = _symbol(self, module, "same_window_expectations")
        times = np.linspace(0.0, 10.0, 1001)
        reference = _planar_reference(times, *_uniform(0.3))
        prefix = first(reference, (1,))[0]
        data = _windowed_data(reference, prefix["requested_endpoint"])
        # Shift one interior timestamp: the endpoint and sample count still
        # match the prefix, but the retained grid bytes do not.
        tampered_times = np.array(data.score.times, dtype=np.float64, copy=True)
        tampered_times[7] += 1e-6
        data.score = SimpleNamespace(
            grid=data.score.grid,
            times=tampered_times,
            positions=np.array(data.score.positions, dtype=np.float64, copy=True),
            inner_pair=data.score.inner_pair,
            masses=data.score.masses,
        )
        with self.assertRaises(refused) as caught:
            expectations(data, scorecard=self.scorecard, prefix=prefix)
        self.assertIn("grid", str(caught.exception))

    def test_short_window_kepler_scores_differ_from_full_window_scores(self):
        module = _module(self)
        first = _symbol(self, module, "first_lap_prefixes")
        expectations = _symbol(self, module, "same_window_expectations")
        times = np.linspace(0.0, 10.0, 1001)
        reference = _planar_reference(times, *_uniform(0.3))
        prefixes = first(reference, (1, 2))
        short = expectations(
            _windowed_data(reference, prefixes[0]["requested_endpoint"]),
            scorecard=self.scorecard,
            prefix=prefixes[0],
        )
        longer = expectations(
            _windowed_data(reference, prefixes[1]["requested_endpoint"]),
            scorecard=self.scorecard,
            prefix=prefixes[1],
        )
        self.assertIs(short["two_kepler"]["applicable"], True)
        self.assertIs(longer["two_kepler"]["applicable"], True)
        self.assertNotEqual(
            short["two_kepler"]["harness"]["score"]["E"],
            longer["two_kepler"]["harness"]["score"]["E"],
        )
        self.assertNotEqual(
            short["window"]["last_time"], longer["window"]["last_time"]
        )


if __name__ == "__main__":
    unittest.main()
