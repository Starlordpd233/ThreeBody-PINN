"""Phase 60 (FEAS-03/04/09): tests for Gate G2, the sweep pair, skips and branch state.

Every test that reads evidence builds a synthetic git repository under a temporary
directory (the helpers of ``tests.phase59.test_evidence_verifier``) and writes plain
JSON records into it. The module under test decides only from files that are tracked and
clean in git, so each fixture commits what it writes. Nothing here touches the real
evidence tree, and no real ruling file is read or written: any ruling text a test needs
is synthetic and lives in a temporary directory.

The frozen scorecard rules (``g2_fires``, ``decision_verdict``) are called by the module
and are never re-implemented here; the tests compare the module's output with them.
"""

from __future__ import annotations

import ast
import atexit
import contextlib
import dataclasses
import hashlib
import io
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from pinn.verification import learnability_g2 as g2
from pinn.verification.feasibility_scorecard import (
    OwnerRouted,
    decision_verdict,
    g2_fires,
    load_scorecard,
)
from pinn.verification.learnability_arms import (
    EVIDENCE_REL,
    PANEL_SYSTEMS,
    PHASE_REL,
    RUN_SCHEMA,
)
from tests.phase59.test_evidence_verifier import commit_all, init_repo
from tests.phase60.test_ruling import checkpoint4, gap6009

ROOT = Path(__file__).resolve().parents[2]
CARD = load_scorecard()
SHA_A = "ab" * 32


def record_payload(arm_id, *, tier, omega=30.0, provenance="locked", hours=1.0,
                   seconds_per_step=2.0, run_kind="real", schema=RUN_SCHEMA, **result):
    """A minimal real-arm record: the fields the G2 module reads, nothing else."""
    body = {
        "state": "adam",
        "tier": tier,
        "E": 0.05,
        "e_in_max": 0.05,
        "h": [[0.01, 0.5], [0.1, 0.9]],
        "eps_h": 0.001,
    }
    body.update(result)
    return {
        "schema": schema,
        "diagnostic": True,
        "run_kind": run_kind,
        "arm_id": arm_id,
        "first_omega_0": omega,
        "omega_provenance": provenance,
        "result": body,
        "wall": {"hours": hours},
        "timing": {"seconds_per_step": seconds_per_step},
    }


def fake_records(tiers):
    """Rung-1 record summaries for the pure rule tests (no file behind them)."""
    return [
        g2.Rung1Record(
            system_id=system,
            arm_id=f"r1-{system}",
            path=f"evidence/arms/r1-{system}/record.json",
            sha256=SHA_A,
            tier=tier,
        )
        for system, tier in zip(PANEL_SYSTEMS, tiers)
    ]


def remeasure_payload(*, verdict="PASS", first_omega_0=120.0, ruling_sha256, complete_pass=None):
    """A synthetic GATE-04 re-measure record with the fields the branch query reads."""
    complete = (verdict == "PASS") if complete_pass is None else complete_pass
    payload = {
        "schema": "phase60-gate04-remeasure/v1",
        "verdict": verdict,
        "complete_pass": complete,
        "first_omega_0": first_omega_0,
        "ruling_sha256": ruling_sha256,
        "on_grid": first_omega_0 in (60.0, 120.0, 240.0, 480.0),
        "equals_confirmed": first_omega_0 == 120.0,
    }
    if verdict == "PASS":
        payload["r_ref_artifact"] = {
            "path": (EVIDENCE_REL / "continue" / "r-ref-approved.json").as_posix(),
            "sha256": "ab" * 32,
        }
    else:
        payload["blocking_reasons"] = ["synthetic fixture block"]
    return payload


_TEMPLATES = {}
_TEMPLATE_HOME = []


def _template_home():
    """One temporary directory for the whole process, holding the cached scenario repositories."""
    if not _TEMPLATE_HOME:
        home = tempfile.TemporaryDirectory(prefix="phase60-g2-templates-")
        atexit.register(home.cleanup)
        _TEMPLATE_HOME.append(home)
    return Path(_TEMPLATE_HOME[0].name).resolve()


class Tree:
    """A temporary git repository holding a synthetic Phase 60 evidence tree."""

    def __init__(self, test, *, root=None):
        self.test = test
        if root is None:
            tmp = tempfile.TemporaryDirectory(prefix="phase60-g2-")
            test.addCleanup(tmp.cleanup)
            root = Path(tmp.name).resolve()
            init_repo(root)
            (root / "README.md").write_text("synthetic repository for the G2 tests\n")
            commit_all(root, "init")
        self.root = Path(root)
        self.evidence = self.root / EVIDENCE_REL

    @classmethod
    def scenario(cls, test, key, build):
        """A private copy of a scenario that is built once per process.

        ``build(tree)`` must be deterministic. The copy is an ordinary repository the
        test may change freely; the records hold repo-relative paths only, so a copy
        reads exactly like the original.
        """
        template = _TEMPLATES.get(key)
        if template is None:
            template = _template_home() / f"scenario-{len(_TEMPLATES)}"
            template.mkdir()
            init_repo(template)
            (template / "README.md").write_text("synthetic repository for the G2 tests\n")
            commit_all(template, "init")
            build(cls(test, root=template))
            _TEMPLATES[key] = template
        tmp = tempfile.TemporaryDirectory(prefix="phase60-g2-")
        test.addCleanup(tmp.cleanup)
        copy = Path(tmp.name).resolve()
        shutil.copytree(template, copy, symlinks=True, dirs_exist_ok=True)
        return cls(test, root=copy)

    # -- files -----------------------------------------------------------------
    def path(self, relative):
        return self.evidence / relative

    def record_path(self, arm_id):
        return self.evidence / "arms" / arm_id / "record.json"

    def write_json(self, path, payload):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def write_record(self, arm_id, **kwargs):
        return self.write_json(self.record_path(arm_id), record_payload(arm_id, **kwargs))

    def write_rung1(self, tiers, *, hours=None, **kwargs):
        for index, (system, tier) in enumerate(zip(PANEL_SYSTEMS, tiers)):
            extra = dict(kwargs)
            if hours is not None:
                extra["hours"] = hours[index]
            self.write_record(f"r1-{system}", tier=tier, **extra)

    def commit(self, message="fixture"):
        return commit_all(self.root, message)

    def read(self, relative):
        return json.loads(self.path(relative).read_text(encoding="utf-8"))

    # -- the command line ------------------------------------------------------
    def cli(self, *argv):
        """Run ``main`` in this process; return ``(exit code, stdout text)``."""
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = g2.main([*argv, "--evidence-root", str(self.evidence)])
        return code, buffer.getvalue().strip()

    def cli_subprocess(self, *argv):
        completed = subprocess.run(
            [sys.executable, "-B", "-m", "pinn.verification.learnability_g2",
             *argv, "--evidence-root", str(self.evidence)],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120,
        )
        return completed.returncode, completed.stdout.strip(), completed.stderr

    def state(self, name):
        return g2.branch_state(name, evidence_root=self.evidence, repo_root=self.root)

    # -- scenario steps (each commits what it writes) --------------------------
    def with_outcome(self, tiers, **kwargs):
        """Write and commit three Rung-1 records, run ``outcome``, commit its file."""
        self.write_rung1(tiers, **kwargs)
        self.commit("rung 1 records")
        code, out = self.cli("outcome")
        self.test.assertEqual(code, 0, out)
        self.commit("g2 outcome")
        return self

    def sweep_system(self):
        return self.read("g2/g2-outcome.json")["sweep_system"]

    def with_sweep(self, tiers_by_omega, *, hours=None):
        """Write and commit the four sweep records of the recorded sweep system."""
        system = self.sweep_system()
        for index, (omega, tier) in enumerate(tiers_by_omega.items()):
            self.write_record(
                f"g2s-{system}-w{int(omega):03d}", tier=tier, omega=float(omega),
                provenance="g2_sweep_override",
                hours=1.0 if hours is None else hours[index],
            )
        self.commit("sweep records")
        return self

    def with_curve(self, tiers_by_omega, **kwargs):
        """Write the sweep records, run ``sweep-curve`` and commit the curve."""
        self.with_sweep(tiers_by_omega, **kwargs)
        code, out = self.cli("sweep-curve")
        self.test.assertEqual(code, 0, out)
        self.commit("sweep curve")
        return self

    def with_confirmation(self, tier, *, hours=1.0):
        """Write and commit the one confirmation record the curve names."""
        curve = self.read("g2/sweep-curve.json")
        self.write_record(
            curve["confirmation_arm"], tier=tier, omega=curve["confirmed_first_omega_0"],
            provenance="confirmation_override", hours=hours,
        )
        self.commit("confirmation record")
        return self

    def with_protocol(self, pre_answer):
        """Commit a run protocol whose g2 section holds the failed-confirmation pre-answer."""
        self.write_json(
            self.path("run-protocol.json"),
            {"schema": "phase60-run-protocol/v1",
             "g2": {"failed_confirmation_pre_answer": pre_answer}},
        )
        self.commit("run protocol")
        return self

    # -- the owner's rulings and the GATE-04 re-measure (synthetic stand-ins) ------
    CHECKPOINT4_NAME = "60-CHECKPOINT-4-RULING.md"
    GAP6009_NAME = "60-GAP-60-09-RULING.md"

    def put_ruling(self, name, text):
        target = self.root / PHASE_REL / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def with_checkpoint4(self, answer, value=None, *, commit=True, **kwargs):
        self.put_ruling(self.CHECKPOINT4_NAME, checkpoint4(answer, value, **kwargs))
        if commit:
            self.commit("checkpoint 4 ruling")
        return self

    def with_gap6009(self, reading, *, commit=True):
        self.put_ruling(self.GAP6009_NAME, gap6009(reading))
        if commit:
            self.commit("gap 60-09 ruling")
        return self

    def ruling_sha(self, name=CHECKPOINT4_NAME):
        return hashlib.sha256((self.root / PHASE_REL / name).read_bytes()).hexdigest()

    def with_remeasure(self, *, commit=True, **overrides):
        """Write the GATE-04 re-measure record (PASS at 120 under the committed ruling by default)."""
        options = {"ruling_sha256": self.ruling_sha()}
        options.update(overrides)
        self.write_json(self.path("continue/gate04-remeasure.json"), remeasure_payload(**options))
        if commit:
            self.commit("gate 04 re-measure")
        return self

    def with_rescue(self, tier, *, pre_answer=None, hours=1.0):
        """Confirmation record, protocol, then ``rescue``; commit rescue.json. Returns (code, out)."""
        self.with_confirmation(tier, hours=hours)
        self.with_protocol(pre_answer)
        result = self.cli("rescue")
        self.commit("rescue")
        return result


def outcome_tree(test, tiers, *, hours=None):
    """Three committed Rung-1 records and a committed outcome (built once per process)."""
    return Tree.scenario(
        test, ("outcome", tuple(tiers), hours),
        lambda tree: tree.with_outcome(tiers, **({} if hours is None else {"hours": hours})),
    )


def curve_tree(test, tiers, grid, *, rung1_hours=None, sweep_hours=None):
    """... and four committed sweep records and a committed sweep curve."""

    def build(tree):
        tree.with_outcome(tiers, **({} if rung1_hours is None else {"hours": rung1_hours}))
        tree.with_curve(grid, **({} if sweep_hours is None else {"hours": sweep_hours}))

    return Tree.scenario(
        test, ("curve", tuple(tiers), tuple(grid.items()), rung1_hours, sweep_hours), build
    )


def protocol_tree(test, tiers, grid, pre_answer):
    """... and a committed run protocol holding ``pre_answer``."""
    return Tree.scenario(
        test, ("protocol", tuple(tiers), tuple(grid.items()), pre_answer),
        lambda tree: (
            tree.with_outcome(tiers).with_curve(grid).with_protocol(pre_answer)
        ),
    )


def confirmed_tree(test, tiers, grid, confirmation_tier, pre_answer=None, *, protocol=True,
                   **hours):
    """... and the one committed confirmation record (``rescue`` has not been run).

    ``protocol=False`` leaves the run protocol out.
    """

    def build(tree):
        tree.with_outcome(tiers, **({"hours": hours["rung1"]} if "rung1" in hours else {}))
        tree.with_curve(grid, **({"hours": hours["sweep"]} if "sweep" in hours else {}))
        tree.with_confirmation(confirmation_tier, hours=hours.get("confirmation", 1.0))
        if protocol:
            tree.with_protocol(pre_answer)

    key = ("confirmed", tuple(tiers), tuple(grid.items()), confirmation_tier, pre_answer,
           protocol, tuple(sorted(hours.items())))
    return Tree.scenario(test, key, build)


