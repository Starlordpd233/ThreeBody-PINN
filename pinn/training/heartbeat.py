"""Liveness + honesty surface: the ``status.json`` timestamped heartbeat (OPS-04a / E3).

Builds the pure schema/render/write functions plus the daemon ``HeartbeatThread``
that answers "is it alive / healthy?" from a single atomically-rewritten file.
Freshness ≡ **process liveness** (CTX-74): a multi-minute L-BFGS line search with
a frozen step count still heartbeats, while a dead/hung process goes stale — a
reader classifies running-vs-stalled from ``now − timestamp_epoch >
staleness_threshold_secs`` using only the file's own carried threshold (CTX-75).

Memory-sampling discipline (cycle-2 review finding, claude MEDIUM; CTX-76):
    MPS APIs (``torch.mps.*``) are main-thread-affine. The daemon ``run()`` body
    contains **zero** ``torch.mps.*`` calls and reads ONLY a mutex-guarded cached
    snapshot. The MAIN step loop samples memory once per logged step via
    :func:`sample_memory_fields` (reusing the existing guard signal) and pushes the
    cached value into the snapshot via ``HeartbeatThread.update(mem=...)``.
    :func:`build_status_snapshot` accepts the pre-sampled ``mem`` and performs no
    MPS query itself. No new dependency.

Thread-safety (cycle-2 review finding, agy LOW):
    The snapshot mutex guards BOTH snapshot generation AND the ``write_status``
    I/O. The daemon's tick body, ``update(...)``, and ``transition(state)`` each
    take the SAME lock, then build the snapshot, then call ``write_status`` UNDER
    that lock before releasing — so a synchronous ``transition()`` from the main
    thread and a daemon tick never race on ``atomic_write_text``'s shared
    ``.tmp.{pid}`` suffix, preserving E3's "reader never sees truncated JSON"
    invariant under contention.

The thread is started/stopped only from ``pinn.train`` main() (42-08); this module
provides the class + pure builders. Every rewrite reuses
``pinn.training.atomic_io.atomic_write_text`` (do NOT reimplement atomic write).
"""

from __future__ import annotations

import json
import logging
import math
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

from pinn.training.atomic_io import atomic_write_text

PathLike = Union[str, Path]

_LOGGER = logging.getLogger("pinn.training.heartbeat")

# status.json schema version (CTX-75). Bump only on a breaking schema change.
SCHEMA_VERSION = 1

# Canonical loss terms: the five terms + total (CTX-68 / CTX-75). A term that
# never finalized stays null (CTX-67 null policy; never fabricated — Anti-Pattern #7).
_LOSS_TERMS = ("data", "ic", "phys", "energy", "angmom", "total")

# Terminal + startup states (CTX-74).
_VALID_STATES = frozenset(
    {"initializing", "running", "finished", "failed", "interrupted"}
)


def _null_if_nonfinite(value: Any) -> Optional[float]:
    """Apply the CTX-67 null policy to a single scalar field.

    ``None`` or a non-finite (NaN/Inf) value serializes as JSON ``null``; a finite
    value is returned as a float. String sentinels are prohibited (CTX-67).
    """
    if value is None:
        return None
    try:
        fv = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(fv):
        return None
    return fv


