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
import numbers
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
    "compact_validation_fields_from_payload",
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


def _strict_nonnegative_integral(value, *, what: str) -> int:
    """Require ``value`` to be a non-negative ``numbers.Integral`` (bool excluded).

    Rejects bool, float/fraction, string, and negative values BEFORE any
    filename or record conversion (WR-01): ``bool`` is a ``numbers.Integral``
    subclass in Python, so it must be excluded explicitly; a float/Fraction
    that happens to hold an integral value (``1.0``) is still not accepted --
    only genuine integer types (``int``, ``numpy`` integer scalars, etc.) via
    ``numbers.Integral``.
    """
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{what} must be a non-negative integer, not {type(value).__name__}: {value!r}")
    n = int(value)
    if n < 0:
        raise ValueError(f"{what} must be non-negative: {n}")
    return n


def sidecar_relative_path(global_step) -> str:
    """Fixed run-relative sidecar path ``validation_gate/step-<8-digit>.json``.

    The step is validated as a strict non-negative ``numbers.Integral`` (bool,
    float/fraction, string, and negative values all raise BEFORE any int
    conversion -- WR-01); the fixed pattern has no user-controlled path
    segment, so neither an absolute path nor a parent-directory escape is
    constructible. Equal integral steps produce the identical name; adjacent
    integral steps produce distinct names.
    """
    n = _strict_nonnegative_integral(global_step, what="global_step")
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

_FRAME_REQUIRED_KEYS = frozenset(
    {"position_frame", "time_coord", "mass_convention", "conf01_evidence_ref"}
)
_ROW_REQUIRED_KEYS = frozenset({"record_key", "eps_h", "scs"})
_RECORD_KEY_REQUIRED_KEYS = frozenset({"variant", "fidelity", "id"})


def _require_exact_keys(obj, required_keys, *, what: str) -> None:
    """Reject a JSON object with any missing OR unknown key (D-18/CR-04)."""
    if not isinstance(obj, dict):
        raise ValueError(f"{what} must be a JSON object; got {type(obj).__name__}")
    keys = set(obj.keys())
    if keys != required_keys:
        missing = sorted(required_keys - keys)
        extra = sorted(keys - required_keys)
        raise ValueError(
            f"{what} keys must be exactly {sorted(required_keys)}; "
            f"missing={missing} extra={extra}"
        )


def _validate_run_dir_name(value) -> None:
    """``run_dir`` must be a non-empty string naming exactly one path component."""
    if not isinstance(value, str) or not value:
        raise ValueError(f"run_dir must be a non-empty string; got {value!r}")
    parts = Path(value).parts
    if len(parts) != 1 or "/" in value or "\\" in value:
        raise ValueError(f"run_dir must be a single path component; got {value!r}")


def _validate_frame(frame_obj) -> None:
    """Exact frame keys, string values, a coherent pair, ordered_raw mass, and a
    non-empty evidence ref (D-07/D-12/D-18). Never mutates
    ``RATIFIED_VALIDATION_FRAME`` or infers a frame from measurement."""
    _require_exact_keys(frame_obj, _FRAME_REQUIRED_KEYS, what="frame")
    for key in _FRAME_REQUIRED_KEYS:
        value = frame_obj[key]
        if not isinstance(value, str):
            raise ValueError(f"frame.{key} must be a JSON string; got {type(value).__name__}")
    position_frame = frame_obj["position_frame"]
    time_coord = frame_obj["time_coord"]
    if (position_frame, time_coord) not in COHERENT_FRAME_PAIRS:
        raise ValueError(
            f"incoherent frame pair: position_frame={position_frame!r} "
            f"time_coord={time_coord!r}; accepted pairs={sorted(COHERENT_FRAME_PAIRS)}"
        )
    if frame_obj["mass_convention"] != MASS_CONVENTION_ORDERED_RAW:
        raise ValueError(
            f"mass_convention must be {MASS_CONVENTION_ORDERED_RAW!r}; "
            f"got {frame_obj['mass_convention']!r}"
        )
    if not frame_obj["conf01_evidence_ref"]:
        raise ValueError("frame.conf01_evidence_ref must be a non-empty string")


