"""Phase 42 / Plan 06 — status heartbeat writer tests (OPS-04a / E3). Realized.

Verifies the ``status.json`` liveness + honesty surface built by plan 42-06:

* OPS-04a — snapshots across the initializing → running → finished/interrupted
  sequence; a reader classifies running-vs-stalled from ``timestamp_epoch`` age
  alone using the file's own carried ``staleness_threshold_secs``; a ``mem:``
  field/line is present.
* E3 startup — the ``initializing`` snapshot has ``step: null`` and null losses
  (never fabricated — Anti-Pattern #7).
* E3 atomicity — many concurrent ``atomic_write_text``-backed rewrites while a
  polling reader ``json.loads`` the file repeatedly; every read is a complete
  parseable object (never a torn read).
* E3 staleness — the classification is pure arithmetic on ``timestamp_epoch``
  (manipulated directly; no real wall-clock wait for K seconds).
* Memory-sampling discipline (cycle-2, claude MEDIUM) — the daemon ``run()`` body
  contains no ``torch.mps.*`` call; MPS is main-thread-sampled and pushed via
  ``update(mem=...)``.

The per-symbol production-symbol skip is DROPPED (the symbols are realized); the
pinn-train availability guard is KEPT.
"""

from __future__ import annotations

import inspect
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path

from tests.phase42 import _SKIP_PHRASE

MODULE = "pinn.training.heartbeat"

# pinn-train availability guard (KEPT): skip the suite when torch / the production
# module is unavailable. The per-symbol production-symbol skip is dropped — the
# symbols below are realized by plan 42-06.
try:
    import torch  # noqa: F401  (pinn-train provides torch)
    from pinn.training.heartbeat import (  # noqa: F401
        HeartbeatThread,
        build_status_snapshot,
        emit_mem_line,
        sample_memory_fields,
        write_status,
    )

    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False


def _snap(**overrides):
    """Build a representative running snapshot; tests override individual fields."""
    base = dict(
        state="running",
        run_name="r",
        pid=1,
        step=0,
        stage=0,
        phase="adam",
        epoch=0,
        losses={"data": 0.1, "ic": 0.1, "phys": 0.1, "energy": 0.1, "angmom": 0.1, "total": 0.5},
        lr=1e-3,
        s_per_step_ema=0.5,
        eta_seconds=100.0,
        mem=None,
        heartbeat_secs=30,
        staleness_factor=3,
    )
    base.update(overrides)
    return build_status_snapshot(**base)


def _reader_classify_stalled(snapshot, now=None):
    """A status.json reader's stall test (CTX-75): stalled iff
    ``now - timestamp_epoch > staleness_threshold_secs``, using ONLY the file's own
    carried fields (no external constant)."""
    if now is None:
        now = time.time()
    return (now - snapshot["timestamp_epoch"]) > snapshot["staleness_threshold_secs"]


