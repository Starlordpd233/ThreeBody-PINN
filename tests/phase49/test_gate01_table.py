"""GATE-01 table/preflight tests.

These tests intentionally use duck-typed schedulers for the table contract so
the assertion cannot accidentally depend on the scheduler's ramped ``current``
value.  The two entrypoint tests exercise the real composition root as well.
"""

from __future__ import annotations

import dataclasses
import importlib
import io
import math
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest
import torch
import yaml

from tests.phase41._fixtures import write_duration_gate_calibration


def _table_module():
    try:
        return importlib.import_module("pinn.conformance.table")
    except ImportError as exc:  # pragma: no cover - keeps early RED useful
        pytest.fail(f"GATE-01 conformance table is not available: {exc}")


def _preflight_module():
    try:
        return importlib.import_module("pinn.conformance.preflight")
    except ImportError as exc:  # pragma: no cover - keeps early RED useful
        pytest.fail(f"GATE-01 preflight is not available: {exc}")


def _state_for(stage: int = 0, *, lambda_ic: float = 1.0, **overrides):
    from pinn.constants import (
        PHYS05_LAMBDA_E_MAX,
        PHYS05_LAMBDA_L_MAX,
        PHYS05_LAMBDA_PHYS_MAX,
    )

    state = {
        "n_adam_k": 100,
        "warmup_length": 10,
        "lambda_phys_max": PHYS05_LAMBDA_PHYS_MAX[stage],
        "lambda_e_max": PHYS05_LAMBDA_E_MAX[stage],
        "lambda_l_max": PHYS05_LAMBDA_L_MAX[stage],
        "lambda_ic": lambda_ic,
    }
    state.update(overrides)
    return state


class _StateOnlyScheduler:
    def __init__(self, state):
        self._state = dict(state)
        self.current_called = False

    def state_dict(self):
        return dict(self._state)

    def current(self, _epoch):
        self.current_called = True
        return SimpleNamespace(
            lambda_data=1.0,
            lambda_ic=1.0,
            lambda_phys=0.0,
            lambda_e=0.0,
            lambda_l=0.0,
        )

    def rewarm(self):
        return None


def test_stage0_pass_reads_caps_from_state_dict_not_current():
    scheduler = _StateOnlyScheduler(_state_for())
    result = _table_module().assert_phys05_table(scheduler, 0)
    assert result["stage"] == 0
    assert result["checks"]
    assert all(check["passed"] for check in result["checks"] if check["tier"] == "locked")
    assert scheduler.current_called is False


def test_conformant_stage0_pass():
    result = _table_module().assert_phys05_table(
        _StateOnlyScheduler(_state_for(stage=0)), 0
    )
    assert result["stage"] == 0
    assert all(check["passed"] for check in result["checks"])


def test_missing_state_key_is_loud():
    state = _state_for()
    del state["lambda_e_max"]
    with pytest.raises(ValueError, match="lambda_e_max"):
        _table_module().assert_phys05_table(_StateOnlyScheduler(state), 0)


def test_none_scheduler_is_loud():
    with pytest.raises(ValueError, match="ScheduledWeights"):
        _table_module().assert_phys05_table(None, 0)


@pytest.mark.parametrize("stage", [-1, 7, 100])
def test_stage_outside_table_is_loud(stage):
    with pytest.raises(ValueError, match="stage"):
        _table_module().assert_phys05_table(_StateOnlyScheduler(_state_for()), stage)


def test_stage1_passes_with_stage0_caps():
    result = _table_module().assert_phys05_table(
        _StateOnlyScheduler(_state_for(stage=1)), 1
    )
    assert all(check["passed"] for check in result["checks"] if check["tier"] == "locked")


def test_stage2_fails_without_rebound_scheduler():
    scheduler = _StateOnlyScheduler(_state_for(stage=0))
    with pytest.raises(ValueError) as exc:
        _table_module().assert_phys05_table(scheduler, 2)
    message = str(exc.value)
    assert "lambda_e_max" in message
    assert "expected 0.01" in message
    assert "actual 0.0" in message


def test_lambda_ic_mismatch_is_advisory_and_reported():
    result = _table_module().assert_phys05_table(
        _StateOnlyScheduler(_state_for(lambda_ic=math.nextafter(1.0, 2.0))), 0
    )
    tiers = {check["tier"] for check in result["checks"]}
    assert tiers == {"locked", "advisory"}
    advisory = [check for check in result["checks"] if check["tier"] == "advisory"]
    assert len(advisory) == 1
    assert advisory[0]["name"] == "lambda_ic"
    assert advisory[0]["passed"] is False


