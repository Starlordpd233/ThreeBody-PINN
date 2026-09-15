"""57-07 band-generation-2 scope brief §3 -- the resource preflight that did
not exist. ``57-05-PLAN.md`` Task 3 requires an "exact-4096 resource
preflight ... abort rather than reduce it if resource preflight fails."
No such check previously existed anywhere in the codebase; generation 1
discovered its memory ceiling by spending 851.9s inside the real training
loop (``blocked-state.json``). ``run_microbatch_memory_preflight`` makes
that discovery a fast, typed refusal, exercised here against an injected
fake memory signal (never the real ``torch.mps`` API) so this test is
platform-independent. GAP-57-05 adds an injected fake peak-footprint
signal on the same terms; ``FootprintReaderTests`` is the one
real-platform read.
"""

from __future__ import annotations

import copy
import sys
import tempfile
import time
import unittest

from pinn.conformance.preflight import (
    ConformancePreflightError,
    _process_phys_footprint_bytes,
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
            footprint_signal=lambda: None,
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
                footprint_signal=lambda: None,
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
            footprint_signal=lambda: None,
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
            footprint_signal=lambda: None,
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

    def test_refuses_when_peak_footprint_exceeds_watermark(self):
        """GAP-57-05: a spike the post-step MPS counter misses must still refuse."""
        controller = self._controller()
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: 100,
        )
        with self.assertRaises(ConformancePreflightError) as ctx:
            run_microbatch_memory_preflight(
                controller, controller._config, step_guards=step_guards,
                footprint_signal=lambda: 950,
            )
        message = str(ctx.exception)
        self.assertIn("peak physical footprint", message)
        self.assertIn("0.95", message)

    def test_reports_peak_footprint_under_watermark(self):
        controller = self._controller()
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: 100,
        )
        result = run_microbatch_memory_preflight(
            controller, controller._config, step_guards=step_guards,
            footprint_signal=lambda: 300,
        )
        self.assertTrue(result["passed"])
        self.assertEqual(result["peak_footprint_bytes"], 300)
        self.assertAlmostEqual(result["peak_footprint_fraction"], 0.3)

    def test_monitor_memory_counts_toward_the_peak_and_its_stash_is_restored(self):
        """GAP-57-05: the per-epoch monitor evaluation runs inside the sampled
        window, and the probe leaves the monitor stash exactly as it found it."""
        controller = self._controller()
        sentinel = {"w_n_stats": {"front_idx": -7}}
        controller._last_front_monitor_stats = sentinel
        monitor = {"ran": False}

        def monitor_spy():
            monitor["ran"] = True
            controller._last_front_monitor_stats = {"overwritten": True}
            return controller._last_front_monitor_stats

        controller._evaluate_front_monitor = monitor_spy
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: 100,
        )
        with self.assertRaises(ConformancePreflightError):
            run_microbatch_memory_preflight(
                controller, controller._config, step_guards=step_guards,
                footprint_signal=lambda: 950 if monitor["ran"] else 100,
            )
        self.assertTrue(monitor["ran"])
        self.assertIs(controller._last_front_monitor_stats, sentinel)

    def test_a_spike_released_before_the_window_ends_is_still_caught(self):
        """The failure mode is a transient allocation; the sampler must see it
        even when the memory is gone by the time the probe returns."""
        controller = self._controller()
        spike = {"active": False}

        def monitor_spy():
            spike["active"] = True
            time.sleep(0.5)  # ten sampling intervals
            spike["active"] = False

        controller._evaluate_front_monitor = monitor_spy
        step_guards = StepGuards(
            controller._config, memory_total_bytes=1000, memory_signal=lambda: 100,
        )
        with self.assertRaises(ConformancePreflightError):
            run_microbatch_memory_preflight(
                controller, controller._config, step_guards=step_guards,
                footprint_signal=lambda: 950 if spike["active"] else 100,
            )


class FootprintReaderTests(unittest.TestCase):
    """The one real-platform read in this file: a mis-laid-out
    ``rusage_info_v2`` would silently return a different counter, so the
    reader is checked against a known allocation wherever it can run."""

    @unittest.skipUnless(sys.platform == "darwin", "phys_footprint is a macOS counter")
    def test_current_footprint_rises_and_falls_with_a_touched_allocation(self):
        before = _process_phys_footprint_bytes()
        block = bytearray(256 * 2**20)
        block[::4096] = b"1" * len(block[::4096])
        touched = _process_phys_footprint_bytes()
        del block
        freed = _process_phys_footprint_bytes()
        self.assertGreaterEqual(touched - before, 200 * 2**20)
        # A lifetime-maximum field would rise but never fall.
        self.assertGreaterEqual(touched - freed, 200 * 2**20)

    @unittest.skipIf(sys.platform == "darwin", "exercises the non-macOS branch")
    def test_reader_reports_unavailable_off_macos(self):
        self.assertIsNone(_process_phys_footprint_bytes())


if __name__ == "__main__":
    unittest.main()
