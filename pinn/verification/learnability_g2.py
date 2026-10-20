"""Phase 60 (FEAS-03/04/09): Gate G2, the sweep pair, skips and branch state.

After the three Rung-1 experiments a fixed rule decides what runs next. This module
turns that rule into small functions over files that are committed in git, so the
decision is mechanical, recorded once and the same every time.

What it does, in order:

* Gate G2 is the frozen ``g2_fires`` applied to the three committed Rung-1 result
  tiers, in the order of the panel (1632, 851, 4658). ``outcome`` writes the result
  and, when G2 fires, the pinned sweep system, confirmation system and uncovered
  system.
* ``sweep-curve`` reads the four settings of the sweep and names the one setting to
  confirm: the highest ``first_omega_0`` that reached Tier 1 or better, else none.
* ``rescue`` reads the one confirmation run. At Tier 1 or better it is a rescue and
  the frozen rule routes it to owner checkpoint 4. Below Tier 1 it is a failed
  confirmation (GAP-60-09): the run protocol's pre-answer decides, and with no
  pre-answer the owner decides.
* ``skip`` and ``stop-handoff`` record the stop at G2: Rung 2 and the hard-stage
  probes are skipped for one of two pre-registered reasons, and Phase 64 receives
  the evidence and the machine hours.
* The owner's answers (checkpoint 4, and GAP-60-09 when it is asked) are read only
  from the committed ruling files, through ``learnability_ruling``. A continue needs
  a committed GATE-04 re-measure that passed at the approved setting before the
  ladder is taken (D-07, D-11).
* ``branch <name>`` is one read-only query that every later plan runs before it acts.
  It answers TAKEN, NOT-TAKEN or PENDING from the committed records alone.

Rules that govern every function here:

* The frozen scorecard functions are called, never re-implemented. After G2 has
  fired, ``decision_verdict`` is never given a later-rung input.
* A decision is taken only from a file that is tracked and clean in git. A branch
  query reports PENDING for an uncommitted deciding file and a writer exits 2.
* Every file is written once (exclusive create). A second write is refused.
* Records hold repo-relative paths and SHA-256 digests only.
* ``OwnerRouted`` and ``FailedConfirmationOwnerStop`` are handled in ``main`` and
  nowhere else: ``main`` prints them, exits 3, and nothing retries or continues.

The module imports the arm catalog, the ruling loaders, the evidence writer and the
frozen scorecard. It never imports the runner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import numbers
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pinn.verification import evidence_io
from pinn.verification.feasibility_scorecard import (
    OwnerRouted,
    decision_verdict,
    g2_fires,
    load_scorecard,
)
from pinn.verification.learnability_arms import (
    EVIDENCE_REL,
    EXIT_OK,
    EXIT_OWNER,
    EXIT_REFUSED,
    PANEL_INNER_LAPS,
    PANEL_SYSTEMS,
    RUN_SCHEMA,
    FirstResultExists,
    UnknownArm,
    arm_evidence_dir,
    arm_run_dir,
    arm_spec,
    catalog,
    write_record_exclusive,
)
from pinn.verification.learnability_ruling import (
    RulingError,
    RulingMissing,
    RulingUncommitted,
    load_checkpoint4_ruling,
    load_gap6009_ruling,
    tracked_and_clean,
)

__all__ = [
    "BRANCH_NAMES",
    "EXIT_BRANCH_PENDING",
    "G2_REL",
    "LEVEL3_SKIPPED",
    "NOT_CONFIRMED_LABEL",
    "NOT_TAKEN",
    "OUTCOME_SCHEMA",
    "PENDING",
    "REMEASURE_REL",
    "REMEASURE_SCHEMA",
    "R_REF_APPROVED_REL",
    "SKIP_REASONS",
    "TAKEN",
    "BranchState",
    "FailedConfirmationOwnerStop",
    "G2Halt",
    "G2Pending",
    "Remeasure",
    "Rung1Record",
    "UncommittedInput",
    "branch_state",
    "confirmed_omega",
    "g2_outcome",
    "load_rung1_records",
    "main",
    "parse_remeasure",
    "rescue_outcome",
    "stop_handoff",
    "sweep_curve",
    "sweep_plan",
    "write_outcome",
    "write_skip_records",
]

_REPO_ROOT = Path(__file__).resolve().parents[2]

G2_REL = EVIDENCE_REL / "g2"
OUTCOME_NAME = "g2-outcome.json"
CURVE_NAME = "sweep-curve.json"
RESCUE_NAME = "rescue.json"
SKIP_NAME = "skip-records.json"
HANDOFF_NAME = "stop-handoff.json"
PROTOCOL_NAME = "run-protocol.json"
# D-07 / GAP-60-10: the GATE-04 re-measure after an owner continue. Plan 60-09 writes both
# files under the continue evidence directory; this module only reads the record.
REMEASURE_REL = EVIDENCE_REL / "continue" / "gate04-remeasure.json"
R_REF_APPROVED_REL = EVIDENCE_REL / "continue" / "r-ref-approved.json"
REMEASURE_SCHEMA = "phase60-gate04-remeasure/v1"
OUTCOME_SCHEMA = "phase60-g2-outcome/v1"
CURVE_SCHEMA = "phase60-sweep-curve/v1"
RESCUE_SCHEMA = "phase60-rescue/v1"
SKIP_SCHEMA = "phase60-skip-records/v1"
HANDOFF_SCHEMA = "phase60-stop-handoff/v1"
# A branch query that cannot decide yet (a deciding file is missing or uncommitted).
EXIT_BRANCH_PENDING = 4

TAKEN = "TAKEN"
NOT_TAKEN = "NOT-TAKEN"
PENDING = "PENDING"
BRANCH_NAMES = (
    "sweep",
    "confirmation",
    "owner-decision",
    "stop",
    "continue-gate",
    "ladder",
)

# The two pre-registered reasons for skipping Rung 2 and FEAS-09 (SPEC Requirement 7).
# U+2463 is the circled digit four.
REASON_NO_RESCUE = "no rescue"
REASON_GO_TO_VERDICT = "checkpoint \u2463 answered go to the verdict"
SKIP_REASONS = (REASON_NO_RESCUE, REASON_GO_TO_VERDICT)
LEVEL3_SKIPPED = "not tested (skipped at G2)"
PHASES_61_63_SKIPPED = "skipped at G2, not failed"
SELECTED_LABEL = "selected for confirmation"
NOT_CONFIRMED_LABEL = "reached Tier 1, not confirmed (one-confirmation budget)"
BELOW_LABEL = "below Tier 1"
# GAP-60-09: what a failed confirmation means, when the run protocol pre-answers it.
PRE_ANSWERS = (None, "no_rescue", "rescue")
# Arm paths of the catalog that belong to Rung 2, the probes and the continue path.
_LADDER_PATHS = ("g2_passed", "continue")


class G2Halt(RuntimeError):
    """A refused write or an inconsistent record. Nothing further runs on this path."""


class G2Pending(RuntimeError):
    """A deciding file is not recorded yet, so the question cannot be answered."""


class UncommittedInput(G2Halt):
    """A deciding file exists but is not tracked and clean in git."""

    def __init__(self, relative):
        super().__init__(f"uncommitted {relative}")
        self.relative = relative


class FailedConfirmationOwnerStop(Exception):
    """The G2 confirmation ended below Tier 1 and the run protocol holds no pre-answer.

    What that means is the owner's to say (GAP-60-09). Like ``OwnerRouted`` it is
    handled in ``main`` and nowhere else; nothing continues or retries.
    """

    MESSAGE = "failed confirmation (GAP-60-09)"

    def __init__(self):
        super().__init__(self.MESSAGE)


@dataclass(frozen=True)
class Rung1Record:
    """What Gate G2 needs from one committed Rung-1 record."""

    system_id: int
    arm_id: str
    path: str
    sha256: str
    tier: int


@dataclass(frozen=True)
class BranchState:
    """The answer to one branch query. ``first_omega_0`` is set only where a setting is named."""

    name: str
    status: str
    reason: str
    first_omega_0: float | None = None
    omega_provenance: str | None = None


@dataclass(frozen=True)
class _Loaded:
    payload: dict
    sha256: str
    path: str


@dataclass(frozen=True)
class _Route:
    """Where the committed records send the ladder: past G2, or into a stop."""

    kind: str  # "passed", "stop" or "continue"
    reason: str
    basis: tuple = ()
    ruling: object = None  # the checkpoint 4 ruling, on a go-to-verdict stop or a continue


# ---------------------------------------------------------------------------
# Committed inputs.
# ---------------------------------------------------------------------------

def _git(repo_root, *args):
    return subprocess.run(
        ["git", *args], cwd=str(repo_root), capture_output=True, text=True, check=False
    )


def _repo_root_of(path):
    """The git top level above ``path`` (which need not exist yet)."""
    probe = Path(path).resolve()
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    if probe.is_file():
        probe = probe.parent
    proc = _git(probe, "rev-parse", "--show-toplevel")
    if proc.returncode != 0 or not proc.stdout.strip():
        raise G2Halt("the evidence root is not inside a git repository")
    return Path(proc.stdout.strip()).resolve()


def _json_form(payload):
    """``payload`` as it reads back from a canonical JSON file."""
    return json.loads(evidence_io.canonical_json_bytes(payload))


class _Inputs:
    """The committed files one query reads, each checked once."""

    def __init__(self, evidence_root, repo_root=None):
        self.evidence_root = Path(evidence_root)
        if repo_root is None:
            self.repo_root = _repo_root_of(self.evidence_root)
        else:
            self.repo_root = Path(repo_root).resolve()
        self._bytes = {}
        self._json = {}

    def under_evidence(self, *parts):
        return self.evidence_root.joinpath(*parts)

    def relative(self, path):
        """``path`` relative to the repository, as posix text."""
        try:
            return Path(path).resolve().relative_to(self.repo_root).as_posix()
        except ValueError as exc:
            raise G2Halt(f"{Path(path).name} lies outside the repository") from exc

    def committed_bytes(self, path):
        """``(bytes, repo-relative path)`` of a tracked, clean file.

        Pending when the file is absent, ``UncommittedInput`` when it is present but
        untracked or changed.
        """
        path = Path(path)
        key = str(path)
        if key in self._bytes:
            return self._bytes[key]
        if path.is_symlink():
            raise G2Halt(f"{self.relative(path)} is a symbolic link")
        relative = self.relative(path)
        if not path.exists():
            raise G2Pending(f"{relative} is not recorded")
        if not path.is_file():
            raise G2Halt(f"{relative} is not a regular file")
        if not tracked_and_clean(self.repo_root, relative):
            raise UncommittedInput(relative)
        self._bytes[key] = (path.read_bytes(), relative)
        return self._bytes[key]

    def json(self, path):
        key = str(Path(path))
        if key in self._json:
            return self._json[key]
        raw, relative = self.committed_bytes(path)
        try:
            payload = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise G2Halt(f"{relative} is not valid JSON") from exc
        if not isinstance(payload, dict):
            raise G2Halt(f"{relative} must hold a JSON object")
        self._json[key] = _Loaded(
            payload=payload, sha256=hashlib.sha256(raw).hexdigest(), path=relative
        )
        return self._json[key]


def _cite(loaded):
    return {"path": loaded.path, "sha256": loaded.sha256}


def _write_once(inputs, name, payload):
    """Create ``g2/<name>`` exactly once; return its repo-relative path."""
    path = inputs.under_evidence("g2", name)
    relative = inputs.relative(path)
    try:
        write_record_exclusive(path, payload)
    except FirstResultExists as exc:
        raise G2Halt(f"{relative} already exists; the first record is the result") from exc
    return relative


# ---------------------------------------------------------------------------
# Arm records.
# ---------------------------------------------------------------------------

def _catalog_spec(arm_id):
    try:
        return arm_spec(arm_id)
    except UnknownArm as exc:
        raise G2Halt(f"{arm_id} is not an arm of the closed catalog") from exc


def _arm_record(inputs, arm_id):
    """The committed, real-kind record of one arm, checked against its own id."""
    loaded = inputs.json(arm_evidence_dir(arm_id, evidence_root=inputs.evidence_root) / "record.json")
    payload = loaded.payload
    if payload.get("schema") != RUN_SCHEMA:
        raise G2Halt(f"{loaded.path} does not carry the schema {RUN_SCHEMA}")
    if payload.get("run_kind") != "real":
        raise G2Halt(f"{loaded.path} is not a real-arm record")
    if payload.get("arm_id") != arm_id:
        raise G2Halt(f"{loaded.path} is filed under {arm_id} but names another arm")
    return loaded


def _result(loaded, *required):
    """The record's ``result`` block, with an integer tier and any extra keys named."""
    result = loaded.payload.get("result")
    if not isinstance(result, dict):
        raise G2Halt(f"{loaded.path} has no result block")
    tier = result.get("tier")
    if isinstance(tier, bool) or not isinstance(tier, int):
        raise G2Halt(f"{loaded.path} has no integer result.tier")
    for key in required:
        if key not in result:
            raise G2Halt(f"{loaded.path} has no result.{key}")
    return result


