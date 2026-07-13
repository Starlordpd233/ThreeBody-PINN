"""Phase 38 / NET-01 — frozen, validated architecture specification.

``ArchitectureSpec`` is the config-supplied topology surface the network
(38-02) instantiates from. Spec-locked values are the validated defaults
(``pinn_architecture.md`` §2.3/§2.4); SIREN ω defaults are sourced from
``pinn.constants`` so science locks stay single-homed.

Pattern: Phase 37 ``RuntimeSpec`` — ``@dataclass(frozen=True)`` with
fail-closed construction-time validation (raise ``ValueError`` naming the
offending field before any tensor is built).

CTX-20: this dataclass carries NO precision/device field. Dtype/device flow
only through ``pinn.runtime.resolve_runtime``; the model constructor accepts
resolved dtype/device explicitly.

Does NOT import v1.3-era ``pinn/`` files (CTX-17).
"""

from __future__ import annotations

from dataclasses import dataclass

from pinn.constants import SIREN_FIRST_OMEGA_0, SIREN_HIDDEN_OMEGA_0

# Documented deterministic default seed for reproducible init (NET-01).
# Phase 41 (CTRL-01) may override via YAML-mapped config; here the default
# is fixed so default construction is deterministic.
_DEFAULT_SEED = 0

# Locked skip / LayerNorm cadence: alternating odd-layer LayerNorm with
# residual skips (pinn_architecture.md §2.3/§2.4, ARCH-02).
_DEFAULT_SKIP_CADENCE = "alternating"


@dataclass(frozen=True)
class ArchitectureSpec:
    """Immutable, validated SQR-SkipResNet-SIREN topology specification.

    Defaults encode the locked Phase 38 topology
    (14 → 256×12 → 9, SIREN ω from constants, LayerNorm
    ``elementwise_affine=False`` on odd layers, power p=2).

    Attributes:
        input_dim: input vector width (locked 14 = [τ, IC₁₃]).
        output_dim: position output width (locked 9 = 3 bodies × 3D).
        hidden_depth: number of hidden layers (locked 12).
        hidden_width: hidden layer width (locked 256).
        first_omega_0: SIREN first-layer frequency (from constants).
        hidden_omega_0: SIREN hidden-layer frequency (from constants).
        layernorm_elementwise_affine: LayerNorm affine flag (locked False).
        layernorm_eps: LayerNorm epsilon (locked 1e-5).
        power_p: skip residual power (locked 2).
        skip_cadence: skip/LayerNorm placement descriptor (``"alternating"``).
        seed: deterministic init seed (default 0).

    No ``precision`` / ``device`` / ``dtype`` fields (CTX-20).
    """

    input_dim: int = 14
    output_dim: int = 9
    hidden_depth: int = 12
    hidden_width: int = 256
    first_omega_0: float = SIREN_FIRST_OMEGA_0
    hidden_omega_0: float = SIREN_HIDDEN_OMEGA_0
    layernorm_elementwise_affine: bool = False
    layernorm_eps: float = 1e-5
    power_p: int = 2
    skip_cadence: str = _DEFAULT_SKIP_CADENCE
    seed: int = _DEFAULT_SEED

    def __post_init__(self) -> None:
        """Fail-closed validation — raise before any downstream build."""
        if self.input_dim != 14:
            raise ValueError(
                f"ArchitectureSpec.input_dim must be 14 (got {self.input_dim!r}); "
                "locked topology is 14 → 256×12 → 9 (pinn_architecture.md §2.3/§2.4)"
            )
        if self.output_dim != 9:
            raise ValueError(
                f"ArchitectureSpec.output_dim must be 9 (got {self.output_dim!r}); "
                "locked topology is 14 → 256×12 → 9 (pinn_architecture.md §2.3/§2.4)"
            )
        if not isinstance(self.hidden_depth, int) or self.hidden_depth <= 0:
            raise ValueError(
                f"ArchitectureSpec.hidden_depth must be a positive int "
                f"(got {self.hidden_depth!r})"
            )
        if self.hidden_depth != 12:
            raise ValueError(
                f"ArchitectureSpec.hidden_depth must be 12 (got {self.hidden_depth!r}); "
                "locked topology is 14 → 256×12 → 9 (pinn_architecture.md §2.3/§2.4)"
            )
        if not isinstance(self.hidden_width, int) or self.hidden_width <= 0:
            raise ValueError(
                f"ArchitectureSpec.hidden_width must be a positive int "
                f"(got {self.hidden_width!r})"
            )
        if self.hidden_width != 256:
            raise ValueError(
                f"ArchitectureSpec.hidden_width must be 256 (got {self.hidden_width!r}); "
                "locked topology is 14 → 256×12 → 9 (pinn_architecture.md §2.3/§2.4)"
            )
        if self.power_p != 2:
            raise ValueError(
                f"ArchitectureSpec.power_p must be 2 (got {self.power_p!r}); "
                "ARCH-02 locked (pinn_architecture.md §2.3/§2.4)"
            )
        if self.layernorm_eps < 0:
            raise ValueError(
                f"ArchitectureSpec.layernorm_eps must be non-negative "
                f"(got {self.layernorm_eps!r})"
            )
        if self.layernorm_elementwise_affine is not False:
            raise ValueError(
                f"ArchitectureSpec.layernorm_elementwise_affine must be False "
                f"(got {self.layernorm_elementwise_affine!r}); "
                "ARCH-02 locked (pinn_architecture.md §2.3/§2.4)"
            )
        if self.first_omega_0 != SIREN_FIRST_OMEGA_0:
            raise ValueError(
                f"ArchitectureSpec.first_omega_0 must be {SIREN_FIRST_OMEGA_0} "
                f"(got {self.first_omega_0!r}); sourced from pinn.constants "
                "(pinn_architecture.md §2.2/§2.4 ARCH-01)"
            )
        if self.hidden_omega_0 != SIREN_HIDDEN_OMEGA_0:
            raise ValueError(
                f"ArchitectureSpec.hidden_omega_0 must be {SIREN_HIDDEN_OMEGA_0} "
                f"(got {self.hidden_omega_0!r}); sourced from pinn.constants "
                "(pinn_architecture.md §2.2/§2.4 ARCH-01)"
            )
        cadence = self.skip_cadence
        if not isinstance(cadence, str) or "alternat" not in cadence.lower():
            raise ValueError(
                f"ArchitectureSpec.skip_cadence must describe alternating "
                f"odd-layer LayerNorm (got {cadence!r})"
            )
        if not isinstance(self.seed, int):
            raise ValueError(
                f"ArchitectureSpec.seed must be an int (got {self.seed!r})"
            )
