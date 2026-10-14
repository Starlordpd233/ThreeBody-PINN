"""Frozen-file, strict-loader, golden-value and tier-boundary tests (FEAS-01)."""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import tempfile
import unittest

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME
from pinn.verification.feasibility_scorecard import (
    SCORECARD_SHA256,
    ScorecardError,
    load_scorecard,
    tier_of,
)

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCORECARD_PATH = ROOT / "pinn" / "verification" / "artifacts" / "feasibility_scorecard_v1.json"


def _canonical(payload: object) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode("ascii")


class FrozenFileTests(unittest.TestCase):
    def test_file_exists_and_bytes_are_canonical(self):
        self.assertTrue(SCORECARD_PATH.is_file())
        raw = SCORECARD_PATH.read_bytes()
        self.assertEqual(raw, _canonical(json.loads(raw)))
        self.assertEqual(hashlib.sha256(raw).hexdigest(), SCORECARD_SHA256)

    def test_load_twice_is_idempotent(self):
        first = load_scorecard()
        second = load_scorecard()
        self.assertEqual(first, second)
        self.assertEqual(first.sha256, second.sha256)
        self.assertEqual(first.sha256, SCORECARD_SHA256)


class StrictLoaderTests(unittest.TestCase):
    def _payload(self) -> dict:
        return json.loads(SCORECARD_PATH.read_text(encoding="ascii"))

    def _expect_path(self, payload: dict, dotted: str, *, indent: int = 2, own_hash: bool = True) -> None:
        raw = (
            json.dumps(payload, sort_keys=True, indent=indent, ensure_ascii=True) + "\n"
        ).encode("ascii")
        digest = hashlib.sha256(raw).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "scorecard.json"
            path.write_bytes(raw)
            with self.assertRaises(ScorecardError) as caught:
                load_scorecard(
                    path,
                    expected_sha256=digest if own_hash else SCORECARD_SHA256,
                )
        self.assertIn(dotted, str(caught.exception))

    def test_unknown_key_at_top_level(self):
        payload = self._payload()
        payload["extra_key"] = 1
        self._expect_path(payload, "extra_key")

    def test_unknown_key_inside_tier_level(self):
        payload = self._payload()
        payload["tiers"]["levels"][0]["extra_key"] = 1
        self._expect_path(payload, "tiers.levels[0].extra_key")

    def test_unknown_key_inside_budget_rule(self):
        payload = self._payload()
        payload["budget_rule"]["extra_key"] = 1
        self._expect_path(payload, "budget_rule.extra_key")

    def test_unknown_key_inside_gate_g1(self):
        payload = self._payload()
        payload["gate_g1"]["extra_key"] = 1
        self._expect_path(payload, "gate_g1.extra_key")

    def test_unknown_key_inside_tolerances(self):
        payload = self._payload()
        payload["diag07"]["tolerances"]["extra_key"] = 1
        self._expect_path(payload, "diag07.tolerances.extra_key")

    def test_missing_key_names_dotted_path(self):
        payload = self._payload()
        del payload["budget_rule"]["timing_run_min_steps"]
        self._expect_path(payload, "budget_rule.timing_run_min_steps")

    def test_changed_value_fails_sha256(self):
        payload = self._payload()
        payload["tiers"]["levels"][0]["E_max"] = 0.02
        raw = _canonical(payload)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "scorecard.json"
            path.write_bytes(raw)
            with self.assertRaises(ScorecardError) as caught:
                load_scorecard(path)
        self.assertIn("SHA-256", str(caught.exception))

    def test_non_canonical_indent_is_refused(self):
        payload = self._payload()
        raw = (
            json.dumps(payload, sort_keys=True, indent=4, ensure_ascii=True) + "\n"
        ).encode("ascii")
        digest = hashlib.sha256(raw).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "scorecard.json"
            path.write_bytes(raw)
            with self.assertRaises(ScorecardError) as caught:
                load_scorecard(path, expected_sha256=digest)
        self.assertIn("canonical", str(caught.exception))


class GoldenValueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = load_scorecard()

    def test_tier_bounds(self):
        levels = self.card.section("tiers")["levels"]
        self.assertEqual(
            [(level["tier"], level["E_max"], level["eps_h_max"]) for level in levels],
            [(3, 0.01, 1e-5), (2, 0.01, 1e-3), (1, 0.1, None)],
        )

    def test_metrics_and_frame(self):
        metrics = self.card.section("metrics")
        frame = self.card.section("frame")
        self.assertEqual(metrics["valid_horizon_deltas"], (0.01, 0.1))
        self.assertEqual(metrics["eps_h_eps_inv"], 1e-10)
        self.assertEqual(
            metrics["physics_residual_r_ref_artifact"],
            "pinn/verification/artifacts/r_ref_stage0.json",
        )
        self.assertEqual(
            dict(metrics["physics_residual_acceleration_sources"]),
            {
                "network": "autograd_second_derivative",
                "two_kepler": "analytic_kepler",
                "nn_copy": "neighbour_newtonian_own_positions_and_masses_eps_1e-12",
            },
        )
        self.assertEqual(frame["D"], D_CHARACTERISTIC_LENGTH)
        self.assertEqual(frame["T"], T_CHARACTERISTIC_TIME)

    def test_budget_lbfgs_and_g2(self):
        budget = self.card.section("budget_rule")
        self.assertEqual(budget["timing_run_min_steps"], 50)
        self.assertEqual(budget["cap_hours_single_system"], 3.0)
        self.assertEqual(budget["cap_hours_rung3"], 8.0)
        self.assertEqual(budget["control_adam_steps"], 1000)
        self.assertEqual(budget["still_improving_reference_fraction"], 0.75)
        self.assertEqual(budget["still_improving_final_fraction"], 0.25)
        self.assertEqual(budget["still_improving_min_relative_drop"], 0.1)
        self.assertEqual(budget["extensions_max"], 1)
        self.assertEqual(budget["extension_factor"], 2.0)
        self.assertEqual(budget["scoring_cadence_max_fraction"], 0.05)
        polish = self.card.section("lbfgs_polish")
        self.assertEqual(polish["lbfgs_history_size"], 10)
        self.assertEqual(polish["lbfgs_line_search"], "strong_wolfe")
        self.assertEqual(polish["lbfgs_max_iter"], 50)
        self.assertEqual(polish["stop_after_outer_calls_without_improvement"], 5)
        self.assertEqual(polish["stop_at_fraction_of_adam_wall_time"], 0.25)
        gate = self.card.section("gate_g2")
        self.assertEqual(gate["grid"], (60.0, 120.0, 240.0, 480.0))
        self.assertEqual(gate["locked_value"], 30.0)
        self.assertEqual(self.card.section("accuracy_cadence")["every_steps"], 100)
        self.assertEqual(self.card.section("scoring_grid")["gold_base_agreement_max"], 1e-6)

    def test_panel_rule(self):
        panel = self.card.section("panel_rule")
        self.assertEqual(panel["singles_percentiles"], (10, 50, 90))
        self.assertEqual(panel["singles_min_samples_per_inner_period"], 3.0)
        self.assertEqual(panel["family_size"], 16)
        self.assertEqual(
            panel["family_bin_sizes"],
            (114, 114, 114, 114, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113),
        )
        self.assertEqual(panel["validation_panel_size"], 227)
        self.assertEqual(panel["population_size"], 1812)

    def test_survey_thresholds(self):
        survey = self.card.section("survey_rules")
        stage3 = survey["stage3"]
        stage4 = survey["stage4"]
        self.assertEqual(stage4["a_tau_L_gt"], 5.0)
        self.assertEqual(stage4["b_tau_L_gt"], 2.0)
        self.assertEqual(stage4["b_tau_L_le"], 5.0)
        self.assertEqual(stage3["Q_min"], 0.9)
        self.assertEqual(stage3["Q_max"], 1.1)
        self.assertEqual(stage3["E_percentile"], 25)
        self.assertEqual(stage3["l_ratio_percentile"], 75)
        tau = survey["tau_L"]
        self.assertEqual(tau["dt"], 0.01)
        self.assertEqual(tau["embedding_dim"], 5)
        self.assertEqual(tau["delay"], 10)
        self.assertEqual(tau["theiler_window"], 100)
        self.assertEqual(tau["sensitivity_fit_windows"], (1.0, 2.0, 3.0))

    def test_gate_g1_diag07_and_checkpoints(self):
        gate = self.card.section("gate_g1")
        self.assertEqual(gate["threshold"], 0.01)
        self.assertEqual(gate["checkpoints"], (900, 951))
        diag = self.card.section("diag07")
        self.assertEqual(diag["jx1"]["passenger_share_le"], 1e-4)
        self.assertEqual(diag["jx1"]["overstated_share_ge"], 1e-2)
        self.assertEqual(diag["jx2"]["draw_seed_base"], 59020)
        self.assertEqual(diag["jx3"]["never_anchored_seed"], 59031)
        self.assertEqual(diag["jx3"]["validation_seed"], 59032)
        self.assertEqual(diag["jx4"]["draw_seed"], 59040)
        self.assertEqual(diag["code_commit"], "629b1a6ca4462915b6340a59b8d4e3ad8df75d8b")
        seed42 = diag["checkpoints"]["stage0-v23g7-seed42"]
        self.assertEqual(seed42["best.pt"], 900)
        self.assertEqual(seed42["step-000951.pt"], 951)
        self.assertEqual(seed42["stage-0-init.pt"], 0)


class TierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = load_scorecard()

    def test_inclusive_bounds_and_one_step_above(self):
        card = self.card
        self.assertEqual(tier_of(0.01, 1e-5, scorecard=card), 3)
        self.assertEqual(tier_of(0.01, 1e-3, scorecard=card), 2)
        self.assertEqual(tier_of(0.1, float("nan"), scorecard=card), 1)
        self.assertEqual(tier_of(float("nan"), 0.0, scorecard=card), 0)
        self.assertEqual(tier_of(math.nextafter(0.01, 1.0), 1e-5, scorecard=card), 1)
        self.assertEqual(tier_of(0.01, math.nextafter(1e-5, 1.0), scorecard=card), 2)
        self.assertEqual(tier_of(math.nextafter(0.1, 1.0), 0.0, scorecard=card), 0)


if __name__ == "__main__":
    unittest.main()
