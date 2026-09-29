"""Deterministic training-versus-validation causal telemetry ownership."""

from __future__ import annotations

import logging
import tempfile
import unittest

import numpy as np
import torch

from pinn.runtime import resolve_runtime
from pinn.train import _guard_causal_inputs, _synthetic_split_sources
from pinn.training.checkpoint import TorchSaveCheckpointStore
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import OptConfig, StageConfig, TrainingConfig
from pinn.training.controllers import RunController
from pinn.training.grad_clip import GradClipper
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine

from tests.phase50._fixtures import _StageAugmentedSource


class _ParameterizedProbeModel(torch.nn.Module):
    """Twice-differentiable probe with a trainable bias so Adam/L-BFGS can step."""

    def __init__(self):
        super().__init__()
        self.bias = torch.nn.Parameter(torch.zeros(9))

    def forward(self, tau_ic13, masses):
        tau = tau_ic13[:, :1]
        base = (
            tau_ic13[:, 1:10] * 0.05
            + masses.repeat_interleave(3, dim=1) * 0.01
            + tau.square()
        )
        return base + self.bias

TRAIN_W = {"w_min": 0.11, "w_mean": 0.22, "w_max": 0.33, "front_idx": 2}
VAL_W = {"w_min": 9.11, "w_mean": 9.22, "w_max": 9.33, "front_idx": 0}
TRAIN_RESIDUALS = [0.01, 0.02, 0.03]
VAL_RESIDUALS = [9.01, 9.02, 9.03]


class _ExtraCapture(logging.Handler):
    """Capture widened step extras emitted by ``RunController._log_step``."""

    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.records = []

    def emit(self, record):
        residual_keys = sorted(
            name for name in record.__dict__ if name.startswith("residuals_bin_")
        )
        self.records.append(
            {
                "phase": getattr(record, "phase", None),
                "step": getattr(record, "step", None),
                "w_min": getattr(record, "w_min", None),
                "w_mean": getattr(record, "w_mean", None),
                "w_max": getattr(record, "w_max", None),
                "front_idx": getattr(record, "front_idx", None),
                "n_collocation_rows": getattr(record, "n_collocation_rows", None),
                "n_bins": getattr(record, "n_bins", None),
                "residuals_per_bin": [getattr(record, key) for key in residual_keys],
            }
        )


def _build_controller(run_dir, *, n_adam, max_epochs, validation_every, guard_hook,
                      collocation_count=None):
    runtime = resolve_runtime("float64", "cpu")
    config = TrainingConfig(
        stage=StageConfig(
            max_epochs=max_epochs,
            n_adam=n_adam,
            stagnation_window=10,
            percentile_10_relaxation=0.1,
            beta=0.9,
            patience=5,
            eps_plateau=1e-5,
            eps_phys=1e-4,
            eps_energy=1e-4,
            energy_floor_factor=1e-4,
            collocation_count=collocation_count,
        ),
        opt=OptConfig(validation_every=validation_every, lbfgs_max_iter=2),
    )
    train_base, validation_base = _synthetic_split_sources(n_train=8, n_validation=4)
    train_source = _StageAugmentedSource(train_base, tuple(range(40_000, 40_008)))
    validation_source = _StageAugmentedSource(
        validation_base, tuple(range(50_000, 50_004))
    )
    return RunController(
        model=_ParameterizedProbeModel().to(
            dtype=runtime.dtype, device=runtime.torch_device
        ),
        train_source=train_source,
        validation_source=validation_source,
        config=config,
        scheduled_weights=ScheduledWeights(
            n_adam, lambda_e_max=0.0, lambda_l_max=0.0
        ),
        grad_clipper=GradClipper(),
        collocation_sampler=CollocationSampler(2, np.random.default_rng(0)),
        stage_exit_machine=StageExitMachine(config),
        checkpoint_store=TorchSaveCheckpointStore(run_dir),
        runtime=runtime,
        s_h=5.0,
        rng=np.random.default_rng(0),
        guard_hook=guard_hook,
        replay_count=4,
    )


def _stamp_distinct_composer_results(controller):
    """Overwrite composer stash with distinguishable training/validation sentinels."""

    original = controller._non_data_terms

    def stamped(anchor_ctx):
        terms = original(anchor_ctx)
        details = controller._last_widened_details
        if details is None:
            details = {}
            controller._last_widened_details = details
        if controller._model.training:
            details["w_n_stats"] = dict(TRAIN_W)
            details["residuals_per_bin"] = list(TRAIN_RESIDUALS)
        else:
            details["w_n_stats"] = dict(VAL_W)
            details["residuals_per_bin"] = list(VAL_RESIDUALS)
        return terms

    controller._non_data_terms = stamped

    # 57-07: the real (unmocked) Adam step no longer reaches
    # ``_non_data_terms`` at all -- Decision A's microbatched execution sets
    # ``_last_widened_details`` itself from its own Pass 1/Pass 2 computation.
    # Stamp that seam too, identically (overwrite after the real call, same
    # TRAIN_W sentinel since Adam is always in training mode on this path).
    original_adam_step = controller._run_adam_step_microbatched

    def stamped_adam_step(batch, anchor_ctx, weights, parameters, **kwargs):
        loss_terms, gradient_stats = original_adam_step(
            batch, anchor_ctx, weights, parameters, **kwargs,
        )
        details = controller._last_widened_details
        if details is None:
            details = {}
            controller._last_widened_details = details
        details["w_n_stats"] = dict(TRAIN_W)
        details["residuals_per_bin"] = list(TRAIN_RESIDUALS)
        return loss_terms, gradient_stats

    controller._run_adam_step_microbatched = stamped_adam_step


class CausalTelemetryOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.assertNotEqual(TRAIN_W, VAL_W)
        self.assertNotEqual(TRAIN_RESIDUALS, VAL_RESIDUALS)
        self.tmp = tempfile.TemporaryDirectory(prefix="phase50-causal-")
        self.guard_seen = []
        self.handler = _ExtraCapture()
        self.logger = logging.getLogger("pinn.training.controllers")
        self._previous_level = self.logger.level
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.logger.removeHandler(self.handler)
        self.logger.setLevel(self._previous_level)
        self.tmp.cleanup()

    def _guard_hook(self, controller, loss_terms, grad_norm, global_step, stage, phase):
        stats, n_colloc, _physics = _guard_causal_inputs(controller, str(phase))
        self.guard_seen.append(
            {
                "phase": str(phase),
                "w_n_stats": dict(stats or {}),
                "n_colloc": n_colloc,
                "n_collocation_rows": (controller._last_widened_details or {}).get(
                    "n_collocation_rows"
                ),
                "n_bins": (controller._last_widened_details or {}).get("n_bins"),
            }
        )
        return None

    def _logged(self, phase):
        return [record for record in self.handler.records if record["phase"] == phase]

    def _assert_training_owned(self, stats, residuals):
        self.assertEqual(stats["w_min"], TRAIN_W["w_min"])
        self.assertEqual(stats["w_mean"], TRAIN_W["w_mean"])
        self.assertEqual(stats["w_max"], TRAIN_W["w_max"])
        self.assertEqual(stats["front_idx"], TRAIN_W["front_idx"])
        self.assertEqual(residuals, TRAIN_RESIDUALS)
        self.assertNotEqual(stats, VAL_W)
        self.assertNotEqual(residuals, VAL_RESIDUALS)

    def test_adam_validation_step_keeps_training_owned_causal_telemetry(self):
        controller = _build_controller(
            self.tmp.name,
            n_adam=1,
            max_epochs=1,
            validation_every=1,
            guard_hook=self._guard_hook,
            collocation_count=2,
        )
        _stamp_distinct_composer_results(controller)
        controller.run_stage(0)

        adam_guards = [row for row in self.guard_seen if row["phase"] == "2a"]
        adam_logs = self._logged("2a")
        self.assertEqual(len(adam_guards), 1)
        self.assertEqual(len(adam_logs), 1)
        self.assertEqual(adam_guards[0]["w_n_stats"], TRAIN_W)
        self.assertEqual(adam_guards[0]["n_collocation_rows"], 2)
        self.assertEqual(
            adam_logs[0]["n_collocation_rows"], adam_guards[0]["n_collocation_rows"]
        )
        self.assertEqual(adam_logs[0]["n_bins"], adam_guards[0]["n_bins"])
        self._assert_training_owned(
            {
                "w_min": adam_logs[0]["w_min"],
                "w_mean": adam_logs[0]["w_mean"],
                "w_max": adam_logs[0]["w_max"],
                "front_idx": adam_logs[0]["front_idx"],
            },
            adam_logs[0]["residuals_per_bin"],
        )
        self.assertEqual(adam_guards[0]["w_n_stats"], {
            "w_min": adam_logs[0]["w_min"],
            "w_mean": adam_logs[0]["w_mean"],
            "w_max": adam_logs[0]["w_max"],
            "front_idx": adam_logs[0]["front_idx"],
        })

    def test_lbfgs_validation_step_keeps_training_owned_causal_telemetry(self):
        controller = _build_controller(
            self.tmp.name,
            n_adam=1,
            max_epochs=2,
            validation_every=1,
            guard_hook=self._guard_hook,
            collocation_count=2,
        )
        _stamp_distinct_composer_results(controller)
        controller.run_stage(0)

        lbfgs_guards = [row for row in self.guard_seen if row["phase"] == "2b"]
        lbfgs_logs = self._logged("2b")
        self.assertEqual(len(lbfgs_guards), 1)
        self.assertEqual(len(lbfgs_logs), 1)
        self.assertEqual(lbfgs_guards[0]["w_n_stats"], TRAIN_W)
        self.assertEqual(lbfgs_guards[0]["n_collocation_rows"], 2)
        self.assertEqual(
            lbfgs_logs[0]["n_collocation_rows"],
            lbfgs_guards[0]["n_collocation_rows"],
        )
        self.assertEqual(lbfgs_logs[0]["n_bins"], lbfgs_guards[0]["n_bins"])
        self._assert_training_owned(
            {
                "w_min": lbfgs_logs[0]["w_min"],
                "w_mean": lbfgs_logs[0]["w_mean"],
                "w_max": lbfgs_logs[0]["w_max"],
                "front_idx": lbfgs_logs[0]["front_idx"],
            },
            lbfgs_logs[0]["residuals_per_bin"],
        )
        self.assertEqual(lbfgs_guards[0]["w_n_stats"], {
            "w_min": lbfgs_logs[0]["w_min"],
            "w_mean": lbfgs_logs[0]["w_mean"],
            "w_max": lbfgs_logs[0]["w_max"],
            "front_idx": lbfgs_logs[0]["front_idx"],
        })


if __name__ == "__main__":
    unittest.main()
