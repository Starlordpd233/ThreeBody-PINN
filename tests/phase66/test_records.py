"""Plan 66-01 (EXP-01): the phase 66 record and verification contract.

``fit_diagnostic`` records the selected registry beside the registered flag
(the Phase 65 default still records ``locked-12`` as registered with a null
registry), the depth-1 EXP-01 similarity entries carry exactly the ``input``
and ``h1`` rows, the frozen network score and both comparison rows are
present, a registered run publishes a phase 66 record, the loss-trace stride
thins only the recorded trace while every in-memory count stays at 20 steps,
and ``verify_fit_result`` re-checks the registry and the stride triple while a
Phase 65-shaped record still verifies against a Phase 65-shaped registration.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace

import pinn.verification.diagnostic_fit as fit_module
from pinn.verification.diagnostic_phase66 import EXP01_VARIANT
from pinn.verification.learnability_arms import SEED
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import (
    FIXTURE_RUNTIME,
    _fit_registration_fixture,
    _loaded,
    _sha256_bytes,
)
from tests.phase66.test_tracer import patch_data_seam, phase66_fixture_registration


class Phase66RecordTests(unittest.TestCase):
    """The record fields and the verify checks, on the synthetic corpus."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase66-records-")
        ))
        cls.spec, cls.context, cls.scorecard, cls.data = _loaded(cls.fixture)
        if cls.context.attestation is None:
            cls.context = SimpleNamespace(
                **{
                    **vars(cls.context),
                    "attestation": SimpleNamespace(
                        summary=lambda: {"test_split_opens": 0, "withheld_refusals": 0}
                    ),
                }
            )
        if not hasattr(cls.context.reader, "access_summary"):
            cls.context.reader.access_summary = lambda: {
                "requested": [], "opened": [], "refused_before_open": 0,
                "actual_opens": 1,
            }
        cls.fit = fit_module
        cls.exp01_registered = cls.fit.fit_diagnostic(
            EXP01_VARIANT,
            cls.data,
            context=cls.context,
            scorecard=cls.scorecard,
            runtime=FIXTURE_RUNTIME,
            out_dir=cls.tmp / "exp01-registered",
            steps=2,
            times_physical=cls.data.score.times,
            seed=SEED,
            variant_registry="phase66",
        )
        cls.exp01_default = cls.fit.fit_diagnostic(
            EXP01_VARIANT,
            cls.data,
            context=cls.context,
            scorecard=cls.scorecard,
            runtime=FIXTURE_RUNTIME,
            out_dir=cls.tmp / "exp01-default",
            steps=2,
            times_physical=cls.data.score.times,
            seed=SEED,
        )
        cls.locked_default = cls.fit.fit_diagnostic(
            "locked-12",
            cls.data,
            context=cls.context,
            scorecard=cls.scorecard,
            runtime=FIXTURE_RUNTIME,
            out_dir=cls.tmp / "locked-default",
            steps=2,
            times_physical=cls.data.score.times,
            seed=SEED,
        )
        cls.stride_fits = {}
        for stride in (None, 5, 3, 20):
            cls.stride_fits[stride] = cls.fit.fit_diagnostic(
                EXP01_VARIANT,
                cls.data,
                context=cls.context,
                scorecard=cls.scorecard,
                runtime=FIXTURE_RUNTIME,
                out_dir=cls.tmp / f"stride-{stride}",
                steps=20,
                times_physical=cls.data.score.times,
                seed=SEED,
                loss_trace_stride=stride,
            )

    def test_fit_records_registry_and_registered_flag(self):
        self.assertIs(self.exp01_registered["variant"]["registered"], True)
        self.assertEqual(self.exp01_registered["variant"]["registry"], "phase66")
        self.assertIs(self.exp01_default["variant"]["registered"], False)
        self.assertIsNone(self.exp01_default["variant"]["registry"])
        self.assertIs(self.locked_default["variant"]["registered"], True)
        self.assertIsNone(self.locked_default["variant"]["registry"])

    def test_the_record_has_input_and_h1_rows_scores_and_both_comparison_rows(self):
        record = self.exp01_registered
        self.assertTrue(record["similarity"]["entries"])
        for entry in record["similarity"]["entries"]:
            self.assertEqual([row["name"] for row in entry["layers"]], ["input", "h1"])
        network = record["scores"]["network"]
        self.assertIn("E", network)
        self.assertIn("tier", network)
        rows = {row["comparison"]: row for row in record["comparisons"]}
        self.assertIn("score", rows["window_mean_constant"])
        self.assertIn("two_kepler", rows)
        if rows["two_kepler"].get("applicable"):
            self.assertIn("score", rows["two_kepler"])
        else:
            self.assertIn("failure", rows["two_kepler"])

    def test_the_loss_trace_stride_thins_only_the_recorded_trace(self):
        full = self.stride_fits[None]["loss"]
        self.assertEqual(set(full), {"final", "trace"})
        self.assertEqual(len(full["trace"]), 20)
        every5 = self.stride_fits[5]["loss"]
        self.assertEqual(every5["trace_stride"], 5)
        self.assertEqual(len(every5["trace"]), 4)
        self.assertEqual(
            every5["trace"],
            [full["trace"][4], full["trace"][9], full["trace"][14], full["trace"][19]],
        )
        every3 = self.stride_fits[3]["loss"]
        self.assertEqual(every3["trace_stride"], 3)
        self.assertEqual(len(every3["trace"]), 7)
        self.assertEqual(every3["trace"][-1], every3["final"])
        every20 = self.stride_fits[20]["loss"]
        self.assertEqual(every20["trace_stride"], 20)
        self.assertEqual(len(every20["trace"]), 1)
        for record in self.stride_fits.values():
            self.assertEqual(record["steps"]["completed"], 20)
            self.assertEqual(record["steps"]["requested"], 20)

    def test_a_registered_run_publishes_a_phase66_record(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        root, _commit = phase66_fixture_registration(self.tmp / "run-published")
        registration = root / "reg/smoke-registration.json"
        output = self.tmp / "run-published-out" / "record.json"
        patch_data_seam(stack, self.context, self.data, self.spec)
        summary = self.fit.run_registered_smoke(registration, output, repo_root=root)
        self.assertEqual(summary["status"], "complete")
        record = json.loads(output.read_bytes())
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["variant"]["registry"], "phase66")
        self.assertIs(record["variant"]["registered"], True)

    def _provenance_record(self, name, registration_path, root, *, variant, **call_extra):
        doc = json.loads(registration_path.read_bytes())
        return self.fit.fit_diagnostic(
            variant,
            self.data,
            context=self.context,
            scorecard=self.scorecard,
            runtime=FIXTURE_RUNTIME,
            out_dir=self.tmp / name,
            steps=20,
            warmup_steps=2,
            cadence=[0, 5, 10, 15, 20],
            times_physical=self.data.score.times,
            seed=SEED,
            registration_provenance={
                "path": registration_path.relative_to(root).as_posix(),
                "sha256": _sha256_bytes(registration_path.read_bytes()),
            },
            logger_parity_provenance={
                "receipt_path": doc["logger_parity"]["receipt"]["path"],
                "receipt_sha256": doc["logger_parity"]["receipt"]["sha256"],
                "run_commit": doc["logger_parity"]["run_commit"],
            },
            **call_extra,
        )

    @staticmethod
    def _rewrite(out_dir, mutate):
        path = out_dir / "record.json"
        record = json.loads(path.read_bytes())
        mutate(record)
        path.write_bytes(
            (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")
        )

    def test_verify_fit_result_checks_the_registry(self):
        root, _commit = _fit_registration_fixture(self.tmp / "verify-65")
        registration = root / "reg/smoke-registration.json"
        out_dir = self.tmp / "verify-65-record"
        self._provenance_record(
            out_dir.name, registration, root, variant="locked-12"
        )
        # A Phase 65-shaped record (no registry key) still verifies against a
        # registration with no variant_registry key.
        self._rewrite(out_dir, lambda record: record["variant"].pop("registry"))
        report = self.fit.verify_fit_result(registration, out_dir / "record.json", repo_root=root)
        self.assertTrue(report["verified"])

        root, _commit = phase66_fixture_registration(self.tmp / "verify-66")
        registration = root / "reg/smoke-registration.json"
        out_dir = self.tmp / "verify-66-mismatch"
        self._provenance_record(out_dir.name, registration, root, variant=EXP01_VARIANT)
        with self.assertRaises(self.fit.DiagnosticFitRefused) as refused:
            self.fit.verify_fit_result(
                registration, out_dir / "record.json", repo_root=root
            )
        self.assertIn("registry", str(refused.exception))

    def test_verify_fit_result_checks_the_loss_trace_stride(self):
        root, _commit = phase66_fixture_registration(
            self.tmp / "verify-stride", loss_trace_stride=3
        )
        registration = root / "reg/smoke-registration.json"
        out_dir = self.tmp / "verify-stride-record"
        self._provenance_record(
            out_dir.name, registration, root, variant=EXP01_VARIANT,
            variant_registry="phase66", loss_trace_stride=3,
        )
        report = self.fit.verify_fit_result(registration, out_dir / "record.json", repo_root=root)
        self.assertTrue(report["verified"])

        pristine = (out_dir / "record.json").read_bytes()

        def tamper(mutate):
            (out_dir / "record.json").write_bytes(pristine)
            self._rewrite(out_dir, mutate)
            with self.assertRaises(self.fit.DiagnosticFitRefused):
                self.fit.verify_fit_result(
                    registration, out_dir / "record.json", repo_root=root
                )

        def corrupt_last_entry(record):
            record["loss"]["trace"][-1] = record["loss"]["final"] + 1.0

        tamper(lambda record: record["loss"].update(trace_stride=5))
        tamper(lambda record: record["loss"]["trace"].pop(2))
        tamper(corrupt_last_entry)
