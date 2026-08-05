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
