"""Phase 59 DIAG-07 tests for JX-5, JX-2, JX-4 and JX-3. The driver is loaded by path.

CPU float64 tiny networks only. No test writes a checkpoint.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[2]
DIAG07 = ROOT / ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07"
COMMON = DIAG07 / "diag07_common.py"
DRIVER = DIAG07 / "jx02_jx05.py"
_LOADED = {}


def load_driver():
    """Load jx02_jx05.py under a unique module name with its sibling library bound."""
    if "driver" in _LOADED:
        return _LOADED["driver"]
    spec = importlib.util.spec_from_file_location("phase59_diag07_common_panels", COMMON)
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    with mock.patch.dict(sys.modules, {"diag07_common": common}):
        spec = importlib.util.spec_from_file_location("phase59_jx02_jx05", DRIVER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    _LOADED["common"] = common
    _LOADED["driver"] = module
    return module


def _network(seed=3):
    from pinn.architecture_spec import ArchitectureSpec
    from pinn.network import build_network

    return build_network(
        ArchitectureSpec(seed=seed), dtype=torch.float64, device=torch.device("cpu"),
    )


def _ic13(seed=11):
    return np.random.default_rng(seed).uniform(-0.8, 0.8, size=13)


MASSES = np.array([1.0, 0.8, 0.6])
F64 = torch.float64
CPU = torch.device("cpu")


class SubsetRuleTests(unittest.TestCase):
    def test_every_sixteenth_row_of_4096(self) -> None:
        driver = load_driver()
        rows = driver.subset_rows(4096)
        self.assertEqual(rows.tolist(), list(range(0, 4096, 16)))
        self.assertEqual(rows.size, 256)
        self.assertEqual(int(rows[-1]), 4080)


class MixedDerivativeTests(unittest.TestCase):
    def test_mixed_derivative_matches_a_finite_difference_of_autograd_velocity(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u_rows = np.array([0.05, 0.37, 0.81])
        norms = driver.mixed_derivative_norms(
            model, ic13, MASSES, u_rows, dtype=F64, device=CPU,
        )
        mass = torch.as_tensor(MASSES, dtype=F64).reshape(1, 3)

        def velocity(u, ic_vector):
            def positions(u_scalar):
                tau = (2.0 * u_scalar - 1.0).reshape(1)
                inp = torch.cat([tau, ic_vector]).unsqueeze(0)
                return model(inp, mass).reshape(-1)

            return torch.func.jacrev(positions)(torch.as_tensor(u, dtype=F64))

        step = 1e-6
        for row, u in enumerate(u_rows):
            columns = []
            for slot in range(13):
                plus = torch.as_tensor(ic13, dtype=F64).clone()
                minus = plus.clone()
                plus[slot] += step
                minus[slot] -= step
                columns.append((velocity(u, plus) - velocity(u, minus)) / (2.0 * step))
            expected = float(torch.linalg.vector_norm(torch.stack(columns, dim=1).detach()))
            with self.subTest(row=row):
                self.assertLessEqual(abs(norms[row] - expected), 1e-5 * expected)

    def test_no_grad_context_gives_the_same_norms(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u_rows = np.array([0.2, 0.6])
        plain = driver.mixed_derivative_norms(model, ic13, MASSES, u_rows, dtype=F64, device=CPU)
        with torch.no_grad():
            quiet = driver.mixed_derivative_norms(model, ic13, MASSES, u_rows, dtype=F64, device=CPU)
        np.testing.assert_allclose(quiet, plain, rtol=1e-12, atol=0.0)


class SkipBranchTests(unittest.TestCase):
    def test_branches_sum_to_the_block_and_derivatives_add(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u_rows = np.array([0.1, 0.5, 0.9])
        rows, values, derivatives = driver.branch_scales(
            model, ic13, u_rows, dtype=F64, device=CPU, return_values=True,
        )
        self.assertEqual([row["hidden_layer_index"] for row in rows], [0, 2, 4, 6, 8, 10])
        self.assertEqual(tuple(values.shape[:3]), (3, 6, 3))
        torch.testing.assert_close(
            values[:, :, 0] + values[:, :, 1], values[:, :, 2], rtol=0.0, atol=1e-12,
        )
        torch.testing.assert_close(
            derivatives[:, :, 0] + derivatives[:, :, 1], derivatives[:, :, 2],
            rtol=0.0, atol=1e-10,
        )

    def test_block_outputs_follow_the_model_forward(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u = 0.42
        _rows, values, derivatives = driver.branch_scales(
            model, ic13, np.array([u]), dtype=F64, device=CPU, return_values=True,
        )
        ic = torch.as_tensor(ic13, dtype=F64)

        def hidden(u_scalar):
            tau = (2.0 * u_scalar - 1.0).reshape(1)
            x = model.input_layer(torch.cat([tau, ic]).unsqueeze(0))
            outputs = []
            for index, layer in enumerate(model.hidden_layers):
                x = layer(x)
                if index in (0, 2, 4, 6, 8, 10):
                    outputs.append(x.reshape(-1))
            return torch.stack(outputs)

        u_tensor = torch.as_tensor(u, dtype=F64)
        torch.testing.assert_close(values[0, :, 2], hidden(u_tensor), rtol=0.0, atol=1e-12)
        h = 1e-6
        numeric = (hidden(u_tensor + h) - hidden(u_tensor - h)) / (2.0 * h)
        torch.testing.assert_close(derivatives[0, :, 2], numeric, rtol=1e-5, atol=1e-6)


def _tiny_controller(tmp_dir):
    """The Phase-40 tiny CPU float64 controller with a refusing store."""
    from tests.phase40.test_optimizer_phase import _build_controller

    load_driver()
    controller = _build_controller(tmp_dir, max_epochs=1, n_adam=1, collocation_count=64)
    controller._checkpoint_store = _LOADED["common"].RefusingCheckpointStore()
    return controller


class FixtureContextTests(unittest.TestCase):
    def test_the_trainer_builds_the_anchor_for_an_arbitrary_key_and_times(self) -> None:
        import tempfile

        driver = load_driver()
        with tempfile.TemporaryDirectory() as tmp:
            controller = _tiny_controller(tmp)
            batch = controller._stage_batch(
                controller._train_source, stage=0, collocation_count=64,
            )
            key = batch.replay_keys[-1]
            times = np.array([7.5, 0.25, 3.0, 9.9, 1.0])
            ctx = driver.fixture_anchor_context(controller, controller._train_source, key, times)
            np.testing.assert_array_equal(ctx.collocation_times, np.sort(times))
            record = controller._train_source.get(key)
            ic13 = torch.as_tensor(np.asarray(record.ic13, dtype=np.float64), dtype=F64)
            masses = torch.as_tensor(np.asarray(record.masses, dtype=np.float64), dtype=F64)
            u = torch.as_tensor(0.3, dtype=F64)
            tau = (2.0 * u - 1.0).reshape(1)
            expected = controller.model(
                torch.cat([tau, ic13]).unsqueeze(0), masses.unsqueeze(0),
            ).reshape(3, 3)
            torch.testing.assert_close(ctx.traj(u), expected, rtol=0.0, atol=0.0)
            positions = np.asarray(controller._train_source.snapshot_positions(key), dtype=np.float64)
            np.testing.assert_allclose(
                ctx.true_r0.detach().numpy(), positions[0], rtol=0.0, atol=0.0,
            )


class Jx2ReadingTests(unittest.TestCase):
    def test_the_frozen_change_must_exceed_both_draw_ranges(self) -> None:
        driver = load_driver()
        draws_900 = [1.0, 1.2, 1.1]
        draws_951 = [2.0, 2.5, 2.1]
        self.assertEqual(
            driver.jx2_reading(1.0, 1.5, draws_900, draws_951),
            "estimator noise not excluded",
        )
        self.assertEqual(
            driver.jx2_reading(1.0, 1.6, draws_900, draws_951),
            "parameter motion",
        )
        self.assertEqual(
            driver.jx2_reading(1.0, 1.3, draws_900, draws_951),
            "estimator noise not excluded",
        )
        self.assertEqual(
            driver.jx2_reading(1.6, 1.0, draws_900, draws_951),
            "parameter motion",
        )


class Jx4ReadingTests(unittest.TestCase):
    @staticmethod
    def row(tier_0, tier_951, e_0, e_951):
        return {"tier_0": tier_0, "tier_951": tier_951, "E_0": e_0, "E_951": e_951}

    def test_the_three_pre_registered_readings(self) -> None:
        driver = load_driver()
        tier0 = [self.row(0, 0, 1.0, 0.5), self.row(0, 0, 2.0, 1.0)]
        self.assertEqual(
            driver.jx4_reading(0, 2, tier0),
            "relative descent without useful accuracy",
        )
        useful = [self.row(0, 1, 1.0, 0.9), self.row(0, 0, 2.0, 1.0)]
        self.assertEqual(
            driver.jx4_reading(0, 2, useful),
            "useful accuracy with relative descent",
        )
        no_drop = [self.row(0, 1, 1.0, 0.95), self.row(0, 0, 2.0, 1.0)]
        self.assertEqual(driver.jx4_reading(0, 2, no_drop), "inconclusive")
        self.assertEqual(driver.jx4_reading(2, 2, tier0), "inconclusive")
        self.assertEqual(driver.jx4_reading(2, 1, useful), "inconclusive")


class PhysicalFrontTests(unittest.TestCase):
    def test_the_front_under_the_physical_scale_is_causal_physics_loss_with_that_r_ref(self) -> None:
        from pinn.loss_catalog import causal_physics_loss

        driver = load_driver()
        centres = (np.arange(16) + 0.5) / 16 * 10.0
        for scale, raw in (
            (0.37, np.full(16, 0.37)),
            (2.0, np.linspace(0.01, 0.6, 16)),
            (1e-3, np.geomspace(1e-6, 1e-2, 16)),
        ):
            with self.subTest(scale=scale):
                _loss, details = causal_physics_loss(
                    torch.as_tensor(raw, dtype=F64), r_ref=scale, times=centres,
                    dtype=F64, device=CPU, return_details=True,
                )
                weights = details["w_n"].tolist()
                expected = max([n for n, w in enumerate(weights) if w > 0.5], default=-1)
                self.assertEqual(driver.physical_front(raw, scale, dtype=F64, device=CPU), expected)

    def test_the_physical_scale_is_the_mean_body_averaged_squared_force(self) -> None:
        from types import SimpleNamespace

        from pinn.physics_residual import softened_acceleration

        driver = load_driver()
        rng = np.random.default_rng(5)
        times = np.linspace(0.0, 10.5, 22)
        positions = rng.normal(size=(22, 3, 3))
        reference = SimpleNamespace(times=times, positions=positions, masses=MASSES)
        keep = times <= 10.0
        force = softened_acceleration(
            positions[keep], MASSES, dtype=F64, device=CPU,
        )
        expected = float(((force ** 2).sum(dim=(-2, -1)) / 3.0).mean())
        self.assertAlmostEqual(driver.physical_scale(reference), expected, places=12)


class NetworkScoreTests(unittest.TestCase):
    """GAP-59-13: the MPS-safe network score equals the scorer's own on CPU float64."""

    def test_network_score_equals_score_network_on_cpu(self) -> None:
        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification.feasibility_scorer import score_network

        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        times = np.linspace(0.0, 10.0, 40)
        ref = np.random.default_rng(9).normal(scale=0.5, size=(40, 3, 3))
        scorecard = load_scorecard()
        expected = score_network(
            model, ic13, MASSES, ref, (0, 1), times,
            scorecard=scorecard, dtype=F64, device=CPU, grid="gold", microbatch_size=16,
        )
        actual = driver.network_score(
            model, ic13, MASSES, ref, (0, 1), times,
            scorecard=scorecard, dtype=F64, device=CPU, grid="gold", microbatch_size=16,
        )
        self.assertEqual(actual.to_json_dict(), expected.to_json_dict())


