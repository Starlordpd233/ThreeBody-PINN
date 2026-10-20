"""Phase 60 (SPEC R4): the run protocol, the record preflight and real-arm admission.

Before the first real experiment the project writes down exactly how every experiment
will run, and fingerprints the code that will run it. Each experiment then refuses to
start if anything changed, if its data file is missing, or if the earlier results say
it should not run. This module holds the pieces of that pre-registration:

* ``build_protocol``, ``write_protocol`` and ``load_protocol``: the run protocol
  (``evidence/run-protocol.json``). Every value in it comes from the code's own
  constants, the frozen scorecard or the committed Phase 59 and Phase 60 evidence the
  plan names, never from a number chosen here. It pins the SHA-256 of every module and
  artifact a real arm executes or reads, so ``load_protocol`` can refuse any drift: the
  code that runs is the code that was pre-registered.
* ``write_preflight``: the record of every assigned data file, checked before the first
  arm, with no substitute for a missing, empty or unreadable record.
* ``admit_arm``: the check every real arm passes before it starts. It loads the
  protocol, the preflight and the committed branch records, and returns what the arm
  must cite.

The module never imports the arm runner (the runner imports this module). It decides
only from files that are tracked and clean in git, and every record it writes holds
repo-relative paths and digests only.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pinn.training.config import (
    R_REF_ARTIFACT_RELATIVE_PATH,
    OptConfig,
    load_frozen_r_ref_artifact,
)
from pinn.training.grad_clip import DEFAULT_C_STAGE_TABLE, DEFAULT_MEDIAN_FLOOR
from pinn.verification import evidence_io
from pinn.verification.feasibility_scorecard import (
    SCORECARD_RELATIVE_PATH,
    SCORECARD_SHA256,
    load_scorecard,
)
from pinn.verification.learnability_arms import (
    CROSS_CHECK_RUNTIME,
    EVIDENCE_REL,
    EXIT_OK,
    EXIT_REFUSED,
    FORMULA_NOT_APPLICABLE,
    PANEL_INNER_LAPS,
    PANEL_SYSTEMS,
    PHASE_REL,
    PROBE_STAGES,
    REAL_RUNTIME,
    RUNS_REL,
    SEED,
    SEQUENCES,
    TIMING_STEPS,
    FirstResultExists,
    OverrideRefused,
    UnknownArm,
    arm_evidence_dir,
    arm_run_dir,
    arm_spec,
    catalog,
    check_override,
    resolve_first_omega_0,
    write_record_exclusive,
)
from pinn.verification.learnability_data import (
    EXPECTED_STATS_SHA256,
    HarnessHalt,
    open_real_context,
    preflight_records,
)
from pinn.verification.learnability_g2 import (
    NOT_CONFIRMED_LABEL,
    PRE_ANSWERS,
    REMEASURE_REL,
    R_REF_APPROVED_REL,
    SKIP_REASONS,
    TAKEN,
    G2Halt,
    G2Pending,
    branch_state,
    parse_remeasure,
    sweep_plan,
)
from pinn.verification.learnability_ruling import (
    RULING4_REL,
    RulingError,
    load_checkpoint4_ruling,
    ruling_grid_facts,
    tracked_and_clean,
)

__all__ = [
    "PINNED_MODULES",
    "PREFLIGHT_REL",
    "PREFLIGHT_SCHEMA",
    "PROTOCOL_DOC_REL",
    "PROTOCOL_REL",
    "PROTOCOL_SCHEMA",
    "AdmissionRefused",
    "LoadedProtocol",
    "ProtocolDrift",
    "admit_arm",
    "build_protocol",
    "load_protocol",
    "main",
    "write_preflight",
    "write_protocol",
]

_REPO_ROOT = Path(__file__).resolve().parents[2]

PROTOCOL_SCHEMA = "phase60-run-protocol/v1"
PREFLIGHT_SCHEMA = "phase60-preflight/v1"
PROTOCOL_REL = EVIDENCE_REL / "run-protocol.json"
PROTOCOL_DOC_REL = PHASE_REL / "60-RUN-PROTOCOL.md"
PREFLIGHT_REL = EVIDENCE_REL / "preflight" / "records.json"

SCORER_SUCCESSOR_REL = EVIDENCE_REL / "scorer-successor.json"
SCORER_REL = "pinn/verification/feasibility_scorer.py"
SCORECARD_REL = SCORECARD_RELATIVE_PATH.as_posix()
R_REF_GOVERNED_REL = R_REF_ARTIFACT_RELATIVE_PATH
_PHASE59_EVIDENCE = Path(".planning/phases/59-read-only-baseline-scorecard/evidence")
PANELS_REL = _PHASE59_EVIDENCE / "census" / "panels.json"
PICKS_REL = _PHASE59_EVIDENCE / "survey" / "picks.json"
TWO_KEPLER_REL = _PHASE59_EVIDENCE / "baselines" / "two_kepler.json"
STAGE0_METADATA_REL = Path("runs/stage0-v23g7-seed42/training_metadata.json")

# GAP-60-12: the energy-term scale the generation-7 run computed once and saved.
EXPECTED_S_H = 22.321729071058996
EXPECTED_EPS_H = 0.0022321729071058997

# Every module and artifact a real arm executes or reads. The protocol pins the SHA-256
# of each, so a changed file is drift and the arm does not start.
PINNED_MODULES = (
    "pinn/verification/learnability_arms.py",
    "pinn/verification/learnability_data.py",
    "pinn/verification/learnability_losses.py",
    "pinn/verification/learnability_run.py",
    "pinn/verification/learnability_g2.py",
    "pinn/verification/learnability_ruling.py",
    "pinn/verification/learnability_protocol.py",
    "pinn/verification/diagnostic_architecture.py",
    "pinn/verification/gate04_omega_remeasure.py",
    "pinn/verification/gate04_train_free.py",
    "pinn/verification/feasibility_scorer.py",
    "pinn/verification/feasibility_scorecard.py",
    "pinn/verification/production_reference.py",
    "pinn/verification/split_allowlist.py",
    "pinn/verification/evidence_io.py",
    "pinn/loss_catalog.py",
    "pinn/physics_residual.py",
    "pinn/network.py",
    "pinn/architecture_spec.py",
    "pinn/constants.py",
    "pinn/training/controllers.py",
    "pinn/training/config.py",
    "pinn/training/grad_clip.py",
    "pinn/training/scheduled_weights.py",
    "pinn/training/determinism.py",
    "pinn/training/atomic_io.py",
    "pinn/training/signals.py",
    "pinn/data/batches.py",
    "pinn/data/preprocessing.py",
    "pinn/data/types.py",
    SCORECARD_REL,
    R_REF_GOVERNED_REL,
    (EVIDENCE_REL / "launch_phase60_arm.py").as_posix(),
)

# SPEC Requirement 8 and 60-RESEARCH Finding G: the number of samples within T = 10 of each
# assigned record, by variant and fidelity (gold 1,001, hierarchical base 126, standard
# base 59). A record whose window holds another count is not the record that was verified.
EXPECTED_WITHIN_T = {
    "hierarchical/gold": 1001,
    "hierarchical/base": 126,
    "standard/gold": 1001,
    "standard/base": 59,
}
# SPEC Requirement 5 and INST-05(b): zero opens of any test-split file, none blocked or refused.
_OPEN_COUNTERS = ("test_split_opened", "blocked_attempts", "refused_before_open")

_COMMIT = re.compile(r"[0-9a-f]{40}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_REFERENCE_NOTE = "Stage-0 reference in force, applied unchanged"


class ProtocolDrift(RuntimeError):
    """A pinned file, or the protocol itself, is not what was pre-registered.

    ``paths`` names the repo-relative files that differ. The same type reports a
    protocol that is absent, uncommitted or malformed, because in every case the
    registered procedure cannot be shown to be the one that would run.
    """

    def __init__(self, message, paths=()):
        super().__init__(message)
        self.paths = tuple(str(path) for path in paths)


class AdmissionRefused(RuntimeError):
    """An arm may not start now. The message says why, in one line."""


@dataclass(frozen=True)
class LoadedProtocol:
    """A protocol that passed ``load_protocol``: its content, file digest and location."""

    payload: dict
    sha256: str
    path: str


def _drift(message, paths):
    paths = [str(path) for path in paths]
    return ProtocolDrift(f"{message}: {', '.join(paths)}" if paths else message, paths)


def _one_line(exc):
    return " ".join(str(exc).split())


# ---------------------------------------------------------------------------
# Small file helpers.
# ---------------------------------------------------------------------------

def _roots(repo_root, evidence_root):
    root = _REPO_ROOT if repo_root is None else Path(repo_root).resolve()
    evidence = root / EVIDENCE_REL if evidence_root is None else Path(evidence_root)
    return root, evidence


def _relative(root, path):
    """``path`` relative to ``root`` as posix text, or ``None`` when it lies outside."""
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return None


def _sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def _file_sha256(path):
    """SHA-256 of a file's bytes, or ``None`` when it cannot be read."""
    try:
        return _sha256(Path(path).read_bytes())
    except OSError:
        return None


