"""Phase 60 (D-07): tests for the first_omega_0 seam in GATE-04 and the omega re-measure entry.

Two groups run here.

``SeamDefaultTests`` prove that ``first_omega_0=None`` leaves GATE-04 exactly as it was: the
first default case's raw bin means equal the committed ``r_ref_stage0.json`` row, and the
locked 30.0 is bitwise equal to the default path. They hold the only two real measurements in
this module (one case each, CPU, float64). Everything else patches ``run_gate`` to a verdict
that is rebuilt from the committed raw bin means, so no six-case measurement ever runs, and
builds its evidence in a temporary git repository (the helpers of
``tests.phase59.test_evidence_verifier``, through ``tests.phase60.test_g2``).

The governed ``r_ref_stage0.json`` is only read and hashed. Nothing here writes under the real
evidence tree, and the unpatched command line is never invoked.
"""

from __future__ import annotations

import ast
import builtins
import contextlib
import dataclasses
import hashlib
import importlib
import inspect
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.training.config import load_frozen_r_ref_artifact
from pinn.verification import gate04_train_free as gate04
from pinn.verification import learnability_g2 as g2
from pinn.verification.architecture_characterization_probe import DEFAULT_CASES
from pinn.verification.learnability_arms import EVIDENCE_REL, PHASE_REL
from pinn.verification.learnability_ruling import Checkpoint4Ruling
from tests.phase39.test_prohibitions import executable_source_from_text
from tests.phase60.test_g2 import ONE_AT_120, Tree, rescued_tree

MODULE = "pinn.verification.gate04_omega_remeasure"
ROOT = Path(__file__).resolve().parents[2]
GOVERNED = gate04.R_REF_ARTIFACT_PATH
PHASE57_EVIDENCE = (
    ROOT / ".planning" / "phases" / "57-corrected-re-run-the-preserved-evaluation" / "evidence"
)
RULING_NAME = "60-CHECKPOINT-4-RULING.md"
EVIDENCE_NAME = "gate04-evidence.json"
RECORD_NAME = "gate04-remeasure.json"
APPROVED_NAME = "r-ref-approved.json"
SEAM_FUNCTIONS = ("_measure_raw_bin_means", "compute_r_ref", "evaluate_case", "run_gate")


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------

def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def committed_artifact():
    return json.loads(GOVERNED.read_text(encoding="utf-8"))


def remeasure_module(test):
    """The re-measure module, or a plain assertion failure that names the missing module."""
    try:
        return importlib.import_module(MODULE)
    except ModuleNotFoundError as exc:
        if exc.name != MODULE:
            raise
        test.fail(f"{MODULE} does not exist yet")


def seam_gaps():
    """The gate functions that do not yet take a keyword-only ``first_omega_0`` defaulting to None."""
    gaps = []
    for name in SEAM_FUNCTIONS:
        parameter = inspect.signature(getattr(gate04, name)).parameters.get("first_omega_0")
        if (
            parameter is None
            or parameter.kind is not inspect.Parameter.KEYWORD_ONLY
            or parameter.default is not None
        ):
            gaps.append(name)
    return gaps


def recorded_measure(case, *, dtype, torch_device, first_omega_0=None):
    """Stands in for ``_measure_raw_bin_means``: the raw bin means committed for this default case."""
    rows = committed_artifact()["raw_bin_means"]
    index = [(item.label, item.seed) for item in DEFAULT_CASES].index((case.label, case.seed))
    return np.asarray(rows[index], dtype=np.float64)


_PASS_VERDICTS = []


def recorded_pass_verdict():
    """The gate's own verdict over the six default cases, rebuilt from the committed rows.

    ``run_gate`` runs for real (reference, weights, the ratified condition checks) with only the
    network measurement replaced by the committed numbers, so the result is a genuine complete
    PASS object and no network is built.
    """
    if not _PASS_VERDICTS:
        with mock.patch.object(gate04, "_measure_raw_bin_means", side_effect=recorded_measure):
            _PASS_VERDICTS.append(gate04.run_gate(DEFAULT_CASES, precision="float64", device="cpu"))
    return _PASS_VERDICTS[0]


def block_verdict(reason="synthetic GATE-04 block for the tests"):
    return gate04.Gate04Verdict(
        verdict=gate04.VERDICT_BLOCK,
        blocking_reasons=(reason,),
        unratified_conditions=(),
        cases=(),
        r_ref=float("nan"),
        causal_clip_min_weight=recorded_pass_verdict().causal_clip_min_weight,
        precision="float64",
        device="cpu",
    )


