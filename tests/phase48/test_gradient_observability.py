"""Phase 48 / INST-02 gradient-statistics conformance tests.

The first tests are deliberately small graph-local oracles.  They exercise the
same helper used by the Adam controller so the numeric contract is independent
of a large training fixture: raw norms are global parameter-gradient L2 norms,
and applied norms are the non-negative scheduled lambda times each raw norm.
"""

from __future__ import annotations

import math
import json
import logging
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest import mock

import pytest
import torch

from pinn.loss_catalog import LossTerms, LossWeights
from pinn.training.controllers import (
    _build_gradient_stats,
)
from pinn.training.step_log import JsonlStepHandler
from tests.phase40.test_optimizer_phase import _build_controller


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
        _terms(parameters), _weights(),
        parameters,
        provenance="pre_total_backward",
    )

    assert stats["grad_norm_raw_data"] == pytest.approx(math.sqrt(5.0))
    assert stats["grad_norm_raw_energy"] == pytest.approx(0.0)
    assert stats["grad_stats_complete"] is True


def test_disconnected_term_yields_zero_norm(monkeypatch: pytest.MonkeyPatch) -> None:
    parameters = (torch.nn.Parameter(torch.tensor(1.0)),)

    def fail_autograd_grad(*args, **kwargs):
        raise AssertionError("graphless terms must not call autograd.grad")

    monkeypatch.setattr(torch.autograd, "grad", fail_autograd_grad)
    terms = {
        name: torch.tensor(float(index + 1))
        for index, name in enumerate(("data", "ic", "phys", "energy", "angmom"))
    }
    stats = _build_gradient_stats(
        terms,
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


def test_adam_step_emits_complete_gradient_stats() -> None:
    with tempfile.TemporaryDirectory(prefix="phase48-adam-stats-") as tmp:
        controller = _build_controller(
            tmp, max_epochs=1, n_adam=1, validation_every=10_000,
        )
        model = controller.model

        def fake_compose(batch, anchor_ctx, weights):
            params = tuple(parameter for parameter in model.parameters())
            terms = {
                "data": (params[0] ** 2).sum(),
                "ic": (params[1] ** 2).sum(),
                "phys": (params[2] ** 2).sum(),
                "energy": (params[3] ** 2).sum(),
                "angmom": (params[4] ** 2).sum(),
            }
            total = sum(
                weight * terms[name]
                for name, weight in (
                    ("data", weights.lambda_data),
                    ("ic", weights.lambda_ic),
                    ("phys", weights.lambda_phys),
                    ("energy", weights.lambda_e),
                    ("angmom", weights.lambda_l),
                )
            )
            return LossTerms(
                data=terms["data"], ic=terms["ic"], phys=terms["phys"],
                energy=terms["energy"], angmom=terms["angmom"], total=total,
            )

        jsonl_path = Path(tmp) / "train.log.jsonl"
        handler = JsonlStepHandler(jsonl_path)
        logger = logging.getLogger("pinn.training.controllers")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        try:
            with mock.patch.object(
                controller, "_compose_loss_terms", side_effect=fake_compose,
            ):
                controller.run_stage(0)
            handler.flush()
        finally:
            logger.removeHandler(handler)
            handler.close()

        records = [json.loads(line) for line in jsonl_path.read_text().splitlines()]
        assert records
        record = records[-1]
        for term in ("data", "ic", "phys", "energy", "angmom"):
            assert math.isfinite(record[f"grad_norm_raw_{term}"])
            assert math.isfinite(record[f"grad_norm_applied_{term}"])
        assert record["grad_stats_provenance"] == "pre_total_backward"
        assert record["grad_stats_complete"] is True
        assert record["record_complete"] is True


def _run_fake_lbfgs_closure(controller, *, instrumented: bool):
    model = controller.model
    parameters = tuple(model.parameters())
    weights = LossWeights(lambda_ic=0.5, lambda_phys=2.0, lambda_e=0.0, lambda_l=0.25)
    fixed_batch = SimpleNamespace(data_points=SimpleNamespace())
    closure_state = {
        "non_finite": False,
        "last_loss": None,
        "gradient_stats": None,
    }

    def fake_data(model_, data_points, *, weight, chunk_size, dtype, device):
        weighted = float(weight) * (tuple(model_.parameters())[0] ** 2).sum() * 0.01
        weighted.backward()
        return weighted.detach()

    def fake_non_data(anchor_ctx):
        return {
            "ic": (parameters[1] ** 2).sum() * 0.01,
            "phys": (parameters[2] ** 2).sum() * 0.02,
            "energy": (parameters[3] ** 2).sum() * 0.03,
            "angmom": (parameters[4] ** 2).sum() * 0.04,
        }

    optimizer = torch.optim.LBFGS(
        model.parameters(), max_iter=1, line_search_fn=None,
    )
    closure = controller._make_lbfgs_closure(
        optimizer, fixed_batch, None, weights, 4, closure_state,
    )
    with mock.patch(
        "pinn.training.controllers.accumulate_chunked_data_term",
        side_effect=fake_data,
    ), mock.patch.object(controller, "_non_data_terms", side_effect=fake_non_data):
        if instrumented:
            result = optimizer.step(closure)
        else:
            with mock.patch(
                "pinn.training.controllers._build_gradient_stats",
                return_value={},
            ):
                result = optimizer.step(closure)
    return result, {key: value for key, value in closure_state.items()}, model


def test_lbfgs_gradient_stats_use_last_closure() -> None:
    with tempfile.TemporaryDirectory(prefix="phase48-lbfgs-stats-") as tmp:
        controller = _build_controller(
            tmp, max_epochs=2, n_adam=1, validation_every=1,
        )
        model = controller.model
        parameters = tuple(model.parameters())
        weights = LossWeights(lambda_ic=0.5, lambda_phys=2.0, lambda_e=0.0, lambda_l=0.25)
        fixed_batch = SimpleNamespace(data_points=SimpleNamespace())
        closure_state = {
            "non_finite": False,
            "last_loss": None,
            "gradient_stats": None,
        }
        calls = {"count": 0}

        def fake_data(model_, data_points, *, weight, chunk_size, dtype, device):
            calls["count"] += 1
            for parameter in model_.parameters():
                parameter.grad = torch.zeros_like(parameter)
            parameters[0].grad = torch.full_like(
                parameters[0], float(calls["count"]),
            )
            return torch.tensor(
                float(calls["count"]), dtype=dtype, device=device,
            )

        def fake_non_data(anchor_ctx):
            scale = float(calls["count"])
            return {
                "ic": scale * parameters[1].sum(),
                "phys": scale * parameters[2].sum(),
                "energy": scale * parameters[3].sum(),
                "angmom": scale * parameters[4].sum(),
            }

        optimizer = torch.optim.LBFGS(
            model.parameters(), max_iter=1, line_search_fn=None,
        )
        closure = controller._make_lbfgs_closure(
            optimizer, fixed_batch, None, weights, 4, closure_state,
        )
        with mock.patch(
            "pinn.training.controllers.accumulate_chunked_data_term",
            side_effect=fake_data,
        ), mock.patch.object(
            controller, "_non_data_terms", side_effect=fake_non_data,
        ):
            closure()
            first_stats = dict(closure_state["gradient_stats"])
            assert controller._last_non_data_terms is None
            closure()
            last_stats = dict(closure_state["gradient_stats"])
            assert controller._last_non_data_terms is None

        assert first_stats["grad_stats_provenance"] == "last_closure_evaluation"
        assert last_stats["grad_stats_provenance"] == "last_closure_evaluation"
        assert last_stats["grad_stats_complete"] is True
        assert last_stats["grad_norm_raw_data"] == pytest.approx(
            2.0 * math.sqrt(parameters[0].numel()),
        )
        assert last_stats["grad_norm_raw_ic"] == pytest.approx(
            2.0 * math.sqrt(parameters[1].numel()),
        )
        assert last_stats["grad_norm_applied_ic"] == pytest.approx(
            weights.lambda_ic * last_stats["grad_norm_raw_ic"],
        )
        assert last_stats["grad_norm_applied_energy"] == pytest.approx(0.0)
        assert last_stats["grad_norm_raw_data"] != first_stats["grad_norm_raw_data"]


def test_gradient_stats_survive_validation_stash_overwrite() -> None:
    with tempfile.TemporaryDirectory(prefix="phase48-validation-stats-") as tmp:
        controller = _build_controller(tmp, max_epochs=1, n_adam=1)
        weights = LossWeights(lambda_ic=0.5, lambda_phys=2.0, lambda_e=0.0, lambda_l=0.25)
        stats = {
            "grad_stats_provenance": "last_closure_evaluation",
            "grad_stats_complete": True,
        }
        for term in ("data", "ic", "phys", "energy", "angmom"):
            stats[f"grad_norm_raw_{term}"] = 1.0 + len(term)
            stats[f"grad_norm_applied_{term}"] = 2.0 + len(term)
        zero = torch.zeros((), dtype=controller._dtype, device=controller._device)
        loss_terms = LossTerms(
            data=zero, ic=zero, phys=zero, energy=zero, angmom=zero, total=zero,
        )
        controller._last_widened_details = {
            "ic": 999.0, "phys": 999.0, "energy": 999.0, "angmom": 999.0,
        }
        path = Path(tmp) / "train.log.jsonl"
        handler = JsonlStepHandler(path)
        logger = logging.getLogger("pinn.training.controllers")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        try:
            controller._log_step(
                step=1, loss_terms=loss_terms, lr=None, phase="2b", weights=weights,
                gradient_stats=stats,
            )
            handler.flush()
        finally:
            logger.removeHandler(handler)
            handler.close()
        record = json.loads(path.read_text().splitlines()[-1])
        assert record["grad_norm_raw_ic"] == stats["grad_norm_raw_ic"]
        assert record["grad_norm_applied_ic"] == stats["grad_norm_applied_ic"]
        assert record["grad_stats_provenance"] == "last_closure_evaluation"
        assert record["record_complete"] is True


def test_gradient_stats_missing_or_nonfinite_fail_completion() -> None:
    with tempfile.TemporaryDirectory(prefix="phase48-missing-stats-") as tmp:
        controller = _build_controller(tmp, max_epochs=1, n_adam=1)
        weights = LossWeights()
        zero = torch.zeros((), dtype=controller._dtype, device=controller._device)
        loss_terms = LossTerms(
            data=zero, ic=zero, phys=zero, energy=zero, angmom=zero, total=zero,
        )
        stats = {
            "grad_stats_provenance": "last_closure_evaluation",
            "grad_stats_complete": False,
            "grad_norm_raw_data": float("nan"),
            "grad_norm_applied_data": float("inf"),
        }
        path = Path(tmp) / "train.log.jsonl"
        handler = JsonlStepHandler(path)
        logger = logging.getLogger("pinn.training.controllers")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        try:
            controller._log_step(
                step=1, loss_terms=loss_terms, lr=None, phase="2b", weights=weights,
                step_completed=True, gradient_stats=stats,
            )
            handler.flush()
        finally:
            logger.removeHandler(handler)
            handler.close()
        record = json.loads(path.read_text().splitlines()[-1])
        assert record["grad_norm_raw_data"] is None
        assert record["grad_norm_applied_data"] is None
        assert record["grad_stats_complete"] is False
        assert record["record_complete"] is False
        assert {
            "grad_norm_raw_data", "grad_norm_applied_data",
        } <= set(record["nonfinite_keys"])


def test_lbfgs_gradient_stats_do_not_change_update() -> None:
    with tempfile.TemporaryDirectory(prefix="phase48-lbfgs-equivalence-") as tmp:
        instrumented = _build_controller(tmp, max_epochs=2, n_adam=1)
        control = _build_controller(tmp, max_epochs=2, n_adam=1)
        control.model.load_state_dict(instrumented.model.state_dict())
        _, _instrumented_state, instrumented_model = _run_fake_lbfgs_closure(
            instrumented, instrumented=True,
        )
        _, _control_state, control_model = _run_fake_lbfgs_closure(
            control, instrumented=False,
        )
        for left, right in zip(instrumented_model.parameters(), control_model.parameters()):
            assert torch.equal(left, right)
