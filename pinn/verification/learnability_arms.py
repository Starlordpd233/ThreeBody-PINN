"""Phase 60 (INST-05): arm specification, evidence paths, the override refusal and the exclusive record writer.

An arm is one training run of the learnability harness on one named system.
This module holds plain data, the path rules for an arm's directories, the
rule that decides whether an arm may run at a first-layer frequency other than
the locked one (INST-05(e)), and the one writer that creates a record file
exactly once. It imports nothing heavier than ``pinn.verification.evidence_io``
and two constants, so the gate, ruling and protocol modules can write evidence
without importing the runner (no import cycle).
"""

from __future__ import annotations

import hashlib
import math
import numbers
import os
import re
from dataclasses import dataclass
from pathlib import Path

from pinn.constants import SIREN_FIRST_OMEGA_0
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
    "OverrideRefused",
    "arm_evidence_dir",
    "arm_run_dir",
    "check_override",
    "fixture_arm",
    "resolve_first_omega_0",
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


class OverrideRefused(RuntimeError):
    """This arm may not run at that first-layer frequency (INST-05(e)). Nothing was built."""


def _positive_real(value, what):
    """A finite, positive real number that is not a bool; anything else is no setting at all."""
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise OverrideRefused(f"{what} must be a finite positive real number; got {value!r}")
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise OverrideRefused(f"{what} must be a finite positive real number; got {value!r}")
    return number


def _locked_value(scorecard):
    """The frozen scorecard's locked setting, checked against the architecture constant."""
    locked = float(scorecard.section("gate_g2")["locked_value"])
    if locked != float(SIREN_FIRST_OMEGA_0):
        raise OverrideRefused(
            f"the scorecard's locked first_omega_0 {locked} is not the architecture "
            f"constant {SIREN_FIRST_OMEGA_0}"
        )
    return locked


def _approved_value(ruling):
    """The setting a committed continue ruling names (D-11). No ruling, or any other answer, is none."""
    if ruling is None:
        raise OverrideRefused("owner_approved needs the committed D-11 ruling and none was supplied")
    if getattr(ruling, "answer", None) != "continue":
        raise OverrideRefused("the committed D-11 ruling does not answer continue")
    return _positive_real(
        getattr(ruling, "approved_first_omega_0", None), "the ruling's approved_first_omega_0"
    )


def resolve_first_omega_0(spec, *, scorecard, ruling=None):
    """The first-layer frequency this arm asks for, by its provenance.

    ``locked`` gives the scorecard's locked value, ``g2_sweep_override`` and
    ``confirmation_override`` give the arm's ``grid_omega``, and
    ``owner_approved`` gives the value the committed D-11 ruling names (it need
    not be on the sweep grid, GAP-60-11). ``ruling`` is duck-typed: ``answer``,
    ``approved_first_omega_0`` and ``sha256``. Whether the arm may use the value
    is ``check_override``'s decision, not this function's.
    """
    locked = _locked_value(scorecard)
    provenance = spec.omega_provenance
    if provenance == "locked":
        return locked
    if provenance == "owner_approved":
        return _approved_value(ruling)
    if spec.grid_omega is None:
        raise OverrideRefused(
            f"arm {spec.arm_id} has provenance {provenance} but names no grid_omega"
        )
    return _positive_real(spec.grid_omega, "grid_omega")


def check_override(spec, first_omega_0, *, scorecard, ruling=None):
    """Refuse a first-layer frequency this arm is not entitled to (INST-05(e)). Returns ``None``.

    Only literal values are compared; there is no range and no tolerance.

    * ``locked`` provenance passes only at the locked value, and carries no
      ``grid_omega``.
    * ``owner_approved`` passes only at the exact value the committed D-11
      ruling names, for any arm and on or off the grid (GAP-60-11); without a
      ruling that answers continue it never passes.
    * ``g2_sweep_override`` and ``confirmation_override`` pass only on a
      data-only arm, only when ``grid_omega`` equals the value, and only for one
      of the four scorecard grid values. An arm with a physics term never passes.

    Callers run this before reading any data or building any network.
    """
    locked = _locked_value(scorecard)
    value = _positive_real(first_omega_0, "first_omega_0")
    provenance = spec.omega_provenance
    if provenance == "locked":
        if spec.grid_omega is not None:
            raise OverrideRefused(
                f"arm {spec.arm_id} runs at the locked setting and so carries no grid_omega"
            )
        if value != locked:
            raise OverrideRefused(
                f"arm {spec.arm_id} has the locked provenance and may run only at {locked}; "
                f"got {value}"
            )
        return None
    if provenance == "owner_approved":
        approved = _approved_value(ruling)
        if value != approved:
            raise OverrideRefused(
                f"arm {spec.arm_id} may run only at the {approved} the committed D-11 ruling "
                f"names; got {value}"
            )
        return None
    if spec.loss_arm != "data_only":
        raise OverrideRefused(
            f"arm {spec.arm_id} has a physics term, so a {provenance} setting is refused"
        )
    grid = tuple(float(item) for item in scorecard.section("gate_g2")["grid"])
    if spec.grid_omega is None or float(spec.grid_omega) != value or value not in grid:
        raise OverrideRefused(
            f"arm {spec.arm_id} may run only at its own grid_omega, one of {grid}; got {value}"
        )
    return None


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
