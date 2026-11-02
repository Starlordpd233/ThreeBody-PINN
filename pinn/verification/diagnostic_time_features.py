"""Phase 67 (D-05): internal differentiable Fourier time features.

The EXP-04 input designs keep the model's PUBLIC contract exactly the
production one — ``forward(tau_ic13, masses)`` on the raw 14-dim
``[tau, IC13]`` vector — and encode inside the model: ordered harmonic
``sin``/``cos`` pairs are appended after the raw tau and IC13 columns, so
the frozen FEAS-01 scorer and the shared similarity logger differentiate the
model through its raw public input exactly as before, with no detach, NumPy
hop or external preprocessing between the input and the backbone.

The two declared designs are ``tau_ic13_fourier1`` (harmonics ``(1,)``,
internal dimension 16) and ``tau_ic13_fourier12`` (harmonics ``(1, 2)``,
internal dimension 18). The base frequency is ``N_in / T`` cycles per
physical time unit with ``N_in`` pinned per system from the committed Phase
59 census row, and the phase over normalized tau is
``pi * N_in * (tau + 1)`` — exactly ``2 * pi * f * t`` under the locked
global normalization ``tau = 2 t / T - 1``, which the constructor asserts by
construction (the phase coefficient is computed from that one conversion).
``ArchitectureSpec`` and the production network are never edited: the
diagnostic network subclasses the production class, builds from a copied
namespace spec whose internal ``input_dim`` is 16 or 18 (the first layer's
fan-in bound becomes ``1 / internal_dim``) and inherits the mass-weighted
COM forward unchanged.
"""

from __future__ import annotations

import dataclasses
import math
import numbers
from types import SimpleNamespace

import torch
import torch.nn as nn

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.network import SQRSkipResNetSIREN

__all__ = [
    "RAW_INPUT_DIM",
    "FOURIER_TIME_FEATURES",
    "FeatureRefused",
    "DiagnosticTimeFeatures",
    "DiagnosticTimeFeatureNetwork",
]

#: The production input width: raw ``[tau, IC13]`` is always accepted
#: publicly, encoded or not.
RAW_INPUT_DIM = 14

#: The declared encoded designs and their ordered harmonic tuples (D-05:
#: the fundamental, and the fundamental plus its second harmonic). A tuple
#: that is not exactly one of these shapes refuses at declaration time.
FOURIER_TIME_FEATURES = {
    "tau_ic13_fourier1": (1,),
    "tau_ic13_fourier12": (1, 2),
}


class FeatureRefused(ValueError):
    """A time-feature declaration, frequency or raw input is not usable."""


def _validated_harmonics(harmonics):
    """A non-empty, strictly ascending tuple of positive non-boolean ints."""
    if isinstance(harmonics, (str, bytes)) or not isinstance(harmonics, (tuple, list)):
        raise FeatureRefused(
            f"harmonics must be a tuple of positive integers in ascending "
            f"order; got {harmonics!r}"
        )
    if not harmonics:
        raise FeatureRefused("harmonics must name at least one harmonic; got ()")
    cleaned = []
    for value in harmonics:
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise FeatureRefused(
                f"each harmonic must be a positive integer (no booleans); "
                f"got {value!r}"
            )
        cleaned.append(int(value))
    for earlier, later in zip(cleaned, cleaned[1:]):
        if later <= earlier:
            raise FeatureRefused(
                f"harmonics must be strictly ascending; got {tuple(cleaned)!r}"
            )
    return tuple(cleaned)


def _validated_frequency(frequency_cycles_per_time):
    """A finite positive real frequency in cycles per physical time unit."""
    if isinstance(frequency_cycles_per_time, bool) \
            or not isinstance(frequency_cycles_per_time, numbers.Real):
        raise FeatureRefused(
            f"the feature frequency must be a finite positive real number of "
            f"cycles per physical time unit; got {frequency_cycles_per_time!r}"
        )
    value = float(frequency_cycles_per_time)
    if not math.isfinite(value) or value <= 0.0:
        raise FeatureRefused(
            f"the feature frequency must be a finite positive real number of "
            f"cycles per physical time unit; got {frequency_cycles_per_time!r}"
        )
    return value


