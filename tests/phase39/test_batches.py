"""Phase 39 Wave-0 contract — the replay/lookahead two-point-set batch (DATA-05).

Deferred contract for ``pinn.data.batches`` (GAP-39-10 global ``T = 10.0`` for
``tau``/collocation with NO per-record ``FixedBatch.T``; GAP-39-12 Option-C
near-even collocation quotas). Every deferred test SKIPs via the localized
``_require`` helper until production lands; the global-``T`` constant anchor runs
green now.

Grounding: ``ctl_instruction.md:1813-1853``; GAP-39-10 resolution (global
``T_CHARACTERISTIC_TIME = 10.0``, per-record ``FixedBatch.T`` removed); GAP-39-12
resolution (Option C: ``q = floor(C/M)``, ``r = C mod M``, one extra point to
``r`` identities by a canonical seeded permutation; 256 -> 16 each; 240 -> 17
each plus 16 seeded 18s).
"""

import importlib
import unittest
from types import SimpleNamespace

from tests.phase39 import _SKIP_PHRASE

BATCHES = "pinn.data.batches"
TYPES = "pinn.data.types"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _rng(seed=0):
    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover
        raise unittest.SkipTest(f"numpy not installed: {exc}")
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# GAP-39-10 — global characteristic time (green now).
# ---------------------------------------------------------------------------

class GlobalCharacteristicTimeTests(unittest.TestCase):
    def test_characteristic_time_is_global_ten(self):
        constants = importlib.import_module("pinn.constants")
        self.assertEqual(constants.T_CHARACTERISTIC_TIME, 10.0)

    def test_fixed_batch_exposes_no_per_record_T_field(self):
        import dataclasses
        FixedBatch = _require("FixedBatch", TYPES)
        names = {f.name for f in dataclasses.fields(FixedBatch)}
        self.assertNotIn("T", names,
                         "GAP-39-10 removed the per-record FixedBatch.T field")


# ---------------------------------------------------------------------------
# GAP-39-12 — Option-C collocation quota allocation.
# ---------------------------------------------------------------------------

class CollocationQuotaTests(unittest.TestCase):
    def setUp(self):
        self.allocate = _require("allocate_collocation_quota", BATCHES)

    def test_populated_lookahead_batch_is_exactly_balanced(self):
        counts = self.allocate(256, 4096, _rng(1))
        self.assertEqual(len(counts), 256)
        self.assertEqual(sum(counts), 4096)
        self.assertEqual(set(counts), {16})

    def test_replay_only_batch_uses_quotient_plus_seeded_remainder(self):
        counts = self.allocate(240, 4096, _rng(1))       # 4096 = 17*240 + 16
        self.assertEqual(len(counts), 240)
        self.assertEqual(sum(counts), 4096)
        self.assertEqual(min(counts), 17)
        self.assertEqual(max(counts), 18)
        self.assertEqual(sum(1 for c in counts if c == 18), 16)

    def test_quota_total_is_exact_and_seed_stable(self):
        a = self.allocate(240, 4096, _rng(7))
        b = self.allocate(240, 4096, _rng(7))
        self.assertEqual(list(a), list(b))               # deterministic per seed


# ---------------------------------------------------------------------------
# Replay / lookahead selection (deferred).
# ---------------------------------------------------------------------------

class _Query:
    """A minimal StageQuery over persisted base Set-1a labels."""

    def __init__(self, RecordKey, StageLabel, n_stage0=300, n_stage1=20,
                 blacklisted=(), inject_gold=False):
        self.RecordKey, self.StageLabel = RecordKey, StageLabel
        self._s0 = [RecordKey("hierarchical", "base", i) for i in range(n_stage0)]
        self._s1 = [RecordKey("hierarchical", "base", 1000 + i) for i in range(n_stage1)]
        if inject_gold and self._s0:
            self._s0[0] = RecordKey("hierarchical", "gold", 0)   # bypass attempt
        self._black = set(blacklisted)

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

    def stage_label(self, key):
        if key in self._s0:
            return self.StageLabel.STAGE_0
        if key in self._s1:
            return self.StageLabel.STAGE_1
        return self.StageLabel.UNASSIGNED

    def is_blacklisted(self, key):
        return (key.variant, key.id) in self._black


