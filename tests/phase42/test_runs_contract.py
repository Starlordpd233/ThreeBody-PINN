"""Phase 42 / Plan 09 — runs contract / kill-timing coverage (OPS-05 / E4).

E4 presence invariant: ``summary.md`` + ``summary.json`` are written at
launch (``stub_summary``) and atomically replaced at the terminal transition
(``finalize_summary``), so they are present under **every** death mode
including SIGKILL — a write-at-exit-only design cannot satisfy this.

Test matrix:
  (a) success → ``summary.json`` carries the full member list (run header,
      config_identity_digest, env_fingerprint, final_losses with all six
      canonical terms non-null, curriculum progression, schema_version).
  (b) SIGKILL at three deterministic barriers (launch / mid-Adam /
      mid-checkpoint) → ``summary.json`` present + parseable + state NOT in
      {``"finished"``, ``"failed"``, ``"interrupted"``} + staleness-decidable:
      the dead heartbeat's final ``timestamp_epoch`` + the file's own
      ``staleness_threshold_secs`` let any later reader classify the run
      stalled by pure arithmetic (CTX-75) — asserted without a wall-clock
      wait, per plan 42-09 Task 2 ("no real wall-clock wait").
  (c) repeated-``main()`` handler-lifecycle regression (in-process): handler
      count returns to baseline, prior SIGINT/SIGTERM handlers restored after
      ``main()``, and no duplicate lines in the JSONL of a single run.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

from tests.phase42._fixtures import (
    launch_train,
    wait_for_status,
    write_train_config,
)

# Loss terms the summary renders (CTX-68 / CTX-77).
_LOSS_TERMS = ("data", "ic", "phys", "energy", "angmom", "total")

# Status states that are terminal (a SIGKILL'd run must NOT be in any of these).
_SIGKILL_FORBIDDEN_STATES = frozenset({"finished", "failed", "interrupted"})


def _unique_name(test_name: str) -> str:
    return f"ctr-{test_name}-{os.getpid()}"


def _proc_alive(proc: subprocess.Popen) -> bool:
    return proc.poll() is None


def _write_success_config(path: Path, run_name: str) -> Path:
    """Short synthetic config that completes normally (finished)."""
    return write_train_config(
        path,
        run={"run_name": run_name, "log_every": 1},
        stage={"max_epochs": 2, "n_adam": 2},
    )


def _write_long_config(path: Path, run_name: str) -> Path:
    """Long-running config for SIGKILL barriers."""
    return write_train_config(
        path,
        run={"run_name": run_name, "log_every": 1},
        stage={"max_epochs": 200, "n_adam": 50},
    )


def _summary_json(run_dir: Path) -> Dict[str, Any]:
    return json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))


def _status_json(run_dir: Path) -> Dict[str, Any]:
    return json.loads((run_dir / "status.json").read_text(encoding="utf-8"))


class RunsContractTests(unittest.TestCase):
    """OPS-05 / E4: summary presence under every death mode + handler lifecycle."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="phase42-contract-"))
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
    # (a) success → full member list.
    # ------------------------------------------------------------------
    def test_success_summary_has_full_member_list(self) -> None:
        name = _unique_name("success")
        cfg = self.tmp / f"{name}.yaml"
        _write_success_config(cfg, run_name=name)
        proc = self._launch(cfg)
        out, err = proc.communicate(timeout=120)
        self.assertEqual(
            proc.returncode,
            0,
            msg=f"expected exit 0\nstdout={out}\nstderr={err}",
        )
        run_dir = self._run_dir(name)
        summary = _summary_json(run_dir)

        # disposition == finished.
        self.assertEqual(summary["disposition"], "finished")
        # schema_version present.
        self.assertIn("schema_version", summary)
        # run_name present.
        self.assertEqual(summary["run_name"], name)
        # header carries the ratified fields.
        header = summary["header"]
        self.assertEqual(header["run_name"], name)
        self.assertIsNotNone(header["start_utc"])
        self.assertIsNotNone(header["end_utc"])
        self.assertIsNotNone(header["wall_clock_secs"])
        self.assertEqual(header["device"], "cpu")
        self.assertEqual(header["precision"], "float64")
        self.assertEqual(header["seed"], 11)
        self.assertIsNotNone(header["config_identity_digest"])
        self.assertIsNotNone(header["env_fingerprint"])
        # final_losses: all six canonical terms non-null for a finished run.
        final_losses = summary["final_losses"]
        for term in _LOSS_TERMS:
            self.assertIsNotNone(
                final_losses.get(term),
                msg=f"finished run should have non-null {term!r} loss",
            )
        # curriculum progression rendered (non-empty for a run that trained).
        self.assertIsInstance(summary.get("curriculum"), list)

        # The hand-over contract is the DIRECTORY, not just summary.json
        # (OPS-05 / SPEC AC "complete runs/<name>/ contract"). logs/, tb/,
        # failure/, and checkpoints/ are scaffolded at launch (train.py:301-305),
        # so every member is deterministically present on a finished run.
        for member in (
            "config.yaml",
            "checkpoints",
            "logs/train.log",
            "logs/train.log.jsonl",
            "tb",
            "summary.md",
            "summary.json",
            "status.json",
            "failure",
        ):
            self.assertTrue(
                (run_dir / member).exists(),
                msg=f"runs/<name>/{member} missing from the hand-over contract",
            )
        self.assertTrue(
            any((run_dir / "tb").rglob("events.out.tfevents*")),
            "tb/ carries no TensorBoard event data",
        )

    # ------------------------------------------------------------------
    # (a2) GAP-42-01 regression: the periodic mem: line must reach train.log
    #      in a REAL run. The pre-existing unit test called emit_mem_line
    #      itself, which proved the format and not the wiring — train.py had
    #      no caller at all, and 251/252-step runs emitted zero lines. This
    #      asserts the line lands in an actual run's log at the configured
    #      cadence, so an unwired emitter fails here.
    # ------------------------------------------------------------------
    def test_mem_line_emitted_into_real_run_train_log(self) -> None:
        name = _unique_name("mem-line")
        cfg = self.tmp / f"{name}.yaml"
        write_train_config(
            cfg,
            run={
                "run_name": name,
                "log_every": 1,
                # run.update() replaces the whole monitor block, so restate it.
                "monitor": {
                    "heartbeat_secs": 5,
                    "staleness_factor": 3,
                    "mem_every": 1,
                },
            },
            stage={"max_epochs": 2, "n_adam": 2},
        )
        proc = self._launch(cfg)
        out, err = proc.communicate(timeout=120)
        self.assertEqual(
            proc.returncode,
            0,
            msg=f"expected exit 0\nstdout={out}\nstderr={err}",
        )
        run_dir = self._run_dir(name)
        log_text = (run_dir / "logs" / "train.log").read_text(encoding="utf-8")
        mem_lines = [ln for ln in log_text.splitlines() if "mem:" in ln]
        self.assertTrue(
            mem_lines,
            "no periodic mem: line in train.log — OPS-04 / GAP-42-01",
        )
        self.assertIn("driver_bytes=", mem_lines[0])
        self.assertIn("current_bytes=", mem_lines[0])
        # The human mirror carries it; the canonical JSONL stays step-only.
        for line in (run_dir / "logs" / "train.log.jsonl").read_text(
            encoding="utf-8"
        ).splitlines():
            if line.strip():
                self.assertEqual(json.loads(line).get("event"), "step")

    # ------------------------------------------------------------------
    # (b) SIGKILL at three barriers → presence + parseable + NOT finished +
    #     staleness-decidable. SIGKILL cannot be caught, so the process dies
    #     without calling finish_run; status.json reflects the last heartbeat
    #     write (initializing or running), never a fabricated terminal state.
    # ------------------------------------------------------------------
    def _kill_and_assert_staleness(
        self,
        name: str,
        kill_barrier: str,
    ) -> None:
        """Shared SIGKILL invariant checker.

        ``kill_barrier`` ∈ {``"launch"``, ``"mid-adam"``, ``"mid-checkpoint"``}.
        """
        cfg = self.tmp / f"{name}.yaml"
        _write_long_config(cfg, run_name=name)
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            if kill_barrier == "launch":
                # Kill as soon as status.json is visible (process is in
                # heartbeat.write_initial / early transition).
                deadline = time.monotonic() + 60.0
                while time.monotonic() < deadline:
                    if (run_dir / "status.json").is_file():
                        break
                    time.sleep(0.05)
                else:
                    self.fail("status.json never appeared at launch barrier")
                # Give the heartbeat one more beat so timestamp_epoch is set.
                time.sleep(0.3)
            elif kill_barrier == "mid-adam":
                wait_for_status(
                    run_dir, pid=proc.pid, states=["running"], timeout=60.0
                )
            elif kill_barrier == "mid-checkpoint":
                wait_for_status(
                    run_dir, pid=proc.pid, states=["running"], timeout=60.0
                )
                ckpt_dir = run_dir / "checkpoints"
                # Wait until at least one rolling checkpoint is visible
                # (store naming is step-{step:06d}.pt, checkpoint.py _STEP_RE).
                deadline = time.monotonic() + 120.0
                while time.monotonic() < deadline:
                    if any(ckpt_dir.glob("step-*.pt")):
                        break
                    time.sleep(0.1)
                else:
                    self.fail("no checkpoint appeared at mid-checkpoint barrier")
            else:
                self.fail(f"unknown kill_barrier={kill_barrier!r}")

            # SIGKILL — uncatchable, no cleanup, no finish_run.
            os.kill(proc.pid, signal.SIGKILL)
            # communicate(), not wait(): it drains and closes the stdout/stderr
            # pipes, which wait() leaves open until GC (ResourceWarning noise).
            proc.communicate(timeout=30)

            # Presence: summary.json exists (written at launch by stub_summary).
            summary_path = run_dir / "summary.json"
            self.assertTrue(
                summary_path.is_file(),
                "summary.json must be present after SIGKILL (E4 presence invariant)",
            )
            # Parseable.
            summary = _summary_json(run_dir)
            self.assertIsInstance(summary, dict)

            # status.json: present + parseable.
            status = _status_json(run_dir)
            self.assertIsInstance(status, dict)

            # NOT in a fabricated terminal state.
            state = status.get("state")
            self.assertNotIn(
                state,
                _SIGKILL_FORBIDDEN_STATES,
                msg=(
                    f"SIGKILL'd run state={state!r} must not be a terminal "
                    f"state in {_SIGKILL_FORBIDDEN_STATES} — no finish_run was called"
                ),
            )

            # Staleness-DECIDABLE, not staleness-elapsed (plan 42-09 Task 2:
            # "no real wall-clock wait"): SIGKILL killed the heartbeat daemon,
            # so timestamp_epoch is final and any later reader classifies the
            # run stalled via `now - timestamp_epoch > staleness_threshold_secs`
            # from the file's own fields (CTX-75). Assert the arithmetic inputs
            # are present, numeric, and sane instead of sleeping past the
            # threshold.
            timestamp_epoch = status.get("timestamp_epoch")
            staleness_threshold = status.get("staleness_threshold_secs")
            self.assertIsNotNone(
                timestamp_epoch,
                "status.json must carry timestamp_epoch for staleness checks",
            )
            self.assertIsNotNone(
                staleness_threshold,
                "status.json must carry staleness_threshold_secs",
            )
            timestamp_epoch = float(timestamp_epoch)
            staleness_threshold = float(staleness_threshold)
            self.assertGreater(
                staleness_threshold,
                0.0,
                "staleness_threshold_secs must be a positive, finite horizon",
            )
            age = time.time() - timestamp_epoch
            # Sanity bounds prove timestamp_epoch is this run's real epoch
            # (not zero, garbage, or in the future), so the age arithmetic
            # is decidable for any reader.
            self.assertGreaterEqual(
                age,
                -2.0,
                msg=f"timestamp_epoch is in the future (age={age:.1f}s)",
            )
            self.assertLess(
                age,
                300.0,
                msg=f"timestamp_epoch is not from this run (age={age:.1f}s)",
            )
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)

    def test_sigkill_at_launch_presence_and_staleness(self) -> None:
        self._kill_and_assert_staleness(_unique_name("kill-launch"), "launch")

    def test_sigkill_mid_adam_presence_and_staleness(self) -> None:
        self._kill_and_assert_staleness(_unique_name("kill-adam"), "mid-adam")

    def test_sigkill_mid_checkpoint_presence_and_staleness(self) -> None:
        self._kill_and_assert_staleness(_unique_name("kill-ckpt"), "mid-checkpoint")

    # ------------------------------------------------------------------
    # (c) repeated-main() handler-lifecycle regression (in-process).
    #
    # Calling pinn.train.main() twice in the same interpreter must not leak
    # logging handlers, must restore the original SIGINT/SIGTERM handlers,
    # and must not produce duplicate JSONL lines from a single run.
    # ------------------------------------------------------------------
    def test_repeated_main_handler_lifecycle_regression(self) -> None:
        """In-process regression: two main() calls → handlers restored, no dup lines."""
        import logging

        import pinn.train as train_mod

        name = _unique_name("repeat")
        cfg = self.tmp / f"{name}.yaml"
        _write_success_config(cfg, run_name=name)

        # Isolate this run's runs-root.
        runs_root = self.tmp / f"repeat-runs-{os.getpid()}"
        runs_root.mkdir()
        orig_root = train_mod._RUNS_ROOT
        train_mod._RUNS_ROOT = str(runs_root)

        training_logger = logging.getLogger("pinn.training")
        baseline_handler_count = len(training_logger.handlers)
        prev_sigint = signal.getsignal(signal.SIGINT)
        prev_sigterm = signal.getsignal(signal.SIGTERM)

        try:
            # First call.
            rc1 = train_mod.main(["--config", str(cfg)])
            self.assertEqual(rc1, 0, "first main() should succeed")

            run_dir = runs_root / name
            jsonl_path = run_dir / "logs" / "train.log.jsonl"
            # No duplicate lines: each JSONL line has a unique (step, phase) pair.
            if jsonl_path.is_file():
                lines = [
                    l for l in jsonl_path.read_text(encoding="utf-8").splitlines() if l
                ]
                pairs = set()
                for line in lines:
                    rec = json.loads(line)
                    pair = (rec.get("step"), rec.get("phase"))
                    self.assertNotIn(
                        pair,
                        pairs,
                        msg=f"duplicate JSONL line at step={rec.get('step')} phase={rec.get('phase')}",
                    )
                    pairs.add(pair)

            # After main() returns, signal handlers must be restored to what
            # they were before the call (restore_handlers() in finish_run).
            self.assertEqual(
                signal.getsignal(signal.SIGINT),
                prev_sigint,
                "SIGINT handler not restored after first main()",
            )
            self.assertEqual(
                signal.getsignal(signal.SIGTERM),
                prev_sigterm,
                "SIGTERM handler not restored after first main()",
            )
            # Handler count returns to baseline (tracked handlers removed).
            self.assertEqual(
                len(training_logger.handlers),
                baseline_handler_count,
                "logging handlers leaked after first main()",
            )

            # Second call with a fresh run name (run dirs collide otherwise).
            name2 = _unique_name("repeat2")
            cfg2 = self.tmp / f"{name2}.yaml"
            _write_success_config(cfg2, run_name=name2)
            rc2 = train_mod.main(["--config", str(cfg2)])
            self.assertEqual(rc2, 0, "second main() should succeed")
            # Same invariants hold after the second call.
            self.assertEqual(signal.getsignal(signal.SIGINT), prev_sigint)
            self.assertEqual(signal.getsignal(signal.SIGTERM), prev_sigterm)
            self.assertEqual(len(training_logger.handlers), baseline_handler_count)
        finally:
            train_mod._RUNS_ROOT = orig_root


if __name__ == "__main__":
    unittest.main()
