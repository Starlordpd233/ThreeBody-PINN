"""Atomic, schema-validated preflight evidence for conformance gates."""

from __future__ import annotations

import copy
import ctypes
import json
import math
import os
import sys
import threading
from pathlib import Path
from typing import Any, Callable, Mapping, Optional

import torch

from pinn.loss_catalog import resolve_causal_clip_facts
from pinn.training.run_metadata import load_training_metadata
from pinn.training.atomic_io import atomic_write_text
from pinn.training.guards import _extract_invariant_window

from .census import run_census
from .register import load_divergence_register
from .table import assert_phys05_table

__all__ = [
    "PREFLIGHT_FILENAME",
    "PREFLIGHT_SCHEMA_VERSION",
    "INV_B_N_UNSET_ID",
    "INVARIANT_B_WINDOW_CHECK_NAME",
    "REQUIRED_RUN_START_CHECKS",
    "ConformancePreflightError",
    "PreflightRecorder",
    "evaluate_eval01_precondition_i",
    "load_preflight",
    "run_start_preflight",
    "run_microbatch_memory_preflight",
]

PREFLIGHT_FILENAME = "preflight.json"
PREFLIGHT_SCHEMA_VERSION = 1

# The run-local divergence id (D-20): the committed register entry records the
# owner ruling GLOBALLY (closed); conformance is per run, so a run whose own
# config omits the window carries the divergence itself in its run record.
INV_B_N_UNSET_ID = "INV-B-N-UNSET"

# The affirmative run-start check proving the run-local invariant-B window was
# actually read and bound (D-16: affirmative evidence, not absence of a
# negative).
INVARIANT_B_WINDOW_CHECK_NAME = "invariant_b_window"

# The required run-start evidence (GAP B): the five locked PHYS-05 table check
# names emitted by ``assert_phys05_table``, the census check, and the
# invariant-B window check.  Eligibility requires every name present on every
# ``run_start`` event with EVERY occurrence passed.
REQUIRED_RUN_START_CHECKS = (
    "lambda_phys_max",
    "lambda_e_max",
    "lambda_l_max",
    "warmup_length",
    "lambda_data",
    "census",
    INVARIANT_B_WINDOW_CHECK_NAME,
)
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


class ConformancePreflightError(ValueError):
    """A run-start setup/probe refusal safe for ``train.main`` to report."""


def _normalized_error(context: str, exc: Exception) -> ConformancePreflightError:
    return ConformancePreflightError(
        f"{context} failed with {type(exc).__name__}: {exc}"
    )


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


def _assert_history_ordering(payload: Mapping[str, Any]) -> None:
    """Refuse an assertion history that does not begin with ``run_start``.

    Only the ORDERING rule lives here; the required-evidence rules live in
    ``evaluate_eval01_precondition_i``.  The separation is load-bearing
    (D-27): a refused run's incomplete ``run_start`` evidence must still
    LOAD, because the artifact IS the caveat record — but a history that never
    opened with ``run_start`` is not evidence any run produced, so the
    codebase must neither CREATE nor READ one.  An empty array remains
    loadable: the predicate already denies it, and no code path can produce
    it.  Append-only resume histories (``run_start``, ``stage_boundary``, …,
    ``run_start``, …) stay legal (D-17 / CR-06).
    """
    assertions = payload["assertions"]
    if assertions and assertions[0]["event"] != "run_start":
        raise ValueError(
            "preflight assertion history must begin with a run_start event; "
            f"got {assertions[0]['event']!r}"
        )


class PreflightRecorder:
    """Append-only assertion events persisted after every event."""

    def __init__(self, run_dir: str | Path):
        self.run_dir = Path(run_dir)
        path = self.run_dir / PREFLIGHT_FILENAME
        if path.is_file():
            existing = load_preflight(self.run_dir)
            self._events = copy.deepcopy(existing["assertions"])
        else:
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
        # The same second-belt discipline the allow_nan=False writer comment
        # records: the codebase must not be able to CREATE a history its own
        # loader would reject.
        _assert_history_ordering(payload)
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
    except (OSError, UnicodeError) as exc:
        # After the FileNotFoundError clause on purpose: it is an OSError
        # subclass and its more specific message must win (WR-02).
        raise ValueError(
            f"preflight artifact could not be read: {path}: {exc}"
        ) from exc
    try:
        # parse_constant fires on the NaN / Infinity / -Infinity tokens that
        # json.loads accepts by default; the hook refuses them before any
        # non-finite value can enter the payload (CR-11).
        payload = json.loads(text, parse_constant=_reject_json_constant)
    except json.JSONDecodeError as exc:
        raise ValueError(f"preflight artifact is not valid JSON: {exc}") from exc
    validated = _validate_payload(payload)
    _assert_history_ordering(validated)
    return validated


