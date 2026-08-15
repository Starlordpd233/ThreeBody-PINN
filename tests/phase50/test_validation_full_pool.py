"""Phase 50 full-pool validation selector — tracer plus population guards."""

from __future__ import annotations

import tempfile
import unittest

import torch

from pinn.data.types import StageZeroUnderpopulated
from tests.phase50._fixtures import make_phase50_controller


class ValidationFullPoolTests(unittest.TestCase):
    def test_validation_pool_below_replay_count_no_longer_raises(self):
        """A Stage-0 val pool smaller than replay_count completes with finite terms.

        Pre-repair this path raised DATA-06 StageZeroUnderpopulated because
        ``_run_validation`` routed the held-out split through the training
        replay draw. Observed RED before the repair: StageZeroUnderpopulated.
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


if __name__ == "__main__":
    unittest.main()