def _json_form(payload):
    """``payload`` as it reads back from a canonical JSON file (plain JSON types only)."""
    return json.loads(evidence_io.canonical_json_bytes(payload))


def _check_commit(value):
    if not isinstance(value, str) or _COMMIT.fullmatch(value) is None:
        raise ValueError("the amendment commit must be a full 40-character lowercase hash")


def _check_digest(value, name):
    if value is not None and (not isinstance(value, str) or _SHA256.fullmatch(value) is None):
        raise ValueError(f"{name} must be a 64-character lowercase SHA-256 or None")


def _load_input(root, relative):
    """``(object, SHA-256)`` of a committed JSON input, or drift naming the file."""
    relative = Path(relative).as_posix()
    try:
        raw = (root / relative).read_bytes()
    except OSError as exc:
        raise _drift("an input the protocol pins cannot be read", [relative]) from exc
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise _drift("an input the protocol pins is not JSON", [relative]) from exc
    if not isinstance(payload, dict):
        raise _drift("an input the protocol pins is not a JSON object", [relative])
    return payload, _sha256(raw)


# ---------------------------------------------------------------------------
# The inputs the protocol checks against their pins.
# ---------------------------------------------------------------------------

def _panel(root):
    """The three panel singles and their inner-lap counts to two decimals (Phase 59 panels)."""
    payload, digest = _load_input(root, PANELS_REL)
    relative = PANELS_REL.as_posix()
    try:
        singles = payload["singles"]
        ids = [row["id"] for row in singles]
        laps = {int(row["id"]): round(float(row["N_in"]), 2) for row in singles}
    except (KeyError, TypeError, ValueError) as exc:
        raise _drift("the Phase 59 panels file has no readable singles", [relative]) from exc
    if ids != list(PANEL_SYSTEMS) or laps != PANEL_INNER_LAPS:
        raise _drift(
            "the Phase 59 panel singles are not 1632, 851 and 4658 with inner laps "
            "10.47, 18.61 and 39.35",
            [relative],
        )
    return {
        "systems": list(PANEL_SYSTEMS),
        "inner_laps": {str(system): laps[system] for system in PANEL_SYSTEMS},
        "source": {"path": relative, "sha256": digest},
    }


def _probes(root):
    """The FEAS-09 picks (Phase 59 survey): standard base 2279 for Stage 4b, 3418 for Stage 6."""
    payload, digest = _load_input(root, PICKS_REL)
    relative = PICKS_REL.as_posix()
    by_stage = {stage: system for system, stage in PROBE_STAGES.items()}
    expected = {
        "stage4b": f"standard/base/{by_stage[4]}",
        "stage6": f"standard/base/{by_stage[6]}",
    }
    try:
        picks = {name: payload[name]["record"] for name in expected}
    except (KeyError, TypeError) as exc:
        raise _drift("the FEAS-09 picks file has no readable picks", [relative]) from exc
    if picks != expected:
        raise _drift(
            "the FEAS-09 picks are not standard/base/2279 for Stage 4b and "
            "standard/base/3418 for Stage 6",
            [relative],
        )
    return {
        "picks": picks,
        "stages": {str(system): stage for system, stage in PROBE_STAGES.items()},
        "formula": FORMULA_NOT_APPLICABLE,
        "source": {"path": relative, "sha256": digest},
    }


def _formula(root, card):
    """The two-Kepler formula error of each counted panel system (Phase 59 baselines)."""
    payload, digest = _load_input(root, TWO_KEPLER_REL)
    relative = TWO_KEPLER_REL.as_posix()
    errors = {}
    try:
        for row in payload["rows"]["singles"]:
            if row["id"] in PANEL_SYSTEMS:
                if row["applicable"] is not True:
                    raise ValueError("not applicable")
                error = float(row["E"])
                if not (math.isfinite(error) and error > 0.0):
                    raise ValueError("not a finite positive error")
                errors[str(row["id"])] = error
    except (KeyError, TypeError, ValueError) as exc:
        raise _drift("the two-Kepler baselines have no usable formula row", [relative]) from exc
    if sorted(errors) != sorted(str(system) for system in PANEL_SYSTEMS):
        raise _drift("the two-Kepler baselines miss a counted panel system", [relative])
    return {
        "source": {"path": relative, "sha256": digest},
        "E_formula": errors,
        "counting_rule": dict(card.section("counting_rule")),
        "comparison": "a counted arm counts only if its position error is strictly less than "
        "E_formula and it is Tier 1 or better; a probe system has no formula",
    }


def _stage0_metadata(root):
    """S_H and eps_H the generation-7 run saved (GAP-60-12), checked against the register."""
    payload, digest = _load_input(root, STAGE0_METADATA_REL)
    relative = STAGE0_METADATA_REL.as_posix()
    if payload.get("s_h") != EXPECTED_S_H or payload.get("eps_h") != EXPECTED_EPS_H:
        raise _drift(
            f"the Stage-0 training metadata does not hold S_H {EXPECTED_S_H} and "
            f"eps_H {EXPECTED_EPS_H}",
            [relative],
        )
    return {
        "value": EXPECTED_S_H,
        "eps_h": EXPECTED_EPS_H,
        "source_path": relative,
        "source_sha256": digest,
        "source": "GAP-60-12",
        "rule": "The two probe physics arms use the persisted generation-7 S_H and eps_H as they "
        "stand and record them with this source file. Nothing is recomputed.",
    }


def _scorer(root):
    """The scorer digest: the committed successor record, which the current file must equal (D-09)."""
    record, record_digest = _load_input(root, SCORER_SUCCESSOR_REL)
    record_rel = SCORER_SUCCESSOR_REL.as_posix()
    successor = record.get("successor_sha256")
    predecessor = record.get("predecessor_sha256")
    if (
        record.get("path") != SCORER_REL
        or not isinstance(successor, str)
        or _SHA256.fullmatch(successor) is None
        or not isinstance(predecessor, str)
        or _SHA256.fullmatch(predecessor) is None
    ):
        raise _drift(
            f"the scorer successor record must name {SCORER_REL} with two SHA-256 digests",
            [record_rel],
        )
    if _file_sha256(root / SCORER_REL) != successor:
        raise _drift("the scorer is not the committed successor", [SCORER_REL])
    return successor, {
        "path": SCORER_REL,
        "predecessor_sha256": predecessor,
        "successor_sha256": successor,
        "record_path": record_rel,
        "record_sha256": record_digest,
    }


def _governed_reference(root):
    """The governed Stage-0 R_ref artifact, read with the trainer's own loader (D-08, GAP-60-10)."""
    path = root / R_REF_GOVERNED_REL
    try:
        value = load_frozen_r_ref_artifact(path)
    except ValueError as exc:
        raise _drift("the governed R_ref artifact does not load", [R_REF_GOVERNED_REL]) from exc
    return {"value": value, "path": R_REF_GOVERNED_REL, "sha256": _file_sha256(path)}