def _failure_check(
    exc: Exception, *, name: str = "phys05_table", tier: str = "locked"
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
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"training metadata could not be read: {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"training metadata is not valid JSON: {exc}") from exc
    if not isinstance(raw, Mapping):
        raise ValueError("training metadata must be a JSON object")
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
    target = next((entry for entry in open_entries if entry.get("id") == INV_B_N_UNSET_ID), None)
    closed = False
    try:
        register_payload = load_divergence_register()
        target = next(
            (entry for entry in register_payload["entries"] if entry.get("id") == INV_B_N_UNSET_ID),
            target,
        )
        closed = bool(target and target.get("status") == "closed")
    except ValueError:
        pass
    n_value, _ = _run_local_invariant_window(config)
    if (n_value is not None and target is not None and target.get("status") == "open") or (
        n_value is None and closed
    ):
        return {
            "kind": "consistency",
            "quantity": "front_advance_window_n",
            "register_id": INV_B_N_UNSET_ID,
            "config_value": n_value,
            "register_status": "closed" if closed else "open",
            "detail": "config N and register status disagree; recorded without adopting either verdict",
        }
    return None


def _run_local_invariant_window(config: Any) -> tuple[Optional[int], Optional[str]]:
    """Resolve the run-local invariant-B window through the ONE accessor.

    Delegates to ``pinn.training.guards._extract_invariant_window`` — the
    single reader of ``run.invariants.front_advance_window_n`` — so the
    guard's view of N and preflight's view cannot diverge.  That accessor
    raises ``ValueError`` on a malformed window; preflight converts the raise
    into a non-null ``error_text`` so a malformed or duck-typed config stays
    fail-closed evidence instead of an exception escaping composition.
    """
    try:
        return _extract_invariant_window(config), None
    except ValueError as exc:
        return None, str(exc)


def _invariant_b_window_check(
    window: Optional[int], error_text: Optional[str]
) -> dict[str, Any]:
    """Build the affirmative run-local invariant-B window evidence record.

    The tier must be advisory, not locked: ``_assert_status_consistency``
    refuses a ``passed`` event carrying a failed LOCKED check, and D-20
    requires an N-unset run to remain runnable and to leave a ``passed``
    run-start record.  ``passed`` is true only when a window is bound and no
    error text was produced.
    """
    return {
        "name": INVARIANT_B_WINDOW_CHECK_NAME,
        "tier": "advisory",
        "expected": (
            "run-local run.invariants.front_advance_window_n bound to the "
            "owner-ratified positive-int window (GATE-03 D-20)"
        ),
        "actual": window if error_text is None else error_text,
        "passed": window is not None and error_text is None,
    }


def _run_local_n_unset_divergence(
    register_payload: Mapping[str, Any]
) -> dict[str, Any]:
    """Build the run-local open ``INV-B-N-UNSET`` record (D-20).

    When the canonical entry is present its ``id``, ``kind``, ``title``,
    ``spec_citation``, ``authority``, ``rationale``, and ``what_it_would_take``
    are copied verbatim so the run carries a human-readable caveat; ``status``
    is forced to ``open``, ``proof_test`` to null (the closure proof does not
    hold for a run that omits the window), and ``waiver`` to null.  When the
    canonical entry is absent the same ten-key record is constructed locally
    with literal text naming D-20 as the source — absence of the canonical
    entry never yields eligibility.
    """
    canonical = next(
        (
            entry
            for entry in register_payload.get("entries", [])
            if isinstance(entry, Mapping) and entry.get("id") == INV_B_N_UNSET_ID
        ),
        None,
    )
    if canonical is not None:
        record = dict(canonical)
        record["status"] = "open"
        record["proof_test"] = None
        record["waiver"] = None
        return record
    return {
        "id": INV_B_N_UNSET_ID,
        "kind": "divergence",
        "status": "open",
        "title": "invariant-B window N is unset",
        "spec_citation": "GATE-03 D-18..D-20; GAP-45-04",
        "authority": "D-20: N unset is a defined, fail-closed state",
        "rationale": (
            "This run's own config omits "
            "run.invariants.front_advance_window_n; D-20 records the unset "
            "window as an open run-local divergence independent of the "
            "committed register entry's global status."
        ),
        "what_it_would_take": (
            "Bind the owner-ratified window in this run's config "
            "(run.invariants.front_advance_window_n)."
        ),
        "proof_test": None,
        "waiver": None,
    }


def evaluate_eval01_precondition_i(payload: Mapping[str, Any]) -> bool:
    """Return the fail-closed EVAL-01 precondition-(i) standing.

    ``True`` requires an existing, valid, passed preflight artifact, every
    assertion event to have status ``passed``, and zero entries in
    ``open_divergences`` whose ``kind`` is ``"divergence"`` and whose ``status``
    is ``"open"``.  That kind filter *is* the EVAL-01 precondition-(i) scope:
    the policy says zero unwaived divergences, while D-23 distinguishes
    qualification (the implementation conforms and the caveat travels in the
    conformance block) from divergence.  Counting qualifications would make
    the permanent CONF-01-QUALIFICATION entry strand every run ineligible.

    The predicate must require the evidence it claims to summarize (GAP B):
    the assertion history begins with a ``run_start`` event, at least one
    ``run_start`` event exists, and EVERY ``run_start`` event carries each
    name in ``REQUIRED_RUN_START_CHECKS`` at least once with every occurrence
    ``passed`` — the affirmative ``invariant_b_window`` check included (D-16:
    affirmative evidence, not absence of a negative) — plus a ``census``
    mapping whose ``verdict`` compares exactly equal to ``"passed"``.  Anything
    unrecognized, absent, null, or non-mapping denies eligibility: fail closed
    on missing, malformed, or ambiguous evidence, never open.
    """
    assertions = payload["assertions"]
    if payload["preflight_status"] != "passed" or not assertions:
        return False
    if assertions[0]["event"] != "run_start":
        return False
    if any(event["status"] != "passed" for event in assertions):
        return False
    if any(
        entry.get("kind") == "divergence" and entry.get("status") == "open"
        for event in assertions
        for entry in event["open_divergences"]
    ):
        return False
    run_starts = [
        event for event in assertions if event["event"] == "run_start"
    ]
    if not run_starts:
        return False
    for event in run_starts:
        checks = event["checks"]
        for name in REQUIRED_RUN_START_CHECKS:
            occurrences = [
                check for check in checks if check["name"] == name
            ]
            if not occurrences or not all(
                check["passed"] for check in occurrences
            ):
                return False
        census = event["census"]
        if not isinstance(census, Mapping) or census.get("verdict") != "passed":
            return False
    return True


def run_start_preflight(
    config: Any,
    scheduled_weights: Any,
    run_dir: str | Path,
    *,
    controller: Any,
) -> PreflightRecorder:
    """Compose table, census, and register evidence at run start.

    A failed table/census assertion is appended and atomically written before
    a normalized ``ConformancePreflightError`` propagates to ``train.py``.
    """
    recorder = PreflightRecorder(run_dir)
    try:
        register_payload = load_divergence_register()
    except Exception as exc:
        recorder.append_event(
            event="run_start",
            stage=0,
            status="failed",
            checks=[_failure_check(exc, name="divergence_register")],
        )
        raise _normalized_error("divergence register setup", exc) from exc
    open_entries = [
        dict(entry) for entry in register_payload["entries"] if entry["status"] == "open"
    ]
    # D-20: the run-local window is read ONCE, here, through the single
    # accessor.  An unbound or malformed window appends the run-local open
    # INV-B-N-UNSET record immediately after the register-derived open
    # entries, so every downstream branch — table failure, census failure,
    # and success — carries the caveat.
    window, window_error = _run_local_invariant_window(config)
    if window is None:
        open_entries.append(_run_local_n_unset_divergence(register_payload))
    try:
        result = assert_phys05_table(scheduled_weights, stage=0)
    except Exception as exc:
        recorder.append_event(
            event="run_start",
            stage=0,
            status="failed",
            checks=[_failure_check(exc)],
            open_divergences=open_entries,
        )
        raise _normalized_error("PHYS-05 table assertion", exc) from exc
    try:
        metadata = _metadata_for_census(config, run_dir)
        raw_census_report = run_census(
            config,
            scheduled_weights,
            metadata,
            getattr(config, "provisional_fields", lambda: ())(),
            controller=controller,
        )
        if not isinstance(raw_census_report, Mapping):
            raise TypeError(
                "conformance census report must be a mapping; got "
                f"{type(raw_census_report).__name__}"
            )
        census_report = dict(raw_census_report)
        findings = list(census_report.get("findings", []))
        consistency = _consistency_finding(config, open_entries)
        if consistency is not None:
            findings.append(consistency)
        checks = list(result["checks"])
        # The window check goes BEFORE the census append in both branches so
        # census stays the terminal check (checks[-1]["name"] == "census").
        checks.append(_invariant_b_window_check(window, window_error))
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
    except Exception as exc:
        raw_report = getattr(exc, "report", None)
        census_report = dict(raw_report) if isinstance(raw_report, Mapping) else None
        checks = list(result["checks"])
        checks.append(_invariant_b_window_check(window, window_error))
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
        raise _normalized_error("conformance census setup", exc) from exc


class _RusageInfoV2(ctypes.Structure):
    """``struct rusage_info_v2`` from macOS ``<sys/resource.h>``."""

    _fields_ = [("ri_uuid", ctypes.c_uint8 * 16)] + [
        (name, ctypes.c_uint64)
        for name in (
            "ri_user_time", "ri_system_time", "ri_pkg_idle_wkups",
            "ri_interrupt_wkups", "ri_pageins", "ri_wired_size",
            "ri_resident_size", "ri_phys_footprint", "ri_proc_start_abstime",
            "ri_proc_exit_abstime", "ri_child_user_time", "ri_child_system_time",
            "ri_child_pkg_idle_wkups", "ri_child_interrupt_wkups",
            "ri_child_pageins", "ri_child_elapsed_abstime", "ri_diskio_bytesread",
            "ri_diskio_byteswritten",
        )
    ]


_RUSAGE_INFO_V2 = 2


def _process_phys_footprint_bytes() -> Optional[int]:
    """This process's current physical footprint; ``None`` off macOS.

    ``phys_footprint`` is the figure ``top``'s MEM column and ``footprint``
    report. Unlike ``ru_maxrss`` it counts unified MPS allocations and does
    not shrink when pages are compressed or swapped out, which is how a
    ``ru_maxrss`` reading hid the band-generation-2 thrash (GAP-57-05).
    Any failure reads as "unavailable".
    """
    if sys.platform != "darwin":
        return None
    try:
        info = _RusageInfoV2()
        libproc = ctypes.CDLL("/usr/lib/libproc.dylib")
        if libproc.proc_pid_rusage(os.getpid(), _RUSAGE_INFO_V2, ctypes.byref(info)) != 0:
            return None
        return int(info.ri_phys_footprint)
    except Exception:
        return None


class _FootprintPeakSampler:
    """The highest footprint a reader reports across one code window.

    Samples on entry, every ``interval_s`` from a daemon thread, and on exit.
    The window's peak therefore does not depend on anything the process did
    before it. The kernel's lifetime maximum does, and a long-lived process
    such as a test runner can pin it far above what the window allocates.
    A reader that is unavailable on entry disables sampling.
    """

    def __init__(
        self, read_footprint: Callable[[], Optional[int]], *, interval_s: float = 0.05,
    ) -> None:
        self._read_footprint = read_footprint
        self._interval_s = float(interval_s)
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.peak_bytes: Optional[int] = None

    def _sample(self) -> None:
        value = self._read_footprint()
        if value is not None and (self.peak_bytes is None or value > self.peak_bytes):
            self.peak_bytes = int(value)

    def _run(self) -> None:
        while not self._stop.wait(self._interval_s):
            self._sample()

    def __enter__(self) -> "_FootprintPeakSampler":
        self._sample()
        if self.peak_bytes is not None:
            self._thread = threading.Thread(
                target=self._run, name="footprint-peak-sampler", daemon=True,
            )
            self._thread.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        if self._thread is not None:
            self._stop.set()
            self._thread.join()
            self._sample()


def run_microbatch_memory_preflight(
    controller: Any,
    config: Any,
    *,
    step_guards: Any,
    stage: int = 0,
    footprint_signal: Optional[Callable[[], Optional[int]]] = None,
) -> dict[str, Any]:
    """Exercise the real Adam step once, at the configured microbatch size,
    before the first optimizer step -- 2026-09-09 band-generation-2 scope
    brief §3. ``57-05-PLAN.md`` Task 3 already requires this ("abort rather
    than reduce it if resource preflight fails"); no such check previously
    existed, so generation 1 discovered its ceiling by spending 851.9s of
    real wall clock inside the training loop (``blocked-state.json``). This
    makes that discovery a typed, fast refusal instead.

    Reads the memory signal through ``step_guards`` (the SAME accessor and
    total-bytes the run's own memory-watermark guard checks every step), so
    the preflight and the guard can never silently disagree about what
    "the watermark" means.

    The controller's own RNG stream is snapshotted and restored byte-for-
    byte in a ``finally`` block, so this probe changes NOTHING about which
    records the real run subsequently draws: band generation 2 remains
    bit-reproducible relative to a hypothetical run without this preflight.
    Model gradients accumulated by the probe step are zeroed before return
    for the same reason -- the real first step must start from a clean
    ``.grad``, exactly as if this preflight had not run.

    GAP-57-05 (owner ruling 2026-09-16): the probe also scores the frozen
    invariant-B monitor, which the real loop evaluates at the top of every
    Adam epoch, and checks the PEAK physical footprint sampled across the
    probed step and monitor against the same watermark fraction and total
    bytes. The MPS driver counter is read after the probed work has released
    its memory, so on its own it could not see the full-batch monitor's
    1.5 -> 22.8 GB per-epoch spike that thrashed the band-generation-2 smoke.
    ``footprint_signal`` reads the current footprint and is injectable for
    tests: ``None`` uses the real macOS counter, and a signal returning
    ``None`` skips that check. The monitor stash is restored afterwards, like
    the RNG and gradients.
    """
    rng = controller._rng
    saved_rng_state = copy.deepcopy(rng.bit_generator.state)
    saved_monitor_stats = controller._last_front_monitor_stats
    read_footprint = (
        footprint_signal if footprint_signal is not None else _process_phys_footprint_bytes
    )
    parameters = tuple(
        parameter for parameter in controller._model.parameters()
        if parameter.requires_grad
    )
    try:
        microbatch_size = int(config.opt.adam_microbatch_size)
        collocation_count = int(controller._collocation_count)
        total_bytes = int(step_guards.memory_total_bytes)
        threshold = float(step_guards.thresholds["memory_watermark_fraction"])
        result: dict[str, Any] = {"passed": True, "microbatch_size": microbatch_size}
        with _FootprintPeakSampler(read_footprint) as footprint:
            batch = controller._stage_batch(
                controller._train_source, stage=stage, collocation_count=collocation_count,
            )
            anchor_ctx = controller._build_anchor_context(
                controller._train_source, batch, None,
            )
            weights = controller._scheduled_weights.current(0)
            for parameter in parameters:
                parameter.grad = None
            controller._run_adam_step_microbatched(
                batch, anchor_ctx, weights, parameters,
                microbatch_size=microbatch_size, want_diagnostics=False,
            )
            allocated = step_guards.read_memory_signal()
            if allocated is not None:
                fraction = float(allocated) / float(total_bytes)
                if fraction > threshold:
                    raise ConformancePreflightError(
                        "resource preflight: exercising the configured microbatch "
                        f"({microbatch_size} rows) allocated {allocated} of "
                        f"{total_bytes} watermark bytes (fraction {fraction:.4f}), "
                        f"exceeding the {threshold} memory_watermark_fraction "
                        "threshold; refusing rather than silently reducing the "
                        "ratified sample count (GAP-57-01 fail-closed evidence)"
                    )
                result["measured_fraction"] = fraction
                result["threshold"] = threshold
            controller._evaluate_front_monitor()
        peak = footprint.peak_bytes
        if peak is not None:
            peak_fraction = float(peak) / float(total_bytes)
            if peak_fraction > threshold:
                raise ConformancePreflightError(
                    "resource preflight: the configured microbatch "
                    f"({microbatch_size} rows) and the frozen invariant-B "
                    f"monitor reached a peak physical footprint of {peak} "
                    f"of {total_bytes} watermark bytes (fraction "
                    f"{peak_fraction:.4f}), exceeding the {threshold} "
                    "memory_watermark_fraction threshold; the host would page "
                    "on every epoch, so refusing rather than thrashing (GAP-57-05)"
                )
            result["peak_footprint_bytes"] = peak
            result["peak_footprint_fraction"] = peak_fraction
            result["threshold"] = threshold
        if allocated is None and peak is None:
            result["reason"] = "memory signal unavailable on this platform; skipped"
        return result
    finally:
        for parameter in parameters:
            parameter.grad = None
        rng.bit_generator.state = saved_rng_state
        controller._last_front_monitor_stats = saved_monitor_stats
