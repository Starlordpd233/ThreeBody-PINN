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
import math
import re
import subprocess
import sys
from decimal import Decimal
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

# The number manifest (64-02). The verifier carries its own copy of the
# rendering rules, its own id-to-key table, its own formulas and its own cited
# tokens: it never imports the producer and never trusts the producer's code.
NUMBERS_REL = EVIDENCE_REL / "numbers.json"
NUMBERS_SCHEMA = "phase64-numbers/v1"
P60_ARMS_REL = P60_EVIDENCE_REL / "arms"
SCORECARD_ARTIFACT_REL = Path("pinn/verification/artifacts/feasibility_scorecard_v1.json")
RESEARCH_REL = PHASE_REL / "64-RESEARCH.md"
RESEARCH_COMMIT = "7fda0a55fc84447ea17abbb4d1188761add94d8a"
PRODUCER_REL = (EVIDENCE_REL / "build_phase64_evidence.py").as_posix()
NUMBERS_LABELS = (
    "official-mps-float32",
    "rederived-cpu-float64",
    "committed-record",
    "arithmetic",
    "cited",
)
NUMBERS_RULES = (
    "E4",
    "F0",
    "F1",
    "F2",
    "F3",
    "F5",
    "F6",
    "INT",
    "EPS",
    "POW10",
    "SCI2",
    "PCT0",
    "OFN",
    "STR",
    "BOOL",
    "LIT",
)
ENTRY_KEYS = frozenset(
    {
        "id",
        "value",
        "render",
        "render_rule",
        "label",
        "source",
        "derivation",
        "required_in",
    }
)
CPU_ENTRY = re.compile(
    r"^cpu\.(?P<arm>[a-z0-9-]+)\.(?P<state>adam|polish)\.(?P<field>[A-Za-z0-9_]+)$"
)
CPU_CONST = re.compile(r"^cpu\.const\.(?P<system>\d+)\.E$")
CPU_SYSTEMS = ("1632", "851", "4658")
CPU_STATES = ("adam", "polish")
CPU_FIELDS = frozenset(
    {
        "E",
        "e_sys_t0",
        "e_in_t0",
        "best_moment",
        "n_within_tier1",
        "n_times",
        "timevar_ratio",
        "rms_ratio",
    }
)

# The figure (64-03). The verifier re-derives the plotted series with its own
# code, compares the series digest, regenerates the SVG bytes from that series
# and parses the committed document for out-of-canvas text, script elements and
# external references.
FIGURE_REL = EVIDENCE_REL / "figure-1632.svg"
FIGURE_PROVENANCE_REL = EVIDENCE_REL / "figure-1632.provenance.json"
FIGURE_PRODUCER_REL = EVIDENCE_REL / "build_phase64_figure.py"
FIGURE_SCHEMA = "phase64-figure-provenance/v1"
FIGURE_ARM = "r1-1632"
FIGURE_STATE = "polish"
FIGURE_PRECISION = "CPU float64"
FIGURE_GROUPS = ("panel-a",)
FIGURE_INPUTS = (
    (P60_EVIDENCE_REL / "arms" / FIGURE_ARM / "record.json").as_posix(),
    (P60_EVIDENCE_REL / "arms" / FIGURE_ARM / f"{FIGURE_STATE}.weights").as_posix(),
    HANDOFF_REL.as_posix(),
    SCORECARD_ARTIFACT_REL.as_posix(),
)
FIGURE_PRODUCERS = (FIGURE_PRODUCER_REL.as_posix(), PRODUCER_REL)


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
    """Walk a dotted key path; a numeric part indexes a list (``trace.0.E``)."""
    current = payload
    for part in dotted.split("."):
        if isinstance(current, (list, tuple)) and part.isdigit():
            index = int(part)
            if index >= len(current):
                fail(f"missing field {dotted}")
            current = current[index]
            continue
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


REQUIREMENTS_REL = Path(".planning/REQUIREMENTS.md")
ROADMAP_REL = Path(".planning/ROADMAP.md")
PROJECT_REL = Path(".planning/PROJECT.md")
TRACEABLE_PHASES = (59, 60, 61, 62, 63, 64)
REQUIREMENT_ID = re.compile(r"[A-Z]+-\d+")
DEFINITION_LINE = re.compile(r"^- \[[ xX]\] \*\*([A-Z]+-\d+)\*\*", re.M)
TABLE_ROW = re.compile(r"^\| ([A-Z]+-\d+) \| Phase (\d+) \| (.+?) \|$", re.M)
PHASE_HEADING = re.compile(r"^### Phase (\d+):", re.M)
REQUIREMENTS_LINE = re.compile(r"^\*\*Requirements\*\*:[ \t]*(.*)$", re.M)


def _read_text(relative: Path, *, what: str) -> str:
    path = repo_path(relative, what=what)
    if not path.is_file():
        fail(f"{what} is missing: {relative.as_posix()}")
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"{what} is unreadable: {path}: {exc}")


def _one_count(pattern: str, text: str, *, what: str) -> int:
    matches = re.findall(pattern, text, re.M)
    if len(matches) != 1:
        fail(f"{what} must appear exactly once, found {len(matches)}")
    return int(matches[0])


def _one_ratio(pattern: str, text: str, *, what: str) -> tuple[int, int]:
    matches = re.findall(pattern, text, re.M)
    if len(matches) != 1:
        fail(f"{what} must appear exactly once, found {len(matches)}")
    left, right = matches[0]
    return int(left), int(right)


def _slice_between(text: str, start_pattern: str, end_pattern: str, *, what: str) -> str:
    starts = list(re.finditer(start_pattern, text, re.M))
    if len(starts) != 1:
        fail(f"{what} must appear exactly once, found {len(starts)}")
    ends = list(re.finditer(end_pattern, text, re.M))
    if len(ends) != 1:
        fail(f"{what} end must appear exactly once, found {len(ends)}")
    if ends[0].start() <= starts[0].start():
        fail(f"{what} end appears before its start")
    return text[starts[0].start() : ends[0].start()]


def traceability_report(
    requirements_text: str, roadmap_text: str, project_text: str
) -> dict[str, Any]:
    """Recount VER-22 from the current registry text: 24 IDs, one phase each.

    Every count is an exact integer parsed from digits and compared with ``==``.
    IDs are whole words compared as exact strings (FEAS-01 and FEAS-10 differ),
    and the creation-time "20/20" history lines match no pattern here, so they
    are never read as the current count.
    """
    requirements_block = _slice_between(
        requirements_text,
        r"^## v2\.4 Requirements$",
        r"^## Scope Boundaries",
        what="REQUIREMENTS.md v2.4 Requirements section",
    )
    defined = DEFINITION_LINE.findall(requirements_block)
    if not defined:
        fail("REQUIREMENTS.md defines no requirement")
    duplicates = sorted({entry for entry in defined if defined.count(entry) > 1})
    if duplicates:
        fail(f"REQUIREMENTS.md defines a requirement twice: {duplicates!r}")

    table_block = _slice_between(
        requirements_text,
        r"^## Traceability$",
        r"^---$",
        what="REQUIREMENTS.md Traceability section",
    )
    rows = TABLE_ROW.findall(table_block)
    if not rows:
        fail("REQUIREMENTS.md Traceability table has no row")
    table_phase: dict[str, int] = {}
    statuses: dict[str, int] = {}
    for requirement, phase_text, status in rows:
        if requirement in table_phase:
            fail(f"REQUIREMENTS.md Traceability table holds {requirement} twice")
        phase = int(phase_text)
        if phase not in TRACEABLE_PHASES:
            fail(f"{requirement} is mapped to Phase {phase}, outside 59 to 64")
        table_phase[requirement] = phase
        statuses[status] = statuses.get(status, 0) + 1

    headings = list(PHASE_HEADING.finditer(roadmap_text))
    sections: dict[int, str] = {}
    for index, heading in enumerate(headings):
        phase = int(heading.group(1))
        end = headings[index + 1].start() if index + 1 < len(headings) else len(roadmap_text)
        if phase in sections:
            fail(f"ROADMAP.md holds two '### Phase {phase}' sections")
        sections[phase] = roadmap_text[heading.start() : end]

    roadmap_phase: dict[str, int] = {}
    per_phase: dict[int, list[str]] = {}
    for phase in TRACEABLE_PHASES:
        if phase not in sections:
            fail(f"ROADMAP.md has no '### Phase {phase}' section")
        matches = REQUIREMENTS_LINE.findall(sections[phase])
        if len(matches) != 1:
            fail(
                f"ROADMAP.md Phase {phase} must hold exactly one **Requirements**: line, "
                f"found {len(matches)}"
            )
        identifiers = REQUIREMENT_ID.findall(matches[0])
        if not identifiers:
            fail(f"ROADMAP.md Phase {phase} **Requirements**: line lists no requirement ID")
        per_phase[phase] = sorted(identifiers)
        for requirement in identifiers:
            if requirement in roadmap_phase:
                fail(
                    f"ROADMAP.md maps {requirement} to Phase {roadmap_phase[requirement]} "
                    f"and Phase {phase}"
                )
            roadmap_phase[requirement] = phase

    defined_set = set(defined)
    if defined_set != set(table_phase):
        missing = sorted(defined_set - set(table_phase))
        extra = sorted(set(table_phase) - defined_set)
        fail(
            "REQUIREMENTS.md definitions and Traceability table disagree: "
            f"missing from table {missing!r}, not defined {extra!r}"
        )
    if defined_set != set(roadmap_phase):
        missing = sorted(defined_set - set(roadmap_phase))
        extra = sorted(set(roadmap_phase) - defined_set)
        fail(
            "REQUIREMENTS.md definitions and ROADMAP.md Requirements lines disagree: "
            f"missing from roadmap {missing!r}, not defined {extra!r}"
        )
    for requirement in sorted(defined_set):
        if table_phase[requirement] != roadmap_phase[requirement]:
            fail(
                f"{requirement} table phase {table_phase[requirement]} != "
                f"roadmap phase {roadmap_phase[requirement]}"
            )

    count = len(defined)
    stated = {
        "REQUIREMENTS.md **Total:**": _one_count(
            r"^\*\*Total:\*\* (\d+) requirements",
            requirements_text,
            what="REQUIREMENTS.md **Total:** line",
        ),
        "REQUIREMENTS.md v2.4 requirements": _one_count(
            r"^- v2\.4 requirements: (\d+) total$",
            requirements_text,
            what="REQUIREMENTS.md v2.4 requirements line",
        ),
        "REQUIREMENTS.md Mapped to phases": _one_count(
            r"^- Mapped to phases: (\d+)$",
            requirements_text,
            what="REQUIREMENTS.md Mapped to phases line",
        ),
        "ROADMAP.md requirements (FEAS-01..10": _one_count(
            r"(\d+) requirements \(FEAS-01\.\.10",
            roadmap_text,
            what="ROADMAP.md requirements (FEAS-01..10 line",
        ),
        "ROADMAP.md 6 phases": _one_count(
            r"6 phases, (\d+) requirements",
            roadmap_text,
            what="ROADMAP.md 6 phases line",
        ),
        "PROJECT.md requirements": _one_count(
            r"^- \*\*(\d+) requirements\.\*\*$",
            project_text,
            what="PROJECT.md requirements line",
        ),
    }
    for what, value in stated.items():
        if value != count:
            fail(f"{what} states {value} != {count} defined")
    unmapped = _one_count(
        r"^- Unmapped: (\d+)",
        requirements_text,
        what="REQUIREMENTS.md Unmapped line",
    )
    if unmapped != 0:
        fail(f"REQUIREMENTS.md Unmapped states {unmapped} != 0")
    for what, pattern in (
        (
            "ROADMAP.md N/N after the 2026-10-11 amendment",
            r"(\d+)/(\d+) after the 2026-10-11 amendment",
        ),
        ("ROADMAP.md N/N mapped.", r"(\d+)/(\d+) mapped\."),
    ):
        left, right = _one_ratio(pattern, roadmap_text, what=what)
        if left != count or right != count:
            fail(f"{what} states {left}/{right} != {count}/{count}")

    return {
        "defined": sorted(defined),
        "table": sorted(table_phase),
        "roadmap": sorted(roadmap_phase),
        "per_phase": {phase: per_phase[phase] for phase in TRACEABLE_PHASES},
        "statuses": statuses,
    }


