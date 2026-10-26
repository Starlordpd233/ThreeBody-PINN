"""Phase 64 verifier: real-worktree smokes and synthetic negative controls.

Every mode is proven on the real committed files before its synthetic tests are
trusted (64-RESEARCH Pattern 4: the Phase 60 verifier crashed on first real use
twice when mocks had the wrong shapes). The synthetic repositories hold byte
copies of the real records, never stand-ins.
"""

from __future__ import annotations

import ast
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import os
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
PHASE = ".planning/phases/64-feasibility-verdict"
EVIDENCE = f"{PHASE}/evidence"
P60 = ".planning/phases/60-single-system-learnability/evidence"
P59 = ".planning/phases/59-read-only-baseline-scorecard/evidence"
VERIFIER_PATH = ROOT / EVIDENCE / "verify_phase64_verdict.py"
PRODUCER_PATH = ROOT / EVIDENCE / "build_phase64_evidence.py"
FIGURE_PRODUCER_PATH = ROOT / EVIDENCE / "build_phase64_figure.py"
FIGURE_SVG_PATH = ROOT / EVIDENCE / "figure-1632.svg"
FIGURE_PROVENANCE_PATH = ROOT / EVIDENCE / "figure-1632.provenance.json"

# The four inputs the figure provenance names and the two producer scripts it
# hashes; the temporary figure repository holds byte copies of all six.
FIGURE_INPUT_RELS = (
    f"{P60}/arms/r1-1632/record.json",
    f"{P60}/arms/r1-1632/polish.weights",
    f"{P60}/g2/stop-handoff.json",
    "pinn/verification/artifacts/feasibility_scorecard_v1.json",
)
FIGURE_PRODUCER_RELS = (
    f"{EVIDENCE}/build_phase64_figure.py",
    f"{EVIDENCE}/build_phase64_evidence.py",
)

G2_FILES = (
    f"{P60}/g2/stop-handoff.json",
    f"{P60}/g2/g2-outcome.json",
    f"{P60}/g2/sweep-curve.json",
    f"{P60}/g2/skip-records.json",
)


