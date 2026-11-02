"""Phase 67 (design & settings ladders): the variant catalog, declarations only.

The Phase 67 registry is built through ``register_variant`` as fresh immutable
copies of the sealed Phase 65 catalog (exactly ``locked-12``), so neither the
sealed catalog nor the frozen Phase 66 EXP-01 entry is ever altered (D-12:
fresh named variants for Phase 67, never an edit to a historical catalog).
``phase67_registry`` is the settings-side dispatch a registration's
``settings.variant_registry`` key resolves through; the fit harness imports
this module, so it must never import the harness, the guard, the data seam,
the similarity logger, the launcher or any reader.

Plan 67-02 declares the experiment ladders (D-03/D-04/D-05):

* EXP-02 depth arms ``d2`` (plan 67-01) then ``d4``/``d6``/``d8``/``d12`` —
  the locked layer types at the locked width 256, raw ``[tau, IC13]`` input,
  ``first_omega_0`` 30, the locked hidden frequency, rate 1e-4 and the full
  [0, 10] window. Phase 66's width 384 and first omega 1000 are deliberately
  NOT imported (D-02/D-03).
* EXP-03 rate arms ``lr1e-3``/``lr3e-4``/``lr1e-4``/``lr3e-5``/``lr1e-5`` on
  the locked depth-12 network, everything else locked (D-04).
* EXP-04 input arms ``locked-raw``/``locked-f1``/``locked-f12`` and
  ``exp01-raw``/``exp01-f1``/``exp01-f12`` at rate 1e-4 and window [0, 10]
  on the two required backbones — the locked depth-12 width-256 omega-30
  network and the actual EXP-01 depth-1 width-384 omega-1000 network
  (D-02/D-05).

The encoded arms (``f1``/``f12``) pin the MAIN comparison system's base
frequency ``N_in / T`` from the committed Phase 59 census row (system 1632,
per D-09); repeat-system variants are materialized later as fresh
orbit-specific registrations, never by editing these declarations. An
encoded declaration's frequency is resolved ONLY from that validated
committed census row: ``phase67_registry`` rejects a settings block whose
orbit's census row disagrees with the declaration the settings name
(T-67-04).
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.verification.diagnostic_variants import (
    REGISTRY,
    DiagnosticVariant,
    VariantRefused,
    register_variant,
)

__all__ = [
    "CENSUS_PANELS_RELATIVE_PATH",
    "CENSUS_PANELS_SCHEMA",
    "CENSUS_N_IN_1632",
    "CENSUS_N_IN_851",
    "FEATURE_FREQUENCY_1632",
    "FEATURE_FREQUENCY_851",
    "EXP02_D2_VARIANT",
    "EXP02_D4_VARIANT",
    "EXP02_D6_VARIANT",
    "EXP02_D8_VARIANT",
    "EXP02_D12_VARIANT",
    "EXP03_LR1E3_VARIANT",
    "EXP03_LR3E4_VARIANT",
    "EXP03_LR1E4_VARIANT",
    "EXP03_LR3E5_VARIANT",
    "EXP03_LR1E5_VARIANT",
    "EXP04_LOCKED_RAW_VARIANT",
    "EXP04_LOCKED_F1_VARIANT",
    "EXP04_LOCKED_F12_VARIANT",
    "EXP04_EXP01_RAW_VARIANT",
    "EXP04_EXP01_F1_VARIANT",
    "EXP04_EXP01_F12_VARIANT",
    "PHASE67_ARMS",
    "PHASE67_REGISTRY",
    "PHASE67_REGISTRY_NAME",
    "census_feature_frequency",
    "census_n_in",
    "phase67_registry",
    "phase67_variant",
]

#: The registry name a Phase 67 fit registration selects through its
#: ``settings.variant_registry`` key.
PHASE67_REGISTRY_NAME = "phase67"

#: The committed Phase 59 panel census this catalog pins encoded frequencies
#: from (validated committed metadata; the only frequency source).
CENSUS_PANELS_RELATIVE_PATH = (
    ".planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json"
)
CENSUS_PANELS_SCHEMA = "phase59-panels/v1"

#: The committed census rows (``panels.json`` singles) for the Phase 67
#: comparison systems, pinned verbatim; the encoded arms' base frequency is
#: ``N_in / T`` cycles per physical time unit.
CENSUS_N_IN_1632 = 10.471994061054543
CENSUS_N_IN_851 = 18.612048388702
FEATURE_FREQUENCY_1632 = CENSUS_N_IN_1632 / T_CHARACTERISTIC_TIME
FEATURE_FREQUENCY_851 = CENSUS_N_IN_851 / T_CHARACTERISTIC_TIME

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

#: The rest of the D-03 depth ladder at the same locked settings.
EXP02_D4_VARIANT = DiagnosticVariant(
    name="exp02-d4-w256-o30", time_features="raw_tau_ic13",
    depth=4, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
)
EXP02_D6_VARIANT = DiagnosticVariant(
    name="exp02-d6-w256-o30", time_features="raw_tau_ic13",
    depth=6, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
)
EXP02_D8_VARIANT = DiagnosticVariant(
    name="exp02-d8-w256-o30", time_features="raw_tau_ic13",
    depth=8, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
)
EXP02_D12_VARIANT = DiagnosticVariant(
    name="exp02-d12-w256-o30", time_features="raw_tau_ic13",
    depth=12, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
)

#: The D-04 rate ladder on the locked depth-12 network (the locked 1e-4 is
#: the control arm, freshly registered). Roughly half-decade spacing spans
#: the declared 1e-3..1e-5 interval without adding an optimizer question.
EXP03_LR1E3_VARIANT = DiagnosticVariant(
    name="exp03-d12-w256-lr1e-3", time_features="raw_tau_ic13",
    depth=12, width=256, learning_rate=1e-3, window_length=10.0, first_omega_0=30.0,
)
EXP03_LR3E4_VARIANT = DiagnosticVariant(
    name="exp03-d12-w256-lr3e-4", time_features="raw_tau_ic13",
    depth=12, width=256, learning_rate=3e-4, window_length=10.0, first_omega_0=30.0,
)
EXP03_LR1E4_VARIANT = DiagnosticVariant(
    name="exp03-d12-w256-lr1e-4", time_features="raw_tau_ic13",
    depth=12, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
)
EXP03_LR3E5_VARIANT = DiagnosticVariant(
    name="exp03-d12-w256-lr3e-5", time_features="raw_tau_ic13",
    depth=12, width=256, learning_rate=3e-5, window_length=10.0, first_omega_0=30.0,
)
EXP03_LR1E5_VARIANT = DiagnosticVariant(
    name="exp03-d12-w256-lr1e-5", time_features="raw_tau_ic13",
    depth=12, width=256, learning_rate=1e-5, window_length=10.0, first_omega_0=30.0,
)

#: The D-05 input arms at rate 1e-4 and window [0, 10]: the raw control and
#: the two encoded designs on each required backbone. The locked backbone
#: keeps depth 12 / width 256 / first omega 30; the EXP-01 backbone keeps
#: its actual depth 1 / width 384 / first omega 1000 (D-02/D-05). The
#: encoded arms pin the main system's census frequency; later lap windows
#: and repeat-system frequencies resolve the same way from validated
#: committed metadata, never by editing these declarations.
EXP04_LOCKED_RAW_VARIANT = DiagnosticVariant(
    name="exp04-locked-raw", time_features="raw_tau_ic13",
    depth=12, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
)
EXP04_LOCKED_F1_VARIANT = DiagnosticVariant(
    name="exp04-locked-f1", time_features="tau_ic13_fourier1",
    depth=12, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
    feature_frequency=FEATURE_FREQUENCY_1632,
)
EXP04_LOCKED_F12_VARIANT = DiagnosticVariant(
    name="exp04-locked-f12", time_features="tau_ic13_fourier12",
    depth=12, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
    feature_frequency=FEATURE_FREQUENCY_1632,
)
EXP04_EXP01_RAW_VARIANT = DiagnosticVariant(
    name="exp04-exp01-raw", time_features="raw_tau_ic13",
    depth=1, width=384, learning_rate=1e-4, window_length=10.0, first_omega_0=1000.0,
)
EXP04_EXP01_F1_VARIANT = DiagnosticVariant(
    name="exp04-exp01-f1", time_features="tau_ic13_fourier1",
    depth=1, width=384, learning_rate=1e-4, window_length=10.0, first_omega_0=1000.0,
    feature_frequency=FEATURE_FREQUENCY_1632,
)
EXP04_EXP01_F12_VARIANT = DiagnosticVariant(
    name="exp04-exp01-f12", time_features="tau_ic13_fourier12",
    depth=1, width=384, learning_rate=1e-4, window_length=10.0, first_omega_0=1000.0,
    feature_frequency=FEATURE_FREQUENCY_1632,
)

#: The exact arm IDs per experiment, in the plan's listed arm order, mapped
#: to their declarations. Later execution plans expand their case-major
#: Cartesian products from these tables.
PHASE67_ARMS = MappingProxyType({
    "exp02": MappingProxyType({
        "d2": EXP02_D2_VARIANT,
        "d4": EXP02_D4_VARIANT,
        "d6": EXP02_D6_VARIANT,
        "d8": EXP02_D8_VARIANT,
        "d12": EXP02_D12_VARIANT,
    }),
    "exp03": MappingProxyType({
        "lr1e-3": EXP03_LR1E3_VARIANT,
        "lr3e-4": EXP03_LR3E4_VARIANT,
        "lr1e-4": EXP03_LR1E4_VARIANT,
        "lr3e-5": EXP03_LR3E5_VARIANT,
        "lr1e-5": EXP03_LR1E5_VARIANT,
    }),
    "exp04": MappingProxyType({
        "locked-raw": EXP04_LOCKED_RAW_VARIANT,
        "locked-f1": EXP04_LOCKED_F1_VARIANT,
        "locked-f12": EXP04_LOCKED_F12_VARIANT,
        "exp01-raw": EXP04_EXP01_RAW_VARIANT,
        "exp01-f1": EXP04_EXP01_F1_VARIANT,
        "exp01-f12": EXP04_EXP01_F12_VARIANT,
    }),
})

#: The ladder declarations in registration order (the depth-2 tracer
#: declaration leads; it is registered first below).
_LADDER_DECLARATIONS = (
    EXP02_D4_VARIANT,
    EXP02_D6_VARIANT,
    EXP02_D8_VARIANT,
    EXP02_D12_VARIANT,
    EXP03_LR1E3_VARIANT,
    EXP03_LR3E4_VARIANT,
    EXP03_LR1E4_VARIANT,
    EXP03_LR3E5_VARIANT,
    EXP03_LR1E5_VARIANT,
    EXP04_LOCKED_RAW_VARIANT,
    EXP04_LOCKED_F1_VARIANT,
    EXP04_LOCKED_F12_VARIANT,
    EXP04_EXP01_RAW_VARIANT,
    EXP04_EXP01_F1_VARIANT,
    EXP04_EXP01_F12_VARIANT,
)

#: The Phase 67 registry: a fresh immutable copy of the sealed catalog
#: extended with the depth-2 tracer declaration and then the ladder
#: declarations in registration order, each through ``register_variant``.
#: It never alters ``REGISTRY`` and refuses duplicates, so equal settings
#: can never acquire the same new name twice.
PHASE67_REGISTRY = register_variant(EXP02_D2_VARIANT, into=REGISTRY)
for _declaration in _LADDER_DECLARATIONS:
    PHASE67_REGISTRY = register_variant(_declaration, into=PHASE67_REGISTRY)


def phase67_variant(experiment, arm):
    """The declaration an (experiment, arm) pair names, or a refusal.

    The exact arm tables above are the only source; an unknown experiment or
    arm refuses before anything is built.
    """
    if experiment not in PHASE67_ARMS:
        raise VariantRefused(
            f"unknown Phase 67 experiment {experiment!r}; known: "
            f"{list(PHASE67_ARMS)}"
        )
    arms = PHASE67_ARMS[experiment]
    if arm not in arms:
        raise VariantRefused(
            f"unknown {experiment} arm {arm!r}; known: {list(arms)}"
        )
    return arms[arm]


def _default_panels_path():
    """The committed census path under this checkout's repository root."""
    return Path(__file__).resolve().parents[2] / CENSUS_PANELS_RELATIVE_PATH