def _runs_at(loaded, spec, omega):
    """The record ran at ``omega`` under the provenance its catalog arm names."""
    value = loaded.payload.get("first_omega_0")
    if (
        isinstance(value, bool)
        or not isinstance(value, numbers.Real)
        or float(value) != omega
        or loaded.payload.get("omega_provenance") != spec.omega_provenance
    ):
        raise G2Halt(
            f"{loaded.path} ({spec.arm_id}) did not run at first_omega_0 {omega} "
            f"under {spec.omega_provenance}"
        )


def _rung1_records(inputs):
    records = []
    for system in PANEL_SYSTEMS:
        arm_id = f"r1-{system}"
        loaded = _arm_record(inputs, arm_id)
        result = _result(loaded)
        records.append(
            Rung1Record(
                system_id=system,
                arm_id=arm_id,
                path=loaded.path,
                sha256=loaded.sha256,
                tier=result["tier"],
            )
        )
    return tuple(records)


def load_rung1_records(evidence_root, *, repo_root=None):
    """The three committed Rung-1 records, in panel order.

    A record that is not there makes the answer pending (``G2Pending``); one that is
    there but uncommitted or malformed halts.
    """
    return _rung1_records(_Inputs(evidence_root, repo_root))


# ---------------------------------------------------------------------------
# Gate G2 and the pinned sweep pair.
# ---------------------------------------------------------------------------