def test_warmup_formula_trip():
    state = _state_for(n_adam_k=100, warmup_length=11)
    with pytest.raises(ValueError, match="warmup_length"):
        _table_module().assert_phys05_table(_StateOnlyScheduler(state), 0)


def test_one_ulp_cap_trip():
    state = _state_for(lambda_e_max=math.nextafter(0.0, 1.0))
    with pytest.raises(ValueError, match="lambda_e_max"):
        _table_module().assert_phys05_table(_StateOnlyScheduler(state), 0)


def test_formula_literals_are_exact_for_k_2_3_4():
    from pinn.constants import PHYS05_LAMBDA_E_MAX, PHYS05_LAMBDA_L_MAX

    for stage in (2, 3, 4):
        assert PHYS05_LAMBDA_E_MAX[stage] == 10.0 ** (stage - 4)
        assert PHYS05_LAMBDA_L_MAX[stage] == 10.0 ** (stage - 4)


def test_lambda_data_default_and_emission_path_are_locked():
    from pinn.constants import PHYS05_LAMBDA_DATA
    from pinn.loss_catalog import LossWeights
    from pinn.training.scheduled_weights import ScheduledWeights

    field = next(field for field in dataclasses.fields(LossWeights) if field.name == "lambda_data")
    assert field.default == PHYS05_LAMBDA_DATA
    assert ScheduledWeights(10).current(0).lambda_data == PHYS05_LAMBDA_DATA
    with pytest.raises(ValueError, match="lambda_data"):
        LossWeights(lambda_data=math.nextafter(1.0, 2.0))


def test_lambda_data_trip_uses_side_effect_free_field_default(monkeypatch):
    from pinn.constants import PHYS05_LAMBDA_DATA

    @dataclasses.dataclass(frozen=True)
    class WrongLossWeights:
        lambda_data: float = math.nextafter(PHYS05_LAMBDA_DATA, 2.0)

    module = _table_module()
    monkeypatch.setattr(module, "LossWeights", WrongLossWeights)
    with pytest.raises(ValueError, match="lambda_data"):
        module.assert_phys05_table(_StateOnlyScheduler(_state_for()), 0)


class _ControllerStore:
    def save(self, _payload):
        return None

    def save_anchor(self, **_kwargs):
        return None

    def promote(self, _old, _new):
        return None

    def record_disposition(self, *_args):
        return None


def _forced_controller(*, scheduler, hook=None, forced=None):
    from pinn.training.controllers import CurriculumController, StageDisposition

    return CurriculumController(
        config=SimpleNamespace(provisional_fields=lambda: []),
        checkpoint_store=_ControllerStore(),
        scheduled_weights=scheduler,
        forced_disposition=forced or (lambda _stage: StageDisposition.ADVANCE),
        conformance_hook=hook,
    )


def test_controller_stage2_fails_at_post_advance_site_without_factory():
    from pinn.training.controllers import StageDisposition

    scheduler = _StateOnlyScheduler(_state_for(stage=0))
    controller = _forced_controller(
        scheduler=scheduler,
        hook=lambda stage, current: _table_module().assert_phys05_table(current, stage),
        forced=lambda _stage: StageDisposition.ADVANCE,
    )
    controller.step()  # Stage 0 -> 1, both rows are locked at zero energy cap.
    with pytest.raises(ValueError, match="lambda_e_max") as exc:
        controller.step()  # Stage 1 -> 2, the un-rebound scheduler is refused.
    assert "expected 0.01" in str(exc.value)
    assert "actual 0.0" in str(exc.value)


def test_controller_stage_boundary_events_follow_entered_order(tmp_path):
    from pinn.training.controllers import StageDisposition

    preflight = _preflight_module()
    scheduler = _StateOnlyScheduler(_state_for(stage=0))
    recorder = preflight.PreflightRecorder(tmp_path)
    recorder.append_event(
        event="run_start", stage=0, status="passed", checks=[
            {"name": "phys05_table", "tier": "locked", "expected": "ok", "actual": "ok", "passed": True}
        ]
    )

    def hook(stage, current):
        if getattr(hook, "last_stage", None) == stage:
            return
        result = _table_module().assert_phys05_table(current, stage)
        recorder.append_event(
            event="stage_boundary", stage=stage, status="passed", checks=result["checks"]
        )
        hook.last_stage = stage

    controller = _forced_controller(
        scheduler=scheduler,
        hook=hook,
        forced=lambda stage: StageDisposition.HALT if stage == 1 else StageDisposition.ADVANCE,
    )
    controller.run()
    payload = preflight.load_preflight(tmp_path)
    assert [(event["event"], event["stage"]) for event in payload["assertions"]] == [
        ("run_start", 0),
        ("stage_boundary", 0),
        ("stage_boundary", 1),
    ]