def snapshot(root):
    """``{relative path: SHA-256}`` of every file under ``root`` except git's own."""
    root = Path(root)
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


class WriteSpy:
    """Records the destination of every file write, atomic replace and exclusive create."""

    def __init__(self):
        self.targets = []

    def __enter__(self):
        self._open, self._os_open, self._replace = builtins.open, os.open, os.replace
        spy = self

        def spy_open(file, mode="r", *args, **kwargs):
            if isinstance(file, (str, os.PathLike)) and any(flag in str(mode) for flag in "wax+"):
                spy.targets.append(Path(file))
            return spy._open(file, mode, *args, **kwargs)

        def spy_os_open(path, flags, *args, **kwargs):
            written = flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
            if written and os.fsdecode(path) != os.devnull:
                spy.targets.append(Path(os.fsdecode(path)))
            return spy._os_open(path, flags, *args, **kwargs)

        def spy_replace(source, destination, *args, **kwargs):
            spy.targets.append(Path(os.fsdecode(destination)))
            return spy._replace(source, destination, *args, **kwargs)

        builtins.open, os.open, os.replace = spy_open, spy_os_open, spy_replace
        return self

    def __exit__(self, *exc_info):
        builtins.open, os.open, os.replace = self._open, self._os_open, self._replace
        return False


class _Stop(Exception):
    """Raised by a patched network builder so that no measurement runs after the branch."""


# ---------------------------------------------------------------------------
# The seam: first_omega_0=None keeps GATE-04 exactly as it was.
# ---------------------------------------------------------------------------

class SeamDefaultTests(unittest.TestCase):
    CASE = DEFAULT_CASES[0]
    DTYPE = torch.float64
    DEVICE = torch.device("cpu")
    _measured = {}

    def require_seam(self):
        self.assertEqual(
            seam_gaps(), [],
            "these gate functions lack a keyword-only first_omega_0 defaulting to None",
        )

    def measure(self, omega):
        """One real measurement of the first default case, kept for the other tests of this class."""
        if omega not in self._measured:
            self._measured[omega] = gate04._measure_raw_bin_means(
                self.CASE, dtype=self.DTYPE, torch_device=self.DEVICE, first_omega_0=omega
            )
        return self._measured[omega]

    def test_the_four_gate_functions_take_a_keyword_only_first_omega_0_that_defaults_to_none(self):
        self.require_seam()

    def test_the_default_path_reproduces_the_committed_first_row(self):
        self.require_seam()
        artifact = committed_artifact()
        self.assertEqual(artifact["cases"][0]["label"], self.CASE.label)
        committed = np.asarray(artifact["raw_bin_means"][0], dtype=np.float64)
        np.testing.assert_allclose(self.measure(None), committed, rtol=1e-12, atol=0.0)

    def test_the_locked_frequency_is_bitwise_equal_to_the_default_path(self):
        self.require_seam()
        default, locked = self.measure(None), self.measure(30.0)
        self.assertEqual(default.dtype, locked.dtype)
        self.assertTrue(np.array_equal(default, locked))

    def test_none_builds_the_locked_network_and_a_value_builds_the_override(self):
        self.require_seam()
        case, dtype, device = self.CASE, self.DTYPE, self.DEVICE
        with mock.patch.object(gate04, "build_network", side_effect=_Stop) as locked, \
                mock.patch.object(gate04, "build_network_with_first_omega", side_effect=_Stop) as override:
            for call in (
                lambda: gate04._measure_raw_bin_means(case, dtype=dtype, torch_device=device),
                lambda: gate04._measure_raw_bin_means(
                    case, dtype=dtype, torch_device=device, first_omega_0=None),
            ):
                with self.assertRaises(_Stop):
                    call()
            self.assertEqual(locked.call_count, 2)
            override.assert_not_called()
            spec = locked.call_args.args[0]
            self.assertIsInstance(spec, ArchitectureSpec)
            self.assertEqual((spec.seed, spec.first_omega_0), (case.seed, 30.0))
            self.assertEqual(locked.call_args.kwargs, {"dtype": dtype, "device": device})
            locked.reset_mock()
            with self.assertRaises(_Stop):
                gate04._measure_raw_bin_means(
                    case, dtype=dtype, torch_device=device, first_omega_0=60.0)
            locked.assert_not_called()
            override.assert_called_once_with(60.0, seed=case.seed, dtype=dtype, device=device)

    def test_the_keyword_reaches_every_measurement_of_run_gate(self):
        self.require_seam()
        with mock.patch.object(
                gate04, "_measure_raw_bin_means", side_effect=recorded_measure) as measure:
            verdict = gate04.run_gate(
                DEFAULT_CASES, precision="float64", device="cpu", first_omega_0=120.0)
            self.assertEqual(verdict.verdict, gate04.VERDICT_PASS)
            self.assertEqual(measure.call_count, 2 * len(DEFAULT_CASES))
            self.assertEqual(
                {call.kwargs.get("first_omega_0") for call in measure.call_args_list}, {120.0})
            measure.reset_mock()
            gate04.run_gate(DEFAULT_CASES, precision="float64", device="cpu")
            self.assertEqual(measure.call_count, 2 * len(DEFAULT_CASES))
            self.assertEqual(
                {call.kwargs.get("first_omega_0") for call in measure.call_args_list}, {None})
            measure.reset_mock()
            reference, _rows = gate04.compute_r_ref(
                DEFAULT_CASES[:1], precision="float64", device="cpu", first_omega_0=60.0)
            self.assertEqual({call.kwargs["first_omega_0"] for call in measure.call_args_list}, {60.0})
            measure.reset_mock()
            gate04.evaluate_case(
                DEFAULT_CASES[0], reference, precision="float64", device="cpu", first_omega_0=240.0)
            self.assertEqual({call.kwargs["first_omega_0"] for call in measure.call_args_list}, {240.0})

    def test_the_recorded_rows_reproduce_the_committed_complete_pass(self):
        verdict = recorded_pass_verdict()
        artifact = committed_artifact()
        self.assertEqual(verdict.verdict, gate04.VERDICT_PASS)
        self.assertEqual(verdict.blocking_reasons, ())
        self.assertEqual(verdict.unratified_conditions, ())
        self.assertEqual(verdict.r_ref, artifact["r_ref"])
        self.assertEqual(
            [(case.label, case.seed) for case in verdict.cases],
            [(case.label, case.seed) for case in DEFAULT_CASES],
        )


