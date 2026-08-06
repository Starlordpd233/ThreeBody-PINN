"""Atomic, schema-validated preflight evidence for conformance gates."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

import torch

from pinn.loss_catalog import resolve_causal_clip_facts
from pinn.training.run_metadata import load_training_metadata
from pinn.training.atomic_io import atomic_write_text

from .census import run_census
from .register import load_divergence_register
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
_EVENT_KEYS = frozenset(
    {
        "event",
        "stage",
        "status",
        "checks",
        "census",
        "open_divergences",
        "findings",
    }
)
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


def _reject_json_constant(name: str) -> Any:
    """Refuse the non-standard JSON constants ``json.loads`` accepts by default."""
    raise ValueError(
        f"preflight artifact contains the non-finite JSON constant {name}"
    )


def _reject_non_finite(value: Any, *, path: str = "payload") -> None:
    """Refuse NaN/Infinity anywhere in the payload, at any depth (CR-11).

    This payload flows into the terminal summary, whose writer serializes with
    ``allow_nan=False``. One non-finite leaf — in a check field or nested
    evidence — would therefore convert a refused run's honest terminal summary
    into an unhandled ``ValueError`` at write time, which is precisely the
    death mode the artifact exists to survive. Refusing at load keeps the
    failure where it can still be reported.

    ``bool`` is short-circuited first because it is an ``int`` subclass.
    """
    if isinstance(value, bool):
        return
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(
            f"preflight payload value at {path} is not finite ({value!r})"
        )
    if isinstance(value, Mapping):
        for key, child in value.items():
            _reject_non_finite(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_non_finite(child, path=f"{path}[{index}]")


def _assert_status_consistency(payload: Mapping[str, Any]) -> None:
    """Refuse an artifact whose declared status contradicts its own evidence.

    Shape validation alone accepts ``preflight_status: "passed"`` sitting on
    top of a failed event, or on top of an event carrying a failed LOCKED
    check, so a hand-edited artifact could report EVAL-01 eligibility it never
    earned. Semantics are therefore revalidated, not just shape.

    The advisory tier is deliberately exempt: ``assert_phys05_table`` records
    an advisory mismatch WITHOUT raising, so a failed advisory check is
    evidence the run legitimately carries, not a contradiction. Treating it as
    one would refuse honest artifacts.
    """
    status = payload["preflight_status"]
    for index, event in enumerate(payload["assertions"]):
        failed_locked = sorted(
            str(check["name"])
            for check in event["checks"]
            if check["tier"] == "locked" and not check["passed"]
        )
        if event["status"] == "passed" and failed_locked:
            raise ValueError(
                f"preflight assertion {index} declares status 'passed' but "
                f"carries failed locked check(s): {failed_locked}"
            )
        if status == "passed" and event["status"] != "passed":
            raise ValueError(
                "preflight_status is 'passed' but assertion "
                f"{index} has status {event['status']!r}"
            )


def _validate_payload(payload: Any) -> dict[str, Any]:
    _reject_gate_keys(payload)
    _reject_non_finite(payload)
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
        census = event["census"]
        if census is not None and not isinstance(census, dict):
            raise ValueError(
                f"preflight assertion {index} census must be an object or null"
            )
        open_divergences = event["open_divergences"]
        if not isinstance(open_divergences, list) or any(
            not isinstance(entry, dict) for entry in open_divergences
        ):
            raise ValueError(
                f"preflight assertion {index} open_divergences must be an object array"
            )
        findings = event["findings"]
        if not isinstance(findings, list) or any(
            not isinstance(finding, dict) for finding in findings
        ):
            raise ValueError(
                f"preflight assertion {index} findings must be an object array"
            )
    _assert_status_consistency(payload)
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
        _validate_payload(payload)
        atomic_write_text(
            self.run_dir / PREFLIGHT_FILENAME,
            # allow_nan=False is the second belt behind _reject_non_finite:
            # this codebase must not be able to CREATE evidence the summary
            # writer cannot serialize.
            json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n",
        )

    def append_event(
        self,
        *,
        event: str,
        stage: int,
        status: str,
        checks: list[dict[str, Any]],
        census: dict[str, Any] | None = None,
        open_divergences: list[dict[str, Any]] | None = None,
        findings: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        record = {
            "event": event,
            "stage": stage,
            "status": status,
            "checks": checks,
            "census": census,
            "open_divergences": list(open_divergences or []),
            "findings": list(findings or []),
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
        # parse_constant fires on the NaN / Infinity / -Infinity tokens that
        # json.loads accepts by default; the hook refuses them before any
        # non-finite value can enter the payload (CR-11).
        payload = json.loads(text, parse_constant=_reject_json_constant)
    except json.JSONDecodeError as exc:
        raise ValueError(f"preflight artifact is not valid JSON: {exc}") from exc
    return _validate_payload(payload)


def _failure_check(
    exc: ValueError, *, name: str = "phys05_table", tier: str = "locked"
) -> dict[str, Any]:
    return {
        "name": name,
        "tier": tier,
        "expected": "conformant setup inputs",
        "actual": str(exc),
        "passed": False,
    }


def _metadata_for_census(config: Any, run_dir: str | Path) -> dict[str, Any]:
    """Load metadata with the live precision/backend expectations."""

    path = Path(run_dir) / "training_metadata.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"training metadata not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"training metadata is not valid JSON: {exc}") from exc
    precision_name = raw.get("causal_clip_precision", "float64")
    dtype = torch.float32 if precision_name == "float32" else torch.float64
    run = getattr(config, "run", None)
    device_name = getattr(run, "device", "cpu")
    if getattr(run, "strict_cpu_determinism", False):
        device_name = "cpu"
    try:
        device = torch.device(device_name)
    except (TypeError, RuntimeError):
        device = torch.device("cpu")
    try:
        facts = resolve_causal_clip_facts(dtype, device)
    except RuntimeError:
        # A configured accelerator may be absent in a verification-only host.
        # Retry on CPU without probing backend state or changing the requested
        # runtime device in the config itself.
        if device.type == "cpu":
            raise
        facts = resolve_causal_clip_facts(dtype, torch.device("cpu"))
    factor = float(getattr(getattr(config, "stage", None), "energy_floor_factor"))
    return load_training_metadata(
        run_dir,
        expected_energy_floor_factor=factor,
        expected_causal_clip_facts=facts,
    )


def _consistency_finding(config: Any, open_entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    target = next((entry for entry in open_entries if entry.get("id") == "INV-B-N-UNSET"), None)
    closed = False
    try:
        register_payload = load_divergence_register()
        target = next(
            (entry for entry in register_payload["entries"] if entry.get("id") == "INV-B-N-UNSET"),
            target,
        )
        closed = bool(target and target.get("status") == "closed")
    except ValueError:
        pass
    n_value = getattr(
        getattr(config, "invariants", None), "front_advance_window_n", None
    )
    if (n_value is not None and target is not None and target.get("status") == "open") or (
        n_value is None and closed
    ):
        return {
            "kind": "consistency",
            "quantity": "front_advance_window_n",
            "register_id": "INV-B-N-UNSET",
            "config_value": n_value,
            "register_status": "closed" if closed else "open",
            "detail": "config N and register status disagree; recorded without adopting either verdict",
        }
    return None


def run_start_preflight(config: Any, scheduled_weights: Any, run_dir: str | Path) -> PreflightRecorder:
    """Compose table, census, and register evidence at run start.

    A failed table/census assertion is appended and atomically written before
    the original ``ValueError`` propagates to ``train.py``.
    """
    recorder = PreflightRecorder(run_dir)
    try:
        register_payload = load_divergence_register()
    except ValueError as exc:
        recorder.append_event(
            event="run_start",
            stage=0,
            status="failed",
            checks=[_failure_check(exc, name="divergence_register")],
        )
        raise
    open_entries = [
        dict(entry) for entry in register_payload["entries"] if entry["status"] == "open"
    ]
    try:
        result = assert_phys05_table(scheduled_weights, stage=0)
    except ValueError as exc:
        recorder.append_event(
            event="run_start",
            stage=0,
            status="failed",
            checks=[_failure_check(exc)],
            open_divergences=open_entries,
        )
        raise
    try:
        metadata = _metadata_for_census(config, run_dir)
        census_report = run_census(
            config,
            scheduled_weights,
            metadata,
            getattr(config, "provisional_fields", lambda: ())(),
        )
    except ValueError as exc:
        census_report = getattr(exc, "report", None)
        checks = list(result["checks"])
        checks.append(
            {
                "name": "census",
                "tier": "locked",
                "expected": "all manifest quantities resolve",
                "actual": str(exc),
                "passed": False,
            }
        )
        recorder.append_event(
            event="run_start",
            stage=0,
            status="failed",
            checks=checks,
            census=census_report,
            open_divergences=open_entries,
            findings=(census_report or {}).get("findings", []),
        )
        raise
    findings = list(census_report.get("findings", []))
    consistency = _consistency_finding(config, open_entries)
    if consistency is not None:
        findings.append(consistency)
    checks = list(result["checks"])
    checks.append(
        {
            "name": "census",
            "tier": "locked",
            "expected": "all manifest quantities resolve",
            "actual": census_report["verdict"],
            "passed": census_report["verdict"] == "passed",
        }
    )
    recorder.append_event(
        event="run_start",
        stage=0,
        status="passed",
        checks=checks,
        census=census_report,
        open_divergences=open_entries,
        findings=findings,
    )
    return recorder
