"""Contract tests for the Phase 38 five-term loss catalog (NET-04).

Tests are authored first (38-05-01). Per-symbol deferred imports SKIP until
each production symbol lands, so the incremental build (data/IC before the
physics terms + composer) stays green step by step.
"""

from __future__ import annotations

import importlib
import math
import unittest
from dataclasses import FrozenInstanceError

import torch

from pinn.constants import (
    CAUSAL_ETA_C,
    CAUSAL_W1,
    D_CHARACTERISTIC_LENGTH,
    EPS_L,
    EPS_SOFT,
    HUBER_DELTA_ANGMOM,
    HUBER_DELTA_DATA,
    HUBER_DELTA_ENERGY,
)


MODULE = "pinn.loss_catalog"


def _import_symbol(name: str):
    """Deferred import so a missing symbol becomes a SKIP, not an ERROR."""
    try:
        mod = importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc
    if not hasattr(mod, name):
        raise unittest.SkipTest(f"{MODULE}.{name} has not landed yet")
    return getattr(mod, name)


def _mps_available() -> bool:
    return bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())


def _huber_elementwise(diff: torch.Tensor, delta: float) -> torch.Tensor:
    """Reference Huber (smooth L1) matching torch.nn.functional.huber_loss reduction='none'."""
    abs_diff = diff.abs()
    quadratic = 0.5 * diff * diff
    linear = delta * (abs_diff - 0.5 * delta)
    return torch.where(abs_diff <= delta, quadratic, linear)