def sweep_plan(failing_ids):
    """``(sweep, confirmation, uncovered)`` for the failing panel systems (SPEC Requirement 6).

    The lap counts 10.47, 18.61 and 39.35 pin the pair: sweep the failing system with
    the fewest inner laps and confirm on the next one. The panel system that neither
    covers is the uncovered one. Fewer than two failing systems is a ``ValueError``.
    """
    if isinstance(failing_ids, (str, bytes)):
        raise ValueError("failing_ids must be a sequence of panel system ids")
    ids = list(failing_ids)
    for item in ids:
        if isinstance(item, bool) or not isinstance(item, int) or item not in PANEL_SYSTEMS:
            raise ValueError(f"{item!r} is not a panel system {PANEL_SYSTEMS}")
    if len(set(ids)) != len(ids):
        raise ValueError("failing_ids must not repeat a system")
    if len(ids) < 2:
        raise ValueError("a sweep pair needs at least two failing systems")
    ordered = sorted(ids, key=lambda system: PANEL_INNER_LAPS[system])
    sweep, confirmation = ordered[0], ordered[1]
    (uncovered,) = [system for system in PANEL_SYSTEMS if system not in (sweep, confirmation)]
    return sweep, confirmation, uncovered


def g2_outcome(records, *, scorecard):
    """Gate G2 from the three Rung-1 result tiers, as the dict ``g2-outcome.json`` holds.

    ``g2_fired`` is the frozen ``g2_fires`` on the tiers in panel order. An
    inconclusive Rung 1 enters at the tier of its result. When G2 fires the dict also
    names the sweep, confirmation and uncovered systems.
    """
    records = tuple(records)
    if [getattr(record, "system_id", None) for record in records] != list(PANEL_SYSTEMS):
        raise ValueError(f"records must be the panel systems {PANEL_SYSTEMS} in panel order")
    tiers = []
    for record in records:
        if isinstance(record.tier, bool) or not isinstance(record.tier, int):
            raise ValueError(f"the tier of {record.arm_id} must be an integer")
        tiers.append(record.tier)
    below = int(scorecard.section("gate_g2")["trigger_below_tier"])
    failing = [record.system_id for record in records if record.tier < below]
    fired = g2_fires(tiers, scorecard=scorecard)
    outcome = {
        "schema": OUTCOME_SCHEMA,
        "panel_systems": list(PANEL_SYSTEMS),
        "tiers": tiers,
        "records": [
            {
                "system_id": record.system_id,
                "arm_id": record.arm_id,
                "path": record.path,
                "sha256": record.sha256,
                "tier": record.tier,
            }
            for record in records
        ],
        "trigger_below_tier": below,
        "failing_systems": failing,
        "g2_fired": fired,
    }
    if fired:
        sweep, confirmation, uncovered = sweep_plan(failing)
        outcome["sweep_system"] = sweep
        outcome["confirmation_system"] = confirmation
        outcome["uncovered_system"] = uncovered
    return outcome


def _write_outcome(inputs, card):
    outcome = g2_outcome(_rung1_records(inputs), scorecard=card)
    return outcome, _write_once(inputs, OUTCOME_NAME, outcome)


def write_outcome(*, evidence_root, repo_root=None, scorecard=None):
    """Compute Gate G2 from the committed Rung-1 records and write ``g2/g2-outcome.json`` once."""
    card = load_scorecard() if scorecard is None else scorecard
    return _write_outcome(_Inputs(evidence_root, repo_root), card)[0]


def _verified_outcome(inputs, card):
    """``g2-outcome.json``, recomputed from the committed Rung-1 records (T-60-16)."""
    loaded = inputs.json(inputs.under_evidence("g2", OUTCOME_NAME))
    try:
        records = _rung1_records(inputs)
    except G2Pending as exc:
        raise G2Halt(f"{loaded.path} cites a Rung-1 record that is not recorded") from exc
    if loaded.payload != _json_form(g2_outcome(records, scorecard=card)):
        raise G2Halt(f"{loaded.path} disagrees with the committed Rung-1 records")
    return loaded


# ---------------------------------------------------------------------------
# The settings sweep and its one confirmation.
# ---------------------------------------------------------------------------

