"""Synthetic train/validation/test manifest over a TinyCorpus.

The manifest is written by the production split writer into a temporary run
directory that is not the corpus. Extra synthetic identities pad each
signature to at least ten physical keys so train, validation, and test are
all non-empty. No test here opens the real data root.
"""

from __future__ import annotations

import hashlib
import shutil
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from pinn.data.splits import SplitRatios, write_split_manifest
from pinn.data.types import PhysicalKey, RecordKey, StageLabel
from tests.phase39._fixtures import TinyCorpus


_CLEAN_BASE_IDS = frozenset({0, 7, 42, 55})
_BLACKLISTED_BASE_ID = 3


class _RecordSource:
    def __init__(self, records):
        self._records = tuple(records)

    def admitted_records(self):
        return self._records


def _pair(variant, identifier, *, with_gold):
    physical = PhysicalKey(variant, identifier)
    base_label = StageLabel.STAGE_0 if variant == "hierarchical" else StageLabel.UNASSIGNED
    records = [
        SimpleNamespace(
            physical_key=physical,
            record_key=RecordKey(variant, "base", identifier),
            stage_label=base_label,
        )
    ]
    if with_gold:
        records.append(
            SimpleNamespace(
                physical_key=physical,
                record_key=RecordKey(variant, "gold", identifier),
                stage_label=StageLabel.UNASSIGNED,
            )
        )
    return records


def _base_keys(manifest, split):
    keys = []
    for group in manifest.groups:
        if group.split != split:
            continue
        for record in group.records:
            key = record.record_key
            if key.variant == "hierarchical" and key.fidelity == "base":
                keys.append(key)
    return tuple(sorted(keys))


def _copy_brutus(corpus, src_id, dest_id):
    src = corpus._brutus_path("brutus_hierarchical", "hierarchical", src_id)
    dest = corpus._brutus_path("brutus_hierarchical", "hierarchical", dest_id)
    if src == dest:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    return dest


@contextmanager
def tiny_split_fixture():
    """Yield a temp corpus, a hash-checked splits file, and known keys."""
    with TinyCorpus() as corpus, TemporaryDirectory(prefix="phase59-splits-") as run_tmp:
        records = []
        # Ten physical keys whose gold sibling exists in the manifest, and ten
        # whose gold sibling is missing. TinyCorpus ids are included so an
        # allowlisted key can have a real file.
        for identifier in (0, 3, 7, 1000, 1001, 1002, 1003, 1004, 1005, 1006):
            records.extend(_pair("hierarchical", identifier, with_gold=True))
        for identifier in (42, 55, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107):
            records.extend(_pair("hierarchical", identifier, with_gold=False))
        manifest = write_split_manifest(
            _RecordSource(records),
            Path(run_tmp) / "run",
            seed=11,
            ratios=SplitRatios(),
        )
        manifest_path = Path(manifest.path)
        raw = manifest_path.read_bytes()
        train_clean = [key for key in _base_keys(manifest, "train") if key.id in _CLEAN_BASE_IDS]
        validation_clean = [
            key for key in _base_keys(manifest, "validation") if key.id in _CLEAN_BASE_IDS
        ]
        if train_clean:
            allowed_key = train_clean[0]
        elif validation_clean:
            allowed_key = validation_clean[0]
        else:
            allowed_key = next(
                key for key in _base_keys(manifest, "train") if key.id != _BLACKLISTED_BASE_ID
            )
            _copy_brutus(corpus, 0, allowed_key.id)
        test_keys = _base_keys(manifest, "test")
        test_key = test_keys[0]
        test_key_with_file = test_keys[-1]
        _copy_brutus(corpus, 0, test_key_with_file.id)
        yield SimpleNamespace(
            data_root=corpus.data_root,
            manifest_path=manifest_path,
            manifest_sha256=hashlib.sha256(raw).hexdigest(),
            allowed_key=allowed_key,
            test_key=test_key,
            test_key_with_file=test_key_with_file,
            blacklist_path=corpus.blacklist_path,
        )
