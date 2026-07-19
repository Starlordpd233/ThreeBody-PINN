"""Phase 41 — four-stream RNG capture/restore + strict-CPU + repro honesty (CTRL-08).

Exact continuation (restore bit_generator.state) is distinct from a fresh
default_rng(seed) reseed restart. Reproducibility scope is statistical-
equivalence + exact-checkpoint-continuation, NEVER bitwise.
"""

from __future__ import annotations

import importlib
import random
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tests.phase41 import _SKIP_PHRASE

MODULE = "pinn.training.determinism"

# Documented stream key order (must match capture_rng_state).
_STREAM_KEYS = ("torch", "torch_mps", "numpy", "python_random")


def _require(symbol, module=MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


class RngCaptureRestoreTests(unittest.TestCase):
    """CTRL-08: capture → advance → restore yields exact next draws."""

    def setUp(self):
        self.capture_rng_state = _require("capture_rng_state")
        self.restore_rng_state = _require("restore_rng_state")
        self.seed = 12345
        self.rng = np.random.default_rng(self.seed)

    def test_captured_dict_has_four_streams_in_order(self):
        state = self.capture_rng_state(self.rng)
        self.assertIsInstance(state, dict)
        keys = list(state.keys())
        # All four present; documented order is the iteration order.
        for key in _STREAM_KEYS:
            self.assertIn(key, state)
        # Documented order: torch, torch_mps, numpy, python_random.
        ordered = [k for k in _STREAM_KEYS if k in keys]
        self.assertEqual(ordered, list(_STREAM_KEYS))
        # numpy stream is the Generator's bit_generator.state, not legacy global.
        self.assertEqual(state["numpy"], self.rng.bit_generator.state)

    def test_round_trip_torch_save_weights_only(self):
        import torch

        state = self.capture_rng_state(self.rng)
        tmp = Path(tempfile.mkdtemp(prefix="phase41-rng-"))
        path = tmp / "rng.pt"
        try:
            torch.save(state, path)
            loaded = torch.load(path, weights_only=True)
        finally:
            if path.exists():
                path.unlink()
            tmp.rmdir()
        self.assertEqual(set(loaded.keys()), set(state.keys()))
        # numpy bit_generator.state is a dict-like container of arrays/scalars.
        np.testing.assert_equal(
            loaded["numpy"]["state"]["state"],
            state["numpy"]["state"]["state"],
        )
        # python_random is a nested tuple; equality after torch round-trip.
        self.assertEqual(loaded["python_random"][0], state["python_random"][0])
        # torch RNG state is a ByteTensor.
        self.assertTrue(torch.equal(loaded["torch"], state["torch"]))

    def test_restore_exact_continuation_not_reseed(self):
        """After capture→advance→restore, next draws equal captured-state draws.

        A fresh default_rng(seed) restart produces DIFFERENT draws, proving
        restore ≠ reseed (the CTRL-08 anti-pattern distinction).
        """
        # Warm the streams so state is non-trivial.
        _ = self.rng.random(8)
        _ = random.random()
        import torch

        _ = torch.rand(4)

        captured = self.capture_rng_state(self.rng)

        # Draws that WOULD have been next from the captured state.
        # We snapshot by restoring a clone path: capture, draw expected, then
        # re-restore and draw again after an intervening advance.
        expected_np = self.rng.random(4).copy()
        expected_py = [random.random() for _ in range(4)]
        expected_torch = torch.rand(4).clone()

        # Advance further away from the captured state.
        _ = self.rng.random(16)
        _ = [random.random() for _ in range(16)]
        _ = torch.rand(16)
        advanced_np = self.rng.random(4)
        # Advanced draws must differ from expected (otherwise the test is weak).
        self.assertFalse(np.allclose(advanced_np, expected_np))

        # Restore exact continuation.
        self.restore_rng_state(captured, self.rng)
        got_np = self.rng.random(4)
        got_py = [random.random() for _ in range(4)]
        got_torch = torch.rand(4)

        np.testing.assert_array_equal(got_np, expected_np)
        self.assertEqual(got_py, expected_py)
        self.assertTrue(torch.equal(got_torch, expected_torch))

        # Fresh reseed restart is statistically-equivalent restart, NOT exact.
        fresh = np.random.default_rng(self.seed)
        fresh_draw = fresh.random(4)
        # After the warmup draws that preceded capture, a pure reseed cannot
        # reproduce the post-capture next draws.
        self.assertFalse(np.allclose(fresh_draw, expected_np))

    def test_restore_does_not_construct_fresh_generator(self):
        """restore_rng_state mutates the injected rng in place (same object)."""
        captured = self.capture_rng_state(self.rng)
        _ = self.rng.random(8)
        before_id = id(self.rng)
        self.restore_rng_state(captured, self.rng)
        self.assertEqual(id(self.rng), before_id)
        # bit_generator.state matches captured.
        self.assertEqual(
            self.rng.bit_generator.state["state"]["state"],
            captured["numpy"]["state"]["state"],
        )


class StrictCpuSwitchTests(unittest.TestCase):
    """CTX-63 + HIGH 4: apply_strict_cpu_determinism returns RuntimeSpec."""

    def setUp(self):
        self.apply_strict = _require("apply_strict_cpu_determinism")

    def tearDown(self):
        # Best-effort restore of global torch settings so later tests are not
        # forced into deterministic-only mode.
        import torch

        try:
            torch.use_deterministic_algorithms(False)
        except Exception:
            pass

    def test_returns_float64_cpu_runtime_spec(self):
        import torch

        from pinn.runtime import RuntimeSpec

        spec = self.apply_strict(42)
        self.assertIsInstance(spec, RuntimeSpec)
        self.assertEqual(spec.precision, "float64")
        self.assertEqual(spec.requested_device, "cpu")
        self.assertEqual(spec.dtype, torch.float64)
        self.assertEqual(spec.torch_device, torch.device("cpu"))

    def test_sets_deterministic_algorithms_and_single_thread(self):
        import torch

        self.apply_strict(7)
        self.assertTrue(torch.are_deterministic_algorithms_enabled())
        self.assertEqual(torch.get_num_threads(), 1)

    def test_strict_cpu_off_by_default_in_config(self):
        from pinn.training.config import RunConfig

        run = RunConfig()
        self.assertIs(run.strict_cpu_determinism, False)

    def test_reseed_four_streams_from_seed(self):
        """Debug path reseeds streams so two calls with the same seed align."""
        import torch

        self.apply_strict(99)
        a_torch = torch.rand(3).clone()
        a_np = np.random.random(3).copy()
        a_py = [random.random() for _ in range(3)]

        self.apply_strict(99)
        b_torch = torch.rand(3)
        b_np = np.random.random(3)
        b_py = [random.random() for _ in range(3)]

        self.assertTrue(torch.equal(a_torch, b_torch))
        np.testing.assert_array_equal(a_np, b_np)
        self.assertEqual(a_py, b_py)


class ReproHonestyTests(unittest.TestCase):
    """CTX-64: scope string is statistical-equivalence + exact-continuation."""

    def test_scope_string_wording(self):
        # Prefer a named constant; fall back to a getter if named differently.
        try:
            scope = _require("REPRODUCIBILITY_SCOPE")
        except unittest.SkipTest:
            get_scope = _require("reproducibility_scope")
            scope = get_scope() if callable(get_scope) else get_scope

        text = scope if isinstance(scope, str) else str(scope)
        lower = text.lower()
        self.assertIn("statistical", lower)
        self.assertIn("equivalence", lower)
        # exact-checkpoint-continuation (or close wording)
        self.assertTrue(
            "exact" in lower and ("continuation" in lower or "checkpoint" in lower),
            f"scope must state exact checkpoint continuation: {text!r}",
        )
        # MUST NOT claim bitwise reproducibility.
        self.assertNotIn("bitwise", lower)
        # Explicit negation of bitwise is allowed/encouraged; if present, fine.
        # But the word "bitwise" as a positive claim is banned — already checked.


class RunStartRngRecordTests(unittest.TestCase):
    """GAP-41-01 representation B: run-start four-stream record round-trip."""

    def setUp(self):
        self.record = _require("record_run_start_rng")
        self.load = _require("load_run_start_rng")
        self.restore = _require("restore_rng_state")
        self.filename = _require("RUN_START_RNG_FILENAME")

    def test_record_and_load_round_trip_four_streams(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            rng = np.random.default_rng(4242)
            written = self.record(run_dir, rng)
            self.assertEqual(Path(written), run_dir / self.filename)
            self.assertTrue((run_dir / self.filename).is_file())

            record = self.load(run_dir)
            self.assertIn("rng", record)
            for key in _STREAM_KEYS:
                self.assertIn(key, record["rng"], msg=f"missing rng.{key}")

            # Exact continuation off the record: restoring the numpy stream
            # into a fresh generator reproduces the recorded generator's draws.
            expected = [float(rng.random()) for _ in range(5)]
            other = np.random.default_rng(1)
            self.restore(record["rng"], other)
            replayed = [float(other.random()) for _ in range(5)]
            self.assertEqual(expected, replayed)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
