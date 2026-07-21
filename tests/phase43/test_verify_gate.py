"""Phase 43 / Plan 04 — ACC-01 >30-min launch duration gate (production path).

The milestone's safety rule, made real for a fresh process rather than a
monkeypatched seam: a non-smoke fresh launch must present a VALID persisted
Stage-0 timing calibration (plan 43-03 ``runs/.calibration/stage0-timing.json``)
so the gate can forecast an honest duration, and a forecast strictly above
1800 s (30 min) additionally needs a fresh GREEN full-fingerprint verify marker
(plan 43-01 ``runs/.verify/latest-marker.json``). A forecast of EXACTLY 1800 s
PASSES (SPEC edge R1 — the reject is the strict inequality ``> 1800``).

Two complementary surfaces are tested:

* ``DurationGateFunctionTests`` drives ``pinn.train._check_duration_gate``
  in-process against REAL persisted calibration + marker files (written through
  the production ``timing.write_calibration`` / ``verify.write_verify_marker``
  writers), covering the full refusal matrix — unavailable / invalid calibration,
  the exact 1800 boundary, over-limit without a marker, and the stale /
  code-mismatch / runtime-mismatch / Git-unavailable marker states — exercising
  the actual persisted read path with no subprocess overhead.

* ``DurationGateLaunchTests`` drives a real ``python -m pinn.train`` subprocess
  (the Phase-42 wrapper that pins ``pinn.train._RUNS_ROOT`` to an isolated temp
  runs-root) and asserts the production backstop: refusal happens BEFORE
  run-directory creation (no run-dir left behind, exit 1, stderr names the gate),
  the exact-1800 boundary is accepted (run-dir created), a complete green marker
  is accepted, and an invalid marker is refused.

Fingerprint matching: both the calibration and the marker are written for
``float64``/``cpu`` — the Phase-42 test config's runtime — so the gate's own
``verify.current_fingerprint(precision, device)`` (same repo, same conda env,
same Git head) matches them. Mismatch states are built by overriding a single
fingerprint field (``git_head`` / ``torch_version`` / ``git_head_available``) so
each refusal is isolated to one dimension.
"""

from __future__ import annotations

import importlib
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from tests.phase43 import _SKIP_PHRASE
from tests.phase43._fixtures import launch_train, write_train_config

TRAIN_MODULE = "pinn.train"


def _require(symbol: str, module: str = TRAIN_MODULE) -> Any:
    """Deferred-import skip guard (Phase-43 convention)."""
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


# The production runtime the Phase-42 test config uses; calibration + marker
# fixtures are written for this pair so the gate's fingerprint matches them.
_PRECISION = "float64"
_DEVICE = "cpu"

# The 30-minute boundary (SPEC prohibition 4 / edge R1).
_LIMIT_S = 1800.0

# s_per_step values chosen against ``max_epochs=2`` so the forecast lands exactly
# on, just below, and just above the 1800 s boundary (forecast = s/step * steps).
_SPS_EXACTLY_1800 = 900.0  # 900.0 * 2 == 1800.0  -> boundary, PASSES
_SPS_ABOVE_1800 = 1000.0  # 1000.0 * 2 == 2000.0 > 1800 -> needs a green marker

# A stable phrase present in every duration-gate refusal message.
_REFUSE_PHRASE = "refusing before construction"


# ---------------------------------------------------------------------------
# Fixture writers — REAL persisted calibration + marker via the production
# writers, so the tests exercise the actual read path the gate consumes.
# ---------------------------------------------------------------------------


def _write_calibration(
    runs_root: Path,
    *,
    s_per_step: float,
    precision: str = _PRECISION,
    device: str = _DEVICE,
    full_stage0_steps: int = 2,
) -> Path:
    timing = importlib.import_module("pinn.training.timing")
    return timing.write_calibration(
        s_per_step=s_per_step,
        full_stage0_steps=full_stage0_steps,
        precision=precision,
        device=device,
        runs_root=runs_root,
    )


