"""Stage-0 energy-cap conformance tests for Phase 48 Plan 02."""

from __future__ import annotations

from pinn.training.config import LossConfig
from pinn.training.scheduled_weights import ScheduledWeights


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
