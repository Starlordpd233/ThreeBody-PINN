"""Phase 49 / GATE-03 runtime invariant coverage."""

from __future__ import annotations

import pytest
from types import SimpleNamespace


def _guard_config(*, front_advance_window_n=None):
    return SimpleNamespace(
        guards=SimpleNamespace(
            loss_explosion_ceiling=1.0e6,
            disk_floor_fraction=0.05,
            memory_watermark_fraction=0.7,
        ),
        invariants=SimpleNamespace(
            front_advance_window_n=front_advance_window_n,
        ),
    )


def _make_guards(*, front_advance_window_n=None):
    from pinn.training.guards import StepGuards

    return StepGuards(
        _guard_config(front_advance_window_n=front_advance_window_n),
        memory_signal=lambda: None,
    )


def _healthy_stats(*, front_idx=0):
    return {
        "w_min": 0.1,
        "w_mean": 0.5,
        "w_max": 0.9,
        "front_idx": front_idx,
    }


def _minimal_yaml(*, invariants: str = "invariants: {}") -> str:
    return f"""\
run:
  {invariants}
stage:
  max_epochs: 10
  n_adam: 5
  stagnation_window: 2
  percentile_10_relaxation: 0.1
opt: {{}}
loss: {{}}
"""


def test_invariants_config_default_is_record_only():
    from pinn.training.config import InvariantsConfig

    config = InvariantsConfig()

    assert config.front_advance_window_n is None


@pytest.mark.parametrize("value", [0, -1, "250", True, False])
def test_invariants_config_rejects_non_positive_or_wrong_type(value):
    from pinn.training.config import InvariantsConfig

    with pytest.raises(ValueError):
        InvariantsConfig(front_advance_window_n=value)


def test_invariants_config_accepts_positive_int():
    from pinn.training.config import InvariantsConfig

    assert InvariantsConfig(front_advance_window_n=250).front_advance_window_n == 250


def test_yaml_invariants_constructs_dataclass(tmp_path):
    from pinn.training.config import InvariantsConfig
    from pinn.training.config_yaml import load_config

    path = tmp_path / "config.yaml"
    path.write_text(_minimal_yaml(invariants="invariants:\n    front_advance_window_n: 250"))

    config = load_config(path)

    assert isinstance(config.run.invariants, InvariantsConfig)
    assert config.run.invariants.front_advance_window_n == 250


def test_yaml_invariants_unknown_key_is_dotted(tmp_path):
    from pinn.training.config_yaml import ConfigKeyError, load_config

    path = tmp_path / "config.yaml"
    path.write_text(_minimal_yaml(invariants="invariants:\n    typo_field: 1"))

    with pytest.raises(ConfigKeyError) as exc_info:
        load_config(path)

    assert exc_info.value.dotted_path == "run.invariants.typo_field"


def test_run_config_rejects_non_invariants_config():
    from pinn.training.config import RunConfig

    with pytest.raises(TypeError, match=r"run\.invariants must be InvariantsConfig"):
        RunConfig(invariants={})  # type: ignore[arg-type]


def test_invariant_a_trips_on_zero_and_nonfinite_weight_stats():
    from pinn.training.stage_exit import StageDisposition

    guards = _make_guards()
    zero = guards.check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats={**_healthy_stats(), "w_min": 0.0},
        n_colloc=4,
        physics_evaluated=True,
    )
    nonfinite = guards.check(
        2, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats={**_healthy_stats(), "w_mean": float("nan")},
        n_colloc=4,
        physics_evaluated=True,
    )

    assert zero.disposition is StageDisposition.HALT
    assert zero.guard == "invariant_a"
    assert nonfinite.disposition is StageDisposition.HALT
    assert nonfinite.guard == "invariant_a"


def test_front_idx_sentinel_trips_invariant_a():
    from pinn.training.stage_exit import StageDisposition

    outcome = _make_guards().check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=-1),
        n_colloc=4,
        physics_evaluated=True,
    )

    assert outcome.disposition is StageDisposition.HALT
    assert outcome.guard == "invariant_a"
    assert "front_idx" in outcome.metric


def test_invariant_b_trips_after_window_and_marks_threshold_nonprovisional():
    from pinn.training.stage_exit import StageDisposition

    guards = _make_guards(front_advance_window_n=2)
    guards.check(
        0, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=0), n_colloc=4,
        physics_evaluated=True,
    )
    outcome = guards.check(
        3, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=0), n_colloc=4,
        physics_evaluated=True,
    )

    assert outcome.disposition is StageDisposition.HALT
    assert outcome.guard == "invariant_b"
    assert outcome.threshold == 2.0
    assert outcome.threshold_provisional is False


def test_invariant_b_saturation_never_trips():
    guards = _make_guards(front_advance_window_n=1)
    guards.check(
        0, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=3), n_colloc=4,
        physics_evaluated=True,
    )

    outcome = guards.check(
        100, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=3), n_colloc=4,
        physics_evaluated=True,
    )

    assert outcome.disposition is None


def test_invariant_b_high_water_tolerates_transient_regression():
    guards = _make_guards(front_advance_window_n=2)
    for step, front_idx in ((0, 3), (1, 2), (2, 3)):
        outcome = guards.check(
            step, 0, "2a", loss_terms={"total": 1.0},
            w_n_stats=_healthy_stats(front_idx=front_idx), n_colloc=5,
            physics_evaluated=True,
        )
        assert outcome.disposition is None

    assert guards.invariant_b_state_dict() == {
        "front_high_water": 3,
        "last_advance_step": 0,
    }


def test_invariant_b_n_unset_record_only_still_tracks_state():
    guards = _make_guards()
    first = guards.check(
        10, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=0), n_colloc=4,
        physics_evaluated=True,
    )
    later = guards.check(
        1000, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=0), n_colloc=4,
        physics_evaluated=True,
    )

    assert first.disposition is None
    assert later.disposition is None
    assert guards.invariant_b_state_dict() == {
        "front_high_water": 0,
        "last_advance_step": 10,
    }


def test_stats_missing_trips_only_when_physics_was_evaluated():
    from pinn.training.stage_exit import StageDisposition

    guards = _make_guards()
    non_physics = guards.check(
        1, 0, "2b", loss_terms={"total": 1.0},
        physics_evaluated=False,
    )
    missing = guards.check(
        2, 0, "2a", loss_terms={"total": 1.0},
        physics_evaluated=True,
    )
    partial = guards.check(
        3, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats={"w_min": 0.1}, physics_evaluated=True,
    )

    assert non_physics.disposition is None
    assert missing.disposition is StageDisposition.HALT
    assert missing.guard == "causal_stats_missing"
    assert partial.disposition is StageDisposition.HALT
    assert partial.guard == "causal_stats_missing"


def test_invariant_trip_halt_wins_recover_trip():
    from pinn.training.stage_exit import StageDisposition

    outcome = _make_guards().check(
        1, 0, "2a", loss_terms={"total": float("nan")},
        w_n_stats={**_healthy_stats(), "w_min": 0.0},
        n_colloc=4,
        physics_evaluated=True,
    )

    assert outcome.disposition is StageDisposition.HALT
    assert "nan_inf" in outcome.tripped_guards
    assert "invariant_a" in outcome.tripped_guards


def test_invariant_b_state_round_trips():
    source = _make_guards(front_advance_window_n=2)
    source.check(
        8, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=2), n_colloc=4,
        physics_evaluated=True,
    )
    target = _make_guards(front_advance_window_n=2)

    target.load_invariant_b_state(source.invariant_b_state_dict())

    assert target.invariant_b_state_dict() == source.invariant_b_state_dict()
