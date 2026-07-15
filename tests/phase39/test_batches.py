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
        mod = importlib.import_module(BATCHES)
        self.allocate = getattr(mod, "allocate_collocation_quota")

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

    def test_general_quota_has_exact_remainder_and_spread(self):
        for identities, total in ((7, 31), (11, 5), (3, 12)):
            with self.subTest(identities=identities, total=total):
                counts = self.allocate(identities, total, _rng(3))
                q, r = divmod(total, identities)
                self.assertEqual(sum(counts), total)
                self.assertTrue(set(counts).issubset({q, q + 1}))
                self.assertEqual(sum(value == q + 1 for value in counts), r)
                self.assertLessEqual(max(counts) - min(counts), 1)

    def test_different_seed_may_change_remainder_recipients(self):
        self.assertNotEqual(
            self.allocate(240, 4096, _rng(1)),
            self.allocate(240, 4096, _rng(2)),
        )

    def test_empty_identity_set_fails(self):
        with self.assertRaises((ValueError, AssertionError)):
            self.allocate(0, 4096, _rng(0))


# ---------------------------------------------------------------------------
# Replay / lookahead selection (deferred).
# ---------------------------------------------------------------------------

class _Query:
    """A minimal StageQuery over persisted base Set-1a labels."""

    def __init__(self, RecordKey, StageLabel, n_stage0=300, n_stage1=20,
                 blacklisted=(), inject_gold=False, inject_standard=False,
                 gold_numeric_stage_count=0):
        self.RecordKey, self.StageLabel = RecordKey, StageLabel
        self._s0 = [RecordKey("hierarchical", "base", i) for i in range(n_stage0)]
        self._s1 = [RecordKey("hierarchical", "base", 1000 + i) for i in range(n_stage1)]
        if inject_gold and self._s0:
            self._s0[0] = RecordKey("hierarchical", "gold", 0)   # bypass attempt
        if inject_standard and self._s0:
            self._s0[0] = RecordKey("standard", "base", 0)       # bypass attempt
        self._black = set(blacklisted)
        self.gold_numeric_stage_count = gold_numeric_stage_count

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
        mod = importlib.import_module(BATCHES)
        self.select = getattr(mod, "select_stage_records")
        self.compat_select = getattr(mod, "select_batch_trajectories")
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

    def test_frozen_name_is_identity_alias_of_canonical_selector(self):
        self.assertIs(self.compat_select, self.select)

    def test_replay_only_when_no_next_stage(self):
        replay, lookahead = self.select(self._query(n_stage1=0), stage=0, rng=_rng(0))
        self.assertEqual(len(replay), 240)
        self.assertEqual(len(lookahead), 0)

    def test_undersized_next_pool_pads_with_replacement_to_16(self):
        replay, lookahead = self.select(self._query(n_stage1=5), stage=0, rng=_rng(0))
        self.assertEqual(len(replay), 240)
        self.assertEqual(len(lookahead), 16)                 # padded to 16
        self.assertLessEqual(len(set(lookahead)), 5)          # replacement padding

    def test_lookahead_boundaries_one_fifteen_sixteen_and_larger(self):
        for pool_size in (1, 15, 16, 17):
            with self.subTest(pool_size=pool_size):
                _replay, lookahead = self.select(
                    self._query(n_stage1=pool_size), stage=0, rng=_rng(4))
                self.assertEqual(len(lookahead), 16)
                if pool_size < 16:
                    self.assertLessEqual(len(set(lookahead)), pool_size)
                else:
                    self.assertEqual(len(set(lookahead)), 16)

    def test_true_but_empty_next_stage_is_inconsistent(self):
        query = self._query(n_stage1=0)
        query.has_stage = lambda stage: stage == 1
        with self.assertRaises((ValueError, AssertionError)):
            self.select(query, stage=0, rng=_rng(0))

    def test_insufficient_replay_pool_fails_before_sampling(self):
        with self.assertRaises(Exception):
            self.select(self._query(n_stage0=239), stage=0, rng=_rng(0))

    def test_selection_is_seed_stable_and_does_not_touch_global_numpy_rng(self):
        import numpy as np

        np.random.seed(321)
        before = np.random.get_state()
        first = self.select(self._query(), stage=0, rng=_rng(9))
        second = self.select(self._query(), stage=0, rng=_rng(9))
        after = np.random.get_state()

        self.assertEqual(first, second)
        self.assertEqual(before[0], after[0])
        self.assertTrue(np.array_equal(before[1], after[1]))
        self.assertEqual(before[2:], after[2:])

    def test_blacklisted_key_in_pool_is_a_hard_failure(self):
        q = self._query(blacklisted=[("hierarchical", 0)])
        with self.assertRaises((ValueError, AssertionError)):
            self.select(q, stage=0, rng=_rng(0))

    def test_gold_key_in_numeric_pool_is_a_hard_failure(self):
        q = self._query(inject_gold=True)
        with self.assertRaises((ValueError, AssertionError)):
            self.select(q, stage=0, rng=_rng(0))

    def test_non_hierarchical_key_in_numeric_pool_is_a_hard_failure(self):
        q = self._query(inject_standard=True)
        with self.assertRaises((ValueError, AssertionError)):
            self.select(q, stage=0, rng=_rng(0))

    def test_nonzero_gold_numeric_count_is_a_hard_failure(self):
        q = self._query(gold_numeric_stage_count=1)
        with self.assertRaises((ValueError, AssertionError)):
            self.select(q, stage=0, rng=_rng(0))


