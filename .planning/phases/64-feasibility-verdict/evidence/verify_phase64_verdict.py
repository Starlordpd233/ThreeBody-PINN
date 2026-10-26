#!/usr/bin/env python3
"""Phase 64: fail-closed verifier for the feasibility verdict, the charter and traceability.

Independent, fail-closed verification of the Phase 64 feasibility verdict. Every
mode reads committed files and re-derives what it checks; no number is typed by
hand and no pre-registered output is rewritten. Each mode prints one success
token on its own line and raises ``VerifyError`` (printed to stderr, exit 1) on
any deviation.

``torch`` and ``pinn`` are imported inside the mode that needs them, never at
module scope, so the committed-JSON modes run in about a tenth of a second with
no data root and no accelerator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

REPO_ROOT = Path(__file__).resolve().parents[4]
HEX64 = re.compile(r"^[0-9a-f]{64}$")

PHASE_REL = Path(".planning/phases/64-feasibility-verdict")
EVIDENCE_REL = PHASE_REL / "evidence"
P60_EVIDENCE_REL = Path(".planning/phases/60-single-system-learnability/evidence")
P59_EVIDENCE_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence")
HANDOFF_REL = P60_EVIDENCE_REL / "g2" / "stop-handoff.json"
HANDOFF_SHA256 = "7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5"
HANDOFF_SCHEMA = "phase60-stop-handoff/v1"

# The seven arms the ladder actually ran, in handoff order. The four later-arm
# families and the two probe arms never ran: Gate G2 fired and the sweep
# rescued nothing, so Phases 61 to 63 were skipped, not failed.
EXPECTED_ARMS = (
    "r1-1632",
    "r1-851",
    "r1-4658",
    "g2s-1632-w060",
    "g2s-1632-w120",
    "g2s-1632-w240",
    "g2s-1632-w480",
)
RUNG1_ARMS = ("r1-1632", "r1-851", "r1-4658")
FORBIDDEN_ARM_PREFIXES = (
    "r2a-",
    "r2b-",
    "c-r1u-",
    "c-r2a-",
    "c-r2b-",
    "p1-",
    "p2b-",
    "c-p1-",
    "c-p2b-",
)


class VerifyError(RuntimeError):
    """Fail-closed evidence verification error."""


def fail(message: str) -> None:
    raise VerifyError(f"verify_phase64_verdict FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def ordered_sum(values: Any) -> float:
    """Left-to-right float sum, starting at ``0.0``, in the order given.

    Builtin ``sum()`` is not interpreter-neutral: CPython 3.12 changed float
    ``sum()`` to compensated summation, which on the seven Phase 60 wall-hour
    values returns one ulp below the stored total. ``math.fsum`` and any sorted
    order disagree with the sealed total too. This helper is the one summation
    the verifier compares exactly, so a comparison that must hold on every
    interpreter goes through it.
    """
    total = 0.0
    for value in values:
        total += value
    return total


def _field(payload: Any, dotted: str) -> Any:
    current = payload
    for part in dotted.split("."):
        if not isinstance(current, Mapping) or part not in current:
            fail(f"missing field {dotted}")
        current = current[part]
    return current


def _check_citation(entry: Any, *, what: str) -> str:
    """Resolve one ``{path, sha256}`` citation and return its repository path."""
    if not isinstance(entry, Mapping):
        fail(f"{what} is not an object")
    raw = entry.get("path")
    cited = entry.get("sha256")
    if not isinstance(raw, str) or not raw:
        fail(f"{what} has no path")
    if not isinstance(cited, str) or HEX64.match(cited) is None:
        fail(f"{what} has no 64-hex sha256")
    path = repo_path(raw, what=what)
    if not path.is_file():
        fail(f"{what} does not exist: {raw}")
    if not is_tracked(raw) or not is_clean(raw):
        fail(f"{what} is not tracked and clean: {raw}")
    disk = sha256_file(path)
    if disk != cited:
        fail(f"{what} SHA-256 {disk} != cited {cited}")
    return raw


def _check_handoff() -> dict[str, Any]:
    """The sealed handoff: pinned bytes, sealed fields and all nine citations."""
    handoff_file = repo_path(HANDOFF_REL, what="stop-handoff.json")
    if not handoff_file.is_file():
        fail(f"stop-handoff.json is missing: {HANDOFF_REL.as_posix()}")
    if not is_tracked(HANDOFF_REL.as_posix()) or not is_clean(HANDOFF_REL.as_posix()):
        fail(f"stop-handoff.json is not tracked and clean: {HANDOFF_REL.as_posix()}")
    disk = sha256_file(handoff_file)
    if disk != HANDOFF_SHA256:
        fail(f"stop-handoff.json SHA-256 {disk} != sealed {HANDOFF_SHA256}")

    handoff = load_json(handoff_file, what="stop-handoff.json")
    if not isinstance(handoff, Mapping):
        fail("stop-handoff.json is not an object")
    if handoff.get("schema") != HANDOFF_SCHEMA:
        fail(f"stop-handoff.json schema {handoff.get('schema')!r} != {HANDOFF_SCHEMA!r}")
    # Sealed by design: the owner's answer and the verdict note stay empty, so
    # the label cannot be amended after the fact (D-01, SCOPE-42, SCOPE-43).
    if handoff.get("owner_answer") is not None:
        fail(f"stop-handoff.json owner_answer is not null: {handoff.get('owner_answer')!r}")
    if handoff.get("verdict_note") is not None:
        fail(f"stop-handoff.json verdict_note is not null: {handoff.get('verdict_note')!r}")
    if handoff.get("level3") != "not tested (skipped at G2)":
        fail(f"stop-handoff.json level3 {handoff.get('level3')!r} != 'not tested (skipped at G2)'")
    if handoff.get("phases_61_63") != "skipped at G2, not failed":
        fail(
            "stop-handoff.json phases_61_63 "
            f"{handoff.get('phases_61_63')!r} != 'skipped at G2, not failed'"
        )
    if handoff.get("stop_reason") != "no rescue":
        fail(f"stop-handoff.json stop_reason {handoff.get('stop_reason')!r} != 'no rescue'")
    if handoff.get("next_phase") != 64:
        fail(f"stop-handoff.json next_phase {handoff.get('next_phase')!r} != 64")

    basis = handoff.get("basis")
    if not isinstance(basis, list) or len(basis) != 2:
        fail("stop-handoff.json basis must hold exactly two citations")
    for index, entry in enumerate(basis):
        _check_citation(entry, what=f"stop-handoff.json basis[{index}]")

    arms = handoff.get("arms")
    if not isinstance(arms, list) or len(arms) != len(EXPECTED_ARMS):
        fail(f"stop-handoff.json must hold exactly {len(EXPECTED_ARMS)} arms")
    arm_ids = tuple(entry.get("arm_id") for entry in arms if isinstance(entry, Mapping))
    if arm_ids != EXPECTED_ARMS:
        fail(f"stop-handoff.json arms {arm_ids!r} != {EXPECTED_ARMS!r}")
    for index, entry in enumerate(arms):
        _check_citation(entry.get("record"), what=f"stop-handoff.json arms[{index}].record")

    total = ordered_sum(
        _field(entry, "wall_hours") for entry in arms
    )
    stored_total = handoff.get("total_wall_hours")
    if not isinstance(stored_total, (int, float)) or isinstance(stored_total, bool):
        fail("stop-handoff.json total_wall_hours is not a number")
    if total != stored_total:
        fail(
            "stop-handoff.json wall_hours do not sum to total_wall_hours: "
            f"ordered_sum {total!r} != stored {stored_total!r}"
        )
    return handoff


def _check_rungs_that_did_not_run() -> None:
    """Exactly the seven arm directories; nothing from a later rung exists."""
    arms_dir = repo_path(P60_EVIDENCE_REL / "arms", what="phase 60 arms directory")
    if not arms_dir.is_dir():
        fail(f"phase 60 arms directory is missing: {(P60_EVIDENCE_REL / 'arms').as_posix()}")
    for entry in sorted(arms_dir.iterdir()):
        if any(entry.name.startswith(prefix) for prefix in FORBIDDEN_ARM_PREFIXES):
            fail(f"a later-rung arm directory exists: {entry.name}")
    present = tuple(sorted(entry.name for entry in arms_dir.iterdir()))
    if present != tuple(sorted(EXPECTED_ARMS)):
        fail(f"phase 60 arms directory holds {present!r} != {tuple(sorted(EXPECTED_ARMS))!r}")

    continue_dir = repo_path(P60_EVIDENCE_REL / "continue", what="phase 60 continue directory")
    if continue_dir.exists():
        fail(f"a continue/ directory exists: {(P60_EVIDENCE_REL / 'continue').as_posix()}")

    evidence_dir = repo_path(P60_EVIDENCE_REL, what="phase 60 evidence directory")
    for rescue in sorted(evidence_dir.rglob("rescue.json")):
        # REPO_ROOT may be an unresolved alias of the resolved directory (a
        # temporary path under /var resolves through /private/var), so build the
        # repo-relative name from the constant rather than from REPO_ROOT.
        named = (P60_EVIDENCE_REL / rescue.relative_to(evidence_dir)).as_posix()
        fail(f"a rescue record exists: {named}")

    ruling = repo_path(
        P60_EVIDENCE_REL.parent / "60-CHECKPOINT-4-RULING.md",
        what="checkpoint four ruling",
    )
    if ruling.exists():
        fail("a 60-CHECKPOINT-4-RULING.md exists: checkpoint four was answered")


def _check_g2_records() -> tuple[tuple[int, ...], dict[str, Any]]:
    """The G2 outcome, the sweep outcome and the skip records."""
    outcome_file = repo_path(P60_EVIDENCE_REL / "g2" / "g2-outcome.json", what="g2-outcome.json")
    if not outcome_file.is_file():
        fail("g2-outcome.json is missing")
    outcome = load_json(outcome_file, what="g2-outcome.json")
    if not isinstance(outcome, Mapping):
        fail("g2-outcome.json is not an object")
    if outcome.get("schema") != "phase60-g2-outcome/v1":
        fail(f"g2-outcome.json schema {outcome.get('schema')!r} != 'phase60-g2-outcome/v1'")

    panel = tuple(int(arm.split("-")[1]) for arm in RUNG1_ARMS)
    recorded_panel = outcome.get("panel_systems")
    if not isinstance(recorded_panel, list) or tuple(recorded_panel) != panel:
        fail(f"g2-outcome.json panel_systems {recorded_panel!r} != {list(panel)!r}")

    tiers = []
    for arm_id in RUNG1_ARMS:
        record_file = repo_path(
            P60_EVIDENCE_REL / "arms" / arm_id / "record.json",
            what=f"Rung 1 record {arm_id}",
        )
        if not record_file.is_file():
            fail(f"Rung 1 record is missing: {arm_id}")
        record = load_json(record_file, what=f"Rung 1 record {arm_id}")
        tier = _field(record, "result.tier")
        if not isinstance(tier, int) or isinstance(tier, bool):
            fail(f"Rung 1 record {arm_id} result.tier is not an integer")
        tiers.append(tier)
    tier_tuple = tuple(tiers)
    recorded_tiers = outcome.get("tiers")
    if not isinstance(recorded_tiers, list) or tuple(recorded_tiers) != tier_tuple:
        fail(f"g2-outcome.json tiers {recorded_tiers!r} != recomputed {list(tier_tuple)!r}")
    if outcome.get("g2_fired") is not True:
        fail(f"g2-outcome.json g2_fired {outcome.get('g2_fired')!r} is not true")

    curve_file = repo_path(P60_EVIDENCE_REL / "g2" / "sweep-curve.json", what="sweep-curve.json")
    if not curve_file.is_file():
        fail("sweep-curve.json is missing")
    curve = load_json(curve_file, what="sweep-curve.json")
    if not isinstance(curve, Mapping):
        fail("sweep-curve.json is not an object")
    if curve.get("schema") != "phase60-sweep-curve/v1":
        fail(f"sweep-curve.json schema {curve.get('schema')!r} != 'phase60-sweep-curve/v1'")
    if curve.get("outcome") != "no_rescue":
        fail(f"sweep-curve.json outcome {curve.get('outcome')!r} != 'no_rescue'")

    skip_file = repo_path(P60_EVIDENCE_REL / "g2" / "skip-records.json", what="skip-records.json")
    if not skip_file.is_file():
        fail("skip-records.json is missing")
    skip = load_json(skip_file, what="skip-records.json")
    if not isinstance(skip, Mapping):
        fail("skip-records.json is not an object")
    if skip.get("schema") != "phase60-skip-records/v1":
        fail(f"skip-records.json schema {skip.get('schema')!r} != 'phase60-skip-records/v1'")
    entries = skip.get("entries")
    if not isinstance(entries, Mapping):
        fail("skip-records.json entries is not an object")
    for requirement in ("FEAS-04", "FEAS-09"):
        entry = entries.get(requirement)
        if not isinstance(entry, Mapping):
            fail(f"skip-records.json has no entry for {requirement}")
        if entry.get("skipped") is not True:
            fail(f"skip-records.json {requirement} is not recorded as skipped")
        if entry.get("reason") != "no rescue":
            fail(f"skip-records.json {requirement} reason {entry.get('reason')!r} != 'no rescue'")
    return tier_tuple, curve


def cmd_inputs(_args: argparse.Namespace) -> None:
    """The sealed handoff, its nine citations and the label re-derived by the rule."""
    handoff = _check_handoff()
    _check_rungs_that_did_not_run()
    tiers, curve = _check_g2_records()

    try:
        from pinn.verification.feasibility_scorecard import (
            decision_verdict,
            g2_fires,
            load_scorecard,
        )
    except Exception as exc:  # noqa: BLE001 - fail-closed CLI
        fail(f"cannot import the frozen decision rule: {exc}")

    card = load_scorecard()
    g2_fired = g2_fires(list(tiers), scorecard=card)
    if g2_fired is not True:
        fail(f"the frozen rule does not fire G2 on the recomputed tiers {list(tiers)!r}")
    sweep_rescued = curve["outcome"] != "no_rescue"
    expected = decision_verdict(
        g2_fired=g2_fired,
        sweep_rescued=sweep_rescued,
        rung2b_counts=None,
        rung3_counts=None,
        control_branch=None,
        rung1_beats_formula=None,
        scorecard=card,
    )
    recorded = handoff.get("verdict")
    if recorded != expected:
        fail(f"stop-handoff.json verdict {recorded!r} != re-derived {expected!r}")
    print("INPUTS-OK")


COMMANDS = {
    "inputs": cmd_inputs,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=tuple(COMMANDS))
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
