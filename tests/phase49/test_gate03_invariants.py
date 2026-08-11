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


def test_guard_hook_wiring_populated_stats_reaches_step_guards():
    from pinn.train import _guard_causal_inputs

    controller = SimpleNamespace(
        _last_widened_details={
            "w_n_stats": _healthy_stats(front_idx=0),
            "residuals_per_bin": [1.0, 0.5, 0.25],
        }
    )
    stats, n_colloc, physics_evaluated = _guard_causal_inputs(controller, "2a")
    outcome = _make_guards().check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=stats, n_colloc=n_colloc,
        physics_evaluated=physics_evaluated,
    )

    assert stats == _healthy_stats(front_idx=0)
    assert n_colloc == 3
    assert physics_evaluated is True
    assert outcome.disposition is None


def test_guard_hook_wiring_stripped_stats_trips_causal_stats_missing():
    from pinn.train import _guard_causal_inputs
    from pinn.training.stage_exit import StageDisposition

    controller = SimpleNamespace(
        _last_widened_details={"residuals_per_bin": [1.0, 0.5, 0.25]}
    )
    stats, n_colloc, physics_evaluated = _guard_causal_inputs(controller, "2a")
    outcome = _make_guards().check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=stats, n_colloc=n_colloc,
        physics_evaluated=physics_evaluated,
    )

    assert stats is None
    assert n_colloc == 3
    assert physics_evaluated is True
    assert outcome.disposition is StageDisposition.HALT
    assert outcome.guard == "causal_stats_missing"


def test_guard_hook_halt_outcome_keeps_failure_bundle_contract(tmp_path):
    from pinn.train import _guard_causal_inputs
    from pinn.training.guards import write_failure_bundle

    controller = SimpleNamespace(_last_widened_details=None)
    stats, n_colloc, physics_evaluated = _guard_causal_inputs(controller, "2a")
    outcome = _make_guards().check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=stats, n_colloc=n_colloc,
        physics_evaluated=physics_evaluated,
    )
    write_failure_bundle(tmp_path, outcome)

    assert (tmp_path / "failure" / "README.txt").is_file()
    assert (tmp_path / "failure" / "trip.json").is_file()


# --- CR-02: malformed front_idx cannot bypass or crash invariant B ---------
#
# Before this hardening the guard coerced with a bare ``int()``, which accepts
# bools, truncates non-integral floats, admits out-of-range indices, and raises
# an uncaught OverflowError on infinity. An index at or above ``n_colloc - 1``
# pins the high-water mark at "saturated", which permanently silences the
# invariant-B stall guard — so each refusal below is driven to actually trip
# (D-16), not merely asserted to exist.


@pytest.mark.parametrize(
    ("label", "front_idx"),
    [
        ("out-of-range-high", 4),
        ("far-out-of-range-high", 99),
        ("below-sentinel", -2),
        ("bool-true", True),
        ("bool-false", False),
        ("non-integral-float", 1.9),
        ("positive-infinity", float("inf")),
        ("negative-infinity", float("-inf")),
        ("nan", float("nan")),
        ("string", "2"),
    ],
)
def test_malformed_front_idx_refuses_via_invariant_a(label, front_idx):
    from pinn.training.stage_exit import StageDisposition

    outcome = _make_guards().check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=front_idx),
        n_colloc=4,
        physics_evaluated=True,
    )

    assert outcome.disposition is StageDisposition.HALT, label
    assert outcome.guard == "invariant_a", label
    assert outcome.metric == "w_n_stats.front_idx", label


