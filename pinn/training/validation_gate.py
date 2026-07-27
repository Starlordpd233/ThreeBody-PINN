"""INST-01 gate-aligned validation observation (Phase 46, plan 46-03).

Composes ``pinn.verification.gate_metrics`` over the COMPLETE current-stage
validation pool at the existing validation-event boundary, producing the
per-trajectory ``epsilon_H`` / SCS conservation signal EVAL-01 precondition
(iii) requires, plus its versioned atomic sidecar and the compact
``validation.jsonl`` field producer.

This module owns WHAT the observation contains; Plan 46-07's hook wiring owns
WHEN it runs (no scheduling logic, trigger condition, cadence, or config option
lives here — D-10). It is observation-only (D-15): it mutates no loss, weight,
optimizer, scheduler, stage-exit, replay, checkpoint-rank, or early-stop state;
its only effects are the returned observation and the sidecar its caller
publishes.

Frame-explicit (D-12): the position/time pair is an explicit, recorded
``FrameConvention``. Only the two COHERENT pairs are accepted — scaled positions
with normalized time ``u = t / T_CHARACTERISTIC_TIME`` (the locked contract), and
raw positions with raw native time (present ONLY so an owner-ratified D-09
outcome is expressible without a code change). The gate's time coordinate is
constructed in exactly one place (``gate_time_coordinate``), so the GAP-46-01
pairing failure — physics-frame positions handed to gate_metrics with raw native
times — cannot arise by omission.

``pinn.evaluate.py`` is the read-only precedent for the per-trajectory eval/no_grad
loop shape; its raw-times pairing at ``evaluate.py:407`` is the GAP-46-01
anti-pattern this module structurally cannot repeat. This module NEVER imports
``pinn.evaluate`` (D-16) and never reimplements a gate-metric formula (D-13/D-26)
or the atomic write primitive (``pinn.training.atomic_io.atomic_write_text``).
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.training import atomic_io
from pinn.verification import gate_metrics

__all__ = [
    "GATE_SIDECAR_SCHEMA_VERSION",
    "POSITION_FRAME_SCALED",
    "POSITION_FRAME_RAW",
    "TIME_COORD_NORMALIZED",
    "TIME_COORD_RAW",
    "MASS_CONVENTION_ORDERED_RAW",
    "COHERENT_FRAME_PAIRS",
    "FrameConvention",
    "IncoherentFrameError",
    "ValidationGateUnavailable",
    "TrajectoryGateRow",
    "ValidationGateObservation",
    "json_safe_float",
    "gate_time_coordinate",
    "build_gate_inputs",
    "compute_validation_gate",
    "sidecar_relative_path",
    "publish_gate_sidecar",
    "validate_sidecar_payload",
    "compact_validation_fields",
]

GATE_SIDECAR_SCHEMA_VERSION = "phase46-validation-gate/v1"

POSITION_FRAME_SCALED = "r_prime"
POSITION_FRAME_RAW = "r_raw"
TIME_COORD_NORMALIZED = "u_t_over_T"
TIME_COORD_RAW = "t_native"
MASS_CONVENTION_ORDERED_RAW = "ordered_raw"

# The only position/time pairs a coherent conservation measurement can use. The
# scaled pair (r_prime, u=t/T) is the locked contract; the raw pair exists ONLY
# to express an owner-ratified D-09 branch outcome, never as a default.
COHERENT_FRAME_PAIRS = frozenset({
    (POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED),
    (POSITION_FRAME_RAW, TIME_COORD_RAW),
})

_NAN_SENTINEL = "NaN"
_POS_INF_SENTINEL = "Infinity"
_NEG_INF_SENTINEL = "-Infinity"
_SENTINELS = frozenset({_NAN_SENTINEL, _POS_INF_SENTINEL, _NEG_INF_SENTINEL})


class IncoherentFrameError(ValueError):
    """Raised when a FrameConvention pairs a position frame with an incoherent
    time coordinate (GAP-46-01 pairing made structurally impossible)."""


class ValidationGateUnavailable(RuntimeError):
    """Raised when no validation observation can be produced (empty eligible
    pool, or a sidecar that compact_validation_fields cannot durably confirm).
    The event is an instrumentation failure that makes the run ineligible,
    never a silent fallback to loss-only validation (D-20)."""


@dataclass(frozen=True)
class FrameConvention:
    """Explicit, recorded position/time/mass convention for one gate pass.

    ``conf01_evidence_ref`` carries the CONF-01 verdict/evidence reference that
    ratified this frame (D-18); the production constant lands in Plan 46-07.
    """

    position_frame: str
    time_coord: str
    mass_convention: str
    conf01_evidence_ref: str

    def __post_init__(self):
        if (self.position_frame, self.time_coord) not in COHERENT_FRAME_PAIRS:
            raise IncoherentFrameError(
                f"incoherent frame pair: position_frame={self.position_frame!r} "
                f"time_coord={self.time_coord!r}; accepted pairs={sorted(COHERENT_FRAME_PAIRS)}"
            )


@dataclass(frozen=True)
class TrajectoryGateRow:
    """One trajectory's gate evidence in the observation."""

    record_key: object
    eps_h: float
    scs: float


