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

import json
import math
import os
import re
import subprocess
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import torch

from pinn.data.types import (
    AdmittedRecord,
    DataVersionHashDeferred,
    DataVersionHashMismatch,
    DataVersionHashVerified,
    Fidelity,
    ParsedTrajectory,
    PhysicalKey,
    RecordKey,
    StageLabel,
    Variant,
)
from pinn.data.admission import evaluate_admission
from pinn.data.preprocessing import (
    GaugeDegenerateError,
    MassInvarianceError,
    PreprocessAssertionError,
    build_raw_ic13,
    compute_invariants,
    compute_normalization_stats,
    normalize_ic13,
    preprocess_trajectory,
)
from pinn.data.stages import classify_stage_label
from pinn.loss_catalog import _matched_plummer_components

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


class EvidenceRedactionError(ValueError):
    """``AdmittedSetAdapter.evidence_lines()`` detected a host-path leak — the
    resolved corpus root or the user's home prefix survived into a projected
    evidence line. The caller must not persist the returned lines; the adapter
    refuses to silently strip a leaking line (fail-closed)."""


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


# ===========================================================================
# Production in-memory admitted-set adapter (DATA-01..03, Plan 39-03).
# ===========================================================================

# DATA-01 explicit memory budget + watermark (never inferred from RSS/MPS).
MEMORY_CAPACITY_DEFAULT = 24 * 1024 ** 3
MEMORY_WATERMARK_DEFAULT = 0.7


def _validate_adapter_config(capacity_bytes, memory_watermark, interim_s0, device):
    """Fail-closed validation of residency/configuration inputs (DATA-01).

    Every check runs before ``_resolve_root``, ``_scan_and_admit``, tensor
    materialization, or memory logging so an invalid caller configuration
    cannot bypass the explicit CPU memory-watermark gate or produce misleading
    ``mem:`` evidence. Returns the normalized CPU ``torch.device``.
    """
    # capacity_bytes: positive finite integer.
    if isinstance(capacity_bytes, bool) or not isinstance(capacity_bytes, (int, float)):
        raise TypeError(
            f"capacity_bytes must be a positive finite int; got {capacity_bytes!r}")
    if not math.isfinite(capacity_bytes) or capacity_bytes <= 0:
        raise ValueError(
            f"capacity_bytes must be positive and finite; got {capacity_bytes!r}")

    # memory_watermark: finite in (0, 1].
    if isinstance(memory_watermark, bool) or not isinstance(memory_watermark, (int, float)):
        raise TypeError(
            f"memory_watermark must be a finite float in (0, 1]; got {memory_watermark!r}")
    if not math.isfinite(memory_watermark) or not (0 < memory_watermark <= 1):
        raise ValueError(
            f"memory_watermark must be in (0, 1] and finite; got {memory_watermark!r}")

    # interim_s0: finite and positive.
    if isinstance(interim_s0, bool) or not isinstance(interim_s0, (int, float)):
        raise TypeError(
            f"interim_s0 must be a finite positive float; got {interim_s0!r}")
    if not math.isfinite(interim_s0) or interim_s0 <= 0:
        raise ValueError(
            f"interim_s0 must be positive and finite; got {interim_s0!r}")

    # device: CPU-only. Normalize through torch.device so malformed devices
    # (including strings that torch cannot parse) are rejected explicitly.
    try:
        normalized = torch.device(device)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"malformed device {device!r}: {exc}") from exc
    if normalized.type != "cpu":
        raise ValueError(
            f"only CPU residency is supported; got device={device!r} "
            f"(normalized type={normalized.type})")
    return normalized


# Corpus layout (README File Naming Conventions; mirrored by the TinyCorpus
# fixture). The four README-documented Brutus folders live beneath
# ``<root>/brutus_output/``; the two IC folders beneath ``<root>/ic_final/``.
BRUTUS_SUBDIR = "brutus_output"
IC_SUBDIR = "ic_final"
README_BRUTUS_FOLDERS = tuple(BRUTUS_FOLDER_TABLE.keys())

DATA_ROOT_ENV = "GSD_DATA_ROOT"
ALLOW_PARTIAL_ENV = "GSD_ALLOW_PARTIAL_DATA_ROOT"
DEFAULT_BLACKLIST_NAME = "problematic_ics_blacklist.json"

