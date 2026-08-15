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
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_REL = Path(".planning/phases/50-valid-stage-0-re-run")
PHASE_EVIDENCE = PHASE_REL / "evidence"
LEDGER_REL = PHASE_EVIDENCE / "run-ledger.md"
SOURCE_MANIFEST_REL = PHASE_EVIDENCE / "source-manifest.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEDGER_JSON_RE = re.compile(r"```json\n(.*?)\n```", re.S)
MODEL_CHECKPOINT_NAME = re.compile(
    r"^(best|latest|step-\d+|failure-.+|stage-[0-9].+|ckpt-.+)\.pt$"
)
EVALUATION_NAMES = {
    "evaluation-attempt.json",
    "evaluation-receipt.json",
    "metrics.json",
    "metrics.md",
}
FINAL_REQUIRED_RELS = (
    "config.yaml",
    "summary.json",
    "summary.md",
    "preflight.json",
    "training_metadata.json",
    "splits.json",
    "curriculum.jsonl",
    "validation.jsonl",
    "status.json",
    "logs/train.log.jsonl",
    "run_start_rng.pt",
)


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
    candidate = repo / raw
    if candidate.is_symlink():
        fail(f"{what} is a symlink: {raw!r}")
    resolved = candidate.resolve()
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


def git_output(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def is_ancestor(repo: Path, ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def path_is_symlink_or_escape(repo: Path, path: Path, *, what: str) -> Path:
    if path.is_symlink() or path.parent.is_symlink():
        fail(f"{what} is a symlink: {path}")
    current = path
    for _ in range(len(path.parts)):
        if current.is_symlink():
            fail(f"{what} is reached through a symlink: {path}")
        if current == repo:
            break
        current = current.parent
    try:
        path.resolve().relative_to(repo.resolve())
    except ValueError:
        fail(f"{what} resolves outside the repo: {path}")
    return path


def assert_no_evaluation_tree(root: Path, *, what: str) -> None:
    if not root.exists():
        return
    if (root / "evaluation").exists():
        fail(f"{what} contains an evaluation/ directory")
    for path in root.rglob("*"):
        if path.is_file() and path.name in EVALUATION_NAMES:
            fail(f"{what} contains evaluation artifact {path}")


def generation_index(ledger: Mapping[str, Any]) -> dict[int, dict[str, Any]]:
    indexed: dict[int, dict[str, Any]] = {}
    for generation in ledger["band_generations"]:
        number = int(generation["band_generation"])
        if number in indexed:
            fail(f"duplicate band_generation {number}")
        indexed[number] = generation
    return indexed


def require_complete_generation(ledger: Mapping[str, Any]) -> tuple[int, dict[str, Any], list[dict[str, Any]]]:
    final = ledger.get("final_band_generation")
    if final is None:
        fail("extract requires a generation-complete band")
    generation_id = int(final)
    generations = generation_index(ledger)
    if generation_id not in generations:
        fail(f"final_band_generation {generation_id} is missing from band_generations")
    generation = generations[generation_id]
    if generation.get("status") != "complete":
        fail(f"generation {generation_id} status is {generation.get('status')!r}")
    records = [
        record
        for record in ledger["records"]
        if int(record.get("band_generation")) == generation_id
    ]
    mixed = [
        record
        for record in ledger["records"]
        if record.get("in_final_band") and int(record.get("band_generation")) != generation_id
    ]
    if mixed:
        fail("in_final_band records exist outside the final generation")
    graded = [record for record in records if record.get("in_final_band")]
    smokes = [
        record
        for record in records
        if str(record.get("run_name", "")).endswith("smoke")
        and record.get("ledger_disposition") == "finished"
    ]
    if len(graded) != 3:
        fail(f"final generation requires exactly three in_final_band records, found {len(graded)}")
    if not smokes:
        fail("final generation requires at least one finished smoke record")
    seeds = set()
    heads = set()
    for record in records:
        name = record.get("run_name", "")
        for invocation in record.get("invocations") or []:
            if invocation.get("launch_kind") != "fresh":
                fail(f"{name} is not a fresh launch")
            command = invocation.get("launch_command") or ""
            if "--stage-0-only" not in command:
                fail(f"{name} lacks --stage-0-only")
            if "--resume" in command or invocation.get("resume_checkpoint"):
                fail(f"{name} used --resume")
    for record in graded:
        name = record.get("run_name", "")
        match = re.search(r"seed(41|42|43)$", name)
        if match is None:
            fail(f"in-band run is not a graded seed: {name}")
        seeds.add(int(match.group(1)))
        heads.add(record.get("git_head"))
        if record.get("ledger_disposition") != "finished":
            fail(f"{name} is not finished")
        if len(record.get("invocations") or []) != 1:
            fail(f"{name} does not have exactly one invocation")
    if seeds != {41, 42, 43}:
        fail(f"in-band seeds are {sorted(seeds)}, not 41/42/43")
    if len(heads) != 1 or next(iter(heads)) != generation.get("git_head"):
        fail("mixed generation/head identities")
    return generation_id, generation, records


def copy_file_atomically(source: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    temporary = dest.with_name(dest.name + f".tmp.{os.getpid()}")
    try:
        shutil.copyfile(source, temporary, follow_symlinks=False)
        os.replace(temporary, dest)
    except OSError as exc:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        fail(f"cannot copy {source} -> {dest}: {exc}")
    return sha256_file(dest)


def cmd_extract(repo: Path) -> None:
    ledger = prepare(repo, "extract")
    generation_id, generation, records = require_complete_generation(ledger)
    band_git_head = generation["git_head"]
    extraction_git_head = git_output(repo, "rev-parse", "HEAD")
    pre_reg = generation.get("pre_registration_commit")
    if not pre_reg:
        fail("generation lacks pre_registration_commit")
    if not is_ancestor(repo, pre_reg, band_git_head) and pre_reg != band_git_head:
        fail("pre_registration_commit is not an ancestor of band_git_head")

    files: dict[str, dict[str, Any]] = {}
    dests: list[str] = []
    sources: list[str] = []

    def add_entry(
        dest_rel: str,
        source_rel: str,
        digest: str,
        *,
        role: str,
        attempt: str | None = None,
        invocation: int | None = None,
        copy_digest: str | None = None,
    ) -> None:
        if digest is None or not HEX64.fullmatch(str(digest)):
            fail(f"required hash is null or malformed for {source_rel}")
        if dest_rel in files:
            fail(f"duplicate destination path: {dest_rel}")
        if source_rel in sources and role != "checkpoint-hash":
            fail(f"duplicate source path: {source_rel}")
        files[dest_rel] = {
            "source": source_rel,
            "ledger_sha256": digest,
            "source_sha256": digest,
            "copy_sha256": copy_digest or digest,
            "attempt": attempt,
            "invocation": invocation,
            "role": role,
        }
        dests.append(dest_rel)
        sources.append(source_rel)

    for record in records:
        artifact_dir = record.get("artifact_dir")
        if not artifact_dir:
            fail(f"{record.get('run_name')} missing artifact_dir")
        artifact_root = reject_escaping_path(repo, artifact_dir, what="artifact_dir")
        path_is_symlink_or_escape(repo, artifact_root, what="artifact_dir")
        assert_no_evaluation_tree(artifact_root, what=artifact_dir)
        attempt_name = f"{record['run_name']}-attempt-{int(record['attempt_ordinal']):02d}"
        terminal_map = record.get("terminal_artifact_sha256") or {}
        if record.get("in_final_band") or str(record.get("run_name", "")).endswith("smoke"):
            for required in FINAL_REQUIRED_RELS:
                if required not in terminal_map:
                    fail(f"{attempt_name} missing required {required}")
        for rel, digest in sorted(terminal_map.items()):
            source_rel = f"{artifact_dir}/{rel}"
            source_path = reject_escaping_path(repo, source_rel, what=source_rel)
            if source_path.is_symlink():
                fail(f"{source_rel} is a symlink")
            if rel.startswith("checkpoints/") or MODEL_CHECKPOINT_NAME.fullmatch(Path(rel).name):
                if Path(rel).name != "run_start_rng.pt":
                    if digest is None:
                        fail(f"checkpoint hash is null: {source_rel}")
                    add_entry(
                        f"{PHASE_EVIDENCE}/hashes/g{generation_id}/{attempt_name}/{rel}.sha256",
                        source_rel,
                        digest,
                        role="checkpoint-hash",
                        attempt=attempt_name,
                        invocation=1,
                    )
                    continue
            if not source_path.is_file():
                fail(f"required source missing: {source_rel}")
            live = sha256_file(source_path)
            if digest is None:
                fail(f"required hash is null: {source_rel}")
            if live != digest:
                fail(f"live source hash mismatch: {source_rel}")
            dest_rel = str(PHASE_EVIDENCE / "copies" / f"g{generation_id}" / attempt_name / rel)
            if rel == "failure/tail.log":
                dest_rel = str(
                    PHASE_EVIDENCE / "copies" / f"g{generation_id}" / attempt_name / "failure/tail.log.txt"
                )
            dest_path = repo / dest_rel
            copy_digest = copy_file_atomically(source_path, dest_path)
            if copy_digest != digest:
                fail(f"copy hash mismatch: {dest_rel}")
            add_entry(
                dest_rel,
                source_rel,
                digest,
                role="attempt-artifact",
                attempt=attempt_name,
                invocation=1,
                copy_digest=copy_digest,
            )
        for invocation in record.get("invocations") or []:
            transcript = invocation.get("launch_transcript")
            digest = invocation.get("transcript_sha256")
            if not transcript:
                continue
            source_path = reject_escaping_path(repo, transcript, what="launch transcript")
            if source_path.is_symlink():
                fail(f"transcript is a symlink: {transcript}")
            if not source_path.is_file():
                fail(f"launch transcript missing: {transcript}")
            live = sha256_file(source_path)
            if digest is None or live != digest:
                fail(f"transcript hash mismatch: {transcript}")
            dest_rel = str(
                PHASE_EVIDENCE
                / "copies"
                / f"g{generation_id}"
                / attempt_name
                / "launch-transcript.txt"
            )
            copy_digest = copy_file_atomically(source_path, repo / dest_rel)
            add_entry(
                dest_rel,
                transcript,
                digest,
                role="launch-transcript",
                attempt=attempt_name,
                invocation=int(invocation.get("invocation_ordinal") or 1),
                copy_digest=copy_digest,
            )

    for snapshot_key, role in (
        ("corpus_snapshot", "corpus"),
        ("environment_snapshot", "environment"),
    ):
        snapshot = generation.get(snapshot_key) or {}
        if snapshot.get("path"):
            source_rel = snapshot["path"]
            source_path = reject_escaping_path(repo, source_rel, what=role)
            digest = snapshot.get("file_sha256")
            if digest is None:
                fail(f"{role} file hash is null")
            live = sha256_file(source_path)
            if live != digest:
                fail(f"{role} live hash mismatch")
            dest_rel = str(PHASE_EVIDENCE / "copies" / f"g{generation_id}" / role / Path(source_rel).name)
            copy_digest = copy_file_atomically(source_path, repo / dest_rel)
            add_entry(dest_rel, source_rel, digest, role=role, copy_digest=copy_digest)
    for receipt in generation.get("cleanliness_receipts") or []:
        if not receipt.get("path"):
            continue
        source_rel = receipt["path"]
        digest = receipt.get("sha256")
        source_path = reject_escaping_path(repo, source_rel, what="cleanliness")
        if digest is None or sha256_file(source_path) != digest:
            fail(f"cleanliness hash mismatch: {source_rel}")
        dest_rel = str(PHASE_EVIDENCE / "copies" / f"g{generation_id}" / "cleanliness" / Path(source_rel).name)
        copy_digest = copy_file_atomically(source_path, repo / dest_rel)
        add_entry(dest_rel, source_rel, digest, role="cleanliness", copy_digest=copy_digest)

    reject_duplicate_paths(dests, what="source-manifest destinations")
    manifest = {
        "schema": "phase50-evidence-source-manifest/v1",
        "band_generation": generation_id,
        "band_git_head": band_git_head,
        "extraction_git_head": extraction_git_head,
        "pre_registration_commit": pre_reg,
        "corpus_snapshot_sha256": (generation.get("corpus_snapshot") or {}).get("corpus_snapshot_sha256"),
        "environment_snapshot_sha256": (generation.get("environment_snapshot") or {}).get(
            "environment_snapshot_sha256"
        ),
        "committed_config_set_sha256": generation.get("committed_config_set_sha256"),
        "files": {key: files[key] for key in sorted(files)},
    }
    atomic_write_json(repo / SOURCE_MANIFEST_REL, manifest)
    print(
        "EXTRACT-OK "
        f"generation={generation_id} files={len(files)} "
        f"band_git_head={band_git_head} extraction_git_head={extraction_git_head}"
    )


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
