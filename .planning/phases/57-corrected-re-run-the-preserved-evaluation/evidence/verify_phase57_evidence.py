#!/usr/bin/env python3
"""Independent verifier for the Phase-57 run/evaluation evidence chain.

Subcommands mirror the remaining execution gates: ``admit-run-window``,
``run-window``, ``candidate``, ``pre-evaluation``, and ``final``.  The checks
are intentionally fail-closed and do not import builder derivation helpers.
Scientific metrics are never used to choose a candidate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

from pinn.verification.candidate_eligibility import (  # noqa: E402
    CANDIDATE_ORDER,
    REQUIRED_STRUCTURAL_FACTS,
    TERMINAL_OUTCOMES,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
PHASE_REL = Path(".planning/phases/57-corrected-re-run-the-preserved-evaluation")
EVIDENCE_REL = PHASE_REL / "evidence"
LEDGER_REL = EVIDENCE_REL / "run-ledger.md"
GATE_ROOT = EVIDENCE_REL / "gate04"
R_REF_REL = Path("pinn/verification/artifacts/r_ref_stage0.json")
CONFORMANCE_REL = EVIDENCE_REL / "production-conformance.json"
GATE_SCHEMA = "phase56-gate04-cli-evidence/v1"
LEDGER_SCHEMA = "phase57-run-ledger/v2"
RETENTION_REL = EVIDENCE_REL / "generation-2-retention.json"
G5_RETENTION_REL = EVIDENCE_REL / "generation-5-retention.json"
HISTORICAL_BLOCKED_STATE_REL = EVIDENCE_REL / "blocked-state.json"
CURRENT_BLOCKED_STATE_REL = EVIDENCE_REL / "blocked-state-g6.json"
FINAL_GENERATION = 6
FINAL_RUN_NAMES = frozenset({
    "stage0-v23g6-smoke",
    "stage0-v23g6-seed41",
    "stage0-v23g6-seed42",
    "stage0-v23g6-seed43",
})
FINAL_LAUNCH_ORDER = (
    "stage0-v23g6-smoke", "stage0-v23g6-seed42",
    "stage0-v23g6-seed41", "stage0-v23g6-seed43",
)
EVALUATION_NAMES = frozenset({
    "evaluation-attempt.json",
    "evaluation-receipt.json",
    "metrics.json",
    "metrics.md",
})
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class VerifyError(RuntimeError):
    """Fail-closed evidence verification error."""


def fail(message: str) -> None:
    raise VerifyError(f"verify_phase57_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_path(raw: str | Path, *, what: str, root: Path | None = None) -> Path:
    root = REPO_ROOT if root is None else root
    value = str(raw)
    supplied = Path(value)
    resolved = (root / supplied).resolve() if not supplied.is_absolute() else supplied.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        fail(f"{what} escapes the repository: {raw!r}")
    if (root / supplied).is_symlink() if not supplied.is_absolute() else False:
        fail(f"{what} is a symlink: {raw!r}")
    return resolved


def load_json(path: Path, *, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{what} is unreadable JSON: {path}: {exc}")


def load_ledger() -> dict[str, Any]:
    path = REPO_ROOT / LEDGER_REL
    if not path.is_file():
        fail(f"run ledger is missing: {path}")
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", text, re.S)
    if match is None:
        fail("run-ledger.md has no fenced JSON block")
    ledger = json.loads(match.group(1))
    if not isinstance(ledger, dict) or ledger.get("schema") != LEDGER_SCHEMA:
        fail(f"unexpected run ledger schema: {ledger.get('schema') if isinstance(ledger, dict) else None!r}")
    if not isinstance(ledger.get("band_generations"), list) or not isinstance(ledger.get("records"), list):
        fail("run ledger band_generations/records are not lists")
    for record in ledger["records"]:
        if not isinstance(record, Mapping) or not isinstance(record.get("invocations"), list) or not record["invocations"]:
            fail("version-2 run ledger record lacks invocations")
    return ledger


def assert_generation_two_retained() -> None:
    """Re-derive the owner-approved historical retention claim from Git and disk."""
    manifest = load_json(REPO_ROOT / RETENTION_REL, what="generation-2 retention manifest")
    if not isinstance(manifest, Mapping) or manifest.get("run_name") != "stage0-v23g2-smoke":
        fail("generation-2 retention manifest has the wrong run identity")
    entries = manifest.get("files")
    if not isinstance(entries, list) or len(entries) != 16 or manifest.get("file_count") != 16:
        fail("generation-2 retention manifest must enumerate exactly 16 files")
    tracked_result = subprocess.run(
        ["git", "ls-files", "--cached", "--", "runs/stage0-v23g2-smoke"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, check=False,
    )
    if tracked_result.returncode != 0:
        fail("cannot verify generation-2 tracked artifact paths")
    tracked = set(tracked_result.stdout.splitlines())
    observed: set[str] = set()
    total_bytes = 0
    for entry in entries:
        if not isinstance(entry, Mapping):
            fail("generation-2 retention entry is not a mapping")
        relative = entry.get("path")
        digest = entry.get("sha256")
        size = entry.get("size_bytes")
        if not isinstance(relative, str) or not relative.startswith("runs/stage0-v23g2-smoke/"):
            fail("generation-2 retention entry has an invalid path")
        if relative in observed or not isinstance(digest, str) or not HEX64.fullmatch(digest):
            fail(f"generation-2 retention entry is duplicate or lacks SHA-256: {relative}")
        if not isinstance(size, int) or size < 0:
            fail(f"generation-2 retention entry lacks a byte size: {relative}")
        path = repo_path(relative, what="generation-2 retained artifact")
        if not path.is_file() or path.stat().st_size != size or sha256_file(path) != digest:
            fail(f"generation-2 retained artifact differs from manifest: {relative}")
        observed.add(relative)
        total_bytes += size
    if observed != tracked or total_bytes != manifest.get("total_bytes"):
        fail("generation-2 retained paths or total bytes differ from the committed manifest")


def assert_generation_one_blocked_state_retained(ledger: Mapping[str, Any]) -> None:
    """Keep the tracked generation-1 blocked evidence byte-for-byte stable."""
    records = [
        record for record in ledger.get("records", [])
        if isinstance(record, Mapping) and record.get("band_generation") == 1
    ]
    if len(records) != 1:
        fail("run ledger must contain exactly one generation-1 record")
    record = records[0]
    expected_path = record.get("blocked_state_path")
    expected_digest = record.get("blocked_state_sha256")
    if expected_path != str(HISTORICAL_BLOCKED_STATE_REL):
        fail("generation-1 blocked-state path no longer points to the historical file")
    if not isinstance(expected_digest, str) or not HEX64.fullmatch(expected_digest):
        fail("generation-1 blocked-state ledger digest is invalid")
    path = REPO_ROOT / HISTORICAL_BLOCKED_STATE_REL
    if not path.is_file() or sha256_file(path) != expected_digest:
        fail("generation-1 blocked-state bytes differ from the ledger")


def assert_generation_three_blocked_state_retained(ledger: Mapping[str, Any]) -> None:
    """Keep the sandbox-blocked generation-3 retry attempt append-only."""
    generations = [
        generation for generation in ledger.get("band_generations", [])
        if isinstance(generation, Mapping) and generation.get("band_generation") == 3
    ]
    if len(generations) != 1 or generations[0].get("status") != "blocked":
        fail("run ledger must retain one blocked generation-3 header")
    records = [
        record for record in ledger.get("records", [])
        if isinstance(record, Mapping) and record.get("band_generation") == 3
    ]
    if len(records) != 1 or records[0].get("run_name") != "stage0-v23g3-smoke":
        fail("run ledger must retain the generation-3 sandbox smoke record")
    record = records[0]
    path_value = record.get("blocked_state_path")
    digest = record.get("blocked_state_sha256")
    if path_value != str(EVIDENCE_REL / "blocked-state-g3.json"):
        fail("generation-3 blocked-state path changed unexpectedly")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        fail("generation-3 blocked-state ledger digest is invalid")
    path = REPO_ROOT / path_value
    if not path.is_file() or sha256_file(path) != digest:
        fail("generation-3 blocked-state bytes differ from the ledger")
    _assert_invocations(record, record.get("git_head"))


def assert_generation_four_blocked_state_retained(ledger: Mapping[str, Any]) -> None:
    """Keep the non-resumable generation-4 operator stop append-only."""
    generations = [
        generation for generation in ledger.get("band_generations", [])
        if isinstance(generation, Mapping) and generation.get("band_generation") == 4
    ]
    if len(generations) != 1 or generations[0].get("status") != "blocked":
        fail("run ledger must retain one blocked generation-4 header")
    records = [
        record for record in ledger.get("records", [])
        if isinstance(record, Mapping) and record.get("band_generation") == 4
    ]
    if len(records) != 1 or records[0].get("run_name") != "stage0-v23g4-smoke":
        fail("run ledger must retain the generation-4 operator-stop smoke record")
    record = records[0]
    path_value = record.get("blocked_state_path")
    digest = record.get("blocked_state_sha256")
    if path_value != str(EVIDENCE_REL / "blocked-state-g4.json"):
        fail("generation-4 blocked-state path changed unexpectedly")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        fail("generation-4 blocked-state ledger digest is invalid")
    path = REPO_ROOT / path_value
    if not path.is_file() or sha256_file(path) != digest:
        fail("generation-4 blocked-state bytes differ from the ledger")
    blocked = load_json(path, what="generation-4 blocked state")
    if (
        blocked.get("band_generation") != 4
        or blocked.get("run_name") != "stage0-v23g4-smoke"
        or blocked.get("evaluation") != "preserved-unspent"
        or blocked.get("terminal") is not False
    ):
        fail("generation-4 blocked-state identity or disposition is invalid")
    ledger_hashes = record.get("artifact_hashes")
    blocked_hashes = blocked.get("run_artifact_hashes")
    if not isinstance(ledger_hashes, Mapping) or not isinstance(blocked_hashes, Mapping):
        fail("generation-4 blocked-state artifact hashes are missing")
    if dict(ledger_hashes) != dict(blocked_hashes):
        fail("generation-4 blocked-state and ledger artifact hashes differ")
    artifact_dir = repo_path(record.get("artifact_dir"), what="generation-4 retained artifact")
    observed = {
        str(file.relative_to(artifact_dir)): sha256_file(file)
        for file in sorted(artifact_dir.rglob("*"))
        if file.is_file()
    }
    if observed != dict(blocked_hashes):
        fail("generation-4 retained artifact bytes differ from the blocked-state hashes")
    source_config = repo_path(record.get("config_path"), what="generation-4 source config")
    if blocked.get("config", {}).get("source_sha256") != sha256_file(source_config):
        fail("generation-4 blocked-state source config digest is stale")
    _assert_invocations(record, record.get("git_head"))


def assert_generation_five_retained(ledger: Mapping[str, Any]) -> None:
    """Re-derive the completed generation-5 smoke retention from Git and disk."""
    manifest = load_json(REPO_ROOT / G5_RETENTION_REL, what="generation-5 retention manifest")
    if (
        not isinstance(manifest, Mapping)
        or manifest.get("schema") != "phase57-generation-retention/v1"
        or manifest.get("band_generation") != 5
        or manifest.get("run_name") != "stage0-v23g5-smoke"
        or manifest.get("file_count") != 25
        or manifest.get("run_file_count") != 23
    ):
        fail("generation-5 retention manifest identity or counts differ")
    entries = manifest.get("files")
    if not isinstance(entries, list) or len(entries) != 25:
        fail("generation-5 retention manifest must enumerate 25 files")
    expected_snapshots = {
        "timing-calibration": (
            EVIDENCE_REL / "generation-5-timing-calibration.json",
            "runs/.calibration/stage0-timing.json",
        ),
        "verify-marker": (
            EVIDENCE_REL / "generation-5-verify-marker.json",
            "runs/.verify/latest-marker.json",
        ),
    }
    observed_paths: set[str] = set()
    run_hashes: dict[str, str] = {}
    snapshot_roles: set[str] = set()
    total_bytes = 0
    run_dir = REPO_ROOT / "runs/stage0-v23g5-smoke"
    for entry in entries:
        if not isinstance(entry, Mapping):
            fail("generation-5 retention entry is not a mapping")
        relative, role = entry.get("path"), entry.get("role")
        digest, size = entry.get("sha256"), entry.get("size_bytes")
        if (
            not isinstance(relative, str) or relative in observed_paths
            or not isinstance(digest, str) or not HEX64.fullmatch(digest)
            or type(size) is not int or size < 0
        ):
            fail("generation-5 retention entry has duplicate or invalid path, size, or SHA-256")
        if role == "run-artifact":
            if not relative.startswith("runs/stage0-v23g5-smoke/"):
                fail("generation-5 run artifact escaped its directory")
            run_hashes[relative.removeprefix("runs/stage0-v23g5-smoke/")] = digest
        elif role in expected_snapshots:
            expected_path, original = expected_snapshots[role]
            if relative != str(expected_path) or entry.get("original_path") != original:
                fail("generation-5 snapshot path or source changed")
            snapshot_roles.add(role)
        else:
            fail("generation-5 retention entry has an unknown role")
        path = repo_path(relative, what="generation-5 retained artifact")
        if not path.is_file() or path.stat().st_size != size or sha256_file(path) != digest:
            fail(f"generation-5 retained artifact bytes differ from manifest: {relative}")
        observed_paths.add(relative)
        total_bytes += size
    if len(run_hashes) != 23 or snapshot_roles != set(expected_snapshots):
        fail("generation-5 retention manifest lacks exact run/snapshot roles")
    disk_run_paths = {
        str(path.relative_to(REPO_ROOT))
        for path in run_dir.rglob("*") if path.is_file()
    }
    if disk_run_paths != {path for path in observed_paths if path.startswith("runs/")}:
        fail("generation-5 run directory contains missing or extra artifacts")
    if total_bytes != manifest.get("total_bytes"):
        fail("generation-5 retained total bytes differ from manifest")
    tracked_result = subprocess.run(
        ["git", "ls-files", "--cached", "--", str(run_dir.relative_to(REPO_ROOT)),
         *(str(value[0]) for value in expected_snapshots.values())],
        cwd=str(REPO_ROOT), capture_output=True, text=True, check=False,
    )
    if tracked_result.returncode != 0 or set(tracked_result.stdout.splitlines()) != observed_paths:
        fail("generation-5 retained paths differ from committed Git paths")
    generations = [g for g in ledger["band_generations"] if g.get("band_generation") == 5]
    records = [r for r in ledger["records"] if r.get("band_generation") == 5]
    if (
        len(generations) != 1 or generations[0].get("status") != "historical-complete-smoke"
        or generations[0].get("retention_manifest") != str(G5_RETENTION_REL)
        or len(records) != 1 or records[0].get("run_name") != "stage0-v23g5-smoke"
    ):
        fail("generation-5 completed smoke is not historical in the run ledger")
    record = records[0]
    if (
        record.get("artifact_hashes") != run_hashes
        or record.get("in_final_band") is not False
        or record.get("ledger_disposition") != "historical-complete-smoke"
        or record.get("evaluation") != "preserved-unspent"
    ):
        fail("generation-5 historical ledger hashes or disposition differ from retention")
    final_invocation = _assert_invocations(record, record.get("git_head"))
    if final_invocation.get("disposition") != "finished" or final_invocation.get("exit_code") != 0:
        fail("generation-5 historical smoke invocation did not finish")
    for role, (snapshot_path, _original) in expected_snapshots.items():
        snapshot = load_json(REPO_ROOT / snapshot_path, what=f"generation-5 {role}")
        if not isinstance(snapshot, Mapping) or (snapshot.get("fingerprint") or {}).get("git_head") != record.get("git_head"):
            fail(f"generation-5 {role} snapshot has a different HEAD")
    _assert_no_evaluation(run_dir)


def current_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"cannot resolve current git HEAD: {result.stderr.strip()}")
    return result.stdout.strip()


FINGERPRINTED_RELS: tuple[str, ...] = (
    "pinn",
    "configs",
    "tests",
    "scripts",
    str(PHASE_REL),
)


def assert_fingerprint_inputs_clean() -> None:
    """57-08: the missing half of Task 1's admission contract.

    Task 1 requires the admission to confirm that "fingerprinted source/
    config/test/plan/environment inputs are committed and clean", but no such
    check existed anywhere in this file. On 2026-09-10 `admit-run-window`
    therefore printed ADMIT-RUN-WINDOW-OK over a tree carrying 733 uncommitted
    lines across 11 files, and the calibration smoke ran against code the
    admitted HEAD did not describe -- exactly threat T-57-13 ("any mutation
    between smoke and band would destroy comparability"), unguarded.

    `runs/` is deliberately NOT fingerprinted: Task 1 permits governed run and
    evidence output writes through the window; what must not move is the code,
    config, test, plan, and script inputs the HEAD claims to pin.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", *FINGERPRINTED_RELS],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(
            "cannot read git status for the fingerprinted inputs: "
            f"{result.stderr.strip()}"
        )
    dirty = [line for line in result.stdout.splitlines() if line.strip()]
    if dirty:
        shown = "\n  ".join(dirty[:20])
        more = "" if len(dirty) <= 20 else f"\n  ... and {len(dirty) - 20} more"
        fail(
            "fingerprinted inputs are not committed and clean, so the admitted "
            "HEAD would not describe the code that runs (D-09 / T-57-13):\n  "
            f"{shown}{more}"
        )


