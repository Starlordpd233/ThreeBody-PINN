"""Plan 67-05 task 67-05-01: the Phase 67 run-directory reader contract.

``read_phase67_run_directory`` reads one Phase 67 run directory against its
committed registration and the committed design metadata: every admitted
record shape (raw and encoded inputs, every depth, window grids) is validated
in a strict staged order — JSON/object/list/scalar shapes, then
identity/settings against the declared matrix row, then the evidence links
(digests, paths, receipt, attempt), then the numeric and scientific fields —
so every malformed or tampered record, receipt, attempt, weight reference,
layer row, timestamp and attestation becomes an explicit value-free
mechanical or setting problem, never a traceback and never a scientific
reading (66-REVIEW CR-01/CR-02 and WR-01..04 applied to the Phase 67 paths,
65-CLOSEOUT WR-03/WR-04/WR-06/IN-01 affected-use rows). The Sunday 22:00
closing instant is derived from the aware receipt's own instant and the
registered whole-launch cap must fit the remaining allowance exactly at the
boundary. Hostile evidence lives in temporary fixture directories only; no
real corpus, timing or training is accessed.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import struct
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pinn.verification.diagnostic_fit as fit_module
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import _fit_registration_fixture, _loaded
from tests.phase67._fixtures import (
    fake_clock,
    fake_pmset,
    inline_supervisor,
    patch_data_seam,
    phase67_settings,
)

#: The registered schedule at the small synthetic scale (test_checkpoints'
#: registered run): N = 100, 20 warmup, the five normalized similarity events
#: and the three frozen-score checkpoints under the registered 900-second cap.
STEPS = 100
WARMUP = 20
CADENCE = [0, 25, 50, 75, STEPS]
SCORE_CADENCE = [50, 75, STEPS]
STRIDE = 1
CAP = 900.0

#: The value-free problem fragments asserted below (never a score value).
FIT_AUDIT = "the result fails the registration-bound fit verification"
RECORD_UNREADABLE = "the record is not a readable diagnostic record"
LAYERS = "the similarity log does not carry exactly the registered layers in order"
COSINE = "a layer row carries an unusable adjacent-time cosine"
MOVEMENT = "a similarity entry carries an unusable output movement or rate"
COORDINATES = "the recorded time coordinates are not finite and strictly increasing"
GRID = "the recorded grid disagrees with the committed window metadata"
SCHEDULE = "the recorded checkpoint schedule is not the registered Phase 67 schedule"
TIER = "the recorded scorecard grade disagrees with the network error"
BASELINE = "the recorded same-window baselines disagree with the committed expectations"
RAW_FREQUENCY = "a raw-input run carries no finite first-layer frequency"
ENCODED_FREQUENCY = (
    "an encoded run's frequency evidence is not the registered nonapplicability "
    "and feature metadata"
)
ACCESS = "the record carries no access evidence"
TRAIN_ACCESS = "the record attests no TRAIN access"
SPLITS = "a validation or test split was opened"
UNSAFE_PATH = "a record-named file resolves outside the run directory"
SYMLINK = "the run evidence replaces a file with a symbolic link"
TIMESTAMPS = "a receipt or attempt timestamp is missing or not timezone-aware ISO 8601"
ATTEMPT_ORDER = "the attempt does not start after the receipt or end after its start"
ATTEMPT_CAP = "the attempt's whole-run cap disagrees with the registration"
ATTEMPT_STEPS = "the attempt's completed steps disagree with the record"
LAUNCH_WALL = "the launch-to-end wall exceeds the registered whole-launch cap"
SUNDAY_CAP = (
    "the registered whole-launch cap does not fit before the owner's "
    "closing instant"
)
AC_FIRST_LINE = "the receipt's recorded pmset first line does not name AC Power"
IMPROVEMENT = (
    "the recorded score checkpoints cannot settle the final-quarter improvement"
)
SETTING_ORBIT = "the run's orbit is not the matrix row's orbit"
SETTING_SEED = "the run's seed is not the matrix row's seed"
SETTING_ARM = "the run's variant is not the matrix row's arm"
SETTING_EXPERIMENT = "the matrix row names no known Phase 67 experiment"
SETTING_CASE = "the matrix row names no registered case role"

SATURDAY = "2026-10-31T12:00:00-05:00"


def _records():
    """The records module, imported lazily so a missing reader fails per test."""
    from pinn.verification import diagnostic_phase67_records

    return diagnostic_phase67_records


def _float64_digest(values):
    """The windows module's grid digest convention over plain Python floats."""
    packed = struct.pack(f"<{len(values)}d", *[float(value) for value in values])
    return hashlib.sha256(packed).hexdigest()


def _schedule_settings(**overrides):
    """Phase 67 fixture settings carrying the exact registered schedule."""
    settings = phase67_settings(
        optimizer_steps=STEPS,
        warmup_steps=WARMUP,
        measured_steps=STEPS - WARMUP,
        similarity_cadence=list(CADENCE),
        score_cadence=list(SCORE_CADENCE),
        loss_trace_stride=STRIDE,
        whole_run_cap_seconds=CAP,
    )
    settings.update(overrides)
    return settings


def _attested(context):
    """The verify gate's access evidence, the tracer's shim."""
    if context.attestation is None:
        context = SimpleNamespace(
            **{
                **vars(context),
                "attestation": SimpleNamespace(
                    summary=lambda: {"test_split_opens": 0, "withheld_refusals": 0}
                ),
            }
        )
    if not hasattr(context.reader, "access_summary"):
        context.reader.access_summary = lambda: {
            "requested": [], "opened": [], "refused_before_open": 0,
            "actual_opens": 1,
        }
    return context