def rescued_tree(test, tiers, grid, confirmation_tier, pre_answer=None, **hours):
    """... and ``rescue`` run and its file committed (whatever its exit code was)."""

    def build(tree):
        tree.with_outcome(tiers, **({"hours": hours["rung1"]} if "rung1" in hours else {}))
        tree.with_curve(grid, **({"hours": hours["sweep"]} if "sweep" in hours else {}))
        tree.with_rescue(confirmation_tier, pre_answer=pre_answer,
                         hours=hours.get("confirmation", 1.0))

    key = ("rescued", tuple(tiers), tuple(grid.items()), confirmation_tier, pre_answer,
           tuple(sorted(hours.items())))
    return Tree.scenario(test, key, build)


# ---------------------------------------------------------------------------
# Task 1: the rule, the pinned sweep pair, the outcome writer, the tracer query.
# ---------------------------------------------------------------------------

class G2RuleTests(unittest.TestCase):
    def outcome(self, tiers):
        return g2.g2_outcome(fake_records(tiers), scorecard=CARD)

    def test_two_or_more_systems_below_tier_one_fire(self):
        for tiers in ((0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)):
            with self.subTest(tiers=tiers):
                self.assertTrue(self.outcome(tiers)["g2_fired"])

    def test_exactly_one_system_below_tier_one_does_not_fire(self):
        for tiers in ((0, 1, 1), (1, 1, 0), (1, 1, 1), (2, 3, 1), (1, 0, 3)):
            with self.subTest(tiers=tiers):
                self.assertFalse(self.outcome(tiers)["g2_fired"])

    def test_a_tier_one_system_is_never_failing(self):
        outcome = self.outcome((1, 0, 1))
        self.assertEqual(outcome["failing_systems"], [851])
        self.assertEqual(self.outcome((1, 1, 1))["failing_systems"], [])
        self.assertEqual(self.outcome((0, 0, 0))["failing_systems"], [1632, 851, 4658])

    def test_the_flag_equals_the_frozen_rule_on_every_tier_triple(self):
        for tiers in itertools.product(range(4), repeat=3):
            with self.subTest(tiers=tiers):
                outcome = self.outcome(tiers)
                self.assertEqual(outcome["g2_fired"], g2_fires(list(tiers), scorecard=CARD))
                self.assertEqual(
                    outcome["failing_systems"],
                    [s for s, t in zip(PANEL_SYSTEMS, tiers) if t < 1],
                )

    def test_tiers_and_records_follow_the_panel_order(self):
        outcome = self.outcome((0, 2, 3))
        self.assertEqual(outcome["schema"], "phase60-g2-outcome/v1")
        self.assertEqual(outcome["panel_systems"], [1632, 851, 4658])
        self.assertEqual(outcome["tiers"], [0, 2, 3])
        self.assertEqual([r["system_id"] for r in outcome["records"]], [1632, 851, 4658])
        self.assertEqual([r["arm_id"] for r in outcome["records"]],
                         ["r1-1632", "r1-851", "r1-4658"])
        self.assertEqual({r["sha256"] for r in outcome["records"]}, {SHA_A})

    def test_a_fired_outcome_carries_the_pinned_pair_and_a_quiet_one_does_not(self):
        fired = self.outcome((0, 0, 1))
        self.assertEqual(
            (fired["sweep_system"], fired["confirmation_system"], fired["uncovered_system"]),
            (1632, 851, 4658),
        )
        quiet = self.outcome((1, 1, 0))
        for key in ("sweep_system", "confirmation_system", "uncovered_system"):
            self.assertNotIn(key, quiet)

    def test_records_must_be_the_three_panel_systems_in_order(self):
        records = fake_records((0, 0, 1))
        for label, bad in (
            ("two records", records[:2]),
            ("four records", records + records[:1]),
            ("swapped", [records[1], records[0], records[2]]),
            ("empty", []),
        ):
            with self.subTest(case=label):
                with self.assertRaises(ValueError):
                    g2.g2_outcome(bad, scorecard=CARD)

    def test_a_tier_that_is_not_an_integer_is_refused(self):
        for bad in (True, 1.0, "1", None):
            with self.subTest(tier=bad):
                records = fake_records((0, 0, 1))
                records[2] = dataclasses.replace(records[2], tier=bad)
                with self.assertRaises(ValueError):
                    g2.g2_outcome(records, scorecard=CARD)


class SweepPlanTests(unittest.TestCase):
    def test_the_four_pinned_cases(self):
        cases = (
            ([1632, 851, 4658], (1632, 851, 4658)),
            ([1632, 851], (1632, 851, 4658)),
            ([1632, 4658], (1632, 4658, 851)),
            ([851, 4658], (851, 4658, 1632)),
        )
        for failing, expected in cases:
            with self.subTest(failing=failing):
                self.assertEqual(g2.sweep_plan(failing), expected)

    def test_the_input_order_does_not_matter(self):
        self.assertEqual(g2.sweep_plan([4658, 1632, 851]), (1632, 851, 4658))
        self.assertEqual(g2.sweep_plan([4658, 851]), (851, 4658, 1632))
        self.assertEqual(g2.sweep_plan((4658, 1632)), (1632, 4658, 851))

    def test_the_pair_follows_the_pinned_lap_counts(self):
        from pinn.verification.learnability_arms import PANEL_INNER_LAPS

        self.assertEqual(PANEL_INNER_LAPS, {1632: 10.47, 851: 18.61, 4658: 39.35})
        for failing in ([1632, 851, 4658], [1632, 851], [1632, 4658], [851, 4658]):
            sweep, confirm, uncovered = g2.sweep_plan(failing)
            self.assertLess(PANEL_INNER_LAPS[sweep], PANEL_INNER_LAPS[confirm])
            self.assertEqual({sweep, confirm, uncovered}, set(PANEL_SYSTEMS))

    def test_fewer_than_two_failing_systems_is_a_value_error(self):
        for failing in ([], [1632], (851,), [4658]):
            with self.subTest(failing=failing):
                with self.assertRaises(ValueError):
                    g2.sweep_plan(failing)

    def test_ids_outside_the_panel_or_repeated_are_refused(self):
        for failing in ([1632, 1632], [1632, 7], [True, 851], ["1632", 851], [1632.0, 851]):
            with self.subTest(failing=failing):
                with self.assertRaises(ValueError):
                    g2.sweep_plan(failing)


class OutcomeWriterTests(unittest.TestCase):
    def test_the_outcome_file_records_tiers_hashes_and_the_pair(self):
        tree = Tree(self)
        tree.write_rung1((0, 0, 1))
        tree.commit("rung 1 records")
        code, out = tree.cli("outcome")
        self.assertEqual(code, 0, out)
        self.assertTrue(out.startswith("G2-OUTCOME-WRITTEN:"), out)
        self.assertEqual(len(out.splitlines()), 1)
        outcome = tree.read("g2/g2-outcome.json")
        self.assertEqual(outcome["schema"], "phase60-g2-outcome/v1")
        self.assertEqual(outcome["tiers"], [0, 0, 1])
        self.assertTrue(outcome["g2_fired"])
        self.assertEqual(outcome["failing_systems"], [1632, 851])
        self.assertEqual(
            (outcome["sweep_system"], outcome["confirmation_system"],
             outcome["uncovered_system"]),
            (1632, 851, 4658),
        )
        for entry in outcome["records"]:
            raw = tree.record_path(entry["arm_id"]).read_bytes()
            self.assertEqual(entry["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(entry["path"], tree.record_path(entry["arm_id"])
                             .relative_to(tree.root).as_posix())

    def test_each_failing_pair_gives_its_pinned_sweep_and_confirmation(self):
        cases = {
            (0, 0, 0): (1632, 851, 4658),
            (0, 0, 1): (1632, 851, 4658),
            (0, 1, 0): (1632, 4658, 851),
            (1, 0, 0): (851, 4658, 1632),
        }
        for tiers, expected in cases.items():
            with self.subTest(tiers=tiers):
                tree = outcome_tree(self, tiers)
                outcome = tree.read("g2/g2-outcome.json")
                self.assertEqual(
                    (outcome["sweep_system"], outcome["confirmation_system"],
                     outcome["uncovered_system"]),
                    expected,
                )

    def test_a_quiet_outcome_has_no_pair(self):
        tree = outcome_tree(self, (1, 1, 0))
        outcome = tree.read("g2/g2-outcome.json")
        self.assertFalse(outcome["g2_fired"])
        self.assertNotIn("sweep_system", outcome)
        self.assertEqual(outcome["failing_systems"], [4658])

    def test_the_command_line_runs_in_a_subprocess(self):
        tree = Tree(self)
        tree.write_rung1((0, 0, 1))
        tree.commit("rung 1 records")
        code, out, err = tree.cli_subprocess("outcome")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(len(out.splitlines()), 1)
        self.assertTrue(out.startswith("G2-OUTCOME-WRITTEN:"), out)
        self.assertTrue(tree.path("g2/g2-outcome.json").is_file())

    def test_a_second_call_exits_two_and_leaves_the_file_unchanged(self):
        tree = outcome_tree(self, (0, 0, 1))
        target = tree.path("g2/g2-outcome.json")
        before = target.read_bytes()
        code, out = tree.cli("outcome")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("G2-HALT:"), out)
        self.assertEqual(target.read_bytes(), before)

    def test_a_missing_rung_one_record_is_pending_and_writes_nothing(self):
        tree = Tree(self)
        tree.write_record("r1-1632", tier=0)
        tree.write_record("r1-851", tier=0)
        tree.commit("two of three")
        code, out = tree.cli("outcome")
        self.assertEqual(code, 4)
        self.assertTrue(out.startswith("BRANCH-PENDING:"), out)
        self.assertFalse(tree.path("g2").exists())

    def test_an_edited_record_halts_and_writes_nothing(self):
        tree = Tree(self)
        tree.write_rung1((0, 0, 1))
        tree.commit("rung 1 records")
        tree.write_record("r1-851", tier=3)  # tracked, then edited
        code, out = tree.cli("outcome")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("G2-HALT:"), out)
        self.assertIn("uncommitted", out)
        self.assertFalse(tree.path("g2/g2-outcome.json").exists())

    def test_an_untracked_record_halts_and_writes_nothing(self):
        tree = Tree(self)
        tree.write_record("r1-1632", tier=0)
        tree.write_record("r1-851", tier=0)
        tree.commit("two of three")
        tree.write_record("r1-4658", tier=1)  # present but never committed
        code, out = tree.cli("outcome")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("G2-HALT:"), out)
        self.assertIn("uncommitted", out)
        self.assertFalse(tree.path("g2/g2-outcome.json").exists())

    def test_a_record_that_is_not_a_real_rung_one_record_halts(self):
        for label, kwargs in (
            ("fixture kind", {"run_kind": "fixture"}),
            ("wrong schema", {"schema": "phase60-harness-run/v0"}),
        ):
            with self.subTest(case=label):
                tree = Tree(self)
                tree.write_rung1((0, 0, 1))
                tree.write_record("r1-851", tier=0, **kwargs)
                tree.commit("rung 1 records")
                code, out = tree.cli("outcome")
                self.assertEqual(code, 2)
                self.assertIn("G2-HALT", out)
                self.assertFalse(tree.path("g2/g2-outcome.json").exists())

    def test_a_symbolic_link_in_place_of_a_record_halts(self):
        tree = Tree(self)
        tree.write_record("r1-1632", tier=0)
        tree.write_record("r1-851", tier=0)
        target = tree.root / "elsewhere.json"
        tree.write_json(target, record_payload("r1-4658", tier=1))
        link = tree.record_path("r1-4658")
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target)
        tree.commit("a link in place of a record")
        code, out = tree.cli("outcome")
        self.assertEqual(code, 2)
        self.assertIn("symbolic link", out)
        self.assertFalse(tree.path("g2/g2-outcome.json").exists())

    def test_a_record_filed_under_the_wrong_arm_halts(self):
        tree = Tree(self)
        tree.write_rung1((0, 0, 1))
        tree.write_json(tree.record_path("r1-851"), record_payload("r1-4658", tier=0))
        tree.commit("rung 1 records")
        code, out = tree.cli("outcome")
        self.assertEqual(code, 2)
        self.assertIn("r1-851", out)

    def test_a_record_with_no_integer_tier_halts(self):
        for bad in (None, True, "1", 1.5):
            with self.subTest(tier=bad):
                tree = Tree(self)
                tree.write_rung1((0, 0, 1))
                tree.write_record("r1-4658", tier=bad)
                tree.commit("rung 1 records")
                code, out = tree.cli("outcome")
                self.assertEqual(code, 2)
                self.assertFalse(tree.path("g2/g2-outcome.json").exists())

    def test_the_outcome_holds_no_home_or_absolute_path(self):
        tree = outcome_tree(self, (0, 0, 1))
        text = tree.path("g2/g2-outcome.json").read_text(encoding="utf-8")
        self.assertNotIn(str(Path.home()), text)
        self.assertNotIn(str(tree.root), text)
        self.assertNotIn("/Users/", text)


