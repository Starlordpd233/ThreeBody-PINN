"""Phase 41 — TrainingConfig field extensions + keyed YAML resolver (CTRL-01).

Task 2 (this file's config-field half) freezes the precision/device/strict-CPU
and ⚖ cadence/guard seam surface. Task 3 extends with YamlMappingTests /
NestedUnknownKeyTests / FrozenCopyRoundTripTests against config_yaml.py.
"""

from __future__ import annotations

import math
import tempfile
import unittest
from pathlib import Path

from tests.phase41.test_prohibitions import _require

CONFIG_MODULE = "pinn.training.config"
YAML_MODULE = "pinn.training.config_yaml"

TrainingConfig = _require("TrainingConfig", CONFIG_MODULE)
RunConfig = _require("RunConfig", CONFIG_MODULE)
StageConfig = _require("StageConfig", CONFIG_MODULE)
OptConfig = _require("OptConfig", CONFIG_MODULE)
LossConfig = _require("LossConfig", CONFIG_MODULE)
ConfigRequiredError = _require("ConfigRequiredError", CONFIG_MODULE)


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


# ---------------------------------------------------------------------------
# Task 2 — config field surface (precision/device/strict-CPU + ⚖ seams)
# ---------------------------------------------------------------------------


class RunFieldTests(unittest.TestCase):
    def test_precision_device_strict_cpu_construct(self):
        run = RunConfig(
            precision="float32",
            device="mps",
            strict_cpu_determinism=False,
        )
        self.assertEqual(run.precision, "float32")
        self.assertEqual(run.device, "mps")
        self.assertIs(run.strict_cpu_determinism, False)

    def test_defaults_match_d1p_production(self):
        run = RunConfig()
        self.assertEqual(run.precision, "float32")
        self.assertEqual(run.device, "mps")
        self.assertIs(run.strict_cpu_determinism, False)
        self.assertIsNone(run.run_name)

    def test_non_str_precision_raises_naming_field(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(precision=32)  # type: ignore[arg-type]
        self.assertIn("precision", str(ctx.exception))

    def test_empty_precision_raises_naming_field(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(precision="")
        self.assertIn("precision", str(ctx.exception))

    def test_empty_device_raises_naming_field(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(device="")
        self.assertIn("device", str(ctx.exception))

    def test_non_bool_strict_cpu_raises_naming_field(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(strict_cpu_determinism=1)  # type: ignore[arg-type]
        msg = str(ctx.exception)
        self.assertIn("strict_cpu_determinism", msg)

    def test_pair_validity_not_reencoded_here(self):
        # RunConfig only validates type/non-empty; pair validity is
        # resolve_runtime's job (CTX-20). An unsupported pair must construct.
        run = RunConfig(precision="float64", device="mps")
        self.assertEqual(run.precision, "float64")
        self.assertEqual(run.device, "mps")


class RunNameValidationTests(unittest.TestCase):
    """Cycle-2 codex MEDIUM — construction-time path-traversal prevention."""

    def test_valid_run_name_constructs(self):
        run = RunConfig(run_name="run-2026-test")
        self.assertEqual(run.run_name, "run-2026-test")

    def test_none_run_name_ok(self):
        run = RunConfig(run_name=None)
        self.assertIsNone(run.run_name)

    def test_empty_run_name_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="")
        self.assertIn("run_name", str(ctx.exception))

    def test_whitespace_run_name_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="   ")
        self.assertIn("run_name", str(ctx.exception))

    def test_path_separator_slash_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="a/b")
        self.assertIn("run_name", str(ctx.exception))

    def test_path_separator_backslash_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="a\\b")
        self.assertIn("run_name", str(ctx.exception))

    def test_dot_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name=".")
        self.assertIn("run_name", str(ctx.exception))

    def test_dotdot_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="..")
        self.assertIn("run_name", str(ctx.exception))

    def test_traversal_dotdot_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="../evil")
        self.assertIn("run_name", str(ctx.exception))

    def test_absolute_path_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="/abs/path")
        self.assertIn("run_name", str(ctx.exception))

    def test_control_character_raises(self):
        with self.assertRaises(ValueError) as ctx:
            RunConfig(run_name="bad\x00name")
        self.assertIn("run_name", str(ctx.exception))


