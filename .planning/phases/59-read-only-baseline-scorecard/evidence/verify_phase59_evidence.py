#!/usr/bin/env python3
"""Phase 59: the independent evidence verifier for the read-only baseline.

Fail-closed checks for the frozen scorecard, area manifests, and guardrails.
This script does not import evidence_io or any producing tool's helpers.
Re-derivation, when a later subcommand asks for it, is a subprocess --check.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
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
    g1_fires,
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
                fail(f"frozen file is dirty: {relative} sha256")
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


REDERIVE = {
    "audit": (["-m", "pinn.verification.stage0_census", "--acceptance", "--check"], "AUDIT-CHECK-OK"),
    "census": (["-m", "pinn.verification.stage0_census", "--check"], "CENSUS-CHECK-OK"),
    "survey": (["-m", "pinn.verification.dataset_survey", "--check"], "SURVEY-CHECK-OK"),
    "baselines": (["-m", "pinn.verification.baselines", "--check"], "BASELINES-CHECK-OK"),
}
_DIAG_FILES = {
    "jx01": "jx01.json",
    "jx02": "jx02.json",
    "jx03": "jx03.json",
    "jx04": "jx04.json",
    "jx05": "jx05.json",
    "jx10": "jx10.json",
    "g1": "g1.json",
}
_JX_KEYS = (
    "experiment", "plain_language", "command", "code_identity", "runtimes",
    "checkpoints", "scorecard_sha256", "results", "reading", "tolerance_checks",
    "memory", "non_interference", "files_opened",
)
_RETENTION_REL = Path(
    ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-7-retention.json"
)


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _file_map(root_dir: Path, *, skip_top: str) -> dict[str, dict[str, Any]]:
    files: dict[str, dict[str, Any]] = {}
    if not root_dir.is_dir():
        return files
    for path in sorted(root_dir.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root_dir)
        name = relative.as_posix()
        if name == skip_top or "__pycache__" in relative.parts or "logs" in relative.parts:
            continue
        raw = path.read_bytes()
        files[name] = {"sha256": sha256_bytes(raw), "size_bytes": len(raw)}
    return files


def _manifest_path(area: str) -> Path:
    if area == "all":
        return REPO_ROOT / EVIDENCE_REL / "manifest.json"
    return REPO_ROOT / EVIDENCE_REL / area / "MANIFEST.json"


def _area_name(raw: Optional[str]) -> str:
    if raw not in (*AREAS, "all"):
        fail(f"unknown area {raw}")
    return str(raw)


def _write_manifest(area: str) -> None:
    freeze_commit = assert_scorecard_frozen()
    head = _rev_parse("HEAD")
    if area == "all":
        payload = {
            "schema": "phase59-evidence-manifest/v1",
            "freeze_commit": freeze_commit,
            "produced_at_head": head,
            "scorecard_sha256": SCORECARD_SHA256,
            "files": _file_map(REPO_ROOT / EVIDENCE_REL, skip_top="manifest.json"),
        }
    else:
        payload = {
            "schema": "phase59-area-manifest/v1",
            "area": area,
            "freeze_commit": freeze_commit,
            "produced_at_head": head,
            "scorecard_sha256": SCORECARD_SHA256,
            "files": _file_map(REPO_ROOT / EVIDENCE_REL / area, skip_top="MANIFEST.json"),
        }
    _atomic_json(_manifest_path(area), payload)


def _check_manifest(area: str) -> dict[str, Any]:
    path = _manifest_path(area)
    if not path.is_file():
        fail(f"missing file {path.name}")
    record = load_json(path, what=path.name)
    if not isinstance(record, Mapping):
        fail(f"{path.name} is not an object")
    freeze_commit = first_commit_of(FREEZE_REL.as_posix())
    if record.get("freeze_commit") != freeze_commit:
        fail(f"manifest freeze_commit {record.get('freeze_commit')} != {freeze_commit}")
    produced = str(record.get("produced_at_head") or "")
    if not produced or not is_ancestor(freeze_commit, produced):
        fail(
            f"manifest produced_at_head {produced} is not a descendant of "
            f"freeze commit {freeze_commit}"
        )
    expected = record.get("files")
    if not isinstance(expected, Mapping):
        fail("manifest files is not an object")
    if area == "all":
        actual = _file_map(REPO_ROOT / EVIDENCE_REL, skip_top="manifest.json")
    else:
        actual = _file_map(REPO_ROOT / EVIDENCE_REL / area, skip_top="MANIFEST.json")
    for name in sorted(set(expected) | set(actual)):
        if name not in actual:
            fail(f"missing file {name}")
        if name not in expected:
            fail(f"extra file {name}")
        want = expected[name]
        got = actual[name]
        if got["sha256"] != want.get("sha256") or got["size_bytes"] != want.get("size_bytes"):
            fail(f"changed file {name}")
    return dict(record)


def cmd_manifest(args: argparse.Namespace) -> None:
    area = _area_name(args.area)
    if args.write:
        _write_manifest(area)
    else:
        assert_scorecard_frozen()
        _check_manifest(area)
    print(f"MANIFEST-{area.upper()}-OK")


def _result_paths(area: str) -> list[Path]:
    directory = REPO_ROOT / EVIDENCE_REL / area
    if not directory.is_dir():
        return []
    found = []
    for path in sorted(directory.glob("*.json")):
        name = path.name
        if (
            name == "MANIFEST.json"
            or name.startswith("provenance")
            or name.startswith("files_opened")
            or name.endswith(".done.json")
        ):
            continue
        found.append(path)
    return found


def _check_result(path: Path) -> dict[str, Any]:
    payload = load_json(path, what=path.name)
    if not isinstance(payload, Mapping):
        fail(f"{path.name} is not an object")
    if not str(payload.get("schema") or "").startswith("phase59-"):
        fail(f"{path.name} schema does not start with phase59-")
    if not str(payload.get("plain_language") or ""):
        fail(f"{path.name} plain_language is empty")
    if "scorecard_sha256" in payload and payload["scorecard_sha256"] != SCORECARD_SHA256:
        fail(f"{path.name} scorecard_sha256 != {SCORECARD_SHA256}")
    producers = payload.get("producer_sha256")
    if not isinstance(producers, Mapping) or not producers:
        fail(f"{path.name} producer_sha256 is missing")
    for relative, digest in producers.items():
        current = sha256_file(repo_path(str(relative), what=str(relative)))
        if current != digest:
            fail(f"{path.name} producer_sha256 does not match {relative}")
    return dict(payload)


def _check_opened(area: str) -> None:
    directory = REPO_ROOT / EVIDENCE_REL / area
    if not directory.is_dir():
        return
    for path in sorted(directory.glob("files_opened*.json")):
        payload = load_json(path, what=path.name)
        for key in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            if payload.get(key) != 0:
                fail(f"{path.name} {key} is not 0")


def _check_markers(area: str, results: Sequence[Path]) -> None:
    directory = REPO_ROOT / EVIDENCE_REL / area
    markers = []
    for path in sorted(directory.glob("*.done.json")):
        payload = load_json(path, what=path.name)
        if isinstance(payload, Mapping):
            markers.append(payload)
    for result in results:
        name = result.name
        digest = sha256_file(result)
        covers = [
            marker for marker in markers
            if isinstance(marker.get("result_files"), Mapping) and name in marker["result_files"]
        ]
        if not covers:
            fail(f"completion marker missing for {name}")
        matched = [
            marker for marker in covers
            if marker.get("status") == "complete" and marker["result_files"].get(name) == digest
        ]
        if matched:
            continue
        if not any(marker.get("status") == "complete" for marker in covers):
            fail(f"completion marker status is not complete for {name}")
        fail(f"completion marker hash does not match {name}")


def _require_committed(area: str, manifest: Mapping[str, Any]) -> None:
    freeze_commit = str(manifest.get("freeze_commit"))
    base = f"{EVIDENCE_REL.as_posix()}/{area}"
    relatives = [f"{base}/{name}" for name in manifest.get("files", {})]
    relatives.append(f"{base}/MANIFEST.json")
    for relative in relatives:
        if not is_tracked(relative) or not is_clean(relative):
            fail(f"{relative} is not tracked and clean")
        first = first_commit_of(relative)
        if first == freeze_commit or not is_ancestor(freeze_commit, first):
            fail(f"{relative} first commit is not a strict descendant of the freeze commit")
    last = _git("log", "-1", "--format=%H", "--", f"{base}/MANIFEST.json").stdout.strip()
    produced = str(manifest.get("produced_at_head") or "")
    if not last or not is_ancestor(produced, last):
        fail(f"manifest produced_at_head {produced} is not an ancestor of {last}")


def _rederive(area: str) -> None:
    if area not in REDERIVE:
        return
    tail, token = REDERIVE[area]
    proc = subprocess.run(
        [sys.executable, "-B", *list(tail)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=1800,
        check=False,
    )
    if proc.returncode != 0:
        fail(f"{area} re-derivation exited {proc.returncode}")
    if token not in proc.stdout:
        fail(f"{area} re-derivation did not print {token}")


def _retention() -> dict[str, Mapping[str, Any]]:
    payload = load_json(repo_path(_RETENTION_REL, what="generation-7 retention"), what="generation-7 retention")
    files = payload.get("files") if isinstance(payload, Mapping) else None
    if not isinstance(files, list):
        fail("generation-7 retention files is not a list")
    return {
        str(entry["path"]): entry
        for entry in files
        if isinstance(entry, Mapping) and isinstance(entry.get("path"), str)
    }


def _check_audit() -> None:
    area = REPO_ROOT / EVIDENCE_REL / "audit"
    audit = load_json(area / "reader_acceptance.json", what="reader acceptance")
    card = load_scorecard()
    retained = _retention().get("runs/stage0-v23g7-seed42/splits.json")
    if retained is None or audit.get("splits", {}).get("sha256") != retained.get("sha256"):
        fail("splits sha256 does not match generation-7 retention")
    monitor = audit["monitor_batch_reproduction"]
    if monitor.get("passed") is not True:
        fail("monitor_batch_reproduction.passed is false")
    for key in ("mismatches_targets", "mismatches_times", "mismatches_masses"):
        if monitor.get(key) != 0:
            fail(f"monitor {key} is not 0")
    tolerance = float(card.section("diag07")["tolerances"]["monitor_reproduction_ic13_abs"])
    if float(monitor["ic13_max_abs"]) > tolerance:
        fail("ic13_max_abs exceeds the scorecard tolerance")
    normalizer = audit["normalizer"]
    limit = float(card.section("diag07")["tolerances"]["normalizer_recovery_max_abs"])
    if float(normalizer["max_abs_residual"]) > limit and normalizer.get("deviation") is not True:
        fail("normalizer residual exceeds tolerance without deviation true")


def _check_census() -> None:
    area = REPO_ROOT / EVIDENCE_REL / "census"
    census = load_json(area / "census.json", what="census")
    panels = load_json(area / "panels.json", what="panels")
    population = census.get("population") or {}
    if population.get("train") != 1812 or population.get("validation") != 227:
        fail("population is not train 1812 and validation 227")
    checks = census.get("checks") or {}
    if checks.get("pair_tracking_failures") != 0:
        fail("pair_tracking_failures is not 0")
    limit = float(load_scorecard().section("scoring_grid")["gold_base_agreement_max"])
    if float(checks.get("gold_base_max_deviation")) > limit:
        fail("gold_base_max_deviation exceeds the scorecard")
    if _plain(panels.get("rule")) != _plain(load_scorecard().section("panel_rule")):
        fail("panels rule differs from the scorecard panel_rule")
    digest = sha256_file(area / "census.csv")
    if panels.get("census_csv_sha256") != digest or census.get("census_csv_sha256") != digest:
        fail("census_csv_sha256 does not match census.csv")
    singles = [row["id"] for row in panels["singles"]]
    family = [row["id"] for row in panels["family"]]
    validation = list(panels["validation"])
    if len(set(singles)) != 3:
        fail("singles are not 3 distinct ids")
    if len(family) != 16 or len(set(family)) != 16:
        fail("family is not 16 distinct ids")
    if set(singles) & set(family):
        fail("family ids overlap singles")
    if len(validation) != 227 or len(set(validation)) != 227:
        fail("validation panel is not 227 distinct ids")


def _pick_ok(entry: Any) -> bool:
    if not isinstance(entry, Mapping):
        return False
    if "no_pick" in entry:
        return isinstance(entry.get("no_pick"), str) and bool(entry.get("no_pick"))
    return (
        isinstance(entry.get("rule"), str)
        and bool(entry.get("rule"))
        and "record" in entry
        and "value" in entry
        and "sensitivity" in entry
    )


def _check_survey() -> None:
    area = REPO_ROOT / EVIDENCE_REL / "survey"
    survey = load_json(area / "survey.json", what="survey")
    picks = load_json(area / "picks.json", what="picks")
    if survey.get("schema") != "phase59-survey/v1":
        fail("survey.json schema is not phase59-survey/v1")
    if picks.get("schema") != "phase59-feas09-picks/v1":
        fail("picks.json schema is not phase59-feas09-picks/v1")
    for name in ("stage4b", "stage6"):
        if not _pick_ok(picks.get(name)):
            fail(f"picks {name} is not a ruled record or a no_pick reason")


def _training_ids() -> set[int]:
    path = REPO_ROOT / EVIDENCE_REL / "census" / "census.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return {int(row["id"]) for row in csv.DictReader(handle)}


def _check_baselines() -> None:
    area = REPO_ROOT / EVIDENCE_REL / "baselines"
    two = load_json(area / "two_kepler.json", what="two kepler")
    copied = load_json(area / "nn_copy.json", what="nn copy")
    summary = load_json(area / "baselines.json", what="baselines")
    panels = load_json(REPO_ROOT / EVIDENCE_REL / "census" / "panels.json", what="panels")
    panel_ids = {row["id"] for row in panels["singles"]}
    panel_ids.update(row["id"] for row in panels["family"])
    panel_ids.update(panels["validation"])
    if not panel_ids <= set(two.get("ids") or []):
        fail("two_kepler.json does not cover every panel id")
    rows = copied.get("rows")
    if not isinstance(rows, list) or len(rows) != 227:
        fail("nn_copy.json does not have 227 rows")
    training = _training_ids()
    for row in rows:
        if int(row["neighbour_id"]) not in training:
            fail("nn_copy neighbour id is outside the census training ids")
    if "feas09" not in summary:
        fail("baselines.json has no feas09 entry")


def _check_diag07(require: Optional[str]) -> None:
    directory = REPO_ROOT / EVIDENCE_REL / "diag07"
    if require:
        names = list(_DIAG_FILES) if require.strip() == "all" else [
            part.strip() for part in require.split(",") if part.strip()
        ]
        for name in names:
            filename = _DIAG_FILES.get(name, name if name.endswith(".json") else f"{name}.json")
            if not (directory / filename).is_file():
                fail(f"required diag07 file is absent: {filename}")
    retained: Optional[dict[str, Mapping[str, Any]]] = None
    for path in sorted(directory.glob("jx*.json")):
        if path.name.endswith(".done.json"):
            continue
        payload = load_json(path, what=path.name)
        for key in _JX_KEYS:
            if key not in payload:
                fail(f"{path.name} missing {key}")
        if payload["code_identity"].get("commit") != load_scorecard().section("diag07")["code_commit"]:
            fail(f"{path.name} code_identity.commit is not the scorecard diag07.code_commit")
        if retained is None:
            retained = _retention()
        for checkpoint in payload["checkpoints"]:
            entry = retained.get(str(checkpoint.get("path")))
            if entry is None or entry.get("sha256") != checkpoint.get("sha256"):
                fail(f"{path.name} checkpoint sha256 does not match generation-7 retention")
        interference = payload["non_interference"]
        for key in ("parameters_unchanged", "grads_none", "optimizer_constructed", "runs_hashes_unchanged"):
            if interference.get(key) is not True:
                fail(f"{path.name} non_interference.{key} is not true")
        if interference.get("checkpoint_writes") != 0:
            fail(f"{path.name} non_interference.checkpoint_writes is not 0")
    g1_path = directory / "g1.json"
    if g1_path.is_file():
        gate = load_json(g1_path, what="g1")
        shares = {int(key): value for key, value in gate["primary_share"].items()}
        expected = g1_fires(shares, scorecard=load_scorecard())
        if gate.get("fires") != expected["fires"] or gate.get("outcome") != expected["outcome"]:
            fail(f"g1_fires recomputed fires {expected['fires']} outcome {expected['outcome']!r}")


def _run_area(area: str, args: argparse.Namespace, specific) -> None:
    assert_scorecard_frozen()
    manifest = _check_manifest(area)
    results = _result_paths(area)
    for path in results:
        _check_result(path)
    _check_opened(area)
    if area in ("survey", "diag07"):
        _check_markers(area, results)
    if args.require_committed:
        _require_committed(area, manifest)
    specific(args)
    if not args.skip_rederive:
        _rederive(area)


def cmd_audit(args: argparse.Namespace) -> None:
    _run_area("audit", args, lambda _args: _check_audit())
    print("AUDIT-OK")


def cmd_census(args: argparse.Namespace) -> None:
    _run_area("census", args, lambda _args: _check_census())
    print("CENSUS-OK")


def cmd_survey(args: argparse.Namespace) -> None:
    _run_area("survey", args, lambda _args: _check_survey())
    print("SURVEY-OK")


def cmd_baselines(args: argparse.Namespace) -> None:
    _run_area("baselines", args, lambda _args: _check_baselines())
    print("BASELINES-OK")


def cmd_diag07(args: argparse.Namespace) -> None:
    _run_area("diag07", args, lambda received: _check_diag07(received.require))
    print("DIAG07-OK")


COMMANDS = {
    "scorecard-frozen": cmd_scorecard_frozen,
    "manifest": cmd_manifest,
    "audit": cmd_audit,
    "census": cmd_census,
    "survey": cmd_survey,
    "baselines": cmd_baselines,
    "diag07": cmd_diag07,
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