def confirmed_omega(rows, *, scorecard):
    """The setting the one confirmation run uses: the highest ``first_omega_0`` at Tier 1 or better.

    ``rows`` hold ``first_omega_0`` and ``tier`` for each sweep setting. "Reaches Tier 1"
    includes Tier exactly 1. The settings are distinct, so there is no tie-break. The
    answer is one of the recorded settings, never an interpolated one, and ``None``
    when no setting reached the rescue tier (no confirmation and no rescue).
    """
    rescue_tier = int(scorecard.section("gate_g2")["rescue_tier"])
    settings = []
    reaching = []
    for row in rows:
        try:
            omega, tier = row["first_omega_0"], row["tier"]
        except (KeyError, TypeError) as exc:
            raise ValueError("each row needs first_omega_0 and tier") from exc
        if isinstance(omega, bool) or not isinstance(omega, numbers.Real):
            raise ValueError(f"first_omega_0 must be a real number; got {omega!r}")
        omega = float(omega)
        if not math.isfinite(omega) or omega <= 0.0:
            raise ValueError(f"first_omega_0 must be finite and positive; got {omega!r}")
        if isinstance(tier, bool) or not isinstance(tier, int):
            raise ValueError(f"tier must be an integer; got {tier!r}")
        settings.append(omega)
        if tier >= rescue_tier:
            reaching.append(omega)
    if len(set(settings)) != len(settings):
        raise ValueError("the sweep settings must be distinct")
    return max(reaching) if reaching else None


def _grid(card):
    return tuple(float(value) for value in card.section("gate_g2")["grid"])


def _setting_digits(omega):
    """``60.0`` -> ``"060"``: the three digits an arm id carries."""
    if float(omega) != int(omega):
        raise G2Halt(f"first_omega_0 {omega} has no three-digit arm suffix")
    return f"{int(omega):03d}"


def _horizons(loaded, result, card):
    deltas = [float(delta) for delta in card.section("metrics")["valid_horizon_deltas"]]
    try:
        seen = [float(pair[0]) for pair in result["h"]]
    except (TypeError, ValueError, IndexError) as exc:
        raise G2Halt(f"{loaded.path} result.h is not a list of [delta, value] pairs") from exc
    if seen != deltas:
        raise G2Halt(f"{loaded.path} result.h does not hold the horizons {deltas}")
    return result["h"]


def _sweep_row(inputs, card, arm_id, omega):
    """One curve row: the setting, the arm, its record hash and its scores."""
    spec = _catalog_spec(arm_id)
    loaded = _arm_record(inputs, arm_id)
    _runs_at(loaded, spec, omega)
    result = _result(loaded, "E", "eps_h", "h")
    return {
        "first_omega_0": omega,
        "arm_id": arm_id,
        "record_sha256": loaded.sha256,
        "tier": result["tier"],
        "E": result["E"],
        "eps_h": result["eps_h"],
        "h": _horizons(loaded, result, card),
    }


def _build_sweep_curve(inputs, card, outcome):
    """The sweep curve of the recorded sweep system, from its four committed records."""
    payload = outcome.payload
    if not payload["g2_fired"]:
        raise G2Halt("g2 did not fire, so there is no settings sweep")
    sweep_system = payload["sweep_system"]
    rows = [
        _sweep_row(inputs, card, f"g2s-{sweep_system}-w{_setting_digits(omega)}", omega)
        for omega in _grid(card)
    ]
    rescue_tier = int(card.section("gate_g2")["rescue_tier"])
    confirmed = confirmed_omega(rows, scorecard=card)
    labelled = []
    for row in rows:
        if confirmed is not None and row["first_omega_0"] == confirmed:
            label = SELECTED_LABEL
        elif row["tier"] >= rescue_tier:
            label = NOT_CONFIRMED_LABEL
        else:
            label = BELOW_LABEL
        labelled.append({**row, "label": label})
    confirmation_arm = None
    if confirmed is not None:
        confirmation_arm = (
            f"g2c-{payload['confirmation_system']}-w{_setting_digits(confirmed)}"
        )
        _catalog_spec(confirmation_arm)
    return {
        "schema": CURVE_SCHEMA,
        "g2_outcome_sha256": outcome.sha256,
        "sweep_system": sweep_system,
        "confirmation_system": payload["confirmation_system"],
        "uncovered_system": payload["uncovered_system"],
        "grid": list(_grid(card)),
        "rescue_tier": rescue_tier,
        "rows": labelled,
        "confirmed_first_omega_0": confirmed,
        "confirmation_arm": confirmation_arm,
        "outcome": "no_rescue" if confirmed is None else "confirmation_pending",
    }


def _write_sweep_curve(inputs, card):
    curve = _build_sweep_curve(inputs, card, _verified_outcome(inputs, card))
    return curve, _write_once(inputs, CURVE_NAME, curve)


def sweep_curve(*, evidence_root, repo_root=None, scorecard=None):
    """Read the four committed sweep records and write ``g2/sweep-curve.json`` once.

    All four settings must be recorded (in grid order, even after a success) before any
    confirmation is named; until then the answer is pending.
    """
    card = load_scorecard() if scorecard is None else scorecard
    return _write_sweep_curve(_Inputs(evidence_root, repo_root), card)[0]


def _verified_curve(inputs, card, outcome):
    """``sweep-curve.json``, recomputed from the four committed sweep records."""
    loaded = inputs.json(inputs.under_evidence("g2", CURVE_NAME))
    try:
        expected = _build_sweep_curve(inputs, card, outcome)
    except G2Pending as exc:
        raise G2Halt(f"{loaded.path} cites a sweep record that is not recorded") from exc
    if loaded.payload != _json_form(expected):
        raise G2Halt(f"{loaded.path} disagrees with the committed sweep records")
    return loaded


# ---------------------------------------------------------------------------
# The confirmation outcome: rescue, or failed confirmation (GAP-60-09).
# ---------------------------------------------------------------------------

