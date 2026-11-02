"""Phase 67: the registration-bound diagnostic run reader.

``read_phase67_record`` reads one Phase 67 run directory against its committed
fit registration: the registration is admitted through the existing
committed-registration door (metadata-only, before any corpus access), its
settings must name the Phase 67 registry, and the run's record, weights,
power-gate receipt and attempt claim are audited into value-free
``mechanical_problems`` and ``setting_problems`` lists beside the registered
identity — the reader derives its expectations from the registration, never
from the record. Frozen scores are exposed only when ``include_scores`` is
requested AND the audit is clean.

The reader owns no scientific branch table: the EXP-02..05 reading rules
belong to their own committed prediction pages (later plans). It reuses the
existing registration-bound fit verification (``verify_fit_result``) as its
record audit, adds the run-directory evidence the fit verifier does not read
(the AC/weekend receipt and the exclusive attempt claim, with the weekday
derived from the receipt's own local time rather than its self-declared
field), and checks every logged layer row against the registered depth.
Malformed evidence becomes a value-free problem, never a traceback
(66-REVIEW CR-02's accepted limitation, not inherited here).

This module imports the fit harness lazily (inside the reader), so the catalog
module the harness imports at module level never sees a cycle. The window and
receipt constants come from the launcher itself, so the gate and the auditor
cannot drift apart.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pinn.verification.diagnostic_phase67_catalog import PHASE67_REGISTRY_NAME
from pinn.verification.diagnostic_power import (
    AC_SOURCE,
    RECEIPT_SCHEMA,
    WINDOW_SUNDAY_LAST_HOUR,
    WINDOW_TIMEZONE,
)

__all__ = [
    "Phase67RecordRefused",
    "read_phase67_record",
    "registered_layers",
]

# Value-free mechanical problem strings: none embeds a score value, so a
# caller can print the problems without exposing an unread score.
_PROBLEM_FIT_AUDIT = "the result fails the registration-bound fit verification"
_PROBLEM_RECORD_UNREADABLE = "the record is not a readable diagnostic record"
_PROBLEM_LAYERS = (
    "the similarity log does not carry exactly the registered layers in order"
)
_PROBLEM_TIER = "the recorded scorecard grade disagrees with the network error"
_PROBLEM_ACCESS = "the record carries no access evidence"
_PROBLEM_SPLITS = "a validation or test split was opened"
_PROBLEM_RECEIPT_MISSING = "the power-gate receipt is missing"
_PROBLEM_RECEIPT_UNREADABLE = "the power-gate receipt is not a readable JSON object"
_PROBLEM_RECEIPT_SCHEMA = "the receipt schema is not the launcher's power-gate schema"
_PROBLEM_RECEIPT_SOURCE = "the receipt does not record AC Power"
_PROBLEM_RECEIPT_WINDOW = "the receipt window is outside the weekend window"
_PROBLEM_TIMESTAMPS = (
    "a receipt or attempt timestamp is missing or not timezone-aware ISO 8601"
)
_PROBLEM_RECEIPT_LATE = "the receipt was written after the attempt started"
_PROBLEM_ATTEMPT_MISSING = "the attempt claim is missing"
_PROBLEM_ATTEMPT_UNREADABLE = "the attempt claim is not a readable JSON object"
_PROBLEM_ATTEMPT_STATUS = "the attempt is not published"
_PROBLEM_ATTEMPT_DIGEST = (
    "the attempt's record digest disagrees with the record bytes"
)


class Phase67RecordRefused(RuntimeError):
    """The Phase 67 reader cannot read this run directory at all."""


def registered_layers(depth):
    """The layer rows a fit at ``depth`` hidden layers logs, in order.

    The shared similarity logger hooks the input layer as ``input`` and each
    hidden layer as ``h1``..``h{depth}``; the order is the hook order, so a
    registered depth fixes the expected row names deterministically.
    """
    count = int(depth)
    if count < 1:
        raise ValueError(f"a diagnostic depth is at least 1; got {depth!r}")
    return ["input"] + [f"h{order}" for order in range(1, count + 1)]


def _read_json_object(path):
    """The parsed JSON object at ``path``, or ``None`` when unreadable."""
    try:
        payload = json.loads(Path(path).read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def _aware_datetime(value):
    """The timezone-aware datetime in ``value``, or ``None``."""
    if not isinstance(value, str):
        return None
    try:
        moment = datetime.fromisoformat(value)
    except ValueError:
        return None
    if moment.tzinfo is None or moment.tzinfo.utcoffset(moment) is None:
        return None
    return moment


def _receipt_window_ok(window):
    """The receipt's window block, audited on its own local time.

    The declared ``isoweekday`` must agree with the weekday the recorded
    ``local_time`` itself carries (a self-declared weekday is not evidence),
    and the Chicago local time must sit inside the owner's weekend window.
    """
    if not isinstance(window, Mapping):
        return False
    declared = window.get("isoweekday")
    if isinstance(declared, bool) or not isinstance(declared, int):
        return False
    if window.get("timezone") != WINDOW_TIMEZONE:
        return False
    moment = _aware_datetime(window.get("local_time"))
    if moment is None:
        return False
    try:
        local = moment.astimezone(ZoneInfo(WINDOW_TIMEZONE))
    except (ValueError, OSError):
        return False
    if local.isoweekday() != declared:
        return False
    return local.isoweekday() == 6 or (
        local.isoweekday() == 7 and local.hour < WINDOW_SUNDAY_LAST_HOUR
    )


def _split_opens(record):
    """``(opens, access_present)`` from the record's own access evidence.

    Fail-closed: a record whose access block is missing cannot attest
    TRAIN-only access, so the caller flags it separately from any counted
    validation or test split open.
    """
    access = record.get("access")
    if not isinstance(access, Mapping):
        return 0, False
    total = 0
    blocks = [access.get("reads"), access.get("attestation")]
    attestation = access.get("attestation")
    if isinstance(attestation, Mapping):
        blocks.append(attestation.get("opened"))
    for block in blocks:
        if not isinstance(block, Mapping):
            continue
        for key in ("validation", "test", "test_split_opened", "test_split_opens"):
            value = block.get(key, 0)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            total += int(value)
    return total, True


def _tier1_max():
    """The frozen scorecard's Tier-1 E limit, read from the scorecard itself."""
    from pinn.verification.diagnostic_phase66 import tier1_e_max
    from pinn.verification.feasibility_scorecard import load_scorecard

    return tier1_e_max(load_scorecard())


