"""Phase 40 — StageExitMachine contract (TRAIN-06 / CURR-03).

Four-criterion ADVANCE conjunction, NaN/Inf → RECOVER (either phase),
max-epoch → HALT, mid-flight → disposition is None (GAP-40-01 → B).
Criterion 1's β-EMA + patience is exercised as a real mechanism via
TotalLossPlateauSmoother, not a boolean stub.

Grounding: ctl_instruction.md:1928 three dispositions; 40-04-PLAN Task 1;
GAP-40-01/02 RESOLVED-WITH-INSTRUCTION 2026-07-17.
"""
from __future__ import annotations

import math
import unittest
from types import SimpleNamespace

from tests.phase40.test_prohibitions import _require

MODULE = "pinn.training.stage_exit"

StageDisposition = _require("StageDisposition", MODULE)
StageExitMachine = _require("StageExitMachine", MODULE)
StageExitOutcome = _require("StageExitOutcome", MODULE)
TotalLossPlateauSmoother = _require("TotalLossPlateauSmoother", MODULE)


def _stub_cfg(
    *,
    beta=0.98,
    patience=5,
    eps_plateau=1e-5,
    eps_phys=1e-4,
    eps_energy=1e-4,
    energy_floor=1e-4,
    max_epochs=100,
    stagnation_window=50,
):
    """Local duck-typed config — no config-module import (Task 1 independent)."""
    return SimpleNamespace(
        beta=beta,
        patience=patience,
        eps_plateau=eps_plateau,
        eps_phys=eps_phys,
        eps_energy=eps_energy,
        energy_floor=energy_floor,
        max_epochs=max_epochs,
        stagnation_window=stagnation_window,
    )


def _flat_history(n, value=1.0):
    return [float(value)] * n


def _descending_history(n, start=1.0, step=0.01):
    return [float(start - i * step) for i in range(n)]


def _plateaued_train_history(patience, beta=0.98, eps_plateau=1e-5):
    """Build a raw train history that fires the smoother at patience."""
    # Long flat after warmup: relative EMA change → 0.
    return _flat_history(patience + 5, value=1.0)


class EnumShapeTests(unittest.TestCase):
    def test_exactly_three_members(self):
        self.assertEqual(len(StageDisposition), 3)
        names = {m.name for m in StageDisposition}
        self.assertEqual(names, {"ADVANCE", "RECOVER", "HALT"})


class AdvanceGateTests(unittest.TestCase):
    def setUp(self):
        self.cfg = _stub_cfg(patience=5, max_epochs=100)
        self.machine = StageExitMachine(self.cfg)
        # Flat train long enough for plateau; val always at min; phys/energy OK.
        self.train = _plateaued_train_history(self.cfg.patience)
        self.val = _flat_history(len(self.train), value=0.5)

    def test_all_four_pass_returns_advance(self):
        out = self.machine.evaluate(
            self.train, self.val, val_phys=1e-5, val_energy=1e-5,
            had_nan_inf=False, epoch_count=len(self.train),
        )
        self.assertIsInstance(out, StageExitOutcome)
        self.assertEqual(out.disposition, StageDisposition.ADVANCE)
        self.assertTrue(out.train_plateau)
        self.assertTrue(out.val_stable)
        self.assertTrue(out.phys_ok)
        self.assertTrue(out.energy_ok)

    def test_train_plateau_fail_not_advance(self):
        # Short descending history never plateaus.
        train = _descending_history(10)
        val = _flat_history(10, 0.5)
        out = self.machine.evaluate(
            train, val, val_phys=1e-5, val_energy=1e-5,
            had_nan_inf=False, epoch_count=10,
        )
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)
        self.assertFalse(out.train_plateau)

    def test_val_stable_fail_not_advance(self):
        train = self.train
        # Current val above historical min → criterion 2 fails.
        val = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
        # pad to train length
        while len(val) < len(train):
            val.append(0.5)
        out = self.machine.evaluate(
            train, val, val_phys=1e-5, val_energy=1e-5,
            had_nan_inf=False, epoch_count=len(train),
        )
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)
        self.assertFalse(out.val_stable)

    def test_phys_fail_not_advance(self):
        out = self.machine.evaluate(
            self.train, self.val, val_phys=1e-3, val_energy=1e-5,
            had_nan_inf=False, epoch_count=len(self.train),
        )
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)
        self.assertFalse(out.phys_ok)

    def test_energy_fail_not_advance(self):
        out = self.machine.evaluate(
            self.train, self.val, val_phys=1e-5, val_energy=1e-3,
            had_nan_inf=False, epoch_count=len(self.train),
        )
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)
        self.assertFalse(out.energy_ok)


