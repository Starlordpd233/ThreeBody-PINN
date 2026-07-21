"""Phase 43 / ACC-02 — fail-closed fresh-launch Stage-0 timing calibration.

A completed Stage-0 smoke measures a real per-step wall time
(``RunController.s_per_step``). This module persists that measurement as a
versioned, fingerprinted artifact so a *later, freshly-launched* long run — which
has no in-memory EMA of its own yet — can obtain an honest duration forecast for
the >30-min launch gate (43-04) instead of an invented number.

The contract is deliberately one-directional and fail-closed:

* ``write_calibration`` refuses to persist anything unless the measured
  seconds-per-step is finite and strictly positive. A diverged / NaN / partial
  smoke never yields a ``valid`` calibration (SPEC edge R2 — "no fabricated
  forecast").
* the calibration is bound to the runtime **and the code** (device, dtype,
  torch/Python version, Git head), reusing ``pinn.verify``'s fingerprint so a
  calibration and a verify marker certify the same identity. A Git lookup
  failure records ``git_head_available: false`` and can NEVER authorize a long
  run — the code the measurement reflects cannot be identified.
* ``forecast_from_calibration`` returns a numeric forecast ONLY from the persisted
  measured seconds-per-step times the caller's requested Stage-0 budget, and only
  when the record is present, ``valid``, fresh, finite-positive, and an exact
  fingerprint match. Absent, malformed, stale, invalid, non-finite, or
  mismatched records return ``None`` (no forecast), never a fabricated one.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

from pinn.training.atomic_io import atomic_write_text
from pinn.verify import current_fingerprint

# --- calibration identity --------------------------------------------------

TIMING_SCHEMA_VERSION = "phase43-stage0-timing/v1"

#: Calibration location, relative to the runs root. Kept under ``runs/``
#: (gitignored, the home of every run-produced artifact), one shared record
#: rather than per-run so a fresh launch reads the most recent measurement.
CALIBRATION_RELATIVE_PATH = Path(".calibration") / "stage0-timing.json"

#: Overridable for tests, mirroring ``pinn.train._RUNS_ROOT`` / ``pinn.verify``.
_RUNS_ROOT: Path = Path("runs")

#: Freshness window for the launch forecast; matches the verify marker window so
#: an unattended machine/driver change cannot silently ride along on stale timing.
DEFAULT_MAX_CALIBRATION_AGE_S = 24 * 60 * 60


def timing_fingerprint(*, precision: str, device: str) -> dict[str, Any]:
    """Runtime + code fingerprint a calibration must match to stay authoritative.

    Reuses ``pinn.verify.current_fingerprint`` so a calibration and a verify
    marker certify the SAME ``{device, dtype, torch_version, python_version,
    git_head, git_head_available}`` identity.
    """
    return current_fingerprint(precision=precision, device=device)


def calibration_path(runs_root: Optional[Path] = None) -> Path:
    """Resolve the calibration path and refuse anything escaping the runs root."""
    root = Path(runs_root if runs_root is not None else _RUNS_ROOT).resolve()
    path = (root / CALIBRATION_RELATIVE_PATH).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:  # pragma: no cover — constant relative path
        raise ValueError(
            f"calibration path escapes the runs root: {path} !< {root}"
        ) from exc
    return path


def write_calibration(
    *,
    s_per_step: float,
    full_stage0_steps: int,
    precision: str,
    device: str,
    runs_root: Optional[Path] = None,
    now: Optional[datetime] = None,
) -> Path:
    """Atomically persist a ``valid`` Stage-0 timing calibration.

    Fail-closed: refuses (``ValueError``) unless ``s_per_step`` is finite and
    strictly positive and ``full_stage0_steps`` is a positive int — a diverged /
    partial / NaN smoke must never produce a ``valid`` calibration. The caller
    (``pinn.train``) is responsible for invoking this ONLY on a terminal-success
    smoke; this function enforces the finite-positive measurement invariant.
    """
    value = float(s_per_step)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(
            f"refusing to write a calibration with non-finite/non-positive "
            f"s_per_step={s_per_step!r}"
        )
    if (
        isinstance(full_stage0_steps, bool)
        or not isinstance(full_stage0_steps, int)
        or full_stage0_steps <= 0
    ):
        raise ValueError(
            f"full_stage0_steps must be a positive int (got {full_stage0_steps!r})"
        )
    stamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    payload = {
        "schema_version": TIMING_SCHEMA_VERSION,
        "s_per_step": value,
        "full_stage0_steps": int(full_stage0_steps),
        "forecast_seconds": value * int(full_stage0_steps),
        "timestamp": stamp.isoformat(),
        "fingerprint": timing_fingerprint(precision=precision, device=device),
        "valid": True,
    }
    destination = calibration_path(runs_root)
    return atomic_write_text(destination, json.dumps(payload, indent=2) + "\n")


def read_calibration(runs_root: Optional[Path] = None) -> Optional[dict[str, Any]]:
    """Read the calibration, or None when absent/unreadable/not valid JSON."""
    path = calibration_path(runs_root)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        record = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(record, dict):
        return None
    return record


def calibration_is_valid(
    record: Optional[Mapping[str, Any]],
    *,
    fingerprint: Mapping[str, Any],
    now: Optional[datetime] = None,
    max_age_s: float = DEFAULT_MAX_CALIBRATION_AGE_S,
) -> bool:
    """Fail-closed: ``valid`` AND finite-positive AND fresh AND full match.

    Every fingerprint value is compared, including ``git_head`` and
    ``git_head_available`` — so a calibration from *different code*, a different
    Torch/Python build, a different device/dtype, or a run whose code identity
    could not be established never authorizes a long run.
    """
    if not isinstance(record, Mapping):
        return False
    if record.get("valid") is not True:
        return False
    if record.get("schema_version") != TIMING_SCHEMA_VERSION:
        return False

    s_per_step = record.get("s_per_step")
    if not isinstance(s_per_step, (int, float)) or isinstance(s_per_step, bool):
        return False
    if not math.isfinite(float(s_per_step)) or float(s_per_step) <= 0.0:
        return False

    stamp = record.get("timestamp")
    if not isinstance(stamp, str):
        return False
    try:
        written = datetime.fromisoformat(stamp)
    except ValueError:
        return False
    if written.tzinfo is None:
        return False
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    age_s = (current - written.astimezone(timezone.utc)).total_seconds()
    if age_s < 0 or age_s > float(max_age_s):
        return False

    recorded = record.get("fingerprint")
    if not isinstance(recorded, Mapping):
        return False
    # A calibration whose code identity is unknown can never authorize a run.
    if not recorded.get("git_head_available") or not fingerprint.get(
        "git_head_available"
    ):
        return False
    for key, expected in fingerprint.items():
        if recorded.get(key) != expected:
            return False
    return True


def forecast_from_calibration(
    runs_root: Optional[Path] = None,
    *,
    requested_steps: int,
    fingerprint: Mapping[str, Any],
    now: Optional[datetime] = None,
    max_age_s: float = DEFAULT_MAX_CALIBRATION_AGE_S,
) -> Optional[float]:
    """Return ``s_per_step * requested_steps`` from a valid matching calibration.

    Returns ``None`` — never a fabricated number — when the calibration is
    absent, malformed, invalid, non-finite, stale, or fingerprint-mismatched.
    The forecast is computed from the PERSISTED measured seconds-per-step times
    the caller's requested Stage-0 budget (not the record's own recorded budget),
    so the launch gate compares its own declared run length against 30 minutes.
    """
    if (
        isinstance(requested_steps, bool)
        or not isinstance(requested_steps, int)
        or requested_steps <= 0
    ):
        return None
    record = read_calibration(runs_root)
    if not calibration_is_valid(
        record, fingerprint=fingerprint, now=now, max_age_s=max_age_s
    ):
        return None
    assert record is not None  # calibration_is_valid guarantees a Mapping
    return float(record["s_per_step"]) * int(requested_steps)