def _pinned_digests(root):
    missing = [relative for relative in PINNED_MODULES if not (root / relative).is_file()]
    if missing:
        raise _drift("a pinned module or artifact is missing", missing)
    return evidence_io.module_hashes(PINNED_MODULES, repo_root=root)


# ---------------------------------------------------------------------------
# The sections of the protocol. Each cites its decision or gap.
# ---------------------------------------------------------------------------

def _arm_row(spec):
    return {
        "rung": spec.rung,
        "path": spec.path,
        "loss_arm": spec.loss_arm,
        "system_id": spec.system_id,
        "variant": spec.variant,
        "train_key": evidence_io.record_key_str(spec.train_key),
        "score_key": evidence_io.record_key_str(spec.score_key),
        "beside_key": evidence_io.record_key_str(spec.beside_key),
        "lr_stage": spec.lr_stage,
        "clip_stage": spec.clip_stage,
        "omega_provenance": spec.omega_provenance,
        "grid_omega": spec.grid_omega,
        "counted": spec.counted,
        "run_kind": spec.run_kind,
    }


def _schedule_section():
    opt = OptConfig()
    stages = sorted({spec.lr_stage for spec in catalog().values()})
    return {
        "source": "D-01, D-02, D-03, D-04, D-05",
        "lr_base": opt.adam_lr_base,
        "lr_decay": opt.adam_lr_decay,
        "lr_rule": "LR_k = lr_base x lr_decay^k with cosine annealing to zero over the arm's "
        "step budget B. Stage 0 uses k = 0, Stage 4b uses k = 4 and Stage 6 uses k = 6 (D-01).",
        "lr_by_stage": {str(stage): opt.lr_for_stage(stage) for stage in stages},
        "betas": list(opt.adam_betas),
        "eps": opt.adam_eps,
        "data_only_stage": 0,
        "data_only_rule": "Every data-only arm uses the Stage-0 cosine (k = 0), not the Phase 38 "
        "constant rate (D-04).",
        "probe_stages": {str(system): stage for system, stage in PROBE_STAGES.items()},
        "probe_rule": "Probe Rung-2b arms use that stage's LR_k, not Stage 0's rate (D-05).",
        "budget_rule": "B is the frozen 3-hour cap divided by the arm's own timing-run seconds per "
        "step. The timing run is not part of the cosine (D-02).",
        "warmup": "min(2000, floor(0.1 B))",
        "extension": "second cosine of length B from LR_k, Adam state kept, no re-ramp",
    }


def _clip_section(clip_data_only_arms):
    stages = sorted({spec.clip_stage for spec in catalog().values()})
    return {
        "source": "GAP-60-03",
        "table": {str(stage): DEFAULT_C_STAGE_TABLE[stage] for stage in stages},
        "median_floor": DEFAULT_MEDIAN_FLOOR,
        "adam_only": True,
        "clip_data_only_arms": clip_data_only_arms,
        "rule": "Every Adam step is clipped by the trainer's median-based GradClipper at the arm's "
        "stage (0 for data-only and Stage-0 arms, 4 and 6 for probe Rung 2b), in the timing run "
        "and in the arm, and never in the polish. The record carries the stage, the multiplier "
        "and the arm's count of clipped steps, and the clipper state is checkpointed for resume. "
        "clip_data_only_arms is true unless the owner vetoes clipping for the data-only arms "
        "before this protocol is committed; physics arms always clip. A non-finite clip outcome "
        "is the divergence case of GAP-60-06.",
    }


def _timing_section(card):
    return {
        "source": "GAP-60-04",
        "data_only_steps": TIMING_STEPS["data_only"],
        "physics_steps": TIMING_STEPS["physics"],
        "minimum_steps": int(card.section("budget_rule")["timing_run_min_steps"]),
        "all_steps_timed": True,
        "rule": "Every arm has its own timing run of the exact arm configuration (record, loss arm, "
        "first_omega_0, stage, batch, chunking and clipper), immediately before the arm: 500 "
        "steps for a data-only arm and 50 for an arm with a physics term, every step timed, "
        "warm-up included. The arm then starts from its own seed-42 initialization and RNG "
        "streams, and its cosine covers only the budgeted steps. No other heavy job runs "
        "during a timing run or an arm. The timing weights are discarded and not committed; "
        "the timing wall time and step count go in the arm record.",
    }


def _cadence_section(card):
    return {
        "source": "D-06 and the frozen budget rule",
        "max_fraction": card.section("budget_rule")["scoring_cadence_max_fraction"],
        "rule": "The scorer is read at step 0, every floor(0.05 B) steps and at B, and on to 2B "
        "after the one extension, so that no gap is larger than 5% of the step budget. A "
        "physics arm logs the frozen monitor's per-bin causal weights and front at these "
        "readings and never halts on them (D-06).",
    }


def _polish_section(card):
    section = dict(card.section("lbfgs_polish"))
    section.update(
        {
            "source": "GAP-60-05",
            "outer_call": "One outer call is one LBFGS step(closure) with the frozen max_iter, "
            "history size and strong Wolfe line search.",
            "improvement": "After each outer call its full-batch objective is compared with the "
            "best so far: a strictly lower value resets the count of calls without improvement, "
            "otherwise the count goes up. The starting value is the objective at the Adam "
            "result. Then polish_should_stop is called.",
            "polish_state": "The polish state is the iterate after the last outer call.",
            "adam_wall": "Adam's running time is the whole Adam phase (steps plus scoring "
            "readings) summed across segments, without interruptions. The polish cap is 25% of it.",
            "non_finite": "If an outer call returns a non-finite objective or leaves non-finite "
            "parameters, the polish stops and the polish state is the parameters from before "
            "that call.",
            "e_never_steers": "The scored position error E may be logged at each outer call for "
            "the trace, but it never steers the polish.",
            "physics_freeze": "Physics arms freeze the collocation rows, causal weights and loss "
            "weights at the handoff (57-RULING.md:112-124).",
        }
    )
    return section


def _divergence_section():
    return {
        "source": "GAP-60-06",
        "rule": "The loss and the clip outcome are checked before optimizer.step(). On a "
        "non-finite value that step is skipped and Adam ends at the last finite state, which is "
        "scored as the Adam state. The polish runs if its weights are finite, and better_state "
        "chooses. diverged_at_step is recorded and the budget outcome is diverged. The arm's "
        "result enters G2 at its tier like any other.",
        "budget_outcome_called": False,
        "restart": False,
    }


def _cross_check_section():
    return {
        "source": "GAP-60-07",
        "scope": "both scored states of every real arm",
        "runtime": {"dtype": CROSS_CHECK_RUNTIME[0], "device": CROSS_CHECK_RUNTIME[1]},
        "disagreement": "Any difference in tier or in the counts boolean between the official "
        "MPS score and the CPU float64 re-score raises a dedicated owner-routed stop.",
        "take_the_better": False,
        "cadence_readings": "MPS only",
    }


def _weights_section():
    return {
        "source": "D-10, GAP-60-08",
        "files": ["adam.weights", "polish.weights"],
        "directory": "evidence/arms/<arm-id>/",
        "format": "torch.save of a CPU state dict in the runtime dtype (float32), one file per "
        "scored state",
        "git": "Both scored states of every real arm are committed in plain git, not Git LFS.",
        "record_digests": "Each record carries the file's SHA-256 and a canonical per-tensor "
        "digest (name, dtype, shape and bytes, in sorted-name order).",
        "load": "torch.load(..., weights_only=True)",
        "kept_out_of_git": "Resume checkpoints and timing-run weights stay under the ignored "
        "runs/ tree.",
    }


def _first_result_section():
    return {
        "source": "SPEC Requirement 4 and its constraints",
        "rule": "The first completed run is the result. A second seed, a second fresh training "
        "run or a silent restart is not the result.",
        "re_derive": "Re-deriving a result re-scores the committed weights and does not retrain.",
        "fresh_runs": "Fresh same-seed runs are statistically similar, not bit-identical.",
        "seeds": "One seed per arm. Extra seeds are not added after a result.",
    }


