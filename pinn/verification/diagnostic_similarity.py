"""Phase 65 (INST-08 / DIAG-09): the shared centred-neighbour time-signal measurement.

One implementation, ``measure_time_signal``, serves both the read-only probe
(DIAG-09, Plan 65-02) and the diagnostic fit logger (``log_similarity`` in
``diagnostic_fit``), per D-05. It is transcribed from the preserved 2026-10-27
exploratory originals (``probe_time_signal.py`` SHA-256 ``16db6c8c…a4f`` and
``probe_all_arms.py`` SHA-256 ``a4dea7d0…c8``, preserved in
65-CONTEXT.md ``specifics``):

* activations come from the network's own forward via temporary hooks on
  ``input_layer`` and each hidden layer, cleaned up in a ``finally`` block —
  the production mathematics and COM projection are never re-implemented;
* each activation is centred feature-wise across the time samples
  (``a - a.mean(dim=0)``) and successive centred rows are compared with
  ``F.cosine_similarity`` at the torch default epsilon, averaged over pairs;
* the first-layer frequency is ``abs(input_layer.weight[:, 0]) * omega_0 / pi``
  (cycles across the full normalized tau window), with its median and maximum —
  a RAW-input diagnostic: on an encoded (Phase 67 D-05) model that weight
  column describes only the raw tau channel of the complete encoded input, so
  the aggregate values are emitted as null with ``frequency_applicability``
  false, an explicit reason, and the encoder's pinned physical feature
  frequencies, harmonic list and internal input dimension instead;
* output movement is the centred output norm divided by the centred gold norm;
* the output-rate comparator is the RMS of the network's autograd d/dtau over
  the RMS of ``torch.gradient`` of the gold targets in the same normalized tau
  coordinate — a labelled comparator, not a physical velocity claim.

Physical time and normalized tau are recorded separately: adjacent gold
samples are physically 0.01 apart on the real corpus, which is NOT a claim
that normalized tau differs by 0.01. Samples are never sorted, merged or
dropped; a non-finite OR non-increasing time coordinate in either the
physical times or the raw tau column raises ``MeasurementRefused`` before any
forward (65-CLOSEOUT WR-06, applied for the encoded-input sample paths), and
undefined denominators and unusable sample sets raise ``MeasurementRefused``
instead of producing a success record. The adjacent-time cosine is associated
evidence — the comparison of centred hidden states at neighbouring times —
never a similarity pass bar (D-02/D-11).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn.functional as F

from pinn.verification.diagnostic_time_features import DiagnosticTimeFeatures

__all__ = [
    "ENCODED_FREQUENCY_REASON",
    "MeasurementRefused",
    "LayerRow",
    "TimeSignalMeasurement",
    "measure_time_signal",
]

#: Why the column-zero aggregate bandwidth is not applicable to an encoded
#: input (D-11/D-13: the field must never be mistakable for an overall
#: bandwidth claim).
ENCODED_FREQUENCY_REASON = (
    "not applicable: abs(input_layer.weight[:, 0]) * omega_0 / pi describes "
    "only the raw tau column of the first layer's weights, and the encoded "
    "input's time signal also spans the appended harmonic sin/cos features, "
    "so no single aggregate bandwidth describes the complete encoded input; "
    "the encoder's pinned per-harmonic physical frequencies are recorded "
    "instead"
)


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
    """The shared probe/logger measurement result.

    The encoded metadata fields (``frequency_applicability`` false, the
    reason, the pinned per-harmonic physical frequencies, the harmonic list
    and the internal input dimension) are ``None`` on a raw measurement, whose
    JSON keeps exactly the historical key set; an encoded measurement appends
    them and nulls the aggregate frequency values.
    """

    layers: tuple
    frequency_median: float
    frequency_max: float
    output_movement: float
    output_rate_ratio: float
    times_physical: tuple
    tau_values: tuple
    physical_dt_median: float
    n_points: int
    frequency_applicability: bool = True
    frequency_reason: str = None
    feature_frequency_cycles: tuple = None
    feature_harmonics: tuple = None
    internal_input_dimension: int = None

    def to_json_dict(self) -> dict:
        applicable = bool(self.frequency_applicability)
        payload = {
            "n_points": int(self.n_points),
            "layers": [
                {"name": row.name, "order": int(row.order),
                 "adjacent_cosine_mean": float(row.adjacent_cosine_mean)}
                for row in self.layers
            ],
            "first_layer_frequency": {
                "definition": "abs(input_layer.weight[:, 0]) * omega_0 / pi, "
                              "cycles across the full normalized tau window",
                "median": float(self.frequency_median) if applicable else None,
                "max": float(self.frequency_max) if applicable else None,
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
        if not applicable:
            payload["frequency_applicability"] = False
            payload["frequency_reason"] = str(self.frequency_reason)
            payload["feature_frequency_cycles"] = [
                float(value) for value in self.feature_frequency_cycles
            ]
            payload["feature_harmonics"] = [
                int(value) for value in self.feature_harmonics
            ]
            payload["internal_input_dimension"] = int(
                self.internal_input_dimension
            )
        return payload


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
    count = int(X.shape[0])
    if int(targets.shape[0]) != count:
        raise MeasurementRefused(
            f"tau_ic13 and targets must hold the same number of samples; got {count} "
            f"and {int(targets.shape[0])}"
        )
    if count < 2:
        raise MeasurementRefused(
            f"at least two samples are needed for a neighbour measurement; got {count}"
        )
    Y = targets.reshape(count, -1)
    if times_physical is None:
        raise MeasurementRefused("times_physical is None")
    if not isinstance(times_physical, torch.Tensor):
        times = torch.as_tensor(times_physical, dtype=torch.float64)
    else:
        times = times_physical.to(dtype=torch.float64)
    if times.dim() != 1 or int(times.shape[0]) != count:
        raise MeasurementRefused(
            f"times_physical must be 1-D with one entry per sample ({count}); "
            f"got {tuple(times.shape)}"
        )
    if masses is None:
        raise MeasurementRefused("masses is None")
    masses_tensor = masses if isinstance(masses, torch.Tensor) else torch.as_tensor(masses)
    if masses_tensor.dim() not in (1, 2) or (
        masses_tensor.dim() == 2 and int(masses_tensor.shape[0]) != count
    ):
        raise MeasurementRefused(
            f"masses must be (3,) or (N, 3) matching the samples; got {tuple(masses_tensor.shape)}"
        )

    # All value validation happens before the forward: samples are never sorted,
    # merged or dropped, so a non-finite or non-increasing time coordinate is a
    # refusal, never a reordered success (E-INST-empty / E-INST-precision).
    for tensor, what in (
        (X, "tau_ic13"),
        (Y, "targets"),
        (times, "times_physical"),
        (masses_tensor, "masses"),
    ):
        if not bool(torch.isfinite(tensor).all()):
            raise MeasurementRefused(f"{what} holds a non-finite value; refusing the measurement")
    if not bool((times.diff() > 0).all()):
        raise MeasurementRefused(
            "times_physical must be strictly increasing; non-increasing times are "
            "refused, never sorted"
        )
    tau = X[:, 0]
    # 65-CLOSEOUT WR-06 (applied for the Phase 67 encoded-input sample paths):
    # the raw tau column must also be strictly increasing before any hook is
    # attached — the gold-rate comparator differentiates against it, so a
    # non-increasing normalized coordinate is a refusal, never a reordering.
    if not bool((tau.diff() > 0).all()):
        raise MeasurementRefused(
            "tau_values must be strictly increasing; non-increasing normalized "
            "times are refused, never sorted"
        )
    flat_targets = Y.reshape(count, -1)
    centered_targets = flat_targets - flat_targets.mean(dim=0, keepdim=True)
    gold_norm = float(centered_targets.norm())
    if not gold_norm > 0.0:
        raise MeasurementRefused(
            "zero target variation: the centred gold norm is 0, so output movement "
            "and the rate comparator are undefined"
        )
    gold_rate = torch.gradient(flat_targets, spacing=(tau,), dim=0)[0]
    rms_gold = _finite_float(gold_rate.pow(2).mean().sqrt(), "gold d/dtau RMS")
    if not rms_gold > 0.0:
        raise MeasurementRefused(
            "the gold finite-difference rate is zero, so the rate comparator is undefined"
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

    # The column-zero aggregate bandwidth is a RAW-input diagnostic. On an
    # encoded (D-05) model that weight column describes only the raw tau
    # channel of the complete encoded input, so the aggregates are emitted as
    # null with an explicit reason and the encoder's pinned per-harmonic
    # physical frequencies, harmonic list and internal dimension instead
    # (T-67-06: the fields can never be mistaken for an overall bandwidth).
    encoder = getattr(model, "features", None)
    encoded = isinstance(encoder, DiagnosticTimeFeatures)
    if encoded:
        frequency_median = None
        frequency_max = None
        frequency_applicability = False
        frequency_reason = ENCODED_FREQUENCY_REASON
        feature_frequency_cycles = tuple(
            float(value) for value in encoder.frequency_cycles.tolist()
        )
        feature_harmonics = tuple(
            int(value) for value in encoder.harmonics.tolist()
        )
        internal_input_dimension = int(model.input_layer.in_features)
    else:
        omega = float(getattr(model.input_layer, "omega_0"))
        frequency = model.input_layer.weight[:, 0].detach().abs() * omega / math.pi
        frequency_median = _finite_float(frequency.median(), "frequency median")
        frequency_max = _finite_float(frequency.max(), "frequency max")
        frequency_applicability = True
        frequency_reason = None
        feature_frequency_cycles = None
        feature_harmonics = None
        internal_input_dimension = None

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
    rms_network = _finite_float(network_rate.pow(2).mean().sqrt(), "network d/dtau RMS")
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
        frequency_applicability=frequency_applicability,
        frequency_reason=frequency_reason,
        feature_frequency_cycles=feature_frequency_cycles,
        feature_harmonics=feature_harmonics,
        internal_input_dimension=internal_input_dimension,
    )
