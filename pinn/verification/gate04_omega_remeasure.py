"""Phase 60 (D-07): re-measure R_ref and re-run GATE-04 at an owner-approved first_omega_0.

If the owner continues at checkpoint 4 and names a first-layer frequency, the physics term's
reference scale (``R_ref``) has to be measured again at that setting, and the train-free
GATE-04 starting-point check has to pass again, before any physics arm runs. Neither step
trains. This module does both from the committed owner ruling and writes only Phase 60
files, so it cannot overwrite the Stage-0 reference that the trainer, the scorer and the
baselines read (GAP-60-10, Pitfall 9).

``remeasure`` does the following, in order, and stops at the first refusal with nothing
measured:

1. Loads the committed checkpoint 4 ruling through ``learnability_ruling`` (tracked, clean,
   strict block). Only ``continue`` goes on. The approved value is checked again here to be
   finite and positive, because ``run_gate`` turns every exception into a BLOCK verdict and a
   bad frequency would otherwise read as a scientific result (Hazard 5).
2. Reads the setting the committed sweep curve confirmed, and records whether the approved
   setting is on the sweep grid and whether it equals the confirmed one (GAP-60-11). Any
   finite positive setting the owner names is accepted.
3. Hashes the governed ``r_ref_stage0.json``, runs ``run_gate`` over the six default cases at
   the approved setting on the CPU in float64, and hashes the governed file again.
4. Writes, under ``<evidence root>/continue/``: the gate evidence (the case records and the
   verdict, in the GATE-04 command line's own evidence shape), on a complete PASS the
   re-measured reference ``r-ref-approved.json``, and last ``gate04-remeasure.json``.

A complete PASS is the gate's own definition: the six canonical default cases, verdict PASS,
no blocking reasons and no unratified conditions. Its pass rule is the ratified one of
57-RULING.md (GAP-56-01): a non-anchor spread of at least 2:1, then the fixed residual
reduction. Anything else is recorded as BLOCK, with no reference written; a BLOCK stops the
work for the owner.

What it never does: it never calls the GATE-04 command line, which overwrites the governed
reference on a PASS and writes a Phase 57 terminal state on a BLOCK; it never writes the
governed file or a terminal state; it never imports the arm runner; and no absolute path
enters any file it writes (every recorded path is relative to the repository).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import numbers
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

from pinn.verification import evidence_io
from pinn.verification import learnability_g2 as g2
from pinn.verification.architecture_characterization_probe import DEFAULT_CASES
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.gate04_train_free import (
    EVIDENCE_SCHEMA_VERSION,
    R_REF_ARTIFACT_PATH,
    VERDICT_BLOCK,
    VERDICT_PASS,
    _case_record,
    _verdict_record,
    run_gate,
    write_r_ref_artifact,
)
from pinn.verification.learnability_arms import EVIDENCE_REL, write_record_exclusive
from pinn.verification.learnability_ruling import (
    RulingError,
    load_checkpoint4_ruling,
    ruling_grid_facts,
    tracked_and_clean,
)
from pinn.verify import git_head

__all__ = [
    "EXIT_BLOCK",
    "EXIT_PASS",
    "EXIT_REFUSED",
    "REMEASURE_SCHEMA",
    "RemeasureHalt",
    "RemeasureRefused",
    "remeasure",
]

_REPO_ROOT = Path(__file__).resolve().parents[2]

EXIT_PASS = 0
EXIT_REFUSED = 2
EXIT_BLOCK = 5
# The record schema is owned by learnability_g2, which reads it back in the branch query.
REMEASURE_SCHEMA = g2.REMEASURE_SCHEMA

GATE_EVIDENCE_NAME = "gate04-evidence.json"
_COMMAND = "python -B -m pinn.verification.gate04_omega_remeasure"
# Locations below the evidence root, taken from the constants learnability_g2 reads them by.
_RECORD_PARTS = g2.REMEASURE_REL.relative_to(EVIDENCE_REL).parts
_APPROVED_PARTS = g2.R_REF_APPROVED_REL.relative_to(EVIDENCE_REL).parts
_EVIDENCE_PARTS = _RECORD_PARTS[:-1] + (GATE_EVIDENCE_NAME,)
_CURVE_PARTS = g2.G2_REL.relative_to(EVIDENCE_REL).parts + (g2.CURVE_NAME,)


class RemeasureRefused(RuntimeError):
    """A precondition failed. Nothing was measured and nothing was written."""


class RemeasureHalt(RuntimeError):
    """The governed Stage-0 reference changed while the re-measure ran. No record is written."""


# ---------------------------------------------------------------------------
# Paths and committed inputs.
# ---------------------------------------------------------------------------

def _repo_root_of(path):
    """The git top level above ``path`` (which need not exist yet)."""
    probe = Path(path).resolve()
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    if probe.is_file():
        probe = probe.parent
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(probe), capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        raise RemeasureRefused("the evidence root is not inside a git repository")
    return Path(completed.stdout.strip()).resolve()


def _resolve_roots(repo_root, evidence_root):
    """``(repository root, evidence root)``: the module's own repository unless told otherwise."""
    if evidence_root is None:
        root = _REPO_ROOT if repo_root is None else Path(repo_root).resolve()
        return root, root / EVIDENCE_REL
    evidence = Path(evidence_root)
    root = _repo_root_of(evidence) if repo_root is None else Path(repo_root).resolve()
    return root, evidence


