"""Atomic, schema-validated preflight evidence for conformance gates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from pinn.training.atomic_io import atomic_write_text

from .table import assert_phys05_table

__all__ = [
    "PREFLIGHT_FILENAME",
    "PREFLIGHT_SCHEMA_VERSION",
    "PreflightRecorder",
    "load_preflight",
    "run_start_preflight",
]

PREFLIGHT_FILENAME = "preflight.json"
PREFLIGHT_SCHEMA_VERSION = 1
_PAYLOAD_KEYS = frozenset({"schema_version", "preflight_status", "assertions"})
_EVENT_KEYS = frozenset({"event", "stage", "status", "checks"})
_CHECK_KEYS = frozenset({"name", "tier", "expected", "actual", "passed"})
_EVENT_NAMES = frozenset({"run_start", "stage_boundary"})
_EVENT_STATUSES = frozenset({"passed", "failed"})


def _reject_gate_keys(value: Any, *, path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if isinstance(key, str) and key.startswith("gate_"):
                raise ValueError(
                    f"preflight payload key {path}.{key} uses the reserved "
                    "Phase-46 gate_* prefix"
                )
            _reject_gate_keys(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_gate_keys(child, path=f"{path}[{index}]")


def _validate_payload(payload: Any) -> dict[str, Any]:
    _reject_gate_keys(payload)
    if not isinstance(payload, dict):
        raise ValueError("preflight payload must be a JSON object")
    if set(payload) != set(_PAYLOAD_KEYS):
        raise ValueError(
            "preflight payload keys must be exactly "
            f"{sorted(_PAYLOAD_KEYS)}; got {sorted(payload)}"
        )
    if payload["schema_version"] != PREFLIGHT_SCHEMA_VERSION:
        raise ValueError(
            f"preflight schema_version must be {PREFLIGHT_SCHEMA_VERSION}; "
            f"got {payload['schema_version']!r}"
        )
    if payload["preflight_status"] not in _EVENT_STATUSES:
        raise ValueError(
            "preflight_status must be 'passed' or 'failed'; "
            f"got {payload['preflight_status']!r}"
        )
    assertions = payload["assertions"]
    if not isinstance(assertions, list):
        raise ValueError("preflight assertions must be a JSON array")
    for index, event in enumerate(assertions):
        if not isinstance(event, dict):
            raise ValueError(f"preflight assertion {index} must be a JSON object")
        if set(event) != set(_EVENT_KEYS):
            raise ValueError(
                f"preflight assertion {index} keys must be exactly "
                f"{sorted(_EVENT_KEYS)}; got {sorted(event)}"
            )
        if event["event"] not in _EVENT_NAMES:
            raise ValueError(
                f"preflight assertion {index} has unknown event "
                f"{event['event']!r}"
            )
        stage = event["stage"]
        if not isinstance(stage, int) or isinstance(stage, bool) or stage < 0:
            raise ValueError(
                f"preflight assertion {index} stage must be a non-negative int"
            )
        if event["status"] not in _EVENT_STATUSES:
            raise ValueError(
                f"preflight assertion {index} status must be 'passed' or 'failed'"
            )
        checks = event["checks"]
        if not isinstance(checks, list):
            raise ValueError(f"preflight assertion {index} checks must be a JSON array")
        for check_index, check in enumerate(checks):
            if not isinstance(check, dict):
                raise ValueError(
                    f"preflight assertion {index} check {check_index} must be an object"
                )
            if set(check) != set(_CHECK_KEYS):
                raise ValueError(
                    f"preflight assertion {index} check {check_index} keys must be "
                    f"exactly {sorted(_CHECK_KEYS)}; got {sorted(check)}"
                )
            if check["tier"] not in {"locked", "advisory"}:
                raise ValueError(
                    f"preflight assertion {index} check {check_index} has an "
                    f"unknown tier {check['tier']!r}"
                )
            if not isinstance(check["passed"], bool):
                raise ValueError(
                    f"preflight assertion {index} check {check_index} passed "
                    "must be boolean"
                )
    return payload


class PreflightRecorder:
    """Append-only assertion events persisted after every event."""

    def __init__(self, run_dir: str | Path):
        self.run_dir = Path(run_dir)
        self._events: list[dict[str, Any]] = []

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._events)

    def _write(self) -> None:
        payload = {
            "schema_version": PREFLIGHT_SCHEMA_VERSION,
            "preflight_status": (
                "failed"
                if any(event["status"] == "failed" for event in self._events)
                else "passed"
            ),
            "assertions": self._events,
        }
        atomic_write_text(
            self.run_dir / PREFLIGHT_FILENAME,
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
        )

    def append_event(
        self,
        *,
        event: str,
        stage: int,
        status: str,
        checks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        record = {
            "event": event,
            "stage": stage,
            "status": status,
            "checks": checks,
        }
        _validate_payload(
            {
                "schema_version": PREFLIGHT_SCHEMA_VERSION,
                "preflight_status": status,
                "assertions": [record],
            }
        )
        self._events.append(record)
        self._write()
        return record

    # Short aliases keep the recorder convenient for later phase composition
    # without introducing a second event-writing path.
    append = append_event
    record_event = append_event


def load_preflight(run_dir: str | Path) -> dict[str, Any]:
    """Load and fail-closed validate ``run_dir/preflight.json``."""
    path = Path(run_dir) / PREFLIGHT_FILENAME
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"preflight artifact not found: {path}") from exc
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"preflight artifact is not valid JSON: {exc}") from exc
    return _validate_payload(payload)


def _failure_check(exc: ValueError) -> dict[str, Any]:
    return {
        "name": "phys05_table",
        "tier": "locked",
        "expected": "conformant PHYS-05 row",
        "actual": str(exc),
        "passed": False,
    }


def run_start_preflight(config: Any, scheduled_weights: Any, run_dir: str | Path) -> PreflightRecorder:
    """Run the D-05 site-1 table assertion and return its event recorder."""
    del config  # The composition seam intentionally receives the resolved config.
    recorder = PreflightRecorder(run_dir)
    try:
        result = assert_phys05_table(scheduled_weights, stage=0)
    except ValueError as exc:
        recorder.append_event(
            event="run_start",
            stage=0,
            status="failed",
            checks=[_failure_check(exc)],
        )
        raise
    recorder.append_event(
        event="run_start",
        stage=0,
        status="passed",
        checks=result["checks"],
    )
    return recorder