def _current_fingerprint(
    precision: str = _PRECISION, device: str = _DEVICE
) -> Dict[str, Any]:
    verify = importlib.import_module("pinn.verify")
    return verify.current_fingerprint(precision=precision, device=device)


def _fingerprint_with(**overrides: Any) -> Dict[str, Any]:
    """The real float64/cpu fingerprint with one field overridden (mismatch)."""
    fingerprint = _current_fingerprint()
    fingerprint.update(overrides)
    return fingerprint


def _write_marker(
    runs_root: Path,
    *,
    fingerprint: Optional[Dict[str, Any]] = None,
    now: Optional[datetime] = None,
    precision: str = _PRECISION,
    device: str = _DEVICE,
) -> Path:
    """Write a GREEN verify marker (all rungs passed) with a chosen fingerprint."""
    verify = importlib.import_module("pinn.verify")
    green_rungs = [
        {"name": rung, "passed": True, "reason": None} for rung in verify.LADDER
    ]
    return verify.write_verify_marker(
        green_rungs,
        precision=precision,
        device=device,
        runs_root=runs_root,
        fingerprint=fingerprint,
        now=now,
    )


def _load_config(cfg_path: Path) -> Any:
    config_yaml = importlib.import_module("pinn.training.config_yaml")
    return config_yaml.load_config(str(cfg_path))


def _write_gate_config(
    path: Path, run_name: str, *, smoke: bool = False, max_epochs: int = 2
) -> Path:
    """A minimal non-smoke (or smoke) float64/cpu config with a declared budget."""
    return write_train_config(
        path,
        run={"run_name": run_name, "smoke": smoke},
        stage={"max_epochs": max_epochs, "n_adam": max_epochs},
    )


# ---------------------------------------------------------------------------
# In-process gate matrix — real persisted fixtures, actual read path.
# ---------------------------------------------------------------------------