class DiagnosticTimeFeatures(nn.Module):
    """The internal encoder: raw14 in, raw14 + ordered harmonic pairs out.

    Owns two persistent tensor buffers so the pinned frequencies and
    harmonics survive ``state_dict`` round-trips beside the parameters:
    ``frequency_cycles`` (the pinned physical frequency of each emitted
    pair, ``k * N_in / T``) and ``harmonics`` (the ordered harmonic list).
    The forward is pure differentiable tensor math on the input's dtype and
    device; the transform is applied to whatever raw ``[tau, IC13]`` samples
    the caller supplies, batched or single-row.
    """

    def __init__(self, harmonics, frequency_cycles_per_time, *,
                 dtype, device, t_characteristic=T_CHARACTERISTIC_TIME):
        super().__init__()
        self._harmonics = _validated_harmonics(harmonics)
        self.base_frequency_cycles = _validated_frequency(frequency_cycles_per_time)
        if isinstance(t_characteristic, bool) \
                or not isinstance(t_characteristic, numbers.Real):
            raise FeatureRefused(
                f"t_characteristic must be a finite positive real number; "
                f"got {t_characteristic!r}"
            )
        self.t_characteristic = float(t_characteristic)
        if not math.isfinite(self.t_characteristic) or self.t_characteristic <= 0.0:
            raise FeatureRefused(
                f"t_characteristic must be a finite positive real number; "
                f"got {t_characteristic!r}"
            )
        # The registered identity: N_in = f * T, and the phase over
        # normalized tau is pi * N_in * (tau + 1). Computed from this one
        # conversion so the encoder realizes exactly the registered
        # 2 * pi * f * t under tau = 2 t / T - 1; a non-finite implied N_in
        # (a frequency whose units do not convert) refuses before any tensor
        # is built.
        self.n_in = self.base_frequency_cycles * self.t_characteristic
        if not math.isfinite(self.n_in) or self.n_in <= 0.0:
            raise FeatureRefused(
                f"the registered frequency {self.base_frequency_cycles!r} cycles "
                f"per physical time unit does not convert to a finite positive "
                f"N_in under T = {self.t_characteristic!r}"
            )
        self.register_buffer(
            "harmonics",
            torch.tensor(list(self._harmonics), dtype=torch.int64, device=device),
        )
        self.register_buffer(
            "frequency_cycles",
            torch.tensor(
                [harmonic * self.base_frequency_cycles for harmonic in self._harmonics],
                dtype=dtype,
                device=device,
            ),
        )

    @property
    def harmonics_tuple(self):
        """The ordered harmonic tuple, as declared."""
        return self._harmonics

    @property
    def internal_input_dimension(self):
        """Raw14 plus one sin/cos pair per harmonic (14, 16 or 18)."""
        return RAW_INPUT_DIM + 2 * len(self._harmonics)

    def forward(self, tau_ic13):
        if not isinstance(tau_ic13, torch.Tensor):
            raise FeatureRefused(
                f"tau_ic13 must be a torch tensor of raw [tau, IC13] rows; "
                f"got {type(tau_ic13).__name__}"
            )
        if tau_ic13.dim() < 1 or int(tau_ic13.shape[-1]) != RAW_INPUT_DIM:
            raise FeatureRefused(
                f"tau_ic13 must carry the raw {RAW_INPUT_DIM}-dim "
                f"[tau, IC13] input; got shape {tuple(tau_ic13.shape)}"
            )
        raw = tau_ic13
        tau = raw[..., :1]
        # pi * T wrapped as the input's dtype/device, then scaled by the
        # pinned per-harmonic frequencies: phase_k = pi * k * N_in * (tau+1).
        pi_times_t = torch.as_tensor(
            math.pi * self.t_characteristic, dtype=raw.dtype, device=raw.device
        )
        phases = self.frequency_cycles.to(dtype=raw.dtype, device=raw.device) \
            * pi_times_t * (tau + 1.0)
        columns = [raw]
        for index in range(int(phases.shape[-1])):
            columns.append(torch.sin(phases[..., index:index + 1]))
            columns.append(torch.cos(phases[..., index:index + 1]))
        return torch.cat(columns, dim=-1)


class DiagnosticTimeFeatureNetwork(SQRSkipResNetSIREN):
    """The production network class over an encoded internal input.

    Built from a COPIED namespace spec whose ``input_dim`` alone is replaced
    by the internal dimension (16 or 18), with every other field — depths,
    widths, omegas, LayerNorm, skip cadence, seed — carried from the variant
    exactly as the raw path builds them, so the first layer reuses the
    production fan-in initializer at ``1 / internal_dim``. The public
    ``forward(tau_ic13, masses)`` (mass-weighted COM projection) is
    inherited unchanged; only ``_forward_unprojected`` encodes first.
    """

    def __init__(self, spec, *, harmonics, feature_frequency,
                 dtype, device, generator):
        if dataclasses.is_dataclass(spec) and not isinstance(spec, type):
            spec_fields = dict(dataclasses.asdict(spec))
        else:
            spec_fields = dict(vars(spec))
        if spec_fields.get("input_dim") != RAW_INPUT_DIM:
            raise FeatureRefused(
                f"the diagnostic model builds from the raw {RAW_INPUT_DIM}-dim "
                f"public spec; got input_dim {spec_fields.get('input_dim')!r}"
            )
        cleaned_harmonics = _validated_harmonics(harmonics)
        frequency = _validated_frequency(feature_frequency)
        internal = RAW_INPUT_DIM + 2 * len(cleaned_harmonics)
        encoded_spec = SimpleNamespace(**{**spec_fields, "input_dim": internal})
        super().__init__(encoded_spec, dtype=dtype, device=device, generator=generator)
        self.features = DiagnosticTimeFeatures(
            cleaned_harmonics, frequency, dtype=dtype, device=device
        )

    @property
    def internal_input_dimension(self):
        """The first layer's actual input width (14, 16 or 18)."""
        return int(self.input_layer.in_features)

    @property
    def first_layer_fan_in_bound(self):
        """The first layer's initialization bound, ``1 / internal_dim``."""
        return 1.0 / float(self.input_layer.in_features)

    def _forward_unprojected(self, tau_ic13):
        return super()._forward_unprojected(self.features(tau_ic13))
