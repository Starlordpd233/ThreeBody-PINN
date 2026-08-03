"""Stage-0 energy-cap conformance tests for Phase 48 Plan 02."""

from __future__ import annotations

from pathlib import Path

import pytest

from pinn.training.config import LossConfig
from pinn.training.config_yaml import load_config
from pinn.training.scheduled_weights import ScheduledWeights


_REPO_ROOT = Path(__file__).resolve().parents[2]


def test_loss_config_default_drives_stage0_zero_schedule():
    """The omitted cap reaches the real scheduler path as exact zero."""
    config = LossConfig()
    assert config.lambda_e_max == 0.0

    schedule = ScheduledWeights(
        n_adam_k=500,
        lambda_e_max=float(config.lambda_e_max),
    )
    for epoch in (0, 25, 50, 1000):
        assert float(schedule.current(epoch).lambda_e) == 0.0

    schedule.freeze()
    assert float(schedule.current(1000).lambda_e) == 0.0

    schedule.rewarm()
    assert float(schedule.current(0).lambda_e) == 0.0


def test_explicit_nonzero_cap_remains_a_schedule_control():
    schedule = ScheduledWeights(n_adam_k=500, lambda_e_max=0.5)
    assert float(schedule.current(25).lambda_e) == 0.25
    assert float(schedule.current(50).lambda_e) == 0.5


@pytest.mark.parametrize(
    "config_path",
    (
        _REPO_ROOT / "configs" / "smoke.yaml",
        _REPO_ROOT / "configs" / "stage0-example.yaml",
    ),
    ids=lambda path: path.name,
)
def test_shipped_stage0_configs_drive_zero_schedule(config_path):
    """Real shipped YAML values reach ScheduledWeights as exact zero."""
    config = load_config(config_path)
    assert config.loss.lambda_e_max == 0.0

    schedule = ScheduledWeights(
        n_adam_k=int(config.stage.n_adam),
        lambda_e_max=float(config.loss.lambda_e_max),
    )
    epochs = (
        0,
        max(1, schedule.warmup_length // 2),
        schedule.warmup_length,
        int(config.stage.n_adam),
        int(config.stage.n_adam) + 1000,
    )
    for epoch in epochs:
        assert float(schedule.current(epoch).lambda_e) == 0.0

    schedule.freeze()
    assert float(schedule.current(epochs[-1]).lambda_e) == 0.0
    schedule.rewarm()
    assert float(schedule.current(0).lambda_e) == 0.0
