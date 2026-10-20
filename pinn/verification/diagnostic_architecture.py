"""Phase 60 (INST-05): the first-layer frequency override builder, with ArchitectureSpec left omega-locked.

``ArchitectureSpec`` refuses every first-layer frequency but the locked 30.0, and
``build_network`` refuses anything that is not an ``ArchitectureSpec``. The G2
settings sweep, its confirmation and an owner-approved continue need other
frequencies, so this module builds the same network around a copy of the
validated spec's fields with ``first_omega_0`` replaced and nothing else
changed. Neither production module is edited (SCOPE-43). The seeding matches
``build_network``, so at 30.0 the parameters are bitwise equal to the locked
network's, and at any other frequency only the first layer's ``omega_0`` differs.
Whether an arm may use a frequency at all is decided by
``learnability_arms.check_override``, not here.
"""

from __future__ import annotations

import dataclasses
import math
import numbers
from types import SimpleNamespace

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.network import SQRSkipResNetSIREN

__all__ = ["DiagnosticOmegaError", "build_network_with_first_omega"]


class DiagnosticOmegaError(ValueError):
    """The requested first-layer frequency is not a finite, positive real number."""


def build_network_with_first_omega(first_omega_0, *, seed, dtype, device):
    """The production network for ``seed`` with only ``first_omega_0`` replaced.

    The remaining fields are copied from a validated ``ArchitectureSpec(seed=seed)``.
    A local ``torch.Generator`` is seeded exactly as ``build_network`` seeds it, so
    the global random state is never touched and the initial parameters do not
    depend on the frequency (the first layer's init bound is ``1 / in_features``).
    """
    if isinstance(first_omega_0, bool) or not isinstance(first_omega_0, numbers.Real):
        raise DiagnosticOmegaError(
            f"first_omega_0 must be a finite positive real number; got {first_omega_0!r}"
        )
    omega = float(first_omega_0)
    if not math.isfinite(omega) or omega <= 0.0:
        raise DiagnosticOmegaError(
            f"first_omega_0 must be a finite positive real number; got {first_omega_0!r}"
        )
    fields = dataclasses.asdict(ArchitectureSpec(seed=seed))
    fields["first_omega_0"] = omega
    generator = torch.Generator(device=device)
    generator.manual_seed(int(seed))
    return SQRSkipResNetSIREN(
        SimpleNamespace(**fields), dtype=dtype, device=device, generator=generator
    )
