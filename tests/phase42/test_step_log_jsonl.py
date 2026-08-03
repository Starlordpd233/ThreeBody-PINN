"""Phase 42 / Plan 04 — canonical JSONL step log + human mirror (OPS-03 / E1).

Covers:
- OPS-03 happy path: every canonical widened field key present in the JSONL
  object, the human §5.4 mirror line written, and the registry-vs-JSONL
  parity assertion (no residuals_bin_* leakage, cycle-2 HIGH-1).
- E1 non-finite coverage: ``json.loads`` EVERY line of a multi-step run that
  includes a diverged step; the diverged line carries ``finite:false`` with
  ``nonfinite_keys`` naming the affected fields, and no string sentinel
  (``"NaN"``/``"Inf"``/``"-Inf"``) appears anywhere.
- Both Adam (phase 2a) and L-BFGS (phase 2b) widened records are parity-checked.
"""

from __future__ import annotations

import importlib
import json
import logging
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.phase42 import _SKIP_PHRASE

STEP_LOG_MODULE = "pinn.training.step_log"


def _require(symbol, module=STEP_LOG_MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _canonical_step_record(
    step: int,
    phase: str,
    stage: int = 0,
    **overrides,
) -> dict:
    """Build a canonical widened step-record dict (mirrors ``_log_step`` extra=)."""
    rec = {
        "event": "step",
        "step": step,
        "stage": stage,
        "phase": phase,
        "epoch": 0,
        "total": 1.5,
        "loss_data": 0.5,
        "loss_ic": 0.3,
        "loss_phys": 0.2,
        "loss_energy": 0.1,
        "loss_angmom": 0.05,
        "lambda_data": 1.0,
        "lambda_ic": 1.0,
        "lambda_phys": 1.0,
        "lambda_e": 1.0,
        "lambda_l": 1.0,
        "grad_norm": 0.01,
        "grad_norm_raw_data": 0.11,
        "grad_norm_raw_ic": 0.12,
        "grad_norm_raw_phys": 0.13,
        "grad_norm_raw_energy": 0.14,
        "grad_norm_raw_angmom": 0.15,
        "grad_norm_applied_data": 0.11,
        "grad_norm_applied_ic": 0.12,
        "grad_norm_applied_phys": 0.13,
        "grad_norm_applied_energy": 0.14,
        "grad_norm_applied_angmom": 0.15,
        "grad_stats_provenance": "pre_total_backward",
        "grad_stats_complete": True,
        "w_min": 0.2,
        "w_mean": 0.5,
        "w_max": 0.9,
        "front_idx": 2,
        "lr": 1e-3,
        "s_per_step": 0.5,
        "eta_seconds": 300.0,
        "step_completed": True,
    }
    rec.update(overrides)
    return rec


class JsonlStepLogTests(unittest.TestCase):
    """OPS-03 happy-path + E1 non-finite coverage for the step-log sinks."""

    def setUp(self):
        self.JsonlStepHandler = _require("JsonlStepHandler")
        self.HumanStepHandler = _require("HumanStepHandler")
        self.STEP_LOG_FIELDS = _require("STEP_LOG_FIELDS")
        self._sanitize_step_record = _require("_sanitize_step_record")

        self.tmp = Path(tempfile.mkdtemp(prefix="phase42-jsonl-"))
        self.jsonl_path = self.tmp / "train.log.jsonl"
        self.human_path = self.tmp / "train.log"

        self.logger = logging.getLogger("pinn.training.test_step_log_jsonl")
        self.logger.setLevel(logging.INFO)

        self.jsonl_handler = self.JsonlStepHandler(self.jsonl_path)
        self.human_handler = self.HumanStepHandler(self.human_path)
        self.logger.addHandler(self.jsonl_handler)
        self.logger.addHandler(self.human_handler)

    def tearDown(self):
        self.logger.removeHandler(self.jsonl_handler)
        self.logger.removeHandler(self.human_handler)
        self.jsonl_handler.close()
        self.human_handler.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _emit(self, record_dict):
        self.logger.info("step", extra=record_dict)

    def test_ops03_happy_path_field_presence(self):
        """OPS-03: canonical widened fields present in JSONL + human mirror line."""
        # Adam (phase 2a) record, with residuals_bin_* TB-only fields included
        # in the widened record to assert they are FILTERED OUT of JSONL.
        rec_2a = _canonical_step_record(
            step=5,
            phase="2a",
            residuals_bin_00=0.11,
            residuals_bin_01=0.22,
        )
        self._emit(rec_2a)

        # L-BFGS (phase 2b) full widened record.
        rec_2b = _canonical_step_record(
            step=6,
            phase="2b",
            residuals_bin_00=0.33,
        )
        self._emit(rec_2b)

        self.jsonl_handler.flush()
        self.human_handler.flush()

        # JSONL: every line parses; ≥2 objects.
        jsonl_lines = self.jsonl_path.read_text(encoding="utf-8").splitlines()
        self.assertGreaterEqual(len(jsonl_lines), 2)
        objs = [json.loads(line) for line in jsonl_lines]

        # Canonical widened field presence (5 loss_* terms, total, lambda_*
        # components, grad_norm, w_n stats, lr, s_per_step, eta_seconds,
        # step, stage).
        required_keys = {
            "loss_data", "loss_ic", "loss_phys", "loss_energy", "loss_angmom",
            "total",
            "lambda_e", "lambda_l", "lambda_data", "lambda_ic", "lambda_phys",
            "grad_norm",
            "w_min", "w_mean", "w_max",
            "lr", "s_per_step", "eta_seconds",
            "step", "stage",
        }
        for obj in objs:
            missing = required_keys - set(obj)
            self.assertEqual(
                missing, set(),
                f"missing canonical keys in step {obj.get('step')}: {missing}",
            )

        # Human mirror: §5.4 pipe-delimited line present for each step.
        human_lines = self.human_path.read_text(encoding="utf-8").splitlines()
        self.assertGreaterEqual(len(human_lines), 2)
        self.assertTrue(
            any("step 5" in line and "phase 2a" in line for line in human_lines),
            f"no human 2a line found; lines={human_lines}",
        )
        self.assertTrue(
            any("step 6" in line and "phase 2b" in line for line in human_lines),
            f"no human 2b line found; lines={human_lines}",
        )

    def test_ops03_registry_parity_and_no_residuals_leak(self):
        """OPS-03 / cycle-2 HIGH-1: registry-vs-JSONL parity + residuals excluded."""
        rec = _canonical_step_record(
            step=7,
            phase="2a",
            # Include TB-only residuals to assert they are filtered out.
            residuals_bin_00=0.11,
            residuals_bin_01=0.22,
            residuals_bin_09=0.99,
        )
        self._emit(rec)
        self.jsonl_handler.flush()

        obj = json.loads(self.jsonl_path.read_text().splitlines()[-1])

        # Parity assertion (review finding #6): every key is in STEP_LOG_FIELDS
        # EXCEPT the two sink-added keys finite / nonfinite_keys.
        extra_keys = set(obj) - {"finite", "nonfinite_keys"}
        self.assertTrue(
            extra_keys <= set(self.STEP_LOG_FIELDS),
            f"keys outside STEP_LOG_FIELDS: {extra_keys - set(self.STEP_LOG_FIELDS)}",
        )

        # cycle-2 review finding HIGH-1: residuals_bin_* MUST NOT leak into
        # the canonical JSONL (TB-only, OPS-04b). No carve-out needed because
        # the handler filters to the OPS-03 set.
        leaked = [k for k in obj if k.startswith("residuals_bin_")]
        self.assertEqual(
            leaked, [],
            f"residuals_bin_* leaked into canonical JSONL: {leaked}",
        )

    def test_e1_nonfinite_whole_file_parseability(self):
        """E1: json.loads EVERY line; diverged line has finite:false + nonfinite_keys;
        no string sentinels anywhere."""
        # Finite step followed by a diverged step.
        self._emit(_canonical_step_record(step=10, phase="2a"))
        self._emit(_canonical_step_record(
            step=11,
            phase="2a",
            total=float("nan"),
            loss_phys=float("inf"),
            loss_energy=float("nan"),
        ))
        self.jsonl_handler.flush()

        lines = self.jsonl_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2, "expected exactly 2 emitted steps")

        # Coverage: json.loads EVERY line (not just the last).
        objs = [json.loads(line) for line in lines]

        # The diverged (last) line.
        diverged = objs[-1]
        self.assertIs(
            diverged["finite"], False,
            f"diverged line should have finite:false, got {diverged.get('finite')}",
        )
        self.assertIn("nonfinite_keys", diverged)
        self.assertIsInstance(diverged["nonfinite_keys"], list)
        self.assertGreater(
            len(diverged["nonfinite_keys"]), 0,
            "nonfinite_keys should name the affected fields",
        )
        # The affected fields are exactly the non-finite ones.
        self.assertEqual(
            set(diverged["nonfinite_keys"]),
            {"total", "loss_phys", "loss_energy"},
            f"unexpected nonfinite_keys: {diverged['nonfinite_keys']}",
        )
        # Non-finite fields serialize as JSON null (not string sentinels).
        for key in diverged["nonfinite_keys"]:
            self.assertIsNone(
                diverged[key],
                f"non-finite field {key} should be JSON null, got {diverged[key]!r}",
            )

        # No string sentinels anywhere in either line.  Skip non-hashable
        # values (the sink-added ``nonfinite_keys`` list) when probing the
        # sentinel set.
        string_sentinels = {"NaN", "Inf", "-Inf", "nan", "inf", "-inf"}
        for obj in objs:
            for k, v in obj.items():
                try:
                    hash(v)
                except TypeError:
                    continue
                self.assertNotIn(
                    v, string_sentinels,
                    f"string sentinel {v!r} at key {k!r} in step {obj.get('step')}",
                )

    def test_last_step_finite_attribute(self):
        """last_step_finite is None initially, updated to finite value on emit."""
        self.assertIsNone(self.jsonl_handler.last_step_finite)
        self._emit(_canonical_step_record(step=1, phase="2a"))
        self.jsonl_handler.flush()
        self.assertIs(self.jsonl_handler.last_step_finite, True)

        self._emit(_canonical_step_record(
            step=2, phase="2a", total=float("nan"),
        ))
        self.jsonl_handler.flush()
        self.assertIs(self.jsonl_handler.last_step_finite, False)


if __name__ == "__main__":
    unittest.main()
