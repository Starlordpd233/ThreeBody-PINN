"""Dataset-free controller fixture for Phase-49 producer census tests."""

from __future__ import annotations

import numpy as np
import torch

from pinn.runtime import resolve_runtime
from pinn.train import _synthetic_split_sources
from pinn.training.checkpoint import TorchSaveCheckpointStore
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import StageConfig, TrainingConfig
from pinn.training.controllers import RunController
from pinn.training.grad_clip import GradClipper
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine


class _QuadraticProbeModel(torch.nn.Module):
    """Small twice-differentiable model for the producer-contract fixture."""

    def forward(self, tau_ic13, masses):
        tau = tau_ic13[:, :1]
        return (
            tau_ic13[:, 1:10] * 0.05
            + masses.repeat_interleave(3, dim=1) * 0.01
            + tau.square()
        )


def make_producer_controller(run_dir) -> RunController:
    runtime = resolve_runtime("float64", "cpu")
    config = TrainingConfig(
        stage=StageConfig(
            max_epochs=1000,
            n_adam=1000,
            stagnation_window=10,
            percentile_10_relaxation=0.1,
            beta=0.9,
            patience=5,
            eps_plateau=1e-5,
            eps_phys=1e-4,
            eps_energy=1e-4,
            energy_floor_factor=1e-4,
        )
    )
    train_source, validation_source = _synthetic_split_sources(
        n_train=3, n_validation=3
    )
    return RunController(
        model=_QuadraticProbeModel().to(
            dtype=runtime.dtype, device=runtime.torch_device
        ),
        train_source=train_source,
        validation_source=validation_source,
        config=config,
        scheduled_weights=ScheduledWeights(
            1000, lambda_e_max=0.0, lambda_l_max=0.0
        ),
        grad_clipper=GradClipper(),
        collocation_sampler=CollocationSampler(2, np.random.default_rng(0)),
        stage_exit_machine=StageExitMachine(config),
        checkpoint_store=TorchSaveCheckpointStore(run_dir),
        runtime=runtime,
        s_h=5.0,
        rng=np.random.default_rng(0),
    )