def _is_strict_nonnegative_json_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _validate_record_key_triple(record_key):
    """Exact RecordKey keys, non-empty string variant/fidelity, strict
    nonnegative int id; returns the ``(variant, fidelity, id)`` triple."""
    _require_exact_keys(record_key, _RECORD_KEY_REQUIRED_KEYS, what="record_key")
    variant = record_key["variant"]
    fidelity = record_key["fidelity"]
    rid = record_key["id"]
    if not isinstance(variant, str) or not variant:
        raise ValueError(f"record_key.variant must be a non-empty string; got {variant!r}")
    if not isinstance(fidelity, str) or not fidelity:
        raise ValueError(f"record_key.fidelity must be a non-empty string; got {fidelity!r}")
    if not _is_strict_nonnegative_json_int(rid):
        raise ValueError(f"record_key.id must be a non-negative JSON integer; got {rid!r}")
    return (variant, fidelity, rid)


def _decode_metric_value(value, *, what: str) -> float:
    """Decode a JSON-safe metric (finite number or sentinel string) to a float.

    Raises ``ValueError`` for bool, a non-finite bare number, an illegal
    string, or any other type -- the finite-or-sentinel legality every gate
    metric must satisfy -- but returns the decoded float so the caller can
    recompute against it (D-13/D-20).
    """
    if isinstance(value, bool):
        raise ValueError(f"{what} must not be a bool: {value!r}")
    if isinstance(value, (int, float)):
        v = float(value)
        if not math.isfinite(v):
            raise ValueError(f"{what} must be finite unless sentinel-encoded; got {value!r}")
        return v
    if isinstance(value, str):
        if value == _NAN_SENTINEL:
            return float("nan")
        if value == _POS_INF_SENTINEL:
            return float("inf")
        if value == _NEG_INF_SENTINEL:
            return float("-inf")
    raise ValueError(f"{what} not finite-or-sentinel: {value!r}")


def _metrics_equal(a: float, b: float) -> bool:
    """Exact equality for decoded metrics; NaN classes compare equal to NaN
    classes only (never to each other's finite/inf counterpart)."""
    if math.isnan(a) and math.isnan(b):
        return True
    if math.isnan(a) or math.isnan(b):
        return False
    return a == b


def _validate_canonical_threshold(payload, field: str, expected) -> None:
    value = payload[field]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a JSON number; got {type(value).__name__}")
    if float(value) != float(expected):
        raise ValueError(f"{field} must equal the canonical threshold {expected!r}; got {value!r}")