def cmd_traceability(_args: argparse.Namespace) -> None:
    """VER-22: definitions, table and roadmap agree on 24 IDs, one phase each."""
    report = traceability_report(
        _read_text(REQUIREMENTS_REL, what="REQUIREMENTS.md"),
        _read_text(ROADMAP_REL, what="ROADMAP.md"),
        _read_text(PROJECT_REL, what="PROJECT.md"),
    )
    print(f"defined {len(report['defined'])}")
    print(f"table {len(report['table'])}")
    print(f"roadmap {len(report['roadmap'])}")
    counts = " ".join(
        f"{phase}:{len(report['per_phase'][phase])}" for phase in TRACEABLE_PHASES
    )
    print(f"per-phase {counts}")
    for label in sorted(report["statuses"]):
        print(f"status {label} {report['statuses'][label]}")
    print("TRACEABILITY-OK")


# ---------------------------------------------------------------------------
# The number manifest: the verifier's own rendering, tables and checks
# ---------------------------------------------------------------------------

_SUPERSCRIPT = {
    "0": "\u2070",
    "1": "\u00b9",
    "2": "\u00b2",
    "3": "\u00b3",
    "4": "\u2074",
    "5": "\u2075",
    "6": "\u2076",
    "7": "\u2077",
    "8": "\u2078",
    "9": "\u2079",
    "-": "\u207b",
}


