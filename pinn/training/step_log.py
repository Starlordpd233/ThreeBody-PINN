"""Phase 42 — provisional STEP_LOG_FIELDS registry (OPS-03 / ⚖ B-2 seam).

Names every CANONICAL JSONL step-record key emitted by
``RunController._log_step`` (cycle-2 review finding HIGH-1, claude +
verification pass).  The registry is provisional — the owner ratifies the
final list before run #1.  Do NOT present it as ratified.

Parity exceptions (deliberately absent from this registry):
  * ``finite`` and ``nonfinite_keys`` — sink-added by 42-04's
    ``_sanitize_step_record`` (CTX-67 E1 non-finite policy).  The
    field-parity check (42-04) treats them as documented sink-added
    exceptions.
  * ``residuals_bin_{n:02d}`` — OPS-04b TensorBoard-only.  Emitted into
    the shared widened ``extra=`` record by 42-01, FILTERED OUT of the
    JSONL serialization by 42-04's handler, and consumed by 42-05's TB
    sink.  Deliberately absent so the 42-04 parity check on a JSONL line
    holds without a dynamic-key carve-out (cycle-2 review finding HIGH-1).
    Under the Phase 56/57 amended recipe this is the NORMALIZED
    (``Rtilde = Rbar / R_ref``) per-bin residual family.
  * ``raw_residuals_bin_{n:02d}`` — Phase 57 Task 3, the RAW (un-normalized)
    counterpart to ``residuals_bin_{n:02d}`` above.  Same TB-only filtering
    discipline: excluded from this registry so it is dropped from the JSONL
    line and consumed only by the TB sink's ``raw_residuals/bin_*`` panel.
"""

from __future__ import annotations

import json
import logging
import math
from pathlib import Path
from typing import Any, Mapping, Optional