def build_status_snapshot(
    *,
    state: str,
    run_name: Optional[str],
    pid: Optional[int],
    step: Optional[int],
    stage: Optional[int],
    phase: Optional[str],
    epoch: Optional[int],
    losses: Optional[Mapping[str, Any]],
    lr: Optional[float],
    s_per_step_ema: Optional[float],
    eta_seconds: Optional[float],
    mem: Optional[Mapping[str, Any]],
    heartbeat_secs: int,
    staleness_factor: int,
) -> Dict[str, Any]:
    """Return the CTX-75 ``status.json`` schema dict for the current instant.

    Pure: performs no I/O and no MPS query. The ``mem`` argument is the
    pre-sampled memory mapping from :func:`sample_memory_fields` (main thread);
    the ``initializing`` snapshot is built with ``step=None`` and null losses
    (Anti-Pattern #7 — never fabricate pre-step-0 losses). The file carries its
    own ``staleness_threshold_secs = heartbeat_secs * staleness_factor`` so a
    reader needs no external constant.
    """
    now = time.time()
    timestamp_utc = datetime.fromtimestamp(now, tz=timezone.utc).isoformat()
    loss_src: Mapping[str, Any] = losses or {}
    mem_src: Mapping[str, Any] = mem or {}
    return {
        "schema_version": SCHEMA_VERSION,
        "run_name": run_name,
        "pid": pid,
        "state": state,
        "timestamp_utc": timestamp_utc,
        "timestamp_epoch": now,
        "heartbeat_interval_secs": heartbeat_secs,
        "staleness_threshold_secs": heartbeat_secs * staleness_factor,
        "step": step,
        "stage": stage,
        "phase": phase,
        "epoch": epoch,
        "losses": {
            term: _null_if_nonfinite(loss_src.get(term)) for term in _LOSS_TERMS
        },
        "lr": _null_if_nonfinite(lr),
        "s_per_step_ema": _null_if_nonfinite(s_per_step_ema),
        "eta_seconds": _null_if_nonfinite(eta_seconds),
        "memory": {
            "driver_bytes": mem_src.get("driver_bytes"),
            "current_bytes": mem_src.get("current_bytes"),
        },
    }


def write_status(path: PathLike, snapshot: Mapping[str, Any]) -> Path:
    """Serialize ``snapshot`` and atomically write it to ``path``.

    Reuses ``atomic_io.atomic_write_text`` (temp + fsync + os.replace + dir fsync)
    — the rename is the only state-visible mutation, so a reader never sees a
    truncated/partial ``status.json`` (E3). ``allow_nan=False`` guarantees every
    emitted byte parses under any JSON parser (CTX-67); non-finite fields are
    already null by :func:`build_status_snapshot`.
    """
    text = json.dumps(snapshot, sort_keys=True, indent=2, allow_nan=False) + "\n"
    return atomic_write_text(path, text)


def sample_memory_fields() -> Dict[str, Optional[int]]:
    """MAIN-THREAD ONLY — sample the memory fields mirrored into ``status.json``.

    Reuses the existing guard memory signal (``guards._default_memory_signal`` →
    ``torch.mps.driver_allocated_memory``) as the primary field and
    ``torch.mps.current_allocated_memory`` as the secondary field (CTX-76 /
    RESEARCH). No new dependency. The daemon ``HeartbeatThread`` MUST NOT call this — MPS
    APIs are main-thread-affine and concurrent daemon calls during live compute are
    unsafe and meaningless. The main step loop calls this once per logged step and
    pushes the result via ``HeartbeatThread.update(mem=...)``.
    """
    # Deferred import keeps this module importable without torch at module load
    # (mirrors atomic_io / guards deferred-import convention).
    from pinn.training.guards import _default_memory_signal

    driver = _default_memory_signal()
    current: Optional[int] = None
    try:
        import torch

        if hasattr(torch, "mps"):
            current = int(torch.mps.current_allocated_memory())
    except Exception:
        current = None
    return {"driver_bytes": driver, "current_bytes": current}


def emit_mem_line(
    mem_fields: Optional[Mapping[str, Any]],
    *,
    logger: logging.Logger = _LOGGER,
) -> None:
    """MAIN-THREAD ONLY — emit the periodic ``mem:`` line to ``train.log`` (CTX-76).

    Called from the SAME main-thread update that cached the value (never from the
    daemon). The line is mirrored into ``status.json`` memory fields via
    ``HeartbeatThread.update(mem=...)``.
    """
    fields: Mapping[str, Any] = mem_fields or {}
    logger.info(
        "mem: driver_bytes=%s current_bytes=%s",
        fields.get("driver_bytes"),
        fields.get("current_bytes"),
    )


