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

Plan 67-06 materializes the repeat-system (851) encoded registrations as
fresh orbit-specific declarations (D-09: the same encoded designs at 851's
own census frequency, so the encoded arms run identically encoded on the
second panel system), and adds the EXP-05 window-variant extension point:
the lap arms' variants depend on the committed metadata capture's exact
first-crossing endpoints, so they are materialized AFTER metadata through
:func:`register_exp05_window_variants` and merge into the registry the
``phase67`` dispatch returns. The locked raw registry entries are never
edited.
"""

from __future__ import annotations

import json
import math
import re
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
    "EXP04_LOCKED_F1_851_VARIANT",
    "EXP04_LOCKED_F12_851_VARIANT",
    "EXP04_EXP01_F1_851_VARIANT",
    "EXP04_EXP01_F12_851_VARIANT",
    "EXP05_WINDOW_ARM_PATTERN",
    "census_feature_frequency",
    "census_n_in",
    "exp05_window_variant",
    "phase67_arm_variant",
    "phase67_registry",
    "phase67_variant",
    "register_exp05_window_variants",
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

#: The repeat-system (851) encoded registrations (plan 67-06, D-09): the same
#: encoded designs at 851's own committed census frequency, materialized as
#: fresh orbit-specific declarations so an encoded arm runs identically
#: encoded on the second panel system. Raw arms need no orbit-specific copy.
EXP04_LOCKED_F1_851_VARIANT = DiagnosticVariant(
    name="exp04-locked-f1-851", time_features="tau_ic13_fourier1",
    depth=12, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
    feature_frequency=FEATURE_FREQUENCY_851,
)
EXP04_LOCKED_F12_851_VARIANT = DiagnosticVariant(
    name="exp04-locked-f12-851", time_features="tau_ic13_fourier12",
    depth=12, width=256, learning_rate=1e-4, window_length=10.0, first_omega_0=30.0,
    feature_frequency=FEATURE_FREQUENCY_851,
)
EXP04_EXP01_F1_851_VARIANT = DiagnosticVariant(
    name="exp04-exp01-f1-851", time_features="tau_ic13_fourier1",
    depth=1, width=384, learning_rate=1e-4, window_length=10.0, first_omega_0=1000.0,
    feature_frequency=FEATURE_FREQUENCY_851,
)
EXP04_EXP01_F12_851_VARIANT = DiagnosticVariant(
    name="exp04-exp01-f12-851", time_features="tau_ic13_fourier12",
    depth=1, width=384, learning_rate=1e-4, window_length=10.0, first_omega_0=1000.0,
    feature_frequency=FEATURE_FREQUENCY_851,
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
#: declaration leads; it is registered first below, and the 851 encoded
#: registrations close the order as the last fresh materializations).
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
    EXP04_LOCKED_F1_851_VARIANT,
    EXP04_LOCKED_F12_851_VARIANT,
    EXP04_EXP01_F1_851_VARIANT,
    EXP04_EXP01_F12_851_VARIANT,
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


#: The EXP-05 encoded arm name pattern: ``exp05-lap<1|2|5|10>-<orbit id>``,
#: materialized from the committed metadata capture's exact first-crossing
#: endpoints (never pinned here — the endpoints are algorithm outputs).
EXP05_WINDOW_ARM_PATTERN = re.compile(r"^exp05-lap(1|2|5|10)-([1-9][0-9]*)$")

#: The materialized EXP-05 window variants (name -> declaration). Populated
#: ONLY through :func:`register_exp05_window_variants` after the committed
#: metadata capture resolves each orbit's lap endpoints; merged into the
#: registry the ``phase67`` dispatch returns. The locked raw registry is
#: never edited and the static name set never collides (no static name
#: matches the pattern).
_EXP05_WINDOW_VARIANTS: dict = {}


def register_exp05_window_variants(declarations):
    """Materialize the EXP-05 lap variants from the committed metadata.

    Idempotent for an identical re-materialization (the same name and the
    same declaration fields), refusing a conflicting re-registration, a name
    outside the ``exp05-lap<L>-<orbit id>`` pattern, an encoded time-feature
    declaration (EXP-05 changes only the window; D-06), or a name that
    collides with the static registry. Returns the effective variant table.
    """
    if not isinstance(declarations, (list, tuple)):
        raise VariantRefused(
            f"the exp05 window variants need a list of declarations; got {declarations!r}"
        )
    for declaration in declarations:
        if not isinstance(declaration, DiagnosticVariant):
            raise VariantRefused(
                "an exp05 window variant must be a DiagnosticVariant; got "
                f"{type(declaration).__name__}"
            )
        if EXP05_WINDOW_ARM_PATTERN.fullmatch(declaration.name) is None:
            raise VariantRefused(
                f"an exp05 window variant name must match exp05-lap<1|2|5|10>-"
                f"<orbit id>; got {declaration.name!r}"
            )
        if declaration.time_features != "raw_tau_ic13":
            raise VariantRefused(
                f"the exp05 window variant {declaration.name!r} changes the "
                "input design too; EXP-05 changes only the window (D-06)"
            )
        if declaration.name in PHASE67_REGISTRY:
            raise VariantRefused(
                f"the exp05 window variant name {declaration.name!r} collides "
                "with the static registry"
            )
        existing = _EXP05_WINDOW_VARIANTS.get(declaration.name)
        if existing is not None and existing.to_json_dict() != (
            declaration.to_json_dict()
        ):
            raise VariantRefused(
                f"the exp05 window variant {declaration.name!r} was already "
                "materialized with different fields; a conflicting "
                "re-registration refuses"
            )
        _EXP05_WINDOW_VARIANTS[declaration.name] = declaration
    return dict(_EXP05_WINDOW_VARIANTS)


def exp05_window_variant(name):
    """One materialized EXP-05 window variant, or ``None``."""
    return _EXP05_WINDOW_VARIANTS.get(name)


def phase67_arm_variant(experiment, arm, orbit_key):
    """The declaration one (experiment, arm, orbit) row runs.

    Orbit-aware (plan 67-06, D-09): the exp04 encoded arms run their
    orbit-specific declaration — the main-system declaration on 1632 and the
    materialized 851 registration on 851 — and any other orbit refuses for
    an encoded arm, exactly as ``phase67_registry``'s census-agreement check
    enforces at admission. Raw arms and every other experiment resolve the
    arm's static declaration on any registered orbit. EXP-05 resolves the
    materialized ``exp05-lap<L>-<orbit id>`` variant.
    """
    if not isinstance(orbit_key, str):
        raise VariantRefused(
            f"the orbit key must be variant/fidelity/id text; got {orbit_key!r}"
        )
    if experiment == "exp05":
        if arm not in ("lap1", "lap2", "lap5", "lap10"):
            raise VariantRefused(
                f"unknown exp05 window arm {arm!r}; known: lap1, lap2, lap5, lap10"
            )
        orbit_id = orbit_key.rsplit("/", 1)[-1]
        declaration = _EXP05_WINDOW_VARIANTS.get(f"exp05-{arm}-{orbit_id}")
        if declaration is None:
            raise VariantRefused(
                f"the exp05 window variant for arm {arm!r} on orbit {orbit_key!r} "
                "is not materialized; it exists only after the committed "
                "metadata capture resolves the exact first-crossing endpoint"
            )
        return declaration
    declaration = phase67_variant(experiment, arm)
    if experiment == "exp04" and declaration.time_features != "raw_tau_ic13":
        if orbit_key == "hierarchical/gold/1632":
            return declaration
        if orbit_key == "hierarchical/gold/851":
            suffix = "-851"
            orbit_declaration = next(
                entry for entry in (
                    EXP04_LOCKED_F1_851_VARIANT, EXP04_LOCKED_F12_851_VARIANT,
                    EXP04_EXP01_F1_851_VARIANT, EXP04_EXP01_F12_851_VARIANT,
                ) if entry.name == declaration.name + suffix
            )
            return orbit_declaration
        raise VariantRefused(
            f"the encoded arm {arm!r} has no orbit-specific registration for "
            f"orbit {orbit_key!r}; encoded arms run only on the registered "
            "panel systems 1632 and 851 (D-09)"
        )
    return declaration


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
    :data:`PHASE67_REGISTRY` extended with any materialized EXP-05 window
    variants (plan 67-06: the lap arms' declarations exist only after the
    committed metadata capture, and the merged table keeps the static
    registration order followed by the materialized names). Any other value
    raises ``VariantRefused`` before any data access, optimizer construction
    or attempt claim. The Phase 66 table stays in
    ``diagnostic_phase66.REGISTRIES``; the fit harness checks it first and
    falls through to this dispatch, so this function needs no Phase 66
    import and the catalog stays declaration-only.

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
    if not _EXP05_WINDOW_VARIANTS:
        return PHASE67_REGISTRY
    return MappingProxyType({
        **PHASE67_REGISTRY, **_EXP05_WINDOW_VARIANTS,
    })
