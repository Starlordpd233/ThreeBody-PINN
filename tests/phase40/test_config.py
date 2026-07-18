"""Phase 40 — TrainingConfig nested frozen dataclasses (CTX-42/39).

CTX-39 required fields raise if unset; GAP-40-02 → A enforces
N_Adam,k ≤ MAX_EPOCHS; CTX-38 thresholds are provisional-tagged defaults.
No YAML, no precision/device field.
"""
from __future__ import annotations

import math
import unittest

from tests.phase40.test_prohibitions import _require

MODULE = "pinn.training.config"

TrainingConfig = _require("TrainingConfig", MODULE)
RunConfig = _require("RunConfig", MODULE)
StageConfig = _require("StageConfig", MODULE)
OptConfig = _require("OptConfig", MODULE)
LossConfig = _require("LossConfig", MODULE)
ConfigRequiredError = _require("ConfigRequiredError", MODULE)


def _valid_stage(**overrides):
    base = dict(
        max_epochs=1000,
        n_adam=800,
        stagnation_window=50,
        percentile_10_relaxation=0.1,
    )
    base.update(overrides)
    return StageConfig(**base)


def _valid_training(**section_overrides):
    stage = section_overrides.pop("stage", _valid_stage())
    run = section_overrides.pop("run", RunConfig())
    opt = section_overrides.pop("opt", OptConfig())
    loss = section_overrides.pop("loss", LossConfig())
    return TrainingConfig(stage=stage, run=run, opt=opt, loss=loss)


class RequiredFieldTests(unittest.TestCase):
    def test_max_epochs_required(self):
        with self.assertRaises(ConfigRequiredError) as ctx:
            StageConfig(
                max_epochs=None,  # type: ignore[arg-type]
                n_adam=100,
                stagnation_window=50,
                percentile_10_relaxation=0.1,
            )
        self.assertIn("max_epochs", str(ctx.exception))

    def test_n_adam_required(self):
        with self.assertRaises(ConfigRequiredError) as ctx:
            StageConfig(
                max_epochs=100,
                n_adam=None,  # type: ignore[arg-type]
                stagnation_window=50,
                percentile_10_relaxation=0.1,
            )
        self.assertIn("n_adam", str(ctx.exception))

    def test_stagnation_window_required(self):
        with self.assertRaises(ConfigRequiredError) as ctx:
            StageConfig(
                max_epochs=100,
                n_adam=50,
                stagnation_window=None,  # type: ignore[arg-type]
                percentile_10_relaxation=0.1,
            )
        self.assertIn("stagnation_window", str(ctx.exception))

    def test_percentile_10_required(self):
        with self.assertRaises(ConfigRequiredError) as ctx:
            StageConfig(
                max_epochs=100,
                n_adam=50,
                stagnation_window=50,
                percentile_10_relaxation=None,  # type: ignore[arg-type]
            )
        self.assertIn("percentile_10_relaxation", str(ctx.exception))


class ValidationTests(unittest.TestCase):
    def test_negative_max_epochs_raises(self):
        with self.assertRaises(ValueError) as ctx:
            _valid_stage(max_epochs=-1)
        self.assertIn("max_epochs", str(ctx.exception))

    def test_nonfinite_threshold_raises(self):
        with self.assertRaises(ValueError) as ctx:
            _valid_stage(eps_phys=math.nan)
        self.assertIn("eps_phys", str(ctx.exception))

    def test_lambda_e_max_gt_one_raises(self):
        with self.assertRaises(ValueError) as ctx:
            LossConfig(lambda_e_max=1.5)
        self.assertIn("lambda_e_max", str(ctx.exception))

    def test_n_adam_gt_max_epochs_raises(self):
        with self.assertRaises(ValueError) as ctx:
            _valid_stage(max_epochs=100, n_adam=101)
        msg = str(ctx.exception)
        self.assertIn("n_adam", msg)
        self.assertIn("max_epochs", msg)

    def test_n_adam_eq_max_epochs_ok(self):
        s = _valid_stage(max_epochs=100, n_adam=100)
        self.assertEqual(s.n_adam, 100)
        self.assertEqual(s.max_epochs, 100)


class ConstructionTests(unittest.TestCase):
    def test_fully_valid_constructs_four_sections(self):
        cfg = _valid_training()
        self.assertIsInstance(cfg.run, RunConfig)
        self.assertIsInstance(cfg.stage, StageConfig)
        self.assertIsInstance(cfg.opt, OptConfig)
        self.assertIsInstance(cfg.loss, LossConfig)

    def test_provisional_threshold_defaults(self):
        cfg = _valid_training()
        self.assertEqual(cfg.stage.beta, 0.98)
        self.assertEqual(cfg.stage.patience, 200)
        self.assertEqual(cfg.stage.eps_plateau, 1e-5)
        self.assertEqual(cfg.stage.eps_phys, 1e-4)
        self.assertEqual(cfg.stage.eps_energy, 1e-4)
        self.assertEqual(cfg.stage.energy_floor_factor, 1e-4)

    def test_provisional_enumeration(self):
        cfg = _valid_training()
        prov = cfg.provisional_fields()
        self.assertIsInstance(prov, (list, tuple))
        names = {p["name"] for p in prov}
        self.assertIn("stage.beta", names)
        self.assertIn("stage.patience", names)
        self.assertIn("stage.eps_plateau", names)
        self.assertIn("stage.eps_phys", names)
        self.assertIn("stage.eps_energy", names)
        self.assertIn("opt.lbfgs_chunk_size", names)
        self.assertIn("opt.lbfgs_max_iter", names)
        for p in prov:
            self.assertTrue(p["provisional"] is True)
            self.assertTrue(p["provenance"])

    def test_opt_exposes_lbfgs_chunk_size(self):
        cfg = _valid_training()
        self.assertTrue(hasattr(cfg.opt, "lbfgs_chunk_size"))
        self.assertIsInstance(cfg.opt.lbfgs_chunk_size, int)
        self.assertGreater(cfg.opt.lbfgs_chunk_size, 0)

    def test_flat_gate_surface_for_stage_exit(self):
        # StageExitMachine reads flat attributes; TrainingConfig exposes them.
        cfg = _valid_training()
        for name in ("beta", "patience", "eps_plateau", "eps_phys",
                     "eps_energy", "max_epochs", "stagnation_window"):
            self.assertTrue(hasattr(cfg, name), f"missing flat attr {name}")
        self.assertEqual(cfg.beta, cfg.stage.beta)
        self.assertEqual(cfg.max_epochs, cfg.stage.max_epochs)

    def test_config_module_has_no_yaml_parser(self):
        # Phase 40 boundary retained: config.py is pure dataclasses.
        # Phase 41 (CTRL-01) adds precision/device on RunConfig and puts YAML
        # parsing in pinn.training.config_yaml — not here.
        import inspect
        import pinn.training.config as mod
        src = inspect.getsource(mod)
        self.assertNotIn("import yaml", src)
        self.assertNotIn("yaml.safe_load", src)
        cfg = _valid_training()
        # Top-level TrainingConfig still has no flat precision/device attrs
        # (they live under run.*, matching RESEARCH Pattern 2 paths).
        self.assertFalse(hasattr(cfg, "precision"))
        self.assertFalse(hasattr(cfg, "device"))
        # Phase 41 surface: run.precision / run.device are first-class fields.
        self.assertTrue(hasattr(cfg.run, "precision"))
        self.assertTrue(hasattr(cfg.run, "device"))


if __name__ == "__main__":
    unittest.main()
