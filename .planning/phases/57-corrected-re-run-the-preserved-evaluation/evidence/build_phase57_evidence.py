#!/usr/bin/env python3
"""Phase-57 append-only evidence builder.

The builder carries the Phase-50 evidence shape forward for the v2.3 paths:
``manifest``, ``band``, ``candidate``, and ``finalize`` serialize already
produced run facts but never derive scientific eligibility from metrics.  A
null ``final_band_generation`` is a deliberate pre-run state and refuses all
normal-mode artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Mapping

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

from pinn.verification.candidate_eligibility import (  # noqa: E402
    CANDIDATE_ORDER,
    structural_facts,
)


PHASE_REL = Path(".planning/phases/57-corrected-re-run-the-preserved-evaluation")
EVIDENCE_REL = PHASE_REL / "evidence"
LEDGER_REL = EVIDENCE_REL / "run-ledger.md"
SOURCE_MANIFEST_REL = EVIDENCE_REL / "source-manifest.json"
BAND_RECORD_REL = EVIDENCE_REL / "band-record.md"
CANDIDATE_REL = EVIDENCE_REL / "candidate-receipt.json"
FINAL_MANIFEST_REL = EVIDENCE_REL / "manifest.json"
HEX64 = set("0123456789abcdef")
EVALUATION_NAMES = frozenset({
    "evaluation-attempt.json",
    "evaluation-receipt.json",
    "metrics.json",
    "metrics.md",
})


class BuildError(RuntimeError):
    """Fail-closed evidence-builder error."""


def fail(message: str) -> None:
    raise BuildError(f"build_phase57_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dumps_canonical(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def atomic_write(path: Path, content: str) -> None:
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


def atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    atomic_write(path, dumps_canonical(payload))


def repo_root(raw: str | Path = ".") -> Path:
    root = Path(raw).expanduser().resolve()
    if not (root / ".planning").is_dir():
        fail(f"repository root has no .planning directory: {root}")
    return root


def repo_path(repo: Path, raw: str | Path, *, what: str) -> Path:
    value = str(raw)
    if not value or value.startswith(("/", "~")) or ".." in Path(value).parts:
        fail(f"{what} must be a repository-relative path: {raw!r}")
    resolved = (repo / value).resolve()
    try:
        resolved.relative_to(repo)
    except ValueError:
        fail(f"{what} escapes the repository: {raw!r}")
    if (repo / value).is_symlink():
        fail(f"{what} is a symlink: {raw!r}")
    return resolved


def load_json(path: Path, *, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{what} is unreadable JSON: {path}: {exc}")


def load_ledger(repo: Path) -> dict[str, Any]:
    text = (repo / LEDGER_REL).read_text(encoding="utf-8")
    start = text.find("```json\n")
    if start < 0:
        fail("run-ledger.md has no fenced JSON block")
    start += len("```json\n")
    end = text.find("\n```", start)
    if end < 0:
        fail("run-ledger.md JSON fence is unterminated")
    try:
        ledger = json.loads(text[start:end])
    except json.JSONDecodeError as exc:
        fail(f"run-ledger.md JSON is malformed: {exc}")
    if not isinstance(ledger, dict) or ledger.get("schema") != "phase57-run-ledger/v2":
        fail(f"unexpected Phase-57 ledger schema: {ledger.get('schema') if isinstance(ledger, dict) else None!r}")
    if not isinstance(ledger.get("band_generations"), list) or not isinstance(ledger.get("records"), list):
        fail("run-ledger band_generations and records must be lists")
    return ledger


def assert_no_evaluation(root: Path) -> None:
    if (root / "evaluation").exists():
        fail(f"held-out evaluation directory exists: {root / 'evaluation'}")
    for path in root.rglob("*"):
        if path.is_file() and path.name in EVALUATION_NAMES:
            fail(f"held-out evaluation artifact exists: {path}")


def require_complete_generation(ledger: Mapping[str, Any]) -> tuple[int, dict[str, Any], list[dict[str, Any]]]:
    final = ledger.get("final_band_generation")
    if final is None:
        fail("final_band_generation is null; normal evidence artifacts are not yet authorized")
    try:
        final_id = int(final)
    except (TypeError, ValueError):
        fail(f"final_band_generation is invalid: {final!r}")
    if final_id != 3:
        fail("normal evidence requires the admitted generation-3 band")
    generations = [item for item in ledger["band_generations"] if int(item.get("band_generation", -1)) == final_id]
    if len(generations) != 1:
        fail(f"final generation {final_id} is not uniquely present in the ledger")
    generation = generations[0]
    records = [item for item in ledger["records"] if int(item.get("band_generation", -1)) == final_id]
    graded = [item for item in records if item.get("in_final_band") is True]
    smoke = [item for item in records if item.get("run_name") == "stage0-v23g3-smoke"]
    seeds = sorted(int(item.get("seed")) for item in graded if item.get("seed") is not None)
    if len(records) != 4 or len(smoke) != 1 or len(graded) != 3 or seeds != [41, 42, 43]:
        fail("final generation requires one smoke and finished in-band seeds 41/42/43")
    return final_id, dict(generation), records


def _record_artifact(repo: Path, record: Mapping[str, Any]) -> Path:
    raw = record.get("artifact_dir")
    if not isinstance(raw, str) or not raw:
        fail(f"record {record.get('run_name')!r} has no artifact_dir")
    path = repo_path(repo, raw, what="run artifact")
    if not path.is_dir():
        fail(f"run artifact directory is missing: {path}")
    assert_no_evaluation(path)
    return path


def _record_structural_facts(repo: Path, record: Mapping[str, Any]) -> dict[str, bool]:
    """Re-derive the four Phase-50 facts from run artifacts only."""
    artifact = _record_artifact(repo, record)
    summary = load_json(artifact / "summary.json", what="run summary")
    status = load_json(artifact / "status.json", what="run status")
    validation = summary.get("validation") if isinstance(summary, Mapping) else {}
    if not isinstance(validation, Mapping):
        validation = {}
    sidecar_rel = validation.get("gate_sidecar")
    sidecar_ok = False
    if isinstance(sidecar_rel, str) and sidecar_rel:
        sidecar = repo_path(artifact, sidecar_rel, what="validation sidecar")
        sidecar_ok = sidecar.is_file()
    raw = {
        "eval01_precondition_i": summary.get("eval01_precondition_i") is True,
        "guard_invariant_rule": record.get("final_guard_disposition") in (None, "finished"),
        "finished": (
            record.get("final_process_disposition") == "finished"
            and record.get("ledger_disposition") == "finished"
            and status.get("state") == "finished"
        ),
        "eval01_precondition_iii": validation.get("eval01_precondition_iii") is True and sidecar_ok,
    }
    return structural_facts(raw)


def _hyndman_fan_type7(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def _load_validation_values(artifact: Path, relative: str) -> list[float]:
    path = (artifact / relative).resolve()
    try:
        path.relative_to(artifact.resolve())
    except ValueError:
        fail(f"validation path escapes run artifact: {relative!r}")
    if not path.is_file():
        fail(f"validation artifact is missing: {path}")
    values: list[float] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        value = row.get("eps_h")
        if isinstance(value, str):
            value = {"NaN": float("nan"), "Infinity": float("inf"), "-Infinity": -float("inf")}.get(value, value)
        try:
            values.append(float(value))
        except (TypeError, ValueError):
            fail(f"validation eps_h is not numeric: {value!r}")
    return values


def cmd_manifest(repo: Path) -> None:
    ledger = load_ledger(repo)
    generation_id, generation, records = require_complete_generation(ledger)
    files: dict[str, dict[str, Any]] = {}
    for record in records:
        if not record.get("in_final_band"):
            continue
        artifact = _record_artifact(repo, record)
        for relative in (
            "config.yaml",
            "summary.json",
            "status.json",
            "training_metadata.json",
            "splits.json",
            "validation.jsonl",
        ):
            source = artifact / relative
            if not source.is_file():
                fail(f"required run artifact is missing: {source}")
            source_rel = str(source.relative_to(repo))
            files[source_rel] = {
                "source": source_rel,
                "source_sha256": sha256_file(source),
                "copy_sha256": sha256_file(source),
                "ledger_sha256": (record.get("terminal_artifact_sha256") or {}).get(relative),
                "role": "run-artifact",
            }
            if files[source_rel]["ledger_sha256"] is None:
                files[source_rel]["ledger_sha256"] = files[source_rel]["source_sha256"]
    payload = {
        "schema": "phase57-evidence-source-manifest/v1",
        "band_generation": generation_id,
        "band_git_head": generation.get("git_head"),
        "extraction_git_head": generation.get("extraction_git_head"),
        "files": files,
        "r_ref_artifact_sha256": sha256_file(repo / "pinn/verification/artifacts/r_ref_stage0.json"),
    }
    atomic_json(repo / SOURCE_MANIFEST_REL, payload)
    print("MANIFEST-OK")


def cmd_band(repo: Path) -> None:
    ledger = load_ledger(repo)
    generation_id, _generation, records = require_complete_generation(ledger)
    seeds: dict[str, Any] = {}
    for seed in (41, 42, 43):
        matches = [item for item in records if item.get("in_final_band") and int(item.get("seed")) == seed]
        if len(matches) != 1:
            fail(f"seed {seed} does not have exactly one final-band record")
        record = matches[0]
        artifact = _record_artifact(repo, record)
        summary = load_json(artifact / "summary.json", what="run summary")
        validation = summary.get("validation") or {}
        sidecar_rel = validation.get("gate_sidecar")
        values = _load_validation_values(artifact, sidecar_rel) if isinstance(sidecar_rel, str) else []
        finite = [value for value in values if math.isfinite(value)]
        seeds[str(seed)] = {
            "run_name": record.get("run_name"),
            "quantiles": {
                "p10": _hyndman_fan_type7(finite, 0.10),
                "p50": _hyndman_fan_type7(finite, 0.50),
                "p90": _hyndman_fan_type7(finite, 0.90),
                "nonfinite_count": len(values) - len(finite),
            },
            "gate": {
                "eval01_precondition_iii": validation.get("eval01_precondition_iii"),
                "gate_sidecar": sidecar_rel,
                "gate_verdict": validation.get("gate_verdict"),
            },
        }
    payload = {
        "schema": "phase57-band-record/v1",
        "band_generation": generation_id,
        "n": 3,
        "variation_label": "compound descriptive n=3 variation; no ranking or causal inference",
        "seeds": seeds,
    }
    narrative = "# Phase 57 Band Record\n\nDescriptive three-seed characterization. This record does not rank seeds or infer causes.\n\n```json\n" + dumps_canonical(payload).rstrip() + "\n```\n"
    atomic_write(repo / BAND_RECORD_REL, narrative)
    print("BAND-RECORD-OK")


def cmd_candidate(repo: Path) -> None:
    ledger = load_ledger(repo)
    terminal_path = repo / EVIDENCE_REL / "terminal-state.json"
    if terminal_path.is_file():
        terminal = load_json(terminal_path, what="terminal state")
        if terminal.get("status") == "terminal" and terminal.get("authorized_terminal_reason") in {
            "gate04_block",
            "invariant_b_halt_no_advance",
        }:
            payload = {
                "schema": "phase57-no-candidate/v1",
                "reason": terminal["authorized_terminal_reason"],
                "owner_stop": True,
                "evaluation": "preserved-unspent",
                "terminal_state_sha256": sha256_file(terminal_path),
            }
            atomic_json(repo / EVIDENCE_REL / "no-candidate.json", payload)
            print("NO-CANDIDATE-OK")
            return
        if terminal.get("status") != "terminal":
            fail("terminal-state.json exists but is not an authorized terminal closure")
    generation_id, generation, records = require_complete_generation(ledger)
    band_records = [item for item in records if item.get("in_final_band")]
    by_seed: dict[str, dict[str, bool]] = {}
    for record in band_records:
        facts = _record_structural_facts(repo, record)
        by_seed[str(int(record["seed"]))] = facts
    selected = None
    for seed in CANDIDATE_ORDER:
        facts = by_seed.get(str(seed))
        if facts and facts.get("eligible") is True:
            selected = seed
            break
    receipt: dict[str, Any] = {
        "schema": "phase57-candidate-receipt/v1",
        "band_generation": generation_id,
        "band_git_head": generation.get("git_head"),
        "order": list(CANDIDATE_ORDER),
        "facts": by_seed,
        "evaluation": "preserved-unspent",
        "owner_stop": selected is None,
        "run_name": None,
    }
    if selected is not None:
        matching = next(item for item in band_records if int(item.get("seed")) == selected)
        artifact = _record_artifact(repo, matching)
        checkpoint = artifact / "checkpoints" / "best.pt"
        if not checkpoint.is_file():
            fail(f"selected candidate best.pt is missing: {checkpoint}")
        receipt.update(
            {
                "run_name": matching.get("run_name"),
                "seed": selected,
                "artifact_dir": str(artifact.relative_to(repo)),
                "candidate_best_path": str(checkpoint.relative_to(repo)),
                "candidate_best_sha256": sha256_file(checkpoint),
                "owner_stop": False,
            }
        )
    atomic_json(repo / CANDIDATE_REL, receipt)
    print("CANDIDATE-OK")


def cmd_finalize(repo: Path) -> None:
    ledger = load_ledger(repo)
    require_complete_generation(ledger)
    paths = [SOURCE_MANIFEST_REL, BAND_RECORD_REL, CANDIDATE_REL]
    files: dict[str, str] = {}
    for relative in paths:
        path = repo / relative
        if not path.is_file():
            fail(f"finalize requires {path}")
        files[str(relative)] = sha256_file(path)
    payload = {"schema": "phase57-evidence-manifest/v1", "files": files}
    atomic_json(repo / FINAL_MANIFEST_REL, payload)
    print("FINAL-MANIFEST-OK")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("manifest", "band", "candidate", "finalize"):
        sub.add_parser(name)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = repo_root(args.repo_root)
        {
            "manifest": cmd_manifest,
            "band": cmd_band,
            "candidate": cmd_candidate,
            "finalize": cmd_finalize,
        }[args.command](root)
    except Exception as exc:  # noqa: BLE001 - fail closed at CLI boundary
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