class BranchTracerTests(unittest.TestCase):
    NAMES = ("sweep", "confirmation", "owner-decision", "stop", "continue-gate", "ladder")

    def test_with_no_outcome_every_branch_is_pending(self):
        tree = Tree(self)
        for name in self.NAMES:
            with self.subTest(name=name):
                state = tree.state(name)
                self.assertEqual((state.name, state.status), (name, "PENDING"))
                code, out = tree.cli("branch", name)
                self.assertEqual(code, 4)
                self.assertTrue(out.startswith(f"BRANCH-PENDING: {name}"), out)

    def test_a_fired_outcome_takes_the_sweep_branch(self):
        tree = outcome_tree(self, (0, 0, 1))
        state = tree.state("sweep")
        self.assertEqual(state.status, "TAKEN")
        self.assertIsNone(state.first_omega_0)
        code, out = tree.cli("branch", "sweep")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("BRANCH-TAKEN: sweep"), out)
        self.assertEqual(len(out.splitlines()), 1)

    def test_a_quiet_outcome_leaves_the_sweep_branch_not_taken(self):
        tree = outcome_tree(self, (1, 1, 0))
        self.assertEqual(tree.state("sweep").status, "NOT-TAKEN")
        code, out = tree.cli("branch", "sweep")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("BRANCH-NOT-TAKEN: sweep"), out)

    def test_a_quiet_outcome_takes_the_ladder_at_the_locked_setting(self):
        tree = outcome_tree(self, (1, 1, 0))
        state = tree.state("ladder")
        self.assertEqual(state.status, "TAKEN")
        self.assertEqual(state.first_omega_0, 30.0)
        self.assertEqual(state.omega_provenance, "locked")
        self.assertEqual(state.reason, "g2 passed; first_omega_0 30.0")

    def test_the_command_line_prints_the_ladder_token_in_a_subprocess(self):
        tree = outcome_tree(self, (1, 1, 1))
        code, out, err = tree.cli_subprocess("branch", "ladder")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(out, "BRANCH-TAKEN: ladder (g2 passed; first_omega_0 30.0)")
        code, out, err = tree.cli_subprocess("branch", "sweep")
        self.assertEqual(code, 0, out + err)
        self.assertTrue(out.startswith("BRANCH-NOT-TAKEN: sweep"), out)

    def test_a_fired_outcome_leaves_the_ladder_pending(self):
        tree = outcome_tree(self, (0, 0, 1))
        state = tree.state("ladder")
        self.assertEqual(state.status, "PENDING")
        code, out = tree.cli("branch", "ladder")
        self.assertEqual(code, 4)
        self.assertTrue(out.startswith("BRANCH-PENDING: ladder"), out)

    def test_an_uncommitted_outcome_makes_every_branch_pending(self):
        tree = Tree(self)
        tree.write_rung1((1, 1, 0))
        tree.commit("rung 1 records")
        self.assertEqual(tree.cli("outcome")[0], 0)  # written, not committed
        relative = tree.path("g2/g2-outcome.json").relative_to(tree.root).as_posix()
        for name in self.NAMES:
            with self.subTest(name=name):
                state = tree.state(name)
                self.assertEqual(state.status, "PENDING")
                self.assertEqual(state.reason, f"uncommitted {relative}")

    def test_an_edited_outcome_makes_the_branch_pending(self):
        tree = outcome_tree(self, (1, 1, 0))
        target = tree.path("g2/g2-outcome.json")
        payload = json.loads(target.read_text())
        payload["g2_fired"] = True
        tree.write_json(target, payload)
        state = tree.state("ladder")
        self.assertEqual(state.status, "PENDING")
        self.assertTrue(state.reason.startswith("uncommitted "))

    def test_a_committed_outcome_that_disagrees_with_the_records_halts(self):
        tree = outcome_tree(self, (1, 1, 0))
        target = tree.path("g2/g2-outcome.json")
        payload = json.loads(target.read_text())
        payload["g2_fired"] = True
        payload["sweep_system"] = 1632
        tree.write_json(target, payload)
        tree.commit("tamper")
        with self.assertRaises(g2.G2Halt):
            tree.state("sweep")
        code, out = tree.cli("branch", "sweep")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("G2-HALT:"), out)

    def test_a_committed_outcome_whose_record_changed_halts(self):
        tree = outcome_tree(self, (1, 1, 0))
        tree.write_record("r1-4658", tier=3)  # tier changes after the outcome
        tree.commit("rewrite a record")
        with self.assertRaises(g2.G2Halt):
            tree.state("ladder")

    def test_a_committed_outcome_whose_record_is_gone_halts(self):
        tree = outcome_tree(self, (1, 1, 0))
        tree.record_path("r1-851").unlink()
        tree.commit("remove a record")
        with self.assertRaises(g2.G2Halt):
            tree.state("sweep")

    def test_the_state_is_a_frozen_value_with_a_closed_vocabulary(self):
        tree = outcome_tree(self, (1, 1, 0))
        state = tree.state("ladder")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            state.status = "PENDING"
        self.assertEqual((g2.TAKEN, g2.NOT_TAKEN, g2.PENDING), ("TAKEN", "NOT-TAKEN", "PENDING"))
        self.assertEqual(g2.EXIT_BRANCH_PENDING, 4)

    def test_an_unknown_branch_name_is_refused(self):
        tree = Tree(self)
        with self.assertRaises(ValueError):
            tree.state("rung3")
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                tree.cli("branch", "rung3")


# ---------------------------------------------------------------------------
# Task 2: the confirmation choice, the sweep curve, the rescue outcome, the skip
# records, the stop handoff and the sweep-related branch states.
# ---------------------------------------------------------------------------

LATER = ("rung2b_counts", "rung3_counts", "control_branch", "rung1_beats_formula")
NO_RESCUE = "no rescue"
GO_TO_VERDICT = "checkpoint \u2463 answered go to the verdict"
ZERO_GRID = {60: 0, 120: 0, 240: 0, 480: 0}
ONE_AT_120 = {60: 0, 120: 1, 240: 0, 480: 0}


class VerdictSpy:
    """Stands in for ``decision_verdict``: records each call's keywords, then calls the frozen rule."""

    def __init__(self):
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append(dict(kwargs))
        return decision_verdict(**kwargs)


class ConfirmedOmegaTests(unittest.TestCase):
    @staticmethod
    def rows(tiers_by_omega):
        return [{"first_omega_0": float(o), "tier": t} for o, t in tiers_by_omega.items()]

    def test_the_highest_setting_that_reached_tier_one_is_confirmed(self):
        cases = (
            ({60: 0, 120: 1, 240: 0, 480: 0}, 120.0),
            ({60: 1, 120: 2, 240: 1, 480: 0}, 240.0),
            ({60: 1, 120: 1, 240: 1, 480: 1}, 480.0),
            ({60: 3, 120: 0, 240: 0, 480: 0}, 60.0),
            ({60: 0, 120: 3, 240: 0, 480: 1}, 480.0),
        )
        for tiers, expected in cases:
            with self.subTest(tiers=tiers):
                self.assertEqual(g2.confirmed_omega(self.rows(tiers), scorecard=CARD), expected)

    def test_no_setting_at_tier_one_confirms_nothing(self):
        self.assertIsNone(g2.confirmed_omega(self.rows(ZERO_GRID), scorecard=CARD))

    def test_tier_exactly_one_counts_as_reaching(self):
        self.assertEqual(g2.confirmed_omega(self.rows({60: 1, 120: 0, 240: 0, 480: 0}),
                                            scorecard=CARD), 60.0)

    def test_row_order_does_not_matter(self):
        base = self.rows({60: 1, 120: 2, 240: 1, 480: 0})
        for ordering in itertools.permutations(base):
            self.assertEqual(g2.confirmed_omega(list(ordering), scorecard=CARD), 240.0)

    def test_the_answer_is_always_one_of_the_recorded_settings(self):
        for tiers in itertools.product(range(4), repeat=4):
            rows = self.rows(dict(zip((60, 120, 240, 480), tiers)))
            answer = g2.confirmed_omega(rows, scorecard=CARD)
            self.assertTrue(answer is None or answer in (60.0, 120.0, 240.0, 480.0))
            reaching = [r["first_omega_0"] for r in rows if r["tier"] >= 1]
            self.assertEqual(answer, max(reaching) if reaching else None)

    def test_the_rescue_tier_is_read_from_the_scorecard(self):
        stand_in = SimpleNamespace(section=lambda name: {"rescue_tier": 2})
        rows = self.rows({60: 1, 120: 2, 240: 1, 480: 0})
        self.assertEqual(g2.confirmed_omega(rows, scorecard=stand_in), 120.0)

    def test_duplicate_or_malformed_rows_are_refused(self):
        for label, rows in (
            ("repeated setting", [{"first_omega_0": 60.0, "tier": 1}, {"first_omega_0": 60.0, "tier": 0}]),
            ("bool tier", [{"first_omega_0": 60.0, "tier": True}]),
            ("float tier", [{"first_omega_0": 60.0, "tier": 1.0}]),
            ("zero setting", [{"first_omega_0": 0.0, "tier": 1}]),
            ("nan setting", [{"first_omega_0": float("nan"), "tier": 1}]),
            ("bool setting", [{"first_omega_0": True, "tier": 1}]),
            ("missing tier", [{"first_omega_0": 60.0}]),
        ):
            with self.subTest(case=label):
                with self.assertRaises(ValueError):
                    g2.confirmed_omega(rows, scorecard=CARD)


