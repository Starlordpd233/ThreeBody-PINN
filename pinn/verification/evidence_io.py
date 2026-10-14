"""Phase 59: the shared evidence writer for Phase-59 tools.

Canonical JSON, redaction, the freeze guard, completion markers, and the
one-launch lock. Producing tools call ``require_frozen_scorecard`` before any
corpus or checkpoint read. This module does not score trajectories and does
not probe a device.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

import numpy as np

from pinn.data.adapter import EvidenceRedactionError
from pinn.data.types import PhysicalKey, RecordKey
from pinn.training.atomic_io import atomic_write_text
from pinn.training.validation_gate import json_safe_float
from pinn.verify import git_head

EVIDENCE_ROOT_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence")
LAUNCH_LOCK_REL = EVIDENCE_ROOT_REL / "logs" / "launch.lock.log"
LAUNCH_FAILURES_REL = EVIDENCE_ROOT_REL / "logs" / "launch-failures.log"
RUNTIME_BUDGET_SECONDS = 600.0
_PHASE_REL = Path(".planning/phases/59-read-only-baseline-scorecard")
_DECISION_MODES = {
    f"{_PHASE_REL.as_posix()}/59-CONTEXT.md": "unchanged",
    f"{_PHASE_REL.as_posix()}/59-GAPS.md": "ancestor_state",
    f"{_PHASE_REL.as_posix()}/59-RESEARCH.md": "unchanged",
    f"{_PHASE_REL.as_posix()}/59-VALIDATION.md": "ancestor_state",
}

__all__ = [
    "EVIDENCE_ROOT_REL",
    "LAUNCH_LOCK_REL",
    "LAUNCH_FAILURES_REL",
    "RUNTIME_BUDGET_SECONDS",
    "FreezeNotEstablished",
    "MemoryPreflightError",
    "LaunchRefused",
    "json_safe",
    "record_key_str",
    "canonical_json_bytes",
    "guard_redaction",
    "reject_evidence_root",
    "write_json",
    "write_text",
    "area_manifest",
    "write_area_manifest",
    "files_opened_record",
    "provenance_record",
    "redacted_command",
    "ru_maxrss_bytes",
    "bytes_identical",
    "require_frozen_scorecard",
    "module_hashes",
    "available_memory_bytes",
    "memory_preflight",
    "write_completion_marker",
    "completion_marker_ok",
    "begin_long_step",
    "end_long_step",
    "record_long_step_failure",
    "runtime_gate",
]


class FreezeNotEstablished(RuntimeError):
    """The frozen scorecard is missing, dirty, or no longer the ancestor of HEAD."""


class MemoryPreflightError(RuntimeError):
    """vm_stat reports less free memory than the long step requires."""


class LaunchRefused(RuntimeError):
    """Another Phase-59 long step holds the launch lock."""


def _repo_root(repo_root: Optional[Path] = None) -> Path:
    if repo_root is not None:
        return Path(repo_root).resolve()
    return Path(__file__).resolve().parents[2]


def _under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def record_key_str(key: Any) -> str:
    """Render a record or physical key as ``variant/fidelity/id`` or ``variant/id``."""
    if isinstance(key, RecordKey):
        return f"{key.variant}/{key.fidelity}/{key.id}"
    if isinstance(key, PhysicalKey):
        return f"{key.variant}/{key.id}"
    raise TypeError(f"expected RecordKey or PhysicalKey, got {type(key).__name__}")


def json_safe(value: Any) -> Any:
    """Recursively replace non-finite floats, numpy values, and identity keys."""
    if isinstance(value, (RecordKey, PhysicalKey)):
        return record_key_str(value)
    if isinstance(value, np.ndarray):
        return json_safe(value.tolist())
    if isinstance(value, np.generic):
        return json_safe(value.item())
    if isinstance(value, float):
        return json_safe_float(value)
    if isinstance(value, Mapping):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def canonical_json_bytes(payload: Any) -> bytes:
    """Sorted, indented JSON with non-finite floats as string sentinels."""
    text = json.dumps(
        json_safe(payload),
        sort_keys=True,
        indent=2,
        ensure_ascii=True,
        allow_nan=False,
    )
    return (text + "\n").encode("ascii")


def guard_redaction(data: Any, *, data_root: Optional[Path] = None) -> None:
    """Refuse text that still contains the home directory or the resolved data root."""
    if isinstance(data, bytes):
        text = data.decode("utf-8", errors="replace")
    else:
        text = str(data)
    home = str(Path.home())
    if home and home in text:
        raise EvidenceRedactionError("evidence contains the host home prefix")
    if data_root is not None:
        root = str(Path(data_root).resolve())
        if root and root in text:
            raise EvidenceRedactionError("evidence contains the resolved data root")


def reject_evidence_root(path: Path, *, data_root: Optional[Path] = None, repo_root: Optional[Path] = None) -> None:
    """Refuse a target inside the corpus tree or the main checkout's simulation_data."""
    resolved = Path(path).resolve()
    dataset = (_repo_root(repo_root) / "simulation_data").resolve()
    if _under(resolved, dataset):
        raise ValueError("evidence path must not be inside simulation_data")
    if data_root is None:
        return
    corpus = Path(data_root).resolve()
    if _under(resolved, corpus):
        raise ValueError("evidence path must not be inside the data root")
    main_simulation = corpus.parent
    if main_simulation.name == "simulation_data" and _under(resolved, main_simulation):
        raise ValueError("evidence path must not be inside the main checkout simulation_data")


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_text(path: Path, text: str, *, data_root: Optional[Path] = None) -> str:
    """Atomically write redacted text and return the SHA-256 of the bytes."""
    reject_evidence_root(path, data_root=data_root)
    guard_redaction(text, data_root=data_root)
    raw = text.encode("utf-8")
    atomic_write_text(path, text)
    return _sha256_bytes(raw)


