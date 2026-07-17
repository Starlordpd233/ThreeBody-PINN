"""Contract tests for the PHYS-05 scheduled loss-weight module (TRAIN-03).

Authored first (RED -> skip) per plan 40-02 Task 1. Each test defers the
production import through ``_require`` so the suite stays green (localized
skip with ``_SKIP_PHRASE``) until ``pinn.training.scheduled_weights`` lands,
then turns green as the schedule is implemented.
"""

from __future__ import annotations

import importlib
import unittest

import torch

from tests.phase40 import _SKIP_PHRASE

MODULE = "pinn.training.scheduled_weights"


def _require(symbol: str):
    """Deferred import -- SkipTest (never ERROR) until the symbol lands."""
    try:
        mod = importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}") from exc
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}")
    return getattr(mod, symbol)


class ScheduledWeightsTests(unittest.TestCase):
    """PHYS-05 warmup / lambda^max / freeze / re-warm state machine."""

    # -- Warmup length: I_warm = min(2000, floor(0.1 * N_Adam,k)) -------------

    def test_warmup_length_formula_two_representative_N(self):
        ScheduledWeights = _require("ScheduledWeights")
        # Per AC: N_Adam=100 -> 10; N_Adam=50000 -> 2000.
        s100 = ScheduledWeights(n_adam_k=100)
        s50000 = ScheduledWeights(n_adam_k=50000)
        self.assertEqual(s100.warmup_length, 10)
        self.assertEqual(s50000.warmup_length, 2000)

    def test_warmup_length_matches_min_formula_across_N(self):
        ScheduledWeights = _require("ScheduledWeights")
        for n_adam in [0, 1, 5, 50, 100, 500, 999, 1000, 5000, 20000, 50000, 123457]:
            with self.subTest(n_adam=n_adam):
                expected = min(2000, int(0.1 * n_adam))
                sched = ScheduledWeights(n_adam_k=n_adam)
                self.assertEqual(sched.warmup_length, expected,
                                 f"I_warm != min(2000, floor(0.1*N)) for N={n_adam}")

    # -- lambda_E <= 1.0 cap holds at every sampled step --------------------

    def test_lambda_e_le_one_across_schedule_for_each_stage_table(self):
        ScheduledWeights = _require("ScheduledWeights")
        # PHYS-05 per-stage table: {0,1}: 0; {2,3,4}: 10^(k-4); {5,6}: 1.
        stage_table = {
            0: (0.0, 0.0),
            1: (0.0, 0.0),
            2: (1e-2, 1e-2),
            3: (1e-1, 1e-1),
            4: (1.0, 1.0),
            5: (1.0, 1.0),
            6: (1.0, 1.0),
        }
        for stage, (le_max, ll_max) in stage_table.items():
            sched = ScheduledWeights(
                n_adam_k=500, lambda_e_max=le_max, lambda_l_max=ll_max)
            for epoch in [0, 1, 5, 25, 50, 100, 500, 1000, 10000]:
                with self.subTest(stage=stage, epoch=epoch):
                    w = sched.current(epoch)
                    self.assertLessEqual(
                        float(w.lambda_e), 1.0 + 1e-12,
                        f"lambda_e > 1 at stage {stage} epoch {epoch}")
                    self.assertLessEqual(
                        float(w.lambda_l), 1.0 + 1e-12,
                        f"lambda_l > 1 at stage {stage} epoch {epoch}")

    def test_lambda_e_max_cap_enforced_at_construction(self):
        ScheduledWeights = _require("ScheduledWeights")
        # PHYS-05 lambda_E^max <= 1 invariant; construction must fail-closed.
        with self.assertRaises(ValueError) as cm:
            ScheduledWeights(n_adam_k=500, lambda_e_max=1.5)
        self.assertIn("lambda_e", str(cm.exception).lower())
        with self.assertRaises(ValueError) as cm:
            ScheduledWeights(n_adam_k=500, lambda_l_max=2.0)
        self.assertIn("lambda_l", str(cm.exception).lower())
        # Negative / non-finite also rejected.
        with self.assertRaises(ValueError):
            ScheduledWeights(n_adam_k=500, lambda_phys_max=-0.1)
        with self.assertRaises(ValueError):
            ScheduledWeights(n_adam_k=500, lambda_e_max=float("nan"))

    # -- current(epoch) returns the existing LossWeights container -----------

    def test_current_returns_lossweights_consumed_by_compose_total(self):
        ScheduledWeights = _require("ScheduledWeights")
        from pinn.loss_catalog import LossWeights, compose_total
        sched = ScheduledWeights(n_adam_k=500)
        w = sched.current(50)
        # The exact existing container -- no parallel weight type.
        self.assertIsInstance(w, LossWeights)
        self.assertEqual(
            set(getattr(w, "__dataclass_fields__", {})),
            {"lambda_data", "lambda_ic", "lambda_phys", "lambda_e", "lambda_l"})

        # compose_total consumes it unchanged (no raise, finite total).
        dtype = torch.float64
        device = torch.device("cpu")
        terms = {
            "data": torch.tensor(2.0, dtype=dtype, device=device),
            "ic": torch.tensor(3.0, dtype=dtype, device=device),
            "phys": torch.tensor(4.0, dtype=dtype, device=device),
            "energy": torch.tensor(5.0, dtype=dtype, device=device),
            "angmom": torch.tensor(6.0, dtype=dtype, device=device),
        }
        result = compose_total(terms, w)
        self.assertTrue(bool(torch.isfinite(result.total).all()))

    def test_lambda_data_pinned_one_across_schedule(self):
        ScheduledWeights = _require("ScheduledWeights")
        sched = ScheduledWeights(n_adam_k=500)
        for epoch in [0, 1, 50, 500, 10000]:
            with self.subTest(epoch=epoch):
                self.assertEqual(float(sched.current(epoch).lambda_data), 1.0)

    # -- Warmup ramp shape: linear min(1, i/I_warm) -------------------------

    def test_warmup_ramp_linear_then_saturate(self):
        ScheduledWeights = _require("ScheduledWeights")
        # warmup_length = 50 for N=500; lambda_phys_max = 2.0.
        sched = ScheduledWeights(n_adam_k=500, lambda_phys_max=2.0)
        self.assertEqual(sched.warmup_length, 50)
        # epoch 0 -> 0 (or a defined floor for the ramp start); epoch 25 -> 1.0;
        # epoch 50 -> 2.0 (saturated at lambda_phys_max).
        self.assertAlmostEqual(float(sched.current(50).lambda_phys), 2.0, places=12)
        self.assertAlmostEqual(float(sched.current(25).lambda_phys), 1.0, places=12)
        self.assertAlmostEqual(float(sched.current(1000).lambda_phys), 2.0, places=12)

    # -- Freeze: lambda pinned across a simulated L-BFGS phase ---------------

    def test_freeze_holds_lambda_across_simulated_lbfgs_phase(self):
        ScheduledWeights = _require("ScheduledWeights")
        sched = ScheduledWeights(
            n_adam_k=500, lambda_phys_max=2.0,
            lambda_e_max=0.5, lambda_l_max=0.5)
        # Establish the Adam-phase ramp at epoch 25 (mid-warmup).
        before = sched.current(25)
        sched.freeze()
        # L-BFGS phase spans many epochs; lambda must be frozen entry == exit.
        snapshots = [sched.current(e) for e in (25, 26, 27, 100, 500, 5000)]
        for w in snapshots:
            self.assertAlmostEqual(float(w.lambda_phys),
                                   float(snapshots[0].lambda_phys), places=9)
            self.assertAlmostEqual(float(w.lambda_ic),
                                   float(snapshots[0].lambda_ic), places=9)
            self.assertAlmostEqual(float(w.lambda_e),
                                   float(snapshots[0].lambda_e), places=9)
            self.assertAlmostEqual(float(w.lambda_l),
                                   float(snapshots[0].lambda_l), places=9)
            self.assertAlmostEqual(float(w.lambda_data),
                                   float(snapshots[0].lambda_data), places=9)
        # The frozen value equals the pre-freeze ramp value at epoch 25.
        self.assertAlmostEqual(float(snapshots[0].lambda_phys),
                               float(before.lambda_phys), places=9)

    # -- Re-warm: lambda returns to the warmup schedule at a stage boundary --

    def test_rewarm_restarts_warmup_below_lambda_max(self):
        ScheduledWeights = _require("ScheduledWeights")
        sched = ScheduledWeights(n_adam_k=500, lambda_phys_max=1.0,
                                 lambda_e_max=1.0, lambda_l_max=1.0)
        # Fully warm the schedule.
        self.assertAlmostEqual(float(sched.current(500).lambda_phys), 1.0, places=12)
        # Freeze (simulated L-BFGS), then rewarm at the stage boundary.
        sched.freeze()
        sched.rewarm()
        # Early-epoch lambda is strictly below lambda^max again.
        early = sched.current(1)
        self.assertLess(float(early.lambda_phys), 1.0 - 1e-6)
        self.assertLess(float(early.lambda_e), 1.0 - 1e-6)
        self.assertLess(float(early.lambda_l), 1.0 - 1e-6)
        # And still non-negative.
        self.assertGreaterEqual(float(early.lambda_phys), 0.0)

    # -- state_dict / load_state_dict round-trip -----------------------------

    def test_state_dict_round_trip_emits_identical_weights(self):
        ScheduledWeights = _require("ScheduledWeights")
        sched = ScheduledWeights(
            n_adam_k=500, lambda_phys_max=1.5,
            lambda_e_max=0.25, lambda_l_max=0.5, lambda_ic=1.0)
        # Drive the ramp to a non-trivial state.
        sched.current(100)
        sd = sched.state_dict()
        # Round-trip into a fresh schedule constructed with different args.
        other = ScheduledWeights(n_adam_k=1000)
        other.load_state_dict(sd)
        for epoch in [0, 1, 25, 50, 100, 500, 2000]:
            with self.subTest(epoch=epoch):
                w1 = sched.current(epoch)
                w2 = other.current(epoch)
                self.assertAlmostEqual(float(w1.lambda_data),
                                       float(w2.lambda_data), places=12)
                self.assertAlmostEqual(float(w1.lambda_ic),
                                       float(w2.lambda_ic), places=12)
                self.assertAlmostEqual(float(w1.lambda_phys),
                                       float(w2.lambda_phys), places=12)
                self.assertAlmostEqual(float(w1.lambda_e),
                                       float(w2.lambda_e), places=12)
                self.assertAlmostEqual(float(w1.lambda_l),
                                       float(w2.lambda_l), places=12)

    def test_state_dict_round_trip_preserves_frozen_state(self):
        ScheduledWeights = _require("ScheduledWeights")
        sched = ScheduledWeights(n_adam_k=500, lambda_phys_max=2.0)
        sched.current(25)
        sched.freeze()
        sd = sched.state_dict()
        other = ScheduledWeights(n_adam_k=1000)
        other.load_state_dict(sd)
        # Frozen schedule: current() is constant across epochs on BOTH sides.
        a1 = sched.current(10)
        a2 = sched.current(9000)
        b1 = other.current(10)
        b2 = other.current(9000)
        self.assertAlmostEqual(float(a1.lambda_phys), float(a2.lambda_phys), places=12)
        self.assertAlmostEqual(float(b1.lambda_phys), float(b2.lambda_phys), places=12)
        self.assertAlmostEqual(float(a1.lambda_phys), float(b1.lambda_phys), places=12)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
