"""Phase 40 / TRAIN-02 + TRAIN-06 wiring -- RunController + PlateauDetector tests.

Dataset-free (stub source/model only). Control-flow-focused tests (plateau
handoff timing, budget-exhaustion, NaN/Inf routing, clip-spy counts) mock the
``RunController._compose_loss_terms`` / ``accumulate_chunked_data_term`` /
``_weighted_non_data_terms`` seams so the real (heavy) physics forward never
runs for those cases -- ``build_stage_batch`` and ``_build_anchor_context``
still run for real (cheap: pure numpy + a single-snapshot Hamiltonian/angular-
momentum calc, no model forward). A small number of DEDICATED tests exercise
the real, non-injected forward/AD path (validation wiring identity, chunked-
accumulation equality, single-collocation-source) to prove the wiring is real.
"""

from __future__ import annotations

import importlib
import tempfile
import unittest
from dataclasses import replace
from types import SimpleNamespace
from unittest import mock

import numpy as np
import torch

from tests.phase40 import _SKIP_PHRASE
from tests.phase40._fixtures import make_stub_model, make_stub_split_sources

MODULE = "pinn.training.controllers"


def _require(symbol):
    try:
        mod = importlib.import_module(MODULE)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}")
    return getattr(mod, symbol)


from pinn.data.batches import build_stage_batch  # noqa: E402  (already landed, Phase 39)
from pinn.loss_catalog import LossTerms, data_huber_loss  # noqa: E402
from pinn.runtime import resolve_runtime  # noqa: E402
from pinn.training.checkpoint import TorchSaveCheckpointStore  # noqa: E402
from pinn.training.collocation_sampler import CollocationSampler  # noqa: E402
from pinn.training.config import OptConfig, StageConfig, TrainingConfig  # noqa: E402
from pinn.training.grad_clip import GradClipOutcome, GradClipper  # noqa: E402
from pinn.training.scheduled_weights import ScheduledWeights  # noqa: E402
from pinn.training.stage_exit import StageDisposition, StageExitMachine  # noqa: E402


# ---------------------------------------------------------------------------
# Shared test helpers.
# ---------------------------------------------------------------------------

def _make_config(*, max_epochs, n_adam, validation_every=10_000, lbfgs_chunk_size=4,
                 lbfgs_max_iter=2, energy_floor_factor=None):
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
    if energy_floor_factor is not None:
        stage_kwargs["energy_floor_factor"] = energy_floor_factor
    stage = StageConfig(**stage_kwargs)
    opt = OptConfig(
        validation_every=validation_every,
        lbfgs_chunk_size=lbfgs_chunk_size,
        lbfgs_max_iter=lbfgs_max_iter,
    )
    return TrainingConfig(stage=stage, opt=opt)


def _build_controller(tmp_dir, *, max_epochs, n_adam, validation_every=10_000,
                      collocation_count=2, energy_floor_factor=None):
    RunController = _require("RunController")
    runtime = resolve_runtime("float64", "cpu")
    model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
    train_source, validation_source = make_stub_split_sources(n_train=300, n_validation=300)
    config = _make_config(
        max_epochs=max_epochs, n_adam=n_adam, validation_every=validation_every,
        energy_floor_factor=energy_floor_factor,
    )
    scheduled_weights = ScheduledWeights(n_adam, lambda_e_max=0.0, lambda_l_max=0.0)
    grad_clipper = GradClipper()
    collocation_sampler = CollocationSampler(collocation_count, np.random.default_rng(0))
    stage_exit_machine = StageExitMachine(config)
    checkpoint_store = TorchSaveCheckpointStore(tmp_dir)
    return RunController(
        model, train_source, validation_source, config,
        scheduled_weights, grad_clipper, collocation_sampler,
        stage_exit_machine, checkpoint_store, runtime,
        rng=np.random.default_rng(1),
    )


def _canned_loss_terms(model, phys_value, dtype, device, total_override=None):
    """A cheap, real-graph-connected LossTerms for control-flow tests.

    ``.total`` is a genuine differentiable function of every model parameter
    (so backward/clip/step exercise real Adam mechanics without a heavy
    forward pass over a large batch), UNLESS ``total_override`` is supplied
    (a plain float, e.g. NaN, used for the non-finite-loss RECOVER tests --
    fine since those paths check isfinite BEFORE calling backward).
    """
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