class GuardConfigTests(unittest.TestCase):
    def test_guards_reachable_from_run(self):
        run = RunConfig()
        self.assertTrue(hasattr(run, "guards"))
        guards = run.guards
        self.assertTrue(hasattr(guards, "loss_explosion_ceiling"))
        self.assertTrue(hasattr(guards, "disk_floor_fraction"))
        self.assertTrue(hasattr(guards, "memory_watermark_fraction"))

    def test_fraction_outside_open_closed_unit_raises(self):
        GuardConfig = _require("GuardConfig", CONFIG_MODULE)
        with self.assertRaises(ValueError) as ctx:
            GuardConfig(
                loss_explosion_ceiling=1e6,
                disk_floor_fraction=0.0,  # not in (0, 1]
                memory_watermark_fraction=0.7,
            )
        self.assertIn("disk_floor_fraction", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            GuardConfig(
                loss_explosion_ceiling=1e6,
                disk_floor_fraction=0.05,
                memory_watermark_fraction=1.5,  # > 1
            )
        self.assertIn("memory_watermark_fraction", str(ctx.exception))

    def test_nonpositive_loss_explosion_raises(self):
        GuardConfig = _require("GuardConfig", CONFIG_MODULE)
        with self.assertRaises(ValueError) as ctx:
            GuardConfig(
                loss_explosion_ceiling=-1.0,
                disk_floor_fraction=0.05,
                memory_watermark_fraction=0.7,
            )
        self.assertIn("loss_explosion_ceiling", str(ctx.exception))

    def test_checkpoint_cadence_surface_reachable(self):
        run = RunConfig()
        self.assertTrue(hasattr(run, "checkpoint"))
        ck = run.checkpoint
        self.assertTrue(hasattr(ck, "every_n_steps"))
        self.assertTrue(hasattr(ck, "wall_clock_ceiling_s"))
        self.assertTrue(hasattr(ck, "rolling_keep"))
        self.assertTrue(hasattr(ck, "failure_keep"))
        self.assertEqual(ck.rolling_keep, 3)
        self.assertIsInstance(ck.failure_keep, int)
        self.assertGreater(ck.failure_keep, 0)

    def test_every_n_steps_must_be_positive_int(self):
        CheckpointCadence = _require("CheckpointCadence", CONFIG_MODULE)
        with self.assertRaises(ValueError) as ctx:
            CheckpointCadence(
                every_n_steps=0,
                wall_clock_ceiling_s=3600.0,
                rolling_keep=3,
                failure_keep=10,
            )
        self.assertIn("every_n_steps", str(ctx.exception))

    def test_wall_clock_ceiling_must_be_finite_positive(self):
        CheckpointCadence = _require("CheckpointCadence", CONFIG_MODULE)
        with self.assertRaises(ValueError) as ctx:
            CheckpointCadence(
                every_n_steps=100,
                wall_clock_ceiling_s=math.nan,
                rolling_keep=3,
                failure_keep=10,
            )
        self.assertIn("wall_clock_ceiling_s", str(ctx.exception))


class ProvisionalSeamTests(unittest.TestCase):
    """⚖ governance gate: provisional seams must appear in provisional_fields()."""

    def test_wall_clock_and_guards_in_provisional_fields(self):
        cfg = _valid_training()
        prov = cfg.provisional_fields()
        names = {p["name"] for p in prov}
        # D4-a wall-clock ceiling
        self.assertIn("run.checkpoint.wall_clock_ceiling_s", names)
        # R-1 guard thresholds
        self.assertIn("run.guards.loss_explosion_ceiling", names)
        self.assertIn("run.guards.disk_floor_fraction", names)
        self.assertIn("run.guards.memory_watermark_fraction", names)
        for p in prov:
            if p["name"].startswith("run.guards.") or p["name"] == (
                "run.checkpoint.wall_clock_ceiling_s"
            ):
                self.assertTrue(p.get("provisional") is True)
                self.assertTrue(p["provenance"])
                # Provenance must signal owner-carved / provisional, not ratified.
                prov_l = p["provenance"].lower()
                self.assertTrue(
                    "provisional" in prov_l
                    or "owner" in prov_l
                    or "⚖" in p["provenance"]
                    or "ratify" in prov_l,
                    f"provenance for {p['name']} must mark owner-carved/provisional: "
                    f"{p['provenance']!r}",
                )

    def test_frozen_config_rng_recording_format_decided_option_b(self):
        # GAP-41-01 RESOLVED-WITH-INSTRUCTION (2026-07-18): representation B —
        # config.yaml stays a pure TrainingConfig; four streams land in the
        # sibling runs/<name>/run_start_rng.pt plus every checkpoint.
        from pinn.training.config import FROZEN_CONFIG_RNG_RECORDING_FORMAT
        from pinn.training.determinism import RUN_START_RNG_FILENAME

        self.assertEqual(
            FROZEN_CONFIG_RNG_RECORDING_FORMAT, "sibling-artifact:run_start_rng.pt"
        )
        self.assertEqual(RUN_START_RNG_FILENAME, "run_start_rng.pt")
        # The seam is decided — it must no longer appear in the run-start
        # provisional (owner-attention) listing.
        cfg = _valid_training()
        names = {p["name"] for p in cfg.provisional_fields()}
        self.assertNotIn("frozen_config_rng_recording_format", names)

    def test_dataclass_equality_holds_with_new_fields(self):
        a = _valid_training()
        b = _valid_training()
        self.assertEqual(a, b)
        self.assertIsInstance(a.opt.adam_betas, tuple)
        self.assertEqual(a.opt.adam_betas, (0.9, 0.999))


# ---------------------------------------------------------------------------
# Task 3 — keyed YAML resolver (deferred until config_yaml lands)
# ---------------------------------------------------------------------------


class YamlMappingTests(unittest.TestCase):
    def test_keyed_yaml_resolves_field_for_field(self):
        load_config = _require("load_config", YAML_MODULE)
        yaml_text = """
run:
  seed: 7
  log_every: 2
  precision: float32
  device: mps
  strict_cpu_determinism: false
  run_name: yaml-roundtrip
stage:
  max_epochs: 100
  n_adam: 80
  stagnation_window: 10
  percentile_10_relaxation: 0.1
opt:
  adam_betas: [0.9, 0.999]
  adam_eps: 1.0e-8
  adam_lr_base: 0.001
  adam_lr_decay: 0.7
  lbfgs_history_size: 10
  lbfgs_max_iter: 20
  lbfgs_line_search: strong_wolfe
  validation_every: 10
  lbfgs_chunk_size: 1024
loss:
  lambda_e_max: 0.0
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cfg.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            cfg = load_config(path)
        self.assertEqual(cfg.run.seed, 7)
        self.assertEqual(cfg.run.precision, "float32")
        self.assertEqual(cfg.run.device, "mps")
        self.assertEqual(cfg.run.run_name, "yaml-roundtrip")
        self.assertEqual(cfg.stage.max_epochs, 100)
        self.assertEqual(cfg.stage.n_adam, 80)
        self.assertIsInstance(cfg.opt.adam_betas, tuple)
        self.assertEqual(cfg.opt.adam_betas, (0.9, 0.999))
        self.assertEqual(cfg.loss.lambda_e_max, 0.0)

    def test_unknown_key_raises_config_key_error_with_dotted_path(self):
        load_config = _require("load_config", YAML_MODULE)
        ConfigKeyError = _require("ConfigKeyError", YAML_MODULE)
        yaml_text = """
run:
  seed: 0
  mx_epochs_typo: 1
stage:
  max_epochs: 10
  n_adam: 5
  stagnation_window: 2
  percentile_10_relaxation: 0.1
opt: {}
loss: {}
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            with self.assertRaises(ConfigKeyError) as ctx:
                load_config(path)
        msg = str(ctx.exception)
        self.assertIn("run.mx_epochs_typo", msg)
        self.assertIsInstance(ctx.exception, ConfigKeyError)
        self.assertNotIsInstance(ctx.exception, ConfigRequiredError)

    def test_missing_file_raises_naming_path(self):
        load_config = _require("load_config", YAML_MODULE)
        missing = Path("/tmp/phase41-definitely-absent-config-xyz.yaml")
        with self.assertRaises(Exception) as ctx:
            load_config(missing)
        self.assertIn(str(missing), str(ctx.exception))

    def test_empty_file_raises_naming_path(self):
        load_config = _require("load_config", YAML_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.yaml"
            path.write_text("", encoding="utf-8")
            with self.assertRaises(Exception) as ctx:
                load_config(path)
            self.assertIn(str(path), str(ctx.exception))

    def test_missing_required_section_raises(self):
        load_config = _require("load_config", YAML_MODULE)
        yaml_text = """
run:
  seed: 0
opt: {}
loss: {}
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "no_stage.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            with self.assertRaises(Exception) as ctx:
                load_config(path)
            self.assertTrue(
                "stage" in str(ctx.exception).lower()
                or str(path) in str(ctx.exception)
            )


class NestedUnknownKeyTests(unittest.TestCase):
    def test_unknown_key_in_run_guards_full_dotted_path(self):
        load_config = _require("load_config", YAML_MODULE)
        ConfigKeyError = _require("ConfigKeyError", YAML_MODULE)
        yaml_text = """
run:
  seed: 0
  guards:
    loss_explosion_ceiling: 1.0e6
    disk_floor_fraction: 0.05
    memory_watermark_fraction: 0.7
    disk_floor_typo: 0.01
stage:
  max_epochs: 10
  n_adam: 5
  stagnation_window: 2
  percentile_10_relaxation: 0.1
opt: {}
loss: {}
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested_guards.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            with self.assertRaises(ConfigKeyError) as ctx:
                load_config(path)
        self.assertIn("run.guards.disk_floor_typo", str(ctx.exception))

    def test_unknown_key_in_run_checkpoint_full_dotted_path(self):
        load_config = _require("load_config", YAML_MODULE)
        ConfigKeyError = _require("ConfigKeyError", YAML_MODULE)
        yaml_text = """
run:
  seed: 0
  checkpoint:
    every_n_steps: 100
    wall_clock_ceiling_s: 3600
    rolling_keep: 3
    failure_keep: 10
    bad_cadence_key: 1
stage:
  max_epochs: 10
  n_adam: 5
  stagnation_window: 2
  percentile_10_relaxation: 0.1
opt: {}
loss: {}
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested_ckpt.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            with self.assertRaises(ConfigKeyError) as ctx:
                load_config(path)
        self.assertIn("run.checkpoint.bad_cadence_key", str(ctx.exception))


class FrozenCopyRoundTripTests(unittest.TestCase):
    def test_freeze_resolved_config_reparse_equal(self):
        load_config = _require("load_config", YAML_MODULE)
        freeze_resolved_config = _require("freeze_resolved_config", YAML_MODULE)
        cfg = _valid_training(
            run=RunConfig(
                seed=3,
                precision="float32",
                device="mps",
                run_name="freeze-test",
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "runs" / "freeze-test"
            run_dir.mkdir(parents=True)
            frozen_path = freeze_resolved_config(cfg, run_dir)
            self.assertEqual(frozen_path, run_dir / "config.yaml")
            self.assertTrue(frozen_path.is_file())
            reloaded = load_config(frozen_path)
            self.assertEqual(reloaded, cfg)
            self.assertIsInstance(reloaded.opt.adam_betas, tuple)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