def write_json(path: Path, payload: Any, *, data_root: Optional[Path] = None) -> str:
    """Atomically write canonical JSON and return the SHA-256 of the bytes."""
    reject_evidence_root(path, data_root=data_root)
    raw = canonical_json_bytes(payload)
    guard_redaction(raw, data_root=data_root)
    atomic_write_text(path, raw.decode("ascii"))
    return _sha256_bytes(raw)


def _skipped_area_part(parts: tuple[str, ...], name: str) -> bool:
    return name == "MANIFEST.json" or "__pycache__" in parts or "logs" in parts


def area_manifest(area_dir: Path) -> dict[str, Any]:
    """Hash every regular file in an area except the manifest, logs, and caches."""
    area = Path(area_dir)
    files: dict[str, dict[str, Any]] = {}
    if area.is_dir():
        for path in sorted(area.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(area)
            if _skipped_area_part(relative.parts, relative.as_posix()):
                continue
            raw = path.read_bytes()
            files[relative.as_posix()] = {
                "sha256": _sha256_bytes(raw),
                "size_bytes": len(raw),
            }
    return {
        "schema": "phase59-area-manifest/v1",
        "area": area.name,
        "files": files,
    }


def write_area_manifest(area_dir: Path) -> dict[str, Any]:
    """Write ``MANIFEST.json`` for ``area_dir`` and return the manifest."""
    manifest = area_manifest(area_dir)
    write_json(Path(area_dir) / "MANIFEST.json", manifest)
    return manifest


def files_opened_record(tool: str, attestation_summary: Mapping[str, Any]) -> dict[str, Any]:
    """Attach the tool name to an attestation summary."""
    record = dict(attestation_summary)
    record["schema"] = "phase59-files-opened/v1"
    record["tool"] = tool
    return record


def redacted_command(argv: Sequence[Any], *, data_root: Optional[Path] = None) -> str:
    """Join an argv and replace the data root and home prefix."""
    rendered = " ".join(str(part) for part in argv)
    if data_root is not None:
        given = str(data_root)
        resolved = str(Path(data_root).resolve())
        rendered = rendered.replace(given, "<DATA_ROOT>").replace(resolved, "<DATA_ROOT>")
    home = str(Path.home())
    if home:
        rendered = rendered.replace(home, "~")
    return rendered


def ru_maxrss_bytes() -> int:
    """Peak resident set of this process, in bytes (darwin reports bytes already)."""
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform == "darwin":
        return value
    return value * 1024


def _worktree_dirty(repo_root: Path) -> bool:
    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    return bool(proc.stdout.strip())


def provenance_record(
    tool: str,
    argv: Sequence[Any],
    *,
    data_root: Optional[Path],
    data_root_source: str,
    utc_started: str,
    monotonic_started: float,
) -> dict[str, Any]:
    """Build the provenance record for one producing invocation."""
    import numpy
    import torch

    sha, available = git_head()
    return {
        "schema": "phase59-provenance/v1",
        "tool": tool,
        "command": redacted_command(argv, data_root=data_root),
        "git_head": sha if available else None,
        "worktree_dirty": _worktree_dirty(_repo_root()),
        "python": platform.python_version(),
        "numpy": numpy.__version__,
        "torch": torch.__version__,
        "utc_started": utc_started,
        "utc_finished": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - float(monotonic_started),
        "ru_maxrss_bytes": ru_maxrss_bytes(),
        "data_root_source": data_root_source,
    }


def bytes_identical(path: Path, new_bytes: bytes) -> bool:
    """True when ``path`` already holds ``new_bytes``."""
    file = Path(path)
    if isinstance(new_bytes, str):
        raw = new_bytes.encode("utf-8")
    else:
        raw = new_bytes
    return file.is_file() and file.read_bytes() == raw


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )


def is_ancestor(ancestor: str, descendant: str, repo: Path) -> bool:
    """True when ``ancestor`` is an ancestor of ``descendant``, including equality."""
    proc = _git(repo, "merge-base", "--is-ancestor", ancestor, descendant)
    return proc.returncode == 0


def _is_tracked(repo: Path, relative: str) -> bool:
    return _git(repo, "ls-files", "--error-unmatch", "--", relative).returncode == 0


def _is_clean(repo: Path, relative: str) -> bool:
    return _git(repo, "status", "--porcelain", "--", relative).stdout.strip() == ""


def _first_commit(repo: Path, relative: str) -> str:
    proc = _git(repo, "log", "--diff-filter=A", "--format=%H", "--", relative)
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if proc.returncode != 0 or not lines:
        raise FreezeNotEstablished(f"no add commit for {relative}")
    return lines[-1]


def _rev_parse(repo: Path, spec: str) -> str:
    proc = _git(repo, "rev-parse", spec)
    if proc.returncode != 0 or not proc.stdout.strip():
        raise FreezeNotEstablished(f"git rev-parse failed for {spec}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def _show_bytes(repo: Path, spec: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", spec],
        cwd=str(repo),
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise FreezeNotEstablished(f"git show failed for {spec}")
    return proc.stdout


def _frozen_rels(record: Mapping[str, Any]) -> list[str]:
    return [
        str(record["scorecard_path"]),
        str(record["scorecard_module_path"]),
        str(record["plain_doc_path"]),
        (EVIDENCE_ROOT_REL / "scorecard-freeze.json").as_posix(),
    ]


def _assert_recorded_hashes(repo: Path, record: Mapping[str, Any]) -> None:
    from pinn.verification.feasibility_scorecard import SCORECARD_SHA256, load_scorecard

    scorecard = (repo / str(record["scorecard_path"])).read_bytes()
    digest = _sha256_bytes(scorecard)
    expected = str(record["scorecard_sha256"])
    if digest != expected or digest != SCORECARD_SHA256:
        raise FreezeNotEstablished(
            f"scorecard sha256 {digest} != record {expected} or {SCORECARD_SHA256}"
        )
    module_digest = _sha256_bytes((repo / str(record["scorecard_module_path"])).read_bytes())
    if module_digest != str(record["scorecard_module_sha256"]):
        raise FreezeNotEstablished(
            f"rule module sha256 {module_digest} != {record['scorecard_module_sha256']}"
        )
    plain_digest = _sha256_bytes((repo / str(record["plain_doc_path"])).read_bytes())
    if plain_digest != str(record["plain_doc_sha256"]):
        raise FreezeNotEstablished(
            f"plain document sha256 {plain_digest} != {record['plain_doc_sha256']}"
        )
    load_scorecard()


def _assert_decision_sources(repo: Path, record: Mapping[str, Any], freeze_commit: str) -> None:
    pins = record.get("decision_sources")
    if not isinstance(pins, Mapping) or set(pins) != set(_DECISION_MODES):
        raise FreezeNotEstablished("decision_sources must pin exactly the four decision files")
    for relative, mode in _DECISION_MODES.items():
        pin = pins[relative]
        if not isinstance(pin, Mapping) or pin.get("verify") != mode:
            raise FreezeNotEstablished(f"{relative} verify mode is not {mode}")
        blob = _rev_parse(repo, f"{freeze_commit}:{relative}")
        if blob != pin.get("git_blob"):
            raise FreezeNotEstablished(
                f"{relative} git_blob {blob} != {pin.get('git_blob')}"
            )
        digest = _sha256_bytes(_show_bytes(repo, f"{freeze_commit}:{relative}"))
        if digest != pin.get("sha256"):
            raise FreezeNotEstablished(f"{relative} sha256 {digest} != {pin.get('sha256')}")
        last = _git(repo, "log", "-1", "--format=%H", freeze_commit, "--", relative).stdout.strip()
        if last != pin.get("last_commit"):
            raise FreezeNotEstablished(
                f"{relative} last_commit {last} != {pin.get('last_commit')}"
            )
        if not is_ancestor(str(pin["last_commit"]), freeze_commit, repo):
            raise FreezeNotEstablished(
                f"{relative} last_commit is not an ancestor of the freeze commit"
            )
        if mode != "unchanged":
            continue
        if not _is_tracked(repo, relative) or not _is_clean(repo, relative):
            raise FreezeNotEstablished(f"{relative} is dirty")
        current = _sha256_bytes((repo / relative).read_bytes())
        if current != pin.get("sha256"):
            raise FreezeNotEstablished(f"{relative} changed after the freeze commit")