class SweepCurveTests(unittest.TestCase):
    def test_the_curve_needs_all_four_records_of_the_recorded_sweep_system(self):
        for present in (0, 3):
            with self.subTest(present=present):
                tree = outcome_tree(self, (0, 0, 1))
                for omega, tier in list(ONE_AT_120.items())[:present]:
                    tree.write_record(f"g2s-1632-w{omega:03d}", tier=tier, omega=float(omega),
                                      provenance="g2_sweep_override")
                if present:
                    tree.commit("some sweep records")
                code, out = tree.cli("sweep-curve")
                self.assertEqual(code, 4)
                self.assertTrue(out.startswith("BRANCH-PENDING:"), out)
                self.assertFalse(tree.path("g2/sweep-curve.json").exists())

    def test_rows_carry_setting_arm_hash_tier_error_energy_and_horizons(self):
        tree = outcome_tree(self, (0, 0, 1))
        for index, omega in enumerate((60, 120, 240, 480)):
            tree.write_record(
                f"g2s-1632-w{omega:03d}", tier=index % 2, omega=float(omega),
                provenance="g2_sweep_override", E=0.1 + index, eps_h=0.01 * (index + 1),
                h=[[0.01, 0.1 * (index + 1)], [0.1, 0.2 * (index + 1)]],
            )
        tree.commit("sweep records")
        code, out = tree.cli("sweep-curve")
        self.assertEqual(code, 0, out)
        self.assertEqual(len(out.splitlines()), 1)
        self.assertTrue(out.startswith("SWEEP-CURVE-WRITTEN:"), out)
        curve = tree.read("g2/sweep-curve.json")
        self.assertEqual(curve["schema"], "phase60-sweep-curve/v1")
        self.assertEqual([r["first_omega_0"] for r in curve["rows"]], [60.0, 120.0, 240.0, 480.0])
        self.assertEqual([r["arm_id"] for r in curve["rows"]],
                         [f"g2s-1632-w{w:03d}" for w in (60, 120, 240, 480)])
        for index, row in enumerate(curve["rows"]):
            raw = tree.record_path(row["arm_id"]).read_bytes()
            self.assertEqual(row["record_sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(row["tier"], index % 2)
            self.assertEqual(row["E"], 0.1 + index)
            self.assertEqual(row["eps_h"], 0.01 * (index + 1))
            self.assertEqual(row["h"], [[0.01, 0.1 * (index + 1)], [0.1, 0.2 * (index + 1)]])
        outcome = tree.read("g2/g2-outcome.json")
        self.assertEqual(curve["sweep_system"], outcome["sweep_system"])
        self.assertEqual(curve["confirmation_system"], outcome["confirmation_system"])
        self.assertEqual(curve["uncovered_system"], outcome["uncovered_system"])
        self.assertEqual(curve["grid"], [60.0, 120.0, 240.0, 480.0])
        self.assertEqual(
            curve["g2_outcome_sha256"],
            hashlib.sha256(tree.path("g2/g2-outcome.json").read_bytes()).hexdigest(),
        )

    def test_the_selected_row_and_the_other_labels(self):
        tree = curve_tree(self, (0, 0, 1), {60: 1, 120: 2, 240: 1, 480: 0})
        curve = tree.read("g2/sweep-curve.json")
        self.assertEqual(curve["outcome"], "confirmation_pending")
        self.assertEqual(curve["confirmed_first_omega_0"], 240.0)
        self.assertEqual(curve["confirmation_arm"], "g2c-851-w240")
        labels = {row["first_omega_0"]: row["label"] for row in curve["rows"]}
        self.assertEqual(labels, {
            60.0: "reached Tier 1, not confirmed (one-confirmation budget)",
            120.0: "reached Tier 1, not confirmed (one-confirmation budget)",
            240.0: "selected for confirmation",
            480.0: "below Tier 1",
        })
        self.assertEqual(labels[60.0], g2.NOT_CONFIRMED_LABEL)

    def test_no_setting_at_tier_one_means_no_rescue_and_no_confirmation(self):
        tree = curve_tree(self, (0, 0, 1), ZERO_GRID)
        curve = tree.read("g2/sweep-curve.json")
        self.assertEqual(curve["outcome"], "no_rescue")
        self.assertIsNone(curve["confirmation_arm"])
        self.assertIsNone(curve["confirmed_first_omega_0"])
        self.assertEqual({row["label"] for row in curve["rows"]}, {"below Tier 1"})

    def test_the_confirmation_names_the_pinned_system_for_each_failing_pair(self):
        cases = (
            ((0, 0, 1), 1632, "g2c-851-w120"),
            ((1, 0, 0), 851, "g2c-4658-w120"),
            ((0, 1, 0), 1632, "g2c-4658-w120"),
            ((0, 0, 0), 1632, "g2c-851-w120"),
        )
        for rung1, sweep_system, confirmation_arm in cases:
            with self.subTest(rung1=rung1):
                tree = curve_tree(self, rung1, ONE_AT_120)
                curve = tree.read("g2/sweep-curve.json")
                self.assertEqual(curve["sweep_system"], sweep_system)
                self.assertEqual(curve["confirmation_arm"], confirmation_arm)
                self.assertEqual([row["arm_id"] for row in curve["rows"]],
                                 [f"g2s-{sweep_system}-w{w:03d}" for w in (60, 120, 240, 480)])

    def test_only_the_recorded_sweep_systems_arms_are_read(self):
        tree = outcome_tree(self, (0, 0, 1))
        for omega in (60, 120, 240, 480):  # another system's sweep arms must not count
            tree.write_record(f"g2s-851-w{omega:03d}", tier=3, omega=float(omega),
                              provenance="g2_sweep_override")
        tree.with_curve(ZERO_GRID)
        self.assertEqual(tree.read("g2/sweep-curve.json")["outcome"], "no_rescue")

    def test_a_record_run_at_another_setting_or_provenance_halts(self):
        for label, kwargs in (
            ("another setting", {"omega": 240.0}),
            ("locked provenance", {"provenance": "locked"}),
            ("confirmation provenance", {"provenance": "confirmation_override"}),
        ):
            with self.subTest(case=label):
                tree = outcome_tree(self, (0, 0, 1))
                for omega in (60, 240, 480):
                    tree.write_record(f"g2s-1632-w{omega:03d}", tier=0, omega=float(omega),
                                      provenance="g2_sweep_override")
                options = {"omega": 120.0, "provenance": "g2_sweep_override"}
                options.update(kwargs)
                tree.write_record("g2s-1632-w120", tier=1, **options)
                tree.commit("sweep records")
                code, out = tree.cli("sweep-curve")
                self.assertEqual(code, 2)
                self.assertIn("g2s-1632-w120", out)
                self.assertFalse(tree.path("g2/sweep-curve.json").exists())

    def test_a_record_without_the_scorecard_horizons_halts(self):
        for label, horizons in (
            ("another first horizon", [[0.02, 0.3], [0.1, 0.9]]),
            ("one horizon only", [[0.01, 0.3]]),
            ("not a list of pairs", "0.01"),
        ):
            with self.subTest(case=label):
                tree = outcome_tree(self, (0, 0, 1))
                for omega in (60, 240, 480):
                    tree.write_record(f"g2s-1632-w{omega:03d}", tier=0, omega=float(omega),
                                      provenance="g2_sweep_override")
                tree.write_record("g2s-1632-w120", tier=1, omega=120.0,
                                  provenance="g2_sweep_override", h=horizons)
                tree.commit("sweep records")
                code, out = tree.cli("sweep-curve")
                self.assertEqual(code, 2, out)
                self.assertIn("result.h", out)
                self.assertFalse(tree.path("g2/sweep-curve.json").exists())

    def test_an_uncommitted_sweep_record_halts(self):
        tree = outcome_tree(self, (0, 0, 1))
        for omega in (60, 120, 240):
            tree.write_record(f"g2s-1632-w{omega:03d}", tier=0, omega=float(omega),
                              provenance="g2_sweep_override")
        tree.commit("three of four")
        tree.write_record("g2s-1632-w480", tier=1, omega=480.0, provenance="g2_sweep_override")
        code, out = tree.cli("sweep-curve")
        self.assertEqual(code, 2)
        self.assertIn("uncommitted", out)
        self.assertFalse(tree.path("g2/sweep-curve.json").exists())

    def test_a_quiet_outcome_has_no_sweep(self):
        tree = outcome_tree(self, (1, 1, 0))
        code, out = tree.cli("sweep-curve")
        self.assertEqual(code, 2)
        self.assertIn("did not fire", out)

    def test_an_uncommitted_outcome_is_not_a_basis_for_a_curve(self):
        tree = Tree(self)
        tree.write_rung1((0, 0, 1))
        tree.commit("rung 1 records")
        self.assertEqual(tree.cli("outcome")[0], 0)  # not committed
        code, out = tree.cli("sweep-curve")
        self.assertEqual(code, 2)
        self.assertIn("uncommitted", out)

    def test_a_second_call_exits_two_and_leaves_the_file_unchanged(self):
        tree = curve_tree(self, (0, 0, 1), ONE_AT_120)
        target = tree.path("g2/sweep-curve.json")
        before = target.read_bytes()
        code, out = tree.cli("sweep-curve")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("G2-HALT:"), out)
        self.assertEqual(target.read_bytes(), before)

    def test_the_curve_holds_no_home_or_absolute_path(self):
        tree = curve_tree(self, (0, 0, 1), ONE_AT_120)
        text = tree.path("g2/sweep-curve.json").read_text(encoding="utf-8")
        self.assertNotIn(str(Path.home()), text)
        self.assertNotIn(str(tree.root), text)


class RescueTests(unittest.TestCase):
    @staticmethod
    def spied(tree, *argv):
        spy = VerdictSpy()
        with mock.patch.object(g2, "decision_verdict", spy):
            code, out = tree.cli(*argv)
        return code, out, spy

    def confirmed(self, confirmation_tier, pre_answer=None, **kwargs):
        return confirmed_tree(self, (0, 0, 1), ONE_AT_120, confirmation_tier, pre_answer, **kwargs)

    def assert_no_later_rung_inputs(self, spy):
        for call in spy.calls:
            for name in LATER:
                self.assertIsNone(call[name], name)
            self.assertIs(call["g2_fired"], True)

    def test_a_confirmed_rescue_writes_the_file_then_routes_to_checkpoint_four(self):
        for tier in (1, 2, 3):
            with self.subTest(tier=tier):
                tree = self.confirmed(tier)
                code, out, spy = self.spied(tree, "rescue")
                self.assertEqual(code, 3)
                self.assertEqual(out, "OWNER-ROUTED: owner checkpoint 4")
                self.assertEqual(len(spy.calls), 1)  # reached the handler once, never retried
                self.assertIs(spy.calls[0]["sweep_rescued"], True)
                self.assert_no_later_rung_inputs(spy)
                rescue = tree.read("g2/rescue.json")
                self.assertEqual(rescue["schema"], "phase60-rescue/v1")
                self.assertEqual(rescue["outcome"], "rescue")
                self.assertEqual(rescue["tier"], tier)
                self.assertEqual(rescue["confirmation_arm"], "g2c-851-w120")
                self.assertEqual(rescue["confirmed_first_omega_0"], 120.0)
                self.assertIsNone(rescue["pre_answer"])

    def test_the_record_hashes_and_results_are_carried(self):
        tree = self.confirmed(1)
        self.assertEqual(self.spied(tree, "rescue")[0], 3)
        rescue = tree.read("g2/rescue.json")
        raw = tree.record_path("g2c-851-w120").read_bytes()
        self.assertEqual(rescue["record"]["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(rescue["record"]["path"],
                         tree.record_path("g2c-851-w120").relative_to(tree.root).as_posix())
        self.assertEqual(rescue["sweep_curve_sha256"],
                         hashlib.sha256(tree.path("g2/sweep-curve.json").read_bytes()).hexdigest())
        self.assertEqual((rescue["E"], rescue["eps_h"], rescue["h"]),
                         (0.05, 0.001, [[0.01, 0.5], [0.1, 0.9]]))

    def test_a_confirmed_rescue_is_a_rescue_whatever_the_pre_answer(self):
        for pre in (None, "no_rescue", "rescue"):
            with self.subTest(pre=pre):
                tree = self.confirmed(1, pre_answer=pre)
                code, out, spy = self.spied(tree, "rescue")
                self.assertEqual((code, out), (3, "OWNER-ROUTED: owner checkpoint 4"))
                self.assertEqual(tree.read("g2/rescue.json")["outcome"], "rescue")
                self.assertEqual(tree.read("g2/rescue.json")["pre_answer"], pre)

    def test_a_failed_confirmation_with_no_pre_answer_stops_for_the_owner(self):
        tree = self.confirmed(0)
        code, out, spy = self.spied(tree, "rescue")
        self.assertEqual(code, 3)
        self.assertEqual(out, "OWNER-ROUTED: failed confirmation (GAP-60-09)")
        self.assertEqual(spy.calls, [])  # decision_verdict is not called
        rescue = tree.read("g2/rescue.json")
        self.assertEqual(rescue["outcome"], "failed_confirmation")
        self.assertEqual(rescue["tier"], 0)
        self.assertIsNone(rescue["pre_answer"])

    def test_a_failed_confirmation_pre_answered_no_rescue_goes_to_the_stop_path(self):
        tree = self.confirmed(0, pre_answer="no_rescue")
        code, out, spy = self.spied(tree, "rescue")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("RESCUE-WRITTEN:"), out)
        self.assertEqual(spy.calls, [])
        rescue = tree.read("g2/rescue.json")
        self.assertEqual((rescue["outcome"], rescue["pre_answer"]), ("failed_confirmation", "no_rescue"))

    def test_a_failed_confirmation_pre_answered_rescue_goes_to_checkpoint_four(self):
        tree = self.confirmed(0, pre_answer="rescue")
        code, out, spy = self.spied(tree, "rescue")
        self.assertEqual((code, out), (3, "OWNER-ROUTED: owner checkpoint 4"))
        self.assertEqual(len(spy.calls), 1)
        self.assertIs(spy.calls[0]["sweep_rescued"], True)
        self.assert_no_later_rung_inputs(spy)
        rescue = tree.read("g2/rescue.json")
        self.assertEqual((rescue["outcome"], rescue["pre_answer"]), ("failed_confirmation", "rescue"))

    def test_the_functions_raise_the_owner_stops_and_return_the_stop_path_normally(self):
        raising = self.confirmed(1)
        with self.assertRaises(OwnerRouted) as caught:
            g2.rescue_outcome(evidence_root=raising.evidence, repo_root=raising.root,
                              scorecard=CARD, pre_answer=None)
        self.assertIn("owner checkpoint 4", str(caught.exception))
        failed = self.confirmed(0)
        with self.assertRaises(g2.FailedConfirmationOwnerStop) as caught:
            g2.rescue_outcome(evidence_root=failed.evidence, repo_root=failed.root,
                              scorecard=CARD, pre_answer=None)
        self.assertEqual(str(caught.exception), "failed confirmation (GAP-60-09)")
        self.assertNotIsInstance(caught.exception, OwnerRouted)
        quiet = self.confirmed(0, pre_answer="no_rescue")
        payload = g2.rescue_outcome(evidence_root=quiet.evidence, repo_root=quiet.root,
                                    scorecard=CARD, pre_answer="no_rescue")
        self.assertEqual(payload["outcome"], "failed_confirmation")

    def test_an_invalid_pre_answer_is_refused_before_anything_is_written(self):
        tree = self.confirmed(0)
        for bad in ("maybe", "", "No_Rescue", 0, False, ["rescue"]):
            with self.subTest(pre=bad):
                with self.assertRaises(ValueError):
                    g2.rescue_outcome(evidence_root=tree.evidence, repo_root=tree.root,
                                      scorecard=CARD, pre_answer=bad)
        self.assertFalse(tree.path("g2/rescue.json").exists())

    def test_the_protocol_must_be_committed_and_hold_the_pre_answer_key(self):
        def fresh():
            return self.confirmed(0, protocol=False)

        missing = fresh()
        cases = [("missing protocol", missing)]
        no_key = fresh()
        no_key.write_json(no_key.path("run-protocol.json"), {"g2": {}})
        no_key.commit("protocol without the key")
        cases.append(("no key", no_key))
        no_section = fresh()
        no_section.write_json(no_section.path("run-protocol.json"), {"schema": "x"})
        no_section.commit("protocol without a g2 section")
        cases.append(("no g2 section", no_section))
        bad_value = fresh()
        bad_value.with_protocol("maybe")
        cases.append(("bad value", bad_value))
        untracked = fresh()
        untracked.write_json(
            untracked.path("run-protocol.json"),
            {"g2": {"failed_confirmation_pre_answer": "no_rescue"}},
        )
        cases.append(("untracked", untracked))
        dirty = fresh().with_protocol(None)
        dirty.write_json(dirty.path("run-protocol.json"),
                         {"g2": {"failed_confirmation_pre_answer": "no_rescue"}})
        cases.append(("edited", dirty))
        for label, tree in cases:
            with self.subTest(case=label):
                code, out, spy = self.spied(tree, "rescue")
                self.assertEqual(code, 2, out)
                self.assertTrue(out.startswith("G2-HALT:"), out)
                self.assertEqual(spy.calls, [])
                self.assertFalse(tree.path("g2/rescue.json").exists())

    def test_the_confirmation_record_must_be_there_committed_and_the_one_named(self):
        pending = protocol_tree(self, (0, 0, 1), ONE_AT_120, None)
        code, out = pending.cli("rescue")
        self.assertEqual(code, 4)
        self.assertTrue(out.startswith("BRANCH-PENDING:"), out)
        self.assertFalse(pending.path("g2/rescue.json").exists())

        uncommitted = protocol_tree(self, (0, 0, 1), ONE_AT_120, None)
        uncommitted.write_record("g2c-851-w120", tier=1, omega=120.0,
                                 provenance="confirmation_override")
        code, out = uncommitted.cli("rescue")
        self.assertEqual(code, 2)
        self.assertIn("uncommitted", out)

        for label, kwargs in (
            ("another setting", {"omega": 240.0}),
            ("sweep provenance", {"provenance": "g2_sweep_override"}),
        ):
            with self.subTest(case=label):
                wrong = protocol_tree(self, (0, 0, 1), ONE_AT_120, None)
                options = {"omega": 120.0, "provenance": "confirmation_override"}
                options.update(kwargs)
                wrong.write_record("g2c-851-w120", tier=1, **options)
                wrong.commit("confirmation record")
                code, out = wrong.cli("rescue")
                self.assertEqual(code, 2)
                self.assertFalse(wrong.path("g2/rescue.json").exists())

    def test_a_sweep_with_no_tier_one_setting_has_nothing_to_confirm(self):
        tree = protocol_tree(self, (0, 0, 1), ZERO_GRID, None)
        code, out, spy = self.spied(tree, "rescue")
        self.assertEqual(code, 2)
        self.assertIn("no confirmation", out)
        self.assertEqual(spy.calls, [])
        self.assertFalse(tree.path("g2/rescue.json").exists())

    def test_a_second_run_exits_two_and_does_not_route_again(self):
        tree = self.confirmed(1)
        self.assertEqual(self.spied(tree, "rescue")[0], 3)
        target = tree.path("g2/rescue.json")
        before = target.read_bytes()
        code, out, spy = self.spied(tree, "rescue")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("G2-HALT:"), out)
        self.assertEqual(spy.calls, [])
        self.assertEqual(target.read_bytes(), before)

    def test_the_command_line_exits_three_in_a_subprocess(self):
        tree = self.confirmed(1)
        code, out, err = tree.cli_subprocess("rescue")
        self.assertEqual(code, 3, out + err)
        self.assertEqual(out, "OWNER-ROUTED: owner checkpoint 4")