def _fake_chunked_data_term(model, data_points, *, weight, chunk_size, dtype, device):
    """Cheap stand-in for ``accumulate_chunked_data_term`` (params-only cost)."""
    total = torch.zeros((), dtype=dtype, device=device)
    for p in model.parameters():
        total = total + (p ** 2).sum() * 1e-7
    weighted = total * float(weight)
    weighted.backward()
    return weighted.detach()


def _make_fake_non_data_terms(controller):
    def fake(anchor_ctx, weights):
        total = torch.zeros((), dtype=controller._dtype, device=controller._device)
        for p in controller._model.parameters():
            total = total + (p ** 2).sum() * 1e-7
        return total
    return fake


# ---------------------------------------------------------------------------
# PlateauDetector (Task 1 / CTX-46).
# ---------------------------------------------------------------------------

class PlateauDetectorTests(unittest.TestCase):
    def setUp(self):
        self.PlateauDetector = _require("PlateauDetector")

    def test_flat_curve_fires_at_50th_consecutive_qualifying_epoch(self):
        d = self.PlateauDetector()
        self.assertFalse(d.update(1.0))  # first call: no slope yet
        fired = False
        for _ in range(49):
            fired = d.update(1.0)
        self.assertFalse(fired)
        self.assertEqual(d.consecutive_qualifying_epochs, 49)
        self.assertTrue(d.update(1.0))
        self.assertEqual(d.consecutive_qualifying_epochs, 50)

    def test_descending_curve_never_fires(self):
        d = self.PlateauDetector()
        value = 1.0
        for _ in range(200):
            fired = d.update(value)
            self.assertFalse(fired)
            value *= 0.5
        self.assertLess(d.consecutive_qualifying_epochs, 50)

    def test_single_violating_epoch_resets_counter(self):
        d = self.PlateauDetector()
        d.update(1.0)
        for _ in range(48):
            d.update(1.0)
        self.assertEqual(d.consecutive_qualifying_epochs, 48)
        d.update(1e-10)  # slope << threshold -- resets
        self.assertEqual(d.consecutive_qualifying_epochs, 0)
        fired = False
        for _ in range(49):
            fired = d.update(1e-10)
        self.assertFalse(fired)
        self.assertTrue(d.update(1e-10))

    def test_no_shared_state_with_stage_exit_smoother(self):
        d = self.PlateauDetector()
        # PlateauDetector exposes no attribute referencing the CURR-03
        # TotalLossPlateauSmoother -- a structural, not just textual, check.
        for name in vars(d):
            self.assertNotIn("smooth", name.lower())


# ---------------------------------------------------------------------------
# RunController construction.
# ---------------------------------------------------------------------------

class RunControllerConstructionTests(unittest.TestCase):
    def setUp(self):
        self.RunController = _require("RunController")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_missing_validation_source_raises(self):
        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        train_source, _validation_source = make_stub_split_sources()
        config = _make_config(max_epochs=1, n_adam=1)
        scheduled_weights = ScheduledWeights(1)
        grad_clipper = GradClipper()
        collocation_sampler = CollocationSampler(2, np.random.default_rng(0))
        stage_exit_machine = StageExitMachine(config)
        checkpoint_store = TorchSaveCheckpointStore(self._tmpdir.name)
        with self.assertRaises(ValueError):
            self.RunController(
                model, train_source, None, config,
                scheduled_weights, grad_clipper, collocation_sampler,
                stage_exit_machine, checkpoint_store, runtime,
            )


# ---------------------------------------------------------------------------
# Adam -> L-BFGS control flow (mocked forward -- fast).
# ---------------------------------------------------------------------------

