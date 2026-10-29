"""Phase 65 (INST-08): named diagnostic fit variants for the root-cause harness.

A diagnostic variant names one fit configuration — depth, width, time-feature
declaration, learning rate and physical window length — for the Phase 65
minute-scale fit harness. The network itself is always the production
``SQRSkipResNetSIREN``: variants are built from a copy of a validated
``ArchitectureSpec``'s fields with only the topology fields replaced, exactly as
``diagnostic_architecture.build_network_with_first_omega`` builds the G2 sweep
networks, so the locked 12-layer variant at the locked frequencies is bitwise
the production network at the same seed (D-04's same-runtime/same-weights
parity, tested in tests/phase65/test_contracts.py). ``ArchitectureSpec`` stays
omega- and topology-locked; no production module is edited.

The registry is deliberately small: Wave 0 registers only ``locked-12``. The
Phase 66-67 ladders are NOT populated here; their prediction pages register
their own approved designs through ``register_variant``, which never alters the
sealed catalog and refuses duplicate names.
"""

from __future__ import annotations

import dataclasses
import math
import numbers
import re
from dataclasses import dataclass
from types import MappingProxyType, SimpleNamespace

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import SIREN_FIRST_OMEGA_0, SIREN_HIDDEN_OMEGA_0
from pinn.network import SQRSkipResNetSIREN

__all__ = [
    "SUPPORTED_TIME_FEATURES",
    "VARIANT_NAME_RE",
    "MAX_WINDOW_LENGTH",
    "VariantRefused",
    "DiagnosticVariant",
    "LOCKED_12",
    "REGISTRY",
    "build_variant",
    "resolve_variant",
]

#: Exact-ASCII diagnostic variant identifiers (same alphabet as arm ids).
VARIANT_NAME_RE = re.compile(r"[a-z0-9][a-z0-9-]*")

#: The only time-feature declaration Wave 0 supports: raw normalized tau beside
#: the raw 13-component IC vector, exactly the production 14D input. Anything
#: else is refused before construction, naming the declaration, so later
#: prediction pages can add their own approved designs explicitly.
SUPPORTED_TIME_FEATURES = ("raw_tau_ic13",)

#: Physical window length is bounded by the Stage-0 scoring horizon (10).
MAX_WINDOW_LENGTH = 10.0


class VariantRefused(ValueError):
    """A diagnostic variant name, declaration or numeric field is not usable."""


@dataclass(frozen=True)
class DiagnosticVariant:
    """One named diagnostic fit configuration.

    ``depth``/``width`` are the hidden topology of the production network class
    (the locks live in ``ArchitectureSpec`` and are not relaxed here — a variant
    merely selects what to build). ``learning_rate`` is the constant Adam rate
    of the diagnostic policy. ``window_length`` is the physical window, from
    t = 0, in the same physical time units as the records.
    """

    name: str
    time_features: str
    depth: int
    width: int
    learning_rate: float
    window_length: float
    first_omega_0: float = SIREN_FIRST_OMEGA_0
    hidden_omega_0: float = SIREN_HIDDEN_OMEGA_0

    def __post_init__(self):
        if not isinstance(self.name, str) or VARIANT_NAME_RE.fullmatch(self.name) is None:
            raise VariantRefused(
                f"a diagnostic variant name must match [a-z0-9][a-z0-9-]* exactly; "
                f"got {self.name!r}"
            )
        if self.time_features not in SUPPORTED_TIME_FEATURES:
            raise VariantRefused(
                f"unsupported time-feature declaration {self.time_features!r} for variant "
                f"{self.name!r}; supported: {list(SUPPORTED_TIME_FEATURES)}"
            )
        for field_name in ("depth", "width"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise VariantRefused(
                    f"{field_name} must be a finite positive integer; got {value!r}"
                )
        for field_name in ("learning_rate", "window_length", "first_omega_0", "hidden_omega_0"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, numbers.Real):
                raise VariantRefused(
                    f"{field_name} must be a finite positive real number; got {value!r}"
                )
            number = float(value)
            if not math.isfinite(number) or number <= 0.0:
                raise VariantRefused(
                    f"{field_name} must be a finite positive real number; got {value!r}"
                )
        if not 0.0 < float(self.window_length) <= MAX_WINDOW_LENGTH:
            raise VariantRefused(
                f"window_length must satisfy 0 < window_length <= {MAX_WINDOW_LENGTH}; "
                f"got {self.window_length!r}"
            )

    def to_json_dict(self) -> dict:
        """Plain JSON types. Numeric fields keep their exact values — never a
        rounded string substitution (E-INST-encoding)."""
        return {
            "name": str(self.name),
            "time_features": str(self.time_features),
            "depth": int(self.depth),
            "width": int(self.width),
            "learning_rate": float(self.learning_rate),
            "window_length": float(self.window_length),
            "first_omega_0": float(self.first_omega_0),
            "hidden_omega_0": float(self.hidden_omega_0),
        }


#: The locked production topology as a diagnostic variant: 12 hidden layers of
#: width 256, raw [tau, IC13] inputs, the locked SIREN frequencies, a constant
#: Adam rate of 1e-4 and the full [0, 10] physical window.
LOCKED_12 = DiagnosticVariant(
    name="locked-12",
    time_features="raw_tau_ic13",
    depth=12,
    width=256,
    learning_rate=1e-4,
    window_length=10.0,
)

#: The sealed Wave 0 registry. Immutable and in registration order; the only
#: entry is ``locked-12`` — the Phase 66-67 ladders are not populated.
REGISTRY = MappingProxyType({"locked-12": LOCKED_12})


def resolve_variant(variant):
    """Resolve a variant reference to a ``DiagnosticVariant``.

    ``None``, an unknown name or a value of any other type raises
    ``VariantRefused`` before anything is built (E-INST-empty).
    """
    if isinstance(variant, DiagnosticVariant):
        return variant
    if variant is None:
        raise VariantRefused(
            "variant is None; name a registered diagnostic variant or pass a "
            "DiagnosticVariant"
        )
    if isinstance(variant, str):
        if variant not in REGISTRY:
            raise VariantRefused(
                f"unknown diagnostic variant {variant!r}; registered: {list(REGISTRY)}"
            )
        return REGISTRY[variant]
    raise VariantRefused(
        f"variant must be a name or a DiagnosticVariant; got {type(variant).__name__}"
    )


def build_variant(variant, *, seed, dtype, device):
    """Build the production network for ``variant``, seeded exactly as production.

    The validated fields of ``ArchitectureSpec(seed=seed)`` are copied and only
    the topology fields the variant names are replaced, so at the locked values
    the parameters are bitwise equal to ``build_network(ArchitectureSpec(seed),
    ...)`` in the same runtime. A local ``torch.Generator`` is used; the global
    RNG is never touched. Synthetic-only custom variants are fixture inputs —
    building one does not register it.
    """
    resolved = resolve_variant(variant)
    fields = dataclasses.asdict(ArchitectureSpec(seed=int(seed)))
    fields["hidden_depth"] = int(resolved.depth)
    fields["hidden_width"] = int(resolved.width)
    fields["first_omega_0"] = float(resolved.first_omega_0)
    fields["hidden_omega_0"] = float(resolved.hidden_omega_0)
    generator = torch.Generator(device=device)
    generator.manual_seed(int(seed))
    return SQRSkipResNetSIREN(
        SimpleNamespace(**fields), dtype=dtype, device=device, generator=generator
    )
