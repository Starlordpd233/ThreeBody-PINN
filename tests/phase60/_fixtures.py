"""Phase 60 test helpers: a tiny corpus with a gold record the harness may read.

Everything is built under temporary directories. No helper opens the real data
root, and none writes under ``simulation_data/``. Folder names appear here
because the sole-reader audit scans only ``pinn/`` modules, not tests.
"""

from __future__ import annotations

import shutil
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from pinn.data.preprocessing import NormalizationStats
from pinn.data.types import RecordKey
from pinn.verification.split_allowlist import AllowlistedCorpusReader, SplitAllowlist
from tests.phase39._fixtures import BRUTUS_SUBDIR
from tests.phase59._corpus_fixtures import tiny_split_fixture

_BASE_FOLDER = "brutus_hierarchical"
_GOLD_FOLDER = "brutus_hierarchical_gold_standard"
_SOURCE_ID = 0  # TinyCorpus id 0 owns both a base and a gold Brutus file
_BLACKLISTED_ID = 3  # the fixture blacklist names hierarchical id 3
FIXTURE_DATA_ROOT_SOURCE = "fixture"


def _brutus_file(data_root, folder, identifier):
    name = f"brutus_hierarchical_{int(identifier):04d}.txt"
    return Path(data_root) / BRUTUS_SUBDIR / folder / name


def _ensure_copy(data_root, folder, identifier):
    """Place a copy of TinyCorpus id 0's file for ``folder`` at ``identifier``."""
    destination = _brutus_file(data_root, folder, identifier)
    if destination.exists():
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(_brutus_file(data_root, folder, _SOURCE_ID), destination)
    return destination


@contextmanager
def gold_corpus_fixture():
    """Yield a tiny corpus whose first train-split hierarchical id has base and gold files.

    The yielded namespace carries ``data_root``, ``data_root_source``,
    ``manifest_path``, ``manifest_sha256``, ``blacklist_path``, ``allowlist``
    (hash-checked), ``reader`` (with the fixture blacklist), ``stats`` (the
    identity normalizer: zero means, unit deviations, unit energy scale),
    ``base_key`` and ``gold_key`` (both train split, same id) and
    ``test_key`` (a withheld test-split base key).
    """
    with tiny_split_fixture() as inner:
        allowlist = SplitAllowlist.from_manifest(
            inner.manifest_path, expected_sha256=inner.manifest_sha256
        )
        candidates = [
            key
            for key in allowlist.records("train", variant="hierarchical", fidelity="base")
            if int(key.id) != _BLACKLISTED_ID
        ]
        if not candidates:
            raise AssertionError("the fixture manifest has no usable train hierarchical key")
        identifier = int(candidates[0].id)
        _ensure_copy(inner.data_root, _BASE_FOLDER, identifier)
        _ensure_copy(inner.data_root, _GOLD_FOLDER, identifier)
        reader = AllowlistedCorpusReader(
            allowlist=allowlist,
            data_root=inner.data_root,
            data_root_source=FIXTURE_DATA_ROOT_SOURCE,
            blacklist_path=inner.blacklist_path,
        )
        yield SimpleNamespace(
            data_root=Path(inner.data_root),
            data_root_source=FIXTURE_DATA_ROOT_SOURCE,
            manifest_path=Path(inner.manifest_path),
            manifest_sha256=inner.manifest_sha256,
            blacklist_path=Path(inner.blacklist_path),
            allowlist=allowlist,
            reader=reader,
            stats=NormalizationStats(
                slot_means=np.zeros(12), slot_stds=np.ones(12), e_scale=1.0
            ),
            base_key=RecordKey("hierarchical", "base", identifier),
            gold_key=RecordKey("hierarchical", "gold", identifier),
            test_key=inner.test_key,
        )