class RunControllerControlFlowTests(unittest.TestCase):
    def setUp(self):
        self.RunController = _require("RunController")
        self.HandoffEvent = _require("HandoffEvent")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_flat_phys_curve_drives_plateau_handoff_through_run_stage(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=55, n_adam=55, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=_fake_chunked_data_term), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)):
            disposition = controller.run_stage(0)

        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertIsNotNone(controller.last_handoff_event)
        self.assertEqual(controller.last_handoff_event.trigger, "plateau")
        self.assertEqual(controller.last_handoff_event.adam_epochs_used, 51)

    def test_descending_curve_exits_adam_via_budget_exhaustion_then_halts(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=5, n_adam=3, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device
        values = iter([1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14])

        def fake_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, next(values), dtype, device)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=_fake_chunked_data_term), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)):
            disposition = controller.run_stage(0)

        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertEqual(controller.last_handoff_event.trigger, "budget-exhausted")
        self.assertEqual(controller.last_handoff_event.adam_epochs_used, 3)

    def test_fresh_adam_and_scheduler_constructed_per_run_stage_call(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        adam_spy = mock.Mock(wraps=torch.optim.Adam)
        sched_spy = mock.Mock(wraps=torch.optim.lr_scheduler.CosineAnnealingLR)
        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_compose), \
             mock.patch("torch.optim.Adam", adam_spy), \
             mock.patch("torch.optim.lr_scheduler.CosineAnnealingLR", sched_spy):
            controller.run_stage(0)
            controller.run_stage(1)

        self.assertEqual(adam_spy.call_count, 2)
        self.assertEqual(sched_spy.call_count, 2)

    def test_finite_loss_nonfinite_gradient_adam_returns_recover_via_clip_outcome(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=2, n_adam=2, validation_every=10_000,
        )
        fake_outcome = GradClipOutcome(
            non_finite=True, clip_value=None,
            total_norm=torch.tensor(float("nan")), window_len=0,
        )
        with mock.patch.object(controller._grad_clipper, "clip", return_value=fake_outcome):
            disposition = controller.run_stage(0)
        self.assertEqual(disposition, StageDisposition.RECOVER)

    def test_nonfinite_loss_in_adam_returns_recover(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=3, n_adam=3, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device, total_override=float("nan"))

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_compose):
            disposition = controller.run_stage(0)
        self.assertEqual(disposition, StageDisposition.RECOVER)

    def test_nonfinite_loss_in_lbfgs_returns_recover(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=3, n_adam=1, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_adam_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        def fake_chunked_nan(model_, data_points, *, weight, chunk_size, dtype, device):
            return torch.tensor(float("nan"), dtype=dtype, device=device)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_adam_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=fake_chunked_nan), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)):
            disposition = controller.run_stage(0)
        self.assertEqual(disposition, StageDisposition.RECOVER)

    def test_nonfinite_gradient_in_lbfgs_returns_recover(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=3, n_adam=1, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_adam_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_adam_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=_fake_chunked_data_term), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)), \
             mock.patch.object(controller, "_grads_finite", return_value=False):
            disposition = controller.run_stage(0)
        self.assertEqual(disposition, StageDisposition.RECOVER)

    def test_finite_lbfgs_stall_is_not_routed_to_recover(self):
        # A finite-but-never-improving loss (constant) is NOT a RECOVER trigger;
        # it falls through the ADVANCE gate to HALT at MAX_EPOCHS, never RECOVER.
        controller = _build_controller(
            self._tmpdir.name, max_epochs=3, n_adam=1, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_adam_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_adam_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=_fake_chunked_data_term), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)):
            disposition = controller.run_stage(0)
        self.assertEqual(disposition, StageDisposition.HALT)

    def test_clip_spy_counts_one_in_adam_zero_in_lbfgs(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=3, n_adam=1, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_adam_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        real_clip = controller._grad_clipper.clip
        clip_spy = mock.Mock(wraps=real_clip)
        torch_clip_spy = mock.Mock(wraps=torch.nn.utils.clip_grad_norm_)

        original_lbfgs = controller._run_lbfgs_phase
        marker = {}

        def spy_lbfgs(*args, **kwargs):
            marker["adam_clip_calls"] = clip_spy.call_count
            clip_spy.reset_mock()
            torch_clip_spy.reset_mock()
            return original_lbfgs(*args, **kwargs)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_adam_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=_fake_chunked_data_term), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)), \
             mock.patch.object(controller._grad_clipper, "clip", clip_spy), \
             mock.patch("torch.nn.utils.clip_grad_norm_", torch_clip_spy), \
             mock.patch.object(controller, "_run_lbfgs_phase", side_effect=spy_lbfgs):
            controller.run_stage(0)

        self.assertEqual(marker["adam_clip_calls"], 1)
        self.assertEqual(clip_spy.call_count, 0)
        self.assertEqual(torch_clip_spy.call_count, 0)

    def test_build_stage_batch_not_called_inside_lbfgs_closure(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=3, n_adam=1, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_adam_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        real_build = build_stage_batch
        build_spy = mock.Mock(wraps=real_build)
        original_lbfgs = controller._run_lbfgs_phase
        marker = {}

        def spy_lbfgs(*args, **kwargs):
            marker["before"] = build_spy.call_count
            return original_lbfgs(*args, **kwargs)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_adam_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=_fake_chunked_data_term), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)), \
             mock.patch(f"{MODULE}.build_stage_batch", build_spy), \
             mock.patch.object(controller, "_run_lbfgs_phase", side_effect=spy_lbfgs):
            controller.run_stage(0)

        # Exactly ONE additional build_stage_batch call from LBFGS entry
        # onward: the fixed batch drawn once at handoff, OUTSIDE the closure.
        # Multiple internal line-search closure invocations must add none.
        self.assertEqual(build_spy.call_count - marker["before"], 1)

    def test_lambda_frozen_across_lbfgs_queried_once(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=4, n_adam=1, validation_every=10_000,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device

        def fake_adam_compose(batch, anchor_ctx, weights):
            return _canned_loss_terms(model, 1.0, dtype, device)

        real_current = controller._scheduled_weights.current
        recorded = []

        def spy_current(epoch):
            result = real_current(epoch)
            recorded.append(result)
            return result

        original_lbfgs = controller._run_lbfgs_phase
        marker = {}

        def spy_lbfgs(*args, **kwargs):
            marker["start"] = len(recorded)
            return original_lbfgs(*args, **kwargs)

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_adam_compose), \
             mock.patch(f"{MODULE}.accumulate_chunked_data_term", side_effect=_fake_chunked_data_term), \
             mock.patch.object(controller, "_weighted_non_data_terms",
                               side_effect=_make_fake_non_data_terms(controller)), \
             mock.patch.object(controller._scheduled_weights, "current", side_effect=spy_current), \
             mock.patch.object(controller, "_run_lbfgs_phase", side_effect=spy_lbfgs):
            controller.run_stage(0)

        lbfgs_calls = recorded[marker["start"]:]
        self.assertEqual(len(lbfgs_calls), 1)  # queried exactly once, then reused for every closure call
        self.assertFalse(controller._scheduled_weights._frozen)  # rewarm() restored after L-BFGS

    def test_zero_lbfgs_headroom_boundary_advances_when_gate_satisfied(self):
        """CR-02: n_adam == max_epochs with a satisfied gate must ADVANCE.

        Equality is legal (GAP-40-02 → A). Pre-fix code short-circuits to
        HALT without polling StageExitMachine, so this FAILS before the fix.
        """
        controller = _build_controller(
            self._tmpdir.name, max_epochs=6, n_adam=6, validation_every=6,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device
        # Graph-connected constant total: backward succeeds, gradient is zero,
        # parameters never move, EMA relative change is exactly 0 < eps_plateau.
        c = 1.0

        def fake_compose(batch, anchor_ctx, weights):
            total = torch.zeros((), dtype=dtype, device=device) + c
            for p in model.parameters():
                total = total + 0.0 * (p ** 2).sum()
            zero = torch.zeros((), dtype=dtype, device=device)
            return LossTerms(
                data=zero, ic=zero,
                phys=torch.tensor(1e-6, dtype=dtype, device=device),
                energy=torch.tensor(1e-6, dtype=dtype, device=device),
                angmom=zero, total=total,
            )

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_compose):
            disposition = controller.run_stage(0)

        self.assertEqual(disposition, StageDisposition.ADVANCE)
        self.assertIsNotNone(controller.last_handoff_event)
        self.assertEqual(controller.last_handoff_event.trigger, "budget-exhausted")
        self.assertEqual(controller.last_handoff_event.adam_epochs_used, 6)

    def test_zero_lbfgs_headroom_boundary_halts_when_gate_unmet(self):
        """CR-02 mirror: same boundary with one failing criterion → HALT only."""
        controller = _build_controller(
            self._tmpdir.name, max_epochs=6, n_adam=6, validation_every=6,
        )
        model = controller._model
        dtype, device = controller._dtype, controller._device
        c = 1.0

        def fake_compose(batch, anchor_ctx, weights):
            total = torch.zeros((), dtype=dtype, device=device) + c
            for p in model.parameters():
                total = total + 0.0 * (p ** 2).sum()
            zero = torch.zeros((), dtype=dtype, device=device)
            # phys above eps_phys=1e-4 → criterion 3 fails → max-epoch HALT
            return LossTerms(
                data=zero, ic=zero,
                phys=torch.tensor(1.0, dtype=dtype, device=device),
                energy=torch.tensor(1e-6, dtype=dtype, device=device),
                angmom=zero, total=total,
            )

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=fake_compose):
            disposition = controller.run_stage(0)

        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertNotEqual(disposition, StageDisposition.ADVANCE)
        self.assertEqual(controller.last_handoff_event.trigger, "budget-exhausted")
        self.assertEqual(controller.last_handoff_event.adam_epochs_used, 6)


