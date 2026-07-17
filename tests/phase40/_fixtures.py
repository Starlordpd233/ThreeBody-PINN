"""Phase 40 dataset-free fixtures — no ``simulation_data/`` access.

Provides three builders that make the whole TRAIN-01..07 suite runnable with no
on-disk corpus:

- ``make_stub_source`` — a duck-typed ``StageQuery`` mirroring the
  ``pinn/data/splits.StageIndex`` method surface that
  ``pinn/data/batches.build_stage_batch`` dereferences (``has_stage``,
  ``records_at``, ``records_at_or_below``, ``record_keys``, ``get``,
  ``n_snapshots``, ``snapshot_times``, ``snapshot_positions``,
  ``snapshot_velocities``, ``acceleration_magnitudes``, ``stage_label``,
  ``is_blacklisted``, plus the ``blacklisted_physical_keys`` property and the
  ``gold_numeric_stage_count`` attribute).
- ``make_stub_split_sources`` — returns a disjoint ``(train_source,
  validation_source)`` pair, mirroring production's
  ``StageIndex.from_split(source, manifest, "train")`` /
  ``StageIndex.from_split(source, manifest, "validation")``: two separate
  StageIndex-shaped instances over non-overlapping physical keys. The held-out
  split name is ``"validation"`` (per ``_SPLIT_NAMES`` at splits.py:39), NOT
  ``"val"`` — no split flag is invented on a single source.
- ``make_stub_model`` — ``build_network(ArchitectureSpec(), dtype=torch.float64,
  device=torch.device("cpu"))``; dtype/device are explicit args (the defaults
  are the cheap test configuration; nothing inside ``pinn/`` hardcodes them).

RNG discipline: any RNG accepted by these fixtures is an explicit
``numpy.random.Generator`` (per ``pinn/data/batches._require_local_rng``); no
``np.random.seed`` / global state.
"""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np


class _StubSource:
    """Duck-typed ``StageQuery`` over a synthetic record population.

    Two instances with disjoint ``id`` populations model production's separate
    ``StageIndex`` per split (the shape ``StageIndex.from_split`` materializes
    for ``"train"`` and ``"validation"``). Heavy ``pinn.data.types`` imports are
    deferred to ``__init__`` so importing this module is side-effect-free.
    """

    def __init__(self, stage0_ids, stage1_ids=(), gold_numeric_stage_count=0,
                 blacklisted=()):
        # Deferred so importing tests.phase40._fixtures performs no heavy init.
        from pinn.data.types import RecordKey, StageLabel
        self.RecordKey = RecordKey
        self.StageLabel = StageLabel
        self._s0 = [RecordKey("hierarchical", "base", i) for i in stage0_ids]
        self._s1 = [RecordKey("hierarchical", "base", i) for i in stage1_ids]
        self._gold_numeric_stage_count = int(gold_numeric_stage_count)
        self._black = set(blacklisted)

    @property
    def blacklisted_physical_keys(self):
        return frozenset(
            key.physical_key
            for key in tuple(self._s0) + tuple(self._s1)
            if (key.variant, key.id) in self._black
        )

    def has_stage(self, k):
        return {0: bool(self._s0), 1: bool(self._s1)}.get(k, False)

    def records_at(self, k):
        return tuple(self._s0 if k == 0 else self._s1 if k == 1 else ())

    def records_at_or_below(self, k):
        out = []
        if k >= 0:
            out += self._s0
        if k >= 1:
            out += self._s1
        return tuple(out)

    def record_keys(self):
        return tuple(sorted(tuple(self._s0) + tuple(self._s1)))

    def get(self, key):
        return SimpleNamespace(
            record_key=key,
            physical_key=key.physical_key,
            stage_label=self.stage_label(key),
            n_snapshots=self.n_snapshots(key),
            ic13=np.linspace(0.0, 1.2, 13, dtype=np.float64) + key.id / 10000.0,
            masses=np.array([1.0 + key.id / 10000.0, 2.0, 3.0], dtype=np.float64),
        )

    def n_snapshots(self, key):
        return 32

    def snapshot_times(self, key):
        # Deliberately ends at 9.5 so a per-record times[-1] normalizer is caught.
        return np.linspace(0.0, 9.5, self.n_snapshots(key), dtype=np.float64)

    def snapshot_positions(self, key):
        times = self.snapshot_times(key)
        positions = np.zeros((len(times), 3, 3), dtype=np.float64)
        positions[:, 0, 0] = times + key.id / 1000.0
        positions[:, 1, 1] = 2.0 * times
        positions[:, 2, 2] = -times
        return positions

    def snapshot_velocities(self, key):
        times = self.snapshot_times(key)
        velocities = np.zeros((len(times), 3, 3), dtype=np.float64)
        velocities[:, 0, 0] = times ** 2
        velocities[:, 1, 1] = times
        return velocities

    def acceleration_magnitudes(self, key):
        return np.arange(1, self.n_snapshots(key) + 1, dtype=np.float64)

    def stage_label(self, key):
        if key in self._s0:
            return self.StageLabel.STAGE_0
        if key in self._s1:
            return self.StageLabel.STAGE_1
        return self.StageLabel.UNASSIGNED

    def is_blacklisted(self, physical_key):
        return physical_key in self.blacklisted_physical_keys

    @property
    def gold_numeric_stage_count(self):
        return self._gold_numeric_stage_count


def make_stub_source(n_stage0=300, n_stage1=0, id_offset=0):
    """Build a single StageQuery-shaped stub source over a synthetic population.

    Defaults to a stage-0-only population (the shape a stage-0 training batch
    draws replay from); ``n_stage1`` and ``id_offset`` let downstream tests
    construct adjacent-stage or offset populations without sharing keys.
    """
    stage0_ids = tuple(range(id_offset, id_offset + n_stage0))
    stage1_ids = tuple(range(id_offset + 10000, id_offset + 10000 + n_stage1))
    return _StubSource(stage0_ids, stage1_ids)


def make_stub_split_sources(n_train=300, n_validation=300):
    """Return a disjoint ``(train_source, validation_source)`` pair.

    Mirrors production's ``StageIndex.from_split(source, manifest, "train")``
    and ``StageIndex.from_split(source, manifest, "validation")`` — two separate
    ``StageIndex`` instances over non-overlapping physical keys. The held-out
    split name is ``"validation"`` (per ``_SPLIT_NAMES`` at splits.py:39), NOT
    ``"val"``; the stub models this as two independent sources, NOT one source
    with a split flag. 40-05's ``RunController`` accepts ``validation_source``
    as its own constructor argument, so no downstream plan edits this file.
    """
    train_source = make_stub_source(n_stage0=n_train, id_offset=0)
    # Non-overlapping id range guarantees disjoint physical keys.
    validation_source = make_stub_source(n_stage0=n_validation, id_offset=50000)
    return train_source, validation_source


def make_stub_model(dtype=None, device=None):
    """Build a CPU/float64 stub model via ``pinn.network.build_network``.

    ``dtype``/``device`` are explicit args (not hardcoded inside ``pinn/``); the
    defaults are the cheap test configuration (CPU/float64 is cheap enough for
    unit tests per ``pinn/verification/overfit_probe.py``).
    """
    if dtype is None:
        import torch
        dtype = torch.float64
    if device is None:
        import torch
        device = torch.device("cpu")
    from pinn.architecture_spec import ArchitectureSpec
    from pinn.network import build_network
    return build_network(ArchitectureSpec(), dtype=dtype, device=device)
