"""Phase 59 (D-26, D-35): the one corpus choke point for Phase-59 tools.

This is the only Phase-59 module that builds a corpus path. It never
instantiates the admitted-set adapter or the trainer's source builder (they
parse every file of every split), and it never globs a corpus folder. Folder
names come from inverting the imported folder table. A refused key raises
before any path is built.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

from pinn.data.adapter import (
    BRUTUS_FOLDER_TABLE,
    BRUTUS_SUBDIR,
    DATA_ROOT_ENV,
    default_data_root,
    load_blacklist_file,
    measure_dt_out,
    parse_brutus_file,
    parse_footer,
    to_parsed_trajectory,
)
from pinn.data.admission import evaluate_admission
from pinn.data.splits import SplitManifest
from pinn.data.types import MISSING_GOLD, PhysicalKey, RecordKey, StageLabel


GENERATION7_SPLITS_REL = Path("runs/stage0-v23g7-seed42/splits.json")
GENERATION7_RETENTION_REL = Path(
    ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/"
    "generation-7-retention.json"
)
# configs/stage0-v23g7-seed42.yaml data.blacklist_path, resolved against the
# data root the way pinn/train.py resolves a relative blacklist.
BLACKLIST_RELATIVE_TO_DATA_ROOT = Path("../Documentation/problematic_ics_blacklist.json")

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_REPO_ROOT = Path(__file__).resolve().parents[2]
_ALLOWED_SPLITS = ("train", "validation")
_FOLDER_FOR = {
    (variant, fidelity): folder
    for folder, (variant, fidelity) in BRUTUS_FOLDER_TABLE.items()
}
_REFUSAL = "refused before any path is built"


class SplitRefused(PermissionError):
    """A key is withheld or unknown. Raised before any corpus path is built."""


class NotAdmitted(ValueError):
    """The production admission gate did not admit this allowlisted record."""

    def __init__(self, record_key, disposition, reasons):
        self.record_key = record_key
        self.disposition = disposition
        self.reasons = tuple(reasons)
        super().__init__(
            f"{record_key.variant}/{record_key.fidelity}/{record_key.id} "
            f"{disposition}: {', '.join(str(reason) for reason in self.reasons)}"
        )


def _repo_root(repo_root):
    if repo_root is None:
        return _REPO_ROOT
    return Path(repo_root)


def expected_splits_sha256(repo_root=None) -> str:
    """Return the retention-manifest SHA-256 of the generation-7 splits file."""
    path = _repo_root(repo_root) / GENERATION7_RETENTION_REL
    payload = json.loads(path.read_text(encoding="utf-8"))
    target = GENERATION7_SPLITS_REL.as_posix()
    for entry in payload.get("files", ()):
        if entry.get("path") != target:
            continue
        digest = entry.get("sha256")
        if not isinstance(digest, str) or _HEX64.fullmatch(digest) is None:
            raise ValueError(f"retention sha256 for {target} is not 64 lowercase hex")
        return digest
    raise ValueError(f"retention manifest has no entry for {target}")


def resolve_data_root(explicit=None):
    """Resolve the corpus root and a label that evidence may record.

    Precedence matches the adapter: an explicit root, then ``GSD_DATA_ROOT``,
    then the git-common-dir default. The label is not a path.
    """
    if explicit is not None:
        return Path(explicit), "explicit"
    env = os.environ.get(DATA_ROOT_ENV)
    if env:
        return Path(env), "env:GSD_DATA_ROOT"
    return default_data_root(), "git_common_dir_default"


def _stage_value(label):
    if label is StageLabel.UNASSIGNED:
        return "UNASSIGNED"
    if isinstance(label, StageLabel):
        return int(label.value)
    return label


def _physical_key(key):
    if isinstance(key, RecordKey):
        return key.physical_key
    if isinstance(key, PhysicalKey):
        return key
    raise TypeError(f"key must be RecordKey or PhysicalKey; got {key!r}")


def _brutus_name(variant, identifier):
    return f"brutus_{variant}_{int(identifier):04d}.txt"


def _ic_name(variant, identifier):
    return f"ic_{variant}_{int(identifier):04d}.txt"


def _iter_keys(manifest, split, *, variant=None, fidelity=None, stage=None):
    found = []
    for group in manifest.groups:
        if group.split != split:
            continue
        gold_missing = group.signature[2] is MISSING_GOLD
        if fidelity == "gold" and gold_missing:
            continue
        for record in group.records:
            key = record.record_key
            if gold_missing and key.fidelity == "gold":
                continue
            if variant is not None and key.variant != variant:
                continue
            if fidelity is not None and key.fidelity != fidelity:
                continue
            if stage is not None and _stage_value(record.stage_label) != stage:
                continue
            found.append(key)
    return tuple(sorted(found))


@dataclass(frozen=True)
class SplitAllowlist:
    """Train and validation physical keys, with the test split withheld."""

    allowed: frozenset
    withheld: frozenset
    split_of: MappingProxyType
    manifest: SplitManifest
    manifest_sha256: str

    @classmethod
    def from_manifest(cls, path, *, expected_sha256):
        manifest_path = Path(path)
        raw = manifest_path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected_sha256:
            raise ValueError(
                f"splits manifest sha256 {digest} != expected {expected_sha256}"
            )
        manifest = SplitManifest.from_dict(json.loads(raw), path=manifest_path)
        allowed = manifest.physical_keys("train") | manifest.physical_keys("validation")
        withheld = manifest.physical_keys("test")
        assert allowed.isdisjoint(withheld)
        split_of = {group.physical_key: group.split for group in manifest.groups}
        return cls(
            allowed=frozenset(allowed),
            withheld=frozenset(withheld),
            split_of=MappingProxyType(split_of),
            manifest=manifest,
            manifest_sha256=digest,
        )

    def require(self, key) -> str:
        """Return ``train`` or ``validation``. Refuse before any path exists."""
        physical = _physical_key(key)
        split = self.split_of.get(physical)
        if split not in _ALLOWED_SPLITS or physical in self.withheld:
            raise SplitRefused(f"{_REFUSAL}: {physical.variant} id {physical.id}")
        return split

    def records(self, split, *, variant=None, fidelity=None, stage=None):
        if split == "test" or split not in _ALLOWED_SPLITS:
            raise SplitRefused(_REFUSAL)
        return _iter_keys(
            self.manifest, split, variant=variant, fidelity=fidelity, stage=stage
        )

    def manifest_stage(self, key):
        """Return the manifest stage ``0``, ``1``, or ``UNASSIGNED``."""
        wanted = key if isinstance(key, RecordKey) else None
        physical = _physical_key(key)
        for group in self.manifest.groups:
            if group.physical_key != physical:
                continue
            for record in group.records:
                if wanted is None or record.record_key == wanted:
                    return _stage_value(record.stage_label)
        raise KeyError(key)

    def withheld_basenames(self):
        names = set()
        for key in self.withheld:
            names.add(_brutus_name(key.variant, key.id))
            names.add(_ic_name(key.variant, key.id))
        return frozenset(names)

    def split_by_basename(self):
        mapping = {}
        for split in _ALLOWED_SPLITS:
            for key in self.records(split):
                mapping[_brutus_name(key.variant, key.id)] = split
                mapping[_ic_name(key.variant, key.id)] = split
        return mapping


@dataclass(frozen=True)
class AdmittedRead:
    record_key: RecordKey
    split: str
    parsed_brutus: object
    parsed: object
    dt_out_reference: object
    dt_out_reference_provenance: object
    dt_out_measured: float
    admission: object


class AllowlistedCorpusReader:
    """Read one allowlisted Brutus file through the production per-file seams."""

    def __init__(self, *, allowlist, data_root, data_root_source, blacklist_path=None):
        self.allowlist = allowlist
        self.data_root = Path(data_root)
        self.data_root_source = data_root_source
        if blacklist_path is None:
            blacklist_path = self.data_root / BLACKLIST_RELATIVE_TO_DATA_ROOT
        keys, _entries = load_blacklist_file(Path(blacklist_path))
        self._blacklist = keys
        self._reads = {"train": 0, "validation": 0}
        self._refusals = 0

    def _require(self, key):
        try:
            return self.allowlist.require(key)
        except SplitRefused:
            self._refusals += 1
            raise

    def _brutus_path(self, key: RecordKey) -> Path:
        folder = _FOLDER_FOR[(key.variant, key.fidelity)]
        return self.data_root / BRUTUS_SUBDIR / folder / _brutus_name(key.variant, key.id)

    def read(self, key: RecordKey) -> AdmittedRead:
        if not isinstance(key, RecordKey):
            raise TypeError(f"read() requires a RecordKey; got {key!r}")
        split = self._require(key)
        path = self._brutus_path(key)
        parsed_brutus = parse_brutus_file(path, root=self.data_root)
        parsed = to_parsed_trajectory(key, parsed_brutus)
        reference, provenance, _anomalous, _missing = parse_footer(
            parsed_brutus.footer_raw, variant=key.variant, fidelity=key.fidelity
        )
        measured = measure_dt_out(parsed_brutus.times)
        admission = evaluate_admission(
            parsed,
            blacklist=self._blacklist,
            remediation_quarantine=frozenset(),
            dt_out=reference.get("dt_out"),
        )
        if admission.disposition != "admit":
            raise NotAdmitted(key, admission.disposition, admission.reasons)
        self._reads[split] += 1
        return AdmittedRead(
            record_key=key,
            split=split,
            parsed_brutus=parsed_brutus,
            parsed=parsed,
            dt_out_reference=reference.get("dt_out"),
            dt_out_reference_provenance=provenance.get("dt_out"),
            dt_out_measured=float(measured),
            admission=admission,
        )

    def exists(self, key: RecordKey) -> bool:
        if not isinstance(key, RecordKey):
            raise TypeError(f"exists() requires a RecordKey; got {key!r}")
        self._require(key)
        return self._brutus_path(key).exists()

    def read_counts(self):
        return {
            "train": self._reads["train"],
            "validation": self._reads["validation"],
            "refusals": self._refusals,
        }


def _lowest_key(manifest, split, variant, fidelity):
    keys = _iter_keys(manifest, split, variant=variant, fidelity=fidelity)
    if not keys:
        raise ValueError(f"no manifest record for {split} {variant} {fidelity}")
    return keys[0]


def _record_payload(key: RecordKey):
    return {"variant": key.variant, "fidelity": key.fidelity, "id": int(key.id)}


def probe(split, *, variant="hierarchical", fidelity="base", data_root=None,
          manifest=GENERATION7_SPLITS_REL):
    """Admit the lowest-id allowlisted record, or refuse a test key before a path."""
    root, label = resolve_data_root(data_root)
    allowlist = SplitAllowlist.from_manifest(
        manifest, expected_sha256=expected_splits_sha256()
    )
    # Test-split identity comes from manifest metadata only. read() then refuses
    # before a path is built. Train and validation are actually read.
    key = _lowest_key(allowlist.manifest, split, variant, fidelity)
    reader = AllowlistedCorpusReader(
        allowlist=allowlist, data_root=root, data_root_source=label
    )
    if split == "test":
        try:
            reader.read(key)
        except SplitRefused:
            return {
                "probe_split": split,
                "record": _record_payload(key),
                "outcome": "refused_before_path",
                "n_snapshots": None,
                "data_root_source": label,
            }
        raise AssertionError("test-split probe read a record")
    admitted = reader.read(key)
    return {
        "probe_split": split,
        "record": _record_payload(key),
        "outcome": "admitted",
        "n_snapshots": int(admitted.parsed.times.shape[0]),
        "data_root_source": label,
    }


def main(argv=None) -> int:
    """Probe CLI. The freeze guard runs before any manifest or corpus access."""
    parser = argparse.ArgumentParser(prog="split_allowlist")
    parser.add_argument("--probe-split", required=True, choices=("train", "validation", "test"))
    parser.add_argument("--variant", default="hierarchical", choices=("hierarchical", "standard"))
    parser.add_argument("--fidelity", default="base", choices=("base", "gold"))
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--manifest", default=str(GENERATION7_SPLITS_REL))
    args = parser.parse_args(argv)
    evidence_io = importlib.import_module("pinn.verification.evidence_io")
    try:
        freeze = evidence_io.require_frozen_scorecard()
    except evidence_io.FreezeNotEstablished as exc:
        print(f"FREEZE-REFUSED: {exc}", file=sys.stderr)
        return 1
    print(f"FREEZE-OK {freeze['freeze_commit']}", file=sys.stderr)
    result = probe(
        args.probe_split,
        variant=args.variant,
        fidelity=args.fidelity,
        data_root=args.data_root,
        manifest=Path(args.manifest),
    )
    print(json.dumps(result))
    expected = "refused_before_path" if args.probe_split == "test" else "admitted"
    return 0 if result.get("outcome") == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "GENERATION7_RETENTION_REL",
    "GENERATION7_SPLITS_REL",
    "AdmittedRead",
    "AllowlistedCorpusReader",
    "NotAdmitted",
    "SplitAllowlist",
    "SplitRefused",
    "expected_splits_sha256",
    "main",
    "probe",
    "resolve_data_root",
]
