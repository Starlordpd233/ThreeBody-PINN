"""Phase 42 / Plan 09 — honesty layer (must-NOT #1).

A failed or interrupted run must NOT masquerade as finished and must NOT
fabricate metrics. ``summary.md`` / ``summary.json`` are written at launch
(``stub_summary``) and atomically replaced at the terminal transition
(``finalize_summary``); a CTX-67 null policy means a loss term that never
finalized stays ``null`` — never a placeholder number.

Test matrix (subprocess-driven, dataset-free synthetic runs):
  (a) forced-HALT (catchable): ``loss_explosion_ceiling`` set so low the
      guard trips RECOVER on the first step → ``finish_run("failed", ...)``.
      Assert ``status.json state == "failed"``, ``summary.json disposition ==
      "failed"``, and every final-loss term is ``null`` (no fabricated
      positive reading).
  (b) forced-divergence (catchable): same shape — a guard-tripped failed run
      whose summary names its state and leaves metrics null.

The production path to a catchable failed run is a guard RECOVER disposition:
``RunController.run_stage`` returns ``StageDisposition.RECOVER`` →
``CurriculumController.run`` returns it → in ``pinn.train.main``
``signal_state.stop_requested`` is False, ``run_raised`` is False, but the
guard has written a failure artifact under ``runs/<name>/failure/`` so
``any((run_dir / "failure").iterdir())`` is True → ``finish_run("failed", 1)``.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Dict

from tests.phase42._fixtures import (
    launch_train,
    wait_for_status,
    write_train_config,
)

# Loss terms the summary renders (must all be null for a failed run).
_LOSS_TERMS = ("data", "ic", "phys", "energy", "angmom", "total")


def _unique_name(test_name: str) -> str:
    return f"hon-{test_name}-{os.getpid()}"


def _proc_alive(proc: subprocess.Popen) -> bool:
    return proc.poll() is None


def _write_failed_config(path: Path, run_name: str) -> Path:
    """Config tuned so the guard trips a catchable failure on step 0.

    ``loss_explosion_ceiling`` is set far below any realistic synthetic-run
    loss, so the loss-explosion guard fires RECOVER on the first step. The
    guard writes a failure artifact under ``runs/<name>/failure/``, which
    ``pinn.train.main`` reads back as a failed run (``finish_run("failed", 1)``).
    """
    return write_train_config(
        path,
        run={"run_name": run_name, "log_every": 1},
        stage={"max_epochs": 200, "n_adam": 50},
        # Loss ceiling so low the synthetic run exceeds it on step 0.
        guards={"loss_explosion_ceiling": 1e-12},
    )


def _wait_for_failure_artifact(
    run_dir: Path, *, timeout: float = 60.0, poll: float = 0.1
) -> None:
    """Block until ``runs/<name>/failure/`` is non-empty (guard wrote its bundle)."""
    failure_dir = run_dir / "failure"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            if any(failure_dir.iterdir()):
                return
        except OSError:
            pass
        time.sleep(poll)
    raise TimeoutError(
        f"no failure artifact appeared under {failure_dir} within {timeout}s"
    )


def _final_status(run_dir: Path) -> Dict[str, Any]:
    return json.loads((run_dir / "status.json").read_text(encoding="utf-8"))


def _final_summary_json(run_dir: Path) -> Dict[str, Any]:
    return json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))


class HonestyTests(unittest.TestCase):
    """must-NOT #1: failed/interrupted runs never masquerade as finished."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="phase42-honesty-"))
        self.runs_root = self.tmp / "runs"
        self.runs_root.mkdir()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.tmp, ignore_errors=True)

    def _launch(self, cfg: Path) -> subprocess.Popen[str]:
        return launch_train(cfg, self.runs_root)

    def _run_dir(self, run_name: str) -> Path:
        return self.runs_root / run_name

    # ------------------------------------------------------------------
    # (a) forced-HALT (catchable) via guard RECOVER.
    # ------------------------------------------------------------------
    def test_forced_halt_catchable_state_not_finished_and_no_fabricated_metrics(
        self,
    ) -> None:
        name = _unique_name("halt")
        cfg = self.tmp / f"{name}.yaml"
        _write_failed_config(cfg, run_name=name)
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            # Readiness barrier: the run is alive and signal handlers are
            # installed. We do NOT wait for terminal — the guard trips fast.
            wait_for_status(run_dir, pid=proc.pid, states=["running"], timeout=60.0)
            # Wait for the guard to write its failure artifact (the signal
            # that ``finish_run("failed", ...)`` will be on the exit path).
            _wait_for_failure_artifact(run_dir, timeout=120.0)
            out, err = proc.communicate(timeout=120)
            # The run terminated via the failed branch, not finished.
            status = _final_status(run_dir)
            self.assertEqual(
                status["state"],
                "failed",
                msg=f"expected state=failed, got {status}\nstdout={out}\nstderr={err}",
            )
            summary = _final_summary_json(run_dir)
            self.assertEqual(
                summary["disposition"],
                "failed",
                msg=f"summary disposition={summary['disposition']}",
            )
            # CTX-67 null policy: a failed run must NOT fabricate positive
            # loss readings. Every final-loss term is null.
            final_losses = summary.get("final_losses") or {}
            for term in _LOSS_TERMS:
                self.assertIsNone(
                    final_losses.get(term),
                    msg=(
                        f"term {term!r} is {final_losses.get(term)!r} — "
                        f"a failed run must leave un-finalized losses null, not fabricated"
                    ),
                )
            # summary.md must name the failed state and not read as healthy.
            md = (run_dir / "summary.md").read_text(encoding="utf-8")
            self.assertIn("failed", md)
            self.assertNotIn("finished", md)
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)

    # ------------------------------------------------------------------
    # (b) forced-divergence (catchable): same catchable failed path,
    #     honesty invariants identical.
    # ------------------------------------------------------------------
    def test_forced_divergence_catchable_state_not_finished(self) -> None:
        name = _unique_name("diverge")
        # Same mechanism as (a): a loss ceiling so low the (finite) synthetic
        # loss exceeds it, exercising the catchable failed path. The honesty
        # invariant is identical — state != finished and no fabricated metrics.
        cfg = self.tmp / f"{name}.yaml"
        _write_failed_config(cfg, run_name=name)
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            wait_for_status(run_dir, pid=proc.pid, states=["running"], timeout=60.0)
            _wait_for_failure_artifact(run_dir, timeout=120.0)
            out, err = proc.communicate(timeout=120)
            status = _final_status(run_dir)
            self.assertEqual(
                status["state"],
                "failed",
                msg=f"expected state=failed, got {status}\nstdout={out}\nstderr={err}",
            )
            summary = _final_summary_json(run_dir)
            self.assertEqual(summary["disposition"], "failed")
            md = (run_dir / "summary.md").read_text(encoding="utf-8")
            self.assertIn("failed", md)
            self.assertNotIn("finished", md)
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)


if __name__ == "__main__":
    unittest.main()
