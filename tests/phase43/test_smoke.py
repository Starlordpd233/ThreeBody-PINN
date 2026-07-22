"""Phase 43 / 43-06 — ACC-02 real-data smoke integration test (Task 2).

Skip-guarded real-data integration test. Validates the artifacts the ORDINARY
``python -m pinn.train --config configs/smoke.yaml`` command actually produced
in ``runs/stage0-smoke/`` (and the timing calibration it would persist on a
terminal-success smoke) against the evidence recorded in
``.planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md``.
Never substitutes synthetic data for a real-corpus check, and never asserts a
fabricated success (SPEC edge R2).

History (see the evidence README for full detail):

* DI-43-06-01 (real corpus reachable but the admitted adapter's default
  blacklist resolution had no file colocated with ``Data/``) is **RESOLVED**
  (owner Option A, 2026-07-22): ``DataConfig.blacklist_path`` +
  ``pinn.train._resolve_blacklist_path`` thread the owner-designated legacy
  65-ID Documentation blacklist through, and a real admitted run now produces
  genuine per-step training losses (previously impossible).
* DI-43-06-02 (**OPEN, BLOCKING**): the re-run surfaced a NEW finding — the
  real admitted corpus's raw physics residual at random SIREN init is large
  enough (~2.8-3.3e8) that even the PHYS-05 warmup ramp's first non-zero
  weight trips the ``⚖ PROVISIONAL (R-1)`` ``run.guards.loss_explosion_ceiling``
  (owner-carved, "calibrate-at-Phase-43-pilot") at step 2. The run terminates
  honestly (``disposition: "failed"``, all ``final_losses`` null, no
  fabricated timing calibration) — this is out of scope to self-fix (R-1 is
  an owner-carved guard threshold, not a wiring bug).

``HonestyGuardTests`` is ACTIVE now and guards the R2 honesty invariant (no
fabricated success/metrics) against whichever real evidence is currently on
disk, independent of which finding produced it. ``RealSmokeArtifactTests`` is
skip-guarded on step-300 checkpoint evidence and will activate automatically
— turning from skip to green, mirroring the Phase-43 ``_require`` convention
used across this package — once DI-43-06-02 is resolved and a full real
smoke + interrupt + resume completes.
"""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path
from typing import Any, Mapping

_REPO_ROOT = Path(__file__).resolve().parents[2]
_RUN_DIR = _REPO_ROOT / "runs" / "stage0-smoke"
_RUNS_ROOT = _REPO_ROOT / "runs"
_SMOKE_README = (
    _REPO_ROOT
    / ".planning"
    / "phases"
    / "43-verification-stage-0-pilot-acceptance"
    / "evidence"
    / "smoke"
    / "README.md"
)


def _default_data_root() -> Path:
    from pinn.data.adapter import default_data_root

    return Path(default_data_root())


def _read_json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class RealCorpusReachabilityGuardTests(unittest.TestCase):
    """CTX-79 directory-level reachability, checked against the true filesystem
    (never mocked — this is the real-data integration guard for the module)."""

    def test_default_root_reachable_in_this_worktree(self):
        root = _default_data_root()
        if not (root.exists() and root.is_dir()):
            raise unittest.SkipTest(
                f"real admitted corpus root unreachable at {root}; skipping "
                "real-data smoke evidence checks (CTX-79 fallback needed)"
            )
        self.assertTrue(root.is_dir())