@dataclass(frozen=True)
class ValidationGateObservation:
    """The full-pool, frame-explicit conservation observation (D-11/D-14/D-18)."""

    schema_version: str
    global_step: int
    stage: int
    split: str
    frame: FrameConvention
    n_trajectories: int
    rows: tuple
    n_nonfinite: int
    eps_h_reject_threshold: float
    scs_reject_threshold: float
    aggregate_eps_h: float
    aggregate_scs: float
    verdict: str
    gate_status: str


# ---------------------------------------------------------------------------
# Frame coordinate + model-facing input
# ---------------------------------------------------------------------------


def gate_time_coordinate(times, frame: FrameConvention) -> torch.Tensor:
    """The gate-metrics time coordinate for ``times`` under ``frame``.

    Float64 CPU tensor. Under ``TIME_COORD_NORMALIZED`` returns ``times / T``;
    under ``TIME_COORD_RAW`` returns ``times`` unchanged. This is the ONLY place
    the gate's time coordinate is constructed, so the GAP-46-01 pairing cannot
    arise by omission.
    """
    t = torch.as_tensor(times, dtype=torch.float64, device=torch.device("cpu")).detach()
    if frame.time_coord == TIME_COORD_NORMALIZED:
        return t / float(T_CHARACTERISTIC_TIME)
    if frame.time_coord == TIME_COORD_RAW:
        return t
    raise IncoherentFrameError(f"unknown time_coord {frame.time_coord!r}")


def build_gate_inputs(times, ic13, *, dtype, device) -> torch.Tensor:
    """The model-facing ``(N, 14)`` input for one record's snapshots.

    ``tau = 2 * (times / T) - 1`` concatenated with the record's ``ic13`` broadcast
    to ``(N, 13)`` — the identical map ``pinn/data/batches.py:271-273`` applies. The
    network leaf ALWAYS uses the locked tau map regardless of the gate frame; the
    FrameConvention governs only the pair handed to gate_metrics. Implemented
    locally because the held-out evaluator's private equivalent may not be
    imported (D-16).
    """
    t = torch.as_tensor(times, dtype=dtype, device=device).detach().reshape(-1)
    tau = (2.0 * (t / float(T_CHARACTERISTIC_TIME)) - 1.0).reshape(-1, 1)
    ic = torch.as_tensor(ic13, dtype=dtype, device=device).detach().reshape(13)
    ic_batch = ic.reshape(1, 13).expand(int(tau.shape[0]), 13)
    return torch.cat([tau, ic_batch], dim=1)


# ---------------------------------------------------------------------------
# Full-pool gate computation
# ---------------------------------------------------------------------------


