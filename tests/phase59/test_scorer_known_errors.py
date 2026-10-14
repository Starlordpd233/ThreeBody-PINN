"""D-10 known-error tests for the FEAS-01 scorer.

Thresholds and horizon deltas come from the loaded scorecard. This module
does not inline a tier boundary.
"""

from __future__ import annotations

import math
import unittest

import numpy as np

from pinn.verification.feasibility_scorecard import load_scorecard, tier_of
from pinn.verification.feasibility_scorer import (
    FRAME_NAME,
    ScoreResult,
    ScoringInputError,
    eps_h_from_velocities,
    position_errors,
    score_trajectory,
)
from tests.phase59 import _fixtures


def _score(pred, vel, ref, masses, inner_pair, times, scorecard):
    return score_trajectory(
        pred,
        vel,
        ref,
        masses,
        inner_pair,
        times,
        velocity_source="analytic",
        scorecard=scorecard,
        grid="gold",
    )


class SelfTests(unittest.TestCase):
    def test_lagrange_reference_against_itself_is_tier_3(self):
        scorecard = load_scorecard()
        times = np.linspace(0.0, 1.0, 25, dtype=np.float64)
        masses = np.array([1.0, 0.8, 0.6], dtype=np.float64)
        positions, velocities, _omega = _fixtures.lagrange_rotation(times, masses=masses)
        result = _score(positions, velocities, positions, masses, (0, 1), times, scorecard)
        self.assertEqual(result.E, 0.0)
        self.assertEqual(result.e_sys_max, 0.0)
        self.assertEqual(result.e_in_max, 0.0)
        self.assertEqual(result.h_by_delta[0.01], 1.0)
        self.assertEqual(result.h_by_delta[0.1], 1.0)
        self.assertEqual(result.eps_h, eps_h_from_velocities(positions, velocities, masses))
        self.assertEqual(result.tier, 3)
        self.assertEqual(result.velocity_source, "analytic")
        self.assertEqual(result.grid, "gold")

    def test_hierarchical_reference_against_itself_has_zero_position_error(self):
        scorecard = load_scorecard()
        times = np.linspace(0.0, 1.0, 25, dtype=np.float64)
        masses = np.array([1.0, 0.8, 0.6], dtype=np.float64)
        positions, velocities = _fixtures.hierarchical_circular(times, masses=masses)
        result = _score(positions, velocities, positions, masses, (0, 1), times, scorecard)
        self.assertEqual(result.E, 0.0)
        self.assertEqual(result.h_by_delta, {0.01: 1.0, 0.1: 1.0})

    def test_nan_eps_h_serializes_as_sentinel(self):
        result = ScoreResult(
            E=0.0,
            e_sys_max=0.0,
            e_in_max=0.0,
            h=((0.01, 1.0), (0.1, 1.0)),
            eps_h=float("nan"),
            tier=0,
            velocity_source="analytic",
            grid="gold",
            frame="r_prime_u",
            n_times=2,
            R_sys=1.0,
        )
        self.assertEqual(result.to_json_dict()["eps_h"], "NaN")


_MASSES = np.array([1.0, 0.8, 0.6], dtype=np.float64)


class OffsetTests(unittest.TestCase):
    def test_constant_offset_is_system_error_only(self):
        scorecard = load_scorecard()
        times = np.linspace(0.0, 1.0, 21, dtype=np.float64)
        positions, velocities = _fixtures.hierarchical_circular(times, masses=_MASSES)
        offset = np.array([0.003, -0.004, 0.0], dtype=np.float64)
        predicted = positions + offset
        result = _score(predicted, velocities, positions, _MASSES, (0, 1), times, scorecard)
        expected = 0.005 / result.R_sys
        self.assertTrue(np.allclose(result.e_sys_max, expected, rtol=1e-12, atol=0.0))
        e_sys, e_in, _r_sys = position_errors(predicted, positions, (0, 1))
        self.assertTrue(np.allclose(e_sys, expected, rtol=1e-12, atol=0.0))
        self.assertLessEqual(float(np.max(e_in)), 1e-14)
        self.assertTrue(math.isclose(result.E, expected, rel_tol=1e-12, abs_tol=0.0))


