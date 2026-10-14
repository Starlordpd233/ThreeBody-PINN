#!/usr/bin/env python3
"""Phase 59: the independent evidence verifier for the read-only baseline.

Fail-closed checks for the frozen scorecard, area manifests, and guardrails.
This script does not import evidence_io or any producing tool's helpers.
Re-derivation, when a later subcommand asks for it, is a subprocess --check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

from pinn.verification.feasibility_scorecard import (  # noqa: E402
    SCORECARD_SHA256,
    load_scorecard,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
PHASE_REL = Path(".planning/phases/59-read-only-baseline-scorecard")
EVIDENCE_REL = PHASE_REL / "evidence"
FREEZE_REL = EVIDENCE_REL / "scorecard-freeze.json"
AREAS = ("audit", "census", "survey", "baselines", "diag07")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
_DECISION_MODES = {
    f"{PHASE_REL.as_posix()}/59-CONTEXT.md": "unchanged",
    f"{PHASE_REL.as_posix()}/59-GAPS.md": "ancestor_state",
    f"{PHASE_REL.as_posix()}/59-RESEARCH.md": "unchanged",
    f"{PHASE_REL.as_posix()}/59-VALIDATION.md": "ancestor_state",
}


class VerifyError(RuntimeError):
    """Fail-closed evidence verification error."""


def fail(message: str) -> None:
    raise VerifyError(f"verify_phase59_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def repo_path(raw: str | Path, *, what: str, root: Optional[Path] = None) -> Path:
    root = REPO_ROOT if root is None else root
    supplied = Path(str(raw))
    resolved = (root / supplied).resolve() if not supplied.is_absolute() else supplied.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        fail(f"{what} escapes the repository: {raw!r}")
    candidate = root / supplied
    if not supplied.is_absolute() and candidate.is_symlink():
        fail(f"{what} is a symlink: {raw!r}")
    return resolved


def load_json(path: Path, *, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{what} is unreadable JSON: {path}: {exc}")


def _git(*args: str, binary: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=not binary,
        check=False,
    )


def is_ancestor(ancestor: str, descendant: str) -> bool:
    return _git("merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


def first_commit_of(relative: str) -> str:
    proc = _git("log", "--diff-filter=A", "--format=%H", "--", relative)
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if proc.returncode != 0 or not lines:
        fail(f"no add commit for {relative}")
    return lines[-1]


def is_tracked(relative: str) -> bool:
    return _git("ls-files", "--error-unmatch", "--", relative).returncode == 0


def is_clean(relative: str) -> bool:
    return _git("status", "--porcelain", "--", relative).stdout.strip() == ""


def _rev_parse(spec: str) -> str:
    proc = _git("rev-parse", spec)
    if proc.returncode != 0 or not proc.stdout.strip():
        fail(f"git rev-parse failed for {spec}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def _show_bytes(spec: str) -> bytes:
    proc = _git("show", spec, binary=True)
    if proc.returncode != 0:
        fail(f"git show failed for {spec}")
    return proc.stdout


def _freeze_record() -> dict[str, Any]:
    path = repo_path(FREEZE_REL, what="freeze record")
    if not path.is_file():
        fail("freeze record is absent")
    record = load_json(path, what="freeze record")
    if not isinstance(record, Mapping):
        fail("freeze record is not a JSON object")
    return dict(record)


def _frozen_rels(record: Mapping[str, Any]) -> list[str]:
    return [
        str(record["scorecard_path"]),
        str(record["scorecard_module_path"]),
        str(record["plain_doc_path"]),
        FREEZE_REL.as_posix(),
    ]


def _assert_recorded_hashes(record: Mapping[str, Any]) -> None:
    scorecard = repo_path(str(record["scorecard_path"]), what="scorecard")
    digest = sha256_file(scorecard)
    expected = str(record.get("scorecard_sha256"))
    if digest != expected or digest != SCORECARD_SHA256:
        fail(
            f"scorecard sha256 {digest} != record {expected} or {SCORECARD_SHA256}"
        )
    module = repo_path(str(record["scorecard_module_path"]), what="rule module")
    module_digest = sha256_file(module)
    if module_digest != str(record.get("scorecard_module_sha256")):
        fail(
            "rule module sha256 "
            f"{module_digest} != {record.get('scorecard_module_sha256')}"
        )
    plain = repo_path(str(record["plain_doc_path"]), what="plain document")
    plain_digest = sha256_file(plain)
    if plain_digest != str(record.get("plain_doc_sha256")):
        fail(
            f"plain document sha256 {plain_digest} != {record.get('plain_doc_sha256')}"
        )
    load_scorecard()


def _assert_decision_sources(record: Mapping[str, Any], freeze_commit: str) -> None:
    pins = record.get("decision_sources")
    if not isinstance(pins, Mapping) or set(pins) != set(_DECISION_MODES):
        fail("decision_sources must pin exactly the four decision files")
    for relative, mode in _DECISION_MODES.items():
        pin = pins[relative]
        if not isinstance(pin, Mapping) or pin.get("verify") != mode:
            fail(f"{relative} verify mode is not {mode}")
        blob = _rev_parse(f"{freeze_commit}:{relative}")
        if blob != pin.get("git_blob"):
            fail(f"{relative} git_blob {blob} != {pin.get('git_blob')}")
        digest = sha256_bytes(_show_bytes(f"{freeze_commit}:{relative}"))
        if digest != pin.get("sha256"):
            fail(f"{relative} sha256 {digest} != {pin.get('sha256')}")
        last = _git("log", "-1", "--format=%H", freeze_commit, "--", relative).stdout.strip()
        if last != pin.get("last_commit"):
            fail(f"{relative} last_commit {last} != {pin.get('last_commit')}")
        if not is_ancestor(str(pin.get("last_commit")), freeze_commit):
            fail(f"{relative} last_commit is not an ancestor of the freeze commit")
        if mode != "unchanged":
            continue
        if not is_tracked(relative) or not is_clean(relative):
            fail(f"{relative} is dirty")
        current = sha256_file(repo_path(relative, what=relative))
        if current != pin.get("sha256"):
            fail(f"{relative} changed after the freeze commit")


def _assert_area_commit_order(freeze_commit: str) -> None:
    for area in AREAS:
        listed = _git("ls-files", "--", f"{EVIDENCE_REL.as_posix()}/{area}")
        if listed.returncode != 0:
            fail(f"cannot list tracked files in {area}: {listed.stderr.strip()}")
        for relative in [line for line in listed.stdout.splitlines() if line.strip()]:
            first = first_commit_of(relative)
            if first == freeze_commit or not is_ancestor(freeze_commit, first):
                fail(
                    "commit-order ancestor check failed for "
                    f"{relative}: first commit {first} is not a strict descendant "
                    f"of freeze commit {freeze_commit}"
                )


def _assert_result_scorecard_hashes() -> None:
    for area in AREAS:
        directory = REPO_ROOT / EVIDENCE_REL / area
        if not directory.is_dir():
            continue
        for path in directory.rglob("*.json"):
            if "__pycache__" in path.parts or "logs" in path.parts:
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if isinstance(payload, Mapping) and "scorecard_sha256" in payload:
                if payload["scorecard_sha256"] != SCORECARD_SHA256:
                    fail(f"{path.name} scorecard_sha256 != {SCORECARD_SHA256}")


def assert_scorecard_frozen(*, pre_commit: bool = False) -> str:
    """Check the four frozen files. Return the freeze commit (empty when skipped)."""
    record = _freeze_record()
    rels = _frozen_rels(record)
    if not pre_commit:
        for relative in rels:
            if not is_tracked(relative) or not is_clean(relative):
                fail(f"frozen file is dirty: {relative}")
    _assert_recorded_hashes(record)
    _assert_result_scorecard_hashes()
    if pre_commit:
        pins = record.get("decision_sources")
        if not isinstance(pins, Mapping) or set(pins) != set(_DECISION_MODES):
            fail("decision_sources must pin exactly the four decision files")
        return ""
    freeze_commit = first_commit_of(FREEZE_REL.as_posix())
    diff = _git("diff", "--quiet", freeze_commit, "HEAD", "--", *rels)
    if diff.returncode != 0:
        fail(f"frozen files differ from the freeze commit {freeze_commit}")
    _assert_decision_sources(record, freeze_commit)
    head = _rev_parse("HEAD")
    if not is_ancestor(freeze_commit, head):
        fail(f"freeze commit {freeze_commit} is not an ancestor of HEAD {head}")
    _assert_area_commit_order(freeze_commit)
    return freeze_commit


def cmd_scorecard_frozen(args: argparse.Namespace) -> None:
    assert_scorecard_frozen(pre_commit=bool(args.pre_commit))
    print("SCORECARD-FROZEN-OK")


COMMANDS = {
    "scorecard-frozen": cmd_scorecard_frozen,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=tuple(COMMANDS))
    parser.add_argument("--pre-commit", action="store_true")
    parser.add_argument("--area", default=None)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--skip-rederive", action="store_true")
    parser.add_argument("--require-committed", action="store_true")
    parser.add_argument("--require", default=None)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        COMMANDS[args.command](args)
    except Exception as exc:  # noqa: BLE001 - verifier CLI is fail-closed
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