# GAP-39-07 / HIGH-1 coarse ballpark decomposition. Per admitted snapshot there
# are 3 bodies, each contributing 3 position + 3 velocity components = 6 dof, so
# the snapshot payload is ``3 bodies x 6 dof = 18`` floats; the per-trajectory
# shared time adds 1 float per snapshot. Concretely ``floats_per_snapshot = 19``.
# This is a LOWER bound by construction: it excludes the per-record IC13
# (13 floats), raw masses (3 floats), normalization caches, and index tensors,
# so the authoritative deduplicated ``resident_tensor_bytes`` is expected to be
# at least this large.
FLOATS_PER_SNAPSHOT = 3 * 6 + 1  # 19


class DataSourceRootMissing(ValueError):
    """The resolved corpus root does not exist at all (claude M6)."""


class DataSourceRootIncomplete(ValueError):
    """The resolved corpus root exists but is missing one or more of the four
    README-documented Brutus folders — the HIGH-A content sanity guard against a
    partial worktree copy silently producing a green run over a tiny corpus."""


class BlacklistSchemaError(ValueError):
    """The blacklist file is missing, unreadable, or fails the exact
    ``{"hierarchical": [...], "standard": [...]}`` integer-list schema."""


# ---------------------------------------------------------------------------
# Root resolution (explicit -> GSD_DATA_ROOT -> main-repo git-common default).
# ---------------------------------------------------------------------------

def default_data_root():
    """Main-repo ``simulation_data/Data`` derived as the PARENT of
    ``git rev-parse --git-common-dir`` plus ``/simulation_data/Data`` (HIGH-A).

    The git COMMON dir is shared across worktrees, so its parent is the main-repo
    root; ``--show-toplevel`` is deliberately NOT used because it returns the
    worktree-local toplevel (a PARTIAL ``simulation_data/Data/`` in a linked
    worktree). Never a hardcoded personal absolute-path literal (claude M6).
    """
    common = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"], text=True).strip()
    main_repo_root = Path(common).resolve().parent
    return main_repo_root / "simulation_data" / "Data"


def load_blacklist_file(path):
    """Load + fail-closed-validate the blacklist file.

    Schema: a JSON object with EXACTLY top-level keys ``hierarchical`` and
    ``standard``, each an integer-like list. Any missing/unreadable file, extra
    or missing key, or non-integer entry raises :class:`BlacklistSchemaError`
    (never a silent empty-blacklist substitution). Returns
    ``(blacklisted_physical_keys, entries_by_family)``.
    """
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise BlacklistSchemaError(f"blacklist file {p} unreadable/invalid: {exc}") from exc
    if not isinstance(data, dict) or set(data.keys()) != {"hierarchical", "standard"}:
        raise BlacklistSchemaError(
            f"blacklist schema must have exactly keys hierarchical/standard; got "
            f"{sorted(data.keys()) if isinstance(data, dict) else type(data)}")
    keys: set[PhysicalKey] = set()
    entries: dict[str, list[int]] = {}
    for family in ("hierarchical", "standard"):
        listed = data[family]
        if not isinstance(listed, list):
            raise BlacklistSchemaError(f"blacklist family {family!r} must be a list")
        family_ids: list[int] = []
        for value in listed:
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise BlacklistSchemaError(
                    f"blacklist family {family!r} entry {value!r} is not a non-negative int")
            keys.add(PhysicalKey(family, value))
            family_ids.append(value)
        entries[family] = family_ids
    return frozenset(keys), entries


# ---------------------------------------------------------------------------
# GAP-39-07 deterministic resident-tensor accounting.
# ---------------------------------------------------------------------------

def resident_tensor_bytes(tensors):
    """Deduplicated owned fp32 storage bytes — the authoritative DATA-01
    numerator (GAP-39-07). Views share their parent's ``untyped_storage`` and are
    counted ONCE; unrelated process allocations are never included because only
    the supplied tensors are visited."""
    seen: dict[tuple, int] = {}
    for tensor in tensors:
        storage = tensor.untyped_storage()
        seen[(storage.data_ptr(), storage.nbytes())] = storage.nbytes()
    return sum(seen.values())


def format_mem_line(resident_bytes, capacity_bytes, watermark=MEMORY_WATERMARK_DEFAULT):
    """The exact deterministic ``mem:`` log line."""
    fraction = resident_bytes / capacity_bytes
    return f"mem: {resident_bytes} ({fraction:.6f}) watermark={watermark}"