# ---------------------------------------------------------------------------
# Real, non-injected wiring: validation pass + TRAIN-06 criteria producers.
# ---------------------------------------------------------------------------

class RunControllerValidationWiringTests(unittest.TestCase):
    def setUp(self):
        self.RunController = _require("RunController")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_validation_pass_wiring_is_real_and_matches_direct_recompute(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1, validation_every=1,
        )
        captured: dict = {}
        real_build = build_stage_batch

        def spy_build(source, **kwargs):
            result = real_build(source, **kwargs)
            if source is controller._validation_source:
                captured["batch"] = result
            return result

        original_anchor = controller._build_anchor_context

        def spy_anchor(source, batch, fixed_times):
            ctx = original_anchor(source, batch, fixed_times)
            if source is controller._validation_source:
                captured["anchor_ctx"] = ctx
            return ctx

        original_run_validation = controller._run_validation

        def spy_run_validation(k, weights):
            result = original_run_validation(k, weights)
            captured["weights"] = weights
            captured["result"] = result
            return result

        with mock.patch(f"{MODULE}.build_stage_batch", side_effect=spy_build), \
             mock.patch.object(controller, "_build_anchor_context", side_effect=spy_anchor), \
             mock.patch.object(controller, "_run_validation", side_effect=spy_run_validation):
            disposition = controller.run_stage(0)

        self.assertEqual(disposition, StageDisposition.HALT)
        for key in ("batch", "anchor_ctx", "weights", "result"):
            self.assertIn(key, captured, f"validation pass never populated {key!r}")

        direct = controller._compose_loss_terms(
            captured["batch"], captured["anchor_ctx"], captured["weights"]
        )
        recorded = captured["result"]
        torch.testing.assert_close(direct.total, recorded.total)
        torch.testing.assert_close(direct.phys, recorded.phys)
        torch.testing.assert_close(direct.energy, recorded.energy)

    def test_validation_pass_restores_train_mode_even_if_forward_raises(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1, validation_every=1,
        )
        model = controller._model

        def boom(batch, anchor_ctx, weights):
            raise RuntimeError("synthetic validation failure")

        with mock.patch.object(controller, "_compose_loss_terms", side_effect=boom):
            with self.assertRaises(RuntimeError):
                controller._run_validation(0, controller._scheduled_weights.current(0))
        self.assertTrue(model.training)

    def test_physics_term_uses_collocation_sampler_only(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1,
        )
        train_source = controller._train_source
        rng = np.random.default_rng(7)
        batch = build_stage_batch(
            train_source, stage=0, rng=rng,
            dtype=controller._dtype, device=controller._device, collocation_count=1,
        )
        # Poison batch.collocation_points.times -- if the physics/energy/angmom
        # terms ever read it, the result would be non-finite. CollocationSampler
        # is the sole physics-point source, so poisoning this must have no effect.
        poisoned_times = batch.collocation_points.times.clone()
        poisoned_times[:] = float("nan")
        poisoned_batch = replace(
            batch, collocation_points=replace(batch.collocation_points, times=poisoned_times)
        )
        anchor_ctx = controller._build_anchor_context(train_source, poisoned_batch, None)
        weights = controller._scheduled_weights.current(0)
        loss_terms = controller._compose_loss_terms(poisoned_batch, anchor_ctx, weights)
        self.assertTrue(bool(torch.isfinite(loss_terms.total)))
        self.assertTrue(bool(torch.isfinite(loss_terms.phys)))