def validate_sidecar_payload(
    payload,
    *,
    expected_run_dir_name=None,
    expected_global_step=None,
    expected_sidecar_path=None,
) -> dict:
    """Fail-closed structural AND semantic validation of a parsed sidecar payload.

    Raises ``ValueError`` with a reason on any violation; returns the payload
    (unmodified) on success. A schema- or semantics-invalid payload is NOT a
    durable validation-gate record (D-20) — this checker is what the D-19
    summary projection and the EVAL-01 precondition (iii) eligibility
    semantics stand on (D-17/D-18/D-19/D-20).

    Every v1 key set (top-level, ``frame``, each row, each ``record_key``) is
    exact — unknown keys fail closed the same as missing ones. ``split``,
    ``gate_status``, and the frame keys/pair/mass-convention are exact
    strings; ``global_step``/``stage``/counts/ids are strict non-negative
    JSON integers with ``bool`` excluded (WR-01); every per-row and aggregate
    metric is independently RECOMPUTED through ``gate_metrics`` and compared
    exactly to the persisted value (D-13) — a payload can never advertise a
    metric, count, or verdict that disagrees with its own rows.

    ``expected_run_dir_name``/``expected_global_step``/``expected_sidecar_path``
    are optional keyword-only CONTEXTUAL bindings a caller may supply (e.g. a
    JSONL record's own claimed identity): when supplied, the payload's
    ``run_dir``/``global_step``/``sidecar_path`` must match exactly, closing
    the cross-run, wrong-step, and forged-pointer paths (CR-03).
    """
    _require_exact_keys(payload, _REQUIRED_TOP_KEYS, what="payload")

    if payload["schema_version"] != GATE_SIDECAR_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version mismatch: {payload['schema_version']!r} "
            f"(expected {GATE_SIDECAR_SCHEMA_VERSION!r})"
        )
    if payload["split"] != "validation":
        raise ValueError(f"split must be 'validation'; got {payload['split']!r}")
    if payload["gate_status"] != "ok":
        raise ValueError(f"gate_status must be 'ok'; got {payload['gate_status']!r}")

    _validate_run_dir_name(payload["run_dir"])

    global_step = _strict_nonnegative_integral(payload["global_step"], what="global_step")
    _strict_nonnegative_integral(payload["stage"], what="stage")

    expected_rel = sidecar_relative_path(global_step)
    if payload["sidecar_path"] != expected_rel:
        raise ValueError(
            f"sidecar_path {payload['sidecar_path']!r} does not match the path "
            f"derived from global_step={global_step}: {expected_rel!r}"
        )

    _validate_frame(payload["frame"])

    n_trajectories = _strict_nonnegative_integral(payload["n_trajectories"], what="n_trajectories")
    if n_trajectories <= 0:
        raise ValueError("n_trajectories must be positive")
    n_nonfinite = _strict_nonnegative_integral(payload["n_nonfinite"], what="n_nonfinite")
    if n_nonfinite > n_trajectories:
        raise ValueError(
            f"n_nonfinite ({n_nonfinite}) must not exceed n_trajectories ({n_trajectories})"
        )

    _validate_canonical_threshold(
        payload, "eps_h_reject_threshold", gate_metrics.GATE_EPS_H_REJECT_THRESHOLD
    )
    _validate_canonical_threshold(
        payload, "scs_reject_threshold", gate_metrics.GATE_SCS_REJECT_THRESHOLD
    )

    rows = payload["rows"]
    if not isinstance(rows, list):
        raise ValueError(f"rows must be a list; got {type(rows).__name__}")
    if len(rows) != n_trajectories:
        raise ValueError(f"row count {len(rows)} != n_trajectories {n_trajectories}")

    triples = []
    decoded_row_eps_h = []
    for row in rows:
        _require_exact_keys(row, _ROW_REQUIRED_KEYS, what="row")
        triples.append(_validate_record_key_triple(row["record_key"]))
        eps_h = _decode_metric_value(row["eps_h"], what="row eps_h")
        scs = _decode_metric_value(row["scs"], what="row scs")
        expected_scs = gate_metrics.scs_from_eps_h(eps_h)
        if not _metrics_equal(scs, expected_scs):
            raise ValueError(
                f"row scs {row['scs']!r} does not match scs_from_eps_h(eps_h) "
                f"for record_key {triples[-1]!r}"
            )
        decoded_row_eps_h.append(eps_h)

    for i in range(len(triples) - 1):
        if not (triples[i] < triples[i + 1]):
            raise ValueError(
                "rows must be uniquely and strictly increasing by record_key "
                f"triple (variant, fidelity, id); got {triples[i]!r} then {triples[i + 1]!r}"
            )

    derived_n_nonfinite = sum(1 for v in decoded_row_eps_h if not math.isfinite(v))
    if derived_n_nonfinite != n_nonfinite:
        raise ValueError(
            f"n_nonfinite {n_nonfinite} does not match the {derived_n_nonfinite} "
            "row(s) with non-finite eps_h"
        )

    aggregate = gate_metrics.aggregate_gate_verdict(decoded_row_eps_h)
    aggregate_eps_h = _decode_metric_value(payload["aggregate_eps_h"], what="aggregate_eps_h")
    aggregate_scs = _decode_metric_value(payload["aggregate_scs"], what="aggregate_scs")
    if not _metrics_equal(aggregate_eps_h, aggregate.eps_h):
        raise ValueError(
            f"aggregate_eps_h {payload['aggregate_eps_h']!r} does not match the "
            "recomputed aggregate"
        )
    if not _metrics_equal(aggregate_scs, aggregate.scs):
        raise ValueError(
            f"aggregate_scs {payload['aggregate_scs']!r} does not match the "
            "recomputed aggregate"
        )
    if payload["verdict"] not in ("PASS", "FAIL"):
        raise ValueError(f"verdict must be PASS/FAIL; got {payload['verdict']!r}")
    if payload["verdict"] != aggregate.verdict:
        raise ValueError(
            f"verdict {payload['verdict']!r} does not match the recomputed "
            f"verdict {aggregate.verdict!r}"
        )

    if expected_run_dir_name is not None and payload["run_dir"] != expected_run_dir_name:
        raise ValueError(
            f"run_dir {payload['run_dir']!r} does not match expected run "
            f"{expected_run_dir_name!r}"
        )
    if expected_global_step is not None:
        expected_step = _strict_nonnegative_integral(
            expected_global_step, what="expected_global_step"
        )
        if global_step != expected_step:
            raise ValueError(
                f"global_step {global_step} does not match expected step {expected_step}"
            )
    if expected_sidecar_path is not None and payload["sidecar_path"] != expected_sidecar_path:
        raise ValueError(
            f"sidecar_path {payload['sidecar_path']!r} does not match expected "
            f"path {expected_sidecar_path!r}"
        )

    return payload