class SkipWriterTests(unittest.TestCase):
    LADDER_IDS = tuple(
        [f"{family}-{system}" for family in ("r2a", "r2b") for system in PANEL_SYSTEMS]
        + [f"{family}-{system}" for family in ("p1", "p2b") for system in (2279, 3418)]
        + [f"{family}-{system}" for family in ("c-r1u", "c-r2a", "c-r2b") for system in PANEL_SYSTEMS]
        + [f"{family}-{system}" for family in ("c-p1", "c-p2b") for system in (2279, 3418)]
    )

    def no_rescue_tree(self):
        return curve_tree(self, (0, 0, 1), ZERO_GRID)

    def write(self, tree, reason):
        return tree.cli("skip", "--reason", reason)

    def test_the_two_reasons_are_byte_exact(self):
        self.assertEqual(g2.SKIP_REASONS, (NO_RESCUE, GO_TO_VERDICT))
        self.assertEqual(g2.SKIP_REASONS[1].encode("utf-8"),
                         b"checkpoint \xe2\x91\xa3 answered go to the verdict")
        self.assertIn("\u2463", g2.SKIP_REASONS[1])
        self.assertEqual(g2.LEVEL3_SKIPPED, "not tested (skipped at G2)")

    def test_only_the_two_exact_strings_are_accepted(self):
        tree = self.no_rescue_tree()
        for bad in (
            "no rescue ", " no rescue", "No rescue", "no  rescue", "no_rescue", "norescue",
            "checkpoint 4 answered go to the verdict",
            "checkpoint \u2463 answered go to the verdict ",
            "checkpoint \u2463 answered go to the Verdict",
            "checkpoint \u2462 answered go to the verdict",
            "a third reason", "", "skipped at G2",
        ):
            with self.subTest(reason=bad):
                with self.assertRaises(g2.G2Halt):
                    g2.write_skip_records(bad, evidence_root=tree.evidence, repo_root=tree.root)
                self.assertFalse(tree.path("g2/skip-records.json").exists())
        for bad in (None, 7, b"no rescue", ["no rescue"]):
            with self.subTest(reason=bad):
                with self.assertRaises(g2.G2Halt):
                    g2.write_skip_records(bad, evidence_root=tree.evidence, repo_root=tree.root)

    def test_a_no_rescue_skip_writes_entries_for_both_requirements(self):
        tree = self.no_rescue_tree()
        code, out = self.write(tree, NO_RESCUE)
        self.assertEqual(code, 0, out)
        self.assertTrue(out.startswith("SKIP-RECORDS-WRITTEN:"), out)
        record = tree.read("g2/skip-records.json")
        self.assertEqual(record["schema"], "phase60-skip-records/v1")
        self.assertEqual(record["reason"], NO_RESCUE)
        for requirement in ("FEAS-04", "FEAS-09"):
            self.assertIs(record["entries"][requirement]["skipped"], True)
            self.assertEqual(record["entries"][requirement]["reason"], NO_RESCUE)
        self.assertEqual(record["level3"], "not tested (skipped at G2)")
        self.assertNotIn("not reached", json.dumps(record))
        cited = {entry["path"] for entry in record["basis"]}
        self.assertIn(tree.path("g2/g2-outcome.json").relative_to(tree.root).as_posix(), cited)
        self.assertIn(tree.path("g2/sweep-curve.json").relative_to(tree.root).as_posix(), cited)

    def test_the_reason_must_match_the_path_the_records_imply(self):
        tree = self.no_rescue_tree()
        code, out = self.write(tree, GO_TO_VERDICT)
        self.assertEqual(code, 2)
        self.assertIn("G2-HALT", out)
        self.assertFalse(tree.path("g2/skip-records.json").exists())
        self.assertEqual(self.write(tree, NO_RESCUE)[0], 0)

    def test_a_failed_confirmation_pre_answered_no_rescue_is_a_no_rescue_skip(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, "no_rescue")
        self.assertTrue(tree.path("g2/rescue.json").is_file())
        self.assertEqual(self.write(tree, NO_RESCUE)[0], 0)

    def test_no_skip_when_the_ladder_continues_or_is_undecided(self):
        passed = outcome_tree(self, (1, 1, 0))
        undecided = outcome_tree(self, (0, 0, 1))
        awaiting = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1)
        for label, tree, expected in (
            ("g2 passed", passed, 2), ("no sweep curve", undecided, 4), ("rescue awaiting", awaiting, 4),
        ):
            with self.subTest(case=label):
                for reason in g2.SKIP_REASONS:
                    code, out = self.write(tree, reason)
                    self.assertEqual(code, expected, out)
                    self.assertFalse(tree.path("g2/skip-records.json").exists())

    def test_any_started_ladder_arm_refuses_the_write(self):
        self.assertEqual(len(self.LADDER_IDS), 23)
        tree = self.no_rescue_tree()
        for arm_id in self.LADDER_IDS:
            for label, directory in (
                ("evidence", tree.evidence / "arms" / arm_id),
                ("run", tree.root / "runs" / "phase60" / arm_id),
            ):
                with self.subTest(arm=arm_id, kind=label):
                    directory.mkdir(parents=True)
                    try:
                        code, out = self.write(tree, NO_RESCUE)
                        self.assertEqual(code, 2, out)
                        self.assertIn(arm_id, out)
                        self.assertFalse(tree.path("g2/skip-records.json").exists())
                    finally:
                        directory.rmdir()
        self.assertEqual(self.write(tree, NO_RESCUE)[0], 0)

    def test_the_rung_one_sweep_and_confirmation_directories_do_not_refuse(self):
        tree = self.no_rescue_tree()
        (tree.root / "runs" / "phase60" / "r1-1632").mkdir(parents=True)
        (tree.root / "runs" / "phase60" / "g2s-1632-w060").mkdir(parents=True)
        (tree.evidence / "arms" / "g2c-851-w120").mkdir(parents=True)
        self.assertEqual(self.write(tree, NO_RESCUE)[0], 0)

    def test_a_second_write_is_refused_and_leaves_the_file_unchanged(self):
        tree = self.no_rescue_tree()
        self.assertEqual(self.write(tree, NO_RESCUE)[0], 0)
        target = tree.path("g2/skip-records.json")
        before = target.read_bytes()
        code, out = self.write(tree, NO_RESCUE)
        self.assertEqual(code, 2)
        self.assertEqual(target.read_bytes(), before)

    def test_the_skip_holds_no_home_or_absolute_path(self):
        tree = self.no_rescue_tree()
        self.write(tree, NO_RESCUE)
        text = tree.path("g2/skip-records.json").read_text(encoding="utf-8")
        self.assertNotIn(str(Path.home()), text)
        self.assertNotIn(str(tree.root), text)
        self.assertNotIn("\u2463", text)  # canonical JSON is ASCII; the digit is escaped

    def test_the_command_line_takes_the_circled_digit_reason_through_argv(self):
        tree = self.no_rescue_tree()
        code, out, err = tree.cli_subprocess("skip", "--reason", GO_TO_VERDICT)
        self.assertEqual(code, 2, out + err)  # the records imply no rescue, not this reason
        code, out, err = tree.cli_subprocess("skip", "--reason", NO_RESCUE)
        self.assertEqual(code, 0, out + err)