def _allowlist():
    from pinn.verification.split_allowlist import (
        GENERATION7_SPLITS_REL,
        SplitAllowlist,
        expected_splits_sha256,
    )

    return SplitAllowlist.from_manifest(
        ROOT / GENERATION7_SPLITS_REL, expected_sha256=expected_splits_sha256(ROOT),
    )


class ReplayProofTests(unittest.TestCase):
    """Real run metadata only. No trajectory file of any split is opened."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = load_driver().replay_anchor_stream(ROOT, _allowlist())

    def test_the_monitor_batch_and_every_checkpoint_proof(self) -> None:
        result = self.result
        self.assertEqual(result["monitor_replay"][:5], [28, 90, 104, 147, 167])
        proofs = {item["file"]: item for item in result["proofs"]}
        self.assertEqual(
            set(proofs),
            {
                "stage-0-init.pt", "best.pt", "step-000931.pt", "step-000941.pt",
                "step-000951.pt", "latest.pt", "failure-stage-0-step-951.pt",
            },
        )
        for name, item in proofs.items():
            with self.subTest(checkpoint=name):
                self.assertTrue(item["proof"])
        self.assertEqual(proofs["stage-0-init.pt"]["after"], "monitor draw")
        self.assertEqual(proofs["best.pt"]["after"], "step 900")
        self.assertEqual(proofs["failure-stage-0-step-951.pt"]["after"], "step 952 draw")

    def test_the_anchor_statistics_over_steps_1_to_951(self) -> None:
        result = self.result
        self.assertEqual(sorted(result["anchors"]), list(range(1, 952)))
        self.assertEqual(result["distinct_anchors"], 40)
        self.assertEqual(result["anchor_counts"][:2], [[0, 132], [1, 111]])
        self.assertEqual(sum(count for _id, count in result["anchor_counts"]), 951)


class Jx3GroupTests(unittest.TestCase):
    RULES = {
        "high_exposure_count": 7,
        "never_anchored_count": 7,
        "never_anchored_seed": 59031,
        "validation_count": 6,
        "validation_seed": 59032,
    }

    def test_groups_are_ordered_seeded_sorted_and_disjoint(self) -> None:
        driver = load_driver()
        counts = {5: 9, 3: 9, 8: 4, 1: 12, 2: 4, 13: 1, 21: 2, 34: 2, 55: 1}
        train = list(range(0, 80))
        validation = list(range(200, 230))
        first = driver.jx3_groups(counts, train, validation, rules=self.RULES)
        second = driver.jx3_groups(counts, train, validation, rules=self.RULES)
        self.assertEqual(first, second)
        self.assertEqual(first["high_exposure"], [1, 3, 5, 2, 8, 21, 34])
        for name, size in (("never_anchored", 7), ("validation", 6)):
            with self.subTest(group=name):
                self.assertEqual(len(first[name]), size)
                self.assertEqual(first[name], sorted(first[name]))
        self.assertTrue(set(first["never_anchored"]).isdisjoint(counts))
        self.assertTrue(set(first["never_anchored"]) <= set(train))
        self.assertTrue(set(first["validation"]) <= set(validation))
        never = sorted(set(train) - set(counts))
        expected = sorted(
            int(value) for value in
            np.random.default_rng(59031).choice(never, size=7, replace=False)
        )
        self.assertEqual(first["never_anchored"], expected)


class Jx3ReadingTests(unittest.TestCase):
    @staticmethod
    def rows(ratios_ic, ratios_res):
        rows = []
        for group, ic, res in zip(
            ("high_exposure", "never_anchored", "validation"), ratios_ic, ratios_res,
        ):
            for value_ic, value_res in zip(ic, res):
                rows.append({
                    "group": group,
                    "L_IC_0": 1.0, "L_IC_951": value_ic,
                    "sum_rtilde_0": 2.0, "sum_rtilde_951": 2.0 * value_res,
                })
        return rows

    def test_exposure_specific_global_inconclusive_and_mixed(self) -> None:
        driver = load_driver()
        specific = [[0.1, 0.1], [0.5, 0.5], [0.6, 0.6]]
        global_ = [[0.2, 0.2], [0.3, 0.3], [0.4, 0.4]]
        between = [[0.2, 0.2], [0.3, 0.3], [0.45, 0.45]]
        self.assertEqual(driver.jx3_reading(self.rows(specific, specific))["outcome"], "exposure-specific")
        self.assertEqual(driver.jx3_reading(self.rows(global_, global_))["outcome"], "global")
        self.assertEqual(driver.jx3_reading(self.rows(between, between))["outcome"], "inconclusive")
        mixed = driver.jx3_reading(self.rows(specific, global_))
        self.assertEqual(mixed["outcome"], "mixed: exposure-specific / global")
        self.assertEqual(mixed["L_IC"], "exposure-specific")
        self.assertEqual(mixed["sum_rtilde"], "global")

    def test_factor_two_bounds(self) -> None:
        driver = load_driver()
        edge = [[0.2], [0.4], [0.1]]
        self.assertEqual(driver.jx3_reading(self.rows(edge, edge))["outcome"], "global")
        just_below_half = [[0.2], [0.40000001], [0.40000001]]
        self.assertEqual(
            driver.jx3_reading(self.rows(just_below_half, just_below_half))["outcome"],
            "exposure-specific",
        )


if __name__ == "__main__":
    unittest.main()