def is_ancestor(ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=str(REPO_ROOT),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def _assert_no_evaluation(root: Path) -> None:
    if (root / "evaluation").exists():
        fail(f"held-out evaluation directory exists: {root / 'evaluation'}")
    if root.exists():
        for path in root.rglob("*"):
            if path.is_file() and path.name in EVALUATION_NAMES:
                fail(f"held-out evaluation artifact exists: {path}")


def _gate_chain() -> tuple[Path, dict[str, Any], Path, dict[str, Any], dict[str, Any]]:
    artifact_path = REPO_ROOT / R_REF_REL
    artifact = load_json(artifact_path, what="R_ref artifact")
    if not isinstance(artifact, Mapping) or artifact.get("valid") is not True:
        fail("R_ref artifact is missing or not valid")
    provenance = artifact.get("provenance")
    if not isinstance(provenance, Mapping):
        fail("R_ref artifact provenance is missing")
    raw_value = provenance.get("gate_evidence_path")
    raw_digest = provenance.get("gate_evidence_sha256")
    if not isinstance(raw_value, str) or not isinstance(raw_digest, str) or not HEX64.fullmatch(raw_digest):
        fail("R_ref artifact lacks a valid Gate raw path/digest")
    raw_path = repo_path(raw_value, what="Gate raw evidence")
    try:
        raw_path.relative_to((REPO_ROOT / GATE_ROOT).resolve())
    except ValueError:
        fail("R_ref artifact Gate evidence is outside the Phase-57 gate root")
    if not raw_path.is_file() or sha256_file(raw_path) != raw_digest:
        fail("R_ref artifact Gate raw path/digest does not match on-disk evidence")
    raw = load_json(raw_path, what="Gate raw evidence")
    if not isinstance(raw, Mapping) or raw.get("schema_version") != GATE_SCHEMA:
        fail("Gate raw evidence schema mismatch")
    verdict = raw.get("verdict")
    if not isinstance(verdict, Mapping) or verdict.get("verdict") != "PASS":
        fail("Gate evidence is not PASS")
    if verdict.get("blocking_reasons") != [] or verdict.get("unratified_conditions") != []:
        fail("Gate evidence is not a complete PASS")
    cases = raw.get("cases")
    expected_labels = ["41", "42", "43", "0", "7", "41-variable-mass"]
    if not isinstance(cases, list) or [case.get("label") for case in cases] != expected_labels:
        fail("Gate evidence does not contain the exact six required cases")
    conformance_path = REPO_ROOT / CONFORMANCE_REL
    conformance = load_json(conformance_path, what="production conformance")
    if not isinstance(conformance, Mapping) or conformance.get("status") != "PASS":
        fail("production conformance is missing or not PASS")
    gate_provenance = conformance.get("gate_provenance")
    if not isinstance(gate_provenance, Mapping):
        fail("production conformance has no Gate provenance")
    if gate_provenance.get("raw_sha256") != raw_digest or gate_provenance.get("artifact_sha256") != sha256_file(artifact_path):
        fail("production conformance is bound to a different Gate/R_ref artifact")
    if conformance.get("loss", {}).get("r_ref") != artifact.get("r_ref"):
        fail("production conformance R_ref value differs from governed artifact")
    return raw_path, dict(raw), conformance_path, dict(conformance), dict(artifact)


def _assert_config_contract() -> Path:
    # GAP-57-06/08 preserve earlier attempts and admit only generation 5.
    from pinn.train import _admitted_data_preflight
    from pinn.training.config_yaml import load_config

    names = ("smoke", "seed41", "seed42", "seed43")
    paths = tuple(REPO_ROOT / f"configs/stage0-v23g6-{name}.yaml" for name in names)
    corpus_roots: set[Path] = set()
    for name, path in zip(names, paths):
        if not path.is_file():
            fail(f"required Phase-57 config is missing: {path}")
        try:
            config = load_config(path)
        except Exception as exc:  # noqa: BLE001 - any config refusal blocks admission
            fail(f"required Phase-57 config does not strict-load: {path}: {exc}")
        expected_seed = 42 if name == "smoke" else int(name.removeprefix("seed"))
        expected_budget = 300 if name == "smoke" else 1000
        if (
            config.run.run_name != f"stage0-v23g6-{name}"
            or config.run.seed != expected_seed
            or config.run.smoke is not (name == "smoke")
            or config.stage.max_epochs != expected_budget
            or config.stage.n_adam != expected_budget
            or config.stage.collocation_count != 4096
            or config.stage.replay_count != 240
            or config.run.invariants.front_advance_window_n != 500
            or config.loss.r_ref_artifact_path != str(R_REF_REL)
            or config.data.source != "admitted"
        ):
            fail(f"{path} differs from the ratified generation-6 recipe")
        try:
            corpus_roots.add(_admitted_data_preflight(config))
        except Exception as exc:  # noqa: BLE001 - missing data fails before a run
            fail(f"admitted corpus is unreachable for {path}: {exc}")
    if len(corpus_roots) != 1:
        fail("generation-6 configs resolve different admitted corpus roots")
    return corpus_roots.pop()


def _assert_mps_runtime() -> dict[str, Any]:
    """Prove the admitted host can allocate one MPS tensor before a run."""
    try:
        import torch
        available = bool(torch.backends.mps.is_available())
        count = int(torch.mps.device_count())
        if not available or count < 1:
            fail(f"host MPS runtime is unavailable at admission: available={available}, device_count={count}")
        probe = torch.ones(1, dtype=torch.float32, device="mps")
        if hasattr(torch.mps, "synchronize"):
            torch.mps.synchronize()
        result = {
            "torch_version": torch.__version__,
            "mps_available": available,
            "mps_device_count": count,
            "probe": str(probe),
        }
        del probe
        if hasattr(torch.mps, "empty_cache"):
            torch.mps.empty_cache()
        return result
    except VerifyError:
        raise
    except Exception as exc:  # noqa: BLE001 - allocation must fail closed
        fail(f"host MPS allocation failed at admission: {exc}")


def _target_runs() -> tuple[Path, ...]:
    return tuple(REPO_ROOT / f"runs/stage0-v23g6-{name}" for name in ("smoke", "seed41", "seed42", "seed43"))


def _assert_seed42_setup(*, before_other_seeds: bool) -> dict[str, Any]:
    """Compare produced seed-42 smoke/graded setup without reading metrics."""
    smoke = REPO_ROOT / "runs/stage0-v23g6-smoke"
    graded = REPO_ROOT / "runs/stage0-v23g6-seed42"
    if before_other_seeds and any(
        (REPO_ROOT / f"runs/stage0-v23g6-seed{seed}").exists()
        for seed in (41, 43)
    ):
        fail("seed-42 setup comparison must pass before seeds 41 or 43 launch")
    smoke_status = load_json(smoke / "status.json", what="seed-42 smoke status")
    smoke_summary = load_json(smoke / "summary.json", what="seed-42 smoke summary")
    if (
        smoke_status.get("state") != "finished"
        or smoke_summary.get("disposition") != "finished"
        or smoke_summary.get("run_name") != "stage0-v23g6-smoke"
    ):
        fail("seed-42 smoke did not finish under the admitted run identity")
    graded_status = load_json(graded / "status.json", what="graded seed-42 status")
    if graded_status.get("run_name") != "stage0-v23g6-seed42":
        fail("graded seed-42 setup has the wrong run identity")
    graded_preflight = load_json(graded / "preflight.json", what="graded seed-42 preflight")
    if graded_preflight.get("preflight_status") != "passed":
        fail("graded seed-42 preflight has not passed")
    split_paths = (smoke / "splits.json", graded / "splits.json")
    try:
        smoke_splits, graded_splits = (path.read_bytes() for path in split_paths)
    except OSError as exc:
        fail(f"seed-42 setup split artifacts are missing or unreadable: {exc}")
    if smoke_splits != graded_splits:
        fail("seed-42 smoke and graded splits.json bytes differ")
    smoke_metadata = load_json(smoke / "training_metadata.json", what="seed-42 smoke metadata")
    graded_metadata = load_json(graded / "training_metadata.json", what="graded seed-42 metadata")
    for field in ("s_h", "n_train"):
        left, right = smoke_metadata.get(field), graded_metadata.get(field)
        valid = (
            type(left) in (int, float) and type(right) in (int, float)
            if field == "s_h" else type(left) is int and type(right) is int
        )
        if not valid or left != right:
            fail(f"seed-42 smoke and graded {field} differ or are invalid")
        if field == "s_h" and not (math.isfinite(float(left)) and left > 0):
            fail(f"seed-42 smoke and graded {field} differ or are invalid")
        if field == "n_train" and left <= 0:
            fail(f"seed-42 smoke and graded {field} differ or are invalid")
    return {
        "splits_sha256": sha256_file(split_paths[0]),
        "s_h": smoke_metadata["s_h"],
        "n_train": smoke_metadata["n_train"],
    }


def cmd_seed42_setup() -> None:
    ledger = load_ledger()
    generation = [item for item in ledger["band_generations"] if item.get("band_generation") == FINAL_GENERATION]
    if len(generation) != 1 or generation[0].get("git_head") != current_head():
        fail("seed-42 setup is outside the admitted immutable band HEAD")
    result = _assert_seed42_setup(before_other_seeds=True)
    print("SEED42-SETUP-OK")
    print(f"head={current_head()}")
    print(f"splits_sha256={result['splits_sha256']}")
    print(f"s_h={result['s_h']}")
    print(f"n_train={result['n_train']}")


def _assert_launch_order(generation: Mapping[str, Any], records: list[Mapping[str, Any]]) -> None:
    if generation.get("launch_order") != list(FINAL_LAUNCH_ORDER):
        fail("generation-6 graded launch order is not smoke, 42, 41, 43")
    ordered = sorted(records, key=lambda record: record["invocations"][0]["start_utc"])
    if [record.get("run_name") for record in ordered] != list(FINAL_LAUNCH_ORDER):
        fail("generation-6 process timestamps violate graded launch order")
    for previous, following in zip(ordered, ordered[1:]):
        previous_end = datetime.fromisoformat(previous["invocations"][-1]["end_utc"])
        following_start = datetime.fromisoformat(following["invocations"][0]["start_utc"])
        if following_start < previous_end:
            fail("generation-6 runs overlap instead of following sequential launch order")


def _assert_ancestry(*commits: Any) -> None:
    head = current_head()
    for commit in commits:
        if isinstance(commit, str) and commit and not is_ancestor(commit, head):
            fail(f"evidence commit {commit} is not an ancestor of current HEAD")


def cmd_admit_run_window() -> None:
    raw_path, raw, conformance_path, conformance, artifact = _gate_chain()
    corpus_root = _assert_config_contract()
    mps_runtime = _assert_mps_runtime()
    assert_fingerprint_inputs_clean()
    ruling = REPO_ROOT / PHASE_REL / "57-RULING.md"
    if not ruling.is_file() or "status: ratified" not in ruling.read_text(encoding="utf-8"):
        fail("57-RULING.md is not the ratified owner record")
    for run_dir in _target_runs():
        if run_dir.exists():
            fail(f"target run directory already exists: {run_dir}")
    ledger = load_ledger()
    assert_generation_one_blocked_state_retained(ledger)
    assert_generation_three_blocked_state_retained(ledger)
    assert_generation_four_blocked_state_retained(ledger)
    assert_generation_five_retained(ledger)
    assert_generation_two_retained()
    historical = {
        (generation.get("band_generation"), generation.get("status"))
        for generation in ledger["band_generations"]
    }
    if historical != {(1, "blocked"), (2, "historical-incomplete"), (3, "blocked"), (4, "blocked"), (5, "historical-complete-smoke")}:
        fail("run ledger does not contain exactly the five preserved prior generations")
    old_attempts = [record for record in ledger["records"] if record.get("band_generation") == 2]
    if len(old_attempts) != 1 or old_attempts[0].get("run_name") != "stage0-v23g2-smoke" or old_attempts[0].get("in_final_band") is not False:
        fail("interrupted generation-2 smoke is not recorded as historical and ineligible")
    manifest = load_json(REPO_ROOT / RETENTION_REL, what="generation-2 retention manifest")
    manifest_hashes = {
        entry["path"].removeprefix("runs/stage0-v23g2-smoke/"): entry["sha256"]
        for entry in manifest["files"]
    }
    if old_attempts[0].get("artifact_hashes") != manifest_hashes:
        fail("generation-2 historical ledger hashes differ from retention manifest")
    # 57-07: admission must refuse a COMPLETED or IN-FLIGHT band (the
    # invariant this check protects), not merely "any record exists at
    # all" -- generation 1's ledger entry is a `blocked` (operational
    # failure, evaluation preserved-unspent) record, not a success, so it
    # does not itself bar a second admission.
    if ledger.get("final_band_generation") is not None:
        fail(
            "run ledger already has a final band generation; immutable "
            "admission must occur before runs"
        )
    gate_head = (raw.get("provenance") or {}).get("git_sha")
    conformance_head = (conformance.get("provenance") or {}).get("git_head")
    _assert_ancestry(gate_head, conformance_head)
    print("ADMIT-RUN-WINDOW-OK")
    print(f"head={current_head()}")
    print(f"gate_raw={raw_path.relative_to(REPO_ROOT)}")
    print(f"conformance={conformance_path.relative_to(REPO_ROOT)}")
    print(f"r_ref_sha256={sha256_file(REPO_ROOT / R_REF_REL)}")
    print(f"corpus_root={corpus_root}")
    print(f"mps_runtime={json.dumps(mps_runtime, sort_keys=True)}")


def _terminal_state() -> dict[str, Any] | None:
    path = REPO_ROOT / EVIDENCE_REL / "terminal-state.json"
    return load_json(path, what="terminal state") if path.is_file() else None


def _blocked_state() -> dict[str, Any] | None:
    path = REPO_ROOT / CURRENT_BLOCKED_STATE_REL
    return load_json(path, what="generation-6 blocked state") if path.is_file() else None


def _assert_resume_checkpoint(raw: Any, artifact_dir: Path) -> None:
    if not isinstance(raw, Mapping):
        fail("resumed invocation lacks a boundary checkpoint record")
    relative, expected = raw.get("path"), raw.get("sha256")
    if not isinstance(relative, str) or not isinstance(expected, str) or not HEX64.fullmatch(expected):
        fail("resumed invocation has an invalid boundary checkpoint path/digest")
    path = repo_path(relative, what="resume boundary checkpoint")
    try:
        path.relative_to(artifact_dir)
    except ValueError:
        fail("resume boundary checkpoint is outside its run directory")
    if not path.is_file() or sha256_file(path) != expected:
        fail("resume boundary checkpoint bytes differ from the ledger")
    try:
        import torch
        payload = torch.load(path, map_location="cpu", weights_only=True)
    except Exception as exc:  # noqa: BLE001 - a bad checkpoint must fail closed
        fail(f"resume boundary checkpoint cannot be read safely: {exc}")
    state = payload.get("invariant_b_state") if isinstance(payload, Mapping) else None
    if not isinstance(state, Mapping) or not {"front_high_water", "last_advance_step"} <= set(state):
        fail("resume boundary checkpoint lacks invariant_b_state")


def _assert_invocations(record: Mapping[str, Any], expected_head: str) -> Mapping[str, Any]:
    """Verify every process of one final-HEAD run before certifying the band."""
    invocations = record.get("invocations")
    if not isinstance(invocations, list) or not invocations:
        fail(f"run {record.get('run_name')!r} lacks invocation history")
    if record.get("git_head") != expected_head or not isinstance(expected_head, str) or not expected_head:
        fail("run invocation history does not match the band HEAD")
    config_sha = record.get("config_sha256")
    if not isinstance(config_sha, str) or not HEX64.fullmatch(config_sha):
        fail("run record lacks a source config digest")
    config = repo_path(record.get("config_path"), what="source run config")
    if not config.is_file() or sha256_file(config) != config_sha:
        fail("source run config changed after the run")
    artifact_dir = repo_path(record.get("artifact_dir"), what="run artifact directory")
    if not artifact_dir.is_dir() or artifact_dir.name != record.get("run_name"):
        fail("run artifact directory does not match its ledger identity")
    previous: Mapping[str, Any] | None = None
    previous_end: datetime | None = None
    for ordinal, invocation in enumerate(invocations, 1):
        if not isinstance(invocation, Mapping) or invocation.get("invocation_ordinal") != ordinal:
            fail("run invocations are not consecutively numbered")
        kind = invocation.get("launch_kind")
        if kind != ("fresh" if ordinal == 1 else "resume"):
            fail("run must start fresh and use resume only for later invocations")
        if invocation.get("git_head") != expected_head or invocation.get("config_sha256") != config_sha:
            fail("resumed process changed the run HEAD or config identity")
        command = invocation.get("command")
        if not isinstance(command, str):
            fail("run invocation lacks its exact launch command")
        try:
            argv = shlex.split(command)
        except ValueError:
            fail("run invocation command cannot be parsed")
        if "--stage-0-only" not in argv or "--config" not in argv:
            fail("run invocation lacks Stage-0-only or config binding")
        config_arg = argv.index("--config")
        if config_arg + 1 >= len(argv) or argv[config_arg + 1] != record.get("config_path"):
            fail("run invocation names a different source config")
        if type(invocation.get("process_pid")) is not int or invocation["process_pid"] <= 0:
            fail("run invocation lacks a process PID")
        if type(invocation.get("exit_code")) is not int:
            fail("run invocation lacks an exit code")
        elapsed = invocation.get("wall_clock_secs")
        if not isinstance(elapsed, (int, float)) or elapsed < 0:
            fail("run invocation lacks nonnegative active wall time")
        try:
            started = datetime.fromisoformat(invocation["start_utc"])
            ended = datetime.fromisoformat(invocation["end_utc"])
        except (KeyError, TypeError, ValueError):
            fail("run invocation has invalid start/end UTC times")
        if started.tzinfo is None or ended.tzinfo is None or ended < started or (previous_end is not None and started < previous_end):
            fail("run invocation timestamps are missing zones or out of order")
        if ordinal == 1:
            if "--resume" in argv or invocation.get("resume_checkpoint") is not None:
                fail("fresh invocation must not resume from a checkpoint")
        else:
            assert previous is not None
            if previous.get("disposition") != "interrupted" or previous.get("exit_code") != 130:
                fail("resume does not follow a governed interrupted process")
            if "--resume" not in argv or argv.index("--resume") + 1 >= len(argv) or argv[argv.index("--resume") + 1] != "latest":
                fail("resumed invocation lacks --resume latest")
            boundary = previous.get("boundary_checkpoint")
            if invocation.get("resume_checkpoint") != boundary:
                fail("resume checkpoint differs from the preceding boundary")
            _assert_resume_checkpoint(boundary, artifact_dir)
        previous = invocation
        previous_end = ended
    return invocations[-1]


def cmd_run_window() -> None:
    _gate_chain()
    assert_generation_two_retained()
    ledger = load_ledger()
    assert_generation_one_blocked_state_retained(ledger)
    assert_generation_three_blocked_state_retained(ledger)
    assert_generation_four_blocked_state_retained(ledger)
    assert_generation_five_retained(ledger)
    current_records = [record for record in ledger["records"] if record.get("band_generation") == FINAL_GENERATION]
    current_generations = [generation for generation in ledger["band_generations"] if generation.get("band_generation") == FINAL_GENERATION]
    if current_records:
        if len(current_generations) != 1:
            fail("generation-6 run records lack one generation header")
        for record in current_records:
            _assert_invocations(record, current_generations[0].get("git_head"))
    blocked = _blocked_state()
    if blocked is not None and (
        blocked.get("band_generation") != FINAL_GENERATION
        or blocked.get("run_name") not in FINAL_RUN_NAMES
        or blocked.get("evaluation") != "preserved-unspent"
        or blocked.get("terminal") is not False
    ):
        fail("generation-6 operational/resource/guard blocked-state is incomplete and cannot close the run window")
    if blocked is not None:
        fail("generation-6 operational/resource/guard blocked-state is incomplete and cannot close the run window")
    terminal = _terminal_state()
    if terminal is not None:
        reason = terminal.get("authorized_terminal_reason")
        if terminal.get("status") != "terminal" or reason not in TERMINAL_OUTCOMES or terminal.get("evaluation") != "preserved-unspent":
            fail("terminal-state is not an authorized scientific unspent closure")
        for run_dir in _target_runs():
            _assert_no_evaluation(run_dir)
        if (REPO_ROOT / "runs/stage0-v23g6-seed42").exists():
            _assert_seed42_setup(before_other_seeds=False)
        print("RUN-WINDOW-TERMINAL-OK")
        return
    final = ledger.get("final_band_generation")
    if final is None:
        fail("run window is neither complete nor an authorized terminal closure")
    if final != FINAL_GENERATION:
        fail("final band generation is not the admitted generation 5")
    records = [record for record in ledger["records"] if int(record.get("band_generation", -1)) == int(final)]
    graded = [record for record in records if record.get("in_final_band") is True]
    smoke = [record for record in records if record.get("run_name") == "stage0-v23g6-smoke"]
    expected_names = {"stage0-v23g6-smoke", "stage0-v23g6-seed41", "stage0-v23g6-seed42", "stage0-v23g6-seed43"}
    if (
        len(records) != 4 or len(smoke) != 1 or smoke[0].get("in_final_band") is not False
        or len(graded) != 3 or sorted(record.get("seed") for record in graded) != [41, 42, 43]
        or {record.get("run_name") for record in records} != expected_names
        or any(record.get("run_name") != f"stage0-v23g6-seed{record.get('seed')}" for record in graded)
    ):
        fail("complete run window has wrong run names or lacks one smoke and three in-band seeds")
    _assert_seed42_setup(before_other_seeds=False)
    for run_dir in _target_runs():
        _assert_no_evaluation(run_dir)
    generation = current_generations[0]
    _assert_launch_order(generation, records)
    run_heads = {record.get("git_head") for record in records if record.get("git_head")}
    if generation.get("git_head") not in run_heads or len(run_heads) != 1:
        fail("run records do not share one immutable HEAD")
    for record in records:
        if record.get("final_process_disposition") != "finished" or record.get("ledger_disposition") != "finished":
            fail("final band contains an unfinished run")
        final_invocation = _assert_invocations(record, generation["git_head"])
        if final_invocation.get("disposition") != "finished" or final_invocation.get("exit_code") != 0:
            fail("final band invocation did not finish cleanly")
    print("RUN-WINDOW-OK")


def _contains_metric_key(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            if any(token in lowered for token in ("scs", "metric", "loss", "eps_h")):
                return True
            if _contains_metric_key(child):
                return True
    elif isinstance(value, (list, tuple)):
        return any(_contains_metric_key(item) for item in value)
    return False


def cmd_candidate() -> None:
    cmd_run_window()
    terminal = _terminal_state()
    no_candidate = REPO_ROOT / EVIDENCE_REL / "no-candidate.json"
    if terminal is not None:
        if not no_candidate.is_file():
            fail("authorized terminal state lacks no-candidate receipt")
        receipt = load_json(no_candidate, what="no-candidate receipt")
        if receipt.get("evaluation") != "preserved-unspent":
            fail("terminal no-candidate receipt does not preserve evaluation")
        print("CANDIDATE-OK")
        return
    path = REPO_ROOT / EVIDENCE_REL / "candidate-receipt.json"
    receipt = load_json(path, what="candidate receipt")
    if receipt.get("schema") != "phase57-candidate-receipt/v1":
        fail("candidate receipt schema mismatch")
    facts = receipt.get("facts")
    if not isinstance(facts, Mapping) or set(facts) != {"41", "42", "43"}:
        fail("candidate facts must cover exactly seeds 41/42/43")
    first = None
    for seed in CANDIDATE_ORDER:
        entry = facts.get(str(seed))
        if not isinstance(entry, Mapping) or set(entry) != set(REQUIRED_STRUCTURAL_FACTS) | {"eligible"}:
            fail(f"candidate seed {seed} does not carry exactly the four structural facts")
        if _contains_metric_key(entry):
            fail("candidate facts contain metric-dependent fields")
        if entry.get("eligible") is True and first is None:
            first = seed
    if first is None:
        if receipt.get("run_name") is not None or receipt.get("owner_stop") is not True:
            fail("no-candidate state must be explicit and preserve the evaluation")
    else:
        if receipt.get("run_name") != f"stage0-v23g6-seed{first}" or receipt.get("seed") != first:
            fail("candidate is not the first eligible seed in 42/41/43 order")
        best = receipt.get("candidate_best_sha256")
        if not isinstance(best, str) or not HEX64.fullmatch(best):
            fail("candidate best.pt digest is missing")
        best_path = repo_path(receipt.get("candidate_best_path"), what="candidate best.pt")
        if not best_path.is_file() or sha256_file(best_path) != best:
            fail("candidate best.pt digest/path mismatch")
    print("CANDIDATE-OK")


def cmd_pre_evaluation() -> None:
    cmd_candidate()
    if _terminal_state() is not None or (REPO_ROOT / EVIDENCE_REL / "no-candidate.json").is_file():
        print("PRE-EVALUATION-UNSPENT-OK")
        return
    readiness = load_json(REPO_ROOT / EVIDENCE_REL / "evaluation-readiness.json", what="evaluation readiness")
    if readiness.get("evaluation") != "preserved-unspent" or readiness.get("preconditions") != {"i": True, "ii": True, "iii": True}:
        fail("evaluation readiness does not prove all three preconditions")
    frame = readiness.get("frame") or {}
    if frame != {"position_frame": "r_prime", "time_coord": "u_t_over_T", "mass_convention": "ordered_raw"}:
        fail("evaluation readiness frame is not canonical")
    for run_dir in _target_runs():
        _assert_no_evaluation(run_dir)
    print("PRE-EVALUATION-OK")


def cmd_final() -> None:
    cmd_candidate()
    terminal = _terminal_state()
    no_candidate = REPO_ROOT / EVIDENCE_REL / "no-candidate.json"
    if terminal is not None or no_candidate.is_file():
        for run_dir in _target_runs():
            _assert_no_evaluation(run_dir)
        print("FINAL-UNSPENT-OK")
        return
    candidate = load_json(REPO_ROOT / EVIDENCE_REL / "candidate-receipt.json", what="candidate receipt")
    selected = candidate.get("run_name")
    if not isinstance(selected, str):
        fail("selected candidate is missing")
    eval_dirs = []
    for run_dir in _target_runs():
        if (run_dir / "evaluation").exists():
            eval_dirs.append(run_dir)
    if len(eval_dirs) != 1 or eval_dirs[0].name != selected:
        fail("evaluation material does not exist exactly once on the selected run")
    receipt_copy = REPO_ROOT / EVIDENCE_REL / "evaluation-receipt-copy.json"
    receipt = load_json(receipt_copy, what="evaluation receipt copy")
    source = repo_path(receipt.get("source"), what="evaluation receipt source")
    if source != eval_dirs[0] / "evaluation" / "evaluation-receipt.json":
        fail("evaluation receipt copy points to the wrong run")
    if receipt.get("source_sha256") != sha256_file(source):
        fail("evaluation receipt copy hash mismatch")
    print("FINAL-EVIDENCE-OK")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("admit-run-window", "seed42-setup", "run-window", "candidate", "pre-evaluation", "final"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        {
            "admit-run-window": cmd_admit_run_window,
            "seed42-setup": cmd_seed42_setup,
            "run-window": cmd_run_window,
            "candidate": cmd_candidate,
            "pre-evaluation": cmd_pre_evaluation,
            "final": cmd_final,
        }[args.command]()
    except Exception as exc:  # noqa: BLE001 - verifier CLI is fail-closed
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
