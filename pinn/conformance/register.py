"""INST-03 known-divergence register.

The committed JSON register is a derived, machine-readable record.  It is
validated every time it crosses the register-to-preflight boundary so a
hand-edited or stale artifact cannot silently become run evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from pinn.training.atomic_io import atomic_write_text

__all__ = [
    "DIVERGENCE_REGISTER_FILENAME",
    "REGISTER_SCHEMA_VERSION",
    "load_divergence_register",
    "write_divergence_register",
]

DIVERGENCE_REGISTER_FILENAME = "divergence_register.json"
REGISTER_SCHEMA_VERSION = 1

_REGISTER_KEYS = frozenset({"schema_version", "entries"})
_ENTRY_KEYS = frozenset(
    {
        "id",
        "kind",
        "status",
        "title",
        "spec_citation",
        "authority",
        "rationale",
        "what_it_would_take",
        "proof_test",
        "waiver",
    }
)
_KINDS = frozenset({"divergence", "qualification", "deferred-scope"})
_STATUSES = frozenset({"open", "closed", "waived"})
_REGISTER_PATH = Path(__file__).with_name(DIVERGENCE_REGISTER_FILENAME)


def _nonempty_text(value: Any, *, field: str, entry_id: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"register entry {entry_id!r} {field} must be a non-empty string"
        )
    return value


def _validate_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("divergence register payload must be a JSON object")
    if set(payload) != set(_REGISTER_KEYS):
        raise ValueError(
            "divergence register keys must be exactly "
            f"{sorted(_REGISTER_KEYS)}; got {sorted(payload)}"
        )
    version = payload["schema_version"]
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError(
            f"divergence register schema_version must be {REGISTER_SCHEMA_VERSION}; "
            f"got {version!r}"
        )
    if version != REGISTER_SCHEMA_VERSION:
        raise ValueError(
            f"divergence register schema_version must be {REGISTER_SCHEMA_VERSION}; "
            f"got {version!r}"
        )

    entries = payload["entries"]
    if not isinstance(entries, list):
        raise ValueError("divergence register entries must be a JSON array")

    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"register entry {index} must be a JSON object")
        if set(entry) != set(_ENTRY_KEYS):
            raise ValueError(
                f"register entry {index} keys must be exactly "
                f"{sorted(_ENTRY_KEYS)}; got {sorted(entry)}"
            )
        entry_id = _nonempty_text(entry["id"], field="id", entry_id=f"#{index}")
        if entry_id in seen:
            raise ValueError(f"duplicate id in divergence register: {entry_id}")
        seen.add(entry_id)

        kind = entry["kind"]
        if kind not in _KINDS:
            raise ValueError(
                f"register entry {entry_id!r} has unknown kind {kind!r}; "
                f"expected one of {sorted(_KINDS)}"
            )
        status = entry["status"]
        if status not in _STATUSES:
            raise ValueError(
                f"register entry {entry_id!r} has unknown status {status!r}; "
                f"expected one of {sorted(_STATUSES)}"
            )
        for field in (
            "title",
            "spec_citation",
            "authority",
            "rationale",
            "what_it_would_take",
        ):
            _nonempty_text(entry[field], field=field, entry_id=entry_id)

        proof_test = entry["proof_test"]
        if proof_test is not None and (
            not isinstance(proof_test, str) or not proof_test.strip()
        ):
            raise ValueError(
                f"register entry {entry_id!r} proof_test must be null or a "
                "non-empty string"
            )
        if status == "closed" and not isinstance(proof_test, str):
            raise ValueError(
                f"closed register entry {entry_id!r} requires a non-empty proof_test"
            )

        waiver = entry["waiver"]
        if waiver is not None and (
            not isinstance(waiver, str) or not waiver.strip()
        ):
            raise ValueError(
                f"register entry {entry_id!r} waiver must be null or a "
                "non-empty citation"
            )
        if status == "waived" and not isinstance(waiver, str):
            raise ValueError(
                f"waived register entry {entry_id!r} requires a non-empty waiver "
                "citation to already-granted authority"
            )

        validated.append(dict(entry))
    return {"schema_version": REGISTER_SCHEMA_VERSION, "entries": validated}


def _path_for(value: str | Path | None) -> Path:
    if value is None:
        return _REGISTER_PATH
    path = Path(value)
    return path / DIVERGENCE_REGISTER_FILENAME if path.is_dir() else path


def load_divergence_register(path: str | Path | None = None) -> dict[str, Any]:
    """Load and fail-closed validate the committed divergence register."""

    target = _path_for(path)
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"divergence register not found: {target}") from exc
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"divergence register is not valid JSON: {exc}") from exc
    return _validate_payload(payload)


def write_divergence_register(
    path: str | Path | None = None, payload: Mapping[str, Any] | None = None
) -> Path:
    """Validate and atomically write a deterministic register artifact."""

    target = _path_for(path)
    if payload is None:
        payload = load_divergence_register()
    checked = _validate_payload(dict(payload))
    text = json.dumps(checked, sort_keys=True, indent=2) + "\n"
    return atomic_write_text(target, text)
