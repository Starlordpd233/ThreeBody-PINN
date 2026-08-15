#!/usr/bin/env python3
"""Phase-50 evidence builder (serialization only).

Subcommands: extract, band, candidate, finalize.

This script writes artifacts atomically from an explicit --repo-root. It does
not derive scientific fields for the verifier to trust. When
final_band_generation is null, every subcommand refuses rather than invent a
band, candidate, source manifest, or final normal manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_EVIDENCE = Path(".planning/phases/50-valid-stage-0-re-run/evidence")
LEDGER_REL = PHASE_EVIDENCE / "run-ledger.md"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEDGER_JSON_RE = re.compile(r"```json\n(.*?)\n```", re.S)


class BuildError(SystemExit):
    """Fail-closed builder exit."""


def fail(message: str) -> None:
    raise BuildError(f"build_phase50_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_repo(root: Path) -> Path:
    repo = root.expanduser().resolve()
    if not (repo / ".planning").is_dir():
        fail(f"repo root has no .planning directory: {repo}")
    if not (repo / LEDGER_REL).is_file():
        fail(f"run ledger missing: {repo / LEDGER_REL}")
    return repo


def reject_escaping_path(repo: Path, raw: str, *, what: str) -> Path:
    if not isinstance(raw, str) or not raw or raw.startswith(("/", "~")):
        fail(f"{what} is not a repo-relative path: {raw!r}")
    parts = Path(raw).parts
    if ".." in parts or parts[:1] == ("/",):
        fail(f"{what} escapes the repo: {raw!r}")
    resolved = (repo / raw).resolve()
    try:
        resolved.relative_to(repo)
    except ValueError:
        fail(f"{what} resolves outside the repo: {raw!r}")
    return resolved


def reject_duplicate_paths(paths: list[str], *, what: str) -> None:
    seen: set[str] = set()
    for item in sorted(paths):
        if item in seen:
            fail(f"{what} has a duplicate path: {item}")
        seen.add(item)


def dumps_canonical(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    atomic_write_text(path, dumps_canonical(payload))


def load_ledger(repo: Path) -> dict[str, Any]:
    text = (repo / LEDGER_REL).read_text(encoding="utf-8")
    match = LEDGER_JSON_RE.search(text)
    if match is None:
        fail("run-ledger.md has no fenced JSON block")
    ledger = json.loads(match.group(1))
    if ledger.get("schema") != "phase50-run-ledger/v2":
        fail(f"unexpected ledger schema: {ledger.get('schema')!r}")
    return ledger


def collect_ledger_paths(ledger: Mapping[str, Any]) -> list[str]:
    paths: list[str] = []
    for generation in ledger.get("band_generations") or []:
        corpus = generation.get("corpus_snapshot") or {}
        environment = generation.get("environment_snapshot") or {}
        for raw in (corpus.get("path"), environment.get("path")):
            if raw:
                paths.append(raw)
        for receipt in generation.get("cleanliness_receipts") or []:
            if receipt.get("path"):
                paths.append(receipt["path"])
        for verify in generation.get("verify_invocations") or []:
            if verify.get("transcript"):
                paths.append(verify["transcript"])
            marker = verify.get("marker") or {}
            if marker.get("path"):
                paths.append(marker["path"])
    for record in ledger.get("records") or []:
        if record.get("artifact_dir"):
            paths.append(record["artifact_dir"])
        if record.get("config"):
            paths.append(record["config"])
        for invocation in record.get("invocations") or []:
            if invocation.get("launch_transcript"):
                paths.append(invocation["launch_transcript"])
            for key in ("calibration_before", "calibration_after"):
                blob = invocation.get(key) or {}
                if blob.get("path"):
                    paths.append(blob["path"])
    return paths


def assert_sorted_unique_paths(repo: Path, paths: list[str], *, what: str) -> None:
    reject_duplicate_paths(sorted(set(paths)), what=what)
    for raw in sorted(set(paths)):
        reject_escaping_path(repo, raw, what=what)


def refuse_terminal(ledger: Mapping[str, Any], command: str) -> None:
    if ledger.get("final_band_generation") is None:
        fail(
            f"{command} is a normal-mode serializer; "
            "final_band_generation is null so no band, candidate, "
            "source-manifest, or final normal manifest may be written"
        )


def prepare(repo: Path, command: str) -> dict[str, Any]:
    ledger = load_ledger(repo)
    assert_sorted_unique_paths(repo, collect_ledger_paths(ledger), what="ledger path")
    refuse_terminal(ledger, command)
    return ledger


def cmd_extract(repo: Path) -> None:
    prepare(repo, "extract")
    fail("extract requires a generation-complete band")


def cmd_band(repo: Path) -> None:
    prepare(repo, "band")
    fail("band requires a generation-complete band")


def cmd_candidate(repo: Path) -> None:
    prepare(repo, "candidate")
    fail("candidate requires a generation-complete band")


def cmd_finalize(repo: Path) -> None:
    prepare(repo, "finalize")
    fail("finalize requires a generation-complete band")


def build_parser() -> argparse.ArgumentParser:
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--repo-root", required=True, type=Path)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("extract", "band", "candidate", "finalize"):
        sub.add_parser(name, parents=[parent])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = require_repo(args.repo_root)
    dispatch = {
        "extract": cmd_extract,
        "band": cmd_band,
        "candidate": cmd_candidate,
        "finalize": cmd_finalize,
    }
    dispatch[args.command](repo)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(exc.code if isinstance(exc.code, int) else 1)