# ⚖ PROVISIONAL — B-2 field set awaiting owner ratification before run #1.
# Pinned to the names the live ``_log_step`` actually emits so the 42-04
# parity assertion holds.  Additive keys are non-breaking (JSONL readers
# ignore unknown keys).
STEP_LOG_FIELDS: dict[str, dict[str, Any]] = {
    # ---- step discriminator ----
    "event": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): JSONL step-record event discriminator; "
            "owner-ratify before run #1"
        ),
    },
    # ---- step identity ----
    "step": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): global step counter; "
            "owner-ratify before run #1"
        ),
    },
    "stage": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): curriculum stage index; "
            "owner-ratify before run #1"
        ),
    },
    "phase": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): curriculum phase label; "
            "owner-ratify before run #1"
        ),
    },
    "epoch": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): epoch within current stage; "
            "owner-ratify before run #1"
        ),
    },
    # ---- loss terms (emitted via **{f"loss_{k}": v for k, v in terms.items()}) ----
    "loss_data": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): data loss term (LossWeights.lambda_data); "
            "owner-ratify before run #1"
        ),
    },
    "loss_ic": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): IC loss term (LossWeights.lambda_ic); "
            "owner-ratify before run #1"
        ),
    },
    "loss_phys": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): physics loss term (LossWeights.lambda_phys); "
            "owner-ratify before run #1"
        ),
    },
    "loss_energy": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): energy loss term (LossWeights.lambda_e); "
            "owner-ratify before run #1"
        ),
    },
    "loss_angmom": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): angular-momentum loss term "
            "(LossWeights.lambda_l); owner-ratify before run #1"
        ),
    },
    "total": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): total weighted loss; "
            "owner-ratify before run #1"
        ),
    },
    # ---- λ weight vector (matching LossWeights dataclass field names) ----
    "lambda_data": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): ScheduledWeights λ_data; "
            "owner-ratify before run #1"
        ),
    },
    "lambda_ic": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): ScheduledWeights λ_ic; "
            "owner-ratify before run #1"
        ),
    },
    "lambda_phys": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): ScheduledWeights λ_phys; "
            "owner-ratify before run #1"
        ),
    },
    "lambda_e": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): ScheduledWeights λ_e (NOT lambda_energy — "
            "matches LossWeights field name); owner-ratify before run #1"
        ),
    },
    "lambda_l": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): ScheduledWeights λ_l (NOT lambda_angmom — "
            "matches LossWeights field name); owner-ratify before run #1"
        ),
    },
    # ---- gradient / weight stats ----
    "grad_norm": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): gradient norm (pre-existing guard hook "
            "computation); owner-ratify before run #1"
        ),
    },
    "grad_norm_raw_data": {
        "provisional": True,
        "provenance": (
            "INST-02: global parameter-gradient L2 norm of the unweighted "
            "data term; owner-ratify before run #1"
        ),
    },
    "grad_norm_raw_ic": {
        "provisional": True,
        "provenance": (
            "INST-02: global parameter-gradient L2 norm of the unweighted "
            "initial-condition term; owner-ratify before run #1"
        ),
    },
    "grad_norm_raw_phys": {
        "provisional": True,
        "provenance": (
            "INST-02: global parameter-gradient L2 norm of the unweighted "
            "physics term; owner-ratify before run #1"
        ),
    },
    "grad_norm_raw_energy": {
        "provisional": True,
        "provenance": (
            "INST-02: global parameter-gradient L2 norm of the unweighted "
            "energy term; owner-ratify before run #1"
        ),
    },
    "grad_norm_raw_angmom": {
        "provisional": True,
        "provenance": (
            "INST-02: global parameter-gradient L2 norm of the unweighted "
            "angular-momentum term; owner-ratify before run #1"
        ),
    },
    "grad_norm_applied_data": {
        "provisional": True,
        "provenance": (
            "INST-02: lambda_data times raw data gradient norm; "
            "owner-ratify before run #1"
        ),
    },
    "grad_norm_applied_ic": {
        "provisional": True,
        "provenance": (
            "INST-02: lambda_ic times raw initial-condition gradient norm; "
            "owner-ratify before run #1"
        ),
    },
    "grad_norm_applied_phys": {
        "provisional": True,
        "provenance": (
            "INST-02: lambda_phys times raw physics gradient norm; "
            "owner-ratify before run #1"
        ),
    },
    "grad_norm_applied_energy": {
        "provisional": True,
        "provenance": (
            "INST-02: lambda_e times raw energy gradient norm; "
            "owner-ratify before run #1"
        ),
    },
    "grad_norm_applied_angmom": {
        "provisional": True,
        "provenance": (
            "INST-02: lambda_l times raw angular-momentum gradient norm; "
            "owner-ratify before run #1"
        ),
    },
    "grad_stats_provenance": {
        "provisional": True,
        "provenance": (
            "INST-02: optimizer-graph provenance for the ten gradient norms; "
            "owner-ratify before run #1"
        ),
    },
    "grad_stats_complete": {
        "provisional": True,
        "provenance": (
            "INST-02: all ten gradient norms are present and finite; "
            "owner-ratify before run #1"
        ),
    },
    "w_min": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): min causal weight w_n; "
            "owner-ratify before run #1"
        ),
    },
    "w_mean": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): mean causal weight w_n; "
            "owner-ratify before run #1"
        ),
    },
    "w_max": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): max causal weight w_n; "
            "owner-ratify before run #1"
        ),
    },
    "front_idx": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): causal propagation front index "
            "max{n : w_n > 0.5}; owner-ratify before run #1"
        ),
    },
    # ---- Phase 56/57 amended-recipe R_ref / allocation provenance ----
    "r_ref": {
        "provisional": True,
        "provenance": (
            "Phase 56/57 (SPEC-01/SPEC-06; 54-RULING.md): the frozen R_ref "
            "that normalized this step's causal exponent and outer physics "
            "loss (residuals_bin_* is the resulting NORMALIZED per-bin "
            "residual family; raw_residuals_bin_* is the RAW, un-normalized "
            "TB-only counterpart); owner-ratify before run #1"
        ),
    },
    "n_collocation_rows": {
        "provisional": True,
        "provenance": (
            "Phase 56/57: exact physics collocation row count this step's "
            "causal loss was computed over (the ratified recipe is exactly "
            "4096); a separate verifier uses this to reject the old "
            "anchor-only path; owner-ratify before run #1"
        ),
    },
    "n_bins": {
        "provisional": True,
        "provenance": (
            "Phase 56/57: the fixed bin count (ratified M=16) the physics "
            "residual was reduced to before the causal loss consumed it; "
            "owner-ratify before run #1"
        ),
    },
    # ---- timing / optimizer ----
    "lr": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): current learning rate; "
            "owner-ratify before run #1"
        ),
    },
    "s_per_step": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): wall-clock seconds per step; "
            "owner-ratify before run #1"
        ),
    },
    "eta_seconds": {
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2): estimated time remaining (seconds); "
            "owner-ratify before run #1"
        ),
    },
    # ---- emission-completeness metadata (NOT a B-2 loss/metric field) ----
    "record_complete": {
        "provisional": True,
        "provenance": (
            "EMISSION-COMPLETENESS METADATA (not a B-2 loss/metric field): "
            "boolean flag indicating the step record was fully assembled -- "
            "the call-site optimizer fact AND all ten gradient norms present "
            "and finite. It is NOT an optimizer-advancement flag: a normally "
            "advanced step whose telemetry is incomplete is false here. Read "
            "the optimizer question from the guard/failure emission path and "
            "the telemetry question from grad_stats_complete; "
            "owner-ratify before run #1"
        ),
    },
}