def require_frozen_scorecard(repo_root: Optional[Path] = None) -> dict[str, str]:
    """Return the freeze commit and HEAD, or raise when the freeze does not hold."""
    repo = _repo_root(repo_root)
    freeze_path = repo / EVIDENCE_ROOT_REL / "scorecard-freeze.json"
    if not freeze_path.is_file():
        raise FreezeNotEstablished("freeze record is absent")
    record = json.loads(freeze_path.read_text(encoding="utf-8"))
    rels = _frozen_rels(record)
    for relative in rels:
        if not _is_tracked(repo, relative) or not _is_clean(repo, relative):
            raise FreezeNotEstablished(f"frozen file is dirty or untracked: {relative}")
    _assert_recorded_hashes(repo, record)
    freeze_rel = (EVIDENCE_ROOT_REL / "scorecard-freeze.json").as_posix()
    freeze_commit = _first_commit(repo, freeze_rel)
    diff = _git(repo, "diff", "--quiet", freeze_commit, "HEAD", "--", *rels)
    if diff.returncode != 0:
        raise FreezeNotEstablished(
            f"frozen files differ from the freeze commit {freeze_commit}"
        )
    _assert_decision_sources(repo, record, freeze_commit)
    head = _rev_parse(repo, "HEAD")
    if not is_ancestor(freeze_commit, head, repo):
        raise FreezeNotEstablished(
            f"freeze commit {freeze_commit} is not an ancestor of HEAD {head}"
        )
    return {"freeze_commit": freeze_commit, "head": head}


def module_hashes(paths: Sequence[str], *, repo_root: Optional[Path] = None) -> dict[str, str]:
    """SHA-256 of each repo-relative module or script, for ``producer_sha256``."""
    repo = _repo_root(repo_root)
    return {str(relative): _sha256_bytes((repo / relative).read_bytes()) for relative in paths}


def _parse_vm_stat(sample: str) -> int:
    import re

    page = re.search(r"page size of (\d+) bytes", sample)
    if page is None:
        raise MemoryPreflightError("vm_stat sample has no page size")
    total = 0
    for label in ("free", "inactive", "speculative"):
        match = re.search(rf"^Pages {label}:\s+(\d+)\.", sample, re.M)
        if match is None:
            raise MemoryPreflightError(f"vm_stat sample has no Pages {label}")
        total += int(match.group(1))
    return total * int(page.group(1))