def compact_validation_fields_from_payload(
    payload,
    *,
    expected_run_dir_name,
    expected_global_step,
    expected_sidecar_path,
) -> dict:
    """The eight ``validation.jsonl`` gate_* fields, derived ONLY from a fully
    validated persisted payload (D-17/D-19/CR-03).

    Runs the complete ``validate_sidecar_payload`` contract (structural,
    semantic, AND the three identity bindings) and, only on success, projects
    the eight compact fields exclusively from the validated payload -- never
    from a caller-supplied in-memory observation, so a record can never
    advertise metrics or counts that differ from its pointed artifact.
    """
    validated = validate_sidecar_payload(
        payload,
        expected_run_dir_name=expected_run_dir_name,
        expected_global_step=expected_global_step,
        expected_sidecar_path=expected_sidecar_path,
    )
    return {
        "gate_schema_version": validated["schema_version"],
        "gate_eps_h": validated["aggregate_eps_h"],
        "gate_scs": validated["aggregate_scs"],
        "gate_verdict": validated["verdict"],
        "gate_status": validated["gate_status"],
        "gate_n_trajectories": validated["n_trajectories"],
        "gate_n_nonfinite": validated["n_nonfinite"],
        "gate_sidecar": validated["sidecar_path"],
    }


def compact_validation_fields(observation: ValidationGateObservation, run_dir) -> dict:
    """The flat ``validation.jsonl`` gate_* fields, only if the sidecar is
    durable, contained, and fully valid (D-17/D-19/CR-03).

    Resolves the run root and the step-derived candidate sidecar path, proves
    containment (``candidate.relative_to(run_root)``), loads the durable
    payload, and delegates to :func:`compact_validation_fields_from_payload`
    with this call's own run basename/step/relative-path as the expected
    identity -- so the returned fields are exclusively payload-derived, never
    drawn from ``observation`` even when the caller's in-memory observation
    differs from what was actually published. A missing, truncated, escaping,
    or schema/semantics-invalid sidecar raises ``ValidationGateUnavailable``:
    a JSONL record can never advertise a sidecar that was not durably
    published (D-17). The failed-status record shape is produced by the
    46-07 hook wrapper, not here.
    """
    run_root = Path(run_dir).resolve()
    rel = sidecar_relative_path(observation.global_step)
    candidate = (run_root / rel).resolve()
    try:
        candidate.relative_to(run_root)
    except ValueError as exc:
        raise ValidationGateUnavailable(f"sidecar escapes run_dir: {candidate}") from exc
    if not candidate.is_file():
        raise ValidationGateUnavailable(f"sidecar not published under run_dir: {rel}")
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationGateUnavailable(f"sidecar unreadable: {rel}: {exc}") from exc
    try:
        return compact_validation_fields_from_payload(
            payload,
            expected_run_dir_name=run_root.name,
            expected_global_step=observation.global_step,
            expected_sidecar_path=rel,
        )
    except ValueError as exc:
        raise ValidationGateUnavailable(f"sidecar schema-invalid: {rel}: {exc}") from exc


# ---------------------------------------------------------------------------
# Ratified production frame (46-07; D-07/D-08/D-09/D-12)
# ---------------------------------------------------------------------------

# Ratification source: GAP-46-06, Status RESOLVED-WITH-INSTRUCTION, owner ruling
# 2026-07-28, option B -- "ratify an operational raw/native validation frame by
# instruction". Full record:
# .planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md,
# section "## GAP-46-06".
#
# The D-09 branch was routed by Plan 46-09's single post-repair measurement,
# which returned the grounded rule-5 verdict VERDICT_NON_FRAME_DIVERGENCE
# (46-VERDICT-POSTREPAIR.md). That verdict is NOT overwritten here. The owner
# exercised the D-09 branch on the recorded evidence and named this pair
# explicitly, so the values below are quoted from the resolution note rather
# than inferred from any measurement (D-12).
#
# The ratified convention is the CONF-08-repaired residency: canonically
# ordered, COM-recentred and boost-corrected, raw dimensional scale, unrotated,
# paired with masses_ordered.
#
# Re-ratification is REQUIRED if Phase 47/48 moves residency to the locked
# canonical scaled contract (r' with u = t/T); this constant then goes stale.
RATIFIED_VALIDATION_FRAME = FrameConvention(
    position_frame=POSITION_FRAME_RAW,
    time_coord=TIME_COORD_RAW,
    mass_convention=MASS_CONVENTION_ORDERED_RAW,
    conf01_evidence_ref=(
        ".planning/phases/46-frame-resolution-gate-aligned-validation/"
        "evidence/target-frame/20260728T014532Z/raw.json"
    ),
)