# ---------------------------------------------------------------------------
# Full batch assembly (deferred) — two point sets, aligned shapes.
# ---------------------------------------------------------------------------

class _DataQuery(_Query):
    """A StageQuery that also serves per-record trajectory data for assembly."""

    def record_keys(self):
        return tuple(sorted(tuple(self._s0) + tuple(self._s1)))

    def get(self, key):
        import numpy as np

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
        import numpy as np
        # Deliberately ends at 9.5 so a per-record times[-1] normalizer is caught.
        return np.linspace(0.0, 9.5, self.n_snapshots(key), dtype=np.float64)

    def snapshot_positions(self, key):
        import numpy as np

        times = self.snapshot_times(key)
        positions = np.zeros((len(times), 3, 3), dtype=np.float64)
        positions[:, 0, 0] = times + key.id / 1000.0
        positions[:, 1, 1] = 2.0 * times
        positions[:, 2, 2] = -times
        return positions

    def snapshot_velocities(self, key):
        import numpy as np

        times = self.snapshot_times(key)
        velocities = np.zeros((len(times), 3, 3), dtype=np.float64)
        velocities[:, 0, 0] = times ** 2
        velocities[:, 1, 1] = times
        return velocities

    def acceleration_magnitudes(self, key):
        import numpy as np

        return np.arange(1, self.n_snapshots(key) + 1, dtype=np.float64)


