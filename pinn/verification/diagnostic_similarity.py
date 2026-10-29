"""Phase 65 (INST-08 / DIAG-09): the shared centred-neighbour time-signal measurement.

One implementation, ``measure_time_signal``, serves both the read-only probe
(DIAG-09, Plan 65-02) and the diagnostic fit logger (``log_similarity`` in
``diagnostic_fit``), per D-05. It is transcribed from the preserved 2026-10-27
exploratory originals (``probe_time_signal.py`` SHA-256 ``16db5c8c…a4f`` and
``probe_all_arms.py`` SHA-256 ``a4dea7d0…c8``, preserved in
65-CONTEXT.md ``specifics``):

* activations come from the network's own forward via temporary hooks on
  ``input_layer`` and each hidden layer, cleaned up in a ``finally`` block —
  the production mathematics and COM projection are never re-implemented;
* each activation is centred feature-wise across the time samples
  (``a - a.mean(dim=0)``) and successive centred rows are compared with
  ``F.cosine_similarity`` at the torch default epsilon, averaged over pairs;
* the first-layer frequency is ``abs(input_layer.weight[:, 0]) * omega_0 / pi``
  (cycles across the full normalized tau window), with its median and maximum;
* output movement is the centred output norm divided by the centred gold norm;
* the output-rate comparator is the RMS of the network's autograd d/dtau over
  the RMS of ``torch.gradient`` of the gold targets in the same normalized tau
  coordinate — a labelled comparator, not a physical velocity claim.

Physical time and normalized tau are recorded separately: adjacent gold
samples are physically 0.01 apart on the real corpus, which is NOT a claim
that normalized tau differs by 0.01. Samples are never sorted, merged or
dropped; undefined denominators and unusable sample sets raise
``MeasurementRefused`` instead of producing a success record.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn.functional as F

__all__ = ["MeasurementRefused", "LayerRow", "TimeSignalMeasurement", "measure_time_signal"]


class MeasurementRefused(ValueError):
    """The measurement cannot be defined for these samples; nothing is published."""


@dataclass(frozen=True)
class LayerRow:
    """One measured layer boundary, in registration order."""

    name: str
    order: int
    adjacent_cosine_mean: float


@dataclass(frozen=True)
class TimeSignalMeasurement:
    """The shared probe/logger measurement result."""

    layers: tuple
    frequency_median: float
    frequency_max: float
    output_movement: float
    output_rate_ratio: float
    times_physical: tuple
    tau_values: tuple
    physical_dt_median: float
    n_points: int

    def to_json_dict(self) -> dict:
        return {
            "n_points": int(self.n_points),
            "layers": [
                {"name": row.name, "order": int(row.order),
                 "adjacent_cosine_mean": float(row.adjacent_cosine_mean)}
                for row in self.layers
            ],
            "first_layer_frequency": {
                "definition": "abs(input_layer.weight[:, 0]) * omega_0 / pi, "
                              "cycles across the full normalized tau window",
                "median": float(self.frequency_median),
                "max": float(self.frequency_max),
            },
            "output_movement": {
                "definition": "centered output norm / centered gold norm",
                "value": float(self.output_movement),
            },
            "output_rate_ratio": {
                "definition": "RMS network autograd d/dtau over RMS torch.gradient "
                              "gold d/dtau, both in normalized tau",
                "value": float(self.output_rate_ratio),
            },
            "times_physical": [float(value) for value in self.times_physical],
            "tau_values": [float(value) for value in self.tau_values],
            "physical_dt_median": {
                "definition": "median physical spacing of adjacent samples",
                "note": "physical time spacing; not normalized-tau spacing",
                "value": float(self.physical_dt_median),
            },
        }


def _as_2d_tensor(value, what):
    if value is None:
        raise MeasurementRefused(f"{what} is None")
    if not isinstance(value, torch.Tensor):
        raise MeasurementRefused(f"{what} must be a torch tensor; got {type(value).__name__}")
    if value.dim() != 2:
        raise MeasurementRefused(f"{what} must be 2-D (N, features); got {tuple(value.shape)}")
    return value


def _finite_float(value, what):
    number = float(value)
    if not math.isfinite(number):
        raise MeasurementRefused(f"{what} is not finite: {number!r}")
    return number


def measure_time_signal(model, tau_ic13, masses, targets, times_physical):
    """Measure the time signal of one network on one window of samples.

    All sample validation happens before the forward pass, so an unusable
    sample set is refused before any measurement is computed. Hooks are removed
    in a ``finally`` block even when the forward raises.
    """
    X = _as_2d_tensor(tau_ic13, "tau_ic13")
    if not isinstance(targets, torch.Tensor):
        raise MeasurementRefused(
            f"targets must be a torch tensor; got {type(targets).__name__}"
        )
    if targets.dim() < 2:
        raise MeasurementRefused(
            f"targets must hold one row per sample; got {tuple(targets.shape)}"
        )
    Y = targets.reshape(targets.shape[0], -1)
    count = int(X.shape[0])
    if int(Y.shape[0]) != count:
        raise MeasurementRefused(
            f"tau_ic13 and targets must hold the same number of samples; got {count} and {int(Y.shape[0])}"
        )
    if count < 2:
        raise MeasurementRefused(
            f"at least two samples are needed for a neighbour measurement; got {count}"
        )
    if not isinstance(times_physical, torch.Tensor):
        times = torch.as_tensor(times_physical, dtype=torch.float64)
    else:
        times = times_physical.to(dtype=torch.float64)
    if times.dim() != 1 or int(times.shape[0]) != count:
        raise MeasurementRefused(
            f"times_physical must be 1-D with one entry per sample ({count}); "
            f"got {tuple(times.shape)}"
        )
    masses_tensor = masses if isinstance(masses, torch.Tensor) else torch.as_tensor(masses)
    if masses_tensor.dim() not in (1, 2) or (
        masses_tensor.dim() == 2 and int(masses_tensor.shape[0]) != count
    ):
        raise MeasurementRefused(
            f"masses must be (3,) or (N, 3) matching the samples; got {tuple(masses_tensor.shape)}"
        )

    tau = X[:, 0]
    flat_targets = Y.reshape(count, -1)
    centered_targets = flat_targets - flat_targets.mean(dim=0, keepdim=True)
    gold_norm = float(centered_targets.norm())
    if not gold_norm > 0.0:
        raise MeasurementRefused(
            "zero target variation: the centred gold norm is 0, so output movement "
            "and the rate comparator are undefined"
        )

    captured = []

    def _capture(name, order):
        def hook(_module, _inputs, output):
            captured.append((order, name, output.detach()))
        return hook

    hooks = []
    try:
        hooks.append(model.input_layer.register_forward_hook(_capture("input", 0)))
        for order, layer in enumerate(model.hidden_layers, 1):
            hooks.append(layer.register_forward_hook(_capture(f"h{order}", order)))
        leaf = X.clone().requires_grad_(True)
        out = model(leaf, masses_tensor)
    finally:
        for handle in hooks:
            handle.remove()

    rows = []
    for order, name, activation in sorted(captured, key=lambda item: item[0]):
        centered = activation - activation.mean(dim=0, keepdim=True)
        adjacent = F.cosine_similarity(centered[:-1], centered[1:], dim=1).mean()
        rows.append(LayerRow(name=name, order=order,
                             adjacent_cosine_mean=_finite_float(adjacent, f"{name} cosine")))

    omega = float(getattr(model.input_layer, "omega_0"))
    frequency = model.input_layer.weight[:, 0].detach().abs() * omega / math.pi
    frequency_median = _finite_float(frequency.median(), "frequency median")
    frequency_max = _finite_float(frequency.max(), "frequency max")

    if out.dim() != 2 or int(out.shape[0]) != count:
        raise MeasurementRefused(
            f"the forward output must hold one row per sample ({count}); got {tuple(out.shape)}"
        )
    centered_out = out - out.mean(dim=0, keepdim=True)
    movement = _finite_float(float(centered_out.detach().norm()) / gold_norm, "output movement")

    columns = []
    for index in range(out.shape[1]):
        gradient = torch.autograd.grad(
            out[:, index].sum(), leaf, retain_graph=index < out.shape[1] - 1
        )[0][:, 0]
        columns.append(gradient.detach())
    network_rate = torch.stack(columns, dim=1)
    gold_rate = torch.gradient(flat_targets, spacing=(tau,), dim=0)[0]
    rms_network = _finite_float(network_rate.pow(2).mean().sqrt(), "network d/dtau RMS")
    rms_gold = _finite_float(gold_rate.pow(2).mean().sqrt(), "gold d/dtau RMS")
    if not rms_gold > 0.0:
        raise MeasurementRefused(
            "the gold finite-difference rate is zero, so the rate comparator is undefined"
        )
    rate_ratio = _finite_float(rms_network / rms_gold, "output rate ratio")

    differences = times[:-1].diff() if count > 1 else torch.zeros(0, dtype=torch.float64)
    dt_median = _finite_float(differences.median(), "physical spacing median")
    return TimeSignalMeasurement(
        layers=tuple(rows),
        frequency_median=frequency_median,
        frequency_max=frequency_max,
        output_movement=movement,
        output_rate_ratio=rate_ratio,
        times_physical=tuple(float(value) for value in times.tolist()),
        tau_values=tuple(float(value) for value in tau.tolist()),
        physical_dt_median=dt_median,
        n_points=count,
    )