class DurationGateFunctionTests(unittest.TestCase):
    """``_check_duration_gate`` against real calibration + marker files."""

    def setUp(self) -> None:
        _require("_check_duration_gate", TRAIN_MODULE)
        _require("DurationGateError", TRAIN_MODULE)
        _require("write_calibration", "pinn.training.timing")
        _require("write_verify_marker", "pinn.verify")
        self.tmp = Path(tempfile.mkdtemp(prefix="phase43-gate-fn-"))
        self.runs_root = self.tmp / "runs"
        self.runs_root.mkdir()
        self.cfg_path = self.tmp / "config.yaml"

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.tmp, ignore_errors=True)

    def _gate(self, *, smoke: bool = False, max_epochs: int = 2) -> None:
        """Run the gate on a fresh config; raises DurationGateError on refusal."""
        train = importlib.import_module(TRAIN_MODULE)
        cfg_path = _write_gate_config(
            self.tmp / f"cfg-{smoke}-{max_epochs}.yaml",
            f"gate-fn-{smoke}-{max_epochs}",
            smoke=smoke,
            max_epochs=max_epochs,
        )
        config = _load_config(cfg_path)
        train._check_duration_gate(config, runs_root=self.runs_root)

    def _refused(self, *, smoke: bool = False, max_epochs: int = 2) -> str:
        train = importlib.import_module(TRAIN_MODULE)
        with self.assertRaises(train.DurationGateError) as ctx:
            self._gate(smoke=smoke, max_epochs=max_epochs)
        return str(ctx.exception)

    # -- exemptions --------------------------------------------------------

    def test_smoke_is_exempt_with_no_calibration(self) -> None:
        # No calibration written; a smoke run is the gate's own calibration
        # source and must never be refused.
        self._gate(smoke=True)  # returns None, no raise

    # -- unavailable / invalid timing -------------------------------------

    def test_no_calibration_is_refused(self) -> None:
        reason = self._refused()
        self.assertIn("timing calibration", reason)
        self.assertIn(_REFUSE_PHRASE, reason)

    def test_fingerprint_mismatched_calibration_is_refused(self) -> None:
        # Calibration written for a different runtime (float32/mps) never matches
        # the float64/cpu launch fingerprint -> no valid forecast -> refused.
        _write_calibration(
            self.runs_root, s_per_step=_SPS_ABOVE_1800, precision="float32", device="mps"
        )
        reason = self._refused()
        self.assertIn(_REFUSE_PHRASE, reason)

    # -- the exact 1800 s boundary (SPEC edge R1) -------------------------

    def test_forecast_exactly_1800_passes_without_marker(self) -> None:
        _write_calibration(self.runs_root, s_per_step=_SPS_EXACTLY_1800)
        # max_epochs=2 -> 900.0 * 2 == 1800.0 exactly; no marker required.
        self._gate(max_epochs=2)  # returns None, no raise

    def test_forecast_just_above_1800_without_marker_is_refused(self) -> None:
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        # max_epochs=2 -> 1000.0 * 2 == 2000.0 > 1800; no marker -> refused.
        reason = self._refused(max_epochs=2)
        self.assertIn("30 min", reason)
        self.assertIn(_REFUSE_PHRASE, reason)

    # -- over-limit with a complete green marker --------------------------

    def test_over_limit_with_green_fresh_marker_passes(self) -> None:
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        _write_marker(self.runs_root)  # green, fresh, matching fingerprint
        self._gate(max_epochs=2)  # returns None, no raise

    # -- over-limit with each invalid marker state ------------------------

    def test_over_limit_with_stale_marker_is_refused(self) -> None:
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        stale = datetime.now(timezone.utc) - timedelta(days=2)
        _write_marker(self.runs_root, now=stale)  # green + matching, but > 24 h old
        reason = self._refused(max_epochs=2)
        self.assertIn(_REFUSE_PHRASE, reason)

    def test_over_limit_with_code_mismatch_marker_is_refused(self) -> None:
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        # Green + fresh, but certified a DIFFERENT commit than the launch HEAD.
        _write_marker(self.runs_root, fingerprint=_fingerprint_with(git_head="0" * 40))
        reason = self._refused(max_epochs=2)
        self.assertIn(_REFUSE_PHRASE, reason)

    def test_over_limit_with_runtime_mismatch_marker_is_refused(self) -> None:
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        # Green + fresh, but certified a different Torch build.
        _write_marker(
            self.runs_root, fingerprint=_fingerprint_with(torch_version="0.0.0-fake")
        )
        reason = self._refused(max_epochs=2)
        self.assertIn(_REFUSE_PHRASE, reason)

    def test_over_limit_with_git_unavailable_marker_is_refused(self) -> None:
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        # Green + fresh, but the code it certified could not be identified.
        _write_marker(
            self.runs_root,
            fingerprint=_fingerprint_with(git_head=None, git_head_available=False),
        )
        reason = self._refused(max_epochs=2)
        self.assertIn(_REFUSE_PHRASE, reason)


# ---------------------------------------------------------------------------
# Subprocess production path — refusal BEFORE run-dir creation.
# ---------------------------------------------------------------------------


def _unique_name(tag: str) -> str:
    import os

    return f"gate-{tag}-{os.getpid()}"