# ---------------------------------------------------------------------------
# The tracer: a committed ruling to Phase 60 evidence, with the governed reference untouched.
# ---------------------------------------------------------------------------

class RemeasureCase(unittest.TestCase):
    """A temporary git repository holding the committed continue ruling. The real gate cannot run."""

    OMEGA = "120"

    def setUp(self):
        self.module = remeasure_module(self)
        for target, name in ((self.module, "run_gate"), (gate04, "_measure_raw_bin_means")):
            patcher = mock.patch.object(
                target, name, side_effect=AssertionError(f"the real {name} must not run in a test"))
            patcher.start()
            self.addCleanup(patcher.stop)
        self.governed_sha = sha256_file(GOVERNED)
        self.phase57_terminal = {
            path.name: sha256_file(path) for path in PHASE57_EVIDENCE.glob("terminal-state.json")
        }
        self.addCleanup(self.assert_governed_untouched)

    def assert_governed_untouched(self):
        self.assertEqual(sha256_file(GOVERNED), self.governed_sha)
        self.assertEqual(
            {path.name: sha256_file(path) for path in PHASE57_EVIDENCE.glob("terminal-state.json")},
            self.phase57_terminal,
        )

    def make_tree(self, answer="continue", value=OMEGA, *, commit=True):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1)
        tree.with_checkpoint4(answer, value, commit=commit)
        return tree

    def remeasure(self, tree, verdict, **kwargs):
        """``remeasure`` over ``tree`` with ``run_gate`` returning ``verdict``; ``(record, run_gate spy)``."""
        with mock.patch.object(self.module, "run_gate", return_value=verdict) as spy:
            record = self.module.remeasure(
                evidence_root=tree.evidence, repo_root=tree.root, **kwargs)
        return record, spy

    def main_function(self):
        main = getattr(self.module, "main", None)
        if main is None:
            self.fail(f"{MODULE} has no main yet")
        return main

    def cli(self, tree, verdict, *extra):
        """``main`` over ``tree`` with ``run_gate`` returning ``verdict``; ``(exit code, stdout, run_gate spy)``."""
        main = self.main_function()
        buffer = io.StringIO()
        with mock.patch.object(self.module, "run_gate", return_value=verdict) as spy:
            with contextlib.redirect_stdout(buffer):
                code = main(["--evidence-root", str(tree.evidence), *extra])
        return code, buffer.getvalue(), spy

    def assert_refused(self, tree, *, fragment=None):
        """Both entries refuse before the gate runs and write nothing."""
        before = snapshot(tree.root)
        with mock.patch.object(
                self.module, "run_gate", return_value=recorded_pass_verdict()) as spy:
            with self.assertRaises(self.module.RemeasureRefused) as raised:
                self.module.remeasure(evidence_root=tree.evidence, repo_root=tree.root)
        spy.assert_not_called()
        if fragment is not None:
            self.assertIn(fragment, str(raised.exception))
        code, out, spy = self.cli(tree, recorded_pass_verdict())
        self.assertEqual(code, self.module.EXIT_REFUSED)
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("GATE04-REFUSED"), out)
        spy.assert_not_called()
        self.assertEqual(snapshot(tree.root), before)
        self.assertFalse(self.continue_dir(tree).exists())

    @staticmethod
    def continue_dir(tree):
        return tree.evidence / "continue"

    def continue_names(self, tree):
        directory = self.continue_dir(tree)
        return sorted(path.name for path in directory.iterdir()) if directory.is_dir() else []


