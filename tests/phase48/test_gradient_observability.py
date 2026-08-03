"""Phase 48 / INST-02 gradient-statistics conformance tests.

The first tests are deliberately small graph-local oracles.  They exercise the
same helper used by the Adam controller so the numeric contract is independent
of a large training fixture: raw norms are global parameter-gradient L2 norms,
and applied norms are the non-negative scheduled lambda times each raw norm.
"""

from __future__ import annotations

import math

import pytest
import torch

from pinn.loss_catalog import LossWeights
from pinn.training.controllers import (
    _build_gradient_stats,
)


def _terms(parameters: tuple[torch.nn.Parameter, ...]) -> dict[str, torch.Tensor]:
    p0, p1, _unused = parameters
    return {
        "data": (p0 * torch.tensor([2.0, -1.0], dtype=p0.dtype)).sum(),
        "ic": (p0 * p0).sum(),
        "phys": 3.0 * p1,
        "energy": torch.tensor(4.0, dtype=p0.dtype),
        "angmom": p1 * p1,
    }


def _weights() -> LossWeights:
    return LossWeights(
        lambda_ic=0.5,
        lambda_phys=2.0,
        lambda_e=0.0,
        lambda_l=0.25,
    )


def test_adam_gradient_stats_match_hand_oracle() -> None:
    parameters = (
        torch.nn.Parameter(torch.tensor([1.0, -2.0])),
        torch.nn.Parameter(torch.tensor(3.0)),
        torch.nn.Parameter(torch.tensor(9.0)),
    )

    stats = _build_gradient_stats(
        _terms(parameters), _weights(), parameters,
        provenance="pre_total_backward",
    )

    expected_raw = {
        "data": math.sqrt(5.0),
        "ic": math.sqrt(20.0),
        "phys": 3.0,
        "energy": 0.0,
        "angmom": 6.0,
    }
    expected_lambda = {
        "data": 1.0,
        "ic": 0.5,
        "phys": 2.0,
        "energy": 0.0,
        "angmom": 0.25,
    }
    for name, raw in expected_raw.items():
        assert stats[f"grad_norm_raw_{name}"] == pytest.approx(raw)
        assert stats[f"grad_norm_applied_{name}"] == pytest.approx(
            expected_lambda[name] * raw,
        )
    assert stats["grad_stats_provenance"] == "pre_total_backward"
    assert stats["grad_stats_complete"] is True


def test_unused_parameter_contributes_zero() -> None:
    parameters = (
        torch.nn.Parameter(torch.tensor([1.0, -2.0])),
        torch.nn.Parameter(torch.tensor(3.0)),
        torch.nn.Parameter(torch.tensor(9.0)),
    )
    stats = _build_gradient_stats(
        {"data": (parameters[0] * 2.0).sum()},
        LossWeights(),
        parameters,
        provenance="pre_total_backward",
    )

    assert stats["grad_norm_raw_data"] == pytest.approx(math.sqrt(8.0))
    assert stats["grad_stats_complete"] is True


def test_disconnected_term_yields_zero_norm(monkeypatch: pytest.MonkeyPatch) -> None:
    parameters = (torch.nn.Parameter(torch.tensor(1.0)),)

    def fail_autograd_grad(*args, **kwargs):
        raise AssertionError("graphless terms must not call autograd.grad")

    monkeypatch.setattr(torch.autograd, "grad", fail_autograd_grad)
    stats = _build_gradient_stats(
        {"energy": torch.tensor(4.0)},
        LossWeights(lambda_e=0.0),
        parameters,
        provenance="pre_total_backward",
    )

    assert stats["grad_norm_raw_energy"] == 0.0
    assert stats["grad_norm_applied_energy"] == 0.0
    assert stats["grad_stats_complete"] is True


def test_adam_gradient_stats_do_not_change_update() -> None:
    initial = torch.tensor([1.0, -2.0])
    instrumented = torch.nn.Parameter(initial.clone())
    control = torch.nn.Parameter(initial.clone())
    weights = _weights()

    def graph(parameter: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        data = (parameter * torch.tensor([2.0, -1.0])).sum()
        total = (
            weights.lambda_data * data
            + weights.lambda_ic * (parameter * parameter).sum()
        )
        return data, total

    data, total = graph(instrumented)
    before_grad = instrumented.grad
    _build_gradient_stats(
        {"data": data, "ic": (instrumented * instrumented).sum()},
        weights,
        (instrumented,),
        provenance="pre_total_backward",
    )
    assert instrumented.grad is before_grad

    optimizer_instrumented = torch.optim.Adam([instrumented], lr=0.01)
    optimizer_instrumented.zero_grad(set_to_none=True)
    total.backward()
    clipped_instrumented = torch.nn.utils.clip_grad_norm_([instrumented], 0.75)
    optimizer_instrumented.step()

    data_control, total_control = graph(control)
    assert data_control.requires_grad
    optimizer_control = torch.optim.Adam([control], lr=0.01)
    optimizer_control.zero_grad(set_to_none=True)
    total_control.backward()
    clipped_control = torch.nn.utils.clip_grad_norm_([control], 0.75)
    optimizer_control.step()

    assert float(clipped_instrumented) == pytest.approx(float(clipped_control))
    assert torch.equal(instrumented, control)