def step_log_fields_provisional_entry() -> dict[str, Any]:
    """``provisional_fields()`` entry for the B-2 step-log registry seam."""
    return {
        "name": "step_log_fields_registry",
        "value": "PROVISIONAL",
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-2 / OPS-03): STEP_LOG_FIELDS in "
            "pinn.training.step_log names the canonical JSONL step-record "
            "vocabulary — event, step/stage/phase/epoch, five loss terms "
            "(loss_data/loss_ic/loss_phys/loss_energy/loss_angmom), total, "
            "λ vector (lambda_data/lambda_ic/lambda_phys/lambda_e/lambda_l), "
            "grad_norm plus ten INST-02 raw/applied per-term gradient norms, "
            "their provenance/completeness metadata, w_n stats "
            "(w_min/w_mean/w_max/front_idx), the Phase 56/57 amended-recipe "
            "r_ref/n_collocation_rows/n_bins allocation provenance, lr, "
            "s_per_step, eta_seconds, record_complete. Residuals_bin_* "
            "(NORMALIZED) and raw_residuals_bin_* (RAW) are both "
            "TB-only (OPS-04b). finite/nonfinite_keys are sink-added "
            "(CTX-67). Owner-ratify the final list before run #1."
        ),
    }


def _sanitize_step_record(record: Mapping[str, Any]) -> dict:
    """CTX-67 non-finite null policy for step records.

    Replaces every non-finite numeric value (NaN/±Inf) with ``None`` and
    augments the record with ``finite`` (``False`` iff any field was
    non-finite) and ``nonfinite_keys`` (sorted list of affected field
    names). A fully-finite record gets ``finite: True`` and
    ``nonfinite_keys: []``.

    The returned dict serializes with ``json.dumps(..., allow_nan=False)``
    without raising. String sentinels (``"NaN"``/``"Inf"``/``"-Inf"``)
    never appear — non-finite fields become JSON ``null``. This is a
    separate sanitizer: do NOT import
    ``pinn.training.guards._json_safe_scalar`` (its string-sentinel policy
    is trip.json-local, Anti-Pattern #1). Non-numeric fields (``phase``,
    ``stage``, ``record_complete``, etc.) pass through unchanged.
    """
    out: dict[str, Any] = {}
    nonfinite_keys: list[str] = []
    for k, v in record.items():
        try:
            nonfinite = not math.isfinite(v)
        except TypeError:
            nonfinite = False
        if nonfinite:
            out[k] = None
            nonfinite_keys.append(k)
        else:
            out[k] = v
    out["finite"] = len(nonfinite_keys) == 0
    out["nonfinite_keys"] = sorted(nonfinite_keys)
    return out