def _sweep_pairs():
    """The pinned sweep and confirmation systems for each way G2 can fire (SPEC Requirement 6)."""
    failing_sets = [list(PANEL_SYSTEMS)]
    failing_sets += [list(pair) for pair in itertools.combinations(PANEL_SYSTEMS, 2)]
    pairs = []
    for failing in failing_sets:
        sweep, confirmation, uncovered = sweep_plan(failing)
        pairs.append(
            {
                "failing": failing,
                "sweep": sweep,
                "confirmation": confirmation,
                "uncovered": uncovered,
            }
        )
    return pairs


def _g2_section(card, failed_confirmation_pre_answer):
    gate = card.section("gate_g2")
    return {
        "grid": list(gate["grid"]),
        "locked_value": gate["locked_value"],
        "rescue_tier": gate["rescue_tier"],
        "trigger_below_tier": gate["trigger_below_tier"],
        "trigger_min_systems": gate["trigger_min_systems"],
        "inner_laps": {str(system): PANEL_INNER_LAPS[system] for system in PANEL_SYSTEMS},
        "sweep_pairs": _sweep_pairs(),
        "sweep_rule": "If G2 fires, all four data-only settings run in grid order, even after a "
        "success. 'Reaches Tier 1' means the arm result, the better of Adam and polish by the "
        "frozen rule, is Tier 1 or higher. No setting between the grid points is run.",
        "confirmation_rule": "The confirmation is the highest first_omega_0 that reached Tier 1: "
        "one run, same seed, runtime, gold grid, budget rule and polish. Zero settings at Tier 1 "
        "or higher means no confirmation and no rescue. The other settings that reached Tier 1 "
        "are listed with the label below. The four-setting curve (tier, E, eps_H, valid "
        "horizon) is part of the checkpoint 4 record.",
        "other_settings_label": NOT_CONFIRMED_LABEL,
        "rescue_rule": "A confirmed rescue raises the frozen OwnerRouted (owner checkpoint 4) and "
        "does not continue by itself. While checkpoint 4 is unanswered, Rung 2 and the probes "
        "are neither run nor skipped.",
        "failed_confirmation_rule": "GAP-60-09: if the confirmation run ends below Tier 1, the "
        "harness writes the sweep curve and the confirmation record and raises an owner-routed "
        "stop. It then runs or skips nothing further, and decision_verdict is not called until "
        "the owner answers. The owner may pre-answer no_rescue or rescue before this protocol "
        "is committed; null means the owner is asked at the time. GAP-60-09 resolves the "
        "procedure only.",
        "failed_confirmation_pre_answer": failed_confirmation_pre_answer,
    }


_DECISIONS = {
    "D-06": "A physics arm never halts on invariant B or any other causal-front rule. At the "
    "budget-rule readings it logs the frozen monitor's per-bin causal weights and front. It does "
    "not run a live 256-identity monitor every step. Phase 61 builds the observe-only guard.",
    "D-07": "If the owner continues at checkpoint 4, R_ref is re-measured and GATE-04 is re-run at "
    "the approved first_omega_0 before any physics arm. Neither step trains. GATE-04 is the "
    "complete-pass rule of 57-RULING.md (GAP-56-01). A fail stops for the owner.",
    "D-08": "Probe physics arms reuse the Stage-0 R_ref in force and do not re-measure it. The run "
    "record says the value is the Stage-0 reference applied unchanged.",
    "D-09": "The Phase 59 verifier accepts exactly one successor SHA-256 for "
    "pinn/verification/feasibility_scorer.py, named in the committed scorer-successor.json. "
    "Every other producer hash is still checked against the Phase 59 result files.",
    "D-10": "Both scored states of every real arm are committed in plain git, not Git LFS. Resume "
    "checkpoints and timing-run weights stay out of git. Re-deriving a result re-scores the "
    "committed weights.",
    "D-11": "A continue-path arm is legal only when a committed ruling file quotes the owner's "
    "message and names the approved first_omega_0. Every continue-path arm record cites it. A "
    "physics arm refuses any other value.",
}

_OWNER_STOPS = (
    {
        "id": "missing_formula_on_counted_system",
        "when": "A counted panel system has no two-Kepler formula, so counts() raises the frozen "
        "OwnerRouted.",
        "source": "SPEC Requirement 7 and the frozen counting_rule",
    },
    {
        "id": "rescue",
        "when": "A confirmed G2 rescue raises the frozen OwnerRouted (owner checkpoint 4).",
        "source": "SPEC Requirement 6",
    },
    {
        "id": "undeterminable_improvement_rate",
        "when": "An extended arm's improvement rate cannot be computed, so budget_outcome raises "
        "the frozen OwnerRouted.",
        "source": "SPEC Requirement 8",
    },
    {
        "id": "cross_check_disagreement",
        "when": "The CPU float64 cross-check of a scored state differs from the official score in "
        "tier or in the counts boolean.",
        "source": "GAP-60-07 and SPEC Requirement 3",
    },
    {
        "id": "failed_confirmation_without_pre_answer",
        "when": "The G2 confirmation ends below Tier 1 and this protocol holds no pre-answer.",
        "source": "GAP-60-09",
    },
    {
        "id": "arm_cannot_resume_or_non_governed_exit",
        "when": "An arm cannot be restored from its checkpoint, or ends by an exit that is not a "
        "governed stop (129, 130 or 143).",
        "source": "SPEC Requirement 8",
    },
    {
        "id": "blocked_record",
        "when": "An assigned train, score or beside record is missing, empty, unreadable or "
        "refused, or has an unexpected window count. No arm runs and nothing is substituted. A "
        "blocked Rung-1 record makes G2 impossible.",
        "source": "SPEC Requirement 8",
    },
    {
        "id": "gate04_block_on_continue",
        "when": "The GATE-04 re-measure at the approved first_omega_0 blocks.",
        "source": "D-07",
    },
    {
        "id": "protocol_drift_after_real_record",
        "when": "A pinned module or artifact differs from this protocol after a real record "
        "exists. An amendment after a result is an owner matter.",
        "source": "SCOPE-42 and SPEC Requirement 4",
    },
)

_READOUT_NOTES = (
    "D-04: every data-only arm uses the Stage-0 cosine (k = 0), so the 75%-100% window of the "
    "frozen still-improving test is the low-rate tail of that cosine.",
    "D-05: probe Rung-2b starts from scratch while the 0.7 factor assumes weights carried forward "
    "from the previous stage.",
    "D-08 with GAP-60-10: Stage-0 reference in force, applied unchanged (the governed artifact at "
    "the locked setting, the re-measured one after a continue).",
    "One seed per arm is a stated limit for the verdict, not a reason to add seeds.",
)


