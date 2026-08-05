"""Phase 49 / GATE-03 D-17 checkpoint payload and resume contract tests."""

from __future__ import annotations

from types import SimpleNamespace

import pytest


def _payload_controller():
    class FakeController:
        def state_dict(self):
            return {
                "model": {"weight": 1},
                "optimizer": None,
                "scheduled_weights": {},
                "clipper": {},
                "rng": {},
                "counters": {},
            }

    return FakeController()


def _make_guards(*, front_advance_window_n=None):
    from pinn.training.guards import StepGuards

    config = SimpleNamespace(
        guards=SimpleNamespace(
            loss_explosion_ceiling=1.0e6,
            disk_floor_fraction=0.05,
            memory_watermark_fraction=0.7,
        ),
        invariants=SimpleNamespace(
            front_advance_window_n=front_advance_window_n,
        ),
    )
    return StepGuards(config, memory_signal=lambda: None)


def test_build_checkpoint_payload_carries_invariant_b_state_and_schema_symbol():
    from pinn.training.checkpoint import CHECKPOINT_SCHEMA_VERSION
    from pinn.training.controllers import build_checkpoint_payload

    state = {"front_high_water": 3, "last_advance_step": 17}
    payload = build_checkpoint_payload(
        _payload_controller(),
        {"stage": 0},
        {"run_id": "test"},
        CHECKPOINT_SCHEMA_VERSION,
        invariant_b_state=state,
    )

    assert CHECKPOINT_SCHEMA_VERSION == 2
    assert payload["schema_version"] == CHECKPOINT_SCHEMA_VERSION
    assert payload["invariant_b_state"] == state


def test_build_checkpoint_payload_without_provider_emits_explicit_none():
    from pinn.training.checkpoint import CHECKPOINT_SCHEMA_VERSION
    from pinn.training.controllers import build_checkpoint_payload

    payload = build_checkpoint_payload(
        _payload_controller(), {"stage": 0}, {}, CHECKPOINT_SCHEMA_VERSION
    )

    assert "invariant_b_state" in payload
    assert payload["invariant_b_state"] is None


def test_curriculum_checkpoint_uses_invariant_b_state_provider():
    from pinn.training.checkpoint import CHECKPOINT_SCHEMA_VERSION
    from pinn.training.controllers import CurriculumController

    class FakeStore:
        def __init__(self):
            self.payloads = []

        def save_anchor(self, *, tag, stage, payload):
            self.payloads.append(payload)

    class FakeRunController:
        _global_step = 17

        def state_dict(self):
            return {
                "model": {"weight": 1},
                "optimizer": None,
                "scheduled_weights": {},
                "clipper": {},
                "rng": {},
                "counters": {},
            }

    state = {"front_high_water": 4, "last_advance_step": 17}
    store = FakeStore()
    curriculum = CurriculumController(
        config=SimpleNamespace(),
        checkpoint_store=store,
        scheduled_weights=SimpleNamespace(),
        run_controller=FakeRunController(),
        invariant_b_state_provider=lambda: state,
    )

    curriculum._save_ctx53_anchor("stage-0-final", 0)

    assert store.payloads[0]["schema_version"] == CHECKPOINT_SCHEMA_VERSION
    assert store.payloads[0]["invariant_b_state"] == state


def _advance_before_checkpoint(guards):
    """Create a non-initial invariant-B window before taking a snapshot."""
    guards.check(
        0,
        0,
        "2a",
        loss_terms={"total": 1.0},
        w_n_stats={"w_min": 0.1, "w_mean": 0.5, "w_max": 0.9, "front_idx": 0},
        n_colloc=10,
        physics_evaluated=True,
    )
    guards.check(
        1,
        0,
        "2a",
        loss_terms={"total": 1.0},
        w_n_stats={"w_min": 0.1, "w_mean": 0.5, "w_max": 0.9, "front_idx": 1},
        n_colloc=10,
        physics_evaluated=True,
    )


def test_restore_preserves_stall_window_across_resume_boundary():
    from pinn.training.checkpoint import CHECKPOINT_SCHEMA_VERSION
    from pinn.training.controllers import build_checkpoint_payload
    from pinn.train import _restore_invariant_b_state

    before = _make_guards(front_advance_window_n=2)
    _advance_before_checkpoint(before)
    payload = build_checkpoint_payload(
        _payload_controller(), {}, {}, CHECKPOINT_SCHEMA_VERSION,
        invariant_b_state=before.invariant_b_state_dict(),
    )

    after = _make_guards(front_advance_window_n=2)
    _restore_invariant_b_state(after, payload)
    assert after.invariant_b_state_dict() == {
        "front_high_water": 1,
        "last_advance_step": 1,
    }

    one_before_trip = after.check(
        3,
        0,
        "2a",
        loss_terms={"total": 1.0},
        w_n_stats={"w_min": 0.1, "w_mean": 0.5, "w_max": 0.9, "front_idx": 1},
        n_colloc=10,
        physics_evaluated=True,
    )
    assert one_before_trip.disposition is None

    trip = after.check(
        4,
        0,
        "2a",
        loss_terms={"total": 1.0},
        w_n_stats={"w_min": 0.1, "w_mean": 0.5, "w_max": 0.9, "front_idx": 1},
        n_colloc=10,
        physics_evaluated=True,
    )
    assert trip.guard == "invariant_b"


def test_restore_explicit_none_keeps_initialized_state():
    from pinn.train import _restore_invariant_b_state

    guards = _make_guards(front_advance_window_n=2)
    _restore_invariant_b_state(guards, {"invariant_b_state": None})

    assert guards.invariant_b_state_dict() == {
        "front_high_water": -1,
        "last_advance_step": None,
    }


def test_restore_rejects_v2_payload_missing_invariant_b_state():
    from pinn.train import _restore_invariant_b_state

    with pytest.raises(ValueError, match="invariant_b_state"):
        _restore_invariant_b_state(_make_guards(), {})


@pytest.mark.parametrize(
    "state",
    [
        ["not", "a", "mapping"],
        {"last_advance_step": 2},
        {"front_high_water": "1", "last_advance_step": 2},
    ],
)
def test_restore_rejects_malformed_invariant_b_state(state):
    from pinn.train import _restore_invariant_b_state

    with pytest.raises((TypeError, ValueError)):
        _restore_invariant_b_state(
            _make_guards(), {"invariant_b_state": state}
        )


def test_schema_v1_payload_is_structurally_invalid_after_bump():
    from pinn.training.checkpoint import (
        CHECKPOINT_SCHEMA_VERSION,
        _is_structurally_valid,
    )
    from pinn.training.controllers import build_checkpoint_payload

    payload = build_checkpoint_payload(
        _payload_controller(), {}, {}, CHECKPOINT_SCHEMA_VERSION,
        invariant_b_state={"front_high_water": 1, "last_advance_step": 1},
    )
    payload["schema_version"] = 1

    assert not _is_structurally_valid(payload)
