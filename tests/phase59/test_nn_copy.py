"""Phase 59 (FEAS-07; D-16): the nearest-neighbour copy."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

import numpy as np
import torch

from pinn.data.types import RecordKey


def _key(identifier, fidelity="base"):
    return RecordKey("hierarchical", fidelity, identifier)


def _reference(times, positions, velocities, masses, identifier=0):
    return SimpleNamespace(
        record_key=_key(identifier, "gold"),
        times=np.asarray(times, dtype=np.float64),
        positions=np.asarray(positions, dtype=np.float64),
        velocities=np.asarray(velocities, dtype=np.float64),
        masses=np.asarray(masses, dtype=np.float64),
        inner_pair=(0, 1),
    )


def _spread_positions(n, rng):
    """Bodies at least 0.1 apart in every sample."""
    base = np.array([[0.0, 0.0, 0.0], [0.4, 0.0, 0.0], [0.0, 0.7, 0.0]])
    return base[None, :, :] + 0.05 * rng.uniform(-1.0, 1.0, size=(n, 3, 3))


class NearestTests(unittest.TestCase):
    def test_euclidean_distance_and_ties_to_the_lower_key(self) -> None:
        from pinn.verification import nn_copy

        query = np.zeros(13)
        far = np.full(13, 1.0)
        near_a = np.zeros(13)
        near_a[0] = 0.5
        near_b = np.zeros(13)
        near_b[5] = -0.5
        candidates = [(_key(9), near_b), (_key(4), far), (_key(7), near_a)]
        key, distance = nn_copy.nearest_training_neighbour(_key(100), query, candidates)
        self.assertEqual(key, _key(7))
        self.assertEqual(distance, 0.5)
        with self.assertRaises(ValueError):
            nn_copy.nearest_training_neighbour(_key(100), query, [])


class CandidatePoolTests(unittest.TestCase):
    def test_the_pool_is_exactly_the_stage0_training_base_keys(self) -> None:
        from pinn.verification import baselines
        from pinn.verification.split_allowlist import SplitAllowlist
        from tests.phase59._corpus_fixtures import tiny_split_fixture

        with tiny_split_fixture() as fixture:
            allowlist = SplitAllowlist.from_manifest(
                fixture.manifest_path, expected_sha256=fixture.manifest_sha256,
            )
            pool = baselines.candidate_pool(allowlist)
            expected = sorted(
                allowlist.records("train", variant="hierarchical", fidelity="base", stage=0)
            )
            validation = set(
                allowlist.records("validation", variant="hierarchical", fidelity="base")
            )
        self.assertEqual(list(pool), expected)
        self.assertTrue(pool)
        self.assertTrue(set(pool).isdisjoint(validation))
        self.assertTrue(all(key.fidelity == "base" for key in pool))


class SelfMatchTests(unittest.TestCase):
    def test_a_query_inside_the_candidates_is_refused(self) -> None:
        from pinn.verification import nn_copy

        vector = np.zeros(13)
        candidates = [(_key(3), vector + 1.0), (_key(8), vector)]
        with self.assertRaises(ValueError):
            nn_copy.nearest_training_neighbour(_key(8), vector, candidates)


class CopyPredictionTests(unittest.TestCase):
    def test_the_neighbour_trajectory_on_the_query_grid(self) -> None:
        from pinn.verification import nn_copy

        rng = np.random.default_rng(1)
        times = np.linspace(0.0, 10.5, 22)
        query = _reference(times, _spread_positions(22, rng), rng.normal(size=(22, 3, 3)), [1.0, 0.8, 0.6])
        neighbour = _reference(
            times + 1e-10, _spread_positions(22, rng), rng.normal(size=(22, 3, 3)), [1.1, 0.7, 0.5], 4,
        )
        positions, velocities, masses, grid = nn_copy.copy_prediction(query, neighbour)
        keep = times <= 10.0
        np.testing.assert_array_equal(positions, neighbour.positions[keep])
        np.testing.assert_array_equal(velocities, neighbour.velocities[keep])
        np.testing.assert_array_equal(masses, neighbour.masses)
        np.testing.assert_array_equal(grid, times[keep])
        shifted = _reference(times + 1e-6, neighbour.positions, neighbour.velocities, neighbour.masses, 4)
        with self.assertRaises(ValueError):
            nn_copy.copy_prediction(query, shifted)
        shorter = _reference(times[:-3], neighbour.positions[:-3], neighbour.velocities[:-3], neighbour.masses, 4)
        with self.assertRaises(ValueError):
            nn_copy.copy_prediction(query, shorter)


class DeterminismTests(unittest.TestCase):
    def test_two_searches_agree(self) -> None:
        from pinn.verification import nn_copy

        rng = np.random.default_rng(7)
        candidates = [(_key(index), rng.uniform(-1.0, 1.0, size=13)) for index in range(200)]
        query = rng.uniform(-1.0, 1.0, size=13)
        first = nn_copy.nearest_training_neighbour(_key(1000), query, candidates)
        second = nn_copy.nearest_training_neighbour(_key(1000), query, list(reversed(candidates)))
        self.assertEqual(first, second)


class CopyResidualTests(unittest.TestCase):
    def test_the_copy_acceleration_and_the_mass_mismatch_column(self) -> None:
        from pinn.physics_residual import softened_acceleration
        from pinn.verification import baselines, nn_copy
        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification.feasibility_scorer import score_trajectory

        rng = np.random.default_rng(3)
        times = np.linspace(0.0, 10.0, 41)
        masses = np.array([1.0, 0.8, 0.6])
        positions = _spread_positions(41, rng)
        neighbour = _reference(times, positions, rng.normal(size=(41, 3, 3)), masses, 5)
        accelerations = nn_copy.copy_accelerations(neighbour)
        expected = softened_acceleration(
            positions, masses, eps_soft=1e-12, dtype=torch.float64, device=torch.device("cpu"),
        ).numpy()
        np.testing.assert_array_equal(accelerations, expected)
        scorecard = load_scorecard()
        plain = score_trajectory(
            positions, neighbour.velocities, positions * 1.001, masses, (0, 1), times,
            velocity_source="brutus", scorecard=scorecard, grid="gold",
        )
        same = baselines.with_residual_context(plain, positions, accelerations, masses, r_ref=1.0)
        heavier = baselines.with_residual_context(
            plain, positions, accelerations, masses * 1.1, r_ref=1.0,
        )
        self.assertLessEqual(same.physics_residual_mean * 1e6, heavier.physics_residual_mean)
        for result in (same, heavier):
            self.assertEqual(result.E, plain.E)
            self.assertEqual(result.tier, plain.tier)


if __name__ == "__main__":
    unittest.main()
