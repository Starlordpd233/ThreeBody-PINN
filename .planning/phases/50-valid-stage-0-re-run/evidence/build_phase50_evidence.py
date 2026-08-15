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
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

_SCRIPT_REPO = Path(__file__).resolve().parents[4]
if str(_SCRIPT_REPO) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_REPO))

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


def _hyndman_fan_type7(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * p
    low = int(position)
    high = low if position == low else low + 1
    if high >= len(ordered):
        return ordered[-1]
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _decode_metric(value: Any) -> float:
    if isinstance(value, str):
        if value == "NaN":
            return float("nan")
        if value == "Infinity":
            return float("inf")
        if value == "-Infinity":
            return float("-inf")
    return float(value)


def _band_seed_blob(repo: Path, record: Mapping[str, Any]) -> dict[str, Any]:
    artifact = reject_escaping_path(repo, record["artifact_dir"], what="band artifact")
    summary = json.loads((artifact / "summary.json").read_text(encoding="utf-8"))
    metadata = json.loads((artifact / "training_metadata.json").read_text(encoding="utf-8"))
    splits = artifact / "splits.json"
    validation = _load_jsonl(artifact / "validation.jsonl")
    steps = _load_jsonl(artifact / "logs/train.log.jsonl")
    if summary.get("validation", {}).get("gate_status") != "ok":
        fail(f"{record['run_name']} gate_status is not healthy")
    if any(event.get("gate_status") != "ok" for event in validation):
        fail(f"{record['run_name']} has an unhealthy validation event")
    expected_steps = list(range(100, 1001, 100))
    actual_steps = [int(event["step"]) for event in validation]
    if actual_steps != expected_steps:
        fail(f"{record['run_name']} validation cadence is {actual_steps}")
    sidecar_rel = summary["validation"]["gate_sidecar"]
    sidecar = json.loads((artifact / sidecar_rel).read_text(encoding="utf-8"))
    finite = []
    nonfinite = 0
    for row in sidecar.get("rows") or []:
        value = _decode_metric(row["eps_h"])
        if math.isfinite(value):
            finite.append(value)
        else:
            nonfinite += 1
    threshold = float(sidecar["eps_h_reject_threshold"])
    tail = sum(1 for value in finite if value > threshold)
    front = []
    high_water = []
    water = -1
    for row in steps:
        if row.get("event") != "step":
            continue
        idx = int(row.get("front_idx") or 0)
        front.append({"step": int(row["step"]), "front_idx": idx})
        water = max(water, idx)
        high_water.append({"step": int(row["step"]), "front_high_water": water})
    gate = summary.get("validation") or {}
    return {
        "run_name": record["run_name"],
        "attempt_ordinal": record["attempt_ordinal"],
        "splits_sha256": sha256_file(splits),
        "s_h": metadata.get("s_h"),
        "eps_h": metadata.get("eps_h"),
        "n_train": metadata.get("n_train"),
        "preflight_status": (summary.get("conformance") or {}).get("preflight_status"),
        "eval01_precondition_i": summary.get("eval01_precondition_i"),
        "eval01_precondition_iii": gate.get("eval01_precondition_iii"),
        "final_losses": summary.get("final_losses"),
        "gate": {
            "gate_eps_h": gate.get("gate_eps_h"),
            "gate_scs": gate.get("gate_scs"),
            "gate_verdict": gate.get("gate_verdict"),
            "gate_status": gate.get("gate_status"),
            "gate_n_trajectories": gate.get("gate_n_trajectories"),
            "gate_n_nonfinite": gate.get("gate_n_nonfinite"),
            "gate_sidecar": gate.get("gate_sidecar"),
            "gate_schema_version": gate.get("gate_schema_version"),
        },
        "validation_steps": actual_steps,
        "quantiles": {
            "min": _hyndman_fan_type7(finite, 0.0),
            "p10": _hyndman_fan_type7(finite, 0.10),
            "p25": _hyndman_fan_type7(finite, 0.25),
            "p50": _hyndman_fan_type7(finite, 0.50),
            "p75": _hyndman_fan_type7(finite, 0.75),
            "p90": _hyndman_fan_type7(finite, 0.90),
            "max": _hyndman_fan_type7(finite, 1.0),
            "finite_count": len(finite),
            "nonfinite_count": nonfinite,
            "finite_tail_count": tail,
            "reject_count": tail + nonfinite,
        },
        "front": front,
        "front_high_water": high_water,
        "front_high_water_terminal": water,
    }


def cmd_band(repo: Path) -> None:
    ledger = prepare(repo, "band")
    _generation_id, _generation, records = require_complete_generation(ledger)
    if not (repo / SOURCE_MANIFEST_REL).is_file():
        fail("band requires a verified source-manifest; run extract first")
    manifest = json.loads((repo / SOURCE_MANIFEST_REL).read_text(encoding="utf-8"))
    for dest, entry in (manifest.get("files") or {}).items():
        if entry.get("role") == "checkpoint-hash":
            continue
        source = reject_escaping_path(repo, entry["source"], what="band source")
        copy = reject_escaping_path(repo, dest, what="band copy")
        live = sha256_file(source)
        if live != entry["source_sha256"] or sha256_file(copy) != entry["copy_sha256"]:
            fail(f"band source/copy hash drift: {entry['source']}")
    seeds: dict[str, Any] = {}
    smoke = None
    for record in records:
        if str(record.get("run_name", "")).endswith("smoke") and record.get("ledger_disposition") == "finished":
            smoke = record
        if record.get("in_final_band"):
            match = re.search(r"seed(41|42|43)$", record["run_name"])
            seeds[match.group(1)] = _band_seed_blob(repo, record)
    if set(seeds) != {"41", "42", "43"}:
        fail("band requires finished seeds 41/42/43")
    v2 = {
        "41": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
        "42": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "43": "a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172",
    }
    qualifications = []
    for seed, blob in seeds.items():
        if blob["splits_sha256"] != v2[seed]:
            qualifications.append(
                {
                    "seed": seed,
                    "kind": "v2_split_hash_mismatch",
                    "observed": blob["splits_sha256"],
                    "expected_v2": v2[seed],
                }
            )
    if smoke is not None:
        smoke_meta = json.loads(
            (reject_escaping_path(repo, smoke["artifact_dir"], what="smoke") / "training_metadata.json").read_text(
                encoding="utf-8"
            )
        )
        smoke_splits = sha256_file(reject_escaping_path(repo, smoke["artifact_dir"], what="smoke") / "splits.json")
        seed42 = seeds["42"]
        if (
            seed42["splits_sha256"] != smoke_splits
            or seed42["s_h"] != smoke_meta.get("s_h")
            or seed42["n_train"] != smoke_meta.get("n_train")
        ):
            fail("D-16 smoke vs seed-42 s_h/n_train/splits mismatch")
    scs_values = [seeds[seed]["gate"]["gate_scs"] for seed in ("41", "42", "43")]
    if all(isinstance(value, (int, float)) and math.isfinite(float(value)) for value in scs_values):
        scs_range = max(scs_values) - min(scs_values)
        scs_spread = {"status": "available", "dex_range": scs_range, "factor": 10 ** scs_range}
    else:
        scs_spread = {"status": "unavailable", "dex_range": None, "affected": ["41", "42", "43"]}
    payload = {
        "schema": "phase50-band-record/v2",
        "n": 3,
        "variation_label": (
            "compound descriptive n=3 variation: run.seed changes validation/test "
            "membership and model/training randomness; not isolated optimizer-seed variance"
        ),
        "seeds": seeds,
        "scs_spread": scs_spread,
        "split_hash_qualification": qualifications,
    }
    narrative = (
        "# Phase 50 Band Record\n\n"
        "Descriptive three-seed characterization. This record does not rank seeds, "
        "estimate significance, or attribute causes. n=3 spread is compound "
        "descriptive variation.\n\n"
        + "```json\n"
        + dumps_canonical(payload).rstrip()
        + "\n```\n"
    )
    atomic_write_text(repo / (PHASE_EVIDENCE / "band-record.md"), narrative)
    print("BAND-RECORD-OK")


def _structural_facts(repo: Path, record: Mapping[str, Any]) -> dict[str, bool]:
    artifact = reject_escaping_path(repo, record["artifact_dir"], what="candidate artifact")
    if (artifact / "evaluation").exists():
        fail(f"{record['run_name']} contains held-out evaluation material")
    summary = json.loads((artifact / "summary.json").read_text(encoding="utf-8"))
    gate = summary.get("validation") or {}
    sidecar_ok = False
    sidecar_rel = gate.get("gate_sidecar")
    if sidecar_rel and (artifact / sidecar_rel).is_file():
        from pinn.training.validation_gate import validate_sidecar_payload

        try:
            validate_sidecar_payload(json.loads((artifact / sidecar_rel).read_text(encoding="utf-8")))
            sidecar_ok = True
        except (OSError, ValueError, json.JSONDecodeError):
            sidecar_ok = False
    facts = {
        "eval01_precondition_i": summary.get("eval01_precondition_i") is True,
        "guard_invariant_rule": record.get("final_guard_disposition") in (None, "finished")
        and summary.get("disposition") == "finished",
        "finished": record.get("final_process_disposition") == "finished"
        and record.get("ledger_disposition") == "finished",
        "eval01_precondition_iii": gate.get("eval01_precondition_iii") is True and sidecar_ok,
    }
    facts["eligible"] = all(facts.values())
    return facts


def cmd_candidate(repo: Path) -> None:
    ledger = prepare(repo, "candidate")
    generation_id, generation, records = require_complete_generation(ledger)
    if not (repo / (PHASE_EVIDENCE / "band-record.md")).is_file():
        fail("candidate requires a band record")
    pre_reg = generation["pre_registration_commit"]
    shown = subprocess.run(
        ["git", "show", f"{pre_reg}:.planning/phases/50-valid-stage-0-re-run/50-PRE-REGISTRATION.md"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    if shown.returncode != 0:
        fail("cannot read selection policy from pre_registration ancestor blob")
    match = LEDGER_JSON_RE.search(shown.stdout)
    if match is None:
        fail("pre-registration ancestor blob has no JSON policy")
    policy_doc = json.loads(match.group(1))
    policy = policy_doc["selection_policy"]
    compact = json.dumps(policy, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    if hashlib.sha256(compact.encode("utf-8")).hexdigest() != policy_doc.get("selection_policy_sha256"):
        fail("selection policy hash drift")
    by_seed = {}
    for record in records:
        if not record.get("in_final_band"):
            continue
        match = re.search(r"seed(41|42|43)$", record["run_name"])
        by_seed[int(match.group(1))] = record
    if set(by_seed) != {41, 42, 43}:
        fail("candidate requires a complete three-seed generation")
    facts = {str(seed): _structural_facts(repo, by_seed[seed]) for seed in (42, 41, 43)}
    selected = None
    for seed in (42, 41, 43):
        if facts[str(seed)]["eligible"]:
            selected = seed
            break
    receipt: dict[str, Any] = {
        "schema": "phase50-candidate-receipt/v1",
        "pre_registration_commit": pre_reg,
        "selection_policy_sha256": policy_doc["selection_policy_sha256"],
        "band_generation": generation_id,
        "band_git_head": generation["git_head"],
        "facts": facts,
        "source_manifest_sha256": sha256_file(repo / SOURCE_MANIFEST_REL),
        "band_record_sha256": sha256_file(repo / (PHASE_EVIDENCE / "band-record.md")),
    }
    if selected is None:
        receipt.update({"run_name": None, "owner_stop": True})
    else:
        record = by_seed[selected]
        artifact = record["artifact_dir"]
        best = reject_escaping_path(repo, f"{artifact}/checkpoints/best.pt", what="best.pt")
        receipt.update(
            {
                "run_name": record["run_name"],
                "attempt_ordinal": record["attempt_ordinal"],
                "artifact_dir": artifact,
                "source_config_sha256": record.get("source_config_sha256"),
                "frozen_config_sha256": record.get("frozen_config_sha256"),
                "config_identity_digest": record.get("config_identity_digest"),
                "splits_sha256": (record.get("terminal_artifact_sha256") or {}).get("splits.json"),
                "candidate_best_path": f"{artifact}/checkpoints/best.pt",
                "best_pt_sha256": sha256_file(best) if best.is_file() else (record.get("terminal_artifact_sha256") or {}).get("checkpoints/best.pt"),
                "corpus_snapshot_sha256": record.get("corpus_snapshot_sha256"),
                "environment_snapshot_sha256": record.get("environment_snapshot_sha256"),
                "owner_stop": False,
            }
        )
    atomic_write_json(repo / (PHASE_EVIDENCE / "candidate-receipt.json"), receipt)
    print("CANDIDATE-OK")


def cmd_finalize(repo: Path) -> None:
    ledger = prepare(repo, "finalize")
    require_complete_generation(ledger)
    required = [
        SOURCE_MANIFEST_REL,
        PHASE_EVIDENCE / "band-record.md",
        PHASE_EVIDENCE / "candidate-receipt.json",
        LEDGER_REL,
        Path(__file__).resolve().relative_to(repo.resolve())
        if str(Path(__file__).resolve()).startswith(str(repo.resolve()))
        else PHASE_EVIDENCE / "build_phase50_evidence.py",
    ]
    files: dict[str, str] = {}
    for rel in (
        LEDGER_REL,
        SOURCE_MANIFEST_REL,
        PHASE_EVIDENCE / "band-record.md",
        PHASE_EVIDENCE / "candidate-receipt.json",
        PHASE_EVIDENCE / "build_phase50_evidence.py",
        PHASE_EVIDENCE / "verify_phase50_evidence.py",
    ):
        path = repo / rel
        if path.is_file():
            files[str(rel)] = sha256_file(path)
    if str(PHASE_EVIDENCE / "manifest.json") in files:
        fail("final manifest must not hash itself")
    payload = {
        "schema": "phase50-evidence-manifest/v2",
        "files": dict(sorted(files.items())),
    }
    atomic_write_json(repo / (PHASE_EVIDENCE / "manifest.json"), payload)
    print("HASHES-OK")


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
