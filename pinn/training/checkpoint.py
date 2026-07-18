"""Phase 40/41 — CheckpointStore Protocol + production store (CTRL-02..04).

Protocol surface for CurriculumController RECOVER (CTX-43):
    save(state) -> id
    load_latest() -> state
    rollback() -> last well-formed state

Phase 41 replaces the naive body of ``TorchSaveCheckpointStore`` with the
production store behind the SAME class name so phase-40 imports keep working.
Every load path passes ``weights_only=True`` (T-40-02 / T-41-05). Writes go
through ``atomic_io.atomic_write_torch`` (tmp → fsync → os.replace → dir-fsync).

``CHECKPOINT_SCHEMA_VERSION`` is the single source of truth for the CTX-53
payload schema version (cycle-2 HIGH 4). 41-04 imports it; never redefine.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Callable, Optional, Protocol, Union, runtime_checkable

from pinn.training.atomic_io import atomic_write_torch
from pinn.training.config import CheckpointCadence

PathLike = Union[str, Path]

# Single source of truth for CTX-53 payload schema version (wave-2 owned).
CHECKPOINT_SCHEMA_VERSION: int = 1

# CTX-53 required top-level keys — presence check, not truthiness.
_CTX53_REQUIRED_KEYS: tuple[str, ...] = (
    "model",
    "optimizer",
    "curriculum",
    "rng",
    "counters",
    "config_identity",
    "schema_version",
)

_STEP_RE = re.compile(r"^step-(\d+)\.pt$")
_STAGE_ANCHOR_RE = re.compile(r"^stage-\d+-(?:final|init)\.pt$")
_FAILURE_RE = re.compile(r"^failure-stage-\d+-step-(\d+)\.pt$")
_INIT_ANCHOR_RE = re.compile(r"^stage-\d+-init\.pt$")

# Adam-only slice terminal stage (stages 0..2); promotion into >=3 refused.
_DEFAULT_TERMINAL_STAGE = 2


class EmptyCheckpointStore(RuntimeError):
    """Raised when load_latest/rollback is called with no successful save yet.

    Also constructible as a no-op store surface (HIGH 5) so CurriculumController
    disposition calls and 41-05 ``load_checkpoint`` are safe against any store
    without controller-side ``hasattr`` guards. Instance methods are no-ops
    (or raise ``NoValidCheckpointError`` for load paths with nothing to load).
    """

    def __init__(self, message: str = "empty checkpoint store") -> None:
        super().__init__(message)

    def save(self, state: Any) -> str:
        return ""

    def load_latest(self) -> Any:
        raise EmptyCheckpointStore(
            "load_latest on empty CheckpointStore (no successful save yet)"
        )

    def rollback(self) -> Any:
        raise EmptyCheckpointStore(
            "rollback on empty CheckpointStore (no successful save yet)"
        )

    def save_anchor(self, tag: str, stage: int, payload: Any) -> Optional[str]:
        return None

    def record_disposition(
        self,
        from_stage: int,
        to_stage: int,
        disposition: Any,
        step: int,
    ) -> bool:
        return False

    def promote(self, from_stage: int, to_stage: int) -> bool:
        return True

    def save_rolling(self, payload: Any, step: int) -> str:
        return ""

    def save_best(self, payload: Any) -> str:
        return ""

    def load_checkpoint(self, path: PathLike) -> Any:
        raise NoValidCheckpointError(path)

    def should_checkpoint(self, step: int, elapsed: float) -> bool:
        return False

    def fallback_scan(self) -> Any:
        raise NoValidCheckpointError(".")


class NoValidCheckpointError(RuntimeError):
    """No structurally-valid checkpoint found at the named path/directory."""

    def __init__(self, location: PathLike) -> None:
        self.location = str(location)
        super().__init__(f"no valid checkpoint at {self.location}")


class PromotionRefused(ValueError):
    """Ordered-promotion guard refused a skip, regress, or beyond-terminal."""

    def __init__(self, from_stage: int, to_stage: int, reason: str) -> None:
        self.from_stage = int(from_stage)
        self.to_stage = int(to_stage)
        self.reason = reason
        super().__init__(
            f"promotion refused from_stage={self.from_stage} "
            f"to_stage={self.to_stage}: {reason}"
        )


@runtime_checkable
class CheckpointStore(Protocol):
    """Narrow seam for Phase-41 swap (CTX-43)."""

    def save(self, state: Any) -> str:
        """Persist ``state``; return a checkpoint id."""
        ...

    def load_latest(self) -> Any:
        """Return the most recently saved well-formed state."""
        ...

    def rollback(self) -> Any:
        """Return the last well-formed saved state (RECOVER target)."""
        ...


def _as_path(path: PathLike) -> Path:
    return path if isinstance(path, Path) else Path(path)


def _disposition_str(disposition: Any) -> str:
    if hasattr(disposition, "value"):
        return str(disposition.value)
    return str(disposition)


def _is_structurally_valid(payload: Any) -> bool:
    """CTX-53 structural validity: required-key PRESENCE + matching schema.

    Presence, not truthiness — ``optimizer: None`` (stage-init / CTRL-06) is
    accepted.
    """
    if not isinstance(payload, dict):
        return False
    for key in _CTX53_REQUIRED_KEYS:
        if key not in payload:
            return False
    if payload.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        return False
    return True


def _parse_step_index(name: str) -> Optional[int]:
    match = _STEP_RE.match(name)
    if match:
        return int(match.group(1))
    return None


def _parse_failure_step(name: str) -> Optional[int]:
    match = _FAILURE_RE.match(name)
    if match:
        return int(match.group(1))
    return None


class TorchSaveCheckpointStore:
    """Production checkpoint store (CTRL-02/03/04) — name preserved for phase-40.

    Rooted at ``runs/<name>/checkpoints/``. Writes are atomic via
    ``atomic_write_torch``. Every load site passes the weights_only flag.
    """

    def __init__(
        self,
        root: PathLike,
        *,
        cadence: Optional[CheckpointCadence] = None,
        clock: Optional[Callable[[], float]] = None,
        terminal_stage: int = _DEFAULT_TERMINAL_STAGE,
        every_n_steps: Optional[int] = None,
        wall_clock_ceiling_s: Optional[float] = None,
        rolling_keep: Optional[int] = None,
        failure_keep: Optional[int] = None,
        config: Any = None,
    ) -> None:
        self._root = _as_path(root)
        self._root.mkdir(parents=True, exist_ok=True)
        # Phase-40 compatibility: some tests introspect ``_ids`` to assert a
        # genuinely-empty store (no prior save). Kept as a simple append-only
        # list of Protocol ``save()`` return ids — not used for production
        # latest/fallback resolution.
        self._ids: list[str] = []

        # Resolve cadence: explicit CheckpointCadence > TrainingConfig.run.checkpoint
        # > individual kwargs > defaults. Ceiling stays a ⚖ provisional config value.
        if cadence is None and config is not None:
            run = getattr(config, "run", None)
            cad = getattr(run, "checkpoint", None) if run is not None else None
            if isinstance(cad, CheckpointCadence):
                cadence = cad
        if cadence is None:
            # Build from defaults, overlaying any explicit kwargs.
            defaults = CheckpointCadence()
            cadence = CheckpointCadence(
                every_n_steps=(
                    every_n_steps
                    if every_n_steps is not None
                    else defaults.every_n_steps
                ),
                wall_clock_ceiling_s=(
                    wall_clock_ceiling_s
                    if wall_clock_ceiling_s is not None
                    else defaults.wall_clock_ceiling_s
                ),
                rolling_keep=(
                    rolling_keep
                    if rolling_keep is not None
                    else defaults.rolling_keep
                ),
                failure_keep=(
                    failure_keep
                    if failure_keep is not None
                    else defaults.failure_keep
                ),
            )
        self._every_n_steps = int(cadence.every_n_steps)
        self._wall_clock_ceiling_s = float(cadence.wall_clock_ceiling_s)
        self._rolling_keep = int(cadence.rolling_keep)
        self._failure_keep = int(cadence.failure_keep)

        # LOW-3: injectable monotonic clock; default time.monotonic (never time.time).
        self._clock: Callable[[], float] = clock if clock is not None else time.monotonic
        self._terminal_stage = int(terminal_stage)

        # Dual-trigger bookkeeping: elapsed is time-since-LAST-checkpoint.
        self._last_written_step: int = -1
        self._last_written_time: float = float(self._clock())

        # curriculum.jsonl lives at runs/<name>/curriculum.jsonl (sibling of
        # checkpoints/). When the root is itself the run dir (tests), put the
        # ledger inside root.
        self._ledger_path = self._resolve_ledger_path()

    def _resolve_ledger_path(self) -> Path:
        # Prefer sibling of a directory named "checkpoints".
        if self._root.name == "checkpoints":
            return self._root.parent / "curriculum.jsonl"
        return self._root / "curriculum.jsonl"

    # ------------------------------------------------------------------
    # Dual-trigger cadence (CTRL-02)
    # ------------------------------------------------------------------

    @property
    def last_written_time(self) -> float:
        """Monotonic timestamp of the last successful checkpoint write."""
        return self._last_written_time

    @property
    def last_written_step(self) -> int:
        return self._last_written_step

    def should_checkpoint(self, step: int, elapsed: float) -> bool:
        """Return True at most once per step when step or wall-clock fires.

        ``elapsed`` is time-since-LAST-checkpoint (``clock() - last_written_time``),
        not time-since-run-start. After a write both ``last_written_step`` and
        ``last_written_time`` advance so the next step does not re-fire from the
        clock alone (cycle-2 HIGH 3).
        """
        step = int(step)
        if step == self._last_written_step:
            return False
        step_fire = (
            self._every_n_steps > 0 and step > 0 and step % self._every_n_steps == 0
        )
        clock_fire = float(elapsed) >= self._wall_clock_ceiling_s
        return bool(step_fire or clock_fire)

    def _mark_written(self, step: Optional[int] = None) -> None:
        if step is not None:
            self._last_written_step = int(step)
        self._last_written_time = float(self._clock())

    # ------------------------------------------------------------------
    # Protocol surface (CTX-43)
    # ------------------------------------------------------------------

    def save(self, state: Any) -> str:
        """Persist ``state`` and refresh ``latest.pt`` (Protocol contract)."""
        cid = f"ckpt-{int(self._clock() * 1e6)}"
        path = self._root / f"{cid}.pt"
        atomic_write_torch(path, state)
        atomic_write_torch(self._root / "latest.pt", state)
        self._ids.append(cid)
        self._mark_written()
        return cid

    def load_latest(self) -> Any:
        """Load ``latest.pt`` under weights_only; fall through to fallback_scan."""
        import torch

        latest = self._root / "latest.pt"
        if latest.is_file():
            try:
                return torch.load(latest, weights_only=True)
            except Exception:
                pass  # corrupt / unreadable → fallback
        # Empty directory (no candidates) → EmptyCheckpointStore for Protocol
        # compatibility with phase-40; fallback_scan raises NoValid when files
        # exist but none are structurally valid.
        candidates = self._fallback_candidates()
        if not candidates and not latest.is_file():
            raise EmptyCheckpointStore(
                "load_latest on empty CheckpointStore (no successful save yet)"
            )
        return self.fallback_scan()

    def rollback(self) -> Any:
        """RECOVER target — same resolution as load_latest."""
        return self.load_latest()

    # ------------------------------------------------------------------
    # Save-class surface (cycle-4 MEDIUM-4)
    # ------------------------------------------------------------------

    def save_rolling(self, payload: Any, step: int) -> str:
        """Write ``step-{step:06d}.pt``, refresh latest.pt, run rolling retention."""
        step = int(step)
        name = f"step-{step:06d}.pt"
        path = self._root / name
        atomic_write_torch(path, payload)
        atomic_write_torch(self._root / "latest.pt", payload)
        self._mark_written(step=step)
        self._evict_rolling()
        return name

    def save_best(self, payload: Any) -> str:
        """Write/overwrite ``best.pt``; does NOT refresh latest.pt."""
        path = self._root / "best.pt"
        atomic_write_torch(path, payload)
        self._mark_written()
        return "best.pt"

    def save_anchor(
        self, tag: str, stage: int, payload: Any
    ) -> Optional[str]:
        """Write a stage or failure anchor; idempotent on existing filename.

        * ``stage-{k}-init.pt`` refreshes ``latest.pt`` (forward resume point).
        * ``failure-*`` never refreshes ``latest.pt`` and is bounded by
          ``failure_keep`` (LOW-2).
        """
        filename = self._anchor_filename(tag, stage)
        path = self._root / filename
        if path.is_file():
            return None  # idempotent no-op
        atomic_write_torch(path, payload)
        if _INIT_ANCHOR_RE.match(filename):
            atomic_write_torch(self._root / "latest.pt", payload)
        if filename.startswith("failure-"):
            self._evict_failure()
        # Anchors count as successful writes for cadence bookkeeping.
        step_hint = _parse_failure_step(filename)
        self._mark_written(step=step_hint)
        return filename

    def _anchor_filename(self, tag: str, stage: int) -> str:
        stem = str(tag).removesuffix(".pt")
        if stem in ("final", "init"):
            return f"stage-{int(stage)}-{stem}.pt"
        return f"{stem}.pt"

    # ------------------------------------------------------------------
    # Fallback scan + exact-path load (CTRL-03 / CTRL-05)
    # ------------------------------------------------------------------

    def _fallback_candidates(self) -> list[Path]:
        """Enumerate step-* and stage-* candidates; EXCLUDE failure-* (LOW-2).

        Ordering: step-* files by step index (desc); stage anchors by mtime
        (desc) after all step files of equal rank. Practically, higher step
        index is preferred; among pure stage anchors, newest mtime wins.
        """
        if not self._root.is_dir():
            return []
        # sort key: (kind_rank, primary, mtime) — higher is newer.
        # kind_rank 1 = step-* (primary = step index); kind_rank 0 = stage-*.
        candidates: list[tuple[tuple[int, int, float], Path]] = []
        for path in self._root.iterdir():
            if not path.is_file() or path.suffix != ".pt":
                continue
            name = path.name
            if name.startswith("failure-"):
                continue  # LOW-2: never auto-resume from a failure state
            if name in ("latest.pt", "best.pt"):
                continue
            mtime = path.stat().st_mtime
            step_idx = _parse_step_index(name)
            if step_idx is not None:
                candidates.append(((1, step_idx, mtime), path))
                continue
            if _STAGE_ANCHOR_RE.match(name):
                candidates.append(((0, 0, mtime), path))
                continue
        candidates.sort(key=lambda item: item[0], reverse=True)
        return [p for _, p in candidates]

    def fallback_scan(self) -> Any:
        """Newest structurally-valid step-*/stage-* checkpoint, or raise."""
        import torch

        for path in self._fallback_candidates():
            try:
                payload = torch.load(path, weights_only=True)
            except Exception:
                continue
            if _is_structurally_valid(payload):
                return payload
        raise NoValidCheckpointError(self._root)

    def load_checkpoint(self, path: PathLike) -> Any:
        """Exact-path load for ``--resume <specific-file>`` (cycle-3 HIGH).

        Validates path containment inside the store root, schema_version, and
        CTX-53 required keys. Never consults latest.pt.
        """
        import torch

        supplied = _as_path(path)
        try:
            resolved = supplied.resolve()
            root_resolved = self._root.resolve()
        except OSError as exc:
            raise NoValidCheckpointError(path) from exc

        # Path/run-root containment (reject traversal / external absolutes).
        try:
            if not resolved.is_relative_to(root_resolved):
                raise NoValidCheckpointError(path)
        except AttributeError:
            # Py < 3.9 fallback (not expected in pinn-train, but safe)
            try:
                resolved.relative_to(root_resolved)
            except ValueError as exc:
                raise NoValidCheckpointError(path) from exc

        if not resolved.is_file():
            raise NoValidCheckpointError(path)

        try:
            payload = torch.load(resolved, weights_only=True)
        except Exception as exc:
            raise NoValidCheckpointError(path) from exc

        if not _is_structurally_valid(payload):
            raise NoValidCheckpointError(path)
        return payload

    # ------------------------------------------------------------------
    # Retention (CTRL-02 / LOW-2)
    # ------------------------------------------------------------------

    def _evict_rolling(self) -> None:
        """Keep newest ``rolling_keep`` step-*.pt; never touch best/latest/anchors."""
        rollings: list[tuple[int, Path]] = []
        for path in self._root.glob("step-*.pt"):
            idx = _parse_step_index(path.name)
            if idx is not None:
                rollings.append((idx, path))
        if len(rollings) <= self._rolling_keep:
            return
        rollings.sort(key=lambda item: item[0])  # oldest first
        to_evict = rollings[: len(rollings) - self._rolling_keep]
        for _, path in to_evict:
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def _evict_failure(self) -> None:
        """Keep newest ``failure_keep`` failure-* anchors by step."""
        fails: list[tuple[int, Path]] = []
        for path in self._root.glob("failure-*.pt"):
            idx = _parse_failure_step(path.name)
            if idx is not None:
                fails.append((idx, path))
        if len(fails) <= self._failure_keep:
            return
        fails.sort(key=lambda item: item[0])
        to_evict = fails[: len(fails) - self._failure_keep]
        for _, path in to_evict:
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    # ------------------------------------------------------------------
    # Promotion + disposition ledger (CTRL-04 store half)
    # ------------------------------------------------------------------

    def promote(self, from_stage: int, to_stage: int) -> bool:
        """Accept only ordered k→k+1 within the slice; refuse otherwise."""
        from_stage = int(from_stage)
        to_stage = int(to_stage)
        if to_stage != from_stage + 1:
            if to_stage <= from_stage:
                raise PromotionRefused(
                    from_stage, to_stage, "regress or equal (require k→k+1)"
                )
            raise PromotionRefused(
                from_stage, to_stage, "skip (require k→k+1)"
            )
        if to_stage > self._terminal_stage:
            raise PromotionRefused(
                from_stage,
                to_stage,
                f"beyond terminal stage {self._terminal_stage}",
            )
        return True

    def record_disposition(
        self,
        from_stage: int,
        to_stage: int,
        disposition: Any,
        step: int,
    ) -> bool:
        """Idempotent curriculum.jsonl append keyed by the 4-tuple.

        Returns True if a new line was appended, False on idempotent replay.
        """
        from_stage = int(from_stage)
        to_stage = int(to_stage)
        step = int(step)
        disp = _disposition_str(disposition)
        key = (from_stage, to_stage, disp, step)

        existing = self._read_ledger_keys()
        if key in existing:
            return False

        record = {
            "disposition": disp,
            "from_stage": from_stage,
            "step": step,
            "to_stage": to_stage,
        }
        line = json.dumps(record, sort_keys=True) + "\n"
        self._ledger_path.parent.mkdir(parents=True, exist_ok=True)
        # Single write()+flush()+fsync append (RESEARCH Pattern 3).
        with open(self._ledger_path, "a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())
        return True

    def _read_ledger_keys(self) -> set[tuple[int, int, str, int]]:
        keys: set[tuple[int, int, str, int]] = set()
        if not self._ledger_path.is_file():
            return keys
        try:
            text = self._ledger_path.read_text(encoding="utf-8")
        except OSError:
            return keys
        for raw in text.splitlines():
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            try:
                keys.add(
                    (
                        int(row["from_stage"]),
                        int(row["to_stage"]),
                        str(row["disposition"]),
                        int(row["step"]),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue
        return keys
