"""Phase 60 (FEAS-03/04/09): Gate G2, the sweep pair, skips and branch state.

After the three Rung-1 experiments a fixed rule decides what runs next. This module
turns that rule into small functions over files that are committed in git, so the
decision is mechanical, recorded once and the same every time.

What it does, in order:

* Gate G2 is the frozen ``g2_fires`` applied to the three committed Rung-1 result
  tiers, in the order of the panel (1632, 851, 4658). ``outcome`` writes the result.
* ``branch <name>`` is one read-only query that every later plan runs before it acts.
  It answers TAKEN, NOT-TAKEN or PENDING from the committed records alone.

Rules that govern every function here:

* The frozen scorecard functions are called, never re-implemented.
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
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pinn.verification import evidence_io
from pinn.verification.feasibility_scorecard import OwnerRouted, g2_fires, load_scorecard
from pinn.verification.learnability_arms import (
    EVIDENCE_REL,
    EXIT_OK,
    EXIT_OWNER,
    EXIT_REFUSED,
    PANEL_INNER_LAPS,
    PANEL_SYSTEMS,
    RUN_SCHEMA,
    FirstResultExists,
    arm_evidence_dir,
    write_record_exclusive,
)

__all__ = [
    "BRANCH_NAMES",
    "EXIT_BRANCH_PENDING",
    "G2_REL",
    "NOT_TAKEN",
    "OUTCOME_SCHEMA",
    "PENDING",
    "TAKEN",
    "BranchState",
    "G2Halt",
    "G2Pending",
    "Rung1Record",
    "UncommittedInput",
    "branch_state",
    "g2_outcome",
    "load_rung1_records",
    "main",
    "sweep_plan",
    "write_outcome",
]

_REPO_ROOT = Path(__file__).resolve().parents[2]

G2_REL = EVIDENCE_REL / "g2"
OUTCOME_NAME = "g2-outcome.json"
OUTCOME_SCHEMA = "phase60-g2-outcome/v1"
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


class G2Halt(RuntimeError):
    """A refused write or an inconsistent record. Nothing further runs on this path."""


class G2Pending(RuntimeError):
    """A deciding file is not recorded yet, so the question cannot be answered."""


class UncommittedInput(G2Halt):
    """A deciding file exists but is not tracked and clean in git."""

    def __init__(self, relative):
        super().__init__(f"uncommitted {relative}")
        self.relative = relative


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


# ---------------------------------------------------------------------------
# Committed inputs.
# ---------------------------------------------------------------------------

def _git(repo_root, *args):
    return subprocess.run(
        ["git", *args], cwd=str(repo_root), capture_output=True, text=True, check=False
    )


def _tracked_and_clean(repo_root, relative):
    """True when ``relative`` is tracked and has no change, staged or not (Phase 59 pattern)."""
    if _git(repo_root, "ls-files", "--error-unmatch", "--", relative).returncode != 0:
        return False
    status = _git(repo_root, "status", "--porcelain", "--", relative)
    return status.returncode == 0 and status.stdout.strip() == ""


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
        self._memo = {}

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
        if key in self._memo:
            return self._memo[key]
        if path.is_symlink():
            raise G2Halt(f"{self.relative(path)} is a symbolic link")
        relative = self.relative(path)
        if not path.exists():
            raise G2Pending(f"{relative} is not recorded")
        if not path.is_file():
            raise G2Halt(f"{relative} is not a regular file")
        if not _tracked_and_clean(self.repo_root, relative):
            raise UncommittedInput(relative)
        self._memo[key] = (path.read_bytes(), relative)
        return self._memo[key]

    def json(self, path):
        raw, relative = self.committed_bytes(path)
        try:
            payload = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise G2Halt(f"{relative} is not valid JSON") from exc
        if not isinstance(payload, dict):
            raise G2Halt(f"{relative} must hold a JSON object")
        return _Loaded(payload=payload, sha256=hashlib.sha256(raw).hexdigest(), path=relative)


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
# The branch query.
# ---------------------------------------------------------------------------

def _branch_sweep(inputs, card):
    outcome = _verified_outcome(inputs, card).payload
    if outcome["g2_fired"]:
        return BranchState("sweep", TAKEN, f"g2 fired; sweep system {outcome['sweep_system']}")
    return BranchState("sweep", NOT_TAKEN, "g2 did not fire")


def _branch_ladder(inputs, card):
    outcome = _verified_outcome(inputs, card).payload
    if outcome["g2_fired"]:
        raise G2Pending("g2 fired; the sweep has not decided the ladder yet")
    locked = float(card.section("gate_g2")["locked_value"])
    return BranchState(
        "ladder", TAKEN, f"g2 passed; first_omega_0 {locked}",
        first_omega_0=locked, omega_provenance="locked",
    )


def _branch_not_yet(inputs, card):
    _verified_outcome(inputs, card)
    raise G2Pending("this branch is decided from records a later step adds")


_BRANCH_RULES = {
    "sweep": _branch_sweep,
    "confirmation": _branch_not_yet,
    "owner-decision": _branch_not_yet,
    "stop": _branch_not_yet,
    "continue-gate": _branch_not_yet,
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
        description="Gate G2, the sweep pair, skip records and the branch query.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("outcome", help="write g2/g2-outcome.json once").add_argument(
        "--evidence-root", default=None
    )
    branch = commands.add_parser("branch", help="read-only: is a branch of the ladder taken?")
    branch.add_argument("name", choices=BRANCH_NAMES)
    branch.add_argument("--evidence-root", default=None)
    return parser


def _run(args, evidence_root):
    """Run one command; return ``(token line, exit code)``."""
    if args.command == "outcome":
        outcome, relative = _write_outcome(_Inputs(evidence_root), load_scorecard())
        tiers = " ".join(str(tier) for tier in outcome["tiers"])
        fired = "true" if outcome["g2_fired"] else "false"
        return f"G2-OUTCOME-WRITTEN: {relative} (g2_fired {fired}; tiers {tiers})", EXIT_OK
    state = branch_state(args.name, evidence_root=evidence_root)
    code = EXIT_BRANCH_PENDING if state.status == PENDING else EXIT_OK
    return f"BRANCH-{state.status}: {state.name} ({state.reason})", code


def main(argv=None):
    """Command line. ``OwnerRouted`` is handled here and only here: print, exit 3, never retry."""
    args = _build_parser().parse_args(argv)
    evidence_root = Path(args.evidence_root) if args.evidence_root else _REPO_ROOT / EVIDENCE_REL
    try:
        line, code = _run(args, evidence_root)
    except OwnerRouted as exc:
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