def _protocol_pre_answer(inputs):
    """``g2.failed_confirmation_pre_answer`` of the committed run protocol (GAP-60-09)."""
    try:
        loaded = inputs.json(inputs.under_evidence(PROTOCOL_NAME))
    except G2Pending as exc:
        raise G2Halt("the run protocol is not recorded, so the pre-answer is unknown") from exc
    section = loaded.payload.get("g2")
    if not isinstance(section, dict) or "failed_confirmation_pre_answer" not in section:
        raise G2Halt(f"{loaded.path} has no g2.failed_confirmation_pre_answer")
    pre_answer = section["failed_confirmation_pre_answer"]
    if pre_answer is not None and pre_answer not in ("no_rescue", "rescue"):
        raise G2Halt(f"{loaded.path} g2.failed_confirmation_pre_answer is not null, no_rescue or rescue")
    return pre_answer, loaded


def _build_rescue(inputs, card, curve, pre_answer):
    """The rescue record: the one confirmation run, read against the rescue tier."""
    plan = curve.payload
    if plan["outcome"] != "confirmation_pending":
        raise G2Halt("the sweep found no setting at Tier 1, so there is no confirmation to evaluate")
    arm_id = plan["confirmation_arm"]
    spec = _catalog_spec(arm_id)
    loaded = _arm_record(inputs, arm_id)
    _runs_at(loaded, spec, plan["confirmed_first_omega_0"])
    result = _result(loaded, "E", "eps_h", "h")
    rescue_tier = int(card.section("gate_g2")["rescue_tier"])
    return {
        "schema": RESCUE_SCHEMA,
        "outcome": "rescue" if result["tier"] >= rescue_tier else "failed_confirmation",
        "confirmation_arm": arm_id,
        "confirmation_system": spec.system_id,
        "confirmed_first_omega_0": plan["confirmed_first_omega_0"],
        "tier": result["tier"],
        "E": result["E"],
        "eps_h": result["eps_h"],
        "h": _horizons(loaded, result, card),
        "rescue_tier": rescue_tier,
        "record": _cite(loaded),
        "sweep_curve_sha256": curve.sha256,
        "pre_answer": pre_answer,
    }


def _route_confirmation(card, payload):
    """Hand a written rescue record to the frozen rule, or to the owner, or to the stop path."""
    rescued = payload["outcome"] == "rescue" or payload["pre_answer"] == "rescue"
    if rescued:
        decision_verdict(
            g2_fired=True,
            sweep_rescued=True,
            rung2b_counts=None,
            rung3_counts=None,
            control_branch=None,
            rung1_beats_formula=None,
            scorecard=card,
        )
        raise G2Halt("the frozen decision rule did not route the rescue to owner checkpoint 4")
    if payload["pre_answer"] is None:
        raise FailedConfirmationOwnerStop()
    return payload


def _rescue(inputs, card, pre_answer):
    """Write ``rescue.json`` first, then route it. May raise an owner stop; never catches one."""
    outcome = _verified_outcome(inputs, card)
    curve = _verified_curve(inputs, card, outcome)
    payload = _build_rescue(inputs, card, curve, pre_answer)
    _write_once(inputs, RESCUE_NAME, payload)
    return _route_confirmation(card, payload)


def rescue_outcome(*, evidence_root, pre_answer, repo_root=None, scorecard=None):
    """Evaluate the one confirmation run, write ``g2/rescue.json`` once, then route it.

    At Tier 1 or better (or with the pre-answer ``rescue``) the frozen
    ``decision_verdict`` is called with ``sweep_rescued=True`` and four ``None``
    later-rung inputs, and its ``OwnerRouted("owner checkpoint 4")`` propagates. A
    failed confirmation with no pre-answer raises ``FailedConfirmationOwnerStop``
    without calling the verdict rule. With the pre-answer ``no_rescue`` the record is
    returned and the stop path follows. The file is written before any raise.
    """
    if pre_answer not in PRE_ANSWERS:
        raise ValueError(f"pre_answer must be None, 'no_rescue' or 'rescue'; got {pre_answer!r}")
    card = load_scorecard() if scorecard is None else scorecard
    return _rescue(_Inputs(evidence_root, repo_root), card, pre_answer)


def _verified_rescue(inputs, card, curve):
    """``rescue.json``, recomputed from the confirmation record and the run protocol."""
    loaded = inputs.json(inputs.under_evidence("g2", RESCUE_NAME))
    pre_answer, _protocol = _protocol_pre_answer(inputs)
    try:
        expected = _build_rescue(inputs, card, curve, pre_answer)
    except G2Pending as exc:
        raise G2Halt(f"{loaded.path} cites a confirmation record that is not recorded") from exc
    if loaded.payload != _json_form(expected):
        raise G2Halt(f"{loaded.path} disagrees with the confirmation record or the run protocol")
    return loaded


# ---------------------------------------------------------------------------
# The GATE-04 re-measure record and the owner's rulings.
# ---------------------------------------------------------------------------

_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True)
class Remeasure:
    """The fields of ``gate04-remeasure.json`` that the ladder reads."""

    verdict: str
    complete_pass: bool
    first_omega_0: float
    ruling_sha256: str
    r_ref_artifact: dict | None


def parse_remeasure(payload, *, path="the re-measure record"):
    """Validate a GATE-04 re-measure record and return the fields the ladder reads.

    A PASS must be a complete pass and cite the re-measured reference (``path`` and
    ``sha256``); a BLOCK must not claim a complete pass. Anything else is a ``G2Halt``.
    """

    def refuse(reason):
        raise G2Halt(f"{path} {reason}")

    if not isinstance(payload, dict) or payload.get("schema") != REMEASURE_SCHEMA:
        refuse(f"does not carry the schema {REMEASURE_SCHEMA}")
    verdict = payload.get("verdict")
    if verdict not in ("PASS", "BLOCK"):
        refuse("has a verdict other than PASS or BLOCK")
    complete = payload.get("complete_pass")
    if not isinstance(complete, bool):
        refuse("has no boolean complete_pass")
    omega = payload.get("first_omega_0")
    if (
        isinstance(omega, bool)
        or not isinstance(omega, numbers.Real)
        or not math.isfinite(omega)
        or omega <= 0
    ):
        refuse("has no finite positive first_omega_0")
    ruling_sha = payload.get("ruling_sha256")
    if not isinstance(ruling_sha, str) or _SHA256.fullmatch(ruling_sha) is None:
        refuse("has no ruling_sha256")
    artifact = None
    if verdict == "PASS":
        if complete is not True:
            refuse("is a PASS that is not a complete pass")
        cited = payload.get("r_ref_artifact")
        if (
            not isinstance(cited, dict)
            or not isinstance(cited.get("path"), str)
            or not cited["path"]
            or not isinstance(cited.get("sha256"), str)
            or _SHA256.fullmatch(cited["sha256"]) is None
        ):
            refuse("is a PASS without a re-measured reference (path and sha256)")
        artifact = {"path": cited["path"], "sha256": cited["sha256"]}
    elif complete is not False:
        refuse("is a BLOCK that claims a complete pass")
    return Remeasure(verdict, complete, float(omega), ruling_sha, artifact)


