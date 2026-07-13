"""Phase 38 / NET-03 — probe-local, read-only single-trajectory Brutus loader.

This is the ONE narrow data source the Phase 38 verification rungs (residual on
ground truth, single-trajectory overfit) consume. It is deliberately NOT the
Phase 39 data adapter: it implements no Step-1A gate, no splits, no batching,
and no data_version_hash (CTX-25..27).

Format contract (transcribed from ``simulation_data/Documentation/README.md``,
File Schemas / File Naming Conventions / Mandatory Parsing Rules; the v1.3-era
``pinn/`` parsers are banned as a source by CTX-17):

  * IC file (``ic_*.txt``): exactly 3 lines, one per body,
    ``m x y z vx vy vz`` in natural units (G = 1, total mass ~ 3).
  * Brutus output (``brutus_*.txt``): repeating snapshots. Each snapshot is a
    header line ``t N t_cpu`` followed by 3 body lines ``m x y z vx vy vz``,
    with a blank line between snapshots. Body lines carry 30-40 significant
    digits.
  * An OPTIONAL trailing ``Result: ...`` line. Its schema is heterogeneous
    (``eta`` and ``tol`` may be absent, the ``filename=`` may be a macOS or a
    Windows path). It is METADATA ONLY and is never used for mapping or for the
    completeness decision.
  * Completeness (mandatory rule): a trajectory is complete iff its FINAL
    parsed timestamp is >= 9.5. ``Result:`` is not trusted for this.
  * The folder defines the variant; the numeric ID (zero-padded to 4 digits)
    maps an IC file to its Brutus output. File names never encode "gold".

Read-only discipline (project governance, threat T-38-08): ``simulation_data/``
is strictly read-only. Every file here is opened in a read mode; this module
contains no directory-creating, file-writing, moving, or deleting call at all.

Precision/device discipline (CTX-14 / ENV-04): ``dtype`` and ``device`` are
mandatory explicit arguments. Tensors are built directly on them. This module
never mutates the global default dtype and never probes device availability.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import torch

__all__ = [
    "TrajectoryFixture",
    "TrajectoryPaths",
    "IncompleteTrajectoryError",
    "COMPLETENESS_MIN_FINAL_TIME",
    "VARIANTS",
    "load_trajectory",
    "resolve_trajectory_path",
    "sha256_file",
]


# ---------------------------------------------------------------------------
# Dataset conventions (README-derived; no absolute path is ever hardcoded).
# ---------------------------------------------------------------------------

# Mandatory Parsing Rule 1: completeness is decided by the final timestamp.
COMPLETENESS_MIN_FINAL_TIME = 9.5

_N_BODIES = 3
_BODY_FIELDS = 7      # m x y z vx vy vz
_HEADER_FIELDS = 3    # t N t_cpu

# variant -> (brutus folder, brutus file prefix, ic folder, ic file prefix).
# Gold status is encoded ONLY by the Brutus folder; the file prefix is the base
# one, and the gold subsets reuse the SAME base IC folder.
VARIANTS = {
    "standard_quasi_random": (
        "brutus_standard_quasi_random", "brutus_standard",
        "ic_standard_quasi_random", "ic_standard",
    ),
    "standard_quasi_random_gold_standard": (
        "brutus_standard_quasi_random_gold_standard", "brutus_standard",
        "ic_standard_quasi_random", "ic_standard",
    ),
    "hierarchical": (
        "brutus_hierarchical", "brutus_hierarchical",
        "ic_hierarchical", "ic_hierarchical",
    ),
    "hierarchical_gold_standard": (
        "brutus_hierarchical_gold_standard", "brutus_hierarchical",
        "ic_hierarchical", "ic_hierarchical",
    ),
}

_BRUTUS_SUBDIR = "brutus_output"
_IC_SUBDIR = "ic_final"

# IDs are exactly 1-4 decimal digits (zero-padded to 4 on resolution). This is
# the ONLY accepted string form: it admits no separator, no '..', no '~', no
# leading '/', so a resolved path can never escape the dataset folders.
_ID_PATTERN = re.compile(r"^[0-9]{1,4}$")
_ID_MAX = 9999


class IncompleteTrajectoryError(ValueError):
    """The trajectory's final timestamp is below the completeness threshold."""


@dataclass(frozen=True)
class TrajectoryPaths:
    """A validated variant+id resolution: the Brutus file and its paired IC."""

    variant: str
    id: str
    brutus_path: Path
    ic_path: Path


@dataclass(frozen=True)
class TrajectoryFixture:
    """One parsed Brutus trajectory on an explicit (dtype, device).

    Attributes:
        times: ``(N_t,)`` snapshot times.
        positions: ``(N_t, 3, 3)`` positions (time, body, coord) — the leading
            axis is the N_t batch axis, matching the residual/loss contract.
        velocities: ``(N_t, 3, 3)`` velocities.
        masses: ``(3,)`` ordered RAW masses (from the paired IC file when the
            trajectory was resolved by variant+id, otherwise from the Brutus
            body lines, which carry the same raw masses).
        provenance: dict with ``variant``, ``id``, ``path``, ``sha256``,
            ``ic_path``, ``ic_sha256``, ``n_snapshots``, ``final_time``,
            ``result_footer`` — enough to bind any evidence to an exact file.
    """

    times: torch.Tensor
    positions: torch.Tensor
    velocities: torch.Tensor
    masses: torch.Tensor
    provenance: dict


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