@unittest.skipUnless(_AVAILABLE, f"{_SKIP_PHRASE} {MODULE} (pinn-train not available)")
class StatusHeartbeatTests(unittest.TestCase):
    """OPS-04a / E3: liveness classification, startup null-loss initializing,
    atomic never-truncated rewrite, self-describing staleness."""

    # ---- (b) E3 startup -------------------------------------------------------
    def test_initializing_snapshot_has_null_step_and_losses(self):
        s = _snap(state="initializing", step=None, losses=None, mem=None)
        self.assertEqual(s["state"], "initializing")
        self.assertIsNone(s["step"])
        # Null losses, never fabricated (Anti-Pattern #7).
        self.assertTrue(all(v is None for v in s["losses"].values()))
        # Self-describing staleness.
        self.assertEqual(s["heartbeat_interval_secs"], 30)
        self.assertEqual(s["staleness_threshold_secs"], 90)
        # Strict JSON: parseable under allow_nan=False.
        json.dumps(s, allow_nan=False)

    def test_nonfinite_loss_serializes_as_null(self):
        s = _snap(losses={"total": float("nan"), "data": float("inf"), "phys": 0.25})
        self.assertIsNone(s["losses"]["total"])
        self.assertIsNone(s["losses"]["data"])
        self.assertEqual(s["losses"]["phys"], 0.25)
        json.dumps(s, allow_nan=False)  # no NaN/Inf escapes

    # ---- (a) OPS-04a state sequence + (d) staleness arithmetic ----------------
    def test_state_sequence_reader_classification_and_staleness_arithmetic(self):
        for state in ("initializing", "running", "finished", "interrupted", "failed"):
            step = None if state == "initializing" else 0
            s = _snap(state=state, step=step, heartbeat_secs=1, staleness_factor=2)
            self.assertEqual(s["state"], state)
            self.assertEqual(s["staleness_threshold_secs"], 2)
            # Fresh snapshot → not stalled (age ≈ 0 < threshold).
            self.assertFalse(_reader_classify_stalled(s))
            # Manipulate timestamp_epoch directly (NO real wall-clock wait): age it
            # past the carried threshold → stalled.
            aged = dict(s)
            aged["timestamp_epoch"] = s["timestamp_epoch"] - (s["staleness_threshold_secs"] + 5)
            self.assertTrue(_reader_classify_stalled(aged))

    # ---- (a) OPS-04a mem field + line ----------------------------------------
    def test_mem_field_mirrored_and_mem_line_emitted(self):
        # mem=None → memory fields null.
        s0 = _snap(mem=None)
        self.assertIsNone(s0["memory"]["driver_bytes"])
        self.assertIsNone(s0["memory"]["current_bytes"])
        # Pre-sampled mem (main-thread) → mirrored into the snapshot.
        s1 = _snap(mem={"driver_bytes": 123, "current_bytes": 456})
        self.assertEqual(s1["memory"]["driver_bytes"], 123)
        self.assertEqual(s1["memory"]["current_bytes"], 456)
        # The periodic mem: line is emitted via the heartbeat logger (main thread).
        with self.assertLogs("pinn.training.heartbeat", level="INFO") as cm:
            emit_mem_line({"driver_bytes": 123, "current_bytes": 456})
        self.assertTrue(any("mem:" in line for line in cm.output))

    def test_sample_memory_fields_returns_int_or_null(self):
        fields = sample_memory_fields()
        self.assertIn("driver_bytes", fields)
        self.assertIn("current_bytes", fields)
        for key in ("driver_bytes", "current_bytes"):
            self.assertTrue(fields[key] is None or isinstance(fields[key], int))

    # ---- write_status round-trip ---------------------------------------------
    def test_write_status_round_trips_complete_json(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "status.json"
            write_status(path, _snap(state="running", losses={"total": 1.0}))
            loaded = json.loads(path.read_text())
            self.assertEqual(loaded["state"], "running")
            self.assertEqual(loaded["losses"]["total"], 1.0)

    # ---- (c) E3 atomicity -----------------------------------------------------
    def test_no_torn_read_under_concurrent_rewrites(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "status.json"
            # Daemon on a fast cadence PLUS synchronous main-thread updates → many
            # concurrent atomic rewrites from two writers (serialized by the mutex).
            hb = HeartbeatThread(
                path, heartbeat_secs=0.01, staleness_factor=3, run_name="r", pid=1
            )
            hb.write_initial()  # seed a complete file so the reader never sees absence
            stop = threading.Event()
            errors = []
            n_reads = [0]

            def reader():
                while not stop.is_set():
                    try:
                        text = path.read_text()
                    except FileNotFoundError:
                        continue
                    if not text:
                        continue
                    try:
                        json.loads(text)
                        n_reads[0] += 1
                    except json.JSONDecodeError as exc:  # a torn read
                        errors.append(exc)

            reader_thread = threading.Thread(target=reader)
            reader_thread.start()
            hb.start()
            try:
                for i in range(400):
                    hb.update(step=i, losses={"total": float(i)})
            finally:
                stop.set()
                reader_thread.join(timeout=5)
                hb.stop()
                hb.join(timeout=3)

            self.assertEqual(errors, [], f"torn read detected: {errors[:3]}")
            self.assertGreater(n_reads[0], 0)

    # ---- CTX-74 liveness: frozen step still heartbeats ------------------------
    def test_frozen_step_count_still_refreshes_timestamp(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "status.json"
            hb = HeartbeatThread(
                path, heartbeat_secs=0.02, staleness_factor=3, run_name="r", pid=1
            )
            hb.write_initial()
            hb.update(step=7)  # frozen step count (e.g. a long L-BFGS line search)
            hb.start()
            try:
                first = json.loads(path.read_text())
                t1 = first["timestamp_epoch"]
                time.sleep(0.15)  # several cadence ticks
                second = json.loads(path.read_text())
                t2 = second["timestamp_epoch"]
            finally:
                hb.stop()
                hb.join(timeout=3)
            self.assertEqual(second["step"], 7)  # step still frozen
            self.assertGreater(t2, t1)  # timestamp refreshed → process is live
            self.assertFalse(_reader_classify_stalled(second))  # fresh → not stalled

    # ---- memory-sampling discipline (cycle-2, claude MEDIUM) ------------------
    def test_daemon_run_body_has_no_mps_call(self):
        src = inspect.getsource(HeartbeatThread.run)
        self.assertNotIn("torch.mps", src)

    # ---- thread-safety: transition() and daemon tick share the lock ----------
    def test_transition_forces_synchronous_rewrite(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "status.json"
            hb = HeartbeatThread(
                path, heartbeat_secs=100, staleness_factor=3, run_name="r", pid=1
            )
            hb.write_initial()
            self.assertEqual(json.loads(path.read_text())["state"], "initializing")
            hb.transition("running")  # synchronous rewrite, no cadence wait
            self.assertEqual(json.loads(path.read_text())["state"], "running")
            hb.transition("finished")
            self.assertEqual(json.loads(path.read_text())["state"], "finished")


if __name__ == "__main__":
    unittest.main()
