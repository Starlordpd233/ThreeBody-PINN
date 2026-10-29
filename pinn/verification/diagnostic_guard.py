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
    "require_not_diagnostic",
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