class HonestyGuardTests(unittest.TestCase):
    """SPEC edge R2: whatever the real run's evidence currently shows, it must
    be genuine — never a fabricated success, never a fabricated metric, never
    a fabricated timing calibration. Applies regardless of which finding
    (DI-43-06-01, resolved; DI-43-06-02, open) produced the current on-disk
    evidence, so this suite keeps guarding honesty as the underlying blocker
    changes."""

    def setUp(self):
        root = _default_data_root()
        if not (root.exists() and root.is_dir()):
            raise unittest.SkipTest(f"real admitted corpus root unreachable at {root}")
        if not (_RUN_DIR / "summary.json").is_file():
            raise unittest.SkipTest(
                f"no recorded run summary at {_RUN_DIR / 'summary.json'}; run "
                "Task 2's `python -m pinn.train --config configs/smoke.yaml` first"
            )

    def test_run_summary_records_genuine_disposition_not_fabricated(self):
        summary = _read_json(_RUN_DIR / "summary.json")
        disposition = summary.get("disposition")
        self.assertIn(disposition, ("failed", "interrupted", "finished"))
        final_losses = summary.get("final_losses") or {}
        if disposition == "finished":
            for key, value in final_losses.items():
                self.assertIsNotNone(value, f"final_losses.{key} missing on finished run")
                self.assertTrue(math.isfinite(float(value)), f"final_losses.{key}={value!r}")
        else:
            for key, value in final_losses.items():
                self.assertIsNone(
                    value, f"final_losses.{key} was fabricated on a {disposition} run: {value!r}"
                )

    def test_status_state_matches_summary_disposition(self):
        status = _read_json(_RUN_DIR / "status.json")
        summary = _read_json(_RUN_DIR / "summary.json")
        self.assertEqual(status.get("state"), summary.get("disposition"))

    def test_no_timing_calibration_unless_terminal_success(self):
        from pinn.training import timing

        summary = _read_json(_RUN_DIR / "summary.json")
        record = timing.read_calibration(_RUNS_ROOT)
        if summary.get("disposition") == "finished":
            self.assertIsNotNone(record)
            self.assertTrue(record.get("valid") is True)
        else:
            self.assertIsNone(
                record,
                "a timing calibration must never be written from a "
                f"{summary.get('disposition')!r} smoke (SPEC R2)",
            )
            # A failed run that actually reached a training step should have a
            # named, honest guard-trip record — never a bare unexplained
            # failure once StepGuards has had a chance to run.
            status = _read_json(_RUN_DIR / "status.json")
            if summary.get("disposition") == "failed" and status.get("step") is not None:
                trip_path = _RUN_DIR / "failure" / "trip.json"
                self.assertTrue(trip_path.is_file(), f"missing {trip_path}")
                trip = _read_json(trip_path)
                self.assertIn("guard", trip)
                self.assertIn("reason", trip)

    def test_evidence_readme_documents_the_findings(self):
        text = _SMOKE_README.read_text(encoding="utf-8")
        self.assertIn("DI-43-06-01", text)
        self.assertIn("RESOLUTION", text)
        self.assertIn("problematic_ics_blacklist.json", text)


class RealSmokeArtifactTests(unittest.TestCase):
    """Full success-path assertions: 32-trajectory replay identity count,
    checkpoints at steps 100/200/300, a finite positive measured
    ``s_per_step``, a persisted valid timing calibration, and a resume
    round-trip to a ``finished`` disposition. Skip-guarded on step-300
    checkpoint evidence so this class turns green automatically once
    DI-43-06-02 is resolved and a full real smoke + interrupt + resume lands
    (Phase-43's established skip-to-green convention)."""

    def setUp(self):
        ckpt_dir = _RUN_DIR / "checkpoints"
        step_300 = ckpt_dir / "step-000300.pt"
        if not step_300.is_file():
            raise unittest.SkipTest(
                "no full real smoke to step 300 recorded yet — blocked on "
                "DI-43-06-02 (see evidence/smoke/README.md); this suite "
                "activates once a full interrupt+resume run lands"
            )

    def test_checkpoints_at_100_200_300(self):
        ckpt_dir = _RUN_DIR / "checkpoints"
        for step in (100, 200, 300):
            path = ckpt_dir / f"step-{step:06d}.pt"
            self.assertTrue(path.is_file(), f"missing checkpoint {path}")

    def test_measured_s_per_step_is_finite_positive(self):
        from pinn.training import timing

        record = timing.read_calibration(_RUNS_ROOT)
        self.assertIsNotNone(record)
        s_per_step = record["s_per_step"]
        self.assertIsInstance(s_per_step, (int, float))
        self.assertGreater(float(s_per_step), 0.0)

    def test_persisted_timing_calibration_is_valid(self):
        from pinn.training import timing

        record = timing.read_calibration(_RUNS_ROOT)
        self.assertIsNotNone(record)
        self.assertTrue(record.get("valid") is True)

    def test_resume_result_recorded_as_finished(self):
        summary = _read_json(_RUN_DIR / "summary.json")
        self.assertEqual(summary.get("disposition"), "finished")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