def build_protocol(
    *,
    repo_root,
    amendment_commit,
    clip_data_only_arms=True,
    failed_confirmation_pre_answer=None,
    preflight_sha256=None,
):
    """The run protocol (``phase60-run-protocol/v1``) as plain JSON types.

    Every pin is read from ``repo_root`` and checked: the Phase 59 panel singles and
    inner laps, the FEAS-09 picks, the GAP-60-12 values of S_H and eps_H, the scorer
    against the committed successor record, and the frozen scorecard bytes. A file that
    does not match its pin raises ``ProtocolDrift`` naming it. ``clip_data_only_arms``
    and ``failed_confirmation_pre_answer`` are the two answers the owner may give before
    the protocol is committed (GAP-60-03 and GAP-60-09); any other value is a
    ``ValueError``.
    """
    root = Path(repo_root).resolve()
    _check_commit(amendment_commit)
    if not isinstance(clip_data_only_arms, bool):
        raise ValueError("clip_data_only_arms must be True or False")
    if not isinstance(failed_confirmation_pre_answer, (str, type(None))) or (
        failed_confirmation_pre_answer not in PRE_ANSWERS
    ):
        raise ValueError("failed_confirmation_pre_answer must be None, 'no_rescue' or 'rescue'")
    _check_digest(preflight_sha256, "preflight_sha256")
    card = load_scorecard()
    if _file_sha256(root / SCORECARD_REL) != SCORECARD_SHA256:
        raise _drift("the scorecard is not the frozen file", [SCORECARD_REL])
    scorer_sha256, successor = _scorer(root)
    panel = _panel(root)
    probes = _probes(root)
    formula = _formula(root, card)
    s_h = _stage0_metadata(root)
    reference = _governed_reference(root)
    modules = _pinned_digests(root)
    protocol = {
        "schema": PROTOCOL_SCHEMA,
        "plain_language": "Before the first real experiment the project writes down exactly how "
        "every experiment will run and fingerprints the code that will run it. Each experiment "
        "then refuses to start if anything changed, if its data file is missing, or if the "
        "earlier results say it should not run.",
        "amendment_commit": amendment_commit,
        "preflight_sha256": preflight_sha256,
        "seed": SEED,
        "runtime": {"dtype": REAL_RUNTIME[0], "device": REAL_RUNTIME[1]},
        "runtime_rule": "Seed 42 and MPS float32 for Adam and the polish on every real arm: "
        "Rung 1, Rung 2a, Rung 2b, the four sweep arms, the confirmation, the uncovered-system "
        "Rung 1 and both probe arms. The production runtime resolver is not consulted. Arms run "
        "one at a time on this Mac.",
        "cross_check_runtime": {"dtype": CROSS_CHECK_RUNTIME[0], "device": CROSS_CHECK_RUNTIME[1]},
        "scorecard_sha256": SCORECARD_SHA256,
        "scorer_sha256": scorer_sha256,
        "scorer_successor": successor,
        "module_sha256": modules,
        "schedule": _schedule_section(),
        "budget": dict(card.section("budget_rule")),
        "clip": _clip_section(clip_data_only_arms),
        "timing": _timing_section(card),
        "cadence": _cadence_section(card),
        "polish": _polish_section(card),
        "divergence": _divergence_section(),
        "cross_check": _cross_check_section(),
        "weights": _weights_section(),
        "first_result": _first_result_section(),
        "panel": panel,
        "g2": _g2_section(card, failed_confirmation_pre_answer),
        "skip_reasons": list(SKIP_REASONS),
        "probes": probes,
        "formula": formula,
        "decisions": dict(_DECISIONS),
        "r_ref_governed": reference,
        "r_ref_rule": {
            "source": "D-08 with GAP-60-10",
            "note": _REFERENCE_NOTE,
            "rule": "A physics arm normalizes its causal term by the Stage-0 reference in force: "
            "the governed r_ref_stage0.json when the ladder runs at the locked setting, and the "
            "reference re-measured at the approved setting (evidence/continue/"
            "r-ref-approved.json) after an owner continue. Probe arms reuse it unchanged and "
            "never re-measure it. The scorer's context column always uses the governed "
            "artifact. The re-measure writes to a Phase 60 evidence path and never overwrites "
            "r_ref_stage0.json.",
        },
        "approved_omega_rule": {
            "source": "GAP-60-11 and D-11",
            "ruling_file": RULING4_REL.as_posix(),
            "rule": "A continue-path arm may run at any finite positive first_omega_0 that the "
            "committed checkpoint 4 ruling names, on or off the sweep grid. D-07 runs at that "
            "value. Every continue-path record cites the ruling file's SHA-256 and states "
            "on_grid and equals_confirmed. A physics arm refuses any other value.",
        },
        "s_h": s_h,
        "normalizer_stats_sha256": EXPECTED_STATS_SHA256,
        "normalizer_rule": "GAP-60-13: every arm uses the IC13 statistics recovered from the "
        "retained generation-7 checkpoint, including the standard-variant probes. Every record "
        "carries the statistics digest, and a mismatch fails closed. The fallback normalizer is "
        "never used silently.",
        "catalog": {arm_id: _arm_row(spec) for arm_id, spec in catalog().items()},
        "sequences": {name: list(arm_ids) for name, arm_ids in SEQUENCES.items()},
        "owner_stops": [dict(stop) for stop in _OWNER_STOPS],
        "readout_notes": list(_READOUT_NOTES),
    }
    return _json_form(protocol)


# ---------------------------------------------------------------------------
# Writing and loading.
# ---------------------------------------------------------------------------

def write_protocol(protocol, *, evidence_root=None, repo_root=None):
    """Write the protocol as canonical JSON and return the SHA-256 of the file.

    Refused (``HarnessHalt``) once any real ``record.json`` or ``owner-stop.json`` exists
    under ``evidence/arms``: an amendment after a result is the owner's matter, not an
    edit. Before any result the file may be written again.
    """
    if not isinstance(protocol, dict) or protocol.get("schema") != PROTOCOL_SCHEMA:
        raise ValueError(f"a protocol must be a dict with the schema {PROTOCOL_SCHEMA}")
    _root, evidence = _roots(repo_root, evidence_root)
    arms = evidence / "arms"
    if arms.is_dir():
        results = sorted(
            path.relative_to(evidence).as_posix()
            for name in ("record.json", "owner-stop.json")
            for path in arms.glob(f"*/{name}")
        )
        if results:
            raise HarnessHalt(
                "a result already exists (" + ", ".join(results) + "); an amendment after a "
                "result is an owner matter and the protocol is not rewritten"
            )
    return evidence_io.write_json(evidence / PROTOCOL_REL.name, protocol)


def _validate(payload, shown):
    """The fields admission reads must be there. Returns the recorded source pins.

    The source pins are the repo-relative files whose digests the protocol records
    (Phase 59 panels, picks and formula, the Stage-0 metadata and the scorer successor
    record). Anything missing or mistyped makes the protocol unusable.
    """
    problems = []
    for name in ("amendment_commit", "scorecard_sha256", "scorer_sha256"):
        if not isinstance(payload.get(name), str):
            problems.append(name)
    if "preflight_sha256" not in payload or not isinstance(
        payload["preflight_sha256"], (str, type(None))
    ):
        problems.append("preflight_sha256")
    clip = payload.get("clip")
    if not isinstance(clip, dict) or not isinstance(clip.get("clip_data_only_arms"), bool):
        problems.append("clip.clip_data_only_arms")
    g2 = payload.get("g2")
    if (
        not isinstance(g2, dict)
        or "failed_confirmation_pre_answer" not in g2
        or not isinstance(g2["failed_confirmation_pre_answer"], (str, type(None)))
        or g2["failed_confirmation_pre_answer"] not in PRE_ANSWERS
    ):
        problems.append("g2.failed_confirmation_pre_answer")
    reference = payload.get("r_ref_governed")
    if not isinstance(reference, dict) or not all(
        key in reference for key in ("value", "path", "sha256")
    ):
        problems.append("r_ref_governed")
    sources = {}
    try:
        for section, path_key, digest_key in (
            ("panel", ("source", "path"), ("source", "sha256")),
            ("probes", ("source", "path"), ("source", "sha256")),
            ("formula", ("source", "path"), ("source", "sha256")),
            ("s_h", ("source_path",), ("source_sha256",)),
            ("scorer_successor", ("record_path",), ("record_sha256",)),
        ):
            path, digest = payload[section], payload[section]
            for key in path_key:
                path = path[key]
            for key in digest_key:
                digest = digest[key]
            if not isinstance(path, str) or not isinstance(digest, str):
                raise TypeError(section)
            sources[path] = digest
        for name in ("value", "eps_h"):
            if name not in payload["s_h"]:
                raise KeyError(name)
    except (KeyError, TypeError):
        problems.append("the recorded source digests")
    if problems:
        raise _drift("the run protocol lacks required fields (" + ", ".join(problems) + ")", [shown])
    return sources