def available_memory_bytes(sample: Optional[str] = None) -> int:
    """Bytes of free + inactive + speculative pages from ``vm_stat``."""
    if sample is None:
        proc = subprocess.run(["vm_stat"], capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise MemoryPreflightError(proc.stderr.strip() or "vm_stat failed")
        sample = proc.stdout
    return _parse_vm_stat(sample)


def memory_preflight(required_bytes: int, *, sample: Optional[str] = None) -> dict[str, Any]:
    """Return the vm_stat preflight, or raise when available memory is short."""
    available = available_memory_bytes(sample)
    if available < int(required_bytes):
        raise MemoryPreflightError(
            f"available {available} bytes < required {int(required_bytes)} bytes"
        )
    return {
        "available_bytes": available,
        "required_bytes": int(required_bytes),
        "source": "vm_stat",
    }


def _result_name(area: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(area.resolve()).as_posix()
    except ValueError:
        return path.name


def write_completion_marker(
    area_dir: Path,
    step: str,
    *,
    command: Any,
    utc_started: str,
    utc_finished: str,
    elapsed_seconds: float,
    result_paths: Sequence[Path],
    preflight: Mapping[str, Any],
) -> dict[str, Any]:
    """Write ``{step}.done.json`` as the last action of a long step."""
    area = Path(area_dir)
    if isinstance(command, str):
        rendered = command
    else:
        rendered = redacted_command(command)
    payload = {
        "schema": "phase59-completion-marker/v1",
        "step": step,
        "command": rendered,
        "status": "complete",
        "utc_started": utc_started,
        "utc_finished": utc_finished,
        "elapsed_seconds": elapsed_seconds,
        "ru_maxrss_bytes": ru_maxrss_bytes(),
        "preflight": dict(preflight),
        "result_files": {
            _result_name(area, Path(path)): _sha256_bytes(Path(path).read_bytes())
            for path in result_paths
        },
    }
    write_json(area / f"{step}.done.json", payload)
    return payload


def completion_marker_ok(area_dir: Path, step: str) -> bool:
    """True when the marker exists, is complete, and its result hashes still match."""
    path = Path(area_dir) / f"{step}.done.json"
    if not path.is_file():
        return False
    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if marker.get("schema") != "phase59-completion-marker/v1" or marker.get("status") != "complete":
        return False
    files = marker.get("result_files")
    if not isinstance(files, dict):
        return False
    area = Path(area_dir)
    for name, digest in files.items():
        target = area / name
        if not target.is_file() or _sha256_bytes(target.read_bytes()) != digest:
            return False
    return True


def _lock_path(evidence_root: Optional[Path]) -> Path:
    if evidence_root is None:
        return _repo_root() / LAUNCH_LOCK_REL
    return Path(evidence_root) / "logs" / "launch.lock.log"


def _failures_path(evidence_root: Optional[Path]) -> Path:
    if evidence_root is None:
        return _repo_root() / LAUNCH_FAILURES_REL
    return Path(evidence_root) / "logs" / "launch-failures.log"


def _read_lock(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LaunchRefused(f"launch lock is unreadable: {exc}") from exc
    if not isinstance(payload, dict):
        raise LaunchRefused("launch lock is not a JSON object")
    return payload


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _refused_message(holder: Mapping[str, Any]) -> str:
    alive = _pid_alive(int(holder["pid"]))
    return (
        f"LAUNCH-REFUSED: {holder['area']}/{holder['step']} "
        f"run {holder['run_id']} pid {holder['pid']} alive {str(alive).lower()} "
        f"started {holder['utc_started']}"
    )


def begin_long_step(area: str, step: str, *, command: Sequence[Any], evidence_root: Optional[Path] = None) -> str:
    """Take the single launch lock by exclusive create and return the run id."""
    path = _lock_path(evidence_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex
    payload = {
        "schema": "phase59-launch-lock/v1",
        "area": area,
        "step": step,
        "run_id": run_id,
        "pid": os.getpid(),
        "command": command if isinstance(command, str) else redacted_command(command),
        "utc_started": datetime.now(timezone.utc).isoformat(),
    }
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        raise LaunchRefused(_refused_message(_read_lock(path))) from None
    try:
        os.write(fd, raw)
    finally:
        os.close(fd)
    return run_id


def end_long_step(run_id: str, *, evidence_root: Optional[Path] = None) -> None:
    """Release the launch lock when ``run_id`` is the holder."""
    path = _lock_path(evidence_root)
    holder = _read_lock(path)
    if holder.get("run_id") != run_id:
        raise LaunchRefused(
            f"launch lock run {holder.get('run_id')} does not match {run_id}"
        )
    path.unlink()


def record_long_step_failure(
    reason: str,
    *,
    run_id: Optional[str] = None,
    evidence_root: Optional[Path] = None,
) -> None:
    """Append a failure line and release the lock.

    Without ``run_id`` this is stale-lock recovery and refuses while the
    holder's pid is still alive.
    """
    path = _lock_path(evidence_root)
    holder = _read_lock(path)
    if run_id is not None:
        if holder.get("run_id") != run_id:
            raise LaunchRefused(
                f"launch lock run {holder.get('run_id')} does not match {run_id}"
            )
    elif _pid_alive(int(holder["pid"])):
        raise LaunchRefused(_refused_message(holder))
    line = {
        "schema": "phase59-launch-failure/v1",
        "area": holder["area"],
        "step": holder["step"],
        "run_id": holder["run_id"],
        "pid": holder["pid"],
        "reason": reason,
        "utc": datetime.now(timezone.utc).isoformat(),
    }
    failure = _failures_path(evidence_root)
    failure.parent.mkdir(parents=True, exist_ok=True)
    with failure.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line, sort_keys=True) + "\n")
    path.unlink()


def runtime_gate(
    elapsed_seconds: float,
    *,
    label: str,
    budget_seconds: float = RUNTIME_BUDGET_SECONDS,
) -> int:
    """Print the wall-clock line. Return 5 when ``elapsed_seconds`` is over budget."""
    budget = float(budget_seconds)
    budget_text = str(int(budget)) if budget == int(budget) else str(budget)
    print(f"WALL-SECONDS {elapsed_seconds} budget {budget_text}", file=sys.stderr)
    if float(elapsed_seconds) > budget:
        print(
            f"{label}-RUNTIME-OVER-BUDGET: {elapsed_seconds} s > {budget_text} s",
            file=sys.stderr,
        )
        return 5
    return 0
