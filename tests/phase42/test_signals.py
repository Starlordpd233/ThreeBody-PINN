"""Phase 42 / Plan 09 — signal handling (OPS-02 / E2).

Subprocess-based tests driving a real ``python -m pinn.train``. Each case
launches a dataset-free synthetic run, polls ``runs/<name>/status.json`` for
the deterministic readiness barrier (state in {``"running"``} + pid match —
a subset of the plan's allowed {``"initializing"``, ``"running"``} that
guarantees the SIGINT/SIGTERM handlers installed in ``main()`` are live,
CTX-71), then delivers signals and asserts the exit code, checkpoint
atomicity, and terminal disposition.

E2 invariants (must-haves):
    SIGINT-once → checkpoint written + exit 130 + ``status.json state ==
    "interrupted"``. SIGTERM → graceful checkpoint + exit 143. Two SIGINTs
    within the ~1 s debounce coalesce into one graceful stop; a deliberate
    second SIGINT outside the window escalates to ``os._exit(130)`` with no
    further checkpoint. Checkpoints are atomic (temp+rename — no abandoned
    ``.tmp``).
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Optional

from tests.phase42._fixtures import (
    _CONDA_PYTHON,
    launch_train,
    wait_for_status,
    write_train_config,
)

# Debounce window in pinn/training/signals.py (SignalState.debounce_secs).
_DEBOUNCE_SECS = 1.0

# Documented ceiling for the escalate-path exit latency (cycle-2 claude-glm
# MEDIUM): on_escalate only flushes handlers and flips status, so it must
# return in bounded time and never deadlock on logging locks.
_ESCALATE_LATENCY_CEIL = 5.0


def _unique_name(test_name: str) -> str:
    """Per-case unique run_name so concurrent tests don't collide on runs/<name>."""
    return f"sig-{test_name}-{os.getpid()}"


def _write_signal_config(
    path: Path,
    *,
    run_name: str,
    max_epochs: int = 200,
    n_adam: int = 50,
    lbfgs_max_iter: int = 2,
    validation_every: int = 50,
    loss_explosion_ceiling: float = 1.0e12,
) -> Path:
    """Write a long-running synthetic config tuned for signal delivery."""
    return write_train_config(
        path,
        run={"run_name": run_name, "log_every": 1},
        stage={
            "max_epochs": max_epochs,
            "n_adam": n_adam,
        },
        opt={
            "lbfgs_max_iter": lbfgs_max_iter,
            "validation_every": validation_every,
        },
        guards={"loss_explosion_ceiling": loss_explosion_ceiling},
    )


def _wait_for_jsonl_phase(
    run_dir: Path,
    phase: str,
    *,
    timeout: float = 120.0,
    poll: float = 0.1,
) -> None:
    """Block until ``train.log.jsonl`` contains a record with ``phase``."""
    jsonl = run_dir / "logs" / "train.log.jsonl"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if jsonl.is_file():
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("phase") == phase:
                    return
        time.sleep(poll)
    raise TimeoutError(
        f"never observed phase={phase!r} in {jsonl} within {timeout}s"
    )


def _count_checkpoints(ckpt_dir: Path) -> int:
    """Number of visible ``.pt`` checkpoints (excludes ``.tmp.*`` temps)."""
    return len([p for p in ckpt_dir.glob("*.pt") if ".tmp." not in p.name])


def _has_abandoned_tmp(ckpt_dir: Path) -> bool:
    """True if any ``.tmp.{pid}`` temp is left behind (atomicity violation)."""
    return bool(list(ckpt_dir.glob("*.tmp.*")))


def _proc_alive(proc: subprocess.Popen) -> bool:
    return proc.poll() is None


class SignalStateLogicTests(unittest.TestCase):
    """Deterministic two-point Nyquist bracket over the debounce LOGIC.

    The subprocess cases below deliver real signals, but whether the process
    survives long enough for a second press is machine-timing-dependent (the
    graceful teardown on this synthetic workload can complete in under W/5).
    This class pins the two-point bracket — coalesce well INSIDE the window,
    escalate well OUTSIDE — directly on ``note_signal``, the pure function the
    SIGINT handler dispatches on, so the bracket itself never races.
    """

    def _fresh_state(self):
        from pinn.training.signals import SignalState

        return SignalState()

    def test_first_press_is_graceful(self) -> None:
        from pinn.training.signals import note_signal

        state = self._fresh_state()
        self.assertEqual(note_signal(state, 100.0), "graceful")
        self.assertTrue(state.stop_requested)
        self.assertFalse(state.escalate)

    def test_second_press_inside_window_coalesces(self) -> None:
        from pinn.training.signals import note_signal

        w = self._fresh_state().debounce_secs
        for gap in (w / 5.0, w / 3.0):  # well inside, per the E2 bracket
            state = self._fresh_state()
            note_signal(state, 100.0)
            self.assertEqual(
                note_signal(state, 100.0 + gap),
                "graceful",
                msg=f"second press at +{gap:.2f}s must coalesce, not escalate",
            )
            self.assertFalse(state.escalate)
            self.assertTrue(state.stop_requested)

    def test_second_press_outside_window_escalates(self) -> None:
        from pinn.training.signals import note_signal

        w = self._fresh_state().debounce_secs
        for gap in (1.5 * w, 2.0 * w):  # well outside, per the E2 bracket
            state = self._fresh_state()
            note_signal(state, 100.0)
            self.assertEqual(
                note_signal(state, 100.0 + gap),
                "escalate",
                msg=f"second press at +{gap:.2f}s must escalate",
            )
            self.assertTrue(state.escalate)


