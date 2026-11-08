"""Plan 67-06 task 67-06-01: the complete synthetic workflow and CLI contract.

The thirteen Phase 67 commands run end to end on one temporary fixture
repository: the frozen design and metadata registration, the gated
metadata-only capture (through the injected data and power seams), the exact
timing matrix and its committed registrations, single-row launches through
the real AC/weekend launch gate (the fit CLI inline over the synthetic gold
corpus seam), the cost-only budget with its immutable prediction page, the
science matrix and rows, the review with its result page, the conditional
scope authority, and the read-only phase audit. Before a prerequisite
commit, its dependent command refuses with no downstream file; unknown
options, experiments, kinds, cases and arms refuse; no real corpus, MPS
device or weekend launch is ever reached.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import math
import re
import subprocess
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pinn.verification.diagnostic_fit as fit_module
import pinn.verification.diagnostic_phase67 as phase67_cli
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import _fit_registration_fixture, _loaded
from tests.phase67._fixtures import (
    fake_clock,
    fake_pmset,
    inline_supervisor,
    patch_data_seam,
)

AC_LINE = "Now drawing from 'AC Power'"
SATURDAY = "2026-10-31T12:00:00-05:00"
#: The owner's weekday amendment: a pre-deadline Tuesday instant (before
#: the 2026-11-07 07:30 deadline, as under its expired predecessors).
TUESDAY_AMENDED = "2026-11-03T11:57:47-06:00"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

#: The workflow's patched arm table: one contrasted pair on the real registry.
WORKFLOW_ARMS = {"exp02": ("d2", "d12")}
_RULE_MODULE = phase67_cli

#: The workflow rule at the fixture scale: the registered timing run is
#: 100 steps (20 warmup, 80 measured) and the budget's floor is the same
#: 100-step quantum, so every synthetic fit stays seconds long.
WORKFLOW_RULE = {
    "cap_seconds": 3540.0, "time_fraction": 0.75, "rate_margin": 0.25,
    "warmup_steps": 20, "step_quantum": 100, "min_steps": 100,
    "similarity_events": 5, "score_events": 3,
    "loss_trace_entries_max": 1000, "loss_entry_bytes": 32,
    "residual_tolerance": 1e-9, "size_limit_bytes": 10485760,
    "size_fraction": 0.9, "timing_steps": 100, "timing_warmup": 20,
    "timing_measured": 80, "timing_cap_seconds": 900.0,
}

_CHAIN: dict = {}
_STACK_HOLDER: list = []  # keeps the chain's contexts open for the process


def _execution(case):
    try:
        import pinn.verification.diagnostic_phase67_execution as execution

        return execution
    except ImportError as exc:
        case.fail(f"pinn.verification.diagnostic_phase67_execution is missing: {exc}")


def _git(root, *args, check=True):
    return subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True, check=check
    )


def _commit(root, message):
    _git(root, "add", ".planning")
    _git(root, "commit", "-q", "-m", message)


def _relabel(data, orbit_key):
    """The fixture data carrying one case's registered orbit identity.

    The data seam is fully injected, so the records block is the fixture's own
    evidence surface: relabelling it to the registered orbit key is exactly
    what the real loader would record for that orbit.
    """
    records = {
        role: {**block, "record_key": orbit_key}
        for role, block in data.records.items()
    }
    return SimpleNamespace(**{**vars(data), "records": records})


def _build_chain(clock_iso=SATURDAY, cache=None):
    """Run the complete synthetic chain once; the holder keeps every path.

    ``clock_iso`` is the aware instant every gated command sees; the default
    Saturday predates the owner's weekday amendment, and the
    weekday-amendment chain builds with a pre-deadline Tuesday instead.
    """
    stack = ExitStack()  # stays open for the process lifetime
    _STACK_HOLDER.append(stack)
    fixture = stack.enter_context(gold_corpus_fixture())
    tmp = Path(stack.enter_context(
        tempfile.TemporaryDirectory(prefix="phase67-workflow-")
    ))
    spec, context, scorecard, data = _loaded(fixture)
    if context.attestation is None:
        context = SimpleNamespace(
            **{**vars(context), "attestation": SimpleNamespace(
                summary=lambda: {"test_split_opens": 0, "withheld_refusals": 0}
            )}
        )
    if not hasattr(context.reader, "access_summary"):
        context.reader.access_summary = lambda: {
            "requested": [], "opened": [], "refused_before_open": 0,
            "actual_opens": 1,
        }
    root, _commit_sha = _fit_registration_fixture(tmp / "repo")
    phase = root / ".planning/phases/67-design-settings-ladders"
    evidence = phase / "evidence"
    evidence.mkdir(parents=True)

    def sha256(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    freeze = {
        "schema": "phase67-harness-freeze/v1",
        "files": [
            {"path": "fit_dep.py", "sha256": sha256(root / "fit_dep.py")},
            {"path": "frozen/scorer.py", "sha256": sha256(root / "frozen/scorer.py")},
        ],
    }
    (evidence / "harness-freeze.json").write_text(json.dumps(freeze, indent=2))
    freeze_rel = ".planning/phases/67-design-settings-ladders/evidence/" \
        "harness-freeze.json"
    _git(root, "add", freeze_rel)
    _git(root, "commit", "-q", "-m", "fixture harness freeze")

    execution = _execution(_ChainTestCase)
    rule_patch = mock.patch.object(_RULE_MODULE, "PHASE67_BUDGET_RULE", WORKFLOW_RULE)
    rule_patch.start()
    arm_patch = mock.patch.object(execution, "ARM_ORDER", WORKFLOW_ARMS)
    arm_patch.start()
    # The fixture repository supplies its own provenance registration and
    # pinned harness files (the production paths live in the real repo).
    provenance_patch = mock.patch.object(
        execution, "PROVENANCE_REGISTRATION_REL", "reg/smoke-registration.json"
    )
    provenance_patch.start()
    dependencies_patch = mock.patch.object(
        execution, "PHASE67_DEPENDENCIES", ("fit_dep.py", "frozen/scorer.py")
    )
    dependencies_patch.start()
    runtime_patch = mock.patch.object(
        execution, "DEFAULT_RUNTIME", {"dtype": "float64", "device": "cpu"}
    )
    runtime_patch.start()
    orbit_data = {
        "hierarchical/gold/1632": _relabel(data, "hierarchical/gold/1632"),
        "hierarchical/gold/851": _relabel(data, "hierarchical/gold/851"),
    }

    def run_cli(argv, **kwargs):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(argv, repo_root=root, **kwargs)
        return code, stdout.getvalue(), stderr.getvalue()

    def launch(kind, case, arm):
        def runner(argv, *, cwd):
            with ExitStack() as inner:
                patch_data_seam(
                    inner, context, orbit_data[
                        json.loads(
                            (phase / f"evidence/exp02/{kind}/{case}/{arm}/"
                             "registration.json").read_bytes()
                        )["settings"]["orbit_key"]
                    ], spec,
                )
                return fit_module.main(
                    argv[6:], repo_root=root, supervisor=inline_supervisor
                )

        from tests.phase67._fixtures import inline_supervisor

        code, _stdout, stderr = run_cli(
            ["launch-row", "--experiment", "exp02", "--kind", kind,
             "--case", case, "--arm", arm],
            read_power=fake_pmset(AC_LINE), run=runner, now=fake_clock(clock_iso),
            supervisor=inline_supervisor,
        )
        assert code == 0, f"launch-row {kind}/{case}/{arm} refused: {stderr}"

    state = {
        "root": root, "phase": phase, "spec": spec, "context": context,
        "scorecard": scorecard, "data": data, "execution": execution,
        "run_cli": run_cli, "launch": launch, "orbit_data": orbit_data,
    }
    _stages(state, clock_iso)
    (cache if cache is not None else _CHAIN).update(state)
    return state


def _stages(state, clock_iso=SATURDAY):
    root, phase, run_cli = state["root"], state["phase"], state["run_cli"]

    # 1-2) The frozen design, its page and the metadata registration.
    code, _out, err = run_cli(["prepare-design", "--experiment", "exp02"])
    assert code == 0, f"prepare-design refused: {err}"
    _commit(root, "frozen design")
    code, out, _err = run_cli(["check-design", "--experiment", "exp02"])
    assert "PHASE67-DESIGN-OK" in out, out

    # 3-4) The gated metadata-only capture for both registered orbits.
    def load_orbit(orbit_key, window_length):
        return state["orbit_data"][orbit_key]

    from tests.phase67._fixtures import inline_supervisor

    code, _out, err = run_cli(
        ["capture-metadata", "--experiment", "exp02"],
        read_power=fake_pmset(AC_LINE), now=fake_clock(clock_iso),
        load_orbit=load_orbit, supervisor=inline_supervisor,
    )
    assert code == 0, f"capture-metadata refused: {err}"
    _commit(root, "metadata capture")
    code, out, _err = run_cli(["check-metadata", "--experiment", "exp02"])
    assert "PHASE67-METADATA-OK" in out, out

    # 5-6) The exact timing matrix, its committed registrations and rows.
    code, _out, err = run_cli(["register-timing", "--experiment", "exp02"])
    assert code == 0, f"register-timing refused: {err}"
    _commit(root, "timing matrix")
    code, out, _err = run_cli(
        ["check-matrix", "--experiment", "exp02", "--kind", "timing"]
    )
    assert "PHASE67-MATRIX-OK" in out, out
    timing_matrix = json.loads(
        (phase / "evidence/exp02/timing-matrix.json").read_bytes()
    )
    state["timing_matrix"] = timing_matrix
    for row in timing_matrix["rows"]:
        state["launch"]("timing", row["case"], row["arm"])
        _commit(root, f"timing row {row['case']}/{row['arm']}")
    code, out, _err = run_cli(
        ["check-row", "--experiment", "exp02", "--kind", "timing",
         "--case", "main-1632-s42", "--arm", "d2"]
    )
    assert "PHASE67-ROW-OK" in out, f"check-row timing: {out}{_err}"

    # 7-8) The cost-only budget, its immutable pages and the science matrix.
    _patch_science_cap(state)
    code, _out, err = run_cli(["budget", "--experiment", "exp02"])
    assert code == 0, f"budget refused: {err}"
    _commit(root, "budget and science registrations")
    code, out, err = run_cli(["check-budget", "--experiment", "exp02"])
    assert "PHASE67-BUDGET-OK" in out, f"{out}{err}"

    # 9-11) The science rows, the review and its conditional scope authority.
    science_matrix = json.loads(
        (phase / "evidence/exp02/science-matrix.json").read_bytes()
    )
    state["science_matrix"] = science_matrix
    for row in science_matrix["rows"]:
        state["launch"]("science", row["case"], row["arm"])
        _commit(root, f"science row {row['case']}/{row['arm']}")
    code, out, _err = run_cli(
        ["check-row", "--experiment", "exp02", "--kind", "science",
         "--case", "main-1632-s42", "--arm", "d2"]
    )
    assert "PHASE67-ROW-OK" in out, out
    code, _out, err = run_cli(["review", "--experiment", "exp02"])
    assert code == 0, f"review refused: {err}"
    _commit(root, "review")
    code, out, _err = run_cli(["check-review", "--experiment", "exp02"])
    assert "PHASE67-REVIEW-OK" in out, out


def _patch_science_cap(state):
    """A rule cap that pins the budget's common N at the fixture scale.

    The cap is probed through the real ``phase67_budget`` on the committed
    timing rows' own cost fields: the smallest cap that admits any N gives
    N at the 100-step floor, and the cap is set inside that N region so the
    derived common N is deterministically 100.
    """
    from pinn.verification.diagnostic_phase67 import phase67_budget

    execution = state["execution"]
    entries = []
    identities = []
    for row in state["timing_matrix"]["rows"]:
        directory = state["phase"] / row["registration_path"]
        directory = directory.parent
        record = json.loads((directory / "record.json").read_bytes())
        receipt = json.loads(
            (directory / "power-gate.json").read_bytes()
        )
        attempt = json.loads((directory / "attempt.json").read_bytes())
        identity = {
            "experiment": row["experiment"], "arm": row["arm"],
            "orbit_key": row["orbit_key"], "seed": row["seed"],
            "window": row["t_end"],
        }
        entries.append((
            identity, record, receipt, attempt,
            len((directory / "record.json").read_bytes()),
            len((directory / "diagnostic.weights").read_bytes()),
        ))
        identities.append(identity)
    rows = execution.phase67_cost_rows(entries)

    def steps_at(cap):
        rule = dict(WORKFLOW_RULE)
        rule["cap_seconds"] = cap
        with mock.patch.object(_RULE_MODULE, "PHASE67_BUDGET_RULE", rule):
            try:
                return phase67_budget(
                    rows, expected_identities=identities
                )["common_optimizer_steps"]
            except ValueError:
                return None

    def boundary(refuse_low, admit_high, admitted):
        """Bisect the cap boundary between two known outcomes."""
        for _ in range(60):
            middle = 0.5 * (refuse_low + admit_high)
            if admitted(middle):
                admit_high = middle
            else:
                refuse_low = middle
            if admit_high - refuse_low < 1e-4:
                break
        return admit_high

    def any_steps(cap):
        return steps_at(cap) is not None

    def above_floor(cap):
        return steps_at(cap) is not None and steps_at(cap) > 100

    high = 8.0
    while steps_at(high) is None:
        high *= 2.0
        assert high <= 512.0, "no admissible cap at the fixture scale"
    first_admissible = boundary(0.5, high, any_steps)
    upper = high
    while not above_floor(upper):
        upper *= 2.0
        assert upper <= 512.0, "the floor region never ends"
    floor_end = boundary(first_admissible, upper, above_floor)
    best = math.sqrt(first_admissible * floor_end)
    rule = dict(WORKFLOW_RULE)
    rule["cap_seconds"] = best
    patch = mock.patch.object(_RULE_MODULE, "PHASE67_BUDGET_RULE", rule)
    patch.start()
    state.setdefault("patches", []).append(patch)
    return rule


class _ChainTestCase(unittest.TestCase):
    """Base: the built chain's state, constructed once per process."""

    @classmethod
    def setUpClass(cls):
        if not _CHAIN:
            _build_chain()
        for name, value in _CHAIN.items():
            if name not in ("patches", "run_cli", "launch"):
                setattr(cls, name, value)

    def run_cli(self, argv, **kwargs):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(argv, repo_root=self.root, **kwargs)
        return code, stdout.getvalue(), stderr.getvalue()