def census_n_in(orbit_id, *, repo_root=None, panels_path=None):
    """The committed census ``N_in`` of ``orbit_id``, validated before use.

    The panels document must exist, parse, carry the Phase 59 schema and a
    numeric finite positive ``N_in`` on the orbit's own row; anything else
    (a missing file, malformed JSON, a foreign schema, a non-numeric or
    non-finite value, an absent row) is a ``VariantRefused`` — never a
    silently regenerated frequency.
    """
    if isinstance(orbit_id, bool) or not isinstance(orbit_id, int):
        raise VariantRefused(f"the census orbit id must be an integer; got {orbit_id!r}")
    path = Path(panels_path) if panels_path is not None else (
        Path(repo_root) / CENSUS_PANELS_RELATIVE_PATH
        if repo_root is not None else _default_panels_path()
    )
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except FileNotFoundError as exc:
        raise VariantRefused(
            f"the committed census panels document is missing: {path}"
        ) from exc
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise VariantRefused(
            f"the committed census panels document is unreadable: {exc}"
        ) from exc
    if not isinstance(doc, Mapping) or doc.get("schema") != CENSUS_PANELS_SCHEMA:
        raise VariantRefused(
            f"the census panels document must be schema {CENSUS_PANELS_SCHEMA!r}"
        )
    singles = doc.get("singles")
    if not isinstance(singles, list):
        raise VariantRefused("the census panels document names no singles rows")
    for row in singles:
        if not isinstance(row, Mapping) or row.get("id") != orbit_id:
            continue
        value = row.get("N_in")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise VariantRefused(
                f"the census row for orbit {orbit_id} names a non-numeric "
                f"N_in: {value!r}"
            )
        number = float(value)
        if not math.isfinite(number) or number <= 0.0:
            raise VariantRefused(
                f"the census row for orbit {orbit_id} names a non-finite or "
                f"non-positive N_in: {value!r}"
            )
        return number
    raise VariantRefused(
        f"the committed census holds no row for orbit {orbit_id}; an encoded "
        "declaration cannot resolve its frequency"
    )


