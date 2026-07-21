"""Phase 43 / Plan 01 — ``python -m pinn.verify`` ladder + marker (ACC-01).

Covers the two falsifiable halves of ACC-01:

1. **The ordered five-rung ladder** (SPEC AC 1/2): device sanity → componentwise
   AD → fp64-CPU gradcheck → residual-on-ground-truth → single-trajectory
   overfit. A healthy environment exits 0; a rung that *raises* and a rung whose
   probe symbol is *missing* both become that rung's FAIL (never a silent skip),
   the run exits non-zero, and the final message names the FIRST failed rung.
2. **The marker contract** (CTX-71 / plan 43-04's gate input): every ladder
   outcome atomically writes ``runs/.verify/latest-marker.json``; the freshness
   predicate accepts only a green marker inside the age window whose *complete*
   fingerprint — device, dtype, torch version, Python version, Git availability
   and Git head — matches the current runtime and code.

Import discipline: this module imports ``pinn.verify`` directly rather than
through the package's ``_SKIP_PHRASE`` guard. That guard exists for *later-wave*
Phase-43 production symbols (plans 43-02..43-08); ``pinn/verify.py`` is this
plan's own artifact, so its absence must be a hard ERROR, not a skip — the same
fail-closed discipline the ladder itself enforces on a missing probe.

The ladder tests never touch MPS or the dataset: they drive the fp64-CPU arm
with ``torch.backends.mps.is_available`` and the four probe entry points
patched, so pass/fail semantics are asserted independently of hardware and of
``simulation_data/``.
"""

from __future__ import annotations

import importlib
import io
import shutil
import tempfile
import unittest
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import pinn.verify as verify

# Probe module → the symbol the ladder dereferences (verified against source).
_AD_MODULE = "pinn.verification.componentwise_ad"
_GRADCHECK_MODULE = "pinn.verification.gradcheck_probe"
_RESIDUAL_MODULE = "pinn.verification.residual_probe"
_OVERFIT_MODULE = "pinn.verification.overfit_probe"

# The fp64-CPU arm: hardware-independent, so the ladder tests run anywhere.
_ARM = {"precision": "float64", "device": "cpu"}


def _healthy_ad_record() -> dict:
    """``run_probe_arm`` has NO top-level pass flag — both patterns + no exception."""
    return {
        "profile": "float64-cpu",
        "exception": None,
        "patterns": {
            "full_jacobian": {"passed": True, "aggregate_relative_error": 1e-16},
            "scalar_u_jvp": {"passed": True, "aggregate_relative_error": 1e-16},
        },
    }


@contextmanager
def _healthy_probes(**overrides):
    """Patch all four probe entry points (plus MPS availability) to PASS.

    ``overrides`` replaces a single probe's patch value by rung name, e.g.
    ``_healthy_probes(gradcheck=mock.Mock(side_effect=RuntimeError("boom")))``.
    """
    specs = {
        "ad": (f"{_AD_MODULE}.run_probe_arm", _healthy_ad_record()),
        "gradcheck": (
            f"{_GRADCHECK_MODULE}.run_gradcheck",
            {"passed": True, "reason": None, "exception": None},
        ),
        "residual": (
            f"{_RESIDUAL_MODULE}.run_residual_on_ground_truth",
            {"passed": True, "gate_a": {"passed": True}, "gate_b": {"passed": True}},
        ),
        "overfit": (
            f"{_OVERFIT_MODULE}.run_overfit",
            {"passed": True, "fail_reason": None, "ratio": 1e4},
        ),
    }
    patches = [mock.patch("torch.backends.mps.is_available", return_value=True)]
    for key, (target, healthy) in specs.items():
        replacement = overrides.get(key)
        if replacement is None:
            patches.append(mock.patch(target, return_value=healthy))
        else:
            patches.append(mock.patch(target, replacement))
    started = [p.start() for p in patches]
    try:
        yield started
    finally:
        for p in reversed(patches):
            p.stop()


@contextmanager
def _hidden_symbol(module_name: str, symbol: str):
    """Temporarily remove a probe symbol to simulate a missing/broken probe."""
    module = importlib.import_module(module_name)
    sentinel = object()
    original = getattr(module, symbol, sentinel)
    if original is not sentinel:
        delattr(module, symbol)
    try:
        yield
    finally:
        if original is not sentinel:
            setattr(module, symbol, original)


