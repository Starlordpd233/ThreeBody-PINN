"""Phase 43 / 43-02 Task 2 — ``pinn.evaluate`` fail-closed edge cases.

Covers empty test data (non-zero refusal), a checkpoint not owned by a frozen
run, an ``--output`` escaping the runs root, malformed frozen inputs
(corrupted ``config.yaml`` / ``splits.json``), a nonfinite gate metric
rendering an honest FAIL artifact rather than crashing, and the single-
evaluation receipt refusing a second request.

Skip discipline: not-yet-landed production symbols route through ``_require``
and SKIP (never ERROR) — the Phase-43 convention (``tests/phase43/__init__``).
"""

from __future__ import annotations

import importlib
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import torch

from tests.phase39._fixtures import TinyCorpus
from tests.phase43 import _SKIP_PHRASE
from tests.phase43.test_evaluate_gate import _build_run

EVALUATE_MODULE = "pinn.evaluate"


def _require(symbol, module=EVALUATE_MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _all_to_split(split_name):
    SplitRatios = importlib.import_module("pinn.data.splits").SplitRatios
    kwargs = {"train": 0.0, "validation": 0.0, "test": 0.0}
    kwargs[split_name] = 1.0
    return SplitRatios(**kwargs)


class EmptyTestSetTests(unittest.TestCase):
    def test_empty_test_view_refuses_via_evaluate_run(self):
        evaluate_run = _require("evaluate_run")
        EmptyTestSetError = _require("EmptyTestSetError")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            # Every admitted record goes to "train" -> the "test" split is empty.
            runs_root, run_dir, ckpt = _build_run(
                tmp, corpus, ratios=_all_to_split("train")
            )
            with self.assertRaises(EmptyTestSetError):
                evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation",
                    runs_root=runs_root,
                )

    def test_empty_test_view_is_a_nonzero_cli_refusal(self):
        main = _require("main")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(
                tmp, corpus, ratios=_all_to_split("train")
            )
            with mock.patch(f"{EVALUATE_MODULE}._RUNS_ROOT", runs_root):
                exit_code = main(
                    ["--checkpoint", str(ckpt), "--output", str(run_dir / "evaluation")]
                )
        self.assertNotEqual(exit_code, 0)


class CheckpointOwnershipTests(unittest.TestCase):
    def test_missing_checkpoint_file_refuses(self):
        evaluate_run = _require("evaluate_run")
        CheckpointOwnershipError = _require("CheckpointOwnershipError")
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "runs" / "nope" / "checkpoints" / "step-000001.pt"
            with self.assertRaises(CheckpointOwnershipError):
                evaluate_run(
                    checkpoint_path=missing, output_dir=Path(tmp) / "runs" / "nope" / "evaluation",
                    runs_root=Path(tmp) / "runs",
                )

    def test_checkpoint_without_a_frozen_run_refuses(self):
        evaluate_run = _require("evaluate_run")
        CheckpointOwnershipError = _require("CheckpointOwnershipError")
        with tempfile.TemporaryDirectory() as tmp:
            # A checkpoint file exists, but its "run" has no config.yaml/splits.json.
            run_dir = Path(tmp) / "runs" / "orphan-run"
            (run_dir / "checkpoints").mkdir(parents=True)
            ckpt = run_dir / "checkpoints" / "step-000001.pt"
            torch.save({"model": {}}, ckpt)
            with self.assertRaises(CheckpointOwnershipError):
                evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation",
                    runs_root=Path(tmp) / "runs",
                )


class OutputPathGuardTests(unittest.TestCase):
    def test_output_escaping_the_runs_root_refuses(self):
        evaluate_run = _require("evaluate_run")
        OutputPathEscapeError = _require("OutputPathEscapeError")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_split("test"))
            outside = Path(tmp) / "not-runs" / "evaluation"
            with self.assertRaises(OutputPathEscapeError):
                evaluate_run(checkpoint_path=ckpt, output_dir=outside, runs_root=runs_root)


class MalformedFrozenInputTests(unittest.TestCase):
    def test_malformed_config_yaml_fails_honestly(self):
        evaluate_run = _require("evaluate_run")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_split("test"))
            (run_dir / "config.yaml").write_text("not: [valid yaml structure\n", encoding="utf-8")
            with self.assertRaises(Exception):
                evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
                )

    def test_malformed_splits_json_fails_honestly(self):
        evaluate_run = _require("evaluate_run")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_split("test"))
            (run_dir / "splits.json").write_text("{ not json", encoding="utf-8")
            with self.assertRaises(Exception):
                evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
                )

    def test_malformed_frozen_input_is_a_nonzero_cli_refusal_not_a_crash(self):
        main = _require("main")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_split("test"))
            (run_dir / "splits.json").write_text("{ not json", encoding="utf-8")
            with mock.patch(f"{EVALUATE_MODULE}._RUNS_ROOT", runs_root):
                exit_code = main(
                    ["--checkpoint", str(ckpt), "--output", str(run_dir / "evaluation")]
                )
        self.assertNotEqual(exit_code, 0)


class NonfiniteMetricTests(unittest.TestCase):
    def test_nonfinite_aggregate_renders_honest_fail_artifacts_not_a_crash(self):
        evaluate_run = _require("evaluate_run")
        gate_metrics = importlib.import_module("pinn.verification.gate_metrics")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_split("test"))
            forced = gate_metrics.TrajectoryGateMetrics(
                hamiltonian_series=torch.tensor([float("nan")], dtype=torch.float64),
                eps_h=float("nan"),
            )
            with mock.patch.object(
                gate_metrics, "compute_trajectory_gate_metrics", return_value=forced,
            ):
                outcome = evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
                )
            self.assertEqual(outcome.verdict, "FAIL")
            self.assertTrue(math.isnan(outcome.eps_h))

            metrics = json.loads(
                (run_dir / "evaluation" / "metrics.json").read_text(encoding="utf-8")
            )
            self.assertEqual(metrics["verdict"], "FAIL")
            self.assertEqual(metrics["eps_h"], "NaN")

            md_text = (run_dir / "evaluation" / "metrics.md").read_text(encoding="utf-8")
            self.assertIn("OVERALL: FAIL", md_text)
            self.assertIn("nan", md_text.lower())


class RerunReceiptRefusalTests(unittest.TestCase):
    def test_rerun_after_a_receipt_exists_is_a_nonzero_cli_refusal(self):
        main = _require("main")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_split("test"))
            with mock.patch(f"{EVALUATE_MODULE}._RUNS_ROOT", runs_root):
                first = main(
                    ["--checkpoint", str(ckpt), "--output", str(run_dir / "evaluation")]
                )
                second = main(
                    ["--checkpoint", str(ckpt), "--output", str(run_dir / "evaluation")]
                )
        self.assertEqual(first, 0)
        self.assertNotEqual(second, 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