def compute_validation_gate(
    model,
    validation_source,
    *,
    stage,
    global_step,
    frame: FrameConvention,
    dtype=torch.float64,
    device=torch.device("cpu"),
) -> ValidationGateObservation:
    """Compose gate_metrics over the complete current-stage validation pool.

    Sorted ``records_at_or_below(stage)``, one detached no-grad forward per
    record, prior train/eval mode restored even on error (D-12). Empty pool
    raises ``ValidationGateUnavailable`` (D-20). PASS/FAIL comes ONLY from
    gate_metrics (D-13); no formula is reimplemented here.
    """
    keys = sorted(validation_source.records_at_or_below(int(stage)))
    if not keys:
        raise ValidationGateUnavailable(
            f"validation gate unavailable: stage={stage} pool=records_at_or_below("
            f"{int(stage)}) is empty; the run is ineligible (D-20)"
        )

    prior_training = bool(model.training)
    rows = []
    try:
        model.eval()
        with torch.no_grad():
            for key in keys:
                record = validation_source.get(key)
                times = torch.as_tensor(
                    validation_source.snapshot_times(key),
                    dtype=torch.float64,
                    device=torch.device("cpu"),
                ).detach()
                inputs = build_gate_inputs(times, record.ic13, dtype=dtype, device=device)
                masses_batch = (
                    torch.as_tensor(record.masses, dtype=dtype, device=device)
                    .detach()
                    .reshape(3)
                    .reshape(1, 3)
                    .expand(int(inputs.shape[0]), 3)
                )
                predicted = model(inputs, masses_batch)
                predicted_positions = (
                    torch.as_tensor(predicted, dtype=torch.float64, device=torch.device("cpu"))
                    .detach()
                    .reshape(-1, 3, 3)
                )
                gate_time = gate_time_coordinate(times, frame)
                masses_vec = (
                    torch.as_tensor(record.masses, dtype=torch.float64)
                    .detach()
                    .reshape(3)
                )
                metrics = gate_metrics.compute_trajectory_gate_metrics(
                    predicted_positions, gate_time, masses_vec
                )
                eps_h = float(metrics.eps_h)
                rows.append(
                    TrajectoryGateRow(
                        record_key=key,
                        eps_h=eps_h,
                        scs=float(gate_metrics.scs_from_eps_h(eps_h)),
                    )
                )
    finally:
        # Restore the PRIOR mode (strictly stronger than the evaluator's
        # unconditional train() restore). Handler-less try/finally: an exception
        # propagates AFTER restoration.
        if prior_training:
            model.train()
        else:
            model.eval()

    aggregate = gate_metrics.aggregate_gate_verdict([row.eps_h for row in rows])
    n_nonfinite = sum(1 for row in rows if not math.isfinite(row.eps_h))
    return ValidationGateObservation(
        schema_version=GATE_SIDECAR_SCHEMA_VERSION,
        global_step=int(global_step),
        stage=int(stage),
        split="validation",
        frame=frame,
        n_trajectories=len(rows),
        rows=tuple(rows),
        n_nonfinite=n_nonfinite,
        eps_h_reject_threshold=float(gate_metrics.GATE_EPS_H_REJECT_THRESHOLD),
        scs_reject_threshold=float(gate_metrics.GATE_SCS_REJECT_THRESHOLD),
        aggregate_eps_h=float(aggregate.eps_h),
        aggregate_scs=float(aggregate.scs),
        verdict=str(aggregate.verdict),
        gate_status="ok",
    )


# ---------------------------------------------------------------------------
# Serialization: json-safe floats, sidecar path, atomic publish, validation
# ---------------------------------------------------------------------------


def json_safe_float(value):
    """Map non-finite floats to JSON string sentinels; finite floats unchanged.

    NaN -> "NaN", +inf -> "Infinity", -inf -> "-Infinity". Applied to EVERY
    per-row and aggregate metric during serialization so ``validation.jsonl``'s
    ``allow_nan=False`` cannot raise and a genuinely non-finite eps_H is preserved
    with a FAIL verdict rather than null-collapsed or dropped (D-20).

    This is the OPPOSITE policy of the null-collapsing summary helper in
    ``pinn.training.summary`` (correct for its own human-summary fields), which
    must NEVER be applied to verdict-bearing gate fields (D-20).
    """
    v = float(value)
    if math.isnan(v):
        return _NAN_SENTINEL
    if math.isinf(v):
        return _POS_INF_SENTINEL if v > 0 else _NEG_INF_SENTINEL
    return v