def load_protocol(*, repo_root=None, evidence_root=None, require_committed=True):
    """The run protocol, if it is the one that was pre-registered.

    The file must have the protocol schema and, when ``require_committed`` is true, be
    tracked and clean in git. It must pin exactly ``PINNED_MODULES``, and the current
    SHA-256 of every pinned file, and of every input file whose digest it records, must
    equal the recorded one. Otherwise ``ProtocolDrift`` names the files that differ (or
    the protocol itself when it is absent, uncommitted or malformed).
    """
    root, evidence = _roots(repo_root, evidence_root)
    path = evidence / PROTOCOL_REL.name
    relative = _relative(root, path)
    shown = relative or path.name
    if path.is_symlink() or not path.is_file():
        raise _drift("there is no run protocol", [shown])
    if require_committed and (relative is None or not tracked_and_clean(root, relative)):
        raise _drift("the run protocol is not tracked and clean in git", [shown])
    raw = path.read_bytes()
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise _drift("the run protocol is not JSON", [shown]) from exc
    if not isinstance(payload, dict) or payload.get("schema") != PROTOCOL_SCHEMA:
        raise _drift(f"the run protocol does not carry the schema {PROTOCOL_SCHEMA}", [shown])
    pins = payload.get("module_sha256")
    if not isinstance(pins, dict):
        raise _drift("the run protocol pins no modules", [shown])
    sources = _validate(payload, shown)
    differing = set(pins).symmetric_difference(PINNED_MODULES)
    differing.update(
        name
        for name in PINNED_MODULES
        if name in pins and _file_sha256(root / name) != pins[name]
    )
    differing.update(name for name, digest in sources.items() if _file_sha256(root / name) != digest)
    if differing:
        raise _drift("a pinned file differs from the run protocol", sorted(differing))
    return LoadedProtocol(payload=payload, sha256=_sha256(raw), path=shown)


# ---------------------------------------------------------------------------
# The record preflight (SPEC Requirement 8).
# ---------------------------------------------------------------------------

def _assigned_keys():
    """Every distinct train, score and beside key of the closed catalog, ``label -> RecordKey``."""
    keys = {}
    for spec in catalog().values():
        for key in (spec.train_key, spec.score_key, spec.beside_key):
            keys.setdefault(evidence_io.record_key_str(key), key)
    return keys


def _expected_within_t(label):
    variant, fidelity, _identifier = label.split("/")
    return EXPECTED_WITHIN_T[f"{variant}/{fidelity}"]


def _key_blocked(entry):
    """A key is usable only when it was read (``ok``) and its window holds the verified count."""
    return entry.get("status") != "ok" or entry.get("count_ok") is not True


def _open_attestation(context):
    """The context's open-attestation summary, if it shows no test-split file was touched."""
    attestation = getattr(context, "attestation", None)
    if attestation is None:
        raise HarnessHalt(
            "the context has no open attestation, so zero test-split opens cannot be shown"
        )
    summary = dict(attestation.summary())
    for counter in _OPEN_COUNTERS:
        if summary.get(counter) != 0:
            raise HarnessHalt(
                f"the open attestation reports {counter} = {summary.get(counter)!r}; it must be 0"
            )
    return summary


def write_preflight(*, repo_root=None, evidence_root=None, context=None, key_map=None):
    """Check every assigned record once, before the first arm, and write ``preflight/records.json``.

    The records are the distinct train, score and beside keys of the closed catalog (the
    ten records of 60-RESEARCH Finding G). Each is read through the allowlist by
    ``preflight_records`` and reported as ``ok``, ``missing``, ``empty``, ``unreadable``
    or ``refused``, with the number of samples within T beside the verified count. A
    record that is not ``ok`` with the verified count blocks the arms that use it and no
    others, and nothing is read in its place. The open attestation must show zero opens
    of a test-split file, else ``HarnessHalt`` and nothing is written. The file is created
    once (``FirstResultExists`` on a second write), holds no data root, and the
    function returns ``(payload, SHA-256 of the file)``.

    ``context`` is opened with ``open_real_context`` when it is not injected.
    ``key_map`` maps a catalog key to the key actually read; it is for tests that run on a
    fixture corpus, and the file is still keyed by the catalog key.
    """
    root, evidence = _roots(repo_root, evidence_root)
    card = load_scorecard()
    if context is None:
        context = open_real_context(repo_root=root)
    mapping = {} if key_map is None else dict(key_map)
    assigned = _assigned_keys()
    read_keys = {label: mapping.get(key, key) for label, key in assigned.items()}
    report = preflight_records(list(read_keys.values()), context, scorecard=card)
    records = {}
    for label, read_key in read_keys.items():
        entry = dict(report[evidence_io.record_key_str(read_key)])
        expected = _expected_within_t(label)
        entry["expected_within_t"] = expected
        entry["count_ok"] = entry.get("status") == "ok" and entry.get("n_within_t") == expected
        records[label] = entry
    arms = {}
    for arm_id, spec in catalog().items():
        roles = {
            "train_key": evidence_io.record_key_str(spec.train_key),
            "score_key": evidence_io.record_key_str(spec.score_key),
            "beside_key": evidence_io.record_key_str(spec.beside_key),
        }
        blocked_by = []
        for label in roles.values():
            if _key_blocked(records[label]) and label not in blocked_by:
                blocked_by.append(label)
        arms[arm_id] = {"status": "blocked" if blocked_by else "ok", **roles, "blocked_by": blocked_by}
    payload = _json_form(
        {
            "schema": PREFLIGHT_SCHEMA,
            "plain_language": "Every record an arm trains on, is scored on or reports beside is "
            "checked once, before the first arm. A record is ok, missing, empty, unreadable or "
            "refused, and its sample count within T is compared with the count that was "
            "verified. A record that is not ok blocks the arms that use it and no others, and "
            "nothing is read in its place.",
            "scorecard_sha256": card.sha256,
            "t_max": card.section("scoring_grid")["t_max"],
            "data_root_source": context.data_root_source,
            "records": records,
            "arms": arms,
            "blocked_arms": sorted(arm for arm, row in arms.items() if row["status"] == "blocked"),
            "attestation": _open_attestation(context),
        }
    )
    path = evidence / PREFLIGHT_REL.relative_to(EVIDENCE_REL)
    digest = write_record_exclusive(
        path, payload, data_root=getattr(getattr(context, "reader", None), "data_root", None)
    )
    return payload, digest


# ---------------------------------------------------------------------------
# Admission of a real arm.
# ---------------------------------------------------------------------------

# What turns into a refusal: an arm may not start, and the reason is the message. A
# frozen OwnerRouted is never in this list; admission never calls the rules that raise it.
_REFUSABLE = (
    ProtocolDrift, UnknownArm, OverrideRefused, G2Halt, G2Pending, RulingError,
    KeyError, TypeError, ValueError, OSError,
)


def _committed_json(root, path, what):
    """``(object, SHA-256, repo-relative path)`` of a JSON file that is tracked and clean in git."""
    relative = _relative(root, path)
    if relative is None:
        raise AdmissionRefused(f"{what} lies outside the repository")
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise AdmissionRefused(f"{what} is not recorded ({relative})")
    if not tracked_and_clean(root, relative):
        raise AdmissionRefused(f"{what} {relative} is not tracked and clean in git")
    raw = path.read_bytes()
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise AdmissionRefused(f"{what} {relative} is not JSON") from exc
    if not isinstance(payload, dict):
        raise AdmissionRefused(f"{what} {relative} is not a JSON object")
    return payload, _sha256(raw), relative