def _load_ruling(inputs, loader, what):
    """A committed owner ruling, or the reason it cannot be used yet."""
    try:
        return loader(repo_root=inputs.repo_root)
    except RulingMissing as exc:
        raise G2Pending(f"{what} is unanswered: no committed ruling") from exc
    except RulingUncommitted as exc:
        raise UncommittedInput(exc.relative) from exc
    except RulingError as exc:
        raise G2Halt(f"the {what} ruling cannot be used: {exc}") from exc


def _cite_ruling(ruling):
    return {"path": ruling.path, "sha256": ruling.sha256}


# ---------------------------------------------------------------------------
# Where the committed records send the ladder.
# ---------------------------------------------------------------------------

def _route(inputs, card):
    """``passed`` when G2 did not fire, ``stop`` with its reason, ``continue`` with the ruling, or a pending/halt exception."""
    outcome = _verified_outcome(inputs, card)
    if not outcome.payload["g2_fired"]:
        return _Route("passed", "g2 did not fire", (_cite(outcome),))
    curve = _verified_curve(inputs, card, outcome)
    basis = (_cite(outcome), _cite(curve))
    if curve.payload["outcome"] == "no_rescue":
        return _Route("stop", REASON_NO_RESCUE, basis)
    rescue = _verified_rescue(inputs, card, curve)
    pre_answer, protocol = _protocol_pre_answer(inputs)
    basis += (_cite(rescue), _cite(protocol))
    if rescue.payload["outcome"] == "failed_confirmation":
        if pre_answer == "no_rescue":
            return _Route("stop", REASON_NO_RESCUE, basis)
        if pre_answer is None:
            # GAP-60-09: with no pre-answer the owner says what a failed confirmation means.
            reading = _load_ruling(inputs, load_gap6009_ruling, "failed confirmation (GAP-60-09)")
            basis += (_cite_ruling(reading),)
            if reading.reading == "no_rescue":
                return _Route("stop", REASON_NO_RESCUE, basis)
    # A confirmed rescue, or a failed confirmation read as a rescue: checkpoint 4.
    ruling = _load_ruling(inputs, load_checkpoint4_ruling, "owner checkpoint 4")
    basis += (_cite_ruling(ruling),)
    if ruling.answer == "go-to-verdict":
        return _Route("stop", REASON_GO_TO_VERDICT, basis, ruling)
    return _Route(
        "continue", f"continue at first_omega_0 {ruling.approved_first_omega_0}", basis, ruling
    )


# ---------------------------------------------------------------------------
# Skip records and the Phase 64 handoff (the stop path).
# ---------------------------------------------------------------------------

def _refuse_started_ladder(inputs):
    """A skip or a stop handoff is impossible once a Rung-2, probe or continue arm has started."""
    started = [
        arm_id
        for arm_id, spec in catalog().items()
        if spec.path in _LADDER_PATHS
        and (
            os.path.lexists(arm_evidence_dir(arm_id, evidence_root=inputs.evidence_root))
            or os.path.lexists(arm_run_dir(arm_id, repo_root=inputs.repo_root))
        )
    ]
    if started:
        raise G2Halt(
            "a Rung-2, probe or continue arm has started (" + ", ".join(started) + "), "
            "so the ladder cannot be recorded as skipped"
        )


def _write_skip(inputs, card, reason):
    if not isinstance(reason, str) or reason not in SKIP_REASONS:
        raise G2Halt(f"{reason!r} is not one of the two pre-registered skip reasons")
    _refuse_started_ladder(inputs)
    route = _route(inputs, card)
    if route.kind != "stop":
        raise G2Halt(f"the committed records do not stop the ladder at G2 ({route.reason})")
    if route.reason != reason:
        raise G2Halt(f"the committed records imply the reason {route.reason!r}, not {reason!r}")
    payload = {
        "schema": SKIP_SCHEMA,
        "reason": reason,
        "entries": {
            requirement: {"skipped": True, "reason": reason}
            for requirement in ("FEAS-04", "FEAS-09")
        },
        "level3": LEVEL3_SKIPPED,
        "basis": list(route.basis),
    }
    return payload, _write_once(inputs, SKIP_NAME, payload)


def write_skip_records(reason, *, evidence_root, repo_root=None, scorecard=None):
    """Record FEAS-04 and FEAS-09 as skipped at G2 with one of the two pre-registered reasons.

    The reason must be byte-exact, must be the one the committed records imply, and no
    Rung-2, probe or continue arm may have started (SPEC Requirement 7). Written once.
    """
    card = load_scorecard() if scorecard is None else scorecard
    return _write_skip(_Inputs(evidence_root, repo_root), card, reason)[0]


def _arm_hours(inputs, arm_id):
    loaded = _arm_record(inputs, arm_id)
    wall = loaded.payload.get("wall")
    hours = wall.get("hours") if isinstance(wall, dict) else None
    if (
        isinstance(hours, bool)
        or not isinstance(hours, numbers.Real)
        or not math.isfinite(hours)
        or hours < 0
    ):
        raise G2Halt(f"{loaded.path} has no finite non-negative wall.hours")
    timing = loaded.payload.get("timing")
    seconds = timing.get("seconds_per_step") if isinstance(timing, dict) else None
    if isinstance(seconds, bool) or not isinstance(seconds, numbers.Real) or not math.isfinite(seconds):
        seconds = None
    return {
        "arm_id": arm_id,
        "record": _cite(loaded),
        "wall_hours": float(hours),
        "seconds_per_step": None if seconds is None else float(seconds),
    }