class TimeShiftTests(unittest.TestCase):
    def test_rigid_rotation_shift_sets_both_errors(self):
        scorecard = load_scorecard()
        times = np.linspace(0.0, 2.0, 17, dtype=np.float64)
        positions, _velocities, omega = _fixtures.lagrange_rotation(times, masses=_MASSES)
        delta = 0.1 / omega
        shifted, shifted_velocities, _omega = _fixtures.lagrange_rotation(
            times + delta, masses=_MASSES
        )
        result = _score(
            shifted, shifted_velocities, positions, _MASSES, (0, 1), times, scorecard
        )
        expected = 2.0 * math.sin(0.05)
        e_sys, e_in, _r_sys = position_errors(shifted, positions, (0, 1))
        self.assertTrue(np.allclose(e_sys, expected, rtol=0.0, atol=1e-12))
        self.assertTrue(np.allclose(e_in, expected, rtol=0.0, atol=1e-12))
        self.assertTrue(math.isclose(result.E, expected, rel_tol=0.0, abs_tol=1e-12))
        self.assertEqual(result.tier, 1)
        self.assertEqual(result.tier, tier_of(result.E, result.eps_h, scorecard=scorecard))
        self.assertEqual(result.h_by_delta[0.01], 0.0)
        self.assertEqual(result.h_by_delta[0.1], 1.0)


class VelocityScalingTests(unittest.TestCase):
    def test_scaled_velocities_match_vis_viva(self):
        eccentric = getattr(_fixtures, "eccentric_homographic", None)
        expected_fn = getattr(_fixtures, "expected_eps_h_velocity_scaling", None)
        self.assertIsNotNone(eccentric, "eccentric_homographic")
        self.assertIsNotNone(expected_fn, "expected_eps_h_velocity_scaling")
        times, positions, velocities, masses, kinetic, h0 = eccentric()
        scorecard = load_scorecard()
        for kappa in (0.9, 1.1):
            with self.subTest(kappa=kappa):
                result = _score(
                    positions,
                    velocities * kappa,
                    positions,
                    masses,
                    (0, 1),
                    times,
                    scorecard,
                )
                expected = float(expected_fn(kinetic, h0, kappa))
                self.assertEqual(result.E, 0.0)
                self.assertLessEqual(abs(result.eps_h - expected) / abs(expected), 1e-9)


class VacuityGuardTests(unittest.TestCase):
    """The rigid Lagrange rotation cannot test velocity scaling.

    Its kinetic energy and every pairwise distance are constant, so
    multiplying the velocities by 1.1 rescales H by a constant and leaves
    eps_H at roundoff. The eccentric homographic fixture is the real test.
    """

    def test_rigid_rotation_velocity_scale_is_vacuous(self):
        scorecard = load_scorecard()
        times = np.linspace(0.0, 1.0, 33, dtype=np.float64)
        positions, velocities, _omega = _fixtures.lagrange_rotation(times, masses=_MASSES)
        result = _score(
            positions, velocities * 1.1, positions, _MASSES, (0, 1), times, scorecard
        )
        self.assertLessEqual(result.eps_h, 1e-12)


class InnerPairPhaseTests(unittest.TestCase):
    def test_inner_phase_exceeds_the_system_error(self):
        rotate = getattr(_fixtures, "rotate_inner_pair", None)
        self.assertIsNotNone(rotate, "rotate_inner_pair")
        scorecard = load_scorecard()
        times = np.linspace(0.0, 1.0, 21, dtype=np.float64)
        masses = _MASSES
        a_in = 0.1
        positions, velocities = _fixtures.hierarchical_circular(
            times, masses=masses, a_in=a_in
        )
        phi = 0.2
        predicted = rotate(positions, masses, (0, 1), phi)
        result = _score(predicted, velocities, positions, masses, (0, 1), times, scorecard)
        e_in_expected = 2.0 * math.sin(0.1)
        e_sys_expected = (
            max(float(masses[0]), float(masses[1]))
            / (float(masses[0]) + float(masses[1]))
            * a_in
            * e_in_expected
            / result.R_sys
        )
        _e_sys, e_in, _r_sys = position_errors(predicted, positions, (0, 1))
        self.assertTrue(np.allclose(e_in, e_in_expected, rtol=0.0, atol=1e-12))
        self.assertTrue(
            math.isclose(result.e_sys_max, e_sys_expected, rel_tol=1e-12, abs_tol=0.0)
        )
        self.assertLess(result.e_sys_max, result.e_in_max)
        self.assertEqual(result.E, result.e_in_max)


