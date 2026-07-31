"""Phase 41 / Plan 04 — RunController + CurriculumController extensions.

Covers CTRL-02/03/04/06/07/08 controller-side wiring:
  * state_dict optimizer + four-stream rng + counters
  * build_checkpoint_payload single composer
  * pending-optimizer build-then-load ordering
  * per-step checkpoint_hook / guard_hook (phase-specific placement)
  * best.pt producer signal (_last_val_total)
  * CurriculumController ledger + promote + Adam-reset init anchors
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Optional
from unittest import mock

import numpy as np
import torch

from pinn.loss_catalog import LossTerms
from pinn.runtime import resolve_runtime
from pinn.training import determinism
from pinn.training.checkpoint import (
    CHECKPOINT_SCHEMA_VERSION,
    PromotionRefused,
    TorchSaveCheckpointStore,
    _is_structurally_valid,
)
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import OptConfig, StageConfig, TrainingConfig
from pinn.training.controllers import (
    CurriculumController,
    RunController,
    build_checkpoint_payload,
)
from pinn.training.grad_clip import GradClipper
from pinn.training.guards import GuardOutcome, StepGuards, write_failure_bundle
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageDisposition, StageExitMachine
from tests.phase41._fixtures import (
    StubClock,
    make_stub_model,
    make_stub_split_sources,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_config(*, max_epochs=4, n_adam=3, validation_every=1, **stage_overrides):
    stage_kwargs = dict(
        max_epochs=max_epochs,
        n_adam=n_adam,
        stagnation_window=10_000,
        percentile_10_relaxation=0.1,
        beta=0.9,
        patience=5,
        eps_plateau=1e-5,
        eps_phys=1e-4,
        eps_energy=1e-4,
    )
    stage_kwargs.update(stage_overrides)
    return TrainingConfig(
        stage=StageConfig(**stage_kwargs),
        opt=OptConfig(
            validation_every=validation_every,
            lbfgs_chunk_size=4,
            lbfgs_max_iter=2,
        ),
    )


def _canned_loss_terms(model, phys_value, dtype, device, total_override=None):
    if total_override is not None:
        total = torch.tensor(float(total_override), dtype=dtype, device=device)
    else:
        total = torch.zeros((), dtype=dtype, device=device)
        for p in model.parameters():
            total = total + (p ** 2).sum() * 1e-6
    zero = torch.zeros((), dtype=dtype, device=device)
    return LossTerms(
        data=zero, ic=zero,
        phys=torch.tensor(float(phys_value), dtype=dtype, device=device),
        energy=zero, angmom=zero, total=total,
    )


def _build_run_controller(
    tmp_dir,
    *,
    max_epochs=4,
    n_adam=3,
    validation_every=1,
    seed=0,
    checkpoint_hook=None,
    guard_hook=None,
    checkpoint_store=None,
):
    runtime = resolve_runtime("float64", "cpu")
    model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
    # Stage-0 selection requires >= 240 replay identities (phase40 convention).
    train_source, validation_source = make_stub_split_sources(n_train=300, n_validation=300)
    config = _make_config(
        max_epochs=max_epochs, n_adam=n_adam, validation_every=validation_every,
    )
    scheduled_weights = ScheduledWeights(n_adam, lambda_e_max=0.0, lambda_l_max=0.0)
    grad_clipper = GradClipper()
    collocation_sampler = CollocationSampler(2, np.random.default_rng(seed))
    stage_exit_machine = StageExitMachine(config)
    if checkpoint_store is None:
        checkpoint_store = TorchSaveCheckpointStore(tmp_dir)
    controller = RunController(
        model, train_source, validation_source, config,
        scheduled_weights, grad_clipper, collocation_sampler,
        stage_exit_machine, checkpoint_store, runtime,
        rng=np.random.default_rng(seed),
        checkpoint_hook=checkpoint_hook,
        guard_hook=guard_hook,
        s_h=1.0,
    )
    return controller, model, config, checkpoint_store


def _patch_cheap_loss(controller, *, phys=1.0, total_seq=None):
    """Replace expensive physics with a cheap params-only loss."""
    dtype, device = controller._dtype, controller._device
    call_count = {"n": 0}
    seq = list(total_seq) if total_seq is not None else None

    def fake_compose(batch, anchor_ctx, weights):
        if seq is not None:
            idx = min(call_count["n"], len(seq) - 1)
            val = seq[idx]
            call_count["n"] += 1
            return _canned_loss_terms(
                controller._model, phys, dtype, device, total_override=val,
            )
        call_count["n"] += 1
        return _canned_loss_terms(controller._model, phys, dtype, device)

    controller._compose_loss_terms = fake_compose  # type: ignore[method-assign]
    return call_count


# ---------------------------------------------------------------------------
# Task 1 — state exposure + payload composer
# ---------------------------------------------------------------------------

class StateDictExposureTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_state_dict_after_adam_has_optimizer_rng_counters(self):
        rc, _model, _cfg, _store = _build_run_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2,
        )
        _patch_cheap_loss(rc)
        rc.run_stage(0)
        sd = rc.state_dict()
        self.assertIn("model", sd)
        self.assertIn("scheduled_weights", sd)
        self.assertIn("clipper", sd)
        self.assertIsNotNone(sd["optimizer"])
        self.assertIsInstance(sd["optimizer"], dict)
        self.assertIn("rng", sd)
        for key in determinism.RNG_STREAM_KEYS:
            self.assertIn(key, sd["rng"])
        self.assertIn("counters", sd)
        self.assertGreater(sd["counters"]["global_step"], 0)

    def test_global_step_does_not_reset_across_run_stage(self):
        rc, _model, _cfg, _store = _build_run_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1,
        )
        _patch_cheap_loss(rc)
        rc.run_stage(0)
        step_after_first = rc._global_step
        self.assertGreater(step_after_first, 0)
        rc.run_stage(0)
        self.assertGreater(rc._global_step, step_after_first)


class CheckpointPayloadComposerTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_mid_stage_payload_has_all_ctx53_keys_optimizer_live(self):
        rc, _model, _cfg, _store = _build_run_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2,
        )
        _patch_cheap_loss(rc)
        rc.run_stage(0)
        curriculum = {"stage": 0, "phase": "2a", "epoch": 1, "step": 1}
        config_identity = {"run_id": "test"}
        payload = build_checkpoint_payload(
            rc, curriculum, config_identity, CHECKPOINT_SCHEMA_VERSION,
        )
        for key in (
            "model", "optimizer", "scheduled_weights", "grad_clip",
            "curriculum", "rng", "counters", "config_identity", "schema_version",
        ):
            self.assertIn(key, payload, msg=f"missing {key}")
        self.assertIsNotNone(payload["optimizer"])
        self.assertEqual(payload["schema_version"], CHECKPOINT_SCHEMA_VERSION)
        self.assertEqual(payload["curriculum"]["stage"], 0)
        self.assertTrue(_is_structurally_valid(payload))

    def test_fresh_init_anchor_optimizer_is_none(self):
        rc, _model, _cfg, _store = _build_run_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1,
        )
        rc._optimizer = None
        payload = build_checkpoint_payload(
            rc, {"stage": 0}, {}, CHECKPOINT_SCHEMA_VERSION,
        )
        self.assertIsNone(payload["optimizer"])

    def test_schema_version_imported_not_redefined(self):
        import pinn.training.controllers as mod
        import inspect
        src = inspect.getsource(mod)
        # Only import, never an assignment of CHECKPOINT_SCHEMA_VERSION = ...
        self.assertNotIn("CHECKPOINT_SCHEMA_VERSION =", src)
        self.assertIs(mod.CHECKPOINT_SCHEMA_VERSION, CHECKPOINT_SCHEMA_VERSION)


class RngRestoreExactTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_restore_exact_continuation_not_reseed(self):
        rc, _model, _cfg, _store = _build_run_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2, seed=7,
        )
        _patch_cheap_loss(rc)
        rc.run_stage(0)
        captured = rc.state_dict()
        expected_draw = float(np.random.default_rng(0).standard_normal())  # placeholder

        # Advance the live RNG after capture.
        _ = rc._rng.standard_normal()
        advanced_draw = float(rc._rng.standard_normal())

        # Branch A: restore from captured → next draw equals post-capture next.
        rc_a, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-a", max_epochs=1, n_adam=1, seed=7,
        )
        # Install the same rng object shape then restore.
        rc_a.load_state_dict(captured)
        draw_restored = float(rc_a._rng.standard_normal())

        # Branch B: reseed from seed (statistically-equivalent restart anti-pattern).
        reseeded = np.random.default_rng(7)
        draw_reseeded = float(reseeded.standard_normal())

        # Exact continuation: restore then draw matches the first post-capture draw
        # from a twin that advanced identically. Rebuild twin from captured.
        twin = np.random.default_rng(0)
        twin.bit_generator.state = captured["rng"]["numpy"]
        expected = float(twin.standard_normal())
        self.assertEqual(draw_restored, expected)
        # Distinct from a fresh same-seed restart (almost surely).
        self.assertNotEqual(draw_restored, draw_reseeded)
        # And distinct from the advanced-without-restore path.
        self.assertNotEqual(draw_restored, advanced_draw)
        del expected_draw  # silence unused


class OptimizerRestoreOrderingTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_pending_optimizer_applied_after_fresh_adam_build(self):
        rc, _model, _cfg, _store = _build_run_controller(
            self._tmpdir.name, max_epochs=3, n_adam=3,
        )
        _patch_cheap_loss(rc)
        rc.run_stage(0)
        captured = rc.state_dict()
        self.assertIsNotNone(captured["optimizer"])
        captured_opt = captured["optimizer"]

        # Fresh controller: optimizer is None at load time.
        rc2, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-2", max_epochs=3, n_adam=3,
        )
        self.assertIsNone(rc2._optimizer)
        rc2.load_state_dict(captured)
        self.assertIsNone(rc2._optimizer)
        self.assertIsNotNone(rc2._pending_optimizer_state)

        _patch_cheap_loss(rc2)
        # Enter run_stage → builds Adam and applies pending.
        rc2.run_stage(0)
        self.assertIsNone(rc2._pending_optimizer_state)
        self.assertIsNotNone(rc2._optimizer)
        # Moment buffers equal the captured ones at the moment of apply
        # (then training continues and may diverge — we re-apply by checking
        # that load into a third controller without running equals).
        rc3, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-3", max_epochs=1, n_adam=1,
        )
        rc3.load_state_dict(captured)
        # Manually build Adam and apply pending the same way run_stage does.
        opt = torch.optim.Adam(rc3._model.parameters(), lr=1e-3)
        rc3._optimizer = opt
        rc3._apply_pending_optimizer_state()
        live = rc3._optimizer.state_dict()
        # Compare state tensors in moment buffers.
        self.assertEqual(set(live["state"].keys()), set(captured_opt["state"].keys()))
        for pk in live["state"]:
            for field in live["state"][pk]:
                a = live["state"][pk][field]
                b = captured_opt["state"][pk][field]
                if torch.is_tensor(a):
                    self.assertTrue(torch.equal(a, b), msg=f"mismatch on {pk}/{field}")
                else:
                    self.assertEqual(a, b)

    def test_boundary_anchor_optimizer_none_leaves_adam_reset(self):
        rc, _model, _cfg, _store = _build_run_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1,
        )
        # Simulate boundary payload with optimizer=None.
        sd = rc.state_dict()
        sd["optimizer"] = None
        rc2, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-b", max_epochs=1, n_adam=1,
        )
        rc2.load_state_dict(sd)
        self.assertIsNone(rc2._pending_optimizer_state)
        _patch_cheap_loss(rc2)
        rc2.run_stage(0)
        # Fresh Adam was built; pending was None so moments start empty/fresh.
        self.assertIsNotNone(rc2._optimizer)
        # After one step moments exist but were not restored from prior stage.
        self.assertIsNone(rc2._pending_optimizer_state)


class BackwardCompatTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_phase40_payload_without_new_keys_loads(self):
        rc, _model, _cfg, _store = _build_run_controller(self._tmpdir.name)
        phase40 = {
            "model": rc._model.state_dict(),
            "scheduled_weights": rc._scheduled_weights.state_dict(),
            "clipper": rc._grad_clipper.state_dict(),
        }
        rc.load_state_dict(phase40)  # must not raise
        self.assertIsNone(rc._pending_optimizer_state)


# ---------------------------------------------------------------------------
# Task 2 — per-step hooks
# ---------------------------------------------------------------------------

class CheckpointHookTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_hook_none_writes_no_mid_stage_rolling(self):
        store = TorchSaveCheckpointStore(
            self._tmpdir.name, every_n_steps=1, wall_clock_ceiling_s=1e9,
        )
        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2, checkpoint_store=store,
        )
        _patch_cheap_loss(rc)
        rc.run_stage(0)
        steps = list(Path(self._tmpdir.name).glob("step-*.pt"))
        self.assertEqual(steps, [])

    def test_hook_writes_rolling_with_live_curriculum_stage(self):
        clock = StubClock(start=0.0)
        store = TorchSaveCheckpointStore(
            self._tmpdir.name,
            every_n_steps=1,
            wall_clock_ceiling_s=1e9,
            clock=clock.now,
        )
        live_stage = {"stage": 0}

        def curriculum_state_accessor():
            return {
                "stage": live_stage["stage"],
                "phase": "2a",
                "epoch": 0,
                "step": 0,
            }

        config_identity = {"run_id": "hook-test"}
        rolling_payloads = []

        def checkpoint_hook(controller, global_step):
            elapsed = float(clock.now()) - float(store.last_written_time)
            if not store.should_checkpoint(global_step, elapsed):
                return
            payload = build_checkpoint_payload(
                controller,
                curriculum_state_accessor(),
                config_identity,
                CHECKPOINT_SCHEMA_VERSION,
            )
            store.save_rolling(payload, global_step)
            rolling_payloads.append(payload)

        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-rc",
            max_epochs=2,
            n_adam=2,
            checkpoint_store=store,
            checkpoint_hook=checkpoint_hook,
        )
        _patch_cheap_loss(rc)
        live_stage["stage"] = 0
        rc.run_stage(0)
        self.assertGreaterEqual(len(rolling_payloads), 1)
        for p in rolling_payloads:
            self.assertEqual(p["curriculum"]["stage"], 0)
            self.assertTrue(_is_structurally_valid(p))
        # After a write, next step does not re-fire from the clock alone
        # (HIGH 3) when wall-clock ceiling is huge and step cadence is 1 —
        # step cadence still fires every step; exercise clock path separately.
        store2 = TorchSaveCheckpointStore(
            Path(self._tmpdir.name) / "clock",
            every_n_steps=10_000,
            wall_clock_ceiling_s=10.0,
            clock=clock.now,
        )
        clock.set(0.0)
        # Force a write mark.
        store2._mark_written(step=0)
        clock.advance(20.0)
        elapsed = clock.now() - store2.last_written_time
        self.assertTrue(store2.should_checkpoint(1, elapsed))
        store2.save_rolling({"model": {}, "optimizer": None, "curriculum": {},
                             "rng": {}, "counters": {}, "config_identity": {},
                             "schema_version": CHECKPOINT_SCHEMA_VERSION}, 1)
        # Same step must not re-fire.
        elapsed2 = clock.now() - store2.last_written_time
        self.assertFalse(store2.should_checkpoint(1, elapsed2))


class BestProducerTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_save_best_on_strict_improvement_only(self):
        store = TorchSaveCheckpointStore(
            self._tmpdir.name, every_n_steps=10_000, wall_clock_ceiling_s=1e9,
        )
        best_val = {"v": float("inf")}
        best_calls = []

        def checkpoint_hook(controller, global_step):
            # Independent of should_checkpoint — best.pt producer.
            val = controller._last_val_total
            if val is not None and val < best_val["v"]:
                best_val["v"] = val
                payload = build_checkpoint_payload(
                    controller, {"stage": 0}, {}, CHECKPOINT_SCHEMA_VERSION,
                )
                store.save_best(payload)
                best_calls.append(val)

        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-rc",
            max_epochs=5,
            n_adam=5,
            validation_every=1,
            checkpoint_store=store,
            checkpoint_hook=checkpoint_hook,
        )
        # Drive decreasing then flat validation totals via patched validation.
        val_seq = [3.0, 2.0, 2.0, 1.5, 1.5]
        idx = {"i": 0}

        def fake_val(k, weights):
            i = min(idx["i"], len(val_seq) - 1)
            v = val_seq[i]
            idx["i"] += 1
            zero = torch.zeros((), dtype=rc._dtype, device=rc._device)
            return LossTerms(
                data=zero, ic=zero, phys=zero, energy=zero, angmom=zero,
                total=torch.tensor(v, dtype=rc._dtype, device=rc._device),
            )

        _patch_cheap_loss(rc)
        rc._run_validation = fake_val  # type: ignore[method-assign]
        rc.run_stage(0)
        # Strict improvements only: 3→2→1.5 (not the plateaus at 2.0 / 1.5).
        self.assertEqual(best_calls, [3.0, 2.0, 1.5])
        best_path = Path(self._tmpdir.name) / "best.pt"
        self.assertTrue(best_path.is_file())
        loaded = torch.load(best_path, weights_only=True)
        self.assertTrue(_is_structurally_valid(loaded))


class AdamGuardHookTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_guard_trips_before_step_writes_bundle_and_failure_ckpt(self):
        store = TorchSaveCheckpointStore(self._tmpdir.name)
        run_dir = Path(self._tmpdir.name)
        step_calls = {"n": 0, "optimizer_stepped": False}
        real_step_holder = {}

        def guard_hook(controller, loss_terms, grad_norm, global_step, stage, phase):
            # Trip on the first Adam epoch (including step-0).
            if step_calls["n"] == 0:
                step_calls["n"] += 1
                outcome = GuardOutcome(
                    disposition=StageDisposition.RECOVER,
                    guard="nan_inf",
                    tier=1,
                    step=global_step,
                    stage=stage,
                    phase=phase,
                    reason="injected-nan",
                )
                write_failure_bundle(run_dir, outcome)
                payload = build_checkpoint_payload(
                    controller, {"stage": stage}, {}, CHECKPOINT_SCHEMA_VERSION,
                )
                store.save_anchor(
                    tag=f"failure-stage-{stage}-step-{global_step}",
                    stage=stage,
                    payload=payload,
                )
                return outcome
            step_calls["n"] += 1
            return GuardOutcome(disposition=None)

        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-rc",
            max_epochs=3,
            n_adam=3,
            checkpoint_store=store,
            guard_hook=guard_hook,
        )
        _patch_cheap_loss(rc)

        # Wrap optimizer.step after run_stage builds it — patch at Adam class.
        original_step = torch.optim.Adam.step

        def tracking_step(self, *args, **kwargs):
            step_calls["optimizer_stepped"] = True
            return original_step(self, *args, **kwargs)

        with mock.patch.object(torch.optim.Adam, "step", tracking_step):
            disposition = rc.run_stage(0)

        self.assertEqual(disposition, StageDisposition.RECOVER)
        self.assertFalse(
            step_calls["optimizer_stepped"],
            "guard must run BEFORE optimizer.step() on Adam trip",
        )
        self.assertTrue((run_dir / "failure" / "README.txt").is_file())
        failures = list(Path(self._tmpdir.name).glob("failure-*.pt"))
        self.assertGreaterEqual(len(failures), 1)
        loaded = torch.load(failures[0], weights_only=True)
        self.assertTrue(_is_structurally_valid(loaded))

    def test_without_guard_hook_inline_checks_still_fire(self):
        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2,
        )
        _patch_cheap_loss(rc, total_seq=[float("nan"), 1.0])
        disposition = rc.run_stage(0)
        self.assertEqual(disposition, StageDisposition.RECOVER)


class LbfgsGuardHookTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_lbfgs_guard_after_step_replaces_bare_recover(self):
        store = TorchSaveCheckpointStore(self._tmpdir.name)
        run_dir = Path(self._tmpdir.name)
        rewarm_calls = {"n": 0}
        guard_fired = {"n": 0}

        def guard_hook(controller, loss_terms, grad_norm, global_step, stage, phase):
            # Trip whenever total is non-finite (L-BFGS bridge forces nan).
            total = loss_terms.total
            is_bad = not bool(torch.isfinite(total))
            if is_bad:
                guard_fired["n"] += 1
                outcome = GuardOutcome(
                    disposition=StageDisposition.RECOVER,
                    guard="nan_inf",
                    tier=1,
                    step=global_step,
                    stage=stage,
                    phase=phase,
                    reason="lbfgs-nonfinite",
                )
                write_failure_bundle(run_dir, outcome)
                payload = build_checkpoint_payload(
                    controller, {"stage": stage}, {}, CHECKPOINT_SCHEMA_VERSION,
                )
                store.save_anchor(
                    tag=f"failure-stage-{stage}-step-{global_step}",
                    stage=stage,
                    payload=payload,
                )
                return outcome
            return GuardOutcome(disposition=None)

        # n_adam=1, max_epochs=3 → enters L-BFGS with budget 2.
        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name + "-rc",
            max_epochs=3,
            n_adam=1,
            checkpoint_store=store,
            guard_hook=guard_hook,
        )
        _patch_cheap_loss(rc)

        real_rewarm = rc._scheduled_weights.rewarm

        def tracking_rewarm():
            rewarm_calls["n"] += 1
            return real_rewarm()

        rc._scheduled_weights.rewarm = tracking_rewarm  # type: ignore[method-assign]

        # Force L-BFGS closure non_finite after Adam completes.
        real_make = rc._make_lbfgs_closure

        def make_bad_closure(optimizer, fixed_batch, anchor_ctx, weights, chunk_size, closure_state):
            def closure():
                optimizer.zero_grad(set_to_none=True)
                # Produce a finite graph then mark non_finite.
                total = torch.zeros((), dtype=rc._dtype, device=rc._device)
                for p in rc._model.parameters():
                    total = total + (p ** 2).sum() * 1e-9
                total.backward()
                closure_state["last_loss"] = float("nan")
                closure_state["non_finite"] = True
                return total

            return closure

        rc._make_lbfgs_closure = make_bad_closure  # type: ignore[method-assign]
        disposition = rc.run_stage(0)
        self.assertEqual(disposition, StageDisposition.RECOVER)
        self.assertGreaterEqual(guard_fired["n"], 1)
        self.assertTrue((run_dir / "failure" / "README.txt").is_file())
        self.assertGreaterEqual(rewarm_calls["n"], 1)
        failures = list(Path(self._tmpdir.name).glob("failure-*.pt"))
        self.assertGreaterEqual(len(failures), 1)
        del real_make


class GuardHaltFamilyTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_disk_floor_propagates_halt_not_recover(self):
        def guard_hook(controller, loss_terms, grad_norm, global_step, stage, phase):
            return GuardOutcome(
                disposition=StageDisposition.HALT,
                guard="disk_floor",
                tier=2,
                step=global_step,
                stage=stage,
                phase=phase,
                reason="disk-floor",
            )

        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2, guard_hook=guard_hook,
        )
        _patch_cheap_loss(rc)
        disposition = rc.run_stage(0)
        self.assertEqual(disposition, StageDisposition.HALT)

    def test_nan_inf_propagates_recover(self):
        def guard_hook(controller, loss_terms, grad_norm, global_step, stage, phase):
            return GuardOutcome(
                disposition=StageDisposition.RECOVER,
                guard="nan_inf",
                tier=1,
                step=global_step,
                stage=stage,
                phase=phase,
                reason="nan",
            )

        rc, _, _, _ = _build_run_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2, guard_hook=guard_hook,
        )
        _patch_cheap_loss(rc)
        disposition = rc.run_stage(0)
        self.assertEqual(disposition, StageDisposition.RECOVER)


# ---------------------------------------------------------------------------
# Task 3 — curriculum ledger + Adam reset composition
# ---------------------------------------------------------------------------

class LedgerAndPromotionTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_advance_writes_one_ledger_row_and_both_anchors(self):
        store = TorchSaveCheckpointStore(self._tmpdir.name, terminal_stage=2)
        config = _make_config(max_epochs=1, n_adam=1)
        sw = ScheduledWeights(1)
        curriculum = CurriculumController(
            config, store, sw,
            forced_disposition=lambda k: StageDisposition.ADVANCE,
        )
        disposition = curriculum.step()
        self.assertEqual(disposition, StageDisposition.ADVANCE)
        ledger = Path(self._tmpdir.name) / "curriculum.jsonl"
        self.assertTrue(ledger.is_file())
        rows = [json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "ADVANCE")
        self.assertEqual(rows[0]["from_stage"], 0)
        self.assertEqual(rows[0]["to_stage"], 1)

    def test_replayed_advance_is_idempotent(self):
        store = TorchSaveCheckpointStore(self._tmpdir.name, terminal_stage=2)
        config = _make_config(max_epochs=1, n_adam=1)
        sw = ScheduledWeights(1)
        # First ADVANCE 0→1
        c1 = CurriculumController(
            config, store, sw,
            forced_disposition=lambda k: StageDisposition.ADVANCE,
            initial_stage=0,
        )
        c1.step()
        ledger = Path(self._tmpdir.name) / "curriculum.jsonl"
        rows1 = ledger.read_text().splitlines()
        # Replay same 4-tuple via record_disposition directly.
        again = store.record_disposition(0, 1, StageDisposition.ADVANCE, 0)
        self.assertFalse(again)
        rows2 = ledger.read_text().splitlines()
        self.assertEqual(len(rows1), len(rows2))
        # save_anchor idempotent for stage-0-final (first write then replay).
        payload = {
            "model": {}, "optimizer": None, "curriculum": {},
            "rng": {}, "counters": {}, "config_identity": {},
            "schema_version": CHECKPOINT_SCHEMA_VERSION,
        }
        first = store.save_anchor("stage-0-final", 0, payload)
        self.assertIsNotNone(first)
        self.assertIsNone(store.save_anchor("stage-0-final", 0, payload))

    def test_recover_and_halt_each_write_one_row(self):
        store = TorchSaveCheckpointStore(self._tmpdir.name)
        store.save({"tag": "seed", "stage": 0})
        config = _make_config()
        sw = ScheduledWeights(1)
        c_rec = CurriculumController(
            config, store, sw,
            forced_disposition=lambda k: StageDisposition.RECOVER,
            recover_retries=0,
        )
        self.assertEqual(c_rec.step(), StageDisposition.HALT)  # recover-exhausted → HALT
        # RECOVER is journaled; HALT from recover-exhausted currently only
        # journals RECOVER in the RECOVER branch — the returned HALT from
        # recover-exhausted does not re-enter the HALT branch. Drive a pure HALT.
        store2_dir = Path(self._tmpdir.name) / "halt"
        store2 = TorchSaveCheckpointStore(store2_dir)
        c_halt = CurriculumController(
            config, store2, sw,
            forced_disposition=lambda k: StageDisposition.HALT,
        )
        self.assertEqual(c_halt.step(), StageDisposition.HALT)
        ledger_halt = store2_dir / "curriculum.jsonl"
        rows = [json.loads(l) for l in ledger_halt.read_text().splitlines() if l.strip()]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "HALT")

        ledger_rec = Path(self._tmpdir.name) / "curriculum.jsonl"
        rec_rows = [json.loads(l) for l in ledger_rec.read_text().splitlines() if l.strip()]
        self.assertTrue(any(r["disposition"] == "RECOVER" for r in rec_rows))

    def test_out_of_order_promotion_raises(self):
        store = TorchSaveCheckpointStore(self._tmpdir.name, terminal_stage=2)
        with self.assertRaises(PromotionRefused):
            store.promote(0, 2)  # skip
        with self.assertRaises(PromotionRefused):
            store.promote(1, 0)  # regress


class AdamResetCompositionTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_stage_init_anchor_optimizer_is_none(self):
        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        train_source, validation_source = make_stub_split_sources(n_train=300, n_validation=300)
        config = _make_config(max_epochs=2, n_adam=2)
        store = TorchSaveCheckpointStore(self._tmpdir.name, terminal_stage=2)

        def make_rc(n_adam, lambda_phys_max):
            sw = ScheduledWeights(n_adam, lambda_e_max=0.0, lambda_l_max=0.0)
            # Force a known lambda_phys_max via state if attribute exists.
            if hasattr(sw, "_lambda_phys_max"):
                sw._lambda_phys_max = lambda_phys_max  # type: ignore[attr-defined]
            rc = RunController(
                model, train_source, validation_source, config,
                sw, GradClipper(),
                CollocationSampler(2, np.random.default_rng(0)),
                StageExitMachine(config), store, runtime,
                rng=np.random.default_rng(1),
                s_h=1.0,
            )
            _patch_cheap_loss(rc)
            return rc

        stage0 = make_rc(2, 1.0)
        # Populate live optimizer moments.
        stage0.run_stage = mock.Mock(return_value=StageDisposition.ADVANCE)  # type: ignore
        # Manually set a non-None optimizer to prove it is cleared on enter.
        stage0._optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
        # Take a step so state is non-empty.
        loss = sum((p ** 2).sum() for p in model.parameters()) * 1e-6
        loss.backward()
        stage0._optimizer.step()
        pre_boundary = stage0._optimizer.state_dict()
        self.assertTrue(len(pre_boundary["state"]) > 0)

        stage1 = make_rc(2, 2.0)
        self.assertIsNone(stage1._optimizer)

        curriculum = CurriculumController(
            config, store, stage0.scheduled_weights,
            run_controller=stage0,
            stage_factory=lambda k: stage1,
        )
        disposition = curriculum.step()
        self.assertEqual(disposition, StageDisposition.ADVANCE)
        self.assertIs(curriculum._run_controller, stage1)
        self.assertIsNone(stage1._optimizer)

        # Production CTX-53 init anchor has optimizer=None.
        init_path = Path(self._tmpdir.name) / "stage-1-init.pt"
        self.assertTrue(init_path.is_file())
        init_payload = torch.load(init_path, weights_only=True)
        self.assertIsNone(init_payload["optimizer"])
        self.assertTrue(_is_structurally_valid(init_payload))

        # Restoring yields pending=None → fresh Adam reset.
        stage1.load_state_dict(init_payload)
        self.assertIsNone(stage1._pending_optimizer_state)
        # Pre-boundary moments differ from a freshly built Adam (empty state).
        fresh = torch.optim.Adam(model.parameters(), lr=1e-3)
        self.assertNotEqual(
            list(pre_boundary["state"].keys()),
            list(fresh.state_dict()["state"].keys()) if fresh.state_dict()["state"] else [],
        )
        # Explicit: pre-boundary had moments; post-boundary pending is None.
        self.assertTrue(len(pre_boundary["state"]) > 0)


if __name__ == "__main__":
    unittest.main()