# ---------------------------------------------------------------------------
# Chunked-accumulation equality (RESEARCH Pitfall 2 / Open Question 2).
# ---------------------------------------------------------------------------

class ChunkedAccumulationTests(unittest.TestCase):
    def setUp(self):
        self.accumulate_chunked_data_term = _require("accumulate_chunked_data_term")

    def test_chunked_accumulation_matches_full_batch_mean_backward(self):
        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        n = 10
        generator = torch.Generator().manual_seed(0)
        tau_ic13 = torch.randn(n, 14, dtype=runtime.dtype, generator=generator)
        masses = torch.rand(n, 3, dtype=runtime.dtype, generator=generator) + 0.5
        targets = torch.randn(n, 9, dtype=runtime.dtype, generator=generator)
        data_points = SimpleNamespace(tau_ic13=tau_ic13, masses=masses, targets=targets)

        for p in model.parameters():
            p.grad = None
        pred = model(tau_ic13, masses)
        full_loss = data_huber_loss(
            pred.reshape(-1, 3, 3), targets.reshape(-1, 3, 3),
            dtype=runtime.dtype, device=runtime.torch_device,
        )
        full_loss.backward()
        full_grads = [
            (p.grad.clone() if p.grad is not None else torch.zeros_like(p))
            for p in model.parameters()
        ]

        for p in model.parameters():
            p.grad = None
        total = self.accumulate_chunked_data_term(
            model, data_points, weight=1.0, chunk_size=3,
            dtype=runtime.dtype, device=runtime.torch_device,
        )
        chunked_grads = [
            (p.grad.clone() if p.grad is not None else torch.zeros_like(p))
            for p in model.parameters()
        ]

        for full_g, chunked_g in zip(full_grads, chunked_grads):
            torch.testing.assert_close(full_g, chunked_g, rtol=1e-6, atol=1e-9)
        torch.testing.assert_close(total, full_loss.detach())

    def test_chunk_size_read_from_config_not_invented(self):
        config = _make_config(max_epochs=1, n_adam=1, lbfgs_chunk_size=17)
        self.assertEqual(config.opt.lbfgs_chunk_size, 17)