class StopHandoffTests(unittest.TestCase):
    ARMS = ("r1-1632", "r1-851", "r1-4658",
            "g2s-1632-w060", "g2s-1632-w120", "g2s-1632-w240", "g2s-1632-w480")

    def seven_arm_tree(self):
        return curve_tree(self, (0, 0, 1), ZERO_GRID, rung1_hours=(1.5, 2.25, 3.0),
                          sweep_hours=(0.5, 0.75, 1.25, 2.0))

    @staticmethod
    def expected_verdict():
        return decision_verdict(g2_fired=True, sweep_rescued=False, rung2b_counts=None,
                                rung3_counts=None, control_branch=None,
                                rung1_beats_formula=None, scorecard=CARD)

    def test_the_no_rescue_handoff_holds_the_frozen_verdict_and_the_hours(self):
        tree = self.seven_arm_tree()
        spy = VerdictSpy()
        with mock.patch.object(g2, "decision_verdict", spy):
            code, out = tree.cli("stop-handoff")
        self.assertEqual(code, 0, out)
        self.assertTrue(out.startswith("STOP-HANDOFF-WRITTEN:"), out)
        self.assertEqual(len(spy.calls), 1)
        self.assertIs(spy.calls[0]["sweep_rescued"], False)
        for name in LATER:
            self.assertIsNone(spy.calls[0][name])
        handoff = tree.read("g2/stop-handoff.json")
        self.assertEqual(handoff["schema"], "phase60-stop-handoff/v1")
        self.assertEqual(handoff["stop_reason"], NO_RESCUE)
        self.assertEqual(handoff["verdict"], self.expected_verdict())
        self.assertEqual(handoff["verdict"]["verdict"], "RETHINK-REPRESENTATION")
        self.assertEqual(handoff["level3"], "not tested (skipped at G2)")
        self.assertNotEqual(handoff["level3"], "not reached")
        self.assertEqual(handoff["phases_61_63"], "skipped at G2, not failed")
        self.assertEqual(handoff["next_phase"], 64)
        self.assertEqual([arm["arm_id"] for arm in handoff["arms"]], list(self.ARMS))
        self.assertEqual([arm["wall_hours"] for arm in handoff["arms"]],
                         [1.5, 2.25, 3.0, 0.5, 0.75, 1.25, 2.0])
        self.assertAlmostEqual(handoff["total_wall_hours"], 11.25, places=12)
        self.assertEqual([arm["seconds_per_step"] for arm in handoff["arms"]], [2.0] * 7)
        for arm in handoff["arms"]:
            raw = tree.record_path(arm["arm_id"]).read_bytes()
            self.assertEqual(arm["record"]["sha256"], hashlib.sha256(raw).hexdigest())

    def test_a_confirmation_run_adds_its_hours_as_the_eighth_arm(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, "no_rescue", rung1=(1.5, 2.25, 3.0),
                            sweep=(0.5, 0.75, 1.25, 2.0), confirmation=4.5)
        code, out = tree.cli("stop-handoff")
        self.assertEqual(code, 0, out)
        handoff = tree.read("g2/stop-handoff.json")
        self.assertEqual(handoff["stop_reason"], NO_RESCUE)
        self.assertEqual([arm["arm_id"] for arm in handoff["arms"]],
                         list(self.ARMS) + ["g2c-851-w120"])
        self.assertAlmostEqual(handoff["total_wall_hours"], 15.75, places=12)

    def test_a_record_without_wall_hours_halts_the_handoff(self):
        tree = outcome_tree(self, (0, 0, 1))
        tree.with_sweep(ZERO_GRID)
        payload = json.loads(tree.record_path("g2s-1632-w060").read_text())
        del payload["wall"]
        tree.write_json(tree.record_path("g2s-1632-w060"), payload)
        tree.commit("a record without hours")
        self.assertEqual(tree.cli("sweep-curve")[0], 0)
        tree.commit("curve")
        code, out = tree.cli("stop-handoff")
        self.assertEqual(code, 2)
        self.assertIn("wall", out)
        self.assertFalse(tree.path("g2/stop-handoff.json").exists())

    def test_the_handoff_is_refused_unless_the_records_stop_the_ladder(self):
        passed = outcome_tree(self, (1, 1, 0))
        awaiting = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1)
        for label, tree, expected in (("g2 passed", passed, 2), ("rescue awaiting", awaiting, 4)):
            with self.subTest(case=label):
                spy = VerdictSpy()
                with mock.patch.object(g2, "decision_verdict", spy):
                    code, out = tree.cli("stop-handoff")
                self.assertEqual(code, expected, out)
                self.assertEqual(spy.calls, [])
                self.assertFalse(tree.path("g2/stop-handoff.json").exists())

    def test_a_started_ladder_arm_refuses_the_handoff(self):
        tree = self.seven_arm_tree()
        (tree.evidence / "arms" / "r2b-1632").mkdir(parents=True)
        code, out = tree.cli("stop-handoff")
        self.assertEqual(code, 2)
        self.assertIn("r2b-1632", out)

    def test_a_second_handoff_is_refused(self):
        tree = self.seven_arm_tree()
        self.assertEqual(tree.cli("stop-handoff")[0], 0)
        target = tree.path("g2/stop-handoff.json")
        before = target.read_bytes()
        self.assertEqual(tree.cli("stop-handoff")[0], 2)
        self.assertEqual(target.read_bytes(), before)

    def test_the_handoff_holds_no_home_or_absolute_path(self):
        tree = self.seven_arm_tree()
        tree.cli("stop-handoff")
        text = tree.path("g2/stop-handoff.json").read_text(encoding="utf-8")
        self.assertNotIn(str(Path.home()), text)
        self.assertNotIn(str(tree.root), text)


class BranchSweepTests(unittest.TestCase):
    NAMES = BranchTracerTests.NAMES

    def states(self, tree):
        return {name: tree.state(name) for name in self.NAMES}

    def statuses(self, tree):
        return {name: state.status for name, state in self.states(tree).items()}

    def test_a_sweep_with_no_tier_one_setting_stops_with_no_rescue(self):
        tree = curve_tree(self, (0, 0, 1), ZERO_GRID)
        self.assertEqual(self.statuses(tree), {
            "sweep": "TAKEN", "confirmation": "NOT-TAKEN", "owner-decision": "NOT-TAKEN",
            "stop": "TAKEN", "continue-gate": "NOT-TAKEN", "ladder": "NOT-TAKEN",
        })
        self.assertIn(NO_RESCUE, tree.state("stop").reason)
        code, out = tree.cli("branch", "stop")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("BRANCH-TAKEN: stop"), out)

    def test_a_tier_one_setting_takes_the_confirmation_and_leaves_the_rest_pending(self):
        tree = curve_tree(self, (0, 0, 1), ONE_AT_120)
        statuses = self.statuses(tree)
        self.assertEqual(statuses["confirmation"], "TAKEN")
        self.assertIn("g2c-851-w120", tree.state("confirmation").reason)
        for name in ("owner-decision", "stop", "continue-gate", "ladder"):
            self.assertEqual(statuses[name], "PENDING", name)

    def test_the_confirmation_branch_follows_the_curve_not_the_arms(self):
        pending = outcome_tree(self, (0, 0, 1))
        self.assertEqual(pending.state("confirmation").status, "PENDING")
        quiet = outcome_tree(self, (1, 1, 1))
        self.assertEqual(quiet.state("confirmation").status, "NOT-TAKEN")

    def test_a_confirmed_rescue_takes_the_owner_decision(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1)
        statuses = self.statuses(tree)
        self.assertEqual(statuses["owner-decision"], "TAKEN")
        for name in ("stop", "continue-gate", "ladder"):
            self.assertEqual(statuses[name], "PENDING", name)
        self.assertIn("checkpoint 4", tree.state("stop").reason)

    def test_a_failed_confirmation_pre_answered_no_rescue_takes_the_stop(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, "no_rescue")
        self.assertEqual(self.statuses(tree), {
            "sweep": "TAKEN", "confirmation": "TAKEN", "owner-decision": "NOT-TAKEN",
            "stop": "TAKEN", "continue-gate": "NOT-TAKEN", "ladder": "NOT-TAKEN",
        })
        self.assertIn(NO_RESCUE, tree.state("stop").reason)

    def test_a_failed_confirmation_without_or_with_a_rescue_pre_answer_asks_the_owner(self):
        for pre in (None, "rescue"):
            with self.subTest(pre=pre):
                tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, pre)
                statuses = self.statuses(tree)
                self.assertEqual(statuses["owner-decision"], "TAKEN")
                for name in ("stop", "continue-gate", "ladder"):
                    self.assertEqual(statuses[name], "PENDING", name)

    def test_a_confirmed_rescue_still_asks_the_owner_whatever_the_pre_answer(self):
        for pre in ("no_rescue", "rescue", None):
            with self.subTest(pre=pre):
                tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1, pre)
                self.assertEqual(tree.state("owner-decision").status, "TAKEN")
                for name in ("stop", "continue-gate", "ladder"):
                    self.assertEqual(tree.state(name).status, "PENDING", name)

    def test_a_quiet_outcome_leaves_every_other_branch_not_taken(self):
        tree = outcome_tree(self, (1, 1, 0))
        self.assertEqual(self.statuses(tree), {
            "sweep": "NOT-TAKEN", "confirmation": "NOT-TAKEN", "owner-decision": "NOT-TAKEN",
            "stop": "NOT-TAKEN", "continue-gate": "NOT-TAKEN", "ladder": "TAKEN",
        })

    def test_a_skip_beside_a_ladder_taken_state_halts(self):
        tree = outcome_tree(self, (1, 1, 0))
        tree.write_json(tree.path("g2/skip-records.json"),
                        {"schema": "phase60-skip-records/v1", "reason": NO_RESCUE})
        tree.commit("a skip beside a passed gate")
        with self.assertRaises(g2.G2Halt):
            tree.state("ladder")
        code, out = tree.cli("branch", "ladder")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("G2-HALT:"), out)

    def test_a_skip_keeps_the_ladder_not_taken_on_a_stop(self):
        tree = curve_tree(self, (0, 0, 1), ZERO_GRID)
        self.assertEqual(tree.cli("skip", "--reason", NO_RESCUE)[0], 0)
        tree.commit("skip records")
        state = tree.state("ladder")
        self.assertEqual(state.status, "NOT-TAKEN")
        self.assertEqual(tree.state("stop").status, "TAKEN")

    def test_a_skip_with_the_wrong_reason_beside_a_stop_halts(self):
        tree = curve_tree(self, (0, 0, 1), ZERO_GRID)
        tree.write_json(tree.path("g2/skip-records.json"),
                        {"schema": "phase60-skip-records/v1", "reason": GO_TO_VERDICT})
        tree.commit("a skip with another reason")
        with self.assertRaises(g2.G2Halt):
            tree.state("ladder")

    def test_a_skip_keeps_the_ladder_closed_while_the_records_are_undecided(self):
        tree = curve_tree(self, (0, 0, 1), ONE_AT_120)
        tree.write_json(tree.path("g2/skip-records.json"),
                        {"schema": "phase60-skip-records/v1", "reason": NO_RESCUE})
        tree.commit("a skip before the confirmation ran")
        self.assertEqual(tree.state("ladder").status, "NOT-TAKEN")

    def test_an_uncommitted_skip_makes_the_ladder_pending(self):
        tree = curve_tree(self, (0, 0, 1), ZERO_GRID)
        self.assertEqual(tree.cli("skip", "--reason", NO_RESCUE)[0], 0)  # written, not committed
        state = tree.state("ladder")
        self.assertEqual(state.status, "PENDING")
        self.assertTrue(state.reason.startswith("uncommitted "), state.reason)
        self.assertTrue(state.reason.endswith("skip-records.json"), state.reason)

    def test_an_uncommitted_curve_makes_the_downstream_branches_pending(self):
        tree = outcome_tree(self, (0, 0, 1)).with_sweep(ZERO_GRID)
        self.assertEqual(tree.cli("sweep-curve")[0], 0)  # written, not committed
        for name in ("confirmation", "owner-decision", "stop", "continue-gate", "ladder"):
            state = tree.state(name)
            self.assertEqual(state.status, "PENDING", name)
            self.assertTrue(state.reason.startswith("uncommitted "), state.reason)
        self.assertEqual(tree.state("sweep").status, "TAKEN")

    def test_a_curve_that_disagrees_with_its_records_halts(self):
        tree = curve_tree(self, (0, 0, 1), ONE_AT_120)
        curve = tree.read("g2/sweep-curve.json")
        curve["confirmation_arm"] = "g2c-851-w480"
        curve["confirmed_first_omega_0"] = 480.0
        tree.write_json(tree.path("g2/sweep-curve.json"), curve)
        tree.commit("tamper with the curve")
        for name in ("confirmation", "stop", "ladder"):
            with self.subTest(name=name):
                with self.assertRaises(g2.G2Halt):
                    tree.state(name)

    def test_a_curve_whose_sweep_record_changed_halts(self):
        tree = curve_tree(self, (0, 0, 1), ZERO_GRID)
        tree.write_record("g2s-1632-w240", tier=3, omega=240.0, provenance="g2_sweep_override")
        tree.commit("rewrite a sweep record")
        with self.assertRaises(g2.G2Halt):
            tree.state("stop")

    def test_a_rescue_file_that_disagrees_with_the_confirmation_record_halts(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1)
        rescue = tree.read("g2/rescue.json")
        rescue["outcome"] = "failed_confirmation"
        tree.write_json(tree.path("g2/rescue.json"), rescue)
        tree.commit("tamper with the rescue")
        with self.assertRaises(g2.G2Halt):
            tree.state("owner-decision")

    def test_a_rescue_file_recorded_under_another_pre_answer_halts(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, "no_rescue")
        tree.with_protocol("rescue")  # the protocol now says something else
        with self.assertRaises(g2.G2Halt):
            tree.state("stop")

    def test_the_rescue_file_without_a_protocol_halts(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, "no_rescue")
        tree.path("run-protocol.json").unlink()
        tree.commit("remove the protocol")
        with self.assertRaises(g2.G2Halt):
            tree.state("stop")