def sha256_file(path):
    """Return the hex sha256 of the file at ``path`` (streamed, read-only).

    Same provenance pattern as ``scripts/run_precision_probe.py`` ``_sha256_file``.
    """
    digest = hashlib.sha256()
    with open(Path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Path resolution — validate BEFORE constructing any path (threat T-38-10).
# ---------------------------------------------------------------------------

def _default_dataset_root():
    """``<repo>/simulation_data/Data``, derived from this file's location.

    Derived, never hardcoded: this module lives at ``<repo>/pinn/verification/``.
    """
    return Path(__file__).resolve().parents[2] / "simulation_data" / "Data"


def _validated_variant(variant):
    if not isinstance(variant, str) or variant not in VARIANTS:
        raise ValueError(
            f"unknown dataset variant {variant!r}; the known variants are "
            f"{sorted(VARIANTS)}"
        )
    return variant


def _validated_id(id_value):
    """Return the 4-digit zero-padded ID string, or raise ``ValueError``.

    Accepts an ``int`` in [0, 9999] or a string of 1-4 decimal digits. Every
    other input — a float, a bool, a negative number, an out-of-range number, a
    non-numeric string, a string with a path separator, ``..``, ``~``, or a
    leading ``/`` — is rejected HERE, before any path component is built, so no
    traversal can reach outside the dataset folders.
    """
    if isinstance(id_value, bool):
        raise ValueError(f"trajectory id must be an int or digit string; got {id_value!r}")
    if isinstance(id_value, int):
        if id_value < 0 or id_value > _ID_MAX:
            raise ValueError(
                f"trajectory id out of range: {id_value!r} (expected 0..{_ID_MAX})")
        return f"{id_value:04d}"
    if isinstance(id_value, str):
        if not _ID_PATTERN.match(id_value):
            raise ValueError(
                f"invalid trajectory id {id_value!r}: expected 1-4 decimal digits "
                f"(no separators, no '..', no absolute path)")
        return f"{int(id_value):04d}"
    raise ValueError(
        f"trajectory id must be an int or a 1-4 digit string; got {type(id_value).__name__}")


def resolve_trajectory_path(variant, id, root=None):  # noqa: A002 - dataset field name
    """Resolve ``(variant, id)`` to the Brutus file and its paired IC file.

    Both inputs are validated BEFORE any path is constructed: an unknown variant
    or a non-numeric / negative / out-of-range / separator-bearing id raises
    ``ValueError``. The folder mapping follows the dataset README (the folder
    defines the variant; the file name uses the base prefix and never encodes
    "gold"; the gold subsets reuse the base IC folder).

    Args:
        variant: one of ``VARIANTS``.
        id: an int in [0, 9999] or a 1-4 digit string.
        root: the dataset ``Data`` root (defaults to the repo's
            ``simulation_data/Data``, derived from this module's location).

    Returns:
        TrajectoryPaths
    """
    variant = _validated_variant(variant)
    id_str = _validated_id(id)
    brutus_dir, brutus_prefix, ic_dir, ic_prefix = VARIANTS[variant]
    base = Path(root) if root is not None else _default_dataset_root()
    return TrajectoryPaths(
        variant=variant,
        id=id_str,
        brutus_path=base / _BRUTUS_SUBDIR / brutus_dir / f"{brutus_prefix}_{id_str}.txt",
        ic_path=base / _IC_SUBDIR / ic_dir / f"{ic_prefix}_{id_str}.txt",
    )


# ---------------------------------------------------------------------------
# Parsing — README File Schemas. Read mode only.
# ---------------------------------------------------------------------------

def _read_lines(path):
    with open(Path(path), "r", encoding="utf-8") as handle:
        return handle.read().splitlines()


def _parse_brutus(path):
    """Parse a Brutus output file into (times, positions, velocities, masses, footer).

    Snapshots are ``t N t_cpu`` headers followed by three ``m x y z vx vy vz``
    body lines, blank-line separated. The trailing ``Result:`` line, when
    present, is captured as metadata and otherwise ignored.
    """
    times = []
    positions = []
    velocities = []
    masses = None
    footer = None
    current_pos = None
    current_vel = None
    current_mass = None

    for lineno, raw in enumerate(_read_lines(path), start=1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("Result:"):
            footer = line
            continue
        parts = line.split()
        if len(parts) == _HEADER_FIELDS:
            if current_pos is not None and len(current_pos) != _N_BODIES:
                raise ValueError(
                    f"{path}: snapshot ending at line {lineno} has "
                    f"{len(current_pos)} body lines (expected {_N_BODIES})")
            times.append(float(parts[0]))
            current_pos = []
            current_vel = []
            current_mass = []
            positions.append(current_pos)
            velocities.append(current_vel)
            if masses is None:
                masses = current_mass
        elif len(parts) == _BODY_FIELDS:
            if current_pos is None:
                raise ValueError(
                    f"{path}: body line {lineno} precedes any snapshot header")
            values = [float(v) for v in parts]
            current_mass.append(values[0])
            current_pos.append(values[1:4])
            current_vel.append(values[4:7])
        else:
            raise ValueError(
                f"{path}: line {lineno} has {len(parts)} fields "
                f"(expected {_HEADER_FIELDS} header or {_BODY_FIELDS} body fields)")

    if not times:
        raise ValueError(f"{path}: no snapshots parsed")
    for index, snapshot in enumerate(positions):
        if len(snapshot) != _N_BODIES:
            raise ValueError(
                f"{path}: snapshot {index} has {len(snapshot)} body lines "
                f"(expected {_N_BODIES})")
    return times, positions, velocities, masses, footer


def _parse_ic(path):
    """Parse a 3-line IC file into (masses, positions, velocities)."""
    rows = [line.split() for line in _read_lines(path) if line.strip()]
    if len(rows) != _N_BODIES:
        raise ValueError(
            f"{path}: IC file has {len(rows)} body lines (expected {_N_BODIES})")
    masses, positions, velocities = [], [], []
    for lineno, parts in enumerate(rows, start=1):
        if len(parts) != _BODY_FIELDS:
            raise ValueError(
                f"{path}: IC line {lineno} has {len(parts)} fields "
                f"(expected {_BODY_FIELDS})")
        values = [float(v) for v in parts]
        masses.append(values[0])
        positions.append(values[1:4])
        velocities.append(values[4:7])
    return masses, positions, velocities


# ---------------------------------------------------------------------------
# Public loader
# ---------------------------------------------------------------------------

def load_trajectory(*, path=None, variant=None, id=None, dtype, device,  # noqa: A002
                    root=None):
    """Load exactly one Brutus trajectory, read-only, with provenance.

    Exactly one invocation form is required: either an explicit ``path`` (the
    Brutus output file) OR a ``variant`` + ``id`` pair resolved through
    ``resolve_trajectory_path``. Supplying both, or neither, or half of the
    variant+id pair, raises ``ValueError``. No absolute path is hardcoded.

    The completeness gate (final timestamp >= 9.5) is applied after parsing and
    raises ``IncompleteTrajectoryError``; the ``Result:`` footer is retained as
    metadata only and never rescues a truncated file.

    Args:
        path: a Brutus output file path (the ``path=`` form).
        variant: one of ``VARIANTS`` (the ``variant=`` + ``id=`` form).
        id: an int in [0, 9999] or a 1-4 digit string.
        dtype: the resolved Torch dtype (explicit; no default).
        device: the resolved Torch device (explicit; no availability probe).
        root: dataset ``Data`` root override (used by the variant+id form).

    Returns:
        TrajectoryFixture with ``(N_t,)`` times, ``(N_t, 3, 3)`` positions and
        velocities, ``(3,)`` raw masses, and a provenance dict.
    """
    by_path = path is not None
    by_variant = variant is not None or id is not None
    if by_path and by_variant:
        raise ValueError(
            "load_trajectory takes EITHER path= OR variant=+id=, not both")
    if not by_path and not by_variant:
        raise ValueError("load_trajectory requires path= or variant=+id=")

    ic_path = None
    if by_variant:
        if variant is None or id is None:
            raise ValueError(
                "the variant+id form requires BOTH variant= and id=; got "
                f"variant={variant!r}, id={id!r}")
        resolved = resolve_trajectory_path(variant, id, root=root)
        brutus_path = resolved.brutus_path
        ic_path = resolved.ic_path
        variant_name, id_str = resolved.variant, resolved.id
    else:
        brutus_path = Path(path)
        variant_name, id_str = None, None

    times, positions, velocities, brutus_masses, footer = _parse_brutus(brutus_path)

    final_time = times[-1]
    if final_time < COMPLETENESS_MIN_FINAL_TIME:
        raise IncompleteTrajectoryError(
            f"{brutus_path}: incomplete trajectory — final timestamp "
            f"{final_time!r} < {COMPLETENESS_MIN_FINAL_TIME} "
            f"(README mandatory completeness rule; the Result: footer is not trusted)")

    ic_sha = None
    masses = brutus_masses
    if ic_path is not None:
        ic_masses, _ic_pos, _ic_vel = _parse_ic(ic_path)
        masses = ic_masses  # the paired IC file is the raw-mass source of record
        ic_sha = sha256_file(ic_path)

    provenance = {
        "variant": variant_name,
        "id": id_str,
        "path": str(brutus_path),
        "sha256": sha256_file(brutus_path),
        "ic_path": str(ic_path) if ic_path is not None else None,
        "ic_sha256": ic_sha,
        "n_snapshots": len(times),
        "final_time": final_time,
        "result_footer": footer,
    }

    return TrajectoryFixture(
        times=torch.tensor(times, dtype=dtype, device=device),
        positions=torch.tensor(positions, dtype=dtype, device=device),
        velocities=torch.tensor(velocities, dtype=dtype, device=device),
        masses=torch.tensor(masses, dtype=dtype, device=device),
        provenance=provenance,
    )
