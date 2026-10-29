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
"""

from __future__ import annotations

from pinn.data.types import RecordKey
from pinn.verification import evidence_io, split_allowlist
from pinn.verification.learnability_arms import fixture_arm
from pinn.verification.learnability_data import load_arm_data
from pinn.verification.split_allowlist import (
    AllowlistedCorpusReader,
    SplitRefused,
)

__all__ = [
    "Stage0TrainingRefused",
    "Stage0TrainingReader",
    "orbit_stage",
    "require_stage0_training",
    "load_diagnostic_data",
    "one_orbit_spec",
]


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


def load_diagnostic_data(spec, context, *, scorecard, dtype, device):
    """Validate every assigned key against the Stage-0 boundary, then load.

    All three assigned keys (train, score, beside) are validated as a set
    before the first record is read, so an invalid ancillary key blocks an
    otherwise valid target with nothing opened. Every later read is guarded
    again by the Stage-0 reader, and the existing ``load_arm_data`` seam
    (preprocessing, residency, raw masses, IC13, body permutation and the
    ``ArmData`` shape) is reused unchanged. The one-orbit gold fit passes
    :func:`one_orbit_spec`, so a single record serves all three roles and no
    base record is opened.
    """
    for _role, key in _assignment(spec):
        require_stage0_training(context.allowlist, key)
    return load_arm_data(spec, context, scorecard=scorecard, dtype=dtype, device=device)


def one_orbit_spec(key):
    """The one-orbit diagnostic fit spec: the same gold key in all three roles.

    The adapter then opens exactly one record (``load_arm_data`` reads each
    distinct key once), so a one-orbit gold fit never needs a base record.
    """
    if not isinstance(key, RecordKey):
        raise TypeError(f"a diagnostic record must be a RecordKey; got {key!r}")
    return fixture_arm(train_key=key, score_key=key, beside_key=key)
