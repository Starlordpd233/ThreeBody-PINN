"""Phase 43 / 43-03 — fresh-launch timing calibration (ACC-02, SPEC edge R2).

Covers ``RunController.s_per_step`` and the ``pinn.training.timing`` fail-closed
calibration: a valid on-disk record yields ``s_per_step * requested_steps``,
while an absent / malformed / non-finite / invalid / stale / mismatched /
git-unavailable record yields NO forecast — never a fabricated one. The writer
refuses to persist a non-finite / non-positive measurement.

Skip discipline: not-yet-landed production symbols route through ``_require`` and
SKIP (never ERROR) — the Phase-43 convention.
"""

from __future__ import annotations

import importlib
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

from tests.phase43 import _SKIP_PHRASE

TIMING_MODULE = "pinn.training.timing"
CONTROLLERS_MODULE = "pinn.training.controllers"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


_CONTROLLED_FINGERPRINT = {
    "device": "mps",
    "dtype": "torch.float32",
    "torch_version": "2.12.0",
    "python_version": "3.11.7",
    "git_head": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
    "git_head_available": True,
}


def _write_record(runs_root, **overrides):
    """Hand-write an on-disk calibration with a controlled fingerprint."""
    timing = importlib.import_module(TIMING_MODULE)
    stamp = overrides.pop("timestamp", datetime.now(timezone.utc).isoformat())
    fingerprint = overrides.pop("fingerprint", dict(_CONTROLLED_FINGERPRINT))
    record = {
        "schema_version": timing.TIMING_SCHEMA_VERSION,
        "s_per_step": 0.5,
        "full_stage0_steps": 1000,
        "forecast_seconds": 500.0,
        "timestamp": stamp,
        "fingerprint": fingerprint,
        "valid": True,
    }
    record.update(overrides)
    path = timing.calibration_path(runs_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# RunController.s_per_step property.
# ---------------------------------------------------------------------------
class SPerStepPropertyTests(unittest.TestCase):
    def _controller(self, tmp_dir):
        _require("RunController", CONTROLLERS_MODULE)
        from pinn.runtime import resolve_runtime
        from pinn.training.checkpoint import TorchSaveCheckpointStore
        from pinn.training.collocation_sampler import CollocationSampler
        from pinn.training.config import OptConfig, StageConfig, TrainingConfig
        from pinn.training.controllers import RunController
        from pinn.training.grad_clip import GradClipper
        from pinn.training.scheduled_weights import ScheduledWeights
        from pinn.training.stage_exit import StageExitMachine
        from tests.phase40._fixtures import make_stub_model, make_stub_split_sources

        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        train_source, validation_source = make_stub_split_sources(
            n_train=300, n_validation=300,
        )
        config = TrainingConfig(
            stage=StageConfig(
                max_epochs=10, n_adam=5, stagnation_window=2,
                percentile_10_relaxation=0.1,
            ),
            opt=OptConfig(validation_every=1),
        )
        return RunController(
            model, train_source, validation_source, config,
            ScheduledWeights(int(config.stage.n_adam), lambda_e_max=0.0),
            GradClipper(),
            CollocationSampler(2, np.random.default_rng(0)),
            StageExitMachine(config),
            TorchSaveCheckpointStore(tmp_dir),
            runtime,
            rng=np.random.default_rng(0),
            s_h=1.0,
        )

    def test_s_per_step_is_none_then_finite_after_steps(self):
        import math

        with tempfile.TemporaryDirectory() as tmp:
            rc = self._controller(tmp)
            if not hasattr(rc, "s_per_step"):
                raise unittest.SkipTest(
                    f"{_SKIP_PHRASE} {CONTROLLERS_MODULE}.RunController.s_per_step"
                )
            self.assertIsNone(rc.s_per_step)
            carrier = rc._scalar_loss_terms(1.0)
            rc._log_step(step=1, loss_terms=carrier, lr=None, phase="2a")
            rc._log_step(step=2, loss_terms=carrier, lr=None, phase="2a")
            self.assertIsNotNone(rc.s_per_step)
            self.assertIsInstance(rc.s_per_step, float)
            self.assertTrue(math.isfinite(rc.s_per_step))


# ---------------------------------------------------------------------------
# Calibration read/write + fail-closed forecast.
# ---------------------------------------------------------------------------
class CalibrationForecastTests(unittest.TestCase):
    def test_valid_on_disk_calibration_yields_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            _write_record(tmp, s_per_step=0.5)
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=dict(_CONTROLLED_FINGERPRINT),
            )
        self.assertEqual(got, 500.0)

    def test_write_calibration_round_trips_valid_record(self):
        write_calibration = _require("write_calibration", TIMING_MODULE)
        read_calibration = _require("read_calibration", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            write_calibration(
                s_per_step=0.25, full_stage0_steps=1000,
                precision="float32", device="mps", runs_root=tmp,
            )
            record = read_calibration(tmp)
        self.assertIsNotNone(record)
        self.assertIs(record["valid"], True)
        self.assertEqual(record["s_per_step"], 0.25)
        self.assertEqual(record["forecast_seconds"], 250.0)
        self.assertIn("git_head_available", record["fingerprint"])

    def test_writer_refuses_non_finite_or_non_positive(self):
        write_calibration = _require("write_calibration", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            for bad in (float("nan"), float("inf"), 0.0, -1.0):
                with self.assertRaises(ValueError):
                    write_calibration(
                        s_per_step=bad, full_stage0_steps=1000,
                        precision="float32", device="mps", runs_root=tmp,
                    )
            with self.assertRaises(ValueError):
                write_calibration(
                    s_per_step=0.5, full_stage0_steps=0,
                    precision="float32", device="mps", runs_root=tmp,
                )

    def test_absent_calibration_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=dict(_CONTROLLED_FINGERPRINT),
            )
        self.assertIsNone(got)

    def test_malformed_calibration_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        calibration_path = _require("calibration_path", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            path = calibration_path(tmp)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{ not json", encoding="utf-8")
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=dict(_CONTROLLED_FINGERPRINT),
            )
        self.assertIsNone(got)

    def test_invalid_flag_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            _write_record(tmp, valid=False)
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=dict(_CONTROLLED_FINGERPRINT),
            )
        self.assertIsNone(got)

    def test_non_finite_stored_s_per_step_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            # JSON cannot carry NaN in strict mode; a null/absent measurement is
            # the on-disk manifestation of a non-finite / partial smoke.
            _write_record(tmp, s_per_step=None)
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=dict(_CONTROLLED_FINGERPRINT),
            )
        self.assertIsNone(got)

    def test_fingerprint_mismatch_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        mismatched = dict(_CONTROLLED_FINGERPRINT)
        mismatched["torch_version"] = "9.9.9"
        with tempfile.TemporaryDirectory() as tmp:
            _write_record(tmp)  # written with the base fingerprint
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=mismatched,
            )
        self.assertIsNone(got)

    def test_git_unavailable_calibration_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        fp = dict(_CONTROLLED_FINGERPRINT)
        fp["git_head_available"] = False
        fp["git_head"] = None
        with tempfile.TemporaryDirectory() as tmp:
            _write_record(tmp, fingerprint=dict(fp))
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=dict(fp),
            )
        self.assertIsNone(got)

    def test_stale_calibration_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        old = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            _write_record(tmp, timestamp=old)
            got = forecast_from_calibration(
                tmp, requested_steps=1000, fingerprint=dict(_CONTROLLED_FINGERPRINT),
            )
        self.assertIsNone(got)

    def test_non_positive_requested_steps_has_no_forecast(self):
        forecast_from_calibration = _require("forecast_from_calibration", TIMING_MODULE)
        with tempfile.TemporaryDirectory() as tmp:
            _write_record(tmp)
            for bad in (0, -5):
                got = forecast_from_calibration(
                    tmp, requested_steps=bad, fingerprint=dict(_CONTROLLED_FINGERPRINT),
                )
                self.assertIsNone(got)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