def _stop_arm_ids(inputs, card):
    """The arms that ran on a stop path: Rung 1, the four sweep settings, any confirmation."""
    outcome = _verified_outcome(inputs, card)
    curve = _verified_curve(inputs, card, outcome)
    arm_ids = [entry["arm_id"] for entry in outcome.payload["records"]]
    arm_ids += [row["arm_id"] for row in curve.payload["rows"]]
    if curve.payload["outcome"] == "confirmation_pending":
        arm_ids.append(curve.payload["confirmation_arm"])
    return arm_ids


def _write_stop_handoff(inputs, card):
    _refuse_started_ladder(inputs)
    route = _route(inputs, card)
    if route.kind != "stop":
        raise G2Halt(f"the committed records do not stop the ladder at G2 ({route.reason})")
    verdict = owner_answer = note = None
    if route.reason == REASON_GO_TO_VERDICT:
        # The owner chose the verdict at checkpoint 4: their answer stands, and the
        # verdict rule is not called at all on this path.
        owner_answer = {
            "checkpoint": 4,
            "answer": route.ruling.answer,
            "ruling_path": route.ruling.path,
            "ruling_sha256": route.ruling.sha256,
        }
        note = f"{REASON_GO_TO_VERDICT}; no decision_verdict call is made on this path"
    else:
        # On the no-rescue path the frozen rule gets g2_fired and no rescue, and nothing
        # else: every later-rung input is None, so no skipped result enters the verdict.
        verdict = decision_verdict(
            g2_fired=True,
            sweep_rescued=False,
            rung2b_counts=None,
            rung3_counts=None,
            control_branch=None,
            rung1_beats_formula=None,
            scorecard=card,
        )
    arms = [_arm_hours(inputs, arm_id) for arm_id in _stop_arm_ids(inputs, card)]
    payload = {
        "schema": HANDOFF_SCHEMA,
        "stop_reason": route.reason,
        "basis": list(route.basis),
        "verdict": verdict,
        "owner_answer": owner_answer,
        "verdict_note": note,
        "level3": LEVEL3_SKIPPED,
        "phases_61_63": PHASES_61_63_SKIPPED,
        "next_phase": 64,
        "arms": arms,
        "total_wall_hours": sum(arm["wall_hours"] for arm in arms),
    }
    return payload, _write_once(inputs, HANDOFF_NAME, payload)


def stop_handoff(*, evidence_root, repo_root=None, scorecard=None):
    """Write the Phase 64 handoff for a stop at G2 once: verdict, skipped levels, machine hours."""
    card = load_scorecard() if scorecard is None else scorecard
    return _write_stop_handoff(_Inputs(evidence_root, repo_root), card)[0]


# ---------------------------------------------------------------------------
# The branch query.
# ---------------------------------------------------------------------------

def _branch_sweep(inputs, card):
    outcome = _verified_outcome(inputs, card).payload
    if outcome["g2_fired"]:
        return BranchState("sweep", TAKEN, f"g2 fired; sweep system {outcome['sweep_system']}")
    return BranchState("sweep", NOT_TAKEN, "g2 did not fire")


def _fired_curve(inputs, card, name):
    """``(BranchState, None)`` when G2 did not fire, else ``(None, curve payload)``."""
    outcome = _verified_outcome(inputs, card)
    if not outcome.payload["g2_fired"]:
        return BranchState(name, NOT_TAKEN, "g2 did not fire"), None
    return None, _verified_curve(inputs, card, outcome)


def _branch_confirmation(inputs, card):
    state, curve = _fired_curve(inputs, card, "confirmation")
    if state is not None:
        return state
    plan = curve.payload
    if plan["outcome"] == "no_rescue":
        return BranchState("confirmation", NOT_TAKEN, "no sweep setting reached Tier 1")
    return BranchState(
        "confirmation", TAKEN,
        f"confirm {plan['confirmation_arm']} at first_omega_0 {plan['confirmed_first_omega_0']}",
    )


def _branch_owner_decision(inputs, card):
    state, curve = _fired_curve(inputs, card, "owner-decision")
    if state is not None:
        return state
    if curve.payload["outcome"] == "no_rescue":
        return BranchState("owner-decision", NOT_TAKEN, "no rescue: no sweep setting reached Tier 1")
    rescue = _verified_rescue(inputs, card, curve).payload
    if rescue["outcome"] == "rescue":
        return BranchState("owner-decision", TAKEN, "confirmed rescue: owner checkpoint 4")
    pre_answer = rescue["pre_answer"]
    if pre_answer == "no_rescue":
        return BranchState(
            "owner-decision", NOT_TAKEN, "the failed confirmation was pre-answered no rescue"
        )
    if pre_answer == "rescue":
        return BranchState(
            "owner-decision", TAKEN, "failed confirmation pre-answered rescue: owner checkpoint 4"
        )
    return BranchState(
        "owner-decision", TAKEN,
        "failed confirmation with no pre-answer: the owner decides (GAP-60-09)",
    )


def _branch_stop(inputs, card):
    route = _route(inputs, card)
    if route.kind == "stop":
        return BranchState("stop", TAKEN, route.reason)
    return BranchState("stop", NOT_TAKEN, route.reason)


def _branch_continue_gate(inputs, card):
    route = _route(inputs, card)
    if route.kind == "continue":
        return BranchState(
            "continue-gate", TAKEN, route.reason,
            first_omega_0=route.ruling.approved_first_omega_0, omega_provenance="owner_approved",
        )
    return BranchState("continue-gate", NOT_TAKEN, route.reason)


def _continue_ladder(inputs, route):
    """The ladder after an owner continue: taken once GATE-04 passed at the approved setting."""
    ruling = route.ruling
    omega = ruling.approved_first_omega_0
    try:
        loaded = inputs.json(inputs.under_evidence(*REMEASURE_REL.relative_to(EVIDENCE_REL).parts))
    except G2Pending as exc:
        raise G2Pending(f"the GATE-04 re-measure at first_omega_0 {omega} is not recorded") from exc
    record = parse_remeasure(loaded.payload, path=loaded.path)
    if record.first_omega_0 != omega or record.ruling_sha256 != ruling.sha256:
        raise G2Halt(
            f"{loaded.path} was measured at another setting or under another ruling "
            "than the committed checkpoint 4 ruling"
        )
    if record.verdict == "BLOCK":
        raise G2Pending(f"GATE-04 BLOCK at {omega}; owner")
    return BranchState(
        "ladder", TAKEN, f"continue; first_omega_0 {omega}; owner_approved",
        first_omega_0=omega, omega_provenance="owner_approved",
    )