class ModuleContractTests(unittest.TestCase):
    """What the module's source promises about owner stops and the frozen verdict rule."""

    @classmethod
    def setUpClass(cls):
        cls.source = Path(g2.__file__).read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    @staticmethod
    def handler_names(handler):
        node = handler.type
        if node is None:
            return {"<bare>"}
        elements = node.elts if isinstance(node, ast.Tuple) else [node]
        names = set()
        for element in elements:
            if isinstance(element, ast.Name):
                names.add(element.id)
            elif isinstance(element, ast.Attribute):
                names.add(element.attr)
        return names

    def test_owner_stops_are_handled_in_main_and_nowhere_else(self):
        stops = {"OwnerRouted", "FailedConfirmationOwnerStop"}
        outside, inside = [], []

        class Scan(ast.NodeVisitor):
            def __init__(self):
                self.stack = []

            def visit_FunctionDef(self, node):
                self.stack.append(node.name)
                self.generic_visit(node)
                self.stack.pop()

            def visit_ExceptHandler(self, node):
                if ModuleContractTests.handler_names(node) & stops:
                    (inside if self.stack == ["main"] else outside).append(node.lineno)
                self.generic_visit(node)

        Scan().visit(self.tree)
        self.assertEqual(outside, [])
        self.assertGreaterEqual(len(inside), 2)  # both stops are handled in main

    def test_every_decision_verdict_call_passes_none_for_each_later_rung_input(self):
        calls = [node for node in ast.walk(self.tree)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                 and node.func.id == "decision_verdict"]
        self.assertGreaterEqual(len(calls), 2)
        for call in calls:
            keywords = {keyword.arg: keyword.value for keyword in call.keywords}
            self.assertTrue(keywords["g2_fired"].value is True)
            for name in LATER:
                self.assertIsInstance(keywords[name], ast.Constant, name)
                self.assertIsNone(keywords[name].value, name)

    def test_the_module_does_not_import_the_runner(self):
        names = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        self.assertFalse([n for n in names if n.endswith("learnability_run")], names)
        self.assertFalse([n for n in names if n.startswith("pinn.train") or n.startswith("pinn.evaluate")])


# ---------------------------------------------------------------------------
# Task 3: the owner's committed rulings, the continue gate and the ladder.
# ---------------------------------------------------------------------------

class RemeasureRecordTests(unittest.TestCase):
    SHA = "cd" * 32

    def payload(self, **overrides):
        return {**remeasure_payload(ruling_sha256=self.SHA), **overrides}

    def test_the_constants_name_the_continue_evidence(self):
        self.assertEqual(g2.REMEASURE_REL, EVIDENCE_REL / "continue" / "gate04-remeasure.json")
        self.assertEqual(g2.R_REF_APPROVED_REL, EVIDENCE_REL / "continue" / "r-ref-approved.json")
        self.assertEqual(g2.REMEASURE_SCHEMA, "phase60-gate04-remeasure/v1")

    def test_a_pass_record_reads_its_fields(self):
        record = g2.parse_remeasure(self.payload())
        self.assertEqual((record.verdict, record.complete_pass, record.first_omega_0,
                          record.ruling_sha256), ("PASS", True, 120.0, self.SHA))
        self.assertEqual(record.r_ref_artifact["sha256"], "ab" * 32)

    def test_a_block_record_reads_its_fields(self):
        record = g2.parse_remeasure(remeasure_payload(verdict="BLOCK", ruling_sha256=self.SHA))
        self.assertEqual((record.verdict, record.complete_pass), ("BLOCK", False))
        self.assertIsNone(record.r_ref_artifact)

    def test_a_record_that_is_not_a_clean_pass_or_block_is_refused(self):
        def without(key):
            payload = self.payload()
            del payload[key]
            return payload

        cases = {
            "another schema": self.payload(schema="phase60-gate04-remeasure/v0"),
            "no schema": without("schema"),
            "verdict maybe": self.payload(verdict="MAYBE"),
            "verdict lower case": self.payload(verdict="pass"),
            "verdict maybe with no complete pass": self.payload(verdict="MAYBE", complete_pass=False),
            "no verdict": without("verdict"),
            "complete_pass missing": without("complete_pass"),
            "complete_pass not a bool": self.payload(complete_pass=1),
            "pass without a complete pass": self.payload(complete_pass=False),
            "block with a complete pass": remeasure_payload(
                verdict="BLOCK", ruling_sha256=self.SHA, complete_pass=True),
            "no setting": without("first_omega_0"),
            "zero setting": self.payload(first_omega_0=0.0),
            "negative setting": self.payload(first_omega_0=-60.0),
            "nan setting": self.payload(first_omega_0=float("nan")),
            "bool setting": self.payload(first_omega_0=True),
            "string setting": self.payload(first_omega_0="120"),
            "no ruling hash": without("ruling_sha256"),
            "short ruling hash": self.payload(ruling_sha256="cd" * 31),
            "upper case ruling hash": self.payload(ruling_sha256="CD" * 32),
            "pass without an artifact": without("r_ref_artifact"),
            "artifact is not an object": self.payload(r_ref_artifact="x"),
            "artifact without a path": self.payload(r_ref_artifact={"sha256": "ab" * 32}),
            "artifact with an empty path": self.payload(r_ref_artifact={"path": "", "sha256": "ab" * 32}),
            "artifact without a hash": self.payload(r_ref_artifact={"path": "x"}),
            "artifact with a short hash": self.payload(r_ref_artifact={"path": "x", "sha256": "ab"}),
        }
        for label, payload in cases.items():
            with self.subTest(case=label):
                with self.assertRaises(g2.G2Halt):
                    g2.parse_remeasure(payload)
        with self.assertRaises(g2.G2Halt):
            g2.parse_remeasure(["not", "an", "object"])