def _is_json_safe_metric(value) -> bool:
    """A metric value is JSON-safe iff it is a finite number OR one sentinel."""
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    return isinstance(value, str) and value in _SENTINELS


def sidecar_relative_path(global_step) -> str:
    """Fixed run-relative sidecar path ``validation_gate/step-<8-digit>.json``.

    The step is validated as a non-negative integer (bool rejected); the fixed
    pattern has no user-controlled path segment, so neither an absolute path nor
    a parent-directory escape is constructible.
    """
    if isinstance(global_step, bool):
        raise ValueError(f"global_step must be a non-negative integer, not bool: {global_step!r}")
    try:
        n = int(global_step)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"global_step must be a non-negative integer: {global_step!r}"
        ) from exc
    if n < 0:
        raise ValueError(f"global_step must be non-negative: {n}")
    return f"validation_gate/step-{n:08d}.json"


def _record_key_triple(record_key):
    return {
        "variant": record_key.variant,
        "fidelity": record_key.fidelity,
        "id": int(record_key.id),
    }


def _observation_payload(observation: ValidationGateObservation, run_dir_name: str) -> dict:
    return {
        "schema_version": observation.schema_version,
        "run_dir": run_dir_name,
        "sidecar_path": sidecar_relative_path(observation.global_step),
        "global_step": int(observation.global_step),
        "stage": int(observation.stage),
        "split": observation.split,
        "frame": {
            "position_frame": observation.frame.position_frame,
            "time_coord": observation.frame.time_coord,
            "mass_convention": observation.frame.mass_convention,
            "conf01_evidence_ref": observation.frame.conf01_evidence_ref,
        },
        "n_trajectories": int(observation.n_trajectories),
        "rows": [
            {
                "record_key": _record_key_triple(row.record_key),
                "eps_h": json_safe_float(row.eps_h),
                "scs": json_safe_float(row.scs),
            }
            for row in observation.rows
        ],
        "n_nonfinite": int(observation.n_nonfinite),
        "eps_h_reject_threshold": float(observation.eps_h_reject_threshold),
        "scs_reject_threshold": float(observation.scs_reject_threshold),
        "aggregate_eps_h": json_safe_float(observation.aggregate_eps_h),
        "aggregate_scs": json_safe_float(observation.aggregate_scs),
        "verdict": observation.verdict,
        "gate_status": observation.gate_status,
    }


def publish_gate_sidecar(run_dir, observation: ValidationGateObservation) -> str:
    """Durably publish the sidecar under ``run_dir``; return its relative path.

    The sidecar is written via ``atomic_io.atomic_write_text`` (tmp+fsync+replace+
    dir-fsync) BEFORE any pointer field is produced (D-17). Serialization is
    ``sort_keys`` with a trailing newline; metric values are json-safe; the run
    identity is the run directory NAME plus the sidecar's own relative path only
    (never an absolute path).
    """
    rel = sidecar_relative_path(observation.global_step)
    base = Path(run_dir).resolve()
    dest = (base / rel).resolve()
    try:
        dest.relative_to(base)  # containment guard (defence in depth)
    except ValueError as exc:
        raise ValidationGateUnavailable(f"sidecar escapes run_dir: {dest}") from exc

    payload = _observation_payload(observation, run_dir_name=Path(run_dir).name)
    text = json.dumps(payload, sort_keys=True, separators=(", ", ": "), allow_nan=False) + "\n"
    atomic_io.atomic_write_text(dest, text)
    return rel


_REQUIRED_TOP_KEYS = frozenset({
    "schema_version", "run_dir", "sidecar_path", "global_step", "stage", "split",
    "frame", "n_trajectories", "rows", "n_nonfinite", "eps_h_reject_threshold",
    "scs_reject_threshold", "aggregate_eps_h", "aggregate_scs", "verdict",
    "gate_status",
})


