"""Phase 43 / 43-03 — real-data smoke composition + config seam (ACC-02).

Covers the Task-1 config seam (``data.source`` / ``data.root`` / ``run.smoke`` /
``stage.replay_count``), the admitted CPU/fp32 composition with a persisted
``splits.json``, the ~32-trajectory selection, the default-synthetic behavior,
and (Task 3) the CTX-79-preserving data-reachability preflight.

Skip discipline: every test that needs a not-yet-landed production symbol goes
through ``_require`` and SKIPS (never ERRORS) until the symbol exists — the
Phase-43 convention (``tests/phase43/__init__``).
"""

from __future__ import annotations

import importlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import torch

from tests.phase43 import _SKIP_PHRASE

CONFIG_MODULE = "pinn.training.config"
YAML_MODULE = "pinn.training.config_yaml"
TRAIN_MODULE = "pinn.train"

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SMOKE_YAML = _REPO_ROOT / "configs" / "smoke.yaml"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _valid_stage(**overrides):
    StageConfig = _require("StageConfig", CONFIG_MODULE)
    kwargs = dict(
        max_epochs=10,
        n_adam=5,
        stagnation_window=2,
        percentile_10_relaxation=0.1,
    )
    kwargs.update(overrides)
    return StageConfig(**kwargs)


# ---------------------------------------------------------------------------
# Config seam — data.source / data.root / run.smoke / stage.replay_count.
# ---------------------------------------------------------------------------
class ConfigSeamTests(unittest.TestCase):
    def test_data_config_defaults_to_synthetic(self):
        DataConfig = _require("DataConfig", CONFIG_MODULE)
        data = DataConfig()
        self.assertEqual(data.source, "synthetic")
        self.assertIsNone(data.root)

    def test_training_config_defaults_data_and_smoke(self):
        _require("DataConfig", CONFIG_MODULE)
        TrainingConfig = _require("TrainingConfig", CONFIG_MODULE)
        cfg = TrainingConfig(stage=_valid_stage())
        self.assertEqual(cfg.data.source, "synthetic")
        self.assertFalse(cfg.run.smoke)
        self.assertIsNone(cfg.stage.replay_count)

    def test_admitted_source_with_explicit_root_and_replay_count(self):
        DataConfig = _require("DataConfig", CONFIG_MODULE)
        RunConfig = _require("RunConfig", CONFIG_MODULE)
        TrainingConfig = _require("TrainingConfig", CONFIG_MODULE)
        cfg = TrainingConfig(
            stage=_valid_stage(replay_count=32),
            run=RunConfig(smoke=True),
            data=DataConfig(source="admitted", root="/some/Data"),
        )
        self.assertEqual(cfg.data.source, "admitted")
        self.assertEqual(cfg.data.root, "/some/Data")
        self.assertTrue(cfg.run.smoke)
        self.assertEqual(cfg.stage.replay_count, 32)

    def test_unsupported_data_source_rejected(self):
        DataConfig = _require("DataConfig", CONFIG_MODULE)
        with self.assertRaises(ValueError) as ctx:
            DataConfig(source="mystery")
        self.assertIn("data.source", str(ctx.exception))

    def test_empty_data_root_rejected(self):
        DataConfig = _require("DataConfig", CONFIG_MODULE)
        with self.assertRaises(ValueError):
            DataConfig(source="admitted", root="")

    def test_replay_count_must_be_positive(self):
        _require("StageConfig", CONFIG_MODULE)
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                _valid_stage(replay_count=bad)

    def test_run_smoke_must_be_bool(self):
        RunConfig = _require("RunConfig", CONFIG_MODULE)
        with self.assertRaises(ValueError):
            RunConfig(smoke="yes")