_WEEKDAY_CHAIN: dict = {}


class WeekdayAmendmentChainTests(unittest.TestCase):
    """The complete chain also runs on a pre-deadline weekday.

    The owner's 2026-11-06 amendment admits weekday operations before
    2026-11-07 07:30 America/Chicago; the whole synthetic chain built on a
    pre-deadline Tuesday proves every gated command (capture, matrix,
    launches, budget) admits and audits the amended weekday receipts.
    """

    @classmethod
    def setUpClass(cls):
        if not _WEEKDAY_CHAIN:
            _build_chain(clock_iso=TUESDAY_AMENDED, cache=_WEEKDAY_CHAIN)
        for name, value in _WEEKDAY_CHAIN.items():
            if name not in ("patches", "run_cli", "launch"):
                setattr(cls, name, value)

    def run_cli(self, argv, **kwargs):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(argv, repo_root=self.root, **kwargs)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_the_weekday_capture_admits_and_records_the_amendment_window(self):
        receipt = json.loads(
            (self.phase / "evidence/exp02/metadata/power-gate.json").read_bytes()
        )
        self.assertEqual(receipt["window"]["isoweekday"], 2)
        self.assertEqual(receipt["window"]["local_time"], TUESDAY_AMENDED)
        self.assertEqual(
            receipt["remaining_window"]["closing_utc"],
            "2026-11-07T13:30:00+00:00",
        )
        code, out, _err = self.run_cli(["check-metadata", "--experiment", "exp02"])
        self.assertEqual(code, 0)
        self.assertIn("PHASE67-METADATA-OK", out)

    def test_the_weekday_row_receipts_admit_through_the_reader(self):
        record_path = (
            self.phase / "evidence/exp02/timing/main-1632-s42/d2/record.json"
        )
        self.assertTrue(record_path.is_file())
        code, out, _err = self.run_cli(
            ["check-row", "--experiment", "exp02", "--kind", "timing",
             "--case", "main-1632-s42", "--arm", "d2"]
        )
        self.assertEqual(code, 0)
        self.assertIn("PHASE67-ROW-OK", out)


