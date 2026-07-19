"""Phase 42 / Plan 05 — TensorBoard residual panel (OPS-04b).

Realized (replacing the 42-03 stub; the ``_require`` production-symbol skip
guard is dropped — ``TbSink`` MUST exist now — while the pinn-train
availability guard is kept so a torch/tensorboard-less interpreter skips
cleanly instead of erroring at collection):

- OPS-04b presence: with ``TbSink`` attached to the
  ``pinn.training.controllers`` logger, drive the synthetic loop's real
  ``RunController._log_step`` emission point (the single CTX-65 fan-out) for
  several steps carrying the widened causal fields, then read back via
  ``EventAccumulator`` — ``residuals/bin_*`` plus
  ``causal/w_min|w_mean|w_max|front_idx`` are present with consistent step
  counts (one fan-out per widened record). ``run_stage(0)`` is not usable as
  the driver here: the synthetic Stage-0 source holds 8 records (< the
  240-record replay batch, ``StageZeroUnderpopulated``) and the stub loss
  produces no causal residuals — so the panel's widening + fan-out is
  exercised directly through the real ``_log_step``.
- Collapse/NaN: a synthetic collapsed record (``w_n -> 0``, ``front_idx=-1``,
  ``residuals_bin_00=NaN``) still emits the whole panel, and the written NaN
  reads back as NaN via ``EventAccumulator`` (``math.isnan``). Pitfall 3: the
  low-level TensorBoard event-file loader would read an on-disk NaN back as
  0.0, so readback goes through ``EventAccumulator`` exclusively.
- CTX-69 warn-once: a forced ``add_scalar`` failure logs exactly ONE warning
  to ``pinn.training.tb_sink`` and does not propagate into the step loop.
"""

from __future__ import annotations

import logging
import math
import shutil
import tempfile
import unittest
from pathlib import Path

try:  # pinn-train availability guard (torch + tensorboard live only there)
    from tensorboard.backend.event_processing.event_accumulator import (
        EventAccumulator,
    )

    from pinn.training.tb_sink import TbSink
    from tests.phase42._fixtures import make_synthetic_stage0_loop

    _PINN_TRAIN_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only outside pinn-train
    EventAccumulator = None
    TbSink = None
    make_synthetic_stage0_loop = None
    _PINN_TRAIN_AVAILABLE = False


