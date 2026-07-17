"""Contract tests for the merged Adam-only gradient clipper (TRAIN-05).

Authored first (RED -> skip) per plan 40-02 Task 2. Each test defers the
production import through ``_require`` so the suite stays green (localized
skip with ``_SKIP_PHRASE``) until ``pinn.training.grad_clip`` lands.

Median semantics are load-bearing: every reference in this file is built with
``torch.median`` (NEVER ``numpy.median`` / ``statistics.median``).
``torch.median`` of an even-length window returns the LOWER of the two middle
values; the averaging numpy/statistics variants would disagree on even-length
windows and must not be substituted.
"""

from __future__ import annotations

import importlib
import unittest

import torch

from tests.phase40 import _SKIP_PHRASE

MODULE = "pinn.training.grad_clip"

# PROVISIONAL C_stage table (CTX-34; pinn_architecture.md §4.4 Stage 0-1 spec
# range 7-10; stages 2-3 inherit the pre-Phase-34 fixed multiplier 5.0;
# stages 4-6 use 3.0). Never cited as ratified -- surfaced for ACC-05.
C_STAGE_TABLE = {0: 8.5, 1: 8.5, 2: 5.0, 3: 5.0, 4: 3.0, 5: 3.0, 6: 3.0}


def _require(symbol: str):
    """Deferred import -- SkipTest (never ERROR) until the symbol lands."""
    try:
        mod = importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}") from exc
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}")
    return getattr(mod, symbol)


def _set_grad(param: torch.nn.Parameter, norm: float, *, dtype=torch.float64) -> None:
    """Set ``param.grad`` to a length-2 vector with L2 norm == ``norm``."""
    param.grad = torch.tensor([norm, 0.0], dtype=dtype)