class RemeasureTracerTests(RemeasureCase):
    ABSOLUTE = re.compile(r'"(?:/|[A-Za-z]:\\)[^"\s]*"')

    def approved_rel(self):
        return g2.R_REF_APPROVED_REL.as_posix()

    def test_a_complete_pass_writes_the_evidence_the_reference_and_the_record(self):
        tree = self.make_tree()
        before = snapshot(tree.root)
        record, _spy = self.remeasure(
            tree, recorded_pass_verdict(), ruling_path=tree.root / PHASE_REL / RULING_NAME)
        self.assertEqual(self.continue_names(tree), [EVIDENCE_NAME, RECORD_NAME, APPROVED_NAME])
        after = snapshot(tree.root)
        added = sorted(set(after) - set(before))
        self.assertEqual(
            added,
            sorted((EVIDENCE_REL / "continue" / name).as_posix()
                   for name in (EVIDENCE_NAME, RECORD_NAME, APPROVED_NAME)),
        )
        self.assertEqual({key: after[key] for key in before}, before)
        self.assertEqual(record, tree.read(f"continue/{RECORD_NAME}"))

    def test_the_record_cites_the_ruling_the_reference_and_the_grid_facts(self):
        tree = self.make_tree()
        verdict = recorded_pass_verdict()
        record, _spy = self.remeasure(tree, verdict)
        approved = tree.path(f"continue/{APPROVED_NAME}")
        self.assertEqual(record["schema"], "phase60-gate04-remeasure/v1")
        self.assertEqual(record["schema"], g2.REMEASURE_SCHEMA)
        self.assertEqual(record["verdict"], "PASS")
        self.assertIs(record["complete_pass"], True)
        self.assertEqual(record["first_omega_0"], 120.0)
        self.assertEqual(record["ruling_sha256"], tree.ruling_sha())
        self.assertEqual(record["ruling_path"], (PHASE_REL / RULING_NAME).as_posix())
        self.assertEqual(record["r_ref"], verdict.r_ref)
        self.assertEqual(record["blocking_reasons"], [])
        self.assertEqual(record["unratified_conditions"], [])
        self.assertEqual(
            record["r_ref_artifact"], {"path": self.approved_rel(), "sha256": sha256_file(approved)})
        self.assertIs(record["on_grid"], True)
        self.assertIs(record["equals_confirmed"], True)
        self.assertIsInstance(record["wall_seconds"], float)
        self.assertGreaterEqual(record["wall_seconds"], 0.0)
        governed = sha256_file(GOVERNED)
        self.assertEqual(record["governed_r_ref_sha256"], {"before": governed, "after": governed})

    def test_the_gate_runs_once_on_the_default_cases_at_the_approved_setting(self):
        tree = self.make_tree()
        _record, spy = self.remeasure(tree, recorded_pass_verdict())
        spy.assert_called_once()
        args, kwargs = spy.call_args
        self.assertEqual(tuple(args[0]), DEFAULT_CASES)
        self.assertEqual(kwargs, {"precision": "float64", "device": "cpu", "first_omega_0": 120.0})

    def test_the_default_ruling_path_is_the_committed_checkpoint_4_file(self):
        tree = self.make_tree()
        record, _spy = self.remeasure(tree, recorded_pass_verdict())
        self.assertEqual(record["ruling_path"], (PHASE_REL / RULING_NAME).as_posix())

    def test_the_artifact_is_a_governed_style_reference_the_trainer_can_load(self):
        tree = self.make_tree()
        verdict = recorded_pass_verdict()
        self.remeasure(tree, verdict)
        approved = tree.path(f"continue/{APPROVED_NAME}")
        evidence = tree.path(f"continue/{EVIDENCE_NAME}")
        payload = json.loads(approved.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], gate04.R_REF_SCHEMA_VERSION)
        self.assertIs(payload["valid"], True)
        self.assertEqual(load_frozen_r_ref_artifact(approved), verdict.r_ref)
        provenance = payload["provenance"]
        self.assertEqual(
            provenance["gate_evidence_path"], (EVIDENCE_REL / "continue" / EVIDENCE_NAME).as_posix())
        self.assertEqual(provenance["gate_evidence_sha256"], sha256_file(evidence))
        self.assertEqual(provenance["gate_verdict"], "PASS")
        document = json.loads(evidence.read_text(encoding="utf-8"))
        self.assertEqual(document["schema_version"], gate04.EVIDENCE_SCHEMA_VERSION)
        self.assertEqual(set(document), set(gate04.EVIDENCE_TOP_LEVEL_KEYS))
        self.assertEqual(document["verdict"]["verdict"], "PASS")
        self.assertEqual(document["configuration"]["r_ref_path"], self.approved_rel())
        self.assertEqual(document["configuration"]["first_omega_0"], 120.0)
        self.assertEqual(len(document["cases"]), len(DEFAULT_CASES))
        self.assertIsNone(document["failure"])

    def test_the_governed_reference_is_unchanged_and_no_terminal_state_is_written(self):
        tree = self.make_tree()
        before = sha256_file(GOVERNED)
        with mock.patch.object(gate04, "main", side_effect=AssertionError("gate04 main ran")), \
                mock.patch.object(
                    gate04, "_write_terminal_state", side_effect=AssertionError("terminal state")):
            self.remeasure(tree, recorded_pass_verdict())
        self.assertEqual(sha256_file(GOVERNED), before)
        self.assertEqual(list(tree.root.rglob("terminal-state.json")), [])
        self.assertEqual(
            {path.name: sha256_file(path) for path in PHASE57_EVIDENCE.glob("terminal-state.json")},
            self.phase57_terminal,
        )

    def test_every_write_lands_under_the_continue_directory(self):
        tree = self.make_tree()
        allowed = self.continue_dir(tree).resolve()
        with WriteSpy() as spy:
            self.remeasure(tree, recorded_pass_verdict())
        self.assertTrue(spy.targets)
        for target in spy.targets:
            with self.subTest(target=target.name):
                self.assertTrue(
                    target.resolve().is_relative_to(allowed), f"a write outside {allowed.name}")
                self.assertNotEqual(target.resolve(), GOVERNED.resolve())

    def test_no_written_file_holds_the_home_directory_or_an_absolute_path(self):
        tree = self.make_tree()
        self.remeasure(tree, recorded_pass_verdict())
        names = self.continue_names(tree)
        self.assertEqual(len(names), 3)
        for name in names:
            text = tree.path(f"continue/{name}").read_text(encoding="utf-8")
            with self.subTest(file=name):
                self.assertNotIn(str(Path.home()), text)
                self.assertNotIn(str(tree.root), text)
                self.assertIsNone(self.ABSOLUTE.search(text))


