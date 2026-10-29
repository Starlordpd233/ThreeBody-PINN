"""Phase 65 (INST-08): intrinsic diagnostic-artifact identity and typed refusal.

Every INST-08 artifact — the JSON record and the tensor payload — carries its
diagnostic identity inside the payload itself (``artifact_kind: diagnostic``,
``diagnostic: true``, ``counted: false`` beside the ``inst08-*`` schema), never
in its filename or directory. ``require_not_diagnostic`` reads a file's content
and raises :class:`DiagnosticArtifactRefused` when that intrinsic marker is
present, so a renamed or relocated diagnostic artifact cannot cross into a
production reader even when production-looking keys are added around the
marker. Plan 65-03 wires this refusal into the production graded-run and
evaluator entry points; this module is the single typed refusal they share.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path

import torch

__all__ = [
    "DiagnosticArtifactRefused",
    "DiagnosticRegistrationRefused",
    "RECORD_SCHEMA",
    "WEIGHTS_SCHEMA",
    "REGISTRATION_SCHEMA",
    "ARTIFACT_KIND",
    "diagnostic_marker",
    "carries_diagnostic_marker",
    "require_not_diagnostic",
    "require_resume_not_diagnostic",
    "require_committed_registration",
    "read_diagnostic_record",
    "read_diagnostic_weights",
]

RECORD_SCHEMA = "inst08-diagnostic/v1"
WEIGHTS_SCHEMA = "inst08-diagnostic-weights/v1"
REGISTRATION_SCHEMA = "phase65-probe-registration/v1"
ARTIFACT_KIND = "diagnostic"


class DiagnosticRegistrationRefused(RuntimeError):
    """The registration is not a committed-clean, digest-exact artifact set.

    Raised before any data resolution, weight deserialization or attempt
    creation. The check is scoped to the registration's own enumerated
    artifacts: an unrelated dirty file elsewhere in the repository is never a
    refusal reason.
    """


class DiagnosticArtifactRefused(RuntimeError):
    """The file is an INST-08 diagnostic artifact and may not enter production.

    Exported as the one typed refusal the production entry points (Plan 65-03)
    raise before any graded-run or evaluator side effect.
    """


def diagnostic_marker(*, schema):
    """The intrinsic identity block every diagnostic payload carries.

    The payload's own schema names which artifact kind it is; the marker fields
    are checked by content, independent of filename or directory.
    """
    if schema not in (RECORD_SCHEMA, WEIGHTS_SCHEMA):
        raise ValueError(f"unknown diagnostic artifact schema: {schema!r}")
    return {
        "schema": schema,
        "artifact_kind": ARTIFACT_KIND,
        "diagnostic": True,
        "counted": False,
    }


def _carries_marker(payload) -> bool:
    if not isinstance(payload, Mapping):
        return False
    if payload.get("diagnostic") is True or payload.get("artifact_kind") == ARTIFACT_KIND:
        return True
    return any(
        _carries_marker(value) for value in payload.values() if isinstance(value, Mapping)
    )


def carries_diagnostic_marker(payload) -> bool:
    """Public predicate over an ALREADY-LOADED payload (no file I/O).

    The production checkpoint store's load routes and structural validator
    (Plan 65-03) call this on every payload they are about to return or accept,
    so the marker check has exactly one implementation.
    """
    return _carries_marker(payload)


def require_not_diagnostic(path):
    """Refuse the file when its content carries the intrinsic diagnostic marker.

    Returns ``None`` when the file is not a diagnostic artifact (for example a
    production state dict or a production checkpoint envelope). The check is
    content-based: a renamed or relocated artifact, or an envelope with all
    production-required keys added around the marker, is still refused.
    """
    raw = Path(path).read_bytes()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        payload = None
    if payload is not None:
        if _carries_marker(payload):
            raise DiagnosticArtifactRefused(
                f"{Path(path).name} carries the intrinsic diagnostic marker and may not "
                "enter a production reader"
            )
        return None
    loaded = torch.load(path, map_location="cpu", weights_only=True)
    if _carries_marker(loaded):
        raise DiagnosticArtifactRefused(
            f"{Path(path).name} carries the intrinsic diagnostic marker and may not "
            "enter a production reader"
        )
    return None


def require_resume_not_diagnostic(resume_arg, checkpoints_dir):
    """Early (pre-run) graded-resume admission — read-only content check.

    Plan 65-03 (D-09 / INST-08 d): ``train.main`` calls this BEFORE creating
    the run directory, so a diagnostic resume candidate can never reach run
    creation, data/model/optimizer setup or the graded training loop. The
    routing mirrors ``pinn.training.resume.load_resume_target`` exactly:

    * an explicit FILE argument is checked by content (``require_not_diagnostic``);
    * the literal ``latest``, a directory, or any other non-file argument is
      resolved against the run's OWN checkpoints directory exactly as
      ``store.load_latest()`` would (``latest.pt`` first, then the step/stage
      candidate ordering — never selection by scientific metric), and the
      payload that WOULD be selected is refused when it carries the marker. A
      marked newest candidate refuses instead of silently falling through to an
      older ordinary file.

    The check never constructs a checkpoint store (whose constructor creates
    its directory): an absent checkpoints directory stays absent, and a
    selection failure with no diagnostic content (no candidates, none
    structurally valid) is left to the real load route to report.
    """
    from pinn.training.checkpoint import (  # deferred: checkpoint imports this module
        DiagnosticCheckpointRefused,
        EmptyCheckpointStore,
        NoValidCheckpointError,
        peek_latest_selection,
    )

    arg = str(resume_arg)
    if arg != "latest":
        path = Path(arg)
        if path.is_file():
            require_not_diagnostic(path)
            return
        # A directory (or any non-file argument) routes to store.load_latest().
    try:
        peek_latest_selection(Path(checkpoints_dir))
    except DiagnosticCheckpointRefused as exc:
        raise DiagnosticArtifactRefused(f"--resume {arg}: {exc}") from exc
    except (NoValidCheckpointError, EmptyCheckpointStore):
        return  # not a diagnostic question; the load route reports it


def read_diagnostic_record(path):
    """Read and verify one diagnostic JSON record. Refuse anything else."""
    payload = json.loads(Path(path).read_bytes().decode("utf-8"))
    if not isinstance(payload, Mapping) or payload.get("schema") != RECORD_SCHEMA \
            or payload.get("diagnostic") is not True:
        raise DiagnosticArtifactRefused(
            f"{Path(path).name} is not a {RECORD_SCHEMA} diagnostic record"
        )
    return payload


def read_diagnostic_weights(path):
    """Read and verify one diagnostic tensor payload. Refuse anything else.

    The payload is saved so ``torch.load(..., weights_only=True)`` reads it;
    the returned mapping carries the intrinsic marker beside the ``state_dict``.
    """
    payload = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(payload, Mapping) or payload.get("schema") != WEIGHTS_SCHEMA \
            or payload.get("diagnostic") is not True \
            or not isinstance(payload.get("state_dict"), Mapping):
        raise DiagnosticArtifactRefused(
            f"{Path(path).name} is not a {WEIGHTS_SCHEMA} diagnostic weights payload"
        )
    return payload


# --------------------------------------------------------------------------
# Committed registration admission (Plan 65-04; shared with the fit harness)
# --------------------------------------------------------------------------


def _registration_repo(repo_root):
    """The repository the registration is checked against."""
    if repo_root is not None:
        return Path(repo_root).resolve()
    probe = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False
    )
    if probe.returncode == 0 and probe.stdout.strip():
        return Path(probe.stdout.strip()).resolve()
    return Path.cwd().resolve()


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _registration_entries(doc):
    """Every enumerated (repo-relative path, recorded SHA-256) in the registration.

    Weight entries are returned separately so the read-only check-registration
    mode can skip weight bytes entirely.
    """
    artifacts = []
    weights = []
    artifacts.append(_one_entry(doc.get("page"), "page"))
    source = doc.get("source")
    if not isinstance(source, Mapping):
        raise DiagnosticRegistrationRefused("the registration names no source block")
    for key in ("manifest", "stdout"):
        artifacts.append(_one_entry(source.get(key), f"source.{key}"))
    scripts = source.get("scripts")
    if not isinstance(scripts, list) or not scripts:
        raise DiagnosticRegistrationRefused("the registration names no source scripts")
    for index, entry in enumerate(scripts):
        artifacts.append(_one_entry(entry, f"source.scripts[{index}]"))
    dependencies = doc.get("code_dependencies")
    if not isinstance(dependencies, list) or not dependencies:
        raise DiagnosticRegistrationRefused("the registration names no code dependencies")
    for index, entry in enumerate(dependencies):
        artifacts.append(_one_entry(entry, f"code_dependencies[{index}]"))
    frozen = doc.get("frozen")
    if isinstance(frozen, list):
        for index, entry in enumerate(frozen):
            artifacts.append(_one_entry(entry, f"frozen[{index}]"))
    arms = doc.get("arms")
    if not isinstance(arms, list) or not arms:
        raise DiagnosticRegistrationRefused("the registration names no arms")
    for index, arm in enumerate(arms):
        if not isinstance(arm, Mapping):
            raise DiagnosticRegistrationRefused(f"arms[{index}] is not a mapping")
        artifacts.append(_one_entry(arm.get("record"), f"arms[{index}].record"))
        weights_map = arm.get("weights")
        if not isinstance(weights_map, Mapping) or not weights_map:
            raise DiagnosticRegistrationRefused(
                f"arms[{index}].weights names no committed weight files"
            )
        for state, entry in weights_map.items():
            weights.append((f"arms[{index}].weights.{state}", _one_entry(entry, "weights")))
    return artifacts, weights


def _one_entry(entry, what):
    if not isinstance(entry, Mapping) or not isinstance(entry.get("path"), str) \
            or not isinstance(entry.get("sha256"), str):
        raise DiagnosticRegistrationRefused(
            f"the registration's {what} entry must name a path and a sha256"
        )
    if entry["path"] in ("", ".", "..") or entry["path"].startswith("/") \
            or ".." in Path(entry["path"]).parts:
        raise DiagnosticRegistrationRefused(
            f"the registration's {what} path must be repo-relative: {entry['path']!r}"
        )
    return entry["path"], entry["sha256"]


def require_committed_registration(registration_path, *, repo_root=None, weight_digests=True):
    """Admit a committed-clean registration BEFORE any data or weight access.

    Every check is scoped to the registration's own enumerated artifacts (the
    page, the expectations file itself, the source manifest/scripts/stdout, the
    arm records, the listed code dependencies, the frozen scorer/scorecard and,
    when present, the pinned protocol that revalidates all 33 frozen sources):

    * each artifact is git-tracked and has no staged or unstaged change;
    * each artifact's on-disk bytes hash to its recorded SHA-256;
    * the expectations file's introducing commit is an ancestor of HEAD;
    * the arms are listed in stable committed-record path order, once each;
    * with ``weight_digests`` (the run path), each recorded weight file is
      tracked, clean and hash-exact — checked before any deserialization.

    An unrelated dirty file elsewhere in the repository is never a refusal
    reason. ``weight_digests=False`` (the read-only check-registration mode)
    touches no weight bytes at all.
    """
    root = _registration_repo(repo_root)
    path = Path(registration_path)
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        raise DiagnosticRegistrationRefused(f"the registration file is missing: {path.name}")
    try:
        relative = path.resolve().relative_to(root).as_posix()
    except ValueError as exc:
        raise DiagnosticRegistrationRefused(
            "the registration file lies outside the repository"
        ) from exc
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise DiagnosticRegistrationRefused(
            f"the registration is not valid JSON: {exc}"
        ) from exc
    if not isinstance(doc, Mapping) or doc.get("schema") != REGISTRATION_SCHEMA:
        raise DiagnosticRegistrationRefused(f"not a {REGISTRATION_SCHEMA} registration")

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(root), capture_output=True, text=True, check=False
        )

    def tracked_and_clean(relative_path):
        if git("ls-files", "--error-unmatch", "--", relative_path).returncode != 0:
            return False
        status = git("status", "--porcelain", "--", relative_path)
        return status.returncode == 0 and status.stdout.strip() == ""

    # Arm order before anything else: a reordered or duplicated registry is a
    # different registration, not this one.
    arms = doc.get("arms")
    record_paths = [arm.get("record", {}).get("path") for arm in arms]
    if record_paths != sorted(record_paths):
        raise DiagnosticRegistrationRefused(
            "the arms are not in stable committed-record path order"
        )
    arm_ids = [arm.get("arm_id") for arm in arms]
    if len(set(arm_ids)) != len(arm_ids):
        raise DiagnosticRegistrationRefused("a duplicate arm_id in the registration")

    artifacts, weights = _registration_entries(doc)
    artifacts.append((relative, None))  # the expectations file itself: tracked/clean only

    for relative_path, recorded in artifacts:
        if not tracked_and_clean(relative_path):
            raise DiagnosticRegistrationRefused(
                f"registration artifact is untracked or dirty: {relative_path}"
            )
    for relative_path, recorded in artifacts:
        if recorded is None:
            continue
        on_disk = _sha256_file(root / relative_path)
        if on_disk != recorded:
            raise DiagnosticRegistrationRefused(
                f"registration artifact changed since it was committed: {relative_path} "
                f"({on_disk} != {recorded})"
            )

    introducing = git("log", "-n1", "--format=%H", "--diff-filter=A", "--", relative)
    if introducing.returncode != 0 or not introducing.stdout.strip():
        raise DiagnosticRegistrationRefused(
            "the registration file has no introducing commit; it is not committed"
        )
    first_commit = introducing.stdout.strip().splitlines()[0]
    ancestor = git("merge-base", "--is-ancestor", first_commit, "HEAD")
    if ancestor.returncode != 0:
        raise DiagnosticRegistrationRefused(
            f"the registration commit {first_commit} is not an ancestor of HEAD"
        )

    if weight_digests:
        for what, entry in weights:
            relative_path, recorded = entry
            if not tracked_and_clean(relative_path):
                raise DiagnosticRegistrationRefused(
                    f"recorded weight file is untracked or dirty: {relative_path}"
                )
            on_disk = _sha256_file(root / relative_path)
            if on_disk != recorded:
                raise DiagnosticRegistrationRefused(
                    f"recorded weight bytes changed for {relative_path} "
                    f"({on_disk} != {recorded})"
                )

    pinned = doc.get("pinned")
    if isinstance(pinned, Mapping):
        protocol_entry = pinned.get("protocol")
        if protocol_entry is not None:
            protocol_relative, protocol_sha = _one_entry(protocol_entry, "pinned.protocol")
            if not tracked_and_clean(protocol_relative):
                raise DiagnosticRegistrationRefused(
                    f"the pinned run protocol is untracked or dirty: {protocol_relative}"
                )
            if _sha256_file(root / protocol_relative) != protocol_sha:
                raise DiagnosticRegistrationRefused(
                    f"the pinned run protocol changed: {protocol_relative}"
                )
        from pinn.verification.learnability_protocol import ProtocolDrift, load_protocol

        try:
            load_protocol(repo_root=root)
        except ProtocolDrift as exc:
            raise DiagnosticRegistrationRefused(
                f"a pinned module changed since the sealed protocol: {exc}"
            ) from exc
    return root