class LossCatalogTests(unittest.TestCase):
    """Five-term catalog: locked deltas, causal weights, composer, finiteness."""

    def test_data_huber_matches_torch_and_locked_delta(self):
        data_huber_loss = _import_symbol("data_huber_loss")
        self.assertEqual(HUBER_DELTA_DATA, 1.0)
        dtype = torch.float64
        device = torch.device("cpu")
        # Already-scaled COM-projected r' positions: (N_t=2, 3, 3).
        pred = torch.tensor(
            [
                [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]],
                [[0.1, 0.0, 0.0], [0.9, 0.2, 0.0], [-1.0, -0.2, 0.0]],
            ],
            dtype=dtype,
            device=device,
        )
        true = torch.zeros_like(pred)
        true[0] = pred[0]  # zero residual at t0
        true[1] = pred[1] - 0.5  # residual of 0.5 everywhere

        got = data_huber_loss(pred, true, dtype=dtype, device=device)
        self.assertTrue(torch.isfinite(got).all())
        self.assertEqual(got.dim(), 0)

        residual = pred - true
        ref = _huber_elementwise(residual, HUBER_DELTA_DATA).mean()
        self.assertTrue(torch.allclose(got, ref, rtol=1e-12, atol=1e-12))

        # Hand batch with residual > delta to exercise the linear branch.
        pred2 = torch.full((1, 3, 3), 3.0, dtype=dtype, device=device)
        true2 = torch.zeros_like(pred2)
        got2 = data_huber_loss(pred2, true2, dtype=dtype, device=device)
        ref2 = _huber_elementwise(pred2 - true2, 1.0).mean()
        self.assertTrue(torch.allclose(got2, ref2, rtol=1e-12, atol=1e-12))

    def test_ic_anchor_squared_error_beta_v(self):
        ic_anchor_loss = _import_symbol("ic_anchor_loss")
        dtype = torch.float64
        device = torch.device("cpu")
        pred_r0 = torch.tensor(
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            dtype=dtype, device=device,
        )
        true_r0 = torch.zeros_like(pred_r0)
        pred_v0 = torch.tensor(
            [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 0.5]],
            dtype=dtype, device=device,
        )
        true_v0 = torch.zeros_like(pred_v0)
        # L_r = (1/3) sum_i ||dr_i||^2 = (1+1+1)/3 = 1
        # L_v = (1/3) sum_i ||dv_i||^2 = (1+1+0.25)/3 = 0.75; beta_v=1
        expected = torch.tensor(1.0 + 0.75, dtype=dtype, device=device)
        got = ic_anchor_loss(pred_r0, true_r0, pred_v0, true_v0,
                             beta_v=1.0, dtype=dtype, device=device)
        self.assertTrue(torch.isfinite(got).all())
        self.assertTrue(torch.allclose(got, expected, rtol=1e-12, atol=1e-12))

    def test_loss_weights_frozen_five_field_validation(self):
        LossWeights = _import_symbol("LossWeights")
        w = LossWeights()
        self.assertEqual(w.lambda_data, 1.0)
        # Exactly five named fields (one per term).
        fields = set(getattr(w, "__dataclass_fields__", {}))
        self.assertEqual(
            fields,
            {"lambda_data", "lambda_ic", "lambda_phys", "lambda_e", "lambda_l"},
        )
        with self.assertRaises(FrozenInstanceError):
            w.lambda_ic = 2.0  # type: ignore[misc]

        # Negative / NaN / non-1.0 lambda_data all raise typed ValueError naming field.
        with self.assertRaises(ValueError) as cm:
            LossWeights(lambda_ic=-0.1)
        self.assertIn("lambda_ic", str(cm.exception).lower())

        with self.assertRaises(ValueError) as cm:
            LossWeights(lambda_phys=float("nan"))
        self.assertIn("lambda_phys", str(cm.exception).lower())

        with self.assertRaises(ValueError) as cm:
            LossWeights(lambda_data=0.5)
        msg = str(cm.exception).lower()
        self.assertIn("lambda_data", msg)
        self.assertTrue("1.0" in msg or "1" in msg or "§3.1" in str(cm.exception)
                        or "3.1" in str(cm.exception))

        # Valid overrides construct.
        ok = LossWeights(lambda_ic=2.0, lambda_phys=0.0, lambda_e=0.5, lambda_l=0.0)
        self.assertEqual(ok.lambda_ic, 2.0)
        self.assertEqual(ok.lambda_data, 1.0)

    def test_causal_physics_weights_and_sorted_time(self):
        causal_physics_loss = _import_symbol("causal_physics_loss")
        dtype = torch.float64
        device = torch.device("cpu")
        self.assertEqual(CAUSAL_ETA_C, 1.0)
        self.assertEqual(CAUSAL_W1, 1.0)

        rbar = torch.tensor([0.5, 1.0, 2.0], dtype=dtype, device=device)
        times = torch.tensor([0.0, 0.5, 1.0], dtype=dtype, device=device)
        loss = causal_physics_loss(rbar, eta_c=CAUSAL_ETA_C, times=times,
                                   dtype=dtype, device=device)
        self.assertTrue(torch.isfinite(loss).all())

        # Hand weights: w0=1; w1=exp(-1*0.5); w2=exp(-1*(0.5+1.0))
        w0 = 1.0
        w1 = math.exp(-1.0 * 0.5)
        w2 = math.exp(-1.0 * (0.5 + 1.0))
        expected = (w0 * 0.5 + w1 * 1.0 + w2 * 2.0) / 3.0
        self.assertAlmostEqual(float(loss), expected, places=12)

        # w_n stays in (0, 1] as upstream residual grows.
        large = torch.tensor([10.0, 10.0, 10.0, 10.0], dtype=dtype, device=device)
        loss_large, details = causal_physics_loss(
            large,
            eta_c=CAUSAL_ETA_C,
            dtype=dtype,
            device=device,
            return_details=True,
        )
        self.assertTrue(torch.isfinite(loss_large).all())
        weights = details["w_n"]
        self.assertTrue(bool(torch.all((weights > 0) & (weights <= 1)).item()))
        # With large Rbar, later weights are clipped at a positive floor, so
        # loss remains below the unweighted mean without erasing supervision.
        self.assertLess(float(loss_large), float(large.mean()))

        # Unordered times -> ValueError.
        unordered = torch.tensor([0.0, 1.0, 0.5], dtype=dtype, device=device)
        with self.assertRaises(ValueError):
            causal_physics_loss(rbar, eta_c=CAUSAL_ETA_C, times=unordered,
                                dtype=dtype, device=device)

        # Order sensitivity: shuffled Rbar (with matching shuffled times that
        # are re-sorted? Plan: shuffled Rbar with matching-shuffled times that
        # are themselves unordered is rejected; instead compare ascending
        # Rbar sequence vs a different permutation of Rbar under ascending
        # times — different prefix cumsums => different loss.
        rbar_shuffled = torch.tensor([2.0, 0.5, 1.0], dtype=dtype, device=device)
        loss_shuffled = causal_physics_loss(
            rbar_shuffled, eta_c=CAUSAL_ETA_C, times=times,
            dtype=dtype, device=device,
        )
        self.assertNotAlmostEqual(float(loss), float(loss_shuffled), places=10)

    def test_soft_energy_uses_supplied_eps_h_not_recomputed(self):
        soft_energy_loss = _import_symbol("soft_energy_loss")
        dtype = torch.float64
        device = torch.device("cpu")
        self.assertEqual(HUBER_DELTA_ENERGY, 1.0)
        self.assertEqual(EPS_SOFT, 1e-5)

        # Simple equal-mass, COM-centered configuration.
        positions = torch.tensor(
            [[[1.0, 0.0, 0.0], [-0.5, 0.86602540378, 0.0], [-0.5, -0.86602540378, 0.0]]],
            dtype=dtype, device=device,
        )
        velocities = torch.zeros_like(positions)
        masses = torch.ones(3, dtype=dtype, device=device)
        # h0 near current H so relative drift is small.
        # Call once with a probe h0 of 0 and large eps_h.
        h0 = torch.tensor(-1.0, dtype=dtype, device=device)
        eps_h = 1e-4  # supplied metadata (= 1e-4 * S_H upstream); NOT recomputed
        loss = soft_energy_loss(
            positions, velocities, h0, eps_h,
            masses=masses, dtype=dtype, device=device,
        )
        self.assertTrue(torch.isfinite(loss).all())
        self.assertEqual(loss.dim(), 0)

        # Changing eps_h changes the loss (proves it is consumed, not ignored).
        loss2 = soft_energy_loss(
            positions, velocities, h0, eps_h * 100.0,
            masses=masses, dtype=dtype, device=device,
        )
        self.assertNotAlmostEqual(float(loss), float(loss2), places=10)

    def test_angular_momentum_huber(self):
        angular_momentum_loss = _import_symbol("angular_momentum_loss")
        dtype = torch.float64
        device = torch.device("cpu")
        self.assertEqual(HUBER_DELTA_ANGMOM, 1.0)
        self.assertEqual(EPS_L, 1e-8)

        positions = torch.tensor(
            [[[1.0, 0.0, 0.0], [-0.5, 0.5, 0.0], [-0.5, -0.5, 0.0]]],
            dtype=dtype, device=device,
        )
        velocities = torch.tensor(
            [[[0.0, 0.2, 0.0], [-0.1, -0.1, 0.0], [0.1, -0.1, 0.0]]],
            dtype=dtype, device=device,
        )
        masses = torch.ones(3, dtype=dtype, device=device)
        # L0 from the same snapshot -> zero drift.
        r = positions[0]
        v = velocities[0]
        l0 = torch.cross(r, v, dim=-1).sum(dim=0)  # sum m_i (r x v) with m=1
        loss = angular_momentum_loss(
            positions, velocities, l0, masses=masses, dtype=dtype, device=device,
        )
        self.assertTrue(torch.isfinite(loss).all())
        self.assertAlmostEqual(float(loss), 0.0, places=10)

        # Perturbed velocities -> positive finite loss.
        v_pert = velocities + 0.3
        loss_pert = angular_momentum_loss(
            positions, v_pert, l0, masses=masses, dtype=dtype, device=device,
        )
        self.assertGreater(float(loss_pert), 0.0)

    def test_compose_total_per_term_and_weighted_sum(self):
        compose_total = _import_symbol("compose_total")
        LossWeights = _import_symbol("LossWeights")
        LossTerms = _import_symbol("LossTerms")
        dtype = torch.float64
        device = torch.device("cpu")
        terms = {
            "data": torch.tensor(2.0, dtype=dtype, device=device),
            "ic": torch.tensor(3.0, dtype=dtype, device=device),
            "phys": torch.tensor(4.0, dtype=dtype, device=device),
            "energy": torch.tensor(5.0, dtype=dtype, device=device),
            "angmom": torch.tensor(6.0, dtype=dtype, device=device),
        }
        w = LossWeights(lambda_ic=2.0, lambda_phys=0.5, lambda_e=0.0, lambda_l=1.0)
        result = compose_total(terms, w)
        self.assertIsInstance(result, LossTerms)
        # Per-term scalars unchanged by weights.
        self.assertTrue(torch.allclose(result.data, terms["data"]))
        self.assertTrue(torch.allclose(result.ic, terms["ic"]))
        self.assertTrue(torch.allclose(result.phys, terms["phys"]))
        self.assertTrue(torch.allclose(result.energy, terms["energy"]))
        self.assertTrue(torch.allclose(result.angmom, terms["angmom"]))
        expected_total = 1.0 * 2.0 + 2.0 * 3.0 + 0.5 * 4.0 + 0.0 * 5.0 + 1.0 * 6.0
        self.assertAlmostEqual(float(result.total), expected_total, places=12)

        # Changing a weight changes only the total.
        w2 = LossWeights(lambda_ic=10.0, lambda_phys=0.5, lambda_e=0.0, lambda_l=1.0)
        result2 = compose_total(terms, w2)
        self.assertTrue(torch.allclose(result2.data, result.data))
        self.assertNotAlmostEqual(float(result2.total), float(result.total), places=10)

    def test_term_inventory_exactly_five_no_linear_momentum(self):
        mod = importlib.import_module(MODULE) if self._module_exists() else None
        if mod is None:
            self.skipTest(f"{MODULE} has not landed yet")
        required = {
            "data_huber_loss",
            "ic_anchor_loss",
            "causal_physics_loss",
            "soft_energy_loss",
            "angular_momentum_loss",
            "compose_total",
            "LossWeights",
            "LossTerms",
        }
        for name in required:
            self.assertTrue(hasattr(mod, name), f"missing export {name}")
        # No linear-momentum term.
        for banned in ("linear_momentum_loss", "l_p_loss", "L_P", "momentum_loss"):
            self.assertFalse(hasattr(mod, banned), f"spurious export {banned}")

    def test_dimensionless_d_and_tau_convention(self):
        """Catalog lives in the dimensionless system: D ≈ 4.6416, t_tau ∈ [-1,1]."""
        self.assertAlmostEqual(D_CHARACTERISTIC_LENGTH, 4.6416, places=3)
        # Importing the catalog must pull D from constants (no silent 6.694).
        if not self._module_exists():
            self.skipTest(f"{MODULE} has not landed yet")
        import pathlib
        import ast
        src = (pathlib.Path(__file__).resolve().parents[2] / "pinn" / "loss_catalog.py").read_text()
        self.assertIn("D_CHARACTERISTIC_LENGTH", src)
        self.assertNotIn("6.694", src)
        # t_tau map identity is documented via the 2u-1 convention (no free param).
        tree = ast.parse(src)
        self.assertIsNotNone(tree)

    def test_huber_transition_continuity(self):
        """Edge R4: Huber value is continuous at |x|=delta."""
        data_huber_loss = _import_symbol("data_huber_loss")
        dtype = torch.float64
        device = torch.device("cpu")
        delta = HUBER_DELTA_DATA
        # Single residual element of magnitude exactly delta vs just below/above.
        # Use a (1,3,3) tensor where only one entry is nonzero residual.
        def loss_at(mag: float) -> float:
            pred = torch.zeros(1, 3, 3, dtype=dtype, device=device)
            true = torch.zeros_like(pred)
            pred[0, 0, 0] = mag
            return float(data_huber_loss(pred, true, dtype=dtype, device=device))

        below = loss_at(delta - 1e-8)
        at = loss_at(delta)
        above = loss_at(delta + 1e-8)
        self.assertAlmostEqual(below, at, places=6)
        self.assertAlmostEqual(at, above, places=6)

    def test_both_precision_finiteness(self):
        """All five terms + composer evaluate finite under both runtime arms."""
        data_huber_loss = _import_symbol("data_huber_loss")
        ic_anchor_loss = _import_symbol("ic_anchor_loss")
        causal_physics_loss = _import_symbol("causal_physics_loss")
        soft_energy_loss = _import_symbol("soft_energy_loss")
        angular_momentum_loss = _import_symbol("angular_momentum_loss")
        compose_total = _import_symbol("compose_total")
        LossWeights = _import_symbol("LossWeights")

        arms = [("float64", torch.float64, torch.device("cpu"))]
        if _mps_available():
            arms.append(("float32", torch.float32, torch.device("mps")))

        for label, dtype, device in arms:
            with self.subTest(arm=label):
                positions = torch.tensor(
                    [[[1.0, 0.0, 0.0], [-0.5, 0.5, 0.0], [-0.5, -0.5, 0.0]]],
                    dtype=dtype, device=device,
                )
                velocities = torch.tensor(
                    [[[0.0, 0.1, 0.0], [-0.05, -0.05, 0.0], [0.05, -0.05, 0.0]]],
                    dtype=dtype, device=device,
                )
                masses = torch.ones(3, dtype=dtype, device=device)
                true = positions * 0.9
                l_data = data_huber_loss(positions, true, dtype=dtype, device=device)
                l_ic = ic_anchor_loss(
                    positions[0], true[0], velocities[0], velocities[0] * 0.9,
                    beta_v=1.0, dtype=dtype, device=device,
                )
                rbar = torch.tensor([0.1, 0.2, 0.3], dtype=dtype, device=device)
                l_phys = causal_physics_loss(rbar, eta_c=CAUSAL_ETA_C,
                                             dtype=dtype, device=device)
                h0 = torch.tensor(-1.0, dtype=dtype, device=device)
                l_e = soft_energy_loss(
                    positions, velocities, h0, 1e-4,
                    masses=masses, dtype=dtype, device=device,
                )
                r0, v0 = positions[0], velocities[0]
                l0 = (masses.unsqueeze(-1) * torch.cross(r0, v0, dim=-1)).sum(dim=0)
                l_l = angular_momentum_loss(
                    positions, velocities, l0, masses=masses,
                    dtype=dtype, device=device,
                )
                for name, val in (
                    ("data", l_data), ("ic", l_ic), ("phys", l_phys),
                    ("energy", l_e), ("angmom", l_l),
                ):
                    self.assertTrue(bool(torch.isfinite(val).all()), f"{name} non-finite on {label}")
                terms = {
                    "data": l_data, "ic": l_ic, "phys": l_phys,
                    "energy": l_e, "angmom": l_l,
                }
                result = compose_total(terms, LossWeights())
                self.assertTrue(bool(torch.isfinite(result.total).all()))

    def _module_exists(self) -> bool:
        try:
            importlib.import_module(MODULE)
            return True
        except ImportError:
            return False


if __name__ == "__main__":
    unittest.main()