# ---------------------------------------------------------------------------
# Task 2: the command line, BLOCK, refusals, non-canonical runs, a second run, the branch link.
# ---------------------------------------------------------------------------

class CommandLineTests(RemeasureCase):
    def test_a_complete_pass_prints_the_pass_token_and_exits_0(self):
        tree = self.make_tree()
        code, out, spy = self.cli(tree, recorded_pass_verdict())
        self.assertEqual(code, self.module.EXIT_PASS)
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("GATE04-PASS"), out)
        spy.assert_called_once()
        self.assertEqual(self.continue_names(tree), [EVIDENCE_NAME, RECORD_NAME, APPROVED_NAME])

    def test_the_command_line_takes_only_an_evidence_root(self):
        tree = self.make_tree()
        main = self.main_function()
        for flag in (
            "--r-ref-path", "--cases-config", "--ruling", "--precision", "--device",
            "--first-omega-0",
        ):
            with self.subTest(flag=flag), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    main([flag, "value", "--evidence-root", str(tree.evidence)])
        self.assertEqual(self.continue_names(tree), [])

    def test_help_lists_the_evidence_root_and_nothing_that_could_aim_at_the_governed_file(self):
        self.main_function()
        completed = subprocess.run(
            [sys.executable, "-B", "-m", MODULE, "--help"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--evidence-root", completed.stdout)
        for flag in ("--r-ref-path", "--cases-config", "--precision", "--device"):
            self.assertNotIn(flag, completed.stdout)


class BlockTests(RemeasureCase):
    REASON = "synthetic GATE-04 block for the tests"

    def test_main_exits_5_and_prints_the_block_token(self):
        tree = self.make_tree()
        code, out, spy = self.cli(tree, block_verdict(self.REASON))
        self.assertEqual(code, self.module.EXIT_BLOCK)
        self.assertEqual(code, 5)
        self.assertTrue(out.startswith("GATE04-BLOCK"), out)
        self.assertIn(self.REASON, out)
        spy.assert_called_once()
        self.assertEqual(spy.call_args.kwargs["first_omega_0"], 120.0)

    def test_the_record_says_block_with_the_reasons_and_no_reference_is_written(self):
        tree = self.make_tree()
        self.cli(tree, block_verdict(self.REASON))
        self.assertEqual(self.continue_names(tree), [EVIDENCE_NAME, RECORD_NAME])
        record = tree.read(f"continue/{RECORD_NAME}")
        governed = sha256_file(GOVERNED)
        self.assertEqual(record["schema"], g2.REMEASURE_SCHEMA)
        self.assertEqual(record["verdict"], "BLOCK")
        self.assertIs(record["complete_pass"], False)
        self.assertEqual(record["blocking_reasons"], [self.REASON])
        self.assertIsNone(record["r_ref_artifact"])
        self.assertEqual(record["r_ref"], "NaN")
        self.assertEqual(record["first_omega_0"], 120.0)
        self.assertEqual(record["ruling_sha256"], tree.ruling_sha())
        self.assertIs(record["on_grid"], True)
        self.assertIs(record["equals_confirmed"], True)
        self.assertEqual(record["governed_r_ref_sha256"], {"before": governed, "after": governed})
        document = tree.read(f"continue/{EVIDENCE_NAME}")
        self.assertEqual(document["verdict"]["verdict"], "BLOCK")
        self.assertEqual(document["cases"], [])
        self.assertIsNone(document["configuration"]["r_ref_path"])
        self.assertEqual(list(tree.root.rglob("terminal-state.json")), [])

    def test_the_ladder_stays_pending_for_the_owner_after_a_block(self):
        tree = self.make_tree()
        self.cli(tree, block_verdict(self.REASON))
        tree.commit("gate 04 re-measure block")
        ladder = tree.state("ladder")
        self.assertEqual((ladder.status, ladder.reason), ("PENDING", "GATE-04 BLOCK at 120.0; owner"))
        code, out = tree.cli("branch", "ladder")
        self.assertEqual(code, 4)
        self.assertEqual(out, "BRANCH-PENDING: ladder (GATE-04 BLOCK at 120.0; owner)")
        self.assertEqual(tree.state("continue-gate").status, "TAKEN")


class RefusalTests(RemeasureCase):
    def test_a_go_to_verdict_ruling_is_refused(self):
        self.assert_refused(self.make_tree("go-to-verdict", None), fragment="go-to-verdict")

    def test_an_uncommitted_ruling_is_refused(self):
        self.assert_refused(self.make_tree(commit=False), fragment="uncommitted")

    def test_a_missing_ruling_is_refused(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1)
        self.assert_refused(tree, fragment=RULING_NAME)

    def test_a_ruling_value_the_loader_rejects_is_refused(self):
        for value in ("0", "-5", "1e3", "nan"):
            with self.subTest(value=value):
                self.assert_refused(self.make_tree("continue", value))

    def test_a_value_that_fails_the_validation_is_refused_before_the_gate_runs(self):
        tree = self.make_tree()
        for value in (float("nan"), float("inf"), float("-inf"), 0.0, -30.0, True, "120", None):
            ruling = Checkpoint4Ruling(
                answer="continue", approved_first_omega_0=value,
                sha256=tree.ruling_sha(), path=(PHASE_REL / RULING_NAME).as_posix(),
            )
            with self.subTest(value=value):
                with mock.patch.object(self.module, "load_checkpoint4_ruling", return_value=ruling):
                    self.assert_refused(tree, fragment="first_omega_0")

    def test_a_missing_sweep_curve_is_refused(self):
        tree = Tree(self)
        tree.with_checkpoint4("continue", "120")
        self.assert_refused(tree, fragment="sweep-curve.json")

    def test_an_uncommitted_sweep_curve_is_refused(self):
        tree = self.make_tree()
        curve = tree.path("g2/sweep-curve.json")
        curve.write_text(curve.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        self.assert_refused(tree, fragment="uncommitted")


class NonCanonicalTests(RemeasureCase):
    def assert_not_complete(self, record, tree):
        self.assertIs(record["complete_pass"], False)
        self.assertEqual(record["verdict"], "BLOCK")
        self.assertIsNone(record["r_ref_artifact"])
        self.assertTrue(any("not a complete pass" in item for item in record["blocking_reasons"]))
        self.assertEqual(self.continue_names(tree), [EVIDENCE_NAME, RECORD_NAME])
        self.assertEqual(tree.read(f"continue/{RECORD_NAME}")["complete_pass"], False)

    def test_a_case_set_that_is_not_the_six_defaults_is_not_a_complete_pass(self):
        two = DEFAULT_CASES[:2]
        full = recorded_pass_verdict()
        short = dataclasses.replace(full, cases=full.cases[:2])
        for label, cases, verdict in (
            ("two cases asked, a six-case pass", two, full),
            ("two cases asked, a two-case pass", two, short),
            ("the defaults asked, a two-case pass", None, short),
        ):
            with self.subTest(case=label):
                tree = self.make_tree()
                record, spy = self.remeasure(tree, verdict, cases=cases)
                self.assertEqual(
                    tuple(spy.call_args.args[0]), DEFAULT_CASES if cases is None else cases)
                self.assert_not_complete(record, tree)

    def test_unratified_conditions_are_not_a_complete_pass(self):
        tree = self.make_tree()
        verdict = dataclasses.replace(recorded_pass_verdict(), unratified_conditions=("ii",))
        record, _spy = self.remeasure(tree, verdict)
        self.assert_not_complete(record, tree)
        self.assertEqual(record["unratified_conditions"], ["ii"])

    def test_the_default_cases_passed_explicitly_are_still_a_complete_pass(self):
        tree = self.make_tree()
        record, _spy = self.remeasure(tree, recorded_pass_verdict(), cases=DEFAULT_CASES)
        self.assertIs(record["complete_pass"], True)
        self.assertEqual(record["verdict"], "PASS")


class SecondRunTests(RemeasureCase):
    def test_a_second_run_refuses_before_measuring_and_writes_nothing(self):
        tree = self.make_tree()
        self.remeasure(tree, recorded_pass_verdict())
        before = snapshot(tree.root)
        raised = None
        with mock.patch.object(
                self.module, "run_gate", return_value=recorded_pass_verdict()) as spy:
            try:
                self.module.remeasure(evidence_root=tree.evidence, repo_root=tree.root)
            except Exception as exc:  # the type is asserted below, so a late failure reads as one
                raised = exc
        self.assertIsInstance(raised, self.module.RemeasureRefused)
        self.assertIn(RECORD_NAME, str(raised))
        spy.assert_not_called()
        self.assertEqual(snapshot(tree.root), before)

    def test_a_second_run_through_the_command_line_exits_2(self):
        tree = self.make_tree()
        self.cli(tree, recorded_pass_verdict())
        before = snapshot(tree.root)
        code, out, spy = self.cli(tree, recorded_pass_verdict())
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("GATE04-REFUSED"), out)
        spy.assert_not_called()
        self.assertEqual(snapshot(tree.root), before)

    def test_a_recorded_block_is_also_the_result_and_is_not_replaced_by_a_pass(self):
        tree = self.make_tree()
        self.cli(tree, block_verdict())
        before = snapshot(tree.root)
        code, out, spy = self.cli(tree, recorded_pass_verdict())
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("GATE04-REFUSED"), out)
        spy.assert_not_called()
        self.assertEqual(snapshot(tree.root), before)

    def test_a_leftover_output_without_a_record_refuses_and_is_left_alone(self):
        for name in (EVIDENCE_NAME, APPROVED_NAME):
            with self.subTest(leftover=name):
                tree = self.make_tree()
                leftover = tree.path(f"continue/{name}")
                leftover.parent.mkdir(parents=True, exist_ok=True)
                leftover.write_text("{}\n", encoding="utf-8")
                before = snapshot(tree.root)
                with mock.patch.object(
                        self.module, "run_gate", return_value=recorded_pass_verdict()) as spy:
                    with self.assertRaises(self.module.RemeasureRefused):
                        self.module.remeasure(evidence_root=tree.evidence, repo_root=tree.root)
                spy.assert_not_called()
                self.assertEqual(snapshot(tree.root), before)


class GovernedReferenceTests(RemeasureCase):
    def test_a_change_to_the_governed_file_during_the_run_halts_and_records_nothing(self):
        tree = self.make_tree()
        with tempfile.TemporaryDirectory(prefix="phase60-governed-") as scratch:
            stand_in = Path(scratch) / "r_ref_stage0.json"
            stand_in.write_bytes(GOVERNED.read_bytes())

            def tamper(*args, **kwargs):
                stand_in.write_bytes(stand_in.read_bytes() + b" ")
                return recorded_pass_verdict()

            with mock.patch.object(self.module, "R_REF_ARTIFACT_PATH", stand_in), \
                    mock.patch.object(self.module, "run_gate", side_effect=tamper):
                with self.assertRaises(self.module.RemeasureHalt):
                    self.module.remeasure(evidence_root=tree.evidence, repo_root=tree.root)
        self.assertNotIn(RECORD_NAME, self.continue_names(tree))


class BranchLinkTests(RemeasureCase):
    def test_a_pass_record_opens_the_ladder_at_the_approved_setting(self):
        tree = self.make_tree()
        self.remeasure(tree, recorded_pass_verdict())
        tree.commit("gate 04 re-measure")
        ladder = tree.state("ladder")
        self.assertEqual(
            (ladder.status, ladder.first_omega_0, ladder.omega_provenance),
            ("TAKEN", 120.0, "owner_approved"),
        )
        code, out = tree.cli("branch", "ladder")
        self.assertEqual(code, 0)
        self.assertEqual(out, "BRANCH-TAKEN: ladder (continue; first_omega_0 120.0; owner_approved)")
        self.assertEqual(tree.state("continue-gate").status, "TAKEN")

    def test_both_records_parse_under_the_ladders_reader(self):
        for label, verdict in (("PASS", recorded_pass_verdict()), ("BLOCK", block_verdict())):
            with self.subTest(verdict=label):
                tree = self.make_tree()
                record, _spy = self.remeasure(tree, verdict)
                parsed = g2.parse_remeasure(tree.read(f"continue/{RECORD_NAME}"))
                self.assertEqual(parsed.verdict, label)
                self.assertEqual(parsed.complete_pass, label == "PASS")
                self.assertEqual(parsed.first_omega_0, 120.0)
                self.assertEqual(parsed.ruling_sha256, tree.ruling_sha())
                self.assertEqual(parsed.r_ref_artifact, record["r_ref_artifact"])

    def test_settings_off_the_grid_or_not_confirmed_are_recorded_and_accepted(self):
        for value, on_grid, equals_confirmed in (
            ("37.5", False, False), ("240", True, False), ("120", True, True),
        ):
            with self.subTest(first_omega_0=value):
                tree = self.make_tree("continue", value)
                record, spy = self.remeasure(tree, recorded_pass_verdict())
                self.assertEqual(spy.call_args.kwargs["first_omega_0"], float(value))
                self.assertEqual(record["first_omega_0"], float(value))
                self.assertIs(record["on_grid"], on_grid)
                self.assertIs(record["equals_confirmed"], equals_confirmed)
                tree.commit("gate 04 re-measure")
                ladder = tree.state("ladder")
                self.assertEqual((ladder.status, ladder.first_omega_0), ("TAKEN", float(value)))


class ModuleContractTests(unittest.TestCase):
    def setUp(self):
        self.module = remeasure_module(self)

    def test_the_plan_names_are_exported(self):
        for name in ("remeasure", "main", "EXIT_PASS", "EXIT_BLOCK", "EXIT_REFUSED", "REMEASURE_SCHEMA"):
            with self.subTest(name=name):
                self.assertTrue(hasattr(self.module, name))
                self.assertIn(name, self.module.__all__)
        self.assertEqual(
            (self.module.EXIT_PASS, self.module.EXIT_REFUSED, self.module.EXIT_BLOCK), (0, 2, 5))
        self.assertEqual(self.module.REMEASURE_SCHEMA, "phase60-gate04-remeasure/v1")
        self.assertEqual(self.module.REMEASURE_SCHEMA, g2.REMEASURE_SCHEMA)

    def test_the_docstring_carries_the_phase_60_marker(self):
        self.assertEqual(
            self.module.__doc__.splitlines()[0],
            "Phase 60 (D-07): re-measure R_ref and re-run GATE-04 at an owner-approved first_omega_0.",
        )

    def test_the_module_never_imports_the_gate_command_line_or_the_arm_runner(self):
        source = Path(self.module.__file__).read_text(encoding="utf-8")
        imported_modules = set()
        gate_names = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
                for alias in node.names:
                    imported_modules.add(f"{node.module}.{alias.name}")
                if node.module == "pinn.verification.gate04_train_free":
                    gate_names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
        self.assertTrue(gate_names)
        self.assertFalse({"main", "_write_terminal_state"} & gate_names)
        self.assertNotIn("pinn.verification.learnability_run", imported_modules)
        self.assertNotIn("terminal-state", executable_source_from_text(source))


if __name__ == "__main__":
    unittest.main()