class JsonlStepHandler(logging.Handler):
    """Append-only JSONL ``logging.Handler`` for the canonical step log.

    Writes one parseable JSON object per ``event=="step"`` record to
    ``train.log.jsonl`` (OPS-03), filtering the widened ``extra=`` record
    to the canonical ``STEP_LOG_FIELDS`` vocabulary. The
    ``residuals_bin_*`` family is excluded (TB-only, OPS-04b) so the
    registry-vs-JSONL parity assertion holds without a dynamic-key
    carve-out (cycle-2 review finding HIGH-1). Each record passes through
    ``_sanitize_step_record`` (CTX-67 null policy) and serializes with
    ``json.dumps(allow_nan=False)``.

    The file is opened once in ``"a"`` mode; each record is written and
    flushed (no ``os.fsync``, no atomic-rename — Anti-Pattern #4).

    Attributes
    ----------
    last_step_finite : Optional[bool]
        Updated to the sanitized record's ``finite`` value on each
        successful step emit. ``None`` until the first step is emitted.
        Read by the 42-08 terminal-cause discriminator in-memory so it
        need not re-parse ``train.log.jsonl`` from disk (cycle-2 review
        finding, agy MEDIUM).
    """

    def __init__(self, path):
        super().__init__()
        self.path = Path(path)
        self._f = self.path.open("a", encoding="utf-8")
        self.last_step_finite: Optional[bool] = None

    def emit(self, record):
        try:
            if getattr(record, "event", None) != "step":
                return
            # Filter to the canonical OPS-03 vocabulary (cycle-2 review
            # finding HIGH-1): iterate STEP_LOG_FIELDS and pull each named
            # key from the widened record. This EXCLUDES residuals_bin_*
            # (TB-only, OPS-04b) so the parity assertion holds without a
            # carve-out.
            obj = {k: record.__dict__.get(k) for k in STEP_LOG_FIELDS}
            sanitized = _sanitize_step_record(obj)
            line = json.dumps(sanitized, allow_nan=False)
            self._f.write(line + "\n")
            self._f.flush()
            self.last_step_finite = sanitized["finite"]
        except Exception:
            self.handleError(record)

    def flush(self):
        if hasattr(self, "_f"):
            self._f.flush()

    def close(self):
        if hasattr(self, "_f"):
            self._f.close()
        super().close()


def _format_step_line(d: Mapping[str, Any]) -> str:
    """Render a step record as the design §5.4 pipe-delimited line."""

    def _fmt(v):
        if v is None:
            return "null"
        if isinstance(v, float):
            return f"{v:.6g}"
        return str(v)

    return (
        f"step {d.get('step')} | "
        f"stage {d.get('stage')} phase {d.get('phase')} | "
        f"total={_fmt(d.get('total'))} "
        f"data={_fmt(d.get('loss_data'))} "
        f"ic={_fmt(d.get('loss_ic'))} "
        f"phys={_fmt(d.get('loss_phys'))} "
        f"energy={_fmt(d.get('loss_energy'))} "
        f"angmom={_fmt(d.get('loss_angmom'))} | "
        f"lr={_fmt(d.get('lr'))} | "
        f"{_fmt(d.get('s_per_step'))} s/step | "
        f"ETA {d.get('eta_seconds')}"
    )


class HumanStepHandler(logging.Handler):
    """Human-readable mirror of the step log (design §5.4 line shape).

    Renders step records into the pipe-delimited line and non-step events
    (run start, mem:, stage dispositions, guard trips) into readable lines
    without crashing on records lacking step fields.
    """

    def __init__(self, path):
        super().__init__()
        self.path = Path(path)
        self._f = self.path.open("a", encoding="utf-8")

    def emit(self, record):
        try:
            d = record.__dict__
            if d.get("event") == "step":
                line = _format_step_line(d)
            else:
                try:
                    msg = record.getMessage()
                except Exception:
                    msg = str(d.get("msg", ""))
                line = f"[{d.get('event', '')}] {msg}"
            self._f.write(line + "\n")
            self._f.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        if hasattr(self, "_f"):
            self._f.flush()

    def close(self):
        if hasattr(self, "_f"):
            self._f.close()
        super().close()


__all__ = [
    "STEP_LOG_FIELDS",
    "step_log_fields_provisional_entry",
    "_sanitize_step_record",
    "JsonlStepHandler",
    "HumanStepHandler",
]