class RecoverTests(unittest.TestCase):
    def setUp(self):
        self.cfg = _stub_cfg(patience=5, max_epochs=100)
        self.machine = StageExitMachine(self.cfg)
        self.train = _plateaued_train_history(5)
        self.val = _flat_history(len(self.train), 0.5)

    def test_nan_inf_adam_phase_recovers(self):
        out = self.machine.evaluate(
            self.train, self.val, val_phys=1e-5, val_energy=1e-5,
            had_nan_inf=True, epoch_count=3,
        )
        self.assertEqual(out.disposition, StageDisposition.RECOVER)

    def test_nan_inf_lbfgs_phase_recovers(self):
        # Same signal path — phase is not an evaluate argument; both phases
        # set had_nan_inf the same way (CTX-41).
        out = self.machine.evaluate(
            self.train, self.val, val_phys=1e-5, val_energy=1e-5,
            had_nan_inf=True, epoch_count=80,
        )
        self.assertEqual(out.disposition, StageDisposition.RECOVER)

    def test_nan_takes_priority_over_max_epoch(self):
        out = self.machine.evaluate(
            self.train, self.val, val_phys=1.0, val_energy=1.0,
            had_nan_inf=True, epoch_count=self.cfg.max_epochs,
        )
        self.assertEqual(out.disposition, StageDisposition.RECOVER)


class HaltAndMidFlightTests(unittest.TestCase):
    def setUp(self):
        self.cfg = _stub_cfg(patience=5, max_epochs=20)
        self.machine = StageExitMachine(self.cfg)

    def test_max_epoch_without_gate_halts(self):
        train = _descending_history(20)
        val = _flat_history(20, 0.5)
        out = self.machine.evaluate(
            train, val, val_phys=1.0, val_energy=1.0,
            had_nan_inf=False, epoch_count=20,
        )
        self.assertEqual(out.disposition, StageDisposition.HALT)

    def test_midflight_disposition_is_none(self):
        # Gate unmet, no NaN, budget remaining → None (GAP-40-01 → B).
        train = _descending_history(5)
        val = _flat_history(5, 0.5)
        out = self.machine.evaluate(
            train, val, val_phys=1.0, val_energy=1.0,
            had_nan_inf=False, epoch_count=5,
        )
        self.assertIsNone(out.disposition)
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)

    def test_no_fallback_advancement(self):
        train = _descending_history(10)
        val = [0.1 + 0.01 * i for i in range(10)]  # val rising, not at min
        out = self.machine.evaluate(
            train, val, val_phys=1.0, val_energy=1.0,
            had_nan_inf=False, epoch_count=10,
        )
        self.assertIsNone(out.disposition)


class StagnationWindowHaltTests(unittest.TestCase):
    """WR-04: cover the stagnation-window HALT branch (stage_exit.py:195-213).

    Spec-grounded at ctl_instruction.md:1989-1990; one of HALT's two ratified
    triggers (GAP-40-02 → A). Pre-existing HaltAndMidFlightTests used histories
    shorter than stagnation_window, so the branch never executed.
    """

    def setUp(self):
        # Small stagnation_window keeps fixtures readable; large max_epochs
        # makes the max-epoch branch structurally unreachable (anti-vacuity).
        self.stag = 5
        self.max_epochs = 100
        self.cfg = _stub_cfg(
            patience=5, max_epochs=self.max_epochs, stagnation_window=self.stag,
        )
        self.machine = StageExitMachine(self.cfg)

    def test_stagnation_window_halts_when_val_never_recovers_running_min(self):
        # Min early, then a full stagnation_window of entries strictly above it.
        # Running min is over FULL history; trailing window never re-touches it.
        val = [0.1, 0.5, 0.5, 0.5, 0.5, 0.5]  # len 6 >= stag 5; last 5 all > 0.1
        train = _descending_history(len(val))  # no train plateau → ADVANCE unreachable
        epoch_count = 10
        # Anti-vacuity: epoch_count < max_epochs makes max-epoch HALT unreachable,
        # so a returned HALT can only come from the stagnation branch.
        self.assertLess(epoch_count, self.cfg.max_epochs)
        out = self.machine.evaluate(
            train, val, val_phys=1.0, val_energy=1.0,
            had_nan_inf=False, epoch_count=epoch_count,
        )
        self.assertEqual(out.disposition, StageDisposition.HALT)
        # Fixture-shape sanity (necessary but not sufficient discriminator —
        # max-epoch HALT also returns val_stable=False).
        self.assertFalse(out.val_stable)
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)

    def test_stagnation_window_does_not_fire_when_window_retouches_running_min(self):
        # Same shape but trailing window re-touches the running min → val_stable.
        val = [0.1, 0.5, 0.5, 0.5, 0.5, 0.1]
        train = _descending_history(len(val))
        epoch_count = 10
        self.assertLess(epoch_count, self.cfg.max_epochs)
        out = self.machine.evaluate(
            train, val, val_phys=1.0, val_energy=1.0,
            had_nan_inf=False, epoch_count=epoch_count,
        )
        # val_stable holds; gate otherwise unmet → mid-flight (GAP-40-01 → B).
        self.assertIsNone(out.disposition)
        self.assertTrue(out.val_stable)
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)

    def test_history_shorter_than_stagnation_window_does_not_fire(self):
        # Length boundary: one entry short of stag, otherwise stagnating.
        val = [0.1, 0.5, 0.5, 0.5]  # len 4 < stag 5
        train = _descending_history(len(val))
        epoch_count = 10
        self.assertLess(epoch_count, self.cfg.max_epochs)
        self.assertLess(len(val), self.stag)
        out = self.machine.evaluate(
            train, val, val_phys=1.0, val_energy=1.0,
            had_nan_inf=False, epoch_count=epoch_count,
        )
        self.assertIsNone(out.disposition)
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)