class HeartbeatThread(threading.Thread):
    """Daemon thread rewriting ``status.json`` on a K-second cadence (CTX-74).

    Reads ONLY a mutex-guarded cached snapshot — the daemon ``run()`` body performs
    no ``torch.mps.*`` query (memory is main-thread-sampled and pushed via
    ``update(mem=...)``). Exposes:

    - ``update(**fields)`` — the step loop pushes step/losses/mem/etc.; performs a
      synchronous atomic rewrite (CTX-74: rewrite at every logged step).
    - ``transition(state)`` — forces a synchronous atomic rewrite on a state
      transition (initializing → running → finished/failed/interrupted).
    - ``stop()`` — sets the stop flag; the daemon exits at the next cadence tick
      (or immediately if waiting) and never blocks process exit.

    A heartbeat write exception is swallowed (warn-once) — the monitoring thread
    never crashes the process it monitors.
    """

    daemon = True  # class-level: every instance is a daemon (never blocks exit)

    def __init__(
        self,
        status_path: PathLike,
        *,
        heartbeat_secs: int,
        staleness_factor: int,
        run_name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> None:
        super().__init__(daemon=True)
        self._status_path = status_path
        self._heartbeat_secs = heartbeat_secs
        self._staleness_factor = staleness_factor
        # One lock guards snapshot generation AND write_status I/O (thread-safety
        # invariant — see module docstring).
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._warned_write_failure = False
        # Mutable snapshot input fields (main thread pushes via update()).
        self._fields: Dict[str, Any] = {
            "state": "initializing",
            "run_name": run_name,
            "pid": pid,
            "step": None,
            "stage": None,
            "phase": None,
            "epoch": None,
            "losses": None,
            "lr": None,
            "s_per_step_ema": None,
            "eta_seconds": None,
            "mem": None,
        }

    # ---- internal: caller MUST hold self._lock --------------------------------
    def _rewrite_locked(self) -> None:
        snapshot = build_status_snapshot(
            heartbeat_secs=self._heartbeat_secs,
            staleness_factor=self._staleness_factor,
            **self._fields,
        )
        write_status(self._status_path, snapshot)

    def _warn_once(self) -> None:
        if not self._warned_write_failure:
            _LOGGER.warning(
                "heartbeat status.json write failed; suppressing further warnings",
                exc_info=True,
            )
            self._warned_write_failure = True

    # ---- public API -----------------------------------------------------------
    def write_initial(self) -> None:
        """Write the startup ``initializing`` snapshot (E3) before model/data build.

        ``step`` is null and loss fields are null (never fabricated). Called once
        from the composition root immediately after run-dir creation.
        """
        try:
            with self._lock:
                self._rewrite_locked()
        except Exception:
            self._warn_once()

    def update(self, **fields: Any) -> None:
        """Push new snapshot fields (main thread) and synchronously rewrite.

        Field-update + snapshot-build + ``write_status`` all happen UNDER the same
        lock so a concurrent daemon tick or ``transition()`` never races on the
        shared ``.tmp.{pid}`` temp path.
        """
        try:
            with self._lock:
                self._fields.update(fields)
                self._rewrite_locked()
        except Exception:
            self._warn_once()

    def transition(self, state: str) -> None:
        """Force a synchronous atomic rewrite on a state transition (CTX-74)."""
        try:
            with self._lock:
                self._fields["state"] = state
                self._rewrite_locked()
        except Exception:
            self._warn_once()

    def stop(self) -> None:
        """Signal the daemon to exit; never blocks process exit."""
        self._stop_event.set()

    # ---- daemon loop ----------------------------------------------------------
    def run(self) -> None:
        """Periodic rewrite loop. Performs no MPS query here — reads only the
        cached, mutex-guarded snapshot. A live process with a frozen step count
        still refreshes the timestamp (freshness ≡ process liveness, CTX-74)."""
        while not self._stop_event.wait(self._heartbeat_secs):
            try:
                with self._lock:
                    self._rewrite_locked()
            except Exception:
                self._warn_once()
