"""Phase 67 (design & settings ladders): the variant catalog, declarations only.

EXP-02's first ladder declaration — a raw-input depth-2 network at the locked
width, frequencies, rate and window — is registered through
``register_variant`` into a NEW immutable registry, so the sealed Phase 65
catalog (exactly ``locked-12``) and the frozen Phase 66 EXP-01 entry are never
altered (D-12: fresh named variants for Phase 67, never an edit to a
historical catalog). ``phase67_registry`` is the settings-side dispatch a
registration's ``settings.variant_registry`` key resolves through; the fit
harness imports this module, so it must never import the harness, the guard,
the data seam, the similarity logger, the launcher or any reader.

The declaration is depth-only against the locked setup: width 256,
``raw_tau_ic13`` inputs, ``first_omega_0`` 30, the locked hidden frequency,
a constant Adam rate of 1e-4 and the full [0, 10] physical window (D-03 —
Phase 66's width 384 and first omega 1000 are deliberately NOT imported;
D-02 keeps EXP-01 a multi-setting positive control, not a depth contrast).
"""

from __future__ import annotations

from collections.abc import Mapping

from pinn.verification.diagnostic_variants import (
    REGISTRY,
    DiagnosticVariant,
    VariantRefused,
    register_variant,
)

__all__ = [
    "EXP02_D2_VARIANT",
    "PHASE67_REGISTRY",
    "PHASE67_REGISTRY_NAME",
    "phase67_registry",
]

#: The registry name a Phase 67 fit registration selects through its
#: ``settings.variant_registry`` key.
PHASE67_REGISTRY_NAME = "phase67"

#: The EXP-02 depth-2 declaration (D-03): the locked layer types at depth 2
#: with width, input, frequency settings, optimizer, learning rate, physical
#: window and data treatment otherwise locked. ``hidden_omega_0`` keeps the
#: locked default; ``first_omega_0`` is the locked 30, not Phase 66's 1000.
EXP02_D2_VARIANT = DiagnosticVariant(
    name="exp02-d2-w256-o30",
    time_features="raw_tau_ic13",
    depth=2,
    width=256,
    learning_rate=1e-4,
    window_length=10.0,
    first_omega_0=30.0,
)

#: The Phase 67 registry: a fresh immutable copy of the sealed catalog extended
#: with the depth-2 declaration in registration order, built through
#: ``register_variant`` exactly as the Phase 66 registry was. It never alters
#: ``REGISTRY`` and refused the duplicate had the name existed, so equal
#: settings can never acquire the same new name twice.
PHASE67_REGISTRY = register_variant(EXP02_D2_VARIANT, into=REGISTRY)


def phase67_registry(settings):
    """The registry a settings block's ``variant_registry`` name selects.

    Accepts either a settings mapping or the registry name itself. ``None`` —
    every Phase 65 registration — selects the sealed ``REGISTRY`` object, so
    Phase 65 behaviour is unchanged; ``PHASE67_REGISTRY_NAME`` selects
    :data:`PHASE67_REGISTRY`. Any other value raises ``VariantRefused`` before
    any data access, optimizer construction or attempt claim. The Phase 66
    table stays in ``diagnostic_phase66.REGISTRIES``; the fit harness checks
    it first and falls through to this dispatch, so this function needs no
    Phase 66 import and the catalog stays declaration-only.
    """
    name = (
        settings.get("variant_registry") if isinstance(settings, Mapping) else settings
    )
    if name is None:
        return REGISTRY
    if isinstance(name, str) and name == PHASE67_REGISTRY_NAME:
        return PHASE67_REGISTRY
    raise VariantRefused(
        f"unknown variant registry {name!r}; the Phase 67 dispatch knows "
        f"{PHASE67_REGISTRY_NAME!r} and the sealed default"
    )