def _check_preflight(spec, protocol, root, evidence):
    """The arm's three records are cleared in the committed preflight the protocol pins."""
    path = evidence / PREFLIGHT_REL.relative_to(EVIDENCE_REL)
    payload, digest, relative = _committed_json(root, path, "the preflight")
    pinned = protocol.payload["preflight_sha256"]
    if pinned is None:
        raise AdmissionRefused("the run protocol pins no preflight")
    if digest != pinned:
        raise AdmissionRefused(
            f"the committed preflight {relative} is not the one the run protocol pins"
        )
    if payload.get("schema") != PREFLIGHT_SCHEMA:
        raise AdmissionRefused(f"{relative} does not carry the schema {PREFLIGHT_SCHEMA}")
    attestation = payload.get("attestation")
    for counter in _OPEN_COUNTERS:
        found = attestation.get(counter) if isinstance(attestation, dict) else None
        if found != 0:
            raise AdmissionRefused(f"the preflight reports {counter} = {found!r}; it must be 0")
    records = payload.get("records")
    for role in ("train", "score", "beside"):
        label = evidence_io.record_key_str(getattr(spec, f"{role}_key"))
        entry = records.get(label) if isinstance(records, dict) else None
        if not isinstance(entry, dict) or _key_blocked(entry):
            status = entry.get("status", "unrecorded") if isinstance(entry, dict) else "unrecorded"
            reason = status if status != "ok" else "an unexpected window count"
            raise AdmissionRefused(
                f"the preflight does not clear the {role} record {label} ({reason})"
            )
    return digest


def _check_pins(protocol, root):
    """The amendment is in the history, and the scorer and scorecard are the registered files."""
    payload = protocol.payload
    commit = payload["amendment_commit"]
    if not evidence_io.is_ancestor(commit, "HEAD", root):
        raise AdmissionRefused(f"the amendment commit {commit} is not an ancestor of HEAD")
    if _file_sha256(root / SCORER_REL) != payload["scorer_sha256"]:
        raise AdmissionRefused(
            "the scorer on disk does not match the scorer digest the run protocol records"
        )
    if (
        payload["scorecard_sha256"] != SCORECARD_SHA256
        or _file_sha256(root / SCORECARD_REL) != payload["scorecard_sha256"]
    ):
        raise AdmissionRefused(
            "the scorecard on disk does not match the scorecard digest the run protocol records"
        )


def _check_run_state(spec, root, evidence, resume):
    """No result exists for the arm; a fresh start has no run directory and a resume has one."""
    for name in ("record.json", "owner-stop.json"):
        if os.path.lexists(arm_evidence_dir(spec.arm_id, evidence_root=evidence) / name):
            raise AdmissionRefused(
                f"{spec.arm_id} already has a {name}; the first completed run is the result"
            )
    shown = (RUNS_REL / spec.arm_id).as_posix()
    run_dir = arm_run_dir(spec.arm_id, repo_root=root)
    if resume:
        if not run_dir.is_dir():
            raise AdmissionRefused(f"a resume needs the run directory {shown} and there is none")
    elif os.path.lexists(run_dir):
        raise AdmissionRefused(f"{shown} already exists; a fresh start needs none")


def _g2_json(root, evidence, name):
    return _committed_json(root, evidence / "g2" / name, f"g2/{name}")[0]


def _require_taken(name, root, evidence, card):
    state = branch_state(name, evidence_root=evidence, repo_root=root, scorecard=card)
    if state.status != TAKEN:
        raise AdmissionRefused(f"branch {name} is {state.status}: {state.reason}")
    return state


def _check_branch(spec, root, evidence, card):
    """The branch the committed G2 records have taken must allow this arm.

    Returns ``(branch state or None, checkpoint 4 ruling or None)``.
    """
    if spec.path == "rung1":
        return None, None
    if spec.path == "g2_sweep":
        state = _require_taken("sweep", root, evidence, card)
        sweep = _g2_json(root, evidence, "g2-outcome.json")["sweep_system"]
        if spec.system_id != sweep:
            raise AdmissionRefused(f"{spec.arm_id} is not on the recorded sweep system {sweep}")
        return state, None
    if spec.path == "g2_confirmation":
        state = _require_taken("confirmation", root, evidence, card)
        confirmation = _g2_json(root, evidence, "sweep-curve.json")["confirmation_arm"]
        if spec.arm_id != confirmation:
            raise AdmissionRefused(
                f"{spec.arm_id} is not the recorded confirmation arm {confirmation}"
            )
        return state, None
    state = _require_taken("ladder", root, evidence, card)
    if spec.path == "g2_passed":
        if state.omega_provenance != "locked":
            raise AdmissionRefused(
                "the ladder is taken by an owner continue, so a plain Rung-2 or probe arm does not run"
            )
        return state, None
    if spec.path != "continue":
        raise AdmissionRefused(f"{spec.arm_id} has the unknown path {spec.path}")
    if state.omega_provenance != "owner_approved":
        raise AdmissionRefused(
            "the ladder runs at the locked setting, so a continue-path arm does not run"
        )
    ruling = load_checkpoint4_ruling(repo_root=root)
    if state.first_omega_0 != ruling.approved_first_omega_0:
        raise AdmissionRefused(
            "the ladder's setting is not the first_omega_0 the committed ruling names"
        )
    if spec.rung == "1":
        uncovered = _g2_json(root, evidence, "g2-outcome.json")["uncovered_system"]
        if spec.system_id != uncovered:
            raise AdmissionRefused(f"{spec.arm_id} is not on the recorded uncovered system {uncovered}")
    return state, ruling


def _reference_in_force(protocol, root, evidence, owner_approved):
    """``(Stage-0 reference in force, governed reference for the scorer's context column)``."""
    governed = protocol.payload["r_ref_governed"]
    governed_path = root / governed["path"]
    if _file_sha256(governed_path) != governed["sha256"]:
        raise AdmissionRefused(f"the governed reference {governed['path']} is not the registered file")
    try:
        value = load_frozen_r_ref_artifact(governed_path)
    except ValueError as exc:
        raise AdmissionRefused(f"the governed reference {governed['path']} does not load") from exc
    if value != governed["value"]:
        raise AdmissionRefused(f"the governed reference {governed['path']} no longer holds its value")
    context = {"path": governed["path"], "sha256": governed["sha256"]}
    if not owner_approved:
        return {**context, "value": value, "note": _REFERENCE_NOTE}, context
    path = evidence / REMEASURE_REL.relative_to(EVIDENCE_REL)
    recorded, _digest, relative = _committed_json(root, path, "the re-measure record")
    remeasure = parse_remeasure(recorded, path=relative)
    cited = remeasure.r_ref_artifact
    approved = R_REF_APPROVED_REL.as_posix()
    if remeasure.verdict != "PASS" or cited is None:
        raise AdmissionRefused(f"the re-measure record {relative} is not a PASS")
    if cited["path"] != approved:
        raise AdmissionRefused(f"the re-measure record cites {cited['path']}, not {approved}")
    if not tracked_and_clean(root, approved):
        raise AdmissionRefused(f"{approved} is not tracked and clean in git")
    if _file_sha256(root / approved) != cited["sha256"]:
        raise AdmissionRefused(f"{approved} is not the file the re-measure record cites")
    try:
        approved_value = load_frozen_r_ref_artifact(root / approved)
    except ValueError as exc:
        raise AdmissionRefused(f"{approved} does not load") from exc
    return {"path": approved, "sha256": cited["sha256"], "value": approved_value,
            "note": _REFERENCE_NOTE}, context


def _admit(arm_id, root, evidence, resume):
    protocol = load_protocol(repo_root=root, evidence_root=evidence, require_committed=True)
    spec = arm_spec(arm_id)
    card = load_scorecard()
    preflight_sha256 = _check_preflight(spec, protocol, root, evidence)
    _check_pins(protocol, root)
    _check_run_state(spec, root, evidence, resume)
    state, ruling = _check_branch(spec, root, evidence, card)
    value = resolve_first_omega_0(spec, scorecard=card, ruling=ruling)
    check_override(spec, value, scorecard=card, ruling=ruling)
    if state is not None and state.first_omega_0 is not None and state.first_omega_0 != value:
        raise AdmissionRefused(f"{arm_id} would run at {value}, not at the ladder's {state.first_omega_0}")
    ruling_facts = None
    if ruling is not None:
        confirmed = _g2_json(root, evidence, "sweep-curve.json").get("confirmed_first_omega_0")
        facts = ruling_grid_facts(ruling, scorecard=card, confirmed_first_omega_0=confirmed)
        ruling_facts = {
            "path": ruling.path,
            "sha256": ruling.sha256,
            "answer": ruling.answer,
            "approved_first_omega_0": ruling.approved_first_omega_0,
            "on_grid": facts["on_grid"],
            "equals_confirmed": facts["equals_confirmed"],
        }
    physics = spec.loss_arm != "data_only"
    reference = context_reference = None
    if physics:
        reference, context_reference = _reference_in_force(
            protocol, root, evidence, spec.omega_provenance == "owner_approved"
        )
    s_h = None
    if spec.rung == "probe-2b":
        recorded = protocol.payload["s_h"]
        s_h = {name: recorded[name] for name in ("value", "eps_h", "source_sha256")}
    return {
        "arm_id": spec.arm_id,
        "protocol_sha256": protocol.sha256,
        "preflight_sha256": preflight_sha256,
        "first_omega_0": value,
        "omega_provenance": spec.omega_provenance,
        "ruling": ruling_facts,
        "r_ref_in_force": reference,
        "scorer_context_r_ref": context_reference,
        "s_h": s_h,
        "clip_enabled": True if physics else protocol.payload["clip"]["clip_data_only_arms"],
        "failed_confirmation_pre_answer": protocol.payload["g2"]["failed_confirmation_pre_answer"],
    }