def _committed_metadata(data, scorecard):
    """The committed window metadata and same-window baselines of the fixture.

    Exactly what a Phase 67 registration commits from the 67-03 evidence
    helpers: the retained grid's endpoint, sample count and both sha256
    digests, and the independently recomputed same-window baseline scores
    (formula nonapplicability retained, never a manufactured score).
    """
    times = [float(value) for value in data.score.times.tolist()]
    tau = [
        float(value)
        for value in data.data_points.tau_ic13[:, 0].tolist()
    ]
    rows = {
        row["comparison"]: row
        for row in fit_module._comparison_rows(data, scorecard=scorecard)
    }
    kepler = rows["two_kepler"]
    applicable = bool(kepler.get("applicable", False))
    baselines = {
        "window_mean_constant": {"E": rows["window_mean_constant"]["score"]["E"]},
        "two_kepler": (
            {"applicable": True, "E": kepler["score"]["E"]}
            if applicable
            else {
                "applicable": False,
                "failure": kepler.get("failure"),
                "reason": kepler.get("reason"),
            }
        ),
    }
    metadata = {
        "first_time": times[0],
        "last_time": times[-1],
        "sample_count": len(times),
        "physical_times_sha256": _float64_digest(times),
        "normalized_tau_sha256": _float64_digest(tau),
    }
    return metadata, baselines


def _launch_run(stack, tmp, context, data, spec, *, variant_settings,
                doc_extra=None, name="run"):
    """A committed registered schedule run through the real launch gate."""
    root, _commit = _fit_registration_fixture(
        tmp / f"repo-{name}",
        settings_extra=variant_settings,
        doc_extra=doc_extra,
    )
    registration = root / "reg/smoke-registration.json"
    output = root / f"evidence/{name}/record.json"

    import pinn.verification.diagnostic_power as power

    def runner(argv, *, cwd):
        patch_data_seam(stack, context, data, spec)
        return fit_module.main(
            argv[6:], repo_root=root, supervisor=inline_supervisor
        )

    code = power.launch(
        registration, output, repo_root=root,
        read_power=fake_pmset("Now drawing from 'AC Power'"), run=runner,
        now=fake_clock(SATURDAY),
    )
    assert code == 0, f"the fixture launch refused: {code}"
    record = json.loads(output.read_bytes())
    return root, registration, output.parent, record


def _copy_run(target, run_dir):
    """A tamperable copy of one run directory's four evidence files."""
    target.mkdir(parents=True, exist_ok=True)
    for name in ("record.json", "diagnostic.weights", "power-gate.json",
                 "attempt.json"):
        shutil.copy2(run_dir / name, target / name)
    return target


def _rewrite(path, mutate):
    """Read, mutate and canonically rewrite one JSON evidence file."""
    payload = json.loads(Path(path).read_bytes())
    mutate(payload)
    Path(path).write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )


def _rewrite_record(run_dir, mutate):
    _rewrite(Path(run_dir) / "record.json", mutate)


def _engineer_times(run_dir, *, checked_utc, local_time, isoweekday,
                    started_utc, ended_utc):
    """Rewrite the receipt and attempt instants as one coherent story."""
    _rewrite(Path(run_dir) / "power-gate.json", lambda receipt: (
        receipt.update(
            checked_utc=checked_utc,
            window={
                "timezone": "America/Chicago",
                "local_time": local_time,
                "isoweekday": isoweekday,
            },
        )
    ))
    _rewrite(Path(run_dir) / "attempt.json", lambda attempt: (
        attempt.update(started_utc=started_utc, ended_utc=ended_utc)
    ))


class _RunTestCase(unittest.TestCase):
    """One real registered 100-step schedule run on the synthetic seam."""

    @classmethod
    def _make_run(cls, *, variant_settings=None, doc_extra=None, name="run"):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-records-")
        ))
        spec, context, scorecard, data = _loaded(fixture)
        context = _attested(context)
        settings = (
            _schedule_settings() if variant_settings is None else variant_settings
        )
        metadata, baselines = _committed_metadata(data, scorecard)
        if doc_extra is None:
            doc_extra = {
                "window_metadata": metadata,
                "window_baselines": baselines,
            }
        return _launch_run(
            stack, tmp, context, data, spec,
            variant_settings=settings, doc_extra=doc_extra, name=name,
        )

    def _read(self, registration, run_dir, root, **kwargs):
        return _records().read_phase67_run_directory(
            registration, run_dir, repo_root=root, **kwargs
        )

    def _matrix_row(self, record, **overrides):
        row = {
            "experiment": "exp02",
            "arm": "d2",
            "case": "main",
            "orbit_key": record["orbit"]["train"]["record_key"],
            "seed": record["seed"],
        }
        row.update(overrides)
        return row