def _relative(root, path):
    """``path`` relative to the repository, as posix text."""
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError as exc:
        raise RemeasureRefused(f"{Path(path).name} lies outside the repository") from exc


def _sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _approved_setting(root, ruling_path):
    """``(ruling, first_omega_0)`` of a committed checkpoint 4 ruling that says continue."""
    try:
        ruling = load_checkpoint4_ruling(repo_root=root, path=ruling_path, require_committed=True)
    except RulingError as exc:
        raise RemeasureRefused(f"the checkpoint 4 ruling cannot be used: {exc}") from exc
    if ruling.answer != "continue":
        raise RemeasureRefused(
            f"checkpoint 4 was answered {ruling.answer}, so there is nothing to re-measure"
        )
    value = ruling.approved_first_omega_0
    if (
        isinstance(value, bool)
        or not isinstance(value, numbers.Real)
        or not math.isfinite(value)
        or value <= 0.0
    ):
        raise RemeasureRefused(
            f"the approved first_omega_0 must be a finite positive real number; got {value!r}"
        )
    return ruling, float(value)


def _confirmed_first_omega_0(root, evidence):
    """The setting the committed sweep curve confirmed, or None when the sweep confirmed nothing."""
    path = evidence.joinpath(*_CURVE_PARTS)
    relative = _relative(root, path)
    if not path.is_file():
        raise RemeasureRefused(f"{relative} is not recorded")
    if not tracked_and_clean(root, relative):
        raise RemeasureRefused(f"uncommitted {relative}")
    try:
        payload = json.loads(path.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RemeasureRefused(f"{relative} is not valid JSON") from exc
    if not isinstance(payload, dict) or "confirmed_first_omega_0" not in payload:
        raise RemeasureRefused(f"{relative} has no confirmed_first_omega_0")
    confirmed = payload["confirmed_first_omega_0"]
    if confirmed is not None and (
        isinstance(confirmed, bool)
        or not isinstance(confirmed, numbers.Real)
        or not math.isfinite(confirmed)
    ):
        raise RemeasureRefused(f"{relative} holds a confirmed_first_omega_0 that is not a number")
    return confirmed


# ---------------------------------------------------------------------------
# The re-measure.
# ---------------------------------------------------------------------------

def _complete_pass(verdict, case_tuple):
    """The gate's own definition (``gate04_train_free.main``), plus whether the case set is canonical."""
    default_ids = tuple((case.label, case.seed) for case in DEFAULT_CASES)
    observed_ids = tuple((case.label, case.seed) for case in verdict.cases)
    canonical = case_tuple == tuple(DEFAULT_CASES) and observed_ids == default_ids
    complete = bool(
        canonical
        and verdict.verdict == VERDICT_PASS
        and not verdict.blocking_reasons
        and not verdict.unratified_conditions
    )
    return complete, canonical


def _blocking_reasons(verdict, *, canonical):
    """The gate's reasons, plus the reason a gate PASS is still not a complete pass."""
    reasons = list(verdict.blocking_reasons)
    if verdict.verdict == VERDICT_PASS:
        if not canonical:
            reasons.append(
                "not a complete pass: the case set is not the six canonical default cases in order"
            )
        if verdict.unratified_conditions:
            reasons.append(
                "not a complete pass: unratified conditions "
                + ", ".join(verdict.unratified_conditions)
            )
    return reasons


def _gate_evidence(verdict, *, omega, ruling, evidence_root_rel, approved_rel):
    """The case records and the verdict, in the shape GATE-04's own command line records them."""
    git_sha, git_available = git_head()
    return {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "provenance": {
            "command": _COMMAND,
            "first_omega_0": omega,
            "ruling_path": ruling.path,
            "ruling_sha256": ruling.sha256,
            "git_sha": git_sha,
            "git_available": git_available,
            "torch_version": torch.__version__,
            "numpy_version": np.__version__,
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        },
        "configuration": {
            "precision": "float64",
            "device": "cpu",
            "cases_config": None,
            "first_omega_0": omega,
            "evidence_root": evidence_root_rel,
            "r_ref_path": approved_rel,
        },
        "verdict": _verdict_record(verdict),
        "cases": [_case_record(case) for case in verdict.cases],
        "failure": None,
    }


def remeasure(*, ruling_path=None, evidence_root=None, repo_root=None, cases=None):
    """Re-measure ``R_ref`` and re-run GATE-04 at the committed ruling's approved setting.

    ``ruling_path`` is for tests (the fixed ``60-CHECKPOINT-4-RULING.md`` by default), and so
    are ``repo_root`` and ``cases`` (the six default cases by default). ``evidence_root``
    defaults to the Phase 60 evidence tree of this repository. Returns the record that was
    written to ``<evidence root>/continue/gate04-remeasure.json``. Raises ``RemeasureRefused``
    before any measurement when a precondition fails.
    """
    root, evidence = _resolve_roots(repo_root, evidence_root)
    case_tuple = tuple(DEFAULT_CASES if cases is None else cases)
    ruling, omega = _approved_setting(root, ruling_path)
    confirmed = _confirmed_first_omega_0(root, evidence)
    facts = ruling_grid_facts(ruling, scorecard=load_scorecard(), confirmed_first_omega_0=confirmed)

    record_path = evidence.joinpath(*_RECORD_PARTS)
    approved_path = evidence.joinpath(*_APPROVED_PARTS)
    evidence_path = evidence.joinpath(*_EVIDENCE_PARTS)
    approved_rel = _relative(root, approved_path)
    evidence_rel = _relative(root, evidence_path)

    governed_before = _sha256_file(R_REF_ARTIFACT_PATH)
    started = time.monotonic()
    verdict = run_gate(case_tuple, precision="float64", device="cpu", first_omega_0=omega)
    wall_seconds = time.monotonic() - started

    complete, canonical = _complete_pass(verdict, case_tuple)
    evidence_sha = evidence_io.write_json(
        evidence_path,
        _gate_evidence(
            verdict, omega=omega, ruling=ruling,
            evidence_root_rel=_relative(root, evidence), approved_rel=approved_rel,
        ),
    )
    artifact = None
    if complete:
        evidence_io.reject_evidence_root(approved_path)
        write_r_ref_artifact(
            verdict, path=approved_path,
            gate_evidence_path=evidence_rel, gate_evidence_sha256=evidence_sha,
        )
        artifact = {"path": approved_rel, "sha256": _sha256_file(approved_path)}

    governed_after = _sha256_file(R_REF_ARTIFACT_PATH)
    if governed_after != governed_before:
        raise RemeasureHalt(
            "the governed Stage-0 reference changed while the re-measure ran; no record is written"
        )
    record = {
        "schema": REMEASURE_SCHEMA,
        "first_omega_0": omega,
        "ruling_path": ruling.path,
        "ruling_sha256": ruling.sha256,
        "verdict": VERDICT_PASS if complete else VERDICT_BLOCK,
        "complete_pass": complete,
        "blocking_reasons": _blocking_reasons(verdict, canonical=canonical),
        "unratified_conditions": list(verdict.unratified_conditions),
        "r_ref": verdict.r_ref,
        "r_ref_artifact": artifact,
        "governed_r_ref_sha256": {"before": governed_before, "after": governed_after},
        "on_grid": facts["on_grid"],
        "equals_confirmed": facts["equals_confirmed"],
        "wall_seconds": wall_seconds,
    }
    write_record_exclusive(record_path, record)
    return record