def resident_ballpark_bytes(total_admitted_snapshots):
    """Coarse independent LOWER-bound cross-check for ``resident_tensor_bytes``
    (HIGH-1): counts the resident fp32 floats actually materialized per snapshot
    (``FLOATS_PER_SNAPSHOT = 19``), never the per-body-row width."""
    return total_admitted_snapshots * FLOATS_PER_SNAPSHOT * 4


def resident_is_misfit(resident_bytes, ballpark_bytes):
    """True iff the authoritative deduplicated numerator falls outside the
    documented band ``[0.5x, 3.0x]`` of the lower-bound ballpark — a signal that
    an ``untyped_storage()`` dedup miscount could silently flip the watermark."""
    if ballpark_bytes <= 0:
        return False
    return resident_bytes < ballpark_bytes * 0.5 or resident_bytes > ballpark_bytes * 3.0


class AdmittedSetAdapter:
    """The sole production in-memory admitted-set adapter (DATA-01..03).

    Two-pass initialization without a corpus reread: (1) resolve/verify the
    read-only root, load + validate the blacklist, then scan every Brutus record
    once (``num_workers=0``), gating each through ``evaluate_admission`` and
    classifying admitted base-Set-1a records via the sole
    ``pinn.data.stages.classify_stage_label``; (2) derive admitted-only
    normalization statistics and materialize normalized CPU fp32 owned tensors.
    All accessors are memory-only after initialization; the source corpus may be
    removed without breaking any accessor.
    """

    def __init__(self, *, root=None, data_root=None, blacklist_path=None,
                 precision: str = "float32", device: str = "cpu",
                 run_dir=None, version_metadata_path=None,
                 capacity_bytes: int = MEMORY_CAPACITY_DEFAULT,
                 memory_watermark: float = MEMORY_WATERMARK_DEFAULT,
                 interim_s0: float = 0.01,
                 remediation_quarantine=frozenset(),
                 expected_data_version_hash=None,
                 supplied_data_version_hash=None):
        if precision != "float32":
            raise ValueError(f"only float32 residency is supported; got {precision!r}")
        # DATA-01 fail-closed safety boundary: validate capacity, watermark,
        # interim_s0, and CPU residency BEFORE root resolution, corpus scanning,
        # tensor materialization, or memory logging.
        self._device = _validate_adapter_config(
            capacity_bytes, memory_watermark, interim_s0, device)
        self._dtype = torch.float32
        self._capacity_bytes = int(capacity_bytes)
        self._watermark = float(memory_watermark)
        self.classifier_interim_s0 = float(interim_s0)
        self._remediation_quarantine = frozenset(remediation_quarantine)
        self.run_dir = run_dir
        self.init_log: list[str] = []

        self.data_root = self._resolve_root(root, data_root)
        self.blacklisted_physical_keys = self._load_blacklist(blacklist_path)
        self._canonical_hash = self._load_version_hash(
            version_metadata_path, expected_data_version_hash)
        if supplied_data_version_hash is not None:
            # Optional at-init comparison (raises on mismatch); the deferred-until
            # -call path is the norm exercised by the frozen contract tests.
            verify_data_version(self._canonical_hash, supplied_data_version_hash)

        # Two-pass ingestion.
        self._records: dict[RecordKey, AdmittedRecord] = {}
        self._trajectory_tensors: dict[RecordKey, tuple] = {}
        self._resident_tensors: list = []
        self.folder_counts: dict[str, dict] = {}
        self._total_admitted_snapshots = 0
        candidates = self._scan_and_admit()
        if not candidates:
            raise ValueError(
                f"admitted set is empty under {self.data_root}; refusing to build "
                "a green run over zero admitted records")
        self._materialize(candidates)
        self._emit_mem_log()

    # -- root / blacklist / version resolution -------------------------------
    def _resolve_root(self, root, data_root):
        chosen = root if root is not None else data_root
        if chosen is not None:
            resolved = Path(chosen)
            source = "explicit"
        elif os.environ.get(DATA_ROOT_ENV):
            resolved = Path(os.environ[DATA_ROOT_ENV])
            source = "env:GSD_DATA_ROOT"
        else:
            resolved = default_data_root()
            source = "git_common_dir_default"

        if not resolved.exists():
            raise DataSourceRootMissing(
                f"data source root {resolved} does not exist (resolved via {source}); "
                f"set {DATA_ROOT_ENV} to the corpus Data/ directory")
        resolved = resolved.resolve()

        self.data_root_source = source

        allow_partial = os.environ.get(ALLOW_PARTIAL_ENV) == "1"
        self.allow_partial_data_root = 1 if allow_partial else 0
        missing = [f for f in README_BRUTUS_FOLDERS
                   if not (resolved / BRUTUS_SUBDIR / f).is_dir()]
        if missing and not allow_partial:
            raise DataSourceRootIncomplete(
                f"data source root {resolved} is missing Brutus folders {missing}; "
                f"a partial/incomplete root cannot silently scan a tiny corpus. Set "
                f"{ALLOW_PARTIAL_ENV}=1 only for small unit-test fixtures (never the "
                "Plan-07 real-corpus gate)")

        self.init_log.append(f"root: {resolved} source={source}")
        for f in README_BRUTUS_FOLDERS:
            self.init_log.append(
                f"brutus_folder {f} present={(resolved / BRUTUS_SUBDIR / f).is_dir()}")
        self.init_log.append(f"allow_partial_data_root={self.allow_partial_data_root}")
        return resolved

    def _load_blacklist(self, blacklist_path):
        if blacklist_path is None:
            blacklist_path = self.data_root / DEFAULT_BLACKLIST_NAME
        keys, entries = load_blacklist_file(blacklist_path)
        for family, ids in entries.items():
            self.init_log.append(f"blacklist {family} n_blacklist_entries={len(ids)}")
        self._blacklist_entries = entries
        return keys

    def _load_version_hash(self, version_metadata_path, expected_data_version_hash):
        canonical = expected_data_version_hash
        if version_metadata_path is not None:
            vpath = Path(version_metadata_path)
            if vpath.exists():
                meta = json.loads(vpath.read_text(encoding="utf-8"))
                canonical = meta.get("data_version_hash")
        return canonical

    # -- pass 1: scan + gate + classify (no residency yet) -------------------
    def _scan_and_admit(self):
        candidates = []
        raw_ic13_population = []
        trajectory_energies = []
        gold_numeric = 0
        # Per-fidelity blacklist disposition counters (39-03-PLAN.md:85 contract).
        # Keyed by the fidelity component of BRUTUS_FOLDER_TABLE[folder]; every
        # fidelity is initialized so a fidelity with zero blacklisted files still
        # emits a ``0`` line rather than being absent.
        blacklist_by_fidelity = {
            fidelity: {"n_present_on_disk": 0, "n_excluded": 0}
            for _, (_, fidelity) in BRUTUS_FOLDER_TABLE.items()
        }

        for folder, (variant, fidelity) in sorted(BRUTUS_FOLDER_TABLE.items()):
            counts = dict(found=0, admitted=0, rejected=0, quarantined=0, dropped_samples=0)
            folder_dir = self.data_root / BRUTUS_SUBDIR / folder
            files = sorted(folder_dir.glob("*.txt")) if folder_dir.is_dir() else []
            for path in files:
                counts["found"] += 1
                parsed_brutus = parse_brutus_file(path, root=self.data_root)
                record_key = record_key_from_brutus(folder, path.name)
                if record_key.physical_key in self.blacklisted_physical_keys:
                    blacklist_by_fidelity[fidelity]["n_present_on_disk"] += 1
                parsed = to_parsed_trajectory(record_key, parsed_brutus)
                reference, provenance, _anom, _missing = parse_footer(
                    parsed_brutus.footer_raw, variant=variant, fidelity=fidelity)
                measured = measure_dt_out(parsed_brutus.times)
                outcome = evaluate_admission(
                    parsed,
                    blacklist=self.blacklisted_physical_keys,
                    remediation_quarantine=self._remediation_quarantine,
                    dt_out=reference.get("dt_out"))
                counts["dropped_samples"] += outcome.dropped_samples
                if record_key.physical_key in self.blacklisted_physical_keys:
                    if outcome.disposition != "admit":
                        blacklist_by_fidelity[fidelity]["n_excluded"] += 1
                if outcome.disposition == "reject":
                    counts["rejected"] += 1
                    continue
                if outcome.disposition == "quarantine":
                    counts["quarantined"] += 1
                    continue
                # disposition == "admit": preprocess -> invariants -> classify.
                try:
                    pre = preprocess_trajectory(
                        parsed_brutus.times, parsed_brutus.positions,
                        parsed_brutus.velocities, parsed_brutus.masses)
                    inv = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
                    raw_ic13 = build_raw_ic13(
                        pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, inv.E)
                    # CONF-02 (D-09/D-10/D-12): the §3.4 S_H components,
                    # captured in float64 at admission — BEFORE the fp32
                    # residency cast — from the completed CONF-09 frame tuple
                    # {position: r_prime, time: u, velocity: dr_prime_du,
                    # masses: ordered_raw} at snapshot 0. The single
                    # loss-catalog seam supplies both components at the
                    # training softening; ``uabs0`` is the ABSOLUTE VALUE of
                    # the softened potential (``V_eps < 0``, so
                    # ``uabs0 = -V_eps``), never the signed Hamiltonian.
                    kinetic0, potential0 = _matched_plummer_components(
                        pre.r_gauge[0], pre.v_gauge[0], pre.masses_ordered,
                        dtype=torch.float64, device=torch.device("cpu"))
                    k0 = float(kinetic0[0])
                    uabs0 = float(abs(potential0[0]))
                except (GaugeDegenerateError, PreprocessAssertionError, MassInvarianceError):
                    counts["quarantined"] += 1
                    continue

                interim = SimpleNamespace(
                    variant=Variant(variant), fidelity=Fidelity(fidelity),
                    E=inv.E, l_ratio=inv.l_ratio, Q=inv.Q, s_min=inv.s_min)
                label = classify_stage_label(interim, self.classifier_interim_s0)
                if fidelity == "gold" and label is not StageLabel.UNASSIGNED:
                    gold_numeric += 1

                # CONF-09 completion (GAP-46-07 owner ruling 2026-07-28, option
                # A): resident arrays carry the FULL canonical pipeline — COM /
                # zero-momentum boost gauge, canonical body order, rotation
                # gauge, and D/V scaling. Times stay native; the u = t/T
                # normalization lives at the sampling boundary in
                # ``pinn/data/batches.py``, which is what makes dr'/du = v'.
                candidates.append(SimpleNamespace(
                    record_key=record_key, variant=variant, fidelity=fidelity,
                    times=parsed_brutus.times, positions=pre.r_gauge,
                    velocities=pre.v_gauge,
                    masses_ordered=pre.masses_ordered, raw_ic13=raw_ic13,
                    inv=inv, measured=measured, k0=k0, uabs0=uabs0,
                    dt_reference=reference.get("dt_out"),
                    dt_provenance=provenance.get("dt_out"),
                    n_snapshots=int(pre.r_gauge.shape[0]),
                    stage_label=label))
                raw_ic13_population.append(raw_ic13)
                trajectory_energies.append(inv.E)
                self._total_admitted_snapshots += int(pre.r_gauge.shape[0])
                counts["admitted"] += 1

            assert counts["found"] == (
                counts["admitted"] + counts["rejected"] + counts["quarantined"]), (
                f"folder {folder} accounting broken: {counts}")
            self.folder_counts[folder] = counts
            self.init_log.append(
                f"folder {folder} found={counts['found']} admitted={counts['admitted']} "
                f"rejected={counts['rejected']} quarantined={counts['quarantined']} "
                f"dropped_samples={counts['dropped_samples']}")

        # Absent listed blacklist IDs (present in the file, absent on disk).
        present_on_disk = set()
        for folder, (variant, _fid) in BRUTUS_FOLDER_TABLE.items():
            folder_dir = self.data_root / BRUTUS_SUBDIR / folder
            if folder_dir.is_dir():
                for path in folder_dir.glob("*.txt"):
                    present_on_disk.add(record_key_from_brutus(folder, path.name).physical_key)
        for family, ids in self._blacklist_entries.items():
            absent = [i for i in ids if PhysicalKey(family, i) not in present_on_disk]
            self.init_log.append(f"blacklist {family} absent_ids={absent}")

        # Per-fidelity blacklist disposition counts (39-03-PLAN.md:85 contract):
        # n_present_on_disk = blacklisted records of this fidelity found on disk;
        # n_excluded = those not admitted (clause-1 defense-in-depth). Emitted in
        # sorted fidelity order (base before gold) for byte-stable evidence.
        for fidelity in sorted(blacklist_by_fidelity):
            present = blacklist_by_fidelity[fidelity]["n_present_on_disk"]
            excluded = blacklist_by_fidelity[fidelity]["n_excluded"]
            self.init_log.append(
                f"blacklist {fidelity} n_present_on_disk={present} n_excluded={excluded}")

        # Zero-gold numeric invariant (hard fail-closed).
        if gold_numeric != 0:
            raise ValueError(
                f"gold_numeric_stage_count must be 0; got {gold_numeric} — a gold "
                "record received a numeric Stage label")
        self.gold_numeric_stage_count = 0
        self._raw_ic13_population = raw_ic13_population
        self._trajectory_energies = trajectory_energies
        return candidates

    # -- pass 2: admitted-only normalization + fp32 residency ----------------
    def _materialize(self, candidates):
        stats = compute_normalization_stats(
            np.asarray(self._raw_ic13_population, dtype=np.float64),
            np.asarray(self._trajectory_energies, dtype=np.float64))
        self._normalization_stats = stats
        for cand in candidates:
            times_t = torch.tensor(
                np.asarray(cand.times, dtype=np.float64), dtype=self._dtype, device=self._device)
            pos_t = torch.tensor(
                np.asarray(cand.positions, dtype=np.float64), dtype=self._dtype, device=self._device)
            vel_t = torch.tensor(
                np.asarray(cand.velocities, dtype=np.float64), dtype=self._dtype, device=self._device)
            normalized = normalize_ic13(cand.raw_ic13, stats)
            ic13_t = torch.tensor(normalized, dtype=self._dtype, device=self._device)
            masses_t = torch.tensor(
                np.asarray(cand.masses_ordered, dtype=np.float64), dtype=self._dtype,
                device=self._device)
            raw_ic13_t = torch.tensor(
                np.asarray(cand.raw_ic13, dtype=np.float64), dtype=self._dtype,
                device=self._device)
            self._resident_tensors.extend([times_t, pos_t, vel_t, ic13_t, masses_t, raw_ic13_t])
            self._trajectory_tensors[cand.record_key] = (times_t, pos_t, vel_t)

            record = AdmittedRecord(
                record_key=cand.record_key,
                physical_key=cand.record_key.physical_key,
                variant=Variant(cand.variant), fidelity=Fidelity(cand.fidelity),
                ic13=ic13_t, masses=masses_t, raw_ic13=raw_ic13_t,
                dt_out_measured=float(cand.measured),
                dt_out_reference=cand.dt_reference,
                dt_out_reference_provenance=cand.dt_provenance,
                n_snapshots=cand.n_snapshots,
                E=float(cand.inv.E), l_ratio=cand.inv.l_ratio, Q=float(cand.inv.Q),
                min_separation=float(cand.inv.s_min),
                k0=float(cand.k0), uabs0=float(cand.uabs0),
                stage_label=cand.stage_label)
            self._records[cand.record_key] = record

    # -- accounting + logging ------------------------------------------------
    def _emit_mem_log(self):
        resident = self.resident_tensor_bytes()
        self._ballpark_bytes = resident_ballpark_bytes(self._total_admitted_snapshots)
        self.mem_ballpark_bytes = self._ballpark_bytes
        self.init_log.append(self.mem_line())
        self.init_log.append(f"mem_ballpark={self._ballpark_bytes}")
        self.init_log.append(f"gold_numeric_stage_count={self.gold_numeric_stage_count}")
        self._check_resident_ballpark()
        fraction = resident / self._capacity_bytes
        if fraction > self._watermark:
            raise RuntimeError(
                f"resident memory fraction {fraction:.6f} exceeds watermark {self._watermark}")

    def _check_resident_ballpark(self):
        resident = self.resident_tensor_bytes()
        if resident_is_misfit(resident, self._ballpark_bytes):
            warnings.warn(
                f"resident_tensor_bytes_misfit resident={resident} "
                f"ballpark={self._ballpark_bytes}")

    # -- redacted evidence projection ----------------------------------------
    # ``init_log`` is the in-process operator diagnostic and must retain the
    # resolved absolute root (39-03-PLAN.md:88 "the resolved root is never
    # opaque"). The retained ``scan.log`` must not contain any absolute source
    # root, username, or hostname (39-07-PLAN.md:29, N12). These two consumers
    # have opposite requirements, so the adapter exposes a separate redacted
    # projection — ``evidence_lines()`` — that Plan 39-12 serializes into
    # ``scan.log`` instead of dumping ``init_log`` verbatim.
    _ROOT_PREFIX = "root: "
    _REDACTED_ROOT_FMT = "GSD_DATA_ROOT=$GSD_DATA_ROOT source={source}"

    def evidence_lines(self):
        """Redacted, verbatim-order projection of ``init_log`` for retention.

        The single ``root: <absolute> source=<src>`` entry is replaced with the
        literal placeholder ``GSD_DATA_ROOT=$GSD_DATA_ROOT source=<src>``
        (``$GSD_DATA_ROOT`` is the literal string, not an expansion) at the same
        position; every other entry passes through verbatim.

        Fail-closed: if any projected line still contains the resolved
        ``data_root`` or the user's home prefix, raises ``EvidenceRedactionError``
        rather than returning a silently-stripped or silently-leaking artifact.
        """
        source = getattr(self, "data_root_source", "unknown")
        redacted_root = self._REDACTED_ROOT_FMT.format(source=source)
        root_str = str(self.data_root)
        home_str = str(Path.home())

        projected = []
        for ln in self.init_log:
            if ln.startswith(self._ROOT_PREFIX):
                projected.append(redacted_root)
            else:
                projected.append(ln)

        # Fail-closed guard: a leak is a hard error, never a silently-stripped
        # line. Use host-agnostic needles so the guard holds on any machine.
        for ln in projected:
            if root_str in ln:
                raise EvidenceRedactionError(
                    f"evidence line contains resolved data_root: {ln!r}")
            if home_str in ln:
                raise EvidenceRedactionError(
                    f"evidence line contains home prefix: {ln!r}")

        return tuple(projected)

    # -- memory-only accessors ----------------------------------------------
    def record_keys(self):
        return tuple(sorted(self._records.keys()))

    def get(self, key):
        return self._records[key]

    def n_snapshots(self, key):
        return self._records[key].n_snapshots

    def snapshot_times(self, key):
        return self._trajectory_tensors[key][0]

    def snapshot_positions(self, key):
        return self._trajectory_tensors[key][1]

    def snapshot_velocities(self, key):
        return self._trajectory_tensors[key][2]

    def k0(self, key):
        """Float64 §3.4 S_H kinetic component captured at admission (CONF-02)."""
        return self._records[key].k0

    def uabs0(self, key):
        """Float64 §3.4 S_H |softened potential| captured at admission (CONF-02)."""
        return self._records[key].uabs0

    def acceleration_magnitudes(self, key):
        """Finite-difference full-trajectory acceleration norms from residency.

        DATA-05 uses these observed-snapshot weights only for data-fidelity
        sampling.  No collocation/adaptive policy is encoded here.
        """
        times, _positions, velocities = self._trajectory_tensors[key]
        n = int(times.shape[0])
        if n < 2:
            raise ValueError(f"record {key!r} needs at least two snapshots")
        acceleration = torch.empty_like(velocities)
        acceleration[0] = (velocities[1] - velocities[0]) / (times[1] - times[0])
        acceleration[-1] = (velocities[-1] - velocities[-2]) / (times[-1] - times[-2])
        if n > 2:
            denominator = (times[2:] - times[:-2]).reshape(-1, 1, 1)
            acceleration[1:-1] = (velocities[2:] - velocities[:-2]) / denominator
        return torch.linalg.vector_norm(acceleration.reshape(n, -1), dim=1)

    def dt_out(self, key):
        return self._records[key].dt_out_measured

    def stage_label(self, key):
        return self._records[key].stage_label

    def has_stage(self, key):
        record = self._records.get(key)
        return record is not None and record.stage_label is not StageLabel.UNASSIGNED

    def records_at(self, stage):
        return tuple(
            k for k, r in sorted(self._records.items())
            if r.stage_label is not StageLabel.UNASSIGNED and r.stage_label == stage)

    def records_at_or_below(self, stage):
        return tuple(
            k for k, r in sorted(self._records.items())
            if r.stage_label is not StageLabel.UNASSIGNED
            and r.stage_label.value <= stage.value)

    def is_blacklisted(self, physical_key):
        return physical_key in self.blacklisted_physical_keys

    def resident_tensor_bytes(self):
        return resident_tensor_bytes(self._resident_tensors)

    def mem_line(self):
        return format_mem_line(
            self.resident_tensor_bytes(), self._capacity_bytes, self._watermark)

    def verify_data_version(self, supplied_data_version_hash):
        return verify_data_version(self._canonical_hash, supplied_data_version_hash)