class SelectionContract(unittest.TestCase):
    def setUp(self):
        self.select = _require("select_batch_trajectories", BATCHES)
        self.RecordKey = _require("RecordKey", TYPES)
        self.StageLabel = _require("StageLabel", TYPES)

    def _query(self, **over):
        return _Query(self.RecordKey, self.StageLabel, **over)

    def test_240_replay_plus_16_lookahead_when_stage1_present(self):
        replay, lookahead = self.select(self._query(), stage=0, rng=_rng(0))
        self.assertEqual(len(replay), 240)
        self.assertEqual(len(lookahead), 16)
        for key in tuple(replay) + tuple(lookahead):
            self.assertEqual(key.fidelity, "base")
            self.assertEqual(key.variant, "hierarchical")

    def test_replay_only_when_no_next_stage(self):
        replay, lookahead = self.select(self._query(n_stage1=0), stage=0, rng=_rng(0))
        self.assertEqual(len(replay), 240)
        self.assertEqual(len(lookahead), 0)

    def test_undersized_next_pool_pads_with_replacement_to_16(self):
        replay, lookahead = self.select(self._query(n_stage1=5), stage=0, rng=_rng(0))
        self.assertEqual(len(replay), 240)
        self.assertEqual(len(lookahead), 16)                 # padded to 16
        self.assertLessEqual(len(set(lookahead)), 5)          # replacement padding

    def test_blacklisted_key_in_pool_is_a_hard_failure(self):
        q = self._query(blacklisted=[("hierarchical", 0)])
        with self.assertRaises((ValueError, AssertionError)):
            self.select(q, stage=0, rng=_rng(0))

    def test_gold_key_in_numeric_pool_is_a_hard_failure(self):
        q = self._query(inject_gold=True)
        with self.assertRaises((ValueError, AssertionError)):
            self.select(q, stage=0, rng=_rng(0))


# ---------------------------------------------------------------------------
# Full batch assembly (deferred) — two point sets, aligned shapes.
# ---------------------------------------------------------------------------

class _DataQuery(_Query):
    """A StageQuery that also serves per-record trajectory data for assembly."""

    def n_snapshots(self, key):
        return 32

    def ic13(self, key):
        import numpy as np
        return np.zeros(13, dtype=np.float64)

    def masses(self, key):
        import numpy as np
        return np.array([1.0, 1.0, 1.0], dtype=np.float64)

    def snapshot_times(self, key):
        import numpy as np
        return np.linspace(0.0, 10.0, 32)


class FullBatchContract(unittest.TestCase):
    def test_batch_emits_two_distinct_point_sets_with_aligned_shapes(self):
        build_stage_batch = _require("build_stage_batch", BATCHES)
        RecordKey = _require("RecordKey", TYPES)
        StageLabel = _require("StageLabel", TYPES)
        torch = None
        try:
            import torch  # noqa: F401
        except ImportError as exc:  # pragma: no cover
            raise unittest.SkipTest(f"torch not installed: {exc}")

        query = _DataQuery(RecordKey, StageLabel)
        batch = build_stage_batch(query, stage=0, rng=_rng(0),
                                  dtype=torch.float32, device=torch.device("cpu"))
        # Two independent point sets (not one aliased field).
        self.assertIsNot(batch.data_points, batch.collocation_points)
        # Model-facing tensors: last dims 14 ([tau, IC13]) and 3 (raw masses).
        self.assertEqual(batch.data_points.tau_ic13.shape[-1], 14)
        self.assertEqual(batch.data_points.masses.shape[-1], 3)
        # Collocation carries continuous times drawn from the global [0, 10].
        self.assertTrue(float(batch.collocation_points.times.min()) >= 0.0)
        self.assertTrue(float(batch.collocation_points.times.max()) <= 10.0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
