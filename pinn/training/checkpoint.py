"""Phase 40 / CTX-43-44 — CheckpointStore seam + naive torch.save impl.

Protocol surface for CurriculumController RECOVER (CTX-41):
    save(state) -> id
    load_latest() -> state
    rollback() -> last well-formed state

The naive ``TorchSaveCheckpointStore`` is deliberately minimal — Phase 41
swaps atomic/retention/promotion behind the same Protocol (CTRL-02..04).
Every load/rollback passes ``weights_only=True`` NOW (T-40-02 closed at
the load boundary, not deferred). Empty-store load/rollback raise
``EmptyCheckpointStore``.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


class EmptyCheckpointStore(RuntimeError):
    """Raised when load_latest/rollback is called with no successful save yet."""


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


class TorchSaveCheckpointStore:
    """Naive directory-of-files checkpoint store.

    Payloads MUST be plain tensors/containers/python scalars (CTX-44) so
    ``torch.load(..., weights_only=True)`` succeeds. No callables / custom
    classes.
    """

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)
        self._index_path = self._root / "index.json"
        self._ids: list[str] = []
        if self._index_path.is_file():
            raw = json.loads(self._index_path.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                self._ids = [str(x) for x in raw]

    def save(self, state: Any) -> str:
        import torch

        cid = f"ckpt-{int(time.time() * 1e6)}-{len(self._ids)}"
        path = self._root / f"{cid}.pt"
        torch.save(state, path)
        self._ids.append(cid)
        self._persist_index()
        return cid

    def load_latest(self) -> Any:
        import torch

        if not self._ids:
            raise EmptyCheckpointStore(
                "load_latest on empty CheckpointStore (no successful save yet)"
            )
        path = self._root / f"{self._ids[-1]}.pt"
        return torch.load(path, weights_only=True)

    def rollback(self) -> Any:
        import torch

        if not self._ids:
            raise EmptyCheckpointStore(
                "rollback on empty CheckpointStore (no successful save yet)"
            )
        path = self._root / f"{self._ids[-1]}.pt"
        return torch.load(path, weights_only=True)

    def _persist_index(self) -> None:
        self._index_path.write_text(
            json.dumps(self._ids), encoding="utf-8"
        )
