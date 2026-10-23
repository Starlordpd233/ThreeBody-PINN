#!/usr/bin/env python3
"""Phase 60: fail-closed evidence verifier for the single-system learnability phase.

Independent, fail-closed verification of the Phase 60 pre-registration protocol,
preflight record catalog, experimental run records and weights, Gate G2 outcomes
and sweeps, and re-scoring on CPU and MPS.
"""

from __future__ import annotations

import argparse
from collections import OrderedDict
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

import torch

from pinn.network import ArchitectureSpec, build_network
from pinn.training.controllers import _tensor_hash
from pinn.verification.diagnostic_architecture import build_network_with_first_omega
from pinn.verification.feasibility_scorecard import (
    SCORECARD_SHA256,
    counts,
    decision_verdict,
    g2_fires,
    load_scorecard,
)
from pinn.verification.feasibility_scorer import score_network
from pinn.verification.learnability_arms import (
    EVIDENCE_REL,
    PANEL_SYSTEMS,
    PHASE_REL,
    SEED,
    arm_evidence_dir,
    arm_spec,
    catalog,
)
from pinn.verification.learnability_data import load_arm_data, open_real_context
from pinn.verification.learnability_g2 import (
    CURVE_SCHEMA,
    HANDOFF_SCHEMA,
    OUTCOME_SCHEMA,
    RESCUE_SCHEMA,
    SKIP_REASONS,
    SKIP_SCHEMA,
    confirmed_omega,
    sweep_plan,
)
from pinn.verification.learnability_protocol import (
    EXPECTED_WITHIN_T,
    PINNED_MODULES,
    PREFLIGHT_REL,
    PREFLIGHT_SCHEMA,
    PROTOCOL_DOC_REL,
    PROTOCOL_REL,
    PROTOCOL_SCHEMA,
    SCORER_REL,
    SCORECARD_REL,
    SCORER_SUCCESSOR_REL,
)
from pinn.verification.learnability_ruling import (
    RULING4_REL,
    RULING_GAP6009_REL,
    RulingError,
    RulingMissing,
    RulingUncommitted,
    load_checkpoint4_ruling,
    load_gap6009_ruling,
)
from pinn.verification.learnability_run import _float32_rounded

REPO_ROOT = Path(__file__).resolve().parents[4]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
_HEX40 = re.compile(r"^[0-9a-f]{40}$")

G2_TOKENS = {
    "outcome": "g2-outcome.json",
    "sweep-curve": "sweep-curve.json",
    "rescue": "rescue.json",
    "skip-records": "skip-records.json",
    "stop-handoff": "stop-handoff.json",
}

REQUIRED_REAL_FIELDS = (
    "schema",
    "diagnostic",
    "run_kind",
    "arm_id",
    "loss_arm",
    "counted",
    "seed",
    "runtime.dtype",
    "runtime.device",
    "versions.torch",
    "versions.numpy",
    "versions.python",
    "versions.macos",
    "code.git_head",
    "code.dirty_pinn_paths",
    "config_sha256",
    "scorecard_sha256",
    "scorer_sha256",
    "protocol_sha256",
    "module_sha256",
    "normalizer.stats_sha256",
    "attestation.test_split_opened",
    "attestation.blocked_attempts",
    "attestation.refused_before_open",
    "timing.seconds_per_step",
    "budget.rule",
    "budget.budget_steps",
    "budget.reading_steps",
    "budget.readings",
    "budget.outcome",
    "budget.extended",
    "trace",
    "states.adam.score_gold",
    "states.adam.score_base",
    "states.adam.cross_check",
    "states.adam.weights.file",
    "states.adam.weights.sha256",
    "states.adam.weights.tensor_digest",
    "states.polish.score_gold",
    "states.polish.score_base",
    "states.polish.cross_check",
    "states.polish.weights.file",
    "states.polish.weights.sha256",
    "states.polish.weights.tensor_digest",
    "better_state",
    "result.state",
    "result.tier",
    "result.E",
    "result.e_in_max",
    "result.h",
    "result.eps_h",
    "formula.E_formula",
    "formula.counts",
    "wall.hours",
)


class VerifyError(RuntimeError):
    """Fail-closed evidence verification error."""


