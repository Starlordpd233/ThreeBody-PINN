"""Shared atomic write primitive (tmp + fsync + os.replace + dir fsync).

Promotes the verified three-site idiom from ``stage_scan.py`` / ``splits.py`` /
``gradcheck_probe.py`` into one module so config_yaml, checkpoint, and guards
import a single implementation rather than a fourth divergent copy.

Ordering (do not invent a new sequence):
    path.tmp.{pid} → write → flush → os.fsync(file) → os.replace → open dir
    → os.fsync(dir) → close, with a finally-unlink of the temp path.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Union

PathLike = Union[str, Path]


def _as_path(path: PathLike) -> Path:
    return path if isinstance(path, Path) else Path(path)


def _atomic_replace(temporary: Path, path: Path) -> None:
    """fsync-file is the caller's responsibility before this is invoked.

    Performs ``os.replace`` then directory ``os.fsync`` so the rename is
    durable on crash. Callers that write the temp file must flush+fsync it
    first (text path) or rely on ``torch.save``'s close semantics (torch path
    re-opens and fsyncs after save).
    """
    os.replace(temporary, path)
    directory_fd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def atomic_write_text(path: PathLike, content: str) -> Path:
    """Atomically write UTF-8 text to ``path``.

    Verified idiom (stage_scan ``_atomic_write``): write to
    ``path.tmp.{pid}``, flush + ``os.fsync`` the file, ``os.replace`` onto the
    canonical name, then ``os.fsync`` the parent directory. A ``finally``
    unlinks any leftover temp so a failed replace cannot leave a partial
    artifact under the canonical name.
    """
    destination = _as_path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + f".tmp.{os.getpid()}")
    try:
        with open(temporary, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        _atomic_replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination


def atomic_write_torch(path: PathLike, payload: Any) -> Path:
    """Atomically write a ``torch.save`` payload to ``path``.

    Same fsync → os.replace → dir-fsync ordering as ``atomic_write_text``,
    with ``torch.save(payload, tmp)`` substituted for the text write.
    ``torch`` is imported lazily so a torch-less import of this module still
    works (mirrors ``checkpoint.py`` deferred-import convention).
    """
    import torch  # deferred: keep module import torch-free

    destination = _as_path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + f".tmp.{os.getpid()}")
    try:
        torch.save(payload, temporary)
        # Re-open and fsync so the binary bytes are durable before rename
        # (torch.save does not guarantee fsync of the underlying fd).
        with open(temporary, "rb") as handle:
            os.fsync(handle.fileno())
        _atomic_replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination
