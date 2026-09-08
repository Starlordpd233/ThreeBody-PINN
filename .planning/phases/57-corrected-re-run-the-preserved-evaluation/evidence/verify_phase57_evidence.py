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
import re
import subprocess
import sys
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
LEDGER_SCHEMA = "phase57-run-ledger/v1"
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


def repo_path(raw: str | Path, *, what: str, root: Path = REPO_ROOT) -> Path:
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
    return ledger


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


def _assert_config_contract() -> None:
    paths = (
        REPO_ROOT / "configs/stage0-v23-smoke.yaml",
        REPO_ROOT / "configs/stage0-v23-seed41.yaml",
        REPO_ROOT / "configs/stage0-v23-seed42.yaml",
        REPO_ROOT / "configs/stage0-v23-seed43.yaml",
    )
    for path in paths:
        if not path.is_file():
            fail(f"required Phase-57 config is missing: {path}")
        text = path.read_text(encoding="utf-8")
        for needle in ("collocation_count: 4096", "front_advance_window_n: 500", "r_ref_artifact_path: pinn/verification/artifacts/r_ref_stage0.json"):
            if needle not in text:
                fail(f"{path} is missing required recipe binding {needle!r}")
    seed_paths = {41: paths[1], 42: paths[2], 43: paths[3]}
    for seed, path in seed_paths.items():
        if f"seed: {seed}" not in path.read_text(encoding="utf-8"):
            fail(f"{path} has the wrong seed")


def _target_runs() -> tuple[Path, ...]:
    return tuple(REPO_ROOT / f"runs/stage0-v23-{name}" for name in ("smoke", "seed41", "seed42", "seed43"))


def _assert_ancestry(*commits: Any) -> None:
    head = current_head()
    for commit in commits:
        if isinstance(commit, str) and commit and not is_ancestor(commit, head):
            fail(f"evidence commit {commit} is not an ancestor of current HEAD")


def cmd_admit_run_window() -> None:
    raw_path, raw, conformance_path, conformance, artifact = _gate_chain()
    _assert_config_contract()
    ruling = REPO_ROOT / PHASE_REL / "57-RULING.md"
    if not ruling.is_file() or "status: ratified" not in ruling.read_text(encoding="utf-8"):
        fail("57-RULING.md is not the ratified owner record")
    for run_dir in _target_runs():
        if run_dir.exists():
            fail(f"target run directory already exists: {run_dir}")
    ledger = load_ledger()
    if ledger.get("final_band_generation") is not None or ledger.get("records"):
        fail("run ledger already contains a band; immutable admission must occur before runs")
    gate_head = (raw.get("provenance") or {}).get("git_sha")
    conformance_head = (conformance.get("provenance") or {}).get("git_head")
    _assert_ancestry(gate_head, conformance_head)
    print("ADMIT-RUN-WINDOW-OK")
    print(f"head={current_head()}")
    print(f"gate_raw={raw_path.relative_to(REPO_ROOT)}")
    print(f"conformance={conformance_path.relative_to(REPO_ROOT)}")
    print(f"r_ref_sha256={sha256_file(REPO_ROOT / R_REF_REL)}")


def _terminal_state() -> dict[str, Any] | None:
    path = REPO_ROOT / EVIDENCE_REL / "terminal-state.json"
    return load_json(path, what="terminal state") if path.is_file() else None


def _blocked_state() -> dict[str, Any] | None:
    path = REPO_ROOT / EVIDENCE_REL / "blocked-state.json"
    return load_json(path, what="blocked state") if path.is_file() else None


def cmd_run_window() -> None:
    _gate_chain()
    blocked = _blocked_state()
    if blocked is not None:
        fail("operational/resource/guard blocked-state is incomplete and cannot close the run window")
    terminal = _terminal_state()
    if terminal is not None:
        reason = terminal.get("authorized_terminal_reason")
        if terminal.get("status") != "terminal" or reason not in TERMINAL_OUTCOMES or terminal.get("evaluation") != "preserved-unspent":
            fail("terminal-state is not an authorized scientific unspent closure")
        for run_dir in _target_runs():
            _assert_no_evaluation(run_dir)
        print("RUN-WINDOW-TERMINAL-OK")
        return
    ledger = load_ledger()
    final = ledger.get("final_band_generation")
    if final is None:
        fail("run window is neither complete nor an authorized terminal closure")
    records = [record for record in ledger["records"] if int(record.get("band_generation", -1)) == int(final)]
    if len([record for record in records if record.get("in_final_band")]) != 3:
        fail("complete run window does not contain three in-band seeds")
    for run_dir in _target_runs():
        _assert_no_evaluation(run_dir)
    generation = next(item for item in ledger["band_generations"] if int(item.get("band_generation", -1)) == int(final))
    run_heads = {record.get("git_head") for record in records if record.get("git_head")}
    if generation.get("git_head") not in run_heads or len(run_heads) != 1:
        fail("run records do not share one immutable HEAD")
    if any(record.get("launch_kind") == "resume" for record in records):
        fail("run window contains a resumed launch")
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
        if receipt.get("run_name") != f"stage0-v23-seed{first}" or receipt.get("seed") != first:
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
    parser.add_argument("command", choices=("admit-run-window", "run-window", "candidate", "pre-evaluation", "final"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        {
            "admit-run-window": cmd_admit_run_window,
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