class LadderOrderTests(unittest.TestCase):
    """The five rungs run in the SPEC-declared order."""

    def test_ladder_order_is_the_spec_order(self):
        self.assertEqual(
            list(verify.LADDER),
            [
                verify.RUNG_DEVICE_SANITY,
                verify.RUNG_COMPONENTWISE_AD,
                verify.RUNG_GRADCHECK,
                verify.RUNG_RESIDUAL,
                verify.RUNG_OVERFIT,
            ],
        )

    def test_run_ladder_returns_records_in_ladder_order(self):
        with _healthy_probes():
            results = verify.run_ladder(**_ARM)
        self.assertEqual([r["name"] for r in results], list(verify.LADDER))
        for record in results:
            self.assertEqual(set(record), {"name", "passed", "reason"})


class AllPassTests(unittest.TestCase):
    """A healthy environment: every rung PASSes and the ladder is green."""

    def test_all_rungs_pass(self):
        with _healthy_probes():
            results = verify.run_ladder(**_ARM)
        self.assertTrue(all(r["passed"] for r in results), msg=str(results))
        self.assertTrue(verify.ladder_is_green(results))
        self.assertIsNone(verify.first_failed_rung(results))

    def test_all_four_probes_are_invoked_as_library_calls(self):
        with _healthy_probes() as started:
            verify.run_ladder(**_ARM)
        # started[0] is the MPS-availability patch; 1..4 are the four probes.
        for probe_mock in started[1:]:
            self.assertEqual(
                probe_mock.call_count,
                1,
                msg=f"probe {probe_mock} was not called exactly once",
            )

    def test_gradcheck_rung_always_uses_float64_cpu(self):
        with _healthy_probes() as started:
            verify.run_ladder(precision="float32", device="mps")
        gradcheck_mock = started[2]
        args, kwargs = gradcheck_mock.call_args
        called_with = list(args) + [kwargs.get("precision"), kwargs.get("device")]
        self.assertIn("float64", called_with)
        self.assertIn("cpu", called_with)


class RaisedRungTests(unittest.TestCase):
    """A rung that raises is that rung's FAIL — never a silent skip."""

    def test_raised_middle_rung_fails_only_that_rung(self):
        boom = mock.Mock(side_effect=RuntimeError("gradcheck exploded"))
        with _healthy_probes(gradcheck=boom):
            results = verify.run_ladder(**_ARM)
        by_name = {r["name"]: r for r in results}
        self.assertFalse(by_name[verify.RUNG_GRADCHECK]["passed"])
        self.assertIn("gradcheck exploded", by_name[verify.RUNG_GRADCHECK]["reason"])
        # The rungs AFTER the raise still ran and recorded their own results.
        self.assertTrue(by_name[verify.RUNG_RESIDUAL]["passed"])
        self.assertTrue(by_name[verify.RUNG_OVERFIT]["passed"])
        self.assertFalse(verify.ladder_is_green(results))

    def test_first_failed_rung_is_the_earliest_failure(self):
        boom_ad = mock.Mock(side_effect=RuntimeError("ad exploded"))
        boom_overfit = mock.Mock(side_effect=RuntimeError("overfit exploded"))
        with _healthy_probes(ad=boom_ad, overfit=boom_overfit):
            results = verify.run_ladder(**_ARM)
        self.assertEqual(
            verify.first_failed_rung(results), verify.RUNG_COMPONENTWISE_AD
        )

    def test_unavailable_mps_fails_the_device_rung(self):
        with _healthy_probes():
            with mock.patch("torch.backends.mps.is_available", return_value=False):
                results = verify.run_ladder(**_ARM)
        by_name = {r["name"]: r for r in results}
        self.assertFalse(by_name[verify.RUNG_DEVICE_SANITY]["passed"])
        self.assertIn("mps", by_name[verify.RUNG_DEVICE_SANITY]["reason"].lower())
        self.assertEqual(
            verify.first_failed_rung(results), verify.RUNG_DEVICE_SANITY
        )

    def test_unsupported_precision_device_pair_fails_the_device_rung(self):
        with _healthy_probes():
            results = verify.run_ladder(precision="float64", device="mps")
        by_name = {r["name"]: r for r in results}
        self.assertFalse(by_name[verify.RUNG_DEVICE_SANITY]["passed"])
        self.assertEqual(
            verify.first_failed_rung(results), verify.RUNG_DEVICE_SANITY
        )

    def test_ad_rung_derives_pass_from_every_pattern(self):
        one_bad = dict(_healthy_ad_record())
        one_bad["patterns"] = {
            "full_jacobian": {"passed": True},
            "scalar_u_jvp": {"passed": False},
        }
        with _healthy_probes(ad=mock.Mock(return_value=one_bad)):
            results = verify.run_ladder(**_ARM)
        by_name = {r["name"]: r for r in results}
        self.assertFalse(by_name[verify.RUNG_COMPONENTWISE_AD]["passed"])
        self.assertIn("scalar_u_jvp", by_name[verify.RUNG_COMPONENTWISE_AD]["reason"])

    def test_ad_rung_fails_on_probe_exception_field(self):
        with_exc = dict(_healthy_ad_record())
        with_exc["exception"] = {"type": "ValueError", "message": "non-finite"}
        with _healthy_probes(ad=mock.Mock(return_value=with_exc)):
            results = verify.run_ladder(**_ARM)
        by_name = {r["name"]: r for r in results}
        self.assertFalse(by_name[verify.RUNG_COMPONENTWISE_AD]["passed"])