class BranchOwnerTests(unittest.TestCase):
    """The full branch table: rulings, the GATE-04 gate and the ladder."""

    NAMES = BranchTracerTests.NAMES

    def statuses(self, tree):
        return {name: tree.state(name).status for name in self.NAMES}

    def rescue_tree(self, pre_answer=None):
        return rescued_tree(self, (0, 0, 1), ONE_AT_120, 1, pre_answer)

    def failed_tree(self, pre_answer=None):
        return rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, pre_answer)

    def test_an_unanswered_checkpoint_holds_the_ladder(self):
        tree = self.rescue_tree()
        statuses = self.statuses(tree)
        self.assertEqual(statuses["owner-decision"], "TAKEN")
        for name in ("stop", "continue-gate", "ladder"):
            self.assertEqual(statuses[name], "PENDING", name)
            self.assertIn("checkpoint 4", tree.state(name).reason)
        code, out = tree.cli("branch", "ladder")
        self.assertEqual(code, 4)
        self.assertTrue(out.startswith("BRANCH-PENDING: ladder"), out)

    def test_go_to_verdict_takes_the_stop(self):
        tree = self.rescue_tree().with_checkpoint4("go-to-verdict")
        self.assertEqual(self.statuses(tree), {
            "sweep": "TAKEN", "confirmation": "TAKEN", "owner-decision": "TAKEN",
            "stop": "TAKEN", "continue-gate": "NOT-TAKEN", "ladder": "NOT-TAKEN",
        })
        self.assertEqual(tree.state("stop").reason, GO_TO_VERDICT)
        code, out = tree.cli("branch", "stop")
        self.assertEqual(code, 0)
        self.assertEqual(out, f"BRANCH-TAKEN: stop ({GO_TO_VERDICT})")

    def test_continue_takes_the_continue_gate_at_the_named_setting(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "120")
        gate = tree.state("continue-gate")
        self.assertEqual((gate.status, gate.first_omega_0, gate.omega_provenance),
                         ("TAKEN", 120.0, "owner_approved"))
        self.assertEqual(gate.reason, "continue at first_omega_0 120.0")
        self.assertEqual(tree.state("stop").status, "NOT-TAKEN")
        self.assertEqual(tree.state("stop").reason, "continue at first_omega_0 120.0")
        ladder = tree.state("ladder")
        self.assertEqual(ladder.status, "PENDING")
        self.assertIn("re-measure", ladder.reason)
        self.assertIsNone(ladder.first_omega_0)

    def test_a_setting_off_the_sweep_grid_is_accepted_and_carried(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "37.5")
        gate = tree.state("continue-gate")
        self.assertEqual((gate.status, gate.first_omega_0), ("TAKEN", 37.5))
        tree.with_remeasure(first_omega_0=37.5)
        ladder = tree.state("ladder")
        self.assertEqual((ladder.status, ladder.first_omega_0), ("TAKEN", 37.5))
        self.assertEqual(ladder.reason, "continue; first_omega_0 37.5; owner_approved")

    def test_the_ladder_waits_for_a_gate_04_pass_at_the_approved_setting(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "120")
        self.assertEqual(tree.state("ladder").status, "PENDING")
        tree.with_remeasure(first_omega_0=120.0)
        ladder = tree.state("ladder")
        self.assertEqual((ladder.status, ladder.first_omega_0, ladder.omega_provenance),
                         ("TAKEN", 120.0, "owner_approved"))
        self.assertEqual(ladder.reason, "continue; first_omega_0 120.0; owner_approved")
        code, out = tree.cli("branch", "ladder")
        self.assertEqual(code, 0)
        self.assertEqual(out, "BRANCH-TAKEN: ladder (continue; first_omega_0 120.0; owner_approved)")
        self.assertEqual(tree.state("stop").status, "NOT-TAKEN")
        self.assertEqual(tree.state("continue-gate").status, "TAKEN")

    def test_a_gate_04_block_keeps_the_ladder_pending_for_the_owner(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "120")
        tree.with_remeasure(verdict="BLOCK", first_omega_0=120.0)
        ladder = tree.state("ladder")
        self.assertEqual(ladder.status, "PENDING")
        self.assertEqual(ladder.reason, "GATE-04 BLOCK at 120.0; owner")
        code, out = tree.cli("branch", "ladder")
        self.assertEqual(code, 4)
        self.assertEqual(out, "BRANCH-PENDING: ladder (GATE-04 BLOCK at 120.0; owner)")
        self.assertEqual(tree.state("continue-gate").status, "TAKEN")

    def test_a_remeasure_at_another_setting_or_under_another_ruling_halts(self):
        for verdict in ("PASS", "BLOCK"):
            for label, overrides in (
                ("another setting", {"first_omega_0": 240.0}),
                ("a slightly different setting", {"first_omega_0": 120.0000001}),
                ("another ruling", {"ruling_sha256": "0" * 64}),
            ):
                with self.subTest(verdict=verdict, case=label):
                    tree = self.rescue_tree().with_checkpoint4("continue", "120")
                    tree.with_remeasure(verdict=verdict, **overrides)
                    with self.assertRaises(g2.G2Halt):
                        tree.state("ladder")
                    code, out = tree.cli("branch", "ladder")
                    self.assertEqual(code, 2)
                    self.assertTrue(out.startswith("G2-HALT:"), out)

    def test_a_changed_ruling_leaves_an_old_remeasure_stale(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "120").with_remeasure()
        self.assertEqual(tree.state("ladder").status, "TAKEN")
        tree.with_checkpoint4("continue", "240")  # the owner re-answers
        with self.assertRaises(g2.G2Halt):
            tree.state("ladder")

    def test_a_malformed_remeasure_record_halts(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "120")
        payload = remeasure_payload(ruling_sha256=tree.ruling_sha())
        payload["verdict"] = "MAYBE"
        tree.write_json(tree.path("continue/gate04-remeasure.json"), payload)
        tree.commit("a malformed re-measure")
        with self.assertRaises(g2.G2Halt):
            tree.state("ladder")

    def test_an_uncommitted_remeasure_makes_the_ladder_pending(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "120")
        tree.with_remeasure(commit=False)
        ladder = tree.state("ladder")
        self.assertEqual(ladder.status, "PENDING")
        self.assertTrue(ladder.reason.startswith("uncommitted "), ladder.reason)
        self.assertTrue(ladder.reason.endswith("gate04-remeasure.json"), ladder.reason)

    def test_a_skip_beside_a_continued_ladder_halts(self):
        tree = self.rescue_tree().with_checkpoint4("continue", "120").with_remeasure()
        tree.write_json(tree.path("g2/skip-records.json"),
                        {"schema": "phase60-skip-records/v1", "reason": NO_RESCUE})
        tree.commit("a skip beside a continue")
        with self.assertRaises(g2.G2Halt):
            tree.state("ladder")

    def test_a_gap_60_09_reading_of_no_rescue_takes_the_stop(self):
        tree = self.failed_tree().with_gap6009("no_rescue")
        self.assertEqual(self.statuses(tree), {
            "sweep": "TAKEN", "confirmation": "TAKEN", "owner-decision": "TAKEN",
            "stop": "TAKEN", "continue-gate": "NOT-TAKEN", "ladder": "NOT-TAKEN",
        })
        self.assertEqual(tree.state("stop").reason, NO_RESCUE)

    def test_a_failed_confirmation_with_no_pre_answer_waits_for_the_owner(self):
        tree = self.failed_tree()
        for name in ("stop", "continue-gate", "ladder"):
            state = tree.state(name)
            self.assertEqual(state.status, "PENDING", name)
            self.assertIn("GAP-60-09", state.reason)

    def test_a_gap_60_09_reading_of_rescue_then_needs_the_checkpoint_4_ruling(self):
        tree = self.failed_tree().with_gap6009("rescue")
        for name in ("stop", "continue-gate", "ladder"):
            state = tree.state(name)
            self.assertEqual(state.status, "PENDING", name)
            self.assertIn("checkpoint 4", state.reason)
        tree.with_checkpoint4("go-to-verdict")
        self.assertEqual(tree.state("stop").reason, GO_TO_VERDICT)
        self.assertEqual(tree.state("stop").status, "TAKEN")

    def test_a_gap_60_09_reading_of_rescue_can_continue(self):
        tree = self.failed_tree().with_gap6009("rescue").with_checkpoint4("continue", "240")
        gate = tree.state("continue-gate")
        self.assertEqual((gate.status, gate.first_omega_0), ("TAKEN", 240.0))
        self.assertEqual(tree.state("stop").status, "NOT-TAKEN")

    def test_a_protocol_pre_answer_decides_before_any_gap_60_09_file(self):
        rescue_pre = self.failed_tree("rescue").with_gap6009("no_rescue")
        self.assertEqual(rescue_pre.state("stop").status, "PENDING")  # still needs checkpoint 4
        self.assertIn("checkpoint 4", rescue_pre.state("stop").reason)
        no_rescue_pre = self.failed_tree("no_rescue").with_gap6009("rescue")
        self.assertEqual(no_rescue_pre.state("stop").status, "TAKEN")
        self.assertEqual(no_rescue_pre.state("stop").reason, NO_RESCUE)

    def test_a_stray_continue_ruling_cannot_open_the_ladder(self):
        cases = {
            "sweep with no rescue": curve_tree(self, (0, 0, 1), ZERO_GRID),
            "failed confirmation pre-answered no rescue": self.failed_tree("no_rescue"),
        }
        for label, tree in cases.items():
            with self.subTest(case=label):
                tree.with_checkpoint4("continue", "120").with_remeasure()
                self.assertEqual(tree.state("stop").status, "TAKEN")
                self.assertEqual(tree.state("continue-gate").status, "NOT-TAKEN")
                self.assertEqual(tree.state("ladder").status, "NOT-TAKEN")

    def test_a_passed_gate_runs_the_ladder_at_the_locked_setting_whatever_the_rulings(self):
        tree = outcome_tree(self, (1, 1, 0)).with_checkpoint4("continue", "120")
        tree.with_gap6009("rescue")
        self.assertEqual(self.statuses(tree), {
            "sweep": "NOT-TAKEN", "confirmation": "NOT-TAKEN", "owner-decision": "NOT-TAKEN",
            "stop": "NOT-TAKEN", "continue-gate": "NOT-TAKEN", "ladder": "TAKEN",
        })
        ladder = tree.state("ladder")
        self.assertEqual((ladder.first_omega_0, ladder.omega_provenance), (30.0, "locked"))

    def test_an_uncommitted_or_edited_ruling_is_pending_not_trusted(self):
        for label, prepare in (
            ("untracked", lambda t: t.with_checkpoint4("continue", "120", commit=False)),
            ("edited", lambda t: (t.with_checkpoint4("go-to-verdict"),
                                  t.with_checkpoint4("continue", "120", commit=False))),
        ):
            with self.subTest(case=label):
                tree = self.rescue_tree()
                prepare(tree)
                for name in ("stop", "continue-gate", "ladder"):
                    state = tree.state(name)
                    self.assertEqual(state.status, "PENDING", name)
                    self.assertTrue(state.reason.startswith("uncommitted "), state.reason)
                    self.assertTrue(state.reason.endswith("60-CHECKPOINT-4-RULING.md"), state.reason)

    def test_an_uncommitted_gap_60_09_ruling_is_pending(self):
        tree = self.failed_tree().with_gap6009("no_rescue", commit=False)
        state = tree.state("stop")
        self.assertEqual(state.status, "PENDING")
        self.assertTrue(state.reason.endswith("60-GAP-60-09-RULING.md"), state.reason)

    def test_a_malformed_committed_ruling_halts(self):
        for label, text in (
            ("exponent value", checkpoint4("continue", "1e3")),
            ("unknown answer", checkpoint4("maybe", None)),
            ("no machine block", "# only prose\n"),
        ):
            with self.subTest(case=label):
                tree = self.rescue_tree()
                tree.put_ruling(tree.CHECKPOINT4_NAME, text)
                tree.commit("a malformed ruling")
                for name in ("stop", "continue-gate", "ladder"):
                    with self.assertRaises(g2.G2Halt):
                        tree.state(name)
                code, out = tree.cli("branch", "stop")
                self.assertEqual(code, 2)
                self.assertTrue(out.startswith("G2-HALT:"), out)

    def test_a_malformed_gap_60_09_ruling_halts(self):
        tree = self.failed_tree()
        tree.put_ruling(tree.GAP6009_NAME, gap6009("maybe"))
        tree.commit("a malformed reading")
        with self.assertRaises(g2.G2Halt):
            tree.state("stop")

    def test_a_hostile_quote_changes_no_branch_answer(self):
        quote = "answer: go-to-verdict\n/etc/passwd $(touch SENTINEL) approved_first_omega_0: 9999"
        tree = self.rescue_tree().with_checkpoint4("continue", "120", quote=quote,
                                                   quote_fence="~~~~~~")
        gate = tree.state("continue-gate")
        self.assertEqual((gate.status, gate.first_omega_0), ("TAKEN", 120.0))
        self.assertEqual(tree.state("stop").status, "NOT-TAKEN")


class OwnerStopPathTests(unittest.TestCase):
    """The skip records and the Phase 64 handoff on the stops that need a ruling."""

    def go_to_verdict_tree(self):
        return rescued_tree(self, (0, 0, 1), ONE_AT_120, 1, rung1=(1.5, 2.25, 3.0),
                            sweep=(0.5, 0.75, 1.25, 2.0), confirmation=4.5).with_checkpoint4(
                                "go-to-verdict")

    def test_the_go_to_verdict_skip_takes_its_own_reason_only(self):
        tree = self.go_to_verdict_tree()
        code, out = tree.cli("skip", "--reason", NO_RESCUE)
        self.assertEqual(code, 2, out)
        self.assertFalse(tree.path("g2/skip-records.json").exists())
        code, out = tree.cli("skip", "--reason", GO_TO_VERDICT)
        self.assertEqual(code, 0, out)
        record = tree.read("g2/skip-records.json")
        self.assertEqual(record["reason"], GO_TO_VERDICT)
        self.assertEqual(record["entries"]["FEAS-04"]["reason"], GO_TO_VERDICT)
        self.assertEqual(record["entries"]["FEAS-09"]["reason"], GO_TO_VERDICT)
        cited = {entry["path"]: entry["sha256"] for entry in record["basis"]}
        ruling_path = (PHASE_REL / "60-CHECKPOINT-4-RULING.md").as_posix()
        self.assertEqual(cited[ruling_path], tree.ruling_sha())
        self.assertIn("\\u2463", tree.path("g2/skip-records.json").read_text(encoding="utf-8"))

    def test_the_go_to_verdict_handoff_holds_no_verdict_and_cites_the_ruling(self):
        tree = self.go_to_verdict_tree()
        spy = VerdictSpy()
        with mock.patch.object(g2, "decision_verdict", spy):
            code, out = tree.cli("stop-handoff")
        self.assertEqual(code, 0, out)
        self.assertEqual(spy.calls, [])  # the verdict rule is not called on this path
        handoff = tree.read("g2/stop-handoff.json")
        self.assertEqual(handoff["stop_reason"], GO_TO_VERDICT)
        self.assertIsNone(handoff["verdict"])
        answer = handoff["owner_answer"]
        self.assertEqual((answer["checkpoint"], answer["answer"]), (4, "go-to-verdict"))
        self.assertEqual(answer["ruling_sha256"], tree.ruling_sha())
        self.assertEqual(answer["ruling_path"], (PHASE_REL / "60-CHECKPOINT-4-RULING.md").as_posix())
        self.assertIn("no decision_verdict call", handoff["verdict_note"])
        self.assertEqual(handoff["level3"], "not tested (skipped at G2)")
        self.assertEqual(handoff["phases_61_63"], "skipped at G2, not failed")
        self.assertEqual(len(handoff["arms"]), 8)
        self.assertAlmostEqual(handoff["total_wall_hours"], 15.75, places=12)

    def test_the_handoff_never_copies_the_owner_quote(self):
        marker = "UNIQUE-QUOTE-MARKER-5512"
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1).with_checkpoint4(
            "go-to-verdict", quote=marker)
        self.assertEqual(tree.cli("stop-handoff")[0], 0)
        self.assertEqual(tree.cli("skip", "--reason", GO_TO_VERDICT)[0], 0)
        for name in ("stop-handoff.json", "skip-records.json"):
            self.assertNotIn(marker, tree.path(f"g2/{name}").read_text(encoding="utf-8"))

    def test_a_gap_60_09_no_rescue_handoff_uses_the_frozen_verdict(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 0, None).with_gap6009("no_rescue")
        spy = VerdictSpy()
        with mock.patch.object(g2, "decision_verdict", spy):
            code, out = tree.cli("stop-handoff")
        self.assertEqual(code, 0, out)
        self.assertEqual(len(spy.calls), 1)
        handoff = tree.read("g2/stop-handoff.json")
        self.assertEqual(handoff["stop_reason"], NO_RESCUE)
        self.assertEqual(handoff["verdict"], StopHandoffTests.expected_verdict())
        cited = {entry["path"]: entry["sha256"] for entry in handoff["basis"]}
        gap_path = (PHASE_REL / "60-GAP-60-09-RULING.md").as_posix()
        self.assertEqual(cited[gap_path], tree.ruling_sha(tree.GAP6009_NAME))
        self.assertEqual(tree.cli("skip", "--reason", NO_RESCUE)[0], 0)

    def test_a_continue_path_has_no_skip_and_no_handoff(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1).with_checkpoint4(
            "continue", "120").with_remeasure()
        for reason in g2.SKIP_REASONS:
            self.assertEqual(tree.cli("skip", "--reason", reason)[0], 2)
        self.assertEqual(tree.cli("stop-handoff")[0], 2)
        for name in ("skip-records.json", "stop-handoff.json"):
            self.assertFalse(tree.path(f"g2/{name}").exists())

    def test_an_unanswered_checkpoint_has_no_skip_and_no_handoff_yet(self):
        tree = rescued_tree(self, (0, 0, 1), ONE_AT_120, 1)
        self.assertEqual(tree.cli("skip", "--reason", GO_TO_VERDICT)[0], 4)
        self.assertEqual(tree.cli("stop-handoff")[0], 4)


if __name__ == "__main__":
    unittest.main()
