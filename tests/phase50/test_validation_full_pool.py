"""Phase 50 full-pool validation selector — tracer plus population guards."""

from __future__ import annotations

import tempfile
import unittest

import numpy as np
import torch

from pinn.data.batches import select_stage_records, select_validation_records
from pinn.data.types import (
    PhysicalKey,
    RecordKey,
    StageZeroUnderpopulated,
    ValidationPoolEmpty,
)
from tests.phase50._fixtures import (
    make_minimal_pool_source,
    make_phase50_controller,
)


class ValidationFullPoolTests(unittest.TestCase):
    def test_validation_pool_below_replay_count_no_longer_raises(self):
        """A Stage-0 val pool smaller than replay_count completes with finite terms.

        Pre-repair this path raised DATA-06 StageZeroUnderpopulated because
        ``_run_validation`` routed the held-out split through the training
        replay draw. Observed RED before the repair: StageZeroUnderpopulated
        (Stage-0 population 50 < required 240).
        """
        with tempfile.TemporaryDirectory() as tmp:
            controller = make_phase50_controller(
                tmp, n_train=240, n_validation=50
            )
            weights = controller._scheduled_weights.current(0)
            try:
                terms = controller._run_validation(0, weights)
            except StageZeroUnderpopulated:
                raise
            for name in ("data", "ic", "phys", "energy", "angmom", "total"):
                value = getattr(terms, name)
                self.assertTrue(
                    torch.isfinite(value).all(),
                    f"{name} is not finite: {value}",
                )

    def test_validation_identity_set_is_full_sorted_pool(self):
        """replay_keys equals the full sorted Stage-<=0 validation pool both sides of 240."""
        for n_validation in (50, 300):
            with self.subTest(n_validation=n_validation):
                self.assertNotEqual(n_validation, 240)
                with tempfile.TemporaryDirectory() as tmp:
                    controller = make_phase50_controller(
                        tmp, n_train=250, n_validation=n_validation
                    )
                    batch = controller._validation_batch(
                        stage=0, collocation_count=1
                    )
                    expected = tuple(
                        sorted(
                            controller._validation_source.records_at_or_below(0)
                        )
                    )
                    self.assertEqual(batch.replay_keys, expected)
                    self.assertEqual(len(batch.replay_keys), n_validation)

    def test_validation_selects_no_lookahead_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = make_phase50_controller(
                tmp, n_train=240, n_validation=50, n_validation_stage1=8
            )
            source = controller._validation_source
            self.assertTrue(source.has_stage(1))
            stage1 = tuple(source.records_at(1))
            self.assertGreater(len(stage1), 0)
            batch = controller._validation_batch(stage=0, collocation_count=1)
            self.assertEqual(batch.lookahead_keys, ())
            self.assertFalse(set(stage1) & set(batch.replay_keys))

    def test_repeated_validation_events_select_identical_identities(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = make_phase50_controller(
                tmp, n_train=240, n_validation=50
            )
            first = controller._validation_batch(stage=0, collocation_count=1)
            controller._rng.random(64)
            second = controller._validation_batch(stage=0, collocation_count=1)
            self.assertEqual(first.replay_keys, second.replay_keys)
            self.assertEqual(first.lookahead_keys, ())
            self.assertEqual(second.lookahead_keys, ())

    def test_train_path_still_draws_replay_and_lookahead_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = make_phase50_controller(
                tmp, n_train=300, n_validation=50, n_train_stage1=16
            )
            self.assertGreater(len(controller._train_source.records_at_or_below(0)), 240)
            self.assertTrue(controller._train_source.has_stage(1))
            batch = controller._stage_batch(
                controller._train_source, stage=0, collocation_count=1
            )
            self.assertEqual(len(batch.replay_keys), 240)
            self.assertEqual(len(set(batch.replay_keys)), 240)
            self.assertEqual(len(batch.lookahead_keys), 16)

    def test_empty_validation_pool_raises_validation_pool_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = make_phase50_controller(
                tmp, n_train=240, n_validation=0, n_validation_stage1=0
            )
            with self.assertRaises(ValidationPoolEmpty) as ctx:
                controller._validation_batch(stage=0, collocation_count=1)
            self.assertEqual(ctx.exception.stage, 0)

    def test_validation_pool_rejects_blacklisted_and_non_set1a_keys(self):
        clean = RecordKey("hierarchical", "base", 1)
        blacklisted_key = RecordKey("hierarchical", "base", 2)
        gold_key = RecordKey("hierarchical", "gold", 3)
        rng = np.random.default_rng(0)

        blacklisted_source = make_minimal_pool_source(
            (clean, blacklisted_key),
            blacklisted=(PhysicalKey("hierarchical", 2),),
        )
        with self.assertRaises(ValueError):
            select_validation_records(blacklisted_source, stage=0)
        with self.assertRaises(ValueError):
            select_stage_records(blacklisted_source, stage=0, rng=rng)

        non_set1a_source = make_minimal_pool_source((clean, gold_key))
        with self.assertRaises(ValueError):
            select_validation_records(non_set1a_source, stage=0)
        with self.assertRaises(ValueError):
            select_stage_records(non_set1a_source, stage=0, rng=np.random.default_rng(1))


if __name__ == "__main__":
    unittest.main()
