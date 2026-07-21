"""Phase 43 / 43-02 Task 2 — the closed one-time ``pinn.evaluate`` data flow.

Covers the happy path: ``--checkpoint`` resolves its owning run, loads the
FROZEN ``config.yaml`` + persisted ``splits.json``, selects
``StageIndex.from_split(adapter, manifest, "test")`` (never rebuilding a
split), runs the model forward pass ONCE under ``.eval()`` +
``torch.no_grad()`` over the held-out records' IC13/masses/times, and writes
``metrics.json`` / ``metrics.md`` / ``evaluation-receipt.json`` whose numbers
and verdict agree — plus the single-evaluation rerun refusal and the
receipt's digest binding.

Skip discipline: not-yet-landed production symbols route through ``_require``
and SKIP (never ERROR) — the Phase-43 convention (``tests/phase43/__init__``).
"""

from __future__ import annotations

import hashlib
import importlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import torch

from tests.phase39._fixtures import TinyCorpus
from tests.phase43 import _SKIP_PHRASE

EVALUATE_MODULE = "pinn.evaluate"


def _require(symbol, module=EVALUATE_MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _sha256(path) -> str:
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def _build_run(base_dir, corpus, *, ratios, seed=0, run_name="test-run"):
    """A minimal real (config.yaml + splits.json + checkpoint) run directory.

    ``ratios`` is threaded straight into ``write_split_manifest`` so a test can
    force the WHOLE admitted population into (or out of) the "test" split
    deterministically, without depending on TinyCorpus's exact population size.
    """
    from pinn.architecture_spec import ArchitectureSpec
    from pinn.data.adapter import AdmittedSetAdapter
    from pinn.data.splits import write_split_manifest
    from pinn.network import build_network
    from pinn.training.config import DataConfig, RunConfig, StageConfig, TrainingConfig
    from pinn.training.config_yaml import freeze_resolved_config

    runs_root = Path(base_dir) / "runs"
    run_dir = runs_root / run_name
    (run_dir / "checkpoints").mkdir(parents=True)

    config = TrainingConfig(
        stage=StageConfig(
            max_epochs=1, n_adam=1, stagnation_window=1, percentile_10_relaxation=0.0,
        ),
        run=RunConfig(seed=seed, precision="float64", device="cpu"),
        data=DataConfig(source="admitted", root=str(corpus.data_root)),
    )
    freeze_resolved_config(config, run_dir)

    adapter = AdmittedSetAdapter(root=corpus.data_root, precision="float32", device="cpu")
    write_split_manifest(adapter, run_dir, seed=seed, ratios=ratios)

    arch_spec = ArchitectureSpec(seed=seed)
    model = build_network(arch_spec, dtype=torch.float64, device=torch.device("cpu"))
    checkpoint_path = run_dir / "checkpoints" / "step-000001.pt"
    torch.save({"model": model.state_dict(), "schema_version": 1}, checkpoint_path)

    return runs_root, run_dir, checkpoint_path


def _all_to_test_ratios():
    SplitRatios = importlib.import_module("pinn.data.splits").SplitRatios
    return SplitRatios(train=0.0, validation=0.0, test=1.0)


class ClosedEvaluationFlowTests(unittest.TestCase):
    def test_happy_path_metrics_and_markdown_carry_matching_numbers_and_verdict(self):
        evaluate_run = _require("evaluate_run")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_test_ratios())
            outcome = evaluate_run(
                checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
            )

            metrics_json_path = run_dir / "evaluation" / "metrics.json"
            metrics_md_path = run_dir / "evaluation" / "metrics.md"
            receipt_path = run_dir / "evaluation" / "evaluation-receipt.json"
            self.assertTrue(metrics_json_path.is_file())
            self.assertTrue(metrics_md_path.is_file())
            self.assertTrue(receipt_path.is_file())

            metrics = json.loads(metrics_json_path.read_text(encoding="utf-8"))
            self.assertGreater(metrics["n_test_trajectories"], 0)
            self.assertIn(metrics["verdict"], ("PASS", "FAIL"))
            self.assertEqual(metrics["verdict"], outcome.verdict)
            self.assertEqual(metrics["eps_h"], outcome.eps_h)
            self.assertEqual(metrics["scs"], outcome.scs)

            md_text = metrics_md_path.read_text(encoding="utf-8")
            self.assertIn("## Gate Check", md_text)
            self.assertIn("ε_H", md_text)
            self.assertIn("reject if > 1e-5", md_text)
            self.assertIn("SCS", md_text)
            self.assertIn("reject if > -5", md_text)
            self.assertIn(f"OVERALL: {metrics['verdict']}", md_text)

            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["verdict"], metrics["verdict"])
            self.assertEqual(receipt["eps_h"], metrics["eps_h"])
            self.assertEqual(receipt["scs"], metrics["scs"])

    def test_never_rebuilds_a_split(self):
        evaluate_run = _require("evaluate_run")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_test_ratios())
            with mock.patch(
                "pinn.data.splits.write_split_manifest",
                side_effect=AssertionError("evaluate must never rebuild a split"),
            ):
                evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
                )

    def test_selects_the_test_split_specifically(self):
        evaluate_run = _require("evaluate_run")
        splits_module = importlib.import_module("pinn.data.splits")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_test_ratios())
            with mock.patch.object(
                splits_module.StageIndex, "from_split",
                wraps=splits_module.StageIndex.from_split,
            ) as spy:
                evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
                )
            self.assertEqual(spy.call_count, 1)
            called_split_name = spy.call_args.args[-1] if spy.call_args.args else spy.call_args.kwargs.get("split_name")
            self.assertEqual(called_split_name, "test")

    def test_consumed_trajectory_count_matches_the_persisted_test_split(self):
        evaluate_run = _require("evaluate_run")
        from pinn.data.adapter import AdmittedSetAdapter
        from pinn.data.splits import SplitManifest, StageIndex

        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_test_ratios())
            outcome = evaluate_run(
                checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
            )

            # Independently rebuild the SAME test split via the public contract
            # and cross-check the count evaluate_run actually consumed.
            adapter = AdmittedSetAdapter(root=corpus.data_root, precision="float32", device="cpu")
            manifest = SplitManifest.from_path(run_dir / "splits.json")
            test_index = StageIndex.from_split(adapter, manifest, "test")
            self.assertEqual(outcome.n_test_trajectories, len(test_index.record_keys()))
            self.assertGreater(outcome.n_test_trajectories, 0)

    def test_second_evaluation_of_the_same_output_is_refused(self):
        evaluate_run = _require("evaluate_run")
        EvaluationReceiptExistsError = _require("EvaluationReceiptExistsError")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_test_ratios())
            evaluate_run(
                checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
            )
            with self.assertRaises(EvaluationReceiptExistsError):
                evaluate_run(
                    checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
                )

    def test_receipt_binds_checkpoint_config_and_splits_digests(self):
        evaluate_run = _require("evaluate_run")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_test_ratios())
            evaluate_run(
                checkpoint_path=ckpt, output_dir=run_dir / "evaluation", runs_root=runs_root,
            )
            receipt = json.loads(
                (run_dir / "evaluation" / "evaluation-receipt.json").read_text(encoding="utf-8")
            )
            self.assertEqual(receipt["checkpoint_sha256"], _sha256(ckpt))
            self.assertEqual(receipt["config_sha256"], _sha256(run_dir / "config.yaml"))
            self.assertEqual(receipt["splits_sha256"], _sha256(run_dir / "splits.json"))
            self.assertIn("timestamp", receipt)

    def test_cli_main_exits_zero_on_a_successful_evaluation(self):
        main = _require("main")
        with tempfile.TemporaryDirectory() as tmp, TinyCorpus() as corpus:
            runs_root, run_dir, ckpt = _build_run(tmp, corpus, ratios=_all_to_test_ratios())
            with mock.patch(f"{EVALUATE_MODULE}._RUNS_ROOT", runs_root):
                exit_code = main(
                    ["--checkpoint", str(ckpt), "--output", str(run_dir / "evaluation")]
                )
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