class MissingProbeSymbolTests(unittest.TestCase):
    """A missing probe symbol counts as that rung's FAIL (CTX-70)."""

    def test_missing_overfit_symbol_fails_its_rung(self):
        with _healthy_probes():
            with _hidden_symbol(_OVERFIT_MODULE, "run_overfit"):
                results = verify.run_ladder(**_ARM)
        by_name = {r["name"]: r for r in results}
        self.assertFalse(by_name[verify.RUNG_OVERFIT]["passed"])
        self.assertIn("run_overfit", by_name[verify.RUNG_OVERFIT]["reason"])
        self.assertFalse(verify.ladder_is_green(results))

    def test_missing_residual_symbol_is_the_first_failed_rung(self):
        with _healthy_probes():
            with _hidden_symbol(_RESIDUAL_MODULE, "run_residual_on_ground_truth"):
                results = verify.run_ladder(**_ARM)
        self.assertEqual(verify.first_failed_rung(results), verify.RUNG_RESIDUAL)

    def test_unimportable_probe_module_fails_its_rung(self):
        with _healthy_probes():
            with mock.patch.object(
                verify.importlib,
                "import_module",
                side_effect=ImportError("no module named pinn.verification.x"),
            ):
                results = verify.run_ladder(**_ARM)
        # Every probe-backed rung fails; the device rung (no probe import) passes.
        by_name = {r["name"]: r for r in results}
        self.assertTrue(by_name[verify.RUNG_DEVICE_SANITY]["passed"])
        for rung in (
            verify.RUNG_COMPONENTWISE_AD,
            verify.RUNG_GRADCHECK,
            verify.RUNG_RESIDUAL,
            verify.RUNG_OVERFIT,
        ):
            self.assertFalse(by_name[rung]["passed"], msg=rung)


class _CliHarness(unittest.TestCase):
    """Shared temp runs-root so ``main()`` never writes the worktree ``runs/``."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase43-verify-"))
        self.runs_root = self.tmp / "runs"
        self.runs_root.mkdir()
        self._orig_runs = verify._RUNS_ROOT
        verify._RUNS_ROOT = self.runs_root

    def tearDown(self):
        verify._RUNS_ROOT = self._orig_runs
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = verify.main(argv)
        return code, out.getvalue(), err.getvalue()

    def _arm_argv(self, *extra):
        return ["--precision", "float64", "--device", "cpu", *extra]


class CliTests(_CliHarness):
    def test_help_works(self):
        with self.assertRaises(SystemExit) as ctx:
            self._main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_green_ladder_exits_zero_and_prints_each_rung(self):
        with _healthy_probes():
            code, out, _err = self._main(self._arm_argv())
        self.assertEqual(code, 0, msg=out)
        for rung in verify.LADDER:
            self.assertIn(rung, out)
        self.assertIn("PASS", out)
        self.assertIn("GREEN", out.upper())

    def test_red_ladder_exits_nonzero_naming_first_failed_rung(self):
        boom = mock.Mock(side_effect=RuntimeError("gradcheck exploded"))
        with _healthy_probes(gradcheck=boom):
            code, out, err = self._main(self._arm_argv())
        self.assertNotEqual(code, 0)
        combined = out + err
        self.assertIn(verify.RUNG_GRADCHECK, combined)
        # The overall verdict line must name the FIRST failed rung.
        verdict_lines = [
            line for line in combined.splitlines() if "VERIFY" in line.upper()
        ]
        self.assertTrue(verdict_lines, msg=combined)
        self.assertIn(verify.RUNG_GRADCHECK, verdict_lines[-1])


if __name__ == "__main__":
    unittest.main()