# ---------------------------------------------------------------------------
# YAML seam — smoke.yaml loads; unknown data.* keys fail loud; data optional.
# ---------------------------------------------------------------------------
class SmokeYamlTests(unittest.TestCase):
    def test_smoke_yaml_loads_supported_fields(self):
        load_config = _require("load_config", YAML_MODULE)
        self.assertTrue(_SMOKE_YAML.is_file(), f"missing {_SMOKE_YAML}")
        cfg = load_config(_SMOKE_YAML)
        self.assertEqual(cfg.data.source, "admitted")
        self.assertTrue(cfg.run.smoke)
        self.assertEqual(cfg.run.device, "mps")
        self.assertEqual(cfg.run.precision, "float32")
        self.assertEqual(cfg.stage.replay_count, 32)
        self.assertEqual(cfg.run.checkpoint.every_n_steps, 100)

    def test_config_without_data_section_defaults_synthetic(self):
        load_config = _require("load_config", YAML_MODULE)
        text = (
            "run:\n  seed: 0\n"
            "stage:\n  max_epochs: 10\n  n_adam: 5\n"
            "  stagnation_window: 2\n  percentile_10_relaxation: 0.1\n"
            "opt: {}\nloss: {}\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "no_data.yaml"
            path.write_text(text, encoding="utf-8")
            cfg = load_config(path)
        self.assertEqual(cfg.data.source, "synthetic")
        self.assertFalse(cfg.run.smoke)

    def test_unknown_data_key_raises_with_dotted_path(self):
        load_config = _require("load_config", YAML_MODULE)
        ConfigKeyError = _require("ConfigKeyError", YAML_MODULE)
        text = (
            "run:\n  seed: 0\n"
            "stage:\n  max_epochs: 10\n  n_adam: 5\n"
            "  stagnation_window: 2\n  percentile_10_relaxation: 0.1\n"
            "opt: {}\nloss: {}\n"
            "data:\n  source: admitted\n  rooot_typo: /x\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad_data.yaml"
            path.write_text(text, encoding="utf-8")
            with self.assertRaises(ConfigKeyError) as ctx:
                load_config(path)
        self.assertIn("data.rooot_typo", str(ctx.exception))


# ---------------------------------------------------------------------------
# Admitted composition — CPU/fp32 adapter, persisted splits.json, split views.
# ---------------------------------------------------------------------------
class AdmittedCompositionTests(unittest.TestCase):
    def _config(self, corpus_root, *, replay_count=32):
        DataConfig = _require("DataConfig", CONFIG_MODULE)
        RunConfig = _require("RunConfig", CONFIG_MODULE)
        TrainingConfig = _require("TrainingConfig", CONFIG_MODULE)
        return TrainingConfig(
            stage=_valid_stage(replay_count=replay_count),
            run=RunConfig(seed=7, smoke=True, run_name="stage0-smoke"),
            data=DataConfig(source="admitted", root=str(corpus_root)),
        )

    def test_admitted_builds_cpu_fp32_adapter_and_persists_manifest(self):
        _build_admitted_sources = _require("_build_admitted_sources", TRAIN_MODULE)
        StageIndex = _require("StageIndex", "pinn.data.splits")
        from tests.phase39._fixtures import TinyCorpus

        with TinyCorpus() as corpus:
            run_dir = corpus.run_dir
            cfg = self._config(corpus.data_root)
            train_index, val_index = _build_admitted_sources(cfg, run_dir)

            # splits.json persisted BEFORE returning the split views.
            self.assertTrue((run_dir / "splits.json").is_file())
            self.assertIsInstance(train_index, StageIndex)
            self.assertIsInstance(val_index, StageIndex)

            # The adapter behind both views is CPU/float32 regardless of the
            # model runtime the config declares (mps/float32).
            adapter = train_index._source
            self.assertEqual(adapter._dtype, torch.float32)
            self.assertEqual(adapter._device.type, "cpu")

    def test_admitted_reloads_existing_manifest_on_resume(self):
        _build_admitted_sources = _require("_build_admitted_sources", TRAIN_MODULE)
        from tests.phase39._fixtures import TinyCorpus

        with TinyCorpus() as corpus:
            run_dir = corpus.run_dir
            cfg = self._config(corpus.data_root)
            _build_admitted_sources(cfg, run_dir)
            manifest_bytes = (run_dir / "splits.json").read_bytes()
            # Second construction (resume) reuses the frozen manifest byte-for-byte.
            _build_admitted_sources(cfg, run_dir)
            self.assertEqual((run_dir / "splits.json").read_bytes(), manifest_bytes)


# ---------------------------------------------------------------------------
# ~32-trajectory selection — the existing DATA-05 selector honors replay_count,
# and RunController threads it while the default preserves the 240 population.
# ---------------------------------------------------------------------------
class ReplayCountSelectionTests(unittest.TestCase):
    def test_existing_selection_honors_replay_count(self):
        from pinn.data.batches import select_stage_records
        from tests.phase40._fixtures import make_stub_split_sources

        train, _ = make_stub_split_sources(n_train=40, n_validation=40)
        selected = select_stage_records(
            train, stage=0, rng=np.random.default_rng(0), replay_count=32,
        )
        self.assertEqual(len(selected.replay), 32)

    def _controller(self, tmp_dir, *, replay_count, n_train):
        from pinn.runtime import resolve_runtime
        from pinn.training.checkpoint import TorchSaveCheckpointStore
        from pinn.training.collocation_sampler import CollocationSampler
        from pinn.training.config import OptConfig, TrainingConfig
        from pinn.training.controllers import RunController
        from pinn.training.grad_clip import GradClipper
        from pinn.training.scheduled_weights import ScheduledWeights
        from pinn.training.stage_exit import StageExitMachine
        from tests.phase40._fixtures import make_stub_model, make_stub_split_sources

        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        train_source, validation_source = make_stub_split_sources(
            n_train=n_train, n_validation=n_train,
        )
        config = TrainingConfig(stage=_valid_stage(), opt=OptConfig(validation_every=1))
        controller = RunController(
            model, train_source, validation_source, config,
            ScheduledWeights(int(config.stage.n_adam), lambda_e_max=0.0),
            GradClipper(),
            CollocationSampler(2, np.random.default_rng(0)),
            StageExitMachine(config),
            TorchSaveCheckpointStore(tmp_dir),
            runtime,
            rng=np.random.default_rng(0),
            replay_count=replay_count,
        )
        return controller

    def test_run_controller_threads_replay_count(self):
        _require("RunController", "pinn.training.controllers")
        with tempfile.TemporaryDirectory() as tmp:
            rc = self._controller(tmp, replay_count=32, n_train=40)
            if not hasattr(rc, "_stage_batch"):
                raise unittest.SkipTest(
                    f"{_SKIP_PHRASE} pinn.training.controllers.RunController._stage_batch"
                )
            batch = rc._stage_batch(rc._train_source, stage=0, collocation_count=1)
            self.assertEqual(len(batch.replay_keys), 32)

    def test_run_controller_default_preserves_240(self):
        _require("RunController", "pinn.training.controllers")
        with tempfile.TemporaryDirectory() as tmp:
            rc = self._controller(tmp, replay_count=None, n_train=300)
            if not hasattr(rc, "_stage_batch"):
                raise unittest.SkipTest(
                    f"{_SKIP_PHRASE} pinn.training.controllers.RunController._stage_batch"
                )
            batch = rc._stage_batch(rc._train_source, stage=0, collocation_count=1)
            self.assertEqual(len(batch.replay_keys), 240)


# ---------------------------------------------------------------------------
# Default synthetic behavior is preserved (no corpus, no adapter).
# ---------------------------------------------------------------------------
class SyntheticDefaultTests(unittest.TestCase):
    def test_build_sources_defaults_to_synthetic_stub(self):
        _build_sources = _require("_build_sources", TRAIN_MODULE)
        TrainingConfig = _require("TrainingConfig", CONFIG_MODULE)
        cfg = TrainingConfig(stage=_valid_stage())
        with tempfile.TemporaryDirectory() as tmp:
            train_source, validation_source = _build_sources(cfg, Path(tmp))
        # The synthetic stub meets the 240 Stage-0 population floor.
        self.assertEqual(len(train_source.records_at_or_below(0)), 240)
        self.assertEqual(len(validation_source.records_at_or_below(0)), 240)


# ---------------------------------------------------------------------------
# Task 3 — CTX-79-preserving data-reachability preflight.
# ---------------------------------------------------------------------------
class DataReachabilityPreflightTests(unittest.TestCase):
    def _config(self, root):
        DataConfig = _require("DataConfig", CONFIG_MODULE)
        TrainingConfig = _require("TrainingConfig", CONFIG_MODULE)
        return TrainingConfig(
            stage=_valid_stage(),
            data=DataConfig(source="admitted", root=(str(root) if root else None)),
        )

    def _assert_names_both_fallbacks(self, message):
        self.assertIn("main-root checkout", message)
        self.assertIn("read-only", message)
        self.assertIn("data.root", message)

    def test_explicit_missing_root_refuses_naming_both_fallbacks(self):
        preflight = _require("_admitted_data_preflight", TRAIN_MODULE)
        DataReachabilityError = _require("DataReachabilityError", TRAIN_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "absent" / "Data"
            with self.assertRaises(DataReachabilityError) as ctx:
                preflight(self._config(missing))
        self._assert_names_both_fallbacks(str(ctx.exception))

    def test_explicit_existing_root_passes(self):
        preflight = _require("_admitted_data_preflight", TRAIN_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            resolved = preflight(self._config(tmp))
        self.assertEqual(resolved, Path(tmp).resolve())

    def test_default_root_missing_refuses_naming_both_fallbacks(self):
        preflight = _require("_admitted_data_preflight", TRAIN_MODULE)
        DataReachabilityError = _require("DataReachabilityError", TRAIN_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "no-corpus" / "Data"
            with mock.patch(
                "pinn.data.adapter.default_data_root", return_value=missing
            ):
                with self.assertRaises(DataReachabilityError) as ctx:
                    preflight(self._config(None))
        self._assert_names_both_fallbacks(str(ctx.exception))

    def test_default_root_success(self):
        preflight = _require("_admitted_data_preflight", TRAIN_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch(
                "pinn.data.adapter.default_data_root", return_value=Path(tmp)
            ):
                resolved = preflight(self._config(None))
        self.assertEqual(resolved, Path(tmp).resolve())

    def test_default_root_resolution_failure_refuses(self):
        preflight = _require("_admitted_data_preflight", TRAIN_MODULE)
        DataReachabilityError = _require("DataReachabilityError", TRAIN_MODULE)
        with mock.patch(
            "pinn.data.adapter.default_data_root",
            side_effect=RuntimeError("git unavailable"),
        ):
            with self.assertRaises(DataReachabilityError) as ctx:
                preflight(self._config(None))
        self._assert_names_both_fallbacks(str(ctx.exception))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
