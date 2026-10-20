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

import contextlib
import dataclasses
import hashlib
import io
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pinn.verification import learnability_g2 as g2
from pinn.verification.feasibility_scorecard import g2_fires, load_scorecard
from pinn.verification.learnability_arms import EVIDENCE_REL, PANEL_SYSTEMS, RUN_SCHEMA
from tests.phase59.test_evidence_verifier import commit_all, init_repo

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


class Tree:
    """A temporary git repository holding a synthetic Phase 60 evidence tree."""

    def __init__(self, test):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase60-g2-")
        test.addCleanup(self._tmp.cleanup)
        self.test = test
        self.root = Path(self._tmp.name).resolve()
        init_repo(self.root)
        (self.root / "README.md").write_text("synthetic repository for the G2 tests\n")
        commit_all(self.root, "init")
        self.evidence = self.root / EVIDENCE_REL

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

    def write_rung1(self, tiers, **kwargs):
        for system, tier in zip(PANEL_SYSTEMS, tiers):
            self.write_record(f"r1-{system}", tier=tier, **kwargs)

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
                tree = Tree(self).with_outcome(tiers)
                outcome = tree.read("g2/g2-outcome.json")
                self.assertEqual(
                    (outcome["sweep_system"], outcome["confirmation_system"],
                     outcome["uncovered_system"]),
                    expected,
                )

    def test_a_quiet_outcome_has_no_pair(self):
        tree = Tree(self).with_outcome((1, 1, 0))
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
        tree = Tree(self).with_outcome((0, 0, 1))
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
        tree = Tree(self).with_outcome((0, 0, 1))
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
        tree = Tree(self).with_outcome((0, 0, 1))
        state = tree.state("sweep")
        self.assertEqual(state.status, "TAKEN")
        self.assertIsNone(state.first_omega_0)
        code, out = tree.cli("branch", "sweep")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("BRANCH-TAKEN: sweep"), out)
        self.assertEqual(len(out.splitlines()), 1)

    def test_a_quiet_outcome_leaves_the_sweep_branch_not_taken(self):
        tree = Tree(self).with_outcome((1, 1, 0))
        self.assertEqual(tree.state("sweep").status, "NOT-TAKEN")
        code, out = tree.cli("branch", "sweep")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("BRANCH-NOT-TAKEN: sweep"), out)

    def test_a_quiet_outcome_takes_the_ladder_at_the_locked_setting(self):
        tree = Tree(self).with_outcome((1, 1, 0))
        state = tree.state("ladder")
        self.assertEqual(state.status, "TAKEN")
        self.assertEqual(state.first_omega_0, 30.0)
        self.assertEqual(state.omega_provenance, "locked")
        self.assertEqual(state.reason, "g2 passed; first_omega_0 30.0")

    def test_the_command_line_prints_the_ladder_token_in_a_subprocess(self):
        tree = Tree(self).with_outcome((1, 1, 1))
        code, out, err = tree.cli_subprocess("branch", "ladder")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(out, "BRANCH-TAKEN: ladder (g2 passed; first_omega_0 30.0)")
        code, out, err = tree.cli_subprocess("branch", "sweep")
        self.assertEqual(code, 0, out + err)
        self.assertTrue(out.startswith("BRANCH-NOT-TAKEN: sweep"), out)

    def test_a_fired_outcome_leaves_the_ladder_pending(self):
        tree = Tree(self).with_outcome((0, 0, 1))
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
        tree = Tree(self).with_outcome((1, 1, 0))
        target = tree.path("g2/g2-outcome.json")
        payload = json.loads(target.read_text())
        payload["g2_fired"] = True
        tree.write_json(target, payload)
        state = tree.state("ladder")
        self.assertEqual(state.status, "PENDING")
        self.assertTrue(state.reason.startswith("uncommitted "))

    def test_a_committed_outcome_that_disagrees_with_the_records_halts(self):
        tree = Tree(self).with_outcome((1, 1, 0))
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
        tree = Tree(self).with_outcome((1, 1, 0))
        tree.write_record("r1-4658", tier=3)  # tier changes after the outcome
        tree.commit("rewrite a record")
        with self.assertRaises(g2.G2Halt):
            tree.state("ladder")

    def test_a_committed_outcome_whose_record_is_gone_halts(self):
        tree = Tree(self).with_outcome((1, 1, 0))
        tree.record_path("r1-851").unlink()
        tree.commit("remove a record")
        with self.assertRaises(g2.G2Halt):
            tree.state("sweep")

    def test_the_state_is_a_frozen_value_with_a_closed_vocabulary(self):
        tree = Tree(self).with_outcome((1, 1, 0))
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


if __name__ == "__main__":
    unittest.main()
