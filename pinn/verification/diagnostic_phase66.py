"""Phase 66 (EXP-01): the small-network control catalog and reading rule.

EXP-01 registers one smaller, shallower diagnostic variant — a 1-hidden-layer
network 384 wide with its first SIREN frequency scaled to the orbit's inner-lap
rate (``first_omega_0 = 1000.0``, covering system 851's fundamental) at the
locked learning rate, window and hidden frequency — through
``register_variant`` into a NEW immutable registry, so the sealed Phase 65
catalog (exactly ``locked-12``) is never altered. ``REGISTRIES`` is the closed
name table a committed fit registration selects through its
``settings.variant_registry`` key; the harness (``diagnostic_fit``) imports
this module, so this module must never import the harness, the guard, the data
seam, the similarity logger or the launcher.

``tier1_e_max`` reads the frozen FEAS-01 scorecard's Tier-1 ``E_max`` from the
scorecard itself, never retyped, and ``classify_exp01`` is the pre-registered
EXP-01 reading rule: tier 1, the constant-predictor band, between, or other.
"""

from __future__ import annotations

import math
from types import MappingProxyType

from pinn.verification.diagnostic_variants import (
    REGISTRY,
    DiagnosticVariant,
    register_variant,
)

__all__ = [
    "EXP01_VARIANT",
    "NEAR_BAND",
    "PHASE66_REGISTRY",
    "REGISTRIES",
    "classify_exp01",
    "tier1_e_max",
]

#: The EXP-01 positive-control network (D-04, D-05, D-06): the production
#: layer types at depth 1 and width 384 (157,065 parameters, under the locked
#: 795,657), ``first_omega_0`` 1000.0 so the first layer's starting
#: time-frequency range covers the faster repeat system's fundamental, and
#: every other setting at its locked or harness value (``hidden_omega_0`` stays
#: at its locked default 1.0).
EXP01_VARIANT = DiagnosticVariant(
    name="exp01-d1-w384-o1000",
    time_features="raw_tau_ic13",
    depth=1,
    width=384,
    learning_rate=1e-4,
    window_length=10.0,
    first_omega_0=1000.0,
)

#: The Phase 66 registry: a fresh immutable copy of the sealed catalog extended
#: with EXP-01 in registration order. ``register_variant`` never alters
#: ``REGISTRY`` and refuses duplicate names.
PHASE66_REGISTRY = register_variant(EXP01_VARIANT, into=REGISTRY)

#: The closed registry-name table a registration's ``settings.variant_registry``
#: selects from. Absent or null keeps the sealed Phase 65 behaviour; anything
#: else is refused before any data access.
REGISTRIES = MappingProxyType({"phase66": PHASE66_REGISTRY})

#: D-09's numeric constant-predictor band, a pre-registered fraction either
#: side of the record's own window-mean-constant E.
NEAR_BAND = 0.05


def tier1_e_max(card):
    """The frozen scorecard's Tier-1 ``E_max``, read from its own tiers section.

    The limit is read, never retyped (the Phase 64 ``_tier1_max`` precedent).
    """
    for level in card.section("tiers")["levels"]:
        if int(level["tier"]) == 1:
            return float(level["E_max"])
    raise ValueError("the scorecard names no level whose tier is 1")


def classify_exp01(e, e_const, *, tier1_max, band=NEAR_BAND):
    """The pre-registered EXP-01 branch for one record's network error.

    ``e`` is the record's ``scores.network.E`` and ``e_const`` its own
    ``window_mean_constant`` comparison score; the Tier-1 limit comes from the
    frozen scorecard through :func:`tier1_e_max`. Inclusive edges, fixed by
    tests before any run; a non-finite error is ``other``.
    """
    if not math.isfinite(e):
        return "other"
    if e <= tier1_max:
        return "tier1"
    low, high = (1.0 - band) * e_const, (1.0 + band) * e_const
    if low <= e <= high:
        return "near"
    return "between" if e < low else "other"
