"""D-10 known-error tests for the FEAS-01 scorer.

Thresholds and horizon deltas come from the loaded scorecard. This module
does not inline a tier boundary.
"""

from __future__ import annotations

import unittest

import numpy as np

from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import (
    ScoreResult,
    eps_h_from_velocities,
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


if __name__ == "__main__":
    unittest.main()
