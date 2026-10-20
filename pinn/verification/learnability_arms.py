"""Phase 60 (INST-05): arm specification, evidence paths and the exclusive record writer.

An arm is one training run of the learnability harness on one named system.
This module holds plain data, the path rules for an arm's directories, and the
one writer that creates a record file exactly once. It imports nothing heavier
than ``pinn.verification.evidence_io``, so the gate, ruling and protocol
modules can write evidence without importing the runner (no import cycle).
Plan 60-23 completes the closed arm catalog, the sequences, the exit codes and
the override refusal.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path

from pinn.data.types import RecordKey
from pinn.verification import evidence_io

__all__ = [
    "PHASE_REL",
    "EVIDENCE_REL",
    "RUNS_REL",
    "RUN_SCHEMA",
    "SEED",
    "REAL_RUNTIME",
    "CROSS_CHECK_RUNTIME",
    "LOSS_ARMS",
    "OMEGA_PROVENANCES",
    "RUN_KINDS",
    "FORMULA_NOT_APPLICABLE",
    "FIXTURE_FORMULA_NOTE",
    "TIMING_STEPS",
    "ArmSpec",
    "FirstResultExists",
    "arm_evidence_dir",
    "arm_run_dir",
    "fixture_arm",
    "write_record_exclusive",
]

PHASE_REL = Path(".planning/phases/60-single-system-learnability")
EVIDENCE_REL = PHASE_REL / "evidence"
RUNS_REL = Path("runs/phase60")
RUN_SCHEMA = "phase60-harness-run/v1"
SEED = 42
REAL_RUNTIME = ("float32", "mps")
CROSS_CHECK_RUNTIME = ("float64", "cpu")
LOSS_ARMS = ("data_only", "physics_ic", "full")
OMEGA_PROVENANCES = (
    "locked",
    "g2_sweep_override",
    "confirmation_override",
    "owner_approved",
)
RUN_KINDS = ("real", "fixture")
FORMULA_NOT_APPLICABLE = "not applicable: no hierarchical split"
FIXTURE_FORMULA_NOTE = "not applicable: fixture record"
# GAP-60-04: steps of the separate timing run before each real arm.
TIMING_STEPS = {"data_only": 500, "physics": 50}

_ARM_ID = re.compile(r"[a-z0-9-]+")


class FirstResultExists(RuntimeError):
    """A record already exists for this arm. The first completed run is the result."""


def _check_arm_id(arm_id):
    """Refuse an id that is not a plain lowercase token (no separator, no ``..``)."""
    if not isinstance(arm_id, str) or _ARM_ID.fullmatch(arm_id) is None:
        raise ValueError(
            f"arm_id must match [a-z0-9-]+ with no path separator or '..'; got {arm_id!r}"
        )
    return arm_id


@dataclass(frozen=True)
class ArmSpec:
    """One arm: which records it trains and is scored on, and under what loss and setting.

    Arms hold ``RecordKey`` values, never paths. ``grid_omega`` is ``None`` for
    every arm that is not a settings-sweep or confirmation arm.
    """

    arm_id: str
    rung: str
    path: str
    loss_arm: str
    system_id: int
    variant: str
    train_key: RecordKey
    score_key: RecordKey
    beside_key: RecordKey
    lr_stage: int
    clip_stage: int
    omega_provenance: str
    grid_omega: float | None
    counted: bool
    run_kind: str

    def __post_init__(self):
        _check_arm_id(self.arm_id)
        if self.loss_arm not in LOSS_ARMS:
            raise ValueError(f"loss_arm must be one of {LOSS_ARMS}; got {self.loss_arm!r}")
        if self.omega_provenance not in OMEGA_PROVENANCES:
            raise ValueError(
                f"omega_provenance must be one of {OMEGA_PROVENANCES}; "
                f"got {self.omega_provenance!r}"
            )
        if self.run_kind not in RUN_KINDS:
            raise ValueError(f"run_kind must be one of {RUN_KINDS}; got {self.run_kind!r}")
        for name in ("train_key", "score_key", "beside_key"):
            if not isinstance(getattr(self, name), RecordKey):
                raise TypeError(f"{name} must be a RecordKey, never a path")


def fixture_arm(
    *,
    train_key,
    score_key,
    beside_key,
    loss_arm="data_only",
    omega_provenance="locked",
    grid_omega=None,
):
    """An uncounted fixture arm. Its record is marked ``fixture`` and is never a rung result."""
    return ArmSpec(
        arm_id=f"fixture-{train_key.variant}-{train_key.fidelity}-{train_key.id}",
        rung="fixture",
        path="fixture",
        loss_arm=loss_arm,
        system_id=int(train_key.id),
        variant=train_key.variant,
        train_key=train_key,
        score_key=score_key,
        beside_key=beside_key,
        lr_stage=0,
        clip_stage=0,
        omega_provenance=omega_provenance,
        grid_omega=grid_omega,
        counted=False,
        run_kind="fixture",
    )


def arm_evidence_dir(arm_id, *, evidence_root):
    """``<evidence_root>/arms/<arm_id>``, after refusing an id that could escape it."""
    return Path(evidence_root) / "arms" / _check_arm_id(arm_id)


def arm_run_dir(arm_id, *, repo_root):
    """``<repo_root>/runs/phase60/<arm_id>`` (the ignored resume tree)."""
    return Path(repo_root) / RUNS_REL / _check_arm_id(arm_id)


def write_record_exclusive(path, payload, *, data_root=None):
    """Create ``path`` with canonical, redacted JSON, exactly once.

    The file is opened with ``O_CREAT | O_EXCL``, so a second writer, or a
    second run of the same arm, raises ``FirstResultExists`` and leaves the
    first file untouched. The file and its directory are fsynced. Returns the
    SHA-256 of the bytes written.
    """
    destination = Path(path)
    evidence_io.reject_evidence_root(destination, data_root=data_root)
    raw = evidence_io.canonical_json_bytes(payload)
    evidence_io.guard_redaction(raw, data_root=data_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        descriptor = os.open(destination, flags, 0o644)
    except FileExistsError as exc:
        raise FirstResultExists(
            f"a record already exists at {destination.name}; the first completed run "
            "is the result and a second run never replaces it"
        ) from exc
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    directory = os.open(destination.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return hashlib.sha256(raw).hexdigest()