def load_verifier():
    spec = importlib.util.spec_from_file_location("verify_phase64_verdict", VERIFIER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_producer():
    spec = importlib.util.spec_from_file_location(
        "build_phase64_evidence", PRODUCER_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_figure_producer():
    spec = importlib.util.spec_from_file_location(
        "build_phase64_figure", FIGURE_PRODUCER_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=False
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc


def init_repo(root: Path) -> None:
    _git(root, "init")
    _git(root, "config", "user.email", "phase64@example.com")
    _git(root, "config", "user.name", "phase64")
    # The 60-06 fixture race: background maintenance must not touch the fixture.
    _git(root, "config", "maintenance.auto", "false")
    _git(root, "config", "gc.auto", "0")


def commit_all(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-m", message)
    return _git(root, "rev-parse", "HEAD").stdout.strip()


def run_main(module, argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = module.main(argv)
    return code, stdout.getvalue(), stderr.getvalue()


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_bytes(root: Path, relative: str) -> Path:
    destination = root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes((ROOT / relative).read_bytes())
    return destination


class VerifierModuleTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()

    def test_module_constants(self):
        self.assertEqual(
            self.module.HANDOFF_SHA256,
            "7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5",
        )
        self.assertEqual(self.module.HANDOFF_SCHEMA, "phase60-stop-handoff/v1")
        self.assertEqual(len(self.module.EXPECTED_ARMS), 7)
        self.assertEqual(self.module.EXPECTED_ARMS[0], "r1-1632")
        self.assertEqual(self.module.EXPECTED_ARMS[-1], "g2s-1632-w480")
        self.assertEqual(len(self.module.FORBIDDEN_ARM_PREFIXES), 9)
        self.assertEqual(self.module.RUNG1_ARMS, ("r1-1632", "r1-851", "r1-4658"))

    def test_commands_and_parser(self):
        self.assertIn("inputs", self.module.COMMANDS)
        self.assertIn("frozen", self.module.COMMANDS)
        self.assertIn("traceability", self.module.COMMANDS)
        parser = self.module.build_parser()
        self.assertEqual(parser.parse_args(["inputs"]).command, "inputs")
        self.assertEqual(parser.parse_args(["frozen"]).command, "frozen")
        self.assertEqual(
            parser.parse_args(["traceability"]).command, "traceability"
        )

    def test_frozen_constants(self):
        self.assertEqual(
            self.module.PHASE_BASE, "1ebb1d9b0c89e678961a8764bbf27ac19cd9b2a9"
        )
        self.assertEqual(self.module.EXPECTED_PINNED_COUNT, 33)
        self.assertEqual(self.module.EXPECTED_PATHSPEC_COUNT, 45)
        self.assertEqual(len(self.module.SEALED_RELS), 8)
        self.assertEqual(len(self.module.FROZEN_TREES), 4)


class InputsRealTests(unittest.TestCase):
    """The mode on the real committed files, before any synthetic fixture."""

    def setUp(self):
        self.module = load_verifier()

    def test_real_worktree_prints_inputs_ok(self):
        code, out, err = run_main(self.module, ["inputs"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out.splitlines(), ["INPUTS-OK"])
        self.assertNotIn("FAIL-CLOSED", err)


class InputsSyntheticTests(unittest.TestCase):
    """Byte copies of the real records in a temporary git repository."""

    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        for relative in G2_FILES:
            copy_bytes(self.root, relative)
        for arm_id in self.module.EXPECTED_ARMS:
            copy_bytes(self.root, f"{P60}/arms/{arm_id}/record.json")

        commit_all(self.root, "setup inputs test")
        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    # -- helpers ---------------------------------------------------------

    def path(self, relative: str) -> Path:
        return self.root / relative

    def read_json(self, relative: str):
        return json.loads(self.path(relative).read_text(encoding="utf-8"))

    def write_json(self, relative: str, payload) -> None:
        self.path(relative).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def patch(self, name: str, value) -> None:
        patcher = mock.patch.object(self.module, name, value)
        patcher.start()
        self.addCleanup(patcher.stop)

    def resign_handoff(self, *, repin_basis: bool = False) -> None:
        """Re-pin the handoff's basis citations, then the handoff's own digest."""
        if repin_basis:
            handoff = self.read_json(f"{P60}/g2/stop-handoff.json")
            for entry in handoff["basis"]:
                entry["sha256"] = sha256_of(self.path(entry["path"]))
            self.write_json(f"{P60}/g2/stop-handoff.json", handoff)
        self.patch(
            "HANDOFF_SHA256", sha256_of(self.path(f"{P60}/g2/stop-handoff.json"))
        )

    def assert_fails_closed(self) -> str:
        code, out, err = run_main(self.module, ["inputs"])
        self.assertEqual(code, 1, f"expected failure, stdout: {out}")
        self.assertIn("verify_phase64_verdict FAIL-CLOSED:", err)
        return err

    # -- the passing case ------------------------------------------------

    def test_committed_copies_pass(self):
        code, out, err = run_main(self.module, ["inputs"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out.splitlines(), ["INPUTS-OK"])

    # -- tampering with the sealed handoff -------------------------------

    def test_changed_handoff_byte_fails(self):
        path = self.path(f"{P60}/g2/stop-handoff.json")
        path.write_bytes(path.read_bytes() + b"\n")
        commit_all(self.root, "append a byte to the handoff")
        err = self.assert_fails_closed()
        self.assertIn("SHA-256", err)

    def test_changed_record_byte_fails(self):
        path = self.path(f"{P60}/arms/r1-851/record.json")
        path.write_bytes(path.read_bytes() + b"\n")
        commit_all(self.root, "append a byte to a record")
        err = self.assert_fails_closed()
        self.assertIn("arms[1].record", err)

    def test_owner_answer_set_fails(self):
        handoff = self.read_json(f"{P60}/g2/stop-handoff.json")
        handoff["owner_answer"] = "go to the verdict"
        self.write_json(f"{P60}/g2/stop-handoff.json", handoff)
        self.resign_handoff()
        commit_all(self.root, "fill owner_answer")
        err = self.assert_fails_closed()
        self.assertIn("owner_answer", err)

    def test_verdict_note_set_fails(self):
        handoff = self.read_json(f"{P60}/g2/stop-handoff.json")
        handoff["verdict_note"] = "amended"
        self.write_json(f"{P60}/g2/stop-handoff.json", handoff)
        self.resign_handoff()
        commit_all(self.root, "fill verdict_note")
        err = self.assert_fails_closed()
        self.assertIn("verdict_note", err)

    def test_changed_verdict_with_patched_pin_fails(self):
        handoff = self.read_json(f"{P60}/g2/stop-handoff.json")
        handoff["verdict"]["reasons"] = ["the sweep rescued something"]
        self.write_json(f"{P60}/g2/stop-handoff.json", handoff)
        self.resign_handoff()
        commit_all(self.root, "alter the verdict reasons")
        err = self.assert_fails_closed()
        self.assertIn("re-derived", err)

    def test_changed_wall_hours_fails(self):
        handoff = self.read_json(f"{P60}/g2/stop-handoff.json")
        handoff["arms"][3]["wall_hours"] = handoff["arms"][3]["wall_hours"] + 1.0
        self.write_json(f"{P60}/g2/stop-handoff.json", handoff)
        self.resign_handoff()
        commit_all(self.root, "change one wall_hours")
        err = self.assert_fails_closed()
        self.assertIn("sum", err)

    # -- the rungs that did not run --------------------------------------

    def test_eighth_arm_directory_fails(self):
        arm = self.path(f"{P60}/arms/r2a-1632")
        arm.mkdir(parents=True)
        (arm / "record.json").write_text("{}\n", encoding="utf-8")
        commit_all(self.root, "add a rung 2a arm")
        err = self.assert_fails_closed()
        self.assertIn("later-rung", err)

    def test_removed_arm_directory_fails(self):
        for child in sorted(self.path(f"{P60}/arms/r1-851").iterdir()):
            child.unlink()
        self.path(f"{P60}/arms/r1-851").rmdir()
        commit_all(self.root, "remove one arm")
        self.assert_fails_closed()

    def test_rescue_json_fails(self):
        self.path(f"{P60}/g2/rescue.json").write_text('{"schema": "phase60-rescue/v1"}\n')
        commit_all(self.root, "add a rescue record")
        err = self.assert_fails_closed()
        self.assertIn("rescue", err)

    def test_continue_directory_fails(self):
        directory = self.path(f"{P60}/continue")
        directory.mkdir(parents=True)
        (directory / "README.md").write_text("continue\n", encoding="utf-8")
        commit_all(self.root, "add a continue directory")
        err = self.assert_fails_closed()
        self.assertIn("continue/", err)

    def test_checkpoint_four_ruling_fails(self):
        ruling = self.path(
            ".planning/phases/60-single-system-learnability/60-CHECKPOINT-4-RULING.md"
        )
        ruling.write_text("# ruling\n", encoding="utf-8")
        commit_all(self.root, "add a checkpoint four ruling")
        err = self.assert_fails_closed()
        self.assertIn("CHECKPOINT-4-RULING", err)

    def test_skip_reason_changed_fails(self):
        skip = self.read_json(f"{P60}/g2/skip-records.json")
        skip["entries"]["FEAS-04"]["reason"] = "no-rescue"
        self.write_json(f"{P60}/g2/skip-records.json", skip)
        commit_all(self.root, "change the skip reason")
        err = self.assert_fails_closed()
        self.assertIn("FEAS-04", err)

    def test_g2_tiers_changed_fails(self):
        outcome = self.read_json(f"{P60}/g2/g2-outcome.json")
        outcome["tiers"] = [0, 0, 1]
        self.write_json(f"{P60}/g2/g2-outcome.json", outcome)
        self.resign_handoff(repin_basis=True)
        commit_all(self.root, "change the g2 tiers")
        err = self.assert_fails_closed()
        self.assertIn("tiers", err)

    def test_sweep_outcome_changed_fails(self):
        curve = self.read_json(f"{P60}/g2/sweep-curve.json")
        curve["outcome"] = "rescued"
        self.write_json(f"{P60}/g2/sweep-curve.json", curve)
        self.resign_handoff(repin_basis=True)
        commit_all(self.root, "change the sweep outcome")
        err = self.assert_fails_closed()
        self.assertIn("no_rescue", err)


class FrozenRealTests(unittest.TestCase):
    """The mode on the real committed files."""

    def setUp(self):
        self.module = load_verifier()

    def test_real_worktree_prints_frozen_ok(self):
        code, out, err = run_main(self.module, ["frozen"])
        self.assertEqual(code, 0, err)
        self.assertEqual(
            out.splitlines(),
            ["frozen paths pinned=33 sealed=8 trees=4", "FROZEN-OK"],
        )
        self.assertNotIn("FAIL-CLOSED", err)


class FrozenSyntheticTests(unittest.TestCase):
    """Byte copies of the real frozen paths in a temporary git repository.

    The base is the fixture's own setup commit, so a change after it is a change
    after the phase base. The 33 pinned paths are read from run-protocol.json,
    never typed here.
    """

    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        for relative in self.module.SEALED_RELS:
            copy_bytes(self.root, relative)
        protocol = json.loads(
            (ROOT / f"{P60}/run-protocol.json").read_text(encoding="utf-8")
        )
        for relative in protocol["module_sha256"]:
            copy_bytes(self.root, relative)

        # One extra file under each frozen tree not already covered by a copy,
        # plus one P60 note and one STATE.md that sit inside and outside the
        # pathspecs respectively (the scope negative controls).
        specs = self.root / "pinn_instruction/markdown_conversion/framework-specs"
        specs.mkdir(parents=True, exist_ok=True)
        (specs / "ctl_instruction.md").write_text("# synthetic spec\n", encoding="utf-8")
        (self.root / "pinn" / "unpinned_note.txt").write_text("note\n", encoding="utf-8")
        (self.root / P60 / "scratch-note.txt").write_text("note\n", encoding="utf-8")
        state = self.root / ".planning/STATE.md"
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("# state\n", encoding="utf-8")

        self.base = commit_all(self.root, "setup frozen test")
        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        base_patcher = mock.patch.object(self.module, "PHASE_BASE", self.base)
        base_patcher.start()
        self.addCleanup(base_patcher.stop)

    def path(self, relative: str) -> Path:
        return self.root / relative

    def append_and_commit(self, relative: str, message: str) -> None:
        path = self.path(relative)
        path.write_bytes(path.read_bytes() + b"\n")
        commit_all(self.root, message)

    def assert_fails_closed(self) -> str:
        code, out, err = run_main(self.module, ["frozen"])
        self.assertEqual(code, 1, f"expected failure, stdout: {out}")
        self.assertIn("verify_phase64_verdict FAIL-CLOSED:", err)
        return err

    # -- the passing case ------------------------------------------------

    def test_clean_tree_passes(self):
        code, out, err = run_main(self.module, ["frozen"])
        self.assertEqual(code, 0, err)
        self.assertEqual(
            out.splitlines(),
            ["frozen paths pinned=33 sealed=8 trees=4", "FROZEN-OK"],
        )

    def test_committed_state_md_change_passes(self):
        # Scope negative control: the check is neither vacuous nor over-broad.
        self.append_and_commit(".planning/STATE.md", "move the state pointer")
        code, out, err = run_main(self.module, ["frozen"])
        self.assertEqual(code, 0, err)
        self.assertIn("FROZEN-OK", out)

    # -- changes inside the 45 pathspecs ---------------------------------

    def test_committed_change_to_sealed_file_fails(self):
        relative = (
            ".planning/phases/60-single-system-learnability/60-RUN-PROTOCOL.md"
        )
        self.append_and_commit(relative, "amend a sealed protocol doc")
        err = self.assert_fails_closed()
        self.assertIn(relative, err)

    def test_pinned_bytes_changed_fails(self):
        self.append_and_commit("pinn/network.py", "change a pinned module")
        err = self.assert_fails_closed()
        self.assertIn("pinned module pinn/network.py SHA-256", err)

    def test_uncommitted_edit_to_pinned_module_fails(self):
        path = self.path("pinn/constants.py")
        path.write_bytes(path.read_bytes() + b"\n")
        err = self.assert_fails_closed()
        self.assertIn("pinn/constants.py", err)
        self.assertIn("not tracked and clean", err)

    def test_uncommitted_edit_under_pinn_tree_fails(self):
        # A tracked file under pinn/ that no module_sha256 pin names: only the
        # git status gate can catch it, so this proves the gate itself.
        path = self.path("pinn/unpinned_note.txt")
        path.write_bytes(path.read_bytes() + b"\n")
        err = self.assert_fails_closed()
        self.assertIn("uncommitted or untracked", err)
        self.assertIn("pinn/unpinned_note.txt", err)

    def test_untracked_file_under_pinn_fails(self):
        (self.path("pinn") / "new_module.py").write_text("x = 1\n", encoding="utf-8")
        err = self.assert_fails_closed()
        self.assertIn("uncommitted or untracked", err)
        self.assertIn("pinn/new_module.py", err)

    def test_committed_change_under_p60_evidence_fails(self):
        relative = f"{P60}/scratch-note.txt"
        self.append_and_commit(relative, "change a P60 evidence note")
        err = self.assert_fails_closed()
        self.assertIn(relative, err)

    def test_committed_change_under_specs_fails(self):
        relative = "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
        self.append_and_commit(relative, "change a frozen spec")
        err = self.assert_fails_closed()
        self.assertIn(relative, err)

    # -- the shape of the frozen inputs ----------------------------------

    def test_short_module_map_fails(self):
        protocol_path = self.path(f"{P60}/run-protocol.json")
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        dropped = list(protocol["module_sha256"])[0]
        del protocol["module_sha256"][dropped]
        protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")
        commit_all(self.root, "drop one pinned module")
        err = self.assert_fails_closed()
        self.assertIn("exactly 33", err)

    def test_base_not_ancestor_fails(self):
        patcher = mock.patch.object(self.module, "PHASE_BASE", "0" * 40)
        patcher.start()
        self.addCleanup(patcher.stop)
        err = self.assert_fails_closed()
        self.assertIn("not an ancestor", err)


class FrozenArgvTests(unittest.TestCase):
    """The zsh-safe argument-count self-test of 64-VALIDATION.md Wave 0 (H4)."""

    def setUp(self):
        self.module = load_verifier()
        self.protocol = json.loads(
            (ROOT / f"{P60}/run-protocol.json").read_text(encoding="utf-8")
        )

    def test_real_pathspecs_are_45_in_three_parts(self):
        pathspecs = self.module.frozen_pathspecs(self.protocol["module_sha256"])
        self.assertEqual(len(pathspecs), 45)
        self.assertEqual(tuple(pathspecs[:8]), self.module.SEALED_RELS)
        self.assertEqual(
            pathspecs[8:41], list(self.protocol["module_sha256"]), "file order"
        )
        self.assertEqual(tuple(pathspecs[41:]), self.module.FROZEN_TREES)
        for entry in pathspecs:
            self.assertIsInstance(entry, str)
            self.assertTrue(entry)
            self.assertEqual(entry, entry.strip())
        self.assertEqual(len(set(pathspecs)), 45)

    def test_git_calls_receive_45_separate_argv_items(self):
        pathspecs = self.module.frozen_pathspecs(self.protocol["module_sha256"])
        calls: list[list[str]] = []
        real_run = subprocess.run

        def spy(command, *args, **kwargs):
            calls.append(list(command))
            return real_run(command, *args, **kwargs)

        with mock.patch("subprocess.run", side_effect=spy):
            code, out, err = run_main(self.module, ["frozen"])
        self.assertEqual(code, 0, err)
        self.assertIn("FROZEN-OK", out)

        diff_calls = [call for call in calls if call[:3] == ["git", "diff", "--quiet"]]
        status_calls = [
            call
            for call in calls
            if call[:4] == ["git", "status", "--porcelain", "--untracked-files=all"]
        ]
        self.assertEqual(len(diff_calls), 1, calls)
        self.assertEqual(len(status_calls), 1, calls)
        for call in (diff_calls[0], status_calls[0]):
            separator = call.index("--")
            self.assertEqual(call[separator + 1 :], pathspecs)

    def test_dropped_tree_fails(self):
        patcher = mock.patch.object(
            self.module, "FROZEN_TREES", self.module.FROZEN_TREES[:3]
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        with self.assertRaises(self.module.VerifyError) as raised:
            self.module.frozen_pathspecs(self.protocol["module_sha256"])
        self.assertIn("FROZEN_TREES must hold exactly 4", str(raised.exception))

    def test_empty_module_map_fails(self):
        with self.assertRaises(self.module.VerifyError) as raised:
            self.module.frozen_pathspecs([])
        self.assertIn("module_sha256 must hold exactly 33", str(raised.exception))

    def test_empty_sealed_entry_fails(self):
        patched = ("",) + tuple(self.module.SEALED_RELS[1:])
        patcher = mock.patch.object(self.module, "SEALED_RELS", patched)
        patcher.start()
        self.addCleanup(patcher.stop)
        with self.assertRaises(self.module.VerifyError) as raised:
            self.module.frozen_pathspecs(self.protocol["module_sha256"])
        self.assertIn("not a non-empty string", str(raised.exception))

    def test_duplicate_pathspec_fails(self):
        trees = self.module.FROZEN_TREES
        patched = (trees[0], trees[0], trees[2], trees[3])
        patcher = mock.patch.object(self.module, "FROZEN_TREES", patched)
        patcher.start()
        self.addCleanup(patcher.stop)
        with self.assertRaises(self.module.VerifyError) as raised:
            self.module.frozen_pathspecs(self.protocol["module_sha256"])
        self.assertIn("duplicates", str(raised.exception))


class TraceabilityRealTests(unittest.TestCase):
    """The mode on the real committed registries."""

    EXPECTED = [
        "defined 24",
        "table 24",
        "roadmap 24",
        "per-phase 59:5 60:4 61:8 62:2 63:2 64:3",
        "status Complete 7",
        "status Complete (recorded as skipped: no rescue) 2",
        "status Pending 15",
        "TRACEABILITY-OK",
    ]

    def setUp(self):
        self.module = load_verifier()

    def test_real_worktree_prints_traceability_ok(self):
        code, out, err = run_main(self.module, ["traceability"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out.splitlines(), self.EXPECTED)
        self.assertNotIn("FAIL-CLOSED", err)

    def test_two_runs_are_byte_identical(self):
        first = run_main(self.module, ["traceability"])
        second = run_main(self.module, ["traceability"])
        self.assertEqual(first[0], 0, first[2])
        self.assertEqual(first[1], second[1])


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(f"fixture anchor appears {text.count(old)} times: {old!r}")
    return text.replace(old, new)


class TraceabilityPureTests(unittest.TestCase):
    """String fixtures built from the real registries, one edit each."""

    def setUp(self):
        self.module = load_verifier()
        self.requirements = (ROOT / ".planning/REQUIREMENTS.md").read_text(
            encoding="utf-8"
        )
        self.roadmap = (ROOT / ".planning/ROADMAP.md").read_text(encoding="utf-8")
        self.project = (ROOT / ".planning/PROJECT.md").read_text(encoding="utf-8")

    def report(
        self,
        requirements: str | None = None,
        roadmap: str | None = None,
        project: str | None = None,
    ) -> dict:
        return self.module.traceability_report(
            self.requirements if requirements is None else requirements,
            self.roadmap if roadmap is None else roadmap,
            self.project if project is None else project,
        )

    def assert_fails(
        self,
        requirements: str | None = None,
        roadmap: str | None = None,
        project: str | None = None,
    ) -> str:
        with self.assertRaises(self.module.VerifyError) as raised:
            self.report(requirements, roadmap, project)
        return str(raised.exception)

    # -- the passing case ------------------------------------------------

    def test_real_files_report_24(self):
        report = self.report()
        self.assertEqual(len(report["defined"]), 24)
        self.assertEqual(len(report["table"]), 24)
        self.assertEqual(len(report["roadmap"]), 24)
        self.assertEqual(
            {phase: len(ids) for phase, ids in report["per_phase"].items()},
            {59: 5, 60: 4, 61: 8, 62: 2, 63: 2, 64: 3},
        )
        self.assertEqual(
            report["statuses"],
            {
                "Complete": 7,
                "Complete (recorded as skipped: no rescue)": 2,
                "Pending": 15,
            },
        )

    def test_creation_time_history_lines_do_not_count(self):
        self.assertIn("20/20 mapped at roadmap creation", self.roadmap)
        self.assertIn("20/20 requirements mapped at creation", self.roadmap)
        self.assertEqual(len(self.report()["defined"]), 24)

    def test_feas_1_and_feas_10_are_two_ids(self):
        # Exact-string comparison: FEAS-1 is not a prefix of FEAS-01 collapsed
        # onto it, and FEAS-10 is a different ID from FEAS-1.
        requirements = self.requirements.replace("FEAS-10", "FEAS-1")
        roadmap = self.roadmap.replace("FEAS-10", "FEAS-1")
        project = self.project.replace("FEAS-10", "FEAS-1")
        report = self.report(requirements, roadmap, project)
        self.assertIn("FEAS-01", report["defined"])
        self.assertIn("FEAS-1", report["defined"])
        self.assertEqual(len(report["defined"]), 24)

    # -- one edit each, every one must fail ------------------------------

    def test_dropped_table_row_fails(self):
        requirements = replace_once(
            self.requirements, "| DIAG-08 | Phase 63 | Pending |\n", ""
        )
        error = self.assert_fails(requirements=requirements)
        self.assertIn("disagree", error)
        self.assertIn("DIAG-08", error)

    def test_extra_definition_fails(self):
        requirements = replace_once(
            self.requirements,
            "## v2.4 Requirements\n",
            "## v2.4 Requirements\n\n- [ ] **FEAS-99**: a synthetic 25th requirement.\n",
        )
        error = self.assert_fails(requirements=requirements)
        self.assertIn("FEAS-99", error)

    def test_duplicate_table_row_fails(self):
        requirements = replace_once(
            self.requirements,
            "| FEAS-01 | Phase 59 | Complete |\n",
            "| FEAS-01 | Phase 59 | Complete |\n| FEAS-01 | Phase 59 | Complete |\n",
        )
        error = self.assert_fails(requirements=requirements)
        self.assertIn("holds FEAS-01 twice", error)

    def test_total_count_changed_fails(self):
        requirements = replace_once(
            self.requirements,
            "**Total:** 24 requirements",
            "**Total:** 25 requirements",
        )
        error = self.assert_fails(requirements=requirements)
        self.assertIn("**Total:**", error)
        self.assertIn("25 != 24", error)

    def test_duplicated_id_on_second_phase_fails(self):
        roadmap = replace_once(
            self.roadmap,
            "**Requirements**: RUN-06, DIAG-08",
            "**Requirements**: RUN-06, DIAG-08, GATE-05",
        )
        error = self.assert_fails(roadmap=roadmap)
        self.assertIn("GATE-05", error)
        self.assertIn("Phase 62", error)

    def test_deleted_phase_requirements_line_fails(self):
        roadmap = replace_once(
            self.roadmap,
            "**Requirements**: GATE-05, FEAS-05\n",
            "",
        )
        error = self.assert_fails(roadmap=roadmap)
        self.assertIn("Phase 62", error)
        self.assertIn("exactly one", error)

    def test_empty_requirements_line_fails(self):
        roadmap = replace_once(
            self.roadmap,
            "**Requirements**: GATE-05, FEAS-05",
            "**Requirements**:",
        )
        error = self.assert_fails(roadmap=roadmap)
        self.assertIn("Phase 62", error)
        self.assertIn("lists no requirement ID", error)

    def test_missing_phase_section_fails(self):
        start = self.roadmap.index("### Phase 62:")
        end = self.roadmap.index("### Phase 63:")
        roadmap = self.roadmap[:start] + self.roadmap[end:]
        error = self.assert_fails(roadmap=roadmap)
        self.assertIn("no '### Phase 62' section", error)

    def test_phase_outside_range_fails(self):
        requirements = replace_once(
            self.requirements,
            "| FEAS-06 | Phase 64 | Pending |",
            "| FEAS-06 | Phase 65 | Pending |",
        )
        roadmap = replace_once(
            self.roadmap,
            "**Requirements**: FEAS-06, FEAS-10, VER-22",
            "**Requirements**: FEAS-10, VER-22",
        )
        roadmap = roadmap + "\n### Phase 65: Synthetic\n\n**Requirements**: FEAS-06\n"
        error = self.assert_fails(requirements=requirements, roadmap=roadmap)
        self.assertIn("FEAS-06", error)
        self.assertIn("outside 59 to 64", error)

    def test_table_phase_differs_from_roadmap_phase_fails(self):
        requirements = replace_once(
            self.requirements,
            "| GATE-05 | Phase 62 | Pending |",
            "| GATE-05 | Phase 63 | Pending |",
        )
        error = self.assert_fails(requirements=requirements)
        self.assertIn("GATE-05", error)
        self.assertIn("table phase 63 != roadmap phase 62", error)

    def test_empty_inputs_fail(self):
        error = self.assert_fails(requirements="", roadmap="", project="")
        self.assertIn("exactly once", error)


class ManifestCase(unittest.TestCase):
    """Shared fixture: the real manifest, mutated in memory for negative controls.

    The real manifest is read once and every negative control mutates a deep copy
    of it in memory. ``cmd_numbers`` loads nothing but ``numbers.json``, so
    patching ``load_json`` for that one name exercises the same code path a
    temporary copy of the tree would, without a second checkout of the evidence
    tree (test-structure refinement, 64-01 deviation 3).
    """

    @classmethod
    def setUpClass(cls):
        cls.module = load_verifier()
        cls.payload = json.loads(
            (ROOT / EVIDENCE / "numbers.json").read_text(encoding="utf-8")
        )

    def mutated(self) -> dict:
        return json.loads(json.dumps(self.payload))

    def entry(self, payload: dict, entry_id: str) -> dict:
        for entry in payload["entries"]:
            if entry["id"] == entry_id:
                return entry
        raise AssertionError(f"{entry_id} is not in the manifest")

    def assert_rejected(self, payload: dict, needle: str) -> str:
        original = self.module.load_json

        def patched(path, *, what):
            if Path(path).name == "numbers.json":
                return payload
            return original(path, what=what)

        with mock.patch.object(self.module, "load_json", patched):
            code, _stdout, stderr = run_main(self.module, ["numbers"])
        self.assertEqual(code, 1, f"the mutated manifest passed: {stderr}")
        self.assertIn("FAIL-CLOSED", stderr)
        self.assertIn(needle, stderr)
        return stderr


class NumbersTracerTests(ManifestCase):
    """The tracer path: one entry of each kind, from its committed source and back."""

    def test_manifest_keeps_the_four_tracer_entries(self):
        self.assertEqual(self.payload["schema"], "phase64-numbers/v1")
        ids = {entry["id"] for entry in self.payload["entries"]}
        self.assertTrue(
            {
                "arm.r1-1632.E",
                "cpu.r1-1632.polish.E",
                "hours.total",
                "pub.kollias.energy_range",
            }
            <= ids
        )

    def test_labels_and_renders(self):
        entries = {entry["id"]: entry for entry in self.payload["entries"]}
        self.assertEqual(entries["arm.r1-1632.E"]["label"], "official-mps-float32")
        self.assertEqual(entries["arm.r1-1632.E"]["render"], "1.1574")
        self.assertEqual(entries["cpu.r1-1632.polish.E"]["label"], "rederived-cpu-float64")
        self.assertEqual(entries["cpu.r1-1632.polish.E"]["render"], "1.1600")
        self.assertEqual(entries["hours.total"]["label"], "arithmetic")
        self.assertEqual(entries["hours.total"]["render"], "22.378")
        self.assertEqual(entries["pub.kollias.energy_range"]["label"], "cited")
        self.assertEqual(entries["pub.kollias.energy_range"]["render"], "0.02\u20133%")
        for entry in entries.values():
            self.assertEqual(
                entry["render"], self.module.render_number(entry["value"], entry["render_rule"])
            )
            self.assertTrue(set(entry["required_in"]) <= {"verdict", "charter"})

    def test_official_entry_equals_the_recorded_result(self):
        record = json.loads(
            (ROOT / f"{P60}/arms/r1-1632/record.json").read_text(encoding="utf-8")
        )
        entry = self.entry(self.payload, "arm.r1-1632.E")
        self.assertEqual(entry["value"], record["result"]["E"])
        self.assertEqual(entry["source"]["key"], "result.E")
        self.assertEqual(
            entry["source"]["path"], f"{P60}/arms/r1-1632/record.json"
        )

    def test_hours_total_equals_the_sealed_total_exactly(self):
        handoff = json.loads(
            (ROOT / f"{P60}/g2/stop-handoff.json").read_text(encoding="utf-8")
        )
        entry = self.entry(self.payload, "hours.total")
        self.assertEqual(entry["value"], handoff["total_wall_hours"])
        self.assertEqual(entry["value"], 22.37828873402778)

    def test_hours_total_is_the_ordered_sum_of_the_seven_records(self):
        handoff = json.loads(
            (ROOT / f"{P60}/g2/stop-handoff.json").read_text(encoding="utf-8")
        )
        values = []
        for arm in handoff["arms"]:
            record = json.loads(
                (ROOT / f"{P60}/arms/{arm['arm_id']}/record.json").read_text(
                    encoding="utf-8"
                )
            )
            values.append(record["wall"]["hours"])
        total = self.entry(self.payload, "hours.total")["value"]
        self.assertEqual(total, self.module.ordered_sum(values))
        # The same pin as OrderedSumTests: math.fsum lands one ulp below.
        self.assertNotEqual(total, math.fsum(values))

    def test_cpu_entry_equals_the_records_cross_check_and_not_the_official_e(self):
        record = json.loads(
            (ROOT / f"{P60}/arms/r1-1632/record.json").read_text(encoding="utf-8")
        )
        entry = self.entry(self.payload, "cpu.r1-1632.polish.E")
        cross_check = record["states"]["polish"]["cross_check"]["E"]
        self.assertAlmostEqual(entry["value"], cross_check, delta=1e-12)
        self.assertNotEqual(entry["value"], record["result"]["E"])
        self.assertGreater(abs(entry["value"] - record["result"]["E"]), 1e-3)

    def test_cited_entry_pins_the_research_page(self):
        entry = self.entry(self.payload, "pub.kollias.energy_range")
        self.assertEqual(entry["value"], "0.02\u20133%")
        self.assertEqual(entry["source"]["token"], "to within \u223c 0.02\u20133%")
        self.assertEqual(entry["source"]["path"], f"{PHASE}/64-RESEARCH.md")
        self.assertRegex(entry["source"]["commit"], r"^[0-9a-f]{40}$")

    def test_manifest_has_no_home_directory_string(self):
        text = (ROOT / EVIDENCE / "numbers.json").read_text(encoding="utf-8")
        self.assertNotIn(str(Path.home()), text)
        self.assertNotIn("/Users/", text)

    def test_numbers_prints_its_token(self):
        code, stdout, stderr = run_main(self.module, ["numbers"])
        self.assertEqual(code, 0, stderr)
        self.assertIn("NUMBERS-OK", stdout.splitlines())

    def test_derive_prints_its_token(self):
        cwd = Path.cwd()
        try:
            code, stdout, stderr = run_main(self.module, ["derive"])
        finally:
            os.chdir(cwd)
        self.assertEqual(code, 0, stderr)
        self.assertIn("DERIVE-OK", stdout.splitlines())

    def test_changed_last_digit_of_the_official_e_fails(self):
        payload = self.mutated()
        entry = self.entry(payload, "arm.r1-1632.E")
        entry["value"] = 1.157387378319296
        # The render is unchanged, so only the record re-read can catch this.
        self.assertEqual(
            self.module.render_number(entry["value"], entry["render_rule"]), entry["render"]
        )
        self.assert_rejected(payload, "entry arm.r1-1632.E value")

    def test_cpu_entry_relabelled_as_official_fails(self):
        payload = self.mutated()
        self.entry(payload, "cpu.r1-1632.polish.E")["label"] = "official-mps-float32"
        # The relabelled entry is looked up in the committed-record table, where a
        # CPU re-derivation has no business being.
        self.assert_rejected(
            payload,
            "entry cpu.r1-1632.polish.E is not in the verifier's committed-record table",
        )

    def test_superseded_cited_token_fails(self):
        payload = self.mutated()
        self.entry(payload, "pub.kollias.energy_range")["source"][
            "token"
        ] = "to within \u223c 0.08\u20133%"
        self.assert_rejected(payload, "citation")

    def test_cited_token_absent_at_its_commit_fails(self):
        # The table itself is patched to the superseded figure so the run reaches
        # the verbatim-occurrence check: the phrase is not in the page at 7fda0a55.
        payload = self.mutated()
        self.entry(payload, "pub.kollias.energy_range")["source"][
            "token"
        ] = "to within \u223c 0.08\u20133%"
        superseded = {
            "pub.kollias.energy_range": (
                self.module.CITED_TABLE["pub.kollias.energy_range"][0],
                self.module.CITED_TABLE["pub.kollias.energy_range"][1],
                "to within \u223c 0.08\u20133%",
            )
        }
        with mock.patch.dict(self.module.CITED_TABLE, superseded):
            self.assert_rejected(payload, "does not occur verbatim")

    def test_bad_render_string_fails(self):
        payload = self.mutated()
        self.entry(payload, "arm.r1-1632.E")["render"] = "1.1575"
        self.assert_rejected(payload, "render '1.1575' != re-rendered '1.1574'")

    def test_unknown_render_rule_fails(self):
        payload = self.mutated()
        self.entry(payload, "arm.r1-1632.E")["render_rule"] = "E9"
        self.assert_rejected(payload, "unknown render_rule 'E9'")

    def test_unknown_label_fails(self):
        payload = self.mutated()
        self.entry(payload, "hours.total")["label"] = "guessed"
        self.assert_rejected(payload, "unknown label 'guessed'")

    def test_entries_out_of_id_order_fail(self):
        payload = self.mutated()
        payload["entries"].reverse()
        self.assert_rejected(payload, "entries are not sorted by id")


class ManifestContentTests(ManifestCase):
    """Every committed, arithmetic and cited number, and the complete check."""

    ARM_IDS = (
        "r1-1632",
        "r1-851",
        "r1-4658",
        "g2s-1632-w060",
        "g2s-1632-w120",
        "g2s-1632-w240",
        "g2s-1632-w480",
    )

    def entries(self) -> dict[str, dict]:
        return {entry["id"]: entry for entry in self.payload["entries"]}

    def test_every_entry_group_is_present(self):
        ids = self.entries()
        for prefix in (
            "arm.",
            "hours.",
            "steps.",
            "seconds_per_step.",
            "timing.",
            "polish.",
            "cost.",
            "best.",
            "rung1.",
            "curve.",
            "handoff.",
            "tiers.",
            "decision.",
            "baseline.",
            "survey.",
            "census.",
            "pub.",
            "gap5908.",
            "machine.",
            "cpu.",
        ):
            self.assertTrue(
                any(entry_id.startswith(prefix) for entry_id in ids), prefix
            )

    def test_each_arm_holds_its_nineteen_numbers(self):
        ids = self.entries()
        for arm_id in self.ARM_IDS:
            prefix = f"arm.{arm_id}."
            self.assertEqual(
                len([entry_id for entry_id in ids if entry_id.startswith(prefix)]),
                19,
                arm_id,
            )

    def test_acceptance_renders(self):
        entries = self.entries()
        expected = {
            "arm.r1-1632.E": "1.1574",
            "arm.r1-851.E": "1.2375",
            "arm.r1-4658.E": "1.1432",
            "arm.r1-4658.eps_h": "13,127.5",
            "hours.total": "22.378",
            "hours.rung1": "11.108",
            "hours.sweep": "11.270",
            "steps.total_adam": "7,437,225",
            "steps.sweep_budget.min": "842,770",
            "steps.sweep_budget.max": "994,807",
            "best.eps_h_official": "123.62",
            "best.ratio_to_bar": "1.24 \u00d7 10\u2077",
            "rung1.below_formula": "1 of 3",
            "baseline.copy.median_E.validation": "2.135",
            "census.one_part_in_0p1": "1,169",
            "cost.forscale.days_low": "28.5",
            "cost.forscale.days_high": "42.8",
        }
        for entry_id, render in expected.items():
            self.assertEqual(entries[entry_id]["render"], render, entry_id)

    def test_totals_are_the_ordered_sums_of_the_records(self):
        handoff = json.loads(
            (ROOT / f"{P60}/g2/stop-handoff.json").read_text(encoding="utf-8")
        )
        arms = [row["arm_id"] for row in handoff["arms"]]
        records = {
            arm_id: json.loads(
                (ROOT / f"{P60}/arms/{arm_id}/record.json").read_text(encoding="utf-8")
            )
            for arm_id in arms
        }
        hours = [records[arm_id]["wall"]["hours"] for arm_id in arms]
        entries = self.entries()
        self.assertEqual(entries["hours.total"]["value"], self.module.ordered_sum(hours))
        self.assertEqual(entries["hours.total"]["value"], handoff["total_wall_hours"])
        self.assertEqual(
            entries["hours.rung1"]["value"], self.module.ordered_sum(hours[:3])
        )
        self.assertEqual(
            entries["hours.sweep"]["value"], self.module.ordered_sum(hours[3:])
        )
        steps = 0
        for arm_id in arms:
            budget = records[arm_id]["budget"]
            steps += (
                budget["new_budget_steps"]
                if budget["extended"]
                else budget["budget_steps"]
            )
        self.assertEqual(entries["steps.total_adam"]["value"], steps)

    def test_the_best_and_rung1_readings(self):
        entries = self.entries()
        self.assertEqual(entries["best.eps_h_official_arms"]["render"], "g2s-1632-w240")
        self.assertEqual(entries["best.eps_h_lowest_state"]["render"], "30.29")
        self.assertEqual(entries["best.eps_h_lowest_state_arm"]["render"], "r1-1632")
        self.assertEqual(entries["best.eps_h_lowest_state_state"]["render"], "adam")
        self.assertEqual(entries["best.eps_h_lowest_trace"]["render"], "0.9999")
        self.assertEqual(entries["best.eps_h_lowest_trace_arm"]["render"], "r1-4658")
        self.assertEqual(entries["best.eps_h_lowest_trace_step"]["render"], "1,863,178")
        self.assertEqual(entries["rung1.below_formula_systems"]["render"], "4658")
        self.assertEqual(entries["rung1.counts_true"]["render"], "0 of 3")

    def test_no_entry_is_a_gpu_figure(self):
        for entry in self.payload["entries"]:
            self.assertNotIn("gpu", entry["id"].lower())
            self.assertNotIn("gpu", entry["derivation"].lower())

    def test_every_required_in_is_a_subset(self):
        for entry in self.payload["entries"]:
            self.assertTrue(set(entry["required_in"]) <= {"verdict", "charter"})

    def test_producer_ordered_sum_cancels_to_zero(self):
        producer = load_producer()
        values = [1e16, 1.0, -1e16]
        self.assertEqual(producer.ordered_sum(values), 0.0)
        self.assertEqual(self.module.ordered_sum(values), 0.0)
        # An exactly rounded sum would keep the 1.0; the ordered loop cannot.
        self.assertEqual(math.fsum(values), 1.0)

    def test_changed_arithmetic_total_fails(self):
        payload = self.mutated()
        entry = self.entry(payload, "hours.total")
        entry["value"] = 22.37828873402779
        self.assert_rejected(payload, "entry hours.total value")

    def test_recorded_key_that_differs_from_the_table_fails(self):
        payload = self.mutated()
        entry = self.entry(payload, "arm.r1-851.E")
        entry["source"]["key"] = "result.eps_h"
        self.assert_rejected(payload, "entry arm.r1-851.E source")

    def test_cited_token_absent_at_its_commit_fails(self):
        payload = self.mutated()
        entry = self.entry(payload, "pub.breen.energy_typical")
        entry["source"]["token"] = "of order 10\u207b\u00b3"
        superseded = {
            "pub.breen.energy_typical": (
                self.module.CITED_TABLE["pub.breen.energy_typical"][0],
                self.module.CITED_TABLE["pub.breen.energy_typical"][1],
                "of order 10\u207b\u00b3",
            )
        }
        with mock.patch.dict(self.module.CITED_TABLE, superseded):
            self.assert_rejected(payload, "does not occur verbatim")

    def test_stale_inputs_sha256_fails(self):
        payload = self.mutated()
        payload["inputs"][0]["sha256"] = "0" * 64
        self.assert_rejected(payload, "SHA-256")

    def test_stale_producer_sha256_fails(self):
        payload = self.mutated()
        payload["producer_sha256"][self.module.PRODUCER_REL] = "0" * 64
        self.assert_rejected(payload, "producer module")

    def test_a_tie_is_listed_in_handoff_order(self):
        facts = dict(self.module._facts())
        facts["records"] = copy.deepcopy(facts["records"])
        winner = "g2s-1632-w240"
        loser = "r1-1632"
        tied = facts["records"][winner]["result"]["eps_h"]
        facts["records"][loser]["result"]["eps_h"] = tied
        payload = self.mutated()
        for arm_id in (loser, winner):
            entry = self.entry(payload, f"arm.{arm_id}.eps_h")
            entry["value"] = tied
            entry["render"] = self.module.render_number(tied, entry["render_rule"])
        arms = self.entry(payload, "best.eps_h_official_arms")
        arms["value"] = f"{loser}, {winner}"
        arms["render"] = arms["value"]
        # The tied pair passes, in handoff order.
        self.module.check_numbers(payload, facts=facts)
        arms["value"] = f"{winner}, {loser}"
        arms["render"] = arms["value"]
        with self.assertRaises(self.module.VerifyError) as caught:
            self.module.check_numbers(payload, facts=facts)
        self.assertIn("best.eps_h_official_arms", str(caught.exception))

    def test_a_steps_budget_one_step_more_fails(self):
        from pinn.verification import feasibility_scorecard

        original = feasibility_scorecard.steps_budget

        def one_more(cap, wall, steps, *, scorecard):
            return original(cap, wall, steps, scorecard=scorecard) + 1

        payload = self.mutated()
        with mock.patch.object(feasibility_scorecard, "steps_budget", one_more):
            self.assert_rejected(payload, "recorded budget")


def _external_data_root_present() -> bool:
    """True when the main repo's ``simulation_data/Data`` directory exists."""
    from pinn.data.adapter import default_data_root

    return Path(default_data_root()).is_dir()


class DeriveHelperTests(unittest.TestCase):
    """The CPU re-derivation helpers on small arrays with a known answer.

    The same frozen scorer serves both programs; these tests pin the definitions
    the manifest records (time variation, RMS ratio, the inclusive Tier-1 limit,
    the best moment, the constant predictor) before the real weights are scored.
    """

    def setUp(self):
        self.verifier = load_verifier()
        self.producer = load_producer()

    def test_time_variation_of_a_constant_output_is_zero(self):
        reference = np.array(
            [
                [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
                [[1.0, 1.0, 0.0], [-1.0, 0.0, 1.0], [0.0, 2.0, -1.0]],
                [[1.0, 2.0, 0.0], [-1.0, 0.0, 2.0], [0.0, 2.0, -2.0]],
            ],
            dtype=np.float64,
        )
        still = np.broadcast_to(reference[0], reference.shape)
        for module in (self.producer, self.verifier):
            self.assertEqual(module.timevar_ratio(still, reference), 0.0)

    def test_rms_ratio_of_the_time_mean_predictor_is_exactly_one(self):
        reference = np.array(
            [
                [[1.0, 0.5, -0.25], [-1.5, 0.0, 0.75], [0.0, 2.0, 0.125]],
                [[1.25, 0.25, 0.5], [-0.75, -0.5, 1.5], [0.5, 1.0, -1.25]],
                [[0.5, 1.5, 0.0], [-2.0, 0.25, 0.25], [1.0, 0.5, 0.5]],
                [[2.0, 0.0, -0.5], [-0.5, 1.0, -1.0], [0.25, 2.0, 0.0]],
            ],
            dtype=np.float64,
        )
        predicted = np.broadcast_to(
            reference.mean(axis=0, keepdims=True), reference.shape
        )
        # (mean - x) is the exact negation of (x - mean), so the two RMS sums are
        # bit-identical and the ratio is exactly 1.0, not merely close.
        for module in (self.producer, self.verifier):
            self.assertEqual(module.rms_ratio(predicted, reference), 1.0)

    def test_the_tier1_limit_is_the_scorecards_inclusive_0_1(self):
        from pinn.verification.feasibility_scorecard import load_scorecard

        card = load_scorecard()
        self.assertEqual(self.verifier._tier1_max(card), 0.1)
        self.assertEqual(card.section("tiers")["comparison"], "inclusive_le")

    def test_within_tier1_counts_an_error_of_exactly_the_limit(self):
        derived = {
            "e_sys": np.array([0.1, 0.1000001, 0.05, 0.0], dtype=np.float64),
            "e_in": np.array([0.0, 0.0, 0.0999999, 0.1], dtype=np.float64),
            "times": np.zeros(4, dtype=np.float64),
        }
        count = self.verifier.cpu_value(
            "cpu.r1-1632.adam.n_within_tier1", derived, 0.1
        )
        self.assertIsInstance(count, int)
        # 0.1 is inside the tier; 0.1000001 is the one moment excluded.
        self.assertEqual(count, 3)
        self.assertEqual(
            self.verifier.cpu_value("cpu.r1-1632.adam.n_times", derived, 0.1), 4
        )

    def test_best_moment_is_the_minimum_of_the_timewise_maximum(self):
        derived = {
            "e_sys": np.array([0.2, 0.05, 0.3], dtype=np.float64),
            "e_in": np.array([0.1, 0.4, 0.2], dtype=np.float64),
            "times": np.zeros(3, dtype=np.float64),
        }
        self.assertEqual(
            self.verifier.cpu_value("cpu.r1-1632.adam.best_moment", derived, 0.1),
            0.2,
        )
        self.assertEqual(
            self.verifier.cpu_value("cpu.r1-1632.adam.e_sys_t0", derived, 0.1), 0.2
        )
        self.assertEqual(
            self.verifier.cpu_value("cpu.r1-1632.adam.e_in_t0", derived, 0.1), 0.1
        )

    def test_constant_error_is_zero_for_bodies_that_do_not_move(self):
        still = np.array(
            [
                [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
                [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
            ],
            dtype=np.float64,
        )
        e_sys, e_in = self.verifier.rederive_constant_error(still, (0, 1))
        np.testing.assert_array_equal(e_sys, np.zeros(2))
        np.testing.assert_array_equal(e_in, np.zeros(2))
        self.assertEqual(float(np.max(np.maximum(e_sys, e_in))), 0.0)

    def test_the_two_constant_predictors_agree_on_a_moving_reference(self):
        reference = np.array(
            [
                [[1.0, 0.0, 0.0], [-1.0, 0.5, 0.0], [0.0, 2.0, 0.25]],
                [[1.5, 0.25, 0.5], [-0.5, -0.25, 1.0], [0.25, 1.5, -1.0]],
                [[0.75, 1.0, 0.0], [-1.5, 0.0, 0.5], [1.0, 2.5, 0.0]],
            ],
            dtype=np.float64,
        )
        produced = self.producer.constant_predictor_error(reference, (0, 1))
        rederived = self.verifier.rederive_constant_error(reference, (0, 1))
        np.testing.assert_array_equal(produced[0], rederived[0])
        np.testing.assert_array_equal(produced[1], rederived[1])
        self.assertGreater(float(rederived[0].max()), 0.0)
        self.assertGreater(float(rederived[1].max()), 0.0)


class DeriveContextTests(unittest.TestCase):
    """The fail-closed gates of ``derive``, on a fake context: no data root needed.

    ``cmd_derive`` imports ``open_real_context`` and ``load_arm_data`` at call
    time, so patching them on ``pinn.verification.learnability_data`` exercises
    the real gate order without reading the corpus.
    """

    def setUp(self):
        self.verifier = load_verifier()
        cwd = Path.cwd()
        self.addCleanup(os.chdir, cwd)

    @staticmethod
    def _summary(**overrides):
        summary = {
            "schema": "phase59-files-opened/v1",
            "data_root_source": "fixture",
            "opened": {"train": 3, "validation": 0, "other_under_root": 0},
            "test_split_opened": 0,
            "blocked_attempts": 0,
            "refused_before_open": 0,
        }
        for dotted, value in overrides.items():
            target = summary
            parts = dotted.split(".")
            for part in parts[:-1]:
                target = target[part]
            target[parts[-1]] = value
        return summary

    @staticmethod
    def _context(summary):
        from pinn.verification.learnability_data import DataContext

        return DataContext(
            allowlist=None,
            reader=None,
            attestation=SimpleNamespace(summary=lambda: summary),
            stats=None,
            stats_sha256="0" * 64,
            normalizer_source="fixture",
            run_kind="fixture",
            data_root_source="fixture",
        )

    def assert_derive_rejected(self, summary: dict, needle: str) -> None:
        context = self._context(summary)
        loader = mock.Mock(side_effect=AssertionError("load_arm_data was called"))
        with mock.patch(
            "pinn.verification.learnability_data.open_real_context",
            return_value=context,
        ), mock.patch("pinn.verification.learnability_data.load_arm_data", loader):
            code, _stdout, stderr = run_main(self.verifier, ["derive"])
        self.assertEqual(code, 1, f"derive passed with {summary}")
        self.assertIn("FAIL-CLOSED", stderr)
        self.assertIn(needle, stderr)
        loader.assert_not_called()

    def test_a_test_split_open_fails_closed(self):
        self.assert_derive_rejected(
            self._summary(test_split_opened=1),
            "the open attestation shows test_split_opened 1",
        )

    def test_a_validation_open_fails_closed(self):
        self.assert_derive_rejected(
            self._summary(**{"opened.validation": 1}),
            "the open attestation shows opened.validation 1",
        )

    def test_a_weights_digest_mismatch_fails_before_torch_load(self):
        original = self.verifier.load_json

        def patched(path, *, what):
            payload = original(path, what=what)
            if Path(path).name == "record.json" and "r1-1632" in str(path):
                payload = copy.deepcopy(payload)
                payload["states"]["polish"]["weights"]["sha256"] = "0" * 64
            return payload

        with mock.patch.object(self.verifier, "load_json", patched), mock.patch(
            "torch.load"
        ) as loader:
            with self.assertRaises(self.verifier.VerifyError) as caught:
                self.verifier.rederive_state(None, None, "r1-1632", "polish")
        self.assertIn("weights SHA-256", str(caught.exception))
        self.assertIn("for r1-1632 polish", str(caught.exception))
        loader.assert_not_called()


@unittest.skipUnless(_external_data_root_present(), "external data root absent")
class DeriveRealTests(unittest.TestCase):
    """The CPU re-derivation on the real committed weights files."""

    def setUp(self):
        self.verifier = load_verifier()
        self.producer = load_producer()
        cwd = Path.cwd()
        self.addCleanup(os.chdir, cwd)

    def test_real_derive_re_derives_136_entries(self):
        code, stdout, stderr = run_main(self.verifier, ["derive"])
        self.assertEqual(code, 0, stderr)
        self.assertEqual(stdout.splitlines(), ["cpu entries 136", "DERIVE-OK"])

    def test_every_cpu_e_equals_its_records_cross_check(self):
        payload = json.loads(
            (ROOT / EVIDENCE / "numbers.json").read_text(encoding="utf-8")
        )
        entries = {entry["id"]: entry for entry in payload["entries"]}
        checked = 0
        for arm_id in self.verifier.EXPECTED_ARMS:
            record = json.loads(
                (ROOT / f"{P60}/arms/{arm_id}/record.json").read_text(encoding="utf-8")
            )
            for state in self.verifier.CPU_STATES:
                entry = entries[f"cpu.{arm_id}.{state}.E"]
                self.assertEqual(entry["label"], "rederived-cpu-float64")
                self.assertAlmostEqual(
                    entry["value"],
                    record["states"][state]["cross_check"]["E"],
                    delta=1e-12,
                )
                checked += 1
        self.assertEqual(checked, 14)

    def test_the_two_rederivations_agree_on_r1_1632_polish(self):
        import torch

        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification.learnability_arms import arm_spec
        from pinn.verification.learnability_data import load_arm_data, open_real_context

        os.chdir(ROOT)
        torch.set_num_threads(1)
        card = load_scorecard()
        ctx = open_real_context(repo_root=ROOT)
        arm_data = load_arm_data(
            arm_spec("r1-1632"), ctx, scorecard=card, dtype=torch.float32, device="cpu"
        )
        produced = self.producer.derive_state(
            ctx, card, "r1-1632", "polish", arm_data=arm_data
        )
        rederived = self.verifier.rederive_state(
            ctx, card, "r1-1632", "polish", arm_data=arm_data
        )
        for field in ("pos", "ref", "times", "e_sys", "e_in"):
            np.testing.assert_allclose(
                rederived[field],
                produced[field],
                rtol=0.0,
                atol=1e-12,
                err_msg=f"{field} differs between the two re-derivations",
            )
        self.assertEqual(rederived["inner_pair"], produced["inner_pair"])


def _zero_attestation_summary() -> dict:
    """The shape ``_check_attestation_summary`` accepts, with every counter zero."""
    return {
        "schema": "phase59-files-opened/v1",
        "data_root_source": "fixture",
        "opened": {"train": 0, "validation": 0, "other_under_root": 0},
        "test_split_opened": 0,
        "blocked_attempts": 0,
        "refused_before_open": 0,
    }


def _synthetic_series() -> dict:
    """A real-shaped plotted series: three bodies, four times, distinct tracks.

    The predicted tracks are tiny beside the real ones, like the real figure's
    (64-RESEARCH Pitfall 11), and every body's mean differs from its track, so a
    renderer that drops a body or a marker cannot pass the shape assertions.
    """
    times = [0.0, 1.0, 2.0, 3.0]
    ref_xy = []
    pred_xy = []
    mean_xy = []
    for body in range(3):
        base = (body - 1) * 3.0
        ref_xy.append(
            [
                [base + 0.0, base + 0.0],
                [base + 0.4, base + 0.2],
                [base + 0.8, base + 0.3],
                [base + 1.2, base + 0.5],
            ]
        )
        pred_xy.append(
            [
                [base + 0.50, base + 0.10],
                [base + 0.52, base + 0.11],
                [base + 0.54, base + 0.09],
                [base + 0.56, base + 0.12],
            ]
        )
        mean_xy.append([base + 0.6, base + 0.2])
    return {
        "arm": "r1-1632",
        "state": "polish",
        "times": times,
        "ref_xy": ref_xy,
        "pred_xy": pred_xy,
        "mean_xy": mean_xy,
        "err_net": [1.0, 1.1, 1.2, 1.3],
        "err_const": [1.05, 1.15, 1.25, 1.35],
        "tier1": 0.1,
        "attestation": _zero_attestation_summary(),
    }


class FigureRenderTests(unittest.TestCase):
    """The SVG renderer on a small synthetic series: pure, no data root needed."""

    @classmethod
    def setUpClass(cls):
        cls.producer = load_figure_producer()
        cls.series = _synthetic_series()

    def test_two_calls_are_byte_identical(self):
        first = self.producer.render_svg(self.series)
        second = self.producer.render_svg(self.series)
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

    def test_the_panel_a_group_holds_three_real_and_three_predicted_tracks(self):
        root = ElementTree.fromstring(self.producer.render_svg(self.series))
        panel = next(
            element for element in root.iter() if element.get("id") == "panel-a"
        )
        polylines = [
            element
            for element in panel.iter()
            if element.tag.rsplit("}", 1)[-1] == "polyline"
        ]
        widths = [element.get("stroke-width") for element in polylines]
        # The main panel draws the real tracks at 1.5 px and the predicted ones
        # at 3 px over a 5 px white halo; the inset's magnified tracks are 1.2 px
        # so they cannot be mistaken for a fourth real track.
        self.assertEqual(widths.count("1.5"), 3, widths)
        self.assertEqual(widths.count("3"), 3, widths)
        self.assertEqual(widths.count("5"), 3, widths)
        self.assertEqual(widths.count("1.2"), 3, widths)

    def test_every_text_and_point_lies_inside_the_viewbox(self):
        verifier = load_verifier()
        verifier._check_svg_document(
            self.producer.render_svg(self.series), required_ids=("panel-a",)
        )

    def test_the_document_holds_no_script_and_no_href(self):
        text = self.producer.render_svg(self.series)
        self.assertNotIn("<script", text)
        self.assertNotIn("href", text)

    def test_the_predicted_track_label_is_drawn(self):
        self.assertIn(
            "network prediction (barely moves)",
            self.producer.render_svg(self.series),
        )

    def test_a_one_time_series_is_refused(self):
        broken = dict(self.series)
        broken["times"] = [0.0]
        with self.assertRaises(self.producer.FigureError):
            self.producer.render_svg(broken)

    def _panel_b_polylines(self, text: str) -> list[ElementTree.Element]:
        root = ElementTree.fromstring(text)
        panel = next(
            element for element in root.iter() if element.get("id") == "panel-b"
        )
        return [
            element
            for element in panel.iter()
            if element.tag.rsplit("}", 1)[-1] == "polyline"
        ]

    def test_the_panel_b_group_holds_two_error_curves_and_the_limit(self):
        text = self.producer.render_svg(self.series)
        root = ElementTree.fromstring(text)
        panel = next(
            element for element in root.iter() if element.get("id") == "panel-b"
        )
        polylines = [
            element
            for element in panel.iter()
            if element.tag.rsplit("}", 1)[-1] == "polyline"
        ]
        self.assertEqual(len(polylines), 2)
        strokes = [element.get("stroke") for element in polylines]
        self.assertIn("#1f2328", strokes)  # network error, ink
        self.assertIn("#57606a", strokes)  # constant predictor, muted grey
        limits = [
            element
            for element in panel.iter()
            if element.tag.rsplit("}", 1)[-1] == "line"
            and element.get("stroke") == "#b3261e"
        ]
        self.assertEqual(len(limits), 1)
        self.assertIn("Tier 1 limit (0.1)", text)

    def test_the_two_error_curves_share_their_x_coordinates(self):
        polylines = self._panel_b_polylines(self.producer.render_svg(self.series))
        x_lists = []
        for polyline in polylines:
            points = polyline.get("points", "").split()
            x_lists.append([point.split(",")[0] for point in points])
        self.assertEqual(len(x_lists[0]), len(self.series["times"]))
        self.assertEqual(x_lists[0], x_lists[1])

    def test_the_legend_lies_inside_the_canvas_below_the_panels(self):
        report = self.producer.legibility_report(
            self.series, self.producer.render_svg(self.series)
        )
        legend = report["legend"]
        self.assertGreaterEqual(legend[0], 0.0)
        self.assertGreaterEqual(legend[1], 0.0)
        self.assertLessEqual(legend[2], self.producer.VIEW_WIDTH)
        self.assertLessEqual(legend[3], self.producer.VIEW_HEIGHT)
        self.assertGreater(
            legend[1], max(frame[3] for frame in report["frames"].values())
        )

    def test_the_axis_and_limit_labels_are_drawn(self):
        text = self.producer.render_svg(self.series)
        for label in (
            "x (system units)",
            "y (system units)",
            "time (system units)",
            "error (largest of the body and inner-pair errors)",
            "Tier 1 limit (0.1)",
        ):
            self.assertIn(label, text)

    def test_a_legend_outside_the_canvas_is_refused(self):
        text = self.producer.render_svg(self.series)
        moved = text.replace('y="476.0"', 'y="600.0"', 1)
        self.assertNotEqual(moved, text)
        with self.assertRaises(self.producer.FigureError):
            self.producer._check_legibility(self.series, moved)

    def test_a_predicted_track_with_no_extent_is_refused(self):
        flat = copy.deepcopy(self.series)
        flat["pred_xy"][0] = [[0.5, 0.1] for _ in flat["times"]]
        with self.assertRaises(self.producer.FigureError):
            self.producer._check_legibility(flat, self.producer.render_svg(flat))


class FigureModeTests(unittest.TestCase):
    """The committed figure set in a temporary repository, then one mutation each.

    The fixture copies the four inputs and both producer scripts byte for byte
    and patches ``REPO_ROOT``, so every digest the verifier checks is a digest
    of real bytes. The series derivation is patched to the synthetic series: the
    real derivation is FigureRealTests' job, and the synthetic one lets each
    negative control fail for exactly one reason.
    """

    @classmethod
    def setUpClass(cls):
        cls.module = load_verifier()
        cls.producer = load_figure_producer()
        cls.series = _synthetic_series()
        cls._tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._tmp.cleanup)
        cls.root = Path(cls._tmp.name).resolve()
        for relative in FIGURE_INPUT_RELS + FIGURE_PRODUCER_RELS:
            copy_bytes(cls.root, relative)
        cls.svg_text = cls.producer.render_svg(cls.series)
        (cls.root / f"{EVIDENCE}/figure-1632.svg").write_text(
            cls.svg_text, encoding="utf-8"
        )
        payload = json.loads(FIGURE_PROVENANCE_PATH.read_text(encoding="utf-8"))
        payload["figure"]["sha256"] = hashlib.sha256(
            cls.svg_text.encode("utf-8")
        ).hexdigest()
        payload["series_sha256"] = cls.module._figure_series_digest(cls.series)
        cls.provenance = payload
        cls.write_provenance(payload)

    @classmethod
    def write_provenance(cls, payload: dict) -> None:
        (cls.root / f"{EVIDENCE}/figure-1632.provenance.json").write_bytes(
            cls.module._canonical_bytes(payload)
        )

    def setUp(self):
        cwd = Path.cwd()
        self.addCleanup(os.chdir, cwd)
        self.write_svg(self.svg_text)
        self.write_provenance(self.provenance)

    def write_svg(self, text: str) -> None:
        (self.root / f"{EVIDENCE}/figure-1632.svg").write_text(text, encoding="utf-8")

    def mutated_provenance(self) -> dict:
        return json.loads(json.dumps(self.provenance))

    def rewrite_with_svg(self, text: str) -> None:
        """Write new SVG bytes and keep the provenance's figure digest honest."""
        self.write_svg(text)
        payload = self.mutated_provenance()
        payload["figure"]["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        self.write_provenance(payload)

    def run_figure(self) -> tuple[int, str, str]:
        context = SimpleNamespace(
            attestation=SimpleNamespace(summary=_zero_attestation_summary)
        )
        with mock.patch.object(self.module, "REPO_ROOT", self.root), mock.patch.object(
            self.module, "_figure_series", return_value=self.series
        ), mock.patch.object(
            self.module, "_load_figure_producer", return_value=self.producer
        ), mock.patch(
            "pinn.verification.learnability_data.open_real_context",
            return_value=context,
        ):
            return run_main(self.module, ["figure"])

    def assert_rejected(self, needle: str) -> None:
        code, _stdout, stderr = self.run_figure()
        self.assertEqual(code, 1, f"the mutated figure set passed: {stderr}")
        self.assertIn("FAIL-CLOSED", stderr)
        self.assertIn(needle, stderr)

    def test_the_committed_set_passes(self):
        code, stdout, stderr = self.run_figure()
        self.assertEqual(code, 0, stderr)
        self.assertEqual(
            stdout.splitlines(),
            [f"figure times {len(self.series['times'])}", "FIGURE-OK"],
        )

    def test_one_changed_svg_byte_fails(self):
        changed = self.svg_text.replace("#2a78d6", "#2a78d7", 1)
        self.assertNotEqual(changed, self.svg_text)
        self.write_svg(changed)
        self.assert_rejected("figure SVG SHA-256")

    def test_a_stale_provenance_svg_digest_fails(self):
        payload = self.mutated_provenance()
        payload["figure"]["sha256"] = "0" * 64
        self.write_provenance(payload)
        self.assert_rejected("figure SVG SHA-256")

    def test_a_stale_input_digest_fails(self):
        payload = self.mutated_provenance()
        payload["inputs"][0]["sha256"] = "0" * 64
        self.write_provenance(payload)
        self.assert_rejected("figure input")

    def test_a_series_digest_that_differs_fails(self):
        payload = self.mutated_provenance()
        payload["series_sha256"] = "0" * 64
        self.write_provenance(payload)
        self.assert_rejected("re-derived series SHA-256")

    def test_a_text_element_outside_the_viewbox_fails(self):
        changed = self.svg_text.replace('x="60.0" y="30.0"', 'x="1600.0" y="30.0"', 1)
        self.assertNotEqual(changed, self.svg_text)
        self.rewrite_with_svg(changed)
        self.assert_rejected("lies outside the viewBox")

    def test_a_home_directory_string_fails(self):
        home = str(Path.home())
        self.assertTrue(home)
        changed = self.svg_text.replace("</svg>", f"<!-- {home} -->\n</svg>", 1)
        self.rewrite_with_svg(changed)
        self.assert_rejected("contains the host home prefix")

    def test_a_script_element_fails(self):
        changed = self.svg_text.replace(
            "</svg>", "<script>alert(1)</script>\n</svg>", 1
        )
        self.rewrite_with_svg(changed)
        self.assert_rejected("script element")

    def test_an_href_attribute_fails(self):
        changed = self.svg_text.replace("</svg>", '<use href="#panel-a"/>\n</svg>', 1)
        self.rewrite_with_svg(changed)
        self.assert_rejected("href attribute")

    def test_a_missing_panel_a_group_fails(self):
        changed = self.svg_text.replace('id="panel-a"', 'id="panel-aa"', 1)
        self.assertNotEqual(changed, self.svg_text)
        self.rewrite_with_svg(changed)
        self.assert_rejected("no group with id 'panel-a'")

    def test_a_missing_legend_group_fails(self):
        changed = self.svg_text.replace('id="legend"', 'id="legend-aa"', 1)
        self.assertNotEqual(changed, self.svg_text)
        self.rewrite_with_svg(changed)
        self.assert_rejected("no group with id 'legend'")

    def test_a_non_zero_recorded_attestation_fails(self):
        payload = self.mutated_provenance()
        payload["attestation"]["opened"]["validation"] = 1
        self.write_provenance(payload)
        self.assert_rejected("shows opened.validation 1")

    def test_the_provenance_holds_the_contracted_keys(self):
        self.assertEqual(self.provenance["schema"], "phase64-figure-provenance/v1")
        self.assertEqual(
            set(self.provenance),
            {
                "schema",
                "plain_language",
                "figure",
                "inputs",
                "producers",
                "series_sha256",
                "arm",
                "state",
                "precision",
                "versions",
                "data_root_source",
                "attestation",
                "command",
            },
        )
        self.assertNotIn("git_head", self.provenance)
        self.assertNotIn("utc_started", self.provenance)


@unittest.skipUnless(_external_data_root_present(), "external data root absent")
class FigureRealTests(unittest.TestCase):
    """The figure mode on the real committed figure and the real weights."""

    def setUp(self):
        self.verifier = load_verifier()
        cwd = Path.cwd()
        self.addCleanup(os.chdir, cwd)

    def test_real_figure_prints_figure_ok(self):
        code, stdout, stderr = run_main(self.verifier, ["figure"])
        self.assertEqual(code, 0, stderr)
        self.assertEqual(stdout.splitlines(), ["figure times 1001", "FIGURE-OK"])

    def test_the_provenance_records_the_committed_svg_digest(self):
        payload = json.loads(FIGURE_PROVENANCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(payload["figure"]["sha256"], sha256_of(FIGURE_SVG_PATH))
        self.assertEqual(
            payload["figure"]["path"], f"{EVIDENCE}/figure-1632.svg"
        )

    def test_the_committed_svg_names_both_panels_and_the_limit(self):
        text = FIGURE_SVG_PATH.read_text(encoding="utf-8")
        for needle in (
            'id="panel-a"',
            'id="panel-b"',
            'id="legend"',
            "Tier 1 limit (0.1)",
        ):
            self.assertIn(needle, text)

    def test_real_error_is_above_tier1_at_every_time(self):
        producer = load_figure_producer()
        series = producer.figure_series(ROOT)
        self.assertEqual(series["tier1"], 0.1)
        self.assertEqual(len(series["err_net"]), 1001)
        self.assertTrue(
            all(value > series["tier1"] for value in series["err_net"]),
            min(series["err_net"]),
        )
        payload = json.loads(
            (ROOT / EVIDENCE / "numbers.json").read_text(encoding="utf-8")
        )
        entry = next(
            item
            for item in payload["entries"]
            if item["id"] == "cpu.r1-1632.polish.n_within_tier1"
        )
        self.assertEqual(entry["value"], 0)


class OrderedSumTests(unittest.TestCase):
    """The one summation helper: left to right, in the order given."""

    def setUp(self):
        self.module = load_verifier()

    def test_ordered_sum_matches_the_sealed_total(self):
        handoff = json.loads(
            (ROOT / f"{P60}/g2/stop-handoff.json").read_text(encoding="utf-8")
        )
        values = [arm["wall_hours"] for arm in handoff["arms"]]
        self.assertEqual(
            self.module.ordered_sum(values), handoff["total_wall_hours"]
        )

    def test_math_fsum_would_not_match_the_sealed_total(self):
        handoff = json.loads(
            (ROOT / f"{P60}/g2/stop-handoff.json").read_text(encoding="utf-8")
        )
        values = [arm["wall_hours"] for arm in handoff["arms"]]
        # Pins why the verifier never uses math.fsum or a sorted order: both
        # land one ulp below the stored total on every interpreter.
        self.assertNotEqual(math.fsum(values), handoff["total_wall_hours"])

    def test_ordered_sum_is_left_to_right(self):
        self.assertEqual(self.module.ordered_sum([1e16, 1.0, -1e16]), 0.0)
        self.assertEqual(math.fsum([1e16, 1.0, -1e16]), 1.0)

    def test_ordered_sum_of_nothing_is_zero(self):
        self.assertEqual(self.module.ordered_sum([]), 0.0)


class StaticGuardTests(unittest.TestCase):
    """Mechanical guards over every script the Phase 64 evidence tree holds."""

    def setUp(self):
        self.module = load_verifier()
        self.evidence = ROOT / EVIDENCE
        self.scripts = sorted(self.evidence.glob("*.py"))
        self.assertIn(VERIFIER_PATH, self.scripts)

    def test_no_module_level_torch_or_pinn_import(self):
        tree = ast.parse(VERIFIER_PATH.read_text(encoding="utf-8"))
        imported: list[str] = []
        for node in tree.body:
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        for name in imported:
            self.assertNotEqual(name, "torch", "the verifier must not import torch at module scope")
            self.assertFalse(
                name == "pinn" or name.startswith("pinn."),
                f"the verifier must not import {name} at module scope",
            )

    def test_no_shell_true_eval_or_exec(self):
        for script in self.scripts:
            tree = ast.parse(script.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    for keyword in node.keywords:
                        if keyword.arg == "shell":
                            self.assertFalse(
                                isinstance(keyword.value, ast.Constant)
                                and keyword.value.value is True,
                                f"{script.name} passes shell=True to a subprocess",
                            )
                    if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                        self.fail(f"{script.name} calls {node.func.id}")

    def test_every_torch_load_pins_weights_only(self):
        for script in self.scripts:
            tree = ast.parse(script.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                if not isinstance(func, ast.Attribute) or func.attr != "load":
                    continue
                owner = func.value
                owner_name = getattr(owner, "id", None) or getattr(owner, "attr", None)
                if owner_name != "torch":
                    continue
                pinned = [
                    keyword
                    for keyword in node.keywords
                    if keyword.arg == "weights_only"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ]
                self.assertTrue(
                    pinned,
                    f"{script.name} calls torch.load without weights_only=True",
                )


VERDICT_REL = f"{PHASE}/64-VERDICT.md"
# The verdict and the three files `rules` hashes or scans beside it.
VERDICT_FIXTURE_RELS = (
    VERDICT_REL,
    f"{EVIDENCE}/numbers.json",
    f"{EVIDENCE}/figure-1632.svg",
    f"{EVIDENCE}/figure-1632.provenance.json",
)


class VerdictCase(unittest.TestCase):
    """Shared fixture: byte copies of the verdict and the files ``rules`` reads.

    The real verdict is proven first (``RulesVerdictTests``), then every negative
    control mutates a byte copy in a temporary repository whose ``REPO_ROOT`` is
    patched. ``numbers`` is exercised with ``verdict_text`` patched instead: its
    manifest check re-reads the committed citations through git, which a
    temporary copy would (correctly) fail.
    """

    @classmethod
    def setUpClass(cls):
        cls.module = load_verifier()
        cls.verdict = (ROOT / VERDICT_REL).read_text(encoding="utf-8")

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        for relative in VERDICT_FIXTURE_RELS:
            copy_bytes(self.root, relative)

    def run_rules(self, text: str) -> tuple[int, str, str]:
        (self.root / VERDICT_REL).write_text(text, encoding="utf-8")
        with mock.patch.object(self.module, "REPO_ROOT", self.root):
            return run_main(self.module, ["rules"])

    def assert_rules_rejected(self, text: str, needle: str) -> str:
        code, _stdout, stderr = self.run_rules(text)
        self.assertEqual(code, 1, f"the mutated verdict passed: {stderr}")
        self.assertIn("FAIL-CLOSED", stderr)
        self.assertIn(needle, stderr)
        return stderr


class RulesVerdictTests(VerdictCase):
    """The tracer gate: the real headline passes, and every wording control fails."""

    def test_real_verdict_prints_rules_ok(self):
        code, out, err = run_main(self.module, ["rules"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out.splitlines(), ["RULES-OK"])
        self.assertNotIn("FAIL-CLOSED", err)

    def test_module_constants(self):
        self.assertEqual(len(self.module.EXPECTED_VERDICT_HEADINGS), 15)
        self.assertEqual(len(self.module.VERDICT_FRONT_MATTER_KEYS), 16)
        self.assertEqual(
            self.module.EXPECTED_VERDICT_HEADINGS[0], "## In plain language"
        )
        self.assertEqual(
            self.module.AUDIENCE_LINE,
            "**Audience:** the project owner, a first-year student; "
            "no specialist background assumed.",
        )
        self.assertIn("rules", self.module.COMMANDS)
        self.assertEqual(self.module.build_parser().parse_args(["rules"]).command, "rules")

    def test_changed_label_fails(self):
        mutated = self.verdict.replace(
            "RETHINK-REPRESENTATION", "RETHINK-REPRESENTATION-OR-RECIPE"
        )
        self.assert_rules_rejected(mutated, "RETHINK-REPRESENTATION")

    def test_first_heading_changed_fails(self):
        mutated = replace_once(
            self.verdict, "## In plain language", "## The headline"
        )
        self.assert_rules_rejected(mutated, "heading")

    def test_audience_line_removed_fails(self):
        mutated = self.verdict.replace(self.module.AUDIENCE_LINE + "\n\n", "")
        self.assert_rules_rejected(mutated, "Audience")

    def test_d02_phrase_removed_fails(self):
        mutated = self.verdict.replace(
            "not evaluated on this branch", "not evaluated here"
        )
        self.assert_rules_rejected(mutated, "not evaluated on this branch")

    def test_box_column_header_renamed_fails(self):
        mutated = replace_once(
            self.verdict,
            "What the pre-registered rule says",
            "What the rule says",
        )
        self.assert_rules_rejected(mutated, "What the pre-registered rule says")

    def test_guarded_wording_outside_a_fence_fails(self):
        mutated = replace_once(
            self.verdict,
            "## The result under the pre-registered rule",
            "rented GPU time\n\n## The result under the pre-registered rule",
        )
        self.assert_rules_rejected(mutated, "guarded wording")

    def test_guarded_wording_inside_an_owner_quote_passes(self):
        mutated = replace_once(
            self.verdict,
            "## The result under the pre-registered rule",
            "```owner-quote\nrented GPU time\n```\n\n"
            "## The result under the pre-registered rule",
        )
        code, out, err = self.run_rules(mutated)
        self.assertEqual(code, 0, err)
        self.assertEqual(out.splitlines(), ["RULES-OK"])

    def test_dollar_digit_fails(self):
        mutated = replace_once(
            self.verdict,
            "## The result under the pre-registered rule",
            "It costs $10 per hour.\n\n## The result under the pre-registered rule",
        )
        self.assert_rules_rejected(mutated, "guarded wording")

    def test_banned_adjective_fails(self):
        mutated = replace_once(
            self.verdict,
            "## The result under the pre-registered rule",
            "The curves were flat.\n\n## The result under the pre-registered rule",
        )
        self.assert_rules_rejected(mutated, "banned adjective")

    def test_proposal_gloss_fails(self):
        mutated = replace_once(
            self.verdict,
            "## The result under the pre-registered rule",
            "no change to the training recipe can fix it\n\n"
            "## The result under the pre-registered rule",
        )
        self.assert_rules_rejected(mutated, "gloss")

    def test_home_directory_string_fails(self):
        mutated = replace_once(
            self.verdict,
            "## The result under the pre-registered rule",
            f"{Path.home()}\n\n## The result under the pre-registered rule",
        )
        self.assert_rules_rejected(mutated, "home prefix")

    def test_status_final_fails(self):
        mutated = replace_once(
            self.verdict, "status: awaiting-owner", "status: final"
        )
        self.assert_rules_rejected(mutated, "status")

    def test_changed_handoff_digest_fails(self):
        mutated = replace_once(
            self.verdict,
            "handoff_sha256: "
            "7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5",
            "handoff_sha256: " + "0" * 64,
        )
        self.assert_rules_rejected(mutated, "handoff_sha256")

    def test_headings_out_of_order_fail(self):
        mutated = self.verdict.replace(
            "## In plain language", "## __SWAP__"
        ).replace(
            "## The result under the pre-registered rule", "## In plain language"
        ).replace(
            "## __SWAP__", "## The result under the pre-registered rule"
        )
        self.assert_rules_rejected(mutated, "heading")


if __name__ == "__main__":
    unittest.main()
