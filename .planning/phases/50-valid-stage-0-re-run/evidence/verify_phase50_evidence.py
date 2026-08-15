#!/usr/bin/env python3
"""Independent Phase-50 evidence verifier.

Subcommands: manifest, band, candidate, terminal, all.

This module re-derives hashes and terminal facts from the ledger, live
sources, committed copies, and terminal-manifest.json. It must not import
builder derivation functions or trust builder caches.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

PHASE_REL = Path(".planning/phases/50-valid-stage-0-re-run")
EVIDENCE_REL = PHASE_REL / "evidence"
LEDGER_REL = EVIDENCE_REL / "run-ledger.md"
ATTEMPTS_REL = EVIDENCE_REL / "attempts"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEDGER_JSON_RE = re.compile(r"```json\n(.*?)\n```", re.S)
ATTEMPT_DIR_RE = re.compile(r"^(?P<run>.+)-attempt-(?P<ord>\d+)$")
MODEL_CHECKPOINT_NAME = re.compile(
    r"^(best|latest|step-\d+|failure-.+|stage-[0-9].+|ckpt-.+)\.pt$"
)
EVALUATION_NAMES = {
    "evaluation-attempt.json",
    "evaluation-receipt.json",
    "metrics.json",
    "metrics.md",
}
NORMAL_MODE_ARTIFACTS = (
    EVIDENCE_REL / "band-record.md",
    EVIDENCE_REL / "candidate-receipt.json",
    EVIDENCE_REL / "manifest.json",
    EVIDENCE_REL / "source-manifest.json",
)
EVAL_COMMAND_NEEDLES = ("pinn.evaluate", "pinn/evaluate.py", "python -m pinn.evaluate")


class VerifyError(SystemExit):
    """Fail-closed verifier exit."""


def fail(message: str) -> None:
    raise VerifyError(f"verify_phase50_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_hex64(value: Any, *, what: str) -> str:
    if value is None:
        fail(f"{what} is null")
    if not isinstance(value, str) or not HEX64.fullmatch(value):
        fail(f"{what} is not a 64-hex sha256: {value!r}")
    return value


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


def reject_duplicate_paths(paths: Iterable[str], *, what: str) -> None:
    seen: set[str] = set()
    for item in sorted(paths):
        if item in seen:
            fail(f"{what} has a duplicate path: {item}")
        seen.add(item)


def load_json(path: Path, *, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{what} is not readable JSON: {path}: {exc}")


def load_ledger(repo: Path) -> dict[str, Any]:
    text = (repo / LEDGER_REL).read_text(encoding="utf-8")
    match = LEDGER_JSON_RE.search(text)
    if match is None:
        fail("run-ledger.md has no fenced JSON block")
    ledger = json.loads(match.group(1))
    if ledger.get("schema") != "phase50-run-ledger/v2":
        fail(f"unexpected ledger schema: {ledger.get('schema')!r}")
    if not isinstance(ledger.get("band_generations"), list):
        fail("ledger band_generations is not a list")
    if not isinstance(ledger.get("records"), list):
        fail("ledger records is not a list")
    return ledger


def git_ls_files(repo: Path, prefix: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", str(prefix)],
        cwd=str(repo),
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"git ls-files failed for {prefix}: {result.stderr.decode()}")
    return [item.decode() for item in result.stdout.split(b"\0") if item]


def command_has_evaluation(command: str) -> bool:
    return any(needle in command for needle in EVAL_COMMAND_NEEDLES)


def parse_attempt_dirname(name: str) -> tuple[str, int]:
    match = ATTEMPT_DIR_RE.fullmatch(name)
    if match is None:
        fail(f"attempt copy directory is not <run>-attempt-<NN>: {name}")
    return match.group("run"), int(match.group("ord"))


def record_key(record: Mapping[str, Any]) -> tuple[str, int]:
    return record["run_name"], int(record["attempt_ordinal"])


def index_records(ledger: Mapping[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    indexed: dict[tuple[str, int], dict[str, Any]] = {}
    keys: list[tuple[str, int]] = []
    for record in ledger["records"]:
        key = record_key(record)
        keys.append(key)
        if key in indexed:
            fail(f"duplicate ledger record {key}")
        indexed[key] = record
    reject_duplicate_paths((f"{run}/{ordinal}" for run, ordinal in keys), what="ledger record")
    return indexed


def latest_generation(ledger: Mapping[str, Any]) -> dict[str, Any]:
    generations = ledger["band_generations"]
    if not generations:
        fail("ledger has no band_generations")
    return max(generations, key=lambda item: int(item["band_generation"]))


def terminal_sections(manifest: Mapping[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    if manifest.get("schema") != "phase50-terminal-manifest/v1":
        fail(f"unexpected terminal-manifest schema: {manifest.get('schema')!r}")
    sections: list[tuple[str, dict[str, Any]]] = [("generation_root", dict(manifest))]
    extra_keys = sorted(
        key
        for key in manifest
        if isinstance(key, str) and re.fullmatch(r"generation_\d+", key)
    )
    for key in extra_keys:
        blob = manifest[key]
        if not isinstance(blob, dict):
            fail(f"{key} is not an object")
        if blob.get("schema") != "phase50-terminal-manifest/v1":
            fail(f"{key} schema is not phase50-terminal-manifest/v1")
        sections.append((key, blob))
    return sections


def relative_under(prefix: str, raw: str) -> str | None:
    prefix_slash = prefix.rstrip("/") + "/"
    if raw == prefix.rstrip("/"):
        return ""
    if raw.startswith(prefix_slash):
        return raw[len(prefix_slash) :]
    return None


def live_source_for_copy(
    repo: Path,
    record: Mapping[str, Any] | None,
    source_raw: str,
    copy_rel: str,
) -> Path | None:
    source_path = reject_escaping_path(repo, source_raw, what="attempt-copy source")
    if source_path.is_file():
        return source_path
    if record and record.get("artifact_dir"):
        artifact = reject_escaping_path(repo, record["artifact_dir"], what="artifact_dir")
        candidate = artifact / Path(source_raw).name
        if copy_rel.endswith("logs/train.log.txt"):
            candidate = artifact / "logs" / "train.log"
        elif copy_rel.startswith("failure/"):
            candidate = artifact / copy_rel
        elif relative_under(record["artifact_dir"], source_raw) is not None:
            candidate = artifact / relative_under(record["artifact_dir"], source_raw)
        else:
            suffix = Path(source_raw)
            if len(suffix.parts) >= 2 and suffix.parts[0] == "runs":
                candidate = artifact / Path(*suffix.parts[2:])
            else:
                candidate = artifact / copy_rel
        if candidate.is_file():
            return candidate
    return source_path if source_path.exists() else None


def assert_hash_equal(path: Path, expected: str, *, what: str) -> None:
    if not path.is_file():
        fail(f"{what} is missing: {path}")
    actual = sha256_file(path)
    if actual != expected:
        fail(f"{what} hash mismatch: {path} expected {expected} computed {actual}")


def walk_files(root: Path) -> Iterator[Path]:
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def assert_no_evaluation_tree(repo: Path, root_rel: str, *, what: str) -> None:
    root = reject_escaping_path(repo, root_rel, what=what)
    if not root.exists():
        return
    if (root / "evaluation").exists():
        fail(f"{what} contains an evaluation/ directory: {root / 'evaluation'}")
    for path in walk_files(root):
        if path.name in EVALUATION_NAMES:
            fail(f"{what} contains evaluation artifact {path}")


def assert_observed_mismatch(blob: Mapping[str, Any], *, section: str) -> None:
    mismatch = blob.get("observed_mismatch")
    if mismatch is None:
        fail(f"{section} observed_mismatch is null; use {{applicable: false}} for a non-drift terminal")
    if not isinstance(mismatch, dict):
        fail(f"{section} observed_mismatch is not an object")
    if "applicable" not in mismatch:
        fail(f"{section} observed_mismatch lacks applicable")
    applicable = mismatch["applicable"]
    if not isinstance(applicable, bool):
        fail(f"{section} observed_mismatch.applicable is not a boolean")
    if applicable:
        for key in (
            "expected_historical_identity",
            "observed_current_identity",
            "causal_boundary_receipt",
        ):
            if key not in mismatch or mismatch[key] in (None, ""):
                fail(f"{section} drift closeout is missing {key}")
        receipt = mismatch["causal_boundary_receipt"]
        if not isinstance(receipt, dict) or not receipt.get("path") or not receipt.get("sha256"):
            fail(f"{section} causal_boundary_receipt must carry path and sha256")


def assert_failure_tail(
    repo: Path,
    ledger: Mapping[str, Any],
    section: Mapping[str, Any],
    *,
    name: str,
) -> None:
    produced: list[str] = []
    for record in ledger["records"]:
        artifact_dir = record.get("artifact_dir")
        if not artifact_dir:
            continue
        tail = reject_escaping_path(repo, f"{artifact_dir}/failure/tail.log", what="failure tail")
        if tail.is_file():
            produced.append(f"{artifact_dir}/failure/tail.log")
    note = (section.get("missing_vs_inapplicable") or {}).get("failure_tail_log", "")
    if produced:
        if isinstance(note, str) and note.lower().startswith("inapplicable"):
            fail(f"{name} marks failure_tail_log inapplicable but tail.log exists: {produced}")
        copies = (section.get("hashes") or {}).get("attempt_copies") or {}
        for source in produced:
            matched = False
            for attempt_name, files in copies.items():
                if not isinstance(files, dict):
                    continue
                entry = files.get("failure/tail.log.txt")
                if not isinstance(entry, dict):
                    continue
                if entry.get("source") == source:
                    require_hex64(entry.get("sha256"), what=f"{attempt_name} failure/tail.log.txt")
                    copy_path = reject_escaping_path(
                        repo,
                        str(ATTEMPTS_REL / attempt_name / "failure/tail.log.txt"),
                        what="failure tail copy",
                    )
                    assert_hash_equal(
                        copy_path,
                        entry["sha256"],
                        what=f"{attempt_name} failure/tail.log.txt copy",
                    )
                    assert_hash_equal(
                        reject_escaping_path(repo, source, what="failure tail source"),
                        entry["sha256"],
                        what=f"{attempt_name} failure/tail.log source",
                    )
                    matched = True
            if not matched:
                fail(f"{name} produced {source} but has no committed failure/tail.log.txt copy")
    elif not (isinstance(note, str) and note.lower().startswith("inapplicable")):
        fail(f"{name} has no tail.log but does not mark failure_tail_log inapplicable")

    for path in walk_files(repo / ATTEMPTS_REL):
        if path.name == "tail.log":
            fail(f"committed failure tail was not renamed to .txt: {path}")


def assert_no_committed_model_checkpoints(repo: Path) -> None:
    tracked = git_ls_files(repo, PHASE_REL)
    for rel in tracked:
        name = Path(rel).name
        if name == "run_start_rng.pt":
            continue
        if Path(rel).parts[-2:] == ("checkpoints", name) or MODEL_CHECKPOINT_NAME.fullmatch(name):
            fail(f"committed model-checkpoint bytes: {rel}")
    for path in walk_files(repo / EVIDENCE_REL):
        if path.name == "run_start_rng.pt":
            continue
        if "checkpoints" in path.parts and path.suffix == ".pt":
            fail(f"evidence tree contains model-checkpoint bytes: {path}")


def assert_no_evaluation(repo: Path, ledger: Mapping[str, Any]) -> None:
    for generation in ledger["band_generations"]:
        for verify in generation.get("verify_invocations") or []:
            command = verify.get("command") or ""
            if command_has_evaluation(command):
                fail(f"verify invocation contains an evaluation command: {command}")
    for record in ledger["records"]:
        for invocation in record.get("invocations") or []:
            command = invocation.get("launch_command") or ""
            if command_has_evaluation(command):
                fail(f"launch command contains an evaluation command: {command}")
        if record.get("artifact_dir"):
            assert_no_evaluation_tree(repo, record["artifact_dir"], what="run artifact_dir")
    assert_no_evaluation_tree(repo, str(ATTEMPTS_REL), what="evidence attempts")
    assert_no_evaluation_tree(repo, str(EVIDENCE_REL), what="evidence tree")


def assert_no_normal_artifacts(repo: Path) -> None:
    present = [str(path) for path in NORMAL_MODE_ARTIFACTS if (repo / path).exists()]
    if present:
        fail(f"terminal mode forbids normal-mode artifacts: {present}")


def assert_ledger_hashes(repo: Path, ledger: Mapping[str, Any]) -> dict[str, int]:
    counts = {
        "cleanliness": 0,
        "verify": 0,
        "transcripts": 0,
        "terminal_artifacts": 0,
    }
    for generation in ledger["band_generations"]:
        if generation.get("status") != "terminal":
            fail(f"generation {generation.get('band_generation')} status is {generation.get('status')!r}")
        for receipt in generation.get("cleanliness_receipts") or []:
            path = reject_escaping_path(repo, receipt["path"], what="cleanliness receipt")
            assert_hash_equal(
                path,
                require_hex64(receipt.get("sha256"), what=receipt["path"]),
                what="cleanliness receipt",
            )
            counts["cleanliness"] += 1
        for verify in generation.get("verify_invocations") or []:
            path = reject_escaping_path(repo, verify["transcript"], what="verify transcript")
            assert_hash_equal(
                path,
                require_hex64(verify.get("transcript_sha256"), what=verify["transcript"]),
                what="verify transcript",
            )
            if verify.get("marker"):
                marker_path = reject_escaping_path(repo, verify["marker"]["path"], what="verify marker")
                assert_hash_equal(
                    marker_path,
                    require_hex64(verify["marker"].get("sha256"), what=verify["marker"]["path"]),
                    what="verify marker",
                )
            counts["verify"] += 1
        for snapshot in (
            generation.get("corpus_snapshot") or {},
            generation.get("environment_snapshot") or {},
        ):
            if snapshot.get("path"):
                file_path = reject_escaping_path(repo, snapshot["path"], what="generation snapshot")
                if snapshot.get("file_sha256"):
                    assert_hash_equal(
                        file_path,
                        require_hex64(snapshot["file_sha256"], what=snapshot["path"]),
                        what="generation snapshot file",
                    )
                payload = load_json(file_path, what="generation snapshot")
                digest_key = (
                    "corpus_snapshot_sha256"
                    if "corpus" in Path(snapshot["path"]).parts
                    else "environment_snapshot_sha256"
                )
                if snapshot.get(digest_key):
                    if payload.get(digest_key) != snapshot[digest_key]:
                        fail(f"{snapshot['path']} {digest_key} does not match the ledger")
    records = index_records(ledger)
    if any(record.get("in_final_band") for record in records.values()):
        fail("terminal ledger has in_final_band=true records")
    for record in records.values():
        for invocation in record.get("invocations") or []:
            if invocation.get("launch_kind") != "fresh":
                fail(f"{record['run_name']} attempt {record['attempt_ordinal']} is not a fresh launch")
            command = invocation.get("launch_command") or ""
            if "--stage-0-only" not in command:
                fail(f"{record['run_name']} attempt {record['attempt_ordinal']} lacks --stage-0-only")
            if "--resume" in command:
                fail(f"{record['run_name']} attempt {record['attempt_ordinal']} used --resume")
            transcript = reject_escaping_path(
                repo, invocation["launch_transcript"], what="launch transcript"
            )
            assert_hash_equal(
                transcript,
                require_hex64(invocation.get("transcript_sha256"), what=invocation["launch_transcript"]),
                what="launch transcript",
            )
            counts["transcripts"] += 1
            for key in ("calibration_before", "calibration_after"):
                blob = invocation.get(key) or {}
                if blob.get("path"):
                    assert_hash_equal(
                        reject_escaping_path(repo, blob["path"], what=key),
                        require_hex64(blob.get("sha256"), what=blob["path"]),
                        what=key,
                    )
        artifact_dir = record.get("artifact_dir")
        terminal_map = record.get("terminal_artifact_sha256") or {}
        if artifact_dir:
            reject_escaping_path(repo, artifact_dir, what="artifact_dir")
            for rel, digest in sorted(terminal_map.items()):
                require_hex64(digest, what=f"{artifact_dir}/{rel}")
                live = reject_escaping_path(repo, f"{artifact_dir}/{rel}", what="terminal artifact")
                if live.is_file():
                    assert_hash_equal(live, digest, what=f"live {artifact_dir}/{rel}")
                    counts["terminal_artifacts"] += 1
                elif not rel.startswith("checkpoints/"):
                    fail(f"required non-checkpoint terminal artifact missing: {artifact_dir}/{rel}")
        elif terminal_map:
            fail(f"{record['run_name']} attempt {record['attempt_ordinal']} has hashes but no artifact_dir")
    return counts


def assert_section_hashes(
    repo: Path,
    ledger: Mapping[str, Any],
    section: Mapping[str, Any],
    *,
    name: str,
    is_latest: bool,
) -> int:
    hashes = section.get("hashes")
    if not isinstance(hashes, dict):
        fail(f"{name} hashes is not an object")
    records = index_records(ledger)
    generation_id = int((section.get("generation") or {}).get("band_generation"))
    if is_latest:
        ledger_hash = require_hex64(hashes.get("run_ledger_md"), what=f"{name} run_ledger_md")
        assert_hash_equal(repo / LEDGER_REL, ledger_hash, what="current run-ledger.md")
    else:
        require_hex64(hashes.get("run_ledger_md"), what=f"{name} historical run_ledger_md")

    copies = hashes.get("attempt_copies")
    if not isinstance(copies, dict):
        fail(f"{name} attempt_copies is not an object")
    copy_count = 0
    dest_paths: list[str] = []
    for attempt_name in sorted(copies):
        files = copies[attempt_name]
        if not isinstance(files, dict):
            fail(f"{name} {attempt_name} copy map is not an object")
        run_name, ordinal = parse_attempt_dirname(attempt_name)
        record = records.get((run_name, ordinal))
        if record is None:
            fail(f"{name} attempt copy {attempt_name} is not in the ledger")
        if int(record["band_generation"]) != generation_id:
            fail(f"{name} attempt copy {attempt_name} is not generation {generation_id}")
        copy_root = ATTEMPTS_REL / attempt_name
        for rel in sorted(files):
            dest_paths.append(f"{attempt_name}/{rel}")
            meta = files[rel]
            if not isinstance(meta, dict):
                fail(f"{attempt_name}/{rel} is not a source/sha256 object")
            digest = require_hex64(meta.get("sha256"), what=f"{attempt_name}/{rel}")
            source_raw = meta.get("source")
            if not source_raw:
                fail(f"{attempt_name}/{rel} lacks source")
            copy_path = reject_escaping_path(repo, str(copy_root / rel), what="attempt copy")
            assert_hash_equal(copy_path, digest, what=f"copy {attempt_name}/{rel}")
            live = live_source_for_copy(repo, record, source_raw, rel)
            if live is None:
                fail(f"{attempt_name}/{rel} live source missing: {source_raw}")
            live_digest = sha256_file(live)
            recorded_source = reject_escaping_path(repo, source_raw, what="attempt-copy source")
            if recorded_source.is_file() and sha256_file(recorded_source) == digest:
                pass
            elif record.get("artifact_dir"):
                archived = reject_escaping_path(
                    repo,
                    f"{record['artifact_dir']}/{rel if rel != 'logs/train.log.txt' else 'logs/train.log'}",
                    what="archived live source",
                )
                if rel == "launch-transcript.txt":
                    archived = reject_escaping_path(repo, source_raw, what="transcript source")
                if archived.is_file() and sha256_file(archived) == digest:
                    pass
                elif live_digest == digest:
                    pass
                else:
                    fail(
                        f"{attempt_name}/{rel} live source hash mismatch "
                        f"(source={source_raw} live={live} computed={live_digest})"
                    )
            elif live_digest != digest:
                fail(f"{attempt_name}/{rel} live source hash mismatch: {source_raw}")
            copy_count += 1

        if record.get("artifact_dir"):
            terminal_map = record.get("terminal_artifact_sha256") or {}
            for rel, digest in sorted(terminal_map.items()):
                if rel.startswith("checkpoints/"):
                    continue
                if rel == "logs/train.log.jsonl" and "logs/train.log.jsonl" in files:
                    if files["logs/train.log.jsonl"]["sha256"] != digest:
                        fail(f"{attempt_name} copy of {rel} disagrees with the ledger")
                elif rel in files and files[rel]["sha256"] != digest:
                    fail(f"{attempt_name} copy of {rel} disagrees with the ledger")

    reject_duplicate_paths(dest_paths, what=f"{name} attempt copy destinations")

    required = section.get("required_non_null_hashes") or {}
    if not isinstance(required, dict) or not required:
        fail(f"{name} required_non_null_hashes is missing")
    for key, digest in sorted(required.items()):
        require_hex64(digest, what=f"{name} required {key}")

    generation_blob = section.get("generation") or {}
    if generation_blob.get("status") != "terminal":
        fail(f"{name} generation.status is {generation_blob.get('status')!r}")
    if required.get("corpus_snapshot_sha256") != generation_blob.get("corpus_snapshot_sha256"):
        fail(f"{name} corpus_snapshot_sha256 disagrees with generation")
    if required.get("environment_snapshot_sha256") != generation_blob.get(
        "environment_snapshot_sha256"
    ):
        fail(f"{name} environment_snapshot_sha256 disagrees with generation")

    for config_name, required_key in (
        ("stage0-rerun-smoke.yaml", "smoke_source_config_sha256"),
        ("stage0-rerun-seed41.yaml", "seed41_source_config_sha256"),
    ):
        config_path = reject_escaping_path(repo, f"configs/{config_name}", what="source config")
        assert_hash_equal(
            config_path,
            require_hex64(required.get(required_key), what=f"{name} {required_key}"),
            what=f"committed {config_name}",
        )

    for key, value in sorted(hashes.items()):
        if key.endswith("_transcript") and isinstance(value, str):
            require_hex64(value, what=f"{name} {key}")
            matched = False
            for record in ledger["records"]:
                if int(record["band_generation"]) != generation_id:
                    continue
                for invocation in record.get("invocations") or []:
                    if invocation.get("transcript_sha256") == value:
                        assert_hash_equal(
                            reject_escaping_path(
                                repo, invocation["launch_transcript"], what="section transcript"
                            ),
                            value,
                            what=f"{name} {key}",
                        )
                        matched = True
            if not matched:
                fail(f"{name} {key} does not match any ledger transcript")

        if key.endswith("_terminal_artifact_sha256") and isinstance(value, dict):
            for rel, digest in sorted(value.items()):
                require_hex64(digest, what=f"{name} {key}/{rel}")
            mapped = None
            for record in ledger["records"]:
                if int(record["band_generation"]) != generation_id:
                    continue
                if key.startswith("smoke") and record["run_name"].endswith("smoke"):
                    mapped = record
                if key.startswith("seed41") and record["run_name"].endswith("seed41"):
                    mapped = record
            if mapped is None:
                fail(f"{name} {key} has no matching ledger record")
            if mapped.get("terminal_artifact_sha256") != value:
                fail(f"{name} {key} does not equal the ledger terminal_artifact_sha256 map")
    return copy_count


def assert_generation3_reason(repo: Path, ledger: Mapping[str, Any], section: Mapping[str, Any]) -> None:
    if section.get("terminal_reason") != "invariant-b-halt-front-idx-stalled-n-500":
        fail(f"generation_3 terminal_reason is {section.get('terminal_reason')!r}")
    latest = latest_generation(ledger)
    proof = latest.get("seed41_first_validation_proof") or {}
    if proof.get("stage_zero_underpopulated_absent") is not True:
        fail("generation-3 C-09 first-validation proof is not present")
    if int(proof.get("first_event_step") or 0) != 100:
        fail("generation-3 first validation event is not step 100")
    seed41 = None
    for record in ledger["records"]:
        if record["band_generation"] == 3 and record["run_name"] == "stage0-rerun-seed41":
            seed41 = record
            break
    if seed41 is None:
        fail("generation 3 has no seed-41 record")
    if seed41.get("ledger_disposition") != "halted":
        fail(f"generation-3 seed 41 disposition is {seed41.get('ledger_disposition')!r}")
    if seed41.get("final_guard_disposition") != "HALT":
        fail("generation-3 seed 41 is not a guard HALT")
    record_proof = seed41.get("first_validation_proof") or {}
    if record_proof.get("stage_zero_underpopulated_absent") is not True:
        fail("seed-41 first_validation_proof does not record C-09 holding")
    validation = None
    copies = ((section.get("hashes") or {}).get("attempt_copies") or {}).get(
        "stage0-rerun-seed41-attempt-02"
    ) or {}
    if "validation.jsonl" in copies:
        validation = reject_escaping_path(
            repo,
            str(ATTEMPTS_REL / "stage0-rerun-seed41-attempt-02" / "validation.jsonl"),
            what="seed41 validation copy",
        )
    elif seed41.get("artifact_dir"):
        validation = reject_escaping_path(
            repo, f"{seed41['artifact_dir']}/validation.jsonl", what="seed41 validation"
        )
    if validation is None or not validation.is_file():
        fail("seed-41 validation.jsonl is missing")
    events = [
        json.loads(line)
        for line in validation.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not events:
        fail("seed-41 validation.jsonl has no events")
    if int(events[0].get("step") or 0) != 100:
        fail("seed-41 first validation event is not step 100")
    payload = validation.read_text(encoding="utf-8")
    if "StageZeroUnderpopulated" in payload:
        fail("seed-41 validation.jsonl still contains StageZeroUnderpopulated")
    trip = reject_escaping_path(
        repo,
        str(ATTEMPTS_REL / "stage0-rerun-seed41-attempt-02" / "failure/trip.json"),
        what="seed41 trip",
    )
    trip_payload = load_json(trip, what="seed41 trip")
    if trip_payload.get("guard") != "invariant_b":
        fail(f"seed-41 trip guard is {trip_payload.get('guard')!r}")
    if int(trip_payload.get("step") or 0) != 501:
        fail(f"seed-41 trip step is {trip_payload.get('step')!r}")
    if trip_payload.get("threshold_provisional") is not False:
        fail("seed-41 trip marks N as provisional")
    if float(trip_payload.get("threshold") or 0) != 500.0:
        fail(f"seed-41 trip threshold is {trip_payload.get('threshold')!r}")
    if trip_payload.get("disposition") != "HALT":
        fail(f"seed-41 trip disposition is {trip_payload.get('disposition')!r}")
    later = [
        record
        for record in ledger["records"]
        if record["band_generation"] == 3
        and record["run_name"] in {"stage0-rerun-seed42", "stage0-rerun-seed43"}
    ]
    if later:
        fail("generation 3 launched seeds 42/43 after the invariant-B HALT")


def cmd_terminal(repo: Path, manifest_rel: str) -> None:
    ledger = load_ledger(repo)
    if ledger.get("final_band_generation") is not None:
        fail(
            f"final_band_generation is {ledger['final_band_generation']!r}; "
            "terminal verification is only for a null final band"
        )
    manifest_path = reject_escaping_path(repo, manifest_rel, what="terminal manifest")
    manifest = load_json(manifest_path, what="terminal-manifest")
    sections = terminal_sections(manifest)
    latest = latest_generation(ledger)
    latest_id = int(latest["band_generation"])
    if latest.get("status") != "terminal":
        fail(f"latest generation {latest_id} status is {latest.get('status')!r}")

    ledger_counts = assert_ledger_hashes(repo, ledger)
    copy_count = 0
    latest_section = None
    for name, section in sections:
        if not section.get("terminal_reason"):
            fail(f"{name} terminal_reason is empty")
        assert_observed_mismatch(section, section=name)
        generation_blob = section.get("generation") or {}
        if generation_blob.get("status") != "terminal":
            fail(f"{name} generation.status is {generation_blob.get('status')!r}")
        is_latest = int(generation_blob.get("band_generation")) == latest_id
        if is_latest:
            latest_section = section
        copy_count += assert_section_hashes(
            repo, ledger, section, name=name, is_latest=is_latest
        )
        assert_failure_tail(repo, ledger, section, name=name)

    if latest_section is None:
        fail(f"terminal-manifest has no section for latest generation {latest_id}")
    if latest_id == 3:
        assert_generation3_reason(repo, ledger, latest_section)

    assert_no_evaluation(repo, ledger)
    assert_no_committed_model_checkpoints(repo)
    assert_no_normal_artifacts(repo)

    print(
        "TERMINAL-EVIDENCE-OK "
        f"generations={len(ledger['band_generations'])} "
        f"records={len(ledger['records'])} "
        f"invocations={ledger_counts['transcripts']} "
        f"attempt_copy_files={copy_count} "
        f"cleanliness={ledger_counts['cleanliness']} "
        f"verify={ledger_counts['verify']}"
    )


def refuse_normal_mode(repo: Path, command: str) -> None:
    ledger = load_ledger(repo)
    if ledger.get("final_band_generation") is None:
        fail(
            f"{command} is a normal-mode verifier; "
            "final_band_generation is null so MANIFEST-OK/BAND-RECORD-OK/"
            "CANDIDATE-OK/PHASE50-EVIDENCE-OK are inapplicable"
        )
    fail(f"{command} is reserved for a generation-complete band")


def cmd_manifest(repo: Path, _manifest: str | None) -> None:
    refuse_normal_mode(repo, "manifest")


def cmd_band(repo: Path) -> None:
    refuse_normal_mode(repo, "band")


def cmd_candidate(repo: Path) -> None:
    refuse_normal_mode(repo, "candidate")


def cmd_all(repo: Path, _manifest: str | None) -> None:
    refuse_normal_mode(repo, "all")


def build_parser() -> argparse.ArgumentParser:
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--repo-root", required=True, type=Path)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    terminal = sub.add_parser("terminal", parents=[parent])
    terminal.add_argument("--manifest", required=True)

    manifest = sub.add_parser("manifest", parents=[parent])
    manifest.add_argument("--manifest", required=False)

    band = sub.add_parser("band", parents=[parent])
    band.add_argument("--source-manifest", required=False)
    band.add_argument("--band-record", required=False)

    candidate = sub.add_parser("candidate", parents=[parent])
    candidate.add_argument("--source-manifest", required=False)
    candidate.add_argument("--band-record", required=False)
    candidate.add_argument("--candidate", required=False)

    everything = sub.add_parser("all", parents=[parent])
    everything.add_argument("--manifest", required=False)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = require_repo(args.repo_root)
    if args.command == "terminal":
        cmd_terminal(repo, args.manifest)
    elif args.command == "manifest":
        cmd_manifest(repo, getattr(args, "manifest", None))
    elif args.command == "band":
        cmd_band(repo)
    elif args.command == "candidate":
        cmd_candidate(repo)
    elif args.command == "all":
        cmd_all(repo, getattr(args, "manifest", None))
    else:
        fail(f"unknown command {args.command}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except VerifyError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(exc.code if isinstance(exc.code, int) else 1)
