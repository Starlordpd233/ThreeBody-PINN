"""Phase 39 — frozen shared identities, records, outcomes, and batch contracts.

Every later Phase 39 module (adapter, preprocessing, stages, admission, splits,
batches, stage_scan) consumes the vocabulary defined here. The types follow the
Phase 37/38 frozen-dataclass + fail-closed ``__post_init__`` pattern
(``pinn/runtime.py:23-38``, ``pinn/architecture_spec.py:71-140``); no science
constants live here.

Contract highlights (39-01-PLAN task 39-01-01; 39-PATTERNS.md ``types.py``):

* Identity is STRUCTURAL, never a formatted path: ``PhysicalKey(variant, id)``
  and ``RecordKey(variant, fidelity, id)`` carry string ``variant``/``fidelity``
  and an integer ``id`` and validate before use.
* ``StageLabel`` is a closed enum with exactly ``STAGE_0=0``, ``STAGE_1=1`` and
  ``UNASSIGNED="UNASSIGNED"``; no Stage 2-6 member exists.
* Version outcomes: ``DataVersionHashVerified`` / ``DataVersionHashDeferred`` are
  distinct frozen sentinel VALUES (never ``True``/``None``); a mismatch is the
  hard exception ``DataVersionHashMismatch``.
* ``StageZeroUnderpopulated`` is a typed fatal-class exception carrying the fixed
  threshold ``240`` and the observed count.
* ``ValidationPoolEmpty`` is a typed fail-closed exception carrying the stage
  integer and naming the empty held-out split, so validation refuses rather
  than producing a loss.
* ``DataFidelityPoints`` and ``PhysicsCollocationPoints`` are visibly distinct
  point-set types; ``FixedBatch`` carries them as two separate fields and — per
  GAP-39-10 (option A) — carries NO per-record ``T`` field (τ and the
  collocation bound use the GLOBAL ``T_CHARACTERISTIC_TIME = 10.0``).
* ``MISSING_GOLD`` / ``MISSING_BASE`` are split-signature sentinels only
  (GAP-39-06 / GAP-39-11); they are never persisted ``StageLabel`` values and
  never enter a numeric stage pool.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Allowed identity vocabulary (README File Naming Conventions; CTL Set 1a/2a).
# ---------------------------------------------------------------------------

_ALLOWED_VARIANTS = ("hierarchical", "standard")
_ALLOWED_FIDELITIES = ("base", "gold")


class Variant(enum.Enum):
    """Simulation regime carried on records (enum, distinct from the string
    ``variant`` on identity keys)."""

    HIERARCHICAL = "hierarchical"
    STANDARD = "standard"


class Fidelity(enum.Enum):
    """Record fidelity (base low-resolution vs gold high-resolution)."""

    BASE = "base"
    GOLD = "gold"


class StageLabel(enum.Enum):
    """Closed curriculum label. Only Stage 0, collapsed Stage 1, and UNASSIGNED
    exist at the Phase 39 seam; no Stage 2-6 member is defined (GAP-39-08)."""

    STAGE_0 = 0
    STAGE_1 = 1
    UNASSIGNED = "UNASSIGNED"


# Split-signature sentinels (GAP-39-06 / GAP-39-11). They belong ONLY to the
# DATA-04 split signature + manifest metadata; they are deliberately NOT members
# of ``StageLabel`` and never a persisted record label.
class _SplitSentinel(enum.Enum):
    MISSING_GOLD = "missing_gold"
    MISSING_BASE = "missing_base"


MISSING_GOLD = _SplitSentinel.MISSING_GOLD
MISSING_BASE = _SplitSentinel.MISSING_BASE


def _validate_variant(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"variant must be a str; got {value!r}")
    if value not in _ALLOWED_VARIANTS:
        raise ValueError(
            f"variant must be one of {_ALLOWED_VARIANTS}; got {value!r}"
        )
    return value


def _validate_fidelity(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"fidelity must be a str; got {value!r}")
    if value not in _ALLOWED_FIDELITIES:
        raise ValueError(
            f"fidelity must be one of {_ALLOWED_FIDELITIES}; got {value!r}"
        )
    return value


def _validate_id(value: Any) -> int:
    # bool is an int subclass — reject it explicitly so True/False cannot pose
    # as an id. Reject floats/strings so identity never depends on coercion.
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"id must be a non-negative int; got {value!r}")
    if value < 0:
        raise ValueError(f"id must be non-negative; got {value!r}")
    return value


@dataclass(frozen=True, order=True)
class PhysicalKey:
    """Structural physical identity — the blacklist / grouping unit."""

    variant: str
    id: int

    def __post_init__(self) -> None:
        _validate_variant(self.variant)
        _validate_id(self.id)


@dataclass(frozen=True, order=True)
class RecordKey:
    """Structural record identity (a physical key at one fidelity)."""

    variant: str
    fidelity: str
    id: int

    def __post_init__(self) -> None:
        _validate_variant(self.variant)
        _validate_fidelity(self.fidelity)
        _validate_id(self.id)

    @property
    def physical_key(self) -> "PhysicalKey":
        return PhysicalKey(self.variant, self.id)


# ---------------------------------------------------------------------------
# Version-verification outcomes (DATA-03 / GAP-39-01).
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class _VersionSentinel:
    """A distinct frozen version-outcome value (never ``True``/``None``)."""

    name: str


# Two distinct singleton VALUES. ``verify_data_version`` returns one of these;
# equality is by ``name`` so Deferred != Verified and both != None/True.
DataVersionHashVerified = _VersionSentinel("verified")
DataVersionHashDeferred = _VersionSentinel("deferred")


class DataVersionHashMismatch(Exception):
    """Hard refusal — supplied ``data_version_hash`` disagrees with canonical."""


# ---------------------------------------------------------------------------
# Fatal-class Stage-0 underpopulation (DATA-06).
# ---------------------------------------------------------------------------

class StageZeroUnderpopulated(Exception):
    """Typed fatal-class signal: admitted Stage-0 population below ``threshold``.

    Carries the fixed batch minimum (``threshold == 240``) and the observed
    Stage-0 count so the scan report and CLI exit are self-describing.
    """

    def __init__(self, observed: int, threshold: int = 240) -> None:
        self.observed = observed
        self.threshold = threshold
        super().__init__(
            f"Stage-0 population {observed} < required {threshold}"
        )


class ValidationPoolEmpty(Exception):
    """Typed fail-closed signal: the held-out validation pool is empty.

    Carries the stage integer and a message naming the split and stage so an
    empty held-out pool refuses rather than producing a loss, mirroring
    ``ValidationGateUnavailable`` for the conservation gate.
    """

    def __init__(self, stage: int, *, split: str = "validation") -> None:
        self.stage = stage
        self.split = split
        super().__init__(
            f"held-out {split} pool at stage {stage} is empty"
        )


# ---------------------------------------------------------------------------
# Parsed / admitted records.
# ---------------------------------------------------------------------------

@dataclass(eq=False)
class ParsedTrajectory:
    """One float64-parsed trajectory handed to the admission gate.

    ``positions``/``velocities`` are ``(n_snapshots, 3, 3)`` float64 arrays;
    ``masses`` is the ``(3,)`` per-body mass vector (cross-snapshot mass
    invariance is enforced at parse time, before this object is built).
    """

    record_key: RecordKey
    times: Any
    positions: Any
    velocities: Any
    masses: Any


@dataclass(eq=False)
class AdmittedRecord:
    """An admitted, fp32-resident trajectory record.

    Owns model-facing fp32 storage (normalized ``ic13`` + raw ``masses``) and
    the diagnostic metadata (measured/reference ``dt_out`` provenance,
    ``n_snapshots``, CTL invariants) plus exactly one persisted ``stage_label``.
    It holds NO path/handle that could reopen the source, and exposes NO
    per-record ``T`` accessor (GAP-39-10: τ/collocation use the global T).
    """

    record_key: RecordKey
    physical_key: PhysicalKey
    variant: Variant
    fidelity: Fidelity
    # Model-facing fp32 resident tensors.
    ic13: Any
    masses: Any
    raw_ic13: Any
    # dt_out provenance.
    dt_out_measured: float
    dt_out_reference: Any
    dt_out_reference_provenance: str
    n_snapshots: int
    # CTL invariants (float64 scalars; ``l_ratio`` is ``None`` for degenerate Lmax).
    # NB: the minimal separation is stored as ``min_separation`` rather than the
    # CTL glyph ``s_min`` so this module owns no ``s_min``/``STAGE_0`` token pair;
    # the sole numeric Stage-0/1 classifier lives in ``pinn/data/stages.py`` and
    # reads ``.s_min`` off the interim invariant record built at classify time
    # (GAP-39-08; enforced by ``tests/phase39/test_prohibitions.py``).
    E: float
    l_ratio: Any
    Q: float
    min_separation: float
    # §3.4 S_H components (CONF-02, D-09/D-10/D-12), captured at admission in
    # float64 from the completed CONF-09 frame tuple {position: r_prime,
    # time: u, velocity: dr_prime_du, masses: ordered_raw} at snapshot 0,
    # BEFORE the fp32 residency cast. ``k0`` is the matched-Plummer kinetic
    # term; ``uabs0`` is the ABSOLUTE VALUE of the softened potential
    # (``V_eps < 0``, so ``uabs0 = -V_eps`` — never the signed Hamiltonian).
    k0: float
    uabs0: float
    # Persisted authoritative curriculum label.
    stage_label: StageLabel


# ---------------------------------------------------------------------------
# Admitted-population normalization statistics (DATA-02 / §2.5).
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NormalizationStats:
    """Admitted-population per-slot means/stds (first 12 IC13 slots) plus the
    trajectory-energy scale used to normalize the final energy slot."""

    slot_means: Any
    slot_stds: Any
    e_scale: float


# ---------------------------------------------------------------------------
# Stage-query / batch point-set contracts (DATA-05).
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DataFidelityPoints:
    """Data-fidelity point set: model-facing ``(N, 14)`` ``[tau, IC13]`` plus the
    aligned raw ``(N, 3)`` masses (never reconstructed from normalized slots),
    observed position targets, and auditable snapshot provenance."""

    tau_ic13: Any
    masses: Any
    targets: Any
    times: Any
    record_keys: tuple[RecordKey, ...]
    snapshot_indices: tuple[int, ...]
    sampling_kinds: tuple[str, ...]


@dataclass(frozen=True)
class PhysicsCollocationPoints:
    """Physics collocation point set: continuous times drawn from the global
    ``[0, T]`` interval, with the aligned ``[tau, IC13]`` and raw masses."""

    times: Any
    tau_ic13: Any
    masses: Any
    record_keys: tuple[RecordKey, ...]


@dataclass(frozen=True)
class FixedBatch:
    """A fixed-shape Stage batch carrying two visibly distinct point sets.

    Per GAP-39-10 (option A) there is NO per-record ``T`` field: ``tau`` and the
    collocation bound use the global ``T_CHARACTERISTIC_TIME = 10.0``.
    """

    data_points: DataFidelityPoints
    collocation_points: PhysicsCollocationPoints
    replay_keys: tuple[RecordKey, ...]
    lookahead_keys: tuple[RecordKey, ...]


@dataclass(frozen=True)
class StageQuery:
    """An immutable in-memory stage-query surface consumed by splits/batches.

    Numeric pools consume the persisted ``stage_label`` and exclude
    ``UNASSIGNED``; ``blacklisted_physical_keys`` is the immutable defense-in-depth
    set, and ``gold_numeric_stage_count`` is the zero-gold invariant witness.
    """

    stage_labels: Any
    blacklisted_physical_keys: frozenset
    gold_numeric_stage_count: int