class FrameInvarianceTests(unittest.TestCase):
    def test_raw_and_scaled_frames_agree(self):
        # A constant 5% scale of the rigid orbit leaves both eps_H values at
        # roundoff, so the required relative check cannot pass and cannot
        # catch a crossed frame. The same 1.05 radial factor is applied in
        # both frames on the later half of the native times.
        scorecard = load_scorecard()
        dual = _fixtures.dual_frame()
        later = dual.times_raw >= np.median(dual.times_raw)
        factor = np.ones(dual.times_raw.shape[0], dtype=np.float64)
        factor[later] = 1.05
        factor = factor[:, None, None]
        raw = _score(
            dual.positions_raw * factor,
            dual.velocities_raw,
            dual.positions_raw,
            dual.masses,
            (0, 1),
            dual.times_raw,
            scorecard,
        )
        scaled = _score(
            dual.positions_scaled * factor,
            dual.velocities_scaled,
            dual.positions_scaled,
            dual.masses,
            (0, 1),
            dual.times_raw,
            scorecard,
        )
        self.assertLessEqual(abs(raw.E - scaled.E), 1e-12)
        self.assertLessEqual(
            abs(raw.eps_h - scaled.eps_h) / abs(scaled.eps_h),
            1e-9,
        )
        self.assertEqual(raw.frame, FRAME_NAME)
        self.assertEqual(scaled.frame, FRAME_NAME)


class NonFiniteAndInputTests(unittest.TestCase):
    def test_nan_position_is_tier_0_and_bad_inputs_are_refused(self):
        scorecard = load_scorecard()
        times = np.linspace(0.0, 1.0, 9, dtype=np.float64)
        positions, velocities, _omega = _fixtures.lagrange_rotation(times, masses=_MASSES)
        predicted = positions.copy()
        predicted[1, 0, 0] = np.nan
        result = _score(predicted, velocities, positions, _MASSES, (0, 1), times, scorecard)
        self.assertTrue(math.isnan(result.E))
        self.assertEqual(result.tier, 0)
        self.assertIn("NaN", result.to_json_dict().values())

        with self.assertRaises(ScoringInputError):
            _score(
                positions[:1],
                velocities[:1],
                positions[:1],
                _MASSES,
                (0, 1),
                times[:1],
                scorecard,
            )
        with self.assertRaises(ScoringInputError):
            _score(
                positions[:, :, :2],
                velocities,
                positions,
                _MASSES,
                (0, 1),
                times,
                scorecard,
            )
        with self.assertRaises(ScoringInputError):
            _score(positions, velocities, positions, _MASSES, (1, 1), times, scorecard)
        with self.assertRaises(ScoringInputError):
            score_trajectory(
                positions,
                velocities,
                positions,
                _MASSES,
                (0, 1),
                times,
                velocity_source="finite_difference_context",
                scorecard=scorecard,
                grid="gold",
            )


class DeterminismTests(unittest.TestCase):
    def test_same_inputs_return_equal_results(self):
        scorecard = load_scorecard()
        times = np.linspace(0.0, 1.0, 11, dtype=np.float64)
        positions, velocities = _fixtures.hierarchical_circular(times, masses=_MASSES)
        first = _score(positions, velocities, positions, _MASSES, (0, 1), times, scorecard)
        second = _score(positions, velocities, positions, _MASSES, (0, 1), times, scorecard)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