def _real(value: Any, rule: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(f"render rule {rule} needs a real number, got {value!r}")
    number = float(value)
    if not math.isfinite(number):
        fail(f"render rule {rule} needs a finite number, got {value!r}")
    return number


def _superscript(exponent: int) -> str:
    try:
        return "".join(_SUPERSCRIPT[character] for character in str(int(exponent)))
    except KeyError as exc:  # pragma: no cover - the table covers every digit and '-'
        fail(f"cannot render the exponent {exponent!r}: {exc}")


def _power_of_ten(value: Any) -> int:
    number = _real(value, "POW10")
    if number <= 0.0:
        fail(f"render rule POW10 needs a positive number, got {value!r}")
    exponent = int(round(math.log10(number)))
    if Decimal(repr(number)) != Decimal(10) ** exponent:
        fail(f"render rule POW10 needs an exact power of ten, got {value!r}")
    return exponent


def render_number(value: Any, rule: str) -> str:
    """The verifier's own copy of the rendering rule, applied to the IEEE double."""
    if rule == "E4":
        return f"{_real(value, rule):.4f}"
    if rule in {"F0", "F1", "F2", "F3", "F5", "F6"}:
        return f"{_real(value, rule):.{int(rule[1:])}f}"
    if rule == "INT":
        if isinstance(value, bool) or not isinstance(value, int):
            fail(f"render rule INT needs an int, got {value!r}")
        return f"{value:,}"
    if rule == "EPS":
        number = _real(value, rule)
        return f"{number:.2f}" if number < 1000.0 else f"{number:,.1f}"
    if rule == "POW10":
        return f"10{_superscript(_power_of_ten(value))}"
    if rule == "SCI2":
        number = _real(value, rule)
        if number <= 0.0:
            fail(f"render rule SCI2 needs a positive number, got {value!r}")
        exponent = int(math.floor(math.log10(number)))
        mantissa = number / (10.0**exponent)
        if round(mantissa, 2) >= 10.0:
            exponent += 1
            mantissa = number / (10.0**exponent)
        return f"{mantissa:.2f} \u00d7 10{_superscript(exponent)}"
    if rule == "PCT0":
        return f"{_real(value, rule) * 100.0:.0f}%"
    if rule == "OFN":
        if (
            not isinstance(value, (list, tuple))
            or len(value) != 2
            or isinstance(value[0], bool)
            or isinstance(value[1], bool)
            or not isinstance(value[0], int)
            or not isinstance(value[1], int)
        ):
            fail(f"render rule OFN needs [count, total] as two ints, got {value!r}")
        return f"{value[0]} of {value[1]}"
    if rule == "STR":
        if not isinstance(value, str):
            fail(f"render rule STR needs a string, got {value!r}")
        return value
    if rule == "BOOL":
        if not isinstance(value, bool):
            fail(f"render rule BOOL needs a bool, got {value!r}")
        return "true" if value else "false"
    if rule == "LIT":
        if not isinstance(value, str):
            fail(f"render rule LIT needs a literal string, got {value!r}")
        return value
    fail(f"unknown render rule {rule!r}")


def _record_rel(arm_id: str) -> str:
    return (P60_ARMS_REL / arm_id / "record.json").as_posix()


def _weights_rel(arm_id: str, state: str) -> str:
    return (P60_ARMS_REL / arm_id / f"{state}.weights").as_posix()


def _load_json_rel(relative: str, *, what: str) -> Any:
    return load_json(repo_path(relative, what=what), what=what)


def _load_record(arm_id: str) -> Mapping[str, Any]:
    record = _load_json_rel(_record_rel(arm_id), what=f"record {arm_id}")
    if not isinstance(record, Mapping):
        fail(f"record {arm_id} is not an object")
    return record


SWEEP_ARMS = (
    "g2s-1632-w060",
    "g2s-1632-w120",
    "g2s-1632-w240",
    "g2s-1632-w480",
)
BASELINES_REL = P59_EVIDENCE_REL / "baselines" / "baselines.json"
SURVEY_REL = P59_EVIDENCE_REL / "survey" / "survey.json"
PICKS_REL = P59_EVIDENCE_REL / "survey" / "picks.json"
CENSUS_REL = P59_EVIDENCE_REL / "census" / "census.json"
GAPS_REL = P59_EVIDENCE_REL.parent / "59-GAPS.md"
STATUS_REL = Path("runs/stage0-v23g7-seed42/status.json")
PROJECT_REL = Path(".planning/PROJECT.md")
AMENDMENTS_REL = Path(
    "docs/work/designs/cross_cutting/v2.4-milestone-proposal/"
    "2026-10-11-v2.4-feasibility-amendments.md"
)
GAPS_COMMIT = "ec2853b0f445d28ac462afd7cc4d395961934da7"
PROJECT_COMMIT = "bb323a52a7eab24e401d3bdc903a5e01528fcbc0"
AMENDMENTS_COMMIT = "e72060daf0de7b31334ccb7fddf8876d8506c27f"

# The illustration sizes the for-scale and example arithmetic re-applies. The
# cited entries carry the same integers from their pinned documents.
FORSCALE_STEPS_LOW = 200000
FORSCALE_STEPS_HIGH = 300000
EXAMPLE_STEPS = 100000

# Entries that must also agree with the sealed handoff's own per-arm table.
HANDOFF_AGREEMENTS = {
    "seconds_per_step": "seconds_per_step",
    "wall_hours": "wall_hours",
}

_LOADED: dict[str, Any] = {}


def _facts() -> dict[str, Any]:
    """Every committed file the manifest reads, loaded once per process."""
    if _LOADED:
        return _LOADED
    from pinn.verification.feasibility_scorecard import load_scorecard

    _LOADED.update(
        {
            "records": {arm_id: _load_record(arm_id) for arm_id in EXPECTED_ARMS},
            "handoff": _load_json_rel(HANDOFF_REL.as_posix(), what="handoff"),
            "card": load_scorecard(),
            "scorecard_raw": _load_json_rel(
                SCORECARD_ARTIFACT_REL.as_posix(), what="scorecard artifact"
            ),
            "baselines": _load_json_rel(BASELINES_REL.as_posix(), what="baselines"),
            "survey": _load_json_rel(SURVEY_REL.as_posix(), what="survey"),
            "picks": _load_json_rel(PICKS_REL.as_posix(), what="picks"),
            "census": _load_json_rel(CENSUS_REL.as_posix(), what="census"),
            "status": _load_json_rel(STATUS_REL.as_posix(), what="status"),
        }
    )
    return _LOADED


def _tier_position(facts: Mapping[str, Any], tier: int) -> int:
    levels = facts["card"].section("tiers")["levels"]
    for position, level in enumerate(levels):
        if int(level["tier"]) == tier:
            return position
    fail(f"the scorecard names no level whose tier is {tier}")


def _tier1_max(card: Any) -> float:
    """The scorecard's Tier-1 E_max, read from its own tiers section."""
    for level in card.section("tiers")["levels"]:
        if int(level["tier"]) == 1:
            return float(level["E_max"])
    fail("the scorecard names no level whose tier is 1")


def committed_table(
    facts: Mapping[str, Any],
) -> dict[str, tuple[str, str, Any]]:
    """The verifier's own id-to-key table for every entry read from a file.

    Written here, independently of the producer: a recorded source that does not
    equal this table's answer fails, so a swapped file or key cannot pass.
    """
    table: dict[str, tuple[str, str, Any]] = {}
    arm_keys = {
        "tier": "result.tier",
        "E": "result.E",
        "eps_h": "result.eps_h",
        "h_1pct": "result.h.0.1",
        "h_10pct": "result.h.1.1",
        "state": "result.state",
        "first_omega_0": "first_omega_0",
        "E_formula": "formula.E_formula",
        "counts": "formula.counts",
        "seconds_per_step": "timing.seconds_per_step",
        "timing_wall_seconds": "timing.wall_seconds",
        "polish_seconds": "wall.polish_seconds",
        "wall_hours": "wall.hours",
        "curve.E_step0": "trace.0.E",
        "curve.E_first_reading": "trace.1.E",
    }
    for arm_id in EXPECTED_ARMS:
        for field, key in arm_keys.items():
            table[f"arm.{arm_id}.{field}"] = (
                _record_rel(arm_id),
                key,
                facts["records"][arm_id],
            )
    handoff = facts["handoff"]
    for entry_id, key in (
        ("handoff.verdict", "verdict.verdict"),
        ("handoff.reason", "verdict.reasons.0"),
        ("handoff.qualifier", "verdict.representation_limit_qualifier"),
        ("handoff.level3", "level3"),
        ("handoff.phases_61_63", "phases_61_63"),
        ("handoff.stop_reason", "stop_reason"),
    ):
        table[entry_id] = (HANDOFF_REL.as_posix(), key, handoff)
    scorecard_path = SCORECARD_ARTIFACT_REL.as_posix()
    for entry_id, tier, field in (
        ("tiers.tier1.E_max", 1, "E_max"),
        ("tiers.tier2.E_max", 2, "E_max"),
        ("tiers.tier2.eps_h_max", 2, "eps_h_max"),
        ("tiers.tier3.E_max", 3, "E_max"),
        ("tiers.tier3.eps_h_max", 3, "eps_h_max"),
    ):
        table[entry_id] = (
            scorecard_path,
            f"tiers.levels.{_tier_position(facts, tier)}.{field}",
            facts["scorecard_raw"],
        )
    baselines_path = BASELINES_REL.as_posix()
    for entry_id, key in (
        ("baseline.formula.median_E.train", "median_E.formula_train"),
        ("baseline.formula.median_E.validation", "median_E.formula_validation"),
        ("baseline.copy.median_E.validation", "median_E.copy_validation"),
        (
            "baseline.copy.tier1.validation",
            "nn_copy_reaches_tier1_on_validation",
        ),
    ):
        table[entry_id] = (baselines_path, key, facts["baselines"])
    survey_path = SURVEY_REL.as_posix()
    for entry_id, key in (
        ("survey.stage0.error_growth_median", "per_stage.0.measures.error_growth.median"),
        ("survey.stage4b.error_growth_median", "per_stage.4b.measures.error_growth.median"),
        ("survey.stage6.error_growth_median", "per_stage.6.measures.error_growth.median"),
        ("survey.stage3.count", "stage3.count"),
    ):
        table[entry_id] = (survey_path, key, facts["survey"])
    picks_path = PICKS_REL.as_posix()
    for entry_id, key in (
        ("survey.picks.stage4b", "stage4b.record"),
        ("survey.picks.stage6", "stage6.record"),
    ):
        table[entry_id] = (picks_path, key, facts["picks"])
    table["census.stage0.N_in_median"] = (
        CENSUS_REL.as_posix(),
        "distributions.N_in.quantiles.50",
        facts["census"],
    )
    status_path = STATUS_REL.as_posix()
    for entry_id, key in (
        ("cost.gen7.seconds_per_step", "s_per_step_ema"),
        ("cost.gen7.step", "step"),
    ):
        table[entry_id] = (status_path, key, facts["status"])
    return table


# --- the verifier's own arithmetic, one function per named formula ----------


def _arm_value(facts: Mapping[str, Any], arm_id: str, dotted: str) -> Any:
    return _field(facts["records"][arm_id], dotted)


def _adam_steps(facts: Mapping[str, Any], arm_id: str) -> int:
    budget = facts["records"][arm_id]["budget"]
    value = budget["new_budget_steps"] if budget["extended"] else budget["budget_steps"]
    if isinstance(value, bool) or not isinstance(value, int):
        fail(f"arm {arm_id} budget names no integer step count: {value!r}")
    return value


def _sustained(facts: Mapping[str, Any], arm_id: str) -> float:
    return _arm_value(facts, arm_id, "wall.adam_seconds") / _adam_steps(facts, arm_id)


def _first_fraction(facts: Mapping[str, Any], arm_id: str) -> float:
    step = _field(facts["records"][arm_id], "trace.1.step")
    frozen = _field(facts["records"][arm_id], "budget.frozen_budget_steps")
    return step / frozen


def _range_after_first(facts: Mapping[str, Any], arm_id: str) -> float:
    tail = [reading["E"] for reading in facts["records"][arm_id]["trace"][1:]]
    return max(tail) - min(tail)


def _hours(facts: Mapping[str, Any], arms: Sequence[str]) -> float:
    return ordered_sum(_arm_value(facts, arm_id, "wall.hours") for arm_id in arms)


def _f_hours_total(facts: Mapping[str, Any]) -> float:
    """The seven wall.hours in handoff order, through 64-01's ordered_sum."""
    return _hours(facts, EXPECTED_ARMS)


def _f_hours_rung1(facts: Mapping[str, Any]) -> float:
    return _hours(facts, RUNG1_ARMS)


def _f_hours_sweep(facts: Mapping[str, Any]) -> float:
    return _hours(facts, SWEEP_ARMS)


def _f_steps_total_adam(facts: Mapping[str, Any]) -> int:
    total = 0
    for arm_id in EXPECTED_ARMS:
        total += _adam_steps(facts, arm_id)
    return total


def _sweep_budgets(facts: Mapping[str, Any]) -> list[int]:
    """The frozen steps_budget rule re-applied to each sweep arm's timing run."""
    from pinn.verification import feasibility_scorecard

    cap = float(facts["card"].section("budget_rule")["cap_hours_single_system"])
    budgets = []
    for arm_id in SWEEP_ARMS:
        timing = _field(facts["records"][arm_id], "timing")
        computed = feasibility_scorecard.steps_budget(
            cap,
            timing["wall_seconds"],
            timing["steps"],
            scorecard=facts["card"],
        )
        recorded = _field(facts["records"][arm_id], "budget.budget_steps")
        if computed != recorded:
            fail(
                f"{arm_id} recorded budget {recorded} != the frozen rule's {computed}"
            )
        budgets.append(computed)
    return budgets


def _f_steps_sweep_budget_min(facts: Mapping[str, Any]) -> int:
    return min(_sweep_budgets(facts))


def _f_steps_sweep_budget_max(facts: Mapping[str, Any]) -> int:
    return max(_sweep_budgets(facts))


def _f_timed_sps_min(facts: Mapping[str, Any]) -> float:
    return min(_arm_value(facts, arm_id, "timing.seconds_per_step") for arm_id in EXPECTED_ARMS)


def _f_timed_sps_max(facts: Mapping[str, Any]) -> float:
    return max(_arm_value(facts, arm_id, "timing.seconds_per_step") for arm_id in EXPECTED_ARMS)


def _f_sustained_sps_min(facts: Mapping[str, Any]) -> float:
    return min(_sustained(facts, arm_id) for arm_id in EXPECTED_ARMS)


def _f_sustained_sps_max(facts: Mapping[str, Any]) -> float:
    return max(_sustained(facts, arm_id) for arm_id in EXPECTED_ARMS)


def _f_timing_wall_min(facts: Mapping[str, Any]) -> float:
    return min(_arm_value(facts, arm_id, "timing.wall_seconds") for arm_id in EXPECTED_ARMS)


def _f_timing_wall_max(facts: Mapping[str, Any]) -> float:
    return max(_arm_value(facts, arm_id, "timing.wall_seconds") for arm_id in EXPECTED_ARMS)


def _f_timing_wall_total(facts: Mapping[str, Any]) -> float:
    return ordered_sum(
        _arm_value(facts, arm_id, "timing.wall_seconds") for arm_id in EXPECTED_ARMS
    )


def _f_polish_min(facts: Mapping[str, Any]) -> float:
    return min(_arm_value(facts, arm_id, "wall.polish_seconds") for arm_id in EXPECTED_ARMS)


def _f_polish_max(facts: Mapping[str, Any]) -> float:
    return max(_arm_value(facts, arm_id, "wall.polish_seconds") for arm_id in EXPECTED_ARMS)


def _f_unextended_hours_min(facts: Mapping[str, Any]) -> float:
    return min(
        _arm_value(facts, arm_id, "wall.hours")
        for arm_id in EXPECTED_ARMS
        if not facts["records"][arm_id]["budget"]["extended"]
    )


def _f_unextended_hours_max(facts: Mapping[str, Any]) -> float:
    return max(
        _arm_value(facts, arm_id, "wall.hours")
        for arm_id in EXPECTED_ARMS
        if not facts["records"][arm_id]["budget"]["extended"]
    )


def _f_extended_hours(facts: Mapping[str, Any]) -> float:
    extended = [
        arm_id
        for arm_id in EXPECTED_ARMS
        if facts["records"][arm_id]["budget"]["extended"]
    ]
    if len(extended) != 1:
        fail(f"expected exactly one arm with a doubled budget, found {extended!r}")
    return _arm_value(facts, extended[0], "wall.hours")


def _f_best_eps_h_official(facts: Mapping[str, Any]) -> float:
    return min(_arm_value(facts, arm_id, "result.eps_h") for arm_id in EXPECTED_ARMS)


def _f_best_eps_h_official_arms(facts: Mapping[str, Any]) -> str:
    best = _f_best_eps_h_official(facts)
    return ", ".join(
        arm_id
        for arm_id in EXPECTED_ARMS
        if _arm_value(facts, arm_id, "result.eps_h") == best
    )


def _f_best_ratio_to_bar(facts: Mapping[str, Any]) -> float:
    levels = facts["card"].section("tiers")["levels"]
    bar = float(levels[_tier_position(facts, 3)]["eps_h_max"])
    return _f_best_eps_h_official(facts) / bar


def _state_eps_h(facts: Mapping[str, Any]) -> list[tuple[float, str, str]]:
    return [
        (_arm_value(facts, arm_id, f"states.{state}.score_gold.eps_h"), arm_id, state)
        for arm_id in EXPECTED_ARMS
        for state in ("adam", "polish")
    ]


def _trace_eps_h(facts: Mapping[str, Any]) -> list[tuple[float, str, int]]:
    return [
        (reading["eps_h"], arm_id, reading["step"])
        for arm_id in EXPECTED_ARMS
        for reading in facts["records"][arm_id]["trace"]
    ]


def _f_best_lowest_state(facts: Mapping[str, Any]) -> float:
    return min(value for value, _arm, _state in _state_eps_h(facts))


def _f_best_lowest_state_arm(facts: Mapping[str, Any]) -> str:
    best = _f_best_lowest_state(facts)
    return next(arm for value, arm, _state in _state_eps_h(facts) if value == best)


def _f_best_lowest_state_state(facts: Mapping[str, Any]) -> str:
    best = _f_best_lowest_state(facts)
    return next(state for value, _arm, state in _state_eps_h(facts) if value == best)


def _f_best_lowest_trace(facts: Mapping[str, Any]) -> float:
    return min(value for value, _arm, _step in _trace_eps_h(facts))


def _f_best_lowest_trace_arm(facts: Mapping[str, Any]) -> str:
    best = _f_best_lowest_trace(facts)
    return next(arm for value, arm, _step in _trace_eps_h(facts) if value == best)


def _f_best_lowest_trace_step(facts: Mapping[str, Any]) -> int:
    best = _f_best_lowest_trace(facts)
    return next(step for value, _arm, step in _trace_eps_h(facts) if value == best)


def _rung1_below(facts: Mapping[str, Any]) -> list[str]:
    return [
        arm_id
        for arm_id in RUNG1_ARMS
        if _arm_value(facts, arm_id, "result.E")
        < _arm_value(facts, arm_id, "formula.E_formula")
    ]


def _f_rung1_below_formula(facts: Mapping[str, Any]) -> list[int]:
    return [len(_rung1_below(facts)), len(RUNG1_ARMS)]


def _f_rung1_below_formula_systems(facts: Mapping[str, Any]) -> str:
    return ", ".join(arm_id[len("r1-") :] for arm_id in _rung1_below(facts))


def _f_rung1_counts_true(facts: Mapping[str, Any]) -> list[int]:
    reached = 0
    for arm_id in RUNG1_ARMS:
        if _arm_value(facts, arm_id, "formula.counts") is True:
            reached += 1
    return [reached, len(RUNG1_ARMS)]


def _curve(facts: Mapping[str, Any], key: str) -> list[float]:
    return [_arm_value(facts, arm_id, key) for arm_id in EXPECTED_ARMS]


def _f_curve_e_step0_min(facts: Mapping[str, Any]) -> float:
    return min(_curve(facts, "trace.0.E"))


def _f_curve_e_step0_max(facts: Mapping[str, Any]) -> float:
    return max(_curve(facts, "trace.0.E"))


def _f_curve_first_reading_min(facts: Mapping[str, Any]) -> float:
    return min(_curve(facts, "trace.1.E"))


def _f_curve_first_reading_max(facts: Mapping[str, Any]) -> float:
    return max(_curve(facts, "trace.1.E"))


def _fold_drop(facts: Mapping[str, Any]) -> list[float]:
    return [
        _arm_value(facts, arm_id, "trace.0.E") / _arm_value(facts, arm_id, "trace.1.E")
        for arm_id in EXPECTED_ARMS
    ]


def _f_curve_fold_drop_min(facts: Mapping[str, Any]) -> float:
    return min(_fold_drop(facts))


def _f_curve_fold_drop_max(facts: Mapping[str, Any]) -> float:
    return max(_fold_drop(facts))


def _f_curve_first_fraction_min(facts: Mapping[str, Any]) -> float:
    return min(_first_fraction(facts, arm_id) for arm_id in EXPECTED_ARMS)


def _f_curve_first_fraction_max(facts: Mapping[str, Any]) -> float:
    return max(_first_fraction(facts, arm_id) for arm_id in EXPECTED_ARMS)


def _f_curve_e_final_min(facts: Mapping[str, Any]) -> float:
    return min(_curve(facts, "result.E"))


def _f_curve_e_final_max(facts: Mapping[str, Any]) -> float:
    return max(_curve(facts, "result.E"))


def _tier1_multiple(facts: Mapping[str, Any]) -> list[float]:
    levels = facts["card"].section("tiers")["levels"]
    limit = float(levels[_tier_position(facts, 1)]["E_max"])
    return [_arm_value(facts, arm_id, "result.E") / limit for arm_id in EXPECTED_ARMS]


def _f_curve_tier1_multiple_min(facts: Mapping[str, Any]) -> float:
    return min(_tier1_multiple(facts))


def _f_curve_tier1_multiple_max(facts: Mapping[str, Any]) -> float:
    return max(_tier1_multiple(facts))


def _f_curve_range_after_first_min(facts: Mapping[str, Any]) -> float:
    return min(_range_after_first(facts, arm_id) for arm_id in EXPECTED_ARMS)


def _f_curve_range_after_first_max(facts: Mapping[str, Any]) -> float:
    return max(_range_after_first(facts, arm_id) for arm_id in EXPECTED_ARMS)


def _rung_rule(facts: Mapping[str, Any], which: str) -> list[int]:
    rule = facts["card"].section("decision_rule")
    return [int(rule[f"{which}_min_count"]), int(rule[f"{which}_panel_size"])]


def _f_decision_rung2b(facts: Mapping[str, Any]) -> list[int]:
    return _rung_rule(facts, "rung2b")


def _f_decision_rung3(facts: Mapping[str, Any]) -> list[int]:
    return _rung_rule(facts, "rung3")


def _f_decision_rung3_share(facts: Mapping[str, Any]) -> float:
    minimum, panel = _rung_rule(facts, "rung3")
    return minimum / panel


def _formula_tier1(facts: Mapping[str, Any], split: str) -> list[int]:
    counts = facts["baselines"]["formula_tier_counts"][split]
    total = 0
    reached = 0
    for key in ("0", "1", "2", "3", "not_applicable"):
        total += int(counts[key])
        if key in {"1", "2", "3"}:
            reached += int(counts[key])
    return [reached, total]


def _f_formula_tier1_train(facts: Mapping[str, Any]) -> list[int]:
    return _formula_tier1(facts, "train")


def _f_formula_tier1_validation(facts: Mapping[str, Any]) -> list[int]:
    return _formula_tier1(facts, "validation")


def _f_census_one_part_in_0p1(facts: Mapping[str, Any]) -> int:
    accuracy = facts["census"]["phase_accuracy"]["0.1"]
    return int(accuracy["one_part_in"])


def _gen7_rate(facts: Mapping[str, Any]) -> float:
    return float(_field(facts["status"], "s_per_step_ema"))


def _f_forscale_days_low(facts: Mapping[str, Any]) -> float:
    return FORSCALE_STEPS_LOW * _gen7_rate(facts) / 86400.0


def _f_forscale_days_high(facts: Mapping[str, Any]) -> float:
    return FORSCALE_STEPS_HIGH * _gen7_rate(facts) / 86400.0


def _f_forscale_hours_low(facts: Mapping[str, Any]) -> float:
    return FORSCALE_STEPS_LOW * _gen7_rate(facts) / 3600.0


def _f_example_sps(facts: Mapping[str, Any]) -> float:
    values = sorted(
        _arm_value(facts, arm_id, "timing.seconds_per_step") for arm_id in EXPECTED_ARMS
    )
    return values[len(values) // 2]


def _f_example_hours(facts: Mapping[str, Any]) -> float:
    return EXAMPLE_STEPS * _f_example_sps(facts) / 3600.0


def _cpu_values(facts: Mapping[str, Any], field: str) -> list[Any]:
    """One field of every one of the 14 CPU states, in handoff arm order."""
    return [
        facts["manifest"][f"cpu.{arm_id}.{state}.{field}"]
        for arm_id in EXPECTED_ARMS
        for state in CPU_STATES
    ]


def _one_cpu_value(facts: Mapping[str, Any], field: str) -> Any:
    values = _cpu_values(facts, field)
    if len(set(values)) != 1:
        fail(f"the 14 CPU states disagree on {field}: {sorted(set(values))!r}")
    return values[0]


def _const_gaps(facts: Mapping[str, Any]) -> list[float]:
    """Each Rung-1 system's official E minus its constant-predictor E."""
    return [
        (
            facts["records"][f"r1-{system}"]["result"]["E"]
            - facts["manifest"][f"cpu.const.{system}.E"]
        )
        for system in CPU_SYSTEMS
    ]


def _f_cpu_const_range_min(facts: Mapping[str, Any]) -> float:
    return min(facts["manifest"][f"cpu.const.{system}.E"] for system in CPU_SYSTEMS)


def _f_cpu_const_range_max(facts: Mapping[str, Any]) -> float:
    return max(facts["manifest"][f"cpu.const.{system}.E"] for system in CPU_SYSTEMS)


def _f_cpu_range_e_sys_t0_min(facts: Mapping[str, Any]) -> float:
    return min(_cpu_values(facts, "e_sys_t0"))


def _f_cpu_range_e_sys_t0_max(facts: Mapping[str, Any]) -> float:
    return max(_cpu_values(facts, "e_sys_t0"))


def _f_cpu_range_e_in_t0_min(facts: Mapping[str, Any]) -> float:
    return min(_cpu_values(facts, "e_in_t0"))


def _f_cpu_range_e_in_t0_max(facts: Mapping[str, Any]) -> float:
    return max(_cpu_values(facts, "e_in_t0"))


def _f_cpu_range_best_moment_min(facts: Mapping[str, Any]) -> float:
    return min(_cpu_values(facts, "best_moment"))


def _f_cpu_range_best_moment_max(facts: Mapping[str, Any]) -> float:
    return max(_cpu_values(facts, "best_moment"))


def _f_cpu_range_timevar_min(facts: Mapping[str, Any]) -> float:
    return min(_cpu_values(facts, "timevar_ratio"))


def _f_cpu_range_timevar_max(facts: Mapping[str, Any]) -> float:
    return max(_cpu_values(facts, "timevar_ratio"))


def _f_cpu_range_rms_ratio_min(facts: Mapping[str, Any]) -> float:
    return min(_cpu_values(facts, "rms_ratio"))


def _f_cpu_range_rms_ratio_max(facts: Mapping[str, Any]) -> float:
    return max(_cpu_values(facts, "rms_ratio"))


def _f_cpu_total_n_within_tier1(facts: Mapping[str, Any]) -> int:
    return sum(_cpu_values(facts, "n_within_tier1"))


def _f_cpu_n_times(facts: Mapping[str, Any]) -> int:
    return _one_cpu_value(facts, "n_times")


def _f_const_gap_min(facts: Mapping[str, Any]) -> float:
    return min(_const_gaps(facts))


def _f_const_gap_max(facts: Mapping[str, Any]) -> float:
    return max(_const_gaps(facts))


def _f_cpu_attestation_test_split_opened(facts: Mapping[str, Any]) -> int:
    return int(facts["attestation"]["test_split_opened"])


def _f_cpu_attestation_validation(facts: Mapping[str, Any]) -> int:
    return int(facts["attestation"]["opened"]["validation"])


def _f_cpu_attestation_other_under_root(facts: Mapping[str, Any]) -> int:
    return int(facts["attestation"]["opened"]["other_under_root"])


def _f_cpu_attestation_blocked_attempts(facts: Mapping[str, Any]) -> int:
    return int(facts["attestation"]["blocked_attempts"])


def _f_cpu_attestation_refused_before_open(facts: Mapping[str, Any]) -> int:
    return int(facts["attestation"]["refused_before_open"])


ARITHMETIC_NAMES: dict[str, Any] = {
    "hours_total": _f_hours_total,
    "hours_rung1": _f_hours_rung1,
    "hours_sweep": _f_hours_sweep,
    "steps_total_adam": _f_steps_total_adam,
    "steps_sweep_budget_min": _f_steps_sweep_budget_min,
    "steps_sweep_budget_max": _f_steps_sweep_budget_max,
    "timed_sps_min": _f_timed_sps_min,
    "timed_sps_max": _f_timed_sps_max,
    "sustained_sps_min": _f_sustained_sps_min,
    "sustained_sps_max": _f_sustained_sps_max,
    "timing_wall_min": _f_timing_wall_min,
    "timing_wall_max": _f_timing_wall_max,
    "timing_wall_total": _f_timing_wall_total,
    "polish_min": _f_polish_min,
    "polish_max": _f_polish_max,
    "unextended_hours_min": _f_unextended_hours_min,
    "unextended_hours_max": _f_unextended_hours_max,
    "extended_hours": _f_extended_hours,
    "best_eps_h_official": _f_best_eps_h_official,
    "best_eps_h_official_arms": _f_best_eps_h_official_arms,
    "best_ratio_to_bar": _f_best_ratio_to_bar,
    "best_lowest_state": _f_best_lowest_state,
    "best_lowest_state_arm": _f_best_lowest_state_arm,
    "best_lowest_state_state": _f_best_lowest_state_state,
    "best_lowest_trace": _f_best_lowest_trace,
    "best_lowest_trace_arm": _f_best_lowest_trace_arm,
    "best_lowest_trace_step": _f_best_lowest_trace_step,
    "rung1_below_formula": _f_rung1_below_formula,
    "rung1_below_formula_systems": _f_rung1_below_formula_systems,
    "rung1_counts_true": _f_rung1_counts_true,
    "curve_e_step0_min": _f_curve_e_step0_min,
    "curve_e_step0_max": _f_curve_e_step0_max,
    "curve_first_reading_min": _f_curve_first_reading_min,
    "curve_first_reading_max": _f_curve_first_reading_max,
    "curve_fold_drop_min": _f_curve_fold_drop_min,
    "curve_fold_drop_max": _f_curve_fold_drop_max,
    "curve_first_fraction_min": _f_curve_first_fraction_min,
    "curve_first_fraction_max": _f_curve_first_fraction_max,
    "curve_e_final_min": _f_curve_e_final_min,
    "curve_e_final_max": _f_curve_e_final_max,
    "curve_tier1_multiple_min": _f_curve_tier1_multiple_min,
    "curve_tier1_multiple_max": _f_curve_tier1_multiple_max,
    "curve_range_after_first_min": _f_curve_range_after_first_min,
    "curve_range_after_first_max": _f_curve_range_after_first_max,
    "decision_rung2b": _f_decision_rung2b,
    "decision_rung3": _f_decision_rung3,
    "decision_rung3_share": _f_decision_rung3_share,
    "formula_tier1_train": _f_formula_tier1_train,
    "formula_tier1_validation": _f_formula_tier1_validation,
    "census_one_part_in_0p1": _f_census_one_part_in_0p1,
    "forscale_days_low": _f_forscale_days_low,
    "forscale_days_high": _f_forscale_days_high,
    "forscale_hours_low": _f_forscale_hours_low,
    "example_sps": _f_example_sps,
    "example_hours": _f_example_hours,
    "cpu_const_range_min": _f_cpu_const_range_min,
    "cpu_const_range_max": _f_cpu_const_range_max,
    "cpu_range_e_sys_t0_min": _f_cpu_range_e_sys_t0_min,
    "cpu_range_e_sys_t0_max": _f_cpu_range_e_sys_t0_max,
    "cpu_range_e_in_t0_min": _f_cpu_range_e_in_t0_min,
    "cpu_range_e_in_t0_max": _f_cpu_range_e_in_t0_max,
    "cpu_range_best_moment_min": _f_cpu_range_best_moment_min,
    "cpu_range_best_moment_max": _f_cpu_range_best_moment_max,
    "cpu_range_timevar_min": _f_cpu_range_timevar_min,
    "cpu_range_timevar_max": _f_cpu_range_timevar_max,
    "cpu_range_rms_ratio_min": _f_cpu_range_rms_ratio_min,
    "cpu_range_rms_ratio_max": _f_cpu_range_rms_ratio_max,
    "cpu_total_n_within_tier1": _f_cpu_total_n_within_tier1,
    "cpu_n_times": _f_cpu_n_times,
    "const_gap_min": _f_const_gap_min,
    "const_gap_max": _f_const_gap_max,
    "cpu_attestation_test_split_opened": _f_cpu_attestation_test_split_opened,
    "cpu_attestation_validation": _f_cpu_attestation_validation,
    "cpu_attestation_other_under_root": _f_cpu_attestation_other_under_root,
    "cpu_attestation_blocked_attempts": _f_cpu_attestation_blocked_attempts,
    "cpu_attestation_refused_before_open": _f_cpu_attestation_refused_before_open,
}

ARM_FORMULAS = {
    "adam_steps": ("arm_adam_steps", _adam_steps),
    "sustained_seconds_per_step": ("arm_sustained", _sustained),
    "curve.first_reading_fraction": ("arm_first_fraction", _first_fraction),
    "curve.range_after_first": ("arm_range_after_first", _range_after_first),
}


def arithmetic_table(
    facts: Mapping[str, Any],
) -> dict[str, tuple[str, Any]]:
    """Every arithmetic id, with the verifier's own formula bound to ``facts``."""
    table: dict[str, tuple[str, Any]] = {}
    for arm_id in EXPECTED_ARMS:
        for field, (name, formula) in ARM_FORMULAS.items():
            table[f"arm.{arm_id}.{field}"] = (
                name,
                lambda f=formula, a=arm_id: f(facts, a),
            )
    ids = {
        "hours_total": "hours.total",
        "hours_rung1": "hours.rung1",
        "hours_sweep": "hours.sweep",
        "steps_total_adam": "steps.total_adam",
        "steps_sweep_budget_min": "steps.sweep_budget.min",
        "steps_sweep_budget_max": "steps.sweep_budget.max",
        "timed_sps_min": "seconds_per_step.timed.min",
        "timed_sps_max": "seconds_per_step.timed.max",
        "sustained_sps_min": "seconds_per_step.sustained.min",
        "sustained_sps_max": "seconds_per_step.sustained.max",
        "timing_wall_min": "timing.wall_seconds.min",
        "timing_wall_max": "timing.wall_seconds.max",
        "timing_wall_total": "timing.wall_seconds.total",
        "polish_min": "polish.seconds.min",
        "polish_max": "polish.seconds.max",
        "unextended_hours_min": "cost.arm_hours.unextended.min",
        "unextended_hours_max": "cost.arm_hours.unextended.max",
        "extended_hours": "cost.arm_hours.extended",
        "best_eps_h_official": "best.eps_h_official",
        "best_eps_h_official_arms": "best.eps_h_official_arms",
        "best_ratio_to_bar": "best.ratio_to_bar",
        "best_lowest_state": "best.eps_h_lowest_state",
        "best_lowest_state_arm": "best.eps_h_lowest_state_arm",
        "best_lowest_state_state": "best.eps_h_lowest_state_state",
        "best_lowest_trace": "best.eps_h_lowest_trace",
        "best_lowest_trace_arm": "best.eps_h_lowest_trace_arm",
        "best_lowest_trace_step": "best.eps_h_lowest_trace_step",
        "rung1_below_formula": "rung1.below_formula",
        "rung1_below_formula_systems": "rung1.below_formula_systems",
        "rung1_counts_true": "rung1.counts_true",
        "curve_e_step0_min": "curve.E_step0.min",
        "curve_e_step0_max": "curve.E_step0.max",
        "curve_first_reading_min": "curve.E_first_reading.min",
        "curve_first_reading_max": "curve.E_first_reading.max",
        "curve_fold_drop_min": "curve.fold_drop.min",
        "curve_fold_drop_max": "curve.fold_drop.max",
        "curve_first_fraction_min": "curve.first_reading_fraction.min",
        "curve_first_fraction_max": "curve.first_reading_fraction.max",
        "curve_e_final_min": "curve.E_final.min",
        "curve_e_final_max": "curve.E_final.max",
        "curve_tier1_multiple_min": "curve.tier1_multiple.min",
        "curve_tier1_multiple_max": "curve.tier1_multiple.max",
        "curve_range_after_first_min": "curve.range_after_first.min",
        "curve_range_after_first_max": "curve.range_after_first.max",
        "decision_rung2b": "decision.rung2b",
        "decision_rung3": "decision.rung3",
        "decision_rung3_share": "decision.rung3_share",
        "formula_tier1_train": "baseline.formula.tier1.train",
        "formula_tier1_validation": "baseline.formula.tier1.validation",
        "census_one_part_in_0p1": "census.one_part_in_0p1",
        "forscale_days_low": "cost.forscale.days_low",
        "forscale_days_high": "cost.forscale.days_high",
        "forscale_hours_low": "cost.forscale.hours_low",
        "example_sps": "cost.example.seconds_per_step",
        "example_hours": "cost.example.hours",
        "cpu_const_range_min": "cpu.const.range.min",
        "cpu_const_range_max": "cpu.const.range.max",
        "cpu_range_e_sys_t0_min": "cpu.range.e_sys_t0.min",
        "cpu_range_e_sys_t0_max": "cpu.range.e_sys_t0.max",
        "cpu_range_e_in_t0_min": "cpu.range.e_in_t0.min",
        "cpu_range_e_in_t0_max": "cpu.range.e_in_t0.max",
        "cpu_range_best_moment_min": "cpu.range.best_moment.min",
        "cpu_range_best_moment_max": "cpu.range.best_moment.max",
        "cpu_range_timevar_min": "cpu.range.timevar.min",
        "cpu_range_timevar_max": "cpu.range.timevar.max",
        "cpu_range_rms_ratio_min": "cpu.range.rms_ratio.min",
        "cpu_range_rms_ratio_max": "cpu.range.rms_ratio.max",
        "cpu_total_n_within_tier1": "cpu.total.n_within_tier1",
        "cpu_n_times": "cpu.n_times",
        "const_gap_min": "const_gap.min",
        "const_gap_max": "const_gap.max",
        "cpu_attestation_test_split_opened": "cpu.attestation.test_split_opened",
        "cpu_attestation_validation": "cpu.attestation.validation",
        "cpu_attestation_other_under_root": "cpu.attestation.other_under_root",
        "cpu_attestation_blocked_attempts": "cpu.attestation.blocked_attempts",
        "cpu_attestation_refused_before_open": "cpu.attestation.refused_before_open",
    }
    for name, formula in ARITHMETIC_NAMES.items():
        table[ids[name]] = (name, lambda f=formula: f(facts))
    return table


CITED_TABLE: dict[str, tuple[str, str, str]] = {
    "pub.breen.energy_typical": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "of order 10\u207b\u00b2",
    ),
    "pub.breen.energy_projected": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "brings it to order 10\u207b\u2075",
    ),
    "pub.kollias.energy_range": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "to within \u223c 0.02\u20133%",
    ),
    "pub.kollias.euler": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "Euler 7.74 \u00d7 10\u207b\u2074",
    ),
    "pub.kollias.lagrange": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "Lagrange 3.23 \u00d7 10\u207b\u00b2",
    ),
    "pub.kollias.figure8": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "figure-eight 1.64 \u00d7 10\u207b\u2074",
    ),
    "pub.kollias.adam_epochs": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "2 to 3 \u00d7 10\u2075 Adam epochs",
    ),
    "pub.kollias.lbfgs_epochs": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "1.5 \u00d7 10\u2074 L-BFGS epochs",
    ),
    "gap5908.floor.1632": (
        GAPS_REL.as_posix(),
        GAPS_COMMIT,
        "4.7e-2, 2.1e-1 and 3.8e-1",
    ),
    "gap5908.floor.851": (
        GAPS_REL.as_posix(),
        GAPS_COMMIT,
        "4.7e-2, 2.1e-1 and 3.8e-1",
    ),
    "gap5908.floor.4658": (
        GAPS_REL.as_posix(),
        GAPS_COMMIT,
        "4.7e-2, 2.1e-1 and 3.8e-1",
    ),
    "gap5908.floor_range": (
        GAPS_REL.as_posix(),
        GAPS_COMMIT,
        "5\u201338%",
    ),
    "machine.model": (
        PROJECT_REL.as_posix(),
        PROJECT_COMMIT,
        "Apple M5 Pro",
    ),
    "machine.memory": (
        PROJECT_REL.as_posix(),
        PROJECT_COMMIT,
        "24 GB",
    ),
    "cost.forscale.steps_low": (
        AMENDMENTS_REL.as_posix(),
        AMENDMENTS_COMMIT,
        "200,000",
    ),
    "cost.forscale.steps_high": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "300,000",
    ),
    "cost.example.steps": (
        RESEARCH_REL.as_posix(),
        RESEARCH_COMMIT,
        "10\u2075 steps",
    ),
}