def read_phase67_record(registration_path, run_dir, *, repo_root, include_scores=False):
    """One Phase 67 run directory read against its committed registration.

    The registration is admitted first (committed-clean artifacts, settings
    against the registry, the logger-parity receipt — all metadata-only, no
    corpus opens), and its settings must name the Phase 67 registry; anything
    else is a typed refusal, as is a run directory with no ``record.json``.
    The record is then audited through the existing registration-bound
    ``verify_fit_result`` plus the receipt, attempt, layer-row, split and
    tier-consistency checks into value-free problem lists. Returns the
    registered identity (registration citation, variant, orbit key, seed,
    runtime, physical window and the expected layer rows) with
    ``mechanical_problems`` and ``setting_problems``; ``setting_problems`` is
    reserved for the experiment-specific reading rules of later plans, so it
    is empty on every clean raw-path reading today. With ``include_scores``
    the frozen network score and both comparison rows are added — only when
    the audit is clean, otherwise a typed refusal.
    """
    from pinn.verification.diagnostic_fit import (
        RECORD_NAME,
        DiagnosticFitRefused,
        require_committed_smoke_registration,
        validate_smoke_settings,
        verify_fit_result,
    )
    from pinn.verification.diagnostic_guard import (
        DiagnosticArtifactRefused,
        DiagnosticRegistrationRefused,
    )

    root, doc = require_committed_smoke_registration(
        registration_path, repo_root=repo_root
    )
    settings, variant, _orbit_key, _runtime_pair = validate_smoke_settings(doc)
    if settings.get("variant_registry") != PHASE67_REGISTRY_NAME:
        raise Phase67RecordRefused(
            "the Phase 67 reader reads phase67 registrations only; the settings "
            f"name variant_registry {settings.get('variant_registry')!r}"
        )
    registration_file = Path(registration_path)
    if not registration_file.is_absolute():
        registration_file = root / registration_file
    try:
        registration_relative = registration_file.resolve().relative_to(root).as_posix()
    except ValueError:
        registration_relative = registration_file.as_posix()
    directory = Path(run_dir)
    if not directory.is_absolute():
        directory = root / directory
    record_path = directory / RECORD_NAME
    if not record_path.is_file():
        raise Phase67RecordRefused(
            f"the run directory carries no {RECORD_NAME}: {directory}"
        )

    layers = registered_layers(variant.depth)
    identity = {
        "registration": {
            "path": registration_relative,
            "sha256": hashlib.sha256(registration_file.read_bytes()).hexdigest(),
        },
        "variant": {**variant.to_json_dict(), "registry": PHASE67_REGISTRY_NAME},
        "orbit_key": settings["orbit_key"],
        "seed": int(settings["seed"]),
        "runtime": dict(settings["runtime"]),
        "physical_window": dict(settings["physical_window"]),
        "layers": layers,
    }
    mechanical: list[str] = []

    # 1) The registration-bound record audit: identity, cadence, steps,
    #    optimizer policy, window, weights bytes and pinned sources.
    try:
        verify_fit_result(registration_path, record_path, repo_root=root)
    except (
        DiagnosticFitRefused,
        DiagnosticRegistrationRefused,
        DiagnosticArtifactRefused,
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
    ):
        mechanical.append(_PROBLEM_FIT_AUDIT)

    # 2) The record's own shape-guarded checks (never a traceback).
    record_raw = record_path.read_bytes()
    try:
        record = json.loads(record_raw.decode("utf-8"))
        if not isinstance(record, dict):
            raise ValueError("not an object")
    except (UnicodeDecodeError, ValueError):
        record = None
        mechanical.append(_PROBLEM_RECORD_UNREADABLE)
    if isinstance(record, dict):
        entries = (record.get("similarity") or {}).get("entries")
        if not isinstance(entries, list) or not entries or any(
            not isinstance(entry, dict)
            or [layer.get("name") for layer in (entry.get("layers") or [])] != layers
            for entry in entries
        ):
            mechanical.append(_PROBLEM_LAYERS)
        network = (record.get("scores") or {}).get("network")
        if not isinstance(network, dict):
            network = {}
            mechanical.append(_PROBLEM_TIER)
        else:
            e_value = network.get("E")
            tier_value = network.get("tier")
            e_number = (
                not isinstance(e_value, bool)
                and isinstance(e_value, (int, float))
                and math.isfinite(float(e_value))
            )
            tier_int = not isinstance(tier_value, bool) and isinstance(tier_value, int)
            if not (e_number and tier_int):
                mechanical.append(_PROBLEM_TIER)
            else:
                try:
                    limit = _tier1_max()
                except Exception:
                    limit = None
                    mechanical.append(_PROBLEM_TIER)
                if limit is not None and (
                    (float(e_value) <= limit and tier_value < 1)
                    or (float(e_value) > limit and tier_value != 0)
                ):
                    mechanical.append(_PROBLEM_TIER)
        opens, access_present = _split_opens(record)
        if not access_present:
            mechanical.append(_PROBLEM_ACCESS)
        elif opens:
            mechanical.append(_PROBLEM_SPLITS)
    else:
        mechanical.append(_PROBLEM_LAYERS)
        mechanical.append(_PROBLEM_TIER)
        mechanical.append(_PROBLEM_ACCESS)

    # 3) The launcher receipt: AC power inside the owner's weekend window.
    receipt = _read_json_object(directory / "power-gate.json")
    receipt_path = directory / "power-gate.json"
    if not receipt_path.is_file():
        mechanical.append(_PROBLEM_RECEIPT_MISSING)
    elif receipt is None:
        mechanical.append(_PROBLEM_RECEIPT_UNREADABLE)
    else:
        if receipt.get("schema") != RECEIPT_SCHEMA:
            mechanical.append(_PROBLEM_RECEIPT_SCHEMA)
        if receipt.get("power_source") != AC_SOURCE:
            mechanical.append(_PROBLEM_RECEIPT_SOURCE)
        if not _receipt_window_ok(receipt.get("window")):
            mechanical.append(_PROBLEM_RECEIPT_WINDOW)

    # 4) The exclusive attempt claim: published, digest-faithful, not preceded
    #    by its own receipt.
    attempt = _read_json_object(directory / "attempt.json")
    attempt_path = directory / "attempt.json"
    if not attempt_path.is_file():
        mechanical.append(_PROBLEM_ATTEMPT_MISSING)
    elif attempt is None:
        mechanical.append(_PROBLEM_ATTEMPT_UNREADABLE)
    else:
        if attempt.get("status") != "published":
            mechanical.append(_PROBLEM_ATTEMPT_STATUS)
        if attempt.get("record_sha256") != hashlib.sha256(record_raw).hexdigest():
            mechanical.append(_PROBLEM_ATTEMPT_DIGEST)

    if receipt is not None and attempt is not None:
        checked = _aware_datetime(receipt.get("checked_utc"))
        started = _aware_datetime(attempt.get("started_utc"))
        if checked is None or started is None:
            mechanical.append(_PROBLEM_TIMESTAMPS)
        elif checked > started:
            mechanical.append(_PROBLEM_RECEIPT_LATE)

    reading = {
        **identity,
        "mechanical_problems": mechanical,
        "setting_problems": [],
    }
    if include_scores:
        if mechanical or reading["setting_problems"]:
            raise Phase67RecordRefused(
                "the Phase 67 reader exposes scores only after a clean audit; "
                f"this reading carries {len(mechanical)} mechanical problems"
            )
        if not isinstance(record, dict):
            raise Phase67RecordRefused(_PROBLEM_RECORD_UNREADABLE)
        reading["scores"] = {
            "network": (record.get("scores") or {}).get("network") or {},
            "comparisons": list(record.get("comparisons") or []),
        }
    return reading
