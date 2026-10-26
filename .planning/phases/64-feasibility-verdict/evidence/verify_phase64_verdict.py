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

# The frozen check: the phase base every frozen byte must predate, the eight
# sealed files named here, the 33 pinned modules read from run-protocol.json at
# run time, and the four trees no Phase 64 change may touch. EXPECTED_PATHSPEC_COUNT
# is a literal, never derived from the lists it checks, so a dropped sealed file,
# a dropped tree or a short module map fails closed instead of shrinking the diff.
PHASE_BASE = "1ebb1d9b0c89e678961a8764bbf27ac19cd9b2a9"
P60_PROTOCOL_REL = P60_EVIDENCE_REL / "run-protocol.json"
P60_PROTOCOL_DOC_REL = Path(".planning/phases/60-single-system-learnability/60-RUN-PROTOCOL.md")
P59_FREEZE_REL = P59_EVIDENCE_REL / "scorecard-freeze.json"
P59_SCORECARD_REL = Path(".planning/phases/59-read-only-baseline-scorecard/59-SCORECARD.md")
SEALED_RELS = (
    P60_PROTOCOL_REL.as_posix(),
    P60_PROTOCOL_DOC_REL.as_posix(),
    (P60_EVIDENCE_REL / "g2" / "g2-outcome.json").as_posix(),
    (P60_EVIDENCE_REL / "g2" / "sweep-curve.json").as_posix(),
    (P60_EVIDENCE_REL / "g2" / "skip-records.json").as_posix(),
    (P60_EVIDENCE_REL / "g2" / "stop-handoff.json").as_posix(),
    P59_FREEZE_REL.as_posix(),
    P59_SCORECARD_REL.as_posix(),
)
FROZEN_TREES = (
    "pinn/",
    "pinn_instruction/markdown_conversion/framework-specs/",
    P59_EVIDENCE_REL.as_posix(),
    P60_EVIDENCE_REL.as_posix(),
)
EXPECTED_SEALED_COUNT = 8
EXPECTED_PINNED_COUNT = 33
EXPECTED_TREE_COUNT = 4
EXPECTED_PATHSPEC_COUNT = 45

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


def frozen_pathspecs(module_sha256: Any) -> list[str]:
    """The 45 git pathspecs of the frozen check, built in one place.

    The 8 sealed files and the 4 frozen trees are named here; the 33 pinned
    module paths come from run-protocol.json's ``module_sha256`` keys at run
    time, so no second copy of that list is committed. Each part and the whole
    list are checked against a literal count, so a dropped tree, a short module
    map or an empty entry fails closed rather than shrinking the git diff.
    """
    sealed = list(SEALED_RELS)
    pinned = list(module_sha256) if module_sha256 is not None else []
    trees = list(FROZEN_TREES)
    if len(sealed) != EXPECTED_SEALED_COUNT:
        fail(f"SEALED_RELS must hold exactly {EXPECTED_SEALED_COUNT} paths, not {len(sealed)}")
    if len(pinned) != EXPECTED_PINNED_COUNT:
        fail(
            "module_sha256 must hold exactly "
            f"{EXPECTED_PINNED_COUNT} paths, not {len(pinned)}"
        )
    if len(trees) != EXPECTED_TREE_COUNT:
        fail(f"FROZEN_TREES must hold exactly {EXPECTED_TREE_COUNT} trees, not {len(trees)}")
    pathspecs = sealed + pinned + trees
    if len(pathspecs) != EXPECTED_PATHSPEC_COUNT:
        fail(f"frozen pathspecs must number {EXPECTED_PATHSPEC_COUNT}, not {len(pathspecs)}")
    for entry in pathspecs:
        if not isinstance(entry, str) or not entry:
            fail(f"frozen pathspec is not a non-empty string: {entry!r}")
        if entry != entry.strip():
            fail(f"frozen pathspec has surrounding whitespace: {entry!r}")
    if len(set(pathspecs)) != len(pathspecs):
        duplicates = sorted({entry for entry in pathspecs if pathspecs.count(entry) > 1})
        fail(f"frozen pathspecs hold duplicates: {duplicates!r}")
    return pathspecs