def _check_current_file(relative: Any, digest: Any, *, what: str) -> None:
    """A recorded ``{path, sha256}`` whose digest must equal the file on disk."""
    if not isinstance(relative, str) or not relative:
        fail(f"{what} has no path")
    if not isinstance(digest, str) or HEX64.match(digest) is None:
        fail(f"{what} has no 64-hex sha256")
    path = repo_path(relative, what=what)
    if not path.is_file():
        fail(f"{what} does not exist: {relative}")
    disk = sha256_file(path)
    if disk != digest:
        fail(f"{what} SHA-256 {disk} != recorded {digest}")


def _check_handoff_agreement(
    entry_id: str, value: Any, facts: Mapping[str, Any]
) -> None:
    """The two per-arm readings the sealed handoff states must agree with it."""
    match = re.fullmatch(
        r"arm\.(?P<arm>[^.]+)\.(?P<field>seconds_per_step|wall_hours)", entry_id
    )
    if match is None:
        return
    rows = {row["arm_id"]: row for row in facts["handoff"]["arms"]}
    arm_id = match.group("arm")
    if arm_id not in rows:
        fail(f"entry {entry_id} names an arm the handoff does not list: {arm_id}")
    expected = rows[arm_id][HANDOFF_AGREEMENTS[match.group("field")]]
    if value != expected:
        fail(f"entry {entry_id} value {value!r} != the handoff's {expected!r}")