def _branch_ladder(inputs, card):
    skip_path = inputs.under_evidence("g2", SKIP_NAME)
    skip = inputs.json(skip_path) if os.path.lexists(skip_path) else None
    try:
        route = _route(inputs, card)
    except G2Pending:
        if skip is not None:
            return BranchState("ladder", NOT_TAKEN, "a skip is recorded")
        raise
    if route.kind == "stop":
        if skip is not None and skip.payload.get("reason") != route.reason:
            raise G2Halt(f"{skip.path} records another reason than the committed records imply")
        return BranchState("ladder", NOT_TAKEN, f"the ladder stopped at G2: {route.reason}")
    if skip is not None:
        raise G2Halt(f"{skip.path} records a skip although the committed records take the ladder")
    if route.kind == "continue":
        return _continue_ladder(inputs, route)
    locked = float(card.section("gate_g2")["locked_value"])
    return BranchState(
        "ladder", TAKEN, f"g2 passed; first_omega_0 {locked}",
        first_omega_0=locked, omega_provenance="locked",
    )


_BRANCH_RULES = {
    "sweep": _branch_sweep,
    "confirmation": _branch_confirmation,
    "owner-decision": _branch_owner_decision,
    "stop": _branch_stop,
    "continue-gate": _branch_continue_gate,
    "ladder": _branch_ladder,
}


def branch_state(name, *, evidence_root, repo_root=None, scorecard=None):
    """Whether the named branch of the ladder is taken, not taken, or not yet decidable.

    Read-only. Every deciding file must be tracked and clean in git; an uncommitted one
    gives PENDING with the reason ``uncommitted <path>``. A record that disagrees with
    the records it was computed from raises ``G2Halt``.
    """
    if name not in BRANCH_NAMES:
        raise ValueError(f"unknown branch {name!r}; the branches are {BRANCH_NAMES}")
    card = load_scorecard() if scorecard is None else scorecard
    inputs = _Inputs(evidence_root, repo_root)
    try:
        return _BRANCH_RULES[name](inputs, card)
    except UncommittedInput as exc:
        return BranchState(name, PENDING, f"uncommitted {exc.relative}")
    except G2Pending as exc:
        return BranchState(name, PENDING, str(exc))


# ---------------------------------------------------------------------------
# The command line.
# ---------------------------------------------------------------------------

def _build_parser():
    parser = argparse.ArgumentParser(
        prog="learnability_g2",
        description="Gate G2, the sweep pair, rescue and skip records, and the branch query.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name, text in (
        ("outcome", "write g2/g2-outcome.json once"),
        ("sweep-curve", "write g2/sweep-curve.json once"),
        ("rescue", "write g2/rescue.json once, then route the confirmation"),
        ("stop-handoff", "write g2/stop-handoff.json once"),
    ):
        commands.add_parser(name, help=text).add_argument("--evidence-root", default=None)
    skip = commands.add_parser("skip", help="write g2/skip-records.json once")
    skip.add_argument("--reason", required=True)
    skip.add_argument("--evidence-root", default=None)
    branch = commands.add_parser("branch", help="read-only: is a branch of the ladder taken?")
    branch.add_argument("name", choices=BRANCH_NAMES)
    branch.add_argument("--evidence-root", default=None)
    return parser


def _run(args, evidence_root):
    """Run one command; return ``(token line, exit code)``."""
    if args.command == "branch":
        state = branch_state(args.name, evidence_root=evidence_root)
        code = EXIT_BRANCH_PENDING if state.status == PENDING else EXIT_OK
        return f"BRANCH-{state.status}: {state.name} ({state.reason})", code
    card = load_scorecard()
    inputs = _Inputs(evidence_root)
    if args.command == "outcome":
        outcome, relative = _write_outcome(inputs, card)
        tiers = " ".join(str(tier) for tier in outcome["tiers"])
        fired = "true" if outcome["g2_fired"] else "false"
        return f"G2-OUTCOME-WRITTEN: {relative} (g2_fired {fired}; tiers {tiers})", EXIT_OK
    if args.command == "sweep-curve":
        curve, relative = _write_sweep_curve(inputs, card)
        detail = f"outcome {curve['outcome']}"
        if curve["confirmation_arm"] is not None:
            detail += f"; confirmation_arm {curve['confirmation_arm']}"
        return f"SWEEP-CURVE-WRITTEN: {relative} ({detail})", EXIT_OK
    if args.command == "rescue":
        pre_answer, _protocol = _protocol_pre_answer(inputs)
        payload = _rescue(inputs, card, pre_answer)
        relative = inputs.relative(inputs.under_evidence("g2", RESCUE_NAME))
        return (
            f"RESCUE-WRITTEN: {relative} (outcome {payload['outcome']}; "
            f"pre-answer {payload['pre_answer']}; the stop path follows)",
            EXIT_OK,
        )
    if args.command == "skip":
        payload, relative = _write_skip(inputs, card, args.reason)
        return f"SKIP-RECORDS-WRITTEN: {relative} (reason {payload['reason']})", EXIT_OK
    payload, relative = _write_stop_handoff(inputs, card)
    return (
        f"STOP-HANDOFF-WRITTEN: {relative} (stop reason {payload['stop_reason']}; "
        f"total wall hours {payload['total_wall_hours']})",
        EXIT_OK,
    )


def main(argv=None):
    """Command line. The owner stops are handled here and only here: print, exit 3, never retry."""
    args = _build_parser().parse_args(argv)
    evidence_root = Path(args.evidence_root) if args.evidence_root else _REPO_ROOT / EVIDENCE_REL
    try:
        line, code = _run(args, evidence_root)
    except OwnerRouted as exc:
        print(f"OWNER-ROUTED: {exc}")
        return EXIT_OWNER
    except FailedConfirmationOwnerStop as exc:
        print(f"OWNER-ROUTED: {exc}")
        return EXIT_OWNER
    except G2Pending as exc:
        print(f"BRANCH-PENDING: {exc}")
        return EXIT_BRANCH_PENDING
    except G2Halt as exc:
        print(f"G2-HALT: {exc}")
        return EXIT_REFUSED
    print(line)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