class CleanReadingTests(_RunTestCase):
    """Raw depths read clean with exact identities; scores stay gated."""

    @classmethod
    def setUpClass(cls):
        cls.root, cls.registration, cls.run_dir, cls.record = cls._make_run()

    def test_a_clean_raw_run_reads_clean_with_the_full_reading_shape(self):
        reading = self._read(
            self.registration, self.run_dir, self.root,
            expected_case=self._matrix_row(self.record),
        )
        self.assertEqual(reading["mechanical_problems"], [])
        self.assertEqual(reading["setting_problems"], [])
        identity = reading["identity"]
        self.assertEqual(identity["variant"]["name"], "exp02-d2-w256-o30")
        self.assertEqual(identity["variant"]["registry"], "phase67")
        self.assertEqual(identity["variant"]["depth"], 2)
        self.assertEqual(identity["orbit_key"], self.record["orbit"]["train"]["record_key"])
        self.assertEqual(identity["seed"], 42)
        self.assertEqual(identity["layers"], ["input", "h1", "h2"])
        self.assertEqual(identity["experiment"], "exp02")
        self.assertEqual(identity["arm"], "d2")
        self.assertEqual(identity["case"], "main")
        self.assertEqual(reading["checkpoint_steps"], SCORE_CADENCE)
        self.assertIs(reading["observed_fit"], True)
        # The unsettled flag is the final-quarter improvement rule on the
        # record's own three checkpoints.
        e_mid, e_end = (
            self.record["score_checkpoints"][i]["score"]["E"] for i in (1, 2)
        )
        self.assertIs(reading["unsettled"], (e_mid - e_end) / e_mid > 0.05)
        coordinates = reading["actual_coordinates"]
        self.assertEqual(
            coordinates["physical"], self.record["similarity"]["entries"][-1]["times_physical"]
        )
        self.assertEqual(
            coordinates["raw_tau"], self.record["similarity"]["entries"][-1]["tau_values"]
        )
        self.assertEqual(
            [entry["step"] for entry in reading["layer_trace"]], CADENCE
        )
        for entry in reading["layer_trace"]:
            self.assertEqual(
                [row["name"] for row in entry["layers"]], ["input", "h1", "h2"]
            )
        self.assertNotIn("scores", reading)

    def test_scores_appear_only_on_a_clean_read_with_include_scores(self):
        scored = self._read(
            self.registration, self.run_dir, self.root,
            expected_case=self._matrix_row(self.record), include_scores=True,
        )
        self.assertIn("E", scored["scores"]["network"])
        self.assertIn("tier", scored["scores"]["network"])
        self.assertEqual(
            {row["comparison"] for row in scored["scores"]["comparisons"]},
            {"window_mean_constant", "two_kepler"},
        )
        # A mechanical problem refuses the score exposure, not the reading.
        tampered = _copy_run(self.run_dir.parent / "score-gate", self.run_dir)
        _rewrite_record(tampered, lambda r: r["scores"]["network"].update(tier=3))
        with self.assertRaises(_records().Phase67RecordRefused):
            self._read(
                self.registration, tampered, self.root,
                expected_case=self._matrix_row(self.record), include_scores=True,
            )

    def test_every_matrix_row_mismatch_is_a_setting_problem(self):
        row = self._matrix_row(self.record)
        cases = [
            ("seed", {**row, "seed": 41}, SETTING_SEED),
            ("orbit", {**row, "orbit_key": "hierarchical/gold/9"}, SETTING_ORBIT),
            ("arm", {**row, "arm": "d12"}, SETTING_ARM),
            ("experiment", {**row, "experiment": "exp03"}, SETTING_ARM),
            ("unknown experiment", {**row, "experiment": "exp99"}, SETTING_EXPERIMENT),
            ("unknown case role", {**row, "case": "repeat-none"}, SETTING_CASE),
        ]
        for name, expected_row, problem in cases:
            with self.subTest(mismatch=name):
                reading = self._read(
                    self.registration, self.run_dir, self.root,
                    expected_case=expected_row,
                )
                self.assertIn(problem, reading["setting_problems"])
                self.assertEqual(reading["mechanical_problems"], [])

    def test_a_malformed_matrix_row_refuses(self):
        for bad in (
            {"experiment": "exp02"},
            "exp02/d2/main",
            {"experiment": 42, "arm": "d2", "case": "main",
             "orbit_key": "hierarchical/gold/0", "seed": 42},
            {"experiment": "exp02", "arm": "d2", "case": "main",
             "orbit_key": "hierarchical/gold/0", "seed": True},
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self._read(
                        self.registration, self.run_dir, self.root,
                        expected_case=bad,
                    )

    def test_a_registration_without_the_registered_schedule_refuses(self):
        with tempfile.TemporaryDirectory(prefix="phase67-nosched-") as raw:
            root, _commit = _fit_registration_fixture(
                Path(raw) / "repo", settings_extra=phase67_settings()
            )
            with self.assertRaises(_records().Phase67RecordRefused) as raised:
                self._read(
                    root / "reg/smoke-registration.json",
                    root / "evidence/none", root,
                )
            self.assertIn("score cadence", str(raised.exception))

    def test_a_registration_without_committed_window_metadata_refuses(self):
        with tempfile.TemporaryDirectory(prefix="phase67-nometa-") as raw:
            stack = ExitStack()
            self.addCleanup(stack.close)
            fixture = stack.enter_context(gold_corpus_fixture())
            tmp = Path(raw)
            spec, context, scorecard, data = _loaded(fixture)
            context = _attested(context)
            root, registration, run_dir, _record = _launch_run(
                stack, tmp, context, data, spec,
                variant_settings=_schedule_settings(), doc_extra=None, name="nometa",
            )
            with self.assertRaises(_records().Phase67RecordRefused) as raised:
                self._read(registration, run_dir, root)
            self.assertIn("window metadata", str(raised.exception))


class HostileRecordShapeTests(_RunTestCase):
    """Malformed and tampered records refuse without a traceback."""

    @classmethod
    def setUpClass(cls):
        cls.root, cls.registration, cls.run_dir, cls.record = cls._make_run()

    def _problem_case(self, name, mutate, problem, *, receipt=None, attempt=None,
                       record_bytes=None):
        with self.subTest(case=name):
            target = _copy_run(self.run_dir.parent / f"hostile-{name}", self.run_dir)
            if record_bytes is not None:
                (target / "record.json").write_bytes(record_bytes)
            elif mutate is not None:
                _rewrite_record(target, mutate)
            if receipt is not None:
                (target / "power-gate.json").write_bytes(receipt)
            if attempt is not None:
                (target / "attempt.json").write_bytes(attempt)
            reading = self._read(
                self.registration, target, self.root,
                expected_case=self._matrix_row(self.record),
            )
            self.assertIn(problem, reading["mechanical_problems"])
            self.assertIn("unsettled", reading)
            with self.assertRaises(_records().Phase67RecordRefused):
                self._read(
                    self.registration, target, self.root,
                    expected_case=self._matrix_row(self.record), include_scores=True,
                )

    def test_array_string_null_and_truncated_record_roots_refuse(self):
        for name, raw in (
            ("array", b"[1, 2, 3]\n"),
            ("string", b'"a record"\n'),
            ("null", b"null\n"),
            ("number", b"17\n"),
            ("truncated", b'{"status": "comp'),
        ):
            self._problem_case(
                f"root-{name}", None, RECORD_UNREADABLE, record_bytes=raw
            )

    def test_bad_nested_similarity_blocks_refuse(self):
        entries = [
            ("entries not a list", lambda r: r["similarity"].update(entries={"0": 1}), LAYERS),
            ("entry not an object", lambda r: r["similarity"]["entries"].__setitem__(0, [1]), LAYERS),
            ("layers missing", lambda r: r["similarity"]["entries"][0].pop("layers"), LAYERS),
            ("extra layer", lambda r: r["similarity"]["entries"][0]["layers"].append(
                {"name": "h3", "order": 3, "adjacent_cosine_mean": 0.9}), LAYERS),
            ("duplicate layer", lambda r: r["similarity"]["entries"][0]["layers"].append(
                r["similarity"]["entries"][0]["layers"][1]), LAYERS),
            ("missing deep layer", lambda r: r["similarity"]["entries"].__setitem__(
                0, {**r["similarity"]["entries"][0],
                    "layers": r["similarity"]["entries"][0]["layers"][:1]}), LAYERS),
            ("order not increasing", lambda r: r["similarity"]["entries"][0]["layers"][1].update(order=5), LAYERS),
            ("cadence tampered", lambda r: r["similarity"].update(cadence=[0, 25, 50, 99, 100]), SCHEDULE),
            ("checkpoints missing", lambda r: r.pop("score_checkpoints"), SCHEDULE),
            ("checkpoint steps tampered", lambda r: r["score_checkpoints"][0].update(step=25), SCHEDULE),
        ]
        for name, mutate, problem in entries:
            self._problem_case(name, mutate, problem)

    def test_unusable_cosines_movements_and_coordinates_refuse(self):
        cases = [
            ("cosine out of range", lambda r: r["similarity"]["entries"][0]["layers"][1].update(adjacent_cosine_mean=1.5), COSINE),
            ("cosine boolean", lambda r: r["similarity"]["entries"][0]["layers"][1].update(adjacent_cosine_mean=True), COSINE),
            ("cosine string", lambda r: r["similarity"]["entries"][0]["layers"][1].update(adjacent_cosine_mean="0.98"), COSINE),
            ("cosine nonfinite", lambda r: r["similarity"]["entries"][0]["layers"][1].update(adjacent_cosine_mean=float("inf")), COSINE),
            ("movement string", lambda r: r["similarity"]["entries"][0]["output_movement"].update(value="0.5"), MOVEMENT),
            ("movement missing", lambda r: r["similarity"]["entries"][0].pop("output_movement"), MOVEMENT),
            ("rate nonfinite", lambda r: r["similarity"]["entries"][0]["output_rate_ratio"].update(value=float("nan")), MOVEMENT),
            ("times not increasing", lambda r: r["similarity"]["entries"][0]["times_physical"].reverse(), COORDINATES),
            ("tau nonfinite", lambda r: r["similarity"]["entries"][0]["tau_values"].__setitem__(3, float("nan")), COORDINATES),
            ("coordinates nonfinite", lambda r: r["similarity"]["entries"][0]["times_physical"].__setitem__(2, float("inf")), COORDINATES),
        ]
        for name, mutate, problem in cases:
            self._problem_case(name, mutate, problem)

    def test_boolean_and_scientific_string_numbers_refuse(self):
        cases = [
            ("E a string", lambda r: r["scores"]["network"].update(E="5.7e0"), TIER),
            ("E a boolean", lambda r: r["scores"]["network"].update(E=True), TIER),
            ("tier a boolean", lambda r: r["scores"]["network"].update(tier=True), TIER),
            ("tier disagreeing", lambda r: r["scores"]["network"].update(tier=3), TIER),
            ("checkpoint E a string", lambda r: r["score_checkpoints"][2]["score"].update(E="1e-3"), IMPROVEMENT),
            ("checkpoint tier a boolean", lambda r: r["score_checkpoints"][1]["score"].update(tier=False), TIER),
            ("checkpoint eps_h missing", lambda r: r["score_checkpoints"][1]["score"].pop("eps_h"), TIER),
        ]
        for name, mutate, problem in cases:
            self._problem_case(name, mutate, problem)

    def test_grid_and_baseline_substitutions_refuse(self):
        committed = json.loads(self.registration.read_bytes())["window_baselines"]
        kepler_applicable = committed["two_kepler"]["applicable"]

        def flip_kepler(record):
            row = next(
                row for row in record["comparisons"]
                if row["comparison"] == "two_kepler"
            )
            if kepler_applicable:
                row.pop("score", None)
                row["applicable"] = False
                row["failure"] = "manufactured refusal"
            else:
                row.pop("failure", None)
                row.pop("reason", None)
                row["applicable"] = True
                row["score"] = {"E": 0.5}

        cases = [
            ("grid tampered", lambda r: r["similarity"]["entries"][0]["times_physical"].__setitem__(
                5, r["similarity"]["entries"][0]["times_physical"][5] + 1e-9), GRID),
            ("grid endpoint tampered", lambda r: r["similarity"]["entries"][0]["times_physical"].__setitem__(
                -1, r["similarity"]["entries"][0]["times_physical"][-1] - 1e-9), GRID),
            ("constant baseline substituted", lambda r: next(
                row for row in r["comparisons"]
                if row["comparison"] == "window_mean_constant"
            )["score"].update(E=r["comparisons"][0]["score"]["E"] + 0.1), BASELINE),
            ("kepler applicability flipped", flip_kepler, BASELINE),
        ]
        for name, mutate, problem in cases:
            self._problem_case(name, mutate, problem)

    def test_raw_frequency_and_access_evidence_refuse(self):
        cases = [
            ("raw median nulled", lambda r: r["similarity"]["entries"][0]["first_layer_frequency"].update(median=None), RAW_FREQUENCY),
            ("raw max a string", lambda r: r["similarity"]["entries"][0]["first_layer_frequency"].update(max="14.8"), RAW_FREQUENCY),
            ("attestation null", lambda r: r["access"].update(attestation=None), ACCESS),
            ("access block missing", lambda r: r.pop("access"), ACCESS),
            ("no train read", lambda r: r["access"]["reads"].update(train=0), TRAIN_ACCESS),
            ("reads block missing", lambda r: r["access"].pop("reads"), TRAIN_ACCESS),
            ("a validation open", lambda r: r["access"]["reads"].update(validation=1), SPLITS),
            ("a test split open", lambda r: r["access"].update(attestation={"test_split_opens": 1}), SPLITS),
            ("stale source pins", lambda r: r.update(source_sha256={"pinn/x.py": "0" * 64}), FIT_AUDIT),
        ]
        for name, mutate, problem in cases:
            self._problem_case(name, mutate, problem)

    def test_unsafe_and_symlinked_weight_references_refuse(self):
        outside = self.run_dir.parent / "outside.weights"
        outside.write_bytes(b"not weights")
        target = _copy_run(self.run_dir.parent / "hostile-symlink", self.run_dir)
        (target / "linked.weights").symlink_to(outside.resolve())
        self._problem_case(
            "parent-relative weights", lambda r: r["weights"].update(file="../outside.weights"), UNSAFE_PATH
        )
        self._problem_case(
            "absolute weights", lambda r: r["weights"].update(file=str(outside.resolve())), UNSAFE_PATH
        )
        self._problem_case(
            "subdirectory weights", lambda r: r["weights"].update(file="sub/weights"), UNSAFE_PATH
        )
        _rewrite_record(target, lambda r: r["weights"].update(file="linked.weights"))
        reading = self._read(
            self.registration, target, self.root,
            expected_case=self._matrix_row(self.record),
        )
        self.assertIn(SYMLINK, reading["mechanical_problems"])

    def test_a_changed_dependency_registration_refuses_admission(self):
        with tempfile.TemporaryDirectory(prefix="phase67-dep-") as raw:
            root, _commit = _fit_registration_fixture(
                Path(raw) / "repo", kind="changed_dependency",
                settings_extra=_schedule_settings(),
            )
            from pinn.verification.diagnostic_guard import DiagnosticRegistrationRefused

            with self.assertRaises(DiagnosticRegistrationRefused):
                self._read(
                    root / "reg/smoke-registration.json",
                    root / "evidence/none", root,
                )


class ReceiptAndAttemptTests(_RunTestCase):
    """The receipt, attempt and whole-launch-cap audit on engineered instants."""

    @classmethod
    def setUpClass(cls):
        cls.root, cls.registration, cls.run_dir, cls.record = cls._make_run()

    def _read(self, run_dir, **kwargs):
        return _records().read_phase67_run_directory(
            self.registration, run_dir, repo_root=self.root, **kwargs
        )

    def test_the_cap_fits_the_sunday_closing_exactly_and_not_one_instant_later(self):
        # checked 21:45:00.000000-06:00 Sunday + the 900 s cap lands exactly on
        # the derived Sunday 22:00 closing instant.
        exact = _copy_run(self.run_dir.parent / "sunday-exact", self.run_dir)
        _engineer_times(
            exact,
            checked_utc="2026-11-02T03:45:00+00:00",
            local_time="2026-11-01T21:45:00-06:00",
            isoweekday=7,
            started_utc="2026-11-02T03:45:01+00:00",
            ended_utc="2026-11-02T03:46:00+00:00",
        )
        reading = self._read(exact)
        self.assertEqual(reading["mechanical_problems"], [])

        late = _copy_run(self.run_dir.parent / "sunday-next", self.run_dir)
        _engineer_times(
            late,
            checked_utc="2026-11-02T03:45:00.000001+00:00",
            local_time="2026-11-01T21:45:00.000001-06:00",
            isoweekday=7,
            started_utc="2026-11-02T03:45:01+00:00",
            ended_utc="2026-11-02T03:46:00+00:00",
        )
        reading = self._read(late)
        self.assertIn(SUNDAY_CAP, reading["mechanical_problems"])

    def test_naive_and_mixed_and_late_and_unordered_timestamps_refuse(self):
        base = dict(
            checked_utc="2026-11-02T03:45:00+00:00",
            local_time="2026-11-01T21:45:00-06:00",
            isoweekday=7,
        )
        cases = [
            ("naive checked", {**base, "started_utc": "2026-11-02T03:45:01+00:00", "ended_utc": "2026-11-02T03:46:00+00:00"}, dict(checked_utc="2026-11-01T21:45:00"), TIMESTAMPS),
            ("naive started", {**base, "started_utc": "2026-11-01T21:45:01", "ended_utc": "2026-11-02T03:46:00+00:00"}, {}, TIMESTAMPS),
            ("naive ended", {**base, "started_utc": "2026-11-02T03:45:01+00:00", "ended_utc": "2026-11-01T21:46:00"}, {}, TIMESTAMPS),
            ("late receipt", {**base, "checked_utc": "2026-11-02T03:46:00+00:00", "started_utc": "2026-11-02T03:45:01+00:00", "ended_utc": "2026-11-02T03:47:00+00:00"}, {}, "the receipt was written after the attempt started"),
            ("ended before start", {**base, "started_utc": "2026-11-02T03:46:30+00:00", "ended_utc": "2026-11-02T03:46:00+00:00"}, {}, ATTEMPT_ORDER),
            ("wall beyond the cap", {**base, "started_utc": "2026-11-02T03:45:01+00:00", "ended_utc": "2026-11-02T04:00:01+00:00"}, {}, LAUNCH_WALL),
        ]
        for name, times, receipt_overrides, problem in cases:
            with self.subTest(case=name):
                target = _copy_run(self.run_dir.parent / f"ts-{name}", self.run_dir)
                _engineer_times(target, **times)
                if receipt_overrides:
                    _rewrite(target / "power-gate.json", lambda r: r.update(receipt_overrides))
                reading = self._read(target)
                self.assertIn(problem, reading["mechanical_problems"])

    def test_a_weekday_receipt_inside_the_owner_amendment_reads_clean(self):
        # The real 2026-11-03 capture instant: a Tuesday the owner's
        # amendment admits (deadline 2026-11-07 07:30, like its expired
        # 2026-11-04 07:30 and 2026-11-05 07:30 predecessors).
        weekday = _copy_run(self.run_dir.parent / "weekday-amended", self.run_dir)
        _engineer_times(
            weekday,
            checked_utc="2026-11-03T17:57:47+00:00",
            local_time="2026-11-03T11:57:47-06:00",
            isoweekday=2,
            started_utc="2026-11-03T17:57:48+00:00",
            ended_utc="2026-11-03T17:58:47+00:00",
        )
        reading = self._read(weekday)
        self.assertEqual(reading["mechanical_problems"], [])

    def test_a_pre_deadline_friday_receipt_fits_the_cap_before_the_saturday_closing(self):
        # The 2026-11-07 07:30 amendment deadline is a Saturday morning, so
        # every admitted Friday instant closes at that deadline with hours
        # of runway: the 900 s cap fits at 07:15 and at the last
        # pre-midnight instant alike. The exact cap boundary is only
        # constructible at the Sunday closing (covered above) — a weekday
        # boundary case cannot exist against a next-morning-Saturday
        # deadline, and the post-deadline weekday refusal is covered by
        # test_a_weekday_after_the_amendment_deadline_refuses.
        early = _copy_run(self.run_dir.parent / "weekday-early", self.run_dir)
        _engineer_times(
            early,
            checked_utc="2026-11-06T13:14:00+00:00",
            local_time="2026-11-06T07:15:00-06:00",
            isoweekday=5,
            started_utc="2026-11-06T13:14:01+00:00",
            ended_utc="2026-11-06T13:15:00+00:00",
        )
        reading = self._read(early)
        self.assertEqual(reading["mechanical_problems"], [])

        last = _copy_run(self.run_dir.parent / "weekday-last", self.run_dir)
        _engineer_times(
            last,
            checked_utc="2026-11-07T05:59:00+00:00",
            local_time="2026-11-06T23:59:00-06:00",
            isoweekday=5,
            started_utc="2026-11-07T05:59:01+00:00",
            ended_utc="2026-11-07T06:00:00+00:00",
        )
        reading = self._read(last)
        self.assertEqual(reading["mechanical_problems"], [])

    def test_a_weekday_after_the_amendment_deadline_refuses(self):
        # The 2026-11-07 07:30 deadline instant itself is a Saturday, so it
        # is weekend-admitted; the weekday refusals are the days after it.
        cases = [
            ("monday after the deadline", "2026-11-09T12:00:00-06:00", 1),
            ("tuesday after the deadline", "2026-11-10T12:00:00-06:00", 2),
        ]
        for name, local_time, isoweekday in cases:
            with self.subTest(case=name):
                target = _copy_run(
                    self.run_dir.parent / f"weekday-refused-{name}",
                    self.run_dir,
                )
                _engineer_times(
                    target,
                    checked_utc="2026-11-09T18:00:00+00:00",
                    local_time=local_time,
                    isoweekday=isoweekday,
                    started_utc="2026-11-09T18:00:01+00:00",
                    ended_utc="2026-11-09T18:01:00+00:00",
                )
                reading = self._read(target)
                self.assertIn(
                    "the receipt window is outside the weekend window",
                    reading["mechanical_problems"],
                )

    def test_forged_weekdays_and_foreign_first_lines_refuse(self):
        cases = [
            ("forged saturday weekday", {"local_time": "2026-10-28T12:00:00-05:00", "isoweekday": 6},
             "the receipt window is outside the weekend window"),
            ("battery first line", None, AC_FIRST_LINE),
        ]
        for name, window, problem in cases:
            with self.subTest(case=name):
                target = _copy_run(self.run_dir.parent / f"receipt-{name}", self.run_dir)
                if window is not None:
                    _rewrite(
                        target / "power-gate.json",
                        lambda r: r.update(window={
                            "timezone": "America/Chicago", **window,
                        }),
                    )
                else:
                    _rewrite(
                        target / "power-gate.json",
                        lambda r: r.update(pmset_first_line="Now drawing from 'Battery Power'"),
                    )
                reading = self._read(target)
                self.assertIn(problem, reading["mechanical_problems"])

    def test_incomplete_and_drifted_attempts_refuse(self):
        cases = [
            ("incomplete", lambda a: a.update(status="incomplete"), "the attempt is not published"),
            ("cap drift", lambda a: a.update(whole_run_cap_seconds=800.0), ATTEMPT_CAP),
            ("steps drift", lambda a: a.update(completed_steps=99), ATTEMPT_STEPS),
            ("digest drift", lambda a: a.update(record_sha256="f" * 64), "the attempt's record digest disagrees with the record bytes"),
            ("missing", None, "the attempt claim is missing"),
            ("unreadable", None, "the attempt claim is not a readable JSON object"),
        ]
        for name, mutate, problem in cases:
            with self.subTest(case=name):
                target = _copy_run(self.run_dir.parent / f"attempt-{name}", self.run_dir)
                if name == "missing":
                    (target / "attempt.json").unlink()
                elif name == "unreadable":
                    (target / "attempt.json").write_bytes(b"[1]\n")
                else:
                    _rewrite(target / "attempt.json", mutate)
                reading = self._read(target)
                self.assertIn(problem, reading["mechanical_problems"])

    def test_missing_and_malformed_receipts_refuse(self):
        missing = _copy_run(self.run_dir.parent / "receipt-missing", self.run_dir)
        (missing / "power-gate.json").unlink()
        self.assertIn(
            "the power-gate receipt is missing",
            self._read(missing)["mechanical_problems"],
        )
        malformed = _copy_run(self.run_dir.parent / "receipt-array", self.run_dir)
        (malformed / "power-gate.json").write_bytes(b"[1]\n")
        self.assertIn(
            "the power-gate receipt is not a readable JSON object",
            self._read(malformed)["mechanical_problems"],
        )


class ImprovementFieldTests(_RunTestCase):
    """The reading's unsettled field is the exact 5 percent boundary rule."""

    @classmethod
    def setUpClass(cls):
        cls.root, cls.registration, cls.run_dir, cls.record = cls._make_run()

    def _unsettled(self, mid_e, end_e):
        target = _copy_run(self.run_dir.parent / "improvement", self.run_dir)
        _rewrite_record(target, lambda r: (
            r["score_checkpoints"][1]["score"].update(E=mid_e, tier=0),
            r["score_checkpoints"][2]["score"].update(E=end_e, tier=0),
            r["scores"]["network"].update(E=end_e, tier=0),
        ))
        reading = self._read(self.registration, target, self.root)
        self.assertIn("unsettled", reading)
        return reading["unsettled"]

    def test_exact_five_percent_is_settled_and_the_next_instant_is_not(self):
        import math

        mid = 20.0
        exact = 19.0  # (20 - 19)/20 == 0.05 exactly in float64
        self.assertEqual((mid - exact) / mid, 0.05)
        self.assertIs(self._unsettled(mid, exact), False)
        larger = math.nextafter(exact, -math.inf)
        self.assertGreater((mid - larger) / mid, 0.05)
        self.assertIs(self._unsettled(mid, larger), True)

    def test_a_zero_reference_final_zero_is_settled_and_positive_final_is_worsening(self):
        self.assertIs(self._unsettled(0.0, 0.0), False)
        self.assertIs(self._unsettled(0.0, 0.5), False)

    def test_negative_or_nonfinite_final_quarter_errors_are_problems(self):
        for mid, end in ((-1.0, -0.5), (float("nan"), 0.5), (2.0, float("inf"))):
            with self.subTest(mid=mid, end=end):
                target = _copy_run(
                    self.run_dir.parent / f"improvement-bad-{mid!r}", self.run_dir
                )
                _rewrite_record(target, lambda r, mid=mid, end=end: (
                    r["score_checkpoints"][1]["score"].update(E=mid, tier=0),
                    r["score_checkpoints"][2]["score"].update(E=end, tier=0),
                ))
                reading = self._read(self.registration, target, self.root)
                self.assertIn(IMPROVEMENT, reading["mechanical_problems"])


class EncodedReadingTests(_RunTestCase):
    """An encoded (D-05) run reads clean with its registered feature metadata."""

    @classmethod
    def setUpClass(cls):
        from pinn.verification.diagnostic_phase67_catalog import (
            CENSUS_N_IN_1632,
            CENSUS_PANELS_SCHEMA,
            EXP04_LOCKED_F1_VARIANT,
        )

        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-encoded-")
        ))
        panels = tmp / "panels.json"
        panels.write_bytes(json.dumps({
            "schema": CENSUS_PANELS_SCHEMA,
            "singles": [{"id": 0, "N_in": CENSUS_N_IN_1632}],
        }).encode("utf-8"))
        import pinn.verification.diagnostic_phase67_catalog as catalog

        stack.enter_context(mock.patch.object(
            catalog, "_default_panels_path", return_value=panels
        ))
        spec, context, scorecard, data = _loaded(fixture)
        context = _attested(context)
        metadata, baselines = _committed_metadata(data, scorecard)
        settings = _schedule_settings(
            variant=EXP04_LOCKED_F1_VARIANT.to_json_dict()
        )
        cls.root, cls.registration, cls.run_dir, cls.record = _launch_run(
            stack, tmp, context, data, spec,
            variant_settings=settings,
            doc_extra={"window_metadata": metadata, "window_baselines": baselines},
            name="encoded",
        )

    def _read(self, run_dir=None, **kwargs):
        return _records().read_phase67_run_directory(
            self.registration, run_dir or self.run_dir, repo_root=self.root, **kwargs
        )

    def test_an_encoded_run_reads_clean_at_every_registered_layer(self):
        row = {
            "experiment": "exp04",
            "arm": "locked-f1",
            "case": "main",
            "orbit_key": self.record["orbit"]["train"]["record_key"],
            "seed": self.record["seed"],
        }
        reading = self._read(expected_case=row)
        self.assertEqual(reading["mechanical_problems"], [])
        self.assertEqual(reading["setting_problems"], [])
        self.assertEqual(reading["identity"]["variant"]["name"], "exp04-locked-f1")
        self.assertEqual(reading["identity"]["variant"]["time_features"], "tau_ic13_fourier1")
        self.assertEqual(
            reading["identity"]["layers"],
            ["input"] + [f"h{order}" for order in range(1, 13)],
        )

    def test_manufactured_applicability_and_drifted_metadata_refuse(self):
        entry = self.record["similarity"]["entries"][0]

        def manufacture(record):
            block = record["similarity"]["entries"][0]
            block["first_layer_frequency"].update(median=4.2, max=14.8)
            block.pop("frequency_applicability", None)
            block.pop("frequency_reason", None)

        def drift_harmonics(record):
            record["similarity"]["entries"][0]["feature_harmonics"] = [1, 2]

        def drift_dimension(record):
            record["similarity"]["entries"][0]["internal_input_dimension"] = 18

        def drift_frequency(record):
            record["similarity"]["entries"][0]["feature_frequency_cycles"] = [0.5]

        for name, mutate in (
            ("manufactured applicability", manufacture),
            ("drifted harmonics", drift_harmonics),
            ("drifted internal dimension", drift_dimension),
            ("drifted feature frequency", drift_frequency),
        ):
            with self.subTest(case=name):
                target = _copy_run(self.run_dir.parent / f"encoded-{name}", self.run_dir)
                _rewrite_record(target, mutate)
                reading = self._read(target)
                self.assertIn(ENCODED_FREQUENCY, reading["mechanical_problems"])
                # The clean entry carried the registered nonapplicability.
                self.assertIs(entry.get("frequency_applicability"), False)
                self.assertIsNotNone(entry.get("frequency_reason"))

    def test_a_float32_round_trip_of_the_registered_cycles_admits(self):
        """A faithful float32 run emits the closest float32 to the constant.

        The registrations declare mps/float32 and the encoder carries its
        registered frequencies in float32 buffers, so a real run's evidence
        holds ``float32(registered)``; the reader must identify that as the
        registration (the first real encoded timing row tripped the old
        float64-exact comparison on exactly this round-trip).
        """
        entry = self.record["similarity"]["entries"][0]
        registered = entry["feature_frequency_cycles"][0]
        round_trip = struct.unpack("<f", struct.pack("<f", registered))[0]
        self.assertNotEqual(round_trip, registered)

        def to_float32(record):
            for block in record["similarity"]["entries"]:
                block["feature_frequency_cycles"] = [
                    struct.unpack("<f", struct.pack("<f", value))[0]
                    for value in block["feature_frequency_cycles"]
                ]

        target = _copy_run(self.run_dir.parent / "encoded-f32-cycles", self.run_dir)
        _rewrite_record(target, to_float32)
        reading = self._read(target)
        # The rewrite invalidates the attempt's record digest by design; the
        # frequency identity itself must read clean.
        self.assertNotIn(ENCODED_FREQUENCY, reading["mechanical_problems"])

    def test_a_near_miss_cycles_value_still_refuses(self):
        """Neither the constant nor its float32 round-trip: a refusal."""
        def near_miss(record):
            for block in record["similarity"]["entries"]:
                block["feature_frequency_cycles"] = [
                    value + 1e-6 for value in block["feature_frequency_cycles"]
                ]

        target = _copy_run(self.run_dir.parent / "encoded-near-miss", self.run_dir)
        _rewrite_record(target, near_miss)
        reading = self._read(target)
        self.assertIn(ENCODED_FREQUENCY, reading["mechanical_problems"])


if __name__ == "__main__":
    unittest.main()
