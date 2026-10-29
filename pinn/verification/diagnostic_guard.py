"""Phase 65 (INST-08): intrinsic diagnostic-artifact identity and typed refusal.

Every INST-08 artifact — the JSON record and the tensor payload — carries its
diagnostic identity inside the payload itself (``artifact_kind: diagnostic``,
``diagnostic: true``, ``counted: false`` beside the ``inst08-*`` schema), never
in its filename or directory. ``require_not_diagnostic`` reads a file's content
and raises :class:`DiagnosticArtifactRefused` when that intrinsic marker is
present, so a renamed or relocated diagnostic artifact cannot cross into a
production reader even when production-looking keys are added around the
marker. Plan 65-03 wires this refusal into the production graded-run and
evaluator entry points; this module is the single typed refusal they share.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import torch

__all__ = [
    "DiagnosticArtifactRefused",
    "RECORD_SCHEMA",
    "WEIGHTS_SCHEMA",
    "ARTIFACT_KIND",
    "diagnostic_marker",
    "carries_diagnostic_marker",
    "require_not_diagnostic",
    "require_resume_not_diagnostic",
    "read_diagnostic_record",
    "read_diagnostic_weights",
]

RECORD_SCHEMA = "inst08-diagnostic/v1"
WEIGHTS_SCHEMA = "inst08-diagnostic-weights/v1"
ARTIFACT_KIND = "diagnostic"


class DiagnosticArtifactRefused(RuntimeError):
    """The file is an INST-08 diagnostic artifact and may not enter production.

    Exported as the one typed refusal the production entry points (Plan 65-03)
    raise before any graded-run or evaluator side effect.
    """


def diagnostic_marker(*, schema):
    """The intrinsic identity block every diagnostic payload carries.

    The payload's own schema names which artifact kind it is; the marker fields
    are checked by content, independent of filename or directory.
    """
    if schema not in (RECORD_SCHEMA, WEIGHTS_SCHEMA):
        raise ValueError(f"unknown diagnostic artifact schema: {schema!r}")
    return {
        "schema": schema,
        "artifact_kind": ARTIFACT_KIND,
        "diagnostic": True,
        "counted": False,
    }


def _carries_marker(payload) -> bool:
    if not isinstance(payload, Mapping):
        return False
    if payload.get("diagnostic") is True or payload.get("artifact_kind") == ARTIFACT_KIND:
        return True
    return any(
        _carries_marker(value) for value in payload.values() if isinstance(value, Mapping)
    )


def carries_diagnostic_marker(payload) -> bool:
    """Public predicate over an ALREADY-LOADED payload (no file I/O).

    The production checkpoint store's load routes and structural validator
    (Plan 65-03) call this on every payload they are about to return or accept,
    so the marker check has exactly one implementation.
    """
    return _carries_marker(payload)


def require_not_diagnostic(path):
    """Refuse the file when its content carries the intrinsic diagnostic marker.

    Returns ``None`` when the file is not a diagnostic artifact (for example a
    production state dict or a production checkpoint envelope). The check is
    content-based: a renamed or relocated artifact, or an envelope with all
    production-required keys added around the marker, is still refused.
    """
    raw = Path(path).read_bytes()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        payload = None
    if payload is not None:
        if _carries_marker(payload):
            raise DiagnosticArtifactRefused(
                f"{Path(path).name} carries the intrinsic diagnostic marker and may not "
                "enter a production reader"
            )
        return None
    loaded = torch.load(path, map_location="cpu", weights_only=True)
    if _carries_marker(loaded):
        raise DiagnosticArtifactRefused(
            f"{Path(path).name} carries the intrinsic diagnostic marker and may not "
            "enter a production reader"
        )
    return None


def require_resume_not_diagnostic(resume_arg, checkpoints_dir):
    """Early (pre-run) graded-resume admission — read-only content check.

    Plan 65-03 (D-09 / INST-08 d): ``train.main`` calls this BEFORE creating
    the run directory, so a diagnostic resume candidate can never reach run
    creation, data/model/optimizer setup or the graded training loop. The
    routing mirrors ``pinn.training.resume.load_resume_target`` exactly:

    * an explicit FILE argument is checked by content (``require_not_diagnostic``);
    * the literal ``latest``, a directory, or any other non-file argument is
      resolved against the run's OWN checkpoints directory exactly as
      ``store.load_latest()`` would (``latest.pt`` first, then the step/stage
      candidate ordering — never selection by scientific metric), and the
      payload that WOULD be selected is refused when it carries the marker. A
      marked newest candidate refuses instead of silently falling through to an
      older ordinary file.

    The check never constructs a checkpoint store (whose constructor creates
    its directory): an absent checkpoints directory stays absent, and a
    selection failure with no diagnostic content (no candidates, none
    structurally valid) is left to the real load route to report.
    """
    from pinn.training.checkpoint import (  # deferred: checkpoint imports this module
        DiagnosticCheckpointRefused,
        EmptyCheckpointStore,
        NoValidCheckpointError,
        peek_latest_selection,
    )

    arg = str(resume_arg)
    if arg != "latest":
        path = Path(arg)
        if path.is_file():
            require_not_diagnostic(path)
            return
        # A directory (or any non-file argument) routes to store.load_latest().
    try:
        peek_latest_selection(Path(checkpoints_dir))
    except DiagnosticCheckpointRefused as exc:
        raise DiagnosticArtifactRefused(f"--resume {arg}: {exc}") from exc
    except (NoValidCheckpointError, EmptyCheckpointStore):
        return  # not a diagnostic question; the load route reports it


def read_diagnostic_record(path):
    """Read and verify one diagnostic JSON record. Refuse anything else."""
    payload = json.loads(Path(path).read_bytes().decode("utf-8"))
    if not isinstance(payload, Mapping) or payload.get("schema") != RECORD_SCHEMA \
            or payload.get("diagnostic") is not True:
        raise DiagnosticArtifactRefused(
            f"{Path(path).name} is not a {RECORD_SCHEMA} diagnostic record"
        )
    return payload


def read_diagnostic_weights(path):
    """Read and verify one diagnostic tensor payload. Refuse anything else.

    The payload is saved so ``torch.load(..., weights_only=True)`` reads it;
    the returned mapping carries the intrinsic marker beside the ``state_dict``.
    """
    payload = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(payload, Mapping) or payload.get("schema") != WEIGHTS_SCHEMA \
            or payload.get("diagnostic") is not True \
            or not isinstance(payload.get("state_dict"), Mapping):
        raise DiagnosticArtifactRefused(
            f"{Path(path).name} is not a {WEIGHTS_SCHEMA} diagnostic weights payload"
        )
    return payload
