"""Phase 38 / NET-01 — SQR-SkipResNet-SIREN backbone with projected-only forward.

Rebuilt from ``pinn_architecture.md`` §2.1/§2.2/§2.3/§2.4 (NOT from the v1.3-era
``pinn/basic_architecture.py`` — CTX-17 bans that as a pattern source). The
network is instantiated entirely from an ``ArchitectureSpec`` (config-supplied
topology) and builds every parameter directly on the resolved dtype/device.

Topology (§2.4 Table 1):
    * Input SIREN layer  : 14 -> 256, omega_0 = first_omega_0 = 30,
                           weights U[-1/n_in, 1/n_in] (n_in = 14).
    * 12 hidden layers   : 256 -> 256 each, omega_0 = hidden_omega_0 = 1,
                           weights U[-sqrt(6/n_in)/hidden_omega_0,
                                     +sqrt(6/n_in)/hidden_omega_0]
                           (n_in = 256). Odd-numbered layers (1,3,...,11) use
                           the SQR-SkipResNet update
                           x = SIREN(x_prev) + (LayerNorm(x_prev))**p (p=2)
                           with LayerNorm(elementwise_affine=False, eps=1e-5);
                           even-numbered layers (2,4,...,12) are plain SIREN.
    * Output head        : 256 -> 9 linear (no activation).

Public contract (NET-02 / CTX-21):
    * ``forward(tau_ic13, masses)`` returns the mass-weighted-COM-PROJECTED
      positions as the ONLY public output. The raw 9-dim tensor is reachable
      solely through the explicitly private ``_forward_unprojected`` hook.
    * ``masses`` are the ordered RAW masses supplied explicitly by the caller
      (unrecoverable from the tanh-normalized IC13 mass slots; never assumed
      equal). ``tau_ic13`` (14-dim) is supplied WHOLESALE — the model never
      synthesizes or re-normalizes the IC13 slice and imposes no IC13
      normalization contract.

Construction discipline (CTX-14 / ENV-04 / edge R1):
    * Constructor accepts the resolved ``dtype``/``device`` explicitly and
      builds every parameter on them directly (no ``.to()`` afterthought, no
      ``torch.set_default_dtype``, no availability probe).
    * Parameters are raw ``nn.Parameter`` tensors built on (dtype, device) and
      initialized with a LOCAL seeded ``torch.Generator`` — the global RNG is
      never touched and the global default dtype is never mutated. Same
      ``spec + seed`` produces bitwise-identical parameters.
    * Scalars that would otherwise be Python-float x tensor are wrapped as
      same-dtype/device tensors (MPS discipline,
      ``componentwise_ad.py:62-76``).
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from pinn.architecture_spec import ArchitectureSpec
from pinn.com_projection import project_com

__all__ = ["SQRSkipResNetSIREN", "build_network"]


class _SIRENLayer(nn.Module):
    """One SIREN sine layer: ``sin(omega_0 * (W x + b))`` with principled init.

    The weight and bias are raw ``nn.Parameter`` tensors built directly on
    ``(dtype, device)`` and filled by ``Tensor.uniform_(generator=...)`` using
    the caller-supplied LOCAL generator — the global RNG is never advanced.

    Init bounds (§2.2 / :983):
        * is_first=True : U[-1/n_in, 1/n_in]            (omega_0 = first_omega_0)
        * is_first=False: U[-sqrt(6/n_in)/omega_0, ...] (omega_0 = hidden_omega_0)

    Bias is initialized with the SAME bound as the layer's weights (the spec is
    silent on bias; this is the conventional, internally-consistent SIREN
    choice and a mechanical decision, not a physics adjudication).
    """

    def __init__(self, in_features, out_features, omega_0, *, is_first,
                 dtype, device, generator):
        super().__init__()
        self.in_features = int(in_features)
        self.out_features = int(out_features)
        self.omega_0 = float(omega_0)
        self.is_first = bool(is_first)
        if self.is_first:
            bound = 1.0 / self.in_features
        else:
            bound = math.sqrt(6.0 / self.in_features) / self.omega_0
        weight = torch.empty(self.out_features, self.in_features,
                             dtype=dtype, device=device)
        bias = torch.empty(self.out_features, dtype=dtype, device=device)
        # explicit generator -> no global RNG mutation.
        weight.uniform_(-bound, bound, generator=generator)
        bias.uniform_(-bound, bound, generator=generator)
        self.weight = nn.Parameter(weight)
        self.bias = nn.Parameter(bias)

    def forward(self, x):
        # Wrap omega_0 as a same-dtype/device tensor so the path never does
        # Python-float x tensor on MPS (componentwise_ad MPS discipline).
        omega = torch.as_tensor(self.omega_0, dtype=x.dtype, device=x.device)
        return torch.sin(omega * F.linear(x, self.weight, self.bias))


class _OddSkipBlock(nn.Module):
    """SQR-SkipResNet odd-layer block (§2.3).

    ``forward(x_prev) = siren(x_prev) + (LayerNorm(x_prev)) ** power_p``

    Both the SIREN block and the LayerNorm consume the SAME ``x_prev`` (the
    input to this layer). LayerNorm uses ``elementwise_affine=False`` and
    ``eps=1e-5`` (§2.4, ARCH-02); with affine disabled it has no parameters,
    so its dtype/device follow the input.
    """

    def __init__(self, width, *, omega_0, power_p, layernorm_eps,
                 layernorm_elementwise_affine, dtype, device, generator):
        super().__init__()
        self.siren = _SIRENLayer(width, width, omega_0=omega_0, is_first=False,
                                 dtype=dtype, device=device, generator=generator)
        self.layernorm = nn.LayerNorm(width, eps=layernorm_eps,
                                      elementwise_affine=layernorm_elementwise_affine)
        self.power_p = int(power_p)

    def forward(self, x_prev):
        return self.siren(x_prev) + self.layernorm(x_prev) ** self.power_p


class _LinearHead(nn.Module):
    """Linear output head (no activation). 256 -> 9.

    The spec (§2.4 Table 1) fixes the output as linear but is silent on its
    init. We initialize weight and bias uniformly in U[-1/sqrt(n_in),
    +1/sqrt(n_in)] (PyTorch's default Linear fan-in bound) using the LOCAL
    generator so construction stays deterministic and global-RNG-free. This is
    a mechanical readout-init choice, not a physics adjudication.
    """

    def __init__(self, in_features, out_features, *, dtype, device, generator):
        super().__init__()
        self.in_features = int(in_features)
        self.out_features = int(out_features)
        bound = 1.0 / math.sqrt(self.in_features)
        weight = torch.empty(self.out_features, self.in_features,
                             dtype=dtype, device=device)
        bias = torch.empty(self.out_features, dtype=dtype, device=device)
        weight.uniform_(-bound, bound, generator=generator)
        bias.uniform_(-bound, bound, generator=generator)
        self.weight = nn.Parameter(weight)
        self.bias = nn.Parameter(bias)

    def forward(self, x):
        return F.linear(x, self.weight, self.bias)


class SQRSkipResNetSIREN(nn.Module):
    """SQR-SkipResNet-SIREN backbone instantiated from an ArchitectureSpec.

    The public ``forward(tau_ic13, masses)`` returns the COM-projected
    positions as the ONLY public output. The raw 9-dim tensor is exposed
    solely through the private ``_forward_unprojected`` test/internal hook.
    """

    def __init__(self, spec, *, dtype, device, generator):
        super().__init__()
        self._build_dtype = dtype
        self._build_device = device
        self.power_p = int(spec.power_p)
        self.first_omega_0 = float(spec.first_omega_0)
        self.hidden_omega_0 = float(spec.hidden_omega_0)

        # The "first" SIREN layer: 14 -> 256, omega_0 = first_omega_0 = 30.
        self.input_layer = _SIRENLayer(
            spec.input_dim, spec.hidden_width,
            omega_0=spec.first_omega_0, is_first=True,
            dtype=dtype, device=device, generator=generator)

        # 12 hidden layers of width 256; odd-numbered (1,3,...,11) are
        # SQR-SkipResNet blocks, even-numbered (2,4,...,12) are plain SIREN.
        layers = []
        for layer_num in range(1, spec.hidden_depth + 1):
            if layer_num % 2 == 1:
                layers.append(_OddSkipBlock(
                    spec.hidden_width,
                    omega_0=spec.hidden_omega_0,
                    power_p=spec.power_p,
                    layernorm_eps=spec.layernorm_eps,
                    layernorm_elementwise_affine=spec.layernorm_elementwise_affine,
                    dtype=dtype, device=device, generator=generator))
            else:
                layers.append(_SIRENLayer(
                    spec.hidden_width, spec.hidden_width,
                    omega_0=spec.hidden_omega_0, is_first=False,
                    dtype=dtype, device=device, generator=generator))
        self.hidden_layers = nn.ModuleList(layers)

        # Linear output head: 256 -> 9 (no activation).
        self.output_layer = _LinearHead(
            spec.hidden_width, spec.output_dim,
            dtype=dtype, device=device, generator=generator)

    def _forward_unprojected(self, tau_ic13):
        """Internal/test hook: the raw 9-dim output before COM projection.

        Private (leading underscore) by design — NET-02 makes the projected
        positions the only PUBLIC model output. Projection tests use this to
        verify ``forward == project_com(raw, masses)``.
        """
        x = self.input_layer(tau_ic13)
        for layer in self.hidden_layers:
            x = layer(x)
        return self.output_layer(x)

    def forward(self, tau_ic13, masses):
        """Return the mass-weighted-COM-projected positions (the only public output).

        Args:
            tau_ic13: the 14-dim input [tau, IC13] (single (14,) or batched
                (N, 14)), supplied WHOLESALE by the caller on the model's
                (dtype, device). The model never synthesizes or re-normalizes
                the IC13 slice.
            masses: the 3 ordered RAW masses (or per-sample (N, 3)) supplied
                EXPLICITLY by the caller. Raw masses are unrecoverable from
                the tanh-normalized IC13 mass slots and are never assumed equal.

        Returns:
            The 9-dim (or (N, 9)) mass-weighted-COM-projected positions on
            (dtype, device).
        """
        raw = self._forward_unprojected(tau_ic13)
        return project_com(raw, masses,
                           dtype=self._build_dtype, device=self._build_device)


def build_network(spec, *, dtype, device):
    """Construct a deterministic ``SQRSkipResNetSIREN`` from an ArchitectureSpec.

    A LOCAL ``torch.Generator`` is seeded from ``spec.seed`` and threaded
    through every layer so the global RNG is never touched and the same
    ``spec + seed`` yields bitwise-identical parameters. Every parameter is
    built directly on ``(dtype, device)``; there is no ``.to()`` afterthought,
    no ``torch.set_default_dtype``, and no availability probe.

    Args:
        spec: an ``ArchitectureSpec`` (config-supplied topology).
        dtype: the resolved Torch dtype (from ``resolve_runtime``).
        device: the resolved Torch device (from ``resolve_runtime``).

    Returns:
        SQRSkipResNetSIREN: the spec-faithful backbone with a projected-only
        public forward.
    """
    if not isinstance(spec, ArchitectureSpec):
        raise TypeError(
            f"build_network requires an ArchitectureSpec (got {type(spec).__name__})"
        )
    generator = torch.Generator(device=device)
    generator.manual_seed(int(spec.seed))
    return SQRSkipResNetSIREN(spec, dtype=dtype, device=device, generator=generator)