def _check_record_entry(
    entry: Mapping[str, Any], source: Mapping[str, Any], facts: Mapping[str, Any]
) -> None:
    entry_id = entry["id"]
    table = committed_table(facts)
    if entry_id not in table:
        fail(f"entry {entry_id} is not in the verifier's committed-record table")
    expected_path, expected_key, payload = table[entry_id]
    if set(source) != {"path", "key"}:
        fail(f"entry {entry_id} source must hold exactly path and key")
    if source["path"] != expected_path or source["key"] != expected_key:
        fail(
            f"entry {entry_id} source {dict(source)!r} != the table's "
            f"({expected_path!r}, {expected_key!r})"
        )
    value = _field(payload, expected_key)
    if entry["value"] != value:
        fail(
            f"entry {entry_id} value {entry['value']!r} != "
            f"{expected_path}:{expected_key} {value!r}"
        )
    _check_handoff_agreement(entry_id, value, facts)


def _check_arithmetic_entry(
    entry: Mapping[str, Any], source: Mapping[str, Any], facts: Mapping[str, Any]
) -> None:
    entry_id = entry["id"]
    if set(source) != {"formula"}:
        fail(f"entry {entry_id} arithmetic source must hold exactly formula")
    table = arithmetic_table(facts)
    if entry_id not in table:
        fail(f"entry {entry_id} is not in the verifier's arithmetic table")
    name, formula = table[entry_id]
    if source["formula"] != name:
        fail(f"entry {entry_id} formula {source['formula']!r} != the table's {name!r}")
    value = formula()
    if entry["value"] != value:
        fail(f"entry {entry_id} value {entry['value']!r} != re-derived {value!r}")