class PlateauSmootherMechanismTests(unittest.TestCase):
    """M3: drive the real TotalLossPlateauSmoother, not a boolean stub."""

    def test_fires_at_patience_not_before_local(self):
        patience = 8
        s = TotalLossPlateauSmoother(beta=0.98, patience=patience, eps_plateau=1e-5)
        fired = []
        for i in range(patience + 3):
            fired.append(s.update(1.0))
        # Before patience epochs of history indexed from 0, need at least
        # patience steps after init to compare L(i) vs L(i-patience).
        self.assertFalse(fired[patience - 1], "must not fire at patience-1")
        self.assertTrue(fired[patience], "must fire at patience-th qualifying epoch")

    def test_fires_at_production_patience_200(self):
        patience = 200
        s = TotalLossPlateauSmoother(beta=0.98, patience=patience, eps_plateau=1e-5)
        fired_at = None
        for i in range(patience + 2):
            if s.update(1.0) and fired_at is None:
                fired_at = i
        self.assertEqual(fired_at, patience)

    def test_violation_resets_counter(self):
        # Slightly looser eps so post-jump EMA settle is testable without
        # hundreds of steps (β=0.98 settles slowly toward a new level).
        patience = 6
        eps = 1e-2
        s = TotalLossPlateauSmoother(beta=0.98, patience=patience, eps_plateau=eps)
        for _ in range(patience + 1):
            s.update(1.0)
        self.assertTrue(s.plateau)
        # Large step change → relative EMA jump exceeds eps_plateau.
        s.update(100.0)
        self.assertFalse(s.plateau)
        # Must not re-fire immediately; lag-patience needs a further full
        # patience of post-violation samples before L(i) and L(i-patience)
        # are both flat at the new level.
        re_fire = []
        for _ in range(200):
            re_fire.append(s.update(100.0))
        self.assertFalse(re_fire[0], "must not re-fire immediately after reset")
        self.assertFalse(
            any(re_fire[:patience]),
            "must not re-fire before a full post-violation patience window",
        )
        self.assertTrue(any(re_fire[patience:]), "re-fires after full patience of flat")

    def test_descending_never_fires(self):
        patience = 10
        s = TotalLossPlateauSmoother(beta=0.98, patience=patience, eps_plateau=1e-5)
        for i in range(50):
            self.assertFalse(s.update(1.0 - 0.01 * i), f"fired on descending step {i}")

    def test_l_smooth_0_equals_first_loss(self):
        s = TotalLossPlateauSmoother(beta=0.98, patience=5, eps_plateau=1e-5)
        first = 3.14159
        s.update(first)
        self.assertTrue(math.isclose(s.l_smooth, first))


class SignatureAndConfigInjectionTests(unittest.TestCase):
    def test_evaluate_accepts_raw_history_only(self):
        cfg = _stub_cfg(patience=5)
        m = StageExitMachine(cfg)
        # Call with raw lists only — no pre-smoothed input.
        out = m.evaluate(
            [1.0] * 10, [0.5] * 10, 1e-5, 1e-5, False, 10,
        )
        self.assertIsInstance(out, StageExitOutcome)

    def test_thresholds_come_from_injected_config(self):
        # Stricter phys threshold fails a value that would pass the default.
        cfg = _stub_cfg(patience=5, eps_phys=1e-8)
        m = StageExitMachine(cfg)
        train = _plateaued_train_history(5)
        val = _flat_history(len(train), 0.5)
        out = m.evaluate(train, val, val_phys=1e-5, val_energy=1e-5,
                         had_nan_inf=False, epoch_count=len(train))
        self.assertFalse(out.phys_ok)
        self.assertNotEqual(out.disposition, StageDisposition.ADVANCE)

    def test_does_not_import_training_config(self):
        # Task 1 is independent of Task 2: production stage_exit must not
        # reference the config module; this test injects only a local stub.
        import inspect
        import pinn.training.stage_exit as se
        prod_src = inspect.getsource(se)
        self.assertEqual(prod_src.count("training.config"), 0)
        self.assertFalse(hasattr(se, "TrainingConfig"))
        self.assertIsInstance(_stub_cfg(), SimpleNamespace)


if __name__ == "__main__":
    unittest.main()
