"""INST-01 wiring + summary-projection suite (plan 46-07, Tasks 2-3).

Drives the ``pinn/train.py`` gate seam and the ``pinn/training/summary.py``
projection against the 46-01 stub fixtures and the REAL validation_gate
publishers — sidecars are never hand-rolled where the production writer exists.
No real run directory, corpus file, or training loop is used; every run dir is a
stdlib temp directory.

The production symbols land in this plan, so every test RUNS; the ``_require``
helper is retained per the package skip discipline and emits ``_SKIP_PHRASE``
only if a symbol is somehow absent.
"""

from __future__ import annotations

import ast
import importlib
import json
import pathlib
import tempfile
import unittest
from pathlib import Path

import torch

from pinn.training import summary as summary_mod
from pinn.training import validation_gate as vg

from tests.phase46 import _SKIP_PHRASE
from tests.phase46._fixtures import (
    StubModel,
    make_empty_source,
    make_stub_split_sources,
)


def _require(symbol, module="pinn.train"):
    """Fetch a later-wave production symbol or skip with the package phrase."""
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


# ---------------------------------------------------------------------------
# Source extraction (verbatim from tests/phase40/test_prohibitions.py:73-92).
# ---------------------------------------------------------------------------

def executable_source_from_text(text, filename="<synthetic>"):
    """Return executable Python text, docstrings and comments stripped."""
    tree = ast.parse(text, filename=filename)
    doc_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and node.body and isinstance(node.body[0], ast.Expr):
                expr = node.body[0]
                for ln in range(expr.lineno, (expr.end_lineno or expr.lineno) + 1):
                    doc_lines.add(ln)
    return "\n".join(
        line.strip()
        for ln, line in enumerate(text.splitlines(), start=1)
        if ln not in doc_lines and line.strip() and not line.lstrip().startswith("#")
    )


def executable_source(path):
    return executable_source_from_text(pathlib.Path(path).read_text(encoding="utf-8"), str(path))


class _RuntimeSpecStub:
    """Minimal stand-in: the seam reads only dtype and torch_device."""

    dtype = torch.float64
    torch_device = torch.device("cpu")


class _PoisonedSource:
    """Non-empty pool whose record access raises mid-pass."""

    def __init__(self, inner):
        self._inner = inner

    def records_at_or_below(self, stage):
        return self._inner.records_at_or_below(stage)

    def get(self, key):
        raise RuntimeError("poisoned validation source")


# ---------------------------------------------------------------------------
# Task 2 — the train.py seam
# ---------------------------------------------------------------------------


class ValidationGateSeamTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="phase46-wiring-")
        self.root = Path(self.tmp.name)
        self.source = make_stub_split_sources()[1]
        self.run_gate_pass = _require("_run_validation_gate_pass")
        self.append_record = _require("_append_validation_record")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_ok_path_publishes_sidecar_before_returning_pointer_fields(self) -> None:
        fields = self.run_gate_pass(
            StubModel(),
            self.source,
            stage=0,
            global_step=64,
            run_dir=self.root,
            runtime_spec=_RuntimeSpecStub(),
        )
        self.assertEqual(fields["gate_status"], "ok")
        self.assertEqual(fields["gate_schema_version"], vg.GATE_SIDECAR_SCHEMA_VERSION)
        rel = fields["gate_sidecar"]
        self.assertEqual(rel, vg.sidecar_relative_path(64))
        sidecar = self.root / rel
        self.assertTrue(sidecar.is_file(), "pointer returned without a durable sidecar")
        # The pointer is only legitimate if the pointed file validates (D-17).
        vg.validate_sidecar_payload(json.loads(sidecar.read_text(encoding="utf-8")))
        for key in ("gate_eps_h", "gate_scs", "gate_verdict", "gate_n_trajectories"):
            self.assertIn(key, fields)

    def test_empty_pool_converts_to_failure_fields_without_raising(self) -> None:
        fields = self.run_gate_pass(
            StubModel(),
            make_empty_source(),
            stage=0,
            global_step=8,
            run_dir=self.root,
            runtime_spec=_RuntimeSpecStub(),
        )
        self.assertTrue(fields["gate_status"].startswith("failed:"), fields)
        self.assertNotIn("gate_sidecar", fields)
        self.assertEqual(fields["gate_schema_version"], vg.GATE_SIDECAR_SCHEMA_VERSION)

    def test_poisoned_source_fails_closed_and_restores_prior_model_mode(self) -> None:
        model = StubModel()
        model.train(True)
        fields = self.run_gate_pass(
            model,
            _PoisonedSource(self.source),
            stage=0,
            global_step=16,
            run_dir=self.root,
            runtime_spec=_RuntimeSpecStub(),
        )
        self.assertTrue(fields["gate_status"].startswith("failed:"), fields)
        self.assertNotIn("gate_sidecar", fields)
        self.assertTrue(model.training, "prior train mode was not restored")

    def test_gate_fields_merge_into_the_appended_record_with_sentinels(self) -> None:
        path = self.root / "validation.jsonl"
        gate_fields = {
            "gate_schema_version": vg.GATE_SIDECAR_SCHEMA_VERSION,
            "gate_eps_h": "Infinity",  # sentinel-encoded non-finite aggregate
            "gate_scs": "NaN",
            "gate_verdict": "FAIL",
            "gate_status": "ok",
            "gate_n_trajectories": 6,
            "gate_n_nonfinite": 1,
            "gate_sidecar": vg.sidecar_relative_path(20),
        }
        # allow_nan=False must not raise: sentinels are strings, not floats.
        self.append_record(
            path,
            step=20,
            final_val_loss=2.5,
            previous_val_loss=3.5,
            gate_fields=gate_fields,
        )
        record = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(record["step"], 20)
        self.assertEqual(record["final_val_loss"], 2.5)
        self.assertEqual(record["trend"], "improving")
        for key, value in gate_fields.items():
            self.assertEqual(record[key], value)

    def test_non_finite_final_val_loss_still_returns_early_without_appending(self) -> None:
        path = self.root / "validation.jsonl"
        returned = self.append_record(
            path,
            step=4,
            final_val_loss=float("nan"),
            previous_val_loss=None,
            gate_fields={"gate_status": "ok"},
        )
        self.assertNotEqual(returned, returned)  # NaN round-trips unchanged
        self.assertFalse(path.exists(), "pre-existing early-return contract broken")

    def test_seam_has_exactly_one_definition_and_one_call_inside_the_branch(self) -> None:
        train_path = Path(importlib.import_module("pinn.train").__file__)
        lines = executable_source(train_path).splitlines()
        defs = [i for i, ln in enumerate(lines) if ln.startswith("def _run_validation_gate_pass(")]
        calls = [
            i
            for i, ln in enumerate(lines)
            if "_run_validation_gate_pass(" in ln and not ln.startswith("def ")
        ]
        self.assertEqual(len(defs), 1, "expected exactly one seam definition")
        self.assertEqual(len(calls), 1, "expected exactly one seam call site (no second cadence)")
        # The single call must sit inside checkpoint_hook's EXISTING
        # validation-append branch: after its dedup condition, before the cell
        # is advanced. Comments are stripped, so they cannot fake either marker.
        opens = [i for i, ln in enumerate(lines)
                 if 'validation_state_cell["last_step"] != int(global_step)' in ln]
        closes = [i for i, ln in enumerate(lines)
                  if 'validation_state_cell["last_step"] = int(global_step)' in ln]
        self.assertEqual(len(opens), 1)
        self.assertEqual(len(closes), 1)
        self.assertLess(opens[0], calls[0])
        self.assertLess(calls[0], closes[0])


# ---------------------------------------------------------------------------
# Task 3 — the summary projection
# ---------------------------------------------------------------------------


_GATE_KEYS = (
    "gate_schema_version",
    "gate_eps_h",
    "gate_scs",
    "gate_verdict",
    "gate_status",
    "gate_n_trajectories",
    "gate_n_nonfinite",
    "gate_sidecar",
)


class SummaryGateProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="phase46-projection-")
        self.root = Path(self.tmp.name)
        (self.root / "config.yaml").write_text("run:\n  run_name: current\n")
        self.curriculum_path = self.root / "curriculum.jsonl"
        self.curriculum_path.write_text(
            json.dumps({"stage": 0, "phase": "2a", "step": 20}) + "\n", encoding="utf-8"
        )
        self.source = make_stub_split_sources()[1]
        self.append_record = _require("_append_validation_record")
        self.header = {
            "run_name": "current",
            "start_utc": "2026-07-28T00:00:00+00:00",
            "end_utc": "2026-07-28T00:05:00+00:00",
            "wall_clock_secs": 300.0,
            "device": "cpu",
            "precision": "fp64",
            "seed": 7,
        }
        self.losses = {
            "data": 1.0, "ic": 2.0, "phys": 3.0,
            "energy": 4.0, "angmom": 5.0, "total": 15.0,
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _publish_real_gate_record(self, step=32):
        """Produce a genuine sidecar + validation record via the real writers."""
        observation = vg.compute_validation_gate(
            StubModel(), self.source, stage=0, global_step=step,
            frame=vg.RATIFIED_VALIDATION_FRAME,
        )
        vg.publish_gate_sidecar(self.root, observation)
        fields = vg.compact_validation_fields(observation, self.root)
        path = self.root / "validation.jsonl"
        self.append_record(
            path, step=step, final_val_loss=2.5,
            previous_val_loss=3.5, gate_fields=fields,
        )
        return path, fields

    def _finalize(self, validation_path):
        summary_mod.finalize_summary(
            self.root,
            disposition="finished",
            header=self.header,
            final_losses=self.losses,
            curriculum_path=self.curriculum_path,
            validation_records_path=validation_path,
        )
        payload = json.loads((self.root / "summary.json").read_text(encoding="utf-8"))
        md = (self.root / "summary.md").read_text(encoding="utf-8")
        return payload["validation"], md

    def test_durable_valid_sidecar_projects_all_gate_keys_and_flags_eligible(self) -> None:
        path, fields = self._publish_real_gate_record()
        validation, md = self._finalize(path)
        for key in _GATE_KEYS:
            self.assertIn(key, validation)
            self.assertEqual(validation[key], fields[key])
        self.assertTrue(validation["eval01_precondition_iii"])
        self.assertIn("- eval01_precondition_iii: True", md)
        self.assertIn(f"- gate_sidecar: {fields['gate_sidecar']}", md)

    def test_missing_sidecar_keeps_persisted_fields_but_flags_ineligible(self) -> None:
        path, fields = self._publish_real_gate_record()
        (self.root / fields["gate_sidecar"]).unlink()
        validation, md = self._finalize(path)
        self.assertEqual(validation["gate_sidecar"], fields["gate_sidecar"])
        self.assertEqual(validation["gate_status"], "ok")
        self.assertFalse(validation["eval01_precondition_iii"])
        self.assertIn("- eval01_precondition_iii: False", md)

    def test_schema_invalid_sidecar_flags_ineligible(self) -> None:
        path, fields = self._publish_real_gate_record()
        sidecar = self.root / fields["gate_sidecar"]
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
        payload.pop("schema_version", None)  # durability alone is not enough
        sidecar.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        validation, _ = self._finalize(path)
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_failure_record_without_pointer_flags_ineligible_without_error(self) -> None:
        path = self.root / "validation.jsonl"
        self.append_record(
            path, step=12, final_val_loss=2.5, previous_val_loss=None,
            gate_fields={
                "gate_schema_version": vg.GATE_SIDECAR_SCHEMA_VERSION,
                "gate_status": "failed:ValidationGateUnavailable",
            },
        )
        validation, md = self._finalize(path)
        self.assertEqual(validation["gate_status"], "failed:ValidationGateUnavailable")
        self.assertIsNone(validation["gate_sidecar"])
        self.assertFalse(validation["eval01_precondition_iii"])
        self.assertIn("- gate_sidecar: null", md)

    def test_sentinel_metric_renders_verbatim_and_is_never_null_collapsed(self) -> None:
        path = self.root / "validation.jsonl"
        self.append_record(
            path, step=8, final_val_loss=2.5, previous_val_loss=None,
            gate_fields={
                "gate_schema_version": vg.GATE_SIDECAR_SCHEMA_VERSION,
                "gate_eps_h": "Infinity",
                "gate_scs": "-Infinity",
                "gate_verdict": "FAIL",
                "gate_status": "ok",
                "gate_n_trajectories": 6,
                "gate_n_nonfinite": 6,
                "gate_sidecar": vg.sidecar_relative_path(8),
            },
        )
        validation, md = self._finalize(path)
        self.assertEqual(validation["gate_eps_h"], "Infinity")
        self.assertEqual(validation["gate_scs"], "-Infinity")
        self.assertIn("- gate_eps_h: Infinity", md)
        self.assertIn("- gate_scs: -Infinity", md)
        # Sidecar was never published, so eligibility still fails closed.
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_legacy_record_without_gate_fields_stays_backward_compatible(self) -> None:
        path = self.root / "validation.jsonl"
        self.append_record(path, step=20, final_val_loss=2.5, previous_val_loss=3.5)
        validation, md = self._finalize(path)
        self.assertEqual(validation["final_val_loss"], 2.5)
        self.assertEqual(validation["trend"], "improving")
        self.assertEqual(validation["step"], 20)
        for key in _GATE_KEYS:
            self.assertIsNone(validation[key])
        self.assertFalse(validation["eval01_precondition_iii"])
        self.assertIn("- gate_verdict: null", md)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