def _check_cited_entry(entry: Mapping[str, Any], source: Mapping[str, Any]) -> None:
    entry_id = entry["id"]
    if set(source) != {"path", "commit", "token"}:
        fail(f"entry {entry_id} cited source must hold exactly path, commit and token")
    if entry_id not in CITED_TABLE:
        fail(f"entry {entry_id} is not in the verifier's cited table")
    path, commit, token = CITED_TABLE[entry_id]
    if (
        source["path"] != path
        or source["commit"] != commit
        or source["token"] != token
    ):
        fail(f"entry {entry_id} citation {dict(source)!r} != the table's")
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        fail(f"entry {entry_id} commit {commit!r} is not a 40-hex commit")
    head = _git("rev-parse", "HEAD")
    head_sha = head.stdout.strip()
    if head.returncode != 0 or not head_sha:
        fail(f"cannot resolve HEAD: {head.stderr.strip()}")
    if not is_ancestor(commit, head_sha):
        fail(f"entry {entry_id} commit {commit} is not an ancestor of HEAD {head_sha}")
    shown = _git("show", f"{commit}:{path}")
    if shown.returncode != 0:
        fail(f"cannot read {path} at {commit}: {shown.stderr.strip()}")
    if token not in shown.stdout:
        fail(
            f"entry {entry_id} token {token!r} does not occur verbatim in "
            f"{path} at {commit}"
        )


def _check_weights_digest(
    arm_id: str, state: str, cache: Optional[dict[tuple[str, str], bool]] = None
) -> None:
    """The weights file is tracked, clean and matches the record's SHA-256."""
    key = (arm_id, state)
    if cache is not None and key in cache:
        return
    record = _load_record(arm_id)
    recorded = _field(record, f"states.{state}.weights")
    weights_rel = _weights_rel(arm_id, state)
    if recorded.get("file") != f"{state}.weights":
        fail(f"{arm_id} {state} record names weights file {recorded.get('file')!r}")
    if not is_tracked(weights_rel) or not is_clean(weights_rel):
        fail(f"weights {weights_rel} is not tracked and clean")
    disk = sha256_file(repo_path(weights_rel, what=f"weights {arm_id} {state}"))
    if disk != recorded.get("sha256"):
        fail(
            f"weights SHA-256 {disk} != recorded {recorded.get('sha256')} "
            f"for {arm_id} {state}"
        )
    if cache is not None:
        cache[key] = True


def _check_rederived_entry(
    entry: Mapping[str, Any],
    source: Mapping[str, Any],
    cache: Optional[dict[tuple[str, str], bool]] = None,
) -> None:
    entry_id = entry["id"]
    if set(source) != {"record", "weights", "state"}:
        fail(
            f"entry {entry_id} rederived source must hold exactly record, weights and state"
        )
    const = CPU_CONST.fullmatch(entry_id)
    if const is not None:
        system = const.group("system")
        if system not in CPU_SYSTEMS:
            fail(f"entry {entry_id} names a system outside the panel: {system}")
        arm_id = f"r1-{system}"
        if source["state"] != "adam":
            fail(f"entry {entry_id} source state {source['state']!r} != 'adam'")
        if source["record"] != _record_rel(arm_id):
            fail(
                f"entry {entry_id} source record {source['record']!r} "
                "is not the system's Rung-1 record"
            )
        if source["weights"] != _weights_rel(arm_id, "adam"):
            fail(
                f"entry {entry_id} source weights {source['weights']!r} "
                "is not the system's adam weights"
            )
        _check_weights_digest(arm_id, "adam", cache)
        return
    match = CPU_ENTRY.fullmatch(entry_id)
    if match is None:
        fail(f"entry {entry_id} is not a cpu.<arm>.<state>.<field> id")
    arm_id, state = match.group("arm"), match.group("state")
    if arm_id not in EXPECTED_ARMS:
        fail(f"entry {entry_id} names an arm that did not run: {arm_id}")
    if match.group("field") not in CPU_FIELDS:
        fail(f"entry {entry_id} names an unknown cpu field {match.group('field')!r}")
    if source["state"] != state:
        fail(f"entry {entry_id} source state {source['state']!r} != {state!r}")
    if source["record"] != _record_rel(arm_id):
        fail(f"entry {entry_id} source record {source['record']!r} is not the arm's record")
    if source["weights"] != _weights_rel(arm_id, state):
        fail(f"entry {entry_id} source weights {source['weights']!r} is not the arm's weights")
    _check_weights_digest(arm_id, state, cache)


def _check_entry(
    entry: Mapping[str, Any],
    facts: Mapping[str, Any],
    digest_cache: Optional[dict[tuple[str, str], bool]] = None,
) -> None:
    entry_id = entry["id"]
    missing = ENTRY_KEYS - set(entry)
    extra = set(entry) - ENTRY_KEYS
    if missing:
        fail(f"entry {entry_id} lacks keys {sorted(missing)!r}")
    if extra:
        fail(f"entry {entry_id} holds unknown keys {sorted(extra)!r}")
    label = entry["label"]
    if label not in NUMBERS_LABELS:
        fail(f"entry {entry_id} has unknown label {label!r}")
    rule = entry["render_rule"]
    if rule not in NUMBERS_RULES:
        fail(f"entry {entry_id} has unknown render_rule {rule!r}")
    required = entry["required_in"]
    if not isinstance(required, list):
        fail(f"entry {entry_id} required_in is not a list")
    unknown = set(required) - {"verdict", "charter"}
    if unknown:
        fail(f"entry {entry_id} is required in unknown documents {sorted(unknown)!r}")
    if len(set(required)) != len(required):
        fail(f"entry {entry_id} repeats a required_in document")
    derivation = entry["derivation"]
    if not isinstance(derivation, str) or not derivation.strip():
        fail(f"entry {entry_id} has no derivation")
    rendered = render_number(entry["value"], rule)
    if entry["render"] != rendered:
        fail(f"entry {entry_id} render {entry['render']!r} != re-rendered {rendered!r}")
    source = entry["source"]
    if not isinstance(source, Mapping):
        fail(f"entry {entry_id} source is not an object")
    if label in {"official-mps-float32", "committed-record"}:
        _check_record_entry(entry, source, facts)
    elif label == "arithmetic":
        _check_arithmetic_entry(entry, source, facts)
    elif label == "cited":
        _check_cited_entry(entry, source)
    else:
        _check_rederived_entry(entry, source, digest_cache)


def check_numbers(
    payload: Any, *, facts: Optional[Mapping[str, Any]] = None
) -> None:
    """Re-derive every entry of the manifest with the verifier's own tables.

    ``facts`` exists so a test can inject a mutated in-memory copy of the
    committed files without touching the repository; the mode always passes
    nothing and reads the real files.
    """
    loaded = _facts() if facts is None else facts
    if not isinstance(payload, Mapping):
        fail("numbers.json is not an object")
    if payload.get("schema") != NUMBERS_SCHEMA:
        fail(f"numbers.json schema {payload.get('schema')!r} != {NUMBERS_SCHEMA!r}")
    plain = payload.get("plain_language")
    if not isinstance(plain, str) or not plain.strip():
        fail("numbers.json plain_language is not a non-empty sentence")
    if "\n" in plain:
        fail("numbers.json plain_language is not one sentence on one line")

    producer = payload.get("producer_sha256")
    if not isinstance(producer, Mapping) or not producer:
        fail("numbers.json producer_sha256 is not a non-empty mapping")
    if PRODUCER_REL not in producer:
        fail(f"numbers.json producer_sha256 does not name {PRODUCER_REL}")
    for relative, digest in producer.items():
        _check_current_file(relative, digest, what=f"producer module {relative}")

    for key, relative in (
        ("scorecard_sha256", SCORECARD_ARTIFACT_REL.as_posix()),
        ("handoff_sha256", HANDOFF_REL.as_posix()),
    ):
        _check_current_file(relative, payload.get(key), what=f"numbers.json {key}")
    if payload.get("handoff_sha256") != HANDOFF_SHA256:
        fail(
            "numbers.json handoff_sha256 "
            f"{payload.get('handoff_sha256')!r} != the sealed {HANDOFF_SHA256}"
        )

    inputs = payload.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        fail("numbers.json inputs is not a non-empty list")
    paths = [
        _check_citation(entry, what=f"numbers.json inputs[{index}]")
        for index, entry in enumerate(inputs)
    ]
    if paths != sorted(paths):
        fail("numbers.json inputs are not sorted by path")
    if len(set(paths)) != len(paths):
        fail("numbers.json inputs name a path twice")

    attestation = payload.get("attestation")
    if not isinstance(attestation, Mapping):
        fail("numbers.json attestation is not an object")
    if attestation.get("schema") != "phase59-files-opened/v1":
        fail(
            "numbers.json attestation schema "
            f"{attestation.get('schema')!r} != 'phase59-files-opened/v1'"
        )

    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        fail("numbers.json entries is not a non-empty list")
    ids = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            fail("a numbers.json entry is not an object")
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            fail(f"a numbers.json entry has no id: {entry!r}")
        ids.append(entry_id)
    if ids != sorted(ids):
        fail(f"numbers.json entries are not sorted by id: {ids!r}")
    if len(set(ids)) != len(ids):
        fail("numbers.json holds a duplicate entry id")
    facts = dict(loaded)
    facts["manifest"] = {entry["id"]: entry["value"] for entry in entries}
    facts["attestation"] = attestation
    digest_cache: dict[tuple[str, str], bool] = {}
    for entry in entries:
        _check_entry(entry, facts, digest_cache)


def cmd_numbers(_args: argparse.Namespace) -> None:
    """The manifest: schema, tables, citations, renders and current digests."""
    payload = load_json(repo_path(NUMBERS_REL, what="numbers.json"), what="numbers.json")
    check_numbers(payload)
    print(f"entries {len(payload['entries'])}")
    print("NUMBERS-OK")


def _check_attestation_summary(summary: Any, *, what: str = "the open attestation") -> None:
    """Every counter of an open-attestation summary must be zero."""
    if not isinstance(summary, Mapping):
        fail(f"{what} summary is not an object")
    if summary.get("schema") != "phase59-files-opened/v1":
        label = "open attestation schema" if what == "the open attestation" else f"{what} schema"
        fail(f"{label} {summary.get('schema')!r} is not phase59-files-opened/v1")
    opened = summary.get("opened")
    if not isinstance(opened, Mapping):
        fail(f"{what} has no opened block")
    for name, value in (
        ("test_split_opened", summary.get("test_split_opened")),
        ("opened.validation", opened.get("validation")),
        ("opened.other_under_root", opened.get("other_under_root")),
        ("blocked_attempts", summary.get("blocked_attempts")),
        ("refused_before_open", summary.get("refused_before_open")),
    ):
        if value != 0:
            fail(f"{what} shows {name} {value!r}, not 0")


def _check_open_attestation(ctx: Any) -> None:
    """The open attestation must show every counter at zero."""
    attestation = getattr(ctx, "attestation", None)
    if attestation is None:
        fail("the real context carries no open attestation")
    _check_attestation_summary(attestation.summary())


