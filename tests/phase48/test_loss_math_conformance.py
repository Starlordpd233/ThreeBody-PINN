"""Assembly-boundary and independent-oracle tests for Phase 48.

These tests deliberately cross the controller-to-catalog seam.  A direct
``causal_physics_loss`` unit test would not prove that ``RunController``
assembles the locked residual statistic before passing it downstream.
"""

from __future__ import annotations

import math
from types import SimpleNamespace
from unittest import mock

import numpy as np
import pytest
import torch

import pinn.training.controllers as controllers
from pinn.loss_catalog import causal_physics_loss, data_huber_loss, resolve_causal_clip_facts
from pinn.runtime import resolve_runtime
from pinn.training.checkpoint import TorchSaveCheckpointStore
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import OptConfig, StageConfig, TrainingConfig
from pinn.training.grad_clip import GradClipper
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine
from tests.phase40._fixtures import make_stub_model, make_stub_split_sources


def _build_controller(tmp_path):
    """Build a real CPU/float64 RunController for seam-level tests."""
    runtime = resolve_runtime("float64", "cpu")
    model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
    train_source, validation_source = make_stub_split_sources(
        n_train=300, n_validation=300,
    )
    config = TrainingConfig(
        stage=StageConfig(
            max_epochs=1,
            n_adam=1,
            stagnation_window=10_000,
            percentile_10_relaxation=0.1,
            beta=0.9,
            patience=5,
            eps_plateau=1e-5,
            eps_phys=1e-4,
            eps_energy=1e-4,
        ),
        opt=OptConfig(validation_every=10_000, lbfgs_chunk_size=4, lbfgs_max_iter=2),
    )
    return controllers.RunController(
        model,
        train_source,
        validation_source,
        config,
        ScheduledWeights(1, lambda_e_max=0.0, lambda_l_max=0.0),
        GradClipper(),
        CollocationSampler(2, np.random.default_rng(0)),
        StageExitMachine(config),
        TorchSaveCheckpointStore(tmp_path),
        runtime,
        s_h=1.0,
        rng=np.random.default_rng(1),
    )


def test_rbar_assembly_value(tmp_path):
    """The real controller seam passes sum(residual**2)/3 to the catalog."""
    controller = _build_controller(tmp_path)
    dtype = controller._dtype
    device = controller._device
    residual = torch.tensor(
        [
            [[3.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[1.0, 2.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        ],
        dtype=dtype,
        device=device,
    )

    def fake_componentwise_du(_traj, times):
        n_times = int(times.numel())
        first = torch.zeros((n_times, 3, 3), dtype=dtype, device=device)
        second = residual.clone() if n_times == 2 else torch.zeros_like(first)
        return first, second

    def fake_acceleration(positions, _masses, *, dtype, device):
        return torch.zeros_like(positions, dtype=dtype, device=device)

    def traj(_u):
        return torch.zeros((3, 3), dtype=dtype, device=device)

    anchor_ctx = SimpleNamespace(
        traj=traj,
        masses=torch.ones(3, dtype=dtype, device=device),
        true_r0=torch.zeros((3, 3), dtype=dtype, device=device),
        true_v0=torch.zeros((3, 3), dtype=dtype, device=device),
        h0=-1.0,
        l0=torch.zeros(3, dtype=dtype, device=device),
        eps_h=1e-4,
        collocation_times=np.array([0.1, 0.2], dtype=np.float64),
    )

    captured = {}
    original_causal = controllers.causal_physics_loss

    def capture_rbar(rbar, **kwargs):
        captured["rbar"] = rbar.detach().clone()
        return original_causal(rbar, **kwargs)

    with (
        mock.patch.object(controllers, "componentwise_du", fake_componentwise_du),
        mock.patch.object(
            controllers, "softened_acceleration", fake_acceleration,
        ),
        mock.patch.object(
            controllers, "causal_physics_loss", side_effect=capture_rbar,
        ),
    ):
        controller._non_data_terms(anchor_ctx)

    expected = (residual ** 2).sum(dim=(-2, -1)) / 3.0
    former_component_mean = (residual ** 2).mean(dim=(-2, -1))
    assert torch.allclose(captured["rbar"], expected, rtol=0.0, atol=0.0)
    assert not torch.allclose(captured["rbar"], former_component_mean)


@pytest.mark.parametrize("n_times", [1, 2, 5])
def test_data_huber_mean_matches_hand_oracle(n_times):
    """Mean Huber equals an independent sum divided by ``9 * N_t``."""
    dtype = torch.float64
    device = torch.device("cpu")
    residual_pattern = torch.tensor(
        [
            [0.5, -1.5, 2.0],
            [0.0, -0.25, 1.25],
            [-2.5, 0.75, -1.0],
        ],
        dtype=dtype,
        device=device,
    )
    residual = residual_pattern.unsqueeze(0).repeat(n_times, 1, 1)
    predicted = residual
    target = torch.zeros_like(predicted)

    got = data_huber_loss(predicted, target, dtype=dtype, device=device)
    abs_residual = residual.abs()
    quadratic = 0.5 * residual.square()
    linear = abs_residual - 0.5
    hand_huber = torch.where(abs_residual <= 1.0, quadratic, linear)
    expected = hand_huber.sum() / (9.0 * n_times)

    assert torch.allclose(got, expected, rtol=1e-13, atol=1e-13)


@pytest.mark.parametrize(
    ("precision", "dtype"),
    [("float32", torch.float32), ("float64", torch.float64)],
)
def test_causal_clip_runtime_facts_drive_strict_positive_weights(precision, dtype):
    """The runtime-derived floor is the same value used by the causal loss."""
    device = torch.device("cpu")
    facts = resolve_causal_clip_facts(dtype, device)

    target = math.log(torch.finfo(dtype).tiny)
    floor = facts["causal_clip_exponent_floor"]
    assert facts["causal_clip_precision"] == precision
    assert math.isfinite(floor) and floor >= target
    assert facts["causal_clip_formula"] == (
        "exp(clamp_min(x_n, causal_clip_exponent_floor))"
    )
    assert facts["causal_clip_provenance"] == "log_smallest_normal:directed_up"

    # The second prefix is large enough to underflow without the clip.
    rbar = torch.tensor([1000.0, 1000.0], dtype=dtype, device=device)
    loss, details = causal_physics_loss(
        rbar, dtype=dtype, device=device, return_details=True,
    )
    weights = details["w_n"]
    assert torch.isfinite(loss)
    assert torch.equal(weights[:1], torch.ones(1, dtype=dtype, device=device))
    assert bool(torch.all((weights > 0) & (weights <= 1)).item())
    assert float(weights[1]) == facts["causal_clip_min_weight"]
