"""Phase 39 — the sole production corpus reader (parser + version seam).

This is the ONE production ``pinn/`` module allowed to know the on-disk
``.txt`` corpus format (GAP-39-02 narrows DATA-01's single-reader rule to the
production ingestion surface; ``pinn/verification/fixture_loader.py`` is the one
retained probe-local exception). Every other Phase 39 module
(``admission``, ``preprocessing``, ``stages``) consumes typed float64 records
and must never open a corpus path.

Plan 39-02 scope: this module provides the format-aware float64 parser helpers,
the README-confirmed 4->2 variant folder tables, footer/default provenance, the
independently *measured* ``dt_out`` (``median(diff(times))``), the asymmetric
IC/Brutus pairing check, and ``verify_data_version`` (typed match / mismatch /
deferral). The production ``AdmittedSetAdapter`` orchestration class — residency,
``resident_tensor_bytes``, and the ``mem:`` line — is Plan 39-03 (residency /
integration) and is deliberately NOT defined here; this wave must not scan the
real corpus (Plan 07 owns the real-corpus gate).

Do NOT import or delegate to ``fixture_loader`` (GAP-39-02). Do NOT read footer
``dE/E`` or any metrics JSON as an admission input (that lives in ``admission``
and recomputes energy from raw arrays).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from pinn.data.types import (
    DataVersionHashDeferred,
    DataVersionHashMismatch,
    DataVersionHashVerified,
    ParsedTrajectory,
    PhysicalKey,
    RecordKey,
)

# ---------------------------------------------------------------------------
# Structural constants (README File Schemas / File Naming Conventions).
# ---------------------------------------------------------------------------

_HEADER_FIELDS = 3          # ``t N t_cpu`` snapshot header
_BODY_FIELDS = 7            # ``m x y z vx vy vz`` body row
_N_BODIES = 3

# The README-confirmed 4->2 variant-based Brutus->IC mapping (HIGH-3,
# ``simulation_data/Documentation/README.md:90-155``). FOUR Brutus folders map
# to TWO IC folders by VARIANT: the gold IC input folders
# (``ic_*_for_gold_standard``) were deleted as duplicates, so a gold Brutus run
# reads the BASE IC folder of its variant. A gold Brutus record's sibling IC is
# therefore the base IC record of the same ``(variant, id)`` — never a deleted
# ``_for_gold_standard`` folder.
BRUTUS_FOLDER_TABLE: dict[str, tuple[str, str]] = {
    "brutus_hierarchical": ("hierarchical", "base"),
    "brutus_hierarchical_gold_standard": ("hierarchical", "gold"),
    "brutus_standard_quasi_random": ("standard", "base"),
    "brutus_standard_quasi_random_gold_standard": ("standard", "gold"),
}

# Both hierarchical Brutus folders resolve ICs from ``ic_hierarchical``; both
# standard Brutus folders resolve ICs from ``ic_standard_quasi_random``.
IC_FOLDER_FOR_VARIANT: dict[str, str] = {
    "hierarchical": "ic_hierarchical",
    "standard": "ic_standard_quasi_random",
}

# Exact filename grammar. Gold status is carried by the FOLDER name only; the
# filename prefix is always the base ``brutus_<variant>`` / ``ic_<variant>``.
_BRUTUS_NAME_RE = re.compile(r"^brutus_(hierarchical|standard)_(\d{4})\.txt$")
_IC_NAME_RE = re.compile(r"^ic_(hierarchical|standard)_(\d{4})\.txt$")

# GAP-39-09 (RESOLVED-WITH-INSTRUCTION, option A): the relative disagreement at
# which the measured ``dt_out`` warns against the footer/default reference. This
# is a REVERSIBLE diagnostic default, NOT source authority; it never gates
# admission or completeness (clause 4 uses ``times[-1] >= 9.5``).
DT_OUT_WARN_REL_THRESHOLD = 0.01

# Static-invariant softening reused as the ``L_max`` degeneracy floor; distinct
# from ``pinn.constants.EPS_SOFT``. Kept here only for the near-zero reference
# comparison tiny epsilon.
_TINY = 1e-300

# Folder-level footer defaults (README:580-628). Fields without a documented
# folder default remain ``None`` with ``absent`` provenance.
_FOOTER_DEFAULTS: dict[tuple[str, str], dict[str, Any]] = {
    ("standard", "base"): {"tol": 1e-13, "Lw": 118, "dt_out": 0.17, "eta": None},
    ("hierarchical", "base"): {"tol": 1e-15, "Lw": 130, "dt_out": 0.08, "eta": None},
    ("hierarchical", "gold"): {"tol": 1e-13, "Lw": 130, "dt_out": 0.01, "eta": None},
    ("standard", "gold"): {"tol": 1e-13, "Lw": 130, "dt_out": 0.01, "eta": None},
}

# Footer key -> (regex group name) for the ``Result: ... key= value`` schema.
_FOOTER_FIELDS = ("tol", "Lw", "dt_out", "t_end", "eta")

# The on-disk footer spells the output cadence ``dt=`` (README File Schemas);
# ``dt_out`` is this module's semantic reference-field name. Energies
# (``E_initial``/``E_final``/``dE/E``) are deliberately NOT aliased here — they
# are footer-only diagnostics and must never enter ``reference``/admission
# (DATA-02 prohibition; enforced separately by ``test_prohibitions.py``).
_FOOTER_KEY_ALIASES = {"dt": "dt_out"}


class DuplicateRecordError(ValueError):
    """Two files resolve to the same ``RecordKey`` — a hard scan failure."""


class CorpusPathEscape(ValueError):
    """A scanned/opened path resolves outside the configured data root."""


# ---------------------------------------------------------------------------
# Version-comparison seam (DATA-03 / GAP-39-01).
# ---------------------------------------------------------------------------

def verify_data_version(expected_data_version_hash, supplied_data_version_hash):
    """Compare a supplied ``data_version_hash`` against the canonical one.

    * canonical present and equal -> ``DataVersionHashVerified``;
    * canonical present and different -> raise ``DataVersionHashMismatch``;
    * canonical absent (``None``) -> ``DataVersionHashDeferred`` (D-05 /
      GAP-39-01: no producer/hash is invented, the unverified state stays typed
      and observable).
    """
    if expected_data_version_hash is None:
        return DataVersionHashDeferred
    if expected_data_version_hash == supplied_data_version_hash:
        return DataVersionHashVerified
    raise DataVersionHashMismatch(
        f"supplied data_version_hash {supplied_data_version_hash!r} does not "
        f"match canonical {expected_data_version_hash!r}"
    )


# ---------------------------------------------------------------------------
# Root containment.
# ---------------------------------------------------------------------------

def resolve_within_root(root, target):
    """Resolve ``target`` and assert it is contained beneath ``root``.

    Raises ``CorpusPathEscape`` on any traversal/symlink escape. Returns the
    resolved absolute ``Path``.
    """
    root_resolved = Path(root).resolve()
    target_resolved = Path(target).resolve()
    try:
        target_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise CorpusPathEscape(
            f"{target_resolved} is not contained beneath data root {root_resolved}"
        ) from exc
    return target_resolved


# ---------------------------------------------------------------------------
# Footer parsing + provenance.
# ---------------------------------------------------------------------------

def _coerce_number(token):
    try:
        return float(token)
    except ValueError:
        return None


def parse_footer(footer_text, *, variant, fidelity):
    """Parse a ``Result: ...`` footer into reference metadata + provenance.

    Returns ``(reference, provenance, footer_anomalous, missing_names)`` where
    ``reference`` is a dict over ``_FOOTER_FIELDS`` and ``provenance`` maps each
    field to ``'direct'`` (present in the footer), ``'inferred'`` (folder
    default for a footer-absent / partial-missing field), or ``'absent'`` (no
    documented default; stored ``None``).

    * ``footer_text is None`` -> every field inferred from the folder default
      (``absent`` provenance for fields without a default); never anomalous.
    * a full footer -> every field present, ``direct``; not anomalous.
    * a partial footer -> present fields ``direct``; every OTHER field is
      ``footer_anomalous=True`` regardless of whether a folder default exists
      (``inferred`` when a default exists, ``absent`` otherwise), and its name
      is logged in ``missing_names``.
    """
    defaults = _FOOTER_DEFAULTS.get((variant, fidelity), {})
    reference: dict[str, Any] = {k: None for k in _FOOTER_FIELDS}
    provenance: dict[str, str] = {k: "absent" for k in _FOOTER_FIELDS}

    present: dict[str, Any] = {}
    if footer_text is not None:
        # ``key= value`` tokens separated by whitespace; tolerate ``dE/E`` etc.
        for raw_key, raw in re.findall(r"([A-Za-z_][A-Za-z0-9_/]*)\s*=\s*([^\s]+)", footer_text):
            key = _FOOTER_KEY_ALIASES.get(raw_key, raw_key)
            if key in _FOOTER_FIELDS:
                present[key] = _coerce_number(raw)

    footer_anomalous = False
    missing_names: list[str] = []
    for key in _FOOTER_FIELDS:
        if key in present and present[key] is not None:
            reference[key] = present[key]
            provenance[key] = "direct"
        elif key in defaults and defaults[key] is not None:
            reference[key] = defaults[key]
            provenance[key] = "inferred"
            if footer_text is not None:
                footer_anomalous = True
                missing_names.append(key)
        else:
            reference[key] = None
            provenance[key] = "absent"
            if footer_text is not None:
                footer_anomalous = True
                missing_names.append(key)

    # A footer that is PRESENT but omits any documented reference field is
    # anomalous, whether or not that field has a folder-level default -- a
    # partial footer signals an upstream irregularity regardless of whether a
    # fallback exists. A fully-absent footer is the ordinary inferred case
    # (never anomalous). ``missing_names`` is retained on the outcome for the
    # adapter/log layer (Plan 03) to report.
    return reference, provenance, footer_anomalous, tuple(missing_names)


def measure_dt_out(times):
    """Independently measured ``dt_out`` = ``median(diff(times))`` (float64)."""
    arr = np.asarray(times, dtype=np.float64)
    if arr.size < 2:
        return float("nan")
    return float(np.median(np.diff(arr)))


def dt_out_disagreement_warns(measured, reference):
    """True iff the finite relative disagreement exceeds the reversible 1%
    GAP-39-09 threshold. Non-finite / absent reference never warns."""
    if reference is None:
        return False
    m = float(measured)
    r = float(reference)
    if not np.isfinite(m) or not np.isfinite(r):
        return False
    denom = max(abs(r), _TINY)
    return abs(m - r) / denom > DT_OUT_WARN_REL_THRESHOLD


# ---------------------------------------------------------------------------
# Float64 block parsing.
# ---------------------------------------------------------------------------

@dataclass
class ParsedBrutus:
    """Raw float64 parse of a Brutus trajectory plus structural diagnostics.

    ``positions``/``velocities`` are ``(n_complete, 3, 3)`` float64 arrays over
    the COMPLETE (3-body) snapshot blocks in file order — including any
    non-finite complete block, so the admission gate (GAP-39-05) can count and
    quarantine them. ``n_malformed_blocks`` counts partial-body blocks that are
    NOT salvaged as samples.
    """

    times: Any
    positions: Any
    velocities: Any
    masses: Any
    n_complete_blocks: int
    n_nonfinite_blocks: int
    n_malformed_blocks: int
    footer_raw: Any = None


def _split_blocks(text):
    """Split file text into blank-line-separated blocks; capture the footer.

    Returns ``(blocks, footer)`` where each block is a list of stripped
    non-empty lines and ``footer`` is the ``Result:`` line (or ``None``).
    """
    blocks: list[list[str]] = []
    footer = None
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if current:
                blocks.append(current)
                current = []
            continue
        if line.startswith("Result:"):
            footer = line
            if current:
                blocks.append(current)
                current = []
            continue
        current.append(line)
    if current:
        blocks.append(current)
    return blocks, footer


def parse_brutus_text(text):
    """Parse Brutus file *text* into a :class:`ParsedBrutus` (float64).

    A COMPLETE block is one ``t N t_cpu`` header followed by exactly three
    ``m x y z vx vy vz`` rows. A block with the wrong row count is a malformed
    (partial) block: counted, never salvaged. Non-finite complete blocks are
    retained in the arrays and counted so the admission gate can quarantine the
    whole trajectory (GAP-39-05).
    """
    blocks, footer = _split_blocks(text)
    times: list[float] = []
    positions: list[list[list[float]]] = []
    velocities: list[list[list[float]]] = []
    masses = None
    n_nonfinite = 0
    n_malformed = 0

    for block in blocks:
        if len(block) != _N_BODIES + 1:
            n_malformed += 1
            continue
        header = block[0].split()
        body_rows = [row.split() for row in block[1:]]
        if len(header) != _HEADER_FIELDS or any(len(r) != _BODY_FIELDS for r in body_rows):
            n_malformed += 1
            continue
        t = float(header[0])
        block_mass = np.array([float(r[0]) for r in body_rows], dtype=np.float64)
        block_pos = np.array([[float(v) for v in r[1:4]] for r in body_rows], dtype=np.float64)
        block_vel = np.array([[float(v) for v in r[4:7]] for r in body_rows], dtype=np.float64)
        if masses is None:
            masses = block_mass
        times.append(t)
        positions.append(block_pos.tolist())
        velocities.append(block_vel.tolist())
        if not (np.all(np.isfinite(block_pos)) and np.all(np.isfinite(block_vel))
                and np.all(np.isfinite(block_mass)) and np.isfinite(t)):
            n_nonfinite += 1

    n_complete = len(times)
    times_arr = np.asarray(times, dtype=np.float64)
    pos_arr = (np.asarray(positions, dtype=np.float64)
               if positions else np.zeros((0, _N_BODIES, 3), dtype=np.float64))
    vel_arr = (np.asarray(velocities, dtype=np.float64)
               if velocities else np.zeros((0, _N_BODIES, 3), dtype=np.float64))
    if masses is None:
        masses = np.zeros((_N_BODIES,), dtype=np.float64)
    return ParsedBrutus(
        times=times_arr, positions=pos_arr, velocities=vel_arr, masses=masses,
        n_complete_blocks=n_complete, n_nonfinite_blocks=n_nonfinite,
        n_malformed_blocks=n_malformed, footer_raw=footer,
    )


def parse_brutus_file(path, *, root=None):
    """Read and parse a Brutus ``.txt`` file (float64), enforcing containment."""
    resolved = resolve_within_root(root, path) if root is not None else Path(path)
    text = Path(resolved).read_text(encoding="utf-8")
    return parse_brutus_text(text)


def parse_ic_text(text):
    """Parse a 3-line IC file into ``(masses, positions, velocities)`` float64."""
    rows = [line.split() for line in text.splitlines() if line.strip()]
    if len(rows) != _N_BODIES or any(len(r) != _BODY_FIELDS for r in rows):
        raise ValueError(
            f"IC text must be exactly {_N_BODIES} rows of {_BODY_FIELDS} fields"
        )
    masses = np.array([float(r[0]) for r in rows], dtype=np.float64)
    positions = np.array([[float(v) for v in r[1:4]] for r in rows], dtype=np.float64)
    velocities = np.array([[float(v) for v in r[4:7]] for r in rows], dtype=np.float64)
    return masses, positions, velocities


def parse_ic_file(path, *, root=None):
    resolved = resolve_within_root(root, path) if root is not None else Path(path)
    return parse_ic_text(Path(resolved).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Identity from folder + filename.
# ---------------------------------------------------------------------------

def record_key_from_brutus(folder_name, filename):
    """Structural ``RecordKey`` from a Brutus folder + exact filename.

    Folder pins ``(variant, fidelity)``; filename pins ``(variant_token, id)``.
    A folder/filename variant disagreement or a non-matching name is a hard
    error — identity never depends on path formatting.
    """
    if folder_name not in BRUTUS_FOLDER_TABLE:
        raise ValueError(f"unknown Brutus folder {folder_name!r}")
    variant, fidelity = BRUTUS_FOLDER_TABLE[folder_name]
    match = _BRUTUS_NAME_RE.match(filename)
    if match is None:
        raise ValueError(f"malformed Brutus filename {filename!r}")
    name_variant, id_str = match.group(1), match.group(2)
    if name_variant != variant:
        raise ValueError(
            f"filename variant {name_variant!r} disagrees with folder "
            f"variant {variant!r} for {filename!r}"
        )
    return RecordKey(variant, fidelity, int(id_str))


def physical_key_from_ic(folder_name, filename):
    """Structural ``PhysicalKey`` from an IC folder + exact filename."""
    match = _IC_NAME_RE.match(filename)
    if match is None:
        raise ValueError(f"malformed IC filename {filename!r}")
    variant, id_str = match.group(1), match.group(2)
    expected_folder = IC_FOLDER_FOR_VARIANT.get(variant)
    if expected_folder is not None and folder_name != expected_folder:
        raise ValueError(
            f"IC folder {folder_name!r} disagrees with filename variant "
            f"{variant!r} (expected {expected_folder!r})"
        )
    return PhysicalKey(variant, int(id_str))


# ---------------------------------------------------------------------------
# Asymmetric IC/Brutus pairing (DATA-04 physical-key grouping, HIGH-3).
# ---------------------------------------------------------------------------

@dataclass
class PairingResult:
    """Outcome of pairing Brutus records to their base IC siblings by
    ``(variant, id)`` — NOT by a 1:1 folder correspondence."""

    missing_ic_sibling: tuple = field(default_factory=tuple)
    missing_brutus_sibling: tuple = field(default_factory=tuple)


def pair_by_physical_key(brutus_physical_keys, ic_physical_keys):
    """Detect asymmetric pairing anomalies by ``PhysicalKey`` grouping.

    A Brutus record is ``missing_ic_sibling`` ONLY when its ``(variant, id)``
    has no base IC record (never merely because no ``_for_gold_standard`` IC
    folder exists — gold Brutus pairs to the BASE IC of the same variant). An IC
    record with no Brutus record of the same ``(variant, id)`` is
    ``missing_brutus_sibling``. Both are typed anomalies naming the missing
    sibling, never a silent skip or silent admission.
    """
    brutus = set(brutus_physical_keys)
    ic = set(ic_physical_keys)
    missing_ic = tuple(sorted(brutus - ic))
    missing_brutus = tuple(sorted(ic - brutus))
    return PairingResult(missing_ic_sibling=missing_ic,
                         missing_brutus_sibling=missing_brutus)


# ---------------------------------------------------------------------------
# Bridge: raw parse -> typed ``ParsedTrajectory`` for the admission gate.
# ---------------------------------------------------------------------------

def to_parsed_trajectory(record_key, parsed_brutus):
    """Wrap a :class:`ParsedBrutus` as the typed ``ParsedTrajectory`` handed to
    ``pinn.data.admission.evaluate_admission``."""
    return ParsedTrajectory(
        record_key=record_key,
        times=parsed_brutus.times,
        positions=parsed_brutus.positions,
        velocities=parsed_brutus.velocities,
        masses=parsed_brutus.masses,
    )