def fail(message: str) -> None:
    raise VerifyError(f"verify_phase60_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def repo_path(raw: str | Path, *, what: str, root: Optional[Path] = None) -> Path:
    base = REPO_ROOT if root is None else root
    supplied = Path(str(raw))
    resolved = (base / supplied).resolve() if not supplied.is_absolute() else supplied.resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        fail(f"{what} escapes the repository: {raw!r}")
    candidate = base / supplied
    if not supplied.is_absolute() and candidate.is_symlink():
        fail(f"{what} is a symlink: {raw!r}")
    return resolved


def load_json(path: Path, *, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{what} is unreadable JSON: {path}: {exc}")


def _git(*args: str, root: Optional[Path] = None) -> subprocess.CompletedProcess[str]:
    base = REPO_ROOT if root is None else root
    return subprocess.run(
        ["git", *args],
        cwd=str(base),
        capture_output=True,
        text=True,
        check=False,
    )


def is_ancestor(ancestor: str, descendant: str, root: Optional[Path] = None) -> bool:
    return _git("merge-base", "--is-ancestor", ancestor, descendant, root=root).returncode == 0


def is_tracked(relative: str, root: Optional[Path] = None) -> bool:
    return _git("ls-files", "--error-unmatch", "--", relative, root=root).returncode == 0


def is_clean(relative: str, root: Optional[Path] = None) -> bool:
    proc = _git("status", "--porcelain", "--", relative, root=root)
    return proc.returncode == 0 and not proc.stdout.strip()


def weights_digest(state_dict: Mapping[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for name in sorted(state_dict):
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_tensor_hash(state_dict[name]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _lookup(payload: Any, dotted: str) -> Any:
    current = payload
    for part in dotted.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


# ---------------------------------------------------------------------------
# Subcommand implementations
# ---------------------------------------------------------------------------

def cmd_protocol(args: argparse.Namespace) -> None:
    protocol_path = repo_path(PROTOCOL_REL, what="run protocol")
    if not protocol_path.is_file():
        fail(f"run protocol is missing: {PROTOCOL_REL}")
    if not is_tracked(str(PROTOCOL_REL)) or not is_clean(str(PROTOCOL_REL)):
        fail(f"run protocol is not tracked and clean: {PROTOCOL_REL}")

    protocol = load_json(protocol_path, what="run protocol")
    if not isinstance(protocol, Mapping):
        fail("run protocol is not a JSON object")
    if protocol.get("schema") != PROTOCOL_SCHEMA:
        fail(f"run protocol schema is not {PROTOCOL_SCHEMA}")

    # Check scorecard
    scorecard_path = repo_path(SCORECARD_REL, what="scorecard")
    if not scorecard_path.is_file():
        fail(f"scorecard is missing: {SCORECARD_REL}")
    scorecard_sha = sha256_file(scorecard_path)
    if scorecard_sha != SCORECARD_SHA256:
        fail(f"scorecard SHA-256 {scorecard_sha} != {SCORECARD_SHA256}")
    if protocol.get("scorecard_sha256") != SCORECARD_SHA256:
        fail(f"protocol scorecard_sha256 does not match {SCORECARD_SHA256}")

    # Check scorer successor
    succ_path = repo_path(SCORER_SUCCESSOR_REL, what="scorer successor")
    if not succ_path.is_file():
        fail(f"scorer successor is missing: {SCORER_SUCCESSOR_REL}")
    if not is_tracked(str(SCORER_SUCCESSOR_REL)) or not is_clean(str(SCORER_SUCCESSOR_REL)):
        fail(f"scorer successor is not tracked and clean: {SCORER_SUCCESSOR_REL}")
    succ_record = load_json(succ_path, what="scorer successor")
    successor_sha = succ_record.get("successor_sha256")
    if not isinstance(successor_sha, str) or not HEX64.fullmatch(successor_sha):
        fail("scorer successor record has invalid successor_sha256")
    if protocol.get("scorer_sha256") != successor_sha:
        fail(f"protocol scorer_sha256 {protocol.get('scorer_sha256')} does not match successor {successor_sha}")
    scorer_path = repo_path(SCORER_REL, what="scorer module")
    if sha256_file(scorer_path) != successor_sha:
        fail(f"scorer module {SCORER_REL} on disk does not equal successor {successor_sha}")

    # Check amendment commit
    amendment_commit = protocol.get("amendment_commit")
    if not isinstance(amendment_commit, str) or not _HEX40.fullmatch(amendment_commit):
        fail(f"protocol amendment_commit {amendment_commit!r} is invalid")
    if not is_ancestor(amendment_commit, "HEAD"):
        fail(f"amendment commit {amendment_commit} is not an ancestor of HEAD")
    log_proc = _git("log", "-1", "--name-only", "--format=", amendment_commit)
    touched_files = [line.strip() for line in log_proc.stdout.splitlines() if line.strip()]
    if not any("REQUIREMENTS.md" in f for f in touched_files):
        fail(f"amendment commit {amendment_commit} did not touch REQUIREMENTS.md")

    # Check preflight
    preflight_path = repo_path(PREFLIGHT_REL, what="preflight records")
    if not preflight_path.is_file():
        fail(f"preflight records file is missing: {PREFLIGHT_REL}")
    preflight_sha = sha256_file(preflight_path)
    if protocol.get("preflight_sha256") != preflight_sha:
        fail(f"protocol preflight_sha256 {protocol.get('preflight_sha256')} != disk {preflight_sha}")

    # Check pinned modules
    module_shas = protocol.get("module_sha256")
    if not isinstance(module_shas, Mapping):
        fail("protocol module_sha256 is not a mapping")
    for mod_rel in PINNED_MODULES:
        if mod_rel not in module_shas:
            fail(f"pinned module {mod_rel} missing from protocol module_sha256")
        mod_path = repo_path(mod_rel, what=f"pinned module {mod_rel}")
        if not mod_path.is_file():
            fail(f"pinned module {mod_rel} does not exist")
        if not is_tracked(mod_rel) or not is_clean(mod_rel):
            fail(f"pinned module {mod_rel} is not tracked and clean")
        mod_disk_sha = sha256_file(mod_path)
        if mod_disk_sha != module_shas[mod_rel]:
            fail(f"pinned module {mod_rel} SHA-256 {mod_disk_sha} != pinned {module_shas[mod_rel]}")

    # Check 60-RUN-PROTOCOL.md
    doc_path = repo_path(PROTOCOL_DOC_REL, what="protocol doc")
    if not doc_path.is_file():
        fail(f"protocol doc {PROTOCOL_DOC_REL} is missing")
    if not is_tracked(str(PROTOCOL_DOC_REL)) or not is_clean(str(PROTOCOL_DOC_REL)):
        fail(f"protocol doc {PROTOCOL_DOC_REL} is not tracked and clean")
    doc_text = doc_path.read_text(encoding="utf-8")
    headings = re.findall(r"^## .+$", doc_text, re.M)
    if not headings or headings[0] != "## In plain language":
        fail(f"protocol doc {PROTOCOL_DOC_REL} does not open with ## In plain language")
    protocol_sha = sha256_file(protocol_path)
    if protocol_sha not in doc_text:
        fail(f"protocol doc {PROTOCOL_DOC_REL} does not cite protocol SHA-256 {protocol_sha}")

    print("PROTOCOL-OK")


def cmd_preflight(args: argparse.Namespace) -> None:
    preflight_path = repo_path(PREFLIGHT_REL, what="preflight records")
    if not preflight_path.is_file():
        fail(f"preflight records file is missing: {PREFLIGHT_REL}")
    if not is_tracked(str(PREFLIGHT_REL)) or not is_clean(str(PREFLIGHT_REL)):
        fail(f"preflight records file is not tracked and clean: {PREFLIGHT_REL}")
    preflight_text = preflight_path.read_text(encoding="utf-8")

    # Redaction checks
    home_str = str(Path.home())
    if home_str and home_str in preflight_text:
        fail("preflight records file contains home directory path")
    data_root = os.environ.get("THREEBODY_DATA_ROOT")
    if data_root and data_root in preflight_text:
        fail("preflight records file contains THREEBODY_DATA_ROOT path")

    payload = load_json(preflight_path, what="preflight records")
    if not isinstance(payload, Mapping):
        fail("preflight is not a JSON object")
    if payload.get("schema") != PREFLIGHT_SCHEMA:
        fail(f"preflight schema is not {PREFLIGHT_SCHEMA}")

    records = payload.get("records")
    if not isinstance(records, Mapping):
        fail("preflight records is not a mapping")

    expected_keys = {
        "hierarchical/gold/1632": 1001,
        "hierarchical/gold/851": 1001,
        "hierarchical/gold/4658": 1001,
        "hierarchical/base/1632": 126,
        "hierarchical/base/851": 126,
        "hierarchical/base/4658": 126,
        "standard/gold/2279": 1001,
        "standard/gold/3418": 1001,
        "standard/base/2279": 59,
        "standard/base/3418": 59,
    }
    if set(records.keys()) != set(expected_keys.keys()):
        fail(f"preflight records keys do not match expected ten assigned records: {sorted(records.keys())}")

    for key, expected_count in expected_keys.items():
        entry = records[key]
        if not isinstance(entry, Mapping):
            fail(f"preflight entry for {key} is not a mapping")
        if entry.get("status") != "ok":
            fail(f"preflight record {key} status is {entry.get('status')!r}, not 'ok'")
        if entry.get("n_within_t") != expected_count:
            fail(f"preflight record {key} count {entry.get('n_within_t')} != {expected_count}")
        if entry.get("count_ok") is not True:
            fail(f"preflight record {key} count_ok is not True")

    attestation = payload.get("attestation")
    if not isinstance(attestation, Mapping):
        fail("preflight attestation is not a mapping")
    for counter in ("test_split_opened", "blocked_attempts", "refused_before_open"):
        val = attestation.get(counter)
        if val != 0:
            fail(f"preflight attestation {counter} is {val}, expected 0")

    print("PREFLIGHT-OK")


def cmd_records(args: argparse.Namespace) -> None:
    arms_dir = repo_path(EVIDENCE_REL / "arms", what="evidence arms directory")
    if not arms_dir.is_dir():
        fail("evidence arms directory does not exist")

    protocol_path = repo_path(PROTOCOL_REL, what="run protocol")
    if not protocol_path.is_file():
        fail("protocol file missing")
    protocol_sha = sha256_file(protocol_path)

    succ_path = repo_path(SCORER_SUCCESSOR_REL, what="scorer successor")
    if not succ_path.is_file():
        fail("scorer successor file missing")
    succ_record = load_json(succ_path, what="scorer successor")
    scorer_successor_sha = succ_record.get("successor_sha256")

    ruling_path = repo_path(RULING4_REL, what="checkpoint 4 ruling")
    ruling_sha = sha256_file(ruling_path) if ruling_path.is_file() else None

    # Check owner stops without record
    for arm_entry in sorted(arms_dir.iterdir()):
        if not arm_entry.is_dir():
            continue
        owner_stop = arm_entry / "owner-stop.json"
        rec = arm_entry / "record.json"
        if owner_stop.is_file() and not rec.is_file():
            print(f"OWNER-STOP {arm_entry.name}")
            fail(f"owner-stop without record.json for {arm_entry.name}")

    if getattr(args, "arm", None):
        target_dirs = [arms_dir / args.arm]
        if not target_dirs[0].is_dir():
            fail(f"arm directory not found: {args.arm}")
    else:
        target_dirs = [d for d in sorted(arms_dir.iterdir()) if d.is_dir()]
        if not target_dirs:
            fail("no arm directories found under evidence/arms/")

    seen_arm_ids = set()
    for arm_dir in target_dirs:
        record_file = arm_dir / "record.json"
        if not record_file.is_file():
            fail(f"missing record.json in {arm_dir}")
        adam_weights = arm_dir / "adam.weights"
        if not adam_weights.is_file():
            fail(f"missing adam.weights in {arm_dir}")
        polish_weights = arm_dir / "polish.weights"
        if not polish_weights.is_file():
            fail(f"missing polish.weights in {arm_dir}")

        record = load_json(record_file, what=f"record.json in {arm_dir.name}")
        arm_id = record.get("arm_id")
        if not arm_id or arm_id != arm_dir.name:
            fail(f"record arm_id {arm_id!r} does not match directory {arm_dir.name}")
        if arm_id in seen_arm_ids:
            fail(f"duplicate record for arm {arm_id}")
        seen_arm_ids.add(arm_id)

        # Check all REQUIRED_REAL_FIELDS
        for field in REQUIRED_REAL_FIELDS:
            val = _lookup(record, field)
            if val is None:
                fail(f"arm {arm_id} record missing required field {field}")

        if record.get("seed") != 42:
            fail(f"arm {arm_id} seed is {record.get('seed')}, expected 42")
        if _lookup(record, "runtime.dtype") != "float32":
            fail(f"arm {arm_id} runtime.dtype is not float32")
        if _lookup(record, "runtime.device") != "mps":
            fail(f"arm {arm_id} runtime.device is not mps")
        if record.get("run_kind") != "real":
            fail(f"arm {arm_id} run_kind is not real")
        if record.get("diagnostic") is not True:
            fail(f"arm {arm_id} diagnostic is not True")
        if record.get("protocol_sha256") != protocol_sha:
            fail(f"arm {arm_id} protocol_sha256 does not match current protocol")
        if record.get("scorer_sha256") != scorer_successor_sha:
            fail(f"arm {arm_id} scorer_sha256 does not match scorer successor")

        adam_sha = sha256_file(adam_weights)
        if _lookup(record, "states.adam.weights.sha256") != adam_sha:
            fail(f"arm {arm_id} adam.weights SHA mismatch")
        polish_sha = sha256_file(polish_weights)
        if _lookup(record, "states.polish.weights.sha256") != polish_sha:
            fail(f"arm {arm_id} polish.weights SHA mismatch")

        # Attestation zeros
        for counter in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            val = _lookup(record, f"attestation.{counter}")
            if val != 0:
                fail(f"arm {arm_id} attestation {counter} is {val}, expected 0")

        # Continue arm ruling check
        if arm_id.startswith("c-"):
            rec_ruling_sha = _lookup(record, "ruling.sha256")
            if not rec_ruling_sha:
                fail(f"continue arm {arm_id} missing ruling.sha256")
            if ruling_sha is None or rec_ruling_sha != ruling_sha:
                fail(f"continue arm {arm_id} ruling SHA {rec_ruling_sha} != committed ruling {ruling_sha}")

    print("RECORDS-OK")


def cmd_g2(args: argparse.Namespace) -> None:
    g2_dir = repo_path(EVIDENCE_REL / "g2", what="evidence g2 directory")

    required_tokens = None
    if getattr(args, "require", None) is not None:
        raw_tokens = args.require.split(",")
        if not raw_tokens or any(len(t) == 0 for t in raw_tokens):
            fail(f"FAIL-CLOSED: empty token in --require {args.require!r}")
        seen = set()
        for t in raw_tokens:
            if t not in G2_TOKENS:
                fail(f"FAIL-CLOSED: unknown token in --require: {t!r}")
            if t in seen:
                fail(f"FAIL-CLOSED: repeated token in --require: {t!r}")
            seen.add(t)
        required_tokens = seen

    arms_dir = repo_path(EVIDENCE_REL / "arms", what="arms directory")

    def _arm_record(arm_id: str) -> Optional[dict]:
        p = arms_dir / arm_id / "record.json"
        if p.is_file():
            return load_json(p, what=f"record for {arm_id}")
        return None

    # outcome check
    outcome_file = g2_dir / "g2-outcome.json"
    outcome_data = None
    if outcome_file.is_file():
        outcome_data = load_json(outcome_file, what="g2-outcome.json")
        if not isinstance(outcome_data, Mapping) or outcome_data.get("schema") != OUTCOME_SCHEMA:
            fail("g2-outcome.json does not carry phase60-g2-outcome/v1 schema")
        r1_records = [_arm_record(f"r1-{s}") for s in PANEL_SYSTEMS]
        if all(r is not None for r in r1_records):
            tiers = tuple(r["result"]["tier"] for r in r1_records)
            card = load_scorecard()
            expected_fired = g2_fires(tiers, scorecard=card)
            if outcome_data.get("g2_fired") != expected_fired:
                fail(f"g2-outcome.json g2_fired {outcome_data.get('g2_fired')} != recomputed {expected_fired}")
            if expected_fired:
                failing = [s for s, t in zip(PANEL_SYSTEMS, tiers) if t < 1]
                sw, co, un = sweep_plan(failing)
                if outcome_data.get("sweep_system") != sw:
                    fail("g2-outcome.json sweep_system mismatch")
                if outcome_data.get("confirmation_system") != co:
                    fail("g2-outcome.json confirmation_system mismatch")
                if outcome_data.get("uncovered_system") != un:
                    fail("g2-outcome.json uncovered_system mismatch")

    # sweep-curve check
    curve_file = g2_dir / "sweep-curve.json"
    curve_data = None
    if curve_file.is_file():
        curve_data = load_json(curve_file, what="sweep-curve.json")
        if not isinstance(curve_data, Mapping) or curve_data.get("schema") != CURVE_SCHEMA:
            fail("sweep-curve.json does not carry phase60-sweep-curve/v1 schema")
        sweep_sys = curve_data.get("sweep_system")
        grid_omegas = [60.0, 120.0, 240.0, 480.0]
        curve_points = []
        for w in grid_omegas:
            arm_id = f"g2s-{sweep_sys}-w{int(w):03d}"
            r = _arm_record(arm_id)
            if r is not None:
                curve_points.append((w, r["result"]["tier"]))
        if len(curve_points) == 4:
            card = load_scorecard()
            rows = [{"first_omega_0": w, "tier": t} for w, t in curve_points]
            expected_conf = confirmed_omega(rows, scorecard=card)
            if curve_data.get("confirmed_first_omega_0") != expected_conf:
                fail("sweep-curve.json confirmed_first_omega_0 mismatch")

    # rescue check
    rescue_file = g2_dir / "rescue.json"
    rescue_data = None
    if rescue_file.is_file():
        rescue_data = load_json(rescue_file, what="rescue.json")
        if not isinstance(rescue_data, Mapping) or rescue_data.get("schema") != RESCUE_SCHEMA:
            fail("rescue.json does not carry phase60-rescue/v1 schema")

    # skip-records check
    skip_file = g2_dir / "skip-records.json"
    skip_data = None
    if skip_file.is_file():
        skip_data = load_json(skip_file, what="skip-records.json")
        if not isinstance(skip_data, Mapping) or skip_data.get("schema") != SKIP_SCHEMA:
            fail("skip-records.json does not carry phase60-skip-records/v1 schema")
        reason = skip_data.get("reason")
        if reason not in SKIP_REASONS:
            fail(f"skip-records.json reason {reason!r} not in {SKIP_REASONS}")
        forbidden_prefixes = ("r2a-", "r2b-", "c-r1u-", "c-r2a-", "c-r2b-", "p1-", "p2b-", "c-p1-", "c-p2b-")
        if arms_dir.is_dir():
            for d in arms_dir.iterdir():
                if d.is_dir() and any(d.name.startswith(p) for p in forbidden_prefixes):
                    fail(f"skip-records.json exists beside later arm directory {d.name}")

    # stop-handoff check
    handoff_file = g2_dir / "stop-handoff.json"
    handoff_data = None
    if handoff_file.is_file():
        handoff_data = load_json(handoff_file, what="stop-handoff.json")
        if not isinstance(handoff_data, Mapping) or handoff_data.get("schema") != HANDOFF_SCHEMA:
            fail("stop-handoff.json does not carry phase60-stop-handoff/v1 schema")
        if handoff_data.get("stop_reason") == "checkpoint ④ answered go to the verdict":
            expected_verdict = None
        else:
            card = load_scorecard()
            expected_verdict = decision_verdict(
                g2_fired=True,
                sweep_rescued=False,
                rung2b_counts=None,
                rung3_counts=None,
                control_branch=None,
                rung1_beats_formula=None,
                scorecard=card,
            )
        if handoff_data.get("verdict") != expected_verdict:
            fail(f"stop-handoff.json verdict {handoff_data.get('verdict')!r} != {expected_verdict!r}")

    # Check requirements
    if required_tokens is not None:
        for t in required_tokens:
            fname = G2_TOKENS[t]
            fpath = g2_dir / fname
            if not fpath.is_file():
                fail(f"FAIL-CLOSED: required g2 file {fname} is missing")
    else:
        if outcome_data is None:
            fail("g2-outcome.json is missing")
        g2_fired = outcome_data.get("g2_fired")

        all_possible = set(G2_TOKENS.values())
        if not g2_fired:
            expected_files = {"g2-outcome.json"}
        else:
            if curve_data is None:
                fail("sweep-curve.json is missing")
            curve_outcome = curve_data.get("outcome")
            if curve_outcome == "no_rescue":
                expected_files = {"g2-outcome.json", "sweep-curve.json", "skip-records.json", "stop-handoff.json"}
            elif curve_outcome == "confirmation_pending":
                if rescue_data is None:
                    fail("rescue.json is missing")
                rescue_outcome = rescue_data.get("outcome")
                proto = load_json(repo_path(PROTOCOL_REL, what="protocol"), what="protocol")
                pre_ans = proto.get("g2", {}).get("failed_confirmation_pre_answer")

                gap6009_ruling = None
                try:
                    gap6009_ruling = load_gap6009_ruling(repo_root=REPO_ROOT)
                except (RulingMissing, RulingUncommitted):
                    gap6009_ruling = None

                cp4_ruling = None
                try:
                    cp4_ruling = load_checkpoint4_ruling(repo_root=REPO_ROOT)
                except (RulingMissing, RulingUncommitted):
                    cp4_ruling = None

                is_stop = False
                is_continue = False

                if rescue_outcome == "failed_confirmation":
                    if pre_ans == "no_rescue" or (gap6009_ruling and gap6009_ruling.reading == "no_rescue"):
                        is_stop = True
                    elif pre_ans == "rescue" or (gap6009_ruling and gap6009_ruling.reading == "rescue"):
                        if cp4_ruling:
                            if cp4_ruling.answer == "go-to-verdict":
                                is_stop = True
                            elif cp4_ruling.answer == "continue":
                                is_continue = True
                    else:
                        fail("failed confirmation has neither a pre-answer nor a GAP-60-09 ruling")
                elif rescue_outcome == "rescue":
                    if cp4_ruling:
                        if cp4_ruling.answer == "go-to-verdict":
                            is_stop = True
                        elif cp4_ruling.answer == "continue":
                            is_continue = True
                    else:
                        fail("rescue has no checkpoint 4 ruling")
                else:
                    fail(f"unknown rescue outcome {rescue_outcome!r}")

                if is_stop:
                    expected_files = {"g2-outcome.json", "sweep-curve.json", "rescue.json", "skip-records.json", "stop-handoff.json"}
                elif is_continue:
                    expected_files = {"g2-outcome.json", "sweep-curve.json", "rescue.json"}
                else:
                    fail("not yet decidable")
            else:
                fail(f"unknown sweep curve outcome {curve_outcome!r}")

        forbidden_files = all_possible - expected_files
        for ef in expected_files:
            if not (g2_dir / ef).is_file():
                fail(f"missing implied g2 file {ef}")
        for ff in forbidden_files:
            if (g2_dir / ff).is_file():
                fail(f"unexpected g2 file {ff} present on disk")

    print("G2-OK")


def cmd_rescore(args: argparse.Namespace) -> None:
    arms_dir = repo_path(EVIDENCE_REL / "arms", what="evidence arms directory")
    if not arms_dir.is_dir():
        fail("evidence arms directory does not exist")

    if getattr(args, "arm", None):
        target_dirs = [arms_dir / args.arm]
        if not target_dirs[0].is_dir():
            fail(f"arm directory not found: {args.arm}")
    else:
        target_dirs = [d for d in sorted(arms_dir.iterdir()) if d.is_dir()]
        if not target_dirs:
            fail("no arm directories found under evidence/arms/")

    card = load_scorecard()
    # learnability_data.open_real_context returns a plain DataContext (not a context manager);
    # the process-wide attestation counts every open, so one context serves all arms.
    ctx = open_real_context(repo_root=REPO_ROOT)
    for arm_dir in target_dirs:
        record_file = arm_dir / "record.json"
        if not record_file.is_file():
            fail(f"missing record.json in {arm_dir}")
        record = load_json(record_file, what=f"record for {arm_dir.name}")
        spec = arm_spec(record["arm_id"])
        first_omega_0 = float(record["first_omega_0"])

        arm_data = load_arm_data(spec, ctx, scorecard=card, dtype=torch.float32, device="cpu")
        attestation = ctx.attestation
        if attestation is None or attestation.test_split_opened != 0:
            fail(f"rescore opened the test split, or has no open attestation, for {arm_dir.name}")

        for state_name in ("adam", "polish"):
            weights_path = arm_dir / f"{state_name}.weights"
            try:
                weights = torch.load(weights_path, map_location="cpu", weights_only=True)
            except Exception as exc:  # noqa: BLE001
                fail(f"cannot load weights {weights_path}: {exc}")
            if not isinstance(weights, Mapping):
                fail(f"weights {weights_path} is not a mapping")

            f_sha = sha256_file(weights_path)
            t_digest = weights_digest(weights)
            rec_weights = record["states"][state_name]["weights"]
            if f_sha != rec_weights["sha256"]:
                fail(f"weights SHA mismatch for {arm_dir.name} {state_name}")
            if t_digest != rec_weights["tensor_digest"]:
                fail(f"weights tensor digest mismatch for {arm_dir.name} {state_name}")

            widened = OrderedDict(
                (name, tensor.detach().to("cpu").to(torch.float64))
                for name, tensor in weights.items()
            )
            if abs(first_omega_0 - 30.0) < 1e-9:
                cpu_model = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device="cpu")
            else:
                cpu_model = build_network_with_first_omega(first_omega_0, seed=SEED, dtype=torch.float64, device="cpu")
            cpu_model.load_state_dict(widened)

            cpu_result = score_network(
                cpu_model,
                _float32_rounded(arm_data.ic13),
                _float32_rounded(arm_data.masses),
                arm_data.score.positions,
                arm_data.score.inner_pair,
                arm_data.score.times,
                scorecard=card,
                dtype=torch.float64,
                device=torch.device("cpu"),
                grid=arm_data.score.grid,
            )
            rec_cross = record["states"][state_name]["cross_check"]
            if cpu_result.tier != rec_cross["tier"]:
                fail(f"cross check tier mismatch for {arm_dir.name} {state_name}: {cpu_result.tier} != {rec_cross['tier']}")
            if abs(cpu_result.E - rec_cross["E"]) > 1e-12:
                fail(f"cross check E mismatch for {arm_dir.name} {state_name}: {cpu_result.E} != {rec_cross['E']}")
            if abs(cpu_result.eps_h - rec_cross["eps_h"]) > 1e-12:
                fail(f"cross check eps_h mismatch for {arm_dir.name} {state_name}: {cpu_result.eps_h} != {rec_cross['eps_h']}")

            if not getattr(args, "cpu_only", False):
                mps_device = torch.device("mps")
                if abs(first_omega_0 - 30.0) < 1e-9:
                    mps_model = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float32, device=mps_device)
                else:
                    mps_model = build_network_with_first_omega(first_omega_0, seed=SEED, dtype=torch.float32, device=mps_device)
                mps_model.load_state_dict(weights)
                mps_result = score_network(
                    mps_model,
                    arm_data.ic13,
                    arm_data.masses,
                    arm_data.score.positions,
                    arm_data.score.inner_pair,
                    arm_data.score.times,
                    scorecard=card,
                    dtype=torch.float32,
                    device=mps_device,
                    grid=arm_data.score.grid,
                )
                rec_score = record["states"][state_name]["score_gold"]
                if mps_result.tier != rec_score["tier"]:
                    fail(f"MPS gold tier mismatch for {arm_dir.name} {state_name}: {mps_result.tier} != {rec_score['tier']}")
                if state_name == record.get("better_state") and spec.counted:
                    c = counts(mps_result.tier, mps_result.E, record["formula"]["E_formula"], scorecard=card)
                    if c != record["formula"]["counts"]:
                        fail(f"MPS counts mismatch for {arm_dir.name}")

    print("RESCORE-OK")


def cmd_final(args: argparse.Namespace) -> None:
    cmd_protocol(args)
    cmd_preflight(args)
    records_args = argparse.Namespace(arm=None)
    cmd_records(records_args)
    g2_args = argparse.Namespace(require=None)
    cmd_g2(g2_args)
    print("PHASE60-EVIDENCE-OK")


COMMANDS = {
    "protocol": cmd_protocol,
    "preflight": cmd_preflight,
    "records": cmd_records,
    "g2": cmd_g2,
    "rescore": cmd_rescore,
    "final": cmd_final,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=tuple(COMMANDS))
    parser.add_argument("--arm", default=None)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--cpu-only", action="store_true")
    parser.add_argument("--require", default=None)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        COMMANDS[args.command](args)
    except Exception as exc:  # noqa: BLE001 - fail-closed CLI
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