def census_feature_frequency(orbit_key, *, repo_root=None, panels_path=None):
    """``N_in / T`` cycles per physical time unit for a ``variant/fidelity/id``
    orbit key, from the validated committed census row."""
    if not isinstance(orbit_key, str):
        raise VariantRefused(
            f"the orbit key must be variant/fidelity/id text; got {orbit_key!r}"
        )
    parts = orbit_key.split("/")
    if len(parts) != 3:
        raise VariantRefused(
            f"the orbit key must be variant/fidelity/id; got {orbit_key!r}"
        )
    try:
        orbit_id = int(parts[2])
    except ValueError as exc:
        raise VariantRefused(
            f"the orbit key id must be an integer; got {parts[2]!r}"
        ) from exc
    n_in = census_n_in(orbit_id, repo_root=repo_root, panels_path=panels_path)
    return n_in / T_CHARACTERISTIC_TIME


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

    When the settings mapping names BOTH a variant and an orbit, an encoded
    declaration's pinned ``feature_frequency`` must agree with the orbit's
    own registered census row (``N_in / T``): the frequency is resolved only
    from that validated committed metadata, and a disagreeing orbit refuses
    (T-67-04 — a 1632-pinned declaration never runs mis-encoded on 851).
    """
    name = (
        settings.get("variant_registry") if isinstance(settings, Mapping) else settings
    )
    if name is None:
        return REGISTRY
    if not (isinstance(name, str) and name == PHASE67_REGISTRY_NAME):
        raise VariantRefused(
            f"unknown variant registry {name!r}; the Phase 67 dispatch knows "
            f"{PHASE67_REGISTRY_NAME!r} and the sealed default"
        )
    if isinstance(settings, Mapping):
        variant_block = settings.get("variant")
        orbit_key = settings.get("orbit_key")
        if isinstance(variant_block, Mapping) \
                and isinstance(variant_block.get("name"), str) \
                and isinstance(orbit_key, str):
            variant = PHASE67_REGISTRY.get(variant_block["name"])
            if variant is None:
                raise VariantRefused(
                    f"unknown diagnostic variant {variant_block['name']!r}; "
                    f"registered: {list(PHASE67_REGISTRY)}"
                )
            if variant.time_features != "raw_tau_ic13":
                expected = census_feature_frequency(orbit_key)
                if expected != float(variant.feature_frequency):
                    raise VariantRefused(
                        f"the encoded variant {variant.name!r} pins "
                        f"feature_frequency {float(variant.feature_frequency)!r} "
                        f"cycles per physical time unit, but orbit {orbit_key!r} "
                        f"resolves {expected!r} from its committed census row; "
                        "an encoded declaration never runs on a disagreeing orbit"
                    )
    return PHASE67_REGISTRY