@unittest.skipUnless(_PINN_TRAIN_AVAILABLE, "pinn-train env not available")
class ResidualPanelTests(unittest.TestCase):
    """OPS-04b: TensorBoard residual panel consumes residuals_bin_* from widened record."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase42-tbpanel-"))
        self.tb_dir = self.tmp / "tb"
        self.sink = TbSink(self.tb_dir)
        # Attach to the real emission logger (RunController._log_step emits
        # here); force INFO so step records are not level-filtered.
        self.logger = logging.getLogger("pinn.training.controllers")
        self._old_level = self.logger.level
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.sink)

    def tearDown(self):
        self.logger.removeHandler(self.sink)
        self.sink.close()
        self.logger.setLevel(self._old_level)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _accumulator(self):
        self.sink.flush()  # push queued events to disk before readback
        acc = EventAccumulator(str(self.tb_dir))
        acc.Reload()
        return acc

    def test_ops04b_panel_present_via_event_accumulator(self):
        """Real _log_step fan-out: residuals/bin_* + causal/* present, counts consistent."""
        loop = make_synthetic_stage0_loop()
        rc = loop["run_controller"]

        # Drive the REAL controllers._log_step emission point (the single
        # CTX-65 fan-out) for several steps, each carrying the widened causal
        # fields. This exercises the genuine widening logic — the
        # ``residuals_bin_{n:02d}`` enumeration and the ``w_min/.../front_idx``
        # extraction in controllers.py — feeding the same ``pinn.training``
        # logger TbSink is attached to. ``run_stage(0)`` cannot be the driver
        # (8-record source < 240-record replay batch; stub loss emits no causal
        # residuals), so the panel's widened-record -> TbSink integration is
        # tested here directly. 16 bins mirrors the loop's
        # ``CollocationSampler(collocation_count=16)``.
        n_bins = 16
        n_steps = 3
        for i in range(n_steps):
            rc._log_step(
                step=i,
                loss_terms=rc._scalar_loss_terms(0.5),
                lr=1e-3,
                phase="2a",
                stage=0,
                grad_norm=1.0,
                w_n_stats={
                    "w_min": 0.1,
                    "w_mean": 0.5,
                    "w_max": 0.9,
                    "front_idx": i,
                },
                residuals_per_bin=[float(i + n) for n in range(n_bins)],
            )

        acc = self._accumulator()
        tags = acc.Tags()["scalars"]

        # Per-bin residuals: bin_00 plus other bins (16 collocation bins).
        bin_tags = [t for t in tags if t.startswith("residuals/bin_")]
        self.assertIn("residuals/bin_00", bin_tags)
        self.assertGreaterEqual(
            len(bin_tags), 2, f"expected multiple residual bins, got {bin_tags}",
        )

        # Causal-weight stats under the CTX-70 namespace.
        causal_tags = (
            "causal/w_min",
            "causal/w_mean",
            "causal/w_max",
            "causal/front_idx",
        )
        for tag in causal_tags:
            self.assertIn(tag, tags, f"missing {tag}; tags={sorted(tags)}")

        # Expected step counts: every panel tag sees the SAME number of
        # logged steps (one fan-out per widened record) — exactly n_steps.
        counts = {
            tag: len(acc.Scalars(tag))
            for tag in ("residuals/bin_00",) + causal_tags
        }
        self.assertTrue(
            all(c >= 1 for c in counts.values()),
            f"panel tags must have >=1 event each: {counts}",
        )
        self.assertEqual(
            len(set(counts.values())), 1,
            f"panel tags diverged from the shared record fan-out: {counts}",
        )
        self.assertEqual(
            counts["residuals/bin_00"], n_steps,
            f"expected {n_steps} events per panel tag (1:1 fan-out): {counts}",
        )

    def test_ops04b_collapse_nan_roundtrip(self):
        """Collapsed w_n / NaN residual: panel STILL emits; NaN survives readback."""
        collapsed = {
            "event": "step",
            "step": 1,
            "stage": 0,
            "phase": "2a",
            # Causal collapse: w_n -> 0 and the propagation front stalled
            # (front_idx=-1 is the 42-01 default=-1 fallback — a REAL reading
            # that must emit, not a missing field).
            "w_min": 0.0,
            "w_mean": 0.0,
            "w_max": 0.0,
            "front_idx": -1,
            "residuals_bin_00": float("nan"),
            "residuals_bin_01": 2.0,
        }
        self.logger.info("step", extra=collapsed)

        acc = self._accumulator()
        tags = acc.Tags()["scalars"]

        # The panel emits even under collapse/NaN — that is its purpose.
        for tag in (
            "residuals/bin_00",
            "residuals/bin_01",
            "causal/w_min",
            "causal/w_mean",
            "causal/w_max",
            "causal/front_idx",
        ):
            self.assertIn(tag, tags, f"panel tag missing under collapse: {tag}")

        # NaN survives the EventAccumulator round trip (Pitfall 3: the
        # low-level event-file loader would read it back as 0.0).
        nan_events = acc.Scalars("residuals/bin_00")
        self.assertGreaterEqual(len(nan_events), 1)
        self.assertTrue(
            any(math.isnan(e.value) for e in nan_events),
            f"NaN did not survive EventAccumulator readback: {nan_events}",
        )

        # Collapsed readings are emitted as real values (0.0 is not skipped;
        # -1 is the propagation-front-stall signal an operator needs).
        self.assertEqual(acc.Scalars("causal/w_min")[-1].value, 0.0)
        self.assertEqual(acc.Scalars("causal/front_idx")[-1].value, -1.0)

    def test_ctx69_warn_once_on_add_scalar_failure(self):
        """Forced add_scalar failure: one warning, never propagates (CTX-69)."""

        def _boom(*args, **kwargs):
            raise RuntimeError("forced add_scalar failure")

        self.sink._writer.add_scalar = _boom
        with self.assertLogs("pinn.training.tb_sink", level="WARNING") as cm:
            # Two failing emissions; neither may raise into the step loop.
            self.logger.info(
                "step", extra={"event": "step", "step": 1, "w_min": 0.5},
            )
            self.logger.info(
                "step", extra={"event": "step", "step": 2, "w_min": 0.6},
            )
        warnings = [r for r in cm.records if "add_scalar" in r.getMessage()]
        self.assertEqual(
            len(warnings), 1,
            f"warn-ONCE latch broken; got {len(warnings)}: {cm.records}",
        )


if __name__ == "__main__":
    unittest.main()
