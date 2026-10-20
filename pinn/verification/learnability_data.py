"""Phase 60 (INST-05): the allowlisted data seam for the learnability harness.

Every record an arm reads goes through the hash-checked train and validation
allowlist and the allowlisted reader; this module never builds a corpus path
and never names a corpus folder. A key is checked against the allowlist before
any record is read. Records are windowed to the scored horizon (so the gold
record keeps 1,001 points, not 1,002), and the network input is the real
normalized IC13, normalized the way the trainer normalized it: the statistics
are recovered from the retention-pinned generation-7 checkpoint and must match
a pinned digest (GAP-60-13). The fallback normalizer is never used.

``preflight_records`` applies the same allowlist and reader to every assigned
record before the first arm launches and reports, per record, whether it is
usable (SPEC Requirement 8). It never reads another record in place of a blocked
one, and its report holds no path.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.types import RecordKey
from pinn.verification import evidence_io
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.production_reference import (
    load_reference,
    load_retained_checkpoint,
    recover_normalizer_from_checkpoint,
    resident_record,
    stats_digest,
)
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    AllowlistedCorpusReader,
    NotAdmitted,
    SplitAllowlist,
    SplitRefused,
    expected_splits_sha256,
    install_open_attestation,
    resolve_data_root,
)

__all__ = [
    "EXPECTED_STATS_SHA256",
    "NORMALIZER_FILE",
    "NORMALIZER_RUN",
    "ArmData",
    "DataContext",
    "HarnessHalt",
    "RecordView",
    "fixture_context",
    "load_arm_data",
    "open_real_context",
    "preflight_records",
    "window",
]

_REPO_ROOT = Path(__file__).resolve().parents[2]
# GAP-60-13: the digest of the IC13 statistics every arm uses (evidence/audit/
# reader_acceptance.json of Phase 59, normalizer.stats_sha256).
EXPECTED_STATS_SHA256 = "77526e53c394bbac4d4a0e8fdd5a7688f0bda108d41c56277b55ad426a7a79f6"
NORMALIZER_RUN = "stage0-v23g7-seed42"
NORMALIZER_FILE = "stage-0-init.pt"
_HORIZON_TOLERANCE = 1e-9
# The preflight keeps an unreadable record's reason short and free of local paths. An
# absolute path starts a token, so the "/base/7" inside a key such as "hierarchical/base/7"
# is left alone.
_MESSAGE_LIMIT = 200
_ABSOLUTE_PATH = re.compile(r"(?<![\w.-])/[^\s'\"]+")


class HarnessHalt(RuntimeError):
    """Fail closed. A harness precondition does not hold, so no arm is run."""


@dataclass(frozen=True)
class DataContext:
    """What an arm needs to read records: the allowlist, the reader and the normalizer."""

    allowlist: object
    reader: object
    attestation: object  # the process-wide open attestation, or None
    stats: object
    stats_sha256: str
    normalizer_source: str
    run_kind: str
    data_root_source: str


@dataclass(frozen=True)
class RecordView:
    """One windowed reference record, for scoring."""

    grid: str
    times: object
    positions: object
    inner_pair: tuple
    masses: object


@dataclass(frozen=True)
class ArmData:
    """Training points, scoring views and the record summaries of one arm."""

    data_points: object
    ic13: object
    masses: object
    true_r0: object
    true_v0: object
    score: RecordView
    beside: RecordView
    records: dict


def open_real_context(*, repo_root=None):
    """Open the real corpus through the allowlist and recover the pinned IC13 normalizer.

    Raises ``HarnessHalt`` when the recovered statistics differ from
    ``EXPECTED_STATS_SHA256``. Evidence records ``data_root_source``, never the
    data root.
    """
    root = _REPO_ROOT if repo_root is None else Path(repo_root)
    scorecard = load_scorecard()
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
    reader = AllowlistedCorpusReader(
        allowlist=allowlist, data_root=data_root, data_root_source=source,
    )
    payload, provenance = load_retained_checkpoint(
        root, NORMALIZER_RUN, NORMALIZER_FILE, expected_step=0,
    )
    tolerance = float(scorecard.section("diag07")["tolerances"]["normalizer_recovery_max_abs"])
    recovered = recover_normalizer_from_checkpoint(reader, payload, tolerance=tolerance)
    del payload
    digest = stats_digest(recovered["stats"])
    if digest != EXPECTED_STATS_SHA256:
        raise HarnessHalt(
            f"normalizer stats_sha256 {digest} != pinned {EXPECTED_STATS_SHA256}"
        )
    return DataContext(
        allowlist=allowlist,
        reader=reader,
        attestation=attestation,
        stats=recovered["stats"],
        stats_sha256=digest,
        normalizer_source=f"{recovered['source']}:{provenance['path']}",
        run_kind="real",
        data_root_source=source,
    )


def fixture_context(*, allowlist, reader, stats, attestation=None):
    """A context over a temporary corpus. Its records are marked ``fixture``."""
    return DataContext(
        allowlist=allowlist,
        reader=reader,
        attestation=attestation,
        stats=stats,
        stats_sha256=stats_digest(stats),
        normalizer_source="fixture",
        run_kind="fixture",
        data_root_source=reader.data_root_source,
    )


def _within_horizon(times, t_max):
    return np.asarray(times, dtype=np.float64).reshape(-1) <= float(t_max) + _HORIZON_TOLERANCE


def window(reference, t_max):
    """Times, positions and velocities with t <= t_max (+1e-9), as float64 arrays."""
    keep = _within_horizon(reference.times, t_max)
    return (
        np.asarray(reference.times, dtype=np.float64).reshape(-1)[keep],
        np.asarray(reference.positions, dtype=np.float64)[keep],
        np.asarray(reference.velocities, dtype=np.float64)[keep],
    )


def _view(reference, t_max):
    times, positions, _velocities = window(reference, t_max)
    return RecordView(
        grid=reference.record_key.fidelity,
        times=times,
        positions=positions,
        inner_pair=tuple(int(index) for index in reference.inner_pair),
        masses=np.asarray(reference.masses, dtype=np.float64).reshape(3),
    )


def _summary(key, reference, view):
    digest = hashlib.sha256()
    digest.update(np.ascontiguousarray(view.times, dtype=np.float64).tobytes())
    digest.update(np.ascontiguousarray(view.positions, dtype=np.float64).tobytes())
    return {
        "record_key": evidence_io.record_key_str(key),
        "split": str(reference.split),
        "n_snapshots": int(reference.n_snapshots),
        "n_within_t": int(view.times.shape[0]),
        "dt_out_measured": float(reference.dt_out_measured),
        "windowed_sha256": digest.hexdigest(),
    }


def load_arm_data(spec, context, *, scorecard, dtype, device):
    """Read the three assigned records and build the arm's training points and views.

    The allowlist is asked about all three keys before any record is read, so
    a withheld key raises ``SplitRefused`` with nothing opened. The raw IC13 of
    the train, score and beside records must be identical.
    """
    assigned = (
        ("train", spec.train_key),
        ("score", spec.score_key),
        ("beside", spec.beside_key),
    )
    for _name, key in assigned:
        if not isinstance(key, RecordKey):
            raise TypeError(f"an arm record must be a RecordKey; got {key!r}")
        context.allowlist.require(key)
    t_max = float(scorecard.section("scoring_grid")["t_max"])
    references = {}
    for _name, key in assigned:
        if key not in references:
            references[key] = load_reference(context.reader, key)
    train = references[spec.train_key]
    for name, key in assigned[1:]:
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
    keep = _within_horizon(train.times, t_max)
    count = int(keep.sum())
    if count < 2:
        raise HarnessHalt(
            f"the train record has {count} point(s) within t <= {t_max}; at least 2 are needed"
        )
    resident = resident_record(train, context.stats)
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
    score = _view(references[spec.score_key], t_max)
    beside = _view(references[spec.beside_key], t_max)
    train_view = _view(train, t_max)
    records = {
        "train": _summary(spec.train_key, train, train_view),
        "score": _summary(spec.score_key, references[spec.score_key], score),
        "beside": _summary(spec.beside_key, references[spec.beside_key], beside),
    }
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


def _redacted(text, reader):
    """Exception text with the data root, the home directory and any absolute path removed."""
    text = str(text)
    for private, label in ((Path(reader.data_root), "<data-root>"), (Path.home(), "<home>")):
        if private.is_absolute() and len(private.parts) > 1:
            text = text.replace(str(private), label)
    return _ABSOLUTE_PATH.sub("<path>", text)[:_MESSAGE_LIMIT]


def _preflight_entry(key, context, t_max):
    try:
        split = context.allowlist.require(key)
    except SplitRefused:
        return {"status": "refused"}
    if not context.reader.exists(key):
        return {"status": "missing", "split": split}
    try:
        reference = load_reference(context.reader, key)
    except IndexError:
        # The production admission gate raises IndexError, not NotAdmitted, for a file
        # with no complete snapshot block, so that is how an empty file reaches here.
        return {"status": "empty", "split": split, "n_snapshots": 0}
    except (NotAdmitted, ValueError, OSError) as exc:
        return {
            "status": "unreadable",
            "split": split,
            "error_type": type(exc).__name__,
            "message": _redacted(exc, context.reader),
        }
    if reference.n_snapshots == 0:
        return {"status": "empty", "split": split, "n_snapshots": 0}
    view = _view(reference, t_max)
    summary = _summary(key, reference, view)
    entry = {"status": "ok"}
    entry.update((name, value) for name, value in summary.items() if name != "record_key")
    entry["inner_pair"] = list(view.inner_pair)
    return entry


def preflight_records(keys, context, *, scorecard):
    """Check each assigned record before any arm starts. Returns ``{record_key_str: entry}``.

    Every key must be a ``RecordKey`` (anything else raises ``TypeError`` before a
    record is touched). For each key, in order:

    * ``refused``: the allowlist does not admit it (a test-split or unknown key).
      Nothing is opened, and the reader is not called.
    * ``missing``: allowlisted, but the corpus has no file for it.
    * ``empty``: the file holds no complete snapshot.
    * ``unreadable``: the reader or the admission gate rejects the file. The entry
      names the exception type and a short message with no path in it.
    * ``ok``: read through the production chain. The entry carries ``split``,
      ``n_snapshots``, ``n_within_t`` (the scorecard horizon window), the measured
      ``dt_out_measured``, the ``inner_pair`` and ``windowed_sha256``, the same
      digest an arm's record carries for that record.

    A blocked key is only reported. No other fidelity, variant or id is read in its
    place, and the report holds no path. An error this function does not classify
    propagates.
    """
    keys = tuple(keys)
    for key in keys:
        if not isinstance(key, RecordKey):
            raise TypeError(f"a preflight key must be a RecordKey; got {key!r}")
    t_max = float(scorecard.section("scoring_grid")["t_max"])
    report = {}
    for key in keys:
        label = evidence_io.record_key_str(key)
        if label not in report:
            report[label] = _preflight_entry(key, context, t_max)
    return report