def rederive_constant_error(ref: Any, inner_pair: Any) -> tuple[Any, Any]:
    """Each body held at its time-mean position, scored with the frozen scorer.

    The verifier's own copy of the constant predictor: it learns nothing and
    returns ``(e_sys, e_in)``, one value per scored time.
    """
    import numpy as np

    from pinn.verification.feasibility_scorer import position_errors

    reference = np.asarray(ref, dtype=np.float64)
    constant = np.broadcast_to(reference.mean(axis=0, keepdims=True), reference.shape)
    e_sys, e_in, _r_sys = position_errors(constant, reference, inner_pair)
    return np.asarray(e_sys, dtype=np.float64), np.asarray(e_in, dtype=np.float64)


def _deviation(positions: Any) -> float:
    """RMS deviation about the series' own time mean, all bodies and coordinates."""
    import numpy as np

    array = np.asarray(positions, dtype=np.float64)
    centered = array - array.mean(axis=0, keepdims=True)
    return float(np.sqrt((centered ** 2).sum(axis=(1, 2)).mean()))


def timevar_ratio(pos: Any, ref: Any) -> float:
    """The output's time variation over the real orbit's own time variation."""
    return _deviation(pos) / _deviation(ref)


def rms_ratio(pos: Any, ref: Any) -> float:
    """The output's RMS error over the orbit's RMS deviation about its own mean."""
    import numpy as np

    predicted = np.asarray(pos, dtype=np.float64)
    reference = np.asarray(ref, dtype=np.float64)
    error = float(np.sqrt(((predicted - reference) ** 2).sum(axis=(1, 2)).mean()))
    return error / _deviation(reference)


def rederive_state(
    ctx: Any, card: Any, arm_id: str, state: str, *, arm_data: Any = None
) -> dict[str, Any]:
    """The verifier's own CPU float64 re-score of one committed weights file.

    Independent of the producer's ``derive_state``: it reads the record, checks
    the weights SHA-256 against it before ``torch.load`` with
    ``weights_only=True``, builds the CPU float64 network at the record's
    ``first_omega_0``, and scores the gold reference through the frozen scorer.

    ``arm_data`` lets a caller share one frozen data load across the states of
    an arm, and across arms of one system (they share a reference).
    """
    from collections import OrderedDict

    import numpy as np
    import torch

    from pinn.architecture_spec import ArchitectureSpec
    from pinn.network import build_network
    from pinn.verification.diagnostic_architecture import build_network_with_first_omega
    from pinn.verification.feasibility_scorer import network_trajectory, position_errors
    from pinn.verification.learnability_arms import SEED, arm_spec
    from pinn.verification.learnability_data import load_arm_data
    from pinn.verification.learnability_run import _float32_rounded

    if arm_id not in EXPECTED_ARMS:
        fail(f"{arm_id} is not an arm that ran")
    if state not in {"adam", "polish"}:
        fail(f"unknown state {state!r} for arm {arm_id}")
    record = _load_record(arm_id)
    recorded = _field(record, f"states.{state}.weights")
    weights_rel = _weights_rel(arm_id, state)
    if recorded.get("file") != f"{state}.weights":
        fail(f"{arm_id} {state} record names weights file {recorded.get('file')!r}")
    if not is_tracked(weights_rel) or not is_clean(weights_rel):
        fail(f"weights {weights_rel} is not tracked and clean")
    weights_path = repo_path(weights_rel, what=f"weights {arm_id} {state}")
    if not weights_path.is_file():
        fail(f"weights file is missing: {weights_rel}")
    disk = sha256_file(weights_path)
    if disk != recorded.get("sha256"):
        fail(
            f"weights SHA-256 {disk} != recorded {recorded.get('sha256')} "
            f"for {arm_id} {state}"
        )
    weights = torch.load(weights_path, map_location="cpu", weights_only=True)
    if not isinstance(weights, Mapping):
        fail(f"weights file {weights_rel} is not a mapping")
    widened = OrderedDict(
        (name, tensor.detach().to("cpu").to(torch.float64))
        for name, tensor in weights.items()
    )
    first_omega_0 = float(record["first_omega_0"])
    if abs(first_omega_0 - 30.0) < 1e-9:
        model = build_network(
            ArchitectureSpec(seed=SEED), dtype=torch.float64, device="cpu"
        )
    else:
        model = build_network_with_first_omega(
            first_omega_0, seed=SEED, dtype=torch.float64, device="cpu"
        )
    model.load_state_dict(widened)
    if arm_data is None:
        arm_data = load_arm_data(
            arm_spec(arm_id), ctx, scorecard=card, dtype=torch.float32, device="cpu"
        )
    pos, _velocities = network_trajectory(
        model,
        _float32_rounded(arm_data.ic13),
        _float32_rounded(arm_data.masses),
        arm_data.score.times,
        dtype=torch.float64,
        device=torch.device("cpu"),
    )
    ref = np.asarray(arm_data.score.positions, dtype=np.float64)
    e_sys, e_in, _r_sys = position_errors(pos, ref, arm_data.score.inner_pair)
    return {
        "pos": pos,
        "ref": ref,
        "times": np.asarray(arm_data.score.times, dtype=np.float64),
        "inner_pair": tuple(arm_data.score.inner_pair),
        "e_sys": np.asarray(e_sys, dtype=np.float64),
        "e_in": np.asarray(e_in, dtype=np.float64),
    }


def cpu_value(entry_id: str, derived: Mapping[str, Any], tier1_max: float) -> Any:
    """One re-derived field of a ``cpu.<arm>.<state>.<field>`` entry."""
    import numpy as np

    from pinn.verification.feasibility_scorer import tier_defining_error

    match = CPU_ENTRY.fullmatch(entry_id)
    if match is None:
        fail(f"{entry_id} is not a cpu.<arm>.<state>.<field> id")
    field = match.group("field")
    if field not in CPU_FIELDS:
        fail(f"{entry_id} names an unknown cpu field {field!r}")
    e_sys = np.asarray(derived["e_sys"], dtype=np.float64)
    e_in = np.asarray(derived["e_in"], dtype=np.float64)
    error = np.maximum(e_sys, e_in)
    if field == "E":
        return float(tier_defining_error(e_sys, e_in))
    if field == "e_sys_t0":
        return float(e_sys[0])
    if field == "e_in_t0":
        return float(e_in[0])
    if field == "best_moment":
        return float(error.min())
    if field == "n_within_tier1":
        return int(np.count_nonzero(error <= tier1_max))
    if field == "n_times":
        return int(len(derived["times"]))
    if field == "timevar_ratio":
        return timevar_ratio(derived["pos"], derived["ref"])
    return rms_ratio(derived["pos"], derived["ref"])


def _compare_rederived(entry_id: str, recorded: Any, value: Any) -> None:
    """Exact for integers, within 1e-12 for floats (the plan's tolerance)."""
    if isinstance(value, int) and not isinstance(value, bool):
        if recorded != value:
            fail(f"entry {entry_id} value {recorded!r} != re-derived {value!r}")
        return
    if isinstance(recorded, bool) or not isinstance(recorded, (int, float)):
        fail(f"entry {entry_id} value {recorded!r} is not a number")
    if abs(float(recorded) - float(value)) > 1e-12:
        fail(
            f"entry {entry_id} value {recorded!r} != re-derived {value!r} "
            "beyond 1e-12"
        )


def cmd_derive(_args: argparse.Namespace) -> None:
    """Re-derive every rederived-cpu-float64 entry from the committed weights."""
    import os

    try:
        import torch

        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification.feasibility_scorer import tier_defining_error
        from pinn.verification.learnability_arms import arm_spec
        from pinn.verification.learnability_data import load_arm_data, open_real_context
    except Exception as exc:  # noqa: BLE001 - fail-closed CLI
        fail(f"cannot import the CPU re-derivation: {exc}")

    os.chdir(REPO_ROOT)
    payload = load_json(repo_path(NUMBERS_REL, what="numbers.json"), what="numbers.json")
    if payload.get("schema") != NUMBERS_SCHEMA:
        fail(f"numbers.json schema {payload.get('schema')!r} != {NUMBERS_SCHEMA!r}")
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        fail("numbers.json entries is not a non-empty list")

    torch.set_num_threads(1)
    card = load_scorecard()
    tier1_max = _tier1_max(card)
    ctx = open_real_context(repo_root=REPO_ROOT)
    _check_open_attestation(ctx)

    data: dict[Any, Any] = {}

    def arm_data_for(arm_id: str) -> Any:
        system = arm_spec(arm_id).score_key.id
        if system not in data:
            data[system] = load_arm_data(
                arm_spec(arm_id),
                ctx,
                scorecard=card,
                dtype=torch.float32,
                device="cpu",
            )
        return data[system]

    states: dict[tuple[str, str], Mapping[str, Any]] = {}
    for arm_id in EXPECTED_ARMS:
        for state in CPU_STATES:
            states[(arm_id, state)] = rederive_state(
                ctx, card, arm_id, state, arm_data=arm_data_for(arm_id)
            )

    constants: dict[str, float] = {}
    for system in CPU_SYSTEMS:
        reference = states[(f"r1-{system}", "adam")]
        e_sys, e_in = rederive_constant_error(
            reference["ref"], reference["inner_pair"]
        )
        constants[system] = float(tier_defining_error(e_sys, e_in))

    fresh: dict[str, Any] = {}
    for (arm_id, state), derived in states.items():
        for field in CPU_FIELDS:
            entry_id = f"cpu.{arm_id}.{state}.{field}"
            fresh[entry_id] = cpu_value(entry_id, derived, tier1_max)
    for system, value in constants.items():
        fresh[f"cpu.const.{system}.E"] = value

    checked = 0
    for entry in entries:
        if not isinstance(entry, Mapping):
            fail("a numbers.json entry is not an object")
        if entry.get("label") != "rederived-cpu-float64":
            continue
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or entry_id not in fresh:
            fail(f"entry {entry_id!r} is not a cpu entry the verifier can re-derive")
        _compare_rederived(entry_id, entry.get("value"), fresh[entry_id])
        checked += 1

    facts = dict(_facts())
    facts["manifest"] = fresh
    facts["attestation"] = ctx.attestation.summary()
    table = arithmetic_table(facts)
    for entry in entries:
        if not isinstance(entry, Mapping):
            fail("a numbers.json entry is not an object")
        if entry.get("label") != "arithmetic":
            continue
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not (
            entry_id.startswith("cpu.") or entry_id.startswith("const_gap.")
        ):
            continue
        if entry_id not in table:
            fail(f"entry {entry_id} is not in the verifier's arithmetic table")
        name, formula = table[entry_id]
        source = entry.get("source")
        if not isinstance(source, Mapping) or source.get("formula") != name:
            fail(f"entry {entry_id} does not name the verifier's formula {name!r}")
        _compare_rederived(entry_id, entry.get("value"), formula())
        checked += 1

    if checked == 0:
        fail("numbers.json holds no rederived-cpu-float64 entry")
    _check_open_attestation(ctx)
    print(f"cpu entries {checked}")
    print("DERIVE-OK")


# ---------------------------------------------------------------------------
# The figure (64-03): independent re-derivation, byte regeneration and parsing.
# ---------------------------------------------------------------------------