def test_preflight_serialization_is_deterministic(tmp_path):
    preflight = _preflight_module()
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first = preflight.PreflightRecorder(first_dir)
    second = preflight.PreflightRecorder(second_dir)
    checks = [{"name": "lambda_phys_max", "tier": "locked", "expected": 1.0, "actual": 1.0, "passed": True}]
    for recorder in (first, second):
        recorder.append_event(event="run_start", stage=0, status="passed", checks=checks)
    assert (first_dir / preflight.PREFLIGHT_FILENAME).read_bytes() == (
        second_dir / preflight.PREFLIGHT_FILENAME
    ).read_bytes()
    loaded = preflight.load_preflight(first_dir)
    assert loaded["schema_version"] == preflight.PREFLIGHT_SCHEMA_VERSION


def _write_config(path: Path, run_name: str) -> Path:
    doc = {
        "run": {
            "seed": 11,
            "precision": "float64",
            "device": "cpu",
            "strict_cpu_determinism": False,
            "log_every": 1,
            "run_name": run_name,
            "checkpoint": {
                "every_n_steps": 1,
                "wall_clock_ceiling_s": 3600.0,
                "rolling_keep": 5,
                "failure_keep": 10,
            },
            "guards": {
                "loss_explosion_ceiling": 1.0e12,
                "disk_floor_fraction": 0.01,
                "memory_watermark_fraction": 0.99,
            },
        },
        "stage": {
            "max_epochs": 2,
            "n_adam": 2,
            "stagnation_window": 10_000,
            "percentile_10_relaxation": 0.1,
            "beta": 0.9,
            "patience": 50,
            "eps_plateau": 1e-5,
            "eps_phys": 1e-4,
            "eps_energy": 1e-4,
        },
        "opt": {"validation_every": 1, "lbfgs_max_iter": 2, "lbfgs_chunk_size": 4},
        "loss": {"lambda_e_max": 0.0},
    }
    path.write_text(yaml.safe_dump(doc, sort_keys=True), encoding="utf-8")
    return path


class _EntrypointHarness(unittest.TestCase):
    def setUp(self):
        self.train = importlib.import_module("pinn.train")
        self.tmp = Path(tempfile.mkdtemp(prefix="phase49-gate01-"))
        self.runs = self.tmp / "runs"
        self.runs.mkdir()
        write_duration_gate_calibration(self.runs)
        self.config = _write_config(self.tmp / "config.yaml", "gate-run")
        self.old_root = self.train._RUNS_ROOT
        self.train._RUNS_ROOT = self.runs

    def tearDown(self):
        self.train._RUNS_ROOT = self.old_root
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.train.main(["--config", str(self.config)])
        return code, out.getvalue(), err.getvalue()


class EntrypointTests(_EntrypointHarness):
    def test_run_start_writes_passed_preflight_artifact(self):
        code, out, err = self._run()
        assert code == 0, f"stdout={out}\nstderr={err}"
        artifact = self.runs / "gate-run" / "preflight.json"
        assert artifact.is_file()
        payload = _preflight_module().load_preflight(self.runs / "gate-run")
        assert payload["assertions"][0]["event"] == "run_start"
        assert payload["assertions"][0]["status"] == "passed"

    def test_tamper_writes_failed_artifact_before_nonzero_exit(self):
        real_scheduler = self.train.ScheduledWeights

        class TamperedScheduler(real_scheduler):
            def state_dict(self):
                state = super().state_dict()
                state["lambda_e_max"] = 1.0
                return state

        with mock.patch.object(self.train, "ScheduledWeights", TamperedScheduler):
            code, _out, err = self._run()
        assert code != 0
        artifact = self.runs / "gate-run" / "preflight.json"
        assert artifact.is_file()
        payload = _preflight_module().load_preflight(self.runs / "gate-run")
        assert payload["preflight_status"] == "failed"
        assert payload["assertions"][0]["status"] == "failed"
        assert "lambda_e_max" in err