class FullBatchContract(unittest.TestCase):
    def setUp(self):
        self.mod = importlib.import_module(BATCHES)
        self.build_stage_batch = getattr(self.mod, "build_stage_batch")
        self.sample_data_points = getattr(self.mod, "sample_data_points")
        self.RecordKey = _require("RecordKey", TYPES)
        self.StageLabel = _require("StageLabel", TYPES)

    def _query(self, **over):
        return _DataQuery(self.RecordKey, self.StageLabel, **over)

    def test_batch_emits_two_distinct_point_sets_with_aligned_shapes(self):
        try:
            import torch
        except ImportError as exc:  # pragma: no cover
            raise unittest.SkipTest(f"torch not installed: {exc}")

        query = self._query()
        batch = self.build_stage_batch(
            query, stage=0, rng=_rng(0),
            dtype=torch.float32, device=torch.device("cpu"))
        # Two independent point sets (not one aliased field).
        self.assertIsNot(batch.data_points, batch.collocation_points)
        # Model-facing tensors: last dims 14 ([tau, IC13]) and 3 (raw masses).
        self.assertEqual(batch.data_points.tau_ic13.shape[-1], 14)
        self.assertEqual(batch.data_points.masses.shape[-1], 3)
        self.assertEqual(batch.data_points.targets.shape[-1], 9)
        self.assertEqual(batch.data_points.tau_ic13.shape[0], 256 * 32)
        self.assertEqual(batch.collocation_points.tau_ic13.shape, (4096, 14))
        self.assertEqual(batch.collocation_points.masses.shape, (4096, 3))
        for tensor in (
            batch.data_points.tau_ic13,
            batch.data_points.masses,
            batch.data_points.targets,
            batch.data_points.times,
            batch.collocation_points.times,
            batch.collocation_points.tau_ic13,
            batch.collocation_points.masses,
        ):
            self.assertEqual(tensor.dtype, torch.float32)
            self.assertEqual(tensor.device, torch.device("cpu"))
        # Collocation carries continuous times drawn from the global [0, 10].
        self.assertTrue(float(batch.collocation_points.times.min()) >= 0.0)
        self.assertTrue(float(batch.collocation_points.times.max()) <= 10.0)

    def test_data_sampler_is_mixed_unique_and_globally_time_normalized(self):
        import torch

        query = self._query(n_stage0=240, n_stage1=0)
        selected = tuple(query.records_at(0))
        points = self.sample_data_points(
            query, selected, rng=_rng(8), dtype=torch.float64,
            device=torch.device("cpu"))

        self.assertEqual(len(points.record_keys), 240 * 32)
        for key in selected:
            rows = [i for i, value in enumerate(points.record_keys) if value == key]
            indices = [points.snapshot_indices[i] for i in rows]
            kinds = [points.sampling_kinds[i] for i in rows]
            self.assertEqual(len(indices), 32)
            self.assertEqual(len(set(indices)), 32)
            self.assertEqual(kinds.count("acceleration"), 16)
            self.assertEqual(kinds.count("uniform"), 16)

        expected_tau = 2.0 * (points.times / 10.0) - 1.0
        self.assertTrue(torch.equal(points.tau_ic13[:, 0], expected_tau))
        self.assertAlmostEqual(float(points.tau_ic13[:, 0].max()), 0.9, places=12)

    def test_fixture_ic13_masses_targets_and_provenance_stay_aligned(self):
        import numpy as np
        import torch

        query = self._query(n_stage0=240, n_stage1=0)
        points = self.sample_data_points(
            query, tuple(query.records_at(0)), rng=_rng(3), dtype=torch.float64,
            device=torch.device("cpu"))
        for row in (0, len(points.record_keys) // 2, len(points.record_keys) - 1):
            key = points.record_keys[row]
            snapshot = points.snapshot_indices[row]
            record = query.get(key)
            np.testing.assert_allclose(points.tau_ic13[row, 1:].numpy(), record.ic13)
            np.testing.assert_allclose(points.masses[row].numpy(), record.masses)
            np.testing.assert_allclose(
                points.targets[row].numpy(),
                query.snapshot_positions(key)[snapshot].reshape(9),
            )

    def test_final_assembly_rechecks_blacklist_and_base_set_membership(self):
        import torch

        query = self._query(n_stage0=240, n_stage1=0)
        selected = tuple(query.records_at(0))
        query._black.add((selected[0].variant, selected[0].id))
        with self.assertRaises((ValueError, AssertionError)):
            self.sample_data_points(
                query, selected, rng=_rng(0), dtype=torch.float32,
                device=torch.device("cpu"))

        gold = self.RecordKey("hierarchical", "gold", 9999)
        with self.assertRaises((ValueError, AssertionError, KeyError)):
            self.sample_data_points(
                query, (gold,), rng=_rng(0), dtype=torch.float32,
                device=torch.device("cpu"))

    def test_collocation_quota_metadata_and_seed_reproducibility(self):
        import collections
        import torch

        query = self._query(n_stage0=240, n_stage1=0)
        first = self.build_stage_batch(
            query, stage=0, rng=_rng(11), dtype=torch.float32,
            device=torch.device("cpu"), collocation_count=4096)
        second = self.build_stage_batch(
            query, stage=0, rng=_rng(11), dtype=torch.float32,
            device=torch.device("cpu"), collocation_count=4096)
        a = first.collocation_points
        b = second.collocation_points
        self.assertTrue(torch.equal(a.times, b.times))
        self.assertEqual(a.record_keys, b.record_keys)
        counts = collections.Counter(a.record_keys)
        self.assertEqual(set(counts.values()), {17, 18})
        self.assertEqual(sum(value == 18 for value in counts.values()), 16)
        self.assertEqual(set(a.record_keys), set(first.replay_keys))

    def test_real_network_accepts_model_facing_batch_shapes(self):
        import torch
        from pinn.architecture_spec import ArchitectureSpec
        from pinn.network import build_network

        batch = self.build_stage_batch(
            self._query(), stage=0, rng=_rng(2), dtype=torch.float32,
            device=torch.device("cpu"), collocation_count=64)
        model = build_network(
            ArchitectureSpec(seed=2), dtype=torch.float32, device=torch.device("cpu"))
        output = model(
            batch.data_points.tau_ic13[:8], batch.data_points.masses[:8])
        self.assertEqual(output.shape, (8, 9))

    def test_train_restricted_stage_index_emits_only_train_keys(self):
        import tempfile
        from pathlib import Path
        import torch
        from pinn.data.splits import StageIndex, SplitRatios, write_split_manifest

        source = self._query(n_stage0=300, n_stage1=20)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source.data_root = root / "corpus"
            source.data_root.mkdir()
            manifest = write_split_manifest(
                source, root / "run", seed=17, ratios=SplitRatios())
            train = StageIndex.from_split(source, manifest, "train")
            batch = self.build_stage_batch(
                train, stage=0, rng=_rng(5), dtype=torch.float32,
                device=torch.device("cpu"), collocation_count=256)

        train_keys = set(train.record_keys())
        self.assertTrue(set(batch.replay_keys).issubset(train_keys))
        self.assertTrue(set(batch.lookahead_keys).issubset(train_keys))
        self.assertTrue(set(batch.data_points.record_keys).issubset(train_keys))
        self.assertTrue(set(batch.collocation_points.record_keys).issubset(train_keys))
        self.assertEqual(train.gold_numeric_stage_count, 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
