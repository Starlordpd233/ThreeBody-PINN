"""Phase 59 (FEAS-07; D-17, D-38): the comparison points' public surface for Phase 60."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

import numpy as np

from pinn.data.types import RecordKey
from pinn.verification import baselines, nn_copy, two_kepler
from tests.phase59._fixtures import hierarchical_circular


EXPORTS = {
    two_kepler: (
        "NotApplicable", "propagate_bound", "two_kepler_prediction",
        "two_kepler_accelerations", "formula_applicability",
    ),
    nn_copy: ("nearest_training_neighbour", "copy_prediction", "copy_accelerations"),
    baselines: (
        "score_formula", "score_copy", "candidate_pool", "feas09_record",
        "with_residual_context", "PRODUCER_MODULES", "main",
    ),
}
NOT_APPLICABLE = "not applicable: no hierarchical split"


class PublicSurfaceTests(unittest.TestCase):
    def test_every_planned_export_exists(self) -> None:
        for module, names in EXPORTS.items():
            for name in names:
                with self.subTest(module=module.__name__, name=name):
                    self.assertTrue(hasattr(module, name))


class Feas09Tests(unittest.TestCase):
    def test_the_formula_does_not_apply_to_standard_records(self) -> None:
        self.assertEqual(two_kepler.formula_applicability("standard"), NOT_APPLICABLE)
        self.assertIsNone(two_kepler.formula_applicability("hierarchical"))

    def test_the_probe_entries_on_the_synthetic_manifest(self) -> None:
        from pinn.verification.split_allowlist import SplitAllowlist
        from tests.phase59._corpus_fixtures import tiny_split_fixture

        with tiny_split_fixture() as fixture:
            allowlist = SplitAllowlist.from_manifest(
                fixture.manifest_path, expected_sha256=fixture.manifest_sha256,
            )
            record = baselines.feas09_record(allowlist)
        self.assertEqual(record["stage4b"], NOT_APPLICABLE)
        self.assertEqual(record["stage6"], NOT_APPLICABLE)
        self.assertTrue(record["hierarchical_records_all_stage_0_or_1"])


class FormulaRowTests(unittest.TestCase):
    def test_a_decoupled_system_scores_near_zero_with_its_residual_columns(self) -> None:
        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification.feasibility_scorer import physics_residual_context

        times = np.linspace(0.0, 10.0, 1001)
        masses = np.array([1.0, 0.8, 0.6])
        positions, velocities = hierarchical_circular(times / 10.0, masses=masses)
        reference = SimpleNamespace(
            record_key=RecordKey("hierarchical", "gold", 5),
            times=times,
            positions=positions,
            velocities=velocities,
            masses=masses,
            inner_pair=(0, 1),
            permutation=np.array([0, 1, 2]),
        )
        row = baselines.score_formula(
            reference, scorecard=load_scorecard(), r_ref=3.0,
        )
        self.assertTrue(row["applicable"])
        self.assertLess(row["E"], 1e-9)
        predicted, _v = two_kepler.two_kepler_prediction(
            positions[0], velocities[0], masses, (0, 1), times / 10.0,
        )
        expected = physics_residual_context(
            predicted,
            two_kepler.two_kepler_accelerations(predicted, masses, (0, 1)),
            masses,
            r_ref=3.0,
        )
        self.assertEqual(row["physics_residual_mean"], expected["mean"])
        self.assertEqual(row["physics_residual_max"], expected["max"])


if __name__ == "__main__":
    unittest.main()
