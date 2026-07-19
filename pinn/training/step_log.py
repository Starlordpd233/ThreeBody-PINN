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
"""

from __future__ import annotations

from typing import Any

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
    "step_completed": {
        "provisional": True,
        "provenance": (
            "EMISSION-COMPLETENESS METADATA (not a B-2 loss/metric field): "
            "boolean flag indicating the step record was fully assembled; "
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
            "grad_norm, w_n stats (w_min/w_mean/w_max/front_idx), lr, "
            "s_per_step, eta_seconds, step_completed. Residuals_bin_* is "
            "TB-only (OPS-04b). finite/nonfinite_keys are sink-added "
            "(CTX-67). Owner-ratify the final list before run #1."
        ),
    }


__all__ = [
    "STEP_LOG_FIELDS",
    "step_log_fields_provisional_entry",
]
