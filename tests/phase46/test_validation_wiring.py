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


class _MpsRuntimeSpec:
    """Production-path runtime: locked Phase-50 float32 / MPS."""

    dtype = torch.float32
    torch_device = torch.device("mps")


class _MpsFloat32Model:
    """Callable stub that emits an actual MPS float32 prediction."""

    def __init__(self):
        self.training = True
        self.calls = []

    def eval(self):
        self.training = False
        return self

    def train(self, mode=True):
        self.training = bool(mode)
        return self

    def __call__(self, tau_ic13, masses):
        n = int(tau_ic13.shape[0])
        self.calls.append((tuple(tau_ic13.shape), tuple(masses.shape)))
        return torch.zeros((n, 9), dtype=torch.float32, device=torch.device("mps"))


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

    def test_non_finite_final_val_loss_is_persisted_not_dropped(self) -> None:
        # CR-05 closure: a non-finite validation loss must still leave exactly
        # one JSON-safe line -- the OLD contract (early return, no append) is
        # precisely the bug that let a later invalid event hide behind an
        # older eligible record.
        path = self.root / "validation.jsonl"
        returned = self.append_record(
            path,
            step=4,
            final_val_loss=float("nan"),
            previous_val_loss=None,
            gate_fields={"gate_status": "ok"},
        )
        self.assertNotEqual(returned, returned)  # NaN round-trips unchanged
        self.assertTrue(path.exists(), "a non-finite validation event must still be appended (CR-05)")
        record = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(record["step"], 4)
        self.assertEqual(record["final_val_loss"], "NaN")
        self.assertEqual(record["trend"], "unavailable")
        self.assertEqual(record["gate_status"], "ok")

    def test_positive_and_negative_infinite_val_loss_persist_as_sentinels(self) -> None:
        path = self.root / "validation.jsonl"
        self.append_record(path, step=5, final_val_loss=float("inf"), previous_val_loss=None)
        self.append_record(path, step=6, final_val_loss=float("-inf"), previous_val_loss=None)
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(json.loads(lines[0])["final_val_loss"], "Infinity")
        self.assertEqual(json.loads(lines[1])["final_val_loss"], "-Infinity")

    def test_trend_is_unavailable_whenever_current_or_previous_loss_is_nonfinite(self) -> None:
        path = self.root / "validation.jsonl"
        self.append_record(path, step=1, final_val_loss=2.0, previous_val_loss=None)
        self.append_record(path, step=2, final_val_loss=float("nan"), previous_val_loss=2.0)
        self.append_record(path, step=3, final_val_loss=3.0, previous_val_loss=float("nan"))
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["trend"] for r in records], ["unavailable"] * 3)

    def test_hostile_step_rejected_before_any_write(self) -> None:
        path = self.root / "validation.jsonl"
        for hostile in (True, False, 1.9, "1", -1):
            with self.subTest(step=hostile):
                with self.assertRaises(ValueError):
                    self.append_record(
                        path, step=hostile, final_val_loss=1.0, previous_val_loss=None
                    )
        self.assertFalse(path.exists(), "a hostile step must not create the file (WR-01)")

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


class MpsProductionWiringTests(unittest.TestCase):
    """Production MPS path must publish a healthy sidecar (50-06 Task 1)."""

    def setUp(self) -> None:
        if not torch.backends.mps.is_available():
            raise AssertionError("canonical MPS host required")
        self.tmp = tempfile.TemporaryDirectory(prefix="phase50-mps-wiring-")
        self.root = Path(self.tmp.name)
        self.source = make_stub_split_sources()[1]
        self.run_gate_pass = _require("_run_validation_gate_pass")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_production_mps_path_publishes_and_revalidates_sidecar(self) -> None:
        model = _MpsFloat32Model()
        model.train()
        fields = self.run_gate_pass(
            model,
            self.source,
            stage=0,
            global_step=100,
            run_dir=self.root,
            runtime_spec=_MpsRuntimeSpec(),
        )
        self.assertTrue(model.training)
        self.assertEqual(fields["gate_status"], "ok")
        self.assertFalse(
            str(fields["gate_status"]).startswith("failed:"),
            f"failed:TypeError is not healthy evidence: {fields}",
        )
        self.assertEqual(fields["gate_schema_version"], vg.GATE_SIDECAR_SCHEMA_VERSION)
        rel = fields["gate_sidecar"]
        self.assertEqual(rel, vg.sidecar_relative_path(100))
        sidecar = self.root / rel
        self.assertTrue(sidecar.is_file(), "pointer returned without a durable sidecar")
        vg.validate_sidecar_payload(json.loads(sidecar.read_text(encoding="utf-8")))
        for key in ("gate_eps_h", "gate_scs", "gate_verdict", "gate_n_trajectories"):
            self.assertIn(key, fields)


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

    def test_missing_and_empty_stream_retain_none_projection(self) -> None:
        summary_mod.finalize_summary(
            self.root, disposition="finished", header=self.header,
            final_losses=self.losses, curriculum_path=self.curriculum_path,
            validation_records_path=self.root / "does-not-exist.jsonl",
        )
        payload = json.loads((self.root / "summary.json").read_text(encoding="utf-8"))
        self.assertIsNone(payload["validation"])

        empty_path = self.root / "validation.jsonl"
        empty_path.write_text("", encoding="utf-8")
        summary_mod.finalize_summary(
            self.root, disposition="finished", header=self.header,
            final_losses=self.losses, curriculum_path=self.curriculum_path,
            validation_records_path=empty_path,
        )
        payload = json.loads((self.root / "summary.json").read_text(encoding="utf-8"))
        self.assertIsNone(payload["validation"])


# ---------------------------------------------------------------------------
# CR-05 closure: latest-event failure is monotonic -- never falls back
# ---------------------------------------------------------------------------