class WorkflowChainTests(_ChainTestCase):
    """Every command ran, produced its exact files, and verified clean."""

    def test_the_design_and_metadata_registration_were_created_and_verified(self):
        design_json = self.phase / "evidence/exp02/design.json"
        meta_registration = self.phase / "evidence/exp02/metadata-registration.json"
        timing_page = self.phase / "67-EXP02-TIMING-PREDICTION.md"
        for path in (design_json, meta_registration, timing_page):
            self.assertTrue(path.is_file(), path)
        design = json.loads(design_json.read_bytes())
        self.assertEqual(design["schema"], "phase67-design/v1")
        self.assertEqual(
            [entry["arm"] for entry in design["variants"]], ["d2", "d12"]
        )
        registration = json.loads(meta_registration.read_bytes())
        self.assertEqual(registration["schema"],
                         "phase67-metadata-registration/v1")
        self.assertEqual(
            registration["orbits"],
            ["hierarchical/gold/1632", "hierarchical/gold/851"],
        )

    def test_the_metadata_capture_recorded_both_orbits_without_a_model(self):
        record = json.loads(
            (self.phase / "evidence/exp02/metadata/record.json").read_bytes()
        )
        self.assertEqual(record["schema"], "phase67-metadata/v1")
        self.assertEqual(record["status"], "complete")
        self.assertEqual(
            sorted(record["orbits"]),
            ["hierarchical/gold/1632", "hierarchical/gold/851"],
        )
        for orbit, block in record["orbits"].items():
            window = block["windows"]["full"]
            self.assertGreater(window["sample_count"], 1)
            self.assertRegex(window["physical_times_sha256"], HEX64)
            baselines = window["baselines"]
            self.assertIsInstance(baselines["window_mean_constant"]["E"], float)
            self.assertIn("applicable", baselines["two_kepler"])
        self.assertNotIn("optimizer", json.dumps(record))
        attempt = json.loads(
            (self.phase / "evidence/exp02/metadata/attempt.json").read_bytes()
        )
        self.assertEqual(attempt["status"], "published")
        receipt = json.loads(
            (self.phase / "evidence/exp02/metadata/power-gate.json").read_bytes()
        )
        self.assertEqual(receipt["power_source"], "AC Power")

    def test_the_timing_matrix_and_registrations_are_exact_and_committed(self):
        matrix = json.loads(
            (self.phase / "evidence/exp02/timing-matrix.json").read_bytes()
        )
        self.assertEqual(matrix["schema"], "phase67-run-matrix/v1")
        self.assertEqual(len(matrix["rows"]), 6)
        expected = [
            (case, arm)
            for case in ("main-1632-s42", "repeat-851-s42", "repeat-1632-s41")
            for arm in ("d2", "d12")
        ]
        self.assertEqual(
            [(row["case"], row["arm"]) for row in matrix["rows"]], expected
        )
        for row in matrix["rows"]:
            registration = self.phase / row["registration_path"]
            self.assertTrue(registration.is_file(), registration)
            doc = json.loads(registration.read_bytes())
            self.assertEqual(doc["schema"], "phase65-fit-registration/v1")
            self.assertEqual(doc["settings"]["variant"]["name"],
                             row["variant_name"])
            self.assertEqual(doc["settings"]["orbit_key"], row["orbit_key"])
            self.assertEqual(doc["settings"]["seed"], row["seed"])
            self.assertEqual(doc["settings"]["physical_window"],
                             {"t_start": 0.0, "t_end": 10.0})
            self.assertIn("window_metadata", doc)
            self.assertIn("window_baselines", doc)
            self.assertIn("harness_freeze", doc)

    def test_each_timing_row_published_its_four_evidence_files(self):
        for row in self.timing_matrix["rows"]:
            directory = (self.phase / row["registration_path"]).parent
            for name in ("record.json", "attempt.json", "power-gate.json",
                         "diagnostic.weights"):
                self.assertTrue((directory / name).is_file(),
                                f"{directory}/{name}")

    def test_the_budget_is_cost_only_and_the_pages_are_separate(self):
        budget = json.loads(
            (self.phase / "evidence/exp02/budget.json").read_bytes()
        )
        self.assertEqual(budget["schema"], "phase67-budget/v1")
        self.assertEqual(budget["common_optimizer_steps"], 100)
        self.assertNotIn("scores", json.dumps(budget))
        self.assertTrue((self.phase / "67-EXP02-BUDGET.md").is_file())
        self.assertTrue((self.phase / "67-EXP02-PREDICTION.md").is_file())
        science = json.loads(
            (self.phase / "evidence/exp02/science-matrix.json").read_bytes()
        )
        self.assertEqual(science["kind"], "science")
        self.assertEqual(len(science["rows"]), 6)
        for row in science["rows"]:
            doc = json.loads((self.phase / row["registration_path"]).read_bytes())
            self.assertEqual(doc["settings"]["optimizer_steps"], 100)
            self.assertEqual(doc["settings"]["whole_run_cap_seconds"],
                             budget["whole_run_cap_seconds"])

    def test_the_review_exposes_contrasts_and_allows_the_dependent_launch(self):
        review = json.loads(
            (self.phase / "evidence/exp02/review.json").read_bytes()
        )
        self.assertEqual(review["schema"], "phase67-review/v1")
        for field in ("contrasts", "predictions_comparison", "roadmap_comparison",
                      "scope49_disposition", "dependent_launch_allowed",
                      "proposed_change"):
            self.assertIn(field, review)
        self.assertEqual(review["contrasts"]["d2"]["control"], "d12")
        self.assertIn("EXP-02", (self.phase / "67-EXP02-RESULT.md").read_text())

    def test_audit_phase_reports_every_experiment_read_only(self):
        code, out, _err = self.run_cli(["audit-phase"])
        self.assertEqual(code, 0)
        self.assertIn("PHASE67-AUDIT-OK", out)
        code, out, _err = self.run_cli(["audit-phase", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["status"], "PHASE67-AUDIT-OK")
        self.assertEqual(sorted(payload["experiments"]),
                         ["exp02", "exp03", "exp04", "exp05"])


class CommandContractTests(_ChainTestCase):
    """Malformed input and broken prerequisites refuse with exit 2."""

    def test_unknown_commands_experiments_kinds_cases_arms_and_flags_refuse(self):
        cases = [
            ["bogus"],
            ["prepare-design", "--experiment", "exp99"],
            ["check-design", "--experiment", "nope"],
            ["capture-metadata"],
            ["register-timing", "--experiment", "exp02", "--bogus"],
            ["check-matrix", "--experiment", "exp02", "--kind", "other"],
            ["check-matrix", "--kind", "timing"],
            ["launch-row", "--experiment", "exp02", "--kind", "timing",
             "--case", "no-such-case", "--arm", "d2"],
            ["launch-row", "--experiment", "exp02", "--kind", "timing",
             "--case", "main-1632-s42", "--arm", "no-such-arm"],
            ["launch-row", "--experiment", "exp02", "--kind", "timing"],
            ["check-row", "--experiment", "exp02"],
            ["audit-phase", "--experiment", "exp02"],
        ]
        for argv in cases:
            with self.subTest(argv=argv):
                code, _out, err = self.run_cli(argv)
                self.assertEqual(code, 2, argv)
                self.assertIn("PHASE67-REFUSED", err, argv)

    def test_a_dependent_command_before_its_prerequisite_refuses_clean(self):
        with tempfile.TemporaryDirectory(prefix="phase67-order-") as raw:
            root = Path(raw)
            evidence = root / (
                ".planning/phases/67-design-settings-ladders/evidence"
            )
            evidence.mkdir(parents=True)
            execution = _execution(self)
            with mock.patch.object(execution, "ARM_ORDER", WORKFLOW_ARMS):
                code, _out, err = self.run_cli_local(
                    root, ["register-timing", "--experiment", "exp02"]
                )
                self.assertEqual(code, 2)
                self.assertIn("PHASE67-REFUSED", err)
            self.assertEqual(list(evidence.rglob("*")), [])

    def run_cli_local(self, root, argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(argv, repo_root=root)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_check_design_refuses_a_dirty_freeze(self):
        freeze = self.phase / "evidence/harness-freeze.json"
        original = freeze.read_bytes()
        freeze.write_bytes(original + b"# drifted\n")
        try:
            code, _out, err = self.run_cli(
                ["check-design", "--experiment", "exp02"]
            )
            self.assertEqual(code, 2)
            self.assertIn("PHASE67-REFUSED", err)
        finally:
            freeze.write_bytes(original)

    def test_a_second_launch_of_one_row_refuses_at_the_exclusive_claim(self):
        def runner(argv, *, cwd):
            raise AssertionError("a second launch started a fit")

        code, _out, err = self.run_cli(
            ["launch-row", "--experiment", "exp02", "--kind", "timing",
             "--case", "main-1632-s42", "--arm", "d2"],
            read_power=fake_pmset(AC_LINE), run=runner, now=fake_clock(SATURDAY),
        )
        self.assertEqual(code, 2)
        self.assertIn("PHASE67-REFUSED", err)

    def _with_pending_proposal(self, callback):
        review_path = self.phase / "evidence/exp02/review.json"
        original = review_path.read_bytes()
        review = json.loads(original)
        review["scope49_disposition"] = "proposal-pending"
        review["dependent_launch_allowed"] = False
        review["proposed_change"] = "a fixture proposal"
        review_path.write_text(json.dumps(review, indent=2, sort_keys=True))
        _git(self.root, "add", ".planning")
        _git(self.root, "commit", "-q", "-m", "pending fixture proposal")
        try:
            callback()
        finally:
            _git(self.root, "revert", "--no-edit", "HEAD")

    def _with_ruled_pending_proposal(self, disposition, callback, *,
                                     stale_review_digest=False):
        """A pending exp02 proposal plus a committed owner ruling over it.

        The ruling carries the exact digests ``_verify_ruling`` demands
        (review, result page, proposal), is committed after both reviewed
        artifacts, and names allowed dependent work covering the prior
        experiment the way the production exp03 ruling does.
        """
        review_path = self.phase / "evidence/exp02/review.json"
        result_path = self.phase / "67-EXP02-RESULT.md"
        review = json.loads(review_path.read_bytes())
        review["scope49_disposition"] = "proposal-pending"
        review["dependent_launch_allowed"] = False
        review["proposed_change"] = "a fixture proposal"
        review_path.write_text(json.dumps(review, indent=2, sort_keys=True))
        _commit(self.root, "pending fixture proposal")
        pending_sha = _git(
            self.root, "rev-parse", "HEAD"
        ).stdout.strip()
        review_digest = hashlib.sha256(
            review_path.read_bytes()
        ).hexdigest()
        if stale_review_digest:
            review_digest = "0" * 64
        ruling = {
            "schema": "phase67-ruling/v1",
            "experiment": "exp02",
            "disposition": disposition,
            "allowed_dependent_work": [
                "exp03 proceeds as the dependent launch of this exp02 ruling",
            ],
            "owner_words_verbatim": "proceed with option 1",
            "review_sha256": review_digest,
            "result_page_sha256": hashlib.sha256(
                result_path.read_bytes()
            ).hexdigest(),
            "proposal_sha256": hashlib.sha256(
                json.dumps(
                    json.loads(review_path.read_bytes())["proposed_change"],
                    sort_keys=True,
                ).encode("utf-8")
            ).hexdigest(),
        }
        ruling_path = self.phase / "67-EXP02-RULING.md"
        ruling_path.write_text(json.dumps(ruling, indent=2, sort_keys=True))
        _commit(self.root, "fixture owner ruling")
        try:
            callback()
        finally:
            ruling_sha = _git(
                self.root, "rev-parse", "HEAD"
            ).stdout.strip()
            _git(self.root, "revert", "--no-edit", ruling_sha)
            _git(self.root, "revert", "--no-edit", pending_sha)

    def test_a_pending_proposal_blocks_only_the_dependent_experiment(self):
        execution = self.execution

        def check():
            self.assertFalse(execution.phase67_prior_experiment_allowed(
                "exp03", phase_dir=self.phase, repo_root=self.root
            ))
            self.assertTrue(execution.phase67_prior_experiment_allowed(
                "exp02", phase_dir=self.phase, repo_root=self.root
            ))

        self._with_pending_proposal(check)

    def test_a_committed_owner_ruling_admits_the_dependent_launch(self):
        execution = self.execution

        def check():
            self.assertTrue(execution.phase67_prior_experiment_allowed(
                "exp03", phase_dir=self.phase, repo_root=self.root
            ))
            self.assertTrue(execution.phase67_prior_experiment_allowed(
                "exp04", phase_dir=self.phase, repo_root=self.root
            ))

        self._with_ruled_pending_proposal("authorized", check)

    def test_a_hold_ruling_keeps_the_dependent_launch_blocked(self):
        execution = self.execution

        def check():
            self.assertFalse(execution.phase67_prior_experiment_allowed(
                "exp03", phase_dir=self.phase, repo_root=self.root
            ))

        self._with_ruled_pending_proposal("hold", check)

    def test_a_stale_digest_ruling_keeps_the_dependent_launch_blocked(self):
        execution = self.execution

        def check():
            self.assertFalse(execution.phase67_prior_experiment_allowed(
                "exp03", phase_dir=self.phase, repo_root=self.root
            ))

        self._with_ruled_pending_proposal(
            "authorized", check, stale_review_digest=True
        )

    def test_check_review_refuses_when_a_proposal_is_pending(self):
        def check():
            code, out, _err = self.run_cli(["check-review", "--experiment", "exp02"])
            self.assertEqual(code, 2)
            self.assertNotIn("PHASE67-REVIEW-OK", out)

        self._with_pending_proposal(check)


class Exp05TimingRegistrationTests(unittest.TestCase):
    """The exp05 lap variants exist before any row registration is written.

    A fresh register-timing process resolves each row's declaration through
    the phase67 registry while the registration is written
    (``_row_settings``), so the materialization from the committed metadata
    record must happen when that record is admitted — materializing only
    after the registrations (the pre-fix order) refuses every exp05
    registration write, because nothing before it ever populated the
    registry in that process.
    """

    #: The fixture window endpoints per declared arm (exact first-crossing
    #: stand-ins; only their finiteness and internal consistency matter).
    T_ENDS = {"lap1": 0.9, "lap2": 1.8, "lap5": 4.5, "lap10": 9.0}
    CASES = ("main-1632-s42", "repeat-851-s42", "repeat-1632-s41")
    ORBIT_ID = {
        "main-1632-s42": "1632",
        "repeat-851-s42": "851",
        "repeat-1632-s41": "1632",
    }

    def test_register_timing_writes_all_rows_from_a_fresh_registry(self):
        from pinn.verification import diagnostic_phase67_execution as execution
        from pinn.verification.diagnostic_phase67_catalog import (
            _EXP05_WINDOW_VARIANTS,
        )

        saved = dict(_EXP05_WINDOW_VARIANTS)
        _EXP05_WINDOW_VARIANTS.clear()
        self.addCleanup(_EXP05_WINDOW_VARIANTS.clear)
        self.addCleanup(_EXP05_WINDOW_VARIANTS.update, saved)

        with ExitStack() as stack:
            tmp = Path(stack.enter_context(tempfile.TemporaryDirectory(
                prefix="phase67-exp05-registration-")))
            root, _commit = _fit_registration_fixture(tmp / "repo")
            for target, value in (
                # The exp05 arm table at production width: the workflow
                # chain classes patch ARM_ORDER down to their exp02 pair
                # and that patch outlives them in the discovery process.
                ("ARM_ORDER", {"exp05": ("lap1", "lap2", "lap5", "lap10")}),
                ("DEFAULT_RUNTIME", {"dtype": "float64", "device": "cpu"}),
                ("PHASE67_DEPENDENCIES", ("fit_dep.py", "frozen/scorer.py")),
                ("PROVENANCE_REGISTRATION_REL", "reg/smoke-registration.json"),
            ):
                patch = mock.patch.object(execution, target, value)
                patch.start()
                self.addCleanup(patch.stop)

            phase = root / ".planning/phases/67-design-settings-ladders"
            evidence = phase / "evidence"
            evidence.mkdir(parents=True)
            (evidence / "harness-freeze.json").write_text(json.dumps(
                {"schema": "phase67-harness-freeze/v1", "files": []}))
            (phase / "67-EXP05-TIMING-PREDICTION.md").write_text(
                "# fixture exp05 timing page\n")

            def window_block(t_end):
                return {
                    "first_time": 0.0,
                    "last_time": t_end,
                    "t_end": t_end,
                    "sample_count": 95,
                    "physical_times_sha256": "a" * 64,
                    "normalized_tau_sha256": "b" * 64,
                    "baselines": {
                        "window_mean_constant": {"E": 1.15},
                        "two_kepler": {"applicable": True, "E": 0.2},
                    },
                }

            windows = {
                arm: window_block(t_end)
                for arm, t_end in self.T_ENDS.items()
            }
            record = {
                "schema": "phase67-metadata/v1",
                "experiment": "exp05",
                "status": "complete",
                "orbits": {
                    "hierarchical/gold/1632": {"windows": dict(windows)},
                    "hierarchical/gold/851": {"windows": dict(windows)},
                },
            }
            record_path = evidence / "exp05" / "metadata" / "record.json"
            record_path.parent.mkdir(parents=True)
            record_path.write_text(json.dumps(record, indent=2) + "\n")
            _git(root, "add",
                 ".planning/phases/67-design-settings-ladders"
                 "/evidence/exp05/metadata/record.json",
                 ".planning/phases/67-design-settings-ladders"
                 "/evidence/harness-freeze.json")
            _git(root, "commit", "-q", "-m", "fixture exp05 metadata")

            result = execution.register_timing(
                "exp05", repo_root=root,
                provenance_registration="reg/smoke-registration.json",
                dependencies=("fit_dep.py", "frozen/scorer.py"),
            )
            self.assertEqual(result["rows"], 12)
            self.assertEqual(len(_EXP05_WINDOW_VARIANTS), 8)

            for case in self.CASES:
                for arm, t_end in self.T_ENDS.items():
                    registration = (
                        root / ".planning/phases/67-design-settings-ladders"
                        / "evidence/exp05/timing" / case / arm
                        / "registration.json"
                    )
                    self.assertTrue(
                        registration.is_file(), f"missing {case}/{arm}")
                    doc = json.loads(registration.read_bytes())
                    self.assertEqual(
                        doc["settings"]["variant"]["name"],
                        f"exp05-{arm}-{self.ORBIT_ID[case]}",
                    )
                    self.assertEqual(
                        float(doc["settings"]["variant"]["window_length"]),
                        t_end,
                    )

            # The written registration admits through the fit door's
            # settings validation in this same fresh process — the registry
            # lookup that the pre-fix order left unpopulated.
            settings, variant, _orbit_key, _runtime = (
                fit_module.validate_smoke_settings(json.loads(
                    (root / ".planning/phases/67-design-settings-ladders"
                     / "evidence/exp05/timing" / self.CASES[0] / "lap1"
                     / "registration.json").read_bytes())))
            self.assertEqual(variant.name, "exp05-lap1-1632")
            self.assertEqual(
                settings["physical_window"]["t_end"], self.T_ENDS["lap1"])


if __name__ == "__main__":
    unittest.main()