class DurationGateLaunchTests(unittest.TestCase):
    """The >30-min gate on a real ``python -m pinn.train`` fresh launch."""

    def setUp(self) -> None:
        _require("_check_duration_gate", TRAIN_MODULE)
        _require("write_calibration", "pinn.training.timing")
        _require("write_verify_marker", "pinn.verify")
        self.tmp = Path(tempfile.mkdtemp(prefix="phase43-gate-launch-"))
        self.runs_root = self.tmp / "runs"
        self.runs_root.mkdir()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.tmp, ignore_errors=True)

    def _launch(self, cfg: Path) -> subprocess.Popen:
        return launch_train(cfg, self.runs_root)

    def _run_dir(self, name: str) -> Path:
        return self.runs_root / name

    def _assert_refused_before_run_dir(self, cfg: Path, name: str) -> None:
        proc = self._launch(cfg)
        try:
            out, err = proc.communicate(timeout=120)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=10)
        self.assertEqual(
            proc.returncode,
            1,
            msg=f"expected exit 1 (gate refusal)\nstdout={out}\nstderr={err}",
        )
        self.assertIn(
            _REFUSE_PHRASE,
            err,
            msg=f"stderr must name the duration gate\nstdout={out}\nstderr={err}",
        )
        self.assertFalse(
            self._run_dir(name).exists(),
            msg=f"run-dir must NOT be created when the gate refuses: {self._run_dir(name)}",
        )

    def _assert_accepted_run_dir_created(self, cfg: Path, name: str) -> None:
        proc = self._launch(cfg)
        try:
            out, err = proc.communicate(timeout=120)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=10)
        self.assertNotIn(
            _REFUSE_PHRASE,
            err,
            msg=f"gate must not refuse\nstdout={out}\nstderr={err}",
        )
        # The gate refuses BEFORE mkdir, so a created run-dir proves it passed.
        self.assertTrue(
            self._run_dir(name).exists(),
            msg=f"gate should have passed and created the run-dir\n"
            f"stdout={out}\nstderr={err}",
        )

    # -- pre-directory refusal: unavailable timing ------------------------

    def test_no_calibration_refused_before_run_dir(self) -> None:
        name = _unique_name("nocal")
        cfg = _write_gate_config(self.tmp / f"{name}.yaml", name)
        self._assert_refused_before_run_dir(cfg, name)

    # -- pre-directory refusal: over-limit without a marker ---------------

    def test_over_limit_no_marker_refused_before_run_dir(self) -> None:
        name = _unique_name("over")
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        cfg = _write_gate_config(self.tmp / f"{name}.yaml", name)
        self._assert_refused_before_run_dir(cfg, name)

    # -- exact boundary accepted ------------------------------------------

    def test_forecast_exactly_1800_accepted_run_dir_created(self) -> None:
        name = _unique_name("edge")
        _write_calibration(self.runs_root, s_per_step=_SPS_EXACTLY_1800)
        cfg = _write_gate_config(self.tmp / f"{name}.yaml", name)
        self._assert_accepted_run_dir_created(cfg, name)

    # -- complete green marker accepted -----------------------------------

    def test_over_limit_with_green_marker_accepted_run_dir_created(self) -> None:
        name = _unique_name("green")
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        _write_marker(self.runs_root)  # green, fresh, matching fingerprint
        cfg = _write_gate_config(self.tmp / f"{name}.yaml", name)
        self._assert_accepted_run_dir_created(cfg, name)

    # -- invalid marker refused (stale + code-mismatch) -------------------

    def test_over_limit_with_stale_marker_refused_before_run_dir(self) -> None:
        name = _unique_name("stale")
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        stale = datetime.now(timezone.utc) - timedelta(days=2)
        _write_marker(self.runs_root, now=stale)
        cfg = _write_gate_config(self.tmp / f"{name}.yaml", name)
        self._assert_refused_before_run_dir(cfg, name)

    def test_over_limit_with_code_mismatch_marker_refused_before_run_dir(self) -> None:
        name = _unique_name("code")
        _write_calibration(self.runs_root, s_per_step=_SPS_ABOVE_1800)
        _write_marker(self.runs_root, fingerprint=_fingerprint_with(git_head="0" * 40))
        cfg = _write_gate_config(self.tmp / f"{name}.yaml", name)
        self._assert_refused_before_run_dir(cfg, name)


if __name__ == "__main__":
    unittest.main()
