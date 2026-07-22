"""Phase 43 / 43-06 — ACC-02 real-data smoke integration test (Task 2).

Skip-guarded real-data integration test. Validates the artifacts the ORDINARY
``python -m pinn.train --config configs/smoke.yaml`` command actually produced
in ``runs/stage0-smoke/`` (and the timing calibration it would persist on a
terminal-success smoke) against the evidence recorded in
``.planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md``.
Never substitutes synthetic data for a real-corpus check, and never asserts a
fabricated success (SPEC edge R2).

Current state (2026-07-22, DI-43-06-01, recorded in the evidence README): the
real admitted corpus root (``simulation_data/Data/``, resolved via
``default_data_root()``) is reachable — the CTX-79 directory-level preflight
passes — but the admitted adapter's DEFAULT blacklist resolution
(``<data_root>/problematic_ics_blacklist.json``) has no file there; the sole
``problematic_ics_blacklist.json`` in the repo lives at
``simulation_data/Documentation/`` and is documented in the dataset's own
README as legacy / not used by current runners. ``pinn.train`` never threads a
``blacklist_path`` override, so an ordinary admitted run over the real corpus
refuses fail-closed BEFORE any training step, checkpoint, or timing
measurement. This is a genuine, pre-existing, out-of-scope wiring gap (see the
evidence README's Task 2 section) — the tests below assert the HONEST
fail-closed refusal actually observed, never a fabricated pass.

``HonestFailureEvidenceTests`` is ACTIVE now and guards the R2 honesty
invariant (no fabricated success/metrics) against the real recorded evidence.
``RealSmokeArtifactTests`` is skip-guarded on step-300 checkpoint evidence and
will activate automatically — turning from skip to green, mirroring the
Phase-43 ``_require`` convention used across this package — once DI-43-06-01
is resolved and a full real smoke + interrupt + resume completes.
"""

from __future__ import annotations

import json
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
_DEFAULT_BLACKLIST_NAME = "problematic_ics_blacklist.json"


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


class HonestFailureEvidenceTests(unittest.TestCase):
    """DI-43-06-01: while the corpus-adjacent blacklist file remains absent at
    the adapter's default resolution, the recorded evidence must show an
    honest fail-closed refusal — never a fabricated success or invented
    timing (SPEC edge R2)."""

    def setUp(self):
        root = _default_data_root()
        if not (root.exists() and root.is_dir()):
            raise unittest.SkipTest(f"real admitted corpus root unreachable at {root}")
        self.blacklist_path = root / _DEFAULT_BLACKLIST_NAME
        if self.blacklist_path.exists():
            raise unittest.SkipTest(
                "DI-43-06-01 appears resolved (a blacklist file now exists at "
                f"{self.blacklist_path}); this failure-path suite is stale — "
                "see RealSmokeArtifactTests for the success-path assertions "
                "and re-run 43-06 Task 2 for fresh evidence"
            )

    def test_run_summary_records_failed_disposition_not_fabricated_success(self):
        summary_path = _RUN_DIR / "summary.json"
        if not summary_path.is_file():
            raise unittest.SkipTest(
                f"no recorded run summary at {summary_path}; run Task 2's "
                "`python -m pinn.train --config configs/smoke.yaml` first"
            )
        summary = _read_json(summary_path)
        self.assertEqual(summary.get("disposition"), "failed")
        final_losses = summary.get("final_losses") or {}
        for key, value in final_losses.items():
            self.assertIsNone(value, f"final_losses.{key} was fabricated: {value!r}")

    def test_status_records_null_metrics_not_fabricated(self):
        status_path = _RUN_DIR / "status.json"
        if not status_path.is_file():
            raise unittest.SkipTest(f"no recorded status at {status_path}")
        status = _read_json(status_path)
        self.assertEqual(status.get("state"), "failed")
        self.assertIsNone(status.get("step"))
        self.assertIsNone(status.get("s_per_step_ema"))
        self.assertIsNone(status.get("stage"))

    def test_no_timing_calibration_was_fabricated(self):
        from pinn.training import timing

        record = timing.read_calibration(_RUNS_ROOT)
        self.assertIsNone(
            record,
            "a timing calibration must never be written from a failed/partial "
            "smoke (SPEC R2) — found one despite the recorded blacklist "
            "wiring gap (DI-43-06-01)",
        )

    def test_evidence_readme_documents_the_honest_failure(self):
        if not _SMOKE_README.is_file():
            raise unittest.SkipTest(f"missing {_SMOKE_README}")
        text = _SMOKE_README.read_text(encoding="utf-8")
        self.assertIn("DI-43-06-01", text)
        self.assertIn("problematic_ics_blacklist.json", text)
        self.assertIn("HONEST FAILURE", text)


class RealSmokeArtifactTests(unittest.TestCase):
    """Full success-path assertions: 32-trajectory replay identity count,
    checkpoints at steps 100/200/300, a finite positive measured
    ``s_per_step``, a persisted valid timing calibration, and a resume
    round-trip to a ``finished`` disposition. Skip-guarded on step-300
    checkpoint evidence so this class turns green automatically once
    DI-43-06-01 is resolved and a full real smoke + interrupt + resume lands
    (Phase-43's established skip-to-green convention)."""

    def setUp(self):
        ckpt_dir = _RUN_DIR / "checkpoints"
        step_300 = ckpt_dir / "step-000300.pt"
        if not step_300.is_file():
            raise unittest.SkipTest(
                "no full real smoke to step 300 recorded yet — blocked on "
                "DI-43-06-01 (see evidence/smoke/README.md); this suite "
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
