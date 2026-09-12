"""57-07 band-generation-2 scope brief §3 -- the resource preflight that did
not exist. ``57-05-PLAN.md`` Task 3 requires an "exact-4096 resource
preflight ... abort rather than reduce it if resource preflight fails."
No such check previously existed anywhere in the codebase; generation 1
discovered its memory ceiling by spending 851.9s inside the real training
loop (``blocked-state.json``). ``run_microbatch_memory_preflight`` makes
that discovery a fast, typed refusal, exercised here against an injected
fake memory signal (never the real ``torch.mps`` API) so this test is
platform-independent.
"""

from __future__ import annotations

import copy
import tempfile
import unittest

from pinn.conformance.preflight import (
    ConformancePreflightError,
    run_microbatch_memory_preflight,
)
from pinn.training.guards import StepGuards
from tests.phase40.test_optimizer_phase import _build_controller


class ResourceMemoryPreflightTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def _controller(self, *, collocation_count=64):
        return _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1,
            collocation_count=collocation_count,
        )

    def test_passes_and_reports_fraction_under_watermark(self):
        controller = self._controller()
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: 100,
        )
        result = run_microbatch_memory_preflight(
            controller, controller._config, step_guards=step_guards,
        )
        self.assertTrue(result["passed"])
        self.assertAlmostEqual(result["measured_fraction"], 0.1)

    def test_refuses_with_typed_error_naming_measured_fraction(self):
        controller = self._controller()
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: 950,
        )
        with self.assertRaises(ConformancePreflightError) as ctx:
            run_microbatch_memory_preflight(
                controller, controller._config, step_guards=step_guards,
            )
        message = str(ctx.exception)
        self.assertIn("0.95", message)
        self.assertIn(str(int(controller._config.opt.adam_microbatch_size)), message)

    def test_skips_gracefully_when_memory_signal_unavailable(self):
        controller = self._controller()
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: None,
        )
        result = run_microbatch_memory_preflight(
            controller, controller._config, step_guards=step_guards,
        )
        self.assertTrue(result["passed"])
        self.assertNotIn("measured_fraction", result)

    def test_probe_does_not_perturb_the_run_rng_or_leave_stray_gradients(self):
        """The probe must be invisible to the real run: identical RNG state
        and record draw before/after, and no gradients left over `.grad`."""
        controller = self._controller()
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: 100,
        )
        pre_state = copy.deepcopy(controller._rng.bit_generator.state)
        run_microbatch_memory_preflight(
            controller, controller._config, step_guards=step_guards,
        )
        post_state = controller._rng.bit_generator.state
        self.assertEqual(pre_state, post_state)
        for p in controller._model.parameters():
            self.assertIsNone(p.grad)

        # The real first draw is identical to a run that never called the
        # preflight at all -- reconstruct a sibling controller from a fresh
        # generator seeded identically and compare the drawn batch's keys.
        sibling = self._controller()
        real_batch = controller._stage_batch(
            controller._train_source, stage=0, collocation_count=64,
        )
        sibling_batch = sibling._stage_batch(
            sibling._train_source, stage=0, collocation_count=64,
        )
        self.assertEqual(
            real_batch.data_points.record_keys,
            sibling_batch.data_points.record_keys,
        )


if __name__ == "__main__":
    unittest.main()
