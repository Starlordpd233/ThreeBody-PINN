"""Phase 64 verifier: real-worktree smokes and synthetic negative controls.

Every mode is proven on the real committed files before its synthetic tests are
trusted (64-RESEARCH Pattern 4: the Phase 60 verifier crashed on first real use
twice when mocks had the wrong shapes). The synthetic repositories hold byte
copies of the real records, never stand-ins.
"""

from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import math
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
PHASE = ".planning/phases/64-feasibility-verdict"
EVIDENCE = f"{PHASE}/evidence"
P60 = ".planning/phases/60-single-system-learnability/evidence"
P59 = ".planning/phases/59-read-only-baseline-scorecard/evidence"
VERIFIER_PATH = ROOT / EVIDENCE / "verify_phase64_verdict.py"

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
        parser = self.module.build_parser()
        self.assertEqual(parser.parse_args(["inputs"]).command, "inputs")
        self.assertEqual(parser.parse_args(["frozen"]).command, "frozen")

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


if __name__ == "__main__":
    unittest.main()