def admit_arm(arm_id, *, repo_root=None, evidence_root=None, resume=False):
    """May this real arm start now? Returns what it must cite, or raises ``AdmissionRefused``.

    In order: the run protocol loads without drift; the arm is in the closed catalog; its
    train, score and beside records are cleared in the committed preflight that the
    protocol pins; the amendment commit is an ancestor of HEAD; the scorer and scorecard on
    disk are the registered ones; no ``record.json`` or ``owner-stop.json`` exists for the
    arm, and a fresh start has no ``runs/phase60/<arm-id>`` while a resume has one; and the
    branch that the committed G2 records have taken allows the arm (Rung 1 always; a sweep
    arm only on the recorded sweep system; the confirmation only as the recorded
    confirmation arm; Rung 2 and the probes only on a ladder taken at the locked setting; a
    continue arm only on a ladder taken at the committed ruling's setting, and the uncovered
    Rung 1 only for the recorded uncovered system).

    The result holds the setting and its provenance, the committed ruling's facts for a
    continue arm (D-11, GAP-60-11), the Stage-0 reference in force for a physics arm
    (D-08, GAP-60-10) and the governed reference the scorer's context column uses, S_H for
    a probe Rung-2b arm (GAP-60-12), the clipping flag, and the protocol's pre-answer to a
    failed confirmation. Nothing is read from the corpus and nothing is written.
    """
    root, evidence = _roots(repo_root, evidence_root)
    try:
        return _admit(arm_id, root, evidence, bool(resume))
    except AdmissionRefused:
        raise
    except _REFUSABLE as exc:
        raise AdmissionRefused(_one_line(exc)) from exc


# ---------------------------------------------------------------------------
# The command line.
# ---------------------------------------------------------------------------

def _git_toplevel(path):
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
        raise ValueError("the evidence root is not inside a git repository")
    return Path(completed.stdout.strip()).resolve()


def _cli_roots(evidence_root):
    if evidence_root is None:
        return _roots(None, None)
    evidence = Path(evidence_root)
    return _git_toplevel(evidence), evidence


def _preflight_digest(evidence):
    """The SHA-256 of the recorded preflight file, which the protocol pins."""
    path = evidence / PREFLIGHT_REL.relative_to(EVIDENCE_REL)
    if not path.is_file():
        raise ValueError("no preflight is recorded; run the preflight first")
    raw = path.read_bytes()
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise ValueError("the recorded preflight is not JSON") from exc
    if not isinstance(payload, dict) or payload.get("schema") != PREFLIGHT_SCHEMA:
        raise ValueError(f"the recorded preflight does not carry the schema {PREFLIGHT_SCHEMA}")
    return _sha256(raw)


def _cli_write(args, root, evidence):
    _check_commit(args.amendment_commit)
    if not evidence_io.is_ancestor(args.amendment_commit, "HEAD", root):
        raise ValueError(f"the amendment commit {args.amendment_commit} is not an ancestor of HEAD")
    preflight = _preflight_digest(evidence)
    protocol = build_protocol(
        repo_root=root,
        amendment_commit=args.amendment_commit,
        clip_data_only_arms=not args.no_clip_data_only_arms,
        failed_confirmation_pre_answer=args.failed_confirmation_pre_answer,
        preflight_sha256=preflight,
    )
    digest = write_protocol(protocol, evidence_root=evidence, repo_root=root)
    shown = _relative(root, evidence / PROTOCOL_REL.name) or PROTOCOL_REL.name
    return f"PROTOCOL-WRITTEN: {shown} sha256 {digest}", EXIT_OK


def _cli_check(root, evidence):
    loaded = load_protocol(repo_root=root, evidence_root=evidence, require_committed=True)
    return f"PROTOCOL-OK: {loaded.path} sha256 {loaded.sha256}", EXIT_OK


def _cli_preflight(root, evidence):
    payload, digest = write_preflight(repo_root=root, evidence_root=evidence)
    shown = _relative(root, evidence / PREFLIGHT_REL.relative_to(EVIDENCE_REL)) or PREFLIGHT_REL.name
    blocked = payload["blocked_arms"]
    if blocked:
        return (
            f"PREFLIGHT-BLOCKED: {len(blocked)} arms blocked ({', '.join(blocked)}); "
            f"{shown} sha256 {digest}",
            EXIT_REFUSED,
        )
    return (
        f"PREFLIGHT-OK: {shown} sha256 {digest} "
        f"({len(payload['records'])} records ok, {len(payload['arms'])} arms ok)",
        EXIT_OK,
    )


def _cli_admit(args, root, evidence):
    admit_arm(args.arm_id, repo_root=root, evidence_root=evidence)
    return f"ADMIT-OK {args.arm_id}", EXIT_OK


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="learnability_protocol",
        description="The Phase 60 run protocol, record preflight and arm admission.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    write = commands.add_parser("write", help="write evidence/run-protocol.json")
    write.add_argument("--amendment-commit", required=True)
    write.add_argument(
        "--no-clip-data-only-arms", action="store_true",
        help="the owner vetoed gradient clipping in the data-only arms (GAP-60-03)",
    )
    write.add_argument(
        "--failed-confirmation-pre-answer", choices=("no_rescue", "rescue"), default=None,
        help="the owner's answer to a G2 confirmation below Tier 1 (GAP-60-09)",
    )
    write.add_argument("--evidence-root", default=None)
    check = commands.add_parser("check", help="is the committed protocol free of drift?")
    check.add_argument("--evidence-root", default=None)
    preflight = commands.add_parser("preflight", help="write evidence/preflight/records.json")
    preflight.add_argument("--evidence-root", default=None)
    admit = commands.add_parser("admit", help="may this arm start now?")
    admit.add_argument("arm_id")
    admit.add_argument("--evidence-root", default=None)
    return parser


_REFUSED_TOKEN = {
    "write": "PROTOCOL-REFUSED",
    "check": "PROTOCOL-REFUSED",
    "preflight": "PREFLIGHT-REFUSED",
    "admit": "ADMIT-REFUSED",
}


def main(argv=None):
    """Command line. Each outcome is one token line and an exit code; nothing is retried."""
    args = _build_parser().parse_args(argv)
    try:
        root, evidence = _cli_roots(args.evidence_root)
        if args.command == "write":
            line, code = _cli_write(args, root, evidence)
        elif args.command == "check":
            line, code = _cli_check(root, evidence)
        elif args.command == "preflight":
            line, code = _cli_preflight(root, evidence)
        else:
            line, code = _cli_admit(args, root, evidence)
    except ProtocolDrift as exc:
        print(f"PROTOCOL-DRIFT: {_one_line(exc)}")
        return EXIT_REFUSED
    except (AdmissionRefused, HarnessHalt, FirstResultExists, ValueError, OSError) as exc:
        print(f"{_REFUSED_TOKEN[args.command]}: {_one_line(exc)}")
        return EXIT_REFUSED
    print(line)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
