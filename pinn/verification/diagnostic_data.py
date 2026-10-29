"""Phase 65 (INST-08 d, D-09): the diagnostic Stage-0 training data boundary.

One guarded corpus seam for the Phase 65 probe and fit. Every target and
ancillary corpus operation — ``read``, ``exists`` or any path resolution —
first requires the record's orbit to sit in the **training split at manifest
stage 0**. Validation, test, later-stage, UNASSIGNED and unknown keys are
refused before anything is opened; an invalid ancillary (score or beside) key
blocks an otherwise valid target because all three assigned keys are
validated as a set before the first read.

Stage semantics (the orbit reading, grounded in INST-08 and D-09). The split
manifest schema requires every gold record's own stage label to be
``UNASSIGNED`` (``pinn/data/splits.py`` refuses a gold record with a numeric
stage), so a record-level stage check would refuse every gold key forever.
The requirement text resolves this: INST-08 trains "on one Stage-0 training
orbit's gold record", so "Stage-0 training record" means a record of an orbit
whose manifest stage (its base record's stage, the group signature's
``base_stage``) is 0 and whose split is ``train``. The base and gold records
of such an orbit are both admissible; standard-variant orbits (base stage
``UNASSIGNED``) and stage-1 orbits are not. Both stage readings — the orbit's
and the record's own — are recorded on every open.

Manifest and blacklist metadata reads (the inherited constructor, split
lookups and ``manifest_stage``) remain identified metadata operations; this
permission never extends to trajectory records. ``pinn/verification/
split_allowlist.py`` and ``pinn/verification/learnability_data.py`` are
pinned and are never modified here; the guarded reader subclasses the one and
delegates to the other.

The retained IC13 normalizer is hydrated directly from the Phase 59
reader-acceptance evidence (research A3): the evidence file is hashed before
parsing, its digest is checked against the committed Phase 59 manifest entry,
and ``stats_digest`` of the hydrated statistics must agree with both the
recorded ``stats_sha256`` and ``EXPECTED_STATS_SHA256`` before any data
access. No monitor recovery, Stage-1 read or normalizer refit ever runs —
``open_real_context``, ``recover_normalizer_from_checkpoint`` and
``fallback_normalizer_from_allowlist`` stay uncalled, because the historical
helper would recover 256 monitor identities (240 Stage 0 + 16 Stage 1) and
Stage 1 is outside this phase's read authority. Fitting a permitted subset
instead of using the recorded full statistics would change the model's input
contract, so a substituted subset halts.

Physical windows are exact: ``0 <= t <= window_length`` in float64, with the
upper endpoint included, everything above it excluded, timestamps distinct
and strictly increasing, and at least two retained samples. ``tau`` is
computed with the locked ``T_CHARACTERISTIC_TIME``, never rescaled to the
shorter window; physical time and tau are recorded separately.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.types import NormalizationStats, RecordKey
from pinn.verification import evidence_io, split_allowlist
from pinn.verification.learnability_arms import fixture_arm
from pinn.verification.learnability_data import (
    ArmData,
    DataContext,
    EXPECTED_STATS_SHA256,
    HarnessHalt,
    RecordView,
)
from pinn.verification.production_reference import (
    load_reference,
    resident_record,
    stats_digest,
)
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    AllowlistedCorpusReader,
    SplitAllowlist,
    SplitRefused,
    expected_splits_sha256,
    install_open_attestation,
    resolve_data_root,
)

__all__ = [
    "Stage0TrainingRefused",
    "Stage0TrainingReader",
    "DiagnosticDataRefused",
    "DiagnosticContext",
    "READER_ACCEPTANCE_REL",
    "orbit_stage",
    "require_stage0_training",
    "load_recorded_stats",
    "open_diagnostic_context",
    "load_diagnostic_data",
    "one_orbit_spec",
    "validate_window",
    "physical_window",
]

_REPO_ROOT = Path(__file__).resolve().parents[2]
READER_ACCEPTANCE_REL = Path(
    ".planning/phases/59-read-only-baseline-scorecard/evidence/"
    "audit/reader_acceptance.json"
)
_READER_ACCEPTANCE_MANIFEST_REL = Path(
    ".planning/phases/59-read-only-baseline-scorecard/evidence/manifest.json"
)
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class Stage0TrainingRefused(SplitRefused):
    """A key is outside the diagnostic Stage-0 training boundary.

    Raised before any reader operation, ``exists`` call or corpus path is
    touched. Subclasses :class:`SplitRefused` so existing refusal handling
    and the open-attestation semantics keep working.
    """


def orbit_stage(allowlist, key):
    """The manifest stage of the key's physical orbit (its base record's stage).

    ``key`` may be a ``RecordKey`` or ``PhysicalKey``. The group signature's
    ``base_stage`` is the orbit's stage, independent of record ordering; it is
    ``0``, ``1``, ``"UNASSIGNED"``, or the ``MISSING_BASE`` sentinel for a
    gold-only group (which is refused by callers, never admitted).
    """
    physical = key.physical_key if isinstance(key, RecordKey) else key
    for group in allowlist.manifest.groups:
        if group.physical_key != physical:
            continue
        return group.signature[1]
    raise Stage0TrainingRefused(
        f"refused before any path is built: orbit {physical.variant} id {physical.id} "
        "is not in the split manifest"
    )


def _stage_label(stage):
    if isinstance(stage, str):
        return stage
    return repr(stage)


def require_stage0_training(allowlist, key):
    """Admit one key to the diagnostic boundary: train split, orbit stage 0.

    Returns a report mapping with the key's ``split``, the orbit's manifest
    ``stage`` (always ``0`` here) and the record's own ``record_stage``.
    Anything else — validation or test split, withheld or unknown key, a
    stage-1 or UNASSIGNED orbit, or a non-``RecordKey`` — refuses before any
    path is built.
    """
    if not isinstance(key, RecordKey):
        raise TypeError(f"a diagnostic record must be a RecordKey; got {key!r}")
    split = allowlist.require(key)  # SplitRefused (withheld/unknown) before any path
    if split != "train":
        raise Stage0TrainingRefused(
            f"refused before any path is built: diagnostic access is Stage-0 "
            f"training only; {evidence_io.record_key_str(key)} is in the {split} split"
        )
    stage = orbit_stage(allowlist, key)
    if not (isinstance(stage, int) and not isinstance(stage, bool) and stage == 0):
        raise Stage0TrainingRefused(
            f"refused before any path is built: diagnostic access is Stage-0 "
            f"training only; orbit {key.variant} id {key.id} has manifest stage "
            f"{_stage_label(stage)}"
        )
    return {
        "split": split,
        "stage": 0,
        "record_stage": allowlist.manifest_stage(key),
    }


class Stage0TrainingReader(AllowlistedCorpusReader):
    """An allowlisted reader whose every operation first requires Stage-0 TRAIN.

    Admission (train split plus orbit stage 0, D-09) runs before ``read``,
    ``exists`` and any corpus path resolution, for target and ancillary keys
    alike, and each admitted key is re-checked on every later operation.
    Actual opens are recorded with their split and both stage readings;
    refusals are counted before any open. The class stays an
    ``AllowlistedCorpusReader`` so ``production_reference.load_reference``'s
    type check accepts it and the existing preprocessing chain is unchanged.
    """

    def __init__(self, *, allowlist, data_root, data_root_source, blacklist_path=None):
        super().__init__(
            allowlist=allowlist,
            data_root=data_root,
            data_root_source=data_root_source,
            blacklist_path=blacklist_path,
        )
        self._stage0_requested = []
        self._stage0_opened = []
        self._stage0_refusals = 0

    def _admit(self, key):
        try:
            return require_stage0_training(self.allowlist, key)
        except SplitRefused:
            self._stage0_refusals += 1
            # Mirror the parent's bookkeeping for refusals raised at this
            # stronger boundary: the process attestation also counts them as
            # refused before open (its hook is never installed here).
            attestation = split_allowlist._ATTESTATION
            if attestation is not None:
                attestation.refused_before_open += 1
            raise

    def _brutus_path(self, key):
        self._admit(key)
        return super()._brutus_path(key)

    def exists(self, key):
        if not isinstance(key, RecordKey):
            raise TypeError(f"exists() requires a RecordKey; got {key!r}")
        report = self._admit(key)
        self._stage0_requested.append(
            {
                "record_key": evidence_io.record_key_str(key),
                "split": report["split"],
                "stage": report["stage"],
                "record_stage": report["record_stage"],
            }
        )
        return super().exists(key)

    def read(self, key):
        if not isinstance(key, RecordKey):
            raise TypeError(f"read() requires a RecordKey; got {key!r}")
        report = self._admit(key)
        self._stage0_requested.append(
            {
                "record_key": evidence_io.record_key_str(key),
                "split": report["split"],
                "stage": report["stage"],
                "record_stage": report["record_stage"],
            }
        )
        admitted = super().read(key)
        self._stage0_opened.append(
            {
                "record_key": evidence_io.record_key_str(key),
                "split": admitted.split,
                "stage": report["stage"],
                "record_stage": report["record_stage"],
            }
        )
        return admitted

    def access_summary(self):
        """The diagnostic read audit: requested and opened keys, refusal count."""
        return {
            "requested": tuple(dict(entry) for entry in self._stage0_requested),
            "opened": tuple(dict(entry) for entry in self._stage0_opened),
            "refused_before_open": self._stage0_refusals,
            "actual_opens": len(self._stage0_opened),
        }


def _assignment(spec):
    return (
        ("train", spec.train_key),
        ("score", spec.score_key),
        ("beside", spec.beside_key),
    )


class DiagnosticDataRefused(RuntimeError):
    """The retained statistics or the requested window fail their contract."""


def _committed_reader_acceptance_sha256(root):
    path = root / _READER_ACCEPTANCE_MANIFEST_REL
    if not path.is_file():
        raise DiagnosticDataRefused("the Phase 59 evidence manifest is missing")
    try:
        manifest = json.loads(path.read_bytes().decode("utf-8"))
        entry = manifest["files"]["audit/reader_acceptance.json"]
        digest = entry["sha256"]
    except (UnicodeDecodeError, ValueError, KeyError, TypeError) as exc:
        raise DiagnosticDataRefused(
            f"the Phase 59 evidence manifest has no readable reader-acceptance entry: {exc}"
        ) from exc
    if not isinstance(digest, str) or _HEX64.fullmatch(digest) is None:
        raise DiagnosticDataRefused(
            "the committed reader-acceptance sha256 is not 64 lowercase hex"
        )
    return digest


def _recorded_block(payload):
    block = payload.get("normalizer") if isinstance(payload, dict) else None
    if not isinstance(block, dict):
        raise DiagnosticDataRefused("the reader-acceptance evidence has no normalizer block")
    return block


def _recorded_floats(block, name):
    values = block.get(name)
    if not isinstance(values, list) or len(values) != 12:
        raise DiagnosticDataRefused(
            f"recorded {name} must be a list of exactly 12 numbers; "
            f"a substituted subset or a padded set halts"
        )
    out = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise DiagnosticDataRefused(f"recorded {name} must hold numbers only")
        number = float(value)
        if not math.isfinite(number):
            raise DiagnosticDataRefused(f"recorded {name} must be finite")
        out.append(number)
    return np.asarray(out, dtype=np.float64)


def load_recorded_stats(repo_root):
    """Hydrate the retained IC13 normalizer from the Phase 59 reader acceptance.

    The evidence file is hashed before parsing and its digest must equal the
    committed Phase 59 manifest entry, so changed evidence halts before any
    statistics are trusted. The hydrated statistics must reproduce the
    recorded ``stats_sha256`` and ``EXPECTED_STATS_SHA256`` exactly; zero
    standard deviations, non-finite entries and substituted subsets halt. No
    corpus record is read and no recovery or refit entry is invoked.
    """
    root = Path(repo_root)
    evidence_path = root / READER_ACCEPTANCE_REL
    if not evidence_path.is_file():
        raise DiagnosticDataRefused("the Phase 59 reader-acceptance evidence is missing")
    raw = evidence_path.read_bytes()
    evidence_sha256 = hashlib.sha256(raw).hexdigest()
    committed = _committed_reader_acceptance_sha256(root)
    if evidence_sha256 != committed:
        raise DiagnosticDataRefused(
            f"reader-acceptance evidence sha256 {evidence_sha256} != committed {committed}"
        )
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise DiagnosticDataRefused(
            f"the reader-acceptance evidence is not readable JSON: {exc}"
        ) from exc
    block = _recorded_block(payload)
    means = _recorded_floats(block, "slot_means")
    stds = _recorded_floats(block, "slot_stds")
    if bool(np.any(stds == 0.0)):
        raise DiagnosticDataRefused("recorded slot_stds include a zero standard deviation")
    e_scale_raw = block.get("e_scale")
    if isinstance(e_scale_raw, bool) or not isinstance(e_scale_raw, (int, float)) \
            or not math.isfinite(float(e_scale_raw)) or float(e_scale_raw) == 0.0:
        raise DiagnosticDataRefused("recorded e_scale must be a finite non-zero number")
    recorded_digest = block.get("stats_sha256")
    if not isinstance(recorded_digest, str) or _HEX64.fullmatch(recorded_digest) is None:
        raise DiagnosticDataRefused("recorded stats_sha256 must be 64 lowercase hex")
    stats = NormalizationStats(
        slot_means=means, slot_stds=stds, e_scale=float(e_scale_raw)
    )
    produced = stats_digest(stats)
    if produced != recorded_digest or recorded_digest != EXPECTED_STATS_SHA256:
        raise DiagnosticDataRefused(
            f"hydrated stats digest {produced} != recorded {recorded_digest} "
            f"or pinned {EXPECTED_STATS_SHA256}"
        )
    return SimpleNamespace(
        stats=stats,
        evidence_path=READER_ACCEPTANCE_REL.as_posix(),
        evidence_sha256=evidence_sha256,
        stats_sha256=produced,
        source="phase59-reader-acceptance",
    )


@dataclass(frozen=True)
class DiagnosticContext(DataContext):
    """A guarded ``DataContext`` plus the registration the record cites."""

    normalizer_evidence_path: str = ""
    normalizer_evidence_sha256: str = ""
    splits_sha256: str = ""


def open_diagnostic_context(*, repo_root=None):
    """Open the guarded diagnostic context from committed metadata only.

    Loads the hash-checked generation-7 split manifest, installs the process
    open attestation (the second, independent test-split check), builds the
    Stage-0 reader and hydrates the recorded normalizer from the Phase 59
    reader-acceptance evidence. No corpus record is opened, and no monitor
    recovery, Stage-1 read or normalizer refit runs.
    """
    root = _REPO_ROOT if repo_root is None else Path(repo_root)
    allowlist = SplitAllowlist.from_manifest(
        root / GENERATION7_SPLITS_REL,
        expected_sha256=expected_splits_sha256(root),
    )
    data_root, source = resolve_data_root(None)
    attestation = install_open_attestation(
        data_root=data_root,
        data_root_source=source,
        withheld_basenames=allowlist.withheld_basenames(),
        split_by_basename=allowlist.split_by_basename(),
    )
    reader = Stage0TrainingReader(
        allowlist=allowlist, data_root=data_root, data_root_source=source
    )
    recorded = load_recorded_stats(root)
    return DiagnosticContext(
        allowlist=allowlist,
        reader=reader,
        attestation=attestation,
        stats=recorded.stats,
        stats_sha256=recorded.stats_sha256,
        normalizer_source=f"{recorded.source}:{recorded.evidence_path}",
        run_kind="diagnostic",
        data_root_source=source,
        normalizer_evidence_path=recorded.evidence_path,
        normalizer_evidence_sha256=recorded.evidence_sha256,
        splits_sha256=allowlist.manifest_sha256,
    )


def validate_window(window_length):
    """Refuse window lengths outside ``(0, T_CHARACTERISTIC_TIME]``."""
    if isinstance(window_length, bool) or not isinstance(window_length, (int, float)):
        raise DiagnosticDataRefused(
            f"window length must be a real number; got {window_length!r}"
        )
    value = float(window_length)
    if not math.isfinite(value):
        raise DiagnosticDataRefused(f"window length must be finite; got {value!r}")
    if not 0.0 < value <= float(T_CHARACTERISTIC_TIME):
        raise DiagnosticDataRefused(
            f"window length must lie in (0, {float(T_CHARACTERISTIC_TIME)}]; got {value!r}"
        )
    return value


def physical_window(times, window_length):
    """The exact physical-time mask ``0 <= t <= window_length``.

    Timestamps must be finite, distinct and strictly increasing; a duplicate
    or touching boundary never duplicates a sample because the mask is a
    pure comparison against each recorded time.
    """
    window = validate_window(window_length)
    t = np.asarray(times, dtype=np.float64).reshape(-1)
    if t.size == 0 or not bool(np.all(np.isfinite(t))):
        raise DiagnosticDataRefused("record times are empty or non-finite")
    if t.size > 1 and not bool(np.all(np.diff(t) > 0.0)):
        raise DiagnosticDataRefused("record times must be distinct and strictly increasing")
    return (t >= 0.0) & (t <= window)


def _windowed_view(reference, window):
    times = np.asarray(reference.times, dtype=np.float64).reshape(-1)
    mask = physical_window(times, window)
    if int(mask.sum()) < 2:
        raise DiagnosticDataRefused(
            f"the {reference.record_key.fidelity} record has {int(mask.sum())} sample(s) "
            f"within [0, {window}]; at least two are needed"
        )
    view = RecordView(
        grid=reference.record_key.fidelity,
        times=times[mask],
        positions=np.asarray(reference.positions, dtype=np.float64)[mask],
        inner_pair=tuple(int(index) for index in reference.inner_pair),
        masses=np.asarray(reference.masses, dtype=np.float64).reshape(3),
    )
    return view, mask


def _diagnostic_summary(key, reference, view, mask, window):
    digest = hashlib.sha256()
    digest.update(np.ascontiguousarray(view.times, dtype=np.float64).tobytes())
    digest.update(np.ascontiguousarray(view.positions, dtype=np.float64).tobytes())
    return {
        "record_key": evidence_io.record_key_str(key),
        "split": str(reference.split),
        "n_snapshots": int(reference.n_snapshots),
        "n_within_window": int(view.times.shape[0]),
        "requested_window": [0.0, float(window)],
        "retained_indices": [int(index) for index in np.flatnonzero(mask)],
        "windowed_sha256": digest.hexdigest(),
    }


_DEFAULT_WINDOW = object()  # distinguishes "omitted" from an explicit window value


def load_diagnostic_data(spec, context, *, scorecard, dtype, device, window_length=_DEFAULT_WINDOW):
    """Load one diagnostic orbit through the Stage-0 boundary and an exact window.

    All three assigned keys (train, score, beside) are validated as a set
    before the first record is read, so an invalid ancillary key blocks an
    otherwise valid target with nothing opened; every later read is guarded
    again by the Stage-0 reader. Training and scoring arrays are sliced by
    the same exact physical-time mask ``0 <= t <= window_length`` (the
    scored horizon when ``window_length`` is omitted; an explicit value,
    including ``None``, is validated and a non-real number refuses),
    ``tau`` is computed with the locked ``T_CHARACTERISTIC_TIME``, and the
    production preprocessing chain (residency, raw masses, IC13, body
    permutation) is reused unchanged through ``resident_record``. The
    one-orbit gold fit passes :func:`one_orbit_spec`, so a single record
    serves all three roles and no base record is opened.
    """
    if window_length is _DEFAULT_WINDOW:
        window_length = float(scorecard.section("scoring_grid")["t_max"])
    window = validate_window(window_length)
    for _role, key in _assignment(spec):
        require_stage0_training(context.allowlist, key)
    references = {}
    for _role, key in _assignment(spec):
        if key not in references:
            references[key] = load_reference(context.reader, key)
    train = references[spec.train_key]
    for name, key in _assignment(spec)[1:]:
        other = references[key]
        if not np.array_equal(other.raw_ic13, train.raw_ic13):
            raise HarnessHalt(
                f"raw IC13 of the {name} record {evidence_io.record_key_str(key)} differs "
                f"from the train record {evidence_io.record_key_str(spec.train_key)}"
            )
        if not np.array_equal(np.asarray(other.permutation), np.asarray(train.permutation)):
            raise HarnessHalt(
                f"body order of the {name} record {evidence_io.record_key_str(key)} differs "
                f"from the train record {evidence_io.record_key_str(spec.train_key)}"
            )
    keep = physical_window(train.times, window)
    count = int(keep.sum())
    if count < 2:
        raise DiagnosticDataRefused(
            f"the train record has {count} sample(s) within [0, {window}]; "
            "at least two distinct samples are needed"
        )
    resident = resident_record(train, context.stats)
    # Two time grids, both intentional. The training tensor keeps the existing
    # residency cast (float32 snapshot times), so tau_ic13 stays bitwise the
    # load_arm_data seam. The recorded physical grid is the exact float64
    # record grid, the same array the score and beside views carry, so the
    # record's target-window rows, scores and comparisons share one ordered
    # time grid (E-INST-adjacency).
    physical_times = np.asarray(train.times, dtype=np.float64).reshape(-1)[keep]
    times = resident.snapshot_times.numpy().astype(np.float64)[keep]
    targets = resident.snapshot_positions.numpy()[keep]
    ic13 = resident.ic13.numpy().astype(np.float64)
    times_t = torch.as_tensor(times, dtype=dtype, device=device)
    tau = 2.0 * (times_t / T_CHARACTERISTIC_TIME) - 1.0
    ic13_rows = torch.as_tensor(ic13, dtype=dtype, device=device).reshape(1, 13).expand(count, 13)
    mass_rows = torch.as_tensor(
        resident.masses.numpy().astype(np.float64), dtype=dtype, device=device
    ).reshape(1, 3).expand(count, 3)
    data_points = SimpleNamespace(
        tau_ic13=torch.cat((tau.reshape(-1, 1), ic13_rows), dim=1),
        masses=mass_rows.contiguous(),
        targets=torch.as_tensor(targets, dtype=dtype, device=device),
    )
    score, score_mask = _windowed_view(references[spec.score_key], window)
    beside, beside_mask = _windowed_view(references[spec.beside_key], window)
    train_view, train_mask = _windowed_view(train, window)
    records = {
        "train": _diagnostic_summary(spec.train_key, train, train_view, train_mask, window),
        "score": _diagnostic_summary(
            spec.score_key, references[spec.score_key], score, score_mask, window
        ),
        "beside": _diagnostic_summary(
            spec.beside_key, references[spec.beside_key], beside, beside_mask, window
        ),
    }
    # Physical time and tau are recorded separately, in float64 regardless of
    # the training dtype, so physical adjacency stays observable beside tau.
    tau64 = 2.0 * (torch.as_tensor(physical_times, dtype=torch.float64) / T_CHARACTERISTIC_TIME) - 1.0
    records["train"]["times_physical"] = [float(value) for value in physical_times.tolist()]
    records["train"]["tau"] = [float(value) for value in tau64.reshape(-1).tolist()]
    return ArmData(
        data_points=data_points,
        ic13=ic13,
        masses=np.asarray(train.masses, dtype=np.float64).reshape(3),
        true_r0=torch.as_tensor(
            resident.snapshot_positions[0].numpy(), dtype=dtype, device=device
        ),
        true_v0=torch.as_tensor(
            resident.snapshot_velocities[0].numpy(), dtype=dtype, device=device
        ),
        score=score,
        beside=beside,
        records=records,
    )


def one_orbit_spec(key):
    """The one-orbit diagnostic fit spec: the same gold key in all three roles.

    The adapter then opens exactly one record (each distinct key is read
    once), so a one-orbit gold fit never needs a base record.
    """
    if not isinstance(key, RecordKey):
        raise TypeError(f"a diagnostic record must be a RecordKey; got {key!r}")
    return fixture_arm(train_key=key, score_key=key, beside_key=key)