class LatestEventMonotonicityTests(unittest.TestCase):
    """A later invalid (failed / nonfinite / malformed / non-mapping) event
    is ALWAYS the reported latest and ALWAYS ineligible; an older eligible
    record is never exposed as current (CR-05, AC-46-10-06/07)."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="phase46-monotonic-")
        self.root = Path(self.tmp.name)
        (self.root / "config.yaml").write_text("run:\n  run_name: current\n")
        self.curriculum_path = self.root / "curriculum.jsonl"
        self.source = make_stub_split_sources()[1]
        self.append_record = _require("_append_validation_record")
        self.header = {
            "run_name": "current", "start_utc": "2026-07-28T00:00:00+00:00",
            "end_utc": "2026-07-28T00:05:00+00:00", "wall_clock_secs": 300.0,
            "device": "cpu", "precision": "fp64", "seed": 7,
        }
        self.losses = {
            "data": 1.0, "ic": 2.0, "phys": 3.0,
            "energy": 4.0, "angmom": 5.0, "total": 15.0,
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _publish_real_gate_record(self, step):
        observation = vg.compute_validation_gate(
            StubModel(), self.source, stage=0, global_step=step,
            frame=vg.RATIFIED_VALIDATION_FRAME,
        )
        vg.publish_gate_sidecar(self.root, observation)
        fields = vg.compact_validation_fields(observation, self.root)
        path = self.root / "validation.jsonl"
        self.append_record(
            path, step=step, final_val_loss=2.5, previous_val_loss=None, gate_fields=fields,
        )
        return path, fields

    def _finalize(self, validation_path):
        summary_mod.finalize_summary(
            self.root, disposition="finished", header=self.header,
            final_losses=self.losses, curriculum_path=self.curriculum_path,
            validation_records_path=validation_path,
        )
        payload = json.loads((self.root / "summary.json").read_text(encoding="utf-8"))
        return payload["validation"]

    def test_valid_event_followed_by_failed_gate_event_stays_ineligible_at_latest(self) -> None:
        path, _ = self._publish_real_gate_record(step=7)
        self.append_record(
            path, step=8, final_val_loss=float("nan"), previous_val_loss=2.5,
            gate_fields={
                "gate_schema_version": vg.GATE_SIDECAR_SCHEMA_VERSION,
                "gate_status": "failed:ValidationGateUnavailable",
            },
        )
        validation = self._finalize(path)
        self.assertEqual(validation["step"], 8, "the LATEST event must be reported, not step 7")
        self.assertEqual(validation["gate_status"], "failed:ValidationGateUnavailable")
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_valid_event_followed_by_nonfinite_loss_ok_gate_event_is_ineligible(self) -> None:
        # A genuinely valid, fully-recomputable gate record at the LATEST
        # step whose final_val_loss just happens to be nonfinite: eligibility
        # must still fail, since a finite loss is jointly necessary
        # (AC-46-10-08) even though the gate itself is otherwise perfect.
        path, _ = self._publish_real_gate_record(step=9)
        observation = vg.compute_validation_gate(
            StubModel(), self.source, stage=0, global_step=10,
            frame=vg.RATIFIED_VALIDATION_FRAME,
        )
        vg.publish_gate_sidecar(self.root, observation)
        fields = vg.compact_validation_fields(observation, self.root)
        self.append_record(
            path, step=10, final_val_loss=float("nan"), previous_val_loss=2.5,
            gate_fields=fields,
        )
        validation = self._finalize(path)
        self.assertEqual(validation["step"], 10)
        self.assertEqual(validation["gate_status"], "ok")
        self.assertIsNone(validation["final_val_loss"])
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_valid_event_followed_by_torn_line_never_falls_back(self) -> None:
        path, _ = self._publish_real_gate_record(step=7)
        with path.open("a", encoding="utf-8") as handle:
            handle.write('{"step": 8, "final_val_loss": 1.0, "trend": "impro')
        validation = self._finalize(path)
        self.assertIsNone(validation["step"])
        self.assertIsNone(validation["final_val_loss"])
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_valid_event_followed_by_non_mapping_line_never_falls_back(self) -> None:
        path, _ = self._publish_real_gate_record(step=7)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps([1, 2, 3]) + "\n")
        validation = self._finalize(path)
        self.assertIsNone(validation["step"])
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_valid_event_followed_by_blank_only_line_never_falls_back(self) -> None:
        path, _ = self._publish_real_gate_record(step=7)
        with path.open("a", encoding="utf-8") as handle:
            handle.write("   \n")
        validation = self._finalize(path)
        self.assertIsNone(validation["step"])
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_valid_event_followed_by_undecodable_bytes_never_falls_back(self) -> None:
        # A torn write can land invalid UTF-8 at the tail. UnicodeDecodeError
        # is a ValueError, not an OSError, so an OSError-only guard lets it
        # escape finalize_summary and finish_run's bare try/finally -- no
        # summary at all, defeating presence-under-every-death-mode.
        path, _ = self._publish_real_gate_record(step=7)
        with path.open("ab") as handle:
            handle.write(b'{"step": 8, "final_val_loss": \xff\xfe}\n')
        validation = self._finalize(path)
        self.assertIsNone(validation["step"])
        self.assertIsNone(validation["final_val_loss"])
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_adjacent_step_events_are_distinct_and_latest_is_reported_eligible(self) -> None:
        path, fields7 = self._publish_real_gate_record(step=7)
        _, fields8 = self._publish_real_gate_record(step=8)
        self.assertNotEqual(fields7["gate_sidecar"], fields8["gate_sidecar"])
        validation = self._finalize(path)
        self.assertEqual(validation["step"], 8)
        self.assertEqual(validation["gate_sidecar"], fields8["gate_sidecar"])
        self.assertTrue(validation["eval01_precondition_iii"])


# ---------------------------------------------------------------------------
# CR-03 closure: cross-run / wrong-step / forged-pointer identity binding
# ---------------------------------------------------------------------------


class Eval01IdentityBindingTests(unittest.TestCase):
    """The record must bind to its OWN exact same-run, same-step sidecar with
    exactly matching compact fields (CR-03, AC-46-10-03/08)."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="phase46-identity-")
        self.root = Path(self.tmp.name)
        (self.root / "config.yaml").write_text("run:\n  run_name: current\n")
        self.curriculum_path = self.root / "curriculum.jsonl"
        self.source = make_stub_split_sources()[1]
        self.append_record = _require("_append_validation_record")
        self.header = {
            "run_name": "current", "start_utc": "2026-07-28T00:00:00+00:00",
            "end_utc": "2026-07-28T00:05:00+00:00", "wall_clock_secs": 300.0,
            "device": "cpu", "precision": "fp64", "seed": 7,
        }
        self.losses = {
            "data": 1.0, "ic": 2.0, "phys": 3.0,
            "energy": 4.0, "angmom": 5.0, "total": 15.0,
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _publish_real_gate_record(self, step):
        observation = vg.compute_validation_gate(
            StubModel(), self.source, stage=0, global_step=step,
            frame=vg.RATIFIED_VALIDATION_FRAME,
        )
        vg.publish_gate_sidecar(self.root, observation)
        fields = vg.compact_validation_fields(observation, self.root)
        path = self.root / "validation.jsonl"
        self.append_record(
            path, step=step, final_val_loss=2.5, previous_val_loss=None, gate_fields=fields,
        )
        return path, fields

    def _finalize(self, validation_path):
        summary_mod.finalize_summary(
            self.root, disposition="finished", header=self.header,
            final_losses=self.losses, curriculum_path=self.curriculum_path,
            validation_records_path=validation_path,
        )
        payload = json.loads((self.root / "summary.json").read_text(encoding="utf-8"))
        return payload["validation"]

    def _overwrite_latest_record(self, path, record):
        lines = path.read_text(encoding="utf-8").splitlines()
        lines[-1] = json.dumps(record, sort_keys=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_cross_run_traversal_pointer_rejected(self) -> None:
        path, _ = self._publish_real_gate_record(step=7)
        record = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
        record["gate_sidecar"] = "../donor/validation_gate/step-00000007.json"
        self._overwrite_latest_record(path, record)
        validation = self._finalize(path)
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_wrong_step_pointer_with_renamed_donor_sidecar_rejected(self) -> None:
        path, fields = self._publish_real_gate_record(step=7)
        donor_rel = fields["gate_sidecar"]
        forged_rel = vg.sidecar_relative_path(999)
        (self.root / forged_rel).parent.mkdir(parents=True, exist_ok=True)
        (self.root / forged_rel).write_bytes((self.root / donor_rel).read_bytes())
        forged_fields = dict(fields)
        forged_fields["gate_sidecar"] = forged_rel
        self.append_record(
            path, step=999, final_val_loss=1.0, previous_val_loss=None,
            gate_fields=forged_fields,
        )
        validation = self._finalize(path)
        self.assertEqual(validation["step"], 999)
        self.assertFalse(validation["eval01_precondition_iii"])

    def test_one_at_a_time_gate_field_mismatch_rejected(self) -> None:
        mutations = {
            "gate_schema_version": lambda v: v + "-tampered",
            "gate_eps_h": lambda v: (v + 1.0) if isinstance(v, float) else v + "-tampered",
            "gate_scs": lambda v: (v + 1.0) if isinstance(v, float) else v + "-tampered",
            "gate_verdict": lambda v: ("FAIL" if v == "PASS" else "PASS"),
            "gate_status": lambda v: "tampered",
            "gate_n_trajectories": lambda v: v + 1,
            "gate_n_nonfinite": lambda v: v + 1,
            "gate_sidecar": lambda v: v + ".tampered",
        }
        self.assertEqual(sorted(mutations), sorted(_GATE_KEYS))
        for key, mutate in mutations.items():
            with self.subTest(key=key):
                tmp = tempfile.TemporaryDirectory(prefix="phase46-onemismatch-")
                self.addCleanup(tmp.cleanup)
                root = Path(tmp.name)
                (root / "config.yaml").write_text("run:\n  run_name: current\n")
                observation = vg.compute_validation_gate(
                    StubModel(), self.source, stage=0, global_step=15,
                    frame=vg.RATIFIED_VALIDATION_FRAME,
                )
                vg.publish_gate_sidecar(root, observation)
                fields = vg.compact_validation_fields(observation, root)
                path = root / "validation.jsonl"
                self.append_record(
                    path, step=15, final_val_loss=2.5, previous_val_loss=None,
                    gate_fields=fields,
                )
                record = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
                record[key] = mutate(record[key])
                path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")
                summary_mod.finalize_summary(
                    root, disposition="finished", header=self.header,
                    final_losses=self.losses, curriculum_path=self.curriculum_path,
                    validation_records_path=path,
                )
                payload = json.loads((root / "summary.json").read_text(encoding="utf-8"))
                self.assertFalse(
                    payload["validation"]["eval01_precondition_iii"],
                    f"mutating {key!r} alone must break eligibility",
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