def _canonical_bytes(payload: Any) -> bytes:
    """The verifier's own canonical JSON bytes (the evidence writer's format)."""
    return (
        json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def _r10(value: Any) -> float:
    """A plain Python float rounded to the ten decimals the series records."""
    return round(float(value), 10)


def _figure_payload(
    derived: Mapping[str, Any],
    e_sys_const: Any,
    e_in_const: Any,
    tier1_max: float,
    attestation: Mapping[str, Any],
) -> dict[str, Any]:
    """Assemble the plotted series in the producer's key order and rounding."""
    import numpy as np

    ref = np.asarray(derived["ref"], dtype=np.float64)
    pos = np.asarray(derived["pos"], dtype=np.float64)
    times = np.asarray(derived["times"], dtype=np.float64)
    mean = ref.mean(axis=0)
    err_net = np.maximum(
        np.asarray(derived["e_sys"], dtype=np.float64),
        np.asarray(derived["e_in"], dtype=np.float64),
    )
    err_const = np.maximum(
        np.asarray(e_sys_const, dtype=np.float64),
        np.asarray(e_in_const, dtype=np.float64),
    )
    series = {
        "arm": FIGURE_ARM,
        "state": FIGURE_STATE,
        "times": [_r10(value) for value in times],
        "ref_xy": [
            [[_r10(point[0]), _r10(point[1])] for point in ref[:, body, :]]
            for body in range(3)
        ],
        "pred_xy": [
            [[_r10(point[0]), _r10(point[1])] for point in pos[:, body, :]]
            for body in range(3)
        ],
        "mean_xy": [[_r10(mean[body][0]), _r10(mean[body][1])] for body in range(3)],
        "err_net": [_r10(value) for value in err_net],
        "err_const": [_r10(value) for value in err_const],
        "tier1": _r10(tier1_max),
        "attestation": dict(attestation),
    }
    count = len(series["times"])
    if count < 2:
        fail(f"the re-derived series holds {count} times, fewer than 2")
    for key in ("ref_xy", "pred_xy"):
        if len(series[key]) != 3 or any(len(body) != count for body in series[key]):
            fail(f"the re-derived series {key} does not hold three tracks of {count} times")
    for key in ("err_net", "err_const"):
        if len(series[key]) != count:
            fail(f"the re-derived series {key} length differs from times")
    return series


def _figure_series(ctx: Any, card: Any) -> dict[str, Any]:
    """The verifier's own plotted series for r1-1632's official state.

    It calls ``rederive_state`` and ``rederive_constant_error`` from 64-02, never
    the producer's ``derive_state`` or ``constant_predictor_error``.
    """
    import torch

    from pinn.verification.learnability_arms import arm_spec
    from pinn.verification.learnability_data import load_arm_data

    arm_data = load_arm_data(
        arm_spec(FIGURE_ARM), ctx, scorecard=card, dtype=torch.float32, device="cpu"
    )
    derived = rederive_state(ctx, card, FIGURE_ARM, FIGURE_STATE, arm_data=arm_data)
    e_sys_const, e_in_const = rederive_constant_error(
        derived["ref"], derived["inner_pair"]
    )
    attestation = getattr(ctx, "attestation", None)
    if attestation is None:
        fail("the real context carries no open attestation")
    return _figure_payload(
        derived, e_sys_const, e_in_const, _tier1_max(card), attestation.summary()
    )


def _figure_series_digest(series: Mapping[str, Any]) -> str:
    """SHA-256 of the canonical plotted series, without the attestation."""
    payload = {key: value for key, value in series.items() if key != "attestation"}
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _load_figure_producer() -> Any:
    """Import the committed figure producer by path, never by package name."""
    import importlib.util

    path = repo_path(FIGURE_PRODUCER_REL, what="figure producer")
    spec = importlib.util.spec_from_file_location("build_phase64_figure", path)
    if spec is None or spec.loader is None:
        fail(f"cannot import the figure producer {FIGURE_PRODUCER_REL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _check_svg_document(svg_text: str, *, required_ids: Sequence[str]) -> None:
    """Parse the SVG: viewBox, text and polyline bounds, no script or href."""
    import xml.etree.ElementTree as ElementTree

    try:
        root = ElementTree.fromstring(svg_text)
    except ElementTree.ParseError as exc:
        fail(f"the figure SVG is not well-formed XML: {exc}")
    view = root.get("viewBox")
    if view is None:
        fail("the figure SVG has no viewBox")
    parts = view.replace(",", " ").split()
    if len(parts) != 4:
        fail(f"the figure SVG viewBox {view!r} does not hold four numbers")
    try:
        min_x, min_y, width, height = (float(part) for part in parts)
    except ValueError:
        fail(f"the figure SVG viewBox {view!r} does not hold four numbers")
    if width <= 0.0 or height <= 0.0:
        fail(f"the figure SVG viewBox {view!r} has no area")
    max_x, max_y = min_x + width, min_y + height

    found: set[str] = set()
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "script":
            fail("the figure SVG holds a script element")
        for name in element.attrib:
            if name.rsplit("}", 1)[-1] == "href":
                fail("the figure SVG holds an href attribute")
        element_id = element.get("id")
        if element_id:
            found.add(element_id)
        if tag == "text":
            x_raw, y_raw = element.get("x"), element.get("y")
            if x_raw is None or y_raw is None:
                fail("a figure text element has no x or y")
            try:
                x, y = float(x_raw), float(y_raw)
            except ValueError:
                fail(
                    f"a figure text element has a non-numeric position "
                    f"{x_raw!r},{y_raw!r}"
                )
            if not (min_x <= x <= max_x and min_y <= y <= max_y):
                fail(f"a figure text element at {x:.1f},{y:.1f} lies outside the viewBox")
        elif tag == "polyline":
            points = element.get("points")
            if not points:
                fail("a figure polyline has no points")
            for pair in points.split():
                if pair.count(",") != 1:
                    fail(f"a figure polyline point {pair!r} is not x,y")
                x_raw, y_raw = pair.split(",", 1)
                try:
                    x, y = float(x_raw), float(y_raw)
                except ValueError:
                    fail(f"a figure polyline point {pair!r} is not numeric")
                if not (min_x <= x <= max_x and min_y <= y <= max_y):
                    fail(
                        f"a figure polyline point at {x:.1f},{y:.1f} lies outside "
                        "the viewBox"
                    )
    for required in required_ids:
        if required not in found:
            fail(f"the figure SVG has no group with id {required!r}")


def _check_figure_provenance(payload: Any, svg_path: Path) -> None:
    """Schema, figure digest, input digests, producer digests and fixed fields."""
    if not isinstance(payload, Mapping):
        fail("the figure provenance is not an object")
    if payload.get("schema") != FIGURE_SCHEMA:
        fail(f"the figure provenance schema {payload.get('schema')!r} != {FIGURE_SCHEMA!r}")

    figure = payload.get("figure")
    if not isinstance(figure, Mapping):
        fail("the figure provenance holds no figure block")
    if figure.get("path") != FIGURE_REL.as_posix():
        fail(
            f"the figure provenance path {figure.get('path')!r} != "
            f"{FIGURE_REL.as_posix()!r}"
        )
    digest = sha256_file(svg_path)
    if figure.get("sha256") != digest:
        fail(
            f"the figure SVG SHA-256 {digest} != recorded {figure.get('sha256')!r}"
        )

    inputs = payload.get("inputs")
    if not isinstance(inputs, list) or len(inputs) != len(FIGURE_INPUTS):
        fail(
            f"the figure provenance names {len(inputs) if isinstance(inputs, list) else 'no'} "
            f"inputs, not {len(FIGURE_INPUTS)}"
        )
    recorded_inputs: dict[str, str] = {}
    for item in inputs:
        if not isinstance(item, Mapping):
            fail("a figure provenance input is not an object")
        path, item_digest = item.get("path"), item.get("sha256")
        if not isinstance(path, str) or not isinstance(item_digest, str):
            fail(f"a figure provenance input is malformed: {item!r}")
        if path in recorded_inputs:
            fail(f"the figure provenance names the input {path!r} twice")
        recorded_inputs[path] = item_digest
    if tuple(sorted(recorded_inputs)) != tuple(sorted(FIGURE_INPUTS)):
        fail(f"the figure provenance inputs {sorted(recorded_inputs)!r} != the four inputs")
    for path, item_digest in recorded_inputs.items():
        actual = sha256_file(repo_path(path, what="figure input"))
        if actual != item_digest:
            fail(f"the figure input {path} SHA-256 {actual} != recorded {item_digest}")

    producers = payload.get("producers")
    if not isinstance(producers, Mapping):
        fail("the figure provenance holds no producers block")
    if tuple(sorted(producers)) != tuple(sorted(FIGURE_PRODUCERS)):
        fail(f"the figure provenance producers {sorted(producers)!r} != the two scripts")
    for path, producer_digest in producers.items():
        actual = sha256_file(repo_path(path, what="figure producer"))
        if actual != producer_digest:
            fail(
                f"the figure producer {path} SHA-256 {actual} != recorded "
                f"{producer_digest}"
            )

    if payload.get("arm") != FIGURE_ARM:
        fail(f"the figure provenance arm {payload.get('arm')!r} != {FIGURE_ARM!r}")
    if payload.get("state") != FIGURE_STATE:
        fail(f"the figure provenance state {payload.get('state')!r} != {FIGURE_STATE!r}")
    if payload.get("precision") != FIGURE_PRECISION:
        fail(
            f"the figure provenance precision {payload.get('precision')!r} != "
            f"{FIGURE_PRECISION!r}"
        )
    versions = payload.get("versions")
    if not isinstance(versions, Mapping) or set(versions) != {"python", "numpy", "torch"}:
        fail("the figure provenance versions block is not python, numpy and torch")
    for name, value in versions.items():
        if not isinstance(value, str) or not value:
            fail(f"the figure provenance version {name} is not a non-empty string")
    if payload.get("data_root_source") != "git_common_dir_default":
        fail(
            "the figure provenance data_root_source "
            f"{payload.get('data_root_source')!r} != 'git_common_dir_default'"
        )
    _check_attestation_summary(
        payload.get("attestation"), what="the recorded attestation"
    )


def cmd_figure(_args: argparse.Namespace) -> None:
    """Re-derive the plotted series, regenerate the SVG and parse the document."""
    import os

    try:
        import torch

        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification.learnability_data import open_real_context
    except Exception as exc:  # noqa: BLE001 - fail-closed CLI
        fail(f"cannot import the CPU re-derivation: {exc}")

    os.chdir(REPO_ROOT)
    provenance_path = repo_path(FIGURE_PROVENANCE_REL, what="figure provenance")
    payload = load_json(provenance_path, what="figure provenance")
    svg_path = repo_path(FIGURE_REL, what="figure SVG")
    if not svg_path.is_file():
        fail(f"the figure SVG is missing: {FIGURE_REL.as_posix()}")
    _check_figure_provenance(payload, svg_path)

    record = load_json(
        repo_path(FIGURE_INPUTS[0], what="r1-1632 record"), what="r1-1632 record"
    )
    if record.get("better_state") != FIGURE_STATE:
        fail(
            f"r1-1632 better_state {record.get('better_state')!r} is not "
            f"{FIGURE_STATE!r}"
        )

    svg_text = svg_path.read_text(encoding="utf-8")
    home = str(Path.home())
    if home and home in svg_text:
        fail("the figure SVG contains the host home prefix")
    if home and home in provenance_path.read_text(encoding="utf-8"):
        fail("the figure provenance contains the host home prefix")
    _check_svg_document(svg_text, required_ids=FIGURE_GROUPS)

    torch.set_num_threads(1)
    card = load_scorecard()
    ctx = open_real_context(repo_root=REPO_ROOT)
    _check_open_attestation(ctx)
    series = _figure_series(ctx, card)
    digest = _figure_series_digest(series)
    recorded = payload.get("series_sha256")
    if digest != recorded:
        fail(f"the re-derived series SHA-256 {digest} != recorded {recorded!r}")
    producer = _load_figure_producer()
    regenerated = producer.render_svg(series)
    if regenerated.encode("utf-8") != svg_path.read_bytes():
        fail("the regenerated figure SVG differs from the committed bytes")
    print(f"figure times {len(series['times'])}")
    print("FIGURE-OK")


COMMANDS = {
    "inputs": cmd_inputs,
    "frozen": cmd_frozen,
    "traceability": cmd_traceability,
    "numbers": cmd_numbers,
    "derive": cmd_derive,
    "figure": cmd_figure,
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