class GradClipTests(unittest.TestCase):
    """§4.4 median clip formula + partial-window + floor + non-finite contract."""

    def _make_param(self, dtype=torch.float64):
        # A parameter whose grad we set by hand to drive known L2 norms.
        return torch.nn.Parameter(torch.zeros(2, dtype=dtype))

    # -- clip_value == C_stage * torch.median(history) for every stage --------

    def test_clip_formula_per_stage_matches_torch_median_reference(self):
        GradClipper = _require("GradClipper")
        for stage in range(7):
            with self.subTest(stage=stage):
                clipper = GradClipper()
                p = self._make_param()
                # Drive five known norms; build the reference with torch.median.
                norms = [3.0, 4.0, 5.0, 6.0, 7.0]
                ref_history = []
                for norm in norms:
                    _set_grad(p, norm)
                    outcome = clipper.clip([p], stage=stage)
                    ref_history.append(norm)
                    # Reference: C_stage * torch.median(stack(history)). NEVER
                    # numpy/statistics.median -- those average even-length windows
                    # and would disagree (torch.median returns the LOWER middle).
                    ref_stack = torch.tensor(ref_history, dtype=torch.float64)
                    expected = C_STAGE_TABLE[stage] * float(torch.median(ref_stack))
                    self.assertAlmostEqual(
                        float(outcome.clip_value), expected, places=6,
                        msg=f"stage {stage} norm {norm}: clip_value != C*median")
                    self.assertFalse(outcome.non_finite)
                    self.assertIsNotNone(outcome.clip_value)

    def test_default_c_stage_table_matches_provisional_table(self):
        GradClipper = _require("GradClipper")
        # The clipper's default C_stage table is the provisional CTX-34 set.
        # Read it via the module-level constant if exposed, else via construction.
        mod = importlib.import_module(MODULE)
        if hasattr(mod, "DEFAULT_C_STAGE_TABLE"):
            self.assertEqual(
                dict(mod.DEFAULT_C_STAGE_TABLE), C_STAGE_TABLE,
                "default C_stage table must match the provisional CTX-34 set")

    # -- Even-length window: torch.median LOWER-middle semantics -----------

    def test_even_length_window_uses_torch_median_lower_middle(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        p = self._make_param()
        # Drive an even-length window of four known norms.
        norms = [10.0, 20.0, 30.0, 40.0]
        ref_history = []
        for norm in norms:
            _set_grad(p, norm)
            outcome = clipper.clip([p], stage=0)
            ref_history.append(norm)
        # torch.median([10,20,30,40]) == 20 (LOWER middle). A numpy.median /
        # statistics.median reference would average to 25 and FAIL this.
        ref_stack = torch.tensor(ref_history, dtype=torch.float64)
        expected = C_STAGE_TABLE[0] * float(torch.median(ref_stack))
        self.assertEqual(float(torch.median(ref_stack)), 20.0)
        self.assertAlmostEqual(float(outcome.clip_value), expected, places=6)
        self.assertAlmostEqual(float(outcome.clip_value), 8.5 * 20.0, places=6)

    # -- Partial-window backstop (SPEC held-out edge) ----------------------

    def test_length_one_window_clip_equals_c_times_single_norm(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        p = self._make_param()
        _set_grad(p, 5.0)
        outcome = clipper.clip([p], stage=2)
        # CTX-35 length-1 identity: clip = C_stage * the single norm.
        self.assertEqual(outcome.window_len, 1)
        self.assertAlmostEqual(float(outcome.clip_value), 5.0 * 5.0, places=6)

    def test_partial_window_length_two_and_four_finite_and_defined(self):
        GradClipper = _require("GradClipper")
        for lengths in ([2.0, 8.0], [1.0, 2.0, 3.0, 4.0]):
            with self.subTest(lengths=lengths):
                clipper = GradClipper()
                p = self._make_param()
                last = None
                for norm in lengths:
                    _set_grad(p, norm)
                    last = clipper.clip([p], stage=0)
                # Finite and defined for every partial window < 100 entries.
                self.assertIsNotNone(last.clip_value)
                self.assertTrue(
                    torch.isfinite(torch.tensor(float(last.clip_value))).all())
                self.assertEqual(last.window_len, len(lengths))
                # Matches the torch.median reference (LOWER middle for even len).
                ref = C_STAGE_TABLE[0] * float(
                    torch.median(torch.tensor(lengths, dtype=torch.float64)))
                self.assertAlmostEqual(float(last.clip_value), ref, places=6)

    # -- Median floor (CTX-36): never collapses clip to 0 -------------------

    def test_median_floor_engages_when_window_median_below_floor(self):
        GradClipper = _require("GradClipper")
        # Custom floor above the injected norms -> effective median == floor.
        clipper = GradClipper(median_floor=10.0)
        p = self._make_param()
        for norm in [1.0, 2.0, 3.0]:
            _set_grad(p, norm)
            outcome = clipper.clip([p], stage=0)
        # torch.median([1,2,3]) == 2 < 10 -> effective median = 10 -> clip = 8.5*10.
        self.assertAlmostEqual(float(outcome.clip_value), 8.5 * 10.0, places=6)

    def test_default_floor_keeps_clip_nonzero_for_tiny_norms(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()  # default median_floor = 1e-6 (CTX-36)
        p = self._make_param()
        _set_grad(p, 1e-12)
        outcome = clipper.clip([p], stage=0)
        # Window median (1e-12) below default floor (1e-6) -> effective = 1e-6.
        self.assertAlmostEqual(float(outcome.clip_value), 8.5 * 1e-6, places=12)
        self.assertGreater(float(outcome.clip_value), 0.0)

    # -- clear() resets the window at a stage boundary (CTX-37) ------------

    def test_clear_resets_window_to_fresh_length_one_bootstrap(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        p = self._make_param()
        for norm in [3.0, 4.0, 5.0]:
            _set_grad(p, norm)
            clipper.clip([p], stage=0)
        clipper.clear()
        # Next clip starts a fresh length-1 bootstrap (new stage's gradient scale).
        _set_grad(p, 7.0)
        outcome = clipper.clip([p], stage=2)
        self.assertEqual(outcome.window_len, 1)
        self.assertAlmostEqual(float(outcome.clip_value), 5.0 * 7.0, places=6)

    # -- M1 non-finite contract: returned flag, never a raise ----------------

    def test_nan_grad_returns_non_finite_flag_without_raising(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        p = self._make_param()
        # Seed the window with a finite norm.
        _set_grad(p, 5.0)
        seeded = clipper.clip([p], stage=0)
        self.assertEqual(seeded.window_len, 1)
        self.assertFalse(seeded.non_finite)
        # NaN grad: clip() MUST NOT raise; returns non_finite flag, clip_value None.
        p.grad = torch.tensor([float("nan"), 1.0], dtype=torch.float64)
        outcome = clipper.clip([p], stage=0)  # no exception escapes
        self.assertTrue(outcome.non_finite)
        self.assertIsNone(outcome.clip_value)
        # Window length UNCHANGED -- the NaN was never appended.
        self.assertEqual(outcome.window_len, 1)

    def test_inf_grad_returns_non_finite_flag_without_raising(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        p = self._make_param()
        _set_grad(p, 5.0)
        clipper.clip([p], stage=0)
        # Inf grad: same contract -- flag, no clip, no raise, window unchanged.
        p.grad = torch.tensor([float("inf"), 1.0], dtype=torch.float64)
        outcome = clipper.clip([p], stage=0)
        self.assertTrue(outcome.non_finite)
        self.assertIsNone(outcome.clip_value)
        self.assertEqual(outcome.window_len, 1)

    def test_finite_step_after_non_finite_uses_uncontaminated_window(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        p = self._make_param()
        _set_grad(p, 5.0)
        clipper.clip([p], stage=0)
        # Non-finite event (must not poison the window).
        p.grad = torch.tensor([float("nan"), 0.0], dtype=torch.float64)
        nan_outcome = clipper.clip([p], stage=0)
        self.assertTrue(nan_outcome.non_finite)
        self.assertEqual(nan_outcome.window_len, 1)
        # Following finite step: finite clip from the uncontaminated [5.0] window.
        _set_grad(p, 7.0)
        outcome = clipper.clip([p], stage=0)
        self.assertFalse(outcome.non_finite)
        self.assertIsNotNone(outcome.clip_value)
        self.assertEqual(outcome.window_len, 2)  # [5.0, 7.0]
        # torch.median([5, 7]) == 5 (LOWER middle); clip = 8.5 * 5 = 42.5.
        self.assertAlmostEqual(float(outcome.clip_value), 8.5 * 5.0, places=6)

    # -- Single public entry point; Adam-only by construction ----------------

    def test_clip_is_only_per_step_entry_point_no_lbfgs_surface(self):
        GradClipper = _require("GradClipper")
        # clip(params, *, stage) is the single per-step entry point; the spy in
        # plan 40-05 targets GradClipper.clip (count = 1 per Adam step).
        self.assertTrue(hasattr(GradClipper, "clip"))
        # No L-BFGS / closure entry point exists (Adam-only by construction).
        for banned in ("clip_lbfgs", "lbfgs_clip", "step_closure",
                       "closure_clip", "lbfgs_step"):
            self.assertFalse(
                hasattr(GradClipper, banned),
                f"GradClipper exposes a forbidden L-BFGS/closure entry point: {banned}")
        # clear() is the stage-boundary maintenance primitive (not per-step).
        self.assertTrue(hasattr(GradClipper, "clear"))

    def test_clip_signature_takes_stage_keyword(self):
        GradClipper = _require("GradClipper")
        import inspect
        sig = inspect.signature(GradClipper.clip)
        self.assertIn("params", sig.parameters)
        self.assertIn("stage", sig.parameters)
        # stage is keyword-only (per the plan: clip(params, *, stage)).
        self.assertTrue(sig.parameters["stage"].kind == inspect.Parameter.KEYWORD_ONLY)

    # -- GradClipOutcome frozen-result shape ---------------------------------

    def test_grad_clip_outcome_is_frozen_with_required_fields(self):
        GradClipOutcome = _require("GradClipOutcome")
        outcome = GradClipOutcome(non_finite=False, clip_value=1.0,
                                  total_norm=torch.tensor(2.0),
                                  window_len=3)
        # Frozen: mutation raises.
        from dataclasses import FrozenInstanceError
        with self.assertRaises(FrozenInstanceError):
            outcome.non_finite = True  # type: ignore[misc]
        # Required fields present.
        for field in ("non_finite", "clip_value", "total_norm", "window_len"):
            self.assertTrue(
                hasattr(outcome, field),
                f"GradClipOutcome missing required field {field!r}")


class GradClipCheckpointRoundTripTests(unittest.TestCase):
    """WR-01: state_dict / load_state_dict preserves the run's window dtype.

    Pre-fix ``load_state_dict`` hardcodes ``dtype=torch.float64`` for every
    restored entry, which silently corrupts an fp32-MPS production resume
    (D1-p). These tests are the first coverage of the checkpoint path in
    either dtype.
    """

    def _populate(self, clipper, *, dtype, norms):
        p = torch.nn.Parameter(torch.zeros(2, dtype=dtype))
        for norm in norms:
            _set_grad(p, norm, dtype=dtype)
            clipper.clip([p], stage=0)
        return p

    def test_float32_round_trip_preserves_window_dtype_and_values(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        norms = [3.0, 4.0, 5.0]
        self._populate(clipper, dtype=torch.float32, norms=norms)
        pre_values = [float(v) for v in clipper._window]
        pre_table = dict(clipper._c_stage_table)
        pre_floor = clipper._median_floor
        pre_len = clipper._window_length

        state = clipper.state_dict()
        # Payload must carry dtype as a plain string (weights_only-clean).
        self.assertIn("dtype", state)
        self.assertIsInstance(state["dtype"], str)
        self.assertEqual(state["dtype"], "float32")

        restored = GradClipper()
        restored.load_state_dict(state)

        self.assertEqual(len(restored._window), len(norms))
        for entry in restored._window:
            self.assertEqual(
                entry.dtype, torch.float32,
                f"restored window entry has dtype {entry.dtype}, expected float32")
        self.assertTrue(
            torch.allclose(
                torch.stack(restored._window),
                torch.tensor(pre_values, dtype=torch.float32),
            ),
            "restored window values must match pre-save values",
        )
        self.assertEqual(dict(restored._c_stage_table), pre_table)
        self.assertEqual(restored._median_floor, pre_floor)
        self.assertEqual(restored._window_length, pre_len)

    def test_float32_clip_after_resume_matches_torch_median_reference(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        norms = [3.0, 4.0, 5.0]
        p = self._populate(clipper, dtype=torch.float32, norms=norms)
        state = clipper.state_dict()

        restored = GradClipper()
        restored.load_state_dict(state)

        # One more clip after resume; reference includes the appended norm.
        _set_grad(p, 6.0, dtype=torch.float32)
        outcome = restored.clip([p], stage=0)
        self.assertFalse(outcome.non_finite)
        ref_history = norms + [6.0]
        ref_stack = torch.tensor(ref_history, dtype=torch.float32)
        expected = C_STAGE_TABLE[0] * float(torch.median(ref_stack))
        self.assertAlmostEqual(float(outcome.clip_value), expected, places=5)
        # Window must stay dtype-homogeneous after the post-resume append.
        for entry in restored._window:
            self.assertEqual(entry.dtype, torch.float32)

    def test_float64_round_trip_preserves_window_dtype(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        self._populate(clipper, dtype=torch.float64, norms=[2.0, 8.0, 4.0])
        state = clipper.state_dict()
        self.assertEqual(state["dtype"], "float64")

        restored = GradClipper()
        restored.load_state_dict(state)
        for entry in restored._window:
            self.assertEqual(entry.dtype, torch.float64)
        self.assertTrue(
            torch.allclose(
                torch.stack(restored._window),
                torch.tensor([2.0, 8.0, 4.0], dtype=torch.float64),
            ))

    def test_empty_window_round_trips_without_dtype(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        self._populate(clipper, dtype=torch.float32, norms=[1.0, 2.0])
        clipper.clear()
        state = clipper.state_dict()
        restored = GradClipper()
        restored.load_state_dict(state)
        self.assertEqual(restored._window, [])
        self.assertEqual(restored._window_length, clipper._window_length)

    def test_unknown_dtype_string_raises_value_error_naming_it(self):
        GradClipper = _require("GradClipper")
        clipper = GradClipper()
        self._populate(clipper, dtype=torch.float32, norms=[1.0])
        state = clipper.state_dict()
        state["dtype"] = "float16"  # outside the closed 2-entry set
        restored = GradClipper()
        with self.assertRaises(ValueError) as ctx:
            restored.load_state_dict(state)
        self.assertIn("float16", str(ctx.exception))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