def validate_sidecar_payload(payload) -> dict:
    """Fail-closed structural validation of a parsed sidecar payload.

    Raises ``ValueError`` with a reason on any violation; returns the payload on
    success. A schema-invalid payload is NOT a durable validation-gate record
    (D-20) — this checker is what the D-19 summary projection (46-07) and the
    eligibility semantics stand on.
    """
    if not isinstance(payload, dict):
        raise ValueError(f"payload must be a JSON object; got {type(payload).__name__}")
    if payload.get("schema_version") != GATE_SIDECAR_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version mismatch: {payload.get('schema_version')!r} "
            f"(expected {GATE_SIDECAR_SCHEMA_VERSION!r})"
        )
    missing = _REQUIRED_TOP_KEYS - payload.keys()
    if missing:
        raise ValueError(f"missing required keys: {sorted(missing)}")

    rows = payload["rows"]
    if not isinstance(rows, list):
        raise ValueError(f"rows must be a list; got {type(rows).__name__}")
    if len(rows) != payload["n_trajectories"]:
        raise ValueError(
            f"row count {len(rows)} != n_trajectories {payload['n_trajectories']}"
        )

    def _triple(row):
        rk = row["record_key"]
        return (rk["variant"], rk["fidelity"], int(rk["id"]))

    triples = []
    for row in rows:
        rk = row.get("record_key")
        if not isinstance(rk, dict) or not {"variant", "fidelity", "id"} <= rk.keys():
            raise ValueError(f"row missing record_key triple: {rk!r}")
        for fld in ("eps_h", "scs"):
            if not _is_json_safe_metric(row.get(fld)):
                raise ValueError(f"row {fld} not finite-or-sentinel: {row.get(fld)!r}")
        triples.append(_triple(row))
    if triples != sorted(triples):
        raise ValueError("rows are not sorted by record_key triple (variant, fidelity, id)")

    for fld in ("aggregate_eps_h", "aggregate_scs"):
        if not _is_json_safe_metric(payload.get(fld)):
            raise ValueError(f"{fld} not finite-or-sentinel: {payload.get(fld)!r}")
    if payload["verdict"] not in ("PASS", "FAIL"):
        raise ValueError(f"verdict must be PASS/FAIL; got {payload['verdict']!r}")
    return payload


def compact_validation_fields(observation: ValidationGateObservation, run_dir) -> dict:
    """The flat ``validation.jsonl`` gate_* fields, only if the sidecar is durable.

    Recomputes the expected relative path, re-reads the file under ``run_dir``,
    runs ``validate_sidecar_payload`` on it, and only then returns the pointer
    fields — all metric values json-safe so ``_append_validation_record``'s
    ``allow_nan=False`` cannot raise. A missing, truncated, or schema-invalid
    sidecar raises ``ValidationGateUnavailable``: a JSONL record can never
    advertise a sidecar that was not durably published (D-17). The failed-status
    record shape is produced by the 46-07 hook wrapper, not here.
    """
    rel = sidecar_relative_path(observation.global_step)
    sidecar_path = Path(run_dir) / rel
    if not sidecar_path.is_file():
        raise ValidationGateUnavailable(f"sidecar not published under run_dir: {rel}")
    try:
        payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationGateUnavailable(f"sidecar unreadable: {rel}: {exc}") from exc
    try:
        validate_sidecar_payload(payload)
    except ValueError as exc:
        raise ValidationGateUnavailable(f"sidecar schema-invalid: {rel}: {exc}") from exc
    return {
        "gate_schema_version": payload["schema_version"],
        "gate_eps_h": json_safe_float(observation.aggregate_eps_h),
        "gate_scs": json_safe_float(observation.aggregate_scs),
        "gate_verdict": observation.verdict,
        "gate_status": "ok",
        "gate_n_trajectories": int(observation.n_trajectories),
        "gate_n_nonfinite": int(observation.n_nonfinite),
        "gate_sidecar": rel,
    }