class SignalTests(unittest.TestCase):
    """OPS-02 / E2: signal-race two-point debounce bracket + exit codes."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="phase42-signals-"))
        self.runs_root = self.tmp / "runs"
        self.runs_root.mkdir()

    def tearDown(self) -> None:
        # Best-effort cleanup; ignore errors from in-use files.
        import shutil

        shutil.rmtree(self.tmp, ignore_errors=True)

    def _launch(self, cfg: Path) -> subprocess.Popen[str]:
        return launch_train(cfg, self.runs_root)

    def _run_dir(self, run_name: str) -> Path:
        return self.runs_root / run_name

    # ------------------------------------------------------------------
    # (a) SIGINT once → checkpoint + exit 130 + status interrupted.
    # ------------------------------------------------------------------
    def test_sigint_once_checkpoints_and_exits_130(self) -> None:
        name = _unique_name("sigint-once")
        cfg = self.tmp / f"{name}.yaml"
        _write_signal_config(cfg, run_name=name)
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            status = wait_for_status(
                run_dir, pid=proc.pid, states=["running"], timeout=60.0
            )
            self.assertEqual(status["state"], "running")
            os.kill(proc.pid, signal.SIGINT)
            out, err = proc.communicate(timeout=60)
            self.assertEqual(
                proc.returncode,
                130,
                msg=f"expected exit 130, got {proc.returncode}\nstdout={out}\nstderr={err}",
            )
            ckpt_dir = run_dir / "checkpoints"
            self.assertTrue(
                (ckpt_dir / "latest.pt").is_file(),
                "expected a checkpoint (latest.pt) after graceful SIGINT",
            )
            self.assertFalse(
                _has_abandoned_tmp(ckpt_dir),
                "abandoned .tmp violates checkpoint atomicity",
            )
            final_status = json.loads(
                (run_dir / "status.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                final_status["state"],
                "interrupted",
                msg=f"status={final_status}",
            )
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)

    # ------------------------------------------------------------------
    # (b) SIGTERM → graceful checkpoint + exit 143.
    # ------------------------------------------------------------------
    def test_sigterm_graceful_exit_143(self) -> None:
        name = _unique_name("sigterm")
        cfg = self.tmp / f"{name}.yaml"
        _write_signal_config(cfg, run_name=name)
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            wait_for_status(run_dir, pid=proc.pid, states=["running"], timeout=60.0)
            os.kill(proc.pid, signal.SIGTERM)
            out, err = proc.communicate(timeout=60)
            self.assertEqual(
                proc.returncode,
                143,
                msg=f"expected exit 143, got {proc.returncode}\nstdout={out}\nstderr={err}",
            )
            self.assertTrue(
                (run_dir / "checkpoints" / "latest.pt").is_file(),
                "expected a checkpoint after graceful SIGTERM",
            )
            final_status = json.loads(
                (run_dir / "status.json").read_text(encoding="utf-8")
            )
            self.assertEqual(final_status["state"], "interrupted")
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)

    # ------------------------------------------------------------------
    # (c) Second SIGINT INSIDE debounce (W/5-W/3) → coalesces, single
    #     graceful exit path (still exit 130, one checkpoint).
    # ------------------------------------------------------------------
    def test_sigint_twice_inside_debounce_coalesces(self) -> None:
        name = _unique_name("coalesce")
        cfg = self.tmp / f"{name}.yaml"
        # L-BFGS closure is the slowest per-step operation — keeps the
        # process alive through the second SIGINT.
        _write_signal_config(
            cfg, run_name=name, lbfgs_max_iter=20, max_epochs=200, n_adam=50
        )
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            wait_for_status(run_dir, pid=proc.pid, states=["running"], timeout=60.0)
            # Wait until L-BFGS (phase 2b) is active so the first SIGINT
            # lands during a long closure eval and the process survives to
            # receive the second SIGINT inside the debounce window.
            _wait_for_jsonl_phase(run_dir, "2b", timeout=180.0)
            before = _count_checkpoints(run_dir / "checkpoints")
            os.kill(proc.pid, signal.SIGINT)
            time.sleep(_DEBOUNCE_SECS / 5)  # W/5 — well inside the 1 s window.
            if not _proc_alive(proc):
                # Graceful teardown beat the second press (machine-dependent:
                # the stop seam fires within one closure eval and teardown can
                # complete in under W/5 on this workload). The coalesce branch
                # itself is pinned deterministically by SignalStateLogicTests;
                # here the graceful-path invariants must still hold — the same
                # accepted fallback shape as the escalate case below.
                out, err = proc.communicate()
                self.assertEqual(proc.returncode, 130)
                # Not a count assertion — see the escalate case: retention
                # eviction makes the visible .pt count non-monotone.
                self.assertTrue(
                    (run_dir / "checkpoints" / "latest.pt").is_file(),
                    "graceful path should have committed a checkpoint",
                )
                self.assertFalse(
                    _has_abandoned_tmp(run_dir / "checkpoints"),
                    "abandoned .tmp violates checkpoint atomicity",
                )
                final_status = json.loads(
                    (run_dir / "status.json").read_text(encoding="utf-8")
                )
                self.assertEqual(final_status["state"], "interrupted")
                return
            os.kill(proc.pid, signal.SIGINT)
            out, err = proc.communicate(timeout=60)
            # Two encodings of the same disposition, "exited on SIGINT after a
            # single graceful stop": 130 when the process reaches its own
            # sys.exit, and -SIGINT when the second press lands after
            # finish_run() restored the default disposition (train.py:380 —
            # interpreter/torch teardown is not instantaneous). A shell reports
            # 128+2 = 130 for both. The handlers stay installed for the whole of
            # finish_run(), so a restored disposition proves the checkpoint,
            # status transition, and summary already landed — asserted below,
            # which is what distinguishes this from an escalated kill.
            self.assertIn(
                proc.returncode,
                (130, -signal.SIGINT),
                msg=f"expected exit 130 (coalesced), got {proc.returncode}"
                f"\nstdout={out}\nstderr={err}",
            )
            after = _count_checkpoints(run_dir / "checkpoints")
            # Coalesced: the second SIGINT did NOT escalate, so the graceful
            # path completed normally (one checkpoint batch, not an abrupt
            # os._exit mid-checkpoint).
            self.assertGreaterEqual(
                after, before, "no checkpoint after coalesced SIGINT"
            )
            self.assertTrue(
                (run_dir / "checkpoints" / "latest.pt").is_file(),
                "expected a checkpoint (latest.pt) after the coalesced stop",
            )
            self.assertFalse(
                _has_abandoned_tmp(run_dir / "checkpoints"),
                "abandoned .tmp violates checkpoint atomicity",
            )
            final_status = json.loads(
                (run_dir / "status.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                final_status["state"],
                "interrupted",
                msg="a coalesced double-SIGINT must still finalize the graceful "
                f"terminal transition; status={final_status}",
            )
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)

    # ------------------------------------------------------------------
    # (d) Second SIGINT OUTSIDE debounce (1.5W-2W) → escalates to
    #     os._exit(130), no further checkpoint, bounded exit latency.
    # ------------------------------------------------------------------
    def test_sigint_twice_outside_debounce_escalates(self) -> None:
        name = _unique_name("escalate")
        cfg = self.tmp / f"{name}.yaml"
        _write_signal_config(
            cfg, run_name=name, lbfgs_max_iter=20, max_epochs=200, n_adam=50
        )
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            wait_for_status(run_dir, pid=proc.pid, states=["running"], timeout=60.0)
            _wait_for_jsonl_phase(run_dir, "2b", timeout=180.0)
            before = _count_checkpoints(run_dir / "checkpoints")
            os.kill(proc.pid, signal.SIGINT)
            # Wait OUTSIDE the debounce window so the second SIGINT is a
            # distinct press, not a coalesced repeat.
            time.sleep(_DEBOUNCE_SECS * 1.5)
            if not _proc_alive(proc):
                # Graceful exit completed before the second press — the
                # escalation branch wasn't exercised, but the invariant
                # (no extra checkpoint, atomic) still holds.
                out, err = proc.communicate()
                self.assertEqual(proc.returncode, 130)
                # Not a count assertion: save_rolling() evicts under retention
                # (checkpoint.py _evict_rolling), so the visible .pt count
                # plateaus rather than incrementing. latest.pt plus the terminal
                # transition is the durable graceful-path evidence.
                self.assertTrue(
                    (run_dir / "checkpoints" / "latest.pt").is_file(),
                    "graceful path should have committed a checkpoint",
                )
                self.assertFalse(
                    _has_abandoned_tmp(run_dir / "checkpoints"),
                    "abandoned .tmp violates checkpoint atomicity",
                )
                final_status = json.loads(
                    (run_dir / "status.json").read_text(encoding="utf-8")
                )
                self.assertEqual(final_status["state"], "interrupted")
                return
            t0 = time.monotonic()
            os.kill(proc.pid, signal.SIGINT)
            out, err = proc.communicate(timeout=60)
            latency = time.monotonic() - t0
            self.assertEqual(
                proc.returncode,
                130,
                msg=f"expected exit 130 (escalated), got {proc.returncode}"
                f"\nstdout={out}\nstderr={err}",
            )
            # Bounded escalate latency (cycle-2 claude-glm MEDIUM):
            # on_escalate must not deadlock on logging locks.
            self.assertLess(
                latency,
                _ESCALATE_LATENCY_CEIL,
                msg=f"escalate path took {latency:.2f}s (ceil {_ESCALATE_LATENCY_CEIL}s)",
            )
            after = _count_checkpoints(run_dir / "checkpoints")
            # Escalation aborts mid-checkpoint — no NEW visible .pt beyond
            # what the graceful path had already committed.
            self.assertLessEqual(
                after,
                before + 1,
                msg=f"escalation should not add a second checkpoint: before={before}, after={after}",
            )
            # Atomicity: an os._exit mid-checkpoint must never leave a
            # partial .tmp behind (the store writes to .tmp.{pid} then
            # renames; an abandoned .tmp would be a torn artifact).
            self.assertFalse(
                _has_abandoned_tmp(run_dir / "checkpoints"),
                "abandoned .tmp after escalate violates atomic checkpoint invariant",
            )
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)

    # ------------------------------------------------------------------
    # (e) Intra-L-BFGS-closure stop (HIGH-2): SIGINT mid-closure fires
    #     the _StopRequested seam BETWEEN closure evaluations, proving
    #     the stop is not deferred to the epoch boundary. Exit 130 within
    #     a latency SHORTER than the configured lbfgs_max_iter budget.
    # ------------------------------------------------------------------
    def test_sigint_mid_lbfgs_closure_stops_between_evals(self) -> None:
        name = _unique_name("lbfgs-closure")
        # lbfgs_max_iter sizing: large enough that a full step's line-search
        # budget (~tens of seconds on this landscape) dwarfs the exit-latency
        # ceiling, but small enough that the FIRST step(closure) returns —
        # the phase-2b JSONL barrier record lands only after that return
        # (max_iter=50 ground past the barrier timeout; 42-09 failing case #4).
        lbfgs_max_iter = 20
        cfg = self.tmp / f"{name}.yaml"
        _write_signal_config(
            cfg,
            run_name=name,
            lbfgs_max_iter=lbfgs_max_iter,
            max_epochs=200,
            n_adam=50,
        )
        proc = self._launch(cfg)
        try:
            run_dir = self._run_dir(name)
            wait_for_status(run_dir, pid=proc.pid, states=["running"], timeout=60.0)
            # Barrier (plan-prescribed): at least one Adam→L-BFGS transition
            # observed in train.log.jsonl — a phase-2b record proves L-BFGS is
            # active. The record lands only after the FIRST step(closure)
            # returns (status.json cannot serve here: the heartbeat's `phase`
            # field is pushed from the step-log hook, also post-step), so the
            # SIGINT below lands inside the SECOND step's line search, whose
            # full budget dwarfs the exit-latency ceiling asserted after it.
            _wait_for_jsonl_phase(run_dir, "2b", timeout=180.0)
            t0 = time.monotonic()
            os.kill(proc.pid, signal.SIGINT)
            out, err = proc.communicate(timeout=120)
            latency = time.monotonic() - t0
            self.assertEqual(
                proc.returncode,
                130,
                msg=f"expected exit 130, got {proc.returncode}\nstdout={out}\nstderr={err}",
            )
            # The stop fired between closure evaluations (CTX-71), not at
            # the epoch boundary — so exit latency is bounded well below
            # what a full lbfgs_max_iter line-search budget would take.
            # A full 50-iter line search on this synthetic workload is
            # materially slower than this ceiling; the observed prompt exit
            # proves the _StopRequested seam fired between closure evals.
            self.assertLess(
                latency,
                _ESCALATE_LATENCY_CEIL,
                msg=(
                    f"mid-closure stop took {latency:.2f}s — too slow to prove "
                    f"the _StopRequested seam fired between closure evaluations "
                    f"(lbfgs_max_iter={lbfgs_max_iter})"
                ),
            )
            # Graceful checkpoint written on the stop path.
            self.assertTrue(
                (run_dir / "checkpoints" / "latest.pt").is_file(),
                "expected checkpoint after mid-closure stop",
            )
            self.assertFalse(
                _has_abandoned_tmp(run_dir / "checkpoints"),
                "abandoned .tmp violates checkpoint atomicity",
            )
        finally:
            if _proc_alive(proc):
                proc.kill()
                proc.wait(timeout=10)


if __name__ == "__main__":
    unittest.main()