def cmd_frozen(_args: argparse.Namespace) -> None:
    """The 33 pinned modules, the 8 sealed files and the 4 frozen trees, unchanged."""
    protocol_file = repo_path(P60_PROTOCOL_REL, what="run-protocol.json")
    if not protocol_file.is_file():
        fail(f"run-protocol.json is missing: {P60_PROTOCOL_REL.as_posix()}")
    protocol = load_json(protocol_file, what="run-protocol.json")
    if not isinstance(protocol, Mapping):
        fail("run-protocol.json is not an object")
    module_sha256 = protocol.get("module_sha256")
    if not isinstance(module_sha256, Mapping):
        fail("run-protocol.json module_sha256 is not a mapping")
    if len(module_sha256) != EXPECTED_PINNED_COUNT:
        fail(
            "run-protocol.json module_sha256 must hold exactly "
            f"{EXPECTED_PINNED_COUNT} paths, not {len(module_sha256)}"
        )

    for mod_rel in module_sha256:
        pinned = module_sha256[mod_rel]
        if not isinstance(mod_rel, str) or not mod_rel:
            fail(f"run-protocol.json module_sha256 holds a non-string key: {mod_rel!r}")
        if not isinstance(pinned, str) or HEX64.match(pinned) is None:
            fail(f"pinned module {mod_rel} has no 64-hex sha256")
        mod_path = repo_path(mod_rel, what=f"pinned module {mod_rel}")
        if not mod_path.is_file():
            fail(f"pinned module {mod_rel} does not exist")
        if not is_tracked(mod_rel) or not is_clean(mod_rel):
            fail(f"pinned module {mod_rel} is not tracked and clean")
        mod_disk_sha = sha256_file(mod_path)
        if mod_disk_sha != pinned:
            fail(f"pinned module {mod_rel} SHA-256 {mod_disk_sha} != pinned {pinned}")

    head = _git("rev-parse", "HEAD")
    if head.returncode != 0 or not head.stdout.strip():
        fail(f"cannot resolve HEAD: {head.stderr.strip()}")
    head_sha = head.stdout.strip()
    if not is_ancestor(PHASE_BASE, head_sha):
        fail(f"the phase base {PHASE_BASE} is not an ancestor of HEAD {head_sha}")

    pathspecs = frozen_pathspecs(module_sha256)

    # One list spread into separate argv items after '--' (never a shell string,
    # so no word-splitting can collapse 45 pathspecs into one that matches
    # nothing). The diff covers committed changes since the phase base; the
    # status call covers uncommitted edits and untracked files.
    diff = _git("diff", "--quiet", PHASE_BASE, head_sha, "--", *pathspecs)
    if diff.returncode != 0:
        changed = _git("diff", "--name-only", PHASE_BASE, head_sha, "--", *pathspecs)
        first = changed.stdout.splitlines()[0] if changed.stdout.strip() else "<unknown>"
        fail(
            f"a sealed, pinned or frozen path changed since the phase base {PHASE_BASE}: "
            f"{first}"
        )

    status = _git("status", "--porcelain", "--untracked-files=all", "--", *pathspecs)
    if status.returncode != 0:
        fail(f"git status failed: {status.stderr.strip()}")
    if status.stdout.strip():
        first = status.stdout.splitlines()[0]
        fail(f"an uncommitted or untracked change sits in a frozen path: {first}")

    print(
        f"frozen paths pinned={EXPECTED_PINNED_COUNT} "
        f"sealed={len(SEALED_RELS)} trees={len(FROZEN_TREES)}"
    )
    print("FROZEN-OK")


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
    "frozen": cmd_frozen,
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