def test_out_of_range_front_idx_cannot_saturate_the_high_water_mark():
    """The bypass this refusal exists to close.

    ``front_idx = 99`` with ``n_colloc = 4`` used to be accepted, leaving
    ``front_high_water >= n_colloc - 1`` forever, so the stall guard read as
    saturated and could never trip again.
    """
    from pinn.training.stage_exit import StageDisposition

    guards = _make_guards(front_advance_window_n=2)
    refused = guards.check(
        0, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=99), n_colloc=4,
        physics_evaluated=True,
    )

    assert refused.guard == "invariant_a"
    # State is untouched: the impossible index never became the high-water mark.
    assert guards.invariant_b_state_dict() == {
        "front_high_water": -1,
        "last_advance_step": None,
    }

    # And the stall guard still works afterwards.
    guards.check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=0), n_colloc=4,
        physics_evaluated=True,
    )
    stalled = guards.check(
        10, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=0), n_colloc=4,
        physics_evaluated=True,
    )

    assert stalled.disposition is StageDisposition.HALT
    assert stalled.guard == "invariant_b"


def test_non_finite_front_idx_raises_no_bare_overflow_error():
    """``int(float("inf"))`` raises OverflowError, which used to escape."""
    guards = _make_guards()

    try:
        outcome = guards.check(
            1, 0, "2a", loss_terms={"total": 1.0},
            w_n_stats=_healthy_stats(front_idx=float("inf")), n_colloc=4,
            physics_evaluated=True,
        )
    except OverflowError as exc:  # pragma: no cover - the regression itself
        pytest.fail(f"OverflowError escaped the invariant-A refusal path: {exc}")

    assert outcome.guard == "invariant_a"
    assert outcome.tier == 2


def test_last_admissible_front_idx_is_accepted():
    """The range is half-open: n_colloc - 1 is valid, n_colloc is not."""
    guards = _make_guards()
    outcome = guards.check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=3), n_colloc=4,
        physics_evaluated=True,
    )

    assert outcome.disposition is None
    assert guards.invariant_b_state_dict()["front_high_water"] == 3


def test_integral_float_front_idx_is_accepted():
    """Instrumentation may report a float; only NON-integral floats are bad."""
    guards = _make_guards()
    outcome = guards.check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=2.0), n_colloc=4,
        physics_evaluated=True,
    )

    assert outcome.disposition is None
    assert guards.invariant_b_state_dict()["front_high_water"] == 2


def test_front_idx_range_unchecked_when_n_colloc_is_unknown():
    """Without a known collocation length only well-formedness is assertable."""
    guards = _make_guards()
    outcome = guards.check(
        1, 0, "2a", loss_terms={"total": 1.0},
        w_n_stats=_healthy_stats(front_idx=99), n_colloc=None,
        physics_evaluated=True,
    )

    assert outcome.disposition is None
    assert guards.invariant_b_state_dict()["front_high_water"] == 99


def test_consistency_finding_reads_run_scoped_window_from_real_config(
    tmp_path, monkeypatch
):
    """The consistency finding must read ``config.run.invariants`` (real path).

    The verifier flagged ``preflight.py:384``: the accessor read
    ``config.invariants``, so even the shipped owner-ratified N = 500 config
    reported ``config_value: None``.  A real ``TrainingConfig`` carrying the
    window under ``run.invariants`` must report 500.
    """
    import copy

    from pinn.conformance import preflight, register
    from pinn.training.config_yaml import load_config

    path = tmp_path / "config.yaml"
    path.write_text(
        _minimal_yaml(invariants="invariants:\n    front_advance_window_n: 500")
    )
    config = load_config(path)
    assert config.run.invariants.front_advance_window_n == 500

    modified = copy.deepcopy(register.load_divergence_register())
    entry = next(
        item for item in modified["entries"] if item["id"] == "INV-B-N-UNSET"
    )
    entry["status"] = "open"
    entry["proof_test"] = None
    monkeypatch.setattr(preflight, "load_divergence_register", lambda: modified)
    open_entries = [
        dict(item) for item in modified["entries"] if item["status"] == "open"
    ]

    finding = preflight._consistency_finding(config, open_entries)

    assert finding is not None
    assert finding["config_value"] == 500
    assert finding["register_id"] == "INV-B-N-UNSET"
    assert finding["register_status"] == "open"
