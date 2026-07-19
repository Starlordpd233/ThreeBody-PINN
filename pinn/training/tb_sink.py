"""Phase 42 / Plan 05 — TensorBoard sink: secondary step view + residual panel.

OPS-03 (CTX-69): a ``torch.utils.tensorboard.SummaryWriter``-backed
``logging.Handler`` fed from the SAME widened ``_log_step`` ``extra=`` record
as the JSONL sink (CTX-65 single emission point). JSONL stays canonical
(D2); TB is the derived, always-on secondary view. ``add_scalar`` enqueues
onto the writer's OWN background event-writer thread — no synchronous
plotting of any kind in the step loop (CTX-69 async constraint).

OPS-04b (CTX-70): per logged step the panel emits ``residuals/bin_{n:02d}``
for each collocation time-bin (from the ``residuals_bin_{n:02d}`` record
fields — the TB-only family the 42-04 JSONL handler filters out, cycle-2
review finding HIGH-1, so this sink is their SOLE consumer) plus
``causal/w_min``, ``causal/w_mean``, ``causal/w_max``, ``causal/front_idx``
(= ``max{n : w_n > 0.5}``) from the ``w_*``/``front_idx`` fields. The
``causal/*`` namespace is the TB-side rename, distinct from the JSONL
canonical keys. Emission is UNCONDITIONAL: guard-tripped, collapsed, and
NaN steps are exactly the diagnostic signal (causal-weight collapse +
propagation-front stall), and ``add_scalar`` accepts NaN and 0.0 floats.
``front_idx`` emits even when ``-1`` — a stalled propagation front is the
reading an operator needs (cycle-2 agy HIGH); only ``None`` (field absent
this step) is skipped.

Monitoring must never abort training (CTX-69): SummaryWriter construction
and every ``add_scalar``/``flush``/``close`` call are wrapped in a warn-once
guard — the first failure logs ONE warning to ``pinn.training.tb_sink`` and
later failures stay silent. (RESEARCH Pitfall 7: the default ``max_queue``
can block a full queue; unlikely at ``log_every=100`` and accepted as a
documented slowdown, threat T-42-04 — never an exception.)

Composition: the class is importable/pure (``torch`` is imported lazily in
``__init__``); INSTANTIATION happens only at the composition root
(``train.py`` main, 42-08) with ``log_dir=runs/<name>/tb/`` (Anti-Pattern
#5). ``close()`` flushes/closes the writer for the terminal path.
"""

from __future__ import annotations

import logging
from pathlib import Path

_LOGGER = logging.getLogger("pinn.training.tb_sink")

# Canonical widened-record scalars mirrored as TB tags under their registry
# names (the OPS-03 secondary view of the step record). The w_* / front_idx
# fields are deliberately ABSENT here — in TB they live under the CTX-70
# ``causal/*`` namespace instead, and ``residuals_bin_*`` maps to
# ``residuals/bin_*``; both are handled separately in ``emit``.
_SCALAR_TAGS = (
    "total",
    "loss_data",
    "loss_ic",
    "loss_phys",
    "loss_energy",
    "loss_angmom",
    "lambda_data",
    "lambda_ic",
    "lambda_phys",
    "lambda_e",
    "lambda_l",
    "grad_norm",
    "lr",
    "s_per_step",
    "eta_seconds",
)

# OPS-04b causal-weight stats → ``causal/*`` TB namespace (CTX-70).
_CAUSAL_FIELDS = ("w_min", "w_mean", "w_max", "front_idx")

# Record-field prefix for the per-bin residual family (OPS-04b, TB-only).
_RESIDUALS_PREFIX = "residuals_bin_"


class TbSink(logging.Handler):
    """SummaryWriter-backed ``logging.Handler`` for the TB secondary view.

    Attaches to the ``pinn.training`` tree exactly like the 42-04 handlers:
    ``emit`` consumes the widened ``extra=`` step record (``event=="step"``)
    and fans it out to TensorBoard. Non-step records are ignored.

    Null policy: a field that is ``None`` (absent this step — e.g. the w_n
    stash is unset, or ``eta_seconds`` before the EMA warms) is simply not
    plotted for that step. NaN/±Inf pass through to ``add_scalar`` — the
    panel exists to surface them. ``0.0`` and ``-1`` are real readings
    (collapsed weights / stalled front) and are always emitted.

    Attributes
    ----------
    log_dir : Path
        The SummaryWriter log directory (``runs/<name>/tb/`` at the
        composition root).
    """

    def __init__(self, log_dir):
        super().__init__()
        self.log_dir = Path(log_dir)
        self._writer = None
        self._warned = False
        try:
            from torch.utils.tensorboard import SummaryWriter

            self._writer = SummaryWriter(log_dir=str(self.log_dir))
        except Exception as exc:  # CTX-69: warn once, never abort training
            self._warn_once(
                "TbSink: SummaryWriter unavailable (%s); TB panel disabled", exc,
            )

    def _warn_once(self, msg, *args):
        """Log ONE warning per sink lifetime; later failures stay silent."""
        if not self._warned:
            self._warned = True
            _LOGGER.warning(msg, *args)

    def _add_scalar(self, tag, value, step):
        # None = field absent this step (skip); NaN/0.0/-1 are real readings
        # and emit (the panel's diagnostic purpose).
        if value is None:
            return
        try:
            self._writer.add_scalar(tag, value, step)
        except Exception as exc:
            self._warn_once(
                "TbSink: add_scalar(%s) failed (%s); further TB failures silent",
                tag,
                exc,
            )

    def emit(self, record):
        try:
            if getattr(record, "event", None) != "step":
                return
            if self._writer is None:
                return
            d = record.__dict__
            step = d.get("step")
            # OPS-03 secondary view: canonical widened scalars.
            for key in _SCALAR_TAGS:
                self._add_scalar(key, d.get(key), step)
            # OPS-04b panel: per-bin residuals + causal-weight stats.
            for key, value in d.items():
                if key.startswith(_RESIDUALS_PREFIX):
                    self._add_scalar(
                        f"residuals/bin_{key[len(_RESIDUALS_PREFIX):]}",
                        value,
                        step,
                    )
            for name in _CAUSAL_FIELDS:
                self._add_scalar(f"causal/{name}", d.get(name), step)
        except Exception as exc:  # monitoring never aborts training (CTX-69)
            self._warn_once(
                "TbSink: emit failed (%s); further TB failures silent", exc,
            )

    def flush(self):
        if self._writer is not None:
            try:
                self._writer.flush()
            except Exception as exc:
                self._warn_once("TbSink: flush failed (%s)", exc)

    def close(self):
        try:
            if self._writer is not None:
                self._writer.close()  # flushes pending events (terminal path)
        except Exception as exc:
            self._warn_once("TbSink: close failed (%s)", exc)
        finally:
            self._writer = None
        super().close()


__all__ = ["TbSink"]