class EnergyFloorFactorWiringTests(unittest.TestCase):
    """WR-02: StageConfig.energy_floor_factor must govern eps_h.

    Pre-fix code shadows the config field with a module constant, so two
    controllers that differ only in the factor produce the same eps_h.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def _eps_h_for(self, energy_floor_factor=None):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1,
            energy_floor_factor=energy_floor_factor,
        )
        batch = build_stage_batch(
            controller._train_source, stage=0,
            rng=np.random.default_rng(0),
            dtype=controller._dtype, device=controller._device,
            collocation_count=2,
        )
        fixed_times = np.asarray([0.1, 0.5], dtype=np.float64)
        ctx = controller._build_anchor_context(
            controller._train_source, batch, fixed_times,
        )
        return ctx, controller

    def test_energy_floor_factor_override_changes_eps_h(self):
        default_factor = 1e-4
        override_factor = 1e-1  # mechanism value, not a calibrated level
        ctx_default, _ = self._eps_h_for(energy_floor_factor=default_factor)
        ctx_override, _ = self._eps_h_for(energy_floor_factor=override_factor)

        expected_default = abs(ctx_default.h0) * default_factor + 1e-12
        expected_override = abs(ctx_override.h0) * override_factor + 1e-12
        self.assertAlmostEqual(ctx_default.eps_h, expected_default, places=12)
        self.assertAlmostEqual(ctx_override.eps_h, expected_override, places=12)
        # The override case is the RED assertion: pre-fix both equal 1e-4 * |h0|.
        self.assertNotAlmostEqual(
            ctx_default.eps_h, ctx_override.eps_h, places=12,
            msg="energy_floor_factor override must change eps_h (WR-02)",
        )
        # Same h0 for both (same stub source / batch) so the ratio tracks factors.
        self.assertAlmostEqual(ctx_default.h0, ctx_override.h0, places=12)

    def test_default_energy_floor_factor_matches_pre_fix_scale(self):
        """Shipped default 1e-4 must keep eps_h == |h0|*1e-4 + 1e-12."""
        ctx, controller = self._eps_h_for(energy_floor_factor=None)
        self.assertEqual(controller._config.stage.energy_floor_factor, 1e-4)
        expected = abs(ctx.h0) * 1e-4 + 1e-12
        self.assertAlmostEqual(ctx.eps_h, expected, places=12)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
